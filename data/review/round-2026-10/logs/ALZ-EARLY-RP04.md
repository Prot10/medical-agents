# ALZ-EARLY-RP04
Reviewer status: R1 not reviewed, R2 not reviewed (no entry in notes/ALZ-EARLY.md) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note names this case. Condition classes C2.3, C2.6, C3, C5, C6, C7, C8, C10, C11, C12, C13, C16 of plans/ALZ-EARLY.md applied (see below). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.differential[sCJD] | sCJD left `high` although the work-up excludes it (C11). Autoimmune and paraneoplastic encephalopathy `moderate` despite acellular CSF, no seizures, normal sodium, no MRI signal change and an Alzheimer CSF profile. | FIXED: sCJD low with the excluding data; autoimmune and paraneoplastic low (antibody testing reserved for continued rapid decline, now a must); depression added very low (flat, withdrawn, GDS 5/15); FTD and vascular key features updated. |
| D/C | major | ground_truth.key_clinical_evidence | "Positive amyloid PET ... closes the differential": the pathway contains no amyloid PET criterion (C2.6); six items (C10). | FIXED: four items (rpAD pearl, absent CJD hallmarks, CSF profile with non-specific total tau, amnestic/MRI signature). |
| A | major | fallback_tool_outputs.advanced_imaging; .drug_interactions; .literature_search; metadata.fallback_tool_kinds | DaTscan report answering every advanced-imaging modality; drug check with "(agent not specified on this case's pathway)" engineering text; generic literature fallback (C2.3, 3.2, C8). | FIXED: all three null; kinds entries removed. |
| A | major | action-10; followup_outputs (literature) | Literature criterion and follow-up (C8). | FIXED: deleted. metadata.citation_gap (which referred to that literature) emptied. |
| B/D | minor | followup_outputs[CSF] | Cytology and oligoclonal bands not ordered (C6); analyte keys outside the vocabulary; interpretation listed every value. | FIXED: special_tests now Abeta42, Abeta40, Abeta42_40_ratio, phospho_tau, total_tau, 14_3_3_protein, RT_QuIC (values unchanged); interpretation pattern-level, with the RT-QuIC sensitivity caveat. Red herring field_path updated to the new key and position. |
| C | major | initial_tool_outputs.labs; new action-11-interpret-labs-mma; followup_outputs | B12 298 pg/mL (low-normal) on 9 years of metformin with reduced great-toe vibration, without MMA (C7.2). | FIXED: recommended MMA criterion after the labs criterion; follow-up MMA 0.24 umol/L, normal (homocysteine normal, so a raised MMA would not fit). |
| D/C | minor | initial_tool_outputs.labs.interpretation | "Consistent with suboptimally controlled type 2 diabetes": interpretive, and wrong for an older adult with dementia, whose HbA1c target is below about 8.0%. Homocysteine 10.2 identical to other cases. | FIXED: plain recital; homocysteine 11.6. |
| B/C | major | initial_tool_outputs.clinical_assessment | Template impression with engineering sentences; findings were fragments split mid-sentence; prion-relevant signs absent (C3). | FIXED: findings with MMSE and MoCA breakdown, prion-relevant negatives, informant tempo and IADL; impression per the skeleton, staged as dementia of moderate severity with a rapid course. |
| B | minor | followup_outputs[neuropsych] | Recognition discrimination 0.2 called "below chance"; impression called it "severe amnestic dementia" while the patient walks, is continent and needs help only with complex tasks. | FIXED: "near chance"; "amnestic multi-domain dementia of moderate severity". |
| B | minor | initial_tool_outputs.mri.additional_observations | Post-gadolinium and leptomeningeal statements with contrast false (C5). | FIXED: removed; added the CJD-relevant FLAIR negative. |
| A | minor | sequence_constraints; stop_rule | Clinical-before-biomarker constraint missing; max 0 (C16). | FIXED: added; max 1. |
| E | minor | all criteria; EEG citation | Rationale equal to label; duplicated citations; `[CJD_criteria_2017]` not the plan's key. | FIXED: rationales rewritten; `[CJD_2021]` (Hermann 2021) on MRI, CSF and EEG. |
| C | major | assessment.required_recommendations | Musts restated the MRI, CSF and lab criteria and one was a prohibition; no treatment, no follow-up plan for a rapid course, no diabetes target (C12). | FIXED: informant (prion-sign questions), early review with repeat DWI and neural antibodies if the tempo continues, AChEI must (memantine add-on if moderate), diabetes must (HbA1c below about 8.0%, avoid hypoglycaemia, B12 on metformin), safety, disclosure and advance care planning. |
| C | minor | assessment.prohibited_recommendations | Generic anticholinergic and benzodiazepine items; diabetes item called the diabetes "suboptimally controlled". | FIXED: CJD-from-tempo and stop-the-work-up prohibitions kept; antimuscarinic prohibition tied to his BPH (tamsulosin is not anticholinergic); diabetes prohibition reworded. |
| A/B | minor | followup_outputs (new amyloid PET) | An amyloid PET ordered as one extra step would have been answered by the library default, "Amyloid-negative", contradicting the case. | FIXED: case-authored positive florbetaben PET follow-up (SUVR 1.68, Centiloid about 88) with no criterion. Plan C2.1 keeps CSF as the single required route here; this only prevents a contradictory answer. |
| - | check | 3.6 check | perfect_agent -v ok: each criterion receives its report (neuropsych, MMA, CSF follow-ups; labs, MRI, EEG initial). Probe: amyloid PET -> case follow-up; FDG-PET -> library (normal), see Open questions. | OK |

