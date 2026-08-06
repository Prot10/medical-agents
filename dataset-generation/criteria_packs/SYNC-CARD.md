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

> **Clinical tool review, July 2026 (Reviewer 2).** Five annotations on this panel, all
> applied: cardiac monitoring raised to REQUIRED, laboratory studies lowered to OPTIONAL and
> narrowed to targeted assays, EEG and brain MRI retained but re-scoped to the two
> differential-diagnosis indications the guideline supports, and a new OPTIONAL item for
> second-line cardiac imaging. The reviewer weighted its own evidence explicitly: the
> escalation to CT or MR rests on advisory guideline text, whereas coronary angiography
> carries a Class IIa recommendation.

**Required:**
- `analyze_ecg` (12-lead) — rhythm, rate, PR/QRS/QT-QTc, axis, conduction and repolarization. Diagnostic at initial evaluation: sinus bradycardia <40 bpm or pauses >3 s awake and untrained, Mobitz II or third-degree AV block, alternating LBBB/RBBB, VT or rapid paroxysmal SVT, non-sustained polymorphic VT with long or short QT, device malfunction with pauses. Suggestive only, requiring further testing: bifascicular block, QRS ≥0.12 s, pre-excitation, type 1 Brugada morphology, early repolarization, negative T waves or epsilon waves in the right precordial leads, LVH. A normal ECG does not exclude cardiac syncope. FIRST test in any syncope [ESC_2018]
- `order_echocardiogram` (`echo_type: TTE`) — for diagnosis and risk stratification of structural heart disease. Report LVEF, maximal wall thickness, left atrial diameter, valve morphology and gradients, RV size and function, estimated pulmonary artery pressure, pericardium, intracardiac masses. Targeted findings: severe aortic stenosis, obstructive tumour or thrombus, tamponade, aortic dissection, hypertrophic or arrhythmogenic cardiomyopathy, signs of pulmonary embolism or pulmonary hypertension. Do NOT frame it as a cardioembolic-source or bubble study — a right-to-left shunt has no established role in the mechanism of syncope [ESC_2018]
- `order_cardiac_monitoring` — the only test that produces the symptom–rhythm correlation on which the diagnosis of arrhythmic syncope rests. Match the modality to event frequency: `telemetry` in hospital when high-risk features are present (Class I), `holter_24h`/`holter_48h` for episodes at least weekly (Class IIa), `event_monitor_14d`/`_30d` when the inter-symptom interval is four weeks or less (Class IIa), `implantable_loop_recorder` when episodes are months apart. Diagnostic when syncope coincides with a brady- or tachyarrhythmia; without syncope, a pause >3 s, Mobitz II or third-degree block, or rapid prolonged paroxysmal SVT/VT make an arrhythmic mechanism likely. Absence of arrhythmia during a recorded syncopal episode excludes an arrhythmic cause; presyncope alone is not a surrogate [ESC_2018]
- `search_medical_literature` — confirm risk stratification, indications for ICD/pacemaker
- `check_drug_interactions` — review QT-prolonging medications, AV-nodal blockers, diuretics, antihypertensives, antiarrhythmics

**Recommended:**
- `interpret_labs` — targeted assays on a specific suspicion, never a routine battery: haemoglobin/haematocrit for suspected haemorrhage, blood gas for suspected hypoxia, troponin for suspected ischaemia, `D_dimer` for suspected pulmonary embolism, electrolytes, `magnesium` and glucose. `BNP` may support the identification of structural heart disease but does not establish the cause of syncope. `TSH` only where a thyroid mechanism is on the differential — supraventricular tachycardia, atrial flutter, sinus node dysfunction, QT prolongation. `genetic_panel:<panel>` is not first-line: it follows a phenotype already suggested by the ECG or by imaging, or a family history of premature sudden death. Untargeted thyroid, inflammatory, autoimmune and paraneoplastic panels have NO established role — the Class I indication for paraneoplastic and anti-ganglionic AChR antibodies is acute or subacute multidomain autonomic failure, which is a different condition. Raise this step to `required` only where a named assay drives a decision in that patient [ESC_2018]
- `order_specialized_test` (`test_type: tilt_table`) — only if neurally-mediated syncope vs cardiac is uncertain; NOT to confirm cardiac syncope
- `order_specialized_test` (`test_type: exercise_stress_test`) — exertional syncope: the ECG and haemodynamic response to exercise. It does NOT report an outflow-tract gradient; that needs `order_echocardiogram{echo_type: exercise_echo}`
- `order_echocardiogram` (`echo_type: exercise_echo`) — Class I in hypertrophic cardiomyopathy with syncope and a resting or provoked peak instantaneous LVOT gradient below 50 mmHg, standing, sitting or semi-supine. Without it, exertional syncope from provocable obstruction cannot be resolved [ESC_2018]
- `order_advanced_imaging` (`modality: MR_angiography`) — if vascular (subclavian steal, vertebrobasilar TIA) on differential
- Specialist referral *(clinical action — `tool_name: null`, no tool call)* — cardiology / electrophysiology referral

