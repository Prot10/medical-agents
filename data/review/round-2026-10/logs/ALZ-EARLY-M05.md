# ALZ-EARLY-M05
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 4ba0d5e5-9d49-4094-8d4c-0982f93182fd | FIXED | `initial_tool_outputs.clinical_assessment.criteria_met.independence_in_instrumental_activities_lost` true; a new "Instrumental activities" finding (bills, supervised medicines, stove guards, driving stopped) replaces the blood-pressure sentence that sat under "Informant history"; impression and staging score say mild dementia. |
| e9050809-0bf7-4960-af00-2007e5730c65 | FIXED | Drug check kept as an optional post-diagnostic step: criterion `action-10-check-drug-interactions` last in `action_criteria`, `required_arguments` `{"drug": "donepezil"}`, label "After the diagnosis is staged and disclosed..."; follow-up last in `followup_outputs`; soft constraint clinical assessment before the drug check. Output rewritten: amlodipine does not slow the heart (the old warning implied it did), the unsupported "cholinergic effect on glycaemic regulation" removed, renal statement updated to eGFR 44. |
| ff4e1ef1-17cd-4541-899d-e3db345c4a14 | FIXED | Literature criterion `action-9-search-medical-literature` and follow-up deleted (the output also prescribed cholinesterase inhibitors); `fallback_tool_outputs.literature_search` null. |
| 34769945-0ba5-461d-aa01-33f67202f44c | FIXED | KCE "Amyloid PET positivity corroborates the A+ status..." deleted. An amyloid PET result now exists only as the authored answer to the PET alternative (`followup_outputs[2]`); no KCE, narrative or must cites a PET result. |
| 32e77625-daa5-43a8-a30b-e25b072efa0d | FIXED | `action-8-analyze-csf` relabelled, optional, alternatives CSF or amyloid PET; positive PET follow-up (Centiloid 72) authored; must "Pursue AD biomarker confirmation... single optional biomarker route" replaced by the canonical amyloid-testing must. |
| af490efa-2a0c-448d-a8a3-9341bb61ccc5 | FIXED | `initial_tool_outputs.labs`: every `clinical_significance` null; abnormal summary and interpretation list HbA1c 7.8%, LDL 104, HDL 48, triglycerides 178, creatinine 1.24 and eGFR 44 as abnormal without interpretive text; lab criterion expected evidence names them as modifiable contributors; musts on blood pressure, lipids and the diabetes regimen with the case values. |
| 339bfe05-7807-48d4-b064-059f3b5958e6 | FIXED | Summary comment; covered by the six rows above. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs.panels.CMP` (eGFR), `patient.clinical_history.past_medical_history[4]` | Creatinine 1.24 mg/dL in a 79-year-old woman gives eGFR about 44 mL/min/1.73 m2 (CKD-EPI 2021), not 68 (stage G2). | FIXED: eGFR 44 flagged low; PMH "stage G3a (eGFR 44)", which also fits the dose-reduced metformin; drug check renal line updated. Creatinine kept. |
| C | major | `ground_truth.assessment.required_recommendations` | "HbA1c toward <7.0%" in a 79-year-old with dementia who lives alone on glipizide and cannot recall her doses invites hypoglycaemia; older-adult targets are individualised (below 8.0% with cognitive impairment, ADA Standards, Older Adults). | FIXED: must reviews the regimen for hypoglycaemia risk, avoids intensification, considers replacing the sulfonylurea. HbA1c 7.8% still named as a contributor per af490efa. |
| C | major | `ground_truth.assessment` | Musts restated tool steps and repeated a prohibition; prohibitions included irrelevant iodinated contrast, benzodiazepines, antipsychotics, anticholinergics. | FIXED (C12): disclosure and planning, AChEI trial with supervised doses, BP and LDL after stroke, diabetes regimen, safety for a woman living alone, amyloid testing. Prohibitions: pure VCI diagnosis, memantine at mild stage. |
| E | major | `initial_tool_outputs.clinical_assessment.impression`, `.findings[0]`, `[2]` | Template impression with engineering sentence; truncated orientation; em dash. | FIXED (C3). |
| B | minor | `followup_outputs[1].output` (CSF) | 14-3-3, RT-QuIC, em dashes, non-vocabulary keys. | FIXED (C6), values unchanged. |
| C | minor | `followup_outputs[0].output.impression` | Rey delayed recall counted as executive; em dash. | FIXED. |
| D | minor | `initial_tool_outputs.mri.additional_observations[4]` | "consistent with prior stroke history" (cross-modality). | FIXED: removed. |
| B | minor | `fallback_tool_outputs.advanced_imaging` | DaTscan report answering every advanced-imaging modality (an amyloid PET or FDG order got a DaTscan). | FIXED (C2.3): null. DaTscan stays an avoided waste action. |
| B | minor | `fallback_tool_outputs.ecg.findings` | "Mildly prolonged PR interval (172 ms), within normal limits" (contradictory). | FIXED: "PR interval 172 ms". |
| B | minor | `initial_tool_outputs.labs.panels.Reviewed_cognitive_panel_additions` | Values identical to M01 (template). | FIXED: Mg 1.9, homocysteine 14.1, ESR 22 (ref 0-30), CRP 2.6, all normal. |
| B | minor | `ground_truth.differential` | VCI `high` while the label makes AD primary; DLB entry cited "amyloid-positive biomarkers". | FIXED (C11): VCI moderate as contributor; DLB, depression, FTD entries case-specific. |
| B | minor | `ground_truth.key_clinical_evidence` | Six items with duplicates and em dashes. | FIXED: four items. |
| A | minor | criteria citations, rationales, expected evidence | Duplicate bare keys; rationale equal to label; em dashes in expected evidence. | FIXED (C13). |
| B | minor | stop rule, sequence | `max_additional_actions` 0; no clinical-before-biomarker constraint. | FIXED. |
| - | check | plan 3.6 | Alternatives probed: CSF, amyloid PET and donepezil check served by case follow-ups. FDG-PET and DaTscan orders now receive the library's normal reports (plan Q4). perfect_agent.py ok; test_case_guards pass. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case remains mild Alzheimer dementia with contributory small vessel disease. The functional field now says instrumental independence is lost (supervised medicines, stove guards, driving stopped). The kidney function is made consistent: creatinine 1.24 is eGFR 44 (stage G3a), not 68. Labs carry no interpretive text and the vascular and metabolic abnormalities are flagged and managed. Musts: disclosure with advance planning, a cholinesterase-inhibitor trial with supervised dosing, blood pressure toward below 130/80 and LDL toward below 70 after her stroke, a diabetes review aimed at avoiding hypoglycaemia on glipizide (individualised HbA1c target), and safety for a woman living alone. The donepezil check stays as an optional last step and its pharmacology was corrected. The literature step and the amyloid PET pearl are gone; amyloid status is one optional step met by CSF (unchanged A+T+ values) or amyloid PET (positive, Centiloid 72). The DaTscan fallback and the irrelevant iodinated-contrast prohibition were removed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys: `[AHA_secondary_stroke_2021]` (Kleindorfer DO et al., 2021 AHA/ASA guideline for the prevention of stroke in patients with stroke and TIA, Stroke 2021;52:e364-e467) and `[ADA_older_adults_2025]` (American Diabetes Association, Standards of Care in Diabetes 2025, Section 13 Older Adults, Diabetes Care 2025;48 Suppl 1), plus `[NICE_NG97]`, `[STRIVE_2013]`.
- Harness: a `check_drug_interactions` call for any drug (e.g. memantine) is answered by the donepezil follow-up; scoring matches only `{"drug": "donepezil"}`, but the served text is donepezil's. A drug discriminator in the MockServer would fix it.

## Open questions for Andrea (judgment calls you could not settle)

- None. The HbA1c decision (individualised target, avoid hypoglycaemia) refines rather than contradicts Reviewer 1's af490efa: HbA1c 7.8% stays flagged and managed as a contributor.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case.
- Notes: all seven ids present; each FIXED claim holds (IADL field true with an instrumental-activities finding, drug check optional and last with corrected pharmacology and HR 72 = vitals, literature gone, amyloid PET pearl gone, biomarker alternatives with authored PET, labs without interpretive text and vascular values flagged and managed). eGFR 44 for creatinine 1.24 in a 79-year-old woman is right (CKD-EPI 2021), and the PMH, drug check and diabetes must now agree; ADA older-adult HbA1c target below 8.0% with cognitive impairment is correctly stated.
- Found and fixed:
  1. `ground_truth.differential[0]` was named "Vascular cognitive impairment (pure or predominant)" at `moderate` while its key features say it is a contributor, not the primary cause (ruling 7 incoherence). Renamed "Vascular cognitive impairment (contributory small vessel disease)", likelihood moderate kept per plan C11.
  2. `ground_truth.differential[1]` (mixed dementia) carried ICD F01.51 (vascular dementia with behavioural disturbance; she has none). Changed to F00.2 (dementia in Alzheimer disease, atypical or mixed type), matching the F00 family already in `icd_codes`.
  3. `ground_truth.key_clinical_evidence[1]` said a decreased CSF Abeta42/40 with raised p-tau "establishes" AD, while CSF is optional; reworded so MRI supports AD as primary and CSF confirms it when tested (plan C2.6).
  4. `initial_tool_outputs.clinical_assessment.findings[3]` (informant history) was a verbatim copy of an HPI sentence (plan C3, the class the worker fixed in the other cases); rewritten from the son's account with the pertinent DLB negatives.
  5. `metadata.key_educational_points[0]` said "biomarker adjudication is required", contradicting the optional biomarker criterion; reworded.
- perfect_agent.py ok; case_io.py check clean; test_case_guards pass.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
- MMSE item arithmetic: the 3 orientation points named only 2 errors (month, day of the week); now orientation 2 plus the three-stage command 1 (the exam already records difficulty with three-step commands), still 22/30; MoCA list gains orientation 2 so its items sum to 18/30 (exam and clinical assessment findings[1], [2]).
- MRI additional observation 'Posterior fossa and brainstem morphologically normal' contradicted the cerebellar lacune in the next line; now 'Brainstem morphologically normal'.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; "early onset alzheimer" and code G30.0 (onset at 65 or later); code G30.8 (atypical presentations only). Added "late onset alzheimer". Now: codes ['G30.1', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'late onset alzheimer'].
- Added follow-up `order_advanced_imaging` FDG_PET (trigger `order_fdg_pet`, no criterion), after the amyloid-status follow-ups: a case-specific Alzheimer-type metabolic report concordant with the MRI and stage. Before, an FDG order returned the library's normal scan, contradicting the case (summary Q4). Probed: FDG and amyloid PET orders each return their own report, in either order.
- Citation `[ADA_older_adults_2025]` -> `[ADA_older_adults_2026]` in the diabetes must: the 2026 Standards supersede the 2025 edition with the same A1C goal (below 8.0% for complex/intermediate health, Table 13.2).
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-6-interpret-labs]`.alternatives: was [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP]; now [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP, HbA1c, lipid_panel] | [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP].
- Decision: serve: new first alternative (old order kept as an alternative). The rationale quantifies diabetes and dyslipidaemia as small-vessel contributors and a must sets the HbA1c target; the vascular-risk panel was not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.
