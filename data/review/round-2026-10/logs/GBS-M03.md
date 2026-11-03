# GBS-M03
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 38ccdb70-95de-45cf-a8b2-90ae9d840ff2 | FIXED | Respiratory follow-up `request_respiratory_monitoring` rewritten in the canonical format with the low flags: FVC 2.4 L (67% predicted; 33.2 mL/kg at 72.3 kg) L, MIP -35 cmH2O L, MEP 62 cmH2O L, cough effective. Weight 72.3 kg and height 163 cm added in `patient.physical_exam.general` (BMI 27.2). The spirometry is removed from `patient.neurological_exam.additional`. |
| 4d885b61-9917-46f5-bff1-71edfd6450cf | FIXED | Of the two options (interpret or remove) I took removal: the ganglioside follow-up with anti-GD1b positive 1:80 is deleted. EAN/PNS 2023 does not advise ganglioside testing in typical sensorimotor GBS, and MFS is not suspected (no ophthalmoplegia or ataxia). `anti-GM1 IgM` and "variant typing" are removed from `action-1-interpret-labs`. |
| 40837d83-a9d7-4f45-9c41-11b33a4d1760 | FIXED | Mycoplasma pneumoniae IgM (positive) and Campylobacter serology are deleted from `initial_tool_outputs.labs`. The antecedent stays the URI in the history. The canonical C3 pearl is added as KCE 5. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history.past_medical_history[0]` | Diabetes was "diet-controlled" while he takes metformin 500 mg twice daily. | FIXED: "Type 2 diabetes mellitus on metformin". |
| B | minor | `patient.history_present_illness` | The URI was 2 weeks before presentation, and symptoms began "on the third day of recovery" (about 6 days ago), which does not fit a 10-day history. | FIXED: URI 3 weeks before; numbness "about 6 days after it resolved". |
| D | major | `patient.neurological_exam.additional` | Spirometry values and an editorial sentence in the exam (C1/C7). | FIXED: clinical respiratory signs only. |
| B/D | major | `followup_outputs` `request_repeat_ncs` | The "Repeat NCS at day 14" was a future result, and it answered the index `emg_ncs` order (the repeat-study guard failed for M03). | FIXED: deleted; nothing in the case depends on it. |
| B | major | CSF follow-up | CSF glucose 62 with ratio 0.67 implied a serum glucose of 92, but the serum glucose is 142 (true ratio 0.44, which would read as low). | FIXED: CSF glucose 88 mg/dL, ratio 0.62; units; report voice. |
| D | minor | `initial_tool_outputs.specialized_test.quantitative_data` | "Superimposed on pre-existing diabetic neuropathy" and "background neuropathy complicates interpretation" cited the history inside the NCS report (style guide prohibition 1). | FIXED: pattern and proximal-involvement fields only. The median CMAP has its limit, normal limits are added to the peroneal values, and a needle EMG line is added. |
| C | major | `initial_tool_outputs.labs` | No liver tests, albumin or CK; no platelets; HIV with the leaky clinical_significance (C10). | FIXED: a CMP with liver tests and albumin, platelets, CK 142, HIV with null significance; interpretation and summary rewritten. |
| C | major | `ground_truth.differential` | "Acute worsening of diabetic polyneuropathy" was high, CIDP moderate, and Lyme cited a serology the case does not contain (C5; plan M03). | FIXED: diabetic worsening low with its reason (acute four-limb weakness, areflexia, facial and bulbar weakness, CSF dissociation, demyelinating NCS; amyotrophy is asymmetric and painful). CIDP low. Lyme and DKA very_low with reasons from the case. |
| C | major | `key_clinical_evidence[3]` | "Aggressive infection or DKA workup should accompany the GBS workup": not indicated (plan M03). | FIXED: glucose monitoring and metformin adjustment. KCE 1 states Brighton level 1 once. KCE 3 is tied to the actual creatinine (1.1). |
| C | major | `assessment` | There was no level-of-care detail, no swallow must despite dysphagia and a diminished gag, and no dose or indication for IVIg. The prohibition cited "diabetic nephropathy" that the case does not contain. The steroid text was the template (C8). | FIXED: a monitored high-dependency bed with serial FVC, MIP and MEP and named ICU triggers (this patient is below none of them: 67% predicted, 33 mL/kg, MIP -35, effective cough). IVIg 2 g/kg (about 29 g/day) or PE with the indication and hydration. A swallow must, a glucose/metformin must, telemetry and DVT prophylaxis. The canonical prohibitions, plus the diabetic-misattribution prohibition reworded. |
| C | major | telemetry follow-up | 96 h, with events on Day 3 (C12). | FIXED: the first 24 h with the same two events; a8 expected_evidence is canonical. |
| D | major | `initial_tool_outputs.literature_search`, `followup_outputs` | The literature output echoed a5. Empty literature and DDI follow-ups (C9, C11). | FIXED: canonical literature output; placeholders deleted; DDI initial output gives category-level metformin content (AKI with IVIg, relative caution). |
| A | major | `action_criteria`, `sequence_constraints`, `stop_rule`, `avoided_actions` citations | Template structure (plan 3.1, 3.3). | FIXED: order a2, a3, a1, a4, a8, a7, a6 (optional: metformin has no interaction that changes the work-up or treatment choice), a5 (optional). Constraints removed. Stop rule of five required criteria, max 3. Citation keys updated. |
| E | minor | `initial_tool_outputs.ecg.interpretation` | "Sinus tachycardia. Borderline QTc." had no rate and no value. | FIXED: rate 104, QTc 452 ms. |
| C | minor | respiratory follow-up `findings[*].reference_range` | The old MIP reference read as an intubation threshold, and there was no MEP reference. | FIXED: MIP and MEP reference ranges are the age- and sex-specific lower limits of normal from Evans and Whitelaw 2009 (Respir Care 2009;54:1348-1359; men: MIP 62-0.15 x age, MEP 117-0.83 x age; women: MIP 62-0.50 x age, MEP 95-0.57 x age). |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-M03 is AIDP after a URI in a man with mild diabetic neuropathy. It now states metformin-treated diabetes and has a timeline that fits the 10-day history. The Mycoplasma IgM, Campylobacter serology, the GD1b ganglioside panel and the future day-14 repeat NCS are deleted. The respiratory step is flagged low and reported with weight (FVC 2.4 L, 67%, 33.2 mL/kg; MIP -35; MEP 62; cough effective). Because no ICU trigger is met, the must is a monitored bed with serial measurements and named escalation triggers. IVIg is dosed by weight with hydration. Swallow and glucose/metformin musts are added. The CSF glucose ratio agrees with the serum glucose 142. The NCS report no longer cites the history. Diabetic neuropathy as the cause of the acute syndrome is lowered to low, with the findings that exclude it. Telemetry covers the first 24 h. Literature and DDI are optional and general.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 5 (weight field) and 6 (variant synonyms in an AIDP case) apply.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the full diff and the whole final case.
- Notes 38ccdb70, 4d885b61, 40837d83: confirmed fixed (FVC flagged L in the canonical format with weight; no ganglioside follow-up or "variant typing"; no Mycoplasma or Campylobacter serology; C3 pearl present).
- Arithmetic re-checked: timeline (URI 21 to 16 days ago, numbness 6 days later = 10 days ago); BMI 27.2; FVC 2.4/3.6 = 67%, 33.2 mL/kg; 20 mL/kg = 1.45 L; MIP/MEP limits for a 58-year-old man (53, 69); CSF 88/142 = 0.62; IVIg 29 g/day. No ICU trigger is met (MIP -35, MEP 62, effective cough), so the high-dependency must with named escalation triggers is consistent with the data. Differential matches the work-up.
- Found and fixed: `red_herrings[0].data_point` named "mildly elevated HbA1c", which sits in the labs, not at the stated `field_path` (`patient.clinical_history.past_medical_history`). Rewritten to "Known diabetic peripheral neuropathy, diagnosed 2 years ago".
- Checks: `perfect_agent.py GBS-M03 -v` passes; `case_io.py check` reports no failure naming GBS-M03.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- B, minor: `action-7-analyze-ecg` expected_evidence was the condition template ("Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities reflecting autonomic involvement") and the rationale repeated the label, while the ECG shows sinus tachycardia 104 bpm with QTc 452 ms. Rewritten to what the ECG shows, with the rationale used in RP12, RP14-RP16 (the RP12 verifier had flagged this template in this case).
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Respiratory follow-up: MIP -35 -> -44 cmH2O (flagged L against -53), out of the band where EAN/PNS 2023 (MIP <40) and Lawn 2001 (MIP weaker than -30) disagree, since the case is a monitored-bed case; escalation must "MIP becomes weaker than -40 cmH2O".
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.
- `initial_tool_outputs.specialized_test.test_type` "Nerve Conduction Studies (NCS) and EMG" -> `emg_ncs`.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI brain without contrast', impression 'No intracranial lesion identified. No brainstem signal change. No meningeal enhancement. No mass, haemorrhage, or restricted diffusion.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 82.4 -> 72.3 kg, height 174 -> 163 cm, BMI 27.2 -> 27.2 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 72.3 kg, height 163 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 40, ECOG 3 (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 and a working patient; he cannot walk without bilateral support, with facial weakness and dysphagia.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: unable to walk without bilateral support; timed gait and balance tests not performed (followup_outputs[3] request_gait_and_balance_timed). Why: rule 1: the library reports a normal timed gait and balance assessment; he cannot walk without bilateral support (hip flexion 3+/5, ankle dorsiflexion 3/5).
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no tremor or rigidity; motor items limited by weakness, response not assessable (followup_outputs[4] request_levodopa_challenge). Why: rule 1: the library describes a normal motor examination, gait and postural reflexes; limb weakness 3-4/5 and a support-dependent gait.
- `order_body_imaging {study: spine_MRI}`: smooth enhancement of the cauda equina roots, ventral more than dorsal; normal cord (fallback_tool_outputs.body_imaging). Why: rule 1: smooth enhancement of the cauda equina and ventral roots is seen in most patients with this polyradiculoneuropathy (Gorson 1996; Byun 1998), while the library reads the roots as normal.
- `order_body_imaging {study: peripheral_nerve_MRI}`: smooth enhancement and mild T2 hyperintensity of the lumbosacral roots, no enlargement (followup_outputs[5] request_peripheral_nerve_mri). Why: rule 1 and 3: the library reads the nerve roots as normal; root enhancement as on the spine MRI of this case.
- `order_specialized_test {test_type: nerve_biopsy}`: segmental demyelination with macrophage infiltration, plus chronic axonal loss and microvessel wall thickening (fallback_tool_outputs.specialized_test). Why: rule 3: the stored nerve conduction study shows absent sural and reduced median sensory responses with a demyelinating pattern; the library sural biopsy is normal.
- `order_specialized_test {test_type: speech_language_evaluation}`: mild flaccid dysarthria; language normal (followup_outputs[6] request_speech_language_evaluation). Why: rule 1 and 3: mild dysarthria, diminished gag and bilateral facial weakness are in the examination; the library reports no dysarthria.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: active standing not performed (cannot stand without bilateral support); supine BP 140/88 mmHg, HR 102 bpm; sitting BP 132/86 mmHg, HR 110 bpm (followup_outputs[7] request_orthostatic_blood_pressure). Why: rule 3: he cannot stand without bilateral support and is tachycardic (HR 104); the library reports 3 minutes of symptom-free standing at a supine heart rate of 68.
- `order_specialized_test {test_type: autonomic_testing}`: reduced cardiovagal function, distal sudomotor impairment and labile blood pressure on tilt (followup_outputs[8] request_autonomic_testing). Why: rule 3: the stored telemetry shows sinus tachycardia with a nocturnal bradycardia to 46 bpm and a hypertensive episode to 170/102 mmHg
- `order_specialized_test {test_type: tilt_table}`: Abnormal head-up tilt: resting tachycardia with labile blood pressure; no sustained orthostatic hypotension or vasovagal response (followup_outputs[9] request_tilt_table). Why: rule 3: the stored telemetry shows sinus tachycardia with a nocturnal bradycardia to 46 bpm and a hypertensive episode to 170/102 mmHg
- `order_specialized_test {test_type: skin_biopsy_iencf}`: reduced distal leg intraepidermal nerve fibre density (3.1 fibres/mm), normal proximal density (followup_outputs[10] request_skin_biopsy_iencf). Why: rule 2: a diabetic peripheral neuropathy diagnosed 2 years ago is in the history; the library reports normal fibre density.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
