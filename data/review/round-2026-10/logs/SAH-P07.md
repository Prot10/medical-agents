# SAH-P07
Reviewer status: R1 none, R2 no notes and no status in the notes file (plan: probably approved) | Approved before this round: probably (not confirmed, plan section 6 question 6)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The notes file has no note for SAH-P07. All changes below are condition-wide classes (plan sections 2 to 4) or own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | minor | `patient.history_present_illness` | Last sentence was teaching text about LP interpretation in IIH (plan P07). | FIXED: sentence deleted; the rest of the HPI unchanged. |
| D | minor | `initial_tool_outputs.ct` | "This patient has known elevated ICP - LP will require careful interpretation" (C14); "could be missed due to IIH vascular engorgement", "consistent with known IIH" (history cited in the report); em dash in the impression; no statement on intraventricular blood. | FIXED: observations rewritten as imaging features ("can be seen with chronically raised intracranial pressure"), finding descriptions without the history, pertinent negative for IVH; LP avoided action stays `harm` (no hydrocephalus, no IVH). |
| D | major | `initial_tool_outputs.drug_interactions` | Empty `general` block whose summary is the criterion's expected evidence, with the same warning three times (C8; failing leak guard). | FIXED: block deleted; `test_case_guards -k SAH-P07` passes. |
| C | major | `followup_outputs[request_nimodipine_icp_management]` | Invented "Target MAP >90 given estimated ICP 35-42 cmH2O" and CPP > 70 target; no ICP was measured (C5, C10). | FIXED: follow-up deleted. |
| C | minor | `followup_outputs[acetazolamide check]` | "Hold or continue" as the proposed drug, patient lab cited, "prioritize SAH treatment" (case-steering). | FIXED: interaction (none pharmacokinetic) and category-level warnings: metabolic acidosis and hypokalemia, diuretic and natriuretic effect against SAH volume and sodium balance, no parenteral nimodipine. Criterion `recommended` with case-specific label, rationale and evidence. |
| C | major | `required_recommendations` | Nothing addressed the home acetazolamide, whose diuresis and acidosis matter after SAH. | FIXED: must to review acetazolamide for the acute phase with neurology (hold or reduce) while monitoring vision and papilledema. |
| C | major | `followup_outputs[TCD]` | "Day 5 TCD" with moderate right MCA vasospasm 4 hours after onset (C2). | FIXED: baseline post-ictus day 0, normal velocities (right MCA 74, left 70 cm/s, Lindegaard 1.8 and 1.7), canonical protocol and recommendation. |
| C | major | `ground_truth.action_criteria`, `followup_outputs` | No DSA before securing (C3). | FIXED: `dsa-aneurysm-anatomy` (recommended) and a diagnostic DSA report matching the CTA (3.7 x 3.2 mm, irregular dome, neck 2.4 mm, dome-to-neck 1.5, inferior M2 not incorporated, no other aneurysm, no vasospasm). |
| B | minor | `followup_outputs[CTA]` | The dissection entry of the differential relies on a neck CTA, but the CTA report said nothing about the cervical arteries. | FIXED: "Cervical vasculature: No dissection" added to the angiography findings and the impression. |
| C | major | `ground_truth.differential` | "IIH flare" left `moderate` after CT shows blood (C11); CVST key features "MR venography indicated to exclude" (template). | FIXED: IIH flare `low` ("IIH does not produce subarachnoid blood"), RCVS, dissection, CVST and migraine key features cite the case's results. |
| B | minor | `ground_truth.red_herrings[0]` | Template red herring described "T-wave inversions and QTc prolongation" while this ECG has non-specific T-wave changes V2-V3 and QTc 444 ms, and the echo is normal. | FIXED: data point, field path (Cardiac panel) and interpretation match the case. |
| B | minor | `ground_truth.red_herrings` | The case's central trap (IIH anchoring, nurse-line advice) was not recorded; `metadata.difficulty_rationale` states at least three red herrings. | FIXED: red herring added for the IIH-flare advice. |
| B | minor | `initial_tool_outputs.labs` | No potassium, magnesium or PTT (C9); BNP "Within reference range" in "Exclusion studies"; type-and-screen engineering sentence; abnormal summary missing glucose. | FIXED: potassium 3.6 mEq/L, magnesium 2.0 mg/dL, PTT 29 s, BNP 31 pg/mL in Cardiac, type-and-screen significance null, summary and interpretation list the same three abnormal values. |
| B | minor | `followup_outputs[telemetry]` | Template telemetry (C12). | FIXED: 5-hour report, sinus rhythm 72-96 bpm, 3 isolated PVCs, no sustained arrhythmia, no pauses. |
| D | major | `followup_outputs[literature]` | IIH literature with patient-steering content ("Acetazolamide should be assessed ..."); criterion recommended (C7). | FIXED: deleted; canonical literature last; criterion `optional`, last. |
| C | major | musts, prohibitions, pearls | 24-72 h securing musts, daily TCD must, BP target in the ICU must, "never IV" nimodipine, CT 98% and LP 6-12 h pearls (C1, C4, C5). | FIXED: MUST-NIMO, MUST-SECURE right MCA bifurcation, MUST-ICU, MUST-BP-B (132/82), acetazolamide must, sodium must kept, MUST-DCI; canonical prohibitions, IIH prohibition kept; CT, LP, securing and DCI pearls replaced, IIH pearl kept. |
| A | minor | `ground_truth.action_criteria[*]`, `sequence_constraints`, `stop_rule` | Label-copied rationales, unbracketed duplicate citations, no constraints. | FIXED: canonical rationales and citations, order per plan 3.1, constraints NCCT before CTA and CTA before DSA (soft), stop rule = four required criteria, `max_additional_actions` 1. |

