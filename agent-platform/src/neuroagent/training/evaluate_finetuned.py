"""Evaluate a fine-tuned model (base + LoRA adapter) on NeuroBench.

Runs the full evaluation suite comparing base model vs fine-tuned,
reporting all existing metrics plus new cost-efficiency metrics.

Usage:
    python -m neuroagent.training.evaluate_finetuned \
        --adapter checkpoints/grpo_final \
        --dataset data/neurobench_v1 \
        --output results/grpo_eval.json
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from neuroagent_schemas import NeuroBenchCase

from ..agent.orchestrator import AgentConfig
from ..evaluation.metrics import MetricsCalculator
from ..evaluation.runner import CaseResult, EvaluationRunner
from .rewards.composite_reward import CompositeReward
from .rewards.cost_reward import CostReward

logger = logging.getLogger(__name__)


@dataclass
class ExtendedMetrics:
    """Extended metrics including cost-efficiency."""

    # Standard metrics
    diagnostic_accuracy_top1: float = 0.0
    diagnostic_accuracy_top3: float = 0.0
    action_precision: float = 0.0
    action_recall: float = 0.0
    critical_actions_hit: float = 0.0
    contraindicated_actions_taken: float = 0.0
    tool_call_count: float = 0.0
    efficiency_score: float = 0.0
    safety_score: float = 0.0

    # New cost metrics
    total_cost_usd: float = 0.0
    cost_efficiency_ratio: float = 0.0  # accuracy / cost
    unnecessary_cost_usd: float = 0.0

    # Composite reward
    composite_reward: float = 0.0


def evaluate_model(
    config: AgentConfig,
    dataset_path: str,
    reward_fn: CompositeReward,
    cost_fn: CostReward,
    max_cases: int | None = None,
    hospital: str = "us_mayo",
) -> tuple[list[CaseResult], ExtendedMetrics]:
    """Run evaluation and compute extended metrics."""
    runner = EvaluationRunner(config=config, dataset_path=dataset_path)
    results = runner.run_evaluation(
        max_cases=max_cases,
        enable_rules=True,
        hospital=hospital,
    )

    calculator = MetricsCalculator()
    cases = _load_cases(dataset_path, max_cases)
    case_map = {c.case_id: c for c in cases}

    # Accumulate metrics
    n = len(results.results)
    totals = ExtendedMetrics()

    for result in results.results:
        case = case_map.get(result.case_id)
        if case is None:
            continue

        # Standard metrics
        metrics = calculator.compute_all(result.trace, case.ground_truth)
        result.metrics = {
            "diagnostic_accuracy_top1": metrics.diagnostic_accuracy_top1,
            "diagnostic_accuracy_top3": metrics.diagnostic_accuracy_top3,
            "action_precision": metrics.action_precision,
            "action_recall": metrics.action_recall,
            "critical_actions_hit": metrics.critical_actions_hit,
            "contraindicated_actions_taken": metrics.contraindicated_actions_taken,
            "tool_call_count": metrics.tool_call_count,
            "efficiency_score": metrics.efficiency_score,
            "safety_score": metrics.safety_score,
        }

        totals.diagnostic_accuracy_top1 += int(metrics.diagnostic_accuracy_top1)
        totals.diagnostic_accuracy_top3 += int(metrics.diagnostic_accuracy_top3)
        totals.action_precision += metrics.action_precision
        totals.action_recall += metrics.action_recall
        totals.critical_actions_hit += metrics.critical_actions_hit
        totals.contraindicated_actions_taken += metrics.contraindicated_actions_taken
        totals.tool_call_count += metrics.tool_call_count
        totals.efficiency_score += metrics.efficiency_score
        totals.safety_score += metrics.safety_score

        # Cost metrics
        optimal_tools = {
            s.tool_name for s in case.ground_truth.optimal_actions if s.tool_name
        }
        breakdown = cost_fn.breakdown(result.trace.tools_called, optimal_tools)
        result.metrics["total_cost_usd"] = breakdown.total_cost
        result.metrics["unnecessary_cost_usd"] = breakdown.wasted_cost

        totals.total_cost_usd += breakdown.total_cost
        totals.unnecessary_cost_usd += breakdown.wasted_cost

        # Composite reward
        reward = reward_fn.compute(result.trace, case)
        result.metrics["composite_reward"] = reward
        totals.composite_reward += reward

    # Average
    if n > 0:
        totals.diagnostic_accuracy_top1 /= n
        totals.diagnostic_accuracy_top3 /= n
        totals.action_precision /= n
        totals.action_recall /= n
        totals.critical_actions_hit /= n
        totals.contraindicated_actions_taken /= n
        totals.tool_call_count /= n
        totals.efficiency_score /= n
        totals.safety_score /= n
        totals.total_cost_usd /= n
        totals.unnecessary_cost_usd /= n
        totals.composite_reward /= n

        # Cost efficiency: accuracy per $1000
        if totals.total_cost_usd > 0:
            totals.cost_efficiency_ratio = (
                totals.diagnostic_accuracy_top1 / (totals.total_cost_usd / 1000)
            )

    return results.results, totals


def _load_cases(
    dataset_path: str, max_cases: int | None
) -> list[NeuroBenchCase]:
    """Load NeuroBench cases."""
    cases_dir = Path(dataset_path) / "cases"
    case_files = sorted(cases_dir.glob("*.json"))
    if max_cases:
        case_files = case_files[:max_cases]
    return [
        NeuroBenchCase.model_validate(json.loads(cf.read_text()))
        for cf in case_files
        if cf.exists()
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned NeuroAgent")
    parser.add_argument("--adapter", help="Path to LoRA adapter checkpoint")
    parser.add_argument("--model", default="Qwen/Qwen3.5-9B", help="Base model name")
    parser.add_argument("--dataset", required=True, help="NeuroBench dataset path")
    parser.add_argument("--output", required=True, help="Results output JSON path")
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument("--base-url", default="http://localhost:8000/v1")
    parser.add_argument("--hospital", default="us_mayo")
    parser.add_argument("--reward-config", default="config/reward_weights.yaml")
    parser.add_argument("--tool-costs", default="config/tool_costs.yaml")
    parser.add_argument("--rules-dir", default="config/hospital_rules")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # If adapter provided, the model should be served with the adapter loaded
    # (e.g., vLLM --lora-modules neuroagent_adapter=checkpoints/grpo_final)
    model = args.model
    if args.adapter:
        logger.info("Adapter: %s (ensure vLLM is serving with --lora-modules)", args.adapter)

    config = AgentConfig(
        base_url=args.base_url,
        model=model,
        temperature=0.0,  # Deterministic for evaluation
    )

    reward_fn = CompositeReward.from_config(
        reward_config_path=args.reward_config,
        tool_costs_path=args.tool_costs,
        rules_dir=args.rules_dir,
        hospital=args.hospital,
    )
    cost_fn = CostReward(config_path=args.tool_costs)

    case_results, avg_metrics = evaluate_model(
        config=config,
        dataset_path=args.dataset,
        reward_fn=reward_fn,
        cost_fn=cost_fn,
        max_cases=args.max_cases,
        hospital=args.hospital,
    )

    # Save results
    output = {
        "model": model,
        "adapter": args.adapter,
        "hospital": args.hospital,
        "num_cases": len(case_results),
        "average_metrics": {
            "diagnostic_accuracy_top1": avg_metrics.diagnostic_accuracy_top1,
            "diagnostic_accuracy_top3": avg_metrics.diagnostic_accuracy_top3,
            "action_precision": avg_metrics.action_precision,
            "action_recall": avg_metrics.action_recall,
            "critical_actions_hit": avg_metrics.critical_actions_hit,
            "contraindicated_actions_taken": avg_metrics.contraindicated_actions_taken,
            "avg_tool_calls": avg_metrics.tool_call_count,
            "efficiency_score": avg_metrics.efficiency_score,
            "safety_score": avg_metrics.safety_score,
            "avg_cost_usd": avg_metrics.total_cost_usd,
            "avg_unnecessary_cost_usd": avg_metrics.unnecessary_cost_usd,
            "cost_efficiency_ratio": avg_metrics.cost_efficiency_ratio,
            "composite_reward": avg_metrics.composite_reward,
        },
        "per_case": [
            {
                "case_id": r.case_id,
                "condition": r.condition,
                "difficulty": r.difficulty,
                "metrics": r.metrics,
            }
            for r in case_results
        ],
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, default=str))
    logger.info("Results saved to %s", output_path)

    # Print summary
    print("\n=== Evaluation Summary ===")
    print(f"Cases: {len(case_results)}")
    print(f"Diagnostic Accuracy (Top-1): {avg_metrics.diagnostic_accuracy_top1:.1%}")
    print(f"Diagnostic Accuracy (Top-3): {avg_metrics.diagnostic_accuracy_top3:.1%}")
    print(f"Action Precision: {avg_metrics.action_precision:.1%}")
    print(f"Action Recall: {avg_metrics.action_recall:.1%}")
    print(f"Safety Score: {avg_metrics.safety_score:.3f}")
    print(f"Efficiency Score: {avg_metrics.efficiency_score:.3f}")
    print(f"Avg Tool Calls: {avg_metrics.tool_call_count:.1f}")
    print(f"Avg Cost (USD): ${avg_metrics.total_cost_usd:.0f}")
    print(f"Avg Unnecessary Cost: ${avg_metrics.unnecessary_cost_usd:.0f}")
    print(f"Cost Efficiency: {avg_metrics.cost_efficiency_ratio:.3f} accuracy/$1K")
    print(f"Composite Reward: {avg_metrics.composite_reward:.3f}")


if __name__ == "__main__":
    main()
