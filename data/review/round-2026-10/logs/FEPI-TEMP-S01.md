# FEPI-TEMP-S01
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (plan 1.3), applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.labs.panels.Additional` (Prolactin 38.9) | Prolactin drawn about 6 h after the event has no diagnostic value (plan fact 11, class M). | FIXED: row deleted; `abnormal_values_summary` emptied; `interpretation` "All values within reference ranges. Urine drug screen negative." |
| C | major | `ground_truth.key_clinical_evidence[0]` | Claimed the single-seizure (>=60% recurrence) rule was needed, but the HPI documents 3-4 stereotyped deja vu/epigastric auras in six months: the two-seizure criterion is met (fact 1). | FIXED: rewritten with `[ILAE_def_2014]`. |
| C | major | `ground_truth.key_clinical_evidence[2]` | "First-line ... lamotrigine, levetiracetam, oxcarbazepine, lacosamide (ILAE 2017 guideline)": no such guideline; misstated evidence (fact 6). | FIXED: lamotrigine or levetiracetam per NICE NG217, lamotrigine superior in SANAD II. |
| B | major | `initial_tool_outputs.mri.findings[0].size` | "reduced by approximately 25%" while 2.1 vs 3.4 cm3 is a 38% reduction (class U). | FIXED: "approximately 38%"; volumes and asymmetry index 0.24 kept (consistent). |
| D | minor | `initial_tool_outputs.mri.additional_observations` | "No enhancement after gadolinium administration" in an HS case (class E). | FIXED: line deleted; impression completed (loss of internal architecture, final period). |
| C | minor | `initial_tool_outputs.eeg.findings[0].morphology` | Sharp waves given a 40-70 ms duration (that is the spike range; sharp waves are 70-200 ms). | FIXED: "duration 80-120 ms", "field" instead of "dipole field". |
| C | minor | `initial_tool_outputs.eeg.findings[0].frequency` | "Frequent" with one discharge every 2-3 minutes (ACNS "occasional"). | FIXED: "about 1 to 2 per minute". |
| E | minor | `initial_tool_outputs.eeg.findings[1].morphology` | TIRDA described as "notched, semi-rhythmic". | FIXED: "Sinusoidal, monomorphic rhythmic delta activity". |
| D | minor | `initial_tool_outputs.eeg.limitations`, `.impression` | Routine-EEG limitations recommended prolonged video-EEG (class K); impression not in report form. | FIXED: limitations "Routine 40-minute recording with drowsiness and stage II sleep; no habitual event captured."; impression as a numbered ABNORMAL EEG list. |
| B | minor | `patient.neurological_exam.additional` | "No tongue bite observed" followed by a lateral tongue bite (class V). | FIXED: right lateral tongue laceration only. |
| B | minor | `patient.history_present_illness` | "denies ... similar episodes in the past" contradicts the 3-4 similar auras described in the previous sentences. | FIXED: "denies any prior convulsions or loss of consciousness other than the febrile seizures". |
| A | major | `followup_outputs[0]` (FDG-PET) | PET stored as the first follow-up, no criterion orders it (class J); asymmetry 0.78 shared with RP04. | FIXED: follow-up deleted, report moved to `fallback_tool_outputs.advanced_imaging` (modality FDG_PET) with its own ratio 0.83 and a numbered impression; avoided action `avoid-waste-5-fdg-pet` (waste, `[Willmann_2007]`) added. |
| D | major | `followup_outputs` literature (now [1]) | Source de Tisi 2011 not on the allow-list; summary listed oxcarbazepine as first-line (class O). | FIXED: results SANAD II, Wiebe 2001, ERSET 2012, Kwan 2010 with real titles; population-level summary; moved last. |
| D | minor | `followup_outputs` drug check (now [0]) | Warning cited "this patient with normal creatinine" (cross-modality). | FIXED: renal dosing stated generically; interactions name omeprazole against levetiracetam/lamotrigine and the omeprazole-phenytoin interaction. |
| A | major | `ground_truth.action_criteria` | Literature and drug check required by template; ECG required; duplicated citations; label = rationale; template evidence (classes A, B, H, T). | FIXED: order labs, ECG, MRI, routine EEG, drug check, literature; MRI and routine EEG required; labs, ECG, drug check, literature optional; one bracketed key each; case-specific rationale and evidence. |
| A | minor | `ground_truth.action_criteria[action-3-analyze-brain-mri]` | Required `{contrast: true, protocol: epilepsy}` (class E). | FIXED: `{protocol: epilepsy}`. |
| A | major | `ground_truth.sequence_constraints`, `stop_rule` | MRI -> drug check soft constraint with the shared "low-grade tumor" reason; stop rule listed literature, drug check and ECG, max 0 (classes C, D). | FIXED: constraint deleted (drug check optional); stop rule MRI and EEG, max 1. |
| C | major | `ground_truth.assessment.required_recommendations` | Process musts (routine EEG, 3T MRI), diagnostic-insight must (recognize the aura), ASM list including oxcarbazepine and lacosamide as first-line (class L). | FIXED: first-line ASM (canonical, omeprazole reason), driving (canonical), SUDEP, seizure safety and sleep. |
| C | minor | `ground_truth.assessment.prohibited_recommendations[1]` | Valproate prohibition without the MHRA 2024 rule. | FIXED: canonical text. |
| C | minor | `ground_truth.differential` | "First unprovoked seizure" left moderate after MRI and history (class P); key features not tied to results. | FIXED: first unprovoked seizure low with reason; syncope, JME, provoked seizure key features cite the ECG, EEG and labs. |
| E | minor | `ground_truth.key_clinical_evidence[3,4]` | Engineering lines "Tier per the July 2026 clinical review" and "July 2026 review applied end to end" (class G). | FIXED: deleted; added concordance, lateralization (right-hand automatisms usually ipsilateral, fact 12) and febrile-seizure antecedent lines. |
| C | minor | `ground_truth.avoided_actions` | Shared template rationales; CT waste cited AAN 2007. | FIXED: case-specific rationales; CT waste kept (back to baseline, no head injury or anticoagulation, fact 3) with `[ILAE_MRI_2019]`. |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type` (class Q/I). | FIXED: `"echo_type": "TTE"`. |
| B | minor | `metadata.difficulty_rationale` | "standard 5-tool workup" no longer true. | FIXED: "two required studies". |

