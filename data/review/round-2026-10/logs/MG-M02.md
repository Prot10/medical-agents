# MG-M02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for myasthenia_gravis, applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.labs`, `ground_truth.red_herrings[1]`, `assessment.required_recommendations[0]` | Plan L: AChR binding 0.6 nmol/L with reference <0.5 called "borderline"; it is positive (fact 2). | FIXED: summary lists the value as (H); interpretation "positive at low titre"; red herring and key evidence say positive. |
| B | major | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Class G stub: TSH "Within reference range", no unit, engineering sentence as clinical significance. | FIXED: replaced by a Thyroid Panel (TSH 1.9 mIU/L, free T4 1.2 ng/dL with ranges, significance null). |
| C | minor | `initial_tool_outputs.labs` | Anti-striated muscle (titin) row and "thymoma less likely" (titin not orderable, fact 4, CENTRAL 7). | FIXED: row and summary line removed. |
| A | major | `followup_outputs` (`request_ivig_plasmapheresis`) | Plan J: post-IVIG day 5 NIF/FVC panel filed as labs: a treatment-response output. | FIXED: deleted; IVIG is not indicated as a must here (no crisis), respiratory monitoring is a must. |
| A | major | `followup_outputs` (`request_musk_antibodies`) | Plan H9: MuSK/LRP4/VGCC follow-up in an AChR-positive case. | FIXED: deleted (MuSK negative remains in the initial panel). |
| D | major | `followup_outputs` (`request_literature_review_mg_sle`) | Empty summary, invented source ("Overlap syndromes ... Muscle & Nerve 2023"), "MMF NEJM 2008" (fact 23), patient-directed management. | FIXED: deleted; one canonical literature output added at `initial_tool_outputs.literature_search` (optional criterion). |
| D | major | `patient.neurological_exam.additional` | NIF -38 cmH2O and FVC 78% in the exam while respiratory function is a criterion (class K). | FIXED: numbers removed; neck weakness kept. |
| B | major | `patient.physical_exam`, `followup_outputs` (`request_respiratory_function`) | No weight or height; FVC without % or mL/kg; no MEP (fact 14). | FIXED: "Weight 58.5 kg, height 162 cm" (BMI 22.3); FVC 2.60 L (76% predicted, 44 mL/kg), MIP -38, MEP 58 cmH2O (reduced), ABG. |
| B | minor | `initial_tool_outputs.specialized_test` | Impression said nasalis 10% "meets the threshold" (the criterion is above 10%); recommended actions named antibodies and CT chest. | FIXED: borderline 8-10% decrement, post-exercise exhaustion to 13%, no facilitation, technique line; SFEMG as the only further step. |
| B | minor | `followup_outputs` (`request_emg_single_fiber`) | "All pairs markedly above normal" with a range starting at 40; 40% blocking at a mean MCD of 58 implausible. | FIXED: muscle named, 12 of 20 pairs above the individual limit, blocking 4 of 20. |
| A | minor | `metadata.actions_withdrawn` | Ice-pack test withdrawn for lack of a result while she has fatigable right ptosis. | FIXED: `request_ice_pack_test` (right MRD1 0.5 to 3.0 mm) and `action-ice-pack-test` recommended; withdrawal entry removed. |
| B | major | `followup_outputs` (`request_hydroxychloroquine_interaction`) | Plan C: `proposed` was a dosing plan; content was treatment advice (MMF preferred, TPMT) rather than interactions; sulfa allergy with celecoxib unaddressed. | FIXED: one stored output moved to `initial_tool_outputs.drug_interactions["pyridostigmine"]`: pilocarpine additive muscarinic effects, hydroxychloroquine MG aggravation, prednisone with celecoxib GI risk, celecoxib labelling contraindication with a recorded sulfa allergy (low cross-reactivity, tolerated; review), HCQ retinal dose. Allergy kept. |
| A | major | `ground_truth.action_criteria` | Class A template; drug check generic with telithromycin; literature required. | FIXED: labs `["anti_AChR","TSH"]`; RNS required; SFEMG recommended (RNS equivocal, plan 3.5); ice pack recommended; mediastinal imaging required (CT, chest CT, mediastinal MRI); respiratory recommended; drug check required with pyridostigmine, hydroxychloroquine, pilocarpine or prednisone as the drug (plan 3.2); literature optional last. One citation per source. |
| C | major | `ground_truth.sequence_constraints`, `stop_rule` | Shared `labs -> RNS` constraint; literature in the stop rule; max 0. | FIXED: `labs -> SFEMG`, `RNS -> SFEMG` soft; stop rule labs, RNS, imaging, drug check; max 2. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts that were tests (confirm AChR, CT, SFEMG); no steroid plan; no thymectomy (MGTX) must; no HCQ or pilocarpine management. | FIXED: six musts: pyridostigmine with muscarinic monitoring; prednisone per fact 18 with PPI (celecoxib); steroid-sparing agent chosen with rheumatology; elective thymectomy per MGTX; HCQ back to at most 5 mg/kg/day (400 mg is 6.8 mg/kg at 58.5 kg) with no further increase; respiratory monitoring with fact 15 thresholds and swallow assessment. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Shared set with telithromycin and the SFEMG-dependent functional line. | FIXED: canonical drug and steroid prohibitions; canonical attribution line with "lupus-related"; HCQ escalation line kept, reworded. |
| C | minor | `ground_truth.differential` | Lupus myositis moderate after normal CK; LEMS "anti-VGCC negative expected" (not tested); drug-induced MG entry ignored her hydroxychloroquine. | FIXED: lupus myositis low, Sjogren neuropathy very_low (normal NCS), LEMS very_low with the RNS facts, drug-aggravated MG (hydroxychloroquine) low with reasons; brainstem key features reworded. |
| C | minor | `ground_truth.key_clinical_evidence` | Shared template lines (telithromycin, "All confirmed MG require CT chest", "paradigmatic indication for SFEMG"). | FIXED: seven case-specific lines. |
| D | minor | `fallback_tool_outputs.ct` | Class F wording "does not address the question this patient's workup turns on". | FIXED: plain normal head CT. |
| C | minor | `initial_tool_outputs.body_imaging` | Region "mediastinum" only, so a chest CT order fell to the library. | FIXED: region "mediastinum chest"; findings compacted, impression unchanged in substance. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` cited for waste rationales. | FIXED: case rationales, Jacob 2025 in text, citations empty. |

## Changes, in one paragraph a physician can read before re-reviewing

A 48-year-old woman with SLE and Sjogren syndrome on hydroxychloroquine 400 mg, celecoxib and pilocarpine, with fatigable ptosis, diplopia, dysphagia for liquids and neck flexor weakness. The work-up: AChR binding 0.6 nmol/L (positive against <0.5) with raised blocking and modulating antibodies, normal thyroid function, mild serological lupus activity; RNS equivocal (8-10%, no facilitation) so SFEMG is recommended and abnormal; a positive ice-pack test; mediastinal CT without thymoma; FVC 76% predicted with MIP -38 and MEP 58 cmH2O. The drug check is required and now holds real content: pilocarpine adds muscarinic effects to pyridostigmine, hydroxychloroquine can worsen MG, celecoxib with prednisone needs gastroprotection, and the celecoxib label lists her sulfa allergy (low cross-reactivity, tolerated). Musts: pyridostigmine, prednisone per the start-low rule with a PPI, a steroid-sparing agent chosen with rheumatology, elective thymectomy per MGTX, hydroxychloroquine back to at most 5 mg/kg/day, and respiratory and swallow monitoring. The post-IVIG panel, the extra antibody and literature follow-ups and the titin row are gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria pack keys `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]` (named in rationale text only) (plan CENTRAL 1).
- `icd_codes[0]` G70.01 for a stable new diagnosis (plan CENTRAL 2; unchanged).
- Perfect-agent warning: the `mediastinum_MRI` alternative of `action-4-order-body-imaging` is answered by the library's normal mediastinal MRI, which is consistent with this case (no thymoma). No change needed unless the warning is to be silenced centrally.

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (M02 entry, 3.2 drug-check table), the diff and the whole final case. No notes file exists for MG. Every FIXED finding is in the file: AChR 0.6 nmol/L against <0.5 called positive in labs, key evidence and red herring; thyroid stub replaced; titin row, post-IVIG panel, MuSK follow-up and literature follow-up deleted; NIF/FVC out of the exam; respiratory report per fact 14 (2.60 L / 58.5 kg = 44 mL/kg, BMI 58.5/1.62^2 = 22.3); RNS equivocal (maximum 10%, which is not above 10%) so SFEMG recommended; ice pack consistent with right-predominant ptosis; drug check required with real content (pilocarpine muscarinic load, hydroxychloroquine aggravation, celecoxib with prednisone, celecoxib label sulfonamide contraindication with the recorded sulfa allergy kept); stop rule includes the required drug check. The hydroxychloroquine must (no more than 5 mg/kg/day; 400 mg is 6.8 mg/kg) is correct and agrees with the HPI dose increase and the differential ("symptoms began before the dose increase"). The thymectomy must fits MGTX (48, AChR+, no thymoma on the stored CT). Discriminator and leak checks pass.

Found: nothing requiring a change. Noted: AChR reference <0.5 nmol/L sits beside MuSK <0.02 nmol/L, two laboratory conventions; the plan explicitly keeps the 0.6/<0.5 pair and MuSK is negative either way, so no clinical consequence; left as is.

Checks: `perfect_agent.py MG-M02 -v` passes (the mediastinum_MRI alternative is answered by the library normal, consistent with no thymoma), `case_io.py check` clean for the case, case guards pass.

## Condition audit (MG auditor, 24 Oct 2026)

- patient.neurological_exam.cranial_nerves: 'right eye adduction weakness' with diplopia on rightward gaze is impossible (the right eye adducts on leftward gaze); now left eye adduction weakness. FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
