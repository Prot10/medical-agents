# MS-RR-RS02
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.mri.findings[3]`, `[5]`, `.additional_observations[2]`, `.impression`, `.volumetrics` | Brain MRI reported thoracic T9-T10 and cervical C2-C3 cord lesions (a thoracic cord lesion is outside any brain field of view) and "No longitudinally extensive transverse myelitis": it showed the result of the spine study the agent must order (plan H). | FIXED: both cord findings and the LETM line removed; observation "Spinal cord not assessed on this study."; lesion count "12 supratentorial, 1 infratentorial"; numbered brain-only impression. The cord lesions live only in the spine follow-up. |
| C | major | `followup_outputs[request_repeat_mri_3months]` | Future 3-month MRI with a new lesion (plan F). | FIXED: deleted. |
| C | minor | `followup_outputs[search_mcdonald_criteria_2017]`, `[search_nmosd_vs_ms_differentiation]` | Two literature outputs: 2017 criteria presented as current; a second citing "Cacciaguerra L, Flanagan EP, Contemporary Clinical Neuroscience 2024", which could not be verified as cited. | FIXED: one general follow-up (`search_ms_diagnostic_criteria`, last) with the canonical 2024 text, Montalban 2025, Wattjes 2021 and Wingerchuk 2015 (NMOSD criteria, worded as the paper states them). |
| B | minor | `patient.neurological_exam.sensory` | Pinprick loss in the left leg ipsilateral to a left dorsal-column cord lesion (spinothalamic fibres cross; a left lesion gives right-sided pain loss), while the exam already records intact temperature sensation. | FIXED: "Decreased light touch over the left lower extremity from the knee distally; pinprick intact." (dorsal column plus corticospinal, ipsilateral, matching the lesion). |
| A | major | `ground_truth.action_criteria[action-3]`, `[action-4]` | Literature required with a typed query; drug check required with non-schema keys (plan A4, A5). | FIXED: both optional, `required_arguments {}`, after the diagnostic core, out of the stop rule. |
| A | major | `ground_truth.action_criteria[action-6]`, `[action-5]` | Labs demanded 9 analytes; CSF demanded three assays together. | FIXED: labs `{panels: [CBC, vitamin_B12, TSH, HIV]}`; CSF two alternatives (OCB or kFLC), optional (two attacks, four regions). Soft MRI-before-CSF constraint with the canonical reason. |
| C | major | `ground_truth.action_criteria`, `initial_tool_outputs.labs` | No AQP4/MOG criterion or result, while a must asked for the test (plan B). | FIXED: `action-aqp4-mog-cba` recommended (optic neuritis plus myelitis, no red flag); "Neuroimmunology" rows negative by CBA; test-as-must deleted. |
| A | minor | `ground_truth.action_criteria[*]`, `.stop_rule` | Label equals rationale; free-text citations; stop rule 0 with literature and drug check required. | FIXED: canonical labels, case-specific rationales, bracketed keys; order brain MRI, spine, labs, AQP4/MOG, CSF, drug, literature; stop rule brain MRI, spine, labs, allowance 2. |
| B | minor | `followup_outputs[0].output` (spine) | Empty lesion descriptions; the mild focal swelling of the T9-T10 lesion was only in the brain report. | FIXED: descriptions with position, cross-section, enhancement and swelling; numbered impression. |
| C | major | `initial_tool_outputs.csf` | Myelin basic protein reported (F6); no kFLC; "(N/A PMN/N/A lymph)" recital; "1 cell/microL (traumatic, not significant)"; WBC 12, 5 bands, IgG index 0.78 and synthesis 10.8 identical to RS01 (template carry-over). | FIXED: MBP deleted; kFLC 18.7 (reference < 6.1); WBC 9, 7 bands, IgG index 0.91, synthesis 13.2; RBC "1 cell/microL"; canonical pattern interpretation. |
| D | minor | `initial_tool_outputs.labs.panels["Mimic exclusion"]` | HIV row with leaked significance text. | FIXED: panel "Serology", significance null. |
| B | minor | `initial_tool_outputs.labs.panels.Other[2]`, summary, interpretation, `red_herrings[0]` | Vitamin D 18 ng/mL copied across cases. | FIXED: 24 ng/mL wherever it appears. |
| C | major | `followup_outputs[check_drug_interactions].output` | Ocrelizumab "300 mg every 6 months" (wrong); empty `interactions` list; TB screening stated as required. | FIXED: correct dosing; each medicine (ibuprofen, COC, ferrous sulfate) and the sulfonamide allergy listed with no relevant interaction; HBV screening, vaccine timing and contraception kept. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts (DIS/DIT interpretation, AQP4 test as a must, IV-only steroid, generic lifestyle); no infection check despite urinary urgency; no bladder management; NSAID during steroids not addressed. | FIXED: formulation must (two attacks, four regions); steroid must with urine dipstick first, stop ibuprofen and consider PPI, PLEX if refractory; post-void residual and antimuscarinic or catheterisation; Uhthoff counselling (reported); DMT must with pregnancy and contraception clause; pre-DMT screening (F11); vitamin D replacement. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | T8 natalizumab/JCV and T9 fingolimod prohibitions with no case trigger. | FIXED: deleted; kept T7, T10 (woman of child-bearing potential), T11, T12, T13 (myelopathic signs); added "Do not treat heat-triggered transient blurring (Uhthoff phenomenon) as a new relapse requiring further steroids". |
| C | major | `ground_truth.differential` | NMOSD and MOGAD "high", neurosarcoidosis "moderate" after a work-up that excludes them; no B12 entry in a myelopathy; no lupus entry despite an ANA row. | FIXED: all low with the case's discriminating results; B12 deficiency myelopathy (E53.8) and CNS lupus (M32.19) added. |
| E | major | `ground_truth.key_clinical_evidence` | Engineering lines, F2 and F5 wrong facts, tumefactive, ELISA, DMT-choice and vitamin D template lines. | FIXED: six case-observable lines (myelitis and lesion, prior optic neuritis, DIS 4 of 5, DIT, AQP4/MOG negative with short lesions, bladder and Uhthoff). |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales; citations that do not govern. | FIXED: case-tied rationales; `[Wattjes_2021]` for CT and PET. |
| E | minor | `fallback_tool_outputs.echo` | No `echo_type`. | FIXED: `TTE`. |
| E | minor | `metadata.difficulty_rationale` | "McDonald 2017". | FIXED: 2024 wording. |

## Changes, in one paragraph a physician can read before re-reviewing

A 27-year-old woman with a left T9-T10 myelitis eight months after a right optic neuritis. The brain MRI now reports the brain only (periventricular, left frontal and right parietal juxtacortical, right MCP/dorsal pontine lesions; one open-ring enhancing left periventricular lesion) and says the cord was not assessed; the cord lesions (enhancing left dorsal T9-T10 with mild swelling, non-enhancing dorsal C2-C3) are in the spine MRI alone. The 3-month repeat MRI is gone. The sensory exam no longer has ipsilateral pinprick loss. CSF: 7 restricted bands, kFLC 18.7, no MBP, values no longer copied from RS01. Labs add negative AQP4-IgG/MOG-IgG by CBA; vitamin D 24 ng/mL. Pathway: brain MRI, spine MRI, labs (required), AQP4/MOG (recommended), CSF, drug check (ocrelizumab dose corrected, each medicine listed) and literature (optional). Musts: RRMS by two attacks and four regions; steroids after a urine dipstick, stopping ibuprofen; bladder residual; Uhthoff counselling; DMT with pregnancy planning; pre-DMT screening; vitamin D. All mimics are low with the results that exclude them.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan CENTRAL 1).
- Diagnosis synonyms G35.B/G35.C and "demyelinating disease" (plan CENTRAL 2); not hand-edited.

## Open questions for Andrea (judgment calls you could not settle)

None. One deviation from the plan's per-case line, decided on the criteria: the plan counts DIS as 5 regions including the optic nerve. In the 2024 criteria the optic nerve counts as a DIS region when shown by MRI, OCT or VEP, and this case serves none of them (plan tier table: no VEP or OCT for RS02). The KCE therefore counts 4 MRI regions and records the optic neuritis as the prior clinical attack with objective residual signs. The diagnosis does not change (two attacks and four regions).

## Verification

`perfect_agent.py MS-RR-RS02 -v`: pass; brain MRI <- `initial_tool_outputs.mri`, spine <- `followup[0] request_spine_mri`, labs and AQP4/MOG <- `initial_tool_outputs.labs` (expected shared-report warning). Brain MRI output contains no T9, C2 or cord lesion text. `case_io.py check`: schema and synonym guard OK, no failure naming MS-RR-RS02. `test_case_guards.py -k MS-RR-RS02`: 2 passed.
