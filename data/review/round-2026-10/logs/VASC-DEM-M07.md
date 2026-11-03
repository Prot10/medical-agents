# VASC-DEM-M07
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (`plans/VASC-DEM.md`) and the worker's own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: `required_arguments` held the non-schema key `sequences` plus `protocol`/`contrast`, so no real MRI call could match the required criterion. | FIXED: one alternative `analyze_brain_mri {}`. |
| D | major | `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search`, criterion `action-8-search-medical-literature` | Plan C2 / ruling 5: literature criterion (recommended) whose output repeated its own expected_evidence (leak test failure). | FIXED: criterion deleted; initial output null; fallback deleted. |
| C | major | criterion `action-9-check-drug-interactions`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group R: generic optional `{}` check with a generic "no prohibitive interaction" fallback, although the patient will be offered a cholinesterase inhibitor while on bisoprolol for AF (additive bradycardia). | FIXED: tier recommended; alternatives `{"drug": "donepezil"}`, `rivastigmine`, `galantamine`; three case-specific outputs (pharmacodynamic bradycardia with bisoprolol, ECG and heart rate before and after starting, no interaction with apixaban, ramipril, atorvastatin, levothyroxine); generic fallback deleted. Wording checked against the leak guard. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: exam gave the MoCA total and item scores, the result of the required screen. | FIXED: bedside observation (orientation, repeated questions, word-finding pauses) and "Formal cognitive screening reported separately". |
| B | major | `initial_tool_outputs.clinical_assessment` (findings, impression, scores) | MoCA arithmetic did not add up: the listed losses (orientation month and date, clock 1/3, etc.) sum to 16/30, not 18/30; "fluency 8 animals" is not the MoCA letter-fluency item. | FIXED: orientation date only (5/6), clock 2/3, letter fluency 8 words; impression lists points lost summing to 18/30. |
| D | major | `initial_tool_outputs.clinical_assessment.impression`, `.criteria_met` | Plan C5: screen impression named Alzheimer disease and the vascular question; `criteria_met` carried interpretive items (`amnestic_predominant_profile`, `independence_in_iadl_lost`, `stepwise_course`) that state the severity and course, not test results. | FIXED: impression is totals and losses only; `criteria_met` keeps `impairment_in_at_least_one_domain` and `recall_improves_with_cueing` (false). Informant FAQ 20/30 kept as an instrument score. |
| D | major | `initial_tool_outputs.specialized_test.impression` | Plan C5: neuropsych impression attributed the amnesia to Alzheimer pathology and the executive part to the vascular burden. | FIXED: numbered profile (storage-type memory deficit, set-shifting and speed impairment, mild anomia) without disease names. |
| D | major | `initial_tool_outputs.mri.additional_observations`, `.impression`, `.volumetrics` | Plan C5: "neither pattern alone accounts for the syndrome", "speaks to effective anticoagulation", "supports mixed pathology", "well beyond the age-adjusted range". | FIXED: STRIVE-2 descriptors only; numbered impression (MTA 3 with temporoparietal atrophy; Fazekas 2, two lacunes, one deep microbleed; no cortical infarct, no lobar microbleed, no cSS). Finding order unchanged, so the red-herring path `mri.findings[4]` still points to the microbleed. |
| D | major | `initial_tool_outputs.csf.interpretation` | Plan C5: CSF interpretation stated "the diagnosis is mixed Alzheimer and vascular dementia". | FIXED: values and pattern only. |
| B | minor | `initial_tool_outputs.csf.glucose_ratio` | 0.63 with serum glucose 96 mg/dL (64/96 = 0.67). | FIXED: "0.67 (serum glucose 96 mg/dL)". |
| D | major | `initial_tool_outputs.advanced_imaging` (FDG PET) | Plan C5: findings labelled "Alzheimer pattern", "Vascular contribution"; impression "typical of Alzheimer's disease ... supports mixed pathology"; `quantitative_data.pattern: mixed`. | FIXED: regional descriptions, impression "pattern consistent with an Alzheimer-type metabolic profile" (style guide wording) plus the patchy frontal defects; `pattern` key removed. |
| B | major | `initial_tool_outputs.labs` | Plan C6: template values (WBC 6.8, Hct 41.6, Plt 238, MCV 88, Na 139, K 4.2, ALT 22, albumin 4.1, folate 11.8); Hct 41.6 inconsistent with Hb 12.8; eGFR 60 against ">60"; HDL range ">40" in a woman; total cholesterol 184 inconsistent with LDL 98 + HDL 54 + TG/5 (178); interpretation "LDL above target ... excluding hypothyroid cognitive impairment". | FIXED: WBC 7.4, Hct 38.6, Plt 261, MCV 91, Na 141, K 4.5, ALT 17, albumin 3.9, folate 9.6; eGFR 62 (CKD-EPI 2021 for creatinine 0.94, woman of 78) with range ">=60"; HDL range ">50"; total cholesterol 178; interpretation "Flagged: HbA1c 5.7% (high). Other results within reference ranges." |
| B | major | `fallback_tool_outputs.cardiac_monitoring` | Holter fallback reported "sinus rhythm throughout, no atrial fibrillation" in a patient with 4 years of AF and an irregularly irregular pulse. | FIXED: AF throughout, mean rate 74, no pauses. |
| B | major | `initial_tool_outputs.ecg` (new) | No ECG output: an ECG order (reasonable before a cholinesterase inhibitor on bisoprolol) would have returned the library's normal sinus rhythm, contradicting the AF. | FIXED: authored ECG (AF, controlled rate 74, QTc 426 ms) and new optional criterion `action-10-analyze-ecg`. |
| B | minor | `fallback_tool_outputs.echo` | LA "normal size" after 4 years of AF; impression "No cardioembolic source identified" (verdict). | FIXED: LA mildly dilated (LAVI 38 mL/m2); impression lists findings. |
| D | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, `.labs` | Plan C7: CT fallback "better characterised on the MRI already obtained"; non-contributory advanced-imaging and labs fallbacks. | FIXED: CT fallback describes what CT shows in this patient (white matter hypodensity, two lacunes, atrophy, CT limitation); advanced-imaging and labs fallbacks deleted; `metadata.fallback_tool_kinds` trimmed to the remaining fallbacks. |
| C | major | criterion `action-6-analyze-csf` | Plan C9: biomarker route CSF only; LP needs apixaban interrupted. | FIXED: id kept; label "Establish amyloid status with CSF Alzheimer biomarkers or amyloid PET"; alternatives CSF special_tests and `order_advanced_imaging {"modality": "amyloid_PET"}`; required; new follow-up `followup_outputs[0]` amyloid PET (18F-florbetaben, positive, BAPL 3, Centiloid 74) consistent with the CSF. Rationale notes that LP needs apixaban withheld and PET avoids that. Probed: amyloid_PET returns the follow-up, FDG_PET returns the initial FDG report. |
| A | minor | all criteria `citations`, `rationale`, `expected_evidence` | Plan C13: rationale equal to label; duplicated unbracketed keys; em dashes in expected evidence. | FIXED: one-sentence case rationales, bracketed keys only, expected evidence rewritten with the case's values. |
| B | minor | `ground_truth.action_criteria` order | Plan C16: neuropsych after MRI. | FIXED: screen, neuropsych, labs, MRI, ECG, amyloid biomarker, FDG, drug check. |
| C | major | `ground_truth.assessment.required_recommendations` | Plan C19: musts restated tool steps (characterise memory, read the MRI, obtain biomarkers, exclude reversible causes) and were unspecific ("treat both components"). | FIXED: five musts: name mixed dementia; cholinesterase inhibitor (donepezil 5 then 10 mg) with heart rate and ECG checks because of bisoprolol [NICE_NG97]; continue apixaban 5 mg twice daily, CHA2DS2-VA 3, dose criteria not met [ESC_AF_2024]; BP gradually below 130/80 from 148/80 with orthostatic checks [ESO_2021_SVD]; caregiver support, driving, advance care planning, 6-12 month review [NICE_NG97]. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Em dash; no prohibition on adding an antiplatelet to apixaban for covert lacunes. | FIXED: reworded six prohibitions, including no antiplatelet for covert SVD on top of apixaban [ESO_2021_SVD] and no stopping or reducing apixaban for one deep microbleed or age. |
| C | major | `ground_truth.differential` | Plan C8: "Alzheimer's disease alone" moderate after a positive amyloid biomarker and an established vascular burden. | FIXED: low, key features rewritten; vascular-alone and cardioembolic entries reworded. |
| B | minor | `ground_truth.key_clinical_evidence`, `red_herrings[0]` | "Anticoagulation has worked" overclaim; AF red herring had empty field_path and location "history". | FIXED: reworded; red herring points to `patient.clinical_history.past_medical_history[1]`. |
| C | minor | `ground_truth.avoided_actions` | Plan C18: generic rationales (CT "already obtained", echo and monitoring "pure small-vessel disease"). | FIXED: case-specific rationales (gradual course, no Lewy features, AF already documented and anticoagulated, CT canonical text). |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | Plan C16: no MRI-before-CSF; `max_additional_actions` 0. | FIXED: soft MRI before the amyloid-biomarker criterion added; stop rule = the four required ids, `max_additional_actions` 1. |
| B | minor | `metadata.difficulty_rationale`, `.key_educational_points` | Referred to "the biomarker" route only. | FIXED: "amyloid biomarker (CSF or PET)"; added the AChEI-bisoprolol point. |

