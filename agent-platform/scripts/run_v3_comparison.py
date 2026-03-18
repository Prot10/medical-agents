"""NeuroBench comparison: multi-model, multi-seed evaluation with cost tracking.

Runs selected cases across model/mode configurations with N repeats (different
temperature seeds) to measure diagnostic consistency. Supports v3 (7-tool) and
v4 (12-tool + cost tracking) datasets.

Usage:
    uv run python agent-platform/scripts/run_v3_comparison.py --dataset v4
    uv run python agent-platform/scripts/run_v3_comparison.py --cases-per-difficulty 30 --repeats 3
    uv run python agent-platform/scripts/run_v3_comparison.py --hospital us_mayo
"""

from __future__ import annotations

import json
import logging
import random
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
AGENT_PLATFORM = REPO_ROOT / "agent-platform"
sys.path.insert(0, str(AGENT_PLATFORM / "src"))
sys.path.insert(0, str(REPO_ROOT / "packages" / "neuroagent-schemas" / "src"))

from neuroagent_schemas import GroundTruth, NeuroBenchCase

from neuroagent.agent.orchestrator import AgentConfig, AgentOrchestrator
from neuroagent.agent.reasoning import AgentTrace
from neuroagent.evaluation.metrics import CaseMetrics, MetricsCalculator
from neuroagent.evaluation.runner import format_patient_info
from neuroagent.rules.rules_engine import RulesEngine
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.tool_registry import ToolRegistry

app = typer.Typer()
console = Console()
logger = logging.getLogger("v3_comparison")

# ---------------------------------------------------------------------------
# Model definitions
# ---------------------------------------------------------------------------
MODELS = {
    "qwen3.5-9b": {
        "model_id": "Qwen/Qwen3.5-9B",
        "max_tokens": 8192,
        "supports_tools": True,
    },
    "qwen3.5-27b-awq": {
        "model_id": "QuantTrio/Qwen3.5-27B-AWQ",
        "max_tokens": 8192,
        "supports_tools": True,
    },
    "medgemma-4b": {
        "model_id": "google/medgemma-1.5-4b-it",
        "max_tokens": 8192,
        "supports_tools": False,
    },
}


# ---------------------------------------------------------------------------
# Run configurations
# ---------------------------------------------------------------------------
@dataclass
class RunConfig:
    name: str
    model_key: str
    model_id: str
    max_tokens: int
    mode: str  # "react" or "no_tools"
    hospital: str


# ---------------------------------------------------------------------------
# Case selection
# ---------------------------------------------------------------------------
def select_cases(
    dataset_path: Path,
    cases_per_difficulty: int,
    seed: int,
) -> list[NeuroBenchCase]:
    """Select N cases per difficulty level, balanced across conditions."""
    cases_dir = dataset_path / "cases"
    all_cases: list[NeuroBenchCase] = []
    for f in sorted(cases_dir.glob("*.json")):
        data = json.loads(f.read_text())
        all_cases.append(NeuroBenchCase.model_validate(data))

    # Group by difficulty
    by_difficulty: dict[str, list[NeuroBenchCase]] = defaultdict(list)
    for c in all_cases:
        by_difficulty[c.difficulty.value].append(c)

    rng = random.Random(seed)
    selected: list[NeuroBenchCase] = []
    for diff in ["straightforward", "moderate", "diagnostic_puzzle"]:
        pool = by_difficulty.get(diff, [])
        # Shuffle deterministically then pick N, trying to get different conditions
        rng.shuffle(pool)
        # Greedy: pick from different conditions first
        seen_conditions: set[str] = set()
        picks: list[NeuroBenchCase] = []
        # First pass: one per condition
        for c in pool:
            if c.condition.value not in seen_conditions and len(picks) < cases_per_difficulty:
                picks.append(c)
                seen_conditions.add(c.condition.value)
        # Second pass: fill remaining
        for c in pool:
            if c not in picks and len(picks) < cases_per_difficulty:
                picks.append(c)
        selected.extend(picks)

    return selected


