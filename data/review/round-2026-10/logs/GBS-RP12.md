# GBS-RP12
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 8e2833d3-10bd-48c5-8534-cab79697b031 | FIXED | Label changed to the examination (the reviewer ruled the label wrong): `ground_truth.diagnosis.accepted[0]` "Guillain-Barré syndrome, severe acute inflammatory demyelinating polyradiculoneuropathy with left ptosis" (was "... cranial-nerve variant (unilateral facial involvement)"). The facial-palsy-derived differential entries (Lyme polyradiculitis with facial palsy, sarcoid cranial neuropathy) and pearl 1 were removed or rewritten; `metadata.difficulty_description` without em dash. |
| d4baaeb9-ead9-4dae-b089-ab2fcfe8fb3c | FIXED | `followup_outputs[3]` (respiratory) rewritten in the canonical format: FVC 2.2 L (58% predicted; 30 mL/kg at 74 kg) L, MIP -28 cmH2O L, MEP 52 cmH2O L, change from 2.4 L / -32 cmH2O on arrival over 4 h (8% fall), cough effective. The arrival values sat in `neurological_exam.additional` and now appear only in the report. Weight and height added (`patient.physical_exam.general` "Weight 74 kg, height 170 cm", BMI 25.6 agrees). Must 1 is ICU-level monitoring now (FVC <60% predicted, MIP weaker than -30, falling trend) with the intubation criteria (FVC <20 mL/kg, about 1.5 L; worsening MIP/MEP; bulbar weakness with weak cough or secretions; distress, hypoxaemia, hypercapnia). a4 canonical. |
| e5ca0f0c-2750-4743-9e2b-8ebb8de3ab25 | FIXED | Edrophonium follow-up (`request_tensilon_test`, which also repeated the ice pack test) deleted; a prohibition explains why no edrophonium test. Single-fibre EMG and the ice pack test removed from the NCS report (not part of an NCS order); RNS stays in the NCS report (median-APB and facial-nasalis). AChR/MuSK moved from the initial labs to their own follow-up with a recommended criterion `action-10-interpret-labs-anti-achr`; the ice pack test became its own follow-up (`request_ice_pack_test`, `test_type: ice_pack_test`) with an optional criterion `action-11-order-specialized-test-ice-pack`. Ptosis resolved: red herring "New unilateral left ptosis" plus differential entries myasthenia gravis (low), Horner syndrome (very_low, pupils equal, no anisocoria in dim light) and partial oculomotor palsy (very_low, full eye movements, pupils spared). The HPI sentence naming the MG/Horner/oculomotor work-up was removed (C7). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.labs` | HIV with the leaky clinical_significance (C10); Campylobacter and EBV IgM (C3); no platelets, glucose, liver tests, albumin or CK although a1 expects them. | FIXED: HIV and infection serology removed; CBC platelets, CMP with glucose, BUN, ALT, AST, ALP, bilirubin and albumin, CK 142 added (all normal); CRP and ESR kept; `clinical_significance: null`. |
| A | major | `followup_outputs` | Ganglioside follow-up (anti-GM1 IgG 1:80) in typical sensorimotor GBS (C2); empty literature and DDI placeholder follow-ups (C9). | FIXED: all three deleted; `anti-GM1 IgM` removed from a1. |
| D | major | `initial_tool_outputs.literature_search` | Literature output echoed a5's expected_evidence (C11). | FIXED: canonical general output [EAN_PNS_2023, Walgaard_2021]; a5 optional and last. |
| C | minor | `initial_tool_outputs.specialized_test` | "with conduction block" without conduction-block data; no needle EMG; `test_type` in prose. | FIXED: pattern "Demyelinating polyradiculoneuropathy", severity Severe, CMAPs labelled reduced, needle EMG line added, `test_type` "emg_ncs". |
| C | minor | `followup_outputs` telemetry | 72-hour report; "Mild autonomic dysfunction" is an interpretation (C12). | FIXED: first 24 h, sinus 64-88 bpm, BP 132/80 to 184/106 mmHg with hourly swings (admission BP 162/102 with well-controlled hypertension before); a8 expected_evidence canonical with these values. |
| C | major | `ground_truth.assessment` | Musts generic ("Initiate IVIG / plasma exchange", ICU without criteria); "Brainstem MRI given asymmetric cranial findings" with no criterion and no indication once the ptosis is pupil-sparing with full eye movements; "corticosteroids as monotherapy" prohibition (C8). | FIXED: ICU-level and intubation must; IVIg 2 g/kg (about 30 g/day at 74 kg) with the indication (GBS disability 4, day 5) and PE alternative; telemetry with cautious treatment of autonomic BP surges [Leonhard_2019]; LMWH prophylaxis. Brain MRI must and pearl 2 deleted (plan option; brain MRI stays waste with a case-specific rationale). Prohibitions: canonical steroid text, no edrophonium test, renal function before IVIg, no succinylcholine. |
| C | major | `ground_truth.differential` | Brainstem stroke and acute-onset CIDP moderate after the work-up (C5); Lyme and sarcoid entries built on a facial palsy the patient does not have. | FIXED: brainstem stroke very_low, CIDP low, vasculitic very_low with reasons; Lyme and sarcoid removed; MG, Horner, oculomotor added. |
| B | minor | `patient.neurological_exam` | `additional` repeated vitals, spirometry and history; motor exam gave no distal arm strength; no plantar responses or pupil detail for the ptosis. | FIXED: `additional` keeps the upgaze fatigability test; finger abduction 4/5, flexor plantars, "no anisocoria in dim light", palate and cough normal added; em dashes removed. |
| B | minor | `followup_outputs[0]` CSF | "N/A PMN/N/A lymph" placeholder; em dash; ratio 0.71 vs serum glucose. | FIXED: interpretation rewritten; ratio 0.68 with serum glucose 94. |
| C | minor | `ground_truth.action_criteria` a6 | DDI required with amlodipine only. | FIXED: optional (amlodipine changes neither the choice nor the dose of IVIg or PE; ruling 6); DDI output category-level (no interaction with IVIg, hypotension with PE as relative caution) without the templated "which agents to taper" warning. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | Template constraints (EMG named for a respiratory reason; labs before an optional DDI); stop rule with literature and 0 extra actions. | FIXED: constraints deleted; stop rule = five required criteria, `max_additional_actions` 3. |
| E | minor | `patient.chief_complaint`, `patient.history_present_illness` | Exam findings and em dashes in the chief complaint; editorial "this is an isolated unilateral ptosis". | FIXED: rewritten in the patient's terms. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is now labelled as what it shows: severe AIDP in a 57-year-old man (74 kg) with a pupil-sparing, non-fatigable left ptosis and no facial weakness. The patient block no longer carries spirometry or the list of tests the ptosis prompted. The edrophonium challenge is gone; myasthenia is addressed by RNS in the NCS report (no decrement), AChR/MuSK antibodies as a recommended order and an optional ice pack test, all negative. The ptosis is a red herring resolved by equal pupils, full eye movements and no fatigability, with Horner syndrome and oculomotor palsy in the differential at very low. Respiratory function reads FVC 2.2 L (58%, 30 mL/kg), MIP -28, MEP 52 cmH2O, falling over 4 h, so must 1 admits him to ICU-level monitoring with explicit intubation criteria; IVIg 2 g/kg is given because he cannot walk at day 5. Baseline labs are complete and normal; the ganglioside panel and infection serology are gone; telemetry reports 24 hours with blood pressure lability. The brain MRI must is gone because nothing in the findings calls for it.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `ground_truth.diagnosis.accepted[0]` changed (note 8e2833d3: label did not match the exam); synonyms untouched.
- Plan CENTRAL 5 (weight field) and 10 (respiratory-report guard) apply.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: all three note ids present; label now matches the exam (left ptosis, no facial weakness); edrophonium follow-up gone and the ice pack test is its own optional follow-up; RNS in the NCS report; AChR/MuSK follow-up with a recommended criterion; Horner and oculomotor entries and the ptosis red herring present. Respiratory arithmetic (2.2 L / 74 kg = 30 mL/kg; 2.4 to 2.2 L = 8% fall; BMI 74 / 1.70^2 = 25.6), ICU and intubation must, CSF ratio 64/94 = 0.68, complete normal labs, telemetry 24 h, no residual serology, HIV or ganglioside text, stop rule = the five required criteria.

Found and fixed:
- C, minor: must 2 gave "GBS disability score 4" while the exam and HPI say he walks only with bilateral support (score 3). Changed to 3 (indication unchanged).
- B, minor: a7 expected_evidence was the template "Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities" while the ECG is normal sinus rhythm 76 with QTc 422 ms, and the rationale repeated the label. Both rewritten to what the ECG shows. Same template remains in M01, M02, M03, P02, RM11-RM16 (outside this batch): tell the lead.
- C, minor: differential "Partial oculomotor nerve palsy" very_low with "isolated levator weakness is part of the cranial involvement" was self-contradictory (levator ptosis in GBS is partial oculomotor involvement). Renamed "Compressive or microvascular oculomotor nerve palsy" with the pupil and eye-movement reasons.

Checks run after the edits: `perfect_agent.py -v` passes (every required and recommended criterion served by its own report), `case_io.py check` clean for the case (schema, synonym guard, no test failure naming it), `test_case_guards.py` leak, follow-up and banned-string guards pass.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.