**Optional — second-line cardiac imaging when echocardiography does not resolve a suspected structural or ischaemic cause.** Report the finding together with its relationship to the suspected mechanism: a structural or angiographic finding alone does not establish the cause of syncope.
- `order_advanced_imaging` (`modality: cardiac_MRI`) — tissue characterization with late gadolinium enhancement: arrhythmogenic or infiltrative cardiomyopathy, myocarditis, an unexplained substrate for ventricular arrhythmia
- `order_advanced_imaging` (`modality: cardiac_FDG_PET`) — active myocardial inflammation, after dietary suppression of physiological myocardial glucose uptake. NOT the same study as `FDG_PET`, which is the cerebral scan
- `order_advanced_imaging` (`modality: coronary_CTA` / `coronary_angiography`) — indicated by suspected myocardial ischaemia or infarction, on the same grounds as in a patient without syncope. Coronary angiography carries a Class IIa recommendation; angiography by itself is not diagnostic of the cause of the syncope
- `order_body_imaging` (`study: chest_CTA`) — when aortic dissection, pulmonary embolism or an intrathoracic mass has to be confirmed or excluded rapidly. Note that `order_ct_scan` images the head and neck only
- `obtain_tissue_diagnosis` (`procedure: lymph_node_biopsy`) — histological confirmation of a granulomatous or infiltrative systemic disease, sampling the accessible node rather than the myocardium
- `analyze_brain_mri` — NOT indicated in uncomplicated syncope and does not contribute to identifying a cardiac cause (Class III). Reserved for a neurological examination showing parkinsonism, ataxia or cognitive impairment, where it supports the assessment of autonomic failure (Class I), and for focal signs or a presentation that makes a non-syncopal cause of transient loss of consciousness likely. The imaging that escalates a non-diagnostic echocardiogram here is cardiac, not cerebral, magnetic resonance
- `analyze_eeg` — NOT indicated in syncope (Class III): the interictal recording is normal and it does not contribute to identifying a cardiac cause. Reserved for the two situations in which it changes the diagnosis — transient loss of consciousness in which epilepsy is the likely cause or the clinical data are equivocal, and suspected psychogenic pseudosyncope, where a normal waking eye-closed pattern recorded during a (ideally provoked) attack supports the diagnosis

## 3. Tools that are typically USELESS

- `analyze_brain_mri` — for typical cardiac syncope, low yield; Class III in ESC 2018, and ACEP/AHA state it is not routinely needed. Retained in the panel because the panel label is the hypothesis under test: an agent that correctly suspects a non-syncopal cause must still be able to act
- `analyze_csf` — no role
- `order_ct_scan` — only if head injury sustained or trauma during syncope; routine head CT for syncope NOT indicated, and this tool cannot image a thorax
- `order_advanced_imaging` (most other modalities) — none routinely indicated; in particular the cerebral tracers (`FDG_PET`, `amyloid_PET`, `tau_PET`, `DaTscan`)
- `interpret_labs` (untargeted `TSH` / `autoimmune_basic` / `paraneoplastic` / `ANA` without a granulomatous or autoimmune suspicion) — no established role in cardiac syncope
- `order_specialized_test` (`emg_ncs / muscle_biopsy / nerve_biopsy / etc.`) — none indicated

## 4. Tools that are HARMFUL / contraindicated

