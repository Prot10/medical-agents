"""GRPO training script for NeuroAgent tool-calling fine-tuning.

Two-stage training:
  Stage 1 (SFT warmup): Short supervised fine-tuning on top trajectories
  Stage 2 (GRPO RL): Reinforcement learning with composite reward

Supports both TRL (Hugging Face) and veRL (Volcano Engine) backends.
Default: TRL GRPOTrainer with LoRA (simpler, single-node friendly).

Usage:
    # Stage 1: SFT warmup
    python -m neuroagent.training.train_grpo \
        --stage sft \
        --model Qwen/Qwen3.5-9B \
        --data training_data/grpo_dataset/train.jsonl \
        --output checkpoints/sft_warmup

    # Stage 2: GRPO
    python -m neuroagent.training.train_grpo \
        --stage grpo \
        --model checkpoints/sft_warmup \
        --data training_data/grpo_dataset/train.jsonl \
        --output checkpoints/grpo_final

    # veRL multi-GPU (4x A100)
    python -m neuroagent.training.train_grpo \
        --stage grpo \
        --backend verl \
        --model Qwen/Qwen3.5-9B \
        --data training_data/grpo_dataset/train.parquet
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# LoRA configuration
# ---------------------------------------------------------------------------

def get_lora_config(rank: int = 64, alpha: int = 32):
    """Build LoRA config targeting attention + MLP layers."""
    from peft import LoraConfig

    return LoraConfig(
        r=rank,
        lora_alpha=alpha,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",  # attention
            "gate_proj", "up_proj", "down_proj",       # MLP
        ],
    )


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_sft_data(data_path: str, top_fraction: float = 0.1) -> list[dict]:
    """Load top trajectories for SFT warmup.

    Selects the top `top_fraction` by reward as gold demonstrations.
    """
    path = Path(data_path)
    examples = []

    if path.suffix == ".jsonl":
        with open(path) as f:
            for line in f:
                examples.append(json.loads(line))
    elif path.suffix == ".json":
        examples = json.loads(path.read_text())
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")

    # For full-trajectory format, flatten completions with rewards
    flat = []
    for ex in examples:
        if "completions" in ex:
            for comp, rew in zip(ex["completions"], ex["rewards"]):
                flat.append({
                    "prompt": ex["prompt"],
                    "completion": comp,
                    "reward": rew,
                })
        else:
            flat.append(ex)

    # Sort by reward descending, take top fraction
    flat.sort(key=lambda x: x.get("reward", 0), reverse=True)
    n_top = max(1, int(len(flat) * top_fraction))
    top = flat[:n_top]

    logger.info("SFT data: %d total → top %d (%.0f%%)", len(flat), n_top, top_fraction * 100)
    return top


def load_grpo_data(data_path: str) -> list[dict]:
    """Load GRPO training data (grouped by prompt)."""
    path = Path(data_path)
    examples = []

    if path.suffix == ".jsonl":
        with open(path) as f:
            for line in f:
                examples.append(json.loads(line))
    elif path.suffix == ".json":
        examples = json.loads(path.read_text())
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")

    logger.info("GRPO data: %d examples loaded", len(examples))
    return examples


# ---------------------------------------------------------------------------
# Stage 1: SFT Warmup
# ---------------------------------------------------------------------------

def run_sft(
    model_name: str,
    data_path: str,
    output_dir: str,
    lora_rank: int = 64,
    lora_alpha: int = 32,
    epochs: int = 2,
    batch_size: int = 4,
    learning_rate: float = 2e-5,
    max_seq_length: int = 4096,
    bf16: bool = True,
) -> None:
    """Run SFT warmup on top trajectories."""
    import torch
    from datasets import Dataset
    from peft import get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import SFTConfig, SFTTrainer

    logger.info("Loading model: %s", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16 if bf16 else torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )

    # Apply LoRA
    lora_config = get_lora_config(rank=lora_rank, alpha=lora_alpha)
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load data
    top_examples = load_sft_data(data_path)

    # Format as chat messages
    formatted = []
    for ex in top_examples:
        messages = []
        if ex.get("prompt"):
            messages.append({"role": "system", "content": ex["prompt"]})
        messages.append({"role": "assistant", "content": ex["completion"]})
        formatted.append({"messages": messages})

    dataset = Dataset.from_list(formatted)

    # Training config
    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        max_seq_length=max_seq_length,
        bf16=bf16,
        logging_steps=10,
        save_steps=100,
        save_total_limit=2,
        gradient_checkpointing=True,
        warmup_ratio=0.1,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )

    logger.info("Starting SFT training for %d epochs", epochs)
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    logger.info("SFT model saved to %s", output_dir)


# ---------------------------------------------------------------------------
# Stage 2: GRPO with TRL
# ---------------------------------------------------------------------------

def _build_reward_fn(
    reward_config: str,
    tool_costs_config: str,
    rules_dir: str,
    hospital: str,
):
    """Build the reward function for GRPO training.

    Returns a callable compatible with TRL GRPOTrainer.reward_funcs.
    """
    from .rewards.composite_reward import CompositeReward

    reward = CompositeReward.from_config(
        reward_config_path=reward_config,
        tool_costs_path=tool_costs_config,
        rules_dir=rules_dir,
        hospital=hospital,
    )
    return reward


def run_grpo_trl(
    model_name: str,
    data_path: str,
    output_dir: str,
    lora_rank: int = 64,
    lora_alpha: int = 32,
    epochs: int = 15,
    batch_size: int = 4,
    learning_rate: float = 3e-6,
    num_generations: int = 8,
    max_completion_length: int = 4096,
    max_prompt_length: int = 2048,
    temperature: float = 1.0,
    kl_coeff: float = 0.001,
    bf16: bool = True,
    use_vllm: bool = False,
) -> None:
    """Run GRPO training using TRL GRPOTrainer."""
    import torch
    from datasets import Dataset
    from peft import get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import GRPOConfig, GRPOTrainer

    logger.info("Loading model: %s", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16 if bf16 else torch.float16,
        device_map="auto",
        trust_remote_code=True,
    )

    # Apply LoRA
    lora_config = get_lora_config(rank=lora_rank, alpha=lora_alpha)
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load data — format as prompts for GRPO
    raw_data = load_grpo_data(data_path)

    # GRPO expects: each example has a "prompt" field
    # The trainer generates completions and scores them with reward_funcs
    formatted = []
    for ex in raw_data:
        prompt_messages = [{"role": "user", "content": ex.get("prompt", "")}]
        formatted.append({"prompt": prompt_messages})

    dataset = Dataset.from_list(formatted)

    # Pre-computed rewards as a reward function
    # For offline GRPO with pre-scored trajectories:
    reward_data = {}
    for ex in raw_data:
        if "completions" in ex and "rewards" in ex:
            for comp, rew in zip(ex["completions"], ex["rewards"]):
                reward_data[comp[:200]] = rew  # key by prefix

    def precomputed_reward(completions: list[str], **kwargs) -> list[float]:
        """Look up pre-computed rewards, fall back to 0."""
        rewards = []
        for comp in completions:
            key = comp[:200]
            rewards.append(reward_data.get(key, 0.0))
        return rewards

    # GRPO config
    training_args = GRPOConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=2,
        learning_rate=learning_rate,
        num_generations=num_generations,
        max_completion_length=max_completion_length,
        max_prompt_length=max_prompt_length,
        temperature=temperature,
        bf16=bf16,
        logging_steps=10,
        save_steps=50,
        save_total_limit=3,
        gradient_checkpointing=True,
        use_vllm=use_vllm,
    )

    trainer = GRPOTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        reward_funcs=precomputed_reward,
    )

    logger.info("Starting GRPO training for %d epochs", epochs)
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    logger.info("GRPO model saved to %s", output_dir)


# ---------------------------------------------------------------------------
# veRL backend (multi-GPU)
# ---------------------------------------------------------------------------

def generate_verl_script(
    model_name: str,
    data_path: str,
    output_dir: str,
    n_gpus: int = 4,
    lora_rank: int = 64,
    lora_alpha: int = 32,
    epochs: int = 15,
    batch_size: int = 512,
    rollout_n: int = 8,
    learning_rate: float = 3e-6,
    kl_coeff: float = 0.001,
) -> str:
    """Generate a veRL training bash script.

    veRL is configured via CLI args, so we generate a runnable script
    rather than calling Python APIs directly.
    """
    script = f"""#!/bin/bash
