# SAH-S06
Reviewer status: R1 none, R2 approved (with 3 notes) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| c3c56bb2-e199-4805-8f47-f61e0110d4d2 | FIXED | Securing: the two "24-72 hours" securing musts replaced by one MUST-SECURE (urgent joint neurosurgical and neurointerventional review, coiling or clipping of the AComA aneurysm as early as feasible, preferably within 24 hours of onset, [Hoh_2023]) in `ground_truth.assessment.required_recommendations`; securing pearl replaced. DSA: new recommended criterion `dsa-aneurysm-anatomy` and diagnostic follow-up `request_digital_subtraction_angiography` (5.9 x 5.1 mm multilobulated AComA aneurysm, neck 3.1 mm, dome-to-neck 1.9, A2 origins clear, no second aneurysm, no vasospasm). Timeline: the day-5 TCD is now an admission baseline (post-ictus day 0, normal velocities), so no result in the case postdates the first hours. |
| 7f1b4f47-fcf5-46eb-88f3-4c840fe7861c | FIXED | `initial_tool_outputs.labs.panels.BMP`: potassium 3.6 mEq/L and magnesium 1.6 mg/dL (L, ref 1.7-2.2; heavy daily alcohol use) added, `abnormal_values_summary` and `interpretation` updated. MUST-QT added: "QTc 516 ms with potassium 3.6 mmol/L: replete potassium to at least 4.0 mmol/L and magnesium to at least 2.0 mg/dL, avoid adding QT-prolonging drugs (for example ondansetron or haloperidol, and review sertraline), and keep continuous ECG monitoring with daily QTc [Drew_2010]." The QTc literature output that held the K/Mg targets was deleted (C7). |
| 633fd9a3-78f1-4d02-b4fc-bb8db375af6f | FIXED | MUST-BP-A "Lower blood pressure now with a short-acting titratable intravenous agent (nicardipine or clevidipine infusion, or labetalol boluses) ..." (LVEF 42%, no bradycardia, asthma or cocaine, so labetalol stays an option); MUST-HOME "Withhold verapamil while on nimodipine (...); withhold sertraline while the QTc exceeds 500 ms."; the drug-check output no longer offers hydralazine (rewritten, `followup_outputs[2].output`). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` drug check (`request_nimodipine_verapamil_sertraline_check`), `action-7` | Output: hydralazine alternative, "Seek cardiology input", "Monitor QTc before each nimodipine dose", no mention that verapamil (a CYP3A4 inhibitor) raises nimodipine levels; criterion recommended with the template anticoagulation evidence (C10). | FIXED: output rewritten in report voice (verapamil pharmacodynamic and CYP3A4 interaction, sertraline QT risk higher with prolonged QTc and low K/Mg, SSRI bleeding tendency, withhold verapamil and replace with a short-acting IV agent, withhold sertraline above QTc 500 ms with discontinuation watch, BP before each dose with the 30 mg every 2 hours adjustment, no parenteral injection); criterion `required` with case-specific rationale and evidence, in the stop rule. Leak guard passes. |
| C | major | `required_recommendations`, `prohibited_recommendations` (nimodipine) | Nimodipine must without the hypotension adjustment; IV prohibition wrong as written (C4). | FIXED: MUST-NIMO and the canonical parenteral-injection prohibition. |
| C | major | `required_recommendations` | Heavy daily alcohol use (4-6 beers, AST and GGT raised) with no withdrawal or thiamine action; the content sat only in a literature output. | FIXED: MUST-ALCOHOL (thiamine before glucose, validated withdrawal scale, lowest effective benzodiazepine dose). Alcohol literature deleted. |
| C | minor | `required_recommendations` ICU and TCD musts, BP prohibition | ICU must carried an SBP target; daily-TCD must overstated TCD; "SBP >160" presented as a guideline threshold. | FIXED: MUST-ICU, MUST-DCI, canonical BP prohibition. |
| D | major | `followup_outputs` literature (alcohol withdrawal, QTc) | Literature as clinical steps; "Current QTc 516 ms - hold all QT-prolonging agents immediately" (patient value and order inside a literature output) (C7). | FIXED: both deleted; canonical literature output last; criterion `optional` with canonical text. |
| B | major | `followup_outputs` TCD | TCD dated "day 5" with ACA vasospasm 40 minutes after arrival (C2). | FIXED: day-0 baseline, MCA 65 to 68 cm/s, Lindegaard 1.7 to 1.8, ACA 49 to 51, basilar 40; canonical protocol, impression and recommendation. |
| B | major | `followup_outputs` telemetry, `action-8` expected evidence | Template text with management, 24 h duration (C12). | FIXED: 4 h since arrival, sinus tachycardia 92 to 114 bpm, 22 unifocal PVCs with one couplet, no sustained arrhythmia or pauses, QTc 512 ms on monitoring leads without torsades. |
| B | minor | `patient.neurological_exam.mental_status` | "Alert and oriented x4; GCS 14 (confused initially, now 15)" (C13). | FIXED: "GCS 15 (confused at the scene, now oriented)". |
| C | minor | `patient.neurological_exam.cranial_nerves` | "mild papilledema suspected - fundoscopy borderline" about an hour after the ictus, with no hydrocephalus on CT: papilledema takes longer to develop and nothing else in the case uses it. | FIXED: "fundi poorly seen because of photophobia, no definite papilledema". |
| B | minor | `initial_tool_outputs.labs` | Type-and-screen engineering sentence (C14). | FIXED: `clinical_significance` null; summary lists values and flags only. |
| B | minor | `initial_tool_outputs.ct.additional_observations`, CTA `angiography_findings`, `ground_truth.differential` | Differential key features generic (C11); reports did not state the sella, sinuses or neck vessels the new key features cite. | FIXED: canonical key features; CT "Sella normal in size without mass; no hyperdense dural venous sinus"; CTA "Cervical carotid and vertebral arteries: Patent, no dissection or stenosis". |
| C | minor | `ground_truth.key_clinical_evidence` | 24-72 h, daily-TCD, CT-sensitivity and xanthochromia pearls (C1, plan 1.3). | FIXED: the four canonical pearls; the other six kept. |
| A | minor | `ground_truth.action_criteria[*]`, order, `sequence_constraints`, `stop_rule`, `metadata.difficulty_rationale` | Label-copied rationales, duplicate free-text citations, drug check and literature before the CTA, no constraints, allowance 0; stale "7 required tools ... consult" rationale. | FIXED: canonical rationales and citations, case-specific expected evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD (optional), literature (optional); follow-ups in the same order; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, drug check, `max_additional_actions` 1; difficulty rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

The presentation is unchanged (56-year-old man, thunderclap headache with a fall and brief confusion, verapamil, sertraline, heavy alcohol and tobacco use, BP 198/114), except that the exam now reads GCS 15 (confused at the scene, now oriented) and no definite papilledema. CT (Fisher 3, no IVH or hydrocephalus), CTA (5.8 x 5.2 mm multilobulated AComA aneurysm), ECG (sinus tachycardia, deep T inversions, QTc 516 ms) and echo (LVEF 42%, stress pattern) are unchanged; labs add potassium 3.6 and a low magnesium 1.6 mg/dL. The pathway is NCCT, labs, ECG, CTA, a new diagnostic catheter angiography, the required nimodipine check (verapamil: additive hypotension, bradycardia, negative inotropy and CYP3A4-mediated rise in nimodipine; sertraline: QT risk at QTc above 500 ms), echo, 4 hours of telemetry (sinus tachycardia, PVCs with one couplet, QTc 512 ms, no torsades), an optional day-0 baseline TCD and an optional general literature search last. The musts now say: enteral nimodipine with the 30 mg every 2 hours adjustment; secure the AComA aneurysm as early as feasible, preferably within 24 hours; neurocritical care admission; lower BP now with nicardipine, clevidipine or labetalol; withhold verapamil, and sertraline while QTc exceeds 500 ms; replete potassium to 4.0 or more and magnesium to 2.0 or more, avoid QT-prolonging drugs, continuous ECG; sodium monitoring; DCI surveillance with euvolemia; thiamine and withdrawal monitoring with the lowest effective benzodiazepine dose.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` (canonical literature output) and `[Drew_2010]` (MUST-QT) must be added to the SAH criteria-pack allow-list (plan section 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None. Decision recorded for the lead: plan section 4 says "low-normal" magnesium for S06 while C9 says "lower (1.5 to 1.8, flagged)" with heavy alcohol use; I chose 1.6 mg/dL, flagged low, because 4-6 beers daily with raised GGT makes hypomagnesemia the expected finding and the MUST-QT repletion applies either way.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the git diff (patient block changed only in mental status, C13 wording, and cranial nerves; the papilledema change is accepted: "suspected, borderline" papilledema an hour after the ictus with no hydrocephalus is implausible and unused); all three notes against the file (one MUST-SECURE, no 24-72 h text, DSA criterion and diagnostic output without treatment content, day-0 TCD; potassium 3.6 and magnesium 1.6 flagged low in the BMP with summary and interpretation in step, MUST-QT with the case values; MUST-BP-A with labetalol kept as an option, LVEF 42% and no bradycardia, asthma or cocaine; MUST-HOME withholds verapamil and sertraline; no hydralazine anywhere); drug check `required` and in the stop rule, after the CTA; leak guard passes; MUST-ALCOHOL present; DSA arithmetic (5.9 / 3.1 = 1.9); lab flags; LP avoided action `harm` (no IVH or hydrocephalus).
Found and changed:
- Ruling 7: the HPI raises a fall (found on the floor after a crash, no recall of falling) but traumatic SAH was neither in the differential nor excluded. Added `ground_truth.differential[4]` "Traumatic subarachnoid hemorrhage from the fall", `low`: he reported the headache by phone before he fell, the blood fills the basal cisterns rather than the convexity sulci, no contusion on CT, saccular AComA aneurysm on CTA.
- Telemetry (new text): "Sinus tachycardia, 92 to 114 bpm" calls a rate of 92 tachycardia. Now "Sinus rhythm and sinus tachycardia, 92 to 114 bpm" in `findings[0]`, `impression`, `rhythm_summary` and the `action-8-order-cardiac-monitoring` expected evidence.
`perfect_agent.py -v` and `case_io.py check` clean after the edits.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `echo.findings[0]`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.findings[1]`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
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
- `ground_truth.action_criteria[action-3-interpret-labs]`.expected_evidence: was "Magnesium 1.6 mg/dL low and potassium 3.6 mEq/L low-normal; WBC 17.2, glucose 168 mg/dL, AST 62 and GGT 184 U/L, troponin I 0.28 ng/mL and BNP 214 pg/mL raised; sodium, creatinine, blood count and INR normal"; now "Magnesium 1.6 mg/dL low and potassium 3.6 mEq/L low-normal; WBC 17.2, glucose 168 mg/dL, troponin I 0.28 ng/mL and BNP 214 pg/mL raised; sodium, creatinine, blood count and INR normal".
- Decision: serve: new first alternative (old order kept as an alternative) + trim evidence. Neurogenic troponin elevation is the case's cardiac red herring (prohibition, key evidence, red herring); baseline troponin belongs with the admission bloods in aSAH (AHA/ASA 2023), and the cardiac panel holds the BNP the evidence reads. CBC + BMP + coagulation did not return it. AST and GGT are incidental to the baseline order (the alcohol must rests on the history) and are trimmed.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.
- Approved case: changed for a real inconsistency (the policy's own order did not return what its evidence cites), so it goes back to re-review for this criterion only.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that this case contradicts now have a case report. Contradiction = the history, the diagnosis or a stored finding makes the normal report impossible.

- `analyze_csf (lumbar puncture, EVD, lumbar drain; xanthochromia)` -> fallback_tool_outputs.csf: blood-stained CSF without clearing (Fisher 3), xanthochromia result per time from onset. The library returned clear acellular CSF in a patient with subarachnoid blood on CT.
- `perform_clinical_assessment {assessment_type: performance_status}` -> fallback_tool_outputs.clinical_assessment: Karnofsky 40, ECOG 3. The library returned Karnofsky 100, ECOG 0, working, in an acutely ill inpatient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}` -> followup_outputs[request_gait_and_balance_timed]: assessment not completed, patient unable to stand safely; the library returned a normal Timed Up and Go in a patient whose gait the exam could not test or found abnormal.
- `order_echocardiogram {echo_type: TEE}` -> fallback_tool_outputs.echo: stored TTE wall motion and LVEF 42% carried over; no thrombus or shunt. The library TEE was normal against an abnormal stored TTE.
- `order_echocardiogram {echo_type: bubble_study}` -> followup_outputs[request_bubble_study]: same wall motion and LVEF, no right-to-left shunt at rest. The library bubble study called the echocardiogram normal.
- `order_advanced_imaging {modality: cardiac_MRI}` -> fallback_tool_outputs.advanced_imaging: wall motion and LVEF as on the stored TTE, oedema in the dysfunctional segments, no late enhancement. The library cardiac MRI reported no structural heart disease.
- `interpret_labs {panels: [CDT]}` -> fallback_tool_outputs.labs: %CDT 2.6%. 4-6 beers daily and a stored GGT of 184 U/L; the library returned 1.2%.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}` -> followup_outputs[request_structured_headache_history_ichd3]: sudden at home; red flags: thunderclap onset, altered consciousness after onset, new headache type after age 50. The library reported no thunderclap onset, no red flags and no nausea or photophobia, against the history.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}` -> followup_outputs[request_orthostatic_blood_pressure]: standing not attempted, supine BP 198/114 as at arrival. The library reported 3 minutes of symptom-free standing at BP 128/78.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}` -> followup_outputs[request_levodopa_challenge]: no parkinsonian signs, challenge not performed. The library reported normal gait and postural reflexes and no nausea in a patient who cannot stand and is vomiting.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k SAH-S06` passed; no criterion answer changed (snapshot diff); every mapped order is answered without the library (`verify.py`).
