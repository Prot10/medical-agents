# GBS-RM14
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0b90c02f-9ca4-42f3-919a-349b87c851f1 | FIXED | The numbers (DML 7.4-8.8 ms, CV 24-28 m/s) are demyelinating, so the label follows them: `diagnosis.accepted[0]` "Guillain-Barré syndrome (acute inflammatory demyelinating polyradiculoneuropathy), postpartum". NCS `impression` and `quantitative_data.pattern` rewritten as demyelinating; "AMSAN" and "predominantly axonal" removed; pearl 1 explains that low distal CMAPs alone do not make the study axonal. |
| c7fc4320-dbc5-47d8-9bc9-af521f53717a | FIXED | The unsourced claim that plasma exchange interrupts breastfeeding for 24-48 h is deleted from the DDI output (`followup_outputs[4]`); must 4 now says breastfeeding can continue during IVIg and asks for a lactation review of each co-medication, citing [LactMed]; the DDI output states the LactMed position for IVIg, ferrous sulfate and ibuprofen. No plasma-exchange lactation statement remains (no source found). |
| 0ddd925b-9d4d-4ced-bd25-3e9f4ecec9d6 | FIXED | Mild upper limb involvement added consistently: HPI (difficulty fastening buttons and gripping), motor exam (finger abduction 4/5, grip 4/5, about 80%), reflexes (biceps and brachioradialis 1+), NCS (median DML 4.6 ms mildly prolonged, median F-wave 33 ms prolonged, reduced first dorsal interosseous recruitment). "Generalized ... axonal" removed from the pattern field, which now reads lower limb predominant with mild upper limb involvement. |
| 61e678b0-bba0-4d15-be7d-9168e980716c | FIXED | Weight 61 kg, height 160 cm (`patient.physical_exam.general`, BMI 23.8). `followup_outputs[2]` canonical: FVC 2.4 L (75%; 39 mL/kg) L, MIP -36 L, MEP 58 L, change 2.6 to 2.4 L over 8 h (8% fall); "All values within normal limits" removed. Must 2: 4-6 hourly serial monitoring with the weight-based ICU triggers (20 mL/kg = about 1.2 L). Spirometry removed from `neurological_exam.additional`. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | minor | `patient.history_present_illness` | Editorial sentence naming epidural haematoma and abscess as the concern; "She denies any upper limb weakness" against the new arm findings. | FIXED: rewritten to history only (no fever or back pain; breastfeeding stated). |
| B | minor | `patient.neurological_exam.additional` | Spirometry and a repeat of the history. | FIXED: removed. |
| C | major | `initial_tool_outputs.labs` | Antecedent serology (Campylobacter, CMV, EBV) and HIV with the leaky sentence; no liver tests, albumin, glucose or CK. | FIXED: removed; CMP and CK added (all normal), Hb 11.2, CRP 6.8, ESR 42 kept. |
| C | major | `followup_outputs[4]` (DDI) | IgA screen, paracetamol premedication and "IVIG preferred" prescriptions; unsourced PE claim. | FIXED: category-level output: ibuprofen adds IVIg renal risk (relative caution), ferrous sulfate no interaction, LactMed lactation statements, IVIg SmPC adverse effects with postpartum thrombotic risk. |
| C | major | `ground_truth.assessment` | Musts did not state the indication, the window, the ICU triggers or VTE prophylaxis in an immobile postpartum woman. | FIXED: IVIg 2 g/kg (about 24 g/day) with indication (disability score 4) and timing; monitored bed with triggers; telemetry with postural precautions; lactation; LMWH. Prohibitions: canonical steroid, renal function, and the spinal-anaesthesia attribution reworded. |
| C | major | `ground_truth.differential` | Spinal-anaesthesia injury and postpartum CIDP left moderate after the MRI and course exclude them. | FIXED: both low with reasons (MRI, symmetry, hand involvement; 2-week course); B12 and vasculitic very_low; CIP "No ICU course before onset". |
| C | minor | `followup_outputs[3]` (telemetry) | 72-hour report. | FIXED: first 24 h with the Day 1 postural hypotension; a8 canonical. |
| A | major | `followup_outputs` | Anti-GM1/GD1a follow-up (typical sensorimotor GBS) and empty literature placeholder. | FIXED: deleted (C2, C9). |
| A | minor | `action_criteria[2]` (a9) | Citation `[EAN_PNS_GBS_2023]` plus a free-text duplicate; label "only because Recent ..." grammar. | FIXED: [EAN_PNS_2023]; label, rationale and expected evidence rewritten; stays optional. |
| D | major | `initial_tool_outputs.literature_search` | Scoring-key echo. | FIXED: canonical general output; a5 optional, last. |
| C | minor | DDI decision | Medicines: ferrous sulfate, ibuprofen as needed. | a6 recommended: NSAID with IVIg and lactation are concrete but do not gate treatment. |
| C | minor | `ground_truth.action_criteria`, constraints, stop rule | Template. | FIXED: canonical criteria, order a2, a3, a9, a1, a4, a8, a7, a6, a5; constraints deleted; stop rule five required, `max_additional_actions` 3. |
| E | minor | em dashes in `past_medical_history[0]`, CSF and MRI impressions; metadata texts | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

