# GBS-M01
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 6644822c-c4a8-4823-a15c-5d41c800d454 | FIXED | I took the reviewer's second option (plan M01): the history stays a respiratory illness, with no diarrhoea added. `ground_truth.diagnosis.accepted[0]` now reads "Guillain-Barre syndrome (acute inflammatory demyelinating polyradiculoneuropathy) after an upper respiratory infection". I deleted the Campylobacter IgM/IgG, CMV IgM and EBV VCA IgM results (`initial_tool_outputs.labs.panels.Infection_serology`) and their line in `abnormal_values_summary` and `interpretation`. `action-1-interpret-labs` no longer asks for stool culture or Campylobacter serology "if recent diarrhea". I rewrote KCE 1 (URI antecedent, Brighton level 1 stated once), deleted KCE 4 (anti-GM1 after Campylobacter) and put the canonical C2 pearl in its place. In the Lyme differential, "Campylobacter serology positive" is replaced with a CSF-based reason. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| D | major | `patient.neurological_exam.additional` | The exam gave the bedside FVC (2.2 L, 58%) and NIF (-28), which are the result of a4, and added an editorial line ("concerning but not yet at intubation threshold") (C1/C7). | FIXED: replaced with clinical respiratory signs only (no accessory muscle use, weak cough). |
| C | major | respiratory follow-up `request_respiratory_monitoring` | FVC 58% predicted and NIF -28 were flagged "(H)". There was no weight, so no mL/kg, and no MEP (C1). | FIXED: weight 67.5 kg and height 160 cm added in `patient.physical_exam.general` (BMI 26.4, which also fits a predicted FVC of 3.8 L). The report is rewritten in the canonical format: FVC 2.2 L (58%, 32.6 mL/kg) L, MIP -28 L, MEP 46 L, cough weak, ABG normal. |
| C | major | `assessment.required_recommendations` | The level-of-care must said "approaching intubation thresholds". The intubation must used "NIF worse than -30 / VC <40% predicted", which is the wrong 20/30/40 wording, and it was a single-threshold rule (C1). | FIXED: an ICU-level monitoring must naming its triggers (FVC <60% predicted, MIP weaker than -30 cmH2O, bulbar weakness, weak cough), and a serial-monitoring and elective-intubation must built on trend, bulbar function, cough, secretions and fatigue, with 20 mL/kg written as about 1.35 L at this weight. |
| C | major | `assessment.required_recommendations` | Dysphagia for thin liquids and nasal speech had no swallow or aspiration must. | FIXED: must added for a formal swallow assessment before oral intake. |
| C | minor | IVIg must | No total dose, no indication and no timing against onset. | FIXED: IVIg 0.4 g/kg/day x5 (2 g/kg, about 27 g/day at 67.5 kg) or PE 200-250 mL/kg in 5 sessions, with the reason: he cannot walk unaided and is 10 days from onset [EAN_PNS_2023]. |
| C | major | `assessment.prohibited_recommendations` | The steroid prohibition was the template ("monotherapy ... may worsen outcome"). "Do not combine IVIG and PE in sequence" and "IgA status" were unsourced (C8). | FIXED: canonical steroid, IVIg-after-PE and renal-function prohibitions. I added a succinylcholine prohibition (denervation hyperkalaemia; intubation is a real possibility here). |
| B | major | `patient.neurological_exam.motor` | "Increased fatigue with sustained effort" (fatigability) contradicted the MG differential ("no fatigability pattern"). | FIXED: phrase deleted. |
| E | minor | `patient.neurological_exam.reflexes` | Editorial "This is the most alarming finding" (plan M01). | FIXED: deleted. |
| B | minor | `patient.neurological_exam.sensory` | "Glove-and-stocking" paraesthesias, while the HPI and exam put them in the feet to the knees only. | FIXED: "stocking distribution to the knees". |
| B | minor | `initial_tool_outputs.specialized_test.findings[0]` | Median CMAP 4.2 mV was called "reduced" against a normal limit of >4 mV (plan M01). | FIXED: 3.1 mV. I added a needle EMG line (reduced recruitment, no denervation at day 10), because the study is titled NCS and EMG but reported no needle findings. The impression now also numbers the needle result. |
| B | minor | CSF follow-up `analyze_csf_gbs` | A CSF glucose of 62 and a ratio of 0.69 implied a serum glucose of 90, but the serum glucose is 112. A WBC of 3 was called "borderline". | FIXED: CSF glucose 72 mg/dL, ratio 0.64; WBC "3 cells/mm3 (mononuclear)"; protein reference range added; interpretation in report voice. |
| C | major | `initial_tool_outputs.labs` | The labs had no liver tests, albumin or CK (EAN/PNS routine tests, plan 3.1). HIV carried the leaky clinical_significance sentence (C10). | FIXED: the BMP panel becomes a CMP with liver tests and albumin (all normal), and a CK of 118 is added. HIV stays non-reactive with `clinical_significance: null`. Interpretation and summary rewritten. |
| C | major | telemetry follow-up `request_cardiac_monitoring` | The report covered 72 h, into the future of the assessment (C12). | FIXED: the first 24 h only (sinus tachycardia, one nocturnal bradycardia to 42 bpm, QTc 448-462 ms, cuff BP range). The Day 2 SVT and Night 2 events are removed. a8 expected_evidence is canonical. |
| A/D | major | `followup_outputs` | There was an empty literature follow-up (`search_gbs_treatment`) and an empty DDI follow-up (`check_ivig_drug_interactions`) (C9). The ganglioside follow-up reported positive GM1/GD1a IgG that nothing interpreted (C2). | FIXED: all three deleted. The pathway order is CSF, respiratory, telemetry. |
| D | major | `initial_tool_outputs.literature_search` | The literature output repeated a5's expected_evidence verbatim, with source `van_den_Berg_2014` (C11). | FIXED: canonical population-keyed summary [EAN_PNS_2023, Walgaard_2021]; `evidence_level` names the source type. |
| C | minor | `initial_tool_outputs.drug_interactions` | Empty interaction block. | FIXED: category-level content for amlodipine (no IVIg interaction; added hypotension with PE, relative caution; BP lability warning). |
| C | major | `ground_truth.action_criteria` | The template criteria put literature and DDI as required, a1 asked for HIV, inflammatory markers and "anti-GM1 IgM", the a3 cell count was "<10", and the a4 thresholds were wrong (C2, C10, C11, ruling 5, 6). | FIXED per plan 3.1: order a2, a3, a1, a4, a8, a7, a6, a5. Canonical labels and evidence. a1 args CBC, CMP, CK. a6 optional (amlodipine has no interaction that changes management). a5 optional and last. Citations now use [EAN_PNS_2023], [Lawn_2001], [Leonhard_2019]. |
| A | major | `ground_truth.sequence_constraints`, `stop_rule` | The first constraint used a6 against EMG for a respiratory reason. Both constraints hung on a6, which is now optional. The stop rule listed literature and DDI, with `max_additional_actions` 0. | FIXED: constraints removed (no order between them matters clinically). The stop rule lists the five required criteria, `max_additional_actions` 3. |
| C | major | `ground_truth.differential` | Acute-onset CIDP was "moderate". The transverse myelitis entry cited a spinal MRI that does not exist (C5). | FIXED: CIDP low (reassess at 8 weeks). Transverse myelitis and Lyme are very_low, with the reasons found in the case. |
| B | minor | `ground_truth.red_herrings[1]` | Cited a lumbosacral MRI with root enhancement that the case does not contain (C6). | FIXED: deleted. RH 1 (WBC 11.2, CRP, ESR) is kept and its resolution rewritten without Campylobacter. |
| C | minor | `key_clinical_evidence` 2, 3, 5 | The CSF pearl used "<10/uL", the EMG pearl said "confirms", and the respiratory pearl used a single threshold. | FIXED: rewritten (cells <5, >50 points elsewhere; "consistent with"; trend-based decision). |
| A | minor | `avoided_actions[*].citations`, `metadata.difficulty_rationale` | The avoided actions cited `van_den_Berg_2014`, and the difficulty rationale gave counts that are now wrong. | FIXED: [EAN_PNS_2023]; rationale updated. |
| C | minor | respiratory follow-up `findings[*].reference_range` | The old MIP reference read as an intubation threshold, and there was no MEP reference. | FIXED: MIP and MEP reference ranges are the age- and sex-specific lower limits of normal from Evans and Whitelaw 2009 (Respir Care 2009;54:1348-1359; men: MIP 62-0.15 x age, MEP 117-0.83 x age; women: MIP 62-0.50 x age, MEP 95-0.57 x age). |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-M01 is now a post-URI AIDP with no Campylobacter attribution: the label names the respiratory antecedent, and all antecedent serology and the ganglioside panel are gone. The patient block no longer gives the spirometry. Weight 67.5 kg and height 160 cm are in the general exam. The respiratory step reports FVC 2.2 L (58% predicted, 32.6 mL/kg), MIP -28, MEP 46 and a weak cough, each flagged low. The musts now require ICU-level monitoring and multi-factor intubation planning, IVIg 2 g/kg or PE with the indication, a swallow assessment, telemetry and DVT prophylaxis. The prohibitions are the guideline ones: no corticosteroids, no IVIg directly after PE and no second course, renal function before IVIg, no succinylcholine. The labs now include liver tests, albumin and CK. The median CMAP is truly reduced (3.1 mV), and a needle EMG line was added. The CSF glucose ratio matches the serum glucose. Telemetry covers the first 24 h. Literature and DDI are optional and carry general, sourced content. The differential is updated after the work-up, and the non-existent lumbosacral MRI red herring is deleted.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 5 (weight field): weight is in `patient.physical_exam.general` until demographics carries `weight_kg`.
- Plan CENTRAL 6: the appended synonyms still accept "miller fisher syndrome", "acute motor axonal neuropathy" and "AMAN" for this AIDP case.

