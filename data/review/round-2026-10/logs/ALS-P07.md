# ALS-P07
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 1138cdf4-aac3-47e3-a816-394f28b496bd | FIXED | Action criteria reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole (`ground_truth.action_criteria`, `followup_outputs`, `ground_truth.sequence_constraints`). The EMG now compares the new findings with the prior polio distribution and prior EMG (see bb7e1af1). |
| bb7e1af1-6266-447b-bf14-3d635136fd5f | FIXED | Literature follow-up `search_als_post_polio_differential` deleted. `initial_tool_outputs.specialized_test.findings` gains a "Comparison" row (EMG 8 years ago: changes confined to the left leg) and the impression states that denervation now extends beyond the left leg to bulbar, cervical, thoracic and right lumbosacral segments; EMG criterion `expected_evidence` names the new denervation outside the polio-affected limb. |
| 6e3e812d-59a1-429b-bde4-4469864fa78d | FIXED | `ground_truth.differential[0]` "Post-polio syndrome alone" high -> low with the note's reasoning (new bulbar involvement, UMN signs, faster progression, denervation outside the polio distribution). |
| eb171932-ffd7-4d83-948f-2d56c07ef471 | FIXED | "Chronic spinal cord signal change at L3-S1" removed. `initial_tool_outputs.body_imaging` now places the old polio change in the cord where it is (lumbar enlargement and conus, T11-L1) and in the cauda equina ventral roots at L3-S1; `region` = "cervical, thoracic and lumbosacral spine". |
| 83e32792-5000-491c-9a9f-d05801feee44 | FIXED | Riluzole check is the last follow-up and last criterion (recommended), with a soft constraint EMG before it. |
| aaf06f54-0c97-4659-924a-c0b89f8b1e9d | FIXED | Respiratory criterion recommended, staging text, after the diagnostic core; impression "Reduced FVC (72% predicted) and SNIP (52 cmH2O), indicating inspiratory muscle weakness."; MUST-RESP reduced (respiratory/NIV referral now) and PROHIB-RESP reduced added. |
| a9be1de4-3f9e-4863-8c69-5c0e5123bbc7 | FIXED | The literature output carrying the note was deleted; AMX0035 also removed from the interaction output (`followup_outputs[2].output.alternatives` = []). |
| 827a1fee-11ff-4d2d-b00e-78a55c3ab5ba | FIXED | Genetic panel criterion optional, after counselling, with a soft constraint EMG before genetics; follow-up second in the post-diagnostic list; output reports all five genes with the canonical negative impression. |
| 03220c38-efa5-4017-82f7-5e2b0db68e59 | FIXED | Same as 1138cdf4 (pathway) and eb171932 (cauda equina anatomy). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | patient.chief_complaint | Chief complaint named the diagnosis ("new ALS superimposed on post-polio syndrome") | FIXED: "Worsening weakness over 8 months, spreading beyond the leg affected by childhood polio" |
| B | major | patient.history_present_illness | PPS at age 53 described with "mild new bilateral arm fatigue, and widespread muscle fasciculations", which contradicts the EMG (arms, tongue, thoracic and right leg normal on the earlier study) and the 8-month history of new disease | FIXED: PPS described as new fatigue and slowly progressive left leg weakness; earlier EMG changes located in the left leg |
| D | minor | patient.neurological_exam.additional | Synthesis stating the discriminator ("new UMN signs and new LMN findings beyond the distribution of her original polio") | FIXED: findings only (fasciculation sites) |
| B | major | initial_tool_outputs.body_imaging | Brain content in the spine report ("NEW bilateral corticospinal tract changes above spinal level"); impression numbered from "2."; `region` cervical and thoracic while lumbar levels were described | FIXED: spine-only report, numbered from 1, region includes lumbosacral, lumbar canal and roots reported (right foot drop) |
| B | minor | initial_tool_outputs.mri.impression | Numbering "1 ... 3."; imaging differential ending in "other primary motor pathway pathology" | FIXED: numbered 1-2, comparison with the MRI of 5 years ago kept, non-specific wording |
| A/B | major | initial_tool_outputs.specialized_test | No motor NCS (conduction block not assessable); impression claimed positive sharp waves and chronic reinnervation in bulbar and thoracic regions that the findings did not contain; "Pulmonary function testing recommended." | FIXED: motor NCS row added (reduced CMAPs in wasted muscles, normal velocities, no block), impression restated from the findings, hint removed |
| B/C | major | initial_tool_outputs.labs | "Exclusion studies" with free T4 as a string; no CBC or metabolic panel; interpretation named ALS | FIXED: canonical panels, numeric values; sodium 137 and potassium 3.8 chosen for a patient on hydrochlorothiazide |
| B | minor | followup_outputs (respiratory, genetics) | SNIP reference ">70 cmH2O women"; bare "Abnormal values:" impression; genetics C9orf72 and SOD1 only with "All values within normal limits" | FIXED: canonical references and impressions; five genes |
| C | major | ground_truth.assessment | Diagnostic musts, generic lab must, irrelevant cervical-surgery and functional prohibitions; no swallowing or speech must despite new tongue atrophy | FIXED: rebuilt per C10 (MUST-DX, MUST-RESP reduced, MUST-BULBAR signs, MUST-RILUZOLE, MUST-MDT, MUST-GEN; PROHIB-IMM, PROHIB-RESP reduced) |
| C | minor | ground_truth.assessment.prohibited_recommendations | The case's central trap (anchoring on PPS) had no prohibition | FIXED: added "Do not attribute the new bulbar, upper motor neuron and right-sided findings to post-polio syndrome and continue energy conservation alone." (not in the plan; see Open questions) |
| E | minor | ground_truth.key_clinical_evidence | Engineering pearl, generic CK and El Escorial pearls, spondylosis pearl without spondylosis on imaging | FIXED: rebuilt per C14 plus a PPS pearl |
| A | minor | ground_truth.action_criteria | Brain MRI required `contrast: true`; free-text citations; label = rationale | FIXED: per C16 |
| A | minor | ground_truth.red_herrings[0].field_path | Pointed to the whole history list | FIXED: `patient.clinical_history.past_medical_history[0]` |
| B | minor | initial_tool_outputs.labs | ESR 8, CRP 2, B12 420, folate 10 identical to ALS-P05 and P06 (template carry-over) | FLAGGED: stored values kept per plan |
| E | minor | metadata.difficulty_rationale | "literature support needed" | FIXED: reworded |

