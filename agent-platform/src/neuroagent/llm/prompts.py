"""Prompt loading and formatting utilities."""

from __future__ import annotations

from pathlib import Path

_PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "config" / "system_prompts"


def load_prompt(name: str) -> str:
    """Load a system prompt from the config/system_prompts directory."""
    path = _PROMPTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text().strip()


# The base prompt already asks for the shortest defensible path, so the "concise" style is
# just the base prompt with no addition — and it is the inference default, matching the
# efficient_linear trajectories. The "differential" style adds one instruction: still order
# only justified tests, but make the exclusion reasoning explicit. It matches the
# differential_reasoned trajectories, which demonstrate ruling out plausible-but-wrong
# diagnoses with evidence while staying optimal (zero useless calls).
#
# This directive is the single source for both training (the trajectory system prompts) and
# inference (AgentOrchestrator._build_system_prompt), so the two cannot drift.
REASONING_STYLE_DIRECTIVE = {
    "concise": "",
    "differential": (
        "## Reasoning Approach\n"
        "Stay concise and order only the tests that will change your differential — never "
        "test for completeness. But make your reasoning explicit: at each step, name the "
        "competing diagnoses and rule out the plausible-but-wrong ones with evidence before "
        "you converge on the answer."
    ),
}

# The two trajectory styles map onto the two directives.
STYLE_TO_DIRECTIVE = {
    "efficient_linear": "concise",
    "differential_reasoned": "differential",
}


def apply_reasoning_style(base: str, style: str | None) -> str:
    """Insert the style directive after the base prompt, before any hospital protocols.

    `style` is a REASONING_STYLE_DIRECTIVE key (or a trajectory-style name, which is mapped).
    An empty/unknown/`concise` style returns `base` unchanged — that is the inference default
    and the efficient_linear trajectories.
    """
    key = STYLE_TO_DIRECTIVE.get(style, style)
    directive = REASONING_STYLE_DIRECTIVE.get(key or "concise", "")
    if not directive:
        return base
    if directive in base:  # idempotent: never append the directive twice
        return base

    marker = "\n\n## Hospital Protocols\n"
    if marker in base:
        head, protocols = base.split(marker, 1)
        return f"{head}\n\n{directive}{marker}{protocols}"
    return f"{base}\n\n{directive}"


def format_tool_result(tool_call_id: str, tool_name: str, result: dict) -> dict:
    """Format a tool result as an OpenAI-style tool message."""
    import json

    content = json.dumps(result, indent=2, default=str)
    return {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": content,
    }
