"""Merge LoRA adapter weights into the base model for deployment.

After GRPO training, merge the LoRA adapter into the base model weights
so it can be served directly via vLLM without adapter overhead.

Usage:
    python -m neuroagent.training.merge_adapter \
        --base-model Qwen/Qwen3.5-9B \
        --adapter checkpoints/grpo_final \
        --output models/neuroagent-qwen3.5-9b-grpo
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def merge_and_save(
    base_model: str,
    adapter_path: str,
    output_dir: str,
    push_to_hub: bool = False,
    hub_name: str | None = None,
) -> None:
    """Merge LoRA adapter into base model and save.

    Args:
        base_model: HuggingFace model name or local path.
        adapter_path: Path to LoRA adapter checkpoint.
        output_dir: Where to save the merged model.
        push_to_hub: Whether to push to HuggingFace Hub.
        hub_name: Hub model name (required if push_to_hub).
    """
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    logger.info("Loading base model: %s", base_model)
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.bfloat16,
        device_map="cpu",  # Merge on CPU to avoid GPU memory issues
        trust_remote_code=True,
    )

    logger.info("Loading adapter: %s", adapter_path)
    model = PeftModel.from_pretrained(model, adapter_path)

    logger.info("Merging adapter weights into base model...")
    model = model.merge_and_unload()

    logger.info("Saving merged model to: %s", output_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir)

    # Save tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    tokenizer.save_pretrained(output_dir)

    if push_to_hub and hub_name:
        logger.info("Pushing to Hub: %s", hub_name)
        model.push_to_hub(hub_name)
        tokenizer.push_to_hub(hub_name)

    logger.info("Done. Merged model at: %s", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge LoRA adapter into base model")
    parser.add_argument("--base-model", required=True, help="Base model name/path")
    parser.add_argument("--adapter", required=True, help="LoRA adapter checkpoint path")
    parser.add_argument("--output", required=True, help="Output directory for merged model")
    parser.add_argument("--push-to-hub", action="store_true")
    parser.add_argument("--hub-name", default=None)

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    merge_and_save(
        base_model=args.base_model,
        adapter_path=args.adapter,
        output_dir=args.output,
        push_to_hub=args.push_to_hub,
        hub_name=args.hub_name,
    )


if __name__ == "__main__":
    main()
