# MIG-AURA-P06

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 26305ba4-baa5-4ad9-b586-89a7ecee7994 | FIXED | Class LIT, commit 393c547e: the literature criterion and follow-up were removed; checked that the case contains no search_medical_literature criterion, follow-up or stored output. |
| 7e1924c9-0541-4646-95eb-1c55fd6282e8 | FIXED | The NOTCH3 report is now targeted Sanger testing of exon 4 for the familial c.544C>T p.(Arg182Cys) after counselling and consent (detected, heterozygous, pathogenic); the exon 2-24 sequencing is gone. The criterion (still required: he is symptomatic) is labelled 'Targeted NOTCH3 testing for the familial variant, after pre-test counselling and consent', its rationale reserves exon 2-24 sequencing for a negative result with strong suspicion, and a new first must requires pre-test counselling and consent, including the implications for his three children. Field: followup_outputs[0]. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| - | - | - | No other defect found on a full read; the triptan prohibition rests on the old putaminal lacune (label contraindication after cerebral infarction) and VASCERN 2023, and stays. | - |

## Changes
The NOTCH3 test is now targeted testing of the familial c.544C>T p.(Arg182Cys) variant (detected, pathogenic: CADASIL confirmed), with no exon 2-24 sequencing; the criterion stays required because he is symptomatic, and its rationale keeps full sequencing for a negative result with strong suspicion. A new first must asks for pre-test counselling and consent, including what the result means for his three adult children. The literature step had already been removed (class LIT). Nothing else changed.

## Verification
Pass 1: 0 errors found
Checked: both notes ruled; the NOTCH3 report is targeted (exon 4, familial c.544C>T), no exon 2-24 sequencing left anywhere; the counselling must agrees with the three adult children in the social history; no literature output left; perfect_agent and test_case_guards pass.
Pass 2: 0 errors found
Checked: every note ruled and applied as the plan states; no literature output; no contradiction found between labels, musts, prohibitions, differential, key evidence and reports; perfect_agent passes; test_case_guards -k passes.
Pass 3: 1 errors found
- C (class TIA-CERT, plan D4 rule 1): ground_truth.differential[0] (Transient ischaemic attack) listed "no acute infarct on MRI" as evidence against TIA; a normal MRI excludes infarction, not TIA. FIXED: "MRI shows no acute infarct, which excludes infarction but not TIA, so these clinical features decide."
Checked and correct: both notes ruled; targeted NOTCH3 report (exon 4, c.544C>T p.(Arg182Cys) is the correct cDNA position for R182C); counselling must agrees with the three adult children; no literature output; perfect_agent passes; case_io check and test_case_guards -k pass.
Pass 4: 0 errors found
Checked: every note ruled and applied as the plan states; no literature output; labels, musts, prohibitions, differential, key evidence, red herrings and reports agree; no answer leakage in the patient block; perfect_agent passes; case_io check (no failure names the case) and test_case_guards -k pass.
Condition audit (MIG-AURA auditor, 17 Nov 2026): 1 error found
- D/leak (own finding, TOOL_REPORT_STYLE_GUIDE check_drug_interactions: a drug check must not announce the patient's diagnosis): initial_tool_outputs.drug_interactions.sumatriptan.summary said 'triptans and ergots are avoided in CADASIL because they are vasoconstrictors', applying the label restriction to this patient as if the diagnosis (CADASIL, which at turn 0 is only his cousin's diagnosis and is established by the required NOTCH3 test) were already made. FIXED: 'if CADASIL is confirmed, triptans and ergots are not first-line acute treatment because they are vasoconstrictors' (VASCERN 2023 wording already in contraindications[0]). The interaction content and the criterion's expected evidence are unchanged; no ruling changes. perfect_agent passes.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Checked the condition-audit change: initial_tool_outputs.drug_interactions.sumatriptan.summary now conditional ('if CADASIL is confirmed ... not first-line'), matching contraindications[0] (VASCERN 2023), the criterion rationale and PRO (old lacune plus VASCERN); no diagnosis asserted at turn 0. metadata.case_body_concerns empty. perfect_agent.py -v ok; test_case_guards -k (eight ids) 64 passed.
- Cosmetic (not counted): action-2 expected_evidence and key_clinical_evidence say triptans are 'avoided in CADASIL', slightly firmer than the report's 'not first-line' (VASCERN); for this patient they are avoided anyway because of the old lacunar infarct (PRO).
