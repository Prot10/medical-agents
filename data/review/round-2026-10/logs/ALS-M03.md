# ALS-M03
Reviewer status: R1 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0b0e9b4c-4820-4156-9474-fc3e254783d8 | FIXED | `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. Core studies stay in `initial_tool_outputs` (plan C1). |
| 58cf87ba-7f2f-47ae-98df-2d3ebeccd299 | FIXED | Riluzole/apixaban check last (`action_criteria[6]`, `followup_outputs[2]`), soft constraint after EMG; output rewritten (apixaban, metoprolol, lisinopril no interaction; alcohol advice; no AMX0035/edaravone). |
| 0ba850d5-eefe-40f3-9b64-87ec1a0cd0d5 | FIXED | EMG/NCS is `action_criteria[0]`, required; report impression numbered with bulbar, cervical, thoracic and early lumbosacral denervation, normal sensory NCS and no conduction block; expected evidence states the same. |
| 077c2cc4-793d-48e5-9181-669f94947af2 | FIXED | Respiratory function recommended, directly after the diagnostic core (`action_criteria[4]`, `followup_outputs[0]`); NIF -55 now drives an NIV referral must. |
| 2255e7cd-9288-465f-8968-4386905b2d03 | FIXED | Swallowing must (MUST-BULBAR dysphagia) moved to `required_recommendations[1]`, right after the diagnosis, with the living-alone clause (son helps with meals; OT and home support); PROHIB-SWALLOW added. |
| 5c29680e-032c-4cdd-a68e-0ceef347bd01 | FIXED | Genetic panel optional, after the core and counselling (`action_criteria[5]`, `followup_outputs[1]`), soft constraint after EMG. |
| ea4bbcb7-e208-4d41-8967-e7c60ffe62d2 | FIXED | Brain MRI criterion rationale: MRI does not confirm ALS; excludes infarcts (relevant with atrial fibrillation) and brainstem lesions; corticospinal signal supportive only. MRI impression reworded accordingly ("no acute or chronic infarct"). |
| 97ab4bf6-1a0c-467f-8981-6c6769ec109e | FIXED | Same as 0b0e9b4c for the pathway, and 2255e7cd for the early swallowing/aspiration-risk must. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | HPI gave the result of the brain MRI the case scores ("showed no infarct but ... subtle changes in the corticospinal tracts") and a reasoning sentence ("the progressive course ... does not fit a vascular etiology"). | FIXED: neutral sentence: the cardiologist considered an embolic event and referred him. |
| D | major | `initial_tool_outputs.literature_search`, `action-1-search-medical-literature` | Literature echo of expected evidence. | FIXED: deleted (C2). |
| C | major | `followup_outputs[2].output` | AMX0035 and edaravone as alternatives; generic "avoid CYP1A2 inhibitors"; no mention of his nightly alcohol. | FIXED: canonical riluzole output with the plan's M03 content. |
| B | minor | `initial_tool_outputs.specialized_test` | `regions_denervated` "bulbar definite, cervical definite, thoracic definite" (C7); impression cites positive sharp waves the findings do not report; "Pulmonary function testing recommended." | FIXED: "bulbar, cervical, thoracic; lumbosacral early"; impression lists fibrillations and complex fasciculations; recommendation removed. |
| D | minor | `initial_tool_outputs.mri` | "No hemorrhage - important given anticoagulation" (cross-modality reasoning); imaging differential "demyelination" while the report finds no plaques; "acute" infarct only, although chronic emboli are the AF question. | FIXED: observation "No hemorrhage"; impression numbered: nonspecific corticospinal signal, no acute or chronic infarct, hemorrhage, mass or plaque, mild atrophy. |
| D | minor | `initial_tool_outputs.body_imaging` | Empty findings; impression "to explain the deficit" (clinical reasoning). | FIXED: normal cervical and thoracic findings added; plain impression. |
| E | minor | `initial_tool_outputs.labs` | "Exclusion studies" with string free T4, "Reviewer baseline rule-out additions", interpretation naming ALS; no liver tests although he drinks nightly and riluzole needs a baseline; no potassium or calcium. | FIXED: panels per C13, stored values kept; added potassium 4.2, calcium 9.3, albumin 4.0, ALT 26, AST 30, ALP 74, bilirubin 0.8, free T4 1.1; interpretation "CK 612 U/L (3.5x ULN)". |
| B | minor | `followup_outputs[0].output` | Bare "Abnormal values" impression; SNIP/NIF limits not per the dataset convention. | FIXED: ranges per C4, `flag` per finding, reduced impression. |
| B | minor | `followup_outputs[1].output` | TBK1 missing; generic impression. | FIXED. |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions and an untested lab list; no NIV referral although NIF -55 meets an AAN marker; cervical-surgery and functional prohibitions with no basis in the case. | FIXED: MUST-DX, MUST-BULBAR (second), MUST-RESP AAN marker (NIF -55), MUST-RILUZOLE, alcohol/apixaban must, MUST-MDT, MUST-GEN; prohibitions PROHIB-IMM, PROHIB-RESP reduced, PROHIB-SWALLOW. |
| C | major | `ground_truth.differential` | Progressive bulbar palsy (ALS phenotype) listed moderate; MG "denervation rather than decrement" (no repetitive stimulation done); brainstem lesion "excluded by brain MRI" without supports/against; no MMN entry. | FIXED: PBP deleted; brainstem stroke or tumour, MG, MMN, cervical myelopathy low and oropharyngeal dystonia very_low, all with case data. |
| E | minor | `ground_truth.key_clinical_evidence` | Template pearls (July 2026 review, 2-5x CK, El Escorial EMG, spondylosis pearl without spondylosis). | FIXED: K-GC, K-EMG, K-NCS normal, K-CK 3.5x, K-RESP, K-BULBAR. |
| C | minor | `ground_truth.red_herrings` | Empty, although the case raises a vascular explanation (atrial fibrillation, cardiologist's embolic question). | FIXED: red herring added, pointing to the HPI. |
| A | minor | `ground_truth.action_criteria` | C16 mechanics and citation format. | FIXED. |
| C | minor | `metadata.notes` | "Rapid progression indicated by high NfL": no NfL in the case (C17). | FIXED: notes reworded to the case's data. |

## Changes, in one paragraph a physician can read before re-reviewing

The work-up now starts with EMG/NCS, brain MRI, spine MRI and mimic-exclusion bloods (all required), then baseline respiratory function (recommended), the gene panel after counselling (optional) and the riluzole interaction check (recommended); the literature step is gone. The HPI no longer reports the cardiologist's brain MRI; the AF/embolic question stays and is now an explicit red herring. The brain MRI says no acute or chronic infarct, hemorrhage, mass or plaque, with nonspecific corticospinal tract signal; the spine MRI is reported as normal without reasoning; labs are regrouped with liver tests added (normal) and CK 612 U/L (3.5x ULN); the respiratory report states reduced FVC 68%, SNIP 41 and NIF -55. The riluzole check says apixaban, metoprolol and lisinopril do not interact and advises reducing his nightly alcohol. Musts: Gold Coast diagnosis and disclosure; an urgent swallowing assessment with dietetics and early gastrostomy discussion, placed second because he chokes on thin liquids and lives alone (son helps with meals, OT and home support); NIV referral now (NIF -55 meets an AAN 2009 marker); riluzole with SmPC monitoring; alcohol reduction with apixaban unchanged; MDT; genetic counselling. Progressive bulbar palsy is no longer a competing diagnosis. The label "clinically definite" is kept (Awaji definite is met; plan C7).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1.
- Review UI: initial work-up in criterion order (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- The plan text for note 2255e7cd is ambiguous ("placed second ... after MUST-DX and MUST-RESP"). I put the swallowing must second, before the respiratory must, because the reviewer asked for it to be highlighted as the early safety action.
- If gastrostomy is chosen, apixaban will need peri-procedural interruption; I did not add this as a must because the decision lies beyond this encounter.

## Verification

Checked: every note id of the case is in the table and each FIXED claim holds in the file (criteria order and tiers per plan 3.1, follow-ups respiratory, genetics, riluzole; literature and initial DI null; both soft constraints; stop rule unchanged); stored lab and respiratory values unchanged against HEAD (only free T4 string made numeric, plan C13); CK multiple recomputed; HPI free of scored results; musts, prohibitions and differential against the plan's per-case decisions; no AMX0035, edaravone, grapefruit, El Escorial, untested anti-GM1/CAG, "July 2026" or new dashes; perfect_agent.py and case_io.py check clean after the changes.

Found and changed:
- EMG impression item 1, `quantitative_data.criteria` and the EMG criterion `expected_evidence` claimed chronic reinnervation in the thoracic region and in mentalis, but the findings record only fibrillations (and sparse fasciculations) there; chronic change is recorded in tongue and cervical muscles, and lumbosacral involvement is early (mildly large MUPs, sparse fibrillations). All three now state exactly that.

Swallowing must placed second (before MUST-RESP) per note 2255e7cd: accepted.

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` replaces the `flag` low/normal field, set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but thoracic paraspinals (T7-T9) show fibrillations and sparse fasciculations only. Regions now: bulbar, cervical and lumbosacral (tibialis anterior: mildly large MUPs with sparse fibrillations), with active denervation also in thoracic paraspinal muscles. The label "clinically definite" still holds (bulbar plus two spinal regions with upper motor neuron signs). Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 ALS cases after the change: clean.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- Leak guard (Andrea, 24 Oct 2026: any-query outputs must not repeat any criterion's expected_evidence): action-2-check-drug-interactions.expected_evidence reworded in policy voice and the riluzole check output (followup_outputs, check_drug_interactions: the case-specific interactions line and summary) rewritten in report voice, so neither copies the other; clinical content unchanged. `test_case_guards.py -k ALS-M03` passes.
- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- required_recommendations: must added (cognitive/behavioural screen and pseudobulbar affect).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
