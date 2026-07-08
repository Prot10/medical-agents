# Training Scripts

Trajectory generation and fine-tuning launchers.

Keep only if fine-tuning remains an active repo concern.

Needs update before use:
- Several launchers still reference `data/neurobench_v4` or v4 split files while the repo is moving toward one final dataset.
- `run_sft_eval_cases.py` is hardcoded to `data/neurobench_v4`.
- `run_finetuning_comparison.sh`, `run_dpo_training.sh`, and `run_sft_training.sh` need final-dataset paths and split handling.
- `batch_generate_trajectories.py` still writes to `raw_v2`; rename that output path if the trajectory workflow is kept.
