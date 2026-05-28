# NeuroBench v5 audit — MS-RR (multiple sclerosis, relapsing-remitting)

Scope: all 20 `MS-RR-*` cases (M01–M03, P01–P03, RM01–RM03, RP01–RP03,
RS01–RS04, S01–S04).
Method: full field-by-field read of every case against the MS-RR criteria pack
(McDonald 2017 / Thompson 2018; NMOSD/MOGAD exclusion) and the tool-report style
guide; mechanical validators run on every case. Per the brief: MRI lesion
description + "demyelinating appearance" KEPT; CSF oligoclonal bands KEPT
(confirmatory); VEP P100 delay KEPT; brain-biopsy histology KEPT — but McDonald
DIS/DIT → MS synthesis in a report is the agent's job and is flagged.
Conservative fix policy — only unambiguous mechanical errors fixed; everything
requiring clinical judgment flagged.

Note on the "R" prefix: all R-prefixed MS-RR cases (RM/RP/RS) keep
`primary_diagnosis = multiple sclerosis` (tumefactive variant for RM01/RM02 and
all RP cases; atypical-onset/standard RRMS for RM03/RS). Here "R" denotes an
MS presentation that mimics something else (tumor, stroke), not a non-MS answer.
case_id prefix and `condition` enum are therefore consistent in every case — not flagged.

Mechanical baseline (all 20 cases): coherence validator 0 issues, schema valid,
tool-vocab pass. Leakage detector: 5 candidate hits, all in
`search_medical_literature` summaries / one MRI hedge — judged below (4 are
population-keyed Kind-2; the MRI hit is a "not classic for MS" negation).

