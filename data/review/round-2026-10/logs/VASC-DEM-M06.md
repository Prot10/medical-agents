# VASC-DEM-M06
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | VASC-DEM was never annotated; no note ids exist for this case. All changes below come from the condition plan and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key. | FIXED: `analyze_brain_mri {}`. |
| D | major | `action-8-search-medical-literature`, literature initial and fallback | Plan C2 leak. | FIXED: criterion deleted; initial null; fallback deleted. |
| C | minor | `action-9-check-drug-interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group D (the furosemide question is a must, not an interaction). | FIXED: deleted; initial null. |
| C | major | `patient.neurological_exam.additional` | "Prosthetic valve click audible" in a patient with a bioprosthesis (echo): tissue valves do not click; that is a mechanical-valve sign. | FIXED: "Soft ejection systolic murmur at the left sternal edge"; added "Jugular venous pressure not raised; no peripheral oedema" (needed to judge the furosemide, plan section 4). |
| B | minor | `patient.neurological_exam.motor` | "Strength 5/5 with mild bilateral proximal deconditioning weakness" is self-contradictory. | FIXED: "Strength 5/5 throughout. No drift." |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: MoCA and item losses in the exam. | FIXED: bedside observation, screening reported separately. |
| D | major | `initial_tool_outputs.clinical_assessment.impression`, `.criteria_met`, `.scores.4AT_delirium_screen` | Impression concluded "this is a persistent deficit rather than ongoing delirium, and it has cost him instrumental independence"; `delirium_resolved` and `onset_within_3_months_of_vascular_event` are conclusions/history. | FIXED: impression lists the scores (MoCA item arithmetic already correct: 11 points lost, 18 years, 19/30); both keys removed; 4AT "0". |
| C | minor | `initial_tool_outputs.ecg.intervals.PR`, `.findings[0]` | "First-degree AV block" with PR 192 ms (first-degree block requires PR above 200 ms). | FIXED: PR 214 ms, stated in the finding. |
| D | major | `initial_tool_outputs.ecg.interpretation`, `.findings` | ECG argued the mechanism ("argues against a cardioembolic mechanism and leaves the documented hypotensive episode as the explanation"), cited the valve disease and the postoperative telemetry. | FIXED: categorical ECG read only; the 5-day telemetry moved to `past_medical_history[0]` as history. |
| D | major | `initial_tool_outputs.echo.impression`, `.echo_type` | Echo attributed the infarct pattern to hypotension (cross-modality); `echo_type` missing on the TTE answer. | FIXED: numbered cardiac findings; `echo_type` TTE. |
| D | major | `initial_tool_outputs.mri.impression`, `.additional_observations`, `.findings[0].signal_characteristics.DWI` | Plan C5: "the signature of global hypoperfusion, not of embolism", "corresponds to the documented prolonged intraoperative and postoperative hypotension", "lesions date to the perioperative period", "neither small-vessel disease nor a degenerative process contributes materially". | FIXED: numbered STRIVE-2 impression describing the bilateral symmetric cortical (ACA-MCA, MCA-PCA) and internal border-zone infarcts, Fazekas 1, no microbleeds, MTA 0-1; no mechanism or history reference. |
| D | minor | `initial_tool_outputs.specialized_test.impression`, `.findings[1].test` | "The profile matches bilateral frontal and parietal border-zone injury" (cross-modality); dash in a test name. | FIXED: percentiles and a "Profile:" sentence; "Wisconsin Card Sorting Test, categories completed". |
| B | major | `initial_tool_outputs.labs` | Plan C6: female Hb/Hct ranges in a man; Hct 41.6 with Hb 12.4 and a "mild anaemia" narrative not flagged; creatinine 1.38 at 68 gives an eGFR of about 56, not 51; template values; interpretive text. | FIXED: male ranges; Hb 12.4 and Hct 37.4 flagged low; creatinine 1.48 (eGFR 51 consistent); WBC 5.8, Plt 196, MCV 89, Na 137, K 4.9, ALT 18, albumin 3.8, folate 10.4; summary rebuilt; "Flagged: ..." interpretation. |
| D | minor | `fallback_tool_outputs.advanced_imaging`, `.labs`, `.ct` | Plan C7. | FIXED: two deleted; CT fallback shows bilateral border-zone hypodensities. Holter fallback kept (sinus, consistent with the telemetry). |
| A | minor | `action_criteria[*]` | Plan C13. | FIXED: case-specific rationales and expected evidence. |
| B | minor | order, `stop_rule` | Plan C16. | FIXED: screen, neuropsych, labs, MRI, ECG, TTE (all required); `max_additional_actions` 1. |
| B | minor | `avoided_actions` | Plan C18. | FIXED: CT canonical; EEG rationale names the resolved delirium and 4AT 0. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were diagnostic steps ("Obtain brain MRI", "Exclude an embolic source with an ECG and echocardiography", "Exclude reversible causes"). | FIXED: explain border-zone vascular dementia [VASCOG_2014]; individualised BP (keep 128/72, avoid systolic below about 120 and orthostatic hypotension) [AHA_ASA_2021_secondary]; stop furosemide without fluid overload (EF 56%, no oedema, eGFR 51); continue aspirin and atorvastatin 40, no anticoagulation; record the injury for future anaesthesia; occupational therapy and carer support. |
| C | minor | `prohibited_recommendations[3]` | "an unnecessary diuretic" (plan: check against the echo). | FIXED: "Do not continue furosemide without a current indication ..."; the echo (EF 56%) and new exam (no oedema) support it. |
| C | major | `ground_truth.differential[0]` | Plan C8: POCD without structural injury `moderate` after MRI shows the injury. | FIXED: `low`. |
| B | minor | `red_herrings[*].field_path` | Empty. | FIXED: HPI (delirium) and `past_medical_history[0]` (valve surgery). |
| - | check | plan 3.6 | perfect_agent ok; probe: all criteria answered by case data; CT and Holter by case fallbacks; `case_io.py check` and test_case_guards list no failure naming M06. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case stays vascular dementia from bilateral symmetric border-zone infarcts after prolonged hypotension at aortic valve replacement. The examination no longer has a valve click (he has a bioprosthesis) and now records no oedema and a normal JVP; motor strength is no longer contradictory. Reports describe only their modality: the MRI describes the border-zone pattern without naming hypoperfusion or the operation, the ECG and echo no longer argue the mechanism, the neuropsychology reports a profile. The ECG's first-degree AV block now has a PR of 214 ms, and the labs use male ranges with the mild anaemia flagged and a creatinine consistent with eGFR 51. Musts: explain the diagnosis, keep BP at its current level and avoid hypotension, stop furosemide, continue aspirin and atorvastatin without anticoagulation, record the injury for anaesthesia, rehabilitation and carer support. Postoperative cognitive dysfunction is low on the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.1): `F06.7` appended to this dementia case's codes.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: MoCA arithmetic (11 lost, 19/30, 18 years); PR 214 ms for first-degree AV block; male ranges, Hb 12.4 / Hct 37.4 flagged, creatinine 1.48 consistent with eGFR 51 at 68; bioprosthesis exam (no click), JVP and oedema supporting the furosemide must; individualised BP must vs the prohibition on systolic below 120; aspirin and statin continuation vs the anticoagulation prohibition; differential.

Found and changed:
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria` (new `action-10-cervical-vessel-imaging`), `initial_tool_outputs.advanced_imaging`, `followup_outputs[0]`, `ground_truth.differential[3]` | Anterior-circulation border-zone infarcts with no carotid imaging anywhere in the pathway (AHA 2021: carotid imaging for anterior-circulation ischaemic stroke). A severe or bilateral carotid stenosis is the main alternative cause of border-zone infarction and would change the mechanism and the individualised BP target the musts set. | FIXED: recommended criterion after the ECG with alternatives `carotid_duplex` (new initial output: bilateral bulb plaque, less than 30% stenosis each side, antegrade vertebrals) and `MR_angiography` (new follow-up agreeing with it, complete circle of Willis); both probed and served by case data. Differential gains "Haemodynamic infarction distal to a severe carotid stenosis or occlusion" (I65.23), low, excluded by the symmetric pattern and the duplex. |

