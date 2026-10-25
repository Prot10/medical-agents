# MS-RR-S06
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MS-RR) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. All changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `ground_truth.key_clinical_evidence`, `initial_tool_outputs.labs` | KCE cited OCT, VEP and AQP4/MOG cell-based results that the case never served (no OCT or VEP follow-up, no AQP4/MOG rows), while the labs interpretation claimed them. | FIXED per plan: VEP follow-up (left P100 120 ms, preserved amplitude, interocular 22 ms) and OCT follow-up (left pRNFL 79, temporal 49, GCIPL 69; right 97/82; inter-eye GCIPL 13; thinning in the eye with prior optic neuropathy, plan I); Neuroimmunology panel with "AQP4-IgG (cell-based assay)" and "MOG-IgG (live cell-based assay)", both negative. |
| C | major | `patient.neurological_exam.sensory` | Pinprick and temperature loss in the RIGHT leg with a right lateral and dorsolateral C5-C6 lesion: the spinothalamic tract carries the contralateral side, so a right lateral cord lesion gives left pain and temperature loss (partial Brown-Sequard). | FIXED: pinprick and temperature mildly reduced in the left leg from the knee; right vibration and touch loss and right pyramidal signs kept (ipsilateral). |
| B | minor | `patient.neurological_exam.gait` | "Mildly antalgic gait" (pain-avoiding) in a painless spastic monoparesis; Romberg positive with intact proprioception and only mild toe vibration loss. | FIXED: "Spastic right leg gait with mild right foot drop"; Romberg sign negative. |
| E | minor | `patient.neurological_exam.cranial_nerves` | Fundus line with an em dash and the interpretive "patient denies any prior painful vision loss". | FIXED: "mild temporal pallor of the left optic disc; right disc normal" (the HPI already records no prior visual symptoms). |
| D | minor | `initial_tool_outputs.mri.additional_observations` | "dedicated orbit/spine imaging recommended for complete evaluation" in the brain MRI (class H: points to the spine criterion). | FIXED: "Dedicated orbital sequences not acquired." and "Spinal cord not assessed on this study."; numbered impression. |
| B | minor | `followup_outputs[0].output` (spine MRI) | Empty finding description; the enhancement appeared only in the impression; thoracic cord not mentioned in a cervical and thoracic study; duplicate LETM observations. | FIXED: description with enhancement; "Thoracic cord normal in calibre and signal"; duplicate removed; numbered impression. |
| C | major | `followup_outputs` (`search_ms_criteria_dmt`) | Presented the 2017 criteria as current (OCB can satisfy DIT) and argued DMT choice with JCV and hepatitis B screening. | FIXED: canonical general 2024 McDonald output (class O), trigger `search_mcdonald_criteria`. |
| C | major | `followup_outputs` (`check_dmt_drug_interactions`) | Natalizumab class review (TOUCH, JCV index thresholds, alternatives by efficacy, fingolimod and teriflunomide warnings) for a man on cetirizine and vitamin D; not a check of a proposed treatment. | FIXED: methylprednisolone check (cetirizine, vitamin D3: no interaction; sulfonamide allergy: no cross-reactivity; urinary infection contraindication; glucose and blood pressure warnings); trigger `request_drug_interaction_check_steroids`. |
| C | minor | `initial_tool_outputs.csf` | Myelin basic protein (F6); no kFLC; OCB line with an em dash; glucose without reference; recital interpretation; IgG index 0.78 and synthesis rate 12.4 shared with other cases (template numbers). | FIXED: MBP deleted; kFLC index 21.3 (< 6.1); glucose reference; IgG index 0.86, synthesis 11.9; pattern interpretation. |
| E | minor | `initial_tool_outputs.labs` | No ESR or CRP although the old labs criterion asked for them; AQP4/MOG absent; mixed "Autoimmune and infectious screen". | FIXED: inflammatory markers (ESR 6, CRP 0.3, normal); panels Autoimmune (ANA), Neuroimmunology, Infectious serology (HIV, RPR), Vitamins, Thyroid; interpretation rewritten. |
| C | major | `ground_truth.action_criteria` | Template criteria: literature and drug check required with unmatched arguments (2017 query string; non-schema `proposed_class`/`screen_for`); CSF needed three assays; labs needed 9 analytes; no AQP4/MOG, VEP or OCT criterion; label = rationale; free-text citations. | FIXED per plan tier table: brain MRI, spine MRI, labs (required), `action-aqp4-mog-cba` (recommended), CSF (OCB or kFLC), VEP, OCT (added), drug check, literature (optional); case-specific rationales and evidence. |
| C | minor | `ground_truth.stop_rule`, `sequence_constraints` | Literature and drug check in the stop rule; max 0; sequence citation `[McDonald_2017]`. | FIXED: brain MRI, spine MRI, labs; max 2; canonical MRI-before-LP soft constraint. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated interpretation (INO localisation, DIS, DIT with OCB "confirmed additionally"), tests (AQP4/MOG, spine MRI), JCV and hepatitis B lines; no infection exclusion, bladder plan or rehabilitation despite urgency with near-incontinence and foot drop. | FIXED: formulation; urinalysis then methylprednisolone (oral 500 mg x5 d or IV 1 g x3-5 d, PLEX if refractory); DMT by activity (no pregnancy clause: male); pre-DMT screening; post-void residual with antimuscarinic or ISC; physiotherapy with an ankle-foot orthosis if needed. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | JCV/TOUCH, fingolimod and ELISA prohibitions without a case reason; "Do not exclude NMOSD on clinical grounds alone ... mandatory"; em dashes. | FIXED: NMOSD-from-cord-lesion and DMT-before-serology prohibitions reworded; lumbar disc attribution prohibition added; non-specific lesions, chronic steroids, live vaccines, cord MRI. |
| C | major | `ground_truth.differential` | NMOSD and MOGAD "high", CIS "moderate" after negative CBA and a short cord lesion; neurosarcoidosis said ACE and hilar nodes were "absent" although neither was tested. | FIXED: NMOSD, MOGAD, CIS low with the case's results; neurosarcoidosis reasons limited to what the case shows; B12 and spondylotic myelopathy very low; NPSLE (ANA) and neurosyphilis (RPR, CSF VDRL) added. |
| C | major | `ground_truth.key_clinical_evidence` | Engineering lines (July 2026 review, Tier), "requires at least two" regions (F2), OCB as DIT, NMOSD "the most important red herring" in a KCE line. | FIXED: five observable bullets (INO and MLF lesion, partial myelopathy and its lesion, DIS 4 regions on MRI plus the optic nerve on OCT/VEP, serology and OCB, the disc-labelled episode). |
| B | minor | `ground_truth.red_herrings` | Single herring with "naive agent"; the herniated-disc label is a second real distractor. | FIXED: cord herring reworded; disc herring added (`patient.clinical_history.past_medical_history[0]`). |
| C | minor | `ground_truth.avoided_actions` | Generic rationales with em dashes; citations to unrelated keys; Holter rationale about fingolimod. | FIXED: case-tied rationales; `[Wattjes_2021]` on CT and PET. |
| A/E | minor | `fallback_tool_outputs.advanced_imaging.modality`, `fallback_tool_outputs.drug_interactions.general.proposed` | "FDG-PET" prose; "(agent not specified on this case pathway)". | FIXED: `FDG_PET`; "Not specified". |
| B | minor | `metadata.difficulty_rationale` | 2017 logic (DIT by OCB, four regions). | FIXED: 2024 wording; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

