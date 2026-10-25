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

## Verification
Adversarial check (24 Oct 2026) of the whole final case against this log, plan section 4 (S01) and classes A-V; diff read against fa1d22e6 (the case was checkpointed in b8be2153).
- Confirmed: prolactin gone everywhere; volumetrics 2.1 vs 3.4 cm3 give 38% and index 0.24; no gadolinium line; sharp-wave duration and "frequent" at 1-2/min agree with ACNS 2021; tongue-bite contradiction resolved; HPI no longer denies the auras; KCE two-seizure criterion and first-line ASM per facts 1 and 6; tiers, criteria order, stop rule (MRI, EEG, max 1), no constraint with an optional drug check; FDG_PET waste and PET as fallback; echo_type; literature sources real and summaries correct (SANAD II, Wiebe 2001, ERSET 2012, Kwan 2010), no leakage (case guards pass); differential matches the results; musts and prohibitions consistent with the omeprazole-only medication list and the ACE-inhibitor allergy.
- Found: the fallback FDG-PET ratio the worker chose (0.83) duplicates P01's ratio. Changed: `fallback_tool_outputs.advanced_imaging.findings[0].signal` and `.impression` to 0.77 (unused in the condition, consistent with "markedly reduced").
- `perfect_agent.py -v` and `case_io.py check` clean for the case.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-7-interpret-labs.rationale`: engineering prefix or tier wording removed (was "A first convulsion in the emergency depa...").
- `action-5-check-drug-interactions.rationale`: engineering prefix or tier wording removed (was "The only regular medicine is omeprazole,...").
- Differential "Primary generalized epilepsy (JME)": ICD-10-CM G40.319 -> G40.B09.
- Literature follow-up query named "mesial temporal sclerosis" (this case's MRI finding); now "temporal lobe epilepsy treatment outcomes".

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added), mesial temporal sclerosis epilepsy; removed focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that contradicts this case now get a case-specific report (term: gist, where stored):

- analyze_eeg ambulatory: This is an ABNORMAL 48-hour ambulatory EEG due to: 1. Left anterior temporal sharp waves (phase reversal at F7), maximal in NREM sleep. 2. Left tempor (fallback_tool_outputs.eeg)
- analyze_eeg video: This is an ABNORMAL 72-hour video-EEG due to: 1. Left anterior temporal sharp waves (phase reversal at F7), maximal in NREM sleep. 2. Left temporal in (followup request_video_eeg)
- obtain_tissue_diagnosis resection: Hippocampal sclerosis, ILAE type 1 (fallback_tool_outputs.tissue_diagnosis)
- obtain_tissue_diagnosis stereotactic_biopsy: Hippocampal neuronal loss with fibrillary gliosis (followup request_stereotactic_biopsy)
- obtain_tissue_diagnosis open_biopsy: Hippocampal neuronal loss with fibrillary gliosis (followup request_open_biopsy)
- order_specialized_test neuropsych_battery: Weakness in verbal learning and delayed verbal recall (T-scores 37 and 34) with visual memory within the average range and intellectual functioning in (fallback_tool_outputs.specialized_test)
- interpret_labs AED_levels: No levetiracetam, valproate, carbamazepine, phenytoin, lamotrigine or lacosamide detected. (fallback_tool_outputs.labs[AED_levels], also answers valproate_level)

Checks: `perfect_agent.py` passes; the criterion snapshot of the case is unchanged; `pytest agent-platform/tests -k FEPI-TEMP` (case guards included), `test_reports_do_not_fabricate.py` and `apply_diagnosis_synonyms.py --check` pass; no new report repeats a 60-character window of any criterion's expected evidence.
