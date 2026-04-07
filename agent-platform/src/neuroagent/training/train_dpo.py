"""DPO (Direct Preference Optimization) training for NeuroAgent.

Offline RL approach that works within single-GPU memory constraints:
1. Pre-generate trajectories via vLLM (decoupled from training)
2. Score with composite reward
3. Build preference pairs (best vs worst per case)
4. Train with DPO loss (same memory as SFT — no generation during training)

Usage:
    # Step 1: Generate trajectories (requires vLLM serving the SFT model)
    python -m neuroagent.training.train_dpo collect \
        --model Qwen/Qwen3.5-9B \
        --dataset data/neurobench_v4 \
        --split-file data/neurobench_v4/splits/fold0_train.txt \
        --output training_data/dpo_trajectories.json \
        --rollouts 8

    # Step 2: Build DPO pairs and train
    python -m neuroagent.training.train_dpo train \
        --model checkpoints/sft_769/checkpoint-272 \
        --trajectories training_data/dpo_trajectories.json \
        --output checkpoints/dpo_from_sft \
        --qlora
"""

from __future__ import annotations

import argparse
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def build_dpo_pairs(
    trajectories_path: str | Path,
    min_reward_gap: float = 0.05,
    dataset_path: str | Path = "data/neurobench_v4",
) -> list[dict[str, Any]]:
    """Build DPO preference pairs from scored trajectories.

    For each case, pairs the highest-reward trajectory (chosen) with the
    lowest-reward trajectory (rejected). Skips cases where the reward gap
    is below min_reward_gap.
    """
    from neuroagent_schemas import NeuroBenchCase
    from ..evaluation.runner import format_patient_info

    data = json.loads(Path(trajectories_path).read_text())
    trajectories = data["trajectories"]

    # Load case prompts
    cases_dir = Path(dataset_path) / "cases"
    case_prompts: dict[str, str] = {}
    for cf in cases_dir.glob("*.json"):
        case = NeuroBenchCase.model_validate(json.loads(cf.read_text()))
        case_prompts[case.case_id] = format_patient_info(case)

    # Group by case
    by_case: dict[str, list[dict]] = defaultdict(list)
    for t in trajectories:
        by_case[t["case_id"]].append(t)

    pairs = []
    skipped = 0
    for case_id, trajs in by_case.items():
        if len(trajs) < 2:
            skipped += 1
            continue

        trajs.sort(key=lambda t: t["reward"], reverse=True)
        best = trajs[0]
        worst = trajs[-1]

        gap = best["reward"] - worst["reward"]
        if gap < min_reward_gap:
            skipped += 1
            continue

        prompt = case_prompts.get(case_id, "")
        if not prompt:
            skipped += 1
            continue

        chosen_completion = _trace_to_messages(best["trace"])
        rejected_completion = _trace_to_messages(worst["trace"])

        if not chosen_completion or not rejected_completion:
            skipped += 1
            continue

        # DPO format: chosen/rejected as message lists
        pairs.append({
            "chosen": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": chosen_completion},
            ],
            "rejected": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": rejected_completion},
            ],
            "case_id": case_id,
            "condition": best.get("condition", ""),
            "difficulty": best.get("difficulty", ""),
            "chosen_reward": best["reward"],
            "rejected_reward": worst["reward"],
            "reward_gap": gap,
        })

    logger.info(
        "Built %d DPO pairs from %d cases (%d skipped: <2 trajs or gap < %.2f)",
        len(pairs), len(by_case), skipped, min_reward_gap,
    )
    return pairs


