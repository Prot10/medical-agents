# FEPI-TEMP-RS01
Reviewer status: no reviewer notes for FEPI-TEMP (R1 and R2 never reviewed this condition in a notes round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: the July 2026 tool guidance for focal_epilepsy_temporal via plans/FEPI-TEMP.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.mri` (class F) | The 1.3 x 1.6 cm sessile tuber cinereum lesion was called "Hypothalamic mass" and never named; the impression omitted it ("Post-gamma knife treatment changes") and called the HS "suggesting" with only "subtle" signal; post-radiosurgery hemosiderin described as T1 hyperintensity; asymmetry "22.7%" (2.41 vs 3.12 is 22.8%) with a teaching threshold. | FIXED: 3T epilepsy-protocol MRI with thin hypothalamic sections; finding and impression state the residual non-enhancing sessile lesion consistent with hypothalamic hamartoma (Kind 2) and definite left HS (atrophy, T2/FLAIR hyperintensity, loss of internal architecture, temporal horn enlargement); hemosiderin on SWI only; asymmetry index -0.13 ((L - R)/(L + R)), 22.8%; comparison with an outside standard MRI; canonical post-contrast line (lesion case). |
| B | major | `followup_outputs` video-EEG | The label rests on a temporal epileptogenic zone, but the video-EEG captured only gelastic seizures and one focal to bilateral seizure; the habitual temporal-type seizures of the HPI (2-4/week) and any interictal temporal activity were absent; limitations recommended intracranial monitoring. | FIXED: two habitual focal impaired-awareness seizures with F7/T3 onset (epigastric aura, lip smacking, swallowing, right-hand fumbling) and interictal left anterior temporal sharp waves added; impression in numbered style; limitations "Surface EEG has limited sensitivity for deep midline seizure onset"; intracranial EEG moved to a must. |
| C | major | `followup_outputs` drug check | "Valproic acid + clonazepam: may increase clonazepam levels by inhibiting CYP3A4" (wrong mechanism); "FDA category X" and contraception counselling written for pregnancy in a man; no paternal valproate warning. | FIXED: valproate-clonazepam additive sedation and the labelled absence-status warning; valproate monitoring; MHRA/EMA 2024 paternal-exposure advice; clonazepam withdrawal; levetiracetam mood; HLA-B*15:02 before any carbamazepine or oxcarbazepine; oxcarbazepine and clobazam alternatives removed; trigger `check_current_asm_regimen_interactions`. |
| D | major | `followup_outputs` literature (class O) | Unverifiable sources (2020-2023 "meta-analysis", "10-year experience", Berkovic "Brain 2020") with invented percentages, query naming the lesion. | FIXED: general summary on surgery for drug-resistant focal epilepsy from Kwan 2010, Wiebe 2001, Engel 2012 (ERSET), Engel 2003; trigger `search_drug_resistant_focal_epilepsy_surgery`; last in the pathway. |
| D | minor | `followup_outputs` FDG-PET | Named the "hypothalamic hamartoma" and reported interictal hypermetabolism; no tracer line. | FIXED: "Hypothalamic lesion isometabolic to adjacent gray matter"; no extratemporal hypometabolism added; tracer "18F-FDG, interictal". |
| B | minor | `fallback_tool_outputs.ct` | Fallback CT "No ... mass" in a patient with a 1.3 x 1.6 cm hypothalamic lesion. | FIXED: isodense non-calcified hypothalamic lesion without hydrocephalus; MRI recommended. |
| A | minor | `fallback_tool_outputs.echo` (class I) | No `echo_type`. | FIXED: `TTE`. |
| A | major | `ground_truth.action_criteria` (classes A, B, D, E, H) | MRI `{contrast: true, protocol: epilepsy}`; literature and drug check required with template evidence; PET recommended; doubled citations; rationales equal labels. | FIXED: MRI `{protocol: epilepsy}` and video-EEG required; PET, drug check, literature optional; one key each ([ILAE_MRI_2019], [IFCN_ILAE_EEG_2023], [Willmann_2007], [NICE_NG217_2025], [Engel_2003]); case-specific labels, rationales and evidence; order MRI, video-EEG, PET, drug check, literature; follow-ups reordered the same way. |
| A | minor | `ground_truth.sequence_constraints`, `.stop_rule` (classes C, D) | Template MRI -> drug check constraint; stop rule with literature and drug check, max 0. | FIXED: constraint deleted; stop rule MRI and video-EEG, max 2. |
| C | major | `ground_truth.assessment` (class L) | Musts were work-up steps (dedicated MRI, video-EEG, FDG-PET); prohibitions were generic (primary generalized epilepsy, LP before imaging); no SUDEP, driving or valproate counselling. | FIXED: musts: presurgical referral (canonical drug-resistance line), treatment options for both lesions with possible intracranial EEG, endocrine review, MHRA/EMA 2024 paternal valproate counselling, SUDEP, driving; prohibitions: ASM escalation as the only plan, abrupt clonazepam withdrawal. |
| C | major | `ground_truth.differential` (class P) | Isolated mesial TLE `moderate` with a hamartoma on MRI. | FIXED: `low`; each entry names the excluding finding (LGS: normal cognition, focal onsets). |
| D | minor | `ground_truth.key_clinical_evidence` (classes G, S) | Engineering lines; "Neuropsych and FDG-PET inform surgical risk" (no neuropsychology output); generic statements. | FIXED: five case-specific statements. |
| C | minor | `ground_truth.avoided_actions` (class I) | Shared template rationales. | FIXED: case-specific rationales; CT waste kept (elective, MRI available). |
| E | minor | `patient.history_present_illness` | "epilepsy was formally diagnosed at age 4. By age 3, he also developed drop attacks" (sequence reads backwards); "secondarily generalizes". | FIXED: "From age 3 he also had drop attacks"; "evolves to a bilateral tonic-clonic seizure". |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale`, `.case_body_concerns` | Stale "Straightforward case ... minimal confounders" flagged by an AUDIT-FLAG; rationale cited neuropsychology. | FIXED: description and rationale rewritten to the case; the resolved AUDIT-FLAG entry removed. |

## Changes, in one paragraph a physician can read before re-reviewing

This 22-year-old man has had gelastic seizures since infancy, drop attacks from age 3, gamma knife radiosurgery of a hypothalamic lesion at 5 and treated central precocious puberty, and now 2-4 temporal-type focal impaired-awareness seizures a week (epigastric aura, oral automatisms, right-hand fumbling) with monthly bilateral convulsions despite valproate, clonazepam and levetiracetam. The required epilepsy-protocol MRI now states the residual sessile non-enhancing tuber cinereum lesion consistent with hypothalamic hamartoma and a definite left hippocampal sclerosis with correct volumetrics; the required video-EEG captures gelastic seizures with a deep midline pattern and, separately, two habitual focal impaired-awareness seizures and one focal to bilateral seizure of left anterior temporal onset with interictal left temporal sharp waves, which is what the dual-pathology label needs. FDG-PET (left temporal hypometabolism, hypothalamic lesion isometabolic), the drug review (correct valproate-clonazepam interaction, paternal valproate advice) and a correctly sourced literature search are optional. Management: presurgical referral for drug-resistant epilepsy with treatment options for both lesions and possible intracranial EEG, endocrine review, valproate counselling for a young man (MHRA/EMA 2024), SUDEP and driving counselling; prohibitions against ASM escalation alone and abrupt clonazepam withdrawal. Isolated mesial TLE is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan request 6): the inherited idiopathic codes G40.009/G40.019 do not fit structural dual-pathology epilepsy.
- Citation keys not yet in the pack allow-list: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]` (plan request 2). The paternal valproate statement cites MHRA and EMA 2024 in prose; a key such as `[MHRA_VPA_2024]` would cover it.

## Open questions for Andrea (judgment calls you could not settle)

- Decided: the video-EEG gained two habitual temporal-type seizures and interictal left temporal sharp waves. The label ("focal epilepsy of left temporal lobe origin with mesial temporal sclerosis ... dual pathology") needs a temporal epileptogenic zone, the HPI reports these seizures 2-4 times a week and the exam records one during the admission, so a 72-hour recording that captured none of them while capturing seven gelastic seizures did not support the label. Nothing for Andrea to supply unless the source case (PMC3687620) reports otherwise.
- Decided: a must on paternal valproate exposure (MHRA and EMA 2024) was added although the plan does not list it, because the patient is a young man on long-term valproate and the advice is current regulatory guidance.

## Verification

Adversarial verifier, 24 Oct 2026. Checked the log against the case file and `git diff master`. Tiers (MRI, video-EEG required; PET, drug check, literature optional), MRI `{protocol: epilepsy}`, no constraints and the stop rule (MRI, video-EEG; `max_additional_actions: 2`, as plan 3.4 sets) match the plan. Volumetrics hold (2.41 vs 3.12 cm3: index -0.13, 22.8% smaller). The MRI names the hamartoma and definite HS, the video-EEG carries the temporal seizures the label needs, the drug output's valproate-clonazepam statements (additive sedation, labelled absence-status warning) and the MHRA/EMA 2024 paternal valproate advice are correct, the literature figures (Wiebe 58% vs 8%, ERSET 11/15 vs 0/23) are right, there is no HLA must (plan), and the differential is graded after the work-up. Guards pass.

Found and fixed:
- `metadata.fallback_tool_kinds.ct` still said `normal` after the worker rewrote the CT fallback to show the hypothalamic lesion: set to `case_specific`.

Noted, not changed: the case stores no routine EEG, so a routine EEG order gets the library's normal report although the patient has frequent left temporal sharp waves (true before this round; a routine EEG may be normal). `metadata.case_body_concerns` keeps a stale note about an up-front ECG the case does not have (metadata only).

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-4-search-medical-literature.label`: "Optional" prefix removed.
- Differential "Lennox-Gastaut syndrome": ICD-10-CM G40.812 -> G40.814.

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added), mesial temporal sclerosis epilepsy; removed focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.219, G40.119, G40.919 (drug-resistant, Kwan 2010); the idiopathic G40.009 and G40.019 removed and the not-intractable codes removed.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that contradicts this case now get a case-specific report (term: gist, where stored):

