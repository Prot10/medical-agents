# SYNC-CARD round plan (November 2026)

Lead plan for SYNC-CARD M01-M05, P01-P04, RM01-RM04, RP01-RP05, RS01-RS06 and S01-S06, written
17 Nov 2026.
- Decisions and reasons: `plans/SYNC-CARD-decisions.md`. D1..D27 below refer to its entries.
- Notes: 60, all R2 (NB-87MF-FBTV-TPWE).
- Approved before this round (`work/approved.txt`): P02, P04, RM04, RP01, RS03, RS04, RS05, RS06,
  S01, S02, S04, S05, S06.

Reading:
- Read in full: M01, RM02, RP05 and RS01.
- Every other case was read through the scripted dumps: criteria, avoided actions, constraints,
  stop rule, musts, differential, follow-up list, and fallbacks with their study types.

Scripts (`/home/aprotani/review-round-2026-11/work/scratch/sync-lead/`):

| file | content |
|---|---|
| `survey_sync.py` / `survey.txt` | per-case policy dump |
| `unlabelled.py` | served follow-ups with no criterion or avoided entry |
| `fallback_decoys.py` | the same check for initial and fallback reports |
| `classes_sync.py` | driving musts, "Mobitz" wording; driving musts over the 600 cases |

Workers:
- Edit only through `case_io`. After each case, run:
  - `perfect_agent.py CASE -v`;
  - `case_io.py check CASE`;
  - `mri_probe.py`, after any MRI edit.
- Keep every `criterion_id`. New ids are given below.
- New avoided entries take the id `avoid-<severity>-<study>`, for example
  `avoid-waste-bubble-study`, `avoid-harm-exercise-echo` or `avoid-waste-coronary-angiography`.
  - Their rationale names this patient's diagnosis, in one sentence.
  - `citations` holds allow-list keys only. A source outside the allow-list is named in the
    rationale text, and its key is requested under CENTRAL C2.
- After any change to `accepted[0]` or `rejected`, test the answers named in this plan with
  `DiagnosisCriterion.matches`. Never hand-edit the synonym labels after `accepted[0]`.
- Do not remove any stored report (D3).
- Move off-pathway follow-ups after the pathway ones, in this order:
  1. ECG;
  2. labs;
  3. TTE;
  4. monitoring;
  5. second-line study;
  6. drug check;
  7. off-pathway reports.
- English in the case's spelling. No em dashes in new text. No review-process text in `metadata`.
- Update `metadata.revision_reason` and `metadata.last_revised` ("2026-11-17").
- Never write "Mobitz II" for 2:1 or 3:1 conduction in new text (C4).

## 1. Governing guidelines and canonical facts

| Key or source | Governs here |
|---|---|
| `[ESC_2018]` Brignole 2018 syncope (main text) | Definition of syncope (Table 2 exclusions: hypoxia, cardiac arrest without spontaneous recovery); Table 6 high-risk features; immediate in-hospital monitoring Class I in high risk; exercise test Class I C in exertional syncope and diagnostic when 2nd/3rd-degree AV block appears with exercise; EPS IIa only when non-invasive work-up is non-diagnostic; coronary angiography follows the usual ischaemia indications |
| ESC 2018 Practical Instructions (Brignole 2018, Eur Heart J 2018;39:e43-e80, Web Table 3) | Driving: pacemaker Group 1 after 1 week, Group 2 after device function is confirmed; ICD Group 1 after 1 month, Group 2 permanently restricted |
| EHRA 2009 driving consensus (Vijgen J et al., Europace 2009;11:1097-1107) | ICD: private driving after 3 months (secondary prevention) or 4 weeks (primary prevention) |
| `[ACC_AHA_HRS_2018_Bradycardia]` Kusumoto 2019 | AV block definitions (C4) |
| `[ESC_2021_Pacing]` Glikson 2021 | Pacing Class I for Mobitz II, high-grade and complete AV block without a reversible cause; ICD with pacing considered in sarcoid, laminopathy or LVEF 35% or lower |
| `[ESC_2022_VA_SCD]` Zeppenfeld 2022 | Induced type 1 Brugada pattern needs "no other heart disease" (IIa C); PES in post-infarct syncope unexplained after non-invasive work-up; isoproterenol or pacing for recurrent torsades in acquired LQT; ICD in sarcoid with a pacing indication should be considered (IIa); PES for risk stratification after an established secondary-prevention ICD indication is IIb |
| `[Fletcher_2013]` | Exercise testing. Absolute contraindications: uncontrolled arrhythmia causing symptoms or haemodynamic compromise, symptomatic severe AS, acute myocarditis, acute PE. Relative: high-degree AV block |
| ACR-NKF consensus (Davenport MS et al., Radiology 2020;294:660-668), ACR Manual on Contrast Media | Iodinated contrast risk material at eGFR below 30 mL/min/1.73 m2 or AKI; not at 30 or above (CI-AKI 0-2% at 30-44, near 0% at 45 or above) |
| `[Drew_2010]`; Tisdale 2020 AHA drug-induced arrhythmias (Circulation 2020;142:e214-e233) | Potassium 4.5-5.0 mmol/L in torsades (Drew); K above 4.0 mEq/L and Mg above 2.0 mg/dL on QT-prolonging drugs (Tisdale) |
| `[Gewitz_2015]` Jones 2015 | Moderate/high-risk population: polyarthralgia major; fever of 38.0 C or more, ESR of 30 or more, CRP of 3.0 mg/dL or more minor; recurrence with 2 major, 1 major + 2 minor, or 3 minor plus evidence of group A streptococcal infection |
| `[HRS_2014_Sarcoid]` | Clinical diagnosis of cardiac sarcoid: extracardiac histology plus compatible cardiac findings, no myocardial biopsy |
| Lyon 2022 ESC cardio-oncology (Eur Heart J 2022;43:4229-4361) | ICI myocarditis: troponin (serial), ECG and CMR; one normal troponin does not exclude it |
| Snook 2021 BSG IDA (Gut 2021;70:2030-2051) | Oral iron first; IV iron when oral iron is ineffective, not tolerated or inappropriate; investigate the cause |

