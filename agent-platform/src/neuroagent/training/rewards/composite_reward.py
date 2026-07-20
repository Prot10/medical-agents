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
        safety_gate: bool = False,
        safety_gate_cap: float = 0.0,
        cost_requires_workup: float | None = None,
    ):
        self.static_weights = weights or RewardWeights()
        self.dynamic_schedule = dynamic_schedule
        self.clinical = ClinicalReward()
        self.cost_reward = CostReward(config_path=tool_costs_path)
        self.compliance = ComplianceReward(rules_dir=rules_dir, hospital=hospital)
        self.format_reward = FormatReward()
        # Non-compensatory safety gate: when on, a trajectory that takes a contraindicated
        # (harmful) action has its composite hard-capped at `safety_gate_cap`, so no amount of
        # good format/cost/tool-selection can buy back a clinically unsafe decision. This
        # matches the LLM-judge's safety veto and the SaFeR-VLM recommendation against pure
        # weighted-sum aggregation for safety-critical axes.
        self.safety_gate = safety_gate
        self.safety_gate_cap = safety_gate_cap
        # Cost credit is dangerous on its own: rewarding low cost directly rewards
        # UNDER-ordering, and "order nothing" is the cheapest path of all. When this is set,
        # the cost component only counts once the required workup is actually ordered
        # (critical_actions_hit >= threshold); below that, cost contributes 0, so skimping on
        # the workup can never be bought back with a cost bonus. This is the single-turn
        # analogue of "cost conditional on correctness" (correctness needs a diagnosis the
        # one-shot rollout never reaches; critical_actions_hit is the signal that exists).
        self.cost_requires_workup = cost_requires_workup

    @classmethod
    def from_config(
        cls,
        reward_config_path: str,
        tool_costs_path: str | None = None,
        rules_dir: str = "config/hospital_rules",
        hospital: str = "us_mayo",
    ) -> CompositeReward:
        """Create from YAML config files.

        Recognised top-level keys:
          default_weights    — the static component weights (required)
          dynamic_schedule   — optional epoch-keyed weight curriculum. NOTE: this only
                               advances across epochs, so a 1-epoch RL run is pinned to
                               phase 1 forever; leave it out for GRPO.
          safety_gate        — {enabled: bool, cap: float} non-compensatory safety cap
          cost_requires_workup — float threshold; cost only counts once critical_actions_hit
                               reaches it (guards against rewarding under-ordering)
        """
        path = Path(reward_config_path)
        with open(path) as f:
            data = yaml.safe_load(f)

        static = RewardWeights(**data.get("default_weights", {}))
        schedule = None
        if "dynamic_schedule" in data:
            schedule = DynamicSchedule(data["dynamic_schedule"])

        gate = data.get("safety_gate", {}) or {}
        return cls(
            weights=static,
            dynamic_schedule=schedule,
            tool_costs_path=tool_costs_path,
            rules_dir=rules_dir,
            hospital=hospital,
            safety_gate=bool(gate.get("enabled", False)),
            safety_gate_cap=float(gate.get("cap", 0.0)),
            cost_requires_workup=data.get("cost_requires_workup"),
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

        # 2. Cost reward — gated on workup completeness so it can never reward under-ordering.
        optimal_tools = {
            s.tool_name for s in gt.optimal_actions if s.tool_name
        }
        r_cost = self.cost_reward.compute(trace.tools_called, optimal_tools)
        total_usd = self.cost_reward.total_cost_usd(trace.tools_called)
        if (
            self.cost_requires_workup is not None
            and clinical.critical_actions_hit < self.cost_requires_workup
        ):
            # Required workup not ordered yet — being cheap is not a virtue here.
            r_cost = 0.0

        # 3. Compliance reward — None when no pathway covers this condition.
        r_compliance = self.compliance.compute(
            trace.tools_called, case.condition.value
        )

        # 4. Format reward
        r_format = self.format_reward.compute(
            trace.tools_called, trace.final_response
        )

        # Composite: weighted sum. Compliance is unmeasurable (no pathway) for most
        # conditions; when it is, its weight is redistributed proportionally across the
        # live components rather than contributing a constant. A constant compliance term
        # is invisible to a group-relative advantage (dead gradient within a condition)
        # yet distorts comparisons across conditions, so "no pathway" must be reward-neutral,
        # not a free +weight. With compliance present this is the original plain weighted
        # sum, unchanged.
        base_sum = (
            weights.correctness * clinical.correctness
            + weights.actions * clinical.actions
            + weights.safety * clinical.safety
            + weights.cost * r_cost
            + weights.format * r_format
        )
        if r_compliance is not None:
            composite = base_sum + weights.compliance * r_compliance
            compliance_weight_used = weights.compliance
        else:
            live_weight = (
                weights.correctness + weights.actions + weights.safety
                + weights.cost + weights.format
            )
            # Scale the live components up to reclaim the compliance mass.
            composite = (
                base_sum * (live_weight + weights.compliance) / live_weight
                if live_weight > 0 else base_sum
            )
            compliance_weight_used = 0.0
        composite = max(-1.0, min(1.0, composite))

        # Non-compensatory safety gate (applied AFTER the sum): a contraindicated action
        # hard-caps the composite, so an unsafe trajectory can never outscore a safe one on
        # the strength of format/cost/tool-selection.
        if self.safety_gate and clinical.contraindicated_actions_taken > 0:
            composite = min(composite, self.safety_gate_cap)

        return RewardBreakdown(
            correctness=clinical.correctness,
            actions=clinical.actions,
            safety=clinical.safety,
            cost=r_cost,
            compliance=r_compliance if r_compliance is not None else 0.0,
            format=r_format,
            composite=composite,
            weights_used={
                "correctness": weights.correctness,
                "actions": weights.actions,
                "safety": weights.safety,
                "cost": weights.cost,
                "compliance": compliance_weight_used,
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
