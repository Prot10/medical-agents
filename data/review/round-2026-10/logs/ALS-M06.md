# ALS-M06
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 8aa7101a-bc57-4cc9-94ef-a0641d0a81bd | FIXED | `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. Core studies stay in `initial_tool_outputs` (plan C1; display order is CENTRAL 5.1). |
| cc56c62e-8bd2-4f25-ac16-0e43b5e9de83 | FIXED | Riluzole-methotrexate check moved last (`action_criteria[6]`, `followup_outputs[2]`) with a soft constraint after EMG. It stays `required` (plan C3: methotrexate and riluzole both raise transaminases, so monitoring changes). Output rewritten: no AMX0035 "lower hepatotoxicity" alternative, no invented "LFT every 2 weeks" schedule; SmPC schedule plus coordination with rheumatology and methotrexate dose review if ALT rises; alendronate and dysphagia point added. |
| c5bda677-7348-4edf-a4de-681b25afd0f1 | FIXED | Literature follow-up "search_als_ra_comorbidity" and the literature criterion deleted (plan C2); the patient-level diagnostic actions (EMG/NCS, brain and spine MRI, targeted labs) are now criteria 1-4. |
| 1b14a503-d29c-4bb0-a114-f557ba88279b | FIXED | `ground_truth.red_herrings[0]` rewritten with the reviewer's content: raised ESR/CRP and joint deformities reflect RA activity; RA does not explain tongue fasciculations, UMN signs, preserved sensation and multi-region denervation; RA is a confounder. The differential (RA muscle/tendon disease, vasculitic neuropathy) now says the same, both `low`. |
| ba26957f-69df-45b7-a3d0-b7696f11f5c7 | FIXED | Respiratory function recommended, after the core (`action_criteria[4]`, `followup_outputs[0]`), relabelled as staging; reduced values lead to a respiratory/NIV referral must. |
| 7a4732cf-c441-4a48-866c-ac49a58b4d5e | FIXED | Genetic panel optional, after the core with pre-test counselling (`action_criteria[5]`, `followup_outputs[1]`), soft constraint after EMG; panel completed to five genes. |
| 32a75e60-527e-46c1-80c0-8421d70be186 | FIXED | "Husband: alive, type 2 diabetes" removed from `patient.clinical_history.family_history`; `social_history.living_situation` already reads "Lives with husband". |
| b9c53147-2daf-4e26-a7d8-7e5a6f62f17b | FIXED | Same as 8aa7101a and c5bda677: diagnostic core first (EMG/NCS, brain and spine MRI, targeted labs); the "ALS-RA" literature step is gone. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | HPI reported the rheumatologist's EMG ("widespread denervation inconsistent with vasculitic neuropathy pattern") and CK 580 U/L, both scored studies, and carried reasoning ("distinct from her known joint disease", "the atrophy was muscular rather than tenosynovial", "which is not a feature of RA", "combined upper and lower motor neuron signs"). | FIXED: results and reasoning removed; the rheumatologist's concern (vasculitic mononeuritis multiplex, inflammatory myopathy) and referral kept; RF and anti-CCP history kept as "seropositive rheumatoid arthritis". |
| B | minor | `patient.history_present_illness` | "She denies sensory symptoms, noting that her hand numbness from RA is unchanged" contradicted itself. | FIXED: "She denies new sensory symptoms; occasional hand numbness that she has had with RA flares is unchanged." |
| B | major | `initial_tool_outputs.mri.impression` | Brain MRI impression was a spine statement ("No cervical cord compression from RA pannus"), identical to the spine impression. | FIXED: brain report covers brain only (nonspecific corticospinal tract T2 signal; no infarct, hemorrhage, mass or demyelinating lesion; brainstem normal). |
| B | minor | `initial_tool_outputs.body_imaging` | JSON dump in `findings[0].description`; thoracic cord not reported although region is "cervical and thoracic spine"; "No demyelinating disease". | FIXED: plain findings (mild C3-C6 degeneration with mild foraminal narrowing, no cord compression or signal change; no pannus at C1-C2; normal thoracic cord), numbered impression. |
| B | minor | `initial_tool_outputs.specialized_test` | Impression claimed active and chronic change "in all 4 body regions" although the thoracic region showed paraspinal fibrillations only and the bulbar region fibrillations and fasciculations without chronic change; motor NCS without values or lower limb nerves; "Pulmonary function testing recommended."; quantitative field arguing against mononeuritis multiplex. | FIXED: findings kept, impression numbered and region-accurate, motor NCS values added (reduced median and ulnar CMAPs, normal peroneal and tibial, normal velocities, no block), sensory nerves named (normal), recommendation removed, quantitative field reduced to the region count. |
| E | minor | `initial_tool_outputs.labs` | "Exclusion studies" panel with Free T4 as a string and a sentence about the case's diagnosis; "Reviewer baseline rule-out additions"; "RA_Panel"; interpretation naming ALS; no liver tests although methotrexate and riluzole both need them; low hemoglobin row with no significance text. | FIXED: panels per C13, stored values kept (WBC 7.8, Hb 11.8, MCV 84, platelets 320, creatinine 0.8, glucose 90, CK 580, TSH 2.8, ESR 58, CRP 12.4, B12 420, folate 10); added sodium 139, potassium 4.2, calcium 9.3, albumin 3.9, ALT 22, AST 26, ALP 88, bilirubin 0.5, free T4 1.3 (normal); interpretation lists hemoglobin, CK (3.4x ULN), ESR and CRP. |
| B | minor | `followup_outputs[0].output` | Women's SNIP reference given as >70 cmH2O; bare "Abnormal values" impression. | FIXED: SNIP >=60 cmH2O (women), flags, canonical "reduced" impression (FVC 76%, SNIP 55 remain reduced). |
| B | minor | `followup_outputs[1].output` | Only C9orf72 and SOD1; "All values within normal limits". | FIXED: TARDBP, FUS, TBK1 added (negative); canonical negative impression. |
| C | major | `followup_outputs[2].output` | AMX0035 offered as a "lower hepatotoxicity" alternative; an invented "LFT every 2 weeks" schedule; folic acid and losartan not listed; alendronate not reviewed although she has dysphagia. | FIXED: rewritten per plan C3 (methotrexate coordination and dose review, alendronate oesophageal risk, no interaction with hydroxychloroquine, folic acid or losartan; SmPC monitoring). |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions and a lab list including untested HIV, RPR, SPEP, anti-GM1 and "androgen receptor CAG repeat in males" in a woman; no swallowing action despite dysphagia to solids; no respiratory referral despite reduced FVC and SNIP; functional prohibition without any psychiatric element. | FIXED: MUST-DX, MUST-RESP reduced, MUST-BULBAR dysphagia, MUST-RILUZOLE, the plan's methotrexate/alendronate must, MUST-MDT, MUST-GEN; prohibitions PROHIB-IMM, PROHIB-RESP reduced, PROHIB-SWALLOW, PROHIB-SURG cervical (C3-C6). |
| C | major | `ground_truth.differential` | RA muscle/tendon disease left `moderate`; cervical myelopathy "low" citing a "brain/cervical MRI"; hydroxychloroquine, a recognised cause of a neuromyopathy with raised CK, not considered. | FIXED: RA muscle/tendon disease (with myositis) low, vasculitic neuropathy low, IBM low, rheumatoid cervical myelopathy very_low, hydroxychloroquine neuromyopathy very_low (added), methotrexate myopathy very_low; supports/against from case data. |
| E | minor | `ground_truth.key_clinical_evidence` | "July 2026 review" pearl, El Escorial-style EMG pearl, generic 2-5x CK pearl, Kennedy disease named in a woman. | FIXED: rebuilt (K-GC, K-EMG, K-NCS normal sensory with the vasculitic neuropathy point, K-CK 3.4x, K-RESP reduced, K-SPINE with the pannus point, K-BULBAR). |
| A | minor | `ground_truth.action_criteria` | Criteria mechanics and citations as in C16 (brain MRI `contrast/protocol`, spine `contrast:false`, free-text and bare duplicate citations, label = rationale); literature criterion with an exact query. | FIXED: canonical criteria; DI `required`; literature criterion deleted. |
| E | minor | `metadata.notes` | "requires enhanced monitoring" restated the invented schedule. | FIXED: reworded to coordinated liver monitoring and the mimics the work-up excludes. |
| B | minor | `initial_tool_outputs.labs` | Vitamin B12 420 pg/mL and folate 10 ng/mL are the same values as ALS-M05 (template); folate 10 is plausible but low-normal for someone taking folic acid 1 mg daily. | FLAGGED only (plan: keep stored values). |

## Changes, in one paragraph a physician can read before re-reviewing

The required work-up is now EMG/NCS, brain MRI, cervical and thoracic spine MRI and mimic-exclusion bloods, then baseline respiratory function (recommended), the five-gene ALS panel after counselling (optional) and the riluzole interaction check, which stays required because methotrexate and riluzole can both raise transaminases; the "ALS-RA comorbidity" literature step is gone. The HPI no longer reports the rheumatologist's EMG result or the CK, nor the reasoning that separated muscular from articular wasting; it keeps her seropositive RA and the rheumatologist's concern about vasculitis and myopathy. The husband is no longer listed as family history. The EMG keeps its findings (denervation and chronic change with complex fasciculations in the hands, fibrillations in tongue, mentalis and thoracic paraspinals, early tibialis anterior involvement), now with motor conduction values, no block and normal sensory studies; its impression no longer claims chronic change where only fibrillations were recorded. The brain MRI no longer carries the spine statement; the spine MRI reports mild C3-C6 degeneration, no pannus and a normal thoracic cord. Labs are regrouped with liver tests and free T4 added (normal); hemoglobin 11.8, ESR 58 and CRP 12.4 reflect active RA and CK 580 is 3.4x ULN. FVC 76% and SNIP 55 cmH2O are reduced, so the musts refer her to the respiratory/NIV service now; she already has dysphagia to solids, so swallowing assessment and early gastrostomy discussion are musts; riluzole is offered with SmPC monitoring coordinated with rheumatology and a review of oral alendronate. RA is framed as a confounder in the red herring and the differential (all RA-related alternatives low or very low), and hydroxychloroquine neuromyopathy is now considered and excluded.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1 (`[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]`).
- Review UI: initial work-up in criterion order (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- PROHIB-SWALLOW's canonical wording ("already choking or coughing on food or fluids") does not match this patient, who reports mild difficulty swallowing solids without choking; I adapted it to "already has difficulty swallowing solid food". The plan's "Rheumatology" lab panel was not created: the case has no RF or anti-CCP values in its labs, and adding them would invent numbers the case does not need (the HPI keeps the RA as seropositive).
- The riluzole check is required here (plan C3 and Q6). Because it is a post-diagnostic step it is not in `stop_rule.required_before_assessment`, consistent with the plan's unchanged stop rule.

## Verification

Checked: every note id of the case is in the table and each FIXED claim holds in the file (criteria order and tiers per plan 3.1, follow-ups respiratory, genetics, riluzole; literature and initial DI null; both soft constraints; stop rule unchanged); stored lab and respiratory values unchanged against HEAD (only free T4 string made numeric, plan C13); CK multiple recomputed; HPI free of scored results; musts, prohibitions and differential against the plan's per-case decisions; no AMX0035, edaravone, grapefruit, El Escorial, untested anti-GM1/CAG, "July 2026" or new dashes; perfect_agent.py and case_io.py check clean after the changes.

Found and changed:
- `ground_truth.differential` vasculitic neuropathy: "against: painless course without sensory symptoms or signs" contradicted the HPI (occasional hand numbness with RA flares; pain not documented either way): now "against: no new sensory symptoms and no sensory signs, ...".
- `ground_truth.red_herrings[0].field_path` pointed at the whole past-medical-history list: now `patient.clinical_history.past_medical_history[0]` (the RA entry).

Checked and accepted: DI criterion required (plan C3, M06); plan's methotrexate/alendronate must verbatim; adapted PROHIB-SWALLOW wording matches the patient (dysphagia to solids, no choking); no "Rheumatology" lab panel (no RF or anti-CCP values exist; not invented).

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` replaces the `flag` low/normal field, set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but the tongue and mentalis show fibrillations and fasciculations without chronic change, and the tongue is not wasted on examination; thoracic paraspinals show fibrillations only. Regions now: cervical and lumbosacral (tibialis anterior: mildly large MUPs with sparse fibrillations), with active denervation also in bulbar (tongue, mentalis) and thoracic paraspinal muscles. The bulbar symptoms and the dysphagia must are unchanged. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 ALS cases after the change: clean.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
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
