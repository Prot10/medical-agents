# SYNC-CARD-RS05

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-5-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R2 approved | Approved before this round: yes (R2, work/approved.txt). Changed for real defects (plan C10, C5) and additive class labels (C3).

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-RS05:policy_verdict | NO-ACTION | Approval with no comment. Class findings applied (see Own findings). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| A | major | `ground_truth.action_criteria[4]` (new `action-coronary-assessment`) | Class UNSATISFIABLE (plan C10, D5): must R6 asks for coronary angiography and no criterion ordered it. Added a recommended criterion, alternatives `order_advanced_imaging {modality: coronary_angiography}` and `{modality: coronary_CTA}`, label "Coronary assessment (invasive angiography or coronary CTA)", rationale monomorphic VT from the inferior scar with troponin 0.06 ng/mL after inferior STEMI and PCI (ESC 2022), citation `[ESC_2022_VA_SCD]`, expected_evidence from the stored angiography (patent RCA stent, no new obstructive disease). Placed after monitoring; not in the stop rule. | FIXED |
| B | minor | `followup_outputs[2]`, `[3]` | The coronary angiography and coronary CTA reports are now pathway studies: moved from the off-pathway tail to right after telemetry (angiography, then CTA), before the drug checks. Each order is answered by its own report (checked). | FIXED |
| C | major | `ground_truth.assessment.required_recommendations[7]` | Driving must attributed the 3-month secondary-prevention ICD interval to ESC 2018 (which gives 1 month after any ICD); the 3-month figure is EHRA 2009. Canonical DR-ICD2 text, adding the Group 2 restriction (plan C5, D8). | FIXED |
| C | minor | `ground_truth.avoided_actions[6]`-`[10]` | Served off-pathway reports without a label (class C3): `avoid-waste-electrophysiology-study` [ESC_2018], `avoid-waste-bubble-study`, `avoid-waste-exercise-echo` (as the exercise test) [ESC_2018], `avoid-waste-emg-ncs` (known mild diabetic neuropathy), `avoid-waste-tee` (fallback). | FIXED |
| E | minor | `followup_outputs[11]` (NCS) | Identical NCS numbers to RS03, S01 and S02 (template carry-over in a decoy report); kept per D3. Reported to the lead. | FLAGGED |
| A | minor | `metadata.last_revised`, `metadata.revision_reason` | Updated to 2026-11-17. | FIXED |

Checks: perfect_agent -v passes (the coronary criterion receives followup[2] request_coronary_angiography; the CTA alternative is answered by its own report); new avoided entries match only their own calls and no criterion; test_case_guards pass; case_io check: no failure names the case.

## Changes
Approved case; Reviewer 2 asked for nothing, but two factual defects were corrected. The must asking for coronary angiography had no matching action, so a recommended "coronary assessment (invasive angiography or coronary CTA)" step was added for monomorphic VT from the inferior scar with a mildly raised troponin (ESC 2022), and the two coronary reports moved up the pathway right after telemetry. The driving advice now attributes the 3-month restriction after a secondary-prevention ICD to the EHRA 2009 consensus (ESC 2018 gives 1 month after any ICD) and adds the permanent Group 2 restriction. Studies the case answers but that play no part here are labelled waste: the electrophysiology study, bubble study, exercise echocardiogram, nerve conduction studies and TEE. Diagnosis, other criteria, sequence and stop rule are unchanged.

## Verification
Pass 1: 0 errors found
Cosmetic (not counted): `avoid-waste-emg-ncs` rationale said "Known ... neuropathy", but no prior diagnosis is recorded; the neuropathy is an examination finding. Reworded to "... peripheral neuropathy on examination". The NCS decoy report had numbers identical to the other SYNC-CARD cases (template carry-over, flagged by the worker). The per-nerve values are now adjusted to this patient (age, height, severity on examination), with the same impression.
Pass 2: 1 error found
- B, `patient.neurological_exam.sensory`: read "vibration ... intact throughout" followed by "mildly diminished vibration at bilateral great toes", contradicting itself and the pass-1 `avoid-waste-emg-ncs` rationale ("vibration mildly reduced at the great toes"). Reworded to "Light touch, pinprick and proprioception intact throughout. Vibration intact except mildly diminished at bilateral great toes, ..." (pre-existing text, fixed because it states the fact the changed rationale relies on).
- Checked: rationale matches the exam and history (type 2 diabetes, Achilles 1+); emg_ncs follow-up values for 56 y, 158 cm are plausible (normal motor studies, sural 5 uV reduced, tibial F 52 ms mildly prolonged for height, H-reflex absent), quantitative_data equals the findings, impression unchanged. perfect_agent -v ok, test_case_guards ok.
Pass 3: 0 errors found
- Checked the pass-2 fix to `patient.neurological_exam.sensory`: now reads "Light touch, pinprick and proprioception intact throughout. Vibration intact except mildly diminished at bilateral great toes", no longer self-contradictory, and agrees with the `avoid-waste-emg-ncs` rationale (vibration mildly reduced at the great toes), Achilles 1+ and the NCS report (mild length-dependent axonal polyneuropathy). No other field states a different vibration finding. No change. perfect_agent -v ok, test_case_guards ok.
- Condition auditor, 17 Nov 2026: exercise severity made uniform (class EXERCISE-SEVERITY, plan D2 as applied). The workers raised RS01 and S03 to harm on Fletcher 2013's absolute contraindication (uncontrolled arrhythmia causing symptoms or haemodynamic compromise), beyond the plan's RS01 line; the same facts hold here, so the waste label under-penalised a contraindicated test. avoided_actions avoid-waste-6-exercise-stress-test (id kept) and the exercise echo entry (now avoid-harm-exercise-echo) changed from waste to harm: sustained monomorphic VT recurred on telemetry (188 bpm, 32 s, near-syncope), an uncontrolled symptomatic arrhythmia; the old rationale itself said the test "risks provoking VT". [Fletcher_2013]. Also Condition auditor, 17 Nov 2026, blind leak pass: a check_drug_interactions output (served to any drug query, including a first call before any test) named the diagnosis: amiodarone alternative "Catheter ablation of the VT substrate" now "Catheter ablation of the arrhythmia substrate". Approved case: changed for real defects only. perfect_agent, test_case_guards -k, case_io check clean.
Pass 4: 0 errors found
- Checked the condition-audit changes: exercise test and exercise echo entries now harm; rationale matches the telemetry follow-up (sustained monomorphic VT 188 bpm, 32 s, near-syncope) and Fletcher 2013; the exercise report (NSVT in recovery) agrees. Amiodarone follow-up alternative now 'Catheter ablation of the arrhythmia substrate', no diagnosis named; drug criterion evidence unaffected. revision_reason and ruling agree. perfect_agent -v ok, test_case_guards ok. No change.
Pass 5: 0 errors found
- Nothing was changed after the last 0-error pass (pass 4; no condition-audit or orchestrator entry after it). Checks only: perfect_agent -v ok, test_case_guards -k ok. No change.
