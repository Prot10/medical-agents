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

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff against `b8be2153^` and the whole final case. Checked: OCT and VEP follow-ups exist with both eyes and match the KCE and expected evidence; the leg-episode/optic-finding mix-up is gone; brain MRI impression has no criteria statements; five-region DIS is correctly stated and the negative CSF (OCB negative, kFLC 1.9) is framed per F3/F6; INO side, diplopia direction (worse on left gaze) and the right dorsal pontine lesion agree; right facial numbness contradiction fixed; smoking dates consistent (quit at 40 = 7 years ago); no T10 in a man; ocrelizumab drug output (antihypertensive withholding before infusion, premedication, HBV, immunoglobulins, live vaccines) correct per label; Dobson 2013 JNNP and other sources exist; differential all low with reasons.
Found and fixed:
- B minor, `patient.neurological_exam.cranial_nerves`, `ground_truth.key_clinical_evidence[2]`: the worker left as an open question "No relative afferent pupillary defect" despite right temporal pallor, 20/25 acuity, an inter-eye pRNFL difference of 24 um and GCIPL difference of 16 um. An asymmetry of that size from a prior optic neuropathy normally gives a detectable RAPD, so the exam now reads "Subtle right relative afferent pupillary defect" and the KCE line on the prior subclinical optic neuropathy names it. The open question is resolved; nothing is left for Andrea.
Re-ran `perfect_agent.py MS-RR-RP04 -v` (pass), `case_io.py check` (clean for the case) and `test_case_guards -k MS-RR-RP04` (pass).

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `ground_truth.differential[4].icd_code` D86.85 -> D86.89: D86.85 is sarcoid myocarditis; neurosarcoidosis is D86.89, as in the other 11 MS-RR cases.
- `action-3-search-medical-literature.label` "Literature search (background only)" -> "Literature search on oligoclonal band-negative MS": engineering text replaced by the topic of the stored output.
- `assessment.prohibited_recommendations[4]` chronic-steroid prohibition set to the condition's canonical text (was "Do not use chronic oral corticosteroids as a maintenance treatment for MS").
- `assessment.prohibited_recommendations[6]` spinal-cord prohibition set to the condition's canonical text (was "Do not omit spinal-cord MRI in a patient with myelopathic signs even if the brain MRI alone meets DIS criteria").
- `followup_outputs` literature result title of Dobson 2013 corrected to the published title ("a meta-analysis of prevalence, prognosis and effect of latitude"), as in P02 and P03.
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders). Initial labs interpretation edited to drop the antibody results: removed "AQP4-IgG and MOG-IgG negative by cell-based assay.".

## Close-out (24 Oct 2026)

Condition close-out (`plans/MS-RR-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G35 entry, re-applied with `apply_diagnosis_synonyms.py --prune --conditions multiple_sclerosis`): removed the label "demyelinating disease" (G37.9 is an Excludes1 of G35.A, and its tokens occur in an NMOSD, MOGAD or ADEM answer, which would have scored as correct) and the codes G35.B and G35.C (primary and secondary progressive MS in FY2026 ICD-10-CM, a different course from this relapsing-remitting case). Accepted now: the label, multiple sclerosis, MS, relapsing(-)remitting multiple sclerosis, RRMS; codes G35.A, G35, G35.D.
- Checks: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MS-RR-` passes with MS-RR now in `DISCRIMINATOR_CONDITIONS`.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-6-interpret-labs]`.alternatives: was [CBC, vitamin_B12, TSH, HIV]; now [CBC, vitamin_B12, TSH, HIV, inflammatory_markers, anti_dsDNA] | [CBC, vitamin_B12, TSH, HIV].
- Decision: serve: new first alternative (old order kept as an alternative). The evidence reads the ESR, CRP, anti-dsDNA and anti-Smith, which the differential relies on (neuropsychiatric lupus or CNS vasculitis, a red herring); CBC, B12, TSH and HIV did not return them. Same decision as MS-RR-P03.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
