# VASC-DEM-S10
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No notes file exists for VASC-DEM. The condition plan's classes (C1-C19) were applied as class rulings (ROUND_POLICY ruling 2); every change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A/C | blocker | ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives | Non-schema `sequences` plus `protocol`/`contrast` (C1) | FIXED: `analyze_brain_mri {}` |
| D | major | ground_truth.action_criteria[action-6-search-medical-literature], initial_tool_outputs.literature_search, fallback_tool_outputs.literature_search | Literature criterion leaking into its own output (C2, ruling 5) | FIXED: criterion deleted, initial null, fallback deleted |
| C | minor | ground_truth.action_criteria[action-7-check-drug-interactions], fallback_tool_outputs.drug_interactions | Generic optional check; no new interacting drug (C3 group D) | FIXED: criterion and fallback deleted (initial already null) |
| D | major | patient.neurological_exam.mental_status | MoCA total and items upfront (C4) | FIXED: bedside observation; abulia kept as an exam sign |
| B | major | initial_tool_outputs.clinical_assessment | MoCA 21/30 not itemised; criteria_met carried IADL loss, onset within 3 months and "deficit disproportionate to lesion volume"; impression localised the syndrome to the genu and caudate (C4, C5) | FIXED: itemised by section (trail 0/1, clock 1/3, digits backward 0/1, serial sevens 2/3, letter fluency 0/1, recall 3/5, orientation 5/6: 9 points lost, 21/30); criteria_met keeps domain impairment and cue-responsive recall; impression lists scores, AES 56, GDS 3/15 |
| D | major | initial_tool_outputs.mri (additional_observations, findings, impression) | "accounts for the abulia and dysexecutive syndrome", "the anatomy of capsular genu syndrome", "insufficient by itself to explain a dementia", "in keeping with diabetic and hypertensive small-vessel disease" (C5) | FIXED: STRIVE-2 numbered impression; comparison with the MRI of five months ago kept (same modality); tract localisation kept as Kind 2 |
| B | minor | initial_tool_outputs.mri.findings[0].size | Volume 0.9 mL with only two dimensions (13 x 8 mm) | FIXED: 13 x 8 x 16 mm (ellipsoid about 0.9 mL) |
| D | major | initial_tool_outputs.specialized_test.impression | "characteristic of frontal-subcortical disconnection rather than of cortical degeneration" (C5) | FIXED: profile only |
| B | major | initial_tool_outputs.labs | Female Hb/Hct ranges in a man; template values; eGFR ">60"; creatinine 1.06 gives CKD-EPI 2021 eGFR 75 at 72, not 66; LDL 84 not derivable from TC 172, HDL 40, TG 164 (Friedewald 99); interpretation with targets and "excluding reversible causes" (C6) | FIXED: male ranges; Hb 14.6, Hct 43.5, WBC 8.2, Plt 226, MCV 89, Na 140, K 4.7, ALT 28, albumin 4.2, folate 10.4; creatinine 1.17 (eGFR 66); TC 157 (157 - 40 - 164/5 = 84); flag-only interpretation |
| C | minor | patient.clinical_history.past_medical_history[2] | The plan keeps echo and monitoring as waste because the lacunar stroke was worked up at the admission, but the case did not say so | FIXED: "inpatient ECG, 48-hour telemetry and carotid duplex were normal" added; waste rationales cite it |
| B/D | major | fallback_tool_outputs (advanced_imaging, labs, ct, echo, cardiac_monitoring) | "non-contributory" fallbacks; CT "already obtained"; echo "No cardioembolic source identified"; template Holter numbers (C7) | FIXED: advanced_imaging and labs deleted; CT written to his lesions; echo modality-only with `echo_type` TTE; Holter values varied; metadata.fallback_tool_kinds updated |
| C | major | ground_truth.assessment.required_recommendations | Musts restated criteria or reasoning (date the change, scales, testing, MRI, reversible causes) and "institute secondary prevention" without content (C19) | FIXED: clopidogrel single antiplatelet; BP below 130/80; continue high-intensity statin (atorvastatin 40 mg already high intensity; small-vessel stroke, so no LDL 70 target per plan 1.2); individualised HbA1c about below 8.0% (7.6% needs no intensification); activity scheduling and caregiver education |
| C | major | ground_truth.differential[Post-stroke depression] | Moderate although GDS-15 3/15, no low mood and AES 56 exclude it at assessment time (C8, ruling 7) | FIXED: low, key features restated |
| C/A | minor | ground_truth.action_criteria[*] | Rationale = label; unbracketed citations; verdicts in expected evidence (C13) | FIXED |
| C | minor | ground_truth.red_herrings[0,1].field_path | Empty field paths; "disconnects prefrontal circuits bilaterally" from a unilateral lesion | FIXED: paths to the history fields; wording "interrupts thalamo-prefrontal projections" |
| C | minor | ground_truth.action_criteria order; avoided_actions[*].rationale; stop_rule | Neuropsych last; generic rationales, CT "already obtained"; max 0 (C16, C18) | FIXED: screen, neuropsych, labs, MRI; max 1 |
| C | note | echo and monitoring waste | Kept as waste per plan section 4 (lacunar infarct worked up at admission) | no change beyond rationale |
| C | check | 3.6 check | each criterion probed on a fresh environment | all four required criteria answered by initial outputs |

## Changes, in one paragraph a physician can read before re-reviewing
The MRI criterion now matches any MRI order. The exam no longer gives the MoCA; the screen itemises 21/30 with the apathy (56) and depression (3/15) scales. The MRI, screen and neuropsychology reports describe the left capsular genu and caudate infarct, the Fazekas 2 background and the dysexecutive profile without explaining the syndrome. The history now records that the stroke was worked up at the admission (ECG, telemetry, carotid duplex), which is why echocardiography and monitoring stay as waste. Labs have male ranges, an LDL that fits the lipid panel and a creatinine that fits the eGFR. Post-stroke depression is now low. Musts: clopidogrel, BP below 130/80, continue the high-intensity statin, HbA1c individualised to about below 8.0% with no intensification at 7.6%, activity scheduling and caregiver education for the abulia.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation key `[ADA_2025_older_adults]` used in a must (plan 5.4).
- Synonyms per plan 5.1 (F06.7 in the `icd_codes` of a dementia case).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Adversarial verifier, 24 Oct 2026. No notes file for VASC-DEM. Read the final case and the diff. Checked: MoCA arithmetic (2+3+4+2+2+3+5 = 21/30); lesion volume (pi/6 x 1.3 x 0.8 x 1.6 cm = 0.87 mL); CKD-EPI 2021 eGFR for creatinine 1.17 at 72 (66); Friedewald LDL (157 - 40 - 32.8 = 84); HDL 40 flagged against ">40"; the history now records the admission work-up (ECG, telemetry, duplex), which supports keeping echo and monitoring as waste per plan section 4 and leaves no ECG criterion needed; the prior MRI in the history names only "acute lacunar infarct" and is a pre-encounter study, not the scored one; genu lesion consistent with the dysarthria, facial weakness and right-sided signs; post-stroke depression low against GDS 3/15 and AES 56; musts consistent with the prohibitions (no anticoagulation, no anticholinergic bladder agent); HbA1c must consistent with ADA older-adult targets.
Found: nothing to correct. No change.
perfect_agent.py and case_io.py check clean for this case.
