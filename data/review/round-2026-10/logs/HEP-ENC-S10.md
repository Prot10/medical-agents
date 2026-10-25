# HEP-ENC-S10
Reviewer status: R1 not reviewed, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | | This case has no reviewer notes; all changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status` | GCS 11 with M4 (withdrawal) in a patient who converses, knows she is in hospital and is graded West Haven II. | FIXED: GCS 13 (E3V4M6), drowsy, follows simple commands slowly. |
| B | minor | `past_medical_history`, `medications` | "Morbid obesity (BMI 31)"; "Child-Pugh B, MELD 14" undated beside the admission values; furosemide listed at 40 mg although the HPI says she raised it to 80 mg three days ago. | FIXED: "Obesity (BMI 31, down from a peak of 38 ...)"; prior score dated to her last clinic review; furosemide 80 mg with the change noted in the indication. |
| B | minor | `history_present_illness`, `social_history.alcohol` | HPI "no history of ... alcohol use" against 1-2 drinks a month. | FIXED: "drinks alcohol only rarely". |
| C | major | `ground_truth.diagnosis.accepted[0]` | Scores from the clinic visit, not from the admission values (C10). | FIXED: Child-Pugh C (13: bilirubin 3.2 3, albumin 2.7 3, INR 1.7 2, moderate ascites 3, HE grade II 2), MELD 19, MELD-Na 21 (Na 134); derivation in `key_clinical_evidence[0]`. |
| C | major | `followup_outputs` (`request_lactulose_rifaximin`, `request_continuous_eeg`, `request_mri_brain`) | Treatment response through tools (ammonia trend, 36-hour EEG) and an MRI follow-up with no criterion (C1, C2, C8). | FIXED: deleted. |
| D | major | `initial_tool_outputs.literature_search`, `action-3-search-medical-literature` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, output null. |
| C | major | `followup_outputs` (`request_check_metformin_safety`, `request_diuretic_adjustment`), `action-4` | Two DI blocks: one "continue metformin" proposal, one with a tolvaptan suggestion and a patient-specific conclusion; initial DI template (C5). | FIXED: initial null; one follow-up `check_furosemide_spironolactone_metformin_lisinopril`, placed last: loop escalation and hypokalemia, hold diuretics then restart at 100:40, hold metformin, lisinopril not recommended with ascites, lower-dose atorvastatin. Required. |
| A | major | `followup_outputs` (`request_sbp_paracentesis`) | Paracentesis served through `interpret_labs` with no criterion (C6). | FIXED: `order_microbiology` `ascitic_fluid` follow-up (`request_diagnostic_paracentesis`): WBC 210, PMN 95 cells/mm3, protein 1.7 g/dL, ascitic albumin 1.0 g/dL (SAAG 1.7), Gram stain negative, no growth at 48 hours; new required criterion `action-diagnostic-paracentesis`. |
| B | minor | `initial_tool_outputs.microbiology`, `action-7`, `action-8` | Template culture text, `collected_before_antimicrobials` true with no antibiotic in the case, test lists in the arguments; cultures required in an afebrile patient with WBC 8.4 (C7). | FIXED: one time point (no growth at 48 hours), flag null, specimen-only arguments; both cultures recommended with the canonical label and rationale; urine block adds microscopy without pyuria. |
| B | major | `initial_tool_outputs.labs` | Ammonia range 11-35 in "umol/L" (C2); magnesium "Within reference range" under "Exclusion studies"; "Metformin Safety" panel; template TSH 2.1 and zinc 82; no CRP (C9). | FIXED: 11-51 µmol/L; magnesium 1.6 mg/dL (low) in the CMP; panel "Lactate and CRP" with CRP 3 mg/L; TSH 1.9, zinc 64; summaries rebuilt. |
| A | minor | `action-1-interpret-labs` | Many named panels demanded (C9). | FIXED: two-alternative core; canonical label and rationale. |
| E | minor | `initial_tool_outputs.eeg` | "uV"; impression without a closing statement. | FIXED: µV; "Moderate diffuse encephalopathy, consistent with a toxic-metabolic cause. Clinical correlation recommended." |
| C | major | `ground_truth.assessment.required_recommendations` | Lactulose "30 mL TID to 2-4 stools" (C3); no plan for metformin, lisinopril, statin, magnesium, the diuretic restart or transplant. | FIXED: 8 musts: precipitants, MUST-K with magnesium and diuretic hold, restart at 100:40 or large-volume paracentesis, MUST-LACT, rifaximin, stop metformin and lisinopril and lower atorvastatin, education, transplant referral (MELD-Na 21). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Benzodiazepine line advised haloperidol; generic LP line; acetaminophen dose unstated (C12). | FIXED: PROHIB-BZD; opioid line with acetaminophen up to 2 g per day; LP line deleted; no loop escalation while potassium is low. |
| C | minor | `ground_truth.differential` | Key features were instructions ("Check glucose", "TSH if ...") rather than the deciding finding (C14). | FIXED: each entry names the excluding result (glucose 188, PMN 95, no focal deficit, TSH 1.9). |
| E | minor | criteria, pearls, metadata, exam | Rationale = label; "(AASLD 2014)" pearls; em dashes; no ammonia pearl; metadata described the old policy. | FIXED: canonical labels and keyed rationales; score pearl, clinical diagnosis, K-AMM, precipitants, ammoniagenesis, adherence; metadata difficulty fields updated; no em dashes remain. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy requires the core laboratory work-up, the diagnostic paracentesis (PMN 95 cells/mm3, no SBP) and one medication review; blood and urine cultures and EEG are recommended and CT optional. The literature search, the ammonia trend, the 36-hour EEG, the MRI and the two separate drug checks are gone. The exam now gives GCS 13 (E3V4M6), which fits grade II; the medication list shows the furosemide increase to 80 mg that the HPI describes. The label reads West Haven grade II, Child-Pugh C (13), MELD-Na 21, from the admission values; "Child-Pugh B, MELD 14" is dated to her last clinic review. Labs use the 11-51 µmol/L ammonia range, give magnesium 1.6 mg/dL and CRP 3 mg/L, and replace the template TSH and zinc. The single drug check covers the loop escalation, metformin, lisinopril with ascites and atorvastatin. Musts: precipitants, potassium and magnesium with the diuretics held, a 100:40 restart or large-volume paracentesis later, lactulose to 2-3 stools, rifaximin, stop metformin and lisinopril, lower atorvastatin, adherence education, transplant referral. Prohibitions: sedatives, opioids, loop escalation while potassium is low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`.
- `accepted[0]` changed under ruling 3 (C10 scores); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- The DI check is required (plan) and also carries new content beyond the precipitant (lisinopril with ascites, atorvastatin dose); trim it to the diuretics and metformin if that widens the case too much.
- Child-Pugh C 13 counts the ascites as moderate (shifting dullness with increasing distension); counted as mild it is 12, still class C.
- New values carry no diagnostic weight: magnesium 1.6, CRP 3, TSH 1.9, zinc 64, ascitic WBC 210, PMN 95, protein 1.7 and albumin 1.0 g/dL.
- GCS changed from 11 to 13 so that the exam matches grade II; if the author meant a deeper patient, the grade would be III instead.

