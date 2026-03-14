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


def format_tool_result(tool_call_id: str, tool_name: str, result: dict) -> dict:
    """Format a tool result as an OpenAI-style tool message."""
    import json

    content = json.dumps(result, indent=2, default=str)
    return {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "content": content,
    }
