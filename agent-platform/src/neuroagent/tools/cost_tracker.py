"""Cost tracking for diagnostic tool calls using Medicare reference rates."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class ToolCostEntry(BaseModel):
    """Cost record for a single tool invocation."""

    tool_name: str
    parameters: dict[str, Any] = {}
    cost_usd: float
    cost_breakdown: dict[str, float] = {}


class CostTracker:
    """Compute and track costs for diagnostic tool calls.

    Loads per-tool cost rules from a YAML config.  Costs are parameter-dependent:
    e.g. MRI cost varies with contrast, labs cost varies by panels requested.
    """

    def __init__(self, config_path: str | Path | None = None):
        if config_path is None:
            config_path = Path(__file__).resolve().parents[3] / "config" / "tool_costs.yaml"
        self.config = self._load_config(Path(config_path))
        self.entries: list[ToolCostEntry] = []

    @staticmethod
    def _load_config(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return data.get("tools", {})

    def compute_cost(self, tool_name: str, parameters: dict[str, Any]) -> ToolCostEntry:
        """Compute cost for a single tool call and record it."""
        tool_cfg = self.config.get(tool_name, {})
        breakdown: dict[str, float] = {}
        total = 0.0

        if tool_name == "analyze_brain_mri":
            total, breakdown = self._cost_mri(tool_cfg, parameters)
        elif tool_name == "analyze_eeg":
            total, breakdown = self._cost_by_type(tool_cfg, parameters, "eeg_type", "routine")
        elif tool_name == "interpret_labs":
            total, breakdown = self._cost_labs(tool_cfg, parameters)
        elif tool_name == "analyze_csf":
            total, breakdown = self._cost_csf(tool_cfg, parameters)
        elif tool_name == "order_ct_scan":
            total, breakdown = self._cost_ct(tool_cfg, parameters)
        elif tool_name == "order_echocardiogram":
            total, breakdown = self._cost_by_type(tool_cfg, parameters, "echo_type", "TTE")
        elif tool_name == "order_cardiac_monitoring":
            total, breakdown = self._cost_by_type(tool_cfg, parameters, "monitor_type", "holter_24h")
        elif tool_name == "order_advanced_imaging":
            total, breakdown = self._cost_by_type(tool_cfg, parameters, "imaging_type", "FDG_PET")
        elif tool_name == "order_specialized_test":
            total, breakdown = self._cost_by_type(tool_cfg, parameters, "test_type", "neuropsych_battery")
        else:
            # Flat base cost (ECG, literature, drug interactions)
            total = float(tool_cfg.get("base", 0))
            if total:
                breakdown["base"] = total

        entry = ToolCostEntry(
            tool_name=tool_name,
            parameters=parameters,
            cost_usd=total,
            cost_breakdown=breakdown,
        )
        self.entries.append(entry)
        return entry

    @property
    def total_cost_usd(self) -> float:
        return sum(e.cost_usd for e in self.entries)

    def get_summary(self) -> dict[str, Any]:
        """Return cost summary for inclusion in agent trace."""
        by_tool: dict[str, float] = {}
        for e in self.entries:
            by_tool[e.tool_name] = by_tool.get(e.tool_name, 0) + e.cost_usd
        return {
            "total_cost_usd": self.total_cost_usd,
            "num_tool_calls": len(self.entries),
            "cost_by_tool": by_tool,
            "entries": [e.model_dump() for e in self.entries],
        }

    def reset(self) -> None:
        """Clear tracked entries for a new case."""
        self.entries.clear()

    # ------------------------------------------------------------------
    # Per-tool cost computation
    # ------------------------------------------------------------------

    @staticmethod
    def _cost_mri(cfg: dict, params: dict) -> tuple[float, dict[str, float]]:
        breakdown: dict[str, float] = {}
        base = float(cfg.get("base", 320))
        breakdown["base"] = base
        total = base
        if params.get("contrast"):
            modifier = float(cfg.get("modifiers", {}).get("contrast", 126))
            breakdown["contrast"] = modifier
            total += modifier
        return total, breakdown

    @staticmethod
    def _cost_by_type(
        cfg: dict, params: dict, type_key: str, default: str,
    ) -> tuple[float, dict[str, float]]:
        by_type = cfg.get("by_type", {})
        selected = params.get(type_key, default)
        cost = float(by_type.get(selected, by_type.get(default, 0)))
        return cost, {selected: cost}

    @staticmethod
    def _cost_labs(cfg: dict, params: dict) -> tuple[float, dict[str, float]]:
        by_panel = cfg.get("by_panel", {})
        default_cost = float(cfg.get("default_panel", 25))
        panels = params.get("panels", [])
        breakdown: dict[str, float] = {}
        total = 0.0
        if not panels:
            # No panels specified — assume basic screening
            cost = default_cost
            breakdown["unspecified"] = cost
            total = cost
        else:
            for panel in panels:
                cost = float(by_panel.get(panel, default_cost))
                breakdown[panel] = cost
                total += cost
        return total, breakdown

    @staticmethod
    def _cost_csf(cfg: dict, params: dict) -> tuple[float, dict[str, float]]:
        base = float(cfg.get("base", 250))
        breakdown: dict[str, float] = {"base": base}
        total = base
        by_test = cfg.get("by_special_test", {})
        default_cost = float(cfg.get("default_test", 50))
        for test in params.get("special_tests", []):
            cost = float(by_test.get(test, default_cost))
            breakdown[test] = cost
            total += cost
        return total, breakdown

    @staticmethod
    def _cost_ct(cfg: dict, params: dict) -> tuple[float, dict[str, float]]:
        base = float(cfg.get("base", 200))
        breakdown: dict[str, float] = {"base": base}
        total = base
        modifiers = cfg.get("modifiers", {})
        if params.get("contrast"):
            mod = float(modifiers.get("contrast", 100))
            breakdown["contrast"] = mod
            total += mod
        if params.get("angiography"):
            mod = float(modifiers.get("angiography", 200))
            breakdown["angiography"] = mod
            total += mod
        return total, breakdown
