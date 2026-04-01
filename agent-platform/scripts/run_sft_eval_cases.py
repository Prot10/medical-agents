"""Evaluate a model on fold0 validation cases (60 cases) and optionally compare two runs.

Usage:
    # Run evaluation
    python agent-platform/scripts/run_sft_eval_cases.py \
        --model-id Qwen/Qwen3.5-9B \
        --run-name base-qwen3.5-9b \
        --output results/sft_eval/base_results.json

    # Compare two runs
    python agent-platform/scripts/run_sft_eval_cases.py \
        --compare \
        --base-results results/sft_eval/base_results.json \
        --sft-results results/sft_eval/sft_results.json \
        --output results/sft_eval/comparison.json
"""

from __future__ import annotations

import json
import logging
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
AGENT_PLATFORM = REPO_ROOT / "agent-platform"
sys.path.insert(0, str(AGENT_PLATFORM / "src"))
sys.path.insert(0, str(REPO_ROOT / "packages" / "neuroagent-schemas" / "src"))

from neuroagent_schemas import NeuroBenchCase

from neuroagent.agent.orchestrator import AgentConfig, AgentOrchestrator
from neuroagent.evaluation.metrics import MetricsCalculator
from neuroagent.evaluation.runner import format_patient_info
from neuroagent.rules.rules_engine import RulesEngine
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.tool_registry import ToolRegistry

app = typer.Typer()
console = Console()
logger = logging.getLogger("sft_eval")

DATASET_PATH = REPO_ROOT / "data" / "neurobench_v4"
SPLITS_DIR = DATASET_PATH / "splits"
FOLD0_VAL = SPLITS_DIR / "fold0_val.txt"


def load_fold0_val_cases() -> list[NeuroBenchCase]:
    """Load the 60 fold0 validation cases."""
    case_ids = FOLD0_VAL.read_text().strip().splitlines()
    cases_dir = DATASET_PATH / "cases"
    cases = []
    for cid in case_ids:
        path = cases_dir / f"{cid}.json"
        if path.exists():
            cases.append(NeuroBenchCase.model_validate(json.loads(path.read_text())))
        else:
            logger.warning("Case not found: %s", cid)
    return cases


def run_single_case(case: NeuroBenchCase, config: AgentConfig, hospital: str):
    """Run one case through the agent and compute metrics."""
    mock = MockServer(case)
    registry = ToolRegistry.create_default_registry(mock_server=mock)
    rules = RulesEngine(
        str(AGENT_PLATFORM / "config" / "hospital_rules"),
        hospital=hospital,
    )
    agent = AgentOrchestrator(
        config=config,
        tool_registry=registry,
        rules_engine=rules,
    )
    patient_info = format_patient_info(case)
    trace = agent.run(patient_info=patient_info, case_id=case.case_id)

    calculator = MetricsCalculator()
    metrics = calculator.compute_all(
        trace=trace,
        ground_truth=case.ground_truth,
        rules_engine=rules,
        condition=case.condition.value,
    )
    return trace, metrics


@dataclass
class CaseResult:
    case_id: str
    condition: str
    difficulty: str
    run_name: str
    repeat: int
    primary_diagnosis_gt: str
    agent_final_response: str
    diagnostic_accuracy_top1: bool
    diagnostic_accuracy_top3: bool
    critical_actions_hit: float
    safety_score: float
    tool_call_count: int
    tools_called: list[str]
    protocol_compliance: bool | None
    missing_required_steps: list[str]
    protocol_violations: list[str]
    elapsed_seconds: float
    total_tokens: int
    total_cost_usd: float = 0.0
    cost_efficiency: float = 0.0


