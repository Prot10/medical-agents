# FND-M05

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 82744d6f | FIXED (class LIT) | No literature criterion or output left (checked). |
| eea4cf43 | FIXED (ACUTE) | ground_truth.action_criteria[1] action-4-analyze-brain-mri recommended to required, canonical rationale, citations [Espay_2018], [AHA_ASA_Stroke_2026], label 'for the acute focal deficit'; stop_rule.required_before_assessment = exam, MRI; exam criterion rationale (action_criteria[0]) and sequence_constraints[0].reason no longer say the examination decides whether imaging is needed; metadata.difficulty_rationale. mri_probe: stored study non-contrast with DWI. Labs stay recommended; ECG stays waste (no TLoC). |
| b9f0043f | FIXED (class LIT) | The literature criterion was removed by the class; none left. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.assessment.required_recommendations[4]; initial_tool_outputs.drug_interactions.general.warnings[0] | The must said 'continue hydroxychloroquine unchanged', but 400 mg daily at 74.1 kg is 5.4 mg/kg actual body weight, above the 5 mg/kg daily maximum the case's own drug check cites for retinal safety (AAO 2016, Marmor et al., Ophthalmology 2016;123:1386-1394). | FIXED: must now asks the rheumatologist for a dose review with the figure; the drug-check warning states the patient's mg/kg. |
| C | minor | initial_tool_outputs.labs.panels['Inflammatory markers'] (ESR) | ESR 22 abnormal with clinical_significance null. | FIXED: 'Mildly raised and non-specific; CRP, complement and anti-dsDNA are normal.' |
| B | minor | ground_truth.sequence_constraints[0].reason | Reason said the examination decides whether imaging has a question, which contradicts the required MRI. | FIXED: the examination defines the deficit the MRI must explain and does not delay it (constraint kept, soft). |
| A | minor | ground_truth.action_criteria; followup_outputs | Order did not follow 2.ORDER (labs before the now-required MRI; performance status before neuropsychology). | FIXED: exam, MRI, labs, drug check, neuropsychology; follow-ups neuropsychology then performance status. |
| E | minor | metadata.revision_reason | Outdated tiers. | FIXED: updated. |
| D | major | initial_tool_outputs.labs.panels['Inflammatory markers'] ESR clinical_significance | The new interpretation said 'CRP, complement and anti-dsDNA are normal': an ESR/CRP order (served alone, checked) revealed the complement and anti-dsDNA results of the recommended action-5-interpret-labs. | FIXED (verifier pass 1): 'Mildly raised and non-specific; CRP is normal.' |
| B | major | fallback_tool_outputs.ecg.rate | Template fallback ECG (served to the waste ECG order) gave 61/min against a vitals heart rate of 94. | FIXED (verifier pass 1): rate 92. |

## Changes
FND-M05 (29-year-old woman with quiescent SLE, sudden right-sided weakness and sensory loss for 48 hours, functional signs). As the physician ruled, the non-contrast brain MRI with DWI is now required and in the stop rule: a new focal deficit of 48 hours is imaged whatever the examination shows, because positive functional signs do not exclude a coexisting acute infarct (Espay 2018; AHA/ASA 2026). The examination criterion and the soft 'examination before MRI' constraint no longer say the examination decides whether imaging is needed. The antiphospholipid, complement and anti-dsDNA panel stays recommended, and the ECG stays waste (no loss of consciousness). The rheumatology must now asks for a hydroxychloroquine dose review, because 400 mg daily is 5.4 mg/kg of her 74.1 kg, above the 5 mg/kg maximum the drug check cites for retinal safety; the drug check states that figure. The mildly raised ESR carries a short interpretation. Stop rule: examination and MRI. Criteria and follow-ups are reordered to the clinical sequence. No literature step remains.

## Verification
Pass 1: 2 errors found
- ESR clinical_significance leaked the complement and anti-dsDNA results of the recommended serology criterion to an ESR/CRP order; now names CRP only.
- fallback ECG rate 61/min contradicted the vitals heart rate 94; set to 92.
- Re-checked after the fixes: perfect_agent.py passes, test_case_guards -k passes.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- None. Checked: MRI required with the ACUTE rationale and in the stop rule; soft constraint reason no longer delays imaging; hydroxychloroquine 400 mg / 74.1 kg = 5.4 mg/kg (AAO 2016 limit 5.0) consistent in must and drug check; an ESR/CRP order is served only its own panel with a trimmed interpretation (checked through the environment); fallback ECG rate 92 vs HR 94; mri_probe shows the plain DWI study; perfect_agent.py -v and test_case_guards -k pass.
Cosmetic (not counted): none.
Pass 3: 0 errors found
- None. Checked: ACUTE applied (MRI with DWI required, in the stop rule, AHA/ASA 2026 and Espay 2018); hydroxychloroquine 400 mg / 74.1 kg = 5.4 mg/kg against the AAO 5 mg/kg limit, consistent in must and drug check; ECG waste with no ECG criterion; fallback ECG rate 92 vs HR 94; mri_probe shows the plain DWI study.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case; the only FND failure is FND-RS02).
Cosmetic (not counted): none.
Pass 4: 0 errors found
- None. Checked: ACUTE (MRI with DWI required, canonical rationale, in the stop rule, soft exam-before-MRI reason no longer gates imaging); hydroxychloroquine 400 mg / 74.1 kg = 5.4 mg/kg consistent in must and drug check; ESR interpretation names only CRP; fallback ECG rate 92 vs HR 94; mri_probe shows the plain DWI study.
- For the lead (not counted, not changed, plan 3 keeps it): the ECG stays a waste avoided action although the case now requires stroke imaging on AHA/ASA 2026, which also recommends a baseline ECG in suspected acute ischemic stroke; P08 keeps its ECG optional. Consider optional rather than waste.
- Re-checked: perfect_agent.py -v passes, test_case_guards -k passes (case_io check: no failure names this case).
- For the lead (not counted, not changed): the neuropsychology battery numbers (MoCA 28/30, RAVLT z = -0.2, Trail B z = -0.4, TOMM 49/50) are identical in 23 FND cases, a condition-wide template carry-over outside this batch's plan.
Cosmetic (not counted): none.
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (29, nursing student): MoCA 29/30, RAVLT delayed recall z = 0.2, Trail Making B z = -0.3, TOMM trial 2 50/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-M05 passes.
Pass 5: 0 errors found
- None. Checked the condition-audit neuropsychology values in `followup_outputs[request_neuropsych_battery]`: MoCA, RAVLT, Trail Making B and TOMM agree between `quantitative_data` and the findings, all lie in the normal range (TOMM above the 45 cut-off) and match the impression 'within normal limits, performance validity passed'; no other field of the case cites them; GAD-7 and PHQ-9 labels match their bands (GAD-7 10-14 moderate, 15-21 severe; PHQ-9 5-9 mild, 10-14 moderate, 15-19 moderately severe) and the self-report sentence in findings and impression.
- Re-checked: perfect_agent.py -v passes; test_case_guards -k (all 8 FND pass-5 cases) 64 passed.
Cosmetic (not counted): none.
