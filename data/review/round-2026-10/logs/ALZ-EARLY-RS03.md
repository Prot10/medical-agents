# ALZ-EARLY-RS03
Reviewer status: R1 none, R2 none (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for ALZ-EARLY-RS03. The plan's classes (C1 to C16) were applied as class rulings (ROUND_POLICY ruling 2); each change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B | major | initial_tool_outputs.clinical_assessment.criteria_met.independence_in_instrumental_activities_lost | false, while the husband took over the finances and supervises cooking, the daughter set up her medicines and she no longer walks out alone after getting lost; label mild dementia (C4) | FIXED: true |
| B/D | major | initial_tool_outputs.clinical_assessment | Template impression with engineering sentence; findings copied HPI sentences, one truncated (C3) | FIXED: impression and findings from the case; cueing field false now grounded in the exam ("even with categorical cues") |
| B | major | patient.neurological_exam.mental_status, clinical_assessment | MMSE 21/30 but the listed losses sum to 8 (recall 3, orientation 3, serial sevens 2) | FIXED: one point on the three-stage command added (the exam already records difficulty with a three-step command) |
| B | major | followup_outputs[neuropsych].impression | "amnestic mild cognitive impairment, multi-domain type" in a dementia case (C4) | FIXED: plan canonical mild dementia wording |
| B | minor | followup_outputs[neuropsych] | Scores identical to RS02 (RAVLT 3rd/1st, Category 8th, TMT-A 28th, TMT-B 15th, Rey 30th): template carry-over; "storage-type" with no recognition trial | FIXED: RAVLT immediate 4th, delayed <1st, recognition 3rd (new), Category 6th, TMT-A 34th, TMT-B 12th, Rey copy 26th; impression updated |
| B/D | major | followup_outputs[CSF] | 14-3-3 and RT-QuIC in a non-rapid case (C6); N/A artefact; p-tau 84 and t-tau 512 identical to RS02; opening pressure 14 in every case | FIXED: 14-3-3 and RT-QuIC removed; keys renamed to the vocabulary analytes; p-tau181 91, t-tau 547, opening pressure 16; interpretation states values and the pattern |
| C | major | ground_truth.action_criteria[action-8-analyze-csf] | "single optional route"; amyloid PET answered by the negative library default (C2) | FIXED: CSF and amyloid_PET alternatives, canonical texts; new follow-up `order_amyloid_pet` (18F-flutemetamol, positive, Centiloid 81) |
| C | major | followup_outputs[search_alzheimer_treatment_guidelines] | Literature step citing a non-existent "2023 AAN Practice Guideline: MCI and Early AD" (C8) | FIXED: deleted |
| C | minor | followup_outputs[request_autonomic_testing] | Tilt-table follow-up with no criterion, repeating the exam's orthostatic vitals (C9; carry-over from the MSA source case) | FIXED: deleted. The remote orthostatic dizziness resolved with amlodipine dose reduction, there is no orthostatic drop on examination and no DLB core feature, so a DLB differential does not need it; declared as the red herring instead |
| C | major | followup_outputs[check_drug_interactions_donepezil] | "monitor heart rate, particularly in combination with amlodipine" (amlodipine does not slow the heart) (C1.2) | FIXED: rewritten per plan 1.2 with metformin and alendronate gastrointestinal content, heart rate from the vitals, sulfonamide allergy stated as not cross-reacting; criterion {"drug": "donepezil"}, optional, last |
| B | minor | patient.vitals, patient.neurological_exam.additional | Vitals identical to RS02 (138/78, 72) | FIXED: BP 134/76, HR 68; orthostatic values in the exam 134/76 supine, 128/72 standing; the drug check quotes 68/min |
| B | minor | initial_tool_outputs.labs | Interpretive summary ("fair glycemic control"); CMP without liver tests; reviewed-panel additions and CBC values identical to RS01/RS02 (C7.1, PATTERNS 4) | FIXED: values-only summary and interpretation; hepatic panel added (normal); magnesium 1.9, homocysteine 9.6, ESR 18, CRP 2.3; WBC 6.4, RBC 4.4, platelets 231, MCV 89.6 (all normal) |
| D | major | initial_tool_outputs.mri | White matter "age-appropriate for a 73-year-old with vascular risk factors" (cross-modality); impression led with posterior fossa negatives and "hot cross bun"/"hummingbird" signs from the MSA source; ventriculomegaly absent from the impression (C5, PATTERNS 4) | FIXED: findings-only white matter text; MSA signs consolidated to "Normal brainstem and cerebellar volume and signal"; numbered impression with ex vacuo ventricular enlargement and the canonical pattern sentence |
| C | major | ground_truth.differential | DLB and FTD moderate (C11); depression entry did not acknowledge GDS 5, tearfulness and loss of interest | FIXED: DLB and FTD low with excluding features; depression low as the cause with coexisting symptoms named |
| C | major | ground_truth.assessment | Template musts and prohibitions (C12, C2.5); no must for her depressive symptoms; medicine safety not addressed although doses are being missed | FIXED: six musts (disclosure; safety with supervised medicines, cooking, finances, wayfinding; AChEI trial; biomarker canonical; depressive symptoms with a low-anticholinergic antidepressant if needed; vascular risk); four prohibitions (tricyclic or paroxetine; benzodiazepine for distress, with osteoporosis; attributing to depression; memantine at the mild stage) |
| C | major | ground_truth.key_clinical_evidence | Generic items (C10) | FIXED: four items (NIA-AA 2011, storage-type memory, depression versus neurodegenerative memory deficit, AChEI/memantine) |
| A/B | minor | ground_truth.action_criteria[*] | Duplicated citations; rationale = label; generic expected evidence (C13) | FIXED |
| C | minor | ground_truth.sequence_constraints, stop_rule | C16 | FIXED: clinical assessment before biomarker (soft); max_additional_actions 1 |
| B | minor | metadata | "single route" wording | FIXED; `adaptation_notes` kept |
| C | check | 3.6 check | every alternative probed on a fresh environment | CSF <- `request_csf_biomarkers`; amyloid PET <- `order_amyloid_pet`; drug check <- `check_drug_interactions_donepezil`; no library answer |

## Changes, in one paragraph a physician can read before re-reviewing
The case is now consistently mild dementia: the instrumental-independence field is true and the neuropsychological impression no longer says MCI. The MMSE arithmetic is fixed (one point on the three-stage command). The clinical assessment reports her own findings, including no benefit from category cues. The autonomic (tilt-table) follow-up, which had no criterion and only repeated the bedside orthostatic vitals, was removed; the remote drug-related orthostatic dizziness is declared as a red herring. The MRI drops the MSA-specific signs and the clinical reference to vascular risk factors. The CSF report drops 14-3-3, RT-QuIC and the N/A artefact; amyloid status can come from CSF or a positive amyloid PET. The literature step (a fabricated 2023 AAN guideline) is gone; the donepezil check is optional, limited to donepezil and pharmacologically correct. Management now includes supervised medicines, cooking and finances, wayfinding safety, a cholinesterase inhibitor trial, attention to her depressive symptoms (avoiding tricyclics, paroxetine and benzodiazepines) and vascular risk. DLB and FTD are low. Several numbers duplicated from RS02 (neuropsych scores, CSF tau, vitals, labs) were changed to distinct plausible values, all agreeing across fields.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used before they exist centrally (plan 5.2): `[NICE_NG97]`, `[Beers_2023]`.
- Synonyms (plan 5.1): `accepted` carries "posterior cortical atrophy", "benson syndrome" and "early onset alzheimer" for a 73-year-old with late-onset amnestic AD (G30.1), granted through G30.0 in `icd_codes`.

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Method: read the log, the full git diff and the whole final case (large rewrite, no reviewer notes); checked every Own-findings claim against the file; MMSE item arithmetic against the exam and the clinical assessment; CSF Abeta42/40 and glucose ratios against Abeta40 and serum glucose; heart rate in the drug check against the vitals; labels, ICD, staging field, both impressions and musts for one staging; differential against the final evidence; red-herring field paths; avoided actions against criteria and musts; fallbacks for case consistency. Probed on a fresh environment that CSF, amyloid PET and the donepezil check are answered by case-authored outputs (no library answer). perfect_agent.py -v: ok. case_io.py check: schema OK, synonym guard OK, no test failure names this case. Not a reviewed or approved case; no note ids exist for it in the notes file (none missing from the table).

Findings:
- B, minor, patient.neurological_exam.mental_status and clinical_assessment.findings[Orientation]: same defect as RS02 left by the worker's MMSE fix: orientation -3 itemised but the text accounts for 2 points (date, day). FIXED: "knows the year and the season but cannot state the month, the exact date or the day of the week" (losses 3+3+2+1 = 9, MMSE 21/30).
- B, minor, fallback_tool_outputs.ct: a 3 mm calcified right frontal "granuloma" that the MRI (SWI reported clear) never shows. FIXED: findings emptied, impression "No acute intracranial abnormality. No hemorrhage, mass, hydrocephalus or large-territory infarct."; metadata.fallback_tool_kinds.ct "incidental" to "normal".
- B, minor, fallback_tool_outputs.ecg.rate 88 against a resting HR of 68 (vitals, drug check). FIXED: 70.
- FLAGGED for the lead (template carry-over, PATTERNS 4, not rewritten here): RS03 (Yumi Tanaka, 73) and RS04 (Yoshiko Tanaka, 79) are both retired seamstresses from a garment factory for 35 years, high school, never smokers, sulfonamide urticaria, amlodipine 5 mg plus alendronate, with the same "clock numbers clustered on the right" item. Differentiating one identity would rewrite the HPI; a decision for the lead or Andrea.
- Every other claim in the log holds: autonomic follow-up gone; CSF 348/7850 = 0.044, glucose 72.5/118 = 0.61; HR 68 in vitals and drug check; orthostatic values in the exam match the new BP; red herring path past_medical_history[4] is the orthostatic history.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (the labs criterion label), the wording the other six cases already use.
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
