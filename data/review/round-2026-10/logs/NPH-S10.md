# NPH-S10
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review applies) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was not annotated in this round; no note id exists for this case. The July 2026 tool review (`condition_tool_guidance.yaml` key `nph`) is applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/C | major | `ground_truth.action_criteria[action-1-search-medical-literature]`, `followup_outputs[2]` (`request_vascular_dementia_af_contribution`) | Literature search as a recommended clinical step; follow-up disguised the AF/vascular question as a search (C1, ruling 5). | FIXED: criterion and follow-up deleted; literature outputs null. The AF point is now the red herring, a prohibition and the VCI differential entry. |
| C | blocker | `followup_outputs[0]` (`request_apixaban_shunt_perioperative`) | Drug check advised "discuss bridging anticoagulation (parenteral)" and a 48-72 h hold, against ASRA 2018 (no bridging of a DOAC, at least 72 h) (C2). | FIXED: deleted; `drug_interactions` null; canonical DOAC must and prohibition [ASRA_2018]. |
| A | major | `followup_outputs[1]` (`request_cardiac_monitoring_af`) | Monitoring follow-up with empty `monitor_type` and `heart_rate_range`, used as a red herring for a diagnosis already in the history (C18). | FIXED: deleted; red herring rewritten as "Known paroxysmal atrial fibrillation on apixaban" in the PMH. |
| D | major | `patient.history_present_illness` | "admitted for NPH evaluation", family "recognizing the classic triad", "anticoagulation will need to be held before lumbar puncture" (management in the history), "admitted for comprehensive NPH workup including DOAC hold protocol before LP" (C3). | FIXED: evaluation of progressive decline, outside MRI reported qualitatively (images not available), referral question; the hold is now only a must. Falls stated as gait falls without loss of consciousness or palpitations. |
| B | major | `patient.neurological_exam.additional` vs `fallback_tool_outputs.ecg`, `.cardiac_monitoring` | Exam recorded an irregular pulse now, while the ECG and Holter fallbacks are in sinus rhythm. | FIXED: "Pulse regular at the time of examination" (paroxysmal AF; vitals HR 72 unchanged), so the sinus ECG and Holter stay consistent. |
| C | minor | `patient.clinical_history.past_medical_history`, `.medications[Apixaban].indication` | "CHADS2-VASc 3": the score is CHA2DS2-VASc and for a 77-year-old hypertensive woman it is 4 (age 2, sex 1, hypertension 1). | FIXED: "CHA2DS2-VASc 4" in both fields and in the DOAC must. Apixaban 5 mg twice daily stays correct (age under 80, creatinine 0.9). |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 30 s, 10-m walk 24 s, MoCA 20/30 and recall 1/5 in the exam (C4). | FIXED: qualitative gait (en-bloc turning added); "formal cognitive screening reported separately". |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Baseline report contained the post-tap result, `criteria_met` keys and the engineering sentence (C5, C6). | FIXED: baseline only (TUG 30 s with cane, 10-m walk 24 s in 34 steps, turn 9 steps, MoCA 20/30). |
| A | major | `followup_outputs` | No post-tap reassessment, no case cognitive screen (C6). | FIXED: `request_moca_cognitive_screen` (MoCA 20/30, subscores sum to 20, serial 7s poor as in the exam, orientation 5/6) and `request_post_reassessment` (TUG 22 s at 2 h, 20 s at 24 h, 10-m 16 s, MoCA 23). |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | "Positive tap trial" verdict (C5). | FIXED: canonical figures-only text; values kept (40 mL, 30/22/20 s, 24/16 s, MoCA 20/23); percentages checked (27%, 33%, 33%). |
| C/D | major | `initial_tool_outputs.mri` | Impression attributed white matter change "from atrial fibrillation and hypertension"; "Fazekas grade 1-2"; "transependymal"; markers missing (C5, C7). | FIXED: full marker set with stored values (Evans 0.39, DESH, callosal angle 74 degrees, flow void); Fazekas 1, no lacunes, cortical infarcts or microhaemorrhages (the questions AF raises); MTA 2; canonical impression without aetiology. |
| C | major | `initial_tool_outputs.labs` | Anti-Xa row whose value was "Held 48h prior to LP, DOAC hold protocol followed" and an abnormal summary about the hold (C9: management in a lab report, and an untreated hold reported as done). | FIXED: Coagulation panel deleted; Serology panel for RPR and HIV; `clinical_significance` null; pattern-only interpretation; abnormal summary empty. |
| B | major | `fallback_tool_outputs.ct` | Normal ventricles in the CT fallback (C18). | FIXED: canonical CT fallback (Evans about 0.39). |
| E | minor | `fallback_tool_outputs.echo` | "benign incidental finding"; no `echo_type`. | FIXED: findings stated (trace mitral regurgitation, normal LA); `echo_type: TTE`. |
| C | major | `ground_truth.assessment.required_recommendations` | Process musts; no DOAC plan (C11). | FIXED: referral (33% TUG, DESH, normal-pressure CSF); apixaban hold at least 72 h, restart no sooner than 6 h, no bridging, CHA2DS2-VASc 4 [ASRA_2018]; falls prevention (six falls, lives alone). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong triad/DESH requirement; AD prohibition copied (C12). | FIXED: canonical ventriculomegaly prohibition; DOAC prohibition; AF-attribution prohibition; LP-before-MRI kept; AD and ageing prohibitions removed (AD is low; ageing not raised). |
| C | major | `ground_truth.differential` | VCI "high" citing a "prior infarct" the case does not have (template carry-over); PD, AD, atrophy moderate (C13). | FIXED: VCI low (Fazekas 1, no infarcts or microbleeds); PD, AD (mother with AD named, MTA 2), atrophy and secondary hydrocephalus low. |
| C/E | major | `ground_truth.key_clinical_evidence` | Triad and DESH as requirements, "sensitivity 50-80%", tier sentence (C19). | FIXED: rebuilt from F1 to F7 with case figures. |
| A | minor | `ground_truth.action_criteria`, `.avoided_actions`, `.stop_rule`, `.sequence_constraints` | Labels equal to rationales, `NPH_pack`, fixed lab panels, generic waste rationales, allowance 0. | FIXED per plan 3.1 to 3.5; ECG, echo and monitoring waste rationales name her known, anticoagulated AF. |
| E | minor | `patient.chief_complaint`, `metadata` | Em dash; stale `vocab_gap`; counts; description with "WMH" red herring and "florid". | FIXED; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

