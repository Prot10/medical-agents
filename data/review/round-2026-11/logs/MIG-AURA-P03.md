# MIG-AURA-P03

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 32b921e6-bc71-4c8d-9c1d-21dcf1106356 | FIXED (class LIT, commit 393c547e) | Literature criterion and follow-up removed by the class; re-checked: no `search_medical_literature` string left. |
| 19136208-5828-49b1-813d-bea582508c35 | FIXED (plan D14) | `ground_truth.action_criteria[1]` (`action-4-analyze-brain-mri`, still required): label -> "Review the outside brain MRI (DWI/ADC, 3 days after the attack) to confirm the infarct and its location against the aura; repeat only if the images are inadequate"; rationale (removes the "report not available, so repeated" contradiction) and expected_evidence rewritten. `initial_tool_outputs.mri` is now the neuroradiology review of the imported day-3 outside study: `additional_observations`, `findings[0]` (DWI restricted, ADC low, FLAIR subtle hyperintense, T2 mildly hyperintense, T1 isointense, type `acute_cortical_infarct`) and `impression`. `contrast_used` stays null (no gadolinium content; MRI-CONTRAST decision 4). mri_probe: every order gets the case report. HPI line "The outside report is not with her today" kept (images obtained, report not). |
| e903ea4c-ce12-4f09-acc8-e65f16ccc745 | FIXED (plan D3) | `ground_truth.assessment.required_recommendations[3]`: topiramate clause -> canonical D3 must, adapted to this patient: copper IUD or LNG-IUS, with DMPA plus condoms named but flagged UKMEC 3 after stroke; pills and the etonogestrel implant not adequate (potential inducer at any dose). `initial_tool_outputs.drug_interactions.sumatriptan.warnings[2]` ("IUD or implant") corrected; `.interactions[4]` keeps the 200 mg/day evidence and adds the FSRH any-dose caution. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.assessment.required_recommendations[3] | The canonical D3 method list includes DMPA, which is UKMEC 3 after stroke (UKMEC: history of stroke, DMPA 3; Cu-IUD 1; LNG-IUS 2). For this post-stroke patient the must names the copper IUD or LNG-IUS and states the DMPA caution, consistent with `required_recommendations[4]`. | FIXED |
| B | major | ground_truth.action_criteria[1].rationale | Said the outside report was unavailable "so the study is repeated and compared" while the report said the images were imported; resolved by the review rewrite (same edit as note 19136208). | FIXED |
| - | - | label | "all secondary causes excluded" kept: four required studies (MRA, 30-day monitor, bubble echo) and the recommended antiphospholipid panel support it (plan D14). | - |
| C | minor | initial_tool_outputs.drug_interactions.sumatriptan.warnings[2] | Listed the DMPA injection for topiramate without its UKMEC 3 status after stroke; caveat added (verification pass 1). | FIXED |

## Changes
The MRI step is no longer a repeat scan. It is now the review of the outside MRI done 3 days after the attack (DWI/ADC), with a repeat only if the images are inadequate; it stays required because ICHD-3 1.4.3 needs an infarct shown in the aura territory. The stored MRI report is now the formal neuroradiology review of the imported outside study: a 4 mm focus of restricted diffusion with low ADC in the right occipital cortex (PCA territory), an acute cortical infarct at day 3, and no other infarct, haemorrhage, white matter disease or mass; the old 4-week follow-up scan with normalised diffusion is gone. The topiramate clause of the prevention must now requires a copper IUD or an LNG-IUS under the pregnancy prevention programme, notes that the DMPA injection (the other method unaffected by enzyme induction) is UKMEC 3 after her stroke, and says pills and the etonogestrel implant are not adequate because topiramate is a potential enzyme inducer at any dose (FSRH 2022). In the drug-check report, the topiramate warning no longer recommends the implant and the desogestrel interaction adds the FSRH any-dose caution. Literature step removed earlier by class LIT. Other criteria, tiers and the stop rule are unchanged.

## Verification
perfect_agent.py MIG-AURA-P03 -v: ok. test_case_guards (-k my six ids): 48 passed. case_io.py check: schema OK, synonym guard OK, no failure names this case (the only condition failure is test_no_review_process_text[MIG-AURA-P05], another worker's case). mri_probe: every order (plain, contrast, both orders, criterion) gets the case report.
Pass 1: 1 errors found
- initial_tool_outputs.drug_interactions.sumatriptan.warnings[2] offered the medroxyprogesterone acetate injection as an adequate topiramate contraceptive without the post-stroke caveat, while the must (REQ3) correctly says it is UKMEC 3 after stroke (UKMEC: history of stroke, DMPA category 3). Added "although the injection is UKMEC category 3 after stroke". Rulings file updated.
- Checked as correct: the MRI report is a review of the imported day-3 study (DWI restricted, ADC low), mri_probe shows every order gets the case report; the expected evidence and label match; the 'all secondary causes excluded' label is supported by the required work-up.
- Re-run after the fix: perfect_agent ok; test_case_guards -k 48 passed; case_io check: no failure names this case.
Pass 2: 0 errors found
- Checked: MRI criterion label, rationale and expected_evidence match the day-3 outside-study review (DWI restricted, ADC low); no 4-week or normalised-diffusion text left; HPI and MRI observations agree that the written report is absent; topiramate must and drug-check warnings[2] and interactions[4] agree (FSRH any dose, DMPA UKMEC 3 after stroke); mri_probe: every order gets the case report.
- Re-checked by pass 2: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed; case_io check: schema OK, synonym guard OK, no test failure names this case.
Pass 3: 0 errors found
- Checked: every note ruled and the ruling holds; diff read and final case read in full; no contradiction, leakage, template carry-over or em dash in new text found; no literature string left.
- Re-checked by pass 3: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed. mri_probe: every order gets the day-3 review report.
Pass 4: 0 errors found
- Checked: all three notes ruled and the rulings hold; MRI review timeline (day 3, DAPT started about day 3) agrees with the HPI and clinical assessment; topiramate must and drug report agree (FSRH any dose; DMPA UKMEC 3 after stroke); lab orders serve the antiphospholipid, ESR/CRP rows; final case read in full.
- Re-run by pass 4: perfect_agent.py -v ok; mri_probe: every order gets the day-3 review; test_case_guards -k (six ids) 48 passed; case_io check: no test failure names this case.
