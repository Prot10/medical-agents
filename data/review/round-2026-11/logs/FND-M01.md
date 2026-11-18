# FND-M01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| f20dfdfa | FIXED (class LIT) | No literature criterion or output left (checked). |
| ccddb06a | FIXED (VEEG, STOP) | ground_truth.action_criteria[4] action-5-analyze-eeg optional to recommended, rationale and citations canonical (October 'Without the recording...' sentence deleted); not in the stop rule; the test is a recommended criterion, and actions matching a criterion are never counted as extra (policy_reward.py, stopping); display: CENTRAL C1. |
| f4d98130 | FIXED (ECG) | ground_truth.action_criteria[1] action-ecg optional to required, canonical label, rationale, citation [NICE_CG109] (NG217 dropped), expected_evidence; initial_tool_outputs.ecg new case ECG; fallback_tool_outputs.ecg null; metadata.fallback_tool_kinds.ecg removed; stop_rule.required_before_assessment = exam, ECG. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | minor | ground_truth.action_criteria; followup_outputs | Order did not follow 2.ORDER (EEG and drug check before labs and MRI; performance status before neuropsychology). | FIXED: exam, ECG, labs, MRI, video-EEG, drug check, neuropsychology; follow-ups neuropsychology then performance status. Ids unchanged. |
| E | minor | metadata.revision_reason | Said 'video-EEG optional', now false. | FIXED: updated to the November tiers; last_revised 2026-11-16. |
| C | major | metadata.clinical_pearls[1] | Pearl defined entrainment as a tremor that 'takes on the rhythm ... or stops'; a tremor that only stops shows suppression or distractibility (class ENTRAIN, plan F8). | FIXED (verifier pass 1): pearl now states the distinction. |
| B | major | ground_truth.avoided_actions avoid-waste-3-order-cardiac-monitoring.rationale | Rationale listed 'preserved responsiveness' as a reason the events are not syncopal, contradicting the HPI (partner: apparent unresponsiveness), the video-EEG event 2 and the required ECG rationale (apparent loss of responsiveness). | FIXED (verifier pass 1): '(eyes tightly closed, rhythmic shaking for up to three minutes, rapid recovery without confusion)'. Waste label kept. |
| B | major | ground_truth.key_clinical_evidence[2]; ground_truth.differential[0].key_features | Both generalized 'preserved responsiveness' to all her events, contradicting the partner's account of apparent unresponsiveness, video-EEG event 2 and the required ECG rationale (same defect pass 1 fixed in the cardiac-monitoring rationale). | FIXED (verifier pass 2): responsiveness preserved during the event observed on examination; witnesses describe apparent unresponsiveness in others. |

## Changes
FND-M01 (35-year-old woman, functional seizures with functional right leg weakness and tremor). The 12-lead ECG is now a required step and in the stop rule, because her events include apparent unresponsiveness (NICE CG109); it is answered by a new case-specific ECG (sinus rhythm 90/min, PR 158 ms, QRS 86 ms, QTc 434 ms, no pre-excitation, Brugada pattern or heart block) instead of the template 'Normal ECG'. The video-EEG is now recommended rather than optional, with the ILAE 2013 / AAN 2025 rationale (an event was witnessed on examination; the recording documents the diagnosis and screens for co-occurring epilepsy); it is credited but not mandatory and is never counted as an extra action. The stop rule is now examination plus ECG. The criteria and follow-ups were reordered to the clinical sequence (examination, ECG, labs, MRI, video-EEG, medicine review, neuropsychology; performance status last). No literature step remains. Diagnosis, musts, prohibitions and differential are unchanged.

## Verification
Pass 1: 2 errors found
- metadata.clinical_pearls: entrainment pearl said 'or stops' (class ENTRAIN, F8); corrected.
- avoided_actions avoid-waste-3-order-cardiac-monitoring: 'preserved responsiveness' contradicted the apparent unresponsiveness on which the required ECG rests; reworded.
- Re-checked after the fixes: perfect_agent.py passes, test_case_guards -k passes.
Cosmetic (not counted): action-neuropsych-battery rationale said the battery 'costs more than any other step on this pathway', but it is priced as the video-EEG (1104 each in costs.yaml); now 'costs as much as the video-EEG'
Pass 2: 1 errors found
- key_clinical_evidence[2] and differential[0] (epileptic seizures) said the events have 'preserved responsiveness', contradicting the witnessed apparent unresponsiveness on which the required ECG rests; now limited to the observed event.
- Re-checked after the fix: perfect_agent.py passes, test_case_guards -k passes.
Cosmetic (not counted): none.
Pass 3: 0 errors found
- None. Checked: rulings against plan (LIT, VEEG recommended, ECG required); stop rule exam and ECG; ECG rate 90 vs HR 91, QTc 354/sqrt(0.667) = 434 ms; responsiveness wording consistent across HPI, KCE, differential and the cardiac-monitoring rationale; drug check holds its own content; no leakage.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case; the only FND failure is FND-RS02).
Cosmetic (not counted): none.
Pass 4: 0 errors found
- None. Checked: rulings of f20dfdfa, ccddb06a, f4d98130 against plan 3 (LIT; VEEG recommended, out of the stop rule; ECG required); stop rule exam + ECG, both required; ECG rate 90 vs HR 91, QT 354 ms gives Bazett QTc 434 ms; responsiveness wording consistent across HPI, exam, KCE, differential and avoided actions; entrainment genuine (tremor takes on the cued rhythm); drug check carries its own content; no leakage; no new em dash.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case).
- For the lead (not counted, not changed): the neuropsychology battery numbers (MoCA 28/30, RAVLT z = -0.2, Trail B z = -0.4, TOMM 49/50) are identical in 23 FND cases, a condition-wide template carry-over outside this batch's plan.
Cosmetic (not counted): none.
Condition audit (17 Nov 2026): 1 error found
- B (consistency, report internal), minor: in `followup_outputs[request_neuropsych_battery]`, `quantitative_data.GAD-7` was labelled "15 (moderately severe)" and the finding and impression said "moderately severe anxiety". GAD-7 bands are 0-4 minimal, 5-9 mild, 10-14 moderate and 15-21 severe (Spitzer 2006); "moderately severe" is a PHQ-9 band. FIXED: "15 (severe)" and "severe anxiety". The score is unchanged. This case keeps the cognitive values (MoCA 28/30, RAVLT z = -0.2, Trail Making B z = -0.4, TOMM 49/50) that the audit changed in the 21 other FND cases that shared them. Every questionnaire label in the condition was then checked against its bands (GAD-7, PHQ-9, PHQ-15, HADS, BDI-II, BAI): no other mismatch.
- Re-checked: perfect_agent.py FND-M01 passes.
Pass 5: 0 errors found
- None. Checked the condition-audit fix: GAD-7 15 now labelled 'severe' (Spitzer 2006 bands) in `quantitative_data`, the mood finding and the impression, which agree; PHQ-9 11 'moderate' matches its band; the cognitive values kept (MoCA 28/30, RAVLT z = -0.2, Trail B z = -0.4, TOMM 49/50) are normal and now unique to this case; no other field of the case states the anxiety severity.
- Re-checked: perfect_agent.py -v passes; test_case_guards -k (all 8 FND pass-5 cases) 64 passed.
Cosmetic (not counted): none.
