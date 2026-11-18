# FND: condition audit summary (November 2026 round)

Condition auditor, 17 Nov 2026. Scope: the 30 `functional_neurological_disorder` cases and the 73
notes, all from R1 (NB-KSC3-TWUA-QDTM). No FND case is approved (`work/approved.txt` lists none).
Base 06b74446. Plan `plans/FND.md`; decisions `plans/FND-decisions.md`. The audit scripts are in
`/home/aprotani/review-round-2026-11/work/scratch/fnd-auditor/`:

- `notecov.py`: note and ruling coverage, and logs.
- `classes.py`, `classes2.py` and `decisions.py`: the plan applied uniformly.
- `leak0.py`, `ddi.py` and `xmod.py`: the blind leak pass.
- `counts.py` and `beforeafter.py`: tier counts, and counts before and after.
- Fixes: `fix_rp03.py`, `fix_resp.py`, `fix_neuropsych.py`.

## Classes: how fixed, counts at base 06b74446 and now

| class (plan) | measure | before | now |
|---|---|---|---|
| LIT (commit 393c547e) | cases with a literature criterion or stored literature output | 30 | 0 |
| VEEG | video-EEG tier | optional 22 | required 7 (M04 M06 P01 RP01 S05 S06 S11), recommended 11 (M01 M02 M03 RM01 RM03 RP03 RS01 RS03 RS04 S01 S09), optional 0 |
| VEEG | October sentence "Without the recording ..." | 22 | 0 |
| VEEG | rationale and citations canonical ([ILAE_PNES_2013], [AAN_Functional_Seizures_2025]); M-DX wording by tier | n/a | 18 of 18 |
| ECG | ECG tier | optional 10 | required 12 (M01 M02 M04 RM01 RM03 RP03 RS01 S01 S05 S06 S09 S11), recommended 3 (RP01 RS03 and RP02, see below), optional 1 (P08), waste 10 (M05 M06 M09 P07 S07 S10 S02 S03 S04 RS02) |
| ECG | case-specific stored ECG (`initial_tool_outputs.ecg`) | 1 | 16. Every required or recommended ECG is case-specific, the rate is within 5 of the vitals HR, Bazett QTc was recomputed, no template "Normal ECG" remains and the fallback ECG is null |
| ACUTE | required brain MRI / spine MRI | 0 / 0 | 8 (M05 M09 P08 S05 S06 S10 RS04 RS02) / 1 (S07); canonical rationale; DWI stated; mri_probe clean (only M09 has a gadolinium pair, consistent) |
| LABS | required safety labs | 0 | 5 (P08 RM01 RM03 RP02 RS01), "must be measured, not assumed" with source |
| MUST | P08 M1, M09 M3, RM03 M6, RP01 M4, MDT (P01 RP02 RS01), GI (RP02 RS01) | open | all canonical (`decisions.py`); "thrombolysis is not indicated" 1 then 0 |
| RP01 drug check | CYP3A4/CYP2C19 induction of diazepam stated | no | yes |
| ENTRAIN | M03 `tremor_entrainment_positive` | true | false (suppression wording); S06 entrainment throughout, no "stops" |
| DX | S09, S11, RP02 labels | old | new (table below); no "alcohol use disorder" or "somatic symptom disorder" left outside `metadata.revision_reason` |
| DUP | S02, S03, S04, RS02 rewritten to 3.R | 0 of 4 | 4 of 4. Phenotypes: tremor, gait, fixed dystonia, visual loss. Grep for PNES, seizure, levetiracetam, Hoover, EGPA and vasculitis: hits are only the synonym labels (CENTRAL C2) and new-scenario negatives. RS02 metadata cites PMC10416532 and no longer PMC9552981 |
| AVOID | P07 MIBG and levodopa-challenge waste | 0 | 2; both follow-ups last |
| ORDER | criteria order per 2.ORDER | n/a | all 30 (recommended before optional where the plan is silent) |
| STOP | `required_before_assessment` = the required ids, `max_additional_actions` 0 | 30 | 30 (required per case: 1 in 7, 2 in 12, 3 in 7, 4 in 4) |
| Drug check required | | 7 | 5 (M02 RM03 RP01 RP03 RS01) |

