# FEPI-TEMP-M03
Reviewer status: R1 none, R2 none (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FEPI-TEMP is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.history_present_illness` (plan R) | Surname Kapoor shared with S03 and S06 and not fitting the recorded Caucasian ethnicity; "he describes his suddenly becoming unresponsive" for an event his wife witnessed. | FIXED: "Mr. Barlow" (no other case uses it); "she describes him suddenly becoming unresponsive". |
| B | blocker | `initial_tool_outputs.mri` (plans F, E) | Equivocal study ("questionable", "could represent early sclerosis versus normal variant", AI 0.08 below threshold) while the label is right mesial temporal sclerosis; gadolinium line; white matter foci "related to migraine" in a man without migraine. | FIXED: dedicated 3T epilepsy-protocol MRI (technique line, no contrast) with mild but definite right HS (2.7 vs 3.4 cm3, 21% smaller, AI 0.11; reproducible T2/FLAIR hyperintensity of the body, subtle loss of internal architecture); periventricular foci kept as nonspecific; numbered impression. |
| B | blocker | `followup_outputs[*]` sleep-deprived EEG (plan K) | `classification: abnormal` with a "Normal" impression and no findings; "96 hours" of sleep and "Only one clinical event captured despite 96 hours"; impression identical to RP02 with a teaching sentence. | FIXED: `classification: normal`; 75-minute sleep-deprived study; own impression; limitations "no habitual event captured". |
| B | blocker | `followup_outputs[*]` ambulatory EEG (plan K) | "48-hour 48-hour" impression, "96 hours" in the limitations, seizure "on day 3" of a 48-hour study; location "evolving to right hemispheric then bilateral" against "remaining lateralized" and "No bilateral evolution"; interictal rate (5-6/h in NREM) hard to reconcile with a normal sleep-deprived EEG. | FIXED: 72-hour ambulatory EEG, seizure on day 3 with push-button and diary semiology, spread to F4 only, "no spread to the left hemisphere"; interictal sharp waves 1-2/h in NREM; numbered impression; limitations name the lack of video. |
| E | minor | `initial_tool_outputs.eeg` | Impression without ABNORMAL opening or final period. | FIXED: numbered impression with the same content; limitations reworded without "recording duration insufficient" advice. |
| D | major | `followup_outputs[0]` FDG-PET (plan J) | FDG-PET follow-up that no criterion orders. | FIXED: moved to `fallback_tool_outputs.advanced_imaging` (modality `FDG_PET`, uptake ratio 0.84 so it no longer equals M02's 0.82; `fallback_tool_kinds.advanced_imaging: case`); avoided action FDG_PET waste `[Willmann_2007]`. |
| C | major | `initial_tool_outputs.labs` (plan M) | Prolactin row with no relation to an event. | FIXED: deleted. |
| B | major | `initial_tool_outputs.labs.panels` | Chloride 112 with sodium 137 and bicarbonate 23 (anion gap 2); female hemoglobin and hematocrit ranges in a man; Hb 13.8 with Hct 36.0 (MCHC 38). | FIXED: chloride 103 (gap 11, normal); Hb 14.6 g/dL (13.5-17.5), Hct 43.5% (41.0-53.0), MCHC 33.6; abnormal summary and interpretation now glucose, magnesium and vitamin D only. |
| B | minor | `initial_tool_outputs.ecg.intervals.QTc` | Interval set nearly identical to M01 (QTc 418). | FIXED: QTc 409 ms. |
| D | major | `followup_outputs[*]` literature (plans A, O) | Required; Bernasconi Ann Neurol 2003, Coan 2014 and LoPinto-Khoury 2012 cited with invented titles and figures. | FIXED: optional, last; Bernasconi 2019, Blumcke 2013 (HS classification), Willmann 2007, general content. |
| C | major | `followup_outputs[*]` drug check (plan B) | Sulfonamide allergy discussed as a lamotrigine issue; duplicated SJS warnings; no mention of the drug the allergy actually excludes (zonisamide). | FIXED: zonisamide contraindication; lamotrigine with sertraline, metformin, vitamin D; carbamazepine lowering sertraline and topiramate with metformin; one rash warning. Criterion optional, canonical evidence. |
| A | major | `ground_truth.action_criteria` (plans E, H, T, 3.2) | MRI `contrast: true`; ECG required; doubled citations; template evidence. | FIXED: MRI `{protocol: epilepsy}`; ECG optional; sleep-deprived and ambulatory EEG recommended with evidence from their reports; labs rationale names metformin; order MRI, routine, sleep-deprived, ambulatory EEG, labs, ECG, drug check, literature. |
| A | major | `ground_truth.sequence_constraints`, `stop_rule` (plans C, D) | Template constraint; stop rule with literature, drug check and ECG, max 0. | FIXED: constraint deleted; stop rule MRI + routine EEG, max 2. |
| C | major | `ground_truth.assessment` (plan L) | Process musts (video-EEG, 3T MRI), a diagnostic-insight must, a vague ASM must; nothing on his untreated OSA, chemistry laboratory or sulfonamide allergy. | FIXED: musts first-line lamotrigine or levetiracetam (anxiety, no interactions), OSA treatment and sleep, driving (canonical), laboratory safety, SUDEP; prohibitions LP, normal sleep-deprived EEG not excluding epilepsy, zonisamide (sulfonamide allergy), valproate (canonical). |
| C | major | `ground_truth.differential` (plan P) | PNES `moderate` "distinguished by video-EEG" that the case does not contain; untreated OSA raised by the history but absent. | FIXED: PNES `low` (ambulatory EEG captured a right temporal seizure); OSA microsleeps added `low`; absence, frontal and syncope entries cite the case results. |
| D | major | `ground_truth.key_clinical_evidence` (plans G, S) | Engineering lines; "3T", "cross-modal concordance is the gold standard before surgical evaluation". | FIXED: five case-specific items. |
| C | minor | `ground_truth.red_herrings` | None defined. | FIXED: untreated OSA (`patient.clinical_history.past_medical_history[1]`) and the normal sleep-deprived EEG (`followup_outputs[0].output.impression`); paths checked after the reorder. |
| C | minor | `ground_truth.avoided_actions` (plan I) | Template rationales. | FIXED: case-specific; CT waste kept (elective, no injury, MRI available). |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type`. | FIXED: `TTE`. |
| E | minor | `metadata` | Template difficulty text. | FIXED: rationale, complexity, revision reason, last revised. |

## Changes, in one paragraph a physician can read before re-reviewing

The patient is now Mr. Barlow. The scored MRI is a dedicated 3T epilepsy-protocol study with mild but definite right hippocampal sclerosis (2.7 vs 3.4 cm3, reproducible T2/FLAIR signal) and no contrast. The EEG pathway is now coherent: an equivocal routine EEG (required), a normal sleep-deprived EEG (recommended; the 96-hour and captured-event text is gone), and a 72-hour ambulatory EEG (recommended) that records a habitual event on day 3 with right anterior temporal onset that stays in the right hemisphere, plus occasional F8/T4 sharp waves. FDG-PET left the pathway (waste; served as a fallback). Prolactin was removed; the chloride, male CBC ranges and MCHC were corrected. Labs, ECG, drug check and literature are optional; the drug check now says that his sulfonamide allergy excludes zonisamide. Musts: lamotrigine or levetiracetam, treat the sleep apnea, driving, laboratory safety, SUDEP; prohibitions add zonisamide and valproate. PNES is `low`; OSA microsleeps are added as a `low` mimic and a red herring, with the normal sleep-deprived EEG as the second red herring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys outside the pack allow-list used per plan 1.1: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`.
- Synonyms and ICD list (plan 5.6): inherited `G40.219` and idiopathic `G40.009`/`G40.019` do not fit.
- Label wording "subtle mesial temporal sclerosis" is kept (the MRI now calls it mild); no change requested.

## Open questions for Andrea (judgment calls you could not settle)

None. Decision: the ambulatory study is 72 hours (the plan asked only that duration and findings agree; 72 hours fits the day-3 seizure).
