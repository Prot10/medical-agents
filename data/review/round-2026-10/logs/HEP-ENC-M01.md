# HEP-ENC-M01
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| dec0d57a-9b9d-4d31-9774-25307651d25a | FIXED | Lorazepam-challenge cEEG follow-up (`followup_outputs`, trigger `request_continuous_eeg`) deleted; EEG criterion `action-5-analyze-eeg` expected evidence no longer mentions a challenge; prohibition 0 replaced by PROHIB-BZD (no haloperidol advice); `differential[3]` (NCSE) and `red_herrings[1]` rewritten so NCSE is excluded by the EEG itself, with no drug challenge. The EEG red herring was kept (rewritten) rather than deleted: its data point, the atypical triphasic-like waves, is still in the report and is a genuine distractor (see Open questions). |
| 22fa5945-b95c-4f89-998c-ed320ca71725 | FIXED | Gadolinium MRI follow-up (`order_advanced_imaging`, `request_mri_brain`) deleted; CSF criterion `action-6-analyze-csf` and its "see impression" CSF follow-up deleted; CT-before-CSF `sequence_constraints` entry deleted (now empty). CT stays optional with a rationale stating that no ACG imaging trigger is present. The LP prohibition was deleted with the LP. |
| 6a7d6fa7-7e8b-441a-b0f7-03310da85a3b | FIXED | Duplicate `interpret_labs` paracentesis criterion `action-8-interpret-labs` deleted (and from the stop rule); the single paracentesis criterion `action-10-order-microbiology` (required, `{"specimen": "ascitic_fluid"}`) now expects "Ascitic PMN 82 cells/mm3, below the 250 cells/mm3 threshold for SBP"; the ascitic report (`followup_outputs[0]`, trigger `request_diagnostic_paracentesis`) states units, Gram stain and one culture time point. The "see impression" CSF block is gone; the CT block now has findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.diagnosis.accepted[0]`, `patient.*.past_medical_history[0]`, HPI | Scores not derivable: "Child-Pugh B, MELD 14" for bilirubin 3.8, albumin 2.4, INR 1.8, Cr 1.2, Na 128, mild ascites, grade II HE. Computed Child-Pugh C (12), MELD 20, MELD-Na 26 (plan C10). | FIXED: `accepted[0]` "Child-Pugh C, MELD-Na 26"; the history score is kept as dated prior data ("at his last hepatology clinic review"); score pearl added. |
| C | minor | `accepted[0]` | Precipitant text listed "likely diuretic non-adherence" as a precipitant; the mechanism in the case is furosemide continued while spironolactone was taken irregularly, causing hypokalaemia; hyponatraemia is a co-precipitant (plan C14). | FIXED: precipitant wording; ICD codes unchanged. |
| B | major | `patient.neurological_exam.mental_status` | "Disoriented to time and place" is the West Haven grade III operative criterion (disoriented also for space), while the label, difficulty and plan say grade II. | FIXED: "disoriented to time. Oriented to place and person." (HPI already says he was not tracking time). |
| D | major | `patient.history_present_illness` | "urine toxicology confirmed no recent use" (scored labs result in the HPI, C13). | FIXED: removed; "He denied alcohol use." kept. |
| C | major | `followup_outputs` (lactulose/rifaximin, thiamine, transplant MELD panel) | Treatment response (ammonia 95 to 61 to 38, potassium after KCl), empiric thiamine level and a transplant-evaluation lab panel delivered through `interpret_labs` (ruling 4, C1, C2). | FIXED: all three deleted; content moved to musts (MUST-K, MUST-THIA, MUST-TX). |
| D | major | `initial_tool_outputs.literature_search`, `action-3-search-medical-literature` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, initial output null. |
| D | major | `initial_tool_outputs.drug_interactions` | Empty DI template whose summary was the expected evidence (C5). | FIXED: initial null; real follow-up `check_lactulose_metformin_furosemide` placed last. |
| C | major | `action-4-check-drug-interactions` | Plan says DI optional, but the case has a concrete issue: metformin 1000 mg twice daily in now decompensated (Child-Pugh C) cirrhosis, and furosemide with hypokalaemia once lactulose starts. | FIXED: DI recommended, alternatives `{"drug": "lactulose"}` or `{"drug": "metformin"}`; output flags metformin, lactulose-furosemide potassium loss, PPI review, sedatives; must "Stop metformin ... insulin". See Open questions. |
| C | major | `ground_truth.assessment.required_recommendations` | Lactulose target 2-4 stools (C3); rifaximin as an adjunct at a first episode (ACG 2026/EASL 2022: rifaximin is added after a recurrence); paracentesis listed as a must (it is a scored criterion); sodium limit "8-10" in a high-risk patient; thiamine justified by a deleted lab value. | FIXED: MUST-LACT, precipitant must, MUST-K with diuretic hold (EASL 2018: stop diuretics in overt HE), sodium limit 8 mEq/L per 24 h with the note that potassium raises sodium, MUST-THIA (poor intake), stop metformin, secondary prophylaxis with rifaximin only on recurrence, MUST-TX (MELD-Na 26), driving advice (truck driver). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Benzodiazepine line advised haloperidol; generic LP prohibition with no LP; acetaminophen dose unstated; ammonia line phrased as anchoring advice. | FIXED: PROHIB-BZD; opioid line with acetaminophen up to 2 g per day; LP line deleted; sodium limit 8; ammonia not to grade or monitor response (ACG 2026 rec 5). |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" block with magnesium and lactate as "Within reference range"; template TSH 2.1 and zinc 82; no CRP; summary incomplete (C9). | FIXED: block deleted; magnesium 1.9 mg/dL (BMP) and lactate 1.4 mmol/L added with ranges; TSH 1.7, zinc 67; CRP 3.1 mg/L added; summary and interpretation list every flagged value. |
| A | minor | `action-1-interpret-labs` | Criterion demanded 9 named panels (C9). | FIXED: two alternatives `[CBC, CMP, coagulation, ammonia]` / `[CBC, BMP, LFTs, coagulation, ammonia]`; canonical label and rationale. |
| C | major | `action-9`, `action-11-order-microbiology` | Blood and urine cultures required "before the first antimicrobial dose" in an afebrile patient with WBC 8.2 and no antibiotic in the case (C7). | FIXED: both recommended as an infection screen, arguments reduced to the specimen; case-specific expected evidence. |
| B | minor | `initial_tool_outputs.microbiology`, urine follow-up | "No growth reported at the time of this encounter" / "No organism isolated to date"; "collected before antimicrobials" true with no antimicrobial in the case (C7). | FIXED: one time point ("no growth at 48 hours"), flag null, urine block with microscopy and culture. |
| B | minor | `initial_tool_outputs.ct` | Empty findings; "restricted diffusion" on CT; "does not exclude early cerebral edema"; MRI suggestion (C8). | FIXED: canonical normal CT findings plus the case's mild atrophy; numbered impression; no recommendation. |
| B | minor | `initial_tool_outputs.eeg.findings[1]`, `impression` | Triphasic-like waves described as "asymmetric distribution" while the background symmetry is "Symmetric"; no clinical-correlation close. | FIXED: asymmetry removed, atypical morphology kept (no consistent phase lag, incomplete positive phase); close added. |
| C | minor | `ground_truth.differential` | Hyponatraemia as moderate alternative (C14); Wernicke entry cited the deleted thiamine level and MRI; SBP and NCSE cited follow-ups now deleted. | FIXED: hyponatraemic encephalopathy as sole cause low (co-precipitant); Wernicke low (wide-based gait, poor intake, no eye signs, no alcohol); SBP low (PMN 82); NCSE very low (EEG). |
| E | minor | `ground_truth.action_criteria[*].rationale`, citations | Every rationale repeated its label; free-text citations beside keys (C17). | FIXED: one-sentence rationales with keys only. |
| E | minor | `ground_truth.key_clinical_evidence` | "(AASLD 2014)" as the only source; no ammonia pearl. | FIXED: ACG 2026 / EASL 2022, K-AMM and the score pearl added. |
| E | minor | `metadata.difficulty_rationale` | Described the deleted literature, drug-check-as-required and consult steps. | FIXED: describes the current policy. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now requires the core laboratory work-up and a diagnostic paracentesis (ascitic PMN 82 cells/mm3, no SBP), and recommends blood and urine cultures as an infection screen (afebrile, WBC 8.2), the EEG and a drug check; the CT is optional because no ACG imaging trigger is present. The literature search, the gadolinium MRI, the lumbar puncture, the lorazepam EEG challenge, the serial ammonia/post-repletion potassium panel, the thiamine panel and the transplant-score panel are gone. The exam now reads "disoriented to time, oriented to place and person" so it supports grade II, and the HPI no longer gives the toxicology result. The label reads Child-Pugh C (12 points), MELD-Na 26, with hypokalaemia (furosemide continued while spironolactone was taken irregularly) and constipation as precipitants and hyponatraemia as a co-precipitant; the "MELD 14" in the history is dated as the last clinic review. Labs: the "Exclusion studies" block is replaced by magnesium 1.9 mg/dL and lactate 1.4 mmol/L, CRP 3.1 mg/L is added, and the template TSH and zinc values are replaced (1.7 and 67). The CT has real findings without "restricted diffusion", the EEG no longer calls the triphasic-like waves asymmetric on a symmetric background, and the cultures report one time point. The drug check flags metformin in decompensated cirrhosis, the potassium loss of lactulose with furosemide and the omeprazole indication. Musts: lactulose to 2-3 soft stools, treat the precipitants, potassium to 4.0 or more with diuretics stopped while overt HE and electrolyte disorders persist, sodium correction no faster than 8 mEq/L per 24 h, parenteral thiamine before glucose, stop metformin for insulin, lactulose secondary prophylaxis with rifaximin only on recurrence, transplant referral (MELD-Na 26) and no driving. Prohibitions: sedatives (PROHIB-BZD), opioids, rapid sodium correction and ammonia-guided treatment.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`.
- `accepted[0]` changed under ruling 3 (C10 scores, plan CENTRAL 6); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- Plan M01 says delete the EEG red herring with the lorazepam challenge. I deleted the challenge but kept the red herring, rewritten: the atypical triphasic-like waves remain in the EEG report and are a fair distractor; the correct interpretation now says the EEG itself excludes NCSE. Delete it if you prefer strict consistency with the plan.
- Plan M01 says DI optional. I made it recommended because metformin in decompensated Child-Pugh C cirrhosis is a concrete change of management; ruling 6 would even allow required.
- The exam orientation was changed (place now oriented) to keep grade II; the alternative is to relabel grade III, which would change the HE points (3, Child-Pugh still C, 13 points) and the case's difficulty.
- New laboratory values (magnesium 1.9, lactate 1.4, CRP 3.1, TSH 1.7, zinc 67) are invented within normal ranges as C9 instructs; they carry no diagnostic weight.

