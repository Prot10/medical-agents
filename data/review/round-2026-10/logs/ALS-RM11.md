# ALS-RM11
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0e1a7582-3e73-49c7-8eda-ec7d5d37cfd7 | FIXED | `patient.history_present_illness`: "EMG is scheduled.", the CK result (860 U/L), the cervical MRI result and the reasoning sentence about spondylotic myelopathy are deleted (EMG, labs and spine MRI are scored criteria); the HPI now ends "His primary care physician found brisk reflexes and referred him for neurological evaluation." The EMG result stays in the work-up. |
| 05603637-ba9e-428a-a591-ab61b2526ecc | FIXED | Action criteria reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed (criterion `action-1-search-medical-literature` and `initial_tool_outputs.literature_search` deleted); sequence constraints EMG before genetics and riluzole. |
| c2bde008-f975-448f-a471-5c4ba546632e | FIXED | `ground_truth.differential[0]` "Cervical spondylotic myelopathy" moderate -> low, key_features with the note's reasoning (tongue fasciculations, bulbar, thoracic and lumbosacral denervation, normal sensory studies, no block, no cord signal change); red herring and pearl 6 say the same; PROHIB-SURG cervical (C4-C6) added. |
| 67ade2c9-94fd-47c0-b9bf-323117e7e88a | FIXED | Riluzole check is the last follow-up and the last criterion (recommended), with a soft constraint EMG before it. |
| d979b5dc-a8b9-4e96-963a-eefb72e2ebdd | FIXED | Respiratory criterion recommended, staging text, after the diagnostic core; impression "Reduced FVC (76% predicted) and SNIP (60 cmH2O), indicating inspiratory muscle weakness."; MUST-RESP reduced (respiratory/NIV referral now) and PROHIB-RESP reduced. |
| 9b390d90-e4e5-43ff-a511-4da5fc8b0dc4 | FIXED | AMX0035 removed (`followup_outputs[2].output.alternatives` = []); output rewritten per C3 (metformin, losartan, moderate alcohol; LFT schedule with stop threshold; neutropenia). |
| de4d37e7-f08e-41ce-8b81-d78b878da744 | FIXED | Genetic panel criterion stays optional, after counselling, with a soft constraint EMG before genetics; follow-up second in the post-diagnostic list; output reports all five genes with the canonical negative impression (was C9orf72 and SOD1 only, "All values within normal limits"). |
| f71232f0-869a-4af9-ba55-952a5199d88d | FIXED | Same as 05603637 (pathway) and 0e1a7582 (EMG "scheduled" contradiction). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.history_present_illness` | PCP "noted ... bilateral Babinski signs" while the exam records a right Babinski only | FIXED: sentence replaced by the neutral referral ("found brisk reflexes") |
| D | minor | `patient.neurological_exam.additional` | Synthesis ("Progressive bilateral weakness with UMN and LMN signs") | FIXED: "No gynecomastia." (a plain finding that the Kennedy entry already relied on but the exam did not document) |
| B/A | major | `initial_tool_outputs.specialized_test` | Impression claimed chronic reinnervation in all four regions while the findings showed it only in the first dorsal interosseous; motor NCS without nerves or values; sensory NCS "Normal."; `quantitative_data` "4 regions" | FIXED: impression restated from the findings and numbered; motor NCS names the nerves with reduced median and ulnar CMAPs (values given), normal latencies and velocities, no block or dispersion; sensory nerves named; factual quantitative_data |
| B/D | major | `initial_tool_outputs.body_imaging` | Finding description was a JSON dump; impression numbered from "2."; "No demyelinating lesions" in a spine report | FIXED: plain sentences (C4-C6 disc-osteophyte complexes, foraminal narrowing, moderate canal narrowing at C4-C5; normal cord signal); impression numbered 1-2 |
| D | minor | `initial_tool_outputs.mri` | Impression numbered "1." with a single item; pertinent negatives limited to "No demyelinating disease" | FIXED: CST signal called non-specific; "No demyelinating, vascular or mass lesion"; brainstem and cerebellum normal |
| A/B | major | `initial_tool_outputs.labs` | "Exclusion studies" with free T4 as a string and engineering text; "Reviewer baseline rule-out additions"; no blood count, renal or liver values although CBC and CMP were required; interpretation names ALS | FIXED: canonical panels, stored values kept (CK 860, TSH 2.1, ESR, CRP, B12, folate); normal CBC, CMP and free T4 1.3 ng/dL added (glucose 128 random in treated diabetes, potassium 4.6 on losartan); interpretation "Abnormal: CK 860 U/L (4.9x ULN)." |
| D | major | `initial_tool_outputs.literature_search` | Stored literature output echoed the criterion's expected evidence verbatim | FIXED: set to null with the criterion (C2) |
| A | minor | `followup_outputs[0].output` | Respiratory reference ">70 cmH2O men", bare "Abnormal values" impression | FIXED: canonical references and impression |
| C | major | `ground_truth.assessment` | Diagnostic musts and a generic lab must (HIV, RPR, SPEP, anti-GM1, CAG repeat); functional-dismissal prohibition without any psychiatric element; no speech/swallowing must despite palatal weakness and tongue fasciculations | FIXED: rebuilt per C10 (MUST-DX, MUST-RESP reduced, MUST-BULBAR signs, MUST-RILUZOLE, MUST-MDT, MUST-GEN; PROHIB-IMM, PROHIB-RESP reduced, PROHIB-SURG cervical) |
| C | minor | `ground_truth.differential` | MMN cited "anti-GM1 negative" and Kennedy cited "androgen receptor CAG repeat normal", neither tested; myasthenia cited "denervation rather than decrement" (no repetitive stimulation done) | FIXED: key_features cite only case data (C8 wording); myasthenia very_low |
| E/C | major | `ground_truth.key_clinical_evidence` | Engineering pearl ("July 2026 review ..."), El Escorial EMG pearl, generic CK 2-5x pearl | FIXED: rebuilt per C14 (K-GC, K-EMG, K-NCS, K-CK 4.9x, K-RESP, K-SPINE) |
| A/B | minor | `ground_truth.red_herrings[0]` | field_path pointed to the brain MRI (`initial_tool_outputs.mri.findings`) for a spine finding, and called "moderate" spondylosis "mild" | FIXED: `initial_tool_outputs.body_imaging`, location "Spine MRI report", data point and interpretation from the report |
| A | minor | `ground_truth.action_criteria` | Brain MRI required `contrast: true`; spine `contrast: false`; nine-item lab list; free-text and duplicated citations; label = rationale | FIXED per C16 and C13 |
| E | minor | `metadata.notes`, `metadata.difficulty_rationale` | "real-seeded v2 dataset pattern", "4 required tools, mild cervical degenerative changes" | FIXED: reworded clinically |
| B | minor | `initial_tool_outputs.labs` | ESR 8, CRP 2, B12 420, folate 10 identical to many ALS cases | FLAGGED: stored values kept per plan |

## Changes, in one paragraph a physician can read before re-reviewing
The HPI no longer says that the EMG is scheduled or gives the CK and cervical MRI results; it ends with the referral for brisk reflexes. The work-up reads EMG/NCS, brain MRI, spine MRI and blood tests first, then respiratory function (recommended), the genetic panel (optional, all five genes negative) and the riluzole check (recommended); the literature search is gone. The EMG impression now follows its findings (fibrillation potentials in tongue, cervical, thoracic and right tibialis anterior muscles; chronic neurogenic change in the hand muscles; reduced median and ulnar CMAPs with normal velocities and no block; normal sensory studies). The spine MRI reads as a plain report of moderate C4-C6 spondylosis with canal narrowing at C4-C5 and normal cord signal; the brain MRI shows only non-specific corticospinal tract signal. Labs show CK 860 U/L (4.9x ULN) with a complete normal baseline. Musts: diagnosis by Gold Coast 2020 with disclosure; respiratory/NIV referral now (FVC 76%, SNIP 60 cmH2O); speech and swallowing assessment for the palatal weakness and tongue fasciculations; riluzole with LFT monitoring; MDT; genetic counselling. Prohibitions: no immunotherapy, no waiting for FVC below 50% before NIV referral, no cervical surgery for the spondylosis. Cervical spondylotic myelopathy is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- New citation keys used: `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]`.
- Review UI: show the initial work-up and follow-ups in criterion order.

## Open questions for Andrea (judgment calls you could not settle)
- The EMG impression now claims chronic neurogenic change only where the findings show it (hand muscles). Gold Coast is met regardless (UMN and LMN signs in the cervical region; clinical LMN signs in bulbar and cervical regions). If you want the original "four-region active and chronic" picture, motor unit data would need to be added to the bulbar, thoracic and lumbosacral findings.
- The case's moderate alcohol use appears in the riluzole check (keep intake low) but not as a separate must (the plan lists alcohol musts only for M03). Add one if wanted.

## Verification
Adversarial re-read of the whole final case against `git show HEAD`, the plan (section 4 RM11) and the eight R1 notes (all ids present).
- Notes: 0e1a7582 and f71232f0: "EMG is scheduled.", the CK value, the cervical MRI result and the reasoning sentence are gone from the HPI; the earlier "bilateral Babinski" (exam: right only) is gone too. Pathway notes (05603637, 67ade2c9, d979b5dc, de4d37e7, 9b390d90): confirmed in criteria and follow-ups; `initial_tool_outputs.literature_search` is null (the remaining `fallback_tool_outputs.literature_search` "general" entry is a neutral no-evidence answer present at HEAD, not a scoring echo). c2bde008: CSM low with the note's reasoning; PROHIB-SURG cervical names C4-C6 from the spine report; red herring `field_path` now `initial_tool_outputs.body_imaging`.
- Cross-field: right Babinski in exam and MUST-DX; mild palatal weakness without dysphagia gives the speech and swallowing must; CK 860/174 = 4.9x (at or below 5x, so the C14 low-ratio pearl is correct); respiratory reduced (FVC 76, SNIP 60 in a man) with MUST-RESP and PROHIB-RESP reduced; random glucose 128 in treated diabetes and potassium 4.6 on losartan inside range; interaction output covers metformin, losartan and moderate alcohol. The exam `additional` now reads "No gynecomastia.", a pertinent negative the Kennedy entry uses; acceptable.
- Found: nothing to change.
- Checks run after verification: `perfect_agent.py -v` ok (every required and recommended criterion answered by the case's own data; the "<- ?" source marker for brain MRI, spine MRI and labs is the same in every ALS case and is not a fallback), `case_io.py check` schema OK, synonym guard OK, no test failure names the case. Grep for AMX0035, Relyvrio, edaravone, grapefruit, serotonergic, "July 2026", El Escorial, "Exclusion studies", "Reviewer baseline" and JSON dumps: none in the case (QTc appears only in the fallback ECG). No new em or en dash in the diff. Citations are bracketed allow-list keys only. Lab `is_abnormal` flags agree with every numeric reference range; ESR 8, CRP 2, B12 420 and folate 10 were already identical at HEAD in P05-P09 and RM11 (kept per plan C13, flagged by the worker).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but the tongue shows fibrillations and fasciculations without chronic change or wasting, thoracic paraspinals show fibrillations only, and the right tibialis anterior shows sparse fibrillations and fasciculations only. Regions now: cervical, with active denervation also in bulbar, thoracic and lumbosacral muscles. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 ALS cases after the change: clean.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- Leak guard (Andrea, 24 Oct 2026: any-query outputs must not repeat any criterion's expected_evidence): action-2-check-drug-interactions.expected_evidence reworded in policy voice and the riluzole check output (followup_outputs, check_drug_interactions: the case-specific interactions line and summary) rewritten in report voice, so neither copies the other; clinical content unchanged. `test_case_guards.py -k ALS-RM11` passes.
- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- required_recommendations: must added (alcohol, as in M03).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
