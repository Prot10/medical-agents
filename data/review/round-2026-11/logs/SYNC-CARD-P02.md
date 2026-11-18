# SYNC-CARD-P02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-8-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split followup_outputs[7] (analyze_brain_mri, trigger request_brain_mri, an unflagged report whose only gadolinium content was negative enhancement statements) into the plain study (contrast_used false, same slot and trigger) and the unchanged gadolinium study (contrast_used true, trigger request_brain_mri_with_contrast, right after it). Plain copy: observations 'No mass lesion or enhancing abnormality' -> 'No mass lesion' and 'No leptomeningeal enhancement' removed; impression drops 'or enhancing lesion' and the closing 'No leptomeningeal enhancement'; white matter, DWI and volume findings kept. The case has no brain MRI criterion: the MRI is an off-pathway study scored by a waste avoided action with empty required_arguments (ESC 2018 Class III, brain imaging not indicated in syncope without focal signs), which matches plain and contrast orders alike, so no criterion, evidence, stop rule or sequence constraint changed. Probe: plain order gets the plain copy (gad_text=n), contrast order the gadolinium study, either order, no library answer; perfect_agent passes.
- MRI-CONTRAST verified: checked the plain copy free of gadolinium content and internally consistent, the gadolinium copy identical to the base report apart from contrast_used true, contrast_used per the decision (no stored gadolinium study left null), mri_probe (plain, contrast and both orders in either sequence answered by the case, never the library), pathway order sensible, nothing outside the MRI split changed versus 393c547e (programmatic diff), perfect_agent -v passes, case_io check clean for this case; no brain MRI criterion (waste avoided action with empty required_arguments, ESC 2018 Class III), so no criterion argument to set; case fallback MRI null. No error found.

## Reviewer notes
Reviewer status: R2 approved (all dimensions) | Approved before this round: yes

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-P02:policy_verdict | NO-ACTION | Approval without comment. Only the class findings below were applied (plan C3, D3, D27). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.avoided_actions (new avoid-waste-bubble-study) | A stored agitated-saline study (followup_outputs[10], no shunt) answered a bubble-study order with no label, although nothing in this HCM syncope raises a shunt (class C3, D3). | FIXED: waste entry {order_echocardiogram, echo_type bubble_study}. |
| C | minor | ground_truth.avoided_actions (new avoid-waste-tee) | The case fallback echo is a TEE; a TEE order was unlabelled though no question is left open by TTE (class C3). | FIXED: waste entry {order_echocardiogram, echo_type TEE}. |
| C | minor | ground_truth.avoided_actions (new avoid-waste-polysomnography) | A stored polysomnography (followup_outputs[11]) answered an unlabelled order; OSA is already diagnosed and on CPAP (class C3). | FIXED: waste entry {order_specialized_test, test_type polysomnography}. |
| B | minor | followup_outputs order | The recommended gene panel sat after the off-pathway exercise test and the MRI pair. | FIXED: moved to followup_outputs[4], after the exercise echo and before the drug checks; off-pathway reports (exercise test, MRI pair, bubble study, polysomnography) now last. |
| C | minor | followup_outputs[7] (exercise_stress_test) | Left unlabelled by plan D27: the BP response and arrhythmia it gives are not useless beside the required exercise echo. | FLAGGED (no change, plan D27). |

## Changes
Approved case, changed only for a condition-wide class defect (served test reports that answer an order with no label). Three avoided actions were added, all waste and all additive: a bubble study (no stroke, TIA, hypoxaemia or shunt question), a transoesophageal echo (no question left open by the transthoracic study) and polysomnography (sleep apnoea already diagnosed and treated with CPAP). In the pathway list the cardiomyopathy gene panel now follows the exercise echo, before the drug checks, so the off-pathway reports (exercise test, brain MRI pair, bubble study, sleep study) come last. No diagnosis, criterion, must, differential or report text changed; the perfect-agent check passes.

## Verification
perfect_agent.py -v passes (each criterion receives the stored report carrying its expected evidence); case_io.py check: schema OK, synonym guard OK, no test failure names the case; test_case_guards.py -k <id> passes.

Pass 1: 0 errors found
- Checked: the approval ruling (NO-ACTION), the three additive waste labels against plan C3 and the stored reports (OSA on CPAP is in the history; no shunt question), the pathway reorder, D27 (exercise test unlabelled), perfect_agent -v, test_case_guards -k and case_io check. Nothing changed.

Pass 2: 0 errors found
- Pass 1 found 0 errors and no condition-audit or orchestrator change follows it, so nothing was left unverified. Re-ran perfect_agent.py -v (passes) and test_case_guards.py -k (passes). Nothing changed.
- Condition auditor, 17 Nov 2026, blind leak pass: a check_drug_interactions output (served to any drug query, including a first call before any test) named the diagnosis: "to be avoided in hypertrophic cardiomyopathy with LVOT obstruction ... (ESC 2023 cardiomyopathy guideline)" in the initial, fallback, amlodipine and losartan outputs. Now "to be avoided if dynamic LVOT obstruction, resting or provocable, is present" (the exam's Valsalva-augmented murmur already raises it). The drug criterion's expected evidence (afterload reduction worsening dynamic outflow obstruction) is still carried. Approved case: changed for a real leak only. perfect_agent, test_case_guards -k, case_io check clean.
Pass 4: 0 errors found
- Verified the condition-audit leak fix: 'hypertrophic cardiomyopathy' no longer appears in any drug output (initial, fallback, amlodipine and losartan followups); the conditional 'if dynamic LVOT obstruction, resting or provocable, is present' is consistent across them, and the exam does carry the Valsalva-augmented murmur. Criterion action-7 evidence (afterload reduction worsening dynamic outflow obstruction) still served. perfect_agent.py -v passes; test_case_guards.py -k (64 tests for the 8 SYNC-CARD pass-4 cases) passes. Nothing changed.
