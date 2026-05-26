# Criteria pack: Functional Neurological Disorder (FND)

**ICD-10:** F44.4 (motor), F44.5 (non-epileptic seizures), F44.6 (sensory), F44.7 (mixed)
**Condition enum:** `NeurologicalCondition.FUNCTIONAL_NEUROLOGICAL_DISORDER`
**Case ID prefix:** `FND`

---

## 1. Diagnostic criteria

DSM-5: Functional Neurological Symptom Disorder — (a) ≥1 symptom of altered
voluntary motor or sensory function, (b) clinical findings provide evidence
of incompatibility with neurological/medical conditions, (c) symptom not
better explained by another disorder, (d) clinically significant distress
or impairment. **RULE-IN** signs are essential — diagnosis is positive, not
purely exclusionary. Examples: Hoover's sign (functional leg weakness),
tremor entrainment (functional tremor), Tinel's-like give-way weakness,
fixed dystonic posturing, midline splitting of sensory loss, tubular visual
fields, ictal eye closure (functional seizures), pelvic thrusting with
preserved awareness, prolonged duration with normal post-ictal state.

## 2. Standard workup hierarchy

**Required:**
- `analyze_brain_mri` — exclude structural cause of symptoms (stroke, MS, tumor); when clinically indicated, MRI is part of due diligence, not the route to diagnosis [Espay_2018]
- `interpret_labs` (CBC, CMP, TSH, B12) — exclude common reversible causes
- `search_medical_literature` — positive diagnostic signs, FND treatment evidence

**Recommended:**
- `analyze_eeg` (`eeg_type: video`) — video-EEG REQUIRED for suspected functional (psychogenic non-epileptic) seizures; capturing an event during normal EEG is diagnostic [ILAE_PNES_2013]
- `order_specialized_test` (`test_type: neuropsych_battery`) — comorbid mood, somatization, trauma history; helpful for treatment planning
- `check_drug_interactions` — review of medications that may worsen symptoms

**Optional:**
- `consult_medical_specialist` — psychiatry/health psychology for treatment

## 3. Tools that are typically USELESS

- `analyze_csf` — no role unless other diagnosis genuinely suspected
- `analyze_ecg` — unrelated
- `order_echocardiogram` — unrelated
- `order_cardiac_monitoring` — unrelated unless syncope on differential
- `order_ct_scan` — MRI is preferred when imaging needed
- `order_advanced_imaging` (most) — none indicated for typical FND
- `order_specialized_test` (`emg_ncs / muscle_biopsy / nerve_biopsy`) — invasive testing reinforces somatic illness model; not indicated

## 4. Tools that are HARMFUL / contraindicated

- Over-investigation in general (not a single tool, but a pattern). The principal harm in FND is iatrogenic — every additional negative test reinforces patient illness conviction and delays definitive diagnosis. Per Stone 2018, repeated negative workups WORSEN prognosis.

## 5. Sequence constraints

(none — workup parallel, but the principle is "as little as needed to confirm rule-in signs + exclude alarm features")

## 6. Subtype variations

- **M (mild):** circumscribed symptom, clear rule-in sign on exam; minimal workup
- **S (standard):** mixed motor/sensory or functional seizures; standard workup including video-EEG if seizure phenotype
- **P (progressive / severe):** disabling symptoms, multiple body regions, prolonged duration, refractory; same diagnostic workup but emphasizes multidisciplinary treatment
- **R (reverse / mimic):** the "FND" diagnosis was wrong — actually MS, stroke, dystonia, autoimmune encephalitis, neuromyelitis optica, or rare metabolic disease; workup adds the targeted rule-out (e.g., LP+OCBs for MS, MOG/AQP4 antibodies, paraneoplastic panel, B12, ceruloplasmin)

## 7. Common red-herring categories

- **Psychiatric history** — does not exclude organic disease; FND can coexist with organic
- **Symptoms during stress** — many organic diseases (MS, migraine) also flare with stress
- **"Patient is dramatic"** — bedside impression is unreliable; rule-in signs are reliable
- **Normal initial workup** — does not equal FND; positive rule-in evidence is required
- **Fluctuating symptoms** — common in FND but also in MG, MS

## 8. Allowed citations

- `[Espay_2018]` — Espay AJ et al. Current concepts in diagnosis and treatment of functional neurological disorders. JAMA Neurology 2018;75:1132-1141
- `[Stone_2018]` — Stone J et al. Functional disorders in the neurology clinic: a complete diagnostic neurological approach. Pract Neurol 2018;18:267-278
- `[ILAE_PNES_2013]` — LaFrance WC Jr et al. ILAE Nonepileptic Seizures Task Force: minimum diagnostic standards. Epilepsia 2013;54:2005-2018
- `[Carson_2012]` — Carson AJ, Lehn A. Epidemiology of functional disorders. Handb Clin Neurol 2016;139:47-60
- `[Nielsen_2015]` — Nielsen G et al. Physiotherapy for functional motor disorders: consensus recommendations. J Neurol Neurosurg Psychiatry 2015;86:1113-1119