# veRL GRPO + LoRA training script for NeuroAgent
# Generated by neuroagent.training.train_grpo
set -x

export PYTHONUNBUFFERED=1
export CUDA_DEVICE_ORDER="PCI_BUS_ID"

python3 -m verl.trainer.main_ppo \\
    \\
    # === ALGORITHM === \\
    algorithm.adv_estimator=grpo \\
    algorithm.use_kl_in_reward=False \\
    \\
    # === DATA === \\
    data.train_files={data_path} \\
    data.train_batch_size={batch_size} \\
    data.max_prompt_length=2048 \\
    data.max_response_length=4096 \\
    data.filter_overlong_prompts=True \\
    data.truncation=error \\
    \\
    # === MODEL === \\
    actor_rollout_ref.model.path={model_name} \\
    actor_rollout_ref.model.lora_rank={lora_rank} \\
    actor_rollout_ref.model.lora_alpha={lora_alpha} \\
    actor_rollout_ref.model.use_remove_padding=True \\
    actor_rollout_ref.model.enable_gradient_checkpointing=True \\
    \\
    # === ACTOR === \\
    actor_rollout_ref.actor.optim.lr={learning_rate} \\
    actor_rollout_ref.actor.ppo_mini_batch_size=256 \\
    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=20 \\
    actor_rollout_ref.actor.use_kl_loss=True \\
    actor_rollout_ref.actor.kl_loss_coef={kl_coeff} \\
    actor_rollout_ref.actor.kl_loss_type=low_var_kl \\
    actor_rollout_ref.actor.entropy_coeff=0 \\
    actor_rollout_ref.actor.fsdp_config.param_offload=False \\
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=False \\
    \\
    # === ROLLOUT (vLLM) === \\
    actor_rollout_ref.rollout.name=vllm \\
    actor_rollout_ref.rollout.tensor_model_parallel_size=1 \\
    actor_rollout_ref.rollout.n={rollout_n} \\
    actor_rollout_ref.rollout.gpu_memory_utilization=0.7 \\
    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=20 \\
    actor_rollout_ref.rollout.load_format=safetensors \\
    \\
    # === REFERENCE MODEL === \\
    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=20 \\
    actor_rollout_ref.ref.fsdp_config.param_offload=True \\
    \\
    # === TRAINER === \\
    trainer.critic_warmup=0 \\
    trainer.val_before_train=False \\
    trainer.n_gpus_per_node={n_gpus} \\
    trainer.nnodes=1 \\
    trainer.total_epochs={epochs} \\
    trainer.save_freq=50 \\
    trainer.save_total_limit=3 \\
    trainer.test_freq=5 \\
    \\
    # === LOGGING === \\
    trainer.logger='["console","wandb"]' \\
    trainer.project_name=neuroagent_grpo \\
    trainer.experiment_name=neuroagent_{model_name.split("/")[-1]}_grpo_lora \\
    \\
    "$@"
