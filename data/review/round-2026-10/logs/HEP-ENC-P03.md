# HEP-ENC-P03
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 4e8a2b60-4d78-4a9d-b8c3-8a603cdeb5d8 | FIXED | Grade II is overt (ACG 2026 key concept 1). `ground_truth.red_herrings[1].correct_interpretation` now reads "A mildly raised ammonia does not grade HE; the grade is clinical (West Haven grade II, overt)"; the covert pearl (`key_clinical_evidence[3]` old, "Even mild ammonia elevation ... can represent covert HE; a lactulose trial is informative") deleted and replaced by the covert/overt definition pearl (`key_clinical_evidence[5]`). The exam (disoriented to time, mild asterixis, GCS 13) supports grade II, so the label grade stays. |
| dac2b026-1842-4c69-9c92-623fbab39a1d | FIXED | Must "Empiric lactulose 30 mL TID + rifaximin 550 mg BID; response is diagnostic" replaced by MUST-LACT (`assessment.required_recommendations[0]`): titrate to 2-3 soft bowel movements per day, avoid over-titration (ACG 2026 rec. 10; EASL 2022). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `diagnosis.accepted[0]`, `past_medical_history[0]` | "Child-Pugh B, MELD 11" not derivable from the printed values; computed Child-Pugh B (9: bilirubin 1.9 1, albumin 2.7 3, INR 1.5 1, mild ascites 2, grade II 2), MELD 13, MELD-Na 13 (Na 138 bounded to 137) (C10). | FIXED: label "Child-Pugh B, MELD-Na 13"; the undated history score removed ("NASH cirrhosis, recently decompensated with ascites"); score line added to key evidence. |
| D | major | `patient.history_present_illness`, `neurological_exam.additional` | Timeline leaks: admission ammonia 64, "EEG shows non-specific slowing", "CT head negative for metastatic disease", "PSA elevated", "CT head shows no evidence of ... metastasis" (C13). | FIXED: removed; HPI now states the current lactulose/rifaximin prophylaxis and pertinent negatives (no fever, vomiting, melena, falls, new medicines). |
| B | minor | `neurological_exam.mental_status` | "Mild asterixis" followed by "No asterixis at home observation" (a wife cannot exclude asterixis; contradictory). | FIXED: second sentence removed. |
| C | major | `followup_outputs` (lactulose/rifaximin response, literature "goals of care", `interpret_labs` paracentesis) and `action-4-search-medical-literature` | Treatment response delivered as a lab result ("72h post-lactulose increase + rifaximin": GCS 15) (C1); required literature search standing in for a goals-of-care discussion (C4); paracentesis filed under `interpret_labs` with no criterion though ascites is present (C6). | FIXED: response and literature follow-ups and the literature criterion deleted; new required `action-diagnostic-paracentesis` (`order_microbiology` `ascitic_fluid`) with the tap moved to a microbiology follow-up (PMN 58, total WBC 190, protein 1.6 g/dL, ascitic albumin 1.2 g/dL, SAAG 1.5 g/dL as before, Gram stain, culture no growth at 48 hours). Goals of care is now a must. |
| B | major | `initial_tool_outputs.mri`, `followup_outputs[0]` (old) | The required `analyze_brain_mri` returned a normal non-contrast template with the scoring line "the finding the lumbar puncture is gated on", while the gadolinium study sat under `order_advanced_imaging` (C8). | FIXED: one MRI report in `initial_tool_outputs.mri` (without and with gadolinium): no parenchymal, leptomeningeal or calvarial metastasis, no restricted diffusion or vasogenic edema, symmetric pallidal T1 hyperintensity, mild cortical volume loss; structured findings filled; advanced-imaging follow-up deleted. Criterion now requires `{"contrast": true}`: the indication is metastatic and leptomeningeal disease, which a non-contrast MRI cannot exclude. |
| C | minor | `action-3-analyze-brain-mri` rationale, differential | PRES is a labelled adverse effect of enzalutamide and was not considered. | FIXED: MRI rationale and the enzalutamide differential entry name PRES; MRI reports no vasogenic edema. |
| B | minor | `initial_tool_outputs.ct` | Empty findings; "restricted diffusion" on CT (C8). | FIXED: canonical normal CT plus mild cortical volume loss (agrees with the MRI). |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" block with magnesium and lactate as "Within reference range"; template TSH 2.1 and zinc 82; no CRP; no calcium although the differential says "Check Ca"; summary omitted four flagged values (C9). | FIXED: magnesium 1.9 mg/dL, calcium 8.6 mg/dL (BMP), lactate 1.3 mmol/L, CRP 3.2 mg/L, TSH 1.6, zinc 64; `abnormal_values_summary` and `interpretation` list every flagged value. |
| A | minor | `action-1-interpret-labs` | 9 named panels demanded. | FIXED: two-alternative core (C9). |
| C | major | `action-8`, `action-9-order-microbiology`, cultures | Blood and urine cultures required "before the first antimicrobial dose" in an afebrile patient with WBC 6.4 and no antibiotic (C7); every block "No organism isolated to date. Specimen taken before the first antimicrobial dose". | FIXED: both recommended as an occult-infection screen, specimen-only arguments; blood block "no growth at 48 hours", urine follow-up with microscopy (no pyuria) and culture; `collected_before_antimicrobials` null (no systemic antibiotic in the case). |
| C | major | `action-5-check-drug-interactions`, `followup_outputs` (DI) | Required with template expected evidence; output claimed apalutamide is "less CNS penetrant" (it is darolutamide that has low blood-brain barrier penetration) and used the check to announce "HE is the confirmed diagnosis" (style guide). | FIXED: recommended (plan), alternatives name enzalutamide, lactulose, rifaximin, leuprolide; new output `check_enzalutamide_lactulose_rifaximin` placed last: enzalutamide CYP3A4/2C9/2C19 induction, seizure and CNS adverse effects, no hepatic starting-dose adjustment, no interaction with lactulose or rifaximin, diuretic monitoring during lactulose titration, penicillin anaphylaxis. |
| C | major | `assessment` | Must "response is diagnostic"; must restating the MRI (a scored study, not management); generic and duplicated LP prohibitions (no LP in the case); boilerplate benzodiazepine line recommending haloperidol; no plan for the penicillin anaphylaxis; no goals-of-care must. | FIXED: musts MUST-LACT; precipitant search with lactulose adherence and continued rifaximin; oncology review at 4-8 weeks with reconsideration of enzalutamide (ACG 2026 key concept 8) and counselling; goals of care (transplant generally precluded by active extrahepatic malignancy). Prohibitions PROHIB-BZD; sedating opioids with acetaminophen up to 2 g per day; no beta-lactam without allergy advice. Both LP prohibitions deleted. |
| C | minor | `ground_truth.differential` | Leptomeningeal entry and Alzheimer entry phrased as pre-work-up ("required to exclude", "lactulose response distinguishes"); hypercalcemia "Check Ca" with no calcium in the case (ruling 7). | FIXED: entries rewritten with the excluding results (contrast MRI; calcium 8.6, about 9.6 corrected); enzalutamide toxicity stays moderate as a possible contributor. |
| C | minor | `key_clinical_evidence[4]` | Pearl named abiraterone and BTK inhibitors as BBB-crossing agents causing neuropsychiatric symptoms; the class effect belongs to the androgen-receptor inhibitors (enzalutamide, apalutamide). | FIXED: pearl restricted to enzalutamide and apalutamide. |
| E | minor | criteria, citations, pearls, metadata | Rationale repeated the label; free-text citations; "AASLD 2014" pearl; metadata named the lactulose response and the literature search as decisive. | FIXED: one-sentence rationales with keys, K-AMM pearl, difficulty fields updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now requires the core labs, a diagnostic paracentesis (ascitic PMN 58 cells/mm3, no SBP) and a contrast MRI, and recommends blood and urine cultures as an occult-infection screen, the EEG and a drug check; CT is optional. The contrast MRI (no metastasis, no leptomeningeal enhancement, no PRES, pallidal T1 hyperintensity) is now the one MRI report, so the normal template with the lumbar-puncture scoring line is gone. The lactulose/rifaximin "response" panel, the literature searches and the duplicate `interpret_labs` tap are deleted. The HPI and exam no longer give the ammonia, EEG or CT results. The label reads Child-Pugh B (9 points), MELD-Na 13 (stated MELD 11); the West Haven grade II is overt throughout (the covert red herring and pearl are corrected). Labs gain magnesium, calcium, lactate and CRP and lose the "Exclusion studies" block and the template TSH and zinc values. The drug check reports enzalutamide's enzyme induction and CNS effects, the absence of interaction with lactulose and rifaximin, and the penicillin anaphylaxis (it no longer claims apalutamide is less CNS-penetrant). Musts: lactulose titrated to 2-3 soft stools, precipitant search with adherence check and continued rifaximin, oncology review of enzalutamide at 4-8 weeks if cognition does not recover, goals of care. Prohibitions: sedatives, sedating opioids, beta-lactams without allergy advice; the LP prohibitions are removed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`.
- `accepted[0]` changed under ruling 3 (C10 scores); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- The MRI criterion requires `{"contrast": true}` rather than the plan's `{}`: the only reason this patient needs an MRI is metastatic and leptomeningeal disease, which needs gadolinium. A non-contrast MRI order would still receive the stored contrast report (the harness has one MRI output), so the requirement only affects scoring.
- No precipitant is identified in this case (no infection, bleeding, electrolyte change or sedative); the must asks for an adherence and stool-frequency check on the prophylactic lactulose dose. A reviewer may want the case to state a precipitant explicitly.
- `fallback_tool_outputs.mri` still holds a normal template MRI; it is never served because `initial_tool_outputs.mri` exists, so I left it.