Canonical facts:
- **F1.** A stored report answers an order. It is not a step that was taken. Label it, never delete
  it (D3).
- **F2.** Conduction arithmetic:
  - ventricular rate = atrial rate / conduction ratio;
  - a pause of n consecutive non-conducted P waves = (n+1) x P-P interval.
- **F3.** Patients' eGFR by CKD-EPI 2021, from the stored creatinine:

  | Case | eGFR |
  |---|---|
  | S03 | 27 |
  | RS02 | 42 |
  | RS03 | 49 |
  | S01 | 59 |
  | RS05 | 59 |
  | M03 | 65 |
  | M01 | 68 |
  | RM03 | 78 |
  | P01 | 89 |
  | RP02 | 124 |

  Only S03 is at contrast risk.

## 2. Classes

### C1 EXERCISE-EXERTIONAL (D1). Notes 9c574360 (M01); M02 verdict
Measured: syncope during exertion with intermittent AV block in M01, M02 and RM03 (HPI scan).
- Not extended to:
  - M03 (only presyncope on stairs);
  - RM02 (sprint drill, but active carditis, an absolute contraindication);
  - S02 (severe AS, harm);
  - the persistent-block cases (RS01: exertional near-syncope only).

Fix in M01, M02 and RM03:
- Delete the exercise waste avoided entry (M01 `avoid-waste-6-exercise-stress-test`, M02
  `avoid-waste-6-exercise-stress-test`, RM03 `avoid-waste-6-exercise-stress-test`).
- Add the criterion `action-exercise-test`:
  - importance recommended;
  - label "Monitored exercise test for exertional syncope (after echocardiography)";
  - alternatives `order_specialized_test {test_type: exercise_stress_test}` and
    `order_echocardiogram {echo_type: exercise_echo}`;
  - citations `[ESC_2018]`, `[Fletcher_2013]`;
  - rationale: "Syncope occurred during exertion: exercise testing is recommended (ESC 2018 Class
    I) and is diagnostic when second- or third-degree AV block develops with exercise, as here.";
  - expected_evidence quoted from the stored exercise report.
- Add the sequence constraint TTE criterion before `action-exercise-test`:
  - `hard`;
  - reason: "Exertional syncope requires severe aortic stenosis and obstructive HCM to be excluded
    on echocardiography before exercise testing (ESC 2018; ESC 2023; ESC/EACTS 2025).";
  - citations `[ESC_2018]`, `[ESC_2023_Cardiomyopathy]`, `[ESC_EACTS_2025_VHD]`.
- Not in the stop rule.
- Place it after monitoring in the criteria list.
- Check that the stored exercise report and the exercise echo report each answer their own order
  (`perfect_agent -v`).

### C2 EXERCISE-SEVERITY (D2, D9). Notes eaa7610b (RS01), 4c6bc3dc (RP05), f8a88107 (M04)
- **RP05** `avoid-waste-6-exercise-stress-test` becomes harm. Keep the id; the severity word in an
  id is cosmetic. Rationale: "Persistent complete AV block with an escape of 38-40 bpm, NSVT and a
  4.8 s pause from cardiac sarcoidosis is an uncontrolled symptomatic arrhythmia, an absolute
  contraindication to exercise testing (Fletcher 2013), and the test adds no decision." Citations
  `[Fletcher_2013]`.
- **RS02** `avoid-waste-5-exercise-stress-test` becomes harm. Same wording, adapted to
  "hypotensive complete heart block with a wide-complex escape".
- **RS01** stays waste. Append to its rationale: "high-degree AV block is a relative
  contraindication (Fletcher 2013)". Add `[Fletcher_2013]` to its citations.
- **M04** `avoid-harm-5-exercise-stress-test`: replace the rationale with "Exercise testing is
  contraindicated while a symptomatic arrhythmia is uncontrolled (Fletcher 2013): recurrent torsades
  de pointes with QTc above 500 ms. It adds nothing to the diagnosis now; after drug washout, the
  recovery QTc of an exercise test can help only if congenital long QT remains in question (ESC
  2022)." Citations `[Fletcher_2013]`, `[ESC_2022_VA_SCD]`.

### C3 AVOIDED-DECOY (D3-D6). Served off-pathway reports without a label
Notes: M03, P01, RS02, S03 and RP04 verdicts; 8baf17ba, 14be9288 (RP03); 0b42012a, 398bb52b,
9007a240, 2e4f14c5 (RP05); 4d6edbb9, 28d00d4d, da138055 (RS01).

Measured (`unlabelled.py`, `fallback_decoys.py`), stored and unlabelled:

| Study | Cases |
|---|---|
| electrophysiology_study | 18 |
| bubble_study | 23 |
| exercise_echo | 22 follow-ups, plus 7 fallbacks |
| coronary_angiography | 8 |
| coronary_CTA | fallback in 7 |
| emg_ncs | 6 follow-ups, plus 3 fallbacks |
| polysomnography | 3 follow-ups, plus 3 fallbacks |
| TEE | fallback in 21 |
| body-imaging decoys | 6 cases |

The rule per study:

