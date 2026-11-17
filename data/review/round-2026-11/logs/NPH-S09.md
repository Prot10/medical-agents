# NPH-S09

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 03abb2d3-2b2a-4b22-b362-e2f9085b5d5b | NO-ACTION | Approval of the chief complaint; it is unchanged. (patient.chief_complaint) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.assessment.required_recommendations[0] | Referral must said 'Refer to neurosurgery for CSF shunting with a programmable valve', presuming surgery (plan C1, D1; class of notes 7f90233f, 8bb5643e, 2cd1748b, 6abe35f0) | FIXED: now 'shunt eligibility assessment ... the tap response supports considering a shunt, with a programmable valve if one is placed, but does not by itself decide surgery [Nakajima_2021]' |
| C | major | ground_truth.assessment.required_recommendations[1] | No must on counselling about the expected benefit and the complications of shunting (plan C2, D2) | FIXED: new counselling must (gait most likely to improve, degree uncertain; shunt obstruction needing revision, infection, headache, subdural haematoma from over-drainage [Nakajima_2021]) |
| C | minor | ground_truth.assessment.required_recommendations[3] | Falls-prevention must 'while awaiting surgery' presumed the operation (plan C3, D4) | FIXED: 'while the neurosurgical assessment is pending' |
| C | minor | ground_truth.avoided_actions[3] | Stored exercise stress test (followup_outputs[3]) had no avoided label (plan C4, D5; class of notes dc2b866b, 89a27997) | FIXED: new avoid-waste-exercise-stress-test (waste, order_specialized_test test_type exercise_stress_test, [AHA_ACC_perioperative_2024]); stored follow-up kept |
| C | minor | ground_truth.avoided_actions[2].rationale | Echocardiogram waste rationale did not name the stored exercise echocardiogram (plan C4) | FIXED: clause on exercise stress echocardiography added, citation [AHA_ACC_perioperative_2024] added |
| C | minor | ground_truth.key_clinical_evidence[5] | 'a clear response supports shunting' overstated the tap test as deciding surgery (class of D1; only S06-S11 carry this sentence) | FIXED: 'supports considering a shunt' |
| B | minor | metadata.difficulty_rationale | Stale tier counts: post-tap reassessment counted as recommended though required (plan C12, D16) | FIXED: recounted (4 required, 0 recommended, 2 optional) |
| E | minor | metadata.revision_reason, metadata.last_revised | Revision metadata | FIXED: clinical description of this round's changes; 2026-11-17 |
| B | minor | initial_tool_outputs.labs.panels | Checked eGFR 70 (CKD-EPI 2021, creatinine 1.1, 75-year-old man) and CSF/serum glucose 70/138 = 0.51: consistent | no change |

## Changes
Assessment: the neurosurgical referral is now for a shunt eligibility assessment (the 35% tap response supports considering a shunt, with a programmable valve if one is placed, but does not decide surgery), and a new must requires counselling on the expected benefit (gait most likely to improve, degree uncertain) and the shunt complications (obstruction needing revision, infection, headache, subdural haematoma from over-drainage). The falls must now applies while the neurosurgical assessment is pending. Policy: an exercise stress test is now scored as waste, and the echocardiogram waste rationale names exercise stress echocardiography. The tap-test key evidence says a clear response supports considering a shunt. Metadata tier counts corrected. The insulin-supervision must, criteria, outputs and the approved chief complaint are unchanged. Not an approved case. Checks: perfect_agent.py -v pass; test_case_guards pass; case_io check: no failure names this case.

## Verification
Pass 1: 0 errors found
Checked: approval note ruling NO-ACTION is right; C1, C2, C3, C4 ('freezing on initiation' matches the exam), echo clause, C12 counts (4 required, 2 optional), key-evidence rewording; insulin-supervision must unchanged; no leakage or em dashes in new text.
Cosmetic (not counted): none.
Checks after verification: perfect_agent.py -v pass (each required criterion served by the case's own data; S10 labs probe: all three alternatives served the stored CBC and BMP panels with creatinine 0.9, haemoglobin 13.4, platelets 208); test_case_guards -k NPH-S06..S11: 48 passed; case_io check: no failure names this case (the only NPH failure is test_guidance_claims on NPH-P08, maintained centrally).
Pass 2: 0 errors found
Nothing changed after Pass 1 (0 errors), so there was nothing unverified to re-check. Checks: perfect_agent.py -v pass; test_case_guards -k NPH-S06..S11: 48 passed.
Cosmetic (not counted): none.
Condition audit, 17 Nov 2026 (B consistency, minor, FIXED): the rationale of avoid-waste-exercise-stress-test (ground_truth.avoided_actions[3]) said treadmill exercise "stops submaximal and non-diagnostic", while the stored exercise stress test and exercise echo of this case report that the exercise was not performed because the patient could not walk safely on a treadmill. The clause now reads "cannot be completed, so the test is non-diagnostic" (the wording NPH-M05 already used). Severity, alternative and citation unchanged. perfect_agent.py: pass; case_io.py check: schema and synonym guard OK, the only failures naming NPH are the test_guidance_claims rows (central).
Pass 3: 0 errors found
Checked the condition-audit edit of ground_truth.avoided_actions[3] (avoid-waste-exercise-stress-test, order_specialized_test test_type exercise_stress_test, severity waste): the rationale now says the treadmill test "cannot be completed, so the test is non-diagnostic", which matches the stored exercise stress test and exercise echo follow-ups (exercise not performed, unable to walk safely on a treadmill; resting data only; non-diagnostic for inducible ischaemia). The gait description in the rationale matches the one in those reports. Severity, alternative and citation are unchanged. perfect_agent.py -v pass; test_case_guards -k (8 NPH cases) 64 passed. Nothing changed.
