# VASC-DEM-P02
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (`plans/VASC-DEM.md`) and the worker's own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1. | FIXED: `analyze_brain_mri {}`; label in STRIVE-2 terms with the atrophy scores. |
| D | major | criterion `action-9-search-medical-literature`, literature outputs | Plan C2. | FIXED: criterion deleted, initial null, fallback deleted. |
| C | minor | criterion `action-8-check-drug-interactions`, drug outputs | Plan C3 group D: no medication decision turns on an interaction (duloxetine with a cholinesterase inhibitor is not a listed interaction to check for). | FIXED: criterion deleted, initial null, fallback deleted. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: MoCA score in the exam. | FIXED: bedside observation and "Formal cognitive screening reported separately". |
| B | major | `initial_tool_outputs.clinical_assessment` | MoCA item list did not add up and used "serial sevens 3/5" (the item scores 0-3); `criteria_met` carried interpretive items; impression argued the mechanism. | FIXED: items itemised to 21/30 (18 years, no adjustment): recall 4, clock 2, trail 1, cube 1, digits backward 1 lost; letter fluency; `criteria_met` reduced to observations; impression scores only. |
| D | major | `initial_tool_outputs.specialized_test.impression`, `.quantitative_data` | Plan C5: impression concluded the dissociation "runs against a subcortical vascular cause". | FIXED: numbered domain profile with percentiles; pattern description only. |
| D | major | `initial_tool_outputs.mri.additional_observations`, `.impression`, `.volumetrics` | Plan C5: report weighed which pathology leads. | FIXED: STRIVE-2 findings, Koedam 2-3, MTA 2, no microbleeds or siderosis; numbered impression. |
| D | major | `initial_tool_outputs.advanced_imaging` (amyloid PET) | Plan C5: read argued the leading pathology. | FIXED: binary positive read, posterior-predominant, SUVr 1.61 with threshold. |
| D | major | `followup_outputs[0]` (FDG-PET) | Plan C5: argued that the deficit is degenerative rather than vascular. | FIXED: regional findings and a pattern statement only; FDG stays recommended. |
| C | major | `ground_truth.avoided_actions[avoid-harm-8-analyze-csf]` (new), `followup_outputs[1]` (new) | Plan C9: he refuses lumbar puncture after a difficult lumbar fusion, yet a CSF order was unanswered and unpenalised. | FIXED: avoided action, severity harm; a concordant CSF report (low Abeta42/40, raised p-tau181) is authored so the order returns data consistent with the positive PET. Probed. |
| B | major | `initial_tool_outputs.labs` | Plan C6: template values; Hb/Hct ranges female; eGFR 76 for creatinine 0.9 in a man of 70 (CKD-EPI 2021 gives 92); total cholesterol 164 vs Friedewald 158. | FIXED: male ranges, Hct 42.5; WBC 5.6, Plt 203, MCV 92, Na 142, K 4.4, ALT 28, albumin 4.4, folate 10.3; eGFR 92 with ">=60"; total cholesterol 158; interpretation lists results only. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated tool steps; no treatment for either component; driving left to the wife's report. | FIXED: five musts: mixed dementia with posterior-predominant AD syndrome leading [VASCOG_2014]; cholinesterase inhibitor [NICE_NG97]; BP below 130/80 from 144/84 with orthostatic checks, continue rosuvastatin and CPAP [ESO_2021_SVD]; formal driving assessment; OT, carer support, advance care planning [NICE_NG97]. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | No prohibition against an antiplatelet for covert small-vessel disease. | FIXED: added [ESO_2021_SVD]; driving and LP prohibitions reworded. |
| C | major | `ground_truth.differential` | Plan C8: "Vascular dementia alone" and PCA entry not low after a positive PET. | FIXED: both low; PCA entry renamed "Posterior cortical atrophy (Alzheimer disease) without significant vascular contribution". |
| B | minor | `ground_truth.red_herrings` (OSA) | Empty field path. | FIXED: `patient.clinical_history.past_medical_history[1]`. |
| C | minor | `ground_truth.avoided_actions` | Plan C18. | FIXED: case-specific rationales; canonical CT text. |
| B | minor | `fallback_tool_outputs.ct`, `.echo`, `.cardiac_monitoring`, `.advanced_imaging`, `.labs` | Plan C7. | FIXED: CT describes his CT appearance with the CT limitation; echo and Holter list findings; advanced-imaging and labs fallbacks deleted; `metadata.fallback_tool_kinds` trimmed. |
| A | minor | all criteria | Plan C13. | FIXED: case-specific rationales, bracketed keys only. |
| B | minor | `ground_truth.action_criteria` order, `.stop_rule` | Plan C16. | FIXED: screen, neuropsych, labs, MRI, amyloid PET, FDG; soft screen-before-MRI kept; `max_additional_actions` 1. |
| E | minor | `patient.history_present_illness` | Em dash in the HPI. | FIXED: colon. |
| C | minor | `ground_truth.key_clinical_evidence[1]` | Phrased as a teaching statement about the reading error. | FIXED: imaging severity and clinical relevance stated as separate questions. |

