# SYNC-CARD-P01
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | The HPI gave the ED ECG result ("again shows normal sinus rhythm with occasional premature ventricular complexes"). | FIXED: replaced by "A repeat 12-lead ECG has been requested." The outside-hospital ECG read stays as history and is now a red herring. |
| B | major | `patient.clinical_history.social_history.occupation` | The occupation was "librarian" but the HPI describes a high school basketball coach carrying equipment at school. | FIXED: "High school physical education teacher and basketball coach". |
| B | major | `action-1-analyze-ecg.expected_evidence`, `initial_tool_outputs.ecg` | The expected evidence claimed epsilon waves and T-wave inversion in V1-V3, but the ECG reported no epsilon wave and T-wave inversion in V1-V2 only, with a hedging "may be normal variant" sentence. | FIXED: ECG reports T-wave inversion in V1-V3 without RBBB, LBBB inferior-axis PVCs, no epsilon wave, QTc 448 ms, in finding voice; expected evidence matches. |
| B | minor | `initial_tool_outputs.labs` | Na 146 and Cl 113 (H) without a cause; troponin I 0.05 (H) while the expected evidence said "troponin negative". | FIXED: Na 141, Cl 104, troponin I 0.02; summary and interpretation updated. |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, magnesium and troponin. | FIXED: recommended `panels: [BMP]` (plan C); extras accepted. |
| G | major | `followup_outputs` echo | Lab-style impression ("Abnormal values: ... qualitative (H)"), values without units, no echo_type, no LVOT gradient or AS statement. | FIXED: full TTE report (echo_type TTE, trigger renamed): LVEF 58% biplane, wall 1.1 cm, no LVOT gradient at rest or on Valsalva, no AS, dilated RV (PLAX RVOT 34 mm, basal 4.6 cm), FAC 30%, TAPSE 16 mm, basal subtricuspid akinesia; no diagnosis sentence. |
| O/B | major | `followup_outputs` CMR | "(major criterion)" annotations, a "meet major Task Force Criteria" sentence and "severely" grading; RVEDV 124 with RVESV 72 gives RVEF 42%, not the stated 34%. | FIXED: annotations and conclusion deleted; RVESV 82 mL/m2 (RVEF 34%); findings only, no LV late enhancement stated. |
| C/B | major | `followup_outputs` monitoring, `action-4-order-cardiac-monitoring` | 24 h Holter pinned (holter_24h) under a telemetry label; 2,847 PVCs at an average of 72 bpm is 2.7%, not 3.3%; the NSVT was "walking in the hallway" on an outpatient Holter. | FIXED: alternatives telemetry, holter_24h, holter_48h; "Inpatient telemetry, 24 h" with 3,420 PVCs (3.3%), trigger `request_telemetry_holter_monitoring`; same recording as `fallback_tool_outputs.cardiac_monitoring`. |
| C | major | `followup_outputs` exercise test, `action-6-order-specialized-test` | Required; the VT was 12 beats then polymorphic for 18 s, self-terminating, which is not the sustained VT of the diagnosis label; defibrillation "not required" stated twice; no ST-segment statement. | FIXED: recommended (plan); sustained monomorphic VT 210 bpm, LBBB with superior axis, syncope, BP 62/40, synchronised cardioversion after 40 s; no ischaemic ST change. Hard TTE-before-exercise constraint added. |
| C | major | `ground_truth.action_criteria` (new `action-9-order-coronary-cta`) | A 55-year-old man with hypertension and prediabetes and exertional VT had no coronary assessment and coronary disease was missing from the differential. | FIXED: recommended coronary CTA or invasive angiography, each with a stored non-obstructive report; CAD added to the differential as low. See Open questions. |
| C | major | `action-7-check-drug-interactions`, drug outputs | Required with no drug named; the only stored drug report was levetiracetam. | FIXED: recommended (plan B), alternatives metoprolol, bisoprolol, sertraline, one report each (sertraline CYP2D6 effect on metoprolol, additive hypotension, sertraline conditional QT risk); `medication_list_review` in initial and fallback; levetiracetam report kept and cleaned. |
| H/C | major | `action-8-search-medical-literature`, literature outputs | Required; cited a "2020 Revised Task Force Criteria" paper, a Sheldon/Rose Neurology paper and a 14-patient Corrado series that cannot be verified; a fallback literature block with generic conclusions. | FIXED: optional with the canonical rationale; one follow-up (last) with Marcus 2010 (Circulation 2010;121:1533-1541) and ESC 2022 VA/SCD; fallback literature deleted. |
| A | minor | `stop_rule`, `sequence_constraints` | Stop rule included exercise, drug check and literature; `max_additional_actions: 0`; no constraints. | FIXED: ECG, TTE, monitoring, CMR; 3; soft ECG before TTE and monitoring; hard TTE before exercise. |
| H | minor | `ground_truth.assessment.prohibited_recommendations` | "Do not call `order_specialized_test`..." text and a tilt prohibition (a test, not management). | FIXED: deleted; tilt is an avoided action. Remaining prohibitions phrased as management. |
| C | major | `ground_truth.assessment.required_recommendations` | CMR must restated a scored test; no ICD class, no driving, no disposition detail, no action on the levetiracetam already given. | FIXED: diagnosis with convulsive syncope, secondary-prevention ICD (ESC 2022 Class I), beta-blocker, exercise restriction, genetic counselling and testing, cascade screening, admission with monitoring until the ICD, stop levetiracetam, no driving for 3 months. |
| C | minor | `ground_truth.avoided_actions` | No EEG or tilt entry; CT and CSF rationales did not name the diagnosis; CT ignored the outside-hospital scan. | FIXED: EEG and tilt waste added; all rationales name ARVC with exercise-induced VT; CT per NICE NG232 with the prior scan. |
| C | major | `ground_truth.differential` | HCM "high" (with "young athlete" for a 55-year-old), CPVT and LQTS/Brugada "moderate" after the pathway excluded them; no CAD, idiopathic RVOT VT or sarcoid. | FIXED: all low with the excluding result; CAD, idiopathic RVOT VT and cardiac sarcoidosis added as low. |
| L | minor | `ground_truth.red_herrings` | The EEG red herring sat in an off-pathway tool; the ECG red herring quoted text absent from the field. | FIXED: EEG and ECG entries replaced by the outside-hospital "normal" ECG read and the earlier stair near-blackout, both quoted from the HPI. |
| D | minor | `initial_tool_outputs.eeg.limitations` | "Exercise provocation was not performed" hinted at the exercise test. | FIXED: sentence removed. |
| E/H | minor | `key_clinical_evidence`, `metadata.clinical_pearls`, exam fields | Em dashes; "young athlete"; an unsourced "up to 12%" figure. | FIXED: rewritten; Task Force categories named per Marcus 2010. |
| H | minor | all `action_criteria[*]` | Free-text "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label. | FIXED: keys only; real rationales. |

