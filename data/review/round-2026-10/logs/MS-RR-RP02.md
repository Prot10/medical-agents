# MS-RR-RP02
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | `ground_truth.action_criteria[action-5-analyze-csf]`, `followup_outputs` CSF, `sequence_constraints` | CSF recommended and served after MRI in a patient with a 4.1 cm mass, 6 mm midline shift and bilateral papilloedema (class L: the pathway performs a contraindicated LP). | FIXED: CSF criterion and its hard constraint deleted; avoided action `avoid-contra-lp-mass-effect` (`analyze_csf {}`, contraindicated); CSF content moved to `fallback_tool_outputs.csf` so an LP still returns a coherent report; LP prohibition reworded to the case. |
| C | major | `followup_outputs` `analyze_brain_mri` `request_perfusion_mri` | Perfusion filed as a brain MRI follow-up (G6). | FIXED: `order_advanced_imaging` `perfusion_MRI` follow-up (rim rCBV 1.4, hypoperfused centre, Ktrans), optional `action-perfusion`. |
| D | major | `initial_tool_outputs.mri.additional_observations[0]`, `.impression` | The brain MRI reported spectroscopy that was not ordered. | FIXED: MRS moved to an `order_advanced_imaging` `MR_spectroscopy` follow-up with the same values (Cho/Cr 2.1, NAA/Cr 1.2, lactate, myo-inositol) and a non-specific read; optional `action-mrs`. MRI impression rewritten as numbered findings with a hedged imaging read and "Tissue diagnosis recommended"; "leftward-to-rightward" shift corrected to "rightward"; "Spinal cord not assessed on this study" added. |
| C | major | `followup_outputs` `interpret_labs` `request_biopsy_pathology` | Biopsy filed as a lab panel; its summary said "Low Ki-67 and no IDH mutation exclude glioma" (G2). | FIXED: `obtain_tissue_diagnosis` `stereotactic_biopsy` follow-up with histology (macrophages with myelin debris, perivascular CD8 T cells, Creutzfeldt cells, preserved axons, no mitoses, microvascular proliferation or necrosis), CD20 and IDH1 IHC, histology-only impression; recommended `action-biopsy`; soft constraint brain MRI before biopsy. |
| C | major | `followup_outputs` drug check | "Corticosteroids may reduce efficacy of hormonal contraception" (false, F11); IVIG offered as an MS relapse alternative; diagnosis named in `proposed`. | FIXED: COC line corrected (oestrogen raises steroid exposure, efficacy unaffected); ibuprofen GI risk kept; IVIG removed; oral MP and PLEX as alternatives. |
| D | major | `followup_outputs` literature | Empty summary (G7); Lucchinetti 2008 attributed to Neurology with a wrong title, Hardy and Chataway 2013 to Practical Neurology, Kiriyama 2011 unverifiable. | FIXED: three verifiable sources (Cha 2001 AJNR, Lucchinetti 2008 Brain, Hardy and Chataway 2013 JNNP), general summary; last in pathway. |
| D | minor | CSF (now fallback) `special_tests`, `interpretation` | Serum AQP4/MOG listed inside the CSF report; "intact blood-brain barrier"; differential sentence about glioma; no kFLC. | FIXED: serum rows removed (results live in labs), Q_alb with a reference only, kFLC index 2.6 (reference <6.1), pattern interpretation. |
| C | major | `patient.history_present_illness`, `chief_complaint` | Bilateral papilloedema and a 4.1 cm lesion with 6 mm shift after a 1-day illness is implausible; "mild tachycardia" with HR 88; the HPI restated the exam. | FIXED: one week of worsening headache (morning predominance) and two days of right-sided weakness; tachycardia and the exam recital deleted. |
| C | major | `ground_truth.avoided_actions[avoid-waste-2-order-ct-scan]`, `fallback_tool_outputs.ct` | Head CT avoided as waste in an ED patient with headache, vomiting, hemiparesis and papilloedema; the CT fallback was normal, contradicting the mass (N, M). | FIXED: CT avoidance deleted; CT fallback shows the left parietal hypodensity with oedema and 6 mm shift (`fallback_tool_kinds.ct` "abnormal", `.csf` "case"). |
| D | minor | `initial_tool_outputs.labs.panels` | AQP4 and HIV rows with leaked significance ("excludes this reversible mimic"); MOG in a separate panel. | FIXED: Neuroimmunology panel with the two CBA rows, HIV in an Infectious panel, significance null; "Tumor Markers" renamed "Other markers"; BUN 14 -> 11 to avoid repeating RM04/RP01 values. |
| A | major | `ground_truth.action_criteria` | Template criteria (literature required, drug check with non-schema keys, labs with 11 analytes including AQP4/MOG). | FIXED: canonical labels and case rationales; labs `[CBC, vitamin_B12, TSH, HIV]` required; `action-aqp4-mog-cba` required (tumefactive); perfusion and MRS optional; biopsy recommended; drug check `{}` and literature `{}` optional, last. |
| A | minor | `ground_truth.stop_rule` | Literature and drug check required before assessment; max 0. | FIXED: brain MRI, spine MRI, labs, AQP4/MOG; max 3. |
| C | major | `ground_truth.differential` | Lymphoma and glioblastoma "high", NMOSD/MOGAD "moderate" after biopsy and CBA (ruling 7); metastasis absent. | FIXED: all low with the biopsy, CBA and imaging results; metastasis added. |
| E | major | `ground_truth.key_clinical_evidence` | Template lines (three regions establish DIS, black holes give DIT, OCB substitute for DIT with no CSF in the pathway, DMT choice, "brain biopsy should be a last resort", engineering lines). | FIXED: seven observable lines (syndrome and lesion, DIS 2 of 5, MRI DIT, histology, CBA, indeterminate perfusion/MRS with LP unsafe, family-history distractor). |
| C | major | `ground_truth.assessment.required_recommendations` | Generic IVMP "for the acute relapse" with no instruction to withhold steroids before biopsy; no ICP management; diagnostic tests as musts; lifestyle must without case basis. | FIXED: formulation must; withhold corticosteroids until stereotactic biopsy (dexamethasone only for impending herniation after neurosurgical discussion); ICP measures; IVMP after histology with PPI (ibuprofen) and glucose monitoring, PLEX if inadequate; DMT by activity with contraception; pre-DMT screening. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Natalizumab, fingolimod and spinal-MRI (no myelopathic signs) prohibitions without case basis. | FIXED: deleted; added "no corticosteroids before tissue" and "no resection or oncological treatment on imaging or family history alone"; T7, T10, T11, T12 kept. |
| B | minor | `ground_truth.red_herrings` | Empty, although the case is built around the father's glioblastoma. | FIXED: one red herring on `patient.clinical_history.family_history[0]`. |
| B | minor | `followup_outputs` spine | Lesion row without description; "lumbar spinal cord". | FIXED: position, cross-section and enhancement stated; "cervical or thoracic cord; conus normal". |
| B | minor | `metadata.difficulty_description`, `difficulty_rationale` | Described CSF results the agent should not obtain and "to avoid biopsy". | FIXED: rewritten to the corrected pathway. |
| E | minor | `fallback_tool_outputs.echo` | `echo_type` missing. | FIXED: `TTE`. |

