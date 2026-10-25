# FTD-M09
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FTD) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes exist for FTD. The physician input is Reviewer 1's July 2026 tool rulings (`condition_tool_guidance.yaml` `ftd:`), applied through plans/FTD.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | "Tox screen ordered by police prior to transport was reported as negative" gave the result of a required step (and police do not order toxicology screens). | FIXED: sentence removed; the result is returned by the toxicology criterion. |
| D | major | `patient.neurological_exam.additional` | The exam carried the wife's history pre-scored as a numbered list of Rascovsky features ("three core changes: (1) Apathy ... (5) Repetitive behavior"), i.e. the synthesis the clinical assessment must produce. | FIXED: replaced by exam content (historian, no signs of intoxication or withdrawal). The two history items found only there (laughing at the funeral and loss of emotional cues; sexual comments to a neighbor; family covering up earlier thefts) moved into the HPI. |
| D | major | `patient.neurological_exam.mental_status`, `red_herrings[1]` | MMSE 27/30 with item losses and the estimated MoCA/clock/trails results (the clinical-assessment result) in the exam. | FIXED: scores removed from the exam and returned by `perform_clinical_assessment`; the MMSE red herring now points at `initial_tool_outputs.clinical_assessment.scores.MMSE`. |
| B | minor | `patient.neurological_exam.cranial_nerves`, `.motor`, `.reflexes` | "No primitive reflexes on cranial nerve exam" against palmomental and snout reflexes filed under motor (C14). | FIXED: primitive reflexes on the reflex line; the contradicting phrase removed. |
| A | major | `action-3-interpret-labs` | One required call had to contain twelve panels (`... tox_screen, BAL, ammonia, LFTs, RPR`); an agent ordering the toxicology screen separately could never match it; RPR required without a risk factor (NICE NG97). | FIXED: labs criterion = canonical seven panels (C4); new required criterion `action-tox-screen-blood-alcohol` (`[tox_screen, BAL]`) with keyed follow-up `request_tox_screen_bal_ammonia`. Ammonia not required (no liver disease, valproate or encephalopathy) but its value stays in the toxicology panel; RPR moved to a keyed follow-up. |
| B | major | `initial_tool_outputs.labs` | C5: folate, ALP, albumin, MCV missing; values labelled "CBC WBC"; free T4 with a normal TSH; `Reviewed_FTD_panel_additions`. | FIXED: rebuilt per C5 with the case values (Na 141, K 3.8, creatinine 1.0, BUN 18, glucose 98, calcium 9.3, Mg 2.0, TSH 2.1, B12 372, Hb 15.2, WBC 7.9, platelets 198, ALT 31, AST 28, bilirubin 0.7, ESR 11, CRP 1.6), folate, ALP, albumin, MCV added (normal); toxicology panel (negative screen, alcohol <10 mg/dL, ammonia 32) kept in the initial output because a criterion orders it; free T4 removed. |
| A | major | `initial_tool_outputs.ct` | Findings were written with MRI fields (`signal_characteristics`, `borders`), which the CT schema drops, so the served report had no finding; impression "No acute structural abnormality to account for the clinical presentation" reached across modalities; unterminated. | FIXED: one CT finding in the CT schema (frontal sulcal prominence, gyral thinning at the poles), pertinent negatives, two-line numbered impression, MRI recommendation kept (a diagnostic step). |
| D | minor | `followup_outputs` MRI | "No encephalitis signal" (diagnostic claim), em dashes, unterminated impression. | FIXED: "No mesial temporal or limbic signal abnormality"; numbered impression; substance unchanged (left > right frontal and anterior temporal atrophy, Fazekas 1, hippocampi at the lower limit of normal). |
| D | minor | `followup_outputs` neuropsych | Findings without domain keys; impression truncated ("anterior-network impairment with posterior cortical sparing") (C13). | FIXED: one domain per finding, scores unchanged; C13 canonical ending. |
| D | minor | `followup_outputs` FDG-PET, `action-6-order-advanced-imaging` | Em dashes, unterminated impression; no SPECT alternative; off-pathway advanced-imaging fallback (C6). | FIXED: FDG report reworded within the modality (values unchanged); `perfusion_SPECT` alternative with authored follow-up `request_perfusion_spect`; `fallback_tool_outputs.advanced_imaging` deleted. FDG stays optional (plan M09). |
| A | major | `action-7-search-medical-literature`, `followup_outputs` literature, `fallback_tool_outputs.literature_search` | Literature required and in the stop rule (C1). The follow-up gave a garbled Rascovsky title, unverifiable figures (diagnostic delay "median of 3-4 years", FDG "97% / 86%") and echoed the expected evidence; the fallback literature was an empty "no evidence" placeholder. | FIXED: optional, `required_arguments: {}`, last, out of the stop rule; canonical psychiatric-mimic output (C1 variant, `[Ducharme_2020]`) in `initial_tool_outputs.literature_search`; the follow-up and the fallback deleted. |
| B | minor | `fallback_tool_outputs.csf` | CSF fallback with empty `special_tests`, so an autoimmune or AD-marker LP returned no assay. | FIXED: deleted; the library answers per assay (normal). |
| B | major | `initial_tool_outputs.clinical_assessment` | C3 template: fragments cut mid-sentence ("(5) Repetitive behavior: watches the same two action films on a daily loop;"), duplicated screen lines, template impression. | FIXED: one finding per feature from the wife's history (all six present, including the executive-predominant bedside profile: clock planning and trails B failed with full orientation and one recall item lost), informant, screen (MMSE 27/30; MoCA not completed), function; 6 of 6; canonical impression. |
| C | major | `ground_truth.differential` | Mania and intoxication "high", delirium and AD "moderate" after a work-up that refutes them (C11). | FIXED: mania low (Ducharme 2020 reasoning), intoxication very low, delirium very low, AD low (optional biomarker), autoimmune encephalitis very low, vascular very low; each with the excluding data. |
| C | major | `ground_truth.assessment` | Six musts with duplicates (discharge and capacity twice), no caregiver must; template prohibitions (C9, C10). | FIXED: five musts (Rascovsky with certainty level; why mania, intoxication and delirium do not explain it; no discharge with a psychiatric label, admission or early cognitive neurology follow-up; safety and capacity including documentation for the legal process; caregiver support without ChEI or memantine). Prohibitions: the ED-discharge prohibition kept, canonical ChEI/memantine/antipsychotic texts, benzodiazepine kept. |
| C | minor | `key_clinical_evidence` | Claimed "≥5 of the 6" features "meeting probable criteria" and cited the neuropsychology before it is ordered in a way that overstated the bedside. | FIXED: five lines from the presentation and the required pathway. |
| C | minor | criteria text, citations, constraints, order | `rationale` = `label`, duplicated free-text citations, `[AAN_dementia_2018]` on labs, CT and the CT -> MRI constraint (C4, C15). | FIXED: canonical labels with case rationales; CT -> MRI soft constraint cites `[NICE_NG97]` with the canonical reason. Order (criteria and follow-ups): assessment, toxicology, labs, CT, MRI, neuropsychology, FDG/SPECT (optional), literature (optional). Stop rule = the six required criteria. |
| B | minor | `metadata` | `fallback_tool_kinds` listed deleted fallbacks; notes "First emergency-encounter FTD case in v5". | FIXED: kinds pruned; notes and difficulty rationale rewritten to the new tiers. |

