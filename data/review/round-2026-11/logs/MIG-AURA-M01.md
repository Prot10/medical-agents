# MIG-AURA-M01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 2a94bbb7-ea1c-4ed2-96bf-9667e37fb65f | FIXED (class LIT, commit 393c547e) | Nothing left to remove: no search_medical_literature criterion, follow-up or stored output in the case; fallback_tool_outputs.literature_search is null. |
| faa8bb3e-1cbf-4bed-a876-cadba921131a | FIXED (plan D4) | Deleted ground_truth.assessment.prohibited_recommendations[1] ("Do not start antiplatelet or anticoagulant therapy for presumed TIA ..."). Rewrote required_recommendations[1] as the conditional must (aura features; MRI excludes infarct, not TIA; antiplatelet only if a real suspicion of ischaemia remains, then TIA pathway). Added optional criterion ground_truth.action_criteria[2] `action-vessel-imaging-optional` (order_advanced_imaging MR_angiography or carotid_duplex; answered by the library normal report; no avoided action matches it). metadata.difficulty_description "first episode requires TIA exclusion" -> "first episode: TIA must be considered" (D17). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | metadata.difficulty_description | "first episode requires TIA exclusion" implied that TIA can be excluded by testing | FIXED (reworded, D17) |
| B | minor | patient.clinical_history.medications | HPI says she took ibuprofen for the attack, but ibuprofen is not in the medication list (the drug-check report mentions it as an as-needed analgesic) | FLAGGED (one-off use during the attack; not a regular medicine, no change) |

PATTERNS check: no literature step, no leakage of MRI results into the patient block, no template carry-over, differential already states that a normal DWI does not exclude TIA (D17), pathway order (history, MRI, vessel imaging if needed, drug check) is clinical.

## Changes
The antiplatelet question is no longer closed by a prohibition. The case now asks the agent to tell the patient and GP that the episode has the features of migraine aura (positive sensory symptom spreading over 10-12 minutes, headache within 15 minutes, normal examination), to state that the MRI excludes an infarct but cannot exclude TIA, and to give antiplatelet therapy only if the clinical assessment leaves a real suspicion of ischaemia (then the TIA pathway). Vessel imaging (MR angiography or carotid duplex) is now an optional, credited step: acceptable when suspicion remains, not required. The difficulty description says TIA must be considered rather than excluded. Nothing else changed; the label, the combined-pill must and the work-up tiers are as before. At verification, the MRI criterion's rationale was corrected to say MRI excludes infarction and structural causes, not TIA.

## Verification
perfect_agent.py -v: ok (every required and recommended criterion served by its own report). test_case_guards.py -k <case>: pass. case_io.py check: schema OK, synonym guard OK, no failure names this case (one unrelated failure names MIG-AURA-P05). DiagnosisCriterion.matches re-checked on a plain correct answer after any label edit: True; TIA / mimic answers: False.
Pass 1: 2 errors found
- ground_truth.action_criteria[1].rationale (action-4-analyze-brain-mri) still said "MRI excludes a structural or ischaemic cause", which implies imaging excludes TIA (plan D4 rule 1, the point of note faa8bb3e). Changed to "MRI excludes infarction and structural causes (not TIA)".
- ground_truth.red_herrings[0].intended_effect said the TIA referral "may lead to antiplatelet therapy or a vascular work-up", presenting vessel imaging as the error while the new optional criterion action-vessel-imaging-optional credits it when suspicion remains. Changed to "a routine vascular work-up without a real suspicion of ischaemia".
Cosmetic (not counted): metadata.difficulty_description "first episode: TIA must be considered" (double colon) -> "first episode, so TIA must be considered".
Re-run after the fixes: perfect_agent.py ok; test_case_guards -k MIG-AURA-M01 pass; case_io.py check: no failure names this case.
Pass 2: 0 errors found
- Checked: D4 conditional must, deletion of the TIA prohibition, optional vessel-imaging criterion (MR_angiography and carotid_duplex both served by the library normal report; no avoided action matches them; fallback advanced_imaging null), D17 wording, pass-1 fixes to the MRI rationale and red herring. R2 file for this case is empty. Every note id has a ruling; no literature string left (fallback literature_search null); no new em dash; no answer leakage in the patient block or drug-check outputs.
Cosmetic (not counted): none.
Re-run at pass 2: perfect_agent.py -v ok (each required and recommended criterion receives the report carrying its expected evidence); test_case_guards -k for MIG-AURA-M01..M06: 48 passed; case_io.py check: schema OK, synonym guard OK, no failure names this case; mri_probe: no gadolinium text, no MRI pair needed; DiagnosisCriterion.matches: correct answer True, TIA / mimic False.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Checked the only change after the last clean pass: metadata.case_body_concerns deletion (condition audit) checked against git diff 06b74446: only the generation-pipeline line was removed, the field is [] and no other field changed with it.
- perfect_agent.py -v ok; test_case_guards -k (M01..M08) 64 passed.
Cosmetic (not counted): none.
