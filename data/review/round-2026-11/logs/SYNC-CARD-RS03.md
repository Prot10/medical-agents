# SYNC-CARD-RS03

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split the stored brain MRI (followup request_brain_mri, off-pathway, no MRI criterion) into a plain copy (contrast_used false, original slot; removed "No enhancing lesions after gadolinium administration" and the impression clause "No enhancing lesions.") and the unchanged gadolinium study (contrast_used true, trigger request_brain_mri_with_contrast, placed right after it). No criterion changed: brain MRI is not indicated in syncope without focal signs (ESC 2018, Class III), so no gadolinium question exists.
- MRI-CONTRAST verified: plain copy free of gadolinium content with impression consistent with findings, gadolinium copy unchanged (contrast_used true) right after it, no MRI criterion (syncope, gadolinium not indicated); mri_probe: plain, contrast and both orders in either sequence answered by the case (never the library), case fallback MRI consistent; no other field changed against 393c547e; perfect_agent -v passes. No error found in the case; removed the two duplicate copies of the worker's MRI-CONTRAST log line.

## Reviewer notes
Reviewer status: R2 approved | Approved before this round (R2, work/approved.txt): changed only for condition class defects (plan SYNC-CARD.md C3 AVOIDED-DECOY, D3), which are additive avoided-action labels.

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-RS03:policy_verdict | NO-ACTION | Approval with no comment. Class C3 labels added (see Own findings). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | `ground_truth.avoided_actions[5]`-`[11]` | Served off-pathway reports without a label (class C3, D3): new waste entries `avoid-waste-electrophysiology-study` [ESC_2018], `avoid-waste-bubble-study`, `avoid-waste-exercise-echo` (as the exercise test, D4) [ESC_2018], `avoid-waste-chest-ct` and `avoid-waste-chest-cta` (no PE, dissection or mass; eGFR about 49, contrast not a material risk per ACR-NKF 2020, no indication), `avoid-waste-emg-ncs` (known mild diabetic neuropathy; fallback NCS), `avoid-waste-tee` (fallback TEE). | FIXED |
| C | minor | coronary angiography follow-up, coronary CTA fallback | Left unlabelled per plan D5: must R5 makes graft angiography conditional on a rising troponin. | no change |
| E | minor | `fallback_tool_outputs.specialized_test` (NCS) | Identical NCS numbers to RS05, S01 and S02 (template carry-over in an off-pathway decoy); clinically consistent with the case's mild neuropathy; stored reports are kept per D3. Reported to the lead. | FLAGGED |
| A | minor | `metadata.last_revised`, `metadata.revision_reason` | Updated to 2026-11-17. | FIXED |

Checks: each new entry matches only its own call (chest_CT and chest_CTA with and without contrast), none matches a criterion; every such call is answered by the case's own report or case fallback; perfect_agent passes; test_case_guards pass; case_io check: no failure names the case. Driving must R6 ("1 week (ESC 2018)") left as is (plan C5 NO-ACTION).

## Changes
Approved case; Reviewer 2 asked for nothing. The only change is additive: studies the case answers when ordered but that play no part in this patient's work-up are now labelled waste, as in the rest of the condition: the electrophysiology study, bubble study, exercise echocardiogram (as the exercise test), chest CT and chest CT angiography, nerve conduction studies and TEE. Coronary and graft angiography stay unlabelled because must R5 makes them conditional on a rising troponin. No clinical text, criterion, sequence or stop rule changed.

## Verification
Pass 1: 0 errors found
Cosmetic (not counted): `avoid-waste-emg-ncs` rationale said "Known ... neuropathy", but no prior diagnosis is recorded; the neuropathy is an examination finding. Reworded to "... peripheral neuropathy on examination". The NCS decoy report had numbers identical to the other SYNC-CARD cases (template carry-over, flagged by the worker). The per-nerve values are now adjusted to this patient (age, height, severity on examination), with the same impression.
Pass 2: 0 errors found
- Checked the pass-1 changes: `avoid-waste-emg-ncs` rationale matches the exam (vibration mildly diminished at the great toes, Achilles 1+, type 2 diabetes in the history, no prior neuropathy diagnosis). Fallback emg_ncs values (72 y, 173 cm) are plausible and internally consistent: motor studies within normal limits for age, sural 4 uV reduced, tibial F 57 ms mildly prolonged, H-reflex absent fits Achilles 1+, quantitative_data equals the findings, impression unchanged and consistent. No change. perfect_agent -v ok, test_case_guards ok.
Pass 3: 0 errors found
- Nothing was changed after the last 0-error pass (no condition-audit or orchestrator entry). Checks only: perfect_agent -v ok, test_case_guards ok.
- Condition auditor, 17 Nov 2026: exercise severity made uniform (class EXERCISE-SEVERITY, plan D2 as applied). The workers raised RS01 and S03 to harm on Fletcher 2013's absolute contraindication (uncontrolled arrhythmia causing symptoms or haemodynamic compromise), beyond the plan's RS01 line; the same facts hold here, so the waste label under-penalised a contraindicated test. avoided_actions avoid-waste-5-exercise-stress-test (id kept) and the exercise echo entry (now avoid-harm-exercise-echo) changed from waste to harm (persistent complete AV block, escape 28-41 bpm, pauses 5.2 s asleep and 4.4 s awake with presyncope), [Fletcher_2013]. Also Condition auditor, 17 Nov 2026, blind leak pass: a check_drug_interactions output (served to any drug query, including a first call before any test) quoted the echo result ("LVEF 45%", expected evidence of action-3-order-echocardiogram) and asserted the diagnosis ("in complete heart block it can slow the escape rhythm further"; initial and fallback "Beta-blockers in third-degree AV block"). Now: "where AV conduction is impaired it can slow an escape rhythm", "Reassess the indication for a beta-blocker after any pacing, given the coronary disease", "after any pacemaker implantation", and the product-label wording "second- or third-degree AV block without a pacemaker". The drug criterion's expected evidence is still carried. Approved case: changed for real defects only. perfect_agent, test_case_guards -k, case_io check clean.
Pass 4: 0 errors found
- Checked the condition-audit changes: avoid-waste-5-exercise-stress-test and avoid-harm-exercise-echo now harm, rationale facts match the telemetry follow-up (complete AV block, escape 28-41 bpm, pauses 5.2 s asleep and 4.4 s awake with presyncope) and Fletcher 2013's absolute contraindication (uncontrolled symptomatic arrhythmia); the stored exercise report (stopped for symptomatic hypotension) agrees; no criterion matches the exercise calls. Drug outputs (initial, fallback, atenolol follow-up) no longer quote LVEF or name complete heart block; the atenolol follow-up still carries action-5's expected evidence (slows escape, CKD 3a accumulation consistent with eGFR about 49, contraindicated without a pacemaker). revision_reason and ruling agree. perfect_agent -v ok, test_case_guards ok. No change.
Pass 5: 0 errors found
- Nothing was changed after the last 0-error pass (pass 4; no condition-audit or orchestrator entry after it). Checks only: perfect_agent -v ok, test_case_guards -k ok. No change.