## Changes, in one paragraph a physician can read before re-reviewing
The case is a 34-year-old man with months of stereotyped deja vu and rising epigastric auras and a first focal to bilateral tonic-clonic seizure; the work-up now reads optional glucose, sodium and calcium (normal) and ECG (normal sinus rhythm, 86/min), then the required epilepsy-protocol MRI (left hippocampal sclerosis, 2.1 vs 3.4 cm3, now correctly a 38% reduction, no gadolinium line) and the required routine EEG (left anterior temporal sharp waves at F7, now with a sharp-wave duration and ACNS frequency, and left TIRDA), then an optional interaction check (omeprazole does not interact with levetiracetam or lamotrigine) and an optional literature search last (SANAD II, Wiebe 2001, ERSET, Kwan 2010). The late prolactin is gone. The FDG-PET is no longer in the pathway: ordering it is waste and returns a left temporal hypometabolism report. The history no longer contradicts itself about prior episodes, and the tongue bite is a right lateral laceration. Key evidence now says the prior auras meet the two-seizure criterion and gives first-line ASM choice per NICE NG217 and SANAD II. Musts are management only: lamotrigine or levetiracetam, no driving with the licensing duty, SUDEP counselling, seizure safety and sleep; valproate is prohibited per MHRA 2024. The stop rule needs only the MRI and EEG, with one extra action allowed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Pack allow-list: `[ILAE_def_2014]`, `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[SANAD2_2021]`, `[Lateralization_2005]`, `[NICE_NG217_2025]` are used here (plan 5, request 2).
- Synonyms: none wrong for this case (left mesial TLE with HS); the idiopathic codes `G40.009`/`G40.019` in the shared list do not fit (plan 5, request 6).

## Open questions for Andrea (judgment calls you could not settle)
- None.
