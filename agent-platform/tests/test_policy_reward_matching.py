"""Criterion matching: assay vocabulary and advertised schema defaults (October 2026 review)."""

from __future__ import annotations

import pytest

from neuroagent.evaluation.policy_reward import criterion_matches, executed_arguments
from neuroagent_schemas import ActionCriterion, AvoidedActionCriterion, ToolAction


def _criterion(tool: str, **required) -> ActionCriterion:
    return ActionCriterion(
        criterion_id="c",
        label="c",
        importance="required",
        alternatives=[{"tool_name": tool, "required_arguments": required}],
    )


def _labs(*panels: str) -> ToolAction:
    return ToolAction(tool_name="interpret_labs", arguments={"clinical_context": "x", "panels": list(panels)})


@pytest.mark.parametrize(
    ("ordered", "wanted"),
    [
        (["paraneoplastic"], ["paraneoplastic_panel"]),
        (["paraneoplastic_panel"], ["paraneoplastic"]),
        (["LFTs"], ["LFT"]),
        (["LFT"], ["LFTs"]),
        (["tox_screen"], ["toxicology"]),
        (["toxicology"], ["tox_screen"]),
        (["syphilis"], ["RPR"]),
        (["coagulation"], ["INR"]),
        (["CMP"], ["BMP", "LFTs"]),
        (["CMP", "CBC"], ["CBC", "BMP"]),
        (["CMP"], ["sodium", "glucose"]),
        (["Protein C"], ["protein_C"]),
        # Class terms are met by a member (existing vocabulary rule).
        (["valproate_level"], ["AED_levels"]),
    ],
)
def test_clinically_equivalent_assays_match(ordered, wanted):
    assert criterion_matches(_criterion("interpret_labs", panels=wanted), _labs(*ordered))


@pytest.mark.parametrize(
    ("ordered", "wanted"),
    [
        # Containment is one-directional: a part never stands for the whole.
        (["BMP"], ["CMP"]),
        (["BMP"], ["LFTs"]),
        (["LFTs"], ["CMP"]),
        (["BMP", "LFTs"], ["coagulation"]),
        (["AED_levels"], ["valproate_level"]),
        (["CBC"], ["CBC", "BMP"]),
        (["CRP"], ["paraneoplastic_panel"]),
    ],
)
def test_non_equivalent_assays_do_not_match(ordered, wanted):
    assert not criterion_matches(_criterion("interpret_labs", panels=wanted), _labs(*ordered))


def test_csf_special_tests_use_assay_vocabulary():
    criterion = _criterion("analyze_csf", special_tests=["paraneoplastic"])
    action = ToolAction(tool_name="analyze_csf", arguments={"clinical_context": "x", "special_tests": ["paraneoplastic_panel"]})
    assert criterion_matches(criterion, action)


def test_schema_default_satisfies_a_criterion_on_an_omitted_argument():
    criterion = _criterion("order_microbiology", specimen="blood", before_antimicrobials=True)
    omitted = ToolAction(tool_name="order_microbiology", arguments={"clinical_context": "x", "specimen": "blood"})
    assert executed_arguments(omitted)["before_antimicrobials"] is True
    assert criterion_matches(criterion, omitted)
    after = ToolAction(
        tool_name="order_microbiology",
        arguments={"clinical_context": "x", "specimen": "blood", "before_antimicrobials": False},
    )
    assert not criterion_matches(criterion, after)


def test_schema_default_false_does_not_meet_a_true_requirement():
    # `order_ct_scan.angiography` defaults to false: a bare CT is not the CT angiogram.
    criterion = _criterion("order_ct_scan", angiography=True)
    bare = ToolAction(tool_name="order_ct_scan", arguments={"clinical_context": "x"})
    assert not criterion_matches(criterion, bare)
    assert criterion_matches(_criterion("order_ct_scan", angiography=False), bare)


def test_avoided_actions_see_the_executed_call():
    avoided = AvoidedActionCriterion(
        criterion_id="contrast_ct",
        severity="harm",
        alternatives=[{"tool_name": "order_ct_scan", "required_arguments": {"contrast": True}}],
        rationale="r",
    )
    bare = ToolAction(tool_name="order_ct_scan", arguments={"clinical_context": "x"})
    assert not criterion_matches(avoided, bare)
    assert criterion_matches(
        avoided, ToolAction(tool_name="order_ct_scan", arguments={"clinical_context": "x", "contrast": True})
    )


def test_other_tool_never_matches():
    assert not criterion_matches(_criterion("interpret_labs", panels=["CBC"]), ToolAction(
        tool_name="analyze_csf", arguments={"clinical_context": "x", "special_tests": ["CBC"]}
    ))
