# NPH-S09
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review applies) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was not annotated in this round; no note id exists for this case. The July 2026 tool review (`condition_tool_guidance.yaml` key `nph`) is applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/C | major | `ground_truth.action_criteria[action-1-search-medical-literature]`, `followup_outputs[1]` (`request_vascular_contribution_white_matter`) | Literature search as a recommended clinical step; the follow-up was the white-matter question disguised as a search (C1, ruling 5). | FIXED: criterion and follow-up deleted; literature outputs null. The real point (white matter disease does not preclude shunt benefit, Tisell 2011) is now a prohibition and a key evidence line. |
| C | major | `followup_outputs[0]` (`request_ckd_insulin_perioperative`) | Drug check wrote perioperative diabetes management and gadolinium thresholds (C2). | FIXED: deleted; `drug_interactions` null. |
| D | major | `patient.history_present_illness` | "admitted for NPH evaluation", granddaughter "recognized the classic triad", outside CT "Evans index approximately 0.39", and an eGFR sentence "relevant for contrast administration planning" (C3, C7). | FIXED: evaluation of functional decline, the triad wording removed, CT reported qualitatively (images not available), referral question; the contrast sentence deleted (CKD stage 2 stays in the PMH). Falls stated as initiation or turning falls without loss of consciousness. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 34 s, 10-m walk 28 s, MoCA 20/30 and its domain results in the exam (C4). | FIXED: qualitative gait (en-bloc turning and rollator added, consistent with the report); "formal cognitive screening reported separately". |
| B/C | minor | `patient.neurological_exam.motor` | "Mild hip flexor weakness bilaterally (4+/5)": a deficit that neither iNPH nor anything else in the case explains, and no study addresses (pattern 3, deficits no lesion explains). | FIXED: "Full strength throughout". Logged here so a re-reviewer can restore it with a cause if preferred. |
| B | minor | `patient.neurological_exam.sensory` | Em dash; sensory exam did not say whether joint position was tested, which the neuropathy reasoning needs. | FIXED: "Mildly reduced vibration at both ankles and distal feet. Light touch and joint position intact." |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Baseline report contained the post-tap result, `criteria_met` keys and the engineering sentence (C5, C6). | FIXED: baseline only (TUG 34 s with rollator, 10-m walk 28 s in 38 steps, turn 10 steps, MoCA 20/30). |
| A | major | `followup_outputs` | No post-tap reassessment, no case cognitive screen (C6). | FIXED: `request_moca_cognitive_screen` (MoCA 20/30, subscores sum to 20, recall 1/5 free, 3/5 cued, 5/5 multiple choice, orientation 5/6 for "uncertain of date") and `request_post_reassessment` (TUG 24 s at 2 h, 22 s at 24 h, 10-m 18 s, MoCA 23). |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | "Positive tap trial" verdict (C5). | FIXED: canonical figures-only text; values kept (42 mL, 34/24/22 s, 28/18 s, MoCA 20/23); percentages checked (29%, 35%, 36%); CSF/serum glucose 70/138 = 0.51 consistent with the labs. |
| C/D | major | `initial_tool_outputs.mri` | "Contrast not administered given CKD stage 2" (a wrong renal reason, C7); "transependymal" in the impression; aetiology "from hypertension and diabetes"; markers missing. | FIXED: technique line without a renal reason; full marker set with stored values (Evans 0.41, DESH, callosal angle 68 degrees, flow void, Fazekas 2); MTA 2; impression describes Fazekas 2 "in keeping with small-vessel disease, without lacunes". |
| C | major | `initial_tool_outputs.labs` | Creatinine 1.4 (flagged high) contradicts CKD stage 2 (C9); HbA1c reference "<8% target" with no flag; HIV "Baseline workup" panel. | FIXED: creatinine 1.1 mg/dL (normal) with a new eGFR row 70 mL/min/1.73m2 (CKD-EPI 2021 for a 75-year-old man, CKD stage 2 range); HbA1c reference <5.7%, flagged high; Serology panel; `clinical_significance` null; interpretation and abnormal summary rewritten. |
| B | minor | `patient.clinical_history.past_medical_history`, `.medications[Metformin].indication` | "Type 2 diabetes (on insulin)" although he also takes metformin; "low dose given CKD stage 2" is not a dosing rule (no reduction above eGFR 45). | FIXED: "Type 2 diabetes mellitus on insulin glargine and metformin"; indication "type 2 diabetes mellitus". |
| B | major | `fallback_tool_outputs.ct` | Normal ventricles in the CT fallback (C18). | FIXED: canonical CT fallback (Evans about 0.41). |
| E | minor | `fallback_tool_outputs.cardiac_monitoring`, `.echo`, `.ecg` | "benign" and "only benign findings" wording; no `echo_type`; removed `clinical_correlation`. | FIXED: findings stated; `echo_type: TTE`. |
| C | major | `ground_truth.assessment.required_recommendations` | Process musts; nothing on the missed insulin doses (C11). | FIXED: referral (35% TUG, DESH, normal-pressure CSF); supervision of insulin and metformin by the family (memory impairment has caused missed insulin doses); falls prevention (five falls, one wrist sprain). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong triad/DESH requirement; AD prohibition copied; ageing prohibition generic (C12). | FIXED: canonical ventriculomegaly prohibition; "Do not withhold shunt referral because of the Fazekas 2 white matter change [Tisell_2011]"; "Do not attribute the magnetic gait with freezing to diabetic peripheral neuropathy"; LP-before-MRI kept; AD and ageing prohibitions removed (neither is in question). |
| C | major | `ground_truth.differential` | VCI high and PD, AD, atrophy moderate after DESH and a 35% tap (C13). | FIXED: VCI moderate (Fazekas 2); neuropathy (the case's red herring) added, low; PD, AD (MTA 2), atrophy and secondary hydrocephalus low. |
| B | minor | `ground_truth.red_herrings[0]` | Pointed at the PMH "potential peripheral neuropathy"; C20 keeps it only with exam signs, which this exam has. | FIXED: `data_point` and `field_path` now the exam's distal vibration loss; interpretation one sentence. |
| C/E | major | `ground_truth.key_clinical_evidence` | Triad and DESH as requirements, "sensitivity 50-80%", tier sentence (C19). | FIXED: rebuilt from F1 to F5 with the case figures, plus the Tisell 2011 white-matter line. |
| A | minor | `ground_truth.action_criteria`, `.avoided_actions`, `.stop_rule`, `.sequence_constraints` | Labels equal to rationales, `NPH_pack`, fixed lab panels, generic waste, allowance 0. | FIXED per plan 3.1 to 3.5. |
| E | minor | `patient.chief_complaint`, `...social_history.alcohol`, `metadata` | Em dashes; stale `vocab_gap`; counts; description naming CKD as a red herring "requiring perioperative management". | FIXED; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

A 75-year-old man with diabetes, hypertension and CKD stage 2, with 18 months of magnetic gait with freezing, urge incontinence and executive slowing that has caused missed insulin doses. The HPI no longer gives the CT Evans index, the triad label or a contrast-planning sentence; the unexplained bilateral hip flexor weakness was removed from the exam. Pathway: brain MRI (required; Evans 0.41, both DESH components, callosal angle 68 degrees, temporal horns enlarged, flow void, Fazekas 2 without lacunes, MTA 2; no contrast, and no renal reason given), optional labs (creatinine corrected to 1.1 mg/dL with eGFR 70, HbA1c 7.6% flagged), baseline timed gait (required; TUG 34 s with rollator, 10-m walk 28 s), optional MoCA (20/30 with cueing benefit), CSF tap test (required; opening pressure 15 cmH2O, normal content, 42 mL) and post-tap reassessment (recommended; TUG 22 s at 24 hours, 35% faster; MoCA 23). Literature and the perioperative diabetes drug check were removed. Musts: neurosurgical referral, family supervision of his diabetes medication, falls prevention. Prohibitions: tap before MRI, iNPH from ventriculomegaly alone, withholding referral because of Fazekas 2 white matter change (Tisell 2011), blaming diabetic neuropathy. Differential: VCI moderate, neuropathy and the rest low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[Nakajima_2021]` cited before the key exists in the pack.
- Plan R4, R5, R7 as in NPH-S08 (post-tap pattern; repeat phrasing re-serves the baseline; library neuropsych battery normal contradicts the case).

## Open questions for Andrea (judgment calls you could not settle)

None. The hip flexor weakness was removed rather than explained, because no finding in the case (spine, muscle enzymes, history) supports a cause and the plan rules out inventing one.

## Verification

Checked against `plans/NPH.md` (sections 2 to 4 and the per-case entry), ROUND_POLICY and PATTERNS; NPH has no notes file, so there is no note id to account for. Read the whole final case (flattened, every field) and compared it with the pre-round version (`1fd43d22~1`). Verified: patient block free of Evans, callosal angle, DESH, NPH, hydrocephalus, tap, shunt, TUG and MoCA results; literature and drug-interaction outputs null with no such follow-ups; MoCA subscores sum to the total and match the exam orientation; TUG and 10-m percentages recomputed from the stored seconds and identical in the baseline report, the CSF report, the post-tap follow-up and the criteria; CSF/serum glucose ratio consistent with the lab glucose; Evans index identical in the MRI, CT fallback (within 0.01), criteria and key evidence; Fazekas grade matches the VCI likelihood (plan C13); musts, prohibitions and differential match plan section 4; discriminator values (`holter_24h`, `TTE`, CSF assay terms) are vocabulary terms; criteria order and tiers per plan 3.1, constraints per 3.4, stop rule per 3.5. Hijack check (MockServer through `NeuroBenchEnvironment`): cognitive screen then "baseline timed gait before tap test" returns the baseline (no `pre_post_comparison`); after the CSF call "post-tap reassessment at 24 hours" returns the follow-up; "repeat timed gait after lumbar puncture" re-serves the baseline (plan R5, already logged). `perfect_agent.py -v`, `case_io.py check` and `test_case_guards -k` pass after the changes below.

Found and changed:
- `ground_truth.action_criteria[action-post-tap-gait-reassessment].rationale`: template sentence (C19); rewritten for his rollator, 42 mL tap and white matter change.
- `ground_truth.red_herrings[0].data_point`: "in long-standing type 2 diabetes" is not in the exam field it points at, and the case never states the duration of his diabetes; set to the exam text "Mildly reduced vibration at both ankles and distal feet".
- Kept: `[Tisell_2011]` on the CSF criterion and in the Fazekas prohibition, where the rationale is the white matter question that paper addresses. The eGFR 70 matches CKD-EPI 2021 for creatinine 1.1 mg/dL in a 75-year-old man (recomputed). The removal of the unexplained 4+/5 hip flexor weakness is logged by the worker and accepted.
- Nothing else found.

## Condition audit (NPH auditor, 24 Oct 2026)
- `analyze_csf {"special_tests": ["HSV_PCR"]}` added to `avoid-waste-generic-csf-assays`, as in the other 24 NPH cases (plan 3.3, PCR panels).
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

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3; requires considerable assistance (fallback_tool_outputs.clinical_assessment). Why: the library gives Karnofsky 100 / ECOG 0 (no evidence of disease, working) in a symptomatic patient.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: MDS-UPDRS III 22 to 21 (5%); gait, gait initiation, turning and postural stability unchanged; no clinically meaningful levodopa response (below 30%) (followup_outputs[2] request_levodopa_challenge). Why: the library describes a normal motor examination and gait; this patient has a gait disorder, and the challenge shows little or no levodopa response.
- `order_specialized_test {test_type: neuropsych_battery}`: frontal-subcortical profile of moderate severity (slowed processing, executive and attention deficits, recognition relatively preserved) (fallback_tool_outputs.specialized_test). Why: the library reports normal cognition in every domain; this patient has documented cognitive impairment on the stored bedside screen.
- `order_specialized_test {test_type: exercise_stress_test}`: treadmill test not performed (unable to walk safely on a treadmill (prominent freezing; walks with a rollator)); non-diagnostic (followup_outputs[3] request_exercise_stress_test). Why: the library describes a 9.5-minute Bruce protocol at 10.4 METs; this patient's gait disorder (magnetic gait with falls) does not allow it.
- `order_echocardiogram {echo_type: exercise_echo}`: exercise not performed (unable to walk safely on a treadmill (prominent freezing; walks with a rollator)); resting findings as on the stored TTE (followup_outputs[4] request_exercise_echo). Why: the library describes 9.5 METs on a treadmill with a normal echo; this patient's gait disorder does not allow it.
- Checks: perfect agent ok; case guards pass; criteria answers unchanged.
