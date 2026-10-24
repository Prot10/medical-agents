# VASC-DEM-P01
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (`plans/VASC-DEM.md`) and the worker's own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1. | FIXED: `analyze_brain_mri {}`. |
| D | major | criterion `action-7-search-medical-literature`, literature outputs | Plan C2. | FIXED: criterion deleted, initial null, fallback deleted. |
| C | minor | criterion `action-8-check-drug-interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group D. | FIXED: criterion deleted, initial null, fallback deleted. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: full MoCA items in the exam. | FIXED: bedside observation and "Formal cognitive screening reported separately". |
| B | major | `initial_tool_outputs.clinical_assessment`, exam | MoCA arithmetic: the listed item losses (clock 1/3, naming 2/3, serial sevens 1/3, abstraction 0/2, recall 0/5, month and date, plus trail, cube, digits, fluency) sum to 12/30, not 16/30; `criteria_met` carried interpretive items; impression argued "neither pathology alone produces both halves". | FIXED: items set so the losses sum to 16/30 (clock 2/3, naming 3/3 with long latencies, serial sevens 2/3, abstraction 1/2); `criteria_met` keeps impairment and cueing (false); impression lists scores only. |
| D | major | `initial_tool_outputs.specialized_test.impression`, `.quantitative_data` | Plan C5: "storage failure ... subcortical failure ... attributing to either pathology alone would require...". | FIXED: numbered domain profile ("storage-type pattern" kept as a neuropsychological description); the arguing `note` removed. |
| D | major | `initial_tool_outputs.mri.additional_observations`, `.impression`, `.volumetrics` | Plan C5: "both pathologies at full strength", "each sufficient for its own diagnosis", "hypertensive, not amyloid". | FIXED: STRIVE-2 findings with a numbered impression. Added the NPH-relevant measurements the case's differential relies on: no DESH, high-convexity sulci not effaced, callosal angle 112 degrees (Evans 0.31 already reported). |
| D | major | `initial_tool_outputs.csf.interpretation` | Plan C5: "this is mixed Alzheimer and vascular dementia with both components severe". | FIXED: values and pattern only. |
| B | minor | `initial_tool_outputs.csf.glucose_ratio` | 0.58 with CSF glucose 82 and serum glucose 172 (= 0.48). | FIXED: "0.48 (serum glucose 172 mg/dL)". |
| C | major | criterion `action-6-analyze-csf`, `followup_outputs[1]` (new) | Plan C9: CSF-only biomarker route. | FIXED: id kept, required, alternatives CSF special_tests and `order_advanced_imaging {"modality": "amyloid_PET"}`; authored amyloid PET (florbetaben, positive, Centiloid 96) concordant with the strongly positive CSF. Probed. |
| C | major | criterion `action-9-perform-clinical-assessment-gait` (new), `followup_outputs[0]` (new) | Plan C14: gait involvement with falls and urgency but no gait criterion. | FIXED: recommended `gait_and_balance_timed` with an authored report (TUG 19.6 s, 0.61 m/s, short steps, wide base, preserved arm swing, 5-step turn, retropulsion with recovery), no diagnostic argument. |
| B | major | `initial_tool_outputs.labs` | Plan C6: template values; Hct 41.6 vs Hb 12.6; eGFR 56 vs creatinine 1.1 in a woman of 74 (CKD-EPI 2021 gives 53); range ">60"; HDL range ">40" for a woman; total cholesterol 182 vs Friedewald 177; interpretation "above the post-stroke target", "worth correcting on metformin", "no reversible cause accounts for the syndrome". | FIXED: Hct 37.8; WBC 6.1, Plt 287, MCV 84, Na 140, K 4.0, ALT 15, albumin 4.0, folate 13.4; eGFR 53 with ">=60"; HDL ">50"; total cholesterol 177; interpretation lists flagged values and the B12 value without advice. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated tool steps (test recognition, read the MRI, obtain biomarkers, exclude reversible causes); no specific treatment for either component; low-normal B12 on 16 years of metformin left without an action (PATTERNS: comorbid contributors dismissed). | FIXED: eight musts: mixed dementia named; donepezil with urgency/bradycardia/falls watch [NICE_NG97]; continue clopidogrel as single antiplatelet [AHA_ASA_2021_secondary]; BP gradually below 130/80 from 156/84 with orthostatic checks [AHA_ASA_2021_secondary]; atorvastatin 80 mg (high intensity, LDL 96 on 40 mg) [AHA_ASA_2021_secondary]; individualised glycaemic target about below 8.0% [ADA_2025_older_adults]; replace B12 or confirm with MMA; falls, urgency, carer support, prognosis and advance care planning [NICE_NG97]. |
| C | major | `ground_truth.differential` | Plan C8: both "alone" entries moderate after the biomarker and MRI. | FIXED: both low; NPH key features now cite the callosal angle and absent DESH; B12 entry says replace or confirm with MMA. |
| C | minor | `ground_truth.avoided_actions` | Plan C18. | FIXED: case-specific rationales (echo and monitoring: lacunar infarcts, no embolic pattern). |
| B | minor | `ground_truth.red_herrings[1]` | Empty field path, location "history". | FIXED: `patient.clinical_history.past_medical_history[3]`. |
| C | minor | `ground_truth.key_clinical_evidence[2]` | "small-vessel disease impairs retrieval, not storage" is too absolute. | FIXED: "impairs retrieval more than storage". |
| B | minor | `fallback_tool_outputs.ct`, `.echo`, `.cardiac_monitoring`, `.advanced_imaging`, `.labs` | Plan C7. | FIXED: CT describes her CT appearance; echo and Holter impressions list findings only; advanced-imaging and labs fallbacks deleted; `metadata.fallback_tool_kinds` trimmed. |
| A | minor | all criteria | Plan C13. | FIXED. |
| B | minor | `ground_truth.action_criteria` order, `.sequence_constraints`, `.stop_rule` | Plan C16. | FIXED: screen, gait, neuropsych, labs, MRI, biomarker; soft MRI before the biomarker criterion; `max_additional_actions` 1. |

## Changes, in one paragraph a physician can read before re-reviewing

A 74-year-old woman with five years of steady decline combining dense storage-type amnesia and severe slowing, gait disorder with falls and urgency, two lacunar strokes and severe small-vessel disease with MTA grade 3. The exam no longer gives the MoCA, and the screen's items now add up to 16/30 (they summed to 12). Reports state only their own findings; the MRI adds the callosal angle (112 degrees) and absence of DESH so the agent can weigh NPH. The biomarker step accepts CSF or a new positive amyloid PET. A recommended timed gait assessment was added with an authored report. Labs carry eGFR 53 matching the creatinine and non-template values. Musts now name mixed dementia, offer donepezil, continue clopidogrel, lower BP below 130/80 gradually, raise atorvastatin to 80 mg, individualise the glycaemic target, replace the low-normal B12 (or check MMA) and address falls, urgency, carer support and prognosis. Both single-pathology alternatives are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[NICE_NG97]`, `[ADA_2025_older_adults]` (plan 5.4).
- Synonyms (plan 5.1): mixed case; add a mixed-dementia entry and stop crediting bare "vascular dementia" and F06.7 here.

