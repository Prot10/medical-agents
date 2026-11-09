"""Outcome reward: the comparison arm of E1, which sees the diagnosis and the bill and nothing else.

R = (1 - w) * D + w * (1 - min(1, cost / B)), with D the diagnosis component of the policy scorer
(scorer v2: the asserted label against the accepted labels), cost the episode's total in USD and B a
budget frozen before training (the 95th percentile of the base model's rollout cost on the training
cases). The default w = 0.15 is the form proposed in the tracker (decision D6); w = 0 is the
diagnosis-only option.

The scalar reads no action criterion, avoided action, sequence constraint or stop rule: the arm must
learn its work-up from the outcome alone, so that E1 compares two training signals and not two
amounts of physician knowledge. The breakdown it returns still carries every policy component,
computed by `ClinicalPolicyReward`, for logging and analysis only; `test_outcome_reward.py` checks
that changing the policy's process criteria never moves the scalar.
"""

from __future__ import annotations

from neuroagent_schemas import ClinicalEpisode, NeuroBenchCase

from .policy_reward import ClinicalPolicyReward, RewardBreakdown


class OutcomeReward:
    scorer_id = "outcome-v1"

    def __init__(self, *, budget_usd: float, cost_weight: float = 0.15, require_approved: bool = True) -> None:
        if budget_usd <= 0:
            raise ValueError("the outcome budget B must be positive")
        if not 0.0 <= cost_weight < 1.0:
            raise ValueError("the cost weight must be in [0, 1)")
        self.budget_usd = budget_usd
        self.cost_weight = cost_weight
        self._policy = ClinicalPolicyReward(require_approved=require_approved)

    def score(self, episode: ClinicalEpisode, case: NeuroBenchCase) -> RewardBreakdown:
        breakdown = self._policy.score(episode, case)
        diagnosis = float(bool(episode.assessment and case.ground_truth.diagnosis.matches(episode.assessment.primary_diagnosis)))
        frugality = 1.0 - min(1.0, episode.total_cost_usd / self.budget_usd)
        scalar = (1.0 - self.cost_weight) * diagnosis + self.cost_weight * frugality
        # The safety caps belong to the policy reward: none is applied to the outcome.
        return breakdown.model_copy(update={"scalar": scalar, "caps_applied": []})