A 34-year-old man with a 12-day right leg weakness, Lhermitte sign and urgency, a left internuclear ophthalmoplegia, left temporal disc pallor without any visual history, and a left leg sensory episode 18 months ago labelled a herniated disc. The sensory exam now fits the right C5-C6 lateral and dorsolateral lesion: right vibration and touch loss with left pinprick and temperature loss (partial Brown-Sequard); the gait is spastic, not antalgic, and Romberg is negative. The brain MRI no longer recommends spine imaging. The case now serves what its evidence cited: a VEP (left P100 120 ms) and an OCT (left RNFL and GCIPL thinning, inter-eye GCIPL 13 micrometers) showing a past subclinical left optic neuropathy, and AQP4-IgG and MOG-IgG cell-based results (negative). The literature output gives general 2024 McDonald text; the drug check screens methylprednisolone instead of a natalizumab class review. Work-up: brain MRI, spine MRI, mimic labs (required), AQP4/MOG CBA (recommended), CSF, VEP, OCT, drug check, literature (optional). CSF: MBP removed, kFLC 21.3. Musts: 2024 formulation (4 regions on MRI, 5 with the optic nerve), urinalysis then methylprednisolone, DMT by activity, pre-DMT screening, bladder management, physiotherapy for the foot drop. Differential low or very low with the case's results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonyms G35.B/G35.C and "demyelinating disease" (plan 5.2).
- `perfect_agent.py` `<- ?` for the labs source is a checker artefact (null fields); the probe confirms the initial labs are served.

