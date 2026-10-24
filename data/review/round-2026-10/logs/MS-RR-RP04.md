# MS-RR-RP04
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.key_clinical_evidence`, `followup_outputs` | KCE cited OCT RNFL 74 um and VEP P100 124 ms that no tool ever served (class R). | FIXED: `order_specialized_test` follow-ups for OCT (right pRNFL 74 um, temporal 48 um, GCIPL 66 um; left 98/82 um) and VEP (right P100 124 ms, left 103 ms); optional criteria `action-oct` and `action-vep`. |
| B | major | `ground_truth.key_clinical_evidence[9]` | Optic nerve axonal loss "correlating with the left leg numbness 8 years ago" (an optic finding tied to a leg episode). | FIXED: KCE line on a prior subclinical right optic neuropathy; HPI now states he never noticed visual blurring, colour desaturation or eye pain. |
| E | major | `ground_truth.key_clinical_evidence` | "DIS is met across three regions", McDonald 2017 DIT as "the central insight", engineering "July 2026" lines (F2, F3). | FIXED: seven observable lines: syndrome, DIS 5 of 5 regions (no DIT needed; MRI DIT present anyway), subclinical optic neuropathy, negative CSF read per F3/F6, mimic exclusion, vascular risk, low vitamin D. |
| D | major | `initial_tool_outputs.mri.impression`, `.additional_observations` | Impression items 3-4 and an observation stated that the scan "fulfils" DIT and DIS criteria; volume loss "in keeping with age and vascular risk factors". | FIXED: numbered findings with one hedged read ("favours inflammatory demyelination"); criteria statements and the attribution removed. |
| D | minor | `followup_outputs` spine | Lesion rows with empty descriptions and type "demyelinating lesion"; impression concluded "demyelinating". | FIXED: T2 hyperintense intramedullary lesion rows with position, cross-section, enhancement; numbered impression with no-compression statement. |
| D | minor | `initial_tool_outputs.csf` | Myelin basic protein (F6); no kFLC; interpretation recital with a teaching sentence on OCB-negative MS. | FIXED: MBP deleted; kFLC index 1.9 (reference <6.1, OCB-negative case); pattern interpretation. |
| D | minor | `initial_tool_outputs.labs` | Interpretation reported AQP4-IgG and MOG-IgG negative but no rows existed. | FIXED: Neuroimmunology panel (cell-based assay rows, significance null); ESR and CRP rows for the vasculitis differential; interpretation rewritten plainly. |
| B | minor | `patient.neurological_exam.cranial_nerves` | "Facial sensation symmetric" followed by "Mild right facial numbness". | FIXED: "Mild right facial numbness to light touch in the V1-V2 distribution; corneal reflexes present". |
| A | major | `ground_truth.action_criteria` | Template criteria: literature with a 15-word query required, drug check with non-schema keys required, labs with 9 analytes, CSF needing three assays. | FIXED per plan A2-A8 and tier table: brain MRI, spine MRI, labs `[CBC, vitamin_B12, TSH, HIV]` required; `action-aqp4-mog-cba` recommended; CSF two alternatives optional; VEP, OCT, drug check `{}`, literature `{}` optional, literature last. |
| A | minor | `ground_truth.stop_rule`, `sequence_constraints` | Literature and drug check required before assessment, max 0; constraint cited McDonald 2017. | FIXED: brain MRI, spine MRI, labs; max 3; soft MRI-before-CSF with the canonical reason. |
| D | major | `followup_outputs` literature | 2017 criteria framing and a summary built around MRI DIT. | FIXED: Montalban 2025 (2024 revisions), Dobson 2013 JNNP (OCB prevalence), Wingerchuk 2015; general summary; last in the pathway. |
| C | major | `followup_outputs` drug check | "Natalizumab contraindicated in JCV positive with index >0.9", fingolimod "avoid in hypertension-related LVH" (not a label contraindication), choice of agent in `proposed`. | FIXED: ocrelizumab with amlodipine (no interaction; infusion-related hypotension, consider holding antihypertensives before infusions), penicillin allergy, HBV, immunoglobulins, live vaccines; alternatives without false claims. |
| C | major | `ground_truth.differential` | Small-vessel disease and NMOSD "moderate" after a work-up that argues against them (ruling 7); "OCB-negative CSF does not favour sarcoidosis" (wrong direction); Lyme "no tick exposure" not in the history. | FIXED: all low with the case's results; compressive myelopathy (prior disc diagnosis) and B12 myelopathy added; Lyme notes Finland is endemic. |
| C | major | `ground_truth.assessment.required_recommendations` | Diagnostic and interpretive musts (DIS, DIT, OCB, AQP4 test, spinal MRI, ANA); generic IVMP; vitamin D target as a "risk factor". | FIXED: formulation must; relapse treatment (IV or oral high-dose methylprednisolone after excluding infection); DMT by activity; pre-DMT screening; vitamin D replacement; Uhthoff counselling (reported). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Natalizumab JCV (no anti-JCV result) and fingolimod ECG (no cardiac reason) prohibitions. | FIXED: deleted; OCB, ANA and small-vessel prohibitions reworded to the case; T7, T11, T12, T13 (myelopathic signs) kept. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales; McDonald 2017, MAGNIMS 2016, Reich 2018 citations. | FIXED: case-tied rationales; `[Wattjes_2021]` for CT and PET, none for EEG, echo, monitoring. |
| B | minor | `ground_truth.red_herrings` | McDonald 2017 framing; the old disc diagnosis, which the HPI builds up as a distractor, not listed. | FIXED: three red herrings rewritten to the 2024 framing; fourth on `patient.clinical_history.past_medical_history[1]`. |
| B | minor | `metadata.difficulty_description`, `difficulty_rationale` | Built on McDonald 2017 MRI DIT. | FIXED: rewritten around five-region DIS and the distractors. |
| E | minor | `fallback_tool_outputs.echo` | `echo_type` missing. | FIXED: `TTE`. |
| E | minor | CSF `special_tests`, exam `additional`, `cranial_nerves` | Em dashes. | FIXED: replaced. |

## Changes, in one paragraph a physician can read before re-reviewing

The case now rests on the 2024 McDonald criteria. Lesions are in five regions: periventricular, right parietal juxtacortical, infratentorial (right dorsal pons at the MLF, which explains the right INO, and left cerebellum), spinal cord (C5-C6 and T4-T5), and the right optic nerve. The OCT (right pRNFL 74 um) and VEP (right P100 124 ms) that the evidence cited are now served as studies, and they document a subclinical right optic neuropathy that he never noticed. Five regions establish dissemination in space without dissemination in time, so the negative oligoclonal bands and the low kFLC index (1.9) do not count against the diagnosis. The MRI reports describe findings only. AQP4/MOG cell-based assays are now real lab rows (recommended). Required: brain MRI, spine MRI and mimic labs. CSF, VEP, OCT, drug check and literature are optional. The musts are diagnosis by the 2024 criteria naming the five regions, high-dose methylprednisolone for the relapse after excluding infection, high-efficacy DMT by activity, pre-DMT screening, vitamin D replacement and Uhthoff counselling. The natalizumab and fingolimod prohibitions had no basis in this patient and are gone. The differential keeps small-vessel disease, NMOSD, MOGAD, lupus/vasculitis, sarcoidosis and Lyme, all low with reasons, and adds compressive and B12 myelopathy. The old disc diagnosis is now an explicit red herring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]`, `[Petzold_2017]` to the MS-RR criteria pack (plan 5.1).
- Diagnosis synonyms: G35.B/G35.C and "demyelinating disease" (plan Q, 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea's information. Decided: the exam keeps "No relative afferent pupillary defect" despite a 24 um inter-eye pRNFL difference, since a mild asymmetry can leave the swinging-flashlight test equivocal; change it to "subtle right RAPD" if you prefer. The left leg numbness 8 years ago is treated as a possible but undocumented earlier event, not as a counted attack.
