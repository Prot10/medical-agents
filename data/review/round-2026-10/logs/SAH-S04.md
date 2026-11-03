# SAH-S04
Reviewer status: R1 none, R2 approved | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| cabb6393-ffec-4695-9d58-f4509ee19eda | FIXED | Securing (C1): the two "24-72 hours" musts replaced by one MUST-SECURE "... by endovascular coiling or microsurgical clipping, after anticoagulant reversal, as early as feasible, preferably within 24 hours of onset [Hoh_2023] ..."; securing pearl replaced. DSA (C3): recommended `dsa-aneurysm-anatomy` and diagnostic DSA follow-up. Reversal: MUST-REVERSE (last 5 mg dose about 8 hours before arrival, anti-Xa 164 ng/mL: andexanet low-dose regimen or four-factor PCC 50 IU/kg, heparin resistance, apixaban stopped, restart decided after securing) replaces the generic "PCC, andexanet alfa, idarucizumab, or vitamin K" must; new required criterion `check-apixaban-reversal` (check_drug_interactions, drug apixaban) answered by `request_apixaban_reversal`, and a `hard` constraint reversal before DSA. Timeline (C2): the "day 7" vasospasm TCD re-dated to a day-0 baseline; the anticoagulation-restart literature step deleted. The joint review is in the must (no consult tool by design). |
| 60a5d171-e5f5-4984-b216-5051d459ab98 | FIXED (BP, home drugs); ALREADY-FIXED (nimodipine must existed) | Both metoprolol holds deleted (reversal output "Metoprolol + nimodipine: additive bradycardia - hold metoprolol"; nimodipine check "Hold metoprolol during nimodipine course") together with the digoxin alternative. MUST-HOME "Continue metoprolol for AF rate control unless bradycardia or hypotension; withhold ramipril during the acute phase; continue rosuvastatin." MUST-BP-A for 176/102 (nicardipine or clevidipine infusion, or labetalol boluses). Nimodipine: the must was present; reworded to MUST-NIMO. Administration itself is a must, since the harness has no treatment tool. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | reversal follow-up `request_apixaban_reversal` | Dosing thresholds "<10 mg ... >10 mg" and "≤8h" wrong (US label: 5 mg or less, or 8 hours or more, gives the low dose), "4F-PCC less effective", "Hold apixaban indefinitely", "typically 4-8 weeks" restart (plan C10). | FIXED: rewritten per plan 1.2 (low and high dose criteria, heparin resistance, boxed thromboembolic warning, idarucizumab and vitamin K do not apply); PCC 50 IU/kg as the alternative; no restart timing. Leak guard passes. |
| B | major | `initial_tool_outputs.ct` | Labelled Fisher 4 but the CT said "No IVH" (C13). | FIXED: finding "Small amount of blood layering in the occipital horns of both lateral ventricles" and impression item 2; "No IVH" removed; no hydrocephalus kept. LP avoided action now `contraindicated` (IVH and anticoagulation). |
| D | minor | CT `additional_observations` | "Possibly mildly hypodense blood due to anticoagulation dilution" cross-references the medication list and is not an imaging fact (C14). | FIXED: removed; sella and sinus statement added for the differential. |
| D | minor | `initial_tool_outputs.ecg.findings` | "Normal rate - metoprolol effect" (C14). | FIXED: removed. |
| C | minor | labs BMP | Potassium and magnesium missing (C9). | FIXED: potassium 4.2 mEq/L, magnesium 2.0 mg/dL. QTc 488: no MUST-QT. |
| E | minor | CTA follow-up | "Large" for a 7.2 mm aneurysm (C13); no neck measurement; neck vessels not described. | FIXED: "Large" removed from findings and impression; neck 3.6 mm; cervical vessels patent, no dissection. DSA matches (7.3 x 6.2 mm, neck 3.6 mm, dome-to-neck 2.0). |
| C | major | nimodipine check follow-up, `action-7` | "additive bradycardia and negative inotropy" for metoprolol with nimodipine overstated; template DOAC evidence. | FIXED: report-voice output (metoprolol additive BP lowering, little AV-nodal effect of nimodipine, rebound risk on abrupt beta-blocker withdrawal; ramipril; rosuvastatin and apixaban no interaction; codeine intolerance; BP check with the 30 mg every 2 hours adjustment; no parenteral injection; CYP3A4). Tier `recommended` (plan C10 lists S04 only for the reversal check as required). |
| C | major | `required_recommendations`, `prohibited_recommendations` | Nimodipine must, IV prohibition, ICU SBP target, daily TCD must (C4, C5). | FIXED: MUST-NIMO, MUST-ICU, MUST-DCI, canonical prohibitions; the reversal prohibition kept. |
| B | minor | `patient.history_present_illness`, `past_medical_history` | "CHADS2VASc score of 3" in a 63-year-old man whose only listed factor is hypertension: CHA2DS2-VASc is 1. | FIXED: "CHA2DS2-VASc score of 1 (hypertension)" in both fields. |
| C | minor | `key_clinical_evidence` last pearl | "hematoma expansion" is an ICH concept; the SAH risk is rebleeding and procedural bleeding. | FIXED: "therapeutic anticoagulation raises the risk of rebleeding and of procedural bleeding, so reversal precedes catheter angiography, CSF diversion and securing." Four canonical pearls also applied. |
| D | minor | echo follow-up | "known AF" and "consistent with AF history" cross-reference the history; "Mild Takotsubo", "borderline Takotsubo". | FIXED: LA "Mildly dilated"; findings "Mild apical hypokinesis, LVEF 50%", "Mildly dilated left atrium"; wall motion "Mild apical hypokinesis". Impression unchanged. |
| B | major | telemetry follow-up | Template text, 24 h (C12). | FIXED: 3 h, sinus rhythm 66 to 84 bpm, 18 atrial premature complexes, no AF, no sustained arrhythmia or pauses, QTc 486 ms, no torsades. |
| D | major | literature follow-up `request_anticoagulation_restart` | Literature as a clinical step with unsourced restart timing (C7). | FIXED: deleted; canonical literature last; criterion `optional`; restart timing is in MUST-REVERSE. |
| E | minor | type and screen; `metadata.difficulty_rationale` | Engineering sentence; rationale listed comorbidities of other cases ("CKD, PKD, lithium, cocaine"). | FIXED: null; case-specific rationale. |
| B | minor | differential | Generic key features (C11). | FIXED: canonical, no trigger wording (bending to plant flowers is not a recognised RCVS trigger). |
| A | minor | criteria, order, constraints, stop rule | Label-copied rationales, free-text citations, no constraints, allowance 0. | FIXED: order NCCT, labs, ECG, CTA, reversal check, DSA, nimodipine check, echo, telemetry, TCD, literature; follow-ups in the same order; soft NCCT before CTA and CTA before DSA, hard reversal before DSA; stop rule NCCT, labs, ECG, CTA, reversal check, allowance 1. Labels of existing criteria kept. |

