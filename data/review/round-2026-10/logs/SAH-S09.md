# SAH-S09
Reviewer status: R1 none, R2 approved (with 1 note) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 899fabe8-c432-4165-bde1-0c1132149643 | FIXED | Securing: the two "24-72 hours" musts replaced by one MUST-SECURE (urgent joint neurosurgical and neurointerventional review, coiling or clipping of the left PComA aneurysm as early as feasible, preferably within 24 hours of onset, [Hoh_2023]); securing pearl replaced. DSA: new recommended criterion `dsa-aneurysm-anatomy` and diagnostic follow-up `request_digital_subtraction_angiography` (4.9 x 4.3 mm aneurysm with a posterolateral bleb, neck 2.6 mm, dome-to-neck 1.9, non-fetal PComA patent at the neck margin, no second aneurysm, no vasospasm). Timeline: the day-6 TCD with left MCA vasospasm and a CT perfusion suggestion is now a day-0 baseline with normal velocities. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `required_recommendations` BP and home drugs, drug-check output | BP 186/110 with no BP-lowering action; candesartan and furosemide held with nothing replacing them (C5). | FIXED: MUST-BP-A (nicardipine or clevidipine infusion, or labetalol boluses; LVEF 52%); MUST-HOME "Withhold candesartan and furosemide during the acute phase (...); hold metformin during the admission because of iodinated contrast for CTA and angiography with eGFR 42, and manage glucose with insulin, avoiding hypoglycemia." |
| C | minor | `followup_outputs` drug check | "HOLD metformin before IV contrast AND hold 48h after contrast" (a fixed 48 h rule; current practice ties metformin to renal function and acute kidney injury, and in an acute admission it is withheld and insulin used); "Hold candesartan during nimodipine course" stated as a nimodipine rule; no word on insulin. | FIXED: output rewritten in report voice (candesartan additive hypotension, furosemide volume and K/Mg loss, metformin withheld for contrast and acute illness with restart once renal function is stable, glargine no interaction, BP before each dose with the 30 mg every 2 hours adjustment, hepatic CYP3A4 elimination without routine renal dose change, no parenteral injection). Criterion stays `recommended` (plan C10) with case-specific rationale and evidence. Leak guard passes. |
| B | minor | `initial_tool_outputs.labs.panels.BMP` Creatinine | Creatinine 1.8 mg/dL gives an eGFR of about 30 mL/min/1.73 m2 (CKD-EPI 2021, woman aged 67), against the documented eGFR 42 in the history and HPI and with no acute kidney injury described. | FIXED: creatinine 1.4 mg/dL (eGFR about 41); summary and interpretation updated. BUN 28 kept. |
| B | minor | `initial_tool_outputs.labs` | Magnesium never measured (C9); type-and-screen engineering sentence; interpretive words ("CKD anemia", "neurogenic") in `abnormal_values_summary` (C14). | FIXED: magnesium 1.8 mg/dL (low-normal on furosemide, ref 1.7-2.2) added; type-and-screen `clinical_significance` null; summary lists values and flags only. Potassium 4.8 was present; QTc 476, no MUST-QT. |
| D | minor | CTA `additional_observations[2]`, echo `findings[1]` | CTA "IV hydration pre and post" (management inside a report, ruling 4); echo "BNP elevation in context of CKD and SAH" (cross-modality). | FIXED: CTA "IV contrast CTA, low-volume contrast protocol"; echo finding "Mild apical hypokinesis with preserved basal segments". CTA also states "Cervical carotid and vertebral arteries: Patent, no dissection or stenosis". |
| D | major | `followup_outputs` literature (contrast nephropathy, glucose) | Literature as clinical steps with patient values ("eGFR 42"), an empty summary, and management orders (C7). | FIXED: both deleted; canonical literature output last; criterion `optional` with canonical text. The glucose content that matters (insulin, avoid hypoglycemia) is in MUST-HOME. |
| C | major | `required_recommendations`, `prohibited_recommendations` (nimodipine) | Nimodipine must without the hypotension adjustment; IV prohibition wrong as written (C4). | FIXED: MUST-NIMO and the canonical parenteral-injection prohibition. |
| C | minor | ICU and TCD musts, BP prohibition | SBP target in the ICU must, daily-TCD must, "SBP >160" as a guideline threshold. | FIXED: MUST-ICU, MUST-DCI, canonical BP prohibition. |
| B | major | `followup_outputs` telemetry, `action-8` | Template text with management, 24 h duration (C12). | FIXED: 3 h since arrival, sinus rhythm 82 to 102 bpm, 9 isolated PVCs, no sustained arrhythmia or pauses. |
| B | minor | `ground_truth.differential`, CT `additional_observations` | Generic key features (C11). | FIXED: canonical key features (basal-cistern blood, saccular left PComA aneurysm); CT states no intraventricular hemorrhage, a normal sella and no hyperdense sinus. |
| C | minor | `ground_truth.key_clinical_evidence` | 24-72 h, daily-TCD, CT-sensitivity and xanthochromia pearls (C1, plan 1.3). | FIXED: the four canonical pearls; the other six kept. |
| A | minor | `ground_truth.action_criteria[*]`, order, `sequence_constraints`, `stop_rule`, `metadata.difficulty_rationale` | Label-copied rationales, duplicate free-text citations, drug check at step 1 before the CTA, no constraints, allowance 0; "7-8 required tools" rationale. | FIXED: canonical rationales and citations, case-specific evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD (optional), literature (optional); follow-ups in the same order; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, `max_additional_actions` 1; difficulty rationale rewritten. `metadata.actions_withdrawn` (MRA) left as it is. |

