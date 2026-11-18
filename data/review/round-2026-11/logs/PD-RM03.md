# PD-RM03

## Reviewer notes
Reviewer status: R1 in_progress, R2 none | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 32a0532b-54c4-4fb1-b6ba-9286d71c43fd | FIXED (plan D15) | `required_recommendations[2]`: review propranolol and reassess its benefit for the postural tremor (resting HR 58 with levodopa being introduced: reduce or stop it if the benefit is small, the heart rate falls further or orthostatic symptoms appear, tapering, not abruptly; lying and standing BP and HR at each levodopa step; wording completed at verification pass 1). 'Which levodopa does not treat' deleted. `prohibited_recommendations[2]` (no abrupt stop) kept. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.action_criteria[0] (action-1-analyze-brain-mri); ground_truth.stop_rule | Structural MRI required and in the stop rule in clinically typical asymmetric rest-tremor PD with no red flag (class D1; NICE NG71 1.2.9) | FIXED: optional, D1 label and rationale ([NICE_NG71][Postuma_2015]); stop rule empty, max_additional_actions 2 |
| C | minor | ground_truth.key_clinical_evidence[5]; ground_truth.differential[3], [4], [5] | Evidence and differential rested on the MRI, now optional (class D1) | FIXED: D1 'if MRI is obtained' / 'and, if imaged' forms |
| C | minor | ground_truth.sequence_constraints | Unsourced soft 'MRI before DaTscan' constraint (class D2) | FIXED: deleted |
| E | minor | initial_tool_outputs.drug_interactions.general.summary, formulary_status | Empty strings | FIXED at verification pass 1: short summary of the listed interactions; 'on formulary' |

## Changes
PD remains the diagnosis, made clinically. Propranolol is no longer continued by default: the must asks to review it and reassess its benefit for his longstanding postural tremor, since his resting heart rate is 58 and levodopa is being introduced, to reduce or stop it if the benefit is small, the heart rate falls further or orthostatic symptoms appear, tapering rather than stopping abruptly, and to measure lying and standing blood pressure and heart rate at each levodopa step; the claim that levodopa does not treat postural tremor was removed. As a class correction for clinically typical PD (NICE NG71 1.2.9), the brain MRI is now optional ('only if an atypical feature or another structural question arises') and leaves the stop rule, which is now empty, so the case has no required test; the evidence and the vascular, PSP and MSA differential entries mention the MRI only as 'if imaged'. The unsourced MRI-before-DaTscan constraint was removed.

## Verification
perfect_agent.py -v: ok (every required/recommended criterion answered from the case's own stored data). test_case_guards.py -k (six PD worker cases): 48 passed. case_io.py check: schema and synonym guard OK; the only failures naming PD are test_guidance_claims PD rows (central, plan CENTRAL 3) and a zero-cost required set in PD-RM05 (another worker's case).
Pass 1: 1 errors found
- Note 32a0532b only partly applied: the must asserted that propranolol 'treats the longstanding postural tremor' instead of reassessing its benefit, as the note asks, and told the agent to act 'if bradycardia appears' when the resting rate is already 58. Fixed `ground_truth.assessment.required_recommendations[2]`: 'Review propranolol and reassess its benefit for the longstanding postural tremor: with a resting heart rate of 58 and levodopa being introduced, reduce or stop it if the benefit is small, the heart rate falls further or orthostatic symptoms appear, tapering rather than stopping abruptly; measure lying and standing blood pressure and heart rate at each levodopa step'. Rulings file updated. Lead: the D15 canonical is shared with PD-M04 (HR 62), which should get the same 'reassess its benefit' wording.
- Cosmetic (not counted): `initial_tool_outputs.drug_interactions.general.summary` and `formulary_status` were empty strings (the worker's own FLAGGED finding); filled with a short summary of the listed interactions and 'on formulary'.
Checks after pass 1: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 2: 0 errors found
- Checked every note ruling against the plan and the note, the changed text against the rest of the case (HPI, exam, vitals, medications, differential, evidence, prohibitions, stop rule); no change.
Checks after pass 2: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 3: 0 errors found
- Checked: REQ[2] per the note (benefit reassessed, HR 58, taper; 'levodopa does not treat' gone everywhere) with PRO[2] consistent; D1 optional MRI label and rationale, empty stop rule, KCE[5] and differential [3]-[5] in the 'if imaged' form, no red herring or must resting on the MRI; constraint deleted; drug output agrees with the medication list (propranolol 40 mg twice daily, sertraline). No change.
Checks after pass 3: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 4: 0 errors found
- Checked: REQ[2] per the note and D15 (benefit reassessed, HR 58 equals the vitals, taper; 'levodopa does not treat' gone everywhere), PRO[2] consistent; D1 optional MRI label and rationale, empty stop rule, KCE[5] and differential [3]-[5] in the 'if imaged' form, no red herring or must resting on the MRI; drug output (summary filled at pass 1) carries real interaction content and agrees with the medication list; constraint deleted. No change.
Checks after pass 4: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
