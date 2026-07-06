# MS-RR — NeuroBench v5 audit

30 cases audited (M01-M04, P01-P05, RM01-RM04, RP01-RP05, RS01-RS06, S01-S06) — 78 findings total (0 blocker, 20 major, 33 minor, 25 nit); 16 fixed, 62 flagged; schema/coherence/leakage validators pass (validators_ok=true).

## Terminology / taxonomy

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| MS-RR (all 30 cases) | terminology | major | ground_truth.icd_code | Primary diagnosis coded G35 (retired parent code); RRMS must use G35.A per ICD-10-CM effective 2025-10-01 | FIXED | Set icd_code = "G35.A" in all 30 cases (done) |
| CONFIG | terminology | major | dataset-generation/config/conditions.yaml:437 | Condition-level canonical icd_code still "G35", outdated for RRMS | FLAGGED | Change line 437 to icd_code: "G35.A" |
| README | terminology | major | dataset-generation/README.md:100 | Condition table lists MS-RR as G35 | FLAGGED | Update cell to G35.A |
| PACK | terminology | major | dataset-generation/criteria_packs/MS-RR.md:3 | Criteria pack header states "ICD-10: G35" | FLAGGED | Update to "ICD-10: G35.A" |
| MS-RR (all 30 cases) | terminology | minor | ground_truth.differential[MOGAD].icd_code | MOGAD differential coded G36.9 instead of dedicated G37.81 (effective 2023-10-01) | FLAGGED | Sweep MOGAD icd_code G36.9 -> G37.81 dataset-wide; leave NMOSD G36.0 as-is |
| MS-RR (all 30 cases) | terminology | nit | ground_truth.primary_diagnosis | No Alzheimer's-style label ambiguity; late-onset/atypical demographics are intentional hard cases, not terminology errors | FLAGGED | No action; recorded for completeness |