# ---------------------------------------------------------------------------
# Single case runner
# ---------------------------------------------------------------------------
def run_single_case(
    case: NeuroBenchCase,
    run_config: RunConfig,
) -> tuple[AgentTrace, CaseMetrics]:
    """Run a single case with the given configuration."""

    config = AgentConfig(
        base_url="http://localhost:8000/v1",
        api_key="not-needed",
        model=run_config.model_id,
        max_tokens=run_config.max_tokens,
        temperature=1.0,
        top_p=0.95,
        presence_penalty=1.5,
        hospital=run_config.hospital,
    )

    # Fresh mock server and tools per case
    mock = MockServer(case)
    registry = ToolRegistry.create_default_registry(mock_server=mock)
    rules = RulesEngine(
        str(AGENT_PLATFORM / "config" / "hospital_rules"),
        hospital=run_config.hospital,
    )
    agent = AgentOrchestrator(
        config=config,
        tool_registry=registry,
        rules_engine=rules,
    )

    # Format patient info (centralized function — single source of truth)
    patient_info = format_patient_info(case)

    # Run based on mode
    if run_config.mode == "react":
        trace = agent.run(patient_info=patient_info, case_id=case.case_id)
    else:
        # no_tools mode: single-shot, no tool outputs
        trace = agent.run_all_info_upfront(
            patient_info=patient_info,
            tool_outputs_text="",  # no tool results — diagnose from clinical info alone
            case_id=case.case_id,
        )

    # Compute metrics
    calculator = MetricsCalculator()
    metrics = calculator.compute_all(
        trace=trace,
        ground_truth=case.ground_truth,
        rules_engine=rules,
        condition=case.condition.value,
    )

    return trace, metrics



# _format_initial_info removed — use format_patient_info from evaluation.runner


# ---------------------------------------------------------------------------
# Results container
# ---------------------------------------------------------------------------
@dataclass
class CaseResult:
    case_id: str
    condition: str
    difficulty: str
    run_name: str
    model: str
    mode: str
    hospital: str
    repeat: int  # 1-indexed repeat number
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


