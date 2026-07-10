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
import os
import random
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# LoRA configuration
# ---------------------------------------------------------------------------

# Qwen3.5 is a *hybrid* architecture: `config.layer_types` interleaves 3 `linear_attention`
# layers (Qwen3_5GatedDeltaNet) for every 1 `full_attention` layer (Qwen3_5Attention).
# On Qwen3.5-9B that is 24 linear-attention vs 8 full-attention layers.
#
# The classic ["q_proj","k_proj","v_proj","o_proj"] list only exists inside the 8 full
# attention layers, so targeting it alone leaves the token-mixing of 24/32 layers entirely
# frozen. The gated-delta-net layers project through different module names.
QWEN35_FULL_ATTENTION_MODULES = ["q_proj", "k_proj", "v_proj", "o_proj"]

# Gated-delta-net (linear attention) projections.
# `in_proj_a` / `in_proj_b` are deliberately excluded: they are (hidden_size, num_v_heads)
# = (4096, 32) per-head gating projections, so out_features < the usual LoRA rank. A rank-64
# adapter there holds more parameters than the weight it adapts and cannot be low-rank at all.
QWEN35_LINEAR_ATTENTION_MODULES = ["in_proj_qkv", "in_proj_z", "out_proj"]

QWEN35_MLP_MODULES = ["gate_proj", "up_proj", "down_proj"]

QWEN35_TARGET_MODULES = (
    QWEN35_FULL_ATTENTION_MODULES + QWEN35_LINEAR_ATTENTION_MODULES + QWEN35_MLP_MODULES
)


def get_lora_config(rank: int = 64, alpha: int = 128, target_modules: list[str] | None = None):
    """Build LoRA config covering BOTH attention families of the hybrid Qwen3.5 stack."""
    from peft import LoraConfig

    return LoraConfig(
        r=rank,
        lora_alpha=alpha,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=target_modules or QWEN35_TARGET_MODULES,
    )


def get_quantization_config():
    """Build BitsAndBytes config for QLoRA (NF4 quantization)."""
    import torch
    from transformers import BitsAndBytesConfig

    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
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

def _split_trajectories(
    examples: list[dict],
    splits_dir: str,
    val_fraction: float = 0.1,
    seed: int = 42,
) -> tuple[list[dict], list[dict]]:
    """Split trajectories into train/val, carving validation out of the TRAIN split.

    The held-out test set (`test_cases.txt`) is never touched here — no gold trajectory
    exists for it by construction. Validation is carved from train *by case_id*, so both
    styles of a case land on the same side and a case cannot be memorised in train and
    scored in val.
    """
    splits_path = Path(splits_dir)
    train_file = splits_path / "train_cases.txt"
    test_file = splits_path / "test_cases.txt"

    if not train_file.exists():
        logger.warning("No train_cases.txt at %s, using all data for training", splits_path)
        return examples, []

    train_cases = {c for c in train_file.read_text().split() if c}
    test_cases = {c for c in test_file.read_text().split() if c} if test_file.exists() else set()

    leaked = [ex for ex in examples if ex.get("case_id", "") in test_cases]
    if leaked:
        raise ValueError(
            f"{len(leaked)} trajectories belong to held-out test cases "
            f"(e.g. {leaked[0].get('case_id')}). Regenerate prompts from the train split."
        )

    unknown = [ex for ex in examples if ex.get("case_id", "") not in train_cases]
    if unknown:
        logger.warning("%d trajectories have case_ids outside the train split", len(unknown))

    val_case_ids: set[str] = set()
    if val_fraction > 0:
        ordered = sorted(train_cases)
        rng = random.Random(seed)
        rng.shuffle(ordered)
        n_val = int(len(ordered) * val_fraction)
        val_case_ids = set(ordered[:n_val])

    train = [ex for ex in examples if ex.get("case_id", "") not in val_case_ids]
    val = [ex for ex in examples if ex.get("case_id", "") in val_case_ids]

    logger.info(
        "Split: %d train / %d val trajectories (%d val cases, val_fraction=%.2f)",
        len(train), len(val), len(val_case_ids), val_fraction,
    )
    return train, val


