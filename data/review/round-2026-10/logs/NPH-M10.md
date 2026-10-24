# NPH-M10
Reviewer status: R1 not reviewed, R2 not reviewed (NPH has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was never annotated; no note ids exist. The July 2026 tool review (Reviewer 1, `condition_tool_guidance.yaml` key `nph`) is applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | criterion `action-1-search-medical-literature`, `stop_rule`, `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search` | Literature search `required` and in the stop rule; the stored output carried uncited papers and a patient-level conclusion ("warrants tap-test evaluation regardless of lumbar spine findings"). | FIXED (C1): criterion, stop-rule id and both outputs removed. |
| D | minor | `patient.history_present_illness`, `.chief_complaint` | "admitted for brain MRI and tap-trial evaluation"; numbered list and em dashes. | FIXED (C3): removed; prose kept otherwise. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 28 s, 10-m walk 22 s, MoCA 21/30 with point losses and MMSE 25/30 in the exam. | FIXED (C4): qualitative only; numbers moved to the gait report and the MoCA follow-up. |
| B | minor | `patient.neurological_exam.motor` | "Normal bulk and tone" and "mild bilateral lower extremity tone increase" in the same field. | FIXED: "Mild paratonia in the lower limbs". |
| C | major | `initial_tool_outputs.mri` | Lumbar MRI comparison and lumbar findings inside a brain MRI report; teaching parenthetical "(reference: <90 degrees supports NPH pattern)"; "transependymal CSF signal" and "hyperdynamic CSF pulsatility" interpretations; impression "consistent with communicating hydrocephalus in an appropriate clinical context"; no technique or MTA. | FIXED (C5, C7): lumbar content removed (moved to the optional spine MRI); canonical impression; temporal horns, Fazekas 2, MTA 1 and technique stated. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline report carried the post-tap result, "positive tap test" and engineering `criteria_met`. | FIXED (C6): baseline only (TUG 28 s, 10-m walk 22 s/26 steps, turn 7 steps, start hesitation, no positional pattern). |
| B | minor | `initial_tool_outputs.csf.interpretation` | "No organisms on Gram stain" for a study nobody ordered; recital. | FIXED (C5): canonical interpretation with the case's 1-hour and 24-hour figures. |
| C | minor | `initial_tool_outputs.labs` | RPR and HIV rows (template); interpretation names the screen. | FIXED (C9): removed; pattern-only interpretation. |
| A | major | `ground_truth.action_criteria`, `followup_outputs` | No cognitive screen, spine MRI or post-tap reassessment; rationales repeated labels; empty follow-ups. | FIXED: MRI, labs (optional, `{}`), baseline gait, MoCA (optional), lumbar spine MRI (optional, C14), CSF, post-tap reassessment (recommended); three authored follow-ups. |
| C | major | `ground_truth.assessment.required_recommendations` | Six musts, five process steps, including "Obtain reversible-cause labs (TSH, B12, RPR, HIV)" against the optional-labs ruling. | FIXED (C9, C11): referral with the spine decision revisited after the shunt response; canonical aspirin must; falls prevention (gait instability, retropulsion, stopped driving). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong DESH/triad criterion; AD prohibition though AD is low. | FIXED (C12): canonical text; aspirin prohibition added; AD prohibition removed; decompression and stenosis-attribution prohibitions reworded. |
| C | major | `ground_truth.differential` | Lumbar stenosis "high" and PD "moderate" after a 32% tap response; PD argued from DESH. | FIXED (C13): stenosis low, PD low, AD low, CSM low; VCI moderate (Fazekas 2). |
| B | major | `ground_truth.red_herrings[1]` | Data point "gait initially described to the spine team as worsening with prolonged ambulation" is not in the patient block (the HPI says the opposite). | FIXED (C20): replaced by the visible deferred-laminectomy recommendation, with a correct interpretation. |
| C | minor | `ground_truth.avoided_actions` | Advanced imaging, neuropsych battery, generic CSF assays not marked; generic rationales. | FIXED (3.3). |
| B | minor | `fallback_tool_outputs.ct`, `.cardiac_monitoring`, `.echo` | CT fallback normal with a modality recommendation; Holter "benign incidental"; echo "no cardioembolic source" phrasing and no `echo_type`. | FIXED (C18). |
| B | minor | `sequence_constraints`, `stop_rule`, `key_clinical_evidence`, `metadata` | Non-canonical reasons; allowance 0; tier sentence; "satisfies Relkin criteria ... predicts shunt responsiveness"; "first spine-misattribution case" note. | FIXED (C19). |

## Changes, in one paragraph a physician can read before re-reviewing
The patient block keeps the 20-month spine-anchored history and the wife's observations but no longer gives the timed gait or MoCA values or the "tap-trial" admission reason; a contradictory tone statement is resolved as paratonia. The brain MRI no longer contains the lumbar study and reads Evans 0.35 with DESH, callosal angle 72 degrees, enlarged temporal horns, Fazekas 2, aqueductal flow void and MTA 1. The lumbar findings come back only if an optional lumbar MRI is ordered (moderate L4-L5 stenosis, unchanged, no cauda equina compression). The gait report is the baseline (TUG 28 s); the CSF report and a separate reassessment give TUG 22 s at 1 hour and 19 s at 24 hours (32%), 10-m walk 22 to 15 s, MoCA 21 to 23. The literature step and the mandatory reversible-cause labs are gone. Musts: shunt referral with the decompression decision revisited afterwards, continue aspirin through the tap, falls prevention. Prohibitions: no decompression for this gait, no attribution to stenosis, MRI before LP, the corrected iNPH criterion, do not stop aspirin.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- R2: `[Nakajima_2021]` and `[ASRA_2018]` (referral and aspirin musts, per the plan's canonical texts) are not yet in the NPH criteria pack.
- R4: post-tap reassessment criterion shares the baseline pattern.

