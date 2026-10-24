# SYNC-CARD-RM03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for SYNC-CARD) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | followup_outputs[order_ct_scan], ground_truth.action_criteria[head CT] | Head CT follow-up was a placeholder equal to the key ("Rule out traumatic intracranial haemorrhage"); optional criterion although a temple bruise on aspirin alone at 58 meets no NICE NG232 criterion | FIXED (plan G, J): follow-up and criterion deleted; head CT waste (the normal fallback head CT answers an order) |
| B | major | initial_tool_outputs.ecg | "Sinus bradycardia at 46 bpm" with 3:2 Mobitz II: 46 bpm is the ventricular rate | FIXED: sinus rhythm, atrial rate 70, ventricular rate 46; "consistent with prior anteroseptal infarction versus septal fibrosis" reduced to "Q waves in V1-V3"; em dash removed |
| A | major | followup_outputs[monitoring], ground_truth.action_criteria[monitoring] | Ambulatory 24 h Holter with a patient diary in an admitted patient; holter_24h pinned | FIXED (plan E): inpatient telemetry 48 h with time stamps, symptom reported to the nurse; alternatives telemetry, holter_24h, holter_48h; same report as fallback monitoring |
| D | major | initial_tool_outputs.labs.panels["Exclusion studies"] | Engineering text ("which is what this case's diagnosis rests on") with magnesium "Within reference range" | FIXED: block deleted; magnesium 2.1 mg/dL in an Electrolytes panel |
| B | minor | initial_tool_outputs.labs.panels.Cardiac[troponin] | Troponin 0.04 flagged normal against a reference of <0.04 | FIXED: 0.02 ng/mL |
| A | minor | ground_truth.action_criteria[labs] | CBC+BMP+Mg+troponin pinned | FIXED (plan C): recommended, `panels: [BMP]` |
| A | major | ground_truth.action_criteria[drug], followup_outputs[drug] | Required with no `drug`; output titled "in a patient with Mobitz type II AV block" served to any drug query | FIXED (plan B, recommended): `{drug: atenolol}`; follow-up rewritten without the diagnosis, trigger `check_atenolol_interactions`; neutral medication-list review as initial and fallback |
| D | major | followup_outputs[literature x2] | Hypothyroidism references that cannot be verified as given; pacing follow-up with an empty summary and an unverifiable 1995 progression figure; literature required and in the stop rule | FIXED (plan A): optional; one follow-up citing ESC 2021 pacing, ESC 2018 syncope and ACC/AHA/HRS 2018 bradycardia, trigger `search_literature_mobitz_pacing`, last; hypothyroidism follow-up deleted; neutral initial literature |
| A | major | ground_truth.action_criteria[exercise test] | Recommended exercise test in symptomatic Mobitz II | FIXED (plan J): criterion deleted, exercise test waste; stored report kept with peak HR corrected to 44% of predicted (was 39%) |
| B | minor | followup_outputs[CMR] | Native T1 1120 ms identical to RS02/RS03 (plan M); impression omitted the LAD-territory scar | FIXED: T1 1090 ms; impression lists scar, LV size and EF |
| B | minor | followup_outputs[TTE] | No echo_type, empty valves, no LA or wall thickness | FIXED (plan G): full TTE report, same LVEF 38%, LVEDD 58 mm, TAPSE 20 mm, RVSP 32 mmHg |
| C | major | ground_truth.assessment.required_recommendations | "Hold AV-nodal blockers" without naming atenolol; no device choice despite LVEF 38%; no ischaemic evaluation of an LAD scar; aspirin not addressed | FIXED (plan RM03): see Changes |
| A | minor | ground_truth.assessment.prohibited_recommendations | "Do not call ..." engineering text; tilt prohibition | FIXED (plan H, I): deleted |
| C | minor | ground_truth.avoided_actions | No EEG, tilt, exercise or head CT avoidance; reasons did not name the diagnosis | FIXED: six waste entries, each naming the diagnosis |
| C | major | ground_truth.differential | VT moderate after telemetry; SSS "SNRT and EP help clarify" (not in the case); atenolol, TSH and family conduction disease missing | FIXED (plan K): VT and SSS low with telemetry results; atenolol-related block, subclinical hypothyroidism (low) and familial conduction disease (moderate) added |
| D | minor | ground_truth.red_herrings | data_points paraphrased; "normal EEG" (non-criterion tool) cited | FIXED: five quoted herrings (jerks, head strike, clinic seizure label, TSH, anaemia) |
| E | minor | all criteria, key_clinical_evidence | rationale equal to label; section citations, [Locati_2014], [Strickberger_2006]; "Head CT is justified by the head strike" | FIXED |
| A | major | ground_truth.sequence_constraints, stop_rule | None; stop rule with drug and literature, max 0 | FIXED: soft ECG before TTE and monitoring; stop rule ECG, TTE, monitoring, max 3 |