Structural checks over the 30 cases found nothing left:
- Every sequence id exists, and no constraint sits on an optional criterion.
- No criterion is matched by an avoided action.
- The musts demand no study that no criterion orders.
- No new em or en dash, apart from the plan's " — " label separator.
- No review-process text in `metadata` beyond the existing `revision_reason` convention.

RP02's recommended ECG is a worker addition not listed in C3. It is justified: ondansetron every
8 h with K 3.3 and Mg 1.5, and the ondansetron labeling advises ECG monitoring with these
abnormalities. It is logged in its verification pass 4.

### Classes found by this audit (not in the plan) and fixed

| class | before | now | cases |
|---|---|---|---|
| Responsiveness over-generalised against the apparent loss of responsiveness that the ECG rests on (the M01 verifier class) | 4 cases (M01 fixed by its verifiers) | 0 | RP01: M-DX, KCE[1], exam rationale, differential. On the stored video-EEG the staring spells do not respond to commands. RS03: KCE, syncope red herring, convulsive-syncope differential. The HPI has her occasionally losing awareness. RM03: cardiac-monitoring waste rationale |
| Management prescription in a drug-check output (kind 1) | 1 | 0 | RP03 summary "withdraw the antiseizure drug and benzodiazepine gradually" became "if they are stopped, ... reduced gradually rather than abruptly" (the M02 form); expected_evidence aligned |
| Template carry-over: identical neuropsychology cognitive values (MoCA 28/30, RAVLT z -0.2, Trail B z -0.4, TOMM 49/50) | 22 cases | 1 (M01 keeps them; the others now have case-plausible normal values) | M02 M03 M04 M05 M09 P01 P08 RM02 RM03 RP01 RP02 RP03 RS01 RS03 RS04 S01 S05 S06 S09 S10 S11. Impressions, mood scores and tiers are unchanged |
| Questionnaire band label wrong | 1 | 0 | M01 GAD-7 15 was "moderately severe"; it is now "severe" (Spitzer 2006). All GAD-7, PHQ-9, PHQ-15, HADS, BDI-II and BAI labels in the condition were checked |

Each change was made through case_io and appended to the case log under '## Verification'.
perfect_agent was re-run on each changed case. No ruling changed, since these are own findings.

## Ruling counts (73 notes)

| status | n |
|---|---|
| FIXED | 72, of which 34 by class LIT (each cites "class LIT, commit 393c547e" and the re-check) |
| DECLINED | 1 |
| ALREADY-FIXED, CENTRAL, NEEDS-ANDREA, NO-ACTION | 0 |

CENTRAL parts sit inside FIXED rulings: C1 on the stop-rule "allow" notes and C2 on the label
changes. Every note id of `notes/FND.json` appears in exactly one `work/rulings/FND-*.json`, with a
valid status. None is missing, duplicated or filed under another case, and every note appears in
its case log. All 30 cases changed since 06b74446, and each has a log with '## Changes'.

## DECLINED and NEEDS-ANDREA

- **DECLINED, FND-RS02 e5a7863c** (refeeding labs). The note is a verbatim copy of the RS01 note
  2cc08f36 (BMI 14.8, nasogastric feeding). RS02 as annotated was a 64-year-old man with BMI 28.3
  and no feeding tube, and the replacement patient has BMI 22.4 and normal electrolytes. NICE CG32
  refeeding monitoring applies only to patients at nutritional risk. The point is applied where
  the data exist: RS01 and RP02, LABS class.
- **NEEDS-ANDREA**: none.
- **For Andrea, as information** (decided, nothing blocking):
  1. The FND construct moves from "examination only" to "examination plus guideline-mandated
     safety tests", following the physician rulings (decisions, final section).
  2. S03 is a test-split case and has been replaced, so any frozen FND-S03 results are stale (C7).
  3. FND-RS03 (record-derived, PMC9937037) states at turn 0 that an outside hospital diagnosed
     "psychogenic seizures", which she doubts. This is the case's scenario and an October red
     herring, whose trap runs both ways: accept the label without examination, or discard it and
     restart an epilepsy work-up. The phrase does not score as a diagnosis on its own (checked with
     `DiagnosisCriterion.matches`). It is kept and is the only turn-0 mention of the condition in
     FND.

## Approved cases changed

None. No FND case is approved.

## Label and code changes (accepted[0]; CENTRAL C2)

