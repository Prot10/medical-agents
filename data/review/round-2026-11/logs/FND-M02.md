# FND-M02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| ea6a9490 | FIXED (class LIT) | No literature criterion or output left (checked). |
| 52f87e18 | FIXED (VEEG, STOP) | ground_truth.action_criteria[4] action-5-analyze-eeg optional to recommended, canonical rationale and citations; taper must (required_recommendations[4]) unchanged, already conditional on the video-EEG; the test is a recommended criterion, and actions matching a criterion are never counted as extra (policy_reward.py, stopping); display: CENTRAL C1. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.action_criteria[1] (action-ecg); initial_tool_outputs.ecg | Class ECG (plan 2.ECG, note f4d98130 of M01): events with unresponsiveness, ECG was optional and answered by the template fallback. | FIXED: required, canonical text, case ECG (sinus 92/min, QTc 438 ms); fallback ecg null; stop rule exam, drug check, ECG. |
| C | minor | initial_tool_outputs.labs.panels.BMP (Sodium, Chloride) | Na 132 and Cl 93 flagged abnormal with clinical_significance null. | FIXED: short interpretation (mild hyponatremia, sertraline a recognised cause via SIADH; chloride low in proportion). |
| A | minor | ground_truth.action_criteria; followup_outputs | Order did not follow 2.ORDER. | FIXED: exam, ECG, labs, MRI, video-EEG, drug check, neuropsychology; follow-ups neuropsychology then performance status. |
| E | minor | metadata.revision_reason | Said 'video-EEG optional'. | FIXED: updated. |
| B | major | patient.clinical_history.social_history.living_situation | 'Lives with her husband and two children' contradicted the HPI and stressors (separated from her husband 3 months ago, estranged husband, custody dispute); pre-existing. | FIXED (verifier pass 2): 'Lives with her two children (ages 5 and 7) in a single-story home; separated from her husband 3 months ago'. |
| B | minor | ground_truth.key_clinical_evidence[3]; metadata.difficulty_rationale | Called the recording a '72-hour video-EEG', but she was admitted two days ago and the stored events are on day 1 and day 2 (pre-existing). | FIXED (verifier pass 3): 'the video-EEG over the two days since admission' / 'the video-EEG since admission'. |

## Changes
FND-M02 (42-year-old woman, functional seizures with functional leg weakness and tremor, on levetiracetam started for presumed epilepsy). The video-EEG is now recommended rather than optional (an event was witnessed on examination; ILAE 2013, AAN 2025): completing the planned monitoring is credited and never penalised, but not mandatory. The levetiracetam taper must still waits for a secure diagnosis, ideally with a habitual event documented on video-EEG. By the condition-wide ECG ruling (NICE CG109, apparent loss of consciousness) the 12-lead ECG is now required, with a case-specific stored ECG (sinus 92/min, PR 152, QRS 84, QTc 438 ms). Stop rule: examination, medicine review, ECG. The mild hyponatremia (Na 132) now carries a clinical-significance line naming sertraline as a recognised cause. Criteria and follow-ups are reordered to the clinical sequence. No literature step remains; diagnosis, musts and differential are unchanged.

## Verification
Pass 1: 0 errors found
- None. Checked: every note has a ruling and the ruling matches the plan; tiers, stop rule, stored outputs, musts, differential and KCE agree; perfect_agent.py -v passes with each criterion served its own report; test_case_guards -k passes.
Cosmetic (not counted): action-neuropsych-battery rationale said the battery 'costs more than any other step on this pathway', but it is priced as the video-EEG (1104 each in costs.yaml); now 'costs as much as the video-EEG'; 'recognised' to 'recognized' in the new BMP sodium clinical_significance (American spelling)
Pass 2: 1 errors found
- patient.clinical_history.social_history.living_situation said she lives with her husband, contradicting the separation in the HPI and stressors (pre-existing); corrected.
- Re-checked after the fix: perfect_agent.py passes, test_case_guards -k passes.
Cosmetic (not counted): rulings file, note 52f87e18 'what': sentence starting 'the test is' capitalized.
Pass 3: 1 errors found
- key_clinical_evidence[3] and metadata.difficulty_rationale said '72-hour video-EEG', contradicting the HPI (admitted two days ago) and the stored events on day 1 and day 2; the duration is removed.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case; the only FND failure is FND-RS02).
Cosmetic (not counted): none.
Pass 4: 0 errors found
- None. Checked: rulings of ea6a9490, 52f87e18 (VEEG recommended; taper must conditional on a secure diagnosis); ECG required, rate 92 vs HR 93, QTc 438 ms; stop rule exam, drug check, ECG (all required); levetiracetam taper must vs 'stop it abruptly' prohibition consistent; living situation and video-EEG duration consistent with the HPI.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case).
- For the lead (not counted, not changed): the neuropsychology battery numbers (MoCA 28/30, RAVLT z = -0.2, Trail B z = -0.4, TOMM 49/50) are identical in 23 FND cases, a condition-wide template carry-over outside this batch's plan.
Cosmetic (not counted): none.
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (42, severe anxiety): MoCA 27/30, RAVLT delayed recall z = -0.3, Trail Making B z = -0.6, TOMM trial 2 49/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-M02 passes.
Pass 5: 0 errors found
- None. Checked the condition-audit neuropsychology values in `followup_outputs[request_neuropsych_battery]`: MoCA, RAVLT, Trail Making B and TOMM agree between `quantitative_data` and the findings, all lie in the normal range (TOMM above the 45 cut-off) and match the impression 'within normal limits, performance validity passed'; no other field of the case cites them; GAD-7 and PHQ-9 labels match their bands (GAD-7 10-14 moderate, 15-21 severe; PHQ-9 5-9 mild, 10-14 moderate, 15-19 moderately severe) and the self-report sentence in findings and impression.
- Re-checked: perfect_agent.py -v passes; test_case_guards -k (all 8 FND pass-5 cases) 64 passed.
Cosmetic (not counted): none.
