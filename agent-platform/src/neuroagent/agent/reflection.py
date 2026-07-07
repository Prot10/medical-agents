"""Reflection module — prompts the agent to reflect after tool results."""

from __future__ import annotations

from ..llm.prompts import load_prompt


def get_reflection_prompt() -> dict[str, str]:
    """Return a reflection prompt as an OpenAI-style user message."""
    return {"role": "user", "content": load_prompt("reflection.txt")}
