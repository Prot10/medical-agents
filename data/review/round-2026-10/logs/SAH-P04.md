# SAH-P04
Reviewer status: R1 none, R2 none (no notes, no status in the notes file; plan treats it as probably among R2's approvals) | Approved before this round: probably (unconfirmed, plan section 6 question 6)

Because the case may have been approved, every change below corrects a real error (a condition-wide class of plan section 2, or a fact wrong in this file).

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer note for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status` | "Alert and oriented x4; GCS 14 ...; mildly somnolent" (alert and somnolent at once) with a Hunt-Hess 3 label. | FIXED: "Somnolent but rousable to voice; GCS 14 (E3V5M6); oriented once roused, with slowed responses" (C13), consistent with the HPI's regained orientation. |
| D | major | `initial_tool_outputs.ct.additional_observations`, `findings[3]` | "Fall may be secondary to SAH", "Trauma vs SAH - CT supports SAH as primary event", "fell during SAH" (clinical synthesis and differential in a CT report). | FIXED: removed; scalp finding reworded as an imaging finding. The trauma question is now scored as a red herring and a differential entry instead. |
| C | major | `followup_outputs` FFP | `request_ffp_coagulopathy`, "Fresh frozen plasma 4 units IV for INR 1.4" is a treatment filed as a drug check, and plasma is not indicated at INR 1.4 (C8). | FIXED: deleted. New must: vitamin K 10 mg IV, no plasma, INR threshold for the EVD agreed with neurosurgery. |
| D | major | `initial_tool_outputs.drug_interactions`, `.literature_search` | Template blocks repeating the criteria's expected evidence (leak guard failed). | FIXED: both deleted. |
| D | major | clonazepam check | "Patient already took double dose (1 mg) - causing somnolence contributing to exam difficulty" is a patient-specific verdict that answers the case's grading question; "Avoid in acute phase" as a formulary status. | FIXED: rewritten as `request_nimodipine_clonazepam_interaction_check` (losartan hypotension, CNS depression with alcohol, masking of the exam, alcohol withdrawal, hepatic impairment raising nimodipine exposure). Criterion accepts `drug: nimodipine` or `drug: clonazepam`, `recommended`. |
| C | major | labs | No potassium or magnesium with QTc 518 ms and daily alcohol; panel named "Liver_Alcohol" (names the cause); summary interpretive and incomplete. | FIXED: potassium 3.6, magnesium 1.6 mg/dL (L) added (C9); panel renamed `Hepatic`; factual summary and interpretation with all abnormal values; type and screen `clinical_significance` null. |
| C | major | musts | EVD template; two 24-72 h musts; ICU with an SBP target; TCD days 4-14; no QT, LVEF, alcohol, INR or home-drug actions. | FIXED: MUST-EVD-NOW (IVH, depressed consciousness), vitamin K must, MUST-SECURE (AComA), MUST-NIMO, MUST-ICU, MUST-BP-A with nicardipine or clevidipine (LVEF 28%, HR 102), home-drug must (withhold losartan, minimal clonazepam), MUST-QT (518 ms, K 3.6), MUST-LVEF (28%, moderate MR), MUST-ALCOHOL, sodium, MUST-DCI. |
| C | major | `avoided_actions` `avoid-harm-1-analyze-csf` | Severity `harm` with IVH and hydrocephalus on CT. | FIXED: `contraindicated` (C6). |
| E | minor | CTA | "Large" for a 9.2 mm aneurysm (small is under 10 mm). | FIXED: dropped (C13); cervical arteries line added. |
| B | major | TCD | "Day 2" in a patient seen about 1 hour after onset; protocol named MCA only. | FIXED: admission baseline, post-ictus day 0, normal velocities. |
| C | major | telemetry | Template text, 24 h. | FIXED: 3 h of sinus rhythm and sinus tachycardia 92 to 116/min, 44 PVCs with one couplet, QTc 518 ms on monitoring leads. |
| B | minor | echo | "Cardiology consultation recommended" phrased as an order; no `echo_type`; em dash. | FIXED: "Consider cardiology consultation"; TTE. |
| C | minor | differential | Template key features; the fall (a mimic the case raises) not in the differential. | FIXED: C11 key features (RCVS with the Valsalva trigger); new `low` entry "Traumatic subarachnoid hemorrhage from the fall". Pituitary entry says "no ocular motor deficit", because visual fields are not documented. |
| C | minor | red herrings | Only the troponin template; its interpretation generic. Clonazepam and the fall confound the case but were not scored. | FIXED: troponin red herring names this patient's values and echo; two red herrings added (double-dose clonazepam; fall with scalp swelling). |
| A | minor | criteria | No DSA; literature `recommended`; template rationales and evidence; free-text citations; no constraints; stop rule allowed 0 extra actions. | FIXED: `dsa-aneurysm-anatomy` (9.0 x 7.8 mm, wide 4.8 mm neck, right A2 origin partly incorporated, single aneurysm, no vasospasm); literature `optional`, canonical output last; plan 1.3 rationales; NCCT before CTA and CTA before DSA (soft); stop rule = the four required criteria, `max_additional_actions` 1. |
| E | minor | `metadata` | Stale TCD-tool and CSF concerns; template difficulty rationale. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The exam is now consistent with Hunt-Hess 3 (somnolent, GCS 14, oriented once roused). The CT reports only imaging findings (Fisher 4, blood in the third and fourth ventricles, hydrocephalus, scalp swelling without fracture). The trauma question and the double-dose clonazepam are scored as red herrings, and traumatic SAH is a `low` differential entry. The pathway is NCCT, labs (potassium 3.6, magnesium 1.6 added), ECG, CTA, a new diagnostic DSA, the nimodipine and clonazepam check, echo (LVEF 28%, moderate MR), telemetry, then optional TCD (admission baseline) and literature. The FFP "drug check" is gone. The musts are: EVD; vitamin K 10 mg IV without plasma for INR 1.4, with the EVD INR threshold agreed with neurosurgery; securing as early as feasible, preferably within 24 hours; nimodipine; neuro-ICU; nicardipine or clevidipine for 196/118; withholding losartan and minimising clonazepam; potassium and magnesium repletion with ECG monitoring for QTc 518 ms; cardiology and neuroanesthesia input for LVEF 28%; thiamine and withdrawal monitoring; sodium; and DCI surveillance. LP is now `contraindicated`.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Drew_2010]` (MUST-QT) and `[Molyneux_2002]` (canonical literature) need the criteria-pack allow-list (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- Approval status unknown (plan section 6 question 6). The changes are error corrections whichever way it goes.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, plan section 4 P04 and the whole final case (probably approved: checked that each change corrects a real error).

Checked: exam Hunt-Hess 3 (somnolent, GCS 14, E3V5M6); MUST-EVD-NOW, LP `contraindicated` (IVH and hydrocephalus on CT); FFP follow-up deleted and replaced by the vitamin K must; no initial drug or literature block; clonazepam check content generic (no patient verdict) and its alternative argument matches the trigger; magnesium 1.6 (L) and potassium 3.6 consistent with MUST-QT and the abnormal summary; MUST-LVEF (28%, moderate MR) matches the echo; MUST-ALCOHOL consistent with the withdrawal warning; MUST-BP-A without labetalol (LVEF 28%); losartan withheld; sulfa allergy does not conflict; CTA 9.2 mm and DSA 9.0 mm agree with a 4.8 mm neck (dome-to-neck 1.9); "Large" removed; differential gains traumatic SAH `low`. Leak guards pass.

Found and fixed:
- The new fall red herring said "Found down after a witnessed fall", and the HPI's last sentence said "found down with a witnessed fall", while the HPI itself says the neighbor heard a thud and then found him. Red herring `data_point` now "Found on the bathroom floor after a fall the neighbor heard, with right parieto-occipital scalp swelling"; HPI sentence now "he was found on the floor after a fall that no one saw" (`patient.history_present_illness`, `ground_truth.red_herrings[2].data_point`).
- Telemetry impression and criterion evidence called 44 isolated PVCs in 3 hours (about 15 per hour) "frequent"; changed to "Isolated PVCs with one couplet" in the telemetry follow-up impression and "isolated PVCs and one couplet" in `action-8-order-cardiac-monitoring.expected_evidence`.

Re-ran `perfect_agent.py SAH-P04 -v` (pass) and `case_io.py check` (no failure names the case).

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `echo.findings[0]`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.wall_motion`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.impression (consultation advice removed)`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.recommended_actions`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- fallback_tool_outputs.mri: SAH-consistent brain MRI instead of the library normal report: an off-pathway brain MRI was answered by the library normal report (no blood on SWI), contradicting the CT; the case fallback now reports the CT's blood on FLAIR and SWI (CENTRAL 10).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
- followup_outputs: MR angiography report added before the literature output (aneurysm site and size from the DSA, 0.2 mm smaller as TOF reads it; P02 negative): an MRA order was answered by a fallback reporting no abnormality, contradicting the CTA and DSA (CENTRAL 10). MRA stays a waste action after the CTA.
- `ground_truth.diagnosis` (synonyms re-expanded with `--prune`): diagnosis_synonyms.yaml: the I60 category no longer grants I60.8 (non-aneurysmal SAH), so the code was pruned from this aneurysmal case.
- Checks after the close-out: `perfect_agent.py` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k SAH-` pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'No diagnostic abnormality identified on this study.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
