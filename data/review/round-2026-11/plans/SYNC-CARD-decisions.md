# SYNC-CARD: November 2026 decisions

Lead decisions for the 60 November notes (all R2, NB-87MF-FBTV-TPWE) on the 30 SYNC-CARD cases,
written 17 Nov 2026. Each entry gives the note ids, the decision, the reason and the citation.
`plans/SYNC-CARD.md` has the per-case index and the canonical texts. October decisions are in
`data/review/round-2026-10/plans/SYNC-CARD-decisions.md` and the October pack
`dataset-generation/criteria_packs/SYNC-CARD.md`. Where a decision departs from them, the entry says so.

Sources verified for this round (web, 17 Nov 2026):
- Kusumoto FM et al. 2018 ACC/AHA/HRS bradycardia guideline, Circulation 2019;140:e382-e482
  (key `[ACC_AHA_HRS_2018_Bradycardia]`). Its definition table gives these terms:
  - Mobitz II: a single non-conducted P wave with a constant PR before and after it, excluding 2:1.
  - 2:1 AV block: a category of its own.
  - Advanced or high-grade AV block: 2 or more consecutive non-conducted P waves at a constant
    rate, with some conduction preserved.
- Brignole M et al. Practical Instructions for the 2018 ESC Guidelines for the diagnosis and
  management of syncope, Eur Heart J 2018;39:e43-e80 (doi:10.1093/eurheartj/ehy071). Its Web
  Table 3, "Advice for driving in patients with syncope", gives:
  - pacemaker implant: Group 1 after 1 week, Group 2 once correct device function is established;
  - ICD implant: Group 1 after 1 month (risk higher in the months after a shock), Group 2
    permanent restriction.
- Vijgen J et al. EHRA consensus: updated recommendations for driving by patients with ICDs,
  Europace 2009;11:1097-1107. Private driving is restricted for 4 weeks after a
  primary-prevention ICD and 3 months after a secondary-prevention ICD.
- Fletcher GF et al. AHA exercise standards, Circulation 2013;128:873-934 (`[Fletcher_2013]`).
  - High-degree AV block is a relative contraindication to exercise testing.
  - Uncontrolled arrhythmia causing symptoms or haemodynamic compromise, symptomatic severe AS,
    acute myocarditis and acute PE are absolute contraindications.
  - The ACC/AHA 2002 exercise-testing update has the same table.
- ACR-NKF consensus on IV iodinated contrast in kidney disease: Davenport MS et al., Radiology
  2020;294:660-668. The ACR Manual on Contrast Media carries the same rule.
  - Prophylaxis is indicated, and the risk is material, at an eGFR below 30 mL/min/1.73 m2 or in
    AKI.
  - It is not indicated at a stable eGFR of 30 or above. Contrast-induced AKI is near 0% at an
    eGFR of 45 or above, and 0-2% at 30-44.
- Recalled and not re-read this round, cited only for the statements named:
  - Brignole 2018 ESC syncope main text (`[ESC_2018]`):
    - exercise testing is recommended in syncope during or shortly after exertion (Class I C);
    - it is diagnostic when second- or third-degree AV block develops during exercise (I C);
    - Table 6 lists high-risk features;
    - immediate in-hospital monitoring is indicated in high-risk patients (I C).
  - Zeppenfeld 2022 ESC VA/SCD (`[ESC_2022_VA_SCD]`). These statements are quoted by R2 in its
    notes and agree with the guideline:
    - Brugada syndrome with an induced type 1 pattern requires "no other heart disease" (IIa C);
    - PES is indicated in post-infarct syncope that is unexplained after non-invasive work-up;
    - in sarcoidosis with a pacing indication, an ICD should be considered (IIa).
  - Glikson 2021 ESC pacing (`[ESC_2021_Pacing]`): pacing is Class I for complete AV block. Its
    sarcoid statements are quoted by R2.
  - Tisdale JE et al. AHA scientific statement on drug-induced arrhythmias, Circulation
    2020;142:e214-e233: K above 4.0 mEq/L and Mg above 2.0 mg/dL on QT-prolonging drugs.
  - Gewitz 2015 Jones revision (`[Gewitz_2015]`). In moderate- or high-risk populations,
    polyarthralgia is a major criterion. The minor criteria there are fever of 38.0 C or more,
    ESR of 30 mm/h or more and CRP of 3.0 mg/dL or more.
  - Lyon AR et al. 2022 ESC cardio-oncology guideline, Eur Heart J 2022;43:4229-4361: immune
    checkpoint inhibitor (ICI) myocarditis is diagnosed with troponin, ECG and CMR; a single
    normal troponin does not exclude it.
  - Snook J et al. BSG guidelines for iron deficiency anaemia in adults, Gut 2021;70:2030-2051:
    oral iron first, IV iron when oral iron is ineffective, not tolerated or inappropriate,
    and investigation of the cause.

