# FTD-S03
Reviewer status: R1 not reviewed, R2 not reviewed (FTD has no notes file; R1's July 2026 tool rulings in `condition_tool_guidance.yaml` `ftd:` apply) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | FTD was never annotated; no note ids exist for this case. All changes below come from the condition plan (`plans/FTD.md`, classes C1-C15 and the S03 index entry) and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `action_criteria[action-8-search-medical-literature]`, `followup_outputs[request_literature_c9orf72]`, `initial_tool_outputs.literature_search` | C1 / ruling 5: literature `required` and in the stop rule; its query presumed the optional C9orf72 result; the only stored output was a prognosis and surveillance essay ("median survival 8-10 years", "annual neurological exam essential"). | FIXED: criterion `optional`, last, out of the stop rule, query "Familial behavioural variant FTD genetics and management"; follow-up deleted; canonical familial-variant literature output stored as the initial output, citations add `[Pottier_2016]`. |
| C | major | `initial_tool_outputs.clinical_assessment` | C3: HPI sentences filed under the wrong feature (the argument/motorcycle/food sentence as hyperorality), duplicated FAB line; loss of empathy (no remorse, amused when confronted) and stereotyped routines (same news programme at the same time, agitated if interrupted) marked false although documented. | FIXED: one finding per feature; empathy and perseverative/stereotyped true; apathy absent (not reported); count 5 of 6; informant, screen and functional-decline lines; canonical impression, first variant (memory and visuospatial relatively preserved). |
| B | minor | `patient.neurological_exam.mental_status` | MMSE 23/30 given without items, so the bedside memory and visuospatial sparing the assessment must score could not be read. | FIXED: items stated (serial sevens 1/5, recall 2/3, loses date and day, pentagons correct; 4+1+2 = 7 points). |
| C | minor | `patient.neurological_exam.motor`, `.gait`, `red_herrings[0]`, `key_clinical_evidence[2]` | C8: copied rigidity and a stooped, reduced-arm-swing gait in a phenotype the plan does not support. | FIXED: rigidity removed; motor "Normal bulk and tone. No fasciculations or wasting."; normal gait; red herring and KCE line deleted; DaTscan rationale case-specific. |
| C | minor | `ground_truth.red_herrings` | With the rigidity removed the case had no red herring; his treated OSA is a real distractor. | FIXED: OSA red herring with interpretation; matching differential entry (low). |
| B | major | `followup_outputs[request_reviewed_neuropsych_battery]` | Battery had no visuospatial or language domain although the criterion expects visuospatial sparing; FrSBe "severe apathy" contradicted a history with no apathy; impression truncated (C13). | FIXED: memory (mild, cue-responsive, normal recognition), Language and Visuospatial (normal) domains; FrSBe apathy scale not elevated; impression finished with the canonical ending. |
| D | minor | `followup_outputs[request_optional_counselled_ftd_genetics]` | Plan M02/C-genetics: template "Abnormal values: ... (H)" impression and "ABNORMAL -" result strings. | FIXED: report-style result (pathogenic C9orf72 expansion, approx. 600 repeats; GRN and MAPT negative; post-test counselling; 50% risk to first-degree relatives). |
| C | major | `ground_truth.assessment.required_recommendations` | C9: must "Given C9orf72 expansion, screen actively for ALS" presumed an optional result; two genetic-counselling musts; template block duplicated. | FIXED: six case-specific musts: Rascovsky with certainty level; why treated OSA or a psychiatric disorder does not explain it; safety and capacity (driving, the motorcycle purchase, safety-critical work, lasting power of attorney); caregiver plan avoiding ChEI/memantine; counselling before testing with predictive testing of the teenage children deferred to adulthood; follow-up for emerging motor neuron disease (familial FTD), without presuming the genetic result. |
| C | minor | `ground_truth.assessment.prohibited_recommendations[0,1]` | C10. | FIXED: canonical ChEI and memantine prohibitions. |
| C | major | `ground_truth.differential` | C11: AD and FTD-MND "moderate" (AD rebutted with an amyloid PET that does not exist; FTD-MND justified by the optional C9orf72 result); alcohol entry justified by a "construction-worker demographic" with 2-3 beers a weekend. | FIXED: AD low and FTD-MND low with reasons; alcohol entry removed; OSA entry added (low); psychiatric low; vascular very low (Fazekas 1). |
| C | major | `ground_truth.key_clinical_evidence` | C12: KCE cited the optional FDG pattern and the optional C9orf72 result. | FIXED: KCE from the required pathway and presentation (feature count, MRI, neuropsychology, C12 canonical AD line, pedigree). |
| B | minor | `initial_tool_outputs.labs` | C5: folate, K, urea, calcium, LFTs, albumin, MCV, eGFR missing; `Reviewed_FTD_panel_additions`; copper and heavy metals unrequested; RPR/HIV under "Vitamins". | FIXED: canonical panels, existing values kept; added K 4.3, BUN 16, eGFR 79 (CKD-EPI 2021, 55 M, creatinine 1.1), calcium 9.5, ALT 31, AST 26, ALP 70, bilirubin 0.8, albumin 4.4, MCV 89, folate 8.9; copper/heavy metals deleted; RPR/HIV in keyed follow-up. |
| D | minor | `initial_tool_outputs.mri` | No vascular negatives in a hypertensive former smoker; impression unpunctuated. | FIXED: Fazekas 1, no microbleeds, no DWI restriction, no mass/haemorrhage/hydrocephalus; numbered impression. |
| C | minor | `action_criteria[action-7-order-advanced-imaging]`, `followup_outputs` | C6: no SPECT alternative. | FIXED: `perfusion_SPECT` alternative and matching SPECT follow-up; FDG impression em dash removed. |
| B | minor | `fallback_tool_outputs.advanced_imaging`, `.drug_interactions`, `.ct`, `metadata.fallback_tool_kinds` | C6/C2: off-pathway advanced-imaging fallback; "agent not specified" drug fallback; normal CT in severe atrophy. | FIXED: both deleted (a drug check now gets the library answer; lisinopril has no interaction of consequence with an SSRI); CT fallback shows bifrontal and anterior temporal volume loss; kinds updated. |
| A | minor | all `action_criteria[*]` | C4: rationale = label; duplicate/free-text citations; `[AAN_dementia_2018]`. | FIXED: canonical labels, rationales, bracketed citations; genetics rationale names the pedigree. |
| B | minor | `action_criteria` order, `sequence_constraints`, `stop_rule` | Genetics sat before labs and MRI; no assessment-before-genetics constraint (C15). | FIXED: order assessment, neuropsych, labs, MRI, FDG, genetics, literature (ids unchanged); soft constraint assessment before genetics `[ACMG_NSGC_2011]`; stop rule = the four required ids. Follow-ups: neuropsych, serology, FDG, SPECT, genetics. |
| C | minor | `ground_truth.diagnosis.accepted[0]` | "probable, familial": with the optional C9orf72 result the diagnosis would be definite bvFTD (Rascovsky 2011). | FLAGGED, not changed (ruling 3): the required pathway supports probable; definite only if the agent chooses the optional test. Same question as plan Q1 (M06). |
| D | minor | `patient.neurological_exam.mental_status` | Exam carries the screen the assessment reports. | FLAGGED: kept per the plan's C3 design (condition-wide). |
| - | check | - | perfect_agent ok; probes: FDG, SPECT, serology, genetics and literature answered by the case; CT by the case fallback; drug check by the library. test_case_guards pass; `case_io.py check` names no S03 failure. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case remains probable familial bvFTD in a 55-year-old construction foreman (history from his wife; father with personality change in his early 50s, died at 62). The bedside assessment now counts the five features the history documents (disinhibition, loss of empathy, stereotyped routines, hyperorality and an executive-predominant screen; the MMSE items are now stated: recall 2/3 and a correct pentagon copy). The copied rigidity and stooped gait are gone; treated sleep apnoea is the case's distractor. Neuropsychology adds the visuospatial and recognition data and no longer reports an apathy the history lacks. Labs are the NICE NG97 set; syphilis and HIV serology answer a separate order. Genetics stays optional (C9orf72 expansion when ordered, now written as a laboratory report) and follows the clinical assessment. No must or key-evidence line presumes the genetic result any more; the musts add predictive testing of the teenage children deferred to adulthood and follow-up for emerging motor neuron disease. The literature search is optional, last and general; FDG-PET has an authored SPECT alternative; CT and drug-check fallbacks were corrected or removed; the differential is the assessment-time view.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[SNLG_ISS_2024]`, `[NICE_NG97]`, `[ACMG_NSGC_2011]` per plan 5.2.
- Label level of certainty (probable vs definite when the optional genetic test is positive): same decision as plan Q1; no change made.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Adversarial verifier, 24 Oct 2026.

- What I checked: Read the log, the field-level diff against HEAD (patient block in full, criteria re-order and arguments) and the whole final case. Checked every own-finding row against the file: labs rebuilt to the canonical panels with values and reference ranges consistent (eGFR recomputed with CKD-EPI 2021 and correct), no `Reviewed_FTD_panel_additions`, serology in its own keyed follow-up; clinical assessment one finding per Rascovsky feature with `criteria_met` and the feature count agreeing with the findings and the HPI/exam; MMSE item arithmetic where itemised; neuropsych impression complete with the canonical ending; FDG criterion with the perfusion_SPECT alternative and an authored SPECT follow-up matching the FDG pattern; advanced-imaging and agent-unspecified drug fallbacks gone; CT fallback with the atrophy; ChEI/memantine prohibitions canonical; literature criterion optional, last, out of the stop rule, output the canonical general text; stop rule = exactly the four required ids; KCE and musts do not presume an optional result; differential at assessment time; no amyloid claim. Reviewer notes: none exist for FTD, so no note id can be missing. Also: the itemised MMSE added to the exam sums correctly (4 serial sevens + 1 recall + 2 orientation = 7 lost, 23/30) and is consistent with the executive-with-sparing feature marked present; FrSBe apathy no longer contradicts the history; genetics report (C9orf72 approx. 600 repeats, GRN/MAPT negative) is report-style; no must or KCE presumes it; soft constraint assessment before genetics present with both ids existing; OSA red herring path correct.
- Found and changed:
  1. Scoring defect (introduced or kept by the worker): the optional literature criterion required the exact free-text `query`, and `_contains_required` matches strings exactly, so any real literature call was unmatched, counted as unjustified (tool accuracy, stopping with max_additional_actions 0) although the criterion intends it as optional. The other 24 FTD cases carry no query argument. FIXED: `query` removed from the literature criterion's `required_arguments` (the stored output is served for any query).
- Agreed FLAGGED item: the "probable" label with an optional positive C9orf72 result (plan Q1); not changed (ruling 3).
- After the edits: `perfect_agent.py -v` passes, `case_io.py check` names no failure for the case, `test_case_guards` passes; a literature call with an arbitrary query and a sertraline check with other arguments now match their optional criteria.

## Condition audit (FTD auditor, 24 Oct 2026)

- D, major, `patient.neurological_exam.mental_status`: the examination gave the bedside screen results (MMSE 23/30 with items, FAB 11/18 and category fluency), which the required `perform_clinical_assessment` returns (ROUND_POLICY timeline-leak rule). The other 12 FTD cases, and VASC-DEM and ALZ-EARLY, had already moved them out. Removed the scores and test results; the behavioural observations, insight and frontal signs stay. The clinical assessment output already carries every removed value, so no information is lost. This settles the worker's FLAGGED row on the same field. FIXED.
- B, major, `followup_outputs`: an order of `genetic_panel:ALS` fell to the benchmark library, which reports a normal C9orf72 and so contradicted the expansion on this case's FTD panel. Added follow-up `request_als_gene_panel_c9orf72` (`test_type: genetic_panel:ALS`) with the same C9orf72 expansion and SOD1, TARDBP and FUS negative, as P04 and P05 already have. No criterion changed. FIXED.
- B, minor, `metadata.fallback_tool_kinds`: the case has a cardiac-monitoring fallback but the kinds map omitted it; added `cardiac_monitoring: normal`. FIXED.
- E, minor, `initial_tool_outputs.literature_search[*].results[*].source`: the sources were citation keys (`[Rascovsky_2011]` or `Rascovsky_2011`), which a literature tool does not return, and the condition used three styles. They now give the full reference, as in M07-P02 (for example "Rascovsky K et al. Brain 2011;134:2456-2477 (FTDC criteria for bvFTD)"). Findings and summary are unchanged. FIXED.
- `perfect_agent.py` and `case_io.py check` were re-run on all 30 FTD cases after the changes and are clean; `test_case_guards.py -k FTD` passes (60 tests).

## Close-out (24 Oct 2026)

Decisions in `plans/FTD-decisions.md`. Changes:

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (the report is a transthoracic study). The MockServer routes echo reports by this field; without it the normal TTE fallback answered a TEE order too (PATTERNS section 5; FTD added to `DISCRIMINATOR_CONDITIONS`).
- Synonyms (`G31.09` entry, applied with `--prune --conditions ftd`): "pick disease" and "pick's disease" (retired) and the code G31.01 are no longer accepted. Pick disease is one FTLD-tau pathology that no case establishes, and G31.01 is where ICD-10-CM codes primary progressive aphasia, so a PPA answer coded G31.01 scored as correct here.

Checks: `perfect_agent.py` and `case_io.py check` clean; `test_case_guards.py -k FTD-` passes, including `test_routed_outputs_name_their_study`.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech-language findings matching the stored neuropsychology (reduced verbal fluency; naming as tested).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status of the case's functional decline instead of Karnofsky 100.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k FTD` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
