# NPH-S06
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review applies) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was not annotated in this round; no note id exists for this case. The July 2026 tool review (`condition_tool_guidance.yaml` key `nph`) is applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/C | major | `ground_truth.action_criteria[action-1-search-medical-literature]`, `followup_outputs[2]` (`request_literature_severe_nph_outcomes`) | Literature search as a recommended clinical step; follow-up with unverifiable registry claims (plan C1, ruling 5). | FIXED: criterion and follow-up deleted; initial and fallback `literature_search` null. |
| C | major | `followup_outputs[1]` (`request_aspirin_perioperative_management`) | Drug check wrote shunt management and wrong advice ("Hold aspirin 5-7 days"); no interaction (C2, ruling 6). | FIXED: deleted; `drug_interactions` initial and fallback null; aspirin must and prohibition added per ASRA 2018. |
| C | minor | `followup_outputs[0]` (`request_cardiac_clearance_pre_shunt`) | Echo "cardiac clearance" follow-up, with a "Normal" placeholder finding (C18). | FIXED: deleted; its findings (EF 58%, mild aortic sclerosis) moved into the TTE fallback so the case stays consistent. |
| D | major | `patient.history_present_illness` | HPI quoted the outside MRI as showing "significant ventriculomegaly" and "admitted for comprehensive NPH evaluation and tap trial" (C3). | FIXED: canonical qualitative sentence (enlarged ventricles reported, images not available) and referral question; no NPH, tap or shunt wording. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | Exam gave TUG 38 s, 10-m walk 32 s and MoCA 18/30 with domain scores, the results of the scored assessments (C4). | FIXED: qualitative gait only (en-bloc turning added, consistent with the report); mental status keeps orientation and insight, "formal cognitive screening reported separately". Numbers live in the baseline gait report and the cognitive-screen follow-up. |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Baseline gait report contained the post-tap result, a verdict in `criteria_met` and the engineering sentence "this is what the case's own tap-trial report states" (C5, C6). | FIXED: baseline only (TUG 38 s with rollator, 10-m walk 32 s in 34 steps, turn 9 steps, MoCA 18/30 same session), `criteria_met` and `pre_post_comparison` null, descriptive impression. |
| A | major | `followup_outputs` | No post-tap reassessment and no case-authored cognitive screen (C6). | FIXED: follow-ups `request_moca_cognitive_screen` (MoCA 18/30, subscores summing to 18, recall 0/5 free with cueing benefit, orientation 4/6 matching "not date") and `request_post_reassessment` (TUG 28 s at 2 h, 24 s at 24 h, 10-m 21 s, MoCA 21, identical to the CSF report). |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | "Positive tap trial" verdict (C5). | FIXED: canonical figures-only interpretation; special_tests keep the stored values (45 mL, 38/28/24 s, 32/21 s, MoCA 18/21, urinary). Percentages checked: 26%, 37%, 34%. |
| C/D | major | `initial_tool_outputs.mri` | No technique line, no temporal horns, fourth ventricle, MTA, no-obstruction statement; DESH described only as "Florid DESH pattern" (C7). | FIXED: technique line (3T, no contrast), both DESH components, temporal horns out of proportion to hippocampi, aqueduct patent with flow void, fourth ventricle mildly enlarged, Fazekas 2, MTA 2, no obstruction, no subdural collection (relevant after his head-injury fall); canonical impression. Stored values (Evans 0.42, callosal angle 65 degrees, Fazekas 2) unchanged. |
| B | minor | `initial_tool_outputs.labs` | HIV row in a "Baseline workup" panel with an interpretive `clinical_significance`; RPR filed under Metabolic (C9). | FIXED: RPR and HIV moved to a Serology panel, every `clinical_significance` null, pattern-only interpretation. Values unchanged. |
| B | major | `fallback_tool_outputs.ct` | CT fallback said ventricles normal, against Evans 0.42 (C18). | FIXED: canonical CT fallback (Evans about 0.41, white matter hypodensity, no subdural collection). |
| E | minor | `fallback_tool_outputs.ecg`, `.echo`, `.cardiac_monitoring` | "Benign incidental finding" wording; echo "structurally normal heart" contradicted the deleted echo follow-up; echo had no `echo_type`; Holter max HR 131 and mean 80 implausible on metoprolol with resting HR 62. | FIXED: ECG states sinus rhythm with PACs; TTE fallback with `echo_type: TTE`, EF 58%, mild aortic sclerosis; Holter mean 66, max 108, PACs noted. |
| B | minor | `patient.clinical_history.past_medical_history` | Lisinopril indication "post-MI cardioprotection" but no MI in the PMH. | FIXED: "Coronary artery disease (myocardial infarction treated with CABG 12 years ago)"; ECG fallback states no pathological Q waves. |
| E | minor | `patient.history_present_illness` | "episodes of soiling" for urinary incontinence (soiling means faecal). | FIXED: "episodes of urge incontinence". Falls now stated as gait falls without loss of consciousness, which the ECG and monitoring waste rationales rely on. |
| C | major | `ground_truth.assessment.required_recommendations` | Four process musts (MRI before LP, document baseline, remove 30-50 mL, reassess) and a generic referral (C11). | FIXED: referral (37% TUG, DESH, normal-pressure CSF; age 80 and stable CAD not contraindications), aspirin continuation [ASRA_2018], falls prevention (four falls, one with laceration). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "DESH, callosal angle <90 and the triad are required" is wrong (F1, F2); AD prohibition copied although AD is not in question (C12). | FIXED: canonical ventriculomegaly prohibition; AD prohibition removed; normal-ageing prohibition reworded; added "Do not stop aspirin for the lumbar tap" and "Do not withhold shunt referral on the grounds of age alone". LP-before-MRI prohibition kept in the condition's shared wording. |
| C | major | `ground_truth.differential` | VCI high, PD, AD and atrophy moderate after DESH and a 37% tap response (C13, ruling 7). | FIXED: VCI moderate (Fazekas 2), PD low, AD low (brother with AD named, cueing benefit, MTA 2), atrophy low, secondary hydrocephalus low (no antecedent, no subdural collection); one case-specific sentence each. |
| C/E | major | `ground_truth.key_clinical_evidence` | Triad and DESH stated as required, "sensitivity 50-80%", "Tier per the July 2026 clinical review" (C19, F1, F4). | FIXED: rebuilt from F1 to F5 with the case's own figures. |
| A | minor | `ground_truth.action_criteria[*]` | Rationale identical to label; "NPH_pack" and unbracketed citations; labs criterion with a fixed panel list (C9, C19). | FIXED: criteria rebuilt per plan 3.1 (MRI, labs optional `{}`, baseline gait, cognitive screen optional, CSF, post-tap recommended), ids kept, case-specific rationales, expected evidence matching the outputs. |
| A | minor | `ground_truth.avoided_actions` | No avoided entry for advanced imaging, neuropsych battery or generic CSF assays; generic rationales (C10, 3.3). | FIXED: added the three; every rationale case-specific. |
| A | minor | `ground_truth.stop_rule`, `.sequence_constraints` | `max_additional_actions` 0; soft constraint cited Relkin. | FIXED: stop rule MRI, baseline gait, CSF with allowance 1; constraints per plan 3.4. |
| E | minor | `metadata.vocab_gap`, `.difficulty_rationale`, `patient...social_history.alcohol` | Stale phase-contrast gap; counts of removed tools; an em dash. | FIXED: gap removed, counts updated, dash replaced; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