## D1. Exercise testing in exertional syncope with intermittent AV block (M01, M02; class to RM03)
Notes: 9c574360 (M01), NB-87M:SYNC-CARD-M02:policy_verdict (exercise part).

**Decision: FIXED, overriding the October pack rule** (pack sec.3: exercise is waste in CHB or
Mobitz II with an established pacing indication).
- In M01, M02 and RM03 a syncope occurred while climbing stairs and the block is intermittent.
- Exercise testing is Class I C in syncope during exertion. It is also diagnostic when second- or
  third-degree AV block appears with exercise (Class I C). The stored reports show exactly that.
- The October rule rested on "no decision changes". The guideline does not make that exception,
  and the physician ruling wins (addendum).

Changes:
- Remove the exercise waste label.
- Add the criterion `action-exercise-test`, recommended. Alternatives:
  - `order_specialized_test {test_type: exercise_stress_test}`;
  - `order_echocardiogram {echo_type: exercise_echo}`.
- Add a hard sequence constraint TTE before the exercise test (pack sec.6, existing canonical
  reason).
- Do not add it to the stop rule.

Not extended to:
- persistent CHB (nothing to unmask: D2);
- severe AS (harm);
- RM02 (active carditis, an absolute contraindication: Fletcher 2013);
- M03, where only presyncope was exertional. ESC 2018 says "syncope".

## D2. Exercise testing in persistent AV block (RS01, RP05; class)
Notes: eaa7610b (RS01), 4c6bc3dc (RP05).

**Decision: FIXED by severity.** "Remove the test and its results" is DECLINED; see D3.
- RS01 keeps waste. Fletcher 2013 makes high-degree block only a relative contraindication, and a
  persistent block has nothing to unmask.
- RP05 and RS02 become harm:
  - RP05 has an escape of 38-40 bpm, NSVT and a 4.8 s pause;
  - RS02 has hypotensive bradycardia;
  - both are uncontrolled arrhythmias causing symptoms or haemodynamic compromise, an absolute
    contraindication (Fletcher 2013).
- Every other persistent-block case keeps waste.
- The exercise-echo label in each case copies the exercise-test label (D4).

## D3. Served off-pathway reports are labelled, never removed (class AVOIDED-DECOY)
Notes:
- NB-87M:SYNC-CARD-M03:policy_verdict, NB-87M:SYNC-CARD-P01:policy_verdict;
- 8baf17ba, 14be9288 (RP03);
- 4c6bc3dc, 0b42012a, 398bb52b, 9007a240, 2e4f14c5 (RP05);
- 4d6edbb9, eaa7610b, 28d00d4d, da138055 (RS01);
- NB-87M:SYNC-CARD-RS02:policy_verdict, NB-87M:SYNC-CARD-S03:policy_verdict,
  NB-87M:SYNC-CARD-RP04:policy_verdict.

**Decision: a stored report is the answer the case gives if an agent orders that test. It is not a
step the clinician took.**
- The reports were stored on 25 Oct 2026 (commit 4221abb6) because the library normal contradicted
  the case, for example a normal exercise echo in complete heart block.
- `config/tools/library_contradictions.yaml` and `test_library_never_answers_a_contradicted_order`
  forbid letting the library answer them again.

So:
- "Remove from the pathway" is DECLINED as worded. Removing the report would make the agent see a
  normal result that contradicts the patient.
- The physician's point, that the test is useless or unsafe for this patient, is applied: every
  such order gets an `avoided_actions` entry. The study table is in the plan (C3).
