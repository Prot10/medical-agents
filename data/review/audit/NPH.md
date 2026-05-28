# NeuroBench v5 audit — NPH (normal pressure hydrocephalus)

Scope: all 25 `NPH-*` cases (M01–M08, P01–P07, S01–S10).
Method: full field-by-field read of every case against the NPH criteria pack
(Relkin 2005 / Hakim triad) and the tool-report style guide; mechanical validators
run on every case. Conservative fix policy — only unambiguous mechanical errors fixed;
everything requiring clinical judgment flagged.

Mechanical baseline (all 25 cases): coherence validator 0 issues, schema valid,
leakage detector 0 candidates, tool-vocab pass.

## Findings

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| NPH-M01 | B/D | minor | initial_tool_outputs.followup `request_amyloid_pet`.output.modality | `modality` read "FDG-PET brain" while tracer, Centiloid score, and impression are unambiguously amyloid PET (18F-Florbetapir, CL 42, binary positive call) | FIXED | changed modality to "Amyloid PET"; the entire report body is amyloid PET, so the label was a copy-paste slip |
| NPH-M08 | E | nit | initial_tool_outputs.labs.interpretation | double space in "INR 1.4  (H)" | FIXED | collapsed to single space |
| NPH-P02 | D | minor | followup `request_msa_exclusion`.output.results[0].key_finding | literature result contained a case-specific verdict ("This patient has good historical levodopa response and no autonomic failure — MSA-P less likely") — Kind-1 leak (literature must be population-keyed) | FIXED | rewrote to general phrasing ("a sustained historical levodopa response and absence of autonomic failure argue against MSA-P"); summary was already population-level |
| NPH-P07 | B | major | ground_truth.red_herrings[1].data_point | red-herring names "Past breast cancer (currently in clinical remission)" but the patient's malignancy is prostate cancer (Gleason 6, finasteride); entry copy-pasted from NPH-P06 | FLAGGED | noted in metadata.case_body_concerns; not auto-edited (ground_truth content). LMC differential/contraindicated-action stay relevant via the prostate cancer, but the named primary is wrong |
| NPH-M07 | C | major | initial_tool_outputs.mri + ground_truth.primary_diagnosis | imaging does NOT formally meet NPH morphometric thresholds — Evans index exactly 0.30 (pack requires >0.3) and callosal angle 91° (pack requires <90°); HPI itself states "does not meet NPH criterion"; gold answer is still iNPH carried on positive tap (20%) + drainage (30%) | FLAGGED | intentional borderline "moderate" design, but a clinician should confirm iNPH is the intended gold answer when neither imaging threshold is strictly satisfied |
| NPH-P04 | C | major | ground_truth.primary_diagnosis vs CSF/FDG-PET | gold = "iNPH with concurrent bvFTD"; single tap only 18% (below threshold), CSF NfL markedly elevated (2840), FDG-PET dominant bvFTD pattern — NPH carried on extended drainage (32%) + interval ventriculomegaly + DESH | FLAGGED | aggressive copathology call; confirm NPH component is intended given the dominant bvFTD signal |
| NPH-M04, M05, M08, M07 | D | minor | followup neuropsych `quantitative_data` (profile/pattern field) | neuropsych free-text names the integrated/cross-modality diagnosis (e.g. "Mixed NPH ... and possible early AD", "Parkinson's cognitive pattern with likely additive NPH frontal component", "...cirrhosis-related cognitive slowing and NPH frontal-subcortical pattern") | FLAGGED | borderline Kind-1: a neuropsych report may name a cognitive profile but should not synthesize NPH/PD/cirrhosis. Consistent across cases (likely intentional authoring style); leak detector did not flag. Impression fields are correctly within-modality |
| NPH-M01 | D | minor | followup `request_amyloid_pet`.output.findings[1] | per-finding text "typical of Alzheimer's amyloid pattern" names the disease in an amyloid-PET report (guide: amyloid PET strictly binary, must not say "Alzheimer's") | FLAGGED | impression itself is correctly binary; the residual disease-naming is in a finding sub-field |
| NPH-P01 | D | minor | followup `request_dat_scan`.output.impression | DaTscan impression distinguishes PD from non-PD ("Pattern does not conform to the typical asymmetric posterior putaminal loss seen in Parkinson's disease") — guide says DaTscan is binary and must NOT distinguish PD vs MSA/PSP | FLAGGED | hedged within-imaging caveat; reasonable clinicians may accept it, but it edges past the binary limit |
| NPH-M05 | D | minor | initial_tool_outputs.mri.findings (substantia nigra) | MRI finding "Reduced neuromelanin signal bilateral substantia nigra — consistent with Parkinson's" names the disease in the MRI report | FLAGGED | defensible as a legitimate neuromelanin-MRI within-modality read (patient genuinely has PD); noted for reviewer |
| NPH-M06, NPH-S10 | D/E | minor | initial_tool_outputs.labs Coagulation Anti-Xa.value | lab `value` holds a management instruction ("Hold rivaroxaban 24h prior to LP" / "Held 48h prior to LP — DOAC hold protocol followed") rather than a measured value | FLAGGED | unrealistic for a lab-result field and carries management text; left as-is (no correct measured value to substitute) |
| NPH-M06 | B | minor | ground_truth.differential[0].key_features | VCI key_features says "Prior infarct and ongoing vascular risk..." but this patient has no prior infarct (subdural + AF); text copy-pasted from a stroke-history case | FLAGGED | does not change the diagnosis; differential entry references a feature the patient lacks |
| NPH-M05 | C | nit | ground_truth.primary_diagnosis | "Idiopathic NPH with concurrent Parkinson's disease" — "idiopathic" is slightly inconsistent with a named concurrent etiology, though still G91.2 | FLAGGED | descriptive label; reviewer may prefer "NPH with concurrent PD" without "idiopathic" |
| NPH-S03, S04, S07, S08, S09 | E | nit | difficulty vs metadata.difficulty_variant_description | difficulty enum = "moderate" while the description text calls them "Straightforward iNPH" | FLAGGED | cosmetic enum/description mismatch; enum is the operative field |
| (all 25) | A | info | metadata.vocab_gap | every case self-documents that "phase_contrast_MRI"/"CSF_flow_MRI" and "extended_lumbar_drainage" are not in the closed tool-parameter vocabulary | NOTED | pre-existing documented gap; whole-dataset vocab validator still passes (free-text modality strings, not enum params) |
| (all 25) | D | info | initial_tool_outputs.csf.special_tests + impression | CSF AD/PD biomarkers (Aβ42, tau, p-tau, α-synuclein RT-QuIC), CSF cytology/flow-cytometry/CEA exclusions, NfL, tau-isoform analysis | KEPT | confirmatory / biomarker results legitimately stated as fact per the style guide (Kind-2); not leakage |
| (all 25) | D | info | initial_tool_outputs.mri Evans/DESH/callosal-angle + tap-test gait response | Evans index, DESH, callosal angle, aqueductal flow void, large-volume-tap TUG/10m improvement | KEPT | objective findings the audit brief explicitly designated KEPT; verified internally consistent in every case |

