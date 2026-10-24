# SAH-S10
Reviewer status: R1 none, R2 approved (with 1 note) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 66c7702e-ae23-405b-8ba8-d7325301e810 | FIXED | Securing: the two "24-72 hours" musts replaced by one MUST-SECURE (urgent joint neurosurgical and neurointerventional review, coiling or clipping of the AComA aneurysm as early as feasible, preferably within 24 hours of onset, [Hoh_2023]); securing pearl replaced. DSA: new recommended criterion `dsa-aneurysm-anatomy` and diagnostic follow-up `request_digital_subtraction_angiography` (4.7 x 4.1 mm aneurysm with an apical nipple-like bleb, neck 2.4 mm, dome-to-neck 2.0, A2 origins clear, no second aneurysm, no vasospasm). Timeline: the day-6 TCD with ACA vasospasm is now a day-0 baseline with normal velocities. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `required_recommendations` BP and home drugs | BP 192/112 with no BP-lowering action; hydrochlorothiazide held with nothing replacing it; the lithium plan existed only inside the drug check and literature (C5, C10). | FIXED: MUST-BP-A (nicardipine or clevidipine infusion, or labetalol boluses; LVEF 52%, no bradycardia); must "Withhold hydrochlorothiazide and check serum lithium and sodium together at least daily, as SAH-related hyponatremia raises lithium levels." |
| C | major | `followup_outputs` drug check, `action-7` | Lithium monitoring "every 24-48h" (weaker than the daily check the case needs), BP alternative offered inside the check, nothing on the fall in lithium after the thiazide stops or on NSAIDs and ARBs; criterion recommended with template anticoagulation evidence. | FIXED: output rewritten in report voice (HCTZ additive hypotension and reduced lithium clearance, hyponatremia and volume depletion raise lithium, no important nimodipine-lithium interaction, levels fall after HCTZ stops, lithium and sodium at least daily, toxicity can mimic deterioration, avoid NSAIDs, ACE inhibitors and ARBs, BP before each dose with the 30 mg every 2 hours adjustment, no parenteral injection); criterion `required` (plan C10) with case-specific rationale and evidence, in the stop rule. Leak guard passes. |
| D | major | `followup_outputs` literature (lithium monitoring, sodium management) | Literature as clinical steps; "SIADH: euvolemia + low urine osmolality" is wrong (SIADH has inappropriately concentrated urine) (C7). | FIXED: both deleted; canonical literature output last; criterion `optional` with canonical text. |
| C | major | `required_recommendations`, `prohibited_recommendations` (nimodipine) | Nimodipine must without the hypotension adjustment; IV prohibition wrong as written (C4). | FIXED: MUST-NIMO and the canonical parenteral-injection prohibition. |
| C | minor | ICU and TCD musts, BP prohibition | SBP target in the ICU must, daily-TCD must, "SBP >160" as a guideline threshold. | FIXED: MUST-ICU, MUST-DCI, canonical BP prohibition. |
| B | major | `followup_outputs` TCD | "Daily TCD through day 14" and day-6 vasospasm in a patient seen within hours (C2). | FIXED: canonical day-0 baseline (MCA 62 to 66 cm/s, Lindegaard 1.7 to 1.8) and recommendation. |
| B | major | `followup_outputs` telemetry, `action-8` | Template text with management, 24 h duration (C12). | FIXED: 4 h since arrival, sinus rhythm and sinus tachycardia 86 to 106 bpm, 12 isolated PVCs, no sustained arrhythmia or pauses, QTc 480 ms on monitoring leads (ECG 482) without torsades. |
| B | minor | `initial_tool_outputs.labs` | Magnesium never measured (C9); type-and-screen engineering sentence; `abnormal_values_summary` listed a normal lithium level with advice ("therapeutic but monitor closely") and interpretive words. | FIXED: magnesium 2.1 mg/dL added; type-and-screen `clinical_significance` null; summary lists only the out-of-range values with flags. Potassium 3.6 was present; QTc 482, no MUST-QT. |
| B | minor | `ground_truth.differential`, CT `additional_observations`, CTA `angiography_findings` | Generic key features (C11); reports did not state the sella, sinuses or neck vessels the key features cite. | FIXED: canonical key features; CT "Sella normal in size without mass; no hyperdense dural venous sinus"; CTA "Cervical carotid and vertebral arteries: Patent, no dissection or stenosis". |
| C | minor | `ground_truth.key_clinical_evidence` | 24-72 h, daily-TCD, CT-sensitivity and xanthochromia pearls (C1, plan 1.3). | FIXED: the four canonical pearls; the other six kept. |
| A | minor | `ground_truth.action_criteria[*]`, order, `sequence_constraints`, `stop_rule`, `metadata.difficulty_rationale` | Label-copied rationales, duplicate free-text citations, drug check at step 1 before the CTA, no constraints, allowance 0; "7-8 required tools" rationale. | FIXED: canonical rationales and citations, case-specific evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD (optional), literature (optional); follow-ups in the same order; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, drug check, `max_additional_actions` 1; difficulty rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

The presentation is unchanged (53-year-old man with hypertension on hydrochlorothiazide and bipolar disorder on lithium 600 mg twice daily, thunderclap headache with transient confusion, now GCS 15, BP 192/112). CT (Fisher 3, no IVH or hydrocephalus), CTA (4.6 x 4.0 mm AComA aneurysm with a nipple sign), ECG (QTc 482 ms), labs (lithium 0.9 mEq/L, sodium 139) and echo (LVEF 52%, mild stress pattern) are unchanged; the CT adds a normal sella and no hyperdense sinus, the CTA normal cervical vessels, the labs magnesium 2.1. The pathway is NCCT, labs, ECG, CTA, a new diagnostic catheter angiography (apical bleb, 2.4 mm neck), the required lithium and thiazide check, echo, 4 hours of telemetry (sinus rhythm, PVCs, QTc 480 ms), an optional day-0 baseline TCD and an optional general literature search last. The musts now say: enteral nimodipine with the 30 mg every 2 hours adjustment; secure the AComA aneurysm as early as feasible, preferably within 24 hours; neurocritical care admission; lower BP now with nicardipine, clevidipine or labetalol; withhold hydrochlorothiazide and check lithium and sodium together at least daily; sodium monitoring; DCI surveillance with euvolemia.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` (canonical literature output) must be added to the SAH criteria-pack allow-list (plan section 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the git diff (patient block unchanged); note 66c7702e against the file (one MUST-SECURE, DSA criterion and output with the nipple-like bleb matching the CTA nipple sign, day-0 TCD); lithium must and drug-check content (thiazide and hyponatremia raise lithium, fall after the thiazide stops, NSAID, ACE inhibitor and ARB warning; no "low urine osmolality" SIADH text left); drug check `required`, in the stop rule, after the CTA; DSA arithmetic (4.7 / 2.4 = 2.0); lab flags (lithium 0.9 in range, sodium 139); telemetry QTc 480 against ECG 482; leak guard passes.
Found and changed: the ECG called a rate of 98 "Sinus tachycardia" (pre-existing internal inconsistency; vitals HR 98). `initial_tool_outputs.ecg.rhythm` now "Normal sinus rhythm", the interpretation "Normal sinus rhythm, rate 98.", and the `action-5-analyze-ecg` expected evidence "Sinus rhythm 98 ...". Telemetry already reads sinus rhythm and sinus tachycardia (86 to 106).
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
