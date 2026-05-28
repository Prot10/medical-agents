# NeuroBench v5 audit — GLIO-HG (high-grade glioma / neuro-oncology)

Scope: all 20 `GLIO-HG-*` cases. Method: full field-by-field read of every case against
`criteria_packs/GLIO-HG.md` and `TOOL_REPORT_STYLE_GUIDE.md`; five dimensions
(A schema, B internal consistency, C clinical correctness, D realism/leakage, E language).
Mechanical validators run on every case: coherence = 0/20, schema valid 20/20, vocab 516/516 pass.

Conservative-fix policy applied: only unambiguous mechanical errors fixed inline; everything
requiring judgment FLAGGED. Diagnosis and within-modality (Kind-2) conclusions never altered.
Per brief: MRI "high-grade neoplasm" differential KEPT; biopsy histology + molecular markers
(IDH/MGMT/1p19q/TERT/EGFR) KEPT as confirmatory; literature summaries KEPT as population-keyed;
GLIO-HG-P02 prefix/diagnosis mismatch (PCNSL mimic) FLAGGED not fixed.

| case_id | dim | severity | region.field | finding | action | detail |
| --- | --- | --- | --- | --- | --- | --- |
| (all M/P/RM/RP/RS01-03) | B/D | minor | followup_outputs[4].output.modality | fMRI content (language/motor/laterality mapping, DTI) delivered under `modality: "perfusion_MRI"`. fMRI is not in the closed advanced-imaging vocab; S04/S01/S02/S03/RS04 correctly use `fMRI_BOLD` for the same content — so this is an internal labeling inconsistency, not a vocab violation (followup modality strings are not vocab-checked). | FLAGGED | Affects M01,M02,M03,P01,P03,RM01,RM03,RP01,RP02,RP03,RS01,RS02,RS03. Mislabel; correct content label = fMRI/BOLD. Not fixed (no clean vocab value; content is unambiguous). |
| GLIO-HG-P01 | B | minor | initial_tool_outputs.labs.abnormal_values_summary | "Hemoglobin: 13.2 g/dL (H)" — Hgb 13.2 vs ref 13.5-17.5 is LOW; `interpretation` field correctly says (L). | FIXED | Changed (H)→(L). |
| GLIO-HG-P01 | B | minor | initial_tool_outputs.labs.abnormal_values_summary | "Chloride: 92 mEq/L (H)" — Cl 92 vs ref 98-106 is LOW; `interpretation` correctly says (L). | FIXED | Changed (H)→(L). |
| GLIO-HG-P01 | E | nit | initial_tool_outputs.labs.abnormal_values_summary | "MGMT promoter methylation: Unmethylated (L)" — interpretation tags it (H); marker is neither high nor low. Cosmetic auto-tag inconsistency. | FLAGGED | Non-numeric marker; left as-is. |
| GLIO-HG-P01 | B/C | major | ground_truth.differential | "Brain abscess" appears twice (idx0 post-dental moderate; idx4 generic very_low) — duplicate diagnosis with contradictory likelihoods. | FLAGGED | idx4 is a generic-template leftover; removing changes GT semantics. |
| GLIO-HG-P01 | C | minor | patient.history_present_illness | Occupation = "accountant" but HPI says he prepared a "lesson plan for his class" — template teacher boilerplate. | FLAGGED | Patient-story edit; do not rewrite. |
| GLIO-HG-P01 | D | minor | followup_outputs[5].output (ID consult via interpret_labs) | ID consult note performs cross-modality synthesis ("MRI perfusion and spectroscopy findings favor neoplasm over abscess") and gives management (empiric ceftriaxone/metronidazole). Partially resolves the abscess-vs-tumor puzzle for the agent. | FLAGGED | Consults may integrate; borderline for a diagnostic_puzzle. Routed through interpret_labs (structural oddity). |
| GLIO-HG-P01 | A | nit | metadata.case_body_concerns | Two identical literature-demotion sentences (duplicate). | FLAGGED | Pre-existing metadata dup. |
| GLIO-HG-M02 | B/C | major | followup_outputs[6].output (check_drug_interactions).warnings | "Verify negative pregnancy test … patient is 52, likely perimenopausal" in a 47-year-old MALE patient — copy-paste from M01 (52yo female). Wrong age and clinically nonsensical for a male. | FLAGGED | Touches clinical warning text; flag for human (do not silently delete). Also note in metadata.case_body_concerns recommended. |
| GLIO-HG-M02 | B | minor | ground_truth.icd_code | C71.9 (unspecified) while lesion is left temporal (C71.2 more specific); diagnosis string omits localizer. Defensible. | FLAGGED | Low priority. |
| GLIO-HG-M03 | C | major | patient.history_present_illness | Occupation = "IT project manager" but HPI repeatedly calls her an "English teacher", references "lectures" and "grading papers". Internal contradiction (template). | FLAGGED | Patient-story edit; do not rewrite. |
| GLIO-HG-P02 | B | minor | initial_tool_outputs.labs.abnormal_values_summary | "CD4 count: 82 cells/mcL (AIDS) (H)" — 82 vs ref >500 is LOW; interpretation correctly (L). | FIXED | Changed (H)→(L). |
| GLIO-HG-P02 | B | blocker | case_id / condition / ground_truth.primary_diagnosis | Filed GLIO-HG / condition brain_tumor_glioma but diagnosis is "Primary CNS lymphoma (EBV-DLBCL) in HIV/AIDS" — intentional mimic, prefix mismatch. | FLAGGED | Per brief: flag, don't fix. Already noted in metadata.case_body_concerns. |
| GLIO-HG-P02 | B/C | major | ground_truth.optimal_actions / critical_actions | GBM-templated expected_findings & actions ("ring enhancement…central necrosis"; "Stupp protocol with temozolomide for IDH-wildtype GBM") embedded in a PCNSL case whose actual MRI is homogeneous non-ring and whose correct Rx is high-dose MTX, not Stupp. | FLAGGED | GT semantics; tied to re-filing. key_reasoning_points correctly describe PCNSL. |
| GLIO-HG-P02 | B/C | major | ground_truth.differential | "Cerebral toxoplasmosis" duplicated (idx1 and idx2, both moderate, near-identical features). | FLAGGED | Duplicate; GT semantics. |
| GLIO-HG-P02 | D | minor | followup_outputs[2] (analyze_csf).interpretation | CSF closes with "CSF findings are diagnostic for primary CNS lymphoma in the setting of AIDS" — cytology/flow/EBER are within-modality confirmatory (KEPT); "in the setting of AIDS" is mild cross-modality. | FLAGGED | Borderline; KEPT per confirmatory rule. |
| GLIO-HG-P02 | A | nit | metadata.case_body_concerns | Duplicate literature-demotion sentence. | FLAGGED | Pre-existing. |
| GLIO-HG-P03 | C | major | patient.history_present_illness | Occupation = "insurance adjuster" but HPI calls him a "high school history teacher", references "mid-lecture" and "his students". Contradiction (template). | FLAGGED | Patient-story edit. |
| GLIO-HG-P03 | B/C | major | ground_truth.differential | "Brain abscess" (idx0 odontogenic moderate + idx4 generic very_low) and "Tumefactive demyelination/demyelinating lesion" (idx1 low + idx5 very_low) — two duplicated/overlapping pairs (generic template leftovers). | FLAGGED | GT semantics. |
| GLIO-HG-P03 | D | minor | followup_outputs[6] (demyelination workup via interpret_labs) | VEP (P100) reported through interpret_labs rather than order_specialized_test; within-modality read is fine. | FLAGGED | Structural oddity only. |
| GLIO-HG-RM01 | A/E | minor | difficulty vs metadata.difficulty_description | Top-level `straightforward` vs metadata "Moderate difficulty". | FLAGGED | Pick one. |
| GLIO-HG-RM01 | B/C | minor | ground_truth (key_reasoning_points, optimal_actions[1].expected_finding) | Generic GBM imaging descriptors ("central necrosis", "restricted diffusion at rim") but this case's MRI says "no central necrosis", "no restricted diffusion centrally"; histology has "No microvascular proliferation, no palisading necrosis" (grade-4 by molecular upgrade). Templated GT vs case data. | FLAGGED | GT semantics; case is real-seed brainstem GBM. |
| GLIO-HG-RM01 | B | minor | ground_truth.differential | "Brainstem metastasis" (idx1) and "Brain metastasis (solitary)" (idx2) overlapping; generic abscess/tumefactive leftovers for a brainstem mass. | FLAGGED | Mild redundancy. |
| GLIO-HG-RM02 | C | major | harmful_tools[analyze_csf] + followup request_csf_analysis | LP contraindication rationale cites "intracranial mass effect / herniation"; but the lesion is an isolated cervical-cord glioma with a NORMAL brain MRI — the herniation rationale does not apply. A CSF followup is nonetheless provided. | FLAGGED | Clinical judgment; harmful classification likely inapplicable to this spinal case. |
| GLIO-HG-RM02 | B/C | major | case localization | Cervical intramedullary cord glioma (C72.0), not cerebral C71.x; optimal_actions[1] says "Order MRI brain … to characterize the cervical spinal cord lesion". | FLAGGED | Already noted in metadata.case_body_concerns; re-filing consideration. |
| GLIO-HG-RM02 | A/E | minor | difficulty vs metadata | Top-level `diagnostic_puzzle` vs metadata "Moderate difficulty". | FLAGGED | — |
| GLIO-HG-RM03 | C | minor | ground_truth.critical_actions | "Initiate antiepileptic therapy with levetiracetam … for documented seizure activity" but HPI explicitly "denies any seizures" (cerebellar mass). Templated action not matching case. | FLAGGED | GT semantics. |
| GLIO-HG-RM03 | A/E | minor | difficulty vs metadata; red_herrings | Top-level `straightforward`; metadata says "Moderate difficulty" and names red herrings; `red_herrings: []` and difficulty_rationale says "no embedded red herrings". Internal disagreement. | FLAGGED | — |
| GLIO-HG-RM03 | B | minor | ground_truth.differential | Generic supratentorial template entries (periventricular PCNSL, etc.) less apt for a cerebellar mass. | FLAGGED | Low priority. |
| GLIO-HG-RP01 | B | minor | ground_truth.differential[0] vs labs | Differential says "undetectable thyroglobulin … makes recurrence unlikely", but current Tg is 3.2 (detectable; the intended red herring). Mild tension (prior value undetectable, current mildly up). | FLAGGED | Defensible; loose wording. |
| GLIO-HG-RP01 | B/C | minor | ground_truth (templated imaging descriptors) | "central necrosis / ring enhancement" in GT but MRI is "no definite central necrosis", predominantly non-enhancing infiltrative. | FLAGGED | GT template vs atypical case. |
| GLIO-HG-RP01 | A/E | minor | difficulty vs metadata | Top-level `moderate`; metadata "Diagnostic puzzle", confidence 0.4. | FLAGGED | — |
| GLIO-HG-RP02 | C | minor | harmful_tools[analyze_csf] + followup request_csf_analysis | Generic herniation rationale with only 3 mm shift; CSF followup provided as TB/MS-excluding test. Recurring mimic-case tension. | FLAGGED | Consistency. |
| GLIO-HG-RP02 | C | minor | ground_truth.differential | Generic 4-entry set omits the case's actual prominent mimics (CNS tuberculoma given prior TB; tumefactive MS given family hx) that the workup addresses. | FLAGGED | Differential under-captures case. |
| GLIO-HG-RP02 | A/E | minor | difficulty vs metadata | Top-level `moderate`; metadata "Diagnostic puzzle", confidence 0.4. | FLAGGED | — |
| GLIO-HG-RP03 | B/C | blocker | ground_truth.primary_diagnosis | "Diffuse astrocytoma, IDH-MUTANT, WHO grade 2 with leptomeningeal dissemination" — a LOW-grade glioma in the high-grade (GLIO-HG) pack. | FLAGGED | Per policy never change dx; already noted in metadata.case_body_concerns (recommends re-filing). Top adjudication item. |
| GLIO-HG-RP03 | B/C | major | ground_truth.optimal_actions / critical_actions | GBM/Stupp-templated GT (central necrosis, temozolomide-for-GBM, AED-for-seizure) contradicts the grade-2 IDH-mutant diagnosis (no necrosis; MGMT methylated; different Rx intent). | FLAGGED | GT semantics. |
| GLIO-HG-RP03 | E | minor | ground_truth.optimal_actions[1].action | Garbled template substitution: "characterize the diffuse with leptomeningeal dissemination lesion" (not a valid noun phrase). | FLAGGED | Language defect; rewriting risks meaning change. |
| GLIO-HG-RP03 | C | minor | harmful_tools[analyze_csf] | "No significant midline shift", multifocal leptomeningeal disease — LP/CSF cytology would be useful and not clearly contraindicated; generic herniation rationale questionable. | FLAGGED | Clinical judgment. |
| GLIO-HG-RS01 | B | nit | ground_truth.differential | Lead "Brain metastasis from malignant paraganglioma/pheochromocytoma" then generic "Brain metastasis (solitary)" — mild overlap. | FLAGGED | Low priority. Chromogranin-A-negative biopsy KEPT (within-modality). |
| GLIO-HG-RS01 | A/E | minor | difficulty | Top-level `diagnostic_puzzle` consistent w/ confidence 0.35; OK. fMRI-as-perfusion_MRI label (see global row). | FLAGGED | — |
| GLIO-HG-RS04 | C | nit | ground_truth | Giant cell glioblastoma (WHO grade 4, valid high-grade) with "Conventional GBM" as differential and recurrent-HSV-encephalitis entry — clinically coherent. fMRI labeled `fMRI_BOLD` (correct content label). | — | No issue; noted as clean. |
| GLIO-HG-S01 | C | nit | patient.history_present_illness | Occupation "insurance adjuster"; HPI "dropping tools … at work" — mildly atypical phrasing but not a hard contradiction. | FLAGGED | Low priority. |
| GLIO-HG-S02 | C | major | patient.history_present_illness | Occupation = "accountant" but HPI: "high school math teacher", "lectures", "teaching", "parent-teacher conference". Contradiction (template). | FLAGGED | Patient-story edit. |
| GLIO-HG-S03 | C | minor | patient.history_present_illness | Occupation = "high school principal"; HPI "uncharacteristic for him as a teacher". Mild contradiction (principal vs teacher). | FLAGGED | Patient-story edit. |
| GLIO-HG-S04 | A | nit | metadata.case_body_concerns | Duplicate entries in metadata. | FLAGGED | Pre-existing. |
| (S02,S03,S04,RS02,RS03,RS04,S01) | C/D | — | overall | Necrotic ring-enhancing GBM with matching templated GT; seizures in HPI match AED critical_action; biopsy confirmatory KEPT; MRI hedged appropriately; literature population-keyed. | — | No actionable findings beyond global fMRI-label row. |

