# VASC-DEM-M04
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | VASC-DEM was never annotated; no note ids exist for this case. All changes below come from the condition plan and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key. | FIXED: `analyze_brain_mri {}`. |
| D | major | `action-7-search-medical-literature`, literature initial and fallback | Plan C2 leak. | FIXED: criterion deleted; initial null; fallback deleted. |
| C | minor | `action-8-check-drug-interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group D (nebivolol, simvastatin: nothing that changes management). | FIXED: deleted; initial null. |
| B | major | `patient.history_present_illness`, `.clinical_history.past_medical_history[2]` | Timeline contradiction: the event "lasted several hours" / "lasting hours" (a TIA), yet the deficits persist six months later and the case is a completed infarct. | FIXED: the deficit began over one afternoon and "has not resolved since"; PMH "persisting since". |
| C | major | `patient.history_present_illness`, `.clinical_history.social_history.driving` | Laterality: "difficulty reading road signs on the left" and "missed a turning on the left" suggest a left hemifield problem, which a left angular gyrus infarct does not produce (fields full). | FIXED: "twice turned the wrong way when following spoken directions" (right-left disorientation); driving field reworded. |
| C | major | `patient.history_present_illness` | Labelled major vascular cognitive disorder, but the history showed loss of occupation only; DSM-5-TR/VASCOG require interference with independence in everyday activities. | FIXED: husband has taken over the household accounts because she cannot add up bills or write cheques (consistent with `criteria_met.independence_in_iadl_lost` true and the acalculia). |
| D | major | `patient.neurological_exam.mental_status`, `.additional` | Plan C4: MoCA and every focused screen result in the exam; "the four elements of Gerstmann's syndrome" named in the exam. | FIXED: bedside observation (fluent, naming intact, hesitates on left-right command, letter errors writing her address), screening reported separately; additional = frontal release absent, pulse. |
| B | major | `initial_tool_outputs.clinical_assessment.findings`, `.impression`, `.criteria_met` | MoCA 22/30 not derivable (listed losses gave 23); impression localised and argued against AD; `abrupt_onset_dateable_to_an_event` is history. | FIXED: item-level findings (cube 1, clock 2, serial sevens 2, digits backwards 1, recall 2 = 8 lost, 17 years, no correction = 22); impression lists scores and the supplementary parietal items only; history key removed. |
| D | major | `initial_tool_outputs.mri.impression`, `.additional_observations`, `.findings[0]`, `.volumetrics` | Plan C5: "accounts precisely for the Gerstmann tetrad", "dates to the episode misattributed to stress", "argues against Alzheimer's disease", "classically associated with Gerstmann's syndrome"; lesion typed "strategic". | FIXED: numbered STRIVE-2 impression (infarct site, territory, size, volume; Fazekas 1; no microbleeds; MTA 0); type "Chronic cortical infarct"; dashes removed. |
| D | major | `initial_tool_outputs.advanced_imaging.impression` | MRA said "infarct attributable to distal branch occlusion, and secondary prevention is medical". | FIXED: vessel findings only. |
| D | major | `initial_tool_outputs.specialized_test.impression`, `.quantitative_data.pattern` | Neuropsych argued against Alzheimer disease and localised to the angular gyrus. | FIXED: percentiles and "Profile: finger agnosia, right-left disorientation, agraphia and acalculia (the Gerstmann tetrad) with preserved memory and language" (syndrome-level, allowed for neuropsychometry). |
| C | major | `ground_truth.action_criteria` (new `action-9-analyze-ecg`, `action-10-order-echocardiogram`, `action-11-order-cardiac-monitoring`; `action-6-order-advanced-imaging` renamed `action-6-cervical-vessel-imaging`), `initial_tool_outputs.ecg`, `.echo`, `.cardiac_monitoring`, `followup_outputs[0]` | Plan C10: a cortical branch infarct had no ECG, the echo and monitoring were scored as waste, and carotid imaging could only be met by MRA. AHA 2021: ECG for every ischaemic stroke, carotid imaging for anterior circulation, TTE and prolonged monitoring reasonable (2a). | FIXED: ECG recommended (normal sinus rhythm output); cervical-vessel criterion recommended with MRA or carotid duplex alternatives (new duplex follow-up with no stenosis, agreeing with the MRA); TTE optional (normal TTE, EF 62%, septum intact); monitoring optional (30-day event monitor, no AF). Echo and Holter fallbacks deleted (now initial outputs). Echo and monitoring waste entries removed. Soft ECG before monitoring. |
| B | minor | `initial_tool_outputs.labs` | Plan C6: template values, female HDL ">40", eGFR ">60", interpretive text ("excluding reversible causes"). | FIXED: WBC 6.2, Hct 40.1, Plt 287, MCV 90, Na 141, K 4.0, ALT 16, albumin 4.4, folate 12.9; HDL ">50" (60 normal); eGFR ">=60"; interpretation "Flagged: ..." only. |
| D | minor | `fallback_tool_outputs.advanced_imaging`, `.labs`, `.ct` | Plan C7. | FIXED: deleted; CT fallback shows the left angular infarct. |
| A | minor | `action_criteria[*]` | Plan C13. | FIXED: case-specific rationales and evidence; screen label now names the focused parietal items. |
| B | minor | `action_criteria` order, `stop_rule` | Plan C16. | FIXED: screen, neuropsych, labs, MRI, ECG, cervical vessels, TTE, monitoring; stop rule = the four required; `max_additional_actions` 1. |
| B | minor | `avoided_actions` | Plan C18. | FIXED: CT canonical; EEG reason specific (abrupt, stable, no episodes). |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were diagnostic steps ("Obtain brain MRI", "Exclude reversible causes", "Test parietal functions") and "Institute secondary prevention" without content. | FIXED: explain infarct not Alzheimer [VASCOG_2014]; single antiplatelet (aspirin 75-100 mg or clopidogrel 75 mg); simvastatin 20 to high-intensity statin (LDL 134; no stenosis, so the plan's non-atherosclerotic wording); BP below 130/80 from 146/88 with orthostatic checks; no driving until formal assessment, occupational therapy and occupational health before teaching. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | No guard against anticoagulating an embolic-pattern infarct without a source. | FIXED: added "Do not anticoagulate without a documented cardioembolic source; anticoagulation has no benefit over aspirin in embolic stroke of undetermined source [AHA_ASA_2021_secondary]"; others kept. |
| C | major | `ground_truth.differential[0]` | Plan C8: early-onset AD `moderate` after normal memory, MTA 0 and a visible infarct. | FIXED: `low`, key features updated. |
| B | minor | `ground_truth.red_herrings[*].field_path` | Empty. | FIXED: `family_history[0]`, `past_medical_history[3]`. |
| - | check | plan 3.6 | perfect_agent ok; probe: required, recommended and both cervical-vessel alternatives answered by case data; TTE and monitoring answered by the new initial outputs; CT by the case fallback; `case_io.py check` and test_case_guards list no failure naming M04. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case stays a strategic left angular gyrus infarct (Gerstmann tetrad) in a 64-year-old teacher who fears Alzheimer disease. The history now says the deficit began over one afternoon and persisted (it previously "lasted hours"), the driving problem is right-left confusion rather than a left-field problem, and her husband has taken over the accounts, which supports the dementia-level label. The examination and the reports no longer give away the localisation or the answer: the screen lists items (MoCA arithmetic now adds to 22), the MRI and MRA report findings, the neuropsychology names the tetrad without arguing against Alzheimer disease. The embolic work-up follows AHA 2021: ECG recommended, carotid imaging by MRA or duplex, TTE and 30-day monitoring optional with normal results, no longer scored as waste. Musts: explain infarct not Alzheimer, single antiplatelet, high-intensity statin (LDL 134), BP below 130/80, no driving until assessed and an occupational review; anticoagulation without a source is prohibited.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- MockServer: `order_cardiac_monitoring` has no `monitor_type` discriminator; a `holter_24h` order returns the stored 30-day event-monitor report. Add `monitor_type` to the discriminators (as `echo_type` is).
- Synonyms (plan 5.1): `F06.7` appended to this dementia case's codes.

## Open questions for Andrea (judgment calls you could not settle)

- None. (The criterion `action-6-order-advanced-imaging` was renamed `action-6-cervical-vessel-imaging` as plan C10 instructs; no sequence constraint or stop rule referred to it.)

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff (including the HPI and exam rewrites) and the whole final case. Checked: MoCA arithmetic (8 lost, 22/30, 17 years, item sum verified); the HPI changes (persisting deficit, right-left confusion while driving, husband taking over the accounts) agree with `criteria_met.independence_in_iadl_lost`, the exam, the diagnosis label and the timeline; laterality (left angular infarct, right-hand graphaesthesia, full fields); C10 applied (ECG recommended, cervical-vessel criterion with MRA initial and duplex follow-up both served by case data, TTE and 30-day monitor optional with case outputs, echo and monitoring waste removed, soft ECG before monitoring); renamed id `action-6-cervical-vessel-imaging` is the plan's instruction and no constraint or stop rule refers to the old id; musts (single antiplatelet, high-intensity statin for LDL 134 without stenosis, BP, driving and occupational review) vs the ESUS anticoagulation prohibition; female HDL range; differential.

Found: nothing that needed a change. No edits.

perfect_agent ok; `case_io.py check` and test_case_guards list no failure naming M04.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3-order-advanced-imaging].rationale`, `[avoid-waste-4-interpret-labs].rationale` | Plan C18: the MIBG and paraneoplastic/autoimmune rationales were still the August template text shared by M01-M06; the autoimmune one described "a chronic stepwise decline with a hypertensive imaging burden", which is wrong for this case. | FIXED: case-specific one-liners (no Lewy features; abrupt deficit stable for six months). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall and the Gerstmann items tested. The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.