An 80-year-old man with three years of magnetic gait, urge incontinence and frontal-subcortical cognitive decline. The patient block no longer gives the outside MRI measurements, the referral diagnosis or the timed gait and MoCA scores. The pathway is now brain MRI (required; Evans 0.42, both DESH components, callosal angle 65 degrees, temporal horns enlarged, aqueductal flow void, Fazekas 2, MTA 2, no obstruction or subdural collection), optional targeted labs (normal), the baseline timed gait (required; TUG 38 s with rollator, 10-m walk 32 s), an optional MoCA (18/30, retrieval deficit with cueing benefit), the CSF tap test (required; opening pressure 15 cmH2O, normal content, 45 mL removed) and the post-tap reassessment (recommended; TUG 24 s at 24 hours, 37% faster; MoCA 21). The literature search, the aspirin "hold 5-7 days" drug check and the pre-shunt echo were removed. Musts: neurosurgical referral for a programmable-valve shunt (age 80 and stable coronary disease are not contraindications), continue aspirin 81 mg through the tap (ASRA 2018), falls prevention. Prohibitions: tap before MRI, iNPH from ventriculomegaly alone, attributing it to ageing, stopping aspirin, withholding referral for age. The differential is the post-work-up view: VCI moderate, everything else low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: the musts and the soft constraint cite `[Nakajima_2021]`, `[ASRA_2018]` and `[Halperin_2015]` (canonical plan text), which are not yet in the criteria pack allow-list.
- Plan R4: the post-tap criterion has the same pattern as the baseline one; the baseline call alone credits it until `timing` becomes a discriminator.
- Plan R5: a re-order phrased "repeat gait after lumbar puncture" returns the baseline report again (no leak, but the post-tap figures are then only in the CSF report).
- Plan R7: an `order_specialized_test {neuropsych_battery}` order (waste) is answered by the library with "Cognitive performance within normal limits across all domains", which contradicts his MoCA 18/30.
- `perfect_agent.py -v` prints `<- ?` for outputs served from `initial_tool_outputs` when the stored dict omits default-None fields; the hijack check confirms MRI and baseline gait are served from the case's initial outputs.

