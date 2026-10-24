# Cross-condition work still to do (October 2026 round)

Kept by the orchestrating session so a resumed session does not lose it. Remove an item when it
lands.

## Rulings for the batch-5 close-out
- FND (Andrea, 24 Oct 2026, from the August 2026 exchange with Flavia Pennisi and Antonio: their
  email in `docs/benchmark/tool-review-2026-07.md` "Dataset composition changes requested", our
  reply section 2 in `tool-review-2026-07-reply-draft.md` and 1.7 in `tool-review-2026-07-decisioni.md`).
  FND stays (20 conditions, 600 cases; DLB is deferred as a future same-size swap). The
  physicians kept FND only with every diagnostic tool optional, and we replied that the exam of
  positive functional signs is the only required diagnostic act and that all instrumental work,
  video-EEG in paroxysmal cases included, is optional. The batch-5 plan broke that: on master FND
  requires only `perform_clinical_assessment` (30/30); after the workflow it also requires
  `analyze_eeg` in 22 cases, `analyze_brain_mri` in M09 and P08, `interpret_labs` in P08 and RM01.
  Close-out: video-EEG back to `optional` in those 22 cases; the red-flag tests (P08 glucose and
  imaging, RM01 sodium, M09 MRI on natalizumab) to `recommended` (the tier the reply already used for
  the 7 MRI cases); keep the exam required. `check_drug_interactions` (required in M02, RM03,
  RP01, RP03, RS01, RS02, S03) is a management act, not a diagnostic one: it may stay required, but
  list it for the physicians. Fix the impressions that say video-EEG "is required in this case"
  (M04, M06, RP01), the sequence constraints and `required_before_assessment` that name those
  tests, the pack and the guidance claims to match.

## Code and tests
- Scorer: a mixed case can score both diagnoses only by recoding (it accepts a diagnosis on its
  ICD code alone). Consider a per-case "all of" diagnosis rule. (HEP-ENC-P04, 24 Oct)
- Test: catch fallback outputs that can never be served. (HEP-ENC, 24 Oct)
- Scorer: per-case rejected tokens, so a dementia case does not accept an MCI answer.
  (ALZ-EARLY, 24 Oct)
- Scorer: C71 codes the site, not the entity, so "glioblastoma, C71.1" still scores in an
  IDH-mutant astrocytoma through the code. Needs a per-case label requirement or ICD-O-3
  morphology codes; same root as the ICD-code-alone item above. (GLIO-HG, 24 Oct)
- Discriminator data (24 Oct): the 12 closed conditions are fixed and guarded
  (`test_case_guards.py::test_routed_outputs_name_their_study`, `DISCRIMINATOR_CONDITIONS`). Left,
  per condition (cases / outputs): FEPI-TEMP 29/33, FND 30/84, MS-RR 30/30, PD 30/30 (SYNC-CARD,
  FTD, MG and NPH are now in `DISCRIMINATOR_CONDITIONS`); mostly untyped `TTE` echo fallbacks and generic
  advanced-imaging and specialized-test fallbacks (null them). Each worker adds its condition to
  `DISCRIMINATOR_CONDITIONS` when clean.
- Library: nulling generic fallbacks exposes library normals that some cases contradict, e.g. a
  normal `neuropsych_battery` in overt hepatic encephalopathy (HEP-ENC, West Haven II-III). Same root
  as the SAH library item below.
- MIG-AURA-P07 keeps its short-recording follow-up: its loop-recorder report stores
  `duration_hours` 720 (the weeks tier), so without it a 14-day monitor order would receive the
  day-17 AF.
