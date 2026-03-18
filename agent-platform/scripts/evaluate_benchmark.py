"""Evaluate benchmark results: compute metrics, generate reports, save structured output.

Reads traces from results/benchmark/ and produces:
  - Per-case metrics (diagnostic accuracy, tool usage, safety, reasoning quality)
  - Per-run aggregate tables
  - Cross-run comparison reports
  - Detailed case-level evaluation JSONs

Can run on partial results — evaluates whatever traces exist.

Usage:
    uv run python agent-platform/scripts/evaluate_benchmark.py
    uv run python agent-platform/scripts/evaluate_benchmark.py --benchmark-dir results/benchmark
"""

from __future__ import annotations

import json
import logging
import re
import statistics
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

logger = logging.getLogger(__name__)

app = typer.Typer()
console = Console()

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_BENCHMARK_DIR = REPO_ROOT / "results" / "benchmark"


# ---------------------------------------------------------------------------
# Evaluation criteria — the rules for scoring
# ---------------------------------------------------------------------------

EVALUATION_CRITERIA = {
    "diagnostic_accuracy_top1": {
        "description": "Primary diagnosis matches ground truth (fuzzy key-term matching, ≥70% of key terms present)",
        "weight": 0.20,
        "type": "boolean",
    },
    "diagnostic_accuracy_top3": {
        "description": "Correct diagnosis appears in the agent's top 3 differential diagnoses",
        "weight": 0.15,
        "type": "boolean",
    },
    "action_recall": {
        "description": "Fraction of optimal/required diagnostic actions the agent performed",
        "weight": 0.12,
        "type": "float_0_1",
    },
    "action_precision": {
        "description": "Fraction of agent's actions that were optimal (no unnecessary tests)",
        "weight": 0.10,
        "type": "float_0_1",
    },
    "critical_actions_hit": {
        "description": "Fraction of critical/must-do actions completed (e.g., EEG for seizure, CT for stroke)",
        "weight": 0.10,
        "type": "float_0_1",
    },
    "safety_score": {
        "description": "Composite safety: rewards critical actions, penalizes contraindicated ones (-0.3 each)",
        "weight": 0.10,
        "type": "float_0_1",
    },
    "efficiency_score": {
        "description": "Ratio of optimal actions to total tool calls (penalizes over-investigation)",
        "weight": 0.03,
        "type": "float_0_1",
    },
    "reasoning_completeness": {
        "description": "Whether final response includes all required sections (Primary Diagnosis, Differential, Key Evidence, Recommendations, Red Flags)",
        "weight": 0.05,
        "type": "float_0_1",
    },
    "protocol_compliance": {
        "description": "Whether the agent followed all mandatory hospital protocol steps and avoided violations",
        "weight": 0.08,
        "type": "boolean",
    },
    "cost_efficiency": {
        "description": "How efficiently the agent spent diagnostic budget vs optimal (1.0 = at or under optimal cost)",
        "weight": 0.07,
        "type": "float_0_1",
    },
}

REQUIRED_SECTIONS = [
    "Primary Diagnosis",
    "Differential",
    "Key Evidence",
    "Recommendations",
    "Red Flags",
]


# ---------------------------------------------------------------------------
# Per-case evaluation
# ---------------------------------------------------------------------------

@dataclass
class CaseEvaluation:
    """Complete evaluation of one trace."""

    case_id: str
    run_id: str
    model_id: str
    mode: str
    hospital: str
    repetition: int
    condition: str
    difficulty: str

    # From trace
    final_response: str
    tools_called: list[str]
    total_tool_calls: int
    total_tokens: int
    elapsed_time_seconds: float
    num_turns: int

    # Ground truth
    gt_primary_diagnosis: str
    gt_icd_code: str

    # Computed metrics
    diagnostic_accuracy_top1: bool = False
    diagnostic_accuracy_top3: bool = False
    action_recall: float = 0.0
    action_precision: float = 0.0
    critical_actions_hit: float = 0.0
    contraindicated_actions_taken: int = 0
    safety_score: float = 0.0
    efficiency_score: float = 0.0
    reasoning_completeness: float = 0.0

    # Cost tracking
    total_cost_usd: float = 0.0
    cost_efficiency: float = 0.0

    # Protocol compliance
    protocol_compliance: bool | None = None
    missing_required_steps: list[str] = field(default_factory=list)
    protocol_violations: list[str] = field(default_factory=list)

    # Weighted composite
    composite_score: float = 0.0


