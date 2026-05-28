# NeuroBench v5 audit — SAH (subarachnoid hemorrhage)

Scope: all 30 `SAH-*` cases (M01–M08, P01–P08, RM11, RP11, RS11, RS12, S01–S10).
Method: full field-by-field read of every case against the SAH criteria pack
(Connolly 2012 / Hoh 2023 / Edlow 2008) and the tool-report style guide; mechanical
validators run on every case. Conservative fix policy — only unambiguous mechanical
errors fixed; everything requiring clinical judgment flagged. Per audit instruction,
non-contrast CT establishing SAH ("hyperdense blood, Fisher grade"), CTA aneurysm
characterization, and CSF xanthochromia are confirmatory/diagnostic and KEPT.

Mechanical baseline (all 30 cases): coherence validator 0 issues, schema valid,
tool-vocab pass. Leakage detector flagged only `search_medical_literature` summaries
containing the phrase "aneurysmal subarachnoid hemorrhage" (population-keyed evidence —
allowed by the style guide) and the P01 CT/MRI modality-establishing-SAH lines
(Kind-2, KEPT). No Kind-1 literature leaks found.

## Findings

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| SAH-P04 | E | minor | initial_tool_outputs.csf.special_tests.Alcohol + csf.interpretation | serum ethanol given as "0.08 mg/dL (legal limit)" — wrong unit; the US legal limit and the value 0.08 are unambiguously g/dL (0.08 mg/dL is physiologically meaningless) | FIXED | changed "mg/dL" → "g/dL" in both the special_tests field and the mirrored interpretation string; no other change |
| SAH-M02 | C/B | major | initial_tool_outputs.csf vs ground_truth.harmful_tools | CT shows IVH (3rd ventricle) + mild hydrocephalus and `harmful_tools` lists `analyze_csf` (herniation risk), yet an LP result is populated as initial data — the contraindicated test was performed | FLAGGED | already in metadata.case_body_concerns; removing/relocating the CSF block changes case structure (judgment). LP is doubly inappropriate (CT already diagnostic + hydrocephalus) |
| SAH-M05 | C/B | major | initial_tool_outputs.csf vs ground_truth.harmful_tools | same contradiction: CT shows communicating hydrocephalus, `harmful_tools`=analyze_csf, yet LP populated (OP 32) | FLAGGED | in case_body_concerns; do-not-fix (structure/semantics) |
| SAH-M07 | C/B | major | initial_tool_outputs.csf vs patient anticoagulation + CT | CT Fisher 4 with IVH + hydrocephalus AND patient fully anticoagulated (apixaban, anti-Xa 186), yet a grossly bloody LP (OP 34) is populated — LP doubly/triply contraindicated (hydrocephalus + IVH + anticoagulation) | FLAGGED | in case_body_concerns; clinically the most egregious of the LP contradictions |
| SAH-P04 | C/B | major | initial_tool_outputs.csf vs CT + coagulopathy | CT Fisher 4 + IVH + moderate hydrocephalus AND INR 1.4 (alcoholic liver disease), yet LP populated (OP 38) — contraindicated (hydrocephalus + uncorrected coagulopathy) | FLAGGED | in case_body_concerns; do-not-fix |
| SAH-RS12 | C/B | major | initial_tool_outputs.csf vs CT | CT Fisher 4 + IVH (3rd ventricle) + early communicating hydrocephalus, `harmful_tools`=analyze_csf, EVD critical-action present, yet LP populated | FLAGGED | in case_body_concerns; same herniation-risk LP contradiction as M02/M05/M07/P04 |
| SAH-M06 | C | major | ground_truth.critical_actions + harmful_tools + metadata.case_body_concerns | CT explicitly "No acute hydrocephalus" and no IVH, yet critical_actions includes "Consult neurosurgery for emergent external ventricular drain placement given acute hydrocephalus", harmful_tools CSF rationale invokes "hydrocephalus or intraventricular extension", and case_body_concerns carries the boilerplate hydrocephalus/IVH note — all reference a complication this case does not have (copy-paste from a hydrocephalus case) | FLAGGED | GT semantics — do not auto-edit. The EVD action is clinically wrong for this Fisher-3, no-hydrocephalus case; the harmful_tools=CSF entry is mis-applied (LP here is unnecessary but not herniation-dangerous) |
| SAH-M08 | C | major | ground_truth.critical_actions + harmful_tools + metadata.case_body_concerns | identical contamination to M06: CT "No acute hydrocephalus", no IVH (Fisher 2-3), yet EVD-for-acute-hydrocephalus critical action + hydrocephalus-keyed harmful_tools CSF rationale + boilerplate case_body_concern | FLAGGED | GT semantics; sentinel-rebleed case incorrectly inherited the severe-case hydrocephalus boilerplate |
| SAH-M03 | D | minor | followup `request_sumatriptan_interaction`.output.warnings[0] | drug-check warning "This patient has confirmed SAH - sumatriptan absolutely contraindicated" announces the case diagnosis in a drug-interaction report (guide: delete sentences that use the drug check to announce/confirm the diagnosis) | FLAGGED | borderline — the sumatriptan-in-SAH contraindication itself is legitimate category management; only the "this patient has confirmed SAH" verdict edges past. Left as-is (trim is judgment) |
| SAH-P01 | D | minor | followup `request_sumatriptan_sah_interaction`.output.warnings[1] | drug-check warning "Residual headache is from SAH, not migraine" is a case-specific diagnostic verdict in a drug-interaction report | FLAGGED | same pattern as M03; the CONTRAINDICATED-in-SAH content is legitimate, the diagnosis assertion is the only leak; do-not-fix (judgment) |
| SAH-P01 | D | nit | followup `request_mri_brain`.output.impression line 2 | MRI impression states FLAIR has "increased sensitivity for subarachnoid blood compared to non-contrast CT in the subacute setting" — a generic cross-modality sensitivity comparison (style guide allows comparison only to a prior study of the same modality) | FLAGGED | generic teaching statement, not citing this patient's CT result; the MRI naming subacute SAH on GRE/SWI/FLAIR is correctly Kind-2 KEPT |
| SAH-P02 | C | minor | ground_truth.critical_actions / optimal_actions step 6 | diagnosis is perimesencephalic NON-aneurysmal SAH (CTA + 6-vessel DSA negative) yet critical_actions/optimal_actions retain generic aneurysmal-SAH boilerplate ("definitive aneurysm securing (clipping or coiling)", nimodipine x21d as critical) with no aneurysm to secure | FLAGGED | GT semantics; step-2 expected_finding correctly says "No aneurysm identified", creating mild internal tension. Reviewer should confirm intended management for the non-aneurysmal entity |
| SAH-RP11 | D | nit | initial_tool_outputs.csf.special_tests.Oligoclonal_bands | confirmatory CSF special test annotated "(known MS finding - not relevant to acute diagnosis)" — a mild within-CSF dismissal of the MS differential | FLAGGED | borderline Kind-1; single hedge (not a numbered refutation), values are confirmatory and KEPT; defensible as factual annotation against the patient's own prior MS CSF |
| SAH-P05 | C | nit | ground_truth.icd_code | right MCA bifurcation aneurysm coded I60.7 ("other intracranial artery") whereas the other MCA cases (M01, M03, S03) use I60.1 | FLAGGED | ICD-10 SAH sub-coding is somewhat discretionary; noted for consistency. Differential reordering (PRES/eclampsia HIGH first → RCVS/dissection/pituitary LOW → migraine very_low) verified CORRECT and likelihood-descending |
| SAH-RS11, RS12, RM11, RP11 | B | info | case_id prefix vs criteria-pack §6 | all four "R" cases are true-positive aneurysmal SAH (positive CT, CTA aneurysm, xanthochromic LP), NOT the "reverse/mimic with negative SAH workup" the criteria pack §6 describes for the R subtype | NOTED | the v5 R-series here are straightforward/standard CONFIRMED SAH (difficulty_rationale = "Classic CT-positive SAH"), not mimics. Diagnosis matches the data — not a data error, but the R-prefix does not carry the pack's mimic meaning. Reviewer should be aware the SAH set contains no true negative-workup mimic case |
| (all 30) | A/B | info | followup_outputs[].tool_name (TCD) | every case routes transcranial Doppler through `order_specialized_test` rather than `order_advanced_imaging` (modality=transcranial_doppler), inconsistent with TOOL_PARAMETER_VOCABULARY.md and the case's own optimal_actions step (which uses order_advanced_imaging + transcranial_doppler) | NOTED | pre-existing, self-documented in every case's metadata.case_body_concerns; whole-dataset vocab validator still passes (test_type free-text). Consistent authoring artifact, not auto-edited |