## Changes, in one paragraph a physician can read before re-reviewing

The 55-year-old coach referred as new-onset seizures after two collapses while sprinting now needs four steps: a 12-lead ECG (T-wave inversion V1-V3, LBBB inferior-axis PVCs), a TTE that excludes aortic stenosis and obstructive HCM and shows a dilated, hypokinetic RV, inpatient telemetry (3.3% PVC burden, one 8-beat NSVT run) and cardiac MRI (RVEDV 124 mL/m2, RVEF 34%, free wall dyskinesia and aneurysm, normal LV). Coronary assessment by CTA or angiography (non-obstructive), a monitored exercise test after the TTE (sustained monomorphic VT with superior axis and syncope, cardioverted), a BMP and a review of the planned beta-blocker against sertraline and the antihypertensives are recommended. The literature lookup is optional and cites the real 2010 Task Force paper and ESC 2022. Brain MRI, head CT, CSF, EEG and tilt are waste. Musts: ARVC diagnosis with convulsive syncope, secondary-prevention ICD, beta-blocker, permanent exercise restriction, genetic counselling and testing, cascade screening of relatives, admission with monitoring until the ICD, stopping levetiracetam, and no driving for 3 months.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: the accepted list includes "supraventricular tachycardia", "SVT" and "AVNRT" and code I47.1 for a VT case, plus the generic "cardiac syncope", "arrhythmic syncope" and "tachyarrhythmia"; not hand-edited.
- An `order_echocardiogram` with `echo_type: TEE` falls through to the library normal report (normal RV), which contradicts this case; consider a library answer that says no study is stored (as in C3).

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Two deviations from the lead plan, both logged above. First, a recommended coronary assessment (coronary CTA or invasive angiography) was added: a 55-year-old man with hypertension and prediabetes and exertional sustained VT needs coronary disease excluded before the VT is attributed to ARVC (ESC 2022). Second, the exercise report was rewritten so that the VT is sustained (40 s, cardioverted for haemodynamic collapse): the original 18-second self-terminating run did not support the diagnosis label or the Class I ICD must in the plan. The plan's "delete the isoproterenol tilt" is applied: the tilt follow-up is gone and the library passive tilt answers a wasted order.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Checked every own-findings row against the file and the whole final case: HPI no longer gives the ED ECG result (the outside-hospital read is history and a red herring with a matching quote); ECG with T-wave inversion V1-V3 and no epsilon wave against the ECG expected_evidence; echo (PLAX RVOT 34 mm, FAC 30%, no LVOT gradient, no AS) and CMR arithmetic (RVEF (124-82)/124 = 34%, LVEF 59%), both meeting 2010 Task Force major imaging criteria; telemetry PVC burden; the rewritten exercise test (sustained VT, cardioverted) against the label and the Class I ICD must; hard TTE-before-exercise constraint; coronary CTA and angiography modalities exist in costs.yaml; drug reports against the medication list; literature content (Marcus 2010, ESC 2022); musts (ICD, beta-blocker, exercise restriction, genetics, cascade screening, admission, driving 3 months); differential; stop rule; leak guard. The two logged deviations (recommended coronary assessment; sustained VT on the exercise test) are clinically sound and were left.

