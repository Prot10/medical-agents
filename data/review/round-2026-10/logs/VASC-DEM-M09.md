# VASC-DEM-M09
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (`plans/VASC-DEM.md`) and the worker's own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: `sequences`/`protocol`/`contrast` arguments made the required MRI unmatchable. | FIXED: `analyze_brain_mri {}`; label and citations now name SWI and the Boston rule. |
| D | major | criterion `action-8-search-medical-literature`, `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search` | Plan C2 / ruling 5. | FIXED: criterion deleted, initial null, fallback deleted. |
| C | minor | criterion `action-9-check-drug-interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group D: generic optional check with a generic fallback; no concrete interaction changes management. | FIXED: criterion deleted; initial already null; fallback deleted. |
| C | major | criterion `action-6-order-advanced-imaging` (carotid duplex), `initial_tool_outputs.advanced_imaging` | Plan C10: carotid imaging has no role after a hypertensive thalamic haemorrhage; the report also stated the mechanism ("substrate is hypertensive arteriopathy, not atherosclerosis"). | FIXED: criterion and initial output deleted; new avoided `avoid-waste-8-order-advanced-imaging` `{"modality": "carotid_duplex"}`, waste, plan rationale [AHA_ASA_2022_ICH]. Probed: a duplex order now returns the library's normal report. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: MoCA total and items in the exam. | FIXED: bedside observation, examined in Mandarin with family interpreting, "Formal cognitive screening reported separately". |
| B | major | `initial_tool_outputs.clinical_assessment` | MoCA arithmetic: listed losses with month-only orientation give 19 raw, and the 12-years-of-education point (MoCA adds 1 for 12 years or fewer) makes 20, not 19; `criteria_met` carried interpretive items (haemorrhagic substrate, onset within 3 months, IADL lost); impression stated the vascular attribution. | FIXED: orientation month and date (4/6), raw 18 + 1 = 19/30 itemised; `criteria_met` keeps impairment and `recall_improves_with_cueing` true; impression lists scores only, "administered in Mandarin"; fluency described as letter fluency. |
| D | major | `initial_tool_outputs.specialized_test.impression` | Plan C5: "matches thalamocortical disconnection rather than a degenerative cortical process". | FIXED: numbered domain profile without attribution. |
| D | major | `initial_tool_outputs.mri.additional_observations`, `.impression` | Plan C5: "the anatomy of the dysexecutive syndrome", "specifically not CAA", "the arteriopathy long predated the haemorrhage", "the distribution is hypertensive rather than amyloid". | FIXED: lesion anatomy and microbleed distribution stated as findings (deep/infratentorial, no lobar microbleed, no cSS) without the conclusion; numbered impression. Finding order unchanged (red-herring paths `findings[3]` and `findings[1]` still valid). |
| D | major | `initial_tool_outputs.ecg.findings`, `.interpretation` | Plan C5: "hypertensive end-organ damage", "corroborating long-standing untreated hypertension", embolic-mechanism argument. | FIXED: rhythm, axis, voltage LVH with secondary repolarisation change. |
| B | major | `initial_tool_outputs.labs` | Plan C6: female Hb/Hct ranges in a man (Hb 13.4 would then be low); template values; eGFR 64 does not match creatinine 1.06 at 74 (CKD-EPI 2021 gives 73); total cholesterol 178 vs Friedewald 167; interpretation "above target ... excluding reversible contributors ... renal function adequate". | FIXED: male ranges, Hb 14.2, Hct 42.4; WBC 7.1, Plt 226, MCV 86, Na 137, K 3.8 (on indapamide), ALT 26, albumin 4.3, folate 12.6; eGFR 73 with ">=60"; total cholesterol 167; interpretation a recital of flagged values. |
| C | major | criterion `action-3-interpret-labs.expected_evidence`, musts | "HbA1c 7.8% above target": wrong for a 74-year-old with dementia, whose individualised target is about below 8.0% (ADA 2025 Older Adults). | FIXED: expected evidence states the value only; new must to individualise the target to about below 8.0% with no intensification; prohibition against intensifying to below 7% at the cost of hypoglycaemia [ADA_2025_older_adults]. |
| B | minor | `fallback_tool_outputs.echo` | Mild LVH with normal LA and "No cardioembolic source" against marked ECG LVH. | FIXED: moderate concentric LVH (septum 14 mm), grade 1 diastolic dysfunction, mildly dilated LA; impression lists findings. |
| D | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, `.labs` | Plan C7. | FIXED: CT fallback describes the chronic thalamic cavity, white matter hypodensity and lacunes with the CT limitation; advanced-imaging and labs fallbacks deleted; `metadata.fallback_tool_kinds` trimmed. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated tool steps (MRI with SWI, exclude reversible causes, first-language testing) and gave no BP target, glycaemic or statin decision. | FIXED: seven musts: diagnosis on the temporal criterion [VASCOG_2014]; distribution rule, Boston v2.0 not met [Boston_v2]; BP below 130/80 from 158/92 with adherence support and resistant-hypertension work-up if adherent [AHA_ASA_2022_ICH]; HbA1c about below 8.0% [ADA_2025_older_adults]; continue atorvastatin [AHA_ASA_2022_ICH]; withhold antithrombotics without indication [AHA_ASA_2022_ICH]; rehabilitation, finances, driving and first-language reassessment. |
| E | minor | `ground_truth.assessment.prohibited_recommendations[3]` | "interpreter-free English or Italian instrument": odd template wording. | FIXED: "Do not interpret cognitive scores obtained without first-language administration and culture-appropriate norms." Em dash removed from the adherence prohibition. |
| C | major | `ground_truth.differential` | Plan C8: CAA moderate although the Boston criteria are not met; subcortical ischaemic VaD moderate although the onset is dated to the haemorrhage. | FIXED: both low with key features saying why. |
| C | minor | `ground_truth.avoided_actions` | Plan C18: generic rationales. | FIXED: case-specific rationales (haemorrhage, not ischaemia, for echo and monitoring; CT canonical text). |
| A | minor | all criteria | Plan C13. | FIXED: case rationales, bracketed keys, expected evidence without em dashes; ECG criterion label no longer calls AF "the embolic source". |
| B | minor | `ground_truth.action_criteria` order, `.stop_rule` | Plan C16. | FIXED: screen, neuropsych, labs, MRI, ECG; `max_additional_actions` 1. |
| B | minor | `ground_truth.key_clinical_evidence`, `.red_herrings[0]`, `metadata.key_educational_points[2]` | Em dashes; BP point without the target. | FIXED: reworded; KCE adds the HbA1c point. |

## Changes, in one paragraph a physician can read before re-reviewing

A 74-year-old man with a dysexecutive, abulic syndrome since a hypertensive right thalamic haemorrhage three months ago, on a background of severe small-vessel disease. The exam no longer gives the MoCA; the screen is itemised to 19/30 including the education point, and the screen, neuropsychology, MRI and ECG report only their own findings (the MRI states the deep and infratentorial microbleed distribution and the absence of lobar microbleeds and siderosis, leaving the Boston decision to the agent). The carotid duplex step is gone and is now waste. Literature and drug-check steps are gone. Labs carry male ranges, eGFR 73 matching the creatinine and non-template values. Musts now give the BP target below 130/80 with adherence support, an individualised HbA1c target of about below 8% (so 7.8% is not "above target"), continuation of atorvastatin, no antithrombotic, rehabilitation and first-language reassessment. CAA and subcortical ischaemic VaD are low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[AHA_ASA_2022_ICH]`, `[ADA_2025_older_adults]` (plan 5.4).
- Synonyms (plan 5.1): F06.7 should be removed from this dementia case's accepted codes.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial check (24 Oct 2026). No reviewer notes. Checked: MoCA items give 18 raw + 1 (12 years) = 19/30 and match the exam (month and date wrong); eGFR 73 matches creatinine 1.06 at 74; Hct 42.4 with Hb 14.2; Friedewald 167; the carotid criterion and output are gone and the carotid waste entry exists, with nothing else referring to them; microbleed and haemorrhage distribution (deep and infratentorial, no lobar, no cSS) supports the Boston v2.0 must and the CAA entry at low; ECG LVH agrees with the echo fallback (moderate LVH); sinus Holter fallback agrees with the regular pulse; HbA1c 7.8% within the individualised target in both must and prohibition; BP must per AHA 2022 ICH; red-herring paths still point to the microbleed and white matter findings.

