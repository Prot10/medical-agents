# v5 Realism Sweep — Report

Removes **answer-leakage** from tool reports so each reads like the real modality
and does not hand the agent the diagnosis. Re-enforces the existing research-backed
`dataset-generation/TOOL_REPORT_STYLE_GUIDE.md` (ACR/RSNA, AANEM, ACNS, ASE, CAP)
across all 516 v5 cases.

After this sweep: coherence 516/516, schema 516/516, vocab 516/516, tests 161/161.

## Why this was needed

A prior realism pass existed, but (a) leaks remained, and (b) the immediately
preceding coherence sweep **re-introduced** leaks in some authored outputs — the
clearest being PERI-NEURO-RP11's FDG-PET stating "small cell lung carcinoma;
paraneoplastic limbic encephalitis" (a PET cannot establish either; that is
cross-modality synthesis). That regression triggered this sweep.

## Two kinds of leakage

- **Kind 1 — cross-modality / verdict leakage (removed everywhere).** A report that
  reaches outside its own test to announce the integrated answer: citing other
  tests/genetics/exam, refuting the differential, or prescribing management.
- **Kind 2 — within-modality naming (KEPT, per decision below).** A report naming a
  diagnosis its own test legitimately establishes (MRI "acute MCA infarct"; CT
  "subarachnoid hemorrhage"; EMG "consistent with a motor neuron disease";
  neuropsych "probable bvFTD").

## How the sweep ran

20 per-condition expert agents, each reading every tool report in its cases and
rewriting Kind-1 leaks to modality-faithful language while preserving objective
findings, measurements, and **confirmatory results** (CSF Gram stain/organism,
genetic mutations, autoantibody titers, biopsy histology — revealing these is the
point of ordering the confirmatory test). The committed detector
`agent-platform/scripts/detect_answer_leakage.py` is a candidate pointer only; the
style guide decides. Detector candidates fell 139→102 cases; the residual is
deliberately-kept confirmatory results + general (population-keyed) literature.

## The within-modality decision

The fleet initially diverged: imaging kept its diagnoses, but neuropsych/EMG were
over-stripped (my sweep instructions were stricter than the guide). **Resolved in
favor of keeping within-modality naming** (guide-compliant, realistic, consistent,
and matching the benchmark's integration-testing intent). The ~31 stripped
neuropsych ("probable bvFTD"/"amnestic MCI") and EMG ("consistent with a motor
neuron disease") conclusions were restored across FTD (24), ALZ-EARLY (4), and ALS
(3) — while the ALS **El Escorial/Awaji ALS categorization stays stripped** (it
cites clinical UMN signs → Kind-1 cross-modality), left as electrodiagnostic-only.

## Guardrails honored

No `ground_truth`, `patient`, `neurological_exam`, or any numeric finding / score /
measurement was altered — only interpretive free-text. Each file's unicode
convention preserved; differentials remain likelihood-sorted; coherence stayed 0
throughout.

## Net change

136 case files across 19 conditions carry realism edits. (24 FTD cases whose only
edit was the neuropsych over-strip reverted cleanly once that was restored — they
had no genuine leak.)