def evaluate_trace(trace_data: dict, run_id: str) -> CaseEvaluation:
    """Evaluate a single trace file."""
    gt = trace_data["ground_truth"]

    ev = CaseEvaluation(
        case_id=trace_data["case_id"],
        run_id=run_id,
        model_id=trace_data["model_id"],
        mode=trace_data["mode"],
        hospital=trace_data["hospital"],
        repetition=trace_data.get("repetition", 1),
        condition=trace_data["condition"],
        difficulty=trace_data["difficulty"],
        final_response=trace_data.get("final_response") or "",
        tools_called=trace_data.get("tools_called", []),
        total_tool_calls=trace_data.get("total_tool_calls", 0),
        total_tokens=trace_data.get("total_tokens", 0),
        elapsed_time_seconds=trace_data.get("elapsed_time_seconds", 0),
        num_turns=trace_data.get("num_turns", 0),
        gt_primary_diagnosis=gt["primary_diagnosis"],
        gt_icd_code=gt.get("icd_code", ""),
    )

    response = ev.final_response.lower()
    diagnosis = gt["primary_diagnosis"].lower()

    # --- Diagnostic accuracy ---
    # Top-1: key terms from ground truth present in response
    key_terms = [t for t in diagnosis.split() if len(t) > 3]
    if key_terms:
        matches = sum(1 for t in key_terms if t in response)
        ev.diagnostic_accuracy_top1 = matches >= len(key_terms) * 0.7
    if diagnosis in response:
        ev.diagnostic_accuracy_top1 = True

    # Top-3: also check differential terms
    ev.diagnostic_accuracy_top3 = ev.diagnostic_accuracy_top1
    if not ev.diagnostic_accuracy_top3:
        for diff in gt.get("differential", [])[:3]:
            if isinstance(diff, dict):
                diag = diff.get("diagnosis", "").lower()
            else:
                diag = str(diff).lower()
            if diag and diag in response:
                ev.diagnostic_accuracy_top3 = True
                break

    # --- Action metrics ---
    agent_actions = set(ev.tools_called)
    optimal_actions = set()
    for action in gt.get("optimal_actions", []):
        # Handle both dict and string (serialized Pydantic) formats
        if isinstance(action, dict):
            tool = action.get("tool_name", "")
        else:
            # Parse tool_name from string like "step=1 action='...' tool_name='analyze_eeg' ..."
            m = re.search(r"tool_name='?([a-z_]+)'?", str(action))
            tool = m.group(1) if m and m.group(1) != "None" else ""
        if tool:
            optimal_actions.add(tool)

    if agent_actions and optimal_actions:
        ev.action_precision = len(agent_actions & optimal_actions) / len(agent_actions)
    if optimal_actions:
        ev.action_recall = len(agent_actions & optimal_actions) / len(optimal_actions)

    # Critical actions — these are free-text descriptions, match against tool names in response
    critical_descriptions = gt.get("critical_actions", [])
    # Extract tool names mentioned in critical action descriptions
    tool_names_all = {
        "analyze_eeg", "analyze_brain_mri", "analyze_ecg", "interpret_labs",
        "analyze_csf", "search_medical_literature", "check_drug_interactions",
        "order_ct_scan", "order_echocardiogram", "order_cardiac_monitoring",
        "order_advanced_imaging", "order_specialized_test",
    }
    critical_tools = set()
    for desc in critical_descriptions:
        desc_lower = str(desc).lower()
        for t in tool_names_all:
            # Match tool name or its key terms (e.g., "eeg" -> analyze_eeg)
            tool_keywords = t.replace("analyze_", "").replace("interpret_", "").replace("check_", "").replace("search_", "")
            if tool_keywords in desc_lower:
                critical_tools.add(t)
    if critical_tools:
        ev.critical_actions_hit = len(agent_actions & critical_tools) / len(critical_tools)

    # Contraindicated — free-text, check if agent did something mentioned
    contraindicated_descs = gt.get("contraindicated_actions", [])
    for desc in contraindicated_descs:
        desc_lower = str(desc).lower()
        for tool in agent_actions:
            if tool.replace("_", " ") in desc_lower or tool in desc_lower:
                ev.contraindicated_actions_taken += 1

    # Efficiency
    if optimal_actions and ev.total_tool_calls > 0:
        ev.efficiency_score = min(1.0, len(optimal_actions) / ev.total_tool_calls)

    # Safety
    penalty = ev.contraindicated_actions_taken * 0.3
    ev.safety_score = max(0.0, min(1.0, ev.critical_actions_hit - penalty))

    # --- Reasoning completeness ---
    sections_found = sum(1 for s in REQUIRED_SECTIONS if s.lower() in response)
    ev.reasoning_completeness = sections_found / len(REQUIRED_SECTIONS)

    # --- Cost tracking ---
    ev.total_cost_usd = trace_data.get("total_cost_usd", 0.0)
    # Compute optimal cost from ground truth
    try:
        from neuroagent.tools.cost_tracker import CostTracker
        tracker = CostTracker()
        for action in gt.get("optimal_actions", []):
            tool = action.get("tool_name", "") if isinstance(action, dict) else ""
            if tool:
                tracker.compute_cost(tool, {})
        optimal_cost = tracker.total_cost_usd
        if optimal_cost > 0:
            overspend = max(0.0, ev.total_cost_usd - optimal_cost)
            ev.cost_efficiency = max(0.0, 1.0 - overspend / (optimal_cost + 1))
        elif ev.total_cost_usd == 0:
            ev.cost_efficiency = 1.0
    except Exception:
        ev.cost_efficiency = 0.0

    # --- Protocol compliance (via rules engine) ---
    hospital = trace_data.get("hospital", "")
    if hospital:
        try:
            from neuroagent.rules.pathway_checker import PathwayChecker
            from neuroagent.rules.rules_engine import RulesEngine

            rules_dir = trace_data.get("rules_dir", "config/hospital_rules")
            rules_engine = RulesEngine(rules_dir, hospital=hospital)
            checker = PathwayChecker(rules_engine)
            compliance = checker.check_case(ev.tools_called, ev.condition)
            if compliance is not None:
                ev.protocol_compliance = compliance.compliant
                ev.missing_required_steps = compliance.missing_required
                ev.protocol_violations = compliance.violations
        except Exception as e:
            logger.warning("Protocol compliance check failed for %s: %s", ev.case_id, e)

    # --- Weighted composite ---
    # Protocol compliance contributes to the composite when available;
    # when no matching pathway exists (None), treat as neutral (1.0) so the
    # weight doesn't penalise cases without applicable pathways.
    protocol_compliance_value = float(ev.protocol_compliance) if ev.protocol_compliance is not None else 1.0

    ev.composite_score = (
        EVALUATION_CRITERIA["diagnostic_accuracy_top1"]["weight"] * float(ev.diagnostic_accuracy_top1)
        + EVALUATION_CRITERIA["diagnostic_accuracy_top3"]["weight"] * float(ev.diagnostic_accuracy_top3)
        + EVALUATION_CRITERIA["action_recall"]["weight"] * ev.action_recall
        + EVALUATION_CRITERIA["action_precision"]["weight"] * ev.action_precision
        + EVALUATION_CRITERIA["critical_actions_hit"]["weight"] * ev.critical_actions_hit
        + EVALUATION_CRITERIA["safety_score"]["weight"] * ev.safety_score
        + EVALUATION_CRITERIA["efficiency_score"]["weight"] * ev.efficiency_score
        + EVALUATION_CRITERIA["reasoning_completeness"]["weight"] * ev.reasoning_completeness
        + EVALUATION_CRITERIA["protocol_compliance"]["weight"] * protocol_compliance_value
        + EVALUATION_CRITERIA["cost_efficiency"]["weight"] * ev.cost_efficiency
    )

    return ev


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

