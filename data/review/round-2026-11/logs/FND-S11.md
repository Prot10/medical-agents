# FND-S11

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress, no R2 note | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 48159203-521c-4e99-8cee-9685ac8d68b4 | FIXED | Class LIT, commit 393c547e; checked: no literature criterion or output left (whole case) |
| b7bfdbac-1e1d-49b5-8616-109c078f70cd | FIXED | Class VEEG: ground_truth.action_criteria[action-4-analyze-eeg] optional -> required, canonical required rationale (October sentence deleted); ground_truth.stop_rule.required_before_assessment += action-4-analyze-eeg; required_recommendations[0] (M-DX) names the recorded episode |
| e3a99195-0f15-4413-a203-8233013eff7b | FIXED | Class DX: ground_truth.diagnosis.accepted[0] -> "Functional neurological disorder — recurrent PNES and functional bilateral hand weakness, with comorbid depression" (synonyms untouched); ground_truth.assessment.required_recommendations[3] (M-PSY) "treat the comorbid depression."; neuropsychology output and rationale keep "high somatic symptom burden" (a score). CENTRAL C2 (label change) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.action_criteria[action-ecg]; ground_truth.stop_rule; initial_tool_outputs.ecg; fallback_tool_outputs.ecg; metadata.fallback_tool_kinds | Plan class ECG (note f4d98130 on M01): the events include apparent loss of responsiveness, for which NICE CG109 1.1.2.2 advises a 12-lead ECG for everyone; the criterion was optional and answered only by the shared template fallback "Normal ECG". | FIXED: required, in the stop rule, citation [NICE_CG109] only (NG217 dropped), canonical rationale; case-specific stored ECG (sinus 82/min matching the vitals, normal PR and QRS, QTc 426 ms); template fallback nulled and its fallback_tool_kinds key removed |
| A | minor | ground_truth.action_criteria order; followup_outputs order | Plan 2.ORDER. | FIXED: exam, ECG, video-EEG, drug check, neuropsychology; neuropsychology answer before the on-request performance status |
| E | minor | metadata.difficulty_rationale; metadata.revision_reason; metadata.last_revised | Still described the October tiers (video-EEG optional, red-flag tests recommended, examination the only required act). | FIXED |

## Changes
The literature step is gone (class LIT). The examination is now joined in the stop rule by two required tests: video-EEG, because none of her episodes has been seen by a clinician, so only a recorded habitual episode without ictal change takes the diagnosis past the ILAE possible level (ILAE 2013; AAN 2025); and a 12-lead ECG for the episodes with apparent loss of responsiveness (NICE CG109), answered by a case-specific normal ECG (sinus 82/min, QTc 426 ms) instead of the shared template. Somatic symptom disorder is removed from the diagnosis label and from the psychological therapy must (DSM-5 criterion B not documented). The diagnosis must names the recorded episode. Criteria and follow-ups are reordered to the condition order.

## Verification
perfect_agent.py -v: ok (ECG <- initial_tool_outputs.ecg, video-EEG <- initial_tool_outputs.eeg). test_case_guards -k FND-S11: pass. case_io.py check: no failure names FND-S11.
Pass 1: 0 errors found
- Checked: note rulings correct (LIT; VEEG required, no episode seen by a clinician; SSD removed from accepted[0] and M-PSY, PHQ-15 kept as a score only); ECG 82/min matches vitals, QTc 426 ms consistent with QT 364 ms; stop rule exam, ECG, video-EEG.
- Re-run after the fixes: perfect_agent.py -v ok; test_case_guards -k for the case: pass; case_io.py check: no failure names this case (the only condition-wide failure is test_library_never_answers_a_contradicted_order[FND-RS02], another case).
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Checked: every note id has a correct ruling in the log and rulings file (LIT; VEEG tier per whether a clinician witnessed an event; DX label, accepted[0] only, synonyms untouched); ECG rate matches the vitals and Bazett QTc matches the stored QT; stop rule = the required criteria; criteria and follow-up order per plan 2.ORDER; drug-check output agrees with the medication list and does not repeat expected_evidence; no patient-text leakage; no em dashes in new text.
- Re-run: perfect_agent.py -v ok; test_case_guards -k for the batch: 48 passed; case_io.py check: no failure names this case (only test_library_never_answers_a_contradicted_order[FND-RS02], another case).
Cosmetic (not counted): none.
Pass 3: 0 errors found
- Checked without change: three note rulings correct (LIT; VEEG required, no clinician-witnessed episode; SSD removed from accepted[0] and M-PSY, PHQ-15 kept as a score); ECG 82 = vitals, QTc 364/sqrt(0.732) = 426 ms; timeline (daughter left 6 weeks ago, symptoms 3 weeks) consistent; drug check matches venlafaxine and naproxen; stop rule exam, ECG, video-EEG; no leakage; no em dashes in new text.
- Re-run: perfect_agent.py -v ok (every required/recommended criterion served by the case's own data, none by the library or case fallback; mri_probe confirms the stored plain DWI study for the MRI orders); test_case_guards -k for the batch: 48 passed; case_io.py check: schema and synonym guard OK, no failure names this case (only test_library_never_answers_a_contradicted_order[FND-RS02], another case).
Cosmetic (not counted): none.
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (45): MoCA 27/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.6, TOMM trial 2 49/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-S11 passes.
Pass 5: 0 errors found
- Verified the condition-audit change only (neuropsychology battery numbers): MoCA 27/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.6, TOMM trial 2 49/50 in quantitative_data match the MoCA and TOMM findings rows; all values are in the normal range (MoCA >= 26, z > -1, TOMM above the 45 cut-off), so they agree with the impression (cognition within normal limits, performance validity passed); no other field of the case cites these numbers (grep MoCA, RAVLT, Trail, TOMM). perfect_agent.py -v ok; test_case_guards -k (eight cases) 64 passed.
