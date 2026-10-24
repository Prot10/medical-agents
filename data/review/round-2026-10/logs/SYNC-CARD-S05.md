# SYNC-CARD-S05
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `followup_outputs` literature (`search_literature_as_syncope`), `action-5-search-medical-literature` | Required literature criterion; its follow-up repeated the expected_evidence (leak guard failure) and cited "Natural history of adults with asymptomatic, hemodynamically significant aortic stenosis" as JACC 2000 for the 3-year survival after syncope (wrong source and year; that figure is the classic Ross and Braunwald natural-history series). | FIXED: optional, canonical rationale, out of the stop rule; follow-up rewritten with ESC/EACTS 2021 (intervention criteria, TAVI at 75 or more) and ESC 2018 (echo Class I) only, placed last. |
| E | major | `fallback_tool_outputs.drug_interactions.general`, `fallback_tool_outputs.literature_search` | "(agent not specified on this case's primary pathway)"; "No directly applicable ... evidence" followed by a recommendation. | FIXED: drug fallback is a `medication_list_review`; literature fallback deleted. |
| C | major | `action-6-check-drug-interactions`, `followup_outputs` drug | Required with no drug; output warned about diuretics he does not take. | FIXED: recommended (plan B) with alternatives amlodipine and lisinopril, one follow-up each, reviewing his actual four drugs (vasodilators in severe AS, nitrates and PDE5 inhibitors, penicillin allergy). |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin and glucose. | FIXED: recommended `panels: [BMP]`; expected_evidence normal electrolytes and creatinine 1.1, troponin not elevated, BNP 312. |
| B | major | `followup_outputs` monitoring, `action-4-order-cardiac-monitoring` | Criterion pinned telemetry only; trigger lacked the holter token; no case fallback (the library is also normal here, but plan E applies). | FIXED: alternatives telemetry, holter_24h, holter_48h; trigger `request_telemetry_holter_monitoring`; impression begins "Inpatient telemetry, 24 h"; same recording as `fallback_tool_outputs.cardiac_monitoring`. |
| B | minor | `followup_outputs[0]` (echo) | No echo_type, TAPSE, stroke volume, LVOT statement (needed to exclude HOCM, which the differential relies on). | FIXED: echo_type TTE; no dynamic LVOT obstruction or SAM, SVi 44 mL/m2, TAPSE 22 mm, no mass. |
| B | minor | `patient.neurological_exam.additional` | "narrow pulse pressure noted" with 118/78 mmHg (pulse pressure 40). | FIXED: phrase removed. |
| C | major | `followup_outputs` tilt | Tilt performed in severe AS; avoided as harm (plan J: delete). | FIXED: follow-up deleted. |
| C | major | `ground_truth.assessment` | Musts restated scored tests ("Obtain echocardiogram urgently", "Recognize BNP"); "Admit ... to exclude concurrent arrhythmia"; no driving or exertion advice; prohibitions of tilt and exercise (tests, already avoided) and of discharge "without echocardiographic assessment". | FIXED: musts are diagnosis, admission until the Heart Team decision, Heart Team with TAVI favoured at 78 including coronary assessment and planning CT, caution with vasodilators, no strenuous exertion or driving until treated. Prohibitions: discharge before the decision, deconditioning attribution, potent vasodilators. |
| C | major | `ground_truth.differential` | Arrhythmic syncope moderate after normal ECG conduction and telemetry; HOCM excluded by a Valsalva murmur sign not in the case. | FIXED: arrhythmic low with the telemetry evidence; HOCM cites the echo (no LVOT obstruction, no SAM); PE cites the normal RV. |
| H | minor | all `action_criteria[*]`, `avoided_actions` | "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label; avoided rationales cited "ACC/AHA Class III" without a key. | FIXED: keys only, real rationales naming ESC 2018 / ESC/EACTS 2021; avoided reasons name the diagnosis; CT waste reason cites NG232. |
| A | minor | `stop_rule`, `sequence_constraints` | Stop rule required the literature and drug checks; `max_additional_actions: 0`; no constraints. | FIXED: ECG, TTE, monitoring; 2; soft ECG before TTE and before monitoring. |
| L | minor | `ground_truth.red_herrings[0]` | data_point paraphrased. | FIXED: quotes the HPI. |
| E | minor | `ground_truth.key_clinical_evidence`, `metadata` | Em dashes; "required tool count is 6". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The 78-year-old man with exertional syncope and a classic aortic stenosis murmur keeps his presentation and results: ECG with LVH and strain, severe high-gradient aortic stenosis on TTE (AVA 0.7 cm2, mean 52 mmHg, Vmax 4.6 m/s, LVEF 62%, now also stating no LVOT obstruction) and 24 h of normal inpatient telemetry (Holter accepted). Required: ECG, TTE, monitoring. Recommended: BMP and a medication review naming amlodipine or lisinopril. The guideline lookup is optional and its report now cites only ESC/EACTS 2021 and ESC 2018 correctly. Tilt and exercise remain harm (the stored tilt report was removed); brain MRI, EEG, CSF and head CT are waste. Musts: diagnosis, admission until the Heart Team decision, Heart Team with TAVI favoured at 78 with coronary assessment and planning CT, cautious vasodilators, no strenuous exertion or driving until treated. The arrhythmic alternative is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: "cardiac syncope" still accepted for this case; not hand-edited.
- Plan C3: a tilt order (avoided as harm) now gets the library's normal tilt report.

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Read the full final case against the log and plan.
- Checked: severe AS grading (AVA 0.7, mean 52, Vmax 4.6, SVi 44) consistent across echo, expected_evidence, musts and key evidence; no LVOT obstruction or SAM stated, as the HOCM differential now relies on it; normal telemetry consistent with the low arrhythmic differential; drug follow-ups and fallback match his four medications and the penicillin allergy; driving and exertion must already conditional on valve treatment; tilt and exercise harm, CT waste (slid down two steps, no head injury); leak guard passes.
- Found and changed:
  - Echo `chambers` gave "Left atrial diameter": "4.4" and "Left ventricular end-diastolic diameter": "4.6" without units; set to "4.4 cm" and "4.6 cm".
  - The log says em dashes were removed from `metadata`, but `clinical_pearls[0]` still had two; reworded the clause without them ("each symptom of the classic triad (syncope, angina and heart failure) confers").
- perfect_agent -v and case_io check clean after the changes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_intervention_symptomatic_severe_aortic_stenosis` renamed to `search_aortic_stenosis_intervention_tavi`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.
- Drug follow-ups and the fallback medication review: removed, where present, wording that asserted results the agent has not obtained ("while AV conduction disease is unpaced", "meets the labelled dose", device-implantation warnings, the eGFR-specific metformin line, cefazolin "for device implantation"). Each is now a conditional rule (e.g. contraindicated in second- or third-degree AV block without a pacemaker; apixaban 5 mg unless two of age 80 or over, weight 60 kg or less, creatinine 1.5 mg/dL or more; anticoagulation advice if a device is implanted). Why: a drug check must not disclose the conduction diagnosis or the management decision.
- `initial_tool_outputs.drug_interactions` set to the medication-list review (copy of the fallback). Why: without it, tier 2 answered an unrelated drug (probe: ibuprofen) with the first per-drug follow-up.
- Added "not performed" follow-ups for `tilt_table` and `exercise_stress_test` (RM04/RP02 format, "Deferred by the clinical team"). Why: otherwise the library returned a normal tilt (HR 68) or a normal exercise test (10.4 METs) in a patient with high-grade AV block, contradicting the case; both orders stay penalised as in the plan.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.
