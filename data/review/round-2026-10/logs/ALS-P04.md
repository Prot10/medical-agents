# ALS-P04
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 959fb8c4-81e1-4e44-9344-a79599881d67 | FIXED | Plan C1/C2: `ground_truth.action_criteria` reordered (EMG/NCS, brain MRI, spine MRI, labs first); `followup_outputs` now respiratory, genetics, riluzole; literature follow-up `search_flail_arm_als` and criterion `action-1-search-medical-literature` deleted; `sequence_constraints` EMG before genetics and riluzole |
| 039f6452-f616-4742-a272-0a5128b5d6bd | FIXED | Flail-arm literature output deleted (it also cited El Escorial); the phenotype is now named in `key_clinical_evidence[3]` (brachial amyotrophic diplegia, slower course, leg UMN signs do not exclude it) and in MUST-DX; EMG/NCS is criterion 1 and states no conduction block including the proximal arm segments |
| a04ceac5-9896-4629-adf7-746ba554eafb | FIXED | `ground_truth.differential`: MMN high -> low with "supports/against" key_features (UMN signs, normal conduction without block, symmetric involvement, thoracic and lumbosacral denervation); brachial amyotrophy / Hirayama moderate -> very_low |
| 3b7649bf-37e6-4f4d-8428-6c4833a9bbd0 | FIXED | Generic "2-5x ULN" pearl replaced by the >5x pearl (CK 1120 U/L is 6.4x ULN, consider a myopathic contributor clinically, the neurogenic EMG argues against a primary myopathy); lab interpretation and summary state "CK 1120 U/L (6.4x ULN)"; IBM key_features cite the CK as the supporting point (C9) |
| eac9df83-0f72-4205-a644-e0312d1ef61a | FIXED | Riluzole check last in criteria and follow-ups, soft constraint `action-6` before `action-2`; criterion text per C3 |
| bc7959ee-02bf-49de-b4ff-ec615f25f5c7 | FIXED | Respiratory follow-up first among the follow-ups, after the diagnostic core; criterion relabelled as staging (`recommended`); output ranges per C4 and impression "Reduced FVC (78% predicted) and SNIP (68 cmH2O), indicating inspiratory muscle weakness."; MUST-RESP reduced (NIV referral now), PROHIB-RESP reduced |
| c1e85ca9-5d63-450d-ab12-85b0d936e3a2 | FIXED | Riluzole output: `alternatives` = [] (AMX0035 granules removed); the formulation-convenience warning (liquid riluzole for hand weakness) removed as the note asks; interactions lisinopril (none) and moderate alcohol (avoid heavy drinking, transaminases); canonical monitoring `summary` |
| b65f7002-dcc1-411e-887b-9ff8cefaeb7c | FIXED | Genetic panel `optional`, after the core work-up with soft constraint EMG before genetics; output reports C9orf72, SOD1, TARDBP, FUS and TBK1 with the canonical negative impression (C5) |
| b67bcf6e-7587-421b-8df5-9cf8163a7c2f | FIXED | Same as 959fb8c4 (pathway), a04ceac5 (MMN low) and 3b7649bf (CK 6.4x) |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Synthesis sentences "the finding of bilateral Babinski responses with areflexic arms is a paradoxical combination of upper and lower motor neuron signs" and "The clinical picture is one of predominant bilateral arm involvement..." do the agent's reasoning | FIXED: deleted; neutral referral sentence added (C11) |
| D | major | `patient.neurological_exam.additional` | Same "paradoxical combination of upper and lower motor neuron signs" synthesis | FIXED: "Profound bilateral arm weakness and atrophy with preserved leg strength." |
| D | major | `patient.clinical_history.past_medical_history[0]` | Names the phenotype ("Flail arm syndrome") in the patient block | FIXED: plan wording "Bilateral arm weakness and wasting noted 12 months ago, initially attributed to bilateral rotator cuff pathology" |
| B | major | `initial_tool_outputs.mri` | Brain report impression identical to the spine report and containing a spine statement ("No cervical cord compression"); finding location mixed "corticospinal tracts, motor cortex arm area" | FIXED: brain-only report (subtle precentral low T2 signal in the arm region, supportive; no mass, brainstem, demyelinating lesion or infarct), numbered impression |
| B | major | `initial_tool_outputs.body_imaging` | Impression described the brain ("corticospinal tract changes in motor cortex arm representation"); JSON dump in `findings[0].description`; thoracic cord not described | FIXED: plain findings for C3-C7 (mild spondylosis, no canal or significant foraminal stenosis, no compression) and the thoracic cord; numbered impression |
| B | minor | `initial_tool_outputs.specialized_test` | Impression "chronic reinnervation (polyphasic MUPs)" and "3 body regions" beyond the findings for thoracic; motor NCS limited to median/ulnar with no distal latencies; "Pulmonary function testing recommended." | FIXED: impression matches findings; Motor NCS adds normal distal latencies, normal peroneal and tibial studies, no block across proximal arm segments, no temporal dispersion (C6); `recommended_actions` emptied |
| A/B | major | `initial_tool_outputs.labs` | TSH and free T4 as strings "Within reference range" in "Mimic exclusion" and "Exclusion studies" with case-level sentences; "Reviewer baseline rule-out additions"; no CBC, renal or liver values although required; CAG repeat as a string; interpretation names ALS | FIXED: panels per C13 (stored CK 1120, ESR, CRP, B12, folate, CAG 21 kept, CAG numeric; added normal CBC, CMP, TSH 2.4 mIU/L, free T4 1.2 ng/dL); canonical interpretation |
| C | major | `ground_truth.action_criteria` | Lab criterion asked `androgen_receptor_CAG_repeat` (not the advertised vocabulary spelling) and 9 other panels by exact name; brain MRI `contrast: true, protocol: standard`; spine `contrast: false`; label = rationale; mixed citations | FIXED: C13/C16 arguments (`["CBC","CK","TSH","vitamin_B12","androgen receptor CAG repeat"]`, `{}`, `{"study":"spine_MRI"}`), canonical label/rationale/citations with case expected_evidence; verified each call receives its report |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions plus a generic lab must; generic functional-dismissal prohibition (no psychiatric history) | FIXED: rebuilt per C10 (DX with flail-arm phenotype, RESP reduced, RILUZOLE, MDT, GEN; no bulbar must: no bulbar symptoms or signs); prohibitions IMM, RESP reduced, SURG cervical (C3-C7, no compression) |
| C | major | `ground_truth.differential` | Cervical spondylotic myelopathy with radiculopathy (the main structural mimic of wasted areflexic arms with UMN signs in the legs, and the case shows C3-C7 spondylosis) was only partly covered by "cervical radiculopathy"; Kennedy disease (tested by the CAG repeat) absent | FIXED: radiculopathy entry broadened to "Cervical spondylotic myelopathy with multilevel radiculopathy" (low, supports/against from the case); Kennedy disease very_low with C8 wording and the normal CAG result; IBM and CIDP key_features rewritten |
| C | minor | `ground_truth.red_herrings` | Empty although the case carries two confounders (shoulder MRI tendinopathy, cervical spondylosis) | FIXED: two red herrings added with case-only reasoning |
| C | minor | `ground_truth.key_clinical_evidence` | "July 2026 review" engineering pearl; El Escorial-style EMG pearl; generic CK pearl | FIXED: rebuilt per C14 (K-GC, K-EMG, K-NCS normal, flail-arm phenotype, K-CK above 5x, K-RESP, K-SPINE) |
| C | minor | `metadata.notes` | "areflexic arms with bilateral Babinski signs is pathognomonic for ALS" is wrong (cervical spondylotic myelopathy with radiculopathy produces the same combination) | FIXED: reworded to what the case contains (C17) |
| E | minor | `metadata.difficulty_rationale` | "5 required tools with literature support" no longer true | FIXED: "4 required tools" |
| B | minor | `initial_tool_outputs.labs` | Vitamin B12 420, folate 10, ESR 8, CRP 2 identical to other ALS cases (template values) | FLAGGED only; stored values kept per plan |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads as a diagnostic pathway: EMG/NCS, brain MRI, spine MRI and blood tests (with the androgen receptor CAG repeat for Kennedy disease) are required actions 1-4, followed by baseline respiratory function (recommended staging), an optional ALS gene panel and the riluzole check (recommended, last); the flail-arm literature step is gone and the phenotype is explained in the key evidence instead. The patient block no longer names the phenotype or explains the "paradoxical" combination of signs; the shoulder MRI history stays. The EMG keeps its findings (severe cervical active and chronic denervation, thoracic paraspinal and lumbosacral involvement, tongue fasciculations only, normal sensory studies) and now states normal distal latencies and no conduction block across the proximal arm segments; it no longer recommends pulmonary tests. The brain MRI describes only a subtle precentral low T2 signal in the arm region; the spine MRI reports mild C3-C7 spondylosis without cord compression. Labs are reorganised into standard panels; CK 1120 U/L is stated as 6.4x ULN and a key-evidence pearl says this is higher than usual in ALS and warrants clinical consideration of a myopathic contributor, while the neurogenic EMG argues against a primary myopathy. MMN is now low and Hirayama very low; cervical spondylotic myelopathy with radiculopathy and Kennedy disease are in the differential as low and very low. FVC 78% and SNIP 68 cmH2O are reduced, so the musts refer him to the respiratory/NIV service; the other musts follow the condition plan (disclosure, riluzole with its LFT schedule, MDT, genetic counselling), and a prohibition rules out cervical surgery for the spondylosis.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used and not yet in criteria pack section 8: `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` (plan section 5 item 2).
- UI: show `initial_tool_outputs` in criterion order (plan section 5 item 1).

