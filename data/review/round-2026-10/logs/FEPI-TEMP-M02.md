# FEPI-TEMP-M02
Reviewer status: R1 none, R2 none (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FEPI-TEMP is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | blocker | `initial_tool_outputs.mri` (plans F, E) | Equivocal study ("questionable", "not definitively abnormal", volumetrics pending) while the label is right mesial temporal sclerosis; gadolinium lines in a non-lesional HS study. | FIXED: dedicated 3T epilepsy-protocol MRI (technique line, no contrast) with definite right HS: 2.2 vs 3.0 cm3 (27% smaller, AI 0.15 by (L-R)/(L+R)), T2/FLAIR hyperintensity, loss of internal architecture, temporal horn enlargement, slight right fornix and mammillary body volume loss; the 3 mm left frontal focus kept as nonspecific; numbered impression. |
| B | major | `initial_tool_outputs.eeg` (plan K) | Routine EEG limitations recommend "prolonged video-EEG monitoring"; essay impression. | FIXED: limitations state the recording's own limits; numbered impression with the same content (right temporal slowing, F8/T4 sharp transients of uncertain significance overlapping with wicket spikes). |
| B | major | `followup_outputs[*]` sleep-deprived EEG (plan K) | "48 hours of recording", "Only one seizure captured during 48-hour recording" and a movement artifact during "onset of automatisms" while the impression says no seizure; impression identical to M01 and RM01; interpretive `clinical_correlation`. | FIXED: about 70-minute sleep-deprived study; artifacts and symmetry rewritten; finding at F8/T2 (maximal T2); own impression including no generalized spike-and-wave; `clinical_correlation` empty; limitations "no habitual event captured". |
| D | major | `followup_outputs[0]` FDG-PET (plan J) | FDG-PET follow-up that no criterion orders. | FIXED: removed from the pathway, moved to `fallback_tool_outputs.advanced_imaging` (modality `FDG_PET`, value written as an uptake ratio; `fallback_tool_kinds.advanced_imaging: case`); avoided action `avoid-waste-5-order-advanced-imaging-fdg-pet` (waste, `[Willmann_2007]`). |
| C | major | `initial_tool_outputs.labs` (plan M) | Prolactin 27 ng/mL flagged high with no timing to any event. | FIXED: row deleted, abnormal summary emptied, interpretation "All values within normal limits." |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | Hb 12.2 with Hct 38.2 (MCHC 31.9 with a normal MCV). | FIXED: Hct 36.4 (MCHC 33.5). |
| D | minor | `initial_tool_outputs.ecg` | `clinical_correlation` about epilepsy and an interpretation about "transient loss of consciousness" (non-cardiac references). | FIXED: `clinical_correlation` empty; interpretation in cardiology terms. |
| D | major | `followup_outputs[*]` literature (plans A, O) | Required; fabricated or misattributed sources (Chen Brain 2003, Kotagal Neurology 2000 with a garbled lateralization claim, Coan 2014); empty summary. | FIXED: criterion `optional`, last; Fisher 2017, Loddenkemper and Kotagal 2005, Bernasconi 2019 with correct general content; summary written. |
| C | major | `followup_outputs[*]` drug check (plan B) | Latex contact dermatitis listed as a drug "contraindication"; "Not teratogenic category D but associated with cleft palate risk"; sumatriptan-sertraline and ibuprofen-sertraline interactions missing. | FIXED: no contraindication; interactions sertraline with sumatriptan (rare serotonin syndrome) and ibuprofen (GI bleeding), lamotrigine with sertraline; warnings on rash and titration, estrogen lowering lamotrigine, pregnancy clearance; HLA-B*15:02 before oxcarbazepine in the alternatives. Criterion `optional` with canonical evidence. |
| A | major | `ground_truth.action_criteria` (plans E, H, T) | MRI `contrast: true`; ECG required; doubled citations; rationale equal to label; template evidence. | FIXED: MRI `{protocol: epilepsy}`; ECG optional; one key per criterion; case-specific labels, rationales and evidence; order MRI, routine EEG, sleep-deprived EEG, labs, ECG, drug check, literature. |
| A | major | `ground_truth.sequence_constraints`, `stop_rule` (plans C, D) | Template MRI -> drug check constraint; stop rule with literature, drug check, ECG, max 0. | FIXED: constraint deleted (drug check optional); stop rule MRI + routine EEG, max 2. |
| C | major | `ground_truth.assessment` (plan L) | Process musts (video-EEG, 3T MRI), a diagnostic-insight must, lacosamide offered as first line; no HLA, SUDEP or valproate item although she is East Asian, has probable nocturnal convulsions, lives alone and is of childbearing potential. | FIXED: musts first-line lamotrigine or levetiracetam (anxiety, childbearing potential), contraception and folic acid, HLA-B*15:02 (canonical), driving (canonical), work and home safety, SUDEP; prohibitions ENT, LP, CT in lieu of MRI kept (em dash removed), valproate (canonical) added. |
| C | major | `ground_truth.differential` (plan P, ruling 7) | PNES `moderate` with "ruled out by video-EEG" that the case does not contain; a mimic the case raises (brother's childhood absence epilepsy and brief staring pauses at interview) missing. | FIXED: PNES `low` with the findings that exclude it; new entry "Genetic generalized epilepsy with absence seizures" `low` (G40.A09) with what raises and what excludes it; migraine and syncope key features updated. |
| D | major | `ground_truth.key_clinical_evidence` (plans G, S) | Engineering lines; "video-EEG is the gold standard" and "3T MRI is needed" claims for studies the case does not serve. | FIXED: six case-specific items, including the probable nocturnal convulsions and the two-seizure definition. |
| C | minor | `ground_truth.red_herrings` | None defined although the case carries two. | FIXED: added the sibling's absence epilepsy (`patient.clinical_history.family_history[2]`) and the equivocal routine EEG (`initial_tool_outputs.eeg.impression`); paths checked. |
| C | minor | `ground_truth.avoided_actions` (plan I) | Template rationales. | FIXED: case-specific rationales; CT waste kept (back to baseline, no injury, MRI available) with `[ILAE_MRI_2019]`. |
| A | minor | `fallback_tool_outputs.echo` (plan Q) | No `echo_type`. | FIXED: `TTE`. |
| C | minor | `patient.history_present_illness` | Left-hand manual automatisms with a right temporal focus. | FLAGGED, not changed: weak lateralizing sign alone; no field uses it for localization. |
| E | minor | `metadata.difficulty_rationale`, `estimated_complexity`, `revision_reason`, `last_revised` | Template text ("five required tools", video-EEG follow-up). | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The scored MRI is now a dedicated 3T epilepsy-protocol study with definite right hippocampal sclerosis (2.2 vs 3.0 cm3, T2/FLAIR signal, lost internal architecture) and no contrast. The routine EEG stays equivocal (right temporal slowing, F8/T4 sharp transients that overlap with wicket spikes) and no longer recommends video monitoring; the recommended sleep-deprived EEG now reads as a sleep-deprived study (no 48-hour recording, no captured seizure) with right anterior temporal sharp waves and no generalized spike-and-wave. FDG-PET left the pathway (waste; served as a fallback). Prolactin was removed and the hematocrit corrected. Labs, ECG, drug check and literature are optional; the drug check now reports the real sertraline interactions with sumatriptan and ibuprofen and drops the latex "contraindication". Musts: lamotrigine or levetiracetam, contraception and folic acid, HLA-B*15:02 before carbamazepine or oxcarbazepine, driving, safety at work and at home, SUDEP (probable nocturnal convulsions, lives alone); valproate is prohibited. PNES is `low`, and genetic generalized epilepsy (her brother's absence epilepsy, brief staring pauses) is added as a `low` mimic and a red herring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys outside the pack allow-list used per plan 1.1: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`, `[Lateralization_2005]`.
- Synonyms and ICD list (plan 5.6): inherited `G40.219` and idiopathic `G40.009`/`G40.019` do not fit.

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial check, 24 Oct 2026 (case committed in b8be2153; read in full).
- Checked: MRI volumetry (2.2/3.0 cm3 = 27% smaller, index 0.15), CBC (Hct 36.4, MCHC 33.5), prolactin gone, PET only as fallback with the waste avoided action, both EEG reports internally consistent (no 48-hour or captured-event text), drug check content matches the medication list (sertraline, sumatriptan, ibuprofen) and the latex allergy is no longer a drug contraindication, HLA-B*15:02 must present (East Asian), new GGE differential and red herrings point at existing fields with matching data points, tiers and stop rule per plan, criteria evidence equals stored values (ECG 76/min, labs 83/138/9.2).
- Found: as in M01, the last C row misreads the sign: left-hand automatisms with a right temporal focus are ipsilateral and therefore concordant (fact 12); the HPI needed no change. A stored `fallback_tool_outputs.ecg` differs from the initial ECG; it is never served while the initial ECG exists, so it was left.
- Changed: nothing in the case. Checks clean for this case.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `initial_tool_outputs.ecg`: rate and intervals (76/min, PR 154, QRS 86, QTc 416) were identical to RM04 and S05; now 72/min (triage HR 73), PR 158, QRS 80, QTc 434; ECG criterion evidence updated.

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added), mesial temporal sclerosis epilepsy; removed focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that contradicts this case now get a case-specific report (term: gist, where stored):

- analyze_eeg ambulatory: This is an ABNORMAL 48-hour ambulatory EEG due to: 1. Right anterior temporal sharp waves (phase reversal at F8), maximal in NREM sleep. 2. Intermitte (fallback_tool_outputs.eeg)
- analyze_eeg video: This is an ABNORMAL 72-hour video-EEG due to: 1. Right anterior temporal sharp waves (phase reversal at F8), maximal in NREM sleep. 2. Intermittent ri (followup request_video_eeg)
- obtain_tissue_diagnosis resection: Hippocampal sclerosis, ILAE type 1 (fallback_tool_outputs.tissue_diagnosis)
- obtain_tissue_diagnosis stereotactic_biopsy: Hippocampal neuronal loss with fibrillary gliosis (followup request_stereotactic_biopsy)
- obtain_tissue_diagnosis open_biopsy: Hippocampal neuronal loss with fibrillary gliosis (followup request_open_biopsy)
- order_specialized_test neuropsych_battery: Weakness in visual learning and delayed visual recall (T-scores 36 and 34) with verbal memory and naming within the average range and intellectual fun (fallback_tool_outputs.specialized_test)
- interpret_labs AED_levels: No levetiracetam, valproate, carbamazepine, phenytoin, lamotrigine or lacosamide detected. (fallback_tool_outputs.labs[AED_levels], also answers valproate_level)

Checks: `perfect_agent.py` passes; the criterion snapshot of the case is unchanged; `pytest agent-platform/tests -k FEPI-TEMP` (case guards included), `test_reports_do_not_fabricate.py` and `apply_diagnosis_synonyms.py --check` pass; no new report repeats a 60-character window of any criterion's expected evidence.
