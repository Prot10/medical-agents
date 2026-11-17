# MIG-AURA-P04

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| fb7dfc9b-e854-4997-8c0d-06048606fb95 | FIXED (class LIT, commit 393c547e) | Literature step removed by the class; re-checked: no `search_medical_literature` string left. |
| 95362414-55a8-4d22-a952-f0b1b27ea2ad | FIXED (plan D16) | `followup_outputs[0].output` (`genetic_panel:CADASIL`): findings, quantitative_data and impression rewritten as targeted Sanger testing of NOTCH3 exon 4 for the familial c.457C>T p.(Arg153Cys), not detected, after pre-test counselling and consent; no exon 2-24 sequencing or CNV. `ground_truth.action_criteria[2]` (`action-5-order-specialized-test`): required -> recommended; label, expected_evidence ("targeted"), rationale (offered after counselling, she may decline) and citation `[EAN_CADASIL_2020]`; removed from `ground_truth.stop_rule.required_before_assessment`. `ground_truth.action_criteria[1]` (`action-4-analyze-brain-mri`): recommended -> required, rationale rewritten, citation `[EAN_CADASIL_2020]`; stop rule now assessment + MRI review. `ground_truth.assessment.required_recommendations[1]` and `[2]` made conditional on her choice to test; `[0]` (counselling, option not to test) unchanged. Class extension: `ground_truth.key_clinical_evidence[2]`, `ground_truth.differential[0].key_features`, `ground_truth.red_herrings[0].correct_interpretation`, `metadata.condition_name`, `metadata.difficulty_description` no longer mention exon 2-24 sequencing or imposed testing. Label kept (plan D16: the stored targeted result supports "CADASIL excluded by NOTCH3 testing"). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | initial_tool_outputs.drug_interactions.sumatriptan.interactions[1] | Gave the 200 mg/day topiramate threshold without the FSRH caution (class TOPI-CONTRA, plan D3). Now keeps the 200 mg/day evidence and adds that FSRH advises treating topiramate as a potential enzyme inducer at any dose. | FIXED |
| E | minor | metadata.case_body_concerns | Authoring-process text in metadata (condition-wide generated line). | FLAGGED |
| B | minor | ground_truth.red_herrings[2].correct_interpretation | Presumed a negative test she may decline; made conditional on her choice to test (verification pass 1). | FIXED |

## Changes
NOTCH3 testing is no longer imposed or comprehensive. The stored genetic report is now targeted Sanger testing of NOTCH3 exon 4 for the aunt's known familial variant c.457C>T p.(Arg153Cys), done after pre-test counselling and consent, with the variant not detected and a note that the rest of the gene was not analysed; full exon 2-24 sequencing and copy-number analysis are gone. The test moved from required to recommended (offered after counselling; she may decline) and left the stop rule, while the formal review of her outside MRI moved from recommended to required and joins the stop rule, since the MRI pattern answers the family-history red flag without depending on her decision to test. The musts explaining the result and the family implications are now conditional: the MRI shows no CADASIL pattern, and if she chooses testing, absence of the familial variant excludes CADASIL in her and means she cannot pass it on; her mother remains at risk and can be referred to clinical genetics. Key evidence item 3, the CADASIL differential, the aunt red herring and the metadata texts now say "targeted". In the drug check, the topiramate-desogestrel interaction adds the FSRH any-dose enzyme-induction caution. Literature step removed earlier by class LIT; the diagnosis label is unchanged.

## Verification
perfect_agent.py MIG-AURA-P04 -v: ok. test_case_guards (-k my six ids): 48 passed. case_io.py check: schema OK, synonym guard OK, no failure names this case (the only condition failure is test_no_review_process_text[MIG-AURA-P05], another worker's case).
Pass 1: 1 errors found
- ground_truth.red_herrings[2].correct_interpretation still said "the patient's own negative test answers her question", presuming the test the note says must be offered, not imposed (the worker made red_herrings[0] and the musts conditional but not this field). Now "if she chooses testing, her own result for the familial variant answers her question". Rulings file updated.
- Re-run after the fix: perfect_agent ok; test_case_guards -k 48 passed; case_io check: no failure names this case.
Pass 2: 0 errors found
- Checked: NOTCH3 report is targeted exon 4 Sanger for c.457C>T p.(Arg153Cys) (R153 is in exon 4), not detected, no exon 2-24 or CNV text; test recommended and out of the stop rule; MRI required and in it; REQ1, REQ2, KCE[2], differential[0], red_herrings[0,2] and metadata conditional on her choice; topiramate caution added; label kept per plan D16.
- Re-checked by pass 2: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed; case_io check: schema OK, synonym guard OK, no test failure names this case.
Pass 3: 0 errors found
- Checked: every note ruled and the ruling holds; diff read and final case read in full; no contradiction, leakage, template carry-over or em dash in new text found; no literature string left.
- Re-checked by pass 3: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed. Variant c.457C>T p.(Arg153Cys) confirmed codon 153 (exon 4).
Pass 4: 0 errors found
- Checked: both notes ruled; NOTCH3 report targeted (c.457C>T is codon 153, CGC>TGC Arg>Cys, exon 4), test recommended and out of the stop rule, MRI required and in it, musts and red herrings conditional on her choice; final case read in full; no leakage.
- Re-run by pass 4: perfect_agent.py -v ok; mri_probe: every order gets the case report; test_case_guards -k (six ids) 48 passed; case_io check: no test failure names this case.
Condition audit (MIG-AURA auditor, 17 Nov 2026): 1 error found
- D/leak, E (own finding, present at base): patient.clinical_history.medications[1].indication read "Contraception — appropriate in migraine with aura", which names the case's diagnosis at turn 0 (format_patient_info prints medication indications) and adds a judgement that is not an indication. FIXED: "Contraception". No ruling changes. perfect_agent passes; test_case_guards -k passes.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Checked the condition-audit changes: patient.clinical_history.medications[1].indication is 'Contraception' (accurate; no judgement text); metadata.case_body_concerns empty. perfect_agent.py -v ok; test_case_guards -k (eight ids) 64 passed.
