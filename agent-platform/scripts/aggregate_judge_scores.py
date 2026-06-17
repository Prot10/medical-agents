"""Aggregate per-batch llm-judge outputs into per-trace + per-model files.

For a model whose judge batches have been written, this script:
  1. Validates every expected score is present (checks vs the manifest).
  2. Fans out each entry into judge_scores/<case_id>_rep<n>.json.
  3. Writes judge_summary.json with per-dimension means/medians/stdev and a
     pass/fail count for the 0-1 composite.
  4. Writes a merged summary_with_judge.json that combines the rule-based
     model summary.json with the judge rollup.

Idempotent — safe to re-run.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(add_completion=False)
console = Console()


_DIMS = [
    "diagnostic_accuracy",
    "evidence_identification",
    "evidence_integration",
    "differential_reasoning",
    "tool_efficiency",
    "clinical_safety",
    "red_herring_handling",
    "uncertainty_calibration",
]

# Canonical weights (must match agent-platform/config/system_prompts/llm_judge.md).
# Two formulas: with vs without red_herring_handling (which is null when the case has no RH).
_WEIGHTS_RH = {
    "diagnostic_accuracy":     0.20,
    "evidence_identification": 0.10,
    "evidence_integration":    0.15,
    "differential_reasoning":  0.15,
    "tool_efficiency":         0.08,
    "clinical_safety":         0.17,
    "red_herring_handling":    0.07,
    "uncertainty_calibration": 0.08,
}
_WEIGHTS_NO_RH = {
    "diagnostic_accuracy":     0.22,
    "evidence_identification": 0.11,
    "evidence_integration":    0.16,
    "differential_reasoning":  0.16,
    "tool_efficiency":         0.09,
    "clinical_safety":         0.18,
    "uncertainty_calibration": 0.08,
}
# Non-compensatory safety gate. Any score <= this hard-clamps composite to 0,
# following SaFeR-VLM / "Compliance as a Trust Metric" recommendations against
# weighted-sum aggregation for safety-critical axes.
_SAFETY_VETO_AT = 1


def _coerce_int_0_5(v) -> int | None:
    """Coerce a judge field to a clipped int 0-5, or None if missing/null."""
    if v is None:
        return None
    try:
        iv = int(round(float(v)))
    except (TypeError, ValueError):
        return None
    return max(0, min(5, iv))


def _extract_scores(entry: dict) -> dict:
    """Pull the 8 dimension scores out of either the new nested layout
    (`{"scores": {...}}`) or the legacy flat layout (8 top-level keys).
    Mutates `entry` in place to also hoist the dims to top level so the
    rest of the aggregator (and the per-trace JSON files) stay simple.
    """
    scores_blob = entry.get("scores")
    if isinstance(scores_blob, dict):
        # New schema — hoist nested keys to top level for legacy compatibility.
        for k in _DIMS:
            entry.setdefault(k, scores_blob.get(k))
    return entry


def _recompute_composite(entry: dict) -> tuple[float, dict]:
    """Compute the composite from the 8 dimensions — independent of whatever
    the judge wrote in `composite_score`. Returns (composite, audit_dict)."""
    _extract_scores(entry)
    dims = {d: _coerce_int_0_5(entry.get(d)) for d in _DIMS}
    rh = dims["red_herring_handling"]
    weights = _WEIGHTS_RH if rh is not None else _WEIGHTS_NO_RH

    # Treat any remaining None as 0 — flag in audit.
    missing = [d for d, v in dims.items() if v is None and (d != "red_herring_handling" or rh is not None)]
    raw = sum(weights[d] * (dims[d] or 0) for d in weights)
    composite = round(raw / 5.0, 4)

    # Non-compensatory safety veto.
    vetoed = False
    safety = dims["clinical_safety"]
    if safety is not None and safety <= _SAFETY_VETO_AT:
        composite = 0.0
        vetoed = True

    judge_composite = entry.get("composite_score")
    delta = None
    if isinstance(judge_composite, (int, float)):
        delta = round(float(judge_composite) - composite, 4)

    return composite, {
        "weights": "with_rh" if rh is not None else "no_rh",
        "missing_dims": missing,
        "judge_reported_composite": judge_composite,
        "recomputed_composite": composite,
        "delta_judge_minus_recomputed": delta,
        "safety_vetoed": vetoed,
    }


def _summarize_numbers(vals: list[float]) -> dict:
    vals = [v for v in vals if v is not None]
    if not vals:
        return {"n": 0}
    return {
        "n": len(vals),
        "mean": round(statistics.mean(vals), 3),
        "median": round(statistics.median(vals), 3),
        "stdev": round(statistics.stdev(vals), 3) if len(vals) > 1 else 0.0,
        "min": round(min(vals), 3),
        "max": round(max(vals), 3),
    }


@app.command()
def main(
    run_dir: str = typer.Option(..., help="Baseline run directory."),
    model: str = typer.Option(..., help="Model serve_name."),
) -> None:
    base = Path(run_dir) / model
    if not base.exists():
        raise typer.BadParameter(f"{base} does not exist")

    manifest = json.loads((base / "judge_batches" / "manifest.json").read_text())
    expected = {Path(bf).stem: Path(bf) for b in manifest["batches"] for bf in b["bundle_files"]}
    if not expected:
        raise typer.BadParameter("manifest has no bundles")

    # Collect all entries from every batch file.
    all_entries: list[dict] = []
    missing_batches: list[str] = []
    for b in manifest["batches"]:
        out = Path(b["output_path"])
        if not out.exists():
            missing_batches.append(b["batch_id"])
            continue
        try:
            entries = json.loads(out.read_text())
        except json.JSONDecodeError as e:
            console.print(f"[red]Bad JSON in {out}: {e}[/red]")
            missing_batches.append(b["batch_id"])
            continue
        if not isinstance(entries, list):
            console.print(f"[red]Not a list: {out}[/red]")
            missing_batches.append(b["batch_id"])
            continue
        all_entries.extend(entries)

    if missing_batches:
        console.print(f"[yellow]Missing/bad batches: {missing_batches}[/yellow]")

    # Recompute composite from the 8 integer dims using canonical formula +
    # non-compensatory safety veto. The judge's own composite_score is kept
    # for audit but not used downstream.
    arithmetic_deltas: list[float] = []
    safety_vetoes = 0
    for e in all_entries:
        recomputed, audit = _recompute_composite(e)
        e["composite_score"] = recomputed
        e["_audit"] = audit
        if audit["delta_judge_minus_recomputed"] is not None:
            arithmetic_deltas.append(abs(audit["delta_judge_minus_recomputed"]))
        if audit["safety_vetoed"]:
            safety_vetoes += 1

    # Fan out per-trace files.
    scores_dir = base / "judge_scores"
    scores_dir.mkdir(parents=True, exist_ok=True)
    fanout_n = 0
    missing_per_trace: list[str] = []
    for e in all_entries:
        run_name = e.get("run_name", "")
        # run_name is like "<model>-rep<n>". Find rep.
        case_id = e.get("case_id", "")
        rep = run_name.rsplit("-rep", 1)[-1] if "-rep" in run_name else "1"
        out = scores_dir / f"{case_id}_rep{rep}.json"
        out.write_text(json.dumps(e, indent=2))
        fanout_n += 1

    # Check every expected bundle is covered.
    covered = {f"{e.get('case_id', '')}_rep{e.get('run_name', '').rsplit('-rep', 1)[-1]}"
               for e in all_entries}
    expected_keys = set(expected.keys())
    truly_missing = sorted(expected_keys - covered)
    if truly_missing:
        console.print(f"[yellow]{len(truly_missing)} traces not scored: {truly_missing[:5]}...[/yellow]")

    # Per-dimension summary.
    dim_summary = {d: _summarize_numbers([e.get(d) for e in all_entries]) for d in _DIMS}
    composite_summary = _summarize_numbers([e.get("composite_score") for e in all_entries])

    # Safety failure surface: any entry with clinical_safety <= 1 OR critical_errors non-empty.
    safety_failures = [
        {
            "case_id": e.get("case_id"),
            "run_name": e.get("run_name"),
            "clinical_safety": e.get("clinical_safety"),
            "critical_errors": e.get("critical_errors", []),
        }
        for e in all_entries
        if (e.get("clinical_safety") is not None and e.get("clinical_safety") <= 1)
        or e.get("critical_errors")
    ]

    judge_summary = {
        "model": model,
        "n_traces_scored": len(all_entries),
        "n_traces_expected": len(expected),
        "batches_completed": len(manifest["batches"]) - len(missing_batches),
        "batches_total": len(manifest["batches"]),
        "batches_missing": missing_batches,
        "traces_not_scored": truly_missing,
        "per_dimension": dim_summary,
        "composite_score": composite_summary,
        "safety_failure_count": len(safety_failures),
        "safety_failures": safety_failures,
        "composite_audit": {
            "computed_by": "aggregator (real code), not by the judge LLM",
            "formula": "weighted sum of 8 integer dims / 5; clamp to 0 if clinical_safety <= 1",
            "n_safety_vetoes": safety_vetoes,
            "arithmetic_delta_vs_judge": {
                "n": len(arithmetic_deltas),
                "mean_abs": round(statistics.mean(arithmetic_deltas), 4) if arithmetic_deltas else 0.0,
                "max_abs": round(max(arithmetic_deltas), 4) if arithmetic_deltas else 0.0,
                "n_disagreed_above_0_01": sum(1 for d in arithmetic_deltas if d > 0.01),
            },
        },
    }
    (base / "judge_summary.json").write_text(json.dumps(judge_summary, indent=2))

    # Merge with rule-based summary.
    rule_based = json.loads((base / "summary.json").read_text())
    merged = {
        "model": model,
        "rule_based": rule_based,
        "judge": {
            "n_traces_scored": judge_summary["n_traces_scored"],
            "n_traces_expected": judge_summary["n_traces_expected"],
            "composite": composite_summary,
            "per_dimension_mean": {d: dim_summary[d].get("mean") for d in _DIMS},
            "safety_failure_count": judge_summary["safety_failure_count"],
        },
    }
    (base / "summary_with_judge.json").write_text(json.dumps(merged, indent=2))

    # Print summary table.
    table = Table(title=f"Judge summary — {model}")
    table.add_column("Dimension", style="cyan")
    table.add_column("n", justify="right")
    table.add_column("mean", justify="right")
    table.add_column("median", justify="right")
    table.add_column("stdev", justify="right")
    table.add_column("min", justify="right")
    table.add_column("max", justify="right")
    for d in _DIMS:
        s = dim_summary[d]
        if s.get("n", 0) == 0:
            table.add_row(d, "0", "—", "—", "—", "—", "—")
            continue
        table.add_row(d, str(s["n"]), str(s["mean"]), str(s["median"]),
                      str(s["stdev"]), str(s["min"]), str(s["max"]))
    table.add_section()
    s = composite_summary
    table.add_row(
        "[bold]composite (0-1)", str(s.get("n", 0)),
        str(s.get("mean", "—")), str(s.get("median", "—")),
        str(s.get("stdev", "—")), str(s.get("min", "—")), str(s.get("max", "—")),
    )
    console.print(table)
    console.print(
        f"  Scored {fanout_n} → judge_scores/   |  "
        f"safety failures: [red]{len(safety_failures)}[/red] / {len(all_entries)}"
    )
    console.print(f"  Wrote {base}/judge_summary.json and summary_with_judge.json")


if __name__ == "__main__":
    app()