This postpartum case is now a demyelinating GBS throughout: the NCS numbers were already demyelinating and the label, impression and pattern now say so (no AMSAN, not "generalized"). To meet the required limb features she has mild hand weakness (finger abduction and grip 4/5) with arm reflexes 1+ and a mildly abnormal median study, while the legs remain severely weak and areflexic. Weight is 61 kg; FVC 2.6 then 2.4 L (75%, 39 mL/kg), MIP -36, MEP 58 cmH2O are flagged low with an 8% fall, and the must is a monitored bed with 4-6 hourly measurements and named ICU triggers. Treatment is IVIg 2 g/kg now (unable to stand, about 2 weeks from onset; PE equivalent), breastfeeding continues (LactMed), LMWH prophylaxis. The unsourced claim that plasma exchange interrupts breastfeeding is gone. The spinal anaesthetic stays the red herring, resolved by timing, symmetry and the optional contrast spine MRI; both it and postpartum CIDP are now low. Serology, HIV and the ganglioside panel are gone; the interaction check is recommended and category-level; telemetry covers 24 h.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation key `[LactMed]` (NIH Drugs and Lactation Database, immune globulin entry), plan open question 5.
- `ground_truth.diagnosis.accepted[0]` changed from AMSAN to AIDP (label not met by the case's own NCS, note 0b90c02f).

## Open questions for Andrea (judgment calls you could not settle)

- None. Plan open question 5 decided: LactMed is cited for IVIg (its immune globulin entry), and no statement about plasma exchange and breastfeeding is made because I could not source one.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: label AIDP matches the NCS numbers (no AMSAN or "generalized" anywhere); arm involvement propagated to HPI, motor, reflexes, NCS and KCE; FVC 2.4/3.2 L = 75%, 39 mL/kg at 61 kg, BMI 23.8 agrees with 160 cm, 20 mL/kg = 1.2 L, 8% fall; breastfeeding contradiction gone (no PE statement left, LactMed cited for IVIg, ibuprofen, iron; CENTRAL key request logged); timeline (CS 22 days ago, weakness from day 8, about 2 weeks) consistent across HPI, musts, differential and RH; LMWH must consistent with postpartum immobility; telemetry 24 h with the postural hypotension that the must addresses; ECG rate 108 = vitals.
Found and fixed: the CSF report carried an unrequested adenosine deaminase result with a wrong reference ("0-30 U/L"; CSF ADA has no such normal range, values above about 10 U/L are the tuberculous-meningitis cut-off), template carry-over with no clinical question in this case. Deleted `special_tests.ADA` and its sentence from `followup_outputs[0].output.interpretation`.
Checks re-run after the verifier's edits: `perfect_agent.py -v` ok (each criterion served by its intended report; labs, brain MRI and ganglioside probes confirmed by a direct MockServer probe where relevant) and `case_io.py check` clean for this case (the remaining failures name GBS-RP16 and GBS-RS16 only).


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- B, minor: `action-7-analyze-ecg` expected_evidence was the condition template ("Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities reflecting autonomic involvement") and the rationale repeated the label, while the ECG shows sinus tachycardia 108 bpm with QTc 432 ms. Rewritten to what the ECG shows, with the rationale used in RP12, RP14-RP16 (the RP12 verifier had flagged this template in this case).
- B, minor: CSF `special_tests.Culture` and interpretation reported "No growth at 48h" for the lumbar puncture the agent orders at the assessment, a result from the future (same class as the RS14 verifier's fix). Now "No growth to date".

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Respiratory follow-up: MIP -36 -> -42 cmH2O and the earlier value -38 -> -44 cmH2O (flagged L against -60), same reason as M03; escalation must "MIP becomes weaker than -40 cmH2O".
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
