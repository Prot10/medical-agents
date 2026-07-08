"""Baseline benchmark: 6 base models × 50-case v5 subsample × 3 reps (ReAct).

Per case: runs the agent, saves the full trace, computes all rule-based
CaseMetrics, and emits a per-(case, rep) judge bundle ready for the
`llm-judge` Claude subagent. Resumable via per-model checkpoint.

When a model finishes, the script writes `<model>/model_done.flag` so an
out-of-band dispatcher can fire parallel judges WHILE this script continues
with the next model.

Output layout (on EOS):

    /eos/.../results/baseline_eval_<TS>/
        config.json
        subsample_case_ids.txt
        benchmark.log
        <model_key>/
            run_config.json
            checkpoint.json
            traces/<case_id>_rep<n>.json     # full agent trace + metrics
            metrics/<case_id>_rep<n>.json    # CaseMetrics only
            judge_bundles/<case_id>_rep<n>.json
            judge_scores/                     # (filled by judge dispatcher)
            summary.json
            model_done.flag
        summary.json                          # cross-model roll-up (final)

Run from the repo root:

    uv run python agent-platform/scripts/run_baseline_eval.py \
        --output-base /eos/project-d/diagbox/dvc/NeuroAgent/results \
        --reps 3 --num-cases 50

Resume the same run by passing --run-dir <existing path>.
"""

from __future__ import annotations

import json
import logging
import os
import random
import signal
import subprocess
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
AGENT_PLATFORM = REPO_ROOT / "agent-platform"
DATASET_DIR = REPO_ROOT / "data" / "neurobench_v5"
SERVE_SCRIPT = AGENT_PLATFORM / "scripts" / "serve_model.sh"

app = typer.Typer(add_completion=False)
console = Console()
logger = logging.getLogger("baseline_eval")


# ---------------------------------------------------------------------------
# Models — keyed by the serve_model.sh entry name, ordered smallest first so
# the cheap iterations validate the pipeline before the expensive ones run.
# ---------------------------------------------------------------------------

