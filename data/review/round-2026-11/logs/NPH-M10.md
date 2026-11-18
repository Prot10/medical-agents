# NPH-M10

## Reviewer notes
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress; no R2 notes | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 8c33ff13-943f-40c6-bbea-5205b6ef2695 | NO-ACTION | Approval of patient.chief_complaint ('tutto ok'); nothing changed |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.assessment.required_recommendations[0] | Referral 'for CSF shunting with a programmable valve' presumed surgery (plan class C1, decision D1) | FIXED: 'shunt eligibility assessment', the tap response supports but does not decide surgery, programmable valve only if a shunt is placed [Nakajima_2021] |
| C | major | ground_truth.assessment.required_recommendations[1] (new) | No must counselled on the benefit and the risks of shunting (class C2, D2) | FIXED: new counselling must (gait most likely to improve; the shunt does not treat the lumbar stenosis, so claudicant or radicular symptoms from it, should they develop, are not expected to change; uncertain degree; complications) [Nakajima_2021]. He denies claudicant and radicular symptoms, so the plan's limit clause is phrased conditionally (wording corrected in verification pass 1) |
| C | minor | ground_truth.assessment.required_recommendations[3] | Falls must 'while awaiting surgery' presumed the operation (class C3, D4) | FIXED: 'while the neurosurgical assessment is pending' |
| C | minor | ground_truth.avoided_actions[3] (new avoid-waste-exercise-stress-test) | The stored exercise stress test was served with no low-yield label (class C4, D5) | FIXED: waste entry for order_specialized_test exercise_stress_test, no cardiac indication, treadmill unsafe with this gait [AHA_ACC_perioperative_2024]; stored follow-up kept |
| C | minor | ground_truth.avoided_actions[2] (avoid-waste-3-order-echocardiogram) | Echo waste rationale did not name the stored exercise echocardiogram (class C4) | FIXED: clause on exercise stress echocardiography and citation added |
| B | minor | ground_truth.sequence_constraints[1].citations | Baseline-gait-before-tap constraint cited [Relkin_2005] while its reason cites [Nakajima_2021] (found only in M07, M08, M09, M10, P01; the other 25 NPH cases already cite Nakajima) | FIXED: citations [Nakajima_2021] |
| B | minor | metadata.difficulty_rationale | Tier counts stale: the post-tap reassessment counted as recommended although required (class C12, D16) | FIXED: recounted from action_criteria |
| B | minor | followup_outputs (exercise stress test and exercise echo) | The stored treadmill reports say the test stopped for 'freezing on the moving belt' (text shared across NPH cases) while the exam describes no freezing; plausible on a treadmill, not contradictory | FLAGGED (stored follow-ups kept per plan C4) |

## Changes
Not approved before this round. The only note approves the chief complaint, which is unchanged. Class changes: the referral (must 1) is for shunt eligibility assessment on the 32% tap response, the DESH MRI and normal-pressure CSF (the tap supports but does not decide surgery; programmable valve if a shunt is placed), keeping the instruction to revisit the deferred lumbar decompression only after the shunt response; a new counselling must (must 2) gives the expected benefit (gait most likely to improve; the shunt does not treat the lumbar stenosis), the uncertainty and the complications of shunting [Nakajima_2021]; the falls must no longer presumes surgery; the stored exercise stress test is labelled waste and the echocardiography waste entry names exercise echocardiography [AHA_ACC_perioperative_2024]; the baseline-gait constraint cites Nakajima; the difficulty rationale gives the correct tier counts (4 required, 3 optional). Diagnosis, tiers, the aspirin must and tool outputs unchanged.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by stored pathway data; evidence numbers of every criterion alternative found in the served report by probe); exercise stress test and exercise echo calls match only their waste entries and no criterion; test_case_guards -k for the six cases: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases. No MRI touched.
Pass 1: 1 errors found
- ground_truth.assessment.required_recommendations[1] (new counselling must) said "the lumbar stenosis, whose claudicant or radicular symptoms are not expected to change", presupposing symptoms the HPI explicitly denies ("has not noticed leg weakness, pain radiating down the leg, or pain that worsens with standing"): internal contradiction. FIXED: "the shunt does not treat the lumbar stenosis, so claudicant or radicular symptoms from it, should they develop, are not expected to change"; own-findings row updated.
Cosmetic (not counted): none.
Re-checked after the pass-1 edits: perfect_agent.py -v pass (6/6, every criterion alternative served the report carrying its expected-evidence numbers, probed); test_case_guards -k for the six cases 48 passed; case_io.py check: schema and synonym guard OK, the only failures naming NPH are test_guidance_claims (NPH-P08 lumbar drain, central).
Pass 2: 0 errors found
Checked the pass-1 fix of required_recommendations[1]: the counselling must now says the shunt does not treat the lumbar stenosis and that claudicant or radicular symptoms, should they develop, are not expected to change; consistent with the HPI (no leg weakness, radicular pain or standing-worsened pain), the differential (no claudicant pattern) and must 1 (deferred decompression revisited after the shunt response). Benefit, uncertainty and complications per plan C2 [Nakajima_2021]. No edits. Re-checked: perfect_agent.py -v pass; test_case_guards -k for the six cases 48 passed.
