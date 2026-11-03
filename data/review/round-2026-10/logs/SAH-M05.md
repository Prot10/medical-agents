# SAH-M05
Reviewer status: R1 none, R2 approved | Approved before this round: yes

Approved case: every change below corrects a real error (plan classes C1 to C14, or a contradiction inside the case).

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| e38a8460-0826-4c02-b86b-27cb655aea7a | FIXED | Magnesium measured: 1.6 mg/dL (L, 1.7-2.2) in `initial_tool_outputs.labs.panels.BMP`, abnormal list and interpretation updated (potassium 3.4, previously missing from the list, added). MUST-QT added: "QTc 524 ms with potassium 3.4 mmol/L, magnesium 1.6 mg/dL and U waves: replete potassium to at least 4.0 mmol/L and magnesium to at least 2.0 mg/dL, avoid adding QT-prolonging drugs ..., continuous ECG monitoring with daily QTc [Drew_2010]". MUST-HOME withholds furosemide (and ramipril). The drug check (`action-7-check-drug-interactions`) is now `required` and its output states the furosemide K/Mg loss with QTc 524 ms and the QT-drug caution. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status`, `.additional`, `patient.history_present_illness` | Label HH3 while the exam read "Alert and oriented x4; GCS 15 ... mild confusion resolved", the grade was justified by a resolved LOC, and the HPI said "now alert and fully oriented" (C13). | FIXED: HPI "In the ED, she is awake but remains mildly confused."; exam "Awake but confused: oriented to person and place, not to date; GCS 14 (E4V4M6)"; additional "Hunt-Hess Grade 3 (confusion, headache, nuchal rigidity)". |
| D | major | `initial_tool_outputs.ct.additional_observations` | "Multiple PKD-related renal cysts visible on lower cuts": a head CT does not image the kidneys (impossible, C14); "Fisher grade 3-4" contradicts the impression (grade 3, no IVH). | FIXED: kidney line deleted; "Fisher grade 3"; sella and venous-sinus negatives added. |
| B | major | `followup_outputs` TCD | "Day 7" TCD with severe ACA and moderate MCA vasospasm and "new bifrontal headache and mild confusion" in a patient seen hours after onset. | FIXED: day-0 baseline, normal velocities, clinical note removed, canonical text. |
| B | major | `followup_outputs` `request_hyponatremia_management` | "Serum sodium Day 3" panel (128, urine Na 92) cannot exist at assessment time (C2). | FIXED: follow-up deleted; the sodium must stays. |
| C | major | `ground_truth.assessment` | Two 24-72 h musts; ICU must with inline SBP; no BP must (SBP 176) or agent choice for LVEF 38%; generic EVD must; no QT, LVEF or home-drug must; TCD days 4-14 must; misworded nimodipine and BP prohibitions. | FIXED: MUST-NIMO; MUST-SECURE for the AComA aneurysm "first, managing the small unruptured left PComA aneurysm separately"; MUST-ICU; MUST-EVD-NOW "with depressed consciousness"; MUST-BP-A with "nicardipine or clevidipine infusion" (LVEF 38%); MUST-HOME (withhold furosemide and ramipril); MUST-QT; MUST-LVEF (38%); sodium kept; MUST-DCI; canonical prohibitions. |
| C | major | `ground_truth.avoided_actions` `avoid-harm-1-analyze-csf` | `harm` although the CT shows hydrocephalus. | FIXED: `contraindicated`, rationale updated. |
| C | major | `ground_truth.action_criteria` | No DSA before securing (C3). | FIXED: `dsa-aneurysm-anatomy` recommended, follow-up with the AComA aneurysm (8.5 x 6.2 mm, neck 3.4 mm, dome-to-neck 2.5, irregular apical lobule, right A2 at the neck) and the 3.1 mm left PComA aneurysm; CTA before DSA (soft). |
| C | minor | drug-check output | Content was partly management prose ("Furosemide on hold given cerebral salt wasting"). | FIXED: rewritten as interaction findings (see note row) plus contrast and creatinine caution, parenteral warning, 30 mg every 2 h rule. |
| D | minor | `followup_outputs` CTA | "Large" for an 8.4 mm aneurysm (C13); "creatinine 1.2 - contrast nephropathy risk low" cites labs (cross-modality). | FIXED: "Large" removed in findings and impression; observation reduced to "IV contrast CTA"; neck-vessel statement added. |
| D | minor | `initial_tool_outputs.ecg.findings[3]` | "U-waves visible (hypokalemia component)" attributes a lab cause inside the ECG. | FIXED: "U-waves visible". |
| B | major | telemetry output | Template text, 24 h. | FIXED: 4 h, sinus tachycardia 96-122 bpm, 64 PVCs with one couplet, no sustained arrhythmia or pauses, QTc 524 ms without torsades. |
| D | major | literature follow-up `request_pkd_aneurysm_literature`, criterion | Empty summary, recommended literature step. | FIXED: deleted; canonical output last; criterion optional. |
| C | minor | `ground_truth.key_clinical_evidence[-1]` | PKD pearl recommended screening for all first-degree relatives; screening applies to relatives with ADPKD (and family history). | FIXED: "... screening MR angiography is warranted in first-degree relatives who also have ADPKD." |
| C | minor | labs type and screen; differential; pearls; citations; rationales; order; constraints; stop rule; metadata | Template items (C9, C11, C14, section 3). | FIXED: significance null; canonical differential; canonical pearls; bracketed citations; canonical rationales and case evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; NCCT before CTA and CTA before DSA (soft); stop rule = five required, allowance 1; stale CSF concern emptied; difficulty rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing
50-year-old woman with ADPKD, father died of aneurysmal SAH, on ramipril and furosemide; thunderclap headache with witnessed LOC this morning, now confused with GCS 14 (the exam previously said GCS 15 oriented, which contradicted the HH3 label), Fisher 3 SAH with communicating hydrocephalus, 8.4 mm multilobulated AComA aneurysm plus a 3.1 mm left PComA aneurysm, QTc 524 ms with U waves, potassium 3.4, magnesium now measured at 1.6, LVEF 38% stress cardiomyopathy. The impossible day-7 vasospasm TCD and day-3 sodium panel are gone; the kidney cysts on a head CT are deleted. The pathway adds a diagnostic DSA and a required drug check (furosemide K/Mg loss with QTc 524, ramipril hypotension). Musts now include enteral nimodipine, securing the AComA aneurysm first as early as feasible and preferably within 24 h, neurocritical care, EVD for hydrocephalus with depressed consciousness, nicardipine or clevidipine for BP (LVEF 38%), withholding furosemide and ramipril, K and Mg repletion with QT precautions, a cardiology and neuroanesthesia plan for LVEF 38%, sodium and DCI surveillance. LP is now `contraindicated`.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- As plan section 5 (allow-list `[Drew_2010]`, `[Molyneux_2002]`).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial check (24 Oct 2026), approved case: diff, full final case, perfect-agent `-v`, `case_io.py check`, `test_case_guards -k SAH-M05`.
- Note e38a8460: confirmed FIXED (magnesium 1.6 mg/dL flagged low in BMP, abnormal list and interpretation; potassium 3.4 listed; MUST-QT with K, Mg and U waves; drug check required, in the stop rule, with furosemide K/Mg content).
- Confirmed each change corrects a real error: HPI and exam now support HH3 (GCS 14, confused); kidney cysts on a head CT deleted; Fisher 3 consistent with no IVH; future-dated TCD and sodium panel removed; MUST-EVD-NOW "with depressed consciousness" matches the hydrocephalus; LP `contraindicated`; BP agents without labetalol for LVEF 38%; MUST-LVEF 38%; MUST-SECURE names the ruptured AComA aneurysm first; DSA 8.5 x 6.2 mm vs CTA 8.4 x 6.2 mm, ratio 8.5/3.4 = 2.5, second aneurysm 3.1 mm on both; sulfa allergy compatible with long-standing furosemide; PKD screening pearl correctly narrowed to relatives with ADPKD. No prose churn beyond these.
- No error found; no change made.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `echo.findings[0]`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.wall_motion`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.impression (consultation advice removed)`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.recommended_actions`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
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
- Decision: serve: new first alternative (old order kept as an alternative). Neurogenic troponin elevation is the case's cardiac red herring (prohibition, key evidence, red herring); baseline troponin belongs with the admission bloods in aSAH (AHA/ASA 2023), and the cardiac panel holds the BNP the evidence reads. CBC + BMP + coagulation did not return it.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.
- Approved case: changed for a real inconsistency (the policy's own order did not return what its evidence cites), so it goes back to re-review for this criterion only.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that this case contradicts now have a case report. Contradiction = the history, the diagnosis or a stored finding makes the normal report impossible.

- `analyze_csf (lumbar puncture, EVD, lumbar drain; xanthochromia)` -> fallback_tool_outputs.csf: blood-stained CSF without clearing (Fisher 3), xanthochromia result per time from onset. The library returned clear acellular CSF in a patient with subarachnoid blood on CT.
- `perform_clinical_assessment {assessment_type: performance_status}` -> fallback_tool_outputs.clinical_assessment: Karnofsky 30, ECOG 4. The library returned Karnofsky 100, ECOG 0, working, in an acutely ill inpatient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}` -> followup_outputs[request_gait_and_balance_timed]: assessment not completed, patient unable to stand safely; the library returned a normal Timed Up and Go in a patient whose gait the exam could not test or found abnormal.
- `perform_clinical_assessment {assessment_type: cognitive_screen}` -> followup_outputs[request_cognitive_screen]: MoCA 16/30; the library returned MoCA 28/30 in a confused patient (GCS 14).
- `order_specialized_test {test_type: neuropsych_battery}` -> fallback_tool_outputs.specialized_test: incomplete battery with impaired attention and orientation; the library returned normal cognition in all domains.
- `order_echocardiogram {echo_type: TEE}` -> fallback_tool_outputs.echo: stored TTE wall motion and LVEF 38% carried over; no thrombus or shunt. The library TEE was normal against an abnormal stored TTE.
- `order_echocardiogram {echo_type: bubble_study}` -> followup_outputs[request_bubble_study]: same wall motion and LVEF, no right-to-left shunt at rest. The library bubble study called the echocardiogram normal.
- `order_advanced_imaging {modality: cardiac_MRI}` -> fallback_tool_outputs.advanced_imaging: wall motion and LVEF as on the stored TTE, oedema in the dysfunctional segments, no late enhancement. The library cardiac MRI reported no structural heart disease.
- `order_body_imaging {study: chest_abdomen_pelvis_CT / pelvis_abdomen_CT}` -> fallback_tool_outputs.body_imaging: enlarged polycystic kidneys and hepatic cysts. Known polycystic kidney disease; the library returned a normal abdomen.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}` -> followup_outputs[request_pelvis_abdomen_ultrasound]: enlarged polycystic kidneys and hepatic cysts. Known polycystic kidney disease; the library returned a normal abdomen.
- `order_body_imaging {study: pelvis_abdomen_MRI}` -> followup_outputs[request_pelvis_abdomen_mri]: enlarged polycystic kidneys and hepatic cysts. Known polycystic kidney disease; the library returned a normal abdomen.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}` -> followup_outputs[request_structured_headache_history_ichd3]: instantaneous at rest at her desk this morning; red flags: thunderclap onset, loss of consciousness at onset. The library reported no thunderclap onset, no red flags and no nausea or photophobia, against the history.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}` -> followup_outputs[request_orthostatic_blood_pressure]: standing not attempted, supine BP 176/104 as at arrival. The library reported 3 minutes of symptom-free standing at BP 128/78.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}` -> followup_outputs[request_levodopa_challenge]: no parkinsonian signs, challenge not performed. The library reported normal gait and postural reflexes and no nausea in a patient who cannot stand and is vomiting.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k SAH-M05` passed; no criterion answer changed (snapshot diff); every mapped order is answered without the library (`verify.py`).
