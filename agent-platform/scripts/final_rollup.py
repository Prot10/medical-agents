"""Cross-model rollup for a finished baseline_eval run.

Reads each model's summary_with_judge.json and writes:
  - final_summary.json: full programmatic rollup
  - final_summary.md: human-readable Markdown report (paper-style)

Usage:
  uv run python agent-platform/scripts/final_rollup.py --run-dir /eos/.../baseline_eval_<TS>
"""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def main(run_dir: str = typer.Option(...)) -> None:
    base = Path(run_dir)
    cfg = json.loads((base / "config.json").read_text())
    rows: list[dict] = []
    for model_key in cfg["models"]:
        merged_path = base / model_key / "summary_with_judge.json"
        if not merged_path.exists():
            console.print(f"[yellow]missing: {merged_path}[/yellow]")
            continue
        merged = json.loads(merged_path.read_text())
        rb = merged.get("rule_based", {})
        jd = merged.get("judge", {})
        rows.append({
            "model": model_key,
            "model_id": cfg["model_ids"].get(model_key, ""),
            # Rule-based headline
            "top1": rb.get("diagnostic_accuracy_top1", 0),
            "top3": rb.get("diagnostic_accuracy_top3", 0),
            "tool_f1": rb.get("tool_f1", 0),
            "required_coverage": rb.get("required_coverage", 0),
            "safety_rule": rb.get("safety_score", 0),
            "useless_call_rate": rb.get("useless_call_rate", 0),
            "harmful_calls": rb.get("harmful_calls", 0),
            "hard_sequence_violations": rb.get("hard_sequence_violations", 0),
            "tools_per_case": rb.get("tool_call_count", 0),
            "total_cost_usd": rb.get("total_cost_usd", 0),
            "cost_efficiency": rb.get("cost_efficiency", 0),
            # Judge
            "judge_composite": jd.get("composite", {}).get("mean", 0),
            "judge_composite_median": jd.get("composite", {}).get("median", 0),
            "judge_composite_stdev": jd.get("composite", {}).get("stdev", 0),
            "judge_dx_acc": jd.get("per_dimension_mean", {}).get("diagnostic_accuracy", 0),
            "judge_safety": jd.get("per_dimension_mean", {}).get("clinical_safety", 0),
            "judge_evi_integ": jd.get("per_dimension_mean", {}).get("evidence_integration", 0),
            "judge_tool_eff": jd.get("per_dimension_mean", {}).get("tool_efficiency", 0),
            "judge_rh": jd.get("per_dimension_mean", {}).get("red_herring_handling", 0),
            "judge_safety_failures": jd.get("safety_failure_count", 0),
            "n": jd.get("n_traces_scored", 0),
        })

    rows.sort(key=lambda r: -r["judge_composite"])

    final = {
        "run_dir": str(base),
        "started_at": cfg.get("started_at"),
        "num_cases": cfg.get("num_cases"),
        "reps": cfg.get("reps"),
        "hospital": cfg.get("hospital"),
        "mode": cfg.get("mode"),
        "models_ranked": rows,
    }
    (base / "final_summary.json").write_text(json.dumps(final, indent=2))

    # Pretty table to terminal
    table = Table(title=f"Baseline benchmark — {cfg.get('num_cases')} cases × {cfg.get('reps')} reps × {len(rows)} models")
    table.add_column("Rank", justify="right")
    table.add_column("Model", style="cyan")
    table.add_column("Judge composite", justify="right")
    table.add_column("Judge DA/5", justify="right")
    table.add_column("Judge Safety/5", justify="right")
    table.add_column("Top-1", justify="right")
    table.add_column("Top-3", justify="right")
    table.add_column("Tool F1", justify="right")
    table.add_column("Tools/case", justify="right")
    table.add_column("Safety fails", justify="right")
    for i, r in enumerate(rows, 1):
        table.add_row(
            str(i), r["model"],
            f"{r['judge_composite']:.3f}",
            f"{r['judge_dx_acc']:.2f}",
            f"{r['judge_safety']:.2f}",
            f"{r['top1']:.2%}",
            f"{r['top3']:.2%}",
            f"{r['tool_f1']:.2f}",
            f"{r['tools_per_case']:.1f}",
            f"{r['judge_safety_failures']}/{r['n']}",
        )
    console.print(table)

    # Markdown report
    md_lines = []
    md_lines.append(f"# NeuroBench v5 baseline — {cfg.get('num_cases')} cases × {cfg.get('reps')} reps × {len(rows)} base models")
    md_lines.append("")
    md_lines.append(f"- **Started**: {cfg.get('started_at')}")
    md_lines.append(f"- **Hospital**: {cfg.get('hospital')}")
    md_lines.append(f"- **Mode**: {cfg.get('mode')} (ReAct loop)")
    md_lines.append(f"- **Sampling**: temperature=1.0, top_p=0.95, presence_penalty=1.5")
    md_lines.append(f"- **Run dir**: `{base}`")
    md_lines.append("")
    md_lines.append("## Headline ranking (by LLM-judge composite)")
    md_lines.append("")
    md_lines.append("| Rank | Model | Judge composite | DA/5 | Safety/5 | Top-1 | Top-3 | Tool F1 | Tools/case | Safety fails |")
    md_lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        md_lines.append(
            f"| {i} | `{r['model']}` | **{r['judge_composite']:.3f}** | "
            f"{r['judge_dx_acc']:.2f} | {r['judge_safety']:.2f} | "
            f"{r['top1']:.2%} | {r['top3']:.2%} | "
            f"{r['tool_f1']:.2f} | {r['tools_per_case']:.1f} | "
            f"{r['judge_safety_failures']}/{r['n']} |"
        )
    md_lines.append("")
    md_lines.append("## Rule-based detail")
    md_lines.append("")
    md_lines.append("| Model | Required cov | Useless rate | Harmful/case | Hard-seq viols/case | Cost (USD) | Cost-eff |")
    md_lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        md_lines.append(
            f"| `{r['model']}` | {r['required_coverage']:.2%} | "
            f"{r['useless_call_rate']:.2%} | {r['harmful_calls']:.3f} | "
            f"{r['hard_sequence_violations']:.3f} | "
            f"${r['total_cost_usd']:.0f} | {r['cost_efficiency']:.2f} |"
        )
    md_lines.append("")
    md_lines.append("## Judge per-dimension means (all 0–5 scale)")
    md_lines.append("")
    md_lines.append("| Model | DA | Evi integ | Tool eff | Safety | Red herrings |")
    md_lines.append("|---|---|---|---|---|---|")
    for r in rows:
        md_lines.append(
            f"| `{r['model']}` | {r['judge_dx_acc']:.2f} | "
            f"{r['judge_evi_integ']:.2f} | {r['judge_tool_eff']:.2f} | "
            f"{r['judge_safety']:.2f} | {r['judge_rh']:.2f} |"
        )
    md_lines.append("")
    md_lines.append("## Notes")
    md_lines.append("")
    md_lines.append(
        f"- All {sum(r['n'] for r in rows)} traces scored by an independent `llm-judge` Claude subagent on the same 8-dimension rubric (`config/system_prompts/llm_judge.txt`).")
    md_lines.append(
        "- Rule-based safety = `critical_actions_hit - (0.3·contraindicated + 0.5·harmful + 0.4·hard_sequence_violations)`, clamped to [0, 1].")
    md_lines.append(
        "- Judge composite = weighted mean of 8 rubric dimensions, normalised to [0, 1].")
    md_lines.append(
        "- Same 50 v5 cases used across all models (`subsample_case_ids.txt`, seed=42).")
    md_lines.append(
        "- Tool calls / total cost depend on the agent's behaviour, not the dataset.")

    md = "\n".join(md_lines) + "\n"
    (base / "final_summary.md").write_text(md)
    console.print(f"\n[green]Wrote[/green] {base}/final_summary.json")
    console.print(f"[green]Wrote[/green] {base}/final_summary.md")


if __name__ == "__main__":
    app()
