# GLIO-HG-RS03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 92ef1523-7d5e-4e1d-9191-8ca53890c7b1 | FIXED | `initial_tool_outputs.labs.panels["Exclusion studies"]` (serum `chr7_gain_chr10_loss`) deleted; +7/-10 reported only on tissue ("Present"). |
| b0d00a8d-5dd2-4a0e-883d-2068a0506684 | FIXED | `action-10-obtain-tissue-diagnosis` `molecular_assays` now `IDH1_IHC`, `IDH1_IDH2_sequencing` (age 31), `ATRX_IHC`, `MGMT_methylation` in both alternatives. Tissue reports: IDH1 R132H IHC negative, IDH1/IDH2 sequencing wildtype, ATRX retained, MGMT methylated (plus TERT mutation, EGFR not amplified, +7/-10 present, 1p/19q not codeleted, H3F3A K27/G34 wildtype). |
| f4b30a6a-9e66-422a-848b-56938528005a | FIXED (impression-plus-action option) | EEG impression now opens "This is an ABNORMAL EEG due to: 1. Lateralized periodic discharges (LPDs) at 1 to 1.5 Hz over the right frontocentral region (F4, C4) ..."; finding renamed from "PLEDs" to ACNS "Lateralized periodic discharges (LPDs)". New recommended `action-eeg-characterise-spells` (`analyze_eeg`, served by the initial EEG), label "Order an EEG to characterise the post-ictal state after a first focal to bilateral seizure". Must added verbatim from the plan: "Continue EEG monitoring given LPDs after a first seizure, and escalate antiseizure treatment if electrographic seizures appear." |
| d061a446-8bfc-4815-bfda-9be5647b2de1 | FIXED | Tissue criterion `resection` first, `stereotactic_biopsy` second; canonical label, rationale and surgery must (interchangeable "stereotactic biopsy or maximal safe resection" must deleted). fMRI follow-up retagged `functional_MRI` (5 mm from the inferoposterior margin); new `DTI_tractography` follow-up (CST displaced, thinned, reduced FA, 3 mm); recommended `action-fmri-functional-mapping` and `action-dti-tractography` with soft constraints to tissue. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C/B | major | initial_tool_outputs.eeg.findings | "Breach rhythm" over the right frontocentral region with higher amplitude, in a patient with no skull defect and an attenuated right background (a breach rhythm requires a craniotomy or skull defect) | FIXED: finding deleted |
| B | major | patient.neurological_exam.additional | A second two-minute GTC seizure "in the emergency department", not in the HPI (template carry-over, same as RS02) | FIXED: "No further seizure activity in the emergency department" |
| C | major | musts 3 and 4 | Dexamethasone and levetiracetam already started in the ED per HPI; musts said "administer"/"initiate" | FIXED: continue forms (C5 treat class, C8) with dose review and enzyme-inducer avoidance |
| A/C | major | action-3 literature criterion, follow-up, stop rule | Literature as a required step (C1) | FIXED: deleted |
| A/D | major | initial_tool_outputs.tissue_diagnosis | Tissue served upfront; template meta-text; "Microscopic description" as a molecular finding (C2) | FIXED: initial null; resection and biopsy follow-ups with a `Histology` row |
| C | minor | tissue, differential | Hemispheric IDH-wildtype glioma at 31: H3 G34 and IDH-mutant astrocytoma are the age-relevant mimics; GBM IDH-wildtype requires H3-wildtype | FIXED: H3F3A K27/G34 row (wildtype); both entities added to the differential at low |
| C | major | assessment | Combined oestrogen contraceptive not addressed before major neurosurgery in a high-grade glioma (VTE risk), and contraception needed on temozolomide | FIXED: must to withhold the combined pill with mechanical thromboprophylaxis and switch to a non-oestrogen method; DDI output corrected (dexamethasone CYP3A4 induction, levetiracetam spares contraceptive efficacy) |
| C | major | assessment must 6 | Template Stupp must (C11); sulfonamide allergy relevant to Pneumocystis prophylaxis | FIXED: age, KPS and entity specific must with fertility counselling and non-co-trimoxazole prophylaxis |
| C | major | ground_truth | No performance status (C7) | FIXED: recommended criterion, follow-up KPS 80, ECOG 1 |
| C | minor | labs | No pregnancy test before anaesthesia in a 31-year-old woman | FIXED: serum beta-hCG <2 mIU/mL added to the lab report (not required by the criterion) |
| B | minor | labs CBC, coagulation | Values identical to the template (WBC 8.2, neutrophils 62, lymphocytes 28, PT 12.8) | FIXED: WBC 7.4, neutrophils 58, lymphocytes 32, PT 12.1 |
| C | minor | labs type_and_screen clinical_significance | Template engineering text | FIXED: null |
| D | minor | initial_tool_outputs.mri.impression | Unnumbered; fine otherwise | FIXED: numbered imaging-only impression |
| E | minor | followup CT CAP | Em dash; "physiologic ... incidental" | FIXED: "Simple left ovarian cyst (1.5 cm)" |
| C | minor | red_herrings, key_clinical_evidence | Her migraine history is a distractor not declared | FIXED: red herring added; key evidence rewritten from the case |
| C | minor | action-1, -2, -6, -7, -8, -9 | Template expected evidence and label-copy rationales; `[Stupp_2005]` on MRI; "right hemisphere lesion" | FIXED from the case's own reports |
| C | minor | avoided_actions, prohibited_recommendations[0] | Template waste rationales; LP text with an em dash | FIXED |
| C | minor | sequence_constraints, stop_rule | Template | FIXED: hard MRI and labs to tissue, soft fMRI and DTI to tissue; stop rule MRI, labs, tissue |
| B | minor | metadata.difficulty_rationale | Counts out of date | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway is contrast MRI, perfusion, spectroscopy, EEG (now recommended: right frontocentral LPDs at 1 to 1.5 Hz are in the impression), optional body CT, pre-operative labs (with a negative beta-hCG), performance status (KPS 80, ECOG 1), functional MRI (hand motor area 5 mm from the margin) and DTI (thinned corticospinal tract 3 mm away), then tissue by maximal safe resection with biopsy as the fallback (IDH1 R132H, IDH1/IDH2 sequencing, ATRX, MGMT), and an optional drug check last. The breach rhythm (impossible without a skull defect) and the duplicated ED seizure are gone. Musts continue the dexamethasone and levetiracetam started in the ED, keep EEG monitoring for the LPDs, withhold the combined oral contraceptive around surgery with a switch to non-oestrogen contraception, and after the integrated diagnosis give 60 Gy/30 with temozolomide, fertility counselling, and Pneumocystis prophylaxis that avoids co-trimoxazole (sulfonamide allergy).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Vocabulary: an H3 G34 status assay (reported here as a findings row only).
- Citation key `[AIOM_brain]` used on the tissue and EEG criteria (plan section 5 item 1).
- Synonym "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan section 5 item 2).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case; the plan's condition-wide questions apply.

