# SYNC-CARD-M04
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `followup_outputs` drug check (`request_drug_interactions`) | Its contraindication text repeated the drug criterion's expected_evidence (leak guard failure). | FIXED: replaced by three per-drug follow-ups (`check_azithromycin`, `check_ondansetron`, `check_citalopram`) and a `medication_list_review` in `initial_tool_outputs.drug_interactions` and the fallback. |
| C | major | same | Wrong pharmacology: citalopram + ondansetron and citalopram + azithromycin called "CONTRAINDICATED per manufacturer labeling" (labelling advises against or monitoring, it does not contraindicate); domperidone offered as an antiemetic alternative (itself QT-prolonging); fluoxetine offered as a low-QT SSRI. The real interaction in the list, omeprazole inhibiting CYP2C19 and raising citalopram exposure (label maximum 20 mg with CYP2C19 inhibitors and over 60), and PPI hypomagnesaemia were missing. | FIXED: severities [MAJOR] with labelling-accurate wording; omeprazole interaction and PPI hypomagnesaemia added; serotonin syndrome risk of citalopram + ondansetron added; alternatives limited to doxycycline (penicillin allergy) and sertraline. |
| A | major | `action-3-check-drug-interactions` | No drug named. | FIXED: alternatives azithromycin, ondansetron, citalopram (plan B); placed straight after the ECG with a soft ECG-before-drug-check constraint. |
| D/C | major | `followup_outputs` literature, `action-6-search-medical-literature` | Required literature step; the ESC 2018 entry contained the tool name "Check_drug_interactions" and an invented "medication review is mandatory" claim; Drew 2010 given a wrong title and a potassium target of 4.0-4.5 (the statement says 4.5-5.0). | FIXED: optional, canonical rationale; output rewritten with the real Drew 2010 title and content (Mg 2 g, K 4.5-5.0, pacing or isoproterenol, monitor until QTc < 500 ms) and ESC 2022; follow-up last. |
| C | major | `action-2-interpret-labs`, `initial_tool_outputs.labs.panels.Metabolic` | Beta-hCG pinned and reported in a 60-year-old woman (template carry-over); CBC and troponin pinned. | FIXED: `panels: [BMP, magnesium]`; beta-hCG deleted from the panel and interpretation; TSH kept in the output (treated hypothyroidism) and accepted as an extra. |
| C | major | `followup_outputs` telemetry, `action-4-order-cardiac-monitoring.expected_evidence` | The report showed QTc shortening to 480 ms "coinciding with electrolyte repletion and drug discontinuation": the effect of management the agent has not yet recommended (ruling 4). Also an outpatient diary and event button on inpatient telemetry, an episode at 02:14 with the patient awake and reporting, and max HR 172 while torsades ran at 230. | FIXED: trend removed (QTc 520-545 ms throughout); symptom reported to the nurse; first episode at 22:14; HR range 58-230; alternatives telemetry, holter_24h, holter_48h; same recording as `fallback_tool_outputs.cardiac_monitoring`; expected_evidence rewritten. |
| C | major | `sequence_constraints[0]` | Hard labs-before-monitoring constraint (delays Class I monitoring in torsades). | FIXED: deleted; soft ECG before drug check, before TTE and before monitoring. |
| A | minor | `stop_rule` | Included the literature criterion; `max_additional_actions: 0`. | FIXED: the five required criteria; 2. |
| B | minor | `initial_tool_outputs.ecg` | QT 500 ms at 68 bpm gives a Bazett QTc of 532, not 540. | FIXED: QT 506 ms (QTc 540 ms); QT added to intervals. |
| B | minor | `patient.clinical_history.medications[2]` | Ondansetron "started 4 days ago" vs HPI "two to three days ago". | FIXED: "started 3 days ago". |
| D | minor | `patient.history_present_illness` | Reasoning clause "raising concern for possible electrolyte losses"; em dashes. | FIXED: clause deleted; dashes replaced (also in `neurological_exam.additional`). |
| B | minor | `followup_outputs` echo | No echo_type, TAPSE or LA index. | FIXED: added; impression in echo voice. |
| C | minor | `action-8-analyze-eeg` | Expected "Normal EEG ... supports convulsive syncope" (an interictal EEG cannot support it). | FIXED: optional EEG with an ESC 2018 Class III rationale; expected_evidence neutral. |
| C | minor | `avoided_actions` | Head CT not addressed despite an occipital head strike at 60 without an NG232 criterion. | FIXED: CT waste added (NICE NG232); MRI, CSF and tilt rationales name the diagnosis. |
| C | major | `ground_truth.assessment` | Potassium target 4.0-4.5 mEq/L; no pacing for pause-dependent recurrence; no repeat ECG off drugs to exclude congenital LQTS; no driving advice; LP prohibition boilerplate; prohibition cited the off-pathway EEG; em dashes. | FIXED: musts per plan (stop the three drugs, Mg sulfate 2 g, K 4.5-5.0 with thiazide held, telemetry with defibrillator until QTc < 500 ms, temporary pacing or isoproterenol, CredibleMeds avoidance and alert record, convulsive syncope, repeat ECG off drugs, driving); prohibitions kept and cleaned; LP deleted. |
| C | minor | `ground_truth.differential` | Congenital LQTS entry relied on the removed QTc normalisation; seizure entry cited the EEG. | FIXED: rewritten from the drug list, electrolytes and telemetry. |
| E/H | minor | `ground_truth.red_herrings[1]`, `key_clinical_evidence`, `metadata` | Red herring named `check_drug_interactions`; "negative EEG" pearl; em dashes. | FIXED: rewritten in clinical words. |
| H | minor | all `action_criteria[*]` | Free-text "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label. | FIXED: keys only; real rationales. |

