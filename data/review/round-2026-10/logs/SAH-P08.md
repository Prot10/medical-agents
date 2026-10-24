# SAH-P08
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 61a944ea-e7de-4e6b-8a21-b22c3b998136 | FIXED | `followup_outputs` reordered: CTA (step 1), DSA, antiplatelet check, echo, telemetry, TCD, literature; `ground_truth.action_criteria` in the same order (NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature). The cardiology-first anchoring is now also a red herring (`red_herrings[1]`, EMS aspirin and catheterization). |
| 2b67f747-643d-4df1-afdd-1573bff9b741 | FIXED | MUST-BP-A with "nicardipine or clevidipine infusion" (labetalol omitted for LVEF 30%) (`required_recommendations[5]`); MUST-LVEF "LVEF 30% from stress cardiomyopathy, with moderate mitral regurgitation: involve cardiology and neuroanesthesia before the securing procedure ..." (`required_recommendations[9]`); the BP prohibition is the canonical one. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `required_recommendations`, `key_clinical_evidence[8]` | 24-72 h securing musts (twice) and pearl; no DSA (C1, C3). | FIXED: MUST-SECURE for the AComA aneurysm (as early as feasible, preferably within 24 hours); securing pearl replaced; `dsa-aneurysm-anatomy` (recommended) with a diagnostic DSA report matching the CTA (7.9 x 6.4 mm, multilobulated, neck 3.4 mm, dome-to-neck 2.3, right A2 partly incorporated, dominant right A1, no other aneurysm, no vasospasm). |
| C | major | `followup_outputs[DAPT check].alternatives` | "Consider bridging with GpIIb/IIIa inhibitor" while the aneurysm is unsecured: an intravenous antiplatelet bridge in acute SAH is unsafe. | FIXED: deleted. |
| C | major | `followup_outputs[DAPT check].warnings` | "Platelet transfusion (1-2 pools) may be needed" as routine advice; patient-specific "Patient on dual antiplatelet" wording. | FIXED: platelet transfusion only before a neurosurgical procedure (no benefit without surgery); stent-thrombosis risk statement kept; interaction of nimodipine with metoprolol and lisinopril added; no parenteral nimodipine. |
| C | major | `ground_truth.action_criteria[action-7]`, `required_recommendations` | DAPT check `recommended` with template evidence; no must on the antiplatelets (C10). | FIXED: `required`, alternatives nimodipine, clopidogrel, aspirin (all served by the stored check), case-specific label, rationale and evidence; must: hold aspirin and clopidogrel including the EMS dose, decide with cardiology given the 2-year-old stent, platelets only for EVD or open surgery. Added to the stop rule. |
| C | major | `required_recommendations` | QTc 532 ms with no K/Mg action; magnesium never measured (C9). | FIXED: potassium 3.6 mEq/L and magnesium 1.9 mg/dL added to the BMP; MUST-QT (QTc 532, K 3.6). |
| C | minor | `required_recommendations` | Home metoprolol, lisinopril and atorvastatin not addressed (C5). | FIXED: MUST-HOME: continue metoprolol (post-MI) unless bradycardia or hypotension, withhold lisinopril in the acute phase, continue atorvastatin. |
| C | major | `followup_outputs[TCD]` | Day 5 TCD with bilateral ACA vasospasm in a patient seen within hours of onset (C2). | FIXED: baseline post-ictus day 0, normal velocities (MCA 84 and 80 cm/s, Lindegaard 1.9 and 1.8, ACA 68 and 64 cm/s), canonical protocol and recommendation. |
| C | major | `ground_truth.differential` | Acute coronary syndrome, the mimic the whole case raises (chest pain, troponin 2.8, prior STEMI), missing; template key features. | FIXED: ACS added (low) with the ECG and echo features that favor stress cardiomyopathy; RCVS (exertional trigger), dissection, apoplexy, CVST, migraine with the case's results. |
| B | minor | `patient.neurological_exam.additional` | "Hunt-Hess Grade 2-3" with GCS 15 and no deficit (C13). | FIXED: "Hunt-Hess Grade 2". |
| B | minor | `followup_outputs[CTA]` | "Large saccular aneurysm" for 7.8 mm (C13); no statement on the cervical arteries although the differential relies on it. | FIXED: "Large" dropped; "Cervical vasculature: No dissection" added to findings and impression. |
| B | minor | `followup_outputs[echo]` | "No right heart thrombus" where the apical akinesis raises an LV apical thrombus question; "CLASSIC Takotsubo" in wall motion; LV "severely dilated apex"; em dash in the impression. | FIXED: "No left ventricular apical thrombus"; wall motion "Severe apical akinesis with hyperdynamic basal segments"; LV "Normal cavity size with apical ballooning"; impression rewritten (wall-motion abnormality beyond a single coronary territory), LVEF 30% and MR unchanged. |
| D | minor | `initial_tool_outputs.ecg.findings[0]` | "(strongly suggesting neurogenic pattern)" is a non-cardiac attribution in an ECG report. | FIXED: removed; em dash removed from the interpretation. |
| B | minor | `initial_tool_outputs.ct` | No statement on intraventricular blood. | FIXED: "No intraventricular hemorrhage" added; LP avoided action stays `harm`. |
| B | minor | `initial_tool_outputs.labs` | Abnormal summary with interpretive words ("leukocytosis", "stress hyperglycemia"); type-and-screen engineering sentence (C14). | FIXED: factual summary matching the interpretation; type-and-screen significance null. |
| B | minor | `followup_outputs[telemetry]` | Template telemetry (C12). | FIXED: 3-hour report, sinus tachycardia 96-122 bpm, 34 PVCs with 2 couplets, no sustained arrhythmia, no pauses, QTc 532 ms, no torsades. |
| D | major | `followup_outputs[literature]` | Neurogenic-STEMI literature (patient-steering); criterion recommended (C7). | FIXED: deleted (the troponin red herring carries the lesson); canonical literature last; criterion `optional`, last. |
| B | minor | `ground_truth.red_herrings[0]` | Template wording ("QTc prolongation" generic) not tied to this case's values. | FIXED: troponin 2.8, BNP 486, T-wave inversions V1-V5, prior STEMI; interpretation cites the echo pattern. |
| C | major | musts, prohibitions, pearls | Daily TCD must, "never IV" nimodipine, BP target in the ICU must, CT 98% and LP 6-12 h pearls (C4, C5). | FIXED: MUST-NIMO, MUST-ICU, MUST-DCI, sodium must kept; canonical prohibitions (cardiac catheterization prohibition kept); CT, LP and DCI pearls replaced. |
| A | minor | `ground_truth.action_criteria[*]`, `sequence_constraints`, `stop_rule` | Label-copied rationales, unbracketed citations, no constraints, `max_additional_actions` 0. | FIXED: canonical rationales and citations; constraints NCCT before CTA and CTA before DSA (soft); stop rule = five required criteria, `max_additional_actions` 1. |