## Changes, in one paragraph a physician can read before re-reviewing

Lumbar puncture is now contraindicated (4.1 cm left parietal lesion, 6 mm midline shift, bilateral papilloedema): the CSF criterion and its constraint are gone, an LP is an avoided contraindicated action, and the old CSF result (OCB negative, kFLC 2.6) is served only as a fallback. The HPI was made plausible (one week of headache, two days of weakness). The brain MRI reports only MRI findings; perfusion (rim rCBV 1.4) and spectroscopy (raised choline, lactate) are separate optional advanced-imaging studies, and the biopsy is a real stereotactic tissue report showing active demyelination without atypical cells (recommended). Head CT is no longer called waste and its fallback shows the mass. Required: brain MRI, spine MRI (dorsal C3-C4 lesion), mimic labs and serum AQP4/MOG CBA. The diagnosis rests on two regions (periventricular, cord) plus MRI DIT once histology excludes tumour. Musts: diagnosis by the 2024 criteria; withhold steroids until biopsy (dexamethasone only for impending herniation after neurosurgical discussion); ICP measures; IV methylprednisolone after histology with a PPI because of ibuprofen; DMT with contraception discussion; pre-DMT screening. The false drug interaction (steroids reducing contraceptive efficacy) is gone, the differential has every mimic low with the excluding result, and the father's glioblastoma is now an explicit red herring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` to the MS-RR criteria pack (plan 5.1).
- Diagnosis synonyms: G35.B/G35.C and "demyelinating disease" (plan Q, 5.2).
- `condition_tool_guidance.yaml` claims: CT no longer avoided in RP02 (plan 5.3).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea's information. Decided: the HPI timeline was lengthened (one week of headache, two days of weakness) because bilateral papilloedema with a 4 cm lesion after a one-day illness is not credible; the chief complaint changed with it.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff against `b8be2153^` and the whole final case. Checked: CSF criterion and its hard constraint gone, contraindicated LP avoided action present and matching the LP prohibition; no criterion or must depends on CSF; perfusion and MRS moved to `order_advanced_imaging` with correct arithmetic (Cho/NAA 2.1/1.2 = 1.75); brain MRI no longer reports spectroscopy; biopsy is a real `obtain_tissue_diagnosis` report with a histology-only impression and recommended tier; head-CT fallback shows the mass and shift; steroids withheld until tissue with dexamethasone only for impending herniation (no contradiction between musts); the COC interaction now states the correct direction (F11); literature sources (Cha 2001 AJNR, Lucchinetti 2008, Hardy and Chataway 2013) exist; DIS 2 regions plus MRI DIT is a valid 2024 formulation; differential all low with the biopsy/CBA results. The HPI timeline change (one week of headache) is justified by bilateral papilloedema.
Found and fixed:
- B minor, `fallback_tool_outputs.csf.opening_pressure` and `.interpretation`: the CSF an agent would get from the contraindicated LP gave an opening pressure of 15 cmH2O in a patient with bilateral papilloedema and 6 mm midline shift. Set to 28 cmH2O (reference 10-20) and the interpretation now opens "Raised opening pressure (28 cm H2O); otherwise normal CSF".
Re-ran `perfect_agent.py MS-RR-RP02 -v` (pass), `case_io.py check` (clean for the case) and `test_case_guards -k MS-RR-RP02` (pass).

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `ground_truth.differential[6].icd_code` G04.81 -> G04.00: G04.81 is other encephalitis; ADEM is G04.00, as in the other 8 MS-RR cases.
- `action-3-search-medical-literature.label` "Literature search (background only)" -> "Literature search on tumefactive demyelination versus glioma": engineering text replaced by the topic of the stored output.
- `assessment.prohibited_recommendations[5]` chronic-steroid prohibition set to the condition's canonical text (was "Do not use chronic oral corticosteroids as a maintenance treatment for MS").
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders). Initial labs interpretation edited to drop the antibody results: removed "All results within reference ranges, including AQP4-IgG and MOG-IgG negative by cell-based assay and serum beta-hCG negative.".
- `action-biopsy.citations` was empty; set to `[McDonald_2024]` (the criteria require that no better explanation remains, which the biopsy settles), as on RM01's biopsy criterion. A tumefactive-specific key (Hardy and Chataway 2013) is requested under CENTRAL in the condition summary.

## Close-out (24 Oct 2026)

Condition close-out (`plans/MS-RR-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G35 entry, re-applied with `apply_diagnosis_synonyms.py --prune --conditions multiple_sclerosis`): removed the label "demyelinating disease" (G37.9 is an Excludes1 of G35.A, and its tokens occur in an NMOSD, MOGAD or ADEM answer, which would have scored as correct) and the codes G35.B and G35.C (primary and secondary progressive MS in FY2026 ICD-10-CM, a different course from this relapsing-remitting case). Accepted now: the label, multiple sclerosis, MS, relapsing(-)remitting multiple sclerosis, RRMS; codes G35.A, G35, G35.D.
- `action-perfusion`, `action-mrs` and `action-biopsy`: added `[Hardy_2013]` (Hardy TA, Chataway J. Tumefactive demyelination: an approach to diagnosis and management. JNNP 2013;84(9):1047-1053), the review that governs the work-up of a tumefactive lesion and the decision to biopsy; now in the pack's allow-list.
- Checks: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MS-RR-` passes with MS-RR now in `DISCRIMINATOR_CONDITIONS`.
