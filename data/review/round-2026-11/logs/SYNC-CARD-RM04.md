# SYNC-CARD-RM04

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-7-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general; removed fallback literature_search output. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split the stored brain MRI (followup request_brain_mri, off-pathway, no MRI criterion) into a plain copy (contrast_used false, original slot; removed "No enhancing lesion") and the unchanged gadolinium study (contrast_used true, trigger request_brain_mri_with_contrast, placed right after it). No criterion changed: brain MRI is not indicated in syncope without focal signs (ESC 2018, Class III), so no gadolinium question exists. Case fallback MRI has no gadolinium content, left null.
- MRI-CONTRAST verified: plain copy free of gadolinium content with impression consistent with findings, gadolinium copy unchanged (contrast_used true) right after it, no MRI criterion (syncope, gadolinium not indicated); mri_probe: plain, contrast and both orders in either sequence answered by the case (never the library), case fallback MRI consistent; no other field changed against 393c547e; perfect_agent -v passes. No error found in the case; removed the two duplicate copies of the worker's MRI-CONTRAST log line.

## Reviewer notes
Reviewer status: R2 approved (all dimensions) | Approved before this round: yes

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-RM04:policy_verdict | NO-ACTION | Approval without comment. Only the class defects below were fixed (plan C3, D3, D4). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.avoided_actions (new avoid-waste-bubble-study) | A stored bubble study (followup_outputs[14]) answered an unlabelled order (class C3). The canonical "no unexplained hypoxaemia" text was adapted, because her hypoxaemia is explained by the emboli. | FIXED: waste. |
| C | minor | ground_truth.avoided_actions (new avoid-harm-exercise-echo) | A stored exercise echo (followup_outputs[15]) answered an unlabelled order, while the exercise test is already harm (acute PE with RV dysfunction, Fletcher 2013; D4). | FIXED: harm, [Fletcher_2013], with the exercise test's wording. |
| C | minor | ground_truth.avoided_actions (new avoid-waste-chest-ct) | A stored non-contrast chest CT (followup_outputs[9]) answered an unlabelled order (class C3). | FIXED: waste on {order_body_imaging, study chest_CT}. Checked: it matches chest_CT with and without contrast and never the CTPA criterion (study chest_CTA), and no call hits two entries. The rationale holds in either order, so it does not assume the CTPA came first. |
| C | minor | ground_truth.avoided_actions (new avoid-waste-tee) | The case fallback echo is a TEE and the order was unlabelled (class C3). | FIXED: waste. |
| A | major | ground_truth.action_criteria[4].alternatives[0].required_arguments (action-4-order-body-imaging) | The required CTPA criterion needed {study chest_CTA, contrast true}. The tool's contrast argument defaults to false, so a correct order {study chest_CTA} was answered with the CTPA but scored as missing the required step. It was the only chest_CTA criterion in the dataset that asked for the flag (FEPI-TEMP-RP02 and SYNC-CARD-RM01 do not). | FIXED: required_arguments {study chest_CTA}. A CT angiogram is a contrast study by definition. Probed: chest_CTA with contrast true, false or absent now credits the criterion. |
| D | minor | initial_tool_outputs.labs (D-dimer 8.4 mg/L FEU in the summary and interpretation) | The lab result served for the troponin/BNP/beta-hCG order also reports a D-dimer, which the case labels waste (avoid-waste-6-d-dimer). So the agent sees a result it was told not to order. | FLAGGED for the lead (neurobench-case-serving class); not changed in this approved case. |
| B | minor | followup_outputs[9] (chest CT) | A chest_CT order with contrast true is answered by the stored non-contrast report. | FLAGGED (serving detail, harmless now that the order is labelled waste). |

## Changes
Approved case, changed only for real class defects. No clinical text changed. Four avoided actions were added for test reports the case already serves but had not labelled. A bubble study is waste: no stroke or shunt question, and the hypoxaemia is explained by the emboli. An exercise echo is harmful, like the exercise test: acute PE with RV dysfunction is an absolute contraindication. A chest CT that is not a pulmonary angiogram is waste because it cannot show the emboli. A transoesophageal echo is waste. The required CT pulmonary angiography step now accepts any chest CTA order. Before, an order without an explicit contrast flag was answered with the angiogram but not credited. The perfect-agent check passes.

## Verification
perfect_agent.py -v passes (each criterion receives the stored report carrying its expected evidence); case_io.py check: schema OK, synonym guard OK, no test failure names the case; test_case_guards.py -k <id> passes.

Pass 1: 0 errors found
- Checked: approval NO-ACTION; four additive labels per plan C3 (exercise echo harm like the exercise test; chest_CT entry does not match the chest_CTA criterion); the CTPA criterion fix is real (policy_reward fills the schema default contrast false, so {study chest_CTA, contrast true} missed a plain chest_CTA order); perfect_agent -v, test_case_guards -k and case_io check.
- Cosmetic (not counted): avoid-waste-chest-ct rationale "cannot assess the pulmonary arteries" -> "is not adequate to assess the pulmonary arteries" (a contrast chest CT can show central emboli but is not a diagnostic PE study).

Pass 2: 0 errors found
- Pass 1 found 0 errors and no condition-audit or orchestrator change follows it, so nothing was left unverified. Re-ran perfect_agent.py -v (passes) and test_case_guards.py -k (passes). Nothing changed.
Pass 4: 0 errors found
- No change after the last 0-error pass. perfect_agent.py -v passes; test_case_guards.py -k (64 tests for the 8 SYNC-CARD pass-4 cases) passes. Nothing changed.
