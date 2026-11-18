# FND-S10

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress, no R2 note | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 320b9e74-3b17-4136-8777-85d6e1f04f6f | FIXED | Class LIT, commit 393c547e; checked: no literature criterion or output left (whole case) |
| f63f04c2-b063-4309-a8c8-666c49392caa | FIXED | Class ACUTE: ground_truth.action_criteria[action-4-analyze-brain-mri] recommended -> required, label "Non-contrast brain MRI with DWI", canonical rationale plus dissection, citations [Espay_2018], [AHA_ASA_Stroke_2026]; ground_truth.stop_rule.required_before_assessment += action-4-analyze-brain-mri |
| 5e190f36-d854-459f-9a5e-9928f037e074 | FIXED | Decision 12: patient.clinical_history.social_history.recent_stressor rewritten to the canonical text (phone call 2 days ago, immediately before onset) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| A | minor | ground_truth.action_criteria order; followup_outputs order | Plan 2.ORDER. | FIXED: criteria already in order; follow-ups: neuropsychology answer before the on-request performance status |
| E | minor | metadata.difficulty_rationale; metadata.revision_reason; metadata.last_revised | Described the MRI as earned but not required. | FIXED |
| C | minor | ground_truth.avoided_actions[avoid-waste-1-analyze-ecg] | Checked per plan: ECG stays waste (no loss of consciousness). | no change |

## Changes
The literature step is gone (class LIT). A non-contrast brain MRI with DWI is now required and in the stop rule with the examination, because a sudden left hemiparesis of 2 days is imaged whatever the examination shows (Espay 2018; AHA/ASA 2026); the stored normal MRI answers it. The social history now dates the dissertation rejection to the phone call 2 days ago, immediately before the onset, as the HPI says. Follow-ups are reordered (neuropsychology before performance status). Reports, differential, musts and prohibitions are unchanged.

## Verification
perfect_agent.py -v: ok (MRI served the case's own plain study). test_case_guards -k FND-S10: pass. case_io.py check: no failure names FND-S10.
Pass 1: 0 errors found
- Checked: note rulings correct (LIT; ACUTE MRI required and in the stop rule; social history now dates the rejection to the phone call 2 days ago, matching HPI and chief complaint, no other 3-week reference left); MRI served from the case's own plain DWI study; ECG stays waste (no loss of consciousness).
- Re-run after the fixes: perfect_agent.py -v ok; test_case_guards -k for the case: pass; case_io.py check: no failure names this case (the only condition-wide failure is test_library_never_answers_a_contradicted_order[FND-RS02], another case).
Cosmetic (not counted): none.
Pass 2: 1 errors found
- Sequence constraint reason contradicted the required MRI: the soft "examination before MRI" constraint said the examination's positive signs "decide whether imaging has a specific question to answer", while the MRI is now required whatever the examination shows (class ACUTE). Fixed: ground_truth.sequence_constraints[0].reason now "The examination comes first: it defines the deficit the imaging must explain and takes minutes, so it does not delay the MRI (Espay 2018)." (wording as in FND-M05). Constraint ids and severity unchanged.
- Checked without change: every note id has a correct ruling in the log and rulings file; tiers, stop rule (all required criteria, max 0) and criteria order match the plan; no literature criterion or output left; stored MRI served to the plain order (mri_probe, contrast_used null per MRI-CONTRAST decision 4); no patient-text leakage; no em dashes in new text.
- Re-run after the fix: perfect_agent.py -v ok; test_case_guards -k for the batch: 48 passed; case_io.py check: no failure names this case (only test_library_never_answers_a_contradicted_order[FND-RS02], another case).
Cosmetic (not counted): none.
Pass 3: 0 errors found
- Checked without change: three note rulings correct (LIT; ACUTE MRI required and in the stop rule; social history now dates the rejection to the phone call 2 days ago, no other 3-week reference left anywhere in the case); MRI evidence names the right motor pathway for a left hemiparesis; ECG and Holter stay waste (no loss of consciousness), consistent with the red herring; no leakage; no em dashes in new text.
- Re-run: perfect_agent.py -v ok (every required/recommended criterion served by the case's own data, none by the library or case fallback; mri_probe confirms the stored plain DWI study for the MRI orders); test_case_guards -k for the batch: 48 passed; case_io.py check: schema and synonym guard OK, no failure names this case (only test_library_never_answers_a_contradicted_order[FND-RS02], another case).
Cosmetic (not counted): none.
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (26, doctoral student): MoCA 30/30, RAVLT delayed recall z = 0.7, Trail Making B z = 0.5, TOMM trial 2 50/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-S10 passes.
Pass 5: 0 errors found
- Verified the condition-audit change only (neuropsychology battery numbers): MoCA 30/30, RAVLT delayed recall z = 0.7, Trail Making B z = 0.5, TOMM trial 2 50/50 in quantitative_data match the MoCA and TOMM findings rows; all values are in the normal range (MoCA >= 26, z > -1, TOMM above the 45 cut-off), so they agree with the impression (cognition within normal limits, performance validity passed); no other field of the case cites these numbers (grep MoCA, RAVLT, Trail, TOMM). perfect_agent.py -v ok; test_case_guards -k (eight cases) 64 passed.
