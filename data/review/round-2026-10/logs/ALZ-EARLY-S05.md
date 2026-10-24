# ALZ-EARLY-S05
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The case has no reviewer notes. The condition-plan classes C1 to C16 were applied as a class (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | staging (C4) | Checked: his wife manages his medication schedule and appointments and supervises the kitchen after a stove incident; IADL field true is consistent; mild dementia, onset about 74, G30.1 correct. | No change to label, ICD or field. |
| B | major | patient.neurological_exam.mental_status, initial_tool_outputs.clinical_assessment.findings | MMSE item list did not add up (3+2+1+1+1 = 8 points lost gives 22/30, not 21/30) and counted "clock drawing", which is not an MMSE item. | FIXED: items now recall 3, orientation 2, serial sevens 1, sentence 1, pentagons 1, three-stage command 1 (= 21/30, consistent with his documented difficulty with three-step commands); clock drawing reported separately. Same in the assessment findings. |
| B | major | initial_tool_outputs.clinical_assessment.criteria_met.delayed_recall_improves_with_cueing | True while the exam records "no improvement with categorical cues" (plan survey, C3). | FIXED: false. |
| D | major | initial_tool_outputs.clinical_assessment.impression, .findings, .scores | Template impression ("partial benefit from cueing recorded", engineering sentence); fragment rows; stove, medicines and driving missing. | FIXED: impression and rows rebuilt from the case. |
| E | minor | patient.neurological_exam.additional | "No anosmia formally tested" (garbled). | FIXED: "Smell not formally tested." |
| D | minor | initial_tool_outputs.labs.abnormal_values_summary, .interpretation | Interpretive text ("consistent with known Type 2 diabetes", "suboptimally controlled diabetes"); HbA1c 7.1% is within the usual target for an older adult with cognitive impairment. | FIXED: factual values only. |
| B | minor | initial_tool_outputs.labs.panels.CBC, Reviewed_cognitive_panel_additions | MCV 88.4 vs Hct/RBC 90.8; template reviewed-panel values. | FIXED: MCV 90.8; magnesium 1.9, homocysteine 11.4, ESR 14, CRP 2.3. |
| C | major | action_criteria, followup_outputs (C7.2) | B12 268 pg/mL (low-normal) after 14 years of metformin, with reduced vibration at the toes, and no MMA. | FIXED: criterion `action-11-interpret-labs-mma` (recommended, after labs), follow-up `request_methylmalonic_acid` (0.27 umol/L, normal). |
| D | minor | initial_tool_outputs.mri.additional_observations | "No mass lesions or abnormal enhancement", "No abnormal meningeal enhancement" with contrast false; "Patent major intracranial vessels on MRA" (not acquired). | FIXED: removed; impression otherwise kept (Kind 2). |
| B | minor | followup_outputs[CSF] (C6) | 14-3-3 and RT-QuIC; non-vocabulary keys with em dashes. | FIXED: removed, vocabulary keys, pattern interpretation; values unchanged (ratio 0.58 verified). |
| C | major | action-8-analyze-csf (C2) | Single route; PET would have returned a negative library PET. | FIXED: CSF or amyloid PET alternatives, plan text; follow-up `order_amyloid_pet` (florbetapir, positive, centiloid 66). Probe: alt1 <- `request_csf_biomarkers`, alt2 <- `order_amyloid_pet`. |
| C | major | fallback_tool_outputs.advanced_imaging (C2.3) | A DaTscan report as the fallback answered every advanced-imaging modality (amyloid PET, FDG, tau PET) with a DaTscan, and its impression argued the differential ("arguing against dementia with Lewy bodies"). | FIXED: null. DaTscan (an avoided action) is now answered by the library's normal DaTscan; verified. |
| C | minor | followup_outputs (plan Q4) | FDG-PET would have returned the library's normal study. | FIXED: concordant `order_fdg_pet` follow-up, no criterion. |
| C | major | action-9-search-medical-literature, followup `search_alzheimer_biomarker_literature`, key_clinical_evidence[5] (C8, ruling 5) | Literature search as a recommended clinical step; its output restated the case's integrated conclusion ("Combined A+T+ ... fulfills criteria for early-stage Alzheimer's disease"); a key-evidence item about the search. | FIXED: criterion, follow-up and key-evidence item deleted. |
| B | major | followup_outputs[drug check], action-10 (C1.2) | Criterion matched any drug. | FIXED: optional, `{"drug": "donepezil"}`, last; output rewritten with HR 74 and the case's medicines (tamsulosin, atorvastatin, lisinopril, metformin), urinary outflow caution with BPH. Leak guard passes. |
| C | major | ground_truth.differential (C11) | DLB moderate although the entry itself says no such features are present; entries cited positive amyloid biomarkers that only an optional test returns. | FIXED: DLB low; all entries cite what the case shows; reversible causes include the MMA. |
| C | major | ground_truth.key_clinical_evidence (C10) | Six items, including engineering wording ("case-designated CSF A+T+ profile; amyloid PET is not duplicated"), the literature item, and a race item with inverted wording ("should not lower the threshold"). | FIXED: four items true for this case (NIA-AA clinical criteria, storage-type deficit, MTA 2 not normal aging, diabetes does not explain the syndrome). Race point kept in metadata with corrected wording ("should not be delayed because of race"). |
| C | major | ground_truth.assessment (C12) | Musts restating tool steps and the engineering biomarker must; generic prohibitions (anticholinergics, benzodiazepines, antipsychotics). | FIXED: musts are informant (he minimizes), specific safety (stove, medicines, finances, driving), disclosure, AChEI trial with tamsulosin and urinary counseling [NICE_NG97], simplified diabetes management with an HbA1c target below 8.0% avoiding hypoglycemia, biomarker offer. Prohibitions kept: diabetes attribution, MTA 2 as aging, memantine at the mild stage. |
| B | minor | red_herrings[0] | `location` cited a `differential_by_imaging` field the MRI does not have; interpretation relied on A+T+ biomarkers from an optional test. | FIXED: location "MRI findings and impression"; interpretation rests on the cognitive profile. |
| A | minor | citations and rationales (C13); sequence, stop rule (C16) | Duplicates; rationale copied from label; max_additional_actions 0. | FIXED; clinical assessment before biomarker added; MRI before CSF kept; max_additional_actions 1. |
| E | minor | avoided_actions rationales, metadata | Generic rationales; metadata single-route point. | FIXED. Other fallbacks (Holter, CT, ECG, echo with mild LA enlargement, EEG) read: case-consistent, kept. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis and staging are unchanged (mild Alzheimer dementia, amnestic, G30.1). The MMSE breakdown in the exam now adds up to 21/30 with real MMSE items, and the bedside assessment records that cues did not help recall. The laboratory report states values only; his low-normal B12 of 268 pg/mL on long-term metformin is followed by a recommended methylmalonic acid, which is normal. The MRI no longer mentions enhancement or MRA. The literature search step, which repeated the case's conclusion, was removed, as was a DaTscan fallback that answered every advanced-imaging order. Amyloid status is optional by CSF or a new concordant positive amyloid PET, with a concordant FDG-PET if ordered. DLB is now low. Musts now include specific safety measures, a cholinesterase-inhibitor trial with tamsulosin and urinary counseling, and simplified diabetes management avoiding hypoglycemia.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms: PCA, Benson and early-onset labels and G30.0 in a late-onset amnestic case (plan 5.1).
- Citation keys `[NICE_NG97]`, `[BSH_B12_2014]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Checked against the plan (C1 to C16, sections 3.1 to 3.6) and PATTERNS.md: log claims against the file, criterion order and tiers, the biomarker criterion's two alternatives each answered by a case-authored follow-up (CSF and amyloid PET, plus a concordant FDG-PET), fallbacks (advanced_imaging, literature and drug_interactions null where required; the remaining Holter, CT, ECG, echo and EEG fallbacks read), CSF arithmetic (Abeta42/40 ratio, CSF/serum glucose ratio), CBC indices, musts and prohibitions against allergies, medicines and avoided actions, the differential against the final evidence, and leakage of expected evidence into any-query outputs (test_case_guards passes).
Found: nothing that needed a change. Checked: the MMSE item list now adds up (3+2+1+1+1+1 = 9, 21/30); cueing field false; MMA recommended and normal for B12 268 on metformin; the DaTscan fallback is gone and the DaTscan avoided action is restricted to modality DaTscan, so it cannot match the amyloid PET or FDG orders; the CSF ratio 372/7900 = 0.047; HbA1c target below 8.0% matches ADA guidance for older adults with cognitive impairment; donepezil and bladder outflow obstruction is a labelled warning; red herring field path points to the MTA finding. Residual, metadata only (not shown to the agent): key_educational_points still describe an "A+T+ CSF profile" and "positive biomarkers", which only the optional biomarker step returns; left as is. The CSF paired serum glucose (118) equals this case's panel glucose, so it was kept here and changed in S02, S03 and S04.
perfect_agent.py -v and case_io.py check: clean.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; "early onset alzheimer" and code G30.0 (onset at 65 or later); code G30.8 (atypical presentations only). Added "late onset alzheimer". Now: codes ['G30.1', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'late onset alzheimer'].
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
