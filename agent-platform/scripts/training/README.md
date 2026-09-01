# Training

The maintained training surface is intentionally small:

- `python -m neuroagent.training.train_sft` runs LoRA SFT over typed episodes;
- `neuroagent.training.grpo.GRPOCoordinator` runs group-relative environment rollouts against a caller-provided `TrainablePolicyBackend`;
- `neuroagent.training.rollout.EnvironmentRollout` is shared with evaluation.

Bootstrap episodes are candidates, not gold. The loader rejects `candidate_not_gold` unless `--allow-candidates` is explicit. No DPO, DAPO, transcript-repair or hidden-reasoning pipeline is supported.
