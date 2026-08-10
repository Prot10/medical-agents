"""The clinical reviewers' per-condition guidance: valid, complete, and never seen by the agent.

`config/review/condition_tool_guidance.yaml` carries the July 2026 review's condition-specific
tool descriptions — the half of the review that had nowhere to live, because
`ToolMeta.description` is one string per tool shown under all twenty conditions. Three
properties have to hold, and only the third is obvious:

1. every entry names a real condition and a real tool, or the app renders guidance against a
   row that does not exist;
2. every entry answers the comment it comes from — an entry without `our_response` is a comment
   read and not replied to, which is the state this file was built to end;
3. **nothing on the agent's side reads it.** The text says things like "mandatory if the head CT
   is negative" and "not indicated in syncope". In the agent-facing schema that is the diagnosis
   handed to the model. The guard is a grep over the packages that build the agent, because an
   import is how the leak would arrive.
"""

from __future__ import annotations

import pathlib

import pytest
import yaml

from neuroagent.review_api.config import CONDITION_TOOL_GUIDANCE_PATH
from neuroagent.review_api.schemas.tool_review import ConditionToolGuidance
from neuroagent.review_api.services.tool_catalog import _TOOL_META
from neuroagent_schemas.enums import NeurologicalCondition

SRC = pathlib.Path(__file__).resolve().parents[1] / "src" / "neuroagent"
# The condition the review asked us to replace. Its annotation is kept so the answer is not
# lost with the row, and it is the only key that may name a condition the enum no longer has.
RETIRED_CONDITIONS = {"peripheral_neuropathy"}
# 91 annotations across the two reviewers, split into 110 entries because eleven of them
# describe a study that belongs to a tool the reviewer could not see. This number is the
# review's own size: if it changes without a new round of review, something was invented.
EXPECTED_ENTRIES = 110


@pytest.fixture(scope="module")
def guidance() -> dict[str, dict[str, dict]]:
    assert CONDITION_TOOL_GUIDANCE_PATH.exists(), CONDITION_TOOL_GUIDANCE_PATH
    return yaml.safe_load(CONDITION_TOOL_GUIDANCE_PATH.read_text()) or {}


def test_every_entry_validates(guidance):
    for condition, tools in guidance.items():
        for tool, entry in tools.items():
            ConditionToolGuidance.model_validate(entry), (condition, tool)


def test_every_condition_exists(guidance):
    known = {c.value for c in NeurologicalCondition} | RETIRED_CONDITIONS
    unknown = sorted(set(guidance) - known)
    assert not unknown, f"guidance for conditions that do not exist: {unknown}"


def test_every_tool_exists(guidance):
    known = {m["name"] for m in _TOOL_META}
    for condition, tools in guidance.items():
        unknown = sorted(set(tools) - known)
        assert not unknown, f"{condition}: guidance for tools that do not exist: {unknown}"
        for tool, entry in tools.items():
            filed = entry.get("filed_under") or []
            assert not set(filed) - known, f"{condition}/{tool}: filed_under names no tool"
            assert tool not in filed, f"{condition}/{tool}: filed_under repeats the tool itself"


def test_the_whole_review_is_accounted_for(guidance):
    """One entry per annotation segment, and every one of them answered."""
    entries = [(c, t, e) for c, tools in guidance.items() for t, e in tools.items()]
    assert len(entries) == EXPECTED_ENTRIES, (
        f"{len(entries)} entries, expected {EXPECTED_ENTRIES} — regenerate with "
        "scripts/review/build_condition_tool_guidance.py, and if the count really changed, "
        "say why in the commit message"
    )
    for condition, tool, entry in entries:
        assert entry.get("our_response", "").strip(), (
            f"{condition}/{tool}: a reviewer comment with no answer"
        )
        if entry["status"] not in {"no_change", "open", "retired"}:
            assert entry.get("guidance", "").strip(), (
                f"{condition}/{tool}: status {entry['status']} but no guidance text"
            )


def test_no_guidance_text_survives_as_a_stale_description(guidance):
    """The strings the reviewers quoted as "to be removed" must not be served back to them."""
    quoted_for_removal = (
        "EMG/NCS, repetitive nerve stimulation, biopsies, neuropsych battery",
        "protocol selection (standard, epilepsy",
        "CBC, metabolic, coagulation, thyroid, inflammatory, autoimmune/paraneoplastic, genetic",
        "Holter, extended event monitoring, or inpatient telemetry",
        "oligoclonal bands, PCR, antibodies, 14-3-3/RT-QuIC",
    )
    for tool in _TOOL_META:
        for stale in quoted_for_removal:
            assert stale not in tool["description"], (
                f"{tool['name']}: the catalog still serves the description the review asked to "
                f"remove ({stale!r})"
            )
    for condition, tools in guidance.items():
        for tool, entry in tools.items():
            for stale in quoted_for_removal:
                assert stale not in (entry.get("guidance") or ""), (
                    f"{condition}/{tool}: the revised description opens with the old one"
                )


def test_the_agent_never_reads_the_guidance():
    """A condition-specific indication in the agent's prompt is the diagnosis, handed over."""
    agent_side = [
        SRC / "tools",
        SRC / "agents",
        SRC / "api",
        SRC / "evaluation",
        SRC / "llm",
    ]
    needles = ("condition_tool_guidance", "CONDITION_TOOL_GUIDANCE_PATH")
    offenders: list[str] = []
    for root in agent_side:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            text = path.read_text()
            if any(n in text for n in needles):
                offenders.append(str(path.relative_to(SRC)))
    assert not offenders, (
        "the per-condition guidance is review-app only; these agent-side modules reference it: "
        f"{offenders}"
    )


def test_no_reviewer_code_leaks_into_a_committed_file(guidance):
    """Reviewer codes are bearer credentials. The file records 1 and 2, never a code."""
    raw = CONDITION_TOOL_GUIDANCE_PATH.read_text()
    assert "NB-" not in raw, "a reviewer code reached a committed file"
    for condition, tools in guidance.items():
        for tool, entry in tools.items():
            assert entry["reviewer"] in (1, 2), f"{condition}/{tool}: bad reviewer label"
