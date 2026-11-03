# ALS-M04
Reviewer status: R1 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| c7a0d7f8-ddb8-41f6-b17b-7d55dd2e9cd1 | FIXED | `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs first, then optional CSF); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. Core studies stay in `initial_tool_outputs` (plan C1). |
| b8ed6243-1422-4877-80f4-115e52d9ff05 | FIXED | Riluzole/tamoxifen check last (`action_criteria[7]`, `followup_outputs[2]`), soft constraint after EMG; output rewritten (tamoxifen and riluzole both raise transaminases, LFTs shared with oncology; sertraline-tamoxifen CYP2D6 note kept; AMX0035 "if liver toxicity concern" and edaravone removed). |
| 74fd510e-c9d0-439d-95d3-cbe0bc756d8e | FIXED | `action-9-analyze-csf` stays optional (`action_criteria[4]`), relabelled as targeted to the leptomeningeal/paraneoplastic question; rationale states CSF is not routine and does not diagnose ALS; CSF interpretation rewritten without dict dumps or diagnosis. |
| 1af03245-5363-4229-839a-db8c1405e006 | FIXED | Genetic panel optional, after the core and counselling (`action_criteria[6]`, `followup_outputs[1]`). |
| a578c958-8aa3-47c7-a142-f28c1d50a9d6 | FIXED | Respiratory function recommended, after the diagnostic core (`action_criteria[5]`, `followup_outputs[0]`), relabelled as staging. |
| e8775879-6037-47e6-9e6a-f968ff243422 | FIXED | "Paraneoplastic antibody panel was ordered and results are pending" deleted from `patient.history_present_illness`; the labs report the antibodies in a "Paraneoplastic antibodies" panel (anti-Hu and anti-Yo negative as stored; anti-Ri, anti-amphiphysin and anti-CV2/CRMP5 added as negative). |
| 991657f8-6496-4db0-8a4d-5bdba698876a | FIXED | Same as c7a0d7f8. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | HPI gave the brain and spine MRI results ("no ... leptomeningeal disease but ... corticospinal tract signal changes") and a reasoning sentence about the differential. | FIXED: kept the referral reason (oncologist's concern) and the prior oncology review (CT chest, breast exam; not scored); results and reasoning deleted. |
| B | major | `initial_tool_outputs.mri`, `initial_tool_outputs.body_imaging` | Identical impression in brain and spine reports; spine content ("No spinal cord compression or epidural disease", "Entire neuraxis") in the brain report; brain content ("No brain ... metastases") in the spine report; contrast not stated consistently although enhancement was reported; radiation remark in the brain report. | FIXED: brain report covers brain, meninges and cranial nerves after gadolinium; spine report (`contrast` true) covers cord, epidural space, vertebrae and spinal meninges; both impressions numbered. |
| D | minor | `initial_tool_outputs.csf.interpretation` | Python dict dumps and "CSF does not confirm ALS". | FIXED: plain values, pattern statement, hedged cytology sentence. |
| E | minor | `initial_tool_outputs.labs` | "Exclusion studies" with string free T4; "Reviewer baseline rule-out additions"; interpretation naming ALS; no liver tests although tamoxifen and riluzole both affect them; no calcium in a cancer survivor. | FIXED: panels per C13 with stored values; added potassium 4.0, calcium 9.6, albumin 4.2, ALT 24, AST 27, ALP 69, bilirubin 0.5, free T4 1.3; "Paraneoplastic antibodies" panel; interpretation "CK 542 U/L (3.2x ULN)". |
| C | minor | `initial_tool_outputs.labs.panels.Paraneoplastic antibodies` | A breast-cancer paraneoplastic screen limited to anti-Hu and anti-Yo omits the antibodies most linked to breast cancer. | FIXED: anti-Ri, anti-amphiphysin and anti-CV2/CRMP5 added as negative. |
| B | minor | `initial_tool_outputs.specialized_test` | "3 definite ... bulbar early/possible" (Awaji wording in the report); em dash; "Pulmonary function testing recommended."; prose impression. | FIXED. |
| D | major | `initial_tool_outputs.literature_search`, `action-1-search-medical-literature` | Literature echo of expected evidence. | FIXED: deleted. |
| B | minor | `followup_outputs[0].output` | SNIP women limit ">70"; generic impression. | FIXED: ranges per C4, `flag`, canonical normal impression. |
| B | minor | `followup_outputs[1].output` | TBK1 missing; generic impression. | FIXED. |
| A | minor | `ground_truth.action_criteria[3]` | Lab criterion required "paraneoplastic", which is not the advertised vocabulary term. | FIXED: three alternatives (`paraneoplastic_panel`, `paraneoplastic`, `paraneoplastic_antibodies`), each with the core panels; all three verified to return the case labs. |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions and an untested lab list (HIV, RPR, SPEP, anti-GM1, CAG repeat); cervical-surgery prohibition with a normal spine. | FIXED: MUST-DX, MUST-RESP normal, MUST-BULBAR signs, MUST-RILUZOLE, MUST-MDT, MUST-GEN; prohibitions PROHIB-IMM, PROHIB-RESP normal, PROHIB-FUNC (anxiety disorder). |
| C | major | `ground_truth.differential` | Paraneoplastic motor neuronopathy left moderate after negative antibodies, CSF and imaging; MMN citing untested anti-GM1; no leptomeningeal entry although the case raises it; MG "decrement" not tested. | FIXED: paraneoplastic low, leptomeningeal metastasis very_low, MMN low, cervical radiculopathy low, MG low, IBM very_low, and radiation-induced brachial plexopathy very_low (added: she had breast radiation), all with case data. |
| E | minor | `ground_truth.key_clinical_evidence` | Template pearls (July 2026, 2-5x, El Escorial, spondylosis without spondylosis). | FIXED: K-GC, K-EMG, K-NCS normal, K-CK 3.2x, K-RESP, plus a pearl on the oncological exclusion. |
| C | minor | `ground_truth.red_herrings` | Empty although the breast cancer history is the case's central confounder. | FIXED: red herring added on `patient.clinical_history.past_medical_history[0]`. |
| A | minor | `ground_truth.action_criteria` | C16 mechanics and citation format; CSF citation. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The work-up now opens with EMG/NCS, brain MRI, spine MRI and bloods including a paraneoplastic antibody panel (all required), then CSF with cytology and flow cytometry as an optional, targeted step because of the breast cancer, then baseline respiratory function (recommended), the gene panel (optional) and the riluzole check (recommended); the literature step is gone. The HPI keeps the oncologist's concern but no longer gives the MRI results or a "pending" antibody panel. The brain and spine MRI reports are now separate and region-pure, both after gadolinium, with no metastasis, leptomeningeal enhancement, epidural disease or cord lesion. The CSF is acellular with protein 48 mg/dL and negative cytology and flow cytometry. Labs are regrouped with liver tests and calcium added (normal), CK 542 U/L (3.2x ULN) and a five-antibody paraneoplastic panel, all negative. The riluzole check says tamoxifen can also raise transaminases (share LFTs with oncology) and keeps the existing sertraline-tamoxifen CYP2D6 note for oncology. Musts are Gold Coast diagnosis and disclosure, 3-monthly respiratory monitoring, speech and swallowing assessment (tongue atrophy), riluzole with SmPC monitoring, MDT and genetic counselling; prohibitions cover immunotherapy, stopping respiratory monitoring and attributing the deficits to her anxiety disorder. Paraneoplastic disease is now low and leptomeningeal metastasis very low, with a new radiation-plexopathy entry (very low) and a breast-cancer red herring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1.
- Review UI: initial work-up in criterion order (plan 5.1).
- Lab matching (plan 5.4): until `_contains_required` uses `normalize_analyte`, the three paraneoplastic spellings need separate alternatives.

## Open questions for Andrea (judgment calls you could not settle)

- The plan gives no M04-specific must for oncology. Sharing the diagnosis and the liver-test plan with her oncologist (tamoxifen continues) is in the riluzole check output and the DI criterion, not in the musts; add a must if you want it scored by the physician panel.
- Three antibodies were added to the paraneoplastic panel (as negative) so that the panel matches what a breast-cancer screen would contain.

## Verification

Checked: every note id of the case is in the table and each FIXED claim holds in the file (criteria order and tiers per plan 3.1, follow-ups respiratory, genetics, riluzole; literature and initial DI null; both soft constraints; stop rule unchanged); stored lab and respiratory values unchanged against HEAD (only free T4 string made numeric, plan C13); CK multiple recomputed; HPI free of scored results; musts, prohibitions and differential against the plan's per-case decisions; no AMX0035, edaravone, grapefruit, El Escorial, untested anti-GM1/CAG, "July 2026" or new dashes; perfect_agent.py and case_io.py check clean after the changes.

Found and changed:
- EMG impression item 1 and the EMG criterion `expected_evidence` claimed chronic reinnervation in the thoracic region; the thoracic finding is T6-T8 paraspinal fibrillations with sparse fasciculations only. Now chronic change in cervical and lumbosacral limb muscles, fibrillation potentials in cervical (C6-C8) and thoracic paraspinals.
- `initial_tool_outputs.body_imaging`: the spine MRI answers a leptomeningeal question in a patient with leg weakness, but its region was "cervical and thoracic spine" while it reported "nerve root" enhancement. Region set to "cervical, thoracic and lumbosacral spine"; findings[1] and [2] and impression item 2 now name the cauda equina explicitly (no compression, no enhancement). No result changed.
- `metadata.difficulty_rationale` "Mn-typical EMG" (reads as manganese): now "an EMG typical of motor neuron disease".

PROHIB-FUNC is supported (anxiety disorder on sertraline); CSF optional with cytology and flow cytometry, both reported; CSF/serum glucose ratio 60/88 = 0.68 checked.

## Condition audit (ALS lead, 23 Oct 2026)
- `ground_truth.key_clinical_evidence[2]` (K-NCS): "or SBMA" removed. SBMA is X-linked and affects men; the plan's C8 already drops the Kennedy entry in women, so the pearl named a mimic that cannot apply (flagged by the S02, S04, S07 and S09 verifiers as a class).
- `followup_outputs[0].output.findings[*].is_abnormal` replaces the `flag` low/normal field, set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but thoracic paraspinals (T6-T8) show fibrillations and sparse fasciculations only. Regions now: bulbar (tongue atrophy and fasciculations, clinical), cervical and lumbosacral, with active denervation also in thoracic paraspinal muscles. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 ALS cases after the change: clean.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- required_recommendations: must added (oncology liaison).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-5-interpret-labs]`.alternatives: was [CBC, CK, TSH, vitamin_B12, paraneoplastic_panel] | [CBC, CK, TSH, vitamin_B12, paraneoplastic] | [CBC, CK, TSH, vitamin_B12, paraneoplastic_antibodies]; now [CBC, CK, TSH, vitamin_B12, paraneoplastic_panel, CMP, folate, inflammatory_markers] | [CBC, CK, TSH, vitamin_B12, paraneoplastic_panel] | [CBC, CK, TSH, vitamin_B12, paraneoplastic] | [CBC, CK, TSH, vitamin_B12, paraneoplastic_antibodies].
- Decision: serve: new first alternative (old order kept as an alternative). The label and rationale name renal and liver function, calcium, folate, ESR and CRP (liver baseline before riluzole, inflammatory mimics); the order named only CBC, CK, TSH and B12, so the CMP and inflammatory results the evidence cites were not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although the case contradicts it now get a case-specific report; every other off-pathway order still gets the library normal.

- `order_specialized_test test_type=emg_single_fiber` -> `fallback_tool_outputs.specialized_test`. Why: the stored EMG shows chronic reinnervation; single-fibre EMG then shows raised fibre density and jitter, not the library's normal study.
- `order_specialized_test test_type=muscle_biopsy` -> `followup_outputs[request_muscle_biopsy]`. Why: muscle in ALS shows neurogenic grouped atrophy; the library reported normal muscle.
- `perform_clinical_assessment assessment_type=performance_status` -> `fallback_tool_outputs.clinical_assessment`. Why: the library reported Karnofsky 100 / ECOG 0 with no limitation; the history documents continues desk work with difficulty typing and using a mouse (Karnofsky 80, ECOG 1).
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[request_gait_and_balance_timed]`. Why: the exam documents a mildly spastic gait with reduced knee flexion; the library reported a normal timed gait (mild slowing stored).
- `order_advanced_imaging modality=DTI_tractography` -> `fallback_tool_outputs.advanced_imaging`. Why: the stored MRI shows corticospinal tract T2/FLAIR hyperintensity; DTI cannot show normal corticospinal anisotropy.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALS-` pass; every mapped order answered without the library (`verify.py`, map_ALS); no criterion answer changed (snapshot diff).
