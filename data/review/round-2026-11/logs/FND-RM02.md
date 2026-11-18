# FND-RM02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 7db59db3 | FIXED (class LIT, commit 393c547e) | Checked: no literature criterion or output left. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.diagnosis.rejected | Rejected label 'comitant esotropia' vetoed correct answers that describe the deviation the convergence spasm produces (tested with DiagnosisCriterion.matches: 'Functional diplopia (spasm of the near reflex) with intermittent comitant esotropia' scored False). | FIXED: replaced by 'acute acquired comitant esotropia' (the mimic named in the differential); the same answers now match, and 'Acute acquired comitant esotropia' is still rejected. |
| C | minor | ground_truth.action_criteria[3] (action-neuropsych-battery).expected_evidence | Template text 'mood, anxiety and somatic symptom burden', but the stored battery measures no somatic symptom burden (MoCA, GAD-7, PHQ-9, TOMM). | FIXED: evidence names what the stored battery reports (anxiety and mood, performance validity). |
| E | minor | metadata.revision_reason, metadata.last_revised | Revision text stale (said red-flag tests recommended / October only). | FIXED: November changes stated; last_revised 2026-11-16. |
| C | note | initial_tool_outputs.mri | Plain MRI with contrast_used null: kept (MRI-CONTRAST decision 4, null answers both orders). | No change. |

## Changes
FND-RM02 (29-year-old woman with functional diplopia from convergence spasm). The only reviewer note (literature step) is resolved by the class change: no literature step remains. One scoring defect was fixed: the rejected diagnosis label 'comitant esotropia' also vetoed correct answers that describe the intermittent comitant esotropia the convergence spasm produces; it is narrowed to 'acute acquired comitant esotropia', the mimic in the differential, which is still rejected. The neuropsychology criterion's evidence now names what the stored battery reports. Patient text, results, criteria tiers (examination required, MRI recommended), musts and prohibitions are unchanged.

## Verification
Pass 1: 0 errors found
Checked: every note id has a ruling in the log and rulings file and each ruling matches the plan; diff vs 06b74446 read, final case read in full (patient, criteria, stop rule, sequence, avoided actions, musts, prohibitions, differential, KCE, red herrings, metadata, stored outputs); no literature output left; perfect_agent.py -v passes and each criterion receives its own report (served outputs printed for the '?' rows); case_io check and test_case_guards -k pass for this case (the only suite failure is FND-RS02, not in this batch); no em dashes in new text. Also checked the rejected-label change with DiagnosisCriterion.matches (correct answers mentioning comitant esotropia match; 'Acute acquired comitant esotropia' stays rejected) and that 'comitant esotropia' is case-authored, not from diagnosis_synonyms.yaml.
Cosmetic (not counted): action-neuropsych-battery label 'Neuropsychological assessment of mood, anxiety and dissociation' changed to 'Neuropsychological assessment of mood and anxiety' (the stored battery has no dissociation measure).
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (29, software engineer): MoCA 30/30, RAVLT delayed recall z = 0.6, Trail Making B z = 0.4, TOMM trial 2 50/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-RM02 passes.
Pass 5: 0 errors found
- Checked (focused, changes after the last 0-error pass): the condition-audit neuropsychology values (quantitative_data and findings agree, all within normal limits for age, TOMM above the 45 cut-off, impression unchanged, no other field cites them) (MoCA 30/30, RAVLT z 0.6, TMT-B z 0.4, TOMM 50/50). perfect_agent.py -v passes; test_case_guards -k (8 cases) 63 passed, the only failure test_library_never_answers_a_contradicted_order[FND-RS02] (library_contradictions.yaml, already CENTRAL).
