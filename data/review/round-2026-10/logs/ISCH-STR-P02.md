# ISCH-STR-P02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 10f6a890-04d8-46d7-9a85-671e833eb331 | FIXED | Decision rule stated in a must (`ground_truth.assessment.required_recommendations[3]`): IV thrombolysis not given once CTA shows moyamoya vasculopathy (safety and benefit not established, fragile collaterals); thrombectomy not indicated (chronic steno-occlusive arteriopathy, no acute thrombotic occlusion). Door-to-needle and pre-IVT BP musts removed. The two overlapping alteplase prohibitions merged into one with that reason (`prohibited_recommendations[0]`); the generic "INR >1.7 ..." and "before NCCT" tPA prohibitions removed (IVT is not given in this case). |
| 50ffe53e-bbbe-4fe5-aa8d-32e639f43067 | FIXED | `initial_tool_outputs.mri.impression` rewritten as a numbered list: acute left frontal opercular infarct, chronic bilateral border-zone infarcts, basal ganglia flow voids, MRA reduction of distal ICA/proximal MCA flow, hedged "suggestive of moyamoya vasculopathy". |
| ceadf1cd-583a-444b-bcd1-f8a5df548537 | FIXED | "right hand motor 1" removed from `patient.neurological_exam.additional`; NIHSS recounted (see own findings). |
| bcb508a7-88a3-4926-a1f0-795499c213d0 | FIXED | Best language scored 1 in `patient.neurological_exam.additional`. |
| 027c14a1-2374-4814-9f24-7ac45ac71434 | FIXED | Template must replaced by: aspirin monotherapy, no anticoagulation (no cardioembolic source, haemorrhage risk), statin only if a lipid profile shows an indication (`required_recommendations[6]`); neurosurgical revascularization referral kept; new prohibition "Do not anticoagulate ..." (`prohibited_recommendations[1]`). The template "Do not start full-dose anticoagulation in the acute phase of a large infarct" removed (plan C6: AF cases only). |
| daf0605e-b483-49f0-bebb-fd9d7f54bf5f | FIXED | New must: genetic counselling with RNF213 testing and screening of first-degree relatives, familial moyamoya more frequent in East Asians, mother's ICH at 45 (`required_recommendations[10]`); key evidence item 5 states the family-history red flag; pearl 3 reworded. |
| bc4354fa-4ca0-4579-856c-1b5093dc08d2 | FIXED | Key evidence item 4: chronic bilateral border-zone infarcts mean some earlier episodes completed infarcts despite clinical recovery (silent infarction), typical of moyamoya. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.additional` | NIHSS 8 did not sum from the exam. Recount: face 1, right arm 1 (deltoid 4/5 with pronator drift: drift without falling to the bed, as R2 reasoned for P03), right leg 1, language 1, dysarthria 1 = 5. | FIXED: itemised NIHSS 5; dysarthria made explicit in `mental_status` ("Articulation mildly slurred."). |
| B | minor | `patient.history_present_illness` | "rapidly progressed to inability to lift her right arm" contradicted deltoid 4/5 on examination. | FIXED: "rapidly progressed to marked weakness of her right hand and arm." |
| A | major | `ground_truth.action_criteria` order and tiers | Pathway inverted (echo, hypercoag panel, drug check, Holter before the CTA); echo and Holter required; literature recommended. | FIXED per plan 3.1: NCCT, labs, ECG, CTA (required), MRI (optional), TTE (recommended), monitoring (recommended, alternatives holter_24h/holter_48h/telemetry), drug check (required), literature (optional, last). `followup_outputs` reordered CTA, TTE, Holter, drug check. |
| C | major | criterion `action-5-interpret-labs` and its follow-up `request_hypercoagulability_panel` | Thrombophilia panel not indicated once the mechanism is moyamoya; the criterion was answered by the initial labs (baseline warning). | FIXED: criterion and follow-up removed (plan C9). |
| D | major | `initial_tool_outputs.labs.panels` "Exclusion studies", "Mimic exclusion", "Lupus anticoagulant" row | Scaffolding panels whose `clinical_significance` leaked the case logic; FVL/prothrombin/antiphospholipid/LA results without an indication. | FIXED: both panels and the LA row removed; troponin moved to a "Cardiac" panel with a value (troponin I 0.01 ng/mL, ref < 0.04). |
| D | minor | `initial_tool_outputs.labs.abnormal_values_summary`, `.interpretation` | Interpretive text ("confirms iron deficiency"); Hct missing. | FIXED: factual list with Hct; pattern-level interpretation. |
| D | major | `initial_tool_outputs.ct` | NCCT template: "clinically implicated territory", "does not justify withholding treatment", "Nothing on this study contraindicates intravenous thrombolysis ...". | FIXED: canonical normal impression with ASPECTS 10; "left MCA territory"; hyperdense vessel sign negative. |
| B | minor | `initial_tool_outputs.mri.findings[0].signal_characteristics` | FLAIR negative with teaching parenthetical while T2 called positive (T2 is less sensitive than FLAIR). | FIXED: FLAIR "No corresponding FLAIR hyperintensity (DWI-FLAIR mismatch)"; T2 "No definite signal abnormality". |
| B | minor | CTA follow-up `findings[0]`, `impression` | "near-occlusion bilaterally" with a right terminus stenosis of 80%; impression not numbered; no statement on acute occlusion although EVT is decided from it. | FIXED: near-occlusion on the left only; numbered impression; additional observation and impression item 3: no intraluminal thrombus or branch cut-off; cervical arteries normal. `contrast_used` was already true. |
| B | minor | echo follow-up | "All values within normal limits." impression; LA volume without unit; em dash; no `echo_type`. | FIXED: real normal TTE report with agitated saline result; `echo_type` TTE in output and `tool_parameters`; trigger `request_tte_echocardiogram`. |
| B | minor | Holter follow-up | Report did not state when it was recorded. | FIXED: opens "Recorded on the stroke unit after admission, 24 hours."; impression without cross-modality "cardioembolism" wording. |
| C | major | drug-check follow-up and `action-8` | Alteplase checklist (IVT is not given; cites AHA_ASA_2019); OCP and escitalopram mentioned only in passing. | FIXED: criterion `drug: aspirin` (required, plan C7); output lists escitalopram bleeding interaction, OCP contraindicated after stroke (stop), ferrous sulfate, cephalosporin allergy (no cross-reactivity), menstrual blood loss warning, clopidogrel alternative. New must: stop the combined oral contraceptive. |
| D | major | `initial_tool_outputs.literature_search` | Output echoed the criterion's expected text. | FIXED: one general-evidence output (2021 AHA/ASA secondary prevention, ESO 2023 moyamoya guideline, RNF213 GWAS); criterion optional, last. |
| A | minor | all criteria `citations`, avoided actions | Free-text "AHA/ASA acute ischemic stroke guideline 2026", duplicated `[AHA_ASA_2019]`/`[AHA_ASA_2014]`. | FIXED: `[AHA_ASA_Stroke_2026]` or `[AHA_ASA_2021_secondary]`, one per list. |
| E | minor | criteria `label`/`rationale` | Rationale a copy of the label (template). | FIXED: case-specific labels, rationales and expected evidence. |
| C | major | `prohibited_recommendations[2]` | "below 140/90" template prohibition. | FIXED: canonical C5 COR 3 No Benefit text (no IVT, no EVT, BP 132/78). |
| A | minor | `sequence_constraints`, `stop_rule` | Template hard NCCT to drug-check constraint; max 0. | FIXED: soft NCCT before CTA, CTA before echo, CTA before monitoring; stop rule lists the five required criteria; `max_additional_actions` 1. |
| C | minor | `ground_truth.differential` | Hypercoagulable entry cited an untested panel; no secondary moyamoya syndrome entry; the panic attribution the history raises not addressed. | FIXED: moyamoya syndrome (low, no associated condition), ICAD (very low), panic/functional (very low) added; hypercoagulable entry removed with the panel; dissection, vasculitis, migraine entries cite case data. |
| E | minor | `ground_truth.key_clinical_evidence` | Template lines (thrombectomy up to 24 h, extended AF monitoring in cryptogenic stroke), three "Off-pathway modality" lines and the "Tier per the July 2026 clinical review" line. | FIXED: rebuilt with case-specific evidence; the AHA/ASA 2026 sequencing line kept. |
| B | minor | `ground_truth.red_herrings[0]` | Interpretation did not say why the migraine history does not explain the episodes. | FIXED: aura visual with headache vs stereotyped motor-language deficits provoked by hyperventilation. |
| C | minor | `metadata.clinical_pearls` | "nearly pathognomonic"; "hemorrhagic stroke (more common in adults)"; em dashes. | FIXED: "highly characteristic"; adults present with ischaemia or haemorrhage. |
| E | minor | `metadata.case_body_concerns`, `difficulty_description`, `difficulty_rationale` | Stale "required tool has no output" concerns; description listed hypercoagulability as a negative work-up item; "thrombolysis contraindicated". | FIXED: concerns emptied; description and rationale aligned with the new pathway and decision. |

## Changes, in one paragraph a physician can read before re-reviewing

The work-up now reads NCCT, core labs, ECG, CTA (all required), then optional MRI, recommended TTE with bubble study and stroke-unit rhythm monitoring, the required aspirin interaction check and an optional literature step last; the thrombophilia panel, its scaffolding rows in the admission labs and the alteplase checklist are gone. NIHSS is 5 (face 1, right arm 1, right leg 1, language 1, dysarthria 1). The CTA impression now leads with the bilateral terminal ICA and M1 stenosis with moyamoya collaterals and states there is no acute thrombotic occlusion; the MRI impression names the acute left frontal opercular infarct, the chronic border-zone infarcts, the flow voids and the MRA findings; the NCCT carries the canonical normal impression; the TTE and Holter are real reports. The musts state the decision (no IV thrombolysis once moyamoya is shown; no thrombectomy, no acute occlusion), stroke-unit monitoring, aspirin without anticoagulation (statin only on a lipid indication), avoidance of hypotension and hyperventilation, neurosurgical revascularization referral, stopping the combined oral contraceptive, and genetic counselling with RNF213 testing and family screening; prohibitions cover thrombolysis in moyamoya, anticoagulation, early antihypertensive treatment (COR 3 No Benefit) and hyperventilation/hypotension. Key evidence adds the silent-infarction point and the familial red flag.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[AHA_ASA_Stroke_2026]` and `[AHA_ASA_2021_secondary]` used per plan section 1.1 (criteria pack allow-list, plan section 5.1).
- `echo_type` is not a field of `EchoReport`, so the key written into the echo output (plan C11) is ignored by the schema and the MockServer discriminator; TTE routing works through the trigger token `tte`. Consider adding `echo_type` to `EchoReport`.