def run_sft(
    model_name: str,
    data_path: str,
    output_dir: str,
    lora_rank: int = 64,
    lora_alpha: int = 128,
    epochs: int = 2,
    batch_size: int = 4,
    learning_rate: float = 2e-5,
    max_seq_length: int = 4096,
    bf16: bool = True,
    qlora: bool = False,
    top_fraction: float = 1.0,
    splits_dir: str | None = None,
    val_fraction: float = 0.1,
    use_liger: bool = True,
) -> None:
    """Run SFT warmup on top trajectories.

    Supports two data formats:
    1. Gold trajectories (from generate_gold_trajectories.py): each example has
       a "messages" field with the full multi-turn conversation.
    2. Legacy format: each example has "prompt" and "completion" fields.

    Args:
        qlora: If True, load base model in 4-bit NF4 quantization (QLoRA).
        splits_dir: Path to the split directory (e.g., data/neurobench/splits/) holding
            train_cases.txt / test_cases.txt. Validation is carved out of the train split.
        val_fraction: Fraction of TRAIN cases held out for eval_loss / best-model selection.
    """
    import torch
    from datasets import Dataset
    from peft import get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import SFTConfig, SFTTrainer

    from .chat_template import apply_training_chat_template

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

    # Prepare for k-bit training if QLoRA
    if qlora:
        model = prepare_model_for_kbit_training(model)

    # Apply LoRA
    lora_config = get_lora_config(rank=lora_rank, alpha=lora_alpha)
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load data and optionally split into train/val
    top_examples = load_sft_data(data_path, top_fraction=top_fraction)

    train_examples, val_examples = top_examples, []
    if splits_dir:
        train_examples, val_examples = _split_trajectories(top_examples, splits_dir, val_fraction)
    else:
        logger.info("No splits_dir provided, using all %d examples for training (no validation)", len(top_examples))

    # Gold trajectories are conversational (`messages` with structured `tool_calls`).
    # We hand them to TRL as-is and let Qwen's own chat template render them, so the
    # training text is byte-identical to what the served model sees at inference.
    #
    # Loss masking: the shipped template has no `{% generation %}` markers, so we patch
    # them in (see training/chat_template.py) and set `assistant_only_loss=True`. Loss
    # then falls on thoughts + tool calls + final answer only — never on tool
    # observations, which the model must learn to *read*, not to *invent*.
    conversational = bool(train_examples) and "messages" in train_examples[0]

    if conversational:
        apply_training_chat_template(tokenizer)
        dataset = Dataset.from_list([{"messages": ex["messages"]} for ex in train_examples])
        eval_dataset = (
            Dataset.from_list([{"messages": ex["messages"]} for ex in val_examples])
            if val_examples
            else None
        )
    else:
        def _to_prompt_completion(examples: list[dict]) -> list[dict]:
            """Legacy prompt/completion examples (pre-gold-trajectory format)."""
            formatted = []
            for ex in examples:
                prompt = ex.get("system_prompt", ex.get("prompt", ""))
                if ex.get("patient_info"):
                    prompt += "\n\n" + ex["patient_info"]
                formatted.append({"prompt": prompt, "completion": ex.get("completion", "")})
            return formatted

        dataset = Dataset.from_list(_to_prompt_completion(train_examples))
        eval_dataset = (
            Dataset.from_list(_to_prompt_completion(val_examples)) if val_examples else None
        )

    if eval_dataset is not None:
        logger.info("Eval dataset: %d examples", len(eval_dataset))

    # Training config — following SFT best practices:
    # - completion_only_loss=True: only compute loss on completion tokens (not prompt)
    # - cosine scheduler for smoother convergence
    # - weight_decay for regularization (important with 600 examples)
    # - neftune_noise_alpha for embedding noise regularization
    # - eval_strategy with validation set if available
    # Configure eval strategy based on whether we have a validation set
    eval_kwargs = {}
    if eval_dataset is not None:
        eval_kwargs = {
            "eval_strategy": "epoch",
            "per_device_eval_batch_size": 1,
            "eval_accumulation_steps": 8,
            "load_best_model_at_end": True,
            "metric_for_best_model": "eval_loss",
            "greater_is_better": False,
        }

    # Conversational data masks via assistant_only_loss; legacy prompt/completion data
    # masks via completion_only_loss. Setting both is contradictory.
    loss_mask_kwargs = (
        {"assistant_only_loss": True} if conversational else {"completion_only_loss": True}
    )

    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=8,
        learning_rate=learning_rate,
        max_length=max_seq_length,
        bf16=bf16,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        save_only_model=True,
        gradient_checkpointing=True,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        weight_decay=0.01,
        neftune_noise_alpha=5.0,
        # Qwen3.5's vocabulary is 248k, so a full logits tensor at seq=8192 is ~4 GB in
        # bf16 and ~8 GB once cross-entropy upcasts to fp32 — the dominant memory term,
        # and what OOMs a 40 GB card. Liger's fused linear cross-entropy computes the loss
        # in chunks without ever materialising full logits.
        use_liger_kernel=use_liger,
        **loss_mask_kwargs,
        **eval_kwargs,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
    )

    logger.info("Starting SFT training for %d epochs on %d examples", epochs, len(dataset))
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
    base_model: str | None = None,
    lora_rank: int = 64,
    lora_alpha: int = 128,
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
    qlora: bool = False,
) -> None:
    """Run GRPO training using TRL GRPOTrainer.

    Args:
        model_name: Model name or PEFT adapter checkpoint path.
        base_model: If model_name is an adapter, this is the base model name.
            Auto-detected from adapter_config.json if not specified.
    """
    import torch
    from datasets import Dataset
    from peft import PeftModel, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import GRPOConfig, GRPOTrainer

    # Detect if model_name is a PEFT adapter checkpoint
    adapter_path = None
    model_path = Path(model_name)
    if model_path.exists() and (model_path / "adapter_config.json").exists():
        adapter_path = str(model_path)
        if base_model is None:
            import json
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

    # Load existing adapter (SFT checkpoint) or create fresh LoRA
    if adapter_path:
        logger.info("Loading SFT adapter from %s", adapter_path)
        model = PeftModel.from_pretrained(model, adapter_path, is_trainable=True)
    else:
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

    # Build reward function — prefer online scoring if dataset is available
    reward_func = None
    dataset_path_env = os.environ.get("NEUROAGENT_DATASET", "data/neurobench")
    dataset_dir = Path(dataset_path_env)

    if (dataset_dir / "cases").exists():
        logger.info("Using ONLINE reward (MockServer + CompositeReward)")
        from .rewards.online_reward import OnlineRewardFunction, build_prompt_to_case_mapping
        from ..tools.cost_tracker import CostTracker

        case_mapping = build_prompt_to_case_mapping(dataset_dir)
        cost_tracker = CostTracker()
        reward_func = OnlineRewardFunction(cases=case_mapping, cost_tracker=cost_tracker)
    else:
        logger.info("Using OFFLINE pre-computed rewards (dataset not found at %s)", dataset_dir)
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

    # GRPO config — TRL v0.29+ API
    # generation_batch_size must be >= num_generations
    gen_batch = max(batch_size, num_generations)
    training_args = GRPOConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=2,
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
    )

    trainer = GRPOTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        reward_funcs=reward_func,
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
    parser.add_argument("--model", required=True, help="Model name or PEFT adapter checkpoint path")
    parser.add_argument("--base-model", default=None, help="Base model name (auto-detected from adapter if not set)")
    parser.add_argument("--data", required=True, help="Training data path")
    parser.add_argument("--output", required=True, help="Output directory")

    # LoRA
    parser.add_argument("--lora-rank", type=int, default=64)
    parser.add_argument("--lora-alpha", type=int, default=128)

    # Training
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--num-generations", type=int, default=8)
    parser.add_argument("--max-completion-length", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--kl-coeff", type=float, default=0.001)
    parser.add_argument("--use-vllm", action="store_true")
    parser.add_argument("--top-fraction", type=float, default=1.0,
                        help="Fraction of top trajectories for SFT (1.0 = use all, 0.1 = top 10%%)")
    parser.add_argument("--qlora", action="store_true", help="Use QLoRA (4-bit NF4 quantization)")
    parser.add_argument("--splits-dir", default=None, help="Split dir with train_cases.txt / test_cases.txt (e.g., data/neurobench/splits/)")
    parser.add_argument("--val-fraction", type=float, default=0.1,
                        help="Fraction of train cases carved out for validation")
    parser.add_argument("--max-seq-length", type=int, default=8192,
                        help="Max sequence length; set from scripts/training/probe_max_seq_length.py")
    parser.add_argument("--no-liger", dest="use_liger", action="store_false", default=True,
                        help="Disable Liger fused cross-entropy (needed on 248k-vocab Qwen3.5)")
    parser.add_argument("--bf16", action="store_true", default=True)

    # Reward (for online GRPO)
    parser.add_argument("--reward-config", default="config/training/reward_weights.yaml")
    parser.add_argument("--tool-costs", default="config/tools/costs.yaml")
    parser.add_argument("--rules-dir", default="config/hospital_rules")
    parser.add_argument("--hospital", default="us_mayo")

    # veRL-specific
    parser.add_argument("--n-gpus", type=int, default=4)

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    if args.stage == "sft":
        epochs = args.epochs or 5
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
            qlora=args.qlora,
            top_fraction=args.top_fraction,
            splits_dir=args.splits_dir,
            val_fraction=args.val_fraction,
            max_seq_length=args.max_seq_length,
            use_liger=args.use_liger,
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
                base_model=args.base_model,
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
                qlora=args.qlora,
            )


if __name__ == "__main__":
    main()
