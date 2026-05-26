# Criteria pack: Anti-NMDAR encephalitis

**ICD-10:** G04.81 (autoimmune encephalitis)
**Condition enum:** `NeurologicalCondition.AUTOIMMUNE_ENCEPHALITIS_NMDAR`
**Case ID prefix:** `NMDAR-ENC`

---

## 1. Diagnostic criteria

Graus 2016 (Lancet Neurol) criteria for autoimmune encephalitis. For
**definite anti-NMDAR encephalitis**: rapid onset (<3 months) + at least 1 of
six major groups (abnormal behavior/cognitive dysfunction, speech dysfunction,
seizures, movement disorder/dyskinesias/rigidity/abnormal postures,
decreased consciousness, autonomic dysfunction/central hypoventilation)
+ IgG anti-NMDAR GluN1 antibodies in CSF (or serum confirmed by CSF and
tissue-based assay) + reasonable exclusion of other disorders.
**Probable** = clinical features + abnormal CSF (lymphocytic pleocytosis,
OCB) or MRI suggestive + reasonable exclusion. Often subacute course with
prodromal viral illness, then psychiatric/cognitive symptoms, then
seizures/movement disorder/dysautonomia/coma. Strong association with
ovarian teratoma (~50% young women, lower in other demographics).

## 2. Standard workup hierarchy

**Required:**
- `analyze_csf` (`special_tests: NMDAR_antibodies, autoimmune_panel, oligoclonal_bands; cells, protein, glucose`) — anti-NMDAR IgG in CSF is most sensitive (100%) and specific; serum less reliable [Graus_2016]
- `analyze_brain_mri` (with gadolinium) — often NORMAL early; may show T2/FLAIR hyperintensity in medial temporal, frontobasal, brainstem; rule out alternative cause [Titulaer_2013]
- `analyze_eeg` — abnormal in >90%, "extreme delta brush" pattern in 30-50% (specific but not sensitive); also helpful for non-convulsive status epilepticus [Schmitt_2012]
- `interpret_labs` (CBC, CMP, TSH, blood cultures, HIV, syphilis, paraneoplastic panel if applicable; comprehensive autoimmune encephalitis panel: anti-Hu, anti-Ma2, anti-LGI1, anti-CASPR2, anti-AMPAR, anti-GABABR, anti-DPPX, anti-IgLON5) [Graus_2016]
- `order_ct_scan` (pelvis + chest + abdomen with contrast in women of reproductive age) OR transvaginal ultrasound — ovarian teratoma screening, all women confirmed cases [Dalmau_2011]
- `search_medical_literature` — Graus 2016 criteria, first-line (steroids, IVIG, PLEX) vs second-line (rituximab, cyclophosphamide) immunotherapy
- `check_drug_interactions` — steroids, IVIG, rituximab, antipsychotics (some worsen movements), benzodiazepines

**Recommended:**
- `consult_medical_specialist` — neurology + psychiatry + gynecology if teratoma

**Optional:**
- `order_advanced_imaging` (`modality: FDG_PET`) — research/specialty use, frontotemporal hypermetabolism in early stages, hypometabolism later

## 3. Tools that are typically USELESS

- `analyze_ecg` — only if dysautonomia/cardiac involvement
- `order_echocardiogram` — only if specific cardiac concern
- `order_cardiac_monitoring` — useful in dysautonomic cases (arrhythmias common in severe NMDAR-E)
- `order_advanced_imaging` (most others) — none indicated
- `order_specialized_test` (most) — not indicated

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` — exclude mass effect on MRI/CT before LP
- Certain antipsychotics (haloperidol especially) — may worsen extrapyramidal symptoms in NMDAR-E; tool should flag

## 5. Sequence constraints

- `analyze_brain_mri` → `analyze_csf` (`hard`): exclude mass effect before LP, especially in patients with focal signs or altered consciousness
- `interpret_labs` (paraneoplastic + autoimmune panel) → empiric immunotherapy (`soft`): start therapy if high pre-test probability — don't wait for antibody results, which take days

## 6. Subtype variations

- **M (mild):** isolated psychiatric features only, partial syndrome; standard workup with serial monitoring
- **S (standard):** classic multistage syndrome (prodrome → psych → seizures/movement → dysautonomia); standard workup
- **P (progressive / severe):** rapidly progressive multistage syndrome with dysautonomia/central hypoventilation/coma; ICU level care, comprehensive workup + earlier escalation to second-line
- **R (reverse / mimic):** primary psychiatric disorder (first-episode psychosis — but typical NMDAR has SUBACUTE not chronic), viral encephalitis (HSV with bilateral mesial temporal — but NMDAR can post-HSV!), other autoimmune encephalitides (LGI1, CASPR2, GABA-B, AMPAR), CJD, NMOSD with brainstem involvement, drug intoxication (NMDA antagonists ketamine/PCP), serotonin/neuroleptic malignant syndrome; workup adds HSV-1/2 PCR (CSF), specific autoantibody panel, RT-QuIC, drug screen, CK

## 7. Common red-herring categories

- **"First-episode psychosis" in young adult** — must screen for NMDAR-E; psychiatric admission often delays diagnosis
- **Negative serum antibodies** — does NOT exclude; CSF is gold standard (some patients serum-negative, CSF-positive)
- **Normal initial MRI** — common; absence doesn't rule out NMDAR-E
- **Improvement with treatment of "psychiatric" disorder** — does NOT mean it's not NMDAR-E; antipsychotics may modestly help
- **Post-HSV encephalitis behavioral change** — secondary NMDAR-E after HSV encephalitis is now well-recognized (5-10% of HSV cases)

## 8. Allowed citations

- `[Graus_2016]` — Graus F et al. A clinical approach to diagnosis of autoimmune encephalitis. Lancet Neurol 2016;15:391-404
- `[Dalmau_2011]` — Dalmau J et al. Clinical experience and laboratory investigations in patients with anti-NMDAR encephalitis. Lancet Neurol 2011;10:63-74
- `[Titulaer_2013]` — Titulaer MJ et al. Treatment and prognostic factors for long-term outcome in patients with anti-NMDA receptor encephalitis: an observational cohort study. Lancet Neurol 2013;12:157-165
- `[Schmitt_2012]` — Schmitt SE et al. Extreme delta brush: a unique EEG pattern in adults with anti-NMDA receptor encephalitis. Neurology 2012;79:1094-1100
- `[Dalmau_2018]` — Dalmau J, Graus F. Antibody-mediated encephalitis. NEJM 2018;378:840-851
- `[Lancaster_2016]` — Lancaster E. The diagnosis and treatment of autoimmune encephalitis. J Clin Neurol 2016;12:1-13
