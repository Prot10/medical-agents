# Criteria pack: Ischemic stroke

**ICD-10:** I63.x (by mechanism and territory)
**Condition enum:** `NeurologicalCondition.ISCHEMIC_STROKE`
**Case ID prefix:** `ISCH-STR`

Updated 24 Oct 2026 to the rulings of the October 2026 physician-review round
(`data/review/round-2026-10/plans/ISCH-STR.md`, `ISCH-STR-summary.md`).

---

## 1. Diagnostic criteria

AHA/ASA 2026 early management of acute ischaemic stroke governs acute management (imaging, IVT,
EVT, BP, labs, stroke unit, early antithrombotic) [AHA_ASA_Stroke_2026]; the 2021 AHA/ASA secondary
prevention guideline governs antithrombotic choice by mechanism, carotid timing, AF, statin,
dissection and PFO [AHA_ASA_2021_secondary]. Cite a section or class only where the reviewer gave it
(§4.3, §4.6.3, §4.7, §4.7.2, §4.7.3, §4.12, §3.3, Early Secondary Prevention rec 7); number nothing
else from memory.

Clinical syndrome of acute focal neurologic deficit + neuroimaging evidence of acute ischaemia (acute
ischaemic stroke = symptoms >24h OR <24h with imaging confirmation; TIA = symptoms resolved AND
imaging negative for acute infarct). NIHSS used for severity and treatment decisions. TOAST
classification by mechanism: large-artery atherosclerosis, cardioembolism, small-vessel occlusion,
stroke of other determined etiology, undetermined (cryptogenic) [Adams_1993_TOAST].

**Last known well (LKW)** is the last time the patient was seen at baseline. It is at or before the
first symptom, never after it. A fluctuating course resets LKW only if the patient returned fully to
baseline.

**IV thrombolysis (IVT)** [AHA_ASA_Stroke_2026]:
- Standard window within 4.5 hours of LKW: alteplase 0.9 mg/kg (maximum 90 mg) or tenecteplase 0.25 mg/kg (maximum 25 mg); door-to-needle under 60 minutes
- Extended window, two separate limbs (§4.6.3, COR 2a): (a) unknown onset with a DWI-positive, FLAIR-negative lesion (WAKE-UP); (b) wake-up stroke within 9 hours of the midpoint of sleep, or 4.5 to 9 hours from LKW, with salvageable penumbra on automated perfusion imaging by EXTEND criteria (penumbra-to-core ratio above 1.2, mismatch volume above 10 mL, core below 70 mL), only in patients not eligible for thrombectomy. The 1.8 ratio with mismatch above 15 mL belongs to TIMELESS and TRACE-III; never use it for limb (b). Every wake-up or unknown-onset case addresses both limbs
- Blocking findings: any intracranial haemorrhage, including haemorrhagic transformation already present; infective endocarditis; a DOAC taken within 48 hours (a normal INR does not exclude its effect); INR above 1.7 on a vitamin K antagonist; known or suspected aortic arch dissection. A non-disabling minor deficit is not an indication for IVT (antiplatelet therapy instead)
- Extracranial cervical artery dissection is not a contraindication; intradural (intracranial) dissection carries subarachnoid haemorrhage risk and the benefit is uncertain
- Only glucose must be known before IVT; CBC and coagulation are awaited only if an anticoagulant, coagulopathy or thrombocytopenia is suspected. ECG and troponin do not delay reperfusion; CTA does not wait for creatinine

**Thrombectomy (EVT)** [AHA_ASA_Stroke_2026]:
- Anterior circulation LVO (ICA or M1) within 6 hours: NIHSS 6 or more, pre-stroke mRS 0 to 1, ASPECTS 3 to 10: COR 1 (§4.7). Give IVT first when eligible; do not wait to see its effect
- 6 to 24 hours: DAWN or DEFUSE 3 selection (clinical-core or perfusion mismatch) [DAWN_2018] [DEFUSE3_2018]
- Basilar artery occlusion within 24 hours of symptom onset: NIHSS 10 or more, pre-stroke mRS 0 to 1, PC-ASPECTS 6 or more: COR 1 (§4.7.3)
- Isolated P2, M2 distal or M3 occlusions are distal or medium vessel occlusions with no graded EVT indication (ESCAPE-MeVO and DISTAL, NEJM 2025, showed no benefit)
- Surgery is not an absolute contraindication to EVT

