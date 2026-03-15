"""Run all models on all NeuroBench cases across hospitals and repetitions.

This script sequentially:
1. Starts vLLM for each model
2. Runs all cases × hospitals × repetitions (or resumes from checkpoint)
3. Saves full traces, metrics, and metadata per case
4. Stops vLLM and moves to the next model

For Qwen models, runs both:
  - "react" mode: agent uses tools via ReAct loop
  - "no_tools" mode: agent receives all tool outputs upfront (ablation)

Default: 4 models × 2 modes × 3 hospitals × 3 reps × 100 cases = 7,200 runs

Usage:
    # Full benchmark (all models, hospitals, 3 reps)
    uv run python agent-platform/scripts/run_full_benchmark.py

    # Quick test
    uv run python agent-platform/scripts/run_full_benchmark.py --max-cases 2 --reps 1

    # Specific model only
    uv run python agent-platform/scripts/run_full_benchmark.py --models qwen3.5-9b

    # Specific modes/hospitals
    uv run python agent-platform/scripts/run_full_benchmark.py --modes react --hospitals de_charite

    # Resume after failure — just re-run the same command
    uv run python agent-platform/scripts/run_full_benchmark.py
"""

from __future__ import annotations

import json
import logging
import os
import signal
import subprocess
import time
from itertools import groupby
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

app = typer.Typer()
console = Console()
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
AGENT_PLATFORM = REPO_ROOT / "agent-platform"
DATASET_DIR = REPO_ROOT / "data" / "neurobench_v1"
RESULTS_DIR = REPO_ROOT / "results" / "benchmark"
SERVE_SCRIPT = AGENT_PLATFORM / "scripts" / "serve_model.sh"

# ---------------------------------------------------------------------------
# Model definitions
# ---------------------------------------------------------------------------

MODELS = {
    "qwen3.5-9b": {
        "serve_name": "qwen3.5-9b",
        "model_id": "Qwen/Qwen3.5-9B",
        "max_tokens": 8192,
    },
    "qwen3.5-27b-awq": {
        "serve_name": "qwen3.5-27b-awq",
        "model_id": "QuantTrio/Qwen3.5-27B-AWQ",
        "max_tokens": 8192,
    },
    "medgemma-4b": {
        "serve_name": "medgemma-4b",
        "model_id": "google/medgemma-1.5-4b-it",
        "max_tokens": 8192,
    },
    "medgemma-27b": {
        "serve_name": "medgemma-27b",
        "model_id": "ig1/medgemma-27b-text-it-FP8-Dynamic",
        "max_tokens": 2048,  # 8K context limit, prompt uses ~2-3K tokens
    },
}

# 3 most diverse hospitals for cross-protocol comparison
DEFAULT_HOSPITALS = ["de_charite", "jp_todai", "br_hcfmusp"]

DEFAULT_MODES = ["react", "no_tools"]


# ---------------------------------------------------------------------------
# Server management
# ---------------------------------------------------------------------------

def kill_vllm() -> None:
    subprocess.run(["pkill", "-f", "vllm_serve.py"], capture_output=True)
    time.sleep(5)


