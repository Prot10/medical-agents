# SYNC-CARD-M04

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split followup_outputs[6] (analyze_brain_mri, trigger request_brain_mri, an unflagged report whose only gadolinium content was negative enhancement statements) into the plain study (contrast_used false, same slot and trigger) and the unchanged gadolinium study (contrast_used true, trigger request_brain_mri_with_contrast, right after it). Plain copy: observation 'No mass, hemorrhage, or enhancing lesion' -> 'No mass or hemorrhage' (impression had no gadolinium content); white matter, DWI and volume findings kept. The case has no brain MRI criterion: the MRI is an off-pathway study scored by a waste avoided action with empty required_arguments (ESC 2018 Class III, brain imaging not indicated in syncope without focal signs), which matches plain and contrast orders alike, so no criterion, evidence, stop rule or sequence constraint changed. Probe: plain order gets the plain copy (gad_text=n), contrast order the gadolinium study, either order, no library answer; perfect_agent passes. Case fallback MRI has no gadolinium content: unchanged, contrast_used null (decision 4). Chest CT body imaging is CT, not in scope of decision 5.
- MRI-CONTRAST verified: checked the plain copy free of gadolinium content and internally consistent, the gadolinium copy identical to the base report apart from contrast_used true, contrast_used per the decision (no stored gadolinium study left null), mri_probe (plain, contrast and both orders in either sequence answered by the case, never the library), pathway order sensible, nothing outside the MRI split changed versus 393c547e (programmatic diff), perfect_agent -v passes, case_io check clean for this case; no brain MRI criterion (waste avoided action with empty required_arguments, ESC 2018 Class III), so no criterion argument to set; case fallback MRI has no gadolinium content and stays null. No error found.

## Reviewer notes
Reviewer status: R2 needs_changes | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| f8a88107-9741-4c25-b2ee-f6c296f94b2d | FIXED | `ground_truth.avoided_actions[4]` (`avoid-harm-5-exercise-stress-test`, still harm): rationale replaced with the C2 text (uncontrolled symptomatic arrhythmia, recurrent torsades with QTc above 500 ms, Fletcher 2013; no gain now; recovery QTc after washout only if congenital LQTS remains in question, ESC 2022); citations `[Fletcher_2013]`, `[ESC_2022_VA_SCD]` (D9). |
| a607c6eb-88be-4ea0-b0cc-ecb51f3972e2 | FIXED (divergence recorded) | `ground_truth.assessment.required_recommendations[2]`: K at least 4.0 mmol/L, aiming for 4.5-5.0 while torsades is active (Drew 2010), AHA 2020 (Tisdale) K above 4.0 mEq/L, Mg above 2.0 mg/dL, hold the thiazide (D10). The labs criterion rationale does not repeat 4.5-5.0: unchanged. |
| 67b578e5-6650-4a37-bb15-7206e6930d4f | FIXED | New `ground_truth.assessment.required_recommendations[6]` (depression plan with a lower-QT-liability antidepressant such as sertraline, psychiatric follow-up); former R6-R8 now R7-R9 (D11). |
| NB-87M:SYNC-CARD-M04:policy_verdict | NO-ACTION | No comment; substance in the three notes above (D26). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | `ground_truth.avoided_actions[5]` (new `avoid-harm-exercise-echo`) | Class C3: the fallback exercise echo answered an order with no label, while the exercise test is harm | FIXED (harm, the C2 rationale naming the echo; citations Fletcher 2013, ESC 2022) |
| C | minor | `followup_outputs[9]` (chest CT) | Unlabelled served report | no change (plan D27: left unlabelled) |
| A | minor | `followup_outputs` order | Drug checks first: correct here, since the medication review is the diagnostic step in drug-induced torsades (ROUND_POLICY ruling 6) | no change |
| E | minor | `metadata.revision_reason`, `metadata.last_revised` | Updated | FIXED |

## Changes
The exercise test remains labelled harmful, now for the right reason: recurrent torsades with a QTc above 500 ms is an uncontrolled symptomatic arrhythmia, an absolute contraindication (Fletcher 2013), and the test adds nothing to the diagnosis now; the text adds that after drug washout the recovery QTc of an exercise test can help if congenital long QT remains in question (ESC 2022). The old reason (adrenergic stress provoking torsades), which contradicted the isoproterenol must, is gone. An exercise echo order is labelled harmful in the same way. The potassium must records both sources: at least 4.0 mmol/L, aiming for 4.5-5.0 mmol/L while torsades is active (Drew 2010; AHA 2020 asks for K above 4.0 mEq/L), with magnesium above 2.0 mg/dL. A new must covers the depression: once the QTc has normalised, an antidepressant of lower QT liability (for example sertraline) with psychiatric follow-up.

CENTRAL: C2 key `[AHA_2020_DrugArrhythmia]` (Tisdale 2020); C3 pack text (torsades potassium divergence, D10).

## Verification
Pass 1: 0 errors found
- Checked the C2 harm rationale (no adrenergic-provocation reason left; consistent with the isoproterenol must and QTc 520-545 ms), the K/Mg must with both sources, the new depression must, and the harm label on the fallback exercise echo ("not performed" report); perfect_agent -v and test_case_guards pass.
Pass 2: 0 errors found
- Focused verifier: no change was made after Pass 1 (0 errors), so nothing was left unverified. Re-ran perfect_agent -v and test_case_guards: both pass.