- Off-pathway follow-ups go last in `followup_outputs`.
- The stop-rule note 2e4f14c5 misreads the served reports as an executed sequence.
  `max_additional_actions` limits the agent's own extra calls, so the stop rule stays. The extra
  tests it names are labelled.

Extended, with no note, to every case that stores such a report. This includes the approved cases,
because a served test that is useless and unlabelled is a scoring defect R2 flagged in 12 cases.
- The change there is additive only: new avoided entries, no clinical text.
- TEE is included as an own extension: no case has an indication for it except RS06 and RP02.

## D4. Exercise echo follows the exercise test of the same case
Notes: M03 verdict, P01 verdict, 8baf17ba (RP03), 398bb52b (RP05), 28d00d4d (RS01).

**Decision.**
- Where the exercise test is a criterion, the exercise echo is added as a second alternative of
  that criterion: M01, M02, RM03 (D1), P01 and RP03. RP01 (approved, exercise optional) is
  not changed: its exercise echo is not useless and the case has no defect to fix.
- Otherwise the exercise echo gets an avoided entry with the same severity as the exercise test.
- Reason: an exercise echo is an ECG-monitored exercise test with imaging. For CPVT, ARVC and
  exertional AV block it answers the same question.
- R2's concern is redundancy: an exercise echo after a full exercise test adds nothing. The scorer
  already handles that, because the second test claims no criterion. It lowers tool accuracy and
  counts as an extra action in the stop rule.
- Waste-labelling an equivalent first choice would penalise a correct work-up.
- RP03 8baf17ba and P01 (exercise echo part) are therefore FIXED by this rule rather than with a
  waste label.
- P02 is unchanged: there the exercise echo is the criterion.

## D5. Invasive coronary angiography and coronary CTA
Notes: M03 verdict, P01 verdict, RS02 verdict, S03 verdict, NB-87M:SYNC-CARD-RM03:policy_verdict
(coronary part).

**Decision.**
- Coronary studies follow the same indications as without syncope: suspected ischaemia or
  infarction (ESC 2018 sec.4; `condition_tool_guidance.yaml` syncope_cardiac advanced imaging).
- A criterion where ischaemia is a real question:
  - P01 (VT, both alternatives, existing);
  - RM03 (new, recommended);
  - RS05 (new, recommended). RS05's must R6 asks for coronary angiography and no criterion orders
    it; this is the class UNSATISFIABLE, a real defect in an approved case.
- Waste where nothing points to ischaemia: M01, M03, S01, RS02 and RP02 (fallback CTA).
  - M03 is waste, not harm. Metformin with an eGFR of about 65 is not a contrast risk (ACR-NKF
    2020: prophylaxis only below 30).
- Harm in S03. Its eGFR is 27 by CKD-EPI 2021, and iodinated contrast with no indication is a
  material risk (ACR-NKF 2020). This accepts R2.
- RS02 (eGFR about 42): R2's "harmful given CKD" is DECLINED for the contrast studies, which stay
  waste. At an eGFR of 30 or above, prophylaxis is not indicated and contrast-induced AKI is 0-2%
  (ACR-NKF 2020). R2's "useless" is applied.
- P01, invasive angiography "useless when ordered after CTA": DECLINED as a label. An avoided
  action matches a call unconditionally, so it would penalise invasive angiography as the first and
  only coronary test, which the criterion accepts. It would also put a criterion and an avoided
  action on the same call (addendum rule). The scorer already treats the second coronary study as
  unjustified (claimed criterion).
- RS03 coronary angiography stays unlabelled. Its must R5 makes graft angiography conditional on a
  rising troponin, so the study is not useless.

## D6. Electrophysiology study
Notes: P01 verdict (EPS part), RM03 verdict (PES), RP04 verdict.

**Decision.**
- Waste wherever the diagnosis and the device or therapy indication are already established
  non-invasively. EPS in syncope is Class IIa only when the non-invasive evaluation is
  non-diagnostic (ESC 2018). For an established secondary-prevention ICD in P01, PES is only IIb
  (ESC 2022, quoted by R2). Cases: M01, M02, M03, P01, RM02, RP01, RP04, RP05, RS01, RS02, RS03,
  RS05, RS06, S01-S04 and S06.
- In RP04 it is the only unlabelled served report, which explains the comment-less avoided-actions
  verdict.
