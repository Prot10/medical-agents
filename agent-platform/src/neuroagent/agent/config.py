"""Runtime configuration for the agent orchestrator."""

from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Mapping

import yaml

DEFAULT_AGENT_CONFIG_PATH = (
    Path(__file__).resolve().parents[3] / "config" / "runtime" / "agent.yaml"
)


class AgentConfigError(ValueError):
    """Raised when the agent runtime config is missing or malformed."""


@dataclass(frozen=True, slots=True)
class AgentConfig:
    """Configuration for the agent orchestrator.

    Values must come from an explicit config source. Keep this dataclass free of
    defaults so missing runtime settings fail at config-load time.
    """

    base_url: str
    api_key: str
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    presence_penalty: float
    max_turns: int
    enable_reflection: bool
    hospital: str
    allowed_tools: list[str] | None
    excluded_tools: list[str] | None
    all_info_upfront: bool

    def __post_init__(self) -> None:
        _require_non_empty_string("base_url", self.base_url)
        _require_non_empty_string("api_key", self.api_key)
        _require_non_empty_string("model", self.model)
        _require_non_empty_string("hospital", self.hospital)
        _require_number("temperature", self.temperature, minimum=0)
        _require_number("top_p", self.top_p, minimum=0, maximum=1)
        _require_number("presence_penalty", self.presence_penalty)
        if (
            not isinstance(self.max_tokens, int)
            or isinstance(self.max_tokens, bool)
            or self.max_tokens <= 0
        ):
            raise AgentConfigError("max_tokens must be a positive integer")
        if (
            not isinstance(self.max_turns, int)
            or isinstance(self.max_turns, bool)
            or self.max_turns <= 0
        ):
            raise AgentConfigError("max_turns must be a positive integer")
        if not isinstance(self.enable_reflection, bool):
            raise AgentConfigError("enable_reflection must be a boolean")
        if not isinstance(self.all_info_upfront, bool):
            raise AgentConfigError("all_info_upfront must be a boolean")
        _require_optional_string_list("allowed_tools", self.allowed_tools)
        _require_optional_string_list("excluded_tools", self.excluded_tools)


_SCHEMA: dict[str, tuple[str, ...]] = {
    "llm": (
        "base_url",
        "api_key",
        "model",
        "temperature",
        "max_tokens",
        "top_p",
        "presence_penalty",
    ),
    "agent": (
        "max_turns",
        "enable_reflection",
        "allowed_tools",
        "excluded_tools",
        "all_info_upfront",
    ),
    "rules": ("hospital",),
}

_CONFIG_FIELDS = {field.name for field in fields(AgentConfig)}


def load_agent_config(
    config_path: str | Path = DEFAULT_AGENT_CONFIG_PATH,
    **overrides: Any,
) -> AgentConfig:
    """Load orchestrator config from YAML, applying explicit field overrides."""
    path = Path(config_path)
    if not path.exists():
        raise AgentConfigError(f"Agent config file not found: {path}")

    raw = yaml.safe_load(path.read_text())
    if not isinstance(raw, Mapping):
        raise AgentConfigError(f"Agent config must be a YAML mapping: {path}")

    values = _flatten_config(raw)
    unknown_overrides = sorted(set(overrides) - _CONFIG_FIELDS)
    if unknown_overrides:
        raise AgentConfigError(
            f"Unknown agent config override(s): {', '.join(unknown_overrides)}"
        )

    values.update(overrides)
    return AgentConfig(**values)


def _flatten_config(raw: Mapping[str, Any]) -> dict[str, Any]:
    unknown_sections = sorted(set(raw) - set(_SCHEMA))
    if unknown_sections:
        raise AgentConfigError(
            f"Unknown agent config section(s): {', '.join(unknown_sections)}"
        )

    values: dict[str, Any] = {}
    for section_name, keys in _SCHEMA.items():
        section = raw.get(section_name)
        if not isinstance(section, Mapping):
            raise AgentConfigError(f"Missing or invalid config section: {section_name}")

        unknown_keys = sorted(set(section) - set(keys))
        if unknown_keys:
            raise AgentConfigError(
                f"Unknown key(s) in {section_name}: {', '.join(unknown_keys)}"
            )

        for key in keys:
            if key not in section:
                raise AgentConfigError(f"Missing required config key: {section_name}.{key}")
            values[key] = section[key]

    return values


def _require_non_empty_string(name: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        raise AgentConfigError(f"{name} must be a non-empty string")


def _require_number(
    name: str,
    value: Any,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise AgentConfigError(f"{name} must be a number")
    if minimum is not None and value < minimum:
        raise AgentConfigError(f"{name} must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise AgentConfigError(f"{name} must be <= {maximum}")


def _require_optional_string_list(name: str, value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise AgentConfigError(f"{name} must be null or a list of strings")
