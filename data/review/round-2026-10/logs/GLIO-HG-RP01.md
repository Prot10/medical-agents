# GLIO-HG-RP01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 786de7f4-26ad-4971-8a8b-c41d24a9a8c9 | FIXED | One thyroglobulin story: `patient.clinical_history.past_medical_history[0]` and the HPI now give a right hemithyroidectomy alone (the "radioactive iodine ablation" was also inconsistent with the intact left lobe on CT and ultrasound) and a thyroglobulin stable at 2 to 4 ng/mL with negative antibodies, 3.0 ng/mL six months ago. Panel `initial_tool_outputs.labs.panels["Tumor markers"][0]`: value 3.2 kept, reference range "1.4-29.2 (intact gland); after lobectomy, interpret against the patient's own trend", `is_abnormal` false; summary and interpretation recomputed. `red_herrings[0].correct_interpretation` uses the residual-tissue argument (up to 5 to 10 ng/mL) moved from the deleted literature output; "undetectable" removed everywhere. |
| 7dc06c7a-bed1-4873-968e-6e39001a8421 | FIXED | Treat class: must 3 (levetiracetam for the documented focal motor seizure of the left hand with retained awareness, treatment not prophylaxis, avoid enzyme inducers); key evidence item 2. EEG impression rewritten in ACNS form with the equivocal C4/P4 sharp transients listed. |
| 6538e4db-02db-4c16-8d88-e1552f5c5622 | FIXED | `action-1-analyze-brain-mri.expected_evidence` written from this MRI (patchy irregular marginal enhancement, no ring or definite necrosis, patchy peripheral restriction, extensive non-enhancing FLAIR, 3 mm shift); the old pearl (now `key_clinical_evidence[2]`) carries the same correct description. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | `initial_tool_outputs.tissue_diagnosis` | Integrated diagnosis served upfront (C2). | FIXED: two follow-ups (`resection` with extent row, `stereotactic_biopsy`); meta-text removed; GFAP moved to the Histology row; site "as targeted on the contrast-enhancing rim" replaced by a real site. |
| C | major | `action-9-obtain-tissue-diagnosis` | Biopsy only (C3); assay list with 1p/19q in an IDH-wildtype case and no ATRX (C4). | FIXED: group A, `resection` then `stereotactic_biopsy`; minimum `IDH1_IHC, ATRX_IHC, MGMT_methylation` (age 68, MVP and necrosis); ATRX row added (retained); thyroglobulin IHC row added beside TTF-1 and PAX8 (not orderable: CENTRAL), and must 1 asks pathology for them. |
| C | major | `action-3-search-medical-literature`, `followup_outputs[4]` (literature), stop rule | Literature as a required step (C1). | FIXED: deleted; the residual-tissue fact moved to the red herring. |
| C | major | `followup_outputs[6]` (`interpret_labs` thyroid ultrasound) | A neck ultrasound filed as a lab panel (C14). | FIXED: deleted; must 7 (thyroid surveillance with neck ultrasound and thyroglobulin trend). |
| C | major | `followup_outputs[3]` | fMRI filed as `perfusion_MRI` (C6). | FIXED: retagged `functional_MRI` with language laterality (0.72, bilateral, right STG co-activation at the anterior margin), motor area 15 mm, Heschl gyrus; new recommended `action-fmri-functional-mapping`, soft constraint to tissue. No DTI: the MRI reports no tract involvement (rule applied from the MRI). |
| C | major | new `action-performance-status`, `followup_outputs[3]` | Performance status absent; the only value is the pre-illness WHO 0 (C7). | FIXED: required (age 68), in the stop rule; KPS 60, ECOG 2 (needs supervision of medications and cooking); social history labelled "Before the current illness". |
| C | major | `assessment.required_recommendations` | Template Stupp must regardless of KPS; no aspirin plan; biopsy and resection interchangeable; dexamethasone not canonical. | FIXED: must 8 per EANO for KPS under 70 (40 Gy/15 with temozolomide or temozolomide alone, MGMT methylated; 60 Gy/30 if KPS recovers to 70); must 5 stop aspirin 7 days before craniotomy; must 1 group A with fMRI; must 4 canonical; must 6 home supervision and no driving. |
| C | minor | `assessment.prohibited_recommendations` | No guard against treating the lesion as thyroid metastasis without histology. | FIXED: prohibition 4. |
| C | minor | `action-8-order-body-imaging` | Optional; plan makes it recommended because of the prior carcinoma. | FIXED: recommended; label, evidence, rationale; output region "neck chest abdomen pelvis" (the report covers the thyroid bed), numbered impression. |
| C | major | `followup_outputs[5]` (DDI) | Temozolomide check; penicillin allergy conflated with sulfonamide tolerance; alternatives lomustine, bevacizumab, TTFields. | FIXED: rewritten for levetiracetam and dexamethasone with her medicines (calcium-levothyroxine spacing, dexamethasone-aspirin GI risk, osteopenia, aspirin before surgery); penicillin allergy stated correctly (no sulfonamide cross-reactivity; relevant to perioperative antibiotic choice). New optional criterion `action-check-drug-interactions`, last. |
| D | minor | `initial_tool_outputs.mri.impression`, `.additional_observations[3]` | "lower-grade glioma (WHO grade 2-3)", "anaplastic component" (retired terms); "No hydrocephalus beyond mild temporal horn effacement". | FIXED: numbered impression, imaging differential without retired names; "No hydrocephalus". |
| D | minor | `initial_tool_outputs.eeg.impression` | Clinical essay ("age-related neurodegenerative process ... structural lesion"). | FIXED: ACNS list (diffuse slowing, right temporal slowing T4/T6, equivocal C4/P4 sharp transients, no seizures). |
| D | minor | `followup_outputs[0]`, `[1]` | Perfusion signal with "above what would be expected for low-grade glioma" and "suggestive of tumor infiltration"; MRS impression "See findings above". | FIXED: values kept, interpretive clauses removed, numbered impressions. |
| C | major | `ground_truth.differential` | Metastasis twice; lymphoma and demyelination keyed on "ring enhancement with necrosis" this MRI lacks; the lower-grade glioma raised by the MRI absent. | FIXED: one metastasis entry (low), IDH-mutant astrocytoma grade 2 or 3 (very low, excluded by sequencing), lymphoma and abscess very low with this case's discriminators. |
| C | minor | `avoided_actions` | Generic LP and cardiac rationales. | FIXED: canonical C17 (3 mm shift, temporal horn effacement); echo and Holter rationale adds that the exertional symptoms were evaluated four months ago. |
| B | minor | `initial_tool_outputs.labs` | `type_and_screen` template significance. | FIXED: null. Values checked (anion gap 14, MCHC 33.3, PT/INR concordant). |
| B | minor | `action-2`, `action-6`, `action-7`, citations, sequence, stop rule, metadata | Template evidence; duplicate bare keys; single soft constraint; literature in the stop rule; metadata "5 required tools", "undetectable". | FIXED: case-specific evidence; one bracketed key each; hard MRI and labs to tissue, soft fMRI to tissue; stop rule MRI, labs, performance status, tissue; metadata rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

