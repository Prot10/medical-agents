# SAH-P02
Reviewer status: R1 none, R2 approved | Approved before this round: yes

Approved case: every change below corrects a real error (a condition-wide class of plan section 2, or a fact wrong in this file); correct prose was left as it was.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| fb64b259-854d-4d07-9e3b-3329c4e0adde | FIXED | Must added: "Withhold amlodipine while on nimodipine (additive dihydropyridine effect) and monitor blood pressure closely; withhold hydrochlorothiazide during the acute phase (additive hypotension, natriuresis) and resume once stable." (`required_recommendations[6]`; HCTZ follows the condition rule of plan 1.2). Drug check `action-8-check-drug-interactions` raised to `required`, also accepting `drug: amlodipine`. Its output was rewritten as a real interaction report (amlodipine, HCTZ, borrowed ibuprofen) under trigger `request_nimodipine_amlodipine_interaction_check`. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.ct.findings`, `.impression` | Blood placed in the "posterior interhemispheric fissure", which is not part of the perimesencephalic pattern (blood centered anterior to the midbrain and pons, possibly in the ambient cisterns, with no complete anterior interhemispheric or lateral Sylvian filling); "Easy to miss without careful review" is a teaching note. | FIXED: interpeduncular, prepontine and ambient cisterns; the impression states there is no Sylvian, anterior interhemispheric or convexity extension; the teaching observation is removed. |
| C | major | musts | Two 24-72 h securing musts in a case with no aneurysm; nimodipine must conditional on "aneurysmal SAH confirmed", which never happens here; template ICU and TCD musts. | FIXED: no MUST-SECURE. The plan's "manage as aneurysmal SAH until catheter angiography excludes an aneurysm; no securing procedure after a negative DSA with a perimesencephalic pattern" must is added. Nimodipine must starts while an aneurysm is not excluded and leaves completion of the 21 days after a negative DSA to the neurovascular team (plan section 6 question 3). Also MUST-ICU, MUST-BP-B (148/88), the home-drug must, sodium, MUST-DCI, and the repeat vascular imaging must (kept). CTA must reworded "to look for an aneurysm or other vascular lesion". |
| B | minor | DSA follow-up | "Follow-up MRA in 6 months recommended" contradicts the must for repeat vascular imaging at 7 to 14 days; 3D rotational imaging not stated. | FIXED: recommendation aligned with the must; protocol includes 3D rotational angiography of the vertebrobasilar system; normal caliber with no vasospasm added. Criterion relabeled per plan C3 ("... to exclude an aneurysm not shown by CTA"), and its rationale and evidence no longer mention an "endovascular treatment result". |
| C | major | literature follow-ups | "Rebleed risk ... 20-30% in first 24h for aneurysmal SAH" (wrong figure); a second literature step on exertional headache; literature `recommended`. | FIXED: both deleted; criterion `optional`; canonical output last. |
| B | major | TCD | "Day 3 TCD" for a patient seen 2 hours after onset; protocol named MCA only. | FIXED: admission baseline, post-ictus day 0, normal velocities, canonical protocol. |
| C | major | telemetry | Template "neurogenic changes; rare malignant arrhythmias warrant intervention", 24 h. | FIXED: 3 h of sinus rhythm 68 to 94/min with 6 PVCs. |
| C | major | labs | No potassium or magnesium; "Exclusion studies" BNP as text with an engineering sentence. | FIXED: potassium 3.7, magnesium 2.1 added; BNP 22 pg/mL in the Cardiac panel; type and screen `clinical_significance` null; abnormal summary "Glucose 118 mg/dL (H)". |
| C | major | `ground_truth.differential` | Aneurysmal SAH `moderate` and RCVS `moderate` after a negative CTA and a negative six-vessel DSA. | FIXED: both `low` with key features citing the CTA and DSA; dissection and CVST key features cite the CTA and DSA; thunderclap migraine excluded by the CT blood. |
| D | minor | CTA | Dissection not stated for the cervical vessels although the differential relies on it. | FIXED: "Cervical carotid and vertebral arteries: No dissection, stenosis or occlusion". |
| A | minor | criteria | Template rationales and evidence; free-text citations; no constraints; stop rule allowed 0 extra actions. | FIXED: plan 1.3 rationales and case-specific evidence; constraints NCCT before CTA and CTA before DSA (soft); stop rule = the five required criteria, `max_additional_actions` 1. |
| E | minor | `metadata.difficulty_rationale` | Template list of other cases' features. | FIXED: case-specific. |

## Changes, in one paragraph a physician can read before re-reviewing

The CT now puts the subtle blood where a perimesencephalic hemorrhage lies: the interpeduncular, prepontine and ambient cisterns, with no Sylvian or anterior interhemispheric extension. CTA (cervical vessels reported clear) and a six-vessel DSA with 3D rotational imaging are negative. The DSA's recommendation now matches the must for repeat vascular imaging at 7 to 14 days. There is no securing must. Instead the case is managed as aneurysmal until the DSA is negative: nimodipine while an aneurysm is not excluded, with the decision to complete 21 days left to the neurovascular team; neuro-ICU; BP monitoring; withholding amlodipine (note fb64b259) and hydrochlorothiazide; sodium; and DCI surveillance. The amlodipine check is now required. The literature steps, one with a wrong rebleeding figure, are gone, and one optional canonical output remains. TCD is an admission baseline. Labs gain potassium, magnesium and numeric BNP. Aneurysmal SAH and RCVS are now `low` after the negative angiography.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.3): `ground_truth.diagnosis.accepted` for this I60.8 case inherits "aneurysmal subarachnoid hemorrhage", "aneurysmal subarachnoid haemorrhage", "ruptured intracranial aneurysm", "ruptured cerebral aneurysm" and the location codes I60.0 to I60.7, so an answer of aneurysmal rupture scores as correct. Exclude these from I60.8 cases in `diagnosis_synonyms.yaml`. Not hand-edited here (ruling 3).
- `[Molyneux_2002]` in the canonical literature output needs the criteria-pack allow-list (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- Plan section 6 question 3 (nimodipine after a negative DSA): I wrote the must so that nimodipine starts at once and completion of 21 days is a team decision, because a fixed 21-day must would contradict the perimesencephalic diagnosis the case labels. If you prefer the full 21-day course regardless, the must can be restored to MUST-NIMO verbatim.
- Plan section 6 question 2: DSA stays `recommended`. In this case it is the test that excludes an aneurysm after a negative CTA, so `required` is defensible; I did not change the tier pending your answer.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, plan section 4 P02 and the whole final case (approved case).

Checked: note fb64b259 fixed (amlodipine withheld, HCTZ withheld per plan 1.2, check `required` with an amlodipine alternative matching its trigger, real interaction content including the borrowed ibuprofen). No MUST-SECURE; the "manage as aneurysmal until DSA" must and the repeat vascular imaging must agree with the DSA recommendation (7 to 14 days). The CT relocation of blood to the interpeduncular, prepontine and ambient cisterns is a real correction (posterior interhemispheric blood is outside the perimesencephalic pattern). CTA and six-vessel DSA negative; differential lowered accordingly; LP `harm` (no IVH or hydrocephalus). Leak guards pass.

Found and fixed: MUST-BP-B said "until the aneurysm is secured" in a case where no aneurysm exists and none will be secured; changed to "until catheter angiography excludes an aneurysm" (`ground_truth.assessment.required_recommendations[5]`).

Left for Andrea (already in the log): DSA tier and nimodipine duration after a negative DSA (plan section 6 questions 2 and 3). The generic prohibitions still say "before the aneurysm is secured"; they read as "until an aneurysm is excluded" here and were not churned.

Re-ran `perfect_agent.py SAH-P02 -v` (pass) and `case_io.py check` (no failure names the case).

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `action_criteria[action-4-order-advanced-imaging] recommended -> required; stop_rule.required_before_assessment`: with a negative CTA, catheter DSA with 3D rotational angiography is the study that excludes an aneurysm (Connolly 2012, Class I, indicated except when a noninvasive angiogram has shown the aneurysm), and the non-aneurysmal label rests on it (Q2).
- `required_recommendations (nimodipine after a negative DSA)`: nimodipine's benefit is established in aneurysmal SAH; after a negative DSA with a perimesencephalic pattern it can be stopped (Q3).
- fallback_tool_outputs.mri: SAH-consistent brain MRI instead of the library normal report: an off-pathway brain MRI was answered by the library normal report (no blood on SWI), contradicting the CT; the case fallback now reports the CT's blood on FLAIR and SWI (CENTRAL 10).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
- followup_outputs: MR angiography report added before the literature output (aneurysm site and size from the DSA, 0.2 mm smaller as TOF reads it; P02 negative): an MRA order was answered by a fallback reporting no abnormality, contradicting the CTA and DSA (CENTRAL 10). MRA stays a waste action after the CTA.
- `ground_truth.diagnosis` (synonyms re-expanded with `--prune`): diagnosis_synonyms.yaml: the I60 category (generic and aneurysmal labels, I60.9 and the location codes) no longer applies to this case, so an answer of aneurysmal rupture no longer scores; perimesencephalic and non-aneurysmal labels added (CENTRAL 3).
- Checks after the close-out: `perfect_agent.py` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k SAH-` pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'No diagnostic abnormality identified on this study.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
