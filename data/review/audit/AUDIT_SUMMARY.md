# NeuroBench v5 — Full Case Audit Summary

Exhaustive field-by-field audit of all 516 v5 cases via the `neurobench-case-audit`
skill — one expert auditor per condition, every field of every case read against the
condition criteria pack, the tool-report style guide, and the schema. Per-condition
detail in the sibling `{CONDITION}.md` files.

**Post-audit gates:** coherence 516/516, schema 516/516, vocab 516/516, tests 161/161.
**Auto-fixed:** ~95 unambiguous mechanical errors across ~94 case files (see below).
**Flagged for human/clinician adjudication:** ~400+ findings, ~100 major.

## Headline integrity findings (systematic, dataset-wide)

### 1. Followup-output union misresolution — REAL functional bug (77 cases, 126 outputs)
`FollowUpToolOutput.output` is an unkeyed Pydantic union. Followup outputs stored with
the wrong shape (a `{"general": {...}}` wrapper, or a literature result missing
top-level `query`/`summary`, or `findings` as strings) fail to match their intended
model and **silently resolve to an all-optional model — usually an empty
`CardiacMonitoringReport`.** ~95 of these carry real `search_medical_literature` /
`check_drug_interactions` content that is **lost at runtime**: an agent calling that
tool in those cases receives an empty wrong-typed object. Invisible to every validator
(the JSON is well-formed and schema-valid). **Fix = discriminated union keyed on
`tool_name` (code) + reshape the malformed outputs (data).** First found via GBS-RS18
and MG-S01.

### 2. Orphan keys (mostly harmless duplicates; minor exam loss)
53 cases carry flat legacy keys (`patient.age/sex/hpi/pmh`, top-level
`vitals`/`physical_exam`/`red_herrings`) **alongside** the populated canonical fields —
harmless duplication, not data loss (verified). Genuine minor loss: ~24 exam
`special_tests`/`special_signs` subfields are silently dropped (no canonical home;
should fold into `neurological_exam.additional`). NMDAR-ENC M04–M08 `sensation`→`sensory`
silent drop already fixed.

### 3. Detector-blind Kind-1 leakage inside specialized_test / imaging free-text
The leak detector skips `specialized_test`; the realism sweep therefore missed
within-`specialized_test` and some imaging essays that still do the agent's work:
EMG differential-refutation essays (ALS), MS-RR repeat-MRI "now meets McDonald
criteria", FND MRI disease-exclusion lists, several CT/MRI `additional_observations`.
A handful were stripped during the audit; the class needs a targeted second realism
pass scoped to these fields.

