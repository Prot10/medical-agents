# Criteria pack: Normal Pressure Hydrocephalus

**ICD-10:** G91.2
**Condition enum:** `NeurologicalCondition.NPH`
**Case ID prefix:** `NPH`

---

## 1. Diagnostic criteria

Relkin 2005 International NPH Study Group criteria. **Probable iNPH**:
(1) Hakim's triad — gait disturbance (magnetic, broad-based, shuffling),
cognitive impairment, urinary urgency/incontinence (only ~50% have full
triad; gait disturbance typically first and most prominent); (2) Imaging:
ventriculomegaly (Evans index >0.3) WITHOUT corresponding sulcal atrophy
or mass effect explaining ventricular dilation; DESH (disproportionately
enlarged subarachnoid space hydrocephalus) — narrowed high convexity sulci
+ widened Sylvian sulci; periventricular hyperintensity; (3) age >40;
(4) chronic course >3-6 months; (5) physiologic criteria: opening pressure
normal (≤24.5 cmH2O); (6) absence of other condition explaining symptoms.
**Confirmed iNPH** = probable + improvement with shunt. Tap test (large-
volume LP, 30-50 mL removal) and lumbar drainage trial used to predict
shunt response (sensitivity ~50-80%, specificity >75%).

## 2. Standard workup hierarchy

**Required:**
- `analyze_brain_mri` — ventricular size (Evans index), DESH pattern, callosal angle, exclude alternative causes (atrophy, mass, prior hemorrhage); MRI > CT [Relkin_2005]
- `order_specialized_test` (`test_type: neuropsych_battery`) — subcortical/frontal pattern (slow processing, executive dysfunction); helpful for tracking + differential from AD [Relkin_2005]
- `analyze_csf` — opening pressure must be <25 cmH2O (normal); large-volume tap test (30-50 mL); pre/post gait + neuropsych assessment for tap response prediction [Tisell_2011]
- `interpret_labs` (TSH, B12, RPR, HIV) — exclude reversible mimics
- `search_medical_literature` — Relkin 2005, INPH Study, shunt response predictors

**Recommended:**
- `consult_medical_specialist` — neurosurgery for shunt evaluation
- Repeat tap test or lumbar drainage (3-5 day trial) if first tap inconclusive

**Optional:**
- `order_advanced_imaging` (`modality: amyloid_PET / FDG_PET`) — for AD comorbidity (50% iNPH have AD co-pathology); inform shunt decision

## 3. Tools that are typically USELESS

- `analyze_eeg` — non-specific
- `analyze_ecg` — unrelated
- `order_echocardiogram` — unrelated
- `order_cardiac_monitoring` — unrelated unless syncope
- `order_ct_scan` — only if MRI contraindicated
- `order_specialized_test` (most others) — gait/cognitive testing covered; specific tests not indicated

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` — relatively contraindicated if mass effect; small risk of post-LP CSF leak in older patients (rare but reported)

## 5. Sequence constraints

- `analyze_brain_mri` → `analyze_csf` (`hard`): exclude mass effect / secondary hydrocephalus before LP [Relkin_2005]
- `order_specialized_test` (`neuropsych_battery`) → `analyze_csf` (tap test) (`soft`): baseline gait + neuropsych BEFORE tap, then re-assess 1-4 hours after — improvement is the response criterion

## 6. Subtype variations

- **M (mild):** subtle gait disturbance, mild cognitive change, no incontinence; conservative trial of tap test
- **S (standard):** Hakim's triad of moderate severity, classic MRI; standard workup + tap test
- **P (progressive):** rapidly progressive, complete triad, severe gait; expedited workup + early shunt consideration
- **R (reverse / mimic):** vascular cognitive impairment (similar gait but more abrupt steps, MRI shows leukoaraiosis disproportionate to ventricles), Parkinson's (rest tremor, asymmetry — but NPH "magnetic gait" can mimic; trial of L-dopa), Alzheimer's (memory predominant), atrophy with secondary ventriculomegaly, post-traumatic hydrocephalus, prior SAH; workup adds DaTscan if PD on differential, more detailed neuropsych, AD biomarkers

## 7. Common red-herring categories

- **Ventriculomegaly alone** — many causes (atrophy, congenital, secondary); MRI must show DESH or other suggestive features
- **Improvement with single tap** — confirms response but small effect can be placebo; sustained improvement needed
- **Concurrent dementia** — AD co-pathology common; doesn't preclude shunt benefit for gait if patient is candidate
- **Imaging-based diagnosis without symptoms** — incidental ventriculomegaly doesn't = iNPH
- **Cognitive decline alone without gait** — uncommon iNPH presentation; reconsider diagnosis

## 8. Allowed citations

- `[Relkin_2005]` — Relkin N et al. Diagnosing idiopathic normal-pressure hydrocephalus. Neurosurgery 2005;57(3 Suppl):S2-S4
- `[Marmarou_2005]` — Marmarou A et al. Diagnosis and management of idiopathic normal-pressure hydrocephalus. Neurosurgery 2005;57(3 Suppl):S1-S52
- `[Tisell_2011]` — Tisell M et al. Shunt surgery in patients with hydrocephalus and white matter changes. J Neurosurg 2011;114:1432-1438
- `[Hakim_1965]` — Hakim S, Adams RD. The special clinical problem of symptomatic hydrocephalus with normal cerebrospinal fluid pressure. J Neurol Sci 1965;2:307-327
- `[Williams_2016]` — Williams MA, Malm J. Diagnosis and treatment of idiopathic normal pressure hydrocephalus. Continuum 2016;22:579-599
