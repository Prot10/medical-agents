# SYNC-CARD-S01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split the stored brain MRI (followup request_brain_mri, off-pathway, no MRI criterion) into a plain copy (contrast_used false, original slot; removed "No enhancing lesions post-gadolinium" and the impression clause "No enhancing lesions.") and the unchanged gadolinium study (contrast_used true, trigger request_brain_mri_with_contrast, placed right after it). No criterion changed: brain MRI is not indicated in syncope without focal signs (ESC 2018, Class III), so no gadolinium question exists.
- MRI-CONTRAST verified: plain copy free of gadolinium content with impression consistent with findings, gadolinium copy unchanged (contrast_used true) right after it, no MRI criterion (syncope, gadolinium not indicated); mri_probe: plain, contrast and both orders in either sequence answered by the case (never the library), case fallback MRI consistent; no other field changed against 393c547e; perfect_agent -v passes. No error found in the case; removed the two duplicate copies of the worker's MRI-CONTRAST log line.

## Reviewer notes
Reviewer status: R2 approved | Approved before this round (R2, work/approved.txt): changed only for condition class defects (plan SYNC-CARD.md C3 AVOIDED-DECOY, D3), which are additive avoided-action labels.

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-S01:policy_verdict | NO-ACTION | Approval with no comment. Class C3 labels added (see Own findings). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | `ground_truth.avoided_actions[5]`-`[11]` | Served off-pathway reports without a label (class C3): `avoid-waste-electrophysiology-study` [ESC_2018], `avoid-waste-bubble-study`, `avoid-waste-exercise-echo` (as the exercise test) [ESC_2018], `avoid-waste-coronary-angiography` and `avoid-waste-coronary-cta` (fallback; troponin I 0.02, no angina, ischaemic change or ventricular arrhythmia) [ESC_2018], `avoid-waste-emg-ncs` (known mild diabetic neuropathy; fallback NCS), `avoid-waste-tee` (fallback). | FIXED |
| E | minor | `fallback_tool_outputs.specialized_test` (NCS) | Identical NCS numbers to RS03, RS05 and S02 (template carry-over in a decoy); kept per D3. Reported to the lead. | FLAGGED |
| A | minor | `metadata.last_revised`, `metadata.revision_reason` | Updated to 2026-11-17. | FIXED |

Checks: new entries match only their own calls and no criterion; each call is answered by the case's own report or case fallback; perfect_agent passes; test_case_guards pass; case_io check: no failure names the case. Driving must R5 left as is (plan C5 NO-ACTION).

## Changes
Approved case; Reviewer 2 asked for nothing. The only change is additive: the electrophysiology study, bubble study, exercise echocardiogram, invasive coronary angiography and coronary CTA, nerve conduction studies and TEE, which the case answers when ordered but which play no part in persistent complete AV block with a wide escape, are now labelled waste, as in the rest of the condition. No clinical text, criterion, sequence or stop rule changed.

## Verification
Pass 1: 0 errors found
Cosmetic (not counted): `avoid-waste-emg-ncs` rationale said "Known mild diabetic peripheral neuropathy", but the PMH records no neuropathy diagnosis. Reworded to "Mild diabetic peripheral neuropathy on examination". This case keeps the original NCS values; RS03, RS05 and S02 now have their own.
Pass 2: 1 error found
- B, `patient.neurological_exam.sensory`: read "proprioception, and vibration intact throughout" followed by "mildly diminished vibration at bilateral great toes", contradicting itself and the pass-1 `avoid-waste-emg-ncs` rationale. Reworded to "Light touch, pinprick and proprioception intact throughout. Vibration intact except mildly diminished at bilateral great toes, ..." (pre-existing text, fixed because it states the fact the changed rationale relies on).
- Checked: rationale now agrees with the exam and history (type 2 diabetes, no prior neuropathy diagnosis); NCS values unchanged. perfect_agent -v ok, test_case_guards ok.
Pass 3: 0 errors found
- Checked the pass-2 fix to `patient.neurological_exam.sensory`: now reads "Light touch, pinprick and proprioception intact throughout. Vibration intact except mildly diminished at bilateral great toes", no longer self-contradictory, and agrees with the `avoid-waste-emg-ncs` rationale (vibration mildly reduced at the great toes), Achilles 1+ and the NCS report (mild length-dependent axonal polyneuropathy). No other field states a different vibration finding. No change. perfect_agent -v ok, test_case_guards ok.
- Condition auditor, 17 Nov 2026: exercise severity made uniform (class EXERCISE-SEVERITY, plan D2 as applied). The workers raised RS01 and S03 to harm on Fletcher 2013's absolute contraindication (uncontrolled arrhythmia causing symptoms or haemodynamic compromise), beyond the plan's RS01 line; the same facts hold here, so the waste label under-penalised a contraindicated test. avoided_actions avoid-waste-5-exercise-stress-test (id kept) and the exercise echo entry (id now avoid-harm-exercise-echo) changed from waste to harm, with the rationale citing the case's own telemetry (persistent complete AV block, escape 28-42 bpm, lightheadedness at 30-32 bpm, 4.2 s pause) and [Fletcher_2013]. Approved case: changed for a real class defect, no other text. metadata.revision_reason updated. perfect_agent, test_case_guards -k, case_io check clean.
Pass 4: 0 errors found
- Checked the condition-audit change: exercise entries now harm; rationale matches telemetry (complete AV block, escape 28-42 bpm, lightheadedness at 30-32 bpm, 4.2 s pause) and Fletcher 2013; the stored exercise reports say 'not performed', consistent; no criterion matches. revision_reason and ruling agree. perfect_agent -v ok, test_case_guards ok. No change.
Pass 5: 0 errors found
- Nothing was changed after the last 0-error pass (pass 4; no condition-audit or orchestrator entry after it). Checks only: perfect_agent -v ok, test_case_guards -k ok. No change.
