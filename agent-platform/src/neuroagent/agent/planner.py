"""Action planning module — decides what tool to call next."""

from __future__ import annotations

# The planner is currently implicit in the orchestrator's ReAct loop:
# the LLM decides what tool to call next based on its chain-of-thought.
# This module provides utilities for forced or constrained planning
# (e.g., ablation experiments with fixed tool ordering).

import random
from typing import Any


def get_forced_tool_order(tool_names: list[str], strategy: str = "sequential") -> list[str]:
    """Return a forced tool ordering for ablation experiments.

    Args:
        tool_names: Available tool names.
        strategy: "sequential" (as-is), "random", or "reverse".

    Returns:
        Ordered list of tool names.
    """
    if strategy == "random":
        names = list(tool_names)
        random.shuffle(names)
        return names
    elif strategy == "reverse":
        return list(reversed(tool_names))
    return list(tool_names)


def restrict_tools(
    all_definitions: list[dict[str, Any]],
    allowed_tools: list[str] | None = None,
    excluded_tools: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Filter tool definitions for ablation experiments.

    Args:
        all_definitions: All tool definitions from the registry.
        allowed_tools: If set, only include these tools.
        excluded_tools: If set, exclude these tools.

    Returns:
        Filtered list of tool definitions.
    """
    if allowed_tools is not None:
        return [d for d in all_definitions if d["function"]["name"] in allowed_tools]
    if excluded_tools is not None:
        return [d for d in all_definitions if d["function"]["name"] not in excluded_tools]
    return all_definitions
