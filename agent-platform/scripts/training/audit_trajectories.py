"""Audit the assembled gold-trajectory dataset before training.

Checks the things that silently ruin an SFT run:
  * sequences longer than max_seq (they get truncated, usually cutting the final answer)
  * assistant-token counts (is there actually any supervised signal per example?)
  * shape diversity: styles, tool-call counts, revision share, hospital mix
  * coverage: conditions and difficulties represented
  * leakage: any test-split case that made it into the training file

Usage:
    HF_HOME=/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface \
        uv run python agent-platform/scripts/training/audit_trajectories.py \
            --data training_data/gold_trajectories_v6/trajectories.jsonl \
            --model Qwen/Qwen3.5-9B \
            --splits-dir data/neurobench/splits
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path

from transformers import AutoTokenizer

from neuroagent.training.chat_template import apply_training_chat_template


def _percentile(values: list[int], q: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(q * (len(ordered) - 1)))]


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit gold trajectories")
    parser.add_argument("--data", required=True)
    parser.add_argument("--model", default="Qwen/Qwen3.5-9B")
    parser.add_argument("--splits-dir", default="data/neurobench/splits")
    parser.add_argument("--max-seq", type=int, default=None, help="Defaults to the probe result")
    parser.add_argument("--probe", default="results/sft_probe/max_seq_probe.json")
    args = parser.parse_args()

    max_seq = args.max_seq
    if max_seq is None and Path(args.probe).exists():
        max_seq = json.loads(Path(args.probe).read_text())["shared_max_seq_length"]
    if not max_seq:
        raise SystemExit("Pass --max-seq or run the probe first.")

    trajectories = [json.loads(line) for line in Path(args.data).read_text().splitlines() if line.strip()]
    if not trajectories:
        raise SystemExit(f"No trajectories in {args.data}")

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    apply_training_chat_template(tokenizer)

    total_tokens: list[int] = []
    assistant_tokens: list[int] = []
    over_budget: list[tuple[str, int]] = []
    no_signal: list[str] = []

    for traj in trajectories:
        enc = tokenizer.apply_chat_template(
            traj["messages"],
            tokenize=True,
            return_dict=True,
            return_assistant_tokens_mask=True,
        )
        n_tokens = len(enc["input_ids"])
        n_assistant = sum(enc["assistant_masks"])
        total_tokens.append(n_tokens)
        assistant_tokens.append(n_assistant)

        stem = f"{traj['case_id']}_{traj.get('style', '?')}"
        if n_tokens > max_seq:
            over_budget.append((stem, n_tokens))
        if n_assistant == 0:
            no_signal.append(stem)

    test_file = Path(args.splits_dir) / "test_cases.txt"
    test_cases = {c for c in test_file.read_text().split() if c} if test_file.exists() else set()
    leaked = sorted({t["case_id"] for t in trajectories if t["case_id"] in test_cases})

    styles = Counter(t.get("style", "?") for t in trajectories)
    hospitals = Counter(t.get("hospital") or "none" for t in trajectories)
    difficulties = Counter(t.get("difficulty", "?") for t in trajectories)
    conditions = Counter(t.get("condition", "?") for t in trajectories)
    tool_counts = Counter(t.get("num_tool_calls", 0) for t in trajectories)
    tools_used = Counter(tool for t in trajectories for tool in t.get("tools_called", []))

    n_cases = len({t["case_id"] for t in trajectories})

    print("=" * 68)
    print(f"  Gold trajectory audit — {len(trajectories)} trajectories over {n_cases} cases")
    print(f"  model={args.model}  max_seq={max_seq}")
    print("=" * 68)

    print("\nSequence length (full, chat-templated):")
    print(f"  mean={statistics.mean(total_tokens):.0f}  p50={_percentile(total_tokens, .5)}  "
          f"p90={_percentile(total_tokens, .9)}  p99={_percentile(total_tokens, .99)}  max={max(total_tokens)}")
    print("Supervised (assistant) tokens:")
    print(f"  mean={statistics.mean(assistant_tokens):.0f}  p50={_percentile(assistant_tokens, .5)}  "
          f"p90={_percentile(assistant_tokens, .9)}  max={max(assistant_tokens)}")

    print(f"\nStyles:       {dict(styles)}")
    print(f"Difficulties: {dict(difficulties)}")
    print(f"Hospital mix: {dict(sorted(hospitals.items()))}")
    print(f"Tool calls per trajectory: {dict(sorted(tool_counts.items()))}")
    print(f"Conditions covered: {len(conditions)}")
    print(f"Tools exercised:    {len(tools_used)} -> {dict(tools_used.most_common())}")

    print("\n--- Problems ---")
    ok = True
    if leaked:
        ok = False
        print(f"  FAIL: {len(leaked)} test-split cases present in training data: {leaked[:5]}")
    if over_budget:
        ok = False
        pct = 100 * len(over_budget) / len(trajectories)
        print(f"  FAIL: {len(over_budget)} ({pct:.1f}%) exceed max_seq={max_seq} and will be truncated:")
        for stem, n in sorted(over_budget, key=lambda x: -x[1])[:5]:
            print(f"        {stem}: {n} tokens")
    if no_signal:
        ok = False
        print(f"  FAIL: {len(no_signal)} have zero supervised tokens: {no_signal[:5]}")
    if ok:
        print("  none — dataset is training-ready")

    print()


if __name__ == "__main__":
    main()
