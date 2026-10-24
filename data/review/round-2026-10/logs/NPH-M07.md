# NPH-M07
Reviewer status: R1 not reviewed, R2 not reviewed (NPH has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was never annotated; no note ids exist. The July 2026 tool review (Reviewer 1, `condition_tool_guidance.yaml` key `nph`) is applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search`, criterion `action-1-search-medical-literature` | Literature search as a recommended clinical step; `general` output repeated the criterion's expected evidence (leak-test failure). | FIXED (C1): criterion deleted, both outputs null. |
| C | major | `followup_outputs[0]` (`request_drug_interactions_b12_metformin`) | Drug check used as management (IM B12 prescription) with no criterion. | FIXED (C2): deleted; B12 replacement is now a must. |
| D | major | `patient.chief_complaint`, `patient.history_present_illness` | "admitted for NPH evaluation"; HPI gave the outside MRI measurements (Evans 0.30, callosal angle 91 degrees, "does not meet NPH criterion") and the lumbar MRI result. | FIXED (C3): referral question and a qualitative outside-MRI sentence; lumbar stenosis left as known history; no antecedent event stated. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | Exam gave TUG 30 s, 10-m walk 24 s and MoCA 21/30, the results of the scored assessments. | FIXED (C4): qualitative gait only; numbers moved to the baseline gait report and the new MoCA follow-up. |
| C | major | `patient.neurological_exam.sensory` | "Mild saddle anesthesia" with urinary incontinence and lumbar stenosis is a cauda equina red flag that would demand urgent spine imaging, which the case never pursues. | FIXED: replaced by "No saddle anaesthesia"; the authored lumbar MRI shows no cauda equina compression. |
| E | minor | `patient.neurological_exam.reflexes`, `.motor`, `.additional` | Garbled "(2- vs 1+)", interpretive parentheses ("diabetes/neuropathy", "could be diabetic amyotrophy vs lumbar stenosis"), duplicated obesity remark. | FIXED: plain findings; tone described as paratonia. |
| B | minor | `patient.clinical_history.past_medical_history` | "Morbid obesity" with BMI 32.1 (class I obesity). | FIXED: "Obesity (BMI 32)"; diabetes entry names metformin and insulin. |
| C | major | `initial_tool_outputs.mri` | Evans index 0.30 fails "greater than 0.3"; no supportive feature; lumbar spine findings inside a brain MRI; no technique, temporal horns, DESH, Fazekas, aqueduct, fourth ventricle or MTA. | FIXED (C7): Evans 0.32 with temporal horn enlargement out of proportion to the hippocampi, callosal angle 91 degrees kept, DESH absent, Fazekas 2, patent aqueduct with flow void, MTA 1, no obstruction; lumbar findings removed; canonical impression. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline gait report contained the post-tap result, a "positive tap test" verdict, engineering `criteria_met` keys and the sentence "this is what the case's own tap-trial report states". | FIXED (C6): baseline only (TUG 30 s, 10-m walk 24 s/26 steps, turn 7 steps, qualitative findings incl. obesity not explaining the gait); `criteria_met` and `pre_post_comparison` null. |
| D | minor | `initial_tool_outputs.csf.interpretation`, `.special_tests.note` | Interpretation was a recital; note attributed the residual weakness to "lumbar/diabetes". | FIXED (C5): canonical interpretation; special tests carry the figures and a plain observation; glucose ratio shows the paired serum glucose (162 mg/dL) that explains 0.42. |
| C | major | `initial_tool_outputs.labs` | HIV "Baseline workup" row with management-style significance; HbA1c reference "<7.0 for diabetics"; MMA only marginally raised (320 vs <271) with creatinine at the upper limit, so not clearly B12-related; summary interpretive. | FIXED (C9): HIV row removed; HbA1c ref <5.7; B12 202 kept, MMA 520 nmol/L, folate, MCV, platelets, potassium added; all `clinical_significance` null; pattern-only interpretation. |
| B | minor | `fallback_tool_outputs.ct`, `.ecg`, `.cardiac_monitoring`, `.echo` | CT fallback said ventricles normal; ECG rate 59 labelled normal sinus rhythm with "benign incidental finding"; Holter "only benign findings"; echo without `echo_type`. | FIXED (C18): CT shows Evans about 0.32; ECG rate 62, descriptive; Holter impression descriptive; `echo_type: TTE`. |
| A | major | `ground_truth.action_criteria` | Order and tiers per plan 3.1 missing: no post-tap reassessment, no cognitive screen, lab panel list with HIV, rationales repeated labels. | FIXED: MRI, labs (recommended, `{}`), baseline gait, MoCA (optional, new `action-cognitive-screen-moca`), lumbar spine MRI (optional, new `action-lumbar-spine-mri`), CSF, post-tap reassessment (recommended, new `action-post-tap-gait-reassessment`); case-specific rationales and expected evidence matched to the reports. |
| A | minor | `followup_outputs` | No outputs for the cognitive screen, spine MRI or post-tap reassessment (library would answer with a normal MoCA). | FIXED: three authored follow-ups (`request_moca_cognitive_screen`, `request_lumbar_spine_mri`, `request_post_reassessment`), in pathway order. |
| C | major | `ground_truth.assessment.required_recommendations` | Four process musts (MRI before LP, baseline gait, 30-50 mL, reassess) and a generic referral. | FIXED (C11): referral must with the case's figures; B12 replacement must; counselling that the neuropathic/stenotic deficits will not respond. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong criterion "DESH, callosal angle <90 and the triad are required"; AD prohibition copied although AD is not in question. | FIXED (C12): canonical text; AD prohibition removed; lumbar stenosis prohibition and a prohibition on withholding referral for the equivocal callosal angle/DESH added. |
| C | major | `ground_truth.differential` | VCI "high", PD/AD/atrophy "moderate" after a positive tap; PD entry argued from DESH the MRI lacks. | FIXED (C13): VCI moderate (Fazekas 2), PD, AD, atrophy low; lumbar stenosis and neuropathy entries added (low); every entry cites the case's data. |
| C | minor | `ground_truth.avoided_actions` | Advanced imaging, neuropsych battery and generic CSF assays not marked waste; generic rationales. | FIXED (3.3): three waste entries added (advanced imaging, neuropsych battery, 14-3-3/RT-QuIC/OCB/meningitis panel/HSV PCR); rationales case-specific. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | Reasons non-canonical; `max_additional_actions` 0. | FIXED (3.4, 3.5): canonical reasons; stop rule MRI, baseline gait, CSF with allowance 1. |
| C | minor | `ground_truth.key_clinical_evidence` | "Tap-test sensitivity 50-80%"; "triad required"; tier sentence. | FIXED (C19, F1-F5): rewritten with the case's figures and the Marmarou figures. |
| B | minor | `ground_truth.red_herrings[1]` | Data point "potential peripheral neuropathy" not present in the patient block; interpretation argued from DESH. | FIXED (C20): data point is the exam's distal sensory loss; both interpretations rewritten. |
| E | minor | `metadata.vocab_gap`, `.difficulty_rationale`, `.difficulty_variant_description`, `.fallback_tool_kinds` | Stale phase-contrast note; counts and "Evans exactly 0.30" out of date. | FIXED (C19). |

## Changes, in one paragraph a physician can read before re-reviewing
The patient block no longer gives the outside imaging measurements, the referral diagnosis, the timed gait values or the MoCA; the exam drops an unexplained saddle anaesthesia and interpretive parentheses, and obesity is graded correctly. The brain MRI is now a complete iNPH read: Evans index 0.32 with temporal horns enlarged out of proportion to the hippocampi (MTA 1), callosal angle 91 degrees, DESH absent, Fazekas 2, patent aqueduct, no obstruction; the lumbar findings moved to an optional lumbar spine MRI (moderate lateral recess stenosis L3-L4 and L4-L5, unchanged, no cauda equina compression). The gait report is the pre-tap baseline only (TUG 30 s, 10-m walk 24 s), the CSF report gives opening pressure 15 cmH2O, normal content and the tap figures (TUG 26 s at 2 hours, 24 s at 24 hours, 20%; 10-m walk 19.5 s; MoCA 21 to 22) without a verdict, and a separate post-tap reassessment returns the same figures. Labs are recommended and show B12 202 pg/mL with raised MMA 520 nmol/L on metformin. Literature and drug-check steps are gone. Musts are the shunt referral with a programmable valve, B12 replacement, and counselling that neuropathic and stenotic deficits will not respond; prohibitions use the corrected iNPH criterion. The differential keeps vascular cognitive impairment moderate (Fazekas 2) and puts lumbar stenosis, neuropathy, PD, AD and atrophy low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- R2: citation keys `[Nakajima_2021]` (used in the referral must and the soft sequence reason, per the plan's canonical text) and `[ASRA_2018]` are not in the NPH criteria pack yet; criterion `citations` arrays use pack keys only.
- R4: the post-tap reassessment criterion has the same pattern as the baseline criterion, so the scorer cannot tell them apart.
- `perfect_agent.py -v` prints "<- ?" for outputs that carry null fields (MRI, labs, baseline gait), because `_source` compares against `model_dump(exclude_none=True)`. The calls are served by the case's own outputs (verified with `MockServer.get_output`), not by fallbacks.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the pre-round version (`fa1d22e6`) against the current file, and the whole final case. Checked: patient block free of Evans, callosal angle, DESH, NPH, tap, shunt, TUG and MoCA (only the qualitative outside-MRI sentence remains); MRI meets F2 (Evans 0.32 with temporal horns out of proportion to MTA 1, callosal angle 91, DESH absent, Fazekas 2 wording matches the grade, no spine content); baseline gait report has no post-tap data; the tap figures agree across the CSF report, the reassessment follow-up, the three criteria and the referral must (TUG 30 to 26 to 24 s, 13% and 20%; 10-m walk 24 to 19.5 s, 19%); MoCA subscores sum to 21; labs (B12 202, MMA 520, HbA1c <5.7 reference) match the criterion and the B12 must; red herrings point at visible data; differential likelihoods follow C13; tiers, sequence constraints and stop rule follow plan 3.1 to 3.5; avoided actions use vocabulary terms. The paired serum glucose (162 mg/dL) in the CSF report matches the lab glucose, and a CSF glucose of 68 mg/dL with ratio 0.42 is acceptable in hyperglycaemia. MockServer probe: cognitive screen then "baseline before tap test" returns the baseline; post-tap call after the CSF returns the follow-up; `spine_MRI` returns the authored lumbar MRI. `perfect_agent.py -v`, `case_io.py check` and `test_case_guards` clean. No error found; no change made.

## Condition audit (NPH auditor, 24 Oct 2026)
- MoCA attention finding "Slowed serial subtraction with two errors; digit span backward 3." -> "Slowed serial subtraction with two errors; digits backward failed." so the finding scores to the stored Attention subscore (4/6); totals unchanged.
- `[Tisell_2011]` removed from `action-4-analyze-csf.citations`: the pack entry is Tisell 2011, shunt surgery in hydrocephalus with white matter changes, and this rationale is about the tap response only; `[Marmarou_2005]` (tap test) stays.
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
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