## Open questions for Andrea (judgment calls you could not settle)
None. The succinylcholine prohibition carries no citation: the plan lists it as a canonical fact, and I could not verify that EAN/PNS 2023 states it in those words.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the full diff and the whole final case.
- Note 6644822c: confirmed fixed everywhere (label, labs, a1, KCE, red herring, Lyme entry); no Campylobacter, diarrhoea or ganglioside text remains.
- Arithmetic re-checked: BMI 67.5/1.60^2 = 26.4; FVC 2.2/3.8 = 58%, 2.2/67.5 = 32.6 mL/kg; 20 mL/kg = 1.35 L; IVIg 0.4 x 67.5 = 27 g; MIP/MEP lower limits match Evans and Whitelaw (54.5, 75.5); CSF 72/112 = 0.64; ECG rate 108 = vitals; telemetry events within 24 h; BP 148/94 inside the telemetry range. Musts and prohibitions do not contradict each other or the avoided actions. Brighton level quoted once.
- Found and fixed (pre-existing, missed by the worker): `initial_tool_outputs.specialized_test.quantitative_data` gave "DML_prolongation 50-90% above ULN" and "motor_CV_reduction 35-45% below LLN", which the report's own numbers do not support (median CV 38 and 36 m/s against >49 m/s is 22-27% below; DML 6.8 and 7.2 ms against <4.2 ms is 62-71% above). Rewritten to those values, named as median motor.
- Left as is: DDI and literature outputs are general and pass the leak guard.
- Checks: `perfect_agent.py GBS-M01 -v` passes; `case_io.py check` reports no failure naming GBS-M01.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- B, minor: `action-7-analyze-ecg` expected_evidence was the condition template ("Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities reflecting autonomic involvement") and the rationale repeated the label, while the ECG shows sinus tachycardia 108 bpm with QTc 448 ms. Rewritten to what the ECG shows, with the rationale used in RP12, RP14-RP16 (the RP12 verifier had flagged this template in this case).
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- `ground_truth.diagnosis.accepted[0]`: spelling normalised to "Guillain-Barré" (was "Guillain-Barre"); content unchanged.
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.
- `initial_tool_outputs.specialized_test.test_type` "Nerve Conduction Studies (NCS) and Electromyography (EMG)" -> `emg_ncs`.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 78.1 -> 67.5 kg, height 172 -> 160 cm, BMI 26.4 -> 26.4 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 67.5 kg, height 160 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 40, ECOG 3 (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 and a working patient; he cannot stand without assistance, with leg weakness, facial diplegia and dysphagia.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: unable to stand without assistance; timed gait and balance tests not performed (followup_outputs[3] request_gait_and_balance_timed). Why: rule 1: the library reports a normal timed gait and balance assessment; he cannot stand without assistance (ankle dorsiflexion 3/5, areflexia).
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no tremor or rigidity; motor items limited by weakness, response not assessable (followup_outputs[4] request_levodopa_challenge). Why: rule 1: the library describes a normal motor examination, gait and postural reflexes; limb weakness 3-4/5 and inability to stand.
- `order_body_imaging {study: spine_MRI}`: smooth enhancement of the cauda equina roots, ventral more than dorsal; normal cord (fallback_tool_outputs.body_imaging). Why: rule 1: smooth enhancement of the cauda equina and ventral roots is seen in most patients with this polyradiculoneuropathy (Gorson 1996; Byun 1998), while the library reads the roots as normal.
- `order_body_imaging {study: peripheral_nerve_MRI}`: smooth enhancement and mild T2 hyperintensity of the lumbosacral roots, no enlargement (followup_outputs[5] request_peripheral_nerve_mri). Why: rule 1 and 3: the library reads the nerve roots as normal; root enhancement as on the spine MRI of this case.
- `order_specialized_test {test_type: nerve_biopsy}`: segmental demyelination with macrophage infiltration and sparse T-lymphocytes; reduced myelinated fibre density (fallback_tool_outputs.specialized_test). Why: rule 3: the stored nerve conduction study shows absent sural sensory responses bilaterally with a demyelinating pattern; the library sural biopsy is normal.
- `order_specialized_test {test_type: speech_language_evaluation}`: moderate flaccid dysarthria with hypernasality; language normal (followup_outputs[6] request_speech_language_evaluation). Why: rule 1 and 3: dysarthria, a nasal voice and bilateral facial weakness are in the examination; the library reports no dysarthria.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: active standing not possible; supine BP 146/92, HR 106; sitting BP 138/88, HR 114 (followup_outputs[7] request_orthostatic_blood_pressure). Why: rule 3: he cannot stand without assistance and is tachycardic (HR 108); the library reports 3 minutes of symptom-free standing at a supine heart rate of 68.
- `order_specialized_test {test_type: autonomic_testing}`: reduced cardiovagal function, distal sudomotor impairment and labile blood pressure on tilt (followup_outputs[8] request_autonomic_testing). Why: rule 3: the stored telemetry shows sinus tachycardia 90-128 bpm, a nocturnal bradycardia to 42 bpm and blood pressure 124/76-166/98 mmHg
- `order_specialized_test {test_type: tilt_table}`: Abnormal head-up tilt: resting tachycardia with labile blood pressure; no orthostatic hypotension or vasovagal response (followup_outputs[9] request_tilt_table). Why: rule 3: the stored telemetry shows sinus tachycardia 90-128 bpm, a nocturnal bradycardia to 42 bpm and blood pressure 124/76-166/98 mmHg
- `interpret_labs {panels: [ABG]}`: pH 7.42, pCO2 40 mmHg, pO2 88 mmHg, SaO2 97%; HCO3 25.7 mmol/L (fallback_tool_outputs.labs['ABG']). Why: rule 3: the stored respiratory assessment records an arterial blood gas of pH 7.42, PaCO2 40 mmHg, PaO2 88 mmHg; the library values differ.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