## Recurring patterns (apply across the pack)

1. **fMRI mislabeled as `perfusion_MRI`** in 13 cases' `followup_outputs[4]`; 5 newer cases use `fMRI_BOLD`. Pure labeling inconsistency (not vocab-checked). Recommend standardizing to `fMRI_BOLD`.
2. **Occupation vs HPI "teacher/lecture/student" template residue**: M03, P01, P03, S02, S03 (and mild S01). Demographics localized but HPI kept teacher boilerplate.
3. **Duplicate / generic-template differential entries**: P01, P02, P03 (true duplicate diagnoses); RM01, RM03, RP01 (less-apt generic leftovers).
4. **Templated GBM GT (necrosis/ring/Stupp/AED-for-seizure) vs atypical case data**: RM01, RM03, RP01, P02, RP03 — most severe in RP03 (grade-2 IDH-mutant) and P02 (PCNSL).
5. **`difficulty` enum vs `metadata.difficulty_description` disagreement**: RM01, RM02, RM03, RP01, RP02.
6. **LP/`analyze_csf` harmful-tool herniation rationale applied generically** to cases where it does not hold (RM02 spinal w/ normal brain; RP03 leptomeningeal, no shift; RP02 only 3 mm).
7. **Off-pathway / mis-prefiled cases (already in metadata.case_body_concerns)**: P02 (PCNSL/HIV), RM02 (spinal C72.0), RP03 (low-grade IDH-mutant).

