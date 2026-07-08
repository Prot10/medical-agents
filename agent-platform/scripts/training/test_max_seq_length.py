"""Find the maximum sequence length for QLoRA SFT on A100-40GB.

Tests increasing seq_lengths until OOM, then reports the max.
"""

from __future__ import annotations

import gc
import time

import torch
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer


def test_seq_length(model, tokenizer, seq_length: int, batch_size: int = 1) -> tuple[bool, float]:
    """Try one training step at the given seq_length. Returns (success, peak_gb)."""
    torch.cuda.reset_peak_memory_stats()
    torch.cuda.empty_cache()
    gc.collect()

    # Create synthetic data at the target length
    dummy_text = "Hello " * (seq_length // 2)  # rough approximation
    dataset = Dataset.from_list([
        {"messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": dummy_text},
            {"role": "assistant", "content": dummy_text},
        ]}
        for _ in range(4)
    ])

    training_args = SFTConfig(
        output_dir="/tmp/seq_test",
        max_steps=1,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=1,
        learning_rate=2e-5,
        max_length=seq_length,
        bf16=True,
        logging_steps=1,
        gradient_checkpointing=True,
        warmup_steps=0,
        save_strategy="no",
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )

    try:
        trainer.train()
        peak = torch.cuda.max_memory_allocated() / 1e9
        return True, peak
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        gc.collect()
        return False, 0.0
    finally:
        del trainer
        torch.cuda.empty_cache()
        gc.collect()


def main():
    model_name = "Qwen/Qwen3.5-9B"

    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print()

    # Load model with QLoRA
    print("Loading model with NF4 quantization...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

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

    lora_config = LoraConfig(
        r=64, lora_alpha=128, lora_dropout=0.05, bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_config)
    base_mem = torch.cuda.max_memory_allocated() / 1e9
    print(f"Base memory (model + LoRA): {base_mem:.2f} GB\n")

    # Binary search for max seq_length
    seq_lengths = [1024, 2048, 3072, 4096, 5120, 6144, 7168, 8192]

    print(f"{'seq_len':>8} | {'status':>8} | {'peak_gb':>10} | {'headroom':>10}")
    print("-" * 50)

    max_working = 0
    for sl in seq_lengths:
        success, peak = test_seq_length(model, tokenizer, sl, batch_size=1)
        status = "OK" if success else "OOM"
        headroom = f"{40.0 - peak:.1f} GB" if success else "---"
        print(f"{sl:>8} | {status:>8} | {peak:>9.2f}G | {headroom:>10}")

        if success:
            max_working = sl
        else:
            break

    print(f"\n{'=' * 50}")
    print(f"Max seq_length at batch=1: {max_working}")
    print(f"Recommended for training (with safety margin): {max_working - 1024 if max_working > 1024 else max_working}")
    print(f"{'=' * 50}")

    # Also test with batch_size=2 at the working length
    if max_working >= 2048:
        test_len = max_working - 1024  # conservative
        success, peak = test_seq_length(model, tokenizer, test_len, batch_size=2)
        if success:
            print(f"\nBatch=2 at seq={test_len}: OK (peak {peak:.2f} GB)")
        else:
            print(f"\nBatch=2 at seq={test_len}: OOM")


if __name__ == "__main__":
    main()
