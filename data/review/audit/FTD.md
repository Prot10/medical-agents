# NeuroBench v5 — FTD case audit

Audited 2026-05-28. Scope: all 25 `FTD-*` cases (M01–M08, P01–P07, S01–S10).
Method: full field-by-field read of every case against `criteria_packs/FTD.md` and
`TOOL_REPORT_STYLE_GUIDE.md`; mechanical validators (coherence, schema, leakage,
vocab) run on all 25. Coherence = 0, schema valid, leakage = 0, vocab pass for all.

Conservative-fix policy applied: only unambiguous mechanical errors fixed inline;
everything requiring judgment FLAGGED. No diagnosis, clinical story, or `ground_truth`
meaning altered. Only `FTD-` files touched.

| case_id | dim (A–E) | severity | region.field path | finding | action | detail |
| --- | --- | --- | --- | --- | --- | --- |
| FTD-M05 | B | minor | `followup_outputs[lithium_adjusted_recheck].output.labs.abnormal_values_summary` | `interpretation` names "Creatinine 1.4 mg/dL (H)" (is_abnormal=true, out of range 0.7–1.3) but `abnormal_values_summary` was `[]` — internal contradiction; every other FTD lab block lists flagged abnormals in the summary. | FIXED | Populated summary with `"Creatinine 1.4 mg/dL (stable CKD stage 2)"` to match the interpretation and is_abnormal flag. Coherence/schema/leakage re-verified green; unicode + trailing newline preserved. |
| FTD-M02 | B | minor | `ground_truth.key_reasoning_points[2]` | Reasoning point says "Symmetric upper-extremity **rigidity** is not parkinsonism warranting DaTscan" but the motor exam explicitly states "no rigidity"; the actual sign is mild bilateral **hyperreflexia** (UMN). The reasoning point cites a sign not present. | FLAGGED | `ground_truth` semantic content — do not edit. Human should reword to "hyperreflexia"/"UMN signs" or remove. Does not change diagnosis (C9orf72 FTD-ALS). |
| FTD-M02 | C/D | minor | `followup_outputs[request_csf_biomarkers].output.special_tests."TDP-43 biomarker (research-grade)"` | CSF reports "Elevated TDP-43 fragments detected (research assay)." No clinically validated CSF TDP-43 assay exists; labelling as "research-grade/research assay" mitigates, but it points at the molecular proteinopathy (TDP-43 = C9orf72 substrate). | FLAGGED | Plausibility / soft answer-pointer; reasonable reviewers could disagree. Consider removing or further hedging. |
| FTD-M06 | B/C | major | `followup_outputs[cbs_motor_exam_apraxia]` + `[request_comprehensive_neuropsych]` vs MRI/FDG | Laterality conflict: MRI and FDG-PET are **left-hemisphere** predominant (and HPI says GRN-FTD "often left-sided"), but the CBS exam reports **LEFT-hand** ideomotor apraxia / graphesthesia loss with right hand intact, and the neuropsych says "LEFT-hand dominant constructions impaired — consistent with right hemisphere praxis." Left-hand cortical signs localize to the RIGHT hemisphere, which contradicts the left-predominant imaging. | FLAGGED | Clinical-judgment laterality inconsistency; a clinician would notice. Either the apraxia laterality or the imaging laterality needs reconciling. Diagnosis (bvFTD-GRN with CBS features) unaffected; flag for human adjudication. |
| FTD-S07 | C | major | `followup_outputs[request_genetic_panel].output.panels.FTD_Genetic_Panel[GRN].value` + `interpretation` + `abnormal_values_summary` | GRN variant `c.1477+1G>A` is labelled a "frameshift mutation," but `+1G>A` at the canonical splice-donor site is a **splice-site** variant, not a frameshift (frameshifts are dup/del/ins). FTD-P02 correctly classifies its GRN `c.1477C>T (p.Arg493*)` as nonsense — so the dataset gets GRN nomenclature right elsewhere; S07 is the outlier. | FLAGGED | Genetics nomenclature is meaning-bearing; fixing requires choosing whether to relabel as "splice-site" or change the variant string — a judgment call. Diagnosis (bvFTD-GRN) unaffected. Recommend human relabel to "splice-site/splice-donor." |
| FTD-P02 | B | minor | `optimal_actions[7]` (`order_specialized_test test_type:genetic_panel:FTD`) vs delivery | Genetic result is delivered via an `interpret_labs` followup, not via `order_specialized_test`; the mock server has a single `specialized_test` output slot (occupied by neuropsych). | FLAGGED (known) | Documented limitation in `metadata.case_body_concerns` ("RESOLVED (coherence sweep)…single output slot"). Per task: flag, do NOT attempt to fix mock-server behavior. |
| FTD-P04 | B | minor | `optimal_actions[7]` (`genetic_panel:FTD`) vs delivery | Same single-output-slot pattern as P02: neuropsych occupies the specialized_test slot, genetics delivered via `interpret_labs`. | FLAGGED (known) | Documented in `metadata.case_body_concerns` ("RESOLVED…single output slot"). Per task: flag, don't fix. |
| FTD-P04 | C | nit (positive) | `ground_truth.useless_tools` / `optimal_actions[8]` | DaTscan is correctly OMITTED from useless_tools and listed as a recommended action because the patient has overt PD (criteria pack: DaTscan useless "unless parkinsonism present"). `key_reasoning_points[0]` flags this exception explicitly. | (none) | No action — noting correct condition-specific handling; the one FTD case where DaTscan is indicated. |
| FTD-M01 / M02 / M03 / M04 / M05 / M06 | C | minor | `ground_truth.optimal_actions[5].tool_name = consult_medical_specialist`, `category: required` | `consult_medical_specialist` is consistently marked `required`, but the criteria pack lists behavioral/cognitive-neurology consult under **Recommended**. Systematic across the series (and S-cases). | FLAGGED | Tier classification (required vs recommended) is judgment; reasonable to keep consult as required for these complex cases. Flag for human tier decision; do not reclassify unilaterally. Note `consult_medical_specialist` is also not in the 12-tool schema list in CLAUDE.md (it is in the criteria pack workup) — a tool-roster question for humans. |
| FTD-P05 / P06 / P07 / S01–S10 | C | minor | `ground_truth.optimal_actions[*].tool_name = consult_medical_specialist` | Same `required` vs pack-`Recommended` tier mismatch as above, present in every P/S case. | FLAGGED | Same as above; systematic, judgment-level. |
| FTD-M07 / M08 | A/E | nit | `metadata.case_body_concerns` | Stale concern claims "required tool `order_specialized_test` (neuropsych) has no initial/followup entry," but the neuropsych report IS present in `initial_tool_outputs.specialized_test`. | FLAGGED | Pre-existing stale metadata note (pre-regen). Skill says append-don't-overwrite metadata; left untouched. Cosmetic. |
| FTD-P01 | A/E | nit | `metadata.case_body_concerns` | Stale concern claims `check_drug_interactions` has no output, but it IS present in `initial_tool_outputs.drug_interactions` (and as step-8 followup). | FLAGGED | Pre-existing stale metadata; left untouched. Cosmetic. |
| FTD-S03 / S05 / S10 | A/E | nit | `metadata.case_body_concerns` (order_cardiac_monitoring fallback "missing") | Stale concern says the `order_cardiac_monitoring` fallback is missing, but a normal Holter fallback IS present in `fallback_tool_outputs.cardiac_monitoring`. These cases also provide a redundant `order_cardiac_monitoring` followup for a tool that is simultaneously in `useless_tools` (harmless: returns a normal result). | FLAGGED | Pre-existing stale metadata + benign redundancy. Left untouched. |
| FTD-P01 | B | nit | `initial_tool_outputs.drug_interactions.valproate.warnings[1]` vs `labs.panels[Ammonia].reference_range` | Warning text says ammonia "upper reference ~32 mcg/dL" (hedged) while the lab panel reference_range for ammonia is "11-35". Soft numeric mismatch (35 vs ~32). | FLAGGED | In hedged interpretive narrative; not a hard contradiction. Cosmetic; reasonable to leave. |
| FTD-M05 | D | nit | `followup_outputs[lithium_adjustment_monitoring].output` (check_drug_interactions) | Gives a specific dose-titration ("Reduce lithium from 450 mg BID to 300 mg BID", "recheck in 1 week"). Style guide allows `check_drug_interactions` category-level management; specific titration is at the edge of that latitude. | FLAGGED | Within the tool's documented exception; noting realism edge only. Not fixed. |
| FTD-M08 | E | nit | `initial_tool_outputs.labs.abnormal_values_summary[0]` | "Toxoplasma IgG 1: 64" has a stray space after the colon (titer should read "1:64"; the value field correctly reads "1:64"). | FLAGGED | Cosmetic typo inside an interpretive summary string; low value, edit risk. Left untouched. |
| FTD-P07 | C | nit | `initial_tool_outputs.labs.panels.Special[CSF 14-3-3 protein]` | A CSF analyte (14-3-3) is listed inside the serum `interpret_labs` panel, though CSF is only obtained later via the `request_csf_biomarkers` followup (which separately reports 14-3-3). A CSF test appearing in a blood-draw panel before any LP is a workflow oddity. | FLAGGED | Plausibility/workflow; could be argued the LP was concurrent. Meaning question — not fixed. |
| FTD-S09 / S10 | C | minor | `ground_truth.differential` vs HPI/social_history | Escalating heavy alcohol use (S09: 6 glasses wine/day; S10: 8–10 beers/day) is described in HPI/social history but is NOT addressed in the differential (no alcohol-related cognitive disorder entry) — unlike FTD-S01/M07 which carefully list and rebut it as a red herring. | FLAGGED | Differential-completeness judgment; escalating alcohol is a plausible competing/contributing cause a reviewer may want represented. Diagnosis unaffected. |

