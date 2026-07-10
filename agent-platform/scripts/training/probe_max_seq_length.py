"""Probe the maximum SFT sequence length for QLoRA on the A100-40GB.

Runs the *real* SFT recipe (QLoRA NF4, LoRA r=64/alpha=128, gradient checkpointing,
NEFTune, bf16) at increasing sequence lengths until OOM, for each target model.
The smallest max across models sets the shared trajectory token budget.

Models are read from the EOS HF cache; nothing is downloaded to local disk.

Usage:
    HF_HOME=/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface \
        uv run python agent-platform/scripts/training/probe_max_seq_length.py \
            --models Qwen/Qwen3.5-9B Qwen/Qwen3.5-4B \
            --output results/sft_probe/max_seq_probe.json
"""

from __future__ import annotations

import argparse
import gc
import json
import logging
from pathlib import Path

import torch
from datasets import Dataset
from peft import get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer

from neuroagent.training.train_grpo import get_lora_config

logger = logging.getLogger(__name__)

# Sequence lengths to probe, ascending. Stops at the first OOM.
# The longest real trajectory is 12,956 tokens once the tool schemas are rendered into the
# prompt, so 13312 is the first length that truncates nothing. Anything below it cuts the
# tail of a trajectory — which is the final diagnosis, the one thing SFT must learn.
DEFAULT_SEQ_LENGTHS = [4096, 6144, 8192, 10240, 12288, 13312, 16384]

# Long filler text; truncation at max_length guarantees exactly seq_length tokens.
_FILLER_SENTENCE = (
    "The patient presents with progressive left-sided weakness and hyperreflexia; "
    "the differential includes motor neuron disease, cervical myelopathy, and stroke. "
)


def _make_dataset(seq_length: int, n_rows: int = 4) -> Dataset:
    """Build a dataset whose rows tokenize to at least seq_length tokens.

    We over-generate text and rely on SFTConfig(max_length=seq_length) truncation, so
    every row is exactly seq_length tokens — an approximation-free memory probe.
    """
    # ~14 tokens per sentence; 3x oversupply so truncation always binds.
    n_sentences = (seq_length // 10) * 3
    text = _FILLER_SENTENCE * n_sentences
    return Dataset.from_list([{"text": text} for _ in range(n_rows)])


def test_seq_length(
    model,
    tokenizer,
    seq_length: int,
    batch_size: int = 1,
    liger: bool = False,
) -> tuple[bool, float]:
    """Run 2 training steps at seq_length. Returns (success, peak_gb).

    Two steps rather than one so optimizer state is materialized.

    Qwen3.5's vocabulary is 248k, so the logits tensor alone is ~4 GB (bf16) at
    seq=8192 and doubles again when cross-entropy upcasts to fp32. `liger=True`
    swaps in a fused linear cross-entropy that never materialises full logits.
    """
    torch.cuda.empty_cache()
    gc.collect()
    torch.cuda.reset_peak_memory_stats()

    dataset = _make_dataset(seq_length)

    training_args = SFTConfig(
        output_dir="/tmp/seq_probe",
        max_steps=2,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=1,
        learning_rate=2e-5,
        max_length=seq_length,
        packing=False,
        bf16=True,
        gradient_checkpointing=True,
        # Mirror the real recipe in `run_sft`, or the probe measures a run nobody will do.
        neftune_noise_alpha=None,
        optim="paged_adamw_8bit",
        use_liger_kernel=liger,
        logging_strategy="no",
        warmup_steps=0,
        save_strategy="no",
        report_to="none",
    )

    trainer = None
    try:
        trainer = SFTTrainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
            processing_class=tokenizer,
        )
        trainer.train()
        peak = torch.cuda.max_memory_allocated() / 1e9
        return True, peak
    except torch.cuda.OutOfMemoryError:
        return False, 0.0
    except RuntimeError as e:
        # bitsandbytes / cublas sometimes surface OOM as a generic RuntimeError.
        if "out of memory" in str(e).lower():
            return False, 0.0
        raise
    finally:
        if trainer is not None:
            del trainer
        torch.cuda.empty_cache()
        gc.collect()


def probe_model(model_name: str, seq_lengths: list[int], liger: bool = False) -> dict:
    """Load one model with the real QLoRA recipe and probe seq lengths."""
    print(f"\n{'=' * 62}\n Probing {model_name}\n{'=' * 62}")

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

    # Same LoRA config the real training run uses — including the gated-delta-net
    # projections, without which 24 of Qwen3.5-9B's 32 layers stay frozen.
    model = get_peft_model(model, get_lora_config(rank=64, alpha=128))
    model.print_trainable_parameters()

    base_mem = torch.cuda.max_memory_allocated() / 1e9
    print(f"Base memory (4-bit model + LoRA): {base_mem:.2f} GB\n")
    print(f"{'seq_len':>8} | {'status':>6} | {'peak_gb':>9} | {'headroom':>9}")
    print("-" * 46)

    total_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
    results: list[dict] = []
    max_working = 0

    for sl in seq_lengths:
        ok, peak = test_seq_length(model, tokenizer, sl, batch_size=1, liger=liger)
        status = "OK" if ok else "OOM"
        headroom = f"{total_gb - peak:.1f} GB" if ok else "---"
        print(f"{sl:>8} | {status:>6} | {peak:>8.2f}G | {headroom:>9}")
        results.append({"seq_length": sl, "ok": ok, "peak_gb": round(peak, 2)})
        if ok:
            max_working = sl
        else:
            break

    del model
    torch.cuda.empty_cache()
    gc.collect()

    return {
        "model": model_name,
        "liger": liger,
        "base_mem_gb": round(base_mem, 2),
        "max_seq_length": max_working,
        "trials": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe max SFT seq length per model")
    parser.add_argument("--models", nargs="+", default=["Qwen/Qwen3.5-9B", "Qwen/Qwen3.5-4B"])
    parser.add_argument("--seq-lengths", nargs="+", type=int, default=DEFAULT_SEQ_LENGTHS)
    parser.add_argument("--output", default="results/sft_probe/max_seq_probe.json")
    parser.add_argument("--liger", action="store_true", help="Use fused linear cross-entropy (Liger)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING)

    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

    probes = [probe_model(m, args.seq_lengths, liger=args.liger) for m in args.models]

    maxes = [p["max_seq_length"] for p in probes if p["max_seq_length"] > 0]
    shared = min(maxes) if maxes else 0

    summary = {
        "gpu": torch.cuda.get_device_name(0),
        "gpu_total_gb": round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1),
        "recipe": f"QLoRA NF4, r=64/alpha=128, grad_ckpt, NEFTune=5.0, bf16, bs=1, liger={args.liger}",
        "probes": probes,
        "shared_max_seq_length": shared,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2))

    print(f"\n{'=' * 62}")
    for p in probes:
        print(f"  {p['model']:<28} max_seq = {p['max_seq_length']}")
    print(f"  SHARED max_seq_length = {shared}")
    print(f"  Written to {out_path}")
    print("=" * 62)


if __name__ == "__main__":
    main()
