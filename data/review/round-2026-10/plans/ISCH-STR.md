# ISCH-STR: condition plan for the October 2026 review round

Lead plan for the 30 ISCH-STR cases (M01..M05, P01..P05, RM01..RM04, RP01..RP05, RS01..RS05,
S01..S06). Read `ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them.

All 97 notes are from Reviewer 2 and cover 29 cases (S06 was never reviewed). R2 approved RS01, RS05,
S02 and S05 (their notes still apply); P04 and RM01 are in progress; the rest need changes. In the
approved cases fix only real errors (order, numbers, guideline, engineering text) and log why.

Baseline (23 October 2026, before any edit): `perfect_agent.py` passes 30/30 with two warnings this
plan removes: the aetiological-lab criterion is answered by the initial labs (M01, M05, P01, P02,
P03, P04, RM01, RP01, RP02, RP03, RP05, RS04), and the P05 event-monitor criterion receives the
Holter report. Section 2 cites notes by 8-character prefix; section 4 gives full ids.

Use: apply the classes of section 2 that name your case (canonical text verbatim, `<...>` slots
filled), then the decisions of section 4, rebuild criteria, follow-ups, constraints and stop rule per
section 3, run both checks, write `logs/{CASE_ID}.md` citing every note id with its ruling.

New text: English, each field's existing spelling, no em or en dashes. New values must be plausible
for age, sex, renal function and medicines, and differ from the shared template values.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which source governs what

| question | source | key |
| --- | --- | --- |
| Acute management (imaging, IVT, EVT, BP, labs, stroke unit, early antithrombotic) | AHA/ASA 2026 early management of AIS: Prabhakaran S, Gonzalez NR, Zachrison KS, et al., Stroke 2026 | `[AHA_ASA_Stroke_2026]` (CENTRAL: pack allow-list) |
| Secondary prevention (antithrombotic by mechanism, carotid timing, AF, statin, dissection, PFO) | Kleindorfer DO et al., Stroke 2021;52:e364-e467 | `[AHA_ASA_2021_secondary]` (in VASC-DEM pack; CENTRAL) |
| Late-window EVT | DAWN, NEJM 2018;378:11-21; DEFUSE 3, NEJM 2018;378:708-718 | `[DAWN_2018]`, `[DEFUSE3_2018]` |
| Prolonged AF monitoring | Sanna T et al., NEJM 2014;370:2478-2486 | `[Sanna_2014]` |
| Mechanism (TOAST) | Adams HP et al., Stroke 1993;24:35-41 | `[Adams_1993_TOAST]` |
| Stroke in pregnancy (RP02, RS04) | ESO guideline on stroke in women, Kremer C et al., Eur Stroke J 2022;7(2), doi 10.1177/23969873221078696 | `[ESO_women_2022]` (CENTRAL) |
| Infective endocarditis (P03) | ESC 2023, Delgado V et al., Eur Heart J 2023;44:3948-4042 | `[ESC_endocarditis_2023]` (CENTRAL) |
| IE prophylaxis (P03) | AHA statement, Wilson WR et al., Circulation 2021;143:e963-e978 | `[AHA_IE_prophylaxis_2021]` (CENTRAL) |
| Dissection antithrombotic | CADISS (Lancet Neurol 2015), TREAT-CAD (Lancet Neurol 2021) | guideline key; trials by name in prose |
| PFO closure | AAN advisory, Messe SR et al., Neurology 2020;94:876-885; RoPE score | `[AAN_PFO_2020]` (CENTRAL) |
| HINTS | Kattah JC et al., Stroke 2009;40:3504-3510 | `[Kattah_HINTS_2009]` (CENTRAL) |

Rules:

- `[AHA_ASA_Stroke_2026]` replaces `[AHA_ASA_2019]` on every acute-management claim (328 occurrences
  across the 30 cases). `[AHA_ASA_2021_secondary]` replaces `[AHA_ASA_2014]` (34 occurrences). Keep
  `[AHA_ASA_2019]` only where a claim is genuinely historical; there should be none.
- One bracketed key per source, no duplicates in one list (`["[AHA_ASA_2019]", "[AHA_ASA_2019]"]`
  becomes one entry), and no free-text citation: remove the string
  `"AHA/ASA acute ischemic stroke guideline 2026"` everywhere (123 occurrences, always next to the key).
- Cite a section or class only where the reviewer gave it (§4.3, §4.6.3, §4.7, §4.7.2, §4.7.3,
  §4.12, §3.3, Early Secondary Prevention rec 7); number nothing else from memory. The pack's
  literature-required and drug-check-required positions are superseded by rulings 5 and 6.

### 1.2 Canonical facts (use these, do not restate them differently)

Reperfusion, IV thrombolysis (IVT):

- Standard window: within 4.5 hours of last known well (LKW). Agents: alteplase 0.9 mg/kg (maximum
  90 mg) or tenecteplase 0.25 mg/kg (maximum 25 mg). Door-to-needle target under 60 minutes.
- LKW is the last time the patient was seen at baseline. It is at or before the first symptom, never
  after it. A fluctuating course resets LKW only if the patient returned fully to baseline.
- Extended window, two separate limbs (AHA/ASA 2026 §4.6.3, COR 2a):
  (a) unknown onset with DWI-positive, FLAIR-negative lesion (WAKE-UP);
  (b) wake-up stroke within 9 hours of the midpoint of sleep, or 4.5 to 9 hours from LKW, with
  salvageable penumbra on automated perfusion imaging by EXTEND criteria (penumbra-to-core ratio above
  1.2, mismatch volume above 10 mL, core below 70 mL), only in patients not eligible for thrombectomy.
  The 1.8 ratio with mismatch above 15 mL belongs to TIMELESS and TRACE-III; do not use it for limb (b).
- Every wake-up or unknown-onset case addresses both limbs: (a) by the FLAIR finding, (b) by the sleep
  midpoint, EVT eligibility and a perfusion result or a stated reason for none.
- Blocking findings: any intracranial haemorrhage, including haemorrhagic transformation already
  present before treatment; infective endocarditis (IVT contraindicated); a DOAC taken within 48 hours
  (a normal INR does not exclude its effect); INR above 1.7 on a vitamin K antagonist; known or
  suspected aortic arch dissection. A non-disabling minor deficit is not an indication for IVT (give
  antiplatelet therapy instead).
- Extracranial cervical artery dissection is not a contraindication to IVT. Intradural (intracranial)
  dissection carries subarachnoid haemorrhage risk; state that the benefit is uncertain.
- Only glucose must be known before IVT; CBC and coagulation are awaited only if an anticoagulant,
  coagulopathy or thrombocytopenia is suspected. ECG and troponin do not delay reperfusion; CTA does
  not wait for creatinine.

Reperfusion, thrombectomy (EVT):

- Anterior circulation LVO (ICA or M1) within 6 hours: NIHSS 6 or more, pre-stroke mRS 0 to 1,
  ASPECTS 3 to 10: COR 1 (§4.7). Give IVT first when eligible; do not wait to see its effect.
- 6 to 24 hours: DAWN or DEFUSE 3 selection (clinical-core or perfusion mismatch).
- Basilar artery occlusion within 24 hours of symptom onset: NIHSS 10 or more, pre-stroke mRS 0 to 1,
  PC-ASPECTS 6 or more: COR 1 (§4.7.3).
- Isolated P2, M2 distal or M3 occlusions are distal or medium vessel occlusions with no graded EVT
  indication; ESCAPE-MeVO and DISTAL (NEJM 2025) showed no benefit.
- Surgery is not an absolute contraindication to EVT.

Blood pressure:

- Before IVT: below 185/110 mmHg (COR 1); for 24 hours after IVT: below 180/105 mmHg.
- Before EVT: at or below 185/110 mmHg (COR 2a). After successful recanalization, do not target
  systolic below 140 mmHg (ENCHANTED2/MT, OPTIMAL-BP: intensive lowering was harmful).
- No IVT and no EVT, BP below 220/120 mmHg, no comorbid indication: starting or restarting
  antihypertensives in the first 48 to 72 hours does not prevent death or dependency (§4.3 rec 4,
  COR 3 No Benefit, LOE A). There is no "140/90 floor" in the guideline.

Carotid and dissection:

- Emergent carotid endarterectomy within 48 hours for AIS or stroke in evolution from high-grade
  carotid stenosis without intracranial occlusion: COR 3 No Benefit (§4.12). Revascularization of a
  symptomatic 70 to 99 percent stenosis between 2 days and 2 weeks is governed by the 2021 secondary
  prevention guideline (COR 1); 50 to 69 percent depends on patient factors.
- Extracranial carotid or vertebral dissection: antiplatelet or anticoagulant for at least 3 months
  (COR 2a, LOE B-R, Early Secondary Prevention rec 7; CADISS and TREAT-CAD enrolled extracranial
  dissection only). Intradural extension: antiplatelet, avoid anticoagulation for subarachnoid
  haemorrhage risk; state that the trial evidence does not cover it.
- Spontaneous cervical ICA dissection starts 2 to 3 cm distal to the bifurcation, sparing the bulb.
  Intramural haematoma is T1 isointense in the first hours; the T1-bright crescent appears from about
  day 2 to 3. Carotid-dissection Horner is postganglionic: facial sweating is spared (sudomotor fibres
  follow the external carotid).

Secondary prevention by mechanism (musts):

- Atrial fibrillation: a DOAC in preference to warfarin; start within 48 hours for minor or moderate
  infarcts and on day 6 to 7 for major infarcts once haemorrhage is excluded (ELAN, NEJM 2023;
  OPTIMAS, Lancet 2024). State CHA2DS2-VASc and HAS-BLED from the record. Apixaban 2.5 mg twice daily
  only with two of: age 80 or more, weight 60 kg or less, creatinine 1.5 mg/dL or more.
- Minor non-cardioembolic stroke (NIHSS 3 or less) or high-risk TIA: aspirin plus clopidogrel for 21
  days, then single antiplatelet (CHANCE, POINT). Otherwise single antiplatelet.
- Statin: high-intensity, LDL target below 70 mg/dL, for an atherosclerotic mechanism. Not in
  pregnancy, not mandated for a non-atherosclerotic mechanism without a lipid indication.
- Pregnancy: LMWH or low-dose aspirin; no warfarin (teratogenic, fetal bleeding); no statin; MRI
  without gadolinium preferred; CT and iodinated contrast are not withheld when they decide reperfusion.
- Sumatriptan is contraindicated after ischaemic stroke and in antiphospholipid syndrome. ACE
  inhibitor with alteplase: watch for orolingual angioedema.
- Infective endocarditis: no anticoagulation or antiplatelet started for the stroke; exclude mycotic
  aneurysm; TEE is recommended in suspected IE with a positive TTE, to detect perivalvular
  complications (ESC 2023). Endocarditis prophylaxis is one pre-procedure dose, not a course, and a
  bicuspid aortic valve is not an indication.

Examination and scales:

- NIHSS items and ranges: 1a LOC 0-3, 1b questions 0-2, 1c commands 0-2, 2 gaze 0-2, 3 visual 0-3,
  4 face 0-3, 5a/5b arms 0-4 each, 6a/6b legs 0-4 each, 7 limb ataxia 0-2 (one item for all limbs),
  8 sensory 0-2, 9 language 0-3, 10 dysarthria 0-2, 11 extinction and inattention 0-2. There is no
  hand item, no gait or truncal ataxia item; nystagmus, saccadic pursuit and diplopia do not score on
  gaze. Arm 3 means no effort against gravity; arm 4 no movement; ataxia is 0 when testing is limited
  by weakness. Extinction in one modality scores 1; in more than one modality, or profound
  hemi-inattention, 2.
- GCS: alert is E4; confused speech is V4; obeys commands is M6; localises is M5.
- A destructive hemispheric lesion deviates the eyes toward the lesion. A supranuclear (UMN) facial
  palsy spares the forehead and eye closure; inability to close the eye is lower motor neuron.
- Neglect follows a non-dominant (usually right) hemisphere lesion and is of the left side.
- HINTS central pattern: normal head impulse (no corrective saccade), direction-changing nystagmus,
  skew deviation. A positive head impulse with a corrective saccade is the peripheral pattern.
- Troponin: COR 1 baseline that must not delay reperfusion (§3.3); an elevated value is acted on.

---

## 2. Error classes in this condition

Each class gives the defect, the notes it resolves, the cases it covers, and the decided fix.

### C1. Pathway order inverted (PATTERNS 1; all 30 cases)

Notes: 6feeb306 (M01), eae4a343 (M02), 132ec224 (P04), 6ecd20c2 (P05), f7f3b32d (M04).

Every case runs echo, Holter, aetiological panel, literature and drug check first and the CTA last;
P04 and P05 show a completed 48-hour Holter (P05 also a 30-day monitor) before the vessel imaging
that decides reperfusion. Fix: order as section 3; the CTA is the first follow-up (RP02 excepted).
M02 eae4a343 (required NCCT, labs, ECG never appear as steps) is FIXED by criterion order plus the
CENTRAL UI request.

### C2. Monitoring results shown before they can exist, and type mismatches (PATTERNS 3)

Notes: f7f3b32d (M04), 6ecd20c2 (P05), 132ec224 (P04).

- Every monitor report opens "Recorded on the stroke unit after admission, <24 or 48> hours." and
  follows the CTA.
- `monitor_type` (report, `tool_parameters`, criterion) agrees with `duration_hours` and the
  vocabulary (`holter_24h`, `holter_48h`, `event_monitor_14d`, `event_monitor_30d`, `telemetry`,
  `implantable_loop_recorder`; no `holter_72h`). 48 h labelled `holter_24h`: P04, P05, RP01, RP02,
  RP03, RP04, RS04, S02; 72 h: M02, P01. Set 24 or 48 h with the matching type; criterion
  alternatives `holter_24h`, `holter_48h`, `telemetry`.
- Prolonged outpatient monitoring is a must, not a stored result: remove the P05 `event_monitor_30d`
  criterion and follow-up; RP03's `event_monitor_30d` criterion becomes inpatient Holter.

Canonical musts: "Admit to a stroke unit with continuous cardiac monitoring (telemetry) for at least
the first 24 hours." (replaces the template "Initiate continuous telemetry and obtain prolonged cardiac
monitoring to detect paroxysmal atrial fibrillation"). Sinus rhythm with an embolic or cryptogenic
pattern only: "If inpatient monitoring finds no atrial fibrillation, arrange prolonged ambulatory
rhythm monitoring (30-day event monitor or implantable loop recorder) after discharge." AF already on
the ECG: the monitoring must concerns rate control (C14).

### C3. Extended-window thrombolysis decided on one limb only (PATTERNS 2)

Notes: 06456aa6 (M01), b798000b (M02), 5e0dbec2 (M03), 6d879e51 (P04). Survey: P05, RS03.

- M01, M02 (wake-up, FLAIR positive, no LVO, within 9 hours of the sleep midpoint): add a
  `CT_perfusion` criterion (recommended, id `ct-perfusion-extended-window`) and a follow-up that does
  not meet EXTEND (core, penumbra, ratio, mismatch in mL), so "no IVT" stands on the right limb.
- M03: CTP becomes recommended; ratio 1.4 meets 1.2, mismatch 8 mL fails 10 mL, so no IVT; remove
  the 1.8 threshold and the thrombectomy-trial reasoning (no LVO).
- P04: limb (b) is closed because she is EVT eligible; CTP becomes required (it selects EVT at 8 h).
- P05, RS03: section 4.

Canonical key evidence: "Wake-up stroke: FLAIR is positive, so the DWI-FLAIR limb is closed; the
sleep midpoint is <time>, <h> hours before arrival, and the patient <is not / is> an EVT candidate,
so <CTP <meets / does not meet> EXTEND criteria (core <x> mL, mismatch <y> mL, ratio <z>) / the
perfusion limb does not apply>."

### C4. Reperfusion decision not stated, contradicted, or inapplicable (PATTERNS 1, 2)

Notes: a407727c (M05), db9768a7 (P04), 0bc84371 (RS01), c0233fc3 (RS05), 3f611291 (S04),
55e9c9c7 and 19d1e303 (RP01), 4660dbc9 (RM02), 19ff066b (RP03), 16f5be33 and d703ff12 (RS03),
7eec1867 and 4e5a5ed6 (RS02), cd879e2d (RS04), 10f6a890 (P02), 7d003b88 (P03, BP part).

The template LKW/NIHSS, door-to-needle and pre-IVT BP musts are pasted into 21 to 23 cases whatever
the eligibility, and no case states the decision. In every case:

1. One case-specific LKW must: "Establish last known well (<time>, <h> hours before arrival) and the
   NIHSS (<n>)."
2. One decision must: "IV thrombolysis: <give / do not give> because <reason>. Thrombectomy:
   <proceed / not indicated> because <reason>." Example (S01): "IV thrombolysis: give (2 hours 47
   minutes from LKW, no contraindication, INR 0.9). Thrombectomy: proceed for the left M1 occlusion
   (NIHSS 22, pre-stroke mRS 0, ASPECTS <n>, within 6 hours); do not wait for the response to
   thrombolysis."
3. Door-to-needle and pre-IVT BP musts only where IVT is given. BP above 185/110 on arrival (M05,
   RS05, S02, S03, S04, S05): "Lower blood pressure below 185/110 mmHg with IV labetalol or nicardipine
   before IV thrombolysis, then keep it below 180/105 mmHg for 24 hours."
4. EVT cases: "Proceed to mechanical thrombectomy for the <vessel> occlusion (<criteria met>); keep
   blood pressure at or below 185/110 mmHg before the procedure and do not target systolic below 140
   mmHg after successful recanalization."
5. No reperfusion musts where reperfusion is not a question (RM02, RM03: no deficit, no infarct).
6. No must that requires IVT steps while a prohibition forbids IVT (P02, P03, RS02, RS03).

### C5. The "below 140/90" blood pressure prohibition (PATTERNS 2, 4; 27 cases)

Notes: df9be70d (M01), db9768a7 (P04, truncated second half).

The prohibition "Do not aggressively lower blood pressure below 140/90 mmHg in the acute phase
outside the tPA window" is in every case except M05, P04 and RS05 (P04 and M05 carry other BP
wording). Replace it. Canonical, for cases with neither IVT nor EVT:

"Do not start or restart antihypertensive treatment in the first 48 to 72 hours for blood pressure
below 220/120 mmHg in a patient who receives neither IV thrombolysis nor thrombectomy and has no
comorbid indication; it does not prevent death or dependency (AHA/ASA 2026, COR 3: No Benefit)."

For cases that receive IVT or EVT, remove it (the BP musts of C4 govern). M05's "permissive 140 to
180 systolic" must and P04's "for thrombectomy-only, avoid excessive BP lowering" are replaced by the
C4 BP musts.

### C6. Template secondary-prevention musts that ignore the mechanism (PATTERNS 2, 4)

Notes: 027c14a1 (P02), 7d003b88 (P03), 60a69345 (RP02), dc0e0aee (RS01), ec9af643 (S04), f9e644a8
(M05).

"Begin secondary prevention (antiplatelet or anticoagulation) and high-intensity statin per
mechanism" (20 cases) becomes one mechanism-specific must from section 1.2:

- AF (M03, P04, RM02, RS01, RS03, S01 to S05; M01, M02 where Holter finds AF): "Start <DOAC and
  dose> for atrial fibrillation (CHA2DS2-VASc <n>, HAS-BLED <n>) <within 48 hours / on day 6 to 7>
  once follow-up imaging excludes haemorrhagic transformation; do not bridge with heparin." Statin
  only for a coexisting atherosclerotic indication.
- Large artery (M01, M05, RS05): antiplatelet (DAPT 21 days if NIHSS 3 or less), high-intensity
  statin, LDL below 70 mg/dL, revascularization timing per section 1.2.
- Small vessel (M02, S06, RP05): antiplatelet, statin per LDL, long-term BP below 130/80 mmHg.
- Dissection (M04, P01, RM01, RM03, RM04, RP02, RS02): section 1.2, 3 months.
- Moyamoya (P02): aspirin, no anticoagulation, statin only on a lipid indication, neurosurgical
  revascularization referral, avoid hypotension, dehydration and hyperventilation.
- IE (P03): no antithrombotic; antibiotics; cardiac surgery evaluation.
- PFO (P05, RP03): antiplatelet; closure discussion (AAN 2020, RoPE); anticoagulation for DVT (P05).
- APS (RP04): warfarin INR 2 to 3 once confirmed at 12 weeks; no DOAC.
- Pregnancy (RP02, RS04): LMWH or low-dose aspirin, no statin, no warfarin.

The prohibition "Do not start full-dose anticoagulation in the acute phase of a large infarct..."
stays, rewritten to ELAN timing, only in AF cases with a large infarct; remove it elsewhere.

### C7. Drug-interaction checks: tier and content (ruling 6; PATTERNS 1)

Notes: ec825b6a (P01), ec9af643 (S04), 4660dbc9 and ffd8459c (RM02), 7d4454af and 4332d93d (RP04),
7d003b88 (P03).

Required in all 30 today, often as an alteplase checklist that ignores the patient's drugs. Required
only with the concrete issue named in the output:

- M01, M02: apixaban dosing with CKD 3a, stop aspirin. M05: clopidogrel with omeprazole (switch to
  pantoprazole). P01: aspirin allergy (clopidogrel or anticoagulation), stop ibuprofen and
  sumatriptan. P02, RM01: stop the combined oral contraceptive (P02 also escitalopram with
  antiplatelet). P03: suspected IE contraindicates IVT; stop ibuprofen. RM02: apixaban restarted 2
  days ago (IVT contraindicated whatever the INR), ketorolac with apixaban and aspirin. RM03, RP05:
  sumatriptan; ibuprofen (RM03). RM04: ibuprofen with antiplatelet. RP02, RS04: pregnancy (LMWH, no
  warfarin, no statin, gadolinium). RP04: sumatriptan, ibuprofen, prolonged aPTT without
  anticoagulant. RS03: enoxaparin on the list, apixaban after recent oesophagectomy and cancer. S03:
  warfarin listed but stopped 3 weeks ago, INR 1.2. S04: recurrent epistaxis, DOAC choice and timing.
- Recommended: M03, M04, P04, P05, RP01, RP03, RS01, RS02, RS05, S01, S02, S05, S06.

Placement: immediately before the decision it informs (section 3); after the CTA where it informs
IVT (P03, RM02, RP04, S03). The output lists the patient's actual medicines and allergies; its
`contraindications` field is never empty when the case has one.

### C8. Literature searches as steps, orphan literature outputs (ruling 5; survey)

Every case has a recommended literature criterion and 1 or 2 outputs, several received by no
criterion (P01, RM02, RM03, RP02, RP03, RP05, RS04, S02). The criterion becomes optional (one at most),
placed last; remove orphan outputs or keep one general-evidence output, never the case's expected
text. RS04 cites an unverifiable "AHA/ASA Scientific Statement ... Too G, Wen T, 2022": replace with
the ESO 2022 guideline. ATTENTION and BAOCHE are NEJM 2022.

### C9. Aetiological laboratory panels: orphans, duplicates, contradictions (PATTERNS 1, 3, 4)

Notes: ba9bdca8 (P01), 7fc996b4 (P05), 7c967ef5 (RP03).

Survey: orphan hypercoagulability follow-up in 19 cases; an initial "Exclusion studies" panel
(`sig` "Ordered to exclude an alternative cause...") duplicates or contradicts it in P01, P02, P05,
RM01, RP01, RP02, RP03, RP05, RS04; orphan autoimmune and connective-tissue panels in P03, RM01; a
"temporal artery biopsy" under `interpret_labs` in RM02; lipid/HbA1c follow-ups duplicating the
initial labs in RS05, S06.

- Remove every initial "Exclusion studies" panel (scaffolding; its `sig` is leakage); move any
  troponin there to the cardiac panel with a value.
- Keep an aetiology criterion (recommended; required in RP04) only in P05, RP03 (young, PFO), RP04
  (APS), RS04 (pregnancy), RP02 (prior TTP: ADAMTS13, haemolysis and antiphospholipid in one
  follow-up), RP05 (young-stroke screen). The follow-up's analytes match the criterion's `panels`
  and the initial labs do not contain them.
- Remove criterion and follow-up elsewhere (M01, M02, M03, RS01, RS02, RS03, S01 to S04, P01, RM01,
  RM03, RM04, P02, P03, RP01): thrombophilia testing is not indicated in these mechanisms.
- Lipids and HbA1c are in the admission bloods: remove the separate criteria (M01, M05, P04, S06,
  RP01) and the RS05 and S06 follow-ups; targets go in the musts.
- Factor V Leiden: P01 drops both entries; P05 keeps the follow-up (heterozygous), drops the initial
  row.
- RP03: VITT is excluded (inactivated vaccine, 48 hours not 5 to 30 days, normal platelets and
  D-dimer): say so in key evidence, restrict the must to adenoviral vector vaccines, no VITT testing.

### C10. Answer leakage and timeline errors in the patient block (leakage policy; PATTERNS 3)

Notes: 06456aa6 and b798000b (HPI conclusions), cd879e2d (RS04), d3d1bb91 (S03), 9685cde6 (RP04),
9e53616c (P05), eea99434 (RS01), bc4354fa (P02), 212fe881 (RS02).

- Remove eligibility verdicts from the HPI, keep the times: "placing him/her outside the standard IV
  tPA/alteplase window" (M01, M02); "This exceeds the standard 4.5-hour window..." (M03); "placing the
  patient definitively outside the 4.5-hour window" and the sentence listing the ordered NCCT, CTA and
  CTP (P04); "well within the ... window" (S02, S06); "placing her within the standard IV alteplase
  window" (S05). M04: remove "A non-contrast CT head was ordered and reported as normal".
- Times and antecedents as section 4 (RS04, S03, RP04, RP01, RS02). Prior infarcts seen on imaging go
  into the history (RS01; S02, S03 if the MRI keeps an old lacune).

### C11. Reports: impression omits the finding, contrast flag, management text (PATTERNS 3, 5)

Notes: ef70fcc1 (RM01), ec46ecc7 (RM03), d923cc86 (RS01), 3fea7d10 (RS03), c7026407 (RS04),
50ffe53e (P02), eea99434 (RS01), fdfaae93 (S01), 0fd09831 (RP05).

- CTA impression opens with the principal finding of its findings ("<Complete / near-complete>
  occlusion of the <side> <segment>..."). Omitted in RM01, RM03, RS01, RS03, RS04 (basilar), S01,
  S02, S03, S04.
- CTA `contrast_used` true. False in M01, M03, P01, RM01, RM02, RM03, RP01, RP02, RP03, RS01, RS02,
  RS03, RS04, S01, S02, S03.
- NCCT template (M01, M03, M05, P01, P02, P03, RM01, RM02, RM03, RP01, RP02, RP03, RP04, RS01, RS02,
  RS03, RS04, S01, S02, S03, S04): remove "does not justify withholding treatment", "Nothing on this
  study contraindicates intravenous thrombolysis. The purpose of the scan is exclusion...", "would
  mandate neurosurgical consultation rather than thrombolysis" (P01, RM03, RP01, RP02, RP04), "must
  not delay angiography" (RS04); replace "in the clinically implicated territory" (P02, P03, RM01,
  RM02, RM03, RP03), "in watershed" (M05), "in basilar" (RP01, RS04) with the anatomical territory.
  Canonical normal impression: "1. No acute intracranial haemorrhage. 2. No established infarct, no
  hyperdense vessel sign and no mass lesion. ASPECTS 10." (posterior circulation: PC-ASPECTS or none).
- MRI impression names the acute infarct, occlusion and dissection of its findings, and nothing they
  lack ("chronic small vessel ischemic disease" without white matter findings: RS01, S01, S03).
- Echo: `echo_type` set in output and `tool_parameters`; a real echo impression, not "Abnormal
  values: X (H)"; LVEF 50 to 55 percent not flagged high; "All values within normal limits." (P02,
  RM01, RM03, RP02) becomes a real normal TTE report.
- RP05 genetic report: remove PP1 (no relative genotyped); PS1, PM2, PP3 remain.

### C12. Imaging timing: FLAIR age against LKW, haematoma age (PATTERNS 3)

Notes: fdfaae93 (S01), c9b7c467 (S05), 667da1af (RM03), 17db3372 (RM04).

- A FLAIR description must agree with LKW. Under 4.5 hours: "DWI hyperintense with ADC reduction; no
  corresponding FLAIR hyperintensity (DWI-FLAIR mismatch)" or "faint FLAIR change less conspicuous
  than DWI". Survey: S01 (2 h 47, ">3-4 hours"), S05 (2 h 58, "3-4 hours"), RS01 (2 h 52, ">3 hours"),
  S02 (2 h 22, ">2 hours", "subacute"), S04 (2 h 22, ">3 hours"), RS05 (38 min, ">3 hours"), RS02
  (3 h, "beyond 3 hours"). Fix all.
- Intramural haematoma age per section 1.2 (RM03 acute, RM04 subacute justified by 3 days of neck
  pain).

### C13. NIHSS and GCS miscounts and invented scale structure (PATTERNS 2; a series defect per R2)

Notes: a46588b0 (M01), d1ad43a9 (M03), b36e42fb (M05), 7695631d (P01), ceadf1cd and bcb508a7 (P02),
0f2a9dec (P03), a220ccd8 (RM04), de5e529f (RS05), f6628b06 (S01), 9802d420 (S05), 8b01e6c6 (RP03 GCS).

Recount the NIHSS of all 30 cases from the exam with section 1.2. The exam is the primary data: set
the total to the recount unless a note says otherwise, itemise with real item names ("NIHSS <n>
(<item> <score>, ...)"), and update every mention (HPI, musts, key evidence, difficulty text,
drug-check output). Re-check EVT thresholds (6 anterior, 10 basilar).

### C14. Abnormal results left without action, impossible numbers (PATTERNS 2, 3)

Notes: 9c627e7e (M01), 55291633 (M03), 3c9586d9 and 22f804cf (RS01), 97a9f686 (RP01), 73bf8a81 (RM03).

- Anion gap (Na - Cl - HCO3) 4 to 16: M01 -1 (chloride about 91), S02 -4 (chloride about 96), M03 26
  (sodium 151 unexplained: normal sodium, gap about 12, drop hypernatraemia), S03 26 (chloride about
  108), M02 24 and S04 19 (raise chloride). Recompute osmolality text.
- Hct about 3 x Hb: M01 (Hct about 37), S03 (Hct about 39.5). P03: urinalysis rows renamed "Urine
  WBC", "Urine RBC". M01: one creatinine everywhere (labs 1.4 vs drug check 1.52/eGFR 52).
- Troponin above reference (RS01 0.05, S01 0.07, S02 0.05, S03 0.08, S04 0.05; RS05 has a must):
  "Repeat troponin and review the ECG; the mild elevation is most likely <demand ischaemia from rapid
  atrial fibrillation / neurogenic myocardial injury>; it does not delay reperfusion." Set
  `clinical_significance` to match.
- Rapid AF (RS01 108 to 142; S03, S04, RS03 on Holter): rate-control must.
- RP01: result or remove the thiamine row; must "Give IV thiamine before any glucose-containing fluid
  in this patient with alcohol use disorder."
- RM03: "Pharmacologic confirmation of the Horner syndrome is not needed once vessel imaging shows the
  dissection." replaces "apraclonidine ... not yet performed".

### C15. Neuroanatomy and laterality errors (PATTERNS 2, 3)

Notes: f9ddb5ea (M02), b36e42fb (M05, neglect side), c97b3f6e (S01), 20b2416f (S03), 5f9d3088 (S04),
3451a4bc (RP03), 8b0515f8 (RS03), 64a4f269 (M04), 1fe2a211 (P01), 68d979b1, 4a90422f, 4d4b454f
(RP02).

Apply section 1.2 and the per-case decisions in section 4. Every side mentioned in chief complaint,
HPI, EMS description, exam, NIHSS itemisation, key evidence and differential must agree with the
lesion side and with dominance (`handedness`).

### C16. Contrast allergy and CKD against a mandatory CTA (PATTERNS 1)

Notes: 799ea64c (S02), 0a65085d (S03).

Decision: CTA stays required. A mild prior contrast reaction and CKD 3a do not justify delaying vessel
imaging in an LVO candidate within the window. Replace S02 must "Adjust contrast use for CKD stage 3a"
and S03 prohibition "Do not give full-dose contrast in CKD without renal protection" with the
canonical must: "Proceed with CTA without waiting for creatinine; a prior mild contrast reaction and
CKD stage 3a do not justify delaying vessel imaging. Give premedication only if it causes no delay,
and have treatment for a reaction at hand." Remove the CKD prohibition.

### C17. Engineering leakage, stale metadata and template key evidence (PATTERNS 5)

Notes: 2e2ccbff (P05, "document in metadata.vocab_gap" inside a must).

- Remove from key evidence "Tier per the July 2026 clinical review..." (30 cases) and the three "Off-
  pathway modality for order_advanced_imaging (modality=...)" lines (23 cases). Keep the AHA/ASA 2026
  sequencing line only as a clinical statement. Rationales give a reason, not a copy of the label
  (identical NCCT, CTA, labs, MRI label/rationale pairs in all 30).
- `metadata.case_body_concerns`: resolve, then empty the list (log it). M03 BMI: history becomes
  "Overweight (BMI 29.8)". M05, P04, RP05, S06 mock-server notes and P01, P02, P03, RM01 "required
  tool has no output": stale, delete. P05 venous imaging: fixed in section 4; empty `vocab_gap`.
  RP01 ethanol: differential says ethanol 2.3 per mille (intoxicated) but focal deficits and the
  basilar occlusion exclude pure intoxication. S01, S03, S04: fixed by C15.

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers (keep criterion_ids; new ones get descriptive ids)

| # | criterion | tier | notes |
| --- | --- | --- | --- |
| 1 | NCCT (`order_ct_scan` contrast false) | required | all |
| 2 | Core labs (glucose, CBC, coagulation, creatinine, troponin) | required | all |
| 3 | ECG | required | all |
| 4 | CTA head and neck (`order_ct_scan` angiography true, contrast true) | required | all except RP02 (MRA instead, section 4) |
| 5 | MRI stroke protocol | optional | required in RP02 only (pregnancy, MRA replaces CTA) |
| 6 | CT perfusion | recommended M01, M02, M03; required P04 | absent elsewhere |
| 7 | Case-specific diagnostic core | as section 4 | P03 blood cultures (required), P03 TEE (required); RP05 NOTCH3 (required); RP03 MR venography (recommended); P05 lower-limb venous duplex (recommended); RM01 EEG (optional) |
| 8 | Drug-interaction check | per C7 | placed before the decision it informs |
| 9 | Echocardiogram | required: M03, P03 (TTE then TEE), P04, P05, RP01, RP03, RP04, RS04; recommended elsewhere | |
| 10 | Inpatient cardiac monitoring | required: M01, M02, M03, P04, P05, RP01, RP03, P03 (telemetry for conduction block); recommended elsewhere | |
| 11 | Aetiological labs | per C9 | |
| 12 | Literature search | optional, last, at most one | |

### 3.2 Follow-ups and initial outputs

- `initial_tool_outputs` keeps NCCT (`ct`), core labs, ECG and MRI; everything else is a follow-up.
- Follow-up order: CTA, CTP, case-specific diagnostic core, drug check (where it informs reperfusion
  or the diagnosis), echocardiogram, monitoring, aetiological labs, drug check (where it informs
  secondary prevention), literature.
- Every follow-up is received by a criterion (`perfect_agent.py -v`), except one kept literature output.

### 3.3 Sequence constraints (replace the template hard NCCT to drug-check constraint)

- NCCT before CTA: `soft`, reason "Non-contrast CT excludes haemorrhage before vessel imaging and the
  reperfusion decision.", `[AHA_ASA_Stroke_2026]`.
- CTA before echocardiogram and CTA before cardiac monitoring: `soft`, reason "Vessel imaging decides
  reperfusion; cardiac aetiology is studied after the acute decisions."
- CTA before CTP where CTP exists: `soft`.
- No `hard` constraint (no reverse order is unsafe in itself).

### 3.4 Stop rule, exemptions, avoided actions

- `required_before_assessment`: every required criterion after the tiers above.
  `max_additional_actions`: 1 in every case (one overlapping vascular study such as carotid duplex
  after CTA is reasonable; 0 today).
- No panel exemption: CT, LABS and ECG stay everywhere (RP02 keeps the NCCT).
- Keep the three waste avoided actions (EEG, CSF, EMG/NCS) with the 2026 key; RM01 has no EEG avoided
  entry (EEG is its optional criterion). RP02, RS04: avoided action `analyze_brain_mri` with
  `contrast: true`, severity `contraindicated`, if not present.

---

## 4. Per-case index

Notes are listed with the class or the decision that resolves them. "Survey" items have no note but
must be fixed. Every case also gets the all-case classes C1, C2, C5 (where the 140/90 text is
present), C6, C7, C8, C9, C11 (NCCT template, CTA contrast where listed), C13 (recount), C17.

### ISCH-STR-M01 (man, 67, wake-up left MCA, symptomatic left ICA 60 to 70 percent, PAF on Holter; R2 needs_changes)

- `06456aa6-f505-4f49-b220-158a054d7df8` C3: add CTP (recommended) failing EXTEND; remove HPI conclusion.
- `a46588b0-d665-4f1a-b171-ed189be9ca6e` C13: recount (at least 7); update total everywhere.
- `9c627e7e-de27-444d-881f-4619f7b832d2` C14: chloride to about 91.
- `6feeb306-8789-4d4c-ac6c-7f5c82227d14` C1: CTA first follow-up.
- `df9be70d-251c-41d3-9761-664de7040cd6` C5: canonical COR 3 prohibition (BP 183/98, not reperfused).
- Survey: Hb/Hct and creatinine (C14); neuropathy in the exam absent from PMH (add diabetic
  peripheral neuropathy to PMH, he takes metformin and glipizide); carotid must: revascularization
  between 2 days and 2 weeks per AHA/ASA 2021 for the 60 to 70 percent symptomatic stenosis
  (case-dependent; mixed mechanism with PAF: state the decision); anticoagulation for PAF plus
  statin.

### ISCH-STR-M02 (woman, 58, wake-up right corona radiata, multifactorial; R2 needs_changes)

- `f9ddb5ea-7835-4e8c-8253-b67625de22b6` C15: "Left lower facial droop".
- `b798000b-b61d-4b76-8fdd-ff4eda0e651a` C3, C10: add CTP failing EXTEND (small subcortical infarct, no mismatch); remove HPI
  conclusion.
- `eae4a343-7b3f-48eb-b231-9c299243a6b1` C1 plus CENTRAL UI.
- Survey: anion gap 24 (C14); Holter 72 h labelled 24 h (C2); CTA findings list empty: write findings
  matching the impression.

### ISCH-STR-M03 (man, 73, wake-up left MCA superior division, PAF; R2 needs_changes)

- `5e0dbec2-ea6c-4420-9b68-5b07c716b8ee` C3: restate on limb (b); remove 1.8 and LVO reasoning; CTP recommended.
- `55291633-d7b2-4e6a-8497-235e3aa19058` C14: sodium normal, gap about 12.
- `d1ad43a9-a011-45bc-ae0f-0c7d77da43ba` C13: recount (at least 8).
- Survey: BMI concern (C17); CTA contrast; echo required, Holter required (PAF burden 14.6 percent
  decides anticoagulation); left ICA 55 to 60 percent stenosis: state that the mechanism is
  cardioembolic and the stenosis is managed medically unless reclassified.

### ISCH-STR-M04 (man, 58, right lateral medullary infarct, right V3 dissection; R2 needs_changes)

- `f7f3b32d-47f2-4ee0-a499-26638a2655ff` C1, C2: Holter after CTA, recorded during admission.
- `64a4f269-6ef3-4cf0-aba8-c4d134f4231e` C15: "head impulse test normal bilaterally (no corrective saccade), a central sign".
- Survey: NIHSS itemisation invents items ("right facial sensory loss", "crossed sensory findings"
  are one sensory item; recount); HPI NCCT result leak (C10); decision must: LKW 2 hours, IVT if the
  deficit is disabling (extracranial dissection is no contraindication, CTA shows no intracranial
  extension); no EVT (no LVO); dissection antithrombotic per section 1.2; lisinopril angioedema
  monitoring if IVT.

### ISCH-STR-M05 (man, 70, right internal watershed, right ICA 85 to 90 percent; R2 needs_changes)

- `f9e644a8-ba54-43b7-ada4-1fb2d1b91165` C6: must becomes "Refer for right carotid revascularization (endarterectomy or
  stenting) between 2 days and 2 weeks; emergent endarterectomy within 48 hours is not beneficial
  (AHA/ASA 2026 §4.12, COR 3 No Benefit)"; cite the class I indication to `[AHA_ASA_2021_secondary]`.
- `a407727c-db4a-4f39-9db6-a6c3bf45b838` C4: decision: IVT candidate (LKW 2 hours, disabling left arm weakness, colonoscopy 5
  days ago without bleeding is not a contraindication): lower BP below 185/110 cautiously, then IVT;
  remove the permissive 140 to 180 must; keep a must on avoiding hypotension and volume repletion.
- `b36e42fb-f85b-40b1-9223-6b91c2c0cd79` C13, C15: neglect of left-sided stimuli; 1 error in serial sevens is normal; NIHSS 6.
- Survey: NCCT "in watershed" (C11); lipid/HbA1c criterion removed (C9); omeprazole with clopidogrel
  (C7 required).

### ISCH-STR-P01 (man, 35, left PICA infarct, left V3 dissection, aspirin allergy, known PFO; R2 needs_changes)

- `ba9bdca8-cd98-41ee-aeea-27b28278c370` C9: remove both FVL entries (thrombophilia criterion and follow-up removed).
- `1fe2a211-73f6-44ca-98d1-8f7362737aaa` C15: correct the HINTS must; change the exam to a normal head impulse bilaterally so
  HINTS is central (normal head impulse, direction-changing nystagmus); no skew stays.
- `ec825b6a-492a-4dd0-9f31-cc49c4d966c9` C7: drug check required, names the aspirin allergy; must names clopidogrel or
  anticoagulation for 3 months.
- `7695631d-5db5-4085-a003-0e77d5c7ce0c` C13: NIHSS 2 (limb ataxia 2).
- Survey: monitor `holter_72h` (C2); PFO-closure literature orphan (C8); PFO is incidental: dissection
  explains the stroke, closure not indicated (state in key evidence); decision must (IVT only if
  disabling; PICA infarct NIHSS 2; extracranial dissection no contraindication); sumatriptan and
  ibuprofen stop.

### ISCH-STR-P02 (woman, 32, moyamoya disease, left frontal opercular infarct, OCP; R2 needs_changes)

- `10f6a890-04d8-46d7-9a85-671e833eb331` C4: decision rule: IVT is withheld once CTA shows moyamoya vasculopathy (safety not
  established, fragile collaterals); remove door-to-needle and pre-IVT BP musts; keep the
  prohibition, reworded to that reason.
- `50ffe53e-bbbe-4fe5-aa8d-32e639f43067` C11: MRI impression names the acute left frontal opercular infarct, the chronic
  watershed infarcts, basal ganglia flow voids and distal ICA/proximal MCA flow reduction.
- `ceadf1cd-583a-444b-bcd1-f8a5df548537` C13: remove "right hand motor".
- `bcb508a7-88a3-4926-a1f0-795499c213d0` C13: language 1.
- `027c14a1-2374-4814-9f24-7ac45ac71434` C6: aspirin; no anticoagulation; statin only if lipid indication (no lipid panel: do not
  mandate); neurosurgical revascularization referral.
- `daf0605e-b483-49f0-bebb-fd9d7f54bf5f` add family screening must: familial moyamoya is more frequent in East Asian
  populations; consider RNF213 testing and screening of first-degree relatives; the mother's
  intracranial haemorrhage at 45 is a red flag (key evidence).
- `bc4354fa-4ca0-4579-856c-1b5093dc08d2` add key evidence: chronic bilateral watershed infarcts mean some earlier episodes
  completed infarcts despite clinical recovery (silent infarction), which is typical of moyamoya.
- Survey: OCP (C7 required); echo "All values within normal limits" (C11); hypercoag criterion and
  orphan removed (C9); "in the clinically implicated territory" (C11).

### ISCH-STR-P03 (man, 41, septic embolism from viridans endocarditis, bicuspid aortic valve; R2 needs_changes)

- `0f2a9dec-c636-4b95-a5bc-ec7694b45a40` C13: NIHSS 7 (arm 2).
- `b331962d-0b79-4ffa-91f4-8e501dcc8bb1` add a TEE follow-up (`echo_type` TEE; perivalvular abscess assessment, vegetation
  size) and keep the TTE; criterion TTE required then TEE required; reconcile pearl and must: TEE is
  indicated with a positive TTE (ESC 2023).
- `0c5ef38d-d59a-4535-9fd0-8b2e8c3ad30a` PMH: amoxicillin was prescribed as a single pre-procedure dose that he did not take;
  remove the 7-day course and the bleeding rationale; add key evidence: prophylaxis is not routinely
  indicated for a bicuspid valve (AHA 2021 statement).
- `7d003b88-4040-4cdb-815a-694e2576d3d5` C4, C6: remove pre-IVT BP and door-to-needle musts; no antithrombotic; telemetry must
  reason is new conduction block signalling perivalvular abscess.
- Survey: duplicate WBC/RBC rows (C14); autoimmune panel orphan and ESR/CRP criterion removed (C9);
  monitor criterion `telemetry`.

### ISCH-STR-P04 (woman, 66, wake-up right M1 occlusion, EVT at 8 hours; R2 in_progress)

- `132ec224-5224-4bc8-9fa3-04d82c292e25` C1: CTA then CTP immediately after NCCT; echo and Holter after.
- `6d879e51-c6a6-4300-bed5-7f328173be9b` C3: state that the perfusion IVT limb applies only to patients not eligible for EVT.
- `db9768a7-2e38-4c21-99df-f5410eb9763c` C4, C5: pre-EVT BP at or below 185/110 (192/104 on arrival); remove the 140/90
  prohibition. The note text is truncated at source after "CONTRAINDICATED sets a fl"; treat it as the
  140/90 floor and log that.
- Survey: HPI leaks (C10); must names carotid duplex with no criterion: remove (CTA covered the
  neck); stale mock-server concern (C17); CTP required; Holter 48 h labelled 24 h (C2).

### ISCH-STR-P05 (man, 34, left PCA territory, PFO with large shunt, long-haul flight; R2 needs_changes)

- `7fc996b4-b5a9-41ba-ae38-13db4d6d7a4a` C9: keep the follow-up (heterozygous FVL), remove the initial panel.
- `2e2ccbff-383b-4aff-b2a0-d8c38f4c2ea1` add `order_body_imaging` study `lower_extremity_venous_duplex` (recommended) with a
  result showing left calf deep vein thrombosis (consistent with D-dimer 1820 and left calf
  tenderness); diagnosis line stays; remove the engineering parenthesis; must: anticoagulation for
  DVT, then PFO closure discussion (RoPE).
- `6ecd20c2-a281-4c6a-b84c-2712d167fc3c` C1, C2: event monitor criterion and follow-up removed, replaced by the must.
- `9e53616c-c655-45a9-830a-174e5b532b76` C10: remove the pre-emptive denial sentence from the HPI; migraine with aura lowered
  to low (DWI-positive infarct excludes it at assessment); rewrite the red herrings so their correct
  interpretation states what excludes migraine aura.
- Survey: decision must: wake-up (LKW 8 hours), FLAIR shows developing hyperintensity (WAKE-UP limb
  closed), distal P2-P3 occlusion is a medium vessel occlusion (no EVT); state that perfusion imaging
  was not pursued only if the sleep midpoint is beyond 9 hours, otherwise add CTP as in M01.

### ISCH-STR-RM01 (woman, 28, left ICA dissection, OCP, tonic hand posturing; R2 in_progress)

- `ef70fcc1-21c8-42f2-b3af-ab0442f7007c` C11: CTA impression opens with the left ICA dissection (intimal flap, mural haematoma,
  over 70 percent stenosis C2 to skull base).
- Survey: CTA contrast; hypercoag, autoimmune and connective-tissue follow-ups removed (C9);
  connective tissue assessment is clinical (exam already records habitus): key evidence; echo report
  (C11); OCP stop (C7 required); EEG optional criterion kept; decision must (LKW 2 hours, NIHSS 3:
  IVT only if disabling; extracranial dissection no contraindication).

### ISCH-STR-RM02 (woman, 74, left ICA dissection with jaw and facial pain, no infarct; R2 needs_changes)

- `ffd8459c-663e-497f-97eb-615736857ab1` relabel (the reviewer rules the label wrong): `accepted[0]` "Left internal carotid
  artery dissection presenting with jaw and facial pain, without completed cerebral infarct",
  `icd_codes[0]` I77.71 (as RM03); CENTRAL synonyms. Remove the reperfusion frame (C4).
- `4660dbc9-6c64-413a-a116-11c1316a9e7c` C4, C7: drug check required, placed after CTA: apixaban restarted 2 days ago, ketorolac
  added to apixaban and aspirin; must stops ketorolac and decides one antithrombotic (apixaban for AF
  also covers the dissection; stop aspirin).
- Survey: `interpret_labs` "temporal artery biopsy" follow-up removed (wrong tool, not indicated once
  the dissection is shown); GCA stays in the differential at low with ESR 34 and CRP 0.8 explained;
  temporal arteritis literature orphan (C8); empiric methylprednisolone given in the ED is history.

### ISCH-STR-RM03 (man, 41, left ICA dissection, painful Horner, no infarct; R2 needs_changes)

- `667da1af-ae3f-4593-9edb-b5cd733452da` C12: relabel the haematoma acute: "crescentic mural thickening, T1 isointense to
  mildly hyperintense on fat-saturated T1, consistent with acute intramural haematoma".
- `ec46ecc7-98f6-4540-bc11-8665d5cf3681` C11: CTA impression opens with the dissection.
- `73bf8a81-d1f7-478b-947f-8dd48075976c` C14: canonical replacement sentence.
- `1a96c82d-a137-47b8-a518-6e4183183ceb` add a teaching pearl on preserved facial sweating (section 1.2).
- `02d120ad-eac1-4b0e-8618-5b6eeec89880` rewrite the prohibition with the discriminators (persistent oculosympathetic signs
  between episodes, single event lasting hours, neck pain). Keep cluster headache low: the
  differential is the assessment-time view and imaging shows the dissection (log the "raise" option
  DECLINED with this reason).
- Survey: remove reperfusion musts (C4); sumatriptan and ibuprofen (C7 required); hypercoag and
  connective-tissue orphans (C8, C9); echo report (C11).

### ISCH-STR-RM04 (man, 34, right PICA infarct, right V3 to V4 dissection; R2 needs_changes)

- `d0aedb17-7635-4f4c-8147-4c2f2297d05b` keep the V4 extension (it explains absent PICA opacification); must: aspirin,
  anticoagulation avoided because of subarachnoid haemorrhage risk in intradural dissection; state that
  CADISS and the guideline recommendation cover extracranial dissection only; drug-check output
  removes the apixaban option; decision must notes the intradural extension weighs against IVT
  (uncertain benefit).
- `17db3372-9b52-4cf4-92c8-f669fd646b25` C12: add to the MRI impression and key evidence that the dissection began with the
  neck pain 3 days earlier, so a subacute haematoma with a hyperacute infarct is expected.
- `a220ccd8-21c0-4902-9469-5c12ffba0249` C13: NIHSS 2.

### ISCH-STR-RP01 (woman, 50, basilar occlusion, alcohol use disorder, stuttering course; R2 needs_changes)

- `97a9f686-9003-4e92-bf27-c87f7ac74397` C14: thiamine must and lab row.
- `55e9c9c7-878d-4ff6-bd00-0621498ac03c` C4: EVT must (basilar occlusion, NIHSS 14, PC-ASPECTS from the MRI must be 6 or more:
  compute and state it; if below 6, say EVT is not indicated and why).
- `19d1e303-10d4-4d11-8a30-e2b91f384b1f` C4, C10: the governing LKW is the previous evening (she improved at 10:30 but did not
  return to baseline), so IVT is outside the window; state it; the drug-check output names the window.
- Survey: ethanol differential (C17); CTA contrast; PFO on echo (state it is incidental or relevant);
  echo and monitoring required; "in basilar", "would mandate neurosurgical" (C11).

### ISCH-STR-RP02 (woman, 35, 18 weeks pregnant, right ICA dissection, prior TTP; R2 needs_changes)

- `68d979b1-bc30-41be-9954-a39b8d8935ca` move the occlusion to a right M2 superior division branch in MRI, MRA, CTA and the
  diagnosis description (consistent with the small insular-opercular infarct and NIHSS 2); remove
  the ACom explanation. Decision: no EVT (medium vessel, non-disabling), no IVT (non-disabling minor
  deficit).
- `4a90422f-ac91-4b35-8a84-ad0ab1a2d60c` dissection about 2 cm distal to the bifurcation, sparing the bulb, in every report and
  in `accepted[0]` description words if they say "ostium" (CENTRAL if the label text changes).
- `4d4b454f-5933-4867-bead-6b3b5cf41723` exam: double simultaneous stimulation tested, no extinction, line bisection normal.
- `15ecae28-8db2-4db2-a69d-e630736d8a7a` remove the CTA criterion and follow-up; MRI with MRA, venography and fat-saturated T1
  becomes required (variant exception, section 3.1).
- `60a69345-b25a-47eb-b8d7-86579246565a` C6: no statin in pregnancy; LMWH or low-dose aspirin.
- Survey: hypercoag follow-up merged with the ADAMTS13/haemolysis criterion (C9; ADAMTS13 16 percent
  one week ago with prior TTP: state whether TTP relapse is excluded by the platelet count and smear);
  echo report (C11); two literature outputs (C8); pregnancy guideline `[ESO_women_2022]`.

### ISCH-STR-RP03 (man, 36, right parietal infarct with HI-1 transformation, PFO, inactivated vaccine 48 hours before; R2 needs_changes)

- `00e99485-c30f-47a3-ae33-63d943d100dc` add `order_advanced_imaging` modality `MR_venography` (recommended) with a normal
  result; key evidence explains why the venous mechanism is set aside.
- `19ff066b-bde9-4228-aca4-f2520ebf9c47` C4: no IVT (HI-1 haemorrhagic transformation before treatment; unwitnessed onset with
  a 24-hour sensory prodrome); no EVT (no occlusion); remove door-to-needle and pre-IVT BP musts.
- `3451a4bc-64f1-4ebf-b177-7ec7d4e8c9ab` C15: "left lower facial weakness with forehead sparing and full eye closure".
- `7c967ef5-5b22-4f9e-b8ce-c4023ad5edc0` C9.
- `8b01e6c6-4870-4372-a193-d2c91130cbbd` C13: GCS 14 (E4 V4 M6).
- Survey: monitor criterion `event_monitor_30d` receives a 48-hour Holter (C2); vaccine literature
  orphan (C8); PFO closure discussion per AAN 2020 and RoPE.

### ISCH-STR-RP04 (woman, 43, left MCA superior division infarct, antiphospholipid syndrome; R2 needs_changes)

- `4332d93d-772e-4ff9-80ac-bfa07fa59bd5` C4, C7: the IVT decision is made on the raw aPTT 46 s with no anticoagulant exposure,
  normal INR and platelets 138; state the decision in the musts (IVT not withheld for an isolated
  prolonged aPTT without anticoagulant exposure, if within 4.5 hours and disabling); the
  antiphospholipid panel follows and explains the aPTT; the drug-check output no longer conditions on
  the LA result.
- `9685cde6-026d-4913-8268-02b1a5988109` C10: the antecedent is the visual aura (deficit began as the aura faded); align the
  additional findings.
- `7d4454af-b30c-4307-a09a-57b74156699d` C7: must "Stop sumatriptan permanently (contraindicated after ischaemic stroke and in
  antiphospholipid syndrome)".
- Survey: APL criterion required (C9); echo required (Libman-Sacks); "would mandate neurosurgical"
  (C11).

### ISCH-STR-RP05 (man, 47, left corona radiata lacune, CADASIL NOTCH3 p.Arg133Cys; R2 needs_changes)

- `58f1cd4c-d249-4a80-a550-fd1df59a9d75` keep migraine without aura and rewrite the red herring: migraine without aura is
  common and unspecific; migraine with aura is the typical early CADASIL symptom, so its absence makes
  the diagnosis harder, not easier; align teaching pearl 4.
- `0fd09831-7c22-4ede-a02b-8f7dd773bfdc` C11: remove PP1.
- Survey: sumatriptan (C7 required); two literature outputs (C8); stale mock-server concern (C17);
  decision must (LKW 2 hours, NIHSS 4: IVT if disabling; CADASIL is not a contraindication).

### ISCH-STR-RS01 (woman, 68, left M1 occlusion, AF off warfarin; R2 approved)

- `0bc84371-e88e-42f8-8db0-ec94169413e5` C4: EVT must (NIHSS 16, M1, within 6 hours).
- `d923cc86-8992-4e53-9234-5635dbccafce` C11: CTA impression opens with the left M1 occlusion.
- `dc0e0aee-915f-4ad2-941d-3f4c96c3eefd` C6: state CHA2DS2-VASc 7 and HAS-BLED from the record (gingival bleeding counts);
  DOAC timing by infarct size.
- `eea99434-9e3e-4f83-8aeb-315349b70086` C10, C11: add prior silent infarct to PMH ("old right basal ganglia lacune on imaging,
  no known prior stroke"); drop "chronic small vessel ischemic disease" from the impression unless
  white matter change is described.
- `22f804cf-b35c-4afd-8295-f118ccea8c2a` C14: rate control must.
- `3c9586d9-8055-487a-8356-f00cfaf365c6` C14: troponin must.
- Survey: FLAIR ">3 hours" at 2 h 52 (C12); IVT given (INR 1.0, warfarin stopped 6 months).

### ISCH-STR-RS02 (man, 70, left CCA to ICA dissection 6 weeks after aortic arch replacement; R2 needs_changes)

- `7eec1867-16a9-40a2-943c-b133ceb449d3` remove every "within 14 days" claim (42 days); decision: IVT withheld because of an
  actively dissected common carotid with an opacified false lumen arising near a six-week-old arch
  anastomosis, where aortic extension must first be excluded (aortic arch dissection contraindicates
  IVT). See open question 2.
- `212fe881-8bf4-422d-8971-03660d1dcb86` C10: crescendo TIA made explicit: teaching pearl, a prohibition "Do not manage
  recurrent transient deficits in a patient with a known carotid abnormality as outpatient
  observation", red herring retargeted; CTA key evidence says it confirms and characterises a lesion
  first seen 6 weeks ago.
- `4e5a5ed6-4e5c-4de3-b114-ba3bccf25371` replace the EVT must (no intracranial LVO) with: "Discuss the dissected segment with
  vascular surgery, cardiothoracic surgery and neurointervention: emergent endarterectomy within 48
  hours is not beneficial (§4.12, COR 3 No Benefit); endovascular stenting is considered if events
  recur despite antithrombotic therapy."
- Survey: FLAIR timing (C12); CTA contrast; echo TEE criterion stays (arch assessment).

### ISCH-STR-RS03 (man, 67, right PCA P2 occlusion, AF, oesophagectomy 3 weeks ago; R2 needs_changes)

- `8b0515f8-94d2-402a-8839-c4edfd7746fd` use the fetal-type right PCA: state it in the MRI and CTA impressions, and extend the
  MRI lesion to the posterior limb of the internal capsule or corona radiata so the mild left
  hemiparesis is explained.
- `3fea7d10-8433-4f09-9eda-2619da7a4293` C11: CTA impression opens with the P2 occlusion.
- `d703ff12-fc6e-4eec-8db9-3696f32098c5` C4: "Isolated P2 occlusion is a medium vessel occlusion with no graded thrombectomy
  indication, and NIHSS 8 does not meet the basilar criteria; thrombectomy is not indicated."
- `16f5be33-8615-45ee-bdc9-eea4046acf3c` C4: no IVT because LKW is over 10 hours, FLAIR is positive (WAKE-UP limb closed) and,
  for the perfusion limb, a fresh oesophageal anastomosis 21 days after resection of a GI malignancy
  makes systemic thrombolysis high risk; remove "on the cusp" and the 14-day reasoning; remove
  door-to-needle and pre-IVT BP musts.
- Survey: enoxaparin and apixaban (C7 required); rate control (C14); TEE avoided early after
  oesophagectomy (must kept).

### ISCH-STR-RS04 (woman, 33, 15 weeks pregnant, basilar and right V3 occlusion; R2 needs_changes)

- `cd879e2d-232b-47a4-a2e2-fc7105b696d3` LKW is the first symptom 18 hours before arrival (headache, dizziness, blurred vision
  as prodrome); the decline 6 hours before is progression. Decision: no IVT (beyond 4.5 hours); EVT for
  basilar occlusion within 24 hours of onset (NIHSS 22, compute PC-ASPECTS, at least 6). Fix HPI and
  every LKW mention.
- `2d805b4d-ad34-4f5b-af2b-de87672627bf` cite `[ESO_women_2022]` for every pregnancy decision; the 2026 AIS guideline covers
  only pre-eclampsia BP. Miller et al. Stroke 2026: open question 1.
- `c7026407-77c4-4054-97fe-e391b7e83fa9` C11: contrast true; impression opens with the basilar occlusion.
- Survey: drug check about alteplase in pregnancy becomes LMWH/aspirin in pregnancy (required);
  hypercoag criterion routed to its follow-up, initial exclusion panel removed (C9); literature
  titles (C8); avoid statin; MRI without gadolinium.

### ISCH-STR-RS05 (man, 63, right M1 near-occlusion on ICAD, aspirin plus clopidogrel; R2 approved)

- `c0233fc3-10d0-46d5-91ba-861dbe98095c` C4: BP-lowering must before IVT (188/104).
- `de5e529f-2a92-4c72-88b5-2317a5893d94` C13: NIHSS 12.
- Survey: FLAIR ">3 hours" at 38 minutes (C12); lipid/HbA1c follow-up removed (C9); drug check
  recommended (DAPT is not a contraindication; ACE inhibitor angioedema must exists).

### ISCH-STR-S01 (man, 72, left M1/ICA-T occlusion, AF not anticoagulated; R2 needs_changes)

- `c97b3f6e-9794-4ba2-ae83-a9adf1f87b01` C15: keep the left MCA label (imaging, ICD I63.412); flip the body to right-sided
  deficits: right hemiplegia, right facial droop, right sensory loss, left gaze deviation, global
  aphasia kept, left hemineglect replaced by right-sided inattention or removed (dominant lesion),
  tongue deviation to the right; chief complaint, HPI and EMS text too.
- `fdfaae93-a476-4a78-ba75-77775c97045f` C11, C12: FLAIR negative or faint at 2 h 47; NCCT and MRI consistent; remove the
  unsupported small vessel line.
- `f6628b06-b982-4450-b101-0378417b8d27` C13: NIHSS 22 (recount after the flip).
- Survey: troponin 0.07 (C14); EVT must explicit (C4); CTA impression and contrast (C11); laterality
  concern cleared (C17).

### ISCH-STR-S02 (woman, 68, left M1/M2 occlusion, AF off warfarin, CKD 3a, contrast allergy; R2 approved)

- `799ea64c-2db4-41ee-b333-47fec8c75b2e` C16.
- Survey: anion gap -4 (C14); FLAIR "subacute" at 2 h 22 (C12); HPI leak (C10); CTA impression and
  contrast (C11); BP 206/105 lowering before IVT (C4); EVT must explicit; troponin (C14); remove "If no
  tPA, permissive hypertension up to ~220/110" (replaced by C5 text only if no reperfusion).

### ISCH-STR-S03 (man, 55, left MCA M1 occlusion, AF, warfarin stopped 3 weeks ago, HFrEF, CKD; R2 needs_changes)

- `d3d1bb91-dfc2-4522-9c4e-d16366e45dda` C10: 09:00 anchor kept, caller becomes his wife (or brother); the mother's death from
  stroke stays in the family history.
- `20b2416f-f0b0-4392-b596-48a725e636b6` C15: left gaze deviation.
- `0a65085d-a1e9-4f73-90ea-47405aec24d8` C16.
- Survey: anion gap 26 and Hct (C14); warfarin listed as current: mark discontinued 3 weeks ago; INR
  1.2 allows IVT (C7 required); EVT must; troponin 0.08 (C14); rate control; CTA impression and
  contrast (C11).

### ISCH-STR-S04 (woman, 78, left MCA occlusion, AF, warfarin stopped for epistaxis; R2 needs_changes)

- `5f9d3088-245e-4621-9be3-27a515be9e0a` C15: left gaze deviation in EMS note and exam.
- `3f611291-2e78-48d2-82a3-183c423e4455` C4: BP-lowering must before IVT (196/111).
- `ec9af643-86d5-4252-a25e-43b65e25c514` C7: drug-check output lists epistaxis, age 78, HAS-BLED; contraindications not empty;
  DOAC timing by infarct size (classify the 4.8 cm infarct by the ELAN imaging categories).
- Survey: anion gap 19 (C14); FLAIR timing (C12); CTA impression (C11); EVT must; troponin (C14);
  rate control.

### ISCH-STR-S05 (woman, 74, right M1 occlusion, AF; R2 approved)

- `c9b7c467-714d-4750-9306-097c63dbce7a` C12: FLAIR faint or absent at 2 h 58.
- `9802d420-6264-4e63-80cb-54241623d298` C13: NIHSS 13 (extinction 2 under item 11, arms and legs 3, sensory 1).
- Survey: HPI leak (C10); BP 188/104 lowering before IVT (C4); EVT must explicit; lisinopril
  angioedema monitoring.

### ISCH-STR-S06 (man, 62, left internal capsule lacune, pure motor; not reviewed, no notes)

- Survey only: HPI leak "well within the IV thrombolysis window" (C10); must "DWI MRI is required to
  confirm the diagnosis" becomes "MRI DWI may confirm the lacune after the reperfusion decision; do not
  delay IV thrombolysis for MRI" (MRI optional per the July review); 140/90 prohibition (C5);
  secondary-prevention labs follow-up removed (C9); stale mock-server concern (C17); decision must:
  IVT for a disabling deficit at 33 minutes (NIHSS 5), no EVT (no LVO); lisinopril angioedema
  monitoring; drug check recommended. Do not churn correct prose: this case was never reviewed.

---

## 5. CENTRAL requests (outside the case files)

1. Criteria pack `dataset-generation/criteria_packs/ISCH-STR.md`: allow-list `[AHA_ASA_Stroke_2026]`,
   `[AHA_ASA_2021_secondary]`, `[ESO_women_2022]`, `[ESC_endocarditis_2023]`,
   `[AHA_IE_prophylaxis_2021]`, `[AAN_PFO_2020]`, `[Kattah_HINTS_2009]` (references in section 1.1);
   mark `[AHA_ASA_2019]` and `[AHA_ASA_2014]` superseded; align the literature and drug-check tiers
   with rulings 5 and 6; replace the pitfall "avoid lowering BP aggressively before tPA unless
   >185/110" with the section 1.2 BP rules.
2. Review UI (M02 eae4a343): show the initial work-up as numbered steps in criterion order.
3. Synonyms: RM02 relabelled to I77.71 (ICA dissection without infarct) needs its synonym list
   regenerated (it carries the I63 stroke synonyms); RP02 too if "ostium" leaves `accepted[0]`.
4. Fallback library: confirm normal reports for `MR_venography`, `CT_perfusion` and
   `lower_extremity_venous_duplex`.
5. Generator: CTA impressions omit the principal finding (9 of 30) and CTA `contrast_used` is false
   (16); the NCCT template writes management text; the echo template prints "Abnormal values: ...
   (H)" and flags LVEF 50 to 55 percent; Holter `monitor_type` ignores `duration_hours`. R2 asks for
   a generator fix (d923cc86).
6. `perfect_agent.py` copies only the first alternative, so it misses alternatives (for example
   `holter_48h`) with no matching follow-up; consider checking every alternative.
7. `condition_tool_guidance.yaml`: no change; note the two departures from the July answers (P04 CTP
   required, RP02 MRI required in pregnancy).

## 6. Open questions for Andrea

1. RS04 note 2d805b4d cites "Miller et al, Stroke 2026;57(4), doi 10.1161/STR.0000000000000514" as an
   AHA/ASA statement on stroke in pregnancy. I could not verify it; the plan uses the ESO 2022
   guideline (Kremer C et al.), which the reviewer also offered. Add the Miller key if you can confirm
   the reference.
2. RS02: IVT is withheld for the dissected common carotid near a six-week-old arch anastomosis, on the
   reviewer's reasoning. The guideline itself only names aortic arch dissection; please confirm with
   R2 that a CCA dissection 7 cm from the graft is treated as a contraindication here.
3. RM02 is relabelled from ischaemic stroke to ICA dissection without infarct (I77.71), as the reviewer
   ruled. The alternative is to keep the stroke label and add a clinically silent DWI lesion. Two of 30
   ISCH cases (RM02, RM03) would then contain no infarct; confirm that is acceptable for the condition.
4. M01, M02 (and P05 if its sleep midpoint qualifies): the plan adds CTP results that fail EXTEND
   criteria so the existing "no IVT" story stands. If you prefer a case where perfusion qualifies the
   patient for IVT, that is a story change for one of them.
5. `max_additional_actions` set to 1 in all 30 cases (ALS chose 0). Confirm the allowance.
6. RP02: moving the occlusion from M1 to M2 is the less invasive of the reviewer's two options; it also
   removes thrombectomy from the case. Confirm.
