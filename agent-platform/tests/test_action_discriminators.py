"""Scoring credits the study the agent ordered, not merely the tool it named.

Two defects motivated these tests, both found while acting on the July 2026 clinical tool
review:

1. Only `order_advanced_imaging` and `order_specialized_test` had a discriminating
   parameter. `interpret_labs` was credited on the tool name alone, so a call ordering a
   EUR 2300 paraneoplastic panel satisfied a ground truth asking for EUR 18 of ammonia. The
   149-value analyte vocabulary in the cases, and the per-analyte prices in `costs.yaml`,
   were never consulted by the score — which is why the reviewers read the shared lab bucket
   as unscoreable.

2. The action metrics were sets of *tool names*, so a case naming one tool in several
   optimal actions collapsed to a single action. 61% of the 600 cases do that, and
   `order_specialized_test` does it in 197: a case requiring both EMG/NCS and an ALS gene
   panel counted as one required action, and ordering only the first scored full coverage.

Measured effect on an agent that calls every correct tool but never says which study:
required coverage 0.885 -> 0.544, cases at full required coverage 336 -> 78 of 600.
"""

from __future__ import annotations

import pytest
from neuroagent_schemas import GroundTruth, ToolClassification
from neuroagent_schemas.evaluation import ActionStep

from neuroagent.agent.reasoning import AgentTrace, AgentTurn
from neuroagent.evaluation.metrics import (
    MetricsCalculator,
    _action_key,
    _classification_matches,
    _optimal_action_satisfied,
)


def calls(*specs: tuple[str, dict]) -> list[tuple[str, dict]]:
    return [(name, args) for name, args in specs]


class TestSetValuedDiscriminators:
    """`interpret_labs.panels` / `analyze_csf.special_tests`: containment, accumulated."""

    def test_exact_set_satisfies(self):
        assert _optimal_action_satisfied(
            "interpret_labs", {"panels": ["ammonia", "CBC"]},
            calls(("interpret_labs", {"panels": ["CBC", "ammonia"]})),
        )

    def test_superset_satisfies(self):
        """Ordering more than asked still covers the action; waste is priced elsewhere."""
        assert _optimal_action_satisfied(
            "interpret_labs", {"panels": ["ammonia"]},
            calls(("interpret_labs", {"panels": ["ammonia", "CBC", "TSH"]})),
        )

    def test_missing_analyte_does_not_satisfy(self):
        assert not _optimal_action_satisfied(
            "interpret_labs", {"panels": ["ammonia", "CBC"]},
            calls(("interpret_labs", {"panels": ["CBC"]})),
        )

    def test_wrong_analyte_does_not_satisfy(self):
        """The defect in one line: a paraneoplastic panel is not an ammonia."""
        assert not _optimal_action_satisfied(
            "interpret_labs", {"panels": ["ammonia"]},
            calls(("interpret_labs", {"panels": ["paraneoplastic_panel"]})),
        )

    def test_accumulates_across_calls(self):
        """Labs ordered in two batches are one workup, not a miss."""
        assert _optimal_action_satisfied(
            "interpret_labs", {"panels": ["ammonia", "CBC"]},
            calls(
                ("interpret_labs", {"panels": ["CBC"]}),
                ("interpret_labs", {"panels": ["ammonia"]}),
            ),
        )

    def test_unspecified_panels_is_a_wildcard(self):
        assert _optimal_action_satisfied(
            "interpret_labs", {}, calls(("interpret_labs", {"panels": ["anything"]}))
        )
        assert _optimal_action_satisfied("interpret_labs", None, calls(("interpret_labs", {})))

    def test_bare_string_is_tolerated(self):
        """A model may pass a single analyte as a string rather than a one-element list."""
        assert _optimal_action_satisfied(
            "interpret_labs", {"panels": "ammonia"},
            calls(("interpret_labs", {"panels": "ammonia"})),
        )

    def test_csf_special_tests_follow_the_same_rule(self):
        assert _optimal_action_satisfied(
            "analyze_csf", {"special_tests": ["HSV_PCR"]},
            calls(("analyze_csf", {"special_tests": ["HSV_PCR", "cytology"]})),
        )
        assert not _optimal_action_satisfied(
            "analyze_csf", {"special_tests": ["HSV_PCR"]},
            calls(("analyze_csf", {"special_tests": ["RT_QuIC"]})),
        )


