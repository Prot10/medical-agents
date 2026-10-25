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
- Library: nulling generic fallbacks exposes library normals that some cases contradict, e.g. a
  normal `neuropsych_battery` in overt hepatic encephalopathy (HEP-ENC, West Haven II-III). Same root
  as the SAH library item below.
- MIG-AURA-P07 keeps its short-recording follow-up: its loop-recorder report stores
  `duration_hours` 720 (the weeks tier), so without it a 14-day monitor order would receive the
  day-17 AF.
- MockServer: prose `test_type` follow-ups in a tool with no initial output are served for any
  test type (MG-RS15's `Neostigmine challenge` answers an `emg_ncs` or audiometry order). Write
  the vocabulary term in stored `test_type`.
- MRI contrast (24 Oct): `contrast` defaults to false and `MRIReport.contrast_used` exists, but
  only ALZ-EARLY-RS06 states it. 575 cases store one MRI study, about 260 of them a contrast study
  by their text, so a non-contrast order receives post-gadolinium findings. Routing needs a
  non-contrast variant (or a "not performed" answer) per case where the criteria allow a plain
  study, then `contrast_used` on every stored MRI and a guard.
- Scorer: negation matching, so "non-aneurysmal SAH" does not score in an aneurysmal case (and
  in general "non-X" / "not X" answers do not match X). (SAH, 24 Oct)
- Library: imaging variants a case does not store (e.g. CT perfusion) get normal defaults that may
  contradict the case. (SAH, 24 Oct)
- Harness: a drug discriminator for `check_drug_interactions` stored outputs. (ALZ-EARLY, 24 Oct)
- `perfect_agent.py`: a mode that tries every criterion alternative, not only the first.
  (ALZ-EARLY, 24 Oct)
- Library: normal amyloid PET, CSF AD-biomarker and FDG-PET defaults. (ALZ-EARLY, 24 Oct)
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
- Library: MIG-AURA-RM11's video-EEG alternative may still receive a library normal (the case
  stores a routine EEG and an untyped fallback). SE now stores a case-specific routine EEG and a
  guard requires one wherever a continuous EEG is stored (25 Oct).
- Lab matcher (25 Oct, `plans/SE-routing-decisions.md` CENTRAL): interpretation prose is filtered
  by sentence, so a one-sentence "Abnormal values: ..." still reads out values of panels the order
  did not name (SE M02, M03, M05-M07, P03, S01, S07, S09); orders are answered panel by panel, so
  an added assay returns its whole stored panel (SE RS11, S05, S10); a stored blood gas answers a
  `CMP` order through `HCO3`. Filter by clause or split the panels.
- Lab evidence (25 Oct): the 143 criteria whose evidence cited abnormal results their order did
  not return are fixed (`plans/LABS-EVIDENCE-decisions.md`, `plans/SE-routing-decisions.md`).
  About 99 more cite normal results their order does not return (ALS 25, MS-RR 18, ...):
  `notes/labs-evidence-normal-unserved-2026-10-25.txt`. Consistency only; the reward does not
  read the evidence.

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
- Batch 5 (25 Oct, recalled): interpret_labs cysticercosis_serology 15 (86682), IGRA 71 (86480).
  Estimates: olfactory_test 46 (no CPT; unlisted 92700), levodopa_challenge 184 (no CPT; priced
  as two scored motor examinations). Methylmalonic acid was already priced as `MMA` 28 (83921).
  `HBV_DNA` 43 (87517), 25 Oct, recalled.

## Close-out recipe per batch (what batches 1 and 2 did)
1. Workflow `bin/round-v2.js` (plan, fix, verify, audit; args `[{cond, cases}]`). 2. One close-out agent per condition
(synonyms, pack, generator block, guidance claims via `build_condition_tool_guidance.py --write`
and the claim table, open questions decided; brief `CLOSEOUT_BRIEF.md` with COND replaced, the batch-2 decisions
files show the result) plus one vocabulary agent for the
batch's CENTRAL terms. 3. One agent per condition wires the new terms into the cases.

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

- Scoring changes of 25 Oct: ALS-M07 requires `blood_lead` and ISCH-STR-RM02 `ESR` and `CRP` in
  every alternative; SE-P01, S05 (thiamine, S05 also phosphate), P05, RS11, S06, S10 (CK), P08
  (serum osmolality) require the added assay; PD-RP04 requires a levodopa challenge; new
  recommended criteria FEPI-TEMP-RS02 (cysticercosis serology, IGRA) and HEP-ENC-S05 (HBV DNA);
  new optional MS-RR-RS06 MMA and the olfactory test in 12 PD cases. 22 approved or probably
  approved cases had lab criteria changed (`plans/LABS-EVIDENCE-decisions.md`).
- FND: instrumental tests are optional per the August 2026 ruling; `check_drug_interactions`
  stays required in M02, RM03, RP01, RP03, RS01, RS02, S03 (a management act): confirm.
