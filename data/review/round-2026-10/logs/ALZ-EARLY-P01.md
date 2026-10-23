# ALZ-EARLY-P01
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| ccca2140-fd22-40f1-a404-ed5dc1bbde21 | FIXED | `initial_tool_outputs.clinical_assessment` rewritten as a posterior cortical syndrome assessment: `criteria_met.amnestic_predominant_profile` false, `delayed_recall_improves_with_cueing` true (recall 4/5, fifth word with a cue); findings for simultanagnosia, optic ataxia, oculomotor apraxia, left extinction, letter-substitution reading errors, husband's account (preserved recall of recent events) and lost instrumental activities; the storage-type amnestic statement and the copied/truncated HPI lines removed; impression and scores rewritten. |
| cd503a58-be28-4aa5-90fa-4da6a84f5bb5 | FIXED | `ground_truth.key_clinical_evidence[0]` replaced by the PCA pearl (visuospatial and visuoperceptual deficits with relatively preserved memory, optometrist first, Alzheimer pathology the commonest cause [PCA_consensus_2017]); the other amnestic, APOE, B12 and AChEI items replaced by: normal hippocampi do not exclude AD, Balint signs, white matter disease does not imply vascular dementia. |
| 52e45910-f88e-4c7b-b363-36a6501398d9 | FIXED | Plan C9: the `interpret_labs` follow-up `request_neuro_ophthalmology_consultation` deleted. Balint signs moved into the clinical assessment. New optional criterion `action-11-order-specialized-test-visual-fields` (`visual_field_perimetry` or `optical_coherence_tomography`, both in the vocabulary) with two authored follow-ups: full fields, acuity 20/25, normal colour vision, RNFL 82/93 microns. Must: refer for ophthalmology and low-vision assessment. The harness has no consult tool, so the assessment is kept as the tests plus the referral. |
| a35c9688-3a28-4487-a92e-84fd613b6ee2 | FIXED | `initial_tool_outputs.mri.additional_observations`: "No mass lesions or pathological enhancement post-gadolinium" becomes "No mass lesions" (`contrast: false` kept); small vessel line without the cross-modality "given age and vascular risk factors"; impression rewritten as a numbered list (Fazekas 2). |
| d7ec34ff-c173-409f-b882-dd8f9cc31c82 | FIXED | Case-level: template residue removed across the case. Assessment (ccca2140), KCE (cd503a58), musts and prohibitions, differential, criteria labels and rationales, metadata `clinical_notes`, `difficulty_rationale`, `key_educational_points` and teaching point 3 are now PCA-specific; no "amnestic" text remains except the comparison in the neuropsych rationale and the false field. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status`, clinical assessment | MMSE 26/30 listed only three lost points (serial sevens 2, pentagons 1). | FIXED: reading item (misread the written command) added, consistent with her alexia. |
| B | minor | `patient.clinical_history.social_history.occupation`, HPI | Occupation and HPI disagreed on her work status. | FIXED: architect moved to non-design duties four months ago, stated in both. |
| B | major | `ground_truth.action_criteria[action-8]`, `followup_outputs` | Biomarker criterion had one route (amyloid PET); no CSF counterpart (plan C2). | FIXED: alternatives amyloid PET and CSF Abeta42/40, p-tau, t-tau; concordant CSF follow-up authored (ratio 0.042, p-tau181 91, t-tau 640); canonical label, rationale and must; PET tracer 18F-florbetapir; fallback advanced imaging null. |
| B | minor | `followup_outputs` (FDG-PET) | medial_temporal_SUVr 0.93 called "normal" below the report's own 0.95 threshold. | FIXED: 0.97. FDG criterion kept optional with a new label and rationale; the must that restated it removed. |
| C | major | `ground_truth.action_criteria[action-10]`, `followup_outputs` | Drug check without a usable argument and output (plan C1.2, dementia case). | FIXED: optional and last, `{"drug": "donepezil"}`, donepezil output against her list (amlodipine does not slow the heart; aspirin GI caution; pulse 78); soft constraint clinical assessment before it; fallback drug interactions null. |
| C | major | `ground_truth.assessment` | Musts restated tool steps and carried an engineering must; prohibitions generic (benzodiazepines, antipsychotics, anticholinergics, aging/OSA). | FIXED (C12): disclosure with planning, ophthalmology and low vision, AChEI trial [NICE_NG97], driving, work and occupational therapy, amyloid testing. Prohibitions: attributing the deficits to the cataracts, memantine at the mild stage. |
| B | minor | `ground_truth.differential` | CBS and DLB likelihoods too high for the findings; CJD entry cited RT-QuIC and 14-3-3 never ordered; vascular cognitive impairment absent. | FIXED (C11): CBS low, DLB low, CJD on course and DWI only, VCI low added, ophthalmologic entry cites perimetry and OCT. |
| D | minor | `ground_truth.red_herrings` | The cataracts, the obvious diversion for visual complaints, were not a red herring. | FIXED: red herring on `past_medical_history[3]`, data point verbatim. |
| B | minor | `initial_tool_outputs.labs.panels.Reviewed_cognitive_panel_additions` | Mg and homocysteine identical to M01 (template). | FIXED: 2.1 and 9.4. |
| C | minor | `followup_outputs[0].output.impression` (neuropsych) | Template impression; Rey delayed recall read as memory loss despite a poor copy. | FIXED. |
| B | minor | `fallback_tool_outputs.literature_search`, `metadata.fallback_tool_kinds` | Literature fallback served; kinds listed null fallbacks. | FIXED (C8): null; stale kinds removed. |
| A | minor | criteria citations, rationales, sequence | Duplicate citations, rationale equal to label, "older patients" reason, `max_additional_actions` 0. | FIXED (C13, C16): MRI before biomarker, clinical assessment before biomarker, stop rule 1. |
| - | check | plan 3.6 | Every alternative probed on a fresh environment: perimetry, OCT, amyloid PET, CSF, FDG-PET and donepezil served by case follow-ups. perfect_agent.py ok; case_io check ok; test_case_guards pass; no em/en dashes, enhancement, 14-3-3, RT-QuIC or N/A. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case is posterior cortical atrophy due to Alzheimer disease at the mild dementia stage in a 65-year-old architect. The bedside assessment is no longer the amnestic template: it records simultanagnosia, optic ataxia, oculomotor apraxia, left visual extinction and letter-substitution reading errors with relatively preserved recall (4/5, the fifth with a cue), her husband's account, and loss of instrumental independence (driving stopped after an accident, moved off design work). The MMSE now adds up to 26/30. The neuro-ophthalmology consult that was filed as a lab test is replaced by optional visual fields or OCT, both normal, and a must to refer for ophthalmology and low-vision support; the cataracts are now an explicit red herring and attributing the deficits to them is prohibited. The MRI no longer mentions gadolinium. Amyloid status is one optional step met by amyloid PET (positive, posterior binding) or CSF (newly authored, concordant). Musts cover disclosure and planning, a cholinesterase-inhibitor trial, driving and work, and amyloid testing; the donepezil check is an optional last step with a real output.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys: `[PCA_consensus_2017]` (Crutch SJ et al., Consensus classification of posterior cortical atrophy, Alzheimers Dement 2017;13:870-884) and `[NICE_NG97]`.
- Harness: a `check_drug_interactions` follow-up is served for any drug; a drug discriminator in the MockServer would prevent a memantine query getting the donepezil text.

## Open questions for Andrea (judgment calls you could not settle)

- Note 52e45910 asks to keep the neuro-ophthalmology assessment as a specialized clinical assessment. The harness has no consult tool, so I kept its content as perimetry/OCT orders plus a referral must and moved the Balint signs into the clinical assessment (plan C9). If you want a dedicated `perform_clinical_assessment` type for it, that is a vocabulary change (CENTRAL).

## Verification
Adversarial check, 24 Oct 2026. Read the log, the notes, the diff and the whole final case.
- Notes: all five ids present; each FIXED claim holds (assessment is a posterior cortical syndrome assessment with amnestic field false and cueing field true matching 4/5 with the fifth on cue; KCE[0] is the PCA pearl; consult-as-lab follow-up removed and replaced by perimetry/OCT, both authored and served; no post-gadolinium text with contrast false; amnestic template residue gone).
- Cross-field: MMSE now 4 lost points = 26/30; IADL lost is justified by plan 1.2 (driving incidents and removal from design duties) although medicines and bills are preserved, and the HPI, occupation and assessment agree; CSF counterpart ratio 412/9800 = 0.042 and concordant with the positive PET; left extinction, left misreaching and right-greater parietal atrophy agree; drug-check pulse 78 = vitals; ICD G30.0 correct (onset about 63.5 years, 18 months before a visit at 65); no CJD entry citing tests the case lacks.
- Worker's open question on a dedicated neuro-ophthalmology assessment type: settled by plan C9; the note's intent (keep the assessment, not as `interpret_labs`) is met by `order_specialized_test` perimetry/OCT plus a referral must. No vocabulary change needed.
- No changes made. perfect_agent.py ok; case_io.py check clean; test_case_guards pass.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (3 places: the labs criterion label and metadata), the wording the other six cases already use.
- `BMP` completed to `CMP` with normal liver tests (total protein 6.9, albumin 4.0, AST 18, ALT 15, ALP 77, bilirubin 0.4): the labs criterion orders a CMP, so the authored report has to carry the hepatic part; no field_path points into the panel.
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
