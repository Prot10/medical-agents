"""Agent mode: a physician works a case exactly as the agent does.

The tests pin the study's contract: which code opens what, that a physician receives what the
agent receives and nothing else, that the harness (not this app) decides every step, that a case
resumes and locks, that the stored episode is a benchmark episode, and that the MIMIC section
exists only where the deployment configures it.
"""

from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from neuroagent_schemas import ClinicalEpisode, ObservationReceived

from neuroagent.datasets import DATASETS, REPO_ROOT, split_case_ids
from neuroagent.evaluation.benchmark import episode_row
from neuroagent.evaluation.policy_reward import ClinicalPolicyReward
from neuroagent.harness.adapters import SUBMIT_TOOL, NativeToolModelAdapter
from neuroagent.harness.context import POLICY_SYSTEM_PROMPT, format_patient_info
from neuroagent.harness.environment import NeuroBenchEnvironment
from neuroagent.harness.interfaces import RunContext
from neuroagent.harness.loops import ClinicalPolicyLoop
from neuroagent.harness.profile import load_profiles
from neuroagent.llm.client import LLMResponse, LLMToolCall, _wire_messages
from neuroagent.review_api.app import create_app
from neuroagent.review_api.config import AGENT_MODE_SETS_PATH
from neuroagent.review_api.schemas.agent_mode import AgentRecord
from neuroagent.review_api.schemas.reviewers import ReviewerCode
from neuroagent.review_api.services.agent_mode.sets import PROFILES_DIR, load_agent_mode
from neuroagent.review_api.services.annotation_store import AnnotationStore
from neuroagent.review_api.services.reviewer_codes import ReviewerCodeRegistry
from neuroagent.tools.mock_server import MockServer

AGENT, AGENT_BOTH, AGENT_LINKED = "AG-SYNTH-ONLY", "AG-BOTH-SECTIONS", "AG-LINKED-CODE"
REVIEWER, ADMIN = "RV-DATASET-CODE", "AD-ADMIN-CODE-X"
CODES = f"""reviewers:
  - {{code: {AGENT}, name: Dr Synthetic, id: phys-synth, sections: [agent_synthetic]}}
  - {{code: {AGENT_BOTH}, name: Dr Both, id: phys-both, sections: [agent_synthetic, agent_mimic]}}
  - {{code: {AGENT_LINKED}, name: Dr Linked, sections: [agent_synthetic], linked_review_codes: [{REVIEWER.lower()}]}}
  - {{code: {REVIEWER}, name: Dataset Reviewer, role: reviewer}}
  - {{code: {ADMIN}, name: Researcher, role: admin}}
"""
BASE = "/api/v1/agent-mode"
SYNTH = f"{BASE}/sections/synthetic"
ASSESSMENT = {
    "primary_diagnosis": "Hepatic encephalopathy",
    "icd10_code": "K76.82",
    "differential": [{"diagnosis": "Wernicke encephalopathy", "confidence": 0.2}],
    "confidence": 0.7,
    "urgency": "urgent",
    "recommendations": ["Lactulose"],
}
LABS = {"clinical_context": "confusion in cirrhosis", "panels": ["ammonia"]}


def _build(tmp_path: Path, monkeypatch, *, mimic: bool = False):
    monkeypatch.setenv("REVIEW_AGENT_MODE_DIR", str(tmp_path / "records"))
    for name in ("REVIEW_AGENT_MIMIC_CASES_DIR", "REVIEW_AGENT_MIMIC_LOG_DIR", "REVIEW_AGENT_MIMIC_CASE_LIST"):
        monkeypatch.delenv(name, raising=False)
    if mimic:
        monkeypatch.setenv("REVIEW_AGENT_MIMIC_CASES_DIR", str(_stand_in_record_cases(tmp_path / "mimic-cases")))
        monkeypatch.setenv("REVIEW_AGENT_MIMIC_LOG_DIR", str(tmp_path / "mimic-logs"))
    app = create_app()
    codes = tmp_path / "reviewer_codes.yaml"
    codes.write_text(CODES)
    app.state.reviewer_registry = ReviewerCodeRegistry(codes)
    app.state.auth_limiter = None
    app.state.annotations_dir = tmp_path / "annotations"
    app.state.annotation_store = AnnotationStore(app.state.annotations_dir, extra_versions=app.state.review_sets)
    return app


def _stand_in_record_cases(target: Path) -> Path:
    """Synthetic stand-ins for record-derived cases: NeuroBench cases marked ``provenance:
    record`` (which is what MIMIC cases carry), so an order with no stored result is answered
    "not available". No MIMIC file is ever read by a test."""
    (target / "cases").mkdir(parents=True)
    for case_id in ("SAH-M01", "ALS-M01", "MG-S03"):
        data = json.loads((DATASETS["neurobench"].path / "cases" / f"{case_id}.json").read_text())
        data.update(provenance="record", fallback_tool_outputs=None)
        (target / "cases" / f"{case_id}.json").write_text(json.dumps(data))
    return target


