# HEP-ENC-M06
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 3e28b7bf-e9cb-457a-b79d-7249dd50c413 | FIXED | The response panel (`request_lactulose_rifaximin`: ammonia 94 to 42 at 72 hours, stool frequency after adjustment) deleted, together with the post-repletion potassium and creatinine panel (`request_potassium_repletion`, ruling 4). One admission ammonia (94 µmol/L, range 11-51) stays. K-AMM pearl added (`key_clinical_evidence[1]`); the lactulose pearl (`[4]`) titrates to stool frequency, and a prohibition forbids titrating lactulose to the ammonia. |
| 167526a9-3633-4aee-b365-7b5ecf77bbcb | FIXED | TIPS Doppler `action-5-order-body-imaging` is now required (arguments `{"study": "pelvis_abdomen_ultrasound"}`) and in the stop rule; the report moved from the follow-up to `initial_tool_outputs.body_imaging` with clearly patent in-stent velocities 112, 124 and 136 cm/s (reference 90-190 cm/s), main portal vein 42 cm/s hepatopetal, no stenosis or thrombosis, no ascites, splenomegaly 15 cm. The TIPS-malfunction differential is now `low` with the Doppler result; the old "Confirm TIPS patency" must is replaced by the TIPS-reduction must (plan). |
| f90a4875-04bb-4ca6-a73d-99babd903035 | FIXED | Blood and urine cultures (`action-7`, `action-8-order-microbiology`) recommended as an occult-infection screen (afebrile, WBC 7.8, no source), specimen-only arguments, case results ("no growth at 48 hours"; concentrated urine without pyuria); `collected_before_antimicrobials` null, since no antibiotic is given. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.diagnosis.accepted[0]`, `past_medical_history[0]` | "Child-Pugh B" (label) and "MELD 13" not derivable; grade "II-III" while the exam (disoriented x3, somnolent) supports III: computed Child-Pugh C (12), MELD 21, MELD-Na 21 (C10). | FIXED: label "West Haven grade III ... (Child-Pugh C, MELD-Na 21)"; prior score dated "before TIPS placement 4 months ago"; score pearl `key_clinical_evidence[2]`. |
| B | major | `patient.history_present_illness` | "Lactulose overdose" in the label but the listed dose (30 mL three times daily) is standard and nothing showed overuse. | FIXED: HPI adds that a lactulose bottle refilled 10 days earlier was nearly empty, about twice the prescribed amount. |
| B | minor | `patient.neurological_exam.mental_status` | GCS motor 4 (withdraws) contradicted "unable to follow multi-step commands" (implies obeying simple ones). | FIXED: GCS 13 (E3V4M6), "follows single-step but not multi-step commands". |
| C | major | `fallback_tool_outputs.ecg`, new `initial_tool_outputs.ecg`, new `action-ecg-hypokalemia-qtc` | Potassium 2.6 in a patient on escitalopram with no ECG in the policy, and the fallback ECG (QTc 434 ms, no U waves) contradicted the potassium. | FIXED: initial ECG with ST depression, T flattening, U waves, QTc 485 ms (QT 400 ms at rate 88); required ECG criterion; fallback ECG removed (`fallback_tool_kinds.ecg` dropped). |
| C | major | `action-4-check-drug-interactions`, follow-up `check_escitalopram_liver_interaction` | Template expected evidence; the output stated a false 5 mg maximum for escitalopram in Child-Pugh B (labels give 10 mg) and suggested mirtazapine; metformin with AKI and decompensated cirrhosis not addressed (C5). | FIXED: required (plan); alternatives escitalopram, potassium chloride, metformin, lactulose; one output `check_escitalopram_potassium_metformin_lactulose`, placed last: QT with low K and Mg, 10 mg maximum, metformin contraindicated, SSRI bleeding and hyponatremia, PPI review, potassium infusion rate. |
| A | minor | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, output null. |
| C | major | `followup_outputs` (MELD panel) | Transplant score panel delivered through `interpret_labs` (C1). | FIXED: deleted; MUST-TX with MELD-Na 21. |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" without values; template TSH 2.1 and zinc 82; no CRP; ethanol value "< 10 mg/dL" repeating its unit; hemoglobin and platelets missing from the summary (C9). | FIXED: magnesium 1.6 mg/dL (low, consistent with diarrhea), lactate 1.6, CRP 4.0, TSH 1.9, zinc 64; ethanol "<10" mg/dL; summary and interpretation list every flagged value. |
| A | minor | `action-1-interpret-labs` | Nine named panels demanded. | FIXED: two-alternative core plus `magnesium` (see Open questions). |
| C | major | `ground_truth.differential`, `key_clinical_evidence[3]` (old), `red_herrings[1]` | TIPS occlusion presented as a cause of worsening HE (moderate); in fact dysfunction causes recurrent ascites or bleeding, and HE reflects a patent shunt. "Post-TIPS expected HE" left moderate although a clear precipitant is present. | FIXED: TIPS dysfunction low with the Doppler result; post-TIPS HE without precipitant low; post-TIPS pearl rewritten; TIPS red herring states the patent shunt and the reduction threshold. |
| C | minor | `ground_truth.differential`, `red_herrings[0]` | Escitalopram described as accumulating at a "supratherapeutic" dose; alcohol relapse not addressed though he "denies alcohol use"; HRS entry without the ICA criterion. | FIXED: escitalopram low (dose within hepatic maximum, QT relevance); alcohol intoxication or withdrawal added (low: ethanol <10, CIWA 3); HRS-AKI after 48 hours of albumin. |
| C | major | `ground_truth.assessment` | Lactulose must without the overuse correction text; vague potassium and AKI musts; "Confirm TIPS patency" as a must; metformin continued during AKI; escitalopram with prolonged QTc not addressed; no transplant referral; haloperidol boilerplate (C12); generic LP prohibition. | FIXED: MUST-LACT-OVERUSE (MUST-LACT's hourly loading omitted in a patient with 8-10 stools, see Open questions), MUST-K with IV KCl under ECG monitoring and magnesium, AKI with crystalloid then albumin per EASL 2018, hold metformin, hold escitalopram until QTc normal then at most 10 mg, continue rifaximin, TIPS reduction if HE recurs, pantoprazole review, MUST-TX. Prohibitions: PROHIB-BZD, opioids (acetaminophen up to 2 g per day), lactulose escalation or ammonia titration, opioid antidiarrheals. LP line deleted. |
| B | minor | `initial_tool_outputs.ct` | Empty findings; "restricted diffusion" on CT (C8). | FIXED: canonical normal CT. |
| A | minor | `ground_truth.action_criteria` | The case has an EEG report but no EEG criterion. | FIXED: recommended `action-6-analyze-eeg` (new; that id was unused), expected generalized delta-theta slowing with atypical triphasic-like waves; EEG impression closes with "Clinical correlation recommended." |
| E | minor | criteria, citations, metadata | Rationale = label; free-text citations; metadata "4 required tools + IR consult" and "escitalopram dosing error". | FIXED: one-sentence rationales with keys; metadata rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy requires the core labs (with magnesium), a 12-lead ECG, the TIPS Doppler and a drug check; blood and urine cultures (afebrile, WBC 7.8) and EEG are recommended, CT optional. The HPI now shows the lactulose overuse (a bottle refilled 10 days earlier nearly empty), and the exam's GCS (13, E3V4M6) matches what he does. The label reads West Haven grade III, Child-Pugh C (12 points), MELD-Na 21. The serial ammonia, the post-repletion potassium and creatinine, the MELD panel and the literature search are gone. Labs report magnesium 1.6 (low), lactate, CRP and case-specific TSH and zinc in place of the "Exclusion studies" block. A new ECG shows U waves and QTc 485 ms with potassium 2.6 on escitalopram. The TIPS Doppler is clearly patent (112-136 cm/s against 90-190), and the differential no longer claims that a blocked TIPS causes HE. Musts: reduce lactulose to 2-3 stools and investigate persisting diarrhea, IV potassium under ECG monitoring with magnesium, crystalloid then albumin for the AKI, hold metformin, hold escitalopram until the QTc normalises then at most 10 mg, continue rifaximin, TIPS reduction only if HE recurs, review pantoprazole, transplant referral. Prohibitions: sedatives, opioids, lactulose escalation or ammonia-guided titration, opioid antidiarrheals.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`.
- `accepted[0]` changed under ruling 3 (C10 scores; grade II-III to III per plan 1.2); ICD codes and synonyms unchanged.
- The new ECG criterion has no citation: none of the allow-listed sources covers ECG monitoring in hypokalemia.

