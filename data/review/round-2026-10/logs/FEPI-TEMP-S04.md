# FEPI-TEMP-S04
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FEPI-TEMP) | Approved before this round: no

Note: the edit was started in an earlier run that stopped at the usage limit before the log was written. This run re-read the whole case against the HEAD version, verified every change below, completed it (one further fix, the anxiety history) and ran the checks.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (plan 1.3), applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.clinical_history.social_history.occupation` | "restaurant manager" against "restaurant worker" in the HPI (class R). | FIXED: "restaurant worker". |
| B | minor | `patient.demographics.ethnicity` | "East Asian" for a patient with a Lao surname (Chanthavong); the HLA-B*15:02 indication is the same for East and Southeast Asian ancestry. | FIXED: "Southeast Asian (Lao)"; drug output and KCE say Southeast Asian. |
| B | minor | `patient.history_present_illness` | Left-hand automatisms (usually ipsilateral, fact 12) against right HS and a right temporal EEG focus in a concordant straightforward case. | FIXED: "her right hand picked repetitively at her apron"; nothing else in the HPI changed. |
| B | minor | `patient.clinical_history.past_medical_history[3]` | "Anxiety disorder ... managed with counseling" while the medication list has sertraline for generalized anxiety disorder. | FIXED: "Generalized anxiety disorder diagnosed at age 17, managed with counseling and sertraline". |
| C | major | `initial_tool_outputs.labs.panels.Additional` (Prolactin 38.8) | Prolactin drawn about 8 h after the event has no value (class M, fact 11). | FIXED: row deleted; abnormal summary and interpretation updated. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` (Hematocrit) | Hematocrit 35.7% flagged low with hemoglobin 14.2 g/dL (impossible pair; Hct is about 3 x Hb). | FIXED: Hematocrit 42.1%, not abnormal; interpretation "All values within reference ranges". |
| D | minor | `initial_tool_outputs.mri.additional_observations`, `.findings[0].borders` | Gadolinium lines in an HS case (class E). | FIXED: "No pathological enhancement following gadolinium" deleted; borders "Well-defined volume loss without an associated mass". |
| B | minor | `initial_tool_outputs.mri.findings[0].size`, `.volumetrics` | "Reduced by approximately 30%" against 1.9 vs 3.3 cm3 (42%); 1.9 cm3 shared with RS04 and RS05 (class U). | FIXED: right 1.8 cm3 (unique in the condition), "approximately 45%" (1 - 1.8/3.3), asymmetry index 0.29 ((3.3 - 1.8)/(3.3 + 1.8)); impression rewritten with atrophy, loss of internal architecture and T2/FLAIR hyperintensity. |
| D | minor | `initial_tool_outputs.eeg.limitations` | Recommended prolonged video-EEG (class K). | FIXED: "Routine 45-minute recording with drowsiness and stage II sleep; no habitual event captured." |
| B | minor | `initial_tool_outputs.eeg.findings` | "Frequent" at 8-10 per hour (ACNS 2021: occasional); "dipole field"; TIRDA "semi-rhythmic". | FIXED: "Occasional, approximately 15-20 per hour"; "field extending to T4 and F4"; "Sinusoidal, monomorphic rhythmic delta activity without evolution"; numbered ABNORMAL EEG impression. |
| A | major | `followup_outputs[0]` (FDG-PET) | PET follow-up no criterion orders (class J). | FIXED: follow-up deleted; report moved to `fallback_tool_outputs.advanced_imaging` (`modality: FDG_PET`, ratio 0.79, no MRI references); avoided action `avoid-waste-5-fdg-pet` (waste, `[Willmann_2007]`). |
| C | major | `followup_outputs` drug check (now [0]) | "Lamotrigine does not interact with oral contraceptives" is wrong (fact 8); warning cited the creatinine value (cross-modality). | FIXED: ethinylestradiol roughly halves lamotrigine (levels rise in the pill-free week); oxcarbazepine reduces pill efficacy; inducers lower sertraline; generic renal dosing line; HLA-B*15:02 warning before carbamazepine or oxcarbazepine. |
| D | major | `followup_outputs` literature (now [1]) | Zupanc 2006 and Tomson Lancet Neurol 2019 not verifiable (class O); Wiebe 2001 title wrong; summary in policy voice. | FIXED: Sabers 2003 (Neurology 61:570-571), Tomson 2018 EURAP (Lancet Neurol 17:530-538, malformation rates as published), Wiebe 2001 with its real title; general summary; last in the pathway. |
| A | major | `ground_truth.action_criteria` | Literature, drug check, ECG required with template text and doubled citations; MRI `{contrast: true, protocol: epilepsy}` (classes A, B, E, H, T). | FIXED: order labs, ECG, MRI, routine EEG, drug check, literature; MRI `{protocol: epilepsy}`, routine EEG and drug check (combined pill, fact 8) required; labs, ECG, literature optional; one bracketed key each; case-specific evidence and rationale. |
| A | major | `ground_truth.sequence_constraints`, `.stop_rule` | Template MRI -> drug check reason; stop rule with literature and ECG, max 0 (classes C, D). | FIXED: constraint kept (drug check required) with the canonical reason and `[NICE_NG217_2025]`; stop rule MRI, EEG, drug check, max 1. |
| C | major | `ground_truth.assessment` | Process musts (3T MRI, routine EEG, recognise the aura); vague ASM and counselling musts (class L). | FIXED: musts first-line lamotrigine or levetiracetam with the pill interaction, contraception and folic acid, HLA-B*15:02, kitchen and work safety, driving, SUDEP; prohibitions valproate (canonical MHRA 2024 text), LP without indication, no enzyme-inducing ASM while relying on the combined pill. |
| C | minor | `ground_truth.differential` | Tumor `moderate` after an MRI with HS and no mass (class P); entries without the excluding findings. | FIXED: tumor low; JME, provoked seizure low and PNES, convulsive syncope very_low, each with the findings that exclude it. |
| E | minor | `ground_truth.key_clinical_evidence` | Engineering lines (class G) and generic text. | FIXED: two-seizure criterion from the prior auras, concordance, febrile seizure antecedent, pill interaction, HLA. |
| C | minor | `ground_truth.avoided_actions` | Template rationales. | FIXED: case-specific; CT waste kept (back to baseline, no injury, no anticoagulation) with `[ILAE_MRI_2019]`. |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type` (class I). | FIXED: "TTE". |

## Changes, in one paragraph a physician can read before re-reviewing
Ms. Chanthavong, a 19-year-old left-handed Lao restaurant worker on sertraline and a combined ethinylestradiol pill, has eight months of olfactory auras with nausea, some with impaired awareness, and a first focal to bilateral tonic-clonic seizure; her manual automatisms are now right-sided, concordant with the right hippocampal sclerosis on the epilepsy-protocol MRI (right hippocampus 1.8 vs 3.3 cm3, about 45% smaller, asymmetry index 0.29; no gadolinium lines) and the right anterior temporal spikes with phase reversal at F8 and TIRDA on the routine EEG. The late prolactin is gone and an impossible hematocrit was corrected; labs and ECG are normal and optional. Required: MRI, routine EEG and the interaction check, whose output now states correctly that ethinylestradiol roughly halves lamotrigine and that oxcarbazepine makes the pill unreliable. FDG-PET became waste and its report a case fallback. Musts: lamotrigine (higher dose) or levetiracetam (mood monitoring), contraception and folic acid, HLA-B*15:02 before carbamazepine or oxcarbazepine, kitchen safety, driving, SUDEP; valproate and enzyme inducers are prohibited. The literature output cites only verifiable sources.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Pack allow-list: `[ILAE_def_2014]`, `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[Sabers_2003]`, `[EURAP_2018]`, `[CPIC_2018]`, `[NICE_NG217_2025]` (plan 5, request 2).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Adversarial check (24 Oct 2026) of the final case against this log, `git diff` and plan section 4 (S04).
- Confirmed: occupation; ethnicity Southeast Asian (Lao) fits the surname and keeps the HLA-B*15:02 indication (CPIC 2018); right-hand automatisms concordant; Hct 42.1 with Hb 14.2; volumes 1.8 vs 3.3 cm3 give 45% and index 0.29, 1.8 unique in the condition; no gadolinium lines; "occasional" at 15-20/h fits ACNS 2021; drug output now correct on ethinylestradiol and lamotrigine (fact 8); drug check required, soft MRI -> drug check, stop rule MRI, EEG, drug check, max 1; EURAP 2018 and Sabers 2003 figures correct; musts (contraception, folic acid, HLA, kitchen safety, driving, SUDEP) consistent with the penicillin allergy and medicines; case guards pass.
- Found: the ECG (rate 80, PR 148, QRS 82 ms) was the same template as S02's. Changed `initial_tool_outputs.ecg.rate` to 76, `.intervals.PR` 136 ms, `.intervals.QRS` 88 ms, `.interpretation` "at 76 bpm", and the ECG criterion `expected_evidence` to match (triage HR 78 stays).
- `perfect_agent.py -v` and `case_io.py check` clean for the case.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-7-interpret-labs.rationale`: engineering prefix or tier wording removed (was "A first convulsion warrants a check for ...").
- Differential "Idiopathic generalized epilepsy (JME)": ICD-10-CM G40.319 -> G40.B09.
