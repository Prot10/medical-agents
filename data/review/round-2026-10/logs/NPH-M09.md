# NPH-M09
Reviewer status: R1 not reviewed, R2 not reviewed (NPH has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was never annotated; no note ids exist. The July 2026 tool review (Reviewer 1, `condition_tool_guidance.yaml` key `nph`) is applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | criterion `action-1-search-medical-literature`, `stop_rule`, `followup_outputs[0]` (`request_literature_post_traumatic_nph`), `fallback_tool_outputs.literature_search` | Literature search `required` and in the stop rule; the follow-up gave unverifiable figures ("60-75% improvement", a 2017 "case series" with no source) and patient-applicable conclusions. | FIXED (C1): criterion, stop-rule id, follow-up and fallback removed. |
| D | major | `patient.history_present_illness` | "head CT ... Evans index estimated 0.34" and "referred him for inpatient NPH evaluation"; editorial closing sentence about the trajectory. | FIXED (C3): CT reported qualitatively, referral question stated; the 3-month MRI Evans 0.30 kept because it differs from the index MRI and documents change (C3 exception). |
| C | minor | HPI, neuropsychology quote | "Post-concussive syndrome" used for a severe TBI (GCS 6, DAI), where the term does not apply. | FIXED: quote and physiatrist attribution now name the diffuse axonal injury. |
| B | minor | `patient.clinical_history.past_medical_history` | "Type 2 diabetes mellitus (diet-controlled)" while on metformin 500 mg twice daily. | FIXED (C9): "Type 2 diabetes mellitus on metformin". |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 31 s, 10-m walk 24 s, MoCA 19/30, recall and trail-making results; "Frontal-subcortical pattern" interpretation. | FIXED (C4): qualitative only; numbers in the gait report and MoCA follow-up. |
| D | major | `initial_tool_outputs.mri.impression` | Impression argued the differential ("cannot be attributed to ex-vacuo effect from this finding alone"); periventricular signal labelled "transependymal CSF seepage"; no technique, temporal horns, Fazekas, MTA; DAI with no microhaemorrhages on SWI. | FIXED (C5, C7): canonical numbered impression with comparison to the prior MRI; Fazekas 1; temporal horns enlarged; incomplete DESH stated (tight convexity, no Sylvian enlargement); SWI microhaemorrhages at grey-white junctions and splenium added to match the documented DAI; technique and MTA 1. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline report carried a garbled post-tap comparison, "positive tap test" and engineering `criteria_met`. | FIXED (C6): baseline only (TUG 31 s with walker, 10-m walk 24 s/27 steps, turn 8 steps, freezing, retropulsion, falls). |
| B | minor | `initial_tool_outputs.csf` | RBC without unit; interpretation a recital ending in a verdict-like sentence. | FIXED (C5): canonical interpretation; protein 52 shown with age-adjusted reference. |
| C | minor | `initial_tool_outputs.labs` | RPR and HIV not indicated in a post-traumatic case (template carry-over); interpretation named causes ("No metabolic or infectious cause..."); "PT/INR" row. | FIXED (C9): RPR/HIV removed; `coagulation` panel; pattern-only interpretation. |
| A | major | `ground_truth.action_criteria`, `followup_outputs` | No cognitive screen or post-tap reassessment; rationales repeated labels. | FIXED: MRI, labs (optional, `{}`), baseline gait, MoCA (optional), CSF, post-tap reassessment (recommended); two authored follow-ups. |
| C | major | `ground_truth.assessment.required_recommendations` | Six musts, five of them process steps (MRI before LP, document gait, remove 30-50 mL, reassess). | FIXED (C11): referral naming the TBI antecedent; sertraline and depression; counselling on DAI deficits; falls (2 falls documented). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "DESH-like features, progressive triad, normal opening pressure and a positive tap test are all required" (wrong per F1/F4). | FIXED (C12): canonical text; static-sequelae and ex-vacuo prohibitions reworded. |
| C | major | `ground_truth.differential` | Static sequelae "high", depression "moderate", iNPH "moderate" after the positive tap. | FIXED (C13): static sequelae low, depression low, iNPH very_low; ex-vacuo atrophy after DAI added (low, plan open question 6); VCI low; focal encephalomalacia very_low. Static-sequelae ICD F07.2 (postconcussional syndrome) replaced by S06.2X9S. |
| C | minor | `ground_truth.avoided_actions` | No CT waste entry although MRI is available and a CT was done 2 weeks ago; advanced imaging, neuropsych battery and generic CSF assays not marked. | FIXED (3.3). |
| B | minor | `fallback_tool_outputs.ct`, `.echo` | CT fallback carried a teaching sentence and a recommendation; echo said "incidental to the current neurological evaluation" and lacked `echo_type`. | FIXED (C18). |
| B | minor | `sequence_constraints`, `stop_rule`, `key_clinical_evidence`, `red_herrings`, `metadata` | Non-canonical reasons; allowance 0; tier sentence; "positive response (>10-15% TUG, or MoCA improvement)"; red herring cited a deleted impression sentence and a moved index. | FIXED: canonical; red herring 2 points to `mri.findings[6]`. |

## Changes, in one paragraph a physician can read before re-reviewing
The HPI keeps the injury, the 3-month MRI (Evans 0.30) and the deteriorating trajectory but no longer gives the recent CT measurement, the referral diagnosis or the timed and MoCA results; post-concussive wording is replaced by diffuse axonal injury. The MRI reads communicating ventriculomegaly with Evans 0.35 (up from 0.30), callosal angle 82 degrees, enlarged temporal horns, incomplete DESH, Fazekas 1, a patent aqueduct, a 1.2 cm right frontal contusion, DAI microhaemorrhages and superficial siderosis, without arguing the differential. The baseline gait report (TUG 31 s, 10-m walk 24 s) no longer holds the tap result; the CSF report and a separate reassessment give TUG 24 s at 2 hours and 21 s at 24 hours (32%) and MoCA 19 to 22. The literature step is removed. Musts: shunt referral for post-traumatic hydrocephalus, continuing sertraline, counselling that DAI deficits will remain, and falls prevention. The differential is set after the tap: static sequelae, ex-vacuo atrophy and depression low, iNPH very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- R1: add G91.3 (post-traumatic hydrocephalus, unspecified) to the accepted ICD codes of this case through `diagnosis_synonyms.yaml` and `apply_diagnosis_synonyms.py`.
- R2: `[Nakajima_2021]` is not yet in the NPH criteria pack.
- R4: post-tap reassessment criterion shares the baseline pattern.

## Open questions for Andrea (judgment calls you could not settle)
None. Plan open question 6 resolved here: the iNPH entry stays at very_low and an explicit "post-traumatic ventriculomegaly ex vacuo" entry is added at low, because it is the realistic alternative after diffuse axonal injury and the serial MRI and tap response are what refute it.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the pre-round MRI, HPI, differential and red herrings, and the final case. Checked: superficial siderosis was in the original report (tSAH sequela) and is kept; the added SWI microhaemorrhages fit the documented diffuse axonal injury; the HPI keeps only the older MRI's Evans 0.30 (allowed by C3, it documents change); tap figures agree across CSF report, reassessment, criteria, key evidence and must (TUG 31 to 24 to 21 s, 23% and 32%; 10-m walk 24 to 17 s, 29%; MoCA 19 to 22); MoCA subscores sum to 19 and orientation 5/6 matches "disoriented to date" in the exam; red herring 2 points at `mri.findings[6]`, which is the encephalomalacia; differential per C13 and plan open question 6 (ex-vacuo entry added at low). Found and fixed: (1) `initial_tool_outputs.mri.findings[4]` described Fazekas 1 as a "smooth periventricular hyperintensity", which is the halo of grade 2; now "Thin periventricular caps and a pencil-thin periventricular lining of T2/FLAIR hyperintensity, Fazekas grade 1; no deep white matter lesions"; (2) the ECG and echo `avoided_actions` rationales were still the generic template text although the log reports 3.3 as fixed; both are now case-specific (falls with the gait decline without syncope; no syncope, murmur or embolic event). `perfect_agent.py -v`, `case_io.py check` and `test_case_guards` clean after the changes. CENTRAL R1 (G91.3) still pending.

## Condition audit (NPH auditor, 24 Oct 2026)
- MoCA attention finding "Markedly slowed responses; serial subtraction with two errors; digit span backward 2." -> "Markedly slowed responses; two errors on letter tapping; serial subtraction with two errors; digit span backward 2." so the finding scores to the stored Attention subscore (3/6); totals unchanged.
- `[Tisell_2011]` removed from `action-4-analyze-csf.citations`: the pack entry is Tisell 2011, shunt surgery in hydrocephalus with white matter changes, and this rationale is about the tap response only; `[Marmarou_2005]` (tap test) stays.
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.2 and the bare labels "normal pressure hydrocephalus" and "NPH" removed, because with token matching they credited "idiopathic NPH", the wrong answer for a case with an antecedent; now credits "secondary NPH" / "secondary normal pressure hydrocephalus", "communicating hydrocephalus", G91.0, G91.9 and labels naming the traumatic antecedent (`traumatic NPH`, `TBI NPH` and long forms) and code G91.3 (plan R1).
- `key_clinical_evidence`: "(Marmarou 2005)" written as the key `[Marmarou_2005]`.
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
