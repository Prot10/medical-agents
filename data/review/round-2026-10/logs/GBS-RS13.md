# GBS-RS13
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| d8e03a5d-cbfa-435b-aa48-631f00e62672 | FIXED | The agent acts on hospital day 2, at the deterioration and before intubation (plan RS13). Every block is date-stamped (the exam fields say "Day 2:"; HPI events are dated day 0, 1 and 2) or reports day 2 or earlier. Day 6 piperacillin/tazobactam is deleted from `neurological_exam.additional` (now null). The NCS is a bedside study on hospital day 2, not day 12, with an early demyelinating pattern. Telemetry covers the first 24 h (days 1-2): the day 5 atropine, day 7 labetalol and day 10 AF events are gone, as is any treatment. CK on day 2 is 9,640 U/L, a plausible fall from 20,518 in 2 days (it was 2,840 "normalising"). The respiratory step reports the current pre-intubation bedside values, not "intubated on day 2". Intubation is now must 1. |
| bff624ff-29ed-42e4-a6df-d534121ee014 | FIXED | Option chosen: corrected protein (plan RS13). The CSF interpretation states that at about 1 mg/dL of protein per 1000 RBC/mm3, the 450 RBC/mm3 account for under 1 mg/dL of the 92 mg/dL (Kind 2, a laboratory statement). a3 expected_evidence is specific to the case: protein not explained by the RBC, and 8 cells/mm3 compatible but prompting exclusion of infection (Gram stain and culture negative). KCE 2 states the rule. CSF EBV/CMV PCR were removed (not orderable, no indication). HSV PCR stays. The "(traumatic tap / SAH-related)" and "SAH adds to protein" annotations are replaced by one hedged interpretation. |
| 9f5289ae-40c4-43c9-82c8-0b80ecf87a67 | FIXED | CIP/myopathy very_low: onset on day 2, before the 1-2 weeks of critical illness they need; demyelinating, not axonal, NCS (KCE 3). Sepsis-associated weakness/meningitis very_low: no source on examination (chest clear, wounds clean, now in `physical_exam.general`), admission blood cultures without growth at 48 h (moved from the lab panel to dated history), CSF Gram stain and culture negative with 8 lymphocytic cells. The fever with leukocytosis is now `red_herrings[1]`, resolved as the post-trauma and crush response. Rhabdomyolysis low (plan RS13). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `neurological_exam.additional` | Editorial sentences: "raised concern for ... myelopathy" and "likely represent PRES ... these do not explain the peripheral areflexia" (the latter resolves a red herring for the agent). "AFTER the trauma" in capitals. Admission findings were duplicated across the HPI and exam (C7). | FIXED: the HPI is a dated narrative. The MRI is reported as history ("reported as consistent with PRES", DWI negative). Pertinent negatives added: unchanged consciousness, no new headache or vomiting, moving all limbs on day 1. `additional` set to null. |
| C | major | HPI (history) | An LP after an acute subdural haematoma needs a statement on mass effect. The case gave none. | FIXED: the admission CT now says "thin convexity subdural haematoma without mass effect or midline shift". |
| C | major | `followup_outputs` respiratory | It said "FVC not measurable - intubated on day 2", and SpO2 93% was flagged "(H)" (C1). | FIXED: canonical format, pre-intubation: FVC 1.3 L (35% predicted; 16 mL/kg at 80 kg) L, MIP -22 L, MEP 30 L, cough weak, best of three with variable effort from confusion, SpO2 93% room air. Weight 80 kg and height 175 cm added (BMI 26.1 agrees). |
| C | major | `ground_truth.assessment` | "Intubation if respiratory failure" and "Initiate IVIG / plasma exchange" were generic. Nothing addressed succinylcholine or donepezil, aspirin with traumatic haemorrhage, or thromboprophylaxis (C8). | FIXED: must 1 intubate electively now, naming the values and clinical signs. Must 2 no succinylcholine (denervation hyperkalaemia, donepezil potentiation). Must 3 IVIg 2 g/kg (about 32 g/day at 80 kg) or PE with relative cautions. Must 4 telemetry and holding donepezil. Must 5 hold aspirin, agree restart with neurosurgery. Must 6 mechanical then LMWH thromboprophylaxis [Leonhard_2019]. Prohibitions: canonical steroid, renal function before IVIg, no succinylcholine. |
| C | major | `action-6-check-drug-interactions`, DDI output | The DDI output listed the medicines with no content, plus taper boilerplate. Donepezil (succinylcholine potentiation, vagotonic, QT with QTc 462) and aspirin (ICH, line placement) are concrete interactions (plan 3.1 item 7). | FIXED: a6 required, with the soft constraint labs before DDI. Category-level DDI output with product-labelling sources; aspirin noted as not a contraindication to LP. The empty DDI follow-up was deleted (C9). |
| C | major | `initial_tool_outputs.labs` | CSF culture, CSF EBV/CMV IgG and CSF HSV PCR sat in the serum lab panel. Blood culture was reported as "Serology". HIV carried the leaky sentence (C10). There was interpretation inside the summary ("stress response", "normalizing"). No platelets, coagulation, glucose, liver tests or albumin. | FIXED: CSF items removed (the CSF report carries HSV PCR). Blood cultures moved to dated history. HIV removed (no risk). Platelets 214, CMP with AST 96 H (muscle-pattern rise with CK) and albumin 3.7, CK 9,640, coagulation normal. a1 adds `coagulation`, with a soft constraint a1 before a3 (traumatic ICH on aspirin). |
| C | minor | `initial_tool_outputs.specialized_test` | Day-12 "severe" study on a day-2 assessment, with "meets electrodiagnostic criteria" phrasing and no needle EMG. | FIXED: bedside study on day 2. Values meet Hadden demyelination criteria in two nerves (DML above 110% of the upper limit, CV below 90% of the lower limit), with absent F and H, sural sparing, and needle EMG without denervation. Hedged impression; `test_type` "emg_ncs". |
| C | major | `ground_truth.action_criteria` a9, order | Spine MRI was optional although new flaccid quadriparesis after a fall must be imaged for cord injury (must 3 asked for it). Respiratory function sat fourth in a patient desaturating with bulbar weakness. | FIXED: a9 recommended (plan said keep; see Open questions). Expected_evidence and rationale are case-specific, and the MRI report covers the whole spine (no cord lesion, fracture, ligamentous injury or epidural haematoma; cauda equina enhancement hedged). Criteria and pathway order: respiratory function first, then spine MRI, NCS, labs, CSF, telemetry, ECG, DDI, literature. |
| A | major | `followup_outputs` | Ganglioside follow-up (typical GBS; C2), with the "seronegative" label and pearl depending on it. Empty literature follow-up (C9). | FIXED: deleted. The label no longer says "seronegative" and the pearl is canonical. |
| D | major | literature | Echoed a5's expected_evidence (C11). | FIXED: canonical general output; a5 optional and last. |
| B | major | `fallback_tool_outputs.ct`, `.mri` | The fallback head CT said "No haemorrhage" and the fallback MRI showed only a pineal cyst, both contradicting the known SAH, subdural and parieto-occipital lesions. | FIXED: both rewritten as repeat studies unchanged from admission. `metadata.fallback_tool_kinds` ct and mri set to "case_specific". |
| C | minor | `ground_truth.avoided_actions` | Head CT was listed as waste in a trauma patient with intracranial haemorrhage and a new deficit, where a repeat CT is reasonable. Bare citations. | FIXED: CT waste removed. Brain MRI waste kept, with a case reason (done on admission). Citations [EAN_PNS_2023]. |
| C | major | `ground_truth.differential` | Cord trauma and CIP stayed moderate after MRI and NCS. Sepsis reason generic. Central lesions and rhabdomyolysis missing (C5). | FIXED: cord injury, CIP/myopathy, sepsis/meningitis, central cause and hypokalaemia very_low; rhabdomyolysis low; acute-onset CIDP low; each with the case findings. |
| C | minor | `key_clinical_evidence`, `diagnosis.accepted[0]`, `red_herrings` | "Trauma and severe stress are recognised triggers ... through immune dysregulation" overstates a 2-day latency. The label said "(trauma / stress trigger), seronegative - ICU course". There was one red herring. | FIXED: label "Severe Guillain-Barré syndrome (acute inflammatory demyelinating polyradiculoneuropathy) after head trauma". KCE 4 says the 2-day interval is short and the diagnosis does not rest on a trigger. Six pearls. Red herrings: trauma, fever with leukocytosis, PRES-like lesions, tetanus toxoid (2 days too early). |
| C | minor | telemetry, ECG | The 10-day report gave treatments. a7 and a8 expected_evidence were templates. | FIXED: 24 h findings (sinus tachycardia 96-124, labile blood pressure 132/70 to 182/98). The ECG interpretation is reworded with no value changes. a7 and a8 expected_evidence describe them. |
| E | minor | criteria, sequence, stop rule, metadata | Template constraints, stop rule including literature with max 0, free-text citations, difficulty rationale. | FIXED: plan 3.3. Stop rule: the six required criteria, max 3. |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-RS13 is now a coherent hospital day 2 case. A 72-year-old man with vascular dementia was admitted after a fall with a small traumatic SAH and a thin subdural haematoma without mass effect. Since this morning he has rapidly ascending areflexic quadriparesis with bulbar weakness and SpO2 93%. Every report is dated day 2 or earlier. The bedside NCS shows an early demyelinating pattern. Telemetry covers the first 24 hours (tachycardia, labile blood pressure, no treatment). CK is falling after the crush injury. The CSF protein of 92 mg/dL with 450 RBC/mm3 is explicitly not explained by the blood (about 1 mg/dL per 1000 RBC). Pre-intubation respiratory values (FVC 16 mL/kg, MIP -22, MEP 30, weak cough) lead to must 1, elective intubation now, without succinylcholine. Donepezil potentiates succinylcholine and adds vagotonic and QT effects, and aspirin matters with the haemorrhage, so the interaction check is required. IVIg 2 g/kg is started. Whole-spine MRI is recommended to exclude cord injury. CIP, sepsis, rhabdomyolysis and central causes are lowered, each with the finding that excludes it, and the fever, PRES-like lesions and tetanus toxoid are red herrings.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- `ground_truth.diagnosis.accepted[0]` changed (reviewer notes on timeline and trigger; plan C2/C3): "Severe Guillain-Barré syndrome (acute inflammatory demyelinating polyradiculoneuropathy) after head trauma". Synonyms untouched.
- Plan CENTRAL 5 (weight field) and 10 (respiratory-report guard).