- M05 (optional) and RS04 (recommended) keep it.
- RM03: R2 offers two options. Option (a) is chosen as clinically better.
  - Programmed ventricular stimulation is added to the stored EPS report: non-inducible for
    sustained monomorphic VT.
  - A recommended criterion `action-electrophysiology-study` is added.
  - Reason: post-infarct scar with an LVEF of 36-38% and syncope not captured on monitoring. PES
    is recommended when post-infarct syncope stays unexplained, and the CRT-P versus CRT-D choice
    turns on inducibility (ESC 2022). Arguing exclusion in text alone (option b) would leave the
    CRT-P must without evidence.

## D7. AV block nomenclature and conduction arithmetic (class AVB-TERMS)
Notes: NB-87M:SYNC-CARD-M01:policy_verdict, NB-87M:SYNC-CARD-M02:policy_verdict,
NB-87M:SYNC-CARD-M03:policy_verdict.

**Decision: FIXED, with Kusumoto 2018 definitions as the rule.** The rule is extended, with no
note, to RM02 and RM03 (not approved).
- "Mobitz II" is used only for a single non-conducted P wave after two or more conducted beats with
  a constant PR (3:2, 4:3...).
- 2:1 is "2:1 second-degree AV block".
- Two or more consecutive non-conducted P waves (3:1 and higher) are "high-grade (advanced) AV
  block".
- Arithmetic:
  - ventricular rate = atrial rate divided by the conduction ratio;
  - a pause made of n consecutive non-conducted P waves lasts (n+1) P-P intervals.

Per case:
- **M01.**
  - Telemetry: the 5.8 s pause at a sinus rate of about 54 bpm (P-P 1.11 s) is five consecutive
    non-conducted P waves. Write it as high-grade AV block with five non-conducted P waves.
  - The minimum HR of 28 bpm is 2:1 conduction at a sinus rate of 56. Write "minimum 28 bpm during
    2:1 conduction".
  - accepted[0] becomes "Cardiac syncope due to paroxysmal 2:1 and high-grade AV block (infranodal)
    on a background of trifascicular conduction disease".
  - The "infra-Hisian on EPS" clause of R2's text is DECLINED. The EPS is waste here (D6), so the
    label must not depend on it.
- **M02.**
  - An ECG rate of 52 bpm at an atrial rate of 78 is impossible with 2:1 or 3:1 conduction. It
    equals 3:2 conduction exactly (78 x 2/3 = 52).
  - The ECG becomes Mobitz II with 3:2 conduction (constant PR 220 ms) and intermittent 2:1. This
    keeps Mobitz II where it is true, as R2's own exception allows.
  - Telemetry: Mobitz II (3:2), 2:1 and high-grade AV block (3:1, 4:1).
  - accepted[0] becomes "Cardiac syncope due to Mobitz II and paroxysmal high-grade AV block with
    bifascicular conduction disease".
- **M03.**
  - Telemetry "Mobitz II with 2:1" becomes 2:1 AV block.
  - The exercise and exercise-echo "Mobitz II 3:1" becomes high-grade AV block (3:1).
  - R0 is reworded.
  - accepted[0] already reads "high-grade".
- **RM02.** Telemetry "Mobitz II 2:1 and 3:1" becomes Mobitz II with 2:1 and high-grade (3:1)
  AV block. Keep Mobitz II only if the ECG shows constant-PR conducted runs; the ECG text says it
  does.
- **RM03.** 3:2 is documented, so Mobitz II stays. Fix only phrases that call 2:1 or 3:1 Mobitz II.
- CENTRAL (synonyms): scope the I44.1 Mobitz labels ("mobitz ii", "mobitz type ii", "mobitz 2") to
  M02 and RM03 only. M01 and M03 keep the high-grade labels.

## D8. Driving advice (class DRIVING-SOURCE)
Notes: c5f02c42 (M01), c90f3000 (P01), b3858fff (P03).

**Decision: FIXED by re-attribution and interval.**
- The pacemaker rule (Group 1 after 1 week) is real. It sits in the ESC 2018 Practical Instructions
  (Web Table 3), not the main text, which is R2's point. Re-attribute it.
