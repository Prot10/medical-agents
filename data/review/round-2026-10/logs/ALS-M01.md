# ALS-M01
Reviewer status: R1 needs_changes, R2 pending | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| a4f2f7d7-3db5-4e46-a063-f6b850457c5b | FIXED | `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. The EMG stays in `initial_tool_outputs.specialized_test` (plan C1; display of the initial work-up in criterion order is a CENTRAL UI request). |
| 44072246-f418-4f13-8e78-702080e6b3d3 | FIXED | Riluzole check moved last (`followup_outputs[2]`, `action_criteria[6]`), soft constraint `action-6` before `action-2`; output rewritten (`followup_outputs[2].output`): wrong CYP1A2/grapefruit and levothyroxine claims, edaravone and AMX0035 removed. |
| 7f4e889f-784b-45e2-a28c-12441a846039 | FIXED | Respiratory function kept recommended, placed after the diagnostic core (`action_criteria[4]`, `followup_outputs[0]`); label and rationale say it stages, not diagnoses; abnormal values now drive MUST-RESP (NIV referral). |
| 6a8c17dc-1b00-4571-97a2-b9cdd3293dfc | FIXED | Genetic panel optional, after the core (`action_criteria[5]`, `followup_outputs[1]`), soft constraint EMG before genetics; label states pre-test counselling and post-diagnostic timing. |
| 78281d7e-581b-464f-810d-cdfb684881fd | FIXED | Spine MRI criterion relabelled as mimic exclusion with the canonical rationale (spondylosis does not explain bulbar signs and must not delay the work-up); K-SPINE pearl, cervical-surgery prohibition and red herring 0 reworded to the same effect. |
| e39e5677-3386-4fa6-adab-01540f6118d8 | FIXED | Same as a4f2f7d7: diagnosis first (EMG, MRI, spine MRI, labs), then staging and treatment steps. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | HPI gave the result of the spine MRI the case scores ("cervical spine MRI which showed moderate spondylosis") plus a reasoning sentence about bulbar signs. | FIXED: replaced by "Her primary care physician referred her for neurological evaluation." |
| B | minor | `patient.history_present_illness` | "fatigue after a long day teaching" while she is a retired teacher. | FIXED: "attributed to fatigue." |
| B | minor | `patient.neurological_exam.additional` | "no gynecomastia" in a woman (template carry-over, C17). | FIXED: deleted. |
| D | major | `initial_tool_outputs.literature_search`, criterion `action-1-search-medical-literature` | Literature output echoed the criterion's expected evidence; literature used as a clinical step. | FIXED: both deleted (C2). Fallback "general" literature output kept. |
| C | major | `followup_outputs[2].output` (DI) | Grapefruit and alcohol "via CYP1A2 inhibition", levothyroxine "CYP1A2" claim, edaravone and AMX0035 as alternatives, cross-reference to the patient's LFTs. | FIXED: canonical riluzole output (each medicine: no interaction; LFT schedule with ALT > 5x ULN stop rule; neutropenia warning; no alternatives). |
| D | minor | `initial_tool_outputs.specialized_test.recommended_actions` | "Pulmonary function testing recommended." (cross-step hint). | FIXED: emptied. |
| C | minor | `initial_tool_outputs.specialized_test.findings[0]` | Tongue MUP amplitude "6-8 mV" is implausible for genioglossus. | FIXED: "up to 2.5 mV". |
| B | minor | `initial_tool_outputs.specialized_test.quantitative_data.dominant_emg_pattern`, `.impression` | Pattern read "chronic denervation with active reinnervation" (inverted); impression a prose paragraph with motor NCS findings missing. | FIXED: "Active denervation with chronic reinnervation"; impression rewritten as a numbered list including reduced CMAPs, no conduction block, normal sensory studies. Em dashes removed from the sensory NCS line. |
| B | minor | `initial_tool_outputs.mri.impression` | Numbering "1 ... 3."; imaging differential listed demyelination although the report finds no white matter lesions. | FIXED: numbered 1-2, corticospinal signal called nonspecific, pertinent negatives stated. |
| B | minor | `initial_tool_outputs.body_imaging.findings`, `.impression` | JSON dump in `findings[0].description`; redundant second finding; impression starting at "2."; thoracic cord not reported although the region is cervical and thoracic; "moderate" vs "mild-moderate" stenosis. | FIXED: plain-sentence findings, normal thoracic cord finding added, numbered impression, stenosis graded "mild to moderate" throughout. |
| E | minor | `initial_tool_outputs.labs` | Panel names "BMP", "LFTs", "Neuromuscular_Panel"; interpretation "Rule-out studies do not confirm ALS" names the diagnosis; albumin missing from the metabolic panel. | FIXED: panels per C13 (CBC, CMP with albumin 4.2 g/dL added, Creatine kinase, Thyroid function, Vitamins, Inflammatory markers); all stored values kept; interpretation "Abnormal: CK 748 U/L (4.4x ULN). All other results are within reference ranges." |
| B | minor | `followup_outputs[0].output` (respiratory) | SNIP limit ">70 cmH2O women", MIP/NIF limits "> -70"; impression a bare "Abnormal values:" list. | FIXED: FVC >=80%, SNIP >=60 cmH2O (women), MIP/NIF -60 cmH2O or more negative, absolute FVC/FEV1 ranges as % predicted; `flag` per finding; impression per C4 (reduced, with MEP and ratio). |
| B | minor | `followup_outputs[1].output` (genetics) | TBK1 missing; impression "All values within normal limits". | FIXED: TBK1 added as negative; canonical negative impression, which also names the extra UBQLN2 and VCP results already stored. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were diagnostic actions (EMG, MRI "to exclude cervical myelopathy", labs with "androgen receptor CAG repeat in males" in a woman, Awaji criteria); no NIV referral despite MIP/NIF markers; swallowing must generic. | FIXED: rebuilt per C10: MUST-DX, MUST-RESP (AAN marker: MIP -48, NIF -52), MUST-BULBAR dysphagia, MUST-RILUZOLE, MUST-MDT, MUST-GEN. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Functional-dismissal prohibition without any psychiatric element; generic wording; oral-feeding prohibition. | FIXED: PROHIB-IMM, PROHIB-RESP reduced, PROHIB-SWALLOW, PROHIB-SURG cervical (C5-C6). |
| C | major | `ground_truth.differential` | Cervical myelopathy left moderate after the MRI excluded compression; "progressive bulbar palsy" (an ALS phenotype) listed as competitor; Kennedy disease in a woman citing an untested CAG repeat; MMN citing an untested anti-GM1; MG citing an untested decrement. | FIXED: CSM low, MMN low, MG low with supports/against from case data; PBP and Kennedy deleted. |
| E | minor | `ground_truth.key_clinical_evidence` | "July 2026 review" engineering pearl; generic 2-5x CK pearl; El Escorial EMG pearl. | FIXED: rebuilt per C14 (K-GC, K-EMG, K-NCS normal, K-CK 4.4x, K-RESP, K-SPINE, K-BULBAR). |
| A | minor | `ground_truth.action_criteria[*].citations`, `label`/`rationale` | Duplicate bare keys ("AAN_2009" next to "[AAN_2009]"), free-text citation "Gold Coast; EAN 2024; NICE NG42"; label identical to rationale; brain MRI required `contrast: true, protocol: standard` and spine `contrast: false`, which fail a correct order. | FIXED: canonical criteria per C3-C6, C12, C13, C16; brain MRI `{}`, spine `{"study": "spine_MRI"}`, labs core panels. |
| B | minor | `ground_truth.red_herrings[0]` | "on brain/cervical MRI" (the finding is on the spine MRI). | FIXED: data_point, location and correct_interpretation reworded; field_path kept. |
| B | minor | `ground_truth.red_herrings[1].correct_interpretation` | "confirming motor neuron disease" overstated. | FIXED: states what the EMG shows that entrapment does not produce. |
| B | minor | `metadata.difficulty_rationale` | Listed respiratory function as required. | FIXED: required tools are EMG/NCS, brain MRI, spine MRI, labs. |

## Changes, in one paragraph a physician can read before re-reviewing

The work-up now reads as diagnosis first: EMG/NCS, brain MRI, spine MRI and mimic-exclusion blood tests are the four required actions (criteria 1-4), followed by baseline respiratory function (recommended), the ALS gene panel after counselling (optional) and the riluzole interaction check (recommended), with soft constraints that genetics and riluzole follow the EMG. The literature step is gone. The HPI no longer reports the spine MRI result. Reports were made modality-pure: the EMG impression lists denervation by region, reduced CMAPs, no conduction block and normal sensory studies; the brain MRI calls the corticospinal signal nonspecific; the spine MRI describes the C5-C6 stenosis without cord compression and a normal thoracic cord; the labs are regrouped with all values kept (CK 748 U/L, 4.4x ULN); the respiratory report uses women's limits (SNIP 60) and states reduced FVC 72%, SNIP 48, MIP -48, NIF -52 and MEP 62; the gene panel adds TBK1. The riluzole check no longer contains grapefruit, CYP1A2 levothyroxine claims, edaravone or AMX0035. Musts now are: diagnosis and disclosure by Gold Coast, referral for NIV now (MIP and NIF meet an AAN 2009 marker), urgent swallowing assessment with early gastrostomy discussion, riluzole with the SmPC monitoring schedule, specialist MDT with advance care planning, and genetic counselling; prohibitions cover immunotherapy, waiting for FVC < 50%, delaying swallowing assessment and cervical surgery for C5-C6 spondylosis. The differential keeps cervical myelopathy, MMN and myasthenia gravis, all low; progressive bulbar palsy (a phenotype) and Kennedy disease (she is a woman) were removed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used per plan section 1.1: `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` (plan section 5.2, criteria pack section 8).
- Review UI: show `initial_tool_outputs` in criterion order so EMG, brain MRI, spine MRI and labs read as Steps 1-4 (plan section 5.1; all four R1 pathway notes depend on it for the display).

## Open questions for Andrea (judgment calls you could not settle)

- The genetic output also reports UBQLN2 and VCP (beyond the dataset's five-gene panel). I kept them as stored data and named them in the impression rather than deleting results.
- `flag` keys ("low"/"normal") were added to the respiratory findings to carry the plan's "is_abnormal per these ranges" in a schema that has no such field for specialized tests.

## Verification

Checked: every note id of the case is in the table and each FIXED claim holds in the file (criteria order and tiers per plan 3.1, follow-ups respiratory, genetics, riluzole; literature and initial DI null; both soft constraints; stop rule unchanged); stored lab and respiratory values unchanged against HEAD (only free T4 string made numeric, plan C13); CK multiple recomputed; HPI free of scored results; musts, prohibitions and differential against the plan's per-case decisions; no AMX0035, edaravone, grapefruit, El Escorial, untested anti-GM1/CAG, "July 2026" or new dashes; perfect_agent.py and case_io.py check clean after the changes.

Found and changed:
- `initial_tool_outputs.specialized_test.impression` item 2 said "reduced CMAP amplitudes in the wasted hand and leg muscles", while the exam records no lower limb atrophy and the report itself measured median, ulnar and peroneal CMAPs: now "Reduced median, ulnar and peroneal CMAP amplitudes ...".
- `ground_truth.red_herrings[1].correct_interpretation` placed extensor digitorum among "muscles of both hands": now "median-innervated (abductor pollicis brevis) and non-median muscles (first dorsal interosseous, extensor digitorum communis) of both arms".

No other error found. Brain MRI rationale keeps the plan's "; such as" case clause (grammar only, not changed).

## Condition audit (ALS lead, 23 Oct 2026)
- `ground_truth.key_clinical_evidence[2]` (K-NCS): "or SBMA" removed. SBMA is X-linked and affects men; the plan's C8 already drops the Kennedy entry in women, so the pearl named a mimic that cannot apply (flagged by the S02, S04, S07 and S09 verifiers as a class).
- `followup_outputs[0].output.findings[*].is_abnormal` replaces the `flag` low/normal field, set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).
- `ground_truth.action_criteria[action-3].rationale`: punctuation slip "signs; such as" corrected to "signs, such as".

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- required_recommendations: must added (cognitive/behavioural screen and pseudobulbar affect).
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

- `ground_truth.action_criteria[action-5-interpret-labs]`.alternatives: was [CBC, CK, TSH, vitamin_B12]; now [CBC, CK, TSH, vitamin_B12, CMP, folate, inflammatory_markers] | [CBC, CK, TSH, vitamin_B12].
- Decision: serve: new first alternative (old order kept as an alternative). The label and rationale name renal and liver function, calcium, folate, ESR and CRP (liver baseline before riluzole, inflammatory mimics); the order named only CBC, CK, TSH and B12, so the CMP and inflammatory results the evidence cites were not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
