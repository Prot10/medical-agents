# PD-M04

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| d579cd94-1eab-44e1-a747-55342f667e32 | FIXED | ground_truth.key_clinical_evidence[3] rewritten in the D1 'if obtained' form with the D9 wording [NICE_NG71][Schwarz_2014][Postuma_2015]. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | major | ground_truth.action_criteria[0] (action-1-analyze-brain-mri); ground_truth.stop_rule | MRI required and in the stop rule in clinically typical asymmetric rest-tremor PD with no red flag (NICE NG71 1.2.9; class TIER-MRI, plan D1) | FIXED (optional, D1 label and rationale, citations [NICE_NG71][Postuma_2015][Schwarz_2014]; required_before_assessment now empty, max_additional_actions 2) |
| D leakage | minor | ground_truth.differential[3].key_features, [4].key_features | MSA and PSP exclusions rested on the MRI | FIXED (clinical features first, 'and, if imaged, ...') |
| A schema | minor | ground_truth.sequence_constraints[0] | Unsourced MRI-before-DaTscan soft constraint (plan D2) | FIXED (deleted) |
| C clinical | minor | ground_truth.assessment.required_recommendations[2] | 'Continue propranolol ... which levodopa does not treat' is unsourced (levodopa can improve the re-emergent postural component) and gave no bradycardia plan at HR 62 (plan D15 class) | FIXED (canonical D15 review-and-taper must, HR 62, keeping 'propranolol and amlodipine add to orthostatic falls') |
| E language | minor | metadata.difficulty_rationale, revision_reason, last_revised | Counted '1 required criterion (MRI)' | FIXED ('no required test: the diagnosis is clinical') |

## Changes
Brain MRI is now optional and out of the stop rule. This is clinically typical asymmetric rest-tremor PD with no red flag, and NICE NG71 1.2.9 says structural MRI is not used to diagnose PD. An agent that makes the clinical diagnosis without a test earns full credit; an MRI order is credited as optional and answered with the same stored report. As the physician asked, the MRI evidence line now says the loss of the nigral swallow-tail sign, if MRI is obtained, is consistent with nigral degeneration but not specific for PD and not a diagnostic criterion. The MSA and PSP differential entries lead with clinical features, the MRI only 'if imaged'. The unsourced MRI-before-DaTscan constraint is removed. The propranolol must now asks to review propranolol at a heart rate of 62 (reduce or taper it if bradycardia or orthostatic symptoms appear) and to measure lying and standing pressure and heart rate at each levodopa step; it no longer says levodopa does not treat the postural tremor. Checks: perfect_agent.py -v ok; test_case_guards.py for PD-M01, PD-M02, PD-M03, PD-M04, PD-M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (maintained centrally, plan CENTRAL 3) and test_panel_case_contract on PD-RM05 (another worker's case). No MRI report edited (mri_probe run on M01: case MRI served). Not an approved case. Literature (class LIT): no literature criterion or stored literature output in the case (checked).

## Verification
Pass 1: 0 errors found
- Checked D1 (optional MRI, empty stop rule, KCE[3] and differential [3], [4] in the 'if imaged' form), D9 wording, D2 and the D15 propranolol must (HR 62). The UPSIT 28/40 cited by REQ[0] and KCE[1] is in the patient's own examination, so no 'if obtained' is needed. No change.
- Cosmetic (not counted): KCE[3] names the swallow-tail loss twice (D1 and D9 canonical texts joined); left as the canonical wording.
- Checks after the fixes: perfect_agent.py -v ok; test_case_guards.py -k for PD-M01..M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (central, plan CENTRAL 3).
Pass 2: 0 errors found
- Re-checked note d579cd94 (D9), D1 (optional MRI, empty stop rule, 'if imaged' lines), D2 and D15 (HR 62); MDS 2015 count (rest tremor plus validated olfactory loss = two supportive criteria); served outputs. No change.
- Cosmetic (not counted): KCE[3] still names the swallow-tail loss twice (D1 and D9 canonical texts joined), as pass 1 noted; left as the plan's canonical wording.
- Checks after pass 2: perfect_agent.py -v ok for all six; test_case_guards.py -k for PD-M01..M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (central, plan CENTRAL 3: labs and ECG counts); mri_probe: the case MRI answers every MRI order.
Pass 3: 0 errors found
- Re-read the whole case against D1, D2, D9 and D15: optional MRI with D1 label and rationale, empty stop rule, KCE[3] and differential [3], [4] in the 'if imaged' form, propranolol must (HR 62 = vitals), MDS 2015 count (rest tremor plus UPSIT 28/40 in the patient's own exam, no red flag: clinically established), DaTscan optional, swallow-tail side (left nigra, right-sided signs). No change.
- Cosmetic (not counted): KCE[3] still names the swallow-tail loss twice (D1 and D9 canonical texts joined); left as the canonical wording, as in passes 1 and 2.
- Checks after pass 3: perfect_agent.py -v ok for all six (MRI served from the case slot, confirmed with mri_probe); test_case_guards.py -k for PD-M01..M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (central, plan CENTRAL 3: labs and ECG counts).
