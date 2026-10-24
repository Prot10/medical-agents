# NPH-M06
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `nph`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for NPH. The case was corrected against plan NPH (classes C1 to C20) and the July 2026 tool review. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | criterion `action-1-search-medical-literature`, `followup_outputs[1]` (`request_literature_secondary_nph`) | Recommended literature criterion; a literature follow-up with uncited claims ("70-80% improvement", "1-5% of cases") (C1, ruling 5). | FIXED: criterion and follow-up deleted; literature outputs null. |
| C | major | `followup_outputs[0]` (`request_drug_interactions_shunt_anticoagulation`) | Wrong DOAC advice as a tool result (48 h hold, "bridging anticoagulation", restart 24-48 h) (C2, F7). | FIXED: deleted; drug outputs null; rivaroxaban must per ASRA 2018 (at least 72 h, restart no sooner than 6 h, no bridging). |
| C | major | `initial_tool_outputs.labs.panels.Coagulation` | Anti-Xa "row" whose value was the management text "Hold rivaroxaban 24h prior to LP" (C9). | FIXED: panel removed; HIV moved to `Serology`; `clinical_significance` null; interpretation states the pattern (haemoglobin 13.4 g/dL just below range). |
| B | major | `patient.clinical_history.past_medical_history[2]` | "Atrial fibrillation (CHA2DS2-VASc 4)": the case supports only hypertension (1) and age 65-74 (1), i.e. 2 (no heart failure, diabetes, stroke or TIA, vascular disease; atorvastatin is for primary prevention). Plan C18 also asks for "paroxysmal" so the sinus ECG and Holter fallbacks stay consistent. | FIXED: "Atrial fibrillation (paroxysmal, CHA2DS2-VASc 2)"; the key evidence cites 2. Anticoagulation remains indicated in a man with a score of 2. |
| D | major | `patient.history_present_illness` | "Admitted for NPH evaluation", "Evans index on current CT is 0.36", "the neurosurgeon suspects secondary NPH", "admitted for tap trial", "Anticoagulation management is a safety concern for LP" (diagnosis and policy hints, C3). | FIXED: admitted for a gait and cognitive decline; surveillance CT last month showed enlarged ventricles not present at 6 months (kept, it documents change; images not available); the diagnostic and anticoagulation sentences removed. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 26 s, 10-metre walk 20 s, MoCA 22/30, recall 3/5 in the exam (C4). | FIXED: qualitative gait with the walker; mental status with slowed processing and "formal cognitive screening reported separately". |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Pre-tap call returned the post-tap result and a verdict (C6). | FIXED: baseline only (TUG 26 s with walker, 10-metre walk 20 s in 28 steps, turn 7 steps, MoCA 22/30). |
| A | major | `followup_outputs` | No post-tap reassessment, no cognitive screen (C6). | FIXED: `[0]` cognitive screen (MoCA 22/30 itemised); `[1]` post-tap reassessment (TUG 20 s at 2 h, 18 s at 24 h, 10-metre walk 14.5 s, MoCA 24; identical to CSF). |
| C | major | `initial_tool_outputs.mri` | No technique, temporal horns, hippocampi, aqueduct; no supportive feature beyond the callosal angle; "Evans index 0.36 - significant" (C7). | FIXED: technique; Evans 0.36; callosal angle 78; temporal horns out of proportion to the hippocampi (MTA 1); tight convexity sulci, DESH incomplete (plan); burr holes with hemosiderin along the tracts and "No residual or recurrent subdural collection"; Fazekas 1; patent aqueduct with flow void; descriptive impression. |
| C | minor | `initial_tool_outputs.csf.appearance`, `.protein` | "Slightly xanthochromic (residual post-operative)" 14 months after evacuation of collections outside the arachnoid is not plausible; protein 56 mg/dL contradicts the normal content the policy relies on (F3). | FIXED: "Clear, colourless"; protein 41 mg/dL; RBC with unit. |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | Prose with "improved" (C5). | FIXED: canonical interpretation (45 mL; 31% at 24 h; 10-metre walk 20 to 14.5 s; MoCA 22 to 24). |
| C | major | `ground_truth.action_criteria` | As M01; MRI label did not name the recurrent subdural question. | FIXED: MRI required (label and rationale name the recurrent collection), labs optional (renal function for the rivaroxaban hold), baseline gait required, cognitive screen optional, CSF required, post-tap recommended. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule`, `.avoided_actions` | As M01. | FIXED: canonical constraints, stop rule three ids and max 1; three waste entries; ECG, echo and monitoring rationales cite the known anticoagulated AF. |
| C | major | `ground_truth.assessment.required_recommendations` | Process musts, plus "Inspect MRI for residual or recurrent subdural collection before LP" (a process step the hard constraint and the prohibition now carry) (C11). | FIXED: referral naming the subdural antecedent, with a programmable valve because of the risk of recurrent collection with overdrainage, on the 31% response; rivaroxaban must; falls prevention (two falls, walker). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong DESH/triad prohibition; AD prohibition copied (C12). | FIXED: LP-before-MRI now names the recurrent subdural collection; DOAC prohibition; "do not label the hydrocephalus idiopathic" (F6); normal ageing. |
| C | major | `ground_truth.differential` | The "post-traumatic / post-SAH / post-meningitic" entry was the case's own diagnosis at `moderate`; VCI `high` citing a "prior infarct" the patient never had; PD, AD, atrophy `moderate`; recurrent subdural haematoma, the first mimic in this patient, absent (C13, ruling 7). | FIXED: the generic secondary entry replaced by "Idiopathic normal pressure hydrocephalus" `low` (an antecedent exists, plan M06); "Recurrent chronic subdural haematoma" (I62.03) `low` (MRI shows none); VCI `low` (Fazekas 1, no infarct); PD, AD, atrophy `low`. |
| C | major | `ground_truth.key_clinical_evidence` | Template items. | FIXED: six case items (secondary NPH per F6, MRI, tap, Marmarou, programmable valve, rivaroxaban hold). |
| B | minor | `ground_truth.red_herrings` | None, although the subdural history invites a recurrence diagnosis. | FIXED: one red herring on the PMH subdural entry, interpreted with the MRI and the tap. |
| B | minor | `fallback_tool_outputs.ct` | Normal CT without burr holes (C18). | FIXED: ventriculomegaly (Evans about 0.36), bilateral burr holes, no subdural collection. ECG and Holter sinus rhythm kept (consistent with paroxysmal AF); echo `echo_type` "TTE". |
| E | minor | `metadata` | Stale gap and counts. | FIXED. |
| - | check | plan 3.6 | perfect_agent ok; guards pass; hijack probe as M01; CT fallback consistent; patient grep clean. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The patient block no longer calls the problem secondary NPH, quotes the Evans index or hints at the anticoagulation plan; it keeps the surveillance CT history (ventricles enlarged after the 6-month post-operative CT). Atrial fibrillation is now paroxysmal with a CHA2DS2-VASc of 2, the score the case supports (it said 4). The MRI reports Evans 0.36, an acute callosal angle of 78 degrees, enlarged temporal horns, the burr holes, no residual or recurrent subdural collection, Fazekas 1 and a patent aqueduct. CSF is clear (no implausible xanthochromia) with protein 41 mg/dL. Baseline gait (TUG 26 s with walker, 10-metre walk 20 s, MoCA 22/30) is separate from the post-tap reassessment and CSF report (TUG 20 s at 2 hours, 18 s at 24 hours, 31%; 10-metre walk 14.5 s; MoCA 24). The literature follow-up, the drug check with heparin "bridging" and the anti-Xa management row are gone. Musts: shunt referral naming the subdural antecedent with a programmable valve, rivaroxaban held at least 72 hours without bridging, falls prevention. The differential now lists iNPH (low, an antecedent exists) and recurrent subdural haematoma (low, MRI) instead of the case's own diagnosis.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[Nakajima_2021]` and `[ASRA_2018]` not yet in the NPH criteria pack.
- Plan R4: post-tap criterion shares the baseline pattern.
- Plan section 4 (M06) says to write "CHA2DS2-VASc 4"; the case data give 2. The lead may want to correct the plan text so no other worker copies 4.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q3 (72 h ASRA hold) applies.
