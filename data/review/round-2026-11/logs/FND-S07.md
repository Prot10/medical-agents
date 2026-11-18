# FND-S07

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed initial literature_search outputs: functional neurological disorder diagnosis treatment. Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress, no R2 note | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 4e4c7f64-6fae-43e4-8dc1-e953d459571f | FIXED | Class LIT, commit 393c547e; checked: no literature criterion or output left (whole case) |
| cd3460cf-ef35-47cb-a82f-388e448d2fb7 | FIXED | Class ACUTE: ground_truth.action_criteria[action-spine-mri] recommended -> required, canonical rationale (cord lesion) plus the cord-emergency sentence, citation [Espay_2018]; ground_truth.stop_rule.required_before_assessment += action-spine-mri. Brain MRI (action-4-analyze-brain-mri) stays optional |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| E | minor | metadata.difficulty_rationale; metadata.revision_reason; metadata.last_revised | Described the spine MRI as recommended. | FIXED |
| C | minor | ground_truth.avoided_actions[avoid-waste-1-analyze-ecg] | Checked per plan: ECG stays waste (no events, no TLoC). | no change |
| B | major | ground_truth.key_clinical_evidence[1] | Verifier pass 1: the KCE said the normal reflex, sensory and sphincter examination is "incompatible with an acute cord lesion", contradicting the now required spine MRI (positive signs do not exclude a coexisting cord lesion; Espay 2018). | FIXED: "argue strongly against an acute cord lesion but do not exclude one, so the cord is imaged" |

## Changes
The literature step is gone (class LIT). A spine MRI is now required and part of the stop rule with the examination, because an acute paraplegia of 24 hours must be imaged to exclude an acute cord lesion even with a bilateral Hoover sign and a normal reflex, sensory and sphincter examination (Espay 2018); the stored normal spine MRI answers it. The brain MRI stays optional, and criteria order, reports, patient text, differential, musts and prohibitions are unchanged.

## Verification
perfect_agent.py -v: ok (spine MRI served initial_tool_outputs.body_imaging, checked with a serving probe). test_case_guards -k FND-S07: pass. case_io.py check: no failure names FND-S07.
Pass 1: 1 errors found
- ACUTE class not propagated: KCE called the normal reflex, sensory and sphincter examination incompatible with an acute cord lesion, contradicting the required spine MRI; fixed (key_clinical_evidence[1]).
- Checked without change: note rulings correct; brain MRI optional, ECG waste (no events); spine MRI served from the case's own body_imaging report.
- Re-run after the fixes: perfect_agent.py -v ok; test_case_guards -k for the case: pass; case_io.py check: no failure names this case (the only condition-wide failure is test_library_never_answers_a_contradicted_order[FND-RS02], another case).
Cosmetic (not counted): none.
Pass 2: 1 errors found
- Sequence constraint reason contradicted the required spine MRI: the soft "examination before spine MRI" constraint said the examination's positive signs "decide whether imaging has a specific question to answer", while the spine MRI is now required whatever the examination shows (class ACUTE). Fixed: ground_truth.sequence_constraints[0].reason now "The examination comes first: it defines the deficit the imaging must explain and takes minutes, so it does not delay the spine MRI (Espay 2018)." (wording as in FND-M05). Constraint ids and severity unchanged.
- Checked without change: every note id has a correct ruling in the log and rulings file; tiers, stop rule (all required criteria, max 0) and criteria order match the plan; no literature criterion or output left; stored MRI served to the plain order (mri_probe, contrast_used null per MRI-CONTRAST decision 4); no patient-text leakage; no em dashes in new text.
- Re-run after the fix: perfect_agent.py -v ok; test_case_guards -k for the batch: 48 passed; case_io.py check: no failure names this case (only test_library_never_answers_a_contradicted_order[FND-RS02], another case).
Cosmetic (not counted): none.
Pass 3: 0 errors found
- Checked without change: note rulings correct (LIT; spine MRI required and in the stop rule, brain MRI optional, ECG waste with no events); stored spine MRI (cervical and thoracic to the conus) carries the criterion's expected evidence; KCE, differential and red herrings agree with the required cord imaging; bilateral Hoover description consistent; no leakage; no em dashes in new text.
- Re-run: perfect_agent.py -v ok (every required/recommended criterion served by the case's own data, none by the library or case fallback; mri_probe confirms the stored plain DWI study for the MRI orders); test_case_guards -k for the batch: 48 passed; case_io.py check: schema and synonym guard OK, no failure names this case (only test_library_never_answers_a_contradicted_order[FND-RS02], another case).
Cosmetic (not counted): none.
