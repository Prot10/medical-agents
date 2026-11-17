# FND-RM01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 18418180 | FIXED (class LIT, commit 393c547e) | Checked: no literature criterion or output left. |
| 3cf7ca94 | FIXED (LABS) | ground_truth.action_criteria[2] action-sodium-osmolality recommended to required, safety rationale (measured, not assumed; Spasovski 2014), citation 'Spasovski G et al. Eur J Endocrinol 2014;170:G1-G47'; stop_rule.required_before_assessment = exam, ECG, sodium; initial_tool_outputs.labs.panels['Electrolytes and osmolality'][0].clinical_significance filled ('Mild hyponatremia, well above the levels at which hyponatremia provokes seizures; consistent with the reported high water intake.'). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.action_criteria[1] (action-ecg); initial_tool_outputs.ecg; fallback_tool_outputs.ecg | Class ECG: events with apparent loss of responsiveness, on risperidone, ECG optional and answered only by the case fallback. | FIXED: required, canonical label, rationale (with risperidone) and [NICE_CG109]; case ECG moved into initial_tool_outputs.ecg (sinus 88/min vs vitals 84, PR 184, QRS 112 incomplete RBBB kept, QTc 434, explicit no pre-excitation, no coved or saddleback ST elevation, no heart block); fallback ecg null; metadata.fallback_tool_kinds.ecg removed; key_clinical_evidence[3] added. |
| C | major | ground_truth.action_criteria[3] (action-4-analyze-eeg) | Class VEEG: event witnessed on examination; video-EEG was optional. | FIXED: recommended, canonical rationale; October sentence deleted; M-DX keeps 'confirmed on video-EEG where recorded'. |
| A | minor | ground_truth.action_criteria; followup_outputs | Order not per 2.ORDER. | FIXED: exam, ECG, sodium, video-EEG, drug check, neuropsychology (ids unchanged); follow-ups neuropsychology, performance status. |
| B | minor | ground_truth.avoided_actions (avoid-waste-2-order-echocardiogram, avoid-waste-3-order-cardiac-monitoring).rationale | 'the events keep responsiveness' contradicted the HPI (apparent loss of consciousness) and the recorded event 3 (apparent unresponsiveness). | FIXED: 'eyes closed, responsiveness when tested and immediate recovery', and the 12-lead ECG answers the cardiac screening question. |
| E | minor | initial_tool_outputs.drug_interactions.general.summary | Haloperidol 'contraindicated by allergy'; the record is an acute dystonic reaction. | FIXED: 'by his documented acute dystonic reaction'. |
| C | minor | fallback_tool_outputs.labs.panels.prolactin[0].clinical_significance | Abnormal prolactin with null significance. | FIXED: raised on risperidone; a random sample not timed to an event cannot be interpreted for the events. |
| C | minor | metadata.difficulty_rationale | Did not mention the ECG. | FIXED: 'check the sodium and obtain an ECG'. |
| C | minor | ground_truth.action_criteria[5] (action-neuropsych-battery).expected_evidence | Template text 'mood, anxiety and somatic symptom burden', but the stored battery measures no somatic symptom burden (MoCA, GAD-7, PHQ-9, DES-II, TOMM). | FIXED: evidence names what the stored battery reports (anxiety, mood and dissociative symptoms, performance validity). |
| E | minor | metadata.revision_reason, metadata.last_revised | Revision text stale (said red-flag tests recommended / October only). | FIXED: November changes stated; last_revised 2026-11-16. |

## Changes
FND-RM01 (38-year-old man with schizophrenia on risperidone, psychogenic polydipsia of 7 to 8 L/day and a prior hyponatremic seizure, with functional seizures and functional leg weakness). Serum sodium and osmolality are now a required safety test and in the stop rule: the sodium must be measured, not assumed, before the events are attributed to anything else; the stored sodium of 134 mEq/L now carries an interpretation (mild, well above seizure-provoking levels). The 12-lead ECG is also required, because his events include apparent unresponsiveness and he takes risperidone (NICE CG109); it is answered by a case ECG (sinus rhythm 88/min, incomplete right bundle branch block kept from the earlier record, normal PR and QTc, no pre-excitation, Brugada pattern or heart block) instead of the case fallback. The video-EEG is now recommended (an event was witnessed on examination). Criteria and follow-ups follow the clinical order. The echocardiography and monitoring waste rationales no longer say the events keep responsiveness, the drug review calls the haloperidol reaction a dystonic reaction rather than an allergy, and the fallback prolactin row is interpreted. Diagnosis label, musts and prohibitions are unchanged; no literature step remains.

## Verification
Pass 1: 0 errors found
Checked: every note id has a ruling in the log and rulings file and each ruling matches the plan; diff vs 06b74446 read, final case read in full (patient, criteria, stop rule, sequence, avoided actions, musts, prohibitions, differential, KCE, red herrings, metadata, stored outputs); no literature output left; perfect_agent.py -v passes and each criterion receives its own report (served outputs printed for the '?' rows); case_io check and test_case_guards -k pass for this case (the only suite failure is FND-RS02, not in this batch); no em dashes in new text. Also checked the ECG (rate 88 vs vitals 84, incomplete RBBB kept, Brugada pattern explicitly excluded) and the sodium panel served to the sodium/osmolality order.
Cosmetic (not counted): none.