A 68-year-old woman with a right temporal glioblastoma, IDH-wildtype, a focal motor seizure, and a prior follicular thyroid carcinoma as the metastasis red herring. The thyroid history is now coherent: hemithyroidectomy without radioiodine and a stable thyroglobulin of 2 to 4 ng/mL (3.2 now, not flagged), which residual thyroid tissue explains. Work-up: contrast MRI (required), perfusion and spectroscopy, staging CT of neck, chest, abdomen and pelvis (recommended), labs (required), performance status (required: KPS 60, ECOG 2), functional MRI for language (bilateral representation at the anterior margin), then tissue by maximal safe resection or stereotactic biopsy (required; IDH1 IHC, ATRX, MGMT; TTF-1, PAX8 and thyroglobulin immunostains negative), drug check optional and last. Musts: resection with fMRI and mapping plus metastasis immunostains; levetiracetam for the documented seizure; dexamethasone; stop aspirin before surgery; home supervision and no driving; continued thyroid surveillance; and MDT referral with the regimen chosen by the current KPS (hypofractionated under 70, standard if it recovers). The literature step, the lab-filed thyroid ultrasound and the mislabelled perfusion step are gone; the tissue result is no longer upfront.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Vocabulary: PAX8, TTF-1 and thyroglobulin IHC are not orderable `molecular_assays` (plan 5.4); they are reported as findings rows and requested in must 1.
- `[AIOM_brain]` used in the tissue criterion (plan 5.1).
- Synonyms: "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan 5.2); accepted[0] "WHO grade 4" to "CNS WHO grade 4" if the synonym tool allows.

