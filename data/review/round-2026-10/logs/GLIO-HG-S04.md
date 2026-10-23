# GLIO-HG-S04
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The notes file has no note for GLIO-HG-S04. The condition classes of the plan were applied (below). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `action-3-search-medical-literature`, `fallback_tool_outputs.literature_search` | Baseline perfect-agent failure: recommended literature criterion answered only by the generic fallback (plan C1, ruling 5); `metadata.case_body_concerns` asked for a literature payload to be added. | FIXED: criterion deleted, fallback set to null, `fallback_tool_kinds.literature_search` and the case-body concern removed. Perfect-agent check now passes. |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Anion gap 141 - 97 - 27 = 17, with chloride flagged low and unexplained (plan C10). | FIXED: chloride 101, gap 13. |
| B | major | `initial_tool_outputs.labs.panels.CBC` | Hb 15.0 with Hct 38.5 gives MCHC 39 g/dL (plan C10). | FIXED: Hct 42.1 (RBC 4.86 x MCV 86.6; MCHC 35.6). Type and screen `clinical_significance` null with a blood group. Summary and interpretation recomputed. |
| D | major | `initial_tool_outputs.eeg.impression` | "The focal slowing and epileptiform discharges correlate with the patient's recent seizure and clinical presentation" (plan C9, style guide). | FIXED: numbered ABNORMAL EEG impression from the findings only. |
| B | minor | `initial_tool_outputs.mri.findings[0].mass_effect` | "Rightward subfalcine herniation with 8 mm leftward midline shift": the right cingulate herniates leftward. | FIXED: "Subfalcine herniation of the right cingulate gyrus to the left, with 8 mm leftward midline shift"; numbered impression adds hemorrhage and subfalcine herniation. |
| D | minor | perfusion and MRS follow-ups | Perfusion graded the tumour against the 1.75 threshold; MRS impression named a peritumoral choline rise with no finding row. | FIXED: perfusion "consistent with a high-grade neoplasm"; peritumoral MRS row (Cho/Cr 1.6, Cho/NAA 1.5) and numbered impression. |
| D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue upfront; template impression; histology rows as molecular findings; "WHO grade IV"; site inside the integrated diagnosis (plan C2). | FIXED: initial null; resection and stereotactic-biopsy follow-ups; one `Histology` row; integrated diagnosis "Glioblastoma, IDH-wildtype, CNS WHO grade 4"; impression with MGMT methylated. |
| C | major | `action-10-obtain-tissue-diagnosis` | Biopsy only; assay list without IDH or ATRX and with 1p/19q (plan C3, C4; age 71). | FIXED: `resection` then `stereotactic_biopsy`, each `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation`; IDH1 R132H negative and ATRX retained rows added. |
| A | major | `followup_outputs` `request_functional_mri` | `fMRI_BOLD` out of vocabulary, unscored; SMA proximity in the impression with no finding row (plan C6). | FIXED: tumour at the precentral and superior frontal gyri into the corona radiata, parietal edema with a left hemianopia, so both apply. `functional_MRI` (hand area 6 mm, SMA 4 mm, language LI 0.89 left) and `DTI_tractography` (CST 5 mm from the margin; optic radiation through the parietal edema with reduced FA, which accounts for the field defect). Recommended criteria, soft constraints to tissue. |
| C | major | `ground_truth.action_criteria`, `stop_rule` | No performance status in a 71-year-old (plan C7). | FIXED: `action-performance-status` required and in the stop rule; KPS 70, ECOG 2. |
| C | major | `required_recommendations` | Stupp must for a patient over 70 (plan C11); test musts; generic surgery and seizure musts. | FIXED: over-70 must (hypofractionated 40 Gy in 15 fractions with temozolomide given methylated MGMT, or temozolomide alone); canonical group A surgery, dexamethasone and treat musts; test musts deleted. |
| C | major | `required_recommendations` | Primary-prevention aspirin and the over-the-counter ibuprofen in the HPI not addressed before craniotomy. | FIXED: must to stop both; DDI warning on the aspirin effect. |
| B | minor | `followup_outputs` drug checks | Two drug-interaction follow-ups; any `check_drug_interactions` call can only receive one (plan survey). | FIXED: merged into one `check_dexamethasone_and_levetiracetam_interactions` output (dexamethasone with metformin and aspirin; levetiracetam without relevant interaction; enzyme-inducer and aspirin warnings); optional, last; guard passes. |
| E | major | `prohibited_recommendations[0]` | "Do not perform lumbar puncture [em dash] herniation risk". | FIXED: names the shift, subfalcine herniation and papilledema; canonical harm rationale. |
| B | minor | `fallback_tool_outputs.csf` | Opening pressure 16 cm H2O with bilateral papilledema. | FIXED: 27 cm H2O. |
| E | minor | HPI, CT CAP | Em dashes. | FIXED: colon and comma. |
| C | minor | criteria rationales, citations, expected evidence; constraints; avoided actions; differential; key evidence | Template text (plan 1.1, 3.3, C9, C12). | FIXED as in S01; alternatives very_low after tissue; key evidence now states why the over-70 regimen applies. |
| B | minor | `metadata.difficulty_rationale` | "4 required tools" with literature. | FIXED: 4 required actions (MRI, labs, performance status, tissue). |