| Study (call) | Severity | Where | Canonical rationale core |
|---|---|---|---|
| `order_echocardiogram {echo_type: bubble_study}` | waste | every case that stores a bubble report (23) | "No stroke, TIA, unexplained hypoxaemia or suspected intracardiac shunt: a bubble study plays no part in the evaluation of <diagnosis>." citations [] |
| `order_echocardiogram {echo_type: TEE}` | waste | every case whose fallback is a TEE, except RS06 and RP02 | "No endocarditis, atrial thrombus or valve question that transthoracic imaging leaves open: TEE adds nothing to <diagnosis>." citations [] |
| `order_echocardiogram {echo_type: exercise_echo}` | the exercise test's severity in the case | wherever exercise is waste or harm (list per case) | as the case's exercise entry, naming the echo |
| exercise_echo as an alternative | (criterion) | M01, M02, RM03, P01, RP03 | D4 |
| `order_specialized_test {test_type: electrophysiology_study}` | waste | M01, M02, M03, P01, RM02, RP01, RP04, RP05, RS01, RS02, RS03, RS05, RS06, S01, S02, S03, S04, S06 | "The diagnosis and the device indication are established non-invasively (<ECG/monitoring finding>); an electrophysiology study is indicated only when the non-invasive evaluation is non-diagnostic (ESC 2018)." [ESC_2018], plus [ESC_2022_VA_SCD] in P01 ("risk stratification by PES after an established secondary-prevention ICD indication is only Class IIb") |
| `order_advanced_imaging {modality: coronary_angiography}` and `{modality: coronary_CTA}` | waste | M01, M03, S01, RS02 (both where stored), RP02 (CTA) | "No angina, troponin rise, ischaemic ECG change or ventricular arrhythmia: coronary imaging follows the usual ischaemia indications and does not address <diagnosis> (ESC 2018)." [ESC_2018] |
| the same | harm | S03 (both) | "eGFR about 27 mL/min/1.73 m2: iodinated contrast without an ischaemic indication carries a material risk of contrast-associated kidney injury (ACR-NKF consensus 2020; ACR Manual on Contrast Media)." citations [] |
| `order_specialized_test {test_type: emg_ncs}` | waste | M01, M02, M03, RS03, RS05, S01, S02, S03, S04 | "<known neuropathy or none>; nerve conduction studies do not test autonomic or cardiac function and do not change the management of <diagnosis>." citations [] |
| `order_specialized_test {test_type: polysomnography}` | waste | P01, P02, M01, M03, S03 | "Sleep study does not contribute to the diagnosis or urgent management of <diagnosis>." In M01, add "(obstructive sleep apnoea is already diagnosed)". citations [] |
| `order_body_imaging {study: pelvis_abdomen_CT}`, `{study: pelvis_abdomen_MRI}`, `{study: pelvis_abdomen_ultrasound}` | waste | RS02 | "No abdominal symptom, and surveillance showed no recurrence: abdominal imaging does not bear on <diagnosis>." In the CT/MRI entries add "eGFR about 42: contrast is not a material risk (ACR-NKF 2020), but the study has no indication." |
| `order_body_imaging {study: chest_CT, contrast: true}` and `{study: chest_CTA}` | harm | S03 | S03 contrast text plus "nothing suggests pulmonary embolism, aortic dissection or an intrathoracic mass" |
| the same, and a plain `{study: chest_CT}` | waste | RS03 (eGFR 49) | waste text |
| `order_body_imaging {study: chest_CT}` | waste | RM04 | "CT pulmonary angiography has already imaged the chest." |
| `order_body_imaging {study: mediastinum_MRI}` | waste | RP05 | "Chest CT has characterised the hilar and mediastinal nodes and EBUS-TBNA has given the tissue diagnosis; mediastinal MRI changes nothing." |
| `order_specialized_test {test_type: exercise_stress_test}` | waste | RM01 (and its exercise_echo) | "Central sleep apnoea with sleep-related asystole is not exertional; exercise testing has no role." [Fletcher_2013] |

Checks before saving:
- Read the stored report before writing the rationale, and use the study's real result.
- Check `order_body_imaging` patterns: run `criterion_matches` against `{study, contrast}` calls
  with and without contrast. No call may hit two entries, and no avoided entry may match a
  criterion call.
- Not labelled (D27): P02 exercise_stress_test; RS06 polysomnography and TEE; RP02 TEE, chest CTA
  and both PETs; RS03 coronary angiography and coronary CTA; RM01 speech, language and cognitive
  screens; performance status, gait and audiometry everywhere; M04 chest CT; M05 exercise test and
  exercise echo; S06 exercise test and exercise echo.

### C4 AVB-TERMS (D7). M01, M02, M03 verdicts; class to RM02, RM03
Measured "Mobitz" strings: M01 29, M02 28, M03 14, RM02 16, RM03 33, RP04 1 (correct, "no
Wenckebach or Mobitz II").

The rule (Kusumoto 2019):
- Mobitz II = a single dropped P after two or more conducted beats with a constant PR.
- "2:1 second-degree AV block" for 2:1.
- "High-grade (advanced) AV block" for 3:1 or more.
- Fix every string in the ECG, monitoring, exercise, exercise echo, tilt, fallback cardiac
  monitoring, criteria, musts, avoided rationales, KCE, red herrings, differential and metadata
  pearls.
- Check the numbers against F2.

Per case:
- **M01.**
  - Telemetry, follow-up and fallback (the same recording): "Day 1, 14:32: paroxysmal 2:1 and
    high-grade AV block; longest pause 5.8 s from five consecutive non-conducted P waves at a
    constant sinus rate of about 54 bpm".
  - The other events become "high-grade AV block, pause X s from N non-conducted P waves", with
    N = pause / 1.11 - 1, rounded.
  - "minimum 28 bpm (during 2:1 conduction)". Telemetry is the only source of the minimum, so
    write a sinus rate of 56 for that episode.
  - accepted[0]: "Cardiac syncope due to paroxysmal 2:1 and high-grade AV block (infranodal) on a
    background of trifascicular conduction disease".
  - R0, KCE[2], expected_evidence of the monitoring criterion, avoided rationales and the pearl
    ("Mobitz type II AV block is infranodal..." stays; it is a general statement) follow.
- **M02.**
  - ECG: "Sinus rhythm, atrial rate 78, with second-degree AV block, Mobitz type II (constant PR
    220 ms) with 3:2 conduction and runs of 2:1; ventricular rate about 52."
  - Telemetry and fallback: "Mobitz II (3:2) and 2:1 AV block, with episodes of high-grade AV block
    (3:1, 4:1)". The exercise report's "resting ventricular rate 38 (2:1)" stays: 76-78 / 2.
  - accepted[0]: "Cardiac syncope due to Mobitz II and paroxysmal high-grade AV block with
    bifascicular conduction disease".
  - Answers to test: "Mobitz II AV block" scores; "high-grade AV block with bifascicular block"
    scores.
