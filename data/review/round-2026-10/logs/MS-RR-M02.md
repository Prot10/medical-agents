# MS-RR-M02
Reviewer status: R1 none, R2 none (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. All changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.chief_complaint` | "bilateral leg weakness" without the right predominance the exam shows (plan R). | FIXED: "Progressive leg weakness, worse on the right, and urinary urgency over the past three weeks". |
| B | minor | `patient.clinical_history.allergies[0]` | "Contrast dye (mild reaction)" while the case requires gadolinium (plan R). | FIXED: "Iodinated CT contrast (mild urticaria)"; prohibition and red herring added that gadolinium is not barred. |
| D | major | `initial_tool_outputs.mri.findings[3]`, `.impression`, `.additional_observations` | Brain MRI reported a C3-C4 cord lesion and counted "spinal cord regions", pre-empting the spine criterion (plan H). | FIXED: cord finding deleted; lesion total 6; "Spinal cord not assessed on this study." added; numbered brain-only impression. |
| C | minor | `initial_tool_outputs.mri.findings[1].location` | "subcortical white matter" (not an MS region, F1) for the centrum semiovale lesion. | FIXED: "Right centrum semiovale, deep white matter" (not counted as a region). |
| B | minor | `initial_tool_outputs.mri.additional_observations` | "ovoid ... perpendicular ... though classic Dawson finger morphology is not definitively seen" (self-contradictory). | FIXED: hedge removed. |
| C | major | `followup_outputs` `request_repeat_mri_3months` | Future scan three months later (plan F). | FIXED: deleted. |
| B | minor | `followup_outputs[0].output` (spine MRI) | Empty lesion descriptions; a "dorsal" C3-C4 lesion does not explain right-predominant weakness and right posterior column loss. | FIXED: C3-C4 lesion right dorsolateral; T2/enhancement descriptions per lesion; impression with the same content and final period. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | Hb 11.6 g/dL with Hct 40.9% (MCHC 28) is not a coherent pair. | FIXED: Hct 35.4%, RBC 4.02, MCV 88.1 (consistent indices); Hb unchanged. |
| B | minor | `initial_tool_outputs.labs.panels` | "Autoimmune Panel" held B12, TSH and ACE; HIV row with leaked significance (plan E); no liver tests; no AQP4/MOG result for a recommended assay (A8). | FIXED: panels CBC, CMP (LFTs added), Inflammatory markers, Thyroid and vitamins, Autoimmune and infectious serology (ANA, AQP4-IgG CBA, MOG-IgG live CBA, HIV), Other (serum ACE); significance null; interpretation states the anaemia with normal MCV. |
| C | minor | `initial_tool_outputs.csf` | IgG index above range not flagged; myelin basic protein (obsolete); no kFLC; recital interpretation (plan J). | FIXED: flags, MBP deleted, kFLC 27.5 (reference < 6.1), pattern interpretation. Cells, protein, glucose, 3 OCB unchanged. |
| C | minor | `followup_outputs` OCT (new), criterion `action-oct` (new) | Library OCT would be normal and symmetric despite prior left optic neuritis with RAPD and pallor. | FIXED: OCT follow-up (left temporal pRNFL 52, GCIPL 74, inter-eye 19/11 um) and optional criterion. |
| B | minor | `followup_outputs` drug check | Empty `interactions`; a monitoring threshold filed as a contraindication (plan O). | FIXED: albuterol, ferrous sulfate, ibuprofen each "no clinically significant interaction"; lymphocyte rule moved to warnings with the label wording. |
| C | minor | `followup_outputs` literature | MAGNIMS 2021 attributed to Mult Scler J (it is Lancet Neurol); AAN guideline "reaffirmed 2023" unverified; McDonald 2017 presented as current (plan O). | FIXED: source Lancet Neurology with a correct monitoring statement; year 2018; third result is the 2024 McDonald revision (general text); summary updated. |
| B | minor | `fallback_tool_outputs.ecg`, `.echo` | ECG "borderline left-axis deviation" with `axis` normal; echo without `echo_type`. | FIXED: normal ECG text (kind "normal"); `echo_type` "TTE". |
| A | major | `ground_truth.action_criteria`, `.stop_rule`, `.sequence_constraints` | Template criteria as in the whole condition (plan A, P, 3.4). | FIXED: brain MRI, spine MRI, labs required; AQP4/MOG recommended; CSF, VEP, OCT, drug check, literature optional; literature last; required_before_assessment = the three required; max 2; soft MRI-before-CSF. |
| C | major | `ground_truth.assessment` | T0/T1/T2 musts (interpretation, a disguised test), generic relapse and lifestyle musts (smoking cessation in a never smoker); JCV and fingolimod prohibitions without a case reason (plan B, K). | FIXED: formulation, relapse (dipstick/culture first given prior UTI; stop ibuprofen or add PPI during steroids), DMT, pre-DMT screening, bladder musts; prohibitions T7, T10, T11, T12, T13 plus gadolinium/contrast allergy. |
| C | major | `ground_truth.differential` | NMOSD/MOGAD high and sarcoid moderate despite negative results; codes D86.85, G04.81 (plan C). | FIXED: all low with case results; B12 entry added; D86.89, G04.00. |
| D | major | `ground_truth.key_clinical_evidence` | Template lines (plan D). | FIXED: six observable lines; DIS 4 of 5 (no infratentorial lesion). |
| E | minor | `metadata.presentation_variant`, `.difficulty_rationale` | "first_clinical_event_with_subclinical_lesions" (she had a clinical optic neuritis); CSF and AQP4/MOG called required. | FIXED. |
| B | minor | `ground_truth.avoided_actions` | Generic rationales (plan N). | FIXED: case-tied sentences, citations per plan. |

## Changes, in one paragraph a physician can read before re-reviewing

A 28-year-old woman with three weeks of paraparesis worse on the right, a T10 sensory level, bladder urgency and Lhermitte sign, 18 months after a left optic neuritis (left RAPD and pallor). The allergy is now specified as iodinated CT contrast, so gadolinium MRI is not barred. The brain MRI no longer reports the cervical cord lesion; it shows periventricular, juxtacortical and one enhancing deep white matter lesion. The spine MRI places the enhancing C3-C4 lesion right dorsolateral (matching the right-sided signs) plus a non-enhancing T6-T7 lesion. The 3-month future MRI was deleted. Labs were regrouped (Hct corrected to match Hb 11.6; liver tests and negative AQP4-IgG/MOG-IgG CBA added). CSF adds kFLC 27.5 and drops MBP. An OCT showing chronic left optic neuropathy was added. DIS is 4 of 5 (no infratentorial lesion), so no separate DIT or CSF is needed. Pathway: brain MRI, spine MRI, labs required; AQP4/MOG recommended; CSF, VEP, OCT, drug check, literature optional. Musts: formulation, steroids after excluding UTI with an NSAID caution, DMT, pre-DMT screening, bladder; prohibitions include not withholding gadolinium. All mimics low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonym codes G35.B/G35.C and "demyelinating disease" (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea. Decision recorded: OCT follow-up and optional `action-oct` added (not in the plan's tier table) because the library's normal OCT contradicted the documented left optic neuropathy.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MS-RR; the table correctly says so.
Checked: allergy now iodinated CT contrast with a matching red herring and prohibition; cord finding removed from the brain MRI; centrum semiovale lesion not counted as a region; right dorsolateral C3-C4 lesion matches the right-predominant signs; future MRI gone; OCT and VEP fit the 18-month-old left optic neuritis (pallor appropriate); DIS 4 of 5 with no infratentorial lesion matches the report and the exam (no nystagmus); CSF kFLC added, MBP gone; drug check lists all three medicines; literature output general and correctly cited; tiers, order and stop rule per plan; musts consistent with ibuprofen (PPI/stop) and the prior UTI.
Found and fixed:
- `initial_tool_outputs.labs.panels.CBC[2]` haematocrit 35.4% was flagged normal against the 36.0-46.0 range the worker had just set: `is_abnormal` true, added to `abnormal_values_summary` and the interpretation.
- `initial_tool_outputs.csf.special_tests` IgG index 0.68 and synthesis rate 9.2 mg/day were identical to M03 (and M01): varied to 0.74 and 10.9 mg/day (still elevated; interpretation unchanged).
- The Susac entry of the differential cites "no corpus callosum lesions", which the brain MRI did not state: observation "No corpus callosum lesions on sagittal FLAIR" added to `initial_tool_outputs.mri.additional_observations`.
Checks re-run after the changes: `perfect_agent.py -v` pass, `case_io.py check` clean for the case, `test_case_guards.py -k` (leak, follow-up, banned strings) pass.

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `action-4-check-drug-interactions.expected_evidence` was empty; written from the stored drug output in policy voice: "Dimethyl fumarate with albuterol, ferrous sulfate and ibuprofen: no relevant interaction; lymphocyte monitoring for PML risk".
- `assessment.prohibited_recommendations[2]` chronic-steroid prohibition set to the condition's canonical text (was "Do not use chronic oral corticosteroids as a maintenance treatment for MS [em dash] they are ineffective long-term and carry significant harm").
- `assessment.prohibited_recommendations[4]` spinal-cord prohibition set to the condition's canonical text (was "Do not omit spinal-cord MRI in a patient with myelopathic signs even if the brain MRI alone meets DIS criteria [em dash] cord lesions change relapse counting and management").
- `assessment.required_recommendations[0]` formulation must made case-specific by appending "(here periventricular, juxtacortical and spinal cord, completed by DIT from the enhancing and non-enhancing lesions or by positive CSF, with the left optic nerve a fourth region by VEP or OCT)", from the KCE DIS line and the stored outputs, as in the other 18 cases.
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders).
- `assessment.required_recommendations[3]` pre-DMT screening: HIV removed from the tests to order and noted as already non-reactive, since the required mimic panel reports it (HIV-1/2 Ag/Ab combination assay: Non-reactive), as the RM, RP and RS cases do.
