# MS-RR-RP01
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs` spine, `patient.neurological_exam.additional` | Reproducible Lhermitte sign with bilateral Babinski signs but "Normal cervical spinal cord" on the spine MRI (class R). | FIXED: spine report now shows a short dorsal C2-C3 lesion (under one segment, under half the cross-section, non-enhancing), thoracic cord normal; impression numbered. DIS becomes 4 regions. |
| C | major | `followup_outputs` `interpret_labs` `request_ct_body` | Body CT (and a mammogram) filed as a lab panel (class G3). | FIXED: replaced by an `order_body_imaging` follow-up (`region chest_abdomen_pelvis`, `modality CT`) with a normal report; new optional criterion `action-ct-cap`. Mammography dropped (not part of the study). |
| B | minor | `followup_outputs` MRS | Signal string carried interpretation ("suggesting neuronal injury"); no quantitative data. | FIXED: metabolite values with Cho/NAA 0.9, normal-appearing white matter reference, within-modality impression; new optional criterion `action-mrs`. |
| D | major | `initial_tool_outputs.mri.impression` | Differential essay (glioma, metastasis, abscess, "atypical for neoplasm"). | FIXED: numbered findings and one hedged imaging read ("favours a tumefactive demyelinating lesion; a neoplasm cannot be excluded on imaging alone"); added "Spinal cord not assessed on this study"; cerebellar lesion located to the middle cerebellar peduncle. |
| C | minor | `initial_tool_outputs.csf.special_tests` | Myelin basic protein with reference "<1.5" (obsolete, F6); "CSF AFB culture: final at 8 weeks" impossible within an inpatient work-up; no kFLC. | FIXED: MBP deleted; AFB culture replaced by "CSF AFB smear: No acid-fast bacilli seen"; kFLC index 42.0 (reference <6.1) added. |
| D | minor | `initial_tool_outputs.csf.interpretation` | Recital with "(N/A PMN/N/A lymph)". | FIXED: pattern statement (acellular, traumatic red cells, CSF-restricted OCB, raised IgG and kFLC index, cytology/flow negative). |
| D | minor | `initial_tool_outputs.labs.panels` | AQP4 row named `AQP4_IgG` with leaked significance ("excludes this reversible mimic"), MOG in a separate panel; "AFB smear" with no specimen. | FIXED: one Neuroimmunology panel with the two CBA rows (significance null); AFB smear row deleted. WBC 7.2 -> 6.4 and BUN 14 -> 12 so no CBC/BMP value repeats RM04 (plan E). |
| A | major | `ground_truth.action_criteria` | Template criteria: literature required, drug check with non-schema keys, CSF needing three assays, labs needing 11 analytes including AQP4/MOG. | FIXED per plan A2-A8: canonical labels and case rationales; labs `[CBC, vitamin_B12, TSH, HIV]` required; new `action-aqp4-mog-cba` required (tumefactive lesion); CSF two alternatives, recommended; MRS and CT CAP optional; drug check `{}` optional; literature `{}` optional last. |
| A | minor | `ground_truth.stop_rule`, `sequence_constraints` | Stop rule listed literature and drug check, max 0; constraint cited McDonald 2017. | FIXED: brain MRI, spine MRI, labs, AQP4/MOG; max 3; soft MRI-before-CSF with canonical reason. |
| D | major | `followup_outputs` literature | Fabricated authors ("Defined group of MS researchers") and unverifiable titles, an invented specificity range. | FIXED: three verifiable sources (Masdeu 2000 Neurology, Lucchinetti 2008 Brain, Hardy and Chataway 2013 JNNP) with general findings; last in the pathway. |
| C | minor | `followup_outputs` drug check | "Sumatriptan ... both may cause vasoconstriction" (interferon beta is not a vasoconstrictor); ibuprofen missing. | FIXED: each current medicine against interferon beta-1a; warnings and contraindications kept, alternatives without choice argument. |
| C | major | `ground_truth.differential` | PCNSL and glioblastoma "high", NMOSD/MOGAD "moderate" after a work-up that argues against them (ruling 7); metastasis and abscess raised by the report but metastasis absent; ACE and ANA rows without entries. | FIXED: all low with the case's own results; metastasis, abscess/tuberculoma, neurosarcoidosis, lupus added; PCNSL ICD C83.39 and "not excluded by tissue" stated. |
| E | major | `ground_truth.key_clinical_evidence` | Template lines: "three regions establish DIS" (F2), T1 black holes give DIT (F5), DMT choice, generic spinal line, engineering "July 2026" lines, "brain biopsy should be a last resort". | FIXED: five observable lines (syndrome, DIS 4 of 5, tumefactive features, positive CSF, mimic exclusion). |
| C | major | `ground_truth.assessment.required_recommendations` | DIS/DIT interpretation musts, AQP4/MOG test as a must, a generic IVMP relapse must for a patient whose lymphoma risk needs CSF first, generic lifestyle must (no smoking, no vitamin D value, no Uhthoff). | FIXED: formulation must; IVMP for the symptomatic tumefactive lesion only after negative CSF cytology and flow, with PPI (ibuprofen) and glucose monitoring; repeat MRI at 4-6 weeks with biopsy if atypical; DMT by activity with contraception; pre-DMT screening. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Natalizumab (no JCV result) and fingolimod (no cardiac issue) prohibitions; surgery prohibition named tests. | FIXED: those two deleted; added "no corticosteroids before CSF cytology and flow cytometry" and "no resection or oncological treatment on imaging alone"; T7, T10 (woman of child-bearing potential), T11, T12, T13 (Lhermitte, bilateral Babinski) kept. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales, McDonald 2017/Reich 2018 citations. | FIXED: case-tied rationales; `[Wattjes_2021]` for CT, none for EEG, echo, monitoring. |
| B | minor | `patient.chief_complaint` | "electric shock-like sensations ... for 7 months" while the HPI dates them to 5 months. | FIXED: "headache for 7 months and electric shock-like sensations ... for 5 months". |
| B | minor | `metadata.difficulty_description`, `difficulty_rationale` | Cited "VEP prolongation", which the case never serves. | FIXED: rewritten from the case's own clues. |
| E | minor | `fallback_tool_outputs.echo` | `echo_type` missing. | FIXED: `TTE`. |

## Changes, in one paragraph a physician can read before re-reviewing

The case now holds together as tumefactive relapsing-remitting MS. The Lhermitte sign and bilateral Babinski signs are explained by a new short dorsal C2-C3 lesion on the spine MRI, so dissemination in space is in four regions (periventricular, left parietal juxtacortical, left middle cerebellar peduncle, cord) and no separate DIT is needed, although the scan also shows enhancing and non-enhancing lesions. The brain MRI impression lists findings and one hedged imaging read. CSF has five restricted bands, kFLC index 42.0 and negative cytology and flow cytometry; the impossible 8-week AFB culture and myelin basic protein were removed. The body CT is now a real chest-abdomen-pelvis CT report, and spectroscopy reports Cho/NAA 0.9 without a lipid peak. Required: brain MRI, spine MRI, mimic labs and AQP4/MOG CBA (tumefactive red flag); CSF recommended; spectroscopy, CT, drug check and literature optional. The differential lists lymphoma, glioma, metastasis, abscess/tuberculoma, NMOSD, MOGAD, ADEM, sarcoidosis and lupus, all low with the excluding results; lymphoma is noted as not excluded by tissue. Musts: diagnosis by the 2024 criteria; IV methylprednisolone for the symptomatic lesion only after negative CSF cytology and flow, with a PPI because she takes ibuprofen; repeat MRI at 4-6 weeks with biopsy if the lesion does not regress; DMT by activity with contraception; pre-DMT screening. Prohibitions add no steroids before CSF and no resection or oncological treatment on imaging alone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` to the MS-RR criteria pack (plan 5.1).
- Diagnosis synonyms: G35.B/G35.C and "demyelinating disease" (plan Q, 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea's information. Decided: corticosteroids are a must after negative CSF cytology and flow cytometry rather than after biopsy, because the plan gives RP01 no biopsy and imaging, spectroscopy, CSF bands and four-region disease make demyelination the clear diagnosis; the repeat-MRI must with biopsy on an atypical course is the safety net (Hardy and Chataway 2013).

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff against `b8be2153^` and the whole final case. Checked each FIXED finding (C2-C3 dorsal lesion in the spine report and in KCE/expected evidence; CT CAP as `order_body_imaging` region chest_abdomen_pelvis / modality CT, which the body-imaging matcher resolves for `study: chest_abdomen_pelvis_CT`; MRS values arithmetic Cho/NAA 1.4/1.6 = 0.9; MBP and 8-week AFB culture gone; kFLC 42.0; no cord text in the brain MRI; literature sources Masdeu 2000, Lucchinetti 2008, Hardy and Chataway 2013 exist as cited). Musts and prohibitions are consistent (no steroids before CSF cytology/flow, IVMP after negative CSF with PPI for ibuprofen; T10 appropriate for a 37-year-old woman). Differential all low with the case's results.
Found and fixed:
- B major, `fallback_tool_outputs.ct`: the head-CT fallback read "No ... mass", contradicting the 2.1 cm right periventricular lesion with oedema that the MRI shows (a CT ordered despite the waste avoidance would have returned a normal brain). Replaced with a right periventricular hypodensity with mild oedema, no shift (same style as RM01/RP02/RP03); `metadata.fallback_tool_kinds.ct` set to "abnormal".
- B minor, `ground_truth.differential[Brain abscess or tuberculoma].key_features`: "CSF AFB smear and culture negative" implied an AFB culture result the CSF no longer reports (the worker removed it); now "CSF AFB smear negative and CSF culture sterile".
Re-ran `perfect_agent.py MS-RR-RP01 -v` (pass), `case_io.py check` (clean for the case) and `test_case_guards -k MS-RR-RP01` (pass).

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `ground_truth.differential[6].icd_code` G04.81 -> G04.00: G04.81 is other encephalitis; ADEM is G04.00, as in the other 8 MS-RR cases.
- `ground_truth.differential[7].icd_code` D86.85 -> D86.89: D86.85 is sarcoid myocarditis; neurosarcoidosis is D86.89, as in the other 11 MS-RR cases.
- `action-3-search-medical-literature.label` "Literature search (background only)" -> "Literature search on tumefactive demyelination": engineering text replaced by the topic of the stored output.
- `assessment.prohibited_recommendations[4]` chronic-steroid prohibition set to the condition's canonical text (was "Do not use chronic oral corticosteroids as a maintenance treatment for MS").
- `assessment.prohibited_recommendations[6]` spinal-cord prohibition set to the condition's canonical text (was "Do not omit spinal-cord MRI in a patient with myelopathic signs even if the brain MRI alone meets DIS criteria").
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders). Initial labs interpretation edited to drop the antibody results: removed "All results within reference ranges, including AQP4-IgG and MOG-IgG negative by cell-based assay.".

## Close-out (24 Oct 2026)

Condition close-out (`plans/MS-RR-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G35 entry, re-applied with `apply_diagnosis_synonyms.py --prune --conditions multiple_sclerosis`): removed the label "demyelinating disease" (G37.9 is an Excludes1 of G35.A, and its tokens occur in an NMOSD, MOGAD or ADEM answer, which would have scored as correct) and the codes G35.B and G35.C (primary and secondary progressive MS in FY2026 ICD-10-CM, a different course from this relapsing-remitting case). Accepted now: the label, multiple sclerosis, MS, relapsing(-)remitting multiple sclerosis, RRMS; codes G35.A, G35, G35.D.
- `action-mrs` and `action-ct-cap` (which had no citation): added `[Hardy_2013]` (Hardy TA, Chataway J. Tumefactive demyelination: an approach to diagnosis and management. JNNP 2013;84(9):1047-1053), the review that governs the work-up of a tumefactive lesion and the decision to biopsy; now in the pack's allow-list.
- Checks: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MS-RR-` passes with MS-RR now in `DISCRIMINATOR_CONDITIONS`.
