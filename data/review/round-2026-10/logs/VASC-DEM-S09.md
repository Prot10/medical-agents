# VASC-DEM-S09
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No notes file exists for VASC-DEM. The condition plan's classes (C1-C19) were applied as class rulings (ROUND_POLICY ruling 2); every change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A/C | blocker | ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives | Non-schema `sequences` plus `protocol`/`contrast` (C1) | FIXED: `analyze_brain_mri {}` |
| D | major | ground_truth.action_criteria[action-7-search-medical-literature], initial_tool_outputs.literature_search, fallback_tool_outputs.literature_search | Literature criterion leaking into its own output (C2, ruling 5) | FIXED: criterion deleted, initial null, fallback deleted |
| C | minor | ground_truth.action_criteria[action-8-check-drug-interactions], fallback_tool_outputs.drug_interactions | Generic optional check; no new interacting drug (C3 group D) | FIXED: criterion and fallback deleted (initial already null) |
| D | major | patient.neurological_exam.mental_status | MoCA total and recall items upfront (C4) | FIXED: bedside observation; confabulation and apathy kept as exam signs |
| B | major | patient.neurological_exam.mental_status, initial_tool_outputs.clinical_assessment | MoCA 23/30 with "all 5 points lost on delayed recall" and every other item full gives 25/30; "fully oriented" in a dense anterograde amnesia of eight months (she cannot remember whether she has eaten); serial sevens "5/5" (the MoCA item scores 0-3) | FIXED: orientation 4/6 (date and day wrong), giving 30 - 5 - 2 = 23; serial sevens 3/3; screen itemised by section |
| D | major | initial_tool_outputs.clinical_assessment (impression, criteria_met, findings) | "the profile of a strategic thalamic lesion, not of small-vessel disease", abrupt onset and "deficit disproportionate to lesion volume" and IADL loss in criteria_met (C5) | FIXED: impression gives total, losses, recall with cues and multiple choice, fluency, AES, GDS; criteria_met keeps domain impairment and recall-with-cueing false |
| D | major | initial_tool_outputs.specialized_test (impression, quantitative_data) | "localises to the medial diencephalic memory circuit rather than to the frontal-subcortical networks affected by small-vessel disease", "excluding a retrieval-only deficit" (C5) | FIXED: profile only |
| D | major | initial_tool_outputs.mri (additional_observations, impression, findings[0]) | "accounts fully for a dense anterograde amnesia", "dates to the admission eight months ago", the admission CT cited (cross-modality), type "strategic infarct" (C5) | FIXED: numbered STRIVE-2 impression; anatomical localisation (anterior nucleus, mamillothalamic tract region) kept as Kind 2; mamillary bodies and periaqueductal grey described normal (pertinent negative for the Wernicke differential) |
| B | minor | initial_tool_outputs.mri.volumetrics.lesion_volume; ground_truth.key_clinical_evidence[0]; criterion expected evidence | 0.7 mL for an 11 x 9 x 8 mm lesion (ellipsoid volume about 0.4 mL) | FIXED: about 0.4 mL everywhere |
| D | major | initial_tool_outputs.advanced_imaging.impression | "attributable to occlusion of a small perforating artery, which is not amenable to revascularisation and is treated with risk-factor control" (C5) | FIXED: vessel findings plus "Thalamoperforating arteries are below the resolution of MRA" (plan P09 wording) |
| C | major | ground_truth.action_criteria, initial_tool_outputs (ecg, echo, cardiac_monitoring), avoided_actions[6,7] | Infarct recognised now, never worked up at the admission (CT only); no ECG, while TTE and monitoring were penalised as waste (C10) | FIXED: new action-9-analyze-ecg (recommended, normal sinus ECG), action-10-order-echocardiogram (optional; the former fallback echo moved to the initial output, modality-only, `echo_type` TTE), action-11-order-cardiac-monitoring (optional, 14-day monitor, sinus throughout); echo and monitoring waste entries removed; soft ECG before monitoring |
| C | minor | ground_truth.action_criteria[action-6-order-advanced-imaging].expected_evidence | "Patent artery of Percheron territory vessels" (another case's text: this is a unilateral infarct) | FIXED: posterior circulation and carotid without stenosis or dissection |
| B | major | initial_tool_outputs.labs | Template values; Hct 41.6 with Hb 13.2; eGFR ">60"; HDL range ">40" in a woman; LDL 102 not derivable from TC 192, HDL 58, TG 118 (Friedewald 110); interpretation "excluding the reversible causes" (C6) | FIXED: WBC 6.1, Hct 39.8, Plt 289, MCV 86, Na 137, K 3.8 (on indapamide), ALT 24, albumin 4.4, folate 15.2; TC 184 (184 - 58 - 118/5 = 102); ranges ">=60" and ">50"; flag-only interpretation |
| B/D | major | fallback_tool_outputs (advanced_imaging, labs, ct, echo, cardiac_monitoring) | "non-contributory" fallbacks; CT "already obtained"; echo "No cardioembolic source identified" (C7) | FIXED: advanced_imaging, labs, cardiac_monitoring deleted; echo moved to the initial output; CT written for this patient (small chronic left anteromedial thalamic hypodensity, now visible at eight months); metadata.fallback_tool_kinds updated |
| C | major | ground_truth.assessment.required_recommendations | Musts restated criteria or reasoning (obtain MRI, test recognition, exclude reversible causes, "institute secondary prevention" without content) (C19) | FIXED: single antiplatelet; BP below 130/80 gradually; high-intensity atorvastatin (LDL 102 on 20 mg; small-vessel infarct, so no LDL 70 target per plan 1.2); fitness to practise and driving; memory rehabilitation and caregiver support |
| C | minor | ground_truth.assessment.prohibited_recommendations | Generic anticholinergic prohibition | FIXED: replaced by "Do not start anticoagulation without a documented cardioembolic source"; MCI prohibition names the lost occupation |
| C/A | minor | ground_truth.action_criteria[*] | Rationale = label; unbracketed citations; verdicts in expected evidence (C13) | FIXED |
| C | minor | ground_truth.red_herrings[1].field_path; red_herrings[0] | Empty field path; "the entire loss falls on delayed recall" no longer true after the orientation fix | FIXED: `patient.history_present_illness`; interpretation names recall and orientation |
| C | minor | ground_truth.avoided_actions[*].rationale; stop_rule | Generic rationales (EEG now names the absence of episodic attacks, the transient epileptic amnesia question); max 0 (C16, C18) | FIXED; max 1 |
| C | check | 3.6 check | each criterion probed on a fresh environment | every criterion, the three new ones included, answered by an initial output; no library answer |

## Changes, in one paragraph a physician can read before re-reviewing
The MRI criterion now matches any MRI order. The exam no longer gives the MoCA; the screen now adds up (23/30 from five recall points and two orientation points, since a patient with this amnesia is not fully oriented) and serial sevens is scored on its 0-3 scale. Reports state only their own findings: the MRI describes the left anterior and paramedian thalamic infarct (about 0.4 mL, corrected from 0.7 mL for an 11 x 9 x 8 mm lesion) in the region of the mamillothalamic tract without explaining the amnesia, the MRA no longer prescribes risk-factor control, and the neuropsychology report gives the profile without localising it. Because this infarct was never worked up, an ECG is now recommended and echocardiography and a 14-day monitor are optional with normal case-authored results, instead of being penalised as waste. Labs have varied values and an LDL consistent with the lipid panel. Musts: aspirin, BP below 130/80, high-intensity statin, fitness to practise and driving, memory rehabilitation and caregiver support.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms per plan 5.1 (F06.7 in the `icd_codes` of a dementia case; "multi-infarct dementia" accepted for a strategic single-infarct case).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Adversarial verifier, 24 Oct 2026. No notes file for VASC-DEM. Read the final case and the diff. Checked: MoCA arithmetic (only recall 0/5 and orientation 4/6 lost: 23/30), with the bedside orientation in the exam agreeing (wrong date and day); lesion volume (pi/6 x 1.1 x 0.9 x 0.8 cm = 0.41 mL) everywhere it appears; Friedewald LDL (184 - 58 - 23.6 = 102); female ranges; the three new C10 criteria (ECG recommended, TTE and 14-day monitor optional) each served by a case-authored normal output, echo and monitoring waste removed, ECG-before-monitoring soft constraint; MRA wording per plan; musts (aspirin, BP, high-intensity statin without an LDL-70 target for a perforator infarct) consistent with the prohibition against anticoagulation; CT fallback consistent with a lesion now visible at eight months; neuropsychology required as before the round.
Found and fixed: the Wernicke-Korsakoff differential said "No alcohol history" while the social history records two glasses of wine weekly. Now "No alcohol misuse (two glasses of wine weekly)".
perfect_agent.py and case_io.py check clean for this case.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here "strategic infarct dementia". Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.