## Cross-cutting observations (informational, not per-case findings)

- **Systemic validator note (all 25):** every case's `metadata.case_body_concerns`
  documents that `order_advanced_imaging` appears in both `optimal_actions`
  (FDG_PET/amyloid_PET) and `useless_tools` (MR_spectroscopy/DaTscan/perfusion_MRI/
  carotid_duplex) — distinct modalities of one catchall tool the coherence script
  cannot disambiguate. Pre-existing, documented, no case-level fix.
- **Single specialized_test slot (P02, P04 explicitly; also the pattern by which all
  cases route the genetic panel through `interpret_labs` rather than
  `order_specialized_test test_type:genetic_panel:FTD`):** mock-server limitation,
  logged in metadata, flagged not fixed per task instruction.
- **Kind-2 (KEPT) within-modality conclusions verified appropriate, not stripped:**
  neuropsych "probable behavioral-variant FTD" (every case); FDG-PET "frontotemporal
  hypometabolism / frontotemporal metabolic profile" (hedged pattern, never "FTD");
  amyloid PET strictly binary "Negative — sparse-to-no amyloid"; DaTscan binary
  "presynaptic dopaminergic deficit" (P04); tau PET regional pattern "consistent with
  a frontotemporal tauopathy / no Alzheimer-typical tau" (P03, P07, S01, S07);
  genetics (C9orf72/GRN/MAPT) and plasma progranulin confirmatory. No Kind-1
  cross-modality synthesis, differential-refutation, or management prescription found
  in any tool report (literature summaries are population-keyed; drug-interaction
  outputs stay category-level per the documented exception).
