# NPH-M03
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress, R2 (NB-87MF-FBTV-TPWE) no notes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 6687fd88-bd7f-4d34-9df8-392fb9751726 | FIXED | ground_truth.assessment.required_recommendations[1]: confirm the last apixaban 5 mg twice-daily dose was at least 72 h earlier, check renal function and the blood count, review bleeding risk; a normal INR or PT does not show apixaban has cleared; reduced renal clearance prolongs the interval; if shorter, postpone or check an apixaban-calibrated anti-Xa level [ASRA_2025]; restart no sooner than 24 h, no heparin bridging, CHA2DS2-VASc 4 with prior stroke [ASRA_2025] [ACCP_2022]. ground_truth.action_criteria[1] action-3-interpret-labs: optional -> required, alternatives panels [CBC, BMP] / [CBC, CMP] / [CBC, creatinine], label 'Renal function and blood count before the lumbar tap on apixaban', citations [ASRA_2025], expected_evidence 'Creatinine 1.0 mg/dL; normal blood count with platelets 204 x10^9/L' (INR no longer cited as evidence). New hard sequence constraint labs before action-4-analyze-csf; stop_rule.required_before_assessment gains action-3-interpret-labs. prohibited_recommendations[2] kept. Limit: the time of the last dose is history, asserted by the must; no tool represents it |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C clinical | major | ground_truth.assessment.required_recommendations (falls must) | 'while awaiting surgery' presumed the operation that the referral no longer decides (plan class C3) | FIXED: 'while the neurosurgical assessment is pending' |
| B consistency | minor | metadata.difficulty_rationale | Tier counts stale: the post-tap reassessment was counted as recommended though required since October (plan class C12) | FIXED: recounted from action_criteria |
| E language | minor | metadata.revision_reason, metadata.last_revised | Described the October changes only | FIXED: clinical description of the November changes, 2026-11-17 |
| D leakage | minor | followup_outputs (exercise stress test, exercise echo) | Waste-labelled stress-test reports share template wording across the condition ('modified Naughton ... stopped at 2 min 30 s ... 2.3 METs ... freezing on the moving belt'); harmless because the agent sees only its own case and the tests are waste, but it is copied text | FLAGGED (lead: condition-wide, not changed here) |
| B consistency | minor | initial_tool_outputs.csf.interpretation / special_tests | The tap-test CSF report also carries the post-tap timed-gait results that the separate required reassessment returns, so the tap report alone reveals the response; this is the condition-wide October design (tap test = CSF removal plus measured response) | FLAGGED (lead) |
| C clinical | minor | ground_truth.key_clinical_evidence[3] | 'a positive tap supports shunting' contradicted the reworded referral (D1) | FIXED: 'supports shunt consideration' |
| C clinical | minor | ground_truth.key_clinical_evidence[5] | Apixaban line said only 'held for at least 72 hours' | FIXED: adds renal function and blood count checked and that a normal INR does not show apixaban has cleared |
| C clinical | major | ground_truth.assessment.required_recommendations[3] | Counselling said 'shunting is expected to improve' (overstated benefit, D3) and named no complications | FIXED: canonical counselling, 'more likely to improve the new shuffling gait and urinary urgency than the fixed post-stroke right-sided weakness and circumduction', degree uncertain, complications listed [Nakajima_2021] |
| C clinical | major | ground_truth.assessment.required_recommendations[0] | 'Refer to neurosurgery for CSF shunting' (class D1) | FIXED: shunt eligibility assessment, tap supports but does not decide [Nakajima_2021] |
| C clinical | minor | ground_truth.avoided_actions | Stored exercise stress test (followup_outputs[3]) had no avoided label (class C4) | FIXED: ground_truth.avoided_actions[3] avoid-waste-exercise-stress-test (new, waste, [AHA_ACC_perioperative_2024]); ground_truth.avoided_actions[2] rationale gained the exercise stress echocardiography clause and its citation (shuffling gait on a post-stroke circumduction) |

## Changes
Before the lumbar tap on apixaban, renal function and the blood count are now a required step that must precede the tap (hard constraint, part of the stop rule), and the apixaban must asks the clinician to confirm a 72-hour hold from the last dose, not to rely on the normal INR, with postponement or a drug-calibrated anti-Xa level if the interval is shorter; restart rules unchanged. The referral is for a shunt eligibility assessment, and the counselling must no longer promises improvement: gait and urgency are more likely to improve than the fixed post-stroke deficits, the degree is uncertain and the complications are listed. Falls prevention applies while the neurosurgical assessment is pending. Exercise stress testing is waste; the echo waste rationale names exercise echocardiography. Key evidence aligned; tier counts and revision metadata updated. The lab report itself (which lists a normal INR) is unchanged.

## CENTRAL
Plan C-PACK and C-GUIDE: labs required here as a pre-tap safety check on apixaban with a hard labs-before-CSF constraint (pack tiers, interpret_labs our_response); [AHA_ACC_perioperative_2024] in the allow-list.

## Open questions for Andrea
None.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion answered by the case's own data). test_case_guards.py -k for NPH-M01..M06: 48 passed. Probe: order_specialized_test {test_type: exercise_stress_test} is matched only by avoid-waste-exercise-stress-test and by no criterion. No MRI touched (mri_probe not needed). Not approved before this round.
case_io.py check: schema OK, synonym guard OK, full suite 6536 passed / 1 failed, and the one failure names none of NPH-M01..M06.

Pass 1: 0 errors found
Checked (verifier pass 1, 17 Nov 2026): every note id has a ruling and the ruling matches the case; plan classes C1, C2, C3, C4, C12, C6 (labs required with CBC+BMP/CMP/creatinine alternatives, all three served the stored CBC and BMP panels; hard labs-before-CSF constraint; stop rule; canonical DOAC must; CHA2DS2-VASc recomputed from the patient block) applied as planned; tier counts in difficulty_rationale recounted and correct; exercise-test rationales match each exam; no leakage, no em dash in new text; no stored literature or drug-interaction output; perfect_agent.py -v pass; test_case_guards -k NPH-M01..M06: 48 passed; case_io.py check: only failure is test_guidance_claims (NPH-P08 drainage, central).
Cosmetic (not counted): log header line, CENTRAL and Open questions sections added; nothing else.
