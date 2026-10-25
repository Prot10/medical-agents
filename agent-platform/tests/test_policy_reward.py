from __future__ import annotations

from pathlib import Path

import pytest

from neuroagent.evaluation import ClinicalPolicyReward
from neuroagent_schemas import (
    ActionProposed,
    AssessmentSubmitted,
    ClinicalEpisode,
    DiagnosisCriterion,
    NeuroBenchCase,
    ObservationReceived,
    PolicyReviewStatus,
    RunCompleted,
    SequenceConstraint,
    SubmitAssessment,
    ToolAction,
)

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = ROOT / "data/neurobench/cases/FEPI-TEMP-M01.json"


def approved_case() -> NeuroBenchCase:
    """The fixture case with the policy shape these tests rely on, whatever the case file holds.

    Reviews change the case's tiers, stop rule and constraints; the tests below need no extra
    action allowance and one constraint between two required criteria.
    """
    case = NeuroBenchCase.model_validate_json(CASE_PATH.read_text())
    policy = case.ground_truth
    first, second = [c.criterion_id for c in policy.action_criteria if c.importance.value == "required"][:2]
    return case.model_copy(
        update={
            "ground_truth": policy.model_copy(
                update={
                    "review_status": PolicyReviewStatus.APPROVED,
                    "stop_rule": policy.stop_rule.model_copy(update={"max_additional_actions": 0}),
                    "sequence_constraints": [
                        SequenceConstraint(
                            before_criterion_id=first, after_criterion_id=second, reason="test fixture"
                        )
                    ],
                }
            )
        }
    )


def criterion_action(criterion) -> ToolAction:
    pattern = criterion.alternatives[0]
    return ToolAction(tool_name=pattern.tool_name, arguments=pattern.required_arguments)


def make_episode(case, actions: list[ToolAction], *, diagnosis: str | None = None):
    assessment = SubmitAssessment(
        primary_diagnosis=diagnosis or case.ground_truth.diagnosis.accepted[0],
        confidence=0.9,
        urgency="urgent",
        recommendations=case.ground_truth.assessment.required_recommendations,
    )
    events = []
    for turn, action in enumerate(actions, 1):
        events += [
            ActionProposed(turn=turn, action=action),
            ObservationReceived(turn=turn, tool_name=action.tool_name, success=True, output={}, cost_usd=100.0),
        ]
    turn = len(actions) + 1
    events += [
        ActionProposed(turn=turn, action=assessment),
        AssessmentSubmitted(turn=turn, assessment=assessment),
        RunCompleted(turn=turn),
    ]
    return ClinicalEpisode(events=events)


def by_importance(case, importance: str):
    return [c for c in case.ground_truth.action_criteria if c.importance.value == importance]


def test_only_approved_policy_is_scoreable_by_default():
    draft = NeuroBenchCase.model_validate_json(CASE_PATH.read_text())
    episode = make_episode(draft, [])
    with pytest.raises(ValueError, match="only approved policies"):
        ClinicalPolicyReward().score(episode, draft)
    ClinicalPolicyReward(require_approved=False).score(episode, draft)


def test_complete_required_workup_scores_full_coverage_and_unlocks_efficiency():
    case = approved_case()
    required = [criterion_action(c) for c in by_importance(case, "required")]
    score = ClinicalPolicyReward().score(make_episode(case, required), case)
    assert score.diagnosis == 1
    assert score.required_action_coverage == 1
    assert score.stopping == 1
    assert score.cost_efficiency > 0
    assert score.caps_applied == []


def test_missing_required_evidence_disables_efficiency_and_stopping():
    case = approved_case()
    score = ClinicalPolicyReward().score(make_episode(case, []), case)
    assert score.required_action_coverage == 0
    assert score.stopping == 0
    assert score.cost_efficiency == 0 and score.token_efficiency == 0


def test_recommended_action_after_required_set_is_not_penalized_as_over_testing():
    case = approved_case()
    required = [criterion_action(c) for c in by_importance(case, "required")]
    recommended = [criterion_action(c) for c in by_importance(case, "recommended")][:1]
    waste = [criterion_action(c) for c in case.ground_truth.avoided_actions if c.severity.value == "waste"][:1]
    scorer = ClinicalPolicyReward()
    baseline = scorer.score(make_episode(case, required), case)
    with_recommended = scorer.score(make_episode(case, required + recommended), case)
    with_waste = scorer.score(make_episode(case, required + waste), case)
    assert with_recommended.stopping == 1
    assert with_recommended.recommended_action_coverage > baseline.recommended_action_coverage
    assert with_waste.stopping < 1
    assert with_waste.scalar < baseline.scalar


def test_harm_and_contraindication_caps_survive_a_correct_diagnosis():
    case = approved_case()
    required = [criterion_action(c) for c in by_importance(case, "required")]
    scorer = ClinicalPolicyReward()
    for severity, cap, label in (("harm", 0.35, "harmful_action"), ("contraindicated", 0.10, "contraindicated_action")):
        avoided = case.ground_truth.avoided_actions[0].model_validate(
            {**case.ground_truth.avoided_actions[0].model_dump(), "severity": severity}
        )
        policy = case.ground_truth.model_copy(update={"avoided_actions": [avoided]})
        variant = case.model_copy(update={"ground_truth": policy})
        score = scorer.score(make_episode(variant, required + [criterion_action(avoided)]), variant)
        assert score.diagnosis == 1
        assert score.scalar <= cap and label in score.caps_applied


