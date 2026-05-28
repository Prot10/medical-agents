# NeuroBench v5 audit — NMDAR-ENC (anti-NMDAR / autoimmune encephalitis)

Scope: all 36 `NMDAR-ENC-*` cases. Method: per the `neurobench-case-audit` skill —
mechanical validators (coherence, leakage, schema, vocab) + exhaustive field-by-field
read of every region against the criteria pack (`NMDAR-ENC.md`) and the tool-report
style guide. Confirmatory anti-NMDAR titers, EEG "extreme delta brush", and hedged
MRI limbic-encephalitis reads are KEPT (not leakage). RP01 is the intentional
seronegative case (verified, flagged, not changed).

Mechanical baseline: all 36 cases pass coherence (0 issues), schema validation,
tool-vocab, and the leakage detector (0 candidates) before and after edits.

## Findings

| case_id | dim | severity | region.field | finding | action | detail |
|---|---|---|---|---|---|---|
| M04 | A/B | major | patient.neurological_exam | Sensory exam stored under non-schema key `sensation`; schema field `sensory` was empty `""`. Pydantic drops `sensation`, so the sensory exam was invisible to the agent/grader. | FIXED | Renamed `sensation`→`sensory` (same exam component, unambiguous). |
| M05 | A/B | major | patient.neurological_exam | Same `sensation`/`sensory` key bug. | FIXED | Renamed `sensation`→`sensory`. |
| M06 | A/B | major | patient.neurological_exam | Same `sensation`/`sensory` key bug. | FIXED | Renamed `sensation`→`sensory`. |
| M07 | A/B | major | patient.neurological_exam | Same `sensation`/`sensory` key bug, PLUS a non-schema `autonomic` key carrying critical dysautonomia (HR 48–140, BP cycling, diaphoresis, T 38.2) that was also being dropped. | FIXED | Renamed `sensation`→`sensory`; folded the dropped `autonomic` line into the schema `additional` field (prefixed "Autonomic:") so the dysautonomia is preserved. |
| M08 | A/B | major | patient.neurological_exam | Same `sensation`/`sensory` key bug. | FIXED | Renamed `sensation`→`sensory`. |
| M04–M08 | A/B | minor | (top level) | Orphan top-level keys `icd_code`, `vitals`, `neurological_exam`, `red_herrings` duplicate content that belongs inside `patient`/`ground_truth`; the schema silently drops them. The orphan top-level `red_herrings` are actually richer and case-specific (e.g. M07 "anti-TPO 186 IU/mL", M08 "known right ovarian dermoid") while the LOADED `ground_truth.red_herrings` are the generic template (psych presentation / Na / CK). | FLAGGED | Dead duplicate data, not graded. A human should decide whether to promote the case-specific top-level red herrings into `ground_truth.red_herrings` (currently those richer herrings are never seen). Did not delete/restructure (judgment). |
| M01–M08 | C | minor | difficulty / metadata.difficulty_rationale | All "M" cases are labelled subtype = mild ("isolated psychiatric features only, partial syndrome" per pack §6) but every one presents the full classic multistage syndrome (seizures + orofacial dyskinesias + dysautonomia). M07 in particular is a severe/P-level dysautonomic presentation. | FLAGGED | Subtype-vs-presentation mismatch across the whole M batch; difficulty label vs clinical content. Diagnosis unchanged. |
| M01–M08 | B | minor | ground_truth.key_reasoning_points[5] | The reasoning point states the trap is "predominantly psychiatric features **without** overt seizures or dyskinesias", but these M cases DO have overt seizures and dyskinesias — the reasoning point describes a phenotype that doesn't match the case. | FLAGGED | Internal inconsistency (templated reasoning point). |
| M05, M07 | D | minor | initial_tool_outputs.mri.impression | M05 MRI: "Urgent CSF with HSV PCR and autoimmune antibody panel required" — an MRI report prescribing a specific lab workup (autoimmune antibody panel) is borderline cross-modality workup prescription beyond the allowed "recommend further imaging." (M07 MRI is fine: MRV ruling out CVST.) | FLAGGED | Borderline Kind-1; trimming is a content edit, left for review. The within-imaging hedge "differs from typical HSV (symmetric, non-haemorrhagic)" is acceptable. |
| M08 | E | minor | initial_tool_outputs.eeg | EEG `impression` is a placeholder ("See findings above."); `findings[].type`/`location` are generic ("Background"/"Background", "Overall"/"Overall") with real content tucked into `morphology`. Quality degraded vs M01–M03. | FLAGGED | Data present and accurate; needs an authored impression. Not fabricated. |
| M07 | B | minor | initial_tool_outputs.mri | Diagnosis names "right ovarian … teratoma" but the brain MRI for this postpartum case is an MRV; tumour screen delivered via followups — confirm the teratoma is actually delivered in a followup (it is). No defect, noted for completeness. | FLAGGED | Verification note only. |
| ALL (7 male cases: M05, P02, P03, RP01, RP02, RP03, RS03) | B/C | minor | ground_truth.key_reasoning_points[4] | Tumour-screen reasoning point carries the female boilerplate verbatim ("~50% of **young women** have an ovarian teratoma … mandatory in **women of reproductive age**") even though `optimal_actions` correctly prescribe testicular/germ-cell screen + urology. The reasoning point contradicts the (correctly male-tailored) optimal action. | FLAGGED | Affects reasoning-point grading for male cases; `ground_truth` semantic edit → flagged not fixed. |
| S05–S10, P02–P08, RM01, RM02, RP02, RP03, RS01, RS03 (18 cases) | E | major | initial_tool_outputs.csf.special_tests / .interpretation | CSF `special_tests` keys are machine snake_case (`gram_stain`, `HSV_PCR`, `oligoclonal_bands`, `anti_NMDAR_antibody`, `IgG_index`, `HSV_1_2_PCR`) and are echoed literally into the `interpretation` string the agent reads ("gram_stain: No organisms. … anti_NMDAR_antibody: POSITIVE"). Not modality-faithful report prose. | FLAGGED | Systematic generator-batch defect. Re-keying ripples into the auto-built `interpretation`; needs a regeneration script, high hand-edit regression risk. Clinical data correct. |
| 18 cases (P04–P08, RM01, RM02, RP01–RP03, RS01, RS03, S05–S10) | B/E | major | initial_tool_outputs.csf.interpretation | The CSF `interpretation` string renders "(N/A PMN/N/A lymph)" because the cell differential is stored under a `differential` sub-key instead of the `Lymphocytes`/`Neutrophils` keys the interpretation generator expects — a visible "N/A" artifact in the report shown to the agent. | FLAGGED | Underlying differential present (e.g. "96% lymphocytes"); the interpretation string is stale/auto-generated. Same batch as the snake_case issue. |
| RP02, RS01 | D | minor | csf.special_tests / followup labs.abnormal_values_summary | Confirmatory CSF antibody value has an answer-announcing editorial appended: RP02 "POSITIVE 1:32 — diagnostic of anti-NMDA receptor encephalitis"; RS01 "POSITIVE (titer 1:320) — diagnostic confirmation". A positive CSF GluN1 IgG genuinely is near-diagnostic (KEPT), but per the style guide the antibody comment should be hedged/templated, not label the case answer in a value field. | FLAGGED | Gray-zone Kind-2 (confirmatory result is KEPT); stripping the editorial would also require regenerating the auto-built `interpretation`. Left for reviewer. Titer values themselves untouched. |
| RP02 | E | nit | followup labs.interpretation | Unit-doubling artifact: "Positive, titer 1:32 titer (H)" ("titer" appears twice — value already contains it and unit is also "titer"). | FLAGGED | Cosmetic auto-generation artifact. |
| RP01 | B/C | major | ground_truth.key_reasoning_points + primary_diagnosis | INTENTIONAL seronegative case — verified: `primary_diagnosis` = "Post-COVID-19 seronegative autoimmune encephalitis", CSF anti-NMDA-R (repeat) = Negative. But the templated `key_reasoning_points` still assert "CSF anti-NMDAR (GluN1) IgG is the gold-standard test (100% sensitive)" and lead with the young-adult NMDAR phenotype — contradictory for an antibody-negative case diagnosed on Graus seronegative-AE criteria. | FLAGGED | Per instructions: verify-and-flag, do NOT fix. The gold-trajectory reasoning is generic NMDAR boilerplate that misfits the seronegative diagnosis; a human should reconcile the reasoning points with the seronegative answer. |
| RM03 | C | minor | patient.history_present_illness / ground_truth | 62F, 3-month progressive memory decline, ex-smoker with prior persistent cough — constructed (subtype = RM, atypical demographic) to weight paraneoplastic limbic encephalitis (SCLC). Course/age are atypical for classic subacute NMDAR. Antibody positive 1:64 (confirmatory) supports NMDAR. | FLAGGED | Intentional mimic design; flagged for clinician adjudication that the data best supports NMDAR vs other autoimmune/paraneoplastic LE. |
| RS02 | C | minor | initial_tool_outputs.mri | MRI shows restricted diffusion in dentate nuclei, inferior cerebellar peduncles, and corticospinal tracts — an atypical, more toxic/metabolic/COVID-pattern picture for anti-NMDAR-E. Antibody positive 1:1280 (confirmatory) supports the diagnosis. | FLAGGED | Clinical-imaging mismatch for clinician adjudication. |
| RS04 | C | minor | initial_tool_outputs.mri | MRI: "bilateral optic nerve enlargement with T2 hyperintensity and enhancement suggests concurrent optic neuritis" + leptomeningeal enhancement — optic neuritis is unusual for pure NMDAR-E and raises NMOSD/MOG overlap. Antibody positive 1:256 (confirmatory). | FLAGGED | Possible overlap syndrome; clinician to confirm "anti-NMDAR encephalitis" is the best single answer. |
| M04–M08, P02–P08, S05–S10, R-batch | E | nit | initial_tool_outputs.csf.protein | Mixed units across the condition: M01–M03/S01–S04 use mg/dL; M04–M08 use g/L (e.g. 0.52 g/L = 52 mg/dL). Internally consistent within each case. | FLAGGED | Terminology consistency note only. |
| search_medical_literature (M02 etc.) | C | nit | followup literature results | Literature results cite papers outside the criteria-pack allow-list (e.g. Florance 2009 Neurology). These are simulated literature-tool content (population-keyed evidence), not `ground_truth` citations — the allow-list governs `ground_truth` citations, which are clean. | OK | Acceptable per style guide; noted for transparency. |

