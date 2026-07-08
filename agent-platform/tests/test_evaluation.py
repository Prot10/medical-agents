"""Tests for the evaluation system."""

import json
from pathlib import Path

import pytest

from neuroagent_schemas import NeuroBenchCase
from neuroagent_schemas.enums import ActionCategory, Likelihood, SequenceSeverity
from neuroagent_schemas.evaluation import (
    ActionStep,
    DifferentialDx,
    GroundTruth,
    SequenceConstraint,
    ToolClassification,
)
from neuroagent.agent.reasoning import AgentTrace, AgentTurn
from neuroagent.evaluation.metrics import MetricsCalculator, CaseMetrics


@pytest.fixture
def sample_case() -> NeuroBenchCase:
    fixture_path = Path(__file__).parent / "fixtures" / "sample_case.json"
    data = json.loads(fixture_path.read_text())
    return NeuroBenchCase.model_validate(data)


@pytest.fixture
def correct_trace() -> AgentTrace:
    """A trace that matches the ground truth well."""
    trace = AgentTrace(case_id="FEPI-TEMP-001")
    trace.tools_called = ["interpret_labs", "analyze_eeg", "analyze_brain_mri",
                          "search_medical_literature", "check_drug_interactions"]
    trace.total_tool_calls = 5
    trace.set_final_response(
        "### Primary Diagnosis\n"
        "Focal epilepsy secondary to right mesial temporal mass (likely DNET) (Confidence: 0.90)\n\n"
        "### Differential Diagnoses\n"
        "1. Focal epilepsy with ganglioglioma\n"
        "2. Low-grade astrocytoma\n"
    )
    return trace


@pytest.fixture
def wrong_trace() -> AgentTrace:
    """A trace with wrong diagnosis and missing actions."""
    trace = AgentTrace(case_id="FEPI-TEMP-001")
    trace.tools_called = ["interpret_labs"]
    trace.total_tool_calls = 1
    trace.set_final_response("### Primary Diagnosis\nMigraine with aura")
    return trace


class TestMetricsCalculator:
    def test_correct_diagnosis(self, correct_trace, sample_case):
        calc = MetricsCalculator()
        metrics = calc.compute_all(correct_trace, sample_case.ground_truth)
        assert metrics.diagnostic_accuracy_top1 is True
        assert metrics.diagnostic_accuracy_top3 is True

    def test_wrong_diagnosis(self, wrong_trace, sample_case):
        calc = MetricsCalculator()
        metrics = calc.compute_all(wrong_trace, sample_case.ground_truth)
        assert metrics.diagnostic_accuracy_top1 is False

    def test_action_recall(self, correct_trace, sample_case):
        calc = MetricsCalculator()
        metrics = calc.compute_all(correct_trace, sample_case.ground_truth)
        assert metrics.action_recall > 0.8  # Most required actions completed

    def test_action_recall_incomplete(self, wrong_trace, sample_case):
        calc = MetricsCalculator()
        metrics = calc.compute_all(wrong_trace, sample_case.ground_truth)
        assert metrics.action_recall < 0.5  # Only 1 of 5 actions

    def test_critical_actions(self, correct_trace, sample_case):
        calc = MetricsCalculator()
        metrics = calc.compute_all(correct_trace, sample_case.ground_truth)
        assert metrics.critical_actions_hit == 1.0  # All critical actions done

    def test_safety_score(self, correct_trace, sample_case):
        calc = MetricsCalculator()
        metrics = calc.compute_all(correct_trace, sample_case.ground_truth)
        assert metrics.safety_score > 0.5


