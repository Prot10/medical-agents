# ISCH-STR-M03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 5e0dbec2-ea6c-4420-9b68-5b07c716b8ee | FIXED | CTP follow-up (`followup_outputs[1]`) impression no longer cites the 1.8 thrombectomy-trial threshold; numbered impression with core 18 mL, Tmax above 6 s 26 mL, mismatch 8 mL, ratio 1.4 and `quantitative_data` filled. CTP criterion `action-5-order-advanced-imaging` made recommended, expected evidence states the EXTEND limb (ratio met, mismatch volume fails). Decision must, wake-up prohibition, key evidence (C3 canonical) and pearl 1 restated on the EXTEND limb; the drug-check text "ratio 1.4 below DAWN/DEFUSE-3 threshold" removed with the whole alteplase checklist. The literature summary now states that 1.8/15 mL belongs to DEFUSE 3 and TIMELESS. |
| 55291633-d7b2-4e6a-8497-235e3aa19058 | FIXED | Sodium 151 changed to 137 (normal), so the anion gap is 137 - 101 - 24 = 12 (plan C14: the hypernatraemia had no story and no action). Hyperglycaemia (237 mg/dL, HbA1c 9.0%) now has a must (140-180 mg/dL in the first 24 h). |
| d1ad43a9-a011-45bc-ae0f-0c7d77da43ba | FIXED | NIHSS recounted to 9 (questions 1 for the wrong month, visual 1 for visual extinction, facial 1, right arm 1, sensory 1, language 1, dysarthria 1, extinction 2 for visual plus tactile). Exam made scorable: "Alert but mildly drowsy" became "Alert", arm drift and leg without drift stated, past-pointing in proportion to weakness (ataxia 0), age correct. Total updated in LKW must and key evidence. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | "This exceeds the standard 4.5-hour window for IV thrombolysis and complicates acute management decisions." (eligibility verdict). | FIXED: sentence removed, times kept. |
| D | major | `initial_tool_outputs.ct` | NCCT template management text. | FIXED: canonical normal impression, ASPECTS 10, hyperdense vessel sign negative. |
| B | major | `followup_outputs[0]` (CTA) | `contrast_used` false; impression recommended "medical optimization versus carotid intervention" (management). | FIXED: contrast true; numbered impression opening with the M2 finding, then no LVO, 55-60% left ICA, mild intracranial atherosclerosis. |
| B | major | `initial_tool_outputs.mri.findings[0].size` | 2.8 x 1.9 cm (the M01 template size) cannot hold an 18 mL CTP core. | FIXED: 4.0 x 2.5 cm axial, 3.5 cm craniocaudal (about 18 mL); impression numbered and gives the size. |
| B | major | `initial_tool_outputs.labs.panels.CBC` | Hb 12.6 with Hct 39.8 and RBC 4.5 x MCV 78 = 35.1: indices inconsistent. | FIXED: Hct 37.8 (L), RBC 4.85; MCV 78 kept. |
| C | major | labs, assessment | Microcytic anaemia (Hb 12.6, MCV 78) in a 73-year-old man about to be anticoagulated, with no action. | FIXED: must for iron studies and GI evaluation; drug check warns; HAS-BLED counts it. |
| B | minor | `initial_tool_outputs.labs` eGFR | eGFR 52 with creatinine 1.5 at 73 years (CKD-EPI 2021 about 49). | FIXED: 49. |
| E | minor | `patient.clinical_history.past_medical_history[5]`, `metadata.case_body_concerns` | "Obesity (BMI 31.2)" against BMI 29.8 (copied from M01). | FIXED: "Overweight (BMI 29.8)"; concern list emptied. |
| C | major | `followup_outputs[4]` (drug check) and criterion `action-8` | An alteplase checklist for a patient who cannot receive alteplase, whose contraindications and alternatives stated the case's reperfusion answer; required argument `drug: alteplase`. | FIXED: replaced by the apixaban check (aspirin stop, dose rationale, anaemia and NSAID warnings); trigger renamed `check_drug_interactions_anticoagulation`; criterion recommended (plan C7) with `{}` arguments, placed after monitoring with a soft constraint. |
| B | minor | echo, Holter | "Abnormal values: ... (H)" echo impression; interpretive "atrial substrate disease" in the Holter. | FIXED: real TTE impression and `tool_parameters`; Holter impression opens "Recorded on the stroke unit after admission, 24 hours.", quantitative, no interpretation. |
| C | major | literature output | 2019 guideline cited; one-limb summary. | FIXED: WAKE-UP, EXTEND, AHA/ASA 2026; criterion optional, `{}` arguments, last. |
| C | major | `followup_outputs` (hypercoagulability) | Orphan thrombophilia panel in a 73-year-old with AF. | FIXED: removed (C9). |
| C | major | `ground_truth.assessment` | Template musts (door-to-needle, pre-IVT BP, generic prevention); 140/90 prohibition; large-infarct anticoagulation prohibition with a moderate infarct; no statement on the ipsilateral 55-60% stenosis. | FIXED: LKW/NIHSS, decision, telemetry, apixaban within 48 h with aspirin stopped (CHA2DS2-VASc 5, HAS-BLED 4 after aspirin), medical management of the stenosis with the reason, ezetimibe added for LDL 126, glucose 140-180, anaemia work-up, risk factors with antihypertensives resumed after 48 to 72 h; C5 canonical prohibition; wake-up prohibition on the EXTEND limb. |
| C | minor | `ground_truth.differential` | Large-artery "moderate" after Holter shows a 14.6% AF burden. | FIXED: low, with the reason; small-vessel and metabolic entries cite the results. |
| E | minor | `ground_truth.key_clinical_evidence` | Off-pathway lines x3 and July 2026 tier line. | FIXED: removed; NIHSS, C3, Holter with scores and the stenosis statement added. |
| A | minor | criteria, avoided actions | Free-text citation, duplicate and superseded keys; labels identical to rationales. | FIXED. |
| B | minor | ECG, echo, Holter PAC count | Template values shared with M01 and M02 (ECG intervals, LAVI 36, 847 PACs). | FLAGGED: plausible, left unchanged to avoid churn. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway now runs NCCT, labs, ECG, CTA, CT perfusion (recommended), optional MRI, TTE and 24-hour Holter (both required), then the apixaban check (recommended) and an optional literature output; the thrombophilia panel is gone. The thrombolysis decision is stated on the limb that applies: FLAIR is positive, he woke 5 h 20 min after the sleep midpoint, there is no LVO, and CTP (core 18 mL, Tmax 26 mL) meets the 1.2 ratio but not the 10 mL mismatch volume, so no IVT; no EVT. The HPI verdict, the NCCT management text and the CTA management sentence are gone; the CTA reports contrast. Sodium is now 137 (gap 12), Hct and RBC agree with Hb 12.6 and MCV 78, eGFR 49, and the MRI infarct size matches the 18 mL core. NIHSS recounted to 9. Musts: LKW and NIHSS, explicit decision, telemetry, apixaban 5 mg twice daily within 48 h with aspirin stopped, medical management of the ipsilateral 55-60% ICA stenosis because the mechanism is cardioembolic, ezetimibe for LDL 126, glucose 140-180 mg/dL, work-up of the microcytic anaemia before long-term anticoagulation, and risk-factor control. The BMI copy error is corrected.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` for the criteria-pack allow-list (plan 5.1).
- Review UI: initial work-up shown as numbered steps in criterion order (plan 5.2).
- `accepted[0]` contains an em dash; left untouched per ruling 3.

## Open questions for Andrea (judgment calls you could not settle)

- Plan open question: the 55-60% ipsilateral ICA stenosis is managed medically because AF with a 14.6% burden is taken as the mechanism. Some vascular neurologists would still offer endarterectomy for a symptomatic 50-69% stenosis in a man; please confirm with R2.
- NIHSS item 3 scored 1 for visual extinction (NIHSS instruction) in addition to item 11; without it the total is 8.
- The microcytic anaemia was kept and given an action rather than normalised; if you prefer a cleaner case, the MCV can be set to normal and the anaemia must removed.

## Verification
Adversarial verifier, 23 October 2026. Checked: all 3 note ids in the table; CTP impression and decision stated on the EXTEND limb (ratio 1.4 above 1.2, mismatch 8 mL below 10 mL), 1.8 appears only in the literature summary attributed to DEFUSE 3 and TIMELESS; sodium 137 gives gap 12; NIHSS 9 recounted from the final exam (questions 1, visual 1, face 1, arm 1, leg 0 without drift, sensory 1, language 1, dysarthria 1, extinction 2). Cross-field: MRI 4.0 x 2.5 x 3.5 cm ellipsoid is about 18 mL, matching the CTP core; Hct, RBC and MCV agree; eGFR 49 by CKD-EPI 2021; CHA2DS2-VASc 5 and HAS-BLED 5/4 (anaemia counted) recomputed; sleep midpoint about 02:50 and 5 h 20 min; NSAID intolerance consistent with the drug check; echo and Holter required, drug check recommended per plan.
Found and changed: the apixaban must started anticoagulation "within 48 hours, since the infarct is moderate in size". The infarct is about 18 mL across posterior frontal and parietal cortex, i.e. more than one cortical branch of the superior division, which is the ELAN major category (DOAC on day 6 to 7). `ground_truth.assessment.required_recommendations` (apixaban must) now reads "on day 6 to 7 once follow-up imaging excludes hemorrhagic transformation, since the infarct (about 18 mL, posterior frontal and parietal cortex) spans more than one cortical branch of the superior division, the ELAN major category". OPTIMAS would also support starting by day 4; if R2 prefers that, the must can say so. Noted, not changed: the label calls the mechanism cardioembolic although TOAST would class AF plus an ipsilateral 55-60% stenosis as "two or more causes"; the plan decided cardioembolic with medical management of the stenosis (worker's open question stands). `perfect_agent.py -v` and `case_io.py check` clean after the edit.

## Condition audit
Condition auditor, 23 October 2026 (cross-case uniformity pass over all 30 ISCH-STR cases).
- Template carry-over (PATTERNS 4), the worker's FLAGGED own finding, now FIXED: ECG, echo and Holter values were copied from M01 (same intervals, LAVI 36, 847 PACs, longest AF episode 02:14 to 04:06). `initial_tool_outputs.ecg`: rate 76 (triage HR 80), PR 176 ms, QRS 98 ms, QTc 452 ms, SV1 + RV5 36 mm, finding "at 76 bpm". Echo follow-up: LAVI 41 mL/m2 (mildly dilated), septum 1.4 cm, LVEF 57%; criterion `action-9-order-echocardiogram` expected evidence updated. Holter follow-up: PAC count 1,214 (still about 1%), longest episode 01:36 to 03:28 (duration unchanged, 1 hour 52 minutes), `heart_rate_range.average` 71 (consistent with 20.5 h of sinus rhythm and 3.5 h of AF at 108 bpm). Burden 14.6% and every decision unchanged. Both checks clean.

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
- Carotid must rewritten: the ipsilateral symptomatic 55-60% stenosis is a competing mechanism referred for vascular surgical review within 2 weeks (endarterectomy for 50-69% decided on patient factors, perioperative risk below 6%, AHA/ASA 2021); key evidence aligned. The ELAN major category (multi-branch superior-division cortical infarct, about 18 mL) is kept (decision OQ4b, OQ4h).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
