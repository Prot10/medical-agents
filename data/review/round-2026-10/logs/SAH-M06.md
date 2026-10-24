# SAH-M06
Reviewer status: R1 none, R2 approved | Approved before this round: yes

Approved case: every change below corrects a real error (plan classes C1 to C14, or a contradiction inside the case).

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| c621cf95-92ee-4525-ae03-02202d225c9c | DECLINED (facts) / FIXED (class) | The note repeats the SAH-M05 facts, which are not in this case: here QTc is 478 ms (`initial_tool_outputs.ecg.intervals.QTc`), potassium 3.7 mEq/L (`labs.panels.BMP`), there is no furosemide (medications: ethinyl estradiol/norgestimate, ibuprofen as needed) and no U waves on the ECG; QTc below 500 ms with normal potassium needs no QT must (plan C9). The class part (magnesium never measured) is fixed: magnesium 2.1 mg/dL (1.7-2.2) added to the BMP panel. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations` | EVD must "given acute hydrocephalus" while the CT reports no hydrocephalus (template carry-over, C6); two 24-72 h securing musts; no BP must (SBP 188); TCD days 4-14 must; no contraceptive decision. | FIXED: EVD must removed; MUST-NIMO, MUST-SECURE (AComA), MUST-ICU, MUST-BP-A (default agents), "Stop the combined oral contraceptive and arrange non-estrogen contraception.", sodium kept, MUST-DCI. Prohibitions: canonical nimodipine and BP texts; the NSAID prohibition covers home ibuprofen. |
| C | major | drug-check output and criterion | The output checked only the OCP ("patient requesting to continue") while the criterion orders nimodipine; "Thrombotic complications can occur post-SAH coiling with OCP use" is unsupported. | FIXED: one check against the home list: combined estrogen contraception unacceptable with SBP 160 or more or DBP 100 or more (CDC/WHO MEC category 4) and inadvisable in smokers 35 or older, VTE risk; ibuprofen NSAID to avoid; no nimodipine-OCP interaction; parenteral and 30 mg every 2 h statements; progestin-only or copper IUD as alternatives. Trigger renamed `request_nimodipine_ocp_interaction_check`. Tier recommended (C10); label, rationale, evidence case-specific. |
| B | major | `ground_truth.red_herrings[0]` | Template says the echo shows apical ballooning; this case's echo is normal (LVEF 56%, no wall-motion abnormality). | FIXED: rewritten to troponin 0.11 with T-wave inversions and QTc 478; normal echo argues against ACS. |
| B | major | `followup_outputs` TCD | "Day 5" TCD with ACA vasospasm in a patient 2 h from onset. | FIXED: day-0 baseline, normal velocities, canonical text. |
| C | major | `ground_truth.action_criteria` | No DSA before securing (C3). | FIXED: `dsa-aneurysm-anatomy` recommended; follow-up (5.9 x 4.6 mm lobulated AComA aneurysm, neck 2.9 mm, dome-to-neck 2.0, left A1 dominant, A2 origins clear, no other aneurysm, no vasospasm); CTA before DSA (soft). |
| D | minor | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Engineering sentence and non-numeric BNP. | FIXED: panel deleted; BNP 58 pg/mL in Cardiac; type and screen significance null. |
| D | major | literature follow-up `request_ocp_sah_risk_literature`, criterion | Patient-directed advice inside literature; recommended literature step. | FIXED: deleted (the OCP content is now a must); canonical literature last; criterion optional. |
| B | major | telemetry output | Template text, 24 h. | FIXED: 3 h, sinus tachycardia 96-120 bpm, 4 PVCs, no sustained arrhythmia or pauses. |
| B | minor | CTA, CT observations, differential, pearls | Neck vessels not reported; generic differential; outdated pearls. | FIXED: neck-vessel statement; sella and venous-sinus negatives; canonical differential; canonical pearls. |
| A | minor | citations, rationales, order, constraints, stop rule, metadata | Template items (section 3); stale CSF concern; rationale described an OSH read and CSF this case lacks. | FIXED: bracketed keys; canonical rationales and case evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; NCCT before CTA and CTA before DSA (soft); stop rule four required, allowance 1; concerns emptied; rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing
43-year-old smoker on a combined oral contraceptive, thunderclap headache 2 h before arrival, HH2, Fisher 3 SAH without hydrocephalus, 5.8 mm lobulated AComA aneurysm, BP 188/112. The carried-over EVD must is removed (no hydrocephalus). The day-5 vasospasm TCD is a normal day-0 baseline; a diagnostic DSA is added; the drug check now covers nimodipine against her real list and states why the combined contraceptive must stop (severe hypertension, smoker over 35) and why ibuprofen is avoided. Musts follow the plan, with a new must to stop the combined contraceptive and arrange non-estrogen contraception. Magnesium is now measured (2.1); the reviewer's QTc note described SAH-M05 and does not apply here (QTc 478, K 3.7, no diuretic). The troponin red herring now matches this case's normal echo.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- As plan section 5 (allow-list `[Molyneux_2002]`).
- Note c621cf95 is a copy of the SAH-M05 note filed on SAH-M06; the review app may want to flag duplicated comment text across cases.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial check (24 Oct 2026), approved case: diff, full final case, perfect-agent `-v`, `case_io.py check`, `test_case_guards -k SAH-M06`.
- Note c621cf95: DECLINED (facts) is sound: the file has QTc 478 ms, K 3.7, no furosemide, no U waves; class part FIXED (magnesium 2.1 mg/dL in BMP).
- Confirmed each change corrects a real error: EVD must removed (CT: no hydrocephalus); LP `harm` (no IVH or hydrocephalus); TCD day 0; DSA 5.9 x 4.6 mm vs CTA 5.8 x 4.6 mm, ratio 5.9/2.9 = 2.0; troponin red herring matches the normal echo (LVEF 56%); contraceptive must supported by the drug check (CDC/WHO MEC category 4 for SBP 160+ or DBP 100+, category 3 for a smoker 35+ under 15 cigarettes a day); MUST-BP-A fits 188/112.
- Found and FIXED: the drug-check criterion's `expected_evidence` called the combined contraceptive "contraindicated with ... smoking over 35", which overstates MEC category 3: now "Combined estrogen contraception contraindicated with BP 188/112 (and inadvisable in a smoker over 35); ibuprofen to be avoided before securing".
- Both checks clean after the edit.

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