## Changes, in one paragraph a physician can read before re-reviewing
58-year-old man on atenolol, amlodipine and aspirin with three abrupt collapses in two months (one seated, one on stairs), brief jerks and a temple bruise. ECG: sinus rhythm 70 with 3:2 Mobitz II (ventricular rate 46), RBBB, LAFB and Q waves V1-V3; telemetry 48 h: frequent Mobitz II and high-grade block with 4.2 s (symptomatic) and 3.8 s pauses, no VT; TTE: LVEF 38% with anteroseptal and apical hypokinesis; CMR: LAD-territory scar into the septum. Required: ECG, TTE, monitoring; recommended: BMP, CMR, atenolol review; optional: literature; waste: brain MRI, CSF, head CT (no NG232 criterion), EEG, tilt, exercise test. Musts: monitored bed with pacing pads; permanent pacing without waiting for washout; CRT rather than RV pacing for LVEF below 40% (ESC 2021); hold atenolol, then an HFrEF beta-blocker and guideline therapy; coronary angiography; continue aspirin and atorvastatin; ECG screening of relatives; driving restriction until 1 week after implantation. Prohibitions: no AV-nodal blockers before pacing, no antiseizure drugs, no discharge without a pacing plan, no deferral of pacing for TSH or atenolol.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Neutral initial literature and drug answers kept (see P02 CENTRAL).
- Plan C2: coronary angiography is not in the vocabulary, so the ischaemic evaluation is a must, not a criterion.
- Synonyms (plan C1): generic "cardiac syncope" and "bradyarrhythmia" accepted.

## Open questions for Andrea (judgment calls you could not settle)
Both questions below were resolved by the verifier (see Verification); none remains open.
- I added musts the plan did not list because the case's own data require them: CRT instead of RV pacing (LVEF 36-38%, ESC 2021 Class I), holding atenolol, and coronary angiography for the LAD scar. A cardiologist should confirm. Whether a CRT-D rather than CRT-P is preferable (ischaemic scar, LVEF just above 35%, syncope) is left open; ESC 2022 recommends programmed ventricular stimulation in prior MI with unexplained syncope, but here the syncope is explained by documented high-grade block.
- Family history (father's sudden death at 52, brother paced at 55) suggests familial conduction disease alongside the ischaemic scar; I added relative screening as a must. Andrea may prefer to drop the family history instead.

## Verification
Adversarial verifier, 24 Oct 2026. Read the whole final case against the plan (RM03 bullets, sections A-O) and the log.
- Confirmed: no "Do not call" text; head-CT follow-up and criterion gone, head CT waste with an NG232 reason; exercise test waste (peak 72 = 44% of 162); CMR recommended, LVEF (198-127)/198 = 36%, LV mass 148/1.94 = 76 g/m2; drug check recommended (atenolol); musts include permanent pacing and continued aspirin; penicillin allergy not contradicted; ECG 3:2 at atrial 70 gives 46 bpm; differential low except familial conduction disease; stop rule = the three required criteria, max 3; ESC 2021, ESC 2018 and ACC/AHA/HRS 2018 statements in the literature follow-up are correct.
- Found and fixed:
  1. B (monitoring arithmetic), major: telemetry reported a 4.2 s pause as 4:1 block and a 3.8 s pause as 3:1 block with an atrial rate of 62-84 bpm. N:1 block gives a pause of N P-P intervals, so 4:1 gives at most 3.9 s and 3:1 at most 2.9 s at those atrial rates. Changed to 5:1 (4.2 s at about 71 bpm) and 4:1 (3.8 s at about 63 bpm), in the follow-up and the fallback (events and findings). No criterion or must quotes the ratios.
  2. M (template carry-over), minor: the ECG QTc 492 ms and the interpretation sentence "QTc 492 ms, partly attributable to the wide QRS" were identical to RM02, and TIBC 420 mcg/dL was identical too (both inherited from before the round). RM03 now has QTc 478 ms and TIBC 405 mcg/dL; nothing else in the case quotes either value.
  3. C/B, minor: the medication-list review (initial and fallback, served for any drug other than atenolol) did not mention that atenolol on the list slows AV conduction in a patient with Mobitz II. Added a warning in report voice to both blocks.
  4. C, minor (resolves the worker's first open question): the CRT must now says a CRT pacemaker. There is no ICD indication now: LVEF is 36-38% (above 35%) and the syncope is explained by documented AV block, so ESC 2022 programmed stimulation for unexplained syncope after MI does not apply. LVEF is reassessed for an ICD after revascularisation and optimised heart-failure therapy.
- Worker's second open question, resolved without a change: the family history (father's sudden death at 52, brother paced at 55) is part of the seed record and is kept; relative screening stays a must and familial conduction disease stays moderate.
- Left as is: "remote history of rheumatic fever in childhood" in the PMH predates the round and contradicts nothing (normal mitral leaflets); it may be carry-over from RM02 but could equally come from the seed, which I could not check.
- Re-ran `perfect_agent.py SYNC-CARD-RM03 -v` (ok), `case_io.py check` (clean for this case) and the case guards (pass).

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: Mobitz II and high-grade AV block labels only (complete heart block labels and I44.2 removed: monitoring shows no complete block); bare "second degree av block" retired (it credits Mobitz I); I44.30 kept, I44.39, I45.9 and R55 dropped.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-2-interpret-labs citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2021_Pacing]']; action-8-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; action-5-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; avoid-waste-3-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-RM03` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report with the orthostatic vitals already in the examination (138/82 HR 48; 1 min 126/78 HR 52; 3 min 118/74 HR 54, mild light-headedness); no criterion (the values are already given to the agent) |
| `followup_outputs[7] (`request_electrophysiology_study`)` | added: electrophysiology_study report. Infra-Hisian conduction disease: HV interval 92 ms, with 2:1 infra-Hisian block during incremental atrial pacing at 600 ms. |
| `ground_truth.action_criteria` | no electrophysiology criterion: the documented AV block (or VT) already settles the device decision; the stored report only keeps a library normal from contradicting the case |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.
