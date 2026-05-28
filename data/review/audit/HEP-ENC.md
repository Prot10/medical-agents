# NeuroBench v5 audit — HEP-ENC (hepatic encephalopathy)

Auditor: condition-audit pass. Scope: all 25 `HEP-ENC-*` case files, read field-by-field
against `dataset-generation/criteria_packs/HEP-ENC.md` and
`dataset-generation/TOOL_REPORT_STYLE_GUIDE.md`.

Mechanical gates (whole set): coherence validator **0 issues** on all 25; schema validation
**passes** on all 25; leakage detector **0 candidate leaks** on all 25; tool-vocab check passes
(516/516 dataset-wide). KEPT findings per task brief verified intact: labs
(ammonia/LFTs/INR/albumin) internally consistent and plausible; EEG triphasic-wave findings
preserved.

## Findings

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| HEP-ENC-M08 | B | minor | ground_truth.red_herrings[1].data_point | Red-herring text said "Low-grade fever 37.8°C" but `patient.vitals.temp`=38.2 (HPI also says 38.2°C); field_path points at that temp | FIXED | Corrected data_point to "38.2°C" to match the value it references; pure descriptor fix, no semantic change |
| HEP-ENC-P02 | B | minor | ground_truth.red_herrings[1].location / .field_path | `location` pointed to `panels.Toxicology` which does not exist in this case; ethanol 22 is in `panels.Drug_Levels`; field_path was empty | FIXED | Set location → `...panels.Drug_Levels`, field_path → `...Drug_Levels[1]` (actual ethanol location) |
| HEP-ENC-M04 | A/B | minor | difficulty | Top-level `difficulty="diagnostic_puzzle"` but metadata.difficulty_description, difficulty_rationale, primary_diagnosis and HPI all describe a *moderate* case ("classic moderate-difficulty HE case"); all 7 sibling M cases are "moderate" | FLAGGED | Difficulty enum is a judgment field; body text strongly implies "moderate" was intended. Human should reconcile. Noted for adjudication |
| HEP-ENC-M07 | B | minor | ground_truth.red_herrings[1].data_point | Says "Morbid obesity (BMI 31 with bariatric history)" but patient BMI=33.6 and there is NO bariatric history anywhere in M07 (PMH/HPI). Phantom history likely cross-contaminated from an S10-style template | FLAGGED | BMI number is wrong (31 vs 33.6) AND a fabricated clinical fact ("bariatric history"); removing the phantom history is a semantic change → flag, don't fix |
| HEP-ENC-M05 | C | major | ground_truth.primary_diagnosis / HPI / lit followup | Case premise = zinc *excess* (zinc 180) precipitates HE by inhibiting urea-cycle arginase. Mainstream view is the opposite: zinc *deficiency* impairs the urea cycle and zinc supplementation is generally *recommended* in HE. The case is internally self-consistent but the mechanism is unconventional | FLAGGED | Clinical-plausibility call for the clinician reviewers; do not change diagnosis. Low copper 68 as a zinc-displacement red herring is internally coherent |
| HEP-ENC-M03 | B | minor | patient.clinical_history.medications | TMP-SMX is a load-bearing precipitant (HPI + ground_truth) but is absent from the `medications` list (started by outside PCP 1 wk ago) | FLAGGED | Defensible (outside Rx, may not be on reconciled home-med list) but a reviewer may want it represented; flag-don't-fix |
| HEP-ENC-S02 | E | minor | metadata.difficulty_description | Stale/templated text: "NASH cirrhosis with constipation and dietary protein excess" — actual case is **alcoholic** cirrhosis precipitated by **rifaximin non-adherence + diarrhea** | FLAGGED | Non-load-bearing metadata description, mismatched to the case; correcting is low-risk but is prose, so flagged for human |
| HEP-ENC-S03 | E | minor | metadata.difficulty_description | Stale/templated text: "hepatitis B cirrhosis, SBP as precipitant" — actual case is **alcoholic** cirrhosis precipitated by **E. coli urosepsis** (paracentesis here *excludes* SBP, PMN 186) | FLAGGED | Same class as S02; mismatched metadata description |
| HEP-ENC-P04 | B | minor | metadata.vocab_gap / optimal_actions[6].tool_parameters | ATP7B (Wilson) genetic test uses placeholder `test_type: "genetic_panel:CADASIL"` because no `genetic_panel:wilson` exists in the closed vocab. Already self-documented in metadata.vocab_gap | NOTED | Author flagged "flag-don't-fix"; requires adding to TOOL_PARAMETER_VOCABULARY.md (out of scope). Followup specialized_test text correctly names ATP7B |
| HEP-ENC-P07 | B | nit | initial_tool_outputs.labs.panels.LFTs (Ammonia ref range) | Ammonia reference_range "11-45" here (and HPI "lab ULN 45"); 23 of 24 sibling cases use "11-51" (S08/S09/S10 use "11-35"). Internally consistent within P07 (48 correctly flagged vs ULN 45) | FLAGGED | Cross-case lab-reference variance, not an intra-case error; touching it would alter P07's deliberate "borderline ammonia" framing. Note only |
| HEP-ENC-S08 | E | nit | patient.history_present_illness | "dark, tarry stools" (melena = upper-GI) described as "active lower GI blood loss" — imprecise; ground_truth correctly treats it as GI hemorrhage | FLAGGED | Minor language imprecision in HPI prose; not fixed |
| HEP-ENC-P06 | B | nit | case_id prefix vs primary_diagnosis | Intentional mimic: condition enum `hepatic_encephalopathy` / prefix HEP-ENC, but primary_diagnosis = NCSE (ICD G41.2) with concurrent severe HE. Deliberate per metadata | NOTED | Intentional reverse/mimic design (NCSE superimposed on HE); EEG legitimately makes the electrographic NCSE call (KEPT). No action |
| HEP-ENC-S01 | D | nit | initial_tool_outputs.eeg.findings[0].morphology | Per-finding morphology says "TEXTBOOK HE triphasic waves" — mild editorializing linking pattern to HE within the EEG | NOTED | Triphasic waves are a standard EEG descriptor and the impression stays electrographic; no cross-modality synthesis. Acceptable Kind-2 |

