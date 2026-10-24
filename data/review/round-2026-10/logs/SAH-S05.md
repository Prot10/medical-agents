# SAH-S05
Reviewer status: R1 none, R2 none (no notes and no status in the notes file; the plan treats it as one of R2's 21 approvals) | Approved before this round: probably yes (unconfirmed, plan section 6 question 6)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for SAH-S05. The condition-wide classes of the plan (C1 to C5, C7 to C12, C14) and the S05 entry of plan section 4 were applied because they are real errors in this case too. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations` | Two duplicate securing musts with a "24-72 hours" window that no guideline gives (C1); nothing secures the ruptured AComA aneurysm. | FIXED: one MUST-SECURE (AComA, as early as feasible, preferably within 24 hours, [Hoh_2023]) plus the plan's S05 must "Secure the ruptured AComA aneurysm first; the small incidental right ICA aneurysm is managed separately (surveillance or elective treatment) after recovery." |
| C | major | `ground_truth.action_criteria`, `followup_outputs` | No catheter angiography before securing (C3). | FIXED: recommended criterion `dsa-aneurysm-anatomy` and a diagnostic DSA follow-up `request_digital_subtraction_angiography`: AComA 4.8 x 4.3 mm (CTA 4.6 x 4.2) with the irregular bleb, neck 2.3 mm, dome-to-neck 2.1, left A1 dominant, A2 origins clear of the neck; the right ICA ophthalmic-segment aneurysm 2.9 x 2.6 mm (CTA 2.8), smooth; no other aneurysm; no vasospasm; no treatment content. Soft constraint CTA before DSA. |
| B | major | `followup_outputs` TCD | TCD dated "day 6" with moderate ACA vasospasm in a patient seen one hour after the ictus and never secured (C2). | FIXED: admission baseline, `quantitative_data` {post_ictus_day: 0}, normal velocities (MCA 60 to 64 cm/s, Lindegaard 1.6 to 1.7, ACA 44 to 47, basilar 36), canonical protocol, impression and serial-TCD recommendation. |
| C | major | `required_recommendations` BP | Presenting BP 166/94 with no BP action; the only BP text was an SBP target inside the ICU must (C5). | FIXED: MUST-BP-A (nicardipine or clevidipine infusion, or labetalol boluses; no low LVEF, bradycardia, asthma or cocaine). No home medicines, so no MUST-HOME. |
| C | major | `required_recommendations` nimodipine, `prohibited_recommendations` | Nimodipine must without the hypotension adjustment; "Do not administer nimodipine intravenously" is wrong as written (C4). | FIXED: MUST-NIMO and the canonical parenteral-injection prohibition. |
| C | minor | `required_recommendations` ICU and TCD musts, BP prohibition | ICU must carried an SBP target; "daily TCD days 4-14" overstates TCD (COR 2a); "SBP >160" presented as a guideline threshold. | FIXED: MUST-ICU, MUST-DCI and the canonical BP prohibition. |
| D | major | `initial_tool_outputs.drug_interactions.general`, `action-7-check-drug-interactions` | Empty initial drug block whose summary was the criterion's expected evidence (scoring-key leak, C8); template evidence about anticoagulation reversal in a woman on no medicines; tier recommended. | FIXED: block deleted; criterion `optional` (no regular medicines, plan C10) with case-specific rationale and evidence; new follow-up `request_nimodipine_interaction_check` in report voice (empty medication list, CYP3A4 inhibitors and inducers, hypotension and the 30 mg every 2 hours adjustment, no parenteral injection). Leak guard passes. |
| D | major | `followup_outputs` literature (three searches) | Literature as clinical steps with patient values ("Right ICA 2.8 mm"), empty summaries, and a wrong family-screening statement (one affected first-degree relative is not the screening threshold) (C7). | FIXED: all three deleted; canonical literature output last; criterion `optional`, canonical rationale, evidence and citations. |
| C | minor | `ground_truth.key_clinical_evidence` | The family-screening content of the deleted literature mattered but was misstated. | FIXED: pearl added: with her SAH and her father's aneurysm, two first-degree relatives are affected, the usual threshold for offering screening MRA to adult first-degree relatives. |
| B | major | `followup_outputs` telemetry, `action-8` expected evidence | Template text identical in all 30 cases, containing management, 24 h duration impossible at assessment (C12). | FIXED: 3 h since arrival, sinus rhythm 76 to 94 bpm, 6 isolated atrial premature complexes, no sustained arrhythmia or pauses. |
| B | minor | `initial_tool_outputs.labs` | Potassium and magnesium never measured (C9); "Exclusion studies" panel with a non-numeric BNP and engineering text; type-and-screen engineering sentence; interpretive words in `abnormal_values_summary` (C14). | FIXED: potassium 3.9 mEq/L and magnesium 2.0 mg/dL (normal) added to BMP; BNP 46 pg/mL in the Cardiac panel; Exclusion panel deleted; type-and-screen `clinical_significance` null; summary lists values and flags only. |
| C | minor | `initial_tool_outputs.ecg.findings`, `.interpretation` | "QTc mildly prolonged 456 ms" in a woman: the female threshold for prolongation is 460 ms. | FIXED: "QTc 456 ms, upper limit of normal"; en dashes removed from the interpretation. |
| B | minor | `patient.neurological_exam.additional` | "Hunt-Hess Grade 1-2" with severe 9/10 headache and marked nuchal rigidity, which is grade 2 (plan 1.2). | FIXED: "Hunt-Hess Grade 2". The diagnosis label keeps "Hunt-Hess 1-2" (ruling 3; plan section 6 question 5). |
| D | minor | `initial_tool_outputs.ct.additional_observations` | "Classic basal cistern SAH pattern" (teaching text, C14). | FIXED: deleted; "Sella normal in size without mass; no hyperdense dural venous sinus" added so that the reports state what the updated differential cites. |
| B | minor | CTA `angiography_findings` | Right ICA entry read "incidental unruptured aneurysm - likely incidental"; no statement on the cervical vessels the differential relies on. | FIXED: "Small saccular aneurysm 2.8 mm with a smooth wall and no bleb"; "Cervical carotid and vertebral arteries: Patent, no dissection or stenosis". |
| B | minor | `ground_truth.differential` | Generic key features not tied to the case (C11). | FIXED: canonical key features (basal-cistern blood, saccular AComA aneurysm, normal neck vessels, normal sella and sinuses); all `low`, migraine `very_low`. |
| B | minor | `ground_truth.red_herrings[0]`, `action-9` expected evidence | Red herring said the echocardiogram shows apical ballooning, and the echo criterion expected Takotsubo, while this echo is normal (LVEF 62%). | FIXED: data point "Troponin I 0.06 ng/mL with T-wave inversions in V2 to V4"; interpretation says troponin is only mildly raised and the echo shows normal wall motion; echo evidence "LVEF 62% with normal wall motion and normal valves". |
| C | minor | `ground_truth.key_clinical_evidence` | 24-72 h securing pearl, daily-TCD vasospasm pearl, CT sensitivity "~98% ... 80-85% by 24 hours", xanthochromia "6-12 hours" (C1, plan 1.3). | FIXED: the four canonical pearls; the other six kept. |
| A | minor | `ground_truth.action_criteria[*]`, order, `sequence_constraints`, `stop_rule` | Rationale copied from the label; free-text and duplicate citations; literature and TCD before the work-up; no constraints; allowance 0. | FIXED: canonical rationales, case-specific expected evidence, `["[Hoh_2023]"]` (literature Hunt-Hess, Fisher, Hoh); order NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD (optional), literature (optional); follow-ups CTA, DSA, drug check, echo, telemetry, TCD, literature; soft NCCT before CTA and CTA before DSA; stop rule NCCT, labs, ECG, CTA, `max_additional_actions` 1. Labels kept. |
| E | minor | `metadata.case_body_concerns`, `metadata.difficulty_rationale` | Stale TCD-tool concern; rationale described "7 required tools ... consult -> nimodipine". | FIXED: concerns emptied; rationale states the four required studies, recommended DSA and the incidental second aneurysm. |

## Changes, in one paragraph a physician can read before re-reviewing

The presentation is unchanged (49-year-old woman, thunderclap headache at rest one hour before arrival, father with a clipped aneurysm, no medicines, BP 166/94), except that the exam now reads Hunt-Hess grade 2 (severe headache with marked nuchal rigidity). CT (Fisher 3, no IVH or hydrocephalus), CTA (AComA 4.6 x 4.2 mm with an irregular bleb plus a smooth 2.8 mm right ICA ophthalmic aneurysm) and echo (LVEF 62%, normal) are unchanged in substance; the CT now states a normal sella and no hyperdense sinus, the CTA normal cervical vessels, the ECG QTc 456 ms as upper limit of normal for a woman, and the labs add potassium 3.9, magnesium 2.0 and BNP 46. The pathway is NCCT, labs, ECG, CTA, a new diagnostic catheter angiography (bleb-bearing AComA aneurysm with a 2.3 mm neck and the smooth 2.9 mm ICA aneurysm), an optional nimodipine interaction check (no medicines; CYP3A4 and hypotension cautions), echo, 3 hours of telemetry (sinus rhythm, rare atrial ectopy), an optional day-0 baseline TCD (normal, replacing a day-6 vasospasm report) and an optional general literature search last. The musts now say: enteral nimodipine 60 mg every 4 hours for 21 days (30 mg every 2 hours if hypotensive); secure the AComA aneurysm by coiling or clipping as early as feasible, preferably within 24 hours, after joint review, the ruptured aneurysm first, with the incidental ICA aneurysm managed separately after recovery; neurocritical care admission; lower BP now with nicardipine, clevidipine or labetalol, avoiding hypotension; sodium monitoring; DCI surveillance with euvolemia and no prophylactic hypervolemia. A pearl on offering screening MRA to adult first-degree relatives (two affected first-degree relatives) replaces the deleted, misstated family-screening literature.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` (ISAT) is cited in the canonical literature output; it must be added to the SAH criteria-pack allow-list (plan section 5.1b).

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case. The label keeps "Hunt-Hess 1-2" while the exam now says grade 2 (plan section 6 question 5, condition-wide).

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the git diff against HEAD (patient block changed only in `neurological_exam.additional`, Hunt-Hess 1-2 to 2, consistent with severe headache and marked nuchal rigidity; label untouched per ruling 3); every own-finding row against the file; criteria order, tiers, required arguments and the perfect-agent mapping (each criterion receives its own report); stop rule equals the required set; soft NCCT-before-CTA and CTA-before-DSA constraints; DSA sizes within 0.3 mm of the CTA and dome-to-neck arithmetic (4.8 / 2.3 = 2.1); lab `is_abnormal` flags against reference ranges; labs, ECG, echo and telemetry expected evidence against the reports; canonical literature output identical across S05-S10; no 24-72 h, 24-48 h, triple-H, Exclusion panel, free-text citation or day-N timeline left; LP avoided action `harm` (no IVH or hydrocephalus); leak guard passes.
Found and changed: the new family-screening pearl said her SAH and her father's aneurysm "make two affected first-degree relatives", which reads as if she herself were the screening candidate. Rewritten (`ground_truth.key_clinical_evidence[-1]`): "Her aneurysmal SAH and her father's aneurysm make this a family with two affected first-degree relatives, the usual threshold for offering screening MR angiography, after counselling, to the other adult first-degree relatives (her siblings and adult children)."
Left as is: the separate "Secure the ruptured AComA aneurysm first ..." must beside MUST-SECURE (plan section 4 asks for it); CTA observation "AComA + right ICA incidental" (a radiologist's legitimate attribution). `perfect_agent.py -v` and `case_io.py check` clean after the edit.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `ground_truth.diagnosis.accepted[0] (Hunt-Hess 2)`: S05's exam is alert, GCS 15, severe headache and nuchal rigidity, which is grade 2 (Q5).
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
