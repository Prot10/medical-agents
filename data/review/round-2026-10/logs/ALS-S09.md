# ALS-S09
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| bf54e165-59c0-4534-b21d-e982d0655ee6 | FIXED | Action criteria reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. `ground_truth.action_criteria`, `followup_outputs`, `ground_truth.sequence_constraints`, `initial_tool_outputs.literature_search` = null. Core studies stay in `initial_tool_outputs` (plan C1; display is CENTRAL 1). |
| c925df65-e437-4ed5-bb53-ca473069944f | FIXED | Respiratory output impression "Reduced FVC (76% predicted) and SNIP (54 cmH2O), NIF -48 cmH2O, indicating inspiratory muscle weakness."; reference ranges FVC/FEV1 >=80% predicted, SNIP >=60 cmH2O (women), NIF -60 cmH2O or more negative. Must 2 = refer to the respiratory/NIV service now and discuss NIV (NIF -48 meets an AAN 2009 marker), overnight oximetry or capnography, repeat in 3 months. Prohibition 2 = do not wait for FVC < 50% or symptoms. Criterion `action-7` recommended, staging label and rationale. |
| 1dc3dd2e-5b3b-4bc0-b7c2-5052d9d1e64c | FIXED | `required_recommendations[0]` (the EMG must the note sat on) deleted with the diagnostic musts; must 3 = speech and language therapy swallowing assessment now (aspiration risk, safe consistencies), dietetic review with baseline weight, early gastrostomy discussion while FVC > 50%, with voice and communication support given her profession. Prohibition 3 = do not delay the swallowing assessment. Key evidence[5] = K-BULBAR. |
| 8b821a0b-6345-4993-b543-f545741db394 | FIXED | Riluzole check moved last. Output: the "riluzole may subtly affect CYP metabolism, monitor TSH" claim and the TSH warning removed; "Levothyroxine: no clinically significant interaction expected"; omeprazole as a CYP1A2 inducer that may modestly lower riluzole exposure, no dose change (plan C3 table). Criterion label, rationale, expected_evidence and citations rewritten. |
| 8ad9e0ff-42cd-40a9-aee1-9e93fb54d084 | FIXED | "Progressive bulbar palsy variant" removed from `ground_truth.differential`; the bulbar-onset ALS phenotype is named in key evidence[0]. |
| e37b6b6b-f2e3-4708-bf10-ac353c41983b | FIXED | Genetic output reports all five genes (C9orf72 repeat-primed PCR; SOD1, TARDBP, FUS, TBK1 sequencing, all negative) with the canonical negative impression; criterion label names the full panel. |
| 3a038a83-299d-4a52-ae2b-543144a91259 | FIXED | AMX0035 removed (`followup_outputs[2].output.alternatives` = []). |
| 7d6955d4-b5cf-4a9f-bbfd-98195994dfaa | FIXED | Case comment (pathway; swallowing and NIV planning more visible): resolved as under bf54e165, c925df65 and 1dc3dd2e; respiratory and swallowing musts are now musts 2 and 3, directly after the diagnosis. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Literature output echoed the criterion's expected_evidence. | FIXED: null; literature criterion deleted (C2). |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were diagnostic actions plus a lab list with "androgen receptor CAG repeat in males" in a woman; no NIV or gastrostomy planning. | FIXED: rebuilt per C10: MUST-DX, MUST-RESP with AAN marker, MUST-BULBAR dysphagia (with voice support), MUST-RILUZOLE, MUST-MDT, MUST-GEN sporadic. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Cervical-surgery prohibition without spondylosis; functional-dismissal prohibition without a psychiatric element; oral-feeding prohibition phrased as "documented dysphagia" while she has coughing on thin liquids only. | FIXED: PROHIB-IMM, PROHIB-RESP reduced, PROHIB-SWALLOW. |
| C, E | minor | `ground_truth.key_clinical_evidence` | Generic pearls (2-5x CK, El Escorial EMG, spondylosis without spondylosis), "July 2026 review" engineering text. | FIXED: K-GC (bulbar-onset phenotype named), K-EMG, K-NCS normal, K-CK (540 U/L = 3.2x ULN), K-RESP, K-BULBAR. |
| B, D | minor | `initial_tool_outputs.specialized_test` | Impression claimed chronic reinnervation in four regions while chronic change is reported only in tongue and hand muscles; bulbar finding carried "Consistent with bulbar lower motor neuron involvement"; quantitative field said "meeting the electrodiagnostic criterion". | FIXED: interpretive sentence removed from the finding; numbered impression states chronic change where found, no conduction block, normal sensory studies; neutral quantitative fields. Stored findings otherwise unchanged. |
| A | minor | `initial_tool_outputs.mri` | `signal_characteristics` `{"T2": "Bilateral symmetric"}`; impression missing final punctuation. | FIXED: T2 and FLAIR descriptors; impression wording unchanged in substance. |
| D | minor | `initial_tool_outputs.body_imaging.impression` | "to explain the deficit" (clinical reference); findings empty. | FIXED: per-level findings and plain impression. |
| A, D | major | `initial_tool_outputs.labs` | "Exclusion studies" (free T4 string and diagnosis sentence), "Neuromuscular_Panel" mixing TSH and "LFTs (ALT)", "Reviewer baseline rule-out additions"; interpretation names ALS. | FIXED: C13 panels; all stored values kept; potassium, calcium, albumin, AST, ALP, bilirubin and numeric free T4 1.4 ng/dL added (normal, consistent with stable replacement); canonical interpretation. |
| C | minor | `ground_truth.action_criteria` | Brain MRI required contrast and protocol; spine `contrast: false`; lab spellings; label = rationale; free-text citations. | FIXED: C16 arguments; canonical texts; brain rationale clause on brainstem lesions in bulbar onset; labs clause on levothyroxine. |
| C | minor | `ground_truth.differential` | MG "No fatigability" (not documented in the case); brainstem entry "Brain MRI excludes" without what supports it; MMN key features did not use the case's results. | FIXED: supports/against from the case's data; MMN very_low with C8 wording. |
| D | minor | `patient.neurological_exam.additional` | "Prominent bulbar-onset in professional singer" names the phenotype (synthesis). | FIXED: "Voice changes are particularly distressing to her as a voice professional." |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first, then respiratory function, the gene panel and the riluzole check; the literature step is gone. Respiratory function is reported as reduced (FVC 76%, SNIP 54 cmH2O) with NIF -48 cmH2O, which meets an AAN 2009 marker: the musts now refer her to the respiratory/NIV service and discuss NIV immediately after the diagnosis, followed by a swallowing assessment now, dietetic review and early gastrostomy discussion with voice and communication support. The progressive bulbar palsy entry is gone from the differential (it is her ALS phenotype, named in the key evidence). The riluzole check says levothyroxine does not interact and omeprazole may modestly lower riluzole exposure without a dose change; the TSH-monitoring claim and AMX0035 are gone. The gene panel reports all five genes. Labs are standard panels (CK 540 U/L, 3.2x ULN; numeric thyroid tests normal on replacement).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Review UI: show the initial work-up and follow-ups in criterion order (plan 5.1).
- New citation keys per plan 1.1 (criteria pack section 8).