## Tally

- **Cases audited:** 36 / 36 (every field of every case read).
- **Mechanical validators:** coherence 0, schema valid, vocab pass, leakage detector 0 — all 36, before and after edits.
- **Findings by severity:** major 6 distinct issues (touching ~25 cases via 3 systematic
  batch defects + the M-exam key bug + RP01); minor 9; nit 4. (Many rows are
  batch/condition-wide rather than single-case.)
- **Fixed:** 5 cases (M04, M05, M06, M07, M08) — the `sensation`→`sensory` schema-key
  bug (sensory exam was being dropped); M07 additionally preserved dropped dysautonomia
  into `additional`.
- **Flagged (not fixed):** everything requiring judgment or `ground_truth`/content
  rewriting — the snake_case CSF keys (18 cases), the "N/A PMN/N/A lymph" interpretation
  artifact (18 cases), the M-subtype-vs-presentation mismatch, the male-case female
  boilerplate reasoning point (7 cases), the borderline "diagnostic" antibody editorials
  (RP02, RS01), RP01 seronegative reasoning contradiction, and the RM03/RS02/RS04
  atypical-presentation clinical questions.

## Top clinical-correctness flags for a human to adjudicate

1. **RP01 (seronegative):** reasoning points still claim CSF anti-NMDAR IgG is the
   gold-standard confirmatory test, but the case is antibody-negative and diagnosed as
   seronegative AE — reconcile the gold-trajectory reasoning with the actual answer.
2. **M-batch subtype mismatch:** all M cases carry the full multistage syndrome
   (seizures/dyskinesias/dysautonomia, M07 frankly severe) yet are labelled mild;
   reconsider subtype labels / difficulty.
3. **Male cases (7):** `key_reasoning_points[4]` tells the model to screen "young women"
   for ovarian teratoma while the optimal action correctly orders testicular/germ-cell
   screen — fix the reasoning point to match.
4. **CSF report realism (18 cases):** snake_case test labels and "N/A PMN/N/A lymph"
   leak into the agent-visible report text; needs a regeneration pass for modality
   faithfulness before clinician validation.
5. **RM03 / RS02 / RS04:** atypical course/imaging (chronic older-adult LE; cerebellar/
   corticospinal restricted diffusion; bilateral optic neuritis) — confirm anti-NMDAR is
   the best single answer vs paraneoplastic LE / overlap (NMOSD-MOG) syndromes.
