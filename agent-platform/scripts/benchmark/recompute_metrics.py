"""Recompute rule-based CaseMetrics for every saved trace.

Use after editing MetricsCalculator (e.g. the cost_efficiency fix). Walks
<run_dir>/<model>/traces/*.json, reconstructs the AgentTrace, recomputes
CaseMetrics from the v5 case JSON, and overwrites both
  <run_dir>/<model>/metrics/<case>_repN.json
  <run_dir>/<model>/traces/<case>_repN.json  (the embedded `metrics` block)

No inference is re-run; this is purely re-evaluating the saved traces.
The model-level summary.json is then refreshed by re-running over the
metrics directory.
"""

from __future__ import annotations

import json
import statistics
import sys
from dataclasses import asdict
from pathlib import Path

import typer
from rich.console import Console

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "agent-platform" / "src"))
sys.path.insert(0, str(REPO / "packages" / "neuroagent-schemas" / "src"))

from neuroagent_schemas import NeuroBenchCase
from neuroagent.agent.reasoning import AgentTrace, AgentTurn
from neuroagent.evaluation.metrics import MetricsCalculator

app = typer.Typer(add_completion=False)
console = Console()


def _trace_from_saved(d: dict) -> AgentTrace:
    t = AgentTrace(case_id=d["case_id"])
    t.total_tokens = d.get("total_tokens", 0)
    t.total_tool_calls = d.get("total_tool_calls", 0)
    t.tools_called = list(d.get("tools_called", []))
    t.final_response = d.get("final_response") or ""
    t.elapsed_time_seconds = d.get("elapsed_time_seconds", 0)
    t.total_cost_usd = d.get("total_cost_usd", 0)
    for turn in d.get("turns", []):
        t.turns.append(AgentTurn(
            turn_number=turn.get("turn_number", 0),
            role=turn.get("role", "assistant"),
            content=turn.get("content"),
            tool_calls=turn.get("tool_calls"),
            tool_results=turn.get("tool_results"),
            token_usage=turn.get("token_usage"),
        ))
    return t


def _summarize_model(model_dir: Path, model_id: str) -> dict:
    metric_files = sorted((model_dir / "metrics").glob("*.json"))
    if not metric_files:
        return {"n_traces": 0, "model": model_dir.name, "model_id": model_id}
    metrics = [json.loads(mf.read_text()) for mf in metric_files]
    n = len(metrics)

    def mean(key: str) -> float:
        vals = [m.get(key, 0) or 0 for m in metrics]
        return round(sum(vals) / n, 4)

    out = {"n_traces": n}
    for key in [
        "diagnostic_accuracy_top1", "diagnostic_accuracy_top3",
        "action_precision", "action_recall", "tool_f1", "required_coverage",
        "useless_call_rate", "harmful_calls", "redundancy_rate",
        "premature_closure_count", "sequence_violations", "hard_sequence_violations",
        "critical_actions_hit", "contraindicated_actions_taken",
        "efficiency_score", "safety_score",
        "total_cost_usd", "cost_efficiency",
        "tool_call_count", "specialist_calls",
    ]:
        out[key] = mean(key)
    out["model"] = model_dir.name
    out["model_id"] = model_id
    return out


@app.command()
def main(
    run_dir: str = typer.Option(..., help="Baseline run directory."),
    dataset_dir: str = typer.Option(
        str(REPO / "data" / "neurobench"),
        help="NeuroBench dataset directory holding cases/<case_id>.json",
    ),
) -> None:
    base = Path(run_dir)
    cases_dir = Path(dataset_dir) / "cases"
    cfg = json.loads((base / "config.json").read_text())

    calc = MetricsCalculator()
    for model_key in cfg["models"]:
        mdir = base / model_key
        traces_dir = mdir / "traces"
        metrics_dir = mdir / "metrics"
        if not traces_dir.exists():
            continue

        # Cache cases lazily.
        loaded_cases: dict[str, NeuroBenchCase] = {}
        n, changed = 0, 0

        for tf in sorted(traces_dir.glob("*.json")):
            full = json.loads(tf.read_text())
            cid = full["case_id"]
            if cid not in loaded_cases:
                loaded_cases[cid] = NeuroBenchCase.model_validate_json(
                    (cases_dir / f"{cid}.json").read_text()
                )
            case = loaded_cases[cid]
            trace = _trace_from_saved(full)

            old_metrics = full.get("metrics", {})
            new_metrics = asdict(calc.compute_all(
                trace=trace,
                ground_truth=case.ground_truth,
                condition=case.condition.value,
            ))

            # Detect changes for a summary line.
            if any(old_metrics.get(k) != new_metrics.get(k)
                   for k in new_metrics if not isinstance(new_metrics[k], (dict, list))):
                changed += 1

            # Write the trace + metrics back in the same dual layout.
            full["metrics"] = new_metrics
            tf.write_text(json.dumps(full, indent=2, default=str))
            (metrics_dir / tf.name).write_text(json.dumps(new_metrics, indent=2, default=str))
            n += 1

        # Refresh model-level summary.
        summary = _summarize_model(mdir, cfg["model_ids"].get(model_key, ""))
        summary["errors_count"] = 0
        (mdir / "summary.json").write_text(json.dumps(summary, indent=2))
        console.print(f"  [cyan]{model_key}[/cyan]: recomputed {n} traces, {changed} changed")

    console.print("[green]Done. Re-run aggregate_judge_scores.py + final_rollup.py to refresh judge merges.[/green]")


if __name__ == "__main__":
    app()
