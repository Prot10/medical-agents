# PD — NeuroBench v5 audit

24 PD cases audited (M01–M05, P01–P04, RM01–RM05, RP01–RP05, RS01–RS05, S01–S06) plus 1 dataset-level (CONFIG) and 1 cohort-level (PACK) finding. 100 findings total: 0 blocker, 27 major, 44 minor, 29 nit. 18 fixed / 82 flagged. Validators: `validators_ok: false` (residual coherence issues remain, all flagged for human/systemic adjudication, none auto-fixable).

## Terminology / taxonomy

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| PD-M01 | terminology | minor | ground_truth.differential[metoclopramide DIP].icd_code | Metoclopramide-induced parkinsonism coded G21.11 (neuroleptic-induced); metoclopramide is not a neuroleptic | FIXED | Changed G21.11 → G21.19 |
| PD-M02 | terminology | minor | ground_truth.differential[metoclopramide DIP].icd_code | Same as PD-M01 | FIXED | Changed G21.11 → G21.19 |
| PD-M03 | terminology | minor | ground_truth.differential[metoclopramide DIP].icd_code | Same as PD-M01 | FIXED | Changed G21.11 → G21.19 |
| PD-RS04 | terminology | minor | ground_truth.differential[metoclopramide DIP].icd_code | Same as PD-M01 | FIXED | Changed G21.11 → G21.19 |
| CONFIG | terminology | minor | conditions.yaml parkinsons.icd_code + all 24 PD case ground_truth.icd_code | Canonical PD code G20 is a non-billable FY2025 parent header; billable children are G20.A1/A2/B1/B2/C, unlike dataset's use of specific children elsewhere (e.g. G30.0) | FLAGGED | Decide benchmark-wide convention: keep G20 as family identifier or adopt children per documented dyskinesia/fluctuation status (needs config change, out of scope here) |
| PD-M05 | terminology | nit | ground_truth.differential[DIP].icd_code | Generic ruled-out DIP differential coded G21.11 (neuroleptic) though no neuroleptic documented; 5 sibling cases use G21.19 for identical entry | FLAGGED | Consider G21.11 → G21.19 for consistency |
| PD-P04 | terminology | nit | ground_truth.differential[DIP].icd_code | Same generic-DIP G21.11-vs-G21.19 inconsistency as PD-M05 | FLAGGED | Consider G21.11 → G21.19 for consistency |
| PD-RP05 | terminology | nit | ground_truth.differential[DIP].icd_code | Same generic-DIP G21.11-vs-G21.19 inconsistency as PD-M05 | FLAGGED | Consider G21.11 → G21.19 for consistency |
| PD-P04 | terminology | nit | ground_truth.primary_diagnosis | "Young-onset Parkinson's disease" at age 42 verified CORRECT against MDS EOPD/YOPD <50 cutoff (Mehanna 2022); no change needed | FLAGGED (no action) | None — label is terminologically and demographically correct |

