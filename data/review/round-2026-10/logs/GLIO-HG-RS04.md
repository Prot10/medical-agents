# GLIO-HG-RS04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| d02be965-432a-4b18-851b-a8ba17245499 | FIXED | `ground_truth.diagnosis.accepted[0]` "Giant cell glioblastoma, IDH-wildtype, WHO grade 4" changed to "Glioblastoma, IDH-wildtype, CNS WHO grade 4" (ruling 3, CENTRAL); `icd_codes` unchanged; synonyms untouched. Tissue reports: `integrated_diagnosis` "Glioblastoma, IDH-wildtype, CNS WHO grade 4"; `histological_diagnosis` "Glioblastoma with giant cell features (giant cell glioblastoma histological subtype), with microvascular proliferation and palisading necrosis"; `Histology` row "Glioblastoma with giant cell features: ...". "Conventional glioblastoma, IDH-wildtype" deleted from the differential. Tissue expected evidence and `metadata.condition_name` follow. |
| a091c170-4fdd-47b3-82ee-1dbd78387f39 | FIXED (add-BRAF option) | `BRAF_V600` added to `molecular_assays` (both alternatives) and to the tissue reports ("BRAF V600E: Not detected"); "Pleomorphic xanthoastrocytoma" added to the differential at low citing van den Bent 2025; `[vandenBent_2025]` on the tissue criterion. The literature step that carried the PXA distinction is deleted (C1); its fact (BRAF V600E separates giant-cell-rich glioblastoma from PXA) moved into the tissue rationale. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | patient.clinical_history.medications, HPI; must 4 | Levetiracetam called "seizure prophylaxis" after a documented GTC seizure; must said "initiate" although he takes it (C5 treat class, continue form) | FIXED: indication and HPI read "antiseizure treatment"; must "Continue levetiracetam ... this is treatment, not prophylaxis", with dose review (500 mg twice daily is low) and enzyme-inducer avoidance |
| A/C | major | action-3 literature criterion, follow-up, stop rule | Literature as a required step (C1) | FIXED: deleted |
| A/D | major | initial_tool_outputs.tissue_diagnosis | Tissue served upfront; template meta-text; "Microscopy" as a molecular finding (C2) | FIXED: initial null; resection and biopsy follow-ups; one Histology row; special stains (GFAP, p53, synaptophysin, neurofilament, reticulin, Ki-67) as findings rows only |
| C | major | action-10 | Stereotactic biopsy only (C3, group A); no IDH or ATRX assay (C4) | FIXED: resection then biopsy; assays IDH1_IHC, IDH1_IDH2_sequencing (age 52), ATRX_IHC, MGMT_methylation, BRAF_V600 |
| A/C | major | followup request_functional_mri | Tagged `fMRI_BOLD` (out of vocabulary), DTI content only in the impression (C6) | FIXED: retagged `functional_MRI`; new `DTI_tractography` follow-up (CST 8 mm, arcuate 5 mm, optic radiation 4 mm); recommended fMRI and DTI criteria with soft constraints. Rule from the MRI: dominant parietal tumour, hand motor cortex 12 mm, edema into the corona radiata and posterior limb, lesion reaching the atrium (sagittal stratum) |
| B/C | major | two `check_drug_interactions` follow-ups | Two outputs; em dashes | FIXED: merged into `check_dexamethasone_levetiracetam_temozolomide` (amlodipine, levetiracetam, dexamethasone, temozolomide); stays optional and last; expected evidence from the case |
| C | major | ground_truth | No performance status (C7) | FIXED: recommended criterion; follow-up KPS 60, ECOG 2 (walks with assistance, 3/5 right hemiparesis) |
| C | major | assessment must 6 | Template Stupp must (C11); KPS 60 and MGMT unmethylated make the branch conditional | FIXED: treatment chosen on post-operative KPS: 60 Gy/30 with temozolomide if KPS 70 or more, else hypofractionated 40 Gy/15 alone (MGMT unmethylated), trial reasonable (EANO 2021) |
| D | minor | initial_tool_outputs.eeg.impression | "indicate cortical irritability and seizure predisposition ... supports a structural etiology" (interpretive, cross-modality) | FIXED: ACNS impression listing the abnormalities |
| D | minor | initial_tool_outputs.mri.impression | Unnumbered | FIXED: numbered, dural contact as "dural invasion cannot be excluded" |
| C | minor | differential | "no CSF inflammation" for recurrent encephalitis, but no CSF exists in the case; IDH-mutant astrocytoma (under 55) not considered | FIXED: clause replaced with tissue; IDH-mutant astrocytoma grade 4 added at low |
| B | minor | labs CBC, coagulation | Template values (WBC 8.2, neutrophils 62, lymphocytes 28, PT 12.8, aPTT 28) | FIXED: WBC 6.9, neutrophils 60, lymphocytes 30, PT 12.5, aPTT 31 |
| C | minor | labs type_and_screen clinical_significance | Template engineering text | FIXED: null |
| C | minor | action-1, -2, -6, -7, -8, -9 | Template evidence; label-copy rationales; `[Stupp_2005]` on MRI | FIXED from the case's reports |
| E | minor | prohibited_recommendations[0] | "with herniation risk — herniation risk" | FIXED |
| C | minor | avoided_actions, sequence_constraints, stop_rule | Templates | FIXED as in the plan (section 3) |
| B | minor | metadata | condition name and counts | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The diagnosis is now glioblastoma, IDH-wildtype, CNS WHO grade 4, with giant cell features in the histology line, as WHO CNS5 classifies it. The pathway is contrast MRI, perfusion, spectroscopy, optional body CT, labs, performance status (KPS 60, ECOG 2), functional MRI and DTI (dominant parietal tumour: hand motor area 12 mm, arcuate 5 mm, optic radiation 4 mm), then tissue by maximal safe resection with biopsy as the fallback, testing IDH (IHC and sequencing), ATRX, MGMT and BRAF V600E (not detected, which with florid necrosis argues against pleomorphic xanthoastrocytoma, now in the differential at low), and one merged optional drug check last. Levetiracetam, which he takes since a GTC seizure nine months ago, is treatment and is continued with a dose review. After surgery treatment is chosen on the post-operative KPS with an unmethylated MGMT promoter.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Label change (ruling 3, reviewer d02be965): `accepted[0]` "Giant cell glioblastoma, IDH-wildtype, WHO grade 4" to "Glioblastoma, IDH-wildtype, CNS WHO grade 4" (plan section 5 item 3); the synonym guard passes.
- Citation keys `[vandenBent_2025]` and `[AIOM_brain]` on the tissue criterion (plan section 5 item 1).
- Synonym "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan section 5 item 2).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case; the plan's condition-wide questions apply.

