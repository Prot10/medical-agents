"""Environment-coupled rollout used by evaluation and policy optimization."""

from __future__ import annotations

from dataclasses import dataclass

from neuroagent_schemas import ClinicalEpisode, NeuroBenchCase

from ...evaluation.policy_reward import ClinicalPolicyReward, RewardBreakdown
from ...harness.environment import NeuroBenchEnvironment
from ...harness.interfaces import AgentLoop, ModelAdapter, RunContext
from ...harness.store import MemoryEpisodeStore


@dataclass(frozen=True, slots=True)
class RolloutResult:
    case_id: str
    episode: ClinicalEpisode
    reward: RewardBreakdown


class EnvironmentRollout:
    """Runs the same typed policy loop used at inference; no training-only parser."""

    def __init__(
        self,
        *,
        loop: AgentLoop,
        scorer: ClinicalPolicyReward,
        max_turns: int = 12,
        max_cost_usd: float | None = 15000.0,
    ) -> None:
        self.loop = loop
        self.scorer = scorer
        self.max_turns = max_turns
        self.max_cost_usd = max_cost_usd

    def run(self, case: NeuroBenchCase, model: ModelAdapter) -> RolloutResult:
        context = RunContext(
            profile_id="training-policy",
            model=model,
            loop=self.loop,
            environment=NeuroBenchEnvironment(case),
            episode_store=MemoryEpisodeStore(),
            max_turns=self.max_turns,
            max_cost_usd=self.max_cost_usd,
            plugin_versions={self.loop.loop_id: "1.0", model.adapter_id: "1.0"},
        )
        episode = self.loop.run(context)
        return RolloutResult(
            case_id=case.case_id,
            episode=episode,
            reward=self.scorer.score(episode, case),
        )
