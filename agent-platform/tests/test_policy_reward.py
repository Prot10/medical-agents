from __future__ import annotations

from pathlib import Path

from neuroagent.evaluation import ClinicalPolicyReward
from neuroagent_schemas import (
    ActionProposed,
    AssessmentSubmitted,
    ClinicalEpisode,
    ObservationReceived,
    PolicyReviewStatus,
    SubmitAssessment,
    ToolAction,
    NeuroBenchCase,
)


ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = ROOT / "data/neurobench/cases/SE-M02.json"


def approved_case() -> NeuroBenchCase:
    case = NeuroBenchCase.model_validate_json(CASE_PATH.read_text())
    return case.model_copy(
        update={
            "ground_truth": case.ground_truth.model_copy(
                update={"review_status": PolicyReviewStatus.APPROVED}
            )
        }
    )


def make_episode(case, *, add_waste=False):
    required = [
        criterion
        for criterion in case.ground_truth.action_criteria
        if criterion.importance.value == "required"
    ]
    actions = [
        ToolAction(
            tool_name=criterion.alternatives[0].tool_name,
            arguments=criterion.alternatives[0].required_arguments,
        )
        for criterion in required
    ]
    if add_waste:
        avoided = next(
            (
                criterion
                for criterion in case.ground_truth.avoided_actions
                if criterion.severity.value == "waste"
            ),
            None,
        )
        if avoided is None:
            return None
        actions.append(
            ToolAction(
                tool_name=avoided.alternatives[0].tool_name,
                arguments=avoided.alternatives[0].required_arguments,
            )
        )
    assessment = SubmitAssessment(
        primary_diagnosis=case.ground_truth.diagnosis.accepted[0],
        confidence=0.9,
        urgency="emergent",
        recommendations=case.ground_truth.assessment.required_recommendations,
    )
    events = []
    for turn, action in enumerate(actions, 1):
        events.extend(
            [
                ActionProposed(turn=turn, action=action),
                ObservationReceived(
                    turn=turn,
                    tool_name=action.tool_name,
                    success=True,
                    output={},
                    cost_usd=100.0,
                ),
            ]
        )
    turn = len(actions) + 1
    events.extend(
        [
            ActionProposed(turn=turn, action=assessment),
            AssessmentSubmitted(turn=turn, assessment=assessment),
        ]
    )
    return ClinicalEpisode(events=events)


def test_only_approved_policy_is_scoreable_by_default():
    case = NeuroBenchCase.model_validate_json(CASE_PATH.read_text())
    episode = make_episode(approved_case())
    try:
        ClinicalPolicyReward().score(episode, case)
    except ValueError as exc:
        assert "only approved policies" in str(exc)
    else:
        raise AssertionError("draft policy was scored")


def test_correct_diagnosis_and_required_actions_unlock_efficiency():
    case = approved_case()
    score = ClinicalPolicyReward().score(make_episode(case), case)
    assert score.diagnosis == 1
    assert score.required_action_coverage == 1
    assert score.cost_efficiency > 0
    assert 0 <= score.scalar <= 1


def test_waste_can_never_increase_reward():
    case = approved_case()
    baseline = make_episode(case)
    with_waste = make_episode(case, add_waste=True)
    if with_waste is None:
        return
    scorer = ClinicalPolicyReward()
    assert scorer.score(with_waste, case).scalar <= scorer.score(baseline, case).scalar


def test_equivalent_action_alternatives_receive_equal_coverage():
    case = approved_case()
    criterion = next(
        (item for item in case.ground_truth.action_criteria if len(item.alternatives) > 1),
        None,
    )
    if criterion is None:
        return
    a = ToolAction(
        tool_name=criterion.alternatives[0].tool_name,
        arguments=criterion.alternatives[0].required_arguments,
    )
    b = ToolAction(
        tool_name=criterion.alternatives[1].tool_name,
        arguments=criterion.alternatives[1].required_arguments,
    )
    assert criterion.matches(a)
    assert criterion.matches(b)