## Verification
Adversarial check (23 Oct 2026) of the final case against the log and the plan (no notes for this case).
- Checked: MELD 19, MELD-Na 21 (Cr 1.3, bilirubin 3.2, INR 1.7, Na 134) and Child-Pugh C 13 recomputed; GCS 13 (E3V4M6) and orientation to place fit grade II; furosemide 80 mg consistent between HPI and medication list; dated pre-encounter labs legitimate; SAAG 1.7 = 2.7 - 1.0; ammonia range 11-51; DI merged into one required check whose content matches the musts; stop rule = the three required ids; no em dashes or template residues.
- Found and changed:
  - C, major, `ground_truth.differential`, `assessment.required_recommendations`: the history (bariatric surgery 3 years ago, a week of nausea with poor intake) raises thiamine deficiency, a mimic neither listed nor addressed (ruling 7). Added "Wernicke encephalopathy" (low; intact extraocular movements, confusion explained by the precipitants; not excluded clinically) and a must: parenteral thiamine before any dextrose, escalating to 200 mg IV three times daily if ophthalmoplegia, nystagmus or ataxia appears (EFNS 2010).
  - B, minor, `fallback_tool_outputs.ecg`: a normal ECG at 60/min contradicted HR 96 and potassium 2.9 (an ECG is the natural safety check for this precipitant). Now sinus rhythm 96/min, flattened T waves with U waves, QTc 462 ms; `metadata.fallback_tool_kinds.ecg` "abnormal_nonspecific".
- perfect_agent -v and case_io check clean after the edit.

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

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: Cognitive screening could not be completed: the patient could not sustain attention or follow the test instructions. No valid score was obtained. (fallback_tool_outputs.clinical_assessment). Why: drowsy, disoriented to date and year, following simple commands slowly, unable to perform a number connection test: no MoCA can be completed.
- `order_specialized_test {test_type: neuropsych_battery}`: Formal neuropsychological testing could not be administered at this level of arousal and attention. No domain scores were obtained. (fallback_tool_outputs.specialized_test). Why: drowsy, disoriented to date and year, following simple commands slowly, unable to perform a number connection test: a battery cannot be administered.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 30, ECOG 4. Severely disabled, completely bed-bound and dependent for all care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Timed gait and balance testing was not possible: too confused to stand safely. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: too confused to stand safely.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: slow, dysarthric speech; slow, simplified output; mixes up names; follows simple commands slowly. (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: slow, dysarthric speech; slow, simplified output; mixes up names.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Generalized theta-delta slowing at 3-5 Hz with a slowed and diminished posterior dominant rhythm. 2. Bifrontally ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Generalized theta-delta slowing at 3-5 Hz with a slowed and diminished posterior dominant rhythm. 2. Bifrontally predominant ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: marked reduction of myo-inositol (mI/Cr 0.16) and choline (Cho/Cr 0.50) with an increased glutamine-glutamate (Glx) peak; NAA ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology with increased echogenicity. 2. No focal liver lesion. 3. Patent portal vein. 4. ... (fallback_tool_outputs.body_imaging). Why: cirrhosis with moderate-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology with steatosis. 2. No focal liver lesion. 3. ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with moderate-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology with steatosis. 2. No focal liver lesion. 3. Patent portal vein. 4. ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with moderate-volume ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; normal white cell morphology; platelets reduced in number, of normal morphology, without ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 94: 'adequate platelets' contradicts it.
- `interpret_labs {panels: [HbA1c]}`: 8.4 (fallback_tool_outputs.labs[HbA1c]). Why: treated or known diabetes: HbA1c 8.4%.
- `analyze_brain_mri`: 1. Subtle symmetric T1 hyperintensity in the globi pallidi without T2 signal change. 2. No diffusion abnormality, haemorrhage or mass. 3. No cerebral oedema. 4. (fallback_tool_outputs.mri). Why: only stored imaging is a CT with mild generalized atrophy: a normal MRI contradicts it.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-S10` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