## 2. Standard workup hierarchy

Canonical criterion order (the review app reads it as the work-up sequence): NCCT, core labs, ECG,
CTA, (MRI), (CT perfusion), case-specific diagnostic core, drug-interaction check where it informs
reperfusion, echocardiogram, inpatient cardiac monitoring, aetiological labs, drug-interaction check
where it informs secondary prevention, literature last.

**Required (acute phase, all cases):**
- `order_ct_scan` (`contrast: false`): non-contrast CT head; excludes haemorrhage; first imaging in any stroke alert. Normal impression: "1. No acute intracranial haemorrhage. 2. No established infarct, no hyperdense vessel sign and no mass lesion. ASPECTS 10." (posterior circulation: PC-ASPECTS or none); never management text [AHA_ASA_Stroke_2026]
- `interpret_labs` core (glucose, CBC, coagulation, creatinine, troponin); lipids and HbA1c are part of the admission bloods, not separate criteria. Troponin is a COR 1 baseline that must not delay reperfusion (§3.3); an elevated value is acted on [AHA_ASA_Stroke_2026]
- `analyze_ecg` (12-lead): AF or other rhythm cause [AHA_ASA_Stroke_2026]
- `order_ct_scan` (`angiography: true`, contrast): CTA head and neck for LVO and dissection; `contrast_used` true and the impression opens with the principal finding. A mild prior contrast reaction and CKD stage 3a do not justify delaying vessel imaging (premedication only if it causes no delay). In pregnancy where MRA replaces CTA, MRI with MRA is required instead [AHA_ASA_Stroke_2026]

**Per case:**
- `order_advanced_imaging` (`modality: CT_perfusion`): **recommended** for the perfusion limb in wake-up stroke without LVO; **required** where it selects EVT in the late window [AHA_ASA_Stroke_2026] [DEFUSE3_2018]
- `analyze_brain_mri` (DWI): optional in most cases; confirms infarct and embolic patterns; not first-line in the acute setting unless the CT is equivocal; required where MRA replaces CTA (pregnancy). No gadolinium in pregnancy [AHA_ASA_Stroke_2026] [ESO_women_2022]
- `order_echocardiogram`: **required** where a cardiac source is the question (cardioembolic or cryptogenic pattern, PFO in the young, suspected endocarditis with TTE then TEE); **recommended** elsewhere. TEE is recommended in suspected IE with a positive TTE (ESC 2023) [AHA_ASA_Stroke_2026] [ESC_endocarditis_2023]
- `order_cardiac_monitoring` (`holter_24h` / `holter_48h` / `telemetry`): inpatient monitoring recorded on the stroke unit after admission, its type matching its duration (no `holter_72h`); **required** in embolic-pattern and cryptogenic cases, **recommended** elsewhere. Prolonged outpatient monitoring (30-day event monitor, implantable loop recorder) is a must after discharge, not a stored result [Sanna_2014]
- Aetiological labs (thrombophilia, antiphospholipid, ADAMTS13, young-stroke screen): only where the mechanism calls for them (young cryptogenic or PFO, antiphospholipid syndrome, pregnancy, prior TTP, young-stroke screen); **recommended**, required where the diagnosis rests on them; not indicated in atherosclerotic, cardioembolic, small-vessel or dissection mechanisms
- `check_drug_interactions`: **required only with a concrete issue that changes management**, named in the output (e.g. DOAC within 48 hours, DOAC dosing with CKD, clopidogrel with omeprazole, aspirin allergy, sumatriptan or combined oral contraceptive to stop, NSAID with antithrombotic, pregnancy, suspected IE); **recommended** otherwise (ruling 6). The output lists the patient's actual medicines and allergies; it is placed immediately before the decision it informs