## Changes, in one paragraph a physician can read before re-reviewing

A 58-year-old man with a coronary stent on aspirin and clopidogrel, given an extra 325 mg aspirin by EMS for presumed STEMI, with thunderclap headache, neck stiffness, Fisher 3 SAH and a 7.8 mm AComA aneurysm. The pathway now starts with the brain: NCCT, labs, ECG, CTA, a recommended catheter DSA (diagnostic only), then the required antiplatelet check, echo (LVEF 30%, apical ballooning, moderate MR, no apical thrombus), telemetry (3 hours, frequent PVCs, QTc 532, no torsades), a normal admission TCD and the canonical literature search last. The antiplatelet check no longer proposes a GP IIb/IIIa bridge and limits platelet transfusion to a neurosurgical procedure. Musts: secure the AComA aneurysm as early as feasible, preferably within 24 hours; nimodipine; ICU; lower BP now with nicardipine or clevidipine (206/122, LVEF 30%); continue metoprolol, withhold lisinopril, continue atorvastatin; hold both antiplatelets with cardiology input; correct potassium and magnesium for QTc 532 with monitoring; cardiology and neuroanesthesia before securing for LVEF 30% with moderate MR; sodium; DCI surveillance. ACS is now in the differential (low), Hunt-Hess is 2, and a second red herring records the cardiology-first anchoring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan section 1.1: `[Drew_2010]` (MUST-QT) and `[Molyneux_2002]` (canonical literature) need the allow-list additions of plan section 5.1b.
- Review UI: initial outputs and follow-ups in criterion order (plan section 5.5).

## Open questions for Andrea (judgment calls you could not settle)

- The HPI keeps the prehospital ECG ("deep T-wave inversions V1-V4"), which is a result from before the encounter while the case scores an ED ECG. I kept it because it is a different study (field ECG) and the STEMI anchoring is the point of the case. No input needed unless you rule otherwise.

## Verification

Adversarial check (24 Oct 2026). Read the log, the diff and the whole final case. Both note ids present and verified FIXED: CTA is follow-up 1 and criterion 4, the echo comes after the drug check; MUST-BP-A names nicardipine or clevidipine only (LVEF 30%); MUST-LVEF names the moderate MR. Also verified: MUST-QT with K 3.6 and Mg 1.9 matching the BMP; DAPT must and check agree (no GP IIb/IIIa bridge; platelets only for EVD or surgery); metoprolol continued as post-MI therapy; ACS in the differential with the case's ECG and echo; Hunt-Hess 2 with GCS 15; "Large" gone; DSA 7.9 x 6.4 mm vs CTA 7.8 x 6.4 mm; the single drug follow-up is served for any drug alternative (no initial drug output); guards pass.
Found and fixed: the troponin was labelled "Troponin I (high sensitivity)" with a conventional-assay unit and cut-off (ng/mL, <0.04); high-sensitivity assays report ng/L. Renamed to "Troponin I" in the Cardiac panel, `abnormal_values_summary` and `interpretation` (value and range unchanged).
Open question in the log (field ECG kept in the HPI): agree; it is a different study from the scored ED ECG and carries the STEMI anchoring.
perfect_agent.py SAH-P08 -v: pass; case_io.py check: clean for SAH-P08.

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
