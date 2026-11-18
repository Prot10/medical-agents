# MG round plan (November 2026)

Lead plan for the 30 myasthenia_gravis cases, written 17 Nov 2026.
- Decisions and reasons: `plans/MG-decisions.md`. D1..D30 below refer to its entries.
- Notes: 40, all from R2 (NB-87MF-FBTV-TPWE), in 29 cases. MG-RM12 has no note but has class
  findings.
- Approved before this round: MG-RM13, MG-RM14, MG-RM15, MG-RS11. They change only where the
  index below says so. Say so in their logs.
- October decisions still in force unless a D entry says otherwise:
  `round-2026-10/plans/MG-decisions.md` and `round-2026-10/plans/MG.md`.
- Cases read in full: M04, RS14, RP13 (patient and ground truth), M03 (outputs). Every other case
  was read through the scripted dumps.
- Scripts (`/home/aprotani/review-round-2026-11/work/scratch/mg-lead/`):

| file | content |
|---|---|
| `survey.txt` | every criterion, follow-up, avoided action, constraint, stop rule, must and prohibition |
| `classes_out.txt` | text classes over the 30, plus counts over the other 570 |
| `struct_out.txt` | per case: AChR titre, RNS/resp/ECG tiers, ECG stored, mediastinal MRI alternative, unlabelled served reports |
| `resp_mg.py` | bulbar keywords and respiratory values |

Workers:
- Edit through `case_io` load/save only. Keep every `criterion_id`; new ids are given below.
- After each case, run `perfect_agent.py CASE -v` and `case_io.py check CASE`. After any MRI edit,
  also run `mri_probe.py CASE`. After any lab-panel split or criterion change, serve each lab order
  of the case and confirm it receives only the panels it names.
- English, American spelling as in the cases. No em dashes in new text. No review-process text in
  `metadata`.
- Update `metadata.last_revised` ("2026-11-17") and `metadata.revision_reason` to describe the case
  as edited.
- Do not churn prose that is correct. Do not add literature criteria or outputs (class LIT).

## 1. Governing guidelines and canonical facts

| Key | Source | Governs |
|---|---|---|
| `[Jacob_2025]` | ABN 2025, Pract Neurol 2025;25:422-437 | Diagnosis order; neurophysiology mandatory when antibodies are negative; thymic imaging in all; steroid protocols (daily); pyridostigmine maximum; ECG before pyridostigmine; IVIG dosing; inpatient/ICU criteria; thymectomy age bands; early non-steroidal immunosuppression; SLT swallow assessment; oncology referral for thymoma |
| `[Narayanaswami_2021]` | ICG 2020 update, Neurology 2021;96:114-122 | Thymectomy rec 1a (18-50, early); seronegative and ocular thymectomy "may be considered"; MuSK rituximab and no thymectomy; Table 1 drugs used with caution (beta-blockers, statins, iodinated contrast); ocular MG section |
| `[Evoli_2019]` | Neurol Sci 2019;40:1111-1124 | Admit bulbar patients to start steroids; ice-pack test above 2 mm positive, NPV 94%; repeat negative RIPA at 6 months; pyridostigmine up to 90 mg five times daily; over-60 thymectomy diversion |
| `[Fionda_2026]` NEW | Fionda L et al., Italian recommendations, Neurol Sci 2026;47:353 (doi 10.1007/s10072-026-08964-y) | Live CBA (clustered AChR and MuSK) before calling MG seronegative (st. 5); LRP4 "may be tested" (st. 6); repeat neurophysiology at a centre in triple-seronegative cases (st. 8); steroid adverse-event prevention and monitoring (prevention st. 1-2); vaccinations (st. 3, HPV up to 45); MGFA and MG-ADL/QMG (severity st. 1-2) |
| `[Sanders_2016]` | Neurology 2016;87:419-425 | MuSK: poor pyridostigmine response, good PLEX response; general management where nothing newer is cited |
| `[Wolfe_2016]` | MGTX, NEJM 2016 | Thymectomy statements only (trial enrolment under 65; it is not an age-range recommendation) |
| `[Relling_2019]` NEW | CPIC thiopurine TPMT/NUDT15, Clin Pharmacol Ther 2019;105:1095-1105 | NUDT15 alongside TPMT |
| `[Virani_2023]` NEW | 2023 AHA/ACC chronic coronary disease, Circulation 2023;148:e9-e119 | RS16 coronary angiography harm label |
| `[Lawn_2001]` | GBS cohort | No longer cited for MG escalation thresholds (D8). Kept only in approved RM14/RM15 |

NEW keys are cited by author in text until CENTRAL C5 adds them to the pack allow-list.

Canonical texts. Fill the `<...>` slots and drop clauses that do not apply. Keep the case's drug
name (prednisone or prednisolone).

- **M1, pyridostigmine (D7, D12):** "Start pyridostigmine 30 mg three to four times daily after a
  baseline ECG <with heart-rate watch if on a beta-blocker or with coronary disease>, titrating to
  effect (usually up to 60 mg four to five times daily); the maximum is 360 mg/day, with specialist
  review above 300 mg/day (Jacob 2025)."
- **S1, outpatient generalized steroids (D4, D5):** "If symptoms persist on pyridostigmine, start
  prednisone 5-10 mg daily and increase by 5 mg every 3-5 days to 30 mg daily (up to 1 mg/kg, not
  above 60 mg, only after specialist discussion), warning that weakness may worsen around days
  5-10 (Jacob 2025)."
- **S2, inpatient steroids (bulbar or admitted) (D4, D5):** "Start prednisone in hospital, because
  bulbar weakness makes steroid-induced worsening dangerous (Evoli 2019): 5-10 mg daily increased
  by 5 mg on alternate days <after IVIG or plasma exchange: from 10 mg by 5-10 mg every second day>
  to 30 mg daily, with bulbar and respiratory monitoring (Jacob 2025)."
- **S3, ocular steroids (S05):** "If ptosis or diplopia stay disabling on pyridostigmine, start
  prednisone 5-10 mg daily and increase by 5 mg every 3-5 days to 20 mg daily (maximum 0.5 mg/kg,
  not above 30 mg) (Jacob 2025; ICG 2020 ocular MG section)."
