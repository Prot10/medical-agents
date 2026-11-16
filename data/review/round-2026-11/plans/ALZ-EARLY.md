# ALZ-EARLY: lead plan for the November 2026 round

Lead plan for the 30 ALZ-EARLY cases. Workers read ROUND_POLICY.md (October, still in force),
work/NOVEMBER_ADDENDUM.md, and `ALZ-EARLY-decisions.md` next to this file (numbered decisions D1-D16
with reasons and sources). Helpers live in `data/review/round-2026-11/bin/` (case_io.py,
perfect_agent.py, caselog.py, mri_probe.py). Run Python as `uv run python -I` from the repository
root.

- Notes: 85, all R1, in 19 cases. 11 cases have no notes (M01-M05, P01-P04, RM01, RM02), but every
  class below still applies to them.
- Approved cases (work/approved.txt): none in ALZ-EARLY.
- Base state measured 16 Nov 2026:
  - No literature criterion or output is left in any ALZ case (class LIT, commit 393c547e).
  - RS06 is the only ALZ case with an MRI pair (class MRI-CONTRAST).
  - Every case has `max_additional_actions` 1.
  - Scripts: /home/aprotani/review-round-2026-11/work/scratch/alz-lead/ (overview_alz.py,
    compact_alz.py, np_flags.py, np_print.py, lab_sig.py, uncredited_fu.py, readcase.py).
- Cases read in full: RM03, RP04, RS06, S06; also S02 (history), RM04 (battery and musts), and the
  neuropsych battery of all 19 noted cases.

## 1. Governing guidelines and canonical facts

| question | source | key |
| --- | --- | --- |
| Staging, MCI vs dementia, labels | McKhann 2011, Albert 2011 (October Q1, unchanged) | `[NIA_AA_2011]` `[NIA_AA_MCI_2011]` |
| When a further subtype test is used; FDG-PET or CSF; the other only if the first is not diagnostic; SPECT only if FDG-PET is unavailable; FDG/SPECT for suspected FTD | NICE NG97 recs 1.2.14, 1.2.15, 1.2.23 (verified 16 Nov 2026) | `[NICE_NG97]` |
| Amyloid PET vs CSF; tau PET has appropriate scenarios (under 65, treatment eligibility) | Rabinovici 2025 AUC | `[Appropriate_Use_Amyloid_PET]` |
| Anti-amyloid antibodies licensed for MCI or mild dementia due to AD with confirmed amyloid (FDA 2023/2024; EC lecanemab 15 Apr 2025, donanemab 24 Sep 2025; ApoE e4 non-carriers or heterozygotes in the EU); eligibility MMSE 22-30 | regulatory decisions; Cummings 2023 AUR | `[Lecanemab_AUR_2023]` |
| MCI: no routine cholinesterase inhibitor or memantine | Petersen 2018 | `[AAN_dementia_2018]` |
| A1C target below 8.0% with mild to moderate cognitive impairment (MCI included) | ADA Older adults 2026, Table 13.2 | `[ADA_older_adults_2026]` |
| Incidental meningioma: MRI diagnosis, observation first | Goldbrunner 2021 EANO, Neuro Oncol 23:1821 | `[EANO_meningioma_2021]` (new key, CENTRAL C5) |
| Cognitive deficits can persist after depressive remission | Bora 2013, Psychol Med 43:2017 | (decision record only) |

Canonical facts:
- One amyloid test is enough. A second test is uncredited, and with the new stop rule (0) it is
  penalised.
- FDG-PET is a conditional subtype test. Perfusion SPECT is never needed when FDG-PET is orderable.
- Tau PET is neither credited nor labelled.
- An action that matches a criterion never counts against the stop rule (`policy_reward.py`,
  stopping).
- A stored report is an answer served on request; it does not mean the study was performed.
- The review app prints `abnormal` above `test` and prints null as "none".

## 2. Classes

### C1. NP-FLAG-DISPLAY: neuropsych flags read one row off (43 notes, 17 cases) -> CENTRAL, no case change
Each note's named row already carries the flag asked for. Every row was checked by script and by eye
(np_print.py). In RP03 and S06, "overall abnormal = no" is the MMSE row, which is correct.
Dataset-wide: 1458 rows have a range and a flag, and the only real error is C2; the other 14 hits
are parser artifacts. Ruling for every note: CENTRAL (CENTRAL.md item 2). The log states the row
checked, its value, range and flag, and that the data is right.

