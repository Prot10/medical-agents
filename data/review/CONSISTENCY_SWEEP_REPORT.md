# NeuroBench v5 cross-condition consistency sweep

**Cases reviewed:** 516
**Date:** 2026-05-26
**Conditions:** 20 (FND=40, NMDAR-ENC=36, SE=30, SAH=30, PERI-NEURO=30, MIG-AURA=30, GBS=30, ALS=30, NPH=25, MG=25, HEP-ENC=25, FTD=25, SYNC-CARD=20, PD=20, MS-RR=20, ISCH-STR=20, GLIO-HG=20, FEPI-TEMP=20, BACT-MEN=20, ALZ-EARLY=20)

---

## 1. Comorbidity handling

**AFib (22 cases across 10 conditions)** — Workup is inconsistent:
- ISCH-STR (8/8): full triad (ECG + Holter + Echo) in all cases — gold standard.
- GBS (2): ECG yes, Holter/Echo no.
- MG-P02, MIG-AURA-P02, SAH-M07, SAH-S04, SYNC-CARD-S01: partial workup (ECG±echo, no Holter).
- NPH (3), PD-RP02, SE (2), ALS-M03: AFib mentioned in case body but **no cardiac workup actions in optimal/critical** — AFib is treated as silent comorbidity. Decide policy: either AFib triggers a workup checklist regardless of index condition, or its presence in PMH is acceptable as background.

**HIV (9 cases)** — Workup varies:
- BACT-MEN (4 of 9): cryptococcal/TB workup, anti-retroviral checks — well-handled.
- ALS, FTD, GBS, GLIO-HG, SE (1 each): HIV is part of HPI but no consistent CSF JC-virus, CD4, viral-load workup directives.
- **Recommend:** standardize an HIV-aware sub-protocol callout (CD4, viral load, opportunistic infection differential) across all conditions where HIV is in PMH.

**Diabetes (145 cases)** — Largely background; only flagged in PERI-NEURO (23), where it correctly drives the workup. In MG (9), GBS (5), ALZ-EARLY (10), SE (7) cases the diabetic neuropathy contribution is rarely acknowledged in optimal_actions, even when EMG findings would be partly attributable.

**Cirrhosis (28 cases)** — 25 of 28 are HEP-ENC (expected). 3 spillovers: GBS, NPH, SE — these have Child-Pugh / MELD anchored cases. Check that ammonia, LFTs are at minimum in the optimal_actions for those 3 spillover cases.

**Anticoagulation (23 cases)** — Distributed across ISCH-STR (8), NPH (3), SAH (3), and 9 others. In SAH cases on anticoagulation, reversal is consistently in optimal_actions; in ISCH-STR, thrombolysis-exclusion logic is consistent. **However:** NPH-on-anticoagulation (3 cases) — no consistent guidance on whether to hold for LP/tap-test. Should be in sequence_constraints.

**Pregnancy (17 cases)** — Concentrated in NMDAR-ENC (4), ISCH-STR (3), FEPI-TEMP (2), MIG-AURA (2), PERI-NEURO (2). Contraindicated-medication lists are inconsistent: triptan/ergot avoidance present in MIG-AURA only; valproate-avoidance in FEPI-TEMP only sometimes; teratogenic-AED guidance variable across SE pregnancy cases.

**CKD/dialysis (24 cases)** — SYNC-CARD (6) reliably flags potassium / dialysis-related arrhythmia, ISCH-STR (6) flags contrast nephropathy for angiography. Other conditions (ALZ-EARLY, FTD, BACT-MEN, HEP-ENC, NMDAR-ENC, NPH, PERI-NEURO, SAH, SE — 12 cases total) inconsistently address renal dosing of antimicrobials / contrast considerations.

---

## 2. Tool classification consistency

**Within-case conflicts:** zero cases have the *same* (tool_name, tool_parameters) signature in both `optimal_actions` and `useless_tools` (no intra-case contradictions).

**Cross-case conflicts** — same (tool_name, tool_parameters) signature classified differently across cases. The validator-limitation note applies (the validator collapses by `tool_name` only) and most cross-case "conflicts" are actually expected because the modality is condition-appropriate in one and not in another. Notable signature-level conflicts to audit:

