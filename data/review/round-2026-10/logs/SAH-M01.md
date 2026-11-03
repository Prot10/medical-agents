# SAH-M01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 38447471-76b4-4877-990d-e5988eca2fb6 | FIXED | Both "within 24-72 hours" securing musts replaced by one MUST-SECURE (left MCA bifurcation, "as early as feasible, preferably within 24 hours of onset [Hoh_2023]") in `ground_truth.assessment.required_recommendations`; the 24-72 h pearl replaced by the canonical securing pearl in `ground_truth.key_clinical_evidence`. The pathway now ends before securing: the DSA is a diagnostic pre-securing study, the TCD is an admission baseline (day 0), no step is dated after the bleed. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` DSA (`request_digital_subtraction_angiography`) | DSA reported endovascular coiling, Raymond class I occlusion and 6-month follow-up: a treatment result inside a diagnostic tool (ruling 4, plan C3). | FIXED: diagnostic report only, anatomy as CTA (4.8 x 4.2 mm, lobulated, daughter sac, neck 3.1 mm, dome-to-neck 1.5), superior M2 origin at the neck, no additional aneurysm, no vasospasm. Criterion `action-4-order-advanced-imaging` relabelled (DSA_LABEL), rationale and evidence per plan 1.3; kept recommended. |
| C | major | drug-check output | "Hold antihypertensives during triple-H therapy" (triple-H not recommended, Hoh 2023); "hold if SBP <100" (guideline divides the dose rather than stopping); "crush and inject IV" wording. Home ibuprofen and the outside ketorolac (NSAIDs) not mentioned. | FIXED: lisinopril additive hypotension, NSAID antiplatelet interaction, parenteral-injection warning, 30 mg every 2 h for hypotension, CYP3A4 note. Criterion rationale and evidence case-specific; tier recommended (C10). |
| C | major | `ground_truth.assessment` | No BP action (SBP 164), nimodipine must without the hypotension rule, ICU must with an inline SBP target, TCD days 4-14 must, IV-nimodipine and BP prohibitions misworded. | FIXED: MUST-NIMO, MUST-ICU, MUST-BP-A (default agents), MUST-HOME "Withhold lisinopril during the acute phase and resume it once stable", MUST-DCI; prohibitions 4 and 7 replaced with the canonical texts. NCCT, CTA and sodium musts kept. |
| B | major | `followup_outputs` TCD | "Day 1" TCD with daily-TCD advice and "peak vasospasm risk days 4-14" in `quantitative_data`; vessel labelled "ipsilateral to aneurysm" (cross-modality). Patient is 8 h from onset. | FIXED: admission baseline, `post_ictus_day` 0, canonical impression, protocol and recommendation, PCA and right Lindegaard added, all normal. |
| B | major | `followup_outputs` telemetry and criterion evidence | Template telemetry text with management words and an impossible 24 h duration. | FIXED: 4 h telemetry, sinus 76-112 bpm, 14 isolated PVCs, no sustained arrhythmia or pauses, QTc 498 ms without torsades; evidence updated. |
| D | major | `initial_tool_outputs.literature_search`, criterion `action-7-search-medical-literature` | Initial literature block repeated the criterion's expected evidence (scoring-key leak); literature was recommended. | FIXED: block deleted; canonical literature follow-up added last; criterion optional, last, rationale/evidence/citations per plan. |
| A | minor | criteria `citations` | Free-text duplicates ("AHA/ASA ... 2023", "Hoh_2023", "Connolly_2012"). | FIXED: bracketed keys only; ECG, echo, telemetry cite [Hoh_2023]. |
| B | minor | `ground_truth.action_criteria`, `followup_outputs` order | Criteria and follow-ups not in diagnostic order. | FIXED: criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; follow-ups CTA, DSA, drug check, echo, telemetry, TCD, literature. Ids unchanged. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | No constraints; stop rule allowance 0. | FIXED: NCCT before CTA (soft), CTA before DSA (soft); `max_additional_actions` 1, required list unchanged (NCCT, labs, ECG, CTA). |
| E | minor | criteria `rationale` | Rationales copied from labels. | FIXED: canonical rationales; case-specific expected evidence for NCCT, labs, ECG, CTA, DSA, echo, telemetry. |
| C | minor | `initial_tool_outputs.labs` | Magnesium never measured (class C9); type-and-screen `clinical_significance` engineering sentence. | FIXED: magnesium 2.1 mg/dL (1.7-2.2) in BMP; type and screen significance null. |
| B | minor | `ground_truth.red_herrings` | Migraine/fibromyalgia red herring with no migraine in the case (carry-over, C11); OSH red herring advised LP although the repeat CT is positive. | FIXED: migraine entry removed; OSH entry's interpretation now states the repeat NCCT shows the blood, so LP is unnecessary. |
| B | minor | `initial_tool_outputs.ct.additional_observations` | "Initial read by OSH radiologist" vs HPI "read as negative by the emergency physician". | FIXED: "Comparison: outside-hospital CT ... reportedly read as negative; images not available"; added pertinent negatives (sella unremarkable, no hyperdense venous sinus) that the differential cites. |
| B | minor | `followup_outputs` CTA | Differential cites a neck CTA with no neck finding. | FIXED: `angiography_findings` "Cervical carotid and vertebral arteries: Patent; no dissection or stenosis". |
| C | minor | `ground_truth.differential` | Generic key features (pituitary MRI, CT venogram). | FIXED: canonical C11 key features citing this case's CT and CTA; likelihoods unchanged (low, very_low). |
| D | minor | `initial_tool_outputs.ecg.findings[0]` | "(neurogenic T-waves)" attributes a non-cardiac cause inside the ECG report. | FIXED: "Deep symmetric T-wave inversions in leads V1-V5". |
| C | minor | `ground_truth.key_clinical_evidence` | CT-sensitivity, LP, 24-72 h and TCD pearls outdated. | FIXED: the four canonical pearls; the other seven kept. |
| A | minor | `metadata.case_body_concerns`, `difficulty_rationale` | Stale TCD-tool concern; rationale lists CSF/LP as required. | FIXED: concerns emptied; rationale states the actual required work-up. |

