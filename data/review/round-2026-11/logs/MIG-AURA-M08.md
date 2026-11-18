# MIG-AURA-M08

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| ce7ba35d-c709-4648-a063-28ea4c569aa8 | FIXED (class LIT, commit 393c547e) | Literature step removed by the class; re-checked: no `search_medical_literature` string left. |
| 034920f8-3d5e-42c8-89cf-894305c9a7a7 | FIXED (plan D9; label change) | `ground_truth.diagnosis.accepted[0]` -> "Migraine with visual and somatosensory aura (ICHD-3 1.2.1), onset after starting sertraline (causal role uncertain); sertraline-sumatriptan co-administration acceptable with counselling". `ground_truth.assessment.required_recommendations[3]`, `ground_truth.key_clinical_evidence[1]` and `ground_truth.red_herrings[0].correct_interpretation` reworded: temporal association, not causation; family history suggests susceptibility; earlier flashes too poorly characterised to count as aura; continue sertraline if helping, contribution uncertain, changes agreed with her prescriber. Class extension: `metadata.difficulty_description`, `metadata.difficulty_rationale` and `patient.pmh[3]` carried the same overstatement (see Own findings). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | metadata.difficulty_description, metadata.difficulty_rationale | Repeated the "predisposition predates the SSRI" / "genetic predisposition vs SSRI causation" framing that note 034920f8 rejects (metadata is shown to physicians). Reworded to an association of uncertain causal weight. | FIXED |
| B | minor | patient.pmh[3] | "Prior 2-3 years of brief monocular visual flashes" stated monocularity as fact, while the clinical assessment says it was never checked. Now "Brief visual flashes over the past 2-3 years, attributed by her to one eye (never assessed)". | FIXED |
| E | minor | metadata.case_body_concerns | Authoring-process text in metadata (condition-wide generated line). | FLAGGED |

## Changes
The diagnosis label no longer attributes the migraine to sertraline: it reads "Migraine with visual and somatosensory aura (ICHD-3 1.2.1), onset after starting sertraline (causal role uncertain); sertraline-sumatriptan co-administration acceptable with counselling" (label change, same entity and codes; synonyms untouched). The must answering her sertraline question, key evidence item 2 and the sertraline red-herring interpretation now say that onset two weeks after starting sertraline is a temporal association that does not establish cause, that the father's and sister's migraine suggest susceptibility, that the earlier flashes she attributed to one eye are too poorly characterised to count as aura, and that sertraline can be continued if the depression is responding while its contribution stays uncertain, with any change agreed with her prescriber. The past-history line no longer calls those flashes monocular as a fact, and the metadata difficulty texts were aligned. Literature step removed earlier by class LIT. Tool outputs, criteria, tiers and stop rule are unchanged.

## Verification
perfect_agent.py MIG-AURA-M08 -v: ok. test_case_guards (-k my six ids): 48 passed. case_io.py check: schema OK, synonym guard OK, no failure names this case (the only condition failure is test_no_review_process_text[MIG-AURA-P05], another worker's case).
Pass 1: 0 errors found
- Checked: label, sertraline must, KCE[1], red_herrings[0], difficulty texts and pmh[3] now state association, not causation, consistently with the HPI and the clinical assessment; no residual 'unmasked' or 'predates' text. perfect_agent -v ok; test_case_guards -k 48 passed; case_io check clean for this case.
Pass 2: 0 errors found
- Checked: label, REQ3, KCE[1], red_herrings[0], pmh[3] and metadata state association, not causation, consistent with the HPI and clinical assessment findings[0]; laterality (right field and right lips, left headache) and medication timeline consistent; no literature string left.
- Re-checked by pass 2: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed; case_io check: schema OK, synonym guard OK, no test failure names this case.
Pass 3: 0 errors found
- Checked: every note ruled and the ruling holds; diff read and final case read in full; no contradiction, leakage, template carry-over or em dash in new text found; no literature string left.
- Re-checked by pass 3: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed.
Pass 4: 0 errors found
- Checked: both notes ruled; label, REQ3, KCE[1], red_herrings[0], pmh[3] and metadata state association, not causation, and agree with the HPI and clinical assessment; final case read in full; no leakage or literature string.
- Re-run by pass 4: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed; case_io check: no test failure names this case.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Checked the only change after the last clean pass: metadata.case_body_concerns deletion (condition audit) checked against git diff 06b74446: only the generation-pipeline line was removed, the field is [] and no other field changed with it.
- perfect_agent.py -v ok; test_case_guards -k (M01..M08) 64 passed.
Cosmetic (not counted): none.