## Open questions for Andrea (judgment calls you could not settle)

- None. Decision recorded: I did not add a methylmalonic acid criterion (plan C21 keeps the lab panel fixed); the low-normal B12 is handled by a must to replace it or confirm with MMA.

## Verification

Adversarial check (24 Oct 2026). No reviewer notes. Checked: MoCA items sum to 16/30 and match the exam (month and date wrong); eGFR 53 matches creatinine 1.1 in a woman of 74 (CKD-EPI 2021), and metformin 2 g/day and sitagliptin 100 mg remain appropriate at that eGFR; Hct 37.8 with Hb 12.6; Friedewald 177; HDL 40 flagged against the female range; B12 268 unflagged in the panel and handled by a must; CSF glucose ratio 82/172 = 0.48; gait follow-up arithmetic (10 m in 16.4 s = 0.61 m/s) and content agree with the exam; MRI adds callosal angle and DESH, matching the NPH entry; both biomarker alternatives answered; sinus Holter and normal-LA echo fallbacks fit a patient without AF; musts (clopidogrel continued, high-intensity statin after lacunar stroke, BP below 130/80) follow plan 1.2.

Found and fixed: the new amyloid-PET follow-up gave Centiloid 96 with a florbetaben composite SUVR of 1.79, which by the florbetaben Centiloid transformation (CL = 153.4 x SUVR - 154.9, whole-cerebellum reference) corresponds to about 120. Changed `followup_outputs[1].output.quantitative_data` to "Composite cortical SUVR (whole-cerebellum reference)": "1.64" (Centiloid 96 unchanged).

Checks re-run after my edits: `perfect_agent.py -v` passes (every required and recommended criterion answered by case data); `case_io.py check` clean for this case (schema, synonym guard, no test failure naming it). Note for the lead, not changed: `metadata.fallback_tool_kinds` still labels case-specific fallbacks (CT with this patient's lesions, AF Holter where present) as "normal"; the field is read by no code or test, so I left it rather than churn it.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here mixed-dementia labels and F00.2 only; generic F01 entry excluded. A vascular-only answer ("vascular dementia", "VaD") no longer scores; accepted: "mixed dementia", "alzheimer vascular dementia" (both spellings), "alzheimer cerebrovascular disease" (both spellings). Code-alone limitation: an answer coded F01.50 still matches (CENTRAL).
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `[ADA_2025_older_adults]` -> `[ADA_older_adults_2026]` in the HbA1c must (same target below about 8.0%; superseded edition, as in ALZ-EARLY).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
