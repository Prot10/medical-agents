# MS-RR-P05
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. All changes below are own findings and the condition plan (plans/MS-RR.md). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations[3]` | Must asked to "exclude NMOSD and MOGAD with AQP4-IgG and MOG-IgG ... negative here" while the case stored no AQP4/MOG result and no criterion ordered it (plan B). | FIXED: must deleted; AQP4-IgG (cell-based) and MOG-IgG (live cell-based) rows added to `initial_tool_outputs.labs`, negative; new recommended criterion `action-aqp4-mog-cba`. |
| B | major | `initial_tool_outputs.mri` | Impression counted four enhancing lesions while the middle cerebellar peduncle finding also enhanced (five); lesion count "14 supratentorial and 1 infratentorial" against 13 + 1 in the findings; "right temporal optic nerve"; impression closed with a differential essay ("tumefactive or vasculitic process cannot be fully excluded"); LP recommendation. | FIXED: MCP lesion non-enhancing (four enhancing, as everywhere else in the case); count 14 (13 + 1); "right retrobulbar optic nerve"; impression findings only with a within-imaging read; `recommended_actions` emptied. |
| A | major | `initial_tool_outputs.csf` | Meningitis boilerplate (Gram stain, bacterial culture "Pending") in an afebrile patient; obsolete myelin basic protein; no kFLC; recital interpretation with em dashes. | FIXED: Gram stain, culture and MBP deleted; kFLC index 64.2 (reference < 6.1) added; pattern interpretation. VDRL kept (syphilis mimic). |
| C | major | `followup_outputs` drug check | Claimed no interaction between the combined oral contraceptive and cladribine (the label requires an added barrier method); no line for ibuprofen with the high-dose steroid the relapse needs; inaccurate live-vaccine window; alternatives list arguing the DMT choice; PML figures. | FIXED: methylprednisolone added to `proposed`; ibuprofen GI risk, COC with steroid (no efficacy loss), COC with cladribine (barrier method), anti-CD20/natalizumab lines; contraindications and warnings corrected; alternatives empty. |
| C | major | `followup_outputs` literature | Unverifiable source ("Multiple Sclerosis Journal 2016; Lancet Neurology 2012"), a "highly active" definition attributed to ECTRIMS 2018 that the guideline does not give, specific PML ratios, NEDA-3 as target, management prescription in the summary. | FIXED: ECTRIMS/EAN 2018 (Montalban, Mult Scler 2018) with what it says, Ho 2017 Lancet Neurol on JCV index and duration, McDonald 2024; general summary. Placed last. |
| A | major | `ground_truth.action_criteria` | Template: label = rationale; literature and drug check required with non-schema keys; labs 9 analytes; CSF three assays together; no AQP4/MOG criterion. | FIXED per plan A: brain MRI, spine MRI, labs required; AQP4/MOG recommended; CSF optional (OCB or kFLC); drug optional; literature optional last. |
| A | minor | `ground_truth.stop_rule`, `sequence_constraints` | Literature and drug check required before assessment, max 0; constraint reason and 2017 citation. | FIXED: required criteria only, max 3; canonical soft MRI-before-CSF. |
| C | major | `ground_truth.assessment.required_recommendations` | DIS/DIT recitals; JCV "obtain" must although the result is in the labs; specialist consult as a must on its own; pregnancy counselling with "ocrelizumab limited data"; no bladder management; no infection check before steroids despite urgency. | FIXED: formulation (5 of 5 regions, two earlier attacks), IVMP after urine check with NSAID/PPI precaution and PLEX if refractory, PVR-guided bladder management, high-efficacy DMT via the specialist team preferring anti-CD20 over natalizumab (index 2.84), use of the completed pre-treatment serology, vitamin D dose adjustment. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | "Do not omit anti-JCV testing before any DMT decision" (it matters for natalizumab only, and is already done); em dashes. | FIXED: deleted; added functional-attribution prohibition; others reworded. |
| C | major | `ground_truth.differential` | ADEM "moderate" despite three attacks and no encephalopathy; "tumefactive demyelinating disease" (an MS variant, not a mimic); neurosarcoidosis "ACE normal on labs panel" with no ACE in the labs. | FIXED: ADEM low; tumefactive entry removed; sarcoid features from the case; functional neurological disorder (raised by the history) added low; NMOSD/MOGAD key features from the CBA results. |
| C | major | `ground_truth.key_clinical_evidence` | NEDA-3 and DMT-choice lines (management), engineering lines, OCB "fulfil the DIT criterion". | FIXED: rebuilt per plan D (attacks, DIS 5 of 5, activity, CSF, antibodies, JCV, ADEM/vasculitis). |
| D | minor | `initial_tool_outputs.labs` | Panel named "Mimic_exclusion_and_pre_DMT_serology"; values with em dashes. | FIXED: panel `Endocrine_vitamins_and_serology`; "Positive, index 2.84", "Positive (immune)"; interpretation includes the hedged antibody comment. |
| B | minor | `followup_outputs[0]` spine | Enhancement status only in the impression; no measurements. | FIXED: per-lesion descriptions and measurements; impression numbered. |
| B | minor | `ground_truth.red_herrings` | Em dashes; "≥4/≥14" wording. | FIXED: reworded; added the "functional overlay" label as a red herring. |
| C | minor | `ground_truth.avoided_actions` | Template rationales and citations. | FIXED: case-tied rationales; `[Wattjes_2021]` for CT and PET. |
| A | minor | `fallback_tool_outputs.echo.echo_type` | Missing discriminator value. | FIXED: "TTE". |
| E | minor | `metadata.difficulty_rationale` | "6 required tools". | FIXED; revision fields updated. |

## Changes, in one paragraph a physician can read before re-reviewing

A 24-year-old woman with a third attack in 18 months (right optic neuritis with residual pallor, left leg episode labelled functional, now a right-predominant myelopathy with T8 band, bladder urgency and Lhermitte sign), a mother with MS, an oral contraceptive and ibuprofen, and an anti-JCV index of 2.84. The brain MRI now consistently reports 14 lesions with four enhancing, and right retrobulbar optic nerve T2 signal, without a differential essay; DIS is 5 of 5 regions. The CSF lost its meningitis boilerplate and MBP and gained a kFLC index of 64.2. AQP4-IgG and MOG-IgG results now exist (negative, cell-based) and are scored by their own recommended criterion. Required: brain MRI, spine MRI, mimic labs; CSF, drug check and literature optional. Musts: formulation with both earlier attacks, IVMP after a urine check with NSAID precaution, bladder management, high-efficacy therapy preferring an anti-CD20 antibody over natalizumab because of the JCV index, use of the completed pre-treatment serology, vitamin D adjustment. The drug check now flags ibuprofen with the steroid pulse and the barrier method needed with cladribine on a COC. ADEM was lowered and functional disorder added as a low alternative.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonyms (plan 5.2).
- `test_guidance_claims`: P05 now has `action-aqp4-mog-cba` (plan 5.3).

## Open questions for Andrea (judgment calls you could not settle)

None. Decided: the middle cerebellar peduncle lesion was made non-enhancing (rather than raising the count to five) so the impression, the KCE and the plan's "4 enhancing" agree; this changes no region count.

## Verification

Adversarial verifier, 24 Oct 2026. Read the whole final case. Confirmed: lesion count 14 = 9 periventricular + 2 juxtacortical + 2 callosal + 1 MCP (13 supratentorial + 1 infratentorial); four enhancing lesions in findings, impression, KCE and must; optic nerve region by MRI T2 signal; three attacks in 18 months consistent across HPI, PMH, KCE and musts; CSF boilerplate and MBP gone, glucose ratio 61/82 = 0.74 matches the CMP; AQP4/MOG rows present and neutral; JCV index 2.84 drives the anti-CD20 preference and the natalizumab prohibition; pre-treatment serology rows exist for the must that uses them; cladribine contraception lines match the SmPC (barrier method during treatment and 4 weeks after the last dose in each treatment year; effective contraception 6 months); ECTRIMS/EAN 2018 and Ho 2017 citations exist as cited; NEDA/DMT lines gone from the KCE.

Found and changed:
- `followup_outputs[0].output.findings[0].location` and `.impression`: the enhancing, swollen C3-C4 lesion (the active lesion of a right-predominant myelopathy with right Babinski and right vibration loss) had no side. Now "right dorsolateral", matching the ipsilateral pyramidal and dorsal-column signs. No count, region or criterion changes.

Not changed: the patchy right thigh/shin pinprick reduction is a multifocal sensory finding, not a hemicord level, and does not contradict the report.

perfect_agent.py -v: pass. case_io.py check: clean for this case. Guards: pass.

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `ground_truth.differential[2].icd_code` G04.81 -> G04.00: G04.81 is other encephalitis; ADEM is G04.00, as in the other 8 MS-RR cases.
- `ground_truth.differential[5].icd_code` D86.85 -> D86.89: D86.85 is sarcoid myocarditis; neurosarcoidosis is D86.89, as in the other 11 MS-RR cases.
- `fallback_tool_outputs.drug_interactions.general.proposed` "(agent not specified on this case's pathway)" -> "Not specified": engineering wording, harmonised with the S cases.
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders). Initial labs interpretation edited to drop the antibody results: removed "AQP4-IgG and MOG-IgG not detected by cell-based assay; a negative result does not entirely exclude NMOSD or MOGAD.".

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

- `ground_truth.action_criteria[action-6-interpret-labs]`.alternatives: was [CBC, vitamin_B12, TSH, HIV]; now [CBC, vitamin_B12, TSH, HIV, inflammatory_markers] | [CBC, vitamin_B12, TSH, HIV].
- Decision: serve: new first alternative (old order kept as an alternative). The evidence reads the ESR and CRP, which the differential relies on (inflammatory mimics); CBC, B12, TSH and HIV did not return them. Same decision as MS-RR-P03.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