## Changes, in one paragraph a physician can read before re-reviewing

A 44-year-old nurse with IIH on acetazolamide and an instantly peaking headache unlike her usual ones. The HPI loses its teaching sentence on LP interpretation; the CT reports a subtle right Sylvian hyperdensity, the IIH imaging features (empty sella, globe flattening) as imaging findings only, and no IVH or hydrocephalus; CTA shows the 3.6 mm right MCA bifurcation aneurysm and now states no cervical dissection; a recommended DSA confirms the anatomy without treatment content. The invented MAP/ICP target step and the leaking initial drug block are gone; the acetazolamide check gives its real effects (acidosis, hypokalemia, natriuresis), and a must asks to review acetazolamide for the acute phase with visual monitoring. The TCD is a normal admission baseline (no day 5 vasospasm). IIH flare is now low in the differential; a red herring records the IIH-flare advice, and the troponin red herring matches this ECG. Musts: nimodipine, securing as early as feasible preferably within 24 hours, ICU, BP monitoring and treatment of rises (132/82), acetazolamide review, sodium, DCI surveillance.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` used in the canonical literature output (plan section 5.1b allow-list request).
- Review UI: initial outputs and follow-ups in criterion order (plan section 5.5).

## Open questions for Andrea (judgment calls you could not settle)

- None. The acetazolamide must leaves hold-versus-reduce to the treating team because no guideline addresses acetazolamide in acute aneurysmal SAH with IIH; the must names the reasons and the monitoring.

## Verification

Adversarial check (24 Oct 2026). Read the log, the diff and the whole final case. No reviewer notes for this case (confirmed in the notes file). Verified in the file: HPI teaching sentence and CT ICP commentary gone; initial drug block and the MAP/ICP follow-up deleted; acetazolamide check content correct (normal anion gap acidosis, hypokalemia, natriuresis), bicarbonate 18 flagged and cited by the acetazolamide must; IIH flare `low`; troponin red herring matches this ECG (QTc 444, T changes V2-V3) and the normal echo; CTA states no cervical dissection; DSA 3.7 x 3.2 mm matches CTA 3.6 x 3.2 mm; MUST-BP-B for 132/82; no IVH or hydrocephalus, LP `harm`; stop rule equals the four required criteria; guards pass.
Nothing found that needed a change. Pre-existing dashes in the ECG interpretation left as they are (not new text).
perfect_agent.py SAH-P07 -v: pass; case_io.py check: clean for SAH-P07.

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