class TestScalarDiscriminators:
    def test_matching_value_satisfies(self):
        assert _optimal_action_satisfied(
            "analyze_eeg", {"eeg_type": "continuous_icu"},
            calls(("analyze_eeg", {"eeg_type": "continuous_icu"})),
        )

    def test_wrong_value_does_not_satisfy(self):
        """A 30-minute routine EEG is not continuous ICU monitoring — 230 EUR vs 828 EUR."""
        assert not _optimal_action_satisfied(
            "analyze_eeg", {"eeg_type": "continuous_icu"},
            calls(("analyze_eeg", {"eeg_type": "routine"})),
        )

    def test_omitted_parameter_falls_back_to_the_schema_default(self):
        """Ground truth pinning the default is satisfied by a call that omits it."""
        assert _optimal_action_satisfied(
            "analyze_eeg", {"eeg_type": "routine"}, calls(("analyze_eeg", {}))
        )
        assert _optimal_action_satisfied(
            "order_ct_scan", {"contrast": False}, calls(("order_ct_scan", {}))
        )

    def test_non_default_is_not_satisfied_by_omission(self):
        assert not _optimal_action_satisfied(
            "order_ct_scan", {"angiography": True}, calls(("order_ct_scan", {}))
        )

    def test_multiple_pinned_parameters_must_all_match(self):
        """SAH: noncontrast CT first, CTA as a separate subsequent study."""
        want = {"contrast": False, "angiography": False}
        assert _optimal_action_satisfied(
            "order_ct_scan", want, calls(("order_ct_scan", {"contrast": False, "angiography": False}))
        )
        assert not _optimal_action_satisfied(
            "order_ct_scan", want, calls(("order_ct_scan", {"contrast": True, "angiography": True}))
        )

    def test_unpinned_discriminator_is_a_wildcard(self):
        assert _optimal_action_satisfied(
            "analyze_brain_mri", {}, calls(("analyze_brain_mri", {"protocol": "dementia"}))
        )

    def test_tool_with_no_discriminator_matches_on_name(self):
        assert _optimal_action_satisfied(
            "analyze_ecg", {"clinical_context": "anything"}, calls(("analyze_ecg", {}))
        )


class TestActionIdentity:
    """Distinct studies under one tool name must be distinct actions."""

    def test_same_tool_different_study_are_different_actions(self):
        a = _action_key("order_specialized_test", {"test_type": "emg_ncs"})
        b = _action_key("order_specialized_test", {"test_type": "genetic_panel:ALS"})
        assert a != b

    def test_panel_order_does_not_affect_identity(self):
        assert _action_key("interpret_labs", {"panels": ["CBC", "TSH"]}) == _action_key(
            "interpret_labs", {"panels": ["TSH", "CBC"]}
        )

    def test_clinical_context_does_not_affect_identity(self):
        """Only the discriminator counts; prose in `clinical_context` is not a study."""
        assert _action_key("analyze_ecg", {"clinical_context": "x"}) == _action_key(
            "analyze_ecg", {"clinical_context": "y"}
        )


def _trace(*specs: tuple[str, dict]) -> AgentTrace:
    tool_calls = [{"function": {"name": n, "arguments": a}} for n, a in specs]
    trace = AgentTrace(
        case_id="T-1", turns=[AgentTurn(turn_number=1, role="assistant", tool_calls=tool_calls)]
    )
    trace.tools_called = [n for n, _ in specs]
    trace.total_tool_calls = len(specs)
    trace.set_final_response("### Primary Diagnosis\nTest condition (Confidence: 0.95)")
    return trace


def _ground_truth(*actions: ActionStep, useless: list[ToolClassification] | None = None):
    return GroundTruth(
        primary_diagnosis="Test condition",
        icd_code="G00.0",
        differential=[],
        optimal_actions=list(actions),
        useless_tools=useless or [],
    )


class TestTierCoverageIsStudyLevel:
    """The collapse bug: two required studies on one tool are two required actions."""

    @pytest.fixture
    def two_required_studies(self):
        return _ground_truth(
            ActionStep(
                step=1, action="EMG/NCS", tool_name="order_specialized_test",
                tool_parameters={"test_type": "emg_ncs"}, category="required",
            ),
            ActionStep(
                step=2, action="ALS gene panel", tool_name="order_specialized_test",
                tool_parameters={"test_type": "genetic_panel:ALS"}, category="required",
            ),
        )

    def test_both_studies_count_toward_the_total(self, two_required_studies):
        metrics = MetricsCalculator().compute_all(
            _trace(("order_specialized_test", {"test_type": "emg_ncs"})), two_required_studies
        )
        assert metrics.required_total == 2, "two distinct studies must be two required actions"
        assert metrics.required_called == 1
        assert metrics.required_coverage == 0.5

    def test_ordering_both_scores_full_coverage(self, two_required_studies):
        metrics = MetricsCalculator().compute_all(
            _trace(
                ("order_specialized_test", {"test_type": "emg_ncs"}),
                ("order_specialized_test", {"test_type": "genetic_panel:ALS"}),
            ),
            two_required_studies,
        )
        assert metrics.required_coverage == 1.0
        assert metrics.action_recall == 1.0
        assert metrics.action_precision == 1.0


