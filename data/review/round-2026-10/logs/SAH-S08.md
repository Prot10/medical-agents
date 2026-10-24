# SAH-S08
Reviewer status: R1 none, R2 approved (with 3 notes) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 6e139dfe-4ffd-45f4-85a0-a303f583594e | FIXED | The cocaine literature follow-up ("avoid labetalol ... use phentolamine or nicardipine") is deleted (C7); the drug-check warning that said "Nicardipine or labetalol IV preferred" now reads "Cocaine use: avoid beta-blockers; labetalol is not first line; use nicardipine or clevidipine, with benzodiazepines for agitation and tachycardia" (`followup_outputs[2].output.warnings[0]`). The case now gives one instruction on labetalol, the same in the drug check, the BP must and a new prohibition. |
| 25ff44d7-2ee9-4cc5-9b44-32766f58adbe | FIXED | Securing: the two "24-72 hours" musts replaced by one MUST-SECURE (urgent joint review, coiling or clipping of the AComA aneurysm as early as feasible, preferably within 24 hours of onset, [Hoh_2023]); securing pearl replaced. DSA: new recommended criterion `dsa-aneurysm-anatomy` and diagnostic follow-up `request_digital_subtraction_angiography` (6.6 x 5.7 mm multilobulated aneurysm with a daughter sac, neck 3.6 mm, dome-to-neck 1.8, no second aneurysm, no vasospasm or segmental vasoconstriction). Timeline: the day-7 TCD with severe ACA vasospasm and a CT perfusion recommendation is now a day-0 baseline with normal velocities. |
| 4f899419-8c58-4575-a0cc-899716794530 | FIXED | BP must added (plan wording for S08): "Lower blood pressure now with a nicardipine or clevidipine infusion and treat cocaine-related agitation and tachycardia with a benzodiazepine; do not give beta-blockers during acute cocaine toxicity; avoid hypotension [Hoh_2023]." The ICU must no longer carries the SBP 160 limit (MUST-ICU); BP prohibition canonical; prohibition added "Do not give beta-blockers for blood pressure or heart rate control during acute cocaine toxicity (unopposed alpha-adrenergic vasoconstriction)." |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `required_recommendations`, `prohibited_recommendations` (nimodipine) | Nimodipine must without the hypotension adjustment; IV prohibition wrong as written (C4). | FIXED: MUST-NIMO and the canonical parenteral-injection prohibition. |
| C | minor | `required_recommendations` TCD must | "Daily TCD days 4-14" overstates TCD (COR 2a). | FIXED: MUST-DCI. |
| C | minor | `action-7-check-drug-interactions` | Recommended with the template anticoagulation evidence in a man on no medicines (C10). | FIXED: `optional`, case-specific rationale and evidence; output in report voice (no regular medicines, cocaine BP-agent caution, BP before each dose with the 30 mg every 2 hours adjustment, CYP3A4, no parenteral injection). Leak guard passes. |
| B | minor | CTA `angiography_findings`, `impression` | "large" for a 6.4 mm aneurysm (C13); no statement on the cervical vessels. | FIXED: "large" removed in both; "Cervical carotid and vertebral arteries: Patent, no dissection or stenosis". |
| D | minor | `followup_outputs` echo `chambers.LV`, `findings` | Echo attributed the dysfunction to "combined cocaine cardiotoxicity and Takotsubo" (cross-modality cause inside an echo report). | FIXED: "Moderate apical hypokinesis"; findings "LVEF 42%, moderately reduced", "Apical hypokinesis with basal hyperkinesis". Impression unchanged. |
| B | major | `followup_outputs` telemetry, `action-8` | Template text with management, 24 h duration (C12). | FIXED: 4 h since arrival, sinus tachycardia 102 to 124 bpm, 30 unifocal PVCs, no sustained arrhythmia or pauses, QTc 496 ms on monitoring leads (ECG 498) without torsades. |
| B | minor | `patient.history_present_illness` | "He is a non-smoker and non-drinker" while the social history records occasional alcohol. | FIXED: "He is a non-smoker, drinks alcohol occasionally and has no medical history." |
| B | minor | `initial_tool_outputs.labs` | Magnesium never measured (C9); interpretive words in `abnormal_values_summary`. | FIXED: magnesium 2.0 mg/dL added; summary lists values and flags only. Potassium 3.6 was present; QTc 498, so no MUST-QT. |
| B | minor | `ground_truth.differential`, CT `additional_observations` | Generic key features; cocaine, a vasoactive trigger of RCVS, not mentioned (C11). | FIXED: canonical key features with "Thunderclap onset, and the cocaine trigger, overlap with SAH ..."; RCVS stays `low` (basal-cistern blood, saccular aneurysm, no segmental vasoconstriction on DSA); CT states a normal sella and no hyperdense sinus. |
| C | minor | `ground_truth.key_clinical_evidence` | 24-72 h, daily-TCD, CT-sensitivity and xanthochromia pearls (C1, plan 1.3). | FIXED: the four canonical pearls; the other six kept. |
| A | minor | `ground_truth.action_criteria[*]`, order, `sequence_constraints`, `stop_rule`, `metadata.difficulty_rationale` | Label-copied rationales, duplicate free-text citations, literature before the echo, no constraints, allowance 0; "7-8 required tools" rationale. | FIXED: canonical rationales and citations, case-specific evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check (optional), echo, telemetry, TCD (optional), literature (optional); follow-ups in the same order; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, `max_additional_actions` 1; difficulty rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

