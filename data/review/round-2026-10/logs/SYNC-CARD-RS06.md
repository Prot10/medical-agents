# SYNC-CARD-RS06
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `assessment`, `key_clinical_evidence`, `metadata.clinical_pearls`, literature follow-up | Anticoagulation framed on CHA2DS2-VASc (plan H). Components checked against the record: age 67 (1), hypertension (1), diabetes (1); no heart failure (LVEF 55%), stroke or vascular disease: CHA2DS2-VA 3. | FIXED: CHA2DS2-VA 3 throughout, with the ESC 2024 AF Class I indication for a DOAC. |
| C | major | `action-5-search-medical-literature`, `stop_rule`, literature follow-up, literature fallback | Literature required and in the stop rule; follow-up cited a non-existent "ACC/AHA/HRS 2019 focused update on catheter ablation" and a CHA2DS2-VASc review; fallback "Correlate with current society guidelines". | FIXED: optional, canonical rationale; follow-up from ESC 2019 SVT (CTI ablation; no class IC without AV-nodal blockade), ESC 2024 AF (CHA2DS2-VA) and ESC 2018 syncope; placed last; fallback literature deleted (the library answers). |
| C | major | `action-6-check-drug-interactions`, drug outputs | Required with no drug; one mixed metoprolol plus apixaban follow-up; empty "general" fallback "(agent not specified on this case's pathway)" (plan B, H). | FIXED: recommended, alternatives metoprolol, bisoprolol, apixaban, rivaroxaban (the drugs the musts start; none rate-slowing on the list); one follow-up per drug with doses checked against the record (apixaban 5 mg twice daily, creatinine 1.1); a medication-list review (thiazide potassium loss, class IC without AV-nodal blockade, beta-blocker with diltiazem or verapamil, no anticoagulant on the list) stored as initial and fallback drug output, so other drugs get the review and not another drug's report. |
| C | minor | `action-2-interpret-labs` | Recommended with CBC, BMP, glucose, troponin and TSH pinned. | FIXED: `panels: [BMP]` (plan C), TSH accepted as an extra; lab interpretation reduced to findings (K 3.6 low-normal noted). |
| B | major | `action-3-order-cardiac-monitoring`, monitoring follow-up | Only telemetry accepted; no case fallback; "patient activated event marker with diary notation" in inpatient telemetry; 48 h of untreated 2:1 flutter; 1:1 conduction at 300 bpm reported with narrow QRS only. | FIXED: telemetry, holter_24h, holter_48h; "Inpatient telemetry, 24 h" with the 1:1 run at hour 2 (before rate control), aberrant wide QRS during 1:1, loss of consciousness witnessed by the nurse; same recording as the monitoring fallback. |
| C | minor | echo follow-up | No `echo_type`; management sentence "formal exclusion ... requires TEE if cardioversion is planned". | FIXED: full TTE report (LVEF 55% biplane, LAVI 40, RA area, TAPSE 21 mm, aortic velocity), the appendage noted as not adequately visualised, no management text. |
| B | minor | `initial_tool_outputs.ecg` | Flutter wave polarity not described, so the typical (CTI-dependent) pattern that justifies CTI ablation was not in the record. | FIXED: negative sawtooth in II, III, aVF and positive in V1; interpretation names typical counterclockwise flutter. |
| C | major | `ground_truth.assessment` | "Do not perform tilt-table testing" as a prohibition; "Initiate continuous inpatient telemetry" (a scored test as a must); no class IC caution; no cardioversion anticoagulation rule. | FIXED: musts are diagnosis, monitoring with pads and synchronised cardioversion if unstable, beta-blocker rate control, DOAC per CHA2DS2-VA 3 (ESC 2024 Class I), CTI ablation (ESC 2019 SVT Class I), driving. Prohibitions: class IC without AV-nodal blockade, elective cardioversion without 3 weeks of anticoagulation or TEE, discharge without rate control and anticoagulation, attribution to anxiety. |
| C | major | `avoided_actions` | Exercise test not penalised; reasons did not name the diagnosis. | FIXED: brain MRI, CSF, EEG, head CT (no head strike: no NG232 criterion), tilt and exercise (adrenergic drive can provoke 1:1) as waste, each naming the diagnosis. |
| C | major | `ground_truth.differential` | Atrial fibrillation "high" and AVNRT "moderate" after the ECG shows sawtooth flutter with fixed ratios (plan K). | FIXED: AF low (I48.91), AVNRT low, VT low (wide complexes only during 1:1, aberration), SND low, thyrotoxicosis very low (TSH 2.1, new), vasovagal very low. |
| L | minor | `red_herrings` | data_points paraphrased the HPI; one correct_interpretation asserted 4:1 conduction, but 4:1 of a 296 bpm flutter gives 74 bpm, not the 88 bpm recorded. | FIXED: data_points quote the HPI; the office ECG is explained as taken between paroxysms or misread during higher-grade block. |
| A | minor | all criteria, `stop_rule`, `sequence_constraints` | Free-text section citations, rationale equal to label, `max_additional_actions: 0`, no constraints. | FIXED: keys only, real rationales; stop rule ECG, TTE, telemetry with 3 additional actions; soft ECG before TTE and before monitoring. |
| E | minor | `metadata` | Fallback kinds and difficulty rationale described the old pathway (required literature and drug checks). | FIXED: updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The 67-year-old man who collapsed at his kitchen counter has typical atrial flutter (negative inferior, positive V1 flutter waves) with 2:1 conduction at 148 bpm on arrival. Required: ECG, TTE and inpatient telemetry (Holter accepted); recommended: BMP (TSH accepted) and an interaction check for the planned beta-blocker or DOAC; the literature lookup is optional. Telemetry captures 18 s of 1:1 conduction at about 300 bpm with aberrant wide QRS and witnessed loss of consciousness. Anticoagulation now uses CHA2DS2-VA, score 3 (age 65-74, hypertension, diabetes). Musts: monitoring with pads and cardioversion if unstable, beta-blocker rate control, DOAC, CTI ablation (ESC 2019 SVT Class I), no driving until treated. Prohibited: class IC drugs without AV-nodal blockade, elective cardioversion without 3 weeks of anticoagulation or TEE. Brain MRI, CSF, EEG, head CT, tilt and exercise are waste. The differential is updated to the results, with every alternative low or very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: "cardiac syncope" is accepted as a generic synonym; not hand-edited.
- Plan C4: no citation key for ESC 2019 SVT or ESC 2024 AF; both are cited by name in rationale and must text.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Deviation from the lead plan, decided for dataset quality: exercise testing added as waste (adrenergic drive before rate control can provoke 1:1 conduction); the plan's subtype row lists only tilt, MRI and EEG.