## Changes, in one paragraph a physician can read before re-reviewing
The case keeps its presentation (45-year-old man, thunderclap headache 8 h earlier, outside CT read negative, HH2, thin Fisher 2 left Sylvian SAH, 4.8 mm lobulated left MCA bifurcation aneurysm). The pathway is now the first hours of the encounter in diagnostic order: NCCT, labs (magnesium added), ECG, CTA (neck vessels now reported), a diagnostic DSA without any treatment result, the nimodipine check (lisinopril hypotension, NSAID antiplatelet effect, no triple-H), echo, a 4-hour telemetry report, a day-0 baseline TCD and the canonical literature output last (optional). Management musts follow the plan: enteral nimodipine with the 30 mg every 2 h rule, securing as early as feasible and preferably within 24 h, neurocritical care, IV titratable BP lowering for SBP 164, withhold lisinopril, sodium monitoring, DCI surveillance with TCD as an adjunct. The migraine red herring (no migraine in this patient) is removed and the outside-read red herring no longer suggests LP.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- As plan section 5: `[Molyneux_2002]` (canonical literature output) and `[Drew_2010]` to the SAH criteria-pack allow-list.
- `fallback_tool_outputs.cardiac_monitoring` is a "Normal 24-hour Holter" (holter_24h); a 24 h recording cannot exist at assessment time, but it is the generic off-pathway fallback and only answers a Holter order. Left unchanged; flag for a library-level decision.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial check (24 Oct 2026) of the log against the file: diff, full final case, perfect-agent `-v`, `case_io.py check`, `test_case_guards -k SAH-M01`.
- Note 38447471: confirmed FIXED; no "24-72" or "24-48" text remains anywhere; one MUST-SECURE; canonical securing pearl.
- Confirmed: DSA output is diagnostic only (no coiling or Raymond class), anatomy matches the CTA (4.8 x 4.2 mm, neck 3.1 mm, dome-to-neck 4.8/3.1 = 1.5); TCD day 0 normal; telemetry 4 h; literature canonical, optional, last; no initial literature block; drug check has real content (lisinopril, NSAIDs) and does not echo the expected evidence; criteria and follow-ups in diagnostic order; constraints and stop rule as plan; MUST-BP-A fits SBP 164; LP `harm` is right (no IVH or hydrocephalus); differential and red herrings match the CT and CTA.
- Found and FIXED: `initial_tool_outputs.ecg` called a rate of 98 "Sinus tachycardia" (pre-existing; vitals HR 94): rhythm and interpretation now "Sinus rhythm, rate 98"; ECG criterion evidence "Sinus rhythm 98 bpm with deep T-wave inversions ...".
- Found and FIXED: HPI "He has not had a neurological examination or brain imaging previously" contradicted the outside CT done today: now "before today".
- Both checks clean after the edits.

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

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-3-interpret-labs]`.alternatives: was [CBC, BMP, coagulation]; now [CBC, BMP, coagulation, troponin, BNP] | [CBC, BMP, coagulation].
- Decision: serve: new first alternative (old order kept as an alternative). Neurogenic troponin elevation is the case's cardiac red herring (prohibition, key evidence, red herring); baseline troponin belongs with the admission bloods in aSAH (AHA/ASA 2023), and the cardiac panel holds the BNP the evidence reads. CBC + BMP + coagulation did not return it.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that this case contradicts now have a case report. Contradiction = the history, the diagnosis or a stored finding makes the normal report impossible.

- `analyze_csf (lumbar puncture, EVD, lumbar drain; xanthochromia)` -> fallback_tool_outputs.csf: blood-stained CSF without clearing (Fisher 2), xanthochromia result per time from onset. The library returned clear acellular CSF in a patient with subarachnoid blood on CT.
- `perform_clinical_assessment {assessment_type: performance_status}` -> fallback_tool_outputs.clinical_assessment: Karnofsky 40, ECOG 3. The library returned Karnofsky 100, ECOG 0, working, in an acutely ill inpatient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}` -> followup_outputs[request_gait_and_balance_timed]: assessment not completed, patient unable to stand safely; the library returned a normal Timed Up and Go in a patient whose gait the exam could not test or found abnormal.
- `order_echocardiogram {echo_type: TEE}` -> fallback_tool_outputs.echo: stored TTE wall motion and LVEF 52% carried over; no thrombus or shunt. The library TEE was normal against an abnormal stored TTE.
- `order_echocardiogram {echo_type: bubble_study}` -> followup_outputs[request_bubble_study]: same wall motion and LVEF, no right-to-left shunt at rest. The library bubble study called the echocardiogram normal.
- `order_advanced_imaging {modality: cardiac_MRI}` -> fallback_tool_outputs.advanced_imaging: wall motion and LVEF as on the stored TTE, oedema in the dysfunctional segments, no late enhancement. The library cardiac MRI reported no structural heart disease.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}` -> followup_outputs[request_structured_headache_history_ichd3]: instantaneous while driving, 8 hours before assessment; red flags: thunderclap onset. The library reported no thunderclap onset, no red flags and no nausea or photophobia, against the history.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}` -> followup_outputs[request_orthostatic_blood_pressure]: standing not attempted, supine BP 164/98 as at arrival. The library reported 3 minutes of symptom-free standing at BP 128/78.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}` -> followup_outputs[request_levodopa_challenge]: no parkinsonian signs, challenge not performed. The library reported normal gait and postural reflexes and no nausea in a patient who cannot stand and is vomiting.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k SAH-M01` passed; no criterion answer changed (snapshot diff); every mapped order is answered without the library (`verify.py`).
