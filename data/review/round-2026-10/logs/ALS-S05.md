# ALS-S05
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

Note: the case file was edited in an earlier, interrupted run that wrote no log. This run re-read the whole case against HEAD, audited the edited state, confirmed every change below and ran both checks; no further edit was needed.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b0f4ba1d-9b74-43bc-94cb-da220f6a608f | FIXED | Plan C1. `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs, then respiratory, genetics, riluzole); `followup_outputs` now respiratory, genetics, riluzole; literature criterion and stored output removed; soft `sequence_constraints` EMG before genetics and before riluzole. The core work-up stays in `initial_tool_outputs`; showing it as Steps 1-4 needs the central UI change (plan 5.1). |
| 008369f3-aa8d-432e-95d9-d558c738ef80 | FIXED | Plan C6. Motor NCS finding added to `initial_tool_outputs.specialized_test.findings[5]` ("Median, ulnar, peroneal and tibial motor studies: CMAP amplitudes reduced in the wasted thenar muscles, distal latencies and conduction velocities normal, no conduction block and no temporal dispersion."); `findings[4]` sensory NCS now names the nerves (median, ulnar, sural normal bilaterally); the impression states "Reduced median CMAP amplitudes with normal distal latencies and conduction velocities; no conduction block". |
| 9cc1c53f-4d21-4e6f-8f48-1b67c55ab497 | FIXED | Plan C1, C3. Riluzole check is last in `followup_outputs` (`followup_outputs[2]`) and in `action_criteria` (`action-2-check-drug-interactions`, recommended), after EMG by a soft sequence constraint; criterion label, rationale and expected evidence rewritten (no regular medicines; transaminase schedule with the 5x ULN stop rule). |
| c26321cf-5650-4c79-a459-f89776ef4bbe | FIXED | Plan C3. The initial `drug_interactions.general` block (alcohol and grapefruit "CYP1A2 modulators", which repeated the old expected evidence and shadowed the follow-up) is deleted (`initial_tool_outputs.drug_interactions` = null). The single riluzole output now carries the consistent treatment-safety content: `interactions` "No regular medicines: no drug interaction to assess."; canonical `summary` (transaminases before the first dose, monthly for 3 months, 3-monthly for the rest of the first year, stop if ALT > 5x ULN; report febrile illness, white cell count for neutropenia); `warnings` "Riluzole can raise liver transaminases; it is metabolised by CYP1A2." The grapefruit claim is gone everywhere. |
| 8681a0e0-7baa-40a8-a926-512d776a671f | FIXED | Plan C4. Respiratory criterion `action-7-order-specialized-test` reframed as staging (recommended, label and rationale per C4) and placed after the diagnostic core; `followup_outputs[0]` now has canonical reference ranges (FVC >=80% predicted, SNIP >=70 cmH2O men), `is_abnormal` false, units, and the impression "FVC 88% predicted and SNIP 80 cmH2O are within normal limits; baseline for serial monitoring." MUST-RESP normal and PROHIB-RESP normal added. |
| a147095c-563e-465c-b003-f599222637d3 | FIXED | Plan C5, option "report the full panel". `followup_outputs[1]` now reports C9orf72 negative plus SOD1, TARDBP, FUS and TBK1 "No pathogenic or likely pathogenic variant detected" (findings and `quantitative_data`), with the canonical negative impression replacing "All values within normal limits."; criterion `action-8` optional, label and rationale per C5. |
| 0864c29f-0820-4fea-a408-1e3702d762fb | FIXED | Plan C3. AMX0035 removed from the riluzole output (`followup_outputs[2].output.alternatives` = []). |
| d44d11a1-5727-420b-b621-64d0c07f426f | FIXED | Case comment (wrong pathway; motor NCS and explicit absence of conduction block missing): both points fixed as in b0f4ba1d (C1) and 008369f3 (C6). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | "Examination shows combined upper and lower motor neuron signs." in the HPI and "Combined upper and lower motor neuron signs on examination." in the exam (diagnostic synthesis handed to the agent). | FIXED: HPI sentence removed; `additional` now lists only the observed finding ("Fasciculations at rest in the tongue, arms and legs.", already documented in the cranial nerve and motor fields). |
| D | major | `initial_tool_outputs.literature_search` | Stored output echoed the literature criterion's expected evidence verbatim and was served for any query. | FIXED: null; criterion `action-1-search-medical-literature` deleted (plan C2, ruling 5). |
| B | major | `initial_tool_outputs.specialized_test.impression`, `.quantitative_data.classification` | Impression and classification claimed "chronic reinnervation" in all four regions, but the findings record chronic neurogenic change (large MUPs) only in the first dorsal interosseous muscles; tongue, thoracic paraspinal and right tibialis anterior show fibrillations (and tongue fasciculations) only. | FIXED: impression rewritten to match the findings (active denervation in four regions, tongue fasciculation potentials, chronic change in FDI); classification "Active denervation in 4 body regions"; findings unchanged. MUST-DX and K-GC state UMN plus LMN involvement in the cervical region with fasciculations and active denervation also in bulbar, thoracic and lumbosacral muscles; Gold Coast is met in the cervical region (brisk biceps, bilateral Hoffman, thenar wasting, FDI active plus chronic denervation). |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions (EMG; brain MRI "to exclude cervical myelopathy", which brain MRI cannot; a lab list with HIV, RPR, SPEP, anti-GM1 and CAG repeat; "Apply Awaji/Gold Coast"); cervical-surgery prohibition with no spondylosis on imaging; functional-dismissal prohibition without any psychiatric element; respiratory prohibition framed for a symptomatic patient although baseline is normal. | FIXED per C10: MUST-DX, MUST-RESP normal, MUST-RILUZOLE, MUST-MDT, MUST-GEN (no bulbar must per plan: tongue fasciculations and brisk jaw jerk without dysarthria or dysphagia); PROHIB-IMM, PROHIB-RESP normal. |
| C | major | `ground_truth.key_clinical_evidence` | El Escorial "bulbar plus 2 spinal regions" EMG pearl, generic "2-5x ULN" CK pearl, spondylosis pearl although the spine MRI shows none, "July 2026 review" engineering pearl, NIV pearl stating thresholds as treatment triggers. | FIXED per C14: K-GC (case signs and regions), K-EMG, K-NCS normal sensory, K-CK at or below 5x (760 U/L, 4.4x ULN), K-RESP (FVC 88%, SNIP 80 cmH2O, normal). |
| C | minor | `ground_truth.differential` | MMN cited "anti-GM1 negative" (never tested); MG cited "no fatigability" (not examined); cervical myelopathy and MG left low although the work-up excludes them. | FIXED: key_features rebuilt from case data ("supports/against"); MMN low; cervical spondylotic myelopathy, MG, IBM and hereditary motor neuropathy very_low. |
| B | major | `initial_tool_outputs.labs` | No blood count, renal or liver results although the old criterion required CBC and CMP (and riluzole needs the liver baseline); "Exclusion studies" panel with free T4 as the string "Within reference range" and engineering text; "Reviewer baseline rule-out additions" panel; TSH inside "Neuromuscular_Panel"; interpretation named ALS; abnormal summary "CK: 760" without unit. | FIXED per C13: panels Complete blood count, Comprehensive metabolic panel, Creatine kinase, Thyroid function, Vitamins, Inflammatory markers; stored values kept (CK 760, TSH 1.8, ESR 8, CRP 2, B12 420, folate 10); added normal Hb 15.4 g/dL, WBC 5.6, platelets 210, Na 140, K 4.4, creatinine 0.8 mg/dL, glucose 87, calcium 9.5, albumin 4.5, ALT 24, AST 31, ALP 64, bilirubin 0.9, free T4 1.0 ng/dL; interpretation "Abnormal: CK 760 U/L (4.4x ULN). All other results are within reference ranges." |
| A | major | `ground_truth.action_criteria[action-3, action-4, action-5]` | Brain MRI required `contrast: true, protocol: standard` (a correct non-contrast order failed a required criterion); spine `contrast: false`; labs nine assay names; label identical to rationale in every criterion; free-text and duplicate citations ("Gold Coast; EAN 2024; NICE NG42", "Awaji_2008"). | FIXED per C16/C13/C12: brain MRI `{}`, spine `{"study": "spine_MRI"}`, labs `["CBC", "CK", "TSH", "vitamin_B12"]`; labels, rationales, case-specific expected evidence and bracketed citations per plan. |
| D | minor | `initial_tool_outputs.body_imaging.impression` | "no cord signal change to explain the deficit" referred to the clinical picture. | FIXED: modality-only wording ("no disc or bony compression of the cord or exiting roots, normal cord calibre and no intramedullary signal change"). |
| E | minor | `initial_tool_outputs.mri.impression`, `.findings[0].signal_characteristics.T2` | Impression unnumbered without a final period; T2 field "Bilateral". | FIXED: impression numbered 1-2 with infarct added to the explicit negatives; T2 "Bilateral hyperintensity". |
| E | minor | `initial_tool_outputs.specialized_test.findings[4]`, `.impression` | Sensory NCS "Normal."; "disorder of lower anterior horn cells", em dash, missing period. | FIXED: nerves named; "anterior horn cells". |
| B | minor | `metadata.difficulty_rationale` | "3 required tools" while four studies are required. | FIXED: "the four required studies are sufficient". |
| B | minor | `initial_tool_outputs.labs` | ESR 8, CRP 2, B12 420, folate 10 identical to other ALS cases (template carry-over). | FLAGGED: stored values kept (plan rule). |
| B | minor | `metadata.fallback_tool_kinds.ecg` | Tagged "incidental" while the fallback ECG is a normal report. Metadata only, not shown to the agent. | FLAGGED: not changed. |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first (required), then baseline respiratory function (recommended, normal: FVC 88% predicted, SNIP 80 cmH2O), the ALS gene panel after counselling (optional, all five genes negative: C9orf72, SOD1, TARDBP, FUS, TBK1) and the riluzole check (recommended), with EMG before genetics and before riluzole as soft constraints; the literature step is gone. The EMG report now states the motor conduction studies explicitly (reduced median CMAPs from the wasted thenar muscles, normal distal latencies and conduction velocities, no conduction block, no temporal dispersion), names the normal sensory nerves, and its impression matches its own findings (active denervation in four regions, chronic change in the first dorsal interosseous muscles). The duplicate "general" interaction block with the grapefruit claim is gone; the single riluzole check (no regular medicines) gives the transaminase schedule and no longer offers AMX0035. The HPI and exam no longer state the UMN/LMN synthesis. The musts are now management: disclosure of the diagnosis by Gold Coast criteria, 3-monthly FVC/SNIP with symptom screening, riluzole with liver and febrile-illness monitoring, MDT referral with advance care planning, and genetic counselling; the prohibitions are no immunotherapy and no stopping respiratory monitoring. The labs now include a full blood count and metabolic panel (added values normal) and CK 760 U/L is reported as 4.4x ULN.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Review UI: show `initial_tool_outputs` in criterion order so the core work-up reads as Steps 1-4 (plan 5.1).
- Criteria pack section 6 and 8: respiratory function recommended, not required; add `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]`, `[Bourke_2006]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)
- The HPI is one sentence and records neither bulbar symptoms (speech, swallowing) nor weight, and the motor exam gives no MRC grades. I did not invent history. Following the plan there is no bulbar must, although the exam (tongue fasciculations, brisk jaw jerk) and EMG (tongue fibrillations) show subclinical bulbar involvement; speech and swallowing review is covered only through the MDT must. Should a fuller HPI state whether speech and swallowing are affected, and should subclinical bulbar involvement get the "signs without dysphagia" SLT must?

