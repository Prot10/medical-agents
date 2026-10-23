# ALS-S07
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| c6e254ac-760f-4ca3-a01a-c68755b41a37 | FIXED | Action criteria reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. `ground_truth.action_criteria`, `followup_outputs`, `ground_truth.sequence_constraints`, `initial_tool_outputs.literature_search` = null. Core studies stay in `initial_tool_outputs` (plan C1; display is CENTRAL 1). |
| fe18f6ef-828e-484f-bfba-068c63ac158f | FIXED | `initial_tool_outputs.specialized_test`: new "Motor NCS" finding (median, ulnar, peroneal, tibial: CMAP reduced in the right median and ulnar recordings, normal elsewhere; distal latencies and velocities normal; no conduction block, no temporal dispersion); sensory row names median, ulnar and sural; impression item 2 states "no conduction block"; `quantitative_data.conduction_block` = "None". |
| 7949f4b4-0594-4e58-89b8-e2681078e02d | FIXED | Riluzole check moved last. Output: serotonin-syndrome statement and "anxiety exacerbation with serotonergic medications" warning removed; escitalopram "no clinically significant interaction expected; escitalopram does not inhibit CYP1A2 to a relevant degree and riluzole has no serotonergic action"; canonical LFT and neutropenia summary. Criterion label, rationale, expected_evidence, citations rewritten. |
| c66738c7-1f13-4a53-8173-a2e041e3670d | FIXED | `ground_truth.red_herrings[0]` added (anxiety disorder, past medical history) with the plan's C15 text, which is the note's wording; PROHIB-FUNC kept: "Do not attribute the progressive weakness, wasting or bulbar signs to anxiety or a functional disorder." |
| 1335871c-a9dc-4803-b97e-6bb95abd175b | FIXED | Respiratory follow-up now first follow-up after the core; criterion `action-7` recommended with staging label and rationale; output impression "FVC 90% predicted and SNIP 82 cmH2O are within normal limits; baseline for serial monitoring."; reference ranges FVC >=80% predicted, SNIP >=60 cmH2O (women). |
| 3234e797-519b-42fd-8f72-700313f01092 | FIXED | Genetic output reports all five genes (C9orf72 repeat-primed PCR; SOD1, TARDBP, FUS, TBK1 sequencing, all negative) with the canonical negative impression. |
| 0ef6c4bc-ba44-47ae-95c6-8043706657f7 | FIXED | Differential entry renamed "Familial (monogenic) ALS", moderate -> low: supports onset at 50; against no family history and a negative five-gene panel. The genetic criterion stays optional; its rationale names the younger onset as a reason to offer testing. |
| 4e7e33b6-2034-463e-81d3-c799f8c7c835 | FIXED | AMX0035 removed (`followup_outputs[2].output.alternatives` = []). |
| 2666c318-b24e-43a3-a6cf-cae6fe2a993f | FIXED | Case comment (pathway, conduction block, escitalopram wording, C9-only panel): each part resolved as under c6e254ac, fe18f6ef, 7949f4b4 and 3234e797. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Literature output echoed the criterion's expected_evidence; served to any search. | FIXED: null; literature criterion deleted (C2). |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were diagnostic actions and a lab list including "androgen receptor CAG repeat in males" in a woman; genetic panel ordered as a must. | FIXED: rebuilt per C10: MUST-DX, MUST-RESP normal, MUST-RILUZOLE, MUST-MDT, MUST-GEN sporadic. No bulbar must (tongue fasciculations only, "No dysarthria yet"). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Cervical-surgery prohibition with no spondylosis on imaging; respiratory prohibition written for a symptomatic patient. | FIXED: PROHIB-IMM, PROHIB-RESP normal, PROHIB-FUNC. |
| C, E | minor | `ground_truth.key_clinical_evidence` | Generic 2-5x CK pearl, El Escorial-style EMG pearl, spondylosis pearl without spondylosis, tofersen pearl, "July 2026 review" engineering text. | FIXED: K-GC, K-EMG, K-NCS normal, K-CK (580 U/L = 3.4x ULN), K-RESP normal. |
| B | major | `initial_tool_outputs.specialized_test` | Impression claimed chronic reinnervation in four regions; findings showed chronic change only in the right hand muscles. | FIXED: tibialis anterior row now carries large, long-duration MUPs with reduced recruitment; impression states chronic change in cervical and lumbosacral muscles (tongue: fibrillations and fasciculations only); numbered impression. |
| A, B | minor | `initial_tool_outputs.mri` | `signal_characteristics` `{"T2": "Bilateral"}`; additional_observations duplicated the impression. | FIXED: T2 and FLAIR hyperintense; numbered impression; brainstem normal. |
| D | minor | `initial_tool_outputs.body_imaging.impression` | "to explain the deficit" referenced the clinical picture; findings empty. | FIXED: per-level findings and plain impression (no cord or root compression, no cord signal abnormality or mass). |
| A, D | major | `initial_tool_outputs.labs` | "Exclusion studies" panel with free T4 as a string and a sentence about the case's diagnosis; "Reviewer baseline rule-out additions"; interpretation names ALS; no CBC, renal or liver tests. | FIXED: C13 panels; stored CK 580, TSH 2.0, B12, folate, ESR, CRP kept; normal CBC, CMP (female reference ranges) and free T4 1.1 ng/dL added; canonical interpretation. |
| C | minor | `ground_truth.action_criteria` | Brain MRI required contrast and protocol; spine required `contrast: false`; lab criterion required CMP, calcium, folate, ESR, CRP spellings; label = rationale; free-text citations. | FIXED: C16 arguments, C3-C6/C12/C13 texts, bracketed citations. |
| C | minor | `ground_truth.differential` | MMN cited "anti-GM1 negative" (never tested); HSP and HMN key features thin; the commonest structural mimic of hand wasting with hyperreflexia was absent although the spine MRI is required to exclude it. | FIXED: supports/against wording from the case's data; added "Cervical spondylotic myelopathy with radiculopathy" low; hereditary motor neuropathy very_low. |
| D | minor | `patient.history_present_illness`, `patient.neurological_exam.additional` | HPI: "she recognized the combination of upper and lower motor neuron signs"; exam additional: "Combined upper and lower motor neuron signs in a younger patient" (synthesis, plan C11 lists S07). | FIXED: HPI keeps her concern about ALS in plain words; exam `additional` set to null (it held only the synthesis). |
| B | minor | `metadata.difficulty_rationale` | "Genetic panel elevated to required" is untrue (optional). | FIXED: reworded to the case's actual confounders. |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first, then respiratory function, the gene panel and the riluzole check; the literature step is gone. The EMG report now includes motor conduction studies with no conduction block and an impression whose chronic-change claim matches the findings. Labs are reported as standard panels (CK 580 U/L, 3.4x ULN; everything else normal, including a full blood count, metabolic panel and numeric thyroid tests). The gene panel reports all five genes, negative, so familial ALS is low in the differential. The riluzole check states that escitalopram does not interact (no serotonergic or CYP1A2 effect) and gives the standard LFT schedule without AMX0035. The anxiety disorder is now an explicit red herring with the reviewer's wording, and the musts are management (diagnosis and disclosure, 3-monthly respiratory monitoring, riluzole with monitoring, MDT, genetic counselling).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Review UI: show the initial work-up and follow-ups in criterion order (plan 5.1).
- New citation keys per plan 1.1 (criteria pack section 8).

