# NPH-S08

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 49b4998b-e3ea-4a6f-bce3-d4e6bf8a481c | FIXED | The must 'Confirm euthyroid status (TSH 1.8 mIU/L, free T4 1.2 ng/dL) and continue levothyroxine 75 mcg unchanged' is now 'Continue levothyroxine 75 mcg daily unchanged'. Thyroid function and targeted labs (action-3-interpret-labs) stay recommended, not required and not in the stop rule; its rationale now says checking thyroid function is good practice and does not decide the iNPH diagnosis. (ground_truth.assessment.required_recommendations[2]) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.assessment.required_recommendations[0] | Referral must said 'Refer to neurosurgery for CSF shunting with a programmable valve', presuming surgery (plan C1, D1; class of notes 7f90233f, 8bb5643e, 2cd1748b, 6abe35f0) | FIXED: now 'shunt eligibility assessment ... the tap response supports considering a shunt, with a programmable valve if one is placed, but does not by itself decide surgery [Nakajima_2021]' |
| C | major | ground_truth.assessment.required_recommendations[1] | No must on counselling about the expected benefit and the complications of shunting (plan C2, D2) | FIXED: new counselling must (gait most likely to improve, degree uncertain; shunt obstruction needing revision, infection, headache, subdural haematoma from over-drainage [Nakajima_2021]) |
| C | minor | ground_truth.assessment.required_recommendations[3] | Falls-prevention must 'while awaiting surgery' presumed the operation (plan C3, D4) | FIXED: 'while the neurosurgical assessment is pending' |
| C | minor | ground_truth.avoided_actions[3] | Stored exercise stress test (followup_outputs[3]) had no avoided label (plan C4, D5; class of notes dc2b866b, 89a27997) | FIXED: new avoid-waste-exercise-stress-test (waste, order_specialized_test test_type exercise_stress_test, [AHA_ACC_perioperative_2024]); stored follow-up kept |
| C | minor | ground_truth.avoided_actions[2].rationale | Echocardiogram waste rationale did not name the stored exercise echocardiogram (plan C4) | FIXED: clause on exercise stress echocardiography added, citation [AHA_ACC_perioperative_2024] added |
| C | minor | ground_truth.key_clinical_evidence[4] | 'a clear response supports shunting' overstated the tap test as deciding surgery (class of D1; only S06-S11 carry this sentence) | FIXED: 'supports considering a shunt' |
| B | minor | metadata.difficulty_rationale | Stale tier counts: post-tap reassessment counted as recommended though required (plan C12, D16) | FIXED: recounted (4 required, 1 recommended, 1 optional) |
| E | minor | metadata.revision_reason, metadata.last_revised | Revision metadata | FIXED: clinical description of this round's changes; 2026-11-17 |
| C | minor | ground_truth.action_criteria[1].rationale | Labs rationale said euthyroid status 'must be confirmed', contradicting the recommended tier the note asks to keep | FIXED: 'checking thyroid function is good practice before hypothyroidism is set aside as a contributor; it does not decide the iNPH diagnosis' |
| D | minor | followup_outputs[3], followup_outputs[4] | Same exercise test template as S07, S10, S11 (2.3 METs, 2 min 30 s) | FLAGGED: not changed |

## Changes
Per the physician's note, the must no longer asks to confirm euthyroid status: it is now 'Continue levothyroxine 75 mcg daily unchanged', and thyroid function testing stays a recommended action (its rationale says it is good practice, not decisive for iNPH). Assessment: the neurosurgical referral is now for a shunt eligibility assessment (the 35% tap response supports considering a shunt but does not decide surgery), with a new counselling must on the expected benefit and the shunt complications; the falls must applies while the neurosurgical assessment is pending. Policy: exercise stress testing is scored as waste and named in the echocardiogram waste rationale. The tap-test key evidence says a clear response supports considering a shunt. Metadata tier counts corrected. Outputs unchanged. Not an approved case. Checks: perfect_agent.py -v pass; test_case_guards pass; case_io check: no failure names this case.

## Verification
Pass 1: 0 errors found
Checked: note 49b4998b FIXED is right (must now 'Continue levothyroxine 75 mcg daily unchanged', labs stay recommended, not in the stop rule; the labs rationale no longer says 'must be confirmed'; the conditional hypothyroidism prohibition stays per D13); C1, C2, C3, C4 ('freezing on initiation' matches the exam), echo clause, C12 counts (4 required, 1 recommended, 1 optional); no leakage or em dashes in new text.
Cosmetic (not counted): none.
Checks after verification: perfect_agent.py -v pass (each required criterion served by the case's own data; S10 labs probe: all three alternatives served the stored CBC and BMP panels with creatinine 0.9, haemoglobin 13.4, platelets 208); test_case_guards -k NPH-S06..S11: 48 passed; case_io check: no failure names this case (the only NPH failure is test_guidance_claims on NPH-P08, maintained centrally).
Pass 2: 0 errors found
Nothing changed after Pass 1 (0 errors), so there was nothing unverified to re-check. Checks: perfect_agent.py -v pass; test_case_guards -k NPH-S06..S11: 48 passed.
Cosmetic (not counted): none.
