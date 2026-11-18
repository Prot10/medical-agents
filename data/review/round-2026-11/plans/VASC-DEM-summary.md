# VASC-DEM: condition audit summary (November 2026 round)

Condition auditor, 17 Nov 2026. Scope: the 30 cases VASC-DEM-M01..M10, P01..P09 and S01..S11, and
the 75 notes in `notes/VASC-DEM.json`. All 75 come from R1 (NB-KSC3-TWUA-QDTM); R2 left none.

- No VASC-DEM case is approved (`work/approved.txt` lists none).
- Base: 06b74446. Plan: `plans/VASC-DEM.md`, decisions D1-D18 in `plans/VASC-DEM-decisions.md`.
- Audit scripts, in `/home/aprotani/review-round-2026-11/work/scratch/vascdem-auditor/`:
  - `notecov_vd.py`: note and ruling coverage.
  - `classes_vd.py`, `classes2_vd.py`, `canon_vd.py`: the plan applied uniformly.
  - `reach.py`: which stored follow-up each single-parameter call reaches, and whether that call is
    credited, labelled or neither.
  - `leak_vd.py`, `report_scan_vd.py`, `ddi_dump.txt`: the blind leak pass.
  - `counts_vd.py`: counts before and after.
  - `fix_stragglers.py`: the audit's fixes.

## Classes: how fixed, counts at base 06b74446 and now (30 cases)

