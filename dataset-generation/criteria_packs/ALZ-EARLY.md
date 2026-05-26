# Criteria pack: Alzheimer's disease, early / MCI due to AD

**ICD-10:** G30.0 (early-onset), F02.80 (with behavioral disturbance), G31.84 (MCI)
**Condition enum:** `NeurologicalCondition.ALZHEIMERS_EARLY`
**Case ID prefix:** `ALZ-EARLY`

---

## 1. Diagnostic criteria

NIA-AA 2018 research framework reclassifies AD biologically by ATN status:
A (amyloid: positive amyloid PET OR CSF Aβ42/Aβ40 ratio reduced), T (tau:
elevated CSF p-tau or tau PET positive), N (neurodegeneration:
hippocampal/medial-temporal atrophy on MRI, FDG-PET hypometabolism in
parietotemporal regions, or elevated CSF total tau). Clinical "early AD"
= MCI or mild dementia phenotype + A+T+ biomarker profile. NIA-AA 2011
clinical criteria still used in non-research practice (probable AD by
clinical features + supportive biomarkers).

## 2. Standard workup hierarchy

**Required:**
- `order_specialized_test` (`test_type: neuropsych_battery`) — episodic memory deficit + ≥1 other cognitive domain; baseline + tracking [NIA_AA_2011]
- `analyze_brain_mri` (volumetric protocol) — medial temporal atrophy + exclude vascular, hippocampal sclerosis, NPH [NIA_AA_2011]
- `interpret_labs` (TSH, B12, CMP, CBC; consider HIV/RPR if risk) — exclude reversible mimics [AAN_dementia_2018]

**Recommended:**
- `analyze_csf` (`Abeta42, phospho_tau, total_tau`) — biomarker profile for ATN classification (research/specialty centers) [NIA_AA_2018]
- `order_advanced_imaging` (`modality: amyloid_PET`) — when CSF biomarkers unavailable or diagnostic uncertainty after clinical+MRI [Appropriate_Use_Amyloid_PET]
- `order_advanced_imaging` (`modality: FDG_PET`) — when AD vs FTD distinction unclear (FDG pattern differentiates) [Foster_2007]
- `search_medical_literature` — confirm biomarker thresholds, treatment options

**Optional:**
- `check_drug_interactions` — for cholinesterase inhibitor or memantine initiation
- `order_specialized_test` (`test_type: genetic_panel:early_onset_AD`) — onset <60 with family history [Bateman_2012]

## 3. Tools that are typically USELESS

- `analyze_eeg` — non-specific in AD; not part of routine workup
- `analyze_ecg` — unrelated to dementia workup
- `order_echocardiogram` — unrelated
- `order_cardiac_monitoring` — unrelated
- `order_ct_scan` — MRI is preferred; CT only if MRI contraindicated
- `order_advanced_imaging` (`modality: DaTscan`) — useless unless parkinsonism present (DaTscan rules out DLB, not AD per se)
- `order_advanced_imaging` (`modality: MR_spectroscopy / perfusion_MRI`) — research only

## 4. Tools that are HARMFUL / contraindicated

(none — workup is largely non-invasive; LP is safe if not contraindicated by mass effect)

## 5. Sequence constraints

- `analyze_brain_mri` → `analyze_csf` (`soft`): exclude mass effect before LP; particularly important in older patients with focal signs [NIA_AA_2011]

## 6. Subtype variations

- **M (mild):** subtle MCI, memory-predominant; standard workup, biomarkers helpful but not required
- **S (standard):** typical amnestic MCI / mild AD; standard workup as listed
- **P (progressive):** rapid progression (suspect CJD if very rapid), atypical features (PCA, lvPPA, frontal variant); add amyloid PET + FDG-PET; consider 14-3-3 / RT-QuIC if very rapid
- **R (reverse / mimic):** reversible cognitive decline (depression, B12 deficiency, hypothyroidism, NPH, medications, sleep apnea); workup emphasizes exclusion labs + neuropsych + sleep evaluation if indicated

## 7. Common red-herring categories

- **Hippocampal atrophy in elderly** — present in normal aging too; must be assessed quantitatively (Scheltens scale ≥2)
- **Low B12 with cognitive decline** — does NOT exclude AD; both can coexist
- **Family history of "dementia"** — vague; sporadic AD is common
- **Normal MMSE** — preserved in early MCI; MoCA more sensitive
- **APOE4 status** — risk factor, not diagnostic

## 8. Allowed citations

- `[NIA_AA_2011]` — McKhann GM et al. Diagnosis of dementia due to Alzheimer's disease. Alzheimers Dement 2011;7:263-269
- `[NIA_AA_2018]` — Jack CR et al. NIA-AA Research Framework: Toward a biological definition of AD. Alzheimers Dement 2018;14:535-562
- `[AAN_dementia_2018]` — Petersen RC et al. Practice guideline update: Mild cognitive impairment. AAN, Neurology 2018;90:126-135
- `[Appropriate_Use_Amyloid_PET]` — Johnson KA et al. Appropriate use criteria for amyloid PET. Alzheimers Dement 2013;9:e-1-16
- `[Foster_2007]` — Foster NL et al. FDG-PET improves accuracy in distinguishing FTD and AD. Brain 2007;130:2616-2635
- `[Bateman_2012]` — Bateman RJ et al. Clinical and biomarker changes in dominantly inherited AD. NEJM 2012;367:795-804
