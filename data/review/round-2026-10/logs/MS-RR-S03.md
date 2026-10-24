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
