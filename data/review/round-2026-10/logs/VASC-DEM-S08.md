# VASC-DEM-S08
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No notes file exists for VASC-DEM. The condition plan's classes (C1-C19) were applied as class rulings (ROUND_POLICY ruling 2); every change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A/C | blocker | ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives | Non-schema `sequences` plus `protocol`/`contrast` (C1) | FIXED: `analyze_brain_mri {}` |
| D | major | ground_truth.action_criteria[action-9-search-medical-literature], initial_tool_outputs.literature_search, fallback_tool_outputs.literature_search | Literature criterion leaking into its own output (C2, ruling 5) | FIXED: criterion deleted, initial null, fallback deleted |
| C | minor | ground_truth.action_criteria[action-10-check-drug-interactions], fallback_tool_outputs.drug_interactions | Generic optional check and generic fallback; no anticoagulant or new interacting drug is started (C3 group D) | FIXED: criterion and fallback deleted (initial output already null) |
| D | major | patient.neurological_exam.mental_status | MoCA total and items upfront (C4) | FIXED: bedside observation |
| B | major | initial_tool_outputs.clinical_assessment | MoCA 19/30 "education-adjusted" not derivable: listed losses (trail, cube, clock 2, digits backward, serial sevens, recall 3, orientation 1) total 10, giving raw 20 and 21 with the education point; impression localised the deficit to right parietal cortex and dated the step; criteria_met carried IADL loss and the abrupt step (C4, C5) | FIXED: itemised by section with letter fluency 0/1 and abstraction 1/2 added (12 losses, raw 18 + 1 = 19/30); criteria_met keeps domain impairment and cue-responsive recall; impression without localisation |
| D | major | initial_tool_outputs.mri (additional_observations, impression) | "points to the severe ipsilateral stenosis rather than to an embolic source", "all downstream of a severe right internal carotid stenosis", "identify a large-artery rather than a cardioembolic mechanism" (cross-modality and mechanism verdict, C5) | FIXED: STRIVE-2 numbered impression; laterality and the internal border-zone distribution kept as imaging description |
| D | major | initial_tool_outputs.advanced_imaging.impression | "This is a large-artery mechanism, and the stenosis reaches the threshold at which revascularisation is discussed" (C5) | FIXED: grades and velocities per side |
| B | minor | initial_tool_outputs.advanced_imaging.findings[1], quantitative_data | Left ICA "40-50%" with PSV 148 cm/s, which is in the 50-69% band of the SRU consensus criteria (PSV 125-230) | FIXED: 40-49% with PSV 118 cm/s (agrees with the MRA "moderate bulb stenosis") |
| D/B | minor | followup_outputs[request_mr_angiography].output | Impression "Both findings are relevant to a revascularisation decision"; "Variant anatomy limiting collateral supply" (interpretive); NASCET 75% from a 1.4 mm residual lumen without the distal diameter | FIXED: numbered findings-only impression; residual lumen 1.2 mm against distal ICA 4.8 mm (NASCET 75%); left bulb 40-49% |
| D | major | initial_tool_outputs.ecg.interpretation | "lowers the probability of an occult cardioembolic source relative to the severe carotid disease found on ultrasound" (cross-modality, C5) | FIXED: rhythm, axis, LVH, old inferior Q waves, no ectopy; finding[2] no longer cites the bypass |
| D | minor | initial_tool_outputs.specialized_test.impression | "matching the infarct distribution" (C5) | FIXED: profile with the education-adjusted norms |
| B | major | initial_tool_outputs.labs | Female Hb/Hct ranges in a man; template values; eGFR range ">60"; creatinine 1.24 gives CKD-EPI 2021 eGFR 59 at 80, not 54; LDL 88 not derivable from TC 168, HDL 38, TG 176 (Friedewald 95); interpretation with targets (C6) | FIXED: male ranges; Hb 13.8, Hct 41.2, WBC 7.9, Plt 197, MCV 92, Na 138, K 4.6, ALT 16, albumin 3.9, folate 7.8; creatinine 1.32 (eGFR 54); TC 161 (161 - 38 - 176/5 = 88); eGFR ">=60"; flag-only interpretation |
| C | major | ground_truth.avoided_actions | Two echo waste entries and two monitoring waste entries, one echo rationale calling the burden "small-vessel" (C10) | FIXED: both echo waste entries (6, 9) and the duplicate monitoring entry (8) removed (TTE is reasonable after ischaemic stroke, 2a); avoid-waste-7 kept with the plan rationale |
| B/D | major | fallback_tool_outputs (advanced_imaging, labs, ct, echo, cardiac_monitoring) | "non-contributory" fallbacks; CT "already obtained"; echo "No cardioembolic source identified" and a normal wall motion in a man with old inferior Q waves; template Holter numbers (C7) | FIXED: advanced_imaging and labs deleted; CT written to his lesions; echo modality-only with mild basal inferior hypokinesis, LVEF 52%, `echo_type` TTE; Holter rates varied (beta-blocked, mean 63); metadata.fallback_tool_kinds updated |
| C | major | ground_truth.assessment.required_recommendations | Musts restated criteria ("exclude reversible causes", "obtain MRI", "quantify the stenosis"); the revascularisation must had no timing, procedure or reason (C19) | FIXED: CEA referral without delay (symptomatic 70-80%, step 3 months ago within 6 months, CEA over stenting at 80); individualised BP until revascularisation then below 130/80; LDL below 70 with atorvastatin 80 and ezetimibe; single antiplatelet, no anticoagulation; occupational therapy and caregiver support |
| C | major | ground_truth.key_clinical_evidence[4], metadata.key_educational_points[3] | LDL target below 55 mg/dL for polyvascular disease: the plan's governing guideline (AHA 2021) sets below 70 in this condition (plan 1.2) | FIXED: LDL below 70 with ezetimibe if needed |
| C | minor | ground_truth.assessment.prohibited_recommendations[2] | Prohibited echocardiography (2a after ischaemic stroke) and duplicated the monitoring waste entry | FIXED: replaced by "Do not defer carotid revascularisation because the presentation is cognitive rather than motor, or because of age alone" |
| C/A | minor | ground_truth.action_criteria[*] | Rationale = label; unbracketed citations; verdicts in expected evidence (C13) | FIXED |
| C | minor | ground_truth.action_criteria order; sequence_constraints; stop_rule | Neuropsych after the vascular studies; no duplex-before-MRA constraint; max 0 (C16) | FIXED: screen, neuropsych, labs, MRI, ECG, duplex, MRA; soft duplex before MRA; max 1 |
| C | minor | ground_truth.avoided_actions[*].rationale | Generic; CT "already obtained" (C18) | FIXED |
| C | note | timing | Symptomatic within 6 months: the abrupt step 3 months ago with right parietal features (topographical disorientation, dressing apraxia) is the ipsilateral event | revascularisation must applies (plan section 4) |
| C | check | 3.6 check | each criterion probed on a fresh environment | duplex <- initial advanced_imaging; MRA <- followup request_mr_angiography (discriminated by modality); others initial; no library answer |

