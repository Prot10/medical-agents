# GLIO-HG-RM01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 16e1c115-3e82-473e-9203-8968b3b9cc80 | FIXED | `action-10-obtain-tissue-diagnosis` assays are now `IDH1_IHC`, `IDH1_IDH2_sequencing`, `ATRX_IHC`, `H3K27_status`, `MGMT_methylation`, `TERT_promoter`, `EGFR_amplification` and `chr7_gain_chr10_loss` (plan C4, midline row plus the molecular-GBM markers, since the histology has no MVP or necrosis). 1p/19q is no longer required. The tissue report (now the follow-up `request_stereotactic_biopsy`) states "H3 K27M not detected on immunohistochemistry and sequencing; H3K27me3 retained", and adds +7/-10 and ATRX IHC rows. The integrated diagnosis is therefore glioblastoma, IDH-wildtype, CNS WHO grade 4. The surgery must and the key evidence name H3 K27 status, and the differential lists diffuse midline glioma with the H3 result against it. |
| 61968ced-c4f0-4954-8aef-8f0038d2b7ef | FIXED | The levetiracetam must is deleted and the canonical no-seizure prohibition is added as `prohibited_recommendations[4]`. Levetiracetam is gone from the DDI criterion and from `key_clinical_evidence`. EEG waste is added (`avoid-waste-3-analyze-eeg`, canonical rationale). The empty-tool part was ALREADY-FIXED (no criterion has an empty tool). Must 1 (neurosurgery) and must 3 (dexamethasone) are management, so they stay musts, rewritten as the group C surgery must and the canonical dexamethasone must. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.tissue_diagnosis` | Tissue sat in the initial work-up. It carried template meta-text in the impression, the site was "as targeted on the contrast-enhancing rim" (the lesion has no rim), and it had a `diagnosis_suffix` (plan C2). | FIXED: moved to the follow-up `request_stereotactic_biopsy`. Site is now "Right pons, enhancing solid component". Integrated diagnosis is "Glioblastoma, IDH-wildtype, CNS WHO grade 4", and the impression follows C2 with a single MGMT sentence. Histology row added. |
| A | major | `action-3-search-medical-literature`, literature follow-up | Required literature step in the stop rule (ruling 5). | FIXED: deleted together with its follow-up and its stop-rule id. |
| A | major | criteria, stop rule | No performance status, at age 67 (C7). | FIXED: added a required `action-performance-status` and put it in the stop rule. Its follow-up gives KPS 40 and ECOG 3, with the basis (wheelchair-bound, needs help with transfers and bathing). |
| E | major | `patient.neurological_exam.additional` | The exam gave away the performance-status answer ("Karnofsky performance status estimated at 30-40"). It also carried reasoning text ("most suggestive of a brainstem localization"). | FIXED: both sentences removed. Papilledema and meningismus kept. |
| C | major | `assessment.required_recommendations` | Template Stupp must, for a patient whose KPS is 30-40, with MGMT unmethylated. | FIXED: entity-specific must per plan 1.2: hypofractionated radiotherapy 40 Gy in 15 fractions alone (MGMT unmethylated), with best supportive care as the alternative (EANO 2021). |
| C | major | `assessment.required_recommendations` | Must list was a template: biopsy and resection given as interchangeable, steroid template, and labs repeated as a must. Nothing on aspirin before biopsy or on the fourth-ventricle watch. | FIXED: group C surgery must (stereotactic biopsy, not resection, H3 K27 named); canonical dexamethasone must; glucose must specific to metformin; aspirin hold before biopsy; hydrocephalus watch for the fourth-ventricle compression. The MRI must is kept. The labs must is removed because the labs criterion covers it. |
| B | major | `followup_outputs` (`request_functional_mri`) | Follow-up tagged `perfusion_MRI` but returning fMRI and DTI content (C6); no resection is planned. | FIXED: deleted. |
| A | minor | `followup_outputs` (`request_asl_perfusion`) | A second `analyze_brain_mri` follow-up returning ASL perfusion. It is not a duplicate of the initial MRI, but it adds nothing to the DSC perfusion, and a repeat MRI order would receive it. | FIXED: deleted. |
| B | major | DDI follow-up | Proposed temozolomide before tissue. Its warnings leaked "MGMT promoter is unmethylated" to any query, and it proposed dapsone without the cross-sensitivity caveat. | FIXED: the follow-up now checks dexamethasone against his five medicines (metformin glycaemia, aspirin bleeding, amlodipine CYP3A4, tamsulosin, acetaminophen). It covers the sulfonamide allergy, the dapsone caveat and atovaquone. The criterion stays optional and last; the guard passes. |
| B | major | `action-1-analyze-brain-mri` expected evidence, `key_clinical_evidence` | Template text: "ring enhancement, central necrosis", plus headache and seizure. The MRI reports solid enhancement without necrosis, and he has had neither headache nor seizure. | FIXED: expected evidence and key evidence now come from the case's own findings. |
| D | minor | MRI impression | Listed "anaplastic astrocytoma" (a retired term) in a long differential. | FIXED: numbered impression with a single hedged differential line. |
| C | minor | `patient.neurological_exam.cranial_nerves` | "Right peripheral facial weakness (lower face only)": lower-face-only weakness is a central pattern, while a pontine lesion of the facial nucleus or fascicle gives peripheral weakness. | FIXED: "involving both the forehead and the lower face (peripheral pattern)". |
| C | minor | `patient.neurological_exam.coordination` | Ataxia was worse on the left, although the lesion involves the right middle cerebellar peduncle (ipsilateral ataxia expected). | FIXED: marked right dysmetria; the left side is limited by weakness. Gait still falls to the left, which the left leg weakness explains. |
| B | minor | `initial_tool_outputs.eeg` | Right posterior temporal-occipital focal slowing, with no supratentorial lesion to explain it. | FIXED: the focal finding is removed. The EEG now shows non-specific diffuse slowing. |
| B | minor | perfusion and MRS follow-ups | Grading thresholds were quoted (">1.75", ">2.0"). MRS wrote "suggesting necrosis" although the histology has no necrosis, and its impression read "See findings above". | FIXED: thresholds removed, `quantitative_data` filled, and the impressions now state biopsy targeting. |
| B | minor | `initial_tool_outputs.labs` | `type_and_screen` row under "Baseline workup" carried meta-text. HbA1c was a string. The summary used dashes. | FIXED: Blood_Bank row with `clinical_significance` null; HbA1c is numeric; summary and interpretation are factual. Anion gap 13 and MCHC 34.3 were checked. |
| C | minor | `ground_truth.differential` | Metastasis and demyelination were each listed twice, and "staging negative" assumed an optional CT. Diffuse midline glioma, the key alternative in the pons, was missing. | FIXED: six entries, each with what supports and what excludes it, at assessment time. |
| A | minor | citations, constraints, avoided actions | Duplicate keys and `WHO_CNS5`; `[Stupp_2005]` on the MRI criterion; one template soft constraint; template waste and LP rationales. | FIXED: bracketed keys only. Hard constraints MRI to tissue and labs to tissue. Cardiac rationale is canonical. The LP harm rationale names the fourth-ventricle compression and prepontine effacement (C17), and the prohibition is aligned with it. |
| C | minor | red herrings, metadata | No red herrings. The difficulty description used retired grade III wording and claimed a ring-enhancing mass with necrosis. | FIXED: two red herrings (the false-negative non-contrast CT with a spinal attribution; smoking with weight loss). Metadata descriptions rewritten. Aspirin indication set to primary prevention. |

## Changes, in one paragraph a physician can read before re-reviewing

A 67-year-old man with type 2 diabetes. He has two months of progressive dizziness, dysarthria and a left-predominant spastic paraparesis, and on examination a right INO, right peripheral facial weakness and right-sided ataxia. He has no seizures, and a community non-contrast CT was read as normal. Pathway:
- Contrast MRI: an infiltrative 3.2 cm right pontine mass with solid heterogeneous enhancement, no necrosis, extension into the right middle cerebellar peduncle, and fourth-ventricle compression.
- Perfusion and spectroscopy, used to target the biopsy.
- Optional body CT (negative).
- Pre-operative labs (glucose 148, HbA1c 7.2).
- Performance status, now required: KPS 40, ECOG 3.
- Stereotactic biopsy: glioblastoma, IDH-wildtype, CNS WHO grade 4. H3 K27M was not detected and H3K27me3 is retained. Grade 4 rests on TERT, EGFR and +7/-10, without MVP or necrosis. MGMT is unmethylated.

Literature, the fMRI and ASL add-ons, and the levetiracetam must are gone, and antiseizure prophylaxis is now prohibited. Musts:
- biopsy rather than resection;
- dexamethasone, with glucose management on metformin;
- hold aspirin;
- watch for hydrocephalus;
- after the diagnosis, hypofractionated radiotherapy alone or best supportive care.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: accepted[0] reads "WHO grade 4 (pontine / brainstem)" (plan 5.3, CNS WHO wording). "astrocytoma grade 4" is wrong for IDH-wildtype glioblastoma (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing your information. Decisions recorded:
  - The required assay list includes all three grade-4 molecular markers (TERT, EGFR, +7/-10), as plan C4 sets, although any one of them suffices.
  - With KPS 40 the treatment must offers hypofractionated radiotherapy alone or best supportive care, rather than the plan's age-based default.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the notes (16e1c115, 61968ced) and the whole final case.
- Notes: both are in the table and fixed. H3K27_status and IDH sequencing are required, and the report reads "H3 K27M not detected; H3K27me3 retained", so the IDH-wildtype, H3-wildtype molecular grade 4 is supportable (TERT, EGFR and +7/-10 are all present). There is no levetiracetam must and the prohibition is present. No criterion has an empty tool, and musts 1 and 3 are management.
- Localisation checked against the right pontine lesion:
  - right INO, with an adduction deficit of the right eye and abducting nystagmus of the left;
  - right peripheral facial palsy;
  - right appendicular ataxia from the middle cerebellar peduncle;
  - left-predominant corticospinal and sensory signs.
- Other cross-field checks:
  - KPS 40 / ECOG 3 against the wheelchair-bound history, with no KPS leak left in the exam;
  - the hypofractionated-RT-or-supportive-care must against KPS 40 and unmethylated MGMT;
  - the sulfonamide allergy in the DDI output;
  - anion gap 13, MCHC 34.3, and Hct consistent with RBC x MCV.
- Found and fixed: the MRI impression ended "Tissue diagnosis is recommended." Deleted (C9).
- After the fix: `perfect_agent.py` passes, `case_io.py check` reports no failure naming the case, and `test_case_guards` passes.

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (pontine / brainstem)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (pontine / brainstem)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure.' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['glioma who grade 4', 'grade 4 glioma', 'astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
