# VASC-DEM-M10
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (`plans/VASC-DEM.md`) and the worker's own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | `initial_tool_outputs.mri.findings[0]`, `.impression`, `.additional_observations`, `.volumetrics`, `ground_truth.differential`, `.key_clinical_evidence` | Laterality error: a LEFT occipital infarct was given as the cause of a dense LEFT homonymous hemianopia (left-sided reading loss, bumping into objects on the left). A left occipital lesion produces a right hemianopia. | FIXED: the infarct is in the right occipital cortex (right PCA territory). To keep the case's two-mechanism logic, the MRI now records intracranial TOF angiography showing both PCAs arising from the basilar tip (no fetal-type PCoA), so the PCA infarct is outside the stenosed carotid's territory. All mentions updated (impression, volumetrics, differential, key clinical evidence, musts). |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1. | FIXED: `analyze_brain_mri {}`; label about territory assignment. |
| D | major | criterion `action-9-search-medical-literature`, literature outputs | Plan C2. | FIXED: criterion deleted, initial null, fallback deleted. |
| C | major | criterion `action-10-check-drug-interactions`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group R: he takes aspirin and will start an anticoagulant; check was optional `{}` with a generic fallback. | FIXED: recommended; alternatives apixaban, rivaroxaban, edoxaban, dabigatran, warfarin; five drug-keyed outputs (bleeding with aspirin, stop aspirin unless a separate indication, label dose rules, alcohol, warfarin-atorvastatin INR note); fallback deleted. Amlodipine checked: no relevant DOAC interaction. |
| C | major | `patient.physical_exam` (new), `patient.demographics.bmi` | No weight for DOAC dosing. | FIXED: "Weight 83 kg, height 172 cm." (BMI 28.2 to 28.1). Cockcroft-Gault about 58 mL/min; apixaban 5 mg twice daily (no reduction criterion). |
| D | major | `patient.neurological_exam.mental_status` | Plan C4. | FIXED: bedside observation and "Formal cognitive screening reported separately". |
| B | major | `initial_tool_outputs.clinical_assessment` | MoCA arithmetic: listed losses with month-only orientation give 18 raw and 19 with the 8-years education point, not 18; `criteria_met` carried interpretive items; impression argued "multi-infarct mechanism". | FIXED: orientation month and date; raw 17 + 1 = 18/30 itemised; `criteria_met` reduced to observations; impression scores only. |
| D | major | `initial_tool_outputs.specialized_test.impression`, `.ecg.interpretation`, `.echo.impression`, `.advanced_imaging.impression`, `.mri.additional_observations`/`.impression` | Plan C5: "maps onto right hemispheric and left occipital lesions", "an anticoagulable embolic source", "no structural embolic source beyond the AF", duplex "two mechanisms coexist ... downstream of the stenosis", MRI "requires two mechanisms ... attributable to cardioembolism ... relevant to anticoagulation". | FIXED: each report in modality-only voice (velocities and NASCET percentage; rhythm and LVH; chambers, EF, no thrombus; territories, border-zone pattern, SWI, PCA origin). |
| C | major | criterion `action-6-order-advanced-imaging`, `followup_outputs[0]` (new) | An MRA order (a common confirmatory study before endarterectomy) would have returned the library's normal MRA, contradicting an 80-90% stenosis. | FIXED: MR_angiography added as a second alternative of the carotid criterion, answered by an authored neck and intracranial MRA (right ICA about 85%, left under 50%, PCAs from the basilar tip). Probed: duplex and MRA each return their own report. |
| A | minor | criterion `action-7-order-echocardiogram`, `initial_tool_outputs.echo.echo_type` | Plan 3.1 uses `order_echocardiogram {}`; report had no `echo_type`. | FIXED: criterion `{}`; report `echo_type` "TTE". |
| B | major | `initial_tool_outputs.labs` | Plan C6: female Hb/Hct ranges in a man (Hb 13.0 would be low); template values; creatinine 1.16 gives eGFR 65 (CKD-EPI 2021), not the 58 the case relies on; range ">60"; total cholesterol 176 vs Friedewald 169; interpretation "above the polyvascular target of 55 mg/dL", "adequate for anticoagulation with dose attention". | FIXED: male ranges, Hb 14.1, Hct 42.0; creatinine 1.27 (flagged) so that eGFR 58 is correct; WBC 7.9, Plt 251, MCV 87, Na 138, K 4.6, ALT 24, albumin 4.2, folate 7.4; total cholesterol 169; the 55 mg/dL target removed; interpretation lists flagged values only. |
| B | major | `fallback_tool_outputs.cardiac_monitoring` | Holter fallback "sinus rhythm, no AF" in a patient whose ECG shows AF. | FIXED: AF throughout, mean rate 86. |
| D | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, `.labs` | Plan C7. | FIXED: CT fallback describes his infarcts (right occipital, right frontoparietal, right deep white matter) with the CT limitation; others deleted; `metadata.fallback_tool_kinds` trimmed. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated tool steps; no DOAC choice or dose, no LDL target, no HbA1c target, no timing for revascularisation. | FIXED: seven musts: two-mechanism diagnosis by territory; DOAC (apixaban 5 mg twice daily) and stop aspirin; urgent vascular referral for endarterectomy (symptomatic 80-90%, last ipsilateral event 5 months ago, CEA preferred at 76 and avoids antiplatelet added to the anticoagulant); individualised BP lowering avoiding systolic below about 120 until treated, then below 130/80; LDL below 70 (92 on atorvastatin 40: atorvastatin 80, ezetimibe if needed); HbA1c about below 8.0%; rehabilitation and driving. Citations [AHA_ASA_2021_secondary], [ADA_2025_older_adults]. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | "Do not leave an uninvestigated hemianopia unexplained for two years" is not a recommendation that can apply at this visit. | FIXED: replaced by "Do not withhold anticoagulation because of age, cognitive impairment or the planned carotid surgery"; others kept, reworded. |
| C | major | `ground_truth.differential` | Plan C8: "cardioembolic alone" and "large-artery alone" moderate after the work-up shows both mechanisms. | FIXED: both low, key features updated to the right PCA infarct. |
| B | minor | `ground_truth.red_herrings[1]` | Empty field path, location "history". | FIXED: `patient.history_present_illness`. |
| C | minor | `ground_truth.avoided_actions` | Plan C18. | FIXED: case-specific rationales. |
| A | minor | all criteria | Plan C13. | FIXED. |
| B | minor | `ground_truth.action_criteria` order, `.stop_rule` | Plan C16. | FIXED: screen, neuropsych, labs, MRI, ECG, carotid imaging, TTE, drug check; `max_additional_actions` 1. |
| B | minor | `metadata.key_educational_points[1]` | "modifies the blood-pressure target" vague. | FIXED: cautious lowering until the stenosis is treated. |

