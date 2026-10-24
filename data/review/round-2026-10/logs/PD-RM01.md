# PD-RM01
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plan PD (classes C1 to C23, per-case entry PD-RM01) and the July 2026 tool review (MRI required, ECG and EEG removed, labs targeted, autonomic and tilt testing removed). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `followup_outputs[0]`, `[2]` (literature), criterion `action-3-search-medical-literature` | Required literature criterion with an exact `query`; two follow-ups with unverifiable or misattributed papers (a Leigh and Zee "2015 textbook" chapter title, "Respondek 2014" with a generic title) and a summary that resolves the case ("Increasing levodopa dose ... can improve oculomotor symptoms") (C1). | FIXED: criterion and both follow-ups deleted; removed from the stop rule. |
| C | major | `followup_outputs[1]` (`request_drug_interaction_check_clonazepam_levodopa`), criterion `action-2-check-drug-interactions` | Required drug criterion with exact `drug` and `current_medications` strings; drug result filed as a follow-up (C2). | FIXED: follow-up deleted; one `initial_tool_outputs.drug_interactions.general` (clonazepam sedation, falls and saccade latency; sertraline canonical MAO-B sentence; amlodipine with levodopa; taper warning; melatonin alternative); criterion `{}`, `optional` (plan RM01), last; expected evidence worded so the leak test passes. |
| A | major | `ground_truth.action_criteria[action-1-analyze-brain-mri]` | Required `{"contrast": false, "protocol": "standard"}` (C5); rationale copied the label (C3). | FIXED: `analyze_brain_mri {}`; rationale adds the brainstem-lesion question for new diplopia; evidence restates the report. |
| B | major | `patient.history_present_illness` | Clonazepam "for restless sleep episodes" in the HPI against "REM sleep behavior disorder" in the medication list (plan C9). | FIXED: HPI states RBD diagnosed on a sleep study 5 years ago after punching and shouting in sleep, episodes now rare. |
| B | major | `initial_tool_outputs.mri.impression` | Impression said "no white matter lesion" while its own finding reports Fazekas 1 periventricular hyperintensities; "mild atherosclerotic changes of the intracranial vasculature" on a protocol without angiography (C12); em dashes in volumetrics. | FIXED: impression lists the Fazekas 1 change; the vascular line removed; volumetrics reworded; cortical finding given a type and location. |
| B | major | `followup_outputs` (no DaTscan, PSG or battery) | The library would answer a DaTscan as normal (an MDS absolute exclusion, C8), a PSG as normal (against PSG-diagnosed RBD on clonazepam, C9) and a battery with MoCA 28/30 (against the exam 27/30, C9). | FIXED: stored an asymmetric DaTscan (left posterior putamen more reduced, for right-predominant signs), a PSG on clonazepam (RSWA 38%, brief limb jerks, no complex behavior, AHI 3.8/h) and a battery (MoCA 27/30, mildly slow processing speed, GDS-15 8/15). No criterion for the PSG or the battery (RBD already diagnosed; cognition not a live question). |
| C | major | `ground_truth.assessment.required_recommendations` | Generic PD musts (C16); "Refer for advanced therapy candidacy (DBS, infusion) if fluctuations persist" although no fluctuations are described; "Document oculomotor exam" is a process step. | FIXED: five musts: keep PD (not PSP, with the oculomotor reasons); increase levodopa (plan doses) and reassess; orthoptic review with base-in prisms and ERM follow-up; clonazepam review (lowest dose or melatonin, taper); physiotherapy for near-falls and reassessment of worsening depression. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic list with pimavanserin. | FIXED: canonical D2-blocker prohibition; "do not revise to PSP on saccadic freezing alone"; anticholinergics in this older patient. |
| C | major | `ground_truth.differential` | PSP and wearing-off `moderate` (C13). | FIXED: all `low` with excluding features; added clonazepam saccade effect and microvascular cranial neuropathy or brainstem lesion (both raised by the case). |
| E | minor | `ground_truth.key_clinical_evidence` | Two "July 2026" sentences (C4); "Levodopa dose optimization should precede expensive functional imaging" (policy, not evidence); "serotonergic risk" overstated. | FIXED: five case items (8-year asymmetric PD on 300 mg/day; saccadic freezing with full range; convergence insufficiency and ERM; MRI; clonazepam and sertraline). |
| B | minor | `ground_truth.red_herrings` | Only the PSP anchor; the case's two other confounders (epiretinal membrane, clonazepam) named in metadata had no red herring. | FIXED: PSP red herring rewritten; ERM (`past_medical_history[5]`) and clonazepam (`medications[1]`) red herrings added. |
| A | minor | `ground_truth.avoided_actions` | Generic rationales; no DaTscan, autonomic or tilt guard (C8, plan 3.3). | FIXED: EEG, CSF, echo, monitoring rationales case-specific; DaTscan, autonomic testing and tilt table `waste` added. |
| B | minor | `ground_truth.stop_rule` | Literature and drug ids listed; `max_additional_actions` 0 (C20). | FIXED: MRI only; 2. No sequence constraint (DaTscan is waste). |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type` (C17). | FIXED: "TTE" with concrete findings. |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale`, revision fields | "upper-normal TSH" with no TSH in the case (C19); "3 required tool actions" text. | FIXED: TSH removed; rationale and revision fields rewritten; `last_revised` 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok (MRI `<- ?` is the dump-comparison label; the routing probe confirms the case MRI answers); case_io check clean; test_case_guards pass; routing: DaTscan, PSG, battery and drug (levodopa, rasagiline, none) from the case; MIBG, FDG, amyloid, orthostatic and labs from the library (consistent: no orthostatic symptoms, no lab question). Pre-existing em dashes in unedited exam sentences left. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The HPI now gives clonazepam's real indication, RBD diagnosed on a sleep study 5 years ago, in line with the medication list. The MRI impression reports its own Fazekas 1 finding and no longer mentions intracranial atherosclerosis on a study without angiography. Literature and the drug follow-up are gone; the medication review is optional and names clonazepam (sedation, falls, slower saccades), sertraline with a future MAO-B inhibitor and amlodipine with levodopa. A DaTscan (asymmetric, ordering it is waste), a PSG on clonazepam and a neuropsychological battery consistent with MoCA 27/30 were stored so that no library default contradicts the case. Policy: MRI required, medication review optional. Musts: keep PD (full vertical range, preserved optokinetic responses, normal midbrain), increase levodopa from 300 mg/day and reassess, orthoptic review of the convergence insufficiency with base-in prisms, review clonazepam, physiotherapy for near-falls and reassessment of her depression. PSP and wearing-off are low; the epiretinal membrane and clonazepam are now explicit red herrings.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` used per the plan; not yet in the PD pack.
- Plan R5: library DaTscan, PSG and neuropsychological defaults contradict this case; it now stores its own reports.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the checkpoint diff (b8be2153) and the whole final case. Checked: HPI clonazepam indication now RBD, matching the medication list; MoCA 27 in exam and stored battery; DaTscan deficit left-predominant for right-predominant signs; PSG on clonazepam coherent (RSWA persists, behaviours suppressed); MRI impression lists its own Fazekas 1 finding, Evans 0.28; levodopa increase must uses real tablet strengths; differential all `low` with the oculomotor exam as excluding evidence; routing serves the case DaTscan, PSG, battery and drug output.
Found and fixed:
- B minor, `ground_truth.differential[1].key_features` (wearing-off): "the episodes are not tied to the timing of her doses" asserted a history the HPI does not give. Now "No dose-related pattern is described, and the motor signs worsened steadily on an unchanged low dose".
No other defect found. After the edit: perfect_agent ok; case_io check clean for PD-RM01; test_case_guards pass; discriminator_defects empty.