perfect_agent ok; `case_io.py check` and test_case_guards list no failure naming M06.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Total cholesterol]` | Total cholesterol 152 mg/dL did not equal LDL + HDL + TG/5 (145.6); the same lab-arithmetic class was fixed in M07-M10, P01, P02 and S06-S11 but not here. | FIXED: total cholesterol 146 mg/dL (flag unchanged; LDL, HDL and TG, which the musts and evidence quote, unchanged). |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3-order-advanced-imaging].rationale`, `[avoid-waste-4-interpret-labs].rationale` | Plan C18: the MIBG and paraneoplastic/autoimmune rationales were still the August template text shared by M01-M06; the autoimmune one described "a chronic stepwise decline with a hypertensive imaging burden", which is wrong for this case. | FIXED: case-specific one-liners (no Lewy features; deficit beginning with the perioperative hypotension, stable since). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall. The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here none (hypoperfusion: generic labels only; "multi-infarct" and "subcortical" labels no longer granted). Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

A fresh order of each study below was answered by the benchmark-level normal library, which contradicted this patient (age, rhythm, devices, surgery, stored findings). Each now has a case-specific report:

- FDG_PET: Bilateral, symmetric strip-like hypometabolism along the anterior-middle and middle-posterior cerebral border zones, a pattern consistent with bilateral border-zone (watershed) injury; territory cores and the posterior cingulate preserved. (fallback_tool_outputs.advanced_imaging)
- perfusion_SPECT: Bilateral, symmetric strip-like hypoperfusion along the anterior-middle and middle-posterior cerebral border zones, a pattern consistent with bilateral border-zone (watershed) injury; territory cores and the posterior cingulate preserved. (followup request_perfusion_spect)
- performance_status: Karnofsky 70 (cares for self; unable to carry on normal activity or active work), ECOG 1 (restricted in strenuous activity, able to carry out light work). (fallback_tool_outputs.clinical_assessment)
- exercise_stress_test: Reduced exercise capacity (4.4 METs); ST segments not interpretable for ischaemia because of the resting repolarisation abnormality. (fallback_tool_outputs.specialized_test)
- gait_and_balance_timed: Mildly slowed, cautious gait (Timed Up and Go 14.2 s) with reduced balance reserve. (followup request_gait_and_balance_timed)
- levodopa_challenge: MDS-UPDRS III 9/132 OFF and 9/132 ON (0% change), below the 30% threshold for a clinically meaningful levodopa response. (followup request_levodopa_challenge)
- TEE: Normally functioning aortic bioprosthesis; mild concentric left ventricular hypertrophy; mildly dilated left atrium. No patent foramen ovale and no left atrial appendage thrombus. (fallback_tool_outputs.echo)
- cardiac_MRI: Concentric left ventricular hypertrophy (septum 13 mm) with preserved function (LVEF 57%), aortic bioprosthesis and mildly dilated left atrium; no scar. (followup request_cardiac_mri)
- DTI_tractography: Bilateral reduced fractional anisotropy along the deep border zones involving the centrum semiovale segments of both corticospinal tracts and the posterior arcuate fasciculi; optic radiations intact. (followup request_dti_tractography)
- CT_perfusion: Matched perfusion defects confined to chronic tissue loss (superior frontal and paracentral border zones bilaterally; parieto-occipital border zones bilaterally); no acute core or penumbral mismatch. (followup request_ct_perfusion)
- perfusion_MRI: Matched perfusion defects confined to chronic tissue loss (superior frontal and paracentral border zones bilaterally; parieto-occipital border zones bilaterally); no acute core or penumbral mismatch. (followup request_perfusion_mri)
- chest_abdomen_pelvis_CT: No mass or lymphadenopathy. Clear lungs without nodule, consolidation or interstitial abnormality; median sternotomy wires; bioprosthetic aortic valve. (fallback_tool_outputs.body_imaging)
- chest_CTA: No pulmonary embolism or aortic dissection. Clear lungs without nodule, consolidation or interstitial abnormality; median sternotomy wires; bioprosthetic aortic valve. (followup request_chest_cta)
- mediastinum_CT: No mediastinal mass or lymphadenopathy; median sternotomy wires; bioprosthetic aortic valve. (followup request_mediastinum_ct)
- chest_xray: No acute cardiopulmonary abnormality; median sternotomy wires; aortic valve prosthesis. (followup request_chest_xray)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k VASC-DEM-M06` pass; criterion outputs unchanged against the pre-pass snapshot; no 60-character window of any expected_evidence in the new reports; synonym guard 0 changes.