@dataclass
class RunAggregate:
    """Aggregate metrics for one run."""

    run_id: str
    model_id: str
    mode: str
    hospital: str
    num_cases: int = 0

    # Means ± std
    top1_accuracy: float = 0.0
    top3_accuracy: float = 0.0
    mean_action_recall: float = 0.0
    mean_action_precision: float = 0.0
    mean_critical_hit: float = 0.0
    mean_safety: float = 0.0
    mean_efficiency: float = 0.0
    mean_reasoning_completeness: float = 0.0
    mean_composite: float = 0.0
    std_composite: float = 0.0

    mean_protocol_compliance: float = 0.0

    mean_cost_usd: float = 0.0
    mean_cost_efficiency: float = 0.0

    mean_tools: float = 0.0
    mean_time: float = 0.0
    mean_tokens: float = 0.0
    total_contraindicated: int = 0

    # Per-condition breakdown
    by_condition: dict = field(default_factory=dict)
    by_difficulty: dict = field(default_factory=dict)


def aggregate_evaluations(evals: list[CaseEvaluation], run_id: str) -> RunAggregate:
    """Compute aggregate stats from a list of case evaluations."""
    if not evals:
        return RunAggregate(run_id=run_id, model_id="", mode="", hospital="")

    agg = RunAggregate(
        run_id=run_id,
        model_id=evals[0].model_id,
        mode=evals[0].mode,
        hospital=evals[0].hospital,
        num_cases=len(evals),
    )

    agg.top1_accuracy = sum(e.diagnostic_accuracy_top1 for e in evals) / len(evals)
    agg.top3_accuracy = sum(e.diagnostic_accuracy_top3 for e in evals) / len(evals)
    agg.mean_action_recall = statistics.mean(e.action_recall for e in evals)
    agg.mean_action_precision = statistics.mean(e.action_precision for e in evals)
    agg.mean_critical_hit = statistics.mean(e.critical_actions_hit for e in evals)
    agg.mean_safety = statistics.mean(e.safety_score for e in evals)
    agg.mean_efficiency = statistics.mean(e.efficiency_score for e in evals)
    agg.mean_reasoning_completeness = statistics.mean(e.reasoning_completeness for e in evals)

    # Protocol compliance: only count cases where compliance was actually checked
    compliance_evals = [e for e in evals if e.protocol_compliance is not None]
    if compliance_evals:
        agg.mean_protocol_compliance = sum(
            e.protocol_compliance for e in compliance_evals
        ) / len(compliance_evals)

    agg.mean_cost_usd = statistics.mean(e.total_cost_usd for e in evals)
    agg.mean_cost_efficiency = statistics.mean(e.cost_efficiency for e in evals)

    composites = [e.composite_score for e in evals]
    agg.mean_composite = statistics.mean(composites)
    agg.std_composite = statistics.stdev(composites) if len(composites) > 1 else 0.0

    agg.mean_tools = statistics.mean(e.total_tool_calls for e in evals)
    agg.mean_time = statistics.mean(e.elapsed_time_seconds for e in evals)
    agg.mean_tokens = statistics.mean(e.total_tokens for e in evals)
    agg.total_contraindicated = sum(e.contraindicated_actions_taken for e in evals)

    # Per-condition
    by_cond: dict[str, list[CaseEvaluation]] = defaultdict(list)
    for e in evals:
        by_cond[e.condition].append(e)
    for cond, cond_evals in sorted(by_cond.items()):
        agg.by_condition[cond] = {
            "n": len(cond_evals),
            "top1": sum(e.diagnostic_accuracy_top1 for e in cond_evals) / len(cond_evals),
            "top3": sum(e.diagnostic_accuracy_top3 for e in cond_evals) / len(cond_evals),
            "composite": statistics.mean(e.composite_score for e in cond_evals),
            "mean_tools": statistics.mean(e.total_tool_calls for e in cond_evals),
        }

    # Per-difficulty
    by_diff: dict[str, list[CaseEvaluation]] = defaultdict(list)
    for e in evals:
        by_diff[e.difficulty].append(e)
    for diff, diff_evals in sorted(by_diff.items()):
        agg.by_difficulty[diff] = {
            "n": len(diff_evals),
            "top1": sum(e.diagnostic_accuracy_top1 for e in diff_evals) / len(diff_evals),
            "composite": statistics.mean(e.composite_score for e in diff_evals),
        }

    return agg


