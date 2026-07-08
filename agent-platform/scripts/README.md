# Agent Platform Scripts

Scripts are grouped by operational purpose:

- `runtime/` — local/manual agent runs and model serving.
- `benchmark/` — benchmark execution, saved-trace scoring, judge batching, and rollups.
- `training/` — trajectory generation, fine-tuning launchers, and fine-tuned model evaluation.

Historical dataset migration and audit scripts were removed. The repo is moving toward one final dataset, so scripts that only existed to transform or compare old dataset versions should not come back here.
