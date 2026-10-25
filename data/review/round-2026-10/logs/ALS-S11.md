# ALS-S11
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b8d3cf2b-8578-4e9d-836f-573a99f3ad13 | FIXED | Action criteria reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. `ground_truth.action_criteria`, `followup_outputs`, `ground_truth.sequence_constraints`, `initial_tool_outputs.literature_search` = null. Core studies stay in `initial_tool_outputs` (plan C1; display is CENTRAL 1). |
| b1d11959-748b-450e-90f6-4b84a6554ca0 | FIXED | The lumbar facet/foraminal observation was removed from `initial_tool_outputs.mri.additional_observations`; the brain report now holds only the corticospinal tract finding and brain pertinent negatives. The L4-L5 disc bulge and L4-L5/L5-S1 facet degeneration now sit only in `initial_tool_outputs.body_imaging` (lumbosacral finding and impression item 2). |
| ad563de2-8dcb-4d59-a6a8-716bde92e819 | FIXED | Chose removal: the spine study stays non-contrast (`contrast: false`) and every "no leptomeningeal enhancement" phrase is gone (findings and impression). There is no leptomeningeal question in this case (low-risk prostate cancer, no metastasis). |
| 3403f58a-341b-41de-8ccb-be549826142e | FIXED | Paraneoplastic motor neuronopathy moved from moderate to low; key_features cite only case data (Gleason 6 on active surveillance, stable PSA 3.2 ng/mL, no metastasis on oncology imaging or spine MRI, classic four-region syndrome). The "paraneoplastic panel negative" claim is removed from the differential and the red herring; no panel was added. |
| 5d1141b1-9051-4d06-bc23-4b494622e2b6 | FIXED | Respiratory impression "Reduced SNIP (68 cmH2O) and NIF (-52 cmH2O), indicating inspiratory muscle weakness; FVC 80% predicted is at the lower limit of normal."; reference ranges harmonised. Must 2: refer to the respiratory/NIV service now and discuss NIV (NIF -52 meets an AAN 2009 marker), overnight oximetry or capnography, repeat FVC and SNIP within 3 months. Prohibition 2: do not wait for FVC below 50% or symptoms. Criterion `action-7` recommended, staging label. |
| 5e8eb882-00ca-4ece-b99e-824074848006 | FIXED | Riluzole-tamsulosin check is now last in `followup_outputs` and in `action_criteria`, with a soft constraint after EMG; its criterion text says "once the diagnosis is established". |
| 9a2859dd-6e23-4489-bb39-3465b5ba6df9 | FIXED | `followup_outputs[1]` now reports C9orf72 plus SOD1, TARDBP, FUS and TBK1 sequencing, with the canonical negative impression replacing "All values within normal limits." |
| 74bcf306-63f8-41c1-be26-4d7ef1cdb561 | FIXED | `followup_outputs[2].output.alternatives` = [] (AMX0035 removed). |
| 30c54a7e-3dc1-47b8-a944-f40bdc8aca65 | FIXED | Case comment (pathway order, reduced respiratory values without action, incoherent imaging, paraneoplastic differential): resolved as under b8d3cf2b, 5d1141b1, b1d11959 and ad563de2, and 3403f58a. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Literature output echoed the criterion's expected_evidence. | FIXED: null; literature criterion deleted (C2). |
| B | major | `initial_tool_outputs.body_imaging` | Region said "cervical and thoracic spine" but the findings described only the thoracic and lumbosacral spine, so the cervical cord (bilateral Hoffman signs, hand wasting) was never reported; findings held a JSON dump, cross-modality conclusions ("metastatic prostate cancer to spine excluded", "prostate metastatic myelopathy excluded") and "Normal lumbar spine" next to a disc bulge; impression numbering started at "2.". | FIXED: region "cervical, thoracic and lumbosacral spine"; plain per-level findings (cervical and thoracic cord normal, conus normal, L4-L5 bulge and L4-L5/L5-S1 facet degeneration without root compression, no vertebral marrow lesion); numbered impression from 1. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were diagnostic actions (EMG, brain MRI "to exclude cervical myelopathy", lab list with HIV, RPR, anti-GM1 and CAG repeat, "Apply Awaji"); no respiratory referral despite an AAN marker. | FIXED: rebuilt per C10: MUST-DX, MUST-RESP reduced with AAN marker (NIF -52), MUST-RILUZOLE, MUST-MDT, MUST-GEN sporadic. No bulbar must (tongue fasciculations and brisk jaw jerk only, no dysarthria or dysphagia). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Cervical-surgery prohibition although the case's degeneration is lumbar; functional-dismissal prohibition with no psychiatric history. | FIXED: PROHIB-IMM, PROHIB-RESP reduced, PROHIB-SURG lumbar (L4-L5 and L5-S1). |
| C, E | minor | `ground_truth.key_clinical_evidence` | El Escorial-style EMG pearl, 2-5x CK pearl, cervical spondylosis pearl where the degeneration is lumbar, "July 2026 review" engineering text. | FIXED: K-GC, K-EMG, K-NCS normal, K-CK 4.3x, K-RESP with AAN marker, K-SPINE lumbar variant merged with the case's paraspinal teaching point (paraspinal denervation localises proximal to the foramina, so it occurs in both L5 radiculopathy and anterior horn cell disease). |
| D | minor | `initial_tool_outputs.specialized_test` | Interpretive tails in findings ("Consistent with early bulbar LMN involvement", "consistent with foot drop", a teaching sentence on paraspinal innervation, "the abnormalities are purely motor"); `quantitative_data` held a classification and a teaching note; impression said "chronic reinnervation in ... four body regions" while chronic change is documented only in the right FDI and TA; motor NCS limited to one peroneal nerve. | FIXED: tails and teaching removed; neutral quantitative fields; numbered impression; added right median (reduced CMAP), right ulnar and right tibial motor studies with no conduction block, without new numeric values. |
| A, D | major | `initial_tool_outputs.labs` | Panels "Exclusion studies" (free T4 as a string with a sentence about the case's diagnosis), "Neuromuscular_Panel" holding TSH, ALP and "LFTs (ALT)", "Reviewer baseline rule-out additions"; interpretation names ALS. | FIXED: C13 panels; every stored value kept; added potassium 4.4, glucose 98, albumin 4.1, AST 31, bilirubin 0.8 and numeric free T4 1.1 ng/dL (all normal); canonical interpretation with CK 740 U/L (4.3x ULN). |
| C | minor | `followup_outputs[2]` | Acetaminophen warning framed as a 3 g/day cap "given concurrent LFT monitoring" (not an interaction); no alcohol entry. | FIXED: tamsulosin no interaction; acetaminophen at his dose no change, consider it when reading a transaminase rise; light alcohol no change; canonical summary and warnings. |
| C | minor | `ground_truth.differential` | "Diabetic amyotrophy" in a man without diabetes; MMN cited an untested "anti-GM1 negative"; no entry for spinal metastasis although the red herring raises it. | FIXED: diabetic amyotrophy deleted; MMN C8 wording; lumbar radiculopathy/cauda equina low with supports/against; spinal metastasis very_low; IBM very_low. |
| C | minor | `ground_truth.red_herrings` | Prostate red herring cited a paraneoplastic panel that was never done; the foot drop with lumbar degeneration (the case's main structural trap) had no red herring. | FIXED: prostate red herring rewritten from case data; added "Right foot drop with mild L4-L5 and L5-S1 degenerative changes" (field_path `initial_tool_outputs.body_imaging`). |
| C | minor | `ground_truth.action_criteria` | Brain MRI required contrast and protocol; spine required `contrast: false`; label = rationale; free-text citations. | FIXED: C16 arguments, canonical texts and citations, case-specific expected_evidence; spine rationale notes why the lumbosacral spine is included. |
| D | minor | `patient.history_present_illness`, `patient.neurological_exam.additional` | "urinary symptoms that would suggest new cord compression" (reasoning); exam `additional` repeated the history and synthesised "combined upper and lower motor neuron signs". | FIXED: sentence trimmed to "He denies any new urinary symptoms."; `additional` set to null. Oncology imaging 8 months ago and PSA kept (prior history, not scored). |
| B | minor | `metadata.notes`, `metadata.difficulty_rationale` | Wording with em dashes; "must exclude spinal metastases" phrased as an instruction. | FIXED: reworded to what the case contains. |
| C | minor | `ground_truth.avoided_actions` | Only five waste items (no amyloid PET, DaTscan or FDG-PET), unlike 28 of 30 ALS cases. | FLAGGED: left unchanged per plan 3.2 (see Open questions). |
| C | minor | labs | Vitamin B12 420, folate 10, ESR 8, CRP 2 are identical to other ALS cases (template values). | FLAGGED: kept (stored values). |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first, then respiratory function, the gene panel and the riluzole check; the literature step is gone. The brain MRI report describes only the brain (corticospinal tract signal, no lesion); the spine MRI covers the cervical, thoracic and lumbosacral spine without contrast and no longer comments on enhancement, with the mild L4-L5 and L5-S1 degenerative changes reported there without root compression. The EMG report lists four-region active denervation, chronic change in the right hand and tibialis anterior, no conduction block in the peroneal, median, ulnar or tibial nerves and normal sensory studies, without teaching text. The labs are standard panels (CK 740 U/L, 4.3x ULN). The reduced SNIP and NIF now lead to a respiratory/NIV referral and an NIV discussion. Paraneoplastic motor neuronopathy is low, supported only by the case's own data (no panel claimed), and lumbar radiculopathy, spinal metastasis and MMN are low or very low. The gene panel reports all five genes; the riluzole check no longer offers AMX0035. Musts are management (diagnosis and disclosure, NIV referral, riluzole with monitoring, MDT, genetic counselling) and the prohibitions include lumbar surgery for the degenerative changes.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Review UI: show the initial work-up and follow-ups in criterion order (plan 5.1).
- New citation keys per plan 1.1 (criteria pack section 8).

## Open questions for Andrea (judgment calls you could not settle)
- `avoided_actions` has five waste items; the other ALS cases also list amyloid PET, DaTscan and FDG-PET as waste. I left them out because the plan says keep the avoided actions unchanged, and a body FDG-PET could be argued in a cancer patient with a paraneoplastic question. Add the three for consistency?
- I added cervical and lumbosacral level findings to the spine MRI (the stored report never described the cervical cord despite its region label), right median, ulnar and tibial motor conduction studies without numbers, a "no calvarial or skull-base marrow lesion" pertinent negative on brain MRI, and a second red herring for the foot drop with lumbar degeneration; none is in the plan's S11 entry.
- MUST-RESP follows the plan's "reduced with AAN marker" category on NIF -52 cmH2O alone; FVC is 80% predicted and there is no orthopnoea in the history (plan Q4 on the MIP/NIF convention applies).

## Verification
Adversarial check, 23 October 2026. Read the log, the full `git diff` against HEAD (old and new case flattened field by field), the whole final case, the plan (sections 1-3 and 4 S11) and the notes file.
- All 9 note ids are in the table and each FIXED claim holds in the file: lumbar findings only in the spine report, brain report brain-only (b1d11959); the non-contrast spine no longer mentions enhancement (ad563de2); paraneoplastic motor neuronopathy low from case data with no panel claimed anywhere (3403f58a); reduced respiratory with an AAN marker (NIF -52, SNIP 68) driving the NIV must and PROHIB-RESP (5d1141b1); riluzole check last (5e8eb882); five-gene panel; AMX0035 gone. No DECLINED or BLOCKED notes.
- Checked: `body_imaging.region` now names the lumbosacral spine the report describes; PROHIB-SURG lumbar names the levels in the spine report; diabetic amyotrophy deleted (no diabetes); CK 740/174 = 4.3x; acetaminophen and alcohol entries agree with the medication list and social history; the prior oncology imaging and PSA stay as history (not scored); no bulbar must; no banned text.
- Found and fixed (B, minor; same class as S01/S02): MUST-DX and K-GC claimed LMN involvement in all four regions, but chronic change is reported only in the right first dorsal interosseous and right tibialis anterior; tongue and thoracic paraspinals show active denervation only. Both now state LMN involvement in the cervical and lumbosacral regions with active denervation also in bulbar and thoracic muscles.
- Found and fixed (B, minor): the EMG impression attributed "large motor unit potentials, markedly reduced recruitment" to both the first dorsal interosseous and tibialis anterior, but the tibialis anterior finding reports reduced recruitment without large MUPs. The impression now says large MUPs in the first dorsal interosseous and markedly reduced recruitment in the tibialis anterior.
- Noted, not changed: the worker's open question on the five avoided actions stands.
- `perfect_agent.py` -v ok after the change (brain MRI, spine MRI and labs are served from the initial work-up); `case_io.py check` clean for the case (schema, synonym guard; the one failing test in the suite does not name it).

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` added (rows carried no abnormality marker), set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 5 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- avoided_actions: amyloid PET and DaTscan waste items added (avoid-waste-6/7); FDG-PET left out (cancer history).
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