## Changes, in one paragraph a physician can read before re-reviewing

The presentation is unchanged (67-year-old woman with hypertension, insulin-treated type 2 diabetes and CKD stage 3 with eGFR 42 on candesartan, metformin, glargine and furosemide; thunderclap headache 30 minutes before arrival; BP 186/110; penicillin anaphylaxis, which no recommended drug touches). CT (Fisher 3, left Sylvian predominance, no hydrocephalus), CTA (4.8 x 4.2 mm left PComA aneurysm with a bleb), ECG (QTc 476 ms) and echo (LVEF 52%, mild stress pattern) are unchanged in substance; creatinine now reads 1.4 mg/dL to match the documented eGFR 42 (it read 1.8, an eGFR of about 30), and magnesium 1.8 is added. The pathway is NCCT, labs, ECG, CTA, a new diagnostic catheter angiography (2.6 mm neck, PComA patent at its margin), the recommended home-drug check, echo, 3 hours of telemetry (sinus rhythm, isolated PVCs), an optional day-0 baseline TCD and an optional general literature search last. The musts now say: enteral nimodipine with the 30 mg every 2 hours adjustment; secure the left PComA aneurysm as early as feasible, preferably within 24 hours; neurocritical care admission; lower BP now with nicardipine, clevidipine or labetalol; withhold candesartan and furosemide, hold metformin for the contrast studies and manage glucose with insulin avoiding hypoglycemia; sodium monitoring; DCI surveillance with euvolemia.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` (canonical literature output) must be added to the SAH criteria-pack allow-list (plan section 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the git diff (patient block unchanged); note 899fabe8 against the file (one MUST-SECURE, DSA criterion and diagnostic output, day-0 TCD, no day-N text); creatinine change 1.8 to 1.4 verified (CKD-EPI 2021, woman 67: 1.4 gives about 41, 1.8 about 30, against the documented eGFR 42; no other field cites 1.8 for creatinine); magnesium 1.8 low-normal on furosemide; lab flags; no patient values left in literature; DSA arithmetic (4.9 / 2.6 = 1.9); drug check `recommended` per plan C10; leak guard passes.
Found and changed: the MUST-HOME said "hold metformin during the admission because of iodinated contrast for CTA and angiography with eGFR 42". Current contrast guidance (ACR Manual on Contrast Media) does not require stopping metformin for iodinated contrast when eGFR is 30 or more without acute kidney injury; the reason to hold it here is the acute critical illness, with insulin as the inpatient standard. Must now reads "... hold metformin while she is critically ill and manage glucose with insulin, avoiding hypoglycemia; recheck renal function after the iodinated contrast studies (eGFR 42)."; `action-7-check-drug-interactions.expected_evidence` changed accordingly ("metformin is held during the acute critical illness with repeated contrast, insulin continued"). The drug-check output already gives acute illness and contrast together and was left.
`perfect_agent.py -v` and `case_io.py check` clean after the edit.


## Condition audit (auditor, 24 Oct 2026)

- `ground_truth.red_herrings[0].correct_interpretation` still carried the condition template "echocardiogram showing apical ballooning confirms etiology", while this echo shows only mild apical hypokinesis (LVEF 52%). Now ends "...the echocardiogram shows only mild apical hypokinesis with preserved ejection fraction and no primary cardiac lesion, and the focus remains on aneurysm securing." Same fix as the verifiers made in S01, S04, P05 and P06.
- Checks after the audit: `perfect_agent.py` 30/30 pass; `case_io.py check` schema and synonym guard OK, no test failure names an SAH case; `test_case_guards -k SAH` 60 passed.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `echo.findings[0]`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.wall_motion`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.impression (Takotsubo overcall removed)`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `action_criteria[echo].expected_evidence`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
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