@app.command()
def evaluate(
    model_id: str = typer.Option(..., help="Model ID for vLLM"),
    run_name: str = typer.Option(..., help="Name for this run"),
    hospital: str = typer.Option("de_charite", help="Hospital rule set"),
    repeats: int = typer.Option(3, help="Repeats per case"),
    output: str = typer.Option(..., help="Output JSON path"),
    port: int = typer.Option(8000, help="vLLM port"),
):
    """Run agent evaluation on fold0 validation set."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    cases = load_fold0_val_cases()
    console.print(f"\n[bold]Evaluating {run_name} on {len(cases)} fold0 val cases × {repeats} repeats[/bold]")

    config = AgentConfig(
        base_url=f"http://localhost:{port}/v1",
        api_key="not-needed",
        model=model_id,
        max_tokens=8192,
        temperature=1.0,
        top_p=0.95,
        presence_penalty=1.5,
        hospital=hospital,
    )

    all_results: list[CaseResult] = []
    checkpoint_file = Path(output).with_suffix(".checkpoint.json")
    completed: set[str] = set()

    if checkpoint_file.exists():
        ckpt = json.loads(checkpoint_file.read_text())
        completed = set(ckpt.get("completed", []))
        all_results = [CaseResult(**r) for r in ckpt.get("results", [])]
        console.print(f"[yellow]Resuming: {len(completed)} already done[/yellow]")

    total = len(cases) * repeats
    done = len(completed)

    for rep in range(1, repeats + 1):
        console.print(f"\n[bold]── Repeat {rep}/{repeats} ──[/bold]")
        for i, case in enumerate(cases):
            run_key = f"{run_name}|{case.case_id}|rep{rep}"
            if run_key in completed:
                continue

            done += 1
            console.print(
                f"  [{done}/{total}] {case.case_id} ({case.difficulty.value}) rep{rep}...",
                end=" ",
            )

            try:
                t0 = time.time()
                trace, metrics = run_single_case(case, config, hospital)
                elapsed = time.time() - t0

                result = CaseResult(
                    case_id=case.case_id,
                    condition=case.condition.value,
                    difficulty=case.difficulty.value,
                    run_name=run_name,
                    repeat=rep,
                    primary_diagnosis_gt=case.ground_truth.primary_diagnosis,
                    agent_final_response=trace.final_response or "",
                    diagnostic_accuracy_top1=metrics.diagnostic_accuracy_top1,
                    diagnostic_accuracy_top3=metrics.diagnostic_accuracy_top3,
                    critical_actions_hit=metrics.critical_actions_hit,
                    safety_score=metrics.safety_score,
                    tool_call_count=metrics.tool_call_count,
                    tools_called=trace.tools_called,
                    protocol_compliance=metrics.protocol_compliance,
                    missing_required_steps=metrics.missing_required_steps,
                    protocol_violations=metrics.protocol_violations,
                    elapsed_seconds=round(elapsed, 1),
                    total_tokens=trace.total_tokens,
                    total_cost_usd=round(metrics.total_cost_usd, 2),
                    cost_efficiency=round(metrics.cost_efficiency, 3),
                )
                all_results.append(result)
                completed.add(run_key)

                # Checkpoint
                checkpoint_file.write_text(json.dumps({
                    "completed": sorted(completed),
                    "results": [asdict(r) for r in all_results],
                }, default=str))

                dx = "✓" if metrics.diagnostic_accuracy_top1 else "✗"
                cost_str = f"${metrics.total_cost_usd:,.0f}"
                console.print(
                    f"dx={dx}  tools={metrics.tool_call_count}  "
                    f"safety={metrics.safety_score:.2f}  cost={cost_str}  "
                    f"{elapsed:.0f}s  {trace.total_tokens}tok"
                )

            except Exception as e:
                console.print(f"[red]FAILED: {e}[/red]")
                logger.exception("Case %s rep%d failed", case.case_id, rep)

    # Save final results
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "run_name": run_name,
        "model_id": model_id,
        "hospital": hospital,
        "repeats": repeats,
        "num_cases": len(cases),
        "num_results": len(all_results),
        "results": [asdict(r) for r in all_results],
    }, indent=2, default=str))

    # Print summary
    _print_summary(all_results, run_name)

    # Clean up checkpoint
    if checkpoint_file.exists():
        checkpoint_file.unlink()

    console.print(f"\n[green]Results saved to {output}[/green]")


@app.command()
def compare(
    base_results: str = typer.Option(..., help="Base model results JSON"),
    sft_results: str = typer.Option(..., help="SFT model results JSON"),
    output: str = typer.Option("results/sft_eval/comparison.json", help="Comparison output"),
):
    """Compare base vs SFT model results."""
    logging.basicConfig(level=logging.INFO)

    base = json.loads(Path(base_results).read_text())
    sft = json.loads(Path(sft_results).read_text())

    base_data = base["results"]
    sft_data = sft["results"]

    console.print(f"\n[bold]Comparing {base['run_name']} vs {sft['run_name']}[/bold]")
    console.print(f"  Base: {len(base_data)} results")
    console.print(f"  SFT:  {len(sft_data)} results")

    base_metrics = _compute_aggregate(base_data)
    sft_metrics = _compute_aggregate(sft_data)

    if not base_metrics or not sft_metrics:
        console.print("[red]Cannot compare: one or both result sets are empty.[/red]")
        raise typer.Exit(1)

    # Overall comparison table
    table = Table(title="Overall Comparison", show_lines=True)
    table.add_column("Metric", style="bold")
    table.add_column("Base", justify="right")
    table.add_column("SFT", justify="right")
    table.add_column("Δ", justify="right")

    for key, fmt in [
        ("top1_accuracy", ".1%"),
        ("top3_accuracy", ".1%"),
        ("critical_actions_hit", ".1%"),
        ("safety_score", ".3f"),
        ("avg_tool_calls", ".1f"),
        ("avg_cost_usd", ",.0f"),
        ("cost_efficiency", ".3f"),
    ]:
        bv = base_metrics[key]
        sv = sft_metrics[key]
        delta = sv - bv
        delta_str = f"{delta:+{fmt}}"
        if "accuracy" in key or "critical" in key or "safety" in key:
            color = "green" if delta > 0 else ("red" if delta < 0 else "")
        elif "cost_usd" in key:
            color = "green" if delta < 0 else ("red" if delta > 0 else "")
        else:
            color = ""
        if fmt.startswith(","):
            table.add_row(key, f"${bv:{fmt}}", f"${sv:{fmt}}", f"[{color}]{delta_str}[/]" if color else delta_str)
        else:
            table.add_row(key, f"{bv:{fmt}}", f"{sv:{fmt}}", f"[{color}]{delta_str}[/]" if color else delta_str)

    console.print(table)

    # Per-difficulty breakdown
    for diff in ["straightforward", "moderate", "diagnostic_puzzle"]:
        base_diff = [r for r in base_data if r["difficulty"] == diff]
        sft_diff = [r for r in sft_data if r["difficulty"] == diff]
        if base_diff and sft_diff:
            ba = sum(1 for r in base_diff if r["diagnostic_accuracy_top1"]) / len(base_diff)
            sa = sum(1 for r in sft_diff if r["diagnostic_accuracy_top1"]) / len(sft_diff)
            delta = sa - ba
            color = "green" if delta > 0 else ("red" if delta < 0 else "white")
            console.print(f"  {diff:20s}  base={ba:.0%}  sft={sa:.0%}  [{color}]Δ={delta:+.0%}[/]")

    # Per-condition breakdown
    console.print("\n[bold]Per-condition Top-1 Accuracy:[/bold]")
    conditions = sorted(set(r["condition"] for r in base_data))
    table2 = Table(show_lines=True)
    table2.add_column("Condition", style="bold")
    table2.add_column("Base", justify="right")
    table2.add_column("SFT", justify="right")
    table2.add_column("Δ", justify="right")

    for cond in conditions:
        bc = [r for r in base_data if r["condition"] == cond]
        sc = [r for r in sft_data if r["condition"] == cond]
        if bc and sc:
            ba = sum(1 for r in bc if r["diagnostic_accuracy_top1"]) / len(bc)
            sa = sum(1 for r in sc if r["diagnostic_accuracy_top1"]) / len(sc)
            delta = sa - ba
            color = "green" if delta > 0 else ("red" if delta < 0 else "")
            table2.add_row(cond, f"{ba:.0%}", f"{sa:.0%}", f"[{color}]{delta:+.0%}[/]" if color else f"{delta:+.0%}")

    console.print(table2)

    # Save comparison
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "base": {"run_name": base["run_name"], "metrics": base_metrics},
        "sft": {"run_name": sft["run_name"], "metrics": sft_metrics},
    }, indent=2, default=str))
    console.print(f"\n[green]Comparison saved to {output}[/green]")


def _compute_aggregate(results: list[dict]) -> dict:
    n = len(results)
    if n == 0:
        return {}
    return {
        "top1_accuracy": sum(1 for r in results if r["diagnostic_accuracy_top1"]) / n,
        "top3_accuracy": sum(1 for r in results if r["diagnostic_accuracy_top3"]) / n,
        "critical_actions_hit": sum(r["critical_actions_hit"] for r in results) / n,
        "safety_score": sum(r["safety_score"] for r in results) / n,
        "avg_tool_calls": sum(r["tool_call_count"] for r in results) / n,
        "avg_cost_usd": sum(r["total_cost_usd"] for r in results) / n,
        "cost_efficiency": sum(r["cost_efficiency"] for r in results) / n,
    }


def _print_summary(results: list[CaseResult], run_name: str):
    n = len(results)
    if n == 0:
        console.print("[red]No results[/red]")
        return

    top1 = sum(1 for r in results if r.diagnostic_accuracy_top1) / n
    top3 = sum(1 for r in results if r.diagnostic_accuracy_top3) / n
    crit = sum(r.critical_actions_hit for r in results) / n
    safety = sum(r.safety_score for r in results) / n
    tools = sum(r.tool_call_count for r in results) / n
    cost = sum(r.total_cost_usd for r in results) / n
    cost_eff = sum(r.cost_efficiency for r in results) / n

    console.print(f"\n[bold]=== {run_name} Summary ({n} results) ===[/bold]")
    console.print(f"  Top-1 Accuracy:   {top1:.1%}")
    console.print(f"  Top-3 Accuracy:   {top3:.1%}")
    console.print(f"  Critical Actions: {crit:.1%}")
    console.print(f"  Safety Score:     {safety:.3f}")
    console.print(f"  Avg Tool Calls:   {tools:.1f}")
    console.print(f"  Avg Cost (USD):   ${cost:,.0f}")
    console.print(f"  Cost Efficiency:  {cost_eff:.3f}")


if __name__ == "__main__":
    app()
