# VASC-DEM-M02
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | VASC-DEM was never annotated; no note ids exist for this case. All changes below come from the condition plan and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-5-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key (plus `protocol`, `contrast`) made the required MRI unmatchable. | FIXED: `analyze_brain_mri {}`. |
| D | major | `action-7-search-medical-literature`, `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search` | Plan C2: literature criterion leaking its expected evidence into its own output. | FIXED: criterion deleted; initial null; fallback deleted. |
| C | minor | `action-8-check-drug-interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group D: generic optional drug check; amlodipine, pantoprazole and thiamine carry no interaction that changes management (the pantoprazole-B12 point is handled as a must). | FIXED: criterion and fallback deleted; initial stays null. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: exam gave the MoCA total and item losses. | FIXED: bedside observation (orientation, slowing, no confabulation, partial insight), "Formal cognitive screening reported separately." |
| B | major | `initial_tool_outputs.clinical_assessment.findings`, `.impression` | MoCA arithmetic: the listed losses (trail, cube, digit span, serial sevens, fluency, recall 3, date) total 9, i.e. 21 raw and 22 after the education point for 11 years; the case says 21. | FIXED: clock 2/3 (hands misplaced) added as a tenth lost point, impression states "20/30 raw plus 1 point for 11 years of education" = 21/30; findings give each MoCA item; letter fluency (7 words) separated from animal fluency (10). |
| D | major | `initial_tool_outputs.clinical_assessment.impression`, `.criteria_met.progression_despite_reduced_alcohol` | Screen argued the attribution ("points to an additional vascular process rather than to alcohol alone"); a history-derived verdict in the structured fields. | FIXED: impression lists scores only; the `progression_despite_reduced_alcohol` key removed (the history carries it). |
| D | major | `initial_tool_outputs.mri.impression`, `.additional_observations`, `.volumetrics.mamillary_bodies`, `.findings[2].signal_characteristics.Sagittal_T1` | Plan C5: MRI said the SVD "accounting for the cognitive syndrome and the higher-level gait disorder", alcohol atrophy "accounting for the truncal component", "against Wernicke-Korsakoff pathology". | FIXED: numbered STRIVE-2 impression (Fazekas 3 P3/D2, 27 mL; three lacunes; one deep thalamic microbleed; superior vermian atrophy; normal mamillary bodies; MTA 1); vermian pattern hedged as "a pattern seen in alcohol-related cerebellar degeneration" (Kind 2); mamillary bodies "Normal volume". |
| D | major | `initial_tool_outputs.specialized_test.impression`, `.quantitative_data` | Neuropsych argued against Korsakoff and said "the pattern matches the small-vessel burden" (cross-modality). | FIXED: percentiles and a "Profile:" sentence; `korsakoff_features` replaced by `confabulation: none elicited`. |
| D | minor | `followup_outputs[0].output.impression`, `.findings[3]`, `.scores.10_metre_walk` | Gait report attributed each component to SVD, alcohol and neuropathy (cross-modality, diagnostic); "s per metre" unit. | FIXED: observations and timings only (TUG 16.8 s, 13.2 s over 10 m = 0.76 m/s, SPPB 7/12, step 36 cm, dual-task 26%, Romberg mildly positive). |
| D | minor | `patient.neurological_exam.sensory` | Exam named the cause ("consistent with alcohol-related polyneuropathy"). | FIXED: "in a length-dependent distribution". |
| C | major | `initial_tool_outputs.labs.panels.CBC` | Female Hb/Hct ranges in a man; "macrocytosis" in the interpretation and red herring with MCV 99.4 inside 80-100; template values. | FIXED: male ranges 13.5-17.5 / 41.0-53.0; Hb 13.9, Hct 41.2; MCV 102.6 flagged (supports the macrocytosis red herring); WBC 7.4, Plt 168 (alcohol), folate 6.4. |
| B | major | `initial_tool_outputs.labs.panels.CMP` | ALT 46 U/L above the 10-40 range but `is_abnormal` false; GGT and thiamine with interpretive `clinical_significance`; Na 139, K 4.2, albumin 4.1 template; eGFR ">60". | FIXED: ALT flagged; all `clinical_significance` null; Na 137, K 3.9, albumin 3.9; eGFR ">=60"; `abnormal_values_summary` rebuilt from the flags; interpretation "Flagged: ..." recital only. |
| D | minor | `fallback_tool_outputs.advanced_imaging`, `.labs`, `.ct`, `.echo` | Plan C7 off-pathway fallbacks; echo without `echo_type`, "No cardioembolic source". | FIXED: advanced imaging and labs fallbacks deleted; CT fallback describes this patient's CT (confluent hypodensity, thalamic and putaminal lacunes, vermian volume loss); echo `echo_type` TTE, descriptive impression. Holter fallback kept (pulse regular). |
| A | minor | `action_criteria[*]` rationale, citations, expected_evidence | Plan C13. | FIXED: case-specific rationales, one bracketed key, case values in expected evidence (gait label now "separate the components of the gait disorder"). |
| B | minor | `action_criteria` order, `stop_rule` | Plan C16: order screen, labs, gait, MRI, neuropsych; `max_additional_actions` 0. | FIXED: screen, gait (required, C14), neuropsych, labs, MRI; stop rule = these five; `max_additional_actions` 1. Soft screen-before-MRI kept. |
| B | minor | `avoided_actions` rationales | Plan C18. | FIXED: CT canonical text; EEG notes the provoked withdrawal seizure; echo and monitoring rationales name the lacunar pattern and regular pulse. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were mostly diagnostic steps ("Obtain brain MRI", "Document the cognitive profile", "Separate the components"); smoking, lipids, B12, home safety absent. | FIXED: six musts: explain subcortical VaD with alcohol contributing to gait [VASCOG_2014]; BP below 130/80 gradually from 164/94 with supervised dosing and orthostatic checks [ESO_2021_SVD]; abstinence support with thiamine; B12 replacement or MMA (214 pg/mL, PPI, neuropathy) and PPI review; smoking cessation and a statin (LDL 128 untreated); gas and finances safety and a falls programme. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | No covert-SVD antiplatelet prohibition (C19). | FIXED: added "Do not start an antiplatelet for covert small-vessel disease alone [ESO_2021_SVD]"; glucose-before-thiamine reworded to "without thiamine cover"; others kept. |
| C | major | `ground_truth.differential[0]`, `[3]` | Plan C8: alcohol-related dementia `moderate` although the case excludes it as the cause; hepatic encephalopathy features garbled ("normal ammonia not required"). | FIXED: alcohol-related dementia `low` (contributor, not sole cause); HE features cite albumin and the exam. |
| B | minor | `ground_truth.red_herrings[0..1]` | Empty field path; macrocytosis pointed to the CMP. | FIXED: `patient.clinical_history.past_medical_history[1]`; macrocytosis herring points to `initial_tool_outputs.labs.panels.CBC`. |
| E | minor | `ground_truth.diagnosis.accepted[0]`, `key_clinical_evidence[1]` | Em dashes in existing text. | FLAGGED: label not edited (ruling 3); KCE prose correct, left as is. |
| - | check | plan 3.6 | perfect_agent ok; probe: every criterion answered by case data; CT and echo answered by case fallbacks; `case_io.py check` and test_case_guards list no failure naming M02. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case stays subcortical vascular dementia in a 66-year-old former heavy drinker whose decline progressed while intake fell, with untreated hypertension (164/94), Fazekas 3, three lacunes and one deep microbleed, plus superior vermian atrophy and a length-dependent neuropathy. Reports no longer make the attribution: the MRI lists STRIVE-2 findings, the neuropsychology a profile without the Korsakoff argument, the gait test measurements without assigning causes, and the screen its scores (MoCA corrected to add up: 20 raw plus 1 for education = 21). Labs now use male ranges, MCV 102.6 is genuinely macrocytic and flagged, ALT 46 is flagged. The literature and drug steps are gone, the MRI criterion matches any MRI order. Musts are now management: explain the diagnosis, BP below 130/80 gradually with orthostatic checks, alcohol abstinence with thiamine, B12 replacement or MMA (PPI, neuropathy), smoking cessation and a statin, and home and falls safety; antiplatelets for covert SVD are prohibited. Alcohol-related dementia is now low on the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.1): the `F01` entry appends `F06.7` to this dementia case.
- `perfect_agent.py -v` "<- ?" display for outputs with null fields (see M01 log).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: MoCA arithmetic (10 points lost, 20 raw + 1 for 11 years = 21/30) against findings, impression and expected evidence; male ranges and every `is_abnormal` flag against its range (MCV 102.6, ALT 46, GGT 118, HbA1c 5.8, lipids); summary and interpretation match the flags; B12 214 handled by a must; criteria order, tiers (gait required per C14), stop rule; musts vs prohibitions (no antiplatelet for covert SVD; thiamine cover); differential vs the final evidence; red-herring field paths; fallbacks.

Found and changed:
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.mri.findings[0].size`, `.signal_characteristics.T2_FLAIR`, `.impression`; `fallback_tool_outputs.ct.impression` | The worker's new "Fazekas 3 (periventricular 3, deep 2)" makes the deep grade beginning-confluent while the location says confluent deep white matter and the whole case argues from a confluent Fazekas 3 burden (27 mL). | FIXED: "Fazekas 3 (periventricular 3, deep 3)", FLAIR "irregular periventricular hyperintensity extending into the deep white matter, with large confluent deep areas"; CT fallback "confluent periventricular and deep" (no "patchy"). |

