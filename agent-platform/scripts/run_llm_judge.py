#!/usr/bin/env python3
"""Batch LLM-judge evaluation on saved v4 comparison results.

Loads the comparison traces and runs each through the LLM judge rubric (8
dimensions + composite) using a vLLM or OpenAI-compatible endpoint.

The judge evaluates reasoning quality, evidence integration, tool efficiency,
clinical safety, and diagnostic accuracy — providing scores that complement
the rule-based metrics from the comparison run.

Usage:
    # Requires a running vLLM server (or OpenAI-compatible endpoint)
    uv run python agent-platform/scripts/run_llm_judge.py
    uv run python agent-platform/scripts/run_llm_judge.py --judge-model Qwen/Qwen3.5-9B
    uv run python agent-platform/scripts/run_llm_judge.py --results-dir results/v4_comparison --run qwen27b-react
    uv run python agent-platform/scripts/run_llm_judge.py --max-cases 10  # quick test
"""

from __future__ import annotations

import json
import logging
import sys
import time
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn
from rich.table import Table

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "agent-platform" / "src"))
sys.path.insert(0, str(REPO_ROOT / "packages" / "neuroagent-schemas" / "src"))

from neuroagent_schemas import NeuroBenchCase
from neuroagent.agent.reasoning import AgentTrace, AgentTurn
from neuroagent.evaluation.llm_judge import LLMJudge, ReasoningScore
from neuroagent.llm.client import LLMClient

app = typer.Typer()
console = Console()
logger = logging.getLogger("llm_judge")

V4_CASES_DIR = REPO_ROOT / "data" / "neurobench_v4" / "cases"


def load_case(case_id: str) -> NeuroBenchCase:
    path = V4_CASES_DIR / f"{case_id}.json"
    return NeuroBenchCase(**json.loads(path.read_text()))


def reconstruct_trace(trace_data: dict, result_data: dict) -> AgentTrace:
    """Reconstruct an AgentTrace from saved comparison data.

    The saved traces have truncated content (500 chars) but full tool call
    arguments and full final_response. We reconstruct as much as possible.
    """
    trace = AgentTrace(case_id=result_data.get("case_id"))
    trace.total_tokens = trace_data.get("total_tokens", 0)
    trace.total_tool_calls = result_data.get("tool_call_count", 0)
    trace.tools_called = result_data.get("tools_called", [])
    trace.final_response = trace_data.get("final_response") or result_data.get("agent_final_response", "")

    for turn in trace_data.get("turns", []):
        t = AgentTurn(
            turn_number=turn.get("turn", 0),
            role=turn.get("role", "assistant"),
            content=turn.get("content"),
            tool_calls=turn.get("tool_calls"),
        )
        trace.turns.append(t)

    return trace


