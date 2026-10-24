# GLIO-HG-RM04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 16ac8653-bfe7-44c6-8ffb-75b9b1434166 | FIXED | Probable class (C5): the levetiracetam "prophylaxis" must replaced by must 3 (treat the stereotyped staring spells with lip-smacking as probable focal impaired-awareness seizures, EEG, levetiracetam, avoid enzyme inducers). New recommended criterion `action-eeg-characterise-spells` and a new `initial_tool_outputs.eeg` (right temporal polymorphic delta, occasional F8/T8 sharp waves, no electrographic seizure); `avoid-waste-3-analyze-eeg` deleted; the normal fallback EEG set to null so no contradicting EEG can be served. Key evidence item 2 states the treatment. |
| 2cd403c7-31bf-4d35-8e92-6f94cfa4eaf8 | FIXED | `action-11-obtain-tissue-diagnosis` is group A: `resection` first, `stereotactic_biopsy` second, canonical label and rationale; two tissue follow-ups (`followup_outputs[6]` resection with an extent-of-resection row, `[7]` biopsy); must 1 is the canonical group A surgery must with fMRI, DTI and intraoperative mapping. |
| b8bef5c9-a0bb-4a58-b696-e1600f0da55e | FIXED | `action-8-analyze-brain-mri` (standard, no contrast, sequences DTI/fMRI) and its `analyze_brain_mri` follow-up deleted; replaced by `action-fmri-functional-mapping` (`functional_MRI`: language laterality index 0.86 left, face motor area 5 mm and hand motor area 12 mm from the tumour) and `action-dti-tractography` (`DTI_tractography`: optic radiation in contact, CST displaced 6 mm, arcuate displaced), both recommended, with soft constraints to tissue. The right-arcuate explanation of the anomia is gone from every field; key evidence item 5 states that with left dominance the anomia is explained by mass effect, oedema, raised pressure or seizures. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | "Emergency brain MRI ... demonstrated a right temporal lobe mass" leaks the scored MRI (C8). | FIXED: outside non-contrast CT with a right temporal mass, surrounding hypodensity and 4 mm leftward shift. |
| D | minor | `patient.neurological_exam.additional` | KPS 80 given in the exam while performance status is now a criterion. | FIXED: removed; the KPS is in the performance-status output (KPS 80, ECOG 1). |
| D | blocker | `initial_tool_outputs.tissue_diagnosis` | Integrated diagnosis served upfront (C2). | FIXED: moved to two follow-ups; meta-text removed; GFAP and reticulin moved from `molecular_findings` to the Histology row and `histological_diagnosis`. |
| C | major | `ground_truth.diagnosis.accepted[0]`, tissue `integrated_diagnosis` | "Gliosarcoma, IDH-wildtype, WHO grade 4" is not a WHO CNS5 integrated diagnosis: gliosarcoma is a histological subtype of glioblastoma, IDH-wildtype (plan open question 2, same logic as the RS04 ruling). | FIXED: accepted[0] "Glioblastoma, IDH-wildtype, CNS WHO grade 4 (right temporal lobe)"; integrated diagnosis "Glioblastoma, IDH-wildtype, CNS WHO grade 4", histology "Gliosarcoma (glioblastoma subtype)". Listed under CENTRAL. ICD C71.2 unchanged. |
| C | major | `action-11` `molecular_assays` | List contained 1p_19q_codeletion in an IDH-wildtype case (C4). | FIXED: minimum `IDH1_IHC, ATRX_IHC, MGMT_methylation` (age 57, MVP and necrosis); report keeps sequencing, TERT, EGFR, +7/-10, TP53 and 1p/19q as extra rows, one row per assay. |
| C | major | `ground_truth.differential[0]` | The ground truth ("Glioblastoma, classic variant", very high) in its own differential; metastasis moderate after the work-up; lymphoma and abscess low. | FIXED: entry deleted; hemorrhagic metastasis low, PCNSL, abscess, tumefactive demyelination very low, with discriminators from the case. |
| B | major | `initial_tool_outputs.mri.findings[0].location` vs old fMRI | "within 5 mm of the precentral gyrus of the parietal operculum" (anatomically confused) against "motor cortex 12 mm superior" in the fMRI. | FIXED: MRI "within 5 mm of the inferior precentral gyrus at the frontal operculum"; fMRI reports the face area at 5 mm and the hand area at 12 mm. |
| D | minor | `initial_tool_outputs.mri.impression`, `.additional_observations[2]` | Prose impression; "consistent with the clinical left upper quadrantanopia" (cross-modality); "cavernous malformation with malignant degeneration" (not an entity); imaging cannot see a "sarcomatous component". | FIXED: numbered impression with imaging differential "high-grade glial neoplasm, including gliosarcoma; solitary hemorrhagic metastasis cannot be excluded"; clinical clause removed. |
| D | minor | `followup_outputs[0]`, `[1]` | Teaching parentheticals (">1.75 supports", ">2.0 markedly above the threshold"), em dashes, prose impressions. | FIXED: values kept, parentheticals removed, numbered impressions. |
| C | minor | `followup_outputs[2]` (CT CAP) | Duplicated observation rows; "consistent with remote smoking history" (cross-reference). | FIXED: duplicates removed, numbered impression. |
| C | minor | new `action-performance-status`, `followup_outputs[3]` | Performance status absent (C7). | FIXED: recommended (age 57); KPS 80, ECOG 1 from the exam and HPI. |
| C | major | `followup_outputs[8]` (DDI) | "Levetiracetam (seizure prophylaxis)"; "dexamethasone may reduce levetiracetam levels via CYP induction" (levetiracetam has no CYP metabolism); TMP-SMX sentence about an allergy he does not have; bevacizumab, lomustine and trials as "alternatives". | FIXED: rewritten for levetiracetam and dexamethasone with his five medicines (dexamethasone against metformin and sitagliptin, aspirin GI and perioperative platelet effect, no levetiracetam interactions, enzyme inducers to avoid). |
| C | minor | `action-9-check-drug-interactions` | Plan says optional unless a concrete interaction exists. | FIXED (kept recommended, decided): there is a concrete pharmacodynamic interaction (dexamethasone against oral glucose-lowering drugs, HbA1c 8.1%) and an antiplatelet drug before craniotomy; label, evidence, rationale rewritten; stays last. |
| C | major | `assessment.required_recommendations` | No aspirin plan before craniotomy; thrombocytopenia must vague; Stupp must generic; dexamethasone must without the diabetes; old musts 2 (awake craniotomy for a non-dominant arcuate) and 3 (fMRI order, now a criterion). | FIXED: must 5 repeat platelet count and blood film, stop aspirin 7 days before craniotomy; must 4 canonical dexamethasone with insulin expected; must 7 entity-specific (age 57, KPS 80: 60 Gy with temozolomide); old musts 2 and 3 replaced by must 1; must 6 driving advice (seizures, quadrantanopia). |
| C | minor | `avoided_actions` | LP harm rationale generic; waste rationales cite NCCN. | FIXED: canonical C17 rationale (4 mm shift, sylvian effacement); echo and Holter "No cardiac question in this presentation" `[EANO_2021]`. |
| C | minor | `ground_truth.red_herrings[0].correct_interpretation` | Thrombocytopenia "related to bone marrow suppression from the tumor" (a brain tumour does not suppress marrow). | FIXED: isolated mild thrombocytopenia above the threshold; confirm and stop aspirin. Red herrings 1 and 2 reworded without "the diagnosis is". |
| C | minor | `action-1`, `action-2`, `action-6`, `action-7` | Template evidence and rationales; perfusion label "confirm high-grade"; `[Stupp_2005]` on MRI; duplicate bare citation keys. | FIXED: evidence from the case's own values; "target the sampling"; one bracketed key each. |
| B | minor | `initial_tool_outputs.labs` | Interpretive summary ("likely perioperative stress contribution"); `type_and_screen` template significance. | FIXED: plain summary; significance null. Values checked (anion gap 12, MCHC 33.5, PT/INR concordant). |
| B | minor | `sequence_constraints`, `stop_rule`, `metadata` | Single soft constraint; literature in the stop rule; metadata named 5 required tools and an EEG fallback kind. | FIXED: hard MRI and labs to tissue, soft fMRI and DTI to tissue; stop rule MRI, labs, tissue; metadata updated. |

