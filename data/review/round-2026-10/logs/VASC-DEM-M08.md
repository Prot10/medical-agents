# VASC-DEM-M08
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (`plans/VASC-DEM.md`) and the worker's own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key plus `protocol`/`contrast` made the required MRI criterion unmatchable. | FIXED: `analyze_brain_mri {}`. |
| D | major | criterion `action-8-search-medical-literature`, `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search` | Plan C2 / ruling 5: literature step whose output repeated its own expected evidence. | FIXED: criterion deleted, initial null, fallback deleted. |
| C | major | `patient.physical_exam`, `patient.demographics.bmi` | Plan C3: edoxaban 60 mg at age 81 with creatinine 1.28 mg/dL cannot be checked without a weight. | FIXED: `physical_exam.general` "Weight 71 kg, height 172 cm." (BMI 24.1 to 24.0). Cockcroft-Gault (140-81) x 71 / (72 x 1.28) = 45.5 mL/min: within the 15-50 band, so the label dose is 30 mg once daily. |
| C | major | criterion `action-9-check-drug-interactions`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group R: generic optional check and false "no prohibitive interaction" fallback, while the plan offers a cholinesterase inhibitor to a man on diltiazem and his edoxaban dose is wrong for his clearance. | FIXED: recommended; alternatives donepezil, rivastigmine, galantamine (plan) plus edoxaban (my addition: the edoxaban check is the one that reveals the renal dosing rule, an equally correct act here); four case-specific outputs (AChEI with diltiazem: bradycardia/AV block and CYP3A4 rise for donepezil and galantamine; edoxaban with diltiazem: no dose change, dose set by Cockcroft-Gault clearance and weight); generic fallback deleted. Leak guard passes. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: exam gave the MoCA and its items. | FIXED: bedside observation and "Formal cognitive screening reported separately". |
| B | major | `initial_tool_outputs.clinical_assessment` | MoCA item losses as listed did not sum to 18/30 (clock 1/3, month only, naming "reduced" plus the rest gives 16-17); "fluency 7 animals" is not the MoCA item; `criteria_met` carried interpretive and severity items; impression named Alzheimer pathology. | FIXED: losses itemised to 18/30 (recall 4, orientation 2 for month and date, trail 1, cube 1, clock 1, digits backward 1, serial sevens 1, letter fluency 1; naming 3/3 with word-finding pauses); `criteria_met` keeps only `impairment_in_at_least_one_domain` and `recall_improves_with_cueing` (false); impression lists scores only; FAQ 21/30 kept. |
| D | major | `initial_tool_outputs.specialized_test.impression` | Plan C5: "amnestic core is degenerative; executive slowing compatible with the vascular burden". | FIXED: numbered profile without disease attribution. |
| D | major | `initial_tool_outputs.mri.additional_observations`, `.impression`, `.volumetrics` | Plan C5: "hypertensive rather than amyloid angiopathy, which matters for the anticoagulation decision", "Alzheimer-type atrophy", "no embolic infarct despite atrial fibrillation", "beyond the age-adjusted range". | FIXED: STRIVE-2 descriptors and numbered impression; microbleed finding order unchanged. |
| D | major | `initial_tool_outputs.advanced_imaging` (amyloid PET) | Plan C5 and style guide (amyloid PET strictly binary): "Typical Alzheimer distribution ... the diagnosis is mixed Alzheimer and vascular dementia". | FIXED: "Positive amyloid PET: moderate-to-frequent cortical amyloid neuritic plaque density (composite SUVr 1.48; positivity threshold 1.11)"; finding labels descriptive. |
| D | major | `followup_outputs[0]` (FDG PET) | Plan C5: "Alzheimer pattern", "Vascular contribution", `pattern: mixed Alzheimer and vascular`. | FIXED: descriptive findings, impression in style-guide wording, `quantitative_data` null. |
| C | major | `ground_truth.avoided_actions` (new `avoid-harm-8-analyze-csf`), `followup_outputs[1]` (new) | Plan C9: LP declined and he is on edoxaban; nothing stopped an agent ordering CSF, and the library would have returned a normal CSF contradicting the positive PET. | FIXED: avoided `analyze_csf {}` severity harm with the plan's rationale; authored CSF follow-up concordant with the PET (Abeta42/40 0.047, p-tau181 81 pg/mL). Probed: any CSF order returns it. |
| B | major | `initial_tool_outputs.labs` | Plan C6: female Hb and Hct ranges in a man; template values; Hct 41.6 vs Hb 12.7; eGFR 52 does not match creatinine 1.28 at 81 (CKD-EPI 2021 gives 56); eGFR range ">60"; total cholesterol 190 vs Friedewald 179; interpretation "LDL above target", "relevant to anticoagulant dosing", "no reversible cause". | FIXED: male ranges (Hb 13.5-17.5, Hct 41-53) with Hb 13.8 and Hct 41.2 (so no new anaemia is introduced); WBC 6.3, Plt 214, MCV 90, Na 140, K 4.7, ALT 19, albumin 4.0, folate 8.9; eGFR 56 with ">=60"; total cholesterol 179; interpretation a recital of flagged values. |
| B | major | `initial_tool_outputs.ecg` (new), criterion `action-10-analyze-ecg` (new, optional) | No ECG output: an ECG (reasonable before a cholinesterase inhibitor on diltiazem) would have returned the library's sinus rhythm, contradicting six years of AF and an irregularly irregular pulse. | FIXED: authored AF ECG, rate 78, voltage LVH (consistent with the echo's concentric hypertrophy), normal QTc; optional criterion. |
| B | major | `fallback_tool_outputs.cardiac_monitoring`, `.echo` | Holter fallback "sinus rhythm, no AF"; echo LA "normal size" after six years of AF and verdict "No cardioembolic source". | FIXED: Holter AF throughout, controlled rate; echo LA moderately dilated, impression lists findings. |
| D | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, `.labs` | Plan C7. | FIXED: CT fallback describes this patient's CT appearance with the CT limitation; advanced-imaging and labs fallbacks deleted; `metadata.fallback_tool_kinds` trimmed. |
| A | minor | all criteria | Plan C13: rationale equal to label, duplicate unbracketed keys, em dashes. | FIXED: case rationales, bracketed keys, expected evidence with values. |
| B | minor | `ground_truth.action_criteria` order | Plan C16. | FIXED: screen, neuropsych, labs, MRI, ECG, amyloid PET, FDG, drug check. |
| C | major | `ground_truth.assessment.required_recommendations` | Plan C19: musts restated tool steps; no edoxaban dose, BP, cholinesterase-inhibitor or carer must. | FIXED: seven musts: mixed dementia named; family's AF question answered with the MRI; edoxaban reduced to 30 mg once daily (CrCl about 46 mL/min) and continued, CHA2DS2-VA 3 [ESC_AF_2024]; donepezil with heart rate and ECG checks because of diltiazem [NICE_NG97]; BP gradually below 130/80 from 152/78 with orthostatic checks (tamsulosin) [ESO_2021_SVD]; leg findings attributed to lumbar stenosis; carer support and 6-12 month review [NICE_NG97]. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | No prohibition against leaving edoxaban at 60 mg. | FIXED: added; others reworded, LP prohibition now says he declined it. |
| C | major | `ground_truth.differential` | Plan C8: "Alzheimer's disease alone" moderate after positive PET plus vascular burden; "Cervical or lumbar myelopathy" mislabels lumbar stenosis (no cord at that level). | FIXED: AD alone low; entry renamed "Lumbar canal stenosis with radiculopathy contributing to the gait" (M48.062 kept); em dash removed from the cardioembolic entry. |
| B | minor | `ground_truth.red_herrings` | Empty field paths, locations "history"/"examination". | FIXED: `patient.clinical_history.past_medical_history[1]` and `patient.neurological_exam.reflexes`. |
| C | minor | `ground_truth.avoided_actions` | Plan C18: generic rationales. | FIXED: case-specific rationales. |
| B | minor | `ground_truth.stop_rule` | `max_additional_actions` 0. | FIXED: 1. |
| B | minor | `ground_truth.key_clinical_evidence`, `metadata.key_educational_points` | No mention of the dosing point. | FIXED: added the Cockcroft-Gault edoxaban point. |

