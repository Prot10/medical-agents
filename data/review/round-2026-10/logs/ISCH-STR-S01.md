# ISCH-STR-S01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| c97b3f6e-9794-4ba2-ae83-a9adf1f87b01 | FIXED | Left MCA label, imaging and I63.412 kept; body findings flipped to the right (plan C15): `patient.chief_complaint` (right-sided weakness), `patient.history_present_illness` (right arm limp, EMS "left gaze deviation, right facial droop, right-sided hemiplegia"), `patient.neurological_exam.cranial_nerves` (left gaze preference, unable to cross midline to the right; right lower facial droop sparing the forehead; tongue deviates to the right), `.motor`, `.reflexes` (right hyperreflexia and Babinski), `.sensory` (right pinprick loss, right extinction, right proprioception), `.coordination`, `.gait`, `.additional` (left hemineglect replaced by right-sided visual inattention). `mental_status` "commands with the left hand" is now the non-paretic hand and was left as written. `metadata.case_body_concerns` laterality entry removed. |
| f6628b06-b982-4450-b101-0378417b8d27 | FIXED | `patient.neurological_exam.additional`: "NIHSS score: 22" itemised (LOC questions 2, commands 1, gaze 2, face 2, right arm 4, right leg 3, sensory 1, language 3, dysarthria 2, extinction and inattention 2), the reviewer's count after the flip; 22 repeated in the LKW must, decision must and `key_clinical_evidence`. |
| fdfaae93-a476-4a78-ba75-77775c97045f | FIXED | `initial_tool_outputs.mri.findings[0].signal_characteristics`: FLAIR "No corresponding FLAIR hyperintensity (DWI-FLAIR mismatch)", T1 and T2 without definite change, `mass_effect` "No mass effect" (an infarct under 3 hours old); `mri.impression` names the acute left MCA infarct with no FLAIR change, the ICA terminus and M1 occlusion and no haemorrhage, and no longer asserts chronic small vessel disease. NCCT and MRI now agree: a normal CT (ASPECTS 10) with a DWI-only lesion is the hyperacute appearance. MRA finding extended to the ICA terminus to match the CTA. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs` order, `ground_truth.action_criteria` order | Echo, Holter, hypercoagulability panel, literature and drug check came before the CTA that decides thrombectomy (C1). | FIXED: follow-ups CTA, drug check, TTE, Holter, literature; criteria NCCT, labs, ECG, CTA, MRI (optional), drug check, echo, monitoring, literature. Criterion ids kept. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts never stated the reperfusion decision; generic LKW/NIHSS, "Administer IV tPA if within window", "Begin secondary prevention ... per mechanism" (C4, C6). | FIXED: case-specific LKW/NIHSS must; decision must (IVT given, EVT for the carotid T occlusion, no waiting for the IVT response); door-to-needle; BP must; stroke unit telemetry; rate control; troponin; apixaban with CHA2DS2-VASc 5 and HAS-BLED 3 on day 6 to 7 (ELAN, major infarct), no heparin bridge, stop aspirin; shared decision on his earlier refusal; atorvastatin 40 to 80 mg. |
| C | major | `patient.vitals` vs musts | BP 185/100 on arrival is not below 185/110, so lowering is needed before IVT; no must said so. | FIXED: canonical BP must with 185/100 named, plus no systolic target below 140 after recanalization. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "below 140/90" prohibition (C5) in a case that receives IVT and EVT; generic anticoagulation and thrombectomy-referral prohibitions. | FIXED: 140/90 removed; anticoagulation prohibition rewritten (not within 24 hours of IVT or before imaging excludes haemorrhage, no bridging); "Do not delay thrombectomy to observe the response to IV thrombolysis". |
| C | minor | `initial_tool_outputs.labs` Troponin I 0.07 (H) | Raised troponin left without action (C14). | FIXED: troponin must. |
| C | minor | `initial_tool_outputs.ecg`, vitals HR 117, Holter range 62-148 | Rapid atrial fibrillation without a rate-control must (C14). | FIXED: rate-control must. |
| D | major | `initial_tool_outputs.ct.additional_observations[0]`, `.impression` | NCCT template management text ("does not justify withholding treatment", "Nothing on this study contraindicates intravenous thrombolysis..."). | FIXED: canonical impression "1. No acute intracranial haemorrhage. 2. No established infarct, no hyperdense vessel sign and no mass lesion. ASPECTS 10."; observation "No hyperdense vessel sign" added to support it. |
| B | major | `followup_outputs[0]` (CTA) `contrast_used`, `impression` | `contrast_used` false; impression omitted the occlusion (C11). | FIXED: contrast true; impression opens with the left ICA terminus and M1 occlusion. |
| C | minor | `followup_outputs[0].output.findings[1]`, `.impression` | Left ICA "approximately 50%" stenosis with AF would make the TOAST class "two or more causes", contradicting the cardioembolic label. | FIXED: left bifurcation stenosis about 35%; differential and key evidence say both sides are under 50%. |
| B | minor | `followup_outputs[2]` (TTE) `impression` | "Abnormal values: ... LVEF 50% (H)" list, LVEF flagged high (C11); no `echo_type`. | FIXED: real numbered impression (concentric LVH, LVEF 50%, LAVI 38 mild LA dilatation, mild MR, appendage not seen); `tool_parameters.echo_type` TTE (the EchoReport schema has no echo_type field, so it is set in `tool_parameters` only). |
| D | minor | `followup_outputs[3]` (Holter) | Impression judged "adequate rate control on current medications" (management, cross-reference); no admission timing (C2); no `tool_parameters`. | FIXED: opens "Recorded on the stroke unit after admission, 24 hours."; burden and rate only; `tool_parameters.monitor_type` holter_24h; criterion alternatives holter_24h, holter_48h, telemetry. |
| C | major | `followup_outputs[1]` (drug check) | Contraindications field held a non-contraindication with a "verify LKW" instruction; alternatives were thrombectomy and DOAC (management and diagnosis leakage); lisinopril angioedema missing. | FIXED: rewritten with his medicines: aspirin not a contraindication (hold antithrombotics 24 h), lisinopril orolingual angioedema, others no interaction, penicillin allergy irrelevant; contraindications empty; tenecteplase as the only alternative. Criterion recommended (C7). |
| C | major | `followup_outputs[4]` (literature) | Fabricated citations: AcT attributed to "Bhatt DL, NEJM 2024" as a pre-thrombectomy trial; a "2019 focused update" title. | FIXED: three real sources (AHA/ASA 2026 Prabhakaran; HERMES, Goyal, Lancet 2016; AcT, Menon, Lancet 2022), general evidence only. Criterion optional, last, `required_arguments` {} (an exact query string could never match). |
| B | minor | removed `followup_outputs` hypercoagulability panel | Orphan thrombophilia panel, not indicated in AF cardioembolism (C9). | FIXED: deleted. |
| A | minor | `ground_truth.action_criteria[*]` | Label identical to rationale; duplicate `[AHA_ASA_2019]` and free-text citation (C17, 1.1). | FIXED: distinct labels and rationales, case-specific expected evidence, `[AHA_ASA_Stroke_2026]` only; avoided actions recited with the 2026 key. |
| A | minor | `ground_truth.sequence_constraints`, `stop_rule` | Hard NCCT-to-drug-check template constraint; drug check, echo and Holter required before assessment; allowance 0. | FIXED: soft NCCT before CTA, CTA before echo, CTA before monitoring; stop rule NCCT, labs, ECG, CTA; `max_additional_actions` 1. |
| E | minor | `ground_truth.key_clinical_evidence` | Engineering lines ("Off-pathway modality...", "Tier per the July 2026 clinical review"), 6-24 h DAWN/DEFUSE pearls irrelevant at 2 h 47, "normal sinus rhythm" pearl in an AF case. | FIXED: case-specific evidence (window, localisation, NIHSS, EVT criteria, hyperacute imaging, mechanism, troponin); AHA/ASA 2026 sequencing line kept. |
| B | minor | `patient.history_present_illness` | "not been taking any blood thinners" while he takes aspirin. | FIXED: "any anticoagulant". |
| B | minor | `ground_truth.differential` | Key features generic. | FIXED: tied to the stored results (CT, glucose, plaque under 50%). |
| E | minor | `metadata.clinical_pearls[2]` | "bridging therapy superior to IV tPA alone" imprecise. | FIXED: thrombectomy added to IV thrombolysis is superior to IV thrombolysis alone. |

## Changes, in one paragraph a physician can read before re-reviewing

The patient now has a coherent dominant left hemisphere syndrome: global aphasia, right hemiplegia (arm 0/5, leg 1/5 at the hip), right lower facial palsy, right sensory loss with right extinction and visual inattention, leftward gaze deviation and tongue deviation to the right, NIHSS 22 itemised. Imaging is hyperacute throughout: NCCT shows no haemorrhage and no established infarct (ASPECTS 10, no hyperdense sign); the optional MRI shows a left MCA DWI lesion without FLAIR change and the ICA terminus/M1 occlusion; the CTA (contrast now recorded) opens with the carotid T occlusion and grades both bifurcations under 50%. The work-up runs NCCT, labs, ECG, CTA, then the drug review, TTE and stroke-unit monitoring; the thrombophilia panel is gone and literature is optional. The musts state the decision: IV thrombolysis at 2 hours 47 minutes after lowering BP from 185/100 below 185/110, thrombectomy without waiting for its effect, door-to-needle under 60 minutes, stroke unit with telemetry, rate control, repeat troponin, apixaban 5 mg twice daily on day 6 to 7 for this major infarct (CHA2DS2-VASc 5, HAS-BLED 3) with aspirin stopped and no heparin bridge, a shared decision about his earlier refusal of anticoagulation, and atorvastatin increased to 80 mg. The drug review lists his medicines (aspirin not a contraindication, lisinopril angioedema risk).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[AHA_ASA_Stroke_2026]` used throughout (plan section 5.1, pack allow-list).
- Synonyms appended to `accepted` include "lacunar stroke" and "lacunar infarct" for a cardioembolic MCA infarct; the I63 synonym list may be too broad for this case (plan section 5.3 owner).
- EchoReport has no `echo_type` field; the plan asks for it in the output. Set in `tool_parameters` only.

