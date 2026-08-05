"""Cost tracking for diagnostic tool calls using Medicare reference rates.

Costs feed a reported metric (cost-efficiency in the paper), so a term missing
from ``config/tools/costs.yaml`` fails loudly (:class:`CostConfigError`) rather
than silently substituting a hardcoded literal.  Two kinds of lookup miss are
deliberately NOT errors, because they depend on model behavior at run time and
must not crash or alter an evaluation run:

* an *out-of-vocabulary parameter value* (unknown panel / modality / test type)
  falls back to the tool's **configured** default rate, exactly as before — the
  catchall tools log a warning at execute time (see tools/vocabulary.py);
* an *unknown tool name* costs 0 with a warning (training rewards replay raw
  rollouts that may contain hallucinated tool names).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from .vocabulary import normalize_analyte

logger = logging.getLogger(__name__)


class CostConfigError(KeyError):
    """A required cost entry is missing from costs.yaml."""


class ToolCostEntry(BaseModel):
    """Cost record for a single tool invocation."""

    tool_name: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    cost_usd: float
    cost_breakdown: dict[str, float] = Field(default_factory=dict)


def _as_item_names(value: Any) -> list[str]:
    """Normalise a free-text list parameter into hashable, priceable item names.

    A generating policy is not bound by the schema: it emits `panels` as a bare string, a list
    of strings, a nested list, or a dict, and the tool-call parser coerces whatever it finds.
    Pricing then does `name in by_panel`, which raises `TypeError: unhashable type: 'list'` on
    a nested entry and killed a real training run mid-rollout. Flatten one level, stringify
    anything exotic, and drop empties, so an odd generation costs money rather than the run.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, dict):
        value = list(value.keys())
    if not isinstance(value, (list, tuple, set)):
        return [str(value)]
    names: list[str] = []
    for item in value:
        if isinstance(item, str):
            if item.strip():
                names.append(item)
        elif isinstance(item, (list, tuple, set)):
            names.extend(_as_item_names(item))  # one nesting level is common; recurse safely
        elif isinstance(item, dict):
            names.extend(_as_item_names(list(item.keys())))
        elif item is not None:
            names.append(str(item))
    return names


