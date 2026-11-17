# PD-RP04

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 7ebc619e-4a7f-47aa-bf25-ff5db7f6379b | FIXED (D24) | `assessment.required_recommendations[2]` canonical D24 text (DBS candidacy, STN versus GPi compared by the multidisciplinary team, GPi possibly preferable with multidomain MCI, anxiety, depressive symptoms and troublesome peak-dose dyskinesia, STN for larger medication reduction; [CAPSIT_PD_1999][Follett_2010]). In `required_recommendations[3]`, 'does not exclude STN-DBS' becomes 'does not exclude DBS'. `prohibited_recommendations[3]` (no exclusion on the MoCA alone) kept. Consistency: `patient.history_present_illness` 'evaluating her for STN-DBS candidacy' becomes 'evaluating her DBS candidacy and target'; `initial_tool_outputs.drug_interactions.general.proposed` 'Current regimen before DBS'. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| - | - | - | No other defect found. The levodopa-challenge rationale ('predicts the benefit of STN-DBS on every sign except tremor') is a correct statement of the CAPSIT evidence and stays. The documented levodopa-unresponsive tremor history stays (D15) | - |

## Changes
Approved before this round: no. STN-DBS is no longer the default target. The candidacy must says the levodopa challenge (65% improvement) supports DBS, and that the multidisciplinary team compares STN and GPi. GPi may be preferable given her multidomain mild cognitive impairment, anxiety and depressive symptoms and troublesome peak-dose dyskinesia, while STN allows a larger medication reduction. The levodopa-unresponsive postural and kinetic tremor enters the target choice. The cognitive must says MCI does not exclude DBS. The HPI and the drug-review report no longer present STN-DBS as the plan. No criterion, tier or stop rule changed. Checks: perfect_agent passes, and so does test_case_guards.

## Verification
Pass 1: 0 errors found
- Checked: note 7ebc619e applied as D24 (REQ[2] canonical, REQ[3] 'does not exclude DBS', HPI and drug report without a preset target); no other STN-default text remains (the levodopa-challenge rationale states the CAPSIT evidence). perfect_agent and test_case_guards pass.
- Cosmetic (not counted): `metadata.difficulty_rationale` counted 3 required criteria; the case has 4 (MRI, levodopa challenge, neuropsychological battery, medication review). Corrected.
