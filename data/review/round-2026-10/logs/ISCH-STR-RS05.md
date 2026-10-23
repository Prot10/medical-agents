# ISCH-STR-RS05
Reviewer status: R1 none, R2 approved | Approved before this round: yes

Approved case: every change below corrects an error (R2's two notes, or a defect class the plan assigns to all 30 cases); the story, the diagnosis, the thrombolysis-plus-thrombectomy decision and correct prose were left alone.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| c0233fc3-10d0-46d5-91ba-861dbe98095c | FIXED | Canonical C4 BP must (`ground_truth.assessment.required_recommendations[2]`): lower 188/104 mmHg below 185/110 with IV labetalol or nicardipine before thrombolysis, then below 180/105 for 24 hours. Decision must (`[1]`) gives IVT "once blood pressure is below 185/110 mmHg"; prohibition "Do not give IV thrombolysis while blood pressure is above 185/110 mmHg"; `key_clinical_evidence[0]`. |
| de5e529f-2a92-4c72-88b5-2317a5893d94 | FIXED | NIHSS 12 as the reviewer counted: `patient.neurological_exam.additional` itemised "NIHSS 12 (gaze 1, facial palsy 2, left arm 3, left leg 3, sensory 1, extinction and inattention 2; limb ataxia not testable on the left, scored 0)". Exam made explicit so the items are scoreable: visual fields full to single stimuli, extinction on double simultaneous stimulation, near-complete lower facial paralysis, leg falls immediately, orientation to month and age. All NIHSS mentions (musts, key evidence) say 12; thrombectomy eligibility unchanged. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.mri.findings[0].signal_characteristics`, `.mass_effect`, `.impression` | FLAIR "consistent with onset greater than 3 hours", T1 hypointensity, sulcal effacement and ventricular compression at 38 minutes from onset (C12). | FIXED: DWI-FLAIR mismatch, no T1 change, subtle T2 change, no significant mass effect; numbered impression. |
| B | minor | `initial_tool_outputs.mri.additional_observations` | "No leptomeningeal enhancement" in a report served for the non-contrast criterion. | FIXED: line removed. |
| B | major | `initial_tool_outputs.ct` | Internal contradiction: findings said "No definite early ischemic parenchymal changes" while the observations gave ASPECTS 9 for an M6 hypodensity, and M6 was placed in "posterior frontal cortex" (M6 is the posterior superior, parietal, region). | FIXED: early change is a subtle loss of the right insular ribbon (insula is in the DWI lesion); "ASPECTS 9 (point lost for the insular ribbon)"; numbered impression. ASPECTS value unchanged. |
| B | minor | `patient.neurological_exam.mental_status` | "Mildly inattentive" on the strength of one error on serial 7s (one error is normal; plan class from M05 b36e42fb). | FIXED: "Attention adequate, one error on serial 7s." |
| B | minor | `patient.clinical_history.past_medical_history[5]`, `ground_truth.key_clinical_evidence[8]` | The MRI shows an old right basal ganglia lacune while the history says "No prior stroke or TIA" (class of RS01 note eea99434). | FIXED: "No known prior stroke or TIA"; pearl that the lacune is a previous silent infarct, making this event a recurrence. No prior imaging was invented. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts: generic NCCT-first and glucose musts, "thrombectomy evaluation" rather than a decision, "24-hour Holter and prolonged monitoring" in a determined large-artery mechanism, troponin conclusion resting on a repeat value from a follow-up the plan removes, statin without dose, no antiplatelet plan for symptomatic ICAD, no smoking cessation (C2, C4, C6, C14). | FIXED: LKW/NIHSS, decision (IVT after BP control, EVT without waiting), BP, dose and door-to-needle, EVT procedure with the ICAD warning and post-recanalization floor, lisinopril angioedema watch, stroke unit telemetry, canonical troponin must, antiplatelet pause then aspirin plus clopidogrel for 90 days (SAMMPRIS) with cardiology review, atorvastatin 80 mg plus ezetimibe if needed, long-term BP, diabetes and smoking cessation. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "Below 140/90" prohibition in a case that receives IVT and EVT (C5); "AHA/ASA 2019" contraindication text; DAPT prohibition phrased so that it conflicted with the 24-hour post-thrombolysis antiplatelet pause. | FIXED: 140/90 removed; generic contraindication without the 2019 year; BP, antiplatelet-not-a-contraindication and thrombectomy-delay prohibitions added; antiplatelet prohibition rewritten around the 24-hour pause. |
| C | major | `ground_truth.differential[0]`, `[1]` | Occult AF left "moderate" after ECG, Holter, TTE and CTA showing ICAD at the occlusion (ruling 7); artery-to-artery entry cited a "carotid duplex" that the case does not contain. | FIXED: cardioembolism low with the excluding data; artery-to-artery entry cites the CTA. |
| B | minor | removed `followup_outputs` "request_lipid_hba1c_labs" | Lipid and HbA1c duplicated the admission bloods (C9), plus a 4-hour troponin with interpretive flags; received by no criterion. | FIXED: deleted; targets in the musts; troponin repeat is a must. |
| C | minor | `followup_outputs[1]` (drug check), criterion `action-7-check-drug-interactions` | `contraindications` field listed non-contraindications; "per AHA/ASA 2019"; "Metformin: hold if contrast studies anticipated" is wrong at creatinine 1.1 (C7). Required in a case without a contraindication. | FIXED: contraindications empty (none present); interactions and warnings restate aspirin, clopidogrel and lisinopril correctly, metformin need not be withheld; criterion recommended and placed after the CTA (it informs IVT monitoring). |
| B | minor | `followup_outputs[2]` (TTE) | Impression called LVEF 50 percent both "mildly reduced" and "at the lower limit of normal"; LAVI without unit; no `echo_type`; criterion expected evidence attributed the EF to "demand/neurogenic injury" (synthesis). | FIXED: LVEF 50 percent mildly reduced; LAVI 34 mL/m2 (normal); numbered impression; `tool_parameters.echo_type` TTE; criterion recommended with factual expected evidence. |
| D | minor | `followup_outputs[3]` (Holter) | No admission timing (C2); heart-rate range average only; criterion said "supports ICAD as primary mechanism". | FIXED: "Recorded on the stroke unit after admission, 24 hours."; min 54, max 106; `tool_parameters.monitor_type` holter_24h; alternatives holter_24h, holter_48h, telemetry; recommended. |
| C | major | `followup_outputs[4]` (literature), criterion `action-6-search-medical-literature` | Recommended literature step (ruling 5); superseded AHA/ASA 2019 entry; "Liebeskind DS, Prevalence and mechanisms of stroke in intracranial atherosclerotic disease, Stroke 2011" could not be verified. | FIXED: SAMMPRIS (Chimowitz, NEJM 2011), its final results (Derdeyn, Lancet 2014) and Banerjee and Chimowitz (Circ Res 2017); general summary. Criterion optional, last, `required_arguments` {}. |
| E | minor | `ground_truth.key_clinical_evidence` | Three "Off-pathway modality" lines, the July 2026 tier line, a pearl recommending 30-day monitoring in a determined mechanism, "ICAD is the most common cause of ischemic stroke globally" (overstated), "flat serial troponins" from a removed result (C17). | FIXED: window and EVT pearls added; ICAD and troponin pearls corrected; SAMMPRIS and silent-infarct pearls; localisation, TOAST and AHA/ASA 2026 sequencing lines kept. Red herring interpretation no longer cites the removed serial troponin. |
| A | minor | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule`, `avoided_actions` | CTA last after echo, Holter, literature, drug check and labs (C1); labels equal rationales; `[AHA_ASA_2019]`, `[Sanna_2014]`, doubled and free-text citations; echo, Holter and drug check required; hard NCCT-to-drug-check constraint; allowance 0. | FIXED: order NCCT, labs, ECG, CTA, MRI (optional), drug check, echo, monitoring (recommended), literature (optional); ids kept; distinct labels and rationales; soft NCCT before CTA, CTA before echo and monitoring; stop rule NCCT, labs, ECG, CTA; allowance 1; avoided actions recited with the 2026 key. |
| E | minor | `initial_tool_outputs.labs.abnormal_values_summary` | Interpretive flags ("elevated despite statin", "suboptimally controlled diabetes"). | FIXED: factual flags, values unchanged. |

## Changes, in one paragraph a physician can read before re-reviewing

The story is unchanged: a 63-year-old man on aspirin and clopidogrel for three-vessel coronary disease, last known well 14:20, arriving at 14:58 with a right M1 near-occlusion on intracranial atherosclerosis. The exam now sums to NIHSS 12 item by item, as R2 counted, and the history says no known prior stroke while the MRI's old lacune is named as a silent infarct. The CT no longer contradicts itself (ASPECTS 9 from a subtle insular ribbon loss), and the MRI shows a hyperacute infarct (no FLAIR change) as expected at under an hour, without a contrast observation. The work-up reads NCCT, labs, ECG, CTA, then the thrombolysis drug check, TTE and monitoring (recommended) and an optional ICAD literature search with verifiable references; the duplicate lipid and HbA1c panel is gone. The musts now lower 188/104 below 185/110 before thrombolysis, give IVT and proceed to thrombectomy without waiting, warn the interventional team about the underlying stenosis, watch for ACE-inhibitor angioedema, repeat the troponin, and plan secondary prevention: no antiplatelet for 24 hours, then aspirin plus clopidogrel for 90 days per SAMMPRIS, atorvastatin 80 mg, and blood pressure, diabetes and smoking control.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms appended to `accepted` include "embolic stroke", "cardioembolic stroke", "lacunar stroke" and "lacunar infarct" for a large-artery intracranial atherosclerotic stroke (plan section 5.3 owner).
- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- The DWI lesion (operculum, insula, lenticular nucleus, corona radiata, internal capsule, 5.4 x 3.9 cm) is large for under an hour against a CT ASPECTS of 9. It is possible with poor collaterals and does not change the thrombectomy indication, so I left its extent unchanged; a reviewer may prefer a smaller lesion.
- Antiplatelet after thrombectomy assumes no intracranial stent is placed; if the interventionalist stents the stenosis, the regimen follows the procedure.

## Verification
Adversarial verifier, 23 October 2026. Approved case: read the log, the diff and the whole final case.
- Notes: c0233fc3 (BP below 185/110 before IVT with labetalol or nicardipine, then below 180/105; matching prohibition) and de5e529f (NIHSS 12 itemised as R2 counted) FIXED as logged. No note missing.
- NIHSS 12 recounted from the exam (gaze 1, face 2 near-complete lower facial paralysis, arm 3 and leg 3 falling immediately, sensory 1, extinction 2 in visual and tactile modalities plus neglect; 1b 0); all mentions say 12. CT ASPECTS 9 now internally consistent (insular ribbon), MRI FLAIR negative at 38 minutes, CTA contrast true and impression opens with the M1 near-occlusion. Decision must values (glucose 168, INR 1.0, platelets 242) match the labs; troponin 0.08 must matches the lab row; SAMMPRIS (NEJM 2011), Derdeyn (Lancet 2014) and Banerjee and Chimowitz (Circ Res 2017) are correct. Changes are limited to the plan's error classes; no prose churn found beyond them.
- Found nothing that needed changing. perfect_agent and case_io check clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "embolic stroke", "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.4, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.51
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TTE" to the stored echocardiogram report (the schema now keeps the field and the MockServer routes TTE/TEE/bubble orders by it; the value was only in `tool_parameters`).
- MRI: the 5.4 x 3.9 cm confluent lesion at 38 minutes made patchy (largest focus 2.6 x 1.8 cm) and T2 set to no definite abnormality, consistent with ASPECTS 9 on NCCT (decision OQ8c).