## Changes, in one paragraph a physician can read before re-reviewing

The case remains a 78-year-old woman with four years of gradual amnestic decline, anticoagulated atrial fibrillation and a mixed Alzheimer and small-vessel picture. The exam no longer gives the MoCA; the screen itself now adds up to 18/30 (delayed recall 0/5, not rescued by cueing, plus executive, visuospatial, attention and date losses) and no report names the diagnosis: the screen, neuropsychology, MRI, CSF and FDG-PET report only their own findings. The required biomarker step can be met by CSF (unchanged values: Abeta42/40 0.042, p-tau181 96) or by a new positive amyloid PET (Centiloid 74). An ECG showing controlled AF was added (optional) because the plan now offers a cholinesterase inhibitor while she takes bisoprolol, and the drug check is recommended and case-specific (bradycardia). The Holter fallback no longer reports sinus rhythm. Labs carry female ranges, non-template values, eGFR 62 and a consistent lipid panel. The literature step is gone. Musts: mixed dementia named; donepezil with heart rate and ECG checks; continue apixaban 5 mg twice daily (CHA2DS2-VA 3) despite one deep microbleed; BP to below 130/80 gradually; caregiver, driving and planning. "Alzheimer disease alone" is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[NICE_NG97]` (cholinesterase inhibitor for mixed dementia, ECG check, care planning), `[ESC_AF_2024]` (plan 5.4).
- Synonyms (plan 5.1): this mixed case currently accepts bare "vascular dementia" and F06.7; per the plan, add a mixed-dementia entry and stop crediting bare "vascular dementia" and F06.7 here.

## Open questions for Andrea (judgment calls you could not settle)

- None. Decision recorded: the plan did not list an ECG for M07; I added an optional ECG with an authored AF report because the library default (sinus rhythm) would contradict the case, and a baseline ECG is reasonable before a cholinesterase inhibitor in a patient on a beta-blocker.

## Verification

Adversarial check (24 Oct 2026) against the plan and the final file. No reviewer notes exist, so no note id can be missing. Checked: MoCA items sum to 18/30 and match the exam (date only wrong, 5/6); eGFR 62 matches creatinine 0.94 in a woman of 78 (CKD-EPI 2021); Hct 38.6 about 3 x Hb 12.8; Friedewald total cholesterol 178; apixaban 5 mg is correct (age 78, creatinine 0.94, so at most one reduction criterion); CHA2DS2-VA 3 (hypertension, age 75 or more); CSF glucose ratio 64/96 = 0.67; the amyloid-PET and CSF alternatives of `action-6-analyze-csf` are both answered by case outputs; the AF fallbacks (Holter, echo LA) agree with the ECG and the irregular pulse; no report names the diagnosis or the severity; drug-check outputs are case-specific and pass the leak guard; differential matches the final evidence; musts and prohibitions do not contradict each other or the avoided actions.

Found and fixed: the new amyloid-PET follow-up gave Centiloid 74 with a florbetaben composite SUVR of 1.58, which by the florbetaben Centiloid transformation (CL = 153.4 x SUVR - 154.9, whole-cerebellum reference) corresponds to about 88. Changed `followup_outputs[0].output.quantitative_data` to "Composite cortical SUVR (whole-cerebellum reference)": "1.49" (Centiloid 74 unchanged, so the criterion's expected evidence still holds).

Checks re-run after my edits: `perfect_agent.py -v` passes (every required and recommended criterion answered by case data); `case_io.py check` clean for this case (schema, synonym guard, no test failure naming it). Note for the lead, not changed: `metadata.fallback_tool_kinds` still labels case-specific fallbacks (CT with this patient's lesions, AF Holter where present) as "normal"; the field is read by no code or test, so I left it rather than churn it.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here mixed-dementia labels and F00.2 only; generic F01 entry excluded. A vascular-only answer ("vascular dementia", "VaD") no longer scores; accepted: "mixed dementia", "alzheimer vascular dementia" (both spellings), "alzheimer cerebrovascular disease" (both spellings). Code-alone limitation: an answer coded F01.50 still matches (CENTRAL).
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: cardiac_monitoring normal->case, ct normal->case, echo normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

A fresh order of each study below was answered by the benchmark-level normal library, which contradicted this patient (age, rhythm, devices, surgery, stored findings). Each now has a case-specific report:

- perfusion_SPECT: Bilateral temporoparietal and posterior cingulate hypoperfusion, a pattern consistent with an Alzheimer-type profile, with additional patchy frontal hypoperfusion. (fallback_tool_outputs.advanced_imaging)
- performance_status: Karnofsky 60 (requires occasional assistance but able to care for most needs), ECOG 2 (ambulatory and capable of all self-care, unable to carry out any work activities). (fallback_tool_outputs.clinical_assessment)
- exercise_stress_test: Reduced exercise capacity (3.4 METs) in atrial fibrillation; non-diagnostic for ischaemia. (fallback_tool_outputs.specialized_test)
- tau_PET: Tau-positive PET: neocortical tau signal in the medial and inferior temporal cortex bilaterally, extending to the lateral temporoparietal cortex and the posterior cingulate and precuneus. (followup request_tau_pet)
- gait_and_balance_timed: Mildly slowed gait with reduced step length (Timed Up and Go 13.8 s). (followup request_gait_and_balance_timed)
- levodopa_challenge: MDS-UPDRS III 8/132 OFF and 8/132 ON (0% change), below the 30% threshold for a clinically meaningful levodopa response. (followup request_levodopa_challenge)
- TEE: Mild concentric left ventricular hypertrophy; mildly dilated left atrium; atrial fibrillation with low appendage emptying velocity and mild spontaneous echo contrast, without appendage thrombus; aortic valve sclerosis without stenosis. No patent foramen ovale and no left atrial appendage thrombus. (followup request_tee)
- cardiac_MRI: Mildly dilated left atrium, imaged in atrial fibrillation; preserved left ventricular function; no scar or thrombus. (followup request_cardiac_mri)
- electrophysiology_study: Atrial fibrillation throughout; normal His-Purkinje conduction (HV 48 ms); no inducible ventricular arrhythmia. (followup request_electrophysiology_study)
- speech_language_evaluation: Mild anomia with word-finding pauses in fluent speech; repetition and comprehension intact; no motor speech disorder. (followup request_speech_language_evaluation)
- DTI_tractography: Mildly reduced periventricular fractional anisotropy with reductions in the fornix and cingulum; tracts continuous. (followup request_dti_tractography)
- BNP: 186 pg/mL, raised (fallback_tool_outputs.labs[BNP])

Checks: `perfect_agent.py` pass; `test_case_guards.py -k VASC-DEM-M07` pass; criterion outputs unchanged against the pre-pass snapshot; no 60-character window of any expected_evidence in the new reports; synonym guard 0 changes.