## Tally

- Cases audited: 20 / 20 (every field of every case).
- Mechanical validators: coherence 0 issue(s) on all 20; schema valid 20/20; tool vocab 516/516 pass (incl. all 20).
- Findings by severity: 2 blocker (P02 prefix, RP03 grade-2 in HG pack — both intentional/known, flag-only); 9 major; ~17 minor; ~6 nit.
- Fixed: 3 (P01 Hgb tag, P01 Cl tag, P02 CD4 tag — all unambiguous H/L direction errors where the `interpretation` field already had the correct direction).
- Flagged: all remaining (~30 distinct findings + recurring-pattern rows).
- Self-verify: P01 and P02 re-validated post-edit — coherence 0, schema valid. Only GLIO-HG-P01 and GLIO-HG-P02 were written; unicode/escaping and trailing newline preserved. No other condition's files touched.

## Top clinical-correctness flags for human adjudication

1. **RP03** is an IDH-MUTANT WHO grade-2 astrocytoma (not high-grade) filed in GLIO-HG — re-file and reconcile its GBM/Stupp-templated ground_truth.
2. **P02** is PCNSL in HIV/AIDS filed under GLIO-HG with GBM-templated optimal/critical actions that contradict the correct MTX-based, biopsy-not-resection management.
3. **M02** drug-interaction warning asserts pregnancy/perimenopausal status and age 52 for a 47-year-old male — clinically nonsensical copy-paste.
4. **RM02** harmful-tool LP/herniation rationale is clinically inapplicable (isolated spinal cord tumor, normal brain); same generic rationale is questionable in RP03 and RP02.
5. **Occupation↔HPI contradictions** (M03, P01, P03, S02, S03) — patient stories internally inconsistent; resolve before clinician validation.
6. **Duplicate differential entries** in P01/P02/P03 (contradictory likelihoods for the same diagnosis).
