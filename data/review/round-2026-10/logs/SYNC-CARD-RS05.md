# SYNC-CARD-RS05
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | monitoring follow-up | VT described as LBBB morphology with inferior axis, the signature of an outflow-tract origin, in a case whose substrate is an inferior (RCA) infarct scar, where VT exits with a superior axis. | FIXED: RBBB morphology with superior axis, matching the inferior scar; expected evidence and key evidence updated. |
| C | major | monitoring follow-up, criterion | Both runs called "sustained", but the 18 s asymptomatic run is non-sustained by definition (under 30 s without haemodynamic compromise). | FIXED: hour 6, 32 s with near-syncope = sustained; hour 31, 18 s = non-sustained. |
| B | minor | monitoring follow-up | "First-degree AV block (PR 172 ms)" (a PR under 200 ms is normal; the ECG reads PR 168 ms normal); `heart_rate_range` keys "maximum"/"minimum" and max 196 above the fastest VT (192). | FIXED: "PR 168-172 ms"; keys min/max, max 192; output named "Inpatient telemetry, 48 h"; same recording as the monitoring fallback. |
| B | major | `action-3-order-cardiac-monitoring` | Only `telemetry` accepted (plan E). | FIXED: telemetry, holter_24h, holter_48h. |
| D | minor | `initial_tool_outputs.labs` | "serial testing required/warranted" inside the lab report (management instruction). | FIXED: removed; the troponin value and flag stay. beta-hCG stays in the output and is not required (plan). |
| C | major | `action-2-interpret-labs`, `sequence_constraints[0]` | Pinned CBC, BMP, Mg, troponin and BNP; hard labs-before-monitoring constraint (delaying monitoring for blood results is the unsafe order). | FIXED: required `panels: [BMP, magnesium]` (plan C); hard constraint deleted; soft ECG before TTE and before monitoring. |
| C | minor | echo follow-up | No `echo_type`; "severely reduced" for LVEF 32% (30-40% is moderately reduced); no TAPSE, thrombus statement. | FIXED: `echo_type: TTE`, "moderately to severely reduced (32%, previously 38%)", TAPSE 19 mm, no LV thrombus, regional abnormality unchanged in distribution. |
| C | major | `action-6-check-drug-interactions`, drug outputs | Required without a drug; one mixed follow-up; empty "general" fallback with "(agent not specified on this case's diagnostic pathway)" (plan B, H). | FIXED: required, alternatives carvedilol and metoprolol (plan B); follow-ups per beta-blocker and for amiodarone (the planned drug); medication-list review (dual beta-blockade, furosemide K/Mg loss, spironolactone with lisinopril once K is repleted, Class IC and sotalol cautions) stored as initial and fallback drug output. |
| C | major | `action-5-search-medical-literature`, `stop_rule`, literature outputs | Literature required and in the stop rule; follow-up cited "Zipes and Wellens 1998" under a wrong title and gave patient-level conclusions; fallback "No directly applicable ... evidence. Recommend ...". | FIXED: optional, canonical rationale; follow-up from ESC 2022 VA (ICD Class I; ablation over escalating AAD) and AHA/ACC/HRS 2017; fallback literature deleted (the library answers). |
| C | major | `ground_truth.assessment` | "Obtain serial troponin" must (a test as a must, plan I); "Electrophysiology consult for ICD evaluation" instead of the decision; "Do not perform tilt-table" as a prohibition; no ablation, ischaemia or driving detail. | FIXED: musts are diagnosis, monitored bed with pads and cardioversion for recurrence, K 4.0-5.0 and Mg repletion with furosemide review, secondary-prevention ICD before discharge (ESC 2022 Class I), single beta-blocker, amiodarone or ablation for recurrences, ischaemia evaluation (coronary angiography), driving (3 months after a secondary-prevention ICD, Group 1). Prohibitions: Class IC, sotalol, discharge without ICD plan, electrolytes as definitive therapy. |
| C | major | `avoided_actions` | Tilt and exercise not penalised. | FIXED: brain MRI, EEG, head CT (knee strike only, age 56, no anticoagulant), CSF, tilt, exercise as waste, each naming the diagnosis. |
| C | major | `ground_truth.differential` | ACS left moderate although the echo shows no new wall motion abnormality and the VT is scar-type monomorphic; dual beta-blockade not considered as a bradyarrhythmic mechanism. | FIXED: ACS low (ischaemia still evaluated by a must), electrolyte-only arrhythmia low, bradyarrhythmia from dual beta-blockade low (no pauses on telemetry), vasovagal and orthostatic very low. |
| L | minor | `red_herrings` | data_point merged two analytes under one field path. | FIXED: data_point "Potassium 3.2 mEq/L" at BMP[1]; red herring added for the palpitations attributed to anxiety. |
| A | minor | all criteria, `stop_rule` | Free-text section citations, rationale equal to label, `max_additional_actions: 0`. | FIXED: keys only, real rationales; stop rule lists the five required criteria with 3 additional actions. |

