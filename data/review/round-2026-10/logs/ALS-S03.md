# ALS-S03
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 97ae7f3b-16ad-4ecf-b94f-6eb7e46702dd | FIXED | Plan C1. `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs, then respiratory, genetics, riluzole); `followup_outputs` now respiratory, genetics, riluzole; literature criterion and stored output removed; soft `sequence_constraints` EMG before genetics and before riluzole. The core work-up stays in `initial_tool_outputs`; showing it as Steps 1-4 needs the central UI change (plan 5.1). |
| dcd17b55-4f67-442a-9334-b2ac7d5d1818 | FIXED | Plan C6. `initial_tool_outputs.specialized_test.findings[5]` (Motor NCS) now reads "Median, ulnar, peroneal and tibial motor studies: CMAP amplitudes reduced in the wasted hand muscles, distal latencies and conduction velocities normal, no conduction block and no temporal dispersion."; the impression states "no conduction block". |
| be205e95-71b1-4415-b0a3-55a8066a12fa | FIXED | Plan C1, C3. Riluzole check last in `followup_outputs` and `action_criteria`, after EMG by soft constraint; AMX0035 removed (`alternatives` empty). |
| 1a295b03-b3a4-4d69-8903-f8991e1c95f6 | FIXED | Plan C3. The initial `drug_interactions.general` block (grapefruit/CYP1A2 text that repeated the old expected evidence) is deleted (`initial_tool_outputs.drug_interactions` = null); the single riluzole output (`followup_outputs[2]`) now holds the consistent treatment-safety content (no regular medicines; transaminase schedule with the 5x ULN stop rule; report febrile illness). |
| c6663c68-f289-45ac-8e0a-fe821c516625 | FIXED | Plan C4. Respiratory criterion `action-7` reframed as staging (recommended) and placed after the core; output ranges and impression rewritten (normal: FVC 84%, SNIP 76 cmH2O, baseline for serial monitoring); MUST-RESP normal and PROHIB-RESP normal. |
| 140104fe-d7c1-4430-b740-79535a641633 | FIXED | Plan C5. Genetic output now reports the full panel: C9orf72 negative plus SOD1, TARDBP, FUS and TBK1 "No pathogenic or likely pathogenic variant detected", with the canonical negative impression. |
| 606775a0-7d41-4db9-9f22-2379797cf15c | FIXED | Case comment "pathway diagnostico errato": same fix as 97ae7f3b (plan C1). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | "Examination shows combined upper and lower motor neuron signs." and the same synthesis in the exam `additional` field. | FIXED: sentence removed from the HPI; `additional` now lists only the observed fasciculations (tongue, deltoids, calves). |
| D | major | `initial_tool_outputs.literature_search` | Stored output echoed the literature criterion's expected evidence and answered any query. | FIXED: null; criterion `action-1-search-medical-literature` deleted (plan C2). |
| B | major | `initial_tool_outputs.specialized_test.impression` | Impression claimed "chronic reinnervation" in all four regions, but the findings record chronic neurogenic change (large MUPs) only in the first dorsal interosseous muscles; tongue, thoracic and tibialis anterior show fibrillations and fasciculations only. | FIXED: impression rewritten to match the findings (active denervation in four regions, fasciculations in tongue and TA, chronic change in FDI); findings unchanged. MUST-DX and K-GC say LMN involvement in the bulbar (clinical atrophy and fasciculations plus EMG) and cervical regions with active denervation also in thoracic and lumbosacral muscles. Gold Coast is met (UMN plus LMN signs in the bulbar and cervical regions). |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions (lab list with HIV, RPR, SPEP, anti-GM1, CAG repeat; brain MRI "to exclude cervical myelopathy"; "Apply Awaji/Gold Coast"); cervical-surgery prohibition without spondylosis on imaging; functional-dismissal prohibition without a psychiatric element. | FIXED per C10: MUST-DX, MUST-RESP normal, MUST-BULBAR signs (bilateral tongue atrophy), MUST-RILUZOLE, MUST-MDT, MUST-GEN; PROHIB-IMM, PROHIB-RESP normal. |
| C | major | `ground_truth.key_clinical_evidence` | El Escorial EMG pearl, generic "2-5x" CK pearl, spondylosis pearl without spondylosis, "July 2026 review" engineering pearl. | FIXED per C14: K-GC, K-EMG, K-NCS normal, K-CK at or below 5x (840 U/L, 4.8x), K-RESP. |
| C | minor | `ground_truth.differential` | MMN cited "anti-GM1 negative" and Kennedy "normal androgen receptor CAG repeat" (neither tested); MG cited "no fatigability or ocular signs" (not examined); cervical myelopathy and IBM left low although the work-up excludes them. | FIXED: key_features from case data; MMN low; cervical spondylotic myelopathy, IBM, MG, Kennedy very_low. |
| B | major | `initial_tool_outputs.labs` | No blood count, renal or liver results although the criterion required CBC and CMP; "Exclusion studies" panel with free T4 as a string and engineering text; "Reviewer baseline rule-out additions"; interpretation named ALS. | FIXED per C13: stored values kept (CK 840, TSH 2.3, ESR 8, CRP 2, B12 420, folate 10); added normal Hb 14.9, WBC 6.8, platelets 222, Na 138, K 4.0, creatinine 1.1, glucose 92, calcium 9.2, albumin 4.3, ALT 35, AST 39, ALP 90, bilirubin 0.8, free T4 1.1 ng/dL. |
| A | major | `ground_truth.action_criteria[action-3, action-4, action-5]` | Brain MRI required `contrast: true, protocol: standard`; spine `contrast: false`; labs nine assay names; labels identical to rationales; free-text citations. | FIXED per C16/C13. |
| E | minor | `initial_tool_outputs.specialized_test.findings[4]`, `.impression` | Sensory NCS "Normal."; "disorder of lower anterior horn cells", em dash, missing period. | FIXED: "Median, ulnar and sural sensory responses normal bilaterally"; "anterior horn cells". |
| E | minor | `initial_tool_outputs.mri.impression` | Unnumbered, no final period. | FIXED: numbered 1-2. |
| D | minor | `initial_tool_outputs.body_imaging.impression` | "to explain the deficit" referred to the clinical picture. | FIXED: modality-only wording. |
| B | minor | `metadata.notes`, `metadata.difficulty_rationale` | "young construction worker" for a 55-year-old; "3 required tools". | FIXED. |
| B | minor | `initial_tool_outputs.labs` | ESR 8, CRP 2, B12 420, folate 10 identical to other ALS cases (template carry-over). | FLAGGED: stored values kept. |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first (required), then baseline respiratory function (recommended, normal: FVC 84%, SNIP 76 cmH2O), the ALS gene panel after counselling (optional, all five genes negative) and the riluzole check (recommended), with EMG before genetics and riluzole as soft constraints; the literature step is gone. The EMG report now states the motor conduction studies explicitly (reduced CMAPs in the wasted hand muscles, normal latencies and velocities, no conduction block, no temporal dispersion), and its impression matches its own findings (active denervation in four regions, chronic change in the hand muscles). The duplicate "general" interaction block is gone; the single riluzole check (no regular medicines) gives the transaminase schedule and no longer offers AMX0035. The HPI and exam no longer state the UMN/LMN synthesis. Musts are now management (disclosure by Gold Coast criteria, 3-monthly FVC/SNIP with symptom screening, speech and swallowing assessment for the tongue atrophy, riluzole with monitoring, MDT, genetic counselling). The labs now include a full blood count and metabolic panel (added values normal) and CK 840 U/L is reported as 4.8x ULN.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Review UI: show `initial_tool_outputs` in criterion order so the core work-up reads as Steps 1-4 (plan 5.1).
- Criteria pack section 8: add `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)
- The exam motor field gives no MRC grades ("Bilateral arm and leg weakness") and no bulbar symptoms are recorded either way (no dysarthria or dysphagia mentioned). I did not invent grades or symptoms. Should the case author add MRC grades and state whether speech and swallowing are affected?

