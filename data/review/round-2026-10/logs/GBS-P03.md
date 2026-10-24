# GBS-P03
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 8018be9e-37f0-4fa0-b466-58d5b1c7e7bd | FIXED | The patient is GBS disability grade 1, 3 days from onset, and EAN/PNS 2023 does not advise routine IVIg for mildly affected patients in the first 2 weeks. `assessment.required_recommendations[0]` ("Initiate IVIG ... Brighton level 1-2") is replaced with "Admit for serial respiratory and autonomic monitoring; IVIg is not routinely advised in mildly affected patients within 2 weeks of onset; treat if she loses the ability to walk unaided or develops bulbar, respiratory or autonomic involvement [EAN_PNS_2023]" (plan P03). A must records the disability grade and daily re-examination. The prohibition "Do not delay IVIG/PLEX waiting ..." is deleted. The prohibitions are now: do not exclude GBS on a normal early CSF, do not discharge her as functional, and the canonical steroid prohibition. The literature output and KCE 3 state the same rule. The musts for repeat EMG and repeat LP are deleted. |
| 605dea03-950a-4786-8757-63d98f7ae6d3 | FIXED | The Brighton level is stated once, in `key_clinical_evidence[1]`: level 2 (normal CSF, consistent NCS), provisional because the nadir has not been reached ("nadir within 4 weeks"), and the level does not decide treatment. The "level 1-2" must and the "2-3" pearl are gone. The literature follow-up `request_literature_early_gbs_treatment` with the "12 weeks" claim is deleted. The initial literature output is sourced and says "nadir within 4 weeks" [EAN_PNS_2023, Leonhard_2019]. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B | major | `patient.chief_complaint`, `history_present_illness`, `neurological_exam.motor`, `reflexes` | The case said "no weakness" and "normal strength", yet called her GBS. The reflexes were "trace" in one place and "global areflexia" in another. Capitalised editorials ("NORMAL", "GLOBAL AREFLEXIA in setting of normal strength"). | FIXED (plan P03): mild distal weakness (ankle dorsiflexion and finger abduction 4+/5). Absent Achilles, biceps and triceps reflexes; trace patellar and brachioradialis reflexes. Plain findings. The HPI says she walked to the ED and can still run (grade 1). "NCS was ordered" deleted (C7). The ED functional-disorder suspicion is now in the history. |
| C/D | major | `initial_tool_outputs.labs` | Campylobacter IgM and anti-GM1 IgG were in the current labs (C2, C3). There was no CMP, potassium, liver tests, albumin, glucose, CK or platelets. HIV had the leaky clinical_significance (C10). | FIXED: serology deleted; the culture-confirmed enteritis stays as history. CMP with potassium 4.0 (needed for the periodic-paralysis entry) and glucose 90 (matches the CSF ratio 0.69), liver tests, albumin, platelets and CK 74 added. HIV clinical_significance is null. KCE 5 is the C3 pearl. |
| A/D | major | `followup_outputs` `request_analyze_ecg`, `check_ivig_drug_interactions` | Placeholder ECG and empty DDI template (C9). There was no initial ECG. | FIXED: both deleted. A real normal initial ECG (sinus rhythm 92, QTc 412 ms) serves a7. There are no current medications, so a6 is optional and the initial DDI output has no boilerplate warning. |
| C | major | `action-3-analyze-csf.expected_evidence` | The canonical text expects raised protein, but this CSF has protein 34 mg/dL (normal). | FIXED: "Cells <5/mm3 excluding an inflammatory or infectious cause; protein may still be normal in the first week and does not exclude GBS". The CSF report shows the reference range and its interpretation no longer comments on the diagnosis. |
| C | minor | respiratory follow-up | No weight and no MEP. "NIF -52" had no reference range (C1). | FIXED: weight 57.9 kg and height 163 cm (BMI 21.8). FVC 3.4 L (89%; 58.7 mL/kg), MIP -52 (Evans and Whitelaw 2009 lower limit for a 22-year-old woman, -51), MEP 90 (lower limit 82). All within reference. |
| C | minor | telemetry follow-up | 48 h (C12). | FIXED: the first 24 h, normal sinus rhythm 68-98 bpm, stable blood pressure. a8 expected_evidence is canonical. |
| B | minor | NCS `findings`, `quantitative_data` | "CV 42 m/s (borderline)" with no normal limit. The EMG reported "normal recruitment" despite distal weakness. Em dashes in `quantitative_data`. | FIXED: normal limits added (median CV 42, reduced against >49). Mildly reduced recruitment in tibialis anterior. Plain quantitative fields. |
| C | major | `key_clinical_evidence`, `red_herrings` | KCE said the routine NCS was "NORMAL", but the NCS is abnormal. The red herring "borderline early CSF and EMG" did not match the data (CSF normal, EMG abnormal) (C6). | FIXED: KCE 1 says the absent F-waves and H-reflexes are early abnormalities, as here. Two red herrings: the normal CSF protein at day 3, and the ED functional-disorder suspicion. |
| C | major | `ground_truth.differential` | CIDP was moderate at day 3. Myositis had no case reason. Tick paralysis had no skin examination. AIP relied on urine porphyrins that cannot be ordered. Hypokalaemic periodic paralysis relied on potassium that was not in the labs (C5). | FIXED: acute-onset CIDP low. Functional disorder, myositis (areflexia, CK normal), tick paralysis (full skin and scalp inspection added to the exam), AIP (clinical reasons) and periodic paralysis (potassium normal) very_low. |
| A | major | `action_criteria`, `sequence_constraints`, `stop_rule`, citations | Template structure (plan 3.1, 3.3). | FIXED: order a2, a3, a1, a4, a8, a7, a6, a5; canonical texts; constraints removed; stop rule of five required criteria, max 3; citations are plan keys, including the avoided actions. |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-P03 is early, mild AIDP 3 days after a culture-confirmed Campylobacter enteritis, at GBS disability grade 1. The exam now has mild distal weakness and consistent reflex findings, and the editorial capitals are gone. The scored management follows EAN/PNS 2023: admit and monitor respiratory and autonomic function, no routine IVIg in a mildly affected patient within 2 weeks, and treat on deterioration. The Brighton level is stated once (level 2, provisional) and the 4-week nadir is used throughout. The CSF criterion expects a normal cell count and accepts a normal early protein. The current serology and anti-GM1 results are removed, the labs are completed, and the placeholder ECG and DDI steps are replaced by a real ECG. The respiratory values have a weight and lower limits, and the telemetry covers 24 h. The red herrings are the normal early CSF and the ED suspicion of a functional disorder.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 5 (weight field).

