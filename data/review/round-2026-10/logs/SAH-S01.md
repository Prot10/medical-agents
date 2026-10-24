# SAH-S01
Reviewer status: R1 none, R2 approved | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| fddcb39d-16c7-4bdd-bdab-ba85e450e0f6 | FIXED | Securing (C1): the two "24-72 hours" musts in `ground_truth.assessment.required_recommendations` replaced by one MUST-SECURE (joint neurosurgical and neurointerventional review, coiling or clipping of the AComA aneurysm as early as feasible, preferably within 24 hours, [Hoh_2023]); securing pearl replaced in `key_clinical_evidence`. DSA (C3): new recommended criterion `dsa-aneurysm-anatomy` and diagnostic follow-up `request_digital_subtraction_angiography`, soft constraint CTA before DSA. Timeline (C2): the "day 6" TCD with moderate vasospasm re-dated to a day-0 admission baseline with normal velocities; the literature follow-up saying "Aneurysm treatment within 24-48 hours" deleted. No consult tool exists by design: the joint review is in the must. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `required_recommendations` | BP 182/106 with no lowering action; losartan held with nothing replacing it (C5). | FIXED: MUST-BP-A (nicardipine or clevidipine infusion, or labetalol boluses) and MUST-HOME "Withhold losartan during the acute phase and resume once stable." |
| C | major | `required_recommendations`, `prohibited_recommendations` | Nimodipine must without the hypotension adjustment; IV nimodipine prohibition wrong as written; ICU must with SBP target; daily TCD must (C4, C5). | FIXED: MUST-NIMO, MUST-ICU, MUST-DCI; canonical nimodipine and BP prohibitions. |
| D | major | `followup_outputs` literature `request_sah_guidelines` | Literature as a clinical step; "Triple-H therapy for symptomatic vasospasm" and "24-48 hours" (C7). | FIXED: deleted; canonical literature output last; criterion `optional`. |
| C | minor | `action-7-check-drug-interactions`, drug-check output | Template expected evidence about DOAC/warfarin reversal; terse output (C10). | FIXED: kept `recommended` (plan); case-specific rationale and evidence; output in report voice (losartan additive hypotension, BP check with the 30 mg every 2 hours adjustment, no parenteral injection, CYP3A4). |
| B | major | `followup_outputs` telemetry, `action-8` | Template text with management, 24 h (C12). | FIXED: 3 h since arrival, sinus rhythm/tachycardia 82 to 104 bpm, 9 atrial premature complexes, no sustained arrhythmia or pauses, QTc 484 ms (ECG 486), no torsades. |
| C | minor | `initial_tool_outputs.labs.panels.BMP` | Magnesium never measured (C9). | FIXED: magnesium 2.0 mg/dL (1.7-2.2). QTc 486: no MUST-QT. |
| D | minor | `initial_tool_outputs.ct.additional_observations` | "Classic SAH pattern" is commentary (C14); the differential needs the CT to state the sella and sinuses. | FIXED: removed; added "No intraventricular hemorrhage" and "Sella normal in size without mass; no hyperdense dural venous sinus". |
| B | minor | CTA follow-up | No neck measurement although the CTA criterion and the DSA need it; no statement on the neck vessels the differential cites. | FIXED: neck 2.7 mm added to observations, findings and impression; cervical carotid and vertebral arteries patent, no dissection. DSA matches (5.5 x 4.7 mm, neck 2.7 mm, dome-to-neck 2.0). |
| E | minor | labs `Baseline workup` type and screen | Engineering sentence (C14). | FIXED: `clinical_significance` null. |
| B | minor | `ground_truth.differential` | Generic key features (C11). | FIXED: canonical key features (exertional trigger, basal-cistern blood, AComA aneurysm). |
| C | minor | `key_clinical_evidence` | 24-72 h, TCD days 4-14, CT sensitivity and xanthochromia pearls (plan 1.3). | FIXED: the four canonical pearls. |
| A | minor | `action_criteria`, order, constraints, stop rule | Label-copied rationales, free-text citations, no constraints, allowance 0. | FIXED: canonical rationales, case-specific evidence, `[Hoh_2023]`; order NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD (optional), literature (optional); soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, allowance 1. Labels kept. |
| E | minor | `metadata.difficulty_rationale` | Listed "consult" and "nimodipine" as steps of a tool chain (no consult or treatment tool exists). | FIXED: describes the diagnostic chain NCCT, labs, ECG, CTA, catheter angiography. |

## Changes, in one paragraph a physician can read before re-reviewing

