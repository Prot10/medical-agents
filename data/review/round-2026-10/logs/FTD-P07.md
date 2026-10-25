# FTD-P07
Reviewer status: R1 not reviewed (no FTD notes file), R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | `data/review/round-2026-10/notes/` holds no FTD file; every change below is a lead-plan (`plans/FTD.md`) or own finding |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Plan C1: the output repeated the literature criterion's `expected_evidence` (leak guard failure); keyed "C9orf72-associated bvFTD and surveillance", which presumes the optional genetic result | FIXED: canonical bvFTD text with the psychiatric-mimic and familial sentences (case is in both plan lists), keyed "familial bvFTD presenting as treatment-resistant depression"; leak guard passes |
| C | major | `ground_truth.action_criteria[action-8-search-medical-literature]` | Ruling 5: literature `recommended` | FIXED: optional, last, `{}` arguments |
| C | major | `ground_truth.action_criteria[action-7-order-advanced-imaging]` | Plan C7: the MRI is borderline, so without functional imaging the case meets only possible bvFTD while the label says probable | FIXED: `recommended`, `perfusion_SPECT` alternative with an authored follow-up concordant with the FDG result (plan Q2) |
| B | major | `initial_tool_outputs.clinical_assessment` | Plan C3: informant false although his wife gives the history; only 3 features marked although the history documents all six (apathy, empathy loss, fixed meals were false); the executive finding was a sentence fragment ending in ";"; duplicated screen lines; template impression | FIXED: one finding per feature, 6 present, informant true, screen line (MMSE, FAB, fluency), functional decline; canonical impression |
| A/B | major | `initial_tool_outputs.labs` | Plan C5: "CSF 14-3-3 protein" reported inside a blood panel without any lumbar puncture; unrequested heavy-metal screen, copper, ceruloplasmin, RPR, HIV; "Reviewed_FTD_panel_additions"; no calcium, ALP, bilirubin, MCV | FIXED: standard panels with stored values kept and missing analytes added; 14-3-3, heavy metals and copper studies deleted; RPR/HIV moved to a keyed follow-up |
| B | minor | `followup_outputs[request_reviewed_neuropsych_battery].output.quantitative_data` | A MoCA 22/30 that appears nowhere else (the bedside test was the MMSE 27/30), plus MMSE and FAB, inside the battery; FrSBe given as percentiles (72nd is not abnormal) and NPI-Q "caregiver distress 18/36" (distress is scored out of 60) | FIXED: battery scores only; FrSBe as T-scores (apathy 78, disinhibition 84, executive 80; significant at 65 or above); NPI-Q severity 18/36; canonical impression (was cut mid-sentence) |
| D | minor | `followup_outputs[request_optional_counselled_ftd_genetics]` | Template "Abnormal values: ..." impression and capitals | FIXED: report voice, numbered impression with post-test counselling note |
| D | minor | `initial_tool_outputs.mri.impression`, `followup_outputs[request_optional_fdg_pet]` | Unnumbered MRI impression ending "findings are subtle and non-diagnostic"; FDG impression unnumbered | FIXED: numbered impressions; the MRI keeps a worded imaging differential ("early FTLD cannot be excluded") |
| D | minor | `patient.neurological_exam.mental_status` | Steering sentence "Mini-Mental State Exam does not capture the disinhibition..." and "Notably" | FIXED: removed; fasciculations stated absent in `motor` (C9orf72 / MND spectrum in the differential) |
| B | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, `.drug_interactions` | Plan C6 | FIXED: CT without atrophy out of proportion to age (consistent with a borderline MRI); off-pathway advanced imaging and "agent not specified" drug check deleted (no drug criterion) |
| C | major | `ground_truth.assessment.required_recommendations` | Plan C9: "Pursue genetic testing", "Surveil for ALS features given C9orf72 risk" (presumes the optional result), template duplicates | FIXED: five musts (Rascovsky certainty; why depression does not explain it; safety, finances and work; caregiver plan without ChEI/memantine; counselling before testing with the brother and adult children, predictive testing only after their own counselling) |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Plan C10 wording | FIXED |
| C | major | `ground_truth.differential` | Plan C11: depression and the target both high; AD and FTD-MND moderate; duplicate psychiatric entries | FIXED: depression as sole cause low, phenocopy low, frontal AD low, coexisting MND very low |
| D | major | `ground_truth.key_clinical_evidence` | Plan C12: "AD biomarker exclusion (amyloid PET) is decisive" (no amyloid criterion); "strongly suggests C9orf72" (presumes the result); tier line | FIXED: four lines |
| C | minor | `ground_truth.red_herrings` | The near-normal MMSE is a distractor the case uses | FIXED: added |
| C | minor | `ground_truth.action_criteria[*]` | Plan C4 labels/rationales/citations | FIXED; avoided CT cites `[NICE_NG97]` |
| C | minor | `ground_truth.action_criteria` order, `sequence_constraints` | Plan C15 | FIXED: assessment, neuropsych, labs, MRI, FDG/SPECT, genetics, literature; soft assessment before genetics |
| E | minor | `metadata.notes`, `difficulty_rationale`, `key_educational_points` | No notes | FIXED: notes written to the case |

