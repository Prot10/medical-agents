# NeuroBench v5 — Full Clinical Audit Summary (2026-07-06)

Exhaustive field-by-field audit of **all 600 v5 cases across all 20 conditions**, run
condition-by-condition in 6 rounds via a multi-agent workflow (1 terminology agent +
10 deep-audit agents + 1 report writer per condition), plus targeted back-fill agents.
Triggered by clinician feedback on the "Early Alzheimer's" label; scope expanded to a
complete terminology + clinical-correctness + internal-consistency + realism audit.

Per-condition detail is in the sibling `{CONDITION}.md` files.

## Post-audit validation gates
- **Schema:** 600 / 600 pass (`NeuroBenchCase`).
- **Coherence:** 579 / 600 pass; the **26 residual issues are ALL one systematic pattern**
  — a tool listed in `ground_truth.useless_tools` with no matching `fallback_tool_outputs`
  entry (21 cases). No other coherence category remains ⇒ the ~330 applied fixes introduced
  **zero regressions**.

## Totals across the 6 rounds
- **~2,040 findings** (≈ 480 major, 0 open blockers — the 2 blockers found were auto-fixed or flagged).
- **~330 objective corrections applied** (mechanical + objective ICD/nomenclature), each
  verified against the case's own data + the official standard, re-validated after edit.
- **~480 major items flagged** for clinician adjudication (ground-truth-meaning changes we
  deliberately did NOT auto-edit).

## The clinician's finding, generalized and fixed
The "Early Alzheimer's" issue was **one instance of a dataset-wide failure mode**: a
condition/case label asserting an onset, severity, variant, or intractability the case's own
data contradicts. Confirmed and fixed at config/README/criteria-pack level:

| Condition | Was | Now | Why |
|---|---|---|---|
| ALZ-EARLY | "Early-stage Alzheimer's disease", ICD G30.0 | **"Alzheimer's disease", G30.9** | G30.0 = onset <65; cohort is mostly ≥65. Per-case codes recoded by onset (G30.0 <65 / G30.1 ≥65 / G31.84 MCI). |
| GBS | "Guillain-Barré syndrome (AIDP)" | **"Guillain-Barré syndrome"** | Set includes Miller-Fisher, AMAN, AMSAN, PCB variants. Age [20,70]→[15,85]. |
| FTD | "Behavioral variant frontotemporal dementia" | **"Frontotemporal dementia"** | Set includes svPPA, nfvPPA. |
| MIG-AURA | "Migraine with typical aura" | **"Migraine with aura"** | Set includes hemiplegic, brainstem, retinal, migrainous-infarction. |
| NPH | "Normal pressure hydrocephalus (idiopathic NPH)" | **"Normal pressure hydrocephalus"** | 4 cases are secondary NPH. |
| SAH | "Aneurysmal subarachnoid hemorrhage" | **"Subarachnoid hemorrhage"** | Includes a non-aneurysmal case. |

## ICD-10-CM currency fixes (web-verified against FY2025/FY2026 updates)
- **MS-RR:** flat `G35` retired 2025-10-01 → **G35.A** (RRMS). Config/README/pack reconciled; 30 cases already correct.
- **PD:** flat `G20` non-billable parent → per-case children (**G20.A1** untreated, **G20.A2** fluctuations, **G20.B2** dyskinesia+fluctuations). 26 cases recoded; canonical set to G20.A1.
- **GLIO-HG:** WHO-2016 "anaplastic astrocytoma" → WHO-2021 "Astrocytoma, IDH-mutant, CNS WHO grade 3" (case + pack).
- **FEPI-TEMP:** wrong seizure family `G40.109` (simple/focal-aware) → `G40.209` (complex-partial); 21 treatment-naïve cases recoded `G40.219`(intractable)→`G40.209`.
- **ALS:** removed invalid "young-onset" qualifier (age >45); pack threshold `<50`→`<45`.
- **BACT-MEN:** organism-specific fixes (Staph G00.8→G00.3; meningococcal miscoded pneumococcal G00.1→A39.0); "Lancet stage"→"MRC grade"; pack G03.9→G00.9.
- **FND:** F44 subtype fixes (F44.7↔F44.5↔F44.4 by symptom-category count).

## Systematic dataset-wide items — recommend a single dedicated cleanup pass
1. **`useless_tools` without `fallback_tool_outputs`** — 21 cases / 26 issues (the only remaining coherence failures). Fix: add a normal-negative fallback output or drop the tool from `useless_tools`.
2. **CTA `contrast_used=false`** on contrast angiography outputs → set `true` where `angiography=true`.
3. **MOGAD differential coded `G36.9`** → `G37.81` dataset-wide.
4. **PD tilt-table / other duplicated-unit strings** ("…mmHg … mmHg", "…bpm … bpm") — partially fixed (PD); sweep the rest.
5. **CSF interpretation template artifacts** — `(N/A PMN/N/A lymph)` placeholder; duplicated `(ratio 0.5x)`.
6. **Tool-vocabulary gaps** — `phase_contrast_MRI` / CSF-flow, cardiac MRI (mislabeled `perfusion_MRI`), extended lumbar drainage, `exercise_stress_test` doc row.
7. **`FollowUpToolOutput` union-misresolution** — a *code* bug flagged by the prior (May) audit (unkeyed Pydantic union silently resolving followup outputs to an empty wrong-typed object). Confirm whether still live; higher-impact than any single case.

## Top clinician-adjudication items (ground-truth meaning — need a neurologist)
- **ISCH-STR-S01:** lesion/exam laterality incoherent (left MCA infarct but all left-sided deficits).
- **SAH copy-paste cluster:** EVD-for-"acute hydrocephalus" critical actions in cases whose CT shows NO hydrocephalus (M06, M08); red-herrings referencing a migraine history the patient lacks (M02, M08); CSF-as-harmful-tool contradictions (M05, M06).
- **NMDAR-ENC:** occupation/narrative mismatches (teacher template on non-teachers); M03 MRI/EEG laterality mismatch; M05 unilateral findings vs bilateral impression; P04 subtype (labeled severe, clinically mild); "young women/teratoma" prose on older-adult patients.
- **Atypical-variant boilerplate:** amnestic-AD reasoning on PCA/lvPPA cases; "no cerebrovascular burden" differential text contradicted by Fazekas-2 MRIs (ALZ, others).
- **PD-P02 (DLB) / PD-P03 (PSP):** non-PD mimics filed under the PD prefix, citing only PD-pack references.
- **SYNC-CARD-M04:** drug-induced long-QT coded to the wrong drug class (antidysrhythmic) when culprits are an SSRI/macrolide.

All changes are staged in the working tree (uncommitted). Per-condition tables: `data/review/audit/{CONDITION}.md`.