- The "3 months after a secondary-prevention ICD (ESC 2018)" is wrong in its source. ESC 2018 gives
  1 month after any ICD implant; the 3-month figure is EHRA 2009, for secondary prevention.
- Canonical texts are in the plan (C5).
- The M01 pacing half of c5f02c42 is DECLINED. ESC 2021 pacing (Glikson) gives Class I pacing for
  Mobitz II, high-grade and complete AV block without a reversible cause, and R2 cites it as such in
  RP05.

Applied to:
- M01, P01, P03 (notes);
- the other non-approved cases whose driving must names an interval (M02, M03, RM02, RM03, RP04,
  RP05, RS01, RS02, S03);
- RS05, approved, because its source is factually wrong. Its interval is right; only the
  attribution changes.

Approved cases with "1 week (ESC 2018)" (S01, S02, S04, S06, RS03) are NO-ACTION. The attribution
is to the ESC 2018 guideline package, which is not an error. Generic "until treated (ESC 2018)"
musts are untouched.

## D9. M04 exercise harm rationale
Note: f8a88107.

**Decision: FIXED.** The label stays harm. The reason becomes uncontrolled symptomatic arrhythmia
with recurrent torsades and QTc above 500 ms, an absolute contraindication (Fletcher 2013), and no
diagnostic gain now.
- The adrenergic-provocation reason goes. It contradicts the isoproterenol must: in acquired long
  QT a faster heart rate suppresses pause-dependent torsades (ESC 2022; Tisdale 2020).
- Add that after drug washout, the recovery QTc of an exercise test can help if congenital LQTS
  remains in question (ESC 2022). This matches must R7.

## D10. M04 potassium and magnesium targets
Note: a607c6eb.

**Decision: FIXED by recording the divergence.**
- Drew 2010 (4.5-5.0 mmol/L in torsades) is an allowed and correct source. Tisdale 2020 asks for
  K above 4.0 mEq/L and Mg above 2.0 mg/dL in patients on QT-prolonging drugs.
- R2 offers either option. Keeping both is clinically better: this patient has active torsades, the
  setting Drew addresses.
- The text is in the plan (C9).

## D11. M04 depression plan
Note: 67b578e5.

**Decision: FIXED.**
- Add a must: once the QTc has normalised, restart antidepressant treatment with a drug of lower QT
  liability (for example sertraline, CredibleMeds), with psychiatric follow-up.
- The stored citalopram drug check already names sertraline.

## D12. M05 AVRT and the EP study
Note: c0eda0e6.

**Decision: remove "AVRT" from `diagnosis.rejected`** (option 1 of the note). "wolff parkinson
white" and "WPW" stay rejected, because the ECG and the monitoring show no pre-excitation.
- Making the EPS required (option 2) is DECLINED. It would require an invasive study before an
  assessment whose management is the same either way: vagal manoeuvres, adenosine and referral for
  EP study with ablation (ESC 2019 SVT). R2 itself offers the first option.
- The "SVT" and "paroxysmal supraventricular tachycardia" labels already credit the mechanism.
- Differential AVRT key_features gain: "orthodromic AVRT over a concealed pathway cannot be excluded
  before EP study; management is the same."
- Test with `DiagnosisCriterion.matches` that "paroxysmal SVT, likely AVNRT, AVRT not excluded"
  scores, and that "WPW" is still vetoed.

## D13. M05 high-risk monitoring and disposition
Note: NB-87M:SYNC-CARD-M05:policy_verdict.

