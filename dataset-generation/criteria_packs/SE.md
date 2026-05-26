# Criteria pack: Status epilepticus

**ICD-10:** G41.x (by type)
**Condition enum:** `NeurologicalCondition.STATUS_EPILEPTICUS`
**Case ID prefix:** `SE`

---

## 1. Diagnostic criteria

ILAE 2015 operational definitions. **Convulsive SE** = convulsive seizures
lasting ≥5 minutes OR ≥2 seizures without return to baseline. T1 (initiate
acute treatment) = 5 min; T2 (long-term consequences likely) = 30 min.
**Non-convulsive SE (NCSE)** = electrographic seizure activity ≥30 min
without convulsive features, OR clinical features (altered MS, subtle motor)
+ electrographic correlate. Defined by Salzburg 2015 criteria when LBM/CBM
patterns require duration + responsiveness assessment. **Refractory SE** =
SE persisting after first-line benzodiazepine + adequate second-line AED.
**Super-refractory SE** = SE continuing or recurring ≥24h after starting
anesthetic therapy.

## 2. Standard workup hierarchy

**Required:**
- `analyze_eeg` (continuous EEG, video-EEG) — confirm electrographic seizure activity, characterize, monitor response to treatment; ESSENTIAL in any altered patient post-SE or in non-convulsive presentations [Brophy_2012]
- `interpret_labs` (CBC, CMP, glucose, calcium, magnesium, AED levels if applicable, ammonia, ABG, lactate, blood cultures, tox screen, beta-hCG in women of reproductive age) — identify provoking factors; lactate often elevated post-seizure [Glauser_2016]
- `order_ct_scan` (non-contrast head) — exclude acute structural cause (hemorrhage, ischemia, mass, edema) — particularly when first SE [Brophy_2012]
- `analyze_brain_mri` — subacute, identifies more subtle causes (encephalitis, hippocampal sclerosis, MS, autoimmune); often needed after initial CT [Glauser_2016]
- `search_medical_literature` — confirm Treatment of SE algorithm, ESETT trial second-line options
- `check_drug_interactions` — benzodiazepines (lorazepam preferred IV), second-line (levetiracetam, fosphenytoin, valproate — all equivalent per ESETT 2019), anesthetic infusions (midazolam, propofol, pentobarbital) in refractory

**Required (when etiology unclear):**
- `analyze_csf` (cells, protein, glucose, cultures, HSV/enterovirus PCR, autoimmune panel including NMDAR) — encephalitis is a major reversible cause; consider in any new-onset SE [Brophy_2012]
- `interpret_labs` (autoimmune encephalitis panel, paraneoplastic panel, anti-thyroid antibodies) — autoimmune SE

**Recommended:**
- `consult_medical_specialist` — neurology + critical care; refractory SE benefits from epilepsy subspecialist
- `order_specialized_test` (`test_type: respiratory_function`) — if airway/respiratory concern (rarely a primary investigation here; usually clinical)

**Optional:**
- `analyze_ecg` — baseline; rule out arrhythmia cause (rare, but cardioembolic stroke causing SE possible)

## 3. Tools that are typically USELESS

- `order_echocardiogram` — only if cardiac cause suspected
- `order_cardiac_monitoring` — only for cardiac comorbidity
- `order_advanced_imaging` (`modality: amyloid_PET / DaTscan`) — none indicated acutely
- `order_advanced_imaging` (`modality: carotid_duplex / transcranial_doppler`) — none indicated

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` — must exclude mass effect on imaging first; usually safe in SE absent imaging contraindication
- Certain AEDs in specific contexts: phenytoin/fosphenytoin in cardiac instability (extravasation, hypotension); valproate in pregnancy and women of reproductive age, mitochondrial disease (VPA-induced hepatotoxicity in POLG)

## 5. Sequence constraints

- Treatment must be SIMULTANEOUS with workup — do not delay benzodiazepines for diagnostics [Brophy_2012]
- `order_ct_scan` → `analyze_csf` (`hard`): when LP indicated, head CT first
- `interpret_labs` (glucose) → glucose administration (`hard`): correct hypoglycemia immediately if present (don't wait for full panel)

## 6. Subtype variations

- **M (mild / brief):** single convulsive seizure with rapid resolution after 1st-line benzodiazepine; workup for trigger
- **S (standard):** convulsive SE responding to benzodiazepine + one AED; standard workup
- **P (progressive / refractory):** refractory or super-refractory SE; full workup including LP if no exclusion, autoimmune encephalitis screen, ICU with continuous EEG, anesthetic infusions, evaluation for ketogenic diet/immunotherapy
- **R (reverse / mimic):** pseudo-status (psychogenic non-epileptic), severe metabolic encephalopathy mimicking NCSE (electrographic correlate distinguishes), severe migraine with confusion, drug intoxication, locked-in syndrome; key tool = video-EEG to distinguish

## 7. Common red-herring categories

- **Cessation of convulsions** — does NOT exclude NCSE; ~14% of patients in convulsive SE remain in non-convulsive SE after motor activity stops
- **AED level "in range"** — does not exclude breakthrough seizures; therapeutic ranges are guidelines
- **Normal labs** — many SE etiologies have normal routine labs (autoimmune, structural)
- **Fever** — could be infectious cause but also post-ictal; broad infectious workup needed
- **Improvement with treatment** — confirms treatable cause but does not confirm specific diagnosis

## 8. Allowed citations

- `[Brophy_2012]` — Brophy GM et al. Guidelines for the evaluation and management of status epilepticus. Neurocrit Care 2012;17:3-23
- `[ILAE_2015_SE]` — Trinka E et al. A definition and classification of status epilepticus. Epilepsia 2015;56:1515-1523
- `[Glauser_2016]` — Glauser T et al. Evidence-based guideline: treatment of convulsive status epilepticus in children and adults. Epilepsy Curr 2016;16:48-61
- `[ESETT_2019]` — Kapur J et al. Randomized trial of three anticonvulsant medications for status epilepticus. NEJM 2019;381:2103-2113
- `[Salzburg_NCSE_2015]` — Leitinger M et al. Salzburg consensus criteria for non-convulsive status epilepticus. Epilepsia 2015;56:1411-1416
- `[Shorvon_2011]` — Shorvon S, Ferlisi M. The treatment of super-refractory status epilepticus. Brain 2011;134:2802-2818