## Changes, in one paragraph a physician can read before re-reviewing

An 81-year-old man with three years of amnestic decline, six years of anticoagulated AF and a family asking whether AF causes "small strokes". The exam no longer gives the MoCA; the screen adds up to 18/30, and no report names the diagnosis (screen, neuropsychology, MRI, amyloid and FDG PET report their own findings only). He declined LP and takes edoxaban: CSF is now an avoided harmful action, with an authored concordant CSF report in case it is ordered anyway. A weight (71 kg) was added: his Cockcroft-Gault clearance is about 46 mL/min, so edoxaban 60 mg is too high and the must is to reduce it to 30 mg and continue anticoagulation. The drug check is recommended and case-specific (AChEI with diltiazem: bradycardia; edoxaban dosing). An optional ECG with AF was authored and the Holter fallback no longer says sinus rhythm. Labs carry male ranges, eGFR 56 matching the creatinine and non-template values. Musts now cover mixed dementia, the AF answer, edoxaban dose, donepezil with ECG checks, BP below 130/80, the lumbar stenosis and carer support. "Alzheimer disease alone" is low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[NICE_NG97]`, `[ESC_AF_2024]` (plan 5.4).
- Synonyms (plan 5.1): mixed case; add a mixed-dementia entry and stop crediting bare "vascular dementia" and F06.7 here.

## Open questions for Andrea (judgment calls you could not settle)

- None. Decisions recorded: (1) edoxaban 30 mg follows from the weight I chose (71 kg, consistent with BMI 24); this makes the plan's dosing check a real management change rather than a confirmation. (2) `edoxaban` added as a fourth drug-check alternative beyond the plan's three cholinesterase inhibitors, since that query is what surfaces the dosing rule. (3) Optional ECG added (not in the plan) to stop the library's sinus-rhythm ECG contradicting the case.

## Verification

Adversarial check (24 Oct 2026). No reviewer notes. Checked: MoCA items sum to 18/30 and match the exam (month and date wrong, 4/6); Cockcroft-Gault (140-81) x 71 / (72 x 1.28) = 45.5 mL/min, so edoxaban 30 mg is the label dose and the must, the prohibition, the drug-check output and the key evidence agree; diltiazem needs no edoxaban reduction (not a strong P-gp inhibitor); eGFR 56 matches creatinine 1.28 at 81 (CKD-EPI 2021); Hct 41.2 with Hb 13.8; Friedewald 179; BMI 71/1.72^2 = 24.0; CHA2DS2-VA 3; avoided CSF harm agrees with the HPI (LP declined) and the authored CSF follow-up is concordant with the PET (glucose ratio 61/98 = 0.62); ECG LVH agrees with the echo fallback; AF fallbacks agree with the ECG; no report names the diagnosis; differential matches the evidence.

Found and fixed: the amyloid PET named 18F-florbetaben with a positivity threshold of SUVr 1.11, which is the florbetapir cut-off (florbetaben SUVr cut-offs are about 1.4-1.5, so 1.48 would be borderline), and its "moderate-to-frequent neuritic plaque density" wording is the florbetapir read language. Changed `initial_tool_outputs.advanced_imaging.tracer_or_protocol` to "18F-florbetapir PET, cortical-to-whole-cerebellum SUVr"; values, read and expected evidence unchanged.

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