## Open questions for Andrea (judgment calls you could not settle)
- Whether a grade 1 patient should keep the "do not discharge as functional" prohibition. It is clinically right here, but it scores a behaviour that comes from the red herring.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the full diff and the whole final case.
- Note 8018be9e: confirmed (no immunotherapy must; admission and monitoring with treatment on progression, matching EAN/PNS 2023 for grade 1 within 2 weeks; the "do not delay IVIg" prohibition is gone). Note 605dea03: confirmed (Brighton level 2 stated once, consistent with normal CSF plus consistent NCS; "nadir within 4 weeks"; the 12-week literature claim deleted).
- Arithmetic: BMI 21.8; FVC 3.4/3.8 = 89%, 58.7 mL/kg; MIP/MEP limits for a 22-year-old woman (51, 82); CSF 62/90 = 0.69; ECG 92 = vitals. The NCS meets demyelinating features (median CV 86% of LLN, DML 133% and 113% of ULN, absent F-waves). Musts and prohibitions are mutually consistent.
- Open question resolved: the worker asked whether to keep "Do not discharge her as functional". Keep it: EAN/PNS 2023 and Leonhard 2019 advise admission and monitoring of patients in the progressive phase, whatever the severity, because respiratory failure can develop within days; the prohibition scores a real unsafe act, not only the red herring.
- Noted, not changed: the label says "areflexia" while the exam keeps trace patellar and brachioradialis reflexes; GBS requires reduced or absent reflexes, the label is close enough, and ROUND_POLICY forbids relabelling without a ruling.
- No changes made. Checks: `perfect_agent.py GBS-P03 -v` passes; `case_io.py check` reports no failure naming GBS-P03.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- `accepted[0]` "... early AIDP (day 3, areflexia with early electrodiagnostic abnormalities)" -> "... early AIDP (day 3, mildly affected and ambulant, with early electrodiagnostic abnormalities)": the exam keeps trace patellar and brachioradialis reflexes, so "areflexia" was inaccurate (auditor flag).
- Escalation must: "MIP becomes weaker than -30 cmH2O" -> "-40 cmH2O" (EAN/PNS 2023 states MIP <40 cmH2O as the point to consider elective ventilation; the earlier of the Lawn and EAN thresholds governs a monitored-bed patient).
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