## Verification

Checked (adversarial verifier, 23 Oct 2026): all three note ids (dec0d57a, 22fa5945, 6a7d6fa7) are in the table and fixed in the file (no challenge, MRI, CSF or `interpret_labs` tap remains; one `ascitic_fluid` criterion expecting PMN 82; CT has findings and no "restricted diffusion"; no constraint left). Recomputed the scores from the printed values: Child-Pugh C 12 (bilirubin 3.8, albumin 2.4, INR 1.8, mild ascites, grade II), MELD 20, MELD-Na 26, as stated in the label, key evidence, expected evidence and MUST-TX. Grade II matches the edited exam (disoriented to time only, asterixis); the HPI no longer leaks toxicology; red-herring paths point at sodium and the triphasic-like finding; flags, summary and interpretation agree; SAAG 1.8 = 2.4 - 0.6; differential is updated to the results; no musts contradict prohibitions; no "2-4", "gated on" or haloperidol text. The worker's departures from the plan (DI recommended for metformin in Child-Pugh C; EEG red herring kept without the challenge) are sound.

Found: one missing management item. Ascitic total protein is 1.2 g/dL with Child-Pugh 12, bilirubin 3.8 mg/dL, sodium 128 and creatinine 1.2, which meets the EASL 2018 criteria for primary SBP prophylaxis (protein < 15 g/L with Child-Pugh >= 9 and bilirubin >= 3 mg/dL, or impaired renal function or hyponatraemia); no must addressed it.

