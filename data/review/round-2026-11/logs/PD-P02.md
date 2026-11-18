# PD-P02

## Reviewer notes
Reviewer status: R1 in_progress, R2 none | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 5b975043-c475-4614-afb7-a073d22fb33e | NO-ACTION (plan D29) | Approval comment on `patient.chief_complaint`; nothing changed for it. The class edits below were still applied because they are real defects. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | patient.neurological_exam.motor | Rigidity written as 'mild bilateral cogwheel rigidity at wrists' with no rest tremor: MDS 2015 parkinsonism needs velocity-independent rigidity, cogwheeling alone does not count (class D5) | FIXED: 'mild velocity-independent rigidity on slow passive movement at both wrists (lead-pipe, with superimposed cogwheeling), symmetric' |
| A | major | ground_truth.assessment.required_recommendations[1]; ground_truth.action_criteria[6] | The must demands an ECG before the cholinesterase inhibitor, but no criterion ordered one and no ECG was stored, while the patient has had two syncopes on midodrine (class D10) | FIXED: new recommended `ecg-before-chei` (`analyze_ecg {}`, [ESC_2018]) before the medication review, with `initial_tool_outputs.ecg` (sinus rhythm 64/min, PR 164, QRS 92, QTc 418 ms) |
| C | minor | ground_truth.sequence_constraints | Soft 'MRI before DaTscan' constraint cited [Postuma_2015], which does not state it (class D2) | FIXED: deleted |
| B | minor | followup_outputs[8] (autonomic_testing), followup_outputs[9] (tilt_table) | The two stored tilt results differ slightly (28/14 vs 30/16 mmHg); both are separate tests and both orders are avoided as waste | FLAGGED (left: plausible as two recordings) |

## Changes
The case is unchanged clinically (probable DLB). The motor examination now describes the rigidity by the MDS definition: mild velocity-independent rigidity at both wrists, lead-pipe with superimposed cogwheeling, symmetric. Because the must asks for an ECG before starting the cholinesterase inhibitor in a man with two syncopes on midodrine, a recommended criterion 'Baseline 12-lead ECG before starting a cholinesterase inhibitor' (ESC 2018) now orders it, and a normal ECG (sinus rhythm 64/min, PR 164 ms, QRS 92 ms, QTc 418 ms) is stored as its result. The soft constraint 'MRI before DaTscan' was removed, since no guideline states it. MRI stays required (dementia work-up). The approval note needed no action.

## Verification
perfect_agent.py -v: ok (every required/recommended criterion answered from the case's own stored data). test_case_guards.py -k (six PD worker cases): 48 passed. case_io.py check: schema and synonym guard OK; the only failures naming PD are test_guidance_claims PD rows (central, plan CENTRAL 3) and a zero-cost required set in PD-RM05 (another worker's case).
Pass 1: 0 errors found
- Checked: NO-ACTION ruling; D5 rigidity sentence; new `ecg-before-chei` (recommended, ECG rate 64 matches the supine HR, no avoided action on analyze_ecg, served from `initial_tool_outputs.ecg`); D2 constraint deletion; MRI required; drug output agrees with medications and allergies. No change.
Checks after pass 1: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 2: 1 errors found
- `ground_truth.key_clinical_evidence[5]` stated the DaTscan, MIBG and PSG results as findings, but all three criteria are optional (plan F4: an optional result is written "if obtained"). Now: "Reduced DaT uptake, low cardiac MIBG uptake and PSG-confirmed REM sleep without atonia, if obtained, are indicative biomarkers; ...".
- Checked, no change: NO-ACTION ruling; D5 rigidity; `ecg-before-chei` (recommended, served from `initial_tool_outputs.ecg`, rate 64 equals the supine HR, fallback ECG null, no avoided action on analyze_ecg); D2 deletion; the drug output agrees with medications and allergies.
Checks after pass 2: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 3: 0 errors found
- Checked: NO-ACTION ruling (D29); D5 rigidity sentence; `ecg-before-chei` (recommended, served from `initial_tool_outputs.ecg`, rate 64 equals the supine HR, no avoided action on analyze_ecg) backs REQ[1]; D2 deletion; KCE[5] 'if obtained'; timeline arithmetic (hallucinations 2 years, motor 8 months, 16 months) in REQ[0], KCE[2] and red herring; rivastigmine and donepezil doses; drug output agrees with medications and allergies. No change.
Checks after pass 3: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 4: 0 errors found
- Checked: NO-ACTION ruling (D29); D5 rigidity sentence; `ecg-before-chei` (recommended, served from `initial_tool_outputs.ecg`, rate 64 equals the supine HR, fallback ECG null, no avoided action on analyze_ecg) backs REQ[1]; drug output (midodrine and rivastigmine bradycardia, haloperidol alert) agrees with medications and allergies; D2 deletion; MRI required and the only stop-rule id; KCE[5] 'if obtained'; timeline (hallucinations 24 months, functional decline 12 months, motor 8 months, haloperidol 3 months) in REQ[0], KCE[2] and the differential; MMSE items sum to 23. No change.
Checks after pass 4: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
