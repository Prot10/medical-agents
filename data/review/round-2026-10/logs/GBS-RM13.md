# GBS-RM13
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 9f5f1a74-9634-4250-bf7c-7b90c41fa661 | FIXED | History shortened to the plan's course: bronchitis about 4 weeks ago, weakness starting a week later and progressing for 3 weeks, unable to stand for the last 2 days (`patient.chief_complaint`, `patient.history_present_illness`; "6 weeks", "7 weeks" and the "chronic demyelinating polyneuropathy" sentence removed; `neurological_exam.additional` with "History of 6 weeks" removed). Acute-onset CIDP lowered to low with the 8-week reassessment; pearl 1 states the 4-week nadir rule. |
| 2f754e55-6dae-4b9f-94af-e88c1a1419c0 | FIXED | Weight 70 kg, height 157 cm in `patient.physical_exam.general` (BMI 28.4). `followup_outputs[2]` canonical: FVC 1.7 L (58% of 2.95 L; 24 mL/kg) L, MIP -26 cmH2O L, MEP 44 cmH2O L, change from 1.8 L 6 h earlier (6% fall), cough effective; the exam's 1.8 L / -28 is now that earlier measurement. Must 1: ICU-level monitoring now (FVC <60%, MIP weaker than -30) with the elective-intubation triggers. a4 canonical. |
| 3b0554e2-c324-4db0-aac9-389d1d4f4fb7 | FIXED | Myopathic needle-EMG features deleted (neurogenic recruitment, occasional distal fibrillations, "no myopathic units"); `quantitative_data.pattern` no longer "concurrent myopathic features"; CK 642 -> 410 U/L and myoglobin deleted; new recommended `action-10-interpret-labs-myositis-panel` (`myositis_panel`) served by new follow-up `request_myositis_antibody_panel` (anti-HMGCR, SRP, synthetase, Mi-2, MDA5, TIF1-gamma negative); differential "Statin-associated or inflammatory myopathy" low with reasons; red herring 2 (CK on atorvastatin); must 3 holds atorvastatin; a6 required with the statin in its label and expected evidence. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness`, `initial_tool_outputs.labs` | HPI "ammonia is not significantly elevated" vs labs ammonia 68 (H). | FIXED: HPI clause deleted (it also leaked a lab result); ammonia 68 kept and the hepatic-encephalopathy differential explains the mild confusion. |
| D | major | `patient.neurological_exam.additional`, HPI last sentence | Spirometry, "Serum CK markedly elevated on admission", "Proximal > distal" and a sentence listing the differential (C7). | FIXED: field removed; editorial sentence deleted. |
| B | minor | `patient.clinical_history.social_history.living_situation` | "Lives alone" while her husband gives history. | FIXED: "Lives with husband". |
| B | minor | `past_medical_history`, HPI | Remote splenectomy with platelets 88 (asplenia gives thrombocytosis, not thrombocytopenia); plays no role. | FIXED: splenectomy removed. |
| C | major | `followup_outputs[0].output.appearance` | CSF "Xanthochromic - hepatic jaundice": bilirubin 3.2 mg/dL and protein 96 do not stain CSF, and xanthochromia would raise SAH. | FIXED: "Clear, colorless"; note removed; interpretation canonical. |
| C | major | `initial_tool_outputs.labs` | HIV with the leaky sentence, Campylobacter IgM (C3, C10); no sodium, potassium, renal function, glucose or albumin in a diabetic cirrhotic on spironolactone; INR filed under LFTs. | FIXED: CMP (Na 136, K 4.8, creatinine 0.9, BUN 16, glucose 168 H, calcium, AST 74, albumin 3.1 L) added to the kept values; Coagulation panel (INR 1.9, PT 21.4 s); CK panel; HIV and Campylobacter removed. Child-Pugh B holds with PBC bilirubin bands (1+2+2+2+2 = 9). |
| C | major | `followup_outputs[4]` (DDI) | Prescriptive and partly wrong: "ensure FFP correction before LP", sucrose-IVIg advice, IgA screen as contraindication, metformin "contrast" warning, "IVIG preferred in this patient" (C8, C13). | FIXED: category-level output: IVIg with spironolactone (relative caution, renal function and potassium), UDCA no interaction, atorvastatin SmPC (active liver disease contraindication, stop if CK rises markedly), metformin SmPC (hepatic insufficiency), IVIg renal and thrombotic risk. |
| C | major | `ground_truth.sequence_constraints` | No platelet/INR gate before the LP (C13). | FIXED: hard a1 before a3 (reason: platelets 88, INR 1.9); soft a1 before a6; `coagulation` in a1 panels. |
| C | major | `ground_truth.assessment` | IVIg without indication or window; "avoid hepatotoxic adjuncts" vague; no statin decision, no respiratory escalation. | FIXED: six musts (ICU-level and intubation plan; IVIg with indication, 3-week timing and why not PE; hold atorvastatin and review metformin; telemetry; hepatology and electrolyte monitoring; mechanical DVT prophylaxis); prohibitions canonical steroid, renal function, PE with albumin replacement as relative caution. |
| C | minor | `initial_tool_outputs.ecg` | Rate 98 called sinus tachycardia; QTc 452 ms in a woman called borderline. | FIXED: normal sinus rhythm, normal intervals. |
| C | minor | `followup_outputs[3]` (telemetry) | 96-hour report with a Day 2 event; "Mild autonomic tachycardia" interpretive (C12). | FIXED: first 24 h, sinus 64-108 bpm, blood pressure range; a8 canonical. |
| A | major | `followup_outputs` | Ganglioside follow-up (typical sensorimotor GBS) and empty literature placeholder. | FIXED: deleted (C2, C9). |
| D | major | `initial_tool_outputs.literature_search` | Scoring-key echo. | FIXED: canonical general output; a5 optional, last. |
| C | major | `ground_truth.diagnosis.accepted[0]` | "AIDP (post-bronchitis), with concurrent PBC-associated immunologic background". | FIXED: "Guillain-Barré syndrome (acute inflammatory demyelinating polyradiculoneuropathy) after bronchitis, with primary biliary cholangitis". |
| C | major | `ground_truth.differential` | Vasculitic neuropathy and CIDP moderate; HE "encephalopathic features absent" against the case; no myopathy. | FIXED: myopathy, CIDP and vasculitic low; HE very_low with the ammonia reasoning; CIP "No ICU course before onset". |
| C | minor | `ground_truth.action_criteria` | Template criteria and order. | FIXED: canonical; order a2, a1, a3 (hard), a10, a4, a8, a7, a6 (required), a5 (optional); stop rule six required, `max_additional_actions` 3. |
| E | minor | `key_clinical_evidence`, `red_herrings[0].location`, `neurological_exam.gait`, metadata | Generic pearls; RH location was a path; em dash; difficulty texts named myoglobin. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The course now meets GBS: bronchitis 4 weeks ago, weakness for 3 weeks, unable to stand for 2 days. The myopathy alternative is resolvable: CK is 410 U/L (myoglobin removed), the needle EMG is neurogenic with no myopathic units, a new recommended myositis antibody panel (including anti-HMGCR) is negative, and the differential puts statin-associated or inflammatory myopathy at low; atorvastatin is held. Labs now include electrolytes, glucose and albumin, with INR 1.9 and platelets 88 in a coagulation panel, and a hard constraint puts the labs before the LP. The CSF is clear (the "xanthochromia from jaundice" was implausible). Respiratory values are consistent with the new weight (70 kg): FVC 1.8 then 1.7 L (58%, 24 mL/kg), MIP -26, MEP 44, so the patient goes to ICU-level monitoring with an elective-intubation plan. IVIg is chosen over plasma exchange because of the coagulopathy, with renal and electrolyte monitoring; the interaction check is required and now gives category-level, sourced cautions for the statin, metformin and spironolactone instead of prescribing FFP. Telemetry covers 24 hours; ganglioside and placeholder steps are gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `ground_truth.diagnosis.accepted[0]` reworded (label text only; same entity and code).

## Open questions for Andrea (judgment calls you could not settle)

- None. IVIg at 3 weeks is outside the 2-week window of the trials; I chose it over plasma exchange (trial window 4 weeks) because of INR 1.9 and platelets 88 and say so in must 2, which a physician can check.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: the timeline is consistent in chief complaint, HPI, KCE, differential and musts (bronchitis 4 weeks ago, weakness 3 weeks, nadir now, no "6/7 weeks" left); FVC 1.7/2.95 L = 58%, 24 mL/kg at 70 kg, BMI 28.4 agrees with 157 cm, 20 mL/kg = 1.4 L, 1.8 to 1.7 L = 6% fall; ICU-level must justified (FVC <60%, MIP -26). Myopathy class resolved: CK 410 (below 5x ULN), myoglobin gone, needle EMG neurogenic, myositis panel follow-up served to a10, statin held. Ammonia: HPI clause removed, lab 68 interpreted in the HE differential. Hard constraint labs before CSF verified in the right direction (before = a1, after = a3); `coagulation` in a1 args; FFP instruction gone from the DDI output; DDI statements (atorvastatin SmPC active liver disease, metformin SmPC hepatic insufficiency) are correct. Child-Pugh B recomputes to 9 with PBC bilirubin bands. QTc 452 normal for a woman. IVIg beyond 2 weeks is reasoned in the must (PE limited by INR 1.9, platelets 88).
Residual, not changed: the NCS reports absent sural SNAPs while sensation is clinically intact; plausible as subclinical diabetic neuropathy in a 54-year-old with type 2 diabetes, so left as is. No changes made.
Checks re-run after the verifier's edits: `perfect_agent.py -v` ok (each criterion served by its intended report; labs, brain MRI and ganglioside probes confirmed by a direct MockServer probe where relevant) and `case_io.py check` clean for this case (the remaining failures name GBS-RP16 and GBS-RS16 only).


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- B, minor: `action-7-analyze-ecg` expected_evidence was the condition template ("Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities reflecting autonomic involvement") and the rationale repeated the label, while the ECG shows normal sinus rhythm 98 bpm with QTc 452 ms. Rewritten to what the ECG shows, with the rationale used in RP12, RP14-RP16 (the RP12 verifier had flagged this template in this case).

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous ICU telemetry" -> `telemetry`.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-6-check-drug-interactions` rationale: "Her medicines include a statin while CK is raised, metformin in hepatic insufficiency and a potassium-sparing diuretic alongside IVIg: concrete interactions that change management (ROUND_POLICY ruling 6)." -> "Her medicines include a statin while CK is raised, metformin in hepatic insufficiency and a potassium-sparing diuretic alongside IVIg: concrete interactions that change management."

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 73.6 -> 70 kg, height 161 -> 157 cm, BMI 28.4 -> 28.4 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 70 kg, height 157 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 40, ECOG 3 (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 and a working patient; she cannot stand unaided, with end-stage liver disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: unable to stand unaided; timed gait and balance tests not performed (followup_outputs[5] request_gait_and_balance_timed). Why: rule 1: the library reports a normal timed gait and balance assessment; she has been unable to stand for 2 days (hip flexion 3/5).
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no tremor or rigidity; motor items limited by weakness, response not assessable (followup_outputs[6] request_levodopa_challenge). Why: rule 1: the library describes a normal motor examination, gait and postural reflexes; proximal weakness 3/5 and inability to stand.
- `order_body_imaging {study: spine_MRI}`: smooth enhancement of the cauda equina roots, ventral more than dorsal; normal cord (fallback_tool_outputs.body_imaging). Why: rule 1: smooth enhancement of the cauda equina and ventral roots is seen in most patients with this polyradiculoneuropathy (Gorson 1996; Byun 1998), while the library reads the roots as normal.
- `order_body_imaging {study: peripheral_nerve_MRI}`: smooth enhancement and mild T2 hyperintensity of the lumbosacral roots, no enlargement (followup_outputs[7] request_peripheral_nerve_mri). Why: rule 1 and 3: the library reads the nerve roots as normal; root enhancement as on the spine MRI of this case.
- `order_specialized_test {test_type: nerve_biopsy}`: segmental demyelination with macrophage infiltration and sparse T-lymphocytes; reduced myelinated fibre density (fallback_tool_outputs.specialized_test). Why: rule 3: the stored nerve conduction study shows absent sural sensory responses bilaterally with a demyelinating pattern; the library sural biopsy is normal.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: active standing not performed (cannot stand unaided); supine BP 146/88 mmHg, HR 96 bpm; sitting BP 140/86 mmHg, HR 102 bpm (followup_outputs[8] request_orthostatic_blood_pressure). Why: rule 3: she cannot stand unaided; the library reports 3 minutes of symptom-free standing at a supine heart rate of 68.
- `interpret_labs {panels: [HbA1c]}`: HbA1c 7.1% (elevated) (fallback_tool_outputs.labs['HbA1c']). Why: rule 2: type 2 diabetes on metformin, with a glucose of 168 mg/dL; the library reports 5.4%.
- `interpret_labs {panels: [quantitative_Ig]}`: IgM 468 mg/dL and IgG 1780 mg/dL (elevated), IgA normal (fallback_tool_outputs.labs['quantitative_Ig']). Why: rule 2: primary biliary cholangitis with end-stage liver disease raises IgM and polyclonal IgG; the library reports normal values.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Cirrhotic liver morphology with splenomegaly and small-volume ascites. No focal liver lesion (followup_outputs[9] request_pelvis_abdomen_ultrasound). Why: rule 2: end-stage liver disease (Child-Pugh B) with ascites on spironolactone is in the history; the library reports a normal liver and no ascites.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Cirrhotic liver with splenomegaly, portosystemic collaterals and small-volume ascites. No focal liver lesion or mass (followup_outputs[10] request_pelvis_abdomen_ct). Why: rule 2: end-stage liver disease (Child-Pugh B) with ascites on spironolactone is in the history; the library reports a normal liver and no ascites.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Cirrhotic liver with splenomegaly, portosystemic collaterals and small-volume ascites. No focal liver lesion on dynamic imaging (followup_outputs[11] request_pelvis_abdomen_mri). Why: rule 2: end-stage liver disease (Child-Pugh B) with ascites on spironolactone is in the history; the library reports a normal liver and no ascites.
- `order_body_imaging {study: chest_abdomen_pelvis_CT}`: Cirrhotic liver with splenomegaly, portosystemic collaterals and small-volume ascites. No focal liver lesion, mass or lymphadenopathy. Chest clear (followup_outputs[12] request_chest_abdomen_pelvis_ct). Why: rule 2: end-stage liver disease (Child-Pugh B) with ascites on spironolactone is in the history; the library reports a normal liver and no ascites.
- Case fallback replaced, `analyze_brain_mri` (fallback_tool_outputs.mri): symmetric T1 hyperintensity of the globi pallidi; no acute abnormality. Why: rule 2: chronic liver disease produces pallidal T1 hyperintensity; the old fallback read a normal brain.
- Case fallback replaced, `analyze_eeg` (fallback_tool_outputs.eeg): mild diffuse slowing (7 Hz posterior rhythm, intermittent theta), no epileptiform discharges. Why: rule 2: grade 1 hepatic encephalopathy with increased confusion and an ammonia of 68 umol/L; the old fallback read a normal awake and drowsy EEG.
- `analyze_eeg {eeg_type: continuous_icu}`: mild diffuse slowing, no seizures or epileptiform discharges (followup_outputs[13] request_continuous_icu). Why: rule 2: grade 1 hepatic encephalopathy with increased confusion; the library reports a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: mild diffuse slowing, no seizures or epileptiform discharges (followup_outputs[14] request_ambulatory). Why: rule 2: grade 1 hepatic encephalopathy with increased confusion; the library reports a normal background.
- `analyze_eeg {eeg_type: video}`: mild diffuse slowing, no seizures or epileptiform discharges (followup_outputs[15] request_video). Why: rule 2: grade 1 hepatic encephalopathy with increased confusion; the library reports a normal background.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 22/30 with attention, executive and recall deficits (followup_outputs[16] request_cognitive_screen). Why: rule 2: grade 1 hepatic encephalopathy and increased confusion are in the case; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: mild impairment of processing speed, attention and set-shifting; recognition and language spared (followup_outputs[17] request_neuropsych_battery). Why: rule 2: grade 1 hepatic encephalopathy and increased confusion are in the case; the library reports normal cognition.
- `order_body_imaging {study: chest_CT}`: no thoracic abnormality; cirrhotic liver, splenomegaly and ascites on the upper abdominal sections (followup_outputs[18] request_chest_ct). Why: rule 3: end-stage liver disease with ascites is in the history and the upper abdomen lies in a chest CT; without its own report this order received the chest-abdomen-pelvis report, which describes the pelvis as well.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
