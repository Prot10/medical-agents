# GLIO-HG-M01
Reviewer status: R1 not reviewed, R2 needs_changes (3 notes) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 67871b5a-9ad9-4671-b2f3-08d68ac3b2ae | FIXED | Uncertain-spells class (plan C5). The levetiracetam "for documented seizure activity" must is replaced by `required_recommendations[2]` "Characterise the brief staring spells with an EEG; start levetiracetam only if they are judged to be seizures, not as prophylaxis." The EEG that already existed in `initial_tool_outputs.eeg` (left temporal delta, no epileptiform discharges) is now scored by the recommended criterion `action-eeg-characterise-spells`; its impression is rewritten in ACNS form. The key-evidence line "New-onset seizure ... mandates AED therapy" is replaced by the uncertain-spells statement. |
| 6ef98175-0152-49ee-8f51-40f425b7c9c8 | FIXED | Procedure decided: group A, resection first (AIOM Q1). The mislabelled `perfusion_MRI` follow-up is now `modality: functional_MRI` (`followup_outputs[4]`, language and motor mapping only, the "DTI tractography of the arcuate fasciculus" sentence removed from its impression); the tract content is a new `modality: DTI_tractography` follow-up (`followup_outputs[5]`) with its findings in `findings` (arcuate fasciculus, temporal-stem tracts, Meyer loop, corticospinal tract). Both are recommended criteria (`action-fmri-functional-mapping`, `action-dti-tractography`) with soft constraints before tissue. The tissue criterion accepts `resection` then `stereotactic_biopsy`, with one follow-up per procedure. |
| df9e2c08-cfa4-4001-a5ad-7325e049b2c4 | FIXED | The temozolomide check with the "allergic to penicillin, verify sulfonamide" warning is replaced by a dexamethasone/levetiracetam check (`followup_outputs[8]`) against her own medicines (ibuprofen, sertraline, levothyroxine, lisinopril) that states her real allergy (tetracycline, photosensitivity, no cross-reactivity). The literature block is deleted with its criterion (plan C1). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Last sentence gave the outpatient MRI result the case scores. | FIXED: outside non-contrast CT showing a left temporal hypodensity with oedema and slight midline shift (C8). |
| E | minor | `patient.neurological_exam.additional` | Author aside "subtle enough that a casual examiner might attribute it to anxiety". | FIXED: deleted. |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Na 134, Cl 111, HCO3 26 gave an anion gap of -3. | FIXED: chloride 99 (normal, unflagged), gap 9. (The plan's "Cl about 101, gap about 12" is arithmetically 7; 99 gives a gap inside 8 to 16.) |
| B | minor | `initial_tool_outputs.labs.panels.CBC` Hemoglobin | Hb 14.8 with Hct 40.5 (MCHC 36.5) and RBC 4.29, MCV 93.7 (Hct derived 40.2). | FIXED: Hb 13.4 (MCHC 33.1, MCH 31.2). |
| B | minor | `initial_tool_outputs.labs` `abnormal_values_summary`, `interpretation`, type_and_screen `clinical_significance` | Recompute after chloride change; template significance text. | FIXED: summary Na and glucose only; plain interpretation; type_and_screen significance null (C9). |
| B | minor | `initial_tool_outputs.mri.findings[0].mass_effect` | A left temporal mass was described with a "leftward" falcine shift. | FIXED: 2 mm rightward shift. |
| D/E | minor | `initial_tool_outputs.mri.impression` | Prose paragraph naming "glioblastoma" by enhancement pattern and the retired "anaplastic astrocytoma". | FIXED: numbered impression, imaging differential "most consistent with a high-grade glial neoplasm; CNS lymphoma and tumefactive demyelination less likely", tissue diagnosis recommended. |
| B/D | minor | `followup_outputs[0]` perfusion, `followup_outputs[1]` MRS | Teaching thresholds in signal text; perfusion impression named a peritumoral rCBV finding with no finding row. | FIXED: thresholds removed, peritumoral finding row added (ratio 1.6), numbered impressions. |
| E | minor | `followup_outputs[2].output.impression` (CT CAP) | Em dash. | FIXED. |
| B | minor | `followup_outputs[4]` fMRI face motor | "Left face motor area" for a left precentral representation. | FIXED: "right-face representation (ventral left precentral gyrus)". |
| A/D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue served in the initial work-up; template meta-text in impression; "WHO grade 4". | FIXED (C2): initial null; two follow-ups (`resection`, `stereotactic_biopsy`) with identical integrated diagnosis "Glioblastoma, IDH-wildtype, CNS WHO grade 4", Histology and Specimen rows, one findings row and one molecular entry per assay. |
| A | major | `action-3-search-medical-literature`, literature follow-up, `fallback_tool_outputs.literature_search` | Literature as a required clinical step (also in stop rule). | FIXED (C1): criterion, follow-up and fallback deleted; `metadata.fallback_tool_kinds.literature_search` removed. |
| C | major | `action-10` `molecular_assays` | Required list carried 1p/19q, TERT, EGFR, +7/-10; label template. | FIXED (C4): minimum list IDH1_IHC, IDH1_IDH2_sequencing (age 52), ATRX_IHC, MGMT_methylation in both alternatives; the report still gives the other markers. |
| C | major | `ground_truth.action_criteria` | No performance status. | FIXED (C7): recommended `action-performance-status` with follow-up KPS 80, ECOG 1. |
| B | major | `action-1` expected evidence, `key_clinical_evidence[1]` | Template "ring enhancement, central necrosis" contradicting this MRI. | FIXED: written from her MRI. |
| C | minor | criteria labels, rationales, citations | Label = rationale; duplicate bare keys; `[Stupp_2005]` on the MRI criterion. | FIXED: canonical labels and rationales; one bracketed key per source, `[EANO_2021]` on MRI. |
| C | major | `sequence_constraints`, `stop_rule` | One soft MRI-to-tissue constraint; literature in stop rule. | FIXED: hard MRI and labs before tissue, soft fMRI and DTI before tissue; stop rule MRI, labs, tissue. |
| C | major | `assessment.required_recommendations` | Biopsy/resection interchangeable; MRI and labs repeated as musts; template Stupp must. | FIXED: C3 surgery must (fMRI, DTI, mapping), C11 dexamethasone must, uncertain-spells must, new ibuprofen must, entity-specific treatment must (age 52, KPS 80: 60 Gy/30 with temozolomide). The MRI and labs musts were removed because they repeat scored criteria already done before the assessment. |
| C | minor | `assessment.required_recommendations[3]` | Patient takes as-needed ibuprofen before neurosurgery and dexamethasone, with sertraline. | FIXED: must to stop ibuprofen and use paracetamol; the drug check says why. |
| C | minor | `avoided_actions` | CSF harm rationale generic; cardiac waste rationales template. | FIXED: C17 rationale citing the 2 mm shift and temporal horn effacement; cardiac rationales "No cardiac question in this presentation". Prohibition rewritten without dash. |
| C | major | `ground_truth.differential` | Retired "Anaplastic astrocytoma" at moderate; demyelination key features contradicted the MRI (closed ring, marked mass effect); likelihoods pre-tissue. | FIXED: assessment-time view, all very_low with case-specific discriminators; depression added because the red herring raises it. |
| C | minor | `key_clinical_evidence` | Generic template lines (off-pathway modalities, seizure mandate). | FIXED: rewritten from this case. |
| B | minor | `red_herrings[0]` | Empty field_path; em dash. | FIXED: `patient.clinical_history.past_medical_history[2]`, reworded. |
| B | minor | `metadata.difficulty_rationale` | "5 required tools". | FIXED: 3 required tools. |

## Changes, in one paragraph a physician can read before re-reviewing

The HPI now ends with an outside non-contrast CT (left temporal hypodensity with oedema), not the MRI result. The pathway reads MRI, perfusion, spectroscopy, EEG for the staring spells, optional CT staging, pre-operative labs, performance status (KPS 80, ECOG 1), functional MRI (left language dominance, Wernicke activation 1.2 cm from the tumour) and DTI (arcuate fasciculus displaced, 6 mm; Meyer loop in the oedema), then tissue by resection or, if not feasible, stereotactic biopsy, and an optional drug check last. The literature step is gone. Tissue is no longer in the initial work-up: both procedures return Glioblastoma, IDH-wildtype, CNS WHO grade 4 (MVP and palisading necrosis; IDH1 R132H negative, IDH1/2 wildtype, ATRX retained, TERT C228T, EGFR amplified, +7/-10, MGMT methylated); the scored assays are IDH IHC, IDH sequencing, ATRX and MGMT. Labs: chloride 99 (gap 9) and haemoglobin 13.4 make the panel internally consistent; sodium 134 is the only electrolyte abnormality. The MRI now has a rightward shift and a numbered impression without "glioblastoma" or "anaplastic astrocytoma". Musts: resection with fMRI, DTI and mapping; dexamethasone at the lowest effective dose; EEG characterisation and levetiracetam only if the spells are seizures (no prophylaxis); stop ibuprofen; MDT and 60 Gy/30 with temozolomide. Prohibitions: LP (2 mm shift, temporal horn effacement), therapy before tissue, anticoagulation. The drug check uses her real allergy (tetracycline) and medicines. The differential is at the assessment-time view (all very_low), with depression added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation key `[AIOM_brain]` used on the tissue, EEG and drug-check criteria (plan section 5.1, pack allow-list).
- Synonym "astrocytoma grade 4" in `diagnosis.accepted` is wrong for an IDH-wildtype glioblastoma (plan section 5.2); not hand-edited.
- accepted[0] keeps "WHO grade 4"; normalising to "CNS WHO grade" is plan section 5.3.

## Open questions for Andrea (judgment calls you could not settle)

None specific to this case. (Plan open questions 4, 5 and 7 apply to all cases.)

## Verification

Adversarial check (24 Oct 2026) of the log against the final file and `git diff`. All three notes are fixed where they apply: no "documented seizure" mandate remains (uncertain-spells must, recommended EEG criterion served by the existing initial EEG, drug check proposes levetiracetam only if the spells are seizures); the mislabelled step is now a `functional_MRI` follow-up plus a separate `DTI_tractography` follow-up with its tract content in `findings`, resection first; the drug check states tetracycline and her real medicines, no penicillin or sulfonamide text. Re-computed: anion gap 9, MCHC 33.1, MCH 31.2, Hct consistent with RBC x MCV; rightward shift for a left mass; KPS 80 and age 52 consistent with the 60 Gy/30 must; LP harm consistent with the 2 mm shift; assays in both alternatives match the report rows; no literature left; guards pass. Found and fixed one overstatement: the exam records only a "questionable" right upper quadrant field deficit, but `key_clinical_evidence[0]`, the depression differential entry and `red_herrings[0].correct_interpretation` called it a field defect; all three now say "a possible right upper quadrant field defect". Not changed: the MRI impression keeps "Tissue diagnosis recommended", which the plan (C9) lists for deletion but `TOOL_REPORT_STYLE_GUIDE.md` (the authority on report wording) explicitly allows as a diagnostic forward step; template-shared values with M02 (MRS Cho/NAA 5.3, Ki-67 35%) pre-date this round. perfect_agent and case_io check clean after the edit.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `initial_tool_outputs.mri.impression`: trailing sentence "Tissue diagnosis recommended." removed, for uniformity with the other 25 GLIO-HG MRI impressions (imaging-only, plan C9); the style guide allows it, so this is consistency, not an error fix.
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (left temporal lobe)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (left temporal lobe)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).
