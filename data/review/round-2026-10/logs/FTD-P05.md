# FTD-P05
Reviewer status: R1 not reviewed (no FTD notes file), R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | `data/review/round-2026-10/notes/` holds no FTD file; every change below is a lead-plan (`plans/FTD.md`) or own finding |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria[action-8-order-advanced-imaging]` | Plan C7: the MRI is normal, so without functional imaging the case meets only possible bvFTD while the label says probable; FDG-PET was optional | FIXED: `recommended`, `perfusion_SPECT` alternative with an authored HMPAO follow-up; rationale per plan (see Open questions, plan Q2) |
| C | major | `followup_outputs[request_optional_fdg_pet]` | The FDG result was "borderline", "at the lower limit of abnormality", "expert interpretation essential": it could not provide the imaging support that the "probable" label needs | FIXED: same distribution (right > left orbitofrontal and anterior cingulate, mild right anterior temporal, posterior sparing) reported as mild but definite hypometabolism with z-scores (-2.4 to -2.9), numbered impression "consistent with an early frontotemporal metabolic profile"; capitals and the NOTE removed |
| C | major | `ground_truth.action_criteria[action-9-search-medical-literature]`, `followup_outputs` (2 literature follow-ups) | Plan C1: literature required and in the stop rule; the two follow-ups were a litigation-capacity essay with management (power of attorney, conservatorship) and a cognitive-reserve essay stating this case's teaching point ("social cognition testing is required") | FIXED: both follow-ups deleted; initial literature authored with the canonical familial-variant text; criterion `optional`, last, `{}` arguments, out of the stop rule |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.mental_status`, `.additional` | Narrator steering: "His MoCA of 25/30 is near-normal and could lead to the conclusion...", "allow him to appear cognitively intact...", "The near-normal MoCA is extremely deceptive", "HOWEVER"; `additional` restated the history and interpreted it ("contrast with profound behavioral disinhibition") | FIXED: the two HPI sentences and the steering phrases deleted; `additional` now an exam finding (no fasciculations, wasting or tongue atrophy) |
| C | major | `patient.history_present_illness`, `ground_truth.differential` | Loss of empathy rested only on "appeared unconcerned" about missed lectures; late-onset mania (disinhibition, litigiousness, hypersexual comments, 12-18 h/day online) was not addressed | FIXED: concrete empathy example from the sister; pertinent negatives (no elevated mood, pressured speech or reduced sleep, sleeps 7-8 h); differential entry for primary psychiatric disorder (low) with for/against |
| B | major | `initial_tool_outputs.clinical_assessment` | Plan C3: fragments ("His intact language ... contrast with profound behavioral disinhibition" as the disinhibition evidence), duplicated "Bedside cognitive testing" entries, steering sentence, template impression; apathy false although he stopped 30 years of daily reading and missed lectures without concern | FIXED: one finding per feature, all six present (apathy now true on the history), informant, screen, functional decline; canonical impression noting the near-normal total |
| A/D | major | `initial_tool_outputs.labs` | Plan C5: "Reviewed_FTD_panel_additions"; free T4 with normal TSH; no folate, platelets, Hb, calcium, LFTs; unrequested copper, ceruloplasmin, RPR, HIV, NMDAR and LGI1 antibodies | FIXED: standard panels, stored values kept, normal values added; free T4 and copper/ceruloplasmin deleted (no indication at 56 without liver disease or movement disorder); serum NMDAR/LGI1 (with CASPR2) moved to a keyed `autoimmune_encephalitis_panel` follow-up with the templated hedge; RPR/HIV to a keyed follow-up |
| D | minor | `followup_outputs[request_reviewed_neuropsych_battery]` | Capitals and steering ("SOCIAL COGNITION (THE KEY DIAGNOSTIC TESTS)", "CONCLUSION FROM STANDARD TESTS ALONE"); "Similarities 13/13" (not a WAIS-IV metric); MoCA (a bedside test) inside the battery; no memory or visuospatial data; truncated impression | FIXED: domain-by-domain findings (Similarities scaled score 15; CVLT-II recall 9/16, recognition 15/16; ROCF copy 35/36, VOSP normal; BNT 58/60), canonical ending |
| D | minor | `followup_outputs[request_optional_counselled_ftd_genetics]` | Template "Abnormal values: ..." impression | FIXED: report voice, numbered impression with post-test counselling note |
| B | minor | `initial_tool_outputs.mri` | Duplicated "normal" statements across fields | FIXED: one-line normal impression; observations kept as pertinent findings |
| B | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, `.drug_interactions` | Plan C6: CT with an incidental granuloma that the MRI does not show; off-pathway advanced imaging; "agent not specified" drug check (no medications) | FIXED: CT without atrophy (consistent with the normal MRI; canonical CT-insensitivity sentence); the other two deleted |
| C | major | `ground_truth.assessment.required_recommendations` | Plan C9: 7 musts with template duplicates; "biomarkers (FDG-PET, genetics)" presumes optional results; "Address occupational capacity urgently" not checkable | FIXED: five case-specific musts (Rascovsky certainty; why MoCA/MRI do not exclude it and why psychiatric illness does not explain it; safety, litigation capacity and fitness to teach; caregiver plan without ChEI/memantine; counselling before testing) |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Plan C10 wording | FIXED |
| C | major | `ground_truth.differential` | Plan C11: the target "Familial bvFTD (C9orf72)" high; AD moderate; alcohol entry in a man who does not drink; no phenocopy syndrome although the MRI is normal | FIXED: psychiatric low, phenocopy low, frontal AD low, autoimmune encephalitis very low, burnout very low |
| D | major | `ground_truth.key_clinical_evidence` | "Family pattern supports a C9orf72 expansion" presumes the optional result; "Tier per the July 2026 clinical review" line | FIXED: four case lines |
| C | minor | `ground_truth.red_herrings` | The normal MRI and the father's sudden cardiac death (plan: no cardiac work-up) are distractors the case uses but did not declare | FIXED: both added; cardiac-monitoring avoided-action rationale mentions the father's death |
| C | minor | `ground_truth.action_criteria[*]` | Plan C4 labels/rationales/citations | FIXED; avoided CT cites `[NICE_NG97]` |
| C | minor | `ground_truth.action_criteria` order, `sequence_constraints` | Plan C15 | FIXED: assessment, neuropsych, labs, MRI, FDG/SPECT, genetics, literature; soft assessment before genetics |
| E | minor | `metadata.notes`, `difficulty_rationale`, `key_educational_points` | "pathognomonic dissociation", "completely masks", "normal MRI + subtle FDG-PET = C9orf72 signature" | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The narrative no longer tells the agent that the MoCA is deceptive; it now gives a concrete loss-of-empathy example and the negatives that make late-onset mania unlikely. The informant assessment scores all six Rascovsky features from the sister's history (apathy is now counted: he stopped lifelong daily reading and missed lectures without concern). Because the MRI is normal, FDG-PET is now recommended (perfusion SPECT accepted) and its result was made a mild but definite right-predominant frontal and right anterior temporal hypometabolism, so that the probable label has its imaging support. The neuropsychological battery reports the IQ / social-cognition dissociation with proper scores and adds memory, visuospatial and language results. Labs are standard panels; autoimmune antibodies and syphilis/HIV serology answer only a targeted order. The two literature essays are gone and literature is optional and last. Musts are case-specific (including litigation capacity and fitness to teach), the differential is the post-work-up view (psychiatric, phenocopy, frontal AD low), and the normal MRI and the father's cardiac death are declared red herrings.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used that the criteria pack does not list: `[SNLG_ISS_2024]`, `[ACMG_NSGC_2011]`, `[NICE_NG97]` (plan section 5 item 2).
- `condition_tool_guidance.yaml` `ftd:`: record FDG-PET recommended in this case (plan section 5 item 6).