## Verification

Adversarial check, 23 Oct 2026. Read the log, the diff and the whole final case. Recomputed the scores from the printed labs: Child-Pugh B 9 (bilirubin 1.9 1, albumin 2.7 3, INR 1.5 1, mild ascites 2, grade II 2), MELD 13, MELD-Na 13 (Na 138 bounded to 137); the label, key evidence, lab expected evidence and goals-of-care must agree. Both notes are fixed everywhere they apply: no "covert" left except the covert/overt definition pearl, MUST-LACT carries the 2-3 target, and the medication list still shows lactulose 20 mL twice daily and rifaximin, which the precipitant must uses. The HPI and exam no longer give the ammonia, EEG, CT or PSA. Checked the drug-check facts against the enzalutamide label (strong CYP3A4, moderate CYP2C9/2C19 inducer; seizures about 0.5%; PRES labelled; no starting-dose change for Child-Pugh A to C) and darolutamide's lower brain penetration: correct. The penicillin anaphylaxis is handled in a prohibition, and no must gives a beta-lactam. Criterion and follow-up order follow plan 3.1; ammonia range 11-51; red-herring paths point at the right entries (`LFTs[5]` is the ammonia). The `{"contrast": true}` MRI requirement is a justified deviation from the plan (logged under open questions). Found nothing to change. `perfect_agent.py` and `case_io.py check` clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- `fallback_tool_outputs.mri` set to null: an unreachable normal template ("ventricles and sulci appropriate for age") contradicting the case's own MRI (diffuse cortical volume loss); `initial_tool_outputs.mri` always answers the order.

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type 'neuropsychological_screening', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-2-order-ct-scan` rationale: "Optional: there is no focal deficit, seizure or head trauma, and non-contrast CT cannot exclude the leptomeningeal disease that the cancer history raises; the contrast MRI answers the structural question." -> "There is no focal deficit, seizure or head trauma, and non-contrast CT cannot exclude the leptomeningeal disease that the cancer history raises; the contrast MRI answers the structural question."

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia]; now [CBC, CMP, coagulation, ammonia, CRP] | [CBC, CMP, coagulation, ammonia] | [CBC, BMP, LFTs, coagulation, ammonia].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP with the core bloods (infection is the precipitant to exclude) and the evidence reads it; CBC, CMP, coagulation and ammonia did not return the inflammatory panel.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 18/30, below the normal range (26 or above), with impaired attention, executive function, delayed recall and orientation to time; naming preserved. (fallback_tool_outputs.clinical_assessment). Why: GCS 13, disoriented to time with slowed processing: a MoCA of 28/30 with full orientation is impossible.
- `order_specialized_test {test_type: neuropsych_battery}`: Abnormal neuropsychological profile dominated by slowed psychomotor speed and impaired attention and executive function, with a retrieval-type memory deficit ... (fallback_tool_outputs.specialized_test). Why: disoriented to time with slowed processing: a battery normal in every domain is impossible.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3. Requires considerable assistance and frequent supervision; capable of only limited self-care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Slowed gait with impaired dynamic balance: Timed Up and Go 14.9 s (above the 13.5 s fall-risk threshold) and 10 m walk speed 0.93 m/s; tandem gait not achieved. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: slightly unsteady.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: normal articulation; reduced spontaneous output with slow, brief answers; follows two-step commands. (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: normal articulation; reduced spontaneous output with slow, brief answers.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Diffuse theta slowing at 6–7 Hz with loss of the posterior dominant rhythm and mild disorganization of background ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Diffuse theta slowing at 6–7 Hz with loss of the posterior dominant rhythm and mild disorganization of background rhythms. No ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: reduction of myo-inositol (mI/Cr 0.28) and choline (Cho/Cr 0.58) with an increased glutamine-glutamate (Glx) peak; NAA preserved; no ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology with increased echogenicity. 2. No focal liver lesion. 3. Patent portal vein. 4. ... (fallback_tool_outputs.body_imaging). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology with steatosis. 2. No focal liver lesion. 3. ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology with steatosis. 2. No focal liver lesion. 3. Patent portal vein. 4. ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; normal white cell morphology; platelets reduced in number, of normal morphology, without ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 118: 'adequate platelets' contradicts it.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-P03` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
