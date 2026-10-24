# FTD-M05
Reviewer status: R1 none, R2 none (no FTD notes file; FTD was never reviewed case by case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | No reviewer note exists for this case. Reviewer 1's July 2026 tool rulings (`condition_tool_guidance.yaml` `ftd:`) are kept: neuropsychology, clinical assessment and labs required; FDG-PET optional. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `initial_tool_outputs.literature_search`, `action-7-search-medical-literature` | The literature output carried the shared echo string of an `expected_evidence` (leak guard failure); criterion required with echo evidence (plan C1). | FIXED: canonical text with the psychiatric-mimic variant (`[Ducharme_2020]`); criterion optional, last, `required_arguments` {}, out of the stop rule. Leak guard passes. |
| C | major | `action-8-check-drug-interactions` | Required lithium "drug interaction" check whose content was a dose-adjustment essay; the clinical question (is lithium toxicity a reversible mimic?) is answered by a serum level (plan M05). | FIXED: same id, now `interpret_labs` `{panels: [lithium_level]}`, required, in the stop rule; new keyed follow-up `request_lithium_level` serving lithium 1.28 mmol/L against the 0.4-1.0 maintenance range (was "0.6-1.2 mEq/L" inside the core panel). |
| C | major | `followup_outputs` (`lithium_adjusted_recheck_behavioral_persistence`) | A repeat level 6 weeks after a dose reduction the case had not yet recommended, with persistent behaviour: a result of future management (ruling 4). | FIXED: deleted. Key evidence, red herring and notes no longer presume normalisation. |
| C | major | `followup_outputs` (`lithium_adjustment_monitoring`, `bipolar_ftd_medication_management`) | Drug essays with doses, and the false claim that empagliflozin raises lithium clearance only "mildly" as a toxicity concern (plan C2). | FIXED: both deleted. New sertraline output: lithium serotonin toxicity and hyponatraemia, aspirin bleeding, metoprolol CYP2D6, empagliflozin and atorvastatin no significant interaction; MAOI/pimozide; hyponatraemia and QT warnings. Optional criterion `action-9-check-drug-interactions-sertraline` (`drug: sertraline`). No toxicity-causing empagliflozin interaction was invented. |
| D | major | `patient.history_present_illness` | "which reduces lithium clearance" hint; duplicated vascular sentence; closing sentence naming the feature ("echolalia-like perseveration"). | FIXED: hint and both sentences deleted; facts kept. |
| D | minor | `patient.neurological_exam.additional` | "lithium level and renal function warrant checking" told the agent what to order. | FIXED: deleted; "He takes lithium and has CKD stage 2 (eGFR 64)." |
| B | minor | `patient.neurological_exam.cranial_nerves`, `.reflexes` | Snout reflex under cranial nerves and "No primitive reflexes on cranial nerve exam" (plan C14). | FIXED: cranial nerves "Normal."; reflexes carry palmomental and snout. |
| B | minor | `patient.neurological_exam.mental_status` | MoCA items (trails, fluency, recall 3/5, naming) could not sum to 9 lost points. | FIXED: trails 1, clock 2, letter fluency 1, abstraction 2, delayed recall 2, naming 1 (21/30). |
| B | major | `initial_tool_outputs.clinical_assessment` | Template fragments and impression (plan C3). | FIXED: rebuilt, 5 of 6 features (disinhibition, apathy, loss of empathy, perseverative, executive); dietary change absent; informant (son), screen and functional decline lines; canonical impression. |
| B | major | `initial_tool_outputs.labs` | Single "Dementia_Bipolar_Lithium_Workup" panel with RPR, HIV and copper; creatinine 1.4 gives an eGFR of about 55 by CKD-EPI 2021, not the 64 stated in the history, exam and PMH; folate, calcium, glucose, LFTs, Hb, platelets missing (plan C5). | FIXED: five panels with stored values kept (TSH 3.6, B12 446, WBC 8.2, Na 138, eGFR 64, HbA1c 7.1 H, ESR 11, CRP 1.6); creatinine set to 1.24 mg/dL so it gives eGFR 64 by CKD-EPI 2021 for a 66-year-old man; glucose 138 H (consistent with HbA1c 7.1) and normal routine analytes added; copper deleted; lithium moved to its keyed follow-up; RPR/HIV to `request_rpr_syphilis_hiv_serology`. |
| D | minor | `initial_tool_outputs.mri` | FLAIR line "insufficient to account for degree of frontal atrophy" (interpretation); unterminated impression. | FIXED: descriptive FLAIR; numbered impression with pertinent negatives. |
| B | minor | `followup_outputs` (neuropsych) | Long teaching impression; `recommended_actions` "Correlate with ... FDG-PET" (plan C13). | FIXED: findings in report voice, numbered impression with canonical ending, `recommended_actions` emptied. |
| D | minor | `followup_outputs` (FDG-PET) | Impression said the scan was "performed under documented conditions of therapeutic lithium level", presuming a result. | FIXED: metabolic findings only; hedged pattern statement. |
| C | minor | `action-6-order-advanced-imaging`, `followup_outputs` (SPECT) | No SPECT alternative (plan C6). | FIXED: `perfusion_SPECT` alternative and an authored right-predominant frontal SPECT. |
| C | major | `fallback_tool_outputs.advanced_imaging`, `.ct` | Generic advanced-imaging fallback; normal CT against MRI atrophy (plan C6). | FIXED: deleted; CT shows bifrontal volume loss; `fallback_tool_kinds.ct` "abnormal". |
| A | minor | `ground_truth.action_criteria[*]` | Rationale equal to label, `[AAN_dementia_2018]`, echo evidence (plan C4). | FIXED: canonical labels and citations; case-specific evidence. Ids kept. |
| C | major | `ground_truth.assessment.required_recommendations` | Template block plus "verify therapeutic lithium level" (an order, not a recommendation) (plan C9). | FIXED: five musts: Rascovsky; why the syndrome is not lithium toxicity or bipolar relapse, without presuming a later level; lithium back into range with his psychiatrist (dose review, recheck level and renal function, avoid dehydration and NSAIDs); safety and capacity (lives alone, medicines, driving, finances, power of attorney); caregiver support. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Overstated memantine harm (plan C10); nothing against stopping lithium abruptly. | FIXED: canonical first two; added "Do not stop lithium abruptly" (relapse risk). |
| C | major | `ground_truth.differential` | Lithium toxicity, bipolar relapse and AD all "moderate"; "Familial FTD" listed with no family history (plan C11). | FIXED: lithium neurotoxicity low, bipolar episode low, frontal AD low, vascular low, with for/against from the case. |
| D | major | `ground_truth.key_clinical_evidence`, `.red_herrings`, `metadata.notes` | Lines presumed persistence after lithium normalisation. | FIXED: rewritten from the history, the level as obtained and the MRI; red herrings for bipolar history and the lithium level (`followup_outputs[1].output.panels`). |
| C | minor | `ground_truth.avoided_actions` (CT, perfusion MRI) | `[AAN_dementia_2018]`; perfusion MRI rationale. | FIXED: `[NICE_NG97]`; reworded. |

## Changes, in one paragraph a physician can read before re-reviewing

Required work-up: informant assessment, neuropsychological battery, reversible-cause blood tests, a serum lithium level (replacing the lithium "interaction check") and MRI brain; optional FDG-PET or SPECT, a sertraline interaction check and a literature search. The history and exam no longer tell the agent that lithium clearance is reduced or that a level is needed, and no longer name the perseveration. The lithium level (1.28 mmol/L, mildly above the 0.4-1.0 maintenance range) is served only when ordered; the six-week post-dose-reduction recheck was deleted because it was the result of a recommendation not yet made. Creatinine is now 1.24 mg/dL so that it matches the stated eGFR of 64. The clinical assessment counts 5 Rascovsky features from the son's account. Musts: Rascovsky; why lithium toxicity and a bipolar relapse do not explain the syndrome; correct the lithium level with his psychiatrist and monitor renal function; safety and capacity for a man living alone; caregiver support. New prohibition: do not stop lithium abruptly.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys used per plan 1.1: `[SNLG_ISS_2024]`, `[Ducharme_2020]`.
- MockServer routing: a single first `interpret_labs` order that combines core panels with `lithium_level` is answered by the keyed lithium follow-up only; the core panel is then served on the next labs order. Consider merging the keyed follow-up with the initial output when a combined order matches both.
- Tier 2: any drug name returns the case's only drug follow-up (sertraline report), as in FTD-M01.

## Open questions for Andrea (judgment calls you could not settle)

- The lithium level criterion keeps the id `action-8-check-drug-interactions` (round rule: ids kept) although it is now a lab order; rename it if ids may change.
- Creatinine was changed from 1.4 to 1.24 mg/dL to match eGFR 64; the alternative is to keep 1.4 and state eGFR about 55 (CKD stage 3a) everywhere.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes apply. Checked: creatinine 1.24 gives eGFR 64 by CKD-EPI 2021 for a 66-year-old man (recomputed); lithium follow-up keyed and in range terms (0.4-1.0 maintenance); the post-dose-reduction recheck is deleted and nothing presumes it; no invented empagliflozin toxicity interaction; sertraline output (lithium, aspirin, metoprolol CYP2D6) correct; MoCA items sum to 21/30; exam records no tremor or ataxia, consistent with the "no neurotoxic signs" must and differential; lithium criterion required and in the stop rule; guards pass. Found and fixed: `fallback_tool_outputs.specialized_test` was a generic "Study within normal limits" with an empty `test_type`, which breaks the discriminator rule (PATTERNS 5) and would answer any specialised order (genetic panel, EMG) with a normal report; set to null and removed `metadata.fallback_tool_kinds.specialized_test`. The criterion id `action-8-check-drug-interactions` on a lab order remains as logged (ids kept). `perfect_agent.py -v` and `case_io.py check` clean.

## Condition audit (FTD auditor, 24 Oct 2026)

- D, major, `patient.neurological_exam.mental_status`: the examination gave the bedside screen results (MoCA 21/30 with item losses and letter fluency), which the required `perform_clinical_assessment` returns (ROUND_POLICY timeline-leak rule). The other 12 FTD cases, and VASC-DEM and ALZ-EARLY, had already moved them out. Removed the scores and test results; the behavioural observations, insight and frontal signs stay. The clinical assessment output already carries every removed value, so no information is lost. FIXED.
- B, minor, `fallback_tool_outputs.csf`: a case CSF fallback with empty `special_tests` answered any CSF order without a stored result (for example Abeta42, p-tau and t-tau), so the ordered assays were missing from the report. Deleted, together with `metadata.fallback_tool_kinds.csf`, as in M07, M09, M10, P01 and P02. The library now answers per assay; a probe returned normal AD markers. FIXED.
- E, minor, `fallback_tool_outputs.literature_search`: the placeholder ("general", "Recommend correlating with current society guidelines") was deleted together with its kind key, as in the other FTD cases. The initial literature output answers any query. FIXED.
- E, minor, `initial_tool_outputs.literature_search[*].results[*].source`: the sources were citation keys (`[Rascovsky_2011]` or `Rascovsky_2011`), which a literature tool does not return, and the condition used three styles. They now give the full reference, as in M07-P02 (for example "Rascovsky K et al. Brain 2011;134:2456-2477 (FTDC criteria for bvFTD)"). Findings and summary are unchanged. FIXED.
- `perfect_agent.py` and `case_io.py check` were re-run on all 30 FTD cases after the changes and are clean; `test_case_guards.py -k FTD` passes (60 tests).

## Close-out (24 Oct 2026)

Decisions in `plans/FTD-decisions.md`. Changes:

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (the report is a transthoracic study). The MockServer routes echo reports by this field; without it the normal TTE fallback answered a TEE order too (PATTERNS section 5; FTD added to `DISCRIMINATOR_CONDITIONS`).
- `ground_truth.diagnosis.accepted[0]`: the em dash replaced by a comma (house style; token matching ignores punctuation, so scoring is unchanged).
- Criterion id `action-8-check-drug-interactions` -> `action-lithium-level` (the criterion orders interpret_labs, not a drug check; stop rule updated); summary CENTRAL 9.
- Added optional criterion `action-genetic-panel-optional` (`order_specialized_test` `genetic_panel:FTD`, `[Pottier_2016]` `[Ducharme_2020]` `[ACMG_NSGC_2011]`), placed after imaging and before any drug check or literature step, a soft constraint clinical assessment before genetics, and a negative FTD panel follow-up (`request_optional_counselled_ftd_genetics`). Reason: sporadic bvFTD with young onset (before 65); the FTD consortium advises C9orf72 screening in every possible or probable bvFTD (Ducharme 2020), so a counselled panel is a defensible order that the stop rule should not penalise, while UK eligibility (onset before 55, a suggestive family history or MND; NHS GeneTYPES) is not met, so it is optional and no counselling must is added (FTD-decisions item 7). Onset about 64.
- Synonyms (`G31.09` entry, applied with `--prune --conditions ftd`): "pick disease" and "pick's disease" (retired) and the code G31.01 are no longer accepted. Pick disease is one FTLD-tau pathology that no case establishes, and G31.01 is where ICD-10-CM codes primary progressive aphasia, so a PPA answer coded G31.01 scored as correct here.

Checks: `perfect_agent.py` and `case_io.py check` clean; `test_case_guards.py -k FTD-` passes, including `test_routed_outputs_name_their_study`.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