## Changes, in one paragraph a physician can read before re-reviewing
The patient block is unchanged except for one steering sentence removed and fasciculations stated absent. The informant assessment now credits the wife as informant and scores all six Rascovsky features that the history documents. Because the MRI shows only borderline frontal and anterior temporal volume loss, FDG-PET (or perfusion SPECT) is now recommended so that the probable label has its imaging support; both report right-predominant frontal hypometabolism or hypoperfusion with posterior sparing. The blood panel no longer contains a CSF 14-3-3 result, heavy metals or copper; syphilis and HIV serology answer only a targeted order. The neuropsychological report now carries only battery scores (the stray MoCA 22/30 is gone) with correct FrSBe T-scores. Literature is general, optional and last, and no longer leaks the scoring key. Musts no longer presume a C9orf72 result and include counselling for the brother and adult children; depression is low in the differential with phenocopy, frontal AD and coexisting MND.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used that the criteria pack does not list: `[SNLG_ISS_2024]`, `[Ducharme_2020]`, `[ACMG_NSGC_2011]`, `[NICE_NG97]` (plan section 5 item 2).
- `condition_tool_guidance.yaml` `ftd:`: record FDG-PET recommended in this case (plan section 5 item 6).

## Open questions for Andrea (judgment calls you could not settle)
- Plan Q2 (FDG-PET recommended rather than Reviewer 1's "optional"): applied, because the MRI is equivocal and the label says probable. If the reviewers keep FDG optional, the label should become possible bvFTD on the required work-up.

## Verification
Adversarial verifier, 24 Oct 2026. There is no FTD notes file. I read the log, the diff and the whole final case.
- Confirmed:
  - MMSE 27/30 arithmetic.
  - NPI-Q severity range 0-36 and the FrSBe T-score threshold of 65.
  - Utilisation behaviour is in the exam.
  - The CT fallback matches the borderline MRI.
  - FDG is recommended with SPECT authored.
  - The literature leak guard passes.
  - The musts presume no genetic result.
- Found and fixed (1, major, class): `genetic_panel:ALS` (plausible here: coexisting MND is in the differential) was answered by the library with a normal C9orf72. That contradicts the authored expansion. Added follow-up `request_als_gene_panel_c9orf72`: the same expansion (~800/8), with SOD1, TARDBP and FUS negative.
- Checks run after the changes: `perfect_agent.py -v` passes, `case_io.py check` names no failure for this case, `test_case_guards` (leak, followup, banned-string) passes. I also called the MockServer directly with FDG_PET, perfusion_SPECT, amyloid_PET, DaTscan, CSF AD markers, genetic_panel:FTD and genetic_panel:ALS, emg_ncs, respiratory_function, the neuropsych battery, targeted RPR/HIV, the baseline labs, CT and literature, to check that every plausible order gets a report consistent with the case.

## Condition audit (FTD auditor, 24 Oct 2026)

- D, major, `patient.neurological_exam.mental_status`: the examination gave the bedside screen results (MMSE 27/30 with item losses, pentagon copy, FAB 13/18 and letter and category fluency), which the required `perform_clinical_assessment` returns (ROUND_POLICY timeline-leak rule). The other 12 FTD cases, and VASC-DEM and ALZ-EARLY, had already moved them out. Removed the scores and test results; the behavioural observations, insight and frontal signs stay. The clinical assessment output already carries every removed value, so no information is lost. FIXED.
- E, minor, `fallback_tool_outputs.literature_search`: the placeholder ("general", "Recommend correlating with current society guidelines") was deleted together with its kind key, as in the other FTD cases. The initial literature output answers any query. FIXED.
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

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-8-search-medical-literature` label: "Literature on familial bvFTD and psychiatric mimics (optional)" -> "Literature on familial bvFTD and psychiatric mimics"
