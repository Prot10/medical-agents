# SAH-M03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 6b4234fb-3474-40f4-9b88-dc24d8d72a36 | FIXED | The literature follow-up `request_migraine_versus_sah_literature` with the misstated Ottawa SAH Rule (four criteria, "age >40") is deleted. The rule's non-applicability is now scored as reasoning: the generic migraine red herring is replaced by data_point "Five-year migraine history and brief confusion" with the interpretation that the Ottawa SAH Rule excludes recurrent similar headaches and new neurological deficits, so it cannot rule out SAH here and the instantaneous onset mandates CT (`ground_truth.red_herrings[1]`). |
| 6a4a8415-c085-4ef0-afd0-8bbe8ca3b099 | FIXED | The reversed statement "LP required if CT negative and presentation <6 hours" was in the same deleted literature follow-up. The canonical LP pearl (LP after a negative CT when presentation is more than 6 h from onset or with a new deficit) replaces the old LP pearl in `ground_truth.key_clinical_evidence`. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status` | "Alert, oriented x4" next to "GCS 14 (E4V4M6 - mild confusion on orientation)" (C13). | FIXED: "Awake but confused: oriented to person and place, not to date; GCS 14 (E4V4M6); photophobic". The exam's "Hunt-Hess Grade 2-3" matches the label and is kept (ruling 3; plan section 6 question 5). |
| C | major | `followup_outputs` DSA | Post-coiling report (Raymond class I, 6-month follow-up DSA): treatment result in a diagnostic tool. | FIXED: diagnostic DSA (3.9 x 3.2 mm irregular right MCA bifurcation aneurysm, daughter sac, neck 2.6 mm, dome-to-neck 1.5, M2 trunks clear, no other aneurysm, no vasospasm); criterion relabelled with canonical rationale and evidence. |
| B | major | `followup_outputs` TCD | "Day 5" TCD with moderate right MCA vasospasm (158 cm/s, Lindegaard 4.1) in a patient 4 h from onset: impossible timeline. | FIXED: day-0 baseline, normal velocities (MCA 78/72 cm/s, Lindegaard 2.2/2.0), canonical text. |
| C | major | drug-check output and criterion | Output checked only sumatriptan while the criterion orders nimodipine; propranolol interaction absent. | FIXED: one check of nimodipine and analgesia against the home list: triptans contraindicated in SAH, sertraline-sumatriptan serotonergic risk, propranolol additive hypotension and no abrupt withdrawal, parenteral-injection and 30 mg every 2 h statements, analgesic alternatives. Trigger renamed `request_nimodipine_sumatriptan_interaction_check` so a nimodipine or a sumatriptan query reaches it. Tier recommended (C10); label, rationale, evidence case-specific. |
| C | major | `ground_truth.assessment` | 24-72 h securing musts (twice), no BP action (SBP 170), no home-drug decision, IV-nimodipine and BP prohibitions misworded, TCD days 4-14 must. | FIXED: MUST-NIMO, MUST-SECURE (right MCA bifurcation), MUST-ICU, MUST-BP-A (default agents), MUST-HOME (no triptan; continue propranolol unless bradycardia or hypotension, no abrupt withdrawal), sodium must kept, MUST-DCI; canonical prohibitions. |
| B | major | `ground_truth.red_herrings[0]` | Template troponin red herring describes T-wave inversions, QTc prolongation and an echo with apical ballooning; this case has T-wave flattening, QTc 468 ms and a normal echo. | FIXED: rewritten to troponin 0.09 with T-wave flattening and borderline QTc; normal echo argues against ACS. |
| D | minor | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Engineering text ("which is what this case's diagnosis rests on") and a non-numeric BNP. | FIXED: panel deleted; BNP 64 pg/mL (<100) in the Cardiac panel; magnesium 2.0 mg/dL added; type and screen significance null. |
| D | minor | `initial_tool_outputs.ct.additional_observations` | "Subtle findings - easy to attribute to artifact" is commentary. | FIXED: removed (impression already says subtle); pertinent negatives (sella, venous sinuses) added. |
| B | major | telemetry output | Template text with management, 24 h duration. | FIXED: 3 h telemetry, sinus 72-96 bpm, 5 PACs, no sustained arrhythmia or pauses (QTc below 480, no QTc line). |
| D | major | literature criterion | Recommended clinical step with case-specific content. | FIXED: optional, last, canonical rationale/evidence/citations; canonical output as the last follow-up. |
| C | minor | `ground_truth.differential[0]` | Generic RCVS key feature; sertraline (SSRI) is a recognized RCVS precipitant in this patient. | FIXED: key feature names sertraline and the CT/CTA findings that point to aneurysmal SAH; low. Other entries canonical. |
| B | minor | `followup_outputs` CTA | No neck-vessel statement. | FIXED: cervical carotid and vertebral arteries patent, no dissection. |
| C | minor | `ground_truth.key_clinical_evidence` | Outdated CT, LP, 24-72 h and TCD pearls. | FIXED: canonical pearls. |
| A | minor | citations, rationales, order, constraints, stop rule, `metadata.difficulty_rationale` | Free-text citations, label-copied rationales, non-diagnostic order, no constraints, allowance 0, rationale mentioned an OSH read this case lacks. | FIXED: bracketed keys; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; NCCT before CTA and CTA before DSA (soft); stop rule required four, allowance 1; rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing
52-year-old woman with migraine, propranolol, sertraline and as-needed sumatriptan; instantaneous headache 4 h before arrival, confused with GCS 14 (the exam no longer says oriented x4), thin Fisher 2 right Sylvian SAH, 3.8 mm irregular right MCA bifurcation aneurysm, SBP 170. The misstated Ottawa and LP literature is deleted; the Ottawa rule's non-applicability (migraine history, confusion) is now a red herring that scores the reasoning. The impossible day-5 vasospasm TCD is a normal day-0 baseline, the DSA no longer reports coiling, and the drug check covers nimodipine against the whole home list (no triptan, sertraline-triptan serotonergic risk, propranolol continued). Musts follow the plan (enteral nimodipine, securing as early as feasible and preferably within 24 h, neurocritical care, IV titratable BP lowering, no triptan and continue propranolol, sodium, DCI surveillance). The troponin red herring now matches this case's normal echo.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- As plan section 5 (allow-list `[Perry_2013]`, `[Molyneux_2002]`).

## Open questions for Andrea (judgment calls you could not settle)
None beyond plan section 6 question 5 (label "Hunt-Hess 2-3"; the exam now describes confusion with GCS 14, which is grade 3).

## Verification
Adversarial check (24 Oct 2026): diff, full final case, perfect-agent `-v`, `case_io.py check`, `test_case_guards -k SAH-M03`.
- Note 6b4234fb: confirmed FIXED (the misstated Ottawa text is gone with its literature follow-up; red herring "Five-year migraine history and brief confusion" carries the plan's interpretation; the confusion is the new deficit that makes the rule inapplicable). Note 6a4a8415: confirmed FIXED (reversed LP statement deleted; canonical LP pearl present).
- Confirmed: mental status now confused with GCS 14, consistent with the HH 2-3 label (left as plan question 5); DSA diagnostic only, 3.9 x 3.2 mm against CTA 3.8 x 3.2 (within 0.3 mm), ratio 3.9/2.6 = 1.5; TCD day 0; telemetry 3 h without a QTc line (QTc 468 < 480); drug check covers nimodipine, triptan contraindication, sertraline-sumatriptan and propranolol, matching MUST-HOME; penicillin allergy has no conflict; troponin red herring matches the normal echo; RCVS key feature (sertraline as precipitant) correct and `low`.
- No error found; no change made.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `ground_truth.diagnosis.accepted[0] (Hunt-Hess 3)`: M03's exam is confused with GCS 14 (E4V4M6), which is grade 3; a label names one grade (Q5).
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
