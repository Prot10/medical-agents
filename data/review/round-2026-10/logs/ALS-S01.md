# ALS-S01
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 2f8554cc-e73a-4b67-bb1b-79654ca218f9 | FIXED | Plan C1. `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs, then respiratory, genetics, riluzole); `followup_outputs` now respiratory, genetics, riluzole; literature criterion and stored output removed; soft `sequence_constraints` EMG before genetics and before riluzole. The core work-up stays in `initial_tool_outputs`; showing it as Steps 1-4 needs the central UI change (plan 5.1). |
| 6c4e6bd6-0841-4774-a9d3-913a918b1ded | FIXED | Plan C1, C3. Riluzole check is last in `followup_outputs` and `action_criteria`, after EMG by soft constraint; its criterion is labelled as a pre-treatment step once the diagnosis is established. |
| cba80908-ce68-45d4-a85a-3910319e8ca9 | FIXED | Plan C9. `key_clinical_evidence[3]`: CK 920 U/L is 5.3x ULN, higher than usual in ALS; consider a myopathic contributor including statin myopathy on atorvastatin; the neurogenic EMG with fasciculations and UMN signs argues against a primary myopathy. Lab `interpretation` gives "CK 920 U/L (5.3x ULN)". `differential` gains "Statin-associated myopathy" (low) with supports/against. Riluzole output and criterion note that atorvastatin also raises transaminases. |
| 4d83e271-9b37-4f1e-af28-21d924b84d6f | FIXED | Plan C4. Respiratory criterion `action-7` reframed as staging (recommended) and placed after the diagnostic core; output reference ranges and impression rewritten (normal: FVC 82%, SNIP 74 cmH2O, baseline for serial monitoring); MUST-RESP normal and PROHIB-RESP normal added. |
| 12755d6e-6f26-418b-bbd6-75f34a5e5f19 | FIXED | Plan C3. AMX0035 removed from `followup_outputs[2].output.alternatives` (now empty); output rebuilt to the canonical structure. |
| 2fab0386-647b-491c-a53c-1b6522a941a0 | FIXED | Plan C5. Genetic criterion `action-8` optional, after EMG by soft constraint, canonical label/rationale; output completed with TARDBP, FUS and TBK1 and the canonical negative impression. |
| cebdf45d-ca48-4810-bd83-0437e64de918 | FIXED | Case comment "solito pathway sbagliato": same fix as 2f8554cc (plan C1). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Stored output echoed the literature criterion's expected evidence and answered any query. | FIXED: null; criterion `action-1-search-medical-literature` deleted (plan C2). |
| B | major | `initial_tool_outputs.labs` | No blood count, renal or liver results although the criterion required CBC and CMP and riluzole needs a liver baseline; "Exclusion studies" panel (free T4 as a string, engineering `clinical_significance`); "Reviewer baseline rule-out additions"; interpretation named ALS. | FIXED per C13: stored values kept (CK 920, TSH 2.1, ESR 8, CRP 2, B12 420, folate 10); added normal Hb 15.1, WBC 7.4, platelets 265, Na 139, K 4.5, creatinine 1.0, glucose 98, calcium 9.6, albumin 4.4, ALT 31, AST 38, ALP 81, bilirubin 0.6, free T4 1.2 ng/dL. |
| A | major | `ground_truth.action_criteria[action-3, action-4, action-5]` | Brain MRI required `contrast: true, protocol: standard`; spine required `contrast: false`; labs required nine assay names; labels identical to rationales; free-text citations. | FIXED per C16/C13 (`{}`, `{"study": "spine_MRI"}`, core CBC/CK/TSH/vitamin_B12; canonical text; bracketed keys). |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions (including a lab list with HIV, RPR, SPEP, anti-GM1, CAG repeat); cervical-surgery prohibition without spondylosis on imaging; functional-dismissal prohibition without any psychiatric element. | FIXED: rebuilt per C10 (MUST-DX, MUST-RESP normal, MUST-BULBAR signs for bilateral tongue atrophy, MUST-RILUZOLE, MUST-MDT, MUST-GEN; PROHIB-IMM, PROHIB-RESP normal). |
| C | major | `ground_truth.key_clinical_evidence` | El Escorial EMG pearl, "2-5x" CK pearl (CK is 5.3x on a statin), spondylosis pearl without spondylosis, "July 2026 review" engineering pearl. | FIXED per C14 (K-GC, K-EMG, K-NCS normal, K-CK >5x with statin, K-RESP). |
| C | minor | `ground_truth.differential` | MMN cited "anti-GM1 negative" and Kennedy "androgen receptor CAG repeat normal" (neither tested); MG cited "no fatigability" (not examined); statin myopathy, the mimic the case itself raises, was absent; cervical myelopathy left low although spine MRI is normal. | FIXED: key_features from case data; statin-associated myopathy low; cervical spondylotic myelopathy, MG, IBM, Kennedy very_low; MMN low. |
| E | minor | `initial_tool_outputs.specialized_test.impression` | "disorder of lower anterior horn cells", em dash, missing period. | FIXED: "widespread disorder of anterior horn cells". |
| E | minor | `initial_tool_outputs.mri.impression` | Third finding unnumbered and without a period. | FIXED: numbered 1-3. |
| D | minor | `initial_tool_outputs.body_imaging.impression` | "to explain the deficit" referred to the clinical picture. | FIXED: modality-only wording. |
| B | minor | `fallback_tool_outputs.ecg.intervals.QRS` | "Incomplete right bundle branch block" with QRS 98 ms (incomplete RBBB needs QRS 110-119 ms in adults). | FIXED: QRS 112 ms. |
| B | minor | `metadata.difficulty_rationale` | "3 required tools sufficient" (4 required studies). | FIXED. |
| B | minor | `initial_tool_outputs.labs` | CK 920 identical to M02 and S08; ESR 8, CRP 2, B12 420, folate 10 identical to RS11 (template carry-over). | FLAGGED: stored values kept, as the plan instructs (C9). |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first (required), then baseline respiratory function (recommended, normal: FVC 82%, SNIP 74 cmH2O), the ALS gene panel after counselling (optional, all five genes negative) and the riluzole check (recommended), with EMG before genetics and riluzole as soft constraints; the literature step is gone. The CK of 920 U/L is described as 5.3x ULN, higher than usual for ALS, with statin myopathy on atorvastatin to consider and the neurogenic EMG arguing against a primary myopathy; statin-associated myopathy is now a low-likelihood differential. The riluzole check no longer offers AMX0035 and notes that atorvastatin can also raise transaminases. Musts are now management (disclosure by Gold Coast criteria, 3-monthly FVC/SNIP with symptom screening, speech and swallowing assessment for the bilateral tongue atrophy, riluzole with the SmPC transaminase schedule, specialist MDT, genetic counselling); the irrelevant cervical-surgery and functional-dismissal prohibitions are removed. The labs now include a full blood count and metabolic panel (added values normal). The EMG, brain MRI and spine MRI impressions were tidied without changing findings.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Review UI: show `initial_tool_outputs` in criterion order so the core work-up reads as Steps 1-4 (plan 5.1).
- Criteria pack section 8: add `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case beyond the plan's condition-wide questions.