- **S4, early steroid-sparing agent (D14):** "Start azathioprine early alongside the steroid, after
  TPMT (and NUDT15 where available) testing, because <diabetes / ischaemic heart disease / BMI
  over 25 with insulin resistance / existing steroid toxicity / age> raises the risk of steroid
  toxicity (Jacob 2025; Fionda 2026)." Elsewhere keep "plan a steroid-sparing agent (azathioprine
  after TPMT testing) if long-term immunosuppression is needed".
- **S5, screening and monitoring (D13):** "Before long-term immunosuppression <, without delaying
  urgent treatment,>: HbA1c, lipids, blood pressure and weight before steroids; hepatitis B
  (HBsAg, anti-HBc) and hepatitis C serology, TB screening (IGRA) and HIV test; vaccinations
  updated at least four weeks before <women up to 45: including HPV> (Jacob 2025; Fionda 2026).
  During steroids: periodic blood pressure, glucose, weight and eye checks, calcium and vitamin D,
  and bone densitometry (Fionda 2026)." Add "an ophthalmological assessment before high-dose
  steroids" in RM16 (thyroid eye disease) and RP13 (ocular hypertension).
- **P1, outpatient prohibition (replaces "above 20 mg/day"):** "Do not start prednisone at full dose
  (for example 1 mg/kg daily) at once; escalate from a low dose, because steroid initiation can
  transiently worsen MG (Jacob 2025)."
- **P2, bulbar prohibition:** "Do not start corticosteroids as an outpatient while bulbar weakness
  is significant; start them in hospital with bulbar and respiratory monitoring (Evoli 2019)."
- **T1, thymectomy under 50 (D6):** "Offer thymectomy early, once MG is optimally controlled:
  AChR-positive generalized MG without thymoma at <age> (ICG 2020 recommendation 1a, ages 18-50;
  Jacob 2025)<; IVIG or plasma exchange beforehand only on clinical indication>."
- **T2, thymectomy at 50-65:** "Discuss thymectomy once MG is optimally controlled: ABN 2025
  advises discussion at 50-65, while ICG 2020 recommends it at 18-50 and found no benefit at 50 or
  over in the post hoc MGTX analysis <60 and over: the Italian recommendations divert
  AChR-positive patients over 60 (Evoli 2019)>."
- **T3, thymoma:** "Refer to thoracic surgery for complete thymectomy (any thymoma, regardless of
  age, antibody status or severity) and to thoracic oncology (Jacob 2025; ICG 2020); optimise MG
  first, with pre-operative IVIG or plasma exchange only on clinical indication <here: bulbar
  weakness / reduced respiratory reserve>."
- **R1, respiratory escalation (D8):** "Repeat FVC (with MIP and MEP) <at least twice daily / if
  symptoms progress>; refer to ICU or HDU if FVC falls below 20 mL/kg or by more than 30%, or if
  she cannot complete a sentence, uses accessory muscles or cannot clear secretions (Jacob 2025)."
  Inpatient criteria where needed: FVC below 30 mL/kg, single-breath count below 25, significant
  bulbar symptoms.
- **I1, IVIG (D15):** "IVIG <1 g/kg over 2-3 days for significant bulbar weakness without
  ventilatory failure / 2 g/kg over 2-5 days in crisis or impending crisis>, dosed by ideal body
  weight (about <g> g), after hepatitis B and C serology and an IgG level, or plasma exchange (5
  exchanges) (Jacob 2025)." Use the Devine IBW (men 50 kg, women 45.5 kg, + 0.9 kg per cm over
  152.4 cm) and the case's height.
- **G1, severity (D23):** "Record the MGFA class (here <class>) and a baseline MG-ADL, with QMG
  where available, to follow treatment against the goal of MG-ADL 0-1 (Fionda 2026; Jacob 2025)."
  Add to the first management must, or as its own must. Not in LEMS cases.
- **Q1, SFEMG constraint reasons (D3):** as in D3, verbatim.

## 2. Classes

Measured over all 30 cases (`classes_out.txt`, `struct_out.txt`). "Other conditions" counts are
over the other 570 cases.

### C1 REPORT-DISPLAY (D1)
Notes: d6d236df (M01), 4baca060 (M02), 4257311d (M03).
Finding: the data are correctly paired in all checked blocks. The app sorts keys alphabetically.
The class exists wherever rows are dicts (every case of every condition).
Fix: CENTRAL.md item 2. Workers check the four blocks of each M case against its impression.

### C2 TIER-RNS (D2)
Notes: verdicts of RM11, RM16, RP11, RP13, RS12, RS13, RS15, RS17, S01, S02, S03, S04, S05.
Measured: RNS is required in 27 cases.
- Downgrade to recommended and drop from the stop rule (19): M01, M03, P03, RM11, RM16, RP11,
  RP13, RS12, RS13, RS14, RS15, RS17, S01, S02, S03, S04, plus the ocular RNS-or-SFEMG criterion
  in S05 and RS11 (approved).
- Keep required: M02, RM12, RP12, RS16, P01, P04, RP14, P02, RM13.
- In downgraded cases, the prohibition "before AChR antibody testing and neurophysiology" becomes
  "before AChR antibody testing (and neurophysiology when serology is negative)".

### C3 SEQ-REASON (D3)
Note: 4382d2ff (M01).
Measured: the text "SFEMG is reserved for seronegative patients" appears in 21 cases (M01, M02,
M03, P01, P03 (+rationale), RM11, RM12, RP11, RP12, RP13, RP14, RS12, RS13, RS14, RS15, RS16, RS17
(+KCE[2]), S01, S02, S03, S04). Other conditions: 0.
Fix: Q1 wording. In M01, M02, M03, S01, S02, S03, S04, RM11, RM12, RS12, RS17 and RS16, move the
SFEMG follow-up after the core results (labs, imaging, respiratory, ice pack).

### C4 STEROID (D4, D5)
Notes: f70a2727 and all verdicts listed in D4.
Measured: the "above 20 mg/day" prohibition is in 25 cases (all but M04, P02, RM13, RM14, RM15).
"10-20 mg" starts are in 15: M01, M02, M03, P01, P03, P04, RS11 (approved, unchanged), RS12,
RS15, RS16, RS17, S01, S02, S03, S04. Other conditions: 0.
Setting per case:
- outpatient S1 + P1: M02, P03, P04, RM16, RP13, RS15, RS16, RS17, S02, S04;
- inpatient S2 + P2: M01, M03, P01, RM12, RP11, RP12, RP14, RS12, RS14, S01, S03;
- ocular S3, no prohibition: S05;
- delete the prohibition only: RM11, RS13 (both already on steroids);
- RS11 approved: unchanged (D4 lists it among the 25, but it is an approved ocular case whose
  wording R2 accepted).
