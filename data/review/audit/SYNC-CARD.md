# NeuroBench v5 audit — SYNC-CARD (cardiac syncope)

Auditor: condition-audit pass. Scope: all 20 `SYNC-CARD-*` case files, read field-by-field
against `dataset-generation/criteria_packs/SYNC-CARD.md` and
`dataset-generation/TOOL_REPORT_STYLE_GUIDE.md`.

Mechanical gates (whole set): coherence validator **0 issues** on all 20; schema validation
**passes** on all 20; tool-vocab check passes (516/516 dataset-wide, no SYNC-CARD entries flagged);
leakage detector returns candidates only inside `search_medical_literature` summaries/results
(ARVC/CPVT/"cardiac syncope" string matches) — each verified to be **population-keyed general
evidence (Kind-2, KEPT)**, not case-specific verdicts; several even self-label "population-level
features." KEPT findings per task brief verified intact: the arrhythmia IS the modality finding and
is preserved across all cases (3rd-degree/complete AV block, Mobitz II, trifascicular block, sinus
arrest/asystole, sustained/bidirectional/polymorphic VT, Type-1 Brugada, WPW pre-excitation);
confirmatory genetics (SCN5A in P03, RYR2 in RP03) and provocation tests (ajmaline in P03,
tilt-table/exercise stress, EP study) preserved. No `primary_diagnosis` or clinical story altered.

No SYNC-CARD case file was modified — every finding below is a FLAG (judgment / meaning / systematic
generation artifact where the corrected text is itself a judgment call). Nothing met the "unambiguous
mechanical error with a single clearly-correct value" bar for an inline fix.

