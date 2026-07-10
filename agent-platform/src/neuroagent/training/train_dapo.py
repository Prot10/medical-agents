"""DAPO (Decoupled Alignment via Policy Optimization) trainer for NeuroAgent.

Implements DAPO modifications over GRPO for better multi-turn ReAct training:
1. Token-level policy gradient loss (better credit assignment for long traces)
2. Clip-higher: asymmetric PPO clipping (prevents premature convergence)
3. Dynamic sampling: focuses on prompts with learning signal
4. No KL penalty

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
import math
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DAPOConfig:
    """DAPO-specific hyperparameters."""

    # Asymmetric clipping bounds
    clip_higher: float = 0.28
    clip_lower: float = 0.18

    # Dynamic sampling
    dynamic_sampling: bool = True
    min_reward_variance: float = 0.01  # skip prompts below this variance

    # Token-level loss
    token_level_loss: bool = True

    # No KL penalty in DAPO
    kl_coeff: float = 0.0

    # Oversampling factor for dynamic sampling
    oversample_factor: float = 1.5


def compute_dapo_loss(
    log_probs: "torch.Tensor",  # (B, T)
    old_log_probs: "torch.Tensor",  # (B, T)
    advantages: "torch.Tensor",  # (B,) or (B, T)
    attention_mask: "torch.Tensor",  # (B, T)
    clip_lower: float = 0.18,
    clip_higher: float = 0.28,
    token_level: bool = True,
) -> "torch.Tensor":
    """Compute DAPO policy gradient loss with asymmetric clipping.

    Key differences from standard PPO/GRPO:
    - Asymmetric clipping: ratio clipped to [1 - clip_lower, 1 + clip_higher]
    - Token-level: advantages broadcast to each token, loss computed per-token
    """
    import torch

    # Log ratio for importance sampling
    log_ratio = log_probs - old_log_probs  # (B, T)
    ratio = torch.exp(log_ratio)

    # Expand advantages to token level if needed
    if token_level and advantages.dim() == 1:
        advantages = advantages.unsqueeze(1).expand_as(ratio)  # (B, T)

    # Asymmetric clipping
    clipped_ratio = torch.clamp(
        ratio,
        min=1.0 - clip_lower,
        max=1.0 + clip_higher,
    )

    # Surrogate loss (take minimum as in PPO)
    surr1 = ratio * advantages
    surr2 = clipped_ratio * advantages
    loss = -torch.min(surr1, surr2)

    # Mask padding tokens
    loss = loss * attention_mask

    if token_level:
        # Average over valid tokens, then over batch
        token_counts = attention_mask.sum(dim=1).clamp(min=1)
        per_sample_loss = loss.sum(dim=1) / token_counts
        return per_sample_loss.mean()
    else:
        return loss.sum() / attention_mask.sum().clamp(min=1)


def filter_by_reward_variance(
    grouped_data: list[dict[str, Any]],
    min_variance: float = 0.01,
) -> list[dict[str, Any]]:
    """Filter out prompt groups where reward variance is too low.

    Dynamic sampling: skip prompts where the model has already converged
    (all completions get similar rewards), focusing compute on harder cases.
    """
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
    max_prompt_length: int = 2048,
    temperature: float = 1.0,
    bf16: bool = True,
    qlora: bool = False,
    dapo_config: DAPOConfig | None = None,
) -> None:
    """Run DAPO training.

    Builds on TRL's GRPOTrainer but overrides the loss computation with
    DAPO's token-level asymmetric clipping.
    """
    import torch
    from datasets import Dataset
    from peft import PeftModel, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import GRPOConfig, GRPOTrainer

    from .train_grpo import (
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

    # Dynamic sampling: filter low-variance groups
    if dapo_config.dynamic_sampling and isinstance(raw_data, list):
        raw_data = filter_by_reward_variance(
            raw_data, min_variance=dapo_config.min_reward_variance,
        )

    # Format for GRPOTrainer
    formatted = []
    for ex in raw_data:
        prompt_messages = [{"role": "user", "content": ex.get("prompt", "")}]
        formatted.append({"prompt": prompt_messages})

    dataset = Dataset.from_list(formatted)

    # Build reward function — prefer online scoring
    reward_func = None
    dataset_path_env = os.environ.get("NEUROAGENT_DATASET", "data/neurobench")
    dataset_dir = Path(dataset_path_env)

    if (dataset_dir / "cases").exists():
        logger.info("Using ONLINE reward (case ground truth scoring)")
        from .rewards.online_reward import OnlineRewardFunction, build_prompt_to_case_mapping
        from ..tools.cost_tracker import CostTracker

        case_mapping = build_prompt_to_case_mapping(dataset_dir)
        cost_tracker = CostTracker()
        reward_func = OnlineRewardFunction(cases=case_mapping, cost_tracker=cost_tracker)
    else:
        logger.info("Using OFFLINE pre-computed rewards")
        reward_data = {}
        for ex in raw_data:
            if "completions" in ex and "rewards" in ex:
                for comp, rew in zip(ex["completions"], ex["rewards"]):
                    if isinstance(comp, str):
                        reward_data[comp[:200]] = rew

        def reward_func(prompts, completions, **kwargs) -> list[float]:
            rewards = []
            for comp in completions:
                if isinstance(comp, str):
                    rewards.append(reward_data.get(comp[:200], 0.0))
                else:
                    rewards.append(0.0)
            return rewards

    # DAPO config via TRL's native loss_type="dapo" support
    # - loss_type="dapo": token-level policy gradient with per-token advantage
    # - epsilon: lower clip bound (1 - epsilon)
    # - epsilon_high: upper clip bound (1 + epsilon_high) for asymmetric clipping
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
        "Starting DAPO training: %d epochs, clip=[%.2f, %.2f], token_level=%s",
        epochs, dapo_config.clip_lower, dapo_config.clip_higher,
        dapo_config.token_level_loss,
    )
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
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

    # DAPO-specific
    parser.add_argument("--clip-higher", type=float, default=0.28)
    parser.add_argument("--clip-lower", type=float, default=0.18)
    parser.add_argument("--no-dynamic-sampling", action="store_true")
    parser.add_argument("--no-token-level", action="store_true")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    dapo_config = DAPOConfig(
        clip_higher=args.clip_higher,
        clip_lower=args.clip_lower,
        dynamic_sampling=not args.no_dynamic_sampling,
        token_level_loss=not args.no_token_level,
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
    )


if __name__ == "__main__":
    main()