## Audit findings

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| MS-RR-M03 | B internal-consistency | major | followup_outputs[2].output.quantitative_data | Duplicate OCT test-name keys with no eye laterality collapse to only the normal-eye values, contradicting the impression's abnormal set | FLAGGED | Add eye laterality to each of the 6 OCT finding names so keys are unique and retain the abnormal right-eye values |
| MS-RR-M01 | B internal-consistency | minor | initial_tool_outputs.csf.special_tests.Myelin basic protein | MBP 3.8 ng/mL labeled "mildly elevated" against its own stated reference "<4.0 ng/mL" | FLAGGED | Change to "within normal limits / high-normal" in special_tests and echoed interpretation |
| MS-RR-M01 | B internal-consistency | nit | initial_tool_outputs.csf.special_tests.IgG index | IgG index 0.65 labeled "borderline elevated" against reference "<0.70" | FLAGGED | Soften to "upper-normal / borderline" |
| MS-RR-M01, M02, M03 | terminology | minor | ground_truth.differential[2].icd_code | Neurosarcoidosis differential coded D86.85 ("Sarcoid myocarditis", cardiac) instead of neuro-appropriate code | FLAGGED | Replace D86.85 with D86.81 (shared template; apply dataset-wide) |
| PACK | C clinical-correctness | minor | dataset-generation/criteria_packs/MS-RR.md:3 | Pack ICD-10 header stale (G35); cases correctly use G35.A | FLAGGED | Update pack header; do not revert case icd_code |
| MS-RR-M04 | E | minor | initial_tool_outputs.mri.findings[3].mass_effect | Duplicated word: "Mild mild swelling of the left optic nerve" | FIXED | Corrected to "Mild swelling of the left optic nerve, no perineural mass" |
| CONFIG | C | major | ground_truth.icd_code | "G35.A" flagged as possibly non-standard relative to bare "G35" convention noted in criteria pack — dataset-wide convention decision needed | FLAGGED | Decide dataset-wide G35 vs G35.A convention at CONFIG level; do not fix cases in isolation |
| MS-RR-M04 | C | major | ground_truth.red_herrings[0] / key_reasoning_points / HPI | HPI documents a prior demyelinating-type sensory episode (~8 months ago) that conflicts with red_herrings[0]'s "first-ever ... no prior documented neurological event" framing | FLAGGED | Clinician to reconcile "first attack" framing vs documented prior episode |
| MS-RR-P01 | D | minor | followup_outputs[2].output.findings / quantitative_data | OCT report's duplicate unlabeled test names collapse quantitative_data, dropping normal-eye values | FLAGGED | Add eye labels to each OCT row as in P02 |
| MS-RR-P01 | E | nit | initial_tool_outputs.csf.interpretation | Template artifact "(N/A PMN/N/A lymph)" despite differential stating 100% lymphocytes | FLAGGED | Strip or populate the differential placeholder |
| MS-RR-P02 | E | nit | initial_tool_outputs.csf.interpretation | Same "(N/A PMN/N/A lymph)" artifact | FLAGGED | Strip or populate placeholder |
| MS-RR-P02 | D | minor | followup_outputs[5] | SSEP delivered via interpret_labs instead of order_specialized_test (test_type=ssep) | FLAGGED | Re-route SSEP to order_specialized_test for modality fidelity |
| MS-RR-P02 | C | minor | ground_truth.optimal_actions[5].category | check_drug_interactions tiered "recommended" vs pack's "Required" and siblings' "required" | FLAGGED | Reconcile tier, likely to "required" |
| MS-RR-P01 | A | nit | followup_outputs[2].output.test_type | OCT report uses "oct" instead of canonical "optical_coherence_tomography" | FLAGGED | Normalize report test_type token |
| MS-RR-P03, P04, P05 | terminology | major | ground_truth.differential[].icd_code (Neurosarcoidosis) | D86.85 ("Sarcoid myocarditis", cardiac) used for a CNS/meningeal differential | FLAGGED | Change to D86.81 or D86.89; correct systematically at generator/config level |
| MS-RR-P05 | B | major | initial_tool_outputs.mri.findings / impression | Impression enumerates 4 enhancing lesions but findings show a 5th (infratentorial) with faint enhancement | FLAGGED | Reconcile enhancing-lesion count between findings and impression |
| MS-RR-P03 | C | minor | initial_tool_outputs.labs.panels.CBC | CBC uses female reference ranges for a 22-year-old male patient (Hgb/RBC/Hct) | FLAGGED | Apply male reference ranges; re-flag Hgb 12.4 as abnormal if below male ULN |
| MS-RR-P03 | B | minor | patient.clinical_history.social_history.occupation vs HPI | Occupation "software engineer" conflicts with HPI/social-history framing as full-time graduate student | FLAGGED | Reconcile occupation field with student narrative |
| MS-RR-P03 | B | nit | initial_tool_outputs.csf.glucose_ratio | CSF glucose ratio 0.70 does not match its own numerator (59.5/88=0.68); serum glucose also differs from BMP (88 vs 80) | FLAGGED | Correct ratio to 0.68 |
| MS-RR-P05 | B | nit | initial_tool_outputs.mri.additional_observations vs findings | Supratentorial lesion subtotal (~14) overstated vs enumerated findings (~13) | FLAGGED | Align subtotal with total-14 framing |
| MS-RR-P04 | A | nit | metadata | Omits expected_agent_confidence and fallback_tool_kinds present in P03/P05 | FLAGGED | Add the two metadata fields for consistency |
| MS-RR-RM01 | B internal-consistency | major | initial_tool_outputs.ecg.interpretation | "Sinus tachycardia, rate 90 bpm" contradicts rhythm field/findings ("Normal sinus rhythm") and rate 90 <100 | FIXED | Corrected to "Normal sinus rhythm, rate 90 bpm" |
| MS-RR-RM01 | D realism-leakage | nit | initial_tool_outputs.labs.abnormal_values_summary | Interpretive labels ("Stress hyperglycemia", "left shift") in a supposedly factual summary | FLAGGED | Optionally reduce to value + direction only |
| MS-RR-RM01 | C clinical-correctness | minor | ground_truth.primary_diagnosis | "Relapsing-remitting" qualifier applied to an apparent first clinical event with DIT resting on CSF/imaging, not a second relapse | FLAGGED | Human adjudication of RRMS vs CIS/tumefactive-demyelination qualifier |
| MS-RR-RM02 | B internal-consistency | nit | followup_outputs[3] | MR spectroscopy delivered via analyze_brain_mri, inconsistent with RM01's order_advanced_imaging routing for the same study | FLAGGED | Standardize spectroscopy onto order_advanced_imaging |
| MS-RR-RM03 | B internal-consistency | major | followup_outputs[0].output (VEP) findings[0].reference_range vs impression | Left-eye P100 reference "<100 ms" (finding) contradicts impression's "<115 ms"; threshold choice is load-bearing for DIS | FLAGGED | Reconcile P100 threshold convention (clinical/lab judgment) |
| MS-RR-RM03 | B internal-consistency | nit | initial_tool_outputs.csf.cell_count.RBC | CSF RBC "1 cell/uL (traumatic tap)" — 1 RBC/uL is not consistent with a traumatic tap | FLAGGED | Consider removing "(traumatic tap)" parenthetical |
| PACK | C clinical-correctness | minor | dataset-generation/criteria_packs/MS-RR.md (ICD-10 header) | Pack lists only "ICD-10: G35"; RRMS cases correctly use G35.A | FLAGGED | Update shared pack to reference G35.A |
| MS-RR-RP01 | B internal-consistency | major | followup_outputs[0].output.findings[0-1].reference_range | VEP P100 reference "<102 ms" contradicted own impression ("<115 ms") and sibling convention | FIXED | Changed reference_range to "<115 ms" for both eyes |
| MS-RR-RP02 | E language | minor | followup_outputs[4].output.findings[0,2].value + quantitative_data | Duplicated trailing units: "118 ms (prolonged) ms" and "4.2 microV (reduced) microV" | FIXED | Removed duplicated units in findings and quantitative_data mirrors |
| MS-RR-RM04 | terminology | minor | ground_truth.differential[0].icd_code | Neurosarcoidosis differential coded D86.85 (cardiac) instead of D86.81/D86.89 | FLAGGED | Dataset-wide replacement of D86.85 -> D86.81 (or D86.89) |
| MS-RR-RP01 | B internal-consistency | nit | followup_outputs[6].output.test_type | OCT output uses "oct" vs case's own optimal_actions "optical_coherence_tomography" | FLAGGED | Normalize OCT output test_type dataset-wide |
| MS-RR-RP02 | B internal-consistency | nit | followup_outputs[7].output.test_type | Same "oct" vs "optical_coherence_tomography" mismatch | FLAGGED | Normalize dataset-wide alongside RP01 |
| MS-RR-RP01 | E language | nit | initial_tool_outputs.csf.interpretation | "(N/A PMN/N/A lymph)" artifact vs actual differential (85% lymphocytes) | FLAGGED | Rephrase to drop fragment or reflect actual differential |
| MS-RR-RM04 | D realism-leakage | nit | metadata.real_seed vs metadata.source_pmid/real_seed_note | Contradictory provenance metadata (PMID claimed both "removed" and "verified") | FLAGGED | Reconcile provenance metadata fields |
| MS-RR-RP03 | E | minor | followup_outputs[3].output.findings[2-3].value / quantitative_data | Duplicated unit token "microvolts microvolts" (4 occurrences) | FIXED | Collapsed to single "microvolts" |
| MS-RR-RP05 | A | major | ground_truth.red_herrings[0].field_path | Compound prose field_path with " and " joins unresolvable by coherence validator | FIXED | Set to single resolving anchor "patient.clinical_history.past_medical_history" |
| MS-RR-RP04 | C | minor | ground_truth.differential[5].icd_code | Lyme neuroborreliosis coded A69.20 (unspecified) instead of specific A69.22 | FLAGGED | Consider A69.22 for neuroborreliosis differential |
| MS-RR-RP04 | D | nit | initial_tool_outputs.csf.interpretation | Templated epidemiologic hedge names "multiple sclerosis" explicitly | FLAGGED | Optionally trim to avoid naming MS |
| MS-RR-RP04 | D | nit | initial_tool_outputs.mri.impression / additional_observations | Impression explicitly states MRI "fulfills" DIT/DIS criteria — borderline but acceptable within-imaging language | FLAGGED | No change; noted for reviewer awareness |
| MS-RR-RP03 | C | minor | ground_truth.differential[0] | Primary CNS lymphoma ranked "high" likelihood in a 34-year-old immunocompetent woman | FLAGGED | Reviewer to consider demoting to "moderate" |
| MS-RR-RP03 | E | nit | initial_tool_outputs.csf.interpretation | "(N/A PMN/N/A lymph)" artifact (WBC normal, so not misleading) | FLAGGED | Cosmetic tidy of fragment |
| PACK | C | nit | criteria_packs/MS-RR.md line 3 | "ICD-10: G35" stale; cases correctly use G35.A | FLAGGED | Update pack ICD reference to G35.A; no case change needed |
| MS-RR-RS02 | B | major | followup_outputs[0].output.impression | VEP impression "reference <115 ms" contradicts own finding reference_range "<102 ms" | FIXED | Impression corrected to "reference <102 ms" |
| MS-RR-RS03 | B | major | followup_outputs[0].output.impression | Same VEP contradiction ("<115 ms" impression vs "<102 ms" finding) | FIXED | Impression corrected to "reference <102 ms" |
| CONFIG | C | minor | ground_truth.differential[1].icd_code (MOGAD) | MOGAD differential coded G36.9 (outdated) instead of dedicated G37.81 | FLAGGED | Update MOGAD icd_code to G37.81 dataset-wide |
| PACK | C | nit | criteria_packs/MS-RR.md#ICD-10 | Pack states "ICD-10: G35"; cases correctly use G35.A | FLAGGED | Update pack (and conditions.yaml) reference to G35.x split |
| MS-RR-RS01 | B | minor | patient.neurological_exam.cranial_nerves | "Bilateral horizontal gaze palsy" label imprecise for a described unilateral left conjugate gaze palsy mechanism | FLAGGED | Clinician to confirm intended label; do not edit seeded exam without adjudication |
| MS-RR-RS01 | E | nit | followup_outputs[].output.findings[].value | Unit-concatenation artifacts on non-numeric values ("Unable to reliably test ms", "Limited signal quality micrometers") and CSF "(N/A PMN/N/A lymph)" filler | FLAGGED | Fix report generator to not append units to qualitative values, dataset-wide |
| MS-RR-RS04 | E language | minor | initial_tool_outputs.csf.interpretation | Broken template substitution "(N/A PMN/N/A lymph)" | FIXED | Replaced with "differential: lymphocyte-predominant" |
| MS-RR-RS04, RS05, RS06 | C clinical-correctness | major | ground_truth.differential[Neurosarcoidosis].icd_code | D86.85 ("Sarcoid myocarditis", cardiac) used for neurosarcoidosis | FLAGGED | Correct dataset-wide to D86.81 (orchestrator-level fix) |
| PACK | terminology | minor | dataset-generation/criteria_packs/MS-RR.md line 3 | "ICD-10: G35" stale vs cases' correct G35.A | FLAGGED | Update pack's ICD-10 line to G35.A subcategory split |
| MS-RR-RS06 | B internal-consistency | minor | ground_truth.differential[CNS vasculitis].key_features | Self-contradictory phrase: ESR/CRP called both "normal" and "not ordered" | FLAGGED | Delete stray word "normal" |
| MS-RR-RS04 | E language | nit | followup_outputs[request_oct].output.findings | OCT findings unlabeled by eye, unlike RS05/RS06 house style | FLAGGED | Add "— right eye" / "— left eye" labels |
| MS-RR-RS04 | C clinical-correctness | nit | ground_truth.key_reasoning_points[4],[6] | Generic KRPs describe MRI features (open-ring enhancement, black holes) not present in this case's MRI | FLAGGED | Consider tailoring KRPs to features actually present |
| MS-RR-S03 | B internal-consistency | minor | followup_outputs[0].output.findings[4].reference_range | VEP interocular-difference reference "<8 ms" contradicts own impression ("<6 ms") and siblings S01/S02 | FIXED | Set reference_range to "<6 ms" |
| CONFIG | C clinical-correctness | minor | criteria_packs/MS-RR.md line 3 | Pack states "ICD-10: G35"; cases correctly use G35.A | FLAGGED | Update pack ICD line to G35.A-G35.D split |
| MS-RR-S01 | C clinical-correctness | minor | ground_truth.differential[1].icd_code (MOGAD) | MOGAD coded G36.9 instead of dedicated G37.81 | FLAGGED | Consider updating to G37.81 across the set |
| MS-RR-S03 | C clinical-correctness | minor | ground_truth.optimal_actions[4].category | search_medical_literature tiered "recommended" vs "required" in siblings S01/S02 and pack | FLAGGED | Harmonize tier to "required" |
| MS-RR-S03 | terminology | minor | followup_outputs[6].output.test_type ("urodynamics") | Not in closed order_specialized_test vocabulary; unreachable by in-vocab agent action (not on gold path) | FLAGGED | Add "urodynamics" to vocabulary or drop unreachable follow-up |
| MS-RR-S01 | E language | nit | initial_tool_outputs.csf.interpretation | "(N/A PMN/N/A lymph)" cosmetic artifact from combined Differential key vs S02/S03's separate keys | FLAGGED | Regenerate interpretation string or normalize cell_count key format |
| MS-RR-S01 | B internal-consistency | nit | patient.patient_id | ID format "NB-MS-RR-S01" inconsistent with S02/S03's "NB-MSRR-S0x" | FLAGGED | Standardize patient_id prefix format dataset-wide |
| MS-RR-S04 | C clinical-correctness | major | ground_truth.differential[2].icd_code | Neurosarcoidosis coded D86.85 (cardiac) | FIXED | Changed to D86.89 |
| MS-RR-S05 | C clinical-correctness | major | ground_truth.differential[3].icd_code | Neurosarcoidosis coded D86.85 (cardiac) | FIXED | Changed to D86.89 |
| MS-RR-S06 | C clinical-correctness | major | ground_truth.differential[3].icd_code | Neurosarcoidosis coded D86.85 (cardiac) | FIXED | Changed to D86.89 |
| MS-RR-S06 | B internal-consistency | major | ground_truth.differential[5].icd_code | "Spondylotic myelopathy" labeled diagnosis coded M47.812 ("without myelopathy"), contradicting its own label | FIXED | Changed to M47.12 |
| MS-RR-S04 | E language | minor | initial_tool_outputs.csf.interpretation | Placeholder "(N/A PMN/N/A lymph)" despite concrete differential (95% lymph/5% mono) | FIXED | Changed to "(0% PMN/95% lymph)" |
| MS-RR-S04 | C clinical-correctness | minor | ground_truth.differential[1].icd_code | MOGAD coded G36.9 instead of dedicated G37.81 | FLAGGED | Consider dataset-wide update to G37.81 |
| MS-RR-S05 | C clinical-correctness | minor | ground_truth.differential[1].icd_code | MOGAD coded G36.9 instead of dedicated G37.81 | FLAGGED | Dataset-wide sweep G36.9 -> G37.81 |
| MS-RR-S06 | C clinical-correctness | minor | ground_truth.differential[1].icd_code | MOGAD coded G36.9 instead of dedicated G37.81 | FLAGGED | Dataset-wide sweep G36.9 -> G37.81 |
| PACK | C clinical-correctness | minor | criteria_packs/MS-RR.md line 3 | "ICD-10: G35" stale; cases correctly use G35.A | FLAGGED | Update pack header (shared file) |
| MS-RR-S04 | terminology | nit | patient.patient_id | ID format inconsistent: S04/S06 "NB-MSRR-Sxx" vs S05 "NB-MS-RR-S05" | FLAGGED | Standardize patient_id prefix format dataset-wide |

**Tally:** 30 cases audited (M01-04, P01-05, RM01-04, RP01-05, RS01-06, S01-06) — 78 findings: 0 blocker / 20 major / 33 minor / 25 nit. 16 fixed, 62 flagged. Schema, coherence, and leakage validators: PASS.
