# Benchmark Scripts

Benchmark execution and post-processing for the current dataset.

Keep:
- `run_baseline_eval.py`, `run_full_benchmark.py` — benchmark runners.
- `prepare_judge_batches.py`, `aggregate_judge_scores.py`, `final_rollup.py` — judge and reporting pipeline.
- `recompute_metrics.py`, `verify_metrics.py`, `evaluate_benchmark.py` — saved-trace scoring and diagnostics.
- `run_model_comparison.py` — quick local model comparison.

Legacy:
- `run_llm_judge.py` — vLLM-based judge for saved `run_model_comparison.py` outputs
  (`merged_results.json` + per-model `traces.json`); `--results-dir` is required, no
  stale defaults. For `results/baseline_eval_*` runs use the batch pipeline above
  (`prepare_judge_batches.py` → llm-judge agents → `aggregate_judge_scores.py`).

Needs update:
- `run_baseline_eval.py` and `run_full_benchmark.py` overlap. Keep both only if they serve distinct experiment workflows.
