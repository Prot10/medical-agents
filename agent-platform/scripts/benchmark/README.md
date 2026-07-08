# Benchmark Scripts

Benchmark execution and post-processing for the current dataset.

Keep:
- `run_baseline_eval.py`, `run_full_benchmark.py` — benchmark runners.
- `prepare_judge_batches.py`, `aggregate_judge_scores.py`, `final_rollup.py` — judge and reporting pipeline.
- `recompute_metrics.py`, `verify_metrics.py`, `evaluate_benchmark.py` — saved-trace scoring and diagnostics.
- `run_model_comparison.py` — quick local model comparison.

Needs update:
- `run_llm_judge.py` still documents/defaults to old v4 comparison paths. Update it to the current benchmark output layout or remove it if the batch judge pipeline is the only supported path.
- `run_baseline_eval.py` and `run_full_benchmark.py` overlap. Keep both only if they serve distinct experiment workflows.
