# SAH-S02
Reviewer status: R1 none, R2 none (no notes and no status in the notes file; the plan treats it as one of R2's 21 approvals) | Approved before this round: probably yes (unconfirmed, plan section 6 question 6)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No note for SAH-S02. The condition-wide classes (C1 to C5, C7, C9 to C12, C14) were applied as real errors, and the coital-trigger item of the M04 note 03a9ce4b (a class, ruling 2) per plan C11. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations` | Duplicate "24-72 hours" securing musts (C1). | FIXED: one MUST-SECURE (right PComA, as early as feasible, preferably within 24 hours). Securing pearl replaced. |
| C | major | `action_criteria`, `followup_outputs` | No catheter angiography (C3). | FIXED: recommended `dsa-aneurysm-anatomy` and a diagnostic DSA follow-up: aneurysm 6.3 x 5.3 mm (CTA 6.2 x 5.4), lobulated with a daughter sac, neck 3.1 mm, dome-to-neck 2.0, PComA arising from the inferior margin of the neck, anterior choroidal separate, no second aneurysm, no vasospasm. Soft CTA before DSA. |
| B | major | `followup_outputs` TCD | Day 5 TCD with right MCA vasospasm in a patient seen within hours (C2). | FIXED: day-0 baseline, normal velocities (MCA 59 to 63 cm/s, Lindegaard 1.5 to 1.6). |
| C | major | `required_recommendations` | BP 188/108 with no lowering action; lisinopril held with nothing replacing it (C5). | FIXED: MUST-BP-A (default agents) and MUST-HOME (withhold lisinopril, continue atorvastatin, hold metformin in critical care with insulin for glucose 186 mg/dL, avoiding hypoglycemia). |
| C | major | `required_recommendations`, `prohibited_recommendations` | Nimodipine must without hypotension adjustment; wrong IV prohibition; ICU SBP target; daily TCD must (C4, C5). | FIXED: MUST-NIMO, MUST-ICU, MUST-DCI, canonical prohibitions. |
| D | major | `followup_outputs` literature `request_sah_guidelines` | Literature step with "24-48 hours" and a case-specific coital-prognosis claim (C7). | FIXED: deleted; canonical literature output last; criterion `optional`. |
| C | minor | drug check, `action-7` | Template expected evidence about DOAC/warfarin; atorvastatin and metformin not addressed; "hold if SBP <100" instead of the dose adjustment (C10). | FIXED: tier `recommended` (plan); output in report voice with lisinopril, atorvastatin, metformin and contrast (eGFR above 30, no hold needed), the penicillin allergy as irrelevant, BP check with the 30 mg every 2 hours adjustment, no parenteral injection, CYP3A4; case-specific rationale and evidence. |
| B | minor | `ground_truth.differential`, `red_herrings` | Coital onset, a classic RCVS trigger, had no entry (class of M04 note 03a9ce4b, plan C11). | FIXED: RCVS `low` with the coital-trigger wording; red herring "Headache onset during sexual intercourse" (field `patient.history_present_illness`) with the plan's interpretation. Other entries canonical. |
| B | major | telemetry follow-up, `action-8` | Template text, management words, 24 h (C12). | FIXED: 4 h, sinus rhythm/tachycardia 86 to 110 bpm, 6 PVCs, no sustained arrhythmia or pauses, QTc 490 ms (ECG 494). |
| C | minor | labs BMP | Magnesium never measured (C9). | FIXED: 1.9 mg/dL (1.7-2.2). QTc 494: no MUST-QT. |
| B | minor | CTA follow-up | No neck measurement; neck vessels not described although the differential relies on them. | FIXED: neck 3.1 mm in observations, findings and impression; cervical carotid and vertebral arteries patent, no dissection. |
| D | minor | CT `additional_observations` | The differential needs the CT to state the sella and sinuses. | FIXED: "Sella normal in size without mass; no hyperdense dural venous sinus" added. |
| B | minor | echo follow-up | "Moderate Takotsubo cardiomyopathy" and "moderate Takotsubo pattern" next to "LVEF 44%, mildly reduced"; "classic Takotsubo". | FIXED: findings and LV chamber describe the wall motion and EF; wall motion "Takotsubo pattern". Impression unchanged. |
| E | minor | labs type and screen; `metadata.difficulty_rationale` | Engineering sentence; "consult" and "nimodipine" listed as tool steps. | FIXED: `clinical_significance` null; rationale describes the diagnostic chain and the coital distractor. |
| C | minor | `key_clinical_evidence` | Template pearls (C1, 1.3). | FIXED: four canonical pearls. |
| A | minor | criteria, order, constraints, stop rule | Label-copied rationales, free-text citations, literature recommended, no constraints, allowance 0. | FIXED: canonical rationales and citations, case-specific evidence; order NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, allowance 1. Labels kept. |

## Changes, in one paragraph a physician can read before re-reviewing

Patient, exam (GCS 15, HH2 after a one-minute confusion), CT (Fisher 3, no IVH or hydrocephalus), CTA (6.2 x 5.4 mm right PComA aneurysm, now with a 3.1 mm neck), ECG (QTc 494 ms), labs and echo (LVEF 44%) are unchanged in substance; magnesium 1.9 mg/dL is added and the CT and CTA now state the sella, sinuses and neck vessels used by the differential. The pathway is NCCT, labs, ECG, CTA, a new diagnostic catheter angiography, the nimodipine check covering lisinopril, atorvastatin and metformin, echo, a 4-hour telemetry report, an optional day-0 TCD with normal velocities (replacing the day-5 vasospasm report) and an optional literature search last. The coital onset is now scored as a reasoning point: RCVS stays low with the coital-trigger wording and a red herring explains why basal-cistern blood with a saccular aneurysm settles it. Musts: enteral nimodipine with the 30 mg every 2 hours adjustment; securing the right PComA aneurysm as early as feasible, preferably within 24 hours; neurocritical care; BP lowering now from 188/108; withholding lisinopril, continuing atorvastatin, insulin instead of metformin; sodium monitoring; DCI surveillance.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` in the canonical literature output needs the SAH allow-list (plan 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: patient block unchanged; coital-trigger red herring and RCVS wording per plan C11 (likelihood `low`); CTA vs DSA (6.2 x 5.4 vs 6.3 x 5.3 mm, neck 3.1 mm); drug check (lisinopril, atorvastatin, metformin, penicillin allergy) consistent with the medication and allergy lists, no leak; MUST-HOME metformin hold for critical care (not for contrast, creatinine 1.1) consistent with the drug-check statement; telemetry vs ECG; differential vs reports; stop rule, constraints, LP `harm` (no IVH).
Found: `initial_tool_outputs.labs.abnormal_values_summary` omitted HbA1c 7.4%, which the panel flags and the interpretation and the labs criterion list (minor).
- FLAGGED for the lead (condition-wide, not changed here): `fallback_tool_outputs.cardiac_monitoring` is a 24-hour Holter report, which cannot exist at assessment time (same reasoning as C12); it answers only a non-telemetry order, but the class spans all 30 cases.
Changed: added "HbA1c 7.4%" to `abnormal_values_summary`. Checks re-run after verification: `perfect_agent.py -v` passes (NCCT and labs show the known `<- ?` display artefact; the initial CT and labs carry the expected evidence by content), `case_io.py check` clean for the case, `test_case_guards.py -k` passes (no leak in the literature or drug-check outputs).


## Condition audit (auditor, 24 Oct 2026)

- `initial_tool_outputs.labs.abnormal_values_summary` rewritten to values and flags only. It named interpretations ("leukocytosis", "stress hyperglycemia", "neurogenic" troponin); "neurogenic" gives away the troponin red herring's answer, and the labs report carries no cross-modality interpretation. Same class as the fix already made in S05 to S10. Values, flags and the labs criterion unchanged.
- Checks after the audit: `perfect_agent.py` 30/30 pass; `case_io.py check` schema and synonym guard OK, no test failure names an SAH case; `test_case_guards -k SAH` 60 passed.