**Decision: FIXED.** This reverses the October tier (October "confirmed M05 telemetry as
high-risk" but left it recommended, which is internally inconsistent).
- Sudden palpitation immediately followed by syncope is a major high-risk feature (ESC 2018
  Table 6). Immediate in-hospital monitoring is Class I.
- `action-7-order-telemetry` becomes required and enters the stop rule. The event monitor stays
  required.
- R4 changes to the canonical text in C9.

## D14. P03 echocardiogram required
Note: NB-87M:SYNC-CARD-P03:policy_verdict.

**Decision: FIXED, overriding the pack tier table** (Brugada: TTE recommended).
- The type 1 pattern here is fever-induced, and an induced pattern needs "no other heart disease"
  before Brugada syndrome is diagnosed (ESC 2022, IIa C).
- Changes:
  - `action-3-order-echocardiogram` becomes required;
  - it is added to `stop_rule.required_before_assessment`;
  - its label becomes "Transthoracic echocardiogram to exclude structural heart disease".
- CENTRAL: update pack sec.2 and sec.7, Brugada row.

## D15. P03 brain MRI header
Note: 1e6f0501.

**Decision: ALREADY-FIXED** by class MRI-CONTRAST (commit 71517e55).
- The initial MRI is `contrast_used: false` with a plain impression.
- `followup_outputs` holds the gadolinium study (`contrast_used: true`, request_contrast_mri).
- `mri_probe.py` was run and shows each order receiving its own study.

## D16. RM01 is not syncope
Note: NB-87M:SYNC-CARD-RM01:policy_verdict.

**Decision: relabel accepted[0] and keep the case in SYNC-CARD.**
- New accepted[0]: "Hypoxic transient loss of consciousness from nocturnal central sleep apnoea
  with secondary sleep-related asystole, due to anti-Hu paraneoplastic brainstem encephalitis".
- Reason: the ESC 2018 definition and Table 2 exclude hypoxia and cardiac arrest without
  spontaneous recovery from syncope, and R2 is right.
- Moving the case is DECLINED. October Q1 stands: no paraneoplastic condition exists, and the case
  is the condition's neurological mimic.
- Its labels already require the anti-Hu cause, and G13.1 and the synonyms are unchanged. CENTRAL
  records the label change (no yaml edit).
- In ground-truth text, wherever "syncope" names these events, write "loss of consciousness" or
  "hypoxic event".

## D17. RM02 Jones criteria and primary diagnosis
Notes: 95a46437, NB-87M:SYNC-CARD-RM02:policy_verdict.

**Decision: FIXED, both notes.** This reverses October's "accepted[0] unchanged". R2 rules the
label wrong: the musts treat active ARF.

Jones criteria (95a46437):
- CRP 18.4 mg/L is 1.84 mg/dL, below the 3.0 mg/dL minor-criterion threshold, so it is removed
  from every argument for recurrence.
- The population risk is stated in the patient block (canonical text in the plan). With it:
  - fever 38.2 C and ESR 48 mm/h count as minor criteria;
  - polyarthralgia counts as major;
  - active carditis is major;
  - ASO 340 is evidence of a preceding group A streptococcal infection.
- Recurrence is therefore met with 2 major criteria (Gewitz 2015).

Primary diagnosis (verdict):
- accepted[0] becomes "Cardiac syncope due to intermittent complete heart block from recurrent
  acute rheumatic fever with active carditis, on chronic rheumatic heart disease".
- The ARF differential entry is removed; its content moves to key evidence.
- `icd_codes[0]` stays I44.2.
- CENTRAL: add ARF labels to `I44.2+rheumatic`.

## D18. RM03 coronary criterion, VT exclusion and device
Note: NB-87M:SYNC-CARD-RM03:policy_verdict.

**Decision: FIXED.**
- Add `action-coronary-assessment`, recommended, accepting coronary_angiography or coronary_CTA.
  The stored angiography and CTA show the LAD CTO. This satisfies must R4.
- Add the EPS with PES (D6).
- Device must R2 gains "with no inducible sustained monomorphic VT at programmed ventricular
  stimulation".
- The differential VT entry cites the PES.
- D1 (exercise recommended) also applies: one of the syncopes was on stairs.

## D19. RP02 myxoma certainty, exercise and tilt
Note: NB-87M:SYNC-CARD-RP02:policy_verdict.

**Decision.**
- accepted[0] becomes "Cardiac syncope due to a right ventricular outflow tract mass most
  consistent with myxoma (histology pending), causing intermittent dynamic RVOT obstruction".
  FIXED. The synonyms are unchanged.
- Exercise: ALREADY-FIXED. It is labelled harm, with an RVOT-mass rationale. The exercise echo is
  labelled harm too (D4).
- Tilt: harm is kept. The note itself allows harm when "the haemodynamic risk is justified
  separately", and the existing rationale does so (preload reduction across a 90 mmHg dynamic
  obstruction; pack sec.4). DECLINED in part, with this reason.

## D20. RP03 genetic report
Note: d08aab43.