## Changes, in one paragraph a physician can read before re-reviewing

Approved case, changed for the condition-wide errors, both notes and four case errors. The patient (63-year-old man on apixaban, metoprolol, ramipril, rosuvastatin; HH2 after 30 seconds of confusion) is unchanged except that his CHA2DS2-VASc score now reads 1, which is what his listed history gives. The CT now shows the small intraventricular blood in both occipital horns that its Fisher 4 label requires (no hydrocephalus), so LP is contraindicated; potassium 4.2 and magnesium 2.0 were added. The pathway is NCCT, labs (anti-Xa 164 ng/mL), ECG, CTA (7.2 mm AComA aneurysm, neck 3.6 mm, no longer "large"), the required apixaban reversal check, then catheter angiography (hard constraint after the reversal), the nimodipine check, echo, telemetry, an optional day-0 TCD with normal velocities (replacing the day-7 vasospasm report) and an optional literature search last. Musts: reverse apixaban now with the andexanet low-dose regimen (5 mg dose 8 hours earlier) or four-factor PCC 50 IU/kg, noting heparin resistance before coiling, with restart decided after securing; enteral nimodipine with the 30 mg every 2 hours adjustment; securing after reversal as early as feasible, preferably within 24 hours; neurocritical care; BP lowering now from 176/102; continue metoprolol for AF rate control, withhold ramipril, continue rosuvastatin; sodium monitoring; DCI surveillance.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` in the canonical literature output needs the SAH allow-list (plan 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None. (Lead note: the plan's section 4 gives no tier for the S04 nimodipine check; I set `recommended`, as for the other cases whose home drugs are only withheld or continued.)

## Verification (adversarial verifier, 24 Oct 2026)

Checked: note cabb6393 (MUST-SECURE after reversal with the Hoh window, MUST-REVERSE low dose, required `check-apixaban-reversal` answered by `request_apixaban_reversal`, hard constraint reversal before DSA, DSA output diagnostic only, day-0 TCD, restart literature deleted); note 60a5d171 (no metoprolol hold left in any output, MUST-HOME continues metoprolol for AF rate control and withholds ramipril, MUST-BP-A present). Reversal output against plan 1.2 (low dose for a 5 mg dose; high-dose criteria; heparin resistance; no idarucizumab or vitamin K use). CHA2DS2-VASc: 63-year-old man with hypertension only (hyperlipidemia and a father's MI do not score) gives 1, so the worker's correction from 3 is right. IVH added for Fisher 4, LP `contraindicated`, no hydrocephalus so no EVD must (plan C6). CTA vs DSA (7.2 x 6.4 vs 7.3 x 6.2 mm, neck 3.6 mm). Telemetry sinus with APCs, consistent with paroxysmal AF in sinus on the ECG.
Found: (1) the anti-Xa reference range "Trough <50 ng/mL therapeutic" is wrong (apixaban 5 mg twice daily has expected trough levels well above 50 ng/mL; 50 ng/mL is the level usually taken as clinically relevant in major bleeding, which is what flags 164 here). (2) `red_herrings[0]` says the echo shows apical ballooning, but this echo shows mild apical hypokinesis with LVEF 50% (same fix as S01 and S03). (3) `abnormal_values_summary` omitted BNP 142 pg/mL, which the panel flags and the interpretation lists.
- FLAGGED for the lead (condition-wide, not changed here): `fallback_tool_outputs.cardiac_monitoring` is a 24-hour Holter report, which cannot exist at assessment time (same reasoning as C12); it answers only a non-telemetry order, but the class spans all 30 cases.
- FLAGGED for the lead: check the same anti-Xa reference wording in SAH-M07 (the other apixaban case), not assigned to this verifier.
Changed: anti-Xa `reference_range` now "<50 (50 or more is clinically relevant in major bleeding)" (value and flag unchanged); red-herring interpretation now ends "the echocardiogram shows only mild apical hypokinesis with preserved ejection fraction and no primary cardiac lesion, and the focus remains on aneurysm securing."; "BNP 142 elevated" added to the summary. Checks re-run after verification: `perfect_agent.py -v` passes (NCCT and labs show the known `<- ?` display artefact; the initial CT and labs carry the expected evidence by content), `case_io.py check` clean for the case, `test_case_guards.py -k` passes (no leak in the literature or drug-check outputs).


## Condition audit (auditor, 24 Oct 2026)

- `initial_tool_outputs.labs.abnormal_values_summary` rewritten to values and flags only. It named interpretations ("leukocytosis", "stress hyperglycemia", "neurogenic" troponin); "neurogenic" gives away the troponin red herring's answer, and the labs report carries no cross-modality interpretation. Same class as the fix already made in S05 to S10. Values, flags and the labs criterion unchanged.
- Checks after the audit: `perfect_agent.py` 30/30 pass; `case_io.py check` schema and synonym guard OK, no test failure names an SAH case; `test_case_guards -k SAH` 60 passed.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
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

- `analyze_csf (lumbar puncture, EVD, lumbar drain; xanthochromia)` -> fallback_tool_outputs.csf: blood-stained CSF without clearing (Fisher 4), xanthochromia result per time from onset. The library returned clear acellular CSF in a patient with subarachnoid blood on CT.
- `perform_clinical_assessment {assessment_type: performance_status}` -> fallback_tool_outputs.clinical_assessment: Karnofsky 40, ECOG 3. The library returned Karnofsky 100, ECOG 0, working, in an acutely ill inpatient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}` -> followup_outputs[request_gait_and_balance_timed]: assessment not completed, patient unable to stand safely; the library returned a normal Timed Up and Go in a patient whose gait the exam could not test or found abnormal.
- `order_echocardiogram {echo_type: TEE}` -> fallback_tool_outputs.echo: stored TTE wall motion and LVEF 50% carried over; no thrombus or shunt. The library TEE was normal against an abnormal stored TTE.
- `order_echocardiogram {echo_type: bubble_study}` -> followup_outputs[request_bubble_study]: same wall motion and LVEF, no right-to-left shunt at rest. The library bubble study called the echocardiogram normal.
- `order_advanced_imaging {modality: cardiac_MRI}` -> fallback_tool_outputs.advanced_imaging: wall motion and LVEF as on the stored TTE, oedema in the dysfunctional segments, no late enhancement. The library cardiac MRI reported no structural heart disease.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}` -> followup_outputs[request_structured_headache_history_ichd3]: instantaneous while bending over in the garden, 45 minutes before arrival; red flags: thunderclap onset, transient confusion at onset, new headache type after age 50, anticoagulant use (apixaban). The library reported no thunderclap onset, no red flags and no nausea or photophobia, against the history.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}` -> followup_outputs[request_orthostatic_blood_pressure]: standing not attempted, supine BP 176/102 as at arrival. The library reported 3 minutes of symptom-free standing at BP 128/78.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}` -> followup_outputs[request_levodopa_challenge]: no parkinsonian signs, challenge not performed. The library reported normal gait and postural reflexes and no nausea in a patient who cannot stand and is vomiting.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k SAH-S04` passed; no criterion answer changed (snapshot diff); every mapped order is answered without the library (`verify.py`).
