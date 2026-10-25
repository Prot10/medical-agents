# HEP-ENC-P08
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 8465dace-a469-4e91-9c69-c28052b0c7f5 | FIXED | The urine culture criterion (`action-9-order-microbiology`) and its output (`request_urine_specimen`) are deleted, because the urinalysis in the labs is clean. Blood cultures (`action-8-order-microbiology`) are now optional and take the specimen as their only argument. The rationale says why: afebrile, WBC 5.6 with a normal differential, lactate 1.4, and an obvious precipitant. The initial `microbiology` block now reads "no growth at 48 hours" with `collected_before_antimicrobials` null. Both culture ids are out of the stop rule. |
| ee768920-f1c3-4cd9-9e9f-1577dcd8a6fb | FIXED | Type C everywhere. `accepted[0]` reads "Recurrent overt hepatic encephalopathy, type C, West Haven grade II, with a large spontaneous splenorenal portosystemic shunt as the dominant mechanism ...". The two "type B/C" pearls are replaced by one pearl: HE in cirrhosis is type C with or without a shunt, and type B is bypass without liver disease [ACG_HE_2026]. The literature output (F2), which carried "type B or mixed type B/C", is deleted, along with the literature criterion whose expected evidence said "type B/C". |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `diagnosis.accepted[0]`, `past_medical_history[0]`, HPI | The case stated "Child-Pugh A, MELD 7", undated. Recomputed (C10): Child-Pugh A (6: bilirubin 1.1 1, albumin 3.8 1, INR 1.1 1, no ascites 1, grade II HE 2), MELD 8, MELD-Na 8. The label also called the cirrhosis "compensated", but recurrent overt HE is a decompensating event. | FIXED: the label now reads "cirrhosis with preserved liver function (Child-Pugh A, MELD-Na 8)". The undated scores are removed from the HPI and PMH. The 6-month-old hepatology note quoting "MELD 7" stays as dated history (C13). |
| B | major | `neurological_exam.mental_status` | The exam (GCS 12 E3V4M5, disoriented to time and place, unable to follow commands) describes West Haven grade III, not the grade II in the label. | FIXED: GCS 14 (E4V4M6), lethargic but rousable, disoriented to time, oriented to person and place, follows one-step commands, asterixis. This is grade II, which matches the label and the Child-Pugh HE points. |
| A | major | `action-4-search-medical-literature`, F2 | Required literature search whose output echoes the expected evidence (C4). | FIXED: criterion and F2 deleted; `initial_tool_outputs.literature_search` set to null. |
| A | minor | F1 MRI, F4 EEG | The decisive MRI and EEG were follow-ups behind trigger tokens (plan). | FIXED: moved to the initial `mri` (structured white matter finding, technique line, numbered impression) and the initial `eeg` (en dashes removed). MRI and CT required; EEG recommended (C8, 3.1). |
| C | major | new `action-abdominal-shunt-imaging`, `initial_tool_outputs.body_imaging` | The case's mechanism (the shunt) had no work-up, and its must asked for abdominal imaging that the policy did not score (C15). The `vocab_gap` said no such tool existed, but `order_body_imaging` now provides one. | FIXED: recommended `order_body_imaging` `{"study": "pelvis_abdomen_CT", "contrast": true}`, with `pelvis_abdomen_MRI` and `pelvis_abdomen_ultrasound` as alternatives. The initial report shows a 14 mm splenorenal shunt into the left renal vein, a patent portal vein without thrombus, a cirrhotic liver without a focal lesion, splenomegaly of 15 cm, no ascites, and a non-obstructing left renal stone (consistent with the history). `vocab_gap` is emptied. |
| C | major | `action-5-check-drug-interactions`, F3 | Required, with template text and wording such as "standard secondary prophylaxis per AASLD" (C5). | FIXED: optional, with alternatives lactulose, rifaximin and aspirin. The output is renamed `check_lactulose_rifaximin_aspirin` and placed last. It reports: no relevant interaction; aspirin adds bleeding risk with platelets of 122 and its indication should be reviewed; atorvastatin and amlodipine can continue at Child-Pugh A; no cross-reactivity with the sulfonamide allergy; avoid sedatives. |
| B | minor | `initial_tool_outputs.ct`, `.labs` | CT findings were empty. TSH 2.1 and zinc 82 were template values. CRP was missing. The summary carried interpretive comments. | FIXED: canonical normal CT; TSH 1.6, zinc 66, CRP 1.8 mg/L; the summary and interpretation list the flagged values only. |
| A | minor | `action-1-interpret-labs` | Nine named panels were demanded. | FIXED: the two-alternative core (C9). |
| C | major | `assessment` | Lactulose 30 mL TID without the canonical loading dose. The precipitant must ("dietary precipitant (high protein meal)", dietary counselling) implied protein restriction. Generic LP prohibition. "Escalate antiplatelet therapy (add clopidogrel, DOAC)" called a DOAC an antiplatelet. Imaging written as a must. | FIXED: MUST-LACT; rifaximin for recurrence; HE despite preserved function; reclassify the TIA episodes and stop the aspirin started for them unless a vascular indication is confirmed; precipitants (constipation, a check for GI bleeding, protein 1.2-1.5 g/kg/day in small meals with a late-evening snack); hepatology referral and a discussion of shunt embolization with IR if HE recurs despite lactulose and rifaximin (plan). Prohibitions: the TIA anchor, dismissing HE because synthetic function is preserved, PROHIB-BZD, sedating opioids (acetaminophen up to 2 g per day), antithrombotic escalation, protein restriction. LP line deleted. |
| C | minor | `ground_truth.differential` | TIA and NCSE were rated moderate after the MRI and EEG (C14). The metabolic entry called ammonia "the only markedly abnormal metabolic parameter". | FIXED: TIA and NCSE are now low, each naming its excluding result. The other entries state what the case shows. |
| C | minor | `key_clinical_evidence`, `red_herrings` | One pearl said "diagnosis rests on hyperammonemia". `red_herrings[2]` pointed to a follow-up path and to the fallback echo. | FIXED: K_CLIN, K-AMM, a score line, the type C pearl, the clinical basis of the diagnosis, TIA versus HE, a precipitants and protein pearl, an embolization pearl and the EEG pearl. `red_herrings[2]` now points to `initial_tool_outputs.mri.impression` (MRI only). |
| E | minor | criteria, metadata | Every rationale repeated its label, and citations were free text (C17). | FIXED: one-sentence rationales with keys. The difficulty fields are rewritten, and `citation_gap` is emptied now that embolization is in a cited must. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now requires the core labs, a head CT and a brain MRI. It recommends the EEG and a contrast CT of the abdomen, which shows the 14 mm splenorenal shunt and a patent portal vein. Blood cultures and the medication check are optional. The urine culture, the literature search and the follow-up indirection are gone: the MRI (no acute infarct, mild small-vessel change) and the EEG (diffuse slowing, triphasic-like waves, no epileptiform activity) are now the initial reports. The exam now matches grade II (GCS 14, disoriented to time only, asterixis). The label reads recurrent overt HE, type C, grade II, with the shunt as the dominant mechanism, Child-Pugh A and MELD-Na 8 (stated MELD 7). TIA and NCSE are rated low. The musts are:
- lactulose by the canonical regimen, plus rifaximin
- recognizing HE despite preserved liver function
- reclassifying the prior TIA episodes and stopping the aspirin started for them
- treating the precipitants with normal protein intake
- discussing shunt embolization with interventional radiology if HE recurs

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`.
- `accepted[0]` changed under ruling 3 (C10 scores; type C per note ee768920). ICD codes and synonyms are unchanged. K76.82 (hepatic encephalopathy, the FY2023 code) sits beside K72.90/K72.91. Check whether the synonym set should keep "hepatic coma" for a grade II case.

## Open questions for Andrea (judgment calls you could not settle)

- Shunt imaging tier: the plan allows optional "if the HPI gives dated shunt imaging". The history does mention the CT from 18 months ago, but it was a renal stone study that found the shunt incidentally, with no diameter or portal vein assessment. I kept the imaging recommended because embolization planning needs that information.
- An ultrasound or MRI order also receives the CT report, because the MockServer serves the first order of a tool from the single initial output. The report gives the modality, so the result is honest about what was done. A per-study follow-up would need the library or MockServer to choose outputs by parameter.
- Transplant referral: recurrent overt HE is a decompensating event, but liver function is preserved (MELD-Na 8) and the mechanism is the shunt. I added no MUST-TX, and the plan names none for P08. Confirm.
- Aspirin: the must says to stop the aspirin unless a vascular indication is confirmed. He is 70 with hypertension, diabetes and a smoking history, and the aspirin was prescribed only for the TIA label. A reviewer may prefer "review" over "stop".

## Verification

Adversarial check, 23 Oct 2026. Read the log, the diff and the whole final case. Recomputed: Child-Pugh A 6 (grade II HE 2 points), MELD 8, MELD-Na 8 (MELD 11 or less, so no sodium term). Both notes are fixed everywhere: "type C" in the label and the pearl, no "type B/C" left; the urine culture criterion and output are deleted and blood cultures are optional with specimen-only arguments. The rewritten exam (GCS 14, disoriented to time only, asterixis) now supports grade II, which the label and the Child-Pugh points use; the MRI and EEG are initial reports, TIA and NCSE are low with their excluding results, and the new shunt-imaging criterion is answered by a contrast CT report consistent with the history (14 mm splenorenal shunt, patent portal vein, left renal stone). The protein advice (1.2-1.5 g/kg/day, late-evening snack) and shunt embolization for recurrence despite lactulose and rifaximin match EASL 2022. The 6-month-old hepatology "MELD 7" stays as dated history.

Found and fixed one inconsistency the exam rewrite left: `patient.neurological_exam.gait` still read "he cannot cooperate with testing" although he now follows one-step commands; it reads "Not assessed: too lethargic to stand safely." `perfect_agent.py` and `case_io.py check` clean after the edit.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Discriminators and vocabulary (24 Oct 2026)

Consequence of the modality fix: the shunt CT now answers only CT orders, so the MRI alternative of `action-abdominal-shunt-imaging` got the library normal. Added the follow-up `request_contrast_mri_abdomen_portosystemic_shunt` (same shunt, portal vein, liver and spleen; the 4 mm stone is not claimed on MRI) and removed the `pelvis_abdomen_ultrasound` alternative: the criterion is contrast-enhanced shunt mapping for possible embolization [EASL_HE_2022], which Doppler ultrasound does not provide.

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `initial_tool_outputs.body_imaging.modality` "CT with IV contrast, portal venous phase" -> `CT` (a body-imaging modality term; the Doppler or contrast detail stays in the findings and the `contrast` field).
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-8-order-microbiology` rationale: "Optional: afebrile, white cell count 5.6 with a normal differential, lactate 1.4, a clean urinalysis and an obvious precipitant (constipation after a large protein load)." -> "Afebrile, white cell count 5.6 with a normal differential, lactate 1.4, a clean urinalysis and an obvious precipitant (constipation after a large protein load)."

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia]; now [CBC, CMP, coagulation, ammonia, CRP, tox_screen] | [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia].
- `ground_truth.action_criteria[action-1-interpret-labs]`.expected_evidence: was "Bilirubin 1.1 mg/dL, albumin 3.8 g/dL, INR 1.1, creatinine 1.0 mg/dL, sodium 139 (Child-Pugh A, MELD-Na 8); platelets 122 x10^9/L; glucose, electrolytes, CRP, TSH and ethanol normal; ammonia 118 µmol/L, consistent with HE but not a measure of its grade."; now "Bilirubin 1.1 mg/dL, albumin 3.8 g/dL, INR 1.1, creatinine 1.0 mg/dL, sodium 139 (Child-Pugh A, MELD-Na 8); platelets 122 x10^9/L; glucose, electrolytes, CRP and ethanol normal; ammonia 118 µmol/L, consistent with HE but not a measure of its grade.".
- Decision: serve: new first alternative (old order kept as an alternative) + trim evidence. The label names CRP with the core bloods (infection is the precipitant to exclude) and the evidence reads it; CBC, CMP, coagulation and ammonia did not return the inflammatory panel. The label adds toxicology where alcohol is in question (serum ethanol). The normal TSH is not part of this order and is trimmed.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
