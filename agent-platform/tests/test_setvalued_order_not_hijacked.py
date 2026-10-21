"""A broad order must not be answered by a follow-up that names one item of it.

`interpret_labs`, `analyze_csf` and `obtain_tissue_diagnosis` identify their study with a *set* of
assays. The follow-up matcher scores a trigger slug against the call's parameter values, and a set
hands it many values to match, so one shared token was enough to declare a specific re-order and
override the initial output. A status-epilepticus case ordering the ten-analyte first-line panel
shared the token `aed` with `request_aed_optimization` and was answered by the post-dose-escalation
drug level alone; the case's own first-line panel then went to a later action asking for an
autoimmune panel it does not carry. The two were crossed — the CT/CTA defect on a set parameter.

Measured before the fix: 82 required and recommended set-valued orders across 93 cases were served a
payload that another stored payload answered better, and 327 of the analytes the gold standard orders
were absent from what the simulator actually served.

The rule is a *comparison*, not a threshold, and that is load-bearing: the share of an order a
trigger names does not separate the crossed calls from the sound ones — 35 legitimate matches name
one item of four, exactly the shape of the crossings. What separates them is whether another stored
payload answers more of the question.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from neuroagent.tools.mock_server import MockServer
from neuroagent_schemas import NeuroBenchCase

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES = REPO_ROOT / "data/neurobench/cases"

SET_PARAM = {"interpret_labs": "panels", "analyze_csf": "special_tests",
             "obtain_tissue_diagnosis": "molecular_assays"}
SLOT = {"interpret_labs": "labs", "analyze_csf": "csf",
        "obtain_tissue_diagnosis": "tissue_diagnosis"}


def _payloads_for(raw: dict, tool: str) -> list[tuple[str, dict]]:
    """Every payload stored in the case that THIS tool could be served — its own slots only."""
    found: list[tuple[str, dict]] = []
    initial = (raw.get("initial_tool_outputs") or {}).get(SLOT[tool])
    if isinstance(initial, dict):
        found.append((f"initial:{SLOT[tool]}", initial))
    for entry in raw.get("followup_outputs") or []:
        if entry.get("tool_name") == tool and isinstance(entry.get("output"), dict):
            found.append((f"followup:{entry.get('trigger_action')}", entry["output"]))
    fallback = (raw.get("fallback_tool_outputs") or {}).get(SLOT[tool])
    if isinstance(fallback, dict):
        found.append((f"fallback:{SLOT[tool]}", fallback))
    return found


SEED = CASES / "SE-M03.json"


def _row(test: str, value: str, unit: str) -> dict:
    return {"test": test, "value": value, "unit": unit,
            "reference_range": "n/a", "is_abnormal": False}


def _case_with(initial_labs: dict, followup_labs: dict) -> NeuroBenchCase:
    """A real case with its laboratory payloads replaced.

    Built from a case file rather than hand-written so the fixture cannot pass a schema the real
    dataset would fail — the patient profile, encounter type and policy stay exactly as authored.
    """
    raw = json.loads(SEED.read_text())
    raw["initial_tool_outputs"]["labs"] = initial_labs
    raw["followup_outputs"] = [{
        "trigger_action": "request_aed_optimization",
        "tool_name": "interpret_labs",
        "output": followup_labs,
    }]
    return NeuroBenchCase.model_validate(raw)


FIRST_LINE = {
    "panels": {"Complete Blood Count": [_row("WBC", "11.2", "10^9/L")],
               "Basic Metabolic Panel": [_row("Sodium", "138", "mmol/L")],
               "Magnesium": [_row("Magnesium", "0.6", "mmol/L")],
               "Lactate": [_row("Lactate", "4.1", "mmol/L")],
               "AED Levels": [_row("Valproate", "42", "ug/mL")]},
    "interpretation": "first-line panel",
    "abnormal_values_summary": ["low magnesium"],
}
AFTER_ESCALATION = {
    "panels": {"AED Levels After Dose Escalation": [_row("Valproate", "78", "ug/mL")]},
    "interpretation": "therapeutic after escalation",
    "abnormal_values_summary": [],
}


@pytest.mark.skipif(not SEED.exists(), reason="cases not present")
def test_a_narrow_reorder_still_reaches_its_followup() -> None:
    """The guard must not close the escalation path it exists to protect."""
    case = _case_with(FIRST_LINE, AFTER_ESCALATION)
    served = MockServer(case).get_output("interpret_labs", {"panels": ["AED_levels"]})
    assert served.success
    assert "After Dose Escalation" in json.dumps(served.output), (
        "a re-order naming only the escalated assay must still be answered by the follow-up; the "
        "comparison only decides orders of two or more assays, where one matched token proves nothing"
    )


@pytest.mark.skipif(not SEED.exists(), reason="cases not present")
def test_a_broad_order_keeps_the_payload_that_answers_more_of_it() -> None:
    case = _case_with(FIRST_LINE, AFTER_ESCALATION)
    served = MockServer(case).get_output(
        "interpret_labs", {"panels": ["CBC", "BMP", "magnesium", "lactate", "AED_levels"]})
    assert served.success
    body = json.dumps(served.output)
    assert "Magnesium" in body and "Lactate" in body, (
        "the five-assay order shares only the token 'aed' with the follow-up trigger; the initial "
        "panel answers four of the five and must be the payload served"
    )


@pytest.mark.skipif(not CASES.exists(), reason="cases not present")
def test_no_set_valued_order_is_served_a_payload_another_one_beats() -> None:
    """The dataset-wide invariant, in the terms the defect was measured in.

    Two orders are exempted by name, not by rule. Both bacterial-meningitis cases order
    `special_tests: [meningitis_panel]` — the multiplex PCR — and are served the initial CSF, which
    carries Gram stain and culture but no PCR panel; the PCR sits in a repeat tap (RP03) or a culture
    read-out (RP05). Their `expected_finding` asks for opening pressure, PMN pleocytosis and the
    glucose ratio, which the initial CSF delivers, and in both the Gram stain identifies the
    organism. Whether a first CSF should carry a PCR panel is a question about what these cases
    sample; answering it by writing a PCR result would invent a measurement. Listed so that a *new*
    crossing fails this test instead of hiding in a count.
    """
    known = {
        ("BACT-MEN-RP03", "analyze_csf"), ("BACT-MEN-RP05", "analyze_csf"),
    }
    crossed: list[str] = []
    for path in sorted(CASES.glob("*.json")):
        raw = json.loads(path.read_text())
        case = NeuroBenchCase.model_validate(raw)
        server = MockServer(case)
        for criterion in case.ground_truth.action_criteria:
            for pattern in criterion.alternatives:
                key = SET_PARAM.get(pattern.tool_name)
                if key is None:
                    continue
                params = dict(pattern.required_arguments)
                wanted = params.get(key) or []
                if isinstance(wanted, str):
                    wanted = [wanted]
                if not wanted:
                    continue
                result = server.get_output(pattern.tool_name, params)
                if not result.success or result.output is None:
                    continue
                served = MockServer._assays_named(result.output, wanted)
                best = max(
                    (
                        MockServer._assays_named(payload, wanted)
                        for _, payload in _payloads_for(raw, pattern.tool_name)
                    ),
                    default=served,
                )
                if best > served and (case.case_id, pattern.tool_name) not in known:
                    crossed.append(
                        f"{case.case_id} {pattern.tool_name}: served {served}/{len(wanted)}, "
                        f"another stored payload answers {best}"
                    )
    assert not crossed, "set-valued orders served a payload another one beats:\n" + "\n".join(crossed)


@pytest.mark.skipif(not CASES.exists(), reason="cases not present")
def test_no_required_order_receives_nothing_it_names() -> None:
    """A required action must not be answered by a payload containing none of what it asks for.

    Sharper than the comparison above and independent of it: this does not ask whether a better payload
    exists, it asks whether the agent learned anything at all. It was 15 before the August 2026 delivery
    audit — thirteen bacterial meningitis cases billing a 322 EUR multiplex PCR panel that no case
    returned, plus the two below.

    The two exemptions order `autoimmune_panel` and are served LGI1 and NMDAR antibodies, which are that
    panel's members and exactly what their `expected_finding` describes. That is a gap in the scorer's
    class map, not a missing measurement; closing it means extending `_ANALYTE_CLASSES`, which moves
    published required-coverage numbers and is deferred to land with the re-baseline.
    """
    known = {("FEPI-TEMP-P02", "analyze_csf"), ("SE-S12", "analyze_csf")}
    empty: list[str] = []
    for path in sorted(CASES.glob("*.json")):
        case = NeuroBenchCase.model_validate(json.loads(path.read_text()))
        server = MockServer(case)
        for criterion in case.ground_truth.action_criteria:
            if criterion.importance.value != "required":
                continue
            for pattern in criterion.alternatives:
                key = SET_PARAM.get(pattern.tool_name)
                if key is None:
                    continue
                params = dict(pattern.required_arguments)
                wanted = params.get(key) or []
                if isinstance(wanted, str):
                    wanted = [wanted]
                if not wanted:
                    continue
                result = server.get_output(pattern.tool_name, params)
                if not result.success or result.output is None:
                    continue
                if (
                    MockServer._assays_named(result.output, wanted) == 0
                    and (case.case_id, pattern.tool_name) not in known
                ):
                    empty.append(
                        f"{case.case_id} {pattern.tool_name}: ordered {list(wanted)}, "
                        "served a payload naming none of them"
                    )
    assert not empty, "required orders answered by nothing they name:\n" + "\n".join(empty)
