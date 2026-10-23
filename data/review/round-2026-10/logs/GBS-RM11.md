# GBS-RM11
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 2a09feee-d8ae-4553-a841-33cca7c377e0 | FIXED | `followup_outputs[1]` (respiratory) rewritten in the canonical format: FVC 2.2 L (65% predicted; 33 mL/kg at 67 kg) L, MIP -36 cmH2O L, MEP 52 cmH2O L, cough effective; "All values within normal limits" removed. Weight and height added (`patient.physical_exam.general` "Weight 67 kg, height 165 cm", BMI 24.6 agrees). Must 1 names the ICU-level triggers including FVC <60% predicted and 20 mL/kg (about 1.3 L at 67 kg). a4 label and expected_evidence canonical. Spirometry removed from the HPI and `neurological_exam.additional`. |
| b2c102d6-ed63-4c0c-8b40-436212532917 | FIXED | Kept the unilateral palsy and encoded it as `ground_truth.red_herrings[0]` (Bell's palsy, brainstem lesion, Lyme; resolved by LMN pattern, no long-tract signs, bilateral areflexic weakness, CSF and NCS). Lyme polyradiculitis in the differential now argues from the acellular CSF instead of the deleted Campylobacter serology. Cranial nerve exam rewritten without the editorial "(unilateral). No bilateral facial involvement", with pertinent negatives (eye movements full, no ptosis). |
| ae0f3536-786c-4083-bcd9-2132b3746b6f | FIXED | Pearl 3 replaced by the canonical C2 pearl; ganglioside follow-up (`request_anti_ganglioside_panel`, anti-GM1 IgG 1:80) deleted; `anti-GM1 IgM` removed from a1. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.labs` | Campylobacter IgM in the current-encounter labs (not orderable, not needed; C3); HIV "Non-reactive" with the leaky clinical_significance sentence (C10); no potassium, glucose, liver tests, albumin or CK although a1 expects them. | FIXED: serology and HIV removed; panels CBC (platelets added), CMP (potassium, BUN, glucose, calcium, ALT, AST, ALP, bilirubin, albumin added, all normal), CK 118 U/L, CRP 14.2 kept; interpretation recites only the abnormal value. |
| C | major | `ground_truth.diagnosis.accepted[0]` | "post-Campylobacter" attribution with no culture or orderable serology (C3, class of 6644822c). | FIXED: "Guillain-Barré syndrome (acute inflammatory demyelinating polyradiculoneuropathy) after a diarrheal illness". |
| D | major | `initial_tool_outputs.literature_search` | Output echoed a5's expected_evidence with "guideline recommendation" and bare `van_den_Berg_2014` (C11). | FIXED: canonical general output [EAN_PNS_2023, Walgaard_2021]; a5 optional, last, general expected_evidence. |
| A | major | `followup_outputs` | Empty literature (`search_gbs_treatment`) and DDI (`check_ivig_drug_interactions`) placeholder follow-ups (C9). | FIXED: deleted. Follow-ups now CSF, respiratory, telemetry. |
| C | major | `ground_truth.action_criteria` | Template criteria: a1 required HIV, inflammatory markers and anti-GM1 IgM and expected trigger identification; a3 "cells <10"; a5 literature and a6 DDI required with no medications; criteria not in clinical order. | FIXED: canonical criteria per plan 3.1 in order a2, a3, a1, a4, a8, a7, a6 (optional), a5 (optional); citations [EAN_PNS_2023] and [Lawn_2001] replace "GBS criteria pack §2" strings. |
| B | major | `ground_truth.sequence_constraints`, `stop_rule` | First constraint named EMG for a respiratory reason; second tied labs to an optional DDI; stop rule listed literature and DDI and allowed 0 extra actions. | FIXED: both constraints deleted (a6 is optional); stop rule = the five required criteria, `max_additional_actions` 3. |
| C | major | `ground_truth.assessment` | Musts generic ("Initiate IVIG ... or plasma exchange" without indication, dose basis or ICU triggers); "corticosteroids as monotherapy" and IgA prohibitions (C8). | FIXED: monitored-bed must with named ICU triggers and swallow/cough check (dysarthria); IVIg 2 g/kg (about 27 g/day at 67 kg) with the indication (cannot walk unaided, day 8) and PE alternative; telemetry; LMWH prophylaxis [Leonhard_2019]. Prohibitions: canonical steroid text and renal function before IVIg. |
| C | minor | `initial_tool_outputs.ecg` | QTc 448 ms called "borderline prolonged" in a woman (normal below 460 ms). | FIXED: "Normal intervals (QTc 448 ms)"; "Borderline QTc" finding removed. |
| D | minor | `initial_tool_outputs.specialized_test.quantitative_data.pattern` | "Moderate AIDP" names the disease in a modality field. | FIXED: "Demyelinating polyradiculoneuropathy". |
| B | minor | `initial_tool_outputs.specialized_test` | Report labelled NCS and EMG but carried no needle EMG result; `test_type` in prose. | FIXED: needle EMG finding added (reduced recruitment, no denervation, as expected at day 8), impression item 5; `test_type` "emg_ncs". |
| E | minor | `followup_outputs[0].output.interpretation` | Em dash, sentence without a close. | FIXED: rewritten with "Clinical correlation recommended." |
| C | minor | `followup_outputs[2].output` (telemetry) | 72-hour report running into the future (C12); "Mild autonomic lability" is an interpretation. | FIXED: first 24 h only, the same events (nocturnal sinus bradycardia 52 bpm, sinus tachycardia to 118) plus blood pressure range; a8 expected_evidence canonical. |
| C | major | `ground_truth.differential` | Acute-onset CIDP moderate; Lyme argued from Campylobacter serology now deleted (C5). | FIXED: CIDP low (reassess at 8 weeks); Lyme low with CSF reason; cord compression very_low with reason; CIP "No ICU course before onset". |
| E | minor | `ground_truth.key_clinical_evidence` | Pearl 1 stated Brighton level 1 while she is still progressing; pearl 2 Campylobacter prognosis claim. | FIXED: Brighton level 1 "once the course plateaus within 4 weeks"; pearl 2 diarrhoea history counts in mEGOS [Walgaard_2011]; new pearl 4 on the treatment indication. |
| C | minor | `ground_truth.avoided_actions` | Bare `van_den_Berg_2014` citations; brain MRI waste without case reason. | FIXED: [EAN_PNS_2023]; brain MRI rationale names the LMN facial palsy. |
| E | minor | `metadata.difficulty_rationale` | "6 required tools, 0 red herring(s)". | FIXED. |
| C | minor | DDI decision (plan 3.1 item 7) | No medications. | a6 optional; DDI output warning de-templated ("which agents to taper"). |

## Changes, in one paragraph a physician can read before re-reviewing

The case stays a moderate post-diarrhoeal AIDP with a left lower motor neuron facial palsy; the label no longer names Campylobacter. The patient block no longer gives spirometry or editorial phrases and now records weight 67 kg and height 165 cm. The respiratory step reports FVC 2.2 L (65% predicted, 33 mL/kg), MIP -36, MEP 52 cmH2O, all flagged low, cough effective; she is above the ICU-level triggers, so must 1 is admission to a monitored bed with 4-6 hourly FVC/MIP/MEP and a swallow and cough check, and names the triggers for ICU-level monitoring (FVC <60% or 20 mL/kg, MIP weaker than -30, MEP <40, a fall >30%, bulbar weakness with weak cough). Must 2 gives IVIg 2 g/kg over 5 days now because she cannot walk unaided at day 8 (PE equivalent). The unilateral facial palsy is now the red herring, resolved within the polyradiculoneuropathy. Campylobacter IgM, HIV and the ganglioside panel are gone; the baseline labs now contain liver tests, albumin, glucose, potassium and CK (all normal) with CRP 14.2. Literature and the interaction check are optional and generic; telemetry reports the first 24 hours. Criteria are in clinical order: NCS/EMG, CSF, labs, respiratory, telemetry, ECG, then the two optional look-ups.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `ground_truth.diagnosis.accepted[0]` changed (Campylobacter attribution removed, plan C3); synonyms untouched.
- Plan CENTRAL 5 (weight field in demographics) and 10 (respiratory-report guard) apply.

## Open questions for Andrea (judgment calls you could not settle)

- None. FVC 65% predicted sits above Reviewer 2's 60% ICU trigger, so ICU-level monitoring is named as an escalation trigger rather than a present must (plan open question 2 governs the 60% rule).

## Verification (adversarial verifier, 24 Oct 2026)

Checked every note against the file: respiratory follow-up canonical and flagged L, weight 67 kg / 165 cm agrees with BMI 24.6, FVC 2.2 L = 33 mL/kg, 20 mL/kg = 1.3 L as stated; must 1 names the ICU triggers and she meets none (65%, MIP -36, MEP 52, effective cough), so a monitored bed with escalation triggers is correct. The unilateral LMN facial palsy is the red herring with Lyme low on the acellular CSF. Pearl 3 is the canonical C2 pearl; no ganglioside follow-up or anti-GM1 argument remains. Cross-checked: ECG rate 102 = vitals HR, QTc 448 normal for a woman, IVIg 26.8 g/day at 67 kg, day 8 within 2 weeks, GBS disability 3 (walks with support), no spirometry or results in the patient block, a6/a5 optional, stop rule = the five required criteria, no avoided action matching a criterion. No errors found; no changes made.
Checks re-run after the verifier's edits: `perfect_agent.py -v` ok (each criterion served by its intended report; labs, brain MRI and ganglioside probes confirmed by a direct MockServer probe where relevant) and `case_io.py check` clean for this case (the remaining failures name GBS-RP16 and GBS-RS16 only).


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- B, minor: `action-7-analyze-ecg` expected_evidence was the condition template ("Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities reflecting autonomic involvement") and the rationale repeated the label, while the ECG shows sinus tachycardia 102 bpm with QTc 448 ms. Rewritten to what the ECG shows, with the rationale used in RP12, RP14-RP16 (the RP12 verifier had flagged this template in this case).
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.