## Open questions for Andrea (judgment calls you could not settle)
- Decided, not open: plan RS13 kept a9 (spine MRI) optional. I made it recommended, because new flaccid quadriparesis after a fall must be imaged for a cervical cord injury (spinal shock is also areflexic). This matches GBS-RS12.
- Decided, not open: I put respiratory function first in the criteria and pathway order, instead of plan 3.1's NCS-first order, because the patient is desaturating with bulbar weakness and the intubation decision comes before the diagnostic work-up.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case, including the rewritten CT and MRI fallbacks.
- Note d8e03a5d: FIXED holds. Every block reports day 2 or earlier (NCS bedside day 2, telemetry days 1-2 without treatment, labs day 2 with CK 9,640, pre-intubation respiratory values); no day 5-12 event remains; admission CT, MRI and CK are dated history and none is a scored study (brain MRI is waste, CT is not scored).
- Note bff624ff: FIXED holds. The correction (about 1 mg/dL per 1000 RBC, so 450 RBC add under 1 mg/dL) is arithmetically right and stated as a laboratory fact; a3 expected_evidence is case-specific.
- Note 9f5289ae: FIXED holds. CIP/myopathy very_low (onset day 2, demyelinating NCS); sepsis very_low with named negatives (blood cultures no growth at 48 h, CSF Gram stain and culture negative, no source); fever with leukocytosis is a red herring.
- Arithmetic: FVC 1.3 L = 16 mL/kg at 80 kg and 35% of a 3.7 L predicted; IVIg 32 g/day at 80 kg; BMI 26.1 agrees; glucose ratio 58/85 = 0.68. Musts (elective intubation now, no succinylcholine, IVIg, telemetry, hold aspirin, thromboprophylaxis) agree with the prohibitions and with the DDI output. Respiratory-first criterion order is justified by the desaturating bulbar patient.
- No errors found; no change made.
- perfect_agent.py GBS-RS13 -v passes; case_io.py check clean for the case.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
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

- criterion `action-6-check-drug-interactions` rationale: "Donepezil changes the choice of neuromuscular blocker and adds to bradyarrhythmia and QT risk with a QTc of 462 ms; aspirin bears on the haemorrhage and on procedures (ROUND_POLICY ruling 6)." -> "Donepezil changes the choice of neuromuscular blocker and adds to bradyarrhythmia and QT risk with a QTc of 462 ms; aspirin bears on the haemorrhage and on procedures."

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 74.5 -> 80 kg, height 169 -> 175 cm, BMI 26.1 -> 26.1 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 80 kg, height 175 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.
