# NPH-S03
Reviewer status: R1 not reviewed, R2 not reviewed (NPH has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was never annotated; the only physician input is the July 2026 tool review (`condition_tool_guidance.yaml` key `nph`), applied through plan NPH sections 2 to 4. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs[request_literature_iNPH_outcomes]`, `action_criteria[action-1-search-medical-literature]` | Literature as a clinical step, with invented thresholds ("Evans >0.38 and callosal angle <75 degrees ... PPV >85%") (C1, ruling 5). | FIXED: criterion and follow-up deleted; literature initial and fallback null. |
| B | minor | `patient.clinical_history.past_medical_history`, `patient.history_present_illness` | "Diet-controlled" diabetes while metformin is listed (C9). | FIXED: "Type 2 diabetes mellitus on metformin" in PMH and HPI; HbA1c 6.4% kept. |
| D | major | `patient.history_present_illness` | "presented for inpatient NPH evaluation", outside CT "noting hydrocephalus", "admitted for comprehensive NPH workup including MRI, lumbar puncture, and tap trial" (C3). | FIXED: admitted for progressive gait difficulty; canonical outside-CT and referral sentences; em dashes removed. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 32 s, 10-m walk 26 s and MoCA 20/30 with subscores in the exam (C4). | FIXED: qualitative; numbers in the gait report and the cognitive-screen follow-up. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline report held the post-tap result, the engineering sentence and `criteria_met` keys (C6). | FIXED: baseline only (TUG 32 s and 10-m walk 26 s in 64 steps with rollator, turn 10 steps, MoCA 20/30; non-antalgic gait noted for the knee red herring); post-tap figures in follow-up `request_post_reassessment`. Step count chosen to match the documented 15 cm step length. |
| D | major | `initial_tool_outputs.csf.interpretation` | "Positive tap trial" (C5). | FIXED: C5 canonical form (42 mL; TUG 32 to 23 s at 2 h, 21 s at 24 h, 34%; 10-m 26 to 17 s; MoCA 20 to 23). |
| D | major | `initial_tool_outputs.mri` | "transependymal" and "hyperdynamic" interpretation, no Fazekas grade, temporal horns, hippocampi, fourth ventricle or technique (C7). | FIXED: rebuilt with the C7 elements (Evans 0.40, DESH, callosal angle 70, temporal horns with MTA 2, Fazekas 1, aqueduct flow void, mildly enlarged fourth ventricle, no obstruction); canonical impression. |
| C | minor | `initial_tool_outputs.labs` | HIV "Baseline workup" row; HbA1c reference with a prediabetes band; `abnormal_values_summary` interpretive ("known T2DM", "diet-controlled") (C9). | FIXED: Serology panel; HbA1c reference "<5.7", flagged high; factual summary and pattern interpretation; criterion `interpret_labs {}` optional. |
| C | major | `ground_truth.assessment` | Process musts; wrong DESH-plus-triad prohibition; AD prohibition where AD is not in question (C11, C12). | FIXED: musts are referral (34%) and falls prevention (four falls, lives alone); prohibitions MRI-first, canonical, knee OA or neuropathy attribution, ageing/deconditioning. |
| C | minor | `ground_truth.red_herrings` | Neuropathy red herring said "long-standing" diabetes (not in the history) and pointed at the PMH; the knee osteoarthritis red herring named in `difficulty_variant_description` was missing. | FIXED: neuropathy red herring kept (the exam documents mild distal vibration loss, C20) and pointed at the sensory exam; knee OA red herring added (HPI). |
| C | major | `ground_truth.differential` | VCI "high", PD, AD and ex vacuo "moderate" after DESH and a 34% tap response; the neuropathy mimic raised by the case absent (C13, ruling 7). | FIXED: all low with case data; diabetic neuropathy added as low. |
| C | minor | `ground_truth.key_clinical_evidence` | Tier sentence; "sensitivity only 50-80%". | FIXED: four pearls (F1, F2, F4, the two mimics). |
| C | minor | `ground_truth.action_criteria`, `avoided_actions`, `sequence_constraints`, `stop_rule` | Label equals rationale, "NPH_pack"; no post-tap or cognitive criteria; waste entries missing; allowance 0. | FIXED: plan 3.1 order and tiers; waste entries added; canonical constraints; allowance 1. |
| B | minor | `fallback_tool_outputs.ct`, `.ecg`, `.echo`, `.drug_interactions` | CT "without acute abnormality" against ventriculomegaly; ECG `axis: normal` while its finding is borderline left axis deviation, and "benign incidental finding"; echo without `echo_type`; placeholder drug check (C18, C2). | FIXED: CT shows enlarged ventricles (Evans about 0.39); ECG axis "borderline left (-25 degrees)" with a factual interpretation; `echo_type: TTE`; drug check null. |
| E | minor | `metadata` | Stale phase-contrast note; removed-tool counts; em dash. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The patient block no longer says "NPH evaluation" or "hydrocephalus" or announces a tap trial; the diabetes is now on metformin, as the medication list says, and the exam is qualitative. The literature step, with its invented Evans and callosal-angle thresholds, is gone. The pathway is MRI, optional labs (glucose 108, HbA1c 6.4%), baseline timed gait with a rollator (TUG 32 s, 10-m walk 26 s in 64 steps, turn 10 steps, not antalgic), optional MoCA (20/30, dysexecutive, recall 1/5 rising to 3/5 with cues), the tap test (opening pressure 13 cmH2O, normal CSF, 42 mL; TUG 23 s at 2 h and 21 s at 24 h, 34%; 10-m walk 17 s; MoCA 23) and a recommended post-tap reassessment. The MRI reports Evans 0.40, DESH, callosal angle 70 degrees, temporal horns out of proportion to MTA 2 hippocampi, Fazekas 1 and a patent aqueduct. Musts are shunt referral and falls prevention (four falls, lives alone). Knee osteoarthritis and diabetic neuropathy are now both red herrings, the neuropathy also a low differential entry, and a prohibition guards against attributing the gait to either.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation key `[Nakajima_2021]` used per plan 1.1 (plan CENTRAL R2).
- Post-tap criterion shares the baseline pattern (plan CENTRAL R4); hijack check as in S01.

## Open questions for Andrea (judgment calls you could not settle)

- None. (Decided here: the exam's "mild symmetric hip flexor weakness (4+/5)" is not an iNPH sign but is plausible from knee osteoarthritis and deconditioning at 78; left unchanged, as no field relies on it.)
