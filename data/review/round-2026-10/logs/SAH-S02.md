# SAH-S02
Reviewer status: R1 none, R2 none (no notes and no status in the notes file; the plan treats it as one of R2's 21 approvals) | Approved before this round: probably yes (unconfirmed, plan section 6 question 6)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No note for SAH-S02. The condition-wide classes (C1 to C5, C7, C9 to C12, C14) were applied as real errors, and the coital-trigger item of the M04 note 03a9ce4b (a class, ruling 2) per plan C11. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations` | Duplicate "24-72 hours" securing musts (C1). | FIXED: one MUST-SECURE (right PComA, as early as feasible, preferably within 24 hours). Securing pearl replaced. |
| C | major | `action_criteria`, `followup_outputs` | No catheter angiography (C3). | FIXED: recommended `dsa-aneurysm-anatomy` and a diagnostic DSA follow-up: aneurysm 6.3 x 5.3 mm (CTA 6.2 x 5.4), lobulated with a daughter sac, neck 3.1 mm, dome-to-neck 2.0, PComA arising from the inferior margin of the neck, anterior choroidal separate, no second aneurysm, no vasospasm. Soft CTA before DSA. |
| B | major | `followup_outputs` TCD | Day 5 TCD with right MCA vasospasm in a patient seen within hours (C2). | FIXED: day-0 baseline, normal velocities (MCA 59 to 63 cm/s, Lindegaard 1.5 to 1.6). |
| C | major | `required_recommendations` | BP 188/108 with no lowering action; lisinopril held with nothing replacing it (C5). | FIXED: MUST-BP-A (default agents) and MUST-HOME (withhold lisinopril, continue atorvastatin, hold metformin in critical care with insulin for glucose 186 mg/dL, avoiding hypoglycemia). |
| C | major | `required_recommendations`, `prohibited_recommendations` | Nimodipine must without hypotension adjustment; wrong IV prohibition; ICU SBP target; daily TCD must (C4, C5). | FIXED: MUST-NIMO, MUST-ICU, MUST-DCI, canonical prohibitions. |
| D | major | `followup_outputs` literature `request_sah_guidelines` | Literature step with "24-48 hours" and a case-specific coital-prognosis claim (C7). | FIXED: deleted; canonical literature output last; criterion `optional`. |
| C | minor | drug check, `action-7` | Template expected evidence about DOAC/warfarin; atorvastatin and metformin not addressed; "hold if SBP <100" instead of the dose adjustment (C10). | FIXED: tier `recommended` (plan); output in report voice with lisinopril, atorvastatin, metformin and contrast (eGFR above 30, no hold needed), the penicillin allergy as irrelevant, BP check with the 30 mg every 2 hours adjustment, no parenteral injection, CYP3A4; case-specific rationale and evidence. |
| B | minor | `ground_truth.differential`, `red_herrings` | Coital onset, a classic RCVS trigger, had no entry (class of M04 note 03a9ce4b, plan C11). | FIXED: RCVS `low` with the coital-trigger wording; red herring "Headache onset during sexual intercourse" (field `patient.history_present_illness`) with the plan's interpretation. Other entries canonical. |
| B | major | telemetry follow-up, `action-8` | Template text, management words, 24 h (C12). | FIXED: 4 h, sinus rhythm/tachycardia 86 to 110 bpm, 6 PVCs, no sustained arrhythmia or pauses, QTc 490 ms (ECG 494). |
| C | minor | labs BMP | Magnesium never measured (C9). | FIXED: 1.9 mg/dL (1.7-2.2). QTc 494: no MUST-QT. |
| B | minor | CTA follow-up | No neck measurement; neck vessels not described although the differential relies on them. | FIXED: neck 3.1 mm in observations, findings and impression; cervical carotid and vertebral arteries patent, no dissection. |
| D | minor | CT `additional_observations` | The differential needs the CT to state the sella and sinuses. | FIXED: "Sella normal in size without mass; no hyperdense dural venous sinus" added. |
| B | minor | echo follow-up | "Moderate Takotsubo cardiomyopathy" and "moderate Takotsubo pattern" next to "LVEF 44%, mildly reduced"; "classic Takotsubo". | FIXED: findings and LV chamber describe the wall motion and EF; wall motion "Takotsubo pattern". Impression unchanged. |
| E | minor | labs type and screen; `metadata.difficulty_rationale` | Engineering sentence; "consult" and "nimodipine" listed as tool steps. | FIXED: `clinical_significance` null; rationale describes the diagnostic chain and the coital distractor. |
| C | minor | `key_clinical_evidence` | Template pearls (C1, 1.3). | FIXED: four canonical pearls. |
| A | minor | criteria, order, constraints, stop rule | Label-copied rationales, free-text citations, literature recommended, no constraints, allowance 0. | FIXED: canonical rationales and citations, case-specific evidence; order NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, allowance 1. Labels kept. |

## Changes, in one paragraph a physician can read before re-reviewing

Patient, exam (GCS 15, HH2 after a one-minute confusion), CT (Fisher 3, no IVH or hydrocephalus), CTA (6.2 x 5.4 mm right PComA aneurysm, now with a 3.1 mm neck), ECG (QTc 494 ms), labs and echo (LVEF 44%) are unchanged in substance; magnesium 1.9 mg/dL is added and the CT and CTA now state the sella, sinuses and neck vessels used by the differential. The pathway is NCCT, labs, ECG, CTA, a new diagnostic catheter angiography, the nimodipine check covering lisinopril, atorvastatin and metformin, echo, a 4-hour telemetry report, an optional day-0 TCD with normal velocities (replacing the day-5 vasospasm report) and an optional literature search last. The coital onset is now scored as a reasoning point: RCVS stays low with the coital-trigger wording and a red herring explains why basal-cistern blood with a saccular aneurysm settles it. Musts: enteral nimodipine with the 30 mg every 2 hours adjustment; securing the right PComA aneurysm as early as feasible, preferably within 24 hours; neurocritical care; BP lowering now from 188/108; withholding lisinopril, continuing atorvastatin, insulin instead of metformin; sodium monitoring; DCI surveillance.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` in the canonical literature output needs the SAH allow-list (plan 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: patient block unchanged; coital-trigger red herring and RCVS wording per plan C11 (likelihood `low`); CTA vs DSA (6.2 x 5.4 vs 6.3 x 5.3 mm, neck 3.1 mm); drug check (lisinopril, atorvastatin, metformin, penicillin allergy) consistent with the medication and allergy lists, no leak; MUST-HOME metformin hold for critical care (not for contrast, creatinine 1.1) consistent with the drug-check statement; telemetry vs ECG; differential vs reports; stop rule, constraints, LP `harm` (no IVH).
Found: `initial_tool_outputs.labs.abnormal_values_summary` omitted HbA1c 7.4%, which the panel flags and the interpretation and the labs criterion list (minor).
- FLAGGED for the lead (condition-wide, not changed here): `fallback_tool_outputs.cardiac_monitoring` is a 24-hour Holter report, which cannot exist at assessment time (same reasoning as C12); it answers only a non-telemetry order, but the class spans all 30 cases.
Changed: added "HbA1c 7.4%" to `abnormal_values_summary`. Checks re-run after verification: `perfect_agent.py -v` passes (NCCT and labs show the known `<- ?` display artefact; the initial CT and labs carry the expected evidence by content), `case_io.py check` clean for the case, `test_case_guards.py -k` passes (no leak in the literature or drug-check outputs).


## Condition audit (auditor, 24 Oct 2026)

- `initial_tool_outputs.labs.abnormal_values_summary` rewritten to values and flags only. It named interpretations ("leukocytosis", "stress hyperglycemia", "neurogenic" troponin); "neurogenic" gives away the troponin red herring's answer, and the labs report carries no cross-modality interpretation. Same class as the fix already made in S05 to S10. Values, flags and the labs criterion unchanged.
- Checks after the audit: `perfect_agent.py` 30/30 pass; `case_io.py check` schema and synonym guard OK, no test failure names an SAH case; `test_case_guards -k SAH` 60 passed.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `echo.wall_motion`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `red_herrings[0].correct_interpretation (echo does not confirm etiology)`: an echocardiogram does not confirm the etiology of neurogenic myocardial injury; the interpretation now states the case's own echo (audit class, Q10).
- fallback_tool_outputs.mri: SAH-consistent brain MRI instead of the library normal report: an off-pathway brain MRI was answered by the library normal report (no blood on SWI), contradicting the CT; the case fallback now reports the CT's blood on FLAIR and SWI (CENTRAL 10).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
- followup_outputs: MR angiography report added before the literature output (aneurysm site and size from the DSA, 0.2 mm smaller as TOF reads it; P02 negative): an MRA order was answered by a fallback reporting no abnormality, contradicting the CTA and DSA (CENTRAL 10). MRA stays a waste action after the CTA.
- `ground_truth.diagnosis` (synonyms re-expanded with `--prune`): diagnosis_synonyms.yaml: the I60 category no longer grants I60.8 (non-aneurysmal SAH), so the code was pruned from this aneurysmal case.
- Checks after the close-out: `perfect_agent.py` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k SAH-` pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- follow-up `request_echocardiogram`: `echo_type` set to `TTE` (was missing); the bedside study is transthoracic, and untyped it also answered a TEE or bubble-study order.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'No diagnostic abnormality identified on this study.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-3-interpret-labs]`.alternatives: was [CBC, BMP, coagulation]; now [CBC, BMP, coagulation, troponin, BNP] | [CBC, BMP, coagulation].
- `ground_truth.action_criteria[action-3-interpret-labs]`.expected_evidence: was "WBC 15.2, glucose 186 mg/dL, HbA1c 7.4%, lactate 2.8 mmol/L, troponin I 0.22 ng/mL and BNP 198 pg/mL raised; sodium, potassium, magnesium, creatinine, hemoglobin, platelets and coagulation normal"; now "WBC 15.2, glucose 186 mg/dL, troponin I 0.22 ng/mL and BNP 198 pg/mL raised; sodium, potassium, magnesium, creatinine, hemoglobin, platelets and coagulation normal".
- Decision: serve: new first alternative (old order kept as an alternative) + trim evidence. Neurogenic troponin elevation is the case's cardiac red herring (prohibition, key evidence, red herring); baseline troponin belongs with the admission bloods in aSAH (AHA/ASA 2023), and the cardiac panel holds the BNP the evidence reads. CBC + BMP + coagulation did not return it. HbA1c and lactate are incidental to the baseline order and are trimmed.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.
- Approved case: changed for a real inconsistency (the policy's own order did not return what its evidence cites), so it goes back to re-review for this criterion only.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that this case contradicts now have a case report. Contradiction = the history, the diagnosis or a stored finding makes the normal report impossible.

- `analyze_csf (lumbar puncture, EVD, lumbar drain; xanthochromia)` -> fallback_tool_outputs.csf: blood-stained CSF without clearing (Fisher 3), xanthochromia result per time from onset. The library returned clear acellular CSF in a patient with subarachnoid blood on CT.
- `perform_clinical_assessment {assessment_type: performance_status}` -> fallback_tool_outputs.clinical_assessment: Karnofsky 40, ECOG 3. The library returned Karnofsky 100, ECOG 0, working, in an acutely ill inpatient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}` -> followup_outputs[request_gait_and_balance_timed]: assessment not completed, patient unable to stand safely; the library returned a normal Timed Up and Go in a patient whose gait the exam could not test or found abnormal.
- `order_echocardiogram {echo_type: TEE}` -> fallback_tool_outputs.echo: stored TTE wall motion and LVEF 44% carried over; no thrombus or shunt. The library TEE was normal against an abnormal stored TTE.
- `order_echocardiogram {echo_type: bubble_study}` -> followup_outputs[request_bubble_study]: same wall motion and LVEF, no right-to-left shunt at rest. The library bubble study called the echocardiogram normal.
- `order_advanced_imaging {modality: cardiac_MRI}` -> fallback_tool_outputs.advanced_imaging: wall motion and LVEF as on the stored TTE, oedema in the dysfunctional segments, no late enhancement. The library cardiac MRI reported no structural heart disease.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}` -> followup_outputs[request_structured_headache_history_ichd3]: instantaneous during sexual intercourse; red flags: thunderclap onset, onset during sexual activity, transient confusion at onset, new headache type after age 50. The library reported no thunderclap onset, no red flags and no nausea or photophobia, against the history.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}` -> followup_outputs[request_orthostatic_blood_pressure]: standing not attempted, supine BP 188/108 as at arrival. The library reported 3 minutes of symptom-free standing at BP 128/78.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}` -> followup_outputs[request_levodopa_challenge]: no parkinsonian signs, challenge not performed. The library reported normal gait and postural reflexes and no nausea in a patient who cannot stand and is vomiting.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k SAH-S02` passed; no criterion answer changed (snapshot diff); every mapped order is answered without the library (`verify.py`).
