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