## Changes, in one paragraph a physician can read before re-reviewing

A 70-year-old retired architect with three years of visuospatial-led decline and storage-type amnesia, referred for Fazekas 3 white matter change with two lacunes; no clinical stroke. The exam no longer gives the MoCA; the screen's items now add up to 21/30. Reports state only their findings: MRI with Koedam 2-3 posterior atrophy and MTA 2, a binary positive amyloid PET (posterior-predominant) and an FDG-PET with posterior hypometabolism. He refuses lumbar puncture, so a CSF order is now an avoided harmful action (answered by a concordant report if made). Labs carry male ranges and eGFR 92 matching creatinine 0.9. Musts: name mixed dementia with the Alzheimer syndrome leading, offer a cholinesterase inhibitor, lower BP below 130/80 and continue rosuvastatin and CPAP, arrange a formal driving assessment, and provide OT, carer support and advance care planning; no antiplatelet for covert small-vessel disease. Vascular dementia alone and PCA without vascular contribution are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation key used: `[NICE_NG97]` (plan 5.4).
- Synonyms (plan 5.1): mixed case; add a mixed-dementia entry and stop crediting bare "vascular dementia" and F06.7 here.

## Open questions for Andrea (judgment calls you could not settle)

- None. Decision recorded: the CSF avoided action is severity harm (procedure in a patient who refuses it) rather than waste; the external capsule involvement on MRI was left without a CADASIL mention (age 70, negative family history, 18 years of hypertension).

## Verification

Adversarial check (24 Oct 2026). No reviewer notes. Checked: MoCA items sum to 21/30 (no adjustment at 18 years) and match the exam (fully oriented); eGFR 92 matches creatinine 0.9 at 70; Hct 42.5 with Hb 14.1; Friedewald 158; all labs unflagged and the interpretation says so; avoided CSF harm agrees with the HPI refusal and the authored CSF follow-up is concordant with the PET (glucose ratio 61/94 = 0.65); FDG follow-up is descriptive; MRI gives Koedam and MTA scores and no microbleeds; differential (vascular alone and PCA without vascular contribution both low) matches the evidence; no antiplatelet for covert SVD (no clinical stroke); the prior headache MRI in the HPI is kept without a grade, as the plan rules.

Found and fixed: the amyloid PET named 18F-flutemetamol with a positivity threshold of SUVr 1.11, which is the florbetapir cut-off (flutemetamol cut-offs with a cerebellar reference are about 1.5-1.6, so 1.61 would be borderline). Changed `initial_tool_outputs.advanced_imaging.tracer_or_protocol` to "18F-florbetapir PET, cortical-to-whole-cerebellum SUVr"; values, read and expected evidence unchanged.

Checks re-run after my edits: `perfect_agent.py -v` passes (every required and recommended criterion answered by case data); `case_io.py check` clean for this case (schema, synonym guard, no test failure naming it). Note for the lead, not changed: `metadata.fallback_tool_kinds` still labels case-specific fallbacks (CT with this patient's lesions, AF Holter where present) as "normal"; the field is read by no code or test, so I left it rather than churn it.
