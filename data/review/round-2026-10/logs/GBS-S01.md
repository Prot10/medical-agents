# GBS-S01
Reviewer status: R1 not reviewed, R2 no notes (counted as approved, plan "Case status") | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for GBS-S01. The changes below are the plan's class fixes (plan S01 entry) and real errors. Correct prose was left as it was. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | The patient block gave the spirometry (FVC 1.8 L, 43%, 22 mL/kg; NIF -24) and "AT INTUBATION THRESHOLD", which are the result of a4 (C1/C7). | FIXED: the HPI says "He is short of breath when lying flat". `additional` now gives clinical signs only: short phrases, accessory muscle use, weak cough. |
| B | major | `patient.history_present_illness` | Timeline: enteritis 2 weeks ago, then tingling "10 days later" after recovery, then 5 days of progression adds up to more than 2 weeks. | FIXED: tingling began 5 days ago, 9 days after the diarrhoea began. The chief complaint (2 weeks, 5 days) now agrees. |
| B | major | `patient.physical_exam.general`, respiratory follow-up | There was no weight. The old FVC pair (1.8 L = 43% of 4.2 L) and 22 mL/kg cannot both hold for a 35-year-old man with BMI 24.1: 22 mL/kg means about 82 kg, hence about 184 cm and a predicted FVC near 5.6 L. | FIXED: weight 82 kg and height 184 cm (BMI 24.2). Predicted FVC 5.6 L, so 1.8 L is 32% and 22.0 mL/kg, and the 4-hour value of 1.4 L is 25% and 17.1 mL/kg. |
| C | major | respiratory follow-up `request_respiratory_monitoring` | FVC 1.4 L, NIF -22 and PaCO2 48 were flagged "(H)" with an "intubation threshold" reference. There was no MEP, no % or mL/kg, and no trend (C1). | FIXED: canonical format with the trend. FVC 1.8 to 1.4 L over 4 h (22% fall). MIP -24 to -22, MEP 34, weak cough. ABG pH 7.34, PaCO2 48, PaO2 72 on room air. Low values are flagged L and PaCO2 H. References follow Evans and Whitelaw 2009. |
| C | major | `initial_tool_outputs.labs` | Campylobacter IgM/IgG and anti-GM1 IgG 1:640 sat in the baseline labs (C2/C3). "FVC 43% predicted - AT THRESHOLD" sat in the lab summary. HIV carried the leaky clinical_significance sentence (C10). There were no liver tests, albumin, glucose or CK. | FIXED: serology and ganglioside results deleted, along with the FVC line. HIV kept with null significance. CMP (glucose 90, consistent with the CSF ratio; liver tests; albumin) and CK added. Interpretation is a plain recital. |
| D | minor | `initial_tool_outputs.specialized_test.quantitative_data` | "Reduced - risk of secondary axonal injury with anti-GM1" was an interpretive and prognostic aside citing another test (plan S01). | FIXED: deleted. The pattern field is rewritten without dashes. A needle EMG line was added (the study is NCS and EMG): reduced recruitment, no denervation. The values are unchanged. |
| A/D | major | ganglioside follow-up `request_anti_ganglioside_panel` | Anti-GM1/GD1a positive, which nothing interpreted, in a typical sensorimotor case (C2). | FIXED: deleted. |
| C | major | telemetry follow-up `request_cardiac_monitoring` | 168 h of monitoring with treatments (atropine, labetalol, vasopressor) and day 2-4 events (C12, ruling 4). | FIXED: the first 24 h only. Sinus tachycardia 104-142, the hour-12 sinus bradycardia to 36 bpm (self-terminating, with no treatment and no suctioning, since he is not yet intubated), BP 128/80 to 186/108, QTc 460-472. a8 expected_evidence is canonical. |
| A | major | `followup_outputs` | Empty literature (`search_gbs_treatment`) and DDI (`check_ivig_drug_interactions`) placeholders (C9). | FIXED: deleted. The pathway order is CSF, respiratory, telemetry. |
| D | major | `initial_tool_outputs.literature_search` | It repeated a5's expected_evidence (C11 leak). | FIXED: canonical population-keyed summary [EAN_PNS_2023, Walgaard_2021]. |
| D/E | minor | `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | The initial block carried an engineering-style warning ("which agents to taper ... is a prescribing decision"). The fallback had "(agent not specified on this case's pathway)". | FIXED: no-medication content with the IVIg renal and succinylcholine warnings. The fallback `proposed` becomes "Medication list review". |
| C | major | `ground_truth.action_criteria` | The template texts (C2, C10, C11, ruling 5/6). | FIXED per plan 3.1. Order a2, a3, a1, a4, a8, a7, a6, a5. a6 optional (no medications) and a5 optional. a7 evidence is case-specific. |
| A | major | `sequence_constraints`, `stop_rule` | Constraints hung on a6 (one tied EMG to DDI for a respiratory reason). The stop rule listed literature and DDI, with `max_additional_actions` 0. | FIXED: constraints removed. The stop rule lists the five required criteria, `max_additional_actions` 3. |
| C | major | `ground_truth.assessment` | "Intubate and mechanically ventilate" gave no reason. "Initiate IVIG / plasma exchange" had no dose. "Do not use neuromuscular blockade outside intubation context" is not the real hazard. The steroid prohibition was the template. There was no swallow must despite dysphagia. | FIXED: ICU admission and elective intubation with the named triggers (FVC <20 mL/kg and falling, MIP, MEP, PaCO2 48, bulbar weakness); IVIg 2 g/kg (about 33 g/day) or PE with the indication; telemetry; nil by mouth until a swallow assessment; DVT prophylaxis; early therapy. Canonical C8 prohibitions, and the succinylcholine prohibition replaces the vague blockade line. |
| C | major | `ground_truth.differential` | AMAN was "moderate" on the strength of the deleted anti-GM1 and "pure motor", while the case has sensory involvement, absent SNAPs and demyelinating-range NCS. Botulism was "low" (ruling 7). | FIXED: AMAN very_low and botulism very_low, with reasons. CIDP stays low. Tick paralysis and CIP stay very_low, with reasons. |
| C | minor | `ground_truth.key_clinical_evidence` | Pearl 2 ("Post-Campylobacter cases warrant repeat EMG for AIDP-vs-AMAN clarification") conflicts with EAN/PNS 2023, which does not advise routine subtyping. | FIXED: four pearls: Brighton level 1, the multi-factor intubation decision, the canonical C3 pearl with the mEGOS diarrhoea point [Walgaard_2011], and autonomic monitoring. |
| A | minor | `avoided_actions[*].citations`, `metadata.difficulty_rationale` | `van_den_Berg_2014`; counts now wrong. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-S01 stays a severe post-Campylobacter AIDP in a 35-year-old man. The label is unchanged, because the antecedent is a prior positive stool culture recorded as history. The patient block no longer gives spirometry, and the onset timeline is consistent: diarrhoea 2 weeks ago, tingling 5 days ago. Weight 82 kg and height 184 cm make the respiratory numbers coherent. The respiratory step now shows FVC 1.8 falling to 1.4 L in 4 h (32% to 25% predicted; 22 to 17.1 mL/kg), MIP -22, MEP 34, PaCO2 48 and a weak cough. The musts make elective intubation in the ICU explicit, with those triggers. They also cover IVIg 2 g/kg or PE, telemetry, nil by mouth until a swallow assessment, DVT prophylaxis and early therapy. Succinylcholine is now prohibited. Campylobacter serology, anti-GM1 and the ganglioside panel are gone. Telemetry covers 24 h with no treatment. Literature and DDI are optional, with general content. AMAN and botulism are lowered for the sensory and demyelinating findings.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 5: weight is in `patient.physical_exam.general`.
- Plan CENTRAL 6: the appended synonyms accept "miller fisher syndrome" and "AMAN" for this AIDP case.

## Open questions for Andrea (judgment calls you could not settle)
None. I decided these myself:
- The predicted FVC is 5.6 L rather than the old 4.2 L, because 22 mL/kg (the plan's anchor) fixes the weight at about 82 kg for BMI 24. The percentages fall as a result (32% and 25%), which strengthens, not changes, the intubation decision.
- The succinylcholine prohibition has no citation, as in M01.

## Verification
Adversarial check, 24 Oct 2026 (approved case). Read the log, the diff and the final patient block, outputs and ground truth.
- No notes; class fixes per plan S01 confirmed: spirometry and "AT INTUBATION THRESHOLD" out of the patient block, weight 82 kg / 184 cm in `physical_exam.general`, Campylobacter serology, anti-GM1 and the ganglioside follow-up gone, label keeps the culture-confirmed antecedent (history), telemetry 24 h without treatment, NCS anti-GM1 aside removed.
- Arithmetic checked: BMI 24.2; FVC 1.8 L = 22.0 mL/kg and 32% of 5.6 L, 1.4 L = 17.1 mL/kg and 25%, fall 22%; MIP and MEP lower limits (-57, 88 cmH2O) match Evans and Whitelaw for a 35-year-old man; CSF:serum glucose 62/90 = 0.69; IVIg 33 g/day at 82 kg. Timeline (diarrhoea day -14, tingling day -5) consistent with the chief complaint.
- Musts, prohibitions and avoided actions do not contradict each other; differential consistent with the final evidence. Nothing changed.
- `perfect_agent.py GBS-S01 -v` passes; `case_io.py check` and `test_case_guards.py -k GBS-S01` clean for the case.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.
- `initial_tool_outputs.specialized_test.test_type` "Nerve Conduction Studies and EMG" -> `emg_ncs`.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
