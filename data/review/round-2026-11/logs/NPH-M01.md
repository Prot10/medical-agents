# NPH-M01
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress, R2 (NB-87MF-FBTV-TPWE) no notes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 7f90233f-8fee-40c4-99d8-cb0f0b741f8d | FIXED | ground_truth.assessment.required_recommendations[0]: 'Refer to neurosurgery for shunt eligibility assessment ...; the tap-test response supports considering a shunt, with a programmable valve if one is placed, but does not by itself decide surgery [Nakajima_2021]'. required_recommendations[2] rewritten as pre-surgical counselling on benefit (gait most likely; memory and urinary symptoms, partly BPH, less predictable; degree uncertain) and complications (obstruction needing revision, infection, headache, subdural haematoma from over-drainage) [Nakajima_2021] |
| dc2b866b-98e3-446a-91d5-2d7dbbe2d5d8 | FIXED | ground_truth.avoided_actions[3] avoid-waste-exercise-stress-test (new, waste, [AHA_ACC_perioperative_2024]); ground_truth.avoided_actions[2] rationale gained the exercise stress echocardiography clause and its citation; the rationale names the magnetic gait and freezing at initiation. followup_outputs[3] kept (stops a library normal contradicting the case) |
| 89a27997-a823-4886-8463-64e9ae327d6c | FIXED | Scoring already treated it as waste (wildcard avoid-waste-3-order-echocardiogram, no criterion credits it); ground_truth.avoided_actions[2] rationale now explicitly classifies exercise stress echocardiography as low-yield with [AHA_ACC_perioperative_2024]. followup_outputs[4] kept |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C clinical | major | ground_truth.assessment.required_recommendations (falls must) | 'while awaiting surgery' presumed the operation that the referral no longer decides (plan class C3) | FIXED: 'while the neurosurgical assessment is pending' |
| B consistency | minor | metadata.difficulty_rationale | Tier counts stale: the post-tap reassessment was counted as recommended though required since October (plan class C12) | FIXED: recounted from action_criteria |
| E language | minor | metadata.revision_reason, metadata.last_revised | Described the October changes only | FIXED: clinical description of the November changes, 2026-11-17 |
| D leakage | minor | followup_outputs (exercise stress test, exercise echo) | Waste-labelled stress-test reports share template wording across the condition ('modified Naughton ... stopped at 2 min 30 s ... 2.3 METs ... freezing on the moving belt'); harmless because the agent sees only its own case and the tests are waste, but it is copied text | FLAGGED (lead: condition-wide, not changed here) |
| B consistency | minor | initial_tool_outputs.csf.interpretation / special_tests | The tap-test CSF report also carries the post-tap timed-gait results that the separate required reassessment returns, so the tap report alone reveals the response; this is the condition-wide October design (tap test = CSF removal plus measured response) | FLAGGED (lead) |
| C clinical | minor | ground_truth.key_clinical_evidence[3] | 'a positive tap supports shunting' contradicted the reworded referral (D1) | FIXED: 'supports shunt consideration' |

## Changes
The neurosurgical referral is now for a shunt eligibility assessment: the 25% tap response, the MRI and normal-pressure CSF support considering a shunt (programmable valve if placed) but do not decide surgery. The counselling must now covers benefit, its uncertainty and the shunt complications, keeping the BPH and memory limits. Falls prevention applies while the neurosurgical assessment is pending. Exercise stress testing is waste (new avoided entry), and the echo waste rationale names exercise echocardiography. One key-evidence line now says the tap 'supports shunt consideration'. Tier counts and revision metadata updated. No change to the patient, reports, criteria, differential or diagnosis.

## CENTRAL
Plan C-PACK: add [AHA_ACC_perioperative_2024] to the NPH criteria-pack allow-list and exercise_stress_test to its waste list; plan C-PACK referral and counselling wording.

## Open questions for Andrea
None.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion answered by the case's own data). test_case_guards.py -k for NPH-M01..M06: 48 passed. Probe: order_specialized_test {test_type: exercise_stress_test} is matched only by avoid-waste-exercise-stress-test and by no criterion. No MRI touched (mri_probe not needed). Not approved before this round.
case_io.py check: schema OK, synonym guard OK, full suite 6536 passed / 1 failed, and the one failure names none of NPH-M01..M06.

Pass 1: 0 errors found
Checked (verifier pass 1, 17 Nov 2026): every note id has a ruling and the ruling matches the case; plan classes C1, C2, C3, C4, C12 applied as planned; tier counts in difficulty_rationale recounted and correct; exercise-test rationales match each exam; no leakage, no em dash in new text; no stored literature or drug-interaction output; perfect_agent.py -v pass; test_case_guards -k NPH-M01..M06: 48 passed; case_io.py check: only failure is test_guidance_claims (NPH-P08 drainage, central).
Cosmetic (not counted): log header line, CENTRAL and Open questions sections added; rulings 'what' quote of the referral made verbatim.