## Changes, in one paragraph a physician can read before re-reviewing
The case failed the perfect-agent check because a recommended literature step had no output; literature is removed. The pathway reads contrast MRI, perfusion, spectroscopy, optional CT staging, labs, a required performance status (KPS 70, ECOG 2), functional MRI (hand area and SMA) and DTI (corticospinal tract and the optic radiation, which runs through the parietal edema and explains the left hemianopia), then resection or stereotactic biopsy with IDH1 IHC, ATRX and MGMT. The tissue gives Glioblastoma, IDH-wildtype, CNS WHO grade 4, MGMT methylated; because he is 71 the treatment must is hypofractionated radiotherapy 40 Gy in 15 fractions with temozolomide (or temozolomide alone), not the Stupp schedule. Laboratory arithmetic is corrected; the two drug checks are merged; aspirin and ibuprofen are stopped before surgery; levetiracetam is treatment of the documented seizure.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- `[AIOM_brain]` citation key needs the pack allow-list (plan 5.1).
- Synonym "astrocytoma grade 4" is wrong for this IDH-wildtype GBM (plan 5.2).
- `accepted[0]` "Glioblastoma, IDH-wildtype, WHO grade 4 (right frontoparietal)" carries "WHO grade" rather than "CNS WHO grade" (plan 5.3); left unchanged per ruling 3.

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case. KPS 70 sits on the boundary that EANO uses; for a patient over 70 the hypofractionated regimen applies whatever the KPS, so the must does not depend on it.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the git diff and the whole final case.
- No reviewer notes. Checked: literature removed (baseline failure gone), gap 141 - 101 - 27 = 13, Hct 42.1 (RBC 4.86 x MCV 86.6; MCHC 35.6), CRP 4.2 flagged against <3.0, subfalcine herniation wording, required performance status in the stop rule (age 71), over-70 must (hypofractionated 40 Gy in 15 fractions with temozolomide for methylated MGMT, EANO 2021), one merged drug check, aspirin and ibuprofen stop must, penicillin allergy real and not contradicted, CSF fallback 27 cm H2O with papilledema.
- Found and fixed:
  - (B, minor, same class the worker fixed in S02 and S03) `patient.neurological_exam.mental_status` "Speech is fluent but with occasional word-finding pauses" with a right frontoparietal tumour and left language dominance on fMRI (LI 0.89). Now "Speech is fluent with intact naming; responses are slowed."
  - (B, minor) the drug check omitted the over-the-counter ibuprofen that the HPI records and that a must stops. Added "Dexamethasone + Ibuprofen (over the counter): combined corticosteroid and NSAID use increases the risk of gastrointestinal ulceration and bleeding; ibuprofen also impairs platelet function." Guard tests still pass (no expected-evidence echo).
- perfect_agent.py and case_io.py check clean after the edits.
