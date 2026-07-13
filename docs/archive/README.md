# Archive — historical records, not instructions

Everything under this directory is a **record of completed work**. It is kept because it
explains *why* specific cases were changed, and who flagged what. It is **not** a guide to
how the repo works today, and several documents here tell you to run scripts that no longer
exist.

**Do not follow any command in this directory.** If you want to validate or fix cases, the
one current entry point is:

```bash
uv run python agent-platform/scripts/validation/validate_cases.py
```

## What is here

| Path | What it records | Why it is stale |
| --- | --- | --- |
| `sweeps/COHERENCE_SWEEP_{SPEC,REPORT}.md` | The v5 coherence sweep (224 issues over 126 cases) | Runs `validate_ground_truth_coherence.py`, deleted in `c44993b`; paths point at `data/neurobench_v5/cases`, which no longer exists |
| `sweeps/REALISM_SWEEP_{SPEC,REPORT}.md`, `sweeps/PHASE3_REALISM_SPEC.md` | The tool-report realism sweep | Runs `detect_answer_leakage.py`, deleted in `c44993b` |
| `sweeps/CONSISTENCY_SWEEP_REPORT.md` | Cross-condition consistency findings | Written when the dataset had 516 cases; it now has 600 |
| `sweeps/CLINICIAN_REVIEW_FLAGS.md` | Open questions handed to clinician review | Its section 5 asks for a ruling on `consult_medical_specialist`; that tool was removed in `64d4091`, so the question is resolved by deletion |
| `sweeps/CASE_CONTRACT_SWEEP_SPEC.md` | The tool-contract sweep that took the cases to 0 validator issues | Uses the current validator, but the work is done |
| `dataset-generation/external_case_sources.md` | Why cases were seeded from PMC / CC-BY sources | Counts describe the 100-case v1 dataset |
| `audit/*.md` | Per-condition field-by-field audits of all 600 cases | Findings at audit time; some quote output from the deleted validators |
| `finetuning-plan.md` | The original Qwen3.5-9B fine-tuning plan and TODO tracker | Describes the earlier 769-trajectory / 200-case phase; superseded by `docs/training/distillation.md` and `docs/training/sft-recipe-hardware-and-evaluation.md` |
| `improvement-plan.md` | Post-v3-audit improvement plan (March 2026) | Predates the 600-case / 20-condition dataset and the tool-contract migration; several items it lists as open are done. Superseded by `docs/architecture.md` |

## What replaced them

The invariants these sweeps checked by hand are now enforced by code, on every commit:

- `agent-platform/scripts/validation/validate_cases.py` — one command, 0 issues on 600/600
- `agent-platform/scripts/validation/check_perfect_agent.py` — proves the ground truth is attainable
- `agent-platform/tests/test_case_tool_contract.py` — the pytest gate

See `docs/benchmark/tool-contract.md`.
