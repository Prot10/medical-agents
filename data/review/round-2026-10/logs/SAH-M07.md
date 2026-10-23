# SAH-M07
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 4daa3aa1-09bf-45fd-978e-98c4e8ee15f6 | FIXED | Substance applied (secure urgently) with the governing window, not the note's "24-72 hours": both 24-72 h musts replaced by one MUST-SECURE ("secure the ruptured basilar apex aneurysm, after anticoagulant reversal, ... as early as feasible, preferably within 24 hours of onset [Hoh_2023]") in `ground_truth.assessment.required_recommendations[4]`; securing pearl replaced (`key_clinical_evidence[8]`). New recommended DSA criterion `dsa-aneurysm-anatomy` with a diagnostic DSA follow-up (`followup_outputs[2]`, trigger `request_digital_subtraction_angiography`). Timeline: TCD re-dated from "Day 8" to an admission baseline (day 0) so no result post-dates an unsecured aneurysm. |
| da99e9e0-0194-487a-a95b-b5f6d7a2e536 | ALREADY-FIXED (must present), wording FIXED | The EVD must already existed; reworded as MUST-EVD-NOW "for the acute hydrocephalus with intraventricular blood and depressed consciousness [Hoh_2023]; reverse the anticoagulant first" (`required_recommendations[3]`), placed after the reversal must. |
| 75c2bb0f-fd1a-4ccc-ab01-a8b09d8dad66 | ALREADY-FIXED | Nimodipine must was present; replaced by the canonical MUST-NIMO wording (enteral 60 mg every 4 h for 21 days; 30 mg every 2 h if hypotension) in `required_recommendations[5]`. |
| b12f861e-6d6b-47f7-aba0-5f0ebb66dc8f | FIXED | MUST-BP-A with "nicardipine or clevidipine infusion" (labetalol not first choice with LVEF 35%) in `required_recommendations[7]`; SBP below 160 mmHg stated as the common target [Connolly_2012], no numeric target in [Hoh_2023]. The SBP target removed from the ICU must; BP prohibition replaced by the canonical text. MUST-HOME withholds amlodipine. |
| 9d172604-37fd-470f-9bc1-d74ccb0abb83 | FIXED | `ground_truth.avoided_actions` `avoid-harm-1-analyze-csf` severity `harm` to `contraindicated`, rationale names intraventricular blood and hydrocephalus. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status` | "Alert and oriented x4" next to GCS 14 with confusion and a Hunt-Hess 3 label. | FIXED: "Confused, GCS 14 (E4V4M6), not oriented to date; photophobic; significant pain" (C13). |
| E | minor | `patient.history_present_illness` | "briefly lost responsiveness for approximately 45 seconds and became unresponsive" (duplicated meaning). | FIXED: "became unresponsive for approximately 45 seconds". |
| D | major | `initial_tool_outputs.drug_interactions` | Empty `general` block whose summary is the drug criterion's expected evidence (C8). | FIXED: block deleted; the nimodipine check is answered by a new follow-up `request_nimodipine_interaction_check` with the real interactions (amlodipine, metoprolol, rosuvastatin, apixaban). |
| C | blocker | `followup_outputs` apixaban reversal | "This patient took apixaban 6 hours ago - high-dose protocol indicated": wrong for a 5 mg dose (US label: low dose when the last dose is 5 mg or less, whatever the timing); infusion totals stated instead of rates. | FIXED: label dosing for both regimens, heparin resistance and thrombotic warnings, 4F-PCC 50 IU/kg alternative; no patient-specific verdict. |
| A | major | `ground_truth.action_criteria` | No reversal criterion although reversal is the pivot of the case; drug check recommended with a template expected evidence. | FIXED: new required `check-apixaban-reversal` (`drug: apixaban`, answered by `request_apixaban_reversal`); nimodipine check `required` (dihydropyridine with nimodipine, C10) with case-specific rationale and evidence. |
| D | major | CTA `additional_observations` | "IV contrast CTA after anticoagulation reversal": reports management the agent has not recommended (C2). | FIXED: removed. Added "Cervical carotid and vertebral arteries: No dissection, stenosis or occlusion" so the differential's dissection statement rests on a result. |
| D | minor | CT `additional_observations` | "Anticoagulation may have contributed to hemorrhage severity" (cross-modality). | FIXED: removed. |
| B | major | TCD follow-up | Day 8 study with moderate basilar vasospasm, in a patient who arrived 3 hours after ictus; protocol named MCA only though basilar was reported. | FIXED: admission baseline, post-ictus day 0, normal velocities (MCA 64/59 cm/s, Lindegaard 1.9/1.7), canonical protocol and recommendation. |
| C | major | telemetry follow-up | Template "Sinus rhythm ... rare malignant arrhythmias warrant intervention" in a patient in AF; 24 h duration impossible at assessment. | FIXED: 4 h since arrival, rate-controlled AF 71 to 104/min, 38 isolated PVCs, no sustained arrhythmia or pauses, QTc 508 ms on monitoring leads; criterion evidence updated. |
| D | minor | `fallback_tool_outputs.cardiac_monitoring` | "consistent with known AF on rate-control therapy", "Known AF on metoprolol; no new arrhythmias requiring additional intervention" (cross-reference and management wording). | FIXED: rhythm-only wording. |
| C | major | labs | No magnesium with QTc 508 ms; anti-Xa reference "Trough <50 ng/mL for afib (on medication)" (186 ng/mL at 6 h is within the expected apixaban on-therapy range; the clinically useful reference is the threshold for a relevant drug effect); abnormal summary omitted WBC and glucose. | FIXED: magnesium 1.9 mg/dL added to BMP; anti-Xa reference "<30"; summary lists all six abnormal values; type and screen `clinical_significance` null. |
| C | major | musts | No K/Mg action with QTc 508 ms and K 3.8; no action for LVEF 35%; home amlodipine and metoprolol not addressed; generic "PCC, andexanet alfa, idarucizumab, or vitamin K" reversal must; TCD "days 4-14" must. | FIXED: MUST-REVERSE (low dose), MUST-QT, MUST-LVEF, MUST-HOME, MUST-ICU, MUST-DCI replace the template entries. |
| C | major | literature follow-up | "AHA/ASA 2023: anticoagulation delayed minimum 4 weeks" (unverifiable attribution); literature as a recommended step. | FIXED: follow-up deleted; criterion `optional`, last; canonical literature output last in the list. Restart timing now sits in MUST-REVERSE (decided with neurosurgery and cardiology after securing). |
| B | minor | echo follow-up | "Cardiology consultation ... recommended" phrased as an order; no `echo_type`; en dash. | FIXED: "Consider cardiology consultation; repeat echocardiogram in 4 to 6 weeks"; `echo_type` TTE. |
| C | minor | `ground_truth.differential` | Template key features ("pituitary MRI / CT without sellar enlargement excludes", "CT venogram ... indicated if SAH excluded"). | FIXED: C11 key features citing this case's CT and CTA. Pituitary entry says "no ocular motor deficit" without visual fields, because the exam documents eye movements but not fields. |
| A | minor | criteria `citations`, `rationale` | Free-text citation strings next to bracketed keys; `[Connolly_2012]` for ECG, echo, telemetry; rationales copied from labels. | FIXED: one bracketed key per criterion per plan 1.3; rationales per 1.3. |
| B | minor | `ground_truth.stop_rule`, `sequence_constraints` | Stop rule omitted required work and allowed 0 extra actions; no constraints. | FIXED: stop rule = the six required criteria, `max_additional_actions` 1; constraints NCCT before CTA (soft), CTA before DSA (soft), reversal check before DSA (hard). |
| E | minor | `metadata.case_body_concerns`, `metadata.difficulty_rationale` | Stale CSF concern (no CSF block exists); template difficulty text ("or sentinel-bleed framing + age", "3 or more red herrings" with one red herring). | FIXED: concerns emptied; case-specific difficulty rationale. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway now reads NCCT, labs, ECG, CTA, the apixaban reversal check, catheter DSA, the nimodipine interaction check, echo, telemetry, then optional TCD and literature. The exam matches Hunt-Hess 3 (confused, GCS 14). The reversal check gives the US label rule, which assigns the low-dose andexanet regimen to his 5 mg dose, with 4F-PCC 50 IU/kg as alternative and the heparin-resistance warning; a hard constraint puts it before the DSA. The DSA is a diagnostic report (7.3 x 6.8 mm basilar apex aneurysm, neck 4.2 mm, dome-to-neck 1.7, both P1 origins at the neck margin, no second aneurysm, no vasospasm), with no treatment content. The TCD is an admission baseline (day 0, normal), and telemetry reports 4 hours of rate-controlled AF with QTc 508 ms. Labs now include magnesium 1.9 mg/dL. The musts are: NCCT; CTA; low-dose andexanet or 4F-PCC with apixaban stopped; EVD after reversal; securing as early as feasible, preferably within 24 hours, after reversal; nimodipine; neuro-ICU; nicardipine or clevidipine for BP 196/118 (LVEF 35%); withholding amlodipine while continuing metoprolol for rate control; potassium and magnesium repletion with ECG monitoring for QTc 508 ms; cardiology and neuroanesthesia input for LVEF 35%; sodium; and DCI surveillance. LP is `contraindicated`. The IV nimodipine and BP prohibitions use the corrected wording.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Drew_2010]` and `[Molyneux_2002]` (in MUST-QT and the canonical literature output) need the criteria-pack allow-list (plan section 5.1).
- Review UI: show the initial work-up in criterion order (plan 5.5).

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case. Plan section 6 questions 1 (EVD) and 2 (DSA tier) apply; here the EVD is indicated anyway (IVH with GCS 14).

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan entries (C1 to C14, section 4 M07) and the whole final case.