## Changes, in one paragraph a physician can read before re-reviewing

A 76-year-old man with stepwise decline after three events, a never-investigated left hemianopia, an irregular pulse and a right carotid bruit. The main correction: the occipital infarct that explains his LEFT hemianopia is now in the RIGHT occipital lobe (it was left, which is anatomically impossible for that field defect); the MRI's TOF angiography shows both PCAs from the basilar tip, so this infarct is still outside the stenosed carotid's territory and the two-mechanism logic (AF plus symptomatic right ICA stenosis with a border-zone infarct) holds. Reports now state only their own findings. A neck MRA was authored so a confirmatory MRA does not return a normal library study. Labs carry male ranges, creatinine 1.27 with eGFR 58, and the 55 mg/dL LDL target is gone. Musts: apixaban 5 mg twice daily and stop aspirin; urgent vascular referral for endarterectomy (last ipsilateral event 5 months ago); cautious BP lowering until the stenosis is treated; LDL below 70 with atorvastatin 80; HbA1c about below 8%; rehabilitation and no driving. The drug check is recommended and case-specific; single-mechanism alternatives are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation key used: `[ADA_2025_older_adults]` (plan 5.4).
- Synonyms (plan 5.1): F06.7 should be removed from this dementia case's accepted codes.

## Open questions for Andrea (judgment calls you could not settle)

- None. Decision recorded: the laterality was fixed by moving the infarct to the right occipital lobe (and documenting a non-fetal PCA) rather than by switching the hemianopia to the right, because the HPI, exam, screen and neuropsychology all describe left-sided visual loss and the motor signs are left-sided.

## Verification

Adversarial check (24 Oct 2026), with extra attention to the laterality rewrite. No reviewer notes. Checked: no "left occipital" or left PCA mention remains anywhere in the file; the right occipital infarct now explains the left hemianopia in the HPI, exam, screen (clock crowded to the right), battery and CT fallback; all MCA and border-zone infarcts are right-sided, matching the left motor signs and the right ICA stenosis; the last ipsilateral event (left hand clumsiness 5 months ago) is within 6 months, so the urgent endarterectomy referral is correct, and CEA over stenting above 70 is per AHA 2021; MoCA 17 raw + 1 = 18/30, matching the exam (month and date wrong); Cockcroft-Gault (140-76) x 83 / (72 x 1.27) = 58 mL/min, apixaban 5 mg (no reduction criterion); eGFR 58 matches creatinine 1.27 at 76; Friedewald 169; LDL target below 70 (atherosclerotic disease), HbA1c individualised; duplex and MRA (both alternatives of `action-6`) agree (80-90% and about 85%); AF Holter fallback agrees with the ECG; DOAC dose rules in the drug outputs are correct; single-mechanism alternatives are low with key features that match the final evidence.

Found: nothing that needed a change in this case.

Checks re-run after my edits: `perfect_agent.py -v` passes (every required and recommended criterion answered by case data); `case_io.py check` clean for this case (schema, synonym guard, no test failure naming it). Note for the lead, not changed: `metadata.fallback_tool_kinds` still labels case-specific fallbacks (CT with this patient's lesions, AF Holter where present) as "normal"; the field is read by no code or test, so I left it rather than churn it.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here multi-infarct labels and F01.1. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- Lipid must: "Intensify lipid lowering to LDL below 70 mg/dL (92 mg/dL on atorvastatin 40 mg): atorvastatin 80 mg, adding ezetimibe if needed [AHA_ASA_2021_secondary]." -> "Intensify lipid lowering to LDL below 55 mg/dL (92 mg/dL on atorvastatin 40 mg): very high risk with ischaemic strokes, peripheral arterial disease, diabetes and hypertension; atorvastatin 80 mg, adding ezetimibe if needed [ACC_AHA_dyslipidemia_2026]." Reason: the 2026 ACC/AHA multisociety dyslipidemia guideline (supersedes the 2018 cholesterol guideline on which the AHA 2021 LDL-below-70 figure rests) sets LDL below 55 mg/dL for clinical ASCVD at very high risk (two major ASCVD events, or one plus two or more high-risk conditions).
- `[ADA_2025_older_adults]` -> `[ADA_older_adults_2026]` in the HbA1c must (same target below about 8.0%; superseded edition, as in ALZ-EARLY).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: cardiac_monitoring normal->case, ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
