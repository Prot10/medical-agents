# FTD-S08
Reviewer status: R1 none, R2 none (FTD has no notes file; the binding clinician input is Reviewer 1's July 2026 tool rulings under `ftd:` in condition_tool_guidance.yaml) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No notes file exists for FTD. The plan's classes (C1-C15) were applied as class rulings (ROUND_POLICY ruling 2); every change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C/D | major | ground_truth.action_criteria[action-8-search-medical-literature]; followup_outputs[request_literature_capacity_ftd] | Literature search required, in the stop rule, expected evidence "Confirms Rascovsky 2011 criteria..."; the only literature output was a capacity and guardianship essay (C1, ruling 5) | FIXED: criterion optional, last, any query, out of `required_before_assessment`; capacity follow-up deleted; `initial_tool_outputs.literature_search` holds the canonical bvFTD text |
| C/D | major | followup_outputs[request_drug_interactions] | Drug check with no medication and no criterion; `proposed` carries a dose plan ("Sertraline 50 mg"), "Trazodone 50 mg" as alternative and ChEI "contraindicated" (C2) | FIXED: follow-up deleted (plan S08); no drug-check criterion |
| B | major | initial_tool_outputs.clinical_assessment | Hyperorality false although he "eats continuously"; empathy false despite emotional flatness with grandchildren; executive feature true while recall and clock were impaired; duplicated "Bedside cognitive testing"; templated impression claiming memory and visuospatial sparing (C3) | FIXED: rebuilt from the history: 4 of 6 features (disinhibition, empathy loss, compulsions, hyperorality); apathy absent; executive profile not established at the bedside; MMSE 22/30 itemised (serial sevens 1/5, recall 1/3, orientation 8/10); clock severely abnormal; canonical impression, second variant (memory/visuospatial items impaired, AD kept in the differential) |
| D | minor | patient.neurological_exam.mental_status | MMSE, FAB, fluency and clock given upfront although the screen and the battery are required criteria | FIXED: scores moved to the assessment and battery outputs; qualitative exam kept |
| B/C | minor | patient.neurological_exam.motor, .gait; ground_truth.red_herrings; key_clinical_evidence | Copied rigidity red herring with shuffling gait and reduced arm swing, i.e. parkinsonism the case never uses (C8) | FIXED: motor "Normal tone and bulk. 5/5 strength.", gait "Normal."; rigidity red herring and KCE line removed; DaTscan avoided-action rationale reworded to this exam |
| C | minor | ground_truth.red_herrings | With the rigidity removed, the case's real decoy is the AD-like bedside screen | FIXED: new red herring on the MMSE recall/orientation losses and clock (`initial_tool_outputs.clinical_assessment.findings[7]`), interpreted as retrieval and planning errors of bvFTD |
| D | major | followup_outputs[request_reviewed_neuropsych_battery].output | Neuropsych report embeds a legal/financial capacity verdict ("Lacks legal and financial decision-making capacity"); impression truncated (C13) | FIXED: capacity removed (now a must); domains executive, social cognition, memory (retrieval pattern), visuospatial (figure copy normal, clock errors of planning), language; canonical ending |
| B/C | major | initial_tool_outputs.labs | No folate, calcium, LFTs, albumin, platelets; `Reviewed_FTD_panel_additions`; unrequested copper; RPR/HIV under "Vitamins" (C5) | FIXED: rebuilt five panels, existing values kept, eGFR 88 (creatinine 1.0, male 56, CKD-EPI 2021); copper deleted; RPR/HIV in keyed follow-up `request_rpr_syphilis_hiv` carrying baseline plus serology (probed) |
| B | minor | followup_outputs[request_optional_counselled_ftd_genetics] | Template impression "All values within normal limits" | FIXED: report with repeat sizes and a one-sentence interpretation (a negative panel does not exclude FTLD) |
| B/C | major | fallback_tool_outputs.ct, .advanced_imaging | CT fallback "age-related involutional change" contradicts severe atrophy; unguarded "No abnormality" advanced-imaging fallback (C6) | FIXED: CT shows bifrontal and anterior temporal atrophy at CT resolution; advanced-imaging fallback deleted; fallback kinds updated |
| C | minor | ground_truth.action_criteria[action-7-order-advanced-imaging]; followup_outputs | No SPECT alternative; FDG impression em dash (C6) | FIXED: `perfusion_SPECT` alternative with an authored matching report; FDG impression reworded; optional |
| C | minor | initial_tool_outputs.mri | No exclusion statements | FIXED: no mass, haemorrhage, hydrocephalus, infarct or restricted diffusion; Fazekas 0 |
| C/A | minor | ground_truth.action_criteria[*] | Rationale = label; duplicate citations; `[AAN_dementia_2018]`; "RPR/HIV per risk" (C4) | FIXED: canonical labels, tailored rationales (battery: resolves the bedside profile; genetics: onset at 54, low yield), bracketed keys; avoided CT cites `[NICE_NG97]`; order assessment, battery, labs, MRI, FDG, genetics, literature |
| C | minor | ground_truth.sequence_constraints | No assessment-before-genetics (C15) | FIXED: soft, `[ACMG_NSGC_2011]` |
| C | major | ground_truth.assessment.required_recommendations | Template block duplicated next to the attorney must; "notify employer/state bar" while he has already resigned (C9) | FIXED: five musts: Rascovsky; why AD (bedside recall/clock) or psychiatric illness does not explain it; safety and capacity incl. finances, LPA and legal practice; caregiver plan; counselling before testing (onset 54) |
| C | minor | ground_truth.assessment.prohibited_recommendations[0,1] | Overstated ChEI and memantine wording (C10) | FIXED: canonical |
| C | major | ground_truth.differential | AD moderate with "biomarker workup needed" (none in the pathway); NPH listed although gait now normal (C11) | FIXED: AD frontal variant low (for and against stated), psychiatric, vascular and FTD-MND very low; NPH removed (no gait disorder, incontinence or disproportionate ventriculomegaly) |
| C/D | minor | ground_truth.key_clinical_evidence | "Rascovsky criteria are met with imaging confirmation" (verdict), rigidity line (C12) | FIXED: features, functional decline, battery profile, MRI pattern, canonical AD line, capacity line |

## Changes, in one paragraph a physician can read before re-reviewing
Literature is optional background with a general bvFTD summary; the capacity essay and the sertraline/trazodone drug plan are gone. The clinical-assessment report now follows the wife's history: four Rascovsky features (hyperorality added, empathy loss recognised), MMSE 22/30 itemised and a severely abnormal clock, so the bedside screen keeps AD in view; the neuropsychology battery then shows an executive and social-cognitive profile with retrieval-type memory and preserved figure copy, and no longer pronounces on legal capacity, which is now a must. The copied rigidity and shuffling gait were removed (exam normal tone and gait); the AD-like bedside screen is the case's red herring instead. Blood tests cover the NICE NG97 panel; syphilis and HIV serology only when ordered. The CT fallback shows the atrophy; FDG-PET or perfusion SPECT is optional with matching reports. Musts cover Rascovsky certainty, the AD and psychiatric mimics, finances and legal practice, caregiver support and counselling before any test. AD is low after the work-up.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys `[SNLG_ISS_2024]`, `[ACMG_NSGC_2011]` per plan section 5.2.

## Open questions for Andrea (judgment calls you could not settle)
- None. Note for the lead: the exam previously carried parkinsonian signs (shuffling gait, reduced arm swing, rigidity); following C8 they were removed rather than kept as a decoy, since nothing in the case used them.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: 4 of 6 features with executive feature false at the bedside agrees with `criteria_met`; MMSE 22/30 adds up (serial sevens -4, recall -2, orientation -2); second impression variant used; neuropsych report no longer pronounces on capacity (now a must); rigidity and shuffling gait removed from exam, red herrings and KCE, DaTscan rationale matches the normal exam; the new red herring points to an existing field (`clinical_assessment.findings[7]`) whose text it paraphrases; eGFR 88 matches creatinine 1.0, male 56; RPR/HIV routing probed (first or second order); FDG/SPECT authored; genetic report negative with correct interpretation; onset age 54 consistent with age 56 and a 2-year course; AD low with for/against. perfect_agent and case_io check clean; case guards pass. No errors found; no changes made.

## Condition audit (FTD auditor, 24 Oct 2026)

- E, minor, `initial_tool_outputs.literature_search[*].results[*].source`: the sources were citation keys (`[Rascovsky_2011]` or `Rascovsky_2011`), which a literature tool does not return, and the condition used three styles. They now give the full reference, as in M07-P02 (for example "Rascovsky K et al. Brain 2011;134:2456-2477 (FTDC criteria for bvFTD)"). Findings and summary are unchanged. FIXED.
- `perfect_agent.py` and `case_io.py check` were re-run on all 30 FTD cases after the changes and are clean; `test_case_guards.py -k FTD` passes (60 tests).

## Close-out (24 Oct 2026)

Decisions in `plans/FTD-decisions.md`. Changes:

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (the report is a transthoracic study). The MockServer routes echo reports by this field; without it the normal TTE fallback answered a TEE order too (PATTERNS section 5; FTD added to `DISCRIMINATOR_CONDITIONS`).
- Synonyms (`G31.09` entry, applied with `--prune --conditions ftd`): "pick disease" and "pick's disease" (retired) and the code G31.01 are no longer accepted. Pick disease is one FTLD-tau pathology that no case establishes, and G31.01 is where ICD-10-CM codes primary progressive aphasia, so a PPA answer coded G31.01 scored as correct here.

Checks: `perfect_agent.py` and `case_io.py check` clean; `test_case_guards.py -k FTD-` passes, including `test_routed_outputs_name_their_study`.