# ---------------------------------------------------------------------------
# Main comparison
# ---------------------------------------------------------------------------
@app.command()
def main(
    hospital: str = typer.Option("de_charite", help="Hospital rule set"),
    cases_per_difficulty: int = typer.Option(5, help="Cases per difficulty level"),
    seed: int = typer.Option(42, help="Random seed for case selection"),
    repeats: int = typer.Option(3, help="Number of repeats per case (different seeds)"),
    dataset: str = typer.Option("v3", help="Dataset version: v1 or v3"),
    output_dir: str = typer.Option(
        "results/v3_comparison", help="Output directory for results"
    ),
    skip_model: list[str] = typer.Option(
        [], help="Model keys to skip (e.g., --skip-model medgemma-4b)"
    ),
):
    """Run NeuroBench v3 comparison with N repeats per case for consistency measurement.

    v3 dataset contains 200 cases: 100 from v1 (synthetic) + 100 from v2 (real-case-seeded).
    Case selection draws from both pools.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    dataset_path = REPO_ROOT / "data" / f"neurobench_{dataset}"
    if not dataset_path.exists():
        console.print(f"[red]Dataset not found: {dataset_path}[/red]")
        raise typer.Exit(1)

    out_path = REPO_ROOT / output_dir
    out_path.mkdir(parents=True, exist_ok=True)

    # --- Select cases ---
    console.print(f"\n[bold]Selecting {cases_per_difficulty} cases per difficulty (seed={seed})...[/bold]")
    cases = select_cases(dataset_path, cases_per_difficulty, seed)
    console.print(f"Selected {len(cases)} cases:")
    for c in cases:
        console.print(f"  {c.case_id} ({c.difficulty.value}, {c.condition.value})")

    # --- Define run configurations ---
    runs: list[RunConfig] = []

    if "qwen3.5-9b" not in skip_model:
        runs.append(RunConfig(
            name="qwen3.5-react",
            model_key="qwen3.5-9b",
            model_id=MODELS["qwen3.5-9b"]["model_id"],
            max_tokens=MODELS["qwen3.5-9b"]["max_tokens"],
            mode="react",
            hospital=hospital,
        ))
        runs.append(RunConfig(
            name="qwen3.5-no-tools",
            model_key="qwen3.5-9b",
            model_id=MODELS["qwen3.5-9b"]["model_id"],
            max_tokens=MODELS["qwen3.5-9b"]["max_tokens"],
            mode="no_tools",
            hospital=hospital,
        ))

    if "medgemma-4b" not in skip_model:
        runs.append(RunConfig(
            name="medgemma-no-tools",
            model_key="medgemma-4b",
            model_id=MODELS["medgemma-4b"]["model_id"],
            max_tokens=MODELS["medgemma-4b"]["max_tokens"],
            mode="no_tools",
            hospital=hospital,
        ))

    if "qwen3.5-27b-awq" not in skip_model:
        runs.append(RunConfig(
            name="qwen27b-react",
            model_key="qwen3.5-27b-awq",
            model_id=MODELS["qwen3.5-27b-awq"]["model_id"],
            max_tokens=MODELS["qwen3.5-27b-awq"]["max_tokens"],
            mode="react",
            hospital=hospital,
        ))
        runs.append(RunConfig(
            name="qwen27b-no-tools",
            model_key="qwen3.5-27b-awq",
            model_id=MODELS["qwen3.5-27b-awq"]["model_id"],
            max_tokens=MODELS["qwen3.5-27b-awq"]["max_tokens"],
            mode="no_tools",
            hospital=hospital,
        ))

    total_executions = len(runs) * len(cases) * repeats
    console.print(
        f"\n[bold]Running {len(runs)} configs × {len(cases)} cases × {repeats} repeats "
        f"= {total_executions} executions[/bold]\n"
    )

    # --- Checkpoint support ---
    checkpoint_file = out_path / "checkpoint.json"
    completed: set[str] = set()
    if checkpoint_file.exists():
        ckpt = json.loads(checkpoint_file.read_text())
        completed = set(ckpt.get("completed", []))
        console.print(f"[yellow]Resuming from checkpoint: {len(completed)} already done[/yellow]")

    # --- Run all cases ---
    all_results: list[CaseResult] = []
    traces: dict[str, dict[str, Any]] = {}  # {run_name: {case_id_repN: trace_dict}}

    for run_config in runs:
        console.print(f"\n[bold cyan]═══ {run_config.name} ({run_config.mode}) ═══[/bold cyan]")
        if run_config.name not in traces:
            traces[run_config.name] = {}

        for rep in range(1, repeats + 1):
            console.print(f"\n  [bold]── Repeat {rep}/{repeats} ──[/bold]")

            for i, case in enumerate(cases):
                run_key = f"{run_config.name}|{case.case_id}|rep{rep}"

                if run_key in completed:
                    console.print(
                        f"  [{i+1}/{len(cases)}] {case.case_id} "
                        f"({case.difficulty.value})... [dim]skipped (checkpoint)[/dim]"
                    )
                    continue

                console.print(
                    f"  [{i+1}/{len(cases)}] {case.case_id} "
                    f"({case.difficulty.value}) rep{rep}...",
                    end=" ",
                )

                try:
                    t0 = time.time()
                    trace, metrics = run_single_case(case, run_config)
                    elapsed = time.time() - t0

                    result = CaseResult(
                        case_id=case.case_id,
                        condition=case.condition.value,
                        difficulty=case.difficulty.value,
                        run_name=run_config.name,
                        model=run_config.model_key,
                        mode=run_config.mode,
                        hospital=run_config.hospital,
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

                    # Store trace
                    trace_key = f"{case.case_id}_rep{rep}"
                    traces[run_config.name][trace_key] = {
                        "turns": [
                            {
                                "turn": t.turn_number,
                                "role": t.role,
                                "content": (t.content or "")[:500],
                                "tool_calls": t.tool_calls,
                            }
                            for t in trace.turns
                        ],
                        "final_response": trace.final_response,
                        "total_tokens": trace.total_tokens,
                    }

                    # Update checkpoint
                    completed.add(run_key)
                    with open(checkpoint_file, "w") as f:
                        json.dump({"completed": sorted(completed)}, f)

                    dx = "✓" if metrics.diagnostic_accuracy_top1 else "✗"
                    cost_str = f"${metrics.total_cost_usd:,.0f}" if metrics.total_cost_usd > 0 else "$0"
                    console.print(
                        f"dx={dx}  tools={metrics.tool_call_count}  "
                        f"safety={metrics.safety_score:.2f}  "
                        f"cost={cost_str}  "
                        f"{elapsed:.0f}s  {trace.total_tokens}tok"
                    )

                except Exception as e:
                    console.print(f"[red]FAILED: {e}[/red]")
                    logger.exception("Case %s rep%d failed on %s", case.case_id, rep, run_config.name)

    # --- Print tables ---
    console.print("\n")
    _print_difficulty_summary(all_results)
    _print_consistency_table(all_results, cases, repeats)
    _print_protocol_compliance_summary(all_results)

    # --- Save results ---
    results_file = out_path / "comparison_results.json"
    with open(results_file, "w") as f:
        json.dump(
            {
                "config": {
                    "hospital": hospital,
                    "dataset": dataset,
                    "cases_per_difficulty": cases_per_difficulty,
                    "seed": seed,
                    "repeats": repeats,
                    "total_cases": len(cases),
                    "total_executions": total_executions,
                    "runs": [r.name for r in runs],
                },
                "cases_selected": [c.case_id for c in cases],
                "results": [asdict(r) for r in all_results],
            },
            f,
            indent=2,
            default=str,
        )
    console.print(f"\n[green]Results saved to {results_file}[/green]")

    # Save detailed traces
    traces_file = out_path / "traces.json"
    with open(traces_file, "w") as f:
        json.dump(traces, f, indent=2, default=str)
    console.print(f"[green]Traces saved to {traces_file}[/green]")

    # Save per-case comparison
    _save_case_comparisons(all_results, cases, out_path)

    # Save consistency report
    _save_consistency_report(all_results, cases, repeats, out_path)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------
def _print_comparison_table(results: list[CaseResult], cases: list[NeuroBenchCase]):
    """Print a head-to-head comparison table."""
    table = Table(title="NeuroBench v3 — Head-to-Head Comparison", show_lines=True)
    table.add_column("Case", style="bold", width=18)
    table.add_column("Difficulty", width=10)

    # Get unique run names
    run_names = sorted(set(r.run_name for r in results))
    for rn in run_names:
        table.add_column(rn, width=22)

    # Group results by case
    by_case: dict[str, dict[str, CaseResult]] = defaultdict(dict)
    for r in results:
        by_case[r.case_id][r.run_name] = r

    for case in cases:
        row = [case.case_id, case.difficulty.value[:6]]
        for rn in run_names:
            r = by_case.get(case.case_id, {}).get(rn)
            if r:
                dx = "[green]✓[/green]" if r.diagnostic_accuracy_top1 else "[red]✗[/red]"
                top3 = "[green]top3[/green]" if r.diagnostic_accuracy_top3 else ""
                tools = f"🔧{r.tool_call_count}" if r.tool_call_count > 0 else "no tools"
                safety = f"⚠{r.safety_score:.1f}" if r.safety_score < 1.0 else ""
                cell = f"{dx} {top3}\n{tools} {safety}\n{r.elapsed_seconds:.0f}s {r.total_tokens}tok"
                row.append(cell)
            else:
                row.append("[dim]—[/dim]")
        table.add_row(*row)

    console.print(table)


def _print_difficulty_summary(results: list[CaseResult]):
    """Print aggregate accuracy by difficulty and run, including cost."""
    table = Table(title="Accuracy by Difficulty", show_lines=True)
    table.add_column("Run", style="bold")
    table.add_column("Straightforward")
    table.add_column("Moderate")
    table.add_column("Puzzle")
    table.add_column("Overall")
    table.add_column("Avg Cost", justify="right")
    table.add_column("Cost Eff", justify="right")

    run_names = sorted(set(r.run_name for r in results))
    for rn in run_names:
        run_results = [r for r in results if r.run_name == rn]
        cells = []
        for diff in ["straightforward", "moderate", "diagnostic_puzzle"]:
            diff_results = [r for r in run_results if r.difficulty == diff]
            if diff_results:
                acc = sum(r.diagnostic_accuracy_top1 for r in diff_results) / len(diff_results)
                cells.append(f"{acc:.0%} ({sum(r.diagnostic_accuracy_top1 for r in diff_results)}/{len(diff_results)})")
            else:
                cells.append("—")
        # Overall
        if run_results:
            overall = sum(r.diagnostic_accuracy_top1 for r in run_results) / len(run_results)
            cells.append(f"[bold]{overall:.0%}[/bold] ({sum(r.diagnostic_accuracy_top1 for r in run_results)}/{len(run_results)})")
            avg_cost = sum(r.total_cost_usd for r in run_results) / len(run_results)
            avg_eff = sum(r.cost_efficiency for r in run_results) / len(run_results)
            cells.append(f"${avg_cost:,.0f}")
            cells.append(f"{avg_eff:.2f}")
        else:
            cells.extend(["—", "—", "—"])
        table.add_row(rn, *cells)

    console.print(table)


def _print_protocol_compliance_summary(results: list[CaseResult]):
    """Print protocol compliance summary."""
    table = Table(title="Protocol Compliance & Safety", show_lines=True)
    table.add_column("Run", style="bold")
    table.add_column("Compliance Rate")
    table.add_column("Mean Safety")
    table.add_column("Violations")
    table.add_column("Missing Steps")

    run_names = sorted(set(r.run_name for r in results))
    for rn in run_names:
        rr = [r for r in results if r.run_name == rn]
        compliant = [r for r in rr if r.protocol_compliance is True]
        checked = [r for r in rr if r.protocol_compliance is not None]
        comp_rate = f"{len(compliant)}/{len(checked)}" if checked else "N/A"
        mean_safety = f"{sum(r.safety_score for r in rr) / len(rr):.2f}" if rr else "—"
        violations = sum(len(r.protocol_violations) for r in rr)
        missing = sum(len(r.missing_required_steps) for r in rr)
        table.add_row(rn, comp_rate, mean_safety, str(violations), str(missing))

    console.print(table)


def _save_case_comparisons(
    results: list[CaseResult],
    cases: list[NeuroBenchCase],
    out_path: Path,
):
    """Save per-case comparison files for detailed review."""
    case_dir = out_path / "cases"
    case_dir.mkdir(exist_ok=True)

    by_case: dict[str, list[CaseResult]] = defaultdict(list)
    for r in results:
        by_case[r.case_id].append(r)

    gt_map = {c.case_id: c.ground_truth for c in cases}

    for case_id, case_results in by_case.items():
        gt = gt_map.get(case_id)
        comparison = {
            "case_id": case_id,
            "ground_truth": {
                "primary_diagnosis": gt.primary_diagnosis if gt else "",
                "icd_code": gt.icd_code if gt else "",
                "critical_actions": gt.critical_actions if gt else [],
                "contraindicated_actions": gt.contraindicated_actions if gt else [],
            },
            "runs": {},
        }
        for r in case_results:
            comparison["runs"][r.run_name] = {
                "diagnostic_accuracy_top1": r.diagnostic_accuracy_top1,
                "diagnostic_accuracy_top3": r.diagnostic_accuracy_top3,
                "agent_response_excerpt": r.agent_final_response[:500],
                "tool_call_count": r.tool_call_count,
                "tools_called": r.tools_called,
                "safety_score": r.safety_score,
                "protocol_compliance": r.protocol_compliance,
                "missing_required_steps": r.missing_required_steps,
                "elapsed_seconds": r.elapsed_seconds,
                "total_tokens": r.total_tokens,
                "total_cost_usd": r.total_cost_usd,
                "cost_efficiency": r.cost_efficiency,
            }

        with open(case_dir / f"{case_id}.json", "w") as f:
            json.dump(comparison, f, indent=2, default=str)


def _print_consistency_table(
    results: list[CaseResult],
    cases: list[NeuroBenchCase],
    repeats: int,
):
    """Print diagnostic consistency across repeats."""
    if repeats <= 1:
        return

    table = Table(title=f"Diagnostic Consistency ({repeats} repeats)", show_lines=True)
    table.add_column("Case", style="bold", width=18)
    table.add_column("Difficulty", width=8)

    run_names = sorted(set(r.run_name for r in results))
    for rn in run_names:
        table.add_column(rn, width=16)

    for case in cases:
        row = [case.case_id, case.difficulty.value[:6]]
        for rn in run_names:
            case_reps = [
                r for r in results
                if r.case_id == case.case_id and r.run_name == rn
            ]
            if case_reps:
                hits = sum(r.diagnostic_accuracy_top1 for r in case_reps)
                total = len(case_reps)
                if hits == total:
                    cell = f"[green]{hits}/{total} ✓✓✓[/green]"
                elif hits == 0:
                    cell = f"[red]{hits}/{total} ✗✗✗[/red]"
                else:
                    cell = f"[yellow]{hits}/{total} mixed[/yellow]"
                row.append(cell)
            else:
                row.append("[dim]—[/dim]")
        table.add_row(*row)

    # Summary row
    summary_row = ["[bold]Consistency[/bold]", ""]
    for rn in run_names:
        rn_results = [r for r in results if r.run_name == rn]
        # Group by case: consistent = all reps agree (all correct OR all wrong)
        by_case_rn: dict[str, list[bool]] = defaultdict(list)
        for r in rn_results:
            by_case_rn[r.case_id].append(r.diagnostic_accuracy_top1)
        n_cases = len(by_case_rn)
        n_consistent = sum(
            1 for hits in by_case_rn.values()
            if all(hits) or not any(hits)
        )
        summary_row.append(f"[bold]{n_consistent}/{n_cases}[/bold] ({n_consistent/n_cases:.0%})")
    table.add_row(*summary_row)

    console.print(table)


def _save_consistency_report(
    results: list[CaseResult],
    cases: list[NeuroBenchCase],
    repeats: int,
    out_path: Path,
):
    """Save a detailed consistency report showing per-case agreement across repeats."""
    if repeats <= 1:
        return

    run_names = sorted(set(r.run_name for r in results))
    report: dict[str, Any] = {
        "repeats": repeats,
        "per_run": {},
    }

    for rn in run_names:
        rn_results = [r for r in results if r.run_name == rn]
        by_case: dict[str, list[CaseResult]] = defaultdict(list)
        for r in rn_results:
            by_case[r.case_id].append(r)

        case_details = []
        n_consistent = 0
        n_always_correct = 0
        n_always_wrong = 0
        n_mixed = 0

        for case in cases:
            reps = by_case.get(case.case_id, [])
            if not reps:
                continue
            hits = [r.diagnostic_accuracy_top1 for r in reps]
            correct_count = sum(hits)
            total = len(hits)

            if all(hits):
                status = "always_correct"
                n_always_correct += 1
                n_consistent += 1
            elif not any(hits):
                status = "always_wrong"
                n_always_wrong += 1
                n_consistent += 1
            else:
                status = "inconsistent"
                n_mixed += 1

            case_details.append({
                "case_id": case.case_id,
                "condition": case.condition.value,
                "difficulty": case.difficulty.value,
                "correct_count": correct_count,
                "total_repeats": total,
                "consistency": status,
                "diagnoses": [r.agent_final_response[:200] for r in reps],
            })

        n_cases = len(case_details)
        report["per_run"][rn] = {
            "total_cases": n_cases,
            "always_correct": n_always_correct,
            "always_wrong": n_always_wrong,
            "inconsistent": n_mixed,
            "consistency_rate": round(n_consistent / n_cases, 3) if n_cases else 0,
            "accuracy_mean": round(
                sum(r.diagnostic_accuracy_top1 for r in rn_results) / len(rn_results), 3
            ) if rn_results else 0,
            "cases": case_details,
        }

    with open(out_path / "consistency_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    console.print(f"[green]Consistency report saved to {out_path / 'consistency_report.json'}[/green]")


if __name__ == "__main__":
    app()
