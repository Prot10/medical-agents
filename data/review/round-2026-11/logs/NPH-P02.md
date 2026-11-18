# NPH-P02

## Reviewer notes
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress; no R2 notes | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| ccbaf98b-801f-4d0e-9672-116469836f25 | NO-ACTION | Approval of patient.chief_complaint ('bene così'); nothing changed |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.assessment.required_recommendations[0] | Referral 'for CSF shunting with a programmable valve' presumed surgery (plan class C1, decision D1) | FIXED: 'shunt eligibility assessment', the tap response supports but does not decide surgery, programmable valve only if a shunt is placed [Nakajima_2021] |
| C | major | ground_truth.assessment.required_recommendations[1] | Counselling said shunting 'is expected to improve' the gait and incontinence, with no risks (class C2, D2, D3) | FIXED: magnetic gait and urge incontinence more likely to improve than bradykinesia, rigidity and tremor, PD keeps its own treatment, uncertain degree, complications of shunting [Nakajima_2021] |
| C | minor | ground_truth.assessment.required_recommendations[4] | Falls must 'while awaiting surgery' presumed the operation (class C3, D4) | FIXED: 'while the neurosurgical assessment is pending' |
| C | minor | ground_truth.avoided_actions[3] (new avoid-waste-exercise-stress-test) | The stored exercise stress test was served with no low-yield label (class C4, D5) | FIXED: waste entry for order_specialized_test exercise_stress_test, no cardiac indication, treadmill unsafe with this gait [AHA_ACC_perioperative_2024]; stored follow-up kept |
| C | minor | ground_truth.avoided_actions[2] (avoid-waste-3-order-echocardiogram) | Echo waste rationale did not name the stored exercise echocardiogram (class C4) | FIXED: clause on exercise stress echocardiography and citation added |
| B | minor | metadata.difficulty_rationale | Tier counts stale: the post-tap reassessment counted as recommended although required (class C12, D16) | FIXED: recounted from action_criteria |
| B | minor | ground_truth.sequence_constraints[1].citations | Already cites [Nakajima_2021] | NO-ACTION |

## Changes
Not approved before this round. The only note approves the chief complaint, which is unchanged. Class changes: the referral (must 1) is for shunt eligibility assessment on the 21% tap response in the ON state, the enlarging ventricles and normal-pressure CSF (the tap supports but does not decide surgery; programmable valve if a shunt is placed); the counselling must (must 2) now says the wide-based magnetic gait and urge incontinence are more likely to improve than the bradykinesia, rigidity and tremor, that Parkinson's disease keeps its own treatment, that the degree of improvement is uncertain, and names the complications of shunting [Nakajima_2021]; the falls must no longer presumes surgery; the stored exercise stress test is labelled waste and the echocardiography waste entry names exercise echocardiography [AHA_ACC_perioperative_2024]; the difficulty rationale gives the correct tier counts (4 required, 2 optional). Diagnosis, tiers, the levodopa and pramipexole musts and tool outputs unchanged.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by stored pathway data; evidence numbers of every criterion alternative found in the served report by probe); exercise stress test and exercise echo calls match only their waste entries and no criterion; test_case_guards -k for the six cases: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases. No MRI touched.
Pass 1: 0 errors found
Checked: C1, C2 (PD limit), C3, C4 (freezing in the exam), C12 correct; levodopa and pramipexole musts unchanged.
Cosmetic (not counted): none.
Re-checked after the pass-1 edits: perfect_agent.py -v pass (6/6, every criterion alternative served the report carrying its expected-evidence numbers, probed); test_case_guards -k for the six cases 48 passed; case_io.py check: schema and synonym guard OK, the only failures naming NPH are test_guidance_claims (NPH-P08 lumbar drain, central).
Pass 2: 0 errors found
Nothing changed after the clean pass 1 (no condition-audit or orchestrator entries); checks only. Re-checked: perfect_agent.py -v pass; test_case_guards -k for the six cases 48 passed.
Pass 3: 0 errors found
Nothing changed after the clean pass 1 (no condition-audit or orchestrator entries), so there was nothing to verify; checks only: perfect_agent.py -v pass; test_case_guards -k (8 NPH cases) 64 passed. Nothing changed.