## Changes, in one paragraph a physician can read before re-reviewing

A 61-year-old man brought to the emergency department after shoplifting, with an 18-month history from his wife of disinhibition, apathy, loss of empathy, stereotyped routines and sweet-food craving, dismissed from work and making impulsive financial transfers. The patient block no longer contains the toxicology result or a pre-scored feature list, and the MMSE is returned by the structured assessment (6 of 6 Rascovsky features). The required pathway is: assessment, urine toxicology and blood alcohol (negative), the reversible-cause blood panel (normal), non-contrast CT (frontal sulcal prominence only, now in a valid CT format), then MRI (left-predominant frontal and anterior temporal atrophy, posterior sparing) and neuropsychology (severe executive and social-cognition impairment, recognition preserved). Ammonia and RPR are no longer required. FDG-PET or perfusion SPECT and literature are optional. The musts ask for the Rascovsky certainty level, why mania, intoxication and delirium are excluded, no discharge with a psychiatric label, safety and capacity (driving, finances, documentation for the legal process) and caregiver support without ChEI/memantine. The differential now rates mania low and intoxication and delirium very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys used: `[NICE_NG97]`, `[SNLG_ISS_2024]`, `[Ducharme_2020]` (plan 5.2). The toxicology criterion carries no key; register an ED key (e.g. ACEP or RCEM guidance on the medical assessment of acute behavioural change) if one is wanted.

