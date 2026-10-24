# GLIO-HG-RP04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0c2fc022-a855-4f5a-9293-b22780913ad3 | FIXED | `action-9-obtain-tissue-diagnosis` assays now `IDH1_IHC, IDH1_IDH2_sequencing, ATRX_IHC, MGMT_methylation, SOX10_IHC, Melan_A_HMB45_IHC` in both alternatives; tissue follow-ups (`followup_outputs[4]` biopsy, `[5]` resection) report SOX10 negative and Melan-A and HMB-45 negative, one row per assay (S100 kept as an extra row); must 7 names SOX10, Melan-A and HMB-45, all now orderable and reported. `H3K27_status` dropped from the required list (no midline lesion: the dominant mass is hemispheric with extension into the splenium); the report still states H3 K27M not detected, H3K27me3 retained. |
| eb3f1800-42e2-4dcb-a081-48d4d69effb1 | FIXED | Treat class (C5): must 3 starts levetiracetam for the documented focal seizure (15 s speech arrest with staring and unawareness), as treatment, with enzyme inducers avoided. `avoid-waste-1-analyze-eeg` deleted; new recommended `action-eeg-characterise-spells`; new `initial_tool_outputs.eeg` (right parieto-occipital delta slowing, occasional left mid temporal sharp waves, no electrographic seizure); the normal fallback EEG set to null. The drug check proposes levetiracetam for the seizure, not "prophylaxis/treatment". |
| 0289beef-683c-41fa-b52e-02116219c4d4 | FIXED | New required `action-performance-status` (in the stop rule) with a follow-up from the current examination: KPS 70, ECOG 2 (independent in self-care, unable to work because of memory and executive lapses, mild left hemiparesis, quadrantanopia). `social_history.functional_status` now reads "Before the current illness: Karnofsky Performance Status 80 ...". Must 9 reads the regimen from the current KPS. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.cranial_nerves` | "right homonymous inferior quadrantanopia" with a right parieto-occipital lesion (laterality flip). | FIXED: "left homonymous inferior quadrantanopia". |
| B | minor | `patient.history_present_illness` | "completed the recommended five-year surveillance protocol" for a melanoma excised three years ago. | FIXED: "remains in the recommended five-year surveillance protocol"; em dashes in the edited sentence removed. |
| D | blocker | `initial_tool_outputs.tissue_diagnosis` | Integrated diagnosis served upfront (C2); template meta-text; site listing all three lesions for one biopsy. | FIXED: two follow-ups, biopsy of the dominant rim and cytoreductive resection with an extent row; integrated diagnosis "Glioblastoma, IDH-wildtype, CNS WHO grade 4"; impression one line with MGMT and the melanocytic markers. |
| C | major | `action-9` alternatives | Biopsy only; 1p/19q required in an IDH-wildtype case (C3, C4). | FIXED: group C, `stereotactic_biopsy` then `resection` (cytoreduction of the dominant lesion); list per plan; label, evidence and rationale rewritten. |
| C | major | `action-3-search-medical-literature`, `followup_outputs[3]` | Literature as a required step and in the stop rule (C1). | FIXED: deleted; the perilesional rCBV and choline discriminator moved into the perfusion and spectroscopy rationales. |
| C | major | `assessment.required_recommendations` | No antiseizure must; no aspirin plan; template dexamethasone; no treatment must; biopsy without resection alternative. | FIXED: must 1 group C; must 3 levetiracetam (treat); must 4 canonical dexamethasone; must 8 stop aspirin 7 days before surgery and no driving; must 9 entity-specific (age 52, KPS 70: 60 Gy covering all three lesions with temozolomide, MGMT unmethylated, hypofractionated if KPS falls below 70). |
| C | major | `ground_truth.differential` | Melanoma metastasis "high" and unknown-primary metastasis "moderate" after the work-up excluded them. | FIXED: melanoma metastasis low, the others very low, with this case's discriminators including SOX10. |
| C | major | `followup_outputs[4]` (DDI) | "Levetiracetam (seizure prophylaxis/treatment)"; alternatives with em dashes; no aspirin timing. | FIXED: rewritten for dexamethasone and levetiracetam with amlodipine, hydrochlorothiazide and aspirin (potassium, blood pressure, GI bleeding, aspirin before surgery); new optional `action-check-drug-interactions`, last. |
| D | minor | `initial_tool_outputs.mri.impression`, finding types | Prose impression ending "Tissue diagnosis is required"; em dashes in the finding types. | FIXED: numbered imaging-only impression with the differential; types reworded. |
| D | minor | `followup_outputs[0]`, `[1]`, `[2]` | Interpretive clauses in perfusion and MRS signals ("indicating tumor infiltration", "above what would be expected"); CT impression "MRI liver recommended" (management advice). | FIXED: values kept, clauses removed, numbered impressions. |
| C | minor | `avoided_actions` | LP harm rationale generic; cardiac waste rationales cite NCCN. | FIXED: canonical C17 (6 mm shift, right occipital horn effacement); "No cardiac question in this presentation". |
| B | minor | `initial_tool_outputs.labs` | Interpretive summary ("borderline", "likely non-fasting"). | FIXED: plain summary and interpretation. Values checked (anion gap 10, MCHC 33.0, PT/INR concordant). |
| C | minor | `key_clinical_evidence`, `red_herrings`, citations, sequence, stop rule, metadata | Unsupported "2-5%" figures; markers without SOX10; duplicate bare keys; single soft constraint; metadata "neurosurgery consult, neuro-oncology consult" as tools. | FIXED: case-specific evidence; SOX10 in the red herrings; one bracketed key; hard MRI and labs to tissue; stop rule MRI, labs, CT CAP, performance status, tissue; difficulty rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

A 52-year-old man with a prior cutaneous melanoma and three enhancing lesions (dominant right parieto-occipital, right frontal, left superior temporal) that prove to be a multicentric glioblastoma, IDH-wildtype. The quadrantanopia is now on the left, as the right parietal lesion requires. The speech arrest with staring is treated as a focal seizure: an EEG is recommended (right posterior slowing, left temporal sharp waves) and levetiracetam is a must. Work-up: contrast MRI, labs, staging CT and current performance status (all required; KPS 70, ECOG 2, down from a pre-illness 80), perfusion and spectroscopy showing infiltration beyond enhancement (recommended), then tissue by stereotactic biopsy of the dominant lesion or its cytoreduction (required; IDH1 IHC and sequencing, ATRX, MGMT, SOX10, Melan-A and HMB-45). The pathology now reports SOX10, so the melanoma-exclusion must can be met. Drug check is optional and last. Musts add aspirin withdrawal before surgery, no driving, and a regimen chosen by the current KPS (60 Gy covering all lesions with temozolomide, MGMT unmethylated).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.2): "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma; accepted[0] "WHO grade 4" to "CNS WHO grade 4" if the synonym tool allows.
- `[AIOM_brain]` used in the tissue and EEG criteria (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

None. Decided in-round: `H3K27_status` not required, because the splenial extension of a hemispheric mass is not a midline diffuse glioma site (the report still states the result); KPS 70 rather than 60, because he is independent in self-care and stopped working only because of the cognitive lapses; the speech arrest is attributed to the left superior temporal lesion, which the new EEG supports with left temporal sharp waves.

## Verification

Adversarial verifier, 24 Oct 2026. All three note ids are in the table and applied: SOX10_IHC and Melan_A_HMB45_IHC in both tissue alternatives and reported negative in both tissue follow-ups, must 7 naming only orderable markers; treat-class levetiracetam must, recommended EEG with a new report, no EEG waste entry and no normal fallback EEG; required performance status in the stop rule with KPS 70 / ECOG 2 derived from the exam and the pre-illness KPS 80 labelled as such. Checked the left inferior quadrantanopia against the right parietal lesion, the left temporal sharp waves against the left superior temporal lesion and the speech arrest, the 6 mm shift against the LP harm entry, the required CT CAP and its hepatic red-herring path, labs flags, aspirin and hydrochlorothiazide in the drug check, the treatment must against KPS 70 and MGMT unmethylated, identical tissue reports, and the decision not to require H3 K27 status (hemispheric mass with splenial extension; H3 K27M still reported not detected): defensible. Found nothing that needed a change; no edit made.

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4, multicentric (right parieto-occipital dominant lesion with right frontal and left temporal satellite lesions)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4, multicentric (right parieto-occipital dominant lesion with right frontal and left temporal satellite lesions)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) as the first step to characterize the multifocal lesions and define biopsy target' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Perform systemic staging CT chest/abdomen/pelvis with contrast to exclude active extracranial primary malignancy before diagnosing primary brain tumor' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Order pre-operative labs (CBC, CMP, coagulation, type and screen) before any surgical intervention' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- fallback specialized_test (generic 'No abnormality identified on this study.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).