## Open questions for Andrea (judgment calls you could not settle)

None. Decided in-round: KPS 60 (not 70), because she needs her daughter to supervise medications and cooking; the regimen must covers recovery to KPS 70 after surgery. No DTI criterion, because the MRI reports no tract involvement; the mild left hemiparesis alone was not used to invent one.

## Verification

Adversarial verifier, 24 Oct 2026. All three note ids are in the table and applied: one thyroglobulin story (history 2 to 4 ng/mL, 3.0 six months ago; panel 3.2 not flagged; red herring with the residual-tissue argument; "undetectable" nowhere), the levetiracetam treat must for the left-hand focal motor seizure, and an action-1 expected evidence that matches this MRI (patchy marginal enhancement, no ring or necrosis). Checked the removal of radioiodine from the history against the intact left lobe on CT, laterality (right temporal lesion, left-sided signs, right centroparietal EEG transients), the 3 mm shift against the LP harm entry, labs flags, KPS 60 / ECOG 2 against the hypofractionated must and the required performance-status criterion in the stop rule, penicillin allergy against the drug check, the TTF-1, PAX8 and thyroglobulin rows (findings only, CENTRAL), and the decision not to add DTI (no tract involvement reported, visual fields full): defensible. Found and fixed:
- `initial_tool_outputs.mri.impression` ended with "Tissue diagnosis recommended." (management text, plan C9): removed.
- `metadata.difficulty_rationale` said "five recommended" while listing and having four (perfusion, spectroscopy, staging CT, functional MRI): corrected to "four".
Re-ran perfect-agent (pass), `case_io.py check` (no failure names the case) and the case guards (pass).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must rewritten: 'Obtain pre-operative labs (CBC, BMP, coagulation, type & screen) before craniotomy/biopsy, and stop aspirin (primary prevention after a normal cardiology work-up) about 7 days before craniotomy.' -> 'Stop aspirin (primary prevention after a normal cardiology work-up) about 7 days before craniotomy.' (Q9: the duplicated diagnostic part dropped, the management part kept)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Central vocabulary wired (24 Oct 2026)

Terms added by commit e19131d6 (batch-2 review vocabulary), wired as the plan and this log intended. The earlier CENTRAL vocabulary request in this log is resolved by them.

- `action-9-obtain-tissue-diagnosis`: `TTF1_IHC`, `PAX8_IHC` and `thyroglobulin_IHC` added to the minimum assay list of both alternatives (metastasis exclusion after follicular thyroid carcinoma, as for the melanoma markers in RP04); label and rationale name them; expected evidence already stated them negative. Tissue reports: the existing TTF-1, PAX8 and thyroglobulin findings rows (all negative) are now also in `molecular_findings`.
- Must 1: the clause "and ask pathology to add TTF-1, PAX8 and thyroglobulin immunostains..." removed, since the stains are now ordered by the criterion (plan Q9).

Checks after the change: `perfect_agent.py GLIO-HG-RP01 -v` ok, `case_io.py check` (schema and synonym guard OK, no failure names the case), `test_case_guards.py -k "GLIO-HG- or ALZ-EARLY-"` 120 passed.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-check-drug-interactions` rationale: "Optional: no interaction changes the diagnostic plan." -> "No interaction changes the diagnostic plan."

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.alternatives: was [CBC, BMP, coagulation, type_and_screen]; now [CBC, BMP, coagulation, type_and_screen, anti_thyroglobulin] | [CBC, BMP, coagulation, type_and_screen].
- Decision: serve: new first alternative (old order kept as an alternative). A must, the differential, the key evidence and a red herring read the stable thyroglobulin with negative antibodies (prior thyroid carcinoma against a metastasis); no term orders thyroglobulin itself (CENTRAL), and anti_thyroglobulin returns the tumour-marker panel that holds both rows.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