**Decision: CENTRAL (display).**
- The stored data are consistent. RYR2 is "Pathogenic"; KCNJ2 is "No pathogenic variants
  detected" with an empty interpretation.
- The review app prints `interpretation` above `test`, so the "Pathogenic" of the "Overall panel
  result" row reads as KCNJ2's.
- CENTRAL request: print label keys first.
- The worker also fills the four empty per-gene `interpretation` strings with "Negative" so the
  table cannot be misread.

## D21. RP03 cascade screening and iron
Notes: c42c1ec4, 99f45b73.

**Decision: FIXED.**
- R7: cascade screening to every first-degree relative, naming the mother, the sister and both
  children.
- R8 is rewritten per BSG 2021 (C9).

## D22. RP04 EEG reasoning
Note: 014edfe5.

**Decision: FIXED.**
- A normal interictal EEG does not exclude epilepsy, and antiseizure-drug failure is not evidence
  against it.
- The decisive evidence is the loop recorder: complete AV block with asystole during three typical
  witnessed episodes.
- Rewrite R0, KCE[0], differential[0], red_herrings[0] and the AED-levels criterion rationale
  (canonical text in the plan).

## D23. RP05 certainty, steroids and device
Notes: 5b75258e, 239d4a90, verdict.

**Decision: FIXED.**
- accepted[0] becomes "Cardiac syncope due to clinically diagnosed cardiac sarcoidosis
  (extracardiac histology with compatible cardiac imaging; no myocardial biopsy) with complete AV
  block and non-sustained VT" (HRS 2014 clinical pathway).
- R3: steroids only once infection is reasonably excluded, with timing set by the
  multidisciplinary team.
- R2: the device text in C9. "Do not defer" and "the indication stands even if AV conduction
  recovers" are removed. The second is not in a source verified this round.
- Driving: 1 month after an ICD (D8).

## D24. RS01 ICD choice and family history
Notes: 0af538d2, 6e00f5d4.

**Decision: FIXED.**
- R3 becomes the canonical individualised text (C9). R2 already says pace this admission.
- "an autosomal dominant pattern" (differential[0]) and "a familial conduction disease" (KCE[2])
  become "a family history suggesting, but not establishing, an inherited conduction disease;
  genetic evaluation decides".
- Likelihood stays high (judgement on CMR and age). D2 and D3 cover the test notes. The EEG
  (da138055) is already waste: ALREADY-FIXED, removal DECLINED (D3).

## D25. RS02 ICI myocarditis
Note: 02b0bfb9.

**Decision: FIXED.**
- red_herrings[1] and differential[0] say that a normal troponin and no CMR oedema make ICI
  myocarditis less likely without excluding it.
- "Most likely degenerative" becomes a stated working judgement.
- Add a must: repeat high-sensitivity troponin with CK, and keep ICI myocarditis in view
  (pembrolizumab, new LV dysfunction), with cardio-oncology input (ESC 2022 cardio-oncology).
- "checkpoint inhibitor myocarditis" stays in `rejected`. It is the alternative the work-up argues
  against, not a condition true in the case.

## D26. Comment-less verdicts and approvals
- NO-ACTION: verdicts M04, RP03, RS01. Their substance is in the same case's notes.
- RP04: avoided_actions, handled by D6.
- NO-ACTION: the 13 approvals (P02, P04, RM04, RP01, RS03, RS04, RS05, RS06, S01, S02, S04, S05,
  S06).
- The approved cases still receive the class findings listed in the plan index. These are additive
  avoided labels, plus RS05's coronary criterion and driving source.

## D27. Not changed this round, recorded
- Exercise test in P02 (approved, HCM): it gives the BP response and arrhythmia. It is not useless
  beside the required exercise echo. Unlabelled.
- Polysomnography in RS06: OSA is a flutter and AF risk factor (ESC 2024 AF-CARE). Unlabelled.
- Speech and language evaluation in RM01 serves the dysphagia must. Unlabelled.
- Performance status, gait, cognitive screen and audiometry stay unlabelled. They are harmless
  context, not useless for these patients.
- An orthostatic BP report is stored in 14 cases with no criterion (the other 16 have a recommended
  one). It is not a defect, because the order is unscored and unpenalised. It is listed as an open
  question.