def _trace_to_messages(trace: dict[str, Any], compact: bool = True) -> str:
    """Convert an AgentTrace dict to a completion string for DPO.

    The completion concatenates the model's reasoning, tool call decisions,
    and final assessment. Tool responses (from MockServer, not model-generated)
    are aggressively truncated in compact mode to maximize the token budget
    for the model's own output (reasoning + diagnosis).

    Args:
        trace: AgentTrace.model_dump() dict.
        compact: If True, truncate tool responses to save tokens for
            model-generated content (reasoning, tool choices, assessment).
    """
    turns = trace.get("turns", [])
    if not turns:
        return ""

    completion_parts = []

    for turn in turns:
        role = turn.get("role", "")
        content = turn.get("content", "") or ""
        tool_calls = turn.get("tool_calls", []) or []
        tool_results = turn.get("tool_results", []) or []

        if role == "assistant":
            if content:
                completion_parts.append(content)
            for tc in tool_calls:
                name = tc.get("name", "unknown")
                args = json.dumps(tc.get("arguments", {}))
                completion_parts.append(
                    f"<tool_call>\n{{\"name\": \"{name}\", \"arguments\": {args}}}\n</tool_call>"
                )
        elif role == "tool":
            for tr in tool_results:
                tool_name = tr.get("tool_name", "")
                output = tr.get("output", "")
                if isinstance(output, dict):
                    output = json.dumps(output)
                if output:
                    # In compact mode, heavily truncate tool responses.
                    # These are MockServer outputs, not model-generated.
                    # The model's DECISIONS (which tool, what params) are
                    # what DPO needs to learn from; the full response content
                    # is less important for preference learning.
                    max_chars = 200 if compact else 2000
                    truncated = str(output)[:max_chars]
                    if len(str(output)) > max_chars:
                        truncated += "... [truncated]"
                    completion_parts.append(
                        f"<tool_response name=\"{tool_name}\">\n{truncated}\n</tool_response>"
                    )

    return "\n\n".join(completion_parts) if completion_parts else ""