### C2. NP-FLAG-REAL: S06 TMT-B (c23ae468) -> FIXED
- `followup_outputs[<neuropsych>].output.findings[<Trail Making Test Part B>].abnormal` changes "no" -> "yes".
- In the impression, replace "Processing speed, executive function, and visuoconstructive ability
  are within the low-normal range." with: "Processing speed (Trail Making A, 38th percentile) and
  visuoconstructive ability (Rey Complex Figure copy, 42nd percentile) are within the reference
  range; set-shifting (Trail Making B, 24th percentile) is just below it."
- Label and staging are unchanged (D2).

### C3. BIOMARKER-PATHWAY: amyloid redundancy, FDG, SPECT, stop rule, pathway order (28 notes in RM03, RM04, RP01-RP05) -> FIXED (D3-D8), all 30 cases
1. Amyloid criterion: unchanged (one optional criterion, CSF or amyloid PET; RP04 CSF required).
   Do not add an avoided action on amyloid PET where it is a criterion alternative. RP04 only gets
   `avoid-waste-<n>-order-advanced-imaging-amyloid-pet` (waste, `{"modality": "amyloid_PET"}`) with
   the D4 rationale.
2. FDG criteria:
   - Delete `action-9-order-advanced-imaging` in P01; `action-10-order-advanced-imaging` in P02,
     RP01 and RP02; `action-9-order-advanced-imaging` in RM04 and RP03 (RP03 with its SPECT
     alternative). Check the ids in the file.
   - Before deleting, confirm that no sequence constraint or stop rule names the deleted id (none
     did at base).
   - Keep P03's FDG criterion.
3. FDG waste avoided action (new id `avoid-waste-<n>-order-advanced-imaging-fdg-pet`, severity
   waste, `{"modality": "FDG_PET"}`, citation `[NICE_NG97]`):
   - Cases: M02, M04, M05, P04, RM01, RM02, RM03, RM04, RP04, RP05, RS01-RS06, S01-S06 (22).
   - Rationale: "In this amnestic presentation with supportive MRI, amyloid status (CSF or amyloid
     PET) is the confirmatory test; FDG-PET would not change the diagnosis or management."
   - Additions: RP05 "; a Lewy body question is answered by the DaTscan." RP04 "; the prion question
     is answered by DWI and CSF RT-QuIC" (add `[CJD_2021]`).
   - In the MCI cases (M02, M04, RM04) write "amnestic mild cognitive impairment with supportive
     MRI".
   - No FDG label in M01, M03, P01, P02, P03, RP01, RP02, RP03.
4. SPECT waste avoided action in all 30 cases:
   - New id `avoid-waste-<n>-order-advanced-imaging-perfusion-spect`, waste,
     `{"modality": "perfusion_SPECT"}`, `[NICE_NG97]`.
   - Rationale: "Perfusion SPECT substitutes for FDG-PET only where FDG-PET is unavailable; it adds
     nothing to this work-up."
5. Tau PET: no change.
6. `ground_truth.stop_rule.max_additional_actions`: 1 -> 0 in all 30; `required_before_assessment`
   unchanged.
7. `followup_outputs` order:
   - (a) the follow-ups that answer a criterion's first alternative, in criterion order;
   - (b) the second-alternative amyloid counterpart (amyloid PET in CSF-first cases, the CSF
     follow-up where CSF is second);
   - (c) on-request answers: FDG (except P03), tau PET, SPECT, speech-language (except P02),
     performance status, gait (except RM02), RP03 visual fields, RP01/RS04 abdominal ultrasound,
     RP04 amyloid PET.
   - Do not delete any stored report. Keep `action_criteria` in clinical order: core four, MMA, the
     case-specific criteria, amyloid, P03 FDG, EEG/DaTscan, genetics, drug check, ECG.
