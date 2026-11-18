# FEPI-TEMP-RP02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-4-search-medical-literature (optional); removed 2 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: no split. The only stored brain MRI (initial_tool_outputs.mri) is a genuinely non-contrast epilepsy-protocol study; its only gadolinium content was the technique note '; no gadolinium', now removed so the report says nothing about contrast, and contrast_used stays null (decision 4: it answers both a plain and a contrast order; false would send a contrast order to the library normal). Criterion action-3-analyze-brain-mri unchanged (protocol epilepsy, plain per ILAE 2019 for a structural cause of focal epilepsy); expected_evidence has no enhancement wording. No case fallback MRI; the stored body imaging is CTPA and venous duplex, no MRI. Probe: plain and contrast orders get the case report with gad_text=n; perfect_agent ok.
- MRI-CONTRAST verified: checked the diff against 393c547e, mri_probe (plain, contrast, both orders, criterion) and perfect_agent -v; checked the diff against 393c547e, mri_probe and perfect_agent -v; only change is the removed "; no gadolinium" technique note, contrast_used null per decision 4 (both orders get the case report, gad_text n); criterion plain epilepsy protocol, expected_evidence in the report; nothing else changed; no case fallback MRI, no body MRI. No error found.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 9d0e5380-ae1e-4ef3-bb95-80e4727d893b | FIXED | LIT |
| a598b629-8c54-4fd1-9cb3-e71c01b4bb32 | FIXED | initial_tool_outputs.labs.panels.Coagulation[0] clinical_significance; CENTRAL 3 |
| 78946c3e-95a5-4762-b8c3-1c13ea60b331 | FIXED | ground_truth.sequence_constraints[1] CTA before MRI, [2] CTA before ambulatory EEG (soft, [ESC_PE_2019]); ground_truth.assessment.required_recommendations[0]; stop rule (see 54a0e930); CENTRAL 4 |
| ae306531-8980-4e76-a002-4497d9e13df7 | FIXED | initial_tool_outputs.labs.panels.AED Levels[0] clinical_significance; ground_truth.key_clinical_evidence[4]; action-9-interpret-labs expected_evidence |
| 54a0e930-b5a4-41d9-a054-d1bbc1e581cb | FIXED | action-6-analyze-eeg importance required -> recommended; ground_truth.stop_rule.required_before_assessment (action-6-analyze-eeg removed) |
| 9f64da60-9038-4049-b2a1-f94deac47cf3 | FIXED | followup_outputs[2].output.findings[2].type and morphology, impression, limitations |
| 02536f90-3380-4973-9442-c701dbf6a773 | FIXED | new ground_truth.avoided_actions[3] avoid-waste-tee |
| d2ad939c-5557-4fff-8f30-b6c430731e3a | FIXED | ground_truth.assessment.prohibited_recommendations[2] |
| 7a342e80-6f30-45b2-8924-df3488f96fd9 | FIXED | LIT |
| c6c6711b-69fb-4ed6-8472-b4ba91b32b9b | FIXED | LIT |
| a1f981cb-a45b-4ebd-8ab3-58a9274b6758 | FIXED | LIT |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.avoided_actions[4], [5], [6] | No tissue action was scored (class BIOPSY, D3; no stored biopsy here) | FIXED: avoid-harm-stereotactic-biopsy and avoid-harm-open-biopsy ([ILAE_MRI_2019]; MRI-negative, ambulatory EEG diagnostic, anticoagulation raises bleeding risk) and avoid-harm-resection ([Kwan_2010]; newly diagnosed, low-dose levetiracetam) |
| B | minor | followup_outputs | Pathway order put the TEE before the venous duplex and the interaction check before the EEGs in the middle of the list | FIXED: CTPA, sleep-deprived EEG, ambulatory EEG, interaction check, venous duplex, TEE |
| C | minor | ground_truth.avoided_actions[avoid-harm-resection].rationale | Called levetiracetam 500 mg twice daily an adequately dosed trial (verification pass 1) | FIXED |

## Changes
Pulmonary embolism first: CT pulmonary angiography now has soft priority over the brain MRI and the ambulatory EEG, and the anticoagulation must says to start anticoagulation without waiting for imaging when clinical probability is high or intermediate and bleeding risk is acceptable. EEG pathway: the routine EEG is recommended rather than required and is no longer in the stop rule; the prolonged ambulatory EEG is the decisive required study. Its report now says the convulsion was witnessed by his partner and logged in the event diary, with the generalized phase obscured by artifact. Labs: D-dimer now reads 'Markedly raised; requires urgent imaging for venous thromboembolism'; the levetiracetam level is described as below the laboratory reference range with no established therapeutic range (read with dose timing, adherence and renal function) in the lab row, the key evidence and the criterion. Prohibitions: valproate is prohibited on clinical grounds without the UK MHRA procedure. Avoided actions: TEE is scored as waste; standalone stereotactic and open biopsy and resection are scored as harmful. Sequence: the drug-interaction check (anticoagulant and ASM) is no longer constrained to follow the brain MRI. Earlier this round: literature searches removed (LIT). Not approved before this round.