M01, M03, P01, S01 and S03 are inpatient because of significant bulbar weakness, or pre-operative
care with significant bulbar weakness. A worker who reads the HPI otherwise switches to S1 + P1
and logs why.

### C5 THYMECTOMY (D6, D24)
Measured: "18-65" in RM11, RM16, RP13, RS17 (+KCE), S02 (+KCE), S04 (+KCE). MGTX or Wolfe as the
basis in M02, RM12, RM16, RS13, RS15, RS16 (KCE), RS17, S02, S04.
- T1: M02 (48), RM12 (42), RM16 (38), RS13 (47), S02 (29), S04 (45).
- T2: RM11 (57, deferred during lymphoma treatment), RP13 (53; keep the long-history
  uncertainty), RS15 (53), RS17 (60, with the Evoli clause).
- Over 65, not routine: RS12, RS16, RP12 (KCE text only).
- T3: M01, M03, P03, RP11, S01, S03.
- Other: RS14 (MuSK, ICG 2020); P01, P04, RP14 (seronegative/LRP4, D6 sentence).
Also fix the criterion rationales that cite MGTX: M02, RM12, RS13, RS15, RS17, S02, S04.

### C6 PYRIDOSTIGMINE CEILING (D7)
Measured: "360-480" in P03, P04, RM11, RM12. RS17 says "maximum about 360 mg/day", which becomes
M1.

### C7 RESPIRATORY THRESHOLDS (D8)
Measured: MIP -30 / MEP 40 / 20-30-40 appear in:
- musts: M01, M02, M03, M04, RM11, RM12, RP11, RS12, RS14, RS17;
- criterion rationales: M01, M04, RP11, RS17, S01, S02, S03, S04;
- RS14 respiratory impression;
- approved RM14 and RM15 (unchanged).
Fix: R1. M04's must 3 keeps its justification for ICU: weak cough, short phrases, accessory
muscle use and a fall in MIP from -52 to -32.

### C8 BETA-BLOCKER (D9)
M04 must 7, P04 contra 4, RP13 must 2. S03 must 6 and RM16 must 4 are already correct.

### C9 UNLABELLED SERVED REPORTS (D10)
Measured with `struct_out.txt`, ignoring labs and drug outputs, which are matched by panel or drug.

| report | cases | label |
|---|---|---|
| levodopa_challenge | M01, M03, M04, P02, P03, RM11, RM12, RM13, RM14, RM15, RS14, RS16 | waste; RP12 optional criterion |
| gait_and_balance_timed | M01, M03, M04, P02, P03, RM11, RM12, RM13, RM14, RM15, RP12, RP13, RS14, RS16, S04 | waste |
| speech_language_evaluation | every case that stores it (all except RS11, S05) | waste (D11) |
| ssep, cognitive_screen, neuropsych_battery | P03; RP12; RS14; RM15 (cog, neuropsych, functional_neuro_signs) | waste |
| DaTscan, MIBG_scan, olfactory_test | RP12 | waste |
| polysomnography | P04 | waste |
| minor_salivary_gland_biopsy | M02 | waste |
| pelvis_abdomen_MRI | M03 | waste |
| brain MRI (analyze_brain_mri) | RM11, RP11, RP12, RP13, RS13, RS15 | waste |
| brain MRI as optional criterion | RS12, RP14, RS16 (RS14 recommended) | criterion |
| whole_body_FDG_PET | RP11, S01, S03 | waste |
| chest_xray | RP11, RM13 | waste |
| ice_pack_test | M04, RM14 | waste |
| orthostatic_blood_pressure | RM14, RM15, RM16 | waste |
| emg_single_fiber | P02 waste; RM16 optional criterion | |
| spine CT | RS16 | waste |
| coronary_angiography | RS16 | harm |
| muscle_biopsy | RS14 waste; RP13 optional criterion (D20) | |

Notes:
- Each entry needs a case-specific rationale and a real citation (e.g. Jacob 2025 for MG
  work-up). Use the term's discriminator (`assessment_type`, `test_type`, `study`, `modality`).
- Never label a study that a criterion matches.
- Move the newly labelled follow-ups to the end of `followup_outputs`.
- M04: delete `avoid-waste-6-order-cardiac-monitoring`.
- Other conditions: the same assessment follow-ups (levodopa_challenge, gait_and_balance_timed,
  speech_language_evaluation) were stored in many conditions by the library-contradiction passes.
  Their labelling is each condition lead's call.

### C10 SWALLOW (D11)
Notes: 6e3dd7da (M04), 8e6fd5cf (P04) and the verdicts listed in D11.
Measured: the musts ask for a swallow assessment in M01, M02, M04, RP12, RP14, RS12, RS14, RS15,
RS16, RS17, S01, and RM15 (approved). P01 has dysphagia in the HPI but no swallow must: add the SLT
swallowing referral to its musts. The reviewer also asks for one in S02
(optional), S03 and S04 (recommended). No criterion carries one; the vocabulary has no term.
Fix:
- Now: label `speech_language_evaluation` waste (C9).
- Musts: say "speech and language therapy swallowing assessment" (a referral) in every case with
  dysphagia. Add it to S03 and S04, whose bulbar symptoms include dysphagia.
- After CENTRAL C1 lands: add `action-swallow-assessment` (recommended; optional in S02) with a
  stored bedside swallow report consistent with the exam in: M01, M02, M04, P01, RP12, RP14, RS12,
  RS14, RS15, RS16, RS17, S01, S02, S03, S04.
- Until C1 lands, log the criterion part as CENTRAL.

### C11 RESPIRATORY TIER (D18)
Measured with `resp_mg.py`; workers confirm against the HPI and exam, with negations.
- Upgrade to required and add to the stop rule: M01, M02, M03, P01, P03, P04, RP12, RP13, RP14,
  RS12, RS15, RS16, RS17, S01, S03, S04.
- Already required: M04, RM11, RM12, RP11, RS14 (and approved RM14, RM15).
- Stay recommended: RM16, RS13, S02.
- Unchanged: RS11 optional (approved); S05 has none.