## Verification
Adversarial check, 23 October 2026. Read the log, the full `git diff`, the whole final case, the plan (sections 2, 3, 4 S03) and the notes file.
- All 7 note ids are in the table; each FIXED claim holds in the file: motor NCS now states CMAPs, latencies, velocities and no conduction block (dcd17b55); the initial "general" interaction block is null and the single riluzole output is consistent (1a295b03); respiratory normal; five-gene panel; AMX0035 gone. No DECLINED or BLOCKED notes.
- The rewritten EMG impression matches the findings (large MUPs only in FDI); MUST-DX and K-GC claim LMN involvement only where the exam or EMG shows it (bulbar: tongue atrophy and fasciculations; cervical: thenar wasting with active and chronic denervation). The new exam `additional` text (fasciculations in tongue, deltoids and calves) restates findings already in the cranial nerve and motor fields; nothing invented. Former smoker who quit 5 years ago: no current CYP1A2 induction, so no smoking point is needed in the riluzole output. CK ratio 840/174 = 4.8 checked. No banned text left.
- Found nothing to change.
- `perfect_agent.py ALS-S03 -v` ok; `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
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

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although the case contradicts it now get a case-specific report; every other off-pathway order still gets the library normal.

- `analyze_csf special_tests=[NfL, NfH]` -> `fallback_tool_outputs.csf`. Why: CSF neurofilaments are raised in ALS; the library reported NfL 420 pg/mL, normal. Basic CSF acellular, protein 41 mg/dL, NfL 4,300 pg/mL..
- `order_specialized_test test_type=emg_single_fiber` -> `fallback_tool_outputs.specialized_test`. Why: the stored EMG shows chronic reinnervation; single-fibre EMG then shows raised fibre density and jitter, not the library's normal study.
- `order_specialized_test test_type=muscle_biopsy` -> `followup_outputs[request_muscle_biopsy]`. Why: muscle in ALS shows neurogenic grouped atrophy; the library reported normal muscle.
- `perform_clinical_assessment assessment_type=performance_status` -> `fallback_tool_outputs.clinical_assessment`. Why: the library reported Karnofsky 100 / ECOG 0 with no limitation; the history documents unable to work in construction because of arm and leg weakness (Karnofsky 60, ECOG 2).
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[request_gait_and_balance_timed]`. Why: the exam documents a spastic gait; the library reported a normal timed gait (moderate slowing stored).
- `order_advanced_imaging modality=DTI_tractography` -> `followup_outputs[request_dti_tractography]`. Why: the stored MRI shows corticospinal tract T2/FLAIR hyperintensity; DTI cannot show normal corticospinal anisotropy.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALS-` pass; every mapped order answered without the library (`verify.py`, map_ALS); no criterion answer changed (snapshot diff).