class CostTracker:
    """Compute and track costs for diagnostic tool calls.

    Loads per-tool cost rules from a YAML config.  Costs are parameter-dependent:
    e.g. MRI cost varies with contrast, labs cost varies by panels requested.
    """

    def __init__(self, config_path: str | Path | None = None):
        if config_path is None:
            config_path = Path(__file__).resolve().parents[3] / "config" / "tools" / "costs.yaml"
        self.config_path = Path(config_path)
        self.config = self._load_config(self.config_path)
        self.entries: list[ToolCostEntry] = []

    @staticmethod
    def _load_config(path: Path) -> dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(
                f"Cost config not found: {path}. Costs feed a reported metric, "
                "so running without a cost registry is not allowed."
            )
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return data.get("tools", {})

    def _require(self, cfg: dict[str, Any], key: str, tool_name: str) -> Any:
        """Fetch a required cost entry; missing keys fail loudly."""
        if key not in cfg:
            raise CostConfigError(
                f"Cost entry '{key}' for tool '{tool_name}' is missing from "
                f"{self.config_path}. Add the entry to costs.yaml — silent "
                "fallback rates are not allowed because costs feed a reported metric."
            )
        return cfg[key]

    def compute_cost(self, tool_name: str, parameters: dict[str, Any]) -> ToolCostEntry:
        """Compute cost for a single tool call and record it."""
        tool_cfg = self.config.get(tool_name)
        breakdown: dict[str, float] = {}
        total = 0.0

        if tool_cfg is None:
            # Unknown tool (e.g. hallucinated name in a raw training rollout):
            # cost 0, but never silently.
            logger.warning(
                "No cost entry for unknown tool '%s' in %s — recording 0 cost.",
                tool_name, self.config_path,
            )
        elif tool_name == "analyze_brain_mri":
            total, breakdown = self._cost_mri(tool_cfg, parameters)
        elif tool_name == "analyze_eeg":
            total, breakdown = self._cost_by_type(tool_cfg, parameters, "eeg_type", "routine", tool_name)
        elif tool_name == "interpret_labs":
            total, breakdown = self._cost_labs(tool_cfg, parameters)
        elif tool_name == "analyze_csf":
            total, breakdown = self._cost_csf(tool_cfg, parameters)
        elif tool_name == "order_ct_scan":
            total, breakdown = self._cost_ct(tool_cfg, parameters)
        elif tool_name == "order_echocardiogram":
            total, breakdown = self._cost_by_type(tool_cfg, parameters, "echo_type", "TTE", tool_name)
        elif tool_name == "order_cardiac_monitoring":
            total, breakdown = self._cost_by_type(tool_cfg, parameters, "monitor_type", "holter_24h", tool_name)
        elif tool_name == "order_advanced_imaging":
            total, breakdown = self._cost_by_type(tool_cfg, parameters, "modality", "FDG_PET", tool_name)
        elif tool_name == "order_specialized_test":
            total, breakdown = self._cost_specialized_test(tool_cfg, parameters)
        else:
            # Flat base cost (ECG, literature, drug interactions)
            total = float(self._require(tool_cfg, "base", tool_name))
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

    def _cost_mri(self, cfg: dict, params: dict) -> tuple[float, dict[str, float]]:
        breakdown: dict[str, float] = {}
        base = float(self._require(cfg, "base", "analyze_brain_mri"))
        breakdown["base"] = base
        total = base
        if params.get("contrast"):
            modifiers = self._require(cfg, "modifiers", "analyze_brain_mri")
            modifier = float(self._require(modifiers, "contrast", "analyze_brain_mri"))
            breakdown["contrast"] = modifier
            total += modifier
        return total, breakdown

    def _cost_by_type(
        self, cfg: dict, params: dict, type_key: str, default: str, tool_name: str,
    ) -> tuple[float, dict[str, float]]:
        by_type = self._require(cfg, "by_type", tool_name)
        # The default type must always be priced — its absence is a config error.
        default_cost = float(self._require(by_type, default, tool_name))
        selected = params.get(type_key, default)
        if selected not in by_type:
            # Out-of-vocabulary parameter value: keep the pre-existing fallback
            # to the default type's rate (never crash mid-run on model output).
            logger.warning(
                "Unpriced %s=%r for tool '%s' in %s — falling back to the "
                "'%s' rate (%.0f).",
                type_key, selected, tool_name, self.config_path, default, default_cost,
            )
        cost = float(by_type.get(selected, default_cost))
        return cost, {selected: cost}

    def _cost_specialized_test(
        self, cfg: dict, params: dict,
    ) -> tuple[float, dict[str, float]]:
        """Cost lookup for `order_specialized_test`.

        Handles the closed-vocabulary case (`test_type` in `by_type`) plus
        the `genetic_panel:<panel>` syntax, where `<panel>` is looked up in
        the `genetic_panels` block. See dataset-generation/TOOL_PARAMETER_VOCABULARY.md.
        """
        tool_name = "order_specialized_test"
        selected = params.get("test_type", "neuropsych_battery")
        if isinstance(selected, str) and selected.startswith("genetic_panel:"):
            genetic_panels = self._require(cfg, "genetic_panels", tool_name)
            default_panel_cost = float(self._require(cfg, "default_genetic_panel", tool_name))
            panel = selected.split(":", 1)[1]
            if panel not in genetic_panels:
                logger.warning(
                    "Unpriced genetic panel %r for tool '%s' in %s — falling "
                    "back to the configured default_genetic_panel rate (%.0f).",
                    panel, tool_name, self.config_path, default_panel_cost,
                )
            cost = float(genetic_panels.get(panel, default_panel_cost))
            return cost, {selected: cost}
        return self._cost_by_type(cfg, params, "test_type", "neuropsych_battery", tool_name)

    @staticmethod
    def _priced_lookup(rates: dict) -> dict[str, float]:
        """Rate table indexed by normalised assay name.

        The score normalises assay names (`evaluation/metrics.py::_as_set`) so a model is
        not penalised for writing `Protein C` instead of `protein_C`. Pricing has to agree,
        or the same call would be credited as correct and billed at the fallback rate — the
        bill and the score must read one workup the same way.
        """
        return {normalize_analyte(str(name)): float(rate) for name, rate in rates.items()}

    def _cost_labs(self, cfg: dict, params: dict) -> tuple[float, dict[str, float]]:
        tool_name = "interpret_labs"
        by_panel = self._priced_lookup(self._require(cfg, "by_panel", tool_name))
        default_cost = float(self._require(cfg, "default_panel", tool_name))
        panels = _as_item_names(params.get("panels", []))
        breakdown: dict[str, float] = {}
        total = 0.0
        if not panels:
            # No panels specified — assume basic screening
            cost = default_cost
            breakdown["unspecified"] = cost
            total = cost
        else:
            for panel in panels:
                key = normalize_analyte(panel)
                if key not in by_panel:
                    logger.warning(
                        "Unpriced lab panel %r for tool '%s' in %s — falling "
                        "back to the configured default_panel rate (%.0f).",
                        panel, tool_name, self.config_path, default_cost,
                    )
                cost = by_panel.get(key, default_cost)
                breakdown[panel] = cost
                total += cost
        return total, breakdown

    def _cost_csf(self, cfg: dict, params: dict) -> tuple[float, dict[str, float]]:
        tool_name = "analyze_csf"
        base = float(self._require(cfg, "base", tool_name))
        breakdown: dict[str, float] = {"base": base}
        total = base
        by_test = self._priced_lookup(self._require(cfg, "by_special_test", tool_name))
        default_cost = float(self._require(cfg, "default_test", tool_name))
        for test in _as_item_names(params.get("special_tests", [])):
            key = normalize_analyte(test)
            if key not in by_test:
                logger.warning(
                    "Unpriced CSF special test %r for tool '%s' in %s — falling "
                    "back to the configured default_test rate (%.0f).",
                    test, tool_name, self.config_path, default_cost,
                )
            cost = by_test.get(key, default_cost)
            breakdown[test] = cost
            total += cost
        return total, breakdown

    def _cost_ct(self, cfg: dict, params: dict) -> tuple[float, dict[str, float]]:
        tool_name = "order_ct_scan"
        base = float(self._require(cfg, "base", tool_name))
        breakdown: dict[str, float] = {"base": base}
        total = base
        if params.get("contrast"):
            modifiers = self._require(cfg, "modifiers", tool_name)
            mod = float(self._require(modifiers, "contrast", tool_name))
            breakdown["contrast"] = mod
            total += mod
        if params.get("angiography"):
            modifiers = self._require(cfg, "modifiers", tool_name)
            mod = float(self._require(modifiers, "angiography", tool_name))
            breakdown["angiography"] = mod
            total += mod
        return total, breakdown
