"""A study named by a boolean flag must be reachable by the call that names it.

`order_ct_scan` is the one tool whose study identity is carried by flags rather than by a vocabulary
value: `{"contrast": True, "angiography": True}` *is* the CT angiogram. The follow-up matcher
tokenised parameter values only, so that call produced the token `"true"` — which identifies nothing —
while the follow-up authored to answer it carried the trigger `request_ct_angiography`. They shared no
meaningful token, so the stored angiogram was unreachable and the non-contrast CT was served instead,
with its own `angiography_findings` null.

The blast radius was 54 required CT-angiography actions across ischaemic stroke and subarachnoid
haemorrhage — the aneurysm-characterising study in one condition and the occlusion-selection study in
the other. Both the scorer (`_SCALAR_DISCRIMINATORS` pins `contrast` and `angiography`) and the cost
model (angiography adds 184 EUR) had always treated it as a distinct study. Only the simulator did
not, so a benchmark that billed for an angiogram never served one.

The asymmetry in the second test is deliberate and load-bearing: a *false* flag must not match, or a
plain-CT order would capture the angiogram — the same defect in the opposite direction.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from neuroagent.tools.followup_matcher import _call_tokens, resolve_followup
from neuroagent.tools.mock_server import MockServer
from neuroagent_schemas import NeuroBenchCase

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES = REPO_ROOT / "data/neurobench/cases"


def test_a_true_flag_contributes_its_name_as_a_token() -> None:
    tokens = _call_tokens("order_ct_scan", {"contrast": True, "angiography": True})
    assert "angiography" in tokens, (
        "a CT angiography request must carry the token 'angiography'; without it the only tokens are "
        "'true' and the tool name, and no trigger can match"
    )


def test_a_false_flag_contributes_nothing() -> None:
    tokens = _call_tokens("order_ct_scan", {"contrast": False, "angiography": False})
    assert "angiography" not in tokens and "contrast" not in tokens, (
        "a plain-CT order asserts the study is NOT the angiogram; if a false flag matched, the bare "
        "order would capture the angiography report"
    )


@pytest.mark.skipif(not CASES.exists(), reason="cases not present")
def test_ct_angiography_and_plain_ct_serve_different_reports() -> None:
    """Across every case that requires both, the two calls must not receive one report."""
    same: list[str] = []
    for path in sorted(CASES.glob("*.json")):
        raw = json.loads(path.read_text())
        actions = [a for a in raw["ground_truth"]["optimal_actions"]
                   if a["tool_name"] == "order_ct_scan"]
        wants_angiography = any((a.get("tool_parameters") or {}).get("angiography") for a in actions)
        wants_plain = any(not (a.get("tool_parameters") or {}).get("angiography") for a in actions)
        if not (wants_angiography and wants_plain):
            continue

        case = NeuroBenchCase.model_validate(raw)
        server = MockServer(case)
        plain = server.get_output("order_ct_scan", {"contrast": False, "angiography": False})
        angio = server.get_output("order_ct_scan", {"contrast": True, "angiography": True})
        if plain.output == angio.output:
            same.append(case.case_id)

    assert not same, (
        "these cases require both a non-contrast CT and a CT angiogram but serve one report for "
        f"both, so the haemorrhage-exclusion scan and the vessel study are indistinguishable: {same}"
    )


@pytest.mark.skipif(not CASES.exists(), reason="cases not present")
def test_a_stored_ct_angiogram_is_reachable_by_the_flagged_call() -> None:
    """Where a case stores a CTA follow-up, the flagged call must resolve to it."""
    unreachable: list[str] = []
    for path in sorted(CASES.glob("*.json")):
        raw = json.loads(path.read_text())
        case = NeuroBenchCase.model_validate(raw)
        stored = [f for f in case.followup_outputs or []
                  if f.tool_name == "order_ct_scan" and "angiograph" in f.trigger_action.lower()]
        if not stored:
            continue
        resolved = resolve_followup(
            "order_ct_scan", {"contrast": True, "angiography": True}, case.followup_outputs,
            set(), has_initial_output=case.initial_tool_outputs.ct is not None,
            is_repeat_call=False,
        )
        if resolved is None or "angiograph" not in resolved.trigger_action.lower():
            unreachable.append(case.case_id)

    assert not unreachable, (
        f"a stored CT angiogram is not reachable by a call for it in: {unreachable}"
    )
