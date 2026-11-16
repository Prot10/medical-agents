# FTD-P02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-10-search-medical-literature (optional); removed initial literature_search outputs: behavioural variant frontotemporal dementia diagnostic criteria and management; difficulty_rationale: literature mention dropped. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| ea2be647-17af-4e44-9142-0d9f3882c2d6 | FIXED (class LIT, 393c547e) | initial_tool_outputs.literature_search null; re-verified |
| 7d0e7312-f577-4246-8bd5-06a1b1b3442e | ALREADY-FIXED | required_recommendations[0] already three-level; scorer accepts "possible bvFTD"; FDG-PET recommended and never extra (stop-rule premise answered) |
| 8aa821c6-6175-4aa3-80ae-efc6841c7856 | ALREADY-FIXED | required_recommendations[0] already includes definite; scorer accepts definite and GRN-associated answers (checked) |
| ad58e131-fd9b-4567-b5b9-e227f5bcc09f | FIXED | followup_outputs[3] (FDG-PET) and followup_outputs[4] (perfusion SPECT) impression closing sentence hedged (C4) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B | minor | initial_tool_outputs.labs.panels["Chemistry (CMP)"][5] | class C8: fasting glucose 102 (abnormal) had null significance; now "Marginally raised, in the impaired fasting glucose range; recheck, since quetiapine can raise glucose" (must 1 already reviews quetiapine for glucose). CENTRAL display remark: null prints as "none" | FIXED |
| B | minor | followup_outputs[request_plasma_progranulin].output.panels.Progranulin[0] | class C8: low progranulin had null significance; now "Low, consistent with GRN haploinsufficiency." | FIXED |
| B | minor | followup_outputs[order_performance_status] | class C6 templated text (prompting for self-care); rewritten from the history (administrative leave, impulsive contracts, husband oversees finances, self-care independent), Karnofsky 70 / ECOG 1 kept | FIXED |
| C | minor | ground_truth.avoided_actions[avoid-waste-5-order-ct-scan] | class C22 CT rationale replaced, citations [NICE_NG97], [SNLG_ISS_2024] | FIXED |
| B | minor | ground_truth.differential[0].key_features | verification pass 3: the primary psychiatric entry cited frontal hypometabolism as unqualified evidence against a psychiatric cause, against note ad58e131 and the hedged FDG/SPECT impressions (Ducharme 2020); now 'supports bvFTD but is not specific on its own with a near-normal MRI' | FIXED |
| B | minor | ground_truth.assessment.required_recommendations[1], [4], key_clinical_evidence[4], action_criteria[action-5-order-specialized-test].rationale | verification pass 3: 'onset at 48' contradicted the HPI (20-month history at age 48, so onset at 46 to 47); corrected to 'onset at 46 to 47' (presentation age 48 kept in metadata.notes and key evidence 0) | FIXED |

## Changes
The FDG-PET and perfusion SPECT impressions keep their findings but now end by saying the pattern is compatible with frontotemporal lobar degeneration, that mild frontal hypometabolism (hypoperfusion) is not specific and can occur in primary psychiatric disorders, and that clinical correlation is recommended. The marginally raised fasting glucose and the low plasma progranulin now carry a clinical significance line. The performance-status report now reflects the history (administrative leave, impulsive property contracts, her husband overseeing the finances, independent self-care; Karnofsky 70, ECOG 1), and the head CT waste rationale now says the CT duplicates an available MRI. The two certainty notes needed no change: must 0 already separates possible, probable and definite bvFTD, the scorer accepts all three, and the recommended FDG-PET and optional gene panel are never counted as extra actions.
Verification pass 3: the primary psychiatric differential no longer uses the frontal hypometabolism as if it excluded a psychiatric cause (supportive but not specific with a near-normal MRI), and the onset age in the musts, key evidence and genetics rationale now matches the 20-month history (46 to 47, not 48).

## Verification
Pass 1: 0 errors found
- Checked: must 0 three-level certainty, C4 hedge in FDG and SPECT, glucose and progranulin significance, performance status (husband's oversight of finances is already in the stored clinical assessment), CT rationale; perfect_agent and test_case_guards pass.
Pass 2: 0 errors found
- Checked: must 0 three levels (possible, definite and GRN-associated answers score), C4 hedge in FDG and SPECT, glucose and progranulin rows, performance status, quetiapine timeline (17 months before), patient text; perfect_agent and test_case_guards pass.
Pass 3: 2 errors found
- ground_truth.differential[0] used frontal hypometabolism as an unqualified argument against a primary psychiatric disorder, contradicting note ad58e131 and the hedged FDG/SPECT impressions; qualified. Rulings file (ad58e131) updated.
- Timeline: musts 1 and 4, key evidence 4 and the genetics rationale said 'onset at 48' although the HPI gives a 20-month history at age 48; now 'onset at 46 to 47'.
- Checked without change: all four note rulings, must 0 three levels, label and rejected (possible, definite and GRN answers score), glucose and progranulin rows, performance status, quetiapine timeline, stop rule and sequence ids, no literature remnant; perfect_agent and test_case_guards pass.
Pass 4: 0 errors found
- Checked: all four note rulings and field paths, must 0 three levels (possible, definite and GRN-associated answers score), FDG/SPECT hedge (C4), differential 0 qualifier, glucose and progranulin significance rows, onset 46 to 47 against the 20-month history, quetiapine timeline (17 months after onset), MoCA arithmetic, performance status, basic lab order served (probed), stop rule and sequence ids, no literature remnant; perfect_agent and test_case_guards -k pass.
Pass 5: 0 errors found
- Checked: all four note rulings and field paths, must 0 three levels (probed: possible and GRN-associated definite answers score, late-onset bipolar does not), FDG/SPECT hedge (C4), differential 0 qualifier, glucose and progranulin significance rows and abnormal flags, onset 46 to 47 and quetiapine timeline (17 months after onset), MoCA arithmetic, BMI, performance status, stop rule and sequence ids, no literature remnant, no em dash in new text; perfect_agent -v, mri_probe and test_case_guards -k pass.
Pass 6: 0 errors found
- Checked: all four note rulings and field paths, must 0 three levels, FDG/SPECT hedge (C4), differential 0 qualifier, glucose and progranulin significance rows, onset 46 to 47 and quetiapine timeline (17 months after onset), MoCA arithmetic (25/30), served orders probed (basic labs, progranulin), performance status, stop rule and sequence ids, no literature remnant, no em dash in new text; perfect_agent -v, mri_probe and test_case_guards -k pass.
Pass 7: 0 errors found
- Checked: all four note rulings and field paths, must 0 three levels (probed: possible and GRN-associated definite answers score, late-onset bipolar does not), FDG/SPECT hedge (C4), differential 0 qualifier, glucose and progranulin rows, onset 46 to 47 and quetiapine timeline, MoCA arithmetic (25/30), performance status, stop rule and sequence ids, no literature remnant, no em dash in new text; perfect_agent -v, mri_probe and test_case_guards -k pass.
Pass 8: 0 errors found
- Checked: every note id against the rulings file (field paths resolve to the intended targets), the pass-7 changes where present, label, musts and prohibitions against the plan classes, rejected list, differential and key evidence against the final reports, lab rows and abnormal flags, MoCA/MMSE arithmetic, performance status against the HPI, patient text for leakage, stop rule and sequence ids, no literature remnant, no em dash in new text; perfect_agent -v, mri_probe and test_case_guards -k pass.