8. Log wording for each "Remove" / "redundant" / "should not be routine" note: "FIXED: removed from
   the scored pathway (criterion deleted / not credited / waste label as applicable), and the
   stop-rule allowance is 0, so a redundant order is penalised. The stored report stays as the
   answer to an order of that study (October Q3/Q4: otherwise the library's normal result would
   contradict the case) and now follows the credited steps. CENTRAL C1 asks the review app to show
   it as 'served if ordered'."
9. Stop-rule notes: FIXED (max 0). The log records the clarification R1 asked for: actions that
   match a criterion (drug check, ECG, MMA, DaTscan, EEG, genetics, the first amyloid test) never
   count; only uncredited actions after the required set count. StopRule has no prose field
   (CENTRAL C3).

### C4. LAB-SIGNIFICANCE: abnormal rows null, shown as "none" (6 notes: RM03, RM04, RP01, RS01, RP05, RS05) -> FIXED + CENTRAL display, all 30
Fill `clinical_significance` on these abnormal rows (initial labs and lab follow-ups). Choose the text
by the patient's history:
- HbA1c with known diabetes: "Above the non-diabetic reference range; reflects average glycaemia
  over the previous 2 to 3 months and is a modifiable vascular risk factor."
- HbA1c 5.7-6.4% without diabetes: "In the prediabetes range (5.7 to 6.4%); a modifiable vascular
  risk factor."
- HbA1c 6.5% or more without known diabetes: "In the diabetes range (6.5% or above); confirm with a
  repeat test."
- LDL, total cholesterol, triglycerides: "Above the desirable level; a modifiable vascular risk
  factor." Low HDL: "Below the desirable level; a modifiable vascular risk factor."
- TSH raised, free T4 normal, no levothyroxine: "Raised TSH with normal free T4, a subclinical
  hypothyroidism pattern; repeat with free T4 and TPO antibodies in 2 to 3 months."
- TSH raised on levothyroxine (RM04): "Raised TSH with normal free T4 on levothyroxine, an
  under-replacement pattern."
- Hb, Hct, MCV low (RM04): "Microcytic anaemia." Ferritin low: "Low ferritin: depleted iron stores."
  Iron low and TIBC high: "Low serum iron with raised TIBC, an iron-deficiency pattern."
- B12 low (M04): "Low serum vitamin B12." Homocysteine raised: "Raised homocysteine, consistent
  with B12 or folate deficiency; also a vascular risk marker." MMA raised: "Raised methylmalonic
  acid: supports functional (tissue) vitamin B12 deficiency."
- eGFR or creatinine (M05): "Reduced eGFR (CKD stage G3b range); relevant to the dosing of renally
  cleared drugs." Adapt the creatinine row to the same effect.
- Leave null: sodium, chloride, BUN, random or fasting glucose (the HbA1c row carries the point).
- The texts must not name the case's diagnosis. Keep the case's spelling (anaemia/anemia).
- The musts these values need already exist (D9). Check that they still name the values.

### C5. MCI-MUST: "no medicine is approved for MCI" (ed848cd8 S06; class M01, M02, M03, M04, RM04) -> FIXED
- In the reassessment must, replace "explain that no medicine is approved for mild cognitive
  impairment [AAN_dementia_2018]" with: "explain that cholinesterase inhibitors and memantine are
  not recommended for mild cognitive impairment [AAN_dementia_2018], and that anti-amyloid
  antibodies, licensed for mild cognitive impairment or mild dementia due to Alzheimer disease with
  confirmed amyloid pathology, need a specialist eligibility assessment (amyloid confirmation, MRI
  for microhaemorrhages, APOE genotype) [Lecanemab_AUR_2023]".
- Use the case's spelling (microhemorrhages in US-spelled cases).
- S06: also rewrite `metadata.key_educational_points[4]`: "Cholinesterase inhibitors and memantine
  are not recommended for mild cognitive impairment; serial assessment, exercise and vascular risk
  management are the evidence-based steps, and anti-amyloid antibodies are an option only after
  amyloid confirmation and specialist assessment."
- Keep the prohibition and the KCE (correct).

### C6. GLYC-TARGET (887d7401 RS05; class M02) -> FIXED
- RS05 must [5]: "Manage vascular risk: keep HbA1c at the individualised target below 8.0% (7.3% now)
  without hypoglycaemia and do not intensify, continue blood pressure and lipid treatment, and
  encourage a return to daily walks [ADA_older_adults_2026]."
