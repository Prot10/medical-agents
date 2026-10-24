# SYNC-CARD-M05
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `action-5-search-medical-literature`, `followup_outputs` literature | Literature required and in the stop rule; two of three sources unverifiable ("Katritsis & Josephson, Epidemiology and Natural History of SVT", "Brembilla-Perrot 2012 Syncope due to SVT"). | FIXED: optional with the canonical rationale; output rewritten with ESC 2019 SVT (vagal manoeuvres then adenosine; slow-pathway ablation Class I, drugs IIa) and REVERT (Lancet 2015); last in the list. |
| C | major | `action-6-check-drug-interactions`, `followup_outputs` drug check | Required without any interaction in the list; no drug named; the output proposed AV-nodal drugs generically and included a management note on lorazepam. | FIXED: recommended (plan B), alternatives adenosine, verapamil, metoprolol (the drugs the musts may start), one follow-up each (caffeine blunts adenosine; verapamil with beta-blocker; pre-excitation contraindication); `medication_list_review` in initial and fallback for any other drug. |
| C | major | `action-4-order-cardiac-monitoring`, monitoring outputs | Plan E: event_monitor_14d required, 30d accepted. Sudden palpitations immediately followed by syncope is an ESC 2018 major high-risk feature, for which immediate in-hospital ECG monitoring is Class I; the case had no answer for a telemetry or Holter order other than the library. | FIXED: event monitor required (alternatives 14d, 30d; trigger renamed so a loop-recorder order also receives it); new recommended criterion `action-7-order-telemetry` (telemetry, holter_24h, holter_48h) with a new non-diagnostic 24 h telemetry follow-up, also the `fallback_tool_outputs.cardiac_monitoring`. See Open questions. |
| C | minor | `action-2-interpret-labs` | Pinned CBC, troponin, TSH and beta-hCG; expected "TSH normal excluding hyperthyroidism". | FIXED: recommended `panels: [BMP]`, TSH accepted as an extra; beta-hCG kept in the output (52, no menopause recorded) but not required; interpretation plain. |
| B | minor | `followup_outputs[0]` (echo) | Chamber values without units ("46", "34"); no echo_type or TAPSE. | FIXED: units, echo_type TTE, TAPSE 23 mm; impression in echo voice. |
| A | minor | `stop_rule`, `sequence_constraints` | Stop rule included literature and drug check; `max_additional_actions: 0`; no sequence constraints. | FIXED: ECG, TTE, event monitor; 2; soft ECG before TTE and before monitoring. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated scored tests (ECG, monitoring); ablation phrased as a referral only; no pre-excitation condition on AV-nodal drugs; no disposition. | FIXED: diagnosis, modified Valsalva (REVERT) then adenosine, EP study and slow-pathway ablation (ESC 2019 Class I), AV-nodal drug bridge only after pre-excitation is excluded, outpatient management with expedited EP follow-up, driving. The "discharge without monitoring plan" prohibition dropped (the rhythm is documented). |
| C | major | `ground_truth.differential` | Panic attack "high", VT and AF/flutter "moderate" after the monitor captured a regular narrow 218-224 bpm short-RP tachycardia; vasovagal cited the off-pathway tilt. | FIXED: all low with the excluding result; AVRT entry notes that a concealed pathway is settled at EP study. |
| C | minor | `avoided_actions` | Tilt not penalised; rationales cited ACC_AHA_HRS for brain MRI and CT. | FIXED: tilt waste added; rationales name the diagnosis, CT per NICE NG232. |
| E | minor | `patient.history_present_illness`, `key_clinical_evidence` | Em dashes; "load-bearing role" engineering phrase. | FIXED: rewritten; ESC high-risk palpitation point added. |
| H | minor | all `action_criteria[*]` | Free-text "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label. | FIXED: keys only; real rationales. |

## Changes, in one paragraph a physician can read before re-reviewing

The 52-year-old woman with syncope immediately after sudden rapid palpitations now has three required steps (ECG without pre-excitation, normal TTE, 14- or 30-day external event monitor capturing a regular 218-224 bpm short-RP tachycardia with symptom correlation), plus recommended ED telemetry (non-diagnostic 24 h of sinus rhythm), a recommended BMP (TSH accepted) and a recommended review of adenosine, verapamil or metoprolol against her medication list. The literature lookup is optional and its content now comes from ESC 2019 SVT and REVERT. Brain MRI, CSF, EEG, head CT and tilt are waste. Musts: AVNRT as the cause, modified Valsalva then adenosine for recurrences, EP study with slow-pathway ablation, AV-nodal drugs only after pre-excitation is excluded, outpatient expedited EP follow-up, and driving advice. Panic disorder, VT and AF or flutter are now low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: the accepted list includes "ventricular tachycardia", "VT" and "tachyarrhythmia" and codes I47.2/I47.20 for an AVNRT case; not hand-edited.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. One deviation from the lead plan, decided on ESC 2018: the plan treats M05 as not high risk (holter optional), but "sudden onset palpitation immediately followed by syncope" is listed by ESC 2018 among the major high-risk features, for which immediate in-hospital monitoring is Class I. I therefore added a recommended ED telemetry step with a truthful non-diagnostic recording, while the event monitor stays the required, diagnostic study.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Checked every own-findings row against the file and the whole final case: event-monitor criterion (14d, 30d) and the stored 14-day report, the added recommended ED telemetry (the deviation is correct: ESC 2018 lists sudden palpitation immediately followed by syncope as a major high-risk feature), drug criterion and the adenosine, verapamil and metoprolol reports against the medication list and caffeine intake, beta-hCG kept but not required (52, no menopause recorded), musts (modified Valsalva, adenosine, slow-pathway ablation, pre-excitation caveat, disposition, driving), differential (the QRS 87 ms cited for VT is in the event-monitor events), the knee-contusion reason for the waste head CT (present in the exam), stop rule and leak guard.

Found and changed:
- `action-4-order-cardiac-monitoring.rationale` cited "Locati 2016" in text while the key is [Locati_2014] and the reference is under verification (plan C5). Removed the text citation; the rationale now cites ESC 2018 IIa only, and the existing key is kept as the plan allows.

Re-run: perfect_agent clean, case_io check clean for this case.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_psvt_avnrt_management` renamed to `search_psvt_avnrt_supraventricular_tachycardia`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.
- red herring 0 moved to `patient.history_present_illness`: the old data_point cited a PCP attribution absent from PMH[0]; it now quotes the HPI's anxiety and panic-attack attribution verbatim.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: SVT and AVNRT labels with I47.10 and I47.19; "ventricular tachycardia" and "VT" (a mimic in this case) and I47.2/I47.20 no longer accepted. Citation `[Locati_2014]` replaced by `[Locati_2016]` (SYNARR-Flash, Europace 2016;18:1265-1272; the old key's Heart 2016 reference could not be verified).
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-1-analyze-ecg citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2019_SVT]']; action-4-order-cardiac-monitoring citations ['[ESC_2018]', '[Locati_2014]'] -> ['[ESC_2018]', '[Locati_2016]']; action-6-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2019_SVT]']; avoid-waste-4-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-M05` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.