Changed: `ground_truth.assessment.required_recommendations` gains, before the transplant referral, "Start primary prophylaxis of spontaneous bacterial peritonitis (norfloxacin 400 mg daily, or ciprofloxacin): ascitic total protein 1.2 g/dL with Child-Pugh 12, bilirubin 3.8 mg/dL and sodium 128 mEq/L (EASL 2018)." `perfect_agent.py` and `case_io.py check` clean.

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

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-2-order-ct-scan` rationale: "Optional: there is no focal deficit, seizure or head trauma and the precipitants are clear, so brain imaging is not routine; thrombocytopenia and INR 1.8 lower the threshold to exclude hemorrhage if the course is atypical." -> "There is no focal deficit, seizure or head trauma and the precipitants are clear, so brain imaging is not routine; thrombocytopenia and INR 1.8 lower the threshold to exclude hemorrhage if the course is atypical."

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia]; now [CBC, CMP, coagulation, ammonia, CRP] | [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP with the core bloods (infection is the precipitant to exclude) and the evidence reads it; CBC, CMP, coagulation and ammonia did not return the inflammatory panel.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Weight and height (25 Oct 2026)

- Past history lists "Obesity" but the stored BMI was 29.3. Rule 3: BMI 29.3 -> 31.5, weight 89.7 -> 96.5 kg, height 175 cm kept. No text cited the old BMI.
- Checks: `perfect_agent.py` pass; weight/height/BMI consistency check clean.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 17/30, below the normal range (26 or above), with impaired attention, executive function, delayed recall and orientation to time; naming preserved. (fallback_tool_outputs.clinical_assessment). Why: GCS 13, disoriented to time with slowed processing: a MoCA of 28/30 with full orientation is impossible.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3. Requires considerable assistance and frequent supervision; capable of only limited self-care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Timed tests could not be completed independently: unsteady, wide-based gait; walks only with one-person hand-held assistance; tandem gait not possible. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: unsteady, wide-based gait; walks only with one-person hand-held assistance.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Generalized theta-delta slowing with fronto-central predominance, background disorganization and absent posterior ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Generalized theta-delta slowing with fronto-central predominance, background disorganization and absent posterior dominant rhythm. 2. (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: reduction of myo-inositol (mI/Cr 0.28) and choline (Cho/Cr 0.58) with an increased glutamine-glutamate (Glx) peak; NAA preserved; no ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology with increased echogenicity. 2. No focal liver lesion. 3. Patent portal vein. 4. ... (fallback_tool_outputs.body_imaging). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology with steatosis. 2. No focal liver lesion. 3. ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology with steatosis. 2. No focal liver lesion. 3. Patent portal vein. 4. ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; normal white cell morphology; platelets reduced in number, of normal morphology, without ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 88, MCV 94: 'adequate platelets' contradicts it.
- `interpret_labs {panels: [HbA1c]}`: 6.9 (fallback_tool_outputs.labs[HbA1c]). Why: treated or known diabetes: HbA1c 6.9%.
- `order_specialized_test {test_type: neuropsych_battery}`: Abnormal neuropsychological profile dominated by slowed psychomotor speed and impaired attention and executive function, with a retrieval-type memory deficit ... (fallback_tool_outputs.specialized_test). Why: disoriented to time with slowed processing: a battery normal in every domain is impossible.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: normal articulation; slow, tangential replies with word-finding pauses; follows two-step commands slowly. (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: normal articulation; slow, tangential replies with word-finding pauses.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-M01` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