- **M03.**
  - Telemetry and fallback: "three episodes of 2:1 second-degree AV block".
  - Exercise follow-up and exercise echo: "high-grade AV block with 3:1 conduction in early
    recovery".
  - R0: "Recognise paroxysmal complete, high-grade and 2:1 AV block on a background of
    trifascicular conduction disease as the cause of the syncope".
  - The monitoring expected_evidence: "intermittent 2:1 AV block".
- **RM02.**
  - ECG: keep Mobitz II (it describes single dropped P waves after conducted beats without PR
    prolongation) and add "and runs of 2:1 conduction".
  - Fallback telemetry: "Mobitz II with 2:1 and high-grade (3:1) AV block, and paroxysmal complete
    AV block".
  - Check the rate: atrial 92 with mostly 2:1 gives 46, so the ECG's 48 is acceptable.
- **RM03.** 3:2 is documented, so keep Mobitz II. Only the tilt report ("Mobitz type II block with
  3...") is fixed: if the text is 3:1, write high-grade AV block (3:1).
- CENTRAL C1a: the Mobitz labels.

### C5 DRIVING-SOURCE (D8). Notes c5f02c42 (M01), c90f3000 (P01), b3858fff (P03)
Measured: 28 of 600 cases have a driving must citing ESC 2018, all in SYNC-CARD (`classes_sync.py`).

Canonical texts:
- **Pacemaker (DR-PM):** "Advise no driving until the pacemaker is implanted; Group 1 drivers may
  resume 1 week after implantation and Group 2 drivers once correct device function is confirmed
  (ESC 2018 syncope Practical Instructions, driving table); national licensing rules apply".
  Keep any case-specific tail (e.g. S02/S04's AS clause).
- **Secondary-prevention ICD after sustained VT (DR-ICD2):** "Advise no driving: Group 1 driving
  may resume 3 months after a secondary-prevention ICD (EHRA 2009 consensus on driving with an
  ICD), Group 2 driving is permanently restricted; national licensing rules apply".
- **Other ICD or CRT-D (DR-ICD1):** "Advise no driving until the device is implanted; Group 1
  driving may resume 1 month after ICD implantation (ESC 2018 syncope Practical Instructions;
  longer after an appropriate shock), Group 2 driving is permanently restricted; national licensing
  rules apply".
- **Device choice still open (DR-OPEN, RS01):** "Advise no driving until the device is implanted;
  Group 1 driving may then resume 1 week after a pacemaker or 1 month after an ICD (ESC 2018
  syncope Practical Instructions); national licensing rules apply".
- **Brugada after an ICD for arrhythmic syncope (P03):** "Advise no driving until treated; after
  ICD implantation the Group 1 restriction follows national licensing rules (ESC 2018 syncope
  Practical Instructions: 1 month after an ICD)". This removes the "about 3 months (ESC 2018)"
  attribution.

Apply:

| Text | Cases |
|---|---|
| DR-PM | M01, M02, M03, RM02, RM03, RP04, RS02 |
| DR-ICD2 | P01, RS05 (approved: source error) |
| DR-ICD1 | RP05, S03 |
| DR-OPEN | RS01 |
| P03 text | P03 |

RP01 (approved) "3 months after ICD (ESC 2018)" has the same source error. Its ICD is for
arrhythmic syncope with NSVT, not sustained VT, so DR-ICD1 applies. Fix it as a class defect.

Untouched (NO-ACTION): S01, S02, S04, S06 and RS03 ("1 week (ESC 2018)", approved, correct
package), and the generic "until treated (ESC 2018)" musts (M05, P02, P04, RM04, RP02, RP03, RS04,
RS06, S05).

### C6 TIER-HIGH-RISK (D13, D14). M05 verdict; P03 verdict
- **M05.**
  - `action-7-order-telemetry` becomes required.
  - Add it to `stop_rule.required_before_assessment`.
  - Its label: "Immediate in-hospital ECG monitoring (telemetry): palpitation followed by syncope
    is a high-risk feature".
  - Rationale cites ESC 2018 Table 6 and Class I.
  - R4: see C9.
- **P03.**
  - `action-3-order-echocardiogram` becomes required.
  - Its label: "Transthoracic echocardiogram to exclude structural heart disease (induced type 1
    pattern)".
  - Rationale: "A fever-induced type 1 pattern supports Brugada syndrome only in the absence of
    other heart disease (ESC 2022, IIa C)."
  - Add it to the stop rule.

### C7 DX-CERTAINTY and labels (D7, D12, D16, D17, D19, D23)
accepted[0] changes, each a reviewer ruling. Log them as label changes and list them in CENTRAL C1:

| Case | New accepted[0] |
|---|---|
| M01 | see C4 |
| M02 | see C4 |
| RM01 | "Hypoxic transient loss of consciousness from nocturnal central sleep apnoea with secondary sleep-related asystole, due to anti-Hu paraneoplastic brainstem encephalitis" |
| RM02 | "Cardiac syncope due to intermittent complete heart block from recurrent acute rheumatic fever with active carditis, on chronic rheumatic heart disease" |
| RP02 | "Cardiac syncope due to a right ventricular outflow tract mass most consistent with myxoma (histology pending), causing intermittent dynamic RVOT obstruction" |
| RP05 | "Cardiac syncope due to clinically diagnosed cardiac sarcoidosis (extracardiac histology with compatible cardiac imaging; no myocardial biopsy) with complete AV block and non-sustained VT" |

M05: remove "AVRT" from `rejected` (D12).

### C8 DIFFERENTIAL and reasoning text (D12, D17, D22, D24, D25)
Texts are given per case below.

### C9 MUST-WRONG: canonical musts
- **M04 R2:** "Replete potassium to at least 4.0 mmol/L, aiming for 4.5-5.0 mmol/L while torsades
  is active (Drew 2010; the AHA 2020 statement on drug-induced arrhythmias asks for K above 4.0
  mEq/L), and magnesium to above 2.0 mg/dL; hold hydrochlorothiazide while repleting". Also update
  the expected_evidence or rationale of the labs criterion if it repeats 4.5-5.0 alone.
- **M04 new must (after R5):** "Once the QTc has normalised, treat the depression with an
  antidepressant of lower QT liability (for example sertraline, CredibleMeds), with psychiatric
  follow-up; do not leave it untreated".
- **M05 R4:** "Discharge only after in-hospital ECG monitoring without recurrence, with expedited
  electrophysiology follow-up for ablation now that the tachycardia is documented, the ECG shows no
  pre-excitation and the heart is structurally normal".
- **RP03 R7:** "Offer genetic counselling and testing (RYR2 and the other CPVT genes), with cascade
  genetic testing and clinical evaluation (ECG and exercise testing) of all first-degree relatives:
  her mother, her sister and both children".
- **RP03 R8:** "Treat the iron-deficiency anaemia: review the dose, timing and adherence of oral
  iron, and give intravenous iron if oral iron is ineffective, not tolerated or inappropriate (BSG
  2021); investigate the cause (menstrual losses, coeliac serology, gastrointestinal evaluation as
  indicated)".
- **RP05 R2:** "A permanent device with pacing capability is indicated this admission for complete
  AV block (ESC 2021 Class I); an ICD with pacing capability should be considered rather than a
  pacemaker in cardiac sarcoidosis with NSVT and septal late enhancement (ESC 2021 pacing and ESC
  2022, Class IIa; HRS 2014 IIa)".
- **RP05 R3:** "Start corticosteroids once tissue is obtained and infection is reasonably excluded
  (non-necrotising granulomas, negative AFB and fungal stains and M. tuberculosis PCR, with
  mycobacterial and fungal cultures pending to 6 weeks), for example prednisone 30-40 mg daily then
  a taper, with a steroid-sparing agent such as methotrexate considered; the timing is decided by
  the multidisciplinary cardiac sarcoidosis team, balancing infection risk against active
  myocardial inflammation (HRS 2014)". Prohibition X4 stays.
- **RS01 R3:** "Choose the device individually: an ICD with pacing capability is favoured if a
  pathogenic LMNA variant is confirmed or the estimated ventricular-arrhythmia risk is high (ESC
  2021 pacing IIa; ESC 2022), weighing the probability of an inherited cardiomyopathy (father's
  sudden death at 45, grandmother paced at 60, septal mid-wall fibrosis); do not delay pacing while
  genetic results are awaited". R2 (pacing this admission) stays.
- **RS02 new must:** "Repeat high-sensitivity troponin with CK and keep immune checkpoint inhibitor
  myocarditis under review (pembrolizumab exposure, LVEF 42%), with cardio-oncology input; a single
  normal troponin and no oedema on CMR make it less likely but do not exclude it (ESC 2022
  cardio-oncology)".
- **RM03 R2 append:** "...and with no inducible sustained monomorphic VT at programmed ventricular
  stimulation".

### C10 UNSATISFIABLE: must with no criterion (D5, D18)
- **RM03 R4 (note).** Add `action-coronary-assessment`:
  - importance recommended;
  - label "Coronary assessment (invasive angiography or coronary CTA)";
  - alternatives `order_advanced_imaging {modality: coronary_angiography}` and
    `{modality: coronary_CTA}`;
  - rationale "Q waves V1-V3, a transmural LAD-territory scar and LVEF 36-38%: ischaemic evaluation
    is indicated (ESC 2022)";
  - citations `[ESC_2022_VA_SCD]`;
  - expected_evidence quoted from the stored angiography report.
- **RS05 R6 (approved; real defect).** The same criterion, id `action-coronary-assessment`, for
  "monomorphic VT from the inferior scar with a mildly raised troponin". Both reports are stored
  (F9 CTA, F10 angiography).
- Check in both cases that the CTA and angiography orders are answered by the case's own reports
  (`-v`).

### C11 NO-ACTION
13 approvals, plus the comment-less verdicts of M04, RP03 and RS01 (D26).

## 3. Per-case index (all 30)

Approved cases are marked [APPROVED]: they change only for the listed class defects, which are
additive labels unless stated.

### SYNC-CARD-M01
- c5f02c42:
  - **driving: FIXED**, DR-PM (C5);
  - **pacing citation: DECLINED** (ESC 2021 gives Class I pacing for Mobitz II, high-grade and
    complete AV block; D8).
- 9c574360: **FIXED**, C1. The waste entry is deleted and `action-exercise-test` added, with a
  hard TTE-before constraint.
- NB-87M:SYNC-CARD-M01:policy_verdict:
  - **FIXED**, C4: terminology, pause arithmetic, minimum HR, accepted[0];
  - "infra-Hisian on EPS" **DECLINED** (D7);
  - avoided actions: C1 and C3;
  - assessment: R5 under C5.
- Class C3: waste for EPS, bubble study, coronary angiography, coronary CTA, EMG/NCS,
  polysomnography and TEE. The exercise echo becomes an alternative of `action-exercise-test`.
- CENTRAL C1a.

### SYNC-CARD-M02
- NB-87M:SYNC-CARD-M02:policy_verdict:
  - **FIXED**, C4: ECG becomes 3:2 Mobitz II with 2:1, rate 52; telemetry and fallback
    terminology; accepted[0];
  - **FIXED**, C1: exercise recommended, with exercise echo as an alternative and the waste entry
    deleted.
- Class C3: waste for EPS, bubble study, EMG/NCS and TEE.
- Class C5: DR-PM in R5.

### SYNC-CARD-M03
- NB-87M:SYNC-CARD-M03:policy_verdict:
  - **FIXED**, C4: steps 9, 13 and 18, i.e. telemetry, exercise and exercise echo, plus R0 and
    the monitoring evidence;
  - **FIXED**, C3: coronary angiography waste (not harm: eGFR 65, D5), bubble waste, exercise
    echo waste (as the exercise test), EMG/NCS waste.
- Class C3: EPS, coronary CTA (fallback), polysomnography (fallback) and TEE waste.
- Class C5: DR-PM in R5.
- CENTRAL C1a.

### SYNC-CARD-M04
- f8a88107: **FIXED**, C2, new harm rationale.
- a607c6eb: **FIXED**, C9 R2, divergence recorded.
- 67b578e5: **FIXED**, C9 new antidepressant must.
- NB-87M:SYNC-CARD-M04:policy_verdict: **NO-ACTION** (substance is in the three notes).
- Class C3: the exercise echo (fallback) gets an avoided entry with harm severity, using the C2
  rationale.

### SYNC-CARD-M05
- c0eda0e6: **FIXED**, D12.
  - Remove "AVRT" from `rejected`.
  - Differential AVRT key_features gain: "orthodromic AVRT over a concealed pathway cannot be
    excluded before EP study; management is the same".
  - The EP study stays optional; making it required is DECLINED.
  - Test: "paroxysmal SVT, likely AVNRT" scores; "WPW" is vetoed.
- NB-87M:SYNC-CARD-M05:policy_verdict: **FIXED**, C6 and C9. Telemetry is required and in the stop
  rule; R4 is reworded.

### SYNC-CARD-P01
- c90f3000: **FIXED**, DR-ICD2 in R8.
- NB-87M:SYNC-CARD-P01:policy_verdict:
  - invasive angiography after CTA: **DECLINED** as a label (D5);
  - bubble study and polysomnography: **FIXED** (waste);
  - exercise echo: **FIXED** as an alternative of `action-6-order-specialized-test` (D4);
  - EP study: **FIXED** (waste, ESC 2022 IIb).
- Class C3: TEE waste.

### SYNC-CARD-P02 [APPROVED]
- NB-87M:SYNC-CARD-P02:policy_verdict: **NO-ACTION**.
- Class C3: waste for the bubble study, polysomnography and TEE. The exercise_stress_test is left
  unlabelled (D27).

### SYNC-CARD-P03
- b3858fff: **FIXED**, P03 driving text (C5).
- 1e6f0501: **ALREADY-FIXED** by MRI-CONTRAST, commit 71517e55: the initial MRI is
  `contrast_used: false` with a plain impression; follow-up[7] is the gadolinium study; checked
  with `mri_probe.py`.
- NB-87M:SYNC-CARD-P03:policy_verdict: **FIXED**, C6. TTE is required and in the stop rule.
- Class C3: exercise echo (fallback) waste, as the exercise test.
- CENTRAL C3 (pack Brugada tier).

### SYNC-CARD-P04 [APPROVED]
- NB-87M:SYNC-CARD-P04:policy_verdict: **NO-ACTION**. No class finding.

### SYNC-CARD-RM01
- NB-87M:SYNC-CARD-RM01:policy_verdict:
  - relabel **FIXED**, C7 (D16);
  - moving the case **DECLINED** (October Q1);
  - also replace "syncope" as the name of these events in R-texts, KCE and differential key
    features with "loss of consciousness" or "hypoxic event". The diagnosis label of mimic entries
    such as "Vasovagal / sleep-related reflex syncope" stays.
- Class C3: exercise_stress_test and exercise echo waste.

### SYNC-CARD-RM02
- 95a46437: **FIXED** (D17).
  - Remove CRP from the recurrence reasoning, so that CRP 18.4 mg/L is cited nowhere as supporting recurrence.
    Look in differential, R2 ("raised ESR, CRP and ASO" becomes "raised ESR and ASO, fever and
    polyarthralgia"), KCE[2], and action-2 expected_evidence and rationale. CRP stays in the lab
    order and may be reported as "CRP 18.4 mg/L, below the Jones threshold".
  - Add to `patient.clinical_history.social_history.living_situation`: "Lives in a university
    dormitory in Ghana, where she has lived since birth". Mirror into `patient.hpi` if it carries
    the sentence.
  - The KCE entry states: "Ghana is a high-risk population for rheumatic fever (Jones 2015): fever
    38.2 C and ESR 48 are minor criteria and polyarthralgia a major one; CRP 1.84 mg/dL is below
    the 3.0 mg/dL threshold; with active carditis and ASO 340 the recurrence criteria are met".
- NB-87M:SYNC-CARD-RM02:policy_verdict: **FIXED** (C7).
  - New accepted[0].
  - Delete differential[0] (ARF) and move its supporting facts into KCE.
  - Keep `icd_codes[0]` I44.2.
  - CENTRAL C1b.
- Class C4: Mobitz wording in the fallback telemetry.
- Class C3: waste for EPS, bubble study, exercise echo and TEE.
- Class C5: DR-PM in R7. R7 currently also names ESC 2018 Group 1; keep its sport clause.

### SYNC-CARD-RM03
- NB-87M:SYNC-CARD-RM03:policy_verdict: **FIXED** (D18).
  - C10: `action-coronary-assessment`.
  - D6: the EPS report gains a PES finding, "Programmed ventricular stimulation from the RV apex
    and outflow tract (two drive cycle lengths, up to three extrastimuli): no sustained
    monomorphic VT induced", with a matching quantitative entry. The impression adds "No inducible
    sustained monomorphic VT". The EPS criterion `action-electrophysiology-study` is recommended,
    with the label "Electrophysiology study with programmed ventricular stimulation (post-infarct
    scar, LVEF 36-38%)", citations `[ESC_2022_VA_SCD]`, `[ESC_2018]`.
  - R2 append (C9).
  - The differential "Sustained VT from ischaemic scar" cites "not inducible at programmed
    ventricular stimulation".
  - Assessment needs_revision is covered by R2 and R4.
- Class C1: exercise recommended, with exercise echo as an alternative.
- Class C3: bubble study and TEE waste.
- Class C4: tilt text.
- Class C5: DR-PM in R7.

### SYNC-CARD-RM04 [APPROVED]
- NB-87M:SYNC-CARD-RM04:policy_verdict: **NO-ACTION**.
- Class C3:
  - bubble study waste;
  - exercise echo harm (as the exercise test: acute PE with RV dysfunction, Fletcher 2013);
  - chest_CT (F9, non-contrast after CTPA) waste;
  - TEE waste.

### SYNC-CARD-RP01 [APPROVED]
- NB-87M:SYNC-CARD-RP01:policy_verdict: **NO-ACTION**.
- Class C3: waste for the bubble study, EPS (fallback) and TEE.
- Class C5: R8 to DR-ICD1, a source error.

### SYNC-CARD-RP02
- NB-87M:SYNC-CARD-RP02:policy_verdict:
  - diagnosis: **FIXED**, C7;
  - exercise: **ALREADY-FIXED** (harm, avoid-harm-6);
  - tilt: harm **kept**, change to waste **DECLINED** (D19: the rationale already justifies the
    preload risk);
  - assessment: R0 already says "most likely a myxoma", so no change.
- Class C3: bubble study waste, exercise echo harm, coronary CTA (fallback) waste.

### SYNC-CARD-RP03
- d08aab43: **CENTRAL** (display, C1d). The data are consistent (RYR2 pathogenic; KCNJ2 negative).
  The worker fills the four empty per-gene `interpretation` strings with "Negative".
- 8baf17ba: **FIXED** (D4): exercise echo becomes an alternative of
  `action-5-order-specialized-test`. A second exercise study is then unjustified.
- 14be9288: **FIXED**, bubble study waste.
- c42c1ec4: **FIXED**, C9 R7.
- 99f45b73: **FIXED**, C9 R8.
- NB-87M:SYNC-CARD-RP03:policy_verdict: **NO-ACTION**.
- Class C3: TEE waste.

### SYNC-CARD-RP04
- 014edfe5: **FIXED** (D22). Canonical sentence: "Normal routine and ambulatory EEGs do not
  exclude epilepsy; the decisive evidence is the loop recorder, which recorded complete AV block
  with asystole during three typical witnessed episodes."
  - R0: delete "normal EEGs and therapeutic drug levels never confirmed epilepsy" and use the
    sentence.
  - KCE[0], differential[0] key_features and red_herrings[0] correct_interpretation: use it, and
    drop drug failure as evidence.
  - Action-2 (AED levels) rationale: delete "Breakthrough events on therapeutic levels argue
    against undertreated epilepsy"; say the levels document exposure before withdrawal.
- NB-87M:SYNC-CARD-RP04:policy_verdict: **FIXED**, C3 EPS waste (D6).
- Class C3: exercise echo (fallback) waste.
- Class C5: DR-PM in R5.

### SYNC-CARD-RP05
- 5b75258e: **FIXED**, C7 accepted[0].
- 239d4a90: **FIXED**, C9 R3.
- 4c6bc3dc:
  - **FIXED**, exercise becomes harm (C2);
  - removal **DECLINED** (D3).
- 0b42012a: **FIXED**, bubble study waste.
- 398bb52b: **FIXED**, exercise echo harm.
- 9007a240: **FIXED**, mediastinum MRI waste.
- 2e4f14c5:
  - **FIXED**, the post-diagnostic reports are labelled;
  - the stop-rule change is **DECLINED** (D3: served reports are not a sequence; max 3 stays).
- NB-87M:SYNC-CARD-RP05:policy_verdict:
  - **FIXED**, C9 R2: "do not defer" removed;
  - R7 to DR-ICD1.
- Class C3: EPS and TEE waste.

### SYNC-CARD-RS01
- 0af538d2: **FIXED**, C9 R3.
- 6e00f5d4: **FIXED** (D24).
  - Differential[0] key_features: replace "an autosomal dominant pattern" with "a family history
    suggesting, but not establishing, an inherited conduction disease".
  - KCE[2]: "...a paternal grandmother paced at 60: suspected inherited conduction disease
    requiring genetic evaluation".
  - Every "likely familial" or "likely inherited" in the avoided rationales becomes "suspected
    inherited".
- 4d6edbb9: **ALREADY-FIXED**. Tilt is waste (avoid-waste-5); removal **DECLINED** (D3).
- eaa7610b: **ALREADY-FIXED**. Exercise is waste; Fletcher is added to its rationale (C2); removal
  **DECLINED**.
- 28d00d4d: **FIXED**, bubble study and exercise echo waste.
- da138055: **ALREADY-FIXED**. EEG is waste (avoid-waste-4); removal **DECLINED**.
- NB-87M:SYNC-CARD-RS01:policy_verdict: **NO-ACTION**.
- Class C3: EPS and TEE waste.
- Class C5: DR-OPEN in R7.

### SYNC-CARD-RS02
- 02b0bfb9: **FIXED** (D25).
  - red_herrings[1] correct_interpretation: "...a normal troponin and no oedema on CMR make immune
    checkpoint inhibitor myocarditis less likely but do not exclude it; the working judgement
    favours degenerative conduction disease".
  - Differential[0] key_features: the same idea.
  - New must (C9).
- NB-87M:SYNC-CARD-RS02:policy_verdict:
  - **FIXED**, coronary angiography and coronary CTA (fallback) waste, abdomen CT, MRI and US
    waste;
  - harm for the contrast studies **DECLINED** (eGFR 42; ACR-NKF 2020; D5).
- Class C2: exercise becomes harm, with the exercise echo harm too.
- Class C3: waste for EPS, bubble study and TEE.
- Class C5: DR-PM in R7.

### SYNC-CARD-RS03 [APPROVED]
- NB-87M:SYNC-CARD-RS03:policy_verdict: **NO-ACTION**.
- Class C3: waste for EPS, bubble study, exercise echo, chest_CT, chest_CTA, EMG/NCS (fallback)
  and TEE. Coronary studies are left unlabelled (R5 makes them conditional).

### SYNC-CARD-RS04 [APPROVED]
- NB-87M:SYNC-CARD-RS04:policy_verdict: **NO-ACTION**. No class finding.

### SYNC-CARD-RS05 [APPROVED]
- NB-87M:SYNC-CARD-RS05:policy_verdict: **NO-ACTION**.
- Class C10: `action-coronary-assessment`, recommended. This is a real defect: must R6 has no
  criterion.
- Class C3: waste for EPS, bubble study, exercise echo, EMG/NCS and TEE.
- Class C5: R7 to DR-ICD2 (source error).

### SYNC-CARD-RS06 [APPROVED]
- NB-87M:SYNC-CARD-RS06:policy_verdict: **NO-ACTION**.
- Class C3: waste for EPS, bubble study and exercise echo (as the exercise test). TEE and PSG stay
  unlabelled.

### SYNC-CARD-S01 [APPROVED]
- NB-87M:SYNC-CARD-S01:policy_verdict: **NO-ACTION**.
- Class C3: waste for EPS, bubble study, exercise echo, coronary angiography, coronary CTA
  (fallback), EMG/NCS (fallback) and TEE.

### SYNC-CARD-S02 [APPROVED]
- NB-87M:SYNC-CARD-S02:policy_verdict: **NO-ACTION**.
- Class C3:
  - EPS waste;
  - bubble study waste;
  - exercise echo harm (symptomatic severe AS, ESC/EACTS 2025);
  - EMG/NCS (fallback) waste;
  - TEE waste.

### SYNC-CARD-S03
- NB-87M:SYNC-CARD-S03:policy_verdict: **FIXED**, harm for coronary angiography, coronary CTA
  (fallback), contrast chest CT and chest CTA (eGFR 27).
- Class C3: waste for EPS, bubble study, exercise echo, EMG/NCS, polysomnography (fallback) and
  TEE.
- Class C5: DR-ICD1 in R6 (CRT-D).

### SYNC-CARD-S04 [APPROVED]
- NB-87M:SYNC-CARD-S04:policy_verdict: **NO-ACTION**.
- Class C3: EPS waste, bubble study waste, exercise echo harm (AS), EMG/NCS waste, TEE waste.

### SYNC-CARD-S05 [APPROVED]
- NB-87M:SYNC-CARD-S05:policy_verdict: **NO-ACTION**.
- Class C3: bubble study waste, exercise echo harm (AS), TEE waste.

### SYNC-CARD-S06 [APPROVED]
- NB-87M:SYNC-CARD-S06:policy_verdict: **NO-ACTION**.
- Class C3: waste for EPS, bubble study and TEE. Exercise test and exercise echo stay unlabelled.

## 4. CENTRAL requests

- **C1 Synonyms** (`diagnosis_synonyms.yaml`, then `apply_diagnosis_synonyms.py --prune
  --conditions syncope_cardiac` and `--check`):
  - a) **I44.1.** Scope "mobitz ii", "mobitz type ii" and "mobitz 2" to SYNC-CARD-M02 and RM03.
    M01 and M03 keep the high-grade labels. Add these labels to `RETIRED` handling for M01/M03,
    or move them into a scoped `I44.1+mobitz` entry (D7).
  - b) **I44.2+rheumatic (RM02).** Add "acute rheumatic fever", "recurrent acute rheumatic fever",
    "recurrent rheumatic fever", "acute rheumatic fever with carditis" and "acute rheumatic
    carditis" (D17). Check them against RM02's mimics: chloroquine, laminopathy, malaria.
  - c) **Label changes to record** (accepted[0] edited in the case files): M01, M02, RM01, RM02,
    RP02, RP05. No synonym edit is needed for RM01, RP02 or RP05.
  - d) **Review UI** (`web-review/.../CaseDetail.tsx`): print a row's label keys (`test`) before
    `interpretation`, `result` and `abnormal`. RP03 d08aab43 was a misread (D20).
