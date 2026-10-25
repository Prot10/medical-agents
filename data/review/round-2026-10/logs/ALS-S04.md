# ALS-S04
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 9f81aef5-a257-4bf1-ae15-5de78168d7b5 | FIXED | Plan C1. `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs, then respiratory, genetics, riluzole); `followup_outputs` now respiratory, genetics, riluzole; literature criterion and stored output removed; soft `sequence_constraints` EMG before genetics and before riluzole. The core work-up stays in `initial_tool_outputs`; showing it as Steps 1-4 needs the central UI change (plan 5.1). |
| 01ec92d7-5996-4119-93b6-0017b98cae94 | FIXED | Plan C6. Motor NCS finding added to `initial_tool_outputs.specialized_test.findings` ("Median, ulnar, peroneal and tibial motor studies: CMAP amplitudes reduced in the wasted hand muscles, distal latencies and conduction velocities normal, no conduction block and no temporal dispersion."); the impression states "no conduction block". |
| 99db8ba8-61a6-4113-8220-6b129ca397d4 | FIXED | Plan C1, C3. Riluzole check last in `followup_outputs` and `action_criteria`, after EMG by soft constraint; AMX0035 removed (`alternatives` empty); output rebuilt (hydrochlorothiazide and calcium carbonate: no clinically significant interaction; transaminase schedule; febrile illness). |
| 7cf92fbd-8fa0-4b0e-8961-0797795fef40 | FIXED | Plan C4, C10. Respiratory output relabelled as reduced (FVC 70%, SNIP 46 cmH2O against the women's limit of 60) with canonical ranges; criterion `action-7` reframed as staging (recommended); `assessment.required_recommendations[1]` refers to the respiratory/NIV service now with overnight oximetry or capnography and repeat FVC/SNIP within 3 months; prohibition "Do not wait for FVC to fall below 50%..." added. |
| 35534ccc-a1e1-4626-8ca0-31f6c4269f7b | FIXED | Plan C10, option "revise the wording" chosen (the history was not changed: no dysphagia was intended). The must "Obtain a swallowing evaluation ... given dysphagia and aspiration risk" and the prohibition "Do not continue oral feeding ... given documented dysphagia" are deleted; `assessment.required_recommendations[2]` now reads "Arrange a speech and language therapy assessment of speech and swallowing, with communication support, and monitor weight and swallowing at each review." No PROHIB-SWALLOW. |
| 56bf56d7-d683-4602-a09e-a35b26f7e978 | FIXED | Plan C5. Genetic output now reports the full panel: C9orf72 negative plus SOD1, TARDBP, FUS and TBK1 "No pathogenic or likely pathogenic variant detected", with the canonical negative impression. |
| 3412b2ae-fd64-41ef-b935-aa45aab0ba14 | FIXED | Plan C8. "Progressive bulbar palsy variant" removed from `differential`; `key_clinical_evidence[0]` names the bulbar-onset ALS phenotype. |
| 4d9b6abe-1d63-4de3-afc8-b60301f17a6a | FIXED | Case comment (pathway wrong; no explicit absence of conduction block; musts speak of dysphagia not documented): the three points are fixed as in 9f81aef5 (C1), 01ec92d7 (C6) and 35534ccc (C10). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.neurological_exam.additional` | "Combined bulbar and limb upper and lower motor neuron signs in an elderly patient." (diagnostic synthesis). | FIXED: trimmed to the observed finding (fasciculations at rest in tongue, arms and legs). |
| D | major | `initial_tool_outputs.literature_search` | Stored output echoed the literature criterion's expected evidence and answered any query. | FIXED: null; criterion `action-1-search-medical-literature` deleted (plan C2). |
| B | major | `initial_tool_outputs.specialized_test.impression` | Claimed "chronic reinnervation" in all four regions, but the findings record chronic change (large MUPs) only in the first dorsal interosseous muscles; tongue, thoracic paraspinal and tibialis anterior show fibrillations (and tongue fasciculations) only. | FIXED: impression rewritten to match the findings; findings unchanged. MUST-DX and K-GC state LMN involvement in the bulbar and cervical regions with active denervation also in thoracic and lumbosacral muscles; Gold Coast is met (UMN plus LMN signs in the bulbar and cervical regions). |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions (EMG, brain MRI "to exclude cervical myelopathy", a lab list with HIV, RPR, SPEP, anti-GM1 and "CAG repeat in males" in a woman, "Apply Awaji/Gold Coast"); cervical-surgery prohibition without spondylosis on imaging; functional-dismissal prohibition without a psychiatric element. | FIXED per C10: MUST-DX, MUST-RESP reduced, MUST-BULBAR signs, MUST-RILUZOLE, MUST-MDT, MUST-GEN; PROHIB-IMM, PROHIB-RESP reduced. |
| C | major | `ground_truth.key_clinical_evidence` | El Escorial EMG pearl, generic "2-5x" CK pearl, spondylosis pearl without spondylosis, "July 2026 review" engineering pearl. | FIXED per C14: K-GC, K-EMG, K-NCS normal, K-CK (680 U/L, 4.0x), K-RESP, K-BULBAR (bulbar onset). |
| C | minor | `ground_truth.differential` | Stroke and cervical myelopathy left low although MRI excludes them; MG cited "no fatigability" (not examined). | FIXED: key_features from case data; MG low; brainstem stroke, cervical spondylotic myelopathy and sarcopenia very_low. |
| B | major | `initial_tool_outputs.labs` | No blood count, renal or liver results although the criterion required CBC and CMP; "Exclusion studies" panel with free T4 as a string and engineering text; "Reviewer baseline rule-out additions"; interpretation named ALS. | FIXED per C13: stored values kept (CK 680, TSH 2.2, ESR 8, CRP 2, B12 420, folate 10); added normal Hb 12.6, WBC 6.1, platelets 274, Na 137, K 3.8, creatinine 0.8, glucose 96, calcium 10.1 (high-normal, consistent with a thiazide plus calcium carbonate), albumin 3.9, ALT 18, AST 26, ALP 95, bilirubin 0.6, free T4 1.2 ng/dL. |
| A | major | `ground_truth.action_criteria[action-3, action-4, action-5]` | Brain MRI required `contrast: true, protocol: standard`; spine `contrast: false`; labs nine assay names; labels identical to rationales; free-text citations. | FIXED per C16/C13. |
| E | minor | `initial_tool_outputs.specialized_test`, `initial_tool_outputs.mri` | Sensory NCS "Normal."; "lower anterior horn cells", em dash; MRI impression unnumbered, "No other pathology" without a period, T2 field "Bilateral symmetric". | FIXED: sensory responses named; "anterior horn cells"; MRI impression numbered 1-3 with explicit negatives; T2 "Bilateral symmetric hyperintensity". |
| D | minor | `initial_tool_outputs.body_imaging.impression` | "to explain the deficit" referred to the clinical picture. | FIXED: modality-only wording. |
| B | minor | `metadata.difficulty_rationale` | "3-4 required tools". | FIXED. |
| B | minor | `initial_tool_outputs.labs` | ESR 8, CRP 2, B12 420, folate 10 identical to other ALS cases (template carry-over). | FLAGGED: stored values kept. |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first (required), then baseline respiratory function (recommended), the ALS gene panel after counselling (optional, all five genes negative) and the riluzole check (recommended), with EMG before genetics and riluzole as soft constraints; the literature step is gone. The EMG report now includes motor conduction studies (reduced CMAPs in the wasted hand muscles, normal latencies and velocities, no conduction block) and its impression matches its own findings. The history still documents no dysphagia, so the musts ask for a speech and language therapy assessment of speech and swallowing with weight monitoring instead of claiming documented dysphagia, and the feeding prohibition is removed. Respiratory function is reported as reduced (FVC 70%, SNIP 46 cmH2O) and the musts refer her to the respiratory/NIV service now. "Progressive bulbar palsy" is named as the phenotype rather than a competing diagnosis. The riluzole check no longer offers AMX0035. Labs now include a full blood count and metabolic panel (added values normal) and CK 680 U/L is reported as 4.0x ULN.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Review UI: show `initial_tool_outputs` in criterion order so the core work-up reads as Steps 1-4 (plan 5.1).
- Criteria pack section 8: add `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)
- The HPI is two sentences and the motor exam gives no MRC grades or leg findings beyond fasciculations; the order of onset (speech before arms) is implied only by the label "bulbar-onset". I did not invent history. A fuller HPI (onset sequence, swallowing, weight) would make the case easier to review.

## Verification
Adversarial check, 23 October 2026. Read the log, the full `git diff`, the whole final case, the plan (sections 2, 3, 4 S04) and the notes file.
- All 8 note ids are in the table; each FIXED claim holds in the file: motor NCS with no conduction block (01ec92d7); the dysphagia must and the feeding prohibition are gone and the bulbar-signs SLT must is in place, with no dysphagia added to the history and no PROHIB-SWALLOW (35534ccc, 4d9b6abe); reduced respiratory category against the women's SNIP limit, no AAN marker (SNIP 46); PBP removed from the differential; five-gene panel; AMX0035 gone. No DECLINED or BLOCKED notes.
- EMG impression matches the findings; MUST-DX and K-GC claim LMN involvement only in the bulbar and cervical regions (hand intrinsic atrophy is on the exam, so "wasted hand muscles" in the motor NCS is supported). Calcium 10.1 on a thiazide plus calcium carbonate is within range. CK ratio 680/170 = 4.0 checked. The sulfa allergy with long-standing hydrochlorothiazide predates the case and nothing new is mandated against it.
- Noted for the lead, not changed: K-BULBAR mentions aspiration risk and early gastrostomy discussion as priorities in a case without documented dysphagia; it is the plan's canonical pearl for bulbar-onset cases and states a general fact, so it was kept. The canonical K-NCS pearl mentions SBMA in a woman (see S02).
- Found nothing to change.
- `perfect_agent.py ALS-S04 -v` ok; `case_io.py check` clean for the case.

## Condition audit (ALS lead, 23 Oct 2026)
- `ground_truth.key_clinical_evidence[2]` (K-NCS): "or SBMA" removed. SBMA is X-linked and affects men; the plan's C8 already drops the Kennedy entry in women, so the pearl named a mimic that cannot apply (flagged by the S02, S04, S07 and S09 verifiers as a class).

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

- `analyze_csf special_tests=[NfL, NfH]` -> `fallback_tool_outputs.csf`. Why: CSF neurofilaments are raised in ALS; the library reported NfL 420 pg/mL, normal. Basic CSF acellular, protein 50 mg/dL, NfL 6,900 pg/mL..
- `order_specialized_test test_type=emg_single_fiber` -> `fallback_tool_outputs.specialized_test`. Why: the stored EMG shows chronic reinnervation; single-fibre EMG then shows raised fibre density and jitter, not the library's normal study.
- `order_specialized_test test_type=muscle_biopsy` -> `followup_outputs[request_muscle_biopsy]`. Why: muscle in ALS shows neurogenic grouped atrophy; the library reported normal muscle.
- `perform_clinical_assessment assessment_type=performance_status` -> `fallback_tool_outputs.clinical_assessment`. Why: the library reported Karnofsky 100 / ECOG 0 with no limitation; the history documents moderate dysarthria with arm weakness and wasting (Karnofsky 50, ECOG 3).
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[request_gait_and_balance_timed]`. Why: the exam documents a spastic gait; the library reported a normal timed gait (moderate slowing stored).
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[request_speech_language_evaluation]`. Why: the exam documents dysarthria; the library reported no motor speech disorder (moderate mixed spastic-flaccid dysarthria stored).
- `order_advanced_imaging modality=DTI_tractography` -> `followup_outputs[request_dti_tractography]`. Why: the stored MRI shows corticospinal tract T2/FLAIR hyperintensity; DTI cannot show normal corticospinal anisotropy.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALS-` pass; every mapped order answered without the library (`verify.py`, map_ALS); no criterion answer changed (snapshot diff).
