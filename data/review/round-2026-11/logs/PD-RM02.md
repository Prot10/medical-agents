# PD-RM02

## Reviewer notes
Reviewer status: R1 in_progress, R2 none | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 07401754-64db-4495-be50-0533ab76ab08 | FIXED (plan D31, D30) | `ground_truth.differential[2].key_features` (not excluded by the unremarkable MRI or the abnormal DaTscan until the outside records are reviewed); `required_recommendations[0]` adds that post-encephalitic parkinsonism, which can also reduce DAT binding, is less likely but not excluded until the records are reviewed; new must `required_recommendations[1]` (obtain and review the outside hospital records: cause, imaging, CSF, course); `red_herrings[2].correct_interpretation` aligned; `action_criteria[0].rationale` 'and here looks for sequelae'; `action_criteria[2].rationale` (DaTscan) says the abnormal scan does not separate PD from a post-encephalitic nigral injury (pass 3); `diagnosis.rejected` minus `post encephalitic parkinsonism` and `postencephalitic`; `metadata.difficulty_rationale` updated. PD kept as label. Matcher tested: 'Parkinson's disease (idiopathic)' matches, 'Valproate-induced parkinsonism' does not. |
| c2e6d577-589e-4342-a044-87fd58fcf3ce | FIXED (plan D14) | New must `required_recommendations[4]` after the levodopa must: coordinate initiation and titration with psychiatry, monitor at each step for hypomania, mania, psychosis and impulse-control symptoms, avoid dopamine agonists or use them only with particular caution and psychiatric agreement [NICE_NG71]. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.sequence_constraints | Unsourced soft 'MRI before DaTscan' constraint (class D2) | FIXED: deleted |
| D | minor | initial_tool_outputs.labs.panels.Hepatic_Function[2].clinical_significance | Raised ammonia (58 umol/L) has a null significance, displayed as 'none' (dataset-wide display class) | FLAGGED (the must and the differential already address it) |

## Changes
Idiopathic PD stays the leading diagnosis, with MRI and DaTscan required. Post-encephalitic parkinsonism is no longer treated as excluded: the differential, the diagnostic must and the red herring now say that neither the unremarkable MRI nor the abnormal DaTscan rules it out, that the non-motor features predating the illness make it less likely, and a new must asks to obtain and review the outside hospital records (cause, imaging, CSF, neurological course) before excluding it; it is no longer a rejected answer. Because of his bipolar II disorder, a new must asks to coordinate levodopa initiation and titration with psychiatry, to monitor for hypomania, mania, psychosis and impulse-control symptoms, and to avoid dopamine agonists or use them only with caution and psychiatric agreement. The unsourced MRI-before-DaTscan constraint was removed.

## Verification
perfect_agent.py -v: ok (every required/recommended criterion answered from the case's own stored data). test_case_guards.py -k (six PD worker cases): 48 passed. case_io.py check: schema and synonym guard OK; the only failures naming PD are test_guidance_claims PD rows (central, plan CENTRAL 3) and a zero-cost required set in PD-RM05 (another worker's case).
Pass 1: 0 errors found
- Checked: D31 differential, REQ[0], new records must, red herring and MRI rationale; rejected labels removed (matcher re-tested: 'Post-encephalitic parkinsonism' is neither accepted nor rejected, 'Parkinson disease' matches); D14 psychiatric must; constraint deleted; stop rule ids are required criteria. No change.
Checks after pass 1: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 2: 0 errors found
- Checked: D31 (differential, REQ[0], records must, red herring, MRI rationale, rejected labels), D14 must, constraint deletion, stop rule ids required; prohibitions do not conflict with the new musts.
- Cosmetic (not counted): `ground_truth.key_clinical_evidence[0]` "(UPSIT 23/40, severe microsmia)" now ends "when tested", as REQ[0] already says (the olfactory test is optional).
Checks after pass 2: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 3: 1 errors found
- `ground_truth.action_criteria[2].rationale` (action-7-order-advanced-imaging, DaTscan) still said 'an abnormal scan shows an underlying degenerative deficit', which contradicts note 07401754 and the new REQ[0] (post-encephalitic nigral injury can also reduce DAT binding). Now: '... so an abnormal scan shows an underlying presynaptic dopaminergic deficit; it does not separate PD from a post-encephalitic nigral injury, which can also reduce DAT binding [Marshall_2009]'. Rulings file updated.
- Checked, no change: D31 differential, REQ[0], records must, red herring, MRI rationale, rejected labels; D14 psychiatric must; constraint deleted; stop rule ids are required criteria; DaTscan and MRI reports state only their own findings.
Checks after pass 3: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 4: 0 errors found
- Checked: D31 differential, REQ[0], records must, red herring, MRI and DaTscan rationales (an abnormal scan does not separate PD from post-encephalitic nigral injury); rejected labels removed (matcher: 'Post-encephalitic parkinsonism' and 'Valproate-induced parkinsonism' neither accepted nor rejected); D14 psychiatric must, consistent with bipolar II, valproate and the drug output (no agonist suggested anywhere); timeline (olanzapine stopped 20 months ago, illness 18 months, motor onset 10 to 12 months, RBD 2 years, constipation 3 years); constraint deleted; stop rule ids are required criteria. No change.
Checks after pass 4: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