## Open questions for Andrea (judgment calls you could not settle)

- NIHSS item 3: the official NIHSS instructions score visual extinction 1 on item 3 and carry it to item 11. The plan and R2 (S05 note 9802d420) count extinction under item 11 only; I followed them (total 22). If the official convention is applied, the total is 23.
- Right-sided inattention was kept (plan option) rather than removed: right neglect is less frequent after left hemisphere infarcts but documented acutely in large left MCA strokes, and the reviewer's total of 22 depends on it.
- Left ICA stenosis lowered from about 50% to about 35% to keep the TOAST class unambiguous (cardioembolic). If you prefer to keep 50%, the label should acknowledge two possible mechanisms.

## Verification
Adversarial verifier, 23 October 2026. Read the log, the diff and the whole final case.

Checked: the three notes (c97b3f6e flip is complete in chief complaint, HPI, EMS text, cranial nerves, motor, reflexes, sensory, coordination, gait and NIHSS; the patient leans toward the plegic right side; the left-hand command following now refers to the non-paretic hand); NIHSS 22 recounted from the exam (LOC 1a 0, questions 2, commands 1, gaze 2, visual 0, face 2, right arm 4, right leg 3, ataxia 0, sensory 1, language 3, dysarthria 2, extinction 2 for tactile plus visual inattention); FLAIR, NCCT and MRI agree on a hyperacute infarct; CTA contrast and impression; anion gap 15; CHA2DS2-VASc 5 (hypertension, age 65 to 74, diabetes, stroke 2); HAS-BLED 3 (stroke, age, aspirin); ELAN class (lesion 5.2 x 3.8 cm across several MCA cortical branches: major); musts against prohibitions (anticoagulation timing, thrombectomy without waiting, BP thresholds) without contradiction; criteria order, tiers, soft constraints and stop rule per plan section 3; no 140/90, `[AHA_ASA_2019]`, free-text citation or engineering line left; differential at assessment-time likelihoods.

