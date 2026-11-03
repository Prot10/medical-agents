# HEP-ENC-M03
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b8fd889d-9eaa-47eb-8317-780425e3f589 | FIXED | Duplicate TSH 2.1 mIU/L (`initial_tool_outputs.labs.panels.TSH`) deleted together with the "Exclusion studies" block; the Thyroid panel keeps TSH 8.4 µIU/mL with free T4 0.7 ng/dL. The levothyroxine increase that sat in a drug-interaction follow-up (`request_thyroid_treatment`, ruling 4) is now a must; the hypothyroid red herring (`red_herrings[1]`) points at `initial_tool_outputs.labs.panels.Thyroid[0]`. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.diagnosis.accepted[0]`, `past_medical_history[0]` | "Child-Pugh B, MELD 12" not derivable: computed Child-Pugh B (9), MELD 13, MELD-Na 16 (C10). | FIXED: label "Child-Pugh B, MELD-Na 16"; history score dated ("at her last clinic review"); score pearl added. |
| B | major | `patient.clinical_history.medications` | Methadone 80 mg daily (social history, HPI, exam, toxicology) and the trimethoprim-sulfamethoxazole started a week ago (HPI) were missing from the medication list. | FIXED: both added. The plan calls the methadone check a carry-over "for a drug she does not take"; she does take it (see Open questions). |
| C | major | `followup_outputs` (lactulose/rifaximin, thyroid treatment, methadone check, literature) | Ammonia 72 to 44 "post-lactulose increase + rifaximin" (C1, C2); levothyroxine dosing filed as a drug check; methadone check that ordered an ECG; literature follow-up (C4). | FIXED: all deleted; a single real drug-interaction follow-up placed last. |
| C | major | `followup_outputs` (`interpret_labs` paracentesis) | Ascites present but the tap was filed under `interpret_labs` with no criterion (C6). | FIXED: new required `action-diagnostic-paracentesis` (`order_microbiology`, `ascitic_fluid`); the report (PMN 45, SAAG 1.6) moved to microbiology with total protein 1.3 g/dL, ascitic albumin 1.2 g/dL, Gram stain and one culture time point. |
| D | major | `action-3-search-medical-literature` | Required literature search (C4). | FIXED: deleted (no initial output existed). |
| C | major | `action-4-check-drug-interactions` | Required with template expected evidence; the real interaction (trimethoprim with spironolactone, hyperkalaemia; with methadone, QT) was absent. | FIXED: recommended (plan says optional; see Open questions), alternatives name the drugs, output with real content. |
| C | major | `ground_truth.assessment` | Lactulose 2-4 stools (C3); "Rifaximin ... restart if interrupted" and a prohibition about rifaximin with TMP-SMX although she is not on rifaximin; counselling to avoid broad-spectrum antibiotics for "gut flora"; boilerplate opioid prohibition contradicting methadone maintenance; generic LP prohibition. | FIXED: MUST-LACT; precipitant must (constipation, lactulose adherence, treat the UTI); rifaximin added because the episode occurred on lactulose prophylaxis; stop TMP-SMX at course end and check potassium; levothyroxine adjustment with recheck at 6-8 weeks; continue methadone without abrupt change; MUST-TX (MELD-Na 16, decompensated). Prohibitions: PROHIB-BZD; no additional opioids or sedatives beyond methadone, acetaminophen up to 2 g per day; LP and rifaximin lines deleted. |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" block; template zinc 82; no CRP; toxicology reference range "Methadone maintenance - expected" (interpretation in the range field) with a positive screen flagged normal (C9). | FIXED: magnesium 2.0 mg/dL and lactate 1.1 mmol/L with ranges, CRP 4.0 mg/L, zinc 70; drug screen reference "Negative", positive flagged; summary and interpretation complete. |
| A | minor | `action-1-interpret-labs` | 9 named panels demanded. | FIXED: two-alternative core. |
| C | major | `action-7`, `action-8-order-microbiology` | Cultures required "before the first antimicrobial dose" in an afebrile patient with WBC 6.2 (C7). | FIXED: recommended screen, specimen-only arguments; urine rationale names the UTI treated this week. |
| B | major | `initial_tool_outputs.microbiology`, urine follow-up | "Specimen taken before the first antimicrobial dose" while she has been on trimethoprim-sulfamethoxazole for a week; "No organism isolated to date". | FIXED: `collected_before_antimicrobials` false for blood, urine and ascitic specimens, stated in the impressions; one time point. |
| B | minor | `initial_tool_outputs.ct` | Empty findings; "restricted diffusion" on CT (C8). | FIXED: canonical normal CT plus mild atrophy. |
| C | minor | `ground_truth.differential` | Hypothyroid encephalopathy left moderate; "rapid lactulose response" (a deleted follow-up) used as evidence; SBP entry conditional ("if ascites present") though ascites is documented; methadone not considered. | FIXED: hypothyroid encephalopathy low (contributor); opioid toxicity added (low); SBP low with PMN 45; MCI entry without the response argument. |
| C | minor | `ground_truth.red_herrings`, `metadata.difficulty_description` | Metadata names a "methadone red herring" that did not exist; the opioid-positive screen is a real distractor. | FIXED: red herring added (opioid-positive screen on maintenance, therapeutic level). |
| C | minor | `key_clinical_evidence[3]` (old) | "Broad-spectrum antibiotics disrupt the gut microbiome on which lactulose/rifaximin efficacy depends; ... under-recognized HE precipitant" overstated a speculative mechanism. | FIXED: hedged pearl; label precipitant text kept (see Open questions). |
| E | minor | criteria, citations, pearls, metadata | Rationale = label; free-text citations; "(AASLD 2014)". | FIXED: one-sentence rationales with keys, K-AMM, score pearl, difficulty rationale updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy requires the core labs and a diagnostic paracentesis (ascitic PMN 45 cells/mm3, no SBP), and recommends blood and urine cultures as an infection screen, the EEG and a drug check; CT is optional. The duplicate TSH 2.1 is gone, so the thyroid panel reads only TSH 8.4 with free T4 0.7. The literature search, the serial ammonia, the levothyroxine "drug check" and the methadone check are deleted. The medication list now includes the methadone maintenance (80 mg daily) and the trimethoprim-sulfamethoxazole started a week ago, which the history already described; since she is on that antibiotic, every culture is marked as collected during therapy. The label reads Child-Pugh B (9 points), MELD-Na 16. Labs gain magnesium, lactate, CRP and a case-specific zinc, and the opioid-positive drug screen is flagged with a plain reference range; a red herring now covers it (therapeutic level, no toxicity). The drug check reports the trimethoprim-spironolactone hyperkalaemia risk and the possible QT effect with methadone. Musts: lactulose to 2-3 stools, treat constipation and the UTI and check lactulose adherence, add rifaximin (recurrence on lactulose), stop TMP-SMX at the end of the course and check potassium, increase levothyroxine with recheck at 6-8 weeks, continue methadone unchanged, and transplant referral. Prohibitions: sedatives, and no opioids beyond her methadone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`.
- `accepted[0]` changed under ruling 3 (C10 scores); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- Plan M03 calls F4 a methadone check "for a drug she does not take". Methadone 80 mg daily is in the social history, HPI, exam and toxicology; only the medication list lacked it. I deleted F4 as planned (it ordered an ECG and declared the level "no evidence of accumulation") but added methadone to the medication list and folded the relevant content into the new drug check.
- Plan M03 says DI optional. I made it recommended: trimethoprim-sulfamethoxazole with spironolactone is a documented hyperkalaemia interaction that changes management (stop the antibiotic at course end, check potassium).
- The label's precipitant "recent TMP-SMX antibiotic use (gut microbiome disruption reducing lactulose efficacy)" is a speculative mechanism; the better-supported precipitants are the constipation, missed doses and the UTI itself. I kept the label text apart from the scores (ruling 3) and dropped "rifaximin" from it, since she is not on rifaximin. A reviewer may want the precipitant reworded.
- Cultures stay recommended per plan, although the HPI contains a urinary tract infection (C7's "infective precipitant in the HPI" would make them required). She is afebrile, WBC 6.2, and already on treatment.
- Rifaximin was added as a must on the reading that lactulose "HE prophylaxis" means a prior overt episode; the history does not state the prior episode explicitly.

## Verification

Checked (adversarial verifier, 23 Oct 2026): note b8fd889d is in the table and fixed (TSH reported once, 8.4 with free T4 0.7; the red herring points at `Thyroid[0]`; the levothyroxine change is a must, not a drug check). Recomputed: Child-Pugh B 9 (bilirubin 2.2, albumin 2.8, INR 1.4, mild ascites, grade II), MELD 13, MELD-Na 16, consistent in label, key evidence and MUST-TX. Grade II fits the exam. Methadone and trimethoprim-sulfamethoxazole, already in the history, are now in the medication list, so `collected_before_antimicrobials` false on all three specimens is consistent. Ascitic PMN 45, SAAG 1.6 = 2.8 - 1.2; ascitic protein 1.3 g/dL does not meet the primary-prophylaxis criteria here (Child-Pugh 9 but bilirubin 2.2, creatinine 0.9, sodium 134). Drug-check content (trimethoprim-spironolactone hyperkalaemia, QT with methadone) is real and agrees with the allergies (codeine intolerance) and medicines. Differential updated to the results; no musts contradict prohibitions; no leakage in the patient block.

Found, not changed: the label keeps "recent TMP-SMX antibiotic use (gut microbiome disruption reducing lactulose efficacy)" as a precipitant while the case's own pearl (`key_clinical_evidence[5]`) calls that evidence limited, and antibiotics that reduce colonic flora are otherwise used to treat HE. The better-supported precipitants (constipation, missed doses, the urinary tract infection) are in the musts. Ruling 3 forbids rewording `accepted[0]` without a reviewer ruling, and the worker already raised it under Open questions; I support rewording the precipitant clause to "constipation, missed lactulose doses and a urinary tract infection under treatment" if Andrea agrees.

Changed: nothing. `perfect_agent.py` and `case_io.py check` clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- Leak guard (Andrea, 24 Oct 2026: any-query outputs must not repeat any criterion's expected evidence, including their own): `ground_truth.action_criteria[action-4-check-drug-interactions].expected_evidence` reworded as the conclusion a grader checks, in words not shared with the stored `check_drug_interactions` follow-up, whose report text is unchanged; clinical content unchanged.
- `ground_truth.diagnosis.accepted[0]`: the speculative mechanism "(gut microbiome disruption reducing lactulose efficacy)" removed; TMP-SMX is now a possible contributor (UTI treated in the past week), constipation the precipitant. ICD unchanged (summary open question, M03 precipitant mechanism).

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia]; now [CBC, CMP, coagulation, ammonia, CRP, thyroid, tox_screen] | [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP and the work-up searches for an infective precipitant (EASL 2022 / ACG 2026); CRP was not in the order, so the CRP the evidence reads was not returned; a must, the differential and a red herring rely on TSH 8.4 with free T4 0.7, and the label asks for toxicology on methadone.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-2-order-ct-scan` rationale: "Optional: there is no focal deficit, seizure or head trauma and the precipitants are clear, so brain imaging is not routine in cirrhosis with confusion." -> "There is no focal deficit, seizure or head trauma and the precipitants are clear, so brain imaging is not routine in cirrhosis with confusion."

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 19/30, below the normal range (26 or above), with impaired attention, executive function, delayed recall and orientation to time; naming preserved. (fallback_tool_outputs.clinical_assessment). Why: GCS 13, disoriented to time with slowed processing: a MoCA of 28/30 with full orientation is impossible.
- `order_specialized_test {test_type: neuropsych_battery}`: Abnormal neuropsychological profile dominated by slowed psychomotor speed and impaired attention and executive function, with a retrieval-type memory deficit ... (fallback_tool_outputs.specialized_test). Why: disoriented to time with slowed processing: a battery normal in every domain is impossible.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3. Requires considerable assistance and frequent supervision; capable of only limited self-care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Slowed gait with impaired dynamic balance: Timed Up and Go 15.8 s (above the 13.5 s fall-risk threshold) and 10 m walk speed 0.88 m/s; tandem gait not achieved. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: slightly unsteady.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: normal articulation; slow, effortful output with word-finding pauses and tangential answers; follows two-step commands. (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: normal articulation; slow, effortful output with word-finding pauses and tangential answers.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Generalized theta slowing at 5-7 Hz with occasional delta bursts, mildly disorganized background and absent ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Generalized theta slowing at 5-7 Hz with occasional delta bursts, mildly disorganized background and absent posterior dominant ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: reduction of myo-inositol (mI/Cr 0.28) and choline (Cho/Cr 0.58) with an increased glutamine-glutamate (Glx) peak; NAA preserved; no ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein. 4. Splenomegaly (13.6 cm). 5. ... (fallback_tool_outputs.body_imaging). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein. 4. Splenomegaly (13.6 cm). 5. ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; normal white cell morphology; platelets reduced in number, of normal morphology, without ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 104: 'adequate platelets' contradicts it.
- `interpret_labs {panels: [hepatitis_C_antibody]}`: Reactive (fallback_tool_outputs.labs[hepatitis_C_antibody]). Why: sustained virologic response after direct-acting antivirals two months ago: the antibody stays reactive.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-M03` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
