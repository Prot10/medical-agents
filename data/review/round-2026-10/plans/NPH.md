# NPH: condition plan for the October 2026 review round

This is the lead plan for the 30 NPH cases (M01..M10, P01..P09, S01..S11). Workers follow it case by case, so that every case reaches the same decision for the same defect. Read `ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them.

No reviewer has annotated this condition. There is no notes file and no note id to cite. Every class below comes from the lead survey of all 30 cases:

- scripts over every field;
- a full read of S01, P07 and P08, most of M05, and the follow-ups of P01, P03, P06, S06, S10 and M06;
- MockServer simulations of the new follow-ups (3.2).

Ruling 2 still applies: fix each class in every case where it occurs, not only in the cases listed as examples. Because nobody reviewed NPH, a worker who finds a defect this plan does not name logs it and fixes it by the closest class.

The July 2026 tool review (Reviewer 1, `condition_tool_guidance.yaml` key `nph`) is the only physician input for this condition, and this plan follows it:

- MRI required, with the NPH markers;
- the CSF tap test required, with opening pressure and objective pre/post gait and cognition;
- generic CSF assays removed;
- labs optional and targeted;
- advanced imaging removed;
- neuropsychological testing removed;
- the timed gait assessment required, before and after the tap.

## Baseline measured on 24 October 2026, before any edit

The baseline covers all 30 cases, with no NPH logs.

- `perfect_agent.py`: 30/30 pass, a false pass: its neutral parameters miss the leaks and the post-tap result inside the baseline gait report.
- `test_case_guards` leak test fails in 9 cases (M01, M02, M03, M04, M05, M07, M08, S01, S05): `literature_search["general"]` repeats the literature criterion's `expected_evidence` (C1). The other guards pass.

## How to use this plan

1. Apply every class of section 2 to your case, in the order listed. Use the canonical text verbatim where one is given, filling the `<...>` slots from the case.
2. Apply the per-case decisions of section 4.
3. Rebuild `action_criteria`, `followup_outputs`, `avoided_actions`, `sequence_constraints` and `stop_rule` as section 3 says.
4. Run the checks of 3.6 and write `logs/<CASE_ID>.md` in the ROUND_POLICY format.

## Conventions for all new text

- English in the spelling of the field you edit (labels British, some histories American); no em or en dashes; the case's units (cmH2O, seconds, MoCA n/30).
- Never change `case_id`, `condition`, `diagnosis.accepted[0]` or `icd_codes[0]`; never hand-edit synonyms; edit only through `case_io.load/save`.
- An added result is plausible for the case (age, sex, medicines, other reports) and differs from other cases.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which guideline governs what

| Question | Source | Citation key |
| --- | --- | --- |
| Diagnostic categories (probable, possible, unlikely iNPH), clinical, imaging and pressure criteria | International iNPH guidelines, Relkin N et al., Neurosurgery 2005;57(3 Suppl):S4-S16 | `[Relkin_2005]` |
| Supplementary prognostic tests: tap test, extended lumbar drainage, their sensitivity and PPV | Marmarou A et al., Neurosurgery 2005;57(3 Suppl):S17-S28 (the pack's key) | `[Marmarou_2005]` |
| DESH, callosal angle, possible/probable/definite iNPH, tap test protocol, adjustable valve | Japanese guidelines for iNPH, 3rd edition, Nakajima M et al., Neurol Med Chir (Tokyo) 2021;61:63-97 | `[Nakajima_2021]` (new key, CENTRAL R2) |
| Shunting effect (AAN level "possibly effective") | Halperin JJ et al., AAN practice guideline summary, Neurology 2015;85:2063-2071 | `[Halperin_2015]` (new key, CENTRAL R2) |
| Tap-test predictors of shunt response | Tisell M et al. 2011 (pack key) | `[Tisell_2011]` |
| Review of iNPH | Williams MA, Malm J 2016 (pack key) | `[Williams_2016]` |
| Anticoagulant and antiplatelet management around a neuraxial puncture | ASRA guidelines, 4th edition, Horlocker TT et al., Reg Anesth Pain Med 2018;43:263-309 | `[ASRA_2018]` (new key, CENTRAL R2) |
| PSP midbrain-to-pons ratio (P07 only) | Massey LA et al., Neurology 2013;80:1856-1861 | `[Massey_2013]` (new key, CENTRAL R2) |

Use bracketed keys only. Drop `NPH_pack` and every unbracketed duplicate from `citations`. Do not add a key that CENTRAL R2 has not added; until it lands, use the pack keys and log the missing one.

### 1.2 Canonical facts (use these, do not restate them differently)

#### F1. Clinical criteria

Probable iNPH requires:

- insidious onset after age 40;
- duration of at least 3 to 6 months;
- no antecedent event such as head trauma, haemorrhage or meningitis;
- progression over time;
- a gait disturbance plus at least one of cognitive impairment or urinary symptoms [Relkin_2005].

The full triad is not required. Its absence never excludes iNPH, and its presence never establishes it.

#### F2. Imaging criteria

- **Required:** ventricular enlargement not entirely attributable to atrophy (Evans index greater than 0.3), with no macroscopic obstruction to CSF flow.
- **At least one supportive feature** [Relkin_2005]:
  - temporal horn enlargement not entirely attributable to hippocampal atrophy;
  - an acute callosal angle;
  - periventricular signal change not attributable to small-vessel disease;
  - an aqueductal or fourth-ventricle flow void.
- **DESH** has two components: tight high-convexity and medial parietal sulci, and enlarged Sylvian fissures [Nakajima_2021].
- **Callosal angle:** measured on the coronal plane through the posterior commissure. An acute angle (below 90 degrees) supports iNPH [Nakajima_2021].
- **Evans index 0.30 exactly does not satisfy "greater than 0.3".**

#### F3. Opening pressure

For iNPH the opening pressure is 70 to 245 mmH2O (5 to 18 mmHg) [Relkin_2005]. The Japanese guideline uses 200 mmH2O or less [Nakajima_2021]. CSF content must be normal (cells, protein, glucose).

#### F4. Tap test

- Remove 30 to 50 mL of CSF by lumbar puncture.
- Repeat the same timed gait measures, and the cognitive screen if done, at 2 to 4 hours and at 24 hours.
- An improvement of 10% or more in TUG time is a commonly used positive criterion [Nakajima_2021].
- Tap-test sensitivity is 26% to 61% and its PPV 73% to 100% [Marmarou_2005]. **A single negative tap test does not exclude shunt-responsive iNPH.**
- Extended lumbar drainage (about 10 mL/h, roughly 300 to 500 mL over 72 hours) has sensitivity 50% to 100% and PPV 80% to 100% [Marmarou_2005].
- Replace every "sensitivity 50-80%" in the cases with these figures.

#### F5. Categories and treatment

- **Possible iNPH:** age 60 or over, a compatible syndrome, and Evans index greater than 0.3.
- **Probable iNPH:** normal-pressure CSF with normal content plus DESH, a positive tap test, or a positive drainage test.
- **Definite iNPH:** improvement after shunting [Nakajima_2021].
- **Treatment:** referral to neurosurgery for CSF shunting (VP or LP) with a programmable (adjustable) valve [Nakajima_2021]. The AAN grades shunting "possibly effective" [Halperin_2015].
- **Treatment is never a tool call.**

#### F6. Secondary NPH

Communicating hydrocephalus with an identified antecedent (SAH, meningitis, head injury, intracranial surgery or subdural haematoma) is secondary NPH, not iNPH. It is treated by the same shunt route.

ICD-10-CM codes:

- G91.2: (idiopathic) normal pressure hydrocephalus;
- G91.0: communicating hydrocephalus, which includes secondary NPH;
- G91.3: post-traumatic hydrocephalus, unspecified (CENTRAL R1 for M09).

#### F7. Anticoagulants and LP

Per [ASRA_2018]:

- hold apixaban and rivaroxaban for at least 72 hours before the puncture (dabigatran by renal function);
- restart no sooner than 6 hours after the puncture;
- do not bridge a DOAC with heparin;
- aspirin and NSAIDs alone do not need to be stopped.

Write the plan as a must, never as a tool output. The decision to interrupt anticoagulation is weighed against the thromboembolic risk (CHA2DS2-VASc).

#### F8. Copathology

iNPH coexists with AD, PD, PSP and bvFTD more often than chance predicts. A coexisting neurodegenerative disease lowers the expected benefit of a shunt but does not exclude it. A positive tap test in a patient with copathology supports referral, with counselling that improvement may be partial (mainly gait) [Nakajima_2021].

#### F9. Bleeding thresholds for LP

Platelets of 50 x10^9/L or more and INR of 1.5 or less are the usual thresholds. M08 (platelets 88, INR 1.4) is within them.

#### F10. PSP sign (P07 only)

A midsagittal midbrain-to-pons diameter ratio below 0.52 is specific for PSP [Massey_2013]. A ratio of 0.55 is not.

---

## 2. Error classes in this condition

### C1. Literature search as a clinical step, with leaks (rulings 1 and 5)

**Found:**

- Every case has a literature criterion: `required` in M09, M10, P08, P09 and S11 (and in their stop rules), `recommended` in the other 25.
- Every case has literature initial or fallback outputs.
- 20 cases have literature follow-ups. Some of these are clinical steps disguised as searches:
  - P01 `request_multidisciplinary_conference`;
  - P04 `request_genetic_ftd_testing` and `request_goals_of_care_ftd_nph`;
  - P02 `request_msa_exclusion`;
  - P05 `request_depression_contribution`;
  - S07 `request_sleep_apnea_cognitive_contribution`;
  - S08 `request_hypothyroidism_cognitive_contribution`;
  - S09 `request_vascular_contribution_white_matter`;
  - S10 `request_vascular_dementia_af_contribution`.
- In 9 cases `literature_search["general"]` repeats the criterion's `expected_evidence`, which is the leak-test failure.

**Fix:**

- Delete the literature criterion and remove its id from `stop_rule` and from every sequence constraint.
- Set `initial_tool_outputs.literature_search` and `fallback_tool_outputs.literature_search` to null.
- Delete every `search_medical_literature` follow-up.
- If a deleted follow-up carried a real clinical point (the contribution of OSA, thyroid, depression or AF; goals of care in bvFTD), move it into a must or the assessment per section 4. Do not turn it into another tool call.

### C2. Drug-interaction checks as perioperative management (ruling 6)

**Found:**

- M03 has a recommended drug-check criterion.
- 23 cases have `check_drug_interactions` follow-ups, initial outputs or fallbacks that write shunt or perioperative management. They carry wrong advice: heparin "bridging" for a DOAC, "hold aspirin", "Hold rivaroxaban 24h".
- Two are fake consults: S02 `request_neurosurgery_consultation` and P06 `request_oncology_comanagement`.
- None is a drug-drug interaction that changes the diagnostic work-up.

**Fix:**

- Delete the M03 criterion.
- Delete every `check_drug_interactions` follow-up and set the drug-interaction initial and fallback outputs to null.
- Put the real content into musts (C11). Use these canonical texts, filling the slots:
  - **DOAC (M03, M06, S10):** "Hold <apixaban/rivaroxaban> for at least 72 hours before the lumbar tap and restart it no sooner than 6 hours after, without heparin bridging, weighing the interruption against the stroke risk of atrial fibrillation [ASRA_2018]".
  - **Aspirin (M10, P05, S06):** "Continue aspirin 81 mg through the lumbar tap; low-dose aspirin alone does not require interruption before lumbar puncture [ASRA_2018]".
  - **Levodopa (M05, P02):** "Continue carbidopa-levodopa unchanged and perform the pre- and post-tap gait measures in the same medication state, so the tap response is not confounded by a dopaminergic ON/OFF change".
  - **Sedating drugs (M04, P03):** "Review gabapentin<, baclofen> as contributors to unsteadiness and cognitive slowing and keep the doses unchanged across the tap test".
  - **P02, with the levodopa must:** "Review pramipexole as a contributor to confusion and falls".

### C3. The patient block gives the imaging measurements and the referral diagnosis (Kind 2 leakage)

**Found:**

- Most HPIs quote the outside imaging measurements: Evans index, callosal angle, DESH, "periventricular transependymal signal", sometimes "meeting NPH criteria".
- Most chief complaints or HPIs give the working diagnosis: "suspected NPH", "referred for NPH evaluation", "admitted for tap trial".
- P06's PMH begins "Leptomeningeal carcinomatosis concern".
- P07's HPI has the son "researching NPH".

**Fix:**

- Replace the measurements with a qualitative sentence: "A <CT/MRI> obtained <when> at an outside facility was reported as showing enlarged ventricles; the images are not available".
  - A measurement on an older scan that differs from the index MRI may stay, because it documents change. For example P04's "Evans 0.27 two years ago" stays.
- Replace a referral diagnosis with the referral question: "referred by <who> for progressive gait difficulty <and memory decline/urinary urgency>".
  - Remove "tap trial", "shunt", "NPH" and "hydrocephalus" from the chief complaint and HPI.
  - Keep a prior diagnosis of a different disease (AD in P01 and P09, PD in M05 and P02, PSP-like syndrome in P07, bvFTD in P04): it is the anchor the case tests.
- P06 PMH: "Breast cancer (lumpectomy, radiation and chemotherapy 6 years ago, in clinical remission on tamoxifen)".
- P07: remove the NPH self-research. "The son brought printed notes on balance disorders" may replace it.

### C4. The exam gives the gait-assessment and cognitive-screen results

**Found:** most `neurological_exam` blocks give the TUG, 10-m walk, step counts or MoCA. Those are the result of the required `perform_clinical_assessment`.

**Fix:**

- **`gait`:** keep only qualitative bedside observation, for example "broad-based, short-stepped, magnetic gait with en-bloc turning; needs one hand-hold".
- **`mental_status`:** "Alert, attentive, slowed responses; formal cognitive screening reported separately".
- **Prior scores:** a prior outpatient MoCA or MMSE may stay in the HPI only if it differs from the baseline score in the assessment report (it documents decline).
- **Moving the numbers:** move the exam numbers into the baseline clinical-assessment report (C6) when that report does not already have them. When the report has different numbers, the report wins.

### C5. Tool reports that state the diagnosis, the tap verdict or the management (Kind 1 leakage)

**Found:**

- MRI impressions say "meets imaging criteria for iNPH", "consistent with NPH" or "shunt-responsive pattern".
- M05 says "consistent with Parkinson's disease".
- P07 says "missed on prior read".
- CSF interpretations say "shunt responsive", "supports shunting" or "positive tap trial: refer".
- Lab summaries recommend actions.
- Gait reports carry `criteria_met` with engineering keys and a "shunt responsiveness" synthesis.
- One gait report carries the engineering sentence "this is what the case's own tap-trial report states".

**Fix:** each report states its own modality's findings only.

- **MRI impression** canonical form: "Communicating ventriculomegaly (Evans index <x>) with <DESH morphology / an acute callosal angle of <y> degrees / temporal horn enlargement> and no obstructing lesion". It never names iNPH, a shunt or a disease.
- **CSF interpretation** canonical form: "Normal opening pressure and normal CSF cell count, protein and glucose. After removal of <n> mL, TUG changed from <a> s to <b> s at 2 hours and <c> s at 24 hours (<d>% at 24 hours); 10-m walk <e> s to <f> s; MoCA <g> to <h>". Use the case's own figures, and give 2-hour values only if the case has them.
  - No "positive", "responsive", "supports shunt" or "refer".
  - P08: report the figures without calling the tap negative either.
- **Labs:** see C9.
- **Assessment reports:** see C6.

### C6. Gait assessment: the baseline report already contains the post-tap result

**Found:**

- The single `initial_tool_outputs.clinical_assessment` holds the baseline, the post-tap values in `pre_post_comparison`, and a verdict in `criteria_met`. So the first, pre-tap gait call returns the tap outcome before the tap.
- There is no follow-up for the post-tap reassessment, although Reviewer 1 ruled the gait assessment "before and after the tap".

**Fix:**

1. **Initial `clinical_assessment` becomes the baseline only.**
   - `assessment_type: "gait_and_balance_timed"`.
   - `scores`: TUG (s), 10-m walk time (s) and steps, 180-degree turn steps, and the MoCA from the same session if the case reports one.
   - `findings`: the qualitative gait features (magnetic, broad-based, short steps, en-bloc turns, freezing on turning, retropulsion on pull test) and urinary urgency if the case documents it.
   - `criteria_met`: null. `pre_post_comparison`: null.
   - `impression`: one descriptive sentence, for example "Slow, short-stepped, broad-based gait with en-bloc turning and impaired postural reflexes".
   - `recommended_actions`: [].
2. **The CSF tap report** carries the post-tap figures, in the C5 canonical form.
3. **Add a follow-up** for the post-tap reassessment:
   - `tool_name: "perform_clinical_assessment"`, `trigger_action: "request_post_reassessment"`;
   - its output has `assessment_type: "gait_and_balance_timed (post-tap reassessment)"`, the same measures at 2 hours (if the case has them) and at 24 hours, and a `pre_post_comparison` with baseline, post value and % change, all identical to the CSF report;
   - `impression`: descriptive, for example "TUG 32% faster and 10-m walk 33% faster at 24 hours than at baseline".
   - Why this trigger (simulated 24 October 2026): a plain `repeat_clinical_assessment` leaked the post-tap result to the baseline call in 5/5 contexts when the cognitive screen came first; `request_post_tap_reassessment` leaked on "before tap test" (4/5); `request_post_reassessment` leaked 0/5 and served 4/6 post-tap phrasings (a miss returns the baseline again, no leak). Never put "tap" in the trigger.
4. **Add a `recommended` criterion** `perform_clinical_assessment {"assessment_type": "gait_and_balance_timed"}`, label "Post-tap timed gait reassessment", placed after the CSF criterion.
   - Its pattern is identical to the required baseline criterion. The reward therefore cannot tell the two calls apart, and the criterion only makes the second call a credited action (CENTRAL R4).
   - **No sequence constraint may name it.** A constraint between two identical-pattern criteria always counts as a violation.
5. **Cognitive screen.** Add an `optional` criterion `perform_clinical_assessment {"assessment_type": "cognitive_screen"}`.
   - Add a case-authored follow-up with `trigger_action: "request_moca_cognitive_screen"`. Its output has `assessment_type: "cognitive_screen"` and the baseline MoCA with domain subscores that fit the case: attention, executive and delayed-recall deficits with cueing benefit in iNPH; the case's own profile in copathology cases.
   - This prevents the library from answering with a normal MoCA.
   - The follow-up is served by the discriminator, as simulated.

### C7. MRI reports: missing markers, spine findings, impossible values

**Found:**

- Most reports lack a technique line and several of Reviewer 1's markers (callosal angle, temporal horns, aqueduct, fourth ventricle, hippocampi). The impression is diagnostic (C5).
- Brain MRI reports describe the spine: M04 cervical, M07 lumbar, P03 C3-C6.
- M10 compares with the lumbar MRI.
- M07 Evans 0.30 fails F2.
- M01, M02, M04 to M09: no DESH, and some lack any other supportive feature, while their differentials argue from DESH.
- S09: "contrast not given given CKD 2".

**Fix:** each MRI report has these elements, with the case's own values:

1. **Technique:** "1.5T/3T brain MRI: sagittal T1, axial T2, FLAIR, DWI, SWI, coronal T2 or 3D T1 for callosal angle and hippocampi; no contrast".
   - Contrast is not needed for this question. Do not give a renal reason.
2. **Evans index** greater than 0.3, measured.
3. **Callosal angle** in degrees.
4. **Temporal horns:** enlarged or not, and whether out of proportion to the hippocampi.
5. **DESH:** state both components, present or absent.
6. **Periventricular signal**, with the Fazekas grade.
7. **Aqueduct:** patent, with or without a flow void. **Fourth ventricle:** normal or mildly enlarged.
8. **No obstruction:** "No obstructing lesion, mass or aqueductal stenosis".
9. **Hippocampi:** MTA score (0 to 4).
10. **Case-specific findings:** remote infarct (M03), burr holes and no residual collection (M06), SAH coil artefact (P05), TBI changes (M09), SWI nigrosome finding (M05 and P02, C8), midbrain and pons measures (P07).

Other rules:

- Delete spine findings and M10's lumbar comparison. The spine belongs to `order_body_imaging {"study": "spine_MRI"}` (C14).
- **M07:** Evans 0.32 with temporal horn enlargement out of proportion to hippocampal volume.
- **M02:** add temporal horn enlargement.
- **Every case without DESH:** give at least one supportive feature (an acute callosal angle, or temporal horns), and remove DESH arguments from the differential, key evidence and musts.

### C8. Imaging carry-over and the PD cases

**Found:** M05's MRI says "consistent with Parkinson's disease". P07 says "missed on prior read", and its "MPAR 0.55" is mislabelled.

**Fix:**

- **M05 and P02:** state the SWI finding only: "Loss of the dorsolateral nigral hyperintensity (swallow-tail sign) bilaterally". No disease name.
- **P07:**
  - midsagittal midbrain anteroposterior diameter in mm;
  - "Midsagittal midbrain-to-pons diameter ratio 0.55" (F10);
  - no hummingbird sign;
  - remove "missed on prior read".

### C9. Lab template carry-over

**Found:**

- The criterion asks for broad panels.
- 25 cases carry an HIV row whose `clinical_significance` is "Baseline workup".
- Interpretations and summaries are interpretive and give management.
- HbA1c references and flags are inconsistent.
- M01, M09, S03 and S11 list "diet-controlled" diabetes with metformin.
- S09's creatinine of 1.4 does not match CKD stage 2.
- M03, M06 and S10 have anti-Xa rows and management text ("Held 48h ... protocol").
- P06 CA 15-3 is 28 with reference "<28", flagged inconsistently.
- P07's PSA summary is interpretive.

**Fix:**

- **Criterion:**
  - `interpret_labs {}` (empty `required_arguments`), `optional`, in every case except those listed below.
  - `recommended` where a case-specific mimic or safety question exists: M04 and S08 (TSH, hypothyroidism), M07 (B12 and MMA, metformin), M08 (CBC and coagulation; criterion `interpret_labs {"panels": ["CBC", "coagulation"]}`).
  - Label "Targeted labs for reversible contributors" (or the case's safety question).
- **Fields:** every row's `clinical_significance` is null, as the style guide requires. The `interpretation` states the pattern only, for example "Normal blood count, electrolytes, renal and thyroid function".
- **HbA1c:** reference "<5.7%", flagged high when 5.7% or above. Where metformin is listed, change the PMH to "Type 2 diabetes mellitus on metformin" (keep the HbA1c the case gives).
- **S09:** creatinine 1.1 mg/dL with an eGFR of 60 to 89, matching CKD stage 2.
- **M03, M06, S10:** delete the anti-Xa rows and all hold or management text. A DOAC level is not part of this work-up.
- **P06:** CA 15-3 22 U/mL, normal (in remission).
- **P07:** PSA value and reference only.
- **M07:** B12 202 pg/mL (low-normal) with raised MMA (for example 0.52 umol/L) and normal folate. This is a real contributor (C11 must).
- **M08:** move the INR to a `coagulation` panel row. Keep platelets 88 and INR 1.4 (F9).
- **M10:** delete the must "Obtain reversible-cause labs".

### C10. Advanced imaging and neuropsychology: ruled out, but the library would contradict the case

**Found:**

- No case has a criterion for DaTscan, amyloid PET, FDG PET or a neuropsych battery.
- Several cases have no case output for them, so the library would serve a normal report that contradicts the case: DaTscan normal in M05 and P02, amyloid normal in P01, FDG normal in P04, a normal battery in P09.

**Fix:**

- Add `avoided_actions` with `severity: "waste"` (Reviewer 1 ruling):
  - `order_advanced_imaging` (any modality), rationale "Molecular or advanced imaging does not change the iNPH decision, which rests on MRI and the tap test";
  - `order_specialized_test {"test_type": "neuropsych_battery"}`, rationale "A full neuropsychological battery is not needed for the iNPH decision; the bedside screen and timed gait measures are".
- Author consistent outputs where the library normal would contradict the case, as a follow-up whose discriminator field is the vocabulary term:
  - M05 and P02 DaTscan: reduced bilateral putaminal uptake, asymmetric (binary read);
  - P01 amyloid PET: positive (binary read);
  - P04 FDG PET: bilateral frontal and anterior temporal hypometabolism, descriptive.
- **P09:** the neuropsych battery is `optional`, not waste. Author the battery follow-up: severe executive and processing-speed impairment, free recall reduced with normal recognition and cueing benefit, preserved naming. P09's prohibition about recognition memory otherwise refers to data no tool returns.

### C11. Musts: process steps instead of case management

**Found:** most musts are process steps:

- "MRI before LP";
- "Document baseline gait";
- "Remove 30-50 mL";
- "Reassess at 2-4 and 24 h".

The criteria and constraints already score these. Case-specific management is missing, and P09 has no referral must.

**Fix:**

- Delete the four process musts.
- Keep or write, per case, 3 to 5 musts from this list (section 4 picks):
  - **Referral (all cases):** "Refer to neurosurgery for CSF shunting with a programmable valve, on the basis of <the tap-test improvement of n% in TUG at 24 hours / the extended drainage response>, the <DESH / supportive> MRI and normal-pressure CSF [Nakajima_2021]".
  - **P08:** "Do not stop at the single negative tap test; proceed to extended lumbar drainage, which has a higher sensitivity [Marmarou_2005]", plus the referral must after the drainage response.
  - **Copathology (M05, P01, P02, P03, P04, P07 if relevant):** "Counsel that shunting is expected to improve gait more than <cognition/parkinsonism/myelopathy features>, and that <the coexisting disease> continues to need its own treatment".
  - **Falls, where the case documents falls:** "Falls-prevention measures (physiotherapy, home assessment, walking aid) while awaiting surgery".
  - **Comorbidity musts** as C2 (DOAC, aspirin, levodopa, gabapentin and baclofen), plus:
    - M07: "Replace vitamin B12 and recheck MMA, as a possible contributor to gait and cognition";
    - M04 and S08: "Confirm euthyroid status";
    - S07: "Continue CPAP; untreated OSA contributes to cognitive slowing";
    - P05: "Continue treatment of post-SAH depression";
    - M09: "Continue sertraline and address post-TBI depression in parallel".
  - **Secondary NPH (M06, M08, M09, P05):** name the antecedent in the referral must.

### C12. Prohibitions: a wrong criterion and template carry-over

**Found:** every case has the prohibition "Do not diagnose NPH without DESH, callosal angle <90°, and the clinical triad". That is wrong under F1 and F2. The AD prohibition is copied into cases where AD is not in question.

**Fix:**

- Replace it with the canonical text: "Do not diagnose iNPH from ventriculomegaly alone: the diagnosis needs the clinical syndrome (gait disturbance with cognitive or urinary symptoms) and supportive imaging, with no other cause explaining them [Relkin_2005]".
- Keep the AD prohibition only in P01 and P09 (and wherever the case's differential keeps AD at moderate).
- Add the case-specific prohibitions per section 4:
  - "Do not perform the lumbar tap while <apixaban/rivaroxaban> is active and do not bridge with heparin [ASRA_2018]" (M03, M06, S10);
  - "Do not stop aspirin for the lumbar tap" (M10, P05, S06);
  - "Do not withhold shunt referral solely because of <AD/PD/bvFTD/myelopathy>" (copathology cases);
  - "Do not exclude shunt-responsive iNPH on a single negative tap test" (P08).
- At most 5 prohibitions per case.

### C13. Differential not updated to the assessment-time view (ruling 7)

**Found:** VCI or subcortical SVD is "high" in 26 of 30 cases, whatever the Fazekas grade. PD, AD and atrophy ex vacuo are "moderate" after DESH and a positive tap. Copathology entries ("AD alone", "PSP alone") are "high". In M09 "static post-TBI sequelae" is "high".

**Fix:** set the likelihoods for the state after MRI, gait and tap.

- **VCI:** `moderate` only when the MRI has Fazekas 2 or higher or lacunes; otherwise `low`.
- **PD, AD, atrophy ex vacuo:** `low` after a positive tap with supportive MRI, unless section 4 keeps one open (M02 and M07 equivocal imaging).
- **"X alone" copathology entries:** `low`. The case diagnosis already names the copathology.
- **M09:** "Chronic post-traumatic encephalopathy / static sequelae" `low`; "Post-TBI depression with pseudodementia" `low`; "iNPH" `very_low` (an antecedent exists).
- **P08:** "Non-shunt-responsive ventriculomegaly" and "Atrophy ex vacuo" `low` after the drainage response.
- **P06:** "Leptomeningeal carcinomatosis" `low` after negative cytology.
- **P07:** delete the leptomeningeal carcinomatosis entry (C15). "PSP" `low` per F10.
- Each entry's reasoning is one sentence citing the case's own data.

### C14. Spine imaging where the case has a spinal mimic

**Found:**

- M04 (prior C5-C6 discectomy) and P03 (severe CSM after fusion) put spine findings in the brain MRI.
- P03 has an `order_body_imaging` follow-up `request_spine_MRI` with "{}" placeholder strings in its signal fields.
- M07 and M10 have documented lumbar stenosis.

**Fix:**

- **P03:** add a `recommended` criterion `order_body_imaging {"study": "spine_MRI"}`.
  - Fix the follow-up: real signal text, solid fusion C3 to C6, no new compression, the old cord T2 signal stable.
  - Label "Cervical spine MRI for recurrent compression".
- **M04:** the same recommended criterion, with a new follow-up: post-discectomy C5-C6 change, no cord compression or myelopathic signal.
- **M07 and M10:** an `optional` criterion with the same pattern and an authored lumbar MRI consistent with the history (moderate L4-L5 central stenosis, unchanged). It is optional because the gait phenotype and the tap response already separate the two.

### C15. P07 template carry-over from a breast-cancer case

**Found:** P07 (a man with prostate cancer on surveillance) has a red herring "Past breast cancer (currently in clinical remission)", a differential entry for leptomeningeal carcinomatosis, a cytology prohibition, and `metadata.case_body_concerns` about it.

**Fix:**

- Delete the red herring, the differential entry and the prohibition.
- Clear `case_body_concerns`.
- Check that no other field of P07 mentions breast cancer, tamoxifen or cytology.

### C16. P08 extended lumbar drainage can hijack the index tap

**Found:** the P08 follow-up `request_extended_lumbar_drainage` shares the token "lumbar" (and the alias of "lp") with an ordinary tap call. A context such as "large-volume lumbar puncture" receives the drainage result at the first call.

**Fix:**

- Rename the trigger to `repeat_csf_analysis`. This is a plain trigger, served only on the second `analyze_csf` call, as simulated.
- The output stays the drainage report.
  - Remove interpretive text such as "confirms shunt responsiveness".
  - Keep the volume and the day-by-day TUG and 10-m walk figures.
  - Use `source: "lumbar_puncture"` until CENTRAL R3 adds a drain term.
- Add a `recommended` criterion `analyze_csf {}`, label "Extended lumbar drainage after the negative tap", placed after the tap criterion. No sequence constraint names it, because its pattern is identical to the tap criterion.
- Update the P08 red herring to the F4 figures.

### C17. CSF follow-ups must repeat the whole tap report

**Found:** P01's AD-biomarker follow-up (`request_targeted_csf_abeta42_phospho_tau`) and P06's cytology and flow follow-up (`request_targeted_csf_cytology_flow`) contain only the assay. An agent that orders the tap and the assays in one call receives no opening pressure, cells or tap response. P01's interpretation is garbled.

**Fix:**

- Each such follow-up repeats the full tap report (C5 canonical form) and adds `special_tests` with the assays.
- **P01:**
  - Aβ42 low, Aβ42/40 ratio low, p-tau181 high;
  - interpretation "CSF Aβ42/40 ratio reduced and phosphorylated tau raised (A+T+ profile)";
  - criterion `recommended`, alternatives `["Abeta42_40_ratio", "phospho_tau"]` and `["Abeta42", "phospho_tau"]` in `special_tests`.
- **P06:** cytology negative for malignant cells and flow cytometry without an abnormal population. The criterion is `required`, alternatives `["cytology"]` and `["cytology", "flow_cytometry"]`.
- **P09:** an `optional` criterion with the same AD alternatives as P01, and an authored follow-up (full tap report plus normal biomarkers: ratio normal, p-tau normal). The AD anchor can then be tested and refuted by data.

### C18. Fallback outputs that contradict the case

**Found:**

- In 29 cases the CT fallback says "No acute intracranial abnormality ... ventricles normal" against ventriculomegaly.
- M03's CT fallback says "no established infarct" against the remote left MCA stroke.
- M06's fallbacks do not mention the burr holes.
- The echo and ECG fallbacks of M03, M06 and S10 are normal sinus rhythm with AF in the history.
- The echo fallbacks say "benign incidental finding".

**Fix:**

- **CT fallback:** "Enlarged lateral and third ventricles (Evans index about <x, the MRI value ±0.01>), no mass, haemorrhage or midline shift". Add the case's own lesions:
  - M03: an old left MCA infarct;
  - M06: bilateral burr holes, no residual collection;
  - P05: coil artefact;
  - M09: a right frontal encephalomalacic focus.
  - No comparison wording.
- **ECG and monitoring:**
  - M03 and S10: sinus rhythm is acceptable for paroxysmal AF.
  - M06: its PMH says only "Atrial fibrillation (CHA2DS2-VASc 4)". Make it "paroxysmal", so the sinus ECG stays consistent, and log it.
- **Echo:** remove "benign incidental finding" and similar phrasing. State the findings.
- **S06 and S10:** delete the echo follow-up ("cardiac clearance pre-shunt") and the monitoring follow-up (`request_cardiac_monitoring_af`).
  - S10's red herring becomes "Known paroxysmal atrial fibrillation on apixaban", with the same correct interpretation.

### C19. Metadata and criterion text

**Found:**

- `key_clinical_evidence` contains "Tier per the July 2026 clinical review" in 30 cases.
- 21 cases carry a stale `vocab_gap` note about phase-contrast MRI.
- `difficulty_rationale` counts tools that are now removed.
- Criterion rationales repeat the label.

**Fix:**

- Remove the tier sentences.
- Delete the phase-contrast `vocab_gap` notes. Flow quantification is not needed; the aqueductal flow void is reported in the MRI.
- Update the counts in `difficulty_rationale`.
- Every criterion's rationale must be one case-specific sentence that differs from its label.
- Every `expected_evidence` must match its case output.

### C20. Red herrings

**Fix:**

- Each red herring's `data_point` must be visible to the agent: the patient block, or an output on the pathway.
- Its `correct_interpretation` must be one sentence that agrees with F1 to F10.
- Delete a red herring that refers to a deleted output (S10 monitoring, as in C18; literature items).
- The recurring "Long-standing type 2 diabetes (potential peripheral neuropathy)" (M01, M07, P03, S03, S04, S09) stays only if the exam documents distal sensory loss or reduced ankle reflexes. Otherwise delete it.

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers

| # | criterion | tool and `required_arguments` | tier |
| --- | --- | --- | --- |
| 1 | brain MRI | `analyze_brain_mri {}` | required |
| 2 | labs | `interpret_labs {}` (M08: `{"panels": ["CBC", "coagulation"]}`) | optional; recommended in M04, M07, M08, S08 |
| 3 | baseline timed gait | `perform_clinical_assessment {"assessment_type": "gait_and_balance_timed"}` | required |
| 4 | cognitive screen | `perform_clinical_assessment {"assessment_type": "cognitive_screen"}` | optional |
| 5 | spine MRI | `order_body_imaging {"study": "spine_MRI"}` | recommended in M04 and P03; optional in M07 and M10 |
| 6 | CSF tap test | `analyze_csf {}` (P06: cytology alternatives, C17; P01: AD alternatives, C17) | required |
| 7 | post-tap reassessment | `perform_clinical_assessment {"assessment_type": "gait_and_balance_timed"}` | recommended |
| 8 | extended lumbar drainage (P08) | `analyze_csf {}` | recommended |
| 9 | CSF AD biomarkers (P09) | as C17 | optional |
| 10 | neuropsych battery (P09) | `order_specialized_test {"test_type": "neuropsych_battery"}` | optional |

There is no literature, drug-check, advanced-imaging, ECG, echo or monitoring criterion.

**P01:** the CSF criterion stays `analyze_csf {}` required. A separate `recommended` criterion carries the AD alternatives, and its follow-up repeats the tap report (C17).

**P06:** the cytology alternatives are on the required CSF criterion itself. A tap without cytology does not exclude the alternative the case tests.

### 3.2 Follow-ups and initial outputs

Order the follow-ups as in 3.1. Every required and recommended criterion must be served by a case output, never by the library. Simulated recipes:

- **Post-tap reassessment:** trigger `request_post_reassessment`, prose `assessment_type` (C6).
- **Cognitive screen:** trigger `request_moca_cognitive_screen`, `assessment_type: "cognitive_screen"`. It is served by the discriminator at any call.
- **P08 drainage:** trigger `repeat_csf_analysis`, a plain trigger served on the second CSF call (C16). It is served correctly even when the second call says "extended lumbar drainage 72 h".
- **CSF assay follow-ups:** the full report (C17). An assay follow-up is reached only when the call names the assays.
- **Advanced imaging (C10):** the discriminator is the `modality` term.

Initial outputs for EEG, ECG, echo and monitoring are kept null. Their fallbacks must follow C18.

### 3.3 `avoided_actions`

- **Keep** EEG, ECG, echo and cardiac monitoring as `waste`. CT stays `waste` only when an MRI is available (all 30 cases).
- **Add** `order_advanced_imaging` and the neuropsych battery as `waste` (C10). P09 omits the battery entry.
- **Add** the generic CSF assays Reviewer 1 removed as `waste`: `analyze_csf {"special_tests": ["14_3_3"]}`, RT-QuIC, oligoclonal bands and PCR panels, only where the vocabulary has the term. Not in P01, P06 or P09 for their own assays.
- **Rationales:** one case-specific sentence each.

### 3.4 Sequence constraints

- MRI before CSF: `hard`. Reason: "Brain imaging must exclude a mass or obstructive hydrocephalus before CSF is removed [Relkin_2005]".
- Baseline gait before CSF: `soft`. Reason: "The baseline gait must be measured before the tap, or the post-tap change cannot be interpreted [Nakajima_2021]".
- Do not add any other constraint. In particular, never one that names the post-tap criterion (7) or the P08 drainage criterion (8): their patterns equal criteria 3 and 6 (C6, C16).

### 3.5 Stop rule

- `required_before_assessment`: the ids of the required criteria (MRI, baseline gait, CSF; plus P06's cytology through its CSF criterion).
- `max_additional_actions: 1`.

### 3.6 Check after editing

- `uv run python data/review/round-2026-10/bin/perfect_agent.py <ID> -v` passes. In the `-v` output, every required and recommended action is served by a case output, not by the library or a fallback.
- `uv run python data/review/round-2026-10/bin/case_io.py check <ID>` passes.
- `uv run pytest agent-platform/tests/test_case_guards.py -q -k <ID>` passes, including the leak test.
- Hijack check (`MockServer(case).get_output`, script in its own folder): `cognitive_screen` then `gait_and_balance_timed` "baseline before tap test" returns the baseline; after the CSF call, "post-tap reassessment" returns the follow-up.
- Grep the patient block for Evans, callosal, DESH, NPH, hydroceph, tap, shunt, TUG, MoCA: each hit allowed by C3 or C4.

---

## 4. Per-case index

The figures are the case's own. "Tap" means the tap-test change in TUG at 24 hours. Every case receives C1, C2, C3, C4, C5, C6, C7, C9, C11, C12, C13, C18, C19 and C20. The bullets list only what is specific to the case.

### NPH-M01 (man, 68, iNPH; tap 22 to 16.5 s, 25%)
- C1: leak-test failure; delete `literature_search["general"]`.
- PMH: "Type 2 diabetes mellitus on metformin (HbA1c 7.2%)" (C9). Keep the BPH. Urinary urgency is attributed to iNPH only if the exam or HPI supports it; otherwise it is mixed. Say so in the assessment.
- MRI has no DESH. Give an acute callosal angle and temporal horn enlargement (C7).
- Red herring on diabetic neuropathy: keep only if distal sensory loss is in the exam (C20).
- Differential: VCI low unless Fazekas is 2 or more.
- Musts: referral; falls if documented.

### NPH-M02 (woman, 71, iNPH; tap 28 to 21.5 s, 23%)
- C1 leak. C2: delete `request_drug_interactions_preop`.
- MRI: add temporal horn enlargement and the callosal angle (C7). No DESH. Keep AD at `moderate` only if the MRI's MTA is 2 or more; otherwise low.
- Depression in remission on sertraline: one sentence in the assessment, not a must.
- Left TKR: the gait report notes the knee does not explain the magnetic gait.
- Musts: referral; falls.

### NPH-M03 (man, 72, iNPH, paroxysmal AF on apixaban, remote left MCA stroke; tap 17%)
- C1 leak. C2: delete the drug-check criterion and `request_drug_interactions_shunt_anticoagulation`. DOAC must and prohibition (C2, C12).
- Labs: delete the anti-Xa rows and the hold text (C9).
- MRI: the old left MCA infarct and Fazekas grade belong in the report. VCI `moderate` if Fazekas is 2 or more.
- Red herring on the remote stroke stays: its residual right-hand weakness does not explain the bilateral magnetic gait.
- CT fallback shows the old infarct (C18).
- Musts: referral; DOAC; falls.

### NPH-M04 (woman, 66, iNPH, prior C5-C6 discectomy, hypothyroidism, gabapentin; tap 21%)
- C1 leak. C2: delete `request_drug_interactions_gabapentin_shunt`. Gabapentin must.
- C7: delete the cervical findings from the brain MRI.
- C14: recommended spine MRI with a new follow-up: no compression or cord signal.
- Labs `recommended`: TSH and free T4 normal on levothyroxine (C9). Euthyroid must.
- Differential: CSM `low` after the spine MRI. VCI low unless Fazekas is 2 or more.
- Red herrings: both stay, and their interpretations name the spine MRI and the TSH.

### NPH-M05 (man, 69, iNPH with PD, carbidopa-levodopa; tap in the ON state, 38 to 31 s)
- C1 leak. C2: delete `request_drug_interactions_periop`. Levodopa must.
- C8: the MRI states the SWI finding, not "consistent with Parkinson's disease". C10: authored DaTscan follow-up, abnormal.
- Make the MRI and the differential agree on DESH. If the report has no DESH, delete the DESH reasoning.
- Differential: "PD progression alone" `low` (the copathology label covers PD).
- Musts: referral with the copathology counselling (gait benefit expected, PD treatment continues); levodopa; falls.
- Prohibition: do not withhold referral because of PD.

### NPH-M06 (man, 74, secondary NPH after bilateral SDH evacuation 14 months ago, AF on rivaroxaban; tap 31%)
- C2: delete `request_drug_interactions_shunt_anticoagulation`. DOAC must and prohibition, with rivaroxaban held for at least 72 hours.
- C1: delete `request_literature_secondary_nph`.
- PMH: "Atrial fibrillation (paroxysmal, CHA2DS2-VASc 4)" (C18).
- MRI and CT fallback: burr holes and no residual collection. MRI has no DESH, so give the supportive features.
- Labs: delete anti-Xa and management rows.
- Differential: "Post-traumatic / post-SAH / post-meningitic" becomes the case's own secondary aetiology. Keep it out of the differential, because it is the diagnosis; replace it with "iNPH" `low` (an antecedent exists).
- Musts: referral naming the SDH antecedent; DOAC; falls.
- Prohibition: DOAC.

### NPH-M07 (woman, 67, iNPH, poorly controlled T2DM on metformin and insulin, lumbar stenosis, meloxicam; tap 20%)
- C1 leak. C2: delete `request_drug_interactions_b12_metformin`.
- C7: Evans 0.32 with temporal horns, and delete the lumbar findings from the brain MRI.
- C9: labs `recommended`, with B12 202 and raised MMA. B12 must.
- C14: optional lumbar spine MRI.
- Meloxicam is an NSAID; no hold for the LP (no must needed).
- Morbid obesity: the gait report records it. It does not explain the magnetic gait.
- Differential: lumbar stenosis `low` (tap response and gait phenotype); AD and atrophy `low`.
- Red herrings: lumbar stenosis stays; neuropathy per C20.

### NPH-M08 (man, 65, secondary NPH after pneumococcal meningitis 8 years ago, alcoholic cirrhosis; tap 22%)
- C1 leak. C2: delete `request_drug_interactions_shunt_cirrhosis`.
- PMH: lactulose and rifaximin imply prior hepatic encephalopathy, which contradicts "compensated". Write "Alcoholic cirrhosis (Child-Pugh A, one episode of overt hepatic encephalopathy 2 years ago, on lactulose and rifaximin; abstinent 5 years)".
- Labs `recommended`: `{"panels": ["CBC", "coagulation"]}`, platelets 88 and INR 1.4 (F9). An ammonia value may be added, normal.
- Red herring (hepatic encephalopathy) stays: no asterixis, normal ammonia, and a gait-predominant syndrome.
- Differential: the meningitis aetiology is the diagnosis. Replace the generic secondary entry with "iNPH" `low` and "covert hepatic encephalopathy" `low`.
- Musts: referral naming the post-meningitic antecedent; continue lactulose and rifaximin; falls.

### NPH-M09 (man, 64, post-traumatic NPH 8 months after severe TBI with tSAH and IVH; tap 23% at 2 hours, 32% at 24 hours)
- C1: literature `required`. Delete it and remove it from the stop rule; delete `request_literature_post_traumatic_nph`.
- PMH: "Type 2 diabetes mellitus on metformin".
- Onset is subacute after the TBI, so F1's idiopathic onset rules do not apply. The diagnosis is secondary (F6). CENTRAL R1 adds G91.3.
- MRI: give the TBI changes (haemosiderin on SWI, a 1.2 cm right frontal encephalomalacic focus) and the supportive features (no DESH).
- Differential per C13: static sequelae `low`, pseudodementia `low`, iNPH `very_low`.
- Musts: referral naming the TBI antecedent; continue sertraline and treat depression in parallel; falls.
- Both red herrings stay.

### NPH-M10 (man, 72, iNPH, L4-L5 stenosis with deferred decompression, aspirin; tap 28 to 19 s)
- C1: literature `required`. Delete it and remove it from the stop rule.
- C7: delete the lumbar comparison from the brain MRI.
- C14: optional lumbar spine MRI, consistent with the moderate L4-L5 stenosis.
- C9: delete the must "Obtain reversible-cause labs".
- Aspirin must and prohibition.
- Differential: lumbar stenosis `low` (the gait improves with the tap and is not claudicant). Keep VCI `moderate` (Fazekas 2).
- Musts: referral, with a recommendation that the spine decision be revisited after the shunt response; aspirin; falls.

### NPH-P01 (man, 75, iNPH with AD, donepezil and memantine; tap 42 to 34 s, 19%)
- C1: delete both literature follow-ups, including `request_multidisciplinary_conference`.
- C17: a `recommended` AD-biomarker criterion, with a follow-up that repeats the full tap report and gives an A+T+ profile.
- C10: authored amyloid PET, positive (waste).
- Differential: "AD alone" `low`; VCI `moderate` (Fazekas 2 to 3).
- Musts: referral with the copathology counselling (gait benefit expected, cognitive benefit limited); continue donepezil and memantine.
- Prohibitions: do not withhold referral because of AD; keep the AD prohibition.

### NPH-P02 (woman, 72, iNPH with PD, levodopa, pramipexole and sertraline; tap in the ON state, 29 to 23 s)
- C1: delete both literature follow-ups, including `request_msa_exclusion`. If MSA is in the differential, keep it `low` with its reasoning: no dysautonomia and no MRI pontine or putaminal signs.
- C2: delete `request_levodopa_perioperative_plan`. Levodopa and pramipexole musts.
- C8: SWI finding only. C10: authored DaTscan, abnormal.
- Differential: "PD progression alone" `low`; VCI `low` (Fazekas 1).
- Musts: referral with copathology counselling; levodopa; pramipexole review.
- Prohibition: do not withhold referral because of PD.

### NPH-P03 (man, 78, iNPH with severe CSM after C3-C6 fusion, gabapentin and baclofen; tap 22%)
- C1: delete `request_literature_myelopathy_nph_differentiation`. C2: delete `request_gabapentin_baclofen_interaction`; gabapentin and baclofen must.
- C7: delete the C3-C6 findings from the brain MRI.
- C14: recommended spine MRI, with the follow-up fixed.
- Differential: "Recurrent CSM" `low` after the spine MRI (the label already names CSM).
- Musts: referral with counselling (myelopathic features will not respond to the shunt); falls.
- Prohibition: do not withhold referral because of the myelopathy.
- Red herrings: CSM stays; neuropathy per C20.

### NPH-P04 (woman, 73, iNPH with bvFTD, sertraline; tap 18%, MoCA change)
- C1: delete `request_genetic_ftd_testing` and `request_goals_of_care_ftd_nph`. Goals of care becomes a must: "Discuss goals of care and the expected limited behavioural benefit with the patient and family before surgery".
- C10: authored FDG PET, frontal and anterior temporal hypometabolism (waste).
- Keep the prior "Evans 0.27 two years ago" in the HPI (C3).
- Differential: "bvFTD alone" `low`; VCI `low` unless Fazekas is 2 or more.
- Musts: referral with copathology counselling; goals of care; continue sertraline for the behavioural symptoms.
- Prohibition: do not withhold referral because of bvFTD.

### NPH-P05 (man, 76, secondary NPH 4 years after coiled aneurysmal SAH, verapamil, sertraline, aspirin; tap 29%)
- C1: delete `request_literature_post_sah_nph` and `request_depression_contribution`. C2: delete `request_aspirin_perioperative_shunt`. Aspirin must and prohibition.
- MRI and CT fallback: coil artefact.
- CSF: the "RBC 2 (traumatic vs old)" wording becomes "RBC 2/mcL".
- Differential: the post-SAH aetiology is the diagnosis. Use "iNPH" `low` and "post-SAH depression with cognitive slowing" `low`.
- Musts: referral naming the SAH; aspirin; continue the depression treatment.

### NPH-P06 (woman, 69, iNPH, breast cancer in remission on tamoxifen, duloxetine; tap 30%)
- C3: PMH rewritten (no "leptomeningeal carcinomatosis concern").
- C2: delete `request_oncology_comanagement`. C1: delete `request_literature_nph_cancer_survivor`.
- C17: the required CSF criterion carries the cytology alternatives, and the follow-up repeats the full tap report.
- MRI: state the absence of leptomeningeal or ependymal enhancement only if contrast was given. Otherwise the cytology answers the question; a contrast sequence is acceptable here.
- C9: CA 15-3 22.
- Differential: leptomeningeal carcinomatosis `low` after negative cytology.
- Musts: referral; inform the oncologist of the result (in the assessment, not a tool call).
- The verbose `accepted[0]` stays (CENTRAL R6).

### NPH-P07 (man, 74, iNPH with a prior PSP-like working diagnosis, prostate cancer on surveillance; tap 32%)
- C15: delete the breast-cancer carry-over. C3: delete the son's NPH research.
- C8: midbrain-to-pons ratio 0.55, no hummingbird sign, no "missed on prior read".
- C1: delete `request_literature_nph_psp_differentiation`. C2: delete `request_finasteride_perioperative`.
- C9: PSA factual.
- Exam: vertical saccades must be consistent with "PSP not supported", meaning normal velocity or only mild upgaze limitation for age. If the exam shows a vertical supranuclear gaze palsy, log it and ask. Do not edit it into the opposite.
- Differential: PSP `low` per F10.
- Musts: referral; falls.
- Prohibition: "Do not keep the PSP label without a vertical supranuclear gaze palsy or a midbrain-to-pons ratio below 0.52 [Massey_2013]". The verbose `accepted[0]` stays (CENTRAL R6).

### NPH-P08 (man, 71, iNPH with a negative single tap, 31 to 30 to 31 s; extended drainage positive, 39% at day 3)
- C1: literature `required`. Delete it and remove it from the stop rule; delete `request_literature_nph_tap_sensitivity`. The sensitivity point goes into a must and the red herring (F4).
- C16: rename the drainage trigger to `repeat_csf_analysis`; recommended drainage criterion; drainage report free of interpretation.
- CSF tap report: the figures only (C5).
- Differential: non-responsive ventriculomegaly `low` and atrophy `low` after the drainage. VCI `moderate` (Fazekas 2).
- Musts: proceed to extended drainage after the negative tap; referral on the drainage response.
- Prohibition: do not exclude shunt-responsive iNPH on a single negative tap test.

### NPH-P09 (woman, 76, cognitive-predominant iNPH with a prior early-AD diagnosis and a family history of dementia; tap 32%)
- C1: literature `required`. Delete it and remove it from the stop rule; delete `request_literature_nph_cognitive_predominant`.
- C10: an optional neuropsych battery with an authored subcortical-frontal profile, with recognition preserved. This makes the recognition-memory prohibition answerable.
- C17: optional CSF AD biomarkers, normal.
- C11: P09 has no referral must; add it.
- Differential: AD `low` once the biomarkers are normal or the profile is subcortical. VCI `moderate` (Fazekas 2).
- Musts: referral; review of the prior AD diagnosis with the patient and family.
- Prohibitions: keep the AD and family-history prohibitions, reworded per C12.

### NPH-S01 (man, 73, iNPH; tap 28 to 18 s, 36%)
- C1 leak. C2: delete `request_drug_interactions_shunt`.
- The baseline exemplar for C6: read the S01 gait report and remove the post-tap part, the `criteria_met` keys and the engineering sentence.
- Musts: referral; falls if documented.

### NPH-S02 (man, 76, iNPH, BPH; tap 32%)
- C2: delete the fake consult `request_neurosurgery_consultation`. C1: delete `request_literature_nph_shunt`.
- Urinary symptoms with BPH on tamsulosin: the assessment says urgency may be mixed.
- Musts: referral.

### NPH-S03 (woman, 78, iNPH; tap 34%)
- C1: delete `request_literature_iNPH_outcomes`.
- PMH: "Type 2 diabetes mellitus on metformin" (C9).
- Red herring on neuropathy per C20.
- Musts: referral; falls.

### NPH-S04 (man, 71, iNPH, T2DM on metformin and sitagliptin; tap 32%)
- C1: delete `request_literature_npH_parkinsonian_features`. If the exam has parkinsonian features, the assessment explains them: lower-body predominance, no rest tremor, no levodopa trial needed.
- Red herring on neuropathy per C20.
- VCI `low` (Fazekas 1).
- Musts: referral.

### NPH-S05 (woman, 74, iNPH, osteoporosis on alendronate; tap 33%)
- C1 leak. C2: delete `request_osteoporosis_perioperative_management`.
- Musts: referral; falls prevention with fracture risk (osteoporosis): "Falls-prevention measures and continued osteoporosis treatment while awaiting surgery".

### NPH-S06 (man, 80, iNPH, CAD after CABG, aspirin; tap 37%)
- C18: delete the echo follow-up `request_cardiac_clearance_pre_shunt`. C2: delete `request_aspirin_perioperative_management`. Aspirin must and prohibition.
- C1: delete `request_literature_severe_nph_outcomes`.
- VCI `moderate` (Fazekas 2).
- Musts: referral (age 80 is not a contraindication); aspirin; falls.

### NPH-S07 (man, 69, iNPH, OSA on CPAP; tap 33%)
- C1: delete `request_sleep_apnea_cognitive_contribution`. CPAP must.
- Red herring (OSA) stays: CPAP-compliant, and OSA does not cause ventriculomegaly or a magnetic gait.
- Musts: referral; CPAP.

### NPH-S08 (woman, 72, iNPH, hypothyroidism on levothyroxine; tap 35%)
- C1: delete `request_hypothyroidism_cognitive_contribution`. C2: delete `request_levothyroxine_perioperative`.
- Labs `recommended`: TSH normal. Euthyroid must.
- Red herring (hypothyroidism) stays.
- Musts: referral; euthyroid.

### NPH-S09 (man, 75, iNPH, T2DM on insulin and metformin, CKD 2; tap 35%)
- C2: delete `request_ckd_insulin_perioperative`. C1: delete `request_vascular_contribution_white_matter`.
- C9: creatinine 1.1.
- C7: delete the contrast and CKD sentence.
- VCI `moderate` (Fazekas 2). Red herring on neuropathy per C20.
- Musts: referral.

### NPH-S10 (woman, 77, iNPH, paroxysmal AF on apixaban and metoprolol; tap 33%)
- C2: delete `request_apixaban_shunt_perioperative`. DOAC must and prohibition.
- C18: delete `request_cardiac_monitoring_af` and rewrite the red herring as known paroxysmal AF. C1: delete `request_vascular_dementia_af_contribution`.
- C9: delete anti-Xa and hold text.
- MRI impression: remove "white matter changes from atrial fibrillation"; state the Fazekas grade only. VCI `low` to `moderate` per Fazekas (1 to 2: `low`).
- Musts: referral; DOAC.

### NPH-S11 (woman, 70, iNPH; tap 26 to 17 s, 35%)
- C1: literature `required`. Delete it and remove it from the stop rule; delete `request_literature_search`.
- PMH: "Type 2 diabetes mellitus on metformin".
- Red herring (white matter changes) stays: Fazekas 2 periventricular signal, which MRI marker 6 separates from transependymal flow. VCI `moderate`.
- Differential: "Cervical or lumbar spondylotic myelopathy" `low`.
- Musts: referral.

---

## 5. CENTRAL requests

- **R1. Synonyms.** Add G91.3 (post-traumatic hydrocephalus) to the accepted codes of post-traumatic secondary NPH (M09) in `diagnosis_synonyms.yaml`, then run `apply_diagnosis_synonyms.py`. G91.0, G91.2 and G91.9 are already accepted in every case.
- **R2. Citation keys.** Add `[Nakajima_2021]`, `[Halperin_2015]`, `[ASRA_2018]` and `[Massey_2013]` with the references of 1.1. Also correct the NPH criteria pack:
  - `[Relkin_2005]` pages S2-S4 should be S4-S16;
  - the tap-test "sensitivity ~50-80%" should become the F4 figures;
  - the required-tools list (neuropsych, literature) and the tiers are superseded by the July 2026 review.
- **R3. CSF source vocabulary.** Add `lumbar_drain` (extended lumbar drainage) to the `analyze_csf.source` enum in `costs.yaml`, its fallback-library entry and the `tool_io.py` mirror. P08 could then say what it is, and a criterion could tell the drainage apart from the tap.
- **R4. Assessment timing discriminator.** Make `perform_clinical_assessment.timing` an enum (`baseline`, `post_intervention`) or add a scorer discriminator.
  - Today the post-tap reassessment criterion has the same pattern as the baseline. Coverage credits it from the baseline call alone, and no sequence constraint can order the two.
  - The same applies to the P08 drainage versus the tap.
- **R5. MockServer repeat-call rule.** `is_repeat_call` counts any earlier call of the tool. A plain-trigger follow-up therefore jumps ahead when a different `assessment_type` or `modality` was called first. Count only earlier calls answered by the same initial output, or with the same discriminator value. This would make plain triggers safe for all conditions.
- **R6. Verbose labels.** `accepted[0]` of P06 ("... leptomeningeal carcinomatosis excluded") and P07 ("... prior PSP label not supported") carry reasoning in the label. Leave them unchanged this round. A central relabel should move the reasoning to the assessment.
- **R7. Library normals.** The fallback library returns normal MoCA, neuropsych, DaTscan and amyloid reports, which contradict copathology cases whenever a case lacks its own output. Consider a library tier keyed by condition, or mark those library reports as "not performed".
- **R8. perfect_agent.** Add a realistic-context mode (varied call order, contexts with "baseline", "before tap", "lumbar", "lp").

## 6. Open questions for Andrea

1. **Shunt referral as the main must.** Is that the intended assessment target for every case, including copathology? Or should a copathology case score a conditional referral ("if goals of care support surgery")? The plan uses a referral with counselling.
2. **The post-tap reassessment tier (C6).** Reviewer 1 asked for gait "before and after the tap". The plan makes the reassessment `recommended`, not `required`, because the scorer cannot tell it apart from the baseline (R4). Should it become required once R4 lands?
3. **DOAC hold length.** ASRA 2018 gives at least 72 hours for apixaban and rivaroxaban before neuraxial puncture. Some neurology services hold for 48 hours for a diagnostic LP. The plan uses ASRA; confirm.
4. **P06 cytology as required.** It is the alternative the case tests. Reviewer 1 removed generic CSF tests, but this is targeted. Keep it required?
5. **P07 exam.** If the exam shows a vertical supranuclear gaze palsy, the case's label "PSP not supported" is wrong, and the case may need to become iNPH with PSP copathology. Workers will log this, not edit it.
6. **M09 secondary NPH 8 months after TBI.** Should the case keep the "iNPH" differential entry at all, or replace it with "post-traumatic ventriculomegaly ex vacuo (atrophy after diffuse axonal injury)", the more realistic alternative? The plan keeps iNPH `very_low`. Ex vacuo should be considered too.
7. **Neuropathy red herrings (C20).** Delete them where the exam has no neuropathy signs, or add the signs to the exam? The plan deletes them, to avoid inventing findings.
