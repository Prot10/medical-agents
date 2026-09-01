"""Typed service contracts for the NeuroAgent plugin harness."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol

from neuroagent_schemas import ClinicalAction, ClinicalEpisode, NeuroBenchCase, ToolAction


@dataclass(frozen=True, slots=True)
class ModelTurn:
    action: ClinicalAction
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_seconds: float = 0.0
    plugin_payload: Mapping[str, Any] = field(default_factory=dict)


class ModelAdapter(Protocol):
    adapter_id: str
    model_id: str

    def next_action(
        self,
        *,
        case: NeuroBenchCase,
        episode: ClinicalEpisode,
        allowed_tools: list[dict[str, Any]],
        require_assessment: bool = False,
        react: bool = False,
    ) -> ModelTurn: ...


class AgentLoop(Protocol):
    loop_id: str

    def run(self, context: "RunContext") -> ClinicalEpisode: ...


class ClinicalEnvironment(Protocol):
    environment_id: str
    case: NeuroBenchCase

    def tool_definitions(self) -> list[dict[str, Any]]: ...
    def execute(self, action: ToolAction) -> Any: ...


class RewardScorer(Protocol):
    scorer_id: str

    def score(self, episode: ClinicalEpisode, case: NeuroBenchCase) -> Any: ...


class EpisodeStore(Protocol):
    store_id: str

    def append(self, event: Any) -> None: ...
    def load(self) -> ClinicalEpisode: ...


@dataclass(slots=True)
class RunContext:
    profile_id: str
    model: ModelAdapter
    loop: AgentLoop
    environment: ClinicalEnvironment
    episode_store: EpisodeStore
    max_turns: int
    max_cost_usd: float | None = None
    max_invalid_actions: int = 1
    plugin_versions: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Plugin:
    plugin_id: str
    version: str
    provides: str
    requires: frozenset[str]
    factory: Callable[[Mapping[str, Any], "ServiceView"], Any]


class ServiceView(Protocol):
    def require(self, service: str) -> Any: ...
