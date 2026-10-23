# GLIO-HG-S03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The notes file has no note for GLIO-HG-S03. The condition classes of the plan were applied (below). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.history_present_illness` | Seizure from a right frontal focus with "eyes deviated to the right": ictal version is away from the focus, so a right frontal seizure turns the eyes to the left. | FIXED: "his eyes and head turned to the left". Kept in the treat must. |
| B | major | `patient.history_present_illness`, `initial_tool_outputs.mri.findings[0].mass_effect` | "8 mm of left-to-right midline shift" for a right frontal mass (the shift is leftward). | FIXED: "leftward midline shift" in both. |
| B | major | `patient.neurological_exam.mental_status`, HPI | Word-finding difficulty and paraphasic errors in a right-handed man with a right frontal tumour while fMRI shows left language dominance remote from the tumour (template copied from S02). | FIXED: HPI "slower to respond in conversations"; exam "fluent with intact naming and repetition and no paraphasic errors; responses are slow". The ictal speech arrest stays (supplementary motor seizures can arrest speech from either side). |
| B | major | `patient.neurological_exam.cranial_nerves` | Left homonymous hemianopia that the lesion (superior and middle frontal gyri, edema to the parietal white matter and internal capsule, no temporal or occipital involvement) does not explain; template from S02. | FIXED: "Visual fields full to confrontation." |
| E | minor | HPI | "uncharacteristic for him as a teacher" while the occupation is high school principal. | FIXED: "as a school principal". |
| C | major | `followup_outputs` drug check | Check of temozolomide before any tissue diagnosis (treatment the agent cannot yet recommend), with "patient has sulfa allergy" while the only allergy is latex (plan C13, ruling 6). | FIXED: replaced by a dexamethasone and levetiracetam check against metformin, amlodipine, lisinopril, atorvastatin and tamsulosin; no allergy line. Criterion stays optional and last; guard passes. |
| C | major | `required_recommendations` | Latex allergy not addressed although surgery is planned. | FIXED: must "Record the latex allergy (contact dermatitis) for a latex-safe operating theatre and ward." |
| C | major | `required_recommendations` | HPI states levetiracetam and dexamethasone were started in the ED, but the musts "initiate" both (plan C5 continue form, C8). | FIXED: "Continue levetiracetam ... review the dose", canonical treat wording; "Continue dexamethasone ... lowest effective dose ... taper after surgery". |
| C | major | `action-3-search-medical-literature`, literature follow-up | Required literature step (ruling 5, plan C1). | FIXED: criterion, follow-up and stop-rule entry deleted. |
| D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue served upfront; template impression (plan C2). | FIXED: initial null; resection and stereotactic-biopsy follow-ups; `Histology` row; canonical impression with MGMT. |
| C | major | `action-10-obtain-tissue-diagnosis` | Biopsy only; assay list without IDH or ATRX and with 1p/19q (plan C3, C4; age 52). | FIXED: `resection` then `stereotactic_biopsy`, each `IDH1_IHC`, `IDH1_IDH2_sequencing`, `ATRX_IHC`, `MGMT_methylation`; IDH1 R132H negative, sequencing wildtype and ATRX retained rows added to both reports. |
| A | major | `followup_outputs` `request_functional_mri` | `fMRI_BOLD` out of vocabulary, unscored; a meaningless motor "laterality index" (plan C6). | FIXED: tumour reaches the precentral gyrus and edema the posterior limb, so both apply. `functional_MRI` (left-hand focus 8 mm from the margin, language LI 0.85 left) and new `DTI_tractography` (CST continuous through the edematous corona radiata, 9 mm from the margin; reduced callosal FA). Recommended criteria and soft constraints to tissue. |
| C | major | `ground_truth.action_criteria` | No performance status (plan C7). | FIXED: recommended criterion; KPS 70, ECOG 2. |
| C | major | `required_recommendations` | Template Stupp and surgery musts; test musts (plan C3, C11; ruling 4). | FIXED: canonical group A surgery must with fMRI and DTI; entity-specific treatment must (age 52, KPS 70); MRI and labs musts deleted. |
| E | major | `prohibited_recommendations[0]` | Broken "Do not perform lumbar puncture with herniation risk [em dash] herniation risk". | FIXED: names the 8 mm shift and bilateral papilledema; canonical CSF harm rationale. |
| D | major | `initial_tool_outputs.eeg.impression` | Template impression omitting the focal delta, IRDA and the F4 sharp waves (plan C9). | FIXED: numbered ABNORMAL EEG impression from its own findings. |
| D | minor | `initial_tool_outputs.mri.impression`, perfusion impression | MRI impression lacked the precentral, callosal and capsular extent; perfusion graded the tumour against the 1.75 threshold (plan C12). | FIXED: numbered imaging-only MRI impression; perfusion "consistent with a high-grade neoplasm". |
| B | minor | MRS follow-up | Impression described a peritumoral choline rise with no finding row. | FIXED: peritumoral row (Cho/Cr 1.7, NAA/Cr 1.2, Cho/NAA 1.4); numbered impression. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | RBC 4.7 x MCV 95.6 implies Hct 44.9 against 43.0. | FIXED: MCV 91.5. Type and screen `clinical_significance` null with a blood group. |
| C | minor | criteria 1, 2, 6, 7, 8, 9; constraints; stop rule; avoided actions | Template rationales, citations, expected evidence; single soft constraint; literature in stop rule. | FIXED as in S01 (hard MRI and labs to tissue, soft fMRI and DTI; stop rule MRI, labs, tissue; cardiac waste rationale). |
| C | minor | `differential`, `key_clinical_evidence` | Not at the assessment-time view; template lines. | FIXED: very_low alternatives with the excluding results, IDH-mutant astrocytoma grade 4 added; evidence from this case. |
| B | minor | `metadata` | "5 required tools". | FIXED: 3; `last_revised`, `revision_reason`. `key_teaching_points` (legacy, not served) left. |

