# ISCH-STR-S05
Reviewer status: R1 none, R2 approved | Approved before this round: yes

Approved case: changes are limited to the two notes, plan classes that correct real errors (pathway order, leakage, guideline, BP and decision musts, the 140/90 prohibition) and three factual errors found on reading (ASPECTS arithmetic, a carotid duplex that does not exist, a laboratory interpretation that cites the history). Correct prose was left as written.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 9802d420-6264-4e63-80cb-54241623d298 | FIXED | `patient.neurological_exam.additional`: "NIHSS score: 13 (LOC questions 1, best gaze 1, facial palsy 2, left arm motor 3, left leg motor 3, sensory 1, extinction and inattention 2)"; the visual point moved to item 11, arms and legs 3, sensory 1 added, as the reviewer counted. 13 repeated in the LKW must, the decision must and `key_clinical_evidence[2]` and `[6]`. |
| c9b7c467-714d-4750-9306-097c63dbce7a | FIXED | `initial_tool_outputs.mri.findings[0].signal_characteristics.FLAIR`: "Faint FLAIR hyperintensity in the right lentiform nucleus only, much less conspicuous than the DWI lesion; no corresponding cortical FLAIR change" (matches the CT lentiform hypodensity at 2 h 58); T1 without definite change, T2 subtle lentiform hyperintensity only, `mass_effect` "No mass effect" (as on CT). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs` order, `ground_truth.action_criteria` order | Echo, Holter, literature and drug check before the CTA (C1). | FIXED: follow-ups CTA, drug review, TTE, Holter, literature; criteria NCCT, labs, ECG, CTA, MRI (optional), drug review, echo, monitoring, literature. Ids kept. |
| D | major | `patient.history_present_illness` | "placing her within the standard IV alteplase window" (C10). | FIXED: removed; times kept. |
| B | major | `initial_tool_outputs.ct.findings[0].description`, `.impression` | ASPECTS 7 with early change in two regions only (insula, lentiform nucleus): 10 - 2 = 8. | FIXED: ASPECTS 8 in the report, the decision must and key evidence. |
| D | minor | `initial_tool_outputs.labs.interpretation` | "INR 1.0, patient not on anticoagulation" cites the history inside a lab report. | FIXED: plain recital of abnormal values. |
| C | major | `ground_truth.assessment.required_recommendations` | No explicit decision; thrombectomy justified "up to 24h per DAWN/DEFUSE-3" in a patient at 2 h 58; "outside tPA window maintain permissive hypertension" in a patient who is treated; generic DOAC timing (C4, C6). | FIXED: LKW (2 h 58) and NIHSS 13; decision must (IVT after BP lowering, EVT for the right M1 occlusion within 6 hours, ASPECTS 8, no waiting); door-to-needle; canonical BP must naming 188/104 and the post-recanalization floor; angioedema must kept; glucose must kept; stroke unit telemetry; apixaban 5 mg twice daily on day 6 to 7 (major infarct by ELAN: cortical plus deep MCA branches), CHA2DS2-VASc 6, HAS-BLED 3, no bridge, stop aspirin. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "below 140/90" (C5); vague anticoagulation prohibition. | FIXED: removed; anticoagulation timing prohibition per ELAN and no heparin bridge; "Do not delay thrombectomy to observe the response to IV thrombolysis" added. Other prohibitions kept as written. |
| B | minor | `ground_truth.differential[0]`, `key_clinical_evidence[1]` | Cite a "bilateral carotid duplex" that the case does not contain. | FIXED: "CTA shows under 30% carotid stenosis". |
| C | minor | `ground_truth.key_clinical_evidence[2]`, `[4]`, `[6]` | Thrombectomy framed by DAWN/DEFUSE 3; an unsourced "2-5 fold" angioedema risk; engineering "Tier per the July 2026 clinical review" line. | FIXED: 0 to 6 hour criteria; risk stated without a number; NIHSS itemisation replaces the engineering line. |
| D | minor | `followup_outputs[3]` (Holter) | "Adequately controlled" judgment; no admission timing (C2). | FIXED: opens "Recorded on the stroke unit after admission, 24 hours."; burden and rates; `tool_parameters.monitor_type` holter_24h; alternatives holter_24h, holter_48h, telemetry. |
| B | minor | `followup_outputs[1]` (drug review) | `contraindications` listed absent contraindications (and lab values); proposed "Alteplase (tPA)". | FIXED: contraindications hold only the BP threshold; the negatives moved to a warning without lab values; formulary text and alternatives without dashes. Criterion recommended (C7). |
| C | minor | `followup_outputs[4]` (literature) | First result was the 2019 guideline with "thrombectomy for LVO within 24 hours" as a blanket statement; query named 2019. | FIXED: the 2026 guideline entry (0 to 6 hours criteria, DAWN/DEFUSE 3 to 24 hours); DAWN, DEFUSE 3 and TOAST entries kept. Criterion optional, last, `required_arguments` {}. |
| A | minor | criteria labels, citations, constraints, stop rule | Label = rationale, duplicate `[AHA_ASA_2019]`, free-text citation, hard template constraint, allowance 0 (C17, 3.3, 3.4). | FIXED: distinct rationales, case-specific evidence, `[AHA_ASA_Stroke_2026]` (avoided actions too); soft constraints; stop rule NCCT, labs, ECG, CTA; allowance 1. |
| B | minor | `followup_outputs[2]` (TTE) | No `echo_type`. | FIXED: `tool_parameters.echo_type` TTE; report unchanged (it was already a real impression). |

## Changes, in one paragraph a physician can read before re-reviewing

The clinical story is unchanged (74-year-old woman, new AF, right M1 occlusion with left hemiplegia, neglect and anosognosia at 2 hours 58 minutes, BP 188/104). The NIHSS is 13 as R2 counted, the MRI FLAIR is now faint and limited to the lentiform nucleus (in keeping with the CT), and the CT ASPECTS is 8 (two regions affected). The HPI no longer states eligibility. The work-up runs NCCT, labs, ECG, CTA, then the drug review, echo and monitoring; literature is optional. The musts now state the decision: lower BP below 185/110, give IV thrombolysis, and proceed to thrombectomy for the M1 occlusion within 6 hours without waiting; angioedema watch for lisinopril, stroke-unit telemetry, and apixaban 5 mg twice daily on day 6 to 7 with aspirin stopped. The 140/90 prohibition is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[AHA_ASA_Stroke_2026]` used throughout (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- NIHSS item 3: the official instructions score visual extinction 1 on item 3 as well as on item 11; R2's note counts it on item 11 only. I followed R2 (13); with the official convention the total is 14, which was the printed value.
- HAS-BLED 3 counts prior stroke, age and aspirin; her hypertension is "variably controlled" and 188/104 in the acute phase, which some would score as uncontrolled (4). It does not change the decision.

## Verification
Adversarial verifier, 23 October 2026. Approved case: read the log, the patient-block diff against HEAD and the whole final case.

Checked: note 9802d420 (NIHSS 13 itemised exactly as R2 counted; LOC questions 1 from "not to date" kept as R2 scored it; 13 repeated in the LKW must, the decision must and key evidence), note c9b7c467 (FLAIR faint and limited to the lentiform nucleus at 2 h 58, consistent with the CT); the only patient-block changes are the HPI eligibility verdict and the NIHSS line; ASPECTS 8 is correct for two affected regions (insula, lentiform) and repeated consistently; the BP must names 188/104; CHA2DS2-VASc 6 (hypertension, age 65 to 74, diabetes, stroke 2, female sex); thrombectomy framed on 0 to 6 hour criteria; prohibitions consistent with the musts; no rate-control or troponin must needed (88 to 92 bpm, troponin 0.03 normal).

Found and fixed:
- `required_recommendations[7]`: "HAS-BLED 3 for prior stroke" contradicted `past_medical_history[5]` "No prior stroke or TIA". Now "for this stroke" (the index stroke is the HAS-BLED S item).

Left as written (approved case, no error): pre-existing em dashes in the echo impression, key evidence and red herrings. `perfect_agent.py -v` passes; `case_io.py check` is clean for this case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.5, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.41
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TTE" to the stored echocardiogram report (the schema now keeps the field and the MockServer routes TTE/TEE/bubble orders by it; the value was only in `tool_parameters`).
- NIHSS recounted by the official item 3 rule: 13 to 14 in the exam, key evidence and both musts; R2's count (note 9802d420) is DECLINED on this point with the NINDS NIHSS item 3 instruction; no decision changes (decision OQ1).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
