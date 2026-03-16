"""Cost-aware reward — penalizes unnecessary expensive diagnostic tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# Default USD costs if config file not found
DEFAULT_TOOL_COSTS: dict[str, float] = {
    "analyze_brain_mri": 2500,
    "analyze_eeg": 800,
    "analyze_csf": 1500,
    "analyze_ecg": 150,
    "interpret_labs": 300,
    "search_medical_literature": 0,
    "check_drug_interactions": 0,
}


@dataclass
class CostBreakdown:
    """Detailed cost analysis for a trajectory."""

    total_cost: float = 0.0
    optimal_cost: float = 0.0
    wasted_cost: float = 0.0
    missed_cost: float = 0.0
    unnecessary_tools: list[str] = field(default_factory=list)
    missing_tools: list[str] = field(default_factory=list)


class CostReward:
    """Reward efficient tool use by penalizing unnecessary expensive tests.

    Key design: missing a needed test is penalized less (0.5x) than ordering
    an unnecessary one, because over-testing is a cost problem while
    under-testing is caught by the safety reward.
    """

    def __init__(
        self,
        tool_costs: dict[str, float] | None = None,
        config_path: str | None = None,
        missing_penalty_weight: float = 0.5,
    ):
        if tool_costs is not None:
            self.tool_costs = tool_costs
        elif config_path is not None:
            self.tool_costs = self._load_costs(config_path)
        else:
            self.tool_costs = DEFAULT_TOOL_COSTS.copy()
        self.missing_penalty_weight = missing_penalty_weight

    @staticmethod
    def _load_costs(config_path: str) -> dict[str, float]:
        path = Path(config_path)
        if not path.exists():
            return DEFAULT_TOOL_COSTS.copy()
        with open(path) as f:
            data = yaml.safe_load(f)
        return data.get("tool_costs", DEFAULT_TOOL_COSTS.copy())

    def compute(
        self,
        agent_tools: list[str],
        optimal_tools: set[str],
    ) -> float:
        """Compute cost reward in [0, 1].

        Args:
            agent_tools: Tools the agent actually called (may have duplicates).
            optimal_tools: Ground-truth optimal tool set from NeuroBench case.

        Returns:
            1.0 when agent matches optimal exactly, lower with waste.
        """
        breakdown = self.breakdown(agent_tools, optimal_tools)

        optimal_cost = breakdown.optimal_cost
        if optimal_cost == 0:
            return 1.0 if breakdown.total_cost == 0 else 0.0

        penalty = breakdown.wasted_cost + breakdown.missed_cost * self.missing_penalty_weight
        efficiency = max(0.0, 1.0 - penalty / (optimal_cost + 1))
        return efficiency

    def breakdown(
        self,
        agent_tools: list[str],
        optimal_tools: set[str],
    ) -> CostBreakdown:
        """Get detailed cost breakdown."""
        agent_set = set(agent_tools)
        unnecessary = [t for t in agent_set if t not in optimal_tools]
        missing = [t for t in optimal_tools if t not in agent_set]

        return CostBreakdown(
            total_cost=sum(self.tool_costs.get(t, 0) for t in agent_set),
            optimal_cost=sum(self.tool_costs.get(t, 0) for t in optimal_tools),
            wasted_cost=sum(self.tool_costs.get(t, 0) for t in unnecessary),
            missed_cost=sum(self.tool_costs.get(t, 0) for t in missing),
            unnecessary_tools=unnecessary,
            missing_tools=missing,
        )

    def total_cost_usd(self, agent_tools: list[str]) -> float:
        """Return total USD cost of tools called."""
        return sum(self.tool_costs.get(t, 0) for t in set(agent_tools))