- MockServer: prose `test_type` follow-ups in a tool with no initial output are served for any
  test type (MG-RS15's `Neostigmine challenge` answers an `emg_ncs` or audiometry order). Write
  the vocabulary term in stored `test_type`.
- Schema: `EEGReport` has no `eeg_type`, so a follow-up trigger that repeats the index study's
  term (`request_continuous_eeg_monitoring` with a `continuous_icu` index) can still capture the
  index order. The SE generator must not emit such triggers, or add `eeg_type` as for echo.
- Scorer: negation matching, so "non-aneurysmal SAH" does not score in an aneurysmal case (and
  in general "non-X" / "not X" answers do not match X). (SAH, 24 Oct)
- Library: imaging variants a case does not store (e.g. CT perfusion) get normal defaults that may
  contradict the case. (SAH, 24 Oct)
- Harness: a drug discriminator for `check_drug_interactions` stored outputs. (ALZ-EARLY, 24 Oct)
- `perfect_agent.py`: a mode that tries every criterion alternative, not only the first.
  (ALZ-EARLY, 24 Oct)
- Library: normal amyloid PET, CSF AD-biomarker and FDG-PET defaults. (ALZ-EARLY, 24 Oct)
- PD cases: `[McKeith_2017_DLB]` should become `[DLB_2017]` (batch 5).
- `analyze_csf.source`: an EVD sample is billed as a lumbar puncture (a lumbar drain is billed on
  top, 184); only shunt-tap, EVD and lumbar-drain criteria may name `source`. (vocabulary agents,
  24 Oct)
- Library (batch 4, 24 Oct): the new terms' normal reports can contradict a case that does not
  store them: a normal electrophysiology study (normal AV conduction, nothing inducible), a normal
  orthostatic test, normal arrhythmia and cardiomyopathy gene panels, a normal whole-body PET.
  SYNC-CARD stores a report or a "not performed" answer wherever the normal would contradict;
  other conditions do not (e.g. a dysautonomia case outside SYNC-CARD ordering
  `orthostatic_blood_pressure`).
- NPH timing (24 Oct): an agent that orders the `post_intervention` gait before the tap still
  receives the stored post-tap report; the soft sequence constraint (tap before reassessment)
  penalises the order but does not hide the result. Consider serving the post-intervention report
  only after the intervention's own criterion has been called.

## Schema
- Demographics lack `weight_kg` and `height_cm` (GBS respiratory mL/kg thresholds, BACT-MEN-RS04
  dosing). A fallback respiratory report with FVC (L, % predicted, mL/kg), MIP and MEP then needs
  the patient's weight. (GBS, 24 Oct)

## Prices to verify
- The October 2026 terms' Medicare rates were recalled, not looked up in the fee schedule; four
  have no CMS rate and are estimates (botulinum_toxin_assay, open_biopsy,
  DNA_methylation_profiling, and one more marked in costs.yaml). Check them against the 2024 MPFS
  / CLFS before any cost result is reported.
- Batch 3 (24 Oct, recalled): plasma_cholinesterase 9 (82480), RBC_cholinesterase 18 (82482),
  NSE 23 (86316), toxoplasma_IgG 18 (86777), urine_sodium 7 (84300), CSF toxoplasma_PCR and
  EBV_PCR 184 (87798), device_interrogation 51 (93288); genetic_panel:hemiplegic_migraine 1104
  is an estimate (81479, unlisted).
- Batch 4 (24 Oct, recalled): interpret_labs CDT 21 (82373); analyze_csf source lumbar_drain 184
  (62272); whole_body_FDG_PET 1840 (78815, priced as the brain study);
  genetic_panel:inherited_arrhythmia 1840 (81413), genetic_panel:cardiomyopathy 1840 (81439);
  tracheal_aspirate 18 (87070 + 87205, priced as sputum). Estimates: electrophysiology_study 2300
  (93620, professional + facility), sodium_channel_blocker_challenge 368 (no CPT, priced as
  autonomic testing), orthostatic_blood_pressure 23 (no CPT; part of an E/M visit).

## Batch-3 cases waiting on data (terms and routing landed 24 Oct)
- Stored monitoring reports with a prose `monitor_type` (routed on `duration_hours` only): none
  left in NPH and SYNC-CARD (both pass the discriminator guard since their close-outs). (SE, VASC-DEM-P08, MIG-AURA and GBS wired 24 Oct; see their logs.)
- Citation keys used by name in the wiring: Di Stefano 2020 (JNNP, hemiplegic migraine genetics)
  for the MIG-AURA pack; the NIH/CDC/IDSA opportunistic-infection guideline for SE (SE-M08).

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
- Leak guard (recounted 24 Oct, after the batch-4 vocabulary wiring): FEPI-TEMP 3 (P02, P03,
  RP05); every other condition passes at that moment (batch 5 is editing FND, MS-RR, FEPI-TEMP
  and PD). `test_guidance_claims` then failed only on FND, MS-RR and PD claims (batch 5). Follow-up guard: clean.
  Workers see the rule in PATTERNS.md section 5.