## Open questions for Andrea (judgment calls you could not settle)
- The plan's "cervical radiculopathy low" entry was broadened to "Cervical spondylotic myelopathy with multilevel radiculopathy" because that is the structural mimic of wasted areflexic arms with leg UMN signs that a neurologist would name here; the plan's other differential decisions are applied as written.
- The riluzole output previously warned that tablets may be hard to handle with bilateral hand weakness (liquid formulation available). The reviewer asked to keep formulation questions out of the interaction step, so it was removed; it is not added as a must (the occupational therapist in the MDT covers handling). Say if you want it as a must.

## Verification
Adversarial verifier, 23 October 2026. Checked: all 9 note ids present; criteria order and tiers; lab criterion uses the vocabulary term "androgen receptor CAG repeat" and the labs report 21 repeats (normal, numeric); CK 1120/174 = 6.4x ULN with the above-5x pearl and IBM low; MMN low and Hirayama very_low per the notes; patient block no longer names the phenotype or reasons about the paradoxical signs (shoulder MRI kept as pre-encounter history); EMG impression vs findings (severe cervical active and chronic change, thoracic fibrillations, lumbosacral sparse fibrillations with mildly large MUPs, tongue fasciculations only, no block); Gold Coast met in the lumbosacral region (extensor plantars, brisk knees, EMG LMN); flail-arm pearl compatible with leg UMN signs; no bulbar must (no bulbar symptoms or signs); spine and brain reports region-pure and numbered; cervical surgery prohibition and K-SPINE match the C3-C7 spondylosis; riluzole output without AMX0035 or the formulation item; forbidden strings: none. Perfect-agent and case_io check clean. Found nothing that needed a change.

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` added (rows carried no abnormality marker), set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but thoracic paraspinals (T4-T8) show fibrillations only. Regions now: cervical and lumbosacral (mildly large MUPs with sparse fibrillations), with active denervation also in thoracic paraspinal muscles. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 ALS cases after the change: clean.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- em dashes in the stored EMG report replaced (auditor flag).
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
