"""An echocardiogram order is answered by the stored study of the type ordered.

`EchoReport` had no `echo_type` field until the October 2026 review, so the value case authors
wrote into echo outputs was dropped on load and the MockServer's echo discriminator never fired:
a TTE order received the stored bubble study or TEE, and a TEE order the stored TTE (ISCH-STR
P02, P05, RP03, RS02). With the field, the guard routes by the report's own type.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from neuroagent.tools.mock_server import MockServer
from neuroagent_schemas import NeuroBenchCase

CASES = Path(__file__).resolve().parents[2] / "data" / "neurobench" / "cases"
ECHO_TYPES = ("TTE", "TEE", "bubble_study")


def _case(case_id: str) -> NeuroBenchCase:
    return NeuroBenchCase.model_validate(json.loads((CASES / f"{case_id}.json").read_text()))


def _stored_echoes(case: NeuroBenchCase) -> list:
    stored = [case.initial_tool_outputs.echo] if case.initial_tool_outputs.echo else []
    stored += [f.output for f in case.followup_outputs or [] if f.tool_name == "order_echocardiogram"]
    return stored


def test_echo_report_keeps_echo_type():
    case = _case("ISCH-STR-P05")
    assert {echo.echo_type for echo in _stored_echoes(case)} == {"bubble_study", "TEE"}


@pytest.mark.parametrize(
    "case_id",
    ["ISCH-STR-P05", "ISCH-STR-P02", "ISCH-STR-RP03", "ISCH-STR-RS02"],
)
@pytest.mark.parametrize("ordered", ECHO_TYPES)
def test_echo_order_is_answered_by_the_matching_stored_study(case_id, ordered):
    case = _case(case_id)
    stored = _stored_echoes(case)
    assert stored and all(echo.echo_type for echo in stored), "every stored echo names its type"
    server = MockServer(case)
    result = server.get_output("order_echocardiogram", {"clinical_context": "stroke", "echo_type": ordered})
    assert result.success
    assert result.output["echo_type"] == ordered
    matching = [echo.model_dump() for echo in stored if echo.echo_type == ordered]
    if matching:
        assert result.output in matching  # the case's own study of that type
    else:
        assert result.library  # no stored study of that type: the normal library report