## Changes, in one paragraph a physician can read before re-reviewing
The chief complaint no longer names ALS, and the HPI no longer gives her post-polio syndrome arm symptoms and widespread fasciculations 8 years ago (they contradicted the earlier EMG). The work-up reads EMG/NCS, brain MRI, spine MRI and blood tests first, then respiratory function (recommended), the genetic panel (optional) and the riluzole check (recommended); the literature search is gone. The EMG now compares with the EMG of 8 years ago and states that denervation has spread beyond the left leg to the tongue, cervical, thoracic and right leg muscles, with motor conduction studies showing no block and normal sensory studies. The spine MRI places the old polio change in the lumbar enlargement and conus with thin ventral roots of the cauda equina (no "cord at L3-S1"), and excludes compression in the cervical, thoracic and lumbar spine; the brain MRI shows only new, non-specific corticospinal tract signal. Respiratory function is reduced (FVC 72%, SNIP 52 cmH2O in a woman), so the musts include respiratory/NIV referral now, a speech and swallowing assessment for the new tongue atrophy, riluzole with LFT monitoring, MDT and genetic counselling. Post-polio syndrome alone is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- New citation keys used: `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]`.
- Review UI: show the initial work-up and follow-ups in criterion order.

## Open questions for Andrea (judgment calls you could not settle)
- The plan proposed "chronic signal change in the cauda equina roots at L3-S1". I wrote instead "mild left-predominant atrophy of the lumbar enlargement and conus (T11-L1) with thin left ventral roots of the cauda equina": old poliomyelitis destroys anterior horn cells, so the lasting MRI change is cord (anterior horn) atrophy at the lumbar enlargement and thin ventral roots, not root signal change. Both versions satisfy the reviewers' anatomical correction.
- I added a PPS-anchoring prohibition (not in the plan). Keep or drop.
- The EMG "Comparison" row describes the earlier EMG as confined to the left leg; the HPI already said the earlier EMG showed chronic polio changes with new active changes, and the old report said the other regions "were not documented as affected". Confirm that this reading of the earlier study is acceptable.

## Verification
Adversarial re-read of the whole final case against `git show HEAD`, the plan (section 4 P07) and the nine R1 notes (all ids present).
- Notes: pathway and literature (1138cdf4, 03220c38, 83e32792, aaf06f54, 827a1fee, a9be1de4): confirmed. bb7e1af1: the EMG carries a comparison with the EMG of 8 years ago (left leg only) and the criterion's expected evidence names new denervation outside the polio limb. 6e3e812d: PPS alone low. eb171932: no "cord at L3-S1"; the old change is placed in the lumbar enlargement and conus (T11-L1) and in the cauda equina ventral roots at L3-S1, which is anatomically correct (the worker's wording differs from the plan's suggestion but satisfies the ruling and is the better description of old anterior horn cell loss).
- Cross-field: right Babinski and right foot drop agree across exam, EMG (new right tibialis anterior denervation), MUST-DX and differential; timeline polio age 8, PPS at 53 = 8 years ago = earlier EMG; CK 820/170 = 4.8x; respiratory reduced (FVC 72, SNIP 52, women limit 60) with MUST-RESP and PROHIB-RESP reduced; tongue atrophy without dysphagia gives the speech and swallowing must (plan "signs without dysphagia"); spine `region` now includes lumbosacral levels. "This was confirmed by EMG" in the HPI was already at HEAD (left, no churn).
- Found: nothing to change.
- Checks run after verification: `perfect_agent.py -v` ok (every required and recommended criterion answered by the case's own data; the "<- ?" source marker for brain MRI, spine MRI and labs is the same in every ALS case and is not a fallback), `case_io.py check` schema OK, synonym guard OK, no test failure names the case. Grep for AMX0035, Relyvrio, edaravone, grapefruit, serotonergic, "July 2026", El Escorial, "Exclusion studies", "Reviewer baseline" and JSON dumps: none in the case (QTc appears only in the fallback ECG). No new em or en dash in the diff. Citations are bracketed allow-list keys only. Lab `is_abnormal` flags agree with every numeric reference range; ESR 8, CRP 2, B12 420 and folate 10 were already identical at HEAD in P05-P09 and RM11 (kept per plan C13, flagged by the worker).

## Condition audit (ALS lead, 23 Oct 2026)
- `ground_truth.key_clinical_evidence[2]` (K-NCS): "or SBMA" removed. SBMA is X-linked and affects men; the plan's C8 already drops the Kennedy entry in women, so the pearl named a mimic that cannot apply (flagged by the S02, S04, S07 and S09 verifiers as a class).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but thoracic paraspinals (T6-T8) show fibrillations only. Regions now: bulbar (new tongue atrophy), cervical and right lumbosacral (new fibrillations with large MUPs) beyond the old polio distribution, with active denervation also in thoracic paraspinal muscles. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
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
