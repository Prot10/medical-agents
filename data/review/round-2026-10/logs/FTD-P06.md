# FTD-P06
Reviewer status: R1 not reviewed (no FTD notes file), R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | `data/review/round-2026-10/notes/` holds no FTD file; every change below is a lead-plan (`plans/FTD.md`) or own finding |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations` | Plan P06/C9: "Definitively exclude AD with amyloid PET" (an optional test, and amyloid PET cannot exclude AD-FTLD overlap definitively); template duplicates; "Optimise vascular risk factors" and "Address judicial capacity formally" not checkable | FIXED: five musts (Rascovsky certainty; why AD and small-vessel disease do not explain it, SVD coexists; vascular risk treatment with individualised HbA1c about 7-8%, BP <130/80, statin indicated in diabetes at 63; safety and capacity incl. finances, medicines and fiduciary roles; caregiver plan without ChEI/memantine). Genetic-counselling template must deleted: no familial FTD indication and no genetics criterion |
| A/C | major | `initial_tool_outputs.labs` | Plan C5: an APOE genotype reported inside the blood panel (unrequested, non-diagnostic); "Reviewed_FTD_panel_additions"; copper/ceruloplasmin and RPR/HIV unrequested; LDL in the baseline; free T4 with a normal TSH; no folate, platelets, calcium, LFTs | FIXED: standard panels; HbA1c 8.2% kept with a fasting glucose of 156 mg/dL consistent with it; APOE, copper, ceruloplasmin and free T4 deleted; lipids (LDL 142 kept) and RPR/HIV moved to keyed follow-ups |
| B | minor | `patient.history_present_illness` | The APOE e4 trap (notes, differential, musts) then rested on a lab row the agent should not receive | FIXED: one APOE e4 allele now stated as a direct-to-consumer result from 3 years ago (prior history, not scored); declared as a red herring |
| D | major | `patient.history_present_illness` | Narrator steering: "both vascular risk factors that could contribute to white matter disease" and the closing sentence listing the features and red herrings; "(HbA1c on recent check)" incomplete | FIXED: removed; added never on a statin and NPH negatives (no gait change, falls or incontinence) |
| B | minor | `patient.neurological_exam.cranial_nerves`, `.additional` | Plan C14: "No primitive reflexes" while palmomental reflexes are present; `additional` restated the history ("indicating that behavioral changes had been causing professional impairment") | FIXED: cranial nerves "Normal."; `additional` holds the palmomental reflexes and a normal gait description |
| B | major | `initial_tool_outputs.clinical_assessment` | Plan C3: the empathy and perseveration findings were the HPI summary sentence; duplicated MoCA; template impression; apathy false although she "has lost interest in her family's activities" | FIXED: one finding per feature, 5 present (apathy now true), hyperorality absent; informant, screen, functional decline; canonical impression |
| D | minor | `initial_tool_outputs.mri` | "Posterior cortex preserved, inconsistent with typical AD predominance" (diagnostic reasoning in a report); "from vascular risk factors" (clinical attribution); no statement on infarcts, microbleeds or ventricles although vascular dementia and NPH are in the differential | FIXED: observations state preserved parietal and posterior cingulate cortex, proportionate ventricles, no infarcts or microbleeds; numbered impression |
| D | minor | `followup_outputs[request_reviewed_neuropsych_battery]` | Plan C13: P04's template text word for word; MoCA in the battery; "argues against a PPA variant"; recommended FDG-PET | FIXED: case-specific scores (TMT-B, WCST, FAS, Ekman 60, RAVLT with normal recognition, ROCF, JLO, BNT, SDMT), canonical ending, `recommended_actions` emptied |
| C | major | `followup_outputs` (`vascular_contribution_quantification`, `judicial_professional_ethical_disclosure`, `diabetes_optimization_cognitive_benefit`) | Plan C1/C2: empty literature follow-up, a judicial-ethics management essay, and a drug check with a plan in `proposed`, sulfonylurea and SSRI-levothyroxine warnings for drugs nobody proposed | FIXED: all three deleted |
| D | major | `ground_truth.action_criteria[action-10-search-medical-literature]`, `initial_tool_outputs.literature_search` | Plan C1: literature required, in the stop rule, no initial output (answered by an empty follow-up) | FIXED: canonical AD-versus-FTD text authored; criterion optional, last, `{}`, out of the stop rule |
| C | minor | `ground_truth.action_criteria[action-8-order-advanced-imaging]`, `[action-9-order-advanced-imaging]`, `followup_outputs` | Plan C6: no SPECT alternative; no CSF alternative for the AD question; FDG reported "patchy periventricular white matter hypometabolism" (not an FDG-PET reading) | FIXED: SPECT and CSF AD-marker alternatives with authored follow-ups (both concordant with FDG and amyloid PET); FDG white-matter line replaced by a medial temporal line; amyloid threshold stated |
| B | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, `.specialized_test` | Plan C6 | FIXED: CT shows bifrontal atrophy and white matter hypodensities (kind `case`); the other two deleted |
| C | major | `ground_truth.differential` | Plan C11: AD and vascular cognitive impairment both high; "resolved by negative amyloid PET" (optional result); familial FTD moderate without a family history of FTD | FIXED: AD low, VCI as sole cause low (SVD coexists), mixed pathology low, NPH very low |
| D | major | `ground_truth.key_clinical_evidence` | Plan C12: "Negative amyloid PET securely excludes AD"; tier line; capacity line (a must, not evidence) | FIXED: four lines in C12 wording |
| C | minor | `ground_truth.red_herrings` | Red-herring interpretation made amyloid PET "the discriminator" | FIXED: reworded; APOE e4 and Fazekas 2 red herrings added |
| C | minor | `ground_truth.action_criteria[*]`, `avoided_actions` | Plan C4; carotid duplex rationale | FIXED: canonical labels, case rationales and evidence; avoided CT cites `[NICE_NG97]`; carotid duplex rationale notes small-vessel disease without infarct or TIA |
| E | minor | `metadata.notes`, `difficulty_rationale`, `key_educational_points` | "definitively excludes AD"; "single most discriminating" | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The diagnostic puzzle is kept but each trap now sits where it belongs: the mother's AD in the family history, one APOE e4 allele as an old direct-to-consumer result in the HPI (no longer a lab row), and Fazekas 2 white matter disease on the MRI, which now also states no infarcts, no microbleeds and proportionate ventricles. The informant assessment counts 5 Rascovsky features (apathy added from the history), the neuropsychological battery has its own scores showing a retrieval pattern with normal recognition, and the labs are the standard panels with HbA1c 8.2% and a matching fasting glucose. Optional FDG-PET (or SPECT) and an optional AD biomarker (amyloid PET or CSF, both negative) remain; the three management and ethics follow-ups are gone and literature is optional and last. The musts no longer demand amyloid PET; they ask for the certainty level, the reasons AD and small-vessel disease do not explain the syndrome, treatment of her vascular risk factors (HbA1c target about 7-8% in cognitive impairment, BP below 130/80, a statin, which she has never taken), safety and capacity, and caregiver support. AD, vascular cognitive impairment and mixed pathology are low in the differential, NPH very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used that the criteria pack does not list: `[SNLG_ISS_2024]`, `[Frisoni_2024]`, `[NICE_NG97]`, `[Amyloid_PET_AUC_2025]` (plan section 5 item 2). The vascular-risk must follows the ADA Standards of Care (older adults with cognitive impairment, statin in diabetes aged 40-75) and the 2017 ACC/AHA blood pressure target; no key exists for these and musts carry no citation field.

## Open questions for Andrea (judgment calls you could not settle)
- None needing information only Andrea has. Decided here: the APOE result moved into the history as a prior direct-to-consumer test so that the intended trap survives without a non-indicated genotype in the blood panel; the vascular-risk must was added because the label includes concurrent small-vessel disease and she has uncontrolled diabetes, BP above target and no statin.

## Verification
Adversarial verifier, 24 Oct 2026. There is no FTD notes file. I read the log, the diff and the whole final case.
- Confirmed:
  - The APOE result is moved into the prior history and declared as a red herring.
  - The vascular must is correct: ADA, older adults with cognitive impairment, HbA1c below 8.0%; statin indicated in diabetes at 40 to 75; BP below 130/80. BP is 138/86 in the vitals, so above target.
  - HbA1c 8.2% sits with fasting glucose 156 mg/dL.
  - eGFR 62 matches CKD-EPI 2021 for a creatinine of 1.0 in a 63-year-old woman.
  - The sulfa allergy is not contradicted.
  - Amyloid and CSF are optional, authored and negative, and the KCE wording is conditional.
  - The genetic-counselling must is deleted, which is sound: there is no FTD family history and no genetics criterion.
  - The library's normal genetic panel is consistent with the case.
- Found and fixed (1, minor): the bedside-screen line "points lost on trail-making, letter fluency, attention and delayed recall" adds up to 6 points, not the 8 behind MoCA 22/30. It now reads "points lost include ...".
- Checks run after the changes: `perfect_agent.py -v` passes, `case_io.py check` names no failure for this case, `test_case_guards` (leak, followup, banned-string) passes. I also called the MockServer directly with FDG_PET, perfusion_SPECT, amyloid_PET, DaTscan, CSF AD markers, genetic_panel:FTD and genetic_panel:ALS, emg_ncs, respiratory_function, the neuropsych battery, targeted RPR/HIV, the baseline labs, CT and literature, to check that every plausible order gets a report consistent with the case.

## Condition audit (FTD auditor, 24 Oct 2026)

- D, major, `patient.neurological_exam.mental_status`: the examination gave the bedside screen results (MoCA 22/30 with item losses and letter fluency), which the required `perform_clinical_assessment` returns (ROUND_POLICY timeline-leak rule). The other 12 FTD cases, and VASC-DEM and ALZ-EARLY, had already moved them out. Removed the scores and test results; the behavioural observations, insight and frontal signs stay. The clinical assessment output already carries every removed value, so no information is lost. FIXED.
- B, minor, `fallback_tool_outputs.csf`: a case CSF fallback with empty `special_tests` answered any CSF order without a stored result (for example Abeta42, p-tau and t-tau), so the ordered assays were missing from the report. Deleted, together with `metadata.fallback_tool_kinds.csf`, as in M07, M09, M10, P01 and P02. The library now answers per assay; a probe returned normal AD markers. FIXED.
- C, minor, `ground_truth.sequence_constraints`: plan C15 asks for MRI before every CSF criterion, and it was missing for `action-9-order-advanced-imaging`. Added soft `action-7-analyze-brain-mri` -> `action-9-order-advanced-imaging`, cited `[NICE_NG97]`, with the M02/M04 reason (imaging excludes a mass lesion before lumbar puncture and characterises the atrophy before a biomarker is chosen). FIXED.
- E, minor, `initial_tool_outputs.literature_search[*].results[*].source`: the sources were citation keys (`[Rascovsky_2011]` or `Rascovsky_2011`), which a literature tool does not return, and the condition used three styles. They now give the full reference, as in M07-P02 (for example "Rascovsky K et al. Brain 2011;134:2456-2477 (FTDC criteria for bvFTD)"). Findings and summary are unchanged. FIXED.
- `perfect_agent.py` and `case_io.py check` were re-run on all 30 FTD cases after the changes and are clean; `test_case_guards.py -k FTD` passes (60 tests).

## Close-out (24 Oct 2026)

Decisions in `plans/FTD-decisions.md`. Changes:

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (the report is a transthoracic study). The MockServer routes echo reports by this field; without it the normal TTE fallback answered a TEE order too (PATTERNS section 5; FTD added to `DISCRIMINATOR_CONDITIONS`).
- Added optional criterion `action-genetic-panel-optional` (`order_specialized_test` `genetic_panel:FTD`, `[Pottier_2016]` `[Ducharme_2020]` `[ACMG_NSGC_2011]`), placed after imaging and before any drug check or literature step, a soft constraint clinical assessment before genetics, and a negative FTD panel follow-up (`request_optional_counselled_ftd_genetics`). Reason: sporadic bvFTD with young onset (before 65); the FTD consortium advises C9orf72 screening in every possible or probable bvFTD (Ducharme 2020), so a counselled panel is a defensible order that the stop rule should not penalise, while UK eligibility (onset before 55, a suggestive family history or MND; NHS GeneTYPES) is not met, so it is optional and no counselling must is added (FTD-decisions item 7). Onset about 61.
- Synonyms (`G31.09` entry, applied with `--prune --conditions ftd`): "pick disease" and "pick's disease" (retired) and the code G31.01 are no longer accepted. Pick disease is one FTLD-tau pathology that no case establishes, and G31.01 is where ICD-10-CM codes primary progressive aphasia, so a PPA answer coded G31.01 scored as correct here.

Checks: `perfect_agent.py` and `case_io.py check` clean; `test_case_guards.py -k FTD-` passes, including `test_routed_outputs_name_their_study`.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-10-search-medical-literature` label: "Literature on FTD versus AD and vascular contributors (optional)" -> "Literature on FTD versus AD and vascular contributors"

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech-language findings matching the stored neuropsychology (reduced verbal fluency; naming as tested).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status of the case's functional decline instead of Karnofsky 100.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k FTD` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
