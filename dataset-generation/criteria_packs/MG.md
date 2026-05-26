# Criteria pack: Myasthenia Gravis

**ICD-10:** G70.0x
**Condition enum:** `NeurologicalCondition.MYASTHENIA_GRAVIS`
**Case ID prefix:** `MG`

---

## 1. Diagnostic criteria

MGFA classification (Jaretzki 2000) + diagnostic criteria. Diagnosis based
on (a) clinical: fluctuating, fatigable weakness affecting ocular (ptosis,
diplopia in 50% at onset, 90% lifetime), bulbar (dysphagia, dysarthria),
limb (proximal > distal), or respiratory muscles; (b) supportive tests:
positive ice-pack test for ptosis (bedside, ~80% sens for ocular MG),
positive edrophonium (Tensilon) test [largely replaced by other tests],
SEROLOGIES (AChR-binding antibody positive in ~85% generalized, ~50%
ocular; MuSK antibody in ~6% AChR-negative; LRP4 in seronegatives),
electrophysiology (decrement on RNS >10%, sensitivity ~75% generalized;
single-fiber EMG abnormal jitter sensitivity >95% — gold standard).
CT/MRI chest for thymoma in all confirmed cases. Differentiate ocular
MG (~50% generalize within 2 years), generalized, MuSK-positive (bulbar
predominant, poor RNS response), congenital myasthenic syndromes.

## 2. Standard workup hierarchy

**Required:**
- `interpret_labs` (AChR-binding antibodies; if negative, MuSK antibodies; if seronegative, LRP4 and consider clustered AChR by cell-based assay; TSH for comorbid thyroid disease) [Wolfe_2016]
- `order_specialized_test` (`test_type: repetitive_nerve_stimulation`) — slow rates 2-3 Hz, decrement >10% supports MG; sensitivity higher in proximal muscles [Wolfe_2016]
- `order_specialized_test` (`test_type: emg_single_fiber`) — when antibody-negative and RNS non-diagnostic; gold standard with >95% sensitivity [Wolfe_2016]
- `order_ct_scan` (chest with contrast) OR `analyze_brain_mri` (with attention to chest) — thymoma screening REQUIRED in all confirmed cases [Wolfe_2016]
- `search_medical_literature` — MGFA classification, treatment options (pyridostigmine, prednisone, steroid-sparing agents, IVIG, PLEX)
- `check_drug_interactions` — many drugs exacerbate MG (aminoglycosides, fluoroquinolones, magnesium IV, certain anesthetics, beta-blockers — though usually safe, telithromycin contraindicated)

**Recommended:**
- `order_specialized_test` (`test_type: ice_pack_test`) — bedside for ptosis; cheap and ~80% sensitive
- `order_specialized_test` (`test_type: respiratory_function`) — FVC, MIP/MEP if any bulbar/respiratory symptoms; critical for crisis assessment

**Optional:**
- `analyze_ecg` — pre-thymectomy + comorbid cardiac assessment
- `consult_medical_specialist` — neurology/thymic surgery

## 3. Tools that are typically USELESS

- `analyze_eeg` — peripheral disease (neuromuscular junction)
- `analyze_csf` — no role
- `analyze_brain_mri` — only useful if alternative CNS cause being considered (e.g., brainstem lesion with bulbar/eye signs)
- `order_echocardiogram` — only if comorbid
- `order_cardiac_monitoring` — only if comorbid
- `order_advanced_imaging` (any modality) — none indicated
- `order_specialized_test` (`emg_ncs`) — basic NCS often normal in MG; need RNS or single-fiber specifically

## 4. Tools that are HARMFUL / contraindicated

- `check_drug_interactions` — must flag aminoglycosides, fluoroquinolones (ciprofloxacin), telithromycin, magnesium IV, neuromuscular blockers, beta-blockers (controversial), procainamide — these can precipitate myasthenic crisis [Wolfe_2016]

## 5. Sequence constraints

- `interpret_labs` (AChR) → `emg_single_fiber` (`soft`): order serologies first; single-fiber EMG reserved for seronegative cases
- `order_specialized_test` (`respiratory_function`) → IVIG/PLEX initiation in crisis (`soft`): document respiratory function before treatment

## 6. Subtype variations

- **M (mild / ocular only):** ptosis and/or diplopia only, no generalization (>2 years); standard workup, lower urgency
- **S (standard / generalized):** classic generalized MG, ocular + limb/bulbar; standard workup with thymoma screening REQUIRED
- **P (progressive / crisis):** myasthenic crisis with respiratory failure or imminent failure (FVC <20 mL/kg, MIP <-30 cmH2O, dysphagia + respiratory weakness); ICU admission, urgent IVIG or PLEX, respiratory function REQUIRED + repeated, intubation criteria documented
- **R (reverse / mimic):** Lambert-Eaton myasthenic syndrome (proximal weakness, INCREASES with brief exercise, autonomic features, anti-VGCC antibodies, small cell lung cancer paraneoplastic), botulism (descending paralysis, autonomic), Miller-Fisher (post-infectious, ophthalmoplegia + ataxia + areflexia), thyroid eye disease, brainstem lesion, congenital myasthenic syndromes; workup adds VGCC antibodies for LEMS, anti-GQ1b for MFS, CT chest for LEMS-associated SCLC, MRI brain

## 7. Common red-herring categories

- **Negative AChR antibodies** — does not exclude MG; MuSK and LRP4 cover most remaining
- **Normal RNS** — does not exclude MG; single-fiber EMG more sensitive
- **Improvement with rest** — supportive but not specific (also LEMS shows transient improvement with exercise — opposite pattern)
- **Symmetric weakness** — common in generalized MG but ocular often asymmetric
- **Stress / fatigue / anxiety** — patients often initially dismissed; fluctuation is the MG signature, not a sign of functional disorder

## 8. Allowed citations

- `[Wolfe_2016]` — Wolfe GI et al. Randomized trial of thymectomy in myasthenia gravis (MGTX). NEJM 2016;375:511-522; and the international consensus guidance [Sanders_2016] for treatment.
- `[Sanders_2016]` — Sanders DB et al. International consensus guidance for management of myasthenia gravis. Neurology 2016;87:419-425
- `[Jaretzki_2000_MGFA]` — Jaretzki A et al. Myasthenia gravis: recommendations for clinical research standards. Neurology 2000;55:16-23
- `[Vincent_2003]` — Vincent A. Unravelling the pathogenesis of myasthenia gravis. Nat Rev Immunol 2002;2:797-804
- `[Gilhus_2016]` — Gilhus NE. Myasthenia gravis. NEJM 2016;375:2570-2581
- `[Punga_2022]` — Punga AR et al. Updated treatment guidelines for myasthenia gravis. Lancet Neurol 2022;21:176-188
