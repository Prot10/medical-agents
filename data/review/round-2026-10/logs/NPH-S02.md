# NPH-S02
Reviewer status: R1 not reviewed, R2 not reviewed (NPH has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was never annotated; the only physician input is the July 2026 tool review (`condition_tool_guidance.yaml` key `nph`), applied through plan NPH sections 2 to 4. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs[request_neurosurgery_consultation]` | A neurosurgery consult faked as a drug check, with shunt perioperative advice ("hold tamsulosin perioperatively") (C2, ruling 4). | FIXED: deleted; drug-interaction fallback null. |
| C | major | `followup_outputs[request_literature_nph_shunt]`, `action_criteria[action-1-search-medical-literature]` | Literature as a clinical step, with unsourced PPV figures (C1, ruling 5). | FIXED: criterion and follow-up deleted. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline report held the post-tap result, the engineering sentence and `criteria_met` keys (C6). | FIXED: baseline only (TUG 28 s, 10-m walk 22 s in 32 steps, turn 7 steps, MoCA 21/30); post-tap values in follow-up `request_post_reassessment`. |
| D | major | `patient.history_present_illness` | "He was admitted for MRI, lumbar puncture, and tap trial assessment" names the work-up and the diagnosis (C3). | FIXED: canonical outside-CT and referral sentences; em dash removed. |
| B | minor | `patient.clinical_history.medications[Tamsulosin].dose` | HPI says the tamsulosin dose was increased without benefit, but the list gave 0.4 mg, the starting dose. | FIXED: 0.8 mg. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG, 10-m walk and MoCA 21/30 with subscores in the exam (C4). | FIXED: qualitative; numbers moved to the gait report and the cognitive-screen follow-up. |
| D | major | `initial_tool_outputs.csf.interpretation` | "Positive tap trial" (C5). | FIXED: C5 canonical form (40 mL; TUG 28 to 21 s at 2 h, 19 s at 24 h, 32%; 10-m 22 to 15.5 s; MoCA 21 to 24). |
| D | major | `initial_tool_outputs.mri` | "transependymal signal" interpretation, two overlapping white-matter findings without a grade, no technique, temporal horns, hippocampi or fourth ventricle (C7). | FIXED: rebuilt with the C7 elements (Evans 0.38, DESH, callosal angle 74, temporal horns with MTA 1, Fazekas 1, aqueduct flow void, normal fourth ventricle, no obstruction); canonical impression. |
| C | minor | `initial_tool_outputs.labs` | HIV "Baseline workup" row with engineering text (C9); criterion with a fixed panel. | FIXED: Serology panel, `clinical_significance` null, pattern interpretation; criterion `interpret_labs {}` optional. |
| C | major | `ground_truth.assessment` | Process musts; wrong DESH-plus-triad prohibition; AD prohibition where AD is not in question; no handling of the BPH confounder the plan asks for (C11, C12). | FIXED: musts are referral (32%), counselling that the urge incontinence may be mixed with BPH, falls prevention (two falls); prohibitions MRI-first, canonical, BPH-alone attribution, ageing/deconditioning. |
| C | minor | `ground_truth.red_herrings` | `difficulty_variant_description` names BPH as the urinary red herring but `red_herrings` was empty. | FIXED: BPH red herring added (data in the HPI), interpretation per F1 (urinary symptoms probably mixed). |
| C | major | `ground_truth.differential` | VCI "high", PD, AD and ex vacuo "moderate" after DESH and a 32% tap response (C13). | FIXED: all low with case data (Fazekas 1; MTA 1 and cue-responsive recall for AD). |
| C | minor | `ground_truth.key_clinical_evidence` | Tier sentence; "sensitivity only 50-80%" (F4). | FIXED: four pearls with F1, F2, F4 and the BPH point. |
| C | minor | `ground_truth.action_criteria`, `avoided_actions`, `sequence_constraints`, `stop_rule` | Label equals rationale, "NPH_pack"; no post-tap or cognitive criteria; waste entries missing; allowance 0. | FIXED: plan 3.1 order and tiers; advanced imaging, battery and generic CSF assays as waste; canonical constraints; allowance 1. |
| B | minor | `fallback_tool_outputs.ct`, `.echo` | CT fallback "without acute abnormality" against ventriculomegaly; echo without `echo_type` (C18). | FIXED: CT shows enlarged ventricles (Evans about 0.37); `echo_type: TTE`. |
| E | minor | `metadata.vocab_gap`, `.difficulty_rationale`, `.difficulty_variant_description` | Stale phase-contrast note; removed-tool counts; em dash. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The HPI no longer announces the admission for "MRI, lumbar puncture and tap trial"; it reports an outside CT read as enlarged ventricles and a referral for gait, memory and urinary symptoms, and the tamsulosin dose now matches the stated increase (0.8 mg). The exam is qualitative. The fake neurosurgery consult and the literature step are gone. The pathway is MRI, optional labs, baseline timed gait (TUG 28 s, 10-m walk 22 s, turn 7 steps), optional MoCA (21/30, dysexecutive with cue-responsive recall), the tap test (opening pressure 11 cmH2O, normal CSF, 40 mL; TUG 21 s at 2 h, 19 s at 24 h, 32%; 10-m 15.5 s; MoCA 24) and a recommended post-tap reassessment. The MRI reports Evans 0.38, DESH, callosal angle 74 degrees, temporal horns out of proportion to MTA 1 hippocampi, Fazekas 1 and a patent aqueduct. Musts are shunt referral, counselling that the urinary response is less predictable because BPH may contribute, and falls prevention; BPH is now an explicit red herring and a prohibition guards against attributing the incontinence to it alone. All differential alternatives are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation key `[Nakajima_2021]` used per plan 1.1 (plan CENTRAL R2).
- Post-tap criterion shares the baseline pattern (plan CENTRAL R4); hijack check as in S01 (post-tap phrasing served, "repeat gait after lumbar puncture" a miss without leak).

## Open questions for Andrea (judgment calls you could not settle)

- None.