- **C2 Citation keys** (pack allow-list, `dataset-generation/criteria_packs/SYNC-CARD.md` sec.10):
  - `[ESC_2018_PI]`: Brignole 2018 Practical Instructions, Eur Heart J 2018;39:e43-e80.
  - `[EHRA_2009_ICD_Driving]`: Vijgen 2009, Europace 2009;11:1097-1107.
  - `[ACR_NKF_2020]`: Davenport 2020, Radiology 2020;294:660-668.
  - `[AHA_2020_DrugArrhythmia]`: Tisdale 2020.
  - `[ESC_2022_CardioOnc]`: Lyon 2022.
  - `[BSG_2021_IDA]`: Snook 2021.
  - Workers name these sources in text until the keys exist.
- **C3 Pack text** (sec.3, 5 and 7):
  - Exercise testing in exertional syncope with intermittent AV block becomes recommended (D1).
  - Exercise testing is harm in uncontrolled symptomatic bradyarrhythmia (D2).
  - Brugada: TTE becomes required when the type 1 pattern is induced (D14).
  - Driving text (D8): replace "[ESC_2018] ... 3 months after an ICD for secondary prevention" with
    the C5 sources.
  - Torsades potassium: record the divergence with Tisdale 2020 (D10).
  - Add the C3 decoy table.
  - `condition_tool_guidance.yaml` claims for syncope (exercise and echo counts) will change:
    `test_guidance_claims` is maintained centrally.
- **C4 Library.** No change is needed. The stored decoy reports stay (D3).

## 5. Open questions

- None needs information only Andrea has.
- **Applying C3 to the 13 approved cases.** Decided yes (additive avoided labels only; D3), but
  each approved case then goes back to re-review. If Andrea prefers to keep approved cases frozen,
  revert C3 in P02, RM04, RP01, RS03, RS05, RS06, S01, S02, S04, S05 and S06. RS05's coronary
  criterion and driving source, and RP01's driving source, fix factual defects and should stay.
- **Orthostatic BP.** 14 cases store an active-stand report with no criterion; 16 have it as
  recommended. ESC 2018 makes it Class I in the initial evaluation. Not changed this round (no
  note, unscored, unpenalised), and offered for the next round.

<!-- PLAN COMPLETE -->