- analyze_eeg ambulatory: This is an ABNORMAL 48-hour ambulatory EEG due to: 1. Left anterior temporal sharp waves (phase reversal at F7), frequent in NREM sleep. 2. Three push (fallback_tool_outputs.eeg)
- obtain_tissue_diagnosis resection: Hippocampal sclerosis, ILAE type 1 (fallback_tool_outputs.tissue_diagnosis)
- obtain_tissue_diagnosis stereotactic_biopsy: Hypothalamic hamartoma (followup request_stereotactic_biopsy)
- obtain_tissue_diagnosis open_biopsy: Hypothalamic hamartoma (followup request_open_biopsy)
- order_specialized_test neuropsych_battery: Low average intellectual functioning (FSIQ 86) with slowed processing speed and impaired verbal learning and delayed verbal recall (T-scores 35 and 33 (fallback_tool_outputs.specialized_test)
- interpret_labs AED_levels: Levetiracetam 21.0 mg/L; Valproate (total) 68.0 mg/L, within the reference ranges. Other analytes not detected. (fallback_tool_outputs.labs[AED_levels], also answers valproate_level)

Checks: `perfect_agent.py` passes; the criterion snapshot of the case is unchanged; `pytest agent-platform/tests -k FEPI-TEMP` (case guards included), `test_reports_do_not_fabricate.py` and `apply_diagnosis_synonyms.py --check` pass; no new report repeats a 60-character window of any criterion's expected evidence.
