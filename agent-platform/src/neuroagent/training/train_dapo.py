"""DAPO trainer for NeuroAgent.

DAPO modifications over GRPO, all delivered through TRL's native support
(``GRPOConfig(loss_type="dapo", epsilon=…, epsilon_high=…)``):
1. Token-level policy gradient loss (better credit assignment for long traces)
2. Clip-higher: asymmetric PPO clipping (prevents premature convergence)
3. Dynamic sampling: focuses on prompts with learning signal (offline filter below)
4. No KL penalty (GRPOConfig's ``beta`` defaults to 0.0)

Reference: arXiv:2503.14476

Usage:
    python -m neuroagent.training.train_dapo \
        --model checkpoints/sft_warmup \
        --data training_data/grpo_dataset/train.jsonl \
        --output checkpoints/dapo_final \
        --qlora
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Reward values format_for_grpo's gold mode assigns by trajectory-style keyword.
# They carry no clinical signal; variance filtering on them is meaningless.
_PLACEHOLDER_REWARD_VALUES = {0.5, 0.6, 0.8}


@dataclass
class DAPOConfig:
    """DAPO-specific hyperparameters (only knobs the TRL path actually uses)."""

    # Asymmetric clipping bounds → GRPOConfig epsilon / epsilon_high
    clip_higher: float = 0.28
    clip_lower: float = 0.18

    # Dynamic sampling (offline pre-filter over pre-computed reward groups)
    dynamic_sampling: bool = True
    min_reward_variance: float = 0.01  # skip prompts below this variance


def filter_by_reward_variance(
    grouped_data: list[dict[str, Any]],
    min_variance: float = 0.01,
) -> list[dict[str, Any]]:
    """Filter out prompt groups where reward variance is too low.

    Dynamic sampling: skip prompts where the model has already converged
    (all completions get similar rewards), focusing compute on harder cases.

    Refuses to run on style-keyword PLACEHOLDER rewards (format_for_grpo gold
    mode): their variance reflects which trajectory styles a case happened to
    get, not any learning signal, so "dynamic sampling" over them silently
    drops arbitrary cases from training.
    """
    marked_placeholder = any(
        group.get("reward_source") == "style_placeholder" for group in grouped_data
    )
    all_rewards = [r for group in grouped_data for r in group.get("rewards", [])]
    looks_placeholder = bool(all_rewards) and set(all_rewards) <= _PLACEHOLDER_REWARD_VALUES
    if marked_placeholder or looks_placeholder:
        raise ValueError(
            "filter_by_reward_variance called on style-keyword placeholder rewards "
            f"({'reward_source=style_placeholder' if marked_placeholder else 'all rewards in ' + str(sorted(_PLACEHOLDER_REWARD_VALUES))}). "
            "These are schema fillers, not scores — variance filtering over them "
            "drops arbitrary cases. Rescore the trajectories with CompositeReward "
            "(prepare_trajectories.py) or disable dynamic sampling."
        )

    filtered = []
    skipped = 0
    for group in grouped_data:
        rewards = group.get("rewards", [])
        if len(rewards) < 2:
            filtered.append(group)
            continue
        mean = sum(rewards) / len(rewards)
        var = sum((r - mean) ** 2 for r in rewards) / len(rewards)
        if var >= min_variance:
            filtered.append(group)
        else:
            skipped += 1

    if skipped > 0:
        logger.info(
            "Dynamic sampling: kept %d/%d prompt groups (skipped %d low-variance)",
            len(filtered), len(filtered) + skipped, skipped,
        )
    return filtered


def run_dapo(
    model_name: str,
    data_path: str,
    output_dir: str,
    base_model: str | None = None,
    lora_rank: int = 64,
    lora_alpha: int = 128,
    epochs: int = 10,
    batch_size: int = 1,
    learning_rate: float = 5e-6,
    num_generations: int = 4,
    max_completion_length: int = 4096,
    temperature: float = 1.0,
    bf16: bool = True,
    qlora: bool = False,
    dapo_config: DAPOConfig | None = None,
    seed: int = 42,
    reward_config: str = "config/training/reward_weights.yaml",
    tool_costs_config: str = "config/tools/costs.yaml",
    rules_dir: str = "config/hospital_rules",
    hospital: str = "us_mayo",
    allow_placeholder_rewards: bool = False,
) -> None:
    """Run DAPO training via TRL's GRPOTrainer with ``loss_type="dapo"``.

    Note: TRL 0.29's GRPOConfig has no `max_prompt_length` (the trainer does not
    truncate prompts), so this function does not accept one.
    """
    import torch
    from datasets import Dataset
    from peft import PeftModel, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import GRPOConfig, GRPOTrainer

    from .train_grpo import (
        _build_offline_reward_fn,
        _build_online_reward_fn,
        _require_case_ids,
        _save_rl_run_summary,
        get_lora_config,
        get_quantization_config,
        load_grpo_data,
    )

    if dapo_config is None:
        dapo_config = DAPOConfig()

    # Detect PEFT adapter checkpoint
    adapter_path = None
    model_path = Path(model_name)
    if model_path.exists() and (model_path / "adapter_config.json").exists():
        adapter_path = str(model_path)
        if base_model is None:
            import json as _json
            adapter_cfg = _json.loads((model_path / "adapter_config.json").read_text())
            base_model = adapter_cfg.get("base_model_name_or_path", "Qwen/Qwen3.5-9B")
        logger.info("Detected PEFT adapter at %s, base model: %s", adapter_path, base_model)
        model_name = base_model

    logger.info("Loading model: %s (qlora=%s, dapo=True)", model_name, qlora)
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

    # Load data
    raw_data = load_grpo_data(data_path)
    _require_case_ids(raw_data)

    # Dynamic sampling: filter low-variance groups. Raises on style-keyword
    # placeholder rewards — pass --no-dynamic-sampling if the data carries them.
    if dapo_config.dynamic_sampling and isinstance(raw_data, list):
        raw_data = filter_by_reward_variance(
            raw_data, min_variance=dapo_config.min_reward_variance,
        )

    # Format for GRPOTrainer. `case_id` is kept as an extra dataset column —
    # GRPOConfig.remove_unused_columns defaults to False, so TRL forwards it to
    # the reward function as a kwarg for explicit, collision-free case lookup.
    formatted = []
    for ex in raw_data:
        prompt_messages = [{"role": "user", "content": ex.get("prompt", "")}]
        formatted.append({"prompt": prompt_messages, "case_id": ex["case_id"]})

    dataset = Dataset.from_list(formatted)

    # Build reward function — same shared builders as GRPO (CompositeReward online,
    # explicit-keyed offline behind --allow-placeholder-rewards).
    dataset_path_env = os.environ.get("NEUROAGENT_DATASET", "data/neurobench")
    dataset_dir = Path(dataset_path_env)

    if (dataset_dir / "cases").exists():
        logger.info("Using ONLINE reward (CompositeReward, weights from %s)", reward_config)
        reward_func = _build_online_reward_fn(
            raw_data, dataset_dir, reward_config, tool_costs_config, rules_dir, hospital
        )
    else:
        reward_func = _build_offline_reward_fn(raw_data, allow_placeholder_rewards)
        logger.info("Using OFFLINE pre-computed rewards (dataset not found at %s)", dataset_dir)

    # DAPO config via TRL's native loss_type="dapo" support
    # - loss_type="dapo": token-level policy gradient with per-token advantage
    # - epsilon: lower clip bound (1 - epsilon)
    # - epsilon_high: upper clip bound (1 + epsilon_high) for asymmetric clipping
    # - beta stays at its 0.0 default: DAPO uses no KL penalty
    # - generation_batch_size must be >= num_generations
    gen_batch = max(batch_size, num_generations)
    training_args = GRPOConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        num_generations=num_generations,
        generation_batch_size=gen_batch,
        max_completion_length=max_completion_length,
        seed=seed,
        bf16=bf16,
        logging_steps=10,
        save_steps=50,
        save_total_limit=3,
        gradient_checkpointing=True,
        generation_kwargs={"temperature": temperature},
        # DAPO-specific
        loss_type="dapo",
        epsilon=dapo_config.clip_lower,        # lower clip: ratio >= 1 - 0.18
        epsilon_high=dapo_config.clip_higher,  # upper clip: ratio <= 1 + 0.28
    )

    # Create trainer
    trainer = GRPOTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        reward_funcs=reward_func,
    )

    logger.info(
        "Starting DAPO training: %d epochs, clip=[%.2f, %.2f], seed=%d",
        epochs, dapo_config.clip_lower, dapo_config.clip_higher, seed,
    )
    result = trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    _save_rl_run_summary(
        output_dir, trainer, result, training_args, model_name,
        n_train=len(dataset), algorithm="dapo", data_path=data_path, seed=seed,
        extra_hyperparameters={
            "loss_type": "dapo",
            "epsilon_clip_lower": dapo_config.clip_lower,
            "epsilon_high_clip_higher": dapo_config.clip_higher,
            "dynamic_sampling": dapo_config.dynamic_sampling,
            "min_reward_variance": dapo_config.min_reward_variance,
            "num_generations": num_generations,
            "max_completion_length": max_completion_length,
            "generation_temperature": temperature,
            "lora_rank": lora_rank,
            "lora_alpha": lora_alpha,
            "qlora": qlora,
            "adapter_init": adapter_path,
        },
    )
    logger.info("DAPO model saved to %s", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="NeuroAgent DAPO training")
    parser.add_argument("--model", required=True, help="Model name or PEFT adapter checkpoint path")
    parser.add_argument("--base-model", default=None, help="Base model name (auto-detected from adapter if not set)")
    parser.add_argument("--data", required=True, help="GRPO-formatted training data")
    parser.add_argument("--output", required=True, help="Output directory")

    # LoRA
    parser.add_argument("--lora-rank", type=int, default=64)
    parser.add_argument("--lora-alpha", type=int, default=128)

    # Training
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--lr", type=float, default=5e-6)
    parser.add_argument("--num-generations", type=int, default=4)
    parser.add_argument("--max-completion-length", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--qlora", action="store_true")
    parser.add_argument("--bf16", action="store_true", default=True)
    parser.add_argument("--seed", type=int, default=42)

    # Reward (for online scoring)
    parser.add_argument("--reward-config", default="config/training/reward_weights.yaml")
    parser.add_argument("--tool-costs", default="config/tools/costs.yaml")
    parser.add_argument("--rules-dir", default="config/hospital_rules")
    parser.add_argument("--hospital", default="us_mayo")
    parser.add_argument(
        "--allow-placeholder-rewards", action="store_true",
        help="Permit offline pre-computed rewards when the cases dir is absent. "
             "Those rewards may be style-keyword placeholders with no clinical "
             "signal — debugging only, never for reportable runs.",
    )

    # DAPO-specific
    parser.add_argument("--clip-higher", type=float, default=0.28)
    parser.add_argument("--clip-lower", type=float, default=0.18)
    parser.add_argument("--no-dynamic-sampling", action="store_true")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    dapo_config = DAPOConfig(
        clip_higher=args.clip_higher,
        clip_lower=args.clip_lower,
        dynamic_sampling=not args.no_dynamic_sampling,
    )

    run_dapo(
        model_name=args.model,
        data_path=args.data,
        output_dir=args.output,
        base_model=args.base_model,
        lora_rank=args.lora_rank,
        lora_alpha=args.lora_alpha,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        num_generations=args.num_generations,
        max_completion_length=args.max_completion_length,
        temperature=args.temperature,
        bf16=args.bf16,
        qlora=args.qlora,
        dapo_config=dapo_config,
        seed=args.seed,
        reward_config=args.reward_config,
        tool_costs_config=args.tool_costs,
        rules_dir=args.rules_dir,
        hospital=args.hospital,
        allow_placeholder_rewards=args.allow_placeholder_rewards,
    )


if __name__ == "__main__":
    main()
