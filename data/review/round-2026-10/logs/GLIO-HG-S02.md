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

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.alternatives: was [CBC, BMP, coagulation, type_and_screen]; now [CBC, BMP, coagulation, type_and_screen, HbA1c] | [CBC, BMP, coagulation, type_and_screen].
- Decision: serve: new first alternative (old order kept as an alternative). Known type 2 diabetes before dexamethasone and surgery: the evidence and the glucose-monitoring must read the HbA1c, which a pre-operative order in a diabetic patient includes.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Case-specific reports stored where the benchmark library's normal report contradicted the case. Why: the stored MRI shows a mass in the right frontal lobe (precentral and middle frontal gyri), extending into the insula and basal ganglia (5.8 x 4.3 x 4.6 cm) with an abnormal routine EEG and a focal history and exam; the library reports a normal head CT, a non-diagnostic biopsy, normal brain metabolism, perfusion and vessels, a normal prolonged EEG, no headache and normal bedside and neurophysiological tests where the exam is abnormal.

- order_ct_scan: CT showing the stored lesion(s) instead of a normal head CT (fallback_tool_outputs.ct)
- obtain_tissue_diagnosis open_biopsy: the stored integrated diagnosis on this procedure's specimen (fallback_tool_outputs.tissue_diagnosis)
- FDG_PET: hypermetabolic lesion(s) (fallback_tool_outputs.advanced_imaging)
- amino_acid_PET: FET-avid lesion(s) (followup request_amino_acid_pet)
- CT_perfusion: lesion perfusion matching the stored perfusion MRI (followup request_ct_perfusion)
- perfusion_SPECT: regional hypoperfusion over the lesion (followup request_perfusion_spect)
- cerebral_angiography: mass effect and lesion vascularity (followup request_cerebral_angiography)
- video EEG: the stored routine EEG's abnormalities over 24 h (fallback_tool_outputs.eeg)
- ambulatory EEG: the stored routine EEG's abnormalities over 48 h (followup request_ambulatory_eeg)
- structured_headache_history_ichd3: the case's headache, prior primary headache and red flags (fallback_tool_outputs.clinical_assessment)
- cognitive_screen: MoCA matching the exam (followup request_cognitive_screen)
- gait_and_balance_timed: matching the exam (followup request_timed_gait_balance)
- neuropsych_battery: domain deficits matching the exam (fallback_tool_outputs.specialized_test)
- visual_field_perimetry: the exam's field defect or blind-spot enlargement (followup request_visual_field_perimetry)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k GLIO-HG-S02` pass; no fixed order still answered by the library (`lib4.source`); no 60-character window of any criterion's expected_evidence in the added text, except tissue copies that repeat the stored tissue report verbatim; every criterion's served output unchanged (snapshot diff against the baseline).
