# Criteria pack: Frontotemporal dementia (bvFTD, semantic, non-fluent variants)

**ICD-10:** G31.09 (frontotemporal lobar degeneration)
**Condition enum:** `NeurologicalCondition.FTD`
**Case ID prefix:** `FTD`

---

## 1. Diagnostic criteria

Rascovsky 2011 (bvFTD): ≥3 of 6 core features in first 3 years: early
behavioral disinhibition, apathy/inertia, loss of empathy, perseverative/
stereotyped behaviors, hyperorality/dietary changes, executive dysfunction
with relative sparing of memory and visuospatial. "Probable bvFTD" requires
clinical criteria + functional decline + frontotemporal atrophy/hypometabolism;
"Definite" adds pathology or known FTD-causing mutation. Gorno-Tempini 2011
for PPA variants: nfvPPA (agrammatism, effortful speech), svPPA (impaired
single-word comprehension, surface dyslexia), lvPPA (impaired word retrieval,
sentence repetition deficits — usually AD pathology).

## 2. Standard workup hierarchy

**Required:**
- `order_specialized_test` (`test_type: neuropsych_battery`) — frontal executive deficits, behavioral inventory, language profile; differentiates from AD (memory-predominant) [Rascovsky_2011]
- `analyze_brain_mri` — frontal/anterior temporal atrophy, lobar pattern; rule out other causes [Rascovsky_2011]
- `interpret_labs` (TSH, B12, CMP, RPR/HIV per risk) — exclude reversible causes [AAN_dementia_2018]
- `search_medical_literature` — criteria, treatment evidence

**Recommended:**
- `order_advanced_imaging` (`modality: FDG_PET`) — frontotemporal hypometabolism; useful when MRI atrophy subtle or when distinguishing from AD [Foster_2007]
- `order_specialized_test` (`test_type: genetic_panel:FTD`) — family history positive or young onset; C9orf72 most common, then GRN, MAPT [Pottier_2016]
- Specialist referral *(clinical action — `tool_name: null`, no tool call)* — behavioral/cognitive neurology

**Optional:**
- `analyze_csf` (`Abeta42, phospho_tau, total_tau`) — distinguishes FTD from AD when amyloid PET unavailable
- `order_advanced_imaging` (`modality: amyloid_PET`) — negative supports FTD; positive does not exclude AD-FTD overlap
- `check_drug_interactions` — for symptomatic treatment (SSRIs for behavior, etc.)

## 3. Tools that are typically USELESS

- `analyze_eeg` — non-specific in FTD; not routine
- `analyze_ecg` — unrelated
- `order_echocardiogram` — unrelated
- `order_cardiac_monitoring` — unrelated
- `order_ct_scan` — MRI preferred
- `order_advanced_imaging` (`modality: DaTscan`) — useless unless parkinsonism present (FTD-MND, PSP-FTD overlap)
- `order_advanced_imaging` (`modality: MR_spectroscopy / perfusion_MRI / carotid_duplex`) — none indicated

## 4. Tools that are HARMFUL / contraindicated

(none routinely)

## 5. Sequence constraints

- `analyze_brain_mri` → `analyze_csf` (`soft`): exclude structural cause of focal cognitive symptoms before LP

## 6. Subtype variations

- **M (mild):** subtle behavioral changes or word-finding difficulty; standard workup, lower-yield biomarkers
- **S (standard):** clinical syndrome meeting Rascovsky criteria; standard workup
- **P (progressive):** rapid cognitive decline, motor features (FTD-ALS, FTD-CBS); add EMG for ALS overlap, DaTscan if parkinsonism, genetic panel for C9orf72
- **R (reverse / mimic):** mood disorder, AD with atypical frontal presentation, vascular cognitive impairment, autoimmune encephalitis (anti-LGI1 with hyperexcitability syndrome can mimic FTD), late-onset psychiatric illness, prion disease (CJD); workup adds autoimmune encephalitis panel, vascular imaging, 14-3-3/RT-QuIC if rapid

## 7. Common red-herring categories

- **Memory complaints in FTD** — often present but secondary; primary deficit is executive/behavioral
- **Family member reports "depression"** — apathy in FTD often mistaken for depression
- **Normal MRI early** — can be normal in first 1-2 years; FDG-PET more sensitive early
- **Negative family history** — most FTD is sporadic (only ~30% genetic)
- **Stable cognitive testing** — bvFTD has disproportionate behavioral decline relative to cognitive scores

## 8. Allowed citations

- `[Rascovsky_2011]` — Rascovsky K et al. Sensitivity of revised diagnostic criteria for the behavioural variant of frontotemporal dementia. Brain 2011;134:2456-2477
- `[Gorno_Tempini_2011]` — Gorno-Tempini ML et al. Classification of primary progressive aphasia and its variants. Neurology 2011;76:1006-1014
- `[Foster_2007]` — Foster NL et al. FDG-PET improves accuracy in distinguishing FTD and AD. Brain 2007;130:2616-2635
- `[AAN_dementia_2018]` — Petersen RC et al. Practice guideline update: MCI. AAN 2018
- `[Pottier_2016]` — Pottier C et al. Genetics of FTLD: an update and 2016 perspective. Curr Opin Neurol 2016;29:710-718
- `[Bang_2015]` — Bang J et al. Frontotemporal dementia. Lancet 2015;386:1672-1682
