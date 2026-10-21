"""LoRA SFT over typed episodes: one sequence per episode, loss on the model's actions only.

The whole episode transcript is rendered once by the model's chat template, exactly as the
harness renders it turn by turn at inference, and every assistant turn is supervised in that
single forward pass (rollout-style). Two properties make this exact rather than approximate:

* prefix chaining — the generation prompt of turn k+1 starts with the full render through turn k
  (asserted per episode; a template that breaks it is an error, not a warning);
* boundary tokenization — prompt, action and inter-turn segments are tokenized separately and
  concatenated, so tokens never merge across the boundary where generation starts at inference.

The loss projects hidden states through the vocabulary only at supervised positions
(``logits_to_keep``), so the sequence-length × vocabulary logits tensor is never materialized.

    uv run python -m neuroagent.training.train_sft --model qwen3.5-9b \\
        --episodes training_data/approved_episodes.jsonl --output outputs/qwen-sft
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from ..model_registry import KEY_TO_MODEL

# fla's TileLang backend needs nvcc (absent on the training host); use the Triton kernels.
os.environ.setdefault("FLA_TILELANG", "0")
from .storage import WEIGHTS_ROOT, require_eos
from .data.episodes import load_case_map, load_episode_records, sft_rows


def episode_segments(tokenizer, rows: list[dict], template_kwargs: dict) -> list[tuple[str, bool]]:
    """Alternating (text, supervised) segments covering one episode's full transcript."""

    def render(messages, row, **kwargs):
        return tokenizer.apply_chat_template(
            messages, tools=row["tools"], tokenize=False, **template_kwargs, **kwargs
        )

    segments: list[tuple[str, bool]] = []
    rendered = ""
    for row in rows:
        prompt = render(row["prompt"], row, add_generation_prompt=True)
        full = render(row["prompt"] + row["completion"], row)
        if not prompt.startswith(rendered) or not full.startswith(prompt):
            raise ValueError("chat template does not chain turns as prefixes of one transcript")
        segments.append((prompt[len(rendered):], False))
        segments.append((full[len(prompt):], True))
        rendered = full
    return segments


def build_examples(model_key: str, episodes_path: str, cases_path: str, tokenizer, *, allow_candidates: bool) -> list[dict]:
    entry = KEY_TO_MODEL[model_key]
    records = load_episode_records(episodes_path, allow_candidates=allow_candidates)
    cases = load_case_map(cases_path)
    missing = sorted({record.case_id for record in records} - cases.keys())
    if missing:
        raise ValueError(f"episodes reference missing cases: {missing[:10]}")
    template_kwargs = entry["request_defaults"].get("chat_template_kwargs", {})
    examples = []
    for record in records:
        input_ids: list[int] = []
        mask: list[int] = []
        for text, supervised in episode_segments(tokenizer, sft_rows(record, cases[record.case_id]), template_kwargs):
            ids = tokenizer(text, add_special_tokens=False)["input_ids"]
            input_ids += ids
            mask += [int(supervised)] * len(ids)
        examples.append({"input_ids": input_ids, "completion_mask": mask})
    return examples


def train(
    *,
    model_key: str,
    episodes_path: str,
    cases_path: str,
    output_dir: str,
    allow_candidates: bool = False,
    epochs: float = 2.0,
    learning_rate: float = 1e-4,
    max_length: int = 32768,
    max_steps: int = -1,
) -> None:
    if model_key not in KEY_TO_MODEL:
        raise ValueError(f"model must be one of {sorted(KEY_TO_MODEL)}")
    try:
        import torch
        from datasets import Dataset
        from peft import LoraConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from trl import SFTConfig, SFTTrainer
    except ImportError as exc:
        raise RuntimeError("install the 'training' optional dependencies to run SFT") from exc

    model_id = KEY_TO_MODEL[model_key]["hf_model_id"]
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    examples = build_examples(model_key, episodes_path, cases_path, tokenizer, allow_candidates=allow_candidates)
    lengths = [len(example["input_ids"]) for example in examples]
    kept = [example for example in examples if len(example["input_ids"]) <= max_length]
    print(
        json.dumps(
            {
                "episodes": len(examples),
                "kept": len(kept),
                "dropped_over_max_length": len(examples) - len(kept),
                "max_tokens": max(lengths),
                "mean_tokens": round(sum(lengths) / len(lengths)),
                "mean_supervised_tokens": round(sum(sum(e["completion_mask"]) for e in examples) / len(examples)),
            }
        ),
        flush=True,
    )
    if not kept:
        raise ValueError("every episode exceeds max_length")

    class SparseLogitsSFTTrainer(SFTTrainer):
        """Cross-entropy from the vocabulary projection at supervised positions only."""

        def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
            labels = inputs["labels"]
            assert labels.shape[0] == 1, "one episode per micro-batch"
            keep = torch.nonzero(labels[0, 1:] != -100).squeeze(1)  # position t predicts t+1
            outputs = model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs.get("attention_mask"),
                logits_to_keep=keep,
            )
            targets = labels[0, keep + 1]
            loss = torch.nn.functional.cross_entropy(outputs.logits[0].float(), targets, reduction="sum")
            loss = loss / (num_items_in_batch if num_items_in_batch is not None else targets.numel())
            return (loss, outputs) if return_outputs else loss

    model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.bfloat16, device_map="cuda")
    trainer = SparseLogitsSFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=Dataset.from_list(kept),
        peft_config=LoraConfig(
            r=16,
            lora_alpha=32,
            lora_dropout=0.05,
            target_modules="all-linear",
            task_type="CAUSAL_LM",
        ),
        args=SFTConfig(
            output_dir=output_dir,
            num_train_epochs=epochs,
            max_steps=max_steps,
            learning_rate=learning_rate,
            lr_scheduler_type="cosine",
            warmup_ratio=0.03,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=8,
            gradient_checkpointing=True,
            bf16=True,
            max_length=max_length,
            completion_only_loss=True,
            logging_steps=1,
            save_strategy="no",
            report_to="none",
        ),
    )
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    Path(output_dir, "train_log.json").write_text(json.dumps(trainer.state.log_history, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, choices=sorted(KEY_TO_MODEL))
    parser.add_argument("--episodes", required=True)
    parser.add_argument("--cases", default="data/neurobench/cases")
    parser.add_argument("--output", required=True, help=f"EOS directory for the adapter and its log, e.g. {WEIGHTS_ROOT}/sft-<run>/<model>")
    parser.add_argument("--allow-candidates", action="store_true")
    parser.add_argument("--epochs", type=float, default=2.0)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--max-length", type=int, default=32768)
    parser.add_argument("--max-steps", type=int, default=-1, help="stop early; for smoke fits")
    args = parser.parse_args()
    train(
        model_key=args.model,
        episodes_path=args.episodes,
        cases_path=args.cases,
        output_dir=str(require_eos(args.output)),
        allow_candidates=args.allow_candidates,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        max_length=args.max_length,
        max_steps=args.max_steps,
    )


if __name__ == "__main__":
    main()