Found and fixed:
- `initial_tool_outputs.labs` CBC: RBC 4.7 with Hct 47.8 gives an MCV of 101.7, not the reported 93.7 (lab arithmetic, PATTERNS 3). RBC set to 5.1 (MCV 93.7, MCH 30.8; within 4.35-5.65).
- `required_recommendations[7]`: "HAS-BLED 3 for prior stroke" read as a previous stroke, which the case does not have; the S item counts the index stroke. Now "for this stroke".

Not changed: the item 3 versus item 11 extinction convention and the 35% left ICA stenosis stay as the worker's open questions. `perfect_agent.py -v` passes (the `<- ?` source label for the initial CT and labs is a labeller quirk in `_source`, which compares against `model_dump(exclude_none=True)`; the same appears in SE-S01); `case_io.py check` is clean for this case.

## Condition audit
Condition auditor, 23 October 2026 (cross-case uniformity pass over all 30 ISCH-STR cases).
- Echo `chambers` "Left Atrial Volume Index" was unitless ("38"); now "38 mL/m2 (mildly dilated)", matching the impression. No other change. Both checks clean.

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
- NIHSS recounted by the official item 3 rule (visual extinction scores 1 on item 3 and is carried to item 11): 22 to 23 in the exam, key evidence and both musts; no decision changes (decision OQ1).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
