# NPH-P01

## Reviewer notes
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress; no R2 notes | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| d61c8272-d96c-4cb0-a377-607d928ca24f | NO-ACTION | Approval of patient.chief_complaint ('tutto ok'); nothing changed |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.assessment.required_recommendations[0] | Referral 'for CSF shunting with a programmable valve' presumed surgery (plan class C1, decision D1) | FIXED: 'shunt eligibility assessment', the tap response supports but does not decide surgery, programmable valve only if a shunt is placed [Nakajima_2021] |
| C | major | ground_truth.assessment.required_recommendations[1] | Counselling said shunting 'is expected to improve gait and continence', with no risks (class C2, D2, D3) | FIXED: gait and continence more likely to improve than cognition, AD keeps its own treatment, uncertain degree, complications of shunting [Nakajima_2021], goals of surgery agreed before any operation |
| C | minor | ground_truth.assessment.required_recommendations[3] | Falls must 'while awaiting surgery' presumed the operation (class C3, D4) | FIXED: 'while the neurosurgical assessment is pending' |
| B | minor | ground_truth.key_clinical_evidence[4] | 'neurosurgical referral for a programmable-valve shunt' presumed surgery (same class as D1) | FIXED: referral for shunt eligibility assessment with counselling on the mainly motor and continence benefit and the risks |
| C | minor | ground_truth.avoided_actions[3] (new avoid-waste-exercise-stress-test) | The stored exercise stress test was served with no low-yield label (class C4, D5) | FIXED: waste entry for order_specialized_test exercise_stress_test, no cardiac indication, treadmill unsafe with this gait [AHA_ACC_perioperative_2024]; stored follow-up kept |
| C | minor | ground_truth.avoided_actions[2] (avoid-waste-3-order-echocardiogram) | Echo waste rationale did not name the stored exercise echocardiogram (class C4) | FIXED: clause on exercise stress echocardiography and citation added |
| B | minor | ground_truth.sequence_constraints[1].citations | Baseline-gait-before-tap constraint cited [Relkin_2005] while its reason cites [Nakajima_2021] (found only in M07, M08, M09, M10, P01; the other 25 NPH cases already cite Nakajima) | FIXED: citations [Nakajima_2021] |
| B | minor | metadata.difficulty_rationale | Tier counts stale: the post-tap reassessment counted as recommended although required (class C12, D16) | FIXED: recounted from action_criteria |

## Changes
Not approved before this round. The only note approves the chief complaint, which is unchanged. Class changes: the referral (must 1) is for shunt eligibility assessment on the 19% tap response, the enlarging ventricles with mild DESH and normal-pressure CSF (the tap supports but does not decide surgery; programmable valve if a shunt is placed); the counselling must (must 2) now says gait and continence are more likely to improve than cognition, that Alzheimer's disease keeps its own treatment, that the degree of improvement is uncertain, names the complications of shunting [Nakajima_2021] and keeps agreeing the goals of surgery before any operation; key evidence 5 matches; the falls must no longer presumes surgery; the stored exercise stress test is labelled waste and the echocardiography waste entry names exercise echocardiography [AHA_ACC_perioperative_2024]; the baseline-gait constraint cites Nakajima; the difficulty rationale gives the correct tier counts (4 required, 1 recommended, 2 optional). Diagnosis, tiers and tool outputs unchanged.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by stored pathway data; evidence numbers of every criterion alternative found in the served report by probe); exercise stress test and exercise echo calls match only their waste entries and no criterion; test_case_guards -k for the six cases: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases. No MRI touched.
Pass 1: 0 errors found
Checked: C1, C2 (cognition limit, AD treatment, goals of surgery kept), C3, C4, C12 correct.
Cosmetic (not counted): avoid-waste-exercise-stress-test rationale read "for which he needs a walker and stops submaximal and non-diagnostic" (garbled, and the stored report says the treadmill was not performed): now "for which he needs a walker, so the test cannot be completed and is non-diagnostic".
Re-checked after the pass-1 edits: perfect_agent.py -v pass (6/6, every criterion alternative served the report carrying its expected-evidence numbers, probed); test_case_guards -k for the six cases 48 passed; case_io.py check: schema and synonym guard OK, the only failures naming NPH are test_guidance_claims (NPH-P08 lumbar drain, central).
Pass 2: 0 errors found
Checked the pass-1 cosmetic rewording of avoid-waste-exercise-stress-test: it now agrees with the stored exercise stress test report (treadmill not performed, non-diagnostic) and the gait described in the exam. No edits. Re-checked: perfect_agent.py -v pass; test_case_guards -k for the six cases 48 passed.