| class (plan) | measure | before | after |
|---|---|---|---|
| C1 TIER-GAIT (D1) | timed-gait criteria that are required / in the stop rule | 7 / 7 | 0 / 0. Recommended in 10 cases; optional in M01, where gait is normal |
| C2 TIER-NEUROPSYCH (D2) | required batteries | 11 | 1 (P07, required by design, D2). The other 10 are recommended and out of the stop rule |
| C3 TIER-BIOMARKER (D3) | required amyloid, FDG or NOTCH3 criteria | 7 | 1 (P05 NOTCH3, which is the diagnosis). M05, M07, P01, P02 amyloid and P06 NOTCH3 are recommended; M08 amyloid and P02 FDG are optional |
| C4 ECG-AETIOLOGY (D4) | required ECG criteria | 7 | 11 (M04, P09, S09, S01 added, each in the stop rule). M04 cervical vessels are required. M04, P09 and S09 carry the conditional echo/monitoring must |
| C5 STOP-RULE | stop-rule ids, summed | 133 | 115. In every case the stop rule equals the set of required criteria |
| C5 CAROTID-ALT (D5) | duplex-only carotid criteria | 7 | 2, both by design: P08 (MR unsafe) and S08 (separate MRA criterion) |
| C6 NP-CUTOFF (D6) | percentile rows at the 9th-24th flagged "yes" / rows off the AACN range and flag | 43 / 187 | 0 / 0 (187 rows checked) |
| C7 LACUNE-COUNT (D7) | stated count differs from the sites listed | 3 (S03, S05, P06) | 0. S03 lists 8 sites, S05 7, P06 9 |
| C8 DX-CERTAINTY (D8) | `accepted[0]` set to the D8 strings | 0 of 7 | 7 of 7 (table below) |
| C8 IMG-SUFF | "requires a confluent burden", "independently sufficient", "cannot explain a dementia" | 9 | 0. Kept: S10 kce4 (consistent) and the trap descriptions in the M01/P08 red-herring `intended_effect` |
| C10 UNSOURCED-RULE (D11) | fixed systolic 120 mmHg floor | 4 | 0 |
| C11 ON-REQUEST (D12) | follow-ups matching no criterion and no avoided action (lead's `onrequest.py`) | 233 | 56 |
| C12 AVOIDED-SOFTEN (D13) | P03 EEG waste, S11 monitoring waste, M03 monitoring waste | 3 | 0. P03 has an optional EEG with its stored routine EEG; S11 has an optional 30-day monitor (`event_monitor_30d`, 720 h). P04 keeps its EEG waste label |
| C13 INTERPRETER (D14) | M09 tested via family interpretation | 1 | 0 (Mandarin-speaking examiner, Chinese norms) |
| D11/D16 canonical musts | case-specific canonical phrases (checked in 26 cases); stale phrases absent | open | all present, except M06 furosemide (worded "Review furosemide, started for postoperative fluid management, with cardiology", same content). No stale phrase left |

C11 details:
- The 56 follow-ups that stay unlabelled are all exceptions in the plan's table: gait,
  speech-language, EMG with neuropathy, polysomnography, respiratory function, orthostatic BP,
  visual fields, headache history, TCD, carotid-stenosis catheter angiography in M10, P08, S08 and
  S11, TEE in P08, S08 and S11, and the M03 cardiac MRI, battery and gait.
- Avoided labels went from 197 to 352 (net; three labels were removed under C12). Harm labels went from 3 to 17, with the severities
  of the table: EP study, catheter angiography, coronary angiography, the M03 contrast studies, and
  the P08 MR modalities.
- `reach.py` confirms that every follow-up is reached by its own term.
  - Credited follow-ups come first in every case. The P05 and P06 young-SVD labs and the S04 MMA
    are credited through their recommended criteria.
  - No call is matched by both a criterion and an avoided action. This also holds for optional
    criteria, which perfect_agent does not test.

Structural checks found nothing wrong:
- Every sequence and stop-rule id exists. `max_additional_actions` is 1 throughout.
- No RPR/HIV change (P06 keeps them: past cocaine use, October rule).
- The rejected lists of M06, M07 and M08 changed with D8/D9:
  - "cardioembolic" removed in M06, M07 and M08;
  - "multi-infarct dementia" rejected in M07 and M08.
- No em or en dash in any new text: every hit is base prose.
- `metadata` changes are teaching points, difficulty rationales and the P08 exemption text only. None
  is review-process text.
- New citation keys: `[VasCog2_WSO_2025]` (17 cases), `[AHA_LV_thrombus_2022]` (M03),
  `[EAN_monogenic_SVD_2020]` (P05), `[HRS_MRI_CIED_2017]` (P08) and `[NICE_CG115]` (M02). They
  await the pack allow-list (CENTRAL 4). `[AACN_labels_2020]` is not cited in any case.

## Ruling counts (75 notes)

| status | n |
|---|---|
| FIXED | 67 (some with a CENTRAL display or label remark in "what") |
| ALREADY-FIXED | 5: f569e1c8 (P05), 6331cc50 (S06), 2c6f29cf (S07), f33e4140 (S08), 77ee2163 (S11). Each stop-rule id already names its study (`genetic_panel:CADASIL`, `carotid_duplex`, `event_monitor_30d`, `MR_angiography`); the display is CENTRAL.md item 3 |
| CENTRAL | 3: e8dbcb56 (M09) and dc877a4d (P07), both a flag read off the next row (data checked correct, CENTRAL.md item 2); 88d4951c (P02), where the case side is done (dd1, must 0) and the synonyms are pending |
| DECLINED | 0 |
| NEEDS-ANDREA | 0 |
| NO-ACTION | 0 |

Coverage:
- Every note id appears in exactly one `work/rulings/VASC-DEM-*.json`, filed under its own case,
  with a valid status. No ruling is missing, duplicated or extra.
- Every note appears in its case log.
- All 30 cases changed since 06b74446, and each has a log with a non-empty '## Changes'.
- No VASC-DEM note concerns literature (class LIT), and no literature criterion or output remains.

## DECLINED and NEEDS-ANDREA

None. Three points are decided but flagged for the re-review (plan section 5):
- **P07** keeps the battery required against the class rule (D2): the screen is normal, and the
  battery is the only objective evidence.
- **P08** keeps MRI as harm, with R1's conditional rationale (D13, HRS 2017).
- **M09 e8dbcb56** was ruled on the most likely reading of "48 false??", a flag read off the next
  row. If Andrea can ask R1, confirm that the note meant nothing else.

## Approved cases changed

None. No VASC-DEM case is approved.

## Label and code changes

Only `accepted[0]` changed. Every `icd_codes[0]` and every synonym label after `accepted[0]` is
unchanged (checked against base).

| case | before | after |
|---|---|---|
| M01 | Mild vascular cognitive impairment (mild vascular cognitive disorder) due to moderate cerebral small-vessel disease; the threshold for vascular dementia is not met | Mild vascular cognitive impairment (mild vascular cognitive disorder), most likely due to moderate cerebral small-vessel disease; the threshold for dementia is not met |
| M02 | ... from untreated hypertension, with a coexisting alcohol-related cerebellar syndrome ... | ... from untreated hypertension, with a possible alcohol-related contribution to the cognitive decline and a coexisting alcohol-related cerebellar syndrome ... |
| M06 | Vascular dementia due to global hypoperfusion: bilateral cortical and internal border-zone infarction sustained during prolonged perioperative hypotension at aortic valve replacement | Vascular dementia after perioperative border-zone infarction: ... predominantly haemodynamic, with perioperative embolism not excluded |
| M10 | ... two coexisting mechanisms, cardioembolism from untreated atrial fibrillation and severe symptomatic right internal carotid stenosis with a haemodynamic component | ... two coexisting potential stroke mechanisms, untreated atrial fibrillation and severe symptomatic right internal carotid stenosis |
| P06 | ...; CADASIL excluded | ...; CADASIL unlikely and not genetically confirmed |
| P08 | ... from symptomatic left internal carotid stenosis with coexisting paroxysmal atrial fibrillation documented on pacemaker interrogation; diagnosed on CT because MRI is contraindicated | ... with two coexisting potential mechanisms, left internal carotid atherosclerosis and device-detected paroxysmal atrial fibrillation; diagnosed on CT because MRI could not be performed safely |
| S08 | ... from severe symptomatic right internal carotid stenosis, ... | ..., most likely from severe right internal carotid stenosis, ... |

`apply_diagnosis_synonyms.py --check --conditions vascular_dementia` reports 0 changes.

Noted, not changed: the M07 and P01 labels say "biomarker-confirmed Alzheimer pathology" while
the amyloid criterion is now recommended.
- The labels describe the case's stored CSF and PET results.
- Scoring goes through the synonyms, so an agent that never orders a biomarker still scores.
- Rule 3 forbids changing `accepted[0]` without a reviewer ruling that the label is wrong, and no
  note asks for one.
- If the labels should read "Alzheimer pathology (biomarker-supported)", that is a re-review
  question.

## Leak pass (turn 0 and stored outputs)

**Turn 0** (`format_patient_info`, rendered for all 30 cases):
- No case names its own diagnosis. The label hits are all legitimate:
  - P01: family history ("father had vascular dementia");
  - M04: the patient's fear of Alzheimer disease, which is the mimic;
  - M05, M09, P07, S04, S10: dated lacunar stroke events or a relative's stroke.
- Prior results kept, because none of them is the decisive result of a criterion:
  - M03: an old ECG infarct, three years ago, is the premise; the decisive TTE result is not given.
  - S10: the admission ECG, telemetry and duplex are history, and S10 has no ECG or vessel
    criterion.
  - S03 eGFR 38 and P06 LVH on an old echo are chronic background.
- P02 keeps "referred after an MRI performed for headache showed extensive white matter change".
  - This is the case's referral red herring, and it points away from the answer.
  - The required MRI adds what decides the case: posterior atrophy, MTA, the lacunes and the
    microbleeds.
- Medication indications name no diagnosis.

**Drug checks** (initial, follow-up and fallback, all cases):
- None repeats an expected_evidence string.
- Each agrees with the medication list and allergies: M03 aspirin with warfarin or DOACs, M05
  gliclazide with perindopril, M07 bisoprolol, M08 diltiazem, M10 aspirin, P04 reduced-dose
  apixaban, P09 zolpidem, S05 apixaban dose, S06 and S07.
- P04's apixaban warning lists a high microbleed burden among the generic risk factors for
  intracranial bleeding. It is kept: this is label-style text and it does not say that the patient
  has microbleeds.

**Cross-modality and kind 1** (initial, follow-up and fallback reports):
- No report names the diagnosis except the genetic reports: P05 establishes CADASIL and P06 says
  the result does not support it. Both are kind 2.
- No report cites another modality. The hits are "CSF-signal" spaces and cardiac MRI "imaged in
  atrial fibrillation", both observed in the same study.
- No report gives management.

## Stragglers fixed by the audit (through case_io, logged under '## Verification')

1. **S01, S02, S03, S05** `avoid-waste-levodopa-challenge`, and **S04** the levodopa, SSEP and
   skin-biopsy labels: removed `[VASCOG_2014]`.
   - It does not support these rationales, and the plan's C11 table gives them no citation.
   - The label is uncited in the other 19 cases.
   - The P05 and P06 verifiers removed the same citation and flagged S01-S05 for the lead.
2. **P06** `patient.chief_complaint`: removed "and a severe white matter burden".
   - It gave at turn 0 the decisive result of the required MRI.
   - No prior scan in the history explains it.
3. **P05** `initial_tool_outputs.drug_interactions.sumatriptan.warnings[0]`: the pass-1 text
   "Cerebral small-vessel disease without a previous stroke or TIA is not itself a labelled
   contraindication" volunteered the diagnostic class to an agent that checks sumatriptan before
   the MRI or NOTCH3.
   - It now reads: "Previous transient focal deficits are a labelled contraindication whether they
     were ischaemic events (stroke or transient ischaemic attack) or hemiplegic aura, so the history
     decides for the individual patient."
   - The matching clause is dropped from `action-8-check-drug-interactions.expected_evidence`.
   - The c7d6ad9b ruling was updated.

All seven cases pass perfect_agent and the case guards afterwards. `case_io.py check` on them:
schema and synonym guard OK, and no test failure names them.

## CENTRAL requests (consolidated)

1. **Review app** (`web-review/src/components/cases/CaseDetail.tsx`):
   - Show the follow-ups that match no criterion in a separate block, "Answered on request (not
     part of the pathway)", after the pathway steps. Notes: 74a16658, 2f5910a5, 75e30bee, 57709b24,
     fa0764bd, dd0174a0, db0cbe3b.
   - Print the label keys (`test`) before `abnormal`/`value`, and null as "not stated" (CENTRAL.md
     item 2; e8dbcb56, dc877a4d).
   - Show the stop-rule criterion with its arguments, not only its id (CENTRAL.md item 3;
     f569e1c8, 6331cc50, 2c6f29cf, f33e4140, 77ee2163).
