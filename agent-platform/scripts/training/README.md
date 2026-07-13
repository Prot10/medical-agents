# Training Scripts

Trajectory generation and fine-tuning launchers for the v5 dataset
(600 cases in `data/neurobench/cases/`; 500 train / 100 test in
`data/neurobench/splits/`, produced by
`neuroagent.training.data.make_train_test_split`).

Current pipeline:

- `run_sft_training.sh` — QLoRA/bf16-LoRA SFT on the gold trajectories, train split only
  (`--splits-dir data/neurobench/splits`, 10% val carve-out, adapter to EOS).
- `run_rft.sh` — rejection-sampling fine-tuning: rollouts on the train split → keep
  verified-correct → SFT data (`build_rft_dataset.py`).
- `run_sft_eval.sh` / `run_definitive_eval.sh` — base-vs-SFT evaluation on the held-out
  test split (greedy + sampled + judge bundles + paired stats).
- `run_sft_eval_cases.py` — the eval/compare runner behind both; loads cases from
  `data/neurobench/cases/` via `data/neurobench/splits/{split}_cases.txt` and doubles as
  the RFT rollout generator (`--split train --rollout-jsonl`).
- `run_finetuning_comparison.sh` — thin orchestrator: precondition checks →
  `run_sft_training.sh` → `run_definitive_eval.sh`.
- `run_dpo_training.sh` — DPO from the SFT adapter: collect rollouts (train split) →
  build pairs → merge adapter → train.
- `batch_generate_trajectories.py` — gold-trajectory generation via the Anthropic API;
  reads/writes `$TRAINING_DATA_ROOT/gold_trajectories/{prompts,raw}` (override with
  `--prompts-dir` / `--output-dir`).

Needs update before use:
- `run_grpo_training.sh` and `run_dapo_training.sh` still point at the retired
  `sft_769/checkpoint-272` adapter and fold0-era GRPO data
  (`grpo_dataset/train_fold0.jsonl`); rebuild their inputs before running.
