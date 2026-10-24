# ALZ-EARLY-RS02
Reviewer status: R1 none, R2 none (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for ALZ-EARLY-RS02. The plan's classes (C1 to C16) were applied as class rulings (ROUND_POLICY ruling 2); each change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B/D | major | initial_tool_outputs.clinical_assessment (impression, scores, findings) | Template impression with the engineering sentence; findings copied HPI sentences, one truncated ("Alert and oriented to person and place;"); cueing field false with no cueing recorded (C3) | FIXED: impression from the case (MMSE 21/30 with item losses, domains, cueing, informants, functional stage); scores give MMSE, cued recall (0/3 free, 0/3 category cue, 1/3 multiple choice), clock, functional stage; findings by domain. `independence_in_instrumental_activities_lost` already true and correct |
| B | major | followup_outputs[neuropsych].impression | "consistent with amnestic mild cognitive impairment, multi-domain type" in a mild dementia case (C4) | FIXED: plan canonical mild dementia wording |
| B | minor | followup_outputs[neuropsych] | "storage-type deficit" and the criterion's "limited benefit from cueing" with no recognition trial in the battery | FIXED: RAVLT recognition (2nd percentile) added to findings and quantitative_data; impression cites it |
| E | minor | patient.neurological_exam.mental_status | "delayed copy of intersecting pentagons" (the pentagon item is a copy, not delayed) | FIXED: "copy of intersecting pentagons" |
| B/D | major | followup_outputs[CSF] | 14-3-3 and RT-QuIC in a non-rapid case (C6); "(N/A PMN/N/A lymph)" artefact | FIXED: both removed; keys renamed to the vocabulary analytes; interpretation states values and the pattern ("consistent with Alzheimer disease pathology"; amyloid and p-tau both abnormal) |
| C | major | ground_truth.action_criteria[action-8-analyze-csf] | "single optional route"; amyloid PET would be answered by the negative library default (C2) | FIXED: CSF and amyloid_PET alternatives, canonical label, rationale, expected evidence; new follow-up `order_amyloid_pet` (18F-florbetapir, positive, Centiloid 74) |
| C | major | followup_outputs[search_early_alzheimers_treatment] | Literature step citing a non-existent "2023 AAN Practice Guideline Update: MCI and Early AD" (C8) | FIXED: deleted |
| C | major | followup_outputs[check_drug_interactions_donepezil] | "baseline ECG recommended given patient's age" while ECG is an avoided waste action and he takes no QT-prolonging drug; aspirin interaction missed; vague BP statement (C1.2) | FIXED: ECG recommendation removed; aspirin (gastric acid, GI bleeding), tamsulosin (orthostatic, bladder outflow), metformin and rosuvastatin content; heart rate 72/min from the vitals; sulfonamide allergy stated as not cross-reacting |
| C | minor | ground_truth.action_criteria[action-9-check-drug-interactions] | `required_arguments` {}; rationale = label (C1.2, C13) | FIXED: {"drug": "donepezil"}, optional, last |
| B | minor | initial_tool_outputs.labs | HbA1c 6.4% flagged normal against a "<5.7 normal" range; interpretive text in abnormal_values_summary ("consistent with known type 2 diabetes"); CMP ordered but no liver tests returned (C7.1) | FIXED: HbA1c is_abnormal true; summary and interpretation list values only; hepatic panel added (AST 24, ALT 21, ALP 82, bilirubin 0.6, albumin 4.1, total protein 7.2, all normal) |
| D | major | initial_tool_outputs.mri | "No abnormal enhancement on post-gadolinium sequences" with contrast false (C5); impression omitted the Evans index 0.33 ventriculomegaly reported in the findings | FIXED: phrase removed; numbered impression includes the ventriculomegaly, states no DESH (added to the ventricular finding), ends with the canonical pattern sentence |
| B | minor | initial_tool_outputs.labs.panels.Reviewed_cognitive_panel_additions | Magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8: identical to RS01 and RS03 (template carry-over, PATTERNS 4) | FIXED: 2.1 mg/dL, 11.4 umol/L, 15 mm/h, 1.2 mg/L (all normal; no other field quotes them) |
| C | major | ground_truth.differential | DLB and FTD moderate against the history (C11); NPH absent although the case raises it (Evans 0.33, mildly slow gait with shortened stride) (ruling 7) | FIXED: DLB and FTD low with excluding features; NPH added, low, with excluding features; VCI key features name the diabetes, hypertension and Fazekas 1-2 background |
| C | minor | ground_truth.red_herrings | The NPH-like data were undeclared | FIXED: declared as red_herrings[0] |
| A/B | minor | ground_truth.action_criteria[*] | Duplicated citations; rationale = label; generic expected evidence (C13) | FIXED: one key each; patient-specific rationales; case values in expected evidence |
| C | major | ground_truth.assessment.required_recommendations | Musts restating criteria and the "single case-designated optional biomarker route" must; no driving decision despite disorientation while driving (C12, C2.5) | FIXED: six musts: disclosure; driving (no driving until formal assessment, local rules); home and medicine safety; C1 dementia AChEI must with aspirin and BPH cautions; C2 biomarker must; vascular risk and exercise |
| C | minor | ground_truth.assessment.prohibited_recommendations | Generic five (C12.2) | FIXED: anticholinergic drugs named for his back pain and BPH; "do not attribute to depression" with his GDS; memantine at the mild stage |
| C | major | ground_truth.key_clinical_evidence | Same generic items as the condition (C10): probable AD "sufficient" from MRI, APOE, B12 (normal here), unsourced AChEI | FIXED: four items (NIA-AA 2011 clinical diagnosis, storage-type memory, Evans index versus NPH, AChEI/memantine [NICE_NG97]) |
| C | minor | ground_truth.sequence_constraints, stop_rule | C16 | FIXED: clinical assessment before biomarker (soft); max_additional_actions 1 |
| B | minor | metadata | "single route" wording | FIXED |
| C | check | 3.6 check | every alternative probed on a fresh environment | CSF <- `request_csf_biomarkers`; amyloid PET <- `order_amyloid_pet`; drug check <- `check_drug_interactions_donepezil`; required criteria <- initial outputs; no library answer |
| C | note | avoided_actions[avoid-waste-1-analyze-ecg] | ECG stays waste: no QT-prolonging co-medication, HR 72, no conduction history (C14 does not apply) | no change |

## Changes, in one paragraph a physician can read before re-reviewing
The clinical assessment now documents this case (MMSE 21/30 with its item losses, no benefit from cues, the wife's and son's account) and the neuropsychological impression calls it mild dementia, matching the loss of instrumental independence (finances taken over, driving and cooking supervised); a RAVLT recognition score was added so the storage-type statement rests on data. The MRI no longer mentions gadolinium, reports the Evans index 0.33 without DESH in its impression, and NPH is now in the differential as low, declared as the red herring. The CSF report drops 14-3-3, RT-QuIC and the N/A artefact; amyloid status can be established by CSF or a positive amyloid PET. The literature step (a fabricated 2023 AAN guideline) is gone. The donepezil check is optional and limited to donepezil, no longer recommends an ECG, and adds the aspirin and BPH cautions. Musts: disclosure, no driving until formal assessment, home and medicine safety, a cholinesterase inhibitor trial, biomarker testing only if it changes management, vascular risk and exercise. DLB and FTD are low. HbA1c 6.4% is flagged against its range and liver tests were added to the CMP.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used before they exist centrally (plan 5.2): `[NICE_NG97]`, `[Beers_2023]`.
- Synonyms (plan 5.1): `accepted` carries "posterior cortical atrophy", "benson syndrome" and "early onset alzheimer" for a 76-year-old with late-onset amnestic AD (G30.1), granted through G30.0 in `icd_codes`.

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Method: read the log, the full git diff and the whole final case (large rewrite, no reviewer notes); checked every Own-findings claim against the file; MMSE item arithmetic against the exam and the clinical assessment; CSF Abeta42/40 and glucose ratios against Abeta40 and serum glucose; heart rate in the drug check against the vitals; labels, ICD, staging field, both impressions and musts for one staging; differential against the final evidence; red-herring field paths; avoided actions against criteria and musts; fallbacks for case consistency. Probed on a fresh environment that CSF, amyloid PET and the donepezil check are answered by case-authored outputs (no library answer). perfect_agent.py -v: ok. case_io.py check: schema OK, synonym guard OK, no test failure names this case. Not a reviewed or approved case; no note ids exist for it in the notes file (none missing from the table).

Findings:
- B, minor, patient.neurological_exam.mental_status and initial_tool_outputs.clinical_assessment.findings[Orientation]: MMSE itemises orientation -3, but the text ("knows the month and year but not the date or the day of the week", oriented to place) accounts for only 2 points. FIXED in both places: "knows the year and the season but cannot state the month, the exact date or the day of the week" (losses now 3+3+2+1 = 9, MMSE 21/30).
- Every other claim in the log holds: CSF ratio 362/7800 = 0.046 and glucose ratio 68/112 = 0.61 match the labs; NPH entry low and red herring path mri.findings[3] is the ventricular finding; ECG recommendation gone and ECG stays an avoided waste action consistent with no QT drug; HbA1c flagged.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (the labs criterion label), the wording the other six cases already use.
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- CBC indices made consistent (MCV = hematocrit x 10 / RBC): RBC 4.3 to 4.8; values within reference ranges and cited nowhere else in the case.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; "early onset alzheimer" and code G30.0 (onset at 65 or later); code G30.8 (atypical presentations only). Added "late onset alzheimer". Now: codes ['G30.1', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'late onset alzheimer'].
- Added follow-up `order_advanced_imaging` FDG_PET (trigger `order_fdg_pet`, no criterion), after the amyloid-status follow-ups: a case-specific Alzheimer-type metabolic report concordant with the MRI and stage. Before, an FDG order returned the library's normal scan, contradicting the case (summary Q4). Probed: FDG and amyloid PET orders each return their own report, in either order.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.
