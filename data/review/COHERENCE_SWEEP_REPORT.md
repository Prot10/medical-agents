# v5 Coherence Sweep — Report

Closes the case-body coherence gaps left after the gold-trajectory regen. After
this sweep, `validate_ground_truth_coherence.py` reports **0 issues across all 516
v5 cases** (was 224), with schema (516/516), vocab (516/516), and the test suite
(161/161) all green.

## Scope

126 cases across 8 conditions had gaps. Two gap classes:

- **Serious (91):** a tool marked `required` in `optimal_actions` had no stored
  output, so the mock server returned a hard error when an agent obeyed the gold.
- **Soft (133):** a tool in `useless_tools` had no `fallback_tool_outputs` entry,
  so calling it errored instead of returning a realistic off-pathway result.

## How they were closed

**Soft (133) — normal fallbacks authored.** Every useless off-pathway tool now has
a NORMAL / non-contributory report in `fallback_tool_outputs` (advanced_imaging, ct,
specialized_test, mri, echo, cardiac_monitoring, eeg). No pathology was placed in any
fallback — an off-pathway test must read as unremarkable.

**Serious (91) — reclassify-or-author, decided per case.**

- **~77 `required` → `recommended` downgrades.** `search_medical_literature` and
  `check_drug_interactions` were systematically over-classified by the regen fleet
  (empty `tool_parameters`, `medications: []`, generic queries, empty rationale).
  These are decision-support tools, not must-calls, so they were downgraded. In a
  few conditions the downgrade was applied across the full condition set for
  internal consistency, not only to the flagged cases.

- **28 genuinely-required on-pathway outputs authored,** each consistent with the
  case's diagnosis, exam, and existing outputs:
  - **CSF** (PERI-NEURO P04/S04/RM11): albuminocytologic dissociation for
    demyelinating / radiculoplexus neuropathy.
  - **Neuropsych batteries** (FTD M05/M07/M08/P02/P04/P06): bvFTD signature built
    from each patient's own MoCA / Trails B / fluency / recall.
  - **tPA contraindication drug screens** (ISCH-STR M03/P01/P02/P03/S01/S03): kept
    `required` because each sits in a HARD `order_ct_scan → check_drug_interactions`
    sequence constraint modeling the thrombolysis gate; outputs name the real drug
    (alteplase) and are patient-specific (P03 infective endocarditis → tPA
    contraindicated, Class III-Harm).
  - **Cardiac monitoring** (ISCH-STR P02/P03/RM01/RM02): yield matched to the
    embolic source (AF where documented, normal where young/dissection).
  - **Advanced imaging** (PERI-NEURO RP11 FDG-PET → occult SCLC; ISCH-STR P03 MRA →
    mycotic aneurysm).
  - **Head CT** (BACT-MEN P02/P03 reflecting each patient's hydrocephalus; MG-RM14
    normal chest CT excluding thymoma in drug-triggered crisis).
  - **Drug-interaction reports** (FTD-P01 valproate → hyperammonemic-encephalopathy
    mimic; PERI-NEURO-M06 leflunomide-induced SFN; MIG-AURA-P03 sumatriptan;
    MIG-AURA-P05 warfarin).

## Guardrails honored

- No `primary_diagnosis`, `chief_complaint`, `history_present_illness`, `icd_code`,
  `condition`, or `difficulty` field was altered (verified by diff scan).
- Diffs are additive and surgical; each file's original unicode convention preserved.
- Differentials remain sorted by likelihood descending.

## Known limitation (logged, not blocking)

The mock server resolves `order_specialized_test` and `order_advanced_imaging` to a
single output slot regardless of `test_type` / `modality`. A case requiring two
distinct tests of the same tool (e.g. FTD-P02/P04: neuropsych_battery +
genetic_panel:FTD) can only return one; the second is delivered via an
`interpret_labs` followup and the limitation is noted in `metadata.case_body_concerns`.
A future mock-server fix should key these outputs by `test_type` / `modality`.
