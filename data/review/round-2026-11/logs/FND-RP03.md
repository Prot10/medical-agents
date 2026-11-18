# FND-RP03

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 4dc5ddb4-dad0-41b7-b408-61c61e631a68 | FIXED (class LIT, commit 393c547e) | Checked: no literature criterion or stored output left. |
| 384cf96b-5922-4590-8dfd-2fc3ed87d928 | FIXED (VEEG + STOP, plan 2) | `ground_truth.action_criteria[action-5-analyze-eeg]`: optional -> recommended with the canonical recommended rationale; `action-4-analyze-brain-mri` stays recommended. Both tests are recommended criteria, and actions matching a criterion are never counted as extra (`policy_reward.py`, stopping); display: CENTRAL C1. `ground_truth.stop_rule.required_before_assessment` = exam, ECG, drug check. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria` | Class ECG: a phase of apparent unresponsiveness after the shaking, palpitations, no ECG on record (telemetry only). | FIXED: new required `action-ecg` (`[NICE_CG109]`), stored `initial_tool_outputs.ecg` (sinus 80 bpm, PR 176, QRS 94, QTc 434 ms). |
| A | minor | `ground_truth.action_criteria`, `followup_outputs` | Class ORDER. | FIXED: exam, ECG, labs, MRI, video-EEG, drug check, neuropsychology; follow-ups neuropsychology, performance status, skin biopsy. |
| E | minor | `metadata.revision_reason` | Stated video-EEG optional. | FIXED; `last_revised` 2026-11-16. |

## Changes
The patient and all reports are unchanged, apart from a new stored 12-lead ECG (sinus rhythm 80 bpm, normal PR, QRS and QTc 434 ms). The brain MRI stays recommended for the CNS vasculitis question, and the video-EEG is now recommended rather than optional: both are credited when ordered and never count as extra actions, which answers the note; neither is required, because a typical event was witnessed on examination. A 12-lead ECG is now required for the events with apparent unresponsiveness (NICE CG109) and enters the stop rule with the examination and the medication review. Criteria and follow-ups are in the clinical order. The literature step was removed earlier this round (class LIT). RP03 keeps its scenario; its former duplicate RS02 was replaced.

## Verification
Pass 1: 0 errors found
- Checked: MRI stays recommended, video-EEG optional -> recommended (event witnessed on examination), the allow-note answered by the tier with CENTRAL C1; new required ECG (80 bpm against vitals 78) for the motionless unresponsive phase; stop rule = exam, ECG, drug check; the taper must keeps "ideally with a habitual event documented on video-EEG" as the recommended-tier wording requires; no RS02 pairing text left in metadata. perfect_agent, mri_probe and test_case_guards -k FND-RP03 pass.
Pass 2: 0 errors found
- Re-checked every note ruling, the tiers and stop rule against plan 3, the ECG rate against the vitals, the served evidence of each required and recommended criterion, musts against prohibitions and avoided actions, and the differential against the pathway results; nothing to change. perfect_agent and test_case_guards pass for this case.
Pass 3: 0 errors found
- Checked: both note rulings hold (MRI and video-EEG recommended, credited and never extra; CENTRAL C1 for the display); new required ECG 80 bpm against vitals 78, for the motionless unresponsive phase; the echocardiogram waste rationale says 'no structural cardiac question', which agrees with the ECG; stop rule = exam, ECG, drug check; criteria and follow-ups in plan order; mri_probe unchanged (stored plain MRI, not edited this round). perfect_agent -v passes (each required and recommended criterion receives its own stored report) and test_case_guards -k FND-RP03 passes.
Pass 4: 0 errors found
- Checked: every note id has a ruling that matches plan 3 and the case; tiers, stop rule (all ids are required criteria), musts against prohibitions and avoided actions, ECG rate against the vitals, the differential against the pathway results, leakage in the patient block, and the stored drug check against the medicines and allergies. The exam sign count (`scores.positive_rule_in_signs_documented`) differs from the number of true flags because, by October fact 2, inconsistency between examination and function is not a counted rule-in sign; correct as stored. perfect_agent -v passes (each required and recommended criterion receives its own stored report) and test_case_guards -k for this case passes.
Condition audit (17 Nov 2026): 1 error found
- D (leakage, kind 1), minor: `initial_tool_outputs.drug_interactions.general.summary` ended with the instruction "withdraw the antiseizure drug and benzodiazepine gradually". That is a management prescription in a pharmacology report, and it implies the events are not epileptic before the video-EEG or examination has been obtained. FIXED: "if they are stopped, the antiseizure drug and the benzodiazepine are reduced gradually rather than abruptly" (the conditional form already used in FND-M02). `ground_truth.action_criteria[action-2-check-drug-interactions].expected_evidence` now says "Levetiracetam and diazepam not to be stopped abruptly, ..." to match the report. Tier, rationale, musts and rulings unchanged.
- Re-checked: perfect_agent.py FND-RP03 -v passes; test_case_guards -k FND-RP03 passes.
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (62, retired engineer): MoCA 27/30, RAVLT delayed recall z = -0.1, Trail Making B z = -0.5, TOMM trial 2 49/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-RP03 passes.
Pass 5: 0 errors found
- Checked (focused, changes after the last 0-error pass): drug-check summary now conditional (no management prescription), action-2 expected evidence matches the report and the warnings; the condition-audit neuropsychology values (quantitative_data and findings agree, all within normal limits for age, TOMM above the 45 cut-off, impression unchanged, no other field cites them). perfect_agent.py -v passes; test_case_guards -k (8 cases) 63 passed, the only failure test_library_never_answers_a_contradicted_order[FND-RS02] (library_contradictions.yaml, already CENTRAL).
