# NPH-M05
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `nph`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for NPH. The case was corrected against plan NPH (classes C1 to C20) and the July 2026 tool review. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, criterion `action-1-search-medical-literature` | Recommended literature criterion with a leaking output (C1). | FIXED: deleted; literature outputs null. |
| C | minor | `followup_outputs[0]` (`request_drug_interactions_periop`) | Perioperative levodopa management as a tool result (C2). | FIXED: deleted; drug outputs null; canonical levodopa must added (same medication state for pre- and post-tap measures). |
| D | major | `patient.chief_complaint`, `patient.history_present_illness` | "Neurologist questioning whether NPH is superimposed", "admitted for NPH evaluation", Evans 0.34 and callosal angle 84 "meeting both NPH imaging criteria", "tap trial" (C3). | FIXED: complaint names the symptoms in a man with PD (the PD anchor kept, plan C3); HPI says the outside MRI was reported as showing enlarged ventricles (images not available) and the referral asks whether a second process contributes. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 38 s and MoCA 20/30 with its domains in the exam (C4); motor signs repeated in mental status. | FIXED: qualitative gait; mental status "slowed responses ... formal cognitive screening reported separately"; tremor stays in `motor`. |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Pre-tap call returned the post-tap result and a verdict (C6). | FIXED: baseline only, with the medication state stated (ON, about one hour after the morning dose): TUG 38 s, 10-metre walk 29 s in 38 steps (new, the case had no walk time), turn 9 steps, MoCA 20/30. |
| A | major | `followup_outputs` | No post-tap reassessment, no cognitive screen; no case DaTscan, so the library would return a normal DaTscan in a man with PD (C6, C10). | FIXED: `[0]` cognitive screen (MoCA 20/30 itemised; recall 1/5 free, 4/5 cued); `[1]` post-tap reassessment in the same ON state (TUG 34 s at 2 h, 31 s at 24 h, 10-metre walk 25 s, MoCA 21; identical to CSF); `[2]` DaTscan (`request_datscan`, modality `DaTscan`): reduced putaminal binding, more marked on the left (contralateral to the right-hand tremor). |
| D | major | `initial_tool_outputs.mri` | "Reduced neuromelanin signal ... consistent with Parkinson's" names the disease from imaging (C8); no technique, temporal horns, hippocampi, aqueduct, Fazekas grade; no statement on atypical-parkinsonism signs (C7). | FIXED: SWI finding only ("loss of the dorsolateral nigral hyperintensity (swallow-tail sign) bilaterally"); technique; Evans 0.34; callosal angle 84; temporal horns out of proportion to the hippocampi (MTA 1); tight convexity sulci without Sylvian enlargement, DESH incomplete (plan: no DESH in M05, the report never described Sylvian enlargement); Fazekas 1; patent aqueduct; midbrain and pons normal, no pontine or putaminal signal change; descriptive impression. |
| D | major | `initial_tool_outputs.csf` | Prose with "improved"; no 10-metre walk; protein 46 mg/dL above the usual range (C5, F3). | FIXED: canonical interpretation including the ON state (18% at 24 h; 10-metre walk 29 to 25 s; MoCA 20 to 21); protein 43 mg/dL; "Lymphocytes". |
| C | minor | `initial_tool_outputs.labs` | HIV under "Baseline workup" (C9). | FIXED: `Serology`; `clinical_significance` null; pattern interpretation naming only the analytes actually reported. |
| C | major | `ground_truth.action_criteria` | As M01. | FIXED: MRI, baseline gait (label and rationale require a stated medication state), CSF required; post-tap recommended; labs and cognitive screen optional. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule`, `.avoided_actions` | As M01; advanced imaging unguarded. | FIXED: canonical constraints and stop rule; waste entries added, the advanced-imaging rationale saying the PD is already clinically established. |
| C | major | `ground_truth.assessment.required_recommendations` | Process musts (C11). | FIXED: referral on the 18% ON-state response with the supportive MRI; copathology counselling (gait and incontinence benefit, PD treatment continues); levodopa must; falls prevention (freezing, festination, retropulsion). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong DESH/triad prohibition; AD prohibition copied (C12). | FIXED: LP-before-MRI; canonical ventriculomegaly-alone; do not withhold referral because of PD; do not attribute the decline to PD progression alone; normal ageing. |
| C | major | `ground_truth.differential` | VCI and "PD progression" `high`, AD and atrophy `moderate`; PD entry argued from DESH the MRI lacked (C13). | FIXED: PD progression `low` (the label names the copathology); new "Atypical parkinsonism (MSA, PSP)" `low`, because the new incontinence raises MSA (good levodopa response, asymmetric rest tremor, full eye movements, normal midbrain, pons and putamina); VCI (Fazekas 1), AD, atrophy and secondary hydrocephalus `low`. |
| C | major | `ground_truth.key_clinical_evidence` | Template items. | FIXED: five case items, including F8 copathology. |
| B | minor | `ground_truth.red_herrings[0]` | Cited DESH; data_point not the PMH text. | FIXED. |
| B | minor | `fallback_tool_outputs.ct`, `.echo` | Normal-ventricle CT; no `echo_type` (C18). | FIXED. |
| E | minor | `metadata` | Variant description said "extended drainage trial needed" (none in the case); stale gap and counts. | FIXED. |
| - | check | plan 3.6 | perfect_agent ok; guards pass; hijack probe as M01; DaTscan order returns the case report. Patient grep clean; one pre-existing em dash in the unedited `additional` exam line left. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The patient block keeps the Parkinson's diagnosis (the anchor) but no longer names NPH, quotes the outside Evans index or callosal angle, or gives the TUG or MoCA. The MRI reports the SWI swallow-tail loss without naming a disease, Evans 0.34, an acute callosal angle of 84 degrees, enlarged temporal horns with MTA 1, incomplete DESH, Fazekas 1, a patent aqueduct and a normal midbrain, pons and putamina. Gait is measured in a stated ON state: baseline TUG 38 s and 10-metre walk 29 s (new value); after the tap 34 s at 2 hours and 31 s at 24 hours (18%), 10-metre walk 25 s, with tremor and bradykinesia unchanged, in both the CSF report and a separate post-tap reassessment. An authored abnormal DaTscan answers any DaTscan order (waste, but no longer contradicted by a library normal). Literature and drug-check steps are gone. Musts: shunt referral on the tap response, copathology counselling, continued levodopa with matched medication state, falls prevention. Atypical parkinsonism was added as a low alternative because of the new incontinence.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[Nakajima_2021]` not yet in the NPH criteria pack.
- Plan R4: post-tap criterion shares the baseline pattern.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case beyond plan Q1 (referral with counselling in copathology).

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the whole final case and its diff against fa1d22e6.
- Checked: the MRI names no disease (SWI swallow-tail finding only, plan C8); DESH stated incomplete and no DESH argument remains in the differential, key evidence or musts; the authored DaTscan (left-predominant putaminal loss, contralateral to the right-hand tremor) is served for a DaTscan order (probe) while staying waste; the levodopa must, copathology counselling and "do not withhold referral because of PD" prohibition are present; medication state is stated as ON for baseline and both post-tap measures in every report. Figures identical (TUG 38 to 34 s = 11%, to 31 s = 18%; 10-metre walk 29 to 25 s = 14%); MoCA items sum to 20 (attention 1+0+0+2 = 3). Atypical-parkinsonism entry agrees with the MRI (normal midbrain, pons, putamina) and cranial nerves. MockServer probe: no leak.
- Found: nothing that needed a change. Noted only: the labs omit platelets and glucose (optional criterion, nothing in the case quotes them).
- No edits. perfect_agent -v ok, case_io check clean for the case, test_case_guards pass.
