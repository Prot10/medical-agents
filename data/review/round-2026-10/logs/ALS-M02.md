# ALS-M02
Reviewer status: R1 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 48e28c3c-7c64-4210-933f-6cba6ee108da | FIXED | `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. Core studies stay in `initial_tool_outputs` (plan C1). |
| 27adc963-aeb2-4a5e-95e1-f803b060889d | FIXED | EMG/NCS is `action_criteria[0]` (required). Its report (`initial_tool_outputs.specialized_test`) keeps the multi-region active and chronic change and now states no conduction block explicitly; expected evidence names it. |
| 81aad685-02fa-4795-a247-34da189eb8e9 | FIXED | Riluzole check last (`action_criteria[6]`, `followup_outputs[2]`), soft constraint after EMG; output rewritten without AMX0035, edaravone or the metformin "hepatic" claim. |
| f3825c75-09df-4ea2-8ff8-e05d432f9bd2 | FIXED | Respiratory function recommended, after the core (`action_criteria[4]`, `followup_outputs[0]`), relabelled as staging. |
| 77948566-be4b-441d-8ce0-a7a2eb9399a9 | FIXED | Genetic panel optional, after the core with pre-test counselling (`action_criteria[5]`, `followup_outputs[1]`), soft constraint after EMG. |
| c04b142c-9259-4485-860e-b00292be8d5a | FIXED | `ground_truth.red_herrings[0]` rewritten with the reviewer's content and the canonical >5x wording (CK 920 = 5.3x ULN, statin can contribute, neurogenic EMG, fasciculations, largely preserved sensation and UMN signs argue against primary myopathy); field_path now `initial_tool_outputs.labs.panels.Creatine kinase[0]`; K-CK >5x pearl and a low "statin-associated myopathy" differential entry added. |
| 82961391-3081-41be-92f0-0d024951c17f | FIXED | Brain MRI criterion rationale "MRI does not confirm ALS ... supportive only"; MRI impression calls corticospinal and motor-cortex signal nonspecific. |
| e04aa960-9f76-4a7f-bedb-a5acb384fd96 | FIXED | Same as 48e28c3c (diagnostic block first: EMG/NCS, brain and spine MRI, targeted labs). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | HPI gave the lumbar MRI result and its interpretation and the CK value (920 U/L), both scored studies. | FIXED: replaced by a neutral referral sentence; the orthopaedic shoulder X-ray (not scored) stays. |
| B | minor | `patient.neurological_exam.additional` | "right deltoid" fasciculations vs "bilateral deltoids" in the motor exam. | FIXED: "both deltoids". |
| C | major | `initial_tool_outputs.specialized_test.findings[5]` | Sural 14 uV and superficial peroneal 12 uV were called "borderline low": both are normal at 58, so the report contradicted its own values while the exam (reduced toe vibration, diabetes) supports a mild neuropathy. | FIXED: values set to sural 5 uV and superficial peroneal 4 uV with stated lower limits, so the "mildly reduced" reading and the K-NCS reduced-sural pearl hold. |
| B | minor | `initial_tool_outputs.specialized_test` | "Insufficient for definite bulbar denervation" (Awaji-style wording inside the report); "no conduction block at standard entrapment sites" only; "Pulmonary function testing recommended."; prose impression. | FIXED: tongue finding stated plainly; "No conduction block or temporal dispersion"; recommendation removed; numbered impression. |
| B | minor | `initial_tool_outputs.mri` | Impression numbered "1 ... 4."; "no enhancing lesion" with no contrast documented. | FIXED: numbered 1-2, motor-cortex observation brought into the impression as nonspecific, enhancement phrase removed. |
| C | minor | `initial_tool_outputs.body_imaging` | JSON dump; "right L5 foraminal narrowing" at L4-L5; "no cord compression" at L4-L5 (no cord there); interpretive "insufficient to explain bilateral leg weakness"; region "cervical and thoracic spine" while lumbar levels are described; impression starting at "2."; thoracic cord not reported. | FIXED: region "cervical, thoracic and lumbosacral spine"; plain findings (L4-L5 foramen, no root or cauda equina compression, conus normal); normal thoracic cord added; numbered impression. |
| E | minor | `initial_tool_outputs.labs` | "Exclusion studies" with Free T4 as a string and a sentence about the case's diagnosis; "Reviewer baseline rule-out additions"; interpretation naming ALS; no liver tests although riluzole needs a baseline. | FIXED: panels per C13; stored values kept; added calcium 9.4, albumin 4.3, ALT 31, AST 36, ALP 81, bilirubin 0.6 and numeric free T4 1.2; interpretation lists glucose and CK (5.3x ULN). |
| D | major | `initial_tool_outputs.literature_search`, criterion `action-1-search-medical-literature` | Literature echo of the expected evidence. | FIXED: deleted (C2). |
| B | minor | `followup_outputs[0].output` | Respiratory impression "All values within normal limits" with no reference conventions. | FIXED: ranges per C4, `flag` per finding, canonical normal impression. |
| B | minor | `followup_outputs[1].output` | TBK1 missing; generic impression. | FIXED: TBK1 negative added; canonical negative impression. |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions and a lab list including untested HIV/RPR/SPEP/anti-GM1/CAG repeat; cervical-surgery prohibition without cervical spondylosis on imaging; functional prohibition without any psychiatric element. | FIXED: musts MUST-DX, MUST-RESP normal (with a clause on his CPAP-treated OSA), MUST-RILUZOLE, MUST-MDT, MUST-GEN; prohibitions PROHIB-IMM, PROHIB-RESP normal, PROHIB-SURG lumbar (L4-L5). |
| C | major | `ground_truth.differential` | Cervical radiculopathy/myelopathy left moderate; flail-arm variant (an ALS phenotype) as a competitor; MMN citing an untested anti-GM1 and "sensory NCS normal" (lower limb SNAPs are reduced); IBM citing tongue fasciculations he does not have; no entry for the lumbar disease or the statin, both raised by the case. | FIXED: cervical low, lumbar radiculopathy low (added), statin-associated myopathy low (added), MMN low, IBM low, MG very_low, all with supports/against from case data; flail-arm deleted. |
| E | minor | `ground_truth.key_clinical_evidence` | "July 2026 review" pearl; 2-5x CK pearl (CK is 5.3x); "Normal sensory NCS ... pivotal" although lower limb SNAPs are reduced; El Escorial EMG pearl. | FIXED: rebuilt (K-GC, K-EMG, K-NCS reduced-sural with diabetes, K-CK >5x with statin, K-RESP normal, lumbar/cervical spine pearl). |
| A | minor | `ground_truth.action_criteria` | Criteria mechanics and citations as in C16 (brain MRI `contrast/protocol`, spine `contrast:false`, free-text citations, label = rationale). | FIXED: canonical criteria. |
| C | minor | `ground_truth.red_herrings` | The lumbar disc disease, a confounder the case raises, had no red herring. | FIXED: red herring added (no root compression; cannot explain UMN signs or cervical and thoracic denervation). |
| C | minor | `metadata.notes` | "anti-GM1 negative excludes MMN" (never tested) and "hexosaminidase A important in African American patient" (adult hexosaminidase A deficiency is linked to Ashkenazi ancestry; not in the case). | FIXED: notes reworded to the case's data. |
| B | minor | `initial_tool_outputs.labs` | CK 920 U/L is the same value as S01 and S08 (template). | FLAGGED only (plan C9 keeps stored CK values). |

## Changes, in one paragraph a physician can read before re-reviewing

The required work-up is now EMG/NCS, brain MRI, spine MRI and mimic-exclusion bloods (criteria 1-4), then baseline respiratory function (recommended), the ALS gene panel after counselling (optional) and the riluzole interaction check (recommended); the literature step is gone. The HPI no longer reports the lumbar MRI or the CK. The EMG report states active and chronic denervation in cervical, thoracic and lumbosacral muscles, tongue fasciculations only, normal conduction without block and, consistent with his diabetes and reduced toe vibration, mildly reduced sural (5 uV) and superficial peroneal (4 uV) responses (previously 14 and 12 uV, which are normal yet were called borderline). The spine MRI now covers the levels it describes, places the L4-L5 change correctly (no root compression; no "cord" at L4-L5) and adds the thoracic cord. Labs are regrouped with liver tests and free T4 added (normal) and CK 920 U/L reported as 5.3x ULN. The CK red herring and pearl say that 5.3x is higher than usual in ALS and that statin myopathy can contribute, while the neurogenic EMG and UMN signs argue against a primary myopathy; a statin-myopathy and a lumbar-radiculopathy entry join the differential (both low), and the flail-arm "competitor" is removed. Musts are diagnosis and disclosure, 3-monthly respiratory monitoring (noting his CPAP-treated sleep apnoea), riluzole with SmPC monitoring, MDT and genetic counselling; prohibitions cover immunotherapy, stopping respiratory monitoring and lumbar surgery.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1 (`[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]`).
- Review UI: initial work-up in criterion order (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- Plan C9 says the CK row keeps `clinical_significance` null, C13 says abnormal rows carry "Above reference range". I applied C13 to every abnormal row (CK and glucose) for consistency inside the panel; the phrase is factual, not interpretive.
- With CK 5.3x ULN on atorvastatin, a neurologist might also pause the statin and recheck CK. The plan's case-specific musts do not include it, so I did not add a must; the pearl and the differential ask for the myopathic contributor to be considered.
- The sensory NCS values were changed (14 to 5 uV, 12 to 4 uV) to make the report agree with its own reading; the alternative was to call them normal and drop the neuropathy, which would leave the reduced toe vibration unexplained.

## Verification

Checked: every note id of the case is in the table and each FIXED claim holds in the file (criteria order and tiers per plan 3.1, follow-ups respiratory, genetics, riluzole; literature and initial DI null; both soft constraints; stop rule unchanged); stored lab and respiratory values unchanged against HEAD (only free T4 string made numeric, plan C13); CK multiple recomputed; HPI free of scored results; musts, prohibitions and differential against the plan's per-case decisions; no AMX0035, edaravone, grapefruit, El Escorial, untested anti-GM1/CAG, "July 2026" or new dashes; perfect_agent.py and case_io.py check clean after the changes.

Found and changed:
- EMG impression item 1 and the EMG criterion `expected_evidence` claimed chronic reinnervation in the thoracic region, but the thoracic finding is T8 paraspinal fibrillations with sparse fasciculations only (the worker fixed the same defect in M05 and M06, not here): now chronic change in cervical and lumbosacral limb muscles, with fibrillation potentials in cervical (C5-C7) and thoracic (T8) paraspinals.
- `metadata.difficulty_rationale` called the CK "mild CK elevation as classic non-distractor red herring", contradicting the 5.3x ULN framing of the red herring and pearl: now "CK 5.3x ULN on atorvastatin as a red herring".

Accepted as logged: sural 14 to 5 uV and superficial peroneal 12 to 4 uV (makes the report agree with its own reading, the exam and plan K-NCS reduced-sural).

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` replaces the `flag` low/normal field, set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but thoracic paraspinals (T8) show fibrillations only. Regions now: cervical and lumbosacral, with active denervation also in thoracic paraspinal muscles. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 ALS cases after the change: clean.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- required_recommendations: must added (statin review for CK 5.3x ULN on atorvastatin).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
