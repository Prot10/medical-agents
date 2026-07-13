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
from neuroagent.evaluation.llm_judge import LLMJudge, ReasoningScore
from neuroagent.evaluation.metrics import MetricsCalculator, CaseMetrics
from neuroagent.evaluation.runner import EvaluationRunner
from neuroagent.datasets import load_dataset


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
    """Tests for the NeuroBench gold-trajectory regen metrics on GroundTruth surface:
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


# ---------------------------------------------------------------------------
# EvaluationRunner: per-case fault isolation, checkpointing, strict splits
# ---------------------------------------------------------------------------

FIXTURE_CASE = Path(__file__).parent / "fixtures" / "sample_case.json"


def _make_dataset(tmp_path: Path, case_ids: list[str], split_ids: list[str] | None = None) -> Path:
    """Build a minimal dataset dir from copies of the sample fixture."""
    dataset = tmp_path / "dataset"
    cases_dir = dataset / "cases"
    cases_dir.mkdir(parents=True)
    base = json.loads(FIXTURE_CASE.read_text())
    for cid in case_ids:
        data = dict(base)
        data["case_id"] = cid
        (cases_dir / f"{cid}.json").write_text(json.dumps(data))
    if split_ids is not None:
        splits = dataset / "splits"
        splits.mkdir()
        (splits / "test.txt").write_text("\n".join(split_ids))
    return dataset


class TestEvaluationRunnerFaultTolerance:
    @pytest.fixture
    def config(self):
        from neuroagent.agent.config import load_agent_config
        return load_agent_config(model="test-model", max_turns=3)

    def _patch_orchestrator(self, monkeypatch, fail_case_ids: set[str]):
        class FakeOrchestrator:
            def __init__(self, config=None, tool_registry=None, rules_engine=None):
                pass

            def run(self, patient_info: str, case_id: str) -> AgentTrace:
                if case_id in fail_case_ids:
                    raise RuntimeError(f"boom on {case_id}")
                trace = AgentTrace(case_id=case_id)
                trace.set_final_response("### Primary Diagnosis\nX")
                return trace

        monkeypatch.setattr(
            "neuroagent.evaluation.runner.AgentOrchestrator", FakeOrchestrator
        )

    def test_failed_case_is_recorded_and_run_continues(self, tmp_path, monkeypatch, config):
        dataset = _make_dataset(tmp_path, ["CASE-S1", "CASE-S2", "CASE-S3"])
        self._patch_orchestrator(monkeypatch, fail_case_ids={"CASE-S2"})

        runner = EvaluationRunner(config, str(dataset))
        results = runner.run_evaluation(split="test", enable_rules=False)

        assert results.num_cases == 2
        assert results.num_failures == 1
        failure = results.failures[0]
        assert failure["case_id"] == "CASE-S2"
        assert "boom on CASE-S2" in failure["error"]
        assert "traceback" in failure

    def test_checkpoint_written_incrementally_and_atomically(self, tmp_path, monkeypatch, config):
        dataset = _make_dataset(tmp_path, ["CASE-S1", "CASE-S2"])
        self._patch_orchestrator(monkeypatch, fail_case_ids={"CASE-S2"})
        out_dir = tmp_path / "out"

        runner = EvaluationRunner(config, str(dataset))
        results = runner.run_evaluation(
            split="test", enable_rules=False, output_dir=out_dir
        )

        ckpt = out_dir / "eval_checkpoint.json"
        assert ckpt.exists()
        payload = json.loads(ckpt.read_text())
        assert payload["num_completed"] == 1
        assert payload["num_failures"] == 1
        assert payload["results"][0]["case_id"] == "CASE-S1"
        assert payload["failures"][0]["case_id"] == "CASE-S2"
        # No leftover temp files from the atomic write
        assert list(out_dir.glob("*.tmp")) == []
        assert results.num_cases == 1

    def test_missing_split_case_file_raises(self, tmp_path, config):
        dataset = _make_dataset(
            tmp_path, ["CASE-S1"], split_ids=["CASE-S1", "CASE-MISSING"]
        )
        runner = EvaluationRunner(config, str(dataset))
        with pytest.raises(FileNotFoundError, match="CASE-MISSING"):
            runner.run_evaluation(split="test", enable_rules=False)


# ---------------------------------------------------------------------------
# datasets.load_dataset: strict by default
# ---------------------------------------------------------------------------

class TestLoadDatasetStrict:
    def test_valid_dataset_loads(self, tmp_path):
        dataset = _make_dataset(tmp_path, ["CASE-S1"])
        idx, objs = load_dataset(dataset)
        assert set(objs) == {"CASE-S1"}

    def test_invalid_case_raises_by_default(self, tmp_path):
        dataset = _make_dataset(tmp_path, ["CASE-S1"])
        (dataset / "cases" / "BROKEN-S1.json").write_text("{not valid json")
        with pytest.raises(ValueError, match="BROKEN-S1"):
            load_dataset(dataset)

    def test_skip_invalid_exposes_skipped_count(self, tmp_path):
        dataset = _make_dataset(tmp_path, ["CASE-S1"])
        (dataset / "cases" / "BROKEN-S1.json").write_text("{not valid json")
        skipped: list[str] = []
        idx, objs = load_dataset(dataset, skip_invalid=True, skipped=skipped)
        assert set(objs) == {"CASE-S1"}
        assert skipped == ["BROKEN-S1.json"]


# ---------------------------------------------------------------------------
# LLMJudge response parsing
# ---------------------------------------------------------------------------

class TestJudgeParsing:
    def _parse(self, response: str) -> ReasoningScore:
        judge = LLMJudge.__new__(LLMJudge)  # skip __init__ (needs an LLM client)
        return judge._parse_response(response)

    def test_parse_failure_is_flagged_invalid(self):
        score = self._parse("The agent did well overall, no JSON here.")
        assert score.valid is False
        assert score.composite_score == 0.0
        assert "Failed to parse" in score.justification

    def test_composite_recomputed_not_trusted(self):
        payload = {
            "diagnostic_accuracy": 5,
            "evidence_identification": 4,
            "evidence_integration": 4,
            "differential_reasoning": 4,
            "tool_efficiency": 3,
            "clinical_safety": 5,
            "red_herring_handling": None,
            "uncertainty_calibration": 4,
            "composite_score": 99.0,  # judge-reported, wrong scale
        }
        score = self._parse(json.dumps(payload))
        assert score.valid is True
        assert score.judge_reported_composite == 99.0
        # Locally recomputed on the 0-1 scale from dimensions + rubric weights
        expected = ReasoningScore(
            diagnostic_accuracy=5,
            evidence_identification=4,
            evidence_integration=4,
            differential_reasoning=4,
            tool_efficiency=3,
            clinical_safety=5,
            red_herring_handling=None,
            uncertainty_calibration=4,
        ).compute_composite()
        assert score.composite_score == expected
        assert 0.0 <= score.composite_score <= 1.0
