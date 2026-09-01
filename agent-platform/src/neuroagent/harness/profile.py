"""Strict YAML profile loader for plugin composition."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import yaml
from pydantic import BaseModel, ConfigDict, Field

from .kernel import PluginConfig


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ProfilePlugin(_StrictModel):
    id: str
    config: dict[str, Any] = Field(default_factory=dict)


class HarnessProfile(_StrictModel):
    profile_id: str
    max_turns: int = Field(gt=0)
    max_cost_usd: float | None = Field(default=None, gt=0)
    plugins: list[ProfilePlugin] = Field(min_length=1)

    def plugin_configs(self) -> list[PluginConfig]:
        return [PluginConfig(plugin_id=item.id, config=item.config) for item in self.plugins]


def load_profile(path: str | Path) -> HarnessProfile:
    profile_path = Path(path)
    raw = yaml.safe_load(profile_path.read_text())
    if not isinstance(raw, Mapping):
        raise ValueError(f"profile must be a mapping: {profile_path}")
    return HarnessProfile.model_validate(raw)
