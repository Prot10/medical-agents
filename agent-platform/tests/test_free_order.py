"""Free-order ablation: one free-text tool, orders translated onto the catalogue, same reward."""

from __future__ import annotations

import json
from pathlib import Path

from neuroagent.evaluation.policy_reward import ClinicalPolicyReward
from neuroagent.harness import (
    FREE_ORDER_SYSTEM_PROMPT,
    FreeOrderGatekeeper,
    FreeOrderLoop,
    ModelTurn,
    NativeToolModelAdapter,
    NeuroBenchEnvironment,
    RunContext,
    transcript,
    typed_episode,
)
from neuroagent.harness.context import SUBMIT_NAME
from neuroagent.harness.free_order import (
    OFF_CATALOGUE_TOOL,
    REQUEST_TEST_NAME,
    TRANSLATION_NAMESPACE,
    UNPLACED_TOOL,
)
from neuroagent.llm.client import LLMResponse, LLMToolCall
from neuroagent_schemas import (
    ActionImportance,
    NeuroBenchCase,
    ObservationReceived,
    PluginEvent,
    RunCompleted,
    SubmitAssessment,
    ToolAction,
)

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = ROOT / "data/neurobench/cases/SE-M02.json"


def load_case() -> NeuroBenchCase:
    return NeuroBenchCase.model_validate_json(CASE_PATH.read_text())


def required_alternative(case: NeuroBenchCase):
    criterion = next(c for c in case.ground_truth.action_criteria if c.importance is ActionImportance.REQUIRED)
    return criterion, criterion.alternatives[0]


def call_arguments(alternative) -> dict:
    """The arguments a translator gives: the policy's required ones plus the order text."""
    return {"clinical_context": "the study", **alternative.required_arguments}


class ScriptedLLM:
    """Answers translator and gatekeeper prompts from a table keyed by order text."""

    model = "fake-gatekeeper"

    def __init__(self, translations: dict[str, dict], reports: list[str] | None = None):
        self.translations = translations
        self.reports = list(reports or [])
        self.calls: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> dict:
        self.calls.append((system, user))
        if system.startswith("You translate"):
            order = json.loads(user.split("Order: ", 1)[1].split("\n", 1)[0])
            answer = self.translations[order["test"]]
            if "refused by the catalogue" in user and "_retry" in answer:
                answer = answer["_retry"]
            answer = {k: v for k, v in answer.items() if k != "_retry"}
        else:
            answer = {"result": self.reports.pop(0)}
        return {"content": json.dumps(answer), "finish_reason": "stop"}


class ScriptedModel:
    adapter_id = "fake"
    model_id = "fake/model"

    def __init__(self, turns):
        self.turns = iter(turns)
        self.calls = []

    def next_action(self, **kwargs):
        self.calls.append(kwargs)
        return next(self.turns)


def order(test: str, details: str = "") -> ModelTurn:
    arguments = {"test": test, **({"details": details} if details else {})}
    return ModelTurn(action=ToolAction(tool_name=REQUEST_TEST_NAME, arguments=arguments))


def assessment() -> ModelTurn:
    return ModelTurn(
        action=SubmitAssessment(primary_diagnosis="status epilepticus", confidence=0.9, urgency="emergent")
    )


def run(tmp_path, llm, turns, *, case=None, max_turns=6):
    case = case or load_case()
    loop = FreeOrderLoop(FreeOrderGatekeeper(llm, cache_dir=tmp_path / "cache"))
    model = ScriptedModel(turns)
    context = RunContext(
        profile_id="free-order-test",
        model=model,
        loop=loop,
        environment=NeuroBenchEnvironment(case),
        max_turns=max_turns,
    )
    return loop.run(context), model, case


def test_mapped_order_is_served_by_the_catalogue_and_scored_as_the_typed_call(tmp_path):
    case = load_case()
    _, alternative = required_alternative(case)
    mapped = {"kind": "mapped", "tool_name": alternative.tool_name, "arguments": call_arguments(alternative)}
    llm = ScriptedLLM({"the study": mapped})
    episode, model, _ = run(tmp_path, llm, [order("The study"), assessment()], case=case)

    assert isinstance(episode.events[-1], RunCompleted)
    observation = next(e for e in episode.events if isinstance(e, ObservationReceived))
    assert observation.tool_name == REQUEST_TEST_NAME  # the agent never sees catalogue names
    assert observation.success and not observation.rejected
    reference = NeuroBenchEnvironment(case).execute(ToolAction(tool_name=alternative.tool_name, arguments=call_arguments(alternative)))
    assert observation.output == reference.output
    assert observation.cost_usd == reference.cost_usd

    event = next(e for e in episode.events if isinstance(e, PluginEvent) and e.namespace == TRANSLATION_NAMESPACE)
    assert event.payload["kind"] == "mapped" and event.payload["tool_name"] == alternative.tool_name
    typed = typed_episode(episode)
    assert typed.tool_actions[0].tool_name == alternative.tool_name
    reward = ClinicalPolicyReward(require_approved=False)
    assert reward.score(episode, case) == reward.score(typed, case)
    assert reward.score(episode, case).tool_accuracy == 1.0
    assert [tool["function"]["name"] for tool in model.calls[0]["allowed_tools"]] == [REQUEST_TEST_NAME]
    assert model.calls[0]["free_order"] is True


