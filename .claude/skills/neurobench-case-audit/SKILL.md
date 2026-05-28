---
name: neurobench-case-audit
description: Exhaustively validate NeuroBench benchmark cases field-by-field — schema, internal consistency, clinical correctness, and answer-leakage realism. Use when auditing or QA-ing the v5 dataset (e.g. before clinician validation or a model run), or when the user asks to "read and validate every line/word" of cases. Reads every field of a case against its condition criteria pack and the tool-report style guide; fixes only unambiguous mechanical errors and flags everything that needs judgment.
---

# NeuroBench Case Audit

Exhaustively validate NeuroBench v5 cases (`data/neurobench_v5/cases/{CASE}.json`),
reading **every field, value, and sentence** of each assigned case. Produce a
trustworthy audit: fix only objectively-wrong mechanical errors, flag everything
requiring judgment, and never silently change clinical meaning.

## Non-negotiable

1. **Read the whole case.** Open the full JSON and read every field — patient,
   exam, every tool output (initial, followup, fallback), and the entire
   `ground_truth`. Do not validate from the detector/validator output alone; those
   are necessary, not sufficient.
2. **Ground every judgment in evidence**, not training-data assumptions: the case's
   own data + the condition's criteria pack + the style guide. If you assert a lab
   value is wrong, name the correct reference range and source.
3. **Conservative fixing.** This is an audit, not a rewrite. The dataset has already
   been swept; over-eager edits have caused regressions before. When in doubt, FLAG,
   don't fix. NEVER change the diagnosis, the patient's clinical story, or any
   `ground_truth` meaning as a "fix" — flag it.

## Reference documents (read the ones relevant to your case)

- Clinical correctness: `dataset-generation/criteria_packs/{CONDITION}.md` — diagnostic
  criteria, required/recommended/optional workup, useless & harmful tools, sequence
  constraints, citation allow-list, subtype variations.
- Report realism: `dataset-generation/TOOL_REPORT_STYLE_GUIDE.md` (authority).
- Tool params: `dataset-generation/TOOL_PARAMETER_VOCABULARY.md`.
- Gold-trajectory rules: `dataset-generation/GOLD_TRAJECTORY_AUTHORING_GUIDE.md`.
- Schema: `packages/neuroagent-schemas/src/neuroagent_schemas/` (case.py, tool_outputs.py, evaluation.py, enums.py).

## Step 1 — run the mechanical validators for your condition

```bash
uv run python agent-platform/scripts/validate_ground_truth_coherence.py --case {CASE}.json   # must be 0
uv run python agent-platform/scripts/detect_answer_leakage.py --case {CASE}.json              # candidates; judge each
uv run python agent-platform/scripts/validate_tool_vocab.py            # whole-dataset; note your cases
uv run python -c "from pathlib import Path; from neuroagent_schemas import NeuroBenchCase; NeuroBenchCase.model_validate_json(Path('data/neurobench_v5/cases/{CASE}.json').read_text())"
```

## Step 2 — read every field against the five dimensions

Walk the case region by region. For each, check all five dimensions:

**Regions:** `case_id`/`condition`/`difficulty`/`encounter_type` → `patient` (demographics,
history, meds, vitals) → `neurological_exam` (each subfield) → `initial_tool_outputs`
(every modality: values AND interpretive text) → `followup_outputs` (each: trigger,
tool, output) → `fallback_tool_outputs` → `ground_truth` (primary_diagnosis, icd_code,
differential, optimal_actions, useless_tools, harmful_tools, sequence_constraints,
critical_actions, contraindicated_actions, red_herrings, key_reasoning_points, citations).

**Dimension A — Schema & format.** Validates against `NeuroBenchCase`; required fields
present; enums valid (likelihood, category, severity, condition, difficulty); JSON
well-formed; each file's unicode convention (escaped vs literal) and trailing newline
preserved on any write.

**Dimension B — Internal consistency (cross-field & numeric).**
- `case_id` prefix matches `condition` enum (flag intentional mimics, don't "fix").
- Patient age/sex used consistently across HPI, exam, and every report.
- Every lab `is_abnormal=true` value is actually outside its stated `reference_range`,
  and vice-versa; units present and correct; values physiologically plausible.
- A report's `impression` is consistent with its own `findings` (no impression
  asserting something the findings contradict).
