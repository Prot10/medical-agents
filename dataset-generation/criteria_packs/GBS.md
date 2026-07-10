# Criteria pack: Guillain-Barré Syndrome (GBS)

**ICD-10:** G61.0
**Condition enum:** `NeurologicalCondition.GUILLAIN_BARRE`
**Case ID prefix:** `GBS`

---

## 1. Diagnostic criteria

Brighton Collaboration (2011) levels of certainty + NINDS criteria (Asbury
1990). Required features: progressive bilateral and relatively symmetric
weakness of the limbs, areflexia/hyporeflexia in weak limbs. Supportive:
nadir 2–4 weeks, antecedent infection (Campylobacter jejuni most common
~30%, EBV, CMV, Mycoplasma, Zika), CSF albuminocytologic dissociation
(elevated protein with normal cell count, typically >1 week into illness),
electrodiagnostic features of demyelination or axonal loss. Variants:
classic AIDP (~85% Western), AMAN, AMSAN, Miller-Fisher (ophthalmoplegia +
ataxia + areflexia, anti-GQ1b positive), pharyngeal-cervical-brachial.

## 2. Standard workup hierarchy

**Required:**
- `order_specialized_test` (`test_type: emg_ncs`) — demyelinating pattern (prolonged distal latencies, conduction block, F-wave abnormalities), or axonal (reduced CMAP amplitudes) [Hadden_1998]
- `analyze_csf` — albuminocytologic dissociation (protein elevated, cells <10/μL — though early in disease may be normal) [Asbury_1990]
- `interpret_labs` (CBC, CMP, HIV, anti-GM1 / anti-GQ1b antibodies, stool culture for Campylobacter if recent diarrhea) — variant typing + identifying triggers [Yuki_2012]
- `order_specialized_test` (`test_type: respiratory_function`) — FVC, MIP/MEP every 4–6 hours initially; deterioration to FVC <20 mL/kg or MIP <30 cmH2O = ICU/intubation indication [Sharshar_2003]
- `search_medical_literature` — IVIG vs plasmapheresis evidence (equivalent efficacy)
- `check_drug_interactions` — IVIG (renal function), plasmapheresis (coagulation, calcium)

**Recommended:**
- `analyze_brain_mri` — only if atypical features (CNS involvement, transverse myelitis on differential, structural mimic)
- `analyze_ecg` + `order_cardiac_monitoring` — autonomic involvement (arrhythmia, BP lability) common; monitor in moderate-severe cases [Asbury_1990]

**Optional:**
- Specialist referral *(clinical action — `tool_name: null`, no tool call)* — neurology/ICU for severe cases

## 3. Tools that are typically USELESS

- `analyze_eeg` — peripheral disease, no role
- `order_echocardiogram` — only if pre-existing cardiac disease or unexplained hemodynamic instability
- `order_ct_scan` — no role
- `order_advanced_imaging` (any) — none indicated

## 4. Tools that are HARMFUL / contraindicated

(none specific to typical GBS workup — care needed with IVIG in renal disease, plasmapheresis in hemodynamic instability, but these are treatment not diagnostics)

## 5. Sequence constraints

- `order_specialized_test` (`respiratory_function`) → IVIG/PLEX initiation (`soft`): respiratory status MUST be documented before treatment; early ICU triage critical [Sharshar_2003]
- `interpret_labs` (CBC, CMP) → IVIG (`soft`): IgA deficiency screen, renal function before IVIG

## 6. Subtype variations

- **M (mild):** ambulatory, mild weakness, normal respiratory function; standard workup, can treat outpatient or short admit
- **S (standard):** ambulatory but progressing or moderate weakness; standard workup + admit for monitoring
- **P (progressive / severe):** rapid progression, bulbar/respiratory involvement, dysautonomia; ICU, frequent FVC, cardiac monitoring REQUIRED
- **R (reverse / mimic):** other acute neuropathies — porphyria, lead/arsenic, tick paralysis, botulism, transverse myelitis, hypokalemic periodic paralysis, vasculitic neuropathy; workup adds urine porphyrins, heavy metals, MRI spine, botulism testing

## 7. Common red-herring categories

- **Normal CSF protein early** — early GBS (<5-7 days) may have normal CSF; if classic clinical + EMG suggests GBS, treat
- **Distal paresthesias** — early symptom often ignored; ascending weakness follows
- **Normal initial EMG** — early electrodiagnostic studies may be normal; F-waves first to be abnormal
- **Fluctuating weakness** — distinguishes from MG (fatigability) — but treatment-related improvement and worsening (TRF) occurs
- **Pain** — often severe in GBS but underrecognized; not "psychogenic"

## 8. Allowed citations

- `[Asbury_1990]` — Asbury AK, Cornblath DR. Assessment of current diagnostic criteria for GBS. Ann Neurol 1990;27 Suppl:S21-24
- `[Hadden_1998]` — Hadden RD et al. Electrophysiological classification of Guillain-Barré syndrome. Ann Neurol 1998;44:780-788
- `[Brighton_2011]` — Sejvar JJ et al. GBS and Fisher syndrome: case definitions and guidelines for collection, analysis and presentation of immunization safety data. Vaccine 2011;29:599-612
- `[Sharshar_2003]` — Sharshar T et al. Early predictors of mechanical ventilation in Guillain-Barré syndrome. Crit Care Med 2003;31:278-283
- `[Yuki_2012]` — Yuki N, Hartung HP. Guillain-Barré syndrome. NEJM 2012;366:2294-2304
- `[van_den_Berg_2014]` — van den Berg B et al. Guillain-Barré syndrome: pathogenesis, diagnosis, treatment, and prognosis. Nat Rev Neurol 2014;10:469-482