## Open questions for Andrea (judgment calls you could not settle)

None. CSF protein 48 mg/dL was kept and reported as normal: it is within the age-adjusted reference for an 80-year-old.

## Verification

Checked against `plans/NPH.md` (sections 2 to 4 and the per-case entry), ROUND_POLICY and PATTERNS; NPH has no notes file, so there is no note id to account for. Read the whole final case (flattened, every field) and compared it with the pre-round version (`1fd43d22~1`). Verified: patient block free of Evans, callosal angle, DESH, NPH, hydrocephalus, tap, shunt, TUG and MoCA results; literature and drug-interaction outputs null with no such follow-ups; MoCA subscores sum to the total and match the exam orientation; TUG and 10-m percentages recomputed from the stored seconds and identical in the baseline report, the CSF report, the post-tap follow-up and the criteria; CSF/serum glucose ratio consistent with the lab glucose; Evans index identical in the MRI, CT fallback (within 0.01), criteria and key evidence; Fazekas grade matches the VCI likelihood (plan C13); musts, prohibitions and differential match plan section 4; discriminator values (`holter_24h`, `TTE`, CSF assay terms) are vocabulary terms; criteria order and tiers per plan 3.1, constraints per 3.4, stop rule per 3.5. Hijack check (MockServer through `NeuroBenchEnvironment`): cognitive screen then "baseline timed gait before tap test" returns the baseline (no `pre_post_comparison`); after the CSF call "post-tap reassessment at 24 hours" returns the follow-up; "repeat timed gait after lumbar puncture" re-serves the baseline (plan R5, already logged). `perfect_agent.py -v`, `case_io.py check` and `test_case_guards -k` pass after the changes below.

Found and changed:
- `ground_truth.action_criteria[action-post-tap-gait-reassessment].rationale`: the same template sentence in every NPH case (C19 asks for a case-specific rationale). Rewritten with his rollator, the 45 mL tap and the 2 and 24 hour timings.
- `ground_truth.action_criteria[action-4-analyze-csf].citations`: `[Tisell_2011]` removed. That key is "Shunt surgery in patients with hydrocephalus and white matter changes" (J Neurosurg 2011), not a tap-test source; `[Marmarou_2005]` covers the tap test (ruling 8). Lead: the pack line for `analyze_csf` attributes the tap test to `[Tisell_2011]`, and plan 1.1 calls it "tap-test predictors"; the same mis-citation is likely in the other NPH cases.
- `ground_truth.key_clinical_evidence[5]`: "age alone does not preclude benefit" was attributed to `[Halperin_2015]`, which grades shunting "possibly effective" but is not the source for an age statement. Split so the citation covers only the AAN grading; the age point stays as clinical reasoning, consistent with the referral must.
- `patient.neurological_exam.additional`: "Bilateral grasp reflexes present bilaterally" (duplicated word) became "Grasp reflexes present bilaterally".
- Nothing else found: the PMH MI wording, the falls without loss of consciousness, the urge incontinence wording, the echo/ECG/Holter fallbacks and the CSF protein 48 mg/dL (normal for age 80) are correct as the worker logged them.

## Condition audit (NPH auditor, 24 Oct 2026)
- `analyze_csf {"special_tests": ["HSV_PCR"]}` added to `avoid-waste-generic-csf-assays`, as in the other 24 NPH cases (plan 3.3, PCR panels).
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
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