## Verification

Checked (24 Oct 2026, adversarial pass): the log against the diff from fa1d22e6 and the whole final case; CHA2DS2-VA 3 against the record (age 67, hypertension, diabetes; LVEF 55%, no vascular disease); ECG typical flutter pattern; telemetry arithmetic (300/4 = 75 bpm during 4:1, max 304) and fallback identical; DOAC doses (apixaban reduction criteria, rivaroxaban 15 mg at CrCl 15-49); ESC 2019 SVT, ESC 2024 AF and ESC 2018 statements in the literature output; red herring quotes; tilt fallback carries `test_type: tilt_table`, so it answers only tilt orders.

Found and changed:
- Initial and fallback drug output read a lab value ("potassium 3.6 mEq/L is low-normal"), and the apixaban and rivaroxaban follow-ups quoted "(creatinine 1.1 mg/dL here)": results the agent may not have ordered (labs are only recommended). Rewritten as general statements (thiazide potassium and magnesium loss, check potassium; the dose-reduction criteria without the patient's value).
- Exercise is waste, but no exercise output was stored, so an exercise order received the library report ("sinus rhythm throughout", 10.4 METs), contradicting persistent flutter. Added a case-consistent exercise follow-up (stopped in stage 1 when 2:1 flutter changed to 1:1 at about 300 bpm with aberrancy and hypotension), consistent with the avoided-action reason.
- `followup_outputs` order: the off-pathway brain MRI and head CT sat before the drug checks; reordered to echo, telemetry, drug checks, off-pathway (MRI, CT, exercise), literature last (plan section 3).

perfect_agent clean, `case_io.py check` clean for this case, leak guard passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_atrial_flutter_guidelines` renamed to `search_atrial_flutter`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: flutter labels plus "typical atrial flutter" and I48.92.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-2-interpret-labs citations ['[ESC_2018]'] -> ['[ESC_2024_AF]']; avoid-waste-4-order-ct-scan citations ['[ACC_AHA_HRS_2017]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-RS06` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure 'Active stand test not performed. Deferred by the clinical team.' (haemodynamically unstable or high-grade AV block at presentation: standing is not safe); no criterion |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

| field path | change |
| --- | --- |
| `followup_outputs[10]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
