# ALS-S08
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 553b128b-525a-47e3-8c7c-a25bd14b20f6 | FIXED | Action criteria reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. `ground_truth.action_criteria`, `followup_outputs`, `ground_truth.sequence_constraints`, `initial_tool_outputs.literature_search` = null. Core studies stay in `initial_tool_outputs` (plan C1; display is CENTRAL 1). |
| d91f9116-520b-4938-be51-4e67baa7aea5 | FIXED | `initial_tool_outputs.body_imaging` rewritten region-pure: per-level cervical and thoracic findings, impression "No cervical or thoracic cord compression, cord signal abnormality or mass." The motor-cortex low T2 signal and the sulcal pattern now sit only in `initial_tool_outputs.mri` (impression item 2). The broken numbering ("2.") is gone. |
| 8c1a9e6d-942f-4f92-8732-bd43a906bb22 | FIXED | Riluzole check moved last. Output: CYP1A2-competition mechanism and the q2-weekly INR schedule removed; "Warfarin: no established pharmacokinetic interaction; check the INR within 1-2 weeks of starting riluzole, as after any new long-term medicine". Must 4 "Check the INR within 1-2 weeks of starting riluzole." Criterion rationale and expected_evidence say the same. `metadata.notes` no longer claims a CYP1A2 interaction. |
| 1466a4e8-45bf-4ebc-82e9-f7941e9f8153 | FIXED | AMX0035 (Relyvrio) removed: `followup_outputs[2].output.alternatives` = []. |
| 18b94541-6b04-47b5-bf6d-7b3c41d7409f | FIXED | `ground_truth.key_clinical_evidence[3]` = K-CK above 5x: "CK 920 U/L is 5.3x ULN, higher than usual in ALS: consider a myopathic contributor clinically, including statin myopathy on atorvastatin, while the neurogenic EMG pattern ... argues against a primary myopathy." Lab interpretation lists "CK 920 U/L (5.3x ULN)". Statin-associated myopathy added to the differential (low) and a CK red herring added with the canonical wording. |
| 8e1531cb-44a9-46f4-8c15-e38068eb698a | FIXED | Respiratory follow-up placed after the core; criterion `action-7` recommended with staging label and rationale; impression "FVC 82% predicted and SNIP 74 cmH2O are within normal limits (NIF -68 cmH2O); baseline for serial monitoring."; reference ranges harmonised (NIF "-60 cmH2O or more negative"). |
| 7bc08482-8baf-4871-8ef7-876e2bbdbbfa | FIXED | Genetic panel kept optional, after the core and after EMG (sequence constraint); TBK1 added so all five genes are reported; canonical negative impression replaces "All values within normal limits". |
| 29717cf6-fbe1-4f9e-8933-8727148963f3 | FIXED | Case comment (pathway order; motor-cortex finding in the spine report): resolved as under 553b128b and d91f9116. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Literature output echoed the criterion's expected_evidence. | FIXED: null; literature criterion deleted (C2). |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were diagnostic actions; no INR must although warfarin is the case's medicine point. | FIXED: rebuilt per C10: MUST-DX, MUST-RESP normal, MUST-RILUZOLE, INR must, MUST-MDT, MUST-GEN sporadic. No bulbar must (tongue fasciculations and brisk jaw jerk, no dysarthria or dysphagia). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Cervical-surgery prohibition with no spondylosis on imaging; functional-dismissal prohibition with no psychiatric history; respiratory prohibition phrased for a symptomatic patient. | FIXED: PROHIB-IMM and PROHIB-RESP normal only. |
| C, E | minor | `ground_truth.key_clinical_evidence` | Generic pearls (2-5x CK, El Escorial EMG, spondylosis without spondylosis) and "July 2026 review" engineering text. | FIXED: K-GC, K-EMG, K-NCS normal, K-CK above 5x with statin, K-RESP normal. |
| D | minor | `initial_tool_outputs.mri.findings[1].signal_characteristics` | "iron deposition in degenerating upper motor neurons": a pathological interpretation inside an imaging descriptor; impression omitted the motor-cortex finding. | FIXED: descriptor "Subtle linear low signal along the precentral gyrus"; impression item 2 reports it; FLAIR added to the corticospinal finding. |
| D | minor | `initial_tool_outputs.specialized_test.quantitative_data` | "meeting the electrodiagnostic criterion for widespread LMN involvement" (criteria judgement inside the report); impression unnumbered. | FIXED: neutral quantitative fields (regions, conduction block none, sensory normal); numbered impression stating chronic change where the findings show it (left FDI) and no conduction block. Stored findings unchanged. |
| A, D | major | `initial_tool_outputs.labs` | Panels "Exclusion studies" (free T4 as a string with a sentence about the case's diagnosis), "Neuromuscular_Panel" holding TSH, B12 and "LFTs (ALT)", "Reviewer baseline rule-out additions"; interpretation names ALS. | FIXED: C13 panels; every stored value kept; added potassium, calcium, albumin, AST, ALP, bilirubin, numeric free T4 1.3 ng/dL, and a "Coagulation" panel with INR 2.4 (warfarin target 2.0-3.0) as the baseline for the INR must; canonical interpretation. |
| C | minor | `ground_truth.action_criteria` | Brain MRI required contrast and protocol; spine required `contrast: false`; lab criterion spellings; label = rationale; free-text citations. | FIXED: C16 arguments, canonical texts and citations. |
| C | minor | `ground_truth.differential` | MMN cited "anti-GM1 negative" and Kennedy "androgen receptor CAG repeat normal", neither tested; no statin myopathy entry despite CK 5.3x on atorvastatin. | FIXED: C8 wording for MMN and Kennedy (very_low); statin-associated myopathy low; IBM very_low; MG very_low; cervical myelopathy with radiculopathy low with supports/against. |
| D | minor | `patient.neurological_exam.additional` | "Combined upper and lower motor neuron signs; no reported toxic exposures." (synthesis; exposures already in the HPI). | FIXED: set to null. |
| B | minor | `metadata.difficulty_rationale` | "3 required tools sufficient" while 4 studies are required. | FIXED: "4 required studies". |
| C | minor | `ground_truth.red_herrings` | Empty although the case carries a statin-related CK confounder. | FIXED: CK red herring added (field_path `initial_tool_outputs.labs.panels`). |
| C | minor | labs | CK 920 U/L is identical to ALS-M02 and ALS-S01 (template value). | FLAGGED: kept per plan C9 (the notes cite the value). |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first, then respiratory function, the gene panel and the riluzole check; the literature step is gone. The motor-cortex low T2 signal now appears only in the brain MRI report, and the spine report describes only the cervical and thoracic spine and cord. The labs are standard panels with the stored values, numeric thyroid tests and a baseline INR of 2.4 on warfarin; CK 920 U/L is reported as 5.3x ULN and the teaching point, red herring and differential now say this is higher than usual for ALS and that statin myopathy can contribute while the neurogenic EMG argues against a primary myopathy. The riluzole check no longer claims a CYP1A2 interaction with warfarin or offers AMX0035: it advises an INR check within 1-2 weeks of starting riluzole and reading LFTs with atorvastatin in mind. The gene panel reports all five genes. Musts are management (diagnosis and disclosure, 3-monthly respiratory monitoring, riluzole with monitoring, INR check, MDT, genetic counselling).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Review UI: show the initial work-up and follow-ups in criterion order (plan 5.1).
- New citation keys per plan 1.1 (criteria pack section 8).

## Open questions for Andrea (judgment calls you could not settle)
- I added a baseline INR (2.4, within the warfarin target) to the labs and a CK red herring; neither is in the plan's S08 entry, both support decisions the plan makes (INR must, K-CK above 5x).
- Mental status records "Anxious about diagnosis" but there is no anxiety disorder; following the plan, no PROHIB-FUNC was added.

## Verification
Adversarial check, 23 October 2026. Read the log, the full `git diff` against HEAD (old and new case flattened field by field), the whole final case, the plan (sections 1-3 and 4 S08) and the notes file.
- All 8 note ids are in the table and each FIXED claim holds in the file: the motor-cortex low T2 signal is only in the brain MRI and the spine report is region-pure (d91f9116, 29717cf6); warfarin has no CYP1A2 claim, the INR check within 1-2 weeks is in the output, the criterion and a must (8c1a9e6d); AMX0035/Relyvrio gone; K-CK above 5x with statin context, statin-associated myopathy low (18b94541); respiratory normal; five-gene panel optional after EMG. No DECLINED or BLOCKED notes.
- Checked: CK 920/174 = 5.3x; INR 2.4 inside the warfarin target is consistent with the medication list; Kennedy very_low with the C8 wording (no untested CAG repeat); no PROHIB-FUNC (no anxiety disorder, only "anxious about diagnosis"); no bulbar must (tongue fasciculations, brisk jaw jerk, no dysarthria); the penicillin allergy is not contradicted anywhere; no banned text.
- Found and fixed (B, minor; same class as S01/S02): MUST-DX and K-GC claimed LMN involvement in all four regions, but chronic neurogenic change is reported only in the left first dorsal interosseous; bulbar, thoracic and lumbosacral muscles show fibrillations and fasciculations only, and the leg exam has fasciculations without wasting. Both now state LMN involvement in the cervical region with active denervation also in bulbar, thoracic and lumbosacral muscles. Gold Coast stays met (UMN signs plus hand wasting and EMG change in the cervical region).
- `perfect_agent.py` -v ok after the change (brain MRI, spine MRI and labs are served from the initial work-up); `case_io.py check` clean for the case (schema, synonym guard; the one failing test in the suite does not name it).

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` added (rows carried no abnormality marker), set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- required_recommendations: must added (statin review for CK 5.3x ULN on atorvastatin).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-5-interpret-labs]`.alternatives: was [CBC, CK, TSH, vitamin_B12]; now [CBC, CK, TSH, vitamin_B12, CMP, folate, inflammatory_markers, coagulation] | [CBC, CK, TSH, vitamin_B12].
- Decision: serve: new first alternative (old order kept as an alternative). The label and rationale name renal and liver function, calcium, folate, ESR and CRP (liver baseline before riluzole, inflammatory mimics); the order named only CBC, CK, TSH and B12, so the CMP and inflammatory results the evidence cites were not returned. The INR on warfarin is read too, and a must checks the INR after riluzole starts.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although the case contradicts it now get a case-specific report; every other off-pathway order still gets the library normal.

- `analyze_csf special_tests=[NfL, NfH]` -> `fallback_tool_outputs.csf`. Why: CSF neurofilaments are raised in ALS; the library reported NfL 420 pg/mL, normal. Basic CSF acellular, protein 43 mg/dL, NfL 3,300 pg/mL..
- `order_specialized_test test_type=emg_single_fiber` -> `fallback_tool_outputs.specialized_test`. Why: the stored EMG shows chronic reinnervation; single-fibre EMG then shows raised fibre density and jitter, not the library's normal study.
- `order_specialized_test test_type=muscle_biopsy` -> `followup_outputs[request_muscle_biopsy]`. Why: muscle in ALS shows neurogenic grouped atrophy; the library reported normal muscle.
- `perform_clinical_assessment assessment_type=performance_status` -> `fallback_tool_outputs.clinical_assessment`. Why: the library reported Karnofsky 100 / ECOG 0 with no limitation; the history documents retired; left hand weakness limits gripping tasks (Karnofsky 80, ECOG 1).
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[request_gait_and_balance_timed]`. Why: the exam documents a mildly wide-based gait with slight right circumduction; the library reported a normal timed gait (mild slowing stored).
- `order_advanced_imaging modality=DTI_tractography` -> `followup_outputs[request_dti_tractography]`. Why: the stored MRI shows corticospinal tract T2/FLAIR hyperintensity; DTI cannot show normal corticospinal anisotropy.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALS-` pass; every mapped order answered without the library (`verify.py`, map_ALS); no criterion answer changed (snapshot diff).
