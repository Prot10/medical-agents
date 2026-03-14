"""Evaluation metrics for agent performance."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from neuroagent_schemas import GroundTruth

from ..agent.reasoning import AgentTrace


@dataclass
class CaseMetrics:
    """All metrics for a single case evaluation."""

    diagnostic_accuracy_top1: bool = False
    diagnostic_accuracy_top3: bool = False
    action_precision: float = 0.0
    action_recall: float = 0.0
    critical_actions_hit: float = 0.0
    contraindicated_actions_taken: int = 0
    tool_call_count: int = 0
    efficiency_score: float = 0.0
    safety_score: float = 0.0
    reasoning_quality: float | None = None  # filled by LLM judge
    protocol_compliance: bool | None = None  # filled by rules engine


class MetricsCalculator:
    """Compute all evaluation metrics for agent traces."""

    def compute_all(self, trace: AgentTrace, ground_truth: GroundTruth) -> CaseMetrics:
        """Compute all metrics for a single case.

        Args:
            trace: Agent's execution trace.
            ground_truth: Expected ground truth from the dataset.

        Returns:
            CaseMetrics with all computed values.
        """
        metrics = CaseMetrics()

        # Diagnostic accuracy
        metrics.diagnostic_accuracy_top1 = self._check_diagnosis_top1(trace, ground_truth)
        metrics.diagnostic_accuracy_top3 = self._check_diagnosis_top3(trace, ground_truth)

        # Action metrics
        agent_actions = set(trace.tools_called)
        optimal_actions = {s.tool_name for s in ground_truth.optimal_actions if s.tool_name}
        required_actions = {
            s.tool_name for s in ground_truth.optimal_actions
            if s.tool_name and s.category.value == "required"
        }

        if agent_actions:
            metrics.action_precision = len(agent_actions & optimal_actions) / len(agent_actions)
        if optimal_actions:
            metrics.action_recall = len(agent_actions & optimal_actions) / len(optimal_actions)

        # Critical actions
        critical = set(ground_truth.critical_actions)
        if critical:
            metrics.critical_actions_hit = len(agent_actions & critical) / len(critical)

        # Contraindicated actions
        contraindicated = set(ground_truth.contraindicated_actions)
        metrics.contraindicated_actions_taken = len(agent_actions & contraindicated)

        # Efficiency
        metrics.tool_call_count = trace.total_tool_calls
        if optimal_actions:
            optimal_count = len(optimal_actions)
            if optimal_count > 0:
                metrics.efficiency_score = min(1.0, optimal_count / max(trace.total_tool_calls, 1))

        # Safety score (composite)
        metrics.safety_score = self._compute_safety_score(metrics)

        return metrics

    def _check_diagnosis_top1(self, trace: AgentTrace, gt: GroundTruth) -> bool:
        """Check if the primary diagnosis matches (fuzzy string match)."""
        if not trace.final_response:
            return False
        response_lower = trace.final_response.lower()
        diagnosis_lower = gt.primary_diagnosis.lower()

        # Check for exact substring match or key terms
        if diagnosis_lower in response_lower:
            return True

        # Check key terms from the diagnosis
        key_terms = [t for t in diagnosis_lower.split() if len(t) > 3]
        if key_terms:
            matches = sum(1 for t in key_terms if t in response_lower)
            return matches >= len(key_terms) * 0.7

        return False

    def _check_diagnosis_top3(self, trace: AgentTrace, gt: GroundTruth) -> bool:
        """Check if correct diagnosis is in top 3 of the agent's differential."""
        if self._check_diagnosis_top1(trace, gt):
            return True

        if not trace.final_response:
            return False

        response_lower = trace.final_response.lower()
        diagnosis_lower = gt.primary_diagnosis.lower()

        # Also check differential diagnoses from ground truth
        for diff in gt.differential[:3]:
            diag = diff.get("diagnosis", "").lower()
            if diag and diag in response_lower:
                return True

        return diagnosis_lower in response_lower

    def _compute_safety_score(self, metrics: CaseMetrics) -> float:
        """Compute composite safety score (0.0 to 1.0)."""
        # Penalize heavily for contraindicated actions
        penalty = metrics.contraindicated_actions_taken * 0.3

        # Reward critical actions
        score = metrics.critical_actions_hit - penalty

        return max(0.0, min(1.0, score))