2. **Synonyms** (`diagnosis_synonyms.yaml`):
   - For VASC-DEM-P02 only, accept "posterior cortical atrophy small vessel disease", "alzheimer
     small vessel disease" and "alzheimers small vessel disease" (88d4951c).
   - Check them under scorer v2 against the P02 rejected list and against AD-only answers. Then
     re-apply with `--prune --conditions vascular_dementia`.
   - The label changes above (M01, M02, M06, M10, P06, P08, S08) are for the record. They change no
     scoring.
3. **Library**: none.
4. **Criteria pack** (`dataset-generation/criteria_packs/VASC-DEM.md`): the tiers, rules and
   allow-list keys in plan section 4 item 4. The six new keys are listed there; five are used in
   the cases.
5. **Guidance** (`condition_tool_guidance.yaml`): VASC-DEM has no entries, so there is nothing to
   update.
6. **Guard suggestion** (tests): a stored invasive follow-up that matches no criterion must carry an
   avoided label. The studies are EP study, catheter, cerebral or coronary angiography, and
   levodopa challenge. Plan item 6 has the dataset-wide counts; now 2820 uncredited and unlabelled
   follow-ups remain in 547 cases, 56 of them in VASC-DEM, all by design.
7. **Cross-condition**: one percentile convention for the dementia conditions. VASC-DEM uses the
   AACN 2020 labels; ALZ-EARLY flags the 9th-24th band "yes" (plan item 7).
8. **MockServer** (`mock_server.py`, observation, pre-existing; S06, S07, S11 logs):
   - An echo order without `echo_type` (schema default TTE) is served the stored TEE follow-up.
   - An explicit TTE order gets the case's TTE fallback instead.
   - The default should take the TTE answer. As it stands, an untyped order receives a TEE report
     that no TEE waste label penalises, because those labels require `echo_type: TEE`.

## Check results

| check | result |
|---|---|
| `perfect_agent.py <id>`, one call per case, all 30 | 30/30 pass, no warnings; re-run after the audit fixes |
| `pytest test_case_guards.py -k "VASC-DEM-"` | 240 passed |
| `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` | 0 of 600 would change |
| `pytest test_panel_case_contract.py test_red_herring_paths_resolve.py` | 4 passed |
| `pytest test_guidance_claims.py` | fails on FND, MIG and PD claims only; no VASC-DEM claim exists, so none went stale |
| `case_io.py check` on the 7 cases edited by the audit | schema OK, synonym guard OK, no failure names them (2 unrelated failures elsewhere) |
