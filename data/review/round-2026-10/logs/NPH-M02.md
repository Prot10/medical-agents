# NPH-M02
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `nph`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for NPH. The case was corrected against plan NPH (classes C1 to C20) and the July 2026 tool review (MRI and tap test required, gait before and after the tap, labs optional, no advanced imaging or neuropsychology). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, criterion `action-1-search-medical-literature` | Recommended literature criterion; stored output repeated its expected_evidence (leak-test failure, C1). | FIXED: criterion deleted; initial and fallback literature outputs null. |
| C | major | `followup_outputs[0]` (check_drug_interactions `request_drug_interactions_preop`) | Perioperative shunt management (cefazolin, sertraline continuation) served as a tool result (C2). | FIXED: follow-up deleted; drug-interaction initial and fallback null. Sertraline needs no change for the tap; no must added (plan). |
| D | major | `patient.history_present_illness` | "Inpatient tap trial evaluation", "progressive triad symptoms", outside report "communicating hydrocephalus", Evans index 0.32, callosal angle 96 degrees with the NPH threshold, outpatient MoCA 21/30 identical to the baseline (C3, C4). | FIXED: admission for evaluation of the three symptoms; outside MRI "reported as showing enlarged ventricles and white matter disease; the images are not available"; the outpatient MoCA sentence removed because it equals the baseline score. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 28 s, 10-metre walk 22 s and the MoCA item profile in the exam (C4). | FIXED: qualitative gait and "formal cognitive screening reported separately"; numbers moved to the baseline gait report and the cognitive-screen follow-up. |
| B | minor | `patient.neurological_exam.mental_status` (old) | Exam MoCA breakdown (4 attention, 3 recall, 1 visuospatial) sums to 22, not 21. | FIXED: the new cognitive screen itemises 21/30 consistently (visuospatial/executive 4/5, attention 2/6, language 2/3 with phonemic fluency 7 words, which the exam's word-finding difficulty supports, recall 2/5 free and 4/5 cued). |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Pre-tap gait call returned the post-tap result, "positive tap test", engineering `criteria_met` keys and the "case's own tap-trial report" sentence (C5, C6). | FIXED: baseline only (TUG 28 s with walker, 10-metre walk 22 s in 30 steps, turn 6 steps, MoCA 21/30), qualitative findings including that the knee replacement does not explain the gait (plan M02), `criteria_met` and `pre_post_comparison` null. |
| A | major | `followup_outputs` | No post-tap reassessment and no case cognitive screen (C6). | FIXED: `followup_outputs[0]` cognitive screen (`request_moca_cognitive_screen`); `followup_outputs[1]` post-tap reassessment (`request_post_reassessment`; TUG 24 s at 2 h, 21.5 s at 24 h, 10-metre walk 17 s, MoCA 22/30, identical to the CSF report). |
| C | major | `initial_tool_outputs.mri` | No technique, temporal horns, hippocampal score, aqueduct or fourth ventricle; with a non-acute callosal angle and no DESH the report had no supportive feature at all (C7, F2). | FIXED: technique line; Evans 0.32; callosal angle 96 degrees kept (the case's equivocal design); temporal horns enlarged out of proportion to the hippocampi (MTA 1, the supportive feature, plan M02); mild convexity tightening with Sylvian fissures not enlarged, DESH absent; Fazekas 2; patent aqueduct with flow void, normal fourth ventricle; no obstruction; descriptive impression. |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | Interpretation in prose with "improved"; "marginal" verdict in special_tests (C5). | FIXED: canonical interpretation (40 mL; TUG 28 to 24 s at 2 h and 21.5 s at 24 h, 23%; 10-metre walk 22 to 17 s; MoCA 21 to 22); special_tests with the same figures and percentages. |
| C | minor | `initial_tool_outputs.labs` | HIV in a "Baseline workup" panel with templated clinical_significance (C9). | FIXED: RPR and HIV in a `Serology` panel; all `clinical_significance` null; "Vitamin B12"; interpretation states the pattern. |
| C | major | `ground_truth.action_criteria` | Labs required four named panels; rationales repeated labels; generic evidence; no post-tap or cognitive criterion. | FIXED: MRI (required), labs `{}` (optional), baseline gait (required), cognitive screen (optional, `action-cognitive-screen`), CSF (required), post-tap reassessment (recommended, `action-post-tap-gait-reassessment`), each with case-specific rationale and evidence matching its report. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | As in M01. | FIXED: hard MRI before CSF [Relkin_2005]; soft baseline gait before CSF [Nakajima_2021]; stop rule three required ids, `max_additional_actions` 1. |
| B | minor | `ground_truth.avoided_actions` | No guard against advanced imaging, neuropsych battery, generic CSF assays (C10, 3.3). | FIXED: three entries added; the five existing rationales rewritten for this patient. |
| C | major | `ground_truth.assessment.required_recommendations` | Four process musts (C11). | FIXED: referral for a programmable-valve shunt citing the 23% TUG response, Evans 0.32 with temporal horn enlargement and normal-pressure CSF; falls prevention (two near-falls, walker). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong DESH/callosal/triad prohibition; AD prohibition copied (C12). | FIXED: canonical ventriculomegaly-alone prohibition; AD prohibition removed (AD low, MTA 1); LP-before-MRI and normal-ageing kept; new prohibition against attributing the gait to the knees. |
| C | major | `ground_truth.differential` | VCI `high`; PD, AD, atrophy `moderate`; PD and atrophy argued from DESH (C13). | FIXED: VCI `moderate` (Fazekas 2); PD, AD (MTA 1, plan rule), atrophy ex vacuo (acknowledging the 96-degree angle) and secondary hydrocephalus `low`, one case-specific sentence each. |
| C | major | `ground_truth.key_clinical_evidence` | DESH stated as required, sensitivity 50-80%, tier sentence (C19, F4). | FIXED: seven case items, including the depression-in-remission sentence the plan asks for and the knee confounder. |
| B | minor | `ground_truth.red_herrings` | None, although the history raises knee osteoarthritis and arthroplasty as the obvious gait confounder. | FIXED: one red herring on `patient.clinical_history.past_medical_history` (knee OA and left TKR), interpretation consistent with the gait report. |
| B | minor | `fallback_tool_outputs.ct` | "No acute intracranial abnormality" against ventriculomegaly (C18). | FIXED: Evans about 0.32, periventricular hypodensity, no mass, haemorrhage or shift. |
| B | minor | `fallback_tool_outputs.echo` | "Benign incidental finding" phrasing; no `echo_type` (C18, PATTERNS 5). | FIXED: findings and impression state grade I diastolic dysfunction with normal function; `echo_type` "TTE". |
| E | minor | `metadata.vocab_gap`, `.fallback_tool_kinds`, `.difficulty_rationale`, `.difficulty_variant_description` | Stale phase-contrast gap; counts of removed tools; variant said an "extended drainage trial strengthens diagnosis" although the case has none (C19). | FIXED: gap and literature kind removed; counts and variant description rewritten; revision fields updated. |
| - | check | plan 3.6 | perfect_agent ok; test_case_guards pass; hijack probe: cognitive screen then "baseline before tap test" returns the baseline; after CSF, "post-tap reassessment at 24 hours" and "post-LP reassessment of gait" return the follow-up; CT and echo fallbacks consistent. Patient-block grep clean. Pre-existing em dashes in unedited HPI and motor sentences left. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The patient block no longer gives the outside Evans index, callosal angle, "communicating hydrocephalus" report, the tap-trial purpose or the bedside scores. The MRI now has a technique line and all iNPH markers: Evans 0.32, callosal angle 96 degrees (not acute), temporal horns enlarged out of proportion to the hippocampi (MTA 1), no DESH, Fazekas 2 white matter change, patent aqueduct, no obstruction. The baseline gait report gives TUG 28 s with the walker, 10-metre walk 22 s, turn in 6 steps and notes that the knee replacement does not explain the gait; a separate post-tap reassessment and the CSF report both give TUG 24 s at 2 hours and 21.5 s at 24 hours (23%), 10-metre walk 17 s, MoCA 22. A cognitive screen itemises the MoCA of 21/30 (the old exam breakdown summed to 22). Literature and drug-check steps are gone. Policy: MRI, baseline gait and tap required, post-tap reassessment recommended, labs and cognitive screen optional; advanced imaging, neuropsychology and generic CSF assays are waste. Musts: programmable-valve shunt referral on the 23% response with the temporal horn finding, and falls prevention. VCI is moderate (Fazekas 2); parkinsonism, AD and atrophy low. A knee red herring was added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[Nakajima_2021]` used per the plan's canonical texts, not yet in the NPH criteria pack.
- Plan R4: post-tap criterion has the baseline pattern; credited from the baseline call until a timing discriminator exists.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 and Q2 apply).

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the whole final case and its diff against fa1d22e6.
- Checked: all own-finding rows against the file; patient-block grep clean; figures identical across baseline report, post-tap follow-up, CSF report and criteria (TUG 28 to 24 s = 14%, to 21.5 s = 23%; 10-metre walk 22 to 17 s = 23%); MoCA items sum to 21 and the attention item (digits forward 1, backward 0, two tapping errors 0, serial sevens 1) scores 2/6 by MoCA rules; CSF glucose 64 with ratio 0.68 matches serum 94; MRI has a supportive feature (temporal horns) without DESH, consistent with the differential, key evidence and musts; AD low with MTA 1 (plan M02); new knee red herring visible in the PMH. MockServer probe as M01: no leak.
- Found and fixed (B, minor): `patient.neurological_exam.mental_status` said "Alert, attentive" while the cognitive screen reports "marked attention and working-memory deficits" (attention 2/6). Now "Alert and fully oriented, with slowed responses."
- Not changed: pre-existing em dashes in unedited HPI and motor sentences; `difficulty: straightforward` against a "Moderate iNPH" variant description is pre-existing and outside this round's edits.
- perfect_agent -v ok, case_io check clean for the case, test_case_guards pass.

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
