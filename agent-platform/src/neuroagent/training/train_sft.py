"""LoRA SFT entry point for physician-approved typed episodes."""

from __future__ import annotations

import argparse

from ..model_registry import KEY_TO_MODEL
from .data.episodes import episode_to_messages, load_case_map, load_episode_records


def train(
    *,
    model_key: str,
    episodes_path: str,
    cases_path: str,
    output_dir: str,
    allow_candidates: bool = False,
    epochs: float = 2.0,
) -> None:
    if model_key not in KEY_TO_MODEL:
        raise ValueError(f"model must be one of {sorted(KEY_TO_MODEL)}")
    model_entry = KEY_TO_MODEL[model_key]
    codec = model_entry["adapter"]
    records = load_episode_records(episodes_path, allow_candidates=allow_candidates)
    cases = load_case_map(cases_path)
    missing = sorted({record.case_id for record in records} - cases.keys())
    if missing:
        raise ValueError(f"episodes reference missing cases: {missing[:10]}")

    try:
        from datasets import Dataset
        from peft import LoraConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from trl import SFTConfig, SFTTrainer
    except ImportError as exc:
        raise RuntimeError("install the 'training' optional dependencies to run SFT") from exc

    model_id = model_entry["hf_model_id"]
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    rows = []
    for record in records:
        messages = episode_to_messages(record, cases[record.case_id], codec=codec)
        rows.append(
            {
                "text": tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=False,
                )
            }
        )
    dataset = Dataset.from_list(rows)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype="auto",
        device_map="auto",
    )
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
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
            learning_rate=2e-5,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=16,
            logging_steps=5,
            save_strategy="epoch",
            dataset_text_field="text",
            report_to="none",
        ),
    )
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=sorted(KEY_TO_MODEL))
    parser.add_argument("--episodes", required=True)
    parser.add_argument("--cases", default="data/neurobench/cases")
    parser.add_argument("--output", required=True)
    parser.add_argument("--allow-candidates", action="store_true")
    parser.add_argument("--epochs", type=float, default=2.0)
    args = parser.parse_args()
    train(
        model_key=args.model,
        episodes_path=args.episodes,
        cases_path=args.cases,
        output_dir=args.output,
        allow_candidates=args.allow_candidates,
        epochs=args.epochs,
    )


if __name__ == "__main__":
    main()
