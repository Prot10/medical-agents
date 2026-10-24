# ALZ-EARLY-S06
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The case has no reviewer notes. The condition-plan classes C1 to C16 were applied as a class (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | patient.history_present_illness (C4) | MCI staging held (she manages finances, medicines, cooking and driving) but the HPI did not say whether the lapses had consequences or whether anyone had taken over (plan: make MCI unambiguous per 1.2). | FIXED: one sentence added: lapses without lasting consequences, compensated by her calendar and lists, no task taken over or supervised. Label (MCI due to AD, amnestic) and G31.84 unchanged. |
| B | minor | patient.neurological_exam.mental_status | MMSE recall "2/3 with one recalled only after categorical cueing" (cued words do not score, so that would be 1/3 and MMSE 27); MoCA "clock copy" (the MoCA has a clock drawing and a cube copy) contradicted "Clock drawing is correct". | FIXED: "2/3 recalled freely; the third not retrieved with a categorical cue"; "mild imprecision on the cube copy and a trail-making error". "Anosmia not formally tested" changed to "Smell not formally tested". |
| B | major | initial_tool_outputs.clinical_assessment.findings, .impression, .scores | The only "informant history" row was the PCP referral sentence; no functional rows; template impression with both engineering sentences ("the threshold is functional...", "This assessment is the step..."). | FIXED: rows and impression rebuilt from the case (MMSE and MoCA breakdown, cue result, husband's report, preserved IADLs with self-compensation); structured fields unchanged and consistent (cueing false, IADL lost false). |
| D | minor | initial_tool_outputs.labs.interpretation | Interpretive text ("consistent with known type 2 diabetes, HbA1c above the diabetic control target"). | FIXED: values only. Reviewed-panel template values replaced (magnesium 2.1, homocysteine 8.7, ESR 16 with reference 0-30, CRP 1.1). B12 348 pg/mL normal: no MMA. |
| D | minor | initial_tool_outputs.mri.additional_observations | MRA and "No abnormal meningeal enhancement" lines with contrast false (C5). | FIXED: removed. |
| C | minor | followup_outputs[neuropsych].impression (C15 class from M03) | Spanish-dominant bilingual patient; the report did not say in which language or with which norms she was tested; "storage-type encoding deficit" (contradictory); em dash. | FIXED: testing in Spanish with norms for age, education and language background; "storage-type deficit with poor benefit from recognition cues"; MCI conclusion kept. |
| B | minor | followup_outputs[CSF] (C6) | 14-3-3 and RT-QuIC in a non-rapid case; non-vocabulary keys; em dash. | FIXED: removed; vocabulary keys; total tau "Normal (upper limit)"; pattern interpretation; values unchanged (ratio 438/8200 = 0.053 verified). |
| C | major | action-8-analyze-csf (C2) | Single route; PET would have returned the library's negative PET. | FIXED: CSF or amyloid PET alternatives; follow-up `order_amyloid_pet` (florbetaben, positive, centiloid 41, concordant with a moderately reduced ratio). Probe: alt1 <- `request_csf_biomarkers`, alt2 <- `order_amyloid_pet`. |
| C | minor | followup_outputs (plan Q4) | FDG-PET would have returned the library's normal study. | FIXED: concordant `order_fdg_pet` follow-up (mild posterior cingulate and inferior parietal hypometabolism), no criterion. |
| C | major | action-10-check-drug-interactions, followup `check_drug_interactions_donepezil` (C1.1) | Donepezil interaction check in an MCI case; the output also routed donepezil through CYP2C19 (omeprazole), which is wrong (CYP2D6 and CYP3A4). | FIXED: criterion and follow-up deleted; initial and fallback drug_interactions null; MCI prohibition, MCI must and MCI key evidence added. Previous prohibition "memantine at the MCI stage" merged into the MCI prohibition. A donepezil order is now answered by the library's neutral report. |
| C | major | action-9-search-medical-literature, followup `search_mci_alzheimers_screening_instruments`, fallback literature (C8, ruling 5) | Literature search recommended as a clinical step; output carried case-conclusion statements. | FIXED: criterion, follow-up and fallback deleted (null). |
| C | major | ground_truth.differential (C11) | Medication-effect entry cited "biomarker positivity" from an optional test; em dash; mild dementia (the staging alternative the functional history must exclude) absent. | FIXED: entries cite only what the case shows; "Mild dementia due to Alzheimer disease (staging alternative)" added as low with the reason (preserved IADLs). |
| C | major | ground_truth.key_clinical_evidence (C10, C1) | Six items, including the engineering item ("case-designated optional CSF ... amyloid PET is not duplicated"). | FIXED: four items (MMSE ceiling and MoCA, neuropsych pattern, canonical MCI treatment fact, bilingual testing). |
| C | major | ground_truth.assessment (C12, C1) | Musts restating tool steps (labs, MRI, neuropsych, "administer the MoCA"), engineering biomarker must; generic prohibitions (anticholinergics, benzodiazepines, antipsychotics). | FIXED: musts are informant, canonical MCI reassessment and exercise (noting she stopped her exercise class), vascular risk management, disclosure and planning, safety review, biomarker offer. Prohibitions: normal-MMSE dismissal, canonical MCI drug prohibition. |
| B | minor | red_herrings[0] | Em dashes in data_point and location. | FIXED: wording kept, dashes removed. Field path followup_outputs[0] still points to the neuropsych report. |
| A | minor | citations and rationales (C13); sequence, stop rule (C16) | Duplicates; rationale copied from label; max_additional_actions 0. | FIXED; clinical assessment before biomarker added; MRI before CSF kept; max_additional_actions 1. |
| E | minor | avoided_actions rationales, metadata | Generic rationales; metadata single-route point. | FIXED; ECG rationale notes no cholinesterase inhibitor is planned. Fallbacks (Holter, CT, ECG, echo, EEG) normal and consistent, kept. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis unchanged (MCI due to Alzheimer disease, amnestic, G31.84), with the functional staging now explicit: she manages finances, medicines, cooking and driving and compensates isolated lapses herself. Two exam details were corrected (MMSE recall scoring and the MoCA cube copy). The bedside assessment now records her own results and her husband's account, and the neuropsychology report states she was tested in Spanish with appropriate norms. The donepezil interaction check (which also had wrong CYP2C19 pharmacology) and the literature search were removed, as no medicine is started for MCI; a prohibition on routine cholinesterase inhibitors or memantine in MCI and a must for reassessment in 6 to 12 months with exercise were added. Amyloid status is optional by CSF (14-3-3 and RT-QuIC removed) or a new concordant positive amyloid PET, with a concordant FDG-PET if ordered. The MRI no longer mentions MRA or enhancement.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms: this MCI case accepts dementia labels ("alzheimer dementia", "dementia due to alzheimer") and G30.x codes, plus PCA, Benson and early-onset labels (plan 5.1: do not cross MCI and dementia labels).
- Library drug-check default answers "no interaction" for any drug (plan 5.5); harmless here.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Checked against the plan (C1 to C16, sections 3.1 to 3.6) and PATTERNS.md: log claims against the file, criterion order and tiers, the biomarker criterion's two alternatives each answered by a case-authored follow-up (CSF and amyloid PET, plus a concordant FDG-PET), fallbacks (advanced_imaging, literature and drug_interactions null where required; the remaining Holter, CT, ECG, echo and EEG fallbacks read), CSF arithmetic (Abeta42/40 ratio, CSF/serum glucose ratio), CBC indices, musts and prohibitions against allergies, medicines and avoided actions, the differential against the final evidence, and leakage of expected evidence into any-query outputs (test_case_guards passes).
Found and fixed:
- patient.neurological_exam.mental_status and clinical_assessment.findings[2]: the MoCA lists verbal fluency of 11 words as a deficit, but the MoCA gives the fluency point for 11 or more words, and with that point the listed losses (delayed recall 4, visuospatial/executive 2, naming 1, date 1) give 22/30, not 21/30. Fluency set to 10 words in both places, which makes the deficit real and the total 21/30.
Checked and correct: MCI staging per plan 1.2 (finances, medicines, cooking and driving kept, lapses self-compensated, nothing taken over), cueing and IADL fields false; drug check, literature and their fallbacks removed with the canonical MCI prohibition, must and key evidence; ratio 438/8200 = 0.053; amyloid PET centiloid 41 concordant with a moderately reduced ratio; MMSE 28/30 arithmetic; red herring path points to the MMSE row.
perfect_agent.py -v and case_io.py check: clean after the edits.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`apply_diagnosis_synonyms.py --prune --conditions alzheimers_early`): MCI labels only. Removed "alzheimer disease", "alzheimer's disease", "alzheimers disease", "alzheimer dementia", "dementia due to alzheimer", "posterior cortical atrophy", "benson syndrome", "early onset alzheimer" and the codes G30.0, G30.1, G30.8, G30.9, F00, because every "dementia due to Alzheimer disease" answer contains those tokens and would have scored an overcall of this MCI case as correct.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