def start_vllm(serve_name: str, port: int = 8000, timeout: int = 300) -> subprocess.Popen:
    env = os.environ.copy()
    env["CUDA_MODULE_LOADING"] = "LAZY"
    env["HF_HOME"] = os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface"))

    proc = subprocess.Popen(
        ["bash", str(SERVE_SCRIPT), serve_name, str(port)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
    )

    console.print(f"  Starting vLLM for [cyan]{serve_name}[/cyan] (pid {proc.pid})...")

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
            stdout = proc.stdout.read().decode() if proc.stdout else ""
            raise RuntimeError(
                f"vLLM exited with code {proc.returncode}.\n{stdout[-2000:]}"
            )
        time.sleep(5)

    raise TimeoutError(f"vLLM did not become ready within {timeout}s")


def stop_vllm(proc: subprocess.Popen) -> None:
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    time.sleep(3)


# ---------------------------------------------------------------------------
# Checkpoint management
# ---------------------------------------------------------------------------

def _checkpoint_key(case_id: str, hospital: str, rep: int) -> str:
    """Unique key for a single execution: case × hospital × repetition."""
    return f"{case_id}|{hospital}|rep{rep}"


def load_checkpoint(run_dir: Path) -> tuple[set[str], dict[str, str]]:
    ckpt = run_dir / "checkpoint.json"
    if ckpt.exists():
        data = json.loads(ckpt.read_text())
        return set(data.get("completed", [])), data.get("errors", {})
    return set(), {}


def save_checkpoint(run_dir: Path, completed: set[str], errors: dict[str, str]) -> None:
    ckpt = run_dir / "checkpoint.json"
    ckpt.write_text(json.dumps({
        "completed": sorted(completed),
        "errors": errors,
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }, indent=2))


# ---------------------------------------------------------------------------
# Case runners — each creates a fresh MockServer + ToolRegistry per case
# but reuses the AgentOrchestrator's LLM client for the run.
# ---------------------------------------------------------------------------

def make_agent(model_id: str, max_tokens: int, hospital: str, case_data: dict):
    """Create a fresh agent for one case (fresh mock/tools, shared LLM config)."""
    from neuroagent_schemas import NeuroBenchCase
    from neuroagent.agent.orchestrator import AgentConfig, AgentOrchestrator
    from neuroagent.evaluation.runner import EvaluationRunner
    from neuroagent.rules.rules_engine import RulesEngine
    from neuroagent.tools.mock_server import MockServer
    from neuroagent.tools.tool_registry import ToolRegistry

    case = NeuroBenchCase.model_validate(case_data)
    config = AgentConfig(base_url="http://localhost:8000/v1", model=model_id, max_tokens=max_tokens)

    # Fresh mock server and tool registry per case — no state leakage
    mock = MockServer(case)
    registry = ToolRegistry.create_default_registry(mock_server=mock)
    rules = RulesEngine(str(AGENT_PLATFORM / "config" / "hospital_rules"), hospital=hospital)

    agent = AgentOrchestrator(config=config, tool_registry=registry, rules_engine=rules)
    patient_info = EvaluationRunner(config=config, dataset_path="")._format_initial_info(case)

    return agent, case, patient_info


def run_case_react(case_data: dict, model_id: str, max_tokens: int, hospital: str) -> dict:
    agent, case, patient_info = make_agent(model_id, max_tokens, hospital, case_data)
    trace = agent.run(patient_info=patient_info, case_id=case.case_id)
    return _trace_to_dict(trace, case, model_id, "react", hospital)


def run_case_no_tools(case_data: dict, model_id: str, max_tokens: int, hospital: str,
                      **_kwargs) -> dict:
    """Run with clinical info only — no tools offered, no tool outputs.

    This is the baseline: the model must diagnose from the initial clinical
    presentation alone, just like a doctor who orders no investigations.
    """
    agent, case, patient_info = make_agent(model_id, max_tokens, hospital, case_data)

    # Call LLM directly with just patient info — no tools in the request
    trace = agent.run_all_info_upfront(
        patient_info=patient_info,
        tool_outputs_text="",  # empty — no tool results provided
        case_id=case.case_id,
    )
    return _trace_to_dict(trace, case, model_id, "no_tools", hospital)


def _format_all_tool_outputs(case) -> str:
    parts = []
    o = case.initial_tool_outputs
    if o.eeg:
        parts.append(f"## EEG Results\n{o.eeg.model_dump_json(indent=2)}")
    if o.mri:
        parts.append(f"## Brain MRI Results\n{o.mri.model_dump_json(indent=2)}")
    if o.ecg:
        parts.append(f"## ECG Results\n{o.ecg.model_dump_json(indent=2)}")
    if o.labs:
        parts.append(f"## Laboratory Results\n{o.labs.model_dump_json(indent=2)}")
    if o.csf:
        parts.append(f"## CSF Analysis\n{o.csf.model_dump_json(indent=2)}")
    if o.literature_search:
        for ls in o.literature_search:
            parts.append(f"## Literature Search: {ls.query}\n{ls.model_dump_json(indent=2)}")
    if o.drug_interactions:
        for di in o.drug_interactions:
            parts.append(f"## Drug Interaction Check: {di.proposed}\n{di.model_dump_json(indent=2)}")
    return "\n\n".join(parts) if parts else "(No tool outputs available)"


def _trace_to_dict(trace, case, model_id: str, mode: str, hospital: str) -> dict:
    return {
        "case_id": case.case_id,
        "condition": case.condition.value,
        "difficulty": case.difficulty.value,
        "model_id": model_id,
        "mode": mode,
        "hospital": hospital,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "final_response": trace.final_response,
        "total_tool_calls": trace.total_tool_calls,
        "tools_called": trace.tools_called,
        "total_tokens": trace.total_tokens,
        "elapsed_time_seconds": round(trace.elapsed_time_seconds, 2),
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
        "ground_truth": {
            "primary_diagnosis": case.ground_truth.primary_diagnosis,
            "icd_code": case.ground_truth.icd_code,
            "differential": case.ground_truth.differential,
            "optimal_actions": case.ground_truth.optimal_actions,
            "critical_actions": case.ground_truth.critical_actions,
            "contraindicated_actions": case.ground_truth.contraindicated_actions,
            "key_reasoning_points": case.ground_truth.key_reasoning_points,
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

@app.command()
def benchmark(
    models: str = typer.Option(
        "",
        help="Comma-separated model keys (empty = all). Options: qwen3.5-9b, qwen3.5-27b-awq, medgemma-4b, medgemma-27b",
    ),
    modes: str = typer.Option(
        "",
        help="Comma-separated modes (empty = both). Options: react, no_tools",
    ),
    hospitals: str = typer.Option(
        "",
        help="Comma-separated hospital IDs (empty = de_charite,jp_todai,br_hcfmusp)",
    ),
    reps: int = typer.Option(3, help="Number of repetitions per case"),
    max_cases: int = typer.Option(0, help="Limit cases per run (0 = all 100)"),
    port: int = typer.Option(8000, help="vLLM server port"),
    server_timeout: int = typer.Option(300, help="Seconds to wait for vLLM startup"),
    output_dir: str = typer.Option(str(RESULTS_DIR), help="Output directory"),
) -> None:
    """Run the full NeuroBench benchmark across all models, hospitals, and repetitions.

    Temperature is 1.0 (Qwen3.5 recommended) so each repetition gives
    a different reasoning trace, enabling variance analysis.
    """
    logging.basicConfig(
        level=logging.INFO,
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Parse filters
    model_keys = [m.strip() for m in models.split(",") if m.strip()] or list(MODELS.keys())
    mode_list = [m.strip() for m in modes.split(",") if m.strip()] or DEFAULT_MODES
    hospital_list = [h.strip() for h in hospitals.split(",") if h.strip()] or DEFAULT_HOSPITALS

    # Validate
    for mk in model_keys:
        if mk not in MODELS:
            console.print(f"[red]Unknown model: {mk}. Available: {list(MODELS.keys())}[/red]")
            raise typer.Exit(1)
    for h in hospital_list:
        from neuroagent.rules.rules_engine import AVAILABLE_HOSPITALS
        if h not in AVAILABLE_HOSPITALS:
            console.print(f"[red]Unknown hospital: {h}. Available: {list(AVAILABLE_HOSPITALS.keys())}[/red]")
            raise typer.Exit(1)

    # Load cases
    cases_dir = DATASET_DIR / "cases"
    case_files = sorted(cases_dir.glob("*.json"))
    if max_cases > 0:
        case_files = case_files[:max_cases]
    all_cases = [json.loads(cf.read_text()) for cf in case_files]

    # Build run plan in explicit order:
    #   1. Qwen 9B (react + no_tools)
    #   2. MedGemma 4B (no_tools only)
    #   3. Qwen 27B (react + no_tools)
    #   4. MedGemma 27B (no_tools only)
    TOOL_CAPABLE = {"qwen3.5-9b", "qwen3.5-27b-awq"}
    MODEL_ORDER = ["qwen3.5-9b", "medgemma-4b", "qwen3.5-27b-awq", "medgemma-27b"]
    run_plan: list[tuple[str, str]] = []
    for mk in MODEL_ORDER:
        if mk not in model_keys:
            continue
        for mode in mode_list:
            if mode == "react" and mk not in TOOL_CAPABLE:
                continue
            run_plan.append((mk, mode))

    total_executions = len(run_plan) * len(hospital_list) * reps * len(all_cases)
    console.print(f"\n[bold]NeuroBench Full Benchmark[/bold]")
    console.print(f"Models: {model_keys}")
    console.print(f"Modes: {mode_list}")
    console.print(f"Hospitals: {hospital_list}")
    console.print(f"Repetitions: {reps}")
    console.print(f"Cases: {len(all_cases)}")
    console.print(f"Total executions: {total_executions}")
    console.print(f"Output: {out}\n")

    # Save benchmark config
    (out / "benchmark_config.json").write_text(json.dumps({
        "models": model_keys,
        "modes": mode_list,
        "hospitals": hospital_list,
        "reps": reps,
        "num_cases": len(all_cases),
        "case_ids": [c["case_id"] for c in all_cases],
        "total_executions": total_executions,
        "temperature": 1.0,
        "top_p": 0.95,
        "presence_penalty": 1.5,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }, indent=2))

    summary: list[dict] = []
    current_serve: str | None = None
    vllm_proc: subprocess.Popen | None = None

    try:
        for serve_name, group in groupby(run_plan, key=lambda x: MODELS[x[0]]["serve_name"]):
            group_items = list(group)

            # Start/switch server
            if current_serve != serve_name:
                if vllm_proc is not None:
                    console.print(f"\n  Stopping vLLM ({current_serve})...")
                    stop_vllm(vllm_proc)
                    kill_vllm()

                console.print(f"\n{'='*70}")
                console.print(f"[bold]Loading model: {serve_name}[/bold]")
                console.print(f"{'='*70}")
                try:
                    vllm_proc = start_vllm(serve_name, port=port, timeout=server_timeout)
                    current_serve = serve_name
                except Exception as e:
                    console.print(f"[red]Failed to start vLLM for {serve_name}: {e}[/red]")
                    for mk, mode in group_items:
                        for h in hospital_list:
                            run_id = f"{mk}-{mode}-{h}"
                            summary.append({
                                "run_id": run_id, "status": "server_failed",
                                "completed": 0, "total": len(all_cases) * reps,
                            })
                    continue

            # Execute each (model, mode) × hospitals × reps
            for model_key, mode in group_items:
                mdef = MODELS[model_key]
                run_fn = run_case_react if mode == "react" else run_case_no_tools

                for hospital in hospital_list:
                    run_id = f"{model_key}-{mode}-{hospital}"
                    run_dir = out / run_id
                    run_dir.mkdir(parents=True, exist_ok=True)
                    traces_dir = run_dir / "traces"
                    traces_dir.mkdir(exist_ok=True)

                    # Save run config
                    (run_dir / "run_config.json").write_text(json.dumps({
                        "run_id": run_id,
                        "model_key": model_key,
                        "model_id": mdef["model_id"],
                        "serve_name": mdef["serve_name"],
                        "mode": mode,
                        "hospital": hospital,
                        "max_tokens": mdef["max_tokens"],
                        "reps": reps,
                        "temperature": 1.0,
                    }, indent=2))

                    completed, errors = load_checkpoint(run_dir)
                    total_for_run = len(all_cases) * reps

                    console.print(f"\n[bold]Run: {run_id}[/bold]")
                    console.print(
                        f"  {mdef['model_id']} | {mode} | {hospital} | {reps} reps"
                    )
                    console.print(
                        f"  {len(completed)}/{total_for_run} done, "
                        f"{total_for_run - len(completed)} pending"
                    )

                    for rep in range(1, reps + 1):
                        for case_data in all_cases:
                            case_id = case_data["case_id"]
                            key = _checkpoint_key(case_id, hospital, rep)

                            if key in completed:
                                continue

                            try:
                                console.print(
                                    f"  rep{rep} {case_id} ...",
                                    end=" ",
                                )
                                t0 = time.time()

                                result = run_fn(
                                    case_data=case_data,
                                    model_id=mdef["model_id"],
                                    max_tokens=mdef["max_tokens"],
                                    hospital=hospital,
                                )
                                result["repetition"] = rep

                                elapsed = time.time() - t0

                                trace_file = traces_dir / f"{case_id}_rep{rep}.json"
                                trace_file.write_text(
                                    json.dumps(result, indent=2, default=str)
                                )

                                completed.add(key)
                                save_checkpoint(run_dir, completed, errors)

                                console.print(
                                    f"[green]OK[/green] "
                                    f"({elapsed:.1f}s, {result['total_tool_calls']}t, "
                                    f"{result['total_tokens']}tok)"
                                )

                            except KeyboardInterrupt:
                                console.print(
                                    "\n[yellow]Interrupted. Progress saved.[/yellow]"
                                )
                                save_checkpoint(run_dir, completed, errors)
                                raise

                            except Exception as e:
                                msg = f"{type(e).__name__}: {e}"
                                errors[key] = msg
                                save_checkpoint(run_dir, completed, errors)
                                console.print(f"[red]FAIL[/red] — {msg[:120]}")
                                logger.debug("Traceback for %s:", key, exc_info=True)

                    summary.append(_build_summary(
                        run_id, mdef["model_id"], mode, hospital,
                        run_dir, completed, errors, total_for_run,
                    ))

    finally:
        if vllm_proc is not None:
            console.print(f"\n  Stopping vLLM ({current_serve})...")
            stop_vllm(vllm_proc)
        kill_vllm()

    # Print summary
    console.print(f"\n{'='*70}")
    console.print("[bold]Benchmark Complete[/bold]")
    console.print(f"{'='*70}\n")

    table = Table(title="Benchmark Summary")
    table.add_column("Run", style="cyan", max_width=40)
    table.add_column("Status")
    table.add_column("Done", justify="right")
    table.add_column("Err", justify="right")
    table.add_column("Avg Time", justify="right")
    table.add_column("Avg Tools", justify="right")

    for s in summary:
        st = "green" if s["status"] == "done" else "yellow" if s["status"] == "partial" else "red"
        table.add_row(
            s["run_id"],
            f"[{st}]{s['status']}[/{st}]",
            f"{s['completed']}/{s['total']}",
            str(s.get("errors_count", 0)),
            f"{s.get('avg_time', 0):.1f}s",
            f"{s.get('avg_tools', 0):.1f}",
        )

    console.print(table)

    summary_file = out / "benchmark_summary.json"
    summary_file.write_text(json.dumps(summary, indent=2))
    console.print(f"\nSummary saved to {summary_file}")


def _build_summary(
    run_id: str, model_id: str, mode: str, hospital: str,
    run_dir: Path, completed: set[str], errors: dict[str, str], total: int,
) -> dict:
    traces_dir = run_dir / "traces"
    times, tools, tokens = [], [], []
    for tf in traces_dir.glob("*.json"):
        try:
            d = json.loads(tf.read_text())
            times.append(d.get("elapsed_time_seconds", 0))
            tools.append(d.get("total_tool_calls", 0))
            tokens.append(d.get("total_tokens", 0))
        except Exception:
            pass
    return {
        "run_id": run_id,
        "model_id": model_id,
        "mode": mode,
        "hospital": hospital,
        "status": "done" if len(completed) >= total else "partial",
        "completed": len(completed),
        "total": total,
        "errors_count": len(errors),
        "errors": errors if errors else None,
        "avg_time": sum(times) / len(times) if times else 0,
        "avg_tools": sum(tools) / len(tools) if tools else 0,
        "avg_tokens": sum(tokens) / len(tokens) if tokens else 0,
        "total_time": sum(times),
    }


if __name__ == "__main__":
    app()
