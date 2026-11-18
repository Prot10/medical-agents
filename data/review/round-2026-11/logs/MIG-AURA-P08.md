# MIG-AURA-P08

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 6ee45bc0-19ee-49b3-b0f3-00a1c126f70a | FIXED | Class LIT, commit 393c547e: the literature criterion and follow-up were removed; checked that the case contains no search_medical_literature criterion, follow-up or stored output. No literature criterion remains in ground_truth.action_criteria. |
| 252c9961-a22d-4393-8b92-f5552951afa7 | FIXED | Class LIT, commit 393c547e: the literature criterion and follow-up were removed; checked that the case contains no search_medical_literature criterion, follow-up or stored output. |
| 64c11ceb-6ab1-40ee-a444-52804daa43a9 | FIXED | Partly applied. The prohibition is now valproate only, on patient-specific grounds: contraindicated in POLG disease, best avoided in other mitochondrial disease when alternatives exist (levetiracetam, lamotrigine, lacosamide), and she can become pregnant (MHRA). Metformin left the prohibition and became a preference in required_recommendations[4]. The drug report (contraindications, alternatives, summary) and the drug-check expected_evidence were aligned. Field: ground_truth.assessment.prohibited_recommendations[0]. Declined part: The part not applied (removing every valproate restriction for this patient) is declined: she is a 29-year-old woman who can become pregnant, so the MHRA 2024 valproate pregnancy prevention rules apply whatever the mitochondrial question, and safer antiseizure alternatives exist (InterERNs 2024 seizure management in primary mitochondrial disease). |
| 7dd02d6c-e3ad-4b40-8ff7-c0f55d4c2451 | FIXED | The triptan and ergot prohibition was deleted (it was prohibited_recommendations[1]). The drug report warning now says that the 2026 international MELAS consensus (Mancuso M et al., Eur J Neurol 2026) identifies no specific contraindication to the standard acute headache drugs, triptans included, and that a stroke-like episode is not an ischaemic stroke; metadata.difficulty_description no longer says triptans are avoided. |
| f5f97597-9d4e-4819-b77a-d5edd23fc009 | FIXED | New recommended criterion action-eeg (analyze_eeg routine, ambulatory or video), placed after the MRI, not in the stop rule; recommended criteria are credited and never count as extra actions. A routine EEG is now stored as followup_outputs[0] (right parieto-occipital slowing, no epileptiform discharges or seizures, consistent with the stored ambulatory and video records, now followup_outputs[1] and [2]). Field: ground_truth.action_criteria[2]. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B | minor | fallback_tool_outputs.eeg | The case fallback held the routine EEG with the same findings as the new routine follow-up. | FIXED: moved into followup_outputs[0] (trigger request_routine_eeg, tool_parameters eeg_type routine); fallback eeg set to null |
| C | minor | initial_tool_outputs.drug_interactions.valproate.warnings[2] | Unsourced 'triptans generally avoided after a stroke-like episode'. | FIXED: per Mancuso 2026 MELAS consensus |
| E | minor | followup_outputs order | EEG follow-ups were in the middle of the pathway. | FIXED: routine, ambulatory and video EEG now followup_outputs[0..2], matching the criterion order (clinical, MRI, EEG, MRS, labs, mtDNA, echo, ECG, drug check) |

## Changes
The blanket drug prohibitions were revised. The triptan and ergot prohibition is gone (2026 MELAS consensus: no specific contraindication; a stroke-like episode is not an ischaemic stroke). Valproate stays prohibited for her, now on patient-specific grounds: POLG contraindication, alternatives available, and she can become pregnant (MHRA). Metformin moved from the prohibitions to a preference in the diabetes must. A recommended EEG step was added (routine, ambulatory or video; not in the stop rule), with a stored routine EEG showing right parieto-occipital slowing and no epileptiform activity; the EEG reports are now listed right after the MRI. The drug report was aligned. The literature step had already been removed (class LIT).

## Verification
Pass 1: 0 errors found
Checked: all five notes ruled; triptan prohibition gone and no other field calls triptans avoided; valproate prohibition on patient grounds; metformin a preference; every eeg_type (routine, sleep_deprived, ambulatory, video, continuous_icu) is answered by a stored abnormal EEG with the same findings, none by the library normal; perfect_agent and test_case_guards pass.
Pass 2: 0 errors found
Checked: every note ruled and applied as the plan states; no literature output; no contradiction found between labels, musts, prohibitions, differential, key evidence and reports; perfect_agent passes; test_case_guards -k passes. EEG probe: routine, sleep_deprived, ambulatory, video and continuous_icu orders are all answered by a stored abnormal EEG.
Pass 3: 0 errors found
Checked: all five notes ruled; the partial DECLINED part of 64c11ceb gives a patient-specific guideline reason (MHRA valproate rules, InterERNs 2024); no triptan prohibition left; metformin a preference; routine, ambulatory and video EEG served by stored abnormal records consistent with the right parieto-occipital MRI lesion and the left field defect; drug report has real content agreeing with her medicines; perfect_agent passes; case_io check and test_case_guards -k pass.
Pass 4: 0 errors found
Checked: every note ruled and applied as the plan states; no literature output; labels, musts, prohibitions, differential, key evidence, red herrings and reports agree; no answer leakage in the patient block; perfect_agent passes; case_io check (no failure names the case) and test_case_guards -k pass.
Condition audit (MIG-AURA auditor, 17 Nov 2026): 1 error found
- D/leak (own finding, present at base 06b74446): initial_tool_outputs.drug_interactions.valproate is returned by the first drug-interaction query of any drug, and its `proposed` line said "a patient with m.3243A>G mitochondrial disease" and its summary "Valproate is avoided in this patient", i.e. the result of the required mtDNA test (action-mtdna-test) and the diagnosis before the test is ordered. FIXED: `proposed` now reads "a woman with suspected maternally inherited mitochondrial disease (her mother carries m.3243A>G; ...)", which is what the HPI already states; the summary keeps the same drug content (valproate avoided: MHRA pregnancy rules, POLG contraindication, avoided in other mitochondrial disease when an alternative exists; metformin not preferred and topiramate with caution in mitochondrial disease; levetiracetam; triptans acceptable) without asserting her genotype. No ruling changes (no note covers it). perfect_agent passes; test_case_guards -k passes.
Pass 5: 0 errors found
- Checked the condition-audit change: initial_tool_outputs.drug_interactions.valproate.proposed ('suspected maternally inherited mitochondrial disease; her mother carries m.3243A>G') matches the patient block (mother with confirmed MELAS, m.3243A>G); summary no longer asserts her genotype and keeps the drug content of the criterion's expected evidence (valproate, metformin, topiramate, levetiracetam, triptans acceptable per [MELAS_2026]). perfect_agent.py -v ok; test_case_guards -k (eight ids) 64 passed.