### C12 ECG (D12)
- Add `action-baseline-ecg` (recommended) plus M1:
  - ECG already stored: RP11, RP12, RP13, RP14, RS12, RS13, RS14, RS15, RS16;
  - add an ECG output first: M01, M02, M03, P01, P03, P04, RM11, RM12, RM16, RS17, S01, S02, S03,
    S04, S05. Promote a case fallback ECG if one exists and fits the patient; otherwise write a
    plain 12-lead report (rate, rhythm, PR, QRS, QTc) consistent with vitals and medicines.
- Not in: P02, RM13 (already required), M04, RM14, RM15 (already on pyridostigmine, crisis), RS11
  (approved).

### C13 SCREENING AND MONITORING (D13), EARLY IMMUNOSUPPRESSION (D14), IVIG (D15), SEVERITY (D23)
Measured: no MG must mentions hepatitis B, TB, HIV, DEXA or HbA1c screening. Vaccination appears
only in RM15.
- S5: every non-approved case except P02 (LEMS).
- S4: S03, S04, RS12, RS13, RS16, RP12, RP13.
- I1 (the must uses IVIG): M01, M03, M04, RM11, RM12, RP11, RP12, RS12, RS14, S01, S03, RP14 (if
  rescue is named).
- G1: every non-approved non-LEMS case.
- NUDT15 stays (D14).

### C14 CBA AND LRP4 (D16)
P01, RP14: split the stored "Cell-based assay panel" into a CBA panel (clustered AChR + clustered
MuSK rows) and an "LRP4 antibody (cell-based assay)" panel, with one interpretation sentence per
panel and no semicolons.
- `action-7-interpret-labs` becomes required: label "Send the high-sensitivity cell-based assay
  (clustered AChR and clustered MuSK)", alternatives `{panels: [clustered_AChR_cell_based]}`.
  When C2 lands, the alternative becomes `[clustered_AChR_cell_based, clustered_MuSK_cell_based]`.
- New `action-lrp4-antibody`: recommended, `{panels: [anti_LRP4]}`.
- Stop rule: add `action-7-interpret-labs`.
- Keep the soft constraints labs -> CBA and MuSK -> CBA; add labs -> LRP4.
P04: split "Extended_Seronegative_MG_Panel" into an LRP4 panel and a CBA panel (add a clustered
MuSK negative row).
- `action-2-interpret-labs` (LRP4) stays required.
- New `action-cell-based-panel`: recommended, `{panels: [clustered_AChR_cell_based]}`.
Record the ABN/Fionda divergence on LRP4 in the rationale.

### C15 MEDIASTINAL MRI ALTERNATIVE (D17)
Measured: thymic criteria lacking `mediastinum_MRI` are in M04 (optional), P03, P04, RM11, RM12,
RP11, RP12, RP13, RP14, and approved RM14 and RM15 (unchanged).
- Add `{study: mediastinum_MRI, contrast: true}`.
- Store an MRI report first where the CT is abnormal: P03 (thymoma), RP11 (thymoma), RM12
  (hyperplasia), RM11 (residual paratracheal lymphoma node).
- Then check with `served()` that the MRI order gets the case report, and that the CT orders are
  unchanged.

### C16 CITATIONS (D24)
Sanders 2016 appears in 24 cases and MGTX or Wolfe in 19 (classes_out.txt). Change only the
statements D24 names. Do not touch citations elsewhere.

### C17 CASE-SPECIFIC
- Label: RP13 (D20).
- Scenario: RS14 (D22).
- TRAb: S02, and the RM16 check (D26).
- Ocular figures: S05 (D27).
- Iodinated contrast: P04 (D25).
- First-order result: M04 initial/follow-up swap (D19).
- LIT: M03 (D29, ALREADY-FIXED).

## 3. Per-case index (all 30)

Ruling codes: FIXED, DECLINED, ALREADY-FIXED, CENTRAL, NEEDS-ANDREA, NO-ACTION. "Class" lines
apply even without a note. Criterion ids are as they are now.

### MG-M01
- d6d236df: CENTRAL (display, D1; data verified).
- 4382d2ff: FIXED. Reword both constraint reasons (Q1). Move the SFEMG follow-up after the core
  results. SFEMG stays optional (D3).
- Class:
  - C2: `action-2-order-specialized-test` to recommended; remove it from the stop rule.
  - C11: `action-7` respiratory to required; add it to the stop rule.
  - C12: add an ECG output and `action-baseline-ecg`; M1 into must 1.
  - C4: must 3 becomes S2 + S5; contra 2 becomes P2.
  - C5: must 2 becomes T3 (oncology, IVIG on clinical indication with I1).
  - C7: must 4 and the action-7 rationale become R1.
  - C9: waste labels for levodopa_challenge, gait_and_balance_timed, speech_language_evaluation.
  - C10: must 5 swallow wording; criterion later.
  - G1.

### MG-M02
- 4baca060: CENTRAL (display, D1).
- bfbee1e2: FIXED. Add a waste avoided action for `minor_salivary_gland_biopsy` (established
  Sjogren, anti-Ro positive, normal NCS and sensory exam; invasive, answers no question).
- Class:
  - C2: RNS stays required (D2 reason; say so in the rationale).
  - C3 reasons; SFEMG follow-up after the core.
  - C11: respiratory to required.
  - C12: ECG output and criterion; M1.
  - C4: must 2 becomes S1 + S5 (keep the PPI clause); contra 2 becomes P1.
  - C5: must 4 becomes T1 (48); fix the action-4 rationale.
  - C7: must 6 becomes R1.
  - C9: speech waste.
  - C10: swallow wording in must 6.
  - G1.

### MG-M03
- 4257311d: CENTRAL (display, D1; respiratory rows verified: FVC 2.45 L, FEV1 1.42 L).
- 7f7f43d1: FIXED.
  - Waste labels: pelvis_abdomen_MRI, gait_and_balance_timed, levodopa_challenge. The stored
    reports stay and move to the end (D10).
  - MG severity: G1 must.
  - The part asking for an MG severity action: CENTRAL not requested (D23).
- b3dbe81b: ALREADY-FIXED (class LIT, commit 393c547e; no literature output left).
- Class:
  - C2: RNS to recommended.
  - C3.
  - C11: respiratory to required.
  - C12: ECG and M1 (COPD: watch bronchial secretions).
  - C4: must 3 becomes S2 + S5 (keep the glucose clause) + S4 (diabetes) replacing must 4; contra 2
    becomes P2.
  - C5: must 2 becomes T3 (keep the COPD pre-operative assessment; I1).
  - C7: must 6 becomes R1.
  - C9: speech waste.

