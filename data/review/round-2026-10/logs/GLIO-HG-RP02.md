# GLIO-HG-RP02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 39e8c0d3-a507-4ea2-ac10-1f12a22510e3 | FIXED | `initial_tool_outputs.tissue_diagnosis` set to null; the layered report is now served only by `obtain_tissue_diagnosis` follow-ups (`followup_outputs[6]` resection, `[7]` stereotactic biopsy), identical integrated diagnosis and molecular results; template meta-text removed from the impression. |
| 41984330-e782-4dbc-9aec-4a629240e197 | FIXED | `action-1-analyze-brain-mri.expected_evidence` written from this MRI (incomplete irregular ring, medial nodule, central FLAIR hypointensity, no central restriction, minimal rim restriction, edema, 3 mm shift, separate 8 mm left frontal lesion); the old pearl is replaced by `key_clinical_evidence[2]` with the same description. |
| 2b8748f1-95d6-4909-86ce-7aa1ff7cf15a | FIXED (both options, as the plan decides) | Differential: tumefactive demyelination (low; incomplete ring, second lesion and sister's MS for; rCBV 4.2, Cho/NAA 5.2, histology against) and tuberculoma (low; treated TB and calcified granulomas for; perfusion, spectroscopy, histology against) with discriminators. Red herrings added for the sister's MS with the second lesion, the treated tuberculosis, and the sinusitis with raised ESR/CRP. The MRI impression keeps the imaging differential but no longer cites the family history. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.cranial_nerves` | "Right lower facial droop" with a right frontal lesion and left arm and leg weakness (laterality flip). | FIXED: "Left lower facial droop". |
| D | major | `patient.history_present_illness` | "initial imaging, which revealed an intracranial abnormality" (C8). | FIXED: outside non-contrast CT with a right frontal hypodense lesion, edema and 3 mm shift. |
| C | major | `action-9-obtain-tissue-diagnosis` | Biopsy only (C3); 1p/19q required in an IDH-wildtype case, no ATRX (C4). | FIXED: group A, `resection` then `stereotactic_biopsy`; minimum `IDH1_IHC, IDH1_IDH2_sequencing, ATRX_IHC, MGMT_methylation` (age 44); report adds ATRX (retained) and renames "IDH2 sequencing" to IDH1/IDH2 sequencing; GFAP moved into the Histology row. |
| C | major | `action-3-search-medical-literature`, `followup_outputs[4]` | Literature as a required step; output with invented claims ("pathognomonic", "95% specific") (C1). | FIXED: deleted. |
| C | major | `followup_outputs[6]` (CSF) | LP performed in a patient with mass effect and a harm entry for it (C17). | FIXED: CSF follow-up deleted; harm kept with the canonical rationale (3 mm shift, frontal horn effacement, right disc blurring). |
| C | major | `followup_outputs[3]` | fMRI filed as `perfusion_MRI`, DTI only in the impression (C6). | FIXED: retagged `functional_MRI` (hand area 8 mm, LI 0.82); new `DTI_tractography` follow-up (CST displaced, 5 mm, preserved); both recommended criteria, soft constraints to tissue. |
| C | major | `assessment.required_recommendations` | No plan for the staring spell; biopsy and resection interchangeable; template Stupp and dexamethasone musts; no contraception note before temozolomide at 44. | FIXED: uncertain-class must 3 and recommended `action-eeg-characterise-spells`; must 1 group A with fMRI, DTI, mapping; canonical dexamethasone; must 6 contraception; must 7 entity-specific (KPS 80). |
| C | minor | `assessment.prohibited_recommendations` | No guard against empirical treatment of the mimics. | FIXED: prohibition 4 (no demyelination or tuberculoma treatment without tissue). |
| D | minor | `initial_tool_outputs.eeg.impression` | Clinical essay; equivocal sharp transients over the left temporal region with no laterality statement (C9). | FIXED: ACNS list; the transients are stated as contralateral to the focal slowing and not meeting epileptiform criteria (data kept). |
| B | minor | `initial_tool_outputs.mri.findings[2]` | Ovoid lesion "oriented parallel to the lateral ventricle", while the report uses it to raise demyelination (typical ovoid demyelinating lesions are perpendicular). | FIXED: "perpendicular"; impression numbered. |
| C | minor | new `action-performance-status`, `followup_outputs[3]` | Performance status absent (C7). | FIXED: recommended; KPS 80, ECOG 1. |
| C | minor | `initial_tool_outputs.labs` | No type and screen in the panel although the criterion orders it; no pregnancy test in a 44-year-old before contrast CT and surgery. | FIXED: "Baseline workup" panel with type and screen and negative beta-hCG; summary and interpretation recomputed (anion gap 12, MCHC 33.5). |
| C | major | `followup_outputs[5]` (DDI) | Temozolomide check; penicillin allergy conflated with sulfonamide; lomustine, bevacizumab, TTFields alternatives. | FIXED: dexamethasone plus levetiracetam-if-seizure with her medicines (SSRI-steroid GI bleeding, sertraline-sumatriptan, levetiracetam and anxiety), penicillin allergy stated correctly, TB reactivation warning. New optional criterion `action-check-drug-interactions`, last. |
| D | minor | `followup_outputs[1]`, `[2]` | "(normal < 1.5)" and "suggesting tumor infiltration" in the MRS signal; CT impression "consistent with prior tuberculous infection and not active disease". | FIXED: values kept, interpretive clauses removed; numbered impressions. |
| C | minor | `ground_truth.differential` | Lymphoma and demyelination keyed on a "closed ring", which this MRI does not have; no entry above low and no tuberculoma (see 2b8748f1). | FIXED: rewritten from this case's findings. |
| B | minor | criteria citations, rationales, sequence, stop rule, metadata | Duplicate bare keys; rationales copied from labels; one soft constraint; literature in the stop rule. | FIXED: one bracketed key; case-specific rationales; hard MRI and labs to tissue, soft fMRI and DTI to tissue; stop rule MRI, labs, tissue; metadata updated. |

## Changes, in one paragraph a physician can read before re-reviewing

A 44-year-old woman with a right precentral glioblastoma, IDH-wildtype, mimicking tumefactive demyelination (sister with MS, second small white matter lesion) and tuberculoma (treated TB). The facial weakness is now on the left, as the lesion requires, and the HPI has an outside CT instead of an unstated "initial imaging". Work-up: contrast MRI (required), perfusion (rCBV 4.2) and spectroscopy (Cho/NAA 5.2), EEG for the single staring spell (recommended; right frontocentral slowing, equivocal contralateral transients), staging CT (optional), labs with type and screen and a negative beta-hCG (required), performance status (KPS 80), functional MRI and DTI of the motor system, then tissue by maximal safe resection or stereotactic biopsy (required; IDH1 IHC, IDH sequencing, ATRX, MGMT), drug check optional and last. The CSF study is gone and LP stays harmful. Musts: resection with fMRI, DTI and mapping; EEG and levetiracetam only if the spell is a seizure; dexamethasone; contraception before temozolomide; MDT for 60 Gy with temozolomide. The differential now carries demyelination and tuberculoma at low likelihood with their discriminators, and three new red herrings explain the MS, TB and sinusitis clues.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[AIOM_brain]` used in the tissue and EEG criteria (plan 5.1).
- Synonyms: "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan 5.2); accepted[0] "WHO grade 4" to "CNS WHO grade 4" if the synonym tool allows.

## Open questions for Andrea (judgment calls you could not settle)

None. Decided in-round: the equivocal sharp transients stay where they were recorded (left temporal) and the report now states that they are contralateral, rather than moving recorded data to the lesion side.

## Verification

Adversarial verifier, 24 Oct 2026. All three note ids are in the table and applied (tissue only in two follow-ups; action-1 evidence matching the MRI's incomplete ring and absent central restriction; tumefactive demyelination and tuberculoma at low with discriminators, plus red herrings for the sister's MS with the second lesion, the treated TB and the sinusitis). Checked the left facial droop fix against the right precentral lesion and left hemiparesis, the outside CT in the HPI, the 3 mm shift, frontal horn effacement and right disc blurring against the LP harm entry, labs flags and the added beta-hCG, KPS 80 against the treatment must, fMRI and DTI outputs against their criteria, the EEG laterality statement, and identical tissue reports. Found and fixed:
- `patient.history_present_illness` said the sister "was recently diagnosed" with MS, while `family_history[2]` gives the diagnosis at 35 in a sister now 40: now "Her younger sister has multiple sclerosis, diagnosed five years ago."
- `action-eeg-characterise-spells.rationale` called the spell "unwitnessed-onset", which the HPI does not say (the husband witnessed it): now "A single witnessed 10-second staring spell with amnesia".
- `metadata.difficulty_rationale` said "seven recommended" while listing and having six: corrected.
Re-ran perfect-agent (pass), `case_io.py check` (no failure names the case) and the case guards (pass).

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `ground_truth.red_herrings[0].field_path` was empty: now `patient.clinical_history.past_medical_history[1]`.
- `patient.neurological_exam.mental_status`: language now "Speech is fluent with normal rate and prosody. No paraphasic errors. Naming intact ..."; a right frontal lesion with left-dominant language does not explain aphasic signs.
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (right frontal)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (right frontal)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Obtain pre-operative labs (CBC, BMP, coagulation, type & screen) before craniotomy/biopsy' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Minor non-specific finding.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).
