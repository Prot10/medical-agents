# ALZ-EARLY-RM02
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 833a3967-63f7-48d4-98a5-9ad78c99ee83 | FIXED | `ground_truth.diagnosis.accepted[0]` "Mild cognitive impairment due to Alzheimer's disease (amnestic, multi-domain)" became "Alzheimer disease (mild dementia, amnestic) with cerebrovascular copathology"; `icd_codes` G31.84 primary removed, now [G30.1, G30.0, G30.9, G30.8, F00] (onset at 74, no duplicates). `initial_tool_outputs.clinical_assessment.criteria_met.independence_in_instrumental_activities_lost` true, stage score "mild dementia: instrumental independence lost", functional-status finding (missed appointments, unpaid bills needing her daughter's intervention, lives alone), impression rewritten. Neuropsych impression ends with the mild dementia wording. The MCI synonym labels after `accepted[0]` were not hand-edited: CENTRAL. |
| fe0d2007-7a19-4ae5-b090-e952afb5d0ae | FIXED | Label names the cerebrovascular copathology; `differential[1]` is now "Vascular cognitive impairment as the sole cause" (low), stating Fazekas 2, hypertension and HbA1c 6.1% as a real copathology that may contribute to the gait disorder while AD stays primary; KCE[2] says the same; MRI impression item 3 names Fazekas 2 small vessel disease; vascular-risk must (BP 142/84 on amlodipine, lipid profile, HbA1c). |
| 878f76e9-e61a-4789-9cb7-4a267ccdd676 | FIXED | `red_herrings[0]` rewritten: the full triad is not required and a negative tap test does not exclude iNPH, so it stays in the differential; no DESH, obtuse callosal angle, no gait response and the AD profile make AD primary. iNPH is `differential[0]` (low) with what raises it and what argues against it; KCE[1] and a must to reassess gait and continence (extended lumbar drainage or neurosurgical opinion if gait worsens or urinary symptoms appear); prohibition on shunting for ventriculomegaly alone. |
| 6a2fe426-9476-4795-a5ba-ffccf7defa6c | FIXED | `initial_tool_outputs.mri`: Evans index 0.32 no longer called "upper limit of normal"; ventriculomegaly finding reports callosal angle 104 degrees, no high-convexity tightness, proportionate Sylvian fissures (no DESH); "No abnormal enhancement on post-contrast sequences" removed from `additional_observations` (protocol is non-contrast); impression numbered (MTA, nonspecific ventriculomegaly without DESH, Fazekas 2, no acute lesion). |
| c5ba4ddf-a7ba-4f72-8cae-ce40803b7e2a | FIXED | `followup_outputs[2]` (CSF): cryptococcal antigen, bacterial and fungal cultures, AFB stain, TB PCR, cytology and NfL removed; routine AD panel only with vocabulary keys; Abeta40 8960 pg/mL added behind the ratio (412/8960 = 0.046; the stored 0.062 with reference >0.089 was a different assay and did not match the other cases), references aligned (Abeta42 >600, ratio >0.065); "(normal)" removed from values; pattern interpretation. |
| ddcae4f0-96c7-4183-b48a-27cf4b73f446 | FIXED | Literature follow-up `search_nph_vs_alzheimers` deleted (no literature criterion existed). The tap test filed as `interpret_labs` (`request_tap_test`) deleted and re-authored as a diagnostic procedure: new optional `action-10-perform-clinical-assessment-gait` (`perform_clinical_assessment {"assessment_type": "gait_and_balance_timed"}`) with follow-up `gait_assessment_and_tap_test` (10 m walk 18.2 s, 17.5 s at 2 h, 17.8 s at 24 h after 40 mL; MMSE 23 to 23; `pre_post_comparison`), and a soft constraint MRI before it. |
| ca63343f-f3a9-4b4c-81d7-1efe91fd19b0 | FIXED | Case comment on staging: resolved by 833a3967. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status`, `clinical_assessment.findings` | MMSE 23/30 with items "orientation 4/10, recall 0/3, serial 7s 3/5" (11 points lost, i.e. 19/30), and orientation 4/10 contradicts "oriented to person, place and year". | FIXED: orientation 8/10 (date and month lost), recall 0/3, serial sevens 3/5 = 23/30; same in the assessment findings; "screening instrument administered at the bedside" score replaced by MMSE 23/30. |
| B | minor | `clinical_assessment.criteria_met`, findings | Cue benefit marked present although 0/3 were recalled with categorical cues; the informant finding copied the HPI ("Over the ensuing weeks..."). | FIXED: cueing false; findings rewritten as examination, informant and functional items. |
| C | minor | `followup_outputs[0].output.impression` | "Processing speed was not formally tested" while Trail Making A 58 s is reported; MCI wording. | FIXED: numbered impression with processing speed within norms and mild dementia wording. |
| B | major | `action-8-analyze-csf` | Single CSF alternative; an amyloid PET order got the library's negative report (C2). | FIXED: two alternatives, canonical label, rationale, expected evidence; new follow-up `order_amyloid_pet` (18F-flutemetamol, positive, Centiloid 58). Probe of every alternative: neuropsych <- `followup_outputs[0]`, gait/tap <- [1], CSF <- [2], PET <- [3], drug check <- [4]; no library answer. |
| C | major | `followup_outputs[4]` drug check | Claimed pantoprazole reduces donepezil absorption and a lowered seizure threshold; criterion had empty arguments. | FIXED: correct pharmacology (no PPI interaction, amlodipine does not slow HR), pulse 72 and falls, titration; `{"drug": "donepezil"}`, trigger `check_drug_interactions_donepezil`, optional and last. |
| C | major | `ground_truth.assessment` | Musts restated tool steps; no safety plan for a woman living alone, no falls, vascular or AChEI must; generic prohibitions. | FIXED: informant, disclosure and planning, home safety and supervision (bills, appointments, medicines), physiotherapy and falls, canonical biomarker and AChEI musts, vascular risk, NPH reassessment. Prohibitions: attributing it to ageing or sleep, shunting for ventriculomegaly alone, benzodiazepine or Z-drug for sleep, memantine at the mild stage. |
| C | minor | `ground_truth.differential` | DLB and FTD template features; depression and reversible causes generic. | FIXED: each entry worded from case data (no hallucinations, fluctuations, RBD or rigidity; glabellar sign and withdrawal nonspecific; GDS 6/15; normal TSH, B12, folate, RPR, HIV). |
| C | minor | `ground_truth.key_clinical_evidence` | Template items. | FIXED: four case-specific items (C10). |
| B | minor | `initial_tool_outputs.labs` | BMP and separate liver panel for a CMP order; panel named "Reviewed_cognitive_panel_additions" (engineering); summary with interpretive text. | FIXED: Comprehensive Metabolic Panel (total protein, ALP, bilirubin added, normal), "Magnesium and Homocysteine" panel, factual summary and interpretation; values unchanged. B12 310 pg/mL needs no MMA (plan C7 threshold). |
| B | minor | `fallback_tool_outputs.ct.impression` | "No ... hydrocephalus" contradicts the MRI ventriculomegaly. | FIXED: reports prominent ventricles and periventricular hypodensity. |
| A | minor | criteria citations, rationales; constraints; stop rule | Duplicate keys, rationale = label, `max_additional_actions` 0. | FIXED: one or two keys each, case-specific rationales, order per plan, assessment-before-biomarker and MRI-before-tap constraints added, MRI-before-CSF reason kept, `max_additional_actions` 1. |
| C | minor | `avoided_actions` | Generic rationales. | FIXED: case-specific (near-falls while walking, no cardiac symptoms; MRI available). |
| E | minor | `metadata.difficulty_description`, `difficulty_rationale`, `key_educational_points` | Engineering wording ("reviewed cognitive laboratory panel", "no duplicate CSF/PET confirmation"). | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is restaged as mild Alzheimer dementia with cerebrovascular copathology (G30.1): she lives alone, has missed appointments and left bills unpaid until her daughter intervened, and the clinical assessment, neuropsychological impression and label now say so. The MMSE item breakdown was corrected to add up to 23/30. The MRI no longer calls an Evans index of 0.32 normal: it reports ventriculomegaly without DESH, a callosal angle of 104 degrees and Fazekas 2 small vessel disease, and the post-contrast statement is gone. Normal pressure hydrocephalus stays in the differential (low): the full triad is not required and a negative tap test does not exclude it, but there is no DESH and gait did not improve. The tap test is now a timed gait assessment before and after removal of 40 mL of CSF (optional, after MRI), and the literature step is gone. The CSF contains only the Alzheimer panel, with Abeta40 behind its ratio; CSF or amyloid PET can establish amyloid status (optional, one test enough; a concordant positive PET was added). The donepezil check now has correct pharmacology. Musts cover home safety for a woman living alone, falls and physiotherapy, vascular risk, the cholinesterase inhibitor and NPH reassessment if gait worsens or urinary symptoms appear.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: primary code changed from MCI (G31.84) to G30.1. The labels appended by the old G31.84 entry ("mild cognitive impairment", "MCI", "amnestic mild cognitive impairment", "amnestic MCI", "prodromal alzheimer", "mild cognitive impairment due to alzheimer") are still in `accepted` and would credit an MCI answer; please re-run `apply_diagnosis_synonyms.py --prune --cases ALZ-EARLY-RM02` (plan 5.1). "posterior cortical atrophy", "benson syndrome" and "early onset alzheimer" (from G30.0) are also wrong for a late-onset amnestic case.
- Citation keys used: `[iNPH_2005]`, `[iNPH_Japan_2021]`, `[STRIVE_2013]`, `[Beers_2023]`, `[NICE_NG97]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea. Decided: iNPH is `low`, not `moderate`. It stays in the differential as the reviewer asks, but without DESH, with an obtuse callosal angle, no urinary symptoms and no response to the tap test, and with an Alzheimer CSF profile, low is the defensible likelihood; the reassessment must covers a later change.

## Verification
Adversarial verifier, 24 Oct 2026. Checked every note row (833a3967, fe0d2007, 878f76e9, 6a2fe426, c5ba4ddf, ddcae4f0, ca63343f) against the file: label and G30.1 (onset 74), IADL field true, cerebrovascular copathology in label, MRI impression and differential, iNPH kept in the differential (low) with the correct statement that a negative tap test does not exclude it, Evans 0.32 reported as ventriculomegaly with callosal angle 104 degrees and no DESH, no post-contrast text, CSF with only the AD panel and Abeta40 (412/8960 = 0.046, glucose ratio 62/107 = 0.58, opening pressure 12 cmH2O), no literature follow-up, tap test re-authored as an optional `gait_and_balance_timed` assessment after MRI (10 m walk 18.2 s to 17.5/17.8 s, under 5%, MMSE unchanged). MMSE breakdown verified (orientation 2 + recall 3 + serial sevens 2 = 7, 23/30). Drug check content correct (pantoprazole, amlodipine; pulse 72 matches the vitals). CT fallback now agrees with the MRI. Musts, prohibitions (no shunting on ventriculomegaly alone, no benzodiazepine or Z-drug) and the differential agree with the pathway. Both biomarker alternatives have case-authored outputs.

Found: nothing that needed a change. No edit made.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- Normal values in `Magnesium and Homocysteine` varied (Magnesium 2.0 to 2.3, Homocysteine 10.2 to 13.6), all still within the case's reference ranges: the same numbers (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8) had been copied into up to 13 cases, a template artefact raised by the S01 worker; no text cites the changed values.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed mild cognitive impairment labels (MCI, amnestic MCI, prodromal alzheimer, MCI due to alzheimer); "posterior cortical atrophy" and "benson syndrome"; "early onset alzheimer" and code G30.0 (onset at 65 or later); code G30.8 (atypical presentations only). Added "late onset alzheimer". Now: codes ['G30.1', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'late onset alzheimer'].
- Added follow-up `order_advanced_imaging` FDG_PET (trigger `order_fdg_pet`, no criterion), after the amyloid-status follow-ups: a case-specific Alzheimer-type metabolic report concordant with the MRI and stage. Before, an FDG order returned the library's normal scan, contradicting the case (summary Q4). Probed: FDG and amyloid PET orders each return their own report, in either order.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-6-interpret-labs]`.alternatives: was [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP]; now [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP, HbA1c] | [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP].
- Decision: serve: new first alternative (old order kept as an alternative). The rationale measures metabolic vascular risk and a must addresses HbA1c 6.1%; HbA1c was not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.