- Numbers referenced in `ground_truth.key_reasoning_points` match the tool outputs.
- `followup_outputs[].trigger_action`/`tool_name` reference real tools; outputs exist
  for required tools; useless tools have fallbacks (coherence validator covers this).
- `differential` sorted by likelihood descending; likelihoods are valid enum values.
- `tool_parameters` are in the closed vocabulary.

**Dimension C — Clinical correctness (vs the criteria pack).**
- The presentation (HPI + exam + test results) genuinely supports the
  `primary_diagnosis`; the gold answer is the best explanation of the data.
- Each test result is clinically plausible for the diagnosis and in a realistic range
  (e.g. bacterial-meningitis CSF: neutrophilic pleocytosis, low glucose, high protein).
- `optimal_actions` tiers (required/recommended/optional) match the criteria pack's
  workup hierarchy; `useless_tools`/`harmful_tools` match; sequence constraints are
  clinically sound; `critical_actions`/`contraindicated_actions` are correct.
- Citations exist in the pack's allow-list and are used appropriately (right guideline
  for the claim). `difficulty` is plausible for the case's subtlety.
- Reference ranges are correct for each analyte.

**Dimension D — Realism / answer-leakage (vs the style guide).**
- **Kind 1 (must be absent):** cross-modality synthesis, differential-refutation
  essays, or management prescription in a tool report; a non-confirmatory modality
  announcing the integrated diagnosis. Flag (or fix if unambiguous) any residual.
- **Kind 2 (KEPT — do NOT strip):** a report naming a diagnosis its own modality
  legitimately establishes (MRI "acute MCA infarct"; CT "subarachnoid hemorrhage";
  EMG "consistent with a motor neuron disease"; neuropsych "probable bvFTD"; per-modality
  limits in the guide — amyloid PET/DaTscan binary, FDG-PET metabolic pattern, EEG never
  "epilepsy", routine labs no narrative). Confirmatory results (CSF organism, genetics,
  antibody titers, biopsy histology) are KEPT.

**Dimension E — Language & quality.** No typos, grammar errors, placeholder/TODO text,
duplicated sentences, or inconsistent terminology/units.

## Step 3 — fix policy

**FIX inline (unambiguous, mechanical):** typos/grammar; wrong/missing units; a
reference range that contradicts the `is_abnormal` flag where the correct value is
unambiguous; internal numeric contradictions where the correct value is clear from
context; differential ordering; format/schema; clear residual Kind-1 leakage. Log every
fix.

**FLAG, do NOT fix (judgment / meaning):** any doubt about the diagnosis or whether the
data supports it; tier reclassification; adding/removing tools; changes to
`ground_truth` semantics; clinical plausibility concerns; mimic mis-prefixing; anything
where a reasonable clinician could disagree. Record in the report; if the case body has
a contradiction, also note it in `metadata.case_body_concerns` (append, don't overwrite).

**Never:** change `primary_diagnosis`; alter the patient's clinical story or exam to
"make it fit"; strip Kind-2 within-modality conclusions; touch another condition's files.

## Step 4 — write the audit report

Append findings to `data/review/audit/{CONDITION}.md`, one row per finding:

```
| case_id | dim (A–E) | severity (blocker/major/minor/nit) | region.field path | finding | action (FIXED/FLAGGED) | detail |
```

End the file with a tally: cases audited, findings by severity, # fixed vs flagged.

## Step 5 — self-verify (required)

For every case you fixed: re-run the coherence validator (must stay 0) and schema
validation (must pass). Confirm you touched only your condition's files and preserved
unicode convention. The detector may legitimately still flag confirmatory results /
general literature / Kind-2 naming — note those as intentional, do not chase to zero.

## Report back

Cases audited; total findings by severity; count fixed vs flagged; the top
clinical-correctness flags a human must adjudicate; confirmation that coherence + schema
stayed green and only your condition's files changed.