"""
    # Save script
    output_path = Path(output_dir) / "run_verl_grpo.sh"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(script)
    output_path.chmod(0o755)
    logger.info("Generated veRL script: %s", output_path)
    return str(output_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="NeuroAgent GRPO training")
    parser.add_argument("--stage", choices=["sft", "grpo"], required=True)
    parser.add_argument("--backend", choices=["trl", "verl"], default="trl")
    parser.add_argument("--model", required=True, help="Model name or checkpoint path")
    parser.add_argument("--data", required=True, help="Training data path")
    parser.add_argument("--output", required=True, help="Output directory")

    # LoRA
    parser.add_argument("--lora-rank", type=int, default=64)
    parser.add_argument("--lora-alpha", type=int, default=32)

    # Training
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--num-generations", type=int, default=8)
    parser.add_argument("--max-completion-length", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--kl-coeff", type=float, default=0.001)
    parser.add_argument("--use-vllm", action="store_true")
    parser.add_argument("--bf16", action="store_true", default=True)

    # Reward (for online GRPO)
    parser.add_argument("--reward-config", default="config/reward_weights.yaml")
    parser.add_argument("--tool-costs", default="config/tool_costs.yaml")
    parser.add_argument("--rules-dir", default="config/hospital_rules")
    parser.add_argument("--hospital", default="us_mayo")

    # veRL-specific
    parser.add_argument("--n-gpus", type=int, default=4)

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.stage == "sft":
        epochs = args.epochs or 2
        lr = args.lr or 2e-5
        run_sft(
            model_name=args.model,
            data_path=args.data,
            output_dir=args.output,
            lora_rank=args.lora_rank,
            lora_alpha=args.lora_alpha,
            epochs=epochs,
            batch_size=args.batch_size,
            learning_rate=lr,
            bf16=args.bf16,
        )

    elif args.stage == "grpo":
        epochs = args.epochs or 15
        lr = args.lr or 3e-6

        if args.backend == "verl":
            generate_verl_script(
                model_name=args.model,
                data_path=args.data,
                output_dir=args.output,
                n_gpus=args.n_gpus,
                lora_rank=args.lora_rank,
                lora_alpha=args.lora_alpha,
                epochs=epochs,
                rollout_n=args.num_generations,
                learning_rate=lr,
                kl_coeff=args.kl_coeff,
            )
        else:
            run_grpo_trl(
                model_name=args.model,
                data_path=args.data,
                output_dir=args.output,
                lora_rank=args.lora_rank,
                lora_alpha=args.lora_alpha,
                epochs=epochs,
                batch_size=args.batch_size,
                learning_rate=lr,
                num_generations=args.num_generations,
                max_completion_length=args.max_completion_length,
                temperature=args.temperature,
                kl_coeff=args.kl_coeff,
                bf16=args.bf16,
                use_vllm=args.use_vllm,
            )


if __name__ == "__main__":
    main()
