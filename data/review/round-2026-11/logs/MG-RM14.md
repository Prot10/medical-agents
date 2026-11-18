# MG-RM14

## Reviewer notes
Reviewer status: R2 approved | Approved before this round: yes (work/approved.txt)

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:MG-RM14:policy_verdict | NO-ACTION | Approval without comment; no change made for it. The class change below (D10) is the only edit. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| D | minor | ground_truth.avoided_actions[8..12]; followup_outputs[3..7] | Stored ice-pack test, timed gait battery, levodopa challenge, speech-language battery and orthostatic blood pressure answered off-pathway orders in a known-MG crisis with no label (class C9, D10) | FIXED: five waste labels with case-specific reasons, citing [Jacob_2025]; the reports were already at the end of the pathway (after the waste-labelled RNS and SFEMG), so no reordering |
| C | minor | ground_truth.action_criteria[0].rationale; assessment musts; action-2-order-body-imaging | Lawn 2001 20/30/40 thresholds, MGTX thymectomy wording and no mediastinal MRI alternative, which the plan corrects in non-approved cases | FLAGGED, not changed: plan D6, D8 and D17 leave approved RM14 as it is (its FVC 16.6 mL/kg meets the ABN ICU criterion anyway; the thymectomy verb is already "discuss"; the thymic criterion is optional) |

## Changes
MG-RM14 (55-year-old woman in myasthenic crisis after ciprofloxacin; approved by R2 before this round). The only change is a condition-wide class change: five stored reports that answered orders the policy neither asks for nor labels are now labelled waste: the ice-pack test (known MG in crisis), the timed gait and balance battery, the levodopa challenge, the speech-language battery and orthostatic blood pressure testing. No criterion, tier, sequence, stop rule, report, must or prohibition changed; metadata.last_revised and revision_reason updated. Because the approved case changed, it goes back to re-review.

## Verification
Pass 1: 0 errors found
- Approved case: only the D10 waste labels were added. Checked each rationale against the case and the stored reports: she is unable to walk safely and in respiratory distress (gait and orthostatic reports say "not performed"), has severe dysphagia and pooled secretions (oral levodopa unsafe), nasal barely intelligible speech; ice-pack test in known AChR-positive MG in crisis. No label matches a criterion (perfect_agent pass). NO-ACTION on the approval is correct; C5/C7/C15 deliberately not applied (D6, D8, D17).
- Cosmetic (not counted), not changed because the case is approved and the field predates this round: the stored orthostatic report (followup_outputs[7]) gives criteria_met as four false values although the test was not performed; null would be more accurate.
Checks after verification: perfect_agent.py -v pass; case_io.py check: no failure names this case; test_case_guards -k this id pass.
Pass 2: 0 errors found
- No change after the last zero-error pass (Pass 1 made no edit; no condition-audit or orchestrator entry), so nothing to re-verify.
- Checks: perfect_agent.py -v pass; test_case_guards -k (six MG cases) 48 passed.
Pass 3: 0 errors found
- Nothing to re-verify: no change after the last zero-error pass (no condition-audit or orchestrator entry). Ran the checks only.
- Checks: perfect_agent.py -v pass; test_case_guards -k (all eight pass-3 ids) 64 passed.