## Internal-consistency spot checks (all passed unless flagged above)

- Patient age/sex used consistently across HPI, exam, and every report in all 25 cases.
- Every lab `is_abnormal=true` value verified outside its stated reference range and vice-versa
  (notably: M03 Anti-Xa 0.18 > trough 0.17; M07 B12 202 at floor not flagged + MMA 320 > 271 flagged;
  M08 cirrhosis panel; P06 CA 15-3 28 at "<28" boundary flagged with explicit rationale;
  P07 PSA 4.2 > 4.0; S09 Cr 1.4 / BUN 24 / glucose 138).
- CSF glucose ratios recompute correctly against paired serum glucose (e.g. M07 68/162=0.42; P03 66/112=0.59; S09 70/138=0.51).
- Opening pressure ≤24.5 cmH2O ("normal pressure" criterion) satisfied in every case (range 11–18).
- Differentials sorted by likelihood descending; all likelihood/category/severity enums valid.
- MRI impressions consistent with their own findings; no cross-modality synthesis in MRI/CT impressions.

## Tally

- Cases audited: 25 / 25 (every field of every case read).
- Findings by severity: 0 blocker; 3 major (all FLAGGED — P07 mis-prefixed red-herring, M07 sub-threshold imaging vs iNPH gold, P04 aggressive bvFTD copathology call); 9 minor; 4 nit; plus KEPT/NOTED info rows.
- Fixed: 3 (NPH-M01 amyloid-PET modality label; NPH-M08 double-space typo; NPH-P02 case-specific literature verdict). Plus 1 case_body_concerns note appended (NPH-P07).
- Flagged (not fixed): all major + the minor/nit judgment items above.
- Files touched: NPH-M01, NPH-M08, NPH-P02, NPH-P07 only. Coherence 0 and schema valid re-confirmed on all four after edits; trailing newlines preserved; no non-NPH file modified by this audit.

## Top clinical flags for human adjudication

1. **NPH-P07** — red_herrings[1] names "breast cancer" but patient has prostate cancer (copy-paste from P06). Correct the named malignancy or remove the entry.
2. **NPH-M07** — gold answer is iNPH although Evans = 0.30 (not >0.30) and callosal angle = 91° (>90°); the HPI explicitly notes the imaging does not meet criteria. Confirm iNPH is intended on the strength of the positive tap/drainage alone.
3. **NPH-P04** — "iNPH + bvFTD copathology" with a sub-threshold single tap (18%), markedly elevated CSF NfL, and a dominant bvFTD FDG-PET pattern. Confirm the NPH component is intended rather than over-called.
4. **Cross-case neuropsych `quantitative_data` synthesis** (M04/M05/M07/M08) — these free-text fields name the integrated NPH/PD/AD/cirrhosis attribution inside a neuropsych report. Decide whether to keep as authoring style or strip to within-modality profile only.
