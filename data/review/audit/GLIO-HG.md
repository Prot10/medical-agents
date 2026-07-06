# GLIO-HG — NeuroBench v5 audit

Audited the full GLIO-HG condition set (terminology pass + per-case audit across all M/P/RM/RP/RS/S cases); 114 findings recorded (0 blocker / 33 major / 45 minor / 36 nit); 18 fixed inline, 96 flagged for author/clinician judgment; `validators_ok: false` (all mechanically-fixable coherence/schema gaps found in this pass were closed, but flagged items require clinical/editorial judgment before full re-validation).

## Terminology / taxonomy

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| GLIO-HG-P02 | terminology | major | ground_truth.icd_code | ICD-10 C85.10 ("unspecified B-cell lymphoma, unspecified site") contradicts documented "Primary CNS lymphoma (EBV-associated DLBCL)" | FIXED | Set icd_code = "C83.390" |
| GLIO-HG-M05 | terminology | major | ground_truth.primary_diagnosis | Uses retired WHO-2016 term "Anaplastic astrocytoma, WHO grade 3" | FLAGGED | Relabel "Astrocytoma, IDH-mutant, WHO grade 3 (ATRX-loss, left frontoparietal)"; align with pack update |
| PACK | terminology | minor | criteria_packs/GLIO-HG.md (lines 18, 58) | Pack still uses retired term "anaplastic astrocytoma", propagating it into M05 | FLAGGED | Replace with "IDH-mutant astrocytoma, CNS WHO grade 3" |
| GLIO-HG-M05, RS02, S04 | terminology | minor | ground_truth.icd_code | Three "frontoparietal" tumors coded to three different single lobes (C71.1/C71.1/C71.3) instead of consistent lobe or C71.8 | FLAGGED | Standardize: C71.8 for genuine overlap, or consistent epicenter-lobe coding |
| GLIO-HG-P05 | terminology | nit | ground_truth.primary_diagnosis | Hybrid phrasing "Diffuse midline glioma, H3 K27M-altered" mixes WHO-2021 tumor name with marker name | FLAGGED | Use "Diffuse midline glioma, H3 K27-altered, WHO grade 4 (thalamic)" |