### MG-M04
- 6e3dd7da: CENTRAL (C1 swallow term). Interim FIXED: speech_language_evaluation labelled waste.
  Must 6 stays as an SLT referral. Rewriting the language battery into a swallow study is DECLINED
  (D11).
- 51d18b0e: FIXED. Must 7 becomes the D9 review wording.
- NB-87M:MG-M04:policy_verdict: FIXED.
  - First-order result: `initial_tool_outputs.specialized_test` becomes the respiratory function
    report; the RNS moves to a follow-up and keeps its waste label (D19). Check that both orders
    are served correctly.
  - Must 6: CENTRAL as above.
  - Waste labels: levodopa_challenge, gait_and_balance_timed, ice_pack_test,
    speech_language_evaluation.
  - Delete `avoid-waste-6-order-cardiac-monitoring`.
  - Stop rule: ALREADY-FIXED (keyed on `action-3`, test_type respiratory_function; display is
    CENTRAL.md item 3).
- Class:
  - C7: must 3 becomes R1. ICU is justified by weak cough, short phrases, accessory muscles and MIP
    falling from -52 to -32. Fix the action-3 rationale and KCE 2.
  - I1 into must 4: 2 g/kg IBW (impending crisis); IBW 50.6 kg at 158 cm, about 100 g.
  - C15: add the MRI alternative to `action-5`.

### MG-P01
- f70a2727: FIXED. Contra 2 becomes P2 (dysphagia: inpatient start). If the worker finds the
  bulbar involvement mild, use P1 and S1 and log why. Must 3 becomes S2 + S5, with a 5-10 mg start.
  Record the ABN/Evoli divergence in the must.
- b093a449: FIXED (C14). The CBA becomes required, LRP4 becomes its own recommended criterion,
  and the CBA joins the stop rule. CENTRAL C2 for clustered MuSK.
- NB-87M:MG-P01:policy_verdict: FIXED.
  - Actions: C14.
  - Stop rule: the SFEMG key is ALREADY-FIXED (`action-3-order-specialized-test` is test_type
    emg_single_fiber; display is CENTRAL.md item 3); add the CBA.
  - Recommendations: as f70a2727.
- Class:
  - C3 reasons.
  - C11: respiratory to required.
  - C12: ECG and M1.
  - C9: speech waste.
  - C10: swallow later.
  - G1 (must 2 already names MG-ADL; merge).

### MG-P02
- NB-87M:MG-P02:policy_verdict: FIXED.
  - Waste labels: levodopa_challenge, gait_and_balance_timed, emg_single_fiber (after a
    diagnostic RNS with facilitation and positive VGCC), speech_language_evaluation.
  - Stop rule: ALREADY-FIXED (`action-2` is test_type repetitive_nerve_stimulation; display is
    CENTRAL.md item 3).
- Class: none further (LEMS keeps its tiers; RNS required).

### MG-P03
- NB-87M:MG-P03:policy_verdict: FIXED.
  - Contrast field: ALREADY-FIXED (MRI-CONTRAST pair; `action-7` with contrast true is served the
    gadolinium study, `mri_probe` checked 17 Nov).
  - Waste labels: levodopa_challenge, gait_and_balance_timed, ssep, cognitive_screen,
    neuropsych_battery.
  - Contra 2 becomes P1 (she is an outpatient with mild bulbar symptoms; must 2 already starts
    low). Must 2 becomes S1, with natalizumab sequencing kept.
- Class:
  - C2: RNS to recommended.
  - C3 (+ the rationale with the old wording).
  - C6: must 1 becomes M1.
  - C11: respiratory to required (dysphagia and breathlessness in the HPI; confirm).
  - C12: ECG.
  - C15: store a mediastinal MRI with the thymoma; add the alternative.
  - C5: must 3 becomes T3 (add oncology).
  - S5 adapted to natalizumab (screening before the switch).
  - G1.

### MG-P04
- 8e6fd5cf: FIXED (polysomnography waste; speech_language_evaluation waste) + CENTRAL (C1, if a
  swallow criterion is wanted; the chewing fatigue and hoarseness are in the HPI).
- 53d0cb94: FIXED. Delete contra 4; must 4 gains the D9 caution.
- 9a202945: FIXED. D25 sentences in the `action-5` rationale and must 4.
- NB-87M:MG-P04:policy_verdict: FIXED.
  - Actions: C14 (split panel, CBA recommended). The OR equivalence is DECLINED (D16).
  - Add the mediastinum_MRI alternative (C15).
  - Stop rule: ALREADY-FIXED (keys are `action-3` emg_single_fiber and `action-2` anti_LRP4;
    CENTRAL.md item 3).
  - Must 1 becomes M1 (C6).
  - Contra 3 becomes P1, must 2 becomes S1 + S5.
- Class:
  - C11: respiratory to required.
  - C12: ECG.
  - G1.

### MG-RM11
- NB-87M:MG-RM11:policy_verdict: FIXED.
  - `action-repetitive-nerve-stimulation` to recommended; remove it from the stop rule (C2).
  - Add the mediastinum_MRI alternative, with a stored MRI showing the residual paratracheal node
    (C15).
  - Constraints: reasons per Q1. Tool-level keying is ALREADY-FIXED (criterion-level;
    CENTRAL.md item 3).
  - Waste labels: gait_and_balance_timed, levodopa_challenge, speech_language_evaluation, and the
    brain MRI pair (contrast MRI already obtained last week, per the HPI).
  - Stop rule: ALREADY-FIXED for respiratory (`action-6`); drop RNS.
  - Must 1 becomes M1.
  - Delete contra 2 (admitted; on EPOCH prednisone).
  - Must 4 thymectomy becomes T2 at 57 (kept deferred during lymphoma treatment).
- Class:
  - C7: must 3 becomes R1.
  - I1 in must 2 (1 g/kg IBW for bulbar weakness without ventilatory failure; with hydration and
    renal monitoring).
  - C12: ECG.
  - S5 (agreed with haematology).
  - G1.
  - Swallow later (C10).

