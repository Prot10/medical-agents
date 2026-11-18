# VASC-DEM-S10

## Reviewer notes
Reviewer status: R1 in_progress, no R2 | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 4bc866bf-172d-435a-9dff-658aa4b6b7db | FIXED (plan C2, D2) | ground_truth.action_criteria[action-5-order-specialized-test].importance required -> recommended; removed from stop_rule.required_before_assessment (now screen, labs, MRI); label "...to characterise the executive-versus-amnestic profile..."; rationale "Characterises the dysexecutive and initiation deficit and sets a baseline for rehabilitation and follow-up; the screen with the apathy and depression scales, the informant history and the MRI establish the disorder [VASCOG_2014]" |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | initial_tool_outputs.specialized_test.findings | Plan C6: RAVLT delayed recall 20th flagged 'yes' against 25th-75th | FIXED: AACN ranges on percentile rows; 20th "low average" (impression does not mention it; unchanged) |
| C | minor | ground_truth.differential[Subcortical ischaemic VaD].key_features | "does not reach the threshold at which small-vessel disease alone explains a dementia": Fazekas 2 with a lacune is in fact supportive imaging under VasCog-2-WSO | FIXED: the burden and the putaminal lacune contribute, but the abrupt onset with the genu infarct without prior decline points to the strategic infarct [VasCog2_WSO_2025] (kce4 kept, plan C8) |
| C | minor | ground_truth.avoided_actions | Plan C11: stored perfusion SPECT, levodopa challenge and DTI unlabelled | FIXED: avoid-waste-perfusion-spect, avoid-waste-levodopa-challenge, avoid-waste-dti-tractography; gait and speech stay unlabelled; TEE already covered by the echo waste label |

## Changes
The diagnosis (strategic capsular genu infarct dementia) and the screen, labs and MRI requirements are unchanged. The formal neuropsychological battery is now recommended rather than required and no longer has to be done before the diagnosis: the documented stroke, the abulia, the screen with apathy and depression scales and the loss of independence establish it, while the battery documents the profile and sets a baseline. The subcortical-ischaemic differential no longer claims a burden threshold: the Fazekas 2 change contributes, but the abrupt onset with the genu infarct points to the strategic mechanism. Perfusion SPECT, levodopa challenge and DTI are now labelled waste; the battery's delayed recall (20th percentile) is labelled low average. Checks: perfect_agent.py passes; test_case_guards for the case passes; case_io check: schema and synonym guard OK, no test failure names the case. No MRI edited.

## Verification
Pass 1: 0 errors found
- Checked: 4bc866bf FIXED (battery recommended, stop rule screen, labs, MRI). SPECT, levodopa and DTI labelled; TEE covered by the existing echo wildcard label; gait and speech unlabelled. Battery 20th low average; MoCA items add to 21; SVD differential follows D8, kce4 kept per plan. perfect_agent ok; case_io check and test_case_guards pass.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Checked: 4bc866bf FIXED (battery recommended, stop rule screen, labs, MRI). MoCA losses add to 21; RAVLT 20th low average; SPECT, levodopa and DTI waste, TEE covered by the existing echo wildcard, gait and speech unlabelled; kce4 kept per plan C8. perfect_agent ok; test_case_guards -k S10 pass.
Cosmetic (not counted): none.
