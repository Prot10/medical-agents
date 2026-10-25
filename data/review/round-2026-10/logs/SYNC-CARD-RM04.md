# SYNC-CARD-RM04
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.clinical_history.past_medical_history[3]` | Diabetes "diet-controlled" while the medication list has metformin 500 mg twice daily. | FIXED: "treated with metformin". |
| B | minor | `patient.neurological_exam.mental_status` | Examined "25 minutes after the episode" although the HPI says she presented 30 minutes after it. | FIXED: 40 minutes. |
| B | minor | `patient.history_present_illness` | "Collapsed without warning" right after a described prodrome; head strike not stated, though the head CT decision depends on it. | FIXED: "collapsed to the floor within seconds; she did not strike her head." |
| C | minor | `patient.clinical_history.past_medical_history` | Pregnancy test is required before CTPA but the record never states menopausal status (plan C). | FIXED: added "Premenopausal; regular menstrual cycles, last menstrual period 2 weeks ago". |
| E | minor | `patient.neurological_exam.additional` | "Homan's sign"; staples still in at day 18. | FIXED: "Homans' sign negative"; healing incision, staples removed. |
| C | major | `action-2-interpret-labs` | Pinned CBC, BMP, troponin, BNP, D-dimer, coagulation and beta-hCG; D-dimer is not used at high clinical probability (Wells 9; ESC 2019); expected_evidence said D-dimer "places" the risk class. | FIXED: `panels: [troponin, BNP, beta-hCG]`; rationale and expected_evidence rewritten (troponin, BNP, hCG, creatinine). D-dimer ordering added as waste (`avoid-waste-6-d-dimer`). The D-dimer value drawn in the ED stays in the stored panel as data. |
| B | minor | `initial_tool_outputs.labs` | "Troponin I (high-sensitivity)" with a conventional ng/mL reference (<0.04); lab-style interpretation listing every value. | FIXED: "Troponin I"; interpretation rewritten as a pattern recital. |
| B | major | `followup_outputs[0]` (TTE) | RVSP 67 mmHg from a TR jet of 3.9 m/s with RA pressure 15 (IVC 2.5 cm, reduced collapse) is arithmetically 76 mmHg, and a previously normal RV rarely generates such a pressure acutely; no echo_type; "bubble study deferred" framing; no LA or wall thickness. | FIXED: TR 3.3 m/s, gradient 44 mmHg, RVSP 59 mmHg; echo_type TTE; LV wall 10 mm, LA 34 mm / LAVI 26, TAPSE in chambers; no bubble framing; numbered echo-voice impression. Echo expected_evidence updated. |
| B | major | `action-5-order-cardiac-monitoring`, `followup_outputs[1]`, `fallback_tool_outputs.cardiac_monitoring` | Telemetry only; fallback null, so a Holter order received the library's normal recording. | FIXED: alternatives telemetry, holter_24h, holter_48h; trigger `request_telemetry_holter_monitoring`; impression "Inpatient telemetry, 24 h"; heart-rate min/max added; same recording as the case fallback. Expected_evidence no longer contains policy text ("monitoring required during anticoagulation"). |
| B | minor | `followup_outputs[2]` (CTPA) | `modality` was prose ("CT angiography"), so the study discriminator could not adjudicate; "Trace" and "Small" effusions in one report; duplicated infarct line; em dash. | FIXED: modality `CTA`, region `chest`; contradicting and duplicate findings removed; impression rewritten. |
| C | major | `action-6-check-drug-interactions`, `followup_outputs[4..8]`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Criterion named no drug; single follow-up repeated the key and prescribed a blanket 48 h metformin hold; fallback was a generic review. | FIXED (plan B): alternatives aspirin, enoxaparin, heparin, apixaban, rivaroxaban, one report-voice follow-up each against her list; initial and fallback both hold the medication-list review (aspirin bleeding, acetaminophen-warfarin, no CYP3A4/P-gp interactors, metformin-contrast rule per ACR Manual, metformin contraindicated in tissue hypoxia). |
| C | major | `action-7-search-medical-literature`, `followup_outputs[13]` | Literature required and in the stop rule; follow-up cited a non-existent "Costantino 2017 Heart" review and mis-titled Jimenez 2010; its summary gave a patient-specific post-surgical verdict. | FIXED: optional, canonical rationale; one follow-up with ESC 2019 PE content only, placed last. Case fallback literature kept (general ESC 2018 text, no leak). |
| C | minor | new `action-8-lower-extremity-venous-duplex`, `followup_outputs[3]` | Plan: venous duplex optional. | FIXED: optional criterion `order_body_imaging{study: lower_extremity_venous_duplex}`; stored duplex report (right popliteal and posterior tibial DVT). |
| C | major | `sequence_constraints` | Hard ECG before CTPA; hard labs before monitoring (unsafe order, ESC 2018). | FIXED: ECG before TTE, monitoring and CTPA (soft); labs (pregnancy test) before CTPA (soft); labs-before-monitoring deleted. |
| A | minor | `stop_rule` | Literature in the required list; `max_additional_actions: 0`. | FIXED: the six required criteria; 3. |
| H/E | minor | all criteria `citations`, `rationale` | Free-text "ESC 2018 §x" citations; rationale equal to label. | FIXED: keys only; real rationales naming ESC 2018 / ESC 2019. Criteria reordered ECG, labs, TTE, telemetry, CTPA, drug review, duplex, literature (ids unchanged). |
| C | blocker | `ground_truth.assessment.required_recommendations` | Rescue plan relied on systemic thrombolysis, which ESC 2019 lists as absolutely contraindicated within 3 weeks of major surgery (arthroplasty 18 days ago); UFH preferred by default (ESC 2019 prefers LMWH); blanket metformin hold (plan: hold only for eGFR < 30 or AKI); thrombophilia work-up for a provoked PE; NIV for hypoxaemia in RV failure; no disposition, no anticoagulation duration. | FIXED: musts are diagnosis with ESC 2019 risk class, monitored admission, weight-based LMWH (UFH if reperfusion likely or CrCl < 30), rescue by catheter-directed treatment or surgical embolectomy planned in advance, stop aspirin, oxygen for SpO2 < 90% with high-flow nasal oxygen before positive pressure, DOAC for 3 months without thrombophilia testing (ESC 2019 Class I; NICE NG158), metformin not held for contrast (eGFR about 79) but withheld while hypoxaemic with lactate 2.8, driving advice. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Antiseizure prohibition irrelevant (no one proposes it); tilt prohibition is a test, not management (plan I). | FIXED: deleted; added no routine primary thrombolysis (ESC 2019 Class III) and no systemic thrombolysis as rescue within 3 weeks of surgery, no coronary angiography on the troponin; kept no-discharge and no-aspirin-with-anticoagulation. |
| C | major | `avoided_actions` | No penalty for a head CT (no NG232 criterion), D-dimer at high probability, or exercise testing in acute PE; library answers to those orders contradicted the patient (normal Bruce test at 10.4 METs). | FIXED: `avoid-waste-5-order-ct-scan` (NG232), `avoid-waste-6-d-dimer` (ESC 2019), `avoid-harm-7-exercise-stress-test` (acute PE and DVT are absolute contraindications, Fletcher 2013); a "not performed, walker-dependent" exercise follow-up added; other avoided rationales name the PE and cite ESC 2018. |
| B | minor | `fallback_tool_outputs.specialized_test`, new `followup_outputs[9]` | Fallback tilt with BP 118/70 contradicted BP 102/64 and HR 118; a non-contrast chest CT order received the library's clear-lung report. | FIXED: fallback set to null (the stored "not performed" tilt follow-up answers tilt orders); non-contrast chest CT follow-up added (RLL wedge opacity, effusions, PA 31 mm, CTPA recommended). |
| C | major | `ground_truth.differential` | ACS and vasovagal left moderate after CTPA confirms PE; hypovolaemia entry argued from D-dimer. | FIXED: ACS low (no ST deviation, CK-MB normal, normal LV wall motion, CT PE); vasovagal low; other entries cite telemetry, echo and CT. |
| C | minor | `ground_truth.key_clinical_evidence`, `metadata.clinical_pearls` | D-dimer "essentially excludes alternative diagnoses"; "systemic thrombolysis must be immediately available"; "misread in the real-seeded case" meta text; unsourced S1Q3T3 sensitivity figures. | FIXED: rewritten from the pathway results, Wells score, ESC 2019 risk class and the thrombolysis contraindication. |
| L | minor | `ground_truth.red_herrings[0..2]` | Interpretations leaned on the D-dimer; red herring 2 data_point did not quote its field. | FIXED: data_points quoted from the fields; interpretations cite ECG, imaging and exam. |
| E | minor | `metadata.vocab_gap`, `difficulty_rationale` | vocab_gap described CTPA through `order_ct_scan` (stale since body imaging exists); rationale counted 5 required tools. | FIXED: vocab_gap emptied; rationale updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The 48-year-old woman with syncope 18 days after right knee arthroplasty now has six required steps: ECG (right-heart strain pattern), troponin, BNP and a pregnancy test (D-dimer removed and made waste at Wells 9, ESC 2019), TTE, inpatient telemetry (Holter accepted), CT pulmonary angiography and a review of aspirin and the chosen anticoagulant against her list. The echocardiogram's pressures are now internally consistent (TR 3.3 m/s, RVSP 59 mmHg). An optional right-leg venous duplex returns a popliteal and posterior tibial DVT; the literature lookup is optional and last. The management is rewritten: intermediate-high-risk PE admitted to a monitored bed, weight-based LMWH (UFH if reperfusion becomes likely), and, because systemic thrombolysis is contraindicated within 3 weeks of major surgery, rescue by catheter-directed treatment or surgical embolectomy planned in advance; aspirin stopped; DOAC for 3 months without thrombophilia testing; metformin not held for contrast at eGFR about 79 but withheld while she is hypoxaemic with lactate 2.8; oxygen below SpO2 90%. Head CT, D-dimer, EEG, MRI, CSF and tilt are waste and exercise testing is harm. ACS and vasovagal syncope are now low. Record fixes: diabetes on metformin, premenopausal status, no head strike, exam timing.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: `accepted` still carries the generic "cardiac syncope"; not hand-edited.
- Plan C4: an ESC 2019 PE citation key ([ESC_PE_2019], Konstantinides 2020) is needed; this case cites it by name in rationales.
- Library: the normal TEE library report (normal RV) and the normal exercise-test report contradict this case; handled per case where an order is plausible (exercise test, chest CT).

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Deviations from the lead plan, decided for clinical correctness:
- Plan says "rescue thrombolysis on deterioration". The arthroplasty was 18 days ago and ESC 2019 lists major surgery within 3 weeks as an absolute contraindication to fibrinolysis, so the must names catheter-directed treatment or surgical embolectomy instead, and a prohibition bars planning systemic thrombolysis as the rescue.
- Plan says hold metformin only for eGFR < 30 or AKI. The contrast rule is applied (no hold for contrast), but the must also withholds metformin while she is hypoxaemic with a lactate of 2.8 mmol/L, because tissue hypoxia is a labelled contraindication.
- Plan C lists troponin and BNP; beta-hCG is also pinned (the plan's own RM04 entry requires it, and the record now states she is premenopausal).
- Exercise testing added as harm (not in the plan's PE row) because the library returned a normal treadmill test for a walker-dependent patient with acute PE and DVT.

## Verification

Adversarial verification, 24 Oct 2026 (diff against fa1d22e6, the pre-round version; the batch-4 checkpoint commit already holds the worker's edit).

Checked: no reviewer notes exist for SYNC-CARD, so the "(none)" row is correct. Every own-finding claim against the file: Wells 9 (DVT signs 3, PE most likely 3, HR > 100 1.5, surgery within 4 weeks 1.5); sPESI 1 or more from HR 118; intermediate-high risk (RV dysfunction on TTE and CT plus raised troponin, ESC 2019); TTE arithmetic (TR 3.3 m/s gives 44 mmHg, plus RA 15 gives RVSP 59); eGFR about 79 from creatinine 0.9 at 48 F (CKD-EPI 2021); lactate 2.8 present in the stored panel, so the metformin must is grounded; major surgery within 3 weeks is an absolute contraindication to fibrinolysis in ESC 2019 Table 10, so the deviation from the plan's "rescue thrombolysis" is correct; 3 months of anticoagulation for PE provoked by a major transient factor (ESC 2019 Class I) and no thrombophilia testing for provoked VTE (NICE NG158) are correct. Musts, prohibitions and avoided actions do not contradict each other (aspirin stopped in a must, combination prohibited; D-dimer waste and absent from the labs criterion; `D_dimer` and `D-dimer` are both vocabulary values). Telemetry fallback equals the follow-up; holter, tilt, exercise, chest CT and duplex orders are answered by case-consistent outputs (probed through the environment). Labs pin troponin, BNP and beta-hCG as the plan requires; sequence constraints are soft, stop rule lists the six required criteria; differential matches the final evidence; red herrings quote their fields; leak, follow-up and banned-string guards pass.

Found and fixed:
- `fallback_tool_outputs.eeg.activating_procedures.hyperventilation` said "hemodynamically unstable patient", contradicting the haemodynamically stable intermediate-high-risk PE in the musts. Now "Not performed (hypoxaemic patient on supplemental oxygen)."

Left as is: a TEE order still receives the library's normal-RV TEE report (worker's CENTRAL note covers the library); TEE is not a plausible order in this case.

perfect_agent.py SYNC-CARD-RM04 -v: ok. case_io.py check: schema, synonym guard and tests clean for this case.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_pulmonary_embolism_risk_stratification_management` renamed to `search_pulmonary_embolism`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.
- red herring 0 `data_point` now quotes the HPI verbatim ("like the room was closing in" and collapse within seconds).

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: PE labels; I26.9 (PE without acute cor pulmonale) dropped, the case has RV strain. `metadata.citation_gap` cleared: `[ESC_2019_PE]` is now in the pack.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-2-interpret-labs citations ['[ESC_2018]'] -> ['[ESC_2019_PE]']; action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2019_PE]']; action-5-order-cardiac-monitoring citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2019_PE]']; action-4-order-body-imaging citations ['[ESC_2018]'] -> ['[ESC_2019_PE]']; action-6-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2019_PE]']; action-8-lower-extremity-venous-duplex citations [] -> ['[ESC_2019_PE]']; avoid-waste-5-order-ct-scan citations [] -> ['[NICE_NG232]']; avoid-waste-6-d-dimer citations [] -> ['[ESC_2019_PE]']; avoid-harm-7-exercise-stress-test citations [] -> ['[Fletcher_2013]']; action-2-interpret-labs->action-4-order-body-imaging citations [] -> ['[ESC_2019_PE]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-RM04` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure 'Active stand test not performed. Deferred by the clinical team.' (haemodynamically unstable or high-grade AV block at presentation: standing is not safe); no criterion |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-8-lower-extremity-venous-duplex` label: "Right leg venous duplex (optional)" -> "Right leg venous duplex"
- criterion `action-7-search-medical-literature` label: "Guideline lookup on acute PE management (optional)" -> "Guideline lookup on acute PE management"

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.alternatives: was [troponin, BNP, beta-hCG]; now [troponin, BNP, beta-hCG, creatinine] | [troponin, BNP, beta-hCG].
- Decision: serve: new first alternative (old order kept as an alternative). The evidence reads the creatinine needed before CT pulmonary angiography and for anticoagulant dosing, which the rationale names; troponin, BNP and beta-hCG did not return it.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
