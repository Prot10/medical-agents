# VASC-DEM-P07

## Reviewer notes
Reviewer status: R1 in_progress, no R2 | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| ae5091af-b3b8-4ab6-b338-507704e63278 | FIXED (plan C1, D1) | action_criteria[action-4-perform-clinical-assessment] (gait_and_balance_timed): importance required -> recommended; rationale "...quantifies the subcortical gait disorder and the falls risk and gives supportive, education-independent evidence of executive dysfunction; the diagnosis does not depend on it [VASCOG_2014]." stop_rule.required_before_assessment: id removed; now screen, labs, MRI, battery (battery kept required, plan D2) |
| dc877a4d-76f1-4260-878d-ac41ac49efea | CENTRAL (plan D15) | Checked initial_tool_outputs.specialized_test.findings: "Estimated premorbid IQ (reading-based)" value 128, abnormal "no", reference_range "not applicable" (already what the note asks). The next row, FAQ 23/30, is "yes" and prints above its own label in the review app. No data change; display request CENTRAL item 2 |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | initial_tool_outputs.specialized_test.findings | Plan class C6 (D6): SDMT 22nd percentile flagged "yes" against a 25th-75th range | FIXED: percentile rows reference_range "9th percentile or above (25th-75th average)"; SDMT 22nd "low average"; Zoo Map 1st and TMT-B 8th stay "yes"; RAVLT 26th, recognition 58th, BNT 70th "no"; non-percentile rows (MET, WCST, IQ, FAQ) unchanged. Impression and expected_evidence do not cite the SDMT: unchanged |
| C | minor | ground_truth.avoided_actions | Plan class C11 (D12): stored SPECT, levodopa challenge and DTI follow-ups matched no criterion and no avoided action | FIXED: avoid-waste-perfusion-spect, avoid-waste-levodopa-challenge, avoid-waste-dti-tractography. TEE covered by the wildcard echo waste label. Credited follow-up (gait) already first |
| E | minor | initial_tool_outputs.specialized_test.findings[0,1]; key_clinical_evidence[1]; screen findings | Pre-existing em dashes in old text | FLAGGED: not churned (correct prose, no new text) |

## Changes
Major vascular cognitive disorder concealed by a normal MoCA in a high-baseline professional is unchanged, and the neuropsychological battery stays required and in the stop rule, because with a normal screen the executive battery against a premorbid IQ of 128 is the objective evidence of the deficit. Timed and dual-task gait testing is now recommended, not required, and out of the stop rule (screen, labs, MRI, battery): it supports the executive picture and measures falls risk but the diagnosis does not depend on it. The premorbid IQ row was already flagged 'no'; the 'yes' the reviewer saw belongs to the FAQ row printed above its label (display request sent centrally). SDMT at the 22nd percentile is low average (AACN 2020). Ordering the stored SPECT, levodopa challenge or DTI is labelled waste. Checks: perfect_agent.py passes; test_case_guards 48 passed for P03-P08; case_io check: schema and synonym guard OK, no test failure names the case. No MRI edited.

## Verification
Pass 1: 0 errors found
- Checked: ae5091af (gait recommended, out of the stop rule; battery stays required per D2), dc877a4d (premorbid IQ row already "no", CENTRAL display); C6 (SDMT 22nd low average, TMT-B 8th stays "yes"); C11 labels against the exam (no parkinsonian features). perfect_agent.py passes; test_case_guards 48 passed.
Pass 2: 0 errors found
- Checked: ae5091af (gait recommended, out of the stop rule; battery stays required per D2), dc877a4d (IQ 128 row already "no"; next row FAQ 23/30 "yes"; CENTRAL display); C6 (SDMT 22nd low average, TMT-B 8th yes); C11 (no parkinsonian features on exam; TEE covered by the echo wildcard); follow-up order. perfect_agent.py -v passes (each required and recommended criterion receives its stored report); test_case_guards -k P03-P08: 48 passed; case_io check: schema and synonym guard OK, no test failure names the case.
Pass 3: 1 errors found
- C, minor, ground_truth.avoided_actions[avoid-waste-levodopa-challenge].citations: [VASCOG_2014] does not address levodopa challenge testing, so it does not support the rationale (a case-specific statement that there is no parkinsonism to test). The plan table (C11) gives no citation for this label, and the same label is uncited in 14 other VASC-DEM cases (S01-S05, outside this batch, carry the same unsupported citation: for the lead); pass 2 removed the same kind of citation from the P06 tilt-table label. FIXED: citation removed, rationale unchanged.
- Checked otherwise: ae5091af (gait recommended, out of the stop rule; battery stays required per D2); dc877a4d (premorbid IQ 128 already "no"; next row FAQ 23/30 "yes"; CENTRAL display); C6 (SDMT 22nd low average; TMT-B 8th yes at the cut-off); C11. perfect_agent.py -v passes for P03-P08 (the criteria printed '<- ?' are served from the case's own initial outputs, which differ from the stored object only by null fields; none comes from a fallback or the library); test_case_guards -k P03-P08: 48 passed; case_io check: schema and synonym guard OK, no test failure names these cases.
Pass 4: 0 errors found
- Checked every note ruling against the plan and the final case (notes, musts, prohibitions, key evidence, red herrings, differential, stop rule, sequence ids, avoided actions vs criteria, C6 rows and impression, C11 labels, laterality, agent-visible text for leakage, new text for em dashes). perfect_agent.py -v passes for P03-P08 (each required and recommended criterion receives its stored report); test_case_guards -k P03-P08: 48 passed; case_io check: schema and synonym guard OK, no test failure names these cases.
