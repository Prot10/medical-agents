# SAH-M02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| bf848453-6712-4272-b24f-d61bb56634ed | FIXED | The "Day 4" TCD (MCA 142/128 cm/s, "mild vasospasm", "worsening headache and mild confusion") was re-dated to an admission baseline: `post_ictus_day` 0 (onset 6 h before arrival), normal velocities (MCA 82/76 cm/s, Lindegaard 2.3/2.1), clinical note removed, canonical impression, protocol and recommendation (`followup_outputs[5]`). `followup_outputs` reordered CTA, DSA (new), nimodipine check, echo, telemetry, TCD, literature, so nimodipine is checked right after the CTA; the nimodipine check is now `required` and in the stop rule. Every result now belongs to the first hours of the encounter. |
| 9bd81d95-96fb-47eb-a556-556933c74f71 | FIXED | Red herring "Past history of migraines, chronic headaches, or fibromyalgia" removed from `ground_truth.red_herrings` (the patient has no headache history). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations` | Two 24-72 h securing musts; no BP action (SBP 178); no action for QTc 512 ms; amlodipine with nimodipine handled only inside the drug check; EVD must worded generically; TCD days 4-14 must. | FIXED: MUST-NIMO, one MUST-SECURE (AComA), MUST-ICU, MUST-EVD-NOW "with intraventricular blood", MUST-BP-A (default agents; LVEF 45%, no bradycardia), MUST-HOME (withhold amlodipine and hydrochlorothiazide), MUST-QT (512 ms, K 3.6), sodium must kept, MUST-DCI. NCCT and CTA musts kept. |
| C | major | `ground_truth.action_criteria` | No catheter angiography before securing (plan C3). | FIXED: new recommended criterion `dsa-aneurysm-anatomy` and follow-up `request_digital_subtraction_angiography` (bilobed AComA 5.2 x 4.8 mm, neck 2.8 mm, dome-to-neck 1.9, right A1 dominant, A2 origins clear, no other aneurysm, no vasospasm); soft constraint CTA before DSA. |
| C | major | drug-check output | "Never crush capsules for IV use", "hold if SBP <100", HCTZ not addressed. | FIXED: amlodipine duplicate dihydropyridine (withhold), HCTZ hypotension/natriuresis/K and Mg loss, parenteral-injection warning, 30 mg every 2 h rule, codeine intolerance noted for analgesia. Tier required (C10); case-specific rationale and evidence. |
| C | major | literature follow-up (`request_literature_search_sah_vasospasm`) | "Triple-H therapy for symptomatic vasospasm" attributed to AHA/ASA 2023 (wrong; prophylactic hypervolemia is not recommended); literature criterion recommended. | FIXED: follow-up deleted; canonical literature output last; criterion optional, last, canonical rationale, evidence, citations. |
| C | major | `ground_truth.avoided_actions` `avoid-harm-1-analyze-csf` | Severity `harm` although the CT shows IVH and hydrocephalus. | FIXED: `contraindicated`, rationale cites the IVH and hydrocephalus. |
| B | major | telemetry output and evidence | Template text with management words, 24 h duration. | FIXED: 4 h telemetry, sinus tachycardia settling (88-118 bpm), 9 isolated PVCs, no sustained arrhythmia or pauses, QTc 512 ms without torsades. |
| C | minor | `initial_tool_outputs.labs` | No magnesium (C9); type-and-screen engineering sentence. | FIXED: magnesium 1.9 mg/dL (low-normal, thiazide); significance null. |
| B | minor | `initial_tool_outputs.ct.findings[2].location` | "Third and fourth ventricles" while the description and impression report third-ventricle blood only. | FIXED: "Third ventricle". Pertinent negatives (sella, venous sinuses) added to observations for the differential. |
| D | minor | `initial_tool_outputs.ecg.findings[1]` | "- risk of Torsades de Pointes" is commentary inside the finding list. | FIXED: "QTc prolongation to 512 ms". |
| B | minor | `followup_outputs` CTA | Neck vessels not reported though the differential relies on them. | FIXED: "Cervical carotid and vertebral arteries: Patent; no dissection or stenosis". |
| C | minor | `ground_truth.differential` | Generic key features. | FIXED: canonical C11 entries citing basal-cistern blood and the AComA aneurysm; likelihoods unchanged. |
| C | minor | `ground_truth.key_clinical_evidence` | Outdated CT, LP, 24-72 h and TCD pearls. | FIXED: canonical pearls; seven others kept. |
| A | minor | criteria citations, rationales, order; constraints; stop rule | Free-text citations, label-copied rationales, non-diagnostic order, no constraints, allowance 0. | FIXED: bracketed keys only; canonical rationales and case-specific evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; NCCT before CTA and CTA before DSA (soft); stop rule = the five required criteria, allowance 1. |
| A | minor | `metadata.case_body_concerns`, `difficulty_rationale` | Stale CSF concern; rationale described anticoagulation and three red herrings (carry-over). | FIXED: concerns emptied; rationale describes this case. |
| C | minor | `ground_truth.diagnosis.accepted[0]` "Fisher 3" | CT shows thick cisternal blood plus a small third-ventricle layer. On the original Fisher scale grade 4 is intracerebral or intraventricular clot with diffuse or no SAH, so thick cisternal clot with a small IVH layer is reasonably grade 3 (it would be grade 4 on the modified Fisher scale). | No change (label kept per ruling 3). |

## Changes, in one paragraph a physician can read before re-reviewing
48-year-old woman, thunderclap headache 6 h before arrival, HH2, Fisher 3 SAH with third-ventricle blood and mild early hydrocephalus, 5.2 mm bilobed AComA aneurysm, SBP 178, QTc 512 ms, on amlodipine and hydrochlorothiazide. The impossible day-4 TCD is now a normal day-0 baseline, and the pathway runs in the first hours: NCCT, labs (magnesium 1.9 added), ECG, CTA, a new diagnostic DSA, the nimodipine check (now required: amlodipine duplicates nimodipine, HCTZ adds hypotension and K loss), echo, 4-hour telemetry, TCD, literature last (optional, canonical). Musts now cover enteral nimodipine, securing as early as feasible and preferably within 24 h, neurocritical care, EVD for hydrocephalus with intraventricular blood, IV titratable BP lowering, withholding amlodipine and HCTZ, potassium and magnesium repletion with QT precautions, sodium and DCI surveillance. LP is now `contraindicated`. The carried-over migraine red herring is gone; the triple-H literature output is deleted.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- As plan section 5 (allow-list `[Molyneux_2002]`, `[Drew_2010]`).

## Open questions for Andrea (judgment calls you could not settle)
- EVD with GCS 15 (plan section 6, question 1): the plan's condition rule gives MUST-EVD-NOW for hydrocephalus with intraventricular blood, applied here for consistency across the 30 cases. Hoh 2023 recommends urgent CSF diversion for acute symptomatic hydrocephalus; this patient is GCS 15 with mild temporal-horn dilatation, so many centres would instead watch closely (MUST-EVD-WATCH) and drain on any decline. If you answer the plan's question against EVD, switch the must here to MUST-EVD-WATCH.

## Verification
Adversarial check (24 Oct 2026): diff, full final case, perfect-agent `-v`, `case_io.py check`, `test_case_guards -k SAH-M02`.
- Note bf848453: confirmed FIXED (TCD post-ictus day 0, normal velocities, no clinical note; drug check is follow-up 3 right after CTA and DSA, required and in the stop rule). Note 9bd81d95: confirmed FIXED (migraine red herring gone; no migraine anywhere in the patient block).
- Confirmed: MUST-EVD-NOW matches the CT (third-ventricle blood, temporal-horn dilatation); LP `contraindicated`; MUST-QT matches QTc 512 and K 3.6; MUST-HOME names amlodipine and HCTZ; MUST-BP-A agents fit LVEF 45% and HR 102; DSA matches CTA (5.2 x 4.8 mm, neck 2.8, ratio 1.9); codeine intolerance handled in the drug check; no output repeats an expected evidence. The worker's Fisher 3 reasoning (thick cisternal clot with a small third-ventricle layer) is acceptable on the original scale and the label is unchanged per ruling 3. The EVD with GCS 15 question stays open as logged (plan section 6 question 1).
- Found and FIXED: `initial_tool_outputs.ct.findings[0].location` "Basal cisterns (suprasellar, prepontine)" disagreed with its own description (suprasellar cistern, interpeduncular fossa): now "Basal cisterns (suprasellar, interpeduncular)".
- Both checks clean after the edit.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `required_recommendations (EVD-NOW -> EVD-WATCH)`: the patient is alert (GCS 15); Hoh 2023 recommends urgent CSF diversion for symptomatic hydrocephalus, so the must is urgent neurosurgical review with hourly checks, repeat CT on decline and EVD if it becomes symptomatic (Q1).
- `metadata.difficulty_rationale`: the patient is alert (GCS 15); Hoh 2023 recommends urgent CSF diversion for symptomatic hydrocephalus, so the must is urgent neurosurgical review with hourly checks, repeat CT on decline and EVD if it becomes symptomatic (Q1).
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

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-3-interpret-labs]`.alternatives: was [CBC, BMP, coagulation]; now [CBC, BMP, coagulation, troponin, BNP] | [CBC, BMP, coagulation].
- Decision: serve: new first alternative (old order kept as an alternative). Neurogenic troponin elevation is the case's cardiac red herring (prohibition, key evidence, red herring); baseline troponin belongs with the admission bloods in aSAH (AHA/ASA 2023), and the cardiac panel holds the BNP the evidence reads. CBC + BMP + coagulation did not return it.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.