## Cross-cutting positives (verified, no action)

- CSF glucose ratios computed correctly in every case with a stated ratio (e.g. M01 78/148=0.53, P06 68/128=0.53, S08 114/228=0.50).
- Lab `is_abnormal` flags consistent with reference ranges throughout (anemia Hgb/MCV/ferritin in P06; HELLP LDH/AST/platelets in P05; anti-Xa 186 in M07; INR 1.4 in P04; bicarbonate 18 with acetazolamide in P07).
- ECG `clinical_correlation` correctly empty `""` across all cases; neurogenic T-wave/QTc findings stay within cardiology voice.
- Differentials likelihood-descending in all 30 cases; valid enum values.
- The S-series correctly does NOT populate an LP when CT shows IVH/hydrocephalus (CSF absent, harmful_tools=analyze_csf) — the contraindicated-LP handling the M/P/RS12 cases got wrong.
- Confirmatory results KEPT as intended: CT "subarachnoid hemorrhage / Fisher grade", CTA saccular aneurysm characterization, CSF xanthochromia/spectrophotometry, MRI GRE-SWI subacute SAH (P01, P05).
- Subtype red herrings clinically sound: perimesencephalic non-aneurysmal (P02), late-presenter CT-negative (P01, P03), anemic CT-false-negative (P06), postpartum PRES/eclampsia overlap (P05), IIH overlap (P07), dual-antiplatelet STEMI-mimic (P08), MS/natalizumab overlap (RP11), cocaine-precipitated (S08).

