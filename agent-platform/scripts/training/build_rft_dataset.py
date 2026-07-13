"""Turn RFT rollouts into an SFT dataset — keep only verified-correct trajectories.

Rejection-sampling fine-tuning (RFT/STaR): the model rolled out N times per train case; we
keep only the trajectories that reached the correct diagnosis (the gold label is the
verifier), run each survivor through the SAME `validate_trajectory` gate the gold
trajectories pass (schema-valid tool args, no answer-key leakage, non-empty <think>
blocks, banned-tool checks, ...), dedupe near-identical ones, cap per case so easy cases
don't dominate, and write them in the exact trajectories.jsonl shape the SFT path consumes.

Input : the JSONL written by run_sft_eval_cases.py --rollout-jsonl (one row per rollout with
        `correct`, `messages`, `case_id`, ...).
Output: trajectories.jsonl-compatible (each line has `messages`, `case_id`, `style`).

    uv run python agent-platform/scripts/training/build_rft_dataset.py \
        --rollouts results/rft/rollouts.jsonl \
        --output training_data/rft_trajectories/trajectories.jsonl \
        --max-per-case 4
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import typer
from rich.console import Console

REPO_ROOT = Path(__file__).resolve().parents[3]
AGENT_PLATFORM = REPO_ROOT / "agent-platform"
sys.path.insert(0, str(AGENT_PLATFORM / "src"))
sys.path.insert(0, str(REPO_ROOT / "packages" / "neuroagent-schemas" / "src"))

app = typer.Typer(add_completion=False)
console = Console()


def _to_training_messages(messages: list[dict]) -> list[dict]:
    """Normalise a live rollout conversation into the gold-trajectory training shape.

    The only fix needed: the agent emits tool_call `arguments` as a JSON string (OpenAI wire
    format), while the chat template (and the gold trajectories) require a dict. Parse it back.
    Reasoning already lives in the assistant `content` as <think>…</think>.
    """
    out = []
    for m in messages:
        m = dict(m)
        if m.get("role") == "assistant" and m.get("tool_calls"):
            calls = []
            for c in m["tool_calls"]:
                c = json.loads(json.dumps(c))  # deep copy
                fn = c.get("function", {})
                args = fn.get("arguments")
                if isinstance(args, str):
                    try:
                        fn["arguments"] = json.loads(args) if args.strip() else {}
                    except json.JSONDecodeError:
                        fn["arguments"] = {}
                calls.append(c)
            m["tool_calls"] = calls
        out.append(m)
    return out


def _tools_called(messages: list[dict]) -> list[str]:
    """Tool names in call order, read from the normalised assistant turns."""
    names = []
    for m in messages:
        if m.get("role") != "assistant":
            continue
        for c in m.get("tool_calls") or []:
            name = c.get("function", {}).get("name")
            if name:
                names.append(name)
    return names


def _signature(messages: list[dict]) -> tuple:
    """A dedupe key: the sequence of (tool, sorted arg keys) plus the final answer's core."""
    sig = []
    for m in messages:
        for c in m.get("tool_calls") or []:
            fn = c.get("function", {})
            args = fn.get("arguments") or {}
            keys = tuple(sorted(args)) if isinstance(args, dict) else ()
            sig.append((fn.get("name"), keys))
    final = (messages[-1].get("content") or "")[:200].lower().split()
    return (tuple(sig), tuple(final[:20]))


@app.command()
def main(
    rollouts: str = typer.Option(..., help="Rollout JSONL from --rollout-jsonl"),
    output: str = typer.Option(..., help="Output trajectories.jsonl"),
    max_per_case: int = typer.Option(4, help="Cap distinct correct trajectories kept per case"),
    min_tool_calls: int = typer.Option(1, help="Drop trajectories that called no tools"),
    dataset: str = typer.Option(
        str(REPO_ROOT / "data" / "neurobench"),
        help="NeuroBench dataset root (cases/ needed for the validate_trajectory gate)",
    ),
) -> None:
    # Same rejection gate the gold-trajectory pipeline applies — correctness alone
    # is not admission: malformed tool args, answer-key leakage, or empty <think>
    # blocks must not enter SFT data through the RFT side door.
    from neuroagent.training.data.generate_gold_trajectories import (
        load_cases,
        validate_trajectory,
    )

    cases_by_id = {c.case_id: c for c in load_cases(Path(dataset))}

    rows = [json.loads(l) for l in Path(rollouts).read_text().splitlines() if l.strip()]
    total = len(rows)
    correct = [r for r in rows if r.get("correct")]

    by_case: dict[str, list] = defaultdict(list)
    for r in correct:
        by_case[r["case_id"]].append(r)

    kept: list[dict] = []
    per_case_counts = []
    n_invalid = 0
    invalid_reasons: Counter = Counter()
    for cid, cand in by_case.items():
        case = cases_by_id.get(cid)
        if case is None:
            raise KeyError(
                f"Rollout references case {cid!r} but no such case exists under "
                f"{dataset}/cases — wrong --dataset?"
            )
        # prefer shorter (more efficient) correct trajectories, then dedupe by signature
        cand.sort(key=lambda r: r.get("num_tool_calls", 99))
        seen, chosen = set(), []
        for r in cand:
            if r.get("num_tool_calls", 0) < min_tool_calls:
                continue
            msgs = _to_training_messages(r["messages"])
            sig = _signature(msgs)
            if sig in seen:
                continue
            trajectory = {
                "case_id": cid,
                "condition": r["condition"],
                "difficulty": r["difficulty"],
                "style": "rft",
                "messages": msgs,
                "tools_called": _tools_called(msgs),
                "num_tool_calls": r.get("num_tool_calls", 0),
            }
            # No token_budget: rollout length is what the model produced; the length
            # audit happens at SFT tokenisation time like every other trajectory.
            is_valid, issues = validate_trajectory(trajectory, case, token_budget=None)
            if not is_valid:
                n_invalid += 1
                for issue in issues:
                    invalid_reasons[issue.split(":")[0]] += 1
                continue
            seen.add(sig)
            chosen.append(trajectory)
            if len(chosen) >= max_per_case:
                break
        kept.extend(chosen)
        per_case_counts.append(len(chosen))

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(json.dumps(k, ensure_ascii=False) for k in kept) + "\n")

    # Report — the numbers that tell you whether RFT is worth training on.
    n_cases_total = len({r["case_id"] for r in rows})
    n_cases_covered = len({k["case_id"] for k in kept})
    console.print(f"\n[bold]RFT dataset built[/bold] → {output}")
    console.print(f"  rollouts: {total}  correct: {len(correct)} ({100*len(correct)/total:.0f}%)")
    console.print(f"  rejected by validate_trajectory gate: {n_invalid}")
    if invalid_reasons:
        console.print(f"  rejection reasons: {dict(invalid_reasons.most_common())}")
    console.print(f"  cases with ≥1 kept trajectory: {n_cases_covered}/{n_cases_total} "
                  f"({100*n_cases_covered/n_cases_total:.0f}%)")
    console.print(f"  kept trajectories (validated, deduped, ≤{max_per_case}/case): {len(kept)}")
    if per_case_counts:
        dist = Counter(per_case_counts)
        console.print(f"  per-case kept distribution: {dict(sorted(dist.items()))}")
    uncovered = n_cases_total - n_cases_covered
    if uncovered:
        console.print(f"  [yellow]{uncovered} cases had NO kept rollout — the model can't "
                      f"solve them yet (or its correct rollouts failed validation); RFT can't "
                      f"teach those without harder sampling or a teacher.[/yellow]")


if __name__ == "__main__":
    app()
