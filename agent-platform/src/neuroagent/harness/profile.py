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
    max_invalid_actions: int = Field(default=2, ge=0)
    plugins: list[ProfilePlugin] = Field(min_length=1)

    def plugin_configs(self) -> list[PluginConfig]:
        return [PluginConfig(plugin_id=item.id, config=item.config) for item in self.plugins]


def load_profile(path: str | Path) -> HarnessProfile:
    profile_path = Path(path)
    raw = yaml.safe_load(profile_path.read_text())
    if not isinstance(raw, Mapping):
        raise ValueError(f"profile must be a mapping: {profile_path}")
    return HarnessProfile.model_validate(raw)


def load_profiles(directory: str | Path) -> dict[str, HarnessProfile]:
    """Every checked profile keyed by id; duplicate ids are a configuration error."""
    profiles: dict[str, HarnessProfile] = {}
    for path in sorted(Path(directory).glob("*.yaml")):
        profile = load_profile(path)
        if profile.profile_id in profiles:
            raise ValueError(f"duplicate profile_id: {profile.profile_id}")
        profiles[profile.profile_id] = profile
    return profiles
