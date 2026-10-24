# Cross-condition work still to do (October 2026 round)

Kept by the orchestrating session so a resumed session does not lose it. Remove an item when it
lands.

## Code and tests
- Scorer: a mixed case can score both diagnoses only by recoding (it accepts a diagnosis on its
  ICD code alone). Consider a per-case "all of" diagnosis rule. (HEP-ENC-P04, 24 Oct)
- Test: catch fallback outputs that can never be served. (HEP-ENC, 24 Oct)
- Scorer: per-case rejected tokens, so a dementia case does not accept an MCI answer.
  (ALZ-EARLY, 24 Oct)
- Scorer: C71 codes the site, not the entity, so "glioblastoma, C71.1" still scores in an
  IDH-mutant astrocytoma through the code. Needs a per-case label requirement or ICD-O-3
  morphology codes; same root as the ICD-code-alone item above. (GLIO-HG, 24 Oct)
- MockServer: a case's fallback is returned for any `test_type` or modality, so generic case
  fallbacks answer studies they do not describe (GLIO-HG nulled them; check other conditions).
- `case_io.py check` reports "1 error" when torch is missing (test_grpo_rollout.py fails to
  collect); make it ignore that file.
- Scorer: negation matching, so "non-aneurysmal SAH" does not score in an aneurysmal case (and
  in general "non-X" / "not X" answers do not match X). (SAH, 24 Oct)
- Library: imaging variants a case does not store (e.g. CT perfusion) get normal defaults that may
  contradict the case. (SAH, 24 Oct)
- Harness: a drug discriminator for `check_drug_interactions` stored outputs. (ALZ-EARLY, 24 Oct)
- `perfect_agent.py`: a mode that tries every criterion alternative, not only the first.
  (ALZ-EARLY, 24 Oct)
- Library: normal amyloid PET, CSF AD-biomarker and FDG-PET defaults. (ALZ-EARLY, 24 Oct)
- PD cases: `[McKeith_2017_DLB]` should become `[DLB_2017]` (batch 5).
- `analyze_csf.source`: an EVD sample is billed as a lumbar puncture; only shunt/EVD criteria may
  name `source`. (vocabulary agent, 24 Oct)

## Schema
- Demographics lack `weight_kg` and `height_cm` (GBS respiratory mL/kg thresholds, BACT-MEN-RS04
  dosing). A fallback respiratory report with FVC (L, % predicted, mL/kg), MIP and MEP then needs
  the patient's weight. (GBS, 24 Oct)

## Prices to verify
- The October 2026 terms' Medicare rates were recalled, not looked up in the fee schedule; four
  have no CMS rate and are estimates (botulinum_toxin_assay, open_biopsy,
  DNA_methylation_profiling, and one more marked in costs.yaml). Check them against the 2024 MPFS
  / CLFS before any cost result is reported.

## Close-out recipe per batch (what batches 1 and 2 did)
1. Workflow `bin/round-v2.js` (plan, fix, verify, audit; args `[{cond, cases}]`). 2. One close-out agent per condition
(synonyms, pack, generator block, guidance claims via `build_condition_tool_guidance.py --write`
and the claim table, open questions decided; brief `CLOSEOUT_BRIEF.md` with COND replaced, the batch-2 decisions
files show the result) plus one vocabulary agent for the
batch's CENTRAL terms. 3. One agent per condition wires the new terms into the cases.

## Vocabulary follow-ups
- Other conditions citing "WHO 2025 Annex A.4" should read "section A.4" (the guideline has no
  Annex A.4).

## Synonym prune effects on later batches
- (MIG-AURA-P03 and P07 done 24 Oct: P03 recoded G43.609 with migrainous-infarction labels only,
  P07 cardioembolic labels only, I63 category excepted; plans/MIG-AURA-decisions.md.)
- `apply_diagnosis_synonyms --prune` would change SE-P04 (lose "stroke"
  and mechanism labels) and SE-P07 (loses "hepatic coma", K72.91); `--check` adds I63.5/I63.51 to
  SE-P04. Apply when those conditions run.

## For the physicians at re-review
- ISCH-STR-RS02: thrombolysis reversed to "give" (its CTA excludes aortic extension, R2's own
  condition for withholding). Tell R2.
- ISCH-STR-S06 was never physician-reviewed.
- AHA/ASA 2026 contraindication table is paywalled: confirm the class of prior ischaemic stroke
  within 3 months (ISCH-STR-RM01) and aPTT > 40 s without anticoagulant (ISCH-STR-RP04).
- Scoring changes: ALS-P08 rejects a plain "ALS" (Z15.89), ALS-P02 credits Graves, HEP-ENC-P04
  coded as Wilson disease.
- Never physician-reviewed and now changed by the round: VASC-DEM, NMDAR-ENC, MIG-AURA (and the
  batch-4/5 conditions). Schedule them into the next review round (Andrea). Point the reviewers at
  the scoring changes in each `plans/<COND>-decisions.md`.
- VASC-DEM: the 2026 ACC/AHA dyslipidemia goal (LDL < 55 mg/dL at very high risk) was read from
  summaries; confirm with the full text whether lacunar and cardioembolic strokes count as major
  ASCVD events (more cases would move to < 55).
- SE: tell R2 about the recodes and that P04 and P06 now need the seizure component for credit.

## Guard failures left in later batches (24 Oct)
- Leak guard: VASC-DEM 30, NMDAR-ENC 18, MIG-AURA 0 (clean 24 Oct), SE 10, SYNC-CARD 10, NPH 9, FTD 6, MG 6,
  FND 5, MS-RR 4, FEPI-TEMP 3, PD 2. Follow-up guard: FTD 1. (Batches 1-2 are clean.)
  Workers see the rule in PATTERNS.md section 5.