- `order_specialized_test` (`test_type: tilt_table`) — relative contraindication in known severe coronary artery disease, severe aortic stenosis, severe carotid stenosis, recent stroke

## 5. Sequence constraints

- `analyze_ecg` → discharge or admission (`hard`): ECG MUST be performed before disposition decision; abnormal ECG mandates admission
- `interpret_labs` (troponin) → cardiac monitoring decision (`hard`): **only in the cases where a named assay drives the decision** — troponin for risk stratification when ischaemia or pulmonary embolism is in play, potassium and magnesium when a correction is itself a required action. Where the labs step is `recommended`, this constraint must NOT be authored: a hard prerequisite that blood tests precede monitoring reinstates the mandate ESC 2018 declines to make, and would penalise an agent for correctly skipping an untargeted panel. It was removed from 18 of the 30 cases for exactly that reason
- `order_echocardiogram` → high-risk discharge (`soft`): document structural disease absence before discharge of high-risk syncope

## 6. Subtype variations

- **M (mild):** brief syncope with rapid recovery, no high-risk features, single event; standard outpatient workup
- **S (standard):** typical cardiac syncope with clear high-risk feature (exertional, abnormal ECG, structural heart disease known); standard workup with cardiology consultation
- **P (progressive / severe):** sustained ventricular tachycardia documented, high-degree AV block, severe aortic stenosis with syncope, HOCM with syncope; urgent treatment (ICD, pacemaker, valve replacement, septal reduction); admission required
- **R (reverse / mimic):** vasovagal syncope (most common syncope, prodromal symptoms, post-prandial / venipuncture / emotional / orthostatic, normal cardiac workup), orthostatic syncope (postural drop in BP, dehydration / medications / autonomic neuropathy), seizure (post-ictal confusion, witnessed convulsive activity, tongue bite — but convulsive syncope causes brief jerks too), cataplexy, drug-induced, hypoglycemia, PE (with syncope at presentation), aortic dissection, pulmonary hypertension; workup adds tilt-table for vasovagal/orthostatic, EEG for seizure, glucose, and `interpret_labs{D_dimer}` plus `order_body_imaging{study: chest_CTA}` if PE suspected — NOT `order_ct_scan`, which images the head and neck

## 7. Common red-herring categories

- **Witness reports "convulsive activity"** — convulsive syncope from cerebral hypoperfusion can mimic seizure; ECG and post-ictal state distinguish
- **Normal ECG** — does NOT exclude paroxysmal arrhythmia; intermittent monitoring needed
- **Negative initial 24h Holter** — sensitivity low for paroxysmal events; event monitor or loop recorder needed
- **"Just vasovagal" in older adult** — atypical for first syncope in elderly; expand workup
- **Tilt-table positive** — supports vasovagal contribution but doesn't exclude concurrent cardiac cause
- **Exertional syncope** — RED FLAG; always cardiac workup including echo, exercise testing
- **The escalation after a non-diagnostic echocardiogram is CARDIAC imaging** — the panel offers brain MRI and a head CT, which makes imaging the wrong organ the most likely error at this point in the pathway. A treadmill test is not an exercise echocardiogram, and a normal ACE does not exclude a granulomatous infiltration

## 8. Allowed citations

- `[ESC_2018]` — Brignole M et al. 2018 ESC Guidelines for the diagnosis and management of syncope. Eur Heart J 2018;39:1883-1948
- `[ACC_AHA_HRS_2017]` — Shen WK et al. 2017 ACC/AHA/HRS guideline for the evaluation and management of patients with syncope. J Am Coll Cardiol 2017;70:e39-e110
- `[Locati_2014]` — Locati ET et al. External prolonged electrocardiographic monitoring in unexplained syncope. Heart 2016;102:1772-1778
- `[EGSYS_2008]` — Del Rosso A et al. Clinical predictors of cardiac syncope at initial evaluation in patients referred urgently to a general hospital: the EGSYS score. Heart 2008;94:1620-1626
- `[ROSE_2010]` — Reed MJ et al. The ROSE (Risk Stratification of Syncope in the Emergency Department) study. J Am Coll Cardiol 2010;55:713-721
- `[Strickberger_2006]` — Strickberger SA et al. AHA/ACCF Scientific Statement on the Evaluation of Syncope. Circulation 2006;113:316-327
