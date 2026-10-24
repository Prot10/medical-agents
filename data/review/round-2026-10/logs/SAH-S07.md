# SAH-S07
Reviewer status: R1 none, R2 approved (with 3 notes) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 09f3f88b-7b15-493d-bbc4-4781ca0d3624 | FIXED | Securing: the two "24-72 hours" musts replaced by one MUST-SECURE (urgent joint neurosurgical and neurointerventional review, coiling or clipping of the right paraclinoid ICA aneurysm as early as feasible, preferably within 24 hours of onset, [Hoh_2023]); securing pearl replaced. DSA: new recommended criterion `dsa-aneurysm-anatomy` and diagnostic follow-up `request_digital_subtraction_angiography` (5.5 x 4.9 mm aneurysm with a superomedial bleb, neck 3.4 mm, dome-to-neck 1.6, ophthalmic artery origin separate, no second aneurysm, no vasospasm). Timeline: the day-7 TCD with right MCA vasospasm is now a day-0 admission baseline with normal velocities. |
| aa75afaa-2dab-42e4-8ea1-9bfaaaca6691 | FIXED | `ground_truth.key_clinical_evidence[-1]` "Polycystic kidney disease carries a 4-fold increase ... family-screening MRA in first-degree relatives is warranted" replaced by "ADPKD with a family history of intracranial aneurysm or SAH is an indication for screening MR angiography; this patient qualified but had never been screened." |
| db7c626e-f23a-4d71-baec-574d34083831 | FIXED | MUST-BP-A (nicardipine or clevidipine infusion, or labetalol boluses; LVEF 58%) and MUST-HOME "Withhold nifedipine extended-release while on nimodipine (additive dihydropyridine effect); continue levothyroxine." added to `required_recommendations`. The nimodipine part is ALREADY-FIXED: the nimodipine must was present; it now reads MUST-NIMO (enteral, 21 days, 30 mg every 2 hours if hypotensive). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.ct.findings[2]`, `.impression`, `.additional_observations` | A head CT reported "Multiple renal cysts ... right kidney partially visualized" (anatomically impossible, C14); observations "PKD patient - aneurysm association known" and "Contrast allergy - premedicate for CTA" (clinical text and management in a report); impression "contrast allergy history noted". | FIXED: kidney finding and impression item deleted; observations Fisher 3, no hydrocephalus, no intraventricular hemorrhage, "Sella normal in size without mass; no hyperdense dural venous sinus"; impression renumbered. |
| D | minor | CTA `additional_observations[2]` | "IV contrast CTA with diphenhydramine + methylprednisolone premedication" reports a management decision the agent has not made (ruling 4). | FIXED: "IV contrast CTA; no contrast reaction during the examination". CTA also states "Cervical carotid and vertebral arteries: Patent, no dissection or stenosis". |
| C | major | `required_recommendations` | The prior mild contrast rash had no management statement; the only guidance sat in a literature output with doses. | FIXED: must "Do not let the prior mild contrast rash delay contrast imaging (CTA, catheter angiography); give accelerated premedication per local protocol only if it causes no delay." (plan wording widened from "the CTA" to both contrast studies, since the CTA is already done when the agent writes its assessment and the DSA also needs contrast); red herring added for the listed contrast allergy. |
| C | major | `followup_outputs` drug check, `action-7` | Output "hold if SBP <100" (unsourced threshold), "Resume nifedipine after 21-day nimodipine course", no word on levothyroxine; criterion recommended with the template anticoagulation evidence (C10). | FIXED: output rewritten in report voice (additive dihydropyridine hypotension, levothyroxine no interaction, withhold nifedipine and review restart after the course, BP before each dose with the 30 mg every 2 hours adjustment, hepatic CYP3A4 elimination with no routine renal dose change, no parenteral injection); criterion `required` with case-specific rationale and evidence, in the stop rule. Leak guard passes. |
| C | major | `prohibited_recommendations`, ICU/TCD musts, BP prohibition | IV nimodipine prohibition wrong as written; SBP target in the ICU must; daily-TCD must; "SBP >160" as a guideline threshold (C4, C5). | FIXED: canonical prohibitions, MUST-ICU, MUST-DCI. |
| D | major | `followup_outputs` literature (PKD screening, contrast premedication) | Literature as clinical steps, empty summaries, patient value "Creatinine 1.4" and a premedication protocol inside literature (C7). | FIXED: both deleted; canonical literature output last; criterion `optional` with canonical text. |
| C | minor | `ground_truth.avoided_actions` `avoid-waste-7-order-advanced-imaging` (MR_angiography) | MRA marked waste in a patient with a contrast allergy, where it is the reasonable alternative (C16). | FIXED: entry deleted. |
| B | major | `followup_outputs` telemetry, `action-8` | Template text with management, 24 h duration (C12). | FIXED: 4 h since arrival, sinus rhythm 74 to 96 bpm, 5 isolated PVCs, no sustained arrhythmia or pauses. |
| B | minor | `initial_tool_outputs.labs` | Magnesium never measured (C9); "Exclusion studies" BNP "Within reference range" with engineering text; type-and-screen engineering sentence; interpretive words in `abnormal_values_summary`. | FIXED: magnesium 2.0 mg/dL added; BNP 72 pg/mL in the Cardiac panel; Exclusion panel deleted; type-and-screen `clinical_significance` null; summary lists values and flags only. Potassium 4.2 was present. |
| B | minor | `ground_truth.red_herrings[0]`, `action-9` expected evidence | Red herring said the echocardiogram shows apical ballooning, and the echo criterion expected Takotsubo, while this echo is normal (LVEF 58%). | FIXED: data point with this case's values; interpretation says the echo shows normal wall motion; echo evidence "LVEF 58% with normal wall motion and normal valves". |
| B | minor | `ground_truth.differential` | Generic key features (C11). | FIXED: canonical key features (basal-cistern blood, saccular right paraclinoid ICA aneurysm). |
| C | minor | `ground_truth.key_clinical_evidence` | 24-72 h, daily-TCD, CT-sensitivity and xanthochromia pearls (C1, plan 1.3). | FIXED: the four canonical pearls; the others kept except the PKD pearl (note aa75afaa). |
| A | minor | `ground_truth.action_criteria[*]`, order, `sequence_constraints`, `stop_rule`, `metadata.difficulty_rationale` | Label-copied rationales, duplicate free-text citations, drug check and literature before the CTA, no constraints, allowance 0; "7-8 required tools" rationale. | FIXED: canonical rationales and citations, case-specific evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD (optional), literature (optional); follow-ups in the same order; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, drug check, `max_additional_actions` 1; difficulty rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

The presentation is unchanged (61-year-old retired nurse with ADPKD, hypertension on nifedipine ER, hypothyroidism, brother dead of SAH and a cousin with an aneurysm, never screened, prior mild contrast rash, BP 178/104). The CT no longer reports kidneys (a head CT does not show them) or clinical notes, and now states no IVH, a normal sella and no hyperdense sinus; the CTA (5.4 x 4.8 mm right paraclinoid ICA aneurysm) no longer names premedication drugs and states normal cervical vessels; labs add magnesium 2.0 and BNP 72. The pathway is NCCT, labs, ECG, CTA, a new diagnostic catheter angiography (ophthalmic artery origin separate from a 3.4 mm neck), the required nifedipine-nimodipine check, echo (normal), 4 hours of telemetry (sinus rhythm, rare PVCs), an optional day-0 baseline TCD (replacing a day-7 vasospasm report) and an optional general literature search last; MRA is no longer marked wasteful. The musts now say: enteral nimodipine with the 30 mg every 2 hours adjustment; secure the right paraclinoid ICA aneurysm as early as feasible, preferably within 24 hours; neurocritical care admission; lower BP now with nicardipine, clevidipine or labetalol; withhold nifedipine ER, continue levothyroxine; do not let the mild contrast rash delay contrast imaging; sodium monitoring; DCI surveillance with euvolemia. The PKD pearl now states the scored lesson: ADPKD with a family history is an indication for screening MRA, and she was never screened.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` (canonical literature output) must be added to the SAH criteria-pack allow-list (plan section 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the git diff (patient block unchanged); the three notes against the file (one MUST-SECURE naming the right paraclinoid ICA aneurysm, DSA criterion and diagnostic output with the ophthalmic origin separate from the neck and no treatment content, day-0 TCD; the PKD pearl replaced with the note's lesson; MUST-BP-A and MUST-HOME withholding nifedipine ER, nimodipine must in MUST-NIMO form); no kidney finding left in the head CT (the only "kidney" strings are the HPI); no premedication drug names in reports; the contrast-rash must and red herring agree with the allergy entry and with the ACR approach to a prior mild allergic-like reaction (do not delay emergency contrast imaging); MRA waste entry removed; creatinine 1.4 gives an eGFR of about 43 (CKD-EPI 2021, woman 61), consistent with the drug check's "moderate renal impairment"; ICD I60.0 fits a carotid siphon aneurysm; DSA arithmetic (5.5 / 3.4 = 1.6); lab flags; drug check `required`, in the stop rule, after the CTA; leak guard passes.
Found: no error. No change made.


## Condition audit (auditor, 24 Oct 2026)

- New follow-up `order_advanced_imaging` (modality `MR_angiography`, trigger `request_mr_angiography`), placed after the DSA follow-up: 3D time-of-flight MRA without gadolinium; saccular right paraclinoid ICA aneurysm 5.3 x 4.7 mm with an irregular dome; no other aneurysm larger than 2 mm; no segmental narrowing. The worker removed the MRA waste entry because MRA is the reasonable alternative with a prior contrast rash, but an MRA order was then answered by the fallback "No abnormality identified", which contradicts the CTA and DSA (confirmed by MockServer simulation). The simulation now serves the new report. No criterion added; MRA stays unscored.
- Checks after the audit: `perfect_agent.py` 30/30 pass; `case_io.py check` schema and synonym guard OK, no test failure names an SAH case; `test_case_guards -k SAH` 60 passed.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- fallback_tool_outputs.mri: SAH-consistent brain MRI instead of the library normal report: an off-pathway brain MRI was answered by the library normal report (no blood on SWI), contradicting the CT; the case fallback now reports the CT's blood on FLAIR and SWI (CENTRAL 10).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
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
