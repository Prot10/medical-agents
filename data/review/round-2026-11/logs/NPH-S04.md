# NPH-S04

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM); no R2 note | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 46348ed9-c172-497e-992f-aa5fb619c71e | NO-ACTION | Approval of the chief complaint ("bene così"); patient.chief_complaint unchanged (plan NPH D15, C13). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C clinical | major | ground_truth.assessment.required_recommendations[0] | Referral must said "Refer to neurosurgery for CSF shunting with a programmable valve", presuming surgery from a prognostic tap response (class C1, D1; NPH notes 7f90233f, 8bb5643e, 2cd1748b, 6abe35f0 as a class) [Marmarou_2005] [Halperin_2015] | FIXED: "Refer to neurosurgery for shunt eligibility assessment ...", case evidence clause kept verbatim, tail "the tap response supports considering a shunt, with a programmable valve if one is placed, but does not by itself decide surgery [Nakajima_2021]" |
| C clinical | major | ground_truth.assessment.required_recommendations[1] | No must counselled on the expected benefit, its uncertainty and the shunt complications (class C2, D2/D3) | FIXED: canonical counselling must (gait most likely to improve, degree uncertain; obstruction needing revision, infection, headache, subdural haematoma from over-drainage [Nakajima_2021]). New must, no limit clause (plan C2 "others"). |
| C clinical | minor | ground_truth.assessment.required_recommendations[2] | Falls must said "while awaiting surgery", presuming the operation (class C3, D4) | FIXED: "while the neurosurgical assessment is pending"; nothing else in the must changed |
| C clinical | minor | ground_truth.avoided_actions[3] | order_specialized_test exercise_stress_test had no waste label although it has no indication and is unsafe with this gait (class C4, D5; notes dc2b866b, 89a27997 as a class) | FIXED: new avoided action avoid-waste-exercise-stress-test (waste, {"test_type": "exercise_stress_test"}), rationale adapted to his freezing gait, [AHA_ACC_perioperative_2024]; no criterion matches the call |
| C clinical | minor | ground_truth.avoided_actions[2].rationale | Echo waste wildcard already covered exercise stress echocardiography but did not say so (class C4) | FIXED: clause "and exercise stress echocardiography adds nothing: there is no cardiac indication, and treadmill exercise is unsafe with this gait disorder [AHA_ACC_perioperative_2024]" appended; key added to citations |
| B consistency | minor | metadata.difficulty_rationale | Tier count said 3 required and 1 recommended (post-tap reassessment), but the post-tap reassessment has been required since October (class C12, D16) | FIXED: recounted from action_criteria (4 required, no recommended); red-herring and differential counts checked and unchanged |
| E language | minor | metadata.revision_reason, metadata.last_revised | Revision metadata out of date | FIXED: November clinical description prepended; last_revised 2026-11-17 |
| C clinical | minor | followup_outputs (request_levodopa_challenge) | A levodopa challenge is stored without a waste label although nothing in the case suggests dopaminergic parkinsonism (key_clinical_evidence[3] even says no levodopa trial is needed) | FLAGGED: plan NPH section 5 leaves the low-yield unlabelled follow-ups (levodopa challenge in all 30) for the next physician review |

Checked with no error found: patient block (no timeline leak beyond the outside imaging report the October round kept, no diagnosis named), MRI (all iNPH markers, descriptive impression, no contrast claimed), baseline gait vs exam, CSF report vs post-tap report vs expected_evidence (numbers and percentages recomputed), labs vs reference ranges and sex, exercise test heart-rate percentages vs age-predicted maximum and rest BP vs vitals, differential likelihoods vs results, sequence constraints and stop rule (no red flag left unaddressed), no literature output left (class LIT), no MRI contrast pair needed (class MRI-CONTRAST: no gadolinium content).

## Changes
The only reviewer note approved the chief complaint, which is unchanged. The case received the NPH class corrections of the November round: the referral must is now a neurosurgical shunt eligibility assessment based on the same tap, MRI and CSF evidence, with a programmable valve only if a shunt is placed, because the tap response supports but does not decide surgery. A new counselling must asks that, before the decision on surgery, the patient and family hear that gait is most likely to improve, the degree is uncertain, and the shunt complications (obstruction needing revision, infection, headache, subdural haematoma from over-drainage). The falls must no longer says "while awaiting surgery" but "while the neurosurgical assessment is pending". An exercise stress test is now labelled waste (no cardiac indication; treadmill exercise is unsafe with this gait and comes out submaximal), and the echocardiography waste rationale now names exercise stress echocardiography too, both citing the 2024 AHA/ACC perioperative guideline. The tier count in the difficulty rationale was corrected (4 required, the post-tap reassessment included). Diagnosis, work-up criteria, sequence constraints, stop rule and all tool reports are unchanged; the perfect-agent check, the case guards and the full test suite pass.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
None for this case (condition-level requests are in plans/NPH.md section 4).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Pass 1: 0 errors found
- Checked: the single note (chief-complaint approval) has a NO-ACTION ruling, which is right; C1 referral (evidence clause verbatim, conditional programmable valve), C2 counselling must (case limit as in the plan), C3 falls wording, C4 exercise-test waste entry (pronoun and gait wording match the exam and HPI; no criterion matches the call) and echo clause with citation, C12 tier, red-herring and differential counts recounted from the case; no remaining text presumes surgery; exercise-test heart-rate percentages and rest values match age and vitals; no em dashes in new text; no answer leakage introduced.
- perfect_agent.py -v passes (MRI served from the case, confirmed with mri_probe.py for P09), test_case_guards -k passes (48 tests over the six cases); case_io check shows only test_guidance_claims failures (maintained centrally) and NPH-P08.
- Cosmetic (not counted): added the missing CENTRAL and Open questions sections of the log template.
