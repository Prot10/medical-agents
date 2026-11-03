# GBS-S03
Reviewer status: R1 not reviewed, R2 approved (with one note) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 3c94e91e-ec7a-4812-8d8a-81013bf1c4dd | FIXED | I took the reviewer's second option (stop calling the attribution confirmed), per plan C3 / S03. The HPI now reads "a bloody diarrhoeal illness 3 weeks ago, lasting 5 days (no stool culture obtained)". "Consistent with Campylobacter ... presentation classic" is gone. The Campylobacter IgM/IgG result is deleted from `initial_tool_outputs.labs`. `action-1-interpret-labs` no longer asks for stool culture or serology. The label names no organism and is unchanged. KCE 1 and 4 treat the diarrhoea as history and say it counts for mEGOS [Walgaard_2011]. A stool culture was not added: stool culture is not in the vocabulary (plan CENTRAL 2), and the guideline does not need it for the diagnosis. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional`, `chief_complaint` | The patient block gave the spirometry (FVC 1.9 L, 41%; NIF -20) with "INTUBATION THRESHOLD CROSSED", and the chief complaint had the editorial "respiratory failure imminent" (C1/C7). | FIXED: the clinical signs stay (SpO2 92%, respiratory distress, short phrases, accessory muscles, weak cough). The numbers and the editorial phrases are deleted. |
| B | minor | `patient.history_present_illness` vs `neurological_exam.motor` | "Now cannot move his legs at all", while the exam gives hip and knee 2/5. | FIXED: "can barely move his legs". |
| C | major | `patient.neurological_exam.motor` | There was no arm strength, so the four-limb pattern could not be checked (plan S03). | FIXED: shoulder abduction 3/5, elbow flexion 3+/5, grip 3+/5 bilaterally, consistent with the severity. |
| C | major | respiratory follow-up `request_respiratory_monitoring` | "1.9 L (post-intubation - confirmed pre-intubation at 1.9 L)" and a post-intubation PaCO2, while the patient is not yet intubated at assessment. FVC was flagged H, with no MIP, MEP or weight (C1). | FIXED: the ED values, before intubation: FVC 1.9 L (41% of 4.6 L; 26.6 mL/kg at 71.5 kg), MIP -20, MEP 30, weak cough. The ABG (PaCO2 52, PaO2 62), formerly in the labs, moves here. Weight and height are in `physical_exam.general` (BMI 22.8; height 177 cm fits the predicted 4.6 L). |
| C | major | `initial_tool_outputs.labs` | Campylobacter serology (C3). The HIV leaky sentence (C10). An ABG inside the routine labs, with interpretive summary text ("CO2 retention", "hypoxemia"). No liver tests, albumin, glucose or CK. | FIXED: serology deleted; HIV with null significance; ABG moved to the respiratory report; CMP (glucose 87, consistent with CSF ratio 0.67; liver tests; albumin) and CK added. |
| A/D | major | ganglioside follow-up `request_anti_ganglioside_panel` | Anti-GM1 1:1280 and GD1a positive, uninterpreted, in a typical sensorimotor case (C2). | FIXED: deleted. |
| C | major | telemetry follow-up `request_cardiac_monitoring` | 240 h of monitoring with transvenous pacing, nitroprusside and day 3-8 events (C12, ruling 4). | FIXED: the first 24 h only. Sinus tachycardia 96-148, BP 112/70 to 198/114 settling spontaneously, QTc 470-486, no pauses. a8 expected_evidence is canonical. |
| D | major | literature follow-up `request_literature_gbs_prognosis` | Case-specific prognosis figures with no source ("60-70% walk at 1 year", "5% mortality", "High anti-GM1 titers ... independently associated"), echoing the deleted antibody (C11). | FIXED: deleted. There is now an initial literature output (there was none) with population-keyed, sourced evidence: IVIg/PE [EAN_PNS_2023], no second course [Walgaard_2021], mEGOS components [Walgaard_2011]. a5 is optional and last. |
| A/D | minor | DDI follow-up `check_ivig_drug_interactions`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | An empty placeholder follow-up, an engineering-style warning, and "(agent not specified ...)". | FIXED: follow-up deleted; no-medication content with IVIg renal and succinylcholine warnings; fallback `proposed` "Medication list review". |
| B | minor | CSF follow-up | RBC had no unit, and the interpretation had a dash aside. | FIXED: report voice, with reference ranges. The values are unchanged. |
| C | major | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule` | The template criteria, constraints hung on a6, and `max_additional_actions` 0. | FIXED per plan 3.1. Order a2, a3, a1, a4, a8, a7, a6, a5. a6 and a5 optional. No constraints. The stop rule lists the five required criteria, `max_additional_actions` 3. |
| C | major | `ground_truth.assessment` | "Intubate" gave no reason, IVIg had no dose, and the steroid prohibition was the template. | FIXED: immediate intubation in the ICU, with the reason that respiratory distress with hypoxaemia and hypercapnia means intubation whatever the numbers, plus the MIP, MEP and FVC values; IVIg 2 g/kg (about 28.5 g/day) or PE with the indication; telemetry; DVT prophylaxis; therapy. Canonical C8 prohibitions plus succinylcholine. |
| C | major | `ground_truth.differential` | CIDP and AMAN/AMSAN were "moderate", with AMAN resting on the deleted antibodies. CIP said "ICU course raises risk". Cord compression said "MRI excludes" with no MRI. | FIXED: CIDP low; AMAN/AMSAN low (the CMAPs are markedly reduced, consistent with the label's secondary axonal injury, but the conduction values are demyelinating and sensory responses are absent); CIP, botulism and cord compression very_low, with reasons. |
| C | minor | `ground_truth.key_clinical_evidence` | Pearl 3 (repeat EMG for subtyping) is against EAN/PNS 2023, and pearl 1 was a single statement without data. | FIXED: Brighton level 1; intubation on clinical distress with the numbers; autonomic monitoring kept; canonical C3 pearl with mEGOS. |
| A | minor | `avoided_actions[*].citations`, `metadata.difficulty_rationale` | `van_den_Berg_2014`; counts now wrong. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-S03 stays a severe AIDP with secondary axonal features in a 28-year-old man after a bloody diarrhoeal illness, and the label is unchanged. The diarrhoea is history only: "no stool culture obtained", no Campylobacter claim and no serology. The patient block keeps the clinical signs of respiratory distress without spirometry. The exam now gives arm strength (3/5 to 3+/5). The respiratory step shows the pre-intubation ED values: FVC 1.9 L (41%, 26.6 mL/kg at 71.5 kg), MIP -20, MEP 30, weak cough and ABG PaCO2 52 / PaO2 62. The musts make immediate intubation in the ICU explicit. They also cover IVIg 2 g/kg or PE, telemetry, DVT prophylaxis and therapy, and succinylcholine is prohibited. Telemetry covers 24 h without pacing or nitroprusside. The ganglioside panel is gone. The literature output is general and sourced, with no case-specific prognosis figures. The labs gain liver tests, albumin, glucose and CK. CIDP and AMAN are lowered with reasons.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 2: stool culture is not orderable, so the reviewer's first option (obtain the culture in a step) is not available. It is also not needed (EAN/PNS 2023).
- Plan CENTRAL 5: weight is in `patient.physical_exam.general`.
- Plan CENTRAL 6: the appended synonyms accept "miller fisher syndrome" and "AMAN" for this AIDP case.

## Open questions for Andrea (judgment calls you could not settle)
None. The succinylcholine prohibition has no citation, as in M01.

## Verification
Adversarial check, 24 Oct 2026 (approved case). Read the log, the diff and the final case content.
- Note 3c94e91e: confirmed fixed (HPI "no stool culture obtained", no Campylobacter claim, serology deleted, a1 canonical, label names no organism).
- Arithmetic checked: BMI 22.8; FVC 1.9 L = 26.6 mL/kg and 41% of 4.6 L; MIP and MEP lower limits (-58, 94 cmH2O) match Evans and Whitelaw for a 28-year-old man; CSF:serum glucose 58/87 = 0.67; IVIg 28.5 g/day at 71.5 kg. The must to intubate now rests correctly on distress, hypoxaemia and hypercapnia rather than on the FVC (26.6 mL/kg).
- Arm strength added per plan; respiratory values pre-intubation; telemetry 24 h without pacing or nitroprusside.
- Noted, not changed: the NCS output has no needle EMG line, unlike the other cases of this batch; the criterion's expected evidence does not need it and the case is approved, so no change.
- `perfect_agent.py GBS-S03 -v` passes; `case_io.py check` and `test_case_guards.py -k GBS-S03` clean for the case.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "ICU continuous telemetry" -> `telemetry`.
- `initial_tool_outputs.specialized_test.test_type` "Nerve Conduction Studies" -> `emg_ncs`.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'not_applicable', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 73.1 -> 71.5 kg, height 179 -> 177 cm, BMI 22.8 -> 22.8 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 71.5 kg, height 177 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 30, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 and a working patient; he cannot lift his legs off the bed and is in respiratory distress.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: unable to walk; timed gait and balance tests not performed (followup_outputs[3] request_gait_and_balance_timed). Why: rule 1: the library reports a normal timed gait and balance assessment; he cannot walk or lift his legs off the bed (hip flexion 2/5).
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no tremor or rigidity; motor items limited by weakness, response not assessable (followup_outputs[4] request_levodopa_challenge). Why: rule 1: the library describes a normal motor examination, gait and postural reflexes; leg weakness 1-2/5 and arm weakness 3/5.
- `order_body_imaging {study: spine_MRI}`: smooth enhancement of the cauda equina roots, ventral more than dorsal; normal cord (fallback_tool_outputs.body_imaging). Why: rule 1: smooth enhancement of the cauda equina and ventral roots is seen in most patients with this polyradiculoneuropathy (Gorson 1996; Byun 1998), while the library reads the roots as normal.
- `order_body_imaging {study: peripheral_nerve_MRI}`: smooth enhancement and mild T2 hyperintensity of the lumbosacral roots, no enlargement (followup_outputs[5] request_peripheral_nerve_mri). Why: rule 1 and 3: the library reads the nerve roots as normal; root enhancement as on the spine MRI of this case.
- `order_specialized_test {test_type: nerve_biopsy}`: segmental demyelination with prominent secondary axonal degeneration; reduced myelinated fibre density (fallback_tool_outputs.specialized_test). Why: rule 3: the stored nerve conduction study shows absent sural sensory responses and markedly reduced CMAP amplitudes with secondary axonal injury with a demyelinating pattern; the library sural biopsy is normal.
- `order_specialized_test {test_type: speech_language_evaluation}`: mild flaccid dysarthria; language normal (followup_outputs[6] request_speech_language_evaluation). Why: rule 1 and 3: bilateral facial diplegia with mild dysarthria is in the examination; the library reports no dysarthria.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: active standing not performed (cannot stand); supine BP 156/100 mmHg, HR 124 bpm; sitting BP 148/98 mmHg, HR 132 bpm (followup_outputs[7] request_orthostatic_blood_pressure). Why: rule 3: he cannot stand and the stored telemetry shows sinus tachycardia 96-148 bpm with blood pressure 112/70-198/114 mmHg; the library reports 3 minutes of symptom-free standing at a supine heart rate of 68.
- `order_specialized_test {test_type: autonomic_testing}`: reduced cardiovagal function, distal sudomotor impairment and labile blood pressure on tilt (followup_outputs[8] request_autonomic_testing). Why: rule 3: sinus tachycardia 96-148 bpm with marked blood pressure lability 112/70-198/114 mmHg on the stored telemetry
- `order_specialized_test {test_type: tilt_table}`: Abnormal head-up tilt: resting tachycardia with labile blood pressure; no sustained orthostatic hypotension or vasovagal response (followup_outputs[9] request_tilt_table). Why: rule 3: sinus tachycardia 96-148 bpm with marked blood pressure lability 112/70-198/114 mmHg on the stored telemetry
- `interpret_labs {panels: [ABG]}`: pH 7.33 (low), pCO2 52 mmHg (elevated), pO2 62 mmHg (low), SaO2 91% (low); HCO3 27.1 mmol/L (fallback_tool_outputs.labs['ABG']). Why: rule 3: the stored respiratory assessment records PaCO2 52 mmHg and PaO2 62 mmHg on room air; the library reports normal gases.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
