"""Multi-agent panel baseline, in the style of MAI-DxO (Nori et al., Science 2026), rebuilt on our harness.

The same model plays five physicians who discuss each step in turn; then the model, as chair,
turns the discussion into exactly one typed action through the canonical adapter. The roles follow
the published description of the MAI-DxO panel; the prompts are ours, and the agent is called a
"multi-agent panel in the style of MAI-DxO", never MAI-DxO.

Each role sees the case, the test menu and the work-up so far as plain text (no tool catalogue, so
a role cannot place an order), plus what the earlier roles said in this turn. The chair's request
is the canonical policy transcript with the discussion delivered as one-off feedback, like a
correction: it is not replayed on later turns and never enters an SFT transcript. The discussion is
kept as the namespaced plugin event ``panel.discussion``; its tokens count towards the turn.
"""

from __future__ import annotations

import json
from typing import Any

from neuroagent_schemas import ActionProposed, ClinicalEpisode, NeuroBenchCase, ObservationReceived

from .context import format_patient_info

PANEL_NAMESPACE = "panel.discussion"
ROLE_MAX_TOKENS = 400

PANEL_ROLES: tuple[tuple[str, str], ...] = (
    (
        "hypothesis",
        "You are Dr. Hypothesis. Keep a ranked differential of the three most likely diagnoses with "
        "a rough probability for each, and update it with every new finding.",
    ),
    (
        "test_chooser",
        "You are Dr. Test-Chooser. Propose at most three tests from the menu that would best "
        "separate the leading diagnoses, or say that no further test is needed.",
    ),
    (
        "challenger",
        "You are Dr. Challenger. Look for anchoring on the leading diagnosis, point out findings "
        "that do not fit it, and name the test that could prove it wrong.",
    ),
    (
        "stewardship",
        "You are Dr. Stewardship. Argue for the cheaper of two tests that answer the same question "
        "and against low-yield or redundant tests.",
    ),
    (
        "checklist",
        "You are Dr. Checklist. Check that the proposed tests exist in the menu, that nothing "
        "required for safety was skipped, and that the panel's reasoning is consistent. End with "
        "the panel's recommendation: one test to order now, or submit the assessment.",
    ),
)

ROLE_SYSTEM = """You sit on a panel of five physicians that decides, one step at a time, the work-up
of a patient in a simulated hospital. {role} Answer in plain text, at most 120 words. Do not
place orders yourself: the chair takes the decision after the panel has spoken. This is research
on clinician support, not autonomous care."""

CHAIR_INSTRUCTION = """The panel has discussed this step:
{discussion}

As chair, take the panel's decision now: make exactly one function call, either one test from the
menu or submit_assessment."""


def _menu(tools: list[dict[str, Any]]) -> str:
    lines = []
    for tool in tools:
        function = tool["function"]
        description = (function.get("description") or "").strip().split("\n")[0]
        lines.append(f"- {function['name']}: {description}" if description else f"- {function['name']}")
    return "\n".join(lines)


def _work_up(episode: ClinicalEpisode) -> str:
    lines, step = [], 0
    for event in episode.events:
        if isinstance(event, ActionProposed) and event.action.type == "tool":
            step += 1
            lines.append(f"{step}. Ordered {event.action.tool_name} {json.dumps(event.action.arguments, sort_keys=True)}")
        elif isinstance(event, ObservationReceived) and event.turn > 0:
            result = event.output if event.success else {"error": event.error_message}
            lines.append(f"   Result: {json.dumps(result, sort_keys=True)}")
    return "\n".join(lines) if lines else "No test ordered yet."


def role_messages(
    case: NeuroBenchCase,
    episode: ClinicalEpisode,
    tools: list[dict[str, Any]],
    role_prompt: str,
    said: list[tuple[str, str]],
    *,
    final_turn: bool,
) -> list[dict[str, Any]]:
    """The request of one role: case, menu, work-up so far and this turn's discussion, as text."""
    parts = [
        format_patient_info(case),
        "Test menu:\n" + _menu(tools),
        "Work-up so far:\n" + _work_up(episode),
    ]
    if final_turn:
        parts.append("This is the last step: the panel must now submit the assessment, no more tests.")
    if said:
        parts.append("Discussion so far in this step:\n" + "\n".join(f"[{name}] {text}" for name, text in said))
    parts.append("Your contribution:")
    return [
        {"role": "system", "content": ROLE_SYSTEM.format(role=role_prompt)},
        {"role": "user", "content": "\n\n".join(parts)},
    ]


def chair_instruction(said: list[tuple[str, str]]) -> str:
    return CHAIR_INSTRUCTION.format(discussion="\n".join(f"[{name}] {text}" for name, text in said))