Found and changed:
- Levetiracetam drug report (`check_drug_interactions_levetiracetam`) proposed "Levetiracetam 500 mg twice daily", a regimen the case never gives: the HPI records a single 1000 mg IV loading dose at the outside hospital and the medication list has no levetiracetam. Changed `proposed` to "Levetiracetam (1000 mg IV loading dose given at the outside hospital)".

Re-run: perfect_agent clean, case_io check clean for this case, leak guard passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_literature_arvc_exertional_syncope` renamed to `search_arvc_arrhythmogenic_right_ventricular_cardiomyopathy`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: ARVC labels and I42.8 only. "ventricular tachycardia", "VT", "SVT" and "AVNRT" removed: idiopathic RVOT VT and ischaemic VT, the case's mimics, contain the VT tokens. Residual: the primary code I47.2 still credits a VT answer that submits it (code-alone scorer item, CENTRAL).
- "ESC/EACTS 2021" renamed "ESC/EACTS 2025" (2025 ESC/EACTS valvular guideline, Praz 2025, supersedes 2021): `.ground_truth.sequence_constraints[2].reason`.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-1-analyze-ecg citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ARVC_TFC_2010]']; action-5-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ARVC_TFC_2010]']; action-9-order-coronary-cta citations ['[ESC_2018]'] -> ['[ESC_2022_VA_SCD]']; action-7-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2022_VA_SCD]']; avoid-waste-2-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]']; action-3-order-echocardiogram->action-6-order-specialized-test citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2023_Cardiomyopathy]', '[ESC_EACTS_2025_VHD]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-P01` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report, supine values = the presenting vitals; No orthostatic fall in blood pressure and no excessive heart rate rise on active standing. |
| `ground_truth.action_criteria[action-orthostatic-blood-pressure]` | added, recommended, after the ECG criterion [ESC_2018] (decisions CENTRAL 1: orthostatic BP in every initial evaluation) |
| `followup_outputs[11] (`request_electrophysiology_study`)` | added: electrophysiology_study report. Inducible sustained monomorphic ventricular tachycardia of LBBB morphology with superior axis at about 210 bpm, matching the clinical VT. Normal AV conduction. |
| `ground_truth.action_criteria` | no electrophysiology criterion: the documented AV block (or VT) already settles the device decision; the stored report only keeps a library normal from contradicting the case |
| `followup_outputs[12] (`request_cardiomyopathy_gene_panel`)` | added: genetic_panel:cardiomyopathy report. Heterozygous pathogenic PKP2 variant c.2146-1G>C (canonical splice acceptor, predicted loss of function) |
| `ground_truth.action_criteria[action-genetic-panel]` | added, recommended [ESC_2022_VA_SCD]; the assessment must on genetic counselling and testing is unchanged |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.