## Changes, in one paragraph a physician can read before re-reviewing
Rapidly progressive Alzheimer disease in a 68-year-old man referred to exclude CJD (label and G30.1 unchanged). CJD is now `low` in the differential, as are autoimmune and paraneoplastic encephalopathy, because DWI, EEG, CSF RT-QuIC and 14-3-3 and the acellular CSF exclude them. The key evidence no longer cites an amyloid PET the pathway never performs. Methylmalonic acid is now a recommended step for B12 298 pg/mL on long-term metformin (result normal). The CSF report has lost cytology and oligoclonal bands, and the DaTscan, drug-check and literature fallbacks and the literature step are gone. The clinical assessment now documents the tempo and the absent prion signs. The musts now include treatment, an early review with repeat DWI and antibody testing if decline continues, a diabetes target suited to dementia (HbA1c below about 8.0%), safety and advance planning. A positive amyloid PET follow-up was authored so that an extra PET order does not return a contradictory negative.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys: `[CJD_2021]`, `[BSH_B12_2014]`, `[NICE_NG97]` (plan section 5.2); `[ADA_older_adults_2024]` = American Diabetes Association, Standards of Care in Diabetes 2024, section 13 Older Adults, Diabetes Care 2024;47(Suppl 1):S244-S257.
- Synonyms: this amnestic late-onset case accepts "posterior cortical atrophy", "benson syndrome" and "early onset alzheimer" through the G30.0 code (plan section 5.1).
- Library (plan Q4): FDG-PET ordered here returns the library's normal study; an FDG-PET in rpAD would normally show temporoparietal hypometabolism.

## Open questions for Andrea (judgment calls you could not settle)
- None needing Andrea. The FDG-PET library answer is covered by the plan's Q4 and CENTRAL item 4.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the full diff and the whole final case. No reviewer note names this case.
- Confirmed: sCJD, autoimmune and paraneoplastic entries low with excluding data that the case returns (DWI, EEG without PSWCs, RT-QuIC and 14-3-3 negative, acellular CSF); key evidence no longer cites an amyloid PET; CSF keeps 14-3-3 and RT-QuIC (plan C6.2), CSF stays required and single-alternative (plan C2.1); MMA criterion recommended, after labs, result normal and consistent with normal homocysteine; red herring field path followup_outputs[2] points to the CSF follow-up; fallbacks for advanced imaging, drug check and literature null; diabetes must target (HbA1c below about 8.0%) matches ADA for older adults with dementia.
- Found and fixed:
  1. (dim B, major) MMSE arithmetic: the breakdown (orientation 4, recall 3, serial sevens 2, repetition 1, writing 1) sums to 11 lost points, i.e. 19/30, not the 18/30 used throughout, and "cannot continue past first subtraction" would lose 4 serial-sevens points, not 2. Pre-existing in the exam and copied by the worker into clinical_assessment.findings[1]. Now serial sevens lose 3 ("stops after two correct subtractions"), which makes the breakdown sum to 18/30 (patient.neurological_exam.mental_status, clinical_assessment.findings[1]).
  2. (dim B, minor) CSF glucose ratio 64/122 is 0.52, not 0.53 (glucose_ratio and interpretation of the CSF follow-up).
  3. (dim C, minor) The cholinesterase-inhibitor must said "memantine can be added if the disease is moderate" while the case itself stages the dementia as moderate (MMSE 18): now "because the dementia is already of moderate severity (MMSE 18/30), consider adding memantine [NICE_NG97]".
- Not changed: an FDG-PET order still gets the library's normal study (plan Q4, already in CENTRAL).
- perfect_agent.py -v and case_io.py check clean after the edits.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (the labs criterion label), the wording the other six cases already use.
- citation key [ADA_older_adults_2024] harmonised to [ADA_older_adults_2025] as in M05 (1 place); the text (HbA1c target below about 8.0% avoiding hypoglycaemia) matches the 2025 Older Adults section.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- Normal values in `Magnesium_homocysteine_ESR_CRP` varied (ESR 12 to 8, CRP 1.8 to 1.1), all still within the case's reference ranges: the same numbers (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8) had been copied into up to 13 cases, a template artefact raised by the S01 worker; no text cites the changed values.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.