## Open questions for Andrea (judgment calls you could not settle)

- The plan withholds IVT once CTA shows moyamoya, which matches R2's note. Guidelines give no firm rule (safety not established); some centres would still thrombolyse a disabling deficit at 2 hours. The case keeps the plan's decision; confirm with R2.
- NIHSS 5 rests on scoring the right arm 1 (deltoid 4/5 with pronator drift). If R2 reads the arm as 2, the total is 6; nothing else in the case depends on the difference.

## Verification

Adversarial verifier, 23 October 2026. Checked: the three reviewer-note rows against the file (decision must and single IVT prohibition, MRI impression items 1 to 4, NIHSS itemisation without a hand item and language 1, aspirin-only must with no anticoagulation and a conditional statin, RNF213 and family-screening must, silent-infarction key evidence); NIHSS 5 recounted from the exam (face 1, arm 1 with deltoid 4/5 and drift, leg 1, language 1, dysarthria 1); lab arithmetic (Hct 3 x Hb, MCV from Hct/RBC, anion gap 14); FLAIR negative at 2 hours; CTA, TTE, Holter and drug check against the medication and allergy lists; tiers, order, constraints and stop rule against plan section 3; the differential against the final evidence; patient-block diff (only the HPI weakness sentence, NIHSS line and dysarthria sentence changed); no new em dashes.

