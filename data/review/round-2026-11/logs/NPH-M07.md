# NPH-M07

## Reviewer notes
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress; no R2 notes | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| f9899f54-b8ea-4c43-a466-72bf9a41157c | NO-ACTION | Approval of patient.chief_complaint ('tutto ok'); nothing changed |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.assessment.required_recommendations[0] | Referral 'for CSF shunting with a programmable valve' presumed surgery (plan class C1, decision D1) | FIXED: 'shunt eligibility assessment', the tap response supports but does not decide surgery, programmable valve only if a shunt is placed [Nakajima_2021] |
| C | major | ground_truth.assessment.required_recommendations[2] | Counselling said shunting 'is expected to improve' the gait, with no risks (class C2, D2, D3) | FIXED: benefit (gait more likely to improve than the neuropathic and stenotic weakness and sensory loss), uncertainty, and complications of shunting [Nakajima_2021] |
| B | minor | ground_truth.key_clinical_evidence[4] | 'neurosurgical referral for a shunt with a programmable valve' presumed surgery (same class as D1) | FIXED: referral for shunt eligibility assessment with counselling on benefit and risks |
| C | minor | ground_truth.avoided_actions[3] (new avoid-waste-exercise-stress-test) | The stored exercise stress test was served with no low-yield label (class C4, D5) | FIXED: waste entry for order_specialized_test exercise_stress_test, no cardiac indication, treadmill unsafe with this gait [AHA_ACC_perioperative_2024]; stored follow-up kept |
| C | minor | ground_truth.avoided_actions[2] (avoid-waste-3-order-echocardiogram) | Echo waste rationale did not name the stored exercise echocardiogram (class C4) | FIXED: clause on exercise stress echocardiography and citation added |
| B | minor | ground_truth.sequence_constraints[1].citations | Baseline-gait-before-tap constraint cited [Relkin_2005] while its reason cites [Nakajima_2021] (found only in M07, M08, M09, M10, P01; the other 25 NPH cases already cite Nakajima) | FIXED: citations [Nakajima_2021] |
| B | minor | metadata.difficulty_rationale | Tier counts stale: the post-tap reassessment counted as recommended although required (class C12, D16) | FIXED: recounted from action_criteria |
| B | minor | followup_outputs (exercise stress test and exercise echo) | The stored treadmill reports say the test stopped for 'freezing on the moving belt' (text shared across NPH cases) while the exam describes no freezing; plausible on a treadmill, not contradictory | FLAGGED (stored follow-ups kept per plan C4) |
| C | minor | ground_truth.assessment.required_recommendations | No falls must exists, so class C3 does not apply; the B12 must stays (D13) | NO-ACTION |
| B | minor | metadata.revision_reason | Claimed 'the falls must no longer presumes surgery', but the case has no falls must (C3 does not apply) | FIXED in verification pass 1: clause removed |

## Changes
Not approved before this round. The only note approves the chief complaint, which is unchanged. Class changes: the neurosurgical referral (must 1) is now for shunt eligibility assessment, saying that the 20% tap response supports but does not decide surgery and that a programmable valve is used if a shunt is placed; the counselling must (must 3) now gives the expected benefit (gait more likely to improve than the proximal weakness and distal sensory loss from neuropathy and lumbar stenosis), the uncertainty of the degree and the complications of shunting (obstruction needing revision, infection, headache, subdural haematoma from over-drainage) [Nakajima_2021]; key evidence 5 matches the referral wording. The stored exercise stress test is now labelled waste and the echocardiography waste entry names exercise echocardiography [AHA_ACC_perioperative_2024]. The baseline-gait constraint now cites the guideline its reason names, and the difficulty rationale gives the correct tier counts (4 required, 1 recommended, 2 optional). Diagnosis, work-up tiers, tool outputs and the B12 must are unchanged.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by stored pathway data; evidence numbers of every criterion alternative found in the served report by probe); exercise stress test and exercise echo calls match only their waste entries and no criterion; test_case_guards -k for the six cases: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases. No MRI touched.
Pass 1: 1 errors found
- metadata.revision_reason said "the falls must no longer presumes surgery", but M07 has no falls must (plan C3 excludes it): factual error in physician-visible metadata. FIXED: clause removed.
Cosmetic (not counted): avoid-waste-3-order-echocardiogram rationale had a double "and" ("..., and the MRI shows no infarct, and exercise ..."): now "... exists and the MRI shows no infarct; exercise ...".
Re-checked after the pass-1 edits: perfect_agent.py -v pass (6/6, every criterion alternative served the report carrying its expected-evidence numbers, probed); test_case_guards -k for the six cases 48 passed; case_io.py check: schema and synonym guard OK, the only failures naming NPH are test_guidance_claims (NPH-P08 lumbar drain, central).
Pass 2: 0 errors found
Checked the pass-1 changes: metadata.revision_reason no longer claims a falls must (case has none; the remaining clauses match the referral, counselling, waste and tier changes); avoid-waste-3-order-echocardiogram reworded rationale is correct (MRI reports no restricted diffusion and only Fazekas 2 white matter change, no infarct). No edits. Re-checked: perfect_agent.py -v pass; test_case_guards -k for the six cases 48 passed.
Cosmetic (not counted): avoid-waste-exercise-stress-test rationale still reads "... impaired postural reflexes and stops submaximal and non-diagnostic" (untouched text, meaning clear).
Condition audit, 17 Nov 2026 (B consistency, minor, FIXED): the stored treadmill reports said the test stopped "for gait unsteadiness with freezing on the moving belt", but her exam and history describe a short-stepped, shuffling gait with no freezing or start hesitation (text shared with other NPH cases). Changed to "for gait unsteadiness on the moving belt" in followup_outputs[4].output.findings[0].result, followup_outputs[4].output.impression (exercise stress test), followup_outputs[5].output.findings[0] and followup_outputs[5].output.impression (exercise echo). Both stay waste-labelled; nothing else changed. perfect_agent.py: pass; case_io.py check: schema and synonym guard OK, the only failures naming NPH are the test_guidance_claims rows (central).
Pass 3: 0 errors found
Checked the condition-audit edit (removed "with freezing" from the treadmill stop reason) in followup_outputs[4] (exercise stress test: findings[0].result, impression) and followup_outputs[5] (exercise echo: findings[0], impression): correct, because the exam gait is short-stepped, wide-based and shuffling with no freezing; no "freez" is left anywhere in the case; the avoid-waste-exercise-stress-test rationale ("stops submaximal and non-diagnostic") agrees with these stored reports, which describe a test performed and stopped at 2.3 METs. Both entries stay waste-labelled. perfect_agent.py -v pass; test_case_guards -k (8 NPH cases) 64 passed. Nothing changed.
