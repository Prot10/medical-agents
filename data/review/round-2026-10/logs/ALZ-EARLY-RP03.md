# ALZ-EARLY-RP03
Reviewer status: R1 not reviewed, R2 not reviewed (no entry in notes/ALZ-EARLY.md) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note names this case. Condition classes C1.2, C2, C3, C4, C5, C8, C10, C11, C12, C13, C16 of plans/ALZ-EARLY.md applied (see below). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | patient.history_present_illness; past_medical_history | Onset "roughly two years ago" in the HPI against "18 months" in the chief complaint and HPI opening; "known mild cataracts" in the HPI absent from the PMH. | FIXED: 18 months throughout (onset about 64.5, so G30.0 stays correct); cataracts added to PMH. |
| B/C | major | initial_tool_outputs.clinical_assessment | `independence_in_instrumental_activities_lost` false while the scores block said dementia and the family has taken over driving (C4); `amnestic_predominant_profile` true in a PCA case; template impression with "storage deficit" and engineering sentences (C3). | FIXED: IADL true; amnestic false; cueing true with a recorded 2/5 free and 3/5 cued recall (MoCA breakdown now adds to 23); PCA, parietal, informant and IADL findings; canonical impression. |
| B | major | followup_outputs[neuropsych].impression | Said "episodic memory and confrontation naming were not formally assessed" while the findings report CVLT-II 10/16 and Boston Naming 52/60. | FIXED: memory, naming and fluency reported as normal; visual-search confound on TMT; mild dementia level. |
| B | minor | initial_tool_outputs.mri | Post-gadolinium statement with contrast false; an MRA nobody ordered; SWI line phrased as a CAA verdict; the atrophy finding's FLAIR said no white matter abnormality while the next finding is Fazekas 2; DWI statement stored in the `borders` field; "colpocephaly" (a congenital term) for ex vacuo enlargement; impression said white matter disease "could confound the clinical picture" (C5). | FIXED: all corrected; numbered impression with "suggestive of a posterior-predominant neurodegenerative process". |
| B | minor | initial_tool_outputs.labs (B12, platelets) | Values identical to RP01 and RP02 (B12 310, platelets 234). | FIXED: 368 pg/mL and 251 x10^9/L. |
| C | major | followup_outputs[drug check]; action-10 | Output said levetiracetam "may lower seizure threshold ... provides protective coverage" (wrong), offered memantine for later combination, and the criterion was optional with no arguments although fluoxetine (strong CYP2D6 inhibitor) is a concrete interaction (C1.2). | FIXED: output rewritten (fluoxetine CYP2D6, levetiracetam none, labelled cholinomimetic seizure warning, HR 72, rivastigmine as the non-CYP alternative); criterion `{"drug": "donepezil"}`, `required`, in the stop rule. No ECG criterion: neither drug is a QT-prolonging co-medication of the citalopram class (plan C14). |
| A | major | followup_outputs (two search_medical_literature) | Literature follow-ups with no criterion (C8). | FIXED: deleted. |
| C | major | action-9 (perfusion SPECT) | Criterion said SPECT is used "when FDG-PET is unavailable", but nothing in the case says so; expected_evidence spoke of hypometabolism for a perfusion study. | FIXED: FDG-PET added as first alternative with an authored concordant follow-up (right more than left parieto-occipital hypometabolism); SPECT kept as second alternative; expected_evidence covers both. |
| A/B | major | action-8; initial_tool_outputs.csf | Amyloid PET the "single optional route"; CSF would return the library normal (C2). | FIXED: CSF and amyloid PET alternatives; concordant CSF authored (Abeta42 476, Abeta40 10200, ratio 0.047 low, p-tau181 88 high, t-tau 590 high). Amyloid PET impression now the binary read; tracer filled. |
| E | minor | all criteria | Rationale equal to label; duplicated citations (C13). | FIXED. MRI label now names the exclusions relevant here. |
| A | minor | sequence_constraints; stop_rule | None; max 0 (C16). | FIXED: soft MRI before biomarker, clinical before biomarker; max 1. |
| C | major | assessment | Restating musts; engineering biomarker must; FDG must for a study the case did not offer; generic prohibitions (C12). | FIXED: AChEI must adapted to fluoxetine and epilepsy, canonical biomarker must, OT and low-vision with home stair assessment (two falls), safety, BP and lipids (Fazekas 2), informant, disclosure. Prohibitions: do not attribute to epilepsy/levetiracetam/depression/cataract; no tramadol or bupropion (seizure threshold; tramadol with fluoxetine, serotonin syndrome); mild-stage memantine. |
| C | major | ground_truth.differential | CBS and DLB moderate with absent features; CJD cited RT-QuIC and 14-3-3 not in the case; epilepsy/antiseizure drug, depression, cataract and vascular contribution, all raised by the case, missing (C11). | FIXED: rebuilt, all alternatives low or very low with the excluding data. |
| D/C | major | ground_truth.key_clinical_evidence | Six template items false for this case (C10). | FIXED: four case-true items. |
| C | minor | ground_truth.red_herrings | Empty; the aunt's Lewy body dementia and the epilepsy/depression history are the case's traps. | FIXED: two red herrings. |
| - | check | 3.6 check | Probe: CSF -> initial csf; amyloid PET, FDG, SPECT, drug check -> their follow-ups; none from the library. perfect_agent -v ok. | OK |

