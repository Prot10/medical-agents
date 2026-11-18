# FND-M06

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 546d3260 | FIXED (class LIT) | No literature criterion or output left (checked). |
| a37be9ec | FIXED (VEEG) | ground_truth.action_criteria[1] action-4-analyze-eeg optional to required, M06 canonical rationale, citations [ILAE_PNES_2013], [AAN_Functional_Seizures_2025]; stop_rule.required_before_assessment = exam, video-EEG; required_recommendations[0] (M-DX) 'and the habitual new event recorded on video-EEG without ictal change'. ECG stays waste (no reported unresponsiveness in the new events). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | initial_tool_outputs.labs.panels['Glucose and HbA1c'] | HbA1c 7.1% and fasting glucose 128 abnormal with clinical_significance null. | FIXED: short interpretations referring to the known type 2 diabetes. |
| E | minor | metadata.revision_reason | Said 'video-EEG optional'. | FIXED: updated. |
| B | major | ground_truth.action_criteria action-neuropsych-battery.rationale | Said the diagnosis 'rests on the examination', contradicting the now-required video-EEG (no event seen, established epilepsy). | FIXED (verifier pass 1): 'rests on the semiology of the events and the habitual event recorded on video-EEG'; cost wording corrected. |
| B | major | fallback_tool_outputs.ecg.rate | Template fallback ECG (served to the waste ECG order) gave 68/min against a vitals heart rate of 82. | FIXED (verifier pass 1): rate 80. |
| B | major | ground_truth.red_herrings[0], [1].correct_interpretation | Said the semiology of the events 'decides it' / 'makes the diagnosis', contradicting the required video-EEG of note a37be9ec (no event seen; history gives only the possible level). | FIXED (verifier pass 2): the semiology raises functional seizures and the habitual new event recorded on video-EEG without ictal change decides it. |
| E | minor | ground_truth.action_criteria action-4-analyze-eeg.rationale | Canonical 'screens for co-occurring epilepsy' read oddly in a man whose epilepsy is established. | FIXED (verifier pass 3): 'separates the new events from a new epileptic seizure type'. |
| E | minor | initial_tool_outputs.labs.panels['Glucose and HbA1c'] HbA1c.reference_range | Reference range '<7.0%' is the diabetes treatment target, not the reference interval (pre-existing). | FIXED (verifier pass 4, cosmetic): '<5.7 (non-diabetic); treatment target in diabetes usually <7.0'; flag unchanged. |

## Changes
FND-M06 (42-year-old truck driver with established right temporal lobe epilepsy, new seizure-like events of different semiology). As the physician ruled, video-EEG capture of a habitual new-type event is now required and in the stop rule: no clinician has seen an event, so the history supports functional seizures only at the ILAE possible level, and with established epilepsy and persistent interictal discharges only the recording separates the new events from a new epileptic seizure type (ILAE 2013; AAN 2025). The diagnosis must now names the recorded event instead of 'where recorded'. Levetiracetam continues for the epilepsy (unchanged musts). The ECG stays waste. The raised HbA1c and fasting glucose carry a short interpretation. Stop rule: examination and video-EEG. No literature step remains.

## Verification
Pass 1: 2 errors found
- action-neuropsych-battery rationale: 'the diagnosis ... rests on the examination' contradicted the required video-EEG of note a37be9ec; corrected.
- fallback ECG rate 68/min contradicted the vitals heart rate 82; set to 80.
- Re-checked after the fixes: perfect_agent.py passes, test_case_guards -k passes.
Cosmetic (not counted): none.
Pass 2: 1 errors found
- red_herrings[0] and [1] still said the semiology decides or makes the diagnosis, against the required video-EEG of note a37be9ec; corrected.
- Re-checked after the fix: perfect_agent.py passes, test_case_guards -k passes.
Cosmetic (not counted): none.
Pass 3: 0 errors found
- None. Checked: rulings against plan (LIT, VEEG required with the M06 rationale, ECG waste); stop rule exam and video-EEG (both required); stored video-EEG records a new-type event without ictal change with persistent right temporal discharges; musts keep levetiracetam and prohibit tapering it; no criterion matches an avoided action.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case; the only FND failure is FND-RS02).
Cosmetic (not counted): action-4-analyze-eeg rationale 'screens for co-occurring epilepsy' (his epilepsy is established) to 'separates the new events from a new epileptic seizure type'.
Pass 4: 0 errors found
- None. Checked: VEEG required with the M06 rationale and citations; stop rule exam + video-EEG; M-DX names the recorded event; levetiracetam continue must vs taper prohibition consistent; ECG waste per plan (no reported unresponsiveness in the new events); fallback ECG rate 80 vs HR 82; driving must present.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case).
Cosmetic (not counted): labs HbA1c reference_range '<7.0%' (a treatment target) to '<5.7 (non-diabetic); treatment target in diabetes usually <7.0'.