## Verification
Checked: every note id in the notes file is in the table; each FIXED claim against the final JSON (assay lists in both tissue alternatives, one findings row and molecular_findings entry per required assay, resection and biopsy follow-ups with identical integrated diagnosis, initial tissue and literature null, literature criterion gone from criteria, constraints and stop rule, fMRI/DTI retagging, performance status follow-up, musts against allergies and medications, LP harm rationale against the MRI shift); laterality, sex, age and timeline across HPI, exam, MRI, EEG and tissue; lab arithmetic (anion gap, Hb/Hct, PT/INR); differential against the final evidence; leakage (any-query outputs, HPI); report voice. perfect_agent.py -v, case_io.py check and test_case_guards pass after the changes.
Found and changed:
- `initial_tool_outputs.mri.impression` ended with "Tissue diagnosis recommended." (plan C9). Removed.
- Template imaging numbers shared with RS01 and RS02 (PATTERNS 4): rCBV 4.1 / necrotic core 0.3 and edema 95 cm3. Changed to rCBV 5.2 and 0.2 (perfusion findings and impression), edema 104 cm3 (MRI volumetrics), and rCBV 5.2 in `action-6` expected evidence and `key_clinical_evidence[2]`.
Verified as sound: LPDs at 1 to 1.5 Hz over F4/C4 now in the EEG impression and in the recommended EEG criterion; breach rhythm removal (no skull defect); EEG monitoring must; COC withdrawal and non-oestrogen contraception must; beta-hCG negative; MRS ratios agree (Cho/Cr 4.2 / NAA/Cr 0.3 = 14.0). The EEG criterion cites `[AIOM_brain]` like the other EEG criteria of the condition; left for the lead's citation pass.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `ground_truth.red_herrings[0].field_path` was empty: now `patient.clinical_history.past_medical_history[0]`.
- `fallback_tool_outputs.csf`: opening pressure 16 changed to 25 cm H2O, interpretation "Elevated opening pressure. Normal cell count, protein and glucose."; a normal pressure contradicts the documented papilloedema (same class as S02, S03, S04, S06).
- Drug check contraindication "during concomitant temozolomide" now "if Pneumocystis prophylaxis becomes necessary, use an alternative agent (inhaled pentamidine or atovaquone)" (no temozolomide before tissue, plan C13).
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).