## Verification
Adversarial check, 23 October 2026. Read the log, the full `git diff`, the whole final case, the plan (sections 2, 3, 4 S01) and the notes file.
- All 7 note ids are in the table; each FIXED claim holds in the file (pathway order and soft constraints, CK 5.3x pearl with statin context and statin-myopathy differential, respiratory normal category, AMX0035 gone, atorvastatin transaminase point in the riluzole output and criterion, five-gene panel). No DECLINED or BLOCKED notes.
- No banned text left (AMX0035, grapefruit, El Escorial, anti-GM1, CAG repeat, "July 2026"); initial literature and interaction blocks null; ECG fallback QRS 112 ms now agrees with incomplete RBBB; CK ratio 920/174 = 5.3 checked; MUST-DX signs match the exam (bilateral Hoffman, right Babinski).
- Found and fixed (B, minor): the EMG impression and the EMG criterion's `expected_evidence` claimed chronic reinnervation in all four regions, and MUST-DX and K-GC claimed LMN involvement in the thoracic region, but the thoracic finding is fibrillations and fasciculations only. Rewritten to active denervation in four regions with chronic neurogenic change (large MUPs or reduced recruitment) in the bulbar, cervical and lumbosacral regions; MUST-DX and K-GC now add "with active denervation also in thoracic paraspinal muscles". Consistent with the worker's own correction in S03-S05.
- Found and fixed (B, minor): SOD1 result string harmonised with the other genes and the impression ("No pathogenic or likely pathogenic variant detected").
- `perfect_agent.py ALS-S01 -v` ok; `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- required_recommendations: must added (statin review for CK 5.3x ULN on atorvastatin).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
