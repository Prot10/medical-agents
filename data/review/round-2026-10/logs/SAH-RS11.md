# SAH-RS11
Reviewer status: R1 none, R2 none (no notes and no status in the notes file; the plan treats it as one of R2's 21 approvals) | Approved before this round: probably yes (unconfirmed, plan section 6 question 6)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for SAH-RS11. The condition-wide classes of the plan (C1 to C5, C7, C9 to C12, C14) were applied because they are real errors in this case too. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations` | Two duplicate securing musts with a "24-72 hours" window that no guideline gives (plan C1); no step secures the 6.8 mm AComA aneurysm. | FIXED: one MUST-SECURE (AComA, as early as feasible, preferably within 24 hours, [Hoh_2023]). |
| C | major | `ground_truth.action_criteria`, `followup_outputs` | No catheter angiography before securing (C3). | FIXED: new recommended criterion `dsa-aneurysm-anatomy` (order_advanced_imaging, modality cerebral_angiography) and a diagnostic DSA follow-up `request_digital_subtraction_angiography`: aneurysm 6.9 x 5.5 mm (CTA 6.8 x 5.6), daughter sac, neck 3.8 mm, dome-to-neck 1.8, right A1 dominant, A2 origins clear of the neck, no second aneurysm, no vasospasm; no treatment content. Soft constraint CTA before DSA. |
| B | major | `followup_outputs` TCD | TCD dated "day 7" with moderate-to-severe vasospasm and a CT perfusion recommendation, impossible for a patient seen within hours of the ictus and never secured (C2). | FIXED: admission baseline, `quantitative_data` {post_ictus_day: 0}, normal MCA/ACA/basilar velocities (MCA 62 to 66 cm/s, Lindegaard 1.6 to 1.7), canonical protocol, impression and serial-TCD recommendation. |
| C | major | `required_recommendations` (BP, home drug), drug-check follow-up | Presenting BP 188/114 with no BP-lowering action; amlodipine held with nothing replacing it (C5). | FIXED: MUST-BP-A (nicardipine or clevidipine infusion, or labetalol boluses; LVEF 46%, no bradycardia or asthma) and MUST-HOME "Withhold amlodipine while on nimodipine (additive dihydropyridine effect)". |
| C | major | `action-7-check-drug-interactions` | Tier recommended and template expected evidence ("anticoagulation reversed if ... DOAC or warfarin") in a patient on amlodipine and no anticoagulant (C8, C10). | FIXED: `required` (dihydropyridine with nimodipine changes management), case-specific rationale and expected evidence; added to the stop rule. Output rewritten in report voice: amlodipine interaction and half-life, BP check before each dose with the 30 mg every 2 hours adjustment, no parenteral injection of capsule contents, CYP3A4. No leak (guard passes). |
| C | major | `required_recommendations` nimodipine, `prohibited_recommendations` | Nimodipine must without the hypotension adjustment; "Do not administer nimodipine intravenously" is wrong as written (IV infusion exists in Europe; the hazard is parenteral injection of capsule contents) (C4). | FIXED: MUST-NIMO and the canonical prohibition. |
| C | minor | `prohibited_recommendations` BP line | "SBP >160" presented as a guideline threshold. | FIXED: canonical BP prohibition. |
| C | minor | `required_recommendations` ICU and TCD musts | ICU must carried an SBP target; "daily TCD days 4-14" must overstates TCD (COR 2a). | FIXED: MUST-ICU and MUST-DCI (frequent examination, TCD as adjunct, euvolemia, no prophylactic hypervolemia). |
| D | major | `followup_outputs` literature (smoking cessation) | Literature as a clinical step (recommended), case-specific query, unsourced "class I" claim (C7, ruling 5). | FIXED: deleted; canonical literature output last; criterion `optional`, canonical rationale, evidence and citations. |
| B | major | `followup_outputs` telemetry, `action-8` expected evidence | Template text identical in all 30 cases, containing management, 24 h duration impossible at assessment (C12). | FIXED: 4 h since arrival, sinus rhythm/tachycardia 84 to 108 bpm, 14 isolated PVCs, no sustained arrhythmia or pauses, QTc 490 ms (ECG 494) with no torsades. |
| C | minor | `initial_tool_outputs.labs.panels.BMP` | Magnesium never measured (C9). | FIXED: magnesium 2.1 mg/dL (1.7-2.2), normal; potassium 3.6 already present. QTc 494, no MUST-QT (threshold 500). |
| E | minor | `initial_tool_outputs.labs.panels["Baseline workup"]` type and screen | Engineering sentence "which is what this case's diagnosis rests on" (C14). | FIXED: `clinical_significance` null. |
| B | minor | `ground_truth.differential` | Generic key features ("pituitary MRI / CT without sellar enlargement excludes", "CT venogram ... indicated if SAH excluded") not tied to the case (C11). | FIXED: canonical key features citing this case (exertional trigger for RCVS, basal-cistern blood, AComA aneurysm); all `low`, migraine `very_low`. |
| B | minor | `initial_tool_outputs.ct.additional_observations`, CTA `angiography_findings` | The differential now cites "no sellar mass, no hyperdense sinus" and "CTA of the neck shows no dissection", which the reports did not state. | FIXED: CT observations "No intraventricular hemorrhage" and "Sella normal in size without mass; no hyperdense dural venous sinus"; CTA "Cervical carotid and vertebral arteries: Patent, no dissection or stenosis". |
| D | minor | CTA `angiography_findings` AComA | "clearly ruptured": imaging cannot assert rupture with certainty; the impression already says "consistent with the source". | FIXED: "...with irregular lobulation and a daughter sac". |
| C | minor | `ground_truth.key_clinical_evidence` | 24-72 h securing pearl, "vasospasm peaks days 4-14 ... daily TCD" pearl, CT sensitivity "~98% ... 80-85% by 24 hours", xanthochromia "6-12 hours" (C1, plan 1.3). | FIXED: the four canonical pearls; the other six kept. |
| A | minor | `ground_truth.action_criteria[*]` | Rationale copied from the label; free-text and unbracketed duplicate citations; ECG/telemetry/echo cited to Connolly (plan 1.1, 1.3). | FIXED: canonical rationales, case-specific expected evidence, `["[Hoh_2023]"]` (literature: Hunt-Hess, Fisher, Hoh). Labels kept. |
| A | minor | `action_criteria` order, `followup_outputs` order, `sequence_constraints`, `stop_rule` | Literature and TCD before the work-up; no constraints; allowance 0 (plan section 3). | FIXED: criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD (optional), literature (optional); follow-ups CTA, DSA, drug check, echo, telemetry, TCD, literature; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, drug check, `max_additional_actions` 1. |
| D | minor | `patient.history_present_illness`, `patient.neurological_exam.additional` | "Hunt-Hess Grade 2" in the patient block is an SAH-specific grade stated before any imaging. | FLAGGED, not changed: the plan keeps the Hunt-Hess grade in the exam in all 30 cases (C13) and it reveals no study result; a condition-wide decision, see Open questions. |

## Changes, in one paragraph a physician can read before re-reviewing

The presentation, CT, CTA, ECG, labs and echo are unchanged in substance (54-year-old woman, exertional thunderclap headache, HH2, Fisher 3 without IVH or hydrocephalus, 6.8 mm AComA aneurysm with a daughter sac, neurogenic T waves with QTc 494 ms, troponin 0.24, LVEF 46% stress pattern). Magnesium 2.1 mg/dL was added to the labs; the CT now states no IVH, a normal sella and no hyperdense sinus, and the CTA states normal cervical vessels, which the updated differential cites. The pathway is now NCCT, labs, ECG, CTA, a new diagnostic catheter angiography (no second aneurysm, no vasospasm, A2 origins clear of the neck), the required nimodipine-amlodipine check, echo, a 4-hour telemetry report (sinus, isolated PVCs, QTc 490 ms), an optional admission-baseline TCD (day 0, normal velocities, replacing the day-7 vasospasm report) and an optional general literature search last. The musts now say: enteral nimodipine 60 mg every 4 hours for 21 days (30 mg every 2 hours if hypotensive); secure the AComA aneurysm by coiling or clipping as early as feasible, preferably within 24 hours, after joint review; neurocritical care admission; lower BP now from 188/114 with nicardipine, clevidipine or labetalol, no numeric 2023 target, SBP below 160 commonly used, avoid hypotension; withhold amlodipine while on nimodipine; sodium monitoring; DCI surveillance with euvolemia and no prophylactic hypervolemia. The IV nimodipine and BP prohibitions and four teaching pearls use the condition's canonical wording.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` (ISAT) is cited in the canonical literature output; it must be added to the SAH criteria-pack allow-list (plan section 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case. Condition-wide (for the lead): "Hunt-Hess Grade 2" appears in the HPI and exam before any imaging; it names an SAH grade in the patient block. I kept it, following the plan; removing it would be a condition-wide change.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: the diff against HEAD field by field (patient block unchanged; criteria ids, labels and alternatives unchanged; tiers drug check recommended to required, literature to optional, per plan C10 and C7); every must, prohibition and pearl against plan 1.2 and 1.3; CT, CTA, DSA (6.9 x 5.5 mm vs CTA 6.8 x 5.6 mm, neck 3.8 mm both), telemetry (84 to 108 bpm vs ECG 102; QTc 490 vs 494), TCD (day 0, normal), labs (magnesium added, summary and interpretation agree), drug check (amlodipine, no leak), differential against the CT and CTA statements it cites (sella, sinuses, cervical vessels now in the reports), stop rule = required criteria, sequence constraints, LP avoided action `harm` (no IVH or hydrocephalus). No note exists for this case.
Found: nothing that needed a change. The echo findings list still says "Takotsubo cardiomyopathy" and "Apical ballooning" while the impression says "pattern"; this is acceptable echo wording in a probably approved case and was left. "Hunt-Hess Grade 2" in the patient block stays as the worker flagged (plan keeps it).
- FLAGGED for the lead (condition-wide, not changed here): `fallback_tool_outputs.cardiac_monitoring` is a 24-hour Holter report, which cannot exist at assessment time (same reasoning as C12); it answers only a non-telemetry order, but the class spans all 30 cases.
Changed: nothing. Checks re-run after verification: `perfect_agent.py -v` passes (NCCT and labs show the known `<- ?` display artefact; the initial CT and labs carry the expected evidence by content), `case_io.py check` clean for the case, `test_case_guards.py -k` passes (no leak in the literature or drug-check outputs).


## Condition audit (auditor, 24 Oct 2026)

- `initial_tool_outputs.ecg` finding "Deep symmetric T-wave inversions V1-V5 (neurogenic pattern)" now "Deep symmetric T-wave inversions V1-V5". The ECG cannot know the cause (cross-modality attribution that answers the cardiac red herring); same fix as in M01 and P08.
- Checks after the audit: `perfect_agent.py` 30/30 pass; `case_io.py check` schema and synonym guard OK, no test failure names an SAH case; `test_case_guards -k SAH` 60 passed.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `patient.history_present_illness (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `echo.wall_motion`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `red_herrings[0].correct_interpretation (echo does not confirm etiology)`: an echocardiogram does not confirm the etiology of neurogenic myocardial injury; the interpretation now states the case's own echo (audit class, Q10).
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
