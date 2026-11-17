# SYNC-CARD-RP01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-8-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:SYNC-CARD-RP01:policy_verdict | NO-ACTION | Approval of every dimension; nothing asked. Class defects of this approved case were fixed separately (driving interval after an ICD, waste labels for served EPS, bubble study and TEE). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.assessment.required_recommendations[8] | Driving after the ICD read '3 months after ICD implantation (ESC 2018, Group 1)': the ESC 2018 Practical Instructions give Group 1 after 1 month for any ICD; 3 months is EHRA 2009 for secondary prevention, and this ICD is for arrhythmic syncope with NSVT (plan C5, DR-ICD1). Now the canonical DR-ICD1 text | FIXED |
| B consistency | minor | ground_truth.avoided_actions[5..7] | Served off-pathway reports without a label (class C3): electrophysiology study (fallback), bubble study, TEE (fallback). Now waste: avoid-waste-electrophysiology-study [5], avoid-waste-bubble-study [6], avoid-waste-tee [7]. The exercise echo stays unlabelled (exercise testing is an optional criterion here, plan D4) | FIXED |

Approved case (R2): changed only for these two class defects, both additive or a source correction.

## Changes
Approved case, changed only for class defects. The driving advice after the ICD now follows the ESC 2018 Practical Instructions (Group 1 may resume 1 month after implantation, longer after an appropriate shock; Group 2 permanently restricted); the previous '3 months (ESC 2018)' was the EHRA 2009 secondary-prevention figure under the wrong source. The electrophysiology study, bubble study and TEE reports that are served if ordered are now labelled as waste. No clinical text, criterion, differential or report changed. 

Checks: perfect_agent.py -v ok; every new label and alternative probed through NeuroBenchEnvironment (each order is served the case's own report and matches only its intended criterion or avoided entry); test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases. No MRI touched.

## Verification
Pass 1: 0 errors found
- Checked the one note (NO-ACTION, approval), the DR-ICD1 driving text (ICD for arrhythmic syncope with NSVT, not sustained VT, so 1 month is right) and the three new waste labels against the stored EPS (fallback), bubble study and TEE (fallback) reports; exercise echo correctly left unlabelled (exercise optional, plan D4). No contradiction with the musts, prohibitions or differential.
- Re-checked: perfect_agent.py -v ok (each criterion receives the report carrying its expected evidence; no avoided entry matches a criterion call); test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Nothing changed after pass 1 (0 errors), so no field needed re-verification. Re-ran perfect_agent.py -v: ok; test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed.
Cosmetic (not counted): none.
- Condition auditor, 17 Nov 2026, blind leak pass: a check_drug_interactions output (served to any drug query, including a first call before any test) quoted the labs result that action-2-interpret-labs orders and cites as expected evidence ("Serum magnesium 4.4 mg/dL on infusion", initial, fallback and magnesium follow-up; "creatinine 0.7 mg/dL" in the magnesium follow-up). Now "Check serum magnesium on the infusion" and "check creatinine during the infusion"; toxicity thresholds kept. Approved case: changed for a real leak only. perfect_agent, test_case_guards -k, case_io check clean.
Pass 4: 0 errors found
- Verified the condition-audit leak fix: no magnesium or creatinine value left in the initial, fallback or magnesium-sulfate followup outputs ('Check serum magnesium on the infusion', 'check creatinine during the infusion'); toxicity thresholds (reflex loss about 8-10 mg/dL, respiratory depression above about 12 mg/dL) are correct. Beta-blocker criterion evidence (LactMed, hypotension with the infusion) still served. perfect_agent.py -v passes; test_case_guards.py -k (64 tests for the 8 SYNC-CARD pass-4 cases) passes. Nothing changed.
