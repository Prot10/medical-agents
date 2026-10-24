# GLIO-HG-S02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The notes file has no note for GLIO-HG-S02. The condition classes of the plan were applied (below). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs.panels.CBC` | Hb 15.8 with Hct 40.9 gives MCHC 38.6 g/dL, impossible; RBC 4.65 x MCV 92.8 implies Hct 43.2 (plan C10). | FIXED: Hb 14.1, Hct 43.2 (MCHC 32.6, consistent with RBC and MCV). RBC reference range was the male range; set to 3.92-5.13. |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Sodium 130 and chloride 92 abnormal with nothing in the case using or explaining them (plan C10: normalise unless used). | FIXED: sodium 138, chloride 101 (anion gap 138 - 101 - 24 = 13). Creatinine reference was the male range; set to 0.59-1.04 with value 0.9. Summary and interpretation recomputed. |
| E | minor | `initial_tool_outputs.labs.panels["Baseline workup"][0]` | Template type-and-screen `clinical_significance` with engineering text (plan C9). | FIXED: `null`; value "Group B RhD positive; antibody screen negative". |
| B | major | `patient.history_present_illness`, `patient.neurological_exam.mental_status` | Word-finding pauses and paraphasic errors in a right-handed woman with a right frontal tumour, while the fMRI shows strongly left-lateralized language remote from the tumour: a deficit no lesion explains (PATTERNS 3). | FIXED: HPI colleagues now note she "seemed slowed and hesitant"; exam "fluent and grammatical with no paraphasic errors; responses are slowed" (right frontal dysexecutive slowing, consistent with the inattention already recorded). |
| E | minor | `patient.history_present_illness` | A right-handed teacher "writing on the blackboard with her left hand for emphasis". | FIXED: "clumsiness handling chalk and papers with her left hand". |
| C | major | `action-3-search-medical-literature`, literature follow-up, `fallback_tool_outputs.literature_search` | Required literature step in the stop rule; literature output carried the treatment standard (ruling 5, plan C1). | FIXED: criterion, follow-up, stop-rule entry and fallback deleted (fallback set to null; `metadata.fallback_tool_kinds.literature_search` removed). |
| D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue served upfront; template impression; histology rows (cellularity, mitoses, necrosis, MVP) listed as molecular findings; "WHO grade IV" (plan C2). | FIXED: initial null; resection and stereotactic-biopsy follow-ups with identical diagnosis; one `Histology` row; impression "Integrated diagnosis: Glioblastoma, IDH-wildtype, CNS WHO grade 4. MGMT promoter unmethylated." |
| C | major | `action-10-obtain-tissue-diagnosis` | Biopsy only (plan C3 group A); assay list without ATRX and with 1p/19q, IDH sequencing, TERT and EGFR required (plan C4: age 64 with MVP and necrosis). | FIXED: `resection` then `stereotactic_biopsy`, each `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation`; ATRX IHC (retained) added to both reports; canonical label, rationale and expected evidence. |
| A | major | `followup_outputs` `request_functional_mri` | `fMRI_BOLD` (out of vocabulary) carrying a DTI sentence; unscored (plan C6). | FIXED: MRI places the tumour in the precentral gyrus and reaching the posterior limb of the internal capsule, with temporal-stem edema and a left homonymous hemianopia, so both apply. `functional_MRI` output (left-hand motor focus 6 mm from the margin, foot focus 11 mm, language LI 0.82 left); `DTI_tractography` output (CST continuous 4 mm from the margin at the posterior limb; optic radiation continuous through the edematous temporal stem with reduced FA). Two recommended criteria and soft constraints to tissue. |
| C | major | `ground_truth.action_criteria` | No performance status (plan C7). | FIXED: `action-performance-status` recommended (age 64); output KPS 70, ECOG 2 (independent self-care, on medical leave, slowed and inattentive). |
| C | major | `required_recommendations` | Template Stupp, dexamethasone and levetiracetam musts; test musts (MRI, labs) (plan C5, C11; ruling 4). | FIXED: canonical group A surgery must with fMRI, DTI and mapping; canonical dexamethasone; canonical treat must for the focal-to-bilateral seizure; entity-specific treatment must (age 64, KPS 70: 60 Gy in 30 fractions with temozolomide); test musts deleted. |
| C | major | `required_recommendations` | Early right uncal herniation, a trapped temporal horn and bilateral papilledema with no must for neurological monitoring or escalation. | FIXED: must for a monitored bed, neurological and pupil observations, hyperosmolar therapy and expedited decompression on deterioration. |
| C | major | `required_recommendations` | Aspirin 81 mg for primary prevention and ibuprofen continue into craniotomy and dexamethasone; the drug check flags both. | FIXED: must to stop both now; DDI warning on the 7 to 10 day aspirin effect. |
| E | major | `prohibited_recommendations[0]` | Broken text "Do not perform lumbar puncture with herniation risk [em dash] herniation risk". | FIXED: "Do not perform lumbar puncture: the 8 mm midline shift, early uncal herniation and bilateral papilledema create a risk of herniation." CSF harm rationale canonical with the same findings. |
| D | major | `initial_tool_outputs.eeg.impression` | Impression omitted the IRDA and the right frontotemporal sharp waves and gave an interpretive sentence (plan C9). | FIXED: numbered ABNORMAL EEG impression listing all findings; no electrographic seizures. |
| D | minor | `initial_tool_outputs.mri` | Impression omitted the insular and basal ganglia extension and the ventricular trapping; "rightward-to-leftward mass effect" wording. | FIXED: numbered imaging-only impression; mass-effect wording corrected; findings otherwise unchanged. |
| B | minor | `fallback_tool_outputs.csf` | Fallback CSF opening pressure 16 cm H2O in a patient with bilateral papilledema and uncal herniation. | FIXED: 29 cm H2O; interpretation says so. |
| C | minor | criteria 1, 2, 6, 7, 8, 9 | Rationale copied the label; action-1 `[Stupp_2005]`; template expected evidence; duplicate citations (plan 1.1, C9). | FIXED: rationales; action-1 `[EANO_2021]`; expected evidence from this case's results; one bracketed key per source. |
| C | minor | DDI follow-up and criterion | Levetiracetam absent from the check although the must starts it. | FIXED: proposed adds levetiracetam; levetiracetam and enzyme-inducer lines added; trigger renamed; optional and last; guard passes. |
| B | minor | `sequence_constraints`, `stop_rule`, `avoided_actions` | Template soft constraint; literature in the stop rule; template waste rationales (plan 3.3, 3.4). | FIXED: hard MRI and labs to tissue, soft fMRI and DTI to tissue; stop rule MRI, labs, tissue; cardiac waste "No cardiac question in this presentation". |
| C | minor | `differential`, `key_clinical_evidence` | Not at the assessment-time view; template lines. | FIXED: alternatives very_low with the excluding results; IDH-mutant astrocytoma grade 4 added; key evidence from this case. |
| B | minor | `metadata` | `difficulty_rationale` "5 required tools". | FIXED: 3; `last_revised`, `revision_reason`. `metadata.clinical_pearls` (legacy, not served) left as is. |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway reads contrast MRI, perfusion, spectroscopy, optional CT chest, abdomen and pelvis, labs, performance status (KPS 70, ECOG 2), functional MRI and DTI (motor cortex, corticospinal tract and the optic radiation in the edematous temporal stem), then tissue by maximal safe resection or stereotactic biopsy, and an optional drug check last; literature is gone. Tissue gives Glioblastoma, IDH-wildtype, CNS WHO grade 4, IDH1 R132H negative, sequencing wildtype, ATRX retained, MGMT unmethylated. The impossible CBC (MCHC 38.6) and the unexplained hyponatraemia are corrected. The aphasic features were removed from the history and exam: a right-handed patient with left-dominant language and a right frontal tumour now shows slowing and inattention instead. Musts add close neurological observation for the early uncal herniation, stopping aspirin and ibuprofen before surgery, levetiracetam as treatment of the documented seizure, and the age- and KPS-specific Stupp regimen after the integrated diagnosis.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- `[AIOM_brain]` citation key on the tissue criterion needs the pack allow-list (plan 5.1).
- Synonym "astrocytoma grade 4" is wrong for this IDH-wildtype GBM (plan 5.2).
- `accepted[0]` "WHO grade 4" versus "CNS WHO grade 4" in the reports (plan 5.3).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the git diff and the whole final case.
- No reviewer notes. Every own finding checked against the file: CBC (Hb 14.1, Hct 43.2, RBC 4.65 x MCV 92.8 = 43.2, MCHC 32.6; female reference ranges), BMP (Na 138, Cl 101, HCO3 24, gap 13; female creatinine range), type and screen, literature removed, tissue in two procedure-matched follow-ups with identical results, assay list per C4 in both alternatives, fMRI and DTI outputs and recommended criteria with soft constraints, KPS 70 / ECOG 2, musts (surgery, dexamethasone, herniation monitoring, treat must, aspirin and ibuprofen stop, glucose, Stupp at 64 with KPS 70), LP prohibition and harm rationale naming shift, uncal herniation and papilledema, CSF fallback 29 cm H2O.
- The removal of the aphasic features is sound (left-lateralized language LI 0.82 remote from a right frontal tumour); the left homonymous hemianopia is explained by the optic radiation in the edematous temporal stem and sagittal stratum on DTI.
- Nothing found that needed a change. perfect_agent.py and case_io.py check clean.

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Minor non-specific finding.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
