"""Reward computed only from typed clinical actions and physician-authored policy criteria."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from neuroagent_schemas import (
    ActionImportance,
    ActionRejected,
    AvoidanceSeverity,
    ClinicalEpisode,
    NeuroBenchCase,
    PolicyReviewStatus,
    SequenceSeverity,
)


class RewardBreakdown(BaseModel):
    model_config = ConfigDict(extra="forbid")
    diagnosis: float = Field(ge=0, le=1)
    required_action_coverage: float = Field(ge=0, le=1)
    recommended_action_coverage: float = Field(ge=0, le=1)
    tool_accuracy: float = Field(ge=0, le=1)
    safety: float = Field(ge=0, le=1)
    waste_avoidance: float = Field(ge=0, le=1)
    sequence: float = Field(ge=0, le=1)
    stopping: float = Field(ge=0, le=1)
    assessment: float = Field(ge=0, le=1)
    cost_efficiency: float = Field(ge=0, le=1)
    token_efficiency: float = Field(ge=0, le=1)
    invalid_actions: int = Field(ge=0)
    scalar: float = Field(ge=0, le=1)
    caps_applied: list[str] = Field(default_factory=list)


class ClinicalPolicyReward:
    scorer_id = "clinical-policy-v1"

    def __init__(self, *, require_approved: bool = True) -> None:
        self.require_approved = require_approved

    def score(self, episode: ClinicalEpisode, case: NeuroBenchCase) -> RewardBreakdown:
        policy = case.ground_truth
        if self.require_approved and policy.review_status is not PolicyReviewStatus.APPROVED:
            raise ValueError(
                f"case {case.case_id} policy is {policy.review_status.value}; only approved policies are scoreable"
            )

        actions = episode.tool_actions
        assessment = episode.assessment
        diagnosis = float(bool(assessment and policy.diagnosis.matches(assessment.primary_diagnosis)))

        matched: dict[str, list[int]] = {
            criterion.criterion_id: [
                index for index, action in enumerate(actions) if criterion.matches(action)
            ]
            for criterion in policy.action_criteria
        }
        required = [
            criterion for criterion in policy.action_criteria
            if criterion.importance is ActionImportance.REQUIRED
        ]
        recommended = [
            criterion for criterion in policy.action_criteria
            if criterion.importance is ActionImportance.RECOMMENDED
        ]
        required_coverage = _coverage(required, matched)
        recommended_coverage = _coverage(recommended, matched)

        positive = [
            any(criterion.matches(action) for criterion in policy.action_criteria)
            for action in actions
        ]
        tool_accuracy = sum(positive) / len(positive) if positive else 1.0

        avoided_hits = [
            criterion
            for criterion in policy.avoided_actions
            for action in actions
            if criterion.matches(action)
        ]
        harmful = sum(
            item.severity in {AvoidanceSeverity.HARM, AvoidanceSeverity.CONTRAINDICATED}
            for item in avoided_hits
        )
        waste = sum(item.severity is AvoidanceSeverity.WASTE for item in avoided_hits)
        safety = max(0.0, 1.0 - harmful / max(1, len(actions)))
        waste_avoidance = max(0.0, 1.0 - waste / max(1, len(actions)))

        sequence_violations = []
        for constraint in policy.sequence_constraints:
            before = matched[constraint.before_criterion_id]
            after = matched[constraint.after_criterion_id]
            if after and (not before or min(before) >= min(after)):
                sequence_violations.append(constraint)
        sequence = (
            1.0 - len(sequence_violations) / len(policy.sequence_constraints)
            if policy.sequence_constraints else 1.0
        )

        required_stop = policy.stop_rule.required_before_assessment
        if all(matched[item] for item in required_stop):
            completion_index = max((min(matched[item]) for item in required_stop), default=-1)
            extra = max(0, len(actions) - completion_index - 1)
            allowed = policy.stop_rule.max_additional_actions
            stopping = 1.0 if extra <= allowed else 1.0 / (1.0 + extra - allowed)
        else:
            stopping = 0.0

        assessment_score = _assessment_score(assessment, policy.assessment)
        efficiency_gate = diagnosis * required_coverage
        cost_efficiency = efficiency_gate * (1.0 / (1.0 + episode.total_cost_usd / 1000.0))
        token_efficiency = efficiency_gate * (1.0 / (1.0 + episode.total_tokens / 4096.0))
        invalid = sum(isinstance(event, ActionRejected) for event in episode.events)

        scalar = (
            0.25 * diagnosis
            + 0.18 * required_coverage
            + 0.05 * recommended_coverage
            + 0.10 * tool_accuracy
            + 0.12 * safety
            + 0.07 * waste_avoidance
            + 0.06 * sequence
            + 0.05 * stopping
            + 0.05 * assessment_score
            + 0.04 * cost_efficiency
            + 0.03 * token_efficiency
        )
        scalar *= 1.0 / (1.0 + 0.1 * invalid)
        caps = []
        if any(item.severity is AvoidanceSeverity.CONTRAINDICATED for item in avoided_hits):
            scalar = min(scalar, 0.10)
            caps.append("contraindicated_action")
        elif any(item.severity is AvoidanceSeverity.HARM for item in avoided_hits):
            scalar = min(scalar, 0.35)
            caps.append("harmful_action")
        if any(item.severity is SequenceSeverity.HARD for item in sequence_violations):
            scalar = min(scalar, 0.50)
            caps.append("hard_sequence_violation")
        return RewardBreakdown(
            diagnosis=diagnosis,
            required_action_coverage=required_coverage,
            recommended_action_coverage=recommended_coverage,
            tool_accuracy=tool_accuracy,
            safety=safety,
            waste_avoidance=waste_avoidance,
            sequence=sequence,
            stopping=stopping,
            assessment=assessment_score,
            cost_efficiency=cost_efficiency,
            token_efficiency=token_efficiency,
            invalid_actions=invalid,
            scalar=max(0.0, min(1.0, scalar)),
            caps_applied=caps,
        )


def _coverage(criteria, matched: dict[str, list[int]]) -> float:
    if not criteria:
        return 1.0
    return sum(bool(matched[item.criterion_id]) for item in criteria) / len(criteria)


def _assessment_score(assessment, criteria) -> float:
    if assessment is None:
        return 0.0
    recommendations = [item.casefold() for item in assessment.recommendations]
    required = [
        any(expected.casefold() in actual for actual in recommendations)
        for expected in criteria.required_recommendations
    ]
    prohibited = [
        any(forbidden.casefold() in actual for actual in recommendations)
        for forbidden in criteria.prohibited_recommendations
    ]
    required_score = sum(required) / len(required) if required else 1.0
    prohibited_score = 1.0 - (sum(prohibited) / len(prohibited) if prohibited else 0.0)
    return 0.5 * required_score + 0.5 * prohibited_score
