# FND-S01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress, no R2 note | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| c8b24f69-26eb-411e-8eb7-681163c62d96 | FIXED | The literature-search step this note rejected was removed from the case by class LIT (commit 393c547e); checked: no literature criterion, follow-up, initial or fallback literature output remains. (whole case) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.action_criteria[action-ecg]; ground_truth.stop_rule; initial_tool_outputs.ecg; fallback_tool_outputs.ecg; metadata.fallback_tool_kinds | Plan class ECG (from note f4d98130 on M01): events during which she sometimes cannot respond are apparent TLoC, for which NICE CG109 1.1.2.2 advises a 12-lead ECG for everyone; the criterion was optional and was answered only by the shared template fallback "Normal ECG" (rate 66 against a vitals HR of 86). | FIXED: required, in the stop rule, citation [NICE_CG109] only (NG217 dropped: the canonical rationale rests on CG109), canonical rationale; case-specific stored ECG (sinus 86/min, PR 164, QRS 88, QTc 432 ms on sertraline); template fallback nulled and its fallback_tool_kinds key removed |
| C | major | ground_truth.action_criteria[action-5-analyze-eeg] | Plan class VEEG: a typical event was witnessed on examination, so video-EEG is recommended, not optional; the October sentence "Without the recording ... (LaFrance 2013)" was still in the rationale. | FIXED: recommended; canonical recommended rationale after the case sentence on the daily events |
| A | minor | ground_truth.action_criteria order; followup_outputs order | Plan 2.ORDER. | FIXED: exam, ECG, brain MRI (optional), video-EEG, drug check, neuropsychology; neuropsychology answer before the on-request performance status |
| E | minor | metadata.difficulty_rationale; metadata.revision_reason | Called the examination the only required work-up. | FIXED |

## Changes
S01 stays the reference case of the S series and is not rewritten. The literature step is gone (class LIT). A 12-lead ECG is now required and part of the stop rule, because her events include apparent loss of responsiveness (NICE CG109: a 12-lead ECG for everyone with transient loss of consciousness); it returns a case-specific normal ECG (sinus 86/min matching the vitals, normal PR, QRS and QTc 432 ms) instead of the shared template. Video-EEG is now recommended rather than optional, because a typical event was witnessed on the ward (ILAE 2013; AAN 2025). Criteria and follow-ups are reordered to the condition order. Musts, prohibitions, differential, reports and patient text are unchanged.

## Verification
perfect_agent.py -v: ok (ECG receives initial_tool_outputs.ecg, video-EEG receives initial_tool_outputs.eeg). No MRI touched.
test_case_guards -k (six cases): 48 passed. case_io.py check: schema and synonym guard OK; the only failure naming the condition is test_library_never_answers_a_contradicted_order[FND-RS02], not this case.
Pass 1: 0 errors found
- Checked: LIT ruling; class ECG (required, in the stop rule, canonical rationale, [NICE_CG109], rate 86 = vitals HR, template fallback nulled and its fallback_tool_kinds key removed); class VEEG recommended with canonical text; no other clinical content changed. perfect_agent.py -v ok; test_case_guards -k 48 passed.
- Cosmetic (not counted): initial_tool_outputs.ecg.intervals.QT 362 -> 361 ms, so that Bazett at 86/min gives the stated QTc 432 ms (362 ms gives 433 ms).
Pass 2: 0 errors found
- Checked: every note id ruled (rulings file and log agree); class rulings per plan (RS03: VEEG recommended, new recommended ECG with a case ECG at the vitals rate, QTc arithmetic correct; RS04: MRI {contrast: false} required and in the stop rule, canonical ACUTE rationale and citations, VEEG recommended, no ECG; S01: ECG required and in the stop rule, case ECG at the vitals rate, VEEG recommended); KCE, red herrings, differential and metadata consistent with the new tiers; stop rule ids are required criteria; no literature left; no leakage; no em dashes in new text. perfect_agent.py -v ok (served reports probed for the "?" rows: the case's own exam and MRI); test_case_guards -k (six cases) 48 passed.
Pass 3: 0 errors found
- Checked: LIT ruling; ECG required and in the stop rule with canonical rationale, case ECG at 86/min = vitals HR, Bazett 361 ms -> 432 ms; VEEG recommended with canonical text; M-DX keeps "where recorded"; template fallback ECG gone; no leakage, no template carry-over, no em dashes in new text. perfect_agent.py -v ok; test_case_guards -k (six cases) 48 passed; case_io.py check: only the FND-RS02 library-contradiction failure, not this case.
Pass 4: 0 errors found
- Checked: LIT ruling; ECG required and in the stop rule with the canonical rationale (she cannot respond during some events), case ECG at 86/min = vitals HR, Bazett 361 ms -> 432 ms, template fallback ECG nulled and no ecg key left in fallback_tool_kinds; there was never an ECG avoided action (base list starts at avoid-waste-2); VEEG recommended with canonical text; M-DX keeps "where recorded"; no leakage. perfect_agent.py -v ok; test_case_guards -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only failure naming the condition is test_library_never_answers_a_contradicted_order[FND-RS02], not this case.
Condition audit (17 Nov 2026), class template carry-over (ROUND_POLICY, realism: identical numbers across cases), minor: the neuropsychology battery (`followup_outputs[request_neuropsych_battery]`) carried the cognitive values MoCA 28/30, RAVLT delayed recall z = -0.2, Trail Making B z = -0.4 and TOMM trial 2 49/50, identical in 22 FND cases (raised by the FND-M01 verifier). FIXED with case-plausible values, all in the normal range (28, paralegal): MoCA 29/30, RAVLT delayed recall z = 0.1, Trail Making B z = -0.3, TOMM trial 2 50/50 (above the 45 cut-off), in `quantitative_data` and in the matching findings. The impression (cognition within normal limits, performance validity passed), the mood, anxiety and dissociation scores, the optional tier and the rulings are unchanged. No other field cites these numbers. perfect_agent.py FND-S01 passes.
Pass 5: 0 errors found
- Verified the condition-audit change only (neuropsychology battery numbers): MoCA 29/30, RAVLT delayed recall z = 0.1, Trail Making B z = -0.3, TOMM trial 2 50/50 in quantitative_data match the MoCA and TOMM findings rows; all values are in the normal range (MoCA >= 26, z > -1, TOMM above the 45 cut-off), so they agree with the impression (cognition within normal limits, performance validity passed); no other field of the case cites these numbers (grep MoCA, RAVLT, Trail, TOMM). perfect_agent.py -v ok; test_case_guards -k (eight cases) 64 passed.
