# SYNC-CARD-S02
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, `initial_tool_outputs.drug_interactions.general` | Literature finding and summary equal to the expected_evidence (leak guard failure); drug block was the bare text "Hold AV-nodal blockers", the key of the drug criterion. | FIXED: both deleted; one ESC 2021 pacing / ESC/EACTS 2021 guideline follow-up added last. |
| E | major | `fallback_tool_outputs.literature_search`, `fallback_tool_outputs.drug_interactions.general` | "No directly applicable ... evidence"; "(agent not specified on this case's pathway)". | FIXED: literature fallback deleted; drug fallback is a `medication_list_review` (amlodipine, losartan and tamsulosin lower blood pressure in severe AS; losartan and potassium; metformin dose at eGFR 30-45; cephalosporin allergy and cefazolin). |
| C | major | `action-6-search-medical-literature`, `action-5-check-drug-interactions` | Literature recommended; drug check recommended with no drug while he takes no AV-nodal blocker. | FIXED: literature optional (canonical rationale); drug check optional (plan B) with alternatives amlodipine, losartan and one follow-up each. |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin; expected_evidence generic. | FIXED: recommended `panels: [BMP]`; expected_evidence K 5.3 on losartan, creatinine 1.8. |
| B | minor | `initial_tool_outputs.labs.panels.BMP` | Sodium 146 with chloride 104 and CO2 23 (gap 19), unexplained hypernatraemia. | FIXED: sodium 140; summary and interpretation updated ("indices suggesting iron deficiency" interpretation removed). |
| B | minor | `patient.vitals.hr` | HR 45 while the ECG escape is 32 bpm and telemetry never exceeds 40. | FIXED: 33. |
| B | major | `initial_tool_outputs.ecg` | "Low-voltage QRS in limb leads" alongside LVH by voltage (contradictory, and an unintended amyloid flag); right axis with an LBBB escape; "increasing risk of polymorphic VT" interpretation. | FIXED: low voltage removed, normal axis, interpretive clause removed. |
| D | minor | `initial_tool_outputs.eeg.limitations` | "a non-epileptic etiology is favored" (cross-modality conclusion). | FIXED: removed. |
| B | major | `followup_outputs` CT, `patient.neurological_exam.additional` | CT reported a right temporal scalp haematoma while the HPI has him landing on his right side and the exam records only hip tenderness; no NG232 criterion. | FIXED: exam states no scalp wound; CT is a normal non-contrast report kept as an off-pathway answer; head CT avoided as waste. |
| B | major | `followup_outputs[0]` (echo) | Lab-style fields, no echo_type, TAPSE, stroke volume, wall motion. | FIXED: full TTE report (Vmax 4.3 m/s, mean 42 mmHg, AVA 0.9 cm2, annular calcification, LVEF 40% global hypokinesis, septum 1.4 / PW 1.3 cm, TAPSE 16 mm, PASP 48 mmHg), no diagnosis sentence. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | 24 h Holter during "wheelchair transport" (an inpatient) under a telemetry label pinned to holter_24h; "frequent PVCs, 0.5%" for 186 beats (0.4%). | FIXED: alternatives telemetry, holter_24h, holter_48h; output "Inpatient telemetry, 24 h" with S02's own rates kept (26-40, average 34, 5.8 s pause at 02:18), near-syncope at 28 bpm added; same recording as the fallback. |
| D | minor | `followup_outputs` CMR | "consistent with reactive fibrosis at the conduction system level", "no features of infiltrative cardiomyopathy" interpretations; LVEDV 185 mL called increased. | FIXED: findings-only impression; CMR optional (age 74). |
| C | major | `followup_outputs` tilt and exercise, `avoided_actions` | Tilt performed in severe AS; exercise report "not performed" stored as a result; exercise not avoided. | FIXED: both follow-ups deleted; tilt and exercise test avoided as harm (severe symptomatic AS). |
| H | minor | all `action_criteria[*]` | "ESC 2018 §x", "Locati 2014" citations; rationale equal to label. | FIXED. |
| A | minor | `stop_rule`, `sequence_constraints` | `max_additional_actions: 0`; no constraints. | FIXED: 2; soft ECG before TTE and before monitoring. |
| C | major | `ground_truth.assessment` | No valve-intervention must; "Restage AS on echo" (a scored test) and "Hold AV-nodal blockers" (he takes none); no handling of vasodilators with BP 94/55, of the cephalosporin allergy at device implantation, or of the microcytic anaemia; tilt prohibition (a test). | FIXED: musts are diagnosis (CHB plus severe AS), monitored bed with pacing pads, permanent pacing with CRT or conduction-system pacing considered at LVEF 40%, Heart Team TAVI or SAVR, hold amlodipine and tamsulosin and review losartan, non-cephalosporin device prophylaxis, investigate the microcytic anaemia, driving. Prohibitions: AV-nodal drugs before pacing, vasodilators, discharge before pacing, cephalosporin prophylaxis. |
| C | major | `ground_truth.differential` | VT moderate after telemetry; SSS cited SNRT/EP study (not on the pathway); severe AS "may be under-staged" although the echo stages it. | FIXED: AS moderate (contributing mechanism, staged), VT and SSS low with the telemetry evidence. |
| L | minor | `ground_truth.red_herrings` | field_path without index; data_point not quoted. | FIXED: point to `past_medical_history[1]` and the ECG interpretation with quoted text. |
| E | minor | `ground_truth.key_clinical_evidence`, `metadata` | Tilt-only evidence; difficulty rationale with 4-5 required tools. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The 74-year-old man with exertional syncope on the stairs has complete AV block with a wide LBBB-morphology escape at 32 bpm and severe calcific aortic stenosis (AVA 0.9 cm2, mean gradient 42 mmHg, Vmax 4.3 m/s, LVEF 40%). Required: ECG, TTE and inpatient telemetry (Holter accepted: persistent block, escape 26-40 bpm, near-syncope at 28 bpm, a 5.8 s pause, three brief NSVT runs). BMP is recommended (K 5.3 on losartan, creatinine 1.8; the impossible sodium was corrected). CMR, the medication review and the guideline lookup are optional. Tilt and exercise testing are harm; EEG, brain MRI, CSF and head CT are waste (he did not strike his head; the CT's scalp haematoma was removed and the exam now says so). Musts: diagnosis of both mechanisms, monitored bed with pacing pads, permanent pacing with CRT or conduction-system pacing considered at LVEF 40%, Heart Team TAVI or SAVR, hold amlodipine and tamsulosin and review losartan, non-cephalosporin device prophylaxis, work-up of the microcytic anaemia, driving.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms and R55 still accepted; not hand-edited.
- Plan C3: an off-pathway tilt or exercise order gets the library's normal report; both are avoided as harm here, and the case's tilt report was deleted per the plan.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Decisions taken: head CT made waste rather than kept with an unexplained scalp haematoma (no head strike in the history or exam); microcytic anaemia added as a must because it changes the pre-TAVI plan and the case left it unaddressed.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Read the full final case against the log and plan.
- Checked: ECG 32 bpm vs vitals 33 vs telemetry 26-40; anion gap 13; Hb/Hct ratio; metformin 1000 mg/day at eGFR about 39; echo AS grading (AVA 0.9, mean 42, Vmax 4.3, SVi 36) consistent with the expected_evidence, differential and musts; CMR LVEF 40% from 185/111 mL; exam now records no scalp wound, so head CT as waste holds (no head injury, NG232 not engaged); cephalosporin allergy vs device prophylaxis must; harm entries for tilt and exercise; red-herring paths; leak guard passes.
- Found and changed:
  - Template carry-over: the CMR native T1 "1120 ms" is RS02's value (plan M: never copy a number from a sibling case). Set to 1085 ms in the finding signal and the impression (both occurrences).
  - Driving must allowed Group 1 driving 1 week after pacing although the severe symptomatic aortic stenosis, a structural cause of this exertional syncope, is still untreated. ESC 2018 driving advice for structural cardiac disease is "until successful treatment is established". The must now restricts driving until the pacemaker is implanted and the aortic stenosis has been treated.
- perfect_agent -v and case_io check clean after the changes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Drug follow-ups and the fallback medication review: removed, where present, wording that asserted results the agent has not obtained ("while AV conduction disease is unpaced", "meets the labelled dose", device-implantation warnings, the eGFR-specific metformin line, cefazolin "for device implantation"). Each is now a conditional rule (e.g. contraindicated in second- or third-degree AV block without a pacemaker; apixaban 5 mg unless two of age 80 or over, weight 60 kg or less, creatinine 1.5 mg/dL or more; anticoagulation advice if a device is implanted). Why: a drug check must not disclose the conduction diagnosis or the management decision.
- `initial_tool_outputs.drug_interactions` set to the medication-list review (copy of the fallback). Why: without it, tier 2 answered an unrelated drug (probe: ibuprofen) with the first per-drug follow-up.
- Added "not performed" follow-ups for `tilt_table` and `exercise_stress_test` (RM04/RP02 format, "Deferred by the clinical team"). Why: otherwise the library returned a normal tilt (HR 68) or a normal exercise test (10.4 METs) in a patient with high-grade AV block, contradicting the case; both orders stay penalised as in the plan.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Valve guideline: ESC/EACTS 2025 (Praz 2025) replaces 2021; TAVI is now favoured from 70 years in tricuspid AS, so the Heart Team must states that at 74 with a trileaflet valve TAVI is favoured if transfemoral access is feasible; literature result updated.
- Labels: complete heart block labels only (Mobitz II and second-degree labels removed: a different grade); I44.30 kept, I44.1, I44.39, I45.9 and R55 dropped.
- "ESC/EACTS 2021" renamed "ESC/EACTS 2025" (2025 ESC/EACTS valvular guideline, Praz 2025, supersedes 2021): `.ground_truth.action_criteria[2].rationale`, `.ground_truth.action_criteria[5].rationale`, `.ground_truth.assessment.required_recommendations[3]`, `.ground_truth.avoided_actions[2].rationale`.
- Literature follow-up: Vahanian 2021 source replaced by Praz 2025 and the TAVI age threshold 75 by 70 years (tricuspid AS, transfemoral access feasible); evidence level written as "Class I" only.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_EACTS_2025_VHD]']; action-8-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; action-5-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_EACTS_2025_VHD]']; avoid-harm-2-exercise-stress-test citations ['[ESC_2018]'] -> ['[ESC_EACTS_2025_VHD]']; avoid-waste-4-order-ct-scan citations [] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-S02` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure 'Active stand test not performed. Deferred by the clinical team.' (haemodynamically unstable or high-grade AV block at presentation: standing is not safe); no criterion |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

| field path | change |
| --- | --- |
| `followup_outputs[10]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-8-order-advanced-imaging` label: "Cardiac MRI to characterise the myocardium (optional)" -> "Cardiac MRI to characterise the myocardium"
- criterion `action-5-check-drug-interactions` label: "Review the medication list (vasodilators) (optional)" -> "Review the medication list (vasodilators)"
- criterion `action-6-search-medical-literature` label: "Guideline lookup on pacing and valve intervention (optional)" -> "Guideline lookup on pacing and valve intervention"
