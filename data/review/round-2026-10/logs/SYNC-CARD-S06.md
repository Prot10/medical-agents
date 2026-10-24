# SYNC-CARD-S06
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs` monitoring, `action-4-order-cardiac-monitoring` | A 48 h ambulatory Holter with a patient diary was stored under trigger `request_telemetry_monitoring`; the criterion pinned holter_24h only; there was no case fallback; the report said "Sinoatrial conduction time appears prolonged" (not measurable on a Holter) and gave an interpretive impression ("consistent with a tachy-brady pattern"). | FIXED (plan E): alternatives telemetry, holter_24h, holter_48h; trigger `request_telemetry_holter_monitoring`; the output is now "Inpatient telemetry, 48 h", monitor_type telemetry, with the symptom reported to the nurse; the SACT line is removed; the impression only describes findings; the same recording is stored as `fallback_tool_outputs.cardiac_monitoring`. |
| C | major | `followup_outputs` drug (`check_metoprolol_diltiazem_interactions`), `action-5-check-drug-interactions` | The output claimed that diltiazem raises metoprolol levels by 30-50% through CYP3A4. Metoprolol is a CYP2D6 substrate, and the clinically relevant interaction is pharmacodynamic. The criterion pinned `current_medications: [metoprolol]`. The text contained an em dash. | FIXED: required, with alternatives `{drug: diltiazem}` and `{drug: metoprolol}` and one follow-up each. Each reviews her actual seven drugs: additive sinus/AV-node suppression; diltiazem raising apixaban (about 1.4-fold, no dose change) and amlodipine; peri-implant apixaban without bridging. The pin was dropped. |
| E | major | `fallback_tool_outputs.drug_interactions`, `fallback_tool_outputs.literature_search` | Read "(agent not specified on this case's pathway)" and "No directly applicable" evidence. | FIXED: the drug fallback is a `medication_list_review`; the literature fallback is deleted. |
| D | major | `followup_outputs` literature, `action-6-search-medical-literature` | The literature criterion was required. Its follow-up echoed the expected evidence and attributed "sinus pause >3 s symptom-correlated Class I" to ACC/AHA via a Locati summary. | FIXED: optional, with the canonical rationale, and out of the stop rule. The follow-up is rewritten with the two ESC 2021 pacing recommendations (symptomatic SND Class I B; bradycardia-tachycardia form Class I B) and placed last. |
| B | major | `followup_outputs` CT | The head CT report listed a "Left elbow (not cranial)" finding. | FIXED: follow-up deleted. A head CT order now gets the case's normal fallback; head CT stays avoided as waste (no head strike, elbow abrasion only, normal exam; NICE NG232 does not apply even on apixaban). |
| C | major | `followup_outputs` tilt | A tilt test result was stored, and the differential cited it to lower vasovagal syncope. | FIXED (plan J/M): follow-up deleted; tilt added as avoided waste `avoid-waste-5-tilt-table`. |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin and TSH. | FIXED: recommended, alternatives `panels: [BMP]` or `[TSH]`; real rationale (exclude reversible metabolic and thyroid causes in a patient on levothyroxine). |
| B | minor | `followup_outputs[0]` (echo) | No echo_type; wall_motion null; no TAPSE or thrombus statement. | FIXED: echo_type TTE, normal wall motion, TAPSE 21 mm, no mass or thrombus; values otherwise unchanged. |
| C | major | `ground_truth.assessment` | The musts included "Obtain Holter" (a scored test) and a generic cardiology referral. Pacing mode, the choice of rate-control drugs, anticoagulation and driving were not covered. The tilt prohibition was phrased as a test. | FIXED: musts are the diagnosis, admission to monitoring, a dual-chamber pacemaker (ESC 2021 Class I), stopping diltiazem while keeping a beta-blocker for AF after pacing, continued apixaban (CHA2DS2-VA 2) without bridging, and driving (Group 1 resumes 1 week after implantation). Prohibitions: excluding arrhythmia on the resting ECG, both nodal drugs without pacing, stopping anticoagulation, and discharge before pacing. |
| C | major | `ground_truth.differential` | AV block was rated moderate even though monitoring showed normal AV conduction. Vasovagal syncope was rated moderate on the basis of the tilt. Drug-induced bradycardia was rated moderate with no explanation of why pacing is still needed. | FIXED: all three are low, each with case-specific evidence (pauses with normal AV conduction; an event coinciding with a post-conversion pause; pauses at AF termination reflect intrinsic SND). |
| H | minor | all `action_criteria[*]`, `avoided_actions` | Section and author citations; rationale equal to label; avoided reasons did not name the diagnosis. | FIXED: keys only (`[ESC_2018]`), real rationales; every avoided reason names the diagnosis. |
| A | minor | `stop_rule`, `sequence_constraints` | The stop rule required the literature criterion; max_additional_actions was not 2; there were no ECG-first constraints. | FIXED: ECG, TTE, monitoring and the required drug check; max 2; soft ECG before TTE and before monitoring, with the canonical reason. |
| L | minor | `ground_truth.red_herrings[0]` | The data_point paraphrased the ECG. | FIXED: quotes `initial_tool_outputs.ecg`. |
| E | minor | `ground_truth.key_clinical_evidence`, `metadata` | Em dashes; the difficulty rationale counted the literature criterion as required; there was no `fallback_tool_kinds` for monitoring. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The 74-year-old woman with recurrent syncope keeps her presentation, a resting ECG with sinus bradycardia at 48 bpm, normal labs (TSH 2.4) and a normal TTE (LVEF 62%; now with TAPSE and wall motion). On metoprolol with diltiazem, her 48 h inpatient telemetry shows three self-terminating AF episodes. The longest ends in a 4.8 s sinus pause at the moment she reports blacking out to the nurse. Holter orders are accepted and receive the same recording. Required: ECG, TTE, monitoring, and a review of the two rate-slowing drugs (diltiazem or metoprolol). Recommended: BMP or TSH. The guideline lookup is optional and now cites ESC 2021 pacing correctly. The stored tilt and the garbled head CT reports were removed. Tilt, brain MRI, EEG, CSF and head CT are waste. Musts: the tachy-brady sick sinus diagnosis, monitored admission, a dual-chamber pacemaker, stopping diltiazem while keeping a beta-blocker for AF after pacing, apixaban continued without bridging, and no driving until 1 week after implantation.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: the synonym list for this case still accepts "cardiac syncope"; not hand-edited.
- Plan C3: after the deletion, a tilt order (avoided as waste) gets the library's normal tilt report, which is harmless here but inconsistent across the bradyarrhythmia cases.

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Read the full final case against the log and plan.
- Checked: CHA2DS2-VA 2 (hypertension, age 65-74; ESC 2024 removes female sex) correct; apixaban dose criteria; diltiazem raising apixaban exposure about 1.4-fold (apixaban label) and amlodipine; female reference ranges correct; drug check required with diltiazem or metoprolol and in the stop rule; musts (stop diltiazem, beta-blocker after pacing, apixaban without bridging) agree with the prohibitions; telemetry and fallback identical, monitor_type telemetry; ECG red-herring quote present; leak guard passes.
- Found and changed:
  - The telemetry event says she told the nurse she "felt dizzy and blacked out briefly" during the 4.8 s pause, while the impression (both copies) and the vasovagal differential called it "near-loss of consciousness". Aligned to "a brief blackout she reported to the nurse" / "the brief blackout on telemetry".
  - Head CT is avoided as waste on the ground that "she did not strike her head", but the HPI never said so (a 74-year-old on apixaban who fell to the floor; NG232 would indicate CT for any head injury). The HPI now states she "slid to the floor onto her left side without striking her head", which matches the left elbow abrasion in the exam and makes the waste ruling hold.
- perfect_agent -v and case_io check clean after the changes.

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
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-2-interpret-labs citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2021_Pacing]']; action-5-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; avoid-waste-4-order-ct-scan citations [] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-S06` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report, supine values = the presenting vitals; No orthostatic fall in blood pressure and no excessive heart rate rise on active standing. |
| `ground_truth.action_criteria[action-orthostatic-blood-pressure]` | added, recommended, after the ECG criterion [ESC_2018] (decisions CENTRAL 1: orthostatic BP in every initial evaluation) |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

| field path | change |
| --- | --- |
| `followup_outputs[8]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |
