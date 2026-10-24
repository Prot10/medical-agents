# VASC-DEM-S02
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The condition has no reviewer notes. The plan's classes (C1-C8, C13, C14, C16, C18, C19 and the S02 index entry) were applied as classes (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | ground_truth.action_criteria[action-5-analyze-brain-mri].alternatives | Non-schema `sequences` key plus `protocol`/`contrast`: no real call could match (C1). | FIXED: `analyze_brain_mri {}`; label and rationale rewritten. |
| D | major | action-7-search-medical-literature; initial and fallback literature_search | Literature criterion leaking its expected evidence into its own output (C2). | FIXED: criterion deleted, initial null, fallback deleted. |
| C | minor | action-8-check-drug-interactions; fallback_tool_outputs.drug_interactions | Generic drug check and fallback (C3 group D). | FIXED: deleted. |
| D | major | patient.neurological_exam.mental_status | Gave MoCA 20/30 and item scores (C4). | FIXED: bedside observation (orientation, slowing, flat affect, her own words), "Formal cognitive screening reported separately". |
| D | major | initial_tool_outputs.clinical_assessment (impression, criteria_met) | "this is the frontal-subcortical apathy of small-vessel disease, not a depressive episode", sertraline history in the screen; criteria_met held "depression_accounts_for_deficit", "executive_predominant_profile" and "independence_in_iadl_lost" verdicts (C5). | FIXED: scores-only impression; criteria_met keeps impairment and cueing. |
| B | major | initial_tool_outputs.clinical_assessment (findings, scores) | Items listed (only trail-making, digits backwards, fluency, recall and orientation lost) cannot give 20/30, and the screen had serial sevens 3/3 while the exam said points were lost on serial sevens; fluency given as animals for the MoCA letter-F item. | FIXED: full MoCA domains 4+3+3+1+1+3+4 = raw 19, plus 1 for 11 years of education = 20; serial sevens 1/3; repetition 1/2 (dysarthria); "9 F-words"; apathy and GDS moved to their own row. |
| D | major | followup_outputs[gait].output.impression | "the higher-level gait disorder of small-vessel disease" (C5). | FIXED: measurements and observations only; Romberg row added (as in the exam); cadence 123 steps/min added, consistent with 38 cm steps at 0.78 m/s. |
| D | major | initial_tool_outputs.specialized_test (impression, quantitative_data) | "the distinction that matters when depression has been assumed" (cross-reference to the history); profile "frontal-subcortical" (C5). | FIXED: profile wording; validity measures stated. |
| B | minor | initial_tool_outputs.labs | Template values (WBC 6.8, Hct 41.6, Plt 238, MCV 88, Na 139, K 4.2, ALT 22, albumin 4.1, folate 11.8); male creatinine range; eGFR ">60"; HDL ">40" in a woman (44 then unflagged); interpretive text (C6). | FIXED: varied values (Hct 40.4 for Hb 13.4, K 3.9 on hydrochlorothiazide), female ranges, HDL ">50" with 44 flagged low, pattern-level interpretation. |
| D | major | initial_tool_outputs.mri (impression, observations) | "The burden accounts for the frontal-subcortical syndrome"; "no abnormal enhancement" in a non-contrast study (C5). | FIXED: numbered STRIVE-2 impression; enhancement statement removed. |
| D | minor | fallback_tool_outputs (advanced_imaging, labs, ct, echo, cardiac_monitoring) | Off-pathway revealing text; echo "No cardioembolic source identified"; Holter average 72 vs her 79 (C7). | FIXED: advanced_imaging and labs deleted; CT rewritten for this patient; echo neutral with echo_type TTE; Holter average 78. metadata.fallback_tool_kinds updated. |
| C | major | ground_truth.differential[Depression] | Moderate after the scales, the failed trial and the MRI exclude it as the explanation (C8). | FIXED: low, may coexist. |
| C | major | ground_truth.assessment | Musts restated the scored work-up (document, exclude, MRI, validity measures) and gave no targets; no covert-SVD antiplatelet prohibition (C19). | FIXED: apathy vs depression recognised; review and consider tapering sertraline; BP below 130/80 gradually with orthostatic checks [ESO_2021_SVD]; smoking cessation; high-intensity statin for LDL 142 on simvastatin 20 mg; CPAP adherence; home safety and supervised medicines (gas ring, lives alone). Prohibition added: no antiplatelet for covert SVD alone [ESO_2021_SVD]. |
| A | minor | all criteria citations and rationales | Unbracketed duplicates; rationale equal to label (C13). | FIXED. |
| C | minor | avoided_actions rationales | Generic text; "MRI already obtained" (C18). | FIXED: case-specific; CT rationale per plan. Echo and monitoring waste kept (no clinical stroke). |
| C | minor | criteria order, stop_rule (C16) | | FIXED: screen, gait, neuropsych, labs, MRI; screen before MRI kept; max_additional_actions 1. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis unchanged (subcortical ischaemic vascular dementia with apathy misattributed to depression). The exam no longer gives the MoCA; the screen now adds up to 20/30 (raw 19 plus the education point) and agrees with the exam on serial sevens. No report states that the apathy is vascular or that the burden explains the syndrome; MRI, gait and neuropsychology report their own findings. Labs use female ranges (HDL 44 now flagged low) and a plain list of flagged values. The literature and drug-check steps are gone. Depression is now low in the differential. Musts now give her targets and safety measures: review sertraline, BP below 130/80 lowered gradually, smoking cessation, a high-intensity statin for LDL 142, CPAP adherence, home safety and supervised medicines; a prohibition on starting an antiplatelet for covert small-vessel disease is added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.1): remove F06.7 from the F01 codes of this dementia case.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Checked every Own-findings row against the file and the git diff: MRI `{}`; literature and drug check gone; MoCA domains give raw 19 plus 1 = 20, lost points (3+2+2+2+1+1) give 19, serial sevens 1/3 agrees with the exam; month wrong in both exam and screen; gait 38 cm at 123 steps/min gives 0.78 m/s; female ranges with HDL 44 flagged against >50, eGFR 71 follows from creatinine 0.88 at 71; depression low; covert-SVD prohibition present and no must starts an antiplatelet; no clinical stroke, so echo and monitoring waste are correct. Guard tests pass. No clinical or consistency error found.
Changed: `fallback_tool_outputs.echo` LVEF 60% to 64% (the fallback text was identical across S01-S05, template carry-over). Nothing else.
Re-ran `perfect_agent.py -v` (pass) and `case_io.py check` (clean for this case).

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Total cholesterol]`, `.abnormal_values_summary`, `.interpretation` | Total cholesterol 232 mg/dL did not equal LDL 142 + HDL 44 + TG 178/5 (221.6). | FIXED: 222 mg/dL in the row, summary and interpretation (still flagged high). |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here subcortical small-vessel labels and F01.2/I67.3. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
