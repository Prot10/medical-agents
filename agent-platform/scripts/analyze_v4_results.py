#!/usr/bin/env python3
"""Comprehensive analysis of NeuroBench v4 comparison results.

Loads merged_results.json, computes aggregate metrics, performs statistical
analysis, and generates a structured evaluation report with tables and JSON.

Usage:
    uv run python agent-platform/scripts/analyze_v4_results.py
    uv run python agent-platform/scripts/analyze_v4_results.py --results-dir results/v4_comparison
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "agent-platform" / "src"))
sys.path.insert(0, str(REPO_ROOT / "packages" / "neuroagent-schemas" / "src"))

app = typer.Typer()
console = Console()


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class RunAgg:
    """Aggregate metrics for one run configuration."""
    run_name: str
    model: str
    mode: str
    n: int = 0
    n_cases: int = 0

    # Accuracy
    top1_accuracy: float = 0.0
    top3_accuracy: float = 0.0

    # Actions
    mean_critical_hit: float = 0.0
    mean_safety: float = 0.0

    # Cost
    mean_cost_usd: float = 0.0
    median_cost_usd: float = 0.0
    std_cost_usd: float = 0.0
    mean_cost_efficiency: float = 0.0

    # Tool usage
    mean_tool_calls: float = 0.0
    tool_frequency: dict[str, int] = field(default_factory=dict)

    # Protocol
    protocol_compliance_rate: float = 0.0

    # Performance
    mean_tokens: float = 0.0
    mean_time: float = 0.0

    # Consistency
    consistency_rate: float = 0.0
    always_correct: int = 0
    always_wrong: int = 0
    inconsistent: int = 0

    # By difficulty
    by_difficulty: dict[str, dict] = field(default_factory=dict)
    # By condition
    by_condition: dict[str, dict] = field(default_factory=dict)


def compute_run_agg(results: list[dict], run_name: str) -> RunAgg:
    rr = [r for r in results if r["run_name"] == run_name]
    if not rr:
        return RunAgg(run_name=run_name, model="", mode="")

    agg = RunAgg(
        run_name=run_name,
        model=rr[0]["model"],
        mode=rr[0]["mode"],
        n=len(rr),
    )

    agg.top1_accuracy = sum(r["diagnostic_accuracy_top1"] for r in rr) / len(rr)
    agg.top3_accuracy = sum(r["diagnostic_accuracy_top3"] for r in rr) / len(rr)
    agg.mean_critical_hit = statistics.mean(r["critical_actions_hit"] for r in rr)
    agg.mean_safety = statistics.mean(r["safety_score"] for r in rr)

    costs = [r["total_cost_usd"] for r in rr]
    agg.mean_cost_usd = statistics.mean(costs)
    agg.median_cost_usd = statistics.median(costs)
    agg.std_cost_usd = statistics.stdev(costs) if len(costs) > 1 else 0.0
    agg.mean_cost_efficiency = statistics.mean(r["cost_efficiency"] for r in rr)

    agg.mean_tool_calls = statistics.mean(r["tool_call_count"] for r in rr)
    agg.mean_tokens = statistics.mean(r["total_tokens"] for r in rr)
    agg.mean_time = statistics.mean(r["elapsed_seconds"] for r in rr)

    # Tool frequency
    freq: dict[str, int] = defaultdict(int)
    for r in rr:
        for t in r["tools_called"]:
            freq[t] += 1
    agg.tool_frequency = dict(sorted(freq.items(), key=lambda x: -x[1]))

    # Protocol compliance
    checked = [r for r in rr if r["protocol_compliance"] is not None]
    if checked:
        agg.protocol_compliance_rate = sum(r["protocol_compliance"] for r in checked) / len(checked)

    # Consistency
    by_case: dict[str, list[bool]] = defaultdict(list)
    for r in rr:
        by_case[r["case_id"]].append(r["diagnostic_accuracy_top1"])
    agg.n_cases = len(by_case)
    for case_id, hits in by_case.items():
        if all(hits):
            agg.always_correct += 1
        elif not any(hits):
            agg.always_wrong += 1
        else:
            agg.inconsistent += 1
    agg.consistency_rate = (agg.always_correct + agg.always_wrong) / agg.n_cases if agg.n_cases else 0

    # By difficulty
    for diff in ["straightforward", "moderate", "diagnostic_puzzle"]:
        dr = [r for r in rr if r["difficulty"] == diff]
        if dr:
            agg.by_difficulty[diff] = {
                "n": len(dr),
                "top1": sum(r["diagnostic_accuracy_top1"] for r in dr) / len(dr),
                "top3": sum(r["diagnostic_accuracy_top3"] for r in dr) / len(dr),
                "mean_cost": statistics.mean(r["total_cost_usd"] for r in dr),
                "mean_tools": statistics.mean(r["tool_call_count"] for r in dr),
                "mean_safety": statistics.mean(r["safety_score"] for r in dr),
            }

    # By condition
    for cond in sorted(set(r["condition"] for r in rr)):
        cr = [r for r in rr if r["condition"] == cond]
        if cr:
            agg.by_condition[cond] = {
                "n": len(cr),
                "top1": sum(r["diagnostic_accuracy_top1"] for r in cr) / len(cr),
                "top3": sum(r["diagnostic_accuracy_top3"] for r in cr) / len(cr),
                "mean_cost": statistics.mean(r["total_cost_usd"] for r in cr),
                "mean_tools": statistics.mean(r["tool_call_count"] for r in cr),
            }

    return agg


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def analyze_cost_by_condition(results: list[dict]) -> dict[str, dict]:
    """Analyze cost patterns across conditions for react runs."""
    react_results = [r for r in results if r["mode"] == "react"]
    by_cond: dict[str, list[dict]] = defaultdict(list)
    for r in react_results:
        by_cond[r["condition"]].append(r)

    analysis = {}
    for cond in sorted(by_cond):
        rr = by_cond[cond]
        costs = [r["total_cost_usd"] for r in rr]
        tools_used = defaultdict(int)
        for r in rr:
            for t in r["tools_called"]:
                tools_used[t] += 1
        analysis[cond] = {
            "n": len(rr),
            "mean_cost": round(statistics.mean(costs), 0),
            "median_cost": round(statistics.median(costs), 0),
            "min_cost": round(min(costs), 0),
            "max_cost": round(max(costs), 0),
            "std_cost": round(statistics.stdev(costs), 0) if len(costs) > 1 else 0,
            "top1_accuracy": round(sum(r["diagnostic_accuracy_top1"] for r in rr) / len(rr), 3),
            "top_tools": dict(sorted(tools_used.items(), key=lambda x: -x[1])[:5]),
        }
    return analysis


def analyze_tool_usage_patterns(results: list[dict]) -> dict:
    """Analyze which tools are used and how often across models."""
    react_results = [r for r in results if r["mode"] == "react"]
    by_model: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    by_model_n: dict[str, int] = defaultdict(int)

    for r in react_results:
        model = r["run_name"]
        by_model_n[model] += 1
        for t in r["tools_called"]:
            by_model[model][t] += 1

    # Compute per-case frequency
    analysis = {}
    for model in sorted(by_model):
        n = by_model_n[model]
        tool_freq = {t: round(count / n, 2) for t, count in sorted(by_model[model].items(), key=lambda x: -x[1])}
        analysis[model] = {
            "n_cases": n,
            "tools_per_case": tool_freq,
            "mean_tools_per_case": round(sum(by_model[model].values()) / n, 1),
            "unique_tools_used": len(by_model[model]),
        }
    return analysis


def analyze_react_vs_no_tools(results: list[dict]) -> dict:
    """Compare react mode (with tools) vs no-tools mode for each model."""
    pairs = defaultdict(lambda: {"react": [], "no_tools": []})
    for r in results:
        model = r["model"]
        mode = r["mode"]
        pairs[model][mode].append(r)

    comparison = {}
    for model in sorted(pairs):
        react = pairs[model]["react"]
        no_tools = pairs[model]["no_tools"]
        if not react or not no_tools:
            continue

        comparison[model] = {
            "react": {
                "n": len(react),
                "top1": round(sum(r["diagnostic_accuracy_top1"] for r in react) / len(react), 3),
                "top3": round(sum(r["diagnostic_accuracy_top3"] for r in react) / len(react), 3),
                "mean_cost": round(statistics.mean(r["total_cost_usd"] for r in react), 0),
                "mean_safety": round(statistics.mean(r["safety_score"] for r in react), 3),
                "mean_tools": round(statistics.mean(r["tool_call_count"] for r in react), 1),
                "mean_time": round(statistics.mean(r["elapsed_seconds"] for r in react), 1),
            },
            "no_tools": {
                "n": len(no_tools),
                "top1": round(sum(r["diagnostic_accuracy_top1"] for r in no_tools) / len(no_tools), 3),
                "top3": round(sum(r["diagnostic_accuracy_top3"] for r in no_tools) / len(no_tools), 3),
                "mean_cost": 0,
                "mean_safety": round(statistics.mean(r["safety_score"] for r in no_tools), 3),
                "mean_tools": 0,
                "mean_time": round(statistics.mean(r["elapsed_seconds"] for r in no_tools), 1),
            },
            "delta_top1": 0.0,
            "delta_top3": 0.0,
        }
        comparison[model]["delta_top1"] = round(
            comparison[model]["react"]["top1"] - comparison[model]["no_tools"]["top1"], 3
        )
        comparison[model]["delta_top3"] = round(
            comparison[model]["react"]["top3"] - comparison[model]["no_tools"]["top3"], 3
        )
    return comparison


def find_hardest_cases(results: list[dict], n: int = 10) -> list[dict]:
    """Find cases that all models struggle with."""
    by_case: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        by_case[r["case_id"]].append(r)

    case_scores = []
    for case_id, rr in by_case.items():
        top1_rate = sum(r["diagnostic_accuracy_top1"] for r in rr) / len(rr)
        case_scores.append({
            "case_id": case_id,
            "condition": rr[0]["condition"],
            "difficulty": rr[0]["difficulty"],
            "gt_diagnosis": rr[0]["primary_diagnosis_gt"],
            "top1_rate": round(top1_rate, 3),
            "n_runs": len(rr),
            "n_correct": sum(r["diagnostic_accuracy_top1"] for r in rr),
        })

    case_scores.sort(key=lambda x: x["top1_rate"])
    return case_scores[:n]


def find_expensive_cases(results: list[dict], n: int = 10) -> list[dict]:
    """Find cases where the agent spent the most on diagnostics."""
    react_results = [r for r in results if r["mode"] == "react"]
    by_case: dict[str, list[dict]] = defaultdict(list)
    for r in react_results:
        by_case[r["case_id"]].append(r)

    case_costs = []
    for case_id, rr in by_case.items():
        mean_cost = statistics.mean(r["total_cost_usd"] for r in rr)
        case_costs.append({
            "case_id": case_id,
            "condition": rr[0]["condition"],
            "difficulty": rr[0]["difficulty"],
            "mean_cost_usd": round(mean_cost, 0),
            "top1_rate": round(sum(r["diagnostic_accuracy_top1"] for r in rr) / len(rr), 3),
            "mean_tools": round(statistics.mean(r["tool_call_count"] for r in rr), 1),
        })

    case_costs.sort(key=lambda x: -x["mean_cost_usd"])
    return case_costs[:n]


def analyze_new_tools_impact(results: list[dict]) -> dict:
    """Analyze how the 5 new tools are being used and their diagnostic impact."""
    new_tools = {"order_ct_scan", "order_echocardiogram", "order_cardiac_monitoring",
                 "order_advanced_imaging", "order_specialized_test"}
    react_results = [r for r in results if r["mode"] == "react"]

    used_new = [r for r in react_results if any(t in new_tools for t in r["tools_called"])]
    not_used_new = [r for r in react_results if not any(t in new_tools for t in r["tools_called"])]

    # Per new tool stats
    per_tool = {}
    for tool in sorted(new_tools):
        cases_using = [r for r in react_results if tool in r["tools_called"]]
        if cases_using:
            per_tool[tool] = {
                "n_uses": len(cases_using),
                "pct_of_react_cases": round(len(cases_using) / len(react_results) * 100, 1),
                "top1_when_used": round(sum(r["diagnostic_accuracy_top1"] for r in cases_using) / len(cases_using), 3),
                "conditions": dict(sorted(
                    defaultdict(int, {r["condition"]: 1 for r in cases_using}).items(),
                    key=lambda x: -x[1],
                )),
            }

    return {
        "n_react_total": len(react_results),
        "n_used_new_tools": len(used_new),
        "n_not_used_new_tools": len(not_used_new),
        "pct_using_new": round(len(used_new) / len(react_results) * 100, 1) if react_results else 0,
        "top1_with_new": round(sum(r["diagnostic_accuracy_top1"] for r in used_new) / len(used_new), 3) if used_new else 0,
        "top1_without_new": round(sum(r["diagnostic_accuracy_top1"] for r in not_used_new) / len(not_used_new), 3) if not_used_new else 0,
        "per_tool": per_tool,
    }


# ---------------------------------------------------------------------------
# Print helpers
# ---------------------------------------------------------------------------

def print_main_comparison(aggs: list[RunAgg]):
    table = Table(title="Model Comparison — NeuroBench v4 (12 tools + cost)", show_lines=True)
    table.add_column("Run", style="bold", width=22)
    table.add_column("N", justify="right")
    table.add_column("Top-1", justify="right")
    table.add_column("Top-3", justify="right")
    table.add_column("Critical", justify="right")
    table.add_column("Safety", justify="right")
    table.add_column("Avg Cost", justify="right")
    table.add_column("Cost Eff", justify="right")
    table.add_column("Tools", justify="right")
    table.add_column("Protocol", justify="right")
    table.add_column("Consist", justify="right")
    table.add_column("Time", justify="right")

    for a in aggs:
        table.add_row(
            a.run_name,
            str(a.n),
            f"{a.top1_accuracy:.0%}",
            f"{a.top3_accuracy:.0%}",
            f"{a.mean_critical_hit:.2f}",
            f"{a.mean_safety:.2f}",
            f"${a.mean_cost_usd:,.0f}",
            f"{a.mean_cost_efficiency:.2f}",
            f"{a.mean_tool_calls:.1f}",
            f"{a.protocol_compliance_rate:.0%}",
            f"{a.consistency_rate:.0%}",
            f"{a.mean_time:.0f}s",
        )
    console.print(table)


def print_difficulty_table(aggs: list[RunAgg]):
    table = Table(title="Accuracy & Cost by Difficulty", show_lines=True)
    table.add_column("Run", style="bold", width=22)
    for d in ["straightforward", "moderate", "diagnostic_puzzle"]:
        table.add_column(d[:6].title(), justify="center")
    table.add_column("Cost S", justify="right")
    table.add_column("Cost M", justify="right")
    table.add_column("Cost P", justify="right")

    for a in aggs:
        cells = []
        costs = []
        for d in ["straightforward", "moderate", "diagnostic_puzzle"]:
            dd = a.by_difficulty.get(d, {})
            if dd:
                cells.append(f"{dd['top1']:.0%} ({dd['n']})")
                costs.append(f"${dd['mean_cost']:,.0f}")
            else:
                cells.append("—")
                costs.append("—")
        table.add_row(a.run_name, *cells, *costs)

    console.print(table)


def print_condition_table(aggs: list[RunAgg]):
    react_aggs = [a for a in aggs if a.mode == "react"]
    if not react_aggs:
        return

    conditions = sorted(set(c for a in react_aggs for c in a.by_condition))
    table = Table(title="Accuracy by Condition (React mode)", show_lines=True)
    table.add_column("Condition", style="bold", width=22)
    for a in react_aggs:
        table.add_column(a.run_name, justify="center")

    for cond in conditions:
        row = [cond]
        for a in react_aggs:
            cd = a.by_condition.get(cond, {})
            if cd:
                row.append(f"{cd['top1']:.0%} (${cd['mean_cost']:,.0f})")
            else:
                row.append("—")
        table.add_row(*row)

    console.print(table)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

@app.command()
def main(
    results_dir: str = typer.Option("results/v4_comparison", help="Results directory"),
):
    results_path = REPO_ROOT / results_dir
    merged_file = results_path / "merged_results.json"

    if not merged_file.exists():
        console.print(f"[red]No merged_results.json in {results_path}[/red]")
        raise typer.Exit(1)

    data = json.loads(merged_file.read_text())
    results = data["results"]
    config = data["config"]

    console.print(Panel(
        f"[bold]NeuroBench v4 Analysis[/bold]\n"
        f"Dataset: {config.get('dataset', 'v4')}  |  Hospital: {config.get('hospital', '?')}  |  "
        f"Cases: {config.get('total_cases', '?')}  |  Repeats: {config.get('repeats', '?')}\n"
        f"Total results: {len(results)}",
        title="Configuration",
    ))

    run_names = sorted(set(r["run_name"] for r in results))
    aggs = [compute_run_agg(results, rn) for rn in run_names]

    # -----------------------------------------------------------------------
    # 1. Main comparison table
    # -----------------------------------------------------------------------
    console.print("\n")
    print_main_comparison(aggs)

    # -----------------------------------------------------------------------
    # 2. Difficulty breakdown
    # -----------------------------------------------------------------------
    console.print("\n")
    print_difficulty_table(aggs)

    # -----------------------------------------------------------------------
    # 3. Condition breakdown (react only)
    # -----------------------------------------------------------------------
    console.print("\n")
    print_condition_table(aggs)

    # -----------------------------------------------------------------------
    # 4. React vs No-Tools comparison
    # -----------------------------------------------------------------------
    console.print("\n")
    react_vs = analyze_react_vs_no_tools(results)
    table = Table(title="React (Tools) vs No-Tools — Diagnostic Accuracy Delta", show_lines=True)
    table.add_column("Model", style="bold")
    table.add_column("React Top-1", justify="right")
    table.add_column("No-Tools Top-1", justify="right")
    table.add_column("Delta", justify="right")
    table.add_column("React Cost", justify="right")
    table.add_column("React Time", justify="right")
    table.add_column("No-Tools Time", justify="right")

    for model, comp in react_vs.items():
        delta_color = "green" if comp["delta_top1"] > 0 else "red" if comp["delta_top1"] < 0 else "white"
        table.add_row(
            model,
            f"{comp['react']['top1']:.0%}",
            f"{comp['no_tools']['top1']:.0%}",
            f"[{delta_color}]{comp['delta_top1']:+.1%}[/{delta_color}]",
            f"${comp['react']['mean_cost']:,.0f}",
            f"{comp['react']['mean_time']:.0f}s",
            f"{comp['no_tools']['mean_time']:.0f}s",
        )
    console.print(table)

    # -----------------------------------------------------------------------
    # 5. New tools impact
    # -----------------------------------------------------------------------
    console.print("\n")
    new_impact = analyze_new_tools_impact(results)
    console.print(Panel(
        f"React cases using new tools: {new_impact['n_used_new_tools']}/{new_impact['n_react_total']} "
        f"({new_impact['pct_using_new']}%)\n"
        f"Top-1 with new tools: {new_impact['top1_with_new']:.0%}  |  "
        f"Top-1 without: {new_impact['top1_without_new']:.0%}",
        title="New Tools (CT, Echo, Cardiac Mon, Adv Imaging, Specialized) Impact",
    ))

    if new_impact["per_tool"]:
        table = Table(title="New Tool Usage Breakdown", show_lines=True)
        table.add_column("Tool", style="bold")
        table.add_column("Uses", justify="right")
        table.add_column("% React", justify="right")
        table.add_column("Top-1 When Used", justify="right")

        for tool, info in new_impact["per_tool"].items():
            table.add_row(
                tool, str(info["n_uses"]),
                f"{info['pct_of_react_cases']}%",
                f"{info['top1_when_used']:.0%}",
            )
        console.print(table)

    # -----------------------------------------------------------------------
    # 6. Cost analysis by condition
    # -----------------------------------------------------------------------
    console.print("\n")
    cost_by_cond = analyze_cost_by_condition(results)
    table = Table(title="Cost Analysis by Condition (React mode)", show_lines=True)
    table.add_column("Condition", style="bold", width=20)
    table.add_column("Mean $", justify="right")
    table.add_column("Median $", justify="right")
    table.add_column("Min $", justify="right")
    table.add_column("Max $", justify="right")
    table.add_column("Top-1", justify="right")
    table.add_column("Top Tools")

    for cond, info in sorted(cost_by_cond.items()):
        top_tools = ", ".join(f"{t}({n})" for t, n in list(info["top_tools"].items())[:3])
        table.add_row(
            cond, f"${info['mean_cost']:,.0f}", f"${info['median_cost']:,.0f}",
            f"${info['min_cost']:,.0f}", f"${info['max_cost']:,.0f}",
            f"{info['top1_accuracy']:.0%}",
            top_tools,
        )
    console.print(table)

    # -----------------------------------------------------------------------
    # 7. Tool usage patterns
    # -----------------------------------------------------------------------
    console.print("\n")
    tool_patterns = analyze_tool_usage_patterns(results)
    table = Table(title="Tool Usage Patterns (React mode)", show_lines=True)
    table.add_column("Run", style="bold", width=22)
    table.add_column("Avg Tools", justify="right")
    table.add_column("Unique", justify="right")
    table.add_column("Top 5 Tools (freq/case)")

    for run, info in tool_patterns.items():
        top5 = ", ".join(f"{t}({f})" for t, f in list(info["tools_per_case"].items())[:5])
        table.add_row(run, f"{info['mean_tools_per_case']}", str(info["unique_tools_used"]), top5)
    console.print(table)

    # -----------------------------------------------------------------------
    # 8. Hardest cases
    # -----------------------------------------------------------------------
    console.print("\n")
    hardest = find_hardest_cases(results, 15)
    table = Table(title="Hardest Cases (lowest accuracy across all models)", show_lines=True)
    table.add_column("Case", style="bold")
    table.add_column("Condition")
    table.add_column("Difficulty")
    table.add_column("Top-1 Rate", justify="right")
    table.add_column("Correct/Total", justify="right")
    table.add_column("GT Diagnosis")

    for c in hardest:
        table.add_row(
            c["case_id"], c["condition"], c["difficulty"][:6],
            f"{c['top1_rate']:.0%}", f"{c['n_correct']}/{c['n_runs']}",
            c["gt_diagnosis"][:50],
        )
    console.print(table)

    # -----------------------------------------------------------------------
    # 9. Most expensive cases
    # -----------------------------------------------------------------------
    console.print("\n")
    expensive = find_expensive_cases(results, 10)
    table = Table(title="Most Expensive Cases (React mode)", show_lines=True)
    table.add_column("Case", style="bold")
    table.add_column("Condition")
    table.add_column("Difficulty")
    table.add_column("Mean Cost", justify="right")
    table.add_column("Top-1 Rate", justify="right")
    table.add_column("Tools", justify="right")

    for c in expensive:
        table.add_row(
            c["case_id"], c["condition"], c["difficulty"][:6],
            f"${c['mean_cost_usd']:,.0f}", f"{c['top1_rate']:.0%}",
            f"{c['mean_tools']:.1f}",
        )
    console.print(table)

    # -----------------------------------------------------------------------
    # 10. Consistency analysis
    # -----------------------------------------------------------------------
    console.print("\n")
    table = Table(title="Diagnostic Consistency (3 repeats)", show_lines=True)
    table.add_column("Run", style="bold", width=22)
    table.add_column("Always Correct", justify="right", style="green")
    table.add_column("Always Wrong", justify="right", style="red")
    table.add_column("Inconsistent", justify="right", style="yellow")
    table.add_column("Consistency", justify="right")

    for a in aggs:
        table.add_row(
            a.run_name,
            str(a.always_correct),
            str(a.always_wrong),
            str(a.inconsistent),
            f"{a.consistency_rate:.0%}",
        )
    console.print(table)

    # -----------------------------------------------------------------------
    # Save full analysis report
    # -----------------------------------------------------------------------
    analysis_dir = results_path / "analysis"
    analysis_dir.mkdir(exist_ok=True)

    report = {
        "config": config,
        "total_results": len(results),
        "run_aggregates": {a.run_name: asdict(a) for a in aggs},
        "react_vs_no_tools": react_vs,
        "new_tools_impact": new_impact,
        "cost_by_condition": cost_by_cond,
        "tool_usage_patterns": tool_patterns,
        "hardest_cases": hardest,
        "most_expensive_cases": expensive,
    }

    report_file = analysis_dir / "full_analysis.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2, default=str)
    console.print(f"\n[green]Full analysis saved to {report_file}[/green]")

    # Save per-run CSVish flat records for plotting
    flat = []
    for r in results:
        flat.append({
            "case_id": r["case_id"],
            "condition": r["condition"],
            "difficulty": r["difficulty"],
            "run_name": r["run_name"],
            "model": r["model"],
            "mode": r["mode"],
            "repeat": r["repeat"],
            "top1": r["diagnostic_accuracy_top1"],
            "top3": r["diagnostic_accuracy_top3"],
            "critical_hit": round(r["critical_actions_hit"], 3),
            "safety": round(r["safety_score"], 3),
            "tool_calls": r["tool_call_count"],
            "cost_usd": round(r["total_cost_usd"], 2),
            "cost_efficiency": round(r["cost_efficiency"], 3),
            "protocol_compliance": r["protocol_compliance"],
            "tokens": r["total_tokens"],
            "time_s": round(r["elapsed_seconds"], 1),
        })
    flat_file = analysis_dir / "flat_results.json"
    with open(flat_file, "w") as f:
        json.dump(flat, f, indent=2)
    console.print(f"[green]Flat results for plotting saved to {flat_file}[/green]")

    console.print(f"\n[bold]Analysis complete. {len(results)} results analyzed across {len(aggs)} configurations.[/bold]")


if __name__ == "__main__":
    app()
