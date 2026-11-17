# NPH-M04
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress, R2 (NB-87MF-FBTV-TPWE) no notes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 2cd1748b-b135-4197-9b61-1543654686af | FIXED | ground_truth.assessment.required_recommendations[0] reworded to 'Refer to neurosurgery for shunt eligibility assessment ...; ... does not by itself decide surgery [Nakajima_2021]'; new required_recommendations[1]: individual counselling before the decision on surgery on benefit (gait most likely, degree uncertain) and surgical risks and complications (obstruction needing revision, infection, headache, subdural haematoma from over-drainage) [Nakajima_2021]. The gabapentin must stays |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C clinical | major | ground_truth.assessment.required_recommendations (falls must) | 'while awaiting surgery' presumed the operation that the referral no longer decides (plan class C3) | FIXED: 'while the neurosurgical assessment is pending' |
| B consistency | minor | metadata.difficulty_rationale | Tier counts stale: the post-tap reassessment was counted as recommended though required since October (plan class C12) | FIXED: recounted from action_criteria |
| E language | minor | metadata.revision_reason, metadata.last_revised | Described the October changes only | FIXED: clinical description of the November changes, 2026-11-17 |
| D leakage | minor | followup_outputs (exercise stress test, exercise echo) | Waste-labelled stress-test reports share template wording across the condition ('modified Naughton ... stopped at 2 min 30 s ... 2.3 METs ... freezing on the moving belt'); harmless because the agent sees only its own case and the tests are waste, but it is copied text | FLAGGED (lead: condition-wide, not changed here) |
| B consistency | minor | initial_tool_outputs.csf.interpretation / special_tests | The tap-test CSF report also carries the post-tap timed-gait results that the separate required reassessment returns, so the tap report alone reveals the response; this is the condition-wide October design (tap test = CSF removal plus measured response) | FLAGGED (lead) |
| C clinical | minor | ground_truth.key_clinical_evidence[3] | 'a positive tap supports shunting' contradicted the reworded referral (D1) | FIXED: 'supports shunt consideration' |
| C clinical | minor | ground_truth.assessment.required_recommendations[3] | 'Confirm euthyroid status on levothyroxine (TSH and free T4)' demanded a lab result as a must (class of note 49b4998b, plan C10) | FIXED: 'Continue levothyroxine 100 mcg daily unchanged'; the labs criterion stays recommended |
| B consistency | minor | patient.history_present_illness | HPI said 'only residual mild right arm paresthesias' while the exam has right arm weakness 4+/5 and a diminished brachioradialis (chronic C6 radiculopathy, confirmed by EMG) | FIXED: 'only residual mild right arm weakness and paresthesias, on gabapentin' (verifier pass 1 reworded the worker's 'for which she takes gabapentin', which tied gabapentin to the weakness) |
| C clinical | minor | ground_truth.avoided_actions | Stored exercise stress test (followup_outputs[4]) had no avoided label (class C4) | FIXED: ground_truth.avoided_actions[3] avoid-waste-exercise-stress-test (new, waste, [AHA_ACC_perioperative_2024]); ground_truth.avoided_actions[2] rationale gained the exercise stress echocardiography clause and its citation (magnetic gait with two falls) |

## Changes
The referral is now for a shunt eligibility assessment, with the 21% tap response supporting but not deciding surgery, and a new must requires individual counselling on the benefit, its uncertainty and the surgical risks and complications. The thyroid must now says to continue levothyroxine 100 mcg daily unchanged (thyroid labs remain recommended, not a must). Falls prevention applies while the neurosurgical assessment is pending. Exercise stress testing is waste; the echo waste rationale names exercise echocardiography. The HPI now mentions the residual right arm weakness that the exam documents. One key-evidence line says the tap 'supports shunt consideration'. Tier counts and revision metadata updated. The cervical spine MRI stays recommended (no upper motor neuron sign, D10).

## CENTRAL
Plan C-PACK: add [AHA_ACC_perioperative_2024] to the NPH criteria-pack allow-list and exercise_stress_test to its waste list; plan C-PACK referral and counselling wording.

## Open questions for Andrea
None.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion answered by the case's own data). test_case_guards.py -k for NPH-M01..M06: 48 passed. Probe: order_specialized_test {test_type: exercise_stress_test} is matched only by avoid-waste-exercise-stress-test and by no criterion. No MRI touched (mri_probe not needed). Not approved before this round.
case_io.py check: schema OK, synonym guard OK, full suite 6536 passed / 1 failed, and the one failure names none of NPH-M01..M06.

Pass 1: 0 errors found
Checked (verifier pass 1, 17 Nov 2026): every note id has a ruling and the ruling matches the case; plan classes C1, C2, C3, C4, C12, C10 applied as planned; tier counts in difficulty_rationale recounted and correct; exercise-test rationales match each exam; no leakage, no em dash in new text; no stored literature or drug-interaction output; perfect_agent.py -v pass; test_case_guards -k NPH-M01..M06: 48 passed; case_io.py check: only failure is test_guidance_claims (NPH-P08 drainage, central).
Cosmetic (not counted): patient.history_present_illness 'only residual mild right arm weakness and paresthesias, for which she takes gabapentin' reworded to '..., on gabapentin' (gabapentin is for the radicular pain and paresthesias, not the weakness; the medication list gives 'residual cervical radiculopathy pain'); rulings 'what' quote of the referral made verbatim; log header, CENTRAL and Open questions sections added.