## Findings

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| SYNC-CARD-RM01 | B/C | major | ground_truth.optimal_actions[2].expected_finding & red_herrings[0].correct_interpretation vs followup_outputs[0] (brain MRI) | Gold reasoning says brain MRI shows "Brainstem T2/FLAIR hyperintensity… consistent with rhombencephalitis" and that "brainstem MRI signal… identify a paraneoplastic encephalitis," but the actual MRI report is **NORMAL brainstem** ("Normal signal intensity throughout the pons and medulla"). The case narrative (MRI-negative, antibody-positive anti-Hu) and the literature summary ("when structural lesions are absent on MRI…") support a normal MRI, so the gold's expected_finding/red-herring text directly contradicts the provided tool output | FLAGGED | Internal contradiction between ground_truth expected_finding and the supplied modality output; resolving it requires deciding which the author intended (the diagnosis effectively hinges on antibody, not MRI). Do not change diagnosis. Human adjudication |
| SYNC-CARD-P01 | D | major | followup_outputs[0].output.impression (echo) | Echo `impression` is a leaked lab-style auto-dump: "Abnormal values: Right ventricle Mildly dilated… (TAPSE 16 mm) qualitative (H), Regional wall motion Subtle RV free wall hypokinesis noted qualitative (H)." Not a proper echo narrative; style guide says echo impression "names cardiac diagnoses directly" | FLAGGED | Clear generation artifact (wrong template applied), but the correct replacement wording is a judgment call → flag rather than rewrite. Underlying findings (RV dilation, TAPSE 16, RV hypokinesis, EF 58%) are intact and correct |
| SYNC-CARD-P02 | D | major | followup_outputs[0].output.impression (echo) | Same lab-style auto-dump leaked into the echo impression: "Abnormal values: Interventricular septum thickness (diastole) 2.1 cm (H)… Diastolic function Grade II diastolic dysfunction (pseudonormal pattern) qualitative (H)." | FLAGGED | Same systematic artifact as P01; the structured echo data (septum 2.1 cm, LVOT-Valsalva gradient 62, SAM, EF 60%) is intact and HCM-coherent. Flag-don't-rewrite |
| SYNC-CARD-RM03 | B/D | major | followup_outputs[3].output.impression (cardiac MRI) | CMR impression omits its own dominant finding: `findings` describe "Subendocardial to transmural LGE in the LAD territory (anteroseptal/apical segments)" + LV dilatation, but the `impression` only states "Elevated native T1 values in the septum suggest additional diffuse interstitial fibrosis. No evidence of infiltrative cardiomyopathy or active inflammation" — the LAD-territory infarct/LGE (corroborated by ECG old Q waves V1-V3 and echo anteroseptal hypokinesis) is dropped | FLAGGED | Impression incomplete vs its own findings; writing the missing line is judgment → flag. The objective findings array is correct and internally consistent |
| SYNC-CARD-RM02 | B | major | followup_outputs[1].output.events / findings (Holter) | Same 03:42 AM event given two contradictory pause durations: events[0] "minimum 28 bpm during a **12-second pause** at 03:42 AM" vs events[3] + impression "Longest pause: **4.8 seconds**… at 03:42 AM." A 12-s pause is also inconsistent with the stated ventricular escape (28-32 bpm) | FLAGGED | Internal numeric contradiction; the 4.8 s value is the one carried into impression/rhythm_summary, but which is intended is ambiguous → flag, don't guess |
| SYNC-CARD-S04 | C | minor | ground_truth.harmful_tools (vs SYNC-CARD-S02) | S04 has severe AS (echo AVA 0.9 cm²) but `harmful_tools` is empty; S02 (also severe AS) correctly lists tilt-table in `harmful_tools` per the criteria pack (tilt relative-contraindicated in moderate-severe AS). S04 only lists it under contraindicated_actions | FLAGGED | Tool-classification inconsistency between two AS cases; per policy, adding/removing harmful_tools is a judgment call. Human should reconcile S02/S04 |
| SYNC-CARD-RS02 | C | minor | ground_truth.differential | Patient completed pembrolizumab (immune-checkpoint inhibitor) 4 months ago — a recognized cause of immune-mediated myocarditis with high-grade AV block — but ICI-myocarditis is absent from the differential (SSS, VT, ACS, vasovagal, orthostatic). CMR T2/edema normal "excludes" it implicitly, and metadata calls it "a minor distracting element" | FLAGGED | Differential-completeness judgment; a clinician may expect ICI myocarditis listed/excluded explicitly. Do not change diagnosis |
| SYNC-CARD-S03 | C/E | minor | initial_tool_outputs.labs.interpretation | Lab interpretation states "low CO2 (20 mEq/L) consistent with a metabolic **alkalosis**/hypervolemic pattern" — low bicarbonate (20) is metabolic **acidosis**, not alkalosis. Also a causal/disease claim that the style guide says routine-panel interpretation should avoid | FLAGGED | Factual error + style-guide deviation in interpretive prose; the abnormal_values_summary list is correct. Fix is a rewording judgment → flag |
| SYNC-CARD-S02 | E | minor | initial_tool_outputs.labs.interpretation | "Mild **normocytic** anemia (Hgb 11.5… MCV 78.7 fL) with **microcytic** indices" — self-contradictory; MCV 78.7 is microcytic by definition (<80) | FLAGGED | Internal wording contradiction in lab prose; the value (MCV flagged L) is correct. Reword is judgment → flag |
| SYNC-CARD-S01 | C | minor | ground_truth.red_herrings[0].correct_interpretation | Says head CT "does not change management… without anticoagulation in a CT-warranted scenario," but the patient IS on apixaban + struck head — which is exactly a CT-warranted scenario. CT is (correctly) NOT in useless_tools and the followup CT is provided | FLAGGED | Slightly self-contradictory red-herring text in an anticoagulated head-strike patient; clinical-judgment nuance for reviewers |
| SYNC-CARD-M01 | C | minor | followup_outputs[2] (tilt-table) | Tilt-table performed (and listed recommended) despite prior anterior STEMI + PCI; pack lists tilt-table as relative-contraindicated in severe CAD. Here it is negative/uneventful and not classed harmful | FLAGGED | Borderline tool-appropriateness call (prior MI vs "severe CAD"); not clearly wrong. Note for reviewers |
| SYNC-CARD-M03 | B | minor | followup_outputs[1] monitor_type vs optimal_actions[3].tool_parameters | Holter followup uses `monitor_type: "holter_48h"` (with duration_hours 48) while the gold step-4 parameter is `holter_24h`; siblings M01/M02 use `holter_24h` with duration 48 | FLAGGED | Cross-field naming inconsistency (validator accepts both); the gold tool_parameters and the returned object differ. Note only |
| SYNC-CARD-M03 | B | nit | followup_outputs[1].events/findings (Holter) | "Isolated PVCs: 187 total in **24 hours**" inside a 48-hour recording (duration_hours 48); same "24 hours" wording appears in M01's 48-h Holter | FLAGGED | Minor intra-report time-window wording mismatch; which count window is intended is ambiguous |
| SYNC-CARD-S01 | B | nit | patient.vitals.hr vs initial_tool_outputs.ecg.rate / Holter | Presenting HR 45 but ECG rate 35 and Holter avg 36 (complete AV block) — ~10 bpm gap | FLAGGED | Plausible given variable escape/bedside-vs-strip timing; note only |
| SYNC-CARD-RS03 | B | nit | ground_truth.optimal_actions[0].expected_finding | Step-1 expected_finding "third-degree AV block with slow ventricular escape **~35 bpm**" but ECG/vitals/Holter all show **38** (templated from an S01-style "~35") | FLAGGED | Tilde-hedged and numerically close; cosmetic. Note only |
| SYNC-CARD-P02 | E | nit | followup_outputs[6].output.results[] (literature) | Literature `results[]` omit the `authors` field that sibling cases include (title/journal/year/key_finding only) | FLAGGED | Schema-optional field absent; cosmetic inconsistency |
| SYNC-CARD (R-series) | B | nit | case_id prefix vs primary_diagnosis | RM01 carries `condition: syncope_cardiac` / SYNC-CARD prefix but the diagnosis is paraneoplastic central sleep apnoea (anti-Hu, G13.1) — an intentional extracardiac mimic; RM02/RM03/RP*/RS* are real-case-seeds whose diagnoses ARE cardiac syncope variants (rheumatic CHB, Mobitz II, ARVC, HCM-mimic myxoma, CPVT, CHB, WPW) | NOTED | Intentional mimic / real-seed design per metadata.source; not mis-prefixing to "fix." No action |
| SYNC-CARD (P/RP) | D | nit | followup_outputs[*].search_medical_literature | Literature summaries name ARVC/CPVT/HCM/Brugada and "cardiac syncope" (detector hits in P01, P02, RM02, RM03, RP01, RP03, RS01, RS02) | NOTED | All verified population-keyed general evidence (guidelines, case-series, registry data); several explicitly framed "population-level." Kind-2 KEPT, intentional. No action |
| SYNC-CARD-P03 / RP03 | D | nit | followup genetics (SCN5A / RYR2) + provocation (ajmaline, exercise) | Confirmatory channelopathy genetics and provocation results name the syndrome/pattern within their own modality | NOTED | KEPT per task brief (genetics/provocation are confirmatory within-modality). Internally consistent (Brugada Type-1 unmasked by fever/ajmaline; bidirectional VT + RYR2 = CPVT). No action |