perfect_agent ok; `case_io.py check` and test_case_guards list no failure naming M02.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.CMP[eGFR]` | eGFR 84 did not follow from creatinine 0.92 mg/dL in a man of 66 (CKD-EPI 2021 about 92); same class the verifiers fixed in P03, P05, P07. | FIXED: eGFR 92 (not quoted elsewhere). |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3-order-advanced-imaging].rationale`, `[avoid-waste-4-interpret-labs].rationale` | Plan C18: the MIBG and paraneoplastic/autoimmune rationales were still the August template text shared by M01-M06; the autoimmune one described "a chronic stepwise decline with a hypertensive imaging burden", which is wrong for this case. | FIXED: case-specific one-liners (no Lewy features; three-year progressive decline with hypertension and past heavy drinking). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, executive_predominant_profile, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall. The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here subcortical small-vessel labels and F01.2/I67.3. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
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

- FDG_PET: Bilateral frontal and anterior cingulate hypometabolism with focal left thalamic and right putaminal reduction and reduced superior vermian uptake; posterior association cortex relatively preserved. The cerebral pattern is consistent with subcortical small-vessel disease. (fallback_tool_outputs.advanced_imaging)
- perfusion_SPECT: Bilateral frontal and anterior cingulate hypoperfusion with focal left thalamic and right putaminal reduction and reduced superior vermian uptake; posterior association cortex relatively preserved. The cerebral pattern is consistent with subcortical small-vessel disease. (followup request_perfusion_spect)
- performance_status: Karnofsky 60 (requires occasional assistance but able to care for most needs), ECOG 2 (ambulatory and capable of all self-care, unable to carry out any work activities). (fallback_tool_outputs.clinical_assessment)
- exercise_stress_test: Reduced exercise capacity (4.6 METs) limited by unsteadiness; submaximal heart rate, non-diagnostic for ischaemia. (fallback_tool_outputs.specialized_test)
- levodopa_challenge: MDS-UPDRS III 16/132 OFF and 15/132 ON (6% change), below the 30% threshold for a clinically meaningful levodopa response. (followup request_levodopa_challenge)
- TEE: Mild concentric left ventricular hypertrophy; aortic valve sclerosis without stenosis. No patent foramen ovale and no left atrial appendage thrombus. (followup request_tee)
- emg_ncs: Length-dependent, sensory-predominant axonal sensorimotor polyneuropathy of moderate severity. (followup request_emg_ncs)
- ssep: Delayed lower-limb responses with normal central conduction times, indicating peripheral slowing in the legs; upper-limb and central pathways normal. (followup request_ssep)
- skin_biopsy_iencf: Reduced distal intraepidermal nerve fibre density with a length-dependent gradient. (followup request_skin_biopsy_iencf)
- DTI_tractography: Diffusely reduced white matter fractional anisotropy involving the corticospinal tracts, arcuate fasciculi and optic radiations, without tract interruption. (followup request_dti_tractography)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k VASC-DEM-M02` pass; criterion outputs unchanged against the pre-pass snapshot; no 60-character window of any expected_evidence in the new reports; synonym guard 0 changes.
