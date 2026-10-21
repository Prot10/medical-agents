"""A prohibited recommendation phrased as a tool call must name a real call the case does not require.

Six stroke cases once required a CTA and, in a later bullet, forbade `order_ct_scan` with
contrast and angiography; six more forbade `check_drug_interactions` with `proposed=alteplase`,
a parameter the tool does not have. Clinical reviewers found both, the fixes of 2026-09-16 removed
them, and a merge brought them back. These two rules keep them out of every case.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import pytest

from neuroagent.review_api.services.tool_io import parameters_for

CASES = sorted((Path(__file__).resolve().parents[2] / "data" / "neurobench" / "cases").glob("*.json"))
# The two shapes the dataset has used for a tool-call prohibition.
TOOL_BULLET = re.compile(r"^Avoid (\w+) with ([^:]+):")
CALL_BULLET = re.compile(r"^Do not call `(\w+)` with parameters (\{[^}]*\})")


def _arguments(text: str) -> dict[str, object]:
    arguments = {}
    for pair in text.split(", "):
        key, _, value = pair.partition("=")
        try:
            arguments[key.strip()] = ast.literal_eval(value.strip())
        except (ValueError, SyntaxError):
            arguments[key.strip()] = value.strip()
    return arguments


def _tool_bullets(case: dict) -> list[tuple[str, str, dict[str, object]]]:
    bullets = []
    for text in case["ground_truth"]["assessment"]["prohibited_recommendations"]:
        if match := TOOL_BULLET.match(text):
            bullets.append((text, match.group(1), _arguments(match.group(2))))
        elif match := CALL_BULLET.match(text):
            bullets.append((text, match.group(1), ast.literal_eval(match.group(2))))
    return bullets


def _agrees(forbidden: dict[str, object], required: dict[str, object]) -> bool:
    shared = forbidden.keys() & required.keys()
    nested = forbidden.keys() <= required.keys() or required.keys() <= forbidden.keys()
    return nested and all(forbidden[key] == required[key] for key in shared)


@pytest.mark.parametrize("path", CASES, ids=lambda p: p.stem)
def test_tool_prohibition_names_real_parameters(path: Path):
    case = json.loads(path.read_text())
    for text, tool, arguments in _tool_bullets(case):
        schema = parameters_for(tool)
        assert schema is not None, f"{text!r} names an unknown tool"
        unknown = set(arguments) - set(schema["properties"])
        assert not unknown, f"{text!r} names parameters {sorted(unknown)} that {tool} does not take"


@pytest.mark.parametrize("path", CASES, ids=lambda p: p.stem)
def test_tool_prohibition_does_not_forbid_a_required_action(path: Path):
    case = json.loads(path.read_text())
    for text, tool, arguments in _tool_bullets(case):
        for criterion in case["ground_truth"]["action_criteria"]:
            if criterion["importance"] == "optional":
                continue
            for alternative in criterion["alternatives"]:
                if alternative["tool_name"] == tool:
                    assert not _agrees(arguments, alternative["required_arguments"]), (
                        f"{text!r} forbids what {criterion['criterion_id']} requires"
                    )
