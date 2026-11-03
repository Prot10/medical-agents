# VASC-DEM-S04
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The condition has no reviewer notes. The plan's classes (C1-C7, C13, C14, C16, C18, C19 and the S04 index entry) were applied as classes (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | ground_truth.action_criteria[action-5-analyze-brain-mri].alternatives | Non-schema `sequences` key plus `protocol`/`contrast`: no real call could match (C1). | FIXED: `analyze_brain_mri {}`; label and rationale rewritten. |
| D | major | action-7-search-medical-literature; initial and fallback literature_search | Literature criterion leaking its expected evidence into its own output (C2). | FIXED: criterion deleted, initial null, fallback deleted. |
| C | minor | action-8-check-drug-interactions; fallback_tool_outputs.drug_interactions | Generic drug check and fallback (C3 group D). | FIXED: deleted. |
| D | major | patient.neurological_exam.mental_status | Gave the Punjabi-adapted MoCA 20/30 and item losses (C4). | FIXED: bedside observation with interpreter, "Formal cognitive screening reported separately". |
| D | minor | patient.neurological_exam.sensory | "consistent with diabetic polyneuropathy" resolves the red herring in the exam. | FIXED: findings only. |
| D | major | initial_tool_outputs.clinical_assessment (impression, criteria_met) | "excludes a linguistic artefact", "Instrumental independence has been lost"; IADL and executive verdicts in criteria_met (C5). | FIXED: scores-only impression; criteria_met keeps first-language administration, impairment and cueing. |
| B | minor | initial_tool_outputs.clinical_assessment (findings, scores) | Listed losses gave raw 21 (22 corrected), not 20. | FIXED: full domains 2+3+3+2+1+2+6 = raw 19, plus 1 for 5 years of education = 20 (serial subtraction 1/3, abstraction 1/2 made explicit; orientation 6/6 as in the exam). |
| D | major | followup_outputs[gait].output (impression, Romberg row) | Impression attributed components to "small-vessel disease" and "diabetic polyneuropathy" (cross-modality synthesis); Romberg row "sensory contribution" (C5). | FIXED: observations only; cadence 134 steps/min added (33 cm at 0.74 m/s); TUG normal value stated. |
| D | major | initial_tool_outputs.specialized_test.impression | "the profile is subcortical ... Neither literacy nor language explains the pattern" (C5). | FIXED: profile wording. |
| B | minor | initial_tool_outputs.labs | Template values (WBC 6.8, Hct 41.6, Plt 238, MCV 88, Na 139, K 4.2, ALT 22, albumin 4.1, folate 11.8); male creatinine range; eGFR ">60"; HDL ">40" in a woman; uACR `clinical_significance` "established diabetic microvascular disease"; interpretation "confirms", "excluding hypothyroid", "warrants correction" (C6). | FIXED: varied values (Na 136 on indapamide), female ranges (HDL ">50", 40 stays flagged), clinical_significance null, pattern-level interpretation. eGFR 58 checked against creatinine 1.04 at 69 (CKD-EPI 2021 about 58). |
| C | major | ground_truth (new action-9-interpret-labs-mma), followup_outputs[1] | B12 244 pg/mL after 22 years of metformin with an established polyneuropathy, called "a contributor to correct" without any test that shows functional deficiency (the same class as ALZ-EARLY S03). | FIXED: recommended MMA criterion and follow-up (MMA 0.52 umol/L, homocysteine 17.8 umol/L, both raised); soft constraint labs before MMA; B12 replacement must; differential and key evidence updated. |
| D | major | initial_tool_outputs.mri (impression, observations) | "of diabetic and hypertensive type ... The burden accounts for the cognitive syndrome"; "no abnormal enhancement" in a non-contrast study (C5). | FIXED: numbered STRIVE-2 impression. |
| D | minor | fallback_tool_outputs (advanced_imaging, labs, ct, echo, cardiac_monitoring) | Off-pathway revealing text; echo "No cardioembolic source identified"; Holter average 72 vs her 82 (C7). | FIXED: advanced_imaging and labs deleted; CT rewritten for this patient; echo neutral with echo_type TTE; Holter average 80. metadata.fallback_tool_kinds updated. |
| C | major | ground_truth.assessment | Musts restated the scored work-up; "bring glycaemia, blood pressure and lipids to target" without targets (C19). | FIXED: deficit genuine on first-language testing; BP below 130/80 gradually with orthostatic checks [ESO_2021_SVD]; HbA1c about below 8.0% intensified with a low-hypoglycaemia agent [ADA_2025_older_adults]; high-intensity statin (LDL 108 on rosuvastatin 10 mg); B12 replacement [BSH_B12_2014]; both gait components; family support through the interpreter. Prohibition added: no antiplatelet for covert SVD alone [ESO_2021_SVD]. |
| A | minor | all criteria citations and rationales | Unbracketed duplicates; rationale equal to label (C13). | FIXED. |
| C | minor | avoided_actions rationales | Generic text; "MRI already obtained" (C18). | FIXED: case-specific; CT rationale per plan. Echo and monitoring waste kept (no clinical stroke). |
| C | minor | criteria order, stop_rule (C16) | | FIXED: screen, gait, neuropsych, labs, MMA, MRI; screen before MRI kept; max_additional_actions 1. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis unchanged (subcortical ischaemic vascular dementia on long-standing diabetes and hypertension, with diabetic polyneuropathy contributing to the gait disorder). The exam no longer gives the MoCA; the screen adds up to 20/30 with the education point and states only scores. The gait, neuropsychology and MRI reports describe their findings without attributing them. Labs use female ranges and list the flagged values. A recommended methylmalonic acid test is added for her B12 of 244 pg/mL on 22 years of metformin with neuropathy; it is raised (0.52 umol/L, homocysteine 17.8), so B12 replacement is now a must. The literature and drug-check steps are gone. Musts give her targets: BP below 130/80 lowered gradually, HbA1c about below 8.0% intensified without sulfonylurea or insulin, a high-intensity statin, falls and neuropathy measures and family support; a prohibition on an antiplatelet for covert small-vessel disease is added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.1): remove F06.7 from the F01 codes of this dementia case.
- Citation keys: `[BSH_B12_2014]` (already used in ALZ-EARLY) and `[ADA_2025_older_adults]` need allow-listing in the VASC-DEM pack.

## Open questions for Andrea (judgment calls you could not settle)
None. Note for the lead: the MMA criterion is an addition beyond the plan, made for the same reason as ALZ-EARLY-S03 (low-normal B12 on metformin with neuropathy).

## Verification
Adversarial verifier, 24 Oct 2026. Checked every Own-findings row against the file and the git diff: MRI `{}`; literature and drug check gone; Punjabi-adapted MoCA domains give raw 19 plus 1 = 20 and the lost points (3+3+3+1+1) agree, orientation 6/6 as in the exam; gait 33 cm at 134 steps/min gives 0.74 m/s and the Romberg agrees with the exam; female ranges, HDL 40 flagged, eGFR 58 follows from creatinine 1.04 at 69 (CKD-EPI 2021 about 58); the added MMA criterion (recommended, `{"panels": ["MMA"]}`) is served by its follow-up, follows the core labs (soft), and its raised result is reflected in the differential, the key evidence and the B12 must. The addition is clinically sound (B12 244 pg/mL is indeterminate; 22 years of metformin with a neuropathy). HbA1c must (about below 8.0%, intensify from 8.9% without sulfonylurea or insulin) follows ADA 2025 Older Adults. Guard tests pass. No clinical or consistency error found.
Changed: `fallback_tool_outputs.echo` LVEF 60% to 63% (identical fallback text across S01-S05, template carry-over). `[BSH_B12_2014]` and `[ADA_2025_older_adults]` remain CENTRAL allow-list requests as the worker logged.
Re-ran `perfect_agent.py -v` (pass) and `case_io.py check` (clean for this case).

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Total cholesterol]` | Total cholesterol 198 mg/dL did not equal LDL + HDL + TG/5 (185.2); the same lab-arithmetic class was fixed in M07-M10, P01, P02 and S06-S11 but not here. | FIXED: total cholesterol 185 mg/dL (flag unchanged; LDL, HDL and TG, which the musts and evidence quote, unchanged). |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here subcortical small-vessel labels and F01.2/I67.3. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `[ADA_2025_older_adults]` -> `[ADA_older_adults_2026]` in the HbA1c must (same target below about 8.0%; superseded edition, as in ALZ-EARLY).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

A fresh order of each study below was answered by the benchmark-level normal library, which contradicted this patient (age, rhythm, devices, surgery, stored findings). Each now has a case-specific report:

- FDG_PET: Bilateral frontal hypometabolism with reduced left thalamic and right putaminal uptake; posterior association cortex preserved. The pattern is consistent with subcortical small-vessel disease. (fallback_tool_outputs.advanced_imaging)
- perfusion_SPECT: Bilateral frontal hypoperfusion with reduced left thalamic and right putaminal uptake; posterior association cortex preserved. The pattern is consistent with subcortical small-vessel disease. (followup request_perfusion_spect)
- performance_status: Karnofsky 60 (requires occasional assistance but able to care for most needs), ECOG 2 (ambulatory and capable of all self-care, unable to carry out any work activities). (fallback_tool_outputs.clinical_assessment)
- exercise_stress_test: Very low workload (2.8 METs) limited by gait; submaximal heart rate, non-diagnostic for ischaemia. (fallback_tool_outputs.specialized_test)
- levodopa_challenge: MDS-UPDRS III 18/132 OFF and 18/132 ON (0% change), below the 30% threshold for a clinically meaningful levodopa response. (followup request_levodopa_challenge)
- TEE: Mild concentric left ventricular hypertrophy; aortic valve sclerosis without stenosis. No patent foramen ovale and no left atrial appendage thrombus. (followup request_tee)
- emg_ncs: Length-dependent sensorimotor polyneuropathy, predominantly axonal with mild conduction slowing, of moderate severity. (followup request_emg_ncs)
- ssep: Delayed lower-limb responses with normal central conduction times, indicating peripheral slowing in the legs; upper-limb and central pathways normal. (followup request_ssep)
- skin_biopsy_iencf: Reduced distal intraepidermal nerve fibre density with a length-dependent gradient. (followup request_skin_biopsy_iencf)
- DTI_tractography: Diffusely reduced white matter fractional anisotropy without tract interruption. (followup request_dti_tractography)
- urinalysis: glucose 3+ and protein trace on an SGLT2 inhibitor (fallback_tool_outputs.labs[urinalysis])
- homocysteine: 17.8 umol/L, as in the stored metformin work-up (fallback_tool_outputs.labs[homocysteine])

Checks: `perfect_agent.py` pass; `test_case_guards.py -k VASC-DEM-S04` pass; criterion outputs unchanged against the pre-pass snapshot; no 60-character window of any expected_evidence in the new reports; synonym guard 0 changes.
