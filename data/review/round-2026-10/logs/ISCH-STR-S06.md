# ISCH-STR-S06
Reviewer status: R1 none, R2 none (never reviewed; no notes in `notes/ISCH-STR.json`) | Approved before this round: no

Never-reviewed case: the plan's survey items (section 4, S06) and the all-case classes were applied, plus the errors found on reading. Correct prose was left as written.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The case has no reviewer notes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | "well within the IV thrombolysis window" is an eligibility verdict (C10). | FIXED: removed; times kept. |
| B | minor | `patient.history_present_illness` | "baseline at 09:30" next to a witnessed onset at 09:45 leaves LKW ambiguous. | FIXED: "at his baseline until the weakness began at 09:45" (LKW 09:45). |
| E | minor | `patient.history_present_illness` | "anticoagulant use beyond his daily aspirin" calls aspirin an anticoagulant. | FIXED: "takes no anticoagulant; his only antithrombotic is daily aspirin". |
| C | major | `patient.neurological_exam.motor`, `.additional` | NIHSS 5 could not be derived: "pronator drift" scores arm 1, and leg drift was not described (recount gave 3) (C13). | FIXED: the exam now describes the drift (arm reaches the bed before 10 s, leg before 5 s, both with some effort against gravity), so NIHSS 5 = facial palsy 1, right arm 2, right leg 2; total itemised; duplicate "no hemineglect" removed. NIHSS 5 unchanged everywhere else. |
| E | minor | `patient.neurological_exam.gait` | "Antalgic" gait for hemiparesis (antalgic means pain-limited). | FIXED: "Hemiparetic gait: circumducts the right leg". |
| D | minor | `initial_tool_outputs.ct.findings[2].description` | "No acute DWI equivalent available on CT" is not radiology language. | FIXED: sentence removed. |
| B | minor | `initial_tool_outputs.labs.interpretation` | "CBC, BMP, and coagulation within normal limits" while BMP glucose is flagged high. | FIXED: "CBC, coagulation, electrolytes, renal function, troponin and TSH within normal limits". |
| B | major | `initial_tool_outputs.mri.findings[0].signal_characteristics.FLAIR` | Self-contradictory ("subtle hyperintensity developing" and "no significant FLAIR signal yet") and interpretive about timing (C12). | FIXED: "Faint FLAIR hyperintensity, less conspicuous than the DWI lesion". |
| B | minor | `initial_tool_outputs.mri.additional_observations[3]` | MRA "mild intracranial atherosclerotic irregularity of the bilateral MCAs" contradicts the CTA (normal MCA calibre). | FIXED: sentence removed; MRA states no occlusion or stenosis, as the CTA. |
| D | minor | `followup_outputs[0]` (CTA) `additional_observations` | "No perforator occlusion visible at CTA resolution": perforators are not resolved by CTA; the line hints at the mechanism. | FIXED: removed. |
| C | minor | `followup_outputs[2]` (TTE) | LAVI 30 mL/m2 called "mildly elevated" and "borderline left atrial enlargement" (normal is up to 34); no `echo_type`. | FIXED: normal left atrial size in findings and impression, unit added in `chambers`; impression rewritten as a TTE report; `tool_parameters.echo_type` TTE. |
| B | minor | `followup_outputs[3]` (Holter) | No admission timing (C2); no `tool_parameters`. | FIXED: findings and impression open "Recorded on the stroke unit after admission, 24 hours."; `tool_parameters.monitor_type` holter_24h. |
| C | major | `followup_outputs[1]` (drug check) | Lab values, times and eligibility verdicts inside `contraindications`; says BP 172/96 "must be reduced to <185/110" (it already is); "hold metformin for contrast, resume after 48 h" (outdated: not needed with eGFR 30 or more and no AKI); 2019 guideline cited; "no anticoagulants beyond aspirin". | FIXED: rewritten from the medication list: aspirin (not a contraindication; no antithrombotic for 24 h after alteplase), lisinopril angioedema, glipizide hypoglycaemia, metformin and contrast, amlodipine, atorvastatin; `contraindications` empty (none present); warnings on BP thresholds, angioedema, glucose; tenecteplase and clopidogrel as alternatives. Criterion recommended (C7), `required_arguments` {}. |
| D | major | `followup_outputs` (secondary prevention labs), `action-5-interpret-labs` | Follow-up duplicates the admission HbA1c and lipids ("Fasting Glucose 188" is the random arrival glucose) and its interpretation echoed the criterion (C9). | FIXED: criterion and follow-up removed; HbA1c and LDL are read from the admission labs and carried into the musts. |
| C | minor | `followup_outputs` (literature) | 2019 guideline as first result; Kernan 2014 cited for SBP below 130 and high-intensity statin in lacunar stroke; summary echoes the case. | FIXED: AHA/ASA 2026 (IVT for disabling deficits, BP thresholds), TOAST, Kleindorfer 2021 (BP below 130/80, atorvastatin 80 mg for LDL above 100), SPS3 antiplatelet (NEJM 2012); general summary. Criterion optional, last, `required_arguments` {} (C8). |
| B | major | `followup_outputs` order, `ground_truth.action_criteria` order | Echo, Holter, literature, drug check and labs before the CTA (C1). | FIXED: follow-ups CTA, drug check, TTE, Holter, literature; criteria NCCT, labs, ECG, CTA, MRI (optional), drug check, TTE, monitoring, literature. Ids kept. |
| A | minor | criteria tiers | Echo and Holter required in a lacunar case (plan 3.1: recommended). | FIXED: both recommended; monitoring alternatives holter_24h, holter_48h, telemetry. |
| A | minor | criteria labels, rationales, citations, expected evidence | Label = rationale; free-text citation; duplicated, superseded `[AHA_ASA_2019]` / `[AHA_ASA_2014]` / `[Sanna_2014]`; template expected evidence (C17). | FIXED: distinct rationales, case-specific expected evidence; `[AHA_ASA_Stroke_2026]` for acute steps and avoided actions, `[AHA_ASA_2021_secondary]` for echo and monitoring (aetiological work-up). |
| A | minor | `sequence_constraints`, `stop_rule` | Hard template constraint (drug check after NCCT); allowance 0; echo and Holter in the stop rule. | FIXED: soft NCCT before CTA, CTA before echo, CTA before monitoring; stop rule NCCT, labs, ECG, CTA; allowance 1. |
| C | major | `ground_truth.assessment.required_recommendations` | No decision; "DWI MRI is required to confirm the diagnosis"; "reduce BP to <185/110 before tPA" in a patient already at 172/96; "well within the window"; generic secondary prevention (C4, C6). | FIXED: LKW (09:45, 33 min) and NIHSS 5; decision must (give IVT: disabling deficit, no contraindication; no EVT: no LVO); door-to-needle; BP kept below 185/110 then 180/105 (no lowering needed now); lisinopril angioedema; glucose 140 to 180 mg/dL in 24 h (188 on arrival, on glipizide); telemetry (C2 canonical); MRI may confirm after the decision; single antiplatelet 24 h after IVT (NIHSS 5 is above the DAPT threshold); atorvastatin 80 mg (LDL 141 on 40 mg); long-term BP below 130/80 with lisinopril and amlodipine resumed once stable; HbA1c 8.4% optimised. ECG and TOAST musts kept. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | 140/90 prohibition in a thrombolysed patient (C5). | FIXED: removed; added "no antithrombotic within 24 hours of IVT" and "no long-term dual antiplatelet therapy for lacunar stroke (SPS3)". Other four kept as written. |
| C | minor | `ground_truth.differential` | Capsular warning syndrome "high" with no fluctuating history; cortical MCA stroke "moderate" while its own key features say "ruled out"; cardioembolic entry "workup still required" (ruling 7). | FIXED: capsular warning syndrome low (single sustained deficit, completed infarct; fluctuation watched for); cortical MCA low; cardioembolic key features state the ECG, Holter and TTE results. |
| E | minor | `ground_truth.key_clinical_evidence` | July 2026 tier line (C17); "must be followed by DWI MRI"; "CTA/carotid duplex" (no duplex in the case); no decision evidence. | FIXED: tier line removed; MRI line states MRI after the decision; "(CTA)"; decision line added (times, NIHSS itemised, disabling deficit, BP, INR, platelets, no LVO). |
| D | minor | `ground_truth.red_herrings[0]` | "DWI MRI is required for confirmation". | FIXED: thrombolysis decided on the deficit and the CT; MRI can confirm afterwards. |
| E | minor | `metadata.case_body_concerns` | Stale mock-server single-slot note (C17). | FIXED: emptied (CTA is served by its own follow-up). |
| A | minor | `ground_truth.diagnosis.accepted` | Synonyms "embolic stroke", "cardioembolic stroke" and "CADASIL" are accepted for a sporadic lacunar infarct; `accepted[0]` has an em dash. | FLAGGED: CENTRAL (not hand-edited, ruling 3). |
| B | minor | `initial_tool_outputs.ct.additional_observations[6]` | NCCT names the left internal capsule and corona radiata (no hypodensity). | FLAGGED: kept; a radiologist given "right hemiparesis" comments on the relevant region, and it states only what CT shows. |