## Verification
Adversarial check, 23 October 2026. Read the log, the full `git diff`, the whole final case, the plan (sections 2, 3, 4 S05) and the notes file.
- All 8 note ids are in the table; each FIXED claim holds in the file: motor NCS with CMAPs, velocities and no conduction block (008369f3, d44d11a1); the initial "general" interaction block is null and the single riluzole output carries the consistent safety content without grapefruit (c26321cf); respiratory normal; five-gene panel; AMX0035 gone. No DECLINED or BLOCKED notes.
- EMG impression matches the findings (large MUPs only in FDI; "reduced median CMAP amplitudes" agrees with the motor NCS finding on the wasted thenar muscles). MUST-DX and K-GC claim UMN plus LMN involvement only in the cervical region, which meets Gold Coast. No bulbar must follows the plan (tongue fasciculations without atrophy, dysarthria or dysphagia); the worker's open question on this stands. CK ratio 760/174 = 4.4 checked. No banned text left.
- Found nothing to change.
- `perfect_agent.py ALS-S05 -v` ok; `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- required_recommendations: must added (subclinical bulbar involvement).
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

- `ground_truth.action_criteria[action-5-interpret-labs]`.alternatives: was [CBC, CK, TSH, vitamin_B12]; now [CBC, CK, TSH, vitamin_B12, CMP, folate, inflammatory_markers] | [CBC, CK, TSH, vitamin_B12].
- Decision: serve: new first alternative (old order kept as an alternative). The label and rationale name renal and liver function, calcium, folate, ESR and CRP (liver baseline before riluzole, inflammatory mimics); the order named only CBC, CK, TSH and B12, so the CMP and inflammatory results the evidence cites were not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