## Audit findings

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| PD-M01 | E | minor | followup_outputs[2].output autonomic tilt value/quantitative_data | Duplicated unit: "18 mmHg at 3 minutes mmHg" | FIXED | Removed trailing "mmHg" |
| PD-M03 | E | minor | followup_outputs[4].output (PSG) TST/REM Latency value+quantitative_data+impression | Duplicated "minutes minutes" | FIXED | Collapsed to single "minutes" |
| PD-M02 | B | major | followup_outputs[1].output panels['Levodopa Challenge Test'][1].is_abnormal | Post-levodopa UPDRS-III 18 flagged abnormal(H) despite own 0-132 range | FIXED | Set is_abnormal=false, updated interpretation/summary |
| PD-M01 | B | major | followup_outputs[1].output panels.Levodopa_Challenge_Test | Improvement % 36% inconsistent with baseline 27/post 19 (true 29.6%, flips >30% threshold) | FLAGGED | Reconcile post-levodopa score or accept borderline/negative response |
| PD-M02 | B | major | followup_outputs[1].output panels['Levodopa Challenge Test'] | Improvement % 35.7% inconsistent with baseline 25/post 18 (true 28%, flips threshold) | FLAGGED | Reconcile scores/percentage |
| PD-M03 | B | minor | followup_outputs[4].output (PSG) impression | TST 342min and Sleep Efficiency 78% below-range tagged (H) not (L) | FLAGGED | Correct direction tags to (L) |
| PD-M01 | B | minor | followup_outputs[2]/[4] impression (autonomic/PSG) | HR-tilt 8bpm and Sleep Efficiency 72% below-range tagged (H) not (L) | FLAGGED | Fix direction tags |
| PD-M01 | B | minor | neurological_exam.mental_status vs followup_outputs[3] (neuropsych) | MoCA 25/30 (exam) vs 23/30 (battery), unexplained 2-pt drop | FLAGGED | Confirm intended MoCA / align |
| PD-M02 | C | minor | initial_tool_outputs.labs.panels.BMP (Sodium) | Sodium 153 mEq/L implausible as asymptomatic incidental finding | FLAGGED | Consider softening to 146-148 |
| PD-M01 | C | minor | ground_truth.key_reasoning_points[0] & differential[0].key_features | "Symmetric onset" reasoning contradicts case's explicitly asymmetric exam/DaTscan | FLAGGED | Reword to reflect asymmetry as PD-supportive |
| PD-P01 | C | major | followup_outputs[1].output.panels.Levodopa_Challenge (Percent improvement) | 17.6% contradicts baseline 31/post 26 (true 16.1%) | FIXED | Corrected 17.6% → 16.1% in value, interpretation, summary |
| PD-P01 | B | major | ground_truth.red_herrings[0] and differential[4] (DIP) | References metoclopramide exposure not present in HPI (which explicitly denies it) | FLAGGED | Author adjudication: reword red herring/DDx or add exposure to HPI |
| PD-P01 | E | minor | followup_outputs[4].output.impression (PSG) | Sleep efficiency 72% tagged (H) not (L) | FIXED | Corrected (H) → (L) |
| PD-P01 | E | minor | followup_outputs[3].output.impression (neuropsych) | CVLT-3 -1.2 and Stroop -1.9 z-scores tagged (H) not (L) | FLAGGED | Change both to (L) if regenerating; low priority |
| PD-P01 | C | minor | labs.panels.Additional (catecholamines) vs followup_outputs[5] (MIBG) | Low supine NE + preserved MIBG is a postganglionic/preganglionic mismatch | FLAGGED | Consider normalizing supine NE or leave as intentional overlap |
| PD-P01 | B | nit | ground_truth.differential[].icd_code | No icd_code fields, unlike PD-M04/M05 | FLAGGED | Optionally add icd_code for cross-case consistency |
| PD-P01 | A | minor | case_id / ground_truth.primary_diagnosis | PD- prefix but diagnosis is MSA-P; intentional mimic, already documented | FLAGGED (no action) | Leave as-is; pack citation gap is a PACK issue |
| PD-M05 | B | major | ground_truth.red_herrings[0].field_path | Compound unresolvable path "patient.neurological_exam.motor and initial_tool_outputs.specialized_test" | FIXED | Set to single resolvable path patient.neurological_exam.motor |
| PD-M05 | B | major | ground_truth.useless_tools (order_advanced_imaging) / fallback_tool_outputs.advanced_imaging | useless_tools lists amyloid_PET but fallback is null (systemic, shared with M04) | FLAGGED | Add neutral advanced_imaging fallback or fix validator keying |
| PD-M05 | B | minor | mental_status vs followup_outputs[1] (MoCA) | MoCA 27/30 (exam) vs 26/30 (battery) | FLAGGED | Consider harmonizing single MoCA score |
| PD-M04 | B | major | ground_truth.useless_tools (order_advanced_imaging) / fallback_tool_outputs.advanced_imaging | Same coherence gap as PD-M05 | FLAGGED | Same structural fix as PD-M05 |
| PD-M04 | C | minor | ground_truth.differential[5] (Enhanced physiologic tremor) | Coded G25.1 (drug-induced tremor); mechanism is anxiety/withdrawal, not drug-induced | FLAGGED | Consider G25.2/R25.1; borderline nuance |
| PD-M04 | E | nit | followup_outputs[1].output.interpretation (levodopa via interpret_labs) | Positive 41.7% response templated as "All values within normal limits" | FLAGGED | Optionally replace with neutral factual recital |
| PD-P03 | B | major | followup_outputs[4].output (tau-PET) tracer_or_protocol vs findings[0].signal | Named Flortaucipir/AV-1451 but signal names 18F-PI-2620 (correct validated 4R tracer) | FIXED | Changed tracer_or_protocol to 18F-PI-2620 PET |
| PD-P02 | B | minor | followup_outputs[1].output.impression (PSG) | Sleep efficiency 68% and REM% 16% tagged (H) not (L) | FLAGGED | Correct (H)→(L), ideally generator-wide |
| PD-P02 | B | minor | followup_outputs[3].output.impression (neuropsych) | Clock Drawing 4/10, JoLO 12/30, Rey Copy 3rd %ile tagged (H) not (L) | FLAGGED | Correct (H)→(L), generator-wide |
| PD-P03 | B | minor | followup_outputs[2].output.impression (neuropsych) | FAB 8/18 tagged (H) not (L) | FLAGGED | Correct (H)→(L) |
| PD-P04 | D | minor | followup_outputs[0].output.findings[0].signal (DaTscan) | Labeled "putamen-to-caudate ratio" with normal ">2.0" but values are SBRs | FLAGGED | Relabel as specific binding ratio (SBR) |
| PD-P02 | D | nit | followup_outputs[4].output.findings[0].signal (FDG-PET) | Signal calls pattern "classic DLB metabolic pattern", stronger than hedged style-guide phrasing | FLAGGED | Optionally soften wording |
| PACK | C | major | PD-P02/PD-P03 primary_diagnosis + citation + criteria_packs/PD.md | DLB and PSP-RS filed under PD- prefix cite only PD-pack references; McKeith/Hoglinger absent from allow-list | FLAGGED | Adjudicate cohort placement or extend pack (do not edit conditions.yaml/PD.md concurrently) |
| PD-P04 | A | minor | metadata.vocab_gap / TOOL_PARAMETER_VOCABULARY.md | No genetic_panel vocab entry for PD monogenic panel (PRKN/PINK1/GBA/LRRK2 etc.) | FLAGGED | Add PD/monogenic_PD genetic_panel suffix (shared file) |
| PD-P02 | E | nit | initial_tool_outputs.eeg/mri.impression (also PD-P03 eeg) | Several impressions lack terminal period | FLAGGED | Add trailing periods; cosmetic |
| PD-RM02 | B | major | followup_outputs[0].output findings[0].signal/impression (DaTscan) | Left-body-predominant exam but DaTscan shows LEFT putamen worst (should be RIGHT, contralateral rule) | FLAGGED | Swap putaminal ratios/laterality text |
| PD-RM03 | B | major | followup_outputs[0].output findings[0].signal/impression (DaTscan) | Right-body-predominant exam but DaTscan shows RIGHT putamen worst (should be LEFT) | FLAGGED | Swap putaminal ratios/laterality text |
| PD-RM02 | C | minor | ground_truth.differential | Prominent prior encephalitis + literature on postencephalitic parkinsonism, but PEP absent from differential | FLAGGED | Consider adding PEP as low-likelihood differential |
| PD-RM03 | B | minor | mental_status vs followup_outputs[4] (MoCA) | MoCA 26/30 (exam) vs 25/30 (battery, flagged abnormal); would flip abnormal flag | FLAGGED | Reconcile to single value |
| PD-RM03 | C | minor | neurological_exam.motor + mri.findings | Right FDI wasting attributed to C5-C6 spondylosis but FDI is C8-T1 myotome | FLAGGED | Move spondylotic level or soften attribution (deliberate ALS red herring) |
| CONFIG | E | nit | followup_outputs[].output.findings[] (tilt-table BP-drop, RM01-03) | Duplicated trailing "mmHg" unit, systemic beyond these 3 cases | FLAGGED | Global sweep to strip redundant unit |
| PD-RM01 | D | nit | followup_outputs[3]/[6].output.summary | Leakage detector flagged "Parkinson's disease" in population-keyed literature summaries | FLAGGED (no action) | Not a leak; intentional, allowed by style guide |
| PD-RP01 | B | major | followup_outputs[7].output.rhythm_summary and .impression | Narrative said "48-hour" while structured duration_hours=24/monitor_type=holter_24h and gold action agree on 24h | FIXED | Changed narrative "48-hour" → "24-hour" (both occurrences) |
| PD-RP01 | B | minor | followup_outputs[7].output.heart_rate_range.max vs narrative | Structured max=118 vs narrative "52-98 bpm" (twice) | FLAGGED | Reconcile max HR value |
| PD-RP01 | C | major | ground_truth.primary_diagnosis | Multiple MSA-P red flags (early severe dysautonomia, symmetric no-tremor parkinsonism, poor 36% levodopa response, putaminal MRI rim) against PD-primary label | FLAGGED | Clinician confirm PD-primary label defensible over MSA-P |
| PD-RP01 | C | minor | initial_tool_outputs.mri.findings[0] | Putaminal rim sign / atrophy (MSA imaging feature) present though PD MRI expected normal | FLAGGED | Reviewer awareness item tied to PD-vs-MSA question |
| PD-RP01 | B | nit | followup_outputs[4].output.findings (HVLT-R Delayed Recall) | Value 7/12 marked abnormal='no' despite reference ">7" (7 is not >7) | FLAGGED | Confirm intended cutoff |
| PD-RP01 | D | nit | followup_outputs[5].output.summary | Leakage flag on population-keyed literature sentence | FLAGGED (no action) | Not a leak; style-guide-permitted |
| PD-RM04 | A | major | ground_truth.useless_tools (order_advanced_imaging) / fallback_tool_outputs.advanced_imaging | Same coherence gap, systemic across ~7 PD cases | FLAGGED | Orchestrator-level fallback template or validator relaxation |
| PD-RM04 | D | nit | followup_outputs[4].output.results[0].key_finding | Leakage flag on population-keyed epidemiology sentence | FLAGGED (no action) | Not a leak |
| PD-RM04 | D | nit | followup_outputs[0].output.findings[0].region (DaTscan) | Region text parenthetically references exam laterality; borderline style-guide violation | FLAGGED | Optional: trim exam parenthetical |
| PD-RM05 | B | nit | initial_tool_outputs.labs.abnormal_values_summary[0] | Lists free T4 0.9 (within range) alongside abnormal TSH; out of scope for abnormal-values field | FLAGGED | Optionally drop free-T4 clause |
| PD-RP02 | E | minor | followup_outputs[4].output (PSG) value/quantitative_data/impression | Duplicated "342 minutes minutes" | FIXED | Normalized to "342 minutes" |
| PD-RP02 | B | major | ground_truth.red_herrings[0] and differential[3] | References metoclopramide mention absent from (denying) HPI | FLAGGED | Reconcile red herring/DDx wording or HPI |
| PD-RP02 | C | major | ground_truth.primary_diagnosis | Nearly all data (symmetric onset, 15.8% levodopa response, symmetric DaTscan, MRI putaminal rim/SWI iron, severe early autonomic failure) favors MSA-P over stated PD label; only MIBG favors PD | FLAGGED | Confirm with movement-disorders reviewer intentional puzzle balance |
| PD-RP02 | B | nit | followup_outputs[3].output.impression (neuropsych) | Clock Drawing 8/10 tagged (H) though below 9-10 normal range | FLAGGED | Low-value generator quirk; flag only |
| PD-RP03 | A | major | case_id vs primary_diagnosis/icd_code | PD- prefix, condition=parkinsons, but diagnosis MSA-P/C; intentional mimic, already documented | FLAGGED (no action) | No case-file fix; pack extension is a CONFIG matter |
| PD-RP04 | B | major | ground_truth.useless_tools (order_advanced_imaging) vs fallback_tool_outputs.advanced_imaging | Same coherence gap | FLAGGED | Add negative fallback or drop useless_tools entries |
| PD-RP04 | D | nit | followup_outputs[2].output.results[0].key_finding | Leakage flag on population-keyed DBS literature | FLAGGED (no action) | Not a leak; keep |
| PD-RS01 | B | major | followup_outputs[0].output (DaTscan) region/signal/quantitative_data/impression | Right-body-predominant exam but scan shows RIGHT putamen worst (ipsilateral, contradicts contralateral rule and gold expected_finding) | FLAGGED | Swap right/left throughout DaTscan followup |
| PD-RS01 | B | major | ground_truth.optimal_actions[2].tool_parameters.current_medications | Lists phantom acetaminophen, omits lithium (central red-herring drug) and metformin | FLAGGED | Replace with true regimen incl. lithium; remove acetaminophen |
| PD-RS01 | B | minor | initial_tool_outputs.mri.impression | Impression says "no white matter lesion" but findings list scattered T2/FLAIR hyperintensities | FLAGGED | Reword impression to acknowledge punctate WMH |
| PD-RP05 | B | major | mri.volumetrics.substantia_nigra_SWI + mri.impression pt4 + key_reasoning_points[4] + optimal_actions[0].expected_finding | Nigrosome-1 loss placed on left, but left-body-predominant exam + right-putamen-worst DaTscan implies RIGHT nigrosome loss (ipsilateral rule) | FLAGGED | Swap left/right for nigrosome-1 finding across all 4 fields |
| PD-RP05 | A | minor | ground_truth.useless_tools (amyloid_PET) + fallback_tool_outputs.advanced_imaging | Same systemic coherence gap (6 PD cases); not runtime-reachable per mock server tool_name-only matching | FLAGGED | Address at dataset level: exempt or add uniform fallback |
| PD-RP05 | B | nit | followup_outputs[0].output.findings[0].signal (asymmetry index) | Stated 42% but computed from SBRs is 38% | FLAGGED | Adjust to ~38% or clarify formula |
| PD-RP05 | B | nit | past_medical_history vs labs (eGFR) | PMH says CKD stage 2 but eGFR 54 corresponds to stage 3a | FLAGGED | Reconcile PMH label with eGFR |
| PD-RP05 | C | nit | ground_truth.differential[1].icd_code | DIP coded G21.11 while sibling PD-RS01 codes same generic entry G21.19 | FLAGGED | Standardize generic DIP code across PD cases |
| PD-RP05 | D | nit | followup_outputs[1].output.results[3].key_finding | Leakage flag on population-keyed swallow-tail literature | FLAGGED (no action) | Not a leak; intentional |
| PD-RS02 | E | minor | followup_outputs (PSG/autonomic/neuropsych) value/quantitative_data/impression | Duplicated units ("355 minutes minutes", "14 bpm variation bpm", "T-score 50/47/42 T-score") + wrong (H)/(L) flags on TST/sleep efficiency | FIXED | Removed duplicated units; corrected 2 direction flags to (L) |
| PD-RS02 | A | nit | ground_truth.differential[].icd_code | Most entries omit icd_code, unlike siblings PD-RS01/PD-RP05 | FLAGGED | Populate icd_codes for consistency |
| PD-RS02 | E | nit | metadata.difficulty vs difficulty_description | difficulty=moderate but description opens "Straightforward case..." (leftover copy) | FLAGGED | Update description wording |
| PD-RS03 | C | major | ground_truth.differential / neurological_exam / followup_outputs[2] | Multiple atypical-parkinsonism red flags (severe early dysautonomia, wide-based gait, early falls, Pisa syndrome, MoCA 22) yet MSA rated very_low with contradicting rationale | FLAGGED | Clinician review of PD-vs-MSA label; correct MSA key_features |
| PD-RS03 | B | minor | followup_outputs[5] (search_parkinsons_self_mutilation) | Orphaned literature search on self-injurious behavior with no anchor in HPI (vestige of source case) | FLAGGED | Remove/replace with relevant literature search |
| PD-RS03 | C | minor | ground_truth.differential[0] | Vascular parkinsonism ranked "moderate" despite its own key_features and MRI arguing against it | FLAGGED | Reconsider likelihood ranking |
| PD-RS03 | B | nit | patient.clinical_history.past_medical_history | Fluoxetine indication "Depression" but Depression absent from PMH (lists Insomnia instead) | FLAGGED | Add Depression to PMH or reconcile indication |
| PD-RS04 | B | major | ground_truth.red_herrings[0] / differential[1] / metadata.difficulty_rationale | All assert metoclopramide exposure "mentioned in history" though HPI explicitly denies it | FLAGGED | Add documented exposure to HPI or delete red herring/differential/rationale |
| PD-RS04 | B | minor | ground_truth.differential[1] and [2] | "Drug-induced parkinsonism" duplicated with contradictory rationales | FLAGGED | Collapse to single consistent DIP entry |
| PD-RS04 | B | minor | neurological_exam.mental_status | MoCA 24/30 stated but enumerated deductions sum to only 4 (implies 26/30) | FLAGGED | Add missing deduction items or reword as non-exhaustive |
| PD-RS04 | E | minor | patient.history_present_illness | "Progressive vertigo" used repeatedly; true vertigo not a PD feature and absent from chief_complaint | FLAGGED | Replace "vertigo" with "dizziness/unsteadiness" |
| PD-RS04 | D | minor | followup_outputs[6] (search_parkinsons_disease_self_mutilation) | Same orphaned self-mutilation literature search as PD-RS03 | FLAGGED | Remove/replace with workup-relevant search |
| PD-RS05 | C | minor | initial_tool_outputs.mri.findings[0].signal_characteristics.SWI | Bilaterally preserved swallow-tail sign in idiopathic PD case, mildly counter-realistic given abnormal DaTscan | FLAGGED | Consider softening to equivocal/partial loss on affected side |
| PD-S02 | C | major | followup_outputs[0].output (DaTscan) region/signal/impression | Right-body-affected patient but DaTscan reported worse reduction on the RIGHT (should be LEFT, contralateral rule); siblings PD-S01/S03 correct | FIXED | Flipped region/signal/impression to left-predominant |
| PD-S02 | B | minor | followup_outputs[1].output.panels.Levodopa_Challenge_Test[Percent Improvement] | 46% doesn't match baseline 27/post 13 (true 51.9%) | FIXED | Corrected 46 → 52 |
| PD-S03 | B | minor | followup_outputs[1].output.panels.Levodopa_Challenge_Test[Percentage Improvement] | 50% contradicts panel's own interpretation/summary of 55% (31→14) | FIXED | Corrected '50%' → '55%' |
| PD-S01 | B | major | ground_truth.optimal_actions[6].expected_finding vs followup_outputs[4] (PSG) | expected_finding says RSWA "absent here" but PSG reports RSWA present in 45% of REM epochs; HPI also denies dream enactment | FLAGGED | Reconcile: reduce PSG RSWA or reword expected_finding |
| PD-S02 | D | nit | followup_outputs[4].output (PSG) vs history_present_illness | HPI denies dream enactment but PSG reports RSWA present; clinically defensible (subclinical), unlike PD-S01 | FLAGGED (no action) | No change required |
| PD-S03 | B | minor | followup_outputs[1].output.panels.Levodopa_Challenge_Test[*].is_abnormal | is_abnormal flags used interpretively (post 14=true, pre 31=false) rather than by range | FLAGGED | Consider is_abnormal=false for scale rows or add clinical_significance field |
| PD-S01 | B | nit | followup_outputs[1].output.panels.Levodopa_Challenge_Test[Percent Improvement] | "50%" loosely rounds true 51.6% (31→15); no contradicting statement | FLAGGED | Optionally tighten to 52% |
| PD-S04 | B | minor | followup_outputs[1].output.panels.Levodopa_Challenge_Test[2].value | 50% vs computed 51.9% (27→13) | FIXED | Corrected to 52% |
| PD-S04 | C | nit | followup_outputs[3].output.findings (FSIQ/VCI) | Above-average scores (111, 116) flagged abnormal='yes' (H), clinically misleading | FLAGGED | Consider only flagging low-side deviations |
| PD-S05 | D | nit | followup_outputs[4].output.results[1].summary | Leakage flag on population-keyed PD-medication literature | FLAGGED (no action) | Not a leak; intentional |
| PD-S05 | B | minor | followup_outputs[3].output.findings[0] (Total Sleep Time) | TST 358min flagged abnormal='no' despite reference "360-480" (358 is below range) | FLAGGED | Adjudicate: flip flag or nudge value ≥360 |
| PD-S06 | A | major | ground_truth.useless_tools[5] (amyloid_PET) + fallback_tool_outputs.advanced_imaging | Same systemic coherence gap across 6 PD cases; not runtime-reachable per mock server matching order | FLAGGED | Orchestrator-level uniform fix (add fallback or drop useless entry) |
| PD-S06 | B | minor | ground_truth.optimal_actions[6].expected_finding | Asserts husband reported nocturnal movements though HPI denies dream enactment and PSG shows none observed | FLAGGED | Reword expected_finding to remove unsupported clause |

## Tally

- Cases audited: 24 PD cases (+ CONFIG, PACK cross-cutting items)
- Findings by severity: 0 blocker / 27 major / 44 minor / 29 nit (100 total)
- Fixed vs flagged: 18 fixed / 82 flagged
- Validators: `validators_ok: false` — all residual coherence/schema issues are systemic (advanced_imaging fallback gaps shared across 6+ cases) or require clinical judgment; none are unambiguous mechanical fixes.
