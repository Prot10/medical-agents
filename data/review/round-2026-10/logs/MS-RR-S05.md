# MS-RR-S05
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MS-RR) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. All changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.additional` | "Uhthoff phenomenon reported: visual blurring in the left eye worsens after a hot shower" while the visual symptoms began 5 days ago and the HPI places the heat-related symptom in the right foot (timeline impossible); em dash. | FIXED: the residual right foot tingling returns when she is overheated (Uhthoff phenomenon), matching the HPI. |
| C | minor | `patient.neurological_exam.additional` | EDSS 2.0 with visual FS 3 (20/80, converted 2) and sensory FS 2 (right leg vibration and light touch loss): two FS of grade 2 give EDSS 2.5. | FIXED: EDSS estimated at 2.5. |
| E | minor | `patient.neurological_exam.cranial_nerves`, `.sensory` | "Red desaturation in the left visual field" with an em dash (monocular finding); fundus line carried the diagnosis "(consistent with acute optic neuritis)"; "consistent with prior relapse territory" labels the earlier episode a relapse. | FIXED: "Red desaturation in the left eye"; "mild left optic disc swelling without pallor; right disc normal"; "in the territory of the earlier episode". Disc swelling kept (anterior optic neuritis, about a third of cases). |
| D | major | `initial_tool_outputs.mri` | Brain MRI stated "No evidence of longitudinally extensive cord signal abnormality" and recommended spine imaging (class H: pre-empts the spine criterion). | FIXED: observation "Spinal cord not assessed on this study."; recommended actions emptied; numbered impression of brain and optic nerve findings (callososeptal lesions named under periventricular). |
| B | minor | `followup_outputs[0].output` (spine MRI) | Empty finding descriptions; side of the C4-C5 lesion unstated while the residual Babinski sign and vibration loss are right-sided. | FIXED: C4-C5 right dorsolateral, T5-T6 dorsal columns, both non-enhancing and under one segment; numbered impression. |
| C | major | `followup_outputs` (`search_mcdonald_criteria_dmt`) | Presented the 2017 criteria ("2 of 4 regions", OCB substitute for DIT) as current and argued DMT efficacy. | FIXED: canonical general 2024 McDonald output (class O), trigger `search_mcdonald_criteria`. |
| C | major | `followup_outputs` (`request_drug_interaction_check_dmt`) | Class review of every DMT (alternatives by efficacy, JCV and teriflunomide text) with an empty `interactions` list; not a check of anything this patient takes. | FIXED: methylprednisolone against her naproxen (GI bleeding: avoid or PPI) and ferrous sulfate (no interaction), sulfonamide allergy (no cross-reactivity), infection contraindication, glucose and blood pressure warnings; trigger `request_drug_interaction_check_steroids`. |
| C | major | `followup_outputs[2]` (OCT) | Left pRNFL 69 / temporal 46 / GCIPL 65 thinning at day 5, together with a swollen disc (impossible acutely, F7). | FIXED: acute form with swelling: left pRNFL 121 (increased superior and inferior), GCIPL 80; right 101/83; inter-eye GCIPL 3; "no RNFL or GCIPL thinning". |
| C | minor | `initial_tool_outputs.csf` | Myelin basic protein reported (obsolete, F6); no kFLC; OCB line with an em dash; recital interpretation. | FIXED: MBP deleted; kFLC index 17.9 (reference < 6.1); pattern interpretation. |
| E | minor | `initial_tool_outputs.labs` | AQP4/MOG rows mixed into an "Autoimmune and infectious panel"; no ESR/CRP; vitamin D 18 ng/mL is the template value copied into 7 cases (plan E). | FIXED: Neuroimmunology panel with "AQP4-IgG (cell-based assay)" and "MOG-IgG (live cell-based assay)"; infectious serology (HIV, RPR) and autoimmune (ANA) panels; ESR 9 and CRP 0.2 added (normal); vitamin D 13 ng/mL with abnormal summary, interpretation, KCE, herring and must updated. |
| C | major | `ground_truth.action_criteria` | Template criteria: literature and drug check required; no AQP4/MOG criterion. | FIXED per plan A/P: brain MRI, spine MRI, labs (required), `action-aqp4-mog-cba` (recommended), CSF (OCB or kFLC), VEP, OCT, drug check, literature (optional); case-specific rationales and evidence. |
| C | minor | `ground_truth.stop_rule` | Literature and drug check in the stop rule; max 0. | FIXED: brain MRI, spine MRI, labs; max 2. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated tests (brain MRI, spine MRI, AQP4/MOG); IV-only steroid; JCV and smoking cessation in a never smoker; no mention of her naproxen with high-dose steroids. | FIXED: formulation (5 of 5 regions); methylprednisolone oral 500 mg x5 d or IV 1 g x3-5 d with naproxen avoided or PPI, PLEX if refractory; DMT by activity with pregnancy and contraception (married, none listed); pre-DMT screening; vitamin D and Uhthoff counselling. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Fingolimod ECG prohibition without a case reason; em dashes; "2024 revised McDonald criteria (DIS and DIT)" (with 5 regions DIT is not needed, F3). | FIXED: fingolimod deleted; CIS and NMOSD/MOGAD prohibitions reworded; canonical non-specific-lesion, teriflunomide, chronic steroid, live vaccine prohibitions; cord MRI prohibition added (right Babinski sign). |
| C | major | `ground_truth.differential` | NMOSD and MOGAD "high", CIS "moderate" whatever the results; CNS vasculitis with nothing to raise it. | FIXED: MOGAD low (disc swelling raises it, MOG-IgG negative by live CBA, 10 mm segment, OCB present), NMOSD low, CIS low (excluded by the second attack); sarcoidosis and B12 low with reasons; NPSLE (ANA) and neurosyphilis (RPR, CSF VDRL) added; vasculitis removed. |
| C | major | `ground_truth.key_clinical_evidence` | "meeting the 2024 revised McDonald criteria for RRMS on clinical grounds alone even before imaging and CSF" (the plan's KCE rule: the 2024 diagnosis rests on MRI, which this case supplies, so the claim is dropped); three regions as DIS; OCB substitute for DIT; "internal consistency ... is essential for case validity" and July 2026 engineering lines. | FIXED: five observable bullets (optic neuritis, two attacks with objective signs and the matching C4-C5 lesion, DIS 5 of 5 with sites, serology and OCB against NMOSD/MOGAD, vitamin D). |
| B | minor | `ground_truth.red_herrings[1]` | "full McDonald 2017 RRMS criteria are met"; em dash. | FIXED: 2024 wording; the herring now names the "lumbar disc herniation" label as the distractor. |
| E | minor | `fallback_tool_outputs.drug_interactions.general.proposed` | "(agent not specified on this case's pathway)". | FIXED: "Not specified". |
| B | minor | `metadata.difficulty_rationale`, `metadata.mcdonald_criteria_met` | 2017-based rationale. | FIXED: 2024 wording (5 of 5 regions); `last_revised` 2026-10-24. |
| E | minor | `followup_outputs[1]` (VEP) | Impression without final period. | FIXED. Values kept (132 ms is not shared with another case). |

## Changes, in one paragraph a physician can read before re-reviewing

A 29-year-old South Asian woman with day-5 painful left optic neuritis (20/80, RAPD, mild disc swelling) and a right leg sensory attack 9 months ago, labelled lumbar disc herniation, that left a right Babinski sign and right leg vibration and touch loss. The heat-related symptom now concerns the right foot, as in the HPI, and the EDSS is 2.5. The OCT shows the swollen left disc (pRNFL 121) and no thinning, as expected at day 5. The brain MRI no longer comments on the cord; the spine MRI places the C4-C5 lesion right dorsolateral, matching the old signs, with a dorsal-column T5-T6 lesion. The literature output gives general 2024 McDonald text and the drug check screens methylprednisolone against her naproxen and iron instead of a DMT class review. Work-up: brain MRI, spine MRI, mimic labs (required), AQP4/MOG CBA (recommended), CSF, VEP, OCT, drug check, literature (optional). CSF: MBP removed, kFLC 17.9 added. Musts: 2024 formulation (5 of 5 regions), methylprednisolone with naproxen stopped or PPI cover, DMT by activity with pregnancy and contraception discussed, pre-DMT screening, vitamin D (13 ng/mL) and Uhthoff counselling. MOGAD, NMOSD and CIS are now low, with the reasons in the case.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonyms G35.B/G35.C and "demyelinating disease" (plan 5.2).
- `perfect_agent.py` `<- ?` for the labs source is a checker artefact (null fields); the probe confirms the initial labs are served.

## Open questions for Andrea (judgment calls you could not settle)

None. Disc swelling is kept: it occurs in about a third of MS optic neuritis and is the case's deliberate MOGAD pull, settled by the negative live-cell MOG-IgG and the other features.

## Verification

`perfect_agent.py MS-RR-S05 -v`: ok (brain MRI <- initial mri; spine <- followup[0]; labs and AQP4/MOG <- initial labs, same-report warning by design of plan A8). Probe: CSF (OCB or kFLC), VEP, OCT, drug check and literature served from the case; CT and FDG-PET from case fallbacks. `test_case_guards.py -k MS-RR-S05`: 2 passed. `case_io.py check MS-RR-S05`: schema and synonym guard OK; the only failure in the condition names MS-RR-P02 (another worker's case).

## Verification (adversarial check, 24 Oct 2026)

Adversarial check: read the log, the full diff against the pre-round file (HEAD~1) and the whole final case; checked laterality (exam vs brain and cord lesions vs VEP/OCT), the acute optic neuritis timeline (disc, OCT), lab arithmetic (Hct = RBC x MCV, MCHC), CSF glucose ratio against the serum glucose, red-herring field paths (all resolve), musts against allergies, medications and prohibitions, the differential against the served results, and the any-query literature and drug outputs for leakage. No reviewer notes exist for MS-RR, so the reviewer-note table is complete.

Found and fixed:
- C minor: the MOGAD differential entry cites "no perineural enhancement", which the brain MRI report never stated (a differential may cite only served results). Added ", without perineural (optic nerve sheath) enhancement" to the post-contrast description of the optic nerve finding in `initial_tool_outputs.mri` (a Kind 2 observation the orbit sequences make). Same class seen outside this batch in the MS-RR-RS03 differential: for the condition lead.
Checked and accepted: right dorsolateral C4-C5 lesion with the residual right Babinski and right leg vibration/touch loss (ipsilateral tracts); acute OCT with left pRNFL swelling 121 micrometers fits the disc swelling at day 5; DMT must activity (enhancing optic nerve and periventricular lesions only) matches the reports; EDSS 2.5 derivable; naproxen GI risk in the steroid check matches the must; the "no DMT before NMOSD/MOGAD excluded" prohibition is consistent with the recommended serology criterion.

perfect_agent.py: ok (labs/AQP4-MOG same-report warning by design of plan A8). case_io.py check: schema and synonym guard OK, no test failure names the case. test_case_guards.py -k MS-RR-S0: 12 passed.

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `fallback_tool_outputs.echo.echo_type` added "TTE": the report is transthoracic and the discriminator guard requires the vocabulary term (every other MS-RR case has it).
- `action-4-check-drug-interactions.expected_evidence` was empty; written from the stored drug output in policy voice: "Naproxen with high-dose methylprednisolone: gastrointestinal bleeding risk, so stop it or add a proton pump inhibitor".
- `assessment.required_recommendations[0]` formulation must made case-specific by appending "(here periventricular, juxtacortical, infratentorial, spinal cord and left optic nerve: five regions, so no separate DIT is required)", from the KCE DIS line and the stored outputs, as in the other 18 cases.
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders). Initial labs interpretation edited to drop the antibody results: removed "All other results, including AQP4-IgG and MOG-IgG by cell-based assay, are within reference ranges or negative.".
- `assessment.required_recommendations[3]` pre-DMT screening: HIV removed from the tests to order and noted as already non-reactive, since the required mimic panel reports it (HIV-1/2 Ag/Ab combination assay: Negative), as the RM, RP and RS cases do.

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

## Library contradictions (25 Oct 2026)

- `order_specialized_test {test_type: ssep}`: 1. Prolonged right tibial cortical P37 latency (46.7 ms) with a normal lumbar N22, indicating central somatosensory conduction delay above the lumbar cord. 2. Normal left tibial and bilateral median responses. (fallback_tool_outputs.specialized_test). Why: rule c: vibration reduced in the right leg from the knee down with a right dorsolateral C4-C5 and a dorsal-column T5-T6 lesion; the library reports a normal study.
- `order_specialized_test {test_type: visual_field_perimetry}`: 1. Diffuse depression of the left visual field, most marked centrally (MD -12.3 dB). 2. Normal right visual field. (followup_outputs[request_visual_field_perimetry]). Why: rule c: acute left optic neuritis with acuity 20/80, a left RAPD and generalized reduction of sensitivity on confrontation; the library reports a normal study.

Checks: perfect agent ok; case guards pass; snapshot diff shows no criterion answer changed; map verified (served without the library).
