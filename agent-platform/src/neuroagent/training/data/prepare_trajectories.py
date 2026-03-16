"""Collect agent trajectories from NeuroBench cases for GRPO training.

Runs the agent N times per case with temperature=1.0 to collect diverse
trajectories, then scores each with the composite reward function.

Usage:
    python -m neuroagent.training.data.prepare_trajectories \
        --dataset data/neurobench_v1 \
        --output training_data/trajectories.json \
        --rollouts-per-case 8
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from neuroagent_schemas import NeuroBenchCase

from ...agent.orchestrator import AgentConfig, AgentOrchestrator
from ...agent.reasoning import AgentTrace
from ...tools.mock_server import MockServer
from ...tools.tool_registry import ToolRegistry
from ..rewards.composite_reward import CompositeReward, RewardBreakdown

logger = logging.getLogger(__name__)


@dataclass
class ScoredTrajectory:
    """A trajectory paired with its reward score."""

    case_id: str
    condition: str
    difficulty: str
    trace: dict[str, Any]  # AgentTrace.model_dump()
    reward: float
    reward_breakdown: dict[str, float]
    total_cost_usd: float


@dataclass
class TrajectoryDataset:
    """Collection of scored trajectories grouped by case."""

    trajectories: list[ScoredTrajectory] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "config": self.config,
            "num_trajectories": len(self.trajectories),
            "trajectories": [
                {
                    "case_id": t.case_id,
                    "condition": t.condition,
                    "difficulty": t.difficulty,
                    "trace": t.trace,
                    "reward": t.reward,
                    "reward_breakdown": t.reward_breakdown,
                    "total_cost_usd": t.total_cost_usd,
                }
                for t in self.trajectories
            ],
        }
        path.write_text(json.dumps(data, indent=2, default=str))
        logger.info("Saved %d trajectories to %s", len(self.trajectories), path)


def load_cases(dataset_path: Path, max_cases: int | None = None) -> list[NeuroBenchCase]:
    """Load NeuroBench cases from a dataset directory."""
    cases_dir = dataset_path / "cases"
    if not cases_dir.exists():
        raise FileNotFoundError(f"Cases directory not found: {cases_dir}")

    case_files = sorted(cases_dir.glob("*.json"))
    if max_cases:
        case_files = case_files[:max_cases]

    cases = []
    for cf in case_files:
        data = json.loads(cf.read_text())
        cases.append(NeuroBenchCase.model_validate(data))
    return cases


def format_patient_info(case: NeuroBenchCase) -> str:
    """Format patient info for the agent prompt."""
    parts = [
        f"Patient: {case.patient.demographics.age}-year-old {case.patient.demographics.sex}",
        f"Chief complaint: {case.patient.chief_complaint}",
        f"History of present illness: {case.patient.history_present_illness}",
    ]

    pmh = case.patient.clinical_history.past_medical_history
    if pmh:
        parts.append(f"Past medical history: {', '.join(pmh)}")

    meds = case.patient.clinical_history.medications
    if meds:
        med_strs = [f"{m.drug} {m.dose} {m.frequency}" for m in meds]
        parts.append(f"Current medications: {', '.join(med_strs)}")

    allergies = case.patient.clinical_history.allergies
    if allergies:
        parts.append(f"Allergies: {', '.join(allergies)}")

    parts.append(f"Neurological examination: {case.patient.neurological_exam.model_dump_json()}")
    parts.append(f"Vitals: {case.patient.vitals.model_dump_json()}")

    return "\n".join(parts)


def collect_trajectories(
    cases: list[NeuroBenchCase],
    agent_config: AgentConfig,
    reward_fn: CompositeReward,
    rollouts_per_case: int = 8,
    rules_dir: str = "config/hospital_rules",
    hospital: str = "us_mayo",
    epoch: int | None = None,
) -> TrajectoryDataset:
    """Run the agent multiple times per case and score each trajectory.

    Args:
        cases: NeuroBench cases to run.
        agent_config: Agent configuration (temperature should be 1.0).
        reward_fn: Composite reward function for scoring.
        rollouts_per_case: Number of trajectories to collect per case.
        rules_dir: Path to hospital rules.
        hospital: Hospital ID for rules/compliance.
        epoch: Training epoch (for dynamic reward scheduling).

    Returns:
        TrajectoryDataset with scored trajectories.
    """
    dataset = TrajectoryDataset(
        config={
            "rollouts_per_case": rollouts_per_case,
            "model": agent_config.model,
            "temperature": agent_config.temperature,
            "hospital": hospital,
        }
    )

    rules_engine = None
    try:
        from ...rules.rules_engine import RulesEngine
        rules_engine = RulesEngine(rules_dir, hospital=hospital)
    except Exception:
        logger.warning("Could not load rules engine")

    for i, case in enumerate(cases):
        logger.info(
            "Case %d/%d: %s (%s, %s) — generating %d rollouts",
            i + 1, len(cases), case.case_id,
            case.condition.value, case.difficulty.value,
            rollouts_per_case,
        )

        mock_server = MockServer(case)
        patient_info = format_patient_info(case)

        for r in range(rollouts_per_case):
            tool_registry = ToolRegistry.create_default_registry(mock_server=mock_server)
            agent = AgentOrchestrator(
                config=agent_config,
                tool_registry=tool_registry,
                rules_engine=rules_engine,
            )

            trace = agent.run(
                patient_info=patient_info,
                case_id=case.case_id,
            )

            breakdown = reward_fn.compute_with_breakdown(trace, case, epoch=epoch)

            scored = ScoredTrajectory(
                case_id=case.case_id,
                condition=case.condition.value,
                difficulty=case.difficulty.value,
                trace=trace.model_dump(),
                reward=breakdown.composite,
                reward_breakdown={
                    "correctness": breakdown.correctness,
                    "actions": breakdown.actions,
                    "safety": breakdown.safety,
                    "cost": breakdown.cost,
                    "compliance": breakdown.compliance,
                    "format": breakdown.format,
                },
                total_cost_usd=breakdown.total_cost_usd,
            )
            dataset.trajectories.append(scored)

            logger.info(
                "  Rollout %d/%d: reward=%.3f, tools=%d, cost=$%.0f",
                r + 1, rollouts_per_case, breakdown.composite,
                trace.total_tool_calls, breakdown.total_cost_usd,
            )

    return dataset


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect agent trajectories for GRPO training")
    parser.add_argument("--dataset", required=True, help="Path to NeuroBench dataset directory")
    parser.add_argument("--output", required=True, help="Output path for trajectories JSON")
    parser.add_argument("--rollouts-per-case", type=int, default=8, help="Rollouts per case")
    parser.add_argument("--max-cases", type=int, default=None, help="Limit number of cases")
    parser.add_argument("--model", default="Qwen/Qwen3.5-9B", help="Model name")
    parser.add_argument("--base-url", default="http://localhost:8000/v1", help="LLM API base URL")
    parser.add_argument("--hospital", default="us_mayo", help="Hospital for rules")
    parser.add_argument("--reward-config", default="config/reward_weights.yaml")
    parser.add_argument("--tool-costs", default="config/tool_costs.yaml")
    parser.add_argument("--rules-dir", default="config/hospital_rules")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    cases = load_cases(Path(args.dataset), max_cases=args.max_cases)
    logger.info("Loaded %d cases", len(cases))

    agent_config = AgentConfig(
        base_url=args.base_url,
        model=args.model,
        temperature=1.0,  # high temperature for diverse rollouts
    )

    reward_fn = CompositeReward.from_config(
        reward_config_path=args.reward_config,
        tool_costs_path=args.tool_costs,
        rules_dir=args.rules_dir,
        hospital=args.hospital,
    )

    dataset = collect_trajectories(
        cases=cases,
        agent_config=agent_config,
        reward_fn=reward_fn,
        rollouts_per_case=args.rollouts_per_case,
        rules_dir=args.rules_dir,
        hospital=args.hospital,
    )

    dataset.save(args.output)
    logger.info("Done. %d total trajectories collected.", len(dataset.trajectories))


if __name__ == "__main__":
    main()