- `order_specialized_test test_type=emg_ncs`: optimal in ALS (30), GBS (30), PERI-NEURO (30), FTD (4); useless in ISCH-STR (20), NMDAR-ENC (36), SAH (30). Confirm useless-classification rationale documented for each. (Many MG case_body_concerns flag that this same signature is *required* for RNS/SFEMG and *useless* as a standalone NCS — the param `emg_ncs` is overloaded.)
- `order_specialized_test test_type=neuropsych_battery`: optimal in 101 cases (ALZ-EARLY, FEPI-TEMP, FTD, HEP-ENC, MIG-AURA, NPH, PD); useless in 4 SE cases (SE-M01, SE-M05, SE-P04, plus 1 other). **Recommend:** verify those 4 SE cases — is neuropsych truly useless during acute SE, or is this an oversight?
- `order_advanced_imaging modality=FDG_PET`: optimal in 96 cases (ALZ-EARLY, FEPI-TEMP, FTD, MG, NMDAR-ENC, NPH, PD, PERI-NEURO, SE); useless in 170 cases. The classification line is generally clinically sound, but boundary cases (FEPI-TEMP, MG, SE) have FDG-PET classified differently across subtypes — audit subtype-by-subtype.
- `order_advanced_imaging modality=amyloid_PET`: optimal in 67 (ALZ-EARLY, FTD, NPH); useless in 159 (ALS, BACT-MEN, HEP-ENC, NMDAR-ENC, SAH, SE). Consistent.
- `order_advanced_imaging modality=DaTscan`: optimal in 21 (FTD, PD); useless in 138 (broad). Note 1 FTD case has DaTscan as both — actually inter-case, not intra-case.
- `analyze_csf`: optimal in 79 cases across FEPI-TEMP, GBS, HEP-ENC, MIG-AURA, NPH, PERI-NEURO, SE; useless in 158 cases across FEPI-TEMP, FND, ISCH-STR, MG, MIG-AURA, PD, SYNC-CARD. **FEPI-TEMP and MIG-AURA appear on both sides** — these are subtype-dependent (LGI1-encephalitis FEPI-TEMP cases need CSF; ordinary mesial TLE doesn't). Verify the rationale is captured.
- `analyze_brain_mri`: optimal in 56 cases (HEP-ENC, NPH, SE); useless in 76 cases (GBS, MG, PERI-NEURO, SE, SYNC-CARD). SE-internal split: some SE cases require MRI (NCSE with cause-search), others useless. Confirm subtype rule.
- `order_specialized_test test_type=tilt_table`: optimal in PD-RP01 and SYNC-CARD-RS01; useless in SYNC-CARD-P03. Same condition, different classification — explain or normalize.

**Param-less (empty tool_parameters={}) signatures appearing on both sides** (`order_echocardiogram`, `order_ct_scan`, `order_cardiac_monitoring`, `analyze_eeg`, `analyze_ecg`, `analyze_brain_mri`) — these are expected cross-condition but require the validator fix to compare jointly with `tool_parameters`. Where the same `tool_name` with **the same empty params** appears in optimal in one condition and useless in another (e.g. `order_echocardiogram` optimal in MG/MIG-AURA/SAH = 30 cases, useless in 349), the classification logic is right but every "useless" entry should have a clinical rationale string (already present).

---

## 3. Citation consistency

**Hasbun_2001 (LP-before-imaging in mass effect / altered consciousness)** — Currently cited **only by GLIO-HG (20 cases)**. Missing from:
- BACT-MEN (0 / 20) — should cite Hasbun when LP timing/imaging-before-LP is in the gold trajectory.
- SAH (0 / 30) — usually relies on Connolly 2012 instead; consider if Hasbun is additionally appropriate when altered mental status complicates LP timing.
- NMDAR-ENC (0 / 36) — LP-before-imaging guidance is implicit but uncited.
- HEP-ENC (0 / 25) — LP is rarely indicated but when included, Hasbun citation would be appropriate.

**Cross-pack-shared citations to audit (clinically transferable):**
- `[Connolly_2012]` / SAH guidelines — used in SAH only (verify).
- `[Hughes_2014]` / GBS — confined to GBS pack.
- `[NICE_CG137]` / status epilepticus — confined to SE pack; could be referenced in FEPI-TEMP-RP cases that progress to SE.
- ICHD-3 citations — MIG-AURA only; ICHD-3 categorization is also relevant in some FND-PNES differential cases.

**Off-pack diagnoses (PD-P01/P02/P03/RP03 = MSA/DLB/PSP)** — Cited as `citation_gap` by the PD agent: `[Gilman_2008_MSA]`, `[McKeith_2017_DLB]`, `[Hoglinger_2017_PSP]`, `[Wenning_2022_MSA]` not in PD pack. Either extend the pack or rehome the cases (see §9).

**FND-P09 (Hashimoto SREAT)** — Needs `[Castillo_2006]` / `[Mocellin_2007]` (per the case's own citation_gap entry).

---

## 4. Difficulty calibration

Distribution (straightforward / moderate / diagnostic_puzzle) per condition:

| Condition | n | straightforward | moderate | puzzle |
|-----------|---:|---:|---:|---:|
| ALS | 30 | 7 (23%) | 13 (43%) | 10 (33%) |
| ALZ-EARLY | 20 | 8 (40%) | 6 (30%) | 6 (30%) |
| **BACT-MEN** | 20 | **0 (0%)** | 9 (45%) | **11 (55%)** |
| FEPI-TEMP | 20 | 5 (25%) | 7 (35%) | 8 (40%) |
| FND | 40 | 16 (40%) | 12 (30%) | 12 (30%) |
| **FTD** | 25 | **0 (0%)** | 18 (72%) | 7 (28%) |
| GBS | 30 | 9 (30%) | 9 (30%) | 12 (40%) |
| GLIO-HG | 20 | 8 (40%) | 6 (30%) | 6 (30%) |
| HEP-ENC | 25 | 5 (20%) | 12 (48%) | 8 (32%) |
| **ISCH-STR** | 20 | **1 (5%)** | 8 (40%) | **11 (55%)** |
| **MG** | 25 | **0 (0%)** | 18 (72%) | 7 (28%) |
| MIG-AURA | 30 | 4 (13%) | 16 (53%) | 10 (33%) |
| MS-RR | 20 | 8 (40%) | 4 (20%) | 8 (40%) |
| **NMDAR-ENC** | 36 | **0 (0%)** | 25 (69%) | 11 (31%) |
| NPH | 25 | 6 (24%) | 8 (32%) | 11 (44%) |
| PD | 20 | 5 (25%) | 9 (45%) | 6 (30%) |
| PERI-NEURO | 30 | 12 (40%) | 9 (30%) | 9 (30%) |
| SAH | 30 | 7 (23%) | 10 (33%) | 13 (43%) |
| SE | 30 | 13 (43%) | 9 (30%) | 8 (27%) |
| SYNC-CARD | 20 | 8 (40%) | 5 (25%) | 7 (35%) |

**Flagged calibration issues:**
- **BACT-MEN, FTD, MG, NMDAR-ENC have ZERO straightforward cases.** These conditions are systematically harder than peers. Consider adding 3–5 straightforward cases each (single-pathogen meningitis with classic Kernig/Brudzinski, classic bvFTD without atypical features, classic ocular MG, canonical NMDAR with teratoma in young woman with prodrome).
- **ISCH-STR has 1 straightforward case (5%)** — undercalibrated. The "easy" classic LMCA cardioembolic stroke from known AFib should be a straightforward template.
- Conditions with the heaviest puzzle skew (ISCH-STR 55%, BACT-MEN 55%, NPH 44%, SAH 43%) should be cross-checked against their straightforward complements.

---

## 5. Sequence constraint consistency

Counts of constraints per case (and severities):

| Condition | Cases with N constraints | Severities present |
|-----------|---|---|
| SAH | 3 in all 30 cases | hard:90 |
| ISCH-STR | 2 or 3 (all 20) | hard:22, soft:21 |
| SYNC-CARD | 2 or 3 (all 20) | hard:39, soft:6 |
| NMDAR-ENC | 2 in all 36 cases | hard:36, soft:36 |
| NPH | 2 in all 25 cases | hard:25, soft:25 |
| GLIO-HG | 2 in all 20 cases | hard:40 |
| BACT-MEN | 2 in all 20 cases | hard:40 |
| GBS | 2 in all 30 cases | soft:60 |
| HEP-ENC | 1 or 2 (all 25) | hard:29 |
| SE | 0, 1, or 2 (most 1–2) | hard:30, soft:12 |
| **FEPI-TEMP** | 1 in 18, 2 in 2 | soft:20, hard:2 |
| MG | 0 in 2, 1 in 23 | soft:23 |
| **MIG-AURA** | **0 in all 30** | none |
| **ALS** | **0 in all 30** | none |
| **FND** | **0 in all 40** | none |
| PERI-NEURO | 1 in 26, 2 in 4 | soft:34 |
| MS-RR | 1 in 20 | soft:19, hard:1 |
| PD | 1 in 2, 2 in 18 | soft:38 |
| FTD | 1 in 25 | soft:25 |
| ALZ-EARLY | 0 in 2, 1 in 18 | soft:18 |

**Issues:**
- **Imaging-before-LP** present in: BACT-MEN (20/20), GLIO-HG (20/20), HEP-ENC (1 or 2 per case all 25), NMDAR-ENC (36/36), SAH (3/3 per case all 30). **Consistent — good.**
- **MIG-AURA, ALS, FND have ZERO sequence_constraints across all cases.** ALS and FND may be defensible (no critical order), but MIG-AURA cases with first-episode brainstem aura should hard-constrain "imaging before triptan administration." ALS cases that initiate riluzole should soft-constrain "baseline LFTs before riluzole start."
- **Hard-severity overuse:** SAH has 90 hard constraints across 30 cases (3 per case). NMDAR-ENC has 36 hard, NPH 25 hard. Is "imaging-before-LP" really hard for NMDAR-ENC when most cases are young women without mass effect? Audit if some should be soft.
- **SAH constraint count (3 per case) is twice the median.** Audit whether all three are truly hard or if one could be soft.

---

## 6. Critical action overlap

**Most-duplicated critical_actions (verbatim across many cases of the same condition) — strong candidates for lifting into structured `optimal_actions` or the criteria pack:**

| Count | Condition | Critical action (verbatim) |
|---:|---|---|
| 39 | FND | "Document at least one positive rule-in sign (Hoover, tremor entrainment, distractibility, give-way, midline split)" |
| 39 | FND | "Obtain brain MRI to exclude structural pathology" |
| 39 | FND | "Communicate the diagnosis transparently using positive language and the rule-in signs as the basis" |
| 39 | FND | "Refer for FND-informed physiotherapy and CBT / psychological therapy" |
| 39 | FND | "Order a comprehensive neuropsychological battery..." |
| 36 | NMDAR-ENC | "Send paired CSF and serum for anti-NMDAR (GluN1) IgG..." |
| 36 | NMDAR-ENC | "Start empiric IV acyclovir 10 mg/kg q8h until CSF HSV-1/2 PCR returns negative" |
| 36 | NMDAR-ENC | "Initiate first-line immunotherapy promptly (IV methylprednisolone + IVIG or PLEX)" |
| 36 | NMDAR-ENC | "Control seizures aggressively (LEV/VPA), continuous EEG for NCSE" |
| 30 | ALS | "Perform EMG/NCS sampling bulbar + ≥2 spinal regions..." |
| 30 | ALS | "Obtain brain MRI to exclude structural mimics..." |
| 30 | ALS | "Order a mimic-exclusion lab panel..." |
| 30 | ALS | "Measure baseline respiratory function (FVC, MIP/MEP, SNIP)" |
| 30 | ALS | "Apply Awaji-Shima 2008 / Gold Coast 2020 criteria" |
| 30 | ALS | "Initiate riluzole 50 mg twice daily after baseline LFTs..." |
| 30 | ALS | "Refer to a multidisciplinary ALS clinic..." |
| 30 | SAH | 7 distinct actions, all appearing in 30/30 cases (CT, CTA, nimodipine, neurosurgical consult, NCC admission, sodium monitoring, TCD) |
| 28 | NMDAR-ENC | "Screen for ovarian teratoma..." |
| 25 | FND | "Obtain video-EEG capturing a habitual event..." |

These are template critical_actions that should be either (a) absorbed into the criteria-pack's required-actions list at the pack level (eliminating per-case copies) or (b) acknowledged as standardized template language. Currently they duplicate identical text across 25–39 cases per condition.

**Within-condition wording variants (normalization candidates):**

- **SE**: 7 variants of "Administer IV lorazepam 0.1 mg/kg first-line" (with/without "—"; "do NOT delay"/"do not delay"). Pick one canonical wording.
- **FEPI-TEMP**: 8 variants of "Counsel on driving restrictions" (occupation-specific tails). Normalize core sentence + appended modifier.
- **MG**: 7 variants of "Confirm AChR antibody positivity" (with/without modifier "binding 8.7 nmol/L", "binding/blocking/modulating", "overturns CPEO label"). Normalize.
- **GBS**: 10 variants of "Initiate IVIG 0.4 g/kg/day for 5 days" (with PLEX alternative or hepatic-function caveat). Normalize.
- **GBS**: 5 variants of "Initiate IVIG / plasma exchange" — the shorter wording.
- **PD**: 3 variants of "Initiate carbidopa-levodopa or dopamine agonist first-line" (with/without "as", "therapy").
- **PD**: 3 variants of "Aggressively treat orthostatic hypotension".
- **MIG-AURA**: 3 variants of "Brain MRI/MRA required for first ..." (motor aura / brainstem aura / exercise-triggered).
- **GLIO-HG**: 4 variants of "Administer dexamethasone (loading dose 10 mg IV, then 4 mg q6h)" with different qualifier tails (midline shift size).

---

## 7. Contraindicated action / harmful_tools alignment

**Coverage:** `contraindicated_actions` is populated in 100% of cases (516/516). `harmful_tools` is sparse.

| Condition | n | with harmful_tools | with contraindicated_actions |
|-----------|---:|---:|---:|
| ALS | 30 | 0 (0%) | 30 (100%) |
| ALZ-EARLY | 20 | 0 (0%) | 20 (100%) |
| BACT-MEN | 20 | 2 (10%) | 20 (100%) |
| FEPI-TEMP | 20 | 0 (0%) | 20 (100%) |
| FND | 40 | 0 (0%) | 40 (100%) |
| FTD | 25 | 0 (0%) | 25 (100%) |
| GBS | 30 | 0 (0%) | 30 (100%) |
| **GLIO-HG** | 20 | **20 (100%)** | 20 (100%) |
| HEP-ENC | 25 | 0 (0%) | 25 (100%) |
| ISCH-STR | 20 | 1 (5%) | 20 (100%) |
| MG | 25 | 0 (0%) | 25 (100%) |
| MIG-AURA | 30 | 1 (3%) | 30 (100%) |
| MS-RR | 20 | 0 (0%) | 20 (100%) |
| NMDAR-ENC | 36 | 0 (0%) | 36 (100%) |
| NPH | 25 | 0 (0%) | 25 (100%) |
| PD | 20 | 0 (0%) | 20 (100%) |
| PERI-NEURO | 30 | 0 (0%) | 30 (100%) |
| **SAH** | 30 | **16 (53%)** | 30 (100%) |
| SE | 30 | 2 (7%) | 30 (100%) |
| SYNC-CARD | 20 | 1 (5%) | 20 (100%) |

**Major issue: `harmful_tools` is empty for almost every condition except GLIO-HG (100%) and SAH (53%).** The "validator-limitation" notes in many cases suggest agents moved harmful intent into `contraindicated_actions` (free-text) because they could not encode a (tool_name, tool_parameters) signature without a validator collision. With the validator now fixed, these should be put back.

**Specific candidates for re-encoding `contraindicated_actions` → `harmful_tools`:**
- **BACT-MEN (20 cases)** — LP-before-imaging in mass-effect cases. 18 of 20 cases have LP in optimal but no harmful_tools entry. Only BACT-MEN-RM03 has explicit mass-effect language. Encode `analyze_csf` with `tool_parameters={"timing":"before_imaging"}` as harmful where applicable, OR add a generic `order_ct_scan first` sequence-constraint.
- **NMDAR-ENC (36 cases)** — All 36 have LP in optimal_actions and zero have harmful_tools entries. For cases where mass effect or papilledema are present, LP-before-imaging should be in harmful_tools.
- **HEP-ENC (25 cases)** — 0 harmful_tools entries; cases with raised ICP risk should flag LP-before-imaging.
- **MIG-AURA** — triptans/ergots contraindicated in hemiplegic migraine and aneurysm cases are in `contraindicated_actions` only; should also be in harmful_tools via `check_drug_interactions` proposed_drug.
- **MG** — neuromuscular-blocking drugs, beta-blockers, fluoroquinolones flagged in contraindicated_actions only; should be in harmful_tools.
- **PD on dopamine antagonists** (PD-M01..M03 + others) — metoclopramide / antipsychotic worsening — currently text only.

**Inconsistent drug-class contraindication encoding (same drug class flagged in one case, not in equally-relevant peer):**
- Neuromuscular-blocking agents in MG-RM cases: contraindication is present in some MG cases (RM11–RM15 crisis cases) but not consistently elsewhere.
- Fluoroquinolones (cipro in particular): explicit in MG-RM11 (ciprofloxacin trigger of crisis) but not flagged across other MG cases where it could equally precipitate.
- Lactulose/rifaximin avoidance in non-HEP-ENC vs. lactulose in HEP-ENC — inconsistent rationale strings.
- Anticoagulant initiation in SAH (clear) vs ISCH-STR-cardioembolic with hemorrhagic transformation risk (variable timing rules).

---

## 8. Subtype naming consistency

**Diagnosis-string variance per condition (lower is better):**

| Condition | Distinct primary_diagnosis strings | Note |
|-----------|---:|---|
| MS-RR | 2 | Excellent — most uniform |
| PD | 9 | Mostly canonical + 4 atypical (see §9) |
| NPH | 10 | Good |
| NMDAR-ENC | 11 | Mostly subtype tails |
| GLIO-HG | 11 | One CNS-lymphoma outlier (see §9) |
| BACT-MEN | 15 | Many bacterial agents — expected |
| SYNC-CARD | 16 | High; lots of mechanism qualifiers |
| FTD | 19 | Mostly bvFTD subtypes |
| ISCH-STR | 19 | Vessel/territory tails |
| MG | 25 | One per case — wording highly variable |
| HEP-ENC | 25 | One per case — variable West Haven grade tails |
| SAH | 27 | One per case — aneurysm site / complication tails |
| ALS | 28 | Many variants of "ALS, [variant]" with different tails |
| MIG-AURA | 29 | Highly variant |
| PERI-NEURO | 30 | One per case (heterogeneous nosology — expected) |
| SE | 30 | One per case (etiology-driven — expected) |
| FND | 38 | Highly variant — see normalization below |
| FEPI-TEMP | 20 | One per case |

**ALS:** "Amyotrophic lateral sclerosis (ALS), bulbar-onset" vs "ALS, bulbar-onset, clinically definite" vs "Amyotrophic lateral sclerosis, flail-arm variant (Vulpian-Bernardt syndrome)" — pick a canonical schema like "ALS, {onset-region}-onset, {certainty}". Standardize across the 28 strings.

**FND:** 38 strings for 40 cases — extreme variance. Examples: "Functional neurological symptom disorder (conversion disorder) with mixed symptoms — psych..." vs "Functional neurological disorder — right-sided functional hemimotor syndrome..." Some say "conversion disorder", some don't. Some prepend "Functional neurological symptom disorder", some "Functional neurological disorder". Pick one parent term (DSM-5: "Functional neurological symptom disorder (conversion disorder)") and append subtype.

**ALZ-EARLY:** The standalone string "Early-stage Alzheimer's disease (mild dementia, amnestic)" (8 cases) vs "Mild cognitive impairment due to Alzheimer's disease (amnestic, multi-domain)" (4 cases) vs "Mild cognitive impairment due to Alzheimer's disease (amnestic, multi-domain), early-onset" (1 case) — these distinct stages should be consistent across M/S/RM/RS subtypes. Most "S" subtype cases use "early-stage AD" while "M" uses "MCI". Verify that S = symptomatic AD and M = MCI is the documented intent.

**NMDAR-ENC:** 26 cases use the bare string "Anti-NMDA receptor encephalitis", others append tumor sites / triggers. Acceptable, but the "with X teratoma" variants are inconsistently formatted ("with left ovarian teratoma" vs "triggered by right ovarian mature teratoma"). Normalize.

**SAH:** "Aneurysmal subarachnoid hemorrhage from {site} aneurysm (Hunt-Hess X, Fisher Y)" — most cases follow this. A few drop the grading tail. Normalize: always include Hunt-Hess and Fisher.

---

## 9. Cross-condition mis-prefixed cases (rehoming candidates)

**Explicit rehoming requests in case_body_concerns (7 cases):**

| case_id | Filed condition | Actual primary diagnosis | Recommended action |
|---|---|---|---|
| **FND-P09** | FND | Hashimoto's encephalopathy (SREAT) | Rehome to a new `AUTOIMM-ENC` or `SREAT` bucket, or move to NMDAR-ENC bucket as "antibody-negative autoimmune encephalitis" |
| **GLIO-HG-P02** | GLIO-HG | Primary CNS lymphoma (EBV-DLBCL) in HIV/AIDS | Rehome to a `CNS-LYMPHOMA` bucket or accept as a "glioma-mimic acceptance" case |
| **NMDAR-ENC-RP01** | NMDAR-ENC | Post-COVID seronegative autoimmune encephalitis (NMDAR antibody negative) | Rehome to `AUTOIMM-ENC-SERONEG` or revise case body to show positive NMDAR antibody |
| **PD-P01** | PD | Multiple system atrophy, parkinsonian type (MSA-P) | Rehome to `MSA` bucket or accept as PD-mimic R-cohort |
| **PD-P02** | PD | Dementia with Lewy bodies (DLB) | Rehome to `DLB` bucket or accept as PD-mimic R-cohort |
| **PD-P03** | PD | Progressive supranuclear palsy, Richardson syndrome (PSP-RS) | Rehome to `PSP` bucket or accept as PD-mimic R-cohort |
| **PD-RP03** | PD | MSA-P/C overlap | Rehome to `MSA` bucket or accept as PD-mimic R-cohort |

**Additional likely rehoming candidates flagged by primary-diagnosis-vs-condition-prefix mismatch (no concern declared but worth review):**

| case_id | Filed condition | Primary diagnosis | Comment |
|---|---|---|---|
| ALS-P02 | ALS | Familial ALS, C9orf72 expansion, early symptomatic | Acceptable — still ALS, just familial |
| ALS-P08 | ALS | Familial ALS, SOD1 A4V | Acceptable — still ALS, just familial |
| ALS-P09 | ALS | ALS-FTD spectrum disorder, C9orf72 | Borderline — spans ALS and FTD; flag for cross-pack |
| ALS-S10 | ALS | Familial ALS, C9orf72, young-onset | Acceptable |
| SE-P04 | SE | Acute left MCA ischemic stroke with post-ischemic lateralized periodic discharges / post-reperfusion seizures | Primary mechanism is stroke; SE is the manifestation. Borderline — could be ISCH-STR with seizure complication |
| FEPI-TEMP-P02 | FEPI-TEMP | (Per agent flag) Drug-resistant focal cortical dysplasia | Within scope — flagged as "atypical pediatric" |
| FEPI-TEMP-P03 | FEPI-TEMP | LGI1 antibody-mediated autoimmune (limbic) encephalitis with FBDS | Borderline — autoimmune encephalitis. Consider rehoming to NMDAR-ENC pack as "non-NMDAR autoimmune encephalitis" |
| PERI-NEURO-S05 | PERI-NEURO | Subacute combined degeneration of the spinal cord (B12) | Borderline — myelopathy, not peripheral neuropathy. Rehome? |
| PERI-NEURO-M05 | PERI-NEURO | EGPA / Churg-Strauss with vasculitic mononeuritis multiplex | Acceptable — peripheral neuropathy variant |

**NMDAR-ENC outlier cases (per agent concern, but currently "tolerated"):**
- NMDAR-ENC-RP02 (checkpoint-inhibitor-associated NMDAR — tumor logic reversed)
- NMDAR-ENC-RP03 (post-HSV NMDAR encephalitis — well-recognized but uncoded entity in the pack)

**Total rehoming-candidates short list (priority): 11 cases** — FND-P09, GLIO-HG-P02, NMDAR-ENC-RP01, PD-P01, PD-P02, PD-P03, PD-RP03, SE-P04, FEPI-TEMP-P03, PERI-NEURO-S05, ALS-P09.

---

## 10. Validator-limitation patterns

**115 cases flag the validator limitation in their case_body_concerns** ("validator flags `order_advanced_imaging` in both optimal and useless — distinct modalities of the same catchall tool. Known systemic validator limitation"). This is fixed at the validator level — agents do **not** need further action.

**However, some agents moved harmful intent into `contraindicated_actions` (free-text) that should now go back into `harmful_tools`** with proper signatures. See §7 — the entire pattern is the same as the harmful_tools gap. Specifically:

- **MG cases**: contraindicated drug classes (NMBs, fluoroquinolones, aminoglycosides, beta-blockers, magnesium) should be encoded as `check_drug_interactions` with `tool_parameters.proposed_drug` in `harmful_tools`.
- **MIG-AURA cases**: triptans / ergots in hemiplegic migraine, basilar migraine, and unruptured aneurysm cases should be in `harmful_tools`.
- **GLIO-HG**: already done (100% coverage).
- **SAH**: 53% already done — extend to remaining 14 cases.
- **NMDAR-ENC**: LP-before-imaging in mass-effect-positive cases should be in harmful_tools (currently in free-text contraindicated_actions only).
- **PD**: dopamine-receptor antagonists (metoclopramide, antipsychotics) should be in harmful_tools.

**33 cases flagged "missing fallback_tool_outputs"** — useless_tools entries were removed because fallback outputs are missing. With the validator now permitting these, agents need to add the fallback_tool_outputs entries (PD-P02, PD-P03, etc.).

**14 cases flagged "missing initial/followup outputs for required tool"** — required tools were demoted to recommended; restore them after adding the followup_outputs (most PD-P0X cases).

---

## Summary: top remediation candidates (priority order)

1. **Rehome 7 confirmed mis-prefixed cases** (PD-P01/P02/P03/RP03, FND-P09, GLIO-HG-P02, NMDAR-ENC-RP01) — either move to appropriate (or new) condition prefix, or convert to explicit "mimic" R-cohort cases with rationale.
2. **Calibrate difficulty** for BACT-MEN, FTD, MG, NMDAR-ENC (0% straightforward) — add 3–5 canonical-textbook straightforward cases each.
3. **Fix ALS followup-output tool wiring** (30 cases): genetic panel routed via `interpret_labs` → should be `order_specialized_test` with `test_type=genetic_panel:ALS`. Documented per-case fix.
4. **Move contraindicated-actions → harmful_tools** systematically: MG (25), MIG-AURA (30), PD (20), NMDAR-ENC with mass-effect (~6), BACT-MEN/HEP-ENC LP-before-imaging-in-mass-effect cases.
5. **Add `phase_contrast_MRI` and `extended_lumbar_drain_trial` to TOOL_PARAMETER_VOCABULARY.md** (21 + 12 NPH cases reference them).
6. **Normalize primary_diagnosis wording**: FND (38→5), ALS (28→8), MIG-AURA (29→10), MG (25→8). Pick canonical schema per condition.
7. **Add Hasbun_2001 to BACT-MEN, SAH, NMDAR-ENC, HEP-ENC criteria packs** for LP-timing citations.
8. **Add MSA/DLB/PSP citations** (`Gilman_2008`, `McKeith_2017`, `Hoglinger_2017`, `Wenning_2022`) — needed only if PD-P0X cases stay in PD pack.
9. **Audit and add sequence_constraints** for MIG-AURA (currently 0): imaging-before-triptan-for-first-aura; for ALS: baseline-LFTs-before-riluzole.
10. **Normalize within-condition critical_action wording**: SE lorazepam (7 variants), FEPI-TEMP driving counsel (8 variants), GBS IVIG dosing (10 variants), MG AChR confirmation (7 variants).
11. **Lift template critical_actions into criteria pack** where they are verbatim across all 25–39 cases (FND, NMDAR-ENC, ALS, SAH) — eliminates 200+ duplicate strings.
12. **Restore demoted required tools and removed useless_tools** for the 33+14 cases (PD-P0X cluster mostly) by adding the missing followup_outputs / fallback_tool_outputs entries.
13. **Add hard sequence_constraint reduction**: SAH (3 hard/case is excessive — demote 1 to soft), NMDAR-ENC (audit hard:36 to see if any are situational).

---

## Aggregated metadata flags

### case_body_concerns (across all 516 cases)

- **Total cases with concerns:** 191 / 516 (37%)
- **Total concern entries:** 307 (mix of strings and dicts; schemas: `{concern, field_path, suggested_fix}` = 30; `{detail, issue, proposed_fix}` = 4; `{case_id, issue, proposed_fix}` = 4; `{issue, proposed_fix, tools_affected}` = 3; `{issue, proposed_fix, removed_useless}` = 2; remaining 264 = plain strings)
- **Concerns by condition (top):** FTD 71, GBS 61, SAH 37, MIG-AURA 35, ALS 30, FEPI-TEMP 24, ISCH-STR 13, GLIO-HG 11, BACT-MEN 10, PD 9, NMDAR-ENC 4, FND 1, PERI-NEURO 1. **HEP-ENC, ALZ-EARLY, MG, MS-RR, NPH, SE, SYNC-CARD = 0 concerns declared.**

**Concern themes (cases that match each):**
- 102 uncategorized (likely the per-case validator-limitation stubs — benign)
- 64 criteria_pack_citation_gap (mostly the validator limitation referencing FDG_PET / amyloid_PET / modality-specific advanced imaging)
- 60 vocab_gap_referenced (NPH phase_contrast, MG emg_ncs, etc.)
- 33 missing_fallback_tool_outputs (PD-P0X cluster + a few SAH)
- 30 tool_wiring_to_wrong_tool_name (ALS genetic-panel cluster)
- 25 validator_param_signature_limitation (MG cluster)
- 14 missing_tool_outputs_for_required (PD-P0X cluster)
- **7 primary_diagnosis_vs_condition_mismatch** (rehoming list)

### Rehoming candidates (final list)

| case_id | Proposed condition / action |
|---|---|
| FND-P09 | AUTOIMM-ENC (SREAT) bucket, or relabel as FND-mimic R-case |
| GLIO-HG-P02 | CNS-LYMPHOMA or HIV-CNS bucket, or relabel as glioma-mimic R-case |
| NMDAR-ENC-RP01 | AUTOIMM-ENC-SERONEG bucket, or fix case body to positive NMDAR antibody |
| PD-P01 | MSA-P bucket, or relabel as PD-mimic R-case |
| PD-P02 | DLB bucket, or relabel as PD-mimic R-case |
| PD-P03 | PSP-RS bucket, or relabel as PD-mimic R-case |
| PD-RP03 | MSA bucket, or relabel as PD-mimic R-case |
| ALS-P09 | ALS-FTD spectrum (cross-pack); accept or split |
| SE-P04 | Possibly ISCH-STR (stroke is primary; seizure is manifestation) |
| FEPI-TEMP-P03 | NMDAR-ENC-like (LGI1 autoimmune); consider |
| PERI-NEURO-S05 | Myelopathy / spinal cord bucket (subacute combined degeneration is central, not peripheral) |
| NMDAR-ENC-RP02 | Accept (checkpoint-inhibitor associated NMDAR — uncoded but recognized entity) |
| NMDAR-ENC-RP03 | Accept (post-HSV NMDAR — recognized entity) |

### vocab_gap (vocabulary additions to consider)

Aggregated from 63 entries across 54 cases:

| Cases | Proposed vocabulary addition |
|---:|---|
| 25 | **Validator fix**: compare `(tool_name, tool_parameters)` jointly so `order_specialized_test:emg_ncs` (useless) and `order_specialized_test:RNS` / `order_specialized_test:SFEMG` (required) can coexist. Affects 25 MG cases. *Already fixed per task brief.* |
| 21 | **`phase_contrast_MRI` modality** for `order_advanced_imaging` (NPH CSF flow studies). Affects all 21 NPH cases referencing it. |
| 12 | **`extended_lumbar_drain_trial`** as a `test_type` for `order_specialized_test` (NPH 72h ELD trial). |
| 1 | **`genetic_panel:wilson`** (ATP7B) for `order_specialized_test`. HEP-ENC-P04. Placeholder `genetic_panel:CADASIL` was used incorrectly. |
| 1 | **`lip_biopsy` / `minor_salivary_gland_biopsy`** for `order_specialized_test`. PERI-NEURO-M04 (Sjögren). |
| 1 | **`chest_HRCT`** and **`PFTs`** as `order_advanced_imaging` / `order_specialized_test` types. PERI-NEURO-P03 (anti-synthetase ILD). |
| 1 | **`genetic_panel:porphyria`** (HMBS/ALAS1/CPOX/PPOX). PERI-NEURO-P06. |
| 1 | **`genetic_panel:small_fiber_neuropathy`** (SCN9A/SCN10A/SCN11A, GLA Fabry). PERI-NEURO-RP12. |

**Recommend adding to TOOL_PARAMETER_VOCABULARY.md (priority order):**
1. `phase_contrast_MRI` modality
2. `extended_lumbar_drain_trial` test_type
3. `genetic_panel:wilson`
4. `lip_biopsy` (or `minor_salivary_gland_biopsy`) test_type
5. `genetic_panel:porphyria`
6. `genetic_panel:small_fiber_neuropathy`
7. `chest_HRCT` modality (also relevant to GBS post-respiratory cases)
8. `PFTs` clarification (currently subsumed under `respiratory_function`)

### citation_gap (citation additions to consider)

Aggregated from 5 entries across 5 cases:

| Source case | Proposed citations | Recommendation |
|---|---|---|
| FND-P09 (Hashimoto SREAT) | `[Castillo_2006]`, `[Mocellin_2007]` | Add to FND pack only if FND-P09 stays; otherwise rehome and drop |
| PD-P01 (MSA-P) | `[Gilman_2008_MSA]`, `[Wenning_2022_MSA]` | Add to PD pack if PD-P01 stays; otherwise rehome |
| PD-P02 (DLB) | `[McKeith_2017_DLB]` | Add to PD pack if PD-P02 stays; otherwise rehome |
| PD-P03 (PSP-RS) | `[Hoglinger_2017_PSP]` | Add to PD pack if PD-P03 stays; otherwise rehome |
| PD-RP03 (MSA overlap) | `[Gilman_2008_MSA]`, `[Wenning_2022_MSA]` | Same as PD-P01 |

**Recommendation: rehome the 5 atypical-parkinsonism / SREAT cases rather than extending PD/FND packs.** Atypical parkinsonisms and Hashimoto SREAT have distinct gold trajectories; extending the PD pack with MSA/DLB/PSP citations would dilute the pack identity and force PD agent prompts to differentiate at runtime.

---

*End of consistency sweep report. 516 cases analyzed; 7 explicit rehoming candidates + 6 borderline candidates identified; 33 vocabulary additions across 8 themes; 5 citation additions tied to rehoming decisions; 12 systemic remediation themes ranked by priority.*