### 4. Case-body answer-leakage (HPI / exam free-text)
Distinct from tool reports: some HPIs/exam `additional` fields pre-state the etiology,
numbered differential, or management (e.g. an SE HPI reading "BENZODIAZEPINE-RESISTANT
SE from isoniazid toxicity"; PERI-NEURO/MG records naming the gold diagnosis). The
patient presentation should not contain the answer.

## Recurring mechanically-fixable classes (most auto-fixed; some dataset-wide remain)
- **Doubled units/words** ("bpm bpm", "% %", "L L", "µm µm", "seconds seconds",
  "percentile percentile", "cells/uL cells/uL", "dB HL dB HL") — generator artifact in
  ~12+ conditions; fixed where audited, but a global sweep would finish it.
- **`is_abnormal=true` on normal/negative results** (negative gene panels, in-range
  values flagged "(H)") and **H/L flag-direction errors** in `abnormal_values_summary`.
- **Unit typos** (CRP mg/dL→mg/L, ethanol mg/dL→g/dL, TSH mIU/mL→mIU/L).
- **enum-vs-text contradictions** (EEG `classification:"normal"` under an "ABNORMAL EEG"
  impression — fixed in MIG-AURA/SE; ECG rate-vs-rhythm "tachycardia" mislabels).
- **Derived-value arithmetic** (CSF glucose-ratio recomputed in MS-RR/ALZ; Holter
  `duration_hours` self-contradictions in ISCH-STR).

## Clinician-adjudication flags (NOT auto-fixed — judgment / clinical meaning)
- **Laterality errors** (serious): ISCH-STR-S01 (left-MCA imaging + left-body deficits —
  internally impossible; flagged blocker), S03/S04 gaze direction; PD DaTscan deficit
  ipsilateral to worse side (4 cases); FTD-M06; FEPI-TEMP-RM01. A left/right
  consistency pass (imaging↔exam↔reasoning) is recommended before clinician review.
- **Copy-paste / template contamination**: GLIO-HG-M02 pregnancy + age in a 47-yo male;
  7 male NMDAR cases with "ovarian teratoma / women of reproductive age" reasoning;
  phantom metoclopramide in 4 PD ground_truths; fabricated penicillin-allergy boilerplate
  (BACT-MEN/FEPI-TEMP); SAH-M06/M08 mandating EVD "for hydrocephalus" their CT denies;
  NPH-P07 "breast cancer" in a prostate-cancer patient.
- **Gold-answer / criteria calls**: PD-RP02 (idiopathic PD over an MSA-P picture),
  PD-RS03; GLIO-HG-RP03 (low-grade tumor in the high-grade set with GBM management);
  NPH-M07/P04 (sub-threshold imaging/tap); HEP-ENC-M05 (zinc-excess premise);
  GBS-RM13 (6-wk course vs GBS window); SE-M02 (LEV "subtherapeutic" but therapeutic).
- **`harmful_tools` vs populated/critical tool**: `analyze_csf` listed harmful while LP
  is the populated confirmatory test / a critical action (SAH ×5, BACT-MEN-P02/P03).
- **`consult_medical_specialist` tiering**: marked `required` widely vs criteria-pack
  `recommended`; also absent from the documented 12-tool roster. Dataset-wide decision.
- **R-subtype taxonomy**: criteria packs define "R" as a non-disease mimic, but most
  R-cases are real-seeded confirmed cases of the index disease. Pack docs vs composition
  disagree (ALS, SAH, FND, ALZ-EARLY, MS-RR…). Reconcile.
- **Mimic prefixing**: PD-P01/P02/P03/RP03 (atypical parkinsonism), GLIO-HG-P02 (PCNSL),
  NMDAR-ENC-RP01 (seronegative), FND-P09 (SREAT), several MIG-AURA — confirm intended.
- **Missing serious competitors** in some differentials; **ICD-code** over-coding
  (FEPI-TEMP G40.219 on non-intractable cases; MIG-AURA ICHD-3 1.2.1.1→1.2.1.2).

## Per-condition auto-fix tally
ALS 0 · ALZ-EARLY 9 · BACT-MEN 9 · FEPI-TEMP 7 · FND 2 · FTD 1 · GBS 2 · GLIO-HG 3 ·
HEP-ENC 2 · ISCH-STR 3 · MG 13 · MIG-AURA 3 · MS-RR 16 · NMDAR-ENC 5 · NPH 3 · PD 0 ·
PERI-NEURO 10 · SAH 1 · SE 6 · SYNC-CARD 0.

## Recommended next actions (in priority order)
1. **Fix the followup union bug** (code: discriminated union on `tool_name`; data:
   reshape the ~126 malformed outputs). Highest impact — it corrupts runtime data.
2. **Global mechanical sweep** for the remaining doubled-units / is_abnormal / unit-typo
   classes (safe, scriptable).
3. **Targeted realism pass** on `specialized_test`/imaging free-text (Kind-1 essays) and
   HPI/exam case-body leakage.
4. **Clinician adjudication** of the flag categories above (laterality, gold-answer,
   harmful-CSF, tiering, R-taxonomy, mimic prefixing) — the items only a clinician should
   decide, ahead of the external validation round.
