# GLIO-HG-P05
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 9046c896-9a52-499d-8925-d7a4c4d6cecf | FIXED | No-seizure class (plan C5): levetiracetam removed from the drug-interaction follow-up (`proposed`, the levetiracetam interaction rows, the "preferred AED" alternative) and from `action-8-check-drug-interactions` label and expected evidence; canonical prohibition added (`prohibited_recommendations[4]`). The interaction output now checks dexamethasone against her actual medicines (combined oral contraceptive, ferrous sulfate) and the sulfonamide allergy. |
| bc69f5ec-4a51-499f-8189-b47743c63ccd | FIXED | Both red herrings rewritten: perfusion (rCBV 2.8) and spectroscopy (Cho/NAA 4.1) "identify the posterolateral component as the biopsy target; the entity and grade come from H3 K27 status on tissue". `key_clinical_evidence[2]` ("pre-biopsy evidence against a low-grade process") replaced by "they do not grade the tumour". The perfusion and MRS reports no longer quote the 1.75 and 2.0 grading thresholds; the perfusion and MRS criteria are relabelled as biopsy targeting. |
| e8cfa028-9108-4db6-9954-ccb5f4d2a30f | FIXED | `ground_truth.differential`: the low-grade entry (renamed "Astrocytoma, IDH-mutant, CNS WHO grade 2", plan C12 retired names) high to low; thalamic infarction moderate to very low (3-week progression, no restricted diffusion); tumefactive demyelination moderate to low (plan: "MS stays low"); lymphoma and metastasis very low. Each entry states what supports and excludes it. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.diagnosis.accepted[0]`, tissue report | "Diffuse midline glioma, H3 K27M-altered" is not a WHO CNS5 name (CNS5: "H3 K27-altered"; WHO 2016: "H3 K27M-mutant"). | FIXED (ruling 3, non-existent name): accepted[0] "Diffuse midline glioma, H3 K27-altered, CNS WHO grade 4 (thalamic)"; integrated diagnosis likewise. Scoring is unchanged in practice (the synonym "diffuse midline glioma" still matches). CENTRAL. |
| A | major | `action-10-obtain-tissue-diagnosis` | Assays MGMT, 1p/19q, ATRX, TERT, H3K27, without IDH (plan C4). | FIXED: `IDH1_IHC`, `IDH1_IDH2_sequencing` (age 30), `ATRX_IHC`, `H3K27_status`, stereotactic biopsy only (group C, deep thalamic). MGMT and 1p/19q are not required: MGMT does not select treatment in diffuse midline glioma and 1p/19q is irrelevant in an IDH-wildtype tumour (the report keeps both results). Report rows for each assay; "WHO 2021 integrated diagnosis" removed as a molecular finding (C2). |
| B | major | `initial_tool_outputs.tissue_diagnosis` | Tissue in the initial work-up; template meta-text; site "thalamic" (C2). | FIXED: `request_stereotactic_biopsy` follow-up; site "Right thalamus, posterolateral enhancing component"; impression "Integrated diagnosis: ...". Histology row added. |
| A | major | `action-3-search-medical-literature`, literature follow-up | Required literature step in the stop rule (ruling 5). | FIXED: deleted with its follow-up and stop-rule id; the Aboian and Vitanza citation gap in metadata cleared. |
| A | minor | `action-9-order-ct-scan`, CT follow-up | Optional CT duplicating the MRI (plan: delete). | FIXED: criterion and follow-up deleted; the case fallback CT stays for an agent that orders one. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | MCH 24.1 with MCV 76.8 gives MCHC 31.4, while Hb/Hct gives 33.3. | FIXED: MCH 25.6 pg (still low); MCHC 33.3 both ways. Summary dashes removed. |
| C | major | labs, musts | A 30-year-old woman on a combined oral contraceptive facing biopsy, steroids and radiotherapy: no pregnancy test, and the estrogen VTE risk unaddressed. | FIXED: serum beta-hCG negative added to the labs; must to stop the combined pill and offer a copper IUD or progestogen-only method and confirm a negative pregnancy test; the interaction output warns about estrogen and thrombosis. |
| C | minor | DDI follow-up | Claimed dexamethasone reduces contraceptive efficacy via CYP3A4 (not established for dexamethasone at these doses); proposed dapsone in a sulfonamide-allergic patient without the cross-sensitivity caveat. | FIXED: interaction stated as minor without an established efficacy loss; dapsone cross-sensitivity noted; atovaquone kept. |
| D | minor | MRI report | Teaching parenthetical in ADC; impression line "does not fulfill criteria for high-grade neoplasm by enhancement pattern alone". | FIXED: ADC factual; numbered impression with a hedged imaging differential. |
| C | major | `assessment.required_recommendations` | Stupp-free but template musts: consults as a must, steroid template, no hydrocephalus watch. | FIXED: group C biopsy must (targeting the posterolateral component), canonical dexamethasone must, hydrocephalus watch given third-ventricle compression, contraception and pregnancy must, PJP prophylaxis with atovaquone, entity-specific must (focal radiotherapy and trial; temozolomide benefit not established; EANO 2021); prognosis must kept. |
| C | minor | `assessment.prohibited_recommendations` | Dashes; "H3 K27M testing is mandatory" wording. | FIXED: reworded to H3 K27 status. |
| A | minor | criteria | No performance status (C7). | FIXED: recommended, follow-up KPS 80, ECOG 1. |
| A | minor | `avoided_actions` | Template waste rationales; LP rationale without the case findings. Amyloid PET and DaTscan waste entries are modality-scoped and do not hit perfusion or MRS (checked). | FIXED: canonical EEG and cardiac rationales; LP harm rationale names third-ventricle compression, early ventricular enlargement and blurred discs. |
| A | minor | citations, constraints, stop rule | Duplicate keys, `WHO_CNS5`, Stupp on MRI; one soft template constraint. | FIXED: hard MRI and labs to tissue; stop rule MRI, labs, tissue. |

## Changes, in one paragraph a physician can read before re-reviewing

A 30-year-old woman with three weeks of morning headache, left hemiparesis and hemisensory loss, no seizures, a prior visual episode and a combined oral contraceptive. Pathway: contrast MRI (infiltrative right thalamic mass, patchy enhancement of the posterolateral part, no restricted diffusion, crossing the massa intermedia, mild third-ventricle compression), perfusion and spectroscopy as biopsy targeting, pre-operative labs (iron deficiency, negative beta-hCG), performance status (KPS 80), then stereotactic biopsy: diffuse midline glioma, H3 K27-altered, CNS WHO grade 4 (H3 K27M with H3K27me3 loss, IDH-wildtype on IHC and sequencing, ATRX retained). Literature, CT and the levetiracetam proposal are gone; prophylaxis is prohibited. Musts: biopsy not resection, dexamethasone, hydrocephalus watch, stop the estrogen contraceptive with a pregnancy test, atovaquone if PJP prophylaxis is needed, focal radiotherapy and trial referral after the diagnosis.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Label change (ruling 3): accepted[0] now "Diffuse midline glioma, H3 K27-altered, CNS WHO grade 4 (thalamic)".
- Synonyms: the C71.9 set appended here ("glioblastoma", "GBM", "astrocytoma grade 4", ...) is wrong for diffuse midline glioma (plan 5.2); the C71.0 set "h3 k27m altered glioma" should become or add "h3 k27 altered glioma". Removing C71.9 from this case's `icd_codes` would stop the glioblastoma synonyms being appended; I left `icd_codes` untouched.

## Open questions for Andrea (judgment calls you could not settle)

- None needing your information. Decision recorded: MGMT is not a required assay for diffuse midline glioma (the plan's midline row adds H3 K27 and IDH sequencing to the glioblastoma list, which includes MGMT); the report still states MGMT unmethylated.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the notes (9046c896, bc69f5ec, e8cfa028) and the whole final case.
- Notes: all three are in the table and fixed. Levetiracetam is absent from the DDI output and its criterion, and the prophylaxis prohibition is present. The red herrings and key evidence describe perfusion and MRS as biopsy targeting, not grading. The differential has low-grade astrocytoma at low, infarction at very low and demyelination at low.
- The label change to "Diffuse midline glioma, H3 K27-altered, CNS WHO grade 4 (thalamic)" is a correct ruling-3 fix: "H3 K27M-altered" is not a WHO CNS5 name. It is listed under CENTRAL.
- Cross-field checks: the sulfonamide allergy against TMP-SMX and dapsone in the DDI output and the atovaquone must; the combined pill against the beta-hCG and the contraception must; MCHC 33.3 by both Hb/Hct and MCH/MCV; the LP harm rationale against the third-ventricle compression and the blurred discs. Laterality is consistent (right thalamus, left hemiparesis and hemisensory loss). The amyloid PET and DaTscan waste entries are modality-scoped and do not penalise the recommended perfusion and MRS.
- Found and fixed: the MRI impression ended "Tissue diagnosis is recommended." and `recommended_actions` held "Tissue diagnosis recommended to characterize the infiltrative thalamic mass." Both are management text in a report (C9) and are removed. The hedged imaging differential stays.
- After the fix: `perfect_agent.py` passes, `case_io.py check` reports no failure naming the case, and `test_case_guards` passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `fallback_tool_outputs.literature_search` set to null (plan C1, uniform with the other 26 cases).
- `fallback_tool_outputs.eeg`: the normal "no focal slowing" study replaced by focal polymorphic slowing over the lesion (intermittent right hemispheric slowing at C4, P4), no epileptiform discharges, in the RS06 format; a normal EEG contradicts a hemispheric mass with oedema (same class as M04, RS05, RS06).
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).
