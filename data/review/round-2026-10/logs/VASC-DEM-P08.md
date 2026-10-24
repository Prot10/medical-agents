# VASC-DEM-P08
Reviewer status: R1 none, R2 none (VASC-DEM has no notes file; never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (classes C1-C19) and from my own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `action-9-search-medical-literature`, literature outputs | Plan C2 leak. | FIXED: criterion deleted, initial null, fallback deleted. |
| C | major | `action-10-check-drug-interactions`, `initial_tool_outputs.drug_interactions`, drug fallback | Plan C3: the interrogation shows AF (2.1% burden), so group R applies. The old criterion was an optional anticholinergic review that did not fit a patient on no anticholinergic drug. | FIXED: recommended, one alternative per drug (apixaban, rivaroxaban, edoxaban, dabigatran, warfarin); case output keyed by each drug (anticoagulant with aspirin roughly doubles major bleeding, stop aspirin; no interaction with ramipril, amlodipine, atorvastatin; dose criteria); fallback deleted. |
| B | major | `action-6-order-cardiac-monitoring`, `initial_tool_outputs.cardiac_monitoring.monitor_type` | Plan C11: a pacemaker interrogation coded as an implantable loop recorder. | FIXED: criterion `order_cardiac_monitoring {}`; `monitor_type` "pacemaker interrogation, stored device diagnostics"; impression lists the stored data only (no "no external monitor could match", no "anticoagulable second mechanism"); the "six weeks before the second clinical event" link removed from the report. |
| B | minor | `action-8-order-ct-scan.alternatives` | Plan: `angiography`/`contrast` arguments. | FIXED: `order_ct_scan {}`. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: MoCA total and item losses in the exam. | FIXED: bedside observation ending "Formal cognitive screening reported separately". |
| D | major | `initial_tool_outputs.clinical_assessment` | Plan C5: impression "The clinical evidence for a left hemispheric vascular substrate is strong"; "impaired" and "retrieval pattern" judgments; `criteria_met` carried the history's "stepwise course"; fluency "9 animals" is not the MoCA item. MoCA arithmetic checked: 11 points lost = 19/30; 13 years of education, no point added. | FIXED: results-only impression; findings give item scores (naming 3/3, repetition 2/2, orientation 5/6 added); letter fluency "9 words beginning with F"; stepwise criterion removed. |
| D | major | `initial_tool_outputs.specialized_test.impression` | "a left-hemisphere-weighted profile matching the two left cortical infarcts seen on CT" (cross-modality). | FIXED: profile with percentiles only; `quantitative_data.pattern` descriptive. |
| D | major | `initial_tool_outputs.ct` | Plan C5: observations gave the clinical MRI contraindication, "satisfies the vascular attribution" and the antithrombotic consequence; impression "Sufficient to attribute the dementia to cerebrovascular disease". | FIXED: technique and limitations only (microbleeds, siderosis, Fazekas, MTA not assessable); numbered impression; dashes removed from findings. Red herring `findings[3]` unchanged. |
| C | major | `initial_tool_outputs.advanced_imaging`, criterion evidence, differential, KCE | "60-70% by NASCET" from a duplex with PSV 224 cm/s, EDV 78 cm/s, ICA/CCA 3.8: all three sit in the consensus 50-69% band (PSV 125-230), and duplex does not measure NASCET directly; "60-70%" also straddles the 70% revascularisation threshold. The impression also linked the stenosis to the infarcts and the pacemaker. | FIXED: "50-69% (consensus velocity criteria)" everywhere; impression lists the findings only. |
| D | minor | `initial_tool_outputs.ecg.interpretation` | "interrogating it is the most informative available test" (recommendation). | FIXED: rhythm, pacing mode and limitation only. |
| B | major | `initial_tool_outputs.labs` | Plan C6: female Hb/Hct ranges in a man; eGFR 60 against ">60" flagged normal; eGFR inconsistent with creatinine 1.1 at age 79 (CKD-EPI 2021 about 68); template values; interpretive interpretation. | FIXED: male ranges, Hct 41.2; eGFR 68 with range ">=60"; WBC 7.1, Plt 205, MCV 91, Na 140, K 4.5, ALT 18, albumin 3.9, folate 9.4; interpretation lists flagged values (glucose, HbA1c) only. |
| B | minor | `patient.physical_exam.general` | No weight, needed for DOAC dosing (Cockcroft-Gault). | FIXED: weight 75.1 kg, height 172 cm (BMI 25.4 as recorded); CrCl about 58 mL/min, so standard doses of every DOAC. |
| B | minor | `ground_truth.action_criteria` | Plan C13 (label = rationale, double citations); order per C16. | FIXED: case rationales and evidence, bracketed keys only; order screen, neuropsych, labs, CT, ECG, carotid, monitoring, drug check. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | Plan C16: none; max 0. | FIXED: soft screen before CT and ECG before monitoring; max 1; required set unchanged. |
| C | major | `ground_truth.assessment.required_recommendations` | Four of seven musts were tool steps (interrogate, image carotids, obtain CT, exclude reversible causes); "refer for revascularisation" of a stenosis whose last event was 8 months ago; no BP, LDL or concrete DOAC must. | FIXED: six musts: record the MRI contraindication and that CT cannot exclude CAA [STRIVE_2]; DOAC with dose reasoning and stop aspirin; best medical therapy for the stenosis with vascular team decision (plan wording); BP below 130/80 gradually; LDL below 70 (96); supervised medication administration (missed doses). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Plan C11 wording; two-part microbleed item; em dashes. | FIXED: loop recorder item per plan; microbleed item "Do not withhold anticoagulation because microbleed status cannot be assessed [ESC_AF_2024]"; others reworded. |
| C | major | `ground_truth.differential` | Plan C8: AD `moderate` although recall is cue-responsive and recognition preserved. | FIXED: AD `low` with key features; CAA stays `moderate` ("cannot be excluded on CT"); cardioembolism entry updated to 50-69%. |
| C | minor | `ground_truth.avoided_actions[*].rationale` | Plan C18. | FIXED: case-specific; MRI harm stays. |
| B | minor | `ground_truth.red_herrings[0].field_path` | Empty. | FIXED: `patient.clinical_history.past_medical_history[0]`. |
| B | major | `fallback_tool_outputs` | Plan C7: advanced_imaging, labs, literature and drug giveaways; echo impression "No cardioembolic source identified". | FIXED: four fallbacks deleted; echo impression descriptive, pacing lead noted; `metadata.fallback_tool_kinds` updated. No CT fallback (CT is the initial study). |
| E | minor | `ground_truth.key_clinical_evidence`, `metadata.key_educational_points` | Em dashes. | FIXED: reworded. |
| E | minor | `ground_truth.diagnosis.accepted[0]` | Em dash in the label (not editable). | FLAGGED. |
| - | check | plan 3.6 | perfect_agent.py ok (drug check served by key, CT and carotid from initial outputs; probe confirms no fallback or library); `test_case_guards -k VASC-DEM-P08` 2 passed; `case_io.py check` schema OK, no failure names P08. | - |

## Changes, in one paragraph a physician can read before re-reviewing

Same case: a 79-year-old man with a non-MR-conditional pacemaker for complete heart block and a two-step decline after two right-sided events, worked up on CT, carotid duplex and pacemaker interrogation. Reports now describe only their own findings: the CT states its technique and what it cannot show (microbleeds, siderosis, Fazekas grade, medial temporal atrophy), the device report lists the stored AF data, and no report attributes the dementia. The carotid stenosis is now 50-69%, which is what the recorded velocities show. Labs use male ranges and an eGFR that matches the creatinine; a weight was added for DOAC dosing. Alzheimer disease is now low; amyloid angiopathy stays moderate because CT cannot exclude it. Musts are now concrete: record the MRI contraindication and the CT limitation, start a DOAC at standard dose and stop aspirin, best medical therapy for the stenosis (last event 8 months ago) with a vascular team decision, BP below 130/80, LDL below 70, and supervised medication. A drug-interaction check is a recommended step.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C11: add a `device_interrogation` term to `order_cardiac_monitoring` in `costs.yaml`, the library and the `tool_io.py` mirror. Until then the criterion is `{}` and any `monitor_type` (including `holter_24h`) is served the 12-month interrogation report, which is inconsistent for an external monitor.
- New citation key used: `[ESC_AF_2024]` (plan 5.4).
- Synonyms (plan 5.1): `F06.7` should not be credited for this dementia case.

## Open questions for Andrea (judgment calls you could not settle)

- None. (The carotid-grade question raised here was closed at verification: the stored velocities meet the 50-69% consensus band.)

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case. Verified: carotid grade 50-69% is what the stored velocities give by the consensus criteria (PSV 224 cm/s within 125-230, EDV 78 within 40-100, ICA/CCA 3.8 within 2-4), so the worker's open question is settled in favour of 50-69% and closed; the last event 8 months ago puts it beyond 6 months, matching the best-medical-therapy must; apixaban 5 mg twice daily is right (age 79, weight 75.1 kg, creatinine 1.1: no criterion), Cockcroft-Gault about 58 mL/min; BMI 25.4 matches the added weight and height; eGFR 68 matches CKD-EPI; MoCA arithmetic (11 points lost = 19/30) and exam (month incorrect) agree; left MCA cortical infarcts match the right-sided exam and history; device report gives AF burden and longest episode without management text; ECG before monitoring and screen before CT soft constraints; aspirin-stop must, drug output and prohibition agree; MRI harm kept; red herring `initial_tool_outputs.ct.findings[3]` is the periventricular low attenuation row.
Found and changed: `patient.clinical_history.past_medical_history[3]` described both events as "transient right arm weakness", contradicting the HPI (the second event was a day of right hand clumsiness with word-finding difficulty, and each left a permanent step down). Rewritten as "Two episodes of right-sided neurological deficit, neither imaged: an hour of right arm weakness 2 years ago and a day of right hand clumsiness with word-finding difficulty 8 months ago". perfect_agent.py pass; case_io.py check: schema OK, no failure names P08; test_case_guards pass.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Total cholesterol]` | Total cholesterol 184 mg/dL did not equal LDL + HDL + TG/5 (170.6); the same lab-arithmetic class was fixed in M07-M10, P01, P02 and S06-S11 but not here. | FIXED: total cholesterol 171 mg/dL (flag unchanged; LDL, HDL and TG, which the musts and evidence quote, unchanged). |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.
