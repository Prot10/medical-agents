# NPH-P04
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress; no R2 notes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| ee99bd6b-c9bb-4b84-9c84-90006b259410 | NO-ACTION | Approval of `patient.chief_complaint` ("niente da segnalare"); unchanged (D15) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | `ground_truth.assessment.required_recommendations[0]` | Referral "for CSF shunting with a programmable valve" presumed surgery (class C1, D1) | FIXED: shunt eligibility assessment; the 18% tap response supports considering a shunt, programmable valve if one is placed, does not by itself decide surgery [Nakajima_2021] |
| C | major | `ground_truth.assessment.required_recommendations[1]` | Counselling said shunting "is expected to improve" and named no risk (class C2, D2, D3) | FIXED: canonical counselling must; gait most likely to improve, gait, falls and continence more likely than cognition or behaviour, degree uncertain, bvFTD keeps its own management; complications listed [Nakajima_2021] |
| C | minor | `ground_truth.assessment.required_recommendations[2]` | Goals-of-care must said "before surgery", presuming the operation (same class as C3, D4) | FIXED: "before the decision on surgery"; the must stays separate as the plan asks |
| C | minor | `ground_truth.assessment.required_recommendations[4]` | Falls must "while awaiting surgery" (class C3, D4) | FIXED: "while the neurosurgical assessment is pending" |
| C | minor | `ground_truth.avoided_actions` | Stored exercise stress test (freezing, walker) carried no waste label (class C4, D5) | FIXED: new `avoid-waste-exercise-stress-test`; echo waste rationale gains the exercise-echo clause; [AHA_ACC_perioperative_2024] |
| B | minor | `metadata.difficulty_rationale` | Tier counts stale: post-tap reassessment counted as recommended (class C12, D16) | FIXED: 4 required, 0 recommended, 2 optional |
| B | minor | `fallback_tool_outputs.specialized_test.quantitative_data.SDMT` | SDMT z = -2.3 contradicted the findings row (z = -2.2) of the same battery | FIXED: z = -2.2 |
| B | minor | `patient.neurological_exam.cranial_nerves` | "Full vertical and horizontal eye movements" contradicted "upgaze range mildly limited" in the same sentence | FIXED: "Full horizontal and downward eye movements with normal saccade velocity; upgaze range mildly limited for age" (the PSP differential, which rests on normal saccade velocity and no gaze palsy, stays true) |
| D | minor | `initial_tool_outputs.csf.interpretation`, `.special_tests` | The CSF report carries the post-tap TUG, 10-m walk and MoCA results, the evidence of the separate post-tap reassessment criterion (condition-wide October design) | FLAGGED (condition-wide) |
| D | minor | `initial_tool_outputs.clinical_assessment.scores` | Baseline gait report lists "MoCA (same session) 17/30", the optional cognitive screen's result | FLAGGED (minor) |

## Changes
The chief complaint was approved and is unchanged. The neurosurgical referral must now asks for a shunt eligibility assessment: the 18% tap response, the interval ventricular enlargement (Evans 0.27 to 0.35) and normal-pressure CSF support considering a shunt (with a programmable valve if one is placed) but do not by themselves decide surgery. The counselling must no longer says shunting "is expected to improve": gait is the symptom most likely to improve, gait, falls and continence more than cognition or behaviour, the degree is uncertain, bvFTD keeps its own management, and the shunt complications are listed (obstruction needing revision, infection, headache, subdural haematoma from over-drainage) [Nakajima_2021]. The goals-of-care must now reads "before the decision on surgery" and the falls must "while the neurosurgical assessment is pending". Exercise stress testing is labelled waste (no cardiac indication, treadmill unsafe with freezing and a walker) and the echocardiogram waste rationale names exercise stress echocardiography [AHA_ACC_perioperative_2024]. Two consistency fixes: the cranial-nerve exam now says "full horizontal and downward eye movements" (it said full vertical movements and limited upgaze in one sentence), and the fallback neuropsychology battery gives SDMT z = -2.2 in both places. The difficulty rationale counts 4 required and 2 optional actions.

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
