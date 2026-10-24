# ALZ-EARLY-RS04
Reviewer status: R1 none, R2 none (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for ALZ-EARLY-RS04. The plan's classes (C1 to C16) were applied as class rulings (ROUND_POLICY ruling 2); each change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B | major | initial_tool_outputs.clinical_assessment.criteria_met.independence_in_instrumental_activities_lost | false, while her daughter took over the finances after an electricity disconnection and she cannot operate her washing machine; label mild dementia (C4) | FIXED: true |
| B/D | major | initial_tool_outputs.clinical_assessment | Template impression with engineering sentence; informant findings copied HPI sentences (one starting "Tanaka, who was..."); cueing field false with no cueing recorded (C3) | FIXED: impression and findings by domain from the case; scores give MMSE with item losses, cued recall (0/3 free, 0/3 category cue, 1/3 multiple choice), clock, animals 9/60 s, functional stage |
| B | major | patient.neurological_exam.mental_status, clinical_assessment | MMSE 21/30 but the listed losses sum to 8 | FIXED: one point on the three-stage command added (the exam already records the omitted last step) |
| B | major | followup_outputs[neuropsych].impression | "amnestic mild cognitive impairment, multi-domain type" in a dementia case (C4) | FIXED: plan canonical mild dementia wording |
| B | minor | followup_outputs[neuropsych] | Scores copied from RS03 (MMSE/MoCA 21/16, RAVLT 3rd/1st, BNT 20th, Category 8th, TMT-B 15th, GDS 5); "storage-type" without a recognition trial; GDS 5 "borderline" while the HPI denies persistent sadness and anhedonia | FIXED: MoCA 15, RAVLT 5th/2nd, recognition 4th (new), BNT 16th, TMT-B 11th, GDS 4/15 (normal); impression updated |
| B/D | major | followup_outputs[CSF] | 14-3-3 and RT-QuIC in a non-rapid case (C6); N/A artefact; Abeta42 348, Abeta40 7850, ratio 0.044 and protein 41.2 identical to RS03 | FIXED: removed; vocabulary keys; Abeta42 372, Abeta40 8150, ratio 0.046, protein 44; interpretation values and pattern only |
| C | major | ground_truth.action_criteria[action-8-analyze-csf] | "single optional route"; amyloid PET answered by the negative library default (C2) | FIXED: CSF and amyloid_PET alternatives, canonical texts; new follow-up `order_amyloid_pet` (18F-florbetaben, positive, Centiloid 77) |
| C | major | followup_outputs[search_early_alzheimer_treatment] | Literature step (C8) | FIXED: deleted |
| C | major | followup_outputs[check_drug_interactions_donepezil] | "especially given concomitant amlodipine (both can lower heart rate)" (wrong); garbled constipation statement (C1.2) | FIXED: rewritten per plan 1.2 (magnesium oxide diarrhea, alendronate GI, weight loss at BMI 19.8, heart rate from the vitals, sulfonamide allergy not cross-reacting); criterion {"drug": "donepezil"}, optional, last |
| D | major | initial_tool_outputs.mri.additional_observations | "No abnormal meningeal enhancement" with contrast false (C5); "Post-cholecystectomy changes noted incidentally on lower cuts", a finding a brain MRI cannot show | FIXED: both removed; numbered impression with ex vacuo ventricular enlargement and the canonical pattern sentence |
| B | minor | fallback_tool_outputs.ecg | rhythm "normal sinus rhythm" and "Normal sinus rhythm. Sinus bradycardia, likely physiological" at rate 58 (self-contradictory, interpretive) | FIXED: rhythm "sinus bradycardia"; findings and interpretation factual |
| B | minor | patient.vitals | BP 138/78, HR 72 identical to RS01 to RS03 | FIXED: BP 142/80, HR 64 (the drug check quotes 64/min; a later fallback ECG at 58/min remains plausible) |
| B | minor | initial_tool_outputs.labs | CMP without liver tests; reviewed-panel additions and CBC values identical to other cases (PATTERNS 4) | FIXED: hepatic panel added (normal, albumin 3.8); magnesium 2.2 (on magnesium oxide), homocysteine 12.1, ESR 16, CRP 0.9; WBC 5.3, platelets 244, MCV 92.4 |
| C | major | ground_truth.differential | DLB and FTD moderate (C11) | FIXED: low with excluding features; depression entry uses the bereavement history and GDS 4/15 |
| C | major | ground_truth.assessment | Template musts and prohibitions (C12, C2.5); she lives alone with expired food, appliance failures and a utility disconnection, but no must addressed living alone | FIXED: six musts (disclosure; living-alone safety and home support with medicine supervision, carer assessment, finances and scams; AChEI trial with weight monitoring; biomarker canonical; nutrition, activity and social contact; blood pressure); three prohibitions (attributing the decline to bereavement; memantine at the mild stage; sedating or anticholinergic drugs with osteoporosis). The generic antipsychotic prohibition (no behavioural symptoms) was dropped |
| C | major | ground_truth.key_clinical_evidence | Generic items (C10) | FIXED: four items (NIA-AA 2011, storage-type memory, bereavement versus dementia in a widow living alone, AChEI/memantine) |
| C | minor | ground_truth.red_herrings | Bereavement and low mood, the case's main distractor, undeclared | FIXED: declared |
| A/B | minor | ground_truth.action_criteria[*] | Duplicated citations; rationale = label; generic expected evidence (C13) | FIXED |
| C | minor | ground_truth.sequence_constraints, stop_rule | C16 | FIXED: clinical assessment before biomarker (soft); max_additional_actions 1 |
| B | minor | metadata | "single route" wording | FIXED |
| C | check | 3.6 check | every alternative probed on a fresh environment | CSF <- `request_csf_biomarkers`; amyloid PET <- `order_amyloid_pet`; drug check <- `check_drug_interactions_donepezil`; no library answer |
| C | note | patient.neurological_exam.motor, reflexes | Hip flexors 4+/5, hyporeflexia and BMI 19.8 are attributed to sarcopenia in the exam; B12, homocysteine, TSH and electrolytes are normal | FLAGGED only: covered by the nutrition must; no neuromuscular work-up added |

## Changes, in one paragraph a physician can read before re-reviewing
Staging is now consistent with mild dementia (field true, neuropsych impression no longer says MCI) and the MMSE item losses add up to 21. The clinical assessment reports this patient's own findings with no cue benefit. The MRI drops a contrast statement and an impossible "post-cholecystectomy" observation. The CSF report drops 14-3-3, RT-QuIC and the N/A artefact; amyloid status can come from CSF or a positive amyloid PET. The literature step is gone; the donepezil check is optional, limited to donepezil and pharmacologically correct. Management now centres on her living alone: home support, food and appliance safety, supervised medicines, carer assessment for her daughter, finances and scam protection, plus a cholinesterase inhibitor trial with weight monitoring, nutrition and activity, and blood pressure. Bereavement is declared as the red herring and a prohibition on attributing the decline to grief was added. DLB and FTD are low. Numbers copied from RS03 (neuropsych scores, CSF amyloid values, vitals, labs) were changed to distinct plausible values; GDS is now 4/15, in line with the HPI.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used before they exist centrally (plan 5.2): `[NICE_NG97]`, `[Beers_2023]`.
- Synonyms (plan 5.1): `accepted` carries "posterior cortical atrophy", "benson syndrome" and "early onset alzheimer" for a 79-year-old with late-onset amnestic AD (G30.1), granted through G30.0 in `icd_codes`.

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Method: read the log, the full git diff and the whole final case (large rewrite, no reviewer notes); checked every Own-findings claim against the file; MMSE item arithmetic against the exam and the clinical assessment; CSF Abeta42/40 and glucose ratios against Abeta40 and serum glucose; heart rate in the drug check against the vitals; labels, ICD, staging field, both impressions and musts for one staging; differential against the final evidence; red-herring field paths; avoided actions against criteria and musts; fallbacks for case consistency. Probed on a fresh environment that CSF, amyloid PET and the donepezil check are answered by case-authored outputs (no library answer). perfect_agent.py -v: ok. case_io.py check: schema OK, synonym guard OK, no test failure names this case. Not a reviewed or approved case; no note ids exist for it in the notes file (none missing from the table).

Findings:
- B, minor, initial_tool_outputs.mri.findings[White matter changes].signal_characteristics.T2_FLAIR: "Punctate and early confluent" hyperintensities contradict the stated Fazekas grade 1 (beginning confluence is grade 2). FIXED: "Punctate periventricular and deep white matter hyperintensities with periventricular caps and pencil-thin lining, consistent with age-appropriate small vessel changes".
- FLAGGED (see RS03 log): near-duplicate identity with RS03 (seamstress Tanaka, same medicines and allergy).
- Every other claim in the log holds: MMSE losses 3+2+1+1+1+1 = 9 (21/30) match the exam; CSF 372/8150 = 0.046 and glucose 59.8/94 = 0.64; HR 64 in vitals and drug check, fallback ECG sinus bradycardia 58 consistent with its rhythm field; GDS 4/15 matches the HPI; bereavement declared as the red herring; the hip-flexor weakness and hyporeflexia flag is reasonable (B12 and homocysteine normal; nutrition must covers it).


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (the labs criterion label), the wording the other six cases already use.
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; "early onset alzheimer" and code G30.0 (onset at 65 or later); code G30.8 (atypical presentations only). Added "late onset alzheimer". Now: codes ['G30.1', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'late onset alzheimer'].
- Added follow-up `order_advanced_imaging` FDG_PET (trigger `order_fdg_pet`, no criterion), after the amyloid-status follow-ups: a case-specific Alzheimer-type metabolic report concordant with the MRI and stage. Before, an FDG order returned the library's normal scan, contradicting the case (summary Q4). Probed: FDG and amyloid PET orders each return their own report, in either order.
- Dataset diversity (auditor flag, near-duplicate of RS03: both "Mrs. Tanaka", retired seamstress from a garment factory, Japanese, with a daughter): surname Tanaka -> Mori, occupation seamstress -> florist who ran a neighbourhood flower shop for 35 years, and the failed complex task now an ikebana arrangement for a neighbour's memorial instead of mending a dress. No clinical content changed.
- Flagged finding settled (hip flexors 4+/5, reflexes 1+ with trace ankle jerks, BMI 19.8): no change. Symmetric mild proximal weakness with reduced bulk and low weight, without sensory signs, at 79 with reduced ankle reflexes (common after 75) and normal B12, homocysteine, TSH and electrolytes, is consistent with sarcopenia; the nutrition and activity must already addresses it.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.
