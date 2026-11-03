# HEP-ENC-S02
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b8268eb9-d737-4a3f-9e74-d9a55e1e9584 | FIXED | `ground_truth.red_herrings[0]` rewritten around the case's own numbers (plan C14): data point "Fever 38.2 °C with leukocytosis (WBC 13.6) after a respiratory illness two weeks earlier"; trap: attribute it to a viral infection and skip the tap; correct interpretation: SBP must still be excluded by paracentesis (PMN 124 excludes it), then chest radiograph and stool testing. The HPI's "low-grade fever" is now "a fever". |
| 3559f393-0f92-41bc-8de4-6b194897fcf3 | DECLINED in part (by design, ruling 4; plan C16) / FIXED in part (C1) | Treatment is scored through the musts, never a tool call. FIXED: the "48h, rifaximin restarted + lactulose optimized + KCl repleted" ammonia panel (`request_lactulose_rifaximin`) and the rifaximin-insurance "drug check" (`check_rifaximin_insurance_adherence`) are deleted; the content is now musts: restart rifaximin with a supply plan (`required_recommendations[0]`), lactulose reduction (`[1]`), potassium and magnesium (`[2]`), fever work-up with empirical antibiotics (`[3]`). The old "optimal action 7" (hepatology input / case management) no longer exists as a criterion. |
| a6ec2282-8ada-4f5c-ae0b-d64877fed336 | FIXED | "Lactulose 30-45 mL QID titrated to 2-4 stools/day" replaced by MUST-LACT-OVERUSE: reduce lactulose to 2-3 soft stools per day (currently 4-5 loose stools with potassium 3.2), correct potassium and volume, investigate the diarrhea including C. difficile toxin; new prohibition "Do not escalate lactulose while he already has 4-5 loose stools per day with hypokalemia". |
| 632aabc9-6d1c-409d-9713-25e61382f9af | FIXED | Recomputed from bilirubin 7.8, INR 2.4, creatinine 1.3, sodium 130: MELD 27, MELD-Na 30; Child-Pugh C, 15 points (moderate ascites 3, HE grade III 3). `accepted[0]` "Child-Pugh C, MELD-Na 30"; the MELD 18 in history and HPI dated "at his last clinic review"; the MELD-Na 21 panel deleted; score pearl added. ICD unchanged. |
| dd9192d8-7d9c-4451-b055-51a1d734dc19 | FIXED (as musts; vocabulary under CENTRAL) | `required_recommendations[3]`: chest radiograph (respiratory illness two weeks earlier) and empirical antibiotic cover after cultures, narrowed by the results; `[1]`: stool testing for C. difficile toxin. Differential entry "Other infection" now names pneumonia and C. difficile colitis as not yet excluded. No tool exists for a chest radiograph or a stool specimen: CENTRAL 5. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` (`request_thiamine_empiric`, `request_liver_transplant_evaluation`) | Treatment ("IV thiamine administered") and a MELD panel through `interpret_labs` (C1). | FIXED: deleted; thiamine and transplant referral are musts. |
| D | major | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, initial output null. |
| A | major | `action-5-interpret-labs` | Duplicate paracentesis criterion via `interpret_labs` `{}` (answered by the core labs) (C6). | FIXED: deleted. `action-9-order-microbiology` (`ascitic_fluid`, required) has the canonical label and "Ascitic PMN 124 cells/mm3, below the 250 cells/mm3 threshold for SBP". |
| B | minor | ascitic follow-up (trigger renamed `request_diagnostic_paracentesis`), blood and urine blocks | PMN and SAAG without units; "no growth at 5 days" beside "no organism isolated to date"; template text (C7). | FIXED: units, protein 1.0, albumin 0.4 (SAAG 1.8), Gram stain, one time point (48 h) in every block; urine microscopy added. |
| A | minor | `action-8`, `action-9`, `action-10-order-microbiology` | `before_antimicrobials`/`tests` arguments; label-copy rationales (C7, C17). | FIXED: specimen-only arguments; required labels (T 38.2, WBC 13.6); case expected evidence; culture timing must. |
| D | major | `patient.history_present_illness` | Ammonia 142, "EEG shows classic triphasic waves", "CT head is normal" in the HPI (C13). | FIXED: removed. |
| B | minor | `initial_tool_outputs.labs` | "Exclusion studies" block; template TSH 2.1 and zinc 82; no CRP; "Rifaximin non-adherence" listed as a lab value (C9). | FIXED: magnesium 1.5 mg/dL (L, diarrhea), lactate 1.8, CRP 52 mg/L, TSH 3.1, zinc 66; summary and interpretation list only flagged values. |
| A | minor | `action-1-interpret-labs` | Criterion demanded 9 panels (C9). | FIXED: two core alternatives; canonical label; case expected evidence. |
| C | major | `ground_truth.assessment.required_recommendations` | Conditional SBP must ("if PMN ≥250") although PMN is 124; no thiamine (prior heavy drinker) or transplant referral once the panels were deleted; nothing on the unexplained fever. | FIXED: musts as listed under the notes, plus MUST-THIA and MUST-TX (MELD-Na 30). |
| C | minor | `prohibited_recommendations` | Haloperidol advice; generic LP prohibition with no LP; acetaminophen dose unstated (C12). | FIXED: PROHIB-BZD; LP line deleted; acetaminophen up to 2 g per day; lactulose-escalation prohibition. |
| C | major | `action-4-check-drug-interactions`, DI follow-up | DI was required, with no concrete interaction, and its only output was the rifaximin-insurance note (C1, C5). | FIXED: DI optional (no concrete interaction); real follow-up `check_rifaximin_lactulose_propranolol_insulin` (propranolol thresholds, spironolactone hold, insulin dose reduction, no sedatives), placed last. |
| C | minor | `ground_truth.differential` | SBP moderate after PMN 124 (C14); other infection without the sources the case raises. | FIXED: SBP low; other infection names pneumonia and C. difficile; SDH key features no longer assume a CT was done. |
| C | minor | `key_clinical_evidence[3]` | "Rifaximin secondary prophylaxis is a 1A indication after a first overt HE episode": rifaximin is added after a recurrence; lactulose is first-line after a first episode. | FIXED; score pearl and K-AMM added. |
| B | minor | `initial_tool_outputs.ct` | Empty findings (C8). | FIXED: canonical normal findings; CT optional with ACG rationale. |
| B | minor | `fallback_tool_outputs.ecg` | Normal sinus rhythm 61 bpm in a patient with HR 110. | FIXED: sinus tachycardia 108. |
| B | major | `metadata.difficulty_description` | Described another case ("NASH cirrhosis with constipation and dietary protein excess"). | FIXED: describes this case; difficulty rationale updated. |
| E | minor | `accepted[0]` | "low-grade fever requires SBP exclusion"; em dash. | FIXED: "fever with leukocytosis requires exclusion of SBP and other infection". |

## Changes, in one paragraph a physician can read before re-reviewing

The label now reads West Haven grade III, Child-Pugh C (15), MELD-Na 30 (bilirubin 7.8, INR 2.4, creatinine 1.3, sodium 130), precipitated by a 10-day rifaximin gap and diarrhea-associated hypokalemia, with fever and leukocytosis requiring infection to be excluded. The HPI no longer gives the ammonia, EEG or CT results. Required: core labs, blood and urine cultures and a diagnostic paracentesis (PMN 124, no SBP, sterile); EEG recommended; CT and medication review optional. The ammonia-response, thiamine, MELD and rifaximin-insurance outputs, the literature search and the duplicate labs-paracentesis criterion are gone. Labs add magnesium 1.5, lactate 1.8 and CRP 52. Musts: restart rifaximin with a secured supply; reduce lactulose to 2-3 soft stools and investigate the diarrhea including C. difficile toxin; potassium to 4.0 or more with magnesium and spironolactone held; chest radiograph and empirical antibiotics after cultures for the unexplained fever; cultures before antibiotics; thiamine before glucose; transplant referral. Prohibitions: sedatives, opioids, escalating lactulose. The red herring now matches the recorded 38.2 °C and WBC 13.6, and SBP is low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 5: `chest_xray` in `order_body_imaging` and a `stool` specimen (C. difficile toxin/PCR) in `order_microbiology`, so that note dd9192d8 can become scored actions; until then they are musts.
- New citation keys per plan 1.1.
- `accepted[0]` changed under ruling 3 (C10); ICD and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- "Stool testing for C. difficile after recent antibiotics" (plan text) was written as "(cirrhosis and recent rifaximin)": the case does not say that the respiratory illness was treated with antibiotics.
- The fever must starts empirical antibiotic cover after cultures (fever, WBC 13.6, HR 110 in decompensated cirrhosis); if you prefer to withhold antibiotics until the chest radiograph, the must should say so.
- New values (magnesium 1.5, lactate 1.8, CRP 52, TSH 3.1, zinc 66, ascitic WBC 290, protein 1.0, albumin 0.4) are invented to fit the case.

## Verification

Adversarial verification, 23 Oct 2026.

- Notes: all five ids in the table with sound rulings. b8268eb9: red herring now uses 38.2 °C and WBC 13.6 (matches vitals and labs). a6ec2282: MUST-LACT-OVERUSE plus a prohibition on escalation; no "2-4" left. 632aabc9: MELD 26.5 -> 27, MELD-Na 30.0 -> 30 (Cr 1.3, bilirubin 7.8, INR 2.4, Na 130); Child-Pugh 15 C (albumin 2.2, moderate ascites, grade III supported by GCS 12, oriented to name only). dd9192d8: chest radiograph and C. difficile testing are musts pending CENTRAL 5. 3559f393: partly declined by design (ruling 4), the panels are deleted.
- Cross-field: ascitic PMN 124 with SAAG 1.8 (2.2 - 0.4), blood and urine sterile, SBP low, "other infection" moderate with the two unexcluded sources named; ethanol not detected with 3 months sober; DI optional and real; HPI free of ammonia, EEG and CT results.
- Changes made: none. `perfect_agent.py HEP-ENC-S02 -v` passes; `case_io.py check` clean for the case.

## Auditor (24 Oct 2026)

- `key_clinical_evidence[0]`: the template pearl "HE is a clinical diagnosis: West Haven grading + evidence of liver dysfunction + exclusion of other causes of AMS ... (AASLD 2014)" survived here (S02-S05 only) and is replaced by the M01 canonical text "HE is a clinical diagnosis: West Haven grade, evidence of liver disease and exclusion of other causes of altered mental status (ACG 2026; EASL 2022)." The ammonia half of the old sentence is already carried by the K-AMM pearl. Removes a superseded citation and an em dash.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Central vocabulary wired (24 Oct 2026)

`chest_xray` and the `stool` specimen are now core terms, so note dd9192d8 (previously FIXED as musts) becomes scored actions.
- New criteria after the urine culture, both recommended, `[EASL_HE_2022]`: `action-chest-xray` `{"study": "chest_xray"}` (respiratory illness two weeks earlier; expected "No consolidation or effusion") and `action-stool-c-difficile` `{"specimen": "stool"}` (five days of diarrhoea with fever; expected both assays negative).
- New `followup_outputs[2]` `request_chest_xray` (no consolidation or effusion, mildly elevated hemidiaphragms from ascites) and `[3]` `request_stool_c_difficile` (negative), before the drug check.
- `assessment.required_recommendations[1]`: the C. difficile clause removed (now an action); the must is the MUST-LACT-OVERUSE text. `[3]`: "no source on paracentesis (PMN 124), urinalysis, chest radiograph and stool C. difficile testing: start empirical antibiotic cover after cultures, and narrow or stop it according to the cultures at 48 hours (EASL 2018)".
- `differential[1]` (other infection) moderate -> low, key features now give the negative radiograph and stool test; `red_herrings[0].correct_interpretation` names "stool C. difficile testing". Both results were chosen negative because the label rests on the rifaximin gap and diarrhoea-associated hypokalaemia.
- Re-run: `perfect_agent.py HEP-ENC-S02 -v` ok; `case_io.py check` schema OK, synonym guard OK, no test failure names the case.

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

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia]; now [CBC, CMP, coagulation, ammonia, CRP] | [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP and the work-up searches for an infective precipitant (EASL 2022 / ACG 2026); CRP was not in the order, so the CRP the evidence reads was not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: Cognitive screening could not be completed: the patient could not sustain attention or follow the test instructions. No valid score was obtained. (fallback_tool_outputs.clinical_assessment). Why: oriented to name only, agitated, unable to perform any cognitive testing: no MoCA can be completed.
- `order_specialized_test {test_type: neuropsych_battery}`: Formal neuropsychological testing could not be administered at this level of arousal and attention. No domain scores were obtained. (fallback_tool_outputs.specialized_test). Why: oriented to name only, agitated, unable to perform any cognitive testing: a battery cannot be administered.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 30, ECOG 4. Severely disabled, completely bed-bound and dependent for all care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Timed gait and balance testing was not possible: unable to stand safely. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: unable to stand safely.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: slurred speech; confused, fragmentary output; follows single commands inconsistently. (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: slurred speech; confused, fragmentary output.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Continuous generalized fronto-predominant triphasic waves at 1.5-2.5 Hz with anterior-to-posterior phase lag and ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Continuous generalized fronto-predominant triphasic waves at 1.5-2.5 Hz with anterior-to-posterior phase lag and positive phase-2 ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: marked reduction of myo-inositol (mI/Cr 0.16) and choline (Cho/Cr 0.50) with an increased glutamine-glutamate (Glx) peak; NAA ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein; recanalized paraumbilical vein. 4. (fallback_tool_outputs.body_imaging). Why: cirrhosis with moderate-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with moderate-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein; gastro-oesophageal varices ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with moderate-volume ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; mild neutrophilia; normal white cell morphology; platelets reduced in number, of normal ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 78, WBC 13.6: 'adequate platelets' contradicts it.
- `interpret_labs {panels: [HbA1c]}`: 7.0 (fallback_tool_outputs.labs[HbA1c]). Why: treated or known diabetes: HbA1c 7.0%.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-S02` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