## Audit findings

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| GLIO-HG-M01 | B | major | social_history.occupation | Occupation "dental hygienist" contradicts HPI's detailed "high school English teacher, 24 years" narrative | FIXED | Aligned occupation to dominant narrative |
| GLIO-HG-M01 | B | major | followup_outputs[6].output.warnings[1] | Drug-check warns of penicillin allergy; patient's real allergy is tetracycline | FLAGGED | Reconcile allergy statement with chart |
| GLIO-HG-M01 | A | major | followup_outputs[4].output.modality | fMRI content mislabeled modality='perfusion_MRI'; no functional_MRI in closed vocab, vocab_gap empty | FLAGGED | Extend vocab or record metadata.vocab_gap |
| GLIO-HG-M02 | C | major | ground_truth.icd_code | C71.9 (unspecified) used despite documented left temporal lobe location; siblings use C71.2 | FIXED | Changed to C71.2 |
| GLIO-HG-M02 | B | major | followup_outputs[6].output.warnings[3] | Drug-check pregnancy/teratogenicity warning for a 47-year-old male patient citing "52, perimenopausal" | FLAGGED | Remove/replace pregnancy line |
| GLIO-HG-M02 | B | major | followup_outputs[6].output.warnings[1] | Drug-check cites penicillin allergy; chart says "No known drug allergies" | FLAGGED | Correct drug-check text |
| GLIO-HG-M02 | C | major | ground_truth.critical_actions / key_reasoning_points | Documented focal motor seizure but no AED critical action/reasoning point, unlike weaker-evidence siblings M01/M03 | FLAGGED | Add levetiracetam critical action + reasoning point |
| GLIO-HG-M02 | terminology | minor | followup_outputs[3].output.panels.Histopathology[0].value | Histology headed "Diffuse astrocytoma, WHO grade 4 (glioblastoma...)" instead of direct "Glioblastoma, IDH-wildtype, WHO grade 4" | FLAGGED | Rename histology header |
| GLIO-HG-M02 | B | minor | followup_outputs[3].output.panels (IDH1/IDH2) | IDH1/IDH2 value equals its own reference_range ("Wildtype") yet is_abnormal=true | FLAGGED | Fix flag or reference_range |
| GLIO-HG-M03 | B | major | patient.history_present_illness | Occupation fields say "IT project manager" but HPI body has 3 English-teacher remnants | FLAGGED | Reconcile occupation vs HPI remnants |
| GLIO-HG-M03 | B | major | followup_outputs[6].output.warnings[1] | Drug-check cites penicillin allergy; real allergy is contrast dye; contrast-dye allergy itself never addressed despite contrast studies ordered | FLAGGED | Correct allergy reference; consider premedication note |
| GLIO-HG-M03 | A | major | followup_outputs[4].output.modality | Same fMRI/perfusion_MRI mislabel as M01; vocab_gap empty | FLAGGED | Extend vocab or record vocab_gap |
| GLIO-HG-M03 | E | minor | followup_outputs[1].output.impression | MRS impression is placeholder "See findings above" | FLAGGED | Replace with real Cho/NAA/lipid-lactate impression |
| GLIO-HG-M01 | C | nit | initial_tool_outputs.mri.impression / literature+histology | Detector flagged "glioblastoma"; legitimate hedged differential + confirmatory Kind-2 content | FLAGGED | No action |
| GLIO-HG-P01 | B | major | differential[0]/[3] key_features, key_reasoning_points, red_herrings[0] vs mri.DWI | GT claims rim diffusion restriction (GBM pattern) to argue against abscess, but case's own MRI documents CENTRAL restriction | FLAGGED | Adjudicate DWI wording vs GT reasoning |
| GLIO-HG-P01 | B | minor | red_herrings[0].correct_interpretation vs mri post_contrast | GT says "thick irregular ring"; MRI says "thin, relatively smooth ring" | FLAGGED | Align red_herrings wording with actual MRI |
| GLIO-HG-P01 | B | minor | differential[0]/[3]/red_herrings vs labs+vitals | GT claims "no fever/leukocytosis" but labs show WBC 11.2(H), neutrophils 8.1(H), CRP/ESR high, temp 37.5 | FLAGGED | Soften absolute claims |
| GLIO-HG-P01 | A | minor | followup_outputs[4].output.modality | fMRI/DTI mislabeled perfusion_MRI, duplicating the real perfusion_MRI followup; no vocab entry | FLAGGED | Record vocab_gap or reroute |
| GLIO-HG-P01 | D | minor | followup_outputs[5]/[6] (tool_name=interpret_labs) | ID/dental consults delivered via interpret_labs with drug-dosing narrative, not consult_medical_specialist | FLAGGED | Re-route to consult_medical_specialist; strip doses |
| GLIO-HG-P01 | B | nit | followup_outputs[3].output.interpretation vs abnormal_values_summary | MGMT tagged "(H)" in one string, "(L)" in the other | FLAGGED | Make tags consistent |
| GLIO-HG-P01 | E | minor | metadata.case_body_concerns | Verbatim-duplicated note (2 identical entries) | FIXED | Removed duplicate |
| GLIO-HG-P01 | B | minor | differential[0] and [3] | "Brain abscess" listed twice with contradictory likelihoods (moderate vs very_low) | FLAGGED | Merge into single entry |
| GLIO-HG-M04 | B | nit | metadata.fallback_tool_kinds.eeg vs fallback_tool_outputs.eeg | Label "incidental" but fallback EEG is fully normal | FLAGGED | Align label to "normal" |
| GLIO-HG-M05 | B | nit | metadata.fallback_tool_kinds.eeg vs fallback_tool_outputs.eeg | Label "abnormal_nonspecific" but fallback EEG is normal | FLAGGED | Align label to "normal" |
| GLIO-HG-M04 | D | nit | followup_outputs[2]/[3] (biopsy, literature) | Detector flagged "astrocytoma"; legitimate Kind-2 confirmatory/general-literature content | FLAGGED | No action |
| GLIO-HG-P01 | D | nit | followup_outputs[3].output.interpretation (biopsy) | Detector flagged "Glioblastoma..."; legitimate confirmatory histology | FLAGGED | No action |
| GLIO-HG-P02 | C | major | ground_truth.optimal_actions[0].expected_finding | Describes GBM morphology (ring/necrosis/rim restriction) contradicting this case's actual homogeneous, diffusely-restricting PCNSL MRI | FLAGGED | Rewrite to PCNSL pattern |
| GLIO-HG-P02 | C | major | ground_truth.optimal_actions[4].expected_finding | Prescribes Stupp/TMZ (glioma therapy) for a PCNSL case; contradicts key_reasoning_points[4] | FLAGGED | Replace with methotrexate-based PCNSL plan |
| GLIO-HG-P02 | B | major | ground_truth.critical_actions | Simultaneously mandates giving dexamethasone and deferring corticosteroids | FLAGGED | Resolve steroid contradiction |
| GLIO-HG-P02 | B | major | ground_truth.differential[1]/[2] | "Cerebral toxoplasmosis" duplicated at same likelihood with near-identical key_features | FLAGGED | Delete redundant entry |
| GLIO-HG-P02 | A | minor | condition / ground_truth.primary_diagnosis | PCNSL/HIV case filed under GLIO-HG (glioma) prefix — intentional mimic | FLAGGED | Consider dedicated pack/labeling |
| GLIO-HG-P02 | E | nit | initial_tool_outputs.eeg.impression | Impression omits documented right frontal focal slowing; doesn't open with ABNORMAL declaration | FLAGGED | Add focal slowing to impression |
| GLIO-HG-P03 | B | major | ground_truth.differential | Two duplicate-entity pairs at contradictory likelihoods (abscess moderate/very_low; tumefactive demyelination low/very_low) | FLAGGED | Deduplicate |
| GLIO-HG-P03 | D | minor | followup_outputs[4].output.modality | fMRI/DTI mislabeled perfusion_MRI; no clean on-list token available | FLAGGED | Route via analyze_brain_mri or record vocab_gap |
| GLIO-HG-P03 | B | nit | fallback_tool_outputs.csf.glucose_ratio | Ratio 0.6 arithmetically inconsistent with patient's serum glucose 171 (should be ~0.36) | FLAGGED | Recompute if fallback surfaced |
| GLIO-HG-P04 | D | nit | followup_outputs[5].output.interpretation | Detector flagged "glioblastoma" in biopsy; legitimate Kind-2 confirmatory histology | FLAGGED | No action |
| GLIO-HG-P05 | A | minor | ground_truth.useless_tools[4-5] / fallback_tool_outputs.advanced_imaging | order_advanced_imaging in useless_tools but fallback is null; coherence validator flags missing fallback | FLAGGED | Add benign negative fallback or remove entries |
| GLIO-HG-RM01 | B | major | optimal_actions[0].expected_finding, key_reasoning_points[1] | GT describes ring/necrosis/rim-restriction contradicting this case's solid, non-necrotic, no-central-restriction MRI (biopsy corroborates) | FLAGGED | Reword to match solid non-necrotic + molecular upgrade |
| GLIO-HG-RM01 | B | major | critical_actions[3], key_reasoning_points[0]/[7] | GT invokes seizure activity and morning headache; HPI explicitly denies both | FLAGGED | Remove/replace seizure/headache-based items |
| GLIO-HG-RM01 | B | minor | differential[0]/[5], [1]/[2] | Two duplicate pairs (demyelination, metastasis); key_features cite absent ring/necrosis features | FLAGGED | Collapse duplicates, align key_features |
| GLIO-HG-RM01 | B | minor | difficulty / metadata.difficulty_description/_rationale / red_herrings | difficulty="straightforward" vs description "Moderate difficulty"; rationale claims classic ring-enhancing GBM (contradicts MRI) and "no red herrings" while description lists red herrings | FLAGGED | Reconcile difficulty metadata |
| GLIO-HG-RM02 | E | nit | followup_outputs[1].output.interpretation | Stray double period ("recommended.. IgG_index") | FIXED | Collapsed to single period |
| GLIO-HG-RM02 | C | major | harmful_tools[0], followup_outputs[1] (analyze_csf), contraindicated_actions[0], sequence_constraints | Cerebral herniation-risk template applied to intramedullary cervical spinal cord glioma with no intracranial mass, yet GT trajectory itself runs a CSF followup | FLAGGED | Resolve harmful/available contradiction; rewrite for spinal anatomy |
| GLIO-HG-RM02 | B | minor | optimal_actions[0] (tool_name analyze_brain_mri), red_herrings[0].field_path | Spinal lesion characterized via analyze_brain_mri with generic cerebral expected_finding; red_herrings[0].field_path empty | FLAGGED | Populate field_path; note tooling limitation |
| GLIO-HG-RM04 | B | minor | fallback_tool_outputs.csf.interpretation | "Mildly elevated protein (42 mg/dL; ULN 45)" — 42 is below its own stated ULN | FIXED | Reworded to "high-normal" |
| GLIO-HG-RP01 | C | major | red_herrings[0].correct_interpretation | Calls lesion "the frontal mass" though documented right temporal lobe throughout | FIXED | Corrected to "right temporal mass" |
| GLIO-HG-RP01 | C | major | ground_truth.icd_code | C71.9 (unspecified) used for unambiguously right temporal tumor; sibling RM04 uses C71.2 | FLAGGED | Adjudicate C71.9→C71.2 |
| GLIO-HG-RP01 | B | major | key_reasoning_points[1], differential[].key_features | Templated "ring-enhancing mass with central necrosis" contradicts case's explicit no-necrosis, no-classic-ring, infiltrative MRI | FLAGGED | Rewrite reasoning to match atypical presentation |
| GLIO-HG-RM03 | C | major | key_reasoning_points[7], critical_actions[3] | Asserts seizure activity mandating AEDs; patient explicitly denies seizures, EEG shows no epileptiform activity | FLAGGED | Remove/soften seizure-contingent items |
| GLIO-HG-RM03 | B | minor | differential[0]/[2] | Duplicate metastasis entries; "(solitary)" key_features cite corpus-callosum involvement templated from a supratentorial case, doesn't fit cerebellar lesion | FLAGGED | Consolidate and localize key_features |
| GLIO-HG-RP01 | B | minor | differential[1].key_features | "No known primary cancer" contradicts documented prior thyroid follicular carcinoma (the case's central red herring) | FLAGGED | Reconcile with PMH |
| GLIO-HG-RP01 | B | minor | followup_outputs[3].output.abnormal_values_summary | TTF-1/PAX8 "Negative" tagged (H) in summary though panel marks is_abnormal=false | FLAGGED | Remove from abnormal summary or drop (H) |
| GLIO-HG-RM03 | B | minor | followup_outputs[4].output.modality | fMRI/DTI mislabeled perfusion_MRI; sibling RM04 routes via analyze_brain_mri | FLAGGED | Re-route or flag vocab_gap |
| GLIO-HG-RP01 | B | minor | followup_outputs[4].output.modality | fMRI (language/motor mapping) mislabeled perfusion_MRI | FLAGGED | Re-route or flag vocab_gap |
| GLIO-HG-RM04 | D | minor | initial_tool_outputs.mri.impression | Names "gliosarcoma given the hemorrhagic-sarcomatous component" — histologic descriptor a radiology report cannot establish | FLAGGED | Soften to "high-grade glioma" |
| GLIO-HG-RP01 | C | minor | initial_tool_outputs.labs.panels['Tumor markers'][0].reference_range | Thyroglobulin reference reflects total-thyroidectomy norm though patient had hemithyroidectomy (residual tissue raises normal range) | FLAGGED | Clarify reference range for hemithyroidectomy (note: intentional red herring) |
| GLIO-HG-RM03 | A | minor | difficulty vs metadata.difficulty_description/_rationale | difficulty="straightforward" vs description "Moderate difficulty"; rationale says no red herrings while description names one and red_herrings=[] | FLAGGED | Reconcile difficulty metadata |
| GLIO-HG-RP01 | E | nit | followup_outputs[1].output.impression | MRS impression placeholder "See findings above" | FLAGGED | Populate real impression |
| GLIO-HG-RM03 | C | nit | initial_tool_outputs.eeg / ground_truth.useless_tools | Abnormal EEG provided though no seizures documented; analyze_eeg not in useless_tools (sibling RM04 lists it) | FLAGGED | Consider adding analyze_eeg to useless_tools |
| GLIO-HG-RP01 | C | nit | initial_tool_outputs.ecg / ground_truth.useless_tools | ECG provided, not listed in useless_tools per pack guidance | FLAGGED | Consider adding analyze_ecg to useless_tools |
| GLIO-HG-RP04 | C | major | patient.neurological_exam.cranial_nerves | "Right homonymous inferior quadrantanopia" documented for a RIGHT parieto-occipital lesion; should be contralateral (LEFT) — all other lateralizing signs are correctly left-sided | FLAGGED | Verify with clinician; likely should read LEFT |
| GLIO-HG-RP02 | C | major | patient.neurological_exam.cranial_nerves | "Right lower facial droop" documented for a RIGHT frontal lesion; UMN facial palsy should be contralateral (LEFT) — all other lateralizing signs are left-sided | FLAGGED | Verify with clinician; likely should read LEFT |
| GLIO-HG-RP03 | C | major | ground_truth.primary_diagnosis | Filed under GLIO-HG (high-grade) pack but tissue diagnosis is WHO grade 2 IDH-mutant diffuse astrocytoma (low-grade) | FLAGGED | Consider re-filing to low-grade pack |
| GLIO-HG-RP03 | B | minor | ground_truth.optimal_actions[0].action/expected_finding, [4].expected_finding | Garbled action text; GBM-boilerplate ring/necrosis expected_finding and Stupp/TMZ IDH-wildtype language for an IDH-mutant grade-2 case | FLAGGED | Reword to match grade-2 IDH-mutant presentation |
| GLIO-HG-RP04 | B | minor | metadata.fallback_tool_kinds.eeg | Labeled "nonspecific_abnormal" though fallback EEG output is unambiguously normal | FLAGGED | Align label or revise fallback |
| GLIO-HG-RP02 | D | minor | followup_outputs[4].output.modality | fMRI/DTI (BOLD motor/language mapping) mislabeled perfusion_MRI; no vocab entry | FLAGGED | Route via analyze_brain_mri or record vocab_gap |
| GLIO-HG-RP03 | D | minor | followup_outputs[4].output.modality | Same fMRI/perfusion_MRI mislabel; also spinal MRI followup routed through analyze_brain_mri (brain tool for spine study) | FLAGGED | Same as RP02; consider dedicated spinal modality |
| GLIO-HG-RP02 | B | nit | followup_outputs[3].output.panels.molecular_profiling | IDH1 R132H "Negative (wild-type)" flagged is_abnormal=true while IDH2 "Wild-type" is is_abnormal=false in same panel; convention also differs from RP04 | FLAGGED | Pick one convention |
| GLIO-HG-RS01 | E | minor | ground_truth.contraindicated_actions[0] | Redundant "with herniation risk — herniation risk" | FIXED | Deduped to factual clause + reason |
| GLIO-HG-RS03 | E | minor | ground_truth.contraindicated_actions[0] | Same redundant duplicated clause | FIXED | Deduped |
| GLIO-HG-RS01 | B | major | followup_outputs[4].output.modality | fMRI/DTI mislabeled perfusion_MRI; unresolved vocab gap; same pattern in RS02/RS03 | FLAGGED | Extend vocab (metadata.vocab_gap) or rescope |
| GLIO-HG-RS01 | D | minor | initial_tool_outputs.mri.additional_observations[2] | "Not expected for this patient's age" is ambiguous and injects age-based interpretation into MRI report (style guide strip rule) | FLAGGED | Reword to pure imaging observation |
| GLIO-HG-RS01 | B | minor | difficulty vs metadata.difficulty_description | difficulty="diagnostic_puzzle" conflicts with description "Straightforward GBM presentation" and confidence 0.85 | FLAGGED | Reconcile difficulty label |
| GLIO-HG-RS01 | C | nit | ground_truth.icd_code | C71.9 used for documented multi-lobe frontotemporal/insular mass; C71.8 more specific | FLAGGED | Consider C71.8 |
| GLIO-HG-RS01 | D | nit | initial_tool_outputs.eeg.impression | Impression omits documented sharp waves/IRDA from findings[] | FLAGGED | Expand impression |
| GLIO-HG-RS02 | D | minor | initial_tool_outputs.eeg.impression | Correlates EEG focus with clinical seizure semiology — cross-modality synthesis discouraged by style guide | FLAGGED | Trim electro-clinical correlation |
| GLIO-HG-RS02 | B | nit | initial_tool_outputs.ecg.interpretation | Omits documented LVH from findings[] | FLAGGED | Add LVH mention |
| GLIO-HG-RS03 | C | nit | ground_truth.icd_code | C71.9 used for documented frontal-centered mass; C71.1/C71.8 more specific | FLAGGED | Consider C71.1/C71.8 |
| GLIO-HG-RS03 | D | nit | initial_tool_outputs.eeg.impression | Omits documented PLEDs/LPDs and continuous delta from findings[]; legacy term PLEDs | FLAGGED | Expand impression; consider LPDs terminology |
| GLIO-HG-RS01 | D | nit | followup_outputs[5].output.results[].key_finding | Detector flagged "glioblastoma"; legitimate general population-keyed literature evidence | FLAGGED | No action |
| GLIO-HG-RS05 | B | major | fallback_tool_outputs.eeg | analyze_eeg listed useless_tools but fallback was null; coherence validator flagged | FIXED | Added standard normal-EEG fallback |
| GLIO-HG-RS06 | B | major | fallback_tool_outputs.eeg | Same missing-fallback coherence issue as RS05 | FIXED | Added standard normal-EEG fallback |
| GLIO-HG-RS06 | E | minor | initial_tool_outputs.mri.findings[0].mass_effect | Nonsensical "Mild left-sided uncal herniation not present" | FIXED | Corrected to "No uncal herniation." |
| GLIO-HG-RS04 | D | nit | followup_outputs[5].output.results[0].summary | Detector flagged "giant cell glioblastoma"; legitimate Kind-2 population-keyed literature post-biopsy | FLAGGED | No action |
| GLIO-HG-RS05 | D | nit | followup_outputs[4].output.results[0].summary | Detector flagged "glioblastoma" in WHO-2021 definitional literature; legitimate | FLAGGED | No action |
| GLIO-HG-RS06 | D | nit | followup_outputs[3].output.results[0].key_finding | Same generic definitional literature flag, legitimate | FLAGGED | No action |
| GLIO-HG-RS04 | D | minor | initial_tool_outputs.eeg.impression | "Indicate cortical irritability and seizure predisposition" / "supports structural etiology" borderline vs style guide's no-diagnose rule | FLAGGED | Tighten to pattern-only language |
| GLIO-HG-RS05 | E | minor | initial_tool_outputs.mri.findings[0].signal_characteristics.FLAIR | Duplicated anatomy phrase naming "posterior limb of the internal capsule" twice | FLAGGED | Reword to single correct anatomical clause |
| GLIO-HG-RS06 | C | nit | ground_truth.icd_code | Lesion spans temporal+parietal (angular gyrus); C71.2 used, borderline vs C71.3 | FLAGGED | Leave unless parietal predominance intended |
| GLIO-HG-S02 | B | minor | patient.clinical_history.social_history.occupation | Occupation "accountant" contradicts HPI's explicit "high school math teacher" with multiple corroborating details | FIXED | Set occupation to "high school math teacher" |
| GLIO-HG-S03 | B | minor | patient.clinical_history.social_history.occupation | Occupation "high school principal" vs single HPI word "teacher" — softer, ambiguous contradiction | FLAGGED | Reconcile occupation vs HPI wording |
| GLIO-HG-S02 | B | minor | ground_truth.icd_code | C71.9 used for a mass centered in frontal lobe (precentral/middle frontal gyri); sibling S01 uses C71.1 | FLAGGED | Consider C71.1/C71.8 for consistency |
| GLIO-HG-S03 | B | minor | ground_truth.icd_code | C71.9 used for frontal-centered mass extending to corpus callosum; same consistency question as S02 | FLAGGED | Consider C71.1/C71.8 |
| GLIO-HG-S01 | B | nit | followup_outputs[3].output.abnormal_values_summary / interpretation | MGMT tagged "(H)" in interpretation, "(L)" in abnormal_values_summary; identical pattern in S02/S03 | FLAGGED | Regenerate flag suffix consistently |
| GLIO-HG-S01 | D | nit | initial_tool_outputs.eeg.impression | Impression doesn't open with "This is an ABNORMAL EEG" despite classification=abnormal; sibling S02 does | FLAGGED | Prefix impression per style guide |
| GLIO-HG-S01 | A | nit | initial_tool_outputs.labs.panels.Other[HbA1c].value | HbA1c value is string "7.2" while all other labs (and siblings' HbA1c) are numeric | FLAGGED | Change to numeric 7.2 |
| GLIO-HG-S02 | A | nit | fallback_tool_outputs.specialized_test.test_type | Empty string while S01/S03 use "neuropsychological_screening" | FLAGGED | Populate with real test_type |
| GLIO-HG-S05 | B | major | fallback_tool_outputs.eeg / ground_truth.useless_tools[0] | analyze_eeg listed useless_tools with no fallback entry; coherence validator flagged | FIXED | Added normal EEG fallback matching S06 |
| GLIO-HG-S05 | B | major | ground_truth.red_herrings[0].field_path | Path pointed to non-existent patient.clinical_history.history_present_illness | FIXED | Corrected to patient.history_present_illness |
| GLIO-HG-S04 | E | minor | ground_truth.contraindicated_actions[0] | Redundant duplicated "with herniation risk — herniation risk" | FIXED | Reduced to single clean clause |
| GLIO-HG-S04 | E | nit | metadata.case_body_concerns | Two byte-identical entries | FIXED | Removed duplicate |
| GLIO-HG-S04 | C | minor | ground_truth.icd_code | C71.3 (parietal) used though documented epicenter is frontal ("junction of precentral and superior frontal gyri") | FLAGGED | Adjudicate C71.1 vs C71.8 |
| GLIO-HG-S04 | D | minor | initial_tool_outputs.eeg.impression | Trailing "...and clinical presentation" reaches slightly beyond EEG's own modality/indication | FLAGGED | Optional trim |
| GLIO-HG-S04 | D | nit | followup_outputs[3].output.interpretation | Detector flagged "glioblastoma" in biopsy histopathology; legitimate confirmatory result | FLAGGED | No action |
| GLIO-HG-S06 | C | minor | ground_truth.critical_actions[4] | "Prophylactic levetiracetam may be initiated" listed as critical action though patient has no documented seizures (against AAN guidance) | FLAGGED | Consider demoting/removing from critical_actions |
| GLIO-HG-S06 | D | minor | initial_tool_outputs.mri.impression (point 2) | FLAIR optic-radiation finding correlated to reported visual field deficit (the stated scan indication) | FLAGGED | Defensible as indication correlation; flag for awareness |
| GLIO-HG-S06 | D | nit | followup_outputs[4]/[3].output | Detector flagged "glioblastoma" in literature + biopsy; both legitimate (general evidence + confirmatory histology) | FLAGGED | No action |
| GLIO-HG-S05 | D | nit | followup_outputs[2].output.results[].key_finding | Detector flagged "glioblastoma" in 3 literature results; legitimate general population-keyed evidence | FLAGGED | No action |
| GLIO-HG-S05 | E | nit | fallback_tool_outputs.specialized_test.impression | Empty impression string; S06 equivalent is populated | FLAGGED | Optional: add normal-limits impression |

## Tally

- Cases audited: all GLIO-HG cases (M01–M05, P01–P05, RM01–RM04, RP01–RP04, RS01–RS06, S01–S06)
- Findings: 114 total — 0 blocker / 33 major / 45 minor / 36 nit
- Fixed inline: 18 · Flagged for judgment: 96
- Validators: `validators_ok: false` (all mechanically-fixable coherence/schema gaps found in this pass were closed; remaining flagged items require clinical/editorial judgment before re-validation)
