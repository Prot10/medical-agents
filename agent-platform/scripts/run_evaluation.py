"""Main entry point: run agent evaluation on NeuroBench dataset."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler

app = typer.Typer()
console = Console()


@app.command()
def evaluate(
    model: str = typer.Option("Qwen/Qwen3.5-9B", help="Model name (must match vLLM --model)"),
    base_url: str = typer.Option("http://localhost:8000/v1", help="LLM API base URL"),
    api_key: str = typer.Option("not-needed", help="API key"),
    dataset: str = typer.Option("data/neurobench_v1", help="Dataset path"),
    split: str = typer.Option("test", help="Dataset split"),
    output_dir: str = typer.Option("results/", help="Output directory"),
    max_cases: int = typer.Option(None, help="Limit number of cases"),
    enable_memory: bool = typer.Option(False, help="Enable patient memory"),
    enable_rules: bool = typer.Option(True, help="Enable hospital rules"),
    rules_dir: str = typer.Option("config/hospital_rules", help="Hospital rules directory"),
    hospital: str = typer.Option("us_mayo", help="Hospital rule set: us_mayo, uk_nhs, de_charite, jp_todai, br_hcfmusp"),
) -> None:
    """Run NeuroAgent evaluation on NeuroBench cases."""
    logging.basicConfig(
        level=logging.INFO,
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )

    from neuroagent.agent.orchestrator import AgentConfig
    from neuroagent.evaluation.runner import EvaluationRunner
    from neuroagent.evaluation.metrics import MetricsCalculator
    from neuroagent.evaluation.analyzer import ResultsAnalyzer

    config = AgentConfig(
        base_url=base_url,
        api_key=api_key,
        model=model,
    )

    runner = EvaluationRunner(config=config, dataset_path=dataset)

    console.print(f"[bold]Running evaluation on {dataset} ({split} split)[/bold]")
    console.print(f"Model: {model}")
    console.print(f"Memory: {enable_memory}, Rules: {enable_rules}, Hospital: {hospital}")

    results = runner.run_evaluation(
        split=split,
        max_cases=max_cases,
        enable_memory=enable_memory,
        enable_rules=enable_rules,
        rules_dir=rules_dir,
        hospital=hospital,
    )

    # Compute metrics for each case
    calculator = MetricsCalculator()
    for case_result in results.results:
        # Load ground truth from case file
        case_file = Path(dataset) / "cases" / f"{case_result.case_id}.json"
        if case_file.exists():
            from neuroagent_schemas import NeuroBenchCase
            case_data = json.loads(case_file.read_text())
            case = NeuroBenchCase.model_validate(case_data)
            metrics = calculator.compute_all(case_result.trace, case.ground_truth)
            case_result.metrics = {
                "diagnostic_accuracy_top1": metrics.diagnostic_accuracy_top1,
                "diagnostic_accuracy_top3": metrics.diagnostic_accuracy_top3,
                "action_precision": metrics.action_precision,
                "action_recall": metrics.action_recall,
                "critical_actions_hit": metrics.critical_actions_hit,
                "contraindicated_actions_taken": metrics.contraindicated_actions_taken,
                "efficiency_score": metrics.efficiency_score,
                "safety_score": metrics.safety_score,
            }

    # Generate summary
    analyzer = ResultsAnalyzer()
    summary = analyzer.generate_main_table(results)

    console.print("\n[bold]Results Summary[/bold]")
    console.print(summary)

    # Save results
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    results_file = out_path / f"eval_{model.replace('/', '_')}_{split}.json"
    with open(results_file, "w") as f:
        json.dump(
            {
                "config": results.config,
                "num_cases": results.num_cases,
                "results": [
                    {
                        "case_id": r.case_id,
                        "condition": r.condition,
                        "difficulty": r.difficulty,
                        "metrics": r.metrics,
                        "tool_calls": r.trace.total_tool_calls,
                        "tools_called": r.trace.tools_called,
                    }
                    for r in results.results
                ],
            },
            f,
            indent=2,
        )

    console.print(f"\nResults saved to {results_file}")


if __name__ == "__main__":
    app()