## Changes, in one paragraph a physician can read before re-reviewing

The story is unchanged: a 62-year-old right-handed man with hypertension, diabetes and dyslipidaemia, witnessed sudden pure motor right hemiparesis at 09:45, arrival 10:18, BP 172/96, normal CT, no LVO on CTA, a 9 x 7 mm left posterior limb internal capsule lacune on MRI, sinus rhythm on ECG and Holter, no cardiac source on TTE. The exam now describes the arm and leg drift so the NIHSS 5 is scorable (face 1, arm 2, leg 2); the HPI no longer states eligibility and fixes LKW at 09:45. The MRI FLAIR is faint (not contradictory), the MRA no longer contradicts the CTA, the echo calls LAVI 30 normal, the Holter is dated to the admission, and the drug check lists his own medicines (aspirin, lisinopril angioedema, glipizide, metformin not stopped for contrast) without lab values. The work-up runs NCCT, labs, ECG, CTA, then drug check, TTE and monitoring (both recommended); the separate HbA1c/lipid step is removed (they are in the admission bloods) and literature is optional. Musts now state the decision (give IV thrombolysis for a disabling deficit at 33 minutes, no thrombectomy without LVO), keep BP below 185/110 and then 180/105 without lowering it now, watch for angioedema, keep glucose 140 to 180, telemetry, single antiplatelet after 24 hours, atorvastatin 80 mg, BP below 130/80 long term and glycaemic optimisation; the 140/90 prohibition is replaced by no antithrombotic within 24 hours of IVT and no long-term dual antiplatelet therapy.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[AHA_ASA_Stroke_2026]` and `[AHA_ASA_2021_secondary]` for the criteria-pack allow-list (plan 5.1).
- Synonyms for `icd_codes[0]` I63.81 (lacunar, small-artery occlusion): the appended list accepts "embolic stroke", "cardioembolic stroke" and "CADASIL", which are wrong answers for a sporadic hypertensive lacune; please restrict the I63.81 synonyms in `diagnosis_synonyms.yaml`. `accepted[0]` also contains an em dash (left untouched, ruling 3).
- `perfect_agent.py -v` prints `<- ?` for criteria answered by `initial_tool_outputs.ct` and `.labs` (its source labeller compares a dump with nulls against one without); a direct call confirms both are served from this case's own reports, not the fallback. Same in S05.

## Open questions for Andrea (judgment calls you could not settle)

- The plan calls the drug check recommended; its `contraindications` field is empty because the case has no contraindicating drug (plan C7 asks for a non-empty field only when a contraindication exists).
- Statin must: atorvastatin 80 mg per SPARCL (LDL above 100 mg/dL); I did not set an LDL target below 70 mg/dL because the carotid plaque is under 30% and TST enrolled patients with established atherosclerotic disease. Some would set the target given diabetes and plaque.
- The case was never physician-reviewed; it needs a first review.

## Verification
Adversarial verifier, 23 October 2026. Read the log, the diff and the whole final case.

Checked: NIHSS 5 now derivable (face 1 "droop on voluntary smile", arm 2 and leg 2 from the described drift with effort against gravity); LKW 09:45 witnessed, arrival 10:18, 33 minutes; BP 172/96 below 185/110 so no lowering before IVT; decision must (IVT for a disabling deficit, no EVT without LVO); drug check recommended with an empty contraindications field (none exists) and correct metformin-contrast statement; HbA1c and lipid follow-up removed with the values carried into the musts; single antiplatelet 24 hours after IVT (NIHSS 5 above the CHANCE/POINT threshold), no long-term DAPT (SPS3); atorvastatin 80 mg for LDL 141; long-term BP below 130/80; differential at assessment-time likelihoods; order, tiers, constraints and stop rule per plan; no "well within the window" left.

Found and fixed:
- `required_recommendations[3]`, `key_clinical_evidence[4]`, `red_herrings[1].correct_interpretation`: "cannot grip" contradicted the exam (3/5 grip); the deficit is disabling because the grip is weak enough to drop a mug and the gait needs assistance. Now "weak right grip (3/5) that made him drop a mug and a gait that needs assistance" (must), "weak right grip, cannot walk safely without assistance" (key evidence), "weak grip, cannot ambulate safely without assistance" (red herring).

The CENTRAL synonym request (embolic, cardioembolic and CADASIL accepted for a lacune) stands. `perfect_agent.py -v` passes; `case_io.py check` is clean for this case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
I63.81 no longer grants CADASIL (scoped to RP05) and the case no longer gets embolic/cardioembolic labels.
- labels removed: "embolic stroke", "cardioembolic stroke", "stroke", "CADASIL"
- labels added: "small vessel stroke"
- codes removed: I63.4, I63.5, I63.3, I63.2, I63.0, I63.1, I63.89
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TTE" to the stored echocardiogram report (the schema now keeps the field and the MockServer routes TTE/TEE/bubble orders by it; the value was only in `tool_parameters`).

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
- Decision: serve: new first alternative (old order kept as an alternative). A must raises atorvastatin for LDL 141; the lipid panel was not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.
