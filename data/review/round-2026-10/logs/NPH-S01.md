# NPH-S01
Reviewer status: R1 not reviewed, R2 not reviewed (NPH has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was never annotated; the only physician input is the July 2026 tool review (`condition_tool_guidance.yaml` key `nph`), applied through plan NPH sections 2 to 4. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search["general"]`, `action_criteria[action-1-search-medical-literature]` | Literature output repeated the criterion's expected evidence (leak-test failure); literature used as a clinical step (C1). | FIXED: criterion deleted; initial and fallback literature null. Leak guard now passes. |
| C | major | `followup_outputs[request_drug_interactions_shunt]` | Drug check wrote shunt perioperative management (cefazolin, vasopressors for amlodipine) (C2). | FIXED: deleted; drug-interaction fallback null. |
| D | major | `initial_tool_outputs.clinical_assessment` | The exemplar of C6: baseline report held the post-tap result, the engineering sentence "this is what the case's own tap-trial report states", `criteria_met` keys and a shunt-responsiveness impression. | FIXED: baseline only (TUG 28 s and 10-m walk 22 s in 34 steps with cane, turn 9 steps, MoCA 22/30), qualitative findings, descriptive impression; post-tap values moved to follow-up `request_post_reassessment`. |
| D | major | `patient.chief_complaint`, `patient.history_present_illness` | "classic triad", outside "Evans index 0.38", "referred ... for tap trial" (C3); numbered list with em dashes; reasoning sentences ("in a compatible timeframe"). | FIXED: chief complaint as symptoms; HPI rewritten in prose with the canonical outside-imaging and referral sentences; prior MMSE 24/30 kept (a different instrument from the baseline MoCA); antecedent events explicitly denied (supports the secondary-NPH entry). |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG, 10-m walk, MoCA 22/30 and "frontal-subcortical pattern" in the exam (C4). | FIXED: qualitative gait and mental status; numbers in the assessment reports. |
| D | major | `initial_tool_outputs.csf.interpretation` | "Positive tap trial" (C5). | FIXED: C5 canonical form with 45 mL, TUG 28 to 22 s (2 h) and 18 s (24 h, 36%), 10-m 22 to 15 s, MoCA 22 to 25; special_tests factual; turn steps made consistent with the baseline (9). |
| D | major | `initial_tool_outputs.mri` | "transependymal CSF seepage" interpretation; no Fazekas grade, temporal horns, hippocampi, fourth ventricle or technique; flow void placed on T1 (it is a T2 sign) (C7). | FIXED: rebuilt with the C7 elements (Evans 0.38, DESH both components, callosal angle 72, temporal horns with MTA 1, Fazekas 1 halo, aqueduct flow void on T2, normal fourth ventricle, no obstruction) and canonical impression. |
| C | minor | `initial_tool_outputs.labs` | HIV row in a "Baseline workup" panel with an engineering `clinical_significance` (C9); criterion asked for a fixed four-test panel. | FIXED: HIV Ag/Ab moved to a Serology panel, all `clinical_significance` null, pattern interpretation; criterion `interpret_labs {}` optional. |
| C | major | `ground_truth.assessment` | Four process musts; prohibition "DESH, callosal angle <90 and a triad are required" contradicts F1/F2; AD prohibition where AD is not in question (C11, C12). | FIXED: musts are referral (36% TUG, DESH MRI, normal-pressure CSF) and falls prevention (four falls); prohibitions MRI-first, canonical ventriculomegaly text, ageing/deconditioning; AD prohibition deleted. |
| C | major | `ground_truth.differential` | VCI "high" with no Fazekas grade; PD, AD and ex vacuo "moderate" after DESH and a 36% tap response (C13). | FIXED: all low, with case-data reasoning; VCI low because the MRI shows Fazekas 1. |
| C | minor | `ground_truth.key_clinical_evidence` | Tier sentence; "sensitivity only 50-80%"; Relkin restated with an "opening pressure <25" rule and a required triad (F1, F4). | FIXED: four pearls using F1, F2, F4 figures. |
| C | minor | `ground_truth.action_criteria`, `avoided_actions`, `sequence_constraints`, `stop_rule` | Label equals rationale, "NPH_pack" and unbracketed citations; no post-tap or cognitive-screen criteria; advanced imaging, battery and generic CSF assays not marked waste; stop-rule allowance 0. | FIXED: plan 3.1 order (MRI, labs opt, baseline gait, MoCA opt, CSF, post-tap rec); waste entries added; canonical constraints; allowance 1. |
| B | minor | `fallback_tool_outputs.ct`, `.echo` | CT fallback "without acute abnormality" against ventriculomegaly; echo "benign incidental finding", no `echo_type` (C18). | FIXED: CT shows enlarged ventricles (Evans about 0.37); echo states the aortic sclerosis, `echo_type: TTE`. |
| E | minor | `metadata.vocab_gap`, `.difficulty_rationale`, `.fallback_tool_kinds` | Stale phase-contrast vocab note; counts of removed tools; literature fallback kind. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The patient block now gives two years of progressive magnetic gait with falls, urinary incontinence and forgetfulness, an outside MRI reported only as enlarged ventricles, and a qualitative exam; no Evans index, "triad", "tap trial" or bedside scores. Literature and drug checks are gone. The pathway is MRI, optional labs, baseline timed gait (TUG 28 s, 10-m walk 22 s, turn 9 steps, with cane), optional MoCA (22/30, dysexecutive with cue-responsive recall), the tap test (opening pressure 12 cmH2O, normal CSF, 45 mL; TUG 22 s at 2 h and 18 s at 24 h, 36%; 10-m walk 15 s; MoCA 25) and a recommended post-tap reassessment with the same figures. The MRI reports Evans 0.38, DESH, callosal angle 72 degrees, temporal horns out of proportion to MTA 1 hippocampi, Fazekas 1, a patent aqueduct with flow void and no obstruction, with a descriptive impression. Musts are shunt referral and falls prevention; the old DESH-plus-triad prohibition was replaced by the canonical one. All differential alternatives are low after the work-up.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation key `[Nakajima_2021]` used per plan 1.1 (plan CENTRAL R2).
- Post-tap criterion shares the baseline pattern (plan CENTRAL R4). Hijack check: post-tap phrasing after the tap returns the follow-up; "repeat gait after lumbar puncture" returns the baseline (miss, no leak).
- Condition lead: baseline TUG 28 s and 10-m walk 22 s with a 2-hour TUG of 22 s recur in M02, M10, P05, P09, S01 and S02 (template numbers). Not changed here because the plan's per-case figures use them; flagged for a condition-level decision.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

What I checked: Read the log and the whole final case; diffed it against the S02 to S05 outputs as a template check. MoCA subscores sum to 22. TUG, 10-m walk and MoCA figures agree across the baseline report, the tap report, the post-tap follow-up, the criteria and the referral must. Evans index, callosal angle and opening pressure agree across the MRI, the CT fallback (±0.01), the criteria, the must and the key evidence. Every log row was checked against the file and is accurate. No banned strings, dashes or engineering text. The patient block has only the prior MMSE 24/30, a different instrument, which C3/C4 allow. Checks run after the edits: `perfect_agent.py -v` ok (MRI and baseline gait show `<- ?` only because of null fields; a MockServer run confirmed both come from the case's own initial outputs, not the library), `case_io.py check` clean for the case, `test_case_guards -k` passes. Hijack check (cognitive screen, baseline gait "before tap test", MRI, tap, post-tap reassessment): every call served by the case's own output in the right order, no post-tap leak to the baseline. Discriminator note for the close-out: the post-tap follow-up's `assessment_type` "gait_and_balance_timed (post-tap reassessment)" is the plan's deliberate prose value (C6). It will fail `test_routed_outputs_name_their_study` once NPH joins `DISCRIMINATOR_CONDITIONS`. Renaming it to the bare term would let the discriminator serve it at the baseline call, so this needs plan CENTRAL R4, not a rename.

Found and fixed:
1. (C, minor) `ground_truth.key_clinical_evidence[0]` stated what probable iNPH "needs" [Relkin_2005] but left out the physiological criterion. Added "a CSF opening pressure of 5 to 18 mmHg (7 to 24.5 cmH2O)" (F3). In `[2]`, the 10% TUG criterion is cited to [Nakajima_2021] (F4); before, only [Marmarou_2005] was cited.

Changed: Edited `key_clinical_evidence[0]` and `[2]` only. Nothing else changed: no labels, tiers, criteria, sequence or stop rule. Template numbers (baseline TUG 28 s, 10-m 22 s, also in S02 and P09) were flagged to the lead by the worker. They are plausible and were not changed here.

## Condition audit (NPH auditor, 24 Oct 2026)
- Lab rows RPR moved from the `Metabolic` panel to `Serology`; values unchanged.
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
- `key_clinical_evidence`: the 10% TUG threshold is no longer attributed to `[Nakajima_2021]`, which sets no numeric tap-test cut-off; it is stated as a commonly used threshold that no guideline fixes (the tap protocol keeps its Nakajima citation where the sentence states it).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` clean, `test_case_guards -k NPH-` pass. Not yet in `DISCRIMINATOR_CONDITIONS`: the post-tap follow-up's prose `assessment_type` is deliberate until the timing discriminator lands (CENTRAL C2 in the decisions file).