## Verification
Pass 1: 1 error found
- Checked every note id against its ruling and the plan (D3, D7, D8, D10, D11, D12, D14, D15, D19-D22, D31), the final case text, the diff against 06b74446, perfect_agent -v (with a served-answer probe of each criterion's alternatives) and test_case_guards; no literature residue, no new em dashes.
- 1. ground_truth.avoided_actions[avoid-harm-resection].rationale read 'has not failed an adequately dosed ASM (levetiracetam 500 mg twice daily)', which presents the 500 mg twice-daily starting dose he is having breakthrough seizures on as the adequate dose, contradicting the must to raise it. FIXED: 'the epilepsy is newly diagnosed and has not yet had an adequate ASM trial (levetiracetam 500 mg twice daily is a starting dose)'. Own finding, no ruling changed.
Pass 2: 0 errors found
- Checked every note id against its ruling and the plan/decisions (D3, D4, D7, D8, D10-D12, D14, D15, D19-D22, D31), the notes text, the final case in full, the diff against 06b74446, perfect_agent -v, a realistic-call drug-interaction serving probe and test_case_guards -k; citations against the pack allow-list; no new em dashes.
- Served-answer probe: check_drug_interactions with an anticoagulant as the drug gets the DOAC/inducer report (followup[3]) that carries the criterion evidence; the perfect agent's generic call gets the current-medication review, by design.
- No change.
Pass 3: 1 error found
- Checked every note id against its ruling, the plan and decisions (D3, D4, D7, D8, D10-D12, D14, D15, D19-D22, D30, D31, MRI-CONTRAST decision 2), the notes text, the final case in full (patient, every stored report, ground truth), the diff against 06b74446, perfect_agent -v, served-answer probes (drug interactions, CT, MRI pair) and test_case_guards -k; no new em dashes.
- 1. ground_truth.sequence_constraints kept a soft constraint 'action-3-analyze-brain-mri before action-5-check-drug-interactions' with the tumour template reason ('a tumor or planned oncologic therapy favors non-inducing ASMs'). In this case the interaction check is the anticoagulant against the ASM, needed for PE treatment, and note 78946c3e rules that anticoagulation must not be delayed by the brain MRI. FIXED: constraint deleted; the two CTPA-first constraints stay. Ruling 78946c3e updated. perfect_agent and guards ok.
Pass 4: 0 errors found
- Checked every note id against its ruling (all present in the rulings file and the log), the plan and decisions (D3, D4, D7, D8, D10-D12, D14, D15, D19-D22, D30, D31, MRI-CONTRAST decision 2, October plan 3.C and pack section 5), the notes text, the final case in full, the diff against 06b74446 (including the unverified condition-audit changes), red-herring field paths, served-answer probes (labs, realistic drug-interaction calls), perfect_agent -v and test_case_guards -k (460 passed); no new em dashes.
- No change.
Pass 5: 0 errors found
- Checked every note id against its ruling (all present in the rulings file and the log), the plan and decisions (D3, D4, D7, D8, D10-D12, D14, D15, D19-D22, D30, D31, MRI-CONTRAST decision 2), the notes text, the final case in full (patient, every stored initial, follow-up and fallback report, ground truth, metadata), the diff against 06b74446 (including the condition-audit changes), red-herring field paths, laterality mentions, served-answer probes, perfect_agent -v and test_case_guards -k (54 passed); no new em dashes.
- No change.
Pass 6: 0 errors found
- Checked every note id against its ruling (all present in the rulings file and the log), the plan and decisions (D3, D4, D7, D8, D10-D12, D14, D15, D19-D22, MRI-CONTRAST decision 2), the notes text, the final case in full (patient, every stored initial, follow-up and fallback report, ground truth, metadata), the diff against 06b74446 (including the condition-audit changes), laterality mentions, red-herring field paths, perfect_agent -v and test_case_guards -k (460 passed); no new em dashes.
- No change.
Pass 7: 0 errors found
- Checked every note id against its ruling (all present in the rulings file and the log), the plan and decisions (D3, D4, D7, D8, D10-D12, D14-D16, D19-D22, D31, MRI-CONTRAST decision 2, October plan 3.C), the notes text, the final case in full (patient, every stored initial, follow-up and fallback report, ground truth, metadata), the diff against 06b74446 (no change since pass 6; the condition-audit changes were verified in passes 4-6), every new string since 06b74446, laterality and timeline, allergies and medications against musts and prohibitions, sequence and stop-rule ids, red-herring field paths, served-answer probes of the lab criteria, mri_probe, perfect_agent -v and case_io check (only the centrally maintained test_guidance_claims counts fail); no new em dashes.
- Kept on purpose: the base warning on lamotrigine with valproate in the anticoagulant interaction report is factually correct and no note targets it.
- No change.
