# MG-RS11

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-4-search-medical-literature (optional); removed initial literature_search outputs: ocular myasthenia gravis. Any literature query is now answered by the neutral library text.
- Synonyms (orchestrator, 17 Nov): G70.01 (with exacerbation) is no longer an accepted code in this stable case (diagnosis_synonyms.yaml G70.00 entry, MG CENTRAL C4); the code is a weight-0 component.

## Reviewer notes
Reviewer status: R2 approved (NB-87MF-FBTV-TPWE) | Approved before this round: yes

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:MG-RS11:policy_verdict | NO-ACTION | Approval with no comment. No change asked. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | major | ground_truth.action_criteria[1] (action-2-order-specialized-test); ground_truth.stop_rule.required_before_assessment | Neurophysiology (SFEMG or RNS) required and in the stop rule although AChR binding antibody is 7.6 nmol/L; the reviewer's identical ruling in MG-S05 (ocular, AChR positive) and ABN 2025 make neurophysiology mandatory only when antibodies are negative (class C2, plan D2) | FIXED: recommended, both alternatives kept, removed from the stop rule; rationale states why; citation [Jacob_2025] |
| C clinical | minor | ground_truth.assessment.prohibited_recommendations[2] | 'before AChR antibody testing and neurophysiology' made neurophysiology a precondition (C2 consequence) | FIXED: 'before AChR antibody testing (and neurophysiology when serology is negative)' |
| B consistency | minor | metadata.difficulty_rationale | Said 3 required actions | FIXED: 2 required, SFEMG or RNS and ice pack recommended |
| E language | minor | metadata.last_revised, metadata.revision_reason | Described the October audit | FIXED |
| C clinical | minor | ground_truth.assessment.prohibited_recommendations[0]; required_recommendations[2] | Unsourced 'above 20 mg/day' outpatient prohibition and a 10-20 mg prednisone start (class C4) | FLAGGED, not changed: plan C4/D4 leaves the approved RS11 wording, which R2 accepted, unchanged |
| C clinical | minor | ground_truth.assessment.required_recommendations[1]; initial_tool_outputs.ecg | Pyridostigmine must without the ABN baseline ECG, although an ECG (LVH by voltage) is stored (class C12) | FLAGGED, not changed: plan C12 excludes the approved RS11 |
| C clinical | minor | ground_truth.diagnosis.icd_codes | G70.01 (with exacerbation) granted in a new ocular presentation (D21) | CENTRAL C4 (synonyms), not hand-edited |
| E language | minor | metadata.vocab_gap | Engineering note about the coherence validator in a field physicians see | FLAGGED: present in all 30 MG cases; condition-wide, left to the lead |
| D leakage | - | patient.history_present_illness | Brain MRI, MRA, MRV and orbital CT before referral are history; no criterion scores ordering them | checked, no action |
| - | - | literature | Class LIT: no literature criterion or stored output left | checked |

## Changes
Approved case, changed only for the condition-wide neurophysiology tier class (plan D2), which applies the reviewer's identical ruling in the other ocular AChR-positive case (MG-S05): single-fiber EMG or repetitive nerve stimulation is now recommended rather than required and no longer has to be done before the diagnosis is submitted, because with an AChR binding antibody of 7.6 nmol/L the diagnosis is serological and ABN 2025 makes neurophysiology mandatory only in antibody-negative patients. Both alternatives stay, and the abnormal SFEMG of the left orbicularis oculi still earns credit. To match, the prohibition on attributing the eye signs to a brainstem vascular cause now reads 'before AChR antibody testing (and neurophysiology when serology is negative)', and the difficulty rationale counts two required actions. Nothing else changed: the steroid wording and the pyridostigmine must R2 approved are kept as they are (the plan leaves them for this approved case). Checks: perfect_agent.py -v ok (the mediastinal MRI alternative gets the library normal, consistent with the normal CT); no MRI edited; class LIT checked, no literature left.

## Verification
- 17 Nov 2026: perfect_agent.py -v ok; test_case_guards.py -k (MG-RS11..MG-RS16) 48 passed; case_io.py check: schema OK, synonym guard OK, no test failure names these cases.
- Pass 1: 0 errors found. Checked the C2 tier change (recommended, out of the stop rule, both alternatives kept), the prohibition wording, the difficulty rationale, that nothing else changed in this approved case, perfect_agent.py -v (SFEMG and ice pack served their stored reports), mri_probe and test_case_guards -k (48 passed). No change.
- Pass 2: 0 errors found. Pass 1 found 0 errors and nothing was changed after it (no condition-audit or orchestrator entry), so nothing new to verify. perfect_agent.py -v ok (mediastinum_MRI contrast alternative answered by a fallback, the plan C-wide alternative, warning only); test_case_guards -k MG-RS11..MG-RS16 48 passed. No change.
- Pass 3: 0 errors found. Pass 2 found 0 errors and nothing was changed after it (no condition-audit or orchestrator entry), so nothing new to verify. perfect_agent.py -v ok (mediastinum_MRI contrast alternative answered by a fallback where flagged, warning only); test_case_guards.py -k (MG-RS11, RS13..RS16, S03, S04) 56 passed. No change.
