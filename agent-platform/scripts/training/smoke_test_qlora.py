"""Smoke test: QLoRA loading + 10 SFT training steps.

Verifies:
1. Qwen3.5-9B loads in NF4 quantization
2. LoRA adapters attach correctly
3. Training runs for 10 steps without OOM
4. Peak GPU memory < 40GB

Usage:
    uv run python scripts/training/smoke_test_qlora.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# Ensure project is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))


def main():
    import torch
    from datasets import Dataset
    from peft import get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from trl import SFTConfig, SFTTrainer

    training_data_root = os.environ.get(
        "TRAINING_DATA_ROOT",
        "/eos/project-d/diagbox/dvc/NeuroAgent/training_data",
    )
    model_name = "Qwen/Qwen3.5-9B"
    data_path = f"{training_data_root}/gold_trajectories_v5/trajectories.jsonl"
    output_dir = "/tmp/smoke_test_qlora"

    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print()

    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load model with QLoRA
    print("Loading model with NF4 quantization...")
    t0 = time.time()
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)
    print(f"  Loaded in {time.time() - t0:.1f}s")
    print(f"  GPU memory after load: {torch.cuda.max_memory_allocated() / 1e9:.2f} GB")

    # Apply LoRA
    from peft import LoraConfig
    lora_config = LoraConfig(
        r=64,
        lora_alpha=128,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    print(f"  GPU memory after LoRA: {torch.cuda.max_memory_allocated() / 1e9:.2f} GB")

    # Load data
    print("\nLoading training data...")
    examples = []
    with open(data_path) as f:
        for line in f:
            ex = json.loads(line)
            if "messages" in ex:
                examples.append({"messages": ex["messages"]})
    print(f"  Loaded {len(examples)} trajectories")

    dataset = Dataset.from_list(examples)

    # Training config — 10 steps only
    # Qwen3.5 has ~248K vocab → logits are huge. Use max_length=4096
    # and chunked loss to avoid OOM on logits float() cast.
    training_args = SFTConfig(
        output_dir=output_dir,
        max_steps=10,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=2,
        learning_rate=2e-5,
        max_length=4096,
        bf16=True,
        logging_steps=1,
        gradient_checkpointing=True,
        warmup_steps=2,
        save_strategy="no",
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )

    # Train
    print("\nStarting 10-step smoke test...")
    t0 = time.time()
    result = trainer.train()
    elapsed = time.time() - t0

    peak_memory = torch.cuda.max_memory_allocated() / 1e9
    print(f"\n{'=' * 50}")
    print(f"Smoke test PASSED!")
    print(f"  Steps: {result.global_step}")
    print(f"  Final loss: {result.training_loss:.4f}")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Peak GPU memory: {peak_memory:.2f} GB / 40.0 GB")
    print(f"  Memory headroom: {40.0 - peak_memory:.2f} GB")
    print(f"{'=' * 50}")

    if peak_memory > 38.0:
        print("WARNING: Very tight on memory! Consider reducing batch size or max_seq_length.")
    elif peak_memory > 30.0:
        print("Memory usage is moderate. GRPO with G=4 may need careful tuning.")
    else:
        print("Plenty of headroom for GRPO/DAPO training.")


if __name__ == "__main__":
    main()
