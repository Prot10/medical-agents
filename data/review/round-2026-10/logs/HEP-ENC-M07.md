# HEP-ENC-M07
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0ea62416-aa98-4374-a103-a97113084e95 | FIXED | Serial ammonia deleted: the `interpret_labs` `request_lactulose_rifaximin` follow-up (74 to 42 µmol/L at 48 h) is gone (C1/C2); one admission ammonia (74, range 11-51, flagged) stays in `initial_tool_outputs.labs.panels.Ammonia`. The label and the first red herring no longer use ammonia as proof of HE; K-AMM pearl added to `key_clinical_evidence`. Lactulose must replaced by MUST-LACT (2-3 soft bowel movements per day, ACG 2026 rec. 10; EASL 2022) in `assessment.required_recommendations[2]`. |
| 5a318475-2762-4603-aa62-372420761674 | FIXED | Afebrile (37.2 °C), WBC 7.4, no source: blood cultures (`action-7-order-microbiology`) and urine culture (`action-8-order-microbiology`) are now `recommended` with arguments `{"specimen": ...}` only, C7 recommended labels and rationale; the "before the first antimicrobial dose" wording and `before_antimicrobials` argument are gone; blocks report one time point ("no growth at 48 hours"), `collected_before_antimicrobials` null (no antibiotic in the case). Removed from the stop rule. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria` (new `action-diagnostic-paracentesis`), `followup_outputs[0]` | Ascites on exam (mild, on furosemide) but the tap was an `interpret_labs` follow-up with no criterion (C6). | FIXED: required `order_microbiology` `ascitic_fluid` criterion; output `request_diagnostic_paracentesis` with the stored PMN 62 and SAAG 1.4, plus WBC 190, total protein 1.6 g/dL, ascitic albumin 1.5 g/dL (consistent with serum 2.9 and SAAG 1.4), Gram stain and culture negative. |
| D | major | `action-3-search-medical-literature`, `followup_outputs[3]` | Required literature search (C4) with expected evidence echoing guidance. | FIXED: criterion and follow-up deleted; `initial_tool_outputs.literature_search` stays null. |
| C | major | `followup_outputs` (MELD panel `request_liver_transplant_evaluation`) | Transplant evaluation delivered as a lab panel (C1). | FIXED: deleted; MUST-TX added (decompensated with overt HE and ascites, MELD-Na 12). |
| B | major | `followup_outputs[2]` (DI), `action-4-check-drug-interactions` | DI output built around metformin, which she does not take; doses ("reduce glargine 25-30%", D10W) prescribed in the check; the real interaction (metoprolol blunting hypoglycemia warning) missing; expected evidence generic. | FIXED: DI kept required (C5, concrete issue: insulin in cirrhosis is the precipitant), output rewritten to her list (insulin in cirrhosis, metoprolol, lactulose/rifaximin no interaction, sedatives, sulfa allergy vs furosemide), placed last; case-specific expected evidence. |
| C | major | `ground_truth.diagnosis.accepted[0]`, `patient.clinical_history.past_medical_history[0]` | Scores not derivable: "Child-Pugh B, MELD 11"; computed MELD 12 / MELD-Na 12, Child-Pugh B 8 (C10). Label also used ammonia 74 as proof of HE. | FIXED: label "Child-Pugh B, MELD-Na 12", ending on persistent disorientation and asterixis; undated score removed from PMH; score pearl added to key evidence. |
| B | minor | `patient.neurological_exam.mental_status` | GCS 13 (E4V4M5) while she obeys commands (arm extension for asterixis). | FIXED: GCS 14 (E4V4M6). |
| C | minor | `past_medical_history[2]`, `red_herrings[1].data_point` | "Morbid obesity" with BMI 33.6 (class I obesity). | FIXED: "Obesity (BMI 33.6)" in both. |
| B | minor | `initial_tool_outputs.labs` | Two glucose rows (PoC 42 and post-D50W 84) in the BMP; "Exclusion studies" block with magnesium and lactate as "Within reference range"; template TSH 2.1 and zinc 82; insulin level filed under toxicology; INR and ammonia under LFTs; no CRP (C9). | FIXED: one glucose (42, drawn on arrival with the insulin level); magnesium 1.9 mg/dL and lactate 1.4 mmol/L with ranges; CRP 4.1 mg/L; TSH 1.6, zinc 66; insulin in an Endocrine panel; INR in Coagulation, ammonia in its own panel; summaries list only flagged values. Bedside glucose series stays in the exam. |
| B | minor | `initial_tool_outputs.ct` | Empty findings and "restricted diffusion" on CT (C8). | FIXED: canonical normal CT finding and impression. |
| B | minor | `initial_tool_outputs.microbiology` | Templated "No organism isolated to date. Specimen taken before the first antimicrobial dose" with no antibiotic in the case. | FIXED: "no growth at 48 hours", one time point, tests `culture`. |
| C | major | `assessment.required_recommendations` | Lactulose 2-4; rifaximin mandated at a first overt episode (rifaximin is add-on after recurrence); musts were partly vague. | FIXED: MUST-PRECIP (dextrose, glucose every 1-2 h), insulin must (reduce glargine, prandial lispro only with meals, education of patient and husband), MUST-LACT, MUST-TX. Rifaximin removed (see Open questions). |
| C | minor | `assessment.prohibited_recommendations` | Benzodiazepine line recommending haloperidol (C12); generic LP prohibition with no LP; acetaminophen dose unspecified; "NPH ... DKA risk" in a type 2 diabetic on glargine. | FIXED: PROHIB-BZD; opioid line with acetaminophen up to 2 g per day; LP line deleted; basal-insulin line reworded (glargine, rebound hyperglycemia). |
| C | minor | `ground_truth.differential` | Post-hypoglycemic impairment left moderate after correction; a mimic raised by the red herring (obesity hypoventilation) missing (ruling 7). | FIXED: post-hypoglycemic encephalopathy low with excluding features; SBP and stroke low with the excluding results; hypercapnic encephalopathy added very_low; DKA/HHS and insulinoma reworded. |
| D | minor | `red_herrings[0].correct_interpretation` | Used "ammonia 74" as the proof of HE. | FIXED: rests on persistent disorientation and new asterixis after correction. |
| A | minor | all `action_criteria` | Rationale repeated the label; citation lists mixed keys and free text; EEG label "consider only if no improvement"; CT label "before any LP" with no LP (C17). | FIXED: one-sentence rationales with keys; labels per plan; criteria reordered per plan 3.1 (labs, blood cultures, tap, urine, CT, EEG, DI). |
| E | minor | `patient.neurological_exam.additional`, `social_history.alcohol` | Capitals and dashes ("Insulin pump NOT used", "CRITICAL"), "Never — NASH cirrhosis". | FIXED: plain wording, same values. |
| E | minor | `metadata.difficulty_description`, `metadata.difficulty_rationale` | "ammonia 74 reveals concurrent HE"; "4 required tools and endocrine consult". | FIXED: reworded to the rebuilt policy. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is now: core labs (required), blood cultures (recommended), diagnostic paracentesis (required, PMN 62, culture negative), urine culture (recommended), non-contrast CT (optional), EEG (recommended), and the insulin medication review (required, last). The serial ammonia panel, the transplant MELD panel and the literature search are gone. The labs have one glucose (42 mg/dL, drawn with the insulin level of 48), real magnesium, lactate, CRP, TSH and zinc values, and one ammonia (74, range 11-51). The CT is a plain normal report. The drug check now covers her actual medicines: insulin in cirrhosis, metoprolol masking hypoglycemia, no interaction with lactulose or rifaximin, avoid sedatives, and furosemide is tolerated despite the sulfa allergy. The label reads Child-Pugh B (8), MELD-Na 12. GCS is corrected to 14 (E4V4M6) because she obeys commands. The musts are to treat the hypoglycemia with glucose monitoring, reduce glargine and give prandial lispro only with meals (with education), lactulose to 2-3 soft stools a day, and transplant referral. The prohibitions are no sedatives, no sedating opioids, and no abrupt stop of basal insulin. Post-hypoglycemic encephalopathy, SBP and stroke are now low, with the results that exclude them.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1 (`[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`).
- `accepted[0]` changed under ruling 3 (C10 scores; plan CENTRAL 6). No ICD or synonym change.

## Open questions for Andrea (judgment calls you could not settle)

- Rifaximin: the old must gave rifaximin 550 mg twice daily. The case describes prior minimal HE on lactulose and this as the first overt episode with a clear precipitant, so following the plan's "recurrent episodes only" rule I removed it from the musts. Reinstate it if you read the history as a recurrence.
- The HPI gives an EMS glucose of 42 mg/dL, partial improvement with oral gel, then an ED point-of-care glucose of 42 mg/dL again. This is plausible but slightly odd. I left it unchanged because the plan calls the EMS glucose legitimate history.

## Verification

Adversarial verifier, 23 Oct 2026. Read the log, the full diff and the final case.
- Both notes confirmed fixed: no serial ammonia anywhere (one admission ammonia 74, range 11-51); MUST-LACT gives 2-3; blood and urine cultures are `recommended` with `{"specimen": ...}` only and out of the stop rule.
- Scores recomputed from the printed labs: MELD 12, MELD-Na 12 (Na 137); Child-Pugh B 8 (bilirubin 1.8 1, albumin 2.9 2, INR 1.4 1, mild ascites 2, HE grade 2 2). The label, key evidence and MUST-TX agree.
- Paracentesis: required `ascitic_fluid` criterion, one output, PMN 62. SAAG arithmetic correct (2.9 - 1.5 = 1.4). Red-herring field paths resolve. No "2-4", no haloperidol, no LP line, no "restricted diffusion" on CT. The drug-interaction check routes correctly for "insulin", "glargine" and "metoprolol".
- Found and fixed: `ground_truth.differential[0].key_features` cited diffuse EEG slowing as evidence against post-hypoglycaemic encephalopathy. Diffuse slowing occurs in both, so it cannot discriminate. Now: asterixis appearing after correction points to a second process, and the EEG slowing does not separate the two.
- Left as is: the drug-interaction label and output mention rifaximin, which she does not take and the musts no longer give. This is harmless (no interaction stated). The worker's open questions (rifaximin, EMS glucose) stand. Some pre-existing em dashes remain in the HPI and mental status, which are old prose.
- `perfect_agent.py HEP-ENC-M07 -v` passes; `case_io.py check` reports no failure naming the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

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

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia]; now [CBC, CMP, coagulation, ammonia, CRP] | [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP with the core bloods (infection is the precipitant to exclude) and the evidence reads it; CBC, CMP, coagulation and ammonia did not return the inflammatory panel.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 17/30, below the normal range (26 or above), with impaired attention, executive function, delayed recall and orientation to time; naming preserved. (fallback_tool_outputs.clinical_assessment). Why: GCS 14, disoriented to time with slowed processing: a MoCA of 28/30 with full orientation is impossible.
- `order_specialized_test {test_type: neuropsych_battery}`: Abnormal neuropsychological profile dominated by slowed psychomotor speed and impaired attention and executive function, with a retrieval-type memory deficit ... (fallback_tool_outputs.specialized_test). Why: disoriented to time with slowed processing: a battery normal in every domain is impossible.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3. Requires considerable assistance and frequent supervision; capable of only limited self-care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Slowed gait with impaired dynamic balance: Timed Up and Go 16.2 s (above the 13.5 s fall-risk threshold) and 10 m walk speed 0.86 m/s; tandem gait not achieved. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: slightly unsteady.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: normal articulation; slow, sparse replies with delayed responses; follows two-step commands slowly. (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: normal articulation; slow, sparse replies with delayed responses.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Generalized theta slowing at 5-6 Hz with occasional 3-4 Hz delta bursts, mildly-moderately disorganized ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Generalized theta slowing at 5-6 Hz with occasional 3-4 Hz delta bursts, mildly-moderately disorganized background, absent ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: reduction of myo-inositol (mI/Cr 0.28) and choline (Cho/Cr 0.58) with an increased glutamine-glutamate (Glx) peak; NAA preserved; no ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology with increased echogenicity. 2. No focal liver lesion. 3. Patent portal vein. 4. ... (fallback_tool_outputs.body_imaging). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology with steatosis. 2. No focal liver lesion. 3. ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology with steatosis. 2. No focal liver lesion. 3. Patent portal vein. 4. ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; normal white cell morphology; platelets reduced in number, of normal morphology, without ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 118: 'adequate platelets' contradicts it.
- `interpret_labs {panels: [HbA1c]}`: 7.2 (fallback_tool_outputs.labs[HbA1c]). Why: treated or known diabetes: HbA1c 7.2%.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-M07` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