def test_off_catalogue_order_gets_a_generated_report_at_the_fixed_price(tmp_path):
    llm = ScriptedLLM({"spine x-ray": {"kind": "off_catalogue"}}, reports=["Alignment preserved. No fracture."])
    episode, _, case = run(tmp_path, llm, [order("Spine X-ray"), assessment()])
    observation = next(e for e in episode.events if isinstance(e, ObservationReceived))
    assert observation.output == {"test": "Spine X-ray", "result": "Alignment preserved. No fracture."}
    assert observation.cost_usd == 150.0
    assert typed_episode(episode).tool_actions[0].tool_name == OFF_CATALOGUE_TOOL
    assert ClinicalPolicyReward(require_approved=False).score(episode, case).tool_accuracy == 0.0
    gatekeeper_prompt = llm.calls[-1][1]
    assert case.ground_truth.diagnosis.accepted[0] in gatekeeper_prompt  # the gatekeeper knows the case


def test_vague_and_non_test_orders_are_never_placed(tmp_path):
    llm = ScriptedLLM(
        {
            "blood tests": {"kind": "vague", "message": "Which blood tests?"},
            "neurology consult": {"kind": "not_a_test", "message": "Only tests can be ordered."},
        }
    )
    episode, _, _ = run(tmp_path, llm, [order("Blood tests"), order("Neurology consult"), assessment()])
    observations = [e for e in episode.events if isinstance(e, ObservationReceived)]
    assert [o.error_message for o in observations] == ["Which blood tests?", "Only tests can be ordered."]
    assert all(o.rejected and o.cost_usd == 0.0 and not o.success for o in observations)
    assert {a.tool_name for a in typed_episode(episode).tool_actions} == {UNPLACED_TOOL}


def test_translations_are_cached_across_cases_and_runs(tmp_path):
    case = load_case()
    _, alternative = required_alternative(case)
    mapped = {"kind": "mapped", "tool_name": alternative.tool_name, "arguments": call_arguments(alternative)}
    llm = ScriptedLLM({"the study": mapped})
    run(tmp_path, llm, [order("The study"), order("  the STUDY. "), assessment()], case=case)
    assert len(llm.calls) == 1  # normalized text, one gateway call
    episode, _, _ = run(tmp_path, llm, [order("The study"), assessment()], case=case)
    assert len(llm.calls) == 1
    event = next(e for e in episode.events if isinstance(e, PluginEvent))
    assert event.payload["cached"] is True


def test_report_naming_the_diagnosis_is_retried_then_replaced(tmp_path):
    case = load_case()
    label = case.ground_truth.diagnosis.accepted[0]
    llm = ScriptedLLM({"spine x-ray": {"kind": "off_catalogue"}}, reports=[f"Consistent with {label}.", f"Typical of {label}."])
    episode, _, _ = run(tmp_path, llm, [order("Spine X-ray"), assessment()], case=case)
    observation = next(e for e in episode.events if isinstance(e, ObservationReceived))
    assert label.lower() not in json.dumps(observation.output).lower()
    assert observation.output["result"] == "Study performed. No abnormality reported."


def test_a_translation_the_schema_refuses_is_retried_with_the_error(tmp_path):
    case = load_case()
    _, alternative = required_alternative(case)
    good = {"kind": "mapped", "tool_name": alternative.tool_name, "arguments": call_arguments(alternative)}
    bad = {"kind": "mapped", "tool_name": "order_body_imaging", "arguments": {"clinical_context": "x", "study": "not_a_study"}}
    llm = ScriptedLLM({"the study": {**bad, "_retry": good}})
    episode, _, _ = run(tmp_path, llm, [order("The study"), assessment()], case=case)
    assert len(llm.calls) == 2 and "refused by the catalogue" in llm.calls[1][1]
    assert typed_episode(episode).tool_actions[0].tool_name == alternative.tool_name


def test_free_order_request_has_its_own_prompt_and_one_tool():
    class Client:
        model = "fake/model"

        def chat(self, messages, *, tools, tool_choice):
            self.messages, self.tools = messages, tools
            return LLMResponse(
                content="", tool_calls=[LLMToolCall(id="c1", name=REQUEST_TEST_NAME, arguments={"test": "EEG"})]
            )

    from neuroagent.harness.free_order import REQUEST_TEST_TOOL
    from neuroagent.harness.store import MemoryEpisodeStore

    client = Client()
    turn = NativeToolModelAdapter(client).next_action(
        case=load_case(), episode=MemoryEpisodeStore().load(), allowed_tools=[REQUEST_TEST_TOOL], free_order=True
    )
    assert turn.action.tool_name == REQUEST_TEST_NAME
    assert [tool["function"]["name"] for tool in client.tools] == [REQUEST_TEST_NAME, SUBMIT_NAME]
    assert client.messages[0]["content"] == FREE_ORDER_SYSTEM_PROMPT


def test_free_order_transcript_never_names_a_catalogue_tool(tmp_path):
    case = load_case()
    _, alternative = required_alternative(case)
    mapped = {"kind": "mapped", "tool_name": alternative.tool_name, "arguments": call_arguments(alternative)}
    episode, _, _ = run(tmp_path, ScriptedLLM({"the study": mapped}), [order("The study"), assessment()], case=case)
    rendered = json.dumps(transcript(case, episode, free_order=True))
    assert alternative.tool_name not in rendered
    assert REQUEST_TEST_NAME in rendered
