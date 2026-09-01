"""Typed benchmark runner with atomic append-only episode checkpoints."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from neuroagent_schemas import ClinicalEpisode, NeuroBenchCase

from ..harness.environment import NeuroBenchEnvironment
from ..harness.interfaces import AgentLoop, ModelAdapter, RunContext
from ..harness.store import JsonlEpisodeStore, MemoryEpisodeStore
from .policy_reward import ClinicalPolicyReward, RewardBreakdown


@dataclass(frozen=True, slots=True)
class CaseResult:
    case_id: str
    episode: ClinicalEpisode
    reward: RewardBreakdown | None


@dataclass(slots=True)
class EvaluationResults:
    results: list[CaseResult] = field(default_factory=list)
    failures: list[dict[str, str]] = field(default_factory=list)


class EvaluationRunner:
    """Execute one immutable profile across a case split."""

    def __init__(
        self,
        *,
        profile_id: str,
        model_factory: Callable[[], ModelAdapter],
        loop: AgentLoop,
        max_turns: int,
        max_cost_usd: float | None = None,
        scorer: ClinicalPolicyReward | None = None,
        output_dir: str | Path | None = None,
    ) -> None:
        self.profile_id = profile_id
        self.model_factory = model_factory
        self.loop = loop
        self.max_turns = max_turns
        self.max_cost_usd = max_cost_usd
        self.scorer = scorer
        self.output_dir = Path(output_dir) if output_dir is not None else None

    def run_case(self, case: NeuroBenchCase) -> CaseResult:
        if self.output_dir is None:
            store = MemoryEpisodeStore()
        else:
            store = JsonlEpisodeStore(self.output_dir / f"{case.case_id}.events.jsonl")
        model = self.model_factory()
        context = RunContext(
            profile_id=self.profile_id,
            model=model,
            loop=self.loop,
            environment=NeuroBenchEnvironment(case),
            episode_store=store,
            max_turns=self.max_turns,
            max_cost_usd=self.max_cost_usd,
            plugin_versions={self.loop.loop_id: "1.0", model.adapter_id: "1.0"},
        )
        episode = self.loop.run(context)
        reward = self.scorer.score(episode, case) if self.scorer is not None else None
        return CaseResult(case_id=case.case_id, episode=episode, reward=reward)

    def run_cases(self, cases: list[NeuroBenchCase]) -> EvaluationResults:
        results = EvaluationResults()
        for case in cases:
            try:
                results.results.append(self.run_case(case))
            except Exception as exc:
                results.failures.append(
                    {
                        "case_id": case.case_id,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
        return results


def load_cases(dataset_path: str | Path, split: str) -> list[NeuroBenchCase]:
    root = Path(dataset_path)
    cases_dir = root / "cases"
    split_file = root / "splits" / f"{split}.txt"
    if split_file.exists():
        ids = [line.strip() for line in split_file.read_text().splitlines() if line.strip()]
        paths = [cases_dir / f"{case_id}.json" for case_id in ids]
    else:
        paths = sorted(cases_dir.glob("*.json"))
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"split references missing cases: {missing[:10]}")
    return [NeuroBenchCase.model_validate_json(path.read_text()) for path in paths]
