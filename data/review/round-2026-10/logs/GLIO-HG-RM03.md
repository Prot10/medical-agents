# GLIO-HG-RM03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 55929ced-466c-4789-8216-127583cf9d1f | FIXED | `ground_truth.action_criteria[action-10-obtain-tissue-diagnosis].alternatives[*].required_arguments.molecular_assays` is now `IDH1_IHC, IDH1_IDH2_sequencing, ATRX_IHC, H3K27_status, MGMT_methylation` (C4, midline because of vermian involvement, under 55). The tissue reports (`followup_outputs[4]`, `[5]`) carry one row per assay: IDH1 R132H negative, no IDH1/IDH2 mutation on sequencing, ATRX retained, "H3 K27M not detected; H3K27me3 retained", MGMT methylated (TERT C228T, EGFR amplified and 1p/19q intact kept). The literature step the note quotes is deleted (C1). Label, rationale and expected evidence name the assays; key evidence item 5 rewritten. |
| 1a5bdcb8-bd18-4cfe-ad42-ea1fbe1e673e | FIXED (seizure part); ALREADY-FIXED (empty tool field) | Levetiracetam must deleted; no-seizure prohibition added to `assessment.prohibited_recommendations[3]`; the seizure pearl in `key_clinical_evidence` replaced by "No seizure has occurred, so antiseizure prophylaxis is not indicated". The empty-tool required actions 4 and 5 were v1 null-tool consult steps removed by the v2 migration; the referral they stood for is must 1 (neurosurgery) and must 7 (neuro-oncology MDT). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | `initial_tool_outputs.tissue_diagnosis` | Integrated diagnosis served in the initial work-up (C2). | FIXED: initial set to null; two follow-ups `obtain_tissue_diagnosis` with `procedure` `resection` (`followup_outputs[4]`, with an extent-of-resection row) and `stereotactic_biopsy` (`[5]`), identical integrated diagnosis and molecular results; template meta-text removed from the impression ("Integrated diagnosis: Glioblastoma, IDH-wildtype, CNS WHO grade 4. MGMT promoter methylated."); histology moved out of `molecular_findings` into `histological_diagnosis` and one `Histology` row. |
| C | major | `action-10` alternatives, label, rationale, must 1 | Stereotactic biopsy as the only procedure for a resectable cerebellar mass; must made biopsy and resection interchangeable (C3). | FIXED: group A, `resection` then `stereotactic_biopsy`; canonical label and rationale (adds that resection relieves the fourth-ventricle compression); must 1 canonical group A surgery must. |
| C | major | `assessment.required_recommendations` | No must on the obstructive hydrocephalus with transependymal flow and papilledema. | FIXED: must 2 (early posterior fossa resection, EVD or ETV if worsening, close observation). |
| C | major | `followup_outputs` (literature x2), `action-3-search-medical-literature`, stop rule | Literature as a required clinical step (C1). | FIXED: criterion, both follow-ups and the stop-rule id deleted. |
| C | major | `followup_outputs[3]` (old) | fMRI/DTI report filed as `perfusion_MRI` in a cerebellar lesion with no eloquent supratentorial structure (C6). | FIXED: deleted. |
| C | minor | new `action-performance-status`, `followup_outputs[3]` | Performance status absent (C7). | FIXED: recommended criterion (age 21) and output: KPS 70, ECOG 2 from the exam and HPI (walks unaided with ataxic gait, self-caring, unable to study for three weeks). |
| C | major | `assessment.required_recommendations` | Template Stupp must; no attention to the combined oral contraceptive (estrogen VTE risk with malignancy and surgery; temozolomide teratogenic) or fertility in a 21-year-old woman. | FIXED: must 7 entity-specific (GBM IDH-wildtype, age 70 or under, KPS 70 or more: 60 Gy/30 fractions with temozolomide); must 6 on contraception and fertility preservation counselling. |
| C | minor | must 4 | Dexamethasone must not canonical (no taper, glucose, gastric protection). | FIXED: canonical C11 text. |
| C | major | `followup_outputs[6]` (DDI) | Output was a temozolomide check (wrong `proposed`) with a false claim that temozolomide reduces contraceptive efficacy "due to enzyme interactions" (it is not an enzyme inducer) and dapsone offered without its sulfonamide cross-sensitivity caveat. | FIXED: rewritten for dexamethasone plus her medicines; estrogen VTE warning, sulfonamide allergy (avoid TMP-SMX; dapsone cross-sensitivity; atovaquone or inhaled pentamidine sulfonamide-free); no levetiracetam (no seizure). Criterion stays optional, last; label, evidence and rationale rewritten; guard passes. |
| B | minor | `initial_tool_outputs.eeg.findings[1]`, `.impression` | Focal right posterior temporal-occipital slowing in a patient whose MRI shows no supratentorial lesion (a finding no lesion explains). | FIXED: focal finding deleted; impression rewritten in ACNS form (bilateral posterior intermittent rhythmic delta, mild generalized slowing, no epileptiform discharges). |
| C | minor | `ground_truth.avoided_actions` | No EEG entry although there is no seizure or spell. | FIXED: `avoid-waste-3-analyze-eeg` with the canonical C5 rationale. |
| C | minor | `avoid-harm-1-analyze-csf.rationale`, prohibition 1 | Generic LP rationale. | FIXED: canonical C17 harm rationale naming fourth-ventricle compression, early obstructive hydrocephalus and papilledema. |
| C | minor | `avoid-waste-1`, `avoid-waste-2` | Waste rationales generic, cited NCCN. | FIXED: "No cardiac question in this presentation", `[EANO_2021]`. |
| C | minor | `initial_tool_outputs.labs` | No pregnancy test before CT with contrast, surgery and later temozolomide in a woman of 21 on contraception; `type_and_screen` significance template; summary with interpretive dashes. | FIXED: serum beta-hCG row added (negative); `type_and_screen.clinical_significance` null; summary and interpretation recomputed (anion gap 13, MCHC 32.8 checked). |
| C | minor | `action-1`, `action-2`, `action-6`, `action-7` expected evidence and rationales | Template text (C9); rationales copied from labels; MRS evidence about post-treatment change. | FIXED: written from this case's MRI (3.2 x 4.1 x 3.5 cm ring-enhancing necrotic haemorrhagic mass, 1.8 cm vermian lesion, peripheral restriction, fourth-ventricle compression, early hydrocephalus), labs, rCBV 3.8 and Cho/NAA 8.0. |
| A | minor | all `citations` | Duplicate bare keys, `WHO_CNS5`, `[Stupp_2005]` on the MRI criterion. | FIXED: one bracketed key each; MRI cites `[EANO_2021]`; tissue `[WHO_2021]`, `[EANO_2021]`, `[AIOM_brain]`. |
| B | minor | `sequence_constraints`, `stop_rule` | Single soft MRI-to-tissue constraint. | FIXED: hard MRI-to-tissue and hard labs-to-tissue (plan 3.3); stop rule MRI, labs, tissue. |
| C | major | `ground_truth.differential` | Metastasis twice (moderate and "solitary" low, while the MRI shows two lesions); ependymoma and medulloblastoma raised by the MRI but absent; high-grade astrocytoma with piloid features (a cerebellar young-adult entity) absent; likelihoods not at the assessment-time view. | FIXED: merged metastasis (low); HGAP added (low, ATRX retained and TERT/EGFR profile against); hemangioblastoma, ependymoma or medulloblastoma, PCNSL, abscess very low with discriminators from the case; tumefactive demyelination removed (no feature raises it). |
| B | minor | `ground_truth.red_herrings` | Empty although the metadata names the breast and ovarian family history as the red herring. | FIXED: one red herring for the family history. |
| C | minor | `patient.neurological_exam.gait` | "Romberg test positive with eyes open and closed" (cerebellar unsteadiness with eyes open is not a positive Romberg; proprioception is intact). | FIXED: unsteady with feet together eyes open without worsening on eye closure (Romberg negative). |
| B | minor | `followup_outputs[2]` (CT CAP) | Duplicated observation rows, em dashes, "no further workup required in this clinical context". | FIXED: three findings, numbered impression, no clinical clause. |
| D | minor | `followup_outputs[0]`, `[1]` impressions | Unnumbered prose impressions. | FIXED: numbered, same values. |
| E | minor | `ground_truth.key_clinical_evidence`, `metadata.difficulty_rationale` | Pearls generic or wrong for this case (seizure mandates AED; biopsy or resection; "5 required tools, no red herrings"). | FIXED: rewritten from this case. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is a 21-year-old woman with a right cerebellar and vermian glioblastoma, IDH-wildtype, with fourth-ventricle compression and early hydrocephalus, and no seizure. The work-up is now: contrast MRI (required), perfusion and spectroscopy (recommended, for sampling targets), staging CT (optional), pre-operative labs (required, now including a negative beta-hCG), performance status (recommended, KPS 70, ECOG 2), and tissue by maximal safe resection or, if not feasible, stereotactic biopsy (required), with a minimum molecular panel of IDH1 R132H IHC, IDH1/IDH2 sequencing, ATRX, H3 K27 status and MGMT; the drug check is optional and last. Literature and the mislabelled fMRI step are gone, and the tissue result is no longer in the initial work-up. MRI and labs must precede tissue (hard). Musts: resection-first neurosurgical referral, urgent management of the hydrocephalus, dexamethasone at the lowest effective dose, stopping the estrogen-containing pill with non-estrogen contraception and fertility counselling, and MDT referral for 60 Gy with temozolomide. Prohibitions: LP (fourth-ventricle compression, hydrocephalus, papilledema), therapy before tissue, anticoagulation without indication, and antiseizure prophylaxis. The differential now has metastasis and high-grade astrocytoma with piloid features low, and hemangioblastoma, ependymoma or medulloblastoma, lymphoma and abscess very low. A stray right temporo-occipital EEG slowing (no supratentorial lesion) was removed, and the Romberg wording corrected.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[AIOM_brain]` used in the tissue criterion citations (plan 5.1, pack allow-list).
- `accepted[0]` "Glioblastoma, IDH-wildtype, WHO grade 4 (cerebellar)": normalise "WHO grade" to "CNS WHO grade" if the synonym tool allows (plan 5.3). The synonym "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan 5.2).
- DNA methylation profiling is not orderable; it would be the definitive discriminator against high-grade astrocytoma with piloid features and diffuse paediatric-type high-grade glioma in a young adult. Not needed here (TERT and EGFR give the adult glioblastoma profile), noted for the vocabulary.

## Open questions for Andrea (judgment calls you could not settle)

None. Decided in-round: the diagnostic musts "Obtain MRI ..." and "Obtain pre-operative labs ..." were kept (they are correct and duplicate the required criteria); the CA-125 row in the labs was kept as stored data (normal, not interpreted).

## Verification

Adversarial verifier, 24 Oct 2026. Checked the log against the diff and the final case: both note ids are in the table and both are applied (tissue assays IDH1 IHC, IDH1/IDH2 sequencing, ATRX, H3 K27 status, MGMT in both alternatives, with one findings row and one molecular entry per assay in both tissue follow-ups and identical integrated diagnosis; no levetiracetam anywhere, no-seizure prohibition present, EEG waste entry with the canonical rationale). Cross-checked laterality (right cerebellar and vermian on exam, MRI, perfusion, MRS, tissue sites), hydrocephalus and papilledema against the LP harm entry and prohibition, labs arithmetic and flags (anion gap 13, MCHC 32.8, every `is_abnormal` agrees with its range), beta-hCG and the estrogen and teratogenicity musts, sulfonamide allergy against the drug check, KPS 70 / ECOG 2 against the threshold in the treatment must, stop rule and hard constraints, differential against the final evidence, and the absence of literature, tissue upfront, "Tissue diagnosis recommended" and engineering text. Perfect-agent, `case_io.py check` and the case guards pass. Found nothing that needed a change; no edit made.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `fallback_tool_outputs.csf`: opening pressure 16 changed to 28 cm H2O, interpretation "Elevated opening pressure. Normal cell count, protein and glucose."; a normal pressure contradicts the documented papilloedema (same class as S02, S03, S04, S06).
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (cerebellar)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (cerebellar)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Obtain pre-operative labs (CBC, BMP, coagulation, type & screen) before craniotomy/biopsy' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Minor non-specific finding.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['glioma who grade 4', 'grade 4 glioma', 'astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Central vocabulary wired (24 Oct 2026)

Terms added by commit e19131d6 (batch-2 review vocabulary), wired as the plan and this log intended. The earlier CENTRAL vocabulary request in this log is resolved by them.

- New recommended criterion `action-dna-methylation-profiling` (`obtain_tissue_diagnosis` with `DNA_methylation_profiling`, resection or stereotactic biopsy), after the tissue criterion. Reason: at 21, a cerebellar IDH- and H3-wildtype high-grade glioma may be a high-grade astrocytoma with piloid features or a diffuse paediatric-type high-grade glioma, H3- and IDH-wildtype, both defined by a methylation profile (WHO CNS5); recommended, not required, because TERT and EGFR already give the adult glioblastoma profile (the earlier log's judgment). Both tissue reports carry the result: methylation class glioblastoma, IDH-wildtype, subclass RTK II (calibrated score 0.95), no match to either entity, CNV EGFR amplification and +7/-10. Citations `[WHO_2021]`, `[Capper_2018]`.
- Differential: HGAP low to very_low with the methylation result; new very_low entry "Diffuse paediatric-type high-grade glioma, H3-wildtype and IDH-wildtype" (the mimic this log raised).
- Perfect-agent note: the methylation criterion is answered by the same stored tissue report as the tissue criterion (one specimen, one report).
- CENTRAL: `[Capper_2018]` for the pack allow-list (see RM02).

Checks after the change: `perfect_agent.py GLIO-HG-RM03 -v` ok, `case_io.py check` (schema and synonym guard OK, no failure names the case), `test_case_guards.py -k "GLIO-HG- or ALZ-EARLY-"` 120 passed.

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

- criterion `action-9-check-drug-interactions` rationale: "Optional: no interaction changes the immediate diagnostic plan, but the contraceptive and the allergy matter for later treatment." -> "No interaction changes the immediate diagnostic plan, but the contraceptive and the allergy matter for later treatment."
