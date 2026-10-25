# GBS-RP13
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 9fee5e3b-336c-4934-9753-945eec5ee2c9 | FIXED | One time point per field: `patient.neurological_exam` is now the hospital day 2 examination (HPI says so), with reflexes biceps/triceps/brachioradialis 1+, knee 1+, ankle absent, flexor plantars, no Hoffmann sign. The normal 2+ reflexes are stated only in the HPI as the admission (day 1) examination, and kept as red herring 3 ("Reflexes can be preserved in the first days of GBS"). The conditional must ("Initiate IVIG ... if areflexia and CSF dissociation present") deleted; must 2 now gives IVIg on the real indication (cannot walk unaided, still progressing, within 2 weeks). The NCS report no longer cites a day-1 NCS or day-1 H-reflexes that the case never contained. |
| e7f671d6-6bae-4ec1-8f3c-ea42e39cf75e | FIXED | New recommended criterion `action-10-order-body-imaging-spine-mri` (contrast spine MRI; reason: known cervical stenosis with asymmetric left hand symptoms, asymmetry makes GBS less likely [EAN_PNS_2023]) served by follow-up `request_spine_mri_contrast` (moderate degenerative narrowing at C5-C6 and C6-C7 without cord compression or signal change; smooth cauda equina root enhancement). Differential: "Cervical spondylotic myelopathy or radiculopathy" very_low with the reasons; red herrings 1 (cervical stenosis and chronic right foot drop) and 2 (wake-up onset with AF) added, each resolved. The left hand asymmetry is kept but made relative: grip and finger abduction 4/5 left, 4+/5 right, tingling of the right fingertips, so the case meets "bilateral, relatively symmetric". The chronic right foot drop is now explained in the history (right peroneal neuropathy at the fibular head on a 2019 NCS) and separated in the NCS report. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `followup_outputs` brain MRI | Brain MRI served under `order_advanced_imaging` (`order_mri_brain`, C9) while `analyze_brain_mri` was listed as waste although the HPI says she was admitted for brain MRI after a wake-up stroke alert. | FIXED: report moved to `initial_tool_outputs.mri` (MRIReport: no acute infarct, chronic small vessel change, no brainstem lesion or enhancement); new recommended criterion `action-11-analyze-brain-mri`; brain MRI removed from waste. Stroke in the differential as very_low with the normal DWI. |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | Editorial sentences ("Critically ... this mismatch raised concern", "multiple background diagnoses ... could individually explain", "lacked the classic ascending paralysis pattern"); exam `additional` repeated the HPI (C7). | FIXED: HPI rewritten as history with a clear day 1 / day 2 timeline and pertinent negatives (no neck or back pain, no bladder change, no bulbar or respiratory symptoms); `additional` now carries the day 2 Romberg finding. |
| C | major | `initial_tool_outputs.labs` | HIV with the leaky clinical_significance (C10); Campylobacter and CMV IgM (C3); B12, folate and TSH inside "BMP"; TSH unit mIU/mL; no creatinine, glucose, liver tests, albumin, platelets or CK although a1 expects them; ESR flagged against a 0-20 range in a 75-year-old woman. | FIXED: serology and HIV removed; CBC with platelets, CMP, CK 96 added (normal); B12/folate under Vitamins, TSH under Endocrine (mIU/L); ESR reference 0-30 (women over 50), still flagged at 32; INR kept (AF, not anticoagulated). |
| A | major | `followup_outputs` | Ganglioside follow-up (anti-GD1b 1:40) in a sensorimotor case (C2); empty literature placeholder (C9); DDI follow-up with management and a false interaction ("Citalopram + IVIG: QTc risk additive"; IVIg does not prolong QT) and "GBS" named in the drug check. | FIXED: ganglioside and literature follow-ups deleted; DDI moved to `initial_tool_outputs.drug_interactions`, category-level (propranolol and autonomic bradycardia/hypotension; solifenacin retention and QT warning; citalopram QT with the 20 mg maximum over 60; amlodipine and PE; atorvastatin none; no anticoagulant on the list; IVIg thrombotic risk). a6 required (plan; propranolol and solifenacin interact with autonomic involvement, and the absent anticoagulant clears the LP). |
| D | major | `initial_tool_outputs.literature_search` | Echoed a5's expected_evidence (C11). | FIXED: canonical general output; a5 optional and last. |
| C | minor | `initial_tool_outputs.specialized_test` | Pattern field "Sensory-predominant AIDP evolving" named the disease; no peroneal motor study although the foot is weak; no needle EMG; `test_type` in prose referencing a day-1 study absent from the case. | FIXED: left peroneal motor (demyelinating), right peroneal (chronic fibular-head neuropathy as in 2019), needle EMG added; pattern "Demyelinating sensorimotor polyradiculoneuropathy"; comparison with the 2019 study only; `test_type` "emg_ncs". |
| C | minor | `initial_tool_outputs.ecg` | QTc 442 ms in a woman called "borderline"; "citalopram may contribute" (cross-modality). | FIXED: "QTc 442 ms (normal)"; PR "Not measurable (atrial fibrillation)"; a7 expected_evidence case-specific. |
| C | minor | `followup_outputs` respiratory, telemetry | Respiratory "All values within normal limits" with no MIP/MEP or weight, predicted FVC 3.0 L implausible for a 158 cm 75-year-old woman; telemetry 72 h (C12). | FIXED: FVC 2.3 L (88% predicted; 34 mL/kg at 68 kg), MIP -46, MEP 72 cmH2O, all within reference (no flags); weight 68 kg, height 158 cm (BMI 27.2) in `physical_exam.general`; telemetry 24 h, AF 64-96 bpm, BP 124/72 to 158/90 mmHg; a4 and a8 canonical. |
| C | major | `ground_truth.assessment` | "Repeat EMG/NCS at 7-14 days if borderline" (the NCS is not borderline), "Broader panels (paraneoplastic, Sjogren) if atypical" (no criterion; not indicated after the NCS), conditional IVIg, generic telemetry; "corticosteroids as monotherapy" (C8). | FIXED: monitored bed with ICU triggers; IVIg 2 g/kg (about 27 g/day at 68 kg) with the indication; telemetry with propranolol review; post-void residuals and solifenacin; LMWH prophylaxis and an oral anticoagulation plan for the AF after the LP. Prohibitions: canonical steroid text, do not withhold immunotherapy for sensory predominance, renal function before IVIg. |
| C | major | `ground_truth.differential` | Ganglionopathy and acute-onset CIDP moderate after an NCS that shows motor demyelination (C5); no stroke or cervical entry although the case raises both; diabetic neuropathy listed in a non-diabetic. | FIXED: ganglionopathy low (motor conduction slowing), CIDP low, B12 very_low (384 pg/mL), cervical and stroke very_low with reasons; diabetic entry removed. |
| B | minor | `followup_outputs[0]` CSF | Culture "Pending"; placeholder "N/A PMN/N/A lymph"; em dash. | FIXED: "No growth to date"; interpretation rewritten. |
| C | minor | `ground_truth.avoided_actions` | Template rationales; CT waste ignores the CT/CTA already done; bare `van_den_Berg_2014`. | FIXED: case-specific rationales (CT done, echo belongs to the outpatient AF work-up); citations [EAN_PNS_2023]. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | Template constraints and stop rule (literature required, 0 extra actions). | FIXED: soft a1 -> a6 kept with a real reason; stop rule = six required criteria, `max_additional_actions` 3. |
| C | minor | C13 check | Plan asked to check for an anticoagulant (new AF). | No anticoagulant or antiplatelet on the list, INR 1.1, platelets 254: no hard labs-before-LP constraint needed; stated in the DDI output and a6. |