def run_dpo_training(
    model_name: str,
    pairs_path: str,
    output_dir: str,
    base_model: str | None = None,
    lora_rank: int = 64,
    lora_alpha: int = 128,
    epochs: int = 3,
    batch_size: int = 1,
    learning_rate: float = 5e-7,
    beta: float = 0.1,
    max_length: int = 4096,
    bf16: bool = True,
    qlora: bool = False,
) -> None:
    """Train with DPO on preference pairs."""
    import torch
    from datasets import Dataset
    from peft import PeftModel, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import DPOConfig, DPOTrainer

    from .train_grpo import get_lora_config, get_quantization_config

    # Detect PEFT adapter checkpoint
    adapter_path = None
    model_path = Path(model_name)
    if model_path.exists() and (model_path / "adapter_config.json").exists():
        adapter_path = str(model_path)
        if base_model is None:
            adapter_cfg = json.loads((model_path / "adapter_config.json").read_text())
            base_model = adapter_cfg.get("base_model_name_or_path", "Qwen/Qwen3.5-9B")
        logger.info("Detected PEFT adapter at %s, base model: %s", adapter_path, base_model)
        model_name = base_model

    logger.info("Loading model: %s (qlora=%s)", model_name, qlora)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    load_kwargs: dict = {
        "device_map": "auto",
        "trust_remote_code": True,
    }
    if qlora:
        load_kwargs["quantization_config"] = get_quantization_config()
    else:
        load_kwargs["torch_dtype"] = torch.bfloat16 if bf16 else torch.float16

    model = AutoModelForCausalLM.from_pretrained(model_name, **load_kwargs)

    if qlora:
        model = prepare_model_for_kbit_training(model)

    if adapter_path:
        logger.info("Loading SFT adapter from %s", adapter_path)
        model = PeftModel.from_pretrained(model, adapter_path, is_trainable=True)
    else:
        lora_config = get_lora_config(rank=lora_rank, alpha=lora_alpha)
        model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load DPO pairs
    pairs = json.loads(Path(pairs_path).read_text())
    logger.info("Loaded %d DPO pairs", len(pairs))

    # Format for TRL DPOTrainer: expects 'chosen' and 'rejected' as message lists
    dataset = Dataset.from_list(pairs)

    # DPO config
    training_args = DPOConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=8,
        learning_rate=learning_rate,
        beta=beta,
        max_length=max_length,
        bf16=bf16,
        logging_steps=10,
        save_steps=50,
        save_total_limit=3,
        gradient_checkpointing=True,
        eval_strategy="no",
        # No ref model — use implicit reference (same model, frozen)
        precompute_ref_log_probs=True,
    )

    trainer = DPOTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )

    logger.info("Starting DPO training for %d epochs (beta=%.2f)", epochs, beta)
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    logger.info("DPO model saved to %s", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="NeuroAgent DPO training")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- collect subcommand ---
    collect_parser = subparsers.add_parser("collect", help="Collect trajectories via vLLM")
    collect_parser.add_argument("--model", default="Qwen/Qwen3.5-9B", help="Model served by vLLM")
    collect_parser.add_argument("--dataset", required=True, help="NeuroBench dataset path")
    collect_parser.add_argument("--split-file", default=None, help="Case IDs file (fold0_train.txt)")
    collect_parser.add_argument("--output", required=True, help="Output trajectories JSON")
    collect_parser.add_argument("--rollouts", type=int, default=8, help="Rollouts per case")
    collect_parser.add_argument("--max-cases", type=int, default=None)
    collect_parser.add_argument("--base-url", default="http://localhost:8000/v1")
    collect_parser.add_argument("--hospital", default="de_charite")

    # --- pairs subcommand ---
    pairs_parser = subparsers.add_parser("pairs", help="Build DPO pairs from trajectories")
    pairs_parser.add_argument("--trajectories", required=True, help="Scored trajectories JSON")
    pairs_parser.add_argument("--output", required=True, help="Output DPO pairs JSON")
    pairs_parser.add_argument("--min-reward-gap", type=float, default=0.05)

    # --- train subcommand ---
    train_parser = subparsers.add_parser("train", help="Train DPO from preference pairs")
    train_parser.add_argument("--model", required=True, help="Model or PEFT adapter")
    train_parser.add_argument("--base-model", default=None)
    train_parser.add_argument("--pairs", required=True, help="DPO pairs JSON")
    train_parser.add_argument("--output", required=True, help="Output checkpoint dir")
    train_parser.add_argument("--lora-rank", type=int, default=64)
    train_parser.add_argument("--lora-alpha", type=int, default=128)
    train_parser.add_argument("--epochs", type=int, default=3)
    train_parser.add_argument("--batch-size", type=int, default=1)
    train_parser.add_argument("--lr", type=float, default=5e-7)
    train_parser.add_argument("--beta", type=float, default=0.1)
    train_parser.add_argument("--max-length", type=int, default=4096)
    train_parser.add_argument("--qlora", action="store_true")
    train_parser.add_argument("--bf16", action="store_true", default=True)

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.command == "collect":
        from .data.prepare_trajectories import collect_trajectories, load_cases
        from .rewards.composite_reward import CompositeReward
        from ..agent.orchestrator import AgentConfig

        cases = load_cases(Path(args.dataset), max_cases=args.max_cases)
        if args.split_file:
            split_ids = set(Path(args.split_file).read_text().strip().splitlines())
            cases = [c for c in cases if c.case_id in split_ids]
            logger.info("Filtered to %d cases from split", len(cases))

        agent_config = AgentConfig(
            base_url=args.base_url,
            model=args.model,
            temperature=1.0,
            hospital=args.hospital,
        )

        reward_fn = CompositeReward.from_config(
            reward_config_path="agent-platform/config/reward_weights.yaml",
            tool_costs_path="agent-platform/config/tool_costs.yaml",
            rules_dir="agent-platform/config/hospital_rules",
            hospital=args.hospital,
        )

        dataset = collect_trajectories(
            cases=cases,
            agent_config=agent_config,
            reward_fn=reward_fn,
            rollouts_per_case=args.rollouts,
            rules_dir="agent-platform/config/hospital_rules",
            hospital=args.hospital,
        )
        dataset.save(args.output)

    elif args.command == "pairs":
        pairs = build_dpo_pairs(args.trajectories, min_reward_gap=args.min_reward_gap)
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(pairs, indent=2, default=str))
        logger.info("Saved %d pairs to %s", len(pairs), out)

    elif args.command == "train":
        run_dpo_training(
            model_name=args.model,
            pairs_path=args.pairs,
            output_dir=args.output,
            base_model=args.base_model,
            lora_rank=args.lora_rank,
            lora_alpha=args.lora_alpha,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.lr,
            beta=args.beta,
            max_length=args.max_length,
            bf16=args.bf16,
            qlora=args.qlora,
        )


if __name__ == "__main__":
    main()