- **Numeric/units spot-check:** all lab `is_abnormal` flags match stated reference
  ranges across all 25 cases (e.g., glucose >100 flagged, HbA1c above goal flagged,
  lithium 1.28 > 1.2 flagged, anti-TPO 320 > 34 flagged). CSF glucose ratios and
  SUVr/Z-score values internally consistent. Differentials sorted by likelihood
  descending in all 25; all likelihood/category/severity enums valid.

## Tally

- **Cases audited:** 25 / 25 (every field of every case read in full).
- **Mechanical validators:** coherence 0, schema valid, leakage 0, vocab pass — all 25.
- **Findings by severity:** 0 blocker; 3 major (M06 laterality, S07 GRN nomenclature — both judgment FLAGs; plus the M-series/P-S `consult_medical_specialist` tier rolled up as 1 systematic major-ish FLAG, counted minor below); 0 additional blockers.
  - blocker: 0
  - major: 2 (FTD-M06 laterality conflict; FTD-S07 GRN "frameshift" mislabel)
  - minor: 9 (M05 fixed summary; M02 reasoning rigidity; M02 CSF TDP-43; consult tier mismatch ×2 rollups; P01 ammonia ref; S09/S10 alcohol-in-differential; P07 CSF-in-serum-panel; M05 dose-specificity)
  - nit: 7 (stale-metadata notes ×4 groups; M08 "1: 64" spacing; P04 positive DaTscan note; P01 stale drug-interaction metadata)
- **Fixed vs flagged:** 1 FIXED (FTD-M05 abnormal_values_summary); all others FLAGGED.
- **Files changed:** only `FTD-M05.json` (1 file). Unicode convention (literal, no `\u`)
  and trailing newline preserved.

## Top clinical-correctness flags for human adjudication

1. **FTD-M06 — laterality conflict (major):** imaging is left-hemisphere predominant
   but the corticobasal exam + neuropsych describe LEFT-hand cortical signs (→ right
   hemisphere). Reconcile the apraxia laterality or the imaging laterality.
2. **FTD-S07 — GRN `c.1477+1G>A` mislabelled "frameshift" (major):** it is a
   splice-site variant; relabel for genetic accuracy (P02 handles GRN nomenclature
   correctly as a model).
3. **`consult_medical_specialist` tier (systematic, M01–M08, P-series, S-series):**
   marked `required` vs the criteria pack's `Recommended`; also not on the CLAUDE.md
   12-tool roster. Decide tier + tool-roster status dataset-wide.
4. **FTD-M02 — CSF "research-grade TDP-43 fragments":** non-validated assay that
   points at the molecular pathology; consider removing/hedging.
5. **FTD-S09 / S10 — escalating heavy alcohol absent from the differential:** add an
   alcohol-related cognitive disorder entry/red herring for consistency with S01/M07,
   or confirm intentional.
