# ALZ-EARLY-S03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The case has no reviewer notes. The condition-plan classes C1 to C16 were applied as a class (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | initial_tool_outputs.clinical_assessment.criteria_met.independence_in_instrumental_activities_lost | False, while the HPI says her wife has taken over the finances and she no longer drives alone after getting lost, and the label and impression say dementia (plan C4). | FIXED: true. Staging per plan 1.2: mild dementia; onset at about 67, G30.1 correct; label unchanged. |
| D | major | initial_tool_outputs.clinical_assessment.impression, .findings, .scores | Template impression with the engineering sentence; fragment row; the decisive IADL facts (finances, driving) missing from the findings. | FIXED: impression rewritten from the case (MMSE 21/30 domains, no phonemic cue benefit, wife's report, finances and driving); rows rebuilt including judgment and basic ADL. Cueing field false kept (consistent with the exam). |
| B | major | initial_tool_outputs.labs.panels.BMP (sodium, chloride) | Sodium 149 and chloride 111 mEq/L in a well outpatient, never addressed by any must, criterion or differential (template value). | FIXED: sodium 141, chloride 104; abnormal summary and interpretation updated (glucose 113, HbA1c 6.9% remain). |
| B | minor | initial_tool_outputs.labs.panels.CBC | Male reference ranges for RBC (4.30-5.70) and hematocrit (39.0-50.0) in a woman; hematocrit 45.6 with Hb 13.6 and RBC 4.45 gives MCV 102, not 95.3. | FIXED: female ranges (3.80-5.10, 36.0-46.0); hematocrit 40.8, MCV 91.7. |
| B | minor | initial_tool_outputs.labs.panels | CMP ordered, BMP returned. | FIXED: renamed CMP with total protein 7.1, albumin 4.2, AST 19, ALT 17 (female range 7-35), ALP 77, bilirubin 0.5. |
| B | minor | initial_tool_outputs.labs.panels.Reviewed_cognitive_panel_additions | Template values shared with 25 cases; ESR reference 0-20 is the young-adult range. | FIXED: magnesium 1.9, homocysteine 13.1, ESR 22 (reference 0-30 for a woman of 69), CRP 2.1 (all normal). |
| C | major | ground_truth.action_criteria, followup_outputs (C7.2) | B12 260 pg/mL (low-normal) after 12 years of metformin, with reduced vibration at the great toes, and no MMA. | FIXED: criterion `action-10-interpret-labs-mma` (recommended, after labs) and follow-up `request_methylmalonic_acid` (0.31 umol/L, within range; homocysteine normal). Result kept normal because homocysteine is normal and the distal vibration loss is explained by diabetes. |
| D | major | initial_tool_outputs.mri | "No abnormal meningeal enhancement on post-contrast sequences" with contrast false (C5); "two small old lacunar infarcts ... likely incidental" dismisses a finding (style guide). | FIXED: post-contrast line removed; lacunes moved to a finding row (left putamen, 4 and 5 mm) and named in a numbered impression with the Fazekas 2 disease as moderate small vessel disease; SWI states no microbleeds. |
| B | major | ground_truth.differential[Vascular cognitive impairment] | "No significant cerebrovascular burden on MRI" contradicted Fazekas 2 and two lacunes. | FIXED: VCI as a moderate contributor with the features that keep AD primary. |
| C | major | ground_truth.differential (C11) | DLB and FTD moderate without supporting features. | FIXED: low with the case's excluding features; depression low (GDS 5/15, may coexist); reversible causes low with the actual values including MMA. |
| B | minor | followup_outputs[neuropsych].impression (C4) | "Amnestic mild cognitive impairment, multi-domain type" in a dementia case; em dash. | FIXED: canonical C4 wording; RAVLT recognition 1st percentile added (findings, quantitative_data). |
| B | minor | followup_outputs[CSF] (C6) | 14-3-3, RT-QuIC, "N/A" artifact; glucose ratio 0.58 for 64.6/118 = 0.55; non-vocabulary keys. | FIXED; values otherwise unchanged. |
| C | major | action-8-analyze-csf (C2) | Single route; PET would have returned the library's negative PET. | FIXED: CSF or amyloid PET alternatives; follow-up `order_amyloid_pet` (flutemetamol, positive, centiloid 69). Probe: alt1 <- `request_csf_biomarkers`, alt2 <- `order_amyloid_pet`. |
| C | minor | followup_outputs (plan Q4) | FDG-PET would have returned the library's normal study. | FIXED: concordant `order_fdg_pet` follow-up, no criterion. |
| B | major | followup_outputs[drug check], action-9 (C1.2) | Heart rate 76 vs vitals 79; criterion matched any drug. | FIXED: optional, `{"drug": "donepezil"}`, last; output with HR 79, aspirin gastrointestinal caution, weight loss and metformin, no interaction with the other medicines. Leak guard passes. |
| C | major | ground_truth.assessment (C12) | Restating musts, engineering biomarker must, generic prohibitions; no AChEI or vascular must. | FIXED: musts are informant, driving cessation pending formal evaluation, finances and medicines supervision, disclosure, AChEI trial [NICE_NG97], vascular management, mood reassessment, biomarker offer. Prohibitions: attributing to depression or aging; memantine at the mild stage. |
| C | minor | key_clinical_evidence (C10) | Generic items (MRI "sufficient", APOE). | FIXED: four items true for this case (B12 item kept, now relevant). |
| A | minor | criteria citations and rationales (C13) | Duplicates; rationale copied from label. | FIXED; expected evidence states this case's results. |
| C | minor | sequence_constraints, stop_rule (C16) | | FIXED: clinical assessment before biomarker added; MRI before CSF kept; max_additional_actions 1. |
| E | minor | fallback literature, metadata, avoided rationales | Generic "general" literature fallback; metadata single-route text; generic rationales. | FIXED: literature fallback null; metadata updated; patient-specific rationales. Other fallbacks normal and consistent, kept. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis unchanged (mild Alzheimer dementia, amnestic, G30.1), and the functional field now agrees with the history: her wife took over the finances and she stopped driving alone after getting lost on a familiar route. The bedside assessment and the neuropsychology report now describe her own results, with an added recognition score at the 1st percentile; the neuropsychology impression no longer says MCI. An unexplained sodium of 149 and chloride of 111 were corrected to normal; the CBC now uses female reference ranges with consistent indices, and the CMP includes hepatic values. Her low-normal B12 of 260 pg/mL on long-term metformin is followed by a recommended methylmalonic acid, which is within range. The MRI no longer mentions post-contrast sequences and reports the two putaminal lacunes and Fazekas 2 disease as moderate small vessel disease, which the differential now treats as a contributor. Amyloid status is optional by CSF or a new concordant positive amyloid PET, with a concordant FDG-PET if ordered. Musts add driving cessation pending evaluation, a cholinesterase-inhibitor trial, vascular management and mood reassessment.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms: PCA, Benson and early-onset labels and G30.0 in a late-onset amnestic case (plan 5.1).
- Citation keys `[NICE_NG97]`, `[BSH_B12_2014]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Checked against the plan (C1 to C16, sections 3.1 to 3.6) and PATTERNS.md: log claims against the file, criterion order and tiers, the biomarker criterion's two alternatives each answered by a case-authored follow-up (CSF and amyloid PET, plus a concordant FDG-PET), fallbacks (advanced_imaging, literature and drug_interactions null where required; the remaining Holter, CT, ECG, echo and EEG fallbacks read), CSF arithmetic (Abeta42/40 ratio, CSF/serum glucose ratio), CBC indices, musts and prohibitions against allergies, medicines and avoided actions, the differential against the final evidence, and leakage of expected evidence into any-query outputs (test_case_guards passes).
Found and fixed:
- patient.neurological_exam.mental_status and clinical_assessment.findings[1]: MMSE items listed sum to 21/30 while the exam records difficulty with three-step commands (an MMSE item); serial sevens set to 2 errors and the three-stage command point added. Score unchanged.
- patient.clinical_history.social_history.living_situation: "her wife of 50 years" for a 69-year-old woman dates a same-sex marriage to 1976, which could not have happened (template carry-over from S02); now "her wife, her partner of 50 years".
- initial_tool_outputs.labs CMP creatinine: the worker moved the CBC to female ranges but left the male creatinine range (0.70-1.30); now 0.50-1.10 (value 1.02 still normal).
- HbA1c 6.9% was the same value as S02 (template); set to 7.2% in the panel, the abnormal summary, the interpretation, the labs expected evidence and the differential (still controlled for her age).
- followup_outputs[CSF]: Abeta40 7800, total tau 520 and serum glucose 118 were identical to S02 and S04. Abeta40 8100 (ratio 342/8100 = 0.042), total tau 545, serum glucose 113 (her panel value; ratio 64.6/113 = 0.57); interpretation updated. The profile is unchanged (decreased ratio, raised p-tau and t-tau).
- initial_tool_outputs.mri.findings[2]: "disproportionate to the patient's stated age" now "disproportionate to age".
Checked and correct: B12 260 on metformin with MMA recommended and normal; IADL field true (finances taken over, no solo driving); MCV 40.8/4.45 = 91.7; drug-check heart rate 79.
Flag for the lead: near-duplicate of S02 and S04 (see the S02 verification).
perfect_agent.py -v and case_io.py check: clean after the edits.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
- MMSE orientation: 2 points were lost but only the date error was named; the second error (day of the week) is now stated in the exam and in clinical assessment findings[0], so the items sum to the stated total.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; "early onset alzheimer" and code G30.0 (onset at 65 or later); code G30.8 (atypical presentations only). Added "late onset alzheimer". Now: codes ['G30.1', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'late onset alzheimer'].
- Dataset diversity (auditor flag, S02/S03/S04 all retired postal workers): occupation "retired postal worker" -> "retired hospital pharmacy technician" (HPI and social history). No clinical content changed.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.