- M02 must [2]: replace "HbA1c 7.3%, above her goal" with "HbA1c 7.3%, within the individualised
  target below 8.0% for an older adult with cognitive impairment"; add `[ADA_older_adults_2026]`.
- Check the medicines: if a sulfonylurea or insulin is listed, add "and review the hypoglycaemia
  risk of <drug>".
- Other glycaemic musts: no change. P02 and RM03 are under 65, where the ADA older-adult target
  does not apply.

### C7. RS06-MRI (f9f5c37f) -> FIXED (D12)
- `action-7-analyze-brain-mri`: delete the `contrast: true` alternative and drop "and either study
  shows the extraaxial lesion" from the rationale.
- New optional criterion `action-11-analyze-brain-mri-contrast` (check the id is free),
  `analyze_brain_mri` `{"contrast": true}`. Label "Characterise the incidental extra-axial lesion
  with gadolinium MRI". Expected evidence quoted from the stored `request_contrast_mri` report.
  Rationale and citation per D12. Place it right after the MRI criterion.
- Soft constraint `action-7-analyze-brain-mri` before the new id, with reason "Contrast is given for
  the lesion the non-contrast study shows; it is not part of the dementia protocol." and citation
  `[NIA_AA_2011]`.
- Move the contrast MRI follow-up right after the neuropsych battery block, in criterion order.
- Run `mri_probe.py ALZ-EARLY-RS06` and perfect_agent.

### C8. RS06-RH (03630de8) -> FIXED
- `red_herrings[0].correct_interpretation`: the first sentence becomes "Cognitive deficits during a
  depressive episode often improve with remission but can persist." The rest stays.
- Class: only case dataset-wide.

### C9. S02-STATIN (9633e19d) -> FIXED (clarification)
The premise (hyperlipidaemia listed) is not in the file. In must [4], replace "check a lipid profile
and start a statin (type 2 diabetes at 74 with lacunes and moderate white matter disease)" with "he
takes no statin: check a lipid profile and start a moderate-intensity statin, indicated by type 2
diabetes at 74 with lacunes and moderate white matter disease".

### C10. Case comments (7) -> NO-ACTION (D15)

## 3. Per-case index (all 30)

Shorthand:
- C3-std = remove nothing; add FDG waste + SPECT waste; max 0; reorder follow-ups.
- C3-sp = SPECT waste; max 0; reorder; no FDG label.
- Lab rows to fill are listed under C4. "fdg-crit-del" = delete FDG criterion.

### ALZ-EARLY-M01 (no notes)
- C3-sp (borderline CSF: no FDG label).
- C4: HbA1c 7.3 (known diabetes).
- C5: must R1.

### ALZ-EARLY-M02 (no notes)
- C3-std. C4: HbA1c 7.3. C5: must R1. C6: must R2 "above her goal".

### ALZ-EARLY-M03 (no notes)
- C3-sp (intermediate likelihood: no FDG label). C4: HbA1c 6.5. C5: must R1.

### ALZ-EARLY-M04 (no notes)
- C3-std.
- C4: B12 180, homocysteine 19.8 (initial and MMA follow-up), TSH 6.8 (no levothyroxine: subclinical
  text), MMA 0.68, HbA1c 7.0.
- C5: must R3.

### ALZ-EARLY-M05 (no notes)
- C3-std. C4: creatinine, eGFR 44, HbA1c 7.8, LDL 104, HDL 48, TG 178.

### ALZ-EARLY-P01 (no notes)
- C3-sp + fdg-crit-del (`action-9-order-advanced-imaging`), no FDG label.
- C4: HbA1c 6.4 (treated diabetes). No new must.

### ALZ-EARLY-P02 (no notes)
- C3-sp + fdg-crit-del (`action-10-order-advanced-imaging`). C4: HbA1c 5.8 (check diabetes status).
- Speech-language follow-up stays credited (recommended criterion).

### ALZ-EARLY-P03 (no notes)
- C3-sp; keep the FDG criterion (NICE 1.2.23, bvFTD question); the FDG follow-up stays in block (a).

### ALZ-EARLY-P04 (no notes)
- C3-std.

