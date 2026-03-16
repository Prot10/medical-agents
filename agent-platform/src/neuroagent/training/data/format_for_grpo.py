"""Convert scored trajectories into GRPO training format.

Takes the trajectories JSON from prepare_trajectories.py and converts it
into the format expected by TRL GRPOTrainer or veRL: a parquet dataset
with prompt/completion/reward columns.

Supports two modes:
1. Full trajectory: prompt = system + patient info, completion = full ReAct trace
2. Per-step decomposition: each tool-call decision becomes its own training example

Usage:
    python -m neuroagent.training.data.format_for_grpo \
        --input training_data/trajectories.json \
        --output training_data/grpo_dataset \
        --mode full
"""

from __future__ import annotations

import argparse
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def load_trajectories(path: str | Path) -> dict[str, Any]:
    """Load scored trajectories from JSON."""
    with open(path) as f:
        return json.load(f)


def _build_prompt_from_trace(trace: dict[str, Any]) -> str:
    """Reconstruct the system + user prompt from a trace.

    The actual system prompt isn't stored in the trace, so we reconstruct
    the user message (patient info) from the first user turn.
    """
    # The trace stores turns; the prompt is everything before the first assistant turn
    # For GRPO, we provide the prompt separately — the model generates the completion
    turns = trace.get("turns", [])

    # Find all content before the first assistant response
    # In practice, the prompt is the patient_info passed to agent.run()
    # We store it as case metadata during trajectory collection
    return ""  # Will be populated from case data during formatting


def _format_completion_from_trace(trace: dict[str, Any]) -> str:
    """Format the full agent trajectory as a completion string.

    Reconstructs the model's output: reasoning + tool calls + final assessment.
    """
    parts = []
    turns = trace.get("turns", [])

    for turn in turns:
        if turn["role"] == "assistant":
            if turn.get("content"):
                parts.append(turn["content"])
            if turn.get("tool_calls"):
                for tc in turn["tool_calls"]:
                    func = tc.get("function", tc)
                    name = func.get("name", "unknown")
                    args = func.get("arguments", {})
                    if isinstance(args, str):
                        args_str = args
                    else:
                        args_str = json.dumps(args, indent=None)
                    parts.append(f'<tool_call>\n{{"name": "{name}", "arguments": {args_str}}}\n</tool_call>')
        elif turn["role"] == "tool":
            results = turn.get("tool_results", [])
            for tr in results:
                tr_str = json.dumps(tr, default=str)
                if len(tr_str) > 3000:
                    tr_str = tr_str[:3000] + "..."
                parts.append(f"<tool_response>\n{tr_str}\n</tool_response>")

    final = trace.get("final_response", "")
    if final:
        parts.append(final)

    return "\n\n".join(parts)


def _decompose_per_step(
    trace: dict[str, Any],
    patient_info: str,
    system_prompt: str,
) -> list[dict[str, str]]:
    """Decompose trajectory into per-step decision points.

    Each step: context so far → next assistant turn (tool choice + reasoning).
    """
    steps = []
    context_parts = []
    turns = trace.get("turns", [])

    for turn in turns:
        if turn["role"] == "assistant":
            # The prompt is everything up to this point
            prompt = system_prompt + "\n\n" + patient_info
            if context_parts:
                prompt += "\n\n" + "\n\n".join(context_parts)

            # The completion is this assistant turn
            completion_parts = []
            if turn.get("content"):
                completion_parts.append(turn["content"])
            if turn.get("tool_calls"):
                for tc in turn["tool_calls"]:
                    func = tc.get("function", tc)
                    name = func.get("name", "unknown")
                    args = func.get("arguments", {})
                    if isinstance(args, str):
                        args_str = args
                    else:
                        args_str = json.dumps(args, indent=None)
                    completion_parts.append(
                        f'<tool_call>\n{{"name": "{name}", "arguments": {args_str}}}\n</tool_call>'
                    )

            if completion_parts:
                steps.append({
                    "prompt": prompt,
                    "completion": "\n\n".join(completion_parts),
                })

            # Add this turn to context for next step
            if turn.get("content"):
                context_parts.append(turn["content"])
            if turn.get("tool_calls"):
                for tc in turn["tool_calls"]:
                    func = tc.get("function", tc)
                    name = func.get("name", "unknown")
                    args = func.get("arguments", {})
                    args_str = json.dumps(args, indent=None) if isinstance(args, dict) else args
                    context_parts.append(
                        f'<tool_call>\n{{"name": "{name}", "arguments": {args_str}}}\n</tool_call>'
                    )

        elif turn["role"] == "tool":
            results = turn.get("tool_results", [])
            for tr in results:
                tr_str = json.dumps(tr, default=str)
                if len(tr_str) > 3000:
                    tr_str = tr_str[:3000] + "..."
                context_parts.append(f"<tool_response>\n{tr_str}\n</tool_response>")

    return steps


