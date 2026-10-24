# FTD-S09
Reviewer status: R1 none, R2 none (FTD has no notes file; the binding clinician input is Reviewer 1's July 2026 tool rulings under `ftd:` in condition_tool_guidance.yaml) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No notes file exists for FTD. The plan's classes (C1-C15) were applied as class rulings (ROUND_POLICY ruling 2); every change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C/D | major | ground_truth.action_criteria[action-7-search-medical-literature]; followup_outputs[request_literature_driving_ftd] | Literature required and in the stop rule with the "Confirms Rascovsky..." expected evidence; driving-safety essay as the only literature output (C1) | FIXED: optional, last, any query, out of `required_before_assessment`; driving follow-up deleted (driving is in the safety must); canonical bvFTD text in `initial_tool_outputs.literature_search` |
| C/D | major | followup_outputs[request_drug_interactions]; ground_truth.action_criteria[action-8-check-drug-interactions] | `proposed` was a dose plan ("Sertraline 50 mg and trazodone 50 mg"), quetiapine as alternative, ChEI "contraindicated"; thiazide interaction called "low"; criterion required an exact `indication` string no agent would type; expected evidence "AChE inhibitors flagged" (C2) | FIXED: keyed follow-ups `request_sertraline_interactions` (thiazide hyponatraemia with sodium check, levothyroxine no interaction, alcohol additive sedation; MAOI contraindication; hyponatraemia and QT warnings) and `request_trazodone_interactions` (alcohol sedation and falls, thiazide orthostasis, QT, priapism); criterion optional, `{"drug": "sertraline"}`, placed after the diagnostic criteria; probed: each drug receives its own report |
| C | major | ground_truth (assessment, differential, red_herrings) | Wine escalated to about 6 glasses a day with impulsive driving and crashes, never addressed: no alcohol must, no alcohol-related mimic in the differential | FIXED: must on alcohol (why it does not explain the syndrome, supervised reduction, husband controls access, oral thiamine); differential "Alcohol-related brain damage" low with for/against; red herring on the alcohol line (increased alcohol is a Rascovsky dietary change); MRI now states normal cerebellar volume |
| B | major | initial_tool_outputs.clinical_assessment | Hyperorality evidenced by the restaurant-decisions sentence; perseveration by an exam fragment; duplicated "Bedside cognitive testing"; templated impression (C3) | FIXED: rebuilt: 4 of 6 features (disinhibition, compulsions, hyperorality incl. alcohol, executive profile); apathy absent; empathy loss not described (the husband reports loss of insight, not of warmth); MMSE 20/30 itemised (serial sevens 0/5, recall 2/3, orientation 8/10, command 2/3, sentence 0/1); canonical impression |
| D | minor | patient.neurological_exam.mental_status; patient.history_present_illness | MMSE, FAB, fluency upfront; "Thyroid function was checked by PCP and is normal" while TSH is a scored required test | FIXED: scores moved to the assessment and battery; the PCP thyroid sentence removed (the PMH still says "well-controlled") |
| E/D | minor | initial_tool_outputs.mri.volumetrics.frontal_lobes | "most severe case in series": engineering text in a report | FIXED: "25% below norms" |
| C | minor | initial_tool_outputs.mri | No exclusion statements | FIXED: no mass, haemorrhage, hydrocephalus, infarct or restricted diffusion; normal cerebellum; Fazekas 1 |
| B/C | major | initial_tool_outputs.labs | No folate, calcium, LFTs, albumin, platelets; `Reviewed_FTD_panel_additions`; copper; RPR/HIV under "Vitamins" (C5) | FIXED: five panels, existing values kept (MCV 98 high-normal, Na 138 on the thiazide), eGFR 84 (creatinine 0.8, female 61), calcium 9.8; copper deleted; RPR/HIV keyed follow-up with baseline plus serology |
| D/E | minor | followup_outputs[request_reviewed_neuropsych_battery].output | Truncated impression (C13) | FIXED: domains with visuospatial and language added; canonical ending |
| B/C | major | fallback_tool_outputs.ct, .advanced_imaging | Normal CT; unguarded advanced-imaging fallback (C6) | FIXED: CT with marked bifrontal and anterior temporal atrophy; advanced fallback deleted; fallback kinds updated |
| C | minor | ground_truth.action_criteria[action-6-order-advanced-imaging]; followup_outputs | No SPECT alternative; FDG em dash | FIXED: SPECT alternative and matching report; optional |
| C/A | minor | ground_truth.action_criteria[*] | Rationale = label; duplicate citations; `[AAN_dementia_2018]`; "RPR/HIV per risk" (C4) | FIXED: canonical labels; tailored lab and MRI rationales (thiazide, thyroid, alcohol); bracketed keys; avoided CT `[NICE_NG97]`; order assessment, battery, labs, MRI, FDG, drug check, literature |
| C | major | ground_truth.assessment.required_recommendations | Template block duplicated; genetic counselling must in a sporadic case with no genetics criterion; driving only as generic "capacity" despite crashes (C9) | FIXED: five musts: Rascovsky; alcohol mimic and management; stop driving now plus finances, kitchen and fire safety, LPA; caregiver plan with supervised food and alcohol and SSRI option, no ChEI or memantine; advance care planning. Counselling must removed: no family history (mother well at 84) and no genetics criterion |
| C | minor | ground_truth.assessment.prohibited_recommendations[0,1]; key_clinical_evidence | Overstated ChEI/memantine wording; KCE "AChE inhibitors are contraindicated" (C10) | FIXED: canonical prohibitions; KCE "not recommended (NICE NG97)" |
| C | major | ground_truth.differential | AD moderate "biomarker testing distinguishes" with no biomarker in the pathway (C11) | FIXED: alcohol low, AD low, psychiatric, NPH and vascular very low, each with reasons; FTD-MND dropped (no motor signs, nothing raises it) |
| C/D | minor | ground_truth.key_clinical_evidence; red_herrings[0] | "Imaging confirms" verdict; non-canonical rigidity text (C8 keeps it in S09, advanced) | FIXED: KCE lists features, decline, MRI, normal labs on thiazide and levothyroxine, canonical rigidity line; red herring canonical interpretation |

## Changes, in one paragraph a physician can read before re-reviewing
The case now deals with the patient's new heavy drinking (about 6 glasses of wine a day): it is scored as a bvFTD dietary change, kept in the differential as alcohol-related brain damage (low: lobar knife-blade atrophy, normal cerebellum, intact coordination), and managed in a must (supervised reduction, husband controls access, thiamine). Driving cessation is explicit after several crashes. The clinical-assessment report was rebuilt (four features, MMSE 20/30 itemised); exam scores and the PCP thyroid result were removed from the patient block. Literature is optional background; the drug check is optional and returns proper reports for sertraline (thiazide hyponatraemia, alcohol) or trazodone. Labs cover the NICE NG97 panel; serology only when ordered. MRI reports exclusions and no cerebellar atrophy; the engineering phrase "most severe case in series" is gone. The CT fallback shows the atrophy; FDG-PET or SPECT is optional with matching reports. The genetic-counselling template must was dropped (no family history, no genetics step).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys `[SNLG_ISS_2024]` per plan section 5.2.
- `accepted[0]` reads "Behavioral variant frontotemporal dementia (bvFTD), probable, sporadic — advanced stage" with an em dash; not edited (rule 3). Cosmetic only (matching ignores punctuation).
- MockServer: a drug check with no initial output serves the first unserved follow-up for any drug, so a citalopram check here receives the sertraline report. Consider a `drug` discriminator for `check_drug_interactions` follow-ups.

## Open questions for Andrea (judgment calls you could not settle)
- None. Note for the lead: "advanced stage" in the label after a 2-year course with MMSE 20/30 is generous but defensible given very severe atrophy and loss of independent function; not changed.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: 4 of 6 features (empathy "not described" is defensible from the HPI, which reports lack of distress and insight, not loss of warmth) agree with `criteria_met`; MMSE 20/30 adds up (serial sevens -5, recall -1, orientation -2, command -1, sentence -1); onset age 59 consistent; eGFR 84 matches creatinine 0.8, female 61; sodium 138 on the thiazide; drug-check follow-ups probed: sertraline and trazodone each receive their own report, contents correct (thiazide plus SSRI hyponatraemia, trazodone orthostasis/QT/priapism, no doses, no ChEI text); alcohol mimic, must and red herring consistent with the social history and MRI (normal cerebellum); genetics absent and the counselling must correctly dropped (no family history); FDG/SPECT authored; KCE ChEI wording per C10. The em dash in `accepted[0]` is pre-existing and correctly left (rule 3). perfect_agent and case_io check clean; case guards pass. No errors found; no changes made.

## Condition audit (FTD auditor, 24 Oct 2026)

- E, minor, `initial_tool_outputs.literature_search[*].results[*].source`: the sources were citation keys (`[Rascovsky_2011]` or `Rascovsky_2011`), which a literature tool does not return, and the condition used three styles. They now give the full reference, as in M07-P02 (for example "Rascovsky K et al. Brain 2011;134:2456-2477 (FTDC criteria for bvFTD)"). Findings and summary are unchanged. FIXED.
- `perfect_agent.py` and `case_io.py check` were re-run on all 30 FTD cases after the changes and are clean; `test_case_guards.py -k FTD` passes (60 tests).

## Close-out (24 Oct 2026)

Decisions in `plans/FTD-decisions.md`. Changes:

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (the report is a transthoracic study). The MockServer routes echo reports by this field; without it the normal TTE fallback answered a TEE order too (PATTERNS section 5; FTD added to `DISCRIMINATOR_CONDITIONS`).
- `ground_truth.diagnosis.accepted[0]`: the em dash replaced by a comma (house style; token matching ignores punctuation, so scoring is unchanged).
- Added optional criterion `action-genetic-panel-optional` (`order_specialized_test` `genetic_panel:FTD`, `[Pottier_2016]` `[Ducharme_2020]` `[ACMG_NSGC_2011]`), placed after imaging and before any drug check or literature step, a soft constraint clinical assessment before genetics, and a negative FTD panel follow-up (`request_optional_counselled_ftd_genetics`). Reason: sporadic bvFTD with young onset (before 65); the FTD consortium advises C9orf72 screening in every possible or probable bvFTD (Ducharme 2020), so a counselled panel is a defensible order that the stop rule should not penalise, while UK eligibility (onset before 55, a suggestive family history or MND; NHS GeneTYPES) is not met, so it is optional and no counselling must is added (FTD-decisions item 7). Onset about 59.
- Synonyms (`G31.09` entry, applied with `--prune --conditions ftd`): "pick disease" and "pick's disease" (retired) and the code G31.01 are no longer accepted. Pick disease is one FTLD-tau pathology that no case establishes, and G31.01 is where ICD-10-CM codes primary progressive aphasia, so a PPA answer coded G31.01 scored as correct here.

Checks: `perfect_agent.py` and `case_io.py check` clean; `test_case_guards.py -k FTD-` passes, including `test_routed_outputs_name_their_study`.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