### ALZ-EARLY-RM01 (no notes)
- C3-std. C4: total cholesterol 228, LDL 148.

### ALZ-EARLY-RM02 (no notes)
- C3-std. C4: HbA1c 6.1 (check diabetes status). Gait follow-up stays credited.

### ALZ-EARLY-RM03 (R1 in_progress)
- f05917ed-36b2-4608-ac6e-5c6ed097b132: FIXED (C3.1/C3.7: amyloid PET second alternative,
  uncredited, penalised at max 0; report kept and reordered; CENTRAL C1).
- b749efc2-31a3-40ce-a459-40198873fbb7: FIXED (C3.3 FDG waste; report kept, block c).
- 2e51aa05-e2ba-4198-8c47-11336e5f6d2d: FIXED (C3.6 max 0; C3.9 clarification). Genetics and drug
  check are credited optional criteria, so they are exempt.
- 09f11b21-5f38-44a7-b183-f260d0f3a667: FIXED + CENTRAL display (C4: HbA1c 6.9 known diabetes; TSH
  5.8 subclinical text; musts R7, R8 exist).
- aff6e392-1328-4f92-9c3b-dce81fb9b853: NO-ACTION (comment; over-testing covered by C3).
- Class: C3-std.

### ALZ-EARLY-RM04 (R1 in_progress)
- d9f0cce8-fff3-4e59-b92f-22426bd1672f: CENTRAL (C1: Category Fluency 12 = yes, RCFT copy 33 = no,
  RCFT delayed 6 = yes already).
- f901b0ca-1015-41be-8a3b-fcea9fb2223e: FIXED (C3.1/C3.7). CSF is in the initial output, and the
  amyloid PET follow-up moves to block (b).
- 6ee54325-c152-4977-836a-e70bfc05e784: FIXED (fdg-crit-del `action-9-order-advanced-imaging` +
  C3.3 FDG waste).
- 0fe88822-c3ae-4fa4-8b4d-2babd6a27159: FIXED (C3.6, C3.9).
- 500ac750-3ac3-45f0-a8d2-d6fe017cf113: FIXED + CENTRAL display (C4: Hb, Hct, MCV, iron, ferritin,
  TIBC; TSH on levothyroxine text; musts R1, R2 exist).
- c7b35285-52f4-412c-ab63-55b05083c82f: NO-ACTION.
- Class: C5 must R3.

### ALZ-EARLY-RP01 (R1 in_progress)
- b459c9ec-817e-4966-9031-205fb46290e5: CENTRAL (C1: CVLT recognition 14 = no, VOSP 4 = yes,
  category 15 = no already).