## Tally

- **Cases audited:** 20 / 20 (M01-03, P01-03, RM01-03, RP01-03, RS01-04, S01-04) — every field of every case read.
- **Findings by severity:** major 5 · minor 6 · nit 5 · noted (intentional, no action) 3 = **19 rows** (16 actionable findings + 3 intentional-design notes).
- **Fixed vs flagged:** 0 fixed, 16 flagged + 3 noted. No case file modified.
- **Top clinical-correctness flags for human adjudication:**
  1. **RM01** — brain-MRI report (normal brainstem) contradicts the gold reasoning that claims brainstem rhombencephalitis signal; reconcile expected_finding/red-herring text with the supplied normal MRI.
  2. **P01 / P02** — echo `impression` fields are leaked lab-style abnormal-value dumps rather than echo narratives (systematic generation artifact); needs proper echo impressions written.
  3. **RM03** — cardiac-MRI impression drops its own dominant LAD-territory infarct/LGE finding.
  4. **RM02** — Holter gives the same 03:42 event a 12-s and a 4.8-s pause duration (pick one).
  5. **S04 vs S02** — tilt-table classed `harmful` in one severe-AS case but not the other; reconcile.
  6. **RS02** — checkpoint-inhibitor (pembrolizumab) myocarditis absent from the AV-block differential.

Coherence and schema stayed **green** for all 20 cases (no edits made). Only SYNC-CARD audit
documentation was written; no condition's case files were touched. Detector residue (literature
summaries, confirmatory genetics, channelopathy provocation) is intentional Kind-2 and not chased to
zero.