def format_full_trajectory(
    data: dict[str, Any],
    system_prompt: str = "",
    min_reward_variance: float = 0.01,
) -> list[dict[str, Any]]:
    """Format trajectories for GRPO with full trajectory completions.

    Groups trajectories by case_id (GRPO needs multiple completions per prompt).
    Filters out cases where all trajectories have identical rewards (no signal).

    Returns list of dicts with: prompt, completions, rewards
    """
    # Group by case_id
    by_case: dict[str, list[dict]] = defaultdict(list)
    for traj in data["trajectories"]:
        by_case[traj["case_id"]].append(traj)

    dataset = []
    skipped = 0

    for case_id, trajs in by_case.items():
        rewards = [t["reward"] for t in trajs]

        # Filter: GRPO needs reward variance for learning
        reward_range = max(rewards) - min(rewards)
        if reward_range < min_reward_variance:
            skipped += 1
            continue

        # Build prompt from first trajectory's trace metadata
        # In practice, all trajectories for same case share the same prompt
        completions = [_format_completion_from_trace(t["trace"]) for t in trajs]

        dataset.append({
            "case_id": case_id,
            "condition": trajs[0]["condition"],
            "difficulty": trajs[0]["difficulty"],
            "prompt": system_prompt,  # System prompt — patient info is in trace
            "completions": completions,
            "rewards": rewards,
        })

    logger.info(
        "Formatted %d cases (%d skipped due to low reward variance)",
        len(dataset), skipped,
    )
    return dataset


def format_per_step(
    data: dict[str, Any],
    system_prompt: str = "",
) -> list[dict[str, Any]]:
    """Format trajectories with per-step decomposition.

    Each tool-call decision point becomes its own training example.
    Reward is propagated from the full trajectory to each step.
    """
    dataset = []

    for traj in data["trajectories"]:
        steps = _decompose_per_step(
            trace=traj["trace"],
            patient_info="",  # Already in trace context
            system_prompt=system_prompt,
        )

        trajectory_reward = traj["reward"]
        for step in steps:
            dataset.append({
                "case_id": traj["case_id"],
                "prompt": step["prompt"],
                "completion": step["completion"],
                "reward": trajectory_reward,
            })

    logger.info("Formatted %d per-step examples from %d trajectories",
                len(dataset), len(data["trajectories"]))
    return dataset


def save_dataset(dataset: list[dict[str, Any]], output_dir: str | Path) -> None:
    """Save dataset as JSON (parquet conversion requires pandas/pyarrow)."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save as JSON lines for flexibility
    jsonl_path = output_dir / "train.jsonl"
    with open(jsonl_path, "w") as f:
        for item in dataset:
            f.write(json.dumps(item, default=str) + "\n")
    logger.info("Saved %d examples to %s", len(dataset), jsonl_path)

    # Also save as single JSON for inspection
    json_path = output_dir / "train.json"
    json_path.write_text(json.dumps(dataset, indent=2, default=str))

    # Try to save as parquet if pyarrow is available
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq

        # For parquet, flatten completions/rewards lists into separate rows
        flat = []
        for item in dataset:
            if "completions" in item:
                for comp, rew in zip(item["completions"], item["rewards"]):
                    flat.append({
                        "case_id": item["case_id"],
                        "prompt": item["prompt"],
                        "completion": comp,
                        "reward": rew,
                    })
            else:
                flat.append(item)

        table = pa.Table.from_pylist(flat)
        pq.write_table(table, output_dir / "train.parquet")
        logger.info("Also saved as parquet (%d rows)", len(flat))
    except ImportError:
        logger.info("pyarrow not installed — skipping parquet output")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert trajectories to GRPO format")
    parser.add_argument("--input", required=True, help="Input trajectories JSON")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument(
        "--mode", choices=["full", "per_step"], default="full",
        help="full = complete trajectory, per_step = decomposed decisions",
    )
    parser.add_argument(
        "--min-reward-variance", type=float, default=0.01,
        help="Skip cases with reward variance below this threshold",
    )
    parser.add_argument("--system-prompt", default="", help="System prompt to prepend")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    data = load_trajectories(args.input)
    logger.info("Loaded %d trajectories", len(data["trajectories"]))

    if args.mode == "full":
        dataset = format_full_trajectory(
            data,
            system_prompt=args.system_prompt,
            min_reward_variance=args.min_reward_variance,
        )
    else:
        dataset = format_per_step(data, system_prompt=args.system_prompt)

    save_dataset(dataset, args.output)
    logger.info("Done.")


if __name__ == "__main__":
    main()