## Verification
Checked: every note id in the notes file is in the table; each FIXED claim against the final JSON (assay lists in both tissue alternatives, one findings row and molecular_findings entry per required assay, resection and biopsy follow-ups with identical integrated diagnosis, initial tissue and literature null, literature criterion gone from criteria, constraints and stop rule, fMRI/DTI retagging, performance status follow-up, musts against allergies and medications, LP harm rationale against the MRI shift); laterality, sex, age and timeline across HPI, exam, MRI, EEG and tissue; lab arithmetic (anion gap, Hb/Hct, PT/INR); differential against the final evidence; leakage (any-query outputs, HPI); report voice. perfect_agent.py -v, case_io.py check and test_case_guards pass after the changes.
Found and changed:
- `initial_tool_outputs.mri.impression` ended with "Tissue diagnosis recommended." (plan C9). Removed.
Verified as sound: label change to "Glioblastoma, IDH-wildtype, CNS WHO grade 4" with giant cell features only in the histology line; BRAF V600E in both alternatives and in the report (not detected); PXA in the differential at low; the molecular profile (TP53 strongly positive, TERT wildtype, EGFR not amplified, reticulin around giant cells) fits the giant cell subtype, and grade 4 rests on MVP and necrosis; KPS 60 conditional treatment must (Stupp if KPS recovers to 70, else 40 Gy/15) is consistent with EANO 2021 and the unmethylated MGMT; levetiracetam continued as treatment.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `ground_truth.red_herrings[0].field_path` was empty: now `patient.clinical_history.past_medical_history[0]`.
- `fallback_tool_outputs.csf`: opening pressure 16 changed to 24 cm H2O, interpretation "Elevated opening pressure. Normal cell count, protein and glucose."; a normal pressure contradicts the documented papilloedema (same class as S02, S03, S04, S06).
- Drug check: temozolomide was proposed before any tissue diagnosis (plan C13). Now dexamethasone 4 mg IV every 6 hours and current levetiracetam 500 mg twice daily with amlodipine; temozolomide contraindication, interactions and warnings removed; warning added for Pneumocystis prophylaxis if dexamethasone continues for several weeks; label, expected evidence and rationale rewritten.
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).
