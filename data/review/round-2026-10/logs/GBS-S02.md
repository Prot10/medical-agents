# GBS-S02
Reviewer status: R1 not reviewed, R2 approved (with one note) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 4021807f-930a-4d1a-87c6-f44df643af6a | FIXED | Plan C3 / S02. The EBV VCA IgM result is deleted from `initial_tool_outputs.labs` (and from its summary and interpretation). The antecedent is now the upper respiratory infection given in the history, named in KCE 1, with the canonical C3 pearl as KCE 4. The trigger-identification requirement is gone: `action-1-interpret-labs` now uses the canonical label and evidence, with no "trigger identification (Campylobacter, CMV, EBV, Mycoplasma, HIV)" and no stool culture or serology. The label names no trigger and stays unchanged. The GD1b ganglioside follow-up is deleted (C2). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | The HPI gave "FVC at triage 1.6 L", and the exam gave FVC 1.6 L (52%) and NIF -26 with "Approaching intubation threshold" (C1/C7). | FIXED: the HPI says she is short of breath lying flat. `additional` gives clinical signs only: short sentences, weak cough, mild accessory muscle use. |
| C | major | respiratory follow-up `request_respiratory_monitoring` | FVC 1.4 L and NIF -24 were flagged "(H)" with "threshold -25" as the reference. There was no weight, mL/kg, MEP or trend (C1). | FIXED: weight 70.5 kg and height 164 cm in `physical_exam.general` (BMI 26.2; predicted FVC 3.1 L fits a 44-year-old woman of 164 cm). The triage values move here: FVC 1.6 L (52%, 22.7 mL/kg), then 1.6 to 1.4 L (45%, 19.9 mL/kg) over 3 h, MIP -26 to -24, MEP 38, weak cough, all L. |
| A/D | major | repeat NCS follow-up `request_repeat_ncs` | A "Repeat NCS at day 10" showing secondary axonal injury reports a study from the future of a day-6 assessment. It also answered the index EMG/NCS order (guard `test_index_order_is_not_answered_by_a_repeat_followup` failed for S02). | FIXED: deleted. Nothing scores a repeat NCS, and the label does not use "axonal". |
| C | major | telemetry follow-up `request_cardiac_monitoring` | 120 h of monitoring, with a day-2 labetalol treatment (C12, ruling 4). | FIXED: the first 24 h only. Sinus tachycardia 100-138, the night-1 bradycardia to 40 during turning, BP 118/72 to 178/104, QTc 452-466. a8 expected_evidence is canonical. |
| C | major | `initial_tool_outputs.labs` | HIV carried the leaky clinical_significance sentence (C10). There were no liver tests, albumin, glucose or CK. | FIXED: HIV with null significance. CMP (glucose 88, consistent with the CSF ratio 0.68; liver tests; albumin) and CK added. |
| A/D | major | `followup_outputs` | Empty literature (`search_gbs_treatment`) and DDI (`check_ivig_drug_interactions`) placeholders, and a GD1b ganglioside panel nothing interpreted (C2, C9). | FIXED: deleted. The pathway order is CSF, respiratory, telemetry. |
| D | major | `initial_tool_outputs.literature_search` | It repeated a5's expected_evidence (C11 leak). | FIXED: canonical population-keyed summary [EAN_PNS_2023, Walgaard_2021]. |
| D/E | minor | `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Engineering-style warning in the initial block, and "(agent not specified on this case's pathway)" in the fallback. | FIXED: no-medication content that names the penicillin allergy as not relevant, with IVIg renal and succinylcholine warnings. The fallback `proposed` becomes "Medication list review". |
| B | minor | `initial_tool_outputs.specialized_test`, CSF follow-up | The NCS had no needle EMG although titled NCS and EMG. CSF RBC had no unit and the interpretation had a dash aside. | FIXED: needle EMG line (reduced recruitment, no denervation) and flags on the abnormal values. The values are unchanged. CSF text in report voice. |
| C | major | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule` | The template criteria, constraints hung on a6, and `max_additional_actions` 0. | FIXED per plan 3.1. Order a2, a3, a1, a4, a8, a7, a6, a5. a6 optional (no medications) and a5 optional. No constraints. The stop rule lists the five required criteria, `max_additional_actions` 3. |
| C | major | `ground_truth.assessment` | "Intubate" gave no reason, IVIg had no dose, the steroid prohibition was the template, and there was no swallow must despite coughing on water. | FIXED: elective intubation in the ICU with the triggers named (FVC 19.9 mL/kg, MIP -24, MEP 38, bulbar weakness, weak cough); IVIg 2 g/kg (about 28 g/day) or PE with the indication; telemetry; nil by mouth until a swallow assessment; DVT prophylaxis; therapy. Canonical C8 prohibitions plus succinylcholine. |
| C | major | `ground_truth.differential` | Acute-onset CIDP and AMAN/AMSAN were "moderate". AMAN rested on the deleted antibody. CIP said "ICU course raises risk" with no ICU course. Cord compression said "MRI excludes" with no MRI (ruling 7). | FIXED: CIDP low; AMAN/AMSAN, CIP, botulism and cord compression very_low, each with the finding from the case. |
| C | minor | `ground_truth.key_clinical_evidence` | Pearl 3 (repeat EMG for AIDP vs axonal subtyping) is against EAN/PNS 2023, which does not advise routine subtyping. Pearl 1 was a single-threshold statement. | FIXED: Brighton level 1 with the URI antecedent; the multi-factor intubation decision; autonomic monitoring kept; canonical C3 pearl. |
| A | minor | `avoided_actions[*].citations`, `metadata.difficulty_rationale` | `van_den_Berg_2014`; counts now wrong. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-S02 stays a severe post-URI AIDP in a 44-year-old woman, and the label is unchanged. The EBV IgM and the GD1b panel are gone. The antecedent is the history alone, and nothing asks the agent to identify a trigger. The patient block no longer gives spirometry. The respiratory step shows FVC 1.6 falling to 1.4 L in 3 h (19.9 mL/kg at 70.5 kg, 45% predicted), MIP -24, MEP 38 and a weak cough. The musts make elective intubation in the ICU explicit with those triggers. They also cover IVIg 2 g/kg or PE, telemetry, nil by mouth until a swallow assessment, DVT prophylaxis and therapy, and succinylcholine is prohibited. The day-10 repeat NCS (a future study) is deleted. Telemetry covers 24 h without treatment. The labs gain liver tests, albumin, glucose and CK. Literature and DDI are optional, with general content. CIDP, AMAN and the other mimics are lowered with reasons.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 5: weight is in `patient.physical_exam.general`.
- Plan CENTRAL 6: the appended synonyms accept "miller fisher syndrome" and "AMAN" for this AIDP case.

## Open questions for Andrea (judgment calls you could not settle)
None. The succinylcholine prohibition has no citation, as in M01.

## Verification
Adversarial check, 24 Oct 2026 (approved case). Read the log, the diff and the final case content.
- Note 4021807f: confirmed fixed (EBV IgM gone from the labs and their summary; a1 canonical with no trigger identification; antecedent is the URI history; GD1b follow-up deleted; label unchanged).
- Arithmetic checked: BMI 26.2; FVC 1.6 L = 22.7 mL/kg and 52% of 3.1 L, 1.4 L = 19.9 mL/kg and 45%, fall 13%; MIP and MEP lower limits (-40, 70 cmH2O) match Evans and Whitelaw for a 44-year-old woman; CSF:serum glucose 60/88 = 0.68; IVIg 28 g/day at 70.5 kg. The penicillin allergy is not contradicted by any must.
- Deletion of the day-10 repeat NCS is correct (future study; guard failure). Nothing changed.
- `perfect_agent.py GBS-S02 -v` passes; `case_io.py check` and `test_case_guards.py -k GBS-S02` clean for the case.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.
- `initial_tool_outputs.specialized_test.test_type` "Nerve Conduction Studies and EMG" -> `emg_ncs`.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'not_applicable', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
