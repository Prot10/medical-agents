# SAH-S03
Reviewer status: R1 none, R2 none (no notes and no status in the notes file; the plan treats it as one of R2's 21 approvals) | Approved before this round: probably yes (unconfirmed, plan section 6 question 6)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No note for SAH-S03. The condition-wide classes (C1 to C5, C7, C9 to C12, C14) were applied as real errors, and the OCP must of plan section 4 (as M06). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `required_recommendations` | Duplicate "24-72 hours" securing musts (C1). | FIXED: one MUST-SECURE (left MCA bifurcation). Securing pearl replaced. |
| C | major | criteria, follow-ups | No catheter angiography (C3). | FIXED: recommended `dsa-aneurysm-anatomy`; DSA follow-up 5.1 x 4.3 mm (CTA 5.0 x 4.4), irregular dome with a bleb, neck 3.0 mm, dome-to-neck 1.7, inferior M2 trunk from the base of the neck, no second aneurysm, no vasospasm. Soft CTA before DSA. |
| B | major | TCD follow-up | Day 6 with moderate left MCA vasospasm and CT perfusion advice in a patient seen within hours (C2). | FIXED: day-0 baseline, normal velocities (MCA 57 to 64 cm/s, Lindegaard 1.5 to 1.7). |
| C | major | `required_recommendations` | BP 174/98 with no lowering action; amlodipine held with nothing replacing it (C5). | FIXED: MUST-BP-A (default agents) and MUST-HOME "Withhold amlodipine while on nimodipine (additive dihydropyridine effect)". |
| C | major | `required_recommendations` | Combined oral contraceptive not addressed once the OCP literature step is removed (plan section 4). | FIXED: must "Stop the combined oral contraceptive and arrange non-estrogen contraception." |
| C | major | `action-7`, drug-check output | Tier recommended with template DOAC/warfarin evidence; output claimed "negative inotropy" from dihydropyridines (minimal) and put a resume instruction under alternatives (C10). | FIXED: `required` (dihydropyridine with nimodipine), in the stop rule; output in report voice (amlodipine additive vasodilation and persistence, OCP no interaction but VTE risk with immobilization, BP check with 30 mg every 2 hours adjustment, no parenteral injection, CYP3A4); alternatives empty. |
| C | major | `required_recommendations`, `prohibited_recommendations` | Nimodipine must, IV prohibition, ICU SBP target, daily TCD must (C4, C5). | FIXED: MUST-NIMO, MUST-ICU, MUST-DCI, canonical prohibitions. |
| D | major | literature follow-up `request_ocp_management` | Literature used as a clinical step (C7). | FIXED: deleted; canonical literature output last; criterion `optional`. |
| E | minor | `initial_tool_outputs.labs.panels["Exclusion studies"]` | BNP "Within reference range" with an engineering sentence (C14). | FIXED: panel deleted; numeric BNP 62 pg/mL (<100) in the Cardiac panel. |
| C | minor | labs BMP | Magnesium never measured (C9). | FIXED: 2.2 mg/dL (1.7-2.2). QTc 468: no MUST-QT. |
| B | minor | `ground_truth.red_herrings[0]` | Interpretation says the echocardiogram shows apical ballooning, but this echo is normal (LVEF 60%, normal wall motion); data point named QTc prolongation generically. | FIXED: data point "Troponin I 0.09 ng/mL with T-wave inversions in V2 to V4"; interpretation cites the normal echo. |
| D | minor | `patient.history_present_illness` | "classic thunderclap pattern" is teaching language naming the pattern for the agent; "recently started amlodipine one year ago" contradicts itself. | FIXED: "The headache reached maximum intensity instantaneously."; "She started amlodipine one year ago ...". |
| B | major | telemetry follow-up, `action-8` | Template text, 24 h (C12). | FIXED: 3 h, sinus rhythm 76 to 98 bpm, 3 PVCs, no sustained arrhythmia or pauses (QTc below 480, no QTc line). |
| B | minor | CTA, CT | No neck measurement; neck vessels, sella and sinuses not stated though the differential relies on them. | FIXED: neck 3.0 mm; cervical vessels patent; CT "Sella normal in size without mass; no hyperdense dural venous sinus". |
| E | minor | type and screen; `metadata.difficulty_rationale` | Engineering sentence; "consult" and "nimodipine" listed as tool steps. | FIXED: null; rationale rewritten. |
| B | minor | differential | Generic key features (C11). | FIXED: canonical (exertional trigger, basal-cistern blood, left MCA bifurcation aneurysm). |
| C | minor | `key_clinical_evidence` | Template pearls. | FIXED: four canonical pearls. |
| A | minor | criteria, order, constraints, stop rule | Label-copied rationales, free-text citations, no constraints, allowance 0. | FIXED: canonical; order NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, drug check, allowance 1. Labels kept. |

## Changes, in one paragraph a physician can read before re-reviewing

Patient, exam (GCS 15, HH2), CT (Fisher 3, left Sylvian predominance, no IVH or hydrocephalus), CTA (5.0 x 4.4 mm left MCA bifurcation aneurysm, now with a 3.0 mm neck), ECG (QTc 468 ms), labs and the normal echo are unchanged in substance; two HPI phrases were tidied, magnesium 2.2 mg/dL and a numeric BNP replace the "Exclusion studies" panel, and the red herring now matches the normal echo. The pathway is NCCT, labs, ECG, CTA, a new diagnostic catheter angiography (inferior M2 trunk at the neck, no second aneurysm, no vasospasm), the required amlodipine-nimodipine check, echo, a 3-hour telemetry report, an optional day-0 TCD with normal velocities (replacing the day-6 vasospasm report) and an optional literature search last. Musts: enteral nimodipine with the 30 mg every 2 hours adjustment; securing the left MCA bifurcation aneurysm as early as feasible, preferably within 24 hours; neurocritical care; BP lowering now from 174/98; withholding amlodipine; stopping the combined oral contraceptive; sodium monitoring; DCI surveillance.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` in the canonical literature output needs the SAH allow-list (plan 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: the two HPI edits (the "classic thunderclap pattern" phrase is answer-pointing teaching text and "recently started ... one year ago" contradicted itself; both changes are corrections, not churn); BNP 62 pg/mL numeric in the Cardiac panel and the Exclusion panel gone; magnesium 2.2 within 1.7-2.2; drug check required (dihydropyridine with nimodipine) and in the stop rule; OCP must; red herring now cites the normal echo (LVEF 60%); telemetry has no QTc line (QTc 468, below 480, per C12); CTA vs DSA (5.0 x 4.4 vs 5.1 x 4.3 mm, neck 3.0 mm); differential vs reports; LP `harm`.
Found: nothing that needed a change.
- FLAGGED for the lead (condition-wide, not changed here): `fallback_tool_outputs.cardiac_monitoring` is a 24-hour Holter report, which cannot exist at assessment time (same reasoning as C12); it answers only a non-telemetry order, but the class spans all 30 cases.
Changed: nothing. Checks re-run after verification: `perfect_agent.py -v` passes (NCCT and labs show the known `<- ?` display artefact; the initial CT and labs carry the expected evidence by content), `case_io.py check` clean for the case, `test_case_guards.py -k` passes (no leak in the literature or drug-check outputs).


## Condition audit (auditor, 24 Oct 2026)

- `initial_tool_outputs.labs.abnormal_values_summary` rewritten to values and flags only. It named interpretations ("leukocytosis", "stress hyperglycemia", "neurogenic" troponin); "neurogenic" gives away the troponin red herring's answer, and the labs report carries no cross-modality interpretation. Same class as the fix already made in S05 to S10. Values, flags and the labs criterion unchanged.
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