## Open questions for Andrea (judgment calls you could not settle)
- To make the EMG findings agree with the impression I added "large, long-duration motor unit potentials with reduced recruitment" to the tibialis anterior row; the tongue keeps active denervation only. Gold Coast is met regardless (UMN and LMN signs in the cervical region).

## Verification
Adversarial check, 23 October 2026. Read the log, the full `git diff` against HEAD (old and new case flattened field by field), the whole final case, the plan (sections 1-3 and 4 S07) and the notes file.
- All 9 note ids are in the table and each FIXED claim holds in the file: motor NCS with CMAPs, velocities and no conduction block (fe18f6ef, 2666c318); escitalopram "no clinically significant interaction", no serotonergic or serotonin-syndrome claim (7949f4b4); anxiety red herring with the reviewer's wording and PROHIB-FUNC (c66738c7); respiratory normal against the women's SNIP limit 60; five-gene panel; familial ALS low; AMX0035 gone. No DECLINED or BLOCKED notes.
- Checked: no Kennedy entry in a woman; female reference ranges in the labs; CK 580/170 = 3.4x; no bulbar must (tongue fasciculations only, "No dysarthria yet"); exam `additional` and HPI synthesis removed; no banned text.
- Found and fixed (B, minor; same class as S01/S02): MUST-DX and K-GC claimed LMN involvement in the bulbar, cervical, thoracic and lumbosacral regions, but chronic neurogenic change is reported only in the hand muscles and tibialis anterior; the tongue and thoracic paraspinals show active denervation only. Both now state LMN involvement in the cervical and lumbosacral regions with active denervation also in the tongue and thoracic paraspinal muscles. Gold Coast stays met (UMN and LMN signs in the cervical region).
- Noted for the lead, not changed: the canonical K-NCS pearl mentions SBMA in a woman (same point as S02, S04). British spellings in new text ("haemorrhage") next to "hemorrhage" in the MRI report; cosmetic.
- `perfect_agent.py` -v ok after the change (brain MRI, spine MRI and labs are served from the initial work-up); `case_io.py check` clean for the case (schema, synonym guard; the one failing test in the suite does not name it).

## Condition audit (ALS lead, 23 Oct 2026)
- `ground_truth.key_clinical_evidence[2]` (K-NCS): "or SBMA" removed. SBMA is X-linked and affects men; the plan's C8 already drops the Kennedy entry in women, so the pearl named a mimic that cannot apply (flagged by the S02, S04, S07 and S09 verifiers as a class).
- `followup_outputs[0].output.findings[*].is_abnormal` added (rows carried no abnormality marker), set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.