### MG-RM12 (no notes)
- Class:
  - C2: RNS stays required (GBS relapse; D2).
  - C3.
  - C6: must 1 becomes M1.
  - C4: must 4 becomes S2 + S5; contra 2 becomes P2.
  - C5: must 5 becomes T1 (42, hyperplasia); fix the action-4 rationale and KCE 5.
  - C7: must 3 becomes R1.
  - I1 in must 2 (the second course 4 weeks after the GBS course is kept).
  - C12: ECG.
  - C15: store an MRI of the hyperplasia; add the alternative.
  - C9: levodopa, gait and speech waste.
  - G1.

### MG-RM13 [APPROVED]
- NB-87M:MG-RM13:policy_verdict: NO-ACTION.
- Class C9 only: waste labels for chest_xray (after the chest CT), gait_and_balance_timed,
  levodopa_challenge, speech_language_evaluation. Nothing else changes.

### MG-RM14 [APPROVED]
- NB-87M:MG-RM14:policy_verdict: NO-ACTION.
- Class C9 only: waste labels for ice_pack_test, gait_and_balance_timed, levodopa_challenge,
  speech_language_evaluation, orthostatic_blood_pressure. C7, C5 and C15 are deliberately not
  applied (D6, D8, D17).

### MG-RM15 [APPROVED]
- NB-87M:MG-RM15:policy_verdict: NO-ACTION.
- Class C9 only: waste labels for gait_and_balance_timed, levodopa_challenge,
  speech_language_evaluation, orthostatic_blood_pressure, cognitive_screen, neuropsych_battery,
  functional_neuro_signs.

### MG-RM16
- NB-87M:MG-RM16:policy_verdict: FIXED.
  - `action-2-order-specialized-test` (RNS) to recommended; remove it from the stop rule.
  - Contra 2 becomes P1. Must 6 becomes S1 + S5 (ophthalmology before high-dose steroids with TED).
  - Must 5 becomes T1 (38, hyperplasia).
  - Must 1 becomes M1 (ECG, propranolol). Add an ECG output and criterion (none stored).
- Class:
  - C9: waste for speech_language_evaluation and orthostatic_blood_pressure. Add an optional
    SFEMG criterion for the stored SFEMG (no constraint needed).
  - D26: TRAb check of `action-1` evidence.
  - G1.

### MG-RP11
- NB-87M:MG-RP11:policy_verdict: FIXED.
  - `action-2` RNS to recommended; remove it from the stop rule.
  - Add the mediastinum_MRI alternative, with a stored thymoma MRI (C15).
  - `action-baseline-ecg` recommended (ECG stored).
  - Contra 2 becomes P2 (single-breath count 22: inpatient).
  - Must 4 becomes R1, with the inpatient criterion already met.
  - Must 1 becomes T3, with oncology.
  - Must 3 becomes M1.
  - Must 6 becomes S2 + S5 (age 68; DEXA).
  - G1 with MGFA, MG-ADL and QMG.
- Class:
  - C7: fix the action-7 rationale.
  - I1 in must 2.
  - C3.
  - C9: waste for brain MRI, whole_body_FDG_PET, chest_xray, speech_language_evaluation.

