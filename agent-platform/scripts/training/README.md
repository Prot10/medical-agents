# Training

The maintained training surface is intentionally small:

- `python -m neuroagent.training.data.export_episodes` turns completed benchmark episodes into `candidate_not_gold` records;
- `python -m neuroagent.training.train_sft` runs LoRA SFT over typed episodes, one prompt/completion example per model turn, rendered by the same transcript codec the harness uses at inference and with loss on the action only;
- `python -m neuroagent.training.train_grpo` runs GRPO with verifiable policy rewards on one GPU: the benchmark loop as the rollout, a colocated vLLM engine, one masked sequence per episode, DAPO loss with token-level importance-sampling correction; every rollout is persisted for audit. Checkpoints and adapters go only to `--weights-dir` on EOS; `--output` holds logs and rollouts.

`scripts/training/eval_checkpoints.sh WEIGHTS_DIR CASES_FILE OUTPUT` scores every `checkpoint-*` of a GRPO run (and the base model) on held-out cases, on a second GPU while the run trains; started again, it scores only the checkpoints that landed since. Checkpoint selection reads validation cases, never the test split, which `train_grpo`, `train_sft` and `export_episodes` refuse. Every benchmark and GRPO run writes `manifest.json` with content hashes of its cases, policies, scorer and tool configuration (`evaluation/manifest.py`).

Bootstrap episodes are candidates, not gold. The loader rejects `candidate_not_gold` unless `--allow-candidates` is explicit, and only completed episodes are accepted. Serve a trained adapter with `LORA_ADAPTER=<dir> LORA_NAME=<alias> serve_model.sh <model>` and evaluate it through a profile whose model plugin sets `served_model: <alias>`.