## Changes, in one paragraph a physician can read before re-reviewing

A 57-year-old right-handed diabetic man with a right temporal glioblastoma, IDH-wildtype (gliosarcoma subtype), probable focal seizures, quadrantanopia and mild left hemiparesis. The HPI now has an outside non-contrast CT, not the MRI. Work-up: contrast MRI (required), perfusion and spectroscopy, an EEG for the stereotyped spells (new report: right temporal slowing and sharp waves), staging CT (optional), labs (required), performance status (KPS 80, ECOG 1), functional MRI (left language dominance, face motor area 5 mm from the tumour) and DTI (optic radiation in contact, corticospinal tract displaced) before tissue, then tissue by maximal safe resection or stereotactic biopsy (required; minimum IDH1 IHC, ATRX, MGMT), and the drug check last (recommended because of dexamethasone against his oral hypoglycaemics and the aspirin). The label is now "Glioblastoma, IDH-wildtype, CNS WHO grade 4" with gliosarcoma as the histology. Musts: resection with fMRI, DTI and mapping; treat the spells with levetiracetam (EEG to characterise); dexamethasone with insulin expected; repeat platelet count and stop aspirin before surgery; no driving; MDT for 60 Gy with temozolomide. The anomia is no longer attributed to the right arcuate fasciculus.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Label change (ruling 3): accepted[0] "Gliosarcoma, IDH-wildtype, WHO grade 4 (right temporal lobe)" to "Glioblastoma, IDH-wildtype, CNS WHO grade 4 (right temporal lobe)" (plan 5.3, open question 2 resolved with the plan's assumption).
- Synonyms: add "gliosarcoma" as an accepted label for this case (a WHO CNS5 subtype of glioblastoma, IDH-wildtype; an answer naming it is correct but matches no current label token set); "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan 5.2).
- `[AIOM_brain]` used in the tissue and EEG criteria (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

None. Decided in-round: drug check kept recommended rather than optional (concrete dexamethasone-antidiabetic interaction and perioperative aspirin); the right arcuate fasciculus stays in the DTI report as an imaging fact, without clinical attribution.

## Verification

Adversarial verifier, 24 Oct 2026. All three note ids are in the table and applied (probable-seizure must, recommended EEG with a new report and no EEG waste entry or normal fallback EEG; group A resection then biopsy with two tissue follow-ups; fMRI and DTI as separate recommended criteria with soft constraints and no right-arcuate attribution of the anomia). Checked laterality, the 4 mm shift in HPI CT, MRI and LP rationale, labs flags and arithmetic, creatinine 1.0 against the levetiracetam warning, the drug-check tier decision (kept recommended for a concrete dexamethasone-antidiabetic interaction: defensible under ruling 6), KPS 80 against the treatment must, the label change (CENTRAL) and identical tissue reports. Found and fixed:
- `initial_tool_outputs.mri.impression`: the MRI named "gliosarcoma" (a histological subtype that imaging cannot identify; answer leakage of the case's subtype) and ended with "Tissue diagnosis recommended." (management text, plan C9). Now "most consistent with a high-grade glial neoplasm; a solitary hemorrhagic metastasis cannot be excluded", without the recommendation.
- `ground_truth.red_herrings[2].data_point` claimed "HbA1c 8.1%" for `past_medical_history[0]`, which records 7.8% three months ago (8.1% is the admission panel). Now "Type 2 diabetes mellitus on metformin and sitagliptin (HbA1c 7.8% three months ago, 8.1% on the admission panel)".
Re-ran perfect-agent (pass), `case_io.py check` (no failure names the case) and the case guards (pass).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain urgent MRI brain with and without gadolinium contrast (tumor protocol with DWI, FLAIR, SWI) before any invasive procedure' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must rewritten: 'Obtain pre-operative CBC, BMP, coagulation, and type & screen; confirm the platelet count of 118 x10^9/L with a repeat count and blood film, and stop aspirin (primary prevention) about 7 days before craniotomy.' -> 'Confirm the platelet count of 118 x10^9/L with a repeat count and blood film before surgery, and stop aspirin (primary prevention) about 7 days before craniotomy.' (Q9: the duplicated diagnostic part dropped, the management part kept)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype', 'gliosarcoma'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
