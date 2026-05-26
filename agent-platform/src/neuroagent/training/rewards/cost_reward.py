"""Cost-aware reward — penalizes unnecessary expensive diagnostic tests.

Supports two modes:
1. Flat costs: Simple per-tool-name costs (backward compatible).
2. Parameter-aware costs: Uses CostTracker for accurate Medicare PFS rates
   that vary by tool parameters (e.g., lab panels, imaging modifiers).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# Default USD costs if config file not found (Medicare reference rates)
DEFAULT_TOOL_COSTS: dict[str, float] = {
    "analyze_brain_mri": 320,
    "analyze_eeg": 250,
    "analyze_csf": 250,
    "analyze_ecg": 20,
    "interpret_labs": 25,
    "order_ct_scan": 200,
    "order_echocardiogram": 300,
    "order_cardiac_monitoring": 150,
    "order_advanced_imaging": 2000,
    "order_specialized_test": 600,
    "search_medical_literature": 0,
    "check_drug_interactions": 0,
    "consult_medical_specialist": 75,
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
    # When the caller supplies the per-case useless_tools / harmful_tools sets
    # from GroundTruth, the "unnecessary" bucket can be split further. This
    # matters for training reward shaping: harmful calls deserve a strictly
    # larger penalty than useless ones.
    useless_calls: list[str] = field(default_factory=list)
    useless_cost: float = 0.0
    harmful_calls: list[str] = field(default_factory=list)
    harmful_cost: float = 0.0


class CostReward:
    """Reward efficient tool use by penalizing unnecessary expensive tests.

    Key design: missing a needed test is penalized less (0.5x) than ordering
    an unnecessary one, because over-testing is a cost problem while
    under-testing is caught by the safety reward.

    When ``cost_tracker`` is provided, costs are computed using parameter-aware
    Medicare PFS rates (e.g., MRI with contrast costs more than without).
    Otherwise falls back to flat per-tool costs.
    """

    def __init__(
        self,
        tool_costs: dict[str, float] | None = None,
        config_path: str | None = None,
        missing_penalty_weight: float = 0.5,
        cost_tracker: Any | None = None,
    ):
        self.missing_penalty_weight = missing_penalty_weight
        self._cost_tracker = cost_tracker

        if tool_costs is not None:
            self.tool_costs = tool_costs
        elif config_path is not None:
            self.tool_costs = self._load_costs(config_path)
        else:
            self.tool_costs = DEFAULT_TOOL_COSTS.copy()

    @staticmethod
    def _load_costs(config_path: str) -> dict[str, float]:
        path = Path(config_path)
        if not path.exists():
            return DEFAULT_TOOL_COSTS.copy()
        with open(path) as f:
            data = yaml.safe_load(f)
        return data.get("tool_costs", DEFAULT_TOOL_COSTS.copy())

    def _get_cost(self, tool_name: str, parameters: dict[str, Any] | None = None) -> float:
        """Get cost for a tool call, using CostTracker if available."""
        if self._cost_tracker is not None and parameters is not None:
            entry = self._cost_tracker.compute_cost(tool_name, parameters)
            return entry.cost_usd
        return self.tool_costs.get(tool_name, 0)

    def compute(
        self,
        agent_tools: list[str],
        optimal_tools: set[str],
    ) -> float:
        """Compute cost reward in [0, 1] using flat costs.

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

    def compute_parameter_aware(
        self,
        agent_tool_calls: list[dict[str, Any]],
        optimal_actions: list[dict[str, Any]],
    ) -> float:
        """Compute cost reward using parameter-aware costs.

        Uses CostTracker for accurate Medicare PFS rates that depend on tool
        parameters (e.g., lab panels, imaging modifiers, CSF special tests).

        Args:
            agent_tool_calls: List of {"tool_name": str, "parameters": dict}.
            optimal_actions: Ground truth optimal_actions from NeuroBench case,
                each with "tool_name", "tool_parameters", and "category".

        Returns:
            Cost efficiency reward in [0, 1].
        """
        if self._cost_tracker is None:
            # Fall back to flat-cost computation
            agent_names = [tc["tool_name"] for tc in agent_tool_calls]
            optimal_names = {
                a["tool_name"]
                for a in optimal_actions
                if a.get("tool_name")
            }
            return self.compute(agent_names, optimal_names)

        # Reset tracker for clean computation
        self._cost_tracker.reset()

        # Compute actual cost from agent's tool calls
        agent_total = 0.0
        agent_tool_names = set()
        for tc in agent_tool_calls:
            entry = self._cost_tracker.compute_cost(
                tc["tool_name"], tc.get("parameters", {})
            )
            agent_total += entry.cost_usd
            agent_tool_names.add(tc["tool_name"])

        # Compute optimal cost from ground truth actions
        self._cost_tracker.reset()
        optimal_total = 0.0
        optimal_tool_names = set()
        for action in optimal_actions:
            tool_name = action.get("tool_name")
            if not tool_name:
                continue
            optimal_tool_names.add(tool_name)
            params = action.get("tool_parameters", {})
            entry = self._cost_tracker.compute_cost(tool_name, params)
            optimal_total += entry.cost_usd

        # Compute wasted cost (tools called but not in optimal set)
        self._cost_tracker.reset()
        wasted = 0.0
        for tc in agent_tool_calls:
            if tc["tool_name"] not in optimal_tool_names:
                entry = self._cost_tracker.compute_cost(
                    tc["tool_name"], tc.get("parameters", {})
                )
                wasted += entry.cost_usd

        # Compute missed cost (optimal tools not called)
        self._cost_tracker.reset()
        missed = 0.0
        for action in optimal_actions:
            tool_name = action.get("tool_name")
            if tool_name and tool_name not in agent_tool_names:
                params = action.get("tool_parameters", {})
                entry = self._cost_tracker.compute_cost(tool_name, params)
                missed += entry.cost_usd

        if optimal_total == 0:
            return 1.0 if agent_total == 0 else 0.0

        penalty = wasted + missed * self.missing_penalty_weight
        efficiency = max(0.0, 1.0 - penalty / (optimal_total + 1))
        return efficiency

    def breakdown(
        self,
        agent_tools: list[str],
        optimal_tools: set[str],
        useless_tools: set[str] | None = None,
        harmful_tools: set[str] | None = None,
    ) -> CostBreakdown:
        """Get detailed cost breakdown using flat costs.

        When ``useless_tools`` / ``harmful_tools`` are provided (from the v5
        gold-trajectory regen schema), the breakdown additionally splits the
        "unnecessary" bucket into ``useless_*`` and ``harmful_*`` fields.
        These do not change the legacy fields — they only annotate.
        """
        agent_set = set(agent_tools)
        unnecessary = [t for t in agent_set if t not in optimal_tools]
        missing = [t for t in optimal_tools if t not in agent_set]

        useless_called: list[str] = []
        harmful_called: list[str] = []
        if useless_tools:
            useless_called = [t for t in agent_set if t in useless_tools]
        if harmful_tools:
            harmful_called = [t for t in agent_set if t in harmful_tools]

        return CostBreakdown(
            total_cost=sum(self.tool_costs.get(t, 0) for t in agent_set),
            optimal_cost=sum(self.tool_costs.get(t, 0) for t in optimal_tools),
            wasted_cost=sum(self.tool_costs.get(t, 0) for t in unnecessary),
            missed_cost=sum(self.tool_costs.get(t, 0) for t in missing),
            unnecessary_tools=unnecessary,
            missing_tools=missing,
            useless_calls=useless_called,
            useless_cost=sum(self.tool_costs.get(t, 0) for t in useless_called),
            harmful_calls=harmful_called,
            harmful_cost=sum(self.tool_costs.get(t, 0) for t in harmful_called),
        )

    def total_cost_usd(self, agent_tools: list[str]) -> float:
        """Return total USD cost of tools called (flat costs)."""
        return sum(self.tool_costs.get(t, 0) for t in set(agent_tools))
