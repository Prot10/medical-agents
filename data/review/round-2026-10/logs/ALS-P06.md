# ALS-P06
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 5c89246b-87bf-4f24-a00c-29be0629f99a | FIXED | Action criteria reordered (EMG, brain MRI, spine MRI, labs with the paraprotein tests first, then optional CSF); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole (`ground_truth.action_criteria`, `followup_outputs`, `ground_truth.sequence_constraints`). |
| 59b49bd2-7c68-4e1d-bd79-d935921b0faf | FIXED | Literature follow-up `search_mgus_als_association` deleted and the literature criterion removed; the paraprotein work-up is now in the required lab criterion (`SPEP`, `IFE`, `serum_free_light_chains`, `anti_MAG`) and reported in `initial_tool_outputs.labs`. |
| e6f29c98-29bf-4091-a96a-94a54b89e5f6 | FIXED | `ground_truth.differential`: MGUS-associated (anti-MAG) neuropathy moderate -> low with the note's reasoning (normal sensory exam and NCS, normal distal latencies and velocities, no block, UMN signs, multi-region denervation, antibodies negative); POEMS, Waldenstrom/Bing-Neel and lymphoma very_low. |
| 69cfac89-8f57-4bd5-ad99-d1684a82f666 | FIXED | "Anti-MAG and anti-GM1 antibodies are pending." deleted from `patient.history_present_illness`; `initial_tool_outputs.labs.panels["Anti-MAG and anti-GM1 antibodies"]` reports anti-MAG IgM 380 BTU (<1000) and anti-GM1 IgM <1:100, both negative. |
| bdc518b8-679f-454d-8f57-6a55af80c4dd | FIXED | Riluzole check is the last follow-up and last criterion, recommended, with a soft constraint EMG before it. |
| 72b81b92-5b22-4fa9-9bf2-0f633603a5ed | FIXED | Respiratory output: references FVC >=80% predicted and SNIP >=70 cmH2O (men); impression "FVC 80% predicted and SNIP 70 cmH2O are at the lower limit of normal."; must "repeat them within 3 months and ask about orthopnoea and sleep-related symptoms of hypoventilation" (MUST-RESP borderline). |
| f378b998-dfcb-4d06-a109-5cd3914f8055 | FIXED | AMX0035 removed (`followup_outputs[2].output.alternatives` = []); output rewritten (lisinopril: no interaction; SmPC monitoring). |
| e1da1f92-fbbf-45c4-b8b6-867da83a4544 | FIXED | Same pathway fix as 5c89246b. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | initial_tool_outputs.mri.impression | Brain MRI impression was the spine impression ("No myeloma-related cord compression or infiltration") | FIXED: brain-only report, post-gadolinium technique (lymphoproliferative question), numbered impression |
| C | minor | initial_tool_outputs.body_imaging | "Myeloma-related" template wording in an IgM (non-myeloma) gammopathy; no description of cord or canal | FIXED: plain findings (cord, canal, vertebral marrow), normal impression |
| B | minor | initial_tool_outputs.specialized_test.impression | Impression claimed positive sharp waves and chronic reinnervation in thoracic and lumbosacral regions; findings show chronic change only in cervical muscles; "Pulmonary function testing recommended." hint | FIXED: impression restated from the findings, nerves named in motor and sensory NCS, recommended_actions emptied |
| B/C | major | initial_tool_outputs.labs | Panel "Paraprotein_Panel" with the M-protein value as a string, row "TSH (POEMS endocrinopathy)", "Reviewer baseline rule-out additions", no CBC, metabolic panel, IFE, free light chains or anti-MAG although the criterion required free light chains; interpretation named ALS | FIXED: canonical panels, numeric values; CBC, CMP, free T4, immunofixation, free light chains (normal ratio) and anti-MAG added; random glucose 100 mg/dL agrees with the CSF/serum glucose ratio 0.64 |
| D | minor | patient.history_present_illness | "Examination shows combined upper and lower motor neuron signs" synthesis; M-protein value of a now-scored test | FIXED: synthesis deleted; paraprotein described as stable without the value; referral reason kept |
| A | minor | initial_tool_outputs.csf.interpretation | Python dict dumps and "CSF does not confirm ALS" | FIXED: factual pattern statement |
| B | minor | followup_outputs (genetics) | C9orf72 and SOD1 only; "All values within normal limits" | FIXED: five genes, canonical negative impression |
| C | major | ground_truth.assessment | Diagnostic musts, a generic lab must, prohibitions on cervical surgery (no spondylosis) and functional dismissal (no psychiatric history) | FIXED: rebuilt per C10 (MUST-DX, MUST-RESP borderline, MUST-RILUZOLE, MUST-MDT, MUST-GEN, MGUS surveillance; PROHIB-IMM, PROHIB-RESP) |
| C | minor | ground_truth.assessment.prohibited_recommendations | No prohibition against treating the incidental IgM paraprotein, the case's central trap | FIXED: added "Do not start rituximab or other immunotherapy directed at the IgM paraprotein..." (not in the plan; see Open questions) |
| C | minor | ground_truth.red_herrings[0] | "IgM MGUS prevalence ~3%" is wrong (about 3% is all-isotype MGUS over 50); field_path pointed to a panel that no longer exists | FIXED: corrected prevalence, path to the immunofixation row |
| C | minor | ground_truth.differential | "hematology consult appropriate" as a key feature; POEMS "no organomegaly, endocrinopathy or skin changes" not documented in the case | FIXED: key_features cite only case data |
| E | minor | ground_truth.key_clinical_evidence | Engineering pearl, generic CK and El Escorial pearls | FIXED: rebuilt per C14 plus an anti-MAG pearl |
| A | minor | ground_truth.action_criteria | Brain MRI required `contrast: true`; free-text citations; label = rationale | FIXED: per C16 |
| B | minor | initial_tool_outputs.labs | ESR 8, CRP 2, B12 420, folate 10 are identical to ALS-P05 (template carry-over) | FLAGGED: stored values kept per plan (keep every stored value) |
| E | minor | metadata.difficulty_rationale | "literature search needed; 5 required tools" | FIXED: reworded |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first (all required), then optional CSF cytology and flow cytometry for the lymphoproliferative question, then respiratory function (recommended), the genetic panel (optional) and the riluzole check (recommended); the literature search is gone. The HPI no longer says that antibodies are pending: the labs now report anti-MAG and anti-GM1 negative, together with immunofixation (IgM kappa 0.4 g/dL), a normal free light chain ratio, a full blood count and metabolic panel, thyroid function and CK 740 U/L (4.3x ULN). Brain and spine MRI are separate reports (brain: subtle corticospinal tract signal, no enhancement after gadolinium; spine: normal, normal marrow). The EMG impression matches its findings (cervical active and chronic denervation, thoracic and lumbosacral active denervation, normal distal latencies and velocities, no block, normal sensory studies). Respiratory values (FVC 80%, SNIP 70) are reported as at the lower limit of normal with a 3-month repeat. Musts: disclose ALS, respiratory follow-up, riluzole with LFT monitoring, MDT, genetic counselling, continued haematology surveillance of the MGUS; prohibitions: no immunotherapy for ALS or for the paraprotein, no stopping respiratory monitoring. The paraproteinaemic mimics are low or very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- New citation keys used: `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]`.
- Review UI: show the initial work-up and follow-ups in criterion order.

