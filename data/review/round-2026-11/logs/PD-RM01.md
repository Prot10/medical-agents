# PD-RM01

## Reviewer notes
Reviewer status: R1 in_progress, R2 none | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| d3fc1f93-df7b-4a01-939e-b149828b4d72 | FIXED (plan D19) | `ground_truth.diagnosis.accepted[0]` -> "Parkinson's disease with motor worsening and episodic saccadic freezing on low-dose levodopa (possibly dopamine-responsive)" (G20.A1 unchanged; CENTRAL synonyms check); `required_recommendations[0]` canonical (keep PD; freezing may be dopamine-responsive; record its relation to levodopa doses and reassess eye movements after dose optimization before attributing it to undertreatment); `metadata.difficulty_description` and `difficulty_rationale` say 'possibly dopamine-responsive'. Matcher tested: 'Parkinson's disease', the new label and 'PD, not PSP' match; 'Progressive supranuclear palsy' does not. |
| cfc0fa20-217c-4158-b4ae-25feba8a247e | FIXED (plan D20) | New `ground_truth.differential[4]` 'Posterior circulation transient ischemic attack' (G45.0, low) with the plan's key features; new conditional must `required_recommendations[2]` (vertebrobasilar vascular imaging if episodes occur without an attempted gaze shift or with brainstem symptoms beyond the slurred speech; wording clarified at verification pass 4). No vascular-imaging criterion, as the note asks. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| - | - | - | No further defect found on a full read (MoCA items sum; MRI, DaTscan, PSG and battery consistent with the exam) | - |

## Changes
PD remains the diagnosis and the MRI remains required. The label and the diagnostic must no longer state that the saccadic freezing is caused by undertreatment: the freezing is described as possibly dopamine-responsive, and the must asks to record its relation to levodopa doses and to reassess the eye movements after dose optimization before attributing it to undertreatment. Posterior circulation TIA is now a low-likelihood safety differential (vascular risk, episodic oculomotor symptoms with dysarthria, a normal MRI does not exclude transient ischemia), with a conditional must to assess the vertebrobasilar circulation if episodes occur outside eye-movement tasks or with other brainstem symptoms; vascular imaging is not made mandatory.

## Verification
perfect_agent.py -v: ok (every required/recommended criterion answered from the case's own stored data). test_case_guards.py -k (six PD worker cases): 48 passed. case_io.py check: schema and synonym guard OK; the only failures naming PD are test_guidance_claims PD rows (central, plan CENTRAL 3) and a zero-cost required set in PD-RM05 (another worker's case).
Pass 1: 0 errors found
- Checked: label and REQ[0] per D19 (matcher re-tested: 'Parkinson disease' matches, PSP and posterior circulation TIA do not); TIA differential and conditional must per D20 (vascular risk factors and dysarthria agree with the medication list, history and exam); no vascular-imaging criterion.
- Cosmetic (not counted): `metadata.difficulty_rationale` double comma ',,' fixed.
Checks after pass 1: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 2: 0 errors found
- Checked every note ruling against the plan and the note, the changed text against the rest of the case (HPI, exam, vitals, medications, differential, evidence, prohibitions, stop rule); no change.
Checks after pass 2: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 3: 0 errors found
- Checked: label and REQ[0] per D19 (no remaining 'subtherapeutic' or 'attributable to undertreatment' wording anywhere in the case); TIA differential and conditional must per D20 (insulin-treated diabetes, hypertension, hyperlipidaemia and the dysarthria during episodes are in the history and exam); no vascular-imaging criterion. No change.
Checks after pass 3: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 4: 0 errors found
- Checked: label and REQ[0] per D19 and the note (no 'undertreatment' or 'subtherapeutic' wording left); TIA differential per D20 (vascular risk factors in the history and medications, dysarthria during episodes in the HPI and exam); no vascular-imaging criterion; matcher: 'Parkinson's disease' matches, 'Progressive supranuclear palsy' and 'Posterior circulation TIA' do not.
- Cosmetic (not counted): `ground_truth.assessment.required_recommendations[2]` said 'if episodes occur outside eye-movement tasks or with other brainstem symptoms', which reads ambiguously because the HPI already reports episodes during conversation with slurred speech; now 'if episodes occur without an attempted gaze shift or with brainstem symptoms beyond the slurred speech (vertigo, limb weakness or numbness, ataxia)', matching the differential's 'without other brainstem signs'. Note row and rulings file updated.
Checks after pass 4: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
