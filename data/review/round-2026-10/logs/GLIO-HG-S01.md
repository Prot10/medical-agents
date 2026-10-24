# GLIO-HG-S01
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 7d836e30-c895-46f5-90dd-cd5420a73e41 | FIXED | Plan C4. Tissue criterion `action-10-obtain-tissue-diagnosis` `required_arguments.molecular_assays` is now `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation` (GBM, IDH-wildtype with MVP and necrosis, age 58, so IDH sequencing is not in the minimum list) in both alternatives; `1p_19q_codeletion` removed from the required list (IDH-wildtype). Label names the three assays in words. Both tissue reports carry a `findings` row and a `molecular_findings` entry for each: IDH1 R132H IHC negative, ATRX retained, MGMT unmethylated, plus IDH1/IDH2 sequencing wildtype, TERT C228T, EGFR amplification, +7/-10 and 1p/19q intact. |
| 73339f93-b6e1-49d4-b880-6d678b2cba73 | FIXED | Plan C10. `initial_tool_outputs.labs`: haematocrit 38.5 (L) to 43.8 (MCHC 14.7/43.8 = 33.6 g/dL); PT 13.6 (H) to 12.6 s with INR 1.1 to 1.0 (PT and INR agree, both in range). `abnormal_values_summary` and `interpretation` recomputed (only glucose 129 and HbA1c 7.2 remain abnormal). `action-2-interpret-labs` expected evidence now states the actual result: glucose and HbA1c relevant to dexamethasone, normal sodium, platelets and coagulation, no laboratory contraindication to surgery. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Sodium 152 (H) with no explanation anywhere in the case and no must addressing it (plan C10). | FIXED: sodium 139, chloride 106 to 103 (anion gap 139 - 103 - 24 = 12). |
| A | major | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Tumour copy-number marker `chr7_gain_chr10_loss` reported as a serum "exclusion study" with engineering text ("which is what this case's diagnosis rests on"). | FIXED: panel deleted. |
| E | minor | `initial_tool_outputs.labs.panels["Baseline workup"][0]` | Template `clinical_significance` with engineering text for type and screen (plan C9). | FIXED: `null`; value now "Group O RhD positive; antibody screen negative". |
| C | major | `action-3-search-medical-literature`, `followup_outputs` literature | Required literature search as a clinical step; in the stop rule (ruling 5, plan C1). | FIXED: criterion, follow-up and stop-rule entry deleted. |
| D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue served in the initial work-up; impression carried the WHO CNS5 template meta-text; "Microscopic description" listed as a molecular finding (plan C2). | FIXED: initial set to null; two follow-ups `obtain_tissue_by_resection` (`procedure: resection`, specimen and extent-of-resection rows) and `obtain_tissue_by_stereotactic_biopsy` (`procedure: stereotactic_biopsy`), identical integrated diagnosis and molecular results; one `Histology` row; impression "Integrated diagnosis: Glioblastoma, IDH-wildtype, CNS WHO grade 4. MGMT promoter unmethylated." |
| C | major | `action-10-obtain-tissue-diagnosis`, must 1 | Tissue by stereotactic biopsy only for a resectable right frontal lesion; must made biopsy and resection interchangeable (plan C3, group A). | FIXED: alternatives `resection` then `stereotactic_biopsy`; canonical label and rationale (AIOM Q1; EANO 2021); canonical group A surgery must with fMRI, DTI and intraoperative mapping. Citations `[WHO_2021]`, `[EANO_2021]`, `[AIOM_brain]` (WHO_CNS5 free text dropped). |
| A | major | `followup_outputs` `request_functional_mri` | Output tagged `fMRI_BOLD` (out of vocabulary) and mixing BOLD and DTI content; no criterion scored it (plan C6). | FIXED: MRI shows tumour centred in the precentral gyrus extending to the corona radiata, so both apply. New `functional_MRI` output (left-hand motor focus 8 mm from the posteromedial margin, normal right-hand and foot maps, language LI 0.85 left) and new `DTI_tractography` output (right CST displaced, continuous, 5 mm from the enhancing margin in the corona radiata, FA 0.47 vs 0.56; reduced FA in the genu). Recommended criteria `action-fmri-functional-mapping` and `action-dti-tractography`, soft constraints to tissue. Impressions report distances and LI only. |
| C | major | `ground_truth.action_criteria` | No performance status (plan C7). | FIXED: `action-performance-status` recommended (age 58); follow-up `score_performance_status`: KPS 70, ECOG 2, with the basis from the exam and work history. |
| C | major | `required_recommendations` | Template "Stupp protocol" must (plan C11); generic loading-dose dexamethasone must. | FIXED: entity-specific must (GBM, IDH-wildtype, age 70 or under with KPS 70 or more: 60 Gy in 30 fractions with concomitant and adjuvant temozolomide); canonical dexamethasone must. |
| C | major | must 4 | Levetiracetam must did not say it is treatment rather than prophylaxis, nor name the enzyme-inducer interaction (plan C5, treat class). | FIXED: canonical treat must for the focal seizure with left arm onset and bilateral tonic-clonic spread. |
| C | minor | `required_recommendations` | Two musts were tests already scored as criteria ("Obtain MRI ... before any invasive procedure", "Obtain pre-operative labs"), not management (ruling 4). | FIXED: deleted; the order is enforced by the hard MRI-to-tissue and labs-to-tissue constraints. |
| C | minor | `required_recommendations` | Ibuprofen as needed with dexamethasone and before craniotomy not addressed, though the drug check flags it. | FIXED: must "Stop as-needed ibuprofen while on dexamethasone and before surgery". Glucose must now names HbA1c 7.2% and the metformin and insulin adjustment. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | One soft MRI-to-tissue constraint; stop rule held the literature criterion (plan 3.3, 3.4). | FIXED: hard MRI to tissue and labs to tissue, soft fMRI and DTI to tissue; stop rule MRI, labs, tissue. |
| D | major | `initial_tool_outputs.eeg.impression` | Impression omitted the focal delta, the rhythmic delta and the right frontal sharp waves in the findings (plan C9). | FIXED: numbered ABNORMAL EEG impression listing all four abnormalities, no electrographic seizures. |
| D | minor | `initial_tool_outputs.mri.impression` | Impression omitted size, diffusion and the shift value. | FIXED: numbered imaging-only impression with 8 mm shift; findings unchanged. |
| B | minor | `patient.history_present_illness` | ED CT "7 mm" against MRI 8 mm shift (plan C9); "dropping tools" for an insurance adjuster. | FIXED: 8 mm in both; "dropping objects"; CT described as a mass with partly hyperdense components (matches T1 hyperintensity), no enhancement or tumour type named. |
| B | minor | `patient.neurological_exam.additional` | "No signs of increased intracranial pressure clinically" beside morning headaches that wake him. | FIXED: sentence removed (papilloedema absence stays in cranial nerves). |
| D | minor | `initial_tool_outputs.ecg.interpretation` | "likely related to long-standing hypertension" is a non-cardiac reference (style guide). | FIXED: clause removed. |
| B | minor | `followup_outputs` perfusion and MRS | Perfusion impression mentioned a perilesional rCBV with no finding row; MRS impression omitted its main finding. | FIXED: perilesional row (rCBV 1.6) added; both impressions numbered and complete (Cho/NAA 3.6/0.4 = 9.0 and 1.8/1.1 = 1.6 checked). |
| C | minor | action-1, -2, -6, -7, -8, -9 | Rationales copied the label; action-1 cited `[Stupp_2005]`; template expected evidence; duplicate "[X]"/"X" citations (plan 1.1, C9). | FIXED: rationales written; action-1 `[EANO_2021]`; expected evidence from this case's MRI, perfusion, MRS and labs; one bracketed key per source. |
| C | minor | `action-9-check-drug-interactions`, drug follow-up | Optional DDI kept; output lacked levetiracetam although the treat must starts it. | FIXED: trigger `check_dexamethasone_and_levetiracetam_interactions`; proposed adds levetiracetam; levetiracetam and enzyme-inducer lines added; stays optional and last; guard passes. |
| C | minor | `ground_truth.differential` | Likelihoods not at the assessment-time view; IDH-mutant astrocytoma grade 4 (the main tissue mimic) absent. | FIXED: all alternatives very_low with the excluding results; IDH-mutant astrocytoma grade 4 added. |
| C | minor | `key_clinical_evidence` | Template lines (biopsy or resection interchangeable, H3K27M in the panel, "mandates AED therapy"). | FIXED: rewritten from this case's data. |
| B | minor | `avoided_actions` | Template rationales. | FIXED: echo and Holter "No cardiac question in this presentation" `[EANO_2021]`; CSF canonical harm with 8 mm shift. LP prohibition rewritten without a dash. |
| E | minor | `followup_outputs` CT CAP | Em dash in the renal cyst line. | FIXED: comma. |
| B | minor | `metadata` | `difficulty_rationale` "5 required tools"; `required_modalities` listed EEG and not tissue. | FIXED: 3 required tools; modalities aligned with the panel; `last_revised`, `revision_reason`. |
| B | minor | `fallback_tool_outputs.specialized_test` | Generic "Study within normal limits" neuropsychological screening, while the exam records inattention and 2/3 recall. Off-pathway fallback, not served by any criterion. | FLAGGED (left; benchmark-wide fallback pattern). |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway now reads contrast MRI, perfusion, spectroscopy, optional CT chest, abdomen and pelvis, pre-operative labs, performance status (KPS 70, ECOG 2), functional MRI and DTI tractography (the tumour sits in the right precentral gyrus and abuts the corticospinal tract), then tissue by maximal safe resection or, if not safely feasible, stereotactic biopsy, and an optional drug check last. The literature step is gone. Tissue is no longer served upfront: both procedures return the same integrated diagnosis, Glioblastoma, IDH-wildtype, CNS WHO grade 4, with IDH1 R132H negative, IDH sequencing wildtype, ATRX retained, MGMT unmethylated, TERT, EGFR and +7/-10 positive; the required assays are IDH1 IHC, ATRX IHC and MGMT. Laboratory values are corrected (sodium 139, haematocrit 43.8, PT 12.6 with INR 1.0); only glucose and HbA1c are abnormal. The EEG impression now lists the right frontal sharp waves. Musts: group A surgery with fMRI, DTI and mapping; dexamethasone at the lowest effective dose; levetiracetam as treatment of the documented focal-to-bilateral seizure, avoiding enzyme inducers; glucose monitoring on metformin; stop ibuprofen; after the integrated diagnosis, 60 Gy in 30 fractions with temozolomide (age 58, KPS 70). MRI before tissue and labs before tissue are hard constraints.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation key `[AIOM_brain]` used on the tissue criterion; needs the criteria-pack allow-list (plan 5.1).
- Synonym "astrocytoma grade 4" is appended to this IDH-wildtype GBM label and is wrong for it (plan 5.2).
- `accepted[0]` reads "WHO grade 4"; the reports now say "CNS WHO grade 4" (plan 5.3 normalisation).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case. KPS 70 sits exactly on the Stupp threshold; I scored 70 (independent self-care, cannot work) rather than 80 because the seizure, left-hand weakness and inattention stop him working. The plan's open questions 4, 5 and 7 (stop allowance, performance status tier, biopsy credit in group A) apply here as to all cases.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the git diff and the whole final case.
- Notes 7d836e30 (assay list) and 73339f93 (Hct, PT) confirmed fixed in every place they apply: both alternatives carry `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation`; both tissue reports have a findings row and a molecular entry for each; Hb 14.7 / Hct 43.8 (MCHC 33.6), PT 12.6 with INR 1.0, flags and summary agree. Sodium 139, Cl 103, HCO3 24 (gap 12). No note id missing.
- Cross-field checks clean: left arm onset, left hemiparesis and right precentral tumour agree; 8 mm leftward shift in CT, MRI, prohibition and CSF harm; KPS 70 / ECOG 2 definitions agree with the functional rows; treatment must matches age 58 and KPS 70; no em dashes, no engineering text; guard tests pass.
- Found and fixed (B, minor, class the worker fixed in S02 and S03 but missed here): `patient.neurological_exam.mental_status` "Language fluent but with intermittent word-finding pauses" in a right-handed man with a right frontal tumour and left language dominance on fMRI (LI 0.85, remote from the lesion). Now "Language fluent with intact naming and repetition; responses are slowed."
- Left as is: the HPI opens with "witnessed generalized tonic-clonic seizure" and then describes the focal left-arm onset; the exam and the must state focal onset with bilateral spread, so the case is internally consistent.
- perfect_agent.py and case_io.py check clean after the edit.

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Study within normal limits.', test_type 'neuropsychological_screening') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
