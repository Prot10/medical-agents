# GRPO prompt datasets

`train_prompts.jsonl` and `test_prompts.jsonl` are **derived** artifacts: one rendered prompt per
case in the split, built from the cases, the split manifest, the hospital rules and the model's
chat template.

## Why the current files are suffixed `.stale-2026-08-05`

The August 2026 composition change — `peripheral_neuropathy` retired, `vascular_dementia` added
(see `docs/benchmark/tool-review-2026-07.md`) — left the 2026-08-05 build referencing **30 cases
that no longer exist** (28 in train, 2 in test) and missing the 30 new ones. A GRPO run reading
that file would train against prompts for deleted cases, which is worse than having no file, so
they are renamed rather than left in place under their operative names. They are kept, not deleted,
because they are the artifact every number published before that date was produced against.

`scripts/training/run_grpo_training.sh` defaults to `train_prompts.jsonl`, so it now fails to find
its input instead of silently using a broken one.

## Regenerating

Needs the training extra (`uv sync --all-packages --extra training`) and the tokenizer, because
the prompt is rendered through the model's chat template:

```bash
uv run python -m neuroagent.training.data.build_grpo_dataset \
  --split train --hospital de_charite --model Qwen/Qwen3.5-9B \
  --output data/neurobench/grpo/train_prompts.jsonl
uv run python -m neuroagent.training.data.build_grpo_dataset \
  --split test --hospital de_charite --model Qwen/Qwen3.5-9B \
  --output data/neurobench/grpo/test_prompts.jsonl
```

`agent-platform/tests/test_grpo_prompt_dataset.py` then checks that every prompt names a case that
exists and that the set matches the split exactly, so this cannot rot silently again.