## Changes, in one paragraph a physician can read before re-reviewing

The 56-year-old woman with ischaemic cardiomyopathy (prior inferior STEMI, LVEF 32%) and syncope now has five required steps: ECG, potassium and magnesium (3.2 and 1.6 on furosemide), TTE, inpatient telemetry (Holter accepted) and a medication review that finds carvedilol and metoprolol taken together. Telemetry captures one sustained run of monomorphic VT at 188 bpm with near-syncope and one non-sustained run; the VT morphology is now RBBB with a superior axis, which fits the inferior scar (it was LBBB with an inferior axis, an outflow-tract pattern). The hard labs-before-monitoring constraint and the serial-troponin must are gone; literature is optional and correctly cited. Musts: monitored bed with cardioversion available, electrolyte repletion, secondary-prevention ICD before discharge (ESC 2022 Class I), one beta-blocker only, amiodarone or ablation for recurrences, ischaemia evaluation for the mildly raised troponin, driving advice. Class IC drugs and sotalol are prohibited. ACS is low with a must to evaluate ischaemia.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: this VT case accepts "supraventricular tachycardia", "SVT", "AVNRT" and I47.1 as synonyms, so an SVT answer scores as correct; and "cardiac syncope", "arrhythmic syncope", "tachyarrhythmia" are generic. Not hand-edited.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea.

## Verification

Checked (24 Oct 2026, adversarial pass): the log against the diff from fa1d22e6 and the whole final case; VT morphology (RBBB, superior axis) consistent across telemetry, key evidence and criterion; sustained (32 s, symptomatic) vs non-sustained (18 s) runs; telemetry fallback identical; heart_rate_range against the events; labs (K 3.2, Mg 1.6) against the labs criterion and red herring field path (BMP[1] is potassium); required drug check placed after the diagnostic core; stop rule lists the five required criteria; ICD must against ESC 2022 Class I; musts vs prohibitions.

Found and changed:
- Initial and fallback drug output (served for any drug at any time) quoted results the agent may not have obtained: "Sotalol with LVEF 32%, QTc 468 ms and hypokalaemia" (LVEF 32% is the new echo value; the HPI gives 38%) and "the loop diuretic is the likely cause of the low potassium and magnesium" (lab result). Rewritten as general cautions (sotalol in reduced LVEF, QT prolongation or hypokalaemia; loop diuretic causes potassium and magnesium loss); both copies identical.
- Amiodarone follow-up warning "Baseline QTc 468 ms." (an ECG value in a drug report) now "Record a baseline QTc and monitor it during loading."
- Exercise is waste, but no exercise output was stored, so an exercise order received the library report (10.4 METs, sinus rhythm throughout, normal), which contradicts LVEF 32% and her limited exercise tolerance. Added a case-consistent `order_specialized_test` exercise follow-up before the literature (3.8 METs, chronotropic response 76% of predicted on two beta-blockers, blunted BP, frequent PVCs of the scar morphology and a 4-beat NSVT run in recovery), the same fix RS01-RS03 received.

perfect_agent clean, `case_io.py check` clean for this case, leak guard passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: VT labels scoped to this case (VT is its diagnosis) with I47.20 and I47.29; SVT and AVNRT removed.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-2-interpret-labs citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2022_VA_SCD]']; action-4-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2022_VA_SCD]']; avoid-waste-3-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-RS05` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure 'Active stand test not performed. Deferred by the clinical team.' (haemodynamically unstable or high-grade AV block at presentation: standing is not safe); no criterion |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

| field path | change |
| --- | --- |
| `followup_outputs[7]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |
