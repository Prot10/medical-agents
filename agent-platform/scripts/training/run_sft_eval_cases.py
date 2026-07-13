"""Evaluate a model on a held-out split (default: the 100-case test set) and compare runs.

Usage:
    # Run evaluation
    python agent-platform/scripts/training/run_sft_eval_cases.py \
        --model-id Qwen/Qwen3.5-9B \
        --run-name base-qwen3.5-9b \
        --output results/sft_eval/base_results.json

    # Compare two runs
    python agent-platform/scripts/training/run_sft_eval_cases.py \
        --compare \
        --base-results results/sft_eval/base_results.json \
        --sft-results results/sft_eval/sft_results.json \
        --output results/sft_eval/comparison.json
"""

from __future__ import annotations

import json
import logging
import math
import os
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table

# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[3]
AGENT_PLATFORM = REPO_ROOT / "agent-platform"
sys.path.insert(0, str(AGENT_PLATFORM / "src"))
sys.path.insert(0, str(REPO_ROOT / "packages" / "neuroagent-schemas" / "src"))

from neuroagent_schemas import NeuroBenchCase

from neuroagent.agent.orchestrator import AgentOrchestrator, load_agent_config
from neuroagent.evaluation.metrics import MetricsCalculator
from neuroagent.evaluation.runner import format_patient_info
from neuroagent.rules.rules_engine import RulesEngine
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.tool_registry import ToolRegistry

if TYPE_CHECKING:
    from neuroagent.agent.config import AgentConfig

app = typer.Typer()
console = Console()
logger = logging.getLogger("sft_eval")


def _atomic_write_text(path: Path, text: str) -> None:
    """Write via a same-directory temp file + os.replace, so a crash mid-write
    (these runs take hours) never leaves a truncated/corrupt JSON behind."""
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)

DATASET_PATH = REPO_ROOT / "data" / "neurobench"
SPLITS_DIR = DATASET_PATH / "splits"


def load_split_cases(split: str = "test") -> list[NeuroBenchCase]:
    """Load the held-out cases named in `{split}_cases.txt`.

    The default is the 100-case test split — the cases no trajectory was ever generated for,
    so evaluating on them measures generalisation rather than memorisation. There is no
    silent fallback to "all cases": scoring a model on its own training data would look like
    a huge gain and be meaningless.
    """
    cases_dir = DATASET_PATH / "cases"
    split_file = SPLITS_DIR / f"{split}_cases.txt"
    if not split_file.exists():
        raise FileNotFoundError(
            f"No split file at {split_file}. Available: "
            f"{[p.name for p in SPLITS_DIR.glob('*_cases.txt')]}"
        )
    case_ids = [c for c in split_file.read_text().split() if c]
    cases = []
    for cid in case_ids:
        path = cases_dir / f"{cid}.json"
        if path.exists():
            cases.append(NeuroBenchCase.model_validate(json.loads(path.read_text())))
        else:
            logger.warning("Case not found: %s", cid)
    if not cases:
        raise RuntimeError(f"{split_file} named {len(case_ids)} cases but none loaded")
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