## Findings

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| MS-RR-M01, M02, M03, P01, P02, P03, RM02, RM03, RP01 | E | minor | followup `request_oct`.output.findings[].value + quantitative_data (+ impression in RP01) | OCT values carried a duplicated unit "`NN um um`" (the value string already ends in "um" and an extra "um" was appended) | FIXED | replaced "um um" → "um" throughout each file (8–12 occurrences/file); numeric values and meaning unchanged |
| MS-RR-RP02 | E | minor | followup `request_oct`.output.findings[].value + quantitative_data + impression | duplicated unit "`72 micrometers (thinned) micrometers`" / "`68 micrometers (reduced) micrometers`" | FIXED | dropped the trailing redundant " micrometers" (3 sites each); value/meaning unchanged |
| MS-RR-M01 | B | minor | initial_tool_outputs.csf.glucose_ratio + interpretation | stated CSF/serum glucose ratio 0.68 ≠ 56.6/91 = 0.62 | FIXED | corrected to 0.62 in both fields (clinically benign either way; arithmetic now matches the case's own component values) |
| MS-RR-M02 | B | minor | initial_tool_outputs.csf.glucose_ratio + interpretation | stated ratio 0.67 ≠ 57.2/92 = 0.62 | FIXED | corrected to 0.62 in both fields |
| MS-RR-P01 | B | minor | initial_tool_outputs.csf.glucose_ratio + interpretation | stated ratio 0.67 ≠ 58.1/92 = 0.63 | FIXED | corrected to 0.63 in both fields |
| MS-RR-RM02 | B | minor | followup `request_spine_mri`.output.impression | impression says lesion "in the dorsal cord" but the finding location, signal text, and additional_observations all say "lateral cord on the right" | FIXED | impression "dorsal cord" → "lateral cord" (correct value clear from 3 concordant sources within the same report) |
| MS-RR-P03 | D | major | followup `request_repeat_mri_3months`.output.additional_observations | MRI report explicitly performs the diagnostic synthesis: "Now meets McDonald 2017 criteria for dissemination in space (periventricular and juxtacortical) and dissemination in time (new lesions on follow-up)" | FLAGGED | per brief, McDonald DIS/DIT → MS verdict is the agent's job; this is the clearest residual Kind-1 leak. Left for human adjudication (do not fix per condition instruction to flag synthesis) |
| MS-RR-RM03 | D | minor | initial_tool_outputs.mri.additional_observations[1] | MRI report cites the exam: "The pontine lesion location correlates with the clinical finding of left abduction deficit (left VI nerve fascicular involvement)" — cross-modality reference (guide prohibition #1) | FLAGGED | within-imaging localization is fine; the exam citation is the leak. Conservative flag (strip-vs-keep is a judgment) |
| MS-RR-RP03 | D | minor | followup `request_repeat_mri_3months`.output.impression | MRI impression names the treatment regimen: "...following 5-day course of IV methylprednisolone 1g/day" (management in a report; guide prohibition #3) | FLAGGED | "interval improvement" comparison is legitimate; only the drug/dose/duration clause is the issue |
| MS-RR-RM01 | B | minor | initial_tool_outputs.ecg | interpretation "Sinus tachycardia, rate 90 bpm" contradicts rhythm/findings ("Normal sinus rhythm"); rate 90 is not tachycardic (>100) | FLAGGED | appended to metadata.case_body_concerns; incidental ECG in an MS workup; not auto-fixed (which field to keep is a judgment) |
| MS-RR-RM03 | B | minor | followup_outputs[0] (VEP) findings[0].reference_range vs impression | left-eye P100 finding ref "<100 ms" (value 106 flagged abnormal) vs impression ref "<115 ms, borderline"; thresholds disagree and flip the abnormal call | FLAGGED | appended to metadata.case_body_concerns; VEP P100 threshold (100 vs 115 ms) is lab-dependent — not auto-fixed |
| MS-RR-RP01 | C/E | minor | followup `request_vep`.output.findings | a `test_type: vep` report contains "Wave I-V interpeak latency" rows — that is a BAEP (auditory) parameter, not a visual evoked potential measure | FLAGGED | mislabeled parameter inside the VEP report; P100 rows are correct |
| MS-RR-P02, P03 | B | minor | followup `request_somatosensory_evoked_potentials`.tool_name | SSEP delivered via `interpret_labs` (LabResults "SSEP" panel) rather than `order_specialized_test` (test_type ssep) | FLAGGED | structurally valid but clinically odd routing; consistent design choice across cases |
| MS-RR-RP01 | B | minor | followup `request_ct_body`.tool_name | CT chest/abdomen/pelvis + mammography delivered via `interpret_labs` (narrative in lab `value` fields) instead of an imaging tool | FLAGGED | appropriate malignancy/sarcoid exclusion content; odd tool routing only |
| MS-RR-RM02, RP01 | B | minor | followup MR-spectroscopy routing | RM02 routes MR spectroscopy through `analyze_brain_mri` (spectroscopy crammed into an MRIFinding); RP01 uses `order_advanced_imaging` (modality MR_spectroscopy) for the same purpose | FLAGGED | inconsistent modeling of the same test across cases; both schema-valid |
| MS-RR-RM01, RM02, RP02, P02, P03 | A/E | nit | followup biopsy/SSEP/CT via interpret_labs `interpretation` | auto-generated lab interpretation strings read awkwardly for free-text "values" and contain double-space before "(H)" (e.g. "...myelin debris  (H)") | FLAGGED | cosmetic auto-generation artifact; not edited |
| MS-RR-RS01 | E | nit | followup `request_oct`.output / VEP | non-numeric values got a unit suffix: "Limited signal quality micrometers", "Unable to reliably test ms" (consistent with the patient's amblyopic left eye) | FLAGGED | cosmetic template artifact; clinically coherent with longstanding left amblyopia; not edited |
| MS-RR-M01, M02, RM03 (initial MRI), and others | D | minor | initial_tool_outputs.mri.impression | several MRI impressions use McDonald terminology ("involves at least three of four typical MS regions"; "suggests dissemination in time") | FLAGGED | borderline: simultaneous enhancing+non-enhancing is a within-MRI observation, but "dissemination in time / N of 4 MS regions" edges into McDonald synthesis. Consistent authoring style; reviewer to decide |
| MS-RR-RS01 | C | minor | patient + ground_truth.primary_diagnosis / difficulty | 61 y/o man, HTN/dyslipidemia/ASA, acute brainstem syndrome (gaze palsy + peripheral CN VII) labelled `straightforward` MS; late-onset MS is a pack red-herring category and vascular causes loom large at this age | FLAGGED | gold is defensible (multiple Dawson-finger + enhancing lesions, cord lesion, 5 OCBs), but "straightforward" undersells the age/vascular confound — reviewer to confirm |
| MS-RR-S04 | D | nit | initial_tool_outputs.csf.interpretation | MBP line adds "consistent with active demyelination" | KEPT | within-CSF pattern read on a demyelination biomarker; acceptable per guide (not a final clinical diagnosis) |
| MS-RR-RM01, RM02, RP01, RP02, RP03 | D | info | followup brain-biopsy histology / MR spectroscopy / perfusion impressions | biopsy (demyelination, Creutzfeldt cells, mixed CD3/CD20 infiltrate); MRS within-imaging read ("favor tumefactive demyelination... cannot exclude neoplasm"); perfusion rCBV read | KEPT | confirmatory histology + within-imaging reads, KEPT per style guide; impressions correctly hedge and recommend tissue/clinical correlation |
| MS-RR-P02, P03, RM03, RS01, S04 | D | info | followup `search_medical_literature`.summary/results | OCB-negative MS prevalence; sixth-nerve palsy in MS; late-onset MS; DMT guidance; migraine-vs-MS WML morphology | KEPT | population-keyed evidence (Kind-2); the 5 leakage-detector hits matching "multiple sclerosis" are all of this kind plus the P01 "not classic for MS" MRI negation |
| (all 20) | D | info | initial_tool_outputs.mri findings/impression; csf OCB/IgG index | demyelinating lesion morphology, open-ring enhancement, Dawson fingers, T1 black holes; CSF oligoclonal bands + IgG index | KEPT | explicitly designated KEPT by the brief; MRI impressions hand off with "Clinical correlation recommended" rather than declaring MS (except the P03 synthesis flagged above) |

## Internal-consistency spot checks (all passed unless flagged above)

- Patient age/sex used consistently across HPI, exam, and every report in all 20 cases.
- Every numeric lab `is_abnormal` flag verified consistent with its stated reference
  range across all 20 cases (programmatic check, 0 mismatches). ANA 1:40/1:80 handled
  per-case: flagged abnormal where described "low positive" against "Negative (<1:40)",
  not flagged where given as "<1:40 = negative" — internally consistent in each case.
- AQP4-IgG and MOG-IgG negative (cell-based assay) in every case; mimic serology
  (NMOSD/MOGAD/sarcoid/lupus/infectious) appropriately excluded.
- Spinal-cord lesions consistently short-segment (<2 vertebral bodies), peripheral —
  correctly favoring MS over NMOSD's LETM; no longitudinally extensive lesions in any MS case.
- CSF glucose ratios recompute correctly against paired serum after the 3 fixes
  (e.g. M03 62.3/92=0.68; RM01 58/118=0.49; S02 68/86=0.79); opening pressures normal (13–18).
- Differentials sorted by likelihood descending; all likelihood/category/severity enums valid in all 20.
- ground_truth.optimal_actions / useless_tools / contraindicated_actions match the
  criteria-pack workup hierarchy and DMT-safety rules (JCV/natalizumab, fingolimod ECG,
  teriflunomide teratogenicity, live-vaccine timing); citations within the pack allow-list.

## Tally

- Cases audited: 20 / 20 (every field of every case read).
- Findings by severity: 0 blocker; 1 major (P03 McDonald-synthesis leak in MRI report, FLAGGED);
  12 minor; 3 nit; plus KEPT/info rows.
- Fixed: 16 file-level edits across 11 cases — OCT "um um" duplicated unit (9 cases),
  RP02 "micrometers" duplicated unit (1 case), 3 CSF glucose-ratio arithmetic corrections
  (M01/M02/P01), 1 MRI dorsal→lateral cord wording (RM02). Plus case_body_concerns notes
  appended to RM01 (ECG) and RM03 (VEP threshold).
- Flagged (not fixed): the 1 major + all minor/nit judgment items above.
- Files touched: MS-RR-M01, M02, M03, P01, P02, P03, RM01, RM02, RM03, RP01, RP02 only.
  Coherence 0 and schema valid re-confirmed on every edited file after edits; em-dash /
  unicode convention and trailing newlines preserved; no non-MS-RR file modified by this audit.

## Top clinical flags for human adjudication

1. **MS-RR-P03** — the 3-month repeat-MRI report's `additional_observations` literally
   states the case meets McDonald 2017 DIS and DIT. This is the diagnostic synthesis the
   benchmark expects the agent to perform; it should be rewritten to a within-imaging
   observation (new juxtacortical + new enhancing lesion vs prior) or removed.
2. **MS-RR-RM03 / RP03** — residual report-level leaks: RM03 MRI cites the exam abduction
   deficit (cross-modality); RP03 MRI names the steroid regimen (management). Decide
   whether to strip to within-imaging language.
3. **MS-RR-RM01** — incidental ECG calls rate 90 "sinus tachycardia" while its own
   rhythm/findings say normal sinus; 90 is not tachycardic. Pick one consistent reading.
4. **MS-RR-RM03** — VEP left-eye P100 reference is "<100 ms" in the finding but "<115 ms"
   in the impression, which flips whether 106 ms is abnormal vs borderline. Set one threshold.
5. **MS-RR-RP01** — VEP report includes "Wave I-V interpeak latency" (a BAEP/auditory
   parameter) inside a visual evoked potential study; remove or relabel.
6. **MS-RR-RS01** — 61 y/o man with vascular risk factors and an acute brainstem syndrome
   labelled "straightforward" MS. Gold is supported by the imaging/CSF burden, but confirm
   the difficulty label and that late-onset MS (not vascular) is the intended best answer.
