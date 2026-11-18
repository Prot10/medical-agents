# MG-RM15

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-5-search-medical-literature (optional); removed initial literature_search outputs: myasthenic crisis management. Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R2 approved | Approved before this round: yes

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:MG-RM15:policy_verdict | NO-ACTION | Approval of all seven dimensions, no comment. No change for the note. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| D | minor | followup_outputs[8..14] | Seven stored reports (gait_and_balance_timed, levodopa_challenge, speech_language_evaluation, orthostatic_blood_pressure, cognitive_screen, neuropsych_battery, functional_neuro_signs) answered off-pathway orders with no label (class C9, D10) | FIXED: ground_truth.avoided_actions[7..13] avoid-waste-gait-and-balance-timed, avoid-waste-levodopa-challenge, avoid-waste-speech-language-evaluation, avoid-waste-orthostatic-blood-pressure, avoid-waste-cognitive-screen, avoid-waste-neuropsych-battery, avoid-waste-functional-neuro-signs (waste, case-specific rationale, [Jacob_2025]); the reports were already last in the pathway, so no reorder |
| B | minor | followup_outputs[10].output (speech_language_evaluation) | Report says "not performed: intubated and sedated" but listed normal naming, repetition, comprehension and reading results with Boston Naming 57/60 and WAB AQ 98.6 | FIXED: findings now motor speech and language "not assessable: intubated and sedated"; quantitative_data emptied; impression unchanged |
| D | minor | ground_truth.avoided_actions[4] (avoid-waste-3-order-advanced-imaging), fallback_tool_outputs.advanced_imaging | The case fallback whole-body FDG-PET answered a whole_body_FDG_PET order unlabelled (the label matched only modality FDG_PET) | FIXED: whole_body_FDG_PET alternative added to the existing PET waste label (as in MG-P03), rationale "cerebral or whole-body", [Jacob_2025] |
| C | minor | ground_truth.action_criteria[0].rationale, key_clinical_evidence[2] | Respiratory rationale and key evidence cite the GBS 20/30/40 rule (Lawn 2001), which D8 replaces in MG | FLAGGED, not changed: approved case, plan D8 leaves RM15 unchanged because VC 12.9 mL/kg meets the ABN criterion (below 20 mL/kg) anyway |
| A | minor | metadata.last_revised, metadata.revision_reason | Updated to describe the edits | FIXED |

## Changes
MG-RM15 (approved by Reviewer 2; 50-year-old man in aspiration-precipitated myasthenic crisis, intubated). The approval is kept and nothing the reviewer approved was rewritten. Two classes of defect were corrected. First, seven bedside assessments or batteries that the case stores but that cannot be performed in a sedated, ventilated patient and answer no question in the crisis (timed gait and balance, levodopa challenge, speech and language battery, orthostatic blood pressure, cognitive screen, neuropsychological battery, functional neurological signs) are now labelled waste, and whole-body FDG-PET joins the existing FDG-PET waste label. Second, the stored speech and language report said the test was not performed but still listed normal naming, comprehension and reading results with test scores; those scores were removed so the report only says the patient is not assessable. No criterion, tier, stop rule, must or prohibition changed.

## Verification
Pass 1: 0 errors found
- Note NB-87M:MG-RM15:policy_verdict is an approval with no comment: NO-ACTION is right. Checked the class D10 changes only: the seven new waste labels each match their stored follow-up by discriminator (gait_and_balance_timed, levodopa_challenge, speech_language_evaluation, orthostatic_blood_pressure, cognitive_screen, neuropsych_battery, functional_neuro_signs) and none matches a criterion; their rationales agree with the patient (alert and oriented x3 before intubation, BP 124/78, VC 12.9 mL/kg); the speech report no longer lists scores for a test it says was not performed; whole_body_FDG_PET joins the PET label; no criterion, tier, stop rule, must or prohibition changed (approved case). No em dashes in new text.
- Cosmetic (not counted): none.
Checks after verification: perfect_agent.py -v pass; case_io.py check: no failure names this case; test_case_guards -k this id pass.
Pass 2: 0 errors found
- Nothing to re-verify: pass 1 found 0 errors and nothing was changed after it (no condition-audit or orchestrator fixes in this log). Ran the checks only.
Checks: perfect_agent.py -v pass; test_case_guards -k this id pass.
Pass 3: 0 errors found
- Nothing to re-verify: no change after the last zero-error pass (no condition-audit or orchestrator entry). Ran the checks only.
- Checks: perfect_agent.py -v pass; test_case_guards -k (all eight pass-3 ids) 64 passed.
