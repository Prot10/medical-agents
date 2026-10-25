# NPH-P05
Reviewer status: R1 none, R2 none (NPH was never annotated; no notes file; the only physician input is the July 2026 tool review, `condition_tool_guidance.yaml` key `nph`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer note exists for this case. The July 2026 tool-review rulings (MRI with NPH markers required; tap test with opening pressure and pre/post gait required; generic CSF assays, advanced imaging and neuropsychology removed; labs optional) are applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.csf.appearance` | "Xanthochromic, faint yellow tinge (expected in chronic post-SAH CSF)": wrong. Xanthochromia after SAH clears within weeks; 4 years later, with protein 62 mg/dL, CSF is clear. A yellow CSF here would point to a new bleed. | FIXED: "Clear, colorless". The metadata red herring built on it was replaced (below). |
| C | major | `patient.clinical_history.medications[Verapamil].indication`, `patient.history_present_illness` | Verapamil "for post-SAH vasospasm prevention" and nimodipine "switched to verapamil for maintenance" 4 years on: vasospasm prophylaxis is a 21-day nimodipine course; there is no maintenance phase. | FIXED: verapamil indication "hypertension"; HPI "treated with a 21-day course of oral nimodipine; his hypertension has since been treated with verapamil". Aspirin indication "cardiovascular risk reduction". |
| C | minor | `patient.history_present_illness` | "basal, extensive (Fisher grade 4)": Fisher 4 means intracerebral or intraventricular clot, not extensive basal blood. | FIXED: "thick basal subarachnoid blood and intraventricular extension (modified Fisher grade 4)" (a known hydrocephalus risk, consistent with secondary NPH). |
| D | major | `patient.history_present_illness`, `.chief_complaint` | HPI gave the outside MRI's Evans 0.34, callosal angle 84 degrees and "siderosis visible on current SWI" (the index MRI result), "requesting NPH evaluation", "following shunt-free"; chief complaint "requesting NPH evaluation" (C3). | FIXED: outside MRI "reported as showing enlarged ventricles; the images are not available"; referral wording without NPH or shunt. |
| C | major | `patient.history_present_illness` | "Aspirin must be held before LP": management inside the patient block, and wrong for low-dose aspirin [ASRA_2018]. | FIXED: deleted; the correct plan is a must and a prohibition. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | Exam gave TUG, 10-m, MoCA and recall score (C4). | FIXED: qualitative only, "reported separately". Cranial-nerve sentence reworded (resolved right third nerve palsy), content unchanged. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline gait report contained the post-tap results, "positive tap test" and engineering keys (C6). | FIXED: baseline only (TUG 28 s, 10-m 22 s, MoCA 21/30; freezing, en-bloc turn, retropulsion, urgency). |
| A | major | `followup_outputs`, `ground_truth.action_criteria` | No post-tap reassessment and no cognitive screen output (C6). | FIXED: `request_post_reassessment` (recommended criterion) and `request_moca_cognitive_screen` (optional; subscores sum to 21, serial 7s with two errors and date with prompting as in the exam). |
| B | minor | `initial_tool_outputs.csf` | "RBC 2 (traumatic vs old)"; interpretation a recital (C5, plan P05). | FIXED: "RBC 2/mcL"; canonical interpretation with the case's figures; protein 62 given against the age reference 15-60 and called mildly raised. |
| D | major | `initial_tool_outputs.mri` | "Partial DESH" with no components; duplicate periventricular findings; no technique, temporal horns, aqueduct or MTA (C7). | FIXED: DESH stated absent (common in secondary NPH), supportive features acute callosal angle 84 degrees and temporal horns; periventricular caps with Fazekas 1; patent aqueduct; superficial siderosis; coil artefact; MTA 1; technique line; canonical impression. |
| C | major | `followup_outputs[search_medical_literature]` x2, `[check_drug_interactions]` | Literature steps with fabricated outcome figures ("70-80% improvement", "secondary NPH responds better"); drug check advising "Hold aspirin 5-7 days" (C1, C2). | FIXED: deleted; aspirin and depression points became musts. |
| B | minor | `initial_tool_outputs.labs` | HIV row with engineering `clinical_significance`; RPR filed under "Metabolic" (C9). | FIXED: "Serology" panel holds RPR and HIV, all `clinical_significance` null, factual interpretation. |
| B | minor | `fallback_tool_outputs.ct` | CT fallback normal against ventriculomegaly and the coil (C18). | FIXED: enlarged ventricles (Evans about 0.34) and coil with streak artefact. |
| C | major | `ground_truth.assessment` | Five process musts; a classification must; wrong DESH/triad prohibition; AD and normal-ageing prohibitions (C11, C12). | FIXED: musts are referral for secondary post-SAH hydrocephalus with figures, continue aspirin [ASRA_2018], continue sertraline; prohibitions canonical ventriculomegaly, do not label it idiopathic, do not stop aspirin, do not attribute the decline to depression or static sequelae. |
| C | major | `ground_truth.differential` | VCI high; PD, AD, atrophy moderate; the diagnosis itself ("post-SAH communicating hydrocephalus") listed as a moderate alternative (C13). | FIXED: iNPH low (antecedent exists), post-SAH depression low, superficial siderosis syndrome low (the case raises siderosis), VCI, PD, AD, atrophy low. |
| B | minor | `ground_truth.red_herrings` | Empty, while the metadata named xanthochromia and depression as confounders. | FIXED: depression and the prior SAH as grounded red herrings. |
| A | minor | `ground_truth.action_criteria`, `avoided_actions`, `sequence_constraints`, `stop_rule`, `key_clinical_evidence` | Literature criterion, four-panel labs, label = rationale, bare citations, no advanced-imaging/neuropsychology/generic-assay avoided entries, max 0; tier sentence and "sensitivity 50-80%" (C1, C9, C10, C19). | FIXED: plan 3.1-3.5 structure; key evidence from F4, F6, F7 with the case figures. |
| E | minor | `metadata.vocab_gap`, `.difficulty_variant_description`, `.difficulty_rationale` | Stale phase-contrast vocab note; "CSF xanthochromia as red herring" and "coil stability required before shunt" (no step tests it); counts out of date (C19). | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

This is secondary NPH four years after a coiled right PCOM aneurysm SAH with intraventricular extension. Three clinical errors were corrected: the CSF is now clear (xanthochromia cannot persist for years), verapamil is for hypertension (nimodipine was a 21-day course, there is no vasospasm maintenance), and the Fisher grade matches the description. The patient block no longer gives the outside MRI measurements, the SWI result or an aspirin instruction. The work-up reads brain MRI, optional labs, baseline timed gait, optional MoCA, tap test and post-tap reassessment. MRI: Evans 0.34, callosal angle 84 degrees, temporal horns enlarged, DESH absent, superficial siderosis, coil artefact, Fazekas 1, MTA 1. Tap: opening pressure 18 cmH2O, normal cells, protein 62 mg/dL, 40 mL removed, TUG 28 to 20 s (29%), 10-m walk 22 to 16 s, MoCA 21 to 24, no incontinence. Musts: shunt referral naming the SAH antecedent, continue aspirin through the tap, continue sertraline. Prohibitions: no NPH from ventriculomegaly alone, not idiopathic, do not stop aspirin, do not blame depression or static sequelae. The differential (iNPH, depression, superficial siderosis syndrome, VCI, PD, AD, atrophy) is all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[Nakajima_2021]` and `[ASRA_2018]` used per plan 1.1 (CENTRAL R2).
- Post-tap criterion pattern equals the baseline criterion (plan R4).

## Open questions for Andrea (judgment calls you could not settle)

None. No falls are documented, so no falls must was added (he lives alone; the referral must covers the risk).

## Verification
Adversarial verifier, 24 Oct 2026. No reviewer notes exist for NPH. Read the log, the diff against the pre-round version and every clinical field of the final case. Checked: the three clinical corrections (clear CSF 4 years after SAH, verapamil for hypertension after a 21-day nimodipine course, modified Fisher 4 with intraventricular extension) are correct; tap figures (TUG 28/22/20 s = 21%/29%, 10-m 22/16 s = 27%, MoCA 21/24) identical across CSF report, follow-up, criteria, musts and key evidence; MoCA subscores sum to 21 (serial 7s with two errors correctly scores attention 5/6; orientation 5/6 matches "knows the date with prompting"); label secondary NPH with G91.0 first; aspirin must and prohibition per ASRA_2018; red-herring timeline (decline 2 to 3 years after the SAH) consistent with 4 years minus 18 months; no falls documented, so no falls must is correct.
Found and fixed:
- `fallback_tool_outputs.ct.impression`: the coil was in the findings but not in the impression (plan C18 asks for the case's own lesions). Impression now names the right posterior communicating artery coil with streak artefact.
- `fallback_tool_outputs.echo`: no `echo_type` (PATTERNS 5). Set to "TTE".
No other defect found. Checks run after the edits: `perfect_agent.py -v` passes (every required and recommended criterion served by a case output, no fallback or library answer); `case_io.py check` clean for the case; `test_case_guards -k` passes (leak, follow-up and banned-string guards); MockServer hijack sequence (cognitive screen, then baseline gait "before tap test", MRI, CSF "large-volume lumbar puncture", post-tap reassessment, second CSF call) returns the baseline, the tap report and the post-tap follow-up in the right places; patient-block grep for Evans, callosal, DESH, NPH, hydroceph, tap, shunt, TUG, MoCA finds only hits allowed by C3/C4.

## Condition audit (NPH auditor, 24 Oct 2026)
- `action-post-tap-gait-reassessment.rationale` was the template sentence shared verbatim by P03 to P07; now case-specific (tap volume and what the reassessment separates).
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.2 and the bare labels "normal pressure hydrocephalus" and "NPH" removed, because with token matching they credited "idiopathic NPH", the wrong answer for a case with an antecedent; now credits "secondary NPH" / "secondary normal pressure hydrocephalus", "communicating hydrocephalus", G91.0, G91.9 and labels naming the SAH antecedent (`SAH NPH`, `haemorrhagic NPH`, `subarachnoid NPH` and long forms).
- Aspirin must (and key evidence): `[ASRA_2018]` -> `[ASRA_2025]` (statement unchanged: aspirin and NSAIDs need no interruption).
- `key_clinical_evidence`: the 10% TUG threshold is no longer attributed to `[Nakajima_2021]`, which sets no numeric tap-test cut-off; it is stated as a commonly used threshold that no guideline fixes (the tap protocol keeps its Nakajima citation where the sentence states it).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` clean, `test_case_guards -k NPH-` pass. Not yet in `DISCRIMINATOR_CONDITIONS`: the post-tap follow-up's prose `assessment_type` is deliberate until the timing discriminator lands (CENTRAL C2 in the decisions file).

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (timing discriminator, NPH R4; decisions Q2 and CENTRAL C2). No clinical text changed.

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment.timing` | added `baseline` |
| `followup_outputs[1]` (`request_post_reassessment`) | `assessment_type` "gait_and_balance_timed (post-tap reassessment)" -> `gait_and_balance_timed`; `timing: post_intervention` added |
| `ground_truth.action_criteria[action-6-perform-clinical-assessment]` | `required_arguments.timing: baseline` (the schema default, so a call that omits it still matches; a post-tap call no longer does) |
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
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: MDS-UPDRS III 18 to 17 (6%); gait, gait initiation, turning and postural stability unchanged; no clinically meaningful levodopa response (below 30%) (followup_outputs[2] request_levodopa_challenge). Why: the library describes a normal motor examination and gait; this patient has a gait disorder, and the challenge shows little or no levodopa response.
- `order_specialized_test {test_type: neuropsych_battery}`: frontal-subcortical profile of mild severity (slowed processing, executive and attention deficits, recognition relatively preserved) (fallback_tool_outputs.specialized_test). Why: the library reports normal cognition in every domain; this patient has documented cognitive impairment on the stored bedside screen.
- `order_specialized_test {test_type: exercise_stress_test}`: submaximal non-diagnostic test, stopped at 2.3 METs for gait unsteadiness with freezing on the moving belt (followup_outputs[3] request_exercise_stress_test). Why: the library describes a 9.5-minute Bruce protocol at 10.4 METs; this patient's gait disorder (magnetic gait with falls) does not allow it.
- `order_echocardiogram {echo_type: exercise_echo}`: submaximal non-diagnostic study stopped at 2.3 METs; resting findings as on the stored TTE (followup_outputs[4] request_exercise_echo). Why: the library describes 9.5 METs on a treadmill with a normal echo; this patient's gait disorder does not allow it.
- `order_advanced_imaging {modality: cerebral_angiography}`: coiled right PCOM aneurysm completely occluded, no recanalisation or new aneurysm (fallback_tool_outputs.advanced_imaging). Why: the library reports no aneurysm; the patient had a right posterior communicating artery aneurysm treated by coiling and the stored MRI and CT show the coil.
- `order_advanced_imaging {modality: MR_angiography}`: coil artefact at the right PCOM aneurysm without flow in the sac; no new aneurysm (followup_outputs[5] request_mr_angiography). Why: the library reports no aneurysm; the patient had a right posterior communicating artery aneurysm treated by coiling and the stored MRI and CT show the coil.
- Checks: perfect agent ok; case guards pass; criteria answers unchanged.
