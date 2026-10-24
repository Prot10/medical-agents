# GBS-RP16
Reviewer status: R2 approved (change only real errors, log why) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b902ee1c-59e1-43f5-9e02-dd2f3600727e | FIXED | The lumbar puncture is now gated on platelets and coagulation: hard sequence constraint a1 -> a3 (platelets 98 x10^9/L on induction, L-asparaginase hypofibrinogenaemia). a1 now requires `{'panels':['CBC','CMP','CK','coagulation']}` and the labs output has a Coagulation panel (INR 1.1, aPTT 31 s, fibrinogen 1.7 g/L L). The "transfuse after the LP" statement in the DDI output was deleted. a3 label and rationale name the platelet and coagulation check. |
| 693830c4-671d-4855-99ba-1d17edef7a68 | FIXED | Respiratory follow-up in the canonical format: FVC 2.6 L (62% predicted; 33 mL/kg at 78 kg) L, MIP -30 cmH2O L, MEP 44 cmH2O L, with the arrival-to-6 h trend (2.8 to 2.6 L, MIP -34 to -30) moved there from `patient.neurological_exam.additional`; nothing is called "normal". Weight and height added (`patient.physical_exam.general` "Weight 78 kg, height 178 cm", BMI 24.6). Must 1 is ICU-level monitoring now (EGRIS 6, MIP at threshold, falling FVC, orthopnoea) with the elective intubation criteria spelled out. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `ground_truth.diagnosis.accepted[0]`, `followup_outputs` | Label carried "anti-GM1 / GD1a positive", a result only the ganglioside follow-up (C2) could supply. | FIXED: suffix removed from accepted[0] (CENTRAL); ganglioside follow-up deleted; KCE 1 now "The pure motor axonal NCS pattern with normal sensory studies defines AMAN". |
| C | major | `ground_truth.assessment` | Musts lacked ICU and intubation criteria, IVIg dose, vincristine plan and thrombosis caveat; no succinylcholine prohibition; template steroid prohibition clashed with induction prednisone. | FIXED: ICU + intubation triggers; IVIg 0.4 g/kg/day x5 (about 31 g/day at 78 kg) with the reason PE is less practical (fibrinogen depletion, central access); hold vincristine with haematology and review fluconazole; telemetry; platelets/fibrinogen monitoring and thromboprophylaxis. Prohibitions: no further vincristine, no corticosteroids for GBS (induction prednisone is chemotherapy), no succinylcholine, renal function before IVIg. |
| C | major | `ground_truth.differential` | Vincristine neuropathy high and leptomeningeal leukaemia moderate after a work-up that addresses both (C5); CIP low without an ICU course. | FIXED: vincristine low (pure motor, normal SNAPs, protein 128), leptomeningeal leukaemia low (cytology no blasts), acute-onset CIDP low with the 8-week reassessment, CIP very_low, cord compression very_low. |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | Editorial reasoning about vincristine and "expected findings from his ALL"; respiratory numbers in the exam (C7). | FIXED: HPI is history only; `additional` holds bladder function and breathing pattern. |
| C | major | `initial_tool_outputs.labs` | HIV, Campylobacter, EBV/CMV PCR, a CSF blast row in the blood labs; no CMP, liver tests, albumin, CK or coagulation. | FIXED: CBC, CMP with liver tests and albumin, CK, Coagulation; ANA/dsDNA kept as negative; interpretation recites values only. |
| A | major | `followup_outputs`, `initial_tool_outputs.literature_search`, `drug_interactions` | Empty literature follow-up (C9), DDI as a follow-up with management advice ("hold vincristine", transfusion). | FIXED: canonical literature output, a5 optional and last; DDI category-level in `initial_tool_outputs.drug_interactions` (fluconazole-vincristine CYP3A4, asparaginase coagulopathy with IVIg and PE, daunorubicin, succinylcholine warning). a6 required (ROUND_POLICY ruling 6). |
| C | minor | `initial_tool_outputs.ecg` | QTc 448 ms in a man called borderline; "daunorubicin/vincristine can prolong QT" (cross-modality). | FIXED: normal intervals, no drug comment. |
| C | minor | `followup_outputs` telemetry | Longer report with "daunorubicin cardiotoxicity monitoring" (C12). | FIXED: 24 h, sinus 76-108 bpm, BP 108/64 to 148/88; a8 canonical. |
| B | minor | `followup_outputs` CSF | "N/A PMN" placeholder, em dashes. | FIXED: 5 lymphocytes, blasts 0, cytology negative, glucose 53 (ratio 0.70 against serum 76). |
| B | minor | `initial_tool_outputs.specialized_test` | `test_type` with "(Day 5)". | FIXED: `emg_ncs`; needle EMG row added. |
| B | minor | `followup_outputs` spine MRI | "Brain" findings inside a spine study and an interpretive "consistent with inflammatory polyradiculopathy". | FIXED: cord, roots and column only, descriptive impression; a9 stays optional. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | Template constraints; stop rule not equal to the required set. | FIXED: hard a1 -> a3, soft a1 -> a6; stop rule = six required criteria, `max_additional_actions` 3. |
| E | minor | `patient.chief_complaint` | Em dashes. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 38-year-old man (78 kg) in week 4 of ALL induction (vincristine, daunorubicin, prednisone, L-asparaginase, with fluconazole) has 48 hours of ascending quadriparesis (legs 0/5, arms 3/5), areflexia, intact sensation and orthopnoea. The work-up now asks for blood tests with coagulation before the lumbar puncture (platelets 98, fibrinogen 1.7 g/L, INR normal), then CSF (protein 128 mg/dL, 5 cells, no blasts), a pure motor axonal NCS with normal sensory potentials, serial respiratory function (FVC 2.6 L, 62%, 33 mL/kg, falling; MIP -30; MEP 44), telemetry, ECG and a required check of the induction regimen. The assessment moves him to ICU-level monitoring with explicit intubation triggers, gives IVIg 2 g/kg over 5 days as the practical choice on L-asparaginase, holds vincristine with haematology, monitors platelets and fibrinogen with thromboprophylaxis, and forbids succinylcholine and corticosteroids for GBS. The label no longer states the anti-ganglioside result, which no order could return.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `ground_truth.diagnosis.accepted[0]` changed from "...during ALL induction; anti-GM1 / GD1a positive" to "Guillain-Barre syndrome, AMAN variant (acute motor axonal neuropathy) during ALL induction" (plan decision; the serology was a leak). accepted[1:] untouched; please check the synonym expansion still matches.
- Plan CENTRAL 5 (weight field) and 10 (respiratory-report guard) apply.
- Citation key [Walgaard_2010] (EGRIS, Ann Neurol 2010) is new in this condition; add it to the citation registry if one is kept.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

