# Criteria pack: Subarachnoid hemorrhage (aneurysmal)

**ICD-10:** I60.x (by location)
**Condition enum:** `NeurologicalCondition.SUBARACHNOID_HEMORRHAGE`
**Case ID prefix:** `SAH`

---

## 1. Diagnostic criteria

AHA/ASA 2012 (Connolly) + 2023 updates for aneurysmal SAH. Clinical
presentation: thunderclap headache (maximal intensity within seconds-minutes,
"worst headache of life"), often with brief loss of consciousness, neck
stiffness, photophobia, focal deficits if vasospasm or hematoma. Hunt-Hess
grade (I-V) and WFNS grade (I-V) for severity. Diagnostic pathway: (1)
non-contrast CT head — sensitivity ~98% within 6h of onset, declining to
~80-85% at 24h, much lower after 7 days; (2) if CT negative but high
suspicion, LP — xanthochromia (yellow CSF supernatant from RBC breakdown,
appears ~6-12h after bleed, persists ~2-3 weeks); RBC count high and
non-clearing across tubes also supportive; (3) CTA OR DSA to identify
aneurysm location for treatment planning. Modified Fisher scale for
vasospasm risk based on CT blood distribution.

## 2. Standard workup hierarchy

**Required:**
- `order_ct_scan` (non-contrast CT head) — FIRST imaging in suspected SAH; cisterns, sulci, fissures hyperdense [Connolly_2012]
- `order_ct_scan` (`angiography: true`, CTA head/neck) — identify aneurysm or AVM after positive CT; gold standard alternative to DSA in initial workup [Connolly_2012]
- `analyze_csf` — required when CT negative but clinical suspicion remains; perform ≥6-12h after symptom onset to allow xanthochromia development; spectrophotometric analysis ideal [Edlow_2008]
- `interpret_labs` (CBC, BMP, coagulation, type & screen, troponin, BNP) — pre-op workup, neurogenic stress cardiomyopathy, hyponatremia (cerebral salt wasting / SIADH)
- `analyze_ecg` — neurogenic stress (broad T-wave inversions, QT prolongation, ST changes); rule out concurrent cardiac event
- `search_medical_literature` — Hunt-Hess + WFNS + Fisher grading, treatment options (clipping vs coiling)
- `consult_medical_specialist` — neurosurgery + interventional neuroradiology REQUIRED
- `check_drug_interactions` — nimodipine (oral, every 4h x 21 days, all patients with aneurysmal SAH), antiseizure prophylaxis (controversial — short course often used), reversal of anticoagulation if applicable

**Recommended:**
- `order_cardiac_monitoring` (`monitor_type: telemetry`) — arrhythmia detection in dysautonomia, monitor for cardiac complications
- `order_echocardiogram` — if cardiac troponin elevation or hemodynamic instability suggesting neurogenic stress cardiomyopathy
- `analyze_brain_mri` (with gradient echo / SWI) — secondary; identifies blood products, can help when CT timing missed; not first-line acute
- `order_advanced_imaging` (`modality: transcranial_doppler`) — vasospasm monitoring days 4-14 post-bleed

**Optional:**
- `order_advanced_imaging` (`modality: MR_angiography`) — alternative to CTA in renal disease or contrast allergy

## 3. Tools that are typically USELESS

- `analyze_eeg` — only if non-convulsive status epilepticus suspected as cause of altered MS
- `order_specialized_test` (most types) — none indicated acutely
- `order_advanced_imaging` (`modality: amyloid_PET / DaTscan / FDG_PET`) — none relevant

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` — LP in SAH with significant mass effect or hydrocephalus risks worsening; CT FIRST [Edlow_2008]
- Aspirin or other antiplatelets pre-securing aneurysm — increases rebleeding risk

## 5. Sequence constraints

- `order_ct_scan` (non-contrast) → `analyze_csf` (`hard`): CT MUST precede LP — both for diagnosis (CT positive obviates LP) and safety [Edlow_2008]
- `order_ct_scan` (positive for SAH) → CTA (`hard`): aneurysm characterization before treatment planning
- `consult_medical_specialist` (neurosurgery) → definitive treatment (`hard`): clipping or coiling within 24-72h to reduce rebleeding risk [Connolly_2012]
- `interpret_labs` (coagulation) → invasive procedures (`hard`): correct coagulopathy before LP or surgery

## 6. Subtype variations

- **M (mild):** Hunt-Hess 1-2, small aneurysm, GCS 14-15; standard workup, urgent surgical/endovascular evaluation
- **S (standard):** Hunt-Hess 2-3, classic presentation; standard workup with monitoring for complications
- **P (progressive / severe):** Hunt-Hess 4-5, large bleed, hydrocephalus, intraventricular extension, comatose; ICU, emergent treatment, EVD often required, full monitoring including TCD for vasospasm
- **R (reverse / mimic):** thunderclap headache with negative SAH workup — RCVS (reversible cerebral vasoconstriction, "string of beads" on angiography), cervical artery dissection, pituitary apoplexy, cerebral venous sinus thrombosis, intracranial hypertension (severe), migraine (thunderclap migraine — diagnosis of exclusion), spontaneous intracranial hypotension; workup adds dedicated MRA/MRV, pituitary MRI, repeat vascular imaging at days 7-14 for RCVS

## 7. Common red-herring categories

- **Maximally severe headache resolved spontaneously** — does NOT rule out SAH; sentinel headaches occur in ~10-40% before major bleed
- **Negative CT after 24h** — sensitivity drops sharply; LP becomes essential
- **Bloody LP — interpret carefully** — traumatic tap vs SAH: traumatic decreases across tubes, xanthochromia absent if very early; SAH has uniform RBCs across tubes + xanthochromia
- **Atraumatic SAH without aneurysm on CTA** — perimesencephalic non-aneurysmal SAH is a more benign entity (peri-pontine cisternal blood without aneurysm)
- **Normotensive patient** — SAH can present without hypertension; absence does not exclude

## 8. Allowed citations

- `[Connolly_2012]` — Connolly ES et al. Guidelines for the management of aneurysmal subarachnoid hemorrhage. Stroke 2012;43:1711-1737
- `[Hoh_2023]` — Hoh BL et al. 2023 Guideline for the management of patients with aneurysmal subarachnoid hemorrhage. Stroke 2023;54:e314-e370
- `[Edlow_2008]` — Edlow JA et al. Clinical policy: critical issues in the evaluation and management of adult patients presenting to the ED with acute headache. Ann Emerg Med 2008;52:407-436
- `[Perry_2011]` — Perry JJ et al. High risk clinical characteristics for subarachnoid haemorrhage in patients with acute headache: prospective cohort study. BMJ 2011;343:d4277
- `[Hunt_Hess_1968]` — Hunt WE, Hess RM. Surgical risk as related to time of intervention in the repair of intracranial aneurysms. J Neurosurg 1968;28:14-20
- `[Fisher_1980]` — Fisher CM et al. Relation of cerebral vasospasm to subarachnoid hemorrhage visualized by computerized tomographic scanning. Neurosurgery 1980;6:1-9