## Open questions for Andrea (judgment calls you could not settle)
- The brain MRI reports "subtle bilateral T2 signal increase at the hypoglossal nuclei". This is not a recognised MRI sign of ALS and is hard to see in practice; I left it (it is not wrong enough to remove without a reviewer ruling). Consider deleting it on re-review.
- The exam describes the dysarthria as "nasal quality, hypophonic"; hypophonia is more typical of parkinsonism, but reduced loudness also occurs with respiratory and bulbar weakness, so it was left.

## Verification
Adversarial check, 23 October 2026. Read the log, the full `git diff` against HEAD (old and new case flattened field by field), the whole final case, the plan (sections 1-3 and 4 S09) and the notes file.
- All 8 note ids are in the table and each FIXED claim holds in the file: reduced respiratory with an AAN marker (NIF -48; SNIP 54 against the women's limit 60) driving the NIV must and PROHIB-RESP (c925df65); the dysphagia SLT must with voice support sits directly after MUST-DX and MUST-RESP, with PROHIB-SWALLOW and K-BULBAR (1dc3dd2e, 7d6955d4); levothyroxine "no interaction" and omeprazole as a CYP1A2 inducer without dose change (8b821a0b); PBP removed and named as phenotype (8ad9e0ff); five-gene panel; AMX0035 gone. No DECLINED or BLOCKED notes.
- Checked: coughing on thin liquids in the HPI supports the dysphagia variant; CK 540/170 = 3.2x; the historical "consistent normal TSH" is prior follow-up allowed by plan C11; no Kennedy entry in a woman; no banned text.
- Found and fixed (B, minor; same class as S01/S02): MUST-DX and K-GC claimed LMN involvement in all four regions, but chronic change is reported only in the tongue and hand muscles; thoracic paraspinals and leg muscles show fibrillations or fasciculations only, and the legs have fasciculations without wasting. Both now state LMN involvement in the bulbar and cervical regions with active denervation also in thoracic and lumbosacral muscles; K-GC's trailing phrase became "This is a bulbar-onset ALS phenotype."
- Noted, not changed: the worker's open question on the hypoglossal-nucleus T2 signal stands (not an established MRI sign; it also sits awkwardly next to "No brainstem structural lesion"); the canonical K-NCS pearl mentions SBMA in a woman (as S02, S04, S07).
- `perfect_agent.py` -v ok after the change (brain MRI, spine MRI and labs are served from the initial work-up); `case_io.py check` clean for the case (schema, synonym guard; the one failing test in the suite does not name it).

## Condition audit (ALS lead, 23 Oct 2026)
- `ground_truth.key_clinical_evidence[2]` (K-NCS): "or SBMA" removed. SBMA is X-linked and affects men; the plan's C8 already drops the Kennedy entry in women, so the pearl named a mimic that cannot apply (flagged by the S02, S04, S07 and S09 verifiers as a class).
- `followup_outputs[0].output.findings[*].is_abnormal` added (rows carried no abnormality marker), set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- brain MRI: 'hypoglossal nuclei T2 signal' finding and impression item deleted (not an established MRI sign).
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

- `analyze_csf special_tests=[NfL, NfH]` -> `fallback_tool_outputs.csf`. Why: CSF neurofilaments are raised in ALS; the library reported NfL 420 pg/mL, normal. Basic CSF acellular, protein 45 mg/dL, NfL 6,100 pg/mL..
- `order_specialized_test test_type=emg_single_fiber` -> `fallback_tool_outputs.specialized_test`. Why: the stored EMG shows chronic reinnervation; single-fibre EMG then shows raised fibre density and jitter, not the library's normal study.
- `order_specialized_test test_type=muscle_biopsy` -> `followup_outputs[request_muscle_biopsy]`. Why: muscle in ALS shows neurogenic grouped atrophy; the library reported normal muscle.
- `perform_clinical_assessment assessment_type=performance_status` -> `fallback_tool_outputs.clinical_assessment`. Why: the library reported Karnofsky 100 / ECOG 0 with no limitation; the history documents has stopped voice coaching; marked functional decline (Karnofsky 60, ECOG 2).
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[request_gait_and_balance_timed]`. Why: the exam documents a spastic gait with scissoring; the library reported a normal timed gait (moderate slowing stored).
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[request_speech_language_evaluation]`. Why: the exam documents dysarthria; the library reported no motor speech disorder (moderate mixed spastic-flaccid dysarthria stored).
- `order_advanced_imaging modality=DTI_tractography` -> `followup_outputs[request_dti_tractography]`. Why: the stored MRI shows corticospinal tract T2/FLAIR hyperintensity; DTI cannot show normal corticospinal anisotropy.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALS-` pass; every mapped order answered without the library (`verify.py`, map_ALS); no criterion answer changed (snapshot diff).
