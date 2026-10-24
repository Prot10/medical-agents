# MS-RR-S03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MS-RR) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. All changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.cranial_nerves` | "Left optic disc mildly pale" at day 5 of a first optic neuritis (plan I, F7). | FIXED: "Optic discs normal on fundoscopy, with no swelling or pallor" (retrobulbar segment on MRI). |
| C | major | `followup_outputs[2]` (OCT) | Left pRNFL 68 / GCL 62 thinning at day 5; bare "Abnormal values" impression. | FIXED: acute form, both eyes labelled (R 96/84, L 100/82, inter-eye 4 and 2 um), "no RNFL or GCIPL thinning". |
| B | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | "For the past several months ... her visual symptoms seem to worsen after hot showers" while the visual symptoms began 5 days ago (timeline impossible). | FIXED: Uhthoff phenomenon now concerns the right hand tingling of the prior episode, in the HPI and the exam line (em dash removed). |
| B | minor | `patient.history_present_illness` | "a particularly busy week at school" for a data analyst. | FIXED: "at work". |
| D | major | `initial_tool_outputs.mri` | Brain MRI reported the C3-C4 cord lesion and a "spinal cord distribution" (class H). | FIXED: cord finding removed; numbered impression of brain and optic nerve findings; "Spinal cord not assessed on this study."; black-hole observation worded as a finding. |
| A/C | major | `followup_outputs` (`request_repeat_mri_3months`) | Future 3-month MRI (class F). | FIXED: deleted. |
| D | blocker | `initial_tool_outputs.literature_search` | Any-query literature output whose finding and summary were the `expected_evidence` of `action-3` (scoring key leak; `test_any_query_outputs_do_not_leak_expected_evidence[MS-RR-S03]` failed). | FIXED: replaced by the canonical general 2024 McDonald output under the key "2024 McDonald criteria multiple sclerosis diagnosis"; guard passes. |
| C | major | `followup_outputs[3]` (ocrelizumab check) | Stated a baseline IgG of 1138 mg/dL, negative HBsAg/anti-HBc and confirmed VZV immunity, none of which the case contains (fabricated results); empty `interactions`; DMT alternatives by efficacy. | FIXED: each current medicine listed (loratadine, COC, vitamin D3: no significant interaction); contraindications (active HBV, active infection, severe immunocompromise); warnings as screening steps (HBV, immunoglobulins, vaccines 4-6 weeks before, infusion premedication, contraception); alternatives emptied. |
| C | major | `ground_truth.action_criteria` | Template criteria; literature criterion `recommended` with a query argument (ruling 5); drug check required with non-schema keys. | FIXED per plan A/P: brain MRI, spine MRI, labs (required), `action-aqp4-mog-cba` (recommended), CSF, VEP, OCT, drug check, literature (optional, last); case-specific rationales and evidence. |
| C | minor | `ground_truth.stop_rule` | Drug check in the stop rule; max 0. | FIXED: brain MRI, spine MRI, labs; max 2. |
| C | major | `ground_truth.assessment` | Template musts (DIS/DIT restatements, AQP4/MOG as a must, JCV, smoking cessation in a never smoker); no infection exclusion or bladder plan despite urgency with near-incontinence; JCV and fingolimod prohibitions without a case reason. | FIXED: formulation; urinalysis before steroids, then IV 1 g x3-5 d or oral 500 mg x5 d, PLEX if refractory; DMT by activity with pregnancy/contraception (married, on COC); pre-DMT screening; post-void residual with antimuscarinic or ISC; Uhthoff counselling and vitamin D review. Prohibitions: non-specific lesions, teriflunomide, chronic steroids, live vaccines, cord MRI, unconfirmed carpal tunnel label. |
| C | major | `ground_truth.differential` | NMOSD and MOGAD "high", sarcoidosis "moderate" whatever the results. | FIXED: all low with the case's results (NMOSD entry states why African American ancestry makes the serology matter); added B12, NPSLE (ANA row), neurosyphilis (CSF VDRL); CNS vasculitis and Susac removed. |
| C | major | `ground_truth.key_clinical_evidence` | Engineering lines, wrong facts (three regions, black holes as DIT, OCB substitute for DIT), tumefactive, ELISA and DMT template lines. | FIXED: six observable bullets. |
| E | minor | `initial_tool_outputs.labs` | AQP4 row without method; HIV row with leaked significance; BMP only; vitamin D 18 ng/mL is the template value copied into 7 cases (plan E). | FIXED: CBA rows in a Neuroimmunology panel; HIV significance null; CMP with liver tests (normal); vitamin D 16 ng/mL (abnormal summary, interpretation, KCE, herring, must updated). |
| B | minor | `initial_tool_outputs.labs.panels.CBC` (Hematocrit) | Hb 13.2 g/dL with Hct 43.1% gives MCHC 30.6 g/dL against a normal MCV 94. | FIXED: Hct 39.4% (MCHC 33.5). |
| C | minor | `initial_tool_outputs.csf` | Myelin basic protein; no kFLC; no references for protein, glucose, WBC; IgG index 0.82 identical to S01; recital interpretation. | FIXED: MBP deleted; kFLC 52.3 (< 6.1); references added; IgG index 0.88; pattern interpretation. |
| B | minor | `followup_outputs[1]` (VEP) | Left eye values identical to S01 (128 ms, 3.2 uV). | FIXED: 126 ms, 3.6 uV, interocular 24 ms. |
| B | minor | `followup_outputs[0]` (spine MRI) | Empty finding descriptions; LETM line with em dash; T6-T7 side unstated while vibration loss is left. | FIXED: descriptions written, T6-T7 left-predominant, numbered impression. |
| A/E | minor | `fallback_tool_outputs.advanced_imaging.modality`, `fallback_tool_outputs.drug_interactions.general.proposed` | "FDG-PET" prose; "(agent not specified on this case's pathway)". | FIXED: `FDG_PET`; "Not specified". |
| C | minor | `ground_truth.avoided_actions`, `red_herrings`, `metadata` | Generic rationales; single herring; 2017 wording. | FIXED: case-tied rationales; carpal tunnel herring added; 2024 wording, `last_revised` 2026-10-24. |
| A | minor | `ground_truth.differential[*].icd_code` | Neurosarcoidosis coded D86.85 (sarcoid myocarditis); ADEM coded G04.81 (other encephalitis); ICD-10-CM codes neurosarcoidosis D86.89 and ADEM G04.00. | FIXED: D86.89 and G04.00. |

