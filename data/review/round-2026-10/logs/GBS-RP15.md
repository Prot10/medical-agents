# GBS-RP15
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 442f0e51-6754-4fe5-a785-0af4ea5a8ae8 | FIXED | Chose "downgrade to a preference with the reason stated". The DDI follow-up that called plasma exchange "CONTRAINDICATED ... IVIG is the only appropriate treatment" was deleted; the interaction check is now `initial_tool_outputs.drug_interactions`, category-level: tacrolimus is largely erythrocyte- and protein-bound and little is removed by PE (check troughs), central-line infection risk on triple immunosuppression as a relative caution. Must 2 says PE is equally effective and not contraindicated, IVIg is the practical first choice because it avoids central access [EAN_PNS_2023]; pearl 2 rewritten to match; `metadata.difficulty_description` no longer says PE is contraindicated. |
| cfa3beb7-266a-49de-aaba-dd681716dc75 | FIXED | Course rewritten to meet the required features: onset 12 days ago with steady progression (cane at day 4, now support from two people), distal paraesthesias from day 5, hand weakness over the last 3 days; reflexes normal at clinic 10 days ago and depressed now (the "week 1 / week 3" exam time points and "total duration about 4 weeks, insidious" are gone). Arms now involved: shoulder abduction 4+/5, grip 4+/5, biceps and brachioradialis 1+. NCS no longer "asymmetric left greater than right" (bilateral, symmetric, with peroneal motor added). Acute-onset CIDP stays low with the 8-week reassessment; "within 2 weeks of onset" now holds for IVIg. |
| 0a7f2022-ff9e-4a61-aa25-1e4d627b0a66 | FIXED | `followup_outputs[1]` (respiratory) in the canonical format: FVC 2.2 L (65% predicted; 28 mL/kg at 80 kg) L, MIP -34 cmH2O L, MEP 58 cmH2O L, cough effective. Weight and height added (`patient.physical_exam.general` "Weight 80 kg, height 174 cm", BMI 26.4 agrees). No ICU trigger is met yet, so must 1 is a high-dependency bed with 4-6 hourly measurements and names every ICU-level trigger (FVC <60% or <20 mL/kg, about 1.6 L; MIP weaker than -30; MEP <40; >30% fall; bulbar weakness with weak cough). a4 canonical. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment` | Valganciclovir 900 mg daily with creatinine 1.4 mg/dL (Cockcroft-Gault about 59 mL/min at 80 kg, age 66): the label prophylaxis dose for CrCl 40-59 is 450 mg daily; nothing in the case caught it. | FIXED: must 4 (renal dose with the transplant team); DDI output and a6 expected_evidence name it. |
| C | major | `ground_truth.assessment` | Musts: "adjust immunosuppression cautiously" (contradicts the prohibition), IVIg "preferred" without dose or renal precautions, "CMV PCR (serum and CSF) and EBV PCR" already in the history and labs, "pharmacology review" as a must; "corticosteroids as monotherapy" (C8). | FIXED: high-dependency monitoring with ICU triggers; IVIg 2 g/kg (about 32 g/day at 80 kg) with sucrose-free product, slow infusion, hydration and daily creatinine; continue immunosuppression unchanged with transplant team, trough and magnesium; valganciclovir renal dose; telemetry; LMWH. Prohibitions: no reduction of immunosuppression, no corticosteroids for GBS (maintenance prednisone continues), renal function before IVIg. |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | Editorial "raised concern for a tacrolimus-related polyneuropathy (tacrolimus can cause demyelinating neuropathy)"; exam `additional` repeated trough statistics, CMV/EBV results, a brain MRI result and the course (C7). | FIXED: HPI is history only; prior blood CMV/EBV PCR kept as dated history (clinic visit 10 days ago); brain MRI mention removed (not scored, waste); `additional` holds orthostatic dizziness and no sphincter dysfunction. |
| C | major | `initial_tool_outputs.labs` | HIV with the leaky clinical_significance (C10); blood CMV/EBV PCR and urine BK PCR in the current labs (duplicating the history); no sodium, glucose, liver tests, albumin or CK. | FIXED: HIV and virology removed; CMP (sodium, BUN, glucose 132 H on prednisone, calcium, liver tests, albumin) and CK added; tacrolimus trough under "Drug levels"; interpretation recites values only. |
| A | major | `followup_outputs` | Ganglioside follow-up (C2) and empty literature placeholder (C9). | FIXED: deleted. |
| D | major | `initial_tool_outputs.literature_search` | Echoed a5's expected_evidence (C11). | FIXED: canonical general output; a5 optional and last. |
| C | minor | `initial_tool_outputs.specialized_test` | Pattern field argued against toxic neuropathy (refutation in a modality field); nerves listed as left only; no needle EMG; `test_type` "(Week 3)". | FIXED: bilateral nerves, peroneal motor and needle EMG added; pattern "Demyelinating polyradiculoneuropathy with reduced CMAP amplitudes"; `test_type` "emg_ncs". |
| B | minor | `followup_outputs[0]` CSF | Placeholder "N/A PMN/N/A lymph"; no cytology although PTLD is in the differential. | FIXED: interpretation rewritten; cytology "no malignant cells" added; CSF glucose 80 mg/dL with ratio 0.61 against serum glucose 132. CSF CMV PCR kept in the stored report (not orderable separately, CENTRAL 4). |
| C | minor | `initial_tool_outputs.ecg` | QTc 442 ms in a man called "borderline"; "tacrolimus may prolong QT" in the ECG findings (cross-modality). | FIXED: normal intervals. |
| C | minor | `followup_outputs` telemetry | 72-hour report (C12); no blood pressure despite orthostatic dizziness. | FIXED: 24 h, sinus 68-96 bpm, BP 104/62 to 152/90 mmHg lowest after sitting up; a8 canonical. |
| C | major | `ground_truth.differential` | Tacrolimus toxicity, PTLD and CMV polyradiculitis moderate after a work-up that addresses them (C5); CIP low without an ICU course. | FIXED: tacrolimus neuropathy low (immune-mediated, troughs in range), CMV very_low (prophylaxis, PCR negative in blood and CSF, 2 cells), PTLD very_low (EBV negative, cytology negative, symmetric), CIP very_low, acute-onset CIDP low. |
| C | minor | `ground_truth.action_criteria` a6 | Template text (IgA, "confirmation IVIG can be given safely"). | FIXED: required (plan; tacrolimus nephrotoxicity with IVIg, valganciclovir renal dosing, PE handling) with a case-specific label; soft a1 -> a6 kept with a real reason. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | a2 -> a6 template constraint; stop rule with literature and 0 extra actions. | FIXED: constraint deleted; stop rule = six required criteria, `max_additional_actions` 3. |
| E | minor | `patient.clinical_history.past_medical_history` | "COPD (post-transplant, chronic management)" after bilateral lung transplant for COPD; em dash. | FIXED: one entry, "Bilateral lung transplant 4 months ago for end-stage COPD, uncomplicated postoperative course". |

## Changes, in one paragraph a physician can read before re-reviewing

A 66-year-old man (80 kg) 4 months after bilateral lung transplantation on tacrolimus, mycophenolate and prednisone has 12 days of steadily progressive leg-predominant weakness, now with mild arm weakness, distal paraesthesias, depressed reflexes and orthostatic dizziness; the insidious 4-week course and the week 1 / week 3 exam time points are gone. The work-up returns a symmetric demyelinating NCS, CSF protein 76 mg/dL with 2 cells (CMV PCR and cytology negative), labs with creatinine 1.4 and magnesium 1.6 and a tacrolimus trough in range, respiratory function FVC 2.2 L (65%, 28 mL/kg), MIP -34, MEP 58 cmH2O, 24-hour telemetry, ECG and a required check of the transplant regimen. The assessment admits him to a high-dependency bed with ICU triggers, gives IVIg 2 g/kg with renal precautions as the practical first choice (plasma exchange equally effective and not contraindicated, but needs central access on triple immunosuppression), keeps the immunosuppression unchanged with the transplant team, adjusts valganciclovir to his renal function, and adds telemetry and DVT prophylaxis. Tacrolimus neuropathy, CMV polyradiculitis and PTLD are now low or very low with reasons.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 4 (CSF `CMV_PCR` special test): the stored CSF report carries a CMV PCR result that no order can request specifically.
- Plan CENTRAL 5 (weight field) and 10 (respiratory-report guard) apply.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: all three note ids present. PE now "not contraindicated", a preference for IVIg with the reason, aligned in must 2, KCE 2 and the DDI output (tacrolimus little removed by PE). Course 12 days with arm weakness and depressed arm reflexes; NCS bilateral and symmetric. Respiratory canonical (2.2 L / 80 kg = 28 mL/kg; BMI 80 / 1.74^2 = 26.4); no ICU trigger met, so the high-dependency must with triggers is right. Cockcroft-Gault (140 - 66) x 80 / (72 x 1.4) = 59 mL/min, so the valganciclovir 450 mg daily must is correct; CSF ratio 80/132 = 0.61; prior CMV/EBV PCR dated history; no residual serology, HIV or ganglioside text.

Found and fixed:
- B, minor: a7 expected_evidence and rationale were the template while the ECG is normal sinus rhythm 86 with QTc 442 ms. Rewritten to what the ECG shows.

Checks run after the edits: `perfect_agent.py -v` passes (every required and recommended criterion served by its own report), `case_io.py check` clean for the case (schema, synonym guard, no test failure naming it), `test_case_guards.py` leak, follow-up and banned-string guards pass.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- `accepted[0]` "... AIDP (post-lung transplant, likely immune dysregulation)" -> "Guillain-Barré syndrome, AIDP, after lung transplantation" (speculative mechanism removed).
- Respiratory follow-up: MIP -34 -> -46 cmH2O (still flagged L against the -80 reference), so a case designed as a monitored-bed case does not sit in the band where EAN/PNS 2023 (MIP <40) would call for considering elective ventilation; escalation must now "MIP becomes weaker than -40 cmH2O".
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)
Terms added in commit e19131d6 (`interpret_labs` `anti_GQ1b_IgG`, `anti_GT1a_IgG`, `botulinum_toxin_assay`; `analyze_csf` `CMV_PCR`), wired per plan C2/C3/C9 and GBS-decisions CENTRAL 1-3. Checks after the change: `perfect_agent.py -v` pass, `case_io.py check` clean for this case, `test_case_guards -k GBS-` 60 passed; optional criteria probed against the MockServer (served the case's own report, not a fallback).

- New `action-9-analyze-csf-cmv-pcr` (optional; `{special_tests: [CMV_PCR]}`), after the CSF criterion, answered by the stored CSF report (CMV PCR not detected). Optional: valganciclovir prophylaxis, a negative blood CMV PCR and 2 cells/mm3 already make CMV polyradiculitis very unlikely, but in a transplant recipient the order is reasonable and must not count as unjustified. Closes CENTRAL 4 for this case.

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

- criterion `action-6-check-drug-interactions` rationale: "A nephrotoxic calcineurin inhibitor with IVIg, a renally dosed antiviral and immunosuppressant handling during plasma exchange change how treatment is given (ROUND_POLICY ruling 6)." -> "A nephrotoxic calcineurin inhibitor with IVIg, a renally dosed antiviral and immunosuppressant handling during plasma exchange change how treatment is given."
