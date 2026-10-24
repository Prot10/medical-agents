# FTD-S10
Reviewer status: R1 none, R2 none (FTD has no notes file; the binding clinician input is Reviewer 1's July 2026 tool rulings under `ftd:` in condition_tool_guidance.yaml) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No notes file exists for FTD. The plan's classes (C1-C15) were applied as class rulings (ROUND_POLICY ruling 2); every change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C/D | major | ground_truth.action_criteria[action-8-search-medical-literature]; followup_outputs[request_literature_c9orf72_adolescent] | Literature required, in the stop rule, "Confirms Rascovsky..." evidence; adolescent predictive-testing essay as the only literature output (C1) | FIXED: optional, last, any query, out of `required_before_assessment`; follow-up deleted, its content now a must (predictive testing of the son deferred); canonical familial-FTD text in `initial_tool_outputs.literature_search` |
| B | major | initial_tool_outputs.clinical_assessment | Informant false although the wife gives the history; stereotyped behaviour false despite "only boxing matches, combative when interrupted"; duplicated bedside line; templated impression (C3) | FIXED: rebuilt: 4 of 6 features (disinhibition, stereotyped behaviour, hyperorality incl. alcohol, executive profile); apathy absent; empathy loss not described; informant true; MMSE 20/30 itemised (serial sevens 1/5, recall 2/3, orientation 8/10, command 2/3, repetition, writing); canonical impression |
| C | major | ground_truth (assessment, differential, red_herrings) | 8 to 10 beers a day never addressed (same defect as S09) | FIXED: alcohol must (why it does not explain the syndrome; medically supervised reduction with withdrawal precautions, wife controls access, oral thiamine); "Alcohol-related brain damage" low in the differential; alcohol red herring (Rascovsky dietary change) |
| C | major | ground_truth.differential; initial_tool_outputs.mri; followup FDG | Caudate atrophy on MRI and caudate hypometabolism on FDG with an affected father and behavioural onset, but Huntington disease absent from the differential | FIXED: Huntington disease low (no chorea or oculomotor signs; lobar knife-blade pattern); caudate red herring on `initial_tool_outputs.mri.additional_observations[1]` |
| B/C | minor | patient.neurological_exam.motor, .gait; ground_truth.red_herrings; key_clinical_evidence | Copied rigidity red herring with shuffling gait (C8) | FIXED: motor "Normal tone and bulk. 5/5 strength throughout. No fasciculations.", gait "Normal."; rigidity red herring and KCE line removed; DaTscan avoided rationale reworded |
| D | minor | patient.neurological_exam.mental_status | MMSE, FAB, fluency upfront | FIXED: moved to the assessment and battery outputs |
| B/C | major | initial_tool_outputs.labs | No folate, calcium, LFTs, albumin, platelets; `Reviewed_FTD_panel_additions`; copper and heavy-metal screen unrequested; RPR/HIV under "Vitamins" (C5) | FIXED: five panels with existing values kept, eGFR 90 (creatinine 1.0, male 53), LFTs at the upper normal range; copper and heavy metals deleted; RPR/HIV keyed follow-up with baseline plus serology |
| B | minor | followup_outputs[request_optional_counselled_ftd_genetics] | Template "Abnormal values: C9orf72 ABNORMAL ..." impression | FIXED: report: about 700 repeats on one allele, 2 on the other; one-sentence interpretation (FTD and ALS); counselling note, 50% risk to each child |
| D/E | minor | followup_outputs[request_reviewed_neuropsych_battery].output | Truncated impression (C13) | FIXED: domains with visuospatial and language; canonical ending |
| C | minor | initial_tool_outputs.mri | No exclusion statements | FIXED: no mass, haemorrhage, hydrocephalus, infarct or restricted diffusion; normal cerebellum; Fazekas 1 |
| B/C | major | fallback_tool_outputs.ct, .advanced_imaging, .drug_interactions | Normal CT; unguarded advanced-imaging fallback; "agent not specified" drug fallback (C6, C2) | FIXED: CT with bifrontal and anterior temporal atrophy; the other two deleted; fallback kinds updated (drug_interactions removed, ct "case") |
| C | minor | ground_truth.action_criteria[action-7-order-advanced-imaging]; followup_outputs | No SPECT alternative; FDG em dash | FIXED: SPECT alternative and matching report; FDG impression reworded; optional |
| C/A | minor | ground_truth.action_criteria[*] | Rationale = label; duplicate citations; `[AAN_dementia_2018]`; "RPR/HIV per risk" (C4) | FIXED: canonical labels, tailored rationales (alcohol for labs and MRI; onset 51 and father for genetics); bracketed keys; avoided CT `[NICE_NG97]`; order assessment, battery, labs, MRI, FDG, genetics, literature |
| C | minor | ground_truth.sequence_constraints | No assessment-before-genetics (C15) | FIXED: soft, `[ACMG_NSGC_2011]` |
| C | major | ground_truth.assessment.required_recommendations | "Pursue genetic testing" and "Screen for ALS given C9orf72 risk" presume an optional result; seven musts with duplicates (C9) | FIXED: six musts: Rascovsky; alcohol mimic and management; safety and capacity incl. finances, LPA and aggression toward wife and teenage son; caregiver plan; counselling before testing with predictive testing of the son deferred; motor neuron disease review at follow-up (phrased on the familial pattern, not on a result) |
| C | minor | ground_truth.assessment.prohibited_recommendations[0,1] | Overstated wording (C10) | FIXED: canonical |
| C | major | ground_truth.differential | "Sporadic bvFTD" and FTD-MND moderate; AD "Amyloid PET should be negative" with no amyloid step (C11, C12) | FIXED: FTD-MND, alcohol, Huntington and AD low; psychiatric very low; each with reasons |
| C/D | minor | ground_truth.key_clinical_evidence | "raises strong suspicion for C9orf72", "Genetic confirmation informs..." (presumes the optional result) (C12) | FIXED: features, functional decline, MRI pattern, pedigree "supports offering genetic counselling and testing", canonical AD line |

## Changes, in one paragraph a physician can read before re-reviewing
The clinical-assessment report now follows the wife's history (four Rascovsky features, informant recorded, MMSE 20/30 itemised); the exam no longer gives the scores, and the copied rigidity and shuffling gait were removed. The heavy drinking (8 to 10 beers a day) is scored as a bvFTD dietary change, kept as a low-likelihood mimic and managed in a must with supervised reduction and thiamine. Huntington disease is now in the differential because the MRI and FDG show caudate involvement in a man with an affected father; it is low without chorea. Labs cover the NICE NG97 panel; serology only when ordered. The genetic report is a proper report of the C9orf72 expansion. Literature is optional; the adolescent-testing essay became a must (defer predictive testing of the teenage son). The CT fallback shows the atrophy; FDG-PET or SPECT optional with matching reports. Musts also cover aggression risk at home and motor neuron disease review at follow-up.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys `[SNLG_ISS_2024]`, `[ACMG_NSGC_2011]` per plan section 5.2.

## Open questions for Andrea (judgment calls you could not settle)
- None. Note for the lead: S09 and S10 both carry new heavy drinking that the plan does not mention; I handled it identically (Rascovsky dietary change, low-likelihood alcohol mimic, management must). Other cases with an alcohol line may need the same.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: 4 of 6 features agree with `criteria_met`, informant true; MMSE 20/30 adds up (serial sevens -4, recall -1, orientation -2, command -1, repetition -1, writing -1); exam scores removed; rigidity and shuffling gait removed consistently (motor, gait, red herrings, KCE, DaTscan rationale); caudate atrophy appears in the MRI and FDG and is handled by the Huntington entry and red herring (field path `mri.additional_observations[1]` holds "Mild caudate atrophy"); alcohol must includes withdrawal precautions; predictive testing of the teenage son deferred in the counselling must; MND review must not conditioned on the optional genetic result; C9orf72 report consistent with the familial pattern; eGFR 90 matches creatinine 1.0, male 53; RPR/HIV, FDG and SPECT routing probed. perfect_agent and case_io check clean; case guards pass. No errors found; no changes made.

## Condition audit (FTD auditor, 24 Oct 2026)

- B, major, `followup_outputs`: an order of `genetic_panel:ALS` fell to the benchmark library, which reports a normal C9orf72 and so contradicted the expansion on this case's FTD panel. Added follow-up `request_als_gene_panel_c9orf72` (`test_type: genetic_panel:ALS`) with the same C9orf72 expansion and SOD1, TARDBP and FUS negative, as P04 and P05 already have. No criterion changed. FIXED.
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
