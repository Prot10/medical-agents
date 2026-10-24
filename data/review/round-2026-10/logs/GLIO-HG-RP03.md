# GLIO-HG-RP03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 4ebbab11-ee50-41ae-8965-41d4258b8e3c | FIXED (add-CDKN2A/B option, as the plan decides) | Tissue report now in two `obtain_tissue_diagnosis` follow-ups (`followup_outputs[6]` stereotactic biopsy, `[7]` resection) with CDKN2A/B "Homozygous deletion detected", integrated diagnosis "Astrocytoma, IDH-mutant, CNS WHO grade 4", `who_grade` "4"; the "Grade 2 (with features of higher-grade behavior)", original-biopsy and cyst-fluid rows deleted from `findings` and `molecular_findings` (the original biopsy and cyst fluid moved to the HPI and `past_medical_history[3]`). `action-10` assays `IDH1_IHC, IDH1_IDH2_sequencing, ATRX_IHC, 1p_19q_codeletion, CDKN2A_B_deletion, MGMT_methylation`; the rationale states that CDKN2A/B deletion assigns grade 4. `diagnosis.accepted[0]` "Astrocytoma, IDH-mutant, CNS WHO grade 4 with leptomeningeal dissemination" (CENTRAL). |
| 753d78af-1a4b-43ad-917c-96dbfed8d8f0 | FIXED | `avoid-harm-1-analyze-csf` deleted; new recommended `action-csf-cytology` (`analyze_csf` `{"special_tests": ["cytology", "flow_cytometry"]}`) with a hard `action-1` to `action-csf-cytology` constraint `[Hasbun_2001]`; new CSF follow-up (protein 168 mg/dL, glucose ratio 0.32, GFAP-positive atypical glial cells, no clonal lymphoid population on flow). The MRI now states the safety it implied: fourth ventricle patent and not effaced, basal cisterns patent, no herniation; the rationale cites the mild papilledema with a functioning shunt. The LP prohibition is removed. |
| 928080d2-ebbd-4585-a423-efc9fa757bdf | FIXED | `ground_truth.differential[0]` primary CNS lymphoma (low) with the steroid response and non-diagnostic biopsy for it and IDH-mutant glial tissue, GFAP-positive CSF cells and negative flow against it. Must 4 is the plan's text ("Do not start dexamethasone; continue prednisone without abrupt withdrawal ..."); prohibitions 1 and 2 forbid steroid escalation before tissue and abrupt prednisone withdrawal. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | `initial_tool_outputs.tissue_diagnosis` | Integrated diagnosis served upfront (C2); template meta-text; site "as targeted on the contrast-enhancing rim". | FIXED: two follow-ups with real sites, resection with an extent row; impression one line plus MGMT. |
| C | major | `action-10-obtain-tissue-diagnosis` | Biopsy only, with no resection alternative; assay list without sequencing or CDKN2A/B (C3, C4). | FIXED: group C, `stereotactic_biopsy` then `resection` (debulking of the dominant lesion); IDH-mutant list; label, evidence and rationale rewritten. |
| B | major | `initial_tool_outputs.mri.additional_observations[2]` | "No abnormal leptomeningeal enhancement ... in the spinal canal on available cervical sequences" while the spine MRI shows nodules from the cervical level down. | FIXED: replaced by a herniation statement; new observation that the spinal canal is not covered by this study. |
| B | major | `initial_tool_outputs.mri.findings[2]`, `[3]` | Fixed dilated left pupil and right V2/V3 numbness unexplained by any finding; "mild compression of the fourth ventricle" contradicts the safe LP the reviewer note asks for. | FIXED: basal meningeal enhancement now involves the left oculomotor nerve and the right trigeminal nerve at Meckel cave; fourth ventricle abutted, not effaced, no tonsillar descent. |
| C | major | `action-3-search-medical-literature`, `followup_outputs[4]` | Literature as a required step (C1). | FIXED: deleted, and removed from the stop rule. |
| C | major | `followup_outputs[3]` | fMRI filed as `perfusion_MRI` in a biopsy-first case (C6). | FIXED: deleted, as the plan rules for RP03. |
| C | major | `followup_outputs[6]` | Spine MRI filed as `analyze_brain_mri`. | FIXED: converted to `order_body_imaging` (`MRI`, region spine, contrast), numbered impression with "no spinal block"; new recommended `action-spine-mri` (`{"study": "spine_MRI"}`). |
| C | major | `assessment.required_recommendations` | Dexamethasone initiation on top of prednisone; Stupp must for an IDH-mutant tumour; levetiracetam "initiate" in a patient already on it; biopsy and resection interchangeable. | FIXED: must 4 (plan text); must 8 grade 4 managed like glioblastoma, individualised for neuraxis dissemination and KPS 50; must 3 continue levetiracetam with dose review (treat class); must 1 group C; must 6 neuraxis staging; must 7 sperm banking and contraception before temozolomide. |
| C | minor | new `action-performance-status`, `followup_outputs[3]` | Performance status absent (C7). | FIXED: recommended (age 31); KPS 50, ECOG 3 (walker, help with bathing and dressing, supervision for confusion). |
| C | major | `followup_outputs[5]` (DDI) | Temozolomide check with lomustine, bevacizumab and PCV "alternatives". | FIXED: rewritten for levetiracetam and the prednisone taper with omeprazole and calcium (PPI-calcium carbonate absorption, adrenal suppression, PJP risk, hyperglycemia); new optional criterion `action-check-drug-interactions`, last. |
| C | minor | `initial_tool_outputs.labs` | Coagulation in "Additional" without aPTT; interpretive "(steroid effect)" summary; `type_and_screen` template significance. | FIXED: "Coagulation" panel PT 11.8 s, INR 1.0, aPTT 29.5 s; plain summary and interpretation; significance null. Values checked (anion gap 13, MCHC 33.3). |
| D | minor | `initial_tool_outputs.eeg.impression` | Clinical essay ("could be seen in diffuse meningeal disease ..."). | FIXED: ACNS list of the three findings, no epileptiform discharges. |
| D | minor | `initial_tool_outputs.mri.impression`, `followup_outputs[0]`, `[1]`, `[2]` | "gliomatosis" (retired term); MRS "normal <1.5", "would favor abscess", "suggesting necrosis"; perfusion "suggesting blood-brain barrier breakdown"; CT "consistent with surgical history". | FIXED: numbered impressions, imaging-only wording, values kept. |
| C | major | `ground_truth.differential` | GBM at moderate after tissue; demyelination without a basis; no lymphoma, no granulomatous infection. | FIXED: lymphoma and neurosarcoidosis low, granulomatous meningitis, carcinomatosis and IDH-wildtype GBM very low, each with this case's discriminators. |
| C | minor | `ground_truth.red_herrings` | Empty, although the case is built on the sarcoidosis anchor. | FIXED: family sarcoidosis with an early steroid response; raised ESR, CRP and upper-limit ACE. |
| C | minor | `assessment.prohibited_recommendations` | LP prohibition contradicts the recommended CSF; no guard on steroid handling or on continued sarcoidosis treatment. | FIXED: LP prohibition removed; prohibitions on steroid escalation, abrupt withdrawal and untested sarcoidosis treatment. |
| B | minor | criteria labels, rationales, citations, sequence, stop rule, avoided actions, metadata | "the diffuse with leptomeningeal dissemination lesion" (broken label); rationales copied from labels; duplicate bare keys; single soft constraint; literature in the stop rule; generic cardiac waste rationales; metadata concern about grade 2. | FIXED: case-specific labels, evidence and rationales; one bracketed key each; hard MRI and labs to tissue, hard MRI to CSF; stop rule MRI, labs, tissue; "No cardiac question in this presentation"; concern cleared (now grade 4), difficulty rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