| case | before | after | icd_codes[0] |
|---|---|---|---|
| S09 | ... with comorbid PTSD and alcohol use disorder | ... with comorbid PTSD and hazardous alcohol use | F44.7 (unchanged) |
| S11 | ... with comorbid somatic symptom disorder and depression | ... with comorbid depression | F44.7 (unchanged) |
| RP02 | FND (conversion disorder) with weakness and functional gastrointestinal symptoms (intractable vomiting/retching) | FND with functional limb weakness, in severe malnutrition with intractable vomiting under evaluation | F44.4 (unchanged) |
| S02 | FND (conversion disorder) with motor symptoms (right leg weakness) and PNES | Functional neurological disorder — functional tremor of both arms | F44.7 to F44.4 |
| S03 | FND (conversion disorder) with right leg weakness and PNES | Functional neurological disorder — functional gait disorder | F44.7 to F44.4 |
| S04 | FND (conversion disorder) with weakness and PNES | Functional neurological disorder — functional fixed dystonia of the right hand | F44.7 to F44.4 |
| RS02 | FND with psychogenic non-epileptic seizures (PNES) | Functional neurological disorder with functional visual loss (bilateral functional blindness) | F44.7 to F44.6 |

## Leak pass (turn 0 and stored outputs)

- **Turn 0** (`format_patient_info`, rendered for all 30 cases): no accepted label appears,
  case-sensitive acronyms (FND, PNES) included.
  - The hits are bedside signs (Hoover, give-way, entrainment), which the patient exam carries by
    the FND design.
  - Comorbid history: psychogenic polydipsia in RM01 and RM03; established TLE and the MTS MRI in
    M06; MS, the 6-month MRI and the JCV index in M09.
  - The RS03 outside label is discussed above.
  - Prior results that are not scored, or differ from the current one, are legitimate history:
    - P01 outside brain and spine MRI and NCS (no criterion; repeat MRI is waste);
    - RP02 and RS01 outside CT and spine MRI;
    - RM03 ED sodium 129 against the measured 131;
    - outside head CT in M02, M03 and S01;
    - M03 routine EEG against the video-EEG criterion.
  - Numbers in expected_evidence found in the patient text are only the vitals heart rate, which
    the ECG is required to match.
  - No medication indication names the diagnosis.
- **Drug checks** (initial, follow-up and fallback, all 28 cases that store one):
  - None names the diagnosis or repeats another criterion's evidence. Overlaps are only with the
    drug-check criterion's own expected_evidence (kind 2).
  - RM03 cites the desmopressin labeling's "psychogenic polydipsia" contraindication (comorbidity).
  - Each agrees with the medication list and allergies: RP01 induction and the sulfonamide allergy
    against zonisamide; RM01 haloperidol dystonia; S04 no dopamine antagonist; S02 sertraline
    tremor.
  - The one management prescription, in RP03, is fixed.
- **Cross-modality**: no MRI, EEG, ECG, CT, lab or specialised-test report cites another modality
  or the diagnosis. Some outputs carry legitimate kind-2 content, which stays:
  - questionnaire results such as "elevated dissociative experiences" and "high somatic symptom
    burden";
  - gait reports that observe an inconsistent pattern;
  - RS03's EEG ECG channel, which belongs to the EEG montage.

## CENTRAL requests (consolidated)

1. **C1 Review app and harness doc**: say that actions matching a recommended or optional
   criterion never count against `max_additional_actions`. Fifteen FND stop-rule notes read the 0
   as a ban. This is the same request as FEPI-TEMP 4, FTD C3 and CENTRAL.md item 3.
2. **C2 `diagnosis_synonyms.yaml`**: apply the F44 group changes of plan section 4 C2, then re-run
   with `--prune --conditions functional_neurological_disorder` and `--check`.
   - Urgent before any run: the four rewrites still accept the old-scenario labels in
     `accepted[1:]`. A "PNES" answer scores in the tremor, gait, dystonia and vision cases, and
     "functional limb weakness" scores in S02 and S03, where strength is 5/5. S04 accepts
     "functional tremor".
   - New groups: F44+dystonia (S04), F44+gait (S03), F44+vision (RS02, codes F44.6 and F44.4).
   - Test against the mimics: "cortical blindness" must not match RS02, and the dystonia labels
     must be checked against PD.
   - Label changes: the seven in the table above.