## Open questions for Andrea (judgment calls you could not settle)
None. The case's early post-tap value is at 1 hour (the plan's protocol says 2 to 4 hours); I kept the stored 1-hour figure rather than relabel the data.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the patient block, every stored output and the ground truth. Checked: patient block free of imaging measurements and timed or MoCA values; brain MRI has no lumbar content and meets F2 with DESH (both components), callosal angle 72, temporal horns, Fazekas 2 wording matching the grade; the optional lumbar MRI agrees with the PMH (moderate L4-L5 central stenosis, compared with the lumbar MRI of 14 months ago); tap figures agree across CSF report, reassessment, criteria and must (TUG 28 to 22 s at 1 hour, 21%, to 19 s at 24 hours, 32%; 10-m walk 22 to 15 s, 32%; MoCA 21 to 23); MoCA subscores sum to 21; aspirin must and prohibition are the canonical texts; the decompression prohibition and the "revisit after the shunt response" clause of the referral must do not contradict each other; red herrings are visible in the PMH and HPI; differential per plan (stenosis low, VCI moderate). Keeping the stored 1-hour value rather than relabelling it as 2 hours is correct. `perfect_agent.py -v`, `case_io.py check`, `test_case_guards` and the MockServer probe clean. No error found; no change made.

## Condition audit (NPH auditor, 24 Oct 2026)
- `[Tisell_2011]` removed from `action-4-analyze-csf.citations`: the pack entry is Tisell 2011, shunt surgery in hydrocephalus with white matter changes, and this rationale is about the tap response only; `[Marmarou_2005]` (tap test) stays.
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
- Aspirin must (and key evidence): `[ASRA_2018]` -> `[ASRA_2025]` (statement unchanged: aspirin and NSAIDs need no interruption).
- `key_clinical_evidence`: "(Marmarou 2005)" written as the key `[Marmarou_2005]`.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` clean, `test_case_guards -k NPH-` pass. Not yet in `DISCRIMINATOR_CONDITIONS`: the post-tap follow-up's prose `assessment_type` is deliberate until the timing discriminator lands (CENTRAL C2 in the decisions file).

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (timing discriminator, NPH R4; decisions Q2 and CENTRAL C2). No clinical text changed.

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment.timing` | added `baseline` |
| `followup_outputs[2]` (`request_post_reassessment`) | `assessment_type` "gait_and_balance_timed (post-tap reassessment)" -> `gait_and_balance_timed`; `timing: post_intervention` added |
| `ground_truth.action_criteria[action-6-perform-clinical-assessment]` | `required_arguments.timing: baseline` (the schema default, so a call that omits it still matches; a post-tap call no longer does) |
| `ground_truth.action_criteria[action-post-tap-gait-reassessment]` | `required_arguments.timing: post_intervention`; importance recommended -> required (Reviewer 1: gait before and after the tap) |
| `ground_truth.sequence_constraints` | soft: `action-4-analyze-csf` before `action-post-tap-gait-reassessment` [Nakajima_2021] |
| `ground_truth.stop_rule.required_before_assessment` | `action-post-tap-gait-reassessment` added |

Scoring change for re-review: the post-tap reassessment is now required and is credited only by a call with `timing: post_intervention`; the baseline order is answered by the baseline report and the reassessment order by the post-tap report (MockServer secondary discriminator).