## Tally

- Cases audited: 30 (all SAH-*).
- Findings: 0 blocker, 8 major, 5 minor, 0 nit-only-fixed (4 nit/info rows), plus 3 info/NOTED rows.
  - By severity: major 8 (M02, M05, M06, M07, M08, P04, RS12, P02), minor 4 (P04-FIXED, M03, P01, RP11), nit 2 (P05, P01-MRI), info/noted 3 (R-prefix, TCD-tagging, leakage-baseline).
- Fixed: 1 case (SAH-P04 — ethanol unit g/dL, mechanical).
- Flagged: 13 distinct findings across 12 cases (judgment / GT semantics / realism).

## Top clinical-correctness flags for human adjudication

1. **Contraindicated LP performed (5 cases: M02, M05, M07, P04, RS12).** Each has CT-confirmed SAH with hydrocephalus and/or IVH (M07 and P04 additionally have anticoagulation / coagulopathy), yet a lumbar-puncture result is populated as initial data while `harmful_tools` simultaneously labels `analyze_csf` contraindicated. The benchmark presents data from a test the gold answer says should not have been done.
2. **Hydrocephalus/EVD boilerplate in non-hydrocephalus cases (M06, M08).** Both CTs state "No acute hydrocephalus" with no IVH, yet `critical_actions` mandates emergent EVD "given acute hydrocephalus" and the harmful_tools CSF rationale invokes hydrocephalus — copy-paste contamination from severe cases producing a clinically wrong critical action.
3. **Perimesencephalic non-aneurysmal SAH (P02) retains aneurysmal-SAH management boilerplate** ("definitive aneurysm securing", nimodipine x21d as critical) despite negative CTA and 6-vessel DSA — confirm intended management for the non-aneurysmal entity.
4. **R-series are not mimics.** All four SAH-R* cases are confirmed aneurysmal SAH, not the negative-workup mimics the criteria pack §6 describes; the SAH set therefore contains no true thunderclap-mimic (RCVS/dissection/pituitary-apoplexy/CVST) case.

Self-verify: coherence validator 0 and schema valid for the fixed case (SAH-P04) and unchanged for all others; only `data/neurobench_v5/cases/SAH-P04.json` was edited; unicode escaping convention preserved. The leakage detector's residual hits (literature population-evidence, CT/MRI modality-establishing-SAH) are intentional and were not chased to zero.
