# MIG-AURA-P01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| af4ad7e1-ff8f-4078-949b-0b2c4f6e8ff6 | FIXED (class LIT, commit 393c547e) | Literature step removed by the class; re-checked: no `search_medical_literature` string left. |
| b37e0b4d-6746-4f6c-a53c-ee0a63498852 | FIXED (plan D4) | `ground_truth.assessment.required_recommendations[1]` -> D4 aspirin-review must (stop if aura and no other indication; continue if TIA remains a real possibility; explain to patient and GP). `ground_truth.assessment.prohibited_recommendations[0]` (no antiplatelet/anticoagulant for presumed TIA) deleted; the list is now empty. `required_recommendations[0]` now says the clinical features favour aura and MRI/MRA exclude infarction and arterial disease but not TIA. `ground_truth.diagnosis.accepted[0]`: "after TIA exclusion" -> "TIA judged unlikely on the clinical features" (label change). `action-mra` (`ground_truth.action_criteria[2]`) recommended -> required, citation `[AHA_ASA_2021_secondary]`, rationale cites NICE NG128; added to `ground_truth.stop_rule.required_before_assessment`; new soft `ground_truth.sequence_constraints[1]` MRI before MRA. Class extension: `ground_truth.key_clinical_evidence[3]`, `ground_truth.red_herrings[0].correct_interpretation` and `ground_truth.red_herrings[2].correct_interpretation` (unconditional aspirin stop; normal imaging read as excluding TIA) reworded. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.key_clinical_evidence[3], ground_truth.red_herrings[2].correct_interpretation | Both said aspirin "should be stopped once aura is recognised", the unconditional stop the note rejects. Made conditional on the completed cerebrovascular evaluation. | FIXED |
| C | major | ground_truth.red_herrings[0].correct_interpretation | "with normal MRI and MRA they are aphasic aura ... its normal result points to migraine" implied imaging settles the TIA question. Now: imaging excludes infarction and arterial disease, not TIA; the distinction is clinical. | FIXED |
| C | minor | ground_truth.diagnosis.accepted[0] | The em dash in the edited label was replaced by a semicolon (no em dashes in new text). | FIXED |
| E | minor | metadata.case_body_concerns | Authoring-process text in metadata (condition-wide generated line). | FLAGGED |
| C | major | ground_truth.red_herrings[0].intended_effect | Presented antithrombotic therapy as the trap, against the conditional aspirin must (verification pass 2). | FIXED |
| E | minor | ground_truth.key_clinical_evidence[0] | Called the recommended ESR/CRP screen a precondition for the diagnosis; reworded to match the tiers (verification pass 2). | FIXED |
| C | major | ground_truth.assessment.required_recommendations[3] | Offered a triptan unconditionally although REQ1 keeps the possible-TIA branch, where triptans are contraindicated; made conditional on TIA being judged unlikely (verification pass 4). | FIXED |

## Changes
Aspirin is no longer stopped automatically. The must now asks the clinician to review the aspirin started for possible TIA once the cerebrovascular evaluation is complete: stop it if the episodes are judged to be migraine aura and there is no other indication, continue it if TIA remains a real possibility, and explain the decision to the patient and the GP. The prohibition on antiplatelet or anticoagulant therapy was deleted. Because the aspirin decision needs that evaluation, head and neck MR angiography moved from recommended to required, joins the stop rule (assessment, MRI, MRA), and a soft order MRI before MRA was added. The diagnosis now reads "Migraine with aphasic aura (ICHD-3 1.2.1); late-onset de novo aura in a postmenopausal woman, TIA judged unlikely on the clinical features" (label change, same codes), and the explanation must, key evidence item 4 and two red-herring interpretations state that the gradual build-up, identical recurrences and headache favour aura while normal MRI and MRA exclude infarction and arterial disease, not TIA. Tool outputs are unchanged; literature step removed earlier by class LIT.

