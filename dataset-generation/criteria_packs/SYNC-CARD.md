# Criteria pack: Cardiac syncope

**ICD-10:** R55 (syncope unspecified), I49.x (cardiac arrhythmia), I20-I25 (CAD)
**Condition enum:** `NeurologicalCondition.SYNCOPE_CARDIAC`
**Case ID prefix:** `SYNC-CARD`

---

## 1. Diagnostic criteria

ESC 2018 guidelines + AHA/ACC/HRS 2017 guideline for evaluation of syncope.
**Cardiac syncope** = transient global hypoperfusion of cerebral cortex
caused by cardiac origin: arrhythmic (sustained VT, sick sinus syndrome,
high-grade AV block, supraventricular tachycardia, pacemaker malfunction,
Brugada, long QT) or structural (aortic stenosis, HOCM, cardiac tamponade,
PE, pulmonary hypertension, atrial myxoma, ACS with right ventricular MI).
High-risk features: syncope during exertion, supine, with palpitations or
chest pain; new ECG abnormalities (Q waves, LBBB, prolonged QT, Brugada);
known structural heart disease; family history of sudden cardiac death.
**EGSYS score** + ROSE rule for risk stratification.

## 2. Standard workup hierarchy

**Required:**
- `analyze_ecg` (12-lead) — arrhythmia, conduction abnormalities, ischemia, prolonged QT, Brugada pattern, pre-excitation; FIRST test in any syncope [ESC_2018]
- `interpret_labs` (CBC, BMP, glucose, troponin, BNP if HF on differential, beta-hCG; consider drug screen) — exclude metabolic, anemia, cardiac ischemia
- `order_echocardiogram` (`echo_type: TTE`) — structural heart disease (LV function, valves, wall motion, pulmonary pressures, pericardial effusion, masses); high-yield in cardiac syncope [ESC_2018]
- `order_cardiac_monitoring` (initial: telemetry inpatient; outpatient: holter_24h, then event monitor, then implantable loop recorder if infrequent) — arrhythmia capture; choice depends on event frequency [Locati_2014]
- `search_medical_literature` — confirm risk stratification, indications for ICD/pacemaker
- `check_drug_interactions` — review QT-prolonging medications, AV-nodal blockers, diuretics, antihypertensives, antiarrhythmics

**Recommended:**
- `order_specialized_test` (`test_type: tilt_table`) — only if neurally-mediated syncope vs cardiac is uncertain; NOT to confirm cardiac syncope
- `order_specialized_test` (`test_type: exercise_stress_test`) — exercise-induced syncope, suspected exercise-triggered arrhythmia
- `order_advanced_imaging` (`modality: MR_angiography`) — if vascular (subclavian steal, vertebrobasilar TIA) on differential
- Specialist referral *(clinical action — `tool_name: null`, no tool call)* — cardiology / electrophysiology referral

**Optional:**
- `analyze_brain_mri` — only if seizure or stroke on differential; routine imaging not indicated in typical syncope
- `analyze_eeg` — only when seizure on differential

## 3. Tools that are typically USELESS

- `analyze_brain_mri` — for typical cardiac syncope, low yield; ACEP, AHA guidelines explicitly state not routinely needed
- `analyze_csf` — no role
- `order_ct_scan` — only if head injury sustained or trauma during syncope; routine CT for syncope NOT indicated
- `order_advanced_imaging` (most other modalities) — none routinely indicated
- `order_specialized_test` (`emg_ncs / muscle_biopsy / nerve_biopsy / etc.`) — none indicated

## 4. Tools that are HARMFUL / contraindicated

- `order_specialized_test` (`test_type: tilt_table`) — relative contraindication in known severe coronary artery disease, severe aortic stenosis, severe carotid stenosis, recent stroke

## 5. Sequence constraints

- `analyze_ecg` → discharge or admission (`hard`): ECG MUST be performed before disposition decision; abnormal ECG mandates admission
- `interpret_labs` (troponin) → cardiac monitoring decision (`hard`): troponin assessment for ACS
- `order_echocardiogram` → high-risk discharge (`soft`): document structural disease absence before discharge of high-risk syncope

## 6. Subtype variations

- **M (mild):** brief syncope with rapid recovery, no high-risk features, single event; standard outpatient workup
- **S (standard):** typical cardiac syncope with clear high-risk feature (exertional, abnormal ECG, structural heart disease known); standard workup with cardiology consultation
- **P (progressive / severe):** sustained ventricular tachycardia documented, high-degree AV block, severe aortic stenosis with syncope, HOCM with syncope; urgent treatment (ICD, pacemaker, valve replacement, septal reduction); admission required
- **R (reverse / mimic):** vasovagal syncope (most common syncope, prodromal symptoms, post-prandial / venipuncture / emotional / orthostatic, normal cardiac workup), orthostatic syncope (postural drop in BP, dehydration / medications / autonomic neuropathy), seizure (post-ictal confusion, witnessed convulsive activity, tongue bite — but convulsive syncope causes brief jerks too), cataplexy, drug-induced, hypoglycemia, PE (with syncope at presentation), aortic dissection, pulmonary hypertension; workup adds tilt-table for vasovagal/orthostatic, EEG for seizure, glucose, D-dimer/CTPA if PE suspected

## 7. Common red-herring categories

- **Witness reports "convulsive activity"** — convulsive syncope from cerebral hypoperfusion can mimic seizure; ECG and post-ictal state distinguish
- **Normal ECG** — does NOT exclude paroxysmal arrhythmia; intermittent monitoring needed
- **Negative initial 24h Holter** — sensitivity low for paroxysmal events; event monitor or loop recorder needed
- **"Just vasovagal" in older adult** — atypical for first syncope in elderly; expand workup
- **Tilt-table positive** — supports vasovagal contribution but doesn't exclude concurrent cardiac cause
- **Exertional syncope** — RED FLAG; always cardiac workup including echo, exercise testing

## 8. Allowed citations

- `[ESC_2018]` — Brignole M et al. 2018 ESC Guidelines for the diagnosis and management of syncope. Eur Heart J 2018;39:1883-1948
- `[ACC_AHA_HRS_2017]` — Shen WK et al. 2017 ACC/AHA/HRS guideline for the evaluation and management of patients with syncope. J Am Coll Cardiol 2017;70:e39-e110
- `[Locati_2014]` — Locati ET et al. External prolonged electrocardiographic monitoring in unexplained syncope. Heart 2016;102:1772-1778
- `[EGSYS_2008]` — Del Rosso A et al. Clinical predictors of cardiac syncope at initial evaluation in patients referred urgently to a general hospital: the EGSYS score. Heart 2008;94:1620-1626
- `[ROSE_2010]` — Reed MJ et al. The ROSE (Risk Stratification of Syncope in the Emergency Department) study. J Am Coll Cardiol 2010;55:713-721
- `[Strickberger_2006]` — Strickberger SA et al. AHA/ACCF Scientific Statement on the Evaluation of Syncope. Circulation 2006;113:316-327
