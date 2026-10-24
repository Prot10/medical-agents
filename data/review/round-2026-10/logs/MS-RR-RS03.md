# MS-RR-RS03
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.cranial_nerves` | "Mild pallor of the right optic disc" at day 4 of a first optic neuritis: pallor appears after 4-6 weeks (F7); the MRI shows an intraorbital/intracanalicular (retrobulbar) lesion. | FIXED: "right optic disc normal, without swelling or pallor; left optic disc normal". |
| C | major | `followup_outputs[request_optical_coherence_tomography].output` | OCT at day 4 showed right pRNFL 68 and GCIPL 64 (established thinning, impossible this early without a prior episode in that eye); rows had no eye labels and "(L)" flags read as left eye; quantitative block gave one eye only. | FIXED: canonical acute report, both eyes labelled (right pRNFL 104, GCIPL 81; left 98, 84; inter-eye GCIPL difference 3 µm); impression "no RNFL or GCIPL thinning"; GCIPL reference 70-90. |
| B | minor | `patient.history_present_illness`, `patient.neurological_exam.additional` | Heat-triggered worsening of vision described as an established phenomenon although the right eye has been affected for 4 days only (Uhthoff follows a prior optic neuropathy); "only vague outlines visible" is worse than the measured 20/70. | FIXED: the heat-triggered worsening now concerns the residual leg symptoms of the earlier myelitis (HPI and exam); "with only vague outlines visible" removed. |
| D | major | `initial_tool_outputs.mri.findings[5]`, `.additional_observations[2]`, `.impression`, `.volumetrics` | Brain MRI reported a C2-C3 cord lesion, "No longitudinally extensive transverse myelitis" and "spinal cord distributions" in the impression (plan H). | FIXED: cord finding and LETM line removed; "Spinal cord not assessed on this study."; count "16 supratentorial, 2 infratentorial"; numbered impression (optic nerve, brain regions, enhancement). |
| B | minor | `initial_tool_outputs.mri.findings[2].location` | "Right middle cerebellar peduncle and left brachium pontis": the brachium pontis is the middle cerebellar peduncle. | FIXED: "Right and left middle cerebellar peduncles (infratentorial)". |
| C | major | `followup_outputs[request_repeat_mri_3months]` | Future 3-month MRI, which also reported a "prior" right optic nerve lesion as resolving (plan F). | FIXED: deleted. |
| C | minor | `followup_outputs[search_mcdonald_criteria_2017]`, `[search_nmosd_vs_ms_differentiation]` | 2017 criteria as current; second output cites a Cacciaguerra and Flanagan 2023 Nature Reviews Neurology title that could not be verified. | FIXED: one general follow-up (`search_ms_diagnostic_criteria`, last) with the canonical 2024 text, Montalban 2025, Wattjes 2021, Wingerchuk 2015. |
| A | major | `ground_truth.action_criteria[action-6]` | Labs criterion demanded 11 analytes, AQP4/MOG embedded (plan A7, A8). | FIXED: labs `{panels: [CBC, vitamin_B12, TSH, HIV]}`; new `action-aqp4-mog-cba` recommended (optic neuritis plus myelopathy, no red flag). |
| B | minor | `initial_tool_outputs.labs.panels["Autoimmune panel"]` | AQP4 row labelled "NMO-IgG (Aquaporin-4 antibodies)" and "MOG antibodies" with no assay method (plan B). | FIXED: moved to "Neuroimmunology" as "AQP4-IgG (cell-based assay)" and "MOG-IgG (live cell-based assay)", negative. ANA stays in the autoimmune panel. |
| A | major | `ground_truth.action_criteria[action-3]`, `[action-4]`, `[action-5]` | Literature and drug check required (typed query, non-schema keys); CSF required three assays together. | FIXED: literature and drug check optional with `{}`; CSF optional with OCB or kFLC alternatives; soft MRI-before-CSF constraint with canonical reason. |
| A | minor | `ground_truth.action_criteria[action-7]`, `[action-8]` | VEP and OCT labels/rationales generic ("this optic-neuritis or equivocal-dissemination question"); free-text citations. | FIXED: optional kept; specific rationales; citations VEP `[McDonald_2024]`, OCT `[Petzold_2017]`, `[McDonald_2024]`. |
| A | minor | `ground_truth.action_criteria[*]`, `.stop_rule` | Label equals rationale; stop rule 0 with literature and drug check. | FIXED: canonical labels; pathway order brain MRI, spine, labs, AQP4/MOG, CSF, VEP, OCT, drug, literature (follow-ups in the same order); stop rule brain MRI, spine, labs, allowance 2. |
| B | minor | `followup_outputs[0].output` (spine) | Empty lesion descriptions. | FIXED: descriptions; numbered impression. |
| C | major | `initial_tool_outputs.csf` | Myelin basic protein (F6); no kFLC; WBC 12, protein 48, 5 bands, IgG index 0.78, synthesis 10.8, MBP 5.2 identical to RS01/RS02 (template carry-over); HSV PCR and West Nile IgM/IgG in an afebrile woman with no encephalitis (not indicated); "(traumatic tap excluded)" for 1 RBC; recital interpretation. | FIXED: WBC 6, protein 41, 4 bands, IgG index 0.84, synthesis 11.6, kFLC 42.5 (reference < 6.1); MBP, HSV and WNV removed (VDRL and cytology kept); canonical interpretation. |
| D | minor | `initial_tool_outputs.labs.panels["Mimic exclusion"]` | HIV row with leaked significance. | FIXED: panel "Serology", significance null. |
| B | minor | vitamin D row, summary, interpretation, `red_herrings[0]` | 18 ng/mL copied across cases. | FIXED: 13 ng/mL wherever it appears (16 is used by RS05). |
| C | minor | `followup_outputs[check_drug_interactions].output` | Ocrelizumab "300 mg IV initial dose" (the first dose is two 300 mg infusions 2 weeks apart); empty `interactions` list; PML "lower than with natalizumab" comparison. | FIXED: correct dosing; albuterol, montelukast, acetaminophen and the sulfonamide allergy listed; PML stated as rare. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts, AQP4 test as a must, no urinary check before steroids despite urinary frequency, no bladder management. | FIXED: formulation must (two attacks, five regions); optic neuritis steroid must with urine dipstick first and the NICE statement that steroids speed recovery only; post-void residual; Uhthoff counselling; DMT with pregnancy planning; pre-DMT screening; vitamin D. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | T8 and T9 without case trigger. | FIXED: deleted; kept T7, T10, T11, T12, T13; added "Do not attribute the earlier bilateral leg numbness to lumbar radiculopathy". |
| C | major | `ground_truth.differential` | NMOSD/MOGAD high, neurosarcoidosis moderate (ACE normal) after the work-up; no lupus entry despite ANA row and SLE family history; no B12 entry in a myelopathy. | FIXED: all low with discriminating results; lupus (M32.19) and B12 myelopathy (E53.8) added. |
| E | major | `ground_truth.key_clinical_evidence` | Engineering lines, F2/F5 wrong facts, tumefactive/ELISA/DMT/vitamin D template lines. | FIXED: six case-observable lines. |
| D | minor | `ground_truth.red_herrings` | The case's real distractor (prior attack labelled radiculopathy) not recorded. | FIXED: second red herring at `patient.clinical_history.past_medical_history[0]`. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales and citations. | FIXED: case-tied; `[Wattjes_2021]` for CT and PET. |
| E | minor | `fallback_tool_outputs.echo` | No `echo_type`. | FIXED: `TTE`. |
| E | minor | `metadata.mcdonald_criteria_met`, `.difficulty_*`, `.educational_value` | "2017 McDonald ... all 4 regions"; "source case context" engineering phrase. | FIXED: 2024 wording (5 of 5 regions). |

## Changes, in one paragraph a physician can read before re-reviewing

A 37-year-old woman with day-4 right optic neuritis (20/70, RAPD) and residual signs of a sensory myelitis 8 months ago that was called radiculopathy. The right disc is now normal (no pallor at day 4) and the OCT is the acute form with both eyes labelled and no thinning; the VEP (right P100 134 ms) is unchanged. The heat-triggered worsening now concerns her legs, not the newly affected eye. The brain MRI reports the right optic nerve and brain only (cord not assessed); the three short cord lesions (C2-C3, T4-T5 faintly enhancing, T9) are in the spine report. The 3-month repeat MRI is gone. CSF values are no longer copied (4 bands, kFLC 42.5), without MBP, HSV or West Nile tests. AQP4-IgG and MOG-IgG by CBA are negative under their own criterion (recommended). Musts: RRMS by two attacks and five regions; methylprednisolone after a urine dipstick; bladder residual; Uhthoff counselling; DMT with pregnancy planning; pre-DMT screening; vitamin D 13. All mimics low, with lupus and B12 added; the radiculopathy label is a red herring and a prohibition.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan CENTRAL 1).
- Diagnosis synonyms G35.B/G35.C and "demyelinating disease" (plan CENTRAL 2); not hand-edited.

## Open questions for Andrea (judgment calls you could not settle)

None. The VEP latency reference (< 102 ms) is used consistently within this report, so it was kept (plan RS03 bullet); the interocular reference (< 6 ms) is strict but not wrong and the 37 ms difference is abnormal under any laboratory's limit.

## Verification

`perfect_agent.py MS-RR-RS03 -v`: pass; brain MRI <- initial MRI, spine <- `followup[0]`, labs and AQP4/MOG <- initial labs (expected shared-report warning). Probes: `vep` returns the VEP follow-up, `optical_coherence_tomography` the OCT follow-up, CSF the initial CSF. Brain MRI output has no cord lesion text. `case_io.py check`: schema and synonym guard OK, no failure naming MS-RR-RS03. `test_case_guards.py -k MS-RR-RS03`: 2 passed.

## Verification (adversarial verifier, 24 Oct 2026)

Checked against the committed worker version (b8be2153): every own-finding row against the case file (field by field read of the whole final case), the plan tier table (section 3.5), the stop rule, the sequence constraint, laterality and lesion-to-exam fit, timeline, allergies against drug outputs, leakage in the brain MRI (no cord text) and the literature/drug outputs (guards pass), PATTERNS classes (template numbers across RS01-RS06, 2017 facts, test-as-must, F2/F5 wrong facts), and the differential against the final results. No reviewer notes exist for MS-RR, so no note id can be missing. Re-run after the changes below: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards.py -k` pass.

