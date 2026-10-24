# ALS-S02
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 94252428-71a6-4cfd-9188-9cb6d74f0d43 | FIXED | Plan C1. `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs, then respiratory, genetics, riluzole); `followup_outputs` now respiratory, genetics, riluzole; literature criterion and stored output removed; soft `sequence_constraints` EMG before genetics and before riluzole. The core work-up stays in `initial_tool_outputs`; showing it as Steps 1-4 needs the central UI change (plan 5.1). |
| 4fdb755c-8cdf-4385-8724-946b70e91ae8 | FIXED | Plan C1, C3. Riluzole check last in `followup_outputs` and `action_criteria`, after EMG by soft constraint. The false claim that riluzole affects CYP1A2 metabolism of T4 and the "TSH recheck 6 weeks after riluzole start" warning are removed; levothyroxine is now "no clinically significant interaction expected". The real point of the case (oral alendronate with dysphagia and choking) is stated in the output, the criterion and a must. |
| 3073e9a1-a2e1-4cc9-a582-f85063743afd | FIXED | Plan C4, C10. Respiratory output relabelled as reduced (FVC 68%, SNIP 42 cmH2O against the women's limit of 60) with canonical ranges; criterion `action-7` reframed as staging (recommended); `assessment.required_recommendations[1]` refers to the respiratory/NIV service now, with overnight oximetry or capnography and repeat FVC/SNIP within 3 months; prohibition "Do not wait for FVC to fall below 50%..." added. No AAN 2009 marker is met (SNIP 42 is above 40), so the reduced variant, not the NIV-discussion variant, applies. |
| de40b53e-4a47-48e3-9aa9-c0ab8b3a5b00 | FIXED | Plan C5. Genetic output now reports the full panel: C9orf72 negative plus SOD1, TARDBP, FUS and TBK1 "No pathogenic or likely pathogenic variant detected", with the canonical negative impression (a negative result does not exclude a genetic contribution). |
| ec0eb223-b51f-436d-b5ae-2f7a83b2448a | FIXED | Plan C8. "Progressive bulbar palsy variant" removed from `differential`; the phenotype is named in `key_clinical_evidence[0]` ("bulbar-onset ALS phenotype"). |
| 5609768e-5365-4b6c-a1bd-e0da827b2696 | FIXED | Plan C3. AMX0035 removed (`followup_outputs[2].output.alternatives` now empty). |
| 5e7f8b26-12a3-4f83-98b3-460f46856723 | FIXED | Case comment "solito problema pathway diagnostico": same fix as 94252428 (plan C1). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Stored output echoed the literature criterion's expected evidence and answered any query. | FIXED: null; criterion `action-1-search-medical-literature` deleted (plan C2). |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were mostly diagnostic actions (EMG, brain MRI "to exclude cervical myelopathy", lab list with HIV, RPR, SPEP, anti-GM1 and "CAG repeat in males" in a woman, "Apply Awaji/Gold Coast"); no alendronate review despite choking. | FIXED per C10: MUST-DX, MUST-RESP reduced, MUST-BULBAR dysphagia, MUST-RILUZOLE, alendronate must, MUST-MDT, MUST-GEN. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Cervical-surgery prohibition without spondylosis on imaging; functional-dismissal prohibition without a psychiatric element. | FIXED: PROHIB-IMM, PROHIB-RESP reduced, PROHIB-SWALLOW (choking documented). |
| C | major | `ground_truth.key_clinical_evidence` | El Escorial EMG pearl, generic "2-5x" CK pearl, spondylosis pearl without spondylosis, "July 2026 review" engineering pearl. | FIXED per C14: K-GC, K-EMG, K-NCS normal, K-CK at or below 5x (780 U/L, 4.6x), K-RESP, K-BULBAR. |
| C | minor | `ground_truth.differential` | MG cited "no fatigability or ocular signs" (not examined); MMN not given its supporting/against data; cervical myelopathy left low although spine MRI is normal. | FIXED: key_features from case data; MG low, the others very_low. |
| B | major | `initial_tool_outputs.labs` | No blood count, renal or liver results although the criterion required CBC and CMP; "Exclusion studies" panel with free T4 as a string and engineering text; "Reviewer baseline rule-out additions"; interpretation named ALS; CK row without `clinical_significance`. | FIXED per C13: stored values kept (CK 780, TSH 1.9, ESR 8, CRP 2, B12 420, folate 10); added normal Hb 13.2, WBC 5.8, platelets 241, Na 141, K 4.1, creatinine 0.7, glucose 89, calcium 9.3, albumin 4.0, ALT 22, AST 29, ALP 68, bilirubin 0.5, free T4 1.4 ng/dL (female reference ranges for Hb and creatinine). |
| A | major | `ground_truth.action_criteria[action-3, action-4, action-5]` | Brain MRI required `contrast: true, protocol: standard`; spine `contrast: false`; labs nine assay names; labels identical to rationales; free-text citations. | FIXED per C16/C13. |
| E | minor | `initial_tool_outputs.specialized_test` | Impression "disorder of lower anterior horn cells", em dash, missing period; sensory and motor NCS findings abbreviated ("Normal.", "No block."). | FIXED: "anterior horn cells"; findings spelled out ("All sensory NCS normal bilaterally", "No conduction block"). |
| E | minor | `initial_tool_outputs.mri` | Impression unnumbered, no final period; T2 field "Bilateral symmetric change". | FIXED: numbered 1-2; T2 "Bilateral symmetric hyperintensity". |
| D | minor | `initial_tool_outputs.body_imaging.impression` | "to explain the deficit" referred to the clinical picture. | FIXED: modality-only wording. |
| B | minor | `metadata.difficulty_rationale` | "3-4 required tools". | FIXED: four required studies. |
| B | minor | `initial_tool_outputs.labs` | ESR 8, CRP 2, B12 420, folate 10 and TSH 1.9 identical to other ALS cases (template carry-over). | FLAGGED: stored values kept. |
| D | minor | `patient.history_present_illness` | "Her thyroid function is appropriately controlled on levothyroxine (TSH normal)" while the scored labs include TSH. | FLAGGED, kept: the plan (C11) keeps S02's historical thyroid tests as legitimate history; it does not reveal any ALS-specific result. |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first (required), then baseline respiratory function (recommended), the ALS gene panel after counselling (optional) and the riluzole check (recommended), with EMG before genetics and riluzole as soft constraints; the literature step is gone. Respiratory function is reported as reduced (FVC 68%, SNIP 42 cmH2O) and the musts refer her to the respiratory/NIV service now. Because she chokes on thin liquids, the musts add an urgent speech and language therapy swallowing assessment, dietetic review and early gastrostomy discussion, and a prohibition on delaying it. The riluzole check no longer claims a CYP1A2 effect on levothyroxine or offers AMX0035; it flags oral alendronate for review given dysphagia with choking (oesophageal injury risk), which is also a must. The gene panel reports all five genes. "Progressive bulbar palsy" is no longer a competing diagnosis; it is named as the phenotype. The labs now include a full blood count and metabolic panel (added values normal) and CK 780 U/L is reported as 4.6x ULN. The brain MRI, spine MRI and EMG reports were tidied without changing findings.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Review UI: show `initial_tool_outputs` in criterion order so the core work-up reads as Steps 1-4 (plan 5.1).
- Criteria pack section 8: add `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case beyond the plan's condition-wide questions.

