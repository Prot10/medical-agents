"""Backend-neutral group-relative policy optimization over typed episodes."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol, Sequence

from neuroagent_schemas import ClinicalEpisode, NeuroBenchCase

from ..harness.interfaces import ModelAdapter
from .rollout.environment_rollout import EnvironmentRollout


class TrainablePolicyBackend(Protocol):
    """Minimal bridge implemented by the Transformers/TRL training process."""

    def sampled_adapters(self, case: NeuroBenchCase, count: int) -> Sequence[ModelAdapter]: ...
    def update(self, episodes: Sequence[ClinicalEpisode], advantages: Sequence[float]) -> dict: ...


@dataclass(frozen=True, slots=True)
class GRPOStep:
    case_id: str
    rewards: tuple[float, ...]
    advantages: tuple[float, ...]
    update_metrics: dict


def group_relative_advantages(rewards: Sequence[float], epsilon: float = 1e-6) -> list[float]:
    if len(rewards) < 2:
        raise ValueError("GRPO requires at least two samples per case")
    mean = sum(rewards) / len(rewards)
    variance = sum((reward - mean) ** 2 for reward in rewards) / len(rewards)
    scale = math.sqrt(variance + epsilon)
    return [(reward - mean) / scale for reward in rewards]


class GRPOCoordinator:
    """Collects environment rollouts and sends normalized advantages to the backend."""

    def __init__(
        self,
        rollout: EnvironmentRollout,
        backend: TrainablePolicyBackend,
        *,
        group_size: int = 8,
    ) -> None:
        if group_size < 2:
            raise ValueError("group_size must be at least 2")
        self.rollout = rollout
        self.backend = backend
        self.group_size = group_size

    def step(self, case: NeuroBenchCase) -> GRPOStep:
        adapters = self.backend.sampled_adapters(case, self.group_size)
        if len(adapters) != self.group_size:
            raise ValueError("backend returned the wrong number of sampled adapters")
        results = [self.rollout.run(case, adapter) for adapter in adapters]
        rewards = [result.reward.scalar for result in results]
        advantages = group_relative_advantages(rewards)
        metrics = self.backend.update(
            [result.episode for result in results],
            advantages,
        )
        return GRPOStep(
            case_id=case.case_id,
            rewards=tuple(rewards),
            advantages=tuple(advantages),
            update_metrics=metrics,
        )
