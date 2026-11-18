# MIG-AURA-P09

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 8d56a61f-e267-4f6f-a6fd-cd3da265cd71 | FIXED | Class LIT, commit 393c547e: the literature criterion and follow-up were removed; checked that the case contains no search_medical_literature criterion, follow-up or stored output. |
| befb9ef9-b1f7-4cc7-843f-7fc513720022 | FIXED | 'Hemiplegic migraine (probable sporadic, ICHD-3 1.2.3)' became 'Sporadic hemiplegic migraine (ICHD-3 1.2.3.2)'; the rest of the label is unchanged. The gene panel stays optional; nothing requires genetic testing. Field: ground_truth.diagnosis.accepted[0]. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.assessment.prohibited_recommendations[1] | TIA prohibition said 'imaging shows no infarct' as if imaging answered the TIA question (plan D4 class, recurrent identical attacks). | FIXED: reworded; a normal MRI excludes infarction, not TIA, so the decision rests on the stereotyped aura features |

## Changes
The label now reads 'Sporadic hemiplegic migraine (ICHD-3 1.2.3.2)' instead of 'probable sporadic': five qualifying attacks and no affected relative meet the criteria, and the gene panel stays optional. The TIA prohibition now rests on the stereotyped aura features and says that a normal MRI excludes infarction, not TIA. The literature step had already been removed (class LIT). Nothing else changed.

## Verification
Pass 1: 0 errors found
Checked: both notes ruled; no 'probable' left; the clinical assessment already states 1.2.3.2; TIA prohibition reworded per D4; the em dash in accepted[0] is the unchanged remainder of the label; perfect_agent and test_case_guards pass.
Pass 2: 0 errors found
Checked: every note ruled and applied as the plan states; no literature output; no contradiction found between labels, musts, prohibitions, differential, key evidence and reports; perfect_agent passes; test_case_guards -k passes.
Pass 3: 1 errors found
- C (class TIA-CERT, plan D4 rule 1): ground_truth.differential[0] (Transient ischaemic attack) listed "normal MRI without infarct" as evidence against TIA, while the reworded prohibition in the same case says a normal MRI excludes infarction, not TIA. FIXED: the MRA, CT and Holter stay as listed; the MRI clause now says it excludes infarction but not TIA, so the clinical features decide.
Checked and correct: both notes ruled; label 1.2.3.2 without "probable", consistent with the clinical assessment; gene panel optional; no literature output; perfect_agent passes; case_io check and test_case_guards -k pass.
Pass 4: 0 errors found
Checked: every note ruled and applied as the plan states; no literature output; labels, musts, prohibitions, differential, key evidence, red herrings and reports agree; no answer leakage in the patient block; perfect_agent passes; case_io check (no failure names the case) and test_case_guards -k pass.
Condition audit (MIG-AURA auditor, 17 Nov 2026): 1 error found
- D/leak (own finding, present at base): initial_tool_outputs.drug_interactions.sumatriptan, returned by the first drug-interaction query of any drug, said the patient has "an unruptured intracranial aneurysm" (`proposed`, and warnings[0] "No data on triptan use with an unruptured intracranial aneurysm"), which is the result of the required MR angiography (action-mra, expected evidence "4 mm unruptured saccular left MCA bifurcation aneurysm"); at turn 0 only his father's and sister's aneurysms are known. FIXED: `proposed` ends at "(pulse 62)"; warnings[0] deleted (its second clause, that the triptan restriction comes from the hemiplegic migraine, is already in contraindications[0] and the summary). The drug-check expected evidence is unaffected. No ruling changes. perfect_agent passes.
Pass 5: 0 errors found
- Checked the condition-audit change: initial_tool_outputs.drug_interactions.sumatriptan no longer mentions the patient's aneurysm (only found by the required MRA); proposed ends at '(pulse 62)', the hemiplegic-migraine triptan restriction stays in contraindications[0] and the summary; the criterion's expected evidence (triptans avoided, no verapamil with propranolol, rizatriptan 5 mg) is still in the report. perfect_agent.py -v ok; test_case_guards -k (eight ids) 64 passed.