## Open questions for Andrea (judgment calls you could not settle)

- ECG added as a required criterion (not in the plan): potassium 2.6 with a QT-prolonging drug makes an ECG standard care before IV potassium, and the drug check the plan requires rests on the QT question. If you prefer it recommended, the stop rule loses it.
- Magnesium added to the core lab criterion (plan gives no extra for M06): severe hypokalemia from diarrhea needs a magnesium level for repletion to hold.
- MUST-LACT (25 mL every 1-2 hours until two soft stools) is not in this case: it would be wrong in a patient with 8-10 loose stools a day. MUST-LACT-OVERUSE carries the 2-3 stool target instead.
- The lactulose-overuse history (bottle nearly empty) is new data added so that the case supports its labelled precipitant.
- Grade III follows plan 1.2 (the exam supports the upper bound: disoriented to time, place and person, eyes open to voice); this moves Child-Pugh to C, as the plan computed.

## Verification

Checked (adversarial verifier, 23 Oct 2026): all three note ids (3e28b7bf, 167526a9, f90a4875) are in the table and fixed in the file (no serial ammonia or post-repletion panel; TIPS Doppler required, in the stop rule, answered by `initial_tool_outputs.body_imaging` with 112-136 cm/s against 90-190; TIPS dysfunction low; cultures recommended with null `collected_before_antimicrobials`). Recomputed: Child-Pugh C 12 (bilirubin 3.4, albumin 2.5, INR 1.7, no ascites, grade III), MELD 21 (21.5 before rounding to the tenth, UNOS 21), MELD-Na 21 (sodium 142 bounded at 137); QTc 400 / sqrt(60/88) = 484 ms, stated 485. Grade III is supported by the exam (disoriented x3, eyes open to voice). The fallback ECG that contradicted the potassium is gone and the new required ECG is answered by the initial output; escitalopram 10 mg as the hepatic maximum and the metformin hold are correct; MUST-LACT-OVERUSE replaces the hourly loading dose appropriately in a patient with 8-10 stools a day; prohibitions (no lactulose escalation, no loperamide) agree with the musts. Differential matches the Doppler, ethanol and CIWA results.

