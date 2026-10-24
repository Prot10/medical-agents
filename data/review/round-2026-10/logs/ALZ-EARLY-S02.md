# ALZ-EARLY-S02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The case has no reviewer notes. The condition-plan classes C1 to C16 were applied as a class (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | initial_tool_outputs.clinical_assessment.criteria_met.delayed_recall_improves_with_cueing | True, while the exam and the assessment's own finding record recall 0/3 "no improvement with cues" (plan survey, C3). | FIXED: false. |
| D | major | initial_tool_outputs.clinical_assessment.impression, .findings, .scores | Template impression ("partial benefit from cueing recorded", engineering sentence "This assessment is the step..."); a fragment row "Alert and oriented to person and place;"; the driving incident missing from the IADL rows. | FIXED: impression rewritten from the case (MMSE 21/30 and its domains, no cue benefit, wife and daughter's report, finances taken over, driving supervised); rows rebuilt; stage text names the lost activities. Staging per plan 1.2: finances taken over by his wife, so mild dementia; onset at about 72, G30.1 correct; label unchanged. |
| B | major | initial_tool_outputs.labs.panels.BMP (sodium, chloride) | Sodium 154 mEq/L with chloride 93 and CO2 28 gives an anion gap of 33 with no explanation, and a sodium of 154 is an urgent finding no part of the case addresses (impossible template value). | FIXED: sodium 140, chloride 102 (normal); abnormal_values_summary and interpretation updated (BUN 23, glucose 107, HbA1c 6.9% remain abnormal). |
| B | minor | initial_tool_outputs.labs.panels | CMP ordered, BMP returned. | FIXED: panel renamed CMP with total protein 7.2, albumin 4.0, AST 24, ALT 21, ALP 92, bilirubin 0.7 (normal). |
| B | minor | initial_tool_outputs.labs.panels.CBC | Hematocrit 40.1 with RBC 4.95 gives MCV 81, not 87.8. | FIXED: hematocrit 43.5, MCV 87.9. |
| B | minor | initial_tool_outputs.labs.panels.Reviewed_cognitive_panel_additions | Template values shared with 25 cases. | FIXED: magnesium 1.8, homocysteine 12.6, ESR 15, CRP 2.6 (normal). |
| C | minor | (C7.2 check) | B12 310 pg/mL on 12 years of metformin: just above the plan's low-normal band and homocysteine is normal, so no MMA criterion was added (a functional deficiency would raise homocysteine). The generic "low-normal B12 should prompt MMA" key evidence item was removed (C10). | No MMA criterion; stated in the differential. |
| D | minor | initial_tool_outputs.mri.additional_observations, .findings, .impression | "No abnormal meningeal enhancement" with contrast false; "Patent major intracranial vessels on MRA" (not acquired, template); the lacunes appeared only as an additional observation. | FIXED: both lines removed; lacunes added as a finding row; impression as a numbered list naming moderate small vessel disease (Fazekas 2, lacunes) and no microbleeds. |
| B | major | ground_truth.differential[Vascular cognitive impairment] | Key features said "No significant cerebrovascular burden on MRI", contradicting Fazekas 2 and bilateral basal ganglia lacunes. | FIXED: VCI as a contributor, likelihood moderate (as plan C11 for M05), with the features that keep AD primary (gradual course, no stroke, memory-led, MTA 3). |
| C | major | ground_truth.differential (C11) | DLB and FTD moderate without supporting features. | FIXED: both low with the excluding features from the case; depression low with GDS 5/15 noted as possibly coexisting; reversible causes low with the actual values. |
| B | minor | followup_outputs[neuropsych].impression (C4) | Ended "consistent with amnestic mild cognitive impairment, multi-domain type" in a dementia-labelled case with IADLs lost; "no benefit from cuing" stated without a recognition or cued measure; em dash. | FIXED: canonical C4 wording; RAVLT recognition 2nd percentile added (findings and quantitative_data); "tested with hearing aids in place" (he has known hearing loss). |
| B | minor | followup_outputs[CSF] (C6) | 14-3-3 and RT-QuIC; "N/A" artifact; glucose ratio 0.58 for 70/118 = 0.59; non-vocabulary keys. | FIXED: removed, ratio 0.59, vocabulary keys, pattern interpretation; values unchanged. |
| C | major | ground_truth.action_criteria[action-8-analyze-csf] (C2) | Single-route criterion; an amyloid PET order would have received the library's negative PET. | FIXED: CSF or amyloid PET alternatives, plan text; new follow-up `order_amyloid_pet` (florbetapir, positive, centiloid 82). Probe: alt1 <- followup `request_csf_biomarkers`, alt2 <- followup `order_amyloid_pet`. |
| C | minor | followup_outputs (plan Q4) | FDG-PET would have returned the library's normal study. | FIXED: concordant follow-up `order_fdg_pet` (temporoparietal and posterior cingulate hypometabolism), no criterion; verified served from the case. |
| B | major | followup_outputs[drug check], action-9 (C1.2) | Heart rate 76 vs vitals 72; criterion matched any drug. | FIXED: optional, `{"drug": "donepezil"}`, last; output rewritten with HR 72, tamsulosin additive orthostatic/syncope risk, aspirin gastrointestinal risk, no interaction with metformin, amlodipine, losartan. Leak guard passes. |
| C | major | ground_truth.assessment (C12, C7.4) | Musts restating tool steps and the engineering biomarker must; generic prohibitions (anticholinergics, benzodiazepines, antipsychotics) not relevant here; no AChEI must; no vascular must despite BP 149/84, HbA1c 6.9%, lacunes and no statin. | FIXED: musts are informant, case-specific safety (driving evaluation, car left running, doors, finances, medicines), disclosure, AChEI trial with tamsulosin and aspirin counseling [NICE_NG97], vascular risk (blood pressure, lipid profile and statin, HbA1c), mood reassessment, biomarker offer. Prohibitions: do not attribute to depression or hearing loss; memantine at the mild stage. |
| C | minor | ground_truth.key_clinical_evidence (C10) | Generic items (MRI "sufficient" for probable AD, APOE, B12). | FIXED: four items true for this case, including co-pathology with small vessel disease. |
| A | minor | action_criteria citations and rationales (C13) | Duplicated citations; rationale copied from label. | FIXED; expected evidence of assessment, neuropsych, labs and MRI states this case's results (MRI now includes the vascular findings). |
| C | minor | sequence_constraints, stop_rule (C16) | | FIXED: clinical assessment before biomarker (soft) added; MRI before CSF kept; max_additional_actions 1. |
| E | minor | fallback literature, metadata, avoided rationales | Literature fallback with case content; metadata described the single-route design; generic avoided rationales. | FIXED: literature fallback null (and its fallback_tool_kinds entry); metadata points updated; patient-specific avoided rationales. Other fallbacks (Holter, CT, ECG, echo) normal and consistent, kept. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis unchanged (mild Alzheimer dementia, amnestic, G30.1): his wife took over the finances a year ago and now accompanies him when he drives after a wrong turn on a familiar route. The bedside assessment now records that cues did not help recall, and the neuropsychology report states multi-domain amnestic impairment at a mild-dementia level with an added recognition score. A sodium of 154 with chloride 93, which no part of the case explained, was corrected to normal values; the CMP now has hepatic values, the red-cell indices agree, and diabetes (HbA1c 6.9%) remains the abnormal metabolic finding. The MRI report lists the basal ganglia lacunes as a finding, no longer mentions contrast or MRA, and the differential now treats small vessel disease as a moderate contributor instead of saying there was none. Amyloid status is optional by CSF or a new concordant positive amyloid PET, with a concordant FDG-PET if ordered. Management musts now include safety specific to his incidents, a cholinesterase-inhibitor trial with counseling about tamsulosin and aspirin, blood pressure, lipid and statin management, and mood reassessment.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms: `accepted` carries "posterior cortical atrophy", "benson syndrome", "early onset alzheimer" and icd G30.0 in a late-onset amnestic case (plan 5.1).
- Citation key `[NICE_NG97]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)
None. The label stays "Early-stage Alzheimer's disease (mild dementia, amnestic)" without a cerebrovascular qualifier because no reviewer ruled on it; the cerebrovascular contribution is carried by the differential, key evidence and musts. If the lead applies the RM01/RM02 "with cerebrovascular copathology" wording condition-wide, this case qualifies (Fazekas 2, bilateral lacunes).

## Verification
Checked against the plan (C1 to C16, sections 3.1 to 3.6) and PATTERNS.md: log claims against the file, criterion order and tiers, the biomarker criterion's two alternatives each answered by a case-authored follow-up (CSF and amyloid PET, plus a concordant FDG-PET), fallbacks (advanced_imaging, literature and drug_interactions null where required; the remaining Holter, CT, ECG, echo and EEG fallbacks read), CSF arithmetic (Abeta42/40 ratio, CSF/serum glucose ratio), CBC indices, musts and prohibitions against allergies, medicines and avoided actions, the differential against the final evidence, and leakage of expected evidence into any-query outputs (test_case_guards passes).
Found and fixed:
- patient.neurological_exam.mental_status and clinical_assessment.findings[1]: the exam says he "fails three-step commands", which costs at least one point on the MMSE three-stage command, but the listed items (recall 3, orientation 2, serial sevens 3, pentagons 1) already account for all 9 points of 21/30. Serial sevens set to 2 errors and the three-stage command point added, so the list adds up to 21/30 and agrees with the command failure. Score unchanged.
- followup_outputs[CSF].glucose_ratio and interpretation: the paired serum glucose (118 mg/dL) was the same template value in S02, S03, S04 and S05; set to this case's panel glucose of 107 mg/dL, ratio 70/107 = 0.65.
Checked and accepted: B12 310 pg/mL on 12 years of metformin with mild distal vibration loss and no MMA criterion. 310 pg/mL (about 229 pmol/L) is above the plan's indeterminate band, homocysteine is normal (12.6 umol/L), and a functional deficiency would usually raise it; the differential states the values. Sodium 154 and chloride 93 (anion gap 33, never addressed) corrected to normal by the worker: accepted as a template error. Must on statin start (type 2 diabetes at 74, lacunes, no statin listed) is guideline-consistent. Drug-check content (tamsulosin syncope, aspirin and gastric acid) is correct; heart rate 72 matches the vitals.
Flag for the lead (not changed here): S02, S03 and S04 are near-duplicates from one template: retired postal worker, "wife of 50 years", the same metformin, amlodipine, losartan, (rosuvastatin), tamsulosin and aspirin list, father with hypertension and diabetes who died of stroke at 71, 15 pack-years quit 20 years ago, the television remote, a 30-year route, MMSE 21/30 with the same item pattern, and identical neuropsychology percentiles (Animals 8th, FAS 22nd in all three). The same question as plan Q5 (RP01/RP02).
perfect_agent.py -v and case_io.py check: clean after the edits.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
- MMSE orientation: 2 points were lost but only the date error was named; the second error (day of the week) is now stated in the exam and in clinical assessment findings[0], so the items sum to the stated total.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; "early onset alzheimer" and code G30.0 (onset at 65 or later); code G30.8 (atypical presentations only). Added "late onset alzheimer". Now: codes ['G30.1', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'late onset alzheimer'].
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
