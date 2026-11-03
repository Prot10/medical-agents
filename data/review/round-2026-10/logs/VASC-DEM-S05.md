# VASC-DEM-S05
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The condition has no reviewer notes. The plan's classes (C1-C7, C13, C14, C16, C18, C19 and the S05 index entry) were applied as classes (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | ground_truth.action_criteria[action-5-analyze-brain-mri].alternatives | Non-schema `sequences` key plus `protocol`/`contrast`: no real call could match (C1). | FIXED: `analyze_brain_mri {}`; label and rationale rewritten. |
| D | major | action-7-search-medical-literature; initial and fallback literature_search | Literature criterion leaking its expected evidence into its own output (C2). | FIXED: criterion deleted, initial null, fallback deleted. |
| C | blocker | ground_truth.assessment (must "Re-examine the anticoagulation indication", prohibition "Do not continue anticoagulation reflexively ... after nine years of sinus rhythm"), red_herrings[0], key_clinical_evidence[2], metadata.key_educational_points[2] | The case taught stopping apixaban for sinus rhythm after flutter ablation, falls and deep microbleeds. ESC AF 2024: anticoagulation is decided on CHA2DS2-VA, not rhythm, after ablation; falls, age and a few deep microbleeds are not reasons to withhold it. His CHA2DS2-VA is 3 (age 82, hypertension) (C19, plan S05). | FIXED: must to continue anticoagulation on CHA2DS2-VA [ESC_AF_2024]; prohibition now forbids stopping it for those reasons; red herring, key evidence and educational point rewritten. |
| C | major | patient.physical_exam; must on apixaban dose | No weight, so the apixaban dose criteria could not be checked (plan 1.2). | FIXED: physical_exam.general "Weight 72 kg, height 1.72 m (BMI 24.3)" (matches the recorded BMI); must keeps 5 mg twice daily (only the age criterion met; creatinine 1.28 below 1.5). |
| C | major | action-8-check-drug-interactions; fallback_tool_outputs.drug_interactions; initial_tool_outputs.drug_interactions | Generic check and generic "no prohibitive interaction" fallback (C3 group O). | FIXED: fallback deleted; criterion optional `{}` with case-specific expected evidence; initial output keyed `apixaban` (dose criteria, no interaction with nebivolol, lercanidipine, atorvastatin, tiotropium; SSRI and NSAID bleeding risk; alcohol), `dextromethorphan-quinidine` (P-gp and CYP2D6 effects, QTc) and `sertraline` (bleeding with apixaban, hyponatraemia), the treatments a pseudobulbar-affect must invites. Leak guard passes. |
| D | major | patient.neurological_exam.mental_status | Gave MoCA 18/30 and item losses (C4). | FIXED: bedside observation, "Formal cognitive screening reported separately". |
| D | major | initial_tool_outputs.clinical_assessment (impression, criteria_met) | "a corticobulbar tract sign that is part of the disease rather than a mood disorder"; IADL, executive and pseudobulbar verdicts in criteria_met (C5). | FIXED: scores-only impression with the CNS-LS and GDS values; criteria_met keeps impairment and cueing. |
| B | minor | initial_tool_outputs.clinical_assessment (findings, scores) | Domain rows were not a full MoCA breakdown; fluency given as animals for the letter-F item. | FIXED: domains 1+3+3+2+2+1+5 = raw 17, plus 1 for 12 years of education = 18; "6 F-words". |
| D | major | followup_outputs[gait].output.impression | "matching the extensor plantar responses and clonus. High falls risk in a first-floor flat" (cross-modality) (C5). | FIXED: measurements only; cadence 113 steps/min added (26 cm at 0.49 m/s); TUG normal value stated. |
| D | minor | initial_tool_outputs.specialized_test.impression | "Severe subcortical profile" (C5). | FIXED: profile wording; the dysarthria-not-aphasia statement is within neuropsychology and kept. |
| B | major | initial_tool_outputs.labs | Female ranges in a man (male Hb range would flag 13.1 as anaemia that no part of the case addresses); creatinine 1.18 gives CKD-EPI 2021 eGFR about 62 at 82, not 56; template values; interpretive text including "relevant to his anticoagulant dosing" (C6). | FIXED: Hb 13.8 with Hct 41.2 and male ranges; creatinine 1.28 (eGFR 56; Cockcroft-Gault about 45 mL/min at 72 kg); varied values; pattern-level interpretation. |
| D | major | initial_tool_outputs.mri (impression, observations) | "explains the pseudobulbar affect, dysarthria and spastic gait", "despite the atrial flutter history", "arguing against hereditary small-vessel disease", "No embolic cortical infarct" (C5). | FIXED: numbered STRIVE-2 impression with observations stated as findings. |
| D | minor | fallback_tool_outputs (advanced_imaging, labs, ct, echo, cardiac_monitoring) | Off-pathway revealing text; echo "No cardioembolic source identified"; Holter average 72 vs his 64 on nebivolol (C7). | FIXED: advanced_imaging and labs deleted; CT rewritten for this patient; echo neutral with echo_type TTE; Holter average 63. metadata.fallback_tool_kinds updated. |
| C | major | ground_truth.assessment (other musts) | Musts restated the scored work-up; generic "secondary-prevention targets" in a patient without clinical stroke; no PBA treatment or social measures. | FIXED: PBA recognised and treated if distressing (SSRI or dextromethorphan-quinidine, interaction checked); BP below 130/80 gradually and alcohol reduction as bleeding-risk modification [ESO_2021_SVD]; statin intensity; falls and housing; finances and carers. Prohibitions: antidepressant escalation, stopping apixaban, adding an antiplatelet, benzodiazepines and anticholinergics, gait misattribution. |
| A | minor | all criteria citations and rationales | Unbracketed duplicates; rationale equal to label (C13). | FIXED. |
| C | minor | avoided_actions rationales | Generic text; "MRI already obtained" (C18). | FIXED: case-specific; CT rationale per plan. Echo and monitoring waste kept (no embolic pattern, already anticoagulated). |
| C | minor | criteria order, stop_rule (C16) | | FIXED: screen, gait, neuropsych, labs, MRI, drug check; screen before MRI kept; max_additional_actions 1. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis unchanged (severe subcortical ischaemic vascular dementia with pseudobulbar affect and spastic gait). The main clinical correction: the case used to reward questioning his apixaban because he has been in sinus rhythm since flutter ablation, falls and has deep microbleeds. Per ESC AF 2024 the decision rests on CHA2DS2-VA (3 here), so the must is now to continue apixaban at 5 mg twice daily (weight 72 kg added; only the age criterion for reduction is met) and to reduce bleeding risk through blood pressure, alcohol and falls measures; stopping it is now prohibited. The exam no longer gives the MoCA, and the screen, gait, neuropsychology and MRI reports describe their own findings without explaining the syndrome. Labs use male ranges and a creatinine (1.28) that gives the stated eGFR of 56. The optional drug check now holds real content for apixaban and for the pseudobulbar-affect treatments it interacts with. The literature step is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.1): remove F06.7 from the F01 codes of this dementia case.
- Citation key `[ESC_AF_2024]` needs allow-listing in the VASC-DEM pack (plan 5.4).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Checked every Own-findings row against the file and the git diff: MRI `{}`; literature gone; the anticoagulation reversal is applied everywhere it appeared (must, prohibition, red herring, key evidence, educational point) and is correct per ESC AF 2024: CHA2DS2-VA 3 (age 82 counts 2, hypertension 1); apixaban 5 mg twice daily is right (age 80 or more is the only criterion met: weight 72 kg, creatinine 1.28 mg/dL); weight and height give the recorded BMI 24.3; creatinine 1.28 gives CKD-EPI 2021 eGFR 56 at 82 and Cockcroft-Gault about 45 mL/min; Hb 13.8 with Hct 41.2 on male ranges; MoCA domains give raw 17 plus 1 = 18 and the lost points (4+4+3+1+1) agree; month wrong in exam and screen; gait 26 cm at 113 steps/min gives 0.49 m/s. Drug-check content checked: quinidine P-gp inhibition with apixaban, CYP2D6 inhibition with nebivolol, QT and AV-block contraindications of dextromethorphan-quinidine, SSRI bleeding and hyponatraemia are correct; leak guard passes. Echo and monitoring waste rationales are case-specific and consistent with the CHA2DS2-VA rule.
Changed: `fallback_tool_outputs.echo` was identical across S01-S05 (template carry-over); for a man with ablated atrial flutter the left atrium is now "mildly dilated, LA volume index 36 mL/m2" in chambers and impression. Nothing else.
Re-ran `perfect_agent.py -v` (pass) and `case_io.py check` (clean for this case).

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Total cholesterol]` | Total cholesterol 190 mg/dL did not equal LDL + HDL + TG/5 (178.4); the same lab-arithmetic class was fixed in M07-M10, P01, P02 and S06-S11 but not here. | FIXED: total cholesterol 178 mg/dL (flag unchanged; LDL, HDL and TG, which the musts and evidence quote, unchanged). |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here subcortical small-vessel labels and F01.2/I67.3. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `metadata.fallback_tool_kinds`: ct normal->case, echo normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 71.1 -> 72 kg, height 171 -> 172 cm, BMI 24.3 -> 24.3 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 72 kg, height 172 cm.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

A fresh order of each study below was answered by the benchmark-level normal library, which contradicted this patient (age, rhythm, devices, surgery, stored findings). Each now has a case-specific report:

- FDG_PET: Bilateral frontal hypometabolism with reduced left thalamic uptake and mild diffuse cortical reduction; posterior cingulate relatively preserved. The pattern is consistent with severe subcortical small-vessel disease. (fallback_tool_outputs.advanced_imaging)
- perfusion_SPECT: Bilateral frontal hypoperfusion with reduced left thalamic uptake and mild diffuse cortical reduction; posterior cingulate relatively preserved. The pattern is consistent with severe subcortical small-vessel disease. (followup request_perfusion_spect)
- performance_status: Karnofsky 50 (requires considerable assistance and frequent care), ECOG 2 (ambulatory and capable of all self-care, unable to carry out any work activities). (fallback_tool_outputs.clinical_assessment)
- exercise_stress_test: Test abandoned at the lowest stage because of gait failure; non-diagnostic. (fallback_tool_outputs.specialized_test)
- levodopa_challenge: MDS-UPDRS III 30/132 OFF and 29/132 ON (3% change), below the 30% threshold for a clinically meaningful levodopa response. (followup request_levodopa_challenge)
- TEE: Mild concentric left ventricular hypertrophy; mildly dilated left atrium; aortic valve sclerosis without stenosis. No patent foramen ovale and no left atrial appendage thrombus. (followup request_tee)
- cardiac_MRI: Mildly dilated left atrium with preserved left ventricular function; no scar or thrombus. (followup request_cardiac_mri)
- speech_language_evaluation: Moderate spastic (pseudobulbar) dysarthria with intact language. (followup request_speech_language_evaluation)
- respiratory_function: Moderate obstructive ventilatory defect (FEV1/FVC 0.56, FEV1 62% predicted) with normal respiratory muscle strength. (followup request_respiratory_function)
- DTI_tractography: Bilateral attenuation of the corticospinal and corticobulbar tracts at the internal capsules on a background of severely reduced white matter fractional anisotropy. (followup request_dti_tractography)
- chest_abdomen_pelvis_CT: No mass or lymphadenopathy. Centrilobular and paraseptal emphysema, upper-lobe predominant, with bronchial wall thickening; coronary artery calcification. (fallback_tool_outputs.body_imaging)
- chest_CTA: No pulmonary embolism or aortic dissection. Centrilobular and paraseptal emphysema, upper-lobe predominant, with bronchial wall thickening; coronary artery calcification. (followup request_chest_cta)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k VASC-DEM-S05` pass; criterion outputs unchanged against the pre-pass snapshot; no 60-character window of any expected_evidence in the new reports; synonym guard 0 changes.