## Verification
perfect_agent.py MIG-AURA-P01 -v: ok. test_case_guards (-k my six ids): 48 passed. case_io.py check: schema OK, synonym guard OK, no failure names this case (the only condition failure is test_no_review_process_text[MIG-AURA-P05], another worker's case).
Pass 1: 0 errors found
- Checked: aspirin must conditional, TIA prohibition gone, MRA required and in the stop rule, soft MRI-before-MRA constraint with existing ids, label and every TIA sentence state that imaging excludes infarction and arterial disease, not TIA; citations [AHA_ASA_2021_secondary] and [AHS_neuroimaging_2020] are in the pack allow-list. perfect_agent -v ok; test_case_guards -k 48 passed; case_io check clean for this case.
Pass 2: 1 errors found
- ground_truth.red_herrings[0].intended_effect still read "May anchor on TIA and lead to antithrombotic therapy", presenting antithrombotic therapy itself as the error, against note b37e0b4d (antiplatelet treatment is not to be classed as wrong while TIA remains possible) and the conditional aspirin must REQ1; same defect pass 1 fixed in P02. Now "May anchor on TIA as the explanation without weighing the aura features of the episodes". Rulings file updated.
- Cosmetic (not counted): ground_truth.key_clinical_evidence[0] said the ESR/CRP screen was needed before the diagnosis is accepted while action-5-interpret-labs is recommended; reworded to "brain MRI and vessel imaging are required, with an ESR/CRP screen recommended".
- Observation (no change): AHA/ASA 2021 secondary prevention advises an ECG in the TIA work-up; the case has no ECG criterion (an ECG order gets the library normal and uses the one extra action). Left as is: the plan does not add it and the pulse is regular on examination; for the re-reviewing physician.
- Re-checked by pass 2: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed; case_io check: schema OK, synonym guard OK, no test failure names this case.
Pass 3: 1 errors found
- ground_truth.sequence_constraints[1] (new soft MRI before MRA, added for note b37e0b4d) cited [AHS_neuroimaging_2020]; that guideline addresses whether to image in migraine and prefers MRI to CT, but says nothing about doing parenchymal imaging before vessel imaging, so the citation did not support the reason. Citations set to [] (as in the same MRI-before-MRA constraint of P03, P07 and P09). Rulings file updated.
- Cosmetic (not counted): action_criteria[0] (action-3-perform-clinical-assessment) rationale said the red flags make "imaging and a GCA screen necessary" while action-5-interpret-labs is recommended; now "make imaging necessary, with a GCA screen advisable".
- Checked as correct: both notes ruled; aspirin must conditional; no antithrombotic prohibition; MRA required and in the stop rule; no text says imaging excludes TIA; label per plan D4; no em dash in new text; no literature string.
- Re-run after the fix: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed; case_io check: schema OK, synonym guard OK, no test failure names this case.
Pass 4: 1 errors found
- ground_truth.assessment.required_recommendations[3] offered a triptan at headache onset with no condition, while REQ1 (note b37e0b4d) keeps aspirin if a TIA remains a real possibility; triptans are contraindicated after TIA (sumatriptan SmPC, listed in the case's own drug report). Now "a triptan is an option at headache onset only once TIA is judged unlikely (triptans are contraindicated after TIA) and after a cardiovascular evaluation ...". Rulings file updated.
- Observation kept from pass 2 (no change): no ECG criterion in a TIA-question work-up; left for the re-reviewing physician, the plan does not add it.
- Re-run after the fix: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed; case_io check: schema OK, synonym guard OK, no test failure names this case.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Checked the pass 4 fix (required_recommendations[3] triptan only once TIA is judged unlikely) against REQ1 (conditional aspirin, note b37e0b4d), the drug report (sumatriptan SmPC lists previous stroke or TIA) and every other triptan mention in the case: consistent. Condition-audit change: metadata.case_body_concerns is empty. perfect_agent.py -v ok; test_case_guards -k (eight ids) 64 passed.
