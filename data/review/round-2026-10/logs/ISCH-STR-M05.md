# ISCH-STR-M05
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| f9e644a8-ba54-43b7-ada4-1fb2d1b91165 | FIXED | Must rewritten: "Refer for right carotid revascularization (endarterectomy, or stenting if surgical risk is high) between 2 days and 2 weeks after the stroke": the class I attribution (70-99%, perioperative risk below 6%) is cited to AHA/ASA 2021 secondary prevention, and "Emergent endarterectomy within 48 hours is not beneficial (AHA/ASA 2026 §4.12, COR 3: No Benefit)" is added. The same timing appears in key evidence, the literature output (2021 and 2026 guidelines) and `metadata.clinical_pearls` (the "class I indication" pearl now carries the 2-week window and the 48-hour limb). |
| a407727c-db4a-4f39-9db6-a6c3bf45b838 | FIXED | Decision taken as the plan states: IVT candidate. The permissive "140 to 180 systolic, do NOT lower BP" must and the "Do NOT aggressively lower blood pressure" prohibition are removed. New musts: explicit decision (IVT: give once BP is below 185/110; no EVT, no LVO); lower BP from 192/106 cautiously to just below 185/110 with small titrated labetalol or nicardipine, then below 180/105 for 24 h, avoiding overshoot because the deficit worsened at 146/82; volume repletion and no antihypertensive restart for 48 to 72 h. New prohibition: do not lower BP more than thrombolysis requires or abruptly. To make LKW at 2 hours defensible, the HPI now states that every earlier episode resolved completely and that he was at baseline that morning (the red herring said "partially resolving", which would have placed LKW 5 days back). |
| b36e42fb-f85b-40b1-9223-6b91c2c0cd79 | FIXED | `mental_status`: "No neglect of left-sided stimuli"; the serial-sevens line no longer calls 1 error in 5 inattention. `cranial_nerves`: the gaze preference is no longer attributed to inattention ("partial gaze preference to the right, overcome on command"). NIHSS is 6 (gaze 1, left arm 2, left leg 2, sensory 1) as R2 recounted; `motor` now describes the arm and leg drift tests that score 2 (the exam said "mild pronator drift", which scores 1). Total updated in the exam, LKW must and key evidence. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.chief_complaint`, HPI, red herring | Timeline cannot happen: a "3-day history" whose episodes began on the evening of a colonoscopy done 5 days ago. | FIXED: 5-day history in chief complaint, HPI and red herring; five episodes in total, each resolving completely. |
| C | major | HPI, PMH | Colonoscopy 5 days ago with no statement on polypectomy or bleeding (decides whether the recent procedure contraindicates IVT); "anesthesia team / intraoperative" for a colonoscopy under conscious sedation. | FIXED: "No polyps were removed, and he has had no rectal bleeding since"; "endoscopy team", "intraprocedural". Reduced oral intake since the procedure added (supports the BUN of 22 and the volume-repletion must). |
| C | major | `assessment`, key evidence | "Withholding of antihypertensives" presented as part of the hypotensive trigger (it raises, not lowers, pressure). | FIXED: the trigger is the procedural hypotension plus poor intake; the must and key evidence say withholding antihypertensives is not a hypotensive trigger. |
| B | major | `initial_tool_outputs.mri` FLAIR, T1, T2 | FLAIR "indicating infarct age greater than 4-6 hours" and T1 hypointensity with LKW 2 hours before arrival; also implies a recent infarct days old, which would weigh against IVT. | FIXED: DWI-FLAIR mismatch (faint FLAIR only in the largest focus), no T1 abnormality; impression numbered and notes the mismatch. |
| D | major | `initial_tool_outputs.ct` | NCCT template: "in watershed", "does not justify withholding treatment", "Nothing on this study contraindicates intravenous thrombolysis...". | FIXED: canonical normal impression, ASPECTS 10; observations describe the deep white matter and the absent hyperdense vessel sign. |
| C | major | key evidence, `metadata.difficulty_description` | "Carotid duplex is the load-bearing tool: PSV >400 cm/s, ratio >7": no duplex exists in the case (template carry-over). | FIXED: CTA named as the load-bearing study with its actual result. |
| C | major | `followup_outputs` drug check, criterion `action-8` | Criterion asked for `drug: alteplase` while the output was a clopidogrel check; lisinopril with alteplase (angioedema) not mentioned; NSAID warnings for a patient who takes none; "not indicated here given no AF on monitoring" (cross-result statement). | FIXED: output covers thrombolysis (lisinopril angioedema, aspirin) and clopidogrel (omeprazole CYP2C19, switch to pantoprazole); NSAID text removed; criterion required (plan C7), `{}` arguments, after the CTA; trigger renamed. Musts added for angioedema watch and the pantoprazole switch. |
| C | major | `assessment` | Antiplatelet must "intensify from aspirin monotherapy" without timing after IVT; "Do not withhold antiplatelet therapy..." conflicts with the 24-hour post-IVT pause. | FIXED: antiplatelet after the 24-hour imaging (aspirin plus clopidogrel short term while awaiting revascularization, then a single agent); prohibition replaced by "no antiplatelet or anticoagulant in the first 24 hours after IVT". Statin must made specific (atorvastatin 80 mg, ezetimibe if LDL stays at or above 70); smoking and prediabetes must added. |
| A | minor | criterion `action-5-interpret-labs` | Lipid/HbA1c criterion answered by the admission labs (plan baseline warning). | FIXED: removed (plan C9); targets live in the musts. |
| C | minor | literature output, criterion `action-7` | AHA/ASA 2019 and 2014 cited; Momjian-Mayor title not the real one; empty summary. | FIXED: Momjian-Mayor and Baron 2005 (real title), AHA/ASA 2021, AHA/ASA 2026 (§4.12 content as quoted by R2), TOAST; general summary; criterion optional, `{}`, last. |
| C | minor | criteria `action-9`, `action-10` | Echo and Holter required. | FIXED: recommended (plan 3.1); monitoring alternatives `holter_24h`, `holter_48h`, `telemetry`; Holter opens "Recorded on the stroke unit after admission, 24 hours.", HR min/max filled, `tool_parameters` set; echo `tool_parameters` TTE and LAVI unit added. |
| C | minor | `ground_truth.differential` | Recurrent TIA "high" and cardioembolism "moderate" after the work-up; seizure entry cites an EEG never done. | FIXED: low and low with the results; seizure entry cites the history and DWI. |
| B | minor | CTA impression | Prose, missing final period. | FIXED: numbered, opening with the ICA stenosis. |
| E | minor | `metadata.case_body_concerns`, pearls | Stale mock-server note; pearl "pathognomonic ... mandates a permissive BP strategy" contradicts the decision. | FIXED: list emptied; pearls rewritten. |
| A | minor | criteria, avoided actions, constraints, stop rule | Free-text citation, `[AHA_ASA_2019]`/`[AHA_ASA_2014]` duplicates, labels copied into rationales, hard template constraint, stop rule with echo and Holter, allowance 0. | FIXED: plan 1.1 keys, real rationales, three soft constraints, stop rule NCCT, labs, ECG, CTA, drug check, allowance 1. |
| B | minor | labs | Friedewald LDL from the panel is about 141 vs 138 reported. | FLAGGED: within the range of a directly measured LDL; left. |

## Changes, in one paragraph a physician can read before re-reviewing

A 70-year-old man with right internal borderzone infarcts from an 85-90% right ICA stenosis after hypotension during a colonoscopy. The timeline is now consistent: five episodes over 5 days, each resolving completely, then a persistent deficit 2 hours before arrival, so LKW is 2 hours; the colonoscopy involved no polypectomy and no bleeding. The case now takes a single position on thrombolysis: IVT is given, after bringing the BP of 192/106 cautiously to just below 185/110 with small titrated doses, then below 180/105 for 24 hours, avoiding overshoot because his deficit worsened at 146/82. The permissive 140-180 must is gone. No thrombectomy (no LVO). Carotid revascularization is referred for 2 days to 2 weeks (AHA/ASA 2021, class I), and emergent endarterectomy within 48 hours is stated as not beneficial (AHA/ASA 2026 §4.12). The NIHSS is 6 (gaze 1, arm 2, leg 2, sensory 1); the exam tests neglect on the left, drops the serial-sevens "inattention", and describes drift that scores 2. The MRI FLAIR now matches a 2-3 hour-old infarct. The NCCT template text is gone, and the phantom carotid duplex is replaced by the CTA. The drug check now covers lisinopril angioedema with the thrombolytic and omeprazole with clopidogrel. Musts add volume repletion, no antihypertensive restart for 48-72 hours, antiplatelet therapy after 24 hours, pantoprazole, atorvastatin 80 mg and smoking cessation. Pathway: NCCT, labs, ECG, CTA, drug check (required); MRI optional; TTE and Holter recommended; literature optional and last; the separate lipid/HbA1c criterion is removed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[AHA_ASA_Stroke_2026]` and `[AHA_ASA_2021_secondary]` for the criteria-pack allow-list (plan 5.1).
- `ground_truth.diagnosis.accepted[0]` contains an em dash; left untouched per ruling 3.