Found: (1) the spine report kept the original faint enhancement of the T4-T5 lesion, while the worker's new red herring names that bilateral posterior-column lesion as the cause of the sensory myelitis 8 months ago; gadolinium enhancement lasts weeks, so the lesion of an 8-month-old attack cannot still enhance. Fixed by making T4-T5 non-enhancing in the spine findings and impression and in everything that repeated it: `action-2` expected_evidence, KCE[3] (DIT now from the right optic nerve and the open-ring periventricular lesion, which still enhance), must[4] ("enhancing optic nerve and brain lesions"), and the B12 differential ("focal asymmetric short cord lesions"). (2) Vitamin B12 512 pg/mL was identical in RS02, RS03 and RS04 (template carry-over): RS03 now 446 pg/mL, also in the B12 differential entry. Note for the re-reviewer: the worker's changes paragraph above still says "T4-T5 faintly enhancing"; that is superseded.

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `ground_truth.differential[2].icd_code` D86.85 -> D86.89: D86.85 is sarcoid myocarditis; neurosarcoidosis is D86.89, as in the other 11 MS-RR cases.
- `ground_truth.differential[6].icd_code` G04.81 -> G04.00: G04.81 is other encephalitis; ADEM is G04.00, as in the other 8 MS-RR cases.
- `action-3-search-medical-literature.label` "Literature search (background evidence only)" -> "Literature search on the MS diagnostic criteria and NMOSD": engineering text replaced by the topic of the stored output.
- `assessment.prohibited_recommendations[3]` chronic-steroid prohibition set to the condition's canonical text (was "Do not use chronic oral corticosteroids as a maintenance treatment for MS [em dash] they are ineffective long-term and carry significant harm").
- `assessment.prohibited_recommendations[5]` spinal-cord prohibition set to the condition's canonical text (was "Do not omit spinal-cord MRI in a patient with myelopathic signs even if the brain MRI alone meets DIS criteria [em dash] cord lesions change relapse counting and management").
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders).