A 77-year-old woman on apixaban for paroxysmal AF with 2.5 years of magnetic gait with freezing, urge leakage and executive decline; she lives alone and has fallen six times. The HPI no longer says she was admitted for an NPH work-up with a "DOAC hold protocol", the exam no longer records an irregular pulse that contradicted the sinus ECG, and CHA2DS2-VASc is corrected to 4. Pathway: brain MRI (required; Evans 0.39, both DESH components, callosal angle 74 degrees, temporal horns enlarged, flow void, Fazekas 1 without infarcts or microhaemorrhages, MTA 2), optional labs (normal; the anti-Xa "held 48 h" row is gone), baseline timed gait (required; TUG 30 s with cane, 10-m walk 24 s), optional MoCA (20/30 with cueing benefit), CSF tap test (required; opening pressure 14 cmH2O, normal content, 40 mL) and post-tap reassessment (recommended; TUG 20 s at 24 hours, 33% faster; MoCA 23). The apixaban drug check (which advised heparin bridging), the AF monitoring follow-up and the literature step were removed. Musts: neurosurgical referral, hold apixaban at least 72 hours before the tap and restart no sooner than 6 hours after without bridging (ASRA 2018), falls prevention. Prohibitions: tap before MRI, iNPH from ventriculomegaly alone, tap on active apixaban or bridging, attributing the decline to AF-related vascular disease. Differential all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[ASRA_2018]` and `[Nakajima_2021]` cited before the keys exist in the pack.
- Plan R4, R5, R7 as in NPH-S08.

## Open questions for Andrea (judgment calls you could not settle)

- Plan open question 3 (DOAC hold length) applies: the must uses the ASRA 2018 72-hour hold, as the plan decided.

## Verification

Checked against `plans/NPH.md` (sections 2 to 4 and the per-case entry), ROUND_POLICY and PATTERNS; NPH has no notes file, so there is no note id to account for. Read the whole final case (flattened, every field) and compared it with the pre-round version (`1fd43d22~1`). Verified: patient block free of Evans, callosal angle, DESH, NPH, hydrocephalus, tap, shunt, TUG and MoCA results; literature and drug-interaction outputs null with no such follow-ups; MoCA subscores sum to the total and match the exam orientation; TUG and 10-m percentages recomputed from the stored seconds and identical in the baseline report, the CSF report, the post-tap follow-up and the criteria; CSF/serum glucose ratio consistent with the lab glucose; Evans index identical in the MRI, CT fallback (within 0.01), criteria and key evidence; Fazekas grade matches the VCI likelihood (plan C13); musts, prohibitions and differential match plan section 4; discriminator values (`holter_24h`, `TTE`, CSF assay terms) are vocabulary terms; criteria order and tiers per plan 3.1, constraints per 3.4, stop rule per 3.5. Hijack check (MockServer through `NeuroBenchEnvironment`): cognitive screen then "baseline timed gait before tap test" returns the baseline (no `pre_post_comparison`); after the CSF call "post-tap reassessment at 24 hours" returns the follow-up; "repeat timed gait after lumbar puncture" re-serves the baseline (plan R5, already logged). `perfect_agent.py -v`, `case_io.py check` and `test_case_guards -k` pass after the changes below.

Found and changed:
- `ground_truth.action_criteria[action-post-tap-gait-reassessment].rationale`: template sentence (C19); rewritten for her cane, 40 mL tap and doorway freezing.
- `ground_truth.action_criteria[action-4-analyze-csf].citations`: `[Tisell_2011]` removed (not a tap-test source; ruling 8).
- Checked and correct: CHA2DS2-VASc 4 (age 77: 2, female: 1, hypertension: 1); apixaban 5 mg twice daily (no dose-reduction criteria met); ASRA 2018 hold of at least 72 hours, restart no sooner than 6 hours, no bridging; the regular pulse at examination agrees with the sinus ECG and Holter fallbacks.
- Nothing else found.

## Condition audit (NPH auditor, 24 Oct 2026)
- `analyze_csf {"special_tests": ["HSV_PCR"]}` added to `avoid-waste-generic-csf-assays`, as in the other 24 NPH cases (plan 3.3, PCR panels).
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
- Apixaban must, key evidence and prohibition: ASRA fifth edition (2025) supersedes the fourth (2018). Therapeutic apixaban is still held at least 72 hours before the tap, but the restart is now no sooner than 24 hours after the puncture (2018: 6 hours); citation `[ASRA_2018]` -> `[ASRA_2025] [ACCP_2022]` (ACCP 2022 for no heparin bridging).
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
