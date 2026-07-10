"""The closed parameter vocabulary for the two catchall diagnostic tools.

`order_specialized_test` and `order_advanced_imaging` each stand in for many distinct
studies, selected by a single parameter (`test_type` / `modality`). That parameter is a
**closed vocabulary**: if two cases could spell the same study differently ("EMG/NCS" vs
"nerve conduction studies"), the metric layer would count them as different tools and cost
lookup would fall back to a default rate.

`config/tools/costs.yaml` is the single source of truth — every vocabulary term is a row
there, so a term cannot exist without a price. The tool schemas, the case validator, and
`dataset-generation/TOOL_PARAMETER_VOCABULARY.md` all derive from it.

This module exists because those three artifacts previously each carried their own copy and
drifted: the tool enums exposed 9 of 19 specialized tests and 6 of 11 imaging modalities,
while the 600 benchmark cases and costs.yaml used the full vocabulary. Ground-truth values
that were perfectly legal became "invalid" against the tool the agent actually calls.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

DEFAULT_COSTS_PATH = Path(__file__).resolve().parents[3] / "config" / "tools" / "costs.yaml"

# A genetic panel is written `genetic_panel:<panel>`; `<panel>` must be a row in the
# `genetic_panels` block. JSON Schema `enum` cannot express this, so the tool schema lists
# the fixed test types and the validator checks the prefixed form.
GENETIC_PANEL_PREFIX = "genetic_panel:"


@lru_cache(maxsize=4)
def _load_tools(costs_path: Path = DEFAULT_COSTS_PATH) -> dict[str, Any]:
    if not costs_path.exists():
        return {}
    with open(costs_path) as f:
        return (yaml.safe_load(f) or {}).get("tools", {})


def specialized_test_types(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `order_specialized_test.test_type` vocabulary (excluding genetic panels)."""
    return sorted(_load_tools(costs_path).get("order_specialized_test", {}).get("by_type", {}))


def genetic_panels(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """Allowed `<panel>` suffixes for `genetic_panel:<panel>`."""
    return sorted(_load_tools(costs_path).get("order_specialized_test", {}).get("genetic_panels", {}))


def advanced_imaging_modalities(costs_path: Path = DEFAULT_COSTS_PATH) -> list[str]:
    """The closed `order_advanced_imaging.modality` vocabulary."""
    return sorted(_load_tools(costs_path).get("order_advanced_imaging", {}).get("by_type", {}))


def is_valid_test_type(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    """True for a fixed test type or a `genetic_panel:<panel>` with a known panel."""
    if value.startswith(GENETIC_PANEL_PREFIX):
        return value[len(GENETIC_PANEL_PREFIX) :] in genetic_panels(costs_path)
    return value in specialized_test_types(costs_path)


def is_valid_modality(value: str, costs_path: Path = DEFAULT_COSTS_PATH) -> bool:
    return value in advanced_imaging_modalities(costs_path)
