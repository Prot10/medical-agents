# NPH-P04
Reviewer status: R1 none, R2 none (NPH was never annotated; no notes file; the only physician input is the July 2026 tool review, `condition_tool_guidance.yaml` key `nph`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer note exists for this case. The July 2026 tool-review rulings (MRI with NPH markers required; tap test with opening pressure and pre/post gait required; generic CSF assays, advanced imaging and neuropsychology removed; labs optional) are applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline gait report contained the post-tap TUG and MoCA, a "positive tap test" verdict, engineering `criteria_met` keys and the "case's own tap-trial report" sentence (C6). | FIXED: baseline only (TUG 38 s, 10-m 30 s, MoCA 17/30 same session; freezing, en-bloc turn, retropulsion, walker, urge incontinence); `criteria_met` and `pre_post_comparison` null. |
| A | major | `followup_outputs`, `ground_truth.action_criteria` | No post-tap reassessment step (C6). | FIXED: follow-up `request_post_reassessment` and recommended criterion `action-post-tap-gait-reassessment`. |
| B | minor | `initial_tool_outputs.csf.special_tests`, post-tap follow-up | The case had a baseline 10-m walk (exam) but no post-tap 10-m value, so the same measures were not repeated. | FIXED: 10-m walk 30 s to 25 s at 24 hours (17%) added, the same figure in the CSF report, the post-tap follow-up and the criteria. |
| D | major | `patient.history_present_illness` | HPI gave the index MRI's Evans index 0.35 and the referral diagnosis "superimposed NPH on bvFTD" (C3). | FIXED: repeat MRI "reported as showing enlarged ventricles; the images are not available"; prior Evans 0.27 kept (documents change, plan); referral question reworded without NPH. "caring neurologist" corrected to "treating neurologist". |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | Exam gave TUG, 10-m walk and MoCA (C4). | FIXED: qualitative gait and mental status, "reported separately". |
| C | major | `patient.neurological_exam.cranial_nerves`, `initial_tool_outputs.mri` | PSP carry-over (the PSP template of P07): "Upward gaze mildly slow, possible PSP feature noted", "hummingbird sign equivocal" and a mislabelled "midbrain-pons area ratio 0.54" (an area ratio is about 0.12 to 0.24; 0.54 is a diameter ratio). Slow vertical saccades with falls and pull-test instability would meet MDS probable PSP-RS, an entity the case never develops (label, red herrings, variant description, differential are all bvFTD). | FIXED: saccade velocity normal with upgaze range mildly limited for age; MRI "Midbrain and pons normal in size; no hummingbird sign"; PSP added to the differential as low with that reasoning. See Open questions. |
| D | major | `initial_tool_outputs.mri` | No technique, aqueduct, fourth ventricle, Fazekas or MTA; DESH "partial, confounded" without saying which component; impression a narrative (C7). | FIXED: technique and comparison lines; Evans 0.35 (0.27 prior); both DESH components with frontal sulci widened by atrophy; callosal angle 80; temporal horns; Fazekas 1; patent aqueduct; MTA 2; canonical numbered impression. |
| C | major | `followup_outputs[search_medical_literature]` x2 | `request_genetic_ftd_testing` and `request_goals_of_care_ftd_nph`: clinical steps disguised as literature searches, with unsupported figures ("~15% of cases") (C1). | FIXED: deleted; goals of care became a must. |
| B | minor | `followup_outputs` | No FDG PET output, so the library would return a normal FDG PET against a bvFTD case (C10). | FIXED: authored `FDG_PET` follow-up (bilateral frontal and anterior temporal hypometabolism, parietal and posterior cingulate preserved); the call stays waste. |
| A | minor | `followup_outputs`, criterion `action-cognitive-screen` | No case cognitive screen; the library would serve a normal MoCA. | FIXED: `request_moca_cognitive_screen` with a frontal profile summing to 17/30; optional criterion. |
| B | minor | `initial_tool_outputs.labs` | HIV row in "Baseline workup" with an engineering `clinical_significance` (C9). | FIXED: panel "Serology", `clinical_significance` null on every row, factual interpretation. |
| B | minor | `fallback_tool_outputs.drug_interactions`, `.ct`; `metadata.fallback_tool_kinds` | Placeholder drug check "(agent not specified on this case's pathway)"; CT fallback "without acute abnormality" against ventriculomegaly (C2, C18). | FIXED: drug-check fallback null (kind entry removed); CT fallback with enlarged ventricles (Evans about 0.35) and frontotemporal atrophy. |
| C | major | `ground_truth.assessment` | Four process musts; wrong DESH/triad prohibition; AD and "normal ageing" prohibitions irrelevant here (C11, C12). | FIXED: musts are referral with figures, copathology counselling, goals of care, continue sertraline, falls prevention (four falls); prohibitions canonical ventriculomegaly, no attribution to bvFTD alone, no withholding referral because of bvFTD. |
| C | major | `ground_truth.differential` | VCI and "bvFTD alone" high; PD, AD, atrophy moderate after the interval MRI change and a positive tap (C13). | FIXED: all low with case-data reasons; PSP entry replaces the generic PD entry. |
| A | minor | `ground_truth.action_criteria`, `avoided_actions`, `sequence_constraints`, `stop_rule` | Literature criterion; four-panel labs; label = rationale; bare citations; no advanced-imaging, neuropsychology or generic-assay avoided entries; `max_additional_actions` 0 (C1, C9, C10, C19, 3.3-3.5). | FIXED: plan 3.1 criteria with case-specific rationales and evidence; avoided entries added; plan constraint texts; stop rule MRI, baseline gait, CSF, max 1. |
| C | minor | `ground_truth.key_clinical_evidence` | Triad/DESH requirement, "sensitivity 50-80%", tier sentence (C19). | FIXED: rebuilt from F1, F2, F4, F8 with the case figures. |
| B | minor | `ground_truth.red_herrings` | Data point not the visible PMH text; interpretation cited "DESH" that the old MRI called partial. | FIXED: data point quotes the PMH; second red herring added for the frontal atrophy on the MRI (the ex-vacuo trap the case sets). |
| E | minor | `metadata.difficulty_variant_description`, `.difficulty_rationale` | "serial objective drainage assessment" (no drainage in this case); counts out of date. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The patient block keeps the bvFTD anchor and the Evans index of 0.27 at diagnosis, but no longer gives the index MRI value, the NPH referral diagnosis, TUG or MoCA. Eye movements now read as normal saccade velocity with an age-appropriate upgaze limit, and the MRI reports a normal midbrain: the PSP signs were carried over from the PSP case and would have met MDS PSP criteria the case never addresses. The work-up reads brain MRI, optional labs, baseline timed gait, optional MoCA, tap test and post-tap reassessment; literature searches are gone. MRI: Evans 0.35 (0.27 sixteen months ago), tight high-convexity sulci and enlarged Sylvian fissures with frontal sulci widened by atrophy, callosal angle 80 degrees, temporal horns enlarged, Fazekas 1, MTA 2. Tap: opening pressure 17 cmH2O, normal CSF, 38 mL removed, TUG 38 to 31 s (18%), 10-m walk 30 to 25 s, MoCA 17 to 18, behaviour unchanged. An FDG PET, if ordered, shows frontal and anterior temporal hypometabolism (waste, but consistent). Musts: shunt referral on these figures, counselling that gait and continence will benefit more than behaviour, goals-of-care discussion, continue sertraline, falls prevention. The differential is all low at assessment time (bvFTD alone, ex-vacuo atrophy, PSP, VCI, AD, secondary hydrocephalus).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation key `[Nakajima_2021]` used per plan 1.1 (CENTRAL R2).
- Post-tap criterion pattern equals the baseline criterion (plan R4).
- Library returns a negative amyloid PET and a normal DaTscan if ordered; both are consistent with this case, no action needed.

## Open questions for Andrea (judgment calls you could not settle)

None left open. Two decisions recorded: (1) the PSP elements (slow upgaze, equivocal hummingbird sign, "area ratio 0.54") were treated as template carry-over from P07 and replaced by normal findings, because kept as written they meet MDS probable PSP-RS (slow vertical saccades plus falls and pull-test instability), which would make the labelled diagnosis incomplete; (2) genetic counselling for the possibly familial FTD (father) was not made a must: it belongs to the bvFTD care, not to the decision this case scores, and the deleted literature step was its only trace.

## Verification
Adversarial verifier, 24 Oct 2026. No reviewer notes exist for NPH. Read the log, the diff against the pre-round version and every clinical field of the final case. Checked: tap figures (TUG 38/34/31 s = 11%/18%, 10-m 30/25 s = 17%, MoCA 17/18) identical across the CSF report, post-tap follow-up, criteria, musts and key evidence; MoCA subscores sum to 17 and orientation 5/6 matches "oriented to person and approximate date"; MRI markers (Evans 0.35 vs 0.27 prior, DESH, callosal angle 80, temporal horns, Fazekas 1, MTA 2) match the differential, red herrings and must; FDG PET follow-up carries `modality: FDG_PET` and stays waste; timeline (MRI 16 months ago, repeat 6 months ago, new features 8 months) coherent.
The worker's removal of the slow upgaze, the equivocal hummingbird sign and the "area ratio 0.54" was checked against the pre-round text: kept as written, slow vertical saccades plus repeated falls and a pull test "would fall if not caught" meet MDS-PSP probable PSP-RS (O2 with P1/P2), which the bvFTD-copathology case never addresses; the decision is sound and logged, and PSP now sits in the differential as low with the reason.
Found and fixed:
- `fallback_tool_outputs.echo`: no `echo_type` (PATTERNS 5). Set to "TTE".
No other defect found. Checks run after the edits: `perfect_agent.py -v` passes (every required and recommended criterion served by a case output, no fallback or library answer); `case_io.py check` clean for the case; `test_case_guards -k` passes (leak, follow-up and banned-string guards); MockServer hijack sequence (cognitive screen, then baseline gait "before tap test", MRI, CSF "large-volume lumbar puncture", post-tap reassessment, second CSF call) returns the baseline, the tap report and the post-tap follow-up in the right places; patient-block grep for Evans, callosal, DESH, NPH, hydroceph, tap, shunt, TUG, MoCA finds only hits allowed by C3/C4.

## Condition audit (NPH auditor, 24 Oct 2026)
- `action-post-tap-gait-reassessment.rationale` was the template sentence shared verbatim by P03 to P07; now case-specific (tap volume and what the reassessment separates).
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
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