Found and changed:
- `ground_truth.assessment.required_recommendations[0]`: "witnessed onset at work" was inaccurate (she noticed it herself at her desk; the coworker only called 911). Now "sudden onset at her desk at work, noticed by the patient, about 2 hours before arrival".

No other error found. `perfect_agent.py ISCH-STR-P02 -v` passes; `case_io.py check` clean for the case.

## Condition audit
Condition auditor, 23 October 2026 (cross-case uniformity pass over all 30 ISCH-STR cases).
- Literature output moved out of the initial work-up: `initial_tool_outputs.literature_search` (shown to reviewers as "Initial workup") is now null and the same general-evidence output is the last follow-up (`search_medical_literature`, trigger `search_moyamoya_antiplatelet_revascularization_evidence`), per ROUND_POLICY ruling 5 and plan 3.2 (initial outputs are NCCT, labs, ECG, MRI only). Content unchanged; a literature call with any query is still served this output (checked with the MockServer).
- Literature criterion `action-7-search-medical-literature`: `required_arguments` was an exact query string, which no agent query can match (exact-equality matching); now {} as in the other 27 cases. Optional tier unchanged. Both checks clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "embolic stroke", "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.4, I63.5, I63.3, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.23
- `case_io.py validate` OK; `perfect_agent.py` passes.
