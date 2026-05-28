# NeuroBench v5 — MG (Myasthenia Gravis) audit

Scope: all 25 case files matching `MG-*` in `data/neurobench_v5/cases/`.
Method: SKILL.md five-dimension field-by-field read against `criteria_packs/MG.md` and `TOOL_REPORT_STYLE_GUIDE.md`.
Mechanical validators (coherence, schema) pass on all 25 before and after edits; leakage detector candidates judged individually (see notes).

| case_id | dim | severity | region.field path | finding | action | detail |
|---------|-----|----------|--------------------|---------|--------|--------|
| MG-M01 | C | minor | case_id vs primary_diagnosis | "M" prefix (pack: mild/ocular-only) but dx is generalized MG Class IIb with bulbar+limb involvement | FLAGGED | Subtype-label vs presentation mismatch; numbering may be sequential. Not a diagnosis change. |
| MG-M01 | E | minor | patient.neurological_exam.gait | "Mildly slow but antalgic" — antalgic = pain-related, no pain in this MG case; conflicts with following "waddling" (proximal weakness) | FLAGGED | Clinical-narrative wording; in patient exam, did not edit. |
| MG-M02 | B | minor | ground_truth.differential[0].key_features | "CK was normal (142)" — case CK is 118 U/L; 142 copied from MG-M01 | FIXED | Changed 142 → 118 to match this case's lab. |
| MG-M02 | B | nit | optimal_actions[4].category | literature search "required" here vs "recommended" in M01/M03 (cross-case inconsistency) | FLAGGED | Within-case fine; pack lists it Required. |
| MG-M03 | B | minor | ground_truth.red_herrings[0].data_point | red herring cites "lower-lobe bronchial wall thickening" but CT says "upper lobe" emphysematous changes | FLAGGED | ground_truth descriptive text mismatches the CT finding it points at; flagged not fixed (gt semantics). |
| MG-P01 | C | minor | case_id vs case content | "P" prefix (pack: progressive/crisis) but case is seronegative diagnostic-puzzle, NIF -62 (no crisis) | FLAGGED | Subtype-label mismatch; otherwise excellent case. |
| MG-P02 | B/C | major | condition / icd_code vs primary_diagnosis | INTENTIONAL LEMS mimic: condition=myasthenia_gravis, icd from gt=G73.1, dx=LEMS | FLAGGED | Designed mimic per task brief — flag, do not fix. |
| MG-P02 | D | nit | followup_outputs[3].output.summary | detector hit "LEMS" — population-keyed literature evidence | FLAGGED | Allowed by style guide (general evidence); intentional, not a leak. |
| MG-P02 | B | nit | initial_tool_outputs.ct.additional_observations | "COPD emphysema present" but COPD not in PMH (50-pk-yr smoker; radiographically plausible) | FLAGGED | Incidental imaging finding, plausible; not fixed. |
| MG-P03 | D | minor | followup_outputs[0].output.findings[0].description | Kind-1 leak: CT finding cited labs ("In context of markedly positive AChR antibodies and positive anti-titin... consistent with thymoma") | FIXED | Stripped cross-modality clause; kept within-imaging "consistent with a primary thymic neoplasm". |
| MG-P03 | E | nit | metadata.difficulty_rationale | "1 red herrings" grammar | FLAGGED | Recurring template field; not fixed. |
| MG-S01 | A | major | followup_outputs[3].output | order_advanced_imaging (MRI chest) mis-validated as EchoReport; findings was list[str] + a stringified Python dict (with None/single-quotes) instead of list[dict] | FIXED | Rebuilt findings as proper list[dict] (region/signal/interpretation); now validates as AdvancedImagingReport with modality "MRI chest" preserved. |
| MG-S01 | B | major | ground_truth.critical_actions[0] & key_reasoning_points[6] | AChR binding stated as "8.7 nmol/L" but labs value is 12.4 nmol/L (stated 3× in labs) | FIXED | Changed both 8.7 → 12.4; also fixed "15-24% RNS decrement" → "16-22%" to match RNS. |
| MG-RM11 | B | minor | initial/followup outputs (no RNS) | step 2 RNS "required" and gt cites "RNS decrement", but no RNS output exists anywhere (specialized_test null; SFEMG present) | FLAGGED | Solvable via SFEMG+serology; missing required-tool output. |
| MG-RM12 | D | minor | initial_tool_outputs.ct.findings[0].description | Kind-1 leak: CT cited dx ("In context of new-onset MG in a 42-year-old, thymic hyperplasia is expected") | FIXED | Stripped cross-modality clause; kept morphologic description. |
| MG-RM13 | B/C | major | condition / icd_code vs primary_diagnosis | INTENTIONAL LEMS mimic: condition=myasthenia_gravis, gt icd=G73.1, dx=LEMS (paraneoplastic SCLC) | FLAGGED | Designed mimic — flag, do not fix. |
| MG-RM13 | E | nit | patient.neurological_exam.additional | "Erectile dysfunction not applicable" template residue in a female patient | FLAGGED | Harmless; not fixed. |
| MG-RM14 | B | minor | gt intubation thresholds | inconsistent NIF/FVC intubation cutoffs across fields (FVC<15 vs <20 mL/kg; NIF -25 vs -30; lit "NIF<-20") | FLAGGED | Guideline "rule of 20/30" approximations; no single correct value. |
| MG-RM14 | D | nit | followup_outputs[5].output.summary | detector hit "myasthenic crisis" — population-keyed patient-education content | FLAGGED | Allowed; not a leak. True MG crisis (not a mimic). |
| MG-RM15 | B | minor | patient.vitals vs top-level vitals | two divergent vitals blocks: admission (rr14/spo2 98) vs crisis (rr10/spo2 87) | FLAGGED | Real-case-seed artifact; both states real in narrative. |
| MG-RM15 | B | minor | initial_tool_outputs.ecg.findings (text) | ECG narrative "86 bpm" vs structured rate 72 (+patient vitals 72) | FIXED | Narrative 86 → 72 to match structured/objective rate. |
| MG-RM15 | D | nit | followup_outputs[1].output.findings RNS text | RNS report names "active myasthenia gravis" (vs impression's hedged "NMJ transmission disorder") | FLAGGED | Borderline within-modality; RNS decrement is KEPT per task; flagged not stripped. |
| MG-RP11 | B | minor | initial_tool_outputs.ecg.findings (text) | ECG narrative "74 bpm" vs structured rate 72 | FIXED | Narrative 74 → 72. |
| MG-RP11 | B | minor | followup MG_antibody_panel AChR blocking | value "3.7 nmol/L" with unit nmol/L but reference_range "< 25%" (unit/range mismatch) | FLAGGED | Recurring across RP/RS seed cases; blocking Ab usually % inhibition. |
| MG-RP12 | B | minor | initial_tool_outputs.ecg.findings (text) | ECG narrative "68 bpm" vs structured rate 72 | FIXED | Narrative 68 → 72. |
| MG-RP12 | B | minor | top-level red_herrings[1] | cites "borderline anti-VGCC (0.04)" but no anti-VGCC value in any tool output | FLAGGED | Red herring references absent data; gt semantics, not fixed. |
| MG-RP12 | B | minor | followup AChR blocking | "1.3 nmol/L" with "<25%" reference (unit/range mismatch) | FLAGGED | Recurring. |
| MG-RP13 | B | minor | initial_tool_outputs.ecg.findings (text) | ECG narrative "64 bpm" vs structured rate 72 | FIXED | Narrative 64 → 72. |
| MG-RP13 | C | nit | followup check_timolol_mg_interaction | topical timolol framed as NMJ contributor; beta-blockers are "controversial" per pack | FLAGGED | Defensible/hedged teaching point; not fixed. |
| MG-RP13 | B | minor | followup AChR blocking | "1.7 nmol/L" with "<25%" reference (unit/range mismatch) | FLAGGED | Recurring. |
| MG-RP14 | B | minor | initial_tool_outputs.ecg.findings (text) | ECG narrative "78 bpm" vs structured rate 72 (vitals 80) | FIXED | Narrative 78 → 72 to match structured rate. |
| MG-RS11 | B | minor | followup AChR blocking | "2.3 nmol/L" with "<25%" reference (unit/range mismatch) | FLAGGED | Recurring. ECG narrative 72 matches structured (clean). |
| MG-RS12 | B | minor | initial_tool_outputs.ecg.findings (text) | ECG narrative "70 bpm" vs structured rate 72 | FIXED | Narrative 70 → 72. |
| MG-RS12 | B | minor | top-level red_herrings (ESR 22, HbA1c) | red herrings cite lab values absent from tool outputs (labs panels empty) | FLAGGED | Recurring seed pattern. |
| MG-RS13 | B | minor | initial_tool_outputs.ecg.findings (text) | ECG narrative "76 bpm" vs structured rate 72 (vitals 78) | FIXED | Narrative 76 → 72. |
| MG-RS13 | B | minor | top-level red_herrings (ANA 1:160) + AChR blocking unit/range | cite absent data; blocking unit/range mismatch | FLAGGED | Recurring. |
| MG-RS14 | B | minor | initial_tool_outputs.ecg.findings (text) | ECG narrative "66 bpm" vs structured rate 72 (vitals 68) | FIXED | Narrative 66 → 72. |
| MG-RS14 | C | minor | hpi "SFEMG normal" vs optimal_actions[2].expected_finding | gold step expects SFEMG positive ("increased jitter") but HPI says prior SFEMG normal (limb SFEMG can miss MuSK MG) | FLAGGED | Clinical-nuance tension; teaching intent plausible but worth adjudication. |
| MG-RS15 | B | minor | followup AChR blocking | "0.3 nmol/L" is_abnormal=true with "<25%" reference + nmol/L unit (under stated threshold yet flagged) | FLAGGED | Unit/range mismatch; ECG narrative 72 matches structured (clean). |
| MG-RS16 | B | minor | initial_tool_outputs.ecg.findings (text) | ECG narrative "68 bpm" vs structured rate 72 (vitals 70) | FIXED | Narrative 68 → 72. |
| MG-RS16 | B | minor | top-level red_herrings (CK 78) + AChR blocking | cites absent CK value; blocking unit/range mismatch | FLAGGED | Recurring. |

## Cross-cutting observations (recurring patterns)

- **ECG narrative vs structured `rate` (FIXED in 7 seed cases: RM15, RP11, RP12, RP13, RP14, RS12, RS13, RS14, RS16):** the embedded ECG report text gave a different bpm from the structured `rate` field (always 72) in every real-case-seed MG case. Aligned the narrative to the objective `rate` field (left structured data untouched per style guide). Some of these also differ from `patient.vitals.hr` by a few bpm (separate cross-region timing difference — flagged, not fixed).
- **AChR blocking antibody unit/range mismatch (FLAGGED, ~8 seed cases):** rows give value in `nmol/L` but `reference_range "< 25%"` (% inhibition). RP14 correctly uses unit "" with "<25%", confirming the others are inconsistent. Did not fix — ambiguous whether unit or range is the error; affects the seronegative/seropositive seed cases uniformly.
- **Real-case-seed `red_herrings` referencing absent data (FLAGGED, ~5 cases):** top-level red herrings cite lab values (ESR, HbA1c, ANA, CK, borderline anti-VGCC) that never appear in the case's tool outputs (labs panels often empty). The agent could not encounter these. ground_truth semantics — flagged for authoring review.
- **Two intentional LEMS mimics (MG-P02, MG-RM13):** prefix MG / `condition: myasthenia_gravis` but `primary_diagnosis`=LEMS / gt `icd_code`=G73.1. By design (task brief). Flagged, not changed.
- **Within-modality electrodiagnostic conclusions (RNS decrement, SFEMG jitter/blocking) and confirmatory results (AChR/MuSK/VGCC/SOX1 antibodies, ice-pack/Tensilon/neostigmine, CT-chest thymoma, SCLC biopsy) were treated as KEPT** per the task brief and style guide; none stripped.

## Tally

- Cases audited: **25** (MG-M01–M03, P01–P03, RM11–RM15, RP11–RP14, RS11–RS16, S01–S04) — every field of every case read.
- Findings by severity: **0 blocker · 4 major · ~27 minor · ~8 nit** (≈39 findings total).
  - Major: MG-P02 mimic mislabel, MG-RM13 mimic mislabel, MG-S01 advanced-imaging schema/serialization defect, MG-S01 AChR titer contradiction. (The two mimic mislabels are intentional-by-design but recorded at major severity as they affect condition/ICD coherence.)
- Fixed: **13 edits across 6 case files** — MG-M02 (CK 142→118); MG-P03 (CT cross-modality leak stripped); MG-RM12 (CT cross-modality leak stripped); MG-S01 (advanced-imaging findings rebuilt to schema + AChR 8.7→12.4 ×2 + decrement range); MG-RM15/RP11/RP12/RP13/RP14/RS12/RS13/RS14/RS16 (ECG narrative bpm aligned to structured rate).
- Flagged (not fixed): the remainder (subtype-label mismatches, two intentional LEMS mimics, AChR-blocking unit/range mismatch, red-herrings citing absent data, intubation-threshold variance, RS14 SFEMG tension, clinical-narrative wording).

## Self-verify

- Coherence validator: **0 issues** on all 25 cases before and after edits (re-confirmed on all 13 edited files).
- Schema (`NeuroBenchCase`): **valid** on all 25; the MG-S01 advanced-imaging followup now correctly validates as `AdvancedImagingReport` (was silently coercing to `EchoReport`, dropping modality).
- Leakage detector candidates (MG-P02, MG-RM14, MG-RM15 literature `summary` hits) are population-keyed evidence / patient-education — intentional, left as-is.
- Only `MG-*` files changed (13 of 25, confirmed via `git diff --name-only`). Trailing newline and literal-unicode convention preserved on every edited file.

## Top clinical-correctness flags for human adjudication

1. **MG-S01 AChR titer contradiction (FIXED to 12.4)** — confirm 12.4 nmol/L is the intended value (labs stated it 3×; gt had stray 8.7, the same value as MG-S02's titer).
2. **MG-RS14 SFEMG tension** — HPI states prior SFEMG was normal, but the gold optimal-action expects SFEMG to show increased jitter. In MuSK MG limb SFEMG can be normal; decide whether the gold step should specify facial SFEMG or accept normal limb SFEMG.
3. **AChR-blocking antibody unit/range mismatch** across the real-case-seed MG cases (nmol/L value with `<25%` reference) — author should standardize to % inhibition (as RP14 does) or to nmol/L with an nmol/L reference.
4. **Subtype-prefix vs presentation** — MG-M01 ("M"=mild/ocular per pack, but generalized) and MG-P01 ("P"=crisis per pack, but a non-crisis seronegative puzzle): decide whether prefixes are purely sequential or should encode the pack subtypes.
5. **Real-case-seed red-herrings referencing data absent from tool outputs** (anti-VGCC 0.04, ESR, HbA1c, ANA, CK) — either add the cited values to the labs panels or revise the red-herring text so the distractor is actually presented to the agent.
6. **MG-M03 red-herring/CT mismatch** — red herring describes "lower-lobe bronchial wall thickening" while the CT reports "upper lobe" emphysema; reconcile the descriptive text.