## Changes, in one paragraph a physician can read before re-reviewing
PCA due to Alzheimer disease, mild dementia, onset at about 64 (label and G30.0 unchanged). The functional field now says independence is lost, matching the history (the family took over driving and she stopped work). The clinical assessment is a PCA assessment, and the neuropsychology impression now reports the memory and naming results it had claimed were not tested. The MRI no longer contains contrast, MRA or contradictory white matter statements. Because she takes fluoxetine, the donepezil check is required and now states the CYP2D6 interaction, with rivastigmine as an alternative. The false levetiracetam statement is gone. FDG-PET was added as the first option for the functional imaging step, with perfusion SPECT kept as a substitute. Amyloid status can be shown by CSF or PET, with a concordant CSF report authored. The literature follow-ups are gone. The differential now covers DLB (aunt), epilepsy and its drug, depression and cataract, all at low. The musts now cover treatment adapted to fluoxetine and epilepsy, low vision and OT, and vascular risk, and a new prohibition bars tramadol and bupropion.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys `[PCA_consensus_2017]`, `[NICE_NG97]` (plan section 5.2).
- Synonyms: G30.1 and its labels appended to an early-onset case (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the full diff and the whole final case. No reviewer note names this case.
- Checked: 18-month timeline throughout (onset about 64.5, G30.0 correct); MoCA breakdown adds to 23 (visuospatial 2, naming 1, recall 3, orientation 1) and agrees with the exam; IADL true, amnestic false, cueing true agree with the narrative and battery; neuropsychology impression now reports the memory, naming and fluency results it contains; MRI has no contrast, MRA or contradictory white matter text, right-predominant atrophy agrees with FDG and SPECT; levetiracetam statement removed; drug check required with correct pharmacology (fluoxetine strong CYP2D6 inhibitor, galantamine partly CYP2D6, rivastigmine non-CYP, labelled cholinomimetic seizure warning, HR 72 matches vitals); the functional-imaging criterion's two alternatives and the biomarker criterion's two alternatives all have case-authored outputs (CSF 476/10200 = 0.047); musts and prohibitions are case-specific and correct (tramadol and bupropion lower the seizure threshold; tramadol with fluoxetine adds serotonin risk); differential matches the evidence.
- Judgment reviewed: no ECG step. Fluoxetine carries only a conditional QT risk and no QT-prolonging drug of the citalopram class is present, and ECG is not an avoided action, so an agent that orders one is not penalised. Accepted.
- Found nothing to change. perfect_agent.py -v and case_io.py check clean.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (the labs criterion label), the wording the other six cases already use.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- Normal values in `Magnesium` varied (Magnesium 2.0 to 2.2), all still within the case's reference ranges: the same numbers (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8) had been copied into up to 13 cases, a template artefact raised by the S01 worker; no text cites the changed values.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.
