"""Debug: run agent on a single case and print the full trace."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel

app = typer.Typer()
console = Console()


@app.command()
def run(
    case_file: str = typer.Argument(help="Path to a NeuroBenchCase JSON file"),
    model: str = typer.Option("Qwen/Qwen3-32B", help="Orchestrator model name"),
    base_url: str = typer.Option("http://localhost:8000/v1", help="LLM API base URL"),
    api_key: str = typer.Option("not-needed", help="API key"),
    enable_rules: bool = typer.Option(True, help="Enable hospital rules"),
    rules_dir: str = typer.Option("config/hospital_rules", help="Hospital rules directory"),
    hospital: str = typer.Option("us_mayo", help="Hospital rule set: us_mayo, uk_nhs, de_charite, jp_todai, br_hcfmusp"),
) -> None:
    """Run NeuroAgent on a single case and display the reasoning trace."""
    logging.basicConfig(
        level=logging.INFO,
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )

    from neuroagent_schemas import NeuroBenchCase
    from neuroagent.agent.orchestrator import AgentConfig
    from neuroagent.evaluation.runner import EvaluationRunner

    # Load case
    case_data = json.loads(Path(case_file).read_text())
    case = NeuroBenchCase.model_validate(case_data)

    console.print(Panel(
        f"[bold]{case.case_id}[/bold]\n"
        f"Condition: {case.condition.value}\n"
        f"Difficulty: {case.difficulty.value}\n"
        f"Patient: {case.patient.demographics.age}yo {case.patient.demographics.sex}\n"
        f"Chief complaint: {case.patient.chief_complaint}",
        title="Case Details",
    ))

    config = AgentConfig(base_url=base_url, api_key=api_key, model=model)
    runner = EvaluationRunner(config=config, dataset_path="")

    trace = runner.run_single_case(case, enable_rules=enable_rules, rules_dir=rules_dir, hospital=hospital)

    # Display trace
    console.print("\n[bold]Agent Reasoning Trace[/bold]\n")
    for turn in trace.turns:
        if turn.role == "assistant" and turn.content:
            console.print(Panel(turn.content, title=f"Turn {turn.turn_number} — Agent"))
        if turn.tool_calls:
            for tc in turn.tool_calls:
                console.print(f"  [cyan]→ Tool Call:[/cyan] {tc}")
        if turn.tool_results:
            for tr in turn.tool_results:
                tr_str = json.dumps(tr, indent=2, default=str)
                if len(tr_str) > 500:
                    tr_str = tr_str[:500] + "..."
                console.print(f"  [green]← Tool Result:[/green] {tr_str}")

    if trace.final_response:
        console.print(Panel(trace.final_response, title="Final Assessment", border_style="green"))

    console.print(f"\n[bold]Summary:[/bold] {trace.total_tool_calls} tool calls, "
                  f"{trace.elapsed_time_seconds:.1f}s, {trace.total_tokens} tokens")

    # Compare with ground truth
    console.print(Panel(
        f"[bold]Expected:[/bold] {case.ground_truth.primary_diagnosis}\n"
        f"[bold]ICD:[/bold] {case.ground_truth.icd_code}",
        title="Ground Truth",
        border_style="yellow",
    ))


if __name__ == "__main__":
    app()
