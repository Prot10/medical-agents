"""Composite reward function — combines all 6 components with dynamic scheduling."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from neuroagent_schemas import GroundTruth, NeuroBenchCase

from ...agent.reasoning import AgentTrace
from .clinical_reward import ClinicalReward, ClinicalScores
from .compliance_reward import ComplianceReward
from .cost_reward import CostReward
from .format_reward import FormatReward

logger = logging.getLogger(__name__)


@dataclass
class RewardWeights:
    """Weights for each reward component."""

    correctness: float = 0.30
    actions: float = 0.20
    safety: float = 0.20
    cost: float = 0.15
    compliance: float = 0.10
    format: float = 0.05

    def validate(self) -> None:
        total = (
            self.correctness + self.actions + self.safety
            + self.cost + self.compliance + self.format
        )
        if abs(total - 1.0) > 0.01:
            logger.warning("Reward weights sum to %.3f (expected 1.0)", total)


@dataclass
class RewardBreakdown:
    """Detailed breakdown of all reward components."""

    correctness: float = 0.0
    actions: float = 0.0
    safety: float = 0.0
    cost: float = 0.0
    compliance: float = 0.0
    format: float = 0.0
    composite: float = 0.0
    weights_used: dict[str, float] = field(default_factory=dict)
    total_cost_usd: float = 0.0


class DynamicSchedule:
    """Reward weight schedule that changes across training epochs."""

    def __init__(self, schedule: list[dict[str, Any]]):
        self.phases = schedule

    def get_weights(self, epoch: int) -> RewardWeights:
        """Return weights for the given epoch."""
        for phase in self.phases:
            if phase["epoch_start"] <= epoch <= phase["epoch_end"]:
                return RewardWeights(**phase["weights"])
        # Fall back to last phase
        if self.phases:
            return RewardWeights(**self.phases[-1]["weights"])
        return RewardWeights()

    @classmethod
    def from_yaml(cls, config_path: str) -> DynamicSchedule:
        path = Path(config_path)
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(data.get("dynamic_schedule", []))


class CompositeReward:
    """Multi-objective reward function for GRPO training.

    Combines 6 components:
    - correctness: Diagnosis accuracy (top-1/top-3)
    - actions: Tool selection precision & recall vs ground truth
    - safety: Critical actions hit, contraindicated actions penalized
    - cost: Cost efficiency (penalize unnecessary expensive tests)
    - compliance: Hospital protocol adherence
    - format: Tool-call syntax and assessment structure

    Supports dynamic reward scheduling across training epochs.
    """

    def __init__(
        self,
        weights: RewardWeights | None = None,
        dynamic_schedule: DynamicSchedule | None = None,
        tool_costs_path: str | None = None,
        rules_dir: str = "config/hospital_rules",
        hospital: str = "us_mayo",
    ):
        self.static_weights = weights or RewardWeights()
        self.dynamic_schedule = dynamic_schedule
        self.clinical = ClinicalReward()
        self.cost_reward = CostReward(config_path=tool_costs_path)
        self.compliance = ComplianceReward(rules_dir=rules_dir, hospital=hospital)
        self.format_reward = FormatReward()

    @classmethod
    def from_config(
        cls,
        reward_config_path: str,
        tool_costs_path: str | None = None,
        rules_dir: str = "config/hospital_rules",
        hospital: str = "us_mayo",
    ) -> CompositeReward:
        """Create from YAML config files."""
        path = Path(reward_config_path)
        with open(path) as f:
            data = yaml.safe_load(f)

        static = RewardWeights(**data.get("default_weights", {}))
        schedule = None
        if "dynamic_schedule" in data:
            schedule = DynamicSchedule(data["dynamic_schedule"])

        return cls(
            weights=static,
            dynamic_schedule=schedule,
            tool_costs_path=tool_costs_path,
            rules_dir=rules_dir,
            hospital=hospital,
        )

    def compute(
        self,
        trace: AgentTrace,
        case: NeuroBenchCase,
        epoch: int | None = None,
    ) -> float:
        """Compute composite reward for a trajectory.

        Args:
            trace: Agent execution trace.
            case: Full NeuroBench case with ground truth.
            epoch: Current training epoch (for dynamic scheduling).

        Returns:
            Scalar reward in [-1, 1].
        """
        return self.compute_with_breakdown(trace, case, epoch).composite

    def compute_with_breakdown(
        self,
        trace: AgentTrace,
        case: NeuroBenchCase,
        epoch: int | None = None,
    ) -> RewardBreakdown:
        """Compute reward with full breakdown of all components.

        Args:
            trace: Agent execution trace.
            case: Full NeuroBench case with ground truth.
            epoch: Current training epoch (for dynamic scheduling).

        Returns:
            RewardBreakdown with per-component scores and composite.
        """
        gt = case.ground_truth
        weights = self._get_weights(epoch)

        # 1. Clinical rewards (correctness, actions, safety)
        clinical = self.clinical.compute(trace, gt)

        # 2. Cost reward
        optimal_tools = {
            s.tool_name for s in gt.optimal_actions if s.tool_name
        }
        r_cost = self.cost_reward.compute(trace.tools_called, optimal_tools)
        total_usd = self.cost_reward.total_cost_usd(trace.tools_called)

        # 3. Compliance reward
        r_compliance = self.compliance.compute(
            trace.tools_called, case.condition.value
        )

        # 4. Format reward
        r_format = self.format_reward.compute(
            trace.tools_called, trace.final_response
        )

        # Composite: weighted sum, then clamp to [-1, 1]
        composite = (
            weights.correctness * clinical.correctness
            + weights.actions * clinical.actions
            + weights.safety * clinical.safety
            + weights.cost * r_cost
            + weights.compliance * r_compliance
            + weights.format * r_format
        )
        composite = max(-1.0, min(1.0, composite))

        return RewardBreakdown(
            correctness=clinical.correctness,
            actions=clinical.actions,
            safety=clinical.safety,
            cost=r_cost,
            compliance=r_compliance,
            format=r_format,
            composite=composite,
            weights_used={
                "correctness": weights.correctness,
                "actions": weights.actions,
                "safety": weights.safety,
                "cost": weights.cost,
                "compliance": weights.compliance,
                "format": weights.format,
            },
            total_cost_usd=total_usd,
        )

    def _get_weights(self, epoch: int | None) -> RewardWeights:
        """Get weights for the current epoch."""
        if epoch is not None and self.dynamic_schedule is not None:
            return self.dynamic_schedule.get_weights(epoch)
        return self.static_weights

    def batch_compute(
        self,
        traces: list[AgentTrace],
        cases: list[NeuroBenchCase],
        epoch: int | None = None,
    ) -> list[float]:
        """Compute rewards for a batch of trajectories.

        Args:
            traces: List of agent traces.
            cases: Corresponding NeuroBench cases.
            epoch: Current training epoch.

        Returns:
            List of scalar rewards.
        """
        return [
            self.compute(trace, case, epoch)
            for trace, case in zip(traces, cases)
        ]