class TestPrecisionBounds:
    def test_precision_never_exceeds_one_when_one_call_serves_two_actions(self):
        """One `interpret_labs` can satisfy two analyte-level actions; precision stays <= 1."""
        ground_truth = _ground_truth(
            ActionStep(
                step=1, action="ammonia", tool_name="interpret_labs",
                tool_parameters={"panels": ["ammonia"]}, category="required",
            ),
            ActionStep(
                step=2, action="CBC", tool_name="interpret_labs",
                tool_parameters={"panels": ["CBC"]}, category="required",
            ),
        )
        metrics = MetricsCalculator().compute_all(
            _trace(("interpret_labs", {"panels": ["ammonia", "CBC"]})), ground_truth
        )
        assert metrics.action_recall == 1.0
        assert 0.0 <= metrics.action_precision <= 1.0
        assert metrics.action_precision == 1.0

    def test_an_unjustified_call_lowers_precision(self):
        ground_truth = _ground_truth(
            ActionStep(
                step=1, action="ammonia", tool_name="interpret_labs",
                tool_parameters={"panels": ["ammonia"]}, category="required",
            ),
        )
        metrics = MetricsCalculator().compute_all(
            _trace(
                ("interpret_labs", {"panels": ["ammonia"]}),
                ("order_advanced_imaging", {"modality": "amyloid_PET"}),
            ),
            ground_truth,
        )
        assert metrics.action_precision == 0.5


class TestRestraintCases:
    """FND becomes a case with no required actions; the metrics must not divide by zero."""

    def test_no_optimal_actions_does_not_crash_or_score_vacuously(self):
        ground_truth = _ground_truth(
            useless=[
                ToolClassification(
                    tool_name="analyze_brain_mri", tool_parameters={},
                    rationale="clinical diagnosis; imaging adds cost without yield",
                )
            ]
        )
        metrics = MetricsCalculator().compute_all(
            _trace(("analyze_brain_mri", {"protocol": "standard"})), ground_truth
        )
        assert metrics.required_total == 0
        assert metrics.required_coverage == 0.0
        assert metrics.action_recall == 0.0
        assert metrics.useless_calls == 1

    def test_abstaining_agent_is_not_charged(self):
        ground_truth = _ground_truth(
            useless=[
                ToolClassification(
                    tool_name="analyze_brain_mri", tool_parameters={}, rationale="no yield"
                )
            ]
        )
        metrics = MetricsCalculator().compute_all(_trace(), ground_truth)
        assert metrics.useless_calls == 0


class TestClassificationMatching:
    """A useless/harmful classification must be reachable by a realistic agent call.

    Every one of these started as a dataset defect. `_classification_matches` compared
    parameters by equality, so a classification carrying a list matched only an agent whose
    call carried that exact list — which no agent produces, because analytes are bundled. Seven
    classifications in the 600 cases were therefore dead: five of them on `analyze_csf.basic`,
    a parameter that does not exist in the tool's schema at all. Nothing failed; they simply
    never fired.
    """

    def test_wildcard_condemns_the_tool_however_parameterised(self):
        classification = ToolClassification(
            tool_name="analyze_csf", tool_parameters={}, rationale="LP contraindicated"
        )
        assert _classification_matches(classification, "analyze_csf", {"special_tests": ["HSV_PCR"]})
        assert _classification_matches(classification, "analyze_csf", {})

    def test_scalar_parameter_still_needs_an_exact_match(self):
        classification = ToolClassification(
            tool_name="order_specialized_test",
            tool_parameters={"test_type": "tilt_table"},
            rationale="relative contraindication in severe aortic stenosis",
        )
        assert _classification_matches(
            classification, "order_specialized_test", {"test_type": "tilt_table"}
        )
        assert not _classification_matches(
            classification, "order_specialized_test", {"test_type": "exercise_stress_test"}
        )

    def test_set_parameter_matches_inside_a_bundle(self):
        """The reviewers' case: one untargeted assay condemned among required ones."""
        classification = ToolClassification(
            tool_name="interpret_labs",
            tool_parameters={"panels": ["TSH"]},
            rationale="untargeted thyroid testing has no established role here",
        )
        assert _classification_matches(
            classification, "interpret_labs", {"panels": ["CBC", "BMP", "troponin", "TSH"]}
        )
        assert not _classification_matches(
            classification, "interpret_labs", {"panels": ["CBC", "BMP", "troponin"]}
        )

    def test_set_parameter_tolerates_spelling(self):
        classification = ToolClassification(
            tool_name="interpret_labs",
            tool_parameters={"panels": ["D_dimer"]},
            rationale="no suspicion of pulmonary embolism",
        )
        assert _classification_matches(
            classification, "interpret_labs", {"panels": ["CBC", "D-dimer"]}
        )

    def test_a_different_tool_never_matches(self):
        classification = ToolClassification(
            tool_name="analyze_csf", tool_parameters={}, rationale="no role"
        )
        assert not _classification_matches(classification, "analyze_brain_mri", {})