Found and fixed: the worker changed the MoCA fluency item from "8 animals" to "letter fluency" and wrote "FAS" into the neuropsychology impression, but the screen and battery were administered in Mandarin, where a letter (FAS) task does not exist; Mandarin MoCA versions use animal naming for this item. Changed `initial_tool_outputs.clinical_assessment.findings[0].performance` to "verbal fluency 8 animals in 60 s (0/1, Mandarin version)", `.scores.verbal_fluency` to "8 animals in 60 s (Mandarin version)", the battery test "Letter fluency (FAS)" to "Category fluency (animals, Mandarin norms)" (4th percentile kept), and the battery impression to "Impaired verbal fluency ... (category fluency 4th, ...)". Point totals unchanged.

Checks re-run after my edits: `perfect_agent.py -v` passes (every required and recommended criterion answered by case data); `case_io.py check` clean for this case (schema, synonym guard, no test failure naming it). Note for the lead, not changed: `metadata.fallback_tool_kinds` still labels case-specific fallbacks (CT with this patient's lesions, AF Holter where present) as "normal"; the field is read by no code or test, so I left it rather than churn it.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here "post-stroke dementia". Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `[ADA_2025_older_adults]` -> `[ADA_older_adults_2026]` in the HbA1c must (same target below about 8.0%; superseded edition, as in ALZ-EARLY).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: ct normal->case, echo normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

A fresh order of each study below was answered by the benchmark-level normal library, which contradicted this patient (age, rhythm, devices, surgery, stored findings). Each now has a case-specific report:

- FDG_PET: Absent right thalamic metabolism with ipsilateral frontal-predominant hemispheric hypometabolism and crossed left cerebellar diaschisis, plus bilateral patchy frontal hypometabolism. No temporoparietal-predominant pattern. (fallback_tool_outputs.advanced_imaging)
- perfusion_SPECT: Absent right thalamic perfusion with ipsilateral frontal-predominant hemispheric hypoperfusion and crossed left cerebellar diaschisis, plus bilateral patchy frontal hypoperfusion. No temporoparietal-predominant pattern. (followup request_perfusion_spect)
- performance_status: Karnofsky 50 (requires considerable assistance and frequent care), ECOG 2 (ambulatory and capable of all self-care, unable to carry out any work activities). (fallback_tool_outputs.clinical_assessment)
- exercise_stress_test: Very low workload (2.0 METs) limited by hemiparesis; non-diagnostic for ischaemia. (fallback_tool_outputs.specialized_test)
- gait_and_balance_timed: Slow hemiparetic gait (Timed Up and Go 22.6 s with a stick) with impaired balance and a raised fall risk. (followup request_gait_and_balance_timed)
- levodopa_challenge: MDS-UPDRS III 18/132 OFF and 18/132 ON (0% change), below the 30% threshold for a clinically meaningful levodopa response. (followup request_levodopa_challenge)
- TEE: Moderate concentric left ventricular hypertrophy; mildly dilated left atrium; aortic valve sclerosis without stenosis. No patent foramen ovale and no left atrial appendage thrombus. (followup request_tee)
- cardiac_MRI: Moderate concentric left ventricular hypertrophy with preserved function and a mildly dilated left atrium; no scar or infiltration. (followup request_cardiac_mri)
- speech_language_evaluation: Reduced verbal initiation and output with preserved naming, repetition and comprehension; no aphasia and no dysarthria. (followup request_speech_language_evaluation)
- ssep: Absent cortical responses to left median and tibial stimulation with preserved cervical responses, indicating interruption of the right central somatosensory pathway above the cervical cord; left hemisphere pathways normal. (followup request_ssep)
- DTI_tractography: Attenuated right corticospinal tract at the internal capsule and interrupted right thalamocortical radiations, on a background of diffusely reduced white matter fractional anisotropy. (followup request_dti_tractography)
- CT_perfusion: Matched perfusion defects confined to chronic tissue loss (right thalamus (haemorrhage cavity)); no acute core or penumbral mismatch. (followup request_ct_perfusion)
- perfusion_MRI: Matched perfusion defects confined to chronic tissue loss (right thalamus (haemorrhage cavity)); no acute core or penumbral mismatch. (followup request_perfusion_mri)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k VASC-DEM-M09` pass; criterion outputs unchanged against the pre-pass snapshot; no 60-character window of any expected_evidence in the new reports; synonym guard 0 changes.