## Open questions for Andrea (judgment calls you could not settle)
- I added a prohibition not in the plan: "Do not start rituximab or other immunotherapy directed at the IgM paraprotein". Anti-MAG neuropathy is the treatable diagnosis the case tempts the agent towards; treating the paraprotein here would expose the patient to rituximab without indication. Keep or drop.
- CSF protein 52 mg/dL is kept as stored (mildly raised, compatible with ALS).

## Verification
Adversarial re-read of the whole final case against `git show HEAD`, the plan (section 4 P06) and the eight R1 notes (all ids present).
- Notes: pathway and literature (5c89246b, 59b49bd2, e1da1f92), riluzole placement and AMX0035 (bdc518b8, f378b998): confirmed in criteria and follow-ups. e6f29c98: MGUS neuropathy low with only case data. 69cfac89: "pending" sentence gone from the HPI and anti-MAG (380 BTU, <1000) and anti-GM1 (<1:100) reported in the labs; the lab criterion asks `SPEP`, `IFE`, `serum_free_light_chains`, `anti_MAG`, all costs.yaml terms. 72b81b92: FVC 80 and SNIP 70 (men) reported "at the lower limit of normal", `is_abnormal` false at the limit, MUST-RESP borderline wording.
- Cross-field: right Babinski in exam, MUST-DX and key evidence; CK 740/174 = 4.3x; free light chain ratio 18.5/14.2 = 1.30 inside 0.26-1.65; CSF glucose 64 with random serum glucose 100 gives 0.64; brain MRI post-gadolinium, spine non-contrast and neither claims what the other did; CSF criterion asks cytology and flow cytometry and the CSF output reports both. The M-protein value moved out of the HPI because SPEP is now scored: correct. The added rituximab prohibition is consistent with negative anti-MAG and anti-GM1 and conflicts with no must.
- Found: nothing to change. The PROHIB-RESP text "because the baseline values are normal" is the plan's canonical wording for both normal and borderline categories; left as is.
- Checks run after verification: `perfect_agent.py -v` ok (every required and recommended criterion answered by the case's own data; the "<- ?" source marker for brain MRI, spine MRI and labs is the same in every ALS case and is not a fallback), `case_io.py check` schema OK, synonym guard OK, no test failure names the case. Grep for AMX0035, Relyvrio, edaravone, grapefruit, serotonergic, "July 2026", El Escorial, "Exclusion studies", "Reviewer baseline" and JSON dumps: none in the case (QTc appears only in the fallback ECG). No new em or en dash in the diff. Citations are bracketed allow-list keys only. Lab `is_abnormal` flags agree with every numeric reference range; ESR 8, CRP 2, B12 420 and folate 10 were already identical at HEAD in P05-P09 and RM11 (kept per plan C13, flagged by the worker).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but thoracic paraspinals show fibrillations only, and tibialis anterior and vastus medialis show fibrillations and fasciculations without chronic change or wasting. Regions now: cervical, with active denervation also in thoracic and lumbosacral muscles. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
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
