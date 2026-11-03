# GBS-M02
Reviewer status: R1 not reviewed, R2 in_progress | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 1b3ba3ad-b993-4b76-86b8-189db252739b | FIXED | The respiratory follow-up `request_respiratory_monitoring` is now a serial report. At ED arrival: FVC 2.0 L (63%, 29.3 mL/kg), MIP -32, MEP 50. At 6 h: FVC 1.6 L (50%, 23.4 mL/kg), MIP -24, MEP 42. It includes the change sentence (20% fall), a weak cough and PaCO2 46 (H). Must 1 is "Admit to the ICU now", with the trend named. |
| 9dc82346-524b-4736-871e-1e299ba7da4a | FIXED | I deleted "Currently just above intubation threshold but declining" and the spirometry from `patient.neurological_exam.additional`. Must 2 is a multi-factor elective-intubation plan (trend, bulbar function, cough, secretions, fatigue; FVC <20 mL/kg written as about 1.37 L at 68.3 kg; >30% fall; MEP <40; intubate at once for distress, hypoxaemia or rising PaCO2). KCE 4 states the same. |
| a69c5ec7-f70b-4d93-b4f8-2e148173298b | FIXED | `anti-GM1 IgM` is removed from `action-1-interpret-labs`. The ganglioside follow-up (GM1 and GD1a IgG positive) is deleted, because typical sensorimotor GBS does not need the antibodies (EAN/PNS 2023; plan C2). KCE 2, the AMAN/AMSAN differential and the repeat-EMG must no longer depend on it. The canonical C2 pearl is added. |
| 3776d769-9d0e-4822-b9db-54d368d24e96 | FIXED | `initial_tool_outputs.specialized_test.quantitative_data.severity` is now "Severe", matching the impression. The median CMAP has values (3.4 and 3.6 mV, normal >4.0). Normal limits are added to the peroneal values, and a needle EMG line is added. The impression numbers the reduced median and peroneal CMAPs. |
| c0279d2a-1ef6-4ce9-a048-c60652e75c44 | FIXED | Every citation is now a key from the plan table ([EAN_PNS_2023], [Lawn_2001], [Leonhard_2019], [Walgaard_2011], [Walgaard_2021], [Brighton_2011]); `van_den_Berg_2014` and "GBS criteria pack §2" are gone. The literature output uses `evidence_level` "guideline" and "randomised controlled trial", the source type, in place of "guideline recommendation". Step 5 (`search_gbs_treatment`, empty) is deleted rather than filled: literature is optional (ruling 5), and the initial literature output now carries the general, sourced evidence. Brighton level 1 is stated once (KCE 1). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B/D | major | `followup_outputs` `request_repeat_ncs` | The "Repeat NCS at day 12" sat 4 days after an assessment made at presentation (day 8), so it was a future result. It also answered the index `emg_ncs` order: `test_index_order_is_not_answered_by_a_repeat_followup` failed for M02. | FIXED: deleted. The label drops "with secondary axonal injury" (the plan allowed this). The must "Repeat EMG/NCS in 1-2 weeks to delineate AIDP vs AMSAN" is deleted, because subtyping is not advised for decisions (EAN/PNS 2023). See Open questions. |
| C | major | `ground_truth.diagnosis.accepted[0]` | The label read "post-Campylobacter", but the case has no organism; only serology that the round deletes (C3). | FIXED: "Guillain-Barre syndrome (acute inflammatory demyelinating polyradiculoneuropathy) after a diarrhoeal illness". The diarrhoea history is kept; KCE 2 makes it the mEGOS factor. |
| C | major | `initial_tool_outputs.labs` | Campylobacter IgM/IgG was in the current labs (C3). The labs had no liver tests, albumin, glucose or CK. HIV carried the leaky clinical_significance (C10). | FIXED: serology deleted. The labs are now a CMP with liver tests, albumin and glucose 84 (which makes the CSF ratio 58/84 = 0.69), plus CK 87. HIV keeps `clinical_significance` null. Interpretation and summary rewritten. |
| C | major | `assessment.required_recommendations` | The musts had no ICU admission, no airway plan and no swallow must, although she coughs on water with a reduced gag. | FIXED: ICU, elective-intubation and swallow/aspiration musts. The IVIg must gives the 2 g/kg total, the dose at 68.3 kg, the indication (cannot walk unaided) and the timing. |
| C | major | `assessment.prohibited_recommendations` | Template steroid text, IgA screening, and "neuromuscular-junction-blocking sedatives" (not a drug class) (C8). | FIXED: canonical steroid, IVIg-after-PE and renal prohibitions, the succinylcholine prohibition, and a sedation caution. |
| B | major | telemetry follow-up | The report covered 120 h and gave treatment (IV labetalol, IV fluids) (C12, ruling 4). | FIXED: the first 24 h with the same three autonomic events (the hypotension moved inside the window), findings only. a8 expected_evidence is canonical. |
| D | major | `initial_tool_outputs.literature_search` | The output echoed a5's expected_evidence (the leak guard failed) (C11). | FIXED: canonical general summary. a5 is optional and last. |
| A/D | minor | `followup_outputs` `check_ivig_drug_interactions` | Empty DDI placeholder (C9). | FIXED: deleted. The initial DDI output gives category-level content for levothyroxine with IVIg and PE, and the sulfonamide allergy. a6 is optional, because levothyroxine has no interaction that changes management (ruling 6). |
| A | major | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule` | Template criteria, order and constraints (plan 3.1, 3.3). | FIXED: order a2, a3, a1, a4, a8, a7, a6, a5. Canonical texts. Constraints removed. The stop rule lists the five required criteria, max 3. |
| C | major | `ground_truth.differential` | AMAN/AMSAN and CIDP were "moderate". CIP was kept in a community-onset case. The Lyme entry cited Campylobacter serology (C5). | FIXED: AMAN/AMSAN low (the NCS is demyelinating), CIDP low, CIP very_low ("no ICU course before onset"), Lyme very_low on the CSF. |
| B | minor | `patient.history_present_illness` | "One week later" did not fit an 8-day history after an illness that started 3 weeks ago and lasted 4 days. The editorial "As a nurse, she was appropriately alarmed" also blurred when she came in. | FIXED: "About 9 days after it resolved"; "Two days ago she began to have difficulty rising from the toilet, and she came to the ED today". |
| C | minor | `patient.physical_exam` | No weight (C1). | FIXED: "Weight 68.3 kg, height 166 cm" (BMI 24.8; a predicted FVC of 3.2 L fits). The exam `additional` now gives clinical respiratory signs only. |
| C | minor | `red_herrings[0]` | Attributed the inflammation to "Campylobacter". | FIXED: non-specific acute-phase response resolved by the afebrile state, no focus and acellular CSF; aspiration flagged as the infection to guard against. |
| B | minor | CSF follow-up | The ratio 0.70 did not match any serum glucose; RBC had no unit. | FIXED: ratio 0.69 against serum 84; units; report voice. |
| A | minor | `avoided_actions[*].citations`, `metadata.difficulty_rationale` | Old citation key and old counts. | FIXED. |
| C | minor | respiratory follow-up `findings[*].reference_range` | The old MIP reference read as an intubation threshold, and there was no MEP reference. | FIXED: MIP and MEP reference ranges are the age- and sex-specific lower limits of normal from Evans and Whitelaw 2009 (Respir Care 2009;54:1348-1359; men: MIP 62-0.15 x age, MEP 117-0.83 x age; women: MIP 62-0.50 x age, MEP 95-0.57 x age). |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-M02 is a post-diarrhoeal AIDP (no organism named) whose respiratory step shows a falling trend over 6 hours after ED arrival: FVC 2.0 to 1.6 L (63% to 50%, 23.4 mL/kg at 68.3 kg), MIP -32 to -24, MEP 50 to 42, weak cough, PaCO2 46. The patient block keeps only clinical signs. The musts now require ICU admission now, early elective intubation planning on trend, bulbar function, cough, secretions and fatigue, IVIg 2 g/kg or PE, a swallow assessment with aspiration precautions, telemetry and DVT prophylaxis. The prohibitions are the guideline ones. The NCS severity reads "Severe" and the median CMAPs have values. The ganglioside panel, the Campylobacter serology, the day-12 repeat NCS (a future result) and the empty literature and DDI steps are deleted. Telemetry covers the first 24 h with no treatment. Citations use EAN/PNS 2023 and the other plan keys; Brighton level 1 is stated once. The differential is updated after the work-up.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 5 (weight field) and 6 (variant synonyms accepted in an AIDP case) apply.

## Open questions for Andrea (judgment calls you could not settle)
- I deviated from the plan on the repeat NCS. The plan kept the day-12 repeat NCS as a follow-up so the label could keep "with secondary axonal features". I deleted it instead, for three reasons. The assessment is made at presentation (day 8), so a day-12 study is a future result. EAN/PNS 2023 does not advise electrodiagnostic subtyping for decisions. And the follow-up answered the index NCS order, which breaks the repeat-study guard. If you want the axonal evolution kept, the place for it is a must ("repeat NCS at 2-3 weeks if the course is atypical"), not a stored result.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the full diff and the whole final case.
- Notes 1b3ba3ad, 9dc82346, a69c5ec7, 3776d769, c0279d2a: each confirmed fixed in the file (serial FVC/MIP/MEP with change sentence and ICU-now must; multi-factor intubation must; no anti-GM1 in a1 and no ganglioside follow-up; NCS severity "Severe" with median CMAP 3.4/3.6 mV; plan citation keys, no empty step). The worker's deletion of the day-12 repeat NCS (a future result that also hijacked the index NCS order) instead of keeping it as the plan suggested is sound and is logged; I accept it as the decision, so it is no longer an open question.
- Arithmetic re-checked: timeline (illness 21 to 17 days ago, tingling 9 days later = 8 days ago); BMI 24.8; FVC 2.0/3.2 = 63%, 1.6/3.2 = 50%, 23.4 mL/kg, 20% fall; 20 mL/kg = 1.37 L; MIP/MEP limits for a 42-year-old woman (41, 71); CSF 58/84 = 0.69; IVIg 27 g/day; ECG 112 = vitals.
- Found and fixed: the labs show potassium 3.4 mEq/L (L) and the ECG a QTc of 462 ms (prolonged for a woman) with vagal bradycardia to 38 bpm on telemetry, but no must addressed the electrolytes (PATTERNS: potassium and magnesium for a long QTc). Added must 5: "Replace potassium (3.4 mEq/L) and check magnesium: the QTc is 462 ms and autonomic bradyarrhythmias are occurring."
- Checks: `perfect_agent.py GBS-M02 -v` passes; `case_io.py check` reports no failure naming GBS-M02.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- B, minor: `action-7-analyze-ecg` expected_evidence was the condition template ("Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities reflecting autonomic involvement") and the rationale repeated the label, while the ECG shows sinus tachycardia 112 bpm with QTc 462 ms. Rewritten to what the ECG shows, with the rationale used in RP12, RP14-RP16 (the RP12 verifier had flagged this template in this case).
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- `ground_truth.diagnosis.accepted[0]`: spelling normalised to "Guillain-Barré"; content unchanged.
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.
- `initial_tool_outputs.specialized_test.test_type` "Nerve Conduction Studies (NCS) and EMG" -> `emg_ncs`.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI brain without contrast', impression 'No intracranial lesion identified. No signal change in brainstem or spinal cord. No mass, haemorrhage, or restricted diffusion.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 62.7 -> 68.3 kg, height 159 -> 166 cm, BMI 24.8 -> 24.8 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 68.3 kg, height 166 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3 (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 and a working patient; she walks 10 feet only with bilateral arm support, with facial weakness and dysphagia.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: severely impaired gait and balance: walks only a few metres with bilateral support (berg 14/56); timed tests not completed (followup_outputs[3] request_gait_and_balance_timed). Why: rule 1: the library reports a normal timed gait and balance assessment; she walks only 10 feet with bilateral arm support and cannot rise from a chair without armrests.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no tremor or rigidity; motor items limited by weakness, response not assessable (followup_outputs[4] request_levodopa_challenge). Why: rule 1: the library describes a normal motor examination, gait and postural reflexes; proximal weakness 3+/5 and a support-dependent gait.
- `order_body_imaging {study: spine_MRI}`: smooth enhancement of the cauda equina roots, ventral more than dorsal; normal cord (fallback_tool_outputs.body_imaging). Why: rule 1: smooth enhancement of the cauda equina and ventral roots is seen in most patients with this polyradiculoneuropathy (Gorson 1996; Byun 1998), while the library reads the roots as normal.
- `order_body_imaging {study: peripheral_nerve_MRI}`: smooth enhancement and mild T2 hyperintensity of the lumbosacral roots, no enlargement (followup_outputs[5] request_peripheral_nerve_mri). Why: rule 1 and 3: the library reads the nerve roots as normal; root enhancement as on the spine MRI of this case.
- `order_specialized_test {test_type: nerve_biopsy}`: segmental demyelination with macrophage infiltration and sparse T-lymphocytes; reduced myelinated fibre density (fallback_tool_outputs.specialized_test). Why: rule 3: the stored nerve conduction study shows absent sural and reduced median sensory responses with a demyelinating pattern; the library sural biopsy is normal.
- `order_specialized_test {test_type: speech_language_evaluation}`: mild flaccid dysarthria with hypernasality; language normal (followup_outputs[6] request_speech_language_evaluation). Why: rule 1 and 3: a nasal voice, diminished gag and bilateral facial weakness are in the examination; the library reports no dysarthria.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: active standing not possible; supine BP 150/96, HR 110; sitting BP 136/88, HR 122 (followup_outputs[7] request_orthostatic_blood_pressure). Why: rule 3: she stands only with bilateral support and is tachycardic (HR 112) with marked blood pressure lability on telemetry; the library reports 3 minutes of symptom-free standing at a supine heart rate of 68.
- `order_specialized_test {test_type: autonomic_testing}`: reduced cardiovagal function, distal sudomotor impairment and marked blood pressure lability on tilt (followup_outputs[8] request_autonomic_testing). Why: rule 3: the stored telemetry shows heart rate 38-140 bpm and blood pressure 84/50-196/110 mmHg
- `order_specialized_test {test_type: tilt_table}`: Abnormal head-up tilt: marked blood pressure lability with a symptomatic fall of 38 mmHg systolic; resting tachycardia (followup_outputs[9] request_tilt_table). Why: rule 3: the stored telemetry shows heart rate 38-140 bpm and blood pressure 84/50-196/110 mmHg
- `interpret_labs {panels: [ABG]}`: pH 7.38, pCO2 46 mmHg (elevated), pO2 82 mmHg, SaO2 95%; HCO3 26.9 mmol/L (fallback_tool_outputs.labs['ABG']). Why: rule 3: the stored respiratory assessment records pH 7.38 and PaCO2 46 mmHg (elevated); the library reports a normal PaCO2.
- `interpret_labs {panels: [anti_TPO]}`: anti-thyroid peroxidase antibodies 412 IU/mL (elevated) (fallback_tool_outputs.labs['anti_TPO']). Why: rule 2: Hashimoto thyroiditis on levothyroxine is in the history; the library reports negative antibodies.
- `interpret_labs {panels: [anti_thyroglobulin]}`: anti-thyroglobulin antibodies 186 IU/mL (elevated) (fallback_tool_outputs.labs['anti_thyroglobulin']). Why: rule 2: Hashimoto thyroiditis is in the history; the library reports negative antibodies.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