## Open questions for Andrea (judgment calls you could not settle)

- Antiplatelet regimen: the must allows short-term aspirin plus clopidogrel while awaiting carotid revascularization (CARESS reduced microembolic signals in symptomatic carotid stenosis), then a single agent. No guideline grades dual therapy for a symptomatic extracranial stenosis at NIHSS 6. If R2 prefers single antiplatelet therapy, the clopidogrel and pantoprazole musts drop to "if clopidogrel is chosen".
- The decision to thrombolyse in a flow-dependent patient depends on lowering BP only to just below 185/110. Some clinicians would avoid lowering BP at all and treat him as a non-candidate. The plan and R2's note allow either, and the plan chose IVT.

## Verification
Adversarial verifier, 23 October 2026. Checked: all 3 note ids in the table; carotid must gives 2 days to 2 weeks, class I attributed to AHA/ASA 2021 (70-99%, perioperative risk below 6%), emergent CEA COR 3 to AHA/ASA 2026 §4.12, and pearl, key evidence and literature agree; the permissive 140-180 must is gone, BP is lowered just below 185/110 before IVT and kept below 180/105 after, with no conflicting prohibition; "No neglect of left-sided stimuli", serial sevens not called inattention, NIHSS 6 recounted (arm and leg drift to the bed with effort against gravity score 2; face 0, ataxia 0). Timeline: five fully resolving episodes over 5 days, baseline that morning, LKW 2 hours; colonoscopy without polypectomy or bleeding; MRI FLAIR mismatch fits 2 hours, so the MRI does not show an infarct days old (no recent-stroke contraindication). Gaze preference to the right matches the right hemisphere lesion. Drug check required (omeprazole with clopidogrel, lisinopril angioedema) and placed after the CTA; antiplatelet only after the 24-hour imaging; atorvastatin 80 mg and pantoprazole musts match the drug check. Found no error requiring a change. `perfect_agent.py -v` and `case_io.py check` clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "embolic stroke", "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.4, I63.5, I63.3, I63.2, I63.1, I63.8, I63.81, I63.89
- codes added: I63.03
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TTE" to the stored echocardiogram report (the schema now keeps the field and the MockServer routes TTE/TEE/bubble orders by it; the value was only in `tool_parameters`).
- Auditor flag: triglycerides 196 to 211 mg/dL (panel value, abnormal summary, interpretation, must) so the Friedewald LDL equals the reported 138 mg/dL (218 - 38 - 211/5 = 137.8). The short DAPT must is kept (decision OQ4c).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-3-interpret-labs]`.alternatives: was [glucose, CBC, coagulation, creatinine, troponin]; now [glucose, CBC, coagulation, creatinine, troponin, lipid_panel] | [glucose, CBC, coagulation, creatinine, troponin].
- Decision: serve: new first alternative (old order kept as an alternative). A must raises atorvastatin and adds ezetimibe for LDL 138; the lipid panel was not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-4-analyze-brain-mri` rationale: "Optional: shows the borderzone pattern that supports a hemodynamic mechanism; it must not delay thrombolysis, which is decided on CT." -> "It shows the borderzone pattern that supports a hemodynamic mechanism; it must not delay thrombolysis, which is decided on CT."