# ---------------------------------------------------------------------------
# Main evaluation
# ---------------------------------------------------------------------------

@app.command()
def evaluate(
    benchmark_dir: str = typer.Option(str(DEFAULT_BENCHMARK_DIR), help="Benchmark results directory"),
    output_dir: str = typer.Option("", help="Output dir for reports (default: benchmark_dir/evaluation)"),
) -> None:
    """Evaluate all benchmark results and generate reports."""
    bdir = Path(benchmark_dir)
    if not bdir.exists():
        console.print(f"[red]Benchmark dir not found: {bdir}[/red]")
        raise typer.Exit(1)

    odir = Path(output_dir) if output_dir else bdir / "evaluation"
    odir.mkdir(parents=True, exist_ok=True)

    # Save evaluation criteria
    (odir / "evaluation_criteria.json").write_text(
        json.dumps(EVALUATION_CRITERIA, indent=2)
    )
    console.print(f"[bold]Evaluation criteria saved to {odir / 'evaluation_criteria.json'}[/bold]\n")

    # Discover all runs
    run_dirs = sorted([d for d in bdir.iterdir() if d.is_dir() and (d / "traces").is_dir()])
    if not run_dirs:
        console.print("[yellow]No completed runs found.[/yellow]")
        raise typer.Exit(0)

    console.print(f"[bold]Evaluating {len(run_dirs)} runs from {bdir}[/bold]\n")

    all_evals: list[CaseEvaluation] = []
    all_aggregates: list[RunAggregate] = []

    for run_dir in run_dirs:
        run_id = run_dir.name
        traces_dir = run_dir / "traces"
        trace_files = sorted(traces_dir.glob("*.json"))

        if not trace_files:
            continue

        console.print(f"[cyan]{run_id}[/cyan]: {len(trace_files)} traces")

        # Evaluate each trace
        run_evals: list[CaseEvaluation] = []
        for tf in trace_files:
            try:
                data = json.loads(tf.read_text())
                ev = evaluate_trace(data, run_id)
                run_evals.append(ev)
            except Exception as e:
                console.print(f"  [red]Error evaluating {tf.name}: {e}[/red]")

        if not run_evals:
            continue

        # Save per-case evaluations
        case_eval_dir = odir / run_id
        case_eval_dir.mkdir(exist_ok=True)
        for ev in run_evals:
            fname = f"{ev.case_id}_rep{ev.repetition}.json"
            (case_eval_dir / fname).write_text(
                json.dumps(asdict(ev), indent=2, default=str)
            )

        # Aggregate
        agg = aggregate_evaluations(run_evals, run_id)
        all_aggregates.append(agg)
        all_evals.extend(run_evals)

        # Save run aggregate
        (case_eval_dir / "_aggregate.json").write_text(
            json.dumps(asdict(agg), indent=2, default=str)
        )

        # Print quick summary
        console.print(
            f"  Top-1: {agg.top1_accuracy:.0%}  "
            f"Top-3: {agg.top3_accuracy:.0%}  "
            f"Composite: {agg.mean_composite:.3f}±{agg.std_composite:.3f}  "
            f"Tools: {agg.mean_tools:.1f}  "
            f"Time: {agg.mean_time:.0f}s"
        )

    if not all_aggregates:
        console.print("[yellow]No evaluations produced.[/yellow]")
        raise typer.Exit(0)

    # -----------------------------------------------------------------------
    # Cross-run comparison table
    # -----------------------------------------------------------------------
    console.print(f"\n{'='*80}")
    console.print("[bold]Cross-Run Comparison[/bold]")
    console.print(f"{'='*80}\n")

    table = Table(title="Model × Mode × Hospital Comparison")
    table.add_column("Run", style="cyan", max_width=35)
    table.add_column("N", justify="right")
    table.add_column("Top-1", justify="right")
    table.add_column("Top-3", justify="right")
    table.add_column("Act Rec", justify="right")
    table.add_column("Critical", justify="right")
    table.add_column("Safety", justify="right")
    table.add_column("Compl", justify="right")
    table.add_column("Protocol", justify="right")
    table.add_column("Cost$", justify="right")
    table.add_column("CostEff", justify="right")
    table.add_column("Composite", justify="right")
    table.add_column("Tools", justify="right")
    table.add_column("Time", justify="right")

    for agg in all_aggregates:
        table.add_row(
            agg.run_id,
            str(agg.num_cases),
            f"{agg.top1_accuracy:.0%}",
            f"{agg.top3_accuracy:.0%}",
            f"{agg.mean_action_recall:.2f}",
            f"{agg.mean_critical_hit:.2f}",
            f"{agg.mean_safety:.2f}",
            f"{agg.mean_reasoning_completeness:.2f}",
            f"{agg.mean_protocol_compliance:.0%}",
            f"${agg.mean_cost_usd:,.0f}",
            f"{agg.mean_cost_efficiency:.2f}",
            f"{agg.mean_composite:.3f}",
            f"{agg.mean_tools:.1f}",
            f"{agg.mean_time:.0f}s",
        )

    console.print(table)

    # -----------------------------------------------------------------------
    # Per-condition breakdown
    # -----------------------------------------------------------------------
    console.print(f"\n{'='*80}")
    console.print("[bold]Per-Condition Breakdown[/bold]")
    console.print(f"{'='*80}\n")

    # Collect all conditions across runs
    conditions = sorted({c for agg in all_aggregates for c in agg.by_condition})

    for cond in conditions:
        ctable = Table(title=f"Condition: {cond}")
        ctable.add_column("Run", style="cyan", max_width=35)
        ctable.add_column("N", justify="right")
        ctable.add_column("Top-1", justify="right")
        ctable.add_column("Top-3", justify="right")
        ctable.add_column("Composite", justify="right")
        ctable.add_column("Avg Tools", justify="right")

        for agg in all_aggregates:
            cd = agg.by_condition.get(cond)
            if cd:
                ctable.add_row(
                    agg.run_id,
                    str(cd["n"]),
                    f"{cd['top1']:.0%}",
                    f"{cd['top3']:.0%}",
                    f"{cd['composite']:.3f}",
                    f"{cd['mean_tools']:.1f}",
                )

        console.print(ctable)
        console.print()

    # -----------------------------------------------------------------------
    # Per-difficulty breakdown
    # -----------------------------------------------------------------------
    console.print(f"\n{'='*80}")
    console.print("[bold]Per-Difficulty Breakdown[/bold]")
    console.print(f"{'='*80}\n")

    dtable = Table(title="Difficulty Analysis")
    dtable.add_column("Run", style="cyan", max_width=35)
    dtable.add_column("Straightforward", justify="center")
    dtable.add_column("Moderate", justify="center")
    dtable.add_column("Puzzle", justify="center")

    for agg in all_aggregates:
        s = agg.by_difficulty.get("straightforward", {})
        m = agg.by_difficulty.get("moderate", {})
        p = agg.by_difficulty.get("diagnostic_puzzle", {})
        dtable.add_row(
            agg.run_id,
            f"{s.get('top1', 0):.0%} ({s.get('n', 0)})" if s else "-",
            f"{m.get('top1', 0):.0%} ({m.get('n', 0)})" if m else "-",
            f"{p.get('top1', 0):.0%} ({p.get('n', 0)})" if p else "-",
        )

    console.print(dtable)

    # -----------------------------------------------------------------------
    # Save full report
    # -----------------------------------------------------------------------
    report = {
        "evaluation_timestamp": __import__("time").strftime("%Y-%m-%dT%H:%M:%S"),
        "benchmark_dir": str(bdir),
        "total_traces_evaluated": len(all_evals),
        "num_runs": len(all_aggregates),
        "evaluation_criteria": EVALUATION_CRITERIA,
        "run_summaries": [asdict(agg) for agg in all_aggregates],
        "overall_stats": {
            "mean_top1_across_runs": statistics.mean(a.top1_accuracy for a in all_aggregates),
            "mean_top3_across_runs": statistics.mean(a.top3_accuracy for a in all_aggregates),
            "mean_composite_across_runs": statistics.mean(a.mean_composite for a in all_aggregates),
            "total_contraindicated_actions": sum(a.total_contraindicated for a in all_aggregates),
        },
    }

    report_file = odir / "evaluation_report.json"
    report_file.write_text(json.dumps(report, indent=2, default=str))
    console.print(f"\n[bold]Full report saved to {report_file}[/bold]")

    # Also save a flat CSV-like JSON for easy analysis
    flat_records = []
    for ev in all_evals:
        flat_records.append({
            "case_id": ev.case_id,
            "run_id": ev.run_id,
            "model_id": ev.model_id,
            "mode": ev.mode,
            "hospital": ev.hospital,
            "repetition": ev.repetition,
            "condition": ev.condition,
            "difficulty": ev.difficulty,
            "top1": ev.diagnostic_accuracy_top1,
            "top3": ev.diagnostic_accuracy_top3,
            "action_recall": round(ev.action_recall, 3),
            "action_precision": round(ev.action_precision, 3),
            "critical_hit": round(ev.critical_actions_hit, 3),
            "safety": round(ev.safety_score, 3),
            "efficiency": round(ev.efficiency_score, 3),
            "reasoning_completeness": round(ev.reasoning_completeness, 3),
            "protocol_compliance": ev.protocol_compliance,
            "missing_required_steps": ev.missing_required_steps,
            "protocol_violations": ev.protocol_violations,
            "cost_usd": round(ev.total_cost_usd, 2),
            "cost_efficiency": round(ev.cost_efficiency, 3),
            "composite": round(ev.composite_score, 4),
            "tools": ev.total_tool_calls,
            "time_s": round(ev.elapsed_time_seconds, 1),
            "tokens": ev.total_tokens,
            "contraindicated": ev.contraindicated_actions_taken,
        })

    flat_file = odir / "all_evaluations_flat.json"
    flat_file.write_text(json.dumps(flat_records, indent=2))
    console.print(f"Flat evaluation data saved to {flat_file}")
    console.print(f"Total: {len(flat_records)} case evaluations across {len(all_aggregates)} runs")


if __name__ == "__main__":
    app()
