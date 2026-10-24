# VASC-DEM-P07
Reviewer status: R1 none, R2 none (VASC-DEM has no notes file; never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (classes C1-C19) and from my own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-5-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key. | FIXED: `analyze_brain_mri {}`; label, rationale, evidence rewritten. |
| D | major | `action-7-search-medical-literature`, literature outputs | Plan C2 leak. | FIXED: criterion deleted, initial null, fallback deleted. |
| B | minor | `action-8-check-drug-interactions`, drug fallback | Plan C3 group D. | FIXED: criterion and fallback deleted; initial null. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: the MoCA total and item losses in the exam. The GP's MoCA 26/30 in the HPI is the red herring and stays (plan C4). | FIXED: bedside observation (oriented, fluent, cannot describe a routine filing, minimises), "Formal cognitive screening reported separately". |
| D | major | `initial_tool_outputs.clinical_assessment` | Plan C5: impression "a substantial fall that the instrument cannot register ... The functional evidence, not the screen, establishes the diagnosis"; score strings "within the normal range", "the patient minimises"; "16 animals" for the MoCA letter-fluency item. MoCA arithmetic checked: 4 points lost = 26/30, no education correction. | FIXED: results-only impression; score strings neutral; fluency "16 words beginning with F". |
| D | major | `followup_outputs[0]` (gait) | "The dual-task cost is the same executive failure the screen missed, expressed in gait" (cross-modality); "markedly abnormal" judgments in findings. | FIXED: measured values only (TUG 13.9 s with the 13.5 s cut-off, SPPB 10/12, 0.85 m/s, dual-task cost 34%, gait description). |
| D | major | `initial_tool_outputs.specialized_test.impression` | "resolves what the screen concealed ... a brief screening instrument cannot detect". | FIXED: profile with the executive scores, the premorbid discrepancy and preserved naming and recognition. |
| D | major | `initial_tool_outputs.mri` | Plan C5: observations gave the "anatomical explanation for a severe dysexecutive syndrome", labelled the microbleeds "hypertensive arteriopathy" and the MTL "against a degenerative amnestic process"; impression said the distribution "explains why a brief screen was insensitive". | FIXED: STRIVE-2 numbered impression; descriptive observations; volumetrics "Marked". |
| B | major | `initial_tool_outputs.labs` | Plan C6: female Hb/Hct ranges in a man; Hct 41.6 with Hb 14.2; eGFR ">60"; template values; interpretation "above target ... excluding reversible causes". | FIXED: male ranges, Hct 42.6; eGFR ">=60"; WBC 7.6, Plt 219, MCV 89, Na 137, K 4.6, ALT 26, albumin 4.3, folate 8.7; interpretation lists flagged values only. |
| C | major | `action-3-interpret-labs.expected_evidence` | "HbA1c 7.9% ... above target": for a patient with dementia an individualised target of about below 8.0% applies (plan 1.2), so 7.9% is not above target. | FIXED: evidence states the values without a target judgment; HbA1c must keeps the target and avoids hypoglycaemic agents. |
| B | minor | `ground_truth.action_criteria` | Plan C13; order per C16 (screen, gait, neuropsych, labs, MRI). Gait stays required (C14). | FIXED: case rationales and evidence; gait label now names the dual-task condition. |
| B | minor | `ground_truth.stop_rule.max_additional_actions` | 0. | FIXED: 1; required set unchanged; soft screen-before-MRI kept. |
| B | major | `fallback_tool_outputs` | Plan C7 giveaways. | FIXED: advanced_imaging and labs deleted; CT rewritten for this patient; echo impression descriptive; `metadata.fallback_tool_kinds` updated. |
| C | minor | `ground_truth.avoided_actions[*].rationale` | Plan C18. | FIXED: case-specific. |
| C | major | `ground_truth.assessment.required_recommendations` | Five of seven musts were process or tool steps (obtain MRI, measure gait, use ecological tests); no secondary-prevention musts although he had a lacunar stroke with BP 148/88 and LDL 108 on atorvastatin 40; no concrete driving or professional action. | FIXED: six musts: diagnosis despite MoCA 26 [VASCOG_2014]; stop driving pending formal assessment and licensing duty; stop independent practice, partner or occupational health with consent, lasting power of attorney; BP below 130/80 gradually [AHA_ASA_2021_secondary]; atorvastatin 80 mg and continue clopidogrel [AHA_ASA_2021_secondary]; HbA1c individualised, reduce alcohol [ADA_2025_older_adults]. Plan C19's covert-SVD prohibition does not apply: he had a clinical lacunar stroke, so single antiplatelet therapy is indicated. |
| C | minor | `ground_truth.assessment.prohibited_recommendations[4]` | "Do not attribute the errors to workload without formal testing" duplicated item 2. | FIXED: replaced by "Do not add aspirin to clopidogrel" (no DAPT indication four years after a lacunar stroke). |
| C | major | `ground_truth.differential[0]` | Plan C8: mild VCI `moderate` after the functional and formal evidence. | FIXED: `low`, key features updated. |
| B | minor | `ground_truth.red_herrings[*]` | The MoCA red herring pointed at the screen scores although its data point is the GP's documented reassurance; second path empty. | FIXED: both point to `patient.history_present_illness`. |
| E | minor | `followup_outputs[0]`, `key_clinical_evidence[1]`, `accepted[0]`, finding strings | Remaining em dashes in untouched strings. | FLAGGED (plan rule; label not editable). |
| C | minor | `initial_tool_outputs.labs` B12 322 pg/mL | Ten years of metformin with reduced toe vibration; B12 322 is above the 200-300 grey zone where MMA is advised. | FLAGGED: no change; value is normal and diabetic neuropathy explains the vibration loss. |
| - | check | plan 3.6 | perfect_agent.py ok; `test_case_guards -k VASC-DEM-P07` 2 passed; `case_io.py check` no failure names P07; `sequences` 0. | - |

## Changes, in one paragraph a physician can read before re-reviewing

Same case: a 63-year-old tax consultant reassured by a GP MoCA of 26/30 who has lost his work and household function (FAQ 23/30), with severe executive failure on ecologically valid tests against a premorbid IQ of 128, a dual-task gait decrement, and Fazekas 3 frontal-predominant small-vessel disease with five lacunes after a lacunar stroke four years ago. The GP's MoCA stays in the history as the red herring; the exam no longer repeats it. All reports describe only their own measurements (no "the screen missed it", no "the lesions explain the syndrome"). Labs use male ranges and only list flagged values. "Mild VCI" is now low in the differential. Musts are now concrete: the dementia diagnosis despite the normal screen, stop driving pending assessment, stop independent practice with legal and financial planning, BP below 130/80, atorvastatin 80 mg with clopidogrel continued, individualised HbA1c and less alcohol; a new prohibition forbids adding aspirin to clopidogrel.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation key used: `[ADA_2025_older_adults]` (plan 5.4).
- Synonyms (plan 5.1): `F06.7` should not be credited for this dementia-severity case, the one most exposed to a "mild VCI" answer.

## Open questions for Andrea (judgment calls you could not settle)

- None. Plan C19 lists P07 among covert-SVD cases for the no-antiplatelet prohibition "if no clinical stroke"; P07 has a documented lacunar stroke, so the prohibition was not added and clopidogrel continues.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff and the final patient, ground truth, reports and follow-ups. Verified: the GP MoCA 26/30 red herring stays in the HPI as plan C4 directs; MoCA arithmetic (trail-making, cube, 2 recall points = 26/30; letter fluency 16 words passes) and exam (fully oriented) agree; gait required (C14) with a measured-values report consistent with the exam; the worker's decision not to add the covert-SVD antiplatelet prohibition is correct (documented lacunar stroke four years ago, clopidogrel indicated), and the new "no aspirin added to clopidogrel" prohibition is consistent with the musts; atorvastatin 80 mg for LDL 108 on 40 mg is consistent with AHA 2021 high-intensity statin after small-vessel stroke; HbA1c 7.9% not called above target; differential alternatives low with result-based features.
Found and changed: eGFR 74 did not match creatinine 1.04 mg/dL in a 63-year-old man (CKD-EPI 2021 about 81); set `initial_tool_outputs.labs.panels.CMP[eGFR].value` to 81 (not flagged). perfect_agent.py pass; case_io.py check: schema OK, no failure names P07; test_case_guards pass.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Triglycerides]`, `.abnormal_values_summary`, `.interpretation`, `action-3-interpret-labs.expected_evidence` | Total cholesterol 202 did not equal LDL 108 + HDL 41 + TG 186/5 (186.2); TC 202 is flagged and quoted, so TG was the value to move. | FIXED: triglycerides 265 mg/dL everywhere it appears (still flagged high). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, occupational_function_lost, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall and `screening_instrument_in_normal_range` (a fact about the MoCA 26/30, the case's red herring). The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here subcortical small-vessel labels and F01.2/I67.3. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `[ADA_2025_older_adults]` -> `[ADA_older_adults_2026]` in the HbA1c must (same target below about 8.0%; superseded edition, as in ALZ-EARLY).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.
