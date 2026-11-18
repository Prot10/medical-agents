# MIG-AURA-M05

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 2 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| fca3be91-d32a-4e88-a04b-2a0f0cdc9e64 | FIXED (class LIT, commit 393c547e) | Nothing left to remove: no search_medical_literature criterion, follow-up or stored output; fallback literature_search null. |
| 8763368b-d059-4ea3-b28d-41af877106cd | FIXED (class LIT, commit 393c547e) | As above (both literature follow-ups were removed by the class change). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.assessment.prohibited_recommendations[0] | "Do not start antiplatelet ... for presumed TIA ... and imaging shows no infarct" rested the decision partly on imaging (class TIA-CERT of notes faa8bb3e/30f0b036/b37e0b4d, plan D4.3) | FIXED (reworded: not on the TIA label alone; stereotyped features of her 20-year aura; a normal MRI excludes infarction, not TIA) |
| C | major | ground_truth.assessment.required_recommendations[0] | "history, examination and MRI show no sign of TIA" claims imaging excludes TIA (D4.4) | FIXED ("the MRI shows no infarct or structural disease, and the TIA question is answered by the identical features of her lifelong aura") |
| C | minor | ground_truth.differential[0].key_features | "MRI shows no infarct." without the DWI limit stated in the other cases | FIXED (added "(a normal DWI does not exclude TIA; the distinction is clinical)") |
| C | minor | ground_truth.action_criteria | No route for a justified cerebrovascular evaluation in a pattern change at 48 (D4.5) | FIXED (new optional `action-vessel-imaging-optional`, ground_truth.action_criteria[2]: MR_angiography or carotid_duplex, library normal; no avoided action matches) |
| B | minor | patient.hpi | "approximately twice monthly for the past year" next to "12-18 months" and "2-3 per month" | FLAGGED (approximate patient wording, compatible; no change) |

PATTERNS check: HRT drug check and musts agree with NICE NG23; GCA entry fits a 48-year-old; no leakage; pathway order is clinical.

## Changes
The antithrombotic wording now rests on the clinical features rather than on imaging. The prohibition reads: do not start antiplatelet or anticoagulant therapy on the TIA label alone, because the stereotyped attacks have the features of her 20-year aura (positive visual symptoms spreading over 20-30 minutes) and a normal MRI excludes infarction, not TIA. The explanation must now says the MRI shows no infarct or structural disease and that the TIA question is answered by the identical features of her lifelong aura (it previously said the MRI showed no sign of TIA). The TIA entry of the differential states that a normal DWI does not exclude TIA. A new optional criterion credits vessel imaging (MR angiography or carotid duplex) if residual suspicion remains, without requiring it. The label, HRT and contraception musts are unchanged.

## Verification
perfect_agent.py -v: ok (every required and recommended criterion served by its own report). test_case_guards.py -k <case>: pass. case_io.py check: schema OK, synonym guard OK, no failure names this case (one unrelated failure names MIG-AURA-P05). DiagnosisCriterion.matches re-checked on a plain correct answer after any label edit: True; TIA / mimic answers: False.
Pass 1: 1 error found
- ground_truth.red_herrings[0].intended_effect said the worry about TIA "may lead to antiplatelet therapy or a vascular work-up", presenting vessel imaging as the error while the new optional criterion action-vessel-imaging-optional credits it when suspicion remains (D4.5). Changed to "a routine vascular work-up without a real suspicion of ischaemia".
Cosmetic (not counted): none.
Re-run after the fix: perfect_agent.py ok; test_case_guards -k MIG-AURA-M05 pass; case_io.py check: no failure names this case.
Pass 2: 0 errors found
- Checked: D4.3 reworded prohibition, REQ0 wording, differential DWI caveat, optional vessel-imaging criterion (library normal reports; no avoided action matches), pass-1 red-herring fix; GCA entry fits age 48. Every note id has a ruling; no literature string left (fallback literature_search null); no new em dash; no answer leakage in the patient block or drug-check outputs.
Cosmetic (not counted): none.
Re-run at pass 2: perfect_agent.py -v ok (each required and recommended criterion receives the report carrying its expected evidence); test_case_guards -k for MIG-AURA-M01..M06: 48 passed; case_io.py check: schema OK, synonym guard OK, no failure names this case; mri_probe: no gadolinium text, no MRI pair needed; DiagnosisCriterion.matches: correct answer True, TIA / mimic False.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Checked the only change after the last clean pass: metadata.case_body_concerns deletion (condition audit) checked against git diff 06b74446: only the generation-pipeline line was removed, the field is [] and no other field changed with it.
- perfect_agent.py -v ok; test_case_guards -k (M01..M08) 64 passed.
Cosmetic (not counted): none.
