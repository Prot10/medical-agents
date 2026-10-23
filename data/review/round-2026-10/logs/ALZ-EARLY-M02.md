# ALZ-EARLY-M02
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 3c5edf5d-f071-4683-b270-64953cd099ff | FIXED | Stays MCI (label `ground_truth.diagnosis.accepted[0]` unchanged, G31.84). Donepezil drug check removed: criterion `action-9-check-drug-interactions` and its follow-up deleted, initial and fallback `drug_interactions` null; MCI prohibition on cholinesterase inhibitors and memantine added. Vascular and metabolic contribution named: disclosure must ("vascular and metabolic contribution"), must on HbA1c 7.3% above goal, BP 136/81, statin, nightly CPAP; differential VCI moderate as a contributor; KCE on modifiable contributors; `metadata.key_educational_points[6]`. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness` | Staging contradicted MCI: husband fills her pill organizer and reviews her tax returns (a third party taking over a complex IADL under plan 1.2). | FIXED (C4, keeping the reviewer's MCI ruling): she fills the organizer herself without missed doses; she found the two return errors on rechecking and now checks every return twice; set up automatic payments after the duplicate bill payment. |
| B | major | `patient.clinical_history.social_history.occupation` | "retired teacher" while the HPI has her preparing tax returns for clients (MBA). | FIXED: "Semi-retired tax preparer; still prepares returns for a few long-standing clients". |
| B | major | `initial_tool_outputs.clinical_assessment.criteria_met.delayed_recall_improves_with_cueing`, `.impression` | Field false and impression "does not recover with cueing, a storage rather than a retrieval deficit", while the exam records a second word recalled after a categorical cue; engineering sentences. | FIXED: field true; impression per C3 skeleton (MMSE 26, MoCA 22, recall and cueing, informant, functional sentence). |
| B | minor | `initial_tool_outputs.clinical_assessment.findings[0]`, `[3]`, `[5]` | Truncated orientation line; informant finding copied the patient introduction; "this happens" without referent. | FIXED: completed or rewritten from the informant's account. |
| C | minor | `followup_outputs[0].output.impression` (neuropsych) | Bilingual patient tested without a statement on language and norms (class of M03 note 8e850ae1); Rey delayed recall called executive; em dash. | FIXED: impression states testing in English, her dominant language, with caution on naming and fluency; Rey delayed recall as visual memory; MCI conclusion added. Storage wording kept because recognition is impaired (12th percentile). |
| B | minor | `followup_outputs[0].output` Trail A/B, Rey copy | Percentiles identical to M01 (template). | FIXED: Trail A 42nd, Trail B 18th, Rey copy 45th (findings and quantitative_data); abnormal flags unchanged and correct. |
| B | minor | `followup_outputs[2].output` (CSF) | 14-3-3 and RT-QuIC; "N/A PMN/N/A lymph"; RBC "1 cell/uL (likely traumatic)". | FIXED (C6): canonical keys, values unchanged, artefacts removed, pattern interpretation. |
| C | major | `initial_tool_outputs.labs`, `ground_truth.action_criteria` | B12 275 pg/mL (low-normal) on eight years of metformin with reduced toe vibration, no MMA. | FIXED (C7.2): MMA follow-up (0.22 umol/L, normal) as `followup_outputs[1]` and new recommended criterion `action-10-interpret-labs-mma`. |
| B | minor | `initial_tool_outputs.labs.panels.Reviewed_cognitive_panel_additions` | Magnesium, homocysteine, ESR, CRP identical to M01 (template). | FIXED: Mg 1.9, homocysteine 11.6, ESR 16 (reference 0-30 for a woman over 50), CRP 2.3; all normal as before. |
| B | minor | `initial_tool_outputs.mri.findings[3]`, `.impression` | Left caudate head 4 mm lacune identical to M01; prose impression. | FIXED: 5 mm lacune in the left corona radiata; numbered impression with pertinent negatives (no microbleeds). |
| B | minor | `ground_truth.differential[0]` | VCI `high`, key features cite microbleeds the MRI does not show and "biomarker positivity". | FIXED: moderate, case-specific features. Depression and reversible-cause entries cite GDS 5/15, TSH, B12 with MMA. |
| C | major | `ground_truth.assessment` | Template musts restating tool steps; smoking cessation (quit 20 years ago); generic prohibitions (benzodiazepines, antipsychotics, anticholinergics) irrelevant to her. | FIXED (C12): five case musts (disclosure, reassessment and exercise, vascular and metabolic values, work and safety, amyloid testing); two prohibitions (MCI AChEI, do not attribute to OSA, TBI or aging). |
| B | minor | `ground_truth.key_clinical_evidence` | Storage pearl, APOE pearl, AChEI first-line pearl. | FIXED (C10): MMSE pearl kept, mixed pathology, low-normal B12 on metformin, AChEI not for MCI. |
| B | minor | `ground_truth.red_herrings[*].correct_interpretation` | "biomarker positivity"; "amnestic dementia syndrome" in an MCI case. | FIXED. |
| A | minor | criteria citations, rationales, expected_evidence | Duplicate bare keys, rationale equal to label, generic expected evidence. | FIXED (C13). |
| B | minor | biomarker criterion, sequence, stop rule | Single CSF route; no PET counterpart; `max_additional_actions` 0. | FIXED (C2): two alternatives, positive amyloid PET follow-up (Centiloid 54) authored; soft clinical-assessment-before-biomarker constraint; `max_additional_actions` 1. |
| D | minor | `fallback_tool_outputs.literature_search` | Literature fallback (C8). | FIXED: null. |
| - | check | plan 3.6 | Every alternative probed on a fresh environment: CSF, amyloid PET and MMA each served by the case's own follow-up. perfect_agent.py ok; test_case_guards pass. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case remains amnestic multi-domain MCI with likely Alzheimer pathology, and the history now supports that staging: she fills her own pill organizer, caught the two tax-return errors herself and now double-checks every return, and set up automatic payments after one duplicate bill. Her occupation is now consistent (semi-retired tax preparer). The bedside assessment records that a categorical cue helped recall (field and impression corrected). The neuropsychological report states that testing was in English, her dominant language, with caution on naming and fluency. The donepezil step is gone; the musts are disclosure, 6-12 month reassessment with exercise, management of HbA1c 7.3%, BP and CPAP adherence, a check of her client work and safety, and amyloid testing only if it would change management. MMA (0.22, normal) is a new recommended step for B12 275 on metformin. The CSF (ratio 0.051, p-tau181 64, t-tau 420) lost 14-3-3 and RT-QuIC, and an amyloid PET alternative (positive, Centiloid 54) was added. The lacune was moved to the left corona radiata to remove a copy of M01.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: the G31.84 expansion grants dementia, PCA, Benson and early-onset labels and the G30.x codes to this MCI case (plan 5.1).
- New citation keys used: `[NIA_AA_MCI_2011]`, `[STRIVE_2013]`, `[BSH_B12_2014]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None. The HPI edits that make MCI explicit (who fills the pill organizer, who caught the errors) were needed to honour the reviewer's MCI ruling under the plan 1.2 functional rule; the alternative, restaging to mild dementia, would contradict the note.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case.
- Note 3c5edf5d: holds (MCI label kept, donepezil step gone, vascular and metabolic contribution named in the disclosure and vascular musts, differential and KCE).
- HPI rewrite reviewed against HEAD: the original had the husband filling the pill organizer and catching the return errors, which under plan 1.2 reads as dementia; the reviewer ruled MCI, so making the compensating strategies explicit is the plan C4 action, not invention against the note. Occupation now agrees with the HPI. Bilingualism and English dominance were in the original (social history, informant findings), so the neuropsych language statement is grounded.
- Cross-field: MMSE (date 1, recall 2, serial sevens 1 = 26/30) consistent; cueing field true matches the exam; MRI says no microbleeds and the differential no longer cites them; GDS 5/15 flagged; ESR range 0-30 for a woman over 50.
- Found and fixed (template carry-over, PATTERNS 4): the CSF Abeta42 465 pg/mL was identical to M01 and Abeta40 9100 pg/mL identical to M03. Changed to Abeta42 452 pg/mL (now "decreased") and Abeta40 8850 pg/mL in `followup_outputs[2].output.special_tests` and the interpretation; ratio 452/8850 = 0.051 unchanged, so the criterion expected evidence and differential still hold.
- perfect_agent.py ok; case_io.py check clean for this case; test_case_guards pass.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
- `BMP` completed to `CMP` with normal liver tests (total protein 6.8, albumin 3.9, AST 20, ALT 16, ALP 94, bilirubin 0.5): the labs criterion orders a CMP, so the authored report has to carry the hepatic part; no field_path points into the panel.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