Checked: all five note ids are in the table and each ruling holds against the file (single MUST-SECURE with the Hoh window "after anticoagulant reversal"; MUST-EVD-NOW with reversal first; MUST-NIMO; MUST-BP-A with nicardipine or clevidipine for LVEF 35%; LP avoided action `contraindicated`). Reversal content matches the US andexanet label for a 5 mg dose taken about 6 h before arrival (low dose), with PCC 50 IU/kg and heparin resistance; HPI timing (last dose 8 AM, about 6 h) agrees with the must and the criterion rationale. Hard constraint reversal before DSA exists; stop rule = the six required criteria. CTA, DSA (7.4 vs 7.3 mm, neck 4.2 mm), telemetry (AF, QTc 508 ms) and ECG agree; magnesium 1.9 within range and MUST-QT target 2.0 consistent; anti-Xa flag consistent with its reference; no initial drug or literature block; leak guards pass; differential low after CTA (cervical arteries reported clear).

Found and fixed: HPI still said "He is now alert but continues to complain..." after the exam was corrected to confused, GCS 14 (Hunt-Hess 3); changed to "He is now awake but confused and continues to complain..." (`patient.history_present_illness`).

Left as is (noted): the `fallback_tool_outputs.cardiac_monitoring` block is a 24 h Holter, which could not exist at assessment time if an agent orders a Holter instead of telemetry; it is an off-pathway fallback shared by the condition, so it is not changed here.

Re-ran `perfect_agent.py SAH-M07 -v` (pass) and `case_io.py check` (no failure names the case); case guards pass.
