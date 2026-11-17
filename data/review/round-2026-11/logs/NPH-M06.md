# NPH-M06
Reviewer status: R1 (NB-KSC3-TWUA-QDTM) in_progress, R2 (NB-87MF-FBTV-TPWE) no notes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 444d9998-c126-4f97-a98a-613aa1a58952 | FIXED | ground_truth.assessment.required_recommendations[2]: confirm the last rivaroxaban 20 mg daily dose was at least 72 h earlier, check renal function and the blood count, review bleeding risk; a normal INR or PT does not show rivaroxaban has cleared; reduced renal clearance prolongs the interval; if shorter, postpone or check a rivaroxaban-calibrated anti-Xa level [ASRA_2025]; restart no sooner than 24 h, no heparin bridging, CHA2DS2-VASc 2 [ASRA_2025] [ACCP_2022]. ground_truth.action_criteria[1] action-3-interpret-labs: optional -> required, alternatives panels [CBC, BMP] / [CBC, CMP] / [CBC, creatinine], label 'Renal function and blood count before the lumbar tap on rivaroxaban', citations [ASRA_2025], expected_evidence 'Creatinine 1.1 mg/dL; platelets 188 x10^9/L and haemoglobin 13.4 g/dL'. New hard sequence constraint labs before action-4-analyze-csf; stop_rule gains action-3-interpret-labs. prohibited_recommendations[1] (no tap while rivaroxaban is active) kept. Limit: the hold time is history, asserted by the must |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C clinical | major | ground_truth.assessment.required_recommendations (falls must) | 'while awaiting surgery' presumed the operation that the referral no longer decides (plan class C3) | FIXED: 'while the neurosurgical assessment is pending' |
| B consistency | minor | metadata.difficulty_rationale | Tier counts stale: the post-tap reassessment was counted as recommended though required since October (plan class C12) | FIXED: recounted from action_criteria |
| E language | minor | metadata.revision_reason, metadata.last_revised | Described the October changes only | FIXED: clinical description of the November changes, 2026-11-17 |
| D leakage | minor | followup_outputs (exercise stress test, exercise echo) | Waste-labelled stress-test reports share template wording across the condition ('modified Naughton ... stopped at 2 min 30 s ... 2.3 METs ... freezing on the moving belt'); harmless because the agent sees only its own case and the tests are waste, but it is copied text | FLAGGED (lead: condition-wide, not changed here) |
| B consistency | minor | initial_tool_outputs.csf.interpretation / special_tests | The tap-test CSF report also carries the post-tap timed-gait results that the separate required reassessment returns, so the tap report alone reveals the response; this is the condition-wide October design (tap test = CSF removal plus measured response) | FLAGGED (lead) |
| C clinical | major | ground_truth.assessment.required_recommendations[0] | 'Refer to neurosurgery for CSF shunting' (class D1) | FIXED: shunt eligibility assessment for secondary NPH after the bilateral SDH; tap supports but does not decide; programmable valve preferred if a shunt is placed because of the risk of a recurrent subdural collection with overdrainage [Nakajima_2021] |
| C clinical | major | ground_truth.assessment.required_recommendations | No counselling on benefit or complications (class D2) | FIXED: new required_recommendations[1], including the higher risk of a recurrent subdural collection after the bilateral haematomas [Nakajima_2021] |
| C clinical | minor | ground_truth.key_clinical_evidence[5] | Rivaroxaban line said only 'held for at least 72 hours' | FIXED: adds renal function and blood count checked and that a normal INR or PT does not show rivaroxaban has cleared |
| C clinical | minor | initial_tool_outputs.labs.panels.CBC[Hemoglobin].clinical_significance | Abnormal haemoglobin 13.4 g/dL (L) had a null significance, though the blood count is now the required pre-tap bleeding-risk check | FIXED: 'Mildly below the male reference range; relevant to the bleeding-risk assessment on rivaroxaban' |
| C clinical | minor | ground_truth.avoided_actions | Stored exercise stress test (followup_outputs[3]) had no avoided label (class C4) | FIXED: ground_truth.avoided_actions[3] avoid-waste-exercise-stress-test (new, waste, [AHA_ACC_perioperative_2024]); ground_truth.avoided_actions[2] rationale gained the exercise stress echocardiography clause and its citation (walker-dependent magnetic gait) |

## Changes
Before the lumbar tap on rivaroxaban, renal function and the blood count are now a required step that must precede the tap (hard constraint, part of the stop rule), and the rivaroxaban must asks for a confirmed 72-hour hold from the last dose rather than reliance on a normal INR or PT, with postponement or a drug-calibrated anti-Xa level if the interval is shorter; restart rules and the prohibition on tapping while the drug is active are unchanged. The mildly low haemoglobin now carries a short interpretation. The referral is for a shunt eligibility assessment for secondary NPH, with a programmable valve preferred if a shunt is placed, and a new must requires counselling on benefit, its uncertainty, the shunt complications and the higher risk of a recurrent subdural collection. Falls prevention applies while the neurosurgical assessment is pending. Exercise stress testing is waste; the echo waste rationale names exercise echocardiography. Key evidence aligned; tier counts and revision metadata updated. The secondary label and the rejected iNPH labels are unchanged (D8).

## CENTRAL
Plan C-PACK and C-GUIDE: labs required here as a pre-tap safety check on rivaroxaban with a hard labs-before-CSF constraint (pack tiers, interpret_labs our_response); [AHA_ACC_perioperative_2024] in the allow-list.

## Open questions for Andrea
None.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion answered by the case's own data). test_case_guards.py -k for NPH-M01..M06: 48 passed. Probe: order_specialized_test {test_type: exercise_stress_test} is matched only by avoid-waste-exercise-stress-test and by no criterion. No MRI touched (mri_probe not needed). Not approved before this round.
case_io.py check: schema OK, synonym guard OK, full suite 6536 passed / 1 failed, and the one failure names none of NPH-M01..M06.

Pass 1: 0 errors found
Checked (verifier pass 1, 17 Nov 2026): every note id has a ruling and the ruling matches the case; plan classes C1, C2, C3, C4, C12, C6 (labs required with CBC+BMP/CMP/creatinine alternatives, all three served the stored CBC and BMP panels; hard labs-before-CSF constraint; stop rule; canonical DOAC must; CHA2DS2-VASc recomputed from the patient block) applied as planned; tier counts in difficulty_rationale recounted and correct; exercise-test rationales match each exam; no leakage, no em dash in new text; no stored literature or drug-interaction output; perfect_agent.py -v pass; test_case_guards -k NPH-M01..M06: 48 passed; case_io.py check: only failure is test_guidance_claims (NPH-P08 drainage, central).
Cosmetic (not counted): log header line, CENTRAL and Open questions sections added; nothing else.
