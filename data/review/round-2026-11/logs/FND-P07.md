# FND-P07

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 3a7cedc9 | FIXED (class LIT, commit 393c547e) | Checked: no literature criterion or output left. |
| a383af93 | FIXED (decision 10) | Second option applied (a reproducible positive sign documented), first option already in place: patient.neurological_exam.motor and .additional now document collapsing (give-way) weakness of left shoulder abduction, elbow flexion and wrist extension; initial_tool_outputs.clinical_assessment.findings[3] new 'Collapsing (give-way) weakness' (the former 'Left arm strength' row, reflexes split into findings[4]), criteria_met.give_way_weakness true, scores.positive_rule_in_signs_documented 3 to 4, impression; ground_truth.action_criteria[0] expected_evidence and rationale; ground_truth.assessment.required_recommendations[0] (M-DX); ground_truth.key_clinical_evidence[0]; ground_truth.differential[1]. Brain MRI (action_criteria[1]) stays recommended: the test is a recommended criterion, and actions matching a criterion are never counted as extra (`policy_reward.py`, stopping); display: CENTRAL C1. |
| 4f56047d | FIXED (AVOID) | ground_truth.avoided_actions[9] avoid-waste-levodopa-challenge (perform_clinical_assessment {assessment_type: levodopa_challenge}, waste, [Espay_2018]); followup_outputs[3] moved after the credited steps. Probe: the order gets its stored report and matches only the avoided action. |
| 2604d242 | FIXED (AVOID) | ground_truth.avoided_actions[8] avoid-waste-mibg-scan (order_advanced_imaging {modality: MIBG_scan}, waste, [Espay_2018]); followup_outputs[4] moved last. Probe: the order gets its stored report and matches only the avoided action. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| E | minor | patient.neurological_exam.additional | 'all developing acutely over 4 weeks' is self-contradictory. | FIXED: 'all developing over 4 weeks'. |
| A | minor | followup_outputs | Order: on-request performance status, levodopa challenge and cognitive screen before the credited neuropsychology. | FIXED: neuropsychology, performance status, cognitive screen, levodopa challenge, MIBG. |
| C | minor | metadata.difficulty_rationale | Did not name the two new waste tests. | FIXED: adds cardiac MIBG and levodopa challenge. |
| C | minor | ground_truth.action_criteria[3] (action-neuropsych-battery).expected_evidence | Template text 'mood, anxiety and somatic symptom burden', but the stored battery measures no somatic symptom burden (MoCA, GDS-15, HADS-A, TOMM). | FIXED: evidence names what the stored battery reports (depressive and anxiety symptoms, performance validity). |
| E | minor | metadata.revision_reason, metadata.last_revised | Revision text stale (said red-flag tests recommended / October only). | FIXED: November changes stated; last_revised 2026-11-16. |

## Changes
FND-P07 (61-year-old woman with established right-predominant Parkinson's disease and a new left functional tremor and arm weakness). The left arm weakness now has a documented positive sign: collapsing (give-way) weakness of shoulder abduction, elbow flexion and wrist extension, reproducible on repeated testing, written into the examination, the examination report (4 rule-in signs), the exam criterion, the diagnosis must and the key evidence; the diagnosis therefore no longer rests on a 3/5 grade alone. The brain MRI stays recommended (credited, never penalised as an extra action). Cardiac MIBG scintigraphy and a levodopa challenge are now waste avoided actions, because her Parkinson's disease is established and neither test separates the functional tremor from parkinsonian progression; their stored reports still answer such orders and now sit at the end of the pathway. Diagnosis label, differential likelihoods, musts other than M-DX and prohibitions are unchanged; no literature step remains.

## Verification
Pass 1: 0 errors found
Checked: every note id has a ruling in the log and rulings file and each ruling matches the plan; diff vs 06b74446 read, final case read in full (patient, criteria, stop rule, sequence, avoided actions, musts, prohibitions, differential, KCE, red herrings, metadata, stored outputs); no literature output left; perfect_agent.py -v passes and each criterion receives its own report (served outputs printed for the '?' rows); case_io check and test_case_guards -k pass for this case (the only suite failure is FND-RS02, not in this batch); no em dashes in new text.
Cosmetic (not counted): action-neuropsych-battery label 'Neuropsychological assessment of mood, anxiety and dissociation' changed to 'Neuropsychological assessment of mood and anxiety' (the stored battery has no dissociation measure).