### MG-RP12
- NB-87M:MG-RP12:policy_verdict: FIXED.
  - `action-7` respiratory to required; add it to the stop rule.
  - Add the mediastinum_MRI alternative (library normal is consistent: no thymic finding).
  - `action-baseline-ecg` recommended.
  - RNS with needle EMG stays required (the reviewer's ruling).
  - Waste labels: brain MRI pair, gait_and_balance_timed, speech_language_evaluation,
    cognitive_screen, neuropsych_battery, DaTscan, MIBG_scan, olfactory_test.
  - New optional `action-levodopa-challenge` (`perform_clinical_assessment{assessment_type:
    levodopa_challenge}`). Check that the stored report fits a patient already on levodopa (an off
    state before the challenge dose).
  - Contra 2 becomes P2. Contra 4 is reworded to fatigable bulbar weakness.
  - Must 3 becomes S2 + S4 (age 74) + S5.
  - Must 2 becomes M1 (keep the timing before meals).
- Class:
  - I1 in must 1 (1 g/kg IBW, significant bulbar weakness without ventilatory failure).
  - C3.
  - C10 swallow wording in must 4 (already SLT).
  - G1.

### MG-RP13
- NB-87M:MG-RP13:policy_verdict: FIXED + CENTRAL.
  - accepted[0] relabelled (D20), with MGFA IIb in the label. CENTRAL C4: synonyms and G70.01.
  - Keep CPEO out of `rejected` (checked: it is absent).
  - Differential CPEO entry: "coexisting mitochondrial myopathy not excluded by blood genetics;
    muscle biopsy, if obtained, shows no mitochondrial pathology".
  - `action-2` RNS to recommended.
  - Add the mediastinum_MRI alternative (normal CT; library normal is consistent).
  - `action-baseline-ecg` recommended.
  - New optional `action-muscle-biopsy` (`order_specialized_test{test_type: muscle_biopsy}`) with
    the D20 stored report.
  - Waste labels: orbit/brain MRI (the differential and evidence that use its atrophy say "if
    obtained"), gait_and_balance_timed, speech_language_evaluation.
  - Contra 2 becomes P1.
  - Must 5 becomes T2, keeping the uncertainty after a long ocular history.
  - Must 4 becomes S1 + S4 (diabetes, BMI) + S5 (ophthalmology before high-dose steroids for
    ocular hypertension; DEXA).
  - Must 3 becomes M1.
  - Must 2 becomes the "consider replacing timolol" wording (D9).
  - G1 (MGFA IIb).
- Class:
  - C3.
  - C11: respiratory to required (choking with liquids).

### MG-RP14
- NB-87M:MG-RP14:policy_verdict: FIXED, one point DECLINED.
  - C14: CBA required, LRP4 recommended separately, CBA added to the stop rule; CENTRAL C2.
  - Add the mediastinum_MRI alternative.
  - `action-baseline-ecg` recommended.
  - RNS and SFEMG stay required.
  - The brain MRI with MRA becomes an optional criterion (`action-brain-mri-aps`,
    `analyze_brain_mri{}`).
  - speech_language_evaluation waste; swallow later (C10).
  - Contra 2 becomes P2.
  - New must: repeat AChR and MuSK at about 6 months, and repeat neurophysiology at a specialised
    centre if the case stays triple seronegative or borderline, with exclusion of mimics (D28).
  - Must 2 becomes M1. Must 3 becomes S2 + S5.
  - Thymectomy sentence per D6.
  - NUDT15 removal: DECLINED (D14, CPIC 2019); TPMT stays first.
- Class:
  - C3.
  - C11: respiratory to required.
  - I1 if rescue IVIG is named (PLEX preferred in APS stays).
  - G1.

### MG-RS11 [APPROVED]
- NB-87M:MG-RS11:policy_verdict: NO-ACTION.
- Class C2 only: `action-2-order-specialized-test` (RNS or SFEMG) to recommended; remove it from
  the stop rule. Nothing else changes (D2, D30).

### MG-RS12
- NB-87M:MG-RS12:policy_verdict: FIXED + CENTRAL (swallow criterion, C1).
  - `action-2` RNS to recommended.
  - `action-7` respiratory to required; add it to the stop rule.
  - `action-baseline-ecg` recommended.
  - Contra 1 becomes P2. Must 4 becomes S2 + S4 (HbA1c 8.1%) + S5 (DEXA). Keep must 5 (glucose).
  - Must 6 becomes R1, with I1 (1 g/kg / 2 g/kg, IBW, hepatitis serology, IgG).
  - Must 2: SLT swallow wording.
- Class:
  - C3.
  - The brain MRI becomes an optional criterion (`action-brain-mri`, the differential already
    says "if obtained").
  - speech waste.
  - M1 in must 3.
  - G1.

### MG-RS13
- NB-87M:MG-RS13:policy_verdict: FIXED.
  - `action-2` RNS to recommended.
  - `action-baseline-ecg` recommended.
  - Waste labels: the third brain/orbit MRI and speech_language_evaluation.
  - Delete contra 1; must 3 carries the ABN generalized rule (target 30 mg, up to 1 mg/kg with
    specialist discussion, worsening at days 5-10) + S4 (cushingoid, BMI 25.5, insulin resistance)
    + S5 (DEXA at 47).
  - Must 6 becomes T1 (47).
  - Must 2 becomes M1, with screening before continued immunosuppression in S5.
- Class:
  - C3.
  - Fix the action-4 rationale and KCE 4 (MGTX).
  - G1.

### MG-RS14
- NB-87M:MG-RS14:policy_verdict: FIXED + CENTRAL (swallow, C1).
  - Scenario per D22: add fatigability to the exam, add the coexisting atypical parkinsonism to
    the differential, remove PSP labels from `rejected` and test with `DiagnosisCriterion.matches`,
    explain the masseter reflex and left upper limb areflexia.
  - MRI report fix and `contrast_used`.
  - Remove the " L" from the respiratory results.
  - `action-brain-mri` optional to recommended.
  - `action-baseline-ecg` recommended.
  - Must 6, the respiratory impression and KCE 3 become R1.
  - Contra 1 becomes P2. Must 3 becomes S2 + S5 (age 75, DEXA), with rituximab screening and
    lamivudine.
  - FcRn antagonist escalation (D22).
  - Must 2 gets I1 (IVIG alternative).
  - Must 7: add "continue levodopa via the nasogastric tube without interruption".
  - Citations per D24.
- Class:
  - C2: RNS to recommended (MuSK 42 nmol/L).
  - C3.
  - C9: waste for gait_and_balance_timed, levodopa_challenge (this admission; must 7 reassesses
    later), speech_language_evaluation, cognitive_screen, neuropsych_battery, muscle_biopsy (done
    last month). The differential cites the exam, not these reports.
  - G1 (MGFA IVb).

### MG-RS15
- NB-87M:MG-RS15:policy_verdict: FIXED + CENTRAL (swallow, C1).
  - `action-2` RNS to recommended.
  - `action-baseline-ecg` recommended.
  - Must 4 becomes T2 (53, "discuss"); fix the action-4 rationale and KCE 4. October Q22 reversed
    (D6).
  - Contra 1 becomes P1. Must 3 becomes S1 + S5 (DEXA at 53).
  - Must 2 becomes M1.
  - Must 5 stays SLT voice and swallow.
- Class:
  - C3.
  - C11: respiratory to required (choking).
  - C9: waste for brain MRI and speech_language_evaluation.
  - G1.

### MG-RS16
- NB-87M:MG-RS16:policy_verdict: FIXED + CENTRAL (swallow, C1).
  - `action-baseline-ecg` recommended.
  - `action-6` drug check optional to recommended (statin).
  - Waste labels: levodopa_challenge, gait_and_balance_timed, speech_language_evaluation, spine
    CT. Harm label: coronary_angiography (D10).
  - New optional `action-brain-cervical-mri` (`analyze_brain_mri{}`).
  - Contra 1 becomes P1. Must 3 becomes S1 + S4 (diabetes, IHD; cite ABN, not Sanders) + S5 (DEXA
    at 73).
  - Must 2 becomes M1.
  - New must: the atorvastatin statement (D28).
  - KCE 4: thymectomy not routine over 65 (ABN; ICG 2020), replacing the MGTX enrolment wording.
- Class:
  - RNS stays required (D2).
  - C3.
  - C11: respiratory to required.
  - G1.

### MG-RS17
- NB-87M:MG-RS17:policy_verdict: FIXED + CENTRAL (swallow, C1).
  - `action-2` RNS to recommended.
  - Must 3 and KCE 3 become T2 at 60 with the Evoli clause; fix the action-3 rationale.
  - Contra 1 becomes P1 (if her dysphagia is significant: P2, with must 2 as S2; worker decides
    and logs).
  - Must 2: 5-10 mg start + S5 (BMI 26.4, family history of diabetes; DEXA at 60).
  - Must 4 becomes R1. Must 1 becomes M1, with an ECG output and criterion.
  - Must 5 swallow wording.
- Class:
  - C3 (+ KCE 2 wording).
  - C11: respiratory to required.
  - C7: fix the action-7 rationale.
  - speech waste.
  - G1.

### MG-S01
- NB-87M:MG-S01:policy_verdict: FIXED + CENTRAL (swallow, C1).
  - `action-2` RNS to recommended.
  - `action-7` respiratory to required; add it to the stop rule.
  - Must 1 becomes T3 (ABN + ICG; oncology).
  - Must 2: IVIG or PLEX on clinical indication, optimum control first, I1 (IBW from her height;
    recompute "125 g").
  - Contra 1 becomes P2. Must 4 becomes S2 + S5 (HPV up to 45).
  - M1, with an ECG output and criterion.
- Class:
  - C3.
  - C7: fix the action-7 rationale.
  - C9: whole_body_FDG_PET and speech waste.
  - G1.

### MG-S02
- NB-87M:MG-S02:policy_verdict: FIXED + CENTRAL (swallow, optional criterion, C1).
  - `action-2` RNS to recommended.
  - `action-1` panels become `[anti_AChR, TSH, TRAb]` (D26).
  - Must 3 and KCE 3 become T1 (29); fix the action-4 rationale.
  - Contra 1 becomes P1. Must 2 becomes S1 + S5 (HPV).
  - Must 1 becomes M1, with an ECG output and criterion.
- Class:
  - C3.
  - C7: fix the action-7 rationale.
  - speech waste.
  - G1.

### MG-S03
- NB-87M:MG-S03:policy_verdict: FIXED + CENTRAL (swallow, C1).
  - `action-2` RNS to recommended.
  - `action-7` respiratory to required; add it to the stop rule.
  - Must 1 becomes T3 (oncology).
  - Must 2: I1, about 146 g at IBW 73 kg (178 cm), hepatitis serology and IgG first, on clinical
    indication with optimum control first.
  - Contra 1 becomes P2. Must 4 becomes S2 + S4 (diabetes, BMI) + S5 (DEXA at 62).
  - Must 3 becomes M1 (metoprolol), with an ECG output and criterion.
- Class:
  - C3.
  - C7: fix the action-7 rationale.
  - C9: whole_body_FDG_PET and speech waste.
  - G1.

### MG-S04
- NB-87M:MG-S04:policy_verdict: FIXED + CENTRAL (swallow, recommended criterion, C1).
  - `action-2` RNS to recommended.
  - Must 4 and KCE 3 become T1 (45); fix the action-4 rationale.
  - Contra 1 becomes P1. Must 2 becomes S1 + S4 (insulin-treated type 1 diabetes; also first choice
    in childbearing potential) + S5 (HPV; DEXA).
  - Must 1 becomes M1, with an ECG output and criterion.
- Class:
  - C3.
  - C11: respiratory to required (dysphagia).
  - C7: fix the action-7 rationale.
  - C9: gait_and_balance_timed and speech waste.
  - G1.

### MG-S05
- NB-87M:MG-S05:policy_verdict: FIXED.
  - `action-3` (RNS or SFEMG) to recommended; keep both alternatives; remove it from the stop rule.
  - Must 2 becomes S3, citing ICG 2020 ocular, not Sanders.
  - Delete contra 1.
  - Must 1 becomes M1, with an ECG output and criterion.
  - S5 (HbA1c and lipids before steroids; monitoring).
  - D27: rewrite contra 3 and the KCE figures.
- Class: G1 (MGFA I).

## 4. CENTRAL requests

- **C1 vocabulary: swallow assessment (blocking for the swallow criteria).** Add to `costs.yaml`
  `perform_clinical_assessment` `by_type: swallow_assessment` (clinical bedside swallow evaluation
  by a speech and language therapist, CPT 92610). Catalogue prose: "oral-motor examination, graded
  water and texture trials, voice and cough after swallowing, aspiration risk and diet texture".
  Add a library normal in `fallback_library.yaml` and the `tool_io.py` mirror. Optional: an
  instrumental term (`order_specialized_test` `videofluoroscopic_swallow_study`, CPT 92611 +
  74230). Keep `speech_language_evaluation` as it is.
  Cases: M01, M02, M04, P01, RP12, RP14, RS12, RS14, RS15, RS16, RS17, S01, S02, S03, S04. Other
  conditions likely to need it: ALS, ISCH-STR, PD (grep their swallow musts).
- **C2 vocabulary: `clustered_MuSK_cell_based`** under `interpret_labs` (send-out, priced like
  `clustered_AChR_cell_based`), with a library normal and the mirror. Cases: P01, RP14, P04.
- **C3 display:** CENTRAL.md items 2 and 3 (M01-M03 row order; stop-rule and constraint display
  for M04, P01, P02, P04, RM11).
- **C4 synonyms (`diagnosis_synonyms.yaml`).** Re-apply with `--prune --conditions
  myasthenia_gravis`, then `--check`.
  - `G70.00: codes: [G70.00, G70.01]` becomes `[G70.00]`. G70.01 stays only for M04, RM14 and RM15
    (D21).
  - Add "AChR antibody positive myasthenia gravis" and "seropositive myasthenia gravis" /
    "seropositive MG", scoped (`cases:`) to the AChR-positive cases: M01, M02, M03, P03, RM11,
    RM12, RM16, RP11, RP12, RP13, RS11, RS12, RS13, RS15, RS16, RS17, S01-S05, and M04, RM14,
    RM15. Do not add them to P01, P04, RP14 or RS14: "AChR antibody positive" tokens appear in
    "AChR antibody negative, MuSK positive".
  - Record the RP13 accepted[0] relabel (D20) as a label change.
- **C5 criteria pack `dataset-generation/criteria_packs/MG.md`** to match D2-D18 and D22-D24.
  - Section 2 tiers: RNS, respiratory, ECG, CBA, LRP4.
  - Section 4: steroid protocols, the prohibition texts P1/P2, thymectomy bands, the 360 mg
    ceiling, R1 replacing the Lawn thresholds, beta-blocker caution, IVIG I1, screening S5.
  - Section 5: constraint reasons Q1.
  - Section 8: add `[Fionda_2026]`, `[Relling_2019]`, `[Virani_2023]`.
  - Also `build_condition_tool_guidance.py` / `condition_tool_guidance.yaml` MG responses (RNS is
    no longer "required in 27") and `test_guidance_claims.py`.
- **C6 generator `conditions.yaml` myasthenia_gravis block:** the same tier changes, so new
  generation does not reintroduce RNS-required, the 20 mg prohibition or "MGTX 18-65".

## 5. Open questions

- NEEDS-ANDREA: none. Every point was decided in `MG-decisions.md`.
- For the orchestrator:
  1. If C1 or C2 cannot land in this round, workers leave the swallow and clustered-MuSK
     criteria for a follow-up pass. The interim forms are given in C10 and C14.
  2. Approved cases RM13, RM14, RM15 (labels only) and RS11 (tier only) go back to re-review.
     The reasons are in D2 and D10.
  3. An MG severity scale term (QMG) is deliberately not requested (D23). A physician may still
     want QMG as an orderable timed examination.

<!-- PLAN COMPLETE -->
