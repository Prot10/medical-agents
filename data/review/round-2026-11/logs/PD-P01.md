# PD-P01

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| caaaca18-6421-457f-b7b3-b7ca2eee2316 | FIXED | ground_truth.avoided_actions: avoid-waste-5-analyze-ecg deleted; ground_truth.action_criteria[1] new recommended ecg-baseline (analyze_ecg {}, [ESC_2018]); initial_tool_outputs.ecg new (moved from fallback_tool_outputs.ecg, sinus 66/min, PR 141, QRS 90, QTc 401 ms); fallback_tool_outputs.ecg set to null so it does not duplicate it. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.action_criteria[0].label, .rationale | PD template text ('MRI is normal in PD and excludes ... the putaminal signs of MSA') in an MSA-P case whose required MRI shows the MDS 2022 putaminal marker | FIXED (label 'Brain MRI for the MDS 2022 MSA markers and to exclude a structural, vascular or other atypical-parkinsonism cause'; rationale on the MSA MRI markers [Wenning_2022][Postuma_2015]) |
| E language | minor | metadata.difficulty_rationale, revision_reason, last_revised | Counted 1 recommended criterion | FIXED (2 recommended: medication review, baseline ECG) |
| C clinical | minor | fallback_tool_outputs.clinical_assessment | A levodopa challenge served if ordered shows a poor acute response (13%) while the case says no chronic trial has been done; an acute challenge is not the MDS 2022 chronic-response criterion, so the label stays probable MSA-P | FLAGGED (no change) |
| E language | minor | ground_truth.action_criteria[1] (ecg-baseline).rationale | 'midodrine or droxidopa planned' overstated REQ[2] ('consider ... if symptoms persist') (pass 2) | FIXED ('under consideration') |

## Changes
As the physician asked, the ECG is no longer counted as diagnostic overuse. A baseline 12-lead ECG is now a recommended step after the MRI, for his recurrent falls, near-syncope and the midodrine or droxidopa under consideration (ESC 2018). The case stores its own normal ECG for it: sinus rhythm 66/min, PR 141, QRS 90, QTc 401 ms, no pre-excitation or conduction block. The MRI criterion's label and rationale now describe what the MRI looks for in suspected MSA (the MDS 2022 putaminal, pontine and cerebellar peduncle markers) instead of PD template text. MRI stays required; the levodopa trial must is unchanged (symptomatic treatment). Holter and echocardiogram stay waste. Checks: perfect_agent.py -v ok; test_case_guards.py for PD-M01, PD-M02, PD-M03, PD-M04, PD-M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (maintained centrally, plan CENTRAL 3) and test_panel_case_contract on PD-RM05 (another worker's case). No MRI report edited (mri_probe run on M01: case MRI served). Not an approved case. Literature (class LIT): no literature criterion or stored literature output in the case (checked).

## Verification
Pass 1: 1 errors found
- Internal contradiction: avoided action avoid-waste-3-order-echocardiogram said 'No murmur, heart failure or exertional symptom', but social_history.exercise reports light-headedness on exertion. Rationale now: 'No murmur, heart failure or exertional syncope: the near-syncope and the light-headedness, including that during exercise, are postural, with a documented neurogenic orthostatic fall, and the echocardiogram does not inform them'. The echocardiogram stays waste.
- D10 checked: ECG recommended after the MRI, stored initial ECG at the case heart rate (66/min), fallback ECG nulled, ECG waste entry gone.
- Checks after the fixes: perfect_agent.py -v ok; test_case_guards.py -k for PD-M01..M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (central, plan CENTRAL 3).
Pass 2: 0 errors found
- Re-checked note caaaca18 (D10): ECG waste entry gone, recommended ecg-baseline after the MRI answered by initial_tool_outputs.ecg (HR 66 = vitals), fallback ECG nulled; MDS 2022 probable MSA-P wording, red-herring field paths and timeline. No material change.
- Cosmetic (not counted): ecg-baseline rationale 'with midodrine or droxidopa planned' now 'under consideration', matching REQ[2] ('consider midodrine or droxidopa if symptoms persist').
- Checks after pass 2: perfect_agent.py -v ok for all six; test_case_guards.py -k for PD-M01..M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (central, plan CENTRAL 3: labs and ECG counts); mri_probe: the case MRI answers every MRI order.
Pass 3: 0 errors found
- Re-read the whole case against D10 and D11: ECG waste entry gone, recommended ecg-baseline after the MRI answered by the stored initial ECG (HR 66 = vitals, fallback ECG nulled), REQ[1] levodopa trial kept; MDS 2022 probable MSA-P (nOH 34/26 at 1 minute and 38/28 at 3 minutes, parkinsonism, supportive postural instability within 3 years and erectile dysfunction before 60), MDS 2015 red-flag count in the PD differential, timeline (onset 18 months, first fall 12 months ago), red-herring field paths, heart-rate arithmetic (68 to 72/min). No change to the case.
- Cosmetic (not counted): the rulings file and the log's Changes paragraph still said 'planned midodrine or droxidopa' after pass 2 changed the criterion to 'under consideration'; both now say 'under consideration'.
- Checks after pass 3: perfect_agent.py -v ok for all six (MRI served from the case slot, confirmed with mri_probe); test_case_guards.py -k for PD-M01..M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (central, plan CENTRAL 3: labs and ECG counts).
- Condition audit (17 Nov 2026): `patient.neurological_exam.motor` described bradykinesia without decrement ('Mild bilateral bradykinesia demonstrated on finger tapping...'). MSA-P (MDS 2022) needs parkinsonism, defined with the MDS 2015 bradykinesia (slowness with decrement). This is the class of note 92ca20f9 (PD-RM04, plan D5), which the plan applied only to PD-labelled cases. Now 'bradykinesia with progressive decrement in amplitude and speed on finger tapping, hand opening/closing, and toe tapping'. No other change. perfect_agent passes; case_io check: no failure names this case apart from the centrally maintained test_guidance_claims.

Pass 4: 0 errors found
Pass 4 (focused verifier, 17 Nov 2026) checked the condition-audit change: `patient.neurological_exam.motor` now documents bradykinesia with progressive decrement in amplitude and speed (MDS 2015 parkinsonism, required by MDS 2022 MSA-P; class of note 92ca20f9, plan D5); it agrees with the symmetric bradykinesia in the evidence lines, the slow rapid alternating movements in coordination and metadata.revision_reason; no field still states bradykinesia without decrement. perfect_agent passes; test_case_guards passes for the case. No change.