## Changes, in one paragraph a physician can read before re-reviewing
The MRI criterion now matches any MRI order. The exam no longer gives the MoCA; the screen is itemised so that raw 18 plus the education point gives 19/30. Reports state only their own findings: the MRI describes three right-hemisphere infarcts (one in the internal border zone) without naming the carotid as the cause, the duplex gives grades and velocities (left side corrected to 40-49% with a PSV that fits that band), the ECG no longer compares itself with the ultrasound, and the MRA states its NASCET measurement. Labs have male ranges, an LDL that fits the lipid panel and a creatinine that fits the eGFR. The duplicate waste entries are gone and echocardiography is no longer penalised. Musts: refer without delay for carotid endarterectomy (symptomatic 70-80% stenosis, step three months ago), individualised BP until revascularisation, LDL below 70 with atorvastatin 80 and ezetimibe, single antiplatelet, occupational therapy and caregiver support. The LDL 55 target was replaced by the AHA 2021 target of 70.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms per plan 5.1 (F06.7 in the `icd_codes` of a dementia case; "subcortical vascular dementia" and "small vessel disease dementia" are accepted for a large-artery multi-infarct case).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Adversarial verifier, 24 Oct 2026. No notes file for VASC-DEM. Read the final case and the diff. Checked: MoCA arithmetic (raw 18 + 1 education point = 19/30); duplex velocities against the SRU bands (right PSV 268, EDV 102, ratio 4.6 for 70-80%; left PSV 118 for 40-49%); MRA NASCET (1 - 1.2/4.8 = 75%); Friedewald LDL (161 - 38 - 35.2 = 88); timing of the symptomatic step (3 months, within the 6-month window) behind the CEA must and the preference for CEA over stenting above 70; individualised BP must consistent with the border-zone prohibition; no anticoagulation must consistent with sinus rhythm and the Holter fallback; duplicate waste entries removed, echo no longer penalised; red-herring paths; duplex-before-MRA soft constraint.
Found and fixed: creatinine 1.32 mg/dL gives a CKD-EPI 2021 eGFR of 54.5 at 80 (rounds to 55), not the stored 54. Creatinine set to 1.33 mg/dL (eGFR 54.0) in `initial_tool_outputs.labs.panels.CMP`, the interpretation and the abnormal-values summary, so the eGFR 54 in the labs, the expected evidence and the log stays valid. The worker's log row "creatinine 1.32" is superseded.
perfect_agent.py and case_io.py check clean for this case.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here multi-infarct labels and F01.1. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- Lipid must: "Intensify lipid lowering to LDL below 70 mg/dL (current 88 mg/dL on atorvastatin 40 mg): atorvastatin 80 mg, adding ezetimibe if the target is not reached [AHA_ASA_2021_secondary]" -> "Intensify lipid lowering to LDL below 55 mg/dL (current 88 mg/dL on atorvastatin 40 mg): very high risk with atherosclerotic ischaemic strokes and peripheral arterial disease; atorvastatin 80 mg, adding ezetimibe if the goal is not reached [ACC_AHA_dyslipidemia_2026]" Reason: the 2026 ACC/AHA multisociety dyslipidemia guideline (supersedes the 2018 cholesterol guideline on which the AHA 2021 LDL-below-70 figure rests) sets LDL below 55 mg/dL for clinical ASCVD at very high risk (two major ASCVD events, or one plus two or more high-risk conditions).
- `ground_truth.key_clinical_evidence` and `metadata.key_educational_points`: LDL goal below 55 mg/dL (very high risk: atherosclerotic stroke plus peripheral arterial disease).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

