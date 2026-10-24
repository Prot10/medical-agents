# MS-RR-S04
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MS-RR) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. All changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.cranial_nerves` | "Mild right optic disc pallor" at day 10 of a first optic neuritis (plan I, F7). | FIXED: normal optic discs, no swelling or pallor (retrobulbar segment on MRI). |
| C | major | `followup_outputs[2]` (OCT) | Right pRNFL 68 / GCL 62 thinning at day 10; left GCIPL missing; bare "Abnormal values" impression. | FIXED: acute form, both eyes (R 109/78, L 104/81, inter-eye 5 and 3 um), "no RNFL or GCIPL thinning". |
| B | minor | `patient.history_present_illness` | "seeing only shapes and shadows" while the exam measures 20/80. | FIXED: "can no longer read print with the right eye". |
| D | major | `initial_tool_outputs.mri` | Brain MRI reported the C3-C4 cord lesion, an LETM statement and a "spinal cord distribution" (class H). | FIXED: cord finding and LETM line removed; numbered impression of brain and optic nerve findings; "Spinal cord not assessed on this study."; enhancing count states the optic nerve separately. |
| E | minor | `initial_tool_outputs.mri.findings[2]` | "Right middle cerebellar peduncle and left brachium pontis": the brachium pontis is the middle cerebellar peduncle. | FIXED: "Right and left middle cerebellar peduncles", left lesion faintly enhancing. |
| B | major | `followup_outputs[0].output` (spine MRI) | Impression named only "a thoracic cord" lesion without level and omitted the C3-C4 lesion; bilateral pyramidal signs, right-predominant, with a dorsal-column C3-C4 lesion and a left lateral T6-T7 lesion; empty descriptions. | FIXED: C3-C4 lesion of the dorsal columns and right lateral column (Lhermitte, right-predominant spasticity), T6-T7 left lateral column with faint enhancement; descriptions and numbered impression with levels. |
| A/C | major | `followup_outputs` (`request_repeat_mri_3months`) | Future 3-month MRI (class F). | FIXED: deleted. |
| C | major | `followup_outputs` (literature) | 2017 criteria presented as current ("OCB can substitute for DIT"); an unverifiable "Lancet Neurology 2023" source; summary empty. | FIXED: canonical general 2024 McDonald output (class O); trigger `search_mcdonald_criteria`. |
| C | major | `followup_outputs` (ocrelizumab check) | "Ocrelizumab is teratogenic" counselled to a man (wrong drug fact and wrong patient); medications listed under warnings with an empty `interactions` list; TB screening and DMT alternatives. | FIXED: interactions list (ferrous sulfate, loratadine: none), cephalosporin allergy line, HBV/immunoglobulin/vaccine/premedication warnings; alternatives emptied. |
| B | major | `initial_tool_outputs.labs.panels.CBC` | Hct 35.6% / RBC 4.59 gives MCV 77.6 fL, but MCV read 91 (normal); Hct and RBC reference ranges were female ranges in a man; "consistent with known iron deficiency anemia" interpretive text in the abnormal summary. | FIXED: MCV 77.6 fL (abnormal), male ranges Hct 40-52%, RBC 4.50-5.90; factual abnormal summary and interpretation. |
| C | major | `ground_truth.assessment.required_recommendations` | No must for iron deficiency anaemia in an adult man (a gastrointestinal source must be sought; comorbidity class "dismissed"); template musts otherwise (DIS/DIT restatement, AQP4/MOG as a must, JCV, smoking cessation in a never smoker); no infection exclusion or bladder plan despite incontinence. | FIXED: formulation; urinalysis then methylprednisolone (IV 1 g x3-5 d or oral 500 mg x5 d, PLEX if refractory); DMT by activity (no pregnancy clause: male); pre-DMT screening; post-void residual with antimuscarinic or ISC; GI investigation of the anaemia if not already done. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Teriflunomide/child-bearing prohibition in a man (T10), JCV and fingolimod prohibitions without a case reason. | FIXED: deleted; kept non-specific lesions, chronic steroids, live vaccines, cord MRI. |
| C | major | `ground_truth.action_criteria`, `stop_rule` | Template criteria and stop rule (literature and drug check required with unmatched arguments, etc.). | FIXED per plan A/P: brain MRI, spine MRI, labs (required), `action-aqp4-mog-cba` (recommended), CSF, VEP, OCT, drug check, literature (optional); stop rule brain MRI, spine MRI, labs; max 2. |
| C | major | `ground_truth.differential` | NMOSD and MOGAD "high", sarcoidosis "moderate" whatever the results. | FIXED: all low with the case's results; added B12 myelopathy and NPSLE (ANA row); CNS vasculitis and Susac removed. |
| C | major | `ground_truth.key_clinical_evidence` | Engineering lines and wrong facts (three regions, black holes as DIT, OCB substitute for DIT), tumefactive, ELISA and DMT lines. | FIXED: six observable bullets. |
| C | minor | `initial_tool_outputs.csf` | Myelin basic protein "consistent with active demyelination" (obsolete, F6, and a diagnostic claim); no kFLC; glucose ratio 0.59 against its own stated normal of > 0.6 in a report called normal; snake_case test names; IgG synthesis 14.2 identical to S03. | FIXED: MBP deleted; kFLC 31.6 added; CSF glucose 61.0 mg/dL (ratio 0.63); readable test names; synthesis rate 16.1; pattern interpretation. |
| B | minor | `followup_outputs[1]` (VEP) | Values identical to S01 (128 ms, 3.2/8.1 uV). | FIXED: right 121 ms, 4.4 uV; left 106 ms, 7.9 uV; interocular 15 ms. |
| E | minor | `initial_tool_outputs.labs` | AQP4 row without method; B12 and TSH in "Autoimmune_Screen"; HIV with leaked significance; BMP only. | FIXED: panels CBC, CMP (male liver ranges, normal), inflammatory markers, vitamins and endocrine, autoimmune, neuroimmunology (CBA rows), infectious serology. |
| A | minor | `fallback_tool_outputs.advanced_imaging.modality` | "FDG-PET" prose. | FIXED: `FDG_PET`. |
| B | minor | `ground_truth.red_herrings` | Empty, although the anaemia is a real distractor. | FIXED: anaemia herring (`initial_tool_outputs.labs.panels.CBC[1]`). |
| E | minor | `metadata.McDonald_criteria_version`, `metadata.clinical_pearls`, `metadata.difficulty_rationale` | "2017"; "Dawson fingers ... pathognomonic for MS" (wrong); "clinical hallmarks". | FIXED: "2024"; "characteristic"; 2024 rationale; `last_revised` 2026-10-24. |
| C | minor | `ground_truth.avoided_actions` | Generic rationales with em dashes. | FIXED: case-tied rationales. |
| A | minor | `ground_truth.differential[*].icd_code` | Neurosarcoidosis coded D86.85 (sarcoid myocarditis); ADEM coded G04.81 (other encephalitis); ICD-10-CM codes neurosarcoidosis D86.89 and ADEM G04.00. | FIXED: D86.89 and G04.00. |

## Changes, in one paragraph a physician can read before re-reviewing

A 36-year-old man with 10 days of right optic neuritis (20/80, RAPD) and a concurrent myelitis (spastic paraparesis, bilateral Babinski signs, incontinence, Lhermitte), with a left arm sensory episode 8 months ago. The fundus is now normal and the OCT normal (acute stage); VEP right P100 121 ms. The brain MRI reports brain and optic nerve findings only (the "brachium pontis" duplicate is now "both middle cerebellar peduncles"); the spine MRI reports both cord lesions with levels (C3-C4 dorsal and right lateral columns, T6-T7 left lateral column, faintly enhancing). The 3-month MRI is deleted; the literature output gives general 2024 McDonald text; the ocrelizumab check no longer calls the drug teratogenic in a man. The blood count now fits a microcytic iron deficiency anaemia (MCV 77.6, male reference ranges), and a must asks for its gastrointestinal source to be investigated. Work-up: brain MRI, spine MRI, mimic labs (required), AQP4/MOG CBA (recommended), CSF, VEP, OCT, drug check, literature (optional). CSF: MBP removed, kFLC 31.6, glucose ratio 0.63. Musts: 2024 formulation (5 of 5 regions), urinalysis then methylprednisolone, DMT by activity, pre-DMT screening, bladder management, anaemia work-up. Male-only prohibitions removed; differential all low with reasons.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonyms (plan 5.2).
- `perfect_agent.py` `<- ?` for the labs source is a checker artefact (null fields); probe-confirmed initial labs.

## Open questions for Andrea (judgment calls you could not settle)

None. The anaemia must (gastrointestinal investigation of iron deficiency in an adult man, BSG 2021 guidance) is outside MS care but is a real management item of this patient; it carries no scalar weight.

## Verification

`perfect_agent.py MS-RR-S04 -v`: ok (brain MRI <- initial mri; spine <- followup[0]; labs/AQP4-MOG <- initial labs). Probe: CSF (OCB or kFLC), VEP, OCT, drug check and literature served from the case; CT and FDG-PET from fallbacks. `test_case_guards.py -k MS-RR-S04`: pass. `case_io.py check MS-RR-S04`: schema and synonym guard OK, no failure names S04.

## Verification (adversarial check, 24 Oct 2026)

Adversarial check: read the log, the full diff against the pre-round file (HEAD~1) and the whole final case; checked laterality (exam vs brain and cord lesions vs VEP/OCT), the acute optic neuritis timeline (disc, OCT), lab arithmetic (Hct = RBC x MCV, MCHC), CSF glucose ratio against the serum glucose, red-herring field paths (all resolve), musts against allergies, medications and prohibitions, the differential against the served results, and the any-query literature and drug outputs for leakage. No reviewer notes exist for MS-RR, so the reviewer-note table is complete.

Found and fixed:
- C minor: the MOGAD differential entry cites "no perineural enhancement", which the brain MRI report never stated (a differential may cite only served results). Added ", without perineural (optic nerve sheath) enhancement" to the post-contrast description of the optic nerve finding in `initial_tool_outputs.mri` (a Kind 2 observation the orbit sequences make). Same class seen outside this batch in the MS-RR-RS03 differential: for the condition lead.
- C minor: `patient.neurological_exam.reflexes` said "Sustained ankle clonus (4-5 beats)": clonus of 4-5 beats is by definition unsustained. Now "Unsustained ankle clonus (4-5 beats) bilaterally" (wording carried over from the pre-round file).
Checked and accepted: microcytic anaemia (Hb 10.9, Hct 35.6, MCV 77.6, RBC 4.59; male reference ranges, flags true) is consistent and supports the GI-source must; no pregnancy clause or teriflunomide prohibition in a man; cephalosporin allergy not contradicted; brain volumetrics (3 enhancing brain lesions plus optic nerve) match the findings.

perfect_agent.py: ok (labs/AQP4-MOG same-report warning by design of plan A8). case_io.py check: schema and synonym guard OK, no test failure names the case. test_case_guards.py -k MS-RR-S0: 12 passed.

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `fallback_tool_outputs.echo.echo_type` added "TTE": the report is transthoracic and the discriminator guard requires the vocabulary term (every other MS-RR case has it).
- `action-4-check-drug-interactions.expected_evidence` was empty; written from the stored drug output in policy voice: "Ocrelizumab with ferrous sulfate and loratadine: no relevant interaction; hepatitis B screening and vaccine timing first".
- `assessment.required_recommendations[0]` formulation must made case-specific by appending "(here periventricular, juxtacortical, infratentorial, spinal cord and right optic nerve: five regions, so no separate DIT is required)", from the KCE DIS line and the stored outputs, as in the other 18 cases.
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders).
- `assessment.required_recommendations[3]` pre-DMT screening: HIV removed from the tests to order and noted as already non-reactive, since the required mimic panel reports it (HIV-1/2 antigen/antibody: Non-reactive), as the RM, RP and RS cases do.

## Close-out (24 Oct 2026)

Condition close-out (`plans/MS-RR-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G35 entry, re-applied with `apply_diagnosis_synonyms.py --prune --conditions multiple_sclerosis`): removed the label "demyelinating disease" (G37.9 is an Excludes1 of G35.A, and its tokens occur in an NMOSD, MOGAD or ADEM answer, which would have scored as correct) and the codes G35.B and G35.C (primary and secondary progressive MS in FY2026 ICD-10-CM, a different course from this relapsing-remitting case). Accepted now: the label, multiple sclerosis, MS, relapsing(-)remitting multiple sclerosis, RRMS; codes G35.A, G35, G35.D.
- Checks: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MS-RR-` passes with MS-RR now in `DISCRIMINATOR_CONDITIONS`.
