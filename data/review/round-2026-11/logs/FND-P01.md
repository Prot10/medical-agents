# FND-P01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b7b2460d | FIXED (class LIT, commit 393c547e) | Checked: no literature criterion or output left. |
| a8a1624e | FIXED (MDT) | ground_truth.assessment.required_recommendations[2]: the physiotherapy must is replaced by the canonical MDT must (specialist multidisciplinary FND rehabilitation: physiotherapy, occupational therapy with a functional independence and equipment plan, psychological therapy), given three months of full-time wheelchair use with help for transfers and daily activities. Sources (log only): Nielsen 2015; Nicholson C et al. J Neurol Neurosurg Psychiatry 2020;91:1037-1045 (CENTRAL C5 for the pack). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.action_criteria[1] (action-5-analyze-eeg); ground_truth.stop_rule | Class VEEG: no habitual event seen by a clinician (functional_seizure_semiology_observed false), so the history supports functional seizures only at the ILAE possible level; video-EEG was optional. | FIXED: required, canonical rationale (ILAE 2013; AAN 2025), October 'Without the recording...' sentence deleted; stop rule = exam, video-EEG. |
| C | minor | ground_truth.assessment.required_recommendations[0]; metadata.difficulty_rationale | M-DX said 'confirmed on video-EEG where recorded' and the difficulty rationale 'confirm the events on video-EEG if needed', both stale once the recording is required. | FIXED: M-DX rests on 'the habitual events recorded on video-EEG without ictal change'; difficulty rationale says the events must be recorded since no clinician has seen one. |
| A | minor | followup_outputs | Performance status before the credited neuropsychology follow-up. | FIXED: neuropsychology, performance status. |
| E | minor | metadata.revision_reason, metadata.last_revised | Revision text stale (said red-flag tests recommended / October only). | FIXED: November changes stated; last_revised 2026-11-16. |
| C | note | ground_truth.action_criteria | No ECG criterion: the events keep awareness (plan class ECG, P01 not listed). | No change. |

## Changes
FND-P01 (40-year-old woman, mixed functional neurological disorder with wheelchair-dependent leg weakness, tremor and shaking events). The video-EEG is now a required step and in the stop rule, because no clinician has seen one of her events (only her husband has), so the history alone supports functional seizures only at the ILAE possible level; the stored 72-hour recording of two habitual events without ictal change documents the diagnosis and screens for co-occurring epilepsy. The diagnosis must now rests on the recorded events. The physiotherapy must is replaced by referral to a specialist multidisciplinary FND rehabilitation service (physiotherapy, occupational therapy with a functional independence and equipment plan, psychological therapy), given three months of full-time wheelchair use with help for transfers and daily activities. The performance-status follow-up moved after neuropsychology. Diagnosis label, examination, differential, prohibitions and the waste labels (repeat MRI, nerve studies, lumbar puncture) are unchanged; no literature step remains.

## Verification
Pass 1: 0 errors found
Checked: every note id has a ruling in the log and rulings file and each ruling matches the plan; diff vs 06b74446 read, final case read in full (patient, criteria, stop rule, sequence, avoided actions, musts, prohibitions, differential, KCE, red herrings, metadata, stored outputs); no literature output left; perfect_agent.py -v passes and each criterion receives its own report (served outputs printed for the '?' rows); case_io check and test_case_guards -k pass for this case (the only suite failure is FND-RS02, not in this batch); no em dashes in new text.
Cosmetic (not counted): none.
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (40, on pregabalin, duloxetine and cyclobenzaprine): MoCA 27/30, RAVLT delayed recall z = -0.6, Trail Making B z = -0.9, TOMM trial 2 48/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-P01 passes.
Pass 5: 0 errors found
- None. Checked the condition-audit neuropsychology values in `followup_outputs[request_neuropsych_battery]`: MoCA, RAVLT, Trail Making B and TOMM agree between `quantitative_data` and the findings, all lie in the normal range (TOMM above the 45 cut-off) and match the impression 'within normal limits, performance validity passed'; no other field of the case cites them; GAD-7 and PHQ-9 labels match their bands (GAD-7 10-14 moderate, 15-21 severe; PHQ-9 5-9 mild, 10-14 moderate, 15-19 moderately severe) and the self-report sentence in findings and impression.
- Re-checked: perfect_agent.py -v passes; test_case_guards -k (all 8 FND pass-5 cases) 64 passed.
Cosmetic (not counted): none.