- 576cbc84-7fd3-46fa-b7d3-4f9b8644ce23: FIXED (C3.1/C3.7).
- 4f25013c-b034-4f33-bec8-82d8c9d9a196: FIXED (fdg-crit-del `action-10-order-advanced-imaging`; no
  waste label, PCA, R1's own "potentially useful").
- 7c1cca06-ba2c-4e9b-b3d8-b6c117cda591: FIXED (C3.6, C3.9: the drug check is exempt as a criterion).
- 5a9b098b-eddb-46e9-ab14-16e8d69bdcea: FIXED + CENTRAL display (C4: TC 218, LDL 132, TG 170; must
  R3 exists).
- 12d38e8c-bed1-4aa8-bbf4-cf6c317c92a2: NO-ACTION.
- Class: C3-sp; the abdominal ultrasound follow-up goes to block (c).

### ALZ-EARLY-RP02 (R1 in_progress)
- a4f0149c-ceed-42a2-b0cb-2dde7fbe7f4b: CENTRAL (C1: CVLT LDFR 9 = yes, recognition 15 = no, Hooper
  11 = yes already).
- 8839e83f-b5d5-40ef-be1a-2c6c7ee9ef72: FIXED (C3.1/C3.7).
- f1647683-49de-423d-9b96-6807a6eb7248: FIXED (fdg-crit-del `action-10-order-advanced-imaging`, no
  label).
- 44dd0687-a2d0-45bb-8a91-2a32d73da45d: FIXED (C3.6, C3.9: the ECG before donepezil with
  escitalopram and the required drug check are criteria, so they are exempt; R1's example is the
  rule).
- 217c0224-3a95-4baf-a0c9-ae05484c6130: NO-ACTION.
- Class: C3-sp.

### ALZ-EARLY-RP03 (R1 in_progress)
- 06bc0294-bd15-45ff-858c-57b30f9474e1: CENTRAL (C1: TMT-B 142 = yes, CVLT LD 10 = no, VOSP 5 = yes
  already; "overall abnormal = no" is the MMSE row, 25/30 within 24-30, correct).
- bd0e2f77-8019-40a3-8c99-0f59066cd562: FIXED (C3.1/C3.7).
- 4997f3f5-a92e-47fd-8877-0c8ac305b4b0: FIXED (FDG|SPECT criterion deleted; C3.4 SPECT waste).
- 4ec3fae9-6c7e-45c1-8a06-2bcbde2fa918: FIXED (fdg-crit-del `action-9-order-advanced-imaging`; FDG
  report kept in block c; no FDG label, PCA).
- 49af6c1f-5047-49c5-b500-e699033865fe: FIXED (C3.6, C3.9).
- Class: the visual-field follow-up goes to block (c).

### ALZ-EARLY-RP04 (R1 in_progress)
- 970178c1-7f36-4666-80bd-70c804e9f461: FIXED (C3.1 amyloid PET waste label, D4).
- efa4da67-60b1-4c53-959a-24da55e2595a: FIXED (C3.3 FDG waste with the CJD clause; report kept,
  block c).
- bac6d7b8-fd6f-4554-8ecc-dd0125de4377: FIXED (C3.6, C3.9; CSF and EEG are criteria).
- 26c3a5c3-a957-4932-8a44-816cf5d61ef6: NO-ACTION.
- Class: C3.4 SPECT; C4 HbA1c 7.6 (must R3 exists).

### ALZ-EARLY-RP05 (R1 in_progress)
- 7e7426ae-64e9-4ff5-97eb-c5a679bd69b6: FIXED (C3.1/C3.7: amyloid PET is a second alternative here,
  CSF in the initial output).
- 1af2b7b1-fc5d-4a25-8337-aee27f4c72ba: FIXED (C3.3 FDG waste with the DaTscan clause).
- a4c820f0-3946-4df4-b73b-b3ca3537d95a: FIXED (C3.6, C3.9: DaTscan and ambulatory EEG are the
  targeted differential tests and are exempt as criteria).
- 2919de25-2aff-4863-badd-6be18532c663: FIXED + CENTRAL display (C4 MMA 0.52; must R2 B12 replacement
  exists).
- 835caa5b-46be-414a-a3bb-40ab1795941f: CENTRAL (C1: Digit Span Forward 5 = yes already).
- c6fb8b7a-2f04-46be-b78d-9e3161887b3b: NO-ACTION.
- Class: C4 HbA1c 7.1; C3.4.

### ALZ-EARLY-RS01 (R1 in_progress)
- 0ec11e0f-cf85-4431-9d6f-eb493665da9a: CENTRAL (C1: BNT 15th = yes already).
- 13bc971a-138f-4e95-9d28-98bfa6b65110: FIXED + CENTRAL display (C4 LDL 112; must R4 exists).
- 1d6670ef-46eb-44f9-a4b4-cd279a94d56a: NO-ACTION.
- Class: C3-std.

### ALZ-EARLY-RS02 (R1 in_progress)
- 024b2b33-fb23-4a1c-b6e5-c22bece10667, 1d4addd4-113f-4a32-9bb6-52971c18280b,
  5588b8a6-2cb9-4d86-9c53-fc666fd32d85, 0dabee48-192b-4ac1-acf9-5e7deff9dd06: CENTRAL (C1: FAS 22nd =
  yes, TMT-A 28th = no, TMT-B 15th = yes, RCFT copy 30th = no already).
- Class: C3-std; C4 HbA1c 6.4.

### ALZ-EARLY-RS03 (R1 in_progress)
- 95193f89-dbda-48d8-9255-d01eb1b4a9c7, a020f346-a2cb-4022-8ee4-3ae9a909e556,
  faa0e42f-9668-4666-9667-4ff0bb3030d5, d0d9771c-ff5d-4688-87e4-7dbc37f8c50b: CENTRAL (C1: category
  6th = yes, TMT-A 34th = no, TMT-B 12th = yes, RCFT copy 26th = no already).
- Class: C3-std; C4 HbA1c 6.8.

### ALZ-EARLY-RS04 (R1 in_progress)
- 5157edef-4881-4384-8f07-d4d0365bf688, 2f905b0a-25f1-427c-a100-a5ed6cb67e86,
  0edcc211-49e9-4cde-bdc7-674125bc676d: CENTRAL (C1: category 8th = yes, TMT-A 25th = no, TMT-B 11th =
  yes already).
- Class: C3-std; the ultrasound goes to block (c).

### ALZ-EARLY-RS05 (R1 in_progress)
- 28a2246b-c3bc-4f68-a682-a4da5959c962, 8efc72ff-bf79-4a01-9440-f525485760b7: CENTRAL (C1: category
  8th = yes, RCFT copy 27th = no already).
- 0d7c5fbb-b132-415b-9299-e5eb8e58c94f: FIXED + CENTRAL display (C4 MMA 0.58; musts R0, R1 exist).
- 887d7401-1e78-40c5-aa36-fbd4dd364c72: FIXED (C6).
- Class: C3-std (CT case; MRI stays an avoided action); C4 HbA1c 7.3.

### ALZ-EARLY-RS06 (R1 in_progress)
- 588ed609-f718-46dc-ba2d-1043e1e0c812: CENTRAL (C1: category 7th = yes already).
- f9f5c37f-7233-4da5-a16d-80aeaffa34ca: FIXED (C7, undoes October Q5 in part).
- 03630de8-f436-41fc-9f6c-f62b32d63119: FIXED (C8).
- Class: C3-std.

### ALZ-EARLY-S01 (R1 in_progress)
- 014be4a3-ea68-4a8c-8ab6-263da1e24fb1, 4876433c-ceb8-4dff-81fe-b2923fa68491,
  27967731-ba3c-4ad0-bfe8-b03b2f62c7e6, 6b2ad704-5a85-43fd-bbcb-226dee330dba,
  19f86249-3238-4676-97a3-10083a4750de: CENTRAL (C1: RAVLT recognition 3rd = yes, BNT 25th = no,
  category 10th = yes, TMT-A 30th = no, TMT-B 20th = yes already).
- Class: C3-std; no C4 rows (sodium and glucose only).

### ALZ-EARLY-S02 (R1 in_progress)
- b9449a3f-7a6e-4165-a112-42b346d74b06, c87dbc22-e568-44ea-b86f-93f9a875a299: CENTRAL (C1: FAS 22nd
  = yes, TMT-A 25th = no already).
- 9633e19d-b3ab-4bea-915b-f858ef175afe: FIXED (C9 clarification; premise absent).
- Class: C3-std; C4 HbA1c 6.9.

### ALZ-EARLY-S03 (R1 in_progress)
- 28e55e70-aba4-404e-a1bd-5a61d689f167, 65ddec21-c619-4985-ab7c-ead1ad1916d7: CENTRAL (C1: FAS 22nd
  = yes, TMT-A 25th = no already).
- Class: C3-std; C4 HbA1c 7.2.

### ALZ-EARLY-S04 (R1 in_progress)
- 86d7f86c-5988-4ef4-b803-309b67a2bf6d, 7a0ae819-dce2-470d-b64f-e7c49be60f5f,
  d274af6a-adeb-44dd-9fbf-0b3b34f17839, 48e85722-cd9b-42f0-be9f-d96ade1f1365,
  05371a20-6cb5-4686-a747-b4c135f5e4e3: CENTRAL (C1: FAS 22nd = yes, TMT-A 28th = no, TMT-B 15th =
  yes, RCFT copy 25th = no, RCFT delayed 5th = yes already).
- Class: C3-std; C4 HbA1c 6.3.

### ALZ-EARLY-S05 (R1 in_progress)
- b05ce663-ba09-4109-b158-cc3e346ea892, 501964ea-9fdb-47d8-ad03-cd24aa303a82,
  bcea24ff-20b5-48e1-959c-d161323070f5, 08f6117b-1eaa-4ddd-8c22-613e6bbb7fe7,
  283cfb61-8eb0-4d75-9866-d091a47ec494: CENTRAL (C1: BVMT delayed 8th = yes, BNT 22nd = no, category
  10th = yes, TMT-B 18th = no, Clock Drawing already yes; the "no" the reviewer saw is the GDS row).
- Class: C3-std; C4 HbA1c 7.1.

### ALZ-EARLY-S06 (R1 in_progress)
- 4e456ba4-ecbb-4d8a-9c31-239bd860b6ba: CENTRAL (C1: the "overall" flag is the MMSE row, 28/30
  within 24-30 = no, correct).
- a9cdf026-ef2e-4f76-b980-5829525c93d6: CENTRAL (C1: MMSE already no).
- 49f28383-df84-461d-818d-124eb720b03b: CENTRAL (C1: category 19th = yes already).
- c23ae468-83ac-406f-afc5-f1fc349c7650: FIXED (C2).
- 58d72c72-0115-4498-946f-8cdc42449cdc: CENTRAL (C1: RCFT copy 42nd = no already).
- bf131bfe-11cf-4a37-8cb0-989f7338f6cb: CENTRAL (C1: RCFT delayed 10th = yes already).
- ed848cd8-2b07-47e7-a24e-2ab4411e820d: FIXED (C5, including metadata.key_educational_points[4]).
- Class: C3-std; C4 HbA1c 7.0.

After editing, for every case:
- `perfect_agent.py <ID> -v` (one id per call) and `case_io.py check <ID>`.
- Confirm that no avoided action matches a criterion call. FDG waste and P03's FDG criterion never
  coexist.
- Confirm that each amyloid alternative is still answered by a case-authored report, not the
  library.

## 4. CENTRAL requests

1. **Review app, on-request follow-ups** (`web-review/src/components/cases/CaseDetail.tsx`,
   `PathwaySection`): render the follow-ups that match no `action_criteria` alternative in a
   separate section, "Served only if ordered (not part of the expected work-up)". Label a
   follow-up that answers a criterion's second alternative "alternative to step N".
   - Measured: 3085 such follow-ups in 554 of 600 cases (143 in ALZ-EARLY).
   - Cause: physicians read them as performed (ALZ notes in RM03, RM04, RP01-RP05).
2. **Review app, CENTRAL.md items 1 and 2** (null as "none"; label keys first): needed for 43 ALZ
   neuropsych notes and 6 lab notes.
3. **Schema / review app, StopRule**: an optional `rationale` string on `StopRule`
   (neuroagent-schemas `evaluation.py`), shown in the review app with the sentence "actions that
   match an optimal action never count against the allowance". Requested by R1 in 7 stop-rule
   notes.
4. **Criteria pack** `dataset-generation/criteria_packs/ALZ-EARLY.md`:
   - section 2: FDG optional only in P03; SPECT and FDG waste rules per D5 and D6;
   - section 5: stop rule `max_additional_actions` 0;
   - RS06 MRI: plain required, contrast optional;
   - section 7: MCI wording per C5;
   - allow-list: `[EANO_meningioma_2021]` (Goldbrunner R et al., EANO guideline on the diagnosis and
     management of meningiomas, Neuro Oncol 2021;23(11):1821-1834).
5. **Citation registry**: add `[EANO_meningioma_2021]` wherever citation keys are checked.
6. **Guidance claims** (`build_condition_tool_guidance.py` ALZ responses, `test_guidance_claims.py`,
   maintained centrally): FDG is now a criterion in 1 case (P03), not 7; perfusion SPECT is a waste
   label in 30; RS06 MRI is plain-required with optional contrast.
7. **Optional guard**: a neuropsych/specialized-test row whose numeric or percentile value falls
   outside its own `reference_range` must not carry the opposite flag (np_flags.py logic; it needs a
   parser that handles z-scores and BP strings).

## 5. Open questions

None for Andrea.

For physicians at re-review:
- max_additional_actions 0 now penalises any uncredited test after the required work-up.
- FDG-PET is uncredited outside P03.
- A remark only, not acted on: the 25th-75th "average" band is used as the abnormality cutoff in
  the S/RS batteries (D2).

<!-- PLAN COMPLETE -->