## Changes, in one paragraph a physician can read before re-reviewing

A 24-year-old African American woman with day-5 left optic neuritis (20/80, RAPD), a concurrent left-sided myelopathy with urgency, and a right hand sensory episode 8 months ago labelled carpal tunnel. The fundus is now normal and the OCT normal and symmetric (acute stage); the VEP shows a left P100 of 126 ms. The Uhthoff phenomenon, which the HPI placed months before any visual symptom, now concerns the right hand tingling. The brain MRI reports brain and optic nerve findings only and the C3-C4 lesion is reported on the spine MRI alone; the 3-month repeat MRI is deleted. The initial literature output, which repeated the scoring key, is replaced by general 2024 McDonald text, and the ocrelizumab check no longer invents immunoglobulin, hepatitis B and VZV results. Work-up: brain MRI, spine MRI, mimic labs (required), AQP4/MOG CBA (recommended), then CSF, VEP, OCT, drug check, literature (optional). CSF: MBP removed, kFLC 52.3 added. Musts: 2024 formulation (5 of 5 regions), urinalysis then methylprednisolone, DMT by activity with pregnancy and contraception, pre-DMT screening, post-void residual and bladder treatment, Uhthoff and vitamin D. Differential all low with the case's results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonyms (plan 5.2).
- `perfect_agent.py` `<- ?` source labels for brain MRI and labs are a checker artefact (null fields); probe-confirmed initial outputs.

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

`perfect_agent.py MS-RR-S03 -v`: ok. Probe: every criterion's tool served from the case (CSF by OCB or kFLC, VEP, OCT, drug check, literature); CT and FDG-PET from fallbacks. `test_case_guards.py -k MS-RR-S03`: pass (the leak failure is gone). `case_io.py check MS-RR-S03`: schema and synonym guard OK, no failure names S03.

## Verification (adversarial check, 24 Oct 2026)

Adversarial check: read the log, the full diff against the pre-round file (HEAD~1) and the whole final case; checked laterality (exam vs brain and cord lesions vs VEP/OCT), the acute optic neuritis timeline (disc, OCT), lab arithmetic (Hct = RBC x MCV, MCHC), CSF glucose ratio against the serum glucose, red-herring field paths (all resolve), musts against allergies, medications and prohibitions, the differential against the served results, and the any-query literature and drug outputs for leakage. No reviewer notes exist for MS-RR, so the reviewer-note table is complete.

Found and fixed:
- C minor: the MOGAD differential entry cites "no perineural enhancement", which the brain MRI report never stated (a differential may cite only served results). Added ", without perineural (optic nerve sheath) enhancement" to the post-contrast description of the optic nerve finding in `initial_tool_outputs.mri` (a Kind 2 observation the orbit sequences make). Same class seen outside this batch in the MS-RR-RS03 differential: for the condition lead.
- B minor (pathway order, ruling 5): the general literature output still sat in `initial_tool_outputs.literature_search`, so the review app showed a literature search as part of the initial work-up, unlike S01, S02 and S04-S06. Moved unchanged to a last follow-up (`search_medical_literature`, trigger `search_mcdonald_criteria`) and set the initial entry to null; a direct environment probe confirms any literature query still returns that output (not the generic fallback), and the leak guard passes.
Checked and accepted: left C3-C4 dorsal/lateral lesion with left leg pyramidal signs; left MCP with left heel-to-shin ataxia; no NSAID in any must (NSAID allergy); ocrelizumab check content correct (HBV, immunoglobulins, live vaccines, premedication); vitamin D herring path resolves to the 16 ng/mL row.

perfect_agent.py: ok (labs/AQP4-MOG same-report warning by design of plan A8). case_io.py check: schema and synonym guard OK, no test failure names the case. test_case_guards.py -k MS-RR-S0: 12 passed.

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `fallback_tool_outputs.echo.echo_type` added "TTE": the report is transthoracic and the discriminator guard requires the vocabulary term (every other MS-RR case has it).
- `action-4-check-drug-interactions.expected_evidence` was empty; written from the stored drug output in policy voice: "Ocrelizumab with loratadine, her oral contraceptive and vitamin D3: no relevant interaction; hepatitis B screening and vaccine timing first".
- `assessment.required_recommendations[0]` formulation must made case-specific by appending "(here periventricular, juxtacortical, infratentorial, spinal cord and left optic nerve: five regions, so no separate DIT is required)", from the KCE DIS line and the stored outputs, as in the other 18 cases.
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders).
- `assessment.required_recommendations[3]` pre-DMT screening: HIV removed from the tests to order and noted as already non-reactive, since the required mimic panel reports it (HIV-1/2 antigen/antibody: Non-reactive), as the RM, RP and RS cases do.