A 31-year-old man with a VP shunt, long-standing epilepsy on levetiracetam and six months of prednisone for presumed neurosarcoidosis, now progressing, with multifocal solid and cystic lesions, basal meningeal disease and spinal leptomeningeal nodules. The outside biopsy, taken two weeks into steroids and non-diagnostic, is now in the history rather than in the tissue report. The MRI states that there is no shift or herniation and the fourth ventricle is patent, and it explains the fixed left pupil and the right facial numbness by oculomotor and trigeminal involvement. Work-up: contrast MRI (required), perfusion and spectroscopy to target the biopsy, staging CT (optional), labs with a coagulation panel (required), performance status (KPS 50, ECOG 3), contrast MRI of the whole spine and, after imaging, CSF cytology and flow cytometry (both recommended; GFAP-positive tumour cells, no clonal lymphocytes), then tissue by stereotactic biopsy or debulking of the right temporal lesion (required; IDH1 IHC and sequencing, ATRX, 1p/19q, CDKN2A/B, MGMT). CDKN2A/B is homozygously deleted, so the diagnosis is astrocytoma, IDH-mutant, CNS WHO grade 4. Lymphoma is in the differential. The steroid must now says not to add dexamethasone and not to stop prednisone abruptly; levetiracetam is continued; the treatment must manages the tumour like glioblastoma, individualised for neuraxis spread and KPS 50.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Label change (ruling 3, plan 5.3): accepted[0] "Diffuse astrocytoma, IDH-mutant, WHO grade 2 with leptomeningeal dissemination" to "Astrocytoma, IDH-mutant, CNS WHO grade 4 with leptomeningeal dissemination". The synonym set needs re-expanding from it, for example "astrocytoma IDH-mutant grade 4".
- Synonyms (plan 5.2): "glioblastoma", "GBM" and "astrocytoma grade 4" are appended to this IDH-mutant case and accept the wrong entity; give IDH-mutant astrocytoma its own synonym set.
- `[AIOM_brain]` used in the tissue criterion (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

1. Grade (plan open question 3): applied the plan's choice, CDKN2A/B homozygous deletion and therefore grade 4. The alternative is grade 2 with the contradicting features removed.
2. In-round decisions you may want to check: (a) to make the reviewer's safe lumbar puncture consistent, the MRI now says the fourth ventricle is abutted but not effaced (it was "mild compression"), and the basal meningeal finding now includes left oculomotor and right trigeminal nerve enhancement, which explains the fixed pupil without herniation; (b) KPS 50, ECOG 3 is derived from the walker, the falls and the confusion, with help for bathing and dressing written into the performance-status output.

## Verification

Adversarial verifier, 24 Oct 2026. All three note ids are in the table and applied: CDKN2A/B homozygous deletion in both tissue follow-ups with "Astrocytoma, IDH-mutant, CNS WHO grade 4" and no "Grade 2 (with features ...)", original-biopsy or cyst-fluid rows; analyze_csf out of the harm list, recommended `action-csf-cytology` with a hard MRI-first constraint and a CSF report consistent with it (glucose ratio 0.32 against serum 148 mg/dL); lymphoma in the differential and the steroid must recast (no dexamethasone, no abrupt prednisone withdrawal, consistent with prohibitions 1 and 2). Checked that the MRI now supports a safe LP (no shift, fourth ventricle patent, no herniation, functioning shunt), that the oculomotor and trigeminal enhancement explains the pupil and the V2/V3 deficit, the spine MRI (no block), the coagulation panel, KPS 50 / ECOG 3 against the individualised treatment must, continued levetiracetam, and the label change and wrong GBM synonyms under CENTRAL. Found and fixed:
- `metadata.difficulty_rationale` said "six recommended" while listing and having five: corrected to "five".
Re-ran perfect-agent (pass), `case_io.py check` (no failure names the case) and the case guards (pass).

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `metadata.condition_name`: "astrocytoma with protoplasmic features" (retired, and contradicting the grade 4 label) now "astrocytoma, IDH-mutant, CNS WHO grade 4, with leptomeningeal dissemination".
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Obtain pre-operative labs (CBC, BMP, coagulation, type & screen) before craniotomy/biopsy' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['glioblastoma', 'GBM', 'astrocytoma grade 4']; added ['astrocytoma idh mutant grade 4'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