def write_judge_bundle(
    bundle_dir: Path, case: NeuroBenchCase, trace, run_name: str, rep: int, model_id: str
) -> None:
    """One bundle per (case, rep) with the FULL reasoning trace, for the llm-judge composite.

    Schema matches run_baseline_eval.py / the llm-judge agent contract so the same
    prepare_judge_batches → llm-judge → aggregate_judge_scores pipeline consumes it.
    """
    raw = json.loads(case.model_dump_json())
    bundle = {
        "case_id": case.case_id,
        "condition": case.condition.value,
        "difficulty": case.difficulty.value,
        "case_presentation": {
            "patient": raw["patient"],
            "encounter_type": raw.get("encounter_type"),
        },
        "ground_truth": raw["ground_truth"],
        "runs": [
            {
                "run_name": f"{run_name}-rep{rep}",
                "model_id": model_id,
                "mode": "react",
                "final_response": trace.final_response,
                "tools_called": list(trace.tools_called),
                "total_tool_calls": trace.total_tool_calls,
                "elapsed_time_seconds": round(trace.elapsed_time_seconds, 2),
                "trace": {
                    "num_turns": len(trace.turns),
                    "turns": [
                        {
                            "turn_number": t.turn_number,
                            "role": t.role,
                            "content": t.content,
                            "tool_calls": t.tool_calls,
                            "tool_results": t.tool_results,
                        }
                        for t in trace.turns
                    ],
                },
            }
        ],
    }
    bundle_dir.mkdir(parents=True, exist_ok=True)
    (bundle_dir / f"{case.case_id}_rep{rep}.json").write_text(
        json.dumps(bundle, indent=2, default=str)
    )


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
    split: str = typer.Option("test", help="Which split_cases.txt to evaluate (default: held-out test)"),
    temperature: float = typer.Option(1.0, help="Sampling temperature (0 = greedy/deterministic)"),
    presence_penalty: float = typer.Option(1.5, help="Presence penalty (set 0 for greedy)"),
    save_bundles: bool = typer.Option(True, help="Write per-case judge bundles (full trace) for the composite score"),
    rollout_jsonl: str = typer.Option(None, help="RFT: append every rollout's training-format messages + correctness here"),
):
    """Run agent evaluation on a held-out split (default: the 100-case test set).

    Doubles as the RFT rollout generator: point --split at the TRAIN split, use --repeats N
    and --temperature 0.7, and pass --rollout-jsonl to dump each sampled trajectory (the exact
    conversation) with its correctness label. build_rft_dataset.py then filters to the correct
    ones and formats them for SFT.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    cases = load_split_cases(split)
    greedy = temperature == 0.0
    console.print(
        f"\n[bold]Evaluating {run_name} on {len(cases)} {split} cases × {repeats} repeats "
        f"(temp={temperature}{' greedy' if greedy else ''})[/bold]"
    )

    config = load_agent_config(
        base_url=f"http://localhost:{port}/v1",
        api_key="not-needed",
        model=model_id,
        max_tokens=8192,
        temperature=temperature,
        # top_p must be 1.0 for true greedy; presence_penalty off so decoding is deterministic.
        top_p=1.0 if greedy else 0.95,
        presence_penalty=0.0 if greedy else presence_penalty,
        hospital=hospital,
    )

    bundle_dir = Path(output).parent / "judge_bundles" / run_name if save_bundles else None

    all_results: list[CaseResult] = []
    checkpoint_file = Path(output).with_suffix(".checkpoint.json")
    completed: set[str] = set()

    if checkpoint_file.exists():
        ckpt = json.loads(checkpoint_file.read_text())
        completed = set(ckpt.get("completed", []))
        all_results = [CaseResult(**r) for r in ckpt.get("results", [])]
        console.print(f"[yellow]Resuming: {len(completed)} already done[/yellow]")

    total = len(cases) * repeats
    correct = sum(1 for r in all_results if r.diagnostic_accuracy_top1)

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None),
        MofNCompleteColumn(),
        TextColumn("[green]top1 {task.fields[acc]}"),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("eta"),
        TimeRemainingColumn(),
        console=console,
    )

    def _acc() -> str:
        n = len(all_results)
        return f"{correct}/{n} ({100 * correct / n:.0f}%)" if n else "0/0"

    with progress:
        task = progress.add_task(
            f"{run_name}", total=total, completed=len(completed), acc=_acc()
        )
        for rep in range(1, repeats + 1):
            for case in cases:
                run_key = f"{run_name}|{case.case_id}|rep{rep}"
                if run_key in completed:
                    continue

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
                    correct += int(metrics.diagnostic_accuracy_top1)

                    if bundle_dir is not None:
                        write_judge_bundle(bundle_dir, case, trace, run_name, rep, model_id)

                    if rollout_jsonl and trace.messages:
                        with open(rollout_jsonl, "a") as fh:
                            fh.write(json.dumps({
                                "case_id": case.case_id,
                                "condition": case.condition.value,
                                "difficulty": case.difficulty.value,
                                "repeat": rep,
                                "correct": bool(metrics.diagnostic_accuracy_top1),
                                "num_tool_calls": metrics.tool_call_count,
                                "messages": trace.messages,
                            }, default=str) + "\n")

                    _atomic_write_text(checkpoint_file, json.dumps({
                        "completed": sorted(completed),
                        "results": [asdict(r) for r in all_results],
                    }, default=str))

                    dx = "[green]✓[/green]" if metrics.diagnostic_accuracy_top1 else "[red]✗[/red]"
                    progress.console.print(
                        f"  {dx} [dim]{case.case_id:<16} rep{rep}[/dim]  "
                        f"tools={metrics.tool_call_count:<2} safety={metrics.safety_score:.2f} "
                        f"${metrics.total_cost_usd:,.0f} {elapsed:.0f}s"
                    )
                except Exception as e:
                    progress.console.print(f"  [red]✗ {case.case_id} rep{rep} FAILED: {e}[/red]")
                    logger.exception("Case %s rep%d failed", case.case_id, rep)

                progress.update(task, advance=1, acc=_acc())

    # Save final results
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(out_path, json.dumps({
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

    # Statistical significance — base and SFT see the SAME cases, so the comparison is PAIRED.
    stats = _paired_significance(base_data, sft_data)
    if stats:
        console.print("\n[bold]Significance (paired, top-1):[/bold]")
        console.print(
            f"  Δ top1 = {stats['delta']:+.1%}   "
            f"95% bootstrap CI [{stats['ci_low']:+.1%}, {stats['ci_high']:+.1%}]   "
            f"{'[green]significant[/]' if stats['significant'] else '[yellow]not significant (CI spans 0)[/]'}"
        )
        console.print(
            f"  McNemar: base-only-correct={stats['base_only']}  sft-only-correct={stats['sft_only']}  "
            f"exact p={stats['mcnemar_p']:.3f}"
        )
        if stats.get("reliability") is not None:
            r = stats["reliability"]
            console.print(
                f"  Reliability (per-case pass-rate SD across repeats): "
                f"base={r['base_sd']:.3f}  sft={r['sft_sd']:.3f}  "
                f"({'[green]SFT more consistent[/]' if r['sft_sd'] < r['base_sd'] else 'base more consistent'})"
            )

    # Per-difficulty breakdown — DESCRIPTIVE ONLY. These subgroup deltas carry no
    # significance test (the paired stats above cover the overall top-1 delta only)
    # and the per-group n is far too small to support a claim. Never cite them as
    # findings.
    console.print(
        "\n[bold]Per-difficulty Top-1 Accuracy[/bold] "
        "[dim](descriptive, no significance test — do not cite as findings)[/dim]"
    )
    for diff in ["straightforward", "moderate", "diagnostic_puzzle"]:
        base_diff = [r for r in base_data if r["difficulty"] == diff]
        sft_diff = [r for r in sft_data if r["difficulty"] == diff]
        if base_diff and sft_diff:
            ba = sum(1 for r in base_diff if r["diagnostic_accuracy_top1"]) / len(base_diff)
            sa = sum(1 for r in sft_diff if r["diagnostic_accuracy_top1"]) / len(sft_diff)
            delta = sa - ba
            color = "green" if delta > 0 else ("red" if delta < 0 else "white")
            console.print(
                f"  {diff:20s}  base={ba:.0%}  sft={sa:.0%}  [{color}]Δ={delta:+.0%}[/]  "
                f"[dim](descriptive, no significance test; n={len(base_diff)} results/arm)[/dim]"
            )

    # Per-condition breakdown — DESCRIPTIVE ONLY, same caveat as above.
    console.print(
        "\n[bold]Per-condition Top-1 Accuracy[/bold] "
        "[dim](descriptive, no significance test; small n per condition — do not cite as findings)[/dim]"
    )
    conditions = sorted(set(r["condition"] for r in base_data))
    table2 = Table(
        show_lines=True,
        caption="Descriptive only — no per-condition significance test; do not cite as findings.",
    )
    table2.add_column("Condition", style="bold")
    table2.add_column("n/arm", justify="right")
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
            table2.add_row(cond, str(len(bc)), f"{ba:.0%}", f"{sa:.0%}",
                           f"[{color}]{delta:+.0%}[/]" if color else f"{delta:+.0%}")

    console.print(table2)

    # Save comparison
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "base": {"run_name": base["run_name"], "metrics": base_metrics},
        "sft": {"run_name": sft["run_name"], "metrics": sft_metrics},
        "significance": stats,
    }, indent=2, default=str))
    console.print(f"\n[green]Comparison saved to {output}[/green]")


def _paired_significance(base_data: list[dict], sft_data: list[dict], n_boot: int = 10000) -> dict:
    """Paired top-1 comparison: bootstrap CI over cases, McNemar, and repeat-reliability.

    base and SFT are evaluated on the SAME cases, so pairing by case_id controls for case
    difficulty and is far more powerful than treating the two as independent samples.
    """
    import random
    import statistics as st
    from collections import defaultdict

    def by_case(data):
        d = defaultdict(list)
        for r in data:
            d[r["case_id"]].append(int(bool(r["diagnostic_accuracy_top1"])))
        return d

    b, s = by_case(base_data), by_case(sft_data)
    cases = sorted(set(b) & set(s))
    if not cases:
        return {}

    # Per-case pass rate (mean over repeats), paired.
    b_rate = {c: st.mean(b[c]) for c in cases}
    s_rate = {c: st.mean(s[c]) for c in cases}
    diffs = [s_rate[c] - b_rate[c] for c in cases]
    delta = st.mean(diffs)

    # Paired bootstrap over cases (resample cases, not rows — preserves pairing).
    rng = random.Random(0)
    n = len(cases)
    boot = []
    for _ in range(n_boot):
        sample = [diffs[rng.randrange(n)] for _ in range(n)]
        boot.append(sum(sample) / n)
    boot.sort()
    ci_low = boot[int(0.025 * n_boot)]
    ci_high = boot[int(0.975 * n_boot)]

    # McNemar on the per-case majority vote; exact two-sided binomial on the discordant pairs.
    b_maj = {c: (1 if b_rate[c] >= 0.5 else 0) for c in cases}
    s_maj = {c: (1 if s_rate[c] >= 0.5 else 0) for c in cases}
    base_only = sum(1 for c in cases if b_maj[c] and not s_maj[c])
    sft_only = sum(1 for c in cases if s_maj[c] and not b_maj[c])
    nd = base_only + sft_only
    k = min(base_only, sft_only)
    # exact two-sided binomial p at rate 0.5
    p = min(1.0, 2 * sum(math.comb(nd, i) for i in range(0, k + 1)) / (2 ** nd)) if nd else 1.0

    reliability = None
    reps = max(len(b[c]) for c in cases)
    if reps > 1:
        reliability = {
            "base_sd": st.mean([st.pstdev(b[c]) for c in cases if len(b[c]) > 1]),
            "sft_sd": st.mean([st.pstdev(s[c]) for c in cases if len(s[c]) > 1]),
        }

    return {
        "n_cases": n,
        "delta": delta,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "significant": ci_low > 0 or ci_high < 0,
        "base_only": base_only,
        "sft_only": sft_only,
        "mcnemar_p": p,
        "reliability": reliability,
    }


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