Approved case, changed only for the condition-wide errors and the note. Patient, exam (GCS 15, HH2), CT (Fisher 3, no IVH or hydrocephalus), ECG (QTc 486 ms), labs and echo (LVEF 50%) are unchanged in substance; magnesium 2.0 mg/dL is added, and the CT and CTA now state the sella, sinuses, neck vessels and a 2.7 mm aneurysm neck, which the updated differential and the new angiogram use. The pathway now runs NCCT, labs, ECG, CTA, a diagnostic catheter angiography (no second aneurysm, no vasospasm), the losartan-nimodipine check, echo, a 3-hour telemetry report, an optional day-0 TCD with normal velocities (replacing the day-6 vasospasm report), and an optional general literature search last. The musts now require enteral nimodipine with the 30 mg every 2 hours adjustment, securing the AComA aneurysm as early as feasible and preferably within 24 hours after joint review, neurocritical care, lowering BP now from 182/106 with a short-acting IV agent, withholding losartan, sodium monitoring and DCI surveillance with euvolemia.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` in the canonical literature output needs the SAH criteria-pack allow-list (plan 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: note fddcb39d (one MUST-SECURE, DSA criterion and diagnostic output, day-0 TCD, the 24-48 h literature deleted); patient block unchanged (approved case); criteria labels and alternatives unchanged; CTA vs DSA (5.4 x 4.8 vs 5.5 x 4.7 mm, neck 2.7 mm); telemetry vs ECG; labs summary vs panels; drug check (losartan) without leak; MUST-BP-A agents (no LVEF, bradycardia or asthma restriction); differential vs CT and CTA; stop rule, constraints, LP `harm`.
Found: (1) `ground_truth.red_herrings[0].correct_interpretation` says the "echocardiogram showing apical ballooning confirms etiology", but this echo shows only mild apical hypokinesis with LVEF 50% (the same cross-field error the worker fixed in S03, ruling 2). (2) The echo `findings` entry "Mild Takotsubo pattern EF 50%" overcalls a mild apical hypokinesis that the impression and wall-motion fields describe without the label (the worker removed the identical wording in S04).
- FLAGGED for the lead (condition-wide, not changed here): `fallback_tool_outputs.cardiac_monitoring` is a 24-hour Holter report, which cannot exist at assessment time (same reasoning as C12); it answers only a non-telemetry order, but the class spans all 30 cases.
Changed: red-herring interpretation now ends "the echocardiogram shows only mild apical hypokinesis with preserved ejection fraction and no primary cardiac lesion, and the focus remains on aneurysm securing."; echo `findings` now ["Mild apical hypokinesis, LVEF 50%"]. Both are corrections of real inconsistencies in an approved case. Checks re-run after verification: `perfect_agent.py -v` passes (NCCT and labs show the known `<- ?` display artefact; the initial CT and labs carry the expected evidence by content), `case_io.py check` clean for the case, `test_case_guards.py -k` passes (no leak in the literature or drug-check outputs).


## Condition audit (auditor, 24 Oct 2026)

- `initial_tool_outputs.labs.abnormal_values_summary` rewritten to values and flags only. It named interpretations ("leukocytosis", "stress hyperglycemia", "neurogenic" troponin); "neurogenic" gives away the troponin red herring's answer, and the labs report carries no cross-modality interpretation. Same class as the fix already made in S05 to S10. Values, flags and the labs criterion unchanged.
- `initial_tool_outputs.ecg.rhythm` "Sinus tachycardia" at a rate of 98 changed to "Sinus rhythm"; the interpretation now reads "Sinus rhythm, rate 98." and the `action-5-analyze-ecg` expected evidence "Sinus rhythm 98 ...". Tachycardia starts at 100 bpm; same template error the verifiers fixed in M01, M04 and S10.
- Checks after the audit: `perfect_agent.py` 30/30 pass; `case_io.py check` schema and synonym guard OK, no test failure names an SAH case; `test_case_guards -k SAH` 60 passed.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- fallback_tool_outputs.mri: SAH-consistent brain MRI instead of the library normal report: an off-pathway brain MRI was answered by the library normal report (no blood on SWI), contradicting the CT; the case fallback now reports the CT's blood on FLAIR and SWI (CENTRAL 10).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
- followup_outputs: MR angiography report added before the literature output (aneurysm site and size from the DSA, 0.2 mm smaller as TOF reads it; P02 negative): an MRA order was answered by a fallback reporting no abnormality, contradicting the CTA and DSA (CENTRAL 10). MRA stays a waste action after the CTA.
- `ground_truth.diagnosis` (synonyms re-expanded with `--prune`): diagnosis_synonyms.yaml: the I60 category no longer grants I60.8 (non-aneurysmal SAH), so the code was pruned from this aneurysmal case.
- Checks after the close-out: `perfect_agent.py` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k SAH-` pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- follow-up `request_echocardiogram`: `echo_type` set to `TTE` (was missing); the bedside study is transthoracic, and untyped it also answered a TEE or bubble-study order.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'No diagnostic abnormality identified on this study.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-3-interpret-labs]`.alternatives: was [CBC, BMP, coagulation]; now [CBC, BMP, coagulation, troponin, BNP] | [CBC, BMP, coagulation].
- Decision: serve: new first alternative (old order kept as an alternative). Neurogenic troponin elevation is the case's cardiac red herring (prohibition, key evidence, red herring); baseline troponin belongs with the admission bloods in aSAH (AHA/ASA 2023), and the cardiac panel holds the BNP the evidence reads. CBC + BMP + coagulation did not return it.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.
- Approved case: changed for a real inconsistency (the policy's own order did not return what its evidence cites), so it goes back to re-review for this criterion only.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.
