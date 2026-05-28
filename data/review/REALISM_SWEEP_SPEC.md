# Realism Sweep Spec — de-leak NeuroBench v5 tool reports

> **AUTHORITY:** `dataset-generation/TOOL_REPORT_STYLE_GUIDE.md` is the governing
> standard (derived from ACR/RSNA, AANEM, ACNS, ASE, CAP, Mayo/ARUP). Where this
> spec and that guide differ, **the guide wins.** In particular, the guide KEEPS
> legitimate *within-modality* conclusions that this spec, if read literally, would
> wrongly strip: MRI/CT may name a diagnosis the imaging genuinely shows ("acute
> MCA infarct", "subarachnoid hemorrhage", "enhancing mass — high-grade neoplasm");
> EMG/NCS may say "consistent with a motor neuron disease"; neuropsychometry may
> commit to "probable bvFTD"/"amnestic MCI"; ECG/echo/monitoring are categorical;
> FDG-PET names a metabolic *pattern* (amyloid PET & DaTscan are strictly binary).
> The real leak targets are the guide's THREE PROHIBITIONS — no cross-modality
> synthesis, no differential-refutation essays, no management — plus the
> per-modality naming limits. Do NOT strip within-modality conclusions the guide
> allows. The detector below is only a rough pointer; the guide decides.

**The principle.** Every tool report must read like the real modality produced it.
It describes what *that test* shows, in the language of a real report. It must NOT
state the integrated final clinical diagnosis that the agent is supposed to
synthesize from the whole picture. The benchmark is broken if the MRI/PET/EEG/labs
hand the agent the answer.

The ground-truth answer lives in `ground_truth` — that block SHOULD name the
diagnosis (it is the answer key). **Never touch `ground_truth`, the patient body,
the exam, or any numeric finding/measurement.** You are only rewriting the
*interpretive free-text* of tool OUTPUTS.

## The one rule, stated three ways

- KEEP: findings, measurements, grades, and a **hedged, modality-level**
  interpretation or differential.
- REMOVE: any statement of the **integrated final clinical diagnosis** on a
  modality that cannot establish it; any editorializing that names the answer.
- Ask of every impression/interpretation: *"Could a radiologist / electrophysiologist /
  pathologist actually conclude this from THIS test alone, blinded to the rest of
  the workup?"* If no — rewrite it to what they could actually say.

## Worked examples (calibration — match these)

**KEEP (already correct — do not weaken):**
- MRI: `"Mild bilateral hippocampal atrophy (Scheltens MTA grade 1-2) with subtle
  temporoparietal volume loss ... could be age-related, though early
  neurodegenerative change cannot be excluded. Fazekas grade 2 small vessel disease."`
  → describes findings, hedged, does NOT say "Alzheimer's". Keep.
- MRI: `"Acute right MCA infarct ... multi-territory embolic pattern. No mycotic
  aneurysm on MRA."` → embolic *pattern*, does NOT say "infective endocarditis". Keep.

**FIX (leak — rewrite):**
- PET (before): `"FDG-avid right hilar mass, most consistent with primary small
  cell lung carcinoma; mesial temporal hypermetabolism compatible with
  paraneoplastic limbic encephalitis."`
  (after): `"Intensely FDG-avid right hilar mass (SUVmax 14.2) with bulky mediastinal
  nodes, highly suspicious for malignancy; tissue diagnosis required. Mild mesial
  temporal hypermetabolism, nonspecific."`
  → states the mass + that it needs biopsy; drops "small cell" and "paraneoplastic
  limbic encephalitis" (the integrated answer the agent must deduce).

## Per-modality guidance

- **Imaging (MRI / CT / PET / DaTscan / angiography / echo):** describe findings +
  a hedged imaging differential ("consistent with X vs Y", "suspicious for
  malignancy — tissue required"). Never state the final clinical syndrome that needs
  clinical/lab correlation, never name a paraneoplastic/autoimmune/etiologic label a
  scan can't prove. DaTscan may report "reduced striatal uptake" but not "Parkinson
  disease vs MSA vs PSP" as a verdict — those are clinical distinctions.
- **EEG / ECG / cardiac monitoring:** report the direct electro read — "frequent
  left temporal sharp waves", "atrial fibrillation", "3rd-degree AV block". Those
  ARE the modality's finding; keep them. Do NOT append "consistent with [the case's
  syndrome]" or name the cause.
- **Routine labs (`interpret_labs`):** report values, flag abnormals, may note a
  pattern ("macrocytic anemia", "transaminitis"). Do NOT name the unifying
  diagnosis in `interpretation`/`clinical_significance`.
- **Literature search (`search_medical_literature`):** must read like a real
  differential-driven query returning *general* evidence about candidate conditions.
  REMOVE phrasing that asserts the patient's own diagnosis ("confirms the patient
  has X", "diagnostic of this patient's X"). KEEP general clinical knowledge
  ("Awaji criteria count fasciculations as equivalent to fibrillations"). Don't
  over-edit — the fix is the confirmatory phrasing, not the topic.
- **CONFIRMATORY tests — KEEP the specific result (this is realistic and intended):**
  CSF Gram stain / culture / PCR (the organism), genetic panel (the mutation),
  specific autoantibody serology (e.g. anti-NMDAR positive, anti-Hu positive),
  biopsy histology. Ordering the confirmatory test in order to reveal its result is
  the whole point — report it as a lab result, not as "→ therefore diagnosis is X,
  start Y".

## Hard constraints

- Do NOT alter `ground_truth`, `patient`, `neurological_exam`, or any numeric
  finding / lab value / measurement / grade.
- Do NOT delete reports or blanket-normalize them — that changes the case. REWRITE
  the verdict text only.
- Preserve each file's unicode convention (escaped vs literal) with the helper:
  ```python
  import json; from pathlib import Path
  p = Path("data/neurobench_v5/cases/<CASE>.json"); raw = p.read_text()
  use_literal = any(ord(c) > 127 for c in raw); case = json.loads(raw)
  # ... mutate the interpretive field(s) ...
  p.write_text(json.dumps(case, indent=2, ensure_ascii=not use_literal) + "\n")
  ```
  (Surgical `Edit` on the exact string is also fine and preserves formatting.)

## Scope & self-verification (REQUIRED)

1. Start from the candidate list: `uv run python agent-platform/scripts/detect_answer_leakage.py --prefix <PREFIX>`
2. The detector UNDER-flags (finding-language leaks like the PET example are
   invisible to it). So ALSO read the `impression` / `interpretation` of every
   imaging / EEG / ECG / PET output and every literature `summary` in ALL your
   condition's cases, and fix any that name the integrated diagnosis.
3. After fixing, every touched case must:
   - `detect_answer_leakage.py --case <CASE>.json` → 0 candidate leaks (or, if a
     remaining hit is a legitimately-confirmatory result you intentionally kept,
     note it in your report).
   - `validate_ground_truth_coherence.py --case <CASE>.json` → still 0 issues.
   - validate against `NeuroBenchCase` schema.
4. Touch ONLY your condition's files.

Report: cases touched, count of fields rewritten, any field you deliberately KEPT
as a legitimate confirmatory result, and any case you flagged instead of fixing.
