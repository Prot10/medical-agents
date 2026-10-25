# NPH-M03
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `nph`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for NPH. The case was corrected against plan NPH (classes C1 to C20) and the July 2026 tool review. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, criterion `action-1-search-medical-literature` | Recommended literature criterion with a stored output repeating its expected_evidence (leak, C1). | FIXED: criterion deleted; initial and fallback literature null. |
| C | major | criterion `action-6-check-drug-interactions`, `followup_outputs[0]` (`request_drug_interactions_shunt_anticoagulation`) | Recommended drug check whose output gave wrong DOAC advice (48 h hold, heparin "bridging", restart 24-48 h) as a tool result (C2, F7). | FIXED: criterion and follow-up deleted; drug-interaction initial and fallback null; the DOAC plan is now a must per ASRA 2018 (hold at least 72 h, restart no sooner than 6 h, no bridging, weighed against CHA2DS2-VASc 4 with prior stroke). |
| C | major | `ground_truth.assessment.required_recommendations[5]`, `.prohibited_recommendations[4]` | Must "hold DOAC 24-48 hours" contradicts ASRA 72 h; prohibition "hold and reverse per protocol" implies reversal for an elective tap. | FIXED: replaced by the canonical DOAC must and prohibition ("Do not perform the lumbar tap while apixaban is active and do not bridge with heparin"). |
| D | major | `patient.chief_complaint`, `patient.history_present_illness` | "Admitted for NPH evaluation" (twice), "Evans index 0.34 out of proportion to cortical atrophy", "referred for NPH evaluation" (C3). | FIXED: complaint lists the symptoms; HPI says a repeat outside MRI 2 months ago was reported as showing enlarged ventricles, images not available. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 32 s, 10-metre walk 26 s, MoCA 20/30, delayed recall 2/5 and trail-making in the exam (C4); right arm weakness repeated in mental status. | FIXED: qualitative gait (start hesitation added, as the HPI describes); mental status "slowed responses ... formal cognitive screening reported separately", dysarthria kept, no aphasia stated; weakness stays in `motor`. |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Pre-tap call returned the post-tap result, "positive tap test", engineering keys (C6). | FIXED: baseline only (TUG 32 s, 10-metre walk 26 s in 34 steps, turn 8 steps, MoCA 20/30, right circumduction noted), `criteria_met` and `pre_post_comparison` null. |
| A | major | `followup_outputs` | No post-tap reassessment, no case cognitive screen (C6). | FIXED: `followup_outputs[0]` cognitive screen (MoCA 20/30 itemised to sum 20, recall 2/5 free and 4/5 cued); `followup_outputs[1]` post-tap reassessment (TUG 28 s at 2 h, 26.5 s at 24 h, 10-metre walk 21 s, MoCA 20, circumduction unchanged; identical to CSF). |
| C | major | `initial_tool_outputs.mri.findings[1]`, `.impression` | Old infarct placed in left temporal and inferior parietal cortex, which does not explain right hand and face weakness, right leg spasticity, Babinski and tongue deviation, and in a right-hander would be expected to leave aphasia, which the exam does not show (PATTERNS 3, deficits no lesion explains). | FIXED: chronic infarct in the left precentral gyrus and underlying corona radiata (MCA superior-division territory) with Wallerian degeneration of the corticospinal tract, perisylvian language cortex not involved; CT fallback matches. |
| C | major | `initial_tool_outputs.mri` | DESH called "partially present" although both components were described; no technique, temporal horns, hippocampi, aqueduct, DWI statement for a new decline; "unchanged from prior" without an available prior; "moderate-severe" WMH without a grade (C7). | FIXED: DESH stated as present (both components); technique; Evans 0.34; callosal angle 82; temporal horns enlarged, MTA 1; Fazekas 2; patent aqueduct with flow void; "No restricted diffusion; no new infarct"; no comparison wording; descriptive impression. |
| B | minor | `initial_tool_outputs.csf.protein`, `.cell_count.RBC` | Protein 52 mg/dL above the usual range while F3 requires normal content; RBC without unit. | FIXED: protein 43 mg/dL; "3 cells/mcL". |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | Prose with "improved" (C5). | FIXED: canonical interpretation with the case's figures (17% at 24 h, MoCA 20 to 20). |
| C | major | `initial_tool_outputs.labs.panels.Coagulation`, `.interpretation`, `.abnormal_values_summary` | Anti-Xa row flagged high with a "trough" reference: not part of this work-up (C9). HIV under "Baseline workup". | FIXED: anti-Xa removed (INR kept); RPR and HIV in `Serology`; all `clinical_significance` null; interpretation states the normal pattern. |
| C | major | `ground_truth.action_criteria` | As M01; plus the drug criterion. | FIXED: MRI (required), labs `{}` (optional; rationale names renal function for the apixaban hold), baseline gait `action-7-perform-clinical-assessment` (required), cognitive screen (optional), CSF (required), post-tap (recommended). |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | As M01. | FIXED: canonical hard and soft constraints; stop rule three required ids, `max_additional_actions` 1. |
| B | minor | `ground_truth.avoided_actions` | Advanced imaging, neuropsych and generic CSF assays not guarded; ECG, echo and monitoring rationales ignored the known AF. | FIXED: three entries added; rationales say the AF is already known and anticoagulated, the stroke source already treated. |
| C | major | `ground_truth.assessment.required_recommendations` | Process musts (C11). | FIXED: referral on the 17% response with DESH and normal-pressure CSF; DOAC must; falls (two falls); counselling that the post-stroke weakness and circumduction will not respond (the tap left them unchanged). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong DESH/triad prohibition; AD prohibition copied (C12). | FIXED: LP-before-MRI, canonical ventriculomegaly-alone, DOAC, "do not attribute the new decline to the old stroke or small-vessel disease alone", normal ageing (five). |
| C | major | `ground_truth.differential` | VCI `high`; PD, AD, atrophy `moderate` (C13). | FIXED: VCI `moderate` (infarct and Fazekas 2 contribute); PD, AD (MTA 1), atrophy (DESH, acute angle) and secondary hydrocephalus (ischaemic, not haemorrhagic, stroke) `low`. |
| C | major | `ground_truth.key_clinical_evidence` | Template items with wrong DESH requirement, 50-80% sensitivity, tier sentence. | FIXED: six case items including the stable post-stroke baseline, DESH, the tap figures, Marmarou figures, Tisell and the ASRA apixaban hold. |
| B | minor | `ground_truth.red_herrings[0]` | Data point not visible as written; interpretation said the baseline "acutely worsened" and called the ventriculomegaly "new" (the decline was over 10-12 months and no prior image is available). | FIXED: data_point quotes the PMH entry; interpretation rewritten. |
| B | minor | `fallback_tool_outputs.ct` | "No established infarct" and normal ventricles (C18). | FIXED: ventriculomegaly (Evans about 0.34), old left precentral and corona radiata infarct, periventricular hypodensity. |
| B | minor | `fallback_tool_outputs.ecg` | "Benign incidental finding" wording. | FIXED: "Sinus rhythm with borderline left axis deviation" (sinus rhythm fits paroxysmal AF, C18). Echo `echo_type` "TTE". |
| E | minor | `metadata` | Variant description said the single tap was "equivocal-negative but extended drainage confirms diagnosis" (no drainage in the case; tap 17%); stale vocab gap and counts. | FIXED: rewritten; vocab gap and literature kind removed. |
| - | check | plan 3.6 | perfect_agent ok; test_case_guards pass; hijack probe as M01 (baseline served before the tap, follow-up after); CT and ECG fallbacks consistent; patient grep clean. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The patient block no longer names NPH or gives the Evans index, TUG, 10-metre walk or MoCA. The old left MCA infarct is now placed where it explains the deficits (left precentral gyrus and corona radiata, with Wallerian degeneration, language cortex spared), and the MRI reports DESH (both components), an acute callosal angle of 82 degrees, Evans 0.34, enlarged temporal horns, Fazekas 2, a patent aqueduct and no new infarct, without naming a disease. The baseline gait report (TUG 32 s, 10-metre walk 26 s, MoCA 20/30, right circumduction) is separate from the post-tap reassessment and the CSF report (TUG 28 s at 2 hours, 26.5 s at 24 hours, 17%; 10-metre walk 21 s; circumduction and MoCA unchanged). CSF protein corrected to 43 mg/dL. The drug-check criterion, its wrong DOAC advice and the anti-Xa lab row are gone; the apixaban plan is a must (hold at least 72 hours, restart at 6 hours or later, no heparin bridging, weighed against CHA2DS2-VASc 4) with the matching prohibition. Musts also cover shunt referral on the tap response, falls prevention and counselling that the post-stroke deficits will not improve. VCI is moderate; PD, AD and atrophy low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[Nakajima_2021]` and `[ASRA_2018]` used per the plan's canonical texts, not yet in the NPH criteria pack.
- Plan R4: post-tap criterion shares the baseline pattern.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q3 (72 h ASRA hold vs a 48 h local practice) applies directly to this case; the case follows ASRA 2018.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the whole final case and its diff against fa1d22e6.
- Checked: the drug-check criterion and follow-up, anti-Xa row and hold text are gone; the DOAC must and prohibition follow F7 (apixaban at least 72 hours, restart no sooner than 6 hours, no bridging); CHA2DS2-VASc 4 is derivable (age 72 = 1, hypertension = 1, prior stroke = 2); aspirin allergy not contradicted anywhere. The infarct relocation is justified: the old temporal and inferior parietal site could not explain right hand and face weakness, tongue deviation, dysarthria, right leg spasticity and Babinski; the new left precentral and corona radiata site does, CT fallback and expected evidence agree, and the corona radiata component can carry the chronic right hemisensory loss. DESH present (both components) agrees with differential, prohibitions and key evidence. Figures identical across reports (TUG 32 to 28 s = 13%, to 26.5 s = 17%; 10-metre walk 26 to 21 s = 19%; MoCA unchanged at 20, items sum to 20). Sinus ECG and Holter fallbacks fit paroxysmal AF. MockServer probe: no leak.
- Found: nothing that needed a change. Noted only: the Holter fallback maximum of 129 bpm in sinus rhythm on metoprolol is high but possible and off-pathway.
- No edits. perfect_agent -v ok, case_io check clean for the case, test_case_guards pass.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
- Apixaban must, key evidence and prohibition: ASRA fifth edition (2025) supersedes the fourth (2018). Therapeutic apixaban is still held at least 72 hours before the tap, but the restart is now no sooner than 24 hours after the puncture (2018: 6 hours); citation `[ASRA_2018]` -> `[ASRA_2025] [ACCP_2022]` (ACCP 2022 for no heparin bridging).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` clean, `test_case_guards -k NPH-` pass. Not yet in `DISCRIMINATOR_CONDITIONS`: the post-tap follow-up's prose `assessment_type` is deliberate until the timing discriminator lands (CENTRAL C2 in the decisions file).

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (timing discriminator, NPH R4; decisions Q2 and CENTRAL C2). No clinical text changed.

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment.timing` | added `baseline` |
| `followup_outputs[1]` (`request_post_reassessment`) | `assessment_type` "gait_and_balance_timed (post-tap reassessment)" -> `gait_and_balance_timed`; `timing: post_intervention` added |
| `ground_truth.action_criteria[action-7-perform-clinical-assessment]` | `required_arguments.timing: baseline` (the schema default, so a call that omits it still matches; a post-tap call no longer does) |
| `ground_truth.action_criteria[action-post-tap-gait-reassessment]` | `required_arguments.timing: post_intervention`; importance recommended -> required (Reviewer 1: gait before and after the tap) |
| `ground_truth.sequence_constraints` | soft: `action-4-analyze-csf` before `action-post-tap-gait-reassessment` [Nakajima_2021] |
| `ground_truth.stop_rule.required_before_assessment` | `action-post-tap-gait-reassessment` added |

Scoring change for re-review: the post-tap reassessment is now required and is credited only by a call with `timing: post_intervention`; the baseline order is answered by the baseline report and the reassessment order by the post-tap report (MockServer secondary discriminator).

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 60, ECOG 2; requires occasional assistance; able to care for most personal needs (fallback_tool_outputs.clinical_assessment). Why: the library gives Karnofsky 100 / ECOG 0 (no evidence of disease, working) in a symptomatic patient.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: MDS-UPDRS III 26 to 25 (4%); gait, gait initiation, turning and postural stability unchanged; no clinically meaningful levodopa response (below 30%) (followup_outputs[2] request_levodopa_challenge). Why: the library describes a normal motor examination and gait; this patient has a gait disorder, and the challenge shows little or no levodopa response.
- `order_specialized_test {test_type: neuropsych_battery}`: frontal-subcortical profile of moderate severity (slowed processing, executive and attention deficits, recognition relatively preserved) (fallback_tool_outputs.specialized_test). Why: the library reports normal cognition in every domain; this patient has documented cognitive impairment on the stored bedside screen.
- `order_specialized_test {test_type: exercise_stress_test}`: submaximal non-diagnostic test, stopped at 2.3 METs for gait unsteadiness with freezing on the moving belt (followup_outputs[3] request_exercise_stress_test). Why: the library describes a 9.5-minute Bruce protocol at 10.4 METs; this patient's gait disorder (magnetic gait with falls) does not allow it.
- `order_echocardiogram {echo_type: exercise_echo}`: submaximal non-diagnostic study stopped at 2.3 METs; resting findings as on the stored TTE (followup_outputs[4] request_exercise_echo). Why: the library describes 9.5 METs on a treadmill with a normal echo; this patient's gait disorder does not allow it.
- `order_advanced_imaging {modality: DTI_tractography}`: left corticospinal tract FA and volume loss below the chronic infarct (Wallerian degeneration) (fallback_tool_outputs.advanced_imaging). Why: the stored MRI and CT show a chronic left precentral and corona radiata infarct (with Wallerian degeneration on MRI), which this study would show.
- `order_advanced_imaging {modality: FDG_PET}`: focal left precentral hypometabolism at the chronic infarct, crossed cerebellar diaschisis (followup_outputs[5] request_fdg_pet). Why: the stored MRI and CT show a chronic left precentral and corona radiata infarct (with Wallerian degeneration on MRI), which this study would show.
- `order_advanced_imaging {modality: perfusion_SPECT}`: focal left precentral hypoperfusion at the chronic infarct (followup_outputs[6] request_perfusion_spect). Why: the stored MRI and CT show a chronic left precentral and corona radiata infarct (with Wallerian degeneration on MRI), which this study would show.
- `order_advanced_imaging {modality: perfusion_MRI}`: matched low perfusion in the chronic left precentral infarct; no other deficit (followup_outputs[7] request_perfusion_mri). Why: the stored MRI and CT show a chronic left precentral and corona radiata infarct (with Wallerian degeneration on MRI), which this study would show.
- `order_advanced_imaging {modality: CT_perfusion}`: no acute deficit; matched low perfusion within the chronic infarct (followup_outputs[8] request_ct_perfusion). Why: the stored MRI and CT show a chronic left precentral and corona radiata infarct (with Wallerian degeneration on MRI), which this study would show.
- `order_advanced_imaging {modality: functional_MRI}`: right-hand motor activation displaced to the infarct margins; left language dominance (followup_outputs[9] request_functional_mri). Why: the stored MRI and CT show a chronic left precentral and corona radiata infarct (with Wallerian degeneration on MRI), which this study would show.
- `order_specialized_test {test_type: ssep}`: attenuated right median N20 and delayed right tibial P37 (left hemispheric central pathway) (followup_outputs[10] request_ssep). Why: the library reports normal SSEPs; the patient has chronic right hemibody sensory loss and the stored imaging shows a left hemispheric infarct.
- `order_specialized_test {test_type: speech_language_evaluation}`: mild spastic dysarthria, no aphasia (followup_outputs[11] request_speech_language_evaluation). Why: the library reports no motor speech disorder; the examination documents chronic post-stroke dysarthria.
- Checks: perfect agent ok; case guards pass; criteria answers unchanged.