class TestGoldTrajectoryMetrics:
    """Tests for the v5 gold-trajectory regen metrics on GroundTruth surface:
    useless_tools, harmful_tools, sequence_constraints, redundancy, premature closure.
    """

    @staticmethod
    def _gt(
        useless: list[str] | None = None,
        harmful: list[str] | None = None,
        constraints: list[tuple[str, str, SequenceSeverity]] | None = None,
        optimal_required: list[str] | None = None,
    ) -> GroundTruth:
        return GroundTruth(
            primary_diagnosis="X",
            icd_code="Z00",
            differential=[DifferentialDx(diagnosis="X", likelihood=Likelihood.HIGH)],
            optimal_actions=[
                ActionStep(step=i + 1, action=f"call {t}", tool_name=t,
                           category=ActionCategory.REQUIRED)
                for i, t in enumerate(optimal_required or [])
            ],
            useless_tools=[
                ToolClassification(tool_name=t, rationale="wasted") for t in (useless or [])
            ],
            harmful_tools=[
                ToolClassification(tool_name=t, rationale="contraindicated")
                for t in (harmful or [])
            ],
            sequence_constraints=[
                SequenceConstraint(before=b, after=a, reason="r", severity=s)
                for (b, a, s) in (constraints or [])
            ],
        )

    def test_useless_calls_counted(self):
        gt = self._gt(useless=["order_echocardiogram"], optimal_required=["analyze_brain_mri"])
        trace = AgentTrace(case_id="T")
        trace.tools_called = ["analyze_brain_mri", "order_echocardiogram", "analyze_eeg"]
        trace.total_tool_calls = 3
        m = MetricsCalculator().compute_all(trace, gt)
        assert m.useless_calls == 1
        assert abs(m.useless_call_rate - 1 / 3) < 1e-6
        assert m.harmful_calls == 0

    def test_harmful_calls_hurt_safety(self):
        gt = self._gt(harmful=["analyze_csf"], optimal_required=["order_ct_scan"])
        trace = AgentTrace(case_id="T")
        trace.tools_called = ["analyze_csf"]
        trace.total_tool_calls = 1
        trace.set_final_response("Diagnosis: foo")
        m = MetricsCalculator().compute_all(trace, gt)
        assert m.harmful_calls == 1
        # safety_score should be heavily penalized
        assert m.safety_score < 0.6

    def test_hard_sequence_violation(self):
        gt = self._gt(
            constraints=[("order_ct_scan", "analyze_csf", SequenceSeverity.HARD)],
        )
        # LP done BEFORE CT — hard violation
        trace = AgentTrace(case_id="T")
        trace.tools_called = ["analyze_csf", "order_ct_scan"]
        trace.total_tool_calls = 2
        m = MetricsCalculator().compute_all(trace, gt)
        assert m.sequence_violations == 1
        assert m.hard_sequence_violations == 1

    def test_no_violation_when_correct_order(self):
        gt = self._gt(
            constraints=[("order_ct_scan", "analyze_csf", SequenceSeverity.HARD)],
        )
        trace = AgentTrace(case_id="T")
        trace.tools_called = ["order_ct_scan", "analyze_csf"]
        trace.total_tool_calls = 2
        m = MetricsCalculator().compute_all(trace, gt)
        assert m.sequence_violations == 0

    def test_redundant_calls_counted(self):
        gt = self._gt()
        trace = AgentTrace(case_id="T")
        trace.turns = [
            AgentTurn(turn_number=1, role="assistant",
                      tool_calls=[{"function": {"name": "interpret_labs",
                                                 "arguments": '{"panel": "cbc"}'}}]),
            AgentTurn(turn_number=2, role="tool"),
            AgentTurn(turn_number=3, role="assistant",
                      tool_calls=[{"function": {"name": "interpret_labs",
                                                 "arguments": '{"panel": "cbc"}'}},
                                  {"function": {"name": "interpret_labs",
                                                 "arguments": '{"panel": "metabolic"}'}}]),
        ]
        trace.tools_called = ["interpret_labs", "interpret_labs", "interpret_labs"]
        trace.total_tool_calls = 3
        m = MetricsCalculator().compute_all(trace, gt)
        # Two calls with same (name, args), one with different args -> 1 redundant
        assert m.redundant_calls == 1
        assert abs(m.redundancy_rate - 1 / 3) < 1e-6

    def test_premature_closure_detected(self):
        gt = self._gt()
        trace = AgentTrace(case_id="T")
        trace.turns = [
            AgentTurn(turn_number=1, role="assistant",
                      content="Need more data.",
                      tool_calls=[{"function": {"name": "interpret_labs",
                                                 "arguments": "{}"}}]),
            AgentTurn(turn_number=2, role="tool"),
            AgentTurn(turn_number=3, role="assistant",
                      content="### Primary Diagnosis: ALS\nThe diagnosis is clear."),
            # Two more tool calls AFTER the confident statement
            AgentTurn(turn_number=4, role="assistant",
                      content=None,
                      tool_calls=[{"function": {"name": "analyze_eeg", "arguments": "{}"}}]),
            AgentTurn(turn_number=5, role="tool"),
            AgentTurn(turn_number=6, role="assistant",
                      content=None,
                      tool_calls=[{"function": {"name": "analyze_csf", "arguments": "{}"}}]),
        ]
        trace.tools_called = ["interpret_labs", "analyze_eeg", "analyze_csf"]
        trace.total_tool_calls = 3
        m = MetricsCalculator().compute_all(trace, gt)
        assert m.premature_closure_count == 2

    def test_per_tier_coverage(self):
        gt = GroundTruth(
            primary_diagnosis="X",
            icd_code="Z00",
            optimal_actions=[
                ActionStep(step=1, action="a", tool_name="analyze_brain_mri",
                           category=ActionCategory.REQUIRED),
                ActionStep(step=2, action="b", tool_name="interpret_labs",
                           category=ActionCategory.RECOMMENDED),
                ActionStep(step=3, action="c", tool_name="search_medical_literature",
                           category=ActionCategory.OPTIONAL),
            ],
        )
        trace = AgentTrace(case_id="T")
        trace.tools_called = ["analyze_brain_mri", "search_medical_literature"]
        trace.total_tool_calls = 2
        m = MetricsCalculator().compute_all(trace, gt)
        assert m.required_called == 1 and m.required_total == 1
        assert m.required_coverage == 1.0
        assert m.recommended_called == 0 and m.recommended_total == 1
        assert m.optional_called == 1 and m.optional_total == 1
        assert 0 < m.tool_f1 < 1
