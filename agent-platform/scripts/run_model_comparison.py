"""Compare different LLM models on the same NeuroBench case(s)."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

app = typer.Typer()
console = Console()


@dataclass
class ModelEndpoint:
    name: str
    base_url: str
    model: str


# Pre-configured model endpoints (match serve_model.sh)
MODELS = {
    "qwen3.5-27b-awq": ModelEndpoint(
        name="Qwen3.5-27B-AWQ",
        base_url="http://localhost:8000/v1",
        model="QuantTrio/Qwen3.5-27B-AWQ",
    ),
    "qwen3.5-27b-fp8": ModelEndpoint(
        name="Qwen3.5-27B-FP8",
        base_url="http://localhost:8000/v1",
        model="Qwen/Qwen3.5-27B-FP8",
    ),
    "medgemma-27b": ModelEndpoint(
        name="MedGemma-27B-Text",
        base_url="http://localhost:8001/v1",
        model="unsloth/medgemma-27b-text-it-GGUF:Q4_K_M",
    ),
    "medgemma-4b": ModelEndpoint(
        name="MedGemma-1.5-4B",
        base_url="http://localhost:8001/v1",
        model="google/medgemma-1.5-4b-it",
    ),
    "openbio-8b": ModelEndpoint(
        name="OpenBioLLM-8B",
        base_url="http://localhost:8002/v1",
        model="aaditya/Llama3-OpenBioLLM-8B",
    ),
}


@app.command()
def compare(
    case_file: str = typer.Argument(
        default="agent-platform/tests/fixtures/sample_case.json",
        help="Path to NeuroBenchCase JSON",
    ),
    models: str = typer.Option(
        "qwen3.5-27b-awq",
        help="Comma-separated model names (or 'all')",
    ),
    output_file: str = typer.Option(
        "results/model_comparison.json",
        help="Output file for results",
    ),
    enable_rules: bool = typer.Option(True, help="Enable hospital rules"),
    rules_dir: str = typer.Option("agent-platform/config/hospital_rules"),
) -> None:
    """Run the same case against multiple models and compare results."""
    logging.basicConfig(
        level=logging.INFO,
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )

    from neuroagent_schemas import NeuroBenchCase
    from neuroagent.agent.orchestrator import AgentConfig
    from neuroagent.evaluation.runner import EvaluationRunner
    from neuroagent.evaluation.metrics import MetricsCalculator

    # Load case
    case_data = json.loads(Path(case_file).read_text())
    case = NeuroBenchCase.model_validate(case_data)
    console.print(f"[bold]Case:[/bold] {case.case_id} — {case.condition.value} ({case.difficulty.value})")
    console.print(f"[bold]Ground truth:[/bold] {case.ground_truth.primary_diagnosis}\n")

    # Determine which models to test
    if models == "all":
        model_list = list(MODELS.values())
    else:
        model_names = [m.strip() for m in models.split(",")]
        model_list = []
        for name in model_names:
            if name in MODELS:
                model_list.append(MODELS[name])
            else:
                # Custom endpoint: name=base_url:model_id
                if "=" in name:
                    parts = name.split("=", 1)
                    url_model = parts[1].rsplit(":", 1)
                    model_list.append(ModelEndpoint(
                        name=parts[0],
                        base_url=url_model[0],
                        model=url_model[1] if len(url_model) > 1 else parts[0],
                    ))
                else:
                    console.print(f"[red]Unknown model: {name}[/red]")
                    raise typer.Exit(1)

    # Run each model
    results = {}
    calculator = MetricsCalculator()

    for endpoint in model_list:
        console.print(f"\n[bold cyan]Testing: {endpoint.name}[/bold cyan]")
        console.print(f"  URL: {endpoint.base_url}, Model: {endpoint.model}")

        try:
            config = AgentConfig(
                base_url=endpoint.base_url,
                api_key="not-needed",
                model=endpoint.model,
            )

            runner = EvaluationRunner(config=config, dataset_path="")
            trace = runner.run_single_case(
                case, enable_rules=enable_rules, rules_dir=rules_dir,
            )

            metrics = calculator.compute_all(trace, case.ground_truth)

            results[endpoint.name] = {
                "model": endpoint.model,
                "tools_called": trace.tools_called,
                "total_tool_calls": trace.total_tool_calls,
                "time_seconds": round(trace.elapsed_time_seconds, 1),
                "total_tokens": trace.total_tokens,
                "diagnostic_accuracy_top1": metrics.diagnostic_accuracy_top1,
                "diagnostic_accuracy_top3": metrics.diagnostic_accuracy_top3,
                "action_recall": round(metrics.action_recall, 2),
                "critical_actions_hit": round(metrics.critical_actions_hit, 2),
                "safety_score": round(metrics.safety_score, 2),
                "final_response_preview": (trace.final_response or "")[:300],
            }

            console.print(f"  [green]OK[/green] — {trace.total_tool_calls} tools, "
                          f"{trace.elapsed_time_seconds:.1f}s, "
                          f"top1={'Y' if metrics.diagnostic_accuracy_top1 else 'N'}")

        except Exception as e:
            console.print(f"  [red]FAILED: {e}[/red]")
            results[endpoint.name] = {"error": str(e)}

    # Print comparison table
    console.print("\n")
    table = Table(title="Model Comparison Results")
    table.add_column("Model", style="cyan")
    table.add_column("Tools", justify="right")
    table.add_column("Time(s)", justify="right")
    table.add_column("Top-1", justify="center")
    table.add_column("Top-3", justify="center")
    table.add_column("Action Recall", justify="right")
    table.add_column("Safety", justify="right")

    for name, r in results.items():
        if "error" in r:
            table.add_row(name, "ERR", "-", "-", "-", "-", "-")
        else:
            table.add_row(
                name,
                str(r["total_tool_calls"]),
                str(r["time_seconds"]),
                "[green]Y[/green]" if r["diagnostic_accuracy_top1"] else "[red]N[/red]",
                "[green]Y[/green]" if r["diagnostic_accuracy_top3"] else "[red]N[/red]",
                str(r["action_recall"]),
                str(r["safety_score"]),
            )

    console.print(table)

    # Save results
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    console.print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    app()
