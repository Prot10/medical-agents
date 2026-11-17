# SYNC-CARD-RP02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-8-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:SYNC-CARD-RP02:policy_verdict | FIXED | Diagnosis: the label now reads 'a right ventricular outflow tract mass most consistent with myxoma (histology pending)'; the must to send the excised mass for histology is kept and R0 already said 'most likely a myxoma'. Exercise test: already labelled harm (avoided_actions[5]); the exercise echocardiogram is now labelled harm too (avoided_actions[7]). Tilt: kept as harm, not changed to waste. Reason: Tilt part DECLINED: the note allows a harm label when the preload risk is justified separately, and avoided_actions[4] does so (head-up tilt lowers preload across a severe dynamic RV outflow obstruction from a mobile mass and can provoke collapse; ESC 2018; plan D19). (ground_truth.diagnosis.accepted[0]) |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B consistency | minor | ground_truth.avoided_actions[6..8] | Served off-pathway reports without a label (class C3): bubble study waste [6], exercise echo harm like the exercise test [7], coronary CTA (fallback) waste [8]. TEE, chest CTA and both FDG-PETs stay unlabelled (plan D27) | FIXED |
| D leakage | minor | fallback_tool_outputs.tissue_diagnosis | An `obtain_tissue_diagnosis` order is answered with the resection histology (cardiac myxoma, completely excised), so an agent that orders the excision as a diagnostic act gets definite histology. This follows the October library decision (LIBRARY-group3, RP02 resection; resection is a callable diagnostic act, as in glioma) and the must to send the excised mass for histology; no change. Noted for the lead | FLAGGED |

## Changes
The diagnosis label now reads 'a right ventricular outflow tract mass most consistent with myxoma (histology pending)', as R2 asked; the must to send the excised mass for histology is unchanged. The exercise test was already labelled harmful; the exercise echocardiogram, served if ordered, is now labelled harmful too, and the bubble study and coronary CT angiography as waste. The tilt test stays labelled harmful (its rationale already justifies the preload risk across the dynamic obstruction), so the request to call it low-yield instead was declined. 

Checks: perfect_agent.py -v ok; every new label and alternative probed through NeuroBenchEnvironment (each order is served the case's own report and matches only its intended criterion or avoided entry); test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases. No MRI touched.

## Verification
Pass 1: 0 errors found
- Checked accepted[0] against R2's wording and the rest of the case (R0 'most likely a myxoma', KCE[3] and the MRI impression 'most consistent with a myxoma; histological confirmation required', sarcoma/thrombus differential low with histology required); the new labels against the stored reports (bubble study, exercise echo not performed, CTA fallback with normal coronaries); the tilt DECLINED part rests on the existing preload rationale (plan D19). DiagnosisCriterion.matches: 'RVOT mass most consistent with myxoma, histology pending' scores. The worker's flag on the tissue fallback (resection histology served if ordered) stands for the lead.
- Re-checked: perfect_agent.py -v ok (each criterion receives the report carrying its expected evidence; no avoided entry matches a criterion call); test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Nothing changed after pass 1 (0 errors), so no field needed re-verification. Re-ran perfect_agent.py -v: ok; test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed.
Cosmetic (not counted): none.