## Changes, in one paragraph a physician can read before re-reviewing

A 75-year-old woman (68 kg) woke with left hand numbness and tingling feet, was triaged as a stroke (CT/CTA negative, outside the thrombolysis window) and on day 2 has spreading sensory loss, mild bilateral distal weakness (left more than right), reflexes depressed or absent and a positive Romberg sign; the day 1 normal reflexes are now history only. The work-up is NCS/EMG (demyelinating sensorimotor polyradiculoneuropathy, separate from her chronic right peroneal neuropathy), CSF (protein 54 mg/dL, 4 cells), brain MRI (no infarct), a contrast spine MRI for the known cervical stenosis (no cord compression), complete baseline bloods, normal respiratory function (FVC 88%, 34 mL/kg), 24-hour telemetry in rate-controlled AF, ECG and a required interaction check (propranolol, solifenacin, citalopram; no anticoagulant). The assessment admits her to a monitored bed with ICU triggers, gives IVIg 2 g/kg because she cannot walk unaided, reviews propranolol and solifenacin against autonomic involvement, and plans DVT prophylaxis and AF anticoagulation after the LP. Cervical stenosis, wake-up onset with AF, and the normal first-day reflexes are the red herrings. Ganglioside and infection serology are gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 5 (weight field) applies.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: both note ids present. Exam is the day 2 exam with reflexes 1+ / ankle absent, normal day 1 reflexes only in the HPI and as red herring 3; no conditional must. Spine MRI criterion and follow-up (moderate C5-C7 narrowing, no cord compression or signal change), cervical and stroke differentials very_low with reasons, red herrings resolved; brain MRI moved to `initial_tool_outputs.mri` with a recommended criterion and removed from waste. a6 required with real content (propranolol, solifenacin, citalopram 20 mg ceiling over 60, no anticoagulant, INR 1.1, platelets 254, so no hard labs-before-LP needed). Arithmetic: BMI 68 / 1.58^2 = 27.2, 2.3 L / 68 kg = 34 mL/kg, CSF ratio 62/89 = 0.70. ECG criterion text matches the AF ECG. No antecedent serology, HIV, ganglioside or editorial residue.

Found: nothing that needed a change.

Checks run after the edits: `perfect_agent.py -v` passes (every required and recommended criterion served by its own report), `case_io.py check` clean for the case (schema, synonym guard, no test failure naming it), `test_case_guards.py` leak, follow-up and banned-string guards pass.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Escalation must: "MIP becomes weaker than -30 cmH2O" -> "-40 cmH2O" (EAN/PNS 2023 MIP <40).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

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

