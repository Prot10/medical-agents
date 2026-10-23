# Cross-condition work still to do (October 2026 round)

Kept by the orchestrating session so a resumed session does not lose it. Remove an item when it
lands.

## Code and tests
- Scorer: a mixed case can score both diagnoses only by recoding (it accepts a diagnosis on its
  ICD code alone). Consider a per-case "all of" diagnosis rule. (HEP-ENC-P04, 24 Oct)
- Test: catch fallback outputs that can never be served. (HEP-ENC, 24 Oct)
- `analyze_csf.source`: an EVD sample is billed as a lumbar puncture; only shunt/EVD criteria may
  name `source`. (vocabulary agent, 24 Oct)

## Guidance claims
- `test_guidance_claims`: the ALZ-EARLY (CSF, amyloid PET, FDG) and GBS (brain MRI) claims fail
  until those conditions finish; update the response in
  `agent-platform/scripts/review/build_condition_tool_guidance.py`, regenerate with `--write`,
  and update the claim table in the same change. (24 Oct)

## Vocabulary follow-ups
- Other conditions citing "WHO 2025 Annex A.4" should read "section A.4" (the guideline has no
  Annex A.4).

## Synonym prune effects on later batches
- `apply_diagnosis_synonyms --prune` would change MIG-AURA-P03, MIG-AURA-P07, SE-P04 (lose "stroke"
  and mechanism labels) and SE-P07 (loses "hepatic coma", K72.91); `--check` adds I63.5/I63.51 to
  SE-P04. Apply when those conditions run.
- ALZ-EARLY prune diffs predate the batch-1 synonym change.

## For the physicians at re-review
- ISCH-STR-RS02: thrombolysis reversed to "give" (its CTA excludes aortic extension, R2's own
  condition for withholding). Tell R2.
- ISCH-STR-S06 was never physician-reviewed.
- AHA/ASA 2026 contraindication table is paywalled: confirm the class of prior ischaemic stroke
  within 3 months (ISCH-STR-RM01) and aPTT > 40 s without anticoagulant (ISCH-STR-RP04).
- Scoring changes: ALS-P08 rejects a plain "ALS" (Z15.89), ALS-P02 credits Graves, HEP-ENC-P04
  coded as Wilson disease.

## Guard failures left in later batches (24 Oct)
- Leak guard: VASC-DEM 30, GBS 25, NMDAR-ENC 18, MIG-AURA 13, SE 10, SYNC-CARD 10, NPH 9, SAH 7,
  FTD 6, MG 6, FND 5, GLIO-HG 5, MS-RR 4, FEPI-TEMP 3, PD 2. Follow-up guard: GBS 4, FTD 1.
  Workers see the rule in PATTERNS.md section 5.