MODELS: list[dict[str, Any]] = [
    {"serve_name": "nemotron-3-nano-4b",  "model_id": "nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16", "max_tokens": 8192},
    {"serve_name": "qwen3.5-4b",          "model_id": "Qwen/Qwen3.5-4B",                       "max_tokens": 8192},
    {"serve_name": "gemma-4-e2b",         "model_id": "google/gemma-4-E2B-it",                 "max_tokens": 8192},
    {"serve_name": "gemma-4-e4b",         "model_id": "google/gemma-4-E4B-it",                 "max_tokens": 8192},
    {"serve_name": "nemotron-nano-9b-v2", "model_id": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",     "max_tokens": 8192},
    {"serve_name": "qwen3.5-9b",          "model_id": "Qwen/Qwen3.5-9B",                       "max_tokens": 8192},
]


# ---------------------------------------------------------------------------
# vLLM server management (mirrors run_full_benchmark.py)
# ---------------------------------------------------------------------------

def kill_vllm() -> None:
    subprocess.run(["pkill", "-f", "vllm_serve.py"], capture_output=True)
    time.sleep(5)


def start_vllm(serve_name: str, port: int, timeout: int, log_path: Path) -> subprocess.Popen:
    env = os.environ.copy()
    env["CUDA_MODULE_LOADING"] = "LAZY"
    # serve_model.sh defaults HF_HOME to the EOS-staged cache; preserve that.
    env.setdefault("HF_HOME", "/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface")

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_fh = log_path.open("ab")

    proc = subprocess.Popen(
        ["bash", str(SERVE_SCRIPT), serve_name, str(port)],
        env=env,
        stdout=log_fh,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
    )
    console.print(f"  Starting vLLM for [cyan]{serve_name}[/cyan] (pid {proc.pid}, log: {log_path})")

    import urllib.error
    import urllib.request

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = urllib.request.urlopen(f"http://localhost:{port}/v1/models", timeout=5)
            if resp.status == 200:
                console.print(f"  [green]vLLM ready[/green] on port {port}")
                return proc
        except (urllib.error.URLError, ConnectionError, OSError):
            pass
        if proc.poll() is not None:
            log_fh.close()
            tail = log_path.read_bytes()[-3000:].decode(errors="replace")
            raise RuntimeError(
                f"vLLM exited with code {proc.returncode} before becoming ready.\n"
                f"Tail of {log_path}:\n{tail}"
            )
        time.sleep(5)

    raise TimeoutError(f"vLLM did not become ready within {timeout}s; tail at {log_path}")


def stop_vllm(proc: subprocess.Popen | None) -> None:
    if proc is None:
        return
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    time.sleep(3)


# ---------------------------------------------------------------------------
# Case selection — seeded random sample, stable across resumes
# ---------------------------------------------------------------------------

def sample_case_ids(num: int, seed: int) -> list[str]:
    cases_dir = DATASET_DIR / "cases"
    all_ids = sorted(p.stem for p in cases_dir.glob("*.json"))
    if not all_ids:
        raise FileNotFoundError(f"No cases under {cases_dir}")
    if num >= len(all_ids):
        return all_ids
    rng = random.Random(seed)
    return sorted(rng.sample(all_ids, num))


def load_case_dict(case_id: str) -> dict:
    return json.loads((DATASET_DIR / "cases" / f"{case_id}.json").read_text())


# ---------------------------------------------------------------------------
# Per-case execution
# ---------------------------------------------------------------------------

def run_one_case(
    case_data: dict,
    model_id: str,
    max_tokens: int,
    hospital: str,
    base_url: str,
    rep: int,
    use_rules: bool = False,
) -> tuple[dict, dict]:
    """Run the agent on a single case; return (trace_dict, metrics_dict).

    use_rules=False (default) → no hospital protocols injected into the agent
    system prompt and protocol_compliance is not computed. This isolates base
    model capability for the baseline; a separate ablation can re-enable
    rules to measure protocol-effect.
    """
    # Imports kept local so the script's --help works without the heavy deps.
    from neuroagent_schemas import NeuroBenchCase
    from neuroagent.agent.orchestrator import AgentOrchestrator, load_agent_config
    from neuroagent.evaluation.metrics import MetricsCalculator
    from neuroagent.evaluation.runner import format_patient_info
    from neuroagent.tools.mock_server import MockServer
    from neuroagent.tools.tool_registry import ToolRegistry

    case = NeuroBenchCase.model_validate(case_data)

    cfg = load_agent_config(
        base_url=base_url,
        model=model_id,
        max_tokens=max_tokens,
        hospital=hospital,
    )

    mock = MockServer(case)
    registry = ToolRegistry.create_default_registry(mock_server=mock)

    rules = None
    if use_rules:
        from neuroagent.rules.rules_engine import RulesEngine
        rules = RulesEngine(str(AGENT_PLATFORM / "config" / "hospital_rules"), hospital=hospital)

    agent = AgentOrchestrator(config=cfg, tool_registry=registry, rules_engine=rules)
    trace = agent.run(patient_info=format_patient_info(case), case_id=case.case_id)

    metrics = MetricsCalculator().compute_all(
        trace=trace,
        ground_truth=case.ground_truth,
        rules_engine=rules,
        condition=case.condition.value,
    )

    trace_dict = {
        "case_id": case.case_id,
        "condition": case.condition.value,
        "difficulty": case.difficulty.value,
        "model_id": model_id,
        "hospital": hospital,
        "rep": rep,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "final_response": trace.final_response,
        "total_tool_calls": trace.total_tool_calls,
        "tools_called": list(trace.tools_called),
        "total_tokens": trace.total_tokens,
        "elapsed_time_seconds": round(trace.elapsed_time_seconds, 2),
        "total_cost_usd": trace.total_cost_usd,
        "num_turns": len(trace.turns),
        "turns": [
            {
                "turn_number": t.turn_number,
                "role": t.role,
                "content": t.content,
                "tool_calls": t.tool_calls,
                "tool_results": t.tool_results,
                "token_usage": t.token_usage,
            }
            for t in trace.turns
        ],
    }
    metrics_dict = asdict(metrics)
    return trace_dict, metrics_dict


# ---------------------------------------------------------------------------
# Judge bundle writer — one file per (case, rep); contract matches the
# llm-judge agent in .claude/agents/llm-judge.md (multi-run array).
# ---------------------------------------------------------------------------

def write_judge_bundle(
    bundle_path: Path,
    case_data: dict,
    trace_dict: dict,
    model_key: str,
    rep: int,
) -> None:
    bundle = {
        "case_id": case_data["case_id"],
        "condition": case_data["condition"],
        "difficulty": case_data["difficulty"],
        "case_presentation": {
            "patient": case_data["patient"],
            "encounter_type": case_data.get("encounter_type"),
        },
        "ground_truth": case_data["ground_truth"],
        "runs": [
            {
                "run_name": f"{model_key}-rep{rep}",
                "model_id": trace_dict["model_id"],
                "mode": "react",
                "final_response": trace_dict["final_response"],
                "tools_called": trace_dict["tools_called"],
                "total_tool_calls": trace_dict["total_tool_calls"],
                "elapsed_time_seconds": trace_dict["elapsed_time_seconds"],
                "trace": {
                    "num_turns": trace_dict["num_turns"],
                    "turns": trace_dict["turns"],
                },
            }
        ],
    }
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path.write_text(json.dumps(bundle, indent=2, default=str))


# ---------------------------------------------------------------------------
# Per-model summary
# ---------------------------------------------------------------------------

def summarize_model_run(model_dir: Path) -> dict:
    metric_files = sorted((model_dir / "metrics").glob("*.json"))
    if not metric_files:
        return {"n": 0}
    metrics = [json.loads(mf.read_text()) for mf in metric_files]
    n = len(metrics)

    def mean(key: str) -> float:
        vals = [m.get(key, 0) or 0 for m in metrics]
        return round(sum(vals) / n, 4)

    return {
        "n_traces": n,
        "diagnostic_accuracy_top1": mean("diagnostic_accuracy_top1"),
        "diagnostic_accuracy_top3": mean("diagnostic_accuracy_top3"),
        "action_precision": mean("action_precision"),
        "action_recall": mean("action_recall"),
        "tool_f1": mean("tool_f1"),
        "required_coverage": mean("required_coverage"),
        "useless_call_rate": mean("useless_call_rate"),
        "harmful_calls": mean("harmful_calls"),
        "redundancy_rate": mean("redundancy_rate"),
        "premature_closure_count": mean("premature_closure_count"),
        "sequence_violations": mean("sequence_violations"),
        "hard_sequence_violations": mean("hard_sequence_violations"),
        "critical_actions_hit": mean("critical_actions_hit"),
        "contraindicated_actions_taken": mean("contraindicated_actions_taken"),
        "efficiency_score": mean("efficiency_score"),
        "safety_score": mean("safety_score"),
        "total_cost_usd": mean("total_cost_usd"),
        "cost_efficiency": mean("cost_efficiency"),
        "tool_call_count": mean("tool_call_count"),
        "specialist_calls": mean("specialist_calls"),
    }


# ---------------------------------------------------------------------------
# Checkpointing
# ---------------------------------------------------------------------------

def ckpt_key(case_id: str, rep: int) -> str:
    return f"{case_id}|rep{rep}"


def load_checkpoint(path: Path) -> tuple[set[str], dict[str, str]]:
    if path.exists():
        d = json.loads(path.read_text())
        return set(d.get("completed", [])), d.get("errors", {})
    return set(), {}


def save_checkpoint(path: Path, completed: set[str], errors: dict[str, str]) -> None:
    path.write_text(json.dumps({
        "completed": sorted(completed),
        "errors": errors,
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }, indent=2))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

@app.command()
def main(
    output_base: str = typer.Option(
        "/eos/project-d/diagbox/dvc/NeuroAgent/results",
        help="Base directory; a timestamped subdir is created (unless --run-dir).",
    ),
    run_dir: str = typer.Option(
        "", help="Resume an existing run by passing its directory (skips subsample reroll)."
    ),
    num_cases: int = typer.Option(50, help="Subsample size."),
    seed: int = typer.Option(42, help="Random seed for the subsample."),
    reps: int = typer.Option(3, help="Repetitions per (model, case)."),
    hospital: str = typer.Option("us_mayo", help="Hospital rules to apply."),
    models_filter: str = typer.Option(
        "", "--models", help="Comma-separated serve_names; empty = all six."
    ),
    port: int = typer.Option(8000, help="vLLM server port."),
    server_timeout: int = typer.Option(600, help="Seconds to wait for vLLM startup."),
    max_cases_per_model: int = typer.Option(
        0, help="Cap traces per model (debug). 0 = no cap."
    ),
    use_rules: bool = typer.Option(
        False, "--use-rules/--no-rules",
        help="Inject hospital protocol rules into the agent system prompt and "
             "compute protocol_compliance. Default OFF — baseline measures pure "
             "model capability; turn ON for a rules ablation.",
    ),
    dry_run: bool = typer.Option(False, help="Plan only; do not start vLLM or run cases."),
) -> None:
    """Run the baseline benchmark."""
    if run_dir:
        out = Path(run_dir)
        if not out.exists():
            raise typer.BadParameter(f"--run-dir does not exist: {out}")
    else:
        ts = time.strftime("%Y%m%d_%H%M%S")
        out = Path(output_base) / f"baseline_eval_{ts}"
        out.mkdir(parents=True, exist_ok=False)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(message)s",
        handlers=[
            RichHandler(console=console, rich_tracebacks=True, show_time=False),
            logging.FileHandler(out / "benchmark.log"),
        ],
    )

    # Subsample — write once on first launch, reuse on resume.
    subsample_file = out / "subsample_case_ids.txt"
    if subsample_file.exists():
        case_ids = subsample_file.read_text().strip().splitlines()
    else:
        case_ids = sample_case_ids(num_cases, seed)
        subsample_file.write_text("\n".join(case_ids) + "\n")

    # Apply model filter.
    if models_filter:
        wanted = {m.strip() for m in models_filter.split(",") if m.strip()}
        models = [m for m in MODELS if m["serve_name"] in wanted]
        if not models:
            raise typer.BadParameter(f"No models match --models={models_filter}")
    else:
        models = list(MODELS)

    # Run-wide config — written once.
    cfg = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "num_cases": len(case_ids),
        "case_ids": case_ids,
        "reps": reps,
        "seed": seed,
        "hospital": hospital,
        "use_hospital_rules": use_rules,
        "mode": "react",
        "models": [m["serve_name"] for m in models],
        "model_ids": {m["serve_name"]: m["model_id"] for m in models},
        "sampling": {
            "temperature": 1.0,
            "top_p": 0.95,
            "presence_penalty": 1.5,
        },
        "dataset": str(DATASET_DIR),
        "vllm_port": port,
    }
    (out / "config.json").write_text(json.dumps(cfg, indent=2))

    total = len(models) * len(case_ids) * reps
    if max_cases_per_model:
        total = len(models) * min(len(case_ids), max_cases_per_model) * reps

    console.print(f"\n[bold]Baseline benchmark[/bold]  →  {out}")
    console.print(f"  Models : {[m['serve_name'] for m in models]}")
    console.print(f"  Cases  : {len(case_ids)} (sampled with seed={seed})")
    console.print(f"  Reps   : {reps}  Hospital: {hospital}")
    console.print(f"  Total executions: {total}\n")

    if dry_run:
        console.print("[yellow]--dry-run: stopping before vLLM/agent execution.[/yellow]")
        return

    # Preload case JSON once.
    cases = {cid: load_case_dict(cid) for cid in case_ids}

    summary_rows: list[dict] = []
    vllm_proc: subprocess.Popen | None = None

    try:
        for mdef in models:
            mkey = mdef["serve_name"]
            mdir = out / mkey
            (mdir / "traces").mkdir(parents=True, exist_ok=True)
            (mdir / "metrics").mkdir(parents=True, exist_ok=True)
            (mdir / "judge_bundles").mkdir(parents=True, exist_ok=True)
            (mdir / "judge_scores").mkdir(parents=True, exist_ok=True)
            (mdir / "logs").mkdir(parents=True, exist_ok=True)

            done_flag = mdir / "model_done.flag"
            if done_flag.exists():
                console.print(f"[dim]Skipping {mkey} — model_done.flag present.[/dim]")
                # Still record summary from disk for the final roll-up.
                summary_rows.append({"model": mkey, **summarize_model_run(mdir)})
                continue

            # Write per-model config
            (mdir / "run_config.json").write_text(json.dumps({
                "model_key": mkey,
                "model_id": mdef["model_id"],
                "max_tokens": mdef["max_tokens"],
                "hospital": hospital,
                "reps": reps,
                "temperature": 1.0,
                "top_p": 0.95,
                "presence_penalty": 1.5,
                "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }, indent=2))

            console.print(f"\n{'=' * 70}\n[bold]Model: {mkey}[/bold]\n{'=' * 70}")

            # Start vLLM for this model.
            stop_vllm(vllm_proc)
            kill_vllm()
            try:
                vllm_proc = start_vllm(
                    mkey,
                    port=port,
                    timeout=server_timeout,
                    log_path=mdir / "logs" / "vllm.log",
                )
            except Exception as e:
                console.print(f"[red]vLLM failed for {mkey}: {e}[/red]")
                (mdir / "vllm_failed.flag").write_text(str(e))
                continue

            base_url = f"http://localhost:{port}/v1"
            ckpt_path = mdir / "checkpoint.json"
            completed, errors = load_checkpoint(ckpt_path)

            case_iter = case_ids[:max_cases_per_model] if max_cases_per_model else case_ids
            for rep in range(1, reps + 1):
                for cid in case_iter:
                    key = ckpt_key(cid, rep)
                    if key in completed:
                        continue
                    t0 = time.time()
                    try:
                        trace_dict, metrics_dict = run_one_case(
                            case_data=cases[cid],
                            model_id=mdef["model_id"],
                            max_tokens=mdef["max_tokens"],
                            hospital=hospital,
                            base_url=base_url,
                            rep=rep,
                            use_rules=use_rules,
                        )
                    except KeyboardInterrupt:
                        save_checkpoint(ckpt_path, completed, errors)
                        raise
                    except Exception as e:
                        errors[key] = f"{type(e).__name__}: {e}"
                        save_checkpoint(ckpt_path, completed, errors)
                        console.print(f"  [red]FAIL[/red] rep{rep} {cid} — {errors[key][:160]}")
                        logger.debug("traceback", exc_info=True)
                        continue

                    # Persist outputs.
                    trace_path = mdir / "traces" / f"{cid}_rep{rep}.json"
                    metric_path = mdir / "metrics" / f"{cid}_rep{rep}.json"
                    bundle_path = mdir / "judge_bundles" / f"{cid}_rep{rep}.json"

                    # Write trace + metrics together to keep one source of truth.
                    full = {**trace_dict, "metrics": metrics_dict}
                    trace_path.write_text(json.dumps(full, indent=2, default=str))
                    metric_path.write_text(json.dumps(metrics_dict, indent=2, default=str))
                    write_judge_bundle(bundle_path, cases[cid], trace_dict, mkey, rep)

                    completed.add(key)
                    save_checkpoint(ckpt_path, completed, errors)

                    elapsed = time.time() - t0
                    console.print(
                        f"  [green]OK[/green] rep{rep} {cid} "
                        f"({elapsed:.1f}s, {trace_dict['total_tool_calls']}t, "
                        f"top1={metrics_dict['diagnostic_accuracy_top1']}, "
                        f"safety={metrics_dict['safety_score']:.2f})"
                    )

            # Model finished — write summary, flag, leave traces ready for judging.
            summary = summarize_model_run(mdir)
            summary["model"] = mkey
            summary["model_id"] = mdef["model_id"]
            summary["errors_count"] = len(errors)
            (mdir / "summary.json").write_text(json.dumps(summary, indent=2))
            done_flag.write_text(time.strftime("%Y-%m-%dT%H:%M:%S") + "\n")
            console.print(f"[bold green]{mkey} done — wrote model_done.flag[/bold green]")
            summary_rows.append({"model": mkey, **summary})

    finally:
        stop_vllm(vllm_proc)
        kill_vllm()

    # Cross-model rollup.
    rollup = {
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "rows": summary_rows,
    }
    (out / "summary.json").write_text(json.dumps(rollup, indent=2))

    # Print table.
    table = Table(title="Baseline summary")
    table.add_column("Model", style="cyan")
    table.add_column("N", justify="right")
    table.add_column("Top-1", justify="right")
    table.add_column("Top-3", justify="right")
    table.add_column("Safety", justify="right")
    table.add_column("Tool F1", justify="right")
    table.add_column("Reqd cov", justify="right")
    table.add_column("Tools/case", justify="right")
    for row in summary_rows:
        table.add_row(
            row["model"],
            str(row.get("n_traces", 0)),
            f"{row.get('diagnostic_accuracy_top1', 0):.2f}",
            f"{row.get('diagnostic_accuracy_top3', 0):.2f}",
            f"{row.get('safety_score', 0):.2f}",
            f"{row.get('tool_f1', 0):.2f}",
            f"{row.get('required_coverage', 0):.2f}",
            f"{row.get('tool_call_count', 0):.1f}",
        )
    console.print(table)
    console.print(f"\n[green]Results:[/green] {out}")


if __name__ == "__main__":
    app()
