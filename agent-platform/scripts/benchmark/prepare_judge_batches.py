"""Batch a finished model's judge bundles for parallel llm-judge dispatch.

Reads <model_dir>/judge_bundles/*.json (one per case-rep, written by
run_baseline_eval.py) and groups them into chunks of N files. For each
chunk, writes the corresponding output-path target where the llm-judge
agent should write its scores JSON. Emits a manifest listing (chunk_id,
bundle_files[], output_path) so the dispatcher (Claude) can spawn one
parallel llm-judge agent per chunk.

Usage:
    uv run python agent-platform/scripts/benchmark/prepare_judge_batches.py \
        --run-dir /eos/.../results/baseline_eval_<TS> \
        --model qwen3.5-4b \
        --batch-size 10
"""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def main(
    run_dir: str = typer.Option(..., help="Baseline run directory."),
    model: str = typer.Option(..., help="Model key (serve_name)."),
    batch_size: int = typer.Option(10, help="Bundles per batch."),
) -> None:
    base = Path(run_dir)
    mdir = base / model
    if not mdir.exists():
        raise typer.BadParameter(f"{mdir} does not exist")

    bundles = sorted((mdir / "judge_bundles").glob("*.json"))
    if not bundles:
        raise typer.BadParameter(f"No bundles in {mdir/'judge_bundles'}")

    scores_dir = mdir / "judge_scores"
    scores_dir.mkdir(parents=True, exist_ok=True)
    batches_dir = mdir / "judge_batches"
    batches_dir.mkdir(parents=True, exist_ok=True)

    # Skip bundles whose score file already exists, so the dispatcher is
    # idempotent across reruns.
    todo: list[Path] = []
    for b in bundles:
        score_path = scores_dir / b.name
        if score_path.exists():
            continue
        todo.append(b)

    if not todo:
        console.print(f"[yellow]All {len(bundles)} bundles already scored for {model}.[/yellow]")
        (batches_dir / "manifest.json").write_text(json.dumps(
            {"model": model, "batch_size": batch_size, "batches": [], "all_done": True},
            indent=2,
        ))
        return

    batches = [todo[i : i + batch_size] for i in range(0, len(todo), batch_size)]

    manifest = {
        "model": model,
        "batch_size": batch_size,
        "n_pending": len(todo),
        "n_total": len(bundles),
        "batches": [
            {
                "batch_id": f"{model}-batch{i:02d}",
                "bundle_files": [str(p) for p in chunk],
                "output_path": str(batches_dir / f"scores_batch{i:02d}.json"),
                "individual_score_paths": [
                    str(scores_dir / p.name) for p in chunk
                ],
            }
            for i, chunk in enumerate(batches)
        ],
    }
    manifest_path = batches_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    console.print(
        f"[green]Wrote {len(batches)} batches[/green] for [cyan]{model}[/cyan] "
        f"({len(todo)}/{len(bundles)} pending).  Manifest: {manifest_path}"
    )


if __name__ == "__main__":
    app()
