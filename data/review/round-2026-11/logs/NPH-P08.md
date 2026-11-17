# NPH-P08
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress; no R2 notes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 6eedd7f8-b3b7-4765-a83b-507525828a4d | FIXED | `ground_truth.action_criteria[6]` (action-extended-lumbar-drainage): importance required -> recommended; soft sequence constraint (drainage after the tap) kept (D11) |
| 9ea36124-a383-4f2a-824d-e20ccfb5625b | FIXED | `ground_truth.stop_rule.required_before_assessment`: action-extended-lumbar-drainage removed; `ground_truth.assessment.required_recommendations[1]`: referral for shunt eligibility assessment on the syndrome, DESH MRI and normal-pressure CSF, with the drainage response only if drainage was performed; a negative single tap does not preclude referral (D11, D1) |
| ff859687-b531-41b4-9962-05b271c739bb | FIXED | `ground_truth.assessment.required_recommendations[0]`: "proceed to extended lumbar drainage" -> "consider extended lumbar drainage ... or another appropriate specialist assessment" with the sensitivities [Marmarou_2005]; class within the case: `ground_truth.red_herrings[0].correct_interpretation` "extended lumbar drainage is the next test" -> "extended drainage or another specialist assessment can be considered" |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | `ground_truth.assessment.required_recommendations[1]` | Referral "for CSF shunting with a programmable valve" presumed surgery and rested only on the drainage response (class C1, D1) | FIXED (with note 9ea36124): shunt eligibility assessment, programmable valve if placed, the evidence does not by itself decide surgery [Nakajima_2021] |
| C | major | `ground_truth.assessment.required_recommendations[2]` (new) | No must on benefit, uncertainty or shunt complications (class C2, D2) | FIXED: canonical counselling must added after the referral (no limit clause) [Nakajima_2021] |
| C | minor | `ground_truth.assessment.required_recommendations[3]` | Falls must "while awaiting surgery" (class C3, D4) | FIXED: "while the neurosurgical assessment is pending" |
| C | minor | `ground_truth.avoided_actions` | Stored exercise stress test (doorway freezing, no cardiac indication) carried no waste label (class C4, D5) | FIXED: new `avoid-waste-exercise-stress-test`; echo waste rationale gains the exercise-echo clause; [AHA_ACC_perioperative_2024] |
| B | minor | `metadata.difficulty_rationale` | Tier counts stale: post-tap reassessment counted recommended (class C12, D16) | FIXED: 4 required, 1 recommended (drainage), 2 optional |
| D | minor | `initial_tool_outputs.csf.interpretation`, `.special_tests` | The CSF report carries the post-tap gait results, the evidence of the separate post-tap reassessment criterion (condition-wide October design) | FLAGGED (condition-wide) |
| C | minor | `followup_outputs[6]` (TEE), `followup_outputs[7]` (bubble study) | Invasive or cardioembolic echo studies with no indication are stored; they are covered by the echo waste wildcard, not credited | FLAGGED (no change: already waste-labelled; TEE could arguably be harm, no note raised it) |
| A | minor | `agent-platform/config/review/condition_tool_guidance.yaml` (NPH, perform_clinical_assessment / lumbar drain) | `test_guidance_claims` now fails on "lumbar drain required in P08": the guidance text must say recommended | CENTRAL (plan C-GUIDE; test maintained centrally) |

## Changes
Following the reviewer, extended lumbar drainage after the negative 45 mL tap is no longer mandatory: it is a recommended step (still expected to follow the tap) and has left the stop rule. The first must now says that after a single tap without objective improvement, extended lumbar drainage (about 10 mL/hour, 300 to 500 mL over 72 hours, with daily timed gait measures) or another appropriate specialist assessment should be considered, because a negative tap does not exclude shunt-responsive iNPH (tap sensitivity 26% to 61%, drainage 50% to 100%) [Marmarou_2005]; the first red herring says the same. The referral must asks for a neurosurgical shunt eligibility assessment on the full syndrome, the DESH MRI and normal-pressure CSF, together with the drainage response (TUG 31 to 19 s, 39%) if drainage was done, and says the evidence supports considering a shunt but does not by itself decide surgery. A new counselling must covers the uncertain benefit and the shunt complications [Nakajima_2021]; the falls must reads "while the neurosurgical assessment is pending". Exercise stress testing is labelled waste and the echocardiogram waste rationale names exercise stress echocardiography [AHA_ACC_perioperative_2024]. The difficulty rationale counts 4 required, 1 recommended and 2 optional actions.

## Verification
17 Nov 2026: perfect_agent.py -v passes (every required and recommended criterion served by the case's own report carrying its evidence); test_case_guards for NPH-P03..P08 48 passed; case_io.py check: schema and synonym guard OK, no failure naming the case apart from the central test_guidance_claims. The only suite failure is test_guidance_claims (central, C-GUIDE).
Pass 1: 0 errors found
- Checked every note ruling against the plan and the note, the diff against 06b74446, the final policy (criteria, tiers, stop rule, sequence ids, musts vs prohibitions vs avoided actions, differential vs evidence), the stored exercise-test reports against the medications and gait, and the tier counts in metadata; perfect_agent.py -v and test_case_guards -k pass; no material error found.
Cosmetic (not counted): added the missing "Reviewer status" header line to the log.
Pass 2: 0 errors found
- Nothing changed after Pass 1 (0 errors), so no unverified change to re-check. Re-ran perfect_agent.py -v (pass) and test_case_guards -k for NPH-P03..P08 (48 passed). No edits.
