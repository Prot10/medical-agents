# NPH-S04
Reviewer status: R1 not reviewed, R2 not reviewed (NPH has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was never annotated; the only physician input is the July 2026 tool review (`condition_tool_guidance.yaml` key `nph`), applied through plan NPH sections 2 to 4. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs[request_literature_npH_parkinsonian_features]`, `action_criteria[action-1-search-medical-literature]` | Literature as a clinical step, overstating that "normal DaTscan effectively excludes Parkinson's disease" (C1, ruling 5). | FIXED: criterion and follow-up deleted; literature initial and fallback null. The parkinsonian point moved to a key pearl, a prohibition and a red herring (plan S04). |
| D | major | `patient.history_present_illness` | Outside CT "showing markedly enlarged ventricles" and "admitted for MRI, lumbar puncture, and tap trial" (C3). | FIXED: canonical outside-CT and referral sentences; em dashes removed. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 25 s, 10-m walk 19 s and MoCA 22/30 with subscores in the exam (C4). | FIXED: qualitative; numbers in the gait report and the cognitive-screen follow-up. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline report held the post-tap result, the engineering sentence and `criteria_met` keys (C6). | FIXED: baseline only (TUG 25 s, 10-m walk 19 s in 30 steps, turn 7 steps, MoCA 22/30, reduced arm swing, doorway freezing); post-tap figures in follow-up `request_post_reassessment`. |
| D | major | `initial_tool_outputs.csf.interpretation` | "Positive tap trial" (C5). | FIXED: C5 canonical form (40 mL; TUG 25 to 19 s at 2 h, 17 s at 24 h, 32%; 10-m 19 to 13 s; MoCA 22 to 24); freezing outcome kept in special_tests. |
| D | major | `initial_tool_outputs.mri` | "Classic DESH" without components, "transependymal" interpretation, white matter in two overlapping findings, no technique, temporal horns, hippocampi or fourth ventricle (C7). | FIXED: rebuilt with the C7 elements (Evans 0.37, DESH both components, callosal angle 76, temporal horns with MTA 1, Fazekas 1, aqueduct flow void, normal fourth ventricle, no obstruction) and an SWI pertinent negative for the PD question (nigral hyperintensity preserved); canonical impression. |
| B | minor | `initial_tool_outputs.labs` | Non-fasting glucose 114 flagged high against a fasting range; HbA1c 6.8% not flagged with a "<7% target" reference; HIV "Baseline workup" row; interpretive summary ("known T2DM") (C9). | FIXED: glucose labelled non-fasting with 70-140 range, not flagged; HbA1c reference "<5.7", flagged high; Serology panel; factual summary and interpretation; criterion `interpret_labs {}` optional. |
| C | major | `ground_truth.assessment` | Process musts; wrong DESH-plus-triad prohibition; AD prohibition where AD is not in question (C11, C12). | FIXED: musts are referral (32%) and falls prevention (three falls); prohibitions MRI-first, canonical, PD attribution of the lower-body parkinsonism, ageing/deconditioning. |
| C | minor | `ground_truth.red_herrings` | Neuropathy red herring said "long-standing" diabetes and pointed at the PMH; the parkinsonian features named in `difficulty_variant_description` had no red herring. | FIXED: neuropathy red herring kept (the exam documents vibration loss at the great toes, C20) and pointed at the sensory exam; parkinsonian-features red herring added (gait exam). The father's late memory problems are not modelled as a red herring; the metadata description no longer claims it. |
| C | major | `ground_truth.differential` | VCI "high" with Fazekas 1; PD, AD and ex vacuo "moderate" after DESH and a 32% tap response (C13). | FIXED: all low with case data (VCI low because Fazekas 1, plan S04); diabetic neuropathy added as low. |
| C | minor | `ground_truth.key_clinical_evidence` | Tier sentence; "sensitivity only 50-80%". | FIXED: four pearls, the last explaining the lower-body parkinsonism and why no levodopa trial is needed (plan S04). |
| C | minor | `ground_truth.action_criteria`, `avoided_actions`, `sequence_constraints`, `stop_rule` | Label equals rationale, "NPH_pack"; no post-tap or cognitive criteria; waste entries missing; allowance 0. | FIXED: plan 3.1 order and tiers; advanced imaging (including DaTscan, whose library normal agrees with this case), battery and generic CSF assays as waste; canonical constraints; allowance 1. |
| B | minor | `fallback_tool_outputs.ct`, `.echo`, `.drug_interactions` | CT "without acute abnormality" against ventriculomegaly; echo "benign incidental finding", no `echo_type`; placeholder drug check (C18, C2). | FIXED: CT shows enlarged ventricles (Evans about 0.36); echo states the sclerosis, `echo_type: TTE`; drug check null. |
| E | minor | `metadata` | Stale phase-contrast note; removed-tool counts; em dash. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The HPI no longer announces the tap trial or quotes the CT; the exam is qualitative. The literature step is gone. The pathway is MRI, optional labs (HbA1c 6.8%), baseline timed gait (TUG 25 s, 10-m walk 19 s, turn 7 steps, doorway freezing, reduced arm swing), optional MoCA (22/30, dysexecutive with cue-responsive recall), the tap test (opening pressure 14 cmH2O, normal CSF, 40 mL; TUG 19 s at 2 h and 17 s at 24 h, 32%; 10-m walk 13 s; MoCA 24; no freezing at 24 h) and a recommended post-tap reassessment. The MRI reports Evans 0.37, DESH, callosal angle 76 degrees, temporal horns out of proportion to MTA 1 hippocampi, Fazekas 1, a patent aqueduct and a preserved nigral hyperintensity on SWI. Musts are shunt referral and falls prevention. The case now handles its parkinsonian features explicitly: a red herring, a prohibition against calling them Parkinson's disease, and a pearl that lower-body parkinsonism without tremor, rigidity or bradykinesia needs no levodopa trial. All differential alternatives are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation key `[Nakajima_2021]` used per plan 1.1 (plan CENTRAL R2).
- Post-tap criterion shares the baseline pattern (plan CENTRAL R4); hijack check as in S01.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

What I checked: Read the log and the final case (diffed against S01). Checked against the pre-round file that the reduced arm swing and the great-toe vibration loss are original exam findings. MoCA subscores sum to 22. The non-fasting glucose 114 is against 70-140 and not flagged; HbA1c 6.8% is flagged. The SWI pertinent negative (nigral hyperintensity preserved) agrees with the PD differential and the prohibition. Figures agree across the reports, criteria and must. Every log row checked. Checks run after the edits: `perfect_agent.py -v` ok (MRI and baseline gait show `<- ?` only because of null fields; a MockServer run confirmed both come from the case's own initial outputs, not the library), `case_io.py check` clean for the case, `test_case_guards -k` passes. Hijack check (cognitive screen, baseline gait "before tap test", MRI, tap, post-tap reassessment): every call served by the case's own output in the right order, no post-tap leak to the baseline. Discriminator note for the close-out: the post-tap follow-up's `assessment_type` "gait_and_balance_timed (post-tap reassessment)" is the plan's deliberate prose value (C6). It will fail `test_routed_outputs_name_their_study` once NPH joins `DISCRIMINATOR_CONDITIONS`. Renaming it to the bare term would let the discriminator serve it at the baseline call, so this needs plan CENTRAL R4, not a rename.

Found and fixed:
1. (C, minor) `ground_truth.key_clinical_evidence[0]` stated what probable iNPH "needs" [Relkin_2005] but left out the physiological criterion. Added "a CSF opening pressure of 5 to 18 mmHg (7 to 24.5 cmH2O)" (F3). In `[2]`, the 10% TUG criterion is cited to [Nakajima_2021] (F4); before, only [Marmarou_2005] was cited.
2. (C, minor) The parkinsonism red herring's `correct_interpretation` called symmetric parkinsonism "typical of iNPH" and labelled it lower-body, though its data point is reduced arm swing (upper body). It now reads that freezing and reduced arm swing without rest tremor, rigidity or limb bradykinesia "occur in iNPH as a lower-body-predominant parkinsonism", which matches the prohibition and the key evidence.

Changed: Edited `key_clinical_evidence[0]` and `[2]`, and `red_herrings[Reduced arm swing ...].correct_interpretation`. Nothing else changed: no labels, tiers, criteria, sequence or stop rule. 

## Condition audit (NPH auditor, 24 Oct 2026)
- Lab rows RPR moved from the `Metabolic` panel to `Serology`; values unchanged.
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
- `key_clinical_evidence`: the 10% TUG threshold is no longer attributed to `[Nakajima_2021]`, which sets no numeric tap-test cut-off; it is stated as a commonly used threshold that no guideline fixes (the tap protocol keeps its Nakajima citation where the sentence states it).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` clean, `test_case_guards -k NPH-` pass. Not yet in `DISCRIMINATOR_CONDITIONS`: the post-tap follow-up's prose `assessment_type` is deliberate until the timing discriminator lands (CENTRAL C2 in the decisions file).