def test_hard_sequence_violation_caps_at_half():
    case = approved_case()
    constraint = case.ground_truth.sequence_constraints[0].model_validate(
        {**case.ground_truth.sequence_constraints[0].model_dump(), "severity": "hard"}
    )
    policy = case.ground_truth.model_copy(update={"sequence_constraints": [constraint]})
    variant = case.model_copy(update={"ground_truth": policy})
    criteria = {c.criterion_id: c for c in variant.ground_truth.action_criteria}
    before = criterion_action(criteria[constraint.before_criterion_id])
    after = criterion_action(criteria[constraint.after_criterion_id])
    scorer = ClinicalPolicyReward()
    ordered = scorer.score(make_episode(variant, [before, after]), variant)
    reversed_ = scorer.score(make_episode(variant, [after, before]), variant)
    assert ordered.sequence == 1 and ordered.caps_applied == []
    assert reversed_.sequence == 0 and reversed_.scalar <= 0.5
    assert "hard_sequence_violation" in reversed_.caps_applied


def test_diagnosis_matches_synonyms_never_the_code_alone():
    diagnosis = approved_case().ground_truth.diagnosis  # FEPI-TEMP-M01: G40.209 + synonyms
    assert diagnosis.matches("Focal impaired awareness seizures, likely temporal lobe epilepsy")
    assert diagnosis.matches("Mesial temporal lobe epilepsy")
    assert not diagnosis.matches("Seizure disorder")
    assert not diagnosis.matches("Psychogenic non-epileptic seizures")
    assert not diagnosis.matches("Temporal")
    assert diagnosis.code_matches("g40.209") and diagnosis.code_matches("G40-209")
    assert diagnosis.code_matches("G40.2")  # the WHO subcategory of G40.209
    assert not diagnosis.code_matches("G43.109") and not diagnosis.code_matches(None)


def test_diagnosis_drops_denied_clauses():
    sah = DiagnosisCriterion(accepted=["aneurysmal subarachnoid hemorrhage", "aneurysmal SAH"])
    assert sah.matches("Aneurysmal SAH, Hunt-Hess 3")
    assert not sah.matches("Non-aneurysmal SAH")
    assert not sah.matches("Non aneurysmal subarachnoid hemorrhage")
    assert not sah.matches("Perimesencephalic SAH, not aneurysmal")
    ms = DiagnosisCriterion(accepted=["multiple sclerosis", "MS"])
    assert not ms.matches("MOGAD rather than MS")
    assert not ms.matches("Multiple sclerosis excluded; MOG antibody disease")
    assert not ms.matches("Not multiple sclerosis")
    assert ms.matches("Relapsing-remitting MS; NMOSD unlikely")
    als = DiagnosisCriterion(accepted=["amyotrophic lateral sclerosis", "ALS"])
    assert not als.matches("Thyrotoxicosis, ALS criteria not met")
    assert not als.matches("Cervical myelopathy mimicking ALS")
    assert not als.matches("Cervical myelopathy, previously misdiagnosed as ALS")
    assert DiagnosisCriterion(accepted=["ALS"], rejected=["bell palsy"]).matches("ALS, initially diagnosed as Bell palsy")


def test_rejected_labels_and_mixed_components():
    pd = DiagnosisCriterion(accepted=["parkinson disease", "PD"], rejected=["PD dementia", "parkinson disease dementia"])
    assert pd.matches("Idiopathic PD")
    assert not pd.matches("PD dementia")
    assert pd.matches("PD, no dementia")
    assert pd.matches("PD without dementia")
    lgi1 = DiagnosisCriterion(accepted=["autoimmune encephalitis"], rejected=["LGI1 encephalitis"])
    assert lgi1.matches("Seronegative autoimmune encephalitis, LGI1-negative")
    assert DiagnosisCriterion(accepted=["myasthenia gravis"]).matches("AChR-negative myasthenia gravis")
    aura = DiagnosisCriterion(accepted=["migraine with aura"])
    assert not aura.matches("Migraine without aura")
    als = DiagnosisCriterion(accepted=["ALS"], rejected=["multiple sclerosis", "MS"])
    assert not als.matches("ALS or MS")
    assert als.matches("ALS rather than MS")
    mixed = DiagnosisCriterion(
        accepted=["hepatic encephalopathy"], required_components=[["wernicke encephalopathy", "wernicke"]]
    )
    assert mixed.matches("Wernicke encephalopathy with concurrent hepatic encephalopathy")
    assert not mixed.matches("Hepatic encephalopathy")
    assert not mixed.matches("Hepatic encephalopathy; Wernicke unlikely")


def test_icd_code_is_reported_without_weight():
    case = approved_case()
    required = [criterion_action(c) for c in by_importance(case, "required")]
    scorer = ClinicalPolicyReward()
    right = make_episode(case, required)
    code = case.ground_truth.diagnosis.icd_codes[0]
    for event in right.events:
        if isinstance(event, AssessmentSubmitted):
            event.assessment.icd10_code = code
    coded, uncoded = scorer.score(right, case), scorer.score(make_episode(case, required), case)
    assert coded.icd_code == 1 and uncoded.icd_code == 0
    assert coded.scalar == uncoded.scalar
    wrong_label = scorer.score(make_episode(case, required, diagnosis="Seizure disorder"), case)
    assert wrong_label.diagnosis == 0