## Open questions for Andrea (judgment calls you could not settle)

None. The plan counts the optic nerve as the fifth region; on MRI alone the case has four, which already meets DIS without DIT (F3), so the formulation and KCE accept either count. The pinprick and temperature loss was moved to the left leg to match the right lateral cord lesion; the HPI's right leg numbness (touch) is unchanged.

## Verification

`perfect_agent.py MS-RR-S06 -v`: ok (brain MRI <- initial mri; spine <- followup[0]; labs and AQP4/MOG <- initial labs, same-report warning by design of plan A8). Probe: CSF (OCB or kFLC), VEP, OCT, drug check and literature served from the case; CT and FDG-PET from case fallbacks. `test_case_guards.py -k MS-RR-S06`: 2 passed. `case_io.py check MS-RR-S06`: schema and synonym guard OK, no test failure names the case.

## Verification (adversarial check, 24 Oct 2026)

Adversarial check: read the log, the full diff against the pre-round file (HEAD~1) and the whole final case; checked laterality (exam vs brain and cord lesions vs VEP/OCT), the acute optic neuritis timeline (disc, OCT), lab arithmetic (Hct = RBC x MCV, MCHC), CSF glucose ratio against the serum glucose, red-herring field paths (all resolve), musts against allergies, medications and prohibitions, the differential against the served results, and the any-query literature and drug outputs for leakage. No reviewer notes exist for MS-RR, so the reviewer-note table is complete.

Found and fixed:
No error found; no change made.
Checked and accepted: left MLF pontine lesion with the left INO; right C5-C6 lesion with right leg weakness and vibration loss and left leg pinprick loss (partial Brown-Sequard pattern); left chronic OCT thinning (inter-eye GCIPL 13 micrometers) and delayed left P100 fit the temporal pallor without an ON history, and the brain MRI states that orbit sequences were not acquired, so the optic region comes only from OCT/VEP as KCE[2] says; MOGAD entry makes no unsupported claim; male case without pregnancy clause; lesion counts in volumetrics match the findings.

perfect_agent.py: ok (labs/AQP4-MOG same-report warning by design of plan A8). case_io.py check: schema and synonym guard OK, no test failure names the case. test_case_guards.py -k MS-RR-S0: 12 passed.

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `fallback_tool_outputs.echo.echo_type` added "TTE": the report is transthoracic and the discriminator guard requires the vocabulary term (every other MS-RR case has it).
- `action-4-check-drug-interactions.expected_evidence` was empty; written from the stored drug output in policy voice: "Methylprednisolone with cetirizine and vitamin D3: no relevant interaction; exclude infection first and monitor glucose".
- `assessment.required_recommendations[0]` formulation must made case-specific by appending "(here periventricular, juxtacortical, infratentorial and spinal cord, with the left optic nerve a fifth region by OCT or VEP; four or more regions need no separate DIT)", from the KCE DIS line and the stored outputs, as in the other 18 cases.
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders). Initial labs interpretation edited to drop the antibody results: removed "All other results, including AQP4-IgG and MOG-IgG by cell-based assay, HIV and RPR, are within reference ranges or negative.".
- `assessment.required_recommendations[3]` pre-DMT screening: HIV removed from the tests to order and noted as already non-reactive, since the required mimic panel reports it (HIV-1/2 Ag/Ab combination assay: Nonreactive), as the RM, RP and RS cases do.

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
