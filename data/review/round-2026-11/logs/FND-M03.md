# FND-M03

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| fd6b12e4 | FIXED (class LIT) | No literature criterion or output left (checked). |
| 06d86723 | FIXED (class LIT) | The literature criterion was removed by the class; none left. |
| 3327b25f | FIXED (VEEG, STOP) | ground_truth.action_criteria[1] action-4-analyze-brain-mri stays recommended; ground_truth.action_criteria[3] action-5-analyze-eeg optional to recommended, canonical rationale and citations; stop rule unchanged (exam); the test is a recommended criterion, and actions matching a criterion are never counted as extra (policy_reward.py, stopping); display: CENTRAL C1. |
| 32418708 | FIXED (ENTRAIN) | initial_tool_outputs.clinical_assessment: findings[2] sign/result, criteria_met.tremor_entrainment_positive false, scores.positive_rule_in_signs_documented 3 to 2, impression; ground_truth.action_criteria[0] expected_evidence and rationale; ground_truth.assessment.required_recommendations[0] (M-DX); ground_truth.key_clinical_evidence[1]; metadata.difficulty_rationale. patient.neurological_exam.additional unchanged (already describes suppression; 'entrainment maneuver' names the test). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | initial_tool_outputs.labs.panels.BMP (Sodium, Chloride) | Na 132 and Cl 94 abnormal with clinical_significance null. | FIXED: short interpretation (escitalopram 20 mg a recognised cause via SIADH). |
| A | minor | ground_truth.action_criteria; followup_outputs | Order did not follow 2.ORDER (labs after drug check). | FIXED: exam, MRI, labs, video-EEG, drug check, neuropsychology; follow-ups neuropsychology then performance status. |
| E | minor | metadata.revision_reason | Said 'video-EEG optional'. | FIXED: updated. |
| C | minor | ground_truth.action_criteria (ECG) | No ECG criterion: events with preserved responsiveness (responds to his name), per plan 2.ECG. | FLAGGED: no change (correct). |

## Changes
FND-M03 (29-year-old man, functional seizures with functional right-sided weakness). The sign seen during the observed event (the arm shaking stopped while he tapped a rhythm with his foot and resumed at another frequency) is now classified as distractibility, not entrainment, because the shaking never adopted the imposed rhythm; the entrainment flag is off, the validated-sign count is 2 (collapsing weakness, distractibility; Hoover equivocal), and the impression, diagnosis must, key evidence, exam criterion and difficulty rationale no longer cite entrainment. The brain MRI for the post-event deficit stays recommended, and the video-EEG is now recommended rather than optional (event witnessed; ILAE 2013, AAN 2025); both are credited, never counted as extra actions, and not mandatory. Stop rule: examination. The mild hyponatremia (Na 132) carries a clinical-significance line naming escitalopram. Criteria and follow-ups are reordered to the clinical sequence. No ECG criterion, since the events keep responsiveness. No literature step remains.

## Verification
Pass 1: 0 errors found
- None. Checked: every note has a ruling and the ruling matches the plan; tiers, stop rule, stored outputs, musts, differential and KCE agree; perfect_agent.py -v passes with each criterion served its own report; test_case_guards -k passes.
Cosmetic (not counted): action-neuropsych-battery rationale said the battery 'costs more than any other step on this pathway', but it is priced as the video-EEG (1104 each in costs.yaml); now 'costs as much as the video-EEG'; 'recognised' to 'recognized' in the new BMP sodium clinical_significance (American spelling)
Pass 2: 0 errors found
- None. Checked: note rulings against plan (LIT, VEEG recommended, MRI recommended, ENTRAIN); sign count 2 (collapsing weakness, distractibility) matches the findings and criteria_met; no remaining 'entrainment' claim except the HPI/exam naming the maneuver; no ECG criterion is correct (responsive to voice during events); perfect_agent.py -v and test_case_guards -k pass; mri_probe shows the plain DWI study.
Cosmetic (not counted): none.
Pass 3: 0 errors found
- None. Checked: ENTRAIN applied (flag false, count 2, impression, M-DX, KCE, exam evidence; exam text names only the maneuver); MRI and video-EEG recommended, stop rule exam; no ECG (responsive to voice); soft constraint ids exist; mri_probe shows the plain DWI study.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case; the only FND failure is FND-RS02).
Cosmetic (not counted): none.
Pass 4: 0 errors found
- None. Checked: ENTRAIN (flag false, finding renamed, count 2 = collapsing weakness + distractibility, impression, M-DX, KCE, exam evidence); MRI and video-EEG recommended, stop rule exam only; no ECG (responsive to his name in every described event); soft constraint ids exist; mri_probe shows the plain study.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case).
- For the lead (not counted, not changed): the neuropsychology battery numbers (MoCA 28/30, RAVLT z = -0.2, Trail B z = -0.4, TOMM 49/50) are identical in 23 FND cases, a condition-wide template carry-over outside this batch's plan.
Cosmetic (not counted): none.
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (29, moderately severe depressive symptoms): MoCA 28/30, RAVLT delayed recall z = -0.5, Trail Making B z = -0.2, TOMM trial 2 50/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-M03 passes.
Pass 5: 0 errors found
- None. Checked the condition-audit neuropsychology values in `followup_outputs[request_neuropsych_battery]`: MoCA, RAVLT, Trail Making B and TOMM agree between `quantitative_data` and the findings, all lie in the normal range (TOMM above the 45 cut-off) and match the impression 'within normal limits, performance validity passed'; no other field of the case cites them; GAD-7 and PHQ-9 labels match their bands (GAD-7 10-14 moderate, 15-21 severe; PHQ-9 5-9 mild, 10-14 moderate, 15-19 moderately severe) and the self-report sentence in findings and impression.
- Re-checked: perfect_agent.py -v passes; test_case_guards -k (all 8 FND pass-5 cases) 64 passed.
Cosmetic (not counted): none.