**Optional:**
- `search_medical_literature`: at most one criterion, last in the order; its output gives general, correctly cited evidence, never the case's expected text (ruling 5). Nothing required or recommended depends on it
- `order_advanced_imaging` (`modality: MR_angiography`): alternative when CTA is not used (pregnancy); carotid duplex after CTA is an overlapping vascular study (covered by `max_additional_actions` 1)
- `order_advanced_imaging` (`modality: transcranial_doppler`): for microemboli detection, sickle cell stroke risk

**Management is a must, never a tool call** (ruling 4). Every case has one LKW must ("Establish last
known well (<time>, <h> hours before arrival) and the NIHSS (<n>).") and one decision must ("IV
thrombolysis: <give / do not give> because <reason>. Thrombectomy: <proceed / not indicated> because
<reason>."), except cases with no deficit and no infarct. Door-to-needle and pre-IVT BP musts only
where IVT is given.

Secondary prevention by mechanism (musts) [AHA_ASA_2021_secondary]:
- **AF:** a DOAC in preference to warfarin; start within 48 hours for minor or moderate infarcts and on day 6 to 7 for major infarcts once haemorrhage is excluded (ELAN, NEJM 2023; OPTIMAS, Lancet 2024); state CHA2DS2-VASc and HAS-BLED from the record; no heparin bridging. Apixaban 2.5 mg twice daily only with two of: age 80 or more, weight 60 kg or less, creatinine 1.5 mg/dL or more
- **Minor non-cardioembolic stroke (NIHSS 3 or less) or high-risk TIA:** aspirin plus clopidogrel for 21 days, then single antiplatelet (CHANCE, POINT); otherwise single antiplatelet
- **Statin:** high-intensity, LDL target below 70 mg/dL, for an atherosclerotic mechanism; not in pregnancy, not mandated for a non-atherosclerotic mechanism without a lipid indication
- **Carotid:** emergent endarterectomy within 48 hours for AIS from high-grade stenosis without intracranial occlusion is COR 3 No Benefit (§4.12); revascularization of a symptomatic 70 to 99 percent stenosis between 2 days and 2 weeks (COR 1); 50 to 69 percent depends on patient factors
- **Extracranial carotid or vertebral dissection:** antiplatelet or anticoagulant for at least 3 months (COR 2a, LOE B-R, Early Secondary Prevention rec 7; CADISS and TREAT-CAD enrolled extracranial dissection only). Intradural extension: antiplatelet, avoid anticoagulation; the trial evidence does not cover it
- **Small vessel:** antiplatelet, statin per LDL, long-term BP below 130/80 mmHg
- **Moyamoya:** aspirin, no anticoagulation, statin only on a lipid indication, neurosurgical revascularization referral, avoid hypotension, dehydration and hyperventilation
- **Infective endocarditis:** no anticoagulation or antiplatelet started for the stroke; exclude mycotic aneurysm; endocarditis prophylaxis is one pre-procedure dose, not a course, and a bicuspid aortic valve is not an indication [ESC_endocarditis_2023] [AHA_IE_prophylaxis_2021]
- **PFO:** antiplatelet; closure discussion with the RoPE score [AAN_PFO_2020]
- **Antiphospholipid syndrome:** warfarin INR 2 to 3 once confirmed at 12 weeks; no DOAC
- **Pregnancy:** LMWH or low-dose aspirin; no warfarin; no statin; MRI without gadolinium preferred; CT and iodinated contrast are not withheld when they decide reperfusion [ESO_women_2022]
- Sumatriptan is contraindicated after ischaemic stroke and in antiphospholipid syndrome [Sumatriptan_SmPC]; ACE inhibitor with alteplase: watch for orolingual angioedema
- Stroke unit: "Admit to a stroke unit with continuous cardiac monitoring (telemetry) for at least the first 24 hours."; sinus rhythm with an embolic or cryptogenic pattern: prolonged ambulatory rhythm monitoring after discharge

## 3. Tools that are typically USELESS

The three waste avoided actions used across the condition, citing `[AHA_ASA_Stroke_2026]`:

- `analyze_eeg`: not part of stroke workup unless post-stroke seizure (optional where the case raises a seizure mimic)
- `analyze_csf`: no role unless SAH or vasculitis on differential
- `order_specialized_test` (`emg_ncs`; most types): not part of routine acute workup; only neuropsych in chronic phase

## 4. Tools that are HARMFUL / contraindicated

- `analyze_brain_mri` with `contrast: true` in pregnancy: gadolinium is avoided (avoided action, severity `contraindicated`) [ESO_women_2022]
- IV thrombolysis with a blocking finding (section 1): a treatment decision, handled by prohibitions and the decision must, not a tool harm
- A mild prior contrast reaction or CKD stage 3a is **not** a reason to withhold CTA in a reperfusion candidate

## 5. Sequence constraints

All `soft` (no reverse order is unsafe in itself); no `hard` constraint:

- `order_ct_scan` (non-contrast) → `order_ct_scan` (CTA): "Non-contrast CT excludes haemorrhage before vessel imaging and the reperfusion decision." [AHA_ASA_Stroke_2026]
- CTA → `order_echocardiogram` and CTA → `order_cardiac_monitoring`: "Vessel imaging decides reperfusion; cardiac aetiology is studied after the acute decisions." [AHA_ASA_Stroke_2026]
- CTA → `order_advanced_imaging` (`CT_perfusion`) where CTP exists
- Where MRA replaces CTA (pregnancy), the MRI takes the CTA's place in these constraints
- No constraint involves the literature or drug-interaction criteria

Stop rule: `required_before_assessment` = every required criterion; `max_additional_actions` 1.

## 6. Subtype variations

- **M (mild):** minor stroke (NIHSS <5), small vessel or wake-up; standard acute workup; both extended-window limbs addressed in wake-up cases (CTP recommended)
- **S (standard):** moderate stroke, anterior circulation, identifiable mechanism; standard acute + secondary workup
- **P (progressive / severe):** large vessel occlusion, NIHSS ≥6, candidate for thrombectomy; emergent CTA + thrombectomy pathway (CTP required where it selects late-window EVT); comprehensive secondary workup post-acute
- **R (reverse / mimic):** stroke mimics (hypoglycaemia, complicated migraine, post-ictal Todd's paralysis, conversion/FND, MS relapse, brain tumour with stroke-like onset) and dissection without infarct; workup adds MRI, targeted labs, EEG if seizure suspected; no reperfusion musts where there is no deficit and no infarct

## 7. Common red-herring categories and pitfalls

- **Normal initial CT:** early ischaemic changes may be subtle; does NOT exclude stroke in a symptomatic patient
- **Resolved symptoms:** TIA still requires the same workup; high short-term recurrence risk (ABCD2)
- **Hypertension:** common in acute stroke. Before IVT: below 185/110 mmHg (COR 1); for 24 hours after IVT: below 180/105 mmHg. Before EVT: at or below 185/110 mmHg (COR 2a); after successful recanalization, do not target systolic below 140 mmHg (ENCHANTED2/MT, OPTIMAL-BP). No IVT and no EVT, BP below 220/120 mmHg, no comorbid indication: starting or restarting antihypertensives in the first 48 to 72 hours does not prevent death or dependency (§4.3 rec 4, COR 3 No Benefit, LOE A). There is no "140/90 floor" in the guideline
- **Atrial fibrillation history:** does NOT prove AF is the cause; lacunar infarct may be unrelated
- **Migraine with aura:** can mimic; new-onset aura in elderly must have stroke workup
- **Imaging timing:** a FLAIR description agrees with LKW (under 4.5 hours: DWI-FLAIR mismatch or faint FLAIR change); dissection intramural haematoma is T1 isointense in the first hours, T1-bright from about day 2 to 3; spontaneous cervical ICA dissection starts 2 to 3 cm distal to the bifurcation, sparing the bulb; carotid-dissection Horner is postganglionic and spares facial sweating
- **Examination and scales:** NIHSS items and ranges as the official scale (no hand, gait or truncal ataxia item; nystagmus, saccadic pursuit and diplopia do not score on gaze; ataxia 0 when testing is limited by weakness); GCS alert E4, confused V4, obeys M6, localises M5; a destructive hemispheric lesion deviates the eyes toward the lesion; UMN facial palsy spares the forehead and eye closure; neglect follows a non-dominant hemisphere lesion and is of the left side; HINTS central pattern is a normal head impulse, direction-changing nystagmus, skew deviation [Kattah_HINTS_2009]
- **Reports:** CTA `contrast_used` true and the principal finding first; echo impressions are real reports (never "Abnormal values: X (H)"; LVEF 50 to 55 percent is not flagged); every side agrees with the lesion side and with handedness

## 8. Allowed citations

- `[AHA_ASA_Stroke_2026]`: Prabhakaran S, Gonzalez NR, Zachrison KS, et al. AHA/ASA guideline for the early management of patients with acute ischemic stroke. Stroke 2026
- `[AHA_ASA_2021_secondary]`: Kleindorfer DO et al. 2021 guideline for the prevention of stroke in patients with stroke and transient ischemic attack. Stroke 2021;52:e364-e467
- `[DAWN_2018]`: Nogueira RG et al. Thrombectomy 6-24 hours after stroke with a mismatch between deficit and infarct. NEJM 2018;378:11-21
- `[DEFUSE3_2018]`: Albers GW et al. Thrombectomy for stroke at 6 to 16 hours with selection by perfusion imaging. NEJM 2018;378:708-718
- `[Sanna_2014]`: Sanna T et al. Cryptogenic stroke and underlying atrial fibrillation. NEJM 2014;370:2478-2486
- `[Adams_1993_TOAST]`: Adams HP et al. Classification of subtype of acute ischemic stroke: TOAST. Stroke 1993;24:35-41
- `[ESO_women_2022]`: Kremer C et al. European Stroke Organisation guideline on stroke in women. Eur Stroke J 2022;7(2), doi 10.1177/23969873221078696
- `[ESC_endocarditis_2023]`: Delgado V et al. 2023 ESC Guidelines for the management of endocarditis. Eur Heart J 2023;44:3948-4042
- `[AHA_IE_prophylaxis_2021]`: Wilson WR et al. AHA scientific statement on prevention of viridans group streptococcal infective endocarditis. Circulation 2021;143:e963-e978
- `[AAN_PFO_2020]`: Messe SR et al. AAN practice advisory update: patent foramen ovale and secondary stroke prevention. Neurology 2020;94:876-885
- `[Kattah_HINTS_2009]`: Kattah JC et al. HINTS to diagnose stroke in the acute vestibular syndrome. Stroke 2009;40:3504-3510
- `[EAN_monogenic_SVD_2020]`: Mancuso M et al. Monogenic cerebral small-vessel diseases: diagnosis and therapy. EAN consensus. Eur J Neurol 2020;27:909-927 (used in RP05)
- `[Sumatriptan_SmPC]`: Sumatriptan Summary of Product Characteristics (contraindication after stroke or TIA; used in RP05)
- `[Chabriat_2009]`: Chabriat H et al. CADASIL. Lancet Neurol 2009;8:643-653 (RP05 literature output)
- `[OSullivan_2001]`: O'Sullivan M et al. MRI hyperintensities of the temporal lobe and external capsule in patients with CADASIL. Neurology 2001;56:628-634 (RP05 literature output)
- `[EULAR_APS_2019]`: EULAR recommendations for the management of antiphospholipid syndrome in adults, 2019 (proposed key, RP04; reference to confirm)
- `[ISTH_TTP_2020]`: ISTH 2020 guideline on TTP (proposed key, RP02; key name and reference to confirm)

**Superseded (do not cite; kept for traceability):**
- `[AHA_ASA_2019]`: Powers WJ et al. Guidelines for the early management of patients with acute ischemic stroke: 2019 update. Stroke 2019;50:e344-e418. Superseded by `[AHA_ASA_Stroke_2026]`
- `[AHA_ASA_2014]`: Kernan WN et al. Guidelines for the prevention of stroke in patients with stroke and TIA. Stroke 2014;45:2160-2236. Superseded by `[AHA_ASA_2021_secondary]`