## Open questions for Andrea (judgment calls you could not settle)
- Plan Q2 (FDG-PET recommended rather than Reviewer 1's "optional"): applied, because with a normal MRI the probable label needs functional imaging. Decided here as well: the FDG report was strengthened from "borderline" to mild but definite hypometabolism, since a borderline study would leave the label unsupported. If the reviewers prefer to keep FDG optional, the label should be reconsidered instead (it would be possible bvFTD on the required work-up).

## Verification
Adversarial verifier, 24 Oct 2026. There is no FTD notes file. I read the log, the diff and the whole final case.
- Confirmed:
  - MoCA 25/30 arithmetic: trails 1, fluency 1, recall 2, abstraction 1.
  - All six Rascovsky features are documented in the HPI.
  - The negatives for late-onset mania are present.
  - FDG is recommended with SPECT as its alternative (plan C7/Q2). The FDG result is strengthened to mild but definite hypometabolism. That is a data change, but it is logged and justified: a borderline study could not support the probable label.
  - The CT fallback is normal, matching the normal MRI.
  - Autoimmune antibodies and RPR/HIV answer targeted orders only.
  - The musts presume no optional result, and the KCE wording is conditional.
- Found and fixed (1, major, class): `genetic_panel:ALS` was answered by the library with a normal C9orf72. That contradicts the authored expansion. Added follow-up `request_als_gene_panel_c9orf72`: the same expansion (>700/2), with SOD1, TARDBP and FUS negative.
- Checks run after the changes: `perfect_agent.py -v` passes, `case_io.py check` names no failure for this case, `test_case_guards` (leak, followup, banned-string) passes. I also called the MockServer directly with FDG_PET, perfusion_SPECT, amyloid_PET, DaTscan, CSF AD markers, genetic_panel:FTD and genetic_panel:ALS, emg_ncs, respiratory_function, the neuropsych battery, targeted RPR/HIV, the baseline labs, CT and literature, to check that every plausible order gets a report consistent with the case.

## Condition audit (FTD auditor, 24 Oct 2026)

- D, major, `patient.neurological_exam.mental_status`: the examination gave the bedside screen results (MoCA 25/30 with item losses and letter fluency), which the required `perform_clinical_assessment` returns (ROUND_POLICY timeline-leak rule). The other 12 FTD cases, and VASC-DEM and ALZ-EARLY, had already moved them out. Removed the scores and test results; the behavioural observations, insight and frontal signs stay. The clinical assessment output already carries every removed value, so no information is lost. FIXED.
- B, minor, `fallback_tool_outputs.csf`: a case CSF fallback with empty `special_tests` answered any CSF order without a stored result (for example Abeta42, p-tau and t-tau), so the ordered assays were missing from the report. Deleted, together with `metadata.fallback_tool_kinds.csf`, as in M07, M09, M10, P01 and P02. The library now answers per assay; a probe returned normal AD markers. FIXED.
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

- criterion `action-9-search-medical-literature` label: "Literature on bvFTD with normal structural imaging (optional)" -> "Literature on bvFTD with normal structural imaging"
