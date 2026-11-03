# SYNC-CARD-S01
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Finding and summary equal to the literature criterion's expected_evidence (leak guard failure). | FIXED: deleted; one ESC 2021 / ESC 2018 guideline follow-up added last in `followup_outputs`. |
| E | major | `fallback_tool_outputs.literature_search`, `fallback_tool_outputs.drug_interactions.general` | "No directly applicable ... evidence" text; "(agent not specified on this case's pathway)". | FIXED: literature fallback deleted (library answers); drug fallback replaced by a `medication_list_review`. |
| C | major | `action-6-search-medical-literature` | Literature recommended. | FIXED: optional, canonical rationale. |
| C | major | `initial_tool_outputs.drug_interactions`, `action-5-check-drug-interactions` | Initial block listed the medications with no review; criterion named no drug. | FIXED: initial block deleted; alternative `{drug: metoprolol}`; follow-up `check_metoprolol` and fallback carry the review (metoprolol slows AV conduction; apixaban plus aspirin bleeding; apixaban dose check; no bridging; metformin and eGFR). |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg and troponin. | FIXED: recommended, `panels: [BMP]` (plan C); expected_evidence states K 4.4, creatinine 1.3, troponin not elevated. |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Na 135, Cl 91, CO2 22: anion gap 22 with nothing to explain it. | FIXED: Na 137, Cl 101, CO2 24 (gap 12), all normal; summary and interpretation updated. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | Hct 38.1% with Hb 13.9 g/dL. | FIXED: Hct 41.6%. |
| B | minor | `initial_tool_outputs.labs.panels.Cardiac_markers` | Troponin I 0.04 against a reference "<0.04" flagged abnormal with "warrants serial testing", an ambiguity no criterion resolves. | FIXED: 0.02 ng/mL, not elevated (ischaemic cause excluded consistently with the ECG and differential). |
| B | minor | `patient.vitals.hr` | HR 45 while the ECG escape is 35 bpm and telemetry never exceeds 42 bpm. | FIXED: 36. |
| D | minor | `initial_tool_outputs.ecg` | "(likely rate-related or ischemic)", "(borderline prolonged)", "(widened, consistent with ventricular escape)" interpretive annotations. | FIXED: findings only. |
| C | major | `followup_outputs` CT, new `action-9-order-ct-scan` | He is 70, lost consciousness, struck his forehead (laceration, subgaleal swelling) and takes apixaban: NICE NG232 indicates a head CT within 8 h. The red herring called the head CT reflexive and the plan lists head CT as avoided. | FIXED: recommended criterion; CT report moved to `initial_tool_outputs.ct` and reworded (no fracture, subgaleal swelling); red herring replaced. See Open questions. |
| B | major | `followup_outputs[0]` (echo) | Wall motion null while the CMR shows mid-anterior hypokinesis after an LAD PCI; LVEDD 5.4 cm called dilated (normal for a man); no echo_type, TAPSE, PASP, gradients. | FIXED: full TTE report (LVEF 45% biplane, mid-anterior hypokinesis, septum 1.2 / PW 1.1 cm, LAVI 38, AV sclerosis Vmax 1.7 m/s, TAPSE 21 mm, PASP 34 mmHg), no diagnosis sentence. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | 24 h Holter under a criterion labelled "continuous inpatient telemetry" pinned to holter_24h; no symptom-rhythm correlation. | FIXED: alternatives telemetry, holter_24h, holter_48h; output "Inpatient telemetry, 24 h" with the same rates (28-42, average 36, 4.2 s pause at 03:42 in sleep) plus two seated lightheaded episodes at 30-32 bpm; same recording as `fallback_tool_outputs.cardiac_monitoring`. |
| D | minor | `followup_outputs` CMR | "No features of ARVC, sarcoidosis, or infiltrative cardiomyopathy" exclusion sentence over a septal mid-wall LGE; anatomical interpretation of the His bundle. | FIXED: findings-only impression (mid-anterior subendocardial scar; small insertion-point mid-wall enhancement); CMR optional (age 70). |
| C | minor | `followup_outputs` tilt and exercise | Tilt and Bruce test performed in persistent complete heart block (plan J, M). | FIXED: both follow-ups deleted; both avoided as waste. |
| D | minor | `followup_outputs` brain MRI | "age-appropriate" wording only; off-pathway. | FIXED: wording; kept as off-pathway report. |
| H | minor | all `action_criteria[*]` | Free-text "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label. | FIXED: keys only; real rationales. |
| A | minor | `stop_rule`, `sequence_constraints` | `max_additional_actions: 0`; no constraints. | FIXED: 2; soft ECG before TTE and before monitoring. |
| C | major | `avoided_actions` | Only CSF avoided. | FIXED: CSF, EEG, brain MRI, tilt and exercise as waste, each naming the diagnosis. |
| C | major | `ground_truth.assessment` | "Cardiology / EP consult" as a must; no pacing must; no handling of the beta-blocker, apixaban plus aspirin, or LVEF 45%; duplicated driving prohibition. | FIXED: musts are diagnosis, monitored bed with pacing pads and temporary pacing if unstable, permanent pacemaker this admission with the pacing mode chosen for LVEF 45%, hold metoprolol without delaying pacing, peri-procedural apixaban without bridging and review of aspirin (ESC 2024 AF), driving. Prohibitions: AV-nodal drugs before pacing, discharge before pacing, delaying pacing, heparin bridging. |
| C | major | `ground_truth.differential` | VT moderate after a work-up that excludes it; "EP study" cited though not on the pathway; beta-blocker-induced block not discussed. | FIXED: VT low (telemetry, LVEF); all entries cite pathway results; beta-blocker-induced AV block added as low. |
| L | minor | `ground_truth.red_herrings` | "Past palpitations attributed to anxiety" is not in the case; head-CT red herring now wrong. | FIXED: palpitation red herring quotes the HPI; metoprolol and the V4-V6 ST depression added. |
| C | minor | `ground_truth.key_clinical_evidence`, `metadata` | "Holter and EP study are confirmatory"; difficulty rationale and pearls. | FIXED: rewritten; `fallback_tool_kinds` updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The 70-year-old man with prior LAD PCI, paroxysmal AF on metoprolol, apixaban and aspirin collapsed while seated and struck his forehead. Required steps are the ECG (complete AV block, wide escape at 35 bpm with RBBB morphology and left axis), the TTE (LVEF 45% with mild mid-anterior hypokinesis, no valve disease) and inpatient telemetry (Holter accepted: persistent complete block, escape 28-42 bpm, lightheadedness at 30-32 bpm, a 4.2 s pause in sleep, no VT). Recommended: BMP (normal potassium, corrected anion gap, troponin not elevated), a head CT within 8 hours (age over 65, loss of consciousness, anticoagulant; NICE NG232) and a medication review naming metoprolol. CMR and the guideline lookup are optional; EEG, brain MRI, CSF, tilt and exercise are waste, and the tilt and exercise reports were removed. Musts: diagnosis, monitored bed with pacing pads, permanent pacemaker this admission with the pacing mode chosen for LVEF 45%, hold metoprolol without delaying pacing, apixaban without heparin bridging and review of the aspirin, driving advice.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms ("cardiac syncope", "bradyarrhythmia" ...) and R55 still accepted; not hand-edited.
- Plan C3: an off-pathway tilt order now gets the library's normal tilt (HR 68), which contradicts persistent complete heart block. The plan deleted the case's tilt report; a library "no study stored" answer would fix this.
- Plan (lead): section 3 lists head CT as avoided for S01, but the case meets the plan's own NG232 rule twice (age 65 or over with loss of consciousness; anticoagulated). M03's worker made the same deviation.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Deviations from the lead plan, decided for dataset quality:
- Head CT recommended instead of avoided (NICE NG232, as above).
- Troponin set below the 99th percentile instead of exactly at it, so the case does not leave an unresolved ACS question that no criterion addresses.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD (no notes file), so no note ids could be missing. Read the full final case against the log and plan sections A-O.
- Checked: ECG 35 bpm vs vitals 36 vs telemetry 28-42; Hb 13.9 / Hct 41.6; anion gap 12; troponin 0.02 below the 99th percentile; echo LVEF 45% vs CMR 168/92 mL (45%); telemetry and fallback identical with monitor_type telemetry; drug follow-up and fallback content against the medication list (apixaban dose criteria, metformin at eGFR about 58); musts against prohibitions (hold metoprolol, no washout delay, no heparin bridging, ESC 2024 OAC monotherapy beyond 12 months after PCI); red-herring field paths and quotes (ecg.findings[4], medications[0], HPI); differential against pathway results; banned strings and tool names in clinical text (none); leak guard passes.
- The head CT deviation from the plan (recommended instead of avoided) is sound: 70, loss of consciousness, forehead strike, apixaban meets NICE NG232 twice.
- Found and changed: the head-CT criterion `action-9-order-ct-scan` cited [ESC_2018], which does not address head injury; citations set to [] (NICE NG232 is named in the rationale, as the plan requires for keys outside the allow-list).
- perfect_agent -v and case_io check clean after the change.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Drug follow-ups and the fallback medication review: removed, where present, wording that asserted results the agent has not obtained ("while AV conduction disease is unpaced", "meets the labelled dose", device-implantation warnings, the eGFR-specific metformin line, cefazolin "for device implantation"). Each is now a conditional rule (e.g. contraindicated in second- or third-degree AV block without a pacemaker; apixaban 5 mg unless two of age 80 or over, weight 60 kg or less, creatinine 1.5 mg/dL or more; anticoagulation advice if a device is implanted). Why: a drug check must not disclose the conduction diagnosis or the management decision.
- `initial_tool_outputs.drug_interactions` set to the medication-list review (copy of the fallback). Why: without it, tier 2 answered an unrelated drug (probe: ibuprofen) with the first per-drug follow-up.
- Added "not performed" follow-ups for `tilt_table` and `exercise_stress_test` (RM04/RP02 format, "Deferred by the clinical team"). Why: otherwise the library returned a normal tilt (HR 68) or a normal exercise test (10.4 METs) in a patient with high-grade AV block, contradicting the case; both orders stay penalised as in the plan.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: complete heart block labels only (Mobitz II and second-degree labels removed: a different grade); I44.30 kept, I44.1, I44.39, I45.9 and R55 dropped.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-2-interpret-labs citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2021_Pacing]']; action-9-order-ct-scan citations [] -> ['[NICE_NG232]']; action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2021_Pacing]']; action-8-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; action-5-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-S01` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure 'Active stand test not performed. Deferred by the clinical team.' (haemodynamically unstable or high-grade AV block at presentation: standing is not safe); no criterion |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

| field path | change |
| --- | --- |
| `followup_outputs[8]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-8-order-advanced-imaging` label: "Cardiac MRI to characterise the substrate (optional)" -> "Cardiac MRI to characterise the substrate"
- criterion `action-6-search-medical-literature` label: "Guideline lookup on pacing indications (optional)" -> "Guideline lookup on pacing indications"

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.alternatives: was [BMP]; now [BMP, troponin] | [BMP].
- Decision: serve: new first alternative (old order kept as an alternative). The ischaemic AV block differential and a red herring read the troponin, and the July 2026 syncope ruling keeps troponin where ischaemia is in question; the BMP did not return it.
- Scoring: none (recommended criterion; any call matching the old order still matches).

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 70, ECOG 2 (fallback_tool_outputs.clinical_assessment). Why: rule 2: the library reports Karnofsky 100 with no complaints in a sedentary man with two months of fatigue, exertional dyspnoea and near-syncope.
- `order_echocardiogram {echo_type: TEE}`: LVEF 45% with mid-anterior hypokinesis, mild LVH, no thrombus (fallback_tool_outputs.echo). Why: rule 3: the stored TTE shows LVEF 45% with regional hypokinesis and mild LVH; the library TEE reports a normal heart.
- `order_echocardiogram {echo_type: bubble_study}`: LVEF 45% as on the TTE, no shunt (followup_outputs[9] request_bubble_study). Why: rule 3: the stored TTE is abnormal (LVEF 45%, regional hypokinesis); the library reports a normal heart.
- `order_echocardiogram {echo_type: exercise_echo}`: stress phase not performed, deferred by the clinical team (followup_outputs[10] request_exercise_echo). Why: rule 3: the stored exercise test is not performed in complete AV block with a 35 bpm escape; the library reports a normal study at 9.5 METs, which this rhythm cannot produce.
- `order_advanced_imaging {modality: coronary_CTA}`: patent LAD stent, non-obstructive RCA and circumflex plaque (fallback_tool_outputs.advanced_imaging). Why: rule 2: coronary artery disease with an LAD stent four years ago and a mid-anterior infarct scar on the stored cardiac MRI; the library reports no plaque.
- `order_advanced_imaging {modality: coronary_angiography}`: patent LAD stent, non-obstructive RCA disease (followup_outputs[11] request_coronary_angiography). Why: rule 2: coronary artery disease with an LAD stent four years ago; the library reports normal coronaries.
- `order_specialized_test {test_type: emg_ncs}`: mild length-dependent sensory-predominant axonal polyneuropathy (fallback_tool_outputs.specialized_test). Why: rule 2: type 2 diabetes for eight years with diminished vibration at the great toes and Achilles reflexes 1+; the library reports normal nerve conduction.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
