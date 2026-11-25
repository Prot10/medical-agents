"""Agent-mode use cases: the work list, one step of a case, and the admin summary."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any

from neuroagent_schemas import (
    ActionProposed,
    ActionRejected,
    AssessmentSubmitted,
    NeuroBenchCase,
    ObservationReceived,
    SubmitAssessment,
    ToolAction,
)

from neuroagent.datasets import REPO_ROOT
from neuroagent.evaluation.benchmark import episode_row
from neuroagent.evaluation.manifest import ENVIRONMENT_FILES, case_hashes
from neuroagent.evaluation.policy_reward import ClinicalPolicyReward
from neuroagent.harness.context import SUBMIT_NAME, observation_payload
from neuroagent.harness.loops import ClinicalPolicyLoop
from neuroagent_schemas.evaluation import PolicyReviewStatus

from ...schemas.agent_mode import ActionRequest, AgentRecord, PhysicianStep
from ...schemas.reviewers import ReviewerCode
from .engine import PHYSICIAN_PROFILE_ID, Advance, Submission, advance, merge_events, plugin_versions
from .sets import AgentModeConfig, AgentSectionConfig
from .store import AgentRecordStore, utcnow

APP_VERSION = "0.2.0"
RECORD_VERSION = 1
DEPLOYED_COMMIT_FILE = REPO_ROOT / "agent-platform" / "config" / "review" / "deployed_commit.txt"


class AgentModeError(Exception):
    """A request the study's rules refuse; ``status`` is the HTTP status to answer with."""

    def __init__(self, status: int, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.detail = detail


def _sha256(value: Any) -> str:
    data = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()


@lru_cache(maxsize=1)
def app_commit() -> dict[str, Any]:
    """The commit this app runs from. A deployed copy has no git tree: the deploy script writes
    the commit next to the review config, and ``REVIEW_APP_COMMIT`` overrides both."""
    if os.environ.get("REVIEW_APP_COMMIT"):
        return {"commit": os.environ["REVIEW_APP_COMMIT"], "dirty": None, "source": "env"}

    def git(*args: str) -> str | None:
        try:
            return subprocess.run(
                ["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True, check=True, timeout=10
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None

    commit = git("rev-parse", "HEAD")
    if commit:
        status = git("status", "--porcelain", "--untracked-files=no")
        return {"commit": commit, "dirty": None if status is None else bool(status), "source": "git"}
    if DEPLOYED_COMMIT_FILE.exists():
        return {"commit": DEPLOYED_COMMIT_FILE.read_text().strip(), "dirty": None, "source": "deploy"}
    return {"commit": None, "dirty": None, "source": "unknown"}


@lru_cache(maxsize=1)
def _environment_hashes() -> dict[str, str]:
    return {path: _sha256((REPO_ROOT / path).read_bytes()) for path in ENVIRONMENT_FILES}


def model_id(reviewer: ReviewerCode) -> str:
    return f"physician:{reviewer.public_id}"


def provenance(config: AgentModeConfig, section: AgentSectionConfig, case: NeuroBenchCase, request: dict) -> dict:
    """Enough to reproduce exactly what the physician was shown."""
    messages = request["messages"]
    return {
        "app": {"name": "neurobench-review", "version": APP_VERSION, "git": app_commit()},
        "set": {"section": section.key, "id": section.set_id, "sha256": section.set_sha256, "cases": len(section.case_ids)},
        "case": {"file_sha256": section.case_sha256[case.case_id], **case_hashes(case)},
        "profile": {
            "profile_id": PHYSICIAN_PROFILE_ID,
            "limits_from": config.limits_from,
            "loop_id": ClinicalPolicyLoop.loop_id,
            "max_turns": config.profile.max_turns,
            "max_cost_usd": config.profile.max_cost_usd,
            "max_invalid_actions": config.profile.max_invalid_actions,
            "plugin_versions": plugin_versions(),
        },
        "agent_facing": {
            "system_prompt_sha256": _sha256(messages[0]["content"].encode()),
            "presentation_sha256": _sha256(messages[1]["content"].encode()),
            "catalogue_sha256": _sha256(request["tools"]),
            "tools": len(request["tools"]),
            "show_step_budget": config.show_step_budget,
        },
        "environment_sha256": _environment_hashes(),
    }


# ── Work list ───────────────────────────────────────────────────────────────────────────────


def reviewed_case_ids(annotations_root: Path | None, codes: list[str]) -> set[str]:
    """Cases any of ``codes`` opened in the dataset review (any version or review set): that
    person has seen their policy and diagnosis."""
    if annotations_root is None or not codes or not annotations_root.is_dir():
        return set()
    return {
        path.stem
        for version_dir in annotations_root.iterdir()
        if version_dir.is_dir()
        for code in codes
        for path in (version_dir / code).glob("*.json")
    }


def assigned_numbers(section: AgentSectionConfig, reviewer: ReviewerCode, annotations_root: Path | None) -> list[int]:
    """The reviewer's cases, by number, in the set's order."""
    skipped = set() if section.record_derived else reviewed_case_ids(annotations_root, reviewer.linked_review_codes)
    return [number for number, case_id in enumerate(section.case_ids, start=1) if case_id not in skipped]


def worklist(
    section: AgentSectionConfig, reviewer: ReviewerCode, store: AgentRecordStore, annotations_root: Path | None
) -> dict[str, Any]:
    records = store.records_of(section, reviewer.public_id)
    cases = []
    for number in assigned_numbers(section, reviewer, annotations_root):
        record = records.get(section.case_ids[number - 1])
        cases.append(
            {
                "number": number,
                "status": "todo" if record is None else "in_progress" if record.status == "in_progress" else "done",
                "orders": sum(step.outcome == "observed" for step in record.steps) if record else 0,
                "finished_at": record.finished_at if record else None,
            }
        )
    in_progress = [item["number"] for item in cases if item["status"] == "in_progress"]
    todo = [item["number"] for item in cases if item["status"] == "todo"]
    return {
        "section": section.key,
        "title": section.title,
        "description": section.description,
        "cases": cases,
        "total": len(cases),
        "done": sum(item["status"] == "done" for item in cases),
        # One case at a time, in the set's order: the open case, else the first not started.
        "current": in_progress[0] if in_progress else todo[0] if todo else None,
    }


# ── One case ────────────────────────────────────────────────────────────────────────────────


def _submissions(record: AgentRecord) -> list[Submission]:
    return [Submission(step.name, step.arguments, step.latency_seconds) for step in record.steps]


def _case(section: AgentSectionConfig, number: int) -> NeuroBenchCase:
    case = section.case_at(number)
    if case is None:
        raise AgentModeError(404, "No such case")
    return case


def _timeline(record: AgentRecord) -> list[dict[str, Any]]:
    """Orders placed so far, each with its rationale and the observation as the agent reads it."""
    rationale = {step.turn: step.rationale for step in record.steps if step.outcome in ("observed", "schema_rejected")}
    entries: dict[int, dict[str, Any]] = {}
    for event in record.episode.events:
        if isinstance(event, ActionProposed) and isinstance(event.action, ToolAction):
            entries[event.turn] = {
                "turn": event.turn,
                "tool_name": event.action.tool_name,
                "arguments": event.action.arguments,
                "rationale": rationale.get(event.turn, ""),
                "sent_at": event.timestamp,
            }
        elif isinstance(event, ObservationReceived) and event.turn in entries:
            payload = observation_payload(event)
            # The exact content of the `tool` message the agent receives for this order.
            entries[event.turn].update(observation=payload, observation_text=json.dumps(payload, sort_keys=True))
    return [entries[turn] for turn in sorted(entries)]


def state_view(
    config: AgentModeConfig, section: AgentSectionConfig, record: AgentRecord, step: Advance, *, next_number: int | None
) -> dict[str, Any]:
    """What the client renders. A finished case shows nothing more than that it is finished:
    the study is blind and the case is locked."""
    view: dict[str, Any] = {
        "section": section.key,
        "number": record.case_number,
        "status": record.status,
        "expected_step": len(record.steps),
        "next": next_number,
    }
    if record.status != "in_progress":
        view["failure"] = record.failure
        return view
    assert step.request is not None
    messages, tools = step.request["messages"], step.request["tools"]
    timeline = _timeline(record)
    view.update(
        turn=len(timeline) + 1,
        orders=len(timeline),
        max_turns=config.profile.max_turns if config.show_step_budget else None,
        require_assessment=step.require_assessment,
        # Extra text the agent receives on this turn (a correction, the final-turn instruction).
        notice=step.notice,
        invalid_actions=step.invalid_actions,
        instructions=messages[0]["content"],
        presentation=messages[1]["content"],
        tools=tools,
        submit_name=SUBMIT_NAME,
        timeline=timeline,
        # The request the model server would receive now, verbatim.
        raw={"messages": messages, "tools": tools},
    )
    return view


def _load_step(
    config: AgentModeConfig, section: AgentSectionConfig, reviewer: ReviewerCode, record: AgentRecord
) -> Advance:
    case = section.cases[record.case_id]
    return advance(case, config.profile, model_id(reviewer), _submissions(record), record.episode)


def start_case(
    config: AgentModeConfig,
    section: AgentSectionConfig,
    reviewer: ReviewerCode,
    number: int,
    store: AgentRecordStore,
    annotations_root: Path | None,
) -> dict[str, Any]:
    """Open a case (idempotent). Only the reviewer's current case can be opened."""
    case = _case(section, number)
    with store.lock(section, reviewer.public_id):
        work = worklist(section, reviewer, store, annotations_root)
        record = store.load(section, reviewer.public_id, case.case_id)
        if record is None:
            if number != work["current"]:
                raise AgentModeError(409, "Cases are worked one at a time, in order")
            first = advance(case, config.profile, model_id(reviewer), [])
            now = utcnow()
            record = AgentRecord(
                section=section.key,
                set_id=section.set_id,
                case_id=case.case_id,
                case_number=number,
                reviewer_id=reviewer.public_id,
                reviewer_name=reviewer.name,
                started_at=now,
                updated_at=now,
                provenance=provenance(config, section, case, first.request),
                episode=merge_events(None, first.episode),
            )
            store.save(section, record)
            store.log(section, reviewer.public_id, case.case_id, "case.started", provenance=record.provenance)
        return get_state(config, section, reviewer, number, store, annotations_root)


def get_state(
    config: AgentModeConfig,
    section: AgentSectionConfig,
    reviewer: ReviewerCode,
    number: int,
    store: AgentRecordStore,
    annotations_root: Path | None,
) -> dict[str, Any]:
    case = _case(section, number)
    record = store.load(section, reviewer.public_id, case.case_id)
    if record is None:
        raise AgentModeError(404, "Case not started")
    store.log(section, reviewer.public_id, case.case_id, "state.viewed", status=record.status, steps=len(record.steps))
    step = _load_step(config, section, reviewer, record) if record.status == "in_progress" else None
    next_number = worklist(section, reviewer, store, annotations_root)["current"]
    return state_view(config, section, record, step, next_number=next_number)


def _outcome(new_events: list[Any]) -> tuple[str, int]:
    for event in new_events:
        if isinstance(event, ActionRejected):
            return "action_rejected", event.turn
        if isinstance(event, AssessmentSubmitted):
            return "assessment", event.turn
        if isinstance(event, ObservationReceived):
            return ("schema_rejected" if event.rejected else "observed"), event.turn
    raise AssertionError("an action always ends in a rejection, an observation or the assessment")


def act(
    config: AgentModeConfig,
    section: AgentSectionConfig,
    reviewer: ReviewerCode,
    number: int,
    body: ActionRequest,
    store: AgentRecordStore,
    annotations_root: Path | None,
) -> dict[str, Any]:
    """Send one action. It goes to the harness as the agent's would; nothing is validated here
    except what only a physician has (the rationale) and that the page is not stale."""
    case = _case(section, number)
    with store.lock(section, reviewer.public_id):
        record = store.load(section, reviewer.public_id, case.case_id)
        if record is None:
            raise AgentModeError(404, "Case not started")
        if record.status != "in_progress":
            raise AgentModeError(409, "This case is finished and locked")
        if body.expected_step != len(record.steps):
            raise AgentModeError(409, "This page is out of date: reload to see the current step")
        now = utcnow()
        server_seconds = max(0.0, (now - record.updated_at).total_seconds())
        active = body.telemetry.active_seconds
        latency = server_seconds if active is None else min(server_seconds, active)
        store.log(
            section, reviewer.public_id, case.case_id, "action.received",
            step=len(record.steps), body=body.model_dump(mode="json"), server_seconds=server_seconds,
        )
        submissions = [*_submissions(record), Submission(body.name, body.arguments, latency)]
        step = advance(case, config.profile, model_id(reviewer), submissions, record.episode)
        episode = merge_events(record.episode, step.episode)
        outcome, turn = _outcome(episode.events[len(record.episode.events):])
        record.steps.append(
            PhysicianStep(
                index=len(record.steps),
                turn=turn,
                name=body.name,
                arguments=body.arguments,
                outcome=outcome,
                rationale=body.rationale,
                shown_at=record.updated_at,
                sent_at=now,
                server_seconds=server_seconds,
                latency_seconds=latency,
                client=body.telemetry,
            )
        )
        record.episode = episode
        record.status = step.status
        record.updated_at = utcnow()
        if step.status != "in_progress":
            record.finished_at = record.updated_at
        if step.status == "completed":
            record.diagnostic_reasoning = body.rationale
        if step.status == "failed":
            record.failure = {"reason": step.failure_reason or "", "message": step.failure_message or ""}
        store.save(section, record)
        store.log(
            section, reviewer.public_id, case.case_id, "action.outcome",
            step=len(record.steps) - 1, outcome=outcome, turn=turn, status=record.status,
        )
        next_number = worklist(section, reviewer, store, annotations_root)["current"]
        return state_view(config, section, record, step, next_number=next_number)


# ── Admin ───────────────────────────────────────────────────────────────────────────────────


def _reward_row(case: NeuroBenchCase, record: AgentRecord) -> dict[str, Any]:
    """The row the benchmark writes for a model episode, scored by the same scorer. A draft policy
    is scored with the engineering flag and marked as not reportable."""
    approved = case.ground_truth.review_status is PolicyReviewStatus.APPROVED
    row = episode_row(case, record.episode, ClinicalPolicyReward(require_approved=approved))
    row["policy_review"] = case.ground_truth.review_status.value
    row["reportable"] = approved
    row["scorer_id"] = ClinicalPolicyReward.scorer_id
    return row


def episode_summary(section: AgentSectionConfig, record: AgentRecord) -> dict[str, Any]:
    case = section.cases[record.case_id]
    finished = record.status != "in_progress"
    active = [step.client.active_seconds for step in record.steps]
    return {
        "section": section.key,
        "reviewer_id": record.reviewer_id,
        "reviewer_name": record.reviewer_name,
        "case_number": record.case_number,
        "case_id": record.case_id,
        "condition": case.condition.value,
        "status": record.status,
        "orders": sum(step.outcome == "observed" for step in record.steps),
        "invalid_attempts": record.invalid_attempts,
        "started_at": record.started_at,
        "finished_at": record.finished_at,
        "elapsed_seconds": sum(step.server_seconds for step in record.steps),
        "active_seconds": sum(value for value in active if value is not None) if any(v is not None for v in active) else None,
        "row": _reward_row(case, record) if finished else None,
    }


def admin_overview(
    config: AgentModeConfig, store: AgentRecordStore, reviewers: list[ReviewerCode], annotations_root: Path | None
) -> dict[str, Any]:
    sections = []
    for section in config.sections.values():
        codes = {code.public_id: code for code in reviewers if section.access in code.sections}
        people, episodes = [], []
        for reviewer_id in sorted(set(codes) | set(store.reviewer_ids(section))):
            records = store.records_of(section, reviewer_id)
            code = codes.get(reviewer_id)
            name = code.name if code else next((r.reviewer_name for r in records.values()), reviewer_id)
            people.append(
                {
                    "reviewer_id": reviewer_id,
                    "name": name,
                    "active": bool(code and code.active),
                    "assigned": len(assigned_numbers(section, code, annotations_root)) if code else len(records),
                    "done": sum(r.status == "completed" for r in records.values()),
                    "failed": sum(r.status == "failed" for r in records.values()),
                    "in_progress": sum(r.status == "in_progress" for r in records.values()),
                }
            )
            episodes.extend(episode_summary(section, record) for record in records.values())
        episodes.sort(key=lambda item: (item["case_number"], item["reviewer_id"]))
        sections.append(
            {
                "key": section.key,
                "title": section.title,
                "set_id": section.set_id,
                "cases": len(section.case_ids),
                "record_derived": section.record_derived,
                "reviewers": people,
                "episodes": episodes,
            }
        )
    return {
        "scorer_id": ClinicalPolicyReward.scorer_id,
        "limits": {"from": config.limits_from, "max_turns": config.profile.max_turns},
        "sections": sections,
    }


def admin_record(section: AgentSectionConfig, store: AgentRecordStore, reviewer_id: str, number: int) -> dict[str, Any]:
    case = _case(section, number)
    record = store.load(section, reviewer_id, case.case_id)
    if record is None:
        raise AgentModeError(404, "No record")
    assessment = record.episode.assessment
    return {
        **episode_summary(section, record),
        "timeline": _timeline(record),
        "steps": [step.model_dump(mode="json") for step in record.steps],
        "assessment": assessment.model_dump(mode="json", exclude={"type"}) if isinstance(assessment, SubmitAssessment) else None,
        "diagnostic_reasoning": record.diagnostic_reasoning,
        "failure": record.failure,
        "provenance": record.provenance,
    }
