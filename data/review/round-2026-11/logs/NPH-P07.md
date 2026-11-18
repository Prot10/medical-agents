# NPH-P07
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress; no R2 notes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 1af93709-617c-4d8c-bb04-8ccdcd99d487 | FIXED | `ground_truth.assessment.prohibited_recommendations[1]`: D12 text (slowed vertical saccades can support PSP [Hoglinger_2017]; here mild, upward only, normal downward saccades, full range, forward falls, midbrain-to-pons ratio 0.55 [Massey_2013], DESH and 32% tap response support iNPH); class within the case: `ground_truth.red_herrings[0].correct_interpretation` reworded ("mild, nonspecific upward-saccade slowing ... PSP is less likely"). Unchanged, no such implication: `differential[0]` (PSP, low) and `red_herrings[1]` |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | `ground_truth.assessment.required_recommendations[0]` | Referral "for CSF shunting with a programmable valve" presumed surgery (class C1, D1) | FIXED: shunt eligibility assessment; the 32% tap response supports considering a shunt, programmable valve if placed, does not by itself decide surgery [Nakajima_2021] |
| C | major | `ground_truth.assessment.required_recommendations[1]` (new) | No must on benefit, uncertainty or shunt complications (class C2, D2) | FIXED: canonical counselling must added after the referral (no limit clause) [Nakajima_2021] |
| C | minor | `ground_truth.assessment.required_recommendations[2]` | Falls must "while awaiting surgery" (class C3, D4) | FIXED: "while the neurosurgical assessment is pending" |
| C | minor | `ground_truth.avoided_actions` | Stored exercise stress test (prominent freezing, no cardiac indication) carried no waste label (class C4, D5) | FIXED: new `avoid-waste-exercise-stress-test`; echo waste rationale gains the exercise-echo clause; [AHA_ACC_perioperative_2024] |
| C | minor | `initial_tool_outputs.labs.panels["Tumour markers"][0].clinical_significance` | PSA 4.2 ng/mL (flagged high) had no interpretation, although he takes finasteride 5 mg, which lowers PSA by about half, and is on prostate cancer active surveillance | FIXED: factual interpretation (finasteride-adjusted value about 8.4 ng/mL, relevant to active surveillance). No must added: labs are optional, so a must would depend on a study no required criterion orders |
| B | minor | `metadata.difficulty_rationale` | Tier counts stale (class C12, D16) | FIXED: 4 required, 0 recommended, 2 optional |
| D | minor | `initial_tool_outputs.csf.interpretation`, `.special_tests` | The CSF report carries the post-tap gait results, the evidence of the separate post-tap reassessment criterion (condition-wide October design) | FLAGGED (condition-wide) |

## Changes
The PSP prohibition no longer implies that PSP requires a vertical supranuclear gaze palsy or midbrain atrophy: it now says slowed vertical saccades can support PSP [Hoglinger_2017], and that here the slowing is mild, upward only, with normal downward saccades and full range, the falls are forward, the midbrain-to-pons ratio is 0.55 [Massey_2013], and the DESH MRI and the 32% tap response support iNPH. The first red herring now says PSP is less likely because the eye finding is nonspecific. The referral must asks for a shunt eligibility assessment and says the tap response supports considering a shunt but does not by itself decide surgery; a new counselling must covers the uncertain benefit and the shunt complications [Nakajima_2021]; the falls must reads "while the neurosurgical assessment is pending". Exercise stress testing is labelled waste and the echocardiogram waste rationale names exercise stress echocardiography [AHA_ACC_perioperative_2024]. The PSA row now notes that finasteride halves PSA (adjusted value about 8.4 ng/mL), which matters for his active surveillance. The difficulty rationale counts 4 required and 2 optional actions.

## Verification
17 Nov 2026: perfect_agent.py -v passes (every required and recommended criterion served by the case's own report carrying its evidence); test_case_guards for NPH-P03..P08 48 passed; case_io.py check: schema and synonym guard OK, no failure naming the case apart from the central test_guidance_claims.
Pass 1: 0 errors found
- Checked every note ruling against the plan and the note, the diff against 06b74446, the final policy (criteria, tiers, stop rule, sequence ids, musts vs prohibitions vs avoided actions, differential vs evidence), the stored exercise-test reports against the medications and gait, and the tier counts in metadata; perfect_agent.py -v and test_case_guards -k pass; no material error found.
Cosmetic (not counted): added the missing "Reviewer status" header line to the log.
Pass 2: 0 errors found
- Nothing changed after Pass 1 (0 errors), so no unverified change to re-check. Re-ran perfect_agent.py -v (pass) and test_case_guards -k for NPH-P03..P08 (48 passed). No edits.
Condition audit, 17 Nov 2026 (B consistency, minor, FIXED): the rationale of avoid-waste-exercise-stress-test (ground_truth.avoided_actions[3]) said treadmill exercise "stops submaximal and non-diagnostic", while the stored exercise stress test and exercise echo of this case report that the exercise was not performed because the patient could not walk safely on a treadmill. The clause now reads "cannot be completed, so the test is non-diagnostic" (the wording NPH-M05 already used). Severity, alternative and citation unchanged. perfect_agent.py: pass; case_io.py check: schema and synonym guard OK, the only failures naming NPH are the test_guidance_claims rows (central).
Pass 3: 0 errors found
Checked the condition-audit edit of ground_truth.avoided_actions[3] (avoid-waste-exercise-stress-test, order_specialized_test test_type exercise_stress_test, severity waste): the rationale now says the treadmill test "cannot be completed, so the test is non-diagnostic", which matches the stored exercise stress test and exercise echo follow-ups (exercise not performed, unable to walk safely on a treadmill; resting data only; non-diagnostic for inducible ischaemia). The gait description in the rationale matches the one in those reports. Severity, alternative and citation are unchanged. perfect_agent.py -v pass; test_case_guards -k (8 NPH cases) 64 passed. Nothing changed.