Found: no error that needed a change. The new ECG criterion has no citation (logged by the worker under CENTRAL).

Changed: nothing. `perfect_agent.py` and `case_io.py check` clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `initial_tool_outputs.body_imaging.modality` "Doppler ultrasound" -> `ultrasound` (a body-imaging modality term; the Doppler or contrast detail stays in the findings and the `contrast` field).
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-2-order-ct-scan` rationale: "Optional: no focal deficit, seizure or known head trauma, but he lives alone and was unreachable for 3 days, so an unwitnessed fall cannot be excluded." -> "No focal deficit, seizure or known head trauma, but he lives alone and was unreachable for 3 days, so an unwitnessed fall cannot be excluded."

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia, magnesium] | [CBC, BMP, LFTs, coagulation, ammonia, magnesium]; now [CBC, CMP, coagulation, ammonia, magnesium, CRP] | [CBC, CMP, coagulation, ammonia, magnesium] | [CBC, BMP, LFTs, coagulation, ammonia, magnesium].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP with the core bloods (infection is the precipitant to exclude) and the evidence reads it; CBC, CMP, coagulation and ammonia did not return the inflammatory panel.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: Cognitive screening could not be completed: the patient could not sustain attention or follow the test instructions. No valid score was obtained. (fallback_tool_outputs.clinical_assessment). Why: disoriented to person, place and time, perseverative, following single-step but not multi-step commands: no MoCA can be completed.
- `order_specialized_test {test_type: neuropsych_battery}`: Formal neuropsychological testing could not be administered at this level of arousal and attention. No domain scores were obtained. (fallback_tool_outputs.specialized_test). Why: disoriented to person, place and time, perseverative, following single-step but not multi-step commands: a battery cannot be administered.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 30, ECOG 4. Severely disabled, completely bed-bound and dependent for all care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Timed gait and balance testing was not possible: cannot stand or walk safely. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: cannot stand or walk safely.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: mildly hypophonic speech; articulation intact; perseverative output, repeatedly asking the same question; follows ... (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: mildly hypophonic speech; articulation intact; perseverative output, repeatedly asking the same question.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Generalized delta-theta slowing at 3–5 Hz, moderately disorganized background, absent posterior dominant rhythm. 2. (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Generalized delta-theta slowing at 3–5 Hz, moderately disorganized background, absent posterior dominant rhythm. 2. Intermittent ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: marked reduction of myo-inositol (mI/Cr 0.16) and choline (Cho/Cr 0.50) with an increased glutamine-glutamate (Glx) peak; NAA ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Opacified TIPS ... (fallback_tool_outputs.body_imaging). Why: cirrhosis with no ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. TIPS lumen not assessable on MRI; patent main ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with no ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; normal white cell morphology; platelets reduced in number, of normal morphology, without ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 98: 'adequate platelets' contradicts it.
- `interpret_labs {panels: [HbA1c]}`: 6.4 (fallback_tool_outputs.labs[HbA1c]). Why: treated or known diabetes: HbA1c 6.4%.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-M06` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