## Open questions for Andrea (judgment calls you could not settle)

None. Decision taken against the plan's wording "tox screen, BAL and ammonia stay targeted": the required toxicology criterion is `[tox_screen, BAL]`. Ammonia has no indication in a man without liver disease, valproate or encephalopathy (alert and fully oriented), so requiring it would penalise a correct omission; its result is still served if ordered.

## Verification

`perfect_agent.py FTD-M09 -v`: ok; assessment, labs and CT from `initial_tool_outputs`; toxicology, MRI and neuropsychology from `followup_outputs[0..2]`. Probed: a combined baseline-plus-toxicology order returns the baseline with the toxicology panel; ammonia alone and RPR reach their keyed follow-ups; perfusion SPECT reaches its follow-up; an autoimmune CSF order and a genetic panel reach the library (normal); any literature query returns the canonical output. `case_io.py check FTD-M09`: no failure names the case. `test_case_guards -k FTD-M09`: 2 passed.

## Verification (adversarial verifier, 24 Oct 2026)

Note: the section above was written by the worker as a self-check; this is the independent verification. Checked against the pre-round file, the plan (M09) and the whole final case: patient diff (police tox result removed from the HPI, pre-scored feature list removed from the exam with its unique history items moved into the HPI, MMSE moved to the assessment, primitive reflexes on the reflex line), the toxicology criterion `[tox_screen, BAL]` (decision to drop ammonia from the requirement is sound: alert, oriented, no liver disease or valproate), CT now in the CT schema, CT -> MRI soft constraint, 6/6 feature scoring against the history, MMSE 27/30 arithmetic (three single-point losses), laterality (left > right on MRI, FDG and SPECT), musts versus the ED-discharge prohibition (consistent), differential (mania low, intoxication and delirium very low with the excluding results) and red herring paths. MockServer probes: tox first or second, baseline, CT then MRI all reach the intended outputs.

Found: nothing that needed a change. Left as is: the FAS total of 14 at the 12th percentile (original value; plausible only with low education, which the case does not state) and the "approximately 70% sporadic" red-herring wording (original, within the range of published estimates). `perfect_agent.py FTD-M09 -v`: ok. `case_io.py check FTD-M09`: schema OK, no failure names the case. `test_case_guards -k FTD-M09`: passed.

## Close-out (24 Oct 2026)

Decisions in `plans/FTD-decisions.md`. Changes:

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (the report is a transthoracic study). The MockServer routes echo reports by this field; without it the normal TTE fallback answered a TEE order too (PATTERNS section 5; FTD added to `DISCRIMINATOR_CONDITIONS`).
- Added optional criterion `action-genetic-panel-optional` (`order_specialized_test` `genetic_panel:FTD`, `[Pottier_2016]` `[Ducharme_2020]` `[ACMG_NSGC_2011]`), placed after imaging and before any drug check or literature step, a soft constraint clinical assessment before genetics, and a negative FTD panel follow-up (`request_optional_counselled_ftd_genetics`). Reason: sporadic bvFTD with young onset (before 65); the FTD consortium advises C9orf72 screening in every possible or probable bvFTD (Ducharme 2020), so a counselled panel is a defensible order that the stop rule should not penalise, while UK eligibility (onset before 55, a suggestive family history or MND; NHS GeneTYPES) is not met, so it is optional and no counselling must is added (FTD-decisions item 7). Onset about 60.
- Synonyms (`G31.09` entry, applied with `--prune --conditions ftd`): "pick disease" and "pick's disease" (retired) and the code G31.01 are no longer accepted. Pick disease is one FTLD-tau pathology that no case establishes, and G31.01 is where ICD-10-CM codes primary progressive aphasia, so a PPA answer coded G31.01 scored as correct here.

Checks: `perfect_agent.py` and `case_io.py check` clean; `test_case_guards.py -k FTD-` passes, including `test_routed_outputs_name_their_study`.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.
- Action-tox-screen-blood-alcohol: dropped 'BAL' from the order (BAL is bronchoalveolar lavage in the vocabulary; blood alcohol is the serum ethanol of tox_screen), which the per-assay lab routing would have answered with a normal lavage.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech-language findings matching the stored neuropsychology (reduced verbal fluency; naming as tested).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status of the case's functional decline instead of Karnofsky 100.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k FTD` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