A fresh order of each study below was answered by the benchmark-level normal library, which contradicted this patient (age, rhythm, devices, surgery, stored findings). Each now has a case-specific report:

- FDG_PET: Right middle cerebral territory metabolic defects (inferior parietal; frontal operculum) with mild right border-zone hypometabolism and crossed left cerebellar diaschisis; left hemisphere preserved. (fallback_tool_outputs.advanced_imaging)
- perfusion_SPECT: Right middle cerebral territory perfusion defects (inferior parietal; frontal operculum) with mild right border-zone hypoperfusion and crossed left cerebellar diaschisis; left hemisphere preserved. (followup request_perfusion_spect)
- performance_status: Karnofsky 60 (requires occasional assistance but able to care for most needs), ECOG 2 (ambulatory and capable of all self-care, unable to carry out any work activities). (fallback_tool_outputs.clinical_assessment)
- exercise_stress_test: Very low workload (2.5 METs) limited by claudication; submaximal heart rate on beta-blockade, non-diagnostic for ischaemia. (fallback_tool_outputs.specialized_test)
- gait_and_balance_timed: Mildly slowed, slightly wide-based gait (Timed Up and Go 14.8 s) with reduced left arm swing; longer walks are limited by calf symptoms rather than balance. (followup request_gait_and_balance_timed)
- levodopa_challenge: MDS-UPDRS III 9/132 OFF and 9/132 ON (0% change), below the 30% threshold for a clinically meaningful levodopa response. (followup request_levodopa_challenge)
- TEE: Mild basal inferior hypokinesis; LVEF 52%; mild concentric left ventricular hypertrophy; aortic valve sclerosis without stenosis; grade III aortic arch atheroma without a mobile component. No patent foramen ovale and no left atrial appendage thrombus. (followup request_tee)
- cardiac_MRI: Chronic basal inferior subendocardial infarct with mild hypokinesis; LVEF 53%; no thrombus. (followup request_cardiac_mri)
- coronary_angiography: Severe native three-vessel disease after bypass grafting: patent arterial graft to the left anterior descending and vein graft to the obtuse marginal; occluded vein graft to the right coronary artery. (followup request_coronary_angiography)
- coronary_CTA: Post-bypass study: patent arterial graft to the left anterior descending and vein graft to the obtuse marginal, occluded vein graft to the right coronary artery; severe calcified native disease. (followup request_coronary_cta)
- speech_language_evaluation: Mild dysarthria with intact language. (followup request_speech_language_evaluation)
- DTI_tractography: Interrupted parietal terminations of the right arcuate fasciculus with reduced fractional anisotropy of the right corticospinal tract in the centrum semiovale; optic radiations intact. (followup request_dti_tractography)
- CT_perfusion: Matched perfusion defects confined to chronic tissue loss (right supramarginal and angular gyri; right frontal operculum); no acute core or penumbral mismatch. Mild haemodynamic delay in the right middle cerebral artery territory without an ischaemic threshold. (followup request_ct_perfusion)
- perfusion_MRI: Matched perfusion defects confined to chronic tissue loss (right supramarginal and angular gyri; right frontal operculum); no acute core or penumbral mismatch. Mild haemodynamic delay in the right middle cerebral artery territory without an ischaemic threshold. (followup request_perfusion_mri)
- cerebral_angiography: Severe right internal carotid stenosis (75%, NASCET) with delayed right middle cerebral branch filling; left bulb stenosis 45%; no tandem intracranial stenosis. (followup request_cerebral_angiography)
- transcranial_doppler: Dampened right middle cerebral artery waveform with reduced velocity and pulsatility and increased right posterior cerebral velocity, consistent with a haemodynamically significant proximal right-sided stenosis with posterior collateral flow. (followup request_transcranial_doppler)
- chest_abdomen_pelvis_CT: No mass or lymphadenopathy. Mild upper-lobe centrilobular emphysema; median sternotomy wires, coronary graft clips and dense native coronary calcification. (fallback_tool_outputs.body_imaging)
- chest_CTA: No pulmonary embolism or aortic dissection. Mild upper-lobe centrilobular emphysema; median sternotomy wires, coronary graft clips and dense native coronary calcification. (followup request_chest_cta)
- mediastinum_CT: No mediastinal mass or lymphadenopathy; median sternotomy wires, coronary graft clips and dense native coronary calcification. (followup request_mediastinum_ct)
- chest_xray: No acute cardiopulmonary abnormality; median sternotomy wires and coronary graft clips. (followup request_chest_xray)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k VASC-DEM-S08` pass; criterion outputs unchanged against the pre-pass snapshot; no 60-character window of any expected_evidence in the new reports; synonym guard 0 changes.