Approved case: checked that the changes are real-error fixes. Both note ids present: hard a1 -> a3 with `coagulation` in a1 and the coagulation panel served (platelets 98, fibrinogen 1.7 L), no transfusion step; respiratory canonical (2.6 L / 78 kg = 33 mL/kg, 2.8 to 2.6 L = 7% fall, BMI 78 / 1.78^2 = 24.6), ICU-level and intubation must. EGRIS 6 verified (onset to admission 2 days = 2, no facial or bulbar weakness = 0, MRC sum 3 x 3 x 2 + 0 = 18/60 = 4). AMAN label met by the NCS (unexcitable leg motor nerves, normal sensory potentials, no demyelinating-range slowing). Prose changes in the patient block remove timeline leaks and editorial text (C7); the added orthopnoea supports the ICU must and is consistent with the respiratory values.

Found and fixed (real errors):
- C, major: must 1 listed "FVC below 20 mL/kg ... or 60% predicted" as an elective-intubation trigger; 60% predicted is the ICU-level trigger (plan C1), and at 62% the must would have intubated him almost at once. Removed "or 60% predicted" from the intubation list.
- B, minor (pre-existing, kept by the worker): ECG at rate 98 reported as "Sinus tachycardia", and telemetry 76-108 bpm as "Sinus tachycardia throughout". Changed to sinus rhythm at 98 (ECG rhythm, findings, interpretation) and "sinus rhythm 76-108 bpm with intermittent sinus tachycardia" (telemetry findings, impression, rhythm summary, a8 expected_evidence).
- B, minor: a7 expected_evidence and rationale were the template; rewritten to what the ECG shows.

Checks run after the edits: `perfect_agent.py -v` passes (every required and recommended criterion served by its own report), `case_io.py check` clean for the case (schema, synonym guard, no test failure naming it), `test_case_guards.py` leak, follow-up and banned-string guards pass.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels plus "acute motor axonal neuropathy" and "AMAN"; AIDP and Miller Fisher labels removed.
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
