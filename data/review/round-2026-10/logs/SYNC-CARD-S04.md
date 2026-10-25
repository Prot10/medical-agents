# SYNC-CARD-S04
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history` (medications, past_medical_history, family_history, social_history) | Record copied from S02 (same seven drugs and doses, PMH wording, "father died suddenly at 58", retired accountant, smoking history) (plan M). | FIXED: his own record: telmisartan, indapamide (added 4 months ago), linagliptin, atorvastatin, paracetamol; PMH with CKD 3b by eGFR, knee osteoarthritis, hearing loss; new family and social history. HPI sentence on medication changes updated to name indapamide. The new record explains his Na 123, Mg 1.6 and urate 8.4. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | Holter numbers copied from S02 (average 34, range 26-40, minimum 26 at 02:18); 24 h Holter under a telemetry label pinned to holter_24h. | FIXED: alternatives telemetry, holter_24h, holter_48h; "Inpatient telemetry, 24 h" with his own numbers (average 36, range 29-43, 4.8 s pause at 03:50, presyncope at 30 bpm on walking); same recording as the fallback. |
| D | major | `initial_tool_outputs.literature_search`, `initial_tool_outputs.drug_interactions.general` | Literature output equal to its key; drug block the bare key "Hold AV-nodal blockers" (he takes none). | FIXED: both deleted; one ESC/EACTS 2021 and ESC 2021 pacing follow-up added last. |
| E | major | `fallback_tool_outputs.literature_search`, `fallback_tool_outputs.drug_interactions.general` | "No directly applicable ... evidence"; "(agent not specified on this case's pathway)". | FIXED: literature fallback deleted; drug fallback is a `medication_list_review` (indapamide hyponatraemia; vasodilators in severe AS; latex allergy). |
| C | major | `action-5-check-drug-interactions`, `action-6-search-medical-literature` | Drug check recommended with no drug; literature recommended. | FIXED: both optional (plan B, A); drug alternative `{drug: indapamide}` with its follow-up. |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin. | FIXED: recommended `panels: [BMP]`; expected_evidence Na 123, Mg 1.6 on indapamide. |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Na 123, Cl 96, CO2 22: anion gap 5. Interpretation used the history ("at or above baseline 1.6", "poorly controlled"). | FIXED: Cl 88, CO2 26 (gap 9), consistent with a thiazide-like diuretic; interpretation states values and eGFR. |
| B | minor | `patient.vitals.hr` | HR 45 while the ECG escape is 32 bpm. | FIXED: 33. |
| B | major | `initial_tool_outputs.ecg` | "Low-voltage QRS in limb leads" with echo LVH (contradiction and an unintended amyloid flag); "raising concern for torsades"; LAFB diagnosed inside an LBBB escape; rhythm "junctional/ventricular" with a 148 ms LBBB QRS. | FIXED: findings only, ventricular escape. |
| B | minor | `initial_tool_outputs.eeg.artifacts[0]` | Artifact "from scalp contusion" placed at T4/T6 while the contusion is parietal. | FIXED: P4. |
| B | major | `followup_outputs[0]` (echo) | AVA 0.9 with "moderate-to-severe" and no gradients; numbers overlapping S02 (LVEF 40%). | FIXED: full TTE report with his own numbers (Vmax 4.4 m/s, mean 46 mmHg, AVA 0.8 cm2, LVEF 46%, septum 1.4 / PW 1.3 cm, LAVI 42, TAPSE 19 mm, PASP 38 mmHg); the CMR volumes moved to match (160/86 mL, EF 46%, mass 186 g) and its interpretive phrases removed. |
| C | minor | `action-8-order-ct-scan`, `followup_outputs` CT, must | Head CT criterion cited [Strickberger_2006] and was repeated as a must; CT impression had a management sentence. | FIXED: rationale cites NICE NG232 (age 82, LOC, head strike); CT moved to `initial_tool_outputs.ct`; must deleted (plan I). |
| C | major | `followup_outputs` tilt and exercise, `avoided_actions` | Tilt and a Bruce test performed in complete heart block with severe AS (plan J, M). | FIXED: follow-ups deleted; tilt and exercise avoided as harm. EEG and brain MRI added as waste. |
| H | minor | all `action_criteria[*]` | "§" citations; rationale equal to label. | FIXED. New optional CMR criterion `action-7-order-advanced-imaging` (plan tier: CMR optional) so the stored CMR is scored, not just served. |
| A | minor | `stop_rule`, `sequence_constraints` | `max_additional_actions: 0`; no constraints. | FIXED: 2; soft ECG before TTE and before monitoring. |
| C | major | `ground_truth.assessment` | Musts "Urgent permanent pacing", "Hold AV-nodal blockers" (none taken), head CT; no valve plan, no latex precaution, no hyponatraemia plan; tilt prohibition (a test). | FIXED: musts are diagnosis, monitored bed with pads, dual-chamber pacemaker with latex precautions, Heart Team with TAVI favoured at 82, stop indapamide and correct sodium by no more than 10 mEq/L in 24 h with magnesium, hold telmisartan, driving. Prohibitions: AV-nodal drugs before pacing, fast sodium correction, vasodilators, discharge before pacing. |
| C | major | `ground_truth.differential` | VT moderate after telemetry; AS "should be confirmed on echo" though the echo stages it; orthostatic mechanism (two antihypertensives, hyponatraemia) not discussed. | FIXED: AS moderate (staged, contributing), VT low, orthostatic hypotension added as low, drug-induced block very low. |
| L | minor | `ground_truth.red_herrings` | Head-strike red herring now wrong (CT is indicated). | FIXED: replaced by the sodium of 123; greying-out red herring quotes the HPI. |
| E | minor | `metadata.clinical_pearls[3]` | "moderate-to-severe AS" as a Class I intervention indication. | FIXED: symptomatic severe AS. |

## Changes, in one paragraph a physician can read before re-reviewing

The 82-year-old man who collapsed walking to the bathroom and struck his head now has his own record (telmisartan, indapamide added 4 months ago, linagliptin), which explains his sodium of 123 and magnesium of 1.6. Required: ECG (complete AV block, wide LBBB escape at 32 bpm), TTE (severe calcific AS with AVA 0.8 cm2, mean gradient 46 mmHg, LVEF 46%) and inpatient telemetry (Holter accepted: escape 29-43 bpm, presyncope at 30 bpm, a 4.8 s pause); none of these numbers is shared with S02 any longer. Recommended: BMP and a head CT within 8 hours (NICE NG232). CMR, the medication review and the guideline lookup are optional; tilt and exercise are harm, EEG, brain MRI and CSF waste. Musts: diagnosis, monitored bed with pacing pads, dual-chamber pacemaker with latex precautions, Heart Team with TAVI favoured, stop indapamide with slow sodium correction, hold telmisartan, driving advice.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms and R55 still accepted; not hand-edited.
- Plan C3: tilt and exercise orders now get the library's normal reports; both are avoided as harm here.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Decision taken: the new medication list was built to explain the case's existing abnormal sodium, magnesium and urate rather than changing those values, so the hyponatraemia became a management must.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Read the full final case against the log and plan; the record and telemetry were rewritten, so every cross-field link was checked.
- Checked: record no longer shares medications, PMH, family or social history with S02; HPI indapamide sentence matches the medication list; eGFR about 40 (CKD-EPI 2021, male, 82, creatinine 1.7: recomputed 40) matches PMH; anion gap 9; echo LVEF 46% vs CMR 160/86 mL (46%); AS grading severe and concordant; ECG 32 bpm vs vitals 33 vs telemetry 29-43; scalp contusion right parietal in HPI, exam, CT and EEG artefact (P4); latex allergy carried into the pacing must; head CT recommended per NG232 (82 with loss of consciousness and a head strike); red-herring field path BMP[0] is sodium; leak guard passes.
- Found and changed:
  - The new PMH lists bilateral sensorineural hearing loss with hearing aids, but the exam still read "CN VIII: Hearing intact to finger rub bilaterally". Now "Hearing reduced bilaterally to finger rub without his hearing aids".
  - A must and a prohibition called him hypotensive at 106/55 mmHg. Reworded: hold telmisartan while blood pressure is low for him with severe aortic stenosis and hyponatraemia, reviewing antihypertensives after the valve decision; the prohibition is "Do not start or increase vasodilators in severe aortic stenosis".
  - Driving must allowed Group 1 driving 1 week after pacing with severe symptomatic aortic stenosis untreated; as in S02, driving is now restricted until the aortic stenosis has also been treated (ESC 2018 structural cardiac disease: until successful treatment).
  - Head-CT criterion `action-8-order-ct-scan` cited [ESC_2018]; set to [] (NICE NG232 named in the rationale).
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
- Valve guideline: ESC/EACTS 2025 replaces 2021 (TAVI threshold 70 years) in the literature result, rationales, must and pearl.
- Labels: complete heart block labels only (Mobitz II and second-degree labels removed: a different grade); I44.30 kept, I44.1, I44.39, I45.9 and R55 dropped.
- "ESC/EACTS 2021" renamed "ESC/EACTS 2025" (2025 ESC/EACTS valvular guideline, Praz 2025, supersedes 2021): `.ground_truth.action_criteria[3].rationale`, `.ground_truth.assessment.required_recommendations[3]`, `.ground_truth.avoided_actions[2].rationale`, `.metadata.clinical_pearls[3]`.
- Literature follow-up: Vahanian 2021 source replaced by Praz 2025 and the TAVI age threshold 75 by 70 years (tricuspid AS, transfemoral access feasible); evidence level written as "Class I" only.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-8-order-ct-scan citations [] -> ['[NICE_NG232]']; action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_EACTS_2025_VHD]']; action-7-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; avoid-harm-2-exercise-stress-test citations ['[ESC_2018]'] -> ['[ESC_EACTS_2025_VHD]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-S04` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure 'Active stand test not performed. Deferred by the clinical team.' (haemodynamically unstable or high-grade AV block at presentation: standing is not safe); no criterion |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

Departure from the decisions file: it named S04 for orthostatic BP (indapamide, telmisartan), but complete heart block at 33 bpm with severe aortic stenosis makes an active stand unsafe, so S04 gets the deferred report and no criterion.

| field path | change |
| --- | --- |
| `followup_outputs[8]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.alternatives: was [BMP]; now [BMP, magnesium] | [BMP].
- Decision: serve: new first alternative (old order kept as an alternative). A must repletes magnesium 1.6 on indapamide; the magnesium panel was not returned by BMP.
- Scoring: none (recommended criterion: coverage unchanged, not in the cost reference).

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-7-order-advanced-imaging` label: "Cardiac MRI to characterise the myocardium (optional)" -> "Cardiac MRI to characterise the myocardium"
- criterion `action-5-check-drug-interactions` label: "Review the medication list (indapamide, telmisartan) (optional)" -> "Review the medication list (indapamide, telmisartan)"
- criterion `action-6-search-medical-literature` label: "Guideline lookup on valve intervention and pacing (optional)" -> "Guideline lookup on valve intervention and pacing"
