# FEPI-TEMP-RS05
Reviewer status: no reviewer notes for FEPI-TEMP (R1 and R2 never reviewed this condition in a notes round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: the July 2026 tool guidance for focal_epilepsy_temporal via plans/FEPI-TEMP.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.mri` (classes E, U) | "Reduced by approximately 28%" with 1.9 vs 3.2 cm3 (41%); asymmetry index +0.25 for a smaller left hippocampus although the condition's definition is (L - R)/(L + R) (gives -0.25); gadolinium lines in an HS case; threshold teaching. | FIXED: size "41% smaller"; index -0.25 ((L - R)/(L + R)); technique line, no gadolinium; numbered impression. Volumes kept (RS04 moved to 1.7 and S04 to 1.8, so 1.9 is now unique to this case). |
| C | major | `initial_tool_outputs.labs` (class M) | Prolactin 42.6 about 7 h after the seizure, flagged abnormal (fact 11); commentary inside `abnormal_values_summary`. | FIXED: prolactin row and mentions deleted; summary and interpretation in panel voice. Red herring path `initial_tool_outputs.labs.panels.BMP[6]` verified (glucose 138). |
| B | minor | `initial_tool_outputs.eeg` (class K) | Limitations "Prolonged monitoring recommended if clinical evaluation warrants"; sharp waves "every 2-3 minutes" called frequent (ACNS: occasional). | FIXED: recording's own limits; frequency 1-2 per minute. |
| D | minor | `initial_tool_outputs.ecg` | Template `clinical_correlation` ("does not diagnose epilepsy") and an interpretation about loss of consciousness (cross-modality). | FIXED: empty correlation; categorical interpretation with rate. |
| B | minor | `fallback_tool_outputs.ecg` | A second, different ECG (rate 84) stored as fallback while the initial ECG exists. | FIXED: fallback set to null; `metadata.fallback_tool_kinds.ecg` removed. |
| D | major | `followup_outputs` literature (classes A, O) | "Glauser ... updated Epilepsia 2017;58:1235-1268" (does not exist); "lamotrigine and levetiracetam Level A, oxcarbazepine Level A" (wrong, fact 6); Engel 2003 with an invented title. | FIXED: Glauser 2013 with correct levels, SANAD II 2021, Fisher 2014 definition, Fisher 2017 classification, all with real titles; general summary; query reworded; trigger `search_literature_initial_monotherapy_focal_seizures`; last in the pathway. |
| C | minor | `followup_outputs` drug check | Quoted the patient's creatinine; mood warning tied to "diabetes-related stressors"; no sulfonamide-zonisamide or HLA content. | FIXED: interactions with metformin and amlodipine; zonisamide contraindicated with sulfonamide allergy; HLA-B*15:02 and sodium for carbamazepine and oxcarbazepine; renal threshold stated generally. |
| A | major | `ground_truth.action_criteria` (classes A, B, D, E, H, T) | MRI `{contrast: true, protocol: epilepsy}`; literature and drug check required; ECG required with template evidence; labs optional with the template; doubled citations; rationales equal labels. | FIXED: order labs, ECG, MRI, EEG, drug check, literature. Labs recommended (glucose, sodium, calcium) [NICE_NG217_2025]; ECG optional; MRI `{protocol: epilepsy}` required [ILAE_MRI_2019]; routine EEG required [IFCN_ILAE_EEG_2023]; drug check optional [CPIC_2018]; literature optional [SANAD2_2021]; case-specific text. |
| A | minor | `ground_truth.sequence_constraints`, `.stop_rule` (classes C, D) | Template MRI -> drug check constraint with the drug check now optional; stop rule with literature, drug check and ECG, max 0. | FIXED: constraint deleted; stop rule MRI, EEG, max 2. |
| C | major | `ground_truth.assessment` (class L) | Musts were insight or work-up steps (recognize aura, 3T MRI, confirm concordance, verify glucose); oxcarbazepine prohibition; generic LP prohibition; duplicated driving lines; no HLA, SUDEP or valproate line. | FIXED: musts: first-line lamotrigine or levetiracetam, HLA-B*15:02 before carbamazepine or oxcarbazepine, sodium monitoring if they are used, driving, SUDEP. Prohibitions: reflux attribution (kept), valproate (canonical, he is 52), zonisamide (sulfonamide allergy). |
| C | minor | `ground_truth.differential` (class P) | "First unprovoked seizure of unknown etiology" is not an alternative once the auras are recognized; panic attacks (raised by "work stress" and fear) absent; hypoglycemia ICD with coma. | FIXED: panic attacks and convulsive syncope `low`; hypoglycemia (E11.649), PNES, genetic generalized epilepsy `very_low`; each names the excluding finding. |
| C | major | `ground_truth.key_clinical_evidence` (classes G, plan RS05) | "ILAE 2017 criteria ... even after a single convulsion" (the recurrent auras already meet the two-seizure definition); overstated amlodipine interaction; engineering lines. | FIXED: five statements; definition per [ILAE_def_2014]; amlodipine line replaced by the HLA and interaction choice. |
| C | minor | `ground_truth.avoided_actions` (class I) | Template rationales. | FIXED: case-specific rationales; CT waste kept (back to baseline, no head injury or anticoagulation, MRI available). |
| E | minor | `ground_truth.red_herrings[0]` | `location` contained an em dash; intended effect named hypoglycemia for a high glucose. | FIXED: location `labs`; effect and interpretation reworded. |
| E | minor | `patient.history_present_illness` (class R) | Duplicate surname Sharma (M04). | FIXED: Mr. Deshpande (used nowhere else in the dataset). |
| A | minor | `fallback_tool_outputs.echo` (class I) | No `echo_type`. | FIXED: `TTE`. |
| B | minor | `metadata.difficulty_rationale` | "Five required tools (... literature search, drug interactions)". | FIXED: reflects the new tiers. |

## Changes, in one paragraph a physician can read before re-reviewing

Mr. Deshpande (renamed), 52, South Asian, with diabetes on metformin, hypertension on amlodipine and a sulfonamide allergy, had a first focal to bilateral convulsion after 12-14 months of deja vu and epigastric auras attributed to reflux. Those recurrent focal seizures already meet the definition of epilepsy. The required epilepsy-protocol MRI shows left hippocampal sclerosis (volumes and asymmetry index now consistent, no gadolinium) and the required routine EEG shows left anterior temporal sharp waves with TIRDA. Glucose and electrolytes are recommended (glucose 138, the red herring); ECG, the drug review and literature are optional; prolactin is gone and the literature now cites real sources with correct evidence levels. Management: lamotrigine or levetiracetam first line, HLA-B*15:02 before carbamazepine or oxcarbazepine with sodium monitoring if they are used, driving and SUDEP counselling; no valproate (under 55), no zonisamide (sulfonamide allergy), and no attribution of the auras to reflux.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys not yet in the pack allow-list: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`, `[CPIC_2018]`, `[SANAD2_2021]`, `[ILAE_def_2014]` (plan request 2).
- Synonyms (plan request 6): the inherited idiopathic codes G40.009/G40.019 do not fit structural epilepsy.
- `perfect_agent.py` prints `<- ?` for the labs criterion (the `exclude_none` comparison in `_source`); the stored labs output is the one served.

## Open questions for Andrea (judgment calls you could not settle)

- Decided: the asymmetry index sign was corrected to -0.25 to follow the (L - R)/(L + R) definition the plan fixes for the condition (RS01 uses the same convention for a smaller left hippocampus).
- Decided: a zonisamide prohibition was added (not in the plan) because zonisamide is a sulfonamide and its label contraindicates it in sulfonamide hypersensitivity; the drug check stays optional because no first-line choice is affected.

## Verification

Adversarial verifier, 24 Oct 2026. Checked the log against the case file and `git diff master`. Tiers (MRI, routine EEG required; labs recommended; ECG, drug check, literature optional), no constraints and the stop rule (MRI, EEG; `max_additional_actions: 2`, as plan 3.4 sets) match the plan. Volumetrics (1.9 vs 3.2 cm3: 41%, index -0.25), the red herring `labs.panels.BMP[6]` (glucose 138), the HLA-B*15:02 must, the sulfonamide allergy against the zonisamide prohibition, the Glauser 2013 levels and the Fisher 2014 and 2017 sources hold. Guards pass.

Found and fixed:
- `initial_tool_outputs.eeg.findings[0].morphology`: "Sharp waves" with "duration 40-70 ms" (spike range); now 80-150 ms.
- `followup_outputs` literature, SANAD II finding: "neither levetiracetam nor zonisamide was non-inferior for 12-month remission" misstates the trial (zonisamide was non-inferior in the intention-to-treat analysis, not per protocol). Corrected.
- `followup_outputs` drug check: "mild CYP3A4 induction" was attributed to carbamazepine as well as oxcarbazepine; carbamazepine is a strong inducer. Reworded.
- `initial_tool_outputs.ecg`: PR 154, QRS 86, QTc 416 at 76/min were identical to RP05 (and M02, RM04, S05), and 76/min was 10 beats below the triage rate of 86. Now 84/min, PR 168, QRS 92, QTc 428; the ECG criterion `expected_evidence` says 84/min.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-4-search-medical-literature.label`: "Optional" prefix removed.

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added), mesial temporal sclerosis epilepsy; removed focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that contradicts this case now get a case-specific report (term: gist, where stored):

- analyze_eeg ambulatory: This is an ABNORMAL 48-hour ambulatory EEG due to: 1. Left anterior temporal sharp waves (phase reversal at F7), maximal in NREM sleep. 2. Left tempor (fallback_tool_outputs.eeg)
- analyze_eeg video: This is an ABNORMAL 72-hour video-EEG due to: 1. Left anterior temporal sharp waves (phase reversal at F7), maximal in NREM sleep. 2. Left temporal in (followup request_video_eeg)
- order_advanced_imaging FDG_PET: 1. Left mesial temporal hypometabolism with milder extension into the lateral temporal neocortex. 2. Normal metabolism elsewhere. Clinical correlation (fallback_tool_outputs.advanced_imaging)
- obtain_tissue_diagnosis resection: Hippocampal sclerosis, ILAE type 1 (fallback_tool_outputs.tissue_diagnosis)
- obtain_tissue_diagnosis stereotactic_biopsy: Hippocampal neuronal loss with fibrillary gliosis (followup request_stereotactic_biopsy)
- obtain_tissue_diagnosis open_biopsy: Hippocampal neuronal loss with fibrillary gliosis (followup request_open_biopsy)
- order_specialized_test neuropsych_battery: Weakness in verbal learning and delayed verbal recall (T-scores 35 and 32) with visual memory within the average range and intellectual functioning in (fallback_tool_outputs.specialized_test)
- interpret_labs AED_levels: No levetiracetam, valproate, carbamazepine, phenytoin, lamotrigine or lacosamide detected. (fallback_tool_outputs.labs[AED_levels], also answers valproate_level)
- order_echocardiogram TEE: 1. Mild left atrial enlargement. 2. Preserved left ventricular systolic function. 3. No intracardiac thrombus. Clinical  (followup request_tee)

Checks: `perfect_agent.py` passes; the criterion snapshot of the case is unchanged; `pytest agent-platform/tests -k FEPI-TEMP` (case guards included), `test_reports_do_not_fabricate.py` and `apply_diagnosis_synonyms.py --check` pass; no new report repeats a 60-character window of any criterion's expected evidence.