@pytest.fixture(scope="module")
def shared_app(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    yield _build(tmp_path_factory.mktemp("agent-mode"), monkeypatch)
    monkeypatch.undo()


@pytest.fixture
def app(shared_app, tmp_path, monkeypatch):
    """The shared app with this test's own record and annotation folders."""
    config = shared_app.state.agent_mode
    section = config.sections["synthetic"]
    fresh = type(section)(**{**{f: getattr(section, f) for f in section.__dataclass_fields__}, "records_dir": tmp_path / "records"})
    monkeypatch.setattr(shared_app.state, "agent_mode", type(config)(config.profile, config.limits_from, config.show_step_budget, {"synthetic": fresh}))
    monkeypatch.setattr(shared_app.state, "annotations_dir", tmp_path / "annotations")
    return shared_app


def _client(app, code: str) -> TestClient:
    client = TestClient(app)
    client.headers["X-Reviewer-Code"] = code
    return client


def _send(client: TestClient, state: dict, name: str, arguments: dict, rationale: str = "to narrow the differential", base: str = SYNTH):
    return client.post(
        f"{base}/cases/{state['number']}/actions",
        json={"expected_step": state["expected_step"], "name": name, "arguments": arguments, "rationale": rationale},
    )


def _record(app, reviewer_id: str, key: str = "synthetic") -> AgentRecord:
    section = app.state.agent_mode.sections[key]
    (record,) = app.state.agent_record_store.records_of(section, reviewer_id).values()
    return record


# ── Access ──────────────────────────────────────────────────────────────────────────────────


def test_existing_code_entries_are_unchanged():
    """A registry row without the new fields is a dataset-review code, as before."""
    code = ReviewerCode.model_validate({"code": "maple-river-stone", "name": "Reviewer 1", "role": "reviewer"})
    assert (code.code, code.sections, code.is_agent_mode, code.linked_review_codes) == ("MAPLE-RIVER-STONE", [], False, [])
    with pytest.raises(ValueError):
        ReviewerCode.model_validate({"code": "X-ADMIN", "name": "A", "role": "admin", "sections": ["agent_synthetic"]})
    with pytest.raises(ValueError):
        ReviewerCode.model_validate({"code": "X-CODE", "name": "A", "sections": ["agent_everything"]})


def test_agent_code_reaches_no_dataset_review_route(app):
    """An agent-mode code never sees the dataset review, a policy or a ground truth: every route
    outside the agent-mode study refuses it."""
    client = _client(app, AGENT)
    assert client.get("/api/v1/reviewers/me").json()["sections"] == ["agent_synthetic"]
    checked = 0
    for route in app.routes:
        path = getattr(route, "path", "")
        if not path.startswith("/api/v1/") or path.startswith(BASE) or path == "/api/v1/reviewers/me":
            continue
        url = path.format(version="neurobench", case_id="SAH-M01", key="synthetic", reviewer_id="phys-synth", number=1,
                          annotation_id="a", comment_id="c", tool_name="analyze_eeg", condition="SAH", set_id="recheck-2026-11",
                          proposal_id="p", field_path="x")
        for method in route.methods - {"HEAD", "OPTIONS"}:
            response = client.request(method, url, json={})
            assert response.status_code == 403, f"{method} {url} -> {response.status_code}"
            checked += 1
    assert checked > 25


def test_dataset_and_admin_codes_cannot_work_cases(app):
    for code in (REVIEWER, ADMIN):
        client = _client(app, code)
        assert client.get(f"{BASE}/sections").status_code == 403
        assert client.post(f"{SYNTH}/cases/1/start").status_code == 403
    assert _client(app, REVIEWER).get("/api/v1/reviewers/me").json()["sections"] == []
    assert _client(app, REVIEWER).get("/api/v1/datasets").status_code == 200
    assert _client(app, AGENT).get("/api/v1/admin/agent-mode/overview").status_code == 403
    assert _client(app, REVIEWER).get("/api/v1/admin/agent-mode/overview").status_code == 403
    assert TestClient(app).get(f"{BASE}/sections").status_code == 401


def test_agent_codes_are_left_out_of_the_dataset_review_admin_views(app):
    text = json.dumps(_client(app, ADMIN).get("/api/v1/admin/datasets/neurobench/progress").json())
    assert "Dataset Reviewer" in text and not any(name in text for name in ("Dr Synthetic", "Dr Both", "Dr Linked"))


# ── The case set ────────────────────────────────────────────────────────────────────────────


def _script(name: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / "agent-platform/scripts/review" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_synthetic_set_is_the_declared_draw_one_case_per_condition(app):
    section = app.state.agent_mode.sections["synthetic"]
    dataset = DATASETS["neurobench"].path
    all_cases = app.state.all_datasets["neurobench"][1]
    assert section.set_id == "agent-synthetic-2026-11-v2" and len(section.case_ids) == 20
    conditions = [section.cases[case_id].condition.value for case_id in section.case_ids]
    assert sorted(conditions) == sorted({case.condition.value for case in all_cases.values()})  # all 20, once each
    # The order follows no grouping a physician could read: not the conditions' order, not the ids'.
    assert conditions != sorted(conditions) and list(section.case_ids) != sorted(section.case_ids)
    # The file records its own rule: the draw script reproduces the list from the seed.
    module = _script("draw_agent_mode_set")
    pool = module.pool(dataset, "all")
    assert len(pool) == 598 and set(pool) == {c for split in ("train", "validation", "test") for c in split_case_ids(dataset, split)}
    drawn = module.draw({c: all_cases[c].condition.value for c in pool}, 1, 20261125)
    assert tuple(drawn) == section.case_ids
    # The frozen copies are the listed cases, and the manifest holds their hashes.
    set_dir = REPO_ROOT / "data/review/sets" / section.set_id
    manifest = json.loads((set_dir / "manifest.json").read_text())
    assert manifest["per_case"] == dict(sorted(section.case_sha256.items())) == module.set_hashes(set_dir / "cases")
    assert not (REPO_ROOT / "data/review/sets/agent-synthetic-2026-11").exists()  # the 8-case set is gone


def test_frozen_set_is_refreshed_from_corrected_cases_without_changing_its_cases(tmp_path):
    """Corrections made after the draw are taken in by re-copying the same case ids; once a
    physician has a record for the set, the refresh is refused."""
    module = _script("draw_agent_mode_set")
    source, sets_dir, records = tmp_path / "source", tmp_path / "sets", tmp_path / "records"
    cases_dir = sets_dir / "demo-set" / "cases"
    source.mkdir()
    cases_dir.mkdir(parents=True)
    for case_id in ("A-S01", "B-S01", "C-S01"):
        (source / f"{case_id}.json").write_text(json.dumps({"case_id": case_id, "v": 1}))
    for case_id in ("A-S01", "B-S01"):
        (cases_dir / f"{case_id}.json").write_text(json.dumps({"case_id": case_id, "v": 1}))
    first = module.write_manifest(cases_dir.parent, set_id="demo-set", action="draw")
    (source / "B-S01.json").write_text(json.dumps({"case_id": "B-S01", "v": 2}))  # corrected later

    result = module.refresh("demo-set", source=source, sets_dir=sets_dir, records_root=records)
    assert result["changed"] == ["B-S01"] and result["cases"] == 2
    assert sorted(p.stem for p in cases_dir.glob("*.json")) == ["A-S01", "B-S01"]  # same cases, C never enters
    assert json.loads((cases_dir / "B-S01.json").read_text())["v"] == 2
    manifest = json.loads((cases_dir.parent / "manifest.json").read_text())
    assert manifest["action"] == "refresh" and manifest["cases_sha256"] == result["cases_sha256"] != first["cases_sha256"]
    assert manifest["per_case"]["A-S01"] == first["per_case"]["A-S01"]

    record = records / "synthetic" / "demo-set" / "phys-01" / "A-S01.json"
    record.parent.mkdir(parents=True)
    record.write_text("{}")
    record.with_suffix(".events.jsonl").write_text("")
    (source / "A-S01.json").write_text(json.dumps({"case_id": "A-S01", "v": 3}))
    with pytest.raises(SystemExit, match="1 physician record"):
        module.refresh("demo-set", source=source, sets_dir=sets_dir, records_root=records)
    assert json.loads((cases_dir / "A-S01.json").read_text())["v"] == 1
    assert module.refresh("demo-set", source=source, sets_dir=sets_dir, records_root=records, force=True)["changed"] == ["A-S01"]
    (source / "B-S01.json").unlink()
    with pytest.raises(SystemExit, match="no longer in"):
        module.refresh("demo-set", source=source, sets_dir=sets_dir, records_root=records, force=True)
    with pytest.raises(SystemExit, match="no frozen set"):
        module.refresh("other-set", source=source, sets_dir=sets_dir, records_root=records)


def test_limits_are_those_of_the_checked_policy_profile(app):
    config = app.state.agent_mode
    profile = load_profiles(PROFILES_DIR)["policy-qwen3.5-9b"]
    assert (config.profile.max_turns, config.profile.max_cost_usd, config.profile.max_invalid_actions) == (
        profile.max_turns, profile.max_cost_usd, profile.max_invalid_actions,
    )


# ── Exactly what the agent sees ─────────────────────────────────────────────────────────────


class _ScriptedModel:
    """A model server that emits a fixed list of tool calls and keeps the requests it received."""

    model = "scripted"

    def __init__(self, calls):
        self.calls, self.requests = list(calls), []

    def chat(self, messages, *, tools=None, tool_choice=None):
        self.requests.append({"messages": _wire_messages(messages), "tools": tools})
        name, arguments = self.calls.pop(0)
        return LLMResponse(tool_calls=[LLMToolCall(id="x", name=name, arguments=arguments)])


def _comparable(episode: ClinicalEpisode) -> list[dict]:
    drop = {"event_id", "timestamp", "latency_seconds", "model_id", "profile_id", "plugin_versions"}
    return [{k: v for k, v in event.model_dump(mode="json").items() if k not in drop} for event in episode.events]


def test_physician_receives_exactly_the_requests_a_model_receives(app):
    """The same actions, sent by a physician through the app and by a model through the policy
    loop, meet the same request at every step (messages and tool list, byte for byte) and leave
    the same episode: catalogue, presentation, observations, error texts and corrections."""
    calls = [
        ("interpret_labs", LABS),
        ("interpret_labs", {"clinical_context": "x", "panels": ["not_an_assay"]}),  # refused by the tool's schema
        ("order_everything", {}),  # no such tool: refused by the adapter, no turn spent
        ("analyze_eeg", {"clinical_context": "encephalopathy"}),
        ("submit_assessment", ASSESSMENT),
    ]
    config = app.state.agent_mode
    case = config.sections["synthetic"].case_at(1)

    model = _ScriptedModel(calls)
    context = RunContext(
        profile_id="policy-qwen3.5-9b", model=NativeToolModelAdapter(model), loop=ClinicalPolicyLoop(),
        environment=NeuroBenchEnvironment(case), max_turns=config.profile.max_turns,
        max_cost_usd=config.profile.max_cost_usd, max_invalid_actions=config.profile.max_invalid_actions,
    )
    model_episode = context.loop.run(context)

    client = _client(app, AGENT)
    state = client.post(f"{SYNTH}/cases/1/start").json()
    assert state["tools"] == [*NeuroBenchEnvironment(case).tool_definitions(), SUBMIT_TOOL]
    assert state["presentation"] == format_patient_info(case)
    assert state["instructions"] == POLICY_SYSTEM_PROMPT
    shown = []
    for name, arguments in calls:
        shown.append(state["raw"])
        state = _send(client, state, name, arguments).json()
    assert shown == model.requests
    assert state["status"] == "completed"

    record = _record(app, "phys-synth")
    assert _comparable(record.episode) == _comparable(model_episode)
    assert record.episode.events[0].model_id == "physician:phys-synth"
    assert [step.outcome for step in record.steps] == ["observed", "schema_rejected", "action_rejected", "observed", "assessment"]


def test_readable_view_carries_the_agent_facing_content(app):
    client = _client(app, AGENT)
    state = client.post(f"{SYNTH}/cases/1/start").json()
    state = _send(client, state, "interpret_labs", LABS, "ammonia first").json()
    state = _send(client, state, "analyze_eeg", {}, "forgot the context").json()
    tool_messages = [m["content"] for m in state["raw"]["messages"] if m["role"] == "tool"]
    assert [entry["observation_text"] for entry in state["timeline"]] == tool_messages
    assert [json.dumps(entry["observation"], sort_keys=True) for entry in state["timeline"]] == tool_messages
    assert state["timeline"][0]["rationale"] == "ammonia first"
    # The invalid order is answered as the agent's is: an error observation that spends the turn.
    assert state["timeline"][1]["observation"] == {
        "tool_name": "analyze_eeg", "success": False, "output": None,
        "error_message": "analyze_eeg: 'clinical_context' is a required property",
    }
    assert state["turn"] == 3


def _walk(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


def test_nothing_the_agent_does_not_see_reaches_the_physician(app):
    """No case id, condition, policy, ground truth or cost in anything a physician's code can
    fetch; cases are addressed by their number in the set."""
    client = _client(app, AGENT)
    section = app.state.agent_mode.sections["synthetic"]
    case = section.case_at(1)
    responses = [client.get(f"{BASE}/sections").json(), client.get(SYNTH).json()]
    state = client.post(f"{SYNTH}/cases/1/start").json()
    responses.append(state)
    for name, arguments in (("interpret_labs", LABS), ("analyze_brain_mri", {"clinical_context": "x"}), ("submit_assessment", ASSESSMENT)):
        state = _send(client, state, name, arguments).json()
        responses.append(state)
    responses += [client.get(f"{SYNTH}/cases/1").json(), client.get(SYNTH).json()]
    text = json.dumps(responses)
    for case_id in section.case_ids:
        assert case_id not in text
    assert case.condition.value not in text
    keys = set(_walk(responses))
    assert not keys & {"case_id", "condition", "ground_truth", "policy", "cost_usd", "difficulty", "reward", "provenance", "from_fallback", "library"}
    # After the assessment: locked, no feedback, the next case offered.
    assert set(responses[-2]) == {"section", "number", "status", "expected_step", "next", "failure"}
    assert responses[-2]["next"] == 2
    assert client.get(f"{SYNTH}/cases/HEP-ENC-P05").status_code == 422  # ids are not addresses


def test_step_budget_is_not_shown_because_the_agent_is_not_told(app):
    state = _client(app, AGENT).post(f"{SYNTH}/cases/1/start").json()
    assert state["max_turns"] is None and "12" not in state["instructions"]


# ── Same constraints ────────────────────────────────────────────────────────────────────────


def test_last_turn_must_be_the_assessment_and_invalid_actions_end_the_case(app):
    client = _client(app, AGENT)
    max_turns = app.state.agent_mode.profile.max_turns
    state = client.post(f"{SYNTH}/cases/1/start").json()
    for turn in range(1, max_turns):
        assert state["require_assessment"] is False and state["notice"] is None
        state = _send(client, state, "analyze_ecg", {"clinical_context": f"order {turn}"}).json()
    assert state["turn"] == max_turns and state["require_assessment"] is True
    assert state["notice"] == "This is the final turn: call submit_assessment now with the structured assessment."
    assert state["raw"]["messages"][-1]["content"].endswith(state["notice"])
    # An order on the final turn is rejected as the agent's is, and counted.
    state = _send(client, state, "analyze_ecg", {"clinical_context": "one more"}).json()
    assert state["invalid_actions"] == 1 and len(state["timeline"]) == max_turns - 1
    assert state["notice"].startswith("The previous response was invalid: a final assessment is required on this turn.")
    state = _send(client, state, "analyze_ecg", {"clinical_context": "again"}).json()
    state = _send(client, state, "analyze_ecg", {"clinical_context": "and again"}).json()
    # The invalid-action budget of the profile is spent: the episode fails, as a model's does.
    assert state["status"] == "failed" and state["failure"]["reason"] == "invalid_action"
    record = _record(app, "phys-synth")
    assert record.episode.events[-1].type == "run.failed" and record.invalid_attempts == 3
    # A failed episode stays in the denominator: the admin view scores it like a failed model run.
    (episode,) = _client(app, ADMIN).get("/api/v1/admin/agent-mode/overview").json()["sections"][0]["episodes"]
    assert episode["status"] == "failed" and episode["row"]["failure_reason"] == "invalid_action"
    assert episode["row"]["reward"]["diagnosis"] == 0


def test_invalid_assessment_is_rejected_by_the_harness_not_by_the_app(app):
    client = _client(app, AGENT)
    state = client.post(f"{SYNTH}/cases/1/start").json()
    response = _send(client, state, "submit_assessment", {**ASSESSMENT, "urgency": "whenever"}, "reasoning")
    assert response.status_code == 200
    state = response.json()
    assert state["status"] == "in_progress" and state["invalid_actions"] == 1 and "urgency" in state["notice"]
    assert _send(client, state, "submit_assessment", ASSESSMENT, "reasoning").json()["status"] == "completed"


def test_rationale_is_required_and_stored_apart_from_the_episode(app):
    client = _client(app, AGENT)
    state = client.post(f"{SYNTH}/cases/1/start").json()
    assert _send(client, state, "interpret_labs", LABS, "   ").status_code == 422
    assert client.post(f"{SYNTH}/cases/1/actions", json={"expected_step": 0, "name": "interpret_labs", "arguments": LABS}).status_code == 422
    state = _send(client, state, "interpret_labs", LABS, "Ammonia: cirrhosis and confusion").json()
    _send(client, state, "submit_assessment", ASSESSMENT, "Asterixis, raised ammonia, precipitant found")
    record = _record(app, "phys-synth")
    assert [step.rationale for step in record.steps] == ["Ammonia: cirrhosis and confusion", "Asterixis, raised ammonia, precipitant found"]
    assert record.diagnostic_reasoning == "Asterixis, raised ammonia, precipitant found"
    assert "Asterixis" not in record.episode.model_dump_json() and "Ammonia: cirrhosis" not in record.episode.model_dump_json()


# ── Resume, lock, order ─────────────────────────────────────────────────────────────────────


def test_case_resumes_where_it_was_and_orders_cannot_be_undone(app, monkeypatch):
    client = _client(app, AGENT)
    state = client.post(f"{SYNTH}/cases/1/start").json()
    state = _send(client, state, "interpret_labs", LABS).json()
    # A new browser session: same code, nothing kept client-side.
    again = _client(app, AGENT)
    assert again.get(SYNTH).json()["current"] == 1
    assert again.get(f"{SYNTH}/cases/1").json() == state
    assert again.post(f"{SYNTH}/cases/1/start").json() == state  # starting again never resets
    # A stale page (double click, second tab) cannot send the same step twice.
    stale = {**state, "expected_step": 0}
    assert _send(again, stale, "analyze_ecg", {"clinical_context": "x"}).status_code == 409
    # What was shown stays what was shown, even if the environment would answer differently now.
    monkeypatch.setattr(MockServer, "get_output", lambda *a, **k: pytest.fail("a recorded order was executed again"))
    assert again.get(f"{SYNTH}/cases/1").json()["timeline"] == state["timeline"]
    for method in ("put", "patch", "delete"):
        assert getattr(again, method)(f"{SYNTH}/cases/1").status_code == 405


def test_case_is_locked_after_the_assessment_and_cases_go_in_order(app):
    client = _client(app, AGENT)
    assert client.post(f"{SYNTH}/cases/2/start").status_code == 409
    assert client.get(f"{SYNTH}/cases/1").status_code == 404
    state = client.post(f"{SYNTH}/cases/1/start").json()
    assert client.post(f"{SYNTH}/cases/2/start").status_code == 409  # one case at a time
    done = _send(client, state, "submit_assessment", ASSESSMENT, "enough on presentation").json()
    assert done["status"] == "completed" and done["next"] == 2
    assert _send(client, done, "interpret_labs", LABS).status_code == 409
    assert _send(client, done, "submit_assessment", ASSESSMENT).status_code == 409
    listing = client.get(SYNTH).json()
    assert [c["status"] for c in listing["cases"][:2]] == ["done", "todo"] and listing["done"] == 1
    assert client.post(f"{SYNTH}/cases/2/start").json()["status"] == "in_progress"
    assert client.post(f"{SYNTH}/cases/99/start").status_code == 404


def test_cases_reviewed_under_a_linked_code_are_skipped(app):
    """A physician who reviewed a case in the dataset review knows its diagnosis."""
    section = app.state.agent_mode.sections["synthetic"]
    reviewed = app.state.annotations_dir / "recheck-2026-11" / REVIEWER
    reviewed.mkdir(parents=True)
    (reviewed / f"{section.case_ids[0]}.json").write_text("{}")
    (app.state.annotations_dir / "neurobench" / REVIEWER).mkdir(parents=True)
    (app.state.annotations_dir / "neurobench" / REVIEWER / f"{section.case_ids[2]}.json").write_text("{}")
    linked = _client(app, AGENT_LINKED).get(SYNTH).json()
    assert [c["number"] for c in linked["cases"]] == [2, *range(4, 21)] and linked["current"] == 2
    assert _client(app, AGENT_LINKED).post(f"{SYNTH}/cases/1/start").status_code == 409
    assert len(_client(app, AGENT).get(SYNTH).json()["cases"]) == 20


# ── Storage ─────────────────────────────────────────────────────────────────────────────────


def test_record_is_a_benchmark_episode_with_physician_data_and_provenance(app):
    client = _client(app, AGENT)
    state = client.post(f"{SYNTH}/cases/1/start").json()
    telemetry = {"active_seconds": 41.5, "tools_opened": ["analyze_eeg", "interpret_labs"], "searches": ["ammonia"], "raw_view_opened": True, "keystrokes": "ignored"}
    response = client.post(f"{SYNTH}/cases/1/actions", json={"expected_step": 0, "name": "interpret_labs", "arguments": LABS, "rationale": "why", "telemetry": telemetry})
    _send(client, response.json(), "submit_assessment", ASSESSMENT, "reasoning")

    section = app.state.agent_mode.sections["synthetic"]
    case = section.case_at(1)
    path = app.state.agent_record_store.path(section, "phys-synth", case.case_id)
    assert path.parent == section.records_dir / "synthetic" / section.set_id / "phys-synth"
    assert AGENT not in path.read_text() and AGENT not in str(path), "the secret code is never stored"
    record = AgentRecord.model_validate_json(path.read_text())

    # The episode is the benchmark's: same event types, scored by the same scorer, unchanged.
    episode = ClinicalEpisode.model_validate(json.loads(path.read_text())["episode"])
    assert [e.type for e in episode.events] == [
        "run.started", "model.requested", "action.proposed", "observation.received",
        "model.requested", "action.proposed", "assessment.submitted", "run.completed",
    ]
    assert episode.events[0].case_id == case.case_id and episode.events[0].profile_id == "policy-physician"
    row = episode_row(case, episode, ClinicalPolicyReward(require_approved=False))
    assert row["status"] == "completed" and 0 <= row["reward"]["scalar"] <= 1 and row["tools_called"] == ["interpret_labs"]
    with pytest.raises(ValueError):  # a draft policy stays unscoreable without the engineering flag
        ClinicalPolicyReward().score(episode, case)

    step = record.steps[0]
    assert (step.client.active_seconds, step.client.tools_opened, step.client.searches, step.client.raw_view_opened) == (41.5, ["analyze_eeg", "interpret_labs"], ["ammonia"], True)
    assert step.shown_at == record.started_at and step.sent_at >= step.shown_at and step.server_seconds >= 0
    assert episode.events[2].latency_seconds == step.latency_seconds <= step.server_seconds

    provenance = record.provenance
    assert provenance["case"]["file_sha256"] == section.case_sha256[case.case_id]
    assert provenance["set"] == {"section": "synthetic", "id": section.set_id, "sha256": section.set_sha256, "cases": 20}
    assert provenance["profile"]["limits_from"] == "policy-qwen3.5-9b" and provenance["profile"]["max_turns"] == 12
    assert set(provenance["agent_facing"]) == {"system_prompt_sha256", "presentation_sha256", "catalogue_sha256", "tools", "show_step_budget"}
    assert provenance["app"]["version"] and "commit" in provenance["app"]["git"]

    # The append-only log keeps every request as received.
    log = [json.loads(line) for line in path.with_suffix(".events.jsonl").read_text().splitlines()]
    assert any(entry["type"] == "state.viewed" for entry in log)
    log = [entry for entry in log if entry["type"] != "state.viewed"]
    assert [entry["type"] for entry in log] == [
        "case.started", "action.received", "action.outcome", "action.received", "action.outcome",
    ]
    assert log[1]["body"]["rationale"] == "why"


def test_admin_sees_progress_and_the_reward_from_the_same_scorer(app):
    client = _client(app, AGENT)
    state = client.post(f"{SYNTH}/cases/1/start").json()
    state = _send(client, state, "interpret_labs", LABS).json()
    _send(client, state, "submit_assessment", ASSESSMENT, "reasoning")
    client.post(f"{SYNTH}/cases/2/start")

    overview = _client(app, ADMIN).get("/api/v1/admin/agent-mode/overview").json()
    (section,) = overview["sections"]
    people = {row["reviewer_id"]: row for row in section["reviewers"]}
    assert people["phys-synth"] | {"name": "Dr Synthetic"} == {
        "reviewer_id": "phys-synth", "name": "Dr Synthetic", "active": True, "assigned": 20, "done": 1, "failed": 0, "in_progress": 1,
    }
    assert people["phys-both"]["done"] == 0
    finished, open_case = section["episodes"]
    record = _record_for(app, "phys-synth", finished["case_id"])
    case = app.state.agent_mode.sections["synthetic"].cases[finished["case_id"]]
    expected = ClinicalPolicyReward(require_approved=False).score(record.episode, case).model_dump(mode="json")
    assert finished["row"]["reward"] == expected
    # Draft policies are scored with the engineering flag and labelled as not reportable.
    assert finished["row"]["policy_review"] == "draft" and finished["row"]["reportable"] is False
    assert open_case["status"] == "in_progress" and open_case["row"] is None

    detail = _client(app, ADMIN).get("/api/v1/admin/agent-mode/sections/synthetic/reviewers/phys-synth/cases/1").json()
    assert detail["diagnostic_reasoning"] == "reasoning" and detail["assessment"]["primary_diagnosis"] == ASSESSMENT["primary_diagnosis"]
    assert detail["timeline"][0]["rationale"] and detail["provenance"]["case"]["file_sha256"]


def _record_for(app, reviewer_id: str, case_id: str) -> AgentRecord:
    section = app.state.agent_mode.sections["synthetic"]
    return app.state.agent_record_store.load(section, reviewer_id, case_id)


def test_export_writes_a_benchmark_run_folder_per_physician(app, tmp_path):
    client = _client(app, AGENT)
    state = client.post(f"{SYNTH}/cases/1/start").json()
    state = _send(client, state, "interpret_labs", LABS).json()
    _send(client, state, "submit_assessment", ASSESSMENT, "reasoning")
    module = _script("export_physician_episodes")
    section = app.state.agent_mode.sections["synthetic"]
    with pytest.raises(ValueError):  # draft policies need the explicit flag, as in the benchmark
        module.export_section(section, tmp_path / "strict", limits={}, allow_draft=False)
    assert module.export_section(section, tmp_path / "out", limits={"max_turns": 12}, allow_draft=True) == {"phys-synth": 1}
    run = tmp_path / "out" / "phys-synth"
    case_id = section.case_ids[0]
    assert ClinicalEpisode.model_validate_json((run / "episodes" / f"{case_id}.json").read_text()).assessment
    (row,) = [json.loads(line) for line in (run / "rewards.jsonl").read_text().splitlines()]
    # The row is the benchmark's row for a model episode: same keys.
    assert set(row) == {"case_id", "condition", "difficulty", "encounter_type", "status", "failure_reason", "invalid_actions",
                        "tool_calls", "tools_called", "primary_diagnosis", "total_cost_usd", "total_tokens",
                        "model_latency_seconds", "reward"}
    summary = json.loads((run / "summary.json").read_text())
    assert summary["model_id"] == "physician:phys-synth" and summary["policy_review"] == "draft (not reportable)"
    assert json.loads((run / "manifest.json").read_text())["cases"]["n"] == 1
    (physician,) = [json.loads(line) for line in (run / "physician.jsonl").read_text().splitlines()]
    assert physician["diagnostic_reasoning"] == "reasoning" and "episode" not in physician


# ── MIMIC ───────────────────────────────────────────────────────────────────────────────────


def test_mimic_section_does_not_exist_unless_the_deployment_configures_it(app):
    assert set(app.state.agent_mode.sections) == {"synthetic"}
    both = _client(app, AGENT_BOTH)  # even a code that lists the section
    assert [s["section"] for s in both.get(f"{BASE}/sections").json()] == ["synthetic"]
    assert both.get(f"{BASE}/sections/mimic").status_code == 404
    assert both.post(f"{BASE}/sections/mimic/cases/1/start").status_code == 404
    assert [s["key"] for s in _client(app, ADMIN).get("/api/v1/admin/agent-mode/overview").json()["sections"]] == ["synthetic"]


def test_mimic_section_served_from_the_configured_directories_only(tmp_path, monkeypatch):
    """Built with synthetic stand-ins marked ``provenance: record``; no MIMIC file is read."""
    app = _build(tmp_path, monkeypatch, mimic=True)
    section = app.state.agent_mode.sections["mimic"]
    assert section.record_derived and len(section.case_ids) == 3
    assert sorted(section.case_ids) == ["ALS-M01", "MG-S03", "SAH-M01"]

    # A code sees only the sections listed for it.
    assert [s["section"] for s in _client(app, AGENT).get(f"{BASE}/sections").json()] == ["synthetic"]
    assert _client(app, AGENT).get(f"{BASE}/sections/mimic").status_code == 404
    both = _client(app, AGENT_BOTH)
    assert [s["section"] for s in both.get(f"{BASE}/sections").json()] == ["synthetic", "mimic"]

    mimic = f"{BASE}/sections/mimic"
    state = both.post(f"{mimic}/cases/1/start").json()
    case = section.case_at(1)
    assert state["presentation"] == format_patient_info(case)
    # An order the recorded admission never placed is answered "not available", as for the agent.
    state = _send(both, state, "analyze_csf", {"clinical_context": "x"}, base=mimic).json()
    observation = state["timeline"][0]["observation"]
    stored = _record(app, "phys-both", "mimic").episode.events
    assert [e.unavailable for e in stored if isinstance(e, ObservationReceived)] == [True]
    assert observation["success"] is False and "not available" in json.dumps(observation).lower()
    _send(both, state, "submit_assessment", ASSESSMENT, "reasoning", base=mimic)

    # Record-derived logs are written under the configured directory and nowhere else.
    written = sorted(p.relative_to(tmp_path).parts[0] for p in tmp_path.rglob("*.json*") if case.case_id in p.name)
    assert set(written) == {"mimic-cases", "mimic-logs"}
    assert not (tmp_path / "records").exists()
    assert (tmp_path / "mimic-logs" / "mimic" / section.set_id / "phys-both" / f"{case.case_id}.json").exists()

    # The two sections stay apart: their records never share a directory, the admin view lists
    # each section with its own episodes, and an export covers one section at a time.
    synthetic = app.state.agent_mode.sections["synthetic"]
    state = both.post(f"{SYNTH}/cases/1/start").json()
    _send(both, state, "submit_assessment", ASSESSMENT, "reasoning")
    assert synthetic.records_dir == tmp_path / "records" and section.records_dir == tmp_path / "mimic-logs"
    assert not list((tmp_path / "records").rglob(f"{case.case_id}*"))
    assert not list((tmp_path / "mimic-logs").rglob(f"{synthetic.case_ids[0]}*"))
    overview = {s["key"]: s for s in _client(app, ADMIN).get("/api/v1/admin/agent-mode/overview").json()["sections"]}
    assert list(overview) == ["synthetic", "mimic"] and overview["mimic"]["record_derived"] is True
    assert [e["case_id"] for e in overview["mimic"]["episodes"]] == [case.case_id]
    assert [e["case_id"] for e in overview["synthetic"]["episodes"]] == [synthetic.case_ids[0]]
    assert {r["reviewer_id"] for r in overview["mimic"]["reviewers"]} == {"phys-both"}  # only codes listing the section
    assert overview["mimic"]["episodes"][0]["row"]["reward"]["scalar"] >= 0
    admin = _client(app, ADMIN)
    assert admin.get("/api/v1/admin/agent-mode/sections/mimic/reviewers/phys-both/cases/1").json()["case_id"] == case.case_id
    assert admin.get("/api/v1/admin/agent-mode/sections/synthetic/reviewers/phys-both/cases/1").json()["case_id"] == synthetic.case_ids[0]

    module = _script("export_physician_episodes")
    # The MIMIC export goes only where the command line says, and never inside the repository.
    with pytest.raises(SystemExit, match="never written inside the repository"):
        module.export_section(section, REPO_ROOT / "outputs" / "physicians-mimic", limits={}, allow_draft=True)
    assert not (REPO_ROOT / "outputs" / "physicians-mimic").exists()
    assert module.export_section(section, tmp_path / "mimic-export", limits={}, allow_draft=True) == {"phys-both": 1}
    assert [p.stem for p in (tmp_path / "mimic-export" / "phys-both" / "episodes").glob("*.json")] == [case.case_id]
    assert module.export_section(synthetic, tmp_path / "synthetic-export", limits={}, allow_draft=True) == {"phys-both": 1}
    assert [p.stem for p in (tmp_path / "synthetic-export" / "phys-both" / "episodes").glob("*.json")] == [synthetic.case_ids[0]]


def test_vps_deployment_keeps_mimic_outside_the_repo_tree():
    """On the VPS the MIMIC cases and records live beside the repo, not in it: the unit reads
    their location from a file there, may write only the records, and the deploy script never
    acts on that directory."""
    hostinger = REPO_ROOT / "deployment" / "hostinger"
    unit = (hostinger / "neurobench-review.service").read_text()
    assert "ProtectHome=read-only" in unit
    assert "EnvironmentFile=-/home/neuroreview/mimic-agent-mode/agent-mode.env" in unit
    assert "ReadWritePaths=-/home/neuroreview/mimic-agent-mode/records" in unit
    assert "mimic-agent-mode/cases" not in "".join(line for line in unit.splitlines() if line.startswith("ReadWritePaths"))
    deploy = [line for line in (hostinger / "deploy.sh").read_text().splitlines() if not line.lstrip().startswith("#")]
    assert not any("mimic" in line.lower() for line in deploy)
    push = (hostinger / "push-mimic-cases.sh").read_text()
    assert 'REMOTE_ROOT="/home/${VPS_USER}/mimic-agent-mode"' in push and "medical-agents" not in push
    assert "/eos/" not in push, "the source folder is an argument, never a path written in the repo"
    # Only the drawn cases leave EOS: the copy sends the files the draw listed, nothing else.
    assert "draw_mimic_set.py" in push and "--files-from=-" in push
    assert not [line for line in push.splitlines() if "rsync" in line and "--include" in line]
    assert "REVIEW_AGENT_MIMIC_CASE_LIST=$REMOTE_ROOT/case-list.txt" in push


MIMIC_COUNTS = {"ISCH": 38, "MS": 22, "SAH": 12, "HEP": 10, "SE": 9, "GBS": 3, "FND": 2, "FEPI": 2, "BACT": 2}
MIMIC_DRAW = {"ISCH": 6, "MS": 4, "SAH": 2, "HEP": 2, "SE": 2, "GBS": 1, "FND": 1, "FEPI": 1, "BACT": 1}


def _fake_hundred(folder: Path) -> dict[str, str]:
    """A folder shaped like the final 100: stand-in files holding a case id and a condition."""
    folder.mkdir(parents=True)
    conditions = {}
    for condition, size in MIMIC_COUNTS.items():
        for index in range(size):
            case_id = f"STANDIN-{condition}-{index:03d}"
            conditions[case_id] = condition
            (folder / f"{case_id}.json").write_text(json.dumps({"case_id": case_id, "condition": condition, "text": "PRIVATE"}))
    return conditions


def test_mimic_draw_is_stratified_by_condition_and_computed_from_the_cases(tmp_path, capsys):
    """One per condition present, the rest in proportion by largest remainder, then seeded draws.
    Run on a fake 100-case folder of stand-ins with the counts of the final cases."""
    module = _script("draw_mimic_set")
    conditions = _fake_hundred(tmp_path / "final")
    assert module.allocate(MIMIC_COUNTS, 20) == MIMIC_DRAW
    # Computed, not written down: other folders give other allocations, never more than a condition has.
    assert module.allocate({"A": 1, "B": 1, "C": 30}, 20) == {"A": 1, "B": 1, "C": 18}
    assert module.allocate({"A": 50, "B": 50}, 20) == {"A": 10, "B": 10}
    assert module.allocate({"A": 2, "B": 2}, 4) == {"A": 2, "B": 2}
    with pytest.raises(ValueError):
        module.allocate({"A": 5, "B": 5, "C": 5}, 2)

    lists = [tmp_path / "list.txt", tmp_path / "copy.txt"]
    assert module.main([str(tmp_path / "final"), "--seed", "20261125", "--write", str(lists[0]), "--write", str(lists[1])]) == 0
    drawn = lists[0].read_text().split()
    assert lists[1].read_text() == lists[0].read_text()
    assert len(drawn) == len(set(drawn)) == 20 and set(drawn) <= set(conditions)
    assert Counter(conditions[case_id] for case_id in drawn) == MIMIC_DRAW
    order = [conditions[case_id] for case_id in drawn]
    assert order != sorted(order)  # not grouped by condition
    # Same seed, same set; another seed, another set with the same allocation.
    assert module.draw(conditions, 20, 20261125)[0] == drawn
    other, allocation = module.draw(conditions, 20, 7)
    assert other != drawn and allocation == MIMIC_DRAW
    # Only counts per condition are printed: no case id, no case text.
    printed = capsys.readouterr().out
    assert "ISCH" in printed and "6 of 38" in printed
    assert "STANDIN-" not in printed and "PRIVATE" not in printed

    (tmp_path / "final" / "odd.json").write_text(json.dumps({"case_id": "SOMETHING-ELSE", "condition": "MS"}))
    assert module.main([str(tmp_path / "final"), "--seed", "1"]) == 1
    assert "odd" not in capsys.readouterr().err


def test_push_script_dry_run_draws_and_prints_counts_only(tmp_path):
    """The script's own path up to the copy, on the stand-in folder: it draws, prints counts per
    condition, writes nothing and contacts no server."""
    import subprocess

    _fake_hundred(tmp_path / "eos" / "final")
    script = REPO_ROOT / "deployment" / "hostinger" / "push-mimic-cases.sh"
    run = subprocess.run(["bash", str(script), "--dry-run", str(tmp_path / "eos" / "final")],
                         capture_output=True, text=True, env={"PATH": "/usr/bin:/bin", "VPS_HOST": "unreachable.invalid"})
    assert run.returncode == 0, run.stderr
    assert "6 of 38" in run.stdout and "Dry run: nothing written, nothing copied" in run.stdout
    assert "STANDIN-" not in run.stdout + run.stderr and "PRIVATE" not in run.stdout + run.stderr
    assert sorted(p.name for p in (tmp_path / "eos").iterdir()) == ["final"]  # no list written
    (tmp_path / "eos" / "final" / "STANDIN-MS-000.json").unlink()
    run = subprocess.run(["bash", str(script), "--dry-run", str(tmp_path / "eos" / "final")],
                         capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    assert run.returncode == 1 and "99 (expected 100)" in run.stdout


def test_mimic_section_serves_the_drawn_list_in_its_order(tmp_path, monkeypatch):
    cases = _stand_in_record_cases(tmp_path / "mimic-cases")
    case_list = tmp_path / "case-list.txt"
    case_list.write_text("MG-S03\nSAH-M01\n")  # two of the three files, in the drawn order
    env = {"REVIEW_AGENT_MIMIC_CASES_DIR": str(cases), "REVIEW_AGENT_MIMIC_LOG_DIR": str(tmp_path / "logs"),
           "REVIEW_AGENT_MIMIC_CASE_LIST": str(case_list)}
    section = load_agent_mode(AGENT_MODE_SETS_PATH, records_root=tmp_path, env=env).sections["mimic"]
    assert section.case_ids == ("MG-S03", "SAH-M01")
    case_list.write_text("MG-S03\nNOT-THERE\n")
    with pytest.raises(ValueError, match="1 unknown"):
        load_agent_mode(AGENT_MODE_SETS_PATH, records_root=tmp_path, env=env)


def test_mimic_directories_inside_the_repository_are_refused(tmp_path):
    env = {"REVIEW_AGENT_MIMIC_CASES_DIR": str(tmp_path), "REVIEW_AGENT_MIMIC_LOG_DIR": str(REPO_ROOT / "data/review/agent-mode")}
    with pytest.raises(ValueError, match="outside the repository"):
        load_agent_mode(AGENT_MODE_SETS_PATH, records_root=tmp_path, env=env)
    with pytest.raises(ValueError, match="needs both"):
        load_agent_mode(AGENT_MODE_SETS_PATH, records_root=tmp_path, env={"REVIEW_AGENT_MIMIC_CASES_DIR": str(tmp_path)})


def test_invalid_record_case_is_reported_without_its_content(tmp_path):
    (tmp_path / "bad.json").write_text(json.dumps({"case_id": "X-1", "patient": {"chief_complaint": "SECRET-TEXT"}}))
    env = {"REVIEW_AGENT_MIMIC_CASES_DIR": str(tmp_path), "REVIEW_AGENT_MIMIC_LOG_DIR": str(tmp_path / "logs")}
    with pytest.raises(ValueError) as error:
        load_agent_mode(AGENT_MODE_SETS_PATH, records_root=tmp_path, env=env)
    assert "bad.json" in str(error.value) and "SECRET-TEXT" not in str(error.value)
