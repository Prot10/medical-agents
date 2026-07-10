# Agent Platform Scripts

Scripts are grouped by operational purpose:

- `runtime/` — local/manual agent runs and model serving.
- `benchmark/` — benchmark execution, saved-trace scoring, judge batching, and rollups.
- `training/` — trajectory generation, fine-tuning launchers, and fine-tuned model evaluation.
- `validation/` — the benchmark's correctness gates.

## `validation/`

| Script | Purpose |
| --- | --- |
| `validate_cases.py` | The one command that defines a correct case. Must report 0 issues on 600/600. `--json` writes a manifest with a `fix_class` per issue |
| `migrate_cases.py` | Applies the deterministic repairs (key renames, removed tools, the CSF basic/special split). `--dry-run` first |
| `check_perfect_agent.py` | Proves the ground truth is attainable: an agent doing exactly what a case says must score 1.0 recall, 1.0 required coverage, 0 useless, 0 harmful |
| `check_sweep_guard.py` | Run after any batch edit of the cases: asserts no case gained issues and that diagnosis / ICD / condition never changed |
| `case_sweep_workflow.js` | Fans one clinician subagent per condition over the issues that need judgment |

The invariants they enforce are documented in
[`docs/benchmark/tool-contract.md`](../../docs/benchmark/tool-contract.md) and gated by
`agent-platform/tests/test_case_tool_contract.py`.

Historical dataset migration and audit scripts were removed. The repo is moving toward one
final dataset, so scripts that only existed to transform or compare old dataset versions
should not come back here.
