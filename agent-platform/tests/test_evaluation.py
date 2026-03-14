"""Tests for the evaluation system."""

import json
from pathlib import Path

import pytest

from neuroagent_schemas import NeuroBenchCase
from neuroagent.agent.reasoning import AgentTrace
from neuroagent.evaluation.metrics import MetricsCalculator, CaseMetrics
from neuroagent.evaluation.noise_injector import NoiseInjector, NoiseType


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


class TestNoiseInjector:
    def test_confidence_noise(self):
        injector = NoiseInjector(seed=42)
        output = {"confidence": 0.9, "findings": [{"type": "sharp_wave"}]}
        noisy = injector.inject(output, "analyze_eeg", NoiseType.CONFIDENCE, severity=0.5)
        assert noisy["confidence"] != 0.9  # Should be modified
        assert 0.0 <= noisy["confidence"] <= 1.0

    def test_completeness_noise(self):
        injector = NoiseInjector(seed=42)
        output = {"findings": [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}]}
        noisy = injector.inject(output, "analyze_eeg", NoiseType.COMPLETENESS, severity=0.5)
        assert len(noisy["findings"]) < 4

    def test_zero_severity(self):
        injector = NoiseInjector()
        output = {"confidence": 0.9, "findings": []}
        noisy = injector.inject(output, "analyze_eeg", NoiseType.CONFIDENCE, severity=0.0)
        assert noisy == output  # No change