- criterion `action-6-check-drug-interactions` rationale: "Her beta-blocker and antimuscarinic interact with the autonomic involvement of GBS and change monitoring and dosing; confirming that no anticoagulant is taken clears the lumbar puncture (ROUND_POLICY ruling 6)." -> "Her beta-blocker and antimuscarinic interact with the autonomic involvement of GBS and change monitoring and dosing; confirming that no anticoagulant is taken clears the lumbar puncture."

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 65.3 -> 68 kg, height 155 -> 158 cm, BMI 27.2 -> 27.2 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 68 kg, height 158 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3 (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 and a working patient; she cannot walk independently, with sensory ataxia and distal weakness.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: severely impaired gait and balance: walks only with one-person assistance, positive romberg sign (berg 24/56); timed tests not completed (followup_outputs[4] request_gait_and_balance_timed). Why: rule 1: the library reports a normal timed gait and balance assessment; she walks only with one-person assistance and the Romberg sign is positive.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no tremor or rigidity; motor items limited by weakness, response not assessable (followup_outputs[5] request_levodopa_challenge). Why: rule 1: the library describes a normal motor examination, gait and postural reflexes; distal weakness, bilateral foot drop and sensory ataxia.
- `order_body_imaging {study: peripheral_nerve_MRI}`: smooth enhancement and mild T2 hyperintensity of the lumbosacral roots, no enlargement (fallback_tool_outputs.body_imaging). Why: rule 1 and 3: the library reads the nerve roots as normal; root enhancement as on the spine MRI of this case (stored spine MRI: smooth enhancement of the cauda equina roots).
- `order_body_imaging {study: spine_CT}`: moderate degenerative canal narrowing at C5-C6 and C6-C7 (followup_outputs[6] request_spine_ct). Why: rule 2 and 3: cervical canal stenosis is in the history and on the stored spine MRI; the library reports no stenosis.
- `order_specialized_test {test_type: nerve_biopsy}`: segmental demyelination with macrophage infiltration and sparse T-lymphocytes; reduced myelinated fibre density (fallback_tool_outputs.specialized_test). Why: rule 3: the stored nerve conduction study shows absent sural sensory responses (present in 2019) and sensory slowing in the arms with a demyelinating pattern; the library sural biopsy is normal.
- `order_specialized_test {test_type: ssep}`: delayed, attenuated peripheral and proximal responses; central conduction normal where measurable (followup_outputs[7] request_ssep). Why: rule 3: the stored nerve conduction study shows absent sural and reduced median and ulnar sensory responses with sensory slowing, and the Romberg sign is positive; the library reports normal SSEPs.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: active standing not performed (cannot stand without one-person assistance); supine BP 144/86 mmHg, HR 80 bpm (irregular); sitting BP 138/84 mmHg, HR 86 bpm (irregular) (followup_outputs[8] request_orthostatic_blood_pressure). Why: rule 3: she cannot stand without assistance and is in atrial fibrillation; the library reports 3 minutes of symptom-free standing at a supine heart rate of 68.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Post-cholecystectomy. Otherwise normal abdominal and pelvic ultrasound (followup_outputs[9] request_pelvis_abdomen_ultrasound). Why: rule 2: colon adenocarcinoma resected in 2015 and a cholecystectomy are in the history; the library reports a normal gallbladder and unremarkable bowel.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Post-surgical changes of prior segmental colectomy and cholecystectomy. No mass, recurrence or lymphadenopathy (followup_outputs[10] request_pelvis_abdomen_ct). Why: rule 2: colon adenocarcinoma resected in 2015 and a cholecystectomy are in the history; the library reports a normal gallbladder and unremarkable bowel.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Post-surgical changes of prior segmental colectomy and cholecystectomy. No mass lesion or lymphadenopathy (followup_outputs[11] request_pelvis_abdomen_mri). Why: rule 2: colon adenocarcinoma resected in 2015 and a cholecystectomy are in the history; the library reports a normal gallbladder and unremarkable bowel.
- `order_body_imaging {study: chest_abdomen_pelvis_CT}`: Post-surgical changes of prior segmental colectomy and cholecystectomy. No mass, recurrence or lymphadenopathy. Chest clear (followup_outputs[12] request_chest_abdomen_pelvis_ct). Why: rule 2: colon adenocarcinoma resected in 2015 and a cholecystectomy are in the history; the library reports a normal gallbladder and unremarkable bowel.
- Case fallback replaced, `analyze_brain_mri` (fallback_tool_outputs.mri): no acute abnormality; scattered chronic small vessel white matter change. Why: rule 3: the stored brain MRI shows chronic small vessel ischaemic change; the old fallback read a normal brain.
- `order_body_imaging {study: chest_CT}`: no thoracic abnormality; post-cholecystectomy clips (followup_outputs[13] request_chest_ct). Why: rule 3: cholecystectomy is in the history; without its own report this order received the chest-abdomen-pelvis report, which describes the colectomy and pelvis.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
