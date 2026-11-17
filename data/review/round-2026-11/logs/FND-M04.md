# FND-M04

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 30667d14 | FIXED (class LIT) | No literature criterion or output left (checked). |
| 80fea3da | FIXED (class LIT) | The literature criterion was removed by the class; none left. |
| 6a40c3ea | FIXED (VEEG) | ground_truth.action_criteria[2] action-4-analyze-eeg optional to required, M04 canonical rationale, citations; stop_rule.required_before_assessment = exam, video-EEG, ECG; required_recommendations[0] (M-DX) and [1] (M-COMM) no longer 'where recorded'; metadata.difficulty_rationale updated. Checked: initial_tool_outputs.eeg.activating_procedures has hyperventilation, photic_stimulation, eye_closure; differential 'Absence epilepsy or eyelid myoclonia' low, citing the recording. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.action_criteria[1] (action-ecg); initial_tool_outputs.ecg | Class ECG: brief unresponsiveness, ECG was optional and answered by the template fallback. | FIXED: required, canonical text, case ECG (sinus 96/min, QTc 436 ms on escitalopram); fallback ecg null. |
| A | minor | ground_truth.action_criteria | Order checked against 2.ORDER. | FIXED: exam, ECG, video-EEG, drug check, neuropsychology (unchanged sequence apart from tiers). |
| E | minor | metadata.revision_reason | Said 'video-EEG optional'. | FIXED: updated. |
| B | major | ground_truth.action_criteria action-neuropsych-battery.rationale | Said the diagnosis 'rests on the examination', contradicting the now-required video-EEG (the examination has no rule-in sign and cannot separate the events from absences). | FIXED (verifier pass 1): 'rests on the semiology of the events and the habitual event recorded on video-EEG'; cost wording corrected (priced as the video-EEG). |
| B | major | ground_truth.red_herrings[0], [2].correct_interpretation | Said 'the semiology of the events decides it' and 'the event semiology makes the diagnosis', contradicting the required video-EEG rationale of note 6a40c3ea (the observed event cannot be separated from absences at the bedside). | FIXED (verifier pass 2): the habitual event recorded on video-EEG without ictal change decides it / makes the diagnosis. |
| E | minor | ground_truth.differential[0].key_features | 'Habitual events recorded' while one event was recorded. | FIXED (verifier pass 3): 'A habitual event recorded'. |
| B | minor | patient.history_present_illness; patient.clinical_history.social_history.occupation | Called her a 'marketing manager' while the HPI and recent_stressor say she was promoted to marketing director 3 months ago (pre-existing). | FIXED (verifier pass 4): 'marketing director' in the HPI; occupation 'Marketing director (promoted 3 months ago)'. |

## Changes
FND-M04 (35-year-old woman, functional seizures mimicking absences: eyelid flutter with brief unresponsiveness, some events after bright light). As the physician ruled, the video-EEG with hyperventilation and photic stimulation is now required and in the stop rule: the observed event cannot be told from absence seizures or eyelid myoclonia at the bedside and there is no positive functional sign, so only a recorded habitual event without ictal change establishes the diagnosis (ILAE 2013; AAN 2025). The diagnosis must and the explanation must now rest on that recording rather than 'where recorded'. By the condition-wide ECG ruling the 12-lead ECG is required, with a case-specific ECG (sinus 96/min, PR 146, QRS 82, QTc 436 ms). Stop rule: examination, video-EEG, ECG. The differential keeps absence epilepsy or eyelid myoclonia at low, citing the recording. No literature step remains.

## Verification
Pass 1: 1 errors found
- action-neuropsych-battery rationale: 'the diagnosis ... rests on the examination' contradicted the required video-EEG of note 6a40c3ea; corrected.
- Re-checked after the fixes: perfect_agent.py passes, test_case_guards -k passes.
Cosmetic (not counted): initial_tool_outputs.ecg.intervals.QT 344 to 345 ms so that Bazett QTc at 96/min rounds to the stated 436 ms (344 gave 435)
Pass 2: 1 errors found
- red_herrings[0] and [2] still said the semiology decides or makes the diagnosis, against the required video-EEG of note 6a40c3ea; corrected.
- Re-checked after the fix: perfect_agent.py passes, test_case_guards -k passes.
Cosmetic (not counted): none.
Pass 3: 0 errors found
- None. Checked: rulings against plan (LIT, VEEG required with the M04 rationale, ECG required); stop rule exam, video-EEG, ECG (all required); stored EEG lists hyperventilation, photic stimulation and eye closure; ECG rate 96 vs HR 98, QTc 345/sqrt(0.625) = 436 ms; absence epilepsy or eyelid myoclonia low citing the recording; no leakage in the patient block.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case; the only FND failure is FND-RS02).
Cosmetic (not counted): differential[0] 'Habitual events recorded' to 'A habitual event recorded' (one event was recorded).
Pass 4: 1 errors found
- patient HPI and social_history.occupation called her a marketing manager, contradicting her promotion to marketing director 3 months ago in the same HPI and in recent_stressor (pre-existing); corrected to director.
- Also checked: VEEG required with the M04 rationale; stored EEG lists hyperventilation, photic stimulation, eye closure; M-DX and M-COMM rest on the recording; ECG required (96 vs HR 98, QTc 436 ms); stop rule exam, video-EEG, ECG.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case).
- For the lead (not counted, not changed): the neuropsychology battery numbers (MoCA 28/30, RAVLT z = -0.2, Trail B z = -0.4, TOMM 49/50) are identical in 23 FND cases, a condition-wide template carry-over outside this batch's plan.
Cosmetic (not counted): none.
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (35, marketing director): MoCA 29/30, RAVLT delayed recall z = 0.4, Trail Making B z = 0.1, TOMM trial 2 50/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-M04 passes.
Pass 5: 0 errors found
- None. Checked the pass-4 fix (HPI and `social_history.occupation` now 'marketing director', consistent with `recent_stressor` 'promotion to director level' and the HPI promotion 3 months ago; no 'manager' left in the case) and the condition-audit neuropsychology values in `followup_outputs[request_neuropsych_battery]`: MoCA, RAVLT, Trail Making B and TOMM agree between `quantitative_data` and the findings, all lie in the normal range (TOMM above the 45 cut-off) and match the impression 'within normal limits, performance validity passed'; no other field of the case cites them; GAD-7 and PHQ-9 labels match their bands (GAD-7 10-14 moderate, 15-21 severe; PHQ-9 5-9 mild, 10-14 moderate, 15-19 moderately severe) and the self-report sentence in findings and impression.
- Re-checked: perfect_agent.py -v passes; test_case_guards -k (all 8 FND pass-5 cases) 64 passed.
Cosmetic (not counted): none.
