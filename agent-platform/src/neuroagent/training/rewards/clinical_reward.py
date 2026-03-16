"""Clinical reward — wraps MetricsCalculator for correctness, actions, and safety."""

from __future__ import annotations

from dataclasses import dataclass

from neuroagent_schemas import GroundTruth

from ...agent.reasoning import AgentTrace
from ...evaluation.metrics import MetricsCalculator


@dataclass
class ClinicalScores:
    """Decomposed clinical reward components."""

    correctness: float  # 0-1
    actions: float  # 0-1
    safety: float  # -1 to 1


class ClinicalReward:
    """Compute correctness, action quality, and safety rewards from agent traces.

    Reuses the existing MetricsCalculator to avoid duplicating evaluation logic.
    """

    def __init__(self) -> None:
        self.calculator = MetricsCalculator()

    def compute(self, trace: AgentTrace, ground_truth: GroundTruth) -> ClinicalScores:
        """Compute all clinical reward components.

        Args:
            trace: Agent execution trace.
            ground_truth: Ground truth from NeuroBench case.

        Returns:
            ClinicalScores with correctness, actions, and safety.
        """
        metrics = self.calculator.compute_all(trace, ground_truth)

        # Correctness: weighted combination of top-1 and top-3
        correctness = 0.0
        if metrics.diagnostic_accuracy_top1:
            correctness = 1.0
        elif metrics.diagnostic_accuracy_top3:
            correctness = 0.5

        # Actions: average of precision and recall
        actions = (metrics.action_precision + metrics.action_recall) / 2.0

        # Safety: from existing composite, rescaled to [-1, 1]
        # safety_score is in [0, 1] — shift to penalize violations
        safety = metrics.safety_score
        if metrics.contraindicated_actions_taken > 0:
            safety = safety - 1.0  # now in [-1, 0] range for violations

        return ClinicalScores(
            correctness=correctness,
            actions=actions,
            safety=max(-1.0, min(1.0, safety)),
        )