The presentation is unchanged (38-year-old man, thunderclap headache 30 to 45 minutes after cocaine, one minute of lost consciousness, now GCS 15, BP 212/126, HR 118), except that the HPI now agrees with the social history on occasional alcohol. CT (extensive Fisher 3, no IVH or hydrocephalus), CTA (6.4 x 5.8 mm multilobulated AComA aneurysm, no longer called "large"), ECG (QTc 498 ms) and echo (LVEF 42%, stress pattern, without the cocaine attribution) are unchanged in substance; labs add magnesium 2.0. The pathway is NCCT, labs, ECG, CTA, a new diagnostic catheter angiography (daughter sac, 3.6 mm neck, no segmental vasoconstriction), an optional nimodipine check (no medicines; cocaine caution), echo, 4 hours of telemetry (sinus tachycardia, PVCs, QTc 496 ms), an optional day-0 baseline TCD and an optional general literature search last. The musts now say: enteral nimodipine with the 30 mg every 2 hours adjustment; secure the AComA aneurysm as early as feasible, preferably within 24 hours; neurocritical care admission; lower BP now with a nicardipine or clevidipine infusion, benzodiazepine for agitation and tachycardia, no beta-blockers, avoid hypotension; sodium monitoring; DCI surveillance with euvolemia. A prohibition of beta-blockers during acute cocaine toxicity joins the existing cocaine prohibition.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` (canonical literature output) must be added to the SAH criteria-pack allow-list (plan section 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the git diff (patient block changed only in the HPI alcohol sentence, which now matches the social history); the three notes against the file (cocaine literature gone; no text anywhere calls labetalol preferred; BP must in the plan's S08 wording; ICU must without the SBP 160 limit; beta-blocker prohibition added; one MUST-SECURE; DSA criterion and output with no segmental vasoconstriction; day-0 TCD); drug check `optional` (no medicines, plan C10); RCVS `low` with the cocaine trigger named and DSA excluding segmental vasoconstriction; echo report no longer attributes the cardiomyopathy to cocaine; telemetry QTc 496 against ECG 498 (no MUST-QT, below 500); DSA arithmetic (6.6 / 3.6 = 1.8); lab flags; LP avoided action `harm`; leak guard passes.
Considered and left: the drug check says "labetalol is not first line" while the must and prohibition exclude beta-blockers; this is the plan's wording and no longer gives opposite instructions, which was the note's point. The CTA calls the dome multilobulated and the DSA adds a daughter sac; acceptable gain in detail from 3D rotational angiography.
Found: no error. No change made.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
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