## Changes, in one paragraph a physician can read before re-reviewing
The history and examination now fit a right frontal tumour in a left-language-dominant man: the seizure turns head and eyes to the left, the shift is leftward, the aphasic features and the left hemianopia (copied from another case and not explained by this lesion) are removed. Levetiracetam and dexamethasone, started in the ED, are continued rather than started; a latex-safe theatre is a new must. The temozolomide drug check with a non-existent sulfa allergy is replaced by a dexamethasone and levetiracetam check against his own medicines. The pathway reads contrast MRI, perfusion, spectroscopy, optional CT staging, labs, performance status (KPS 70, ECOG 2), functional MRI and DTI, then resection or stereotactic biopsy with IDH1 IHC, IDH sequencing (age 52), ATRX and MGMT, giving Glioblastoma, IDH-wildtype, CNS WHO grade 4, MGMT unmethylated; after it, 60 Gy in 30 fractions with temozolomide. Literature is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- `[AIOM_brain]` citation key needs the pack allow-list (plan 5.1).
- Synonym "astrocytoma grade 4" is wrong for this IDH-wildtype GBM (plan 5.2).
- `accepted[0]` "WHO grade 4" versus "CNS WHO grade 4" (plan 5.3).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the git diff and the whole final case.
- No reviewer notes. Checked each own finding against the file: leftward version and leftward shift, removal of aphasia and hemianopia (exam now "Visual fields full"), continue forms of the levetiracetam and dexamethasone musts (HPI says both were started in the ED), latex must, drug check against his own medicines with no sulfa line, assay list with IDH sequencing at 52 in both alternatives and in both reports, fMRI and DTI, KPS 70 / ECOG 2, labs (gap 140 - 105 - 26 = 9, RBC 4.7 x MCV 91.5 = 43.0).
- Found and fixed (B, minor, class fixed by the worker in S02, S04 and S06 but missed here): `fallback_tool_outputs.csf` opening pressure 16 cm H2O and "Unremarkable CSF" in a patient with bilateral papilledema and 8 mm shift. Now 26 cm H2O, "Elevated opening pressure. Normal cell count, protein and glucose." (The LP itself stays harm; the fallback only answers an off-pathway order.)
- perfect_agent.py and case_io.py check clean after the edit.