3. **C3 Guidance and claims** (`condition_tool_guidance.yaml` FND `our_response`,
   `test_guidance_claims.py`, `criteria_packs/FND.md` sections 2, 3, 5, 6 and 8, `conditions.yaml`
   FND key_findings). Use the counts of the class table, with ECG recommended **3** (RP01, RS03,
   RP02), not 2 as in plan C3. Other counts: brain MRI recommended 4 (M03 P07 RM02 RP03), optional
   8, waste 2 (P01 S02); labs recommended 4 (M05 RP03 S02 S09), optional 4 (M01 M02 M03 M09);
   drug check recommended 8, optional 15; spine MRI optional 2 (M09 S03), waste 3 (P01 RP02 RS01).
   Drop "no instrumental test is required in any case" and "Efficient traces stop after the
   examination", and withdraw October canonical fact 9.
4. **C4 Vocabulary**: LH, FSH and estradiol only if Andrea wants the RP02 endocrine evaluation
   scored; it is a must until then. TSH is a priced panel: S02's criterion is served the TSH panel
   (verified by the S02 verifier's probe).
5. **C5 Pack allow-list**: Nicholson 2020, the Joint benzodiazepine tapering guideline 2025, WHO
   AUDIT (Babor 2001), Schrag 2004, Pozuelo Moyano 2023, NICE CG32 as a key, Bhatia 2018 (MDS
   tremor consensus, S02), Bruce and Newman 2010 (RS02) and Spitzer 2006 (GAD-7 bands).
6. **C6 `test_case_guards.py` banned strings**: "thrombolysis is not indicated" (FND now 0; still
   in ISCH-STR-RP02 for its lead) and "slowly over weeks" for a benzodiazepine taper. Suggested
   new guard: identical neuropsychology cognitive values across cases of one condition.
7. **C7 Splits**: FND-S03 (test) is replaced, so frozen test results for it are stale.
8. **C8 `agent-platform/config/tools/library_contradictions.yaml`**, FND `cases.FND-RS02`: delete
   the `emg_ncs`, `skin_biopsy_iencf` and `interpret_labs {panels: [HbA1c]}` entries, which come
   from the old scenario. The new patient has normal limbs, so a library-normal EMG or skin biopsy
   is consistent, and HbA1c is served by the stored labs. This is the only failing FND case guard.
   Re-derive the S02, S03 and S04 entries for the new scenarios. They pass today, because each
   stores its own gait, performance-status and neuropsychology reports, but they were written
   for the old cases.
9. **Cross-condition** (from decisions 3): the TLoC ECG question plausibly exists in SE,
   FEPI-TEMP and SYNC-CARD; their leads should check.

## Check results (17 Nov 2026, after the audit fixes)

- `perfect_agent.py <id>`, one call per case: 30 of 30 pass, with no warning.
- `pytest test_case_guards.py -k "FND-"`: 239 passed, 1 failed. The failure is
  `test_library_never_answers_a_contradicted_order[FND-RS02]`, from the stale config entries of
  CENTRAL 8, not a case-file error.
- `apply_diagnosis_synonyms.py --check --conditions functional_neurological_disorder`: would
  change 0 of 600 cases.
- `pytest test_panel_case_contract.py test_red_herring_paths_resolve.py`: 4 passed.
- `pytest test_guidance_claims.py`: fails. These are the stale FND claims, all the intended effect
  of the tier changes (CENTRAL 3); the app says one thing, the cases now say another:

  | claim | app | cases |
  |---|---|---|
  | `fnd/video-EEG optional in 22` | 22 | 0 |
  | `fnd/video-EEG never required/recommended` | 0 | 18 |
  | `fnd/brain MRI recommended 12 optional 9` | (12, 9) | (4, 8) |
  | `fnd/spine MRI recommended in 1` | 1 | 0 |
  | `fnd/labs recommended 8 optional 4` | (8, 4) | (4, 4) |
  | `fnd/ECG optional in 10` | 10 | 1 |
  | `fnd/no instrumental required` | 0 | 35 |
  | `fnd/medicine review required in 7` | 7 | 5 |

  The guidance files were not edited.
- `mri_probe.py` over the 30 cases: only M09 has gadolinium text, and it is a consistent pair
  (plain `contrast_used: false`, gadolinium follow-up `true`).
