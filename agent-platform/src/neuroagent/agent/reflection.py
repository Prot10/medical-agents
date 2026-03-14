"""Reflection module — prompts the agent to reflect after tool results."""

from __future__ import annotations

from ..llm.prompts import load_prompt

_DEFAULT_REFLECTION = (
    "Based on the tool results above, update your clinical reasoning. "
    "What do these findings tell you? How does this change your differential? "
    "What should you do next? If you have enough information for a diagnosis "
    "and recommendations, provide your final assessment."
)


def get_reflection_prompt() -> dict[str, str]:
    """Return a reflection prompt as an OpenAI-style user message."""
    try:
        text = load_prompt("reflection.txt")
    except FileNotFoundError:
        text = _DEFAULT_REFLECTION
    return {"role": "user", "content": text}