## Cross-cutting observations (no action)

- **ICD mapping is internally sound**: grade III–IV / coma cases use K72.91 (with coma);
  grade II / II–III cases use K72.90 (without coma). Consistent across all 25.
- **Differential ordering**: every case sorts likelihood descending; all likelihood/category
  enums valid.
- **Sequence constraints**: every case has the `order_ct_scan → analyze_csf` (hard) LP-after-imaging
  constraint; cases adding MRI (M04, P03, P04, P05) also add `analyze_brain_mri → analyze_csf`.
- **Style-guide compliance**: routine labs carry `clinical_significance: null`; EEG impressions stay
  electrographic and never say "epilepsy"; advanced-imaging Wilson/Wernicke/PRES/manganese calls are
  within-modality (Kind-2 KEPT); `check_drug_interactions` gives category-level management as allowed.
- Confirmatory results legitimately named within-modality (ATP7B variants P04, ascitic Gram-stain/culture
  S01/S09, MRI Wernicke pattern P05) are KEPT, not leakage.

## Tally

- Cases audited: **25** (M01–M08, P01–P07, S01–S10) — every field of every case read.
- Findings: **13 total** — 0 blocker, 1 major (M05 zinc-mechanism), 8 minor, 4 nit/noted.
- Fixed: **2** (M08 fever value; P02 red-herring panel pointer) — both unambiguous mechanical descriptor errors.
- Flagged: **11** (1 major + minors/nits requiring judgment).
- Self-verify: coherence stayed **0** and schema **valid** on both edited files; only HEP-ENC-M08
  and HEP-ENC-P02 changed; unicode/no-trailing-newline convention preserved.

## Top clinical flags for human adjudication

1. **HEP-ENC-M05 (major)** — premise that zinc *excess* causes HE via arginase inhibition runs
   counter to the mainstream teaching that zinc *deficiency* impairs the urea cycle (zinc is usually
   supplemented in HE). Internally consistent but clinically unconventional; needs a clinician's call.
2. **HEP-ENC-M07** — red-herring fabricates a "bariatric history" and wrong BMI (31 vs 33.6) not
   present in the case body; decide whether to correct the descriptor or accept as-is.
3. **HEP-ENC-M04** — difficulty enum (`diagnostic_puzzle`) contradicts its own metadata/HPI ("moderate");
   reconcile the label.
4. **HEP-ENC-S02 / S03** — metadata.difficulty_description copied from a different case template
   (wrong etiology and precipitant); cosmetic but worth correcting before clinician review.