## Verification
Adversarial check, 23 October 2026. Read the log, the full `git diff`, the whole final case, the plan (sections 2, 3, 4 S02) and the notes file.
- All 7 note ids are in the table; each FIXED claim holds in the file (pathway order, levothyroxine no longer a CYP1A2 claim, alendronate point in output, criterion and must, reduced respiratory category against the women's SNIP limit with no AAN marker since SNIP 42 > 40, five-gene panel, PBP removed from the differential and named as phenotype, AMX0035 gone). No DECLINED or BLOCKED notes.
- Dysphagia must, PROHIB-SWALLOW and K-BULBAR are supported by the HPI (choking on thin liquids). CK ratio 780/170 = 4.6 checked. The HPI "(TSH normal)" is kept as historical thyroid follow-up per plan C11.
- Found and fixed (B, minor; same class the worker fixed in S03-S05 but missed here): the EMG impression, `quantitative_data.classification` and the EMG criterion's `expected_evidence` claimed chronic reinnervation in all four regions, and MUST-DX and K-GC claimed LMN involvement in the thoracic and lumbosacral regions, while the findings show large MUPs only in the tongue and hand muscles (thoracic paraspinals: fibrillations only; tibialis anterior: fibrillations and fasciculations; the leg exam has only mild hip flexor weakness). Rewritten: active denervation in four regions, fasciculations in tongue, hand muscles and tibialis anterior, chronic change in tongue and hand muscles; MUST-DX and K-GC now state LMN involvement in the bulbar and cervical regions with active denervation also in thoracic and lumbosacral muscles. Gold Coast remains met (UMN plus LMN signs in the bulbar and cervical regions).
- Noted for the lead, not changed: the canonical K-NCS pearl mentions SBMA in a woman (plan text used verbatim; plan C8 deletes the Kennedy entry in women). Consider a women's variant of K-NCS without "or SBMA" (also S04).
- `perfect_agent.py ALS-S02 -v` ok; `case_io.py check` clean for the case.

## Condition audit (ALS lead, 23 Oct 2026)
- `ground_truth.key_clinical_evidence[2]` (K-NCS): "or SBMA" removed. SBMA is X-linked and affects men; the plan's C8 already drops the Kennedy entry in women, so the pearl named a mimic that cannot apply (flagged by the S02, S04, S07 and S09 verifiers as a class).

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- Leak guard (Andrea, 24 Oct 2026: any-query outputs must not repeat any criterion's expected_evidence): action-2-check-drug-interactions.expected_evidence reworded in policy voice and the riluzole check output (followup_outputs, check_drug_interactions: the case-specific interactions line and summary) rewritten in report voice, so neither copies the other; clinical content unchanged. `test_case_guards.py -k ALS-S02` passes.
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