## Changes, in one paragraph a physician can read before re-reviewing

The 60-year-old woman with drug-induced long QT and torsades now has five required steps in clinical order: ECG (QTc 540 ms, U waves), review of the medication list naming azithromycin, ondansetron or citalopram, potassium and magnesium (3.1 and 1.4), inpatient telemetry (two self-terminating pause-dependent torsades runs) and TTE (normal). The telemetry no longer shows a QTc improvement caused by treatment the agent has not given. Each of the three drugs has its own interaction report, now pharmacologically accurate, including the omeprazole-citalopram CYP2C19 interaction and PPI hypomagnesaemia. Beta-hCG is gone. EEG and the literature lookup are optional; brain MRI, CSF, tilt and head CT are waste. Musts follow Drew 2010 and ESC 2022: stop the three drugs, magnesium sulfate 2 g IV, potassium to 4.5-5.0 with the thiazide held, telemetry with a defibrillator until QTc < 500 ms, pacing or isoproterenol for recurrence, CredibleMeds avoidance, convulsive syncope rather than epilepsy, repeat ECG off drugs to screen for congenital long QT, and driving advice.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1 / Q2: `icd_codes[0]` T46.2X5A is wrong for azithromycin, ondansetron and citalopram; left unchanged for CENTRAL (I45.81 primary with T36.3X5A, T45.0X5A, T43.225A).

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. The medication-list review is stored in `initial_tool_outputs.drug_interactions` (as in M01-M03) so that an unnamed drug, for example magnesium sulfate, is answered with this patient's list rather than a per-drug report.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Checked every own-findings row against the file and the whole final case: QT arithmetic (QT 506 ms at 68 bpm gives a Bazett QTc of 539-540 ms), beta-hCG removed from criterion and output, drug criterion alternatives and the three per-drug reports (labelling wording, omeprazole-citalopram CYP2C19, citalopram 20 mg ceiling over 60), telemetry without a treatment-response trend, ondansetron start date against the HPI, potassium target 4.5-5.0 in the musts and the literature output (Drew 2010), isoproterenol only where there is no ischaemia, NICE NG232 reasoning for the waste head CT (age 60, no anticoagulant, GCS 15), sequence constraints, stop rule (five required criteria), banned strings (no tool names in clinical text) and the leak guard. icd_codes[0] left for CENTRAL as the plan rules.

Found: nothing that needed a change. No edits made.

Re-run: perfect_agent clean, case_io check clean for this case.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_drug_induced_long_qt_torsades_management` renamed to `search_drug_induced_long_qt_torsades`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.
- Added avoided action `avoid-harm-5-exercise-stress-test` (order_specialized_test, test_type exercise_stress_test, severity harm). Why: recurrent pause-dependent torsades is uncontrolled symptomatic arrhythmia, an absolute contraindication to exercise testing (Fletcher 2013 AHA exercise standards); the library would otherwise have returned a normal exercise report. Added a matching "not performed" exercise follow-up before the literature follow-up.
- red herring 0 `data_point` now quotes the HPI verbatim (the 15 to 20 second shaking likened to a seizure).

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Code: `icd_codes[0]` T46.2X5A (adverse effect of other antidysrhythmic drugs, wrong for these drugs) recoded to I45.81 (long QT syndrome), with I47.21 (torsades de pointes) and the adverse-effect codes of the three drugs, T36.3X5A (macrolides), T45.0X5A (antiallergic and antiemetic drugs: ondansetron) and T43.225A (SSRIs), all checked against the ICD-10-CM tabular list (summary Q3 / plan Q2, ruling 3). Labels: drug-induced and acquired long QT labels only; bare "torsades de pointes" retired, since "congenital long QT syndrome with torsades de pointes", the case's first mimic, contains its tokens.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-3-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2022_VA_SCD]', '[Drew_2010]']; action-2-interpret-labs citations ['[ESC_2018]'] -> ['[Drew_2010]']; action-5-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2022_VA_SCD]']; avoid-waste-4-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]']; avoid-harm-5-exercise-stress-test citations [] -> ['[Fletcher_2013]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-M04` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report, supine values = the presenting vitals; No orthostatic fall in blood pressure and no excessive heart rate rise on active standing. |
| `ground_truth.action_criteria[action-orthostatic-blood-pressure]` | added, recommended, after the ECG criterion [ESC_2018] (decisions CENTRAL 1: orthostatic BP in every initial evaluation) |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- follow-up EEG `request_eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-8-analyze-eeg` label: "EEG only if epilepsy remains likely after the cardiac work-up (optional)" -> "EEG only if epilepsy remains likely after the cardiac work-up"
- criterion `action-6-search-medical-literature` label: "Guideline lookup on torsades management (optional)" -> "Guideline lookup on torsades management"
