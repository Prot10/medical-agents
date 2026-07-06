# Criteria pack: Bacterial meningitis

**ICD-10:** G00.x (by organism), G00.9 (unspecified bacterial)
**Condition enum:** `NeurologicalCondition.BACTERIAL_MENINGITIS`
**Case ID prefix:** `BACT-MEN`

---

## 1. Diagnostic criteria

IDSA 2004 guidelines (acute bacterial meningitis): clinical syndrome
(fever + headache + meningismus + altered mental status, though classic
triad in only ~40%) + CSF findings (turbid appearance, opening pressure
typically >250 mmH2O, WBC >100 with PMN predominance >80%, glucose
<40 or CSF:serum ratio <0.4, protein >200 mg/dL, +/- positive Gram stain
and culture). PCR / multiplex pathogen panel useful when antibiotics
already given. The Bacterial Meningitis Score (Nigrovic) stratifies in
children: low risk if all of: negative CSF Gram stain, CSF ANC <1000,
CSF protein <80 mg/dL, peripheral ANC <10,000, no seizure at presentation.

## 2. Standard workup hierarchy

**Required:**
- `analyze_csf` (`special_tests: meningitis_panel`) — Gram stain, culture, cell count + differential, glucose, protein, lactate; multiplex PCR if available [IDSA_2004]
- `interpret_labs` (CBC with diff, CMP, blood cultures ×2, lactate, procalcitonin) — peripheral leukocytosis, bacteremia [IDSA_2004]
- `order_ct_scan` (without contrast) — exclude mass effect / herniation risk PRIOR to LP if any of: immunocompromise, recent seizure, focal neurologic deficit, papilledema, altered mental status, age >60 [IDSA_2004]
- `search_medical_literature` — empiric antibiotic selection by age/risk; dexamethasone evidence [IDSA_2004]
- `check_drug_interactions` — empiric vancomycin + ceftriaxone (+ ampicillin if Listeria risk); dexamethasone timing (before/with first antibiotic dose) [De_Gans_2002]

**Recommended:**
- `analyze_brain_mri` — if delayed presentation, abscess suspicion, or workup for complications (subdural empyema, ventriculitis); MRI > CT for these [Brouwer_2012]

**Optional:**
- `analyze_eeg` — only if seizure activity or persistent altered mental status

## 3. Tools that are typically USELESS

- `analyze_ecg` — unrelated to meningitis diagnosis
- `order_echocardiogram` — only if endocarditis suspected as a primary source
- `order_cardiac_monitoring` — unrelated
- `order_advanced_imaging` (any modality) — none indicated; advanced imaging adds no diagnostic value in routine acute meningitis
- `order_specialized_test` (most types) — most don't apply

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` — when imaging shows mass effect, midline shift, or basal cistern obliteration (LP can precipitate herniation) [IDSA_2004]

## 5. Sequence constraints

- `order_ct_scan` → `analyze_csf` (`hard`): CT MUST precede LP when ANY indication for imaging-first applies (immunocompromise, focal signs, altered consciousness, seizure, papilledema, age >60). Failure = preventable herniation event. [IDSA_2004]
- `interpret_labs` → empiric antibiotics (`hard`): blood cultures MUST be drawn BEFORE first antibiotic dose; LP should ideally precede antibiotics too but antibiotics must not be delayed >1 hour for LP [IDSA_2004]

## 6. Subtype variations

- **M (mild):** community-acquired, immunocompetent adult, classic presentation; standard workup
- **S (standard):** typical adult presentation, may have one risk factor for complicated course; standard workup + MRI optional
- **P (progressive / severe):** septic shock, severely altered mental status, focal signs, complications; CT REQUIRED before LP, MRI may be needed early, ICU-level care; consider repeat LP at 24-48h if poor clinical response
- **R (reverse / mimic):** viral meningitis (lymphocytic predominance, normal glucose), TB meningitis (subacute, low glucose, high protein, lymphocytic), fungal (cryptococcal antigen), drug-induced aseptic, partially-treated bacterial; workup adds HSV/enterovirus PCR, AFB stain + TB PCR + ADA, cryptococcal antigen

## 7. Common red-herring categories

- **Recent antibiotic use** — converts CSF to "partially treated" pattern (lower PMN%, may have negative Gram stain) — does not exclude bacterial meningitis
- **Petechial rash without fever** — could be other entities, but meningococcemia must be excluded
- **CSF lymphocyte-predominant early** — possible in early bacterial meningitis (PMN shift happens in hours)
- **Negative Gram stain** — does not exclude meningitis; sensitivity ~60-90%
- **Normal CT** — does NOT prove safety of LP if clinical signs of herniation risk (papilledema)

## 8. Allowed citations

- `[IDSA_2004]` — Tunkel AR et al. Practice guidelines for the management of bacterial meningitis. Clin Infect Dis 2004;39:1267-1284
- `[De_Gans_2002]` — De Gans J, van de Beek D. Dexamethasone in adults with bacterial meningitis. NEJM 2002;347:1549-1556
- `[Brouwer_2012]` — Brouwer MC et al. Community-acquired bacterial meningitis in adults. NEJM 2012;367:146-156
- `[Nigrovic_2007]` — Nigrovic LE et al. Clinical prediction rule for identifying children with CSF pleocytosis at very low risk of bacterial meningitis. JAMA 2007;297:52-60
- `[ESCMID_2016]` — van de Beek D et al. ESCMID guideline for diagnosis and treatment of acute bacterial meningitis. Clin Microbiol Infect 2016;22(Suppl 3):S37-62