@app.command()
def main(
    results_dir: str = typer.Option("results/v4_comparison", help="Results directory"),
    judge_base_url: str = typer.Option("http://localhost:8000/v1", help="Judge LLM endpoint"),
    judge_model: str = typer.Option("", help="Judge model ID (auto-detect if empty)"),
    judge_api_key: str = typer.Option("not-needed", help="API key for judge endpoint"),
    run: str = typer.Option("", help="Specific run to evaluate (e.g. qwen27b-react). Empty = all react runs."),
    max_cases: int = typer.Option(0, help="Max cases to evaluate per run (0 = all)"),
    repeat: int = typer.Option(1, help="Which repeat to evaluate (1-3, default 1)"),
    output_name: str = typer.Option("llm_judge_scores", help="Output filename prefix"),
):
    """Run LLM-judge evaluation on saved v4 comparison traces."""

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

    results_path = REPO_ROOT / results_dir

    # Auto-detect judge model from vLLM
    if not judge_model:
        try:
            import urllib.request
            resp = urllib.request.urlopen(f"{judge_base_url.rstrip('/').replace('/v1', '')}/v1/models")
            models_data = json.loads(resp.read())
            judge_model = models_data["data"][0]["id"]
            console.print(f"[green]Auto-detected judge model: {judge_model}[/green]")
        except Exception as e:
            console.print(f"[red]Cannot auto-detect model. Is vLLM running at {judge_base_url}?[/red]")
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(1)

    # Load merged results
    merged = json.loads((results_path / "merged_results.json").read_text())
    all_results = merged["results"]

    # Select runs to evaluate
    react_runs = sorted(set(r["run_name"] for r in all_results if r["mode"] == "react"))
    if run:
        runs_to_eval = [run]
    else:
        runs_to_eval = react_runs

    console.print(f"[bold]LLM Judge Evaluation[/bold]")
    console.print(f"  Judge model: {judge_model}")
    console.print(f"  Endpoint: {judge_base_url}")
    console.print(f"  Runs to evaluate: {runs_to_eval}")
    console.print(f"  Repeat: {repeat}")
    if max_cases:
        console.print(f"  Max cases per run: {max_cases}")

    # Load trace files
    trace_files = {}
    for subdir in ["qwen3.5-9b", "qwen3.5-27b-awq", "medgemma-4b"]:
        tf = results_path / subdir / "traces.json"
        if tf.exists():
            trace_files[subdir] = json.loads(tf.read_text())

    # Map run_name to trace file subdir
    run_to_subdir = {}
    for r in all_results:
        model = r["model"]
        run_name = r["run_name"]
        if model == "qwen3.5-9b":
            run_to_subdir[run_name] = "qwen3.5-9b"
        elif model == "qwen3.5-27b-awq":
            run_to_subdir[run_name] = "qwen3.5-27b-awq"
        elif model == "medgemma-4b":
            run_to_subdir[run_name] = "medgemma-4b"

    # Initialize judge
    llm = LLMClient(
        base_url=judge_base_url,
        api_key=judge_api_key,
        model=judge_model,
        temperature=0.0,
        max_tokens=4096,
    )
    judge = LLMJudge(llm)

    # Checkpoint support
    out_dir = results_path / "analysis"
    out_dir.mkdir(exist_ok=True)
    checkpoint_file = out_dir / f"{output_name}_checkpoint.json"
    completed: set[str] = set()
    all_scores: list[dict] = []
    if checkpoint_file.exists():
        ckpt = json.loads(checkpoint_file.read_text())
        completed = set(ckpt.get("completed", []))
        all_scores = ckpt.get("scores", [])
        console.print(f"[yellow]Resuming from checkpoint: {len(completed)} already done[/yellow]")

    # Evaluate
    for run_name in runs_to_eval:
        subdir = run_to_subdir.get(run_name)
        if not subdir or subdir not in trace_files:
            console.print(f"[yellow]No traces for {run_name}, skipping[/yellow]")
            continue

        traces = trace_files[subdir].get(run_name, {})
        run_results = [
            r for r in all_results
            if r["run_name"] == run_name and r["repeat"] == repeat
        ]

        if max_cases:
            run_results = run_results[:max_cases]

        console.print(f"\n[bold cyan]═══ {run_name} ({len(run_results)} cases) ═══[/bold cyan]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(f"Judging {run_name}", total=len(run_results))

            for r in run_results:
                case_id = r["case_id"]
                trace_key = f"{case_id}_rep{repeat}"
                judge_key = f"{run_name}|{case_id}|rep{repeat}"

                if judge_key in completed:
                    progress.advance(task)
                    continue

                trace_data = traces.get(trace_key)
                if not trace_data:
                    progress.advance(task)
                    continue

                try:
                    case = load_case(case_id)
                    trace = reconstruct_trace(trace_data, r)
                    t0 = time.time()
                    score = judge.judge(trace, case)
                    elapsed = time.time() - t0

                    entry = {
                        "case_id": case_id,
                        "run_name": run_name,
                        "condition": r["condition"],
                        "difficulty": r["difficulty"],
                        "repeat": repeat,
                        "diagnostic_accuracy_top1": r["diagnostic_accuracy_top1"],
                        "total_cost_usd": r.get("total_cost_usd", 0),
                        **asdict(score),
                        "judge_time_s": round(elapsed, 1),
                        "judge_model": judge_model,
                    }
                    all_scores.append(entry)
                    completed.add(judge_key)

                    # Checkpoint after each case
                    with open(checkpoint_file, "w") as f:
                        json.dump({"completed": sorted(completed), "scores": all_scores}, f, indent=2, default=str)

                    progress.console.print(
                        f"  {case_id:18s} composite={score.composite_score:.2f} "
                        f"dx={score.diagnostic_accuracy}/5 safety={score.clinical_safety}/5 "
                        f"tools={score.tool_efficiency}/5 ({elapsed:.0f}s)"
                    )

                except Exception as e:
                    progress.console.print(f"  [red]{case_id}: {e}[/red]")
                    logger.exception("Judge failed for %s", case_id)

                progress.advance(task)

    if not all_scores:
        console.print("[yellow]No scores generated.[/yellow]")
        raise typer.Exit(0)

    # -----------------------------------------------------------------------
    # Save and summarize
    # -----------------------------------------------------------------------
    scores_file = out_dir / f"{output_name}.json"
    with open(scores_file, "w") as f:
        json.dump(all_scores, f, indent=2, default=str)
    console.print(f"\n[green]Scores saved to {scores_file}[/green]")

    # Print summary tables
    console.print(f"\n{'='*80}")
    console.print("[bold]LLM JUDGE EVALUATION SUMMARY[/bold]")
    console.print(f"{'='*80}\n")

    # Per-run summary
    by_run: dict[str, list[dict]] = defaultdict(list)
    for s in all_scores:
        by_run[s["run_name"]].append(s)

    table = Table(title="Judge Scores by Run", show_lines=True)
    table.add_column("Run", style="bold")
    table.add_column("N", justify="right")
    table.add_column("Composite", justify="right")
    table.add_column("Dx Acc", justify="right")
    table.add_column("Evidence", justify="right")
    table.add_column("Integr", justify="right")
    table.add_column("Diff Dx", justify="right")
    table.add_column("Tools", justify="right")
    table.add_column("Safety", justify="right")
    table.add_column("Uncert", justify="right")

    import statistics
    for rn in sorted(by_run):
        scores = by_run[rn]
        n = len(scores)
        def mean(key): return round(statistics.mean(s[key] for s in scores), 2)
        table.add_row(
            rn, str(n),
            f"{mean('composite_score'):.2f}",
            f"{mean('diagnostic_accuracy'):.1f}",
            f"{mean('evidence_identification'):.1f}",
            f"{mean('evidence_integration'):.1f}",
            f"{mean('differential_reasoning'):.1f}",
            f"{mean('tool_efficiency'):.1f}",
            f"{mean('clinical_safety'):.1f}",
            f"{mean('uncertainty_calibration'):.1f}",
        )
    console.print(table)

    # Per-condition summary
    by_cond: dict[str, list[dict]] = defaultdict(list)
    for s in all_scores:
        by_cond[s["condition"]].append(s)

    table = Table(title="Judge Scores by Condition", show_lines=True)
    table.add_column("Condition", style="bold", width=25)
    table.add_column("N", justify="right")
    table.add_column("Composite", justify="right")
    table.add_column("Dx Acc", justify="right")
    table.add_column("Safety", justify="right")
    table.add_column("Tools", justify="right")

    for cond in sorted(by_cond):
        scores = by_cond[cond]
        n = len(scores)
        def mean(key): return round(statistics.mean(s[key] for s in scores), 2)
        table.add_row(
            cond, str(n),
            f"{mean('composite_score'):.2f}",
            f"{mean('diagnostic_accuracy'):.1f}",
            f"{mean('clinical_safety'):.1f}",
            f"{mean('tool_efficiency'):.1f}",
        )
    console.print(table)

    # Most common critical errors
    all_errors = []
    for s in all_scores:
        all_errors.extend(s.get("critical_errors", []))
    if all_errors:
        console.print(f"\n[bold red]Critical Errors ({len(all_errors)} total):[/bold red]")
        from collections import Counter
        for err, count in Counter(all_errors).most_common(10):
            console.print(f"  {count}x {err[:100]}")

    # Most common strengths/weaknesses
    all_strengths = []
    all_weaknesses = []
    for s in all_scores:
        all_strengths.extend(s.get("strengths", []))
        all_weaknesses.extend(s.get("weaknesses", []))
    if all_strengths:
        console.print(f"\n[bold green]Top Strengths ({len(all_strengths)} total):[/bold green]")
        from collections import Counter
        for s, count in Counter(all_strengths).most_common(5):
            console.print(f"  {count}x {s[:100]}")
    if all_weaknesses:
        console.print(f"\n[bold yellow]Top Weaknesses ({len(all_weaknesses)} total):[/bold yellow]")
        for w, count in Counter(all_weaknesses).most_common(5):
            console.print(f"  {count}x {w[:100]}")

    console.print(f"\n[bold]Done. {len(all_scores)} cases evaluated by LLM judge.[/bold]")


if __name__ == "__main__":
    app()
