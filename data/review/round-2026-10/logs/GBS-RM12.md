# GBS-RM12
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| a2cd5342-e2a0-444d-ae96-622cecab7def | FIXED | One pair chosen and used everywhere: FVC 2.8 L of 4.2 L predicted = 67%, 37 mL/kg at 75 kg (`patient.physical_exam.general` "Weight 75 kg, height 180 cm", BMI 23.1 agrees). `followup_outputs[3]` (respiratory) rewritten canonically: FVC L, MIP -34 cmH2O L, MEP 46 cmH2O L, cough weak; "All values within normal limits" removed. Spirometry removed from `neurological_exam.additional`. Musts 1-2: ICU-level monitoring (bulbar weakness with weak cough) and elective intubation triggers (FVC <20 mL/kg = 1.5 L, MIP weaker than -30, MEP <40, worsening bulbar function). a4 canonical. |
| 39b7526d-309e-44bf-9f6a-8c28786a621f | FIXED (CMV part) / BLOCKED (GT1a criterion) | CMV IgM (with Campylobacter and EBV IgM) deleted from the labs; "post-CMV, probable" removed from `diagnosis.accepted[0]`; "CMV serology and PCR" removed from the must. `anti-GM1 IgM` removed from a1. The ganglioside follow-up is kept, renamed `request_anti_gq1b_gt1a_ganglioside_panel` (anti-GT1a IgG 1:320 positive, anti-GQ1b negative; anti-GM1 row dropped) and probed reachable when the order's context names GT1a, GQ1b or ganglioside; must 6 asks for it. A scored criterion for it cannot be written until the vocabulary has a ganglioside term (plan CENTRAL 1): BLOCKED. |
| 7b88d7ad-6228-4237-9df3-c574b6cfc2e3 | FIXED | MG: repetitive nerve stimulation (ulnar and spinal accessory, no decrement) added to the NCS report; new recommended criterion `action-10-interpret-labs-anti-achr-musk` (`interpret_labs` `anti_AChR`) served by new follow-up `request_achr_musk_antibodies` (AChR 0.02 nmol/L, MuSK negative); MG lowered to low with those reasons. Botulism lowered to low with clinical reasons (normal pupils and eye movements, demyelinating NCS, raised CSF protein, no exposure); a botulinum assay is not in the vocabulary (plan CENTRAL 3). The prohibition that referred to RNS and single-fibre EMG as unavailable is deleted. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.motor` | Legs 4+/5 while the HPI says no leg weakness and the label is PCB (legs spared); no neck weakness although the variant is pharyngeal-cervical-brachial (C4). | FIXED: legs 5/5; neck flexion 3+/5, extension 4/5; HPI adds difficulty holding his head up. |
| B | minor | `patient.neurological_exam.additional` | "Low-grade fever 37.7°C on admission two days ago" while he presents to the ED today; editorial "atypical distribution". | FIXED: field removed (spirometry, timeline error and editorial). |
| D | minor | `patient.history_present_illness` | Editorial reasoning ("that would suggest botulism", "The descending pattern ... is an atypical distribution"), em dashes. | FIXED: exposures stated as history; reasoning sentence deleted. |
| B | minor | `patient.neurological_exam.cranial_nerves` | No pupil exam although botulism is in the differential; em dash. | FIXED: pupils equal and reactive, no ptosis, eye movements full, weak cough. |
| C | minor | `initial_tool_outputs.ecg` | Rate 96 called "sinus tachycardia". | FIXED: normal sinus rhythm, rate 96. |
| C | major | `initial_tool_outputs.labs` | Antecedent serology (CMV, EBV, Campylobacter IgM) and HIV with the leaky clinical_significance sentence; no liver tests, albumin or CK (C3, C10). | FIXED: serology and HIV removed; CMP completed (BUN, calcium, magnesium, ALT, AST, ALP, bilirubin, albumin), CK 164 U/L; CRP 8.4 and ESR 28 kept; interpretation pattern-level. |
| A | major | `followup_outputs` | Barium swallow served as `interpret_labs` (C9); empty literature and DDI placeholders. | FIXED: deleted; the swallow assessment is must 4 (nil by mouth until a formal swallow assessment). |
| C | minor | `followup_outputs[4]` (telemetry) | 72-hour report with a Day 2 nasogastric-tube event (future); "Mild sinus tachycardia throughout" with a minimum of 68; "Mild autonomic tachycardia" interpretive. | FIXED: first 24 h, sinus rhythm 68-104 bpm, blood pressure range; a8 canonical. |
| D | minor | `initial_tool_outputs.specialized_test` | `quantitative_data.pattern` claimed an "axial/bulbar demyelinating pattern" that NCS cannot show; no needle EMG; em dash. | FIXED: pattern "Demyelinating, upper limb predominant, lower limbs spared"; needle EMG (reduced recruitment in cervical and arm muscles, legs normal) and RNS added; impression renumbered. |
| C | major | `ground_truth.differential`, `avoided_actions` | Brainstem lesion in the differential and KCE 4 asking for brain MRI while brain MRI was waste (plan RM12). | FIXED: recommended `action-11-analyze-brain-mri` with a normal `initial_tool_outputs.mri`; waste-4 removed; brainstem lesion very_low. |
| C | major | `ground_truth.assessment` | Generic musts; IVIg without indication in an ambulant patient; generic steroid prohibition. | FIXED: ICU-level, intubation-plan, IVIg (indication: progressive bulbar weakness with aspiration risk, 30 g/day at 75 kg; PE alternative), nil by mouth, telemetry, ganglioside antibodies; prohibitions canonical steroid and renal function. |
| C | major | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule` | Template criteria and constraints (plan section 3). | FIXED: canonical a1-a8, order a2, a3, a10, a11, a1, a4, a8, a7, a6 optional, a5 optional; constraints deleted; stop rule five required, `max_additional_actions` 3. a6 optional (no medications). |
| E | minor | `ground_truth.key_clinical_evidence`, `red_herrings[0].location` | Pearls without the case's data; brain MRI pearl unsupported; RH location was a field path. | FIXED: four pearls with case data [Wakerley_2014, EAN_PNS_2023]; RH location "Neurological examination, motor" and MG resolution added. |
| D | major | `initial_tool_outputs.literature_search` | Scoring-key echo (C11). | FIXED: canonical general output. |
| E | minor | `followup_outputs[0].output.interpretation`, `metadata.difficulty_description` | Em dashes; CSF interpretation without a close. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is now a clean pharyngeal-cervical-brachial GBS: nasal dysarthria, dysphagia with coughing on liquids and a weak cough, neck flexion 3+/5, proximal arm weakness with absent arm reflexes, legs 5/5, normal sensation, CSF protein 72 with 3 cells, and an upper-limb demyelinating NCS with normal leg studies and no decrement on RNS. "Post-CMV" is gone with the CMV, EBV and Campylobacter serology; the label is "Guillain-Barré syndrome, pharyngeal-cervical-brachial variant". Anti-GT1a IgG 1:320 (GQ1b negative) stays as a follow-up reachable by naming ganglioside antibodies; its criterion waits for a vocabulary term. Myasthenia is excluded by a new recommended AChR/MuSK antibody step (negative) plus the RNS, and a brainstem lesion by a new recommended normal brain MRI; botulism is low on clinical grounds. Respiratory values agree (FVC 2.8 of 4.2 L, 67%, 37 mL/kg at 75 kg; MIP -34; MEP 46) and are flagged low; because the cough is weak and he aspirates, the musts are ICU-level monitoring, an elective-intubation plan with named triggers, IVIg for progressive bulbar weakness (PE equivalent), nil by mouth until a formal swallow assessment, and telemetry. The barium swallow "lab" and placeholder steps are deleted.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 1: an `interpret_labs` ganglioside term (anti-GT1a/GQ1b IgG) so the anti-GT1a step can be a recommended criterion (note 39b7526d BLOCKED part).
- Plan CENTRAL 3: `botulinum_toxin_assay` for the botulism mimic.
- `ground_truth.diagnosis.accepted[0]` changed (CMV attribution removed).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: 2.8/4.2 L = 67%, 37 mL/kg at 75 kg, BMI 23.1 agrees with 75 kg / 180 cm, 20 mL/kg = 1.5 L; CMV/EBV/Campylobacter serology and "post-CMV" gone everywhere; anti-GT1a follow-up reachable by clinical_context (probed) and BLOCKED for a criterion per CENTRAL 1 (sound); MG low with RNS and negative AChR/MuSK, botulism low with pupils normal and no exposure, brainstem lesion very_low with the normal MRI served to the new criterion; PCB features met (neck 3+/5, arms weak and areflexic, legs 5/5); IVIg indication (bulbar, ambulant) matches plan section 1.2; telemetry 24 h; ECG rate 96 = vitals.
Found and fixed: `patient.chief_complaint` said "no preceding infection recalled" while the HPI reports a low-grade fever with malaise 10 days before onset. Changed to "Five-day progressive dysphagia and arm weakness with nasal speech; gait preserved." (the HPI is the history; no trigger is named in the label, per C3).
Checks re-run after the verifier's edits: `perfect_agent.py -v` ok (each criterion served by its intended report; labs, brain MRI and ganglioside probes confirmed by a direct MockServer probe where relevant) and `case_io.py check` clean for this case (the remaining failures name GBS-RP16 and GBS-RS16 only).


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- B, minor: `action-7-analyze-ecg` expected_evidence was the condition template ("Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities reflecting autonomic involvement") and the rationale repeated the label, while the ECG shows normal sinus rhythm 96 bpm with QTc 438 ms. Rewritten to what the ECG shows, with the rationale used in RP12, RP14-RP16 (the RP12 verifier had flagged this template in this case).
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels plus "pharyngeal cervical brachial"; AIDP, AMAN and Miller Fisher labels removed.
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)
Terms added in commit e19131d6 (`interpret_labs` `anti_GQ1b_IgG`, `anti_GT1a_IgG`, `botulinum_toxin_assay`; `analyze_csf` `CMV_PCR`), wired per plan C2/C3/C9 and GBS-decisions CENTRAL 1-3. Checks after the change: `perfect_agent.py -v` pass, `case_io.py check` clean for this case, `test_case_guards -k GBS-` 60 passed; optional criteria probed against the MockServer (served the case's own report, not a fallback).

- New `action-12-interpret-labs-anti-gt1a` (recommended; `{panels: [anti_GT1a_IgG]}`), after the AChR/MuSK step, answered by `request_anti_gq1b_gt1a_ganglioside_panel` (GT1a 1:320, GQ1b negative). The criterion names GT1a, the PCB antibody; a GQ1b-only order is served the same report but not credited.
- New `action-13-interpret-labs-botulinum-toxin` (optional; `{panels: [botulinum_toxin_assay]}`) with a new follow-up `request_botulinum_toxin_assay` (serum neurotoxin A, B, E, F not detected), placed after the ganglioside follow-up. Optional: pupils, eye movements, areflexia, demyelinating NCS, raised CSF protein and no exposure already make botulism low. Differential 'Botulism' key_features add "the serum botulinum toxin assay, if sent, is negative" (likelihood stays low).
- Must 6 "Send anti-GT1a and anti-GQ1b IgG antibodies ..." deleted (now a scored criterion; interpretation is in KCE 2); new prohibition "Do not delay IVIg while waiting for the send-out anti-GT1a and anti-GQ1b result."
- Resolves the BLOCKED part of note 39b7526d (CENTRAL 1) and CENTRAL 3.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-6-check-drug-interactions` rationale: "He takes no medicines, so the check cannot change management (ROUND_POLICY ruling 6)." -> "He takes no medicines, so the check cannot change management."
