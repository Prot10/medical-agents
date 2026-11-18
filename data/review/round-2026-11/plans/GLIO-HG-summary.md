# GLIO-HG: condition audit summary, November 2026 round (17 Nov 2026)

Auditor pass over all 30 GLIO-HG cases after the workers and verifiers. Plan: `GLIO-HG.md`, decisions
`GLIO-HG-decisions.md` (D1 to D11). Scratch scripts: `work/scratch/glio-auditor/` (`classes.py`,
`callos.py`, `leak.py`, `leak_out2.py`, `ddi.py`, `ddi_ctx.py`, `xmod.py`, `rulings_check.py`,
`fix_stragglers.py`, `logs_append.py`).

## Notes and rulings

- 10 notes, all from R2 (NB-87MF-FBTV-TPWE), in S02 to S06. Each note id is in exactly one
  `work/rulings/<CASE>.json` file, under the right case. No id is missing, duplicated or extra, and
  every status is valid.
- Counts: FIXED 5 (36546be3 S02, 35803946 S03, f465277d S04, 1e375c3a S05, a1f18356 S06) and
  ALREADY-FIXED 5 (b63e4af9 S02; 4022233f S03, 365d96f2 S04, c011f7ee S05 and f987e3d1 S06 by
  class MRI-CONTRAST, commit 71517e55).
- DECLINED as a whole: none. Two notes were declined in part. The reasons are logged in their rulings:
  - 35803946 (S03): the PCNSL likelihood stays very_low. Ruling 7 says likelihood is the view at
    assessment time, and the tissue shows glioblastoma. Before tissue, a thick necrotic ring with
    rim-only restriction is atypical of PCNSL (EANO PCNSL 2015). The `key_features` now name the
    callosal extension. The display question is CENTRAL 3.
  - a1f18356 (S06): the treatment must is a discussion of Stupp versus Perry, not a switch.
    EANO 2021 keeps 70 as the cut-off, and Perry 2017 makes the short course an option from 65.
- NEEDS-ANDREA: none.
- Approved cases: no GLIO-HG case is in `work/approved.txt`, so no approved case was changed.
- Label and code changes: none. `accepted[0]` and `icd_codes[0]` are unchanged in all 30.

## Classes: counts before and after

| class | before (at plan) | after workers | after audit | how fixed |
| --- | --- | --- | --- | --- |
| C1 MRI-CONTRAST (D1) | 0 of 30 unpaired | 0 | 0 | already fixed in 71517e55 |
| C2 FIELD-LOCALISATION (D2) | 3 (P04, S02, S04) | 0 of the planned 3 | 0; the audit found and fixed 2 more (M01, M02) | the MRI names the visual-pathway segment |
| C3 ANTIPLATELET-TIMING (D5) | 5 aspirin cases with no interval (P03, RM01, S02, S04, S05) and 1 NSAID case with no must (P05) | 0 | 0 | variant A or B must; P05 NSAID must; RM04, RP01, RP04 and RS05 already compliant |
| C4 FMRI-UNSCORED (D6) | 1 (S05) | 0 | 0 | recommended criterion, soft constraint, pathway order, must |
| C5 DIFFERENTIAL-CALLOSAL (D7) | 2 (S03, M04) | 0 | 0 | PCNSL `key_features` |
| C6 CALLOSAL-RESECTION (D8) | 3 (S03, M04, M05) | 0 of the planned 3 | 0; the audit found and fixed 1 more (RP04) | callosal clause in the surgery must |
| C7 TREATMENT-65-70 (D9) | 1 (S06) | 0 | 0 | discussion must; key evidence item 7 |
| C8 VENTRICLE-ENTRAPMENT (D10) | 3 (S02 partly covered, S03, S06) | 0 | 0 | entrapment must, or the S02 clause |
| C9 CBC / assays / KPS (D3, D4) | 0 | 0 | 0 | already fixed in October |
| Audit: drug-interaction output names the diagnosis | 3 (P05, RM02, RS03: "high-grade glioma") | 3 | 0 | clause removed, interaction content kept |
| Audit: turn-0 text names the entity | 1 (M04: "IDH-mutant gliomas") | 1 | 0 | wording removed |

Uniform application was checked with scripts over all 30 cases:
- Canonical must texts are present where the plan places them: variant A in RM01, S04 and S05;
  variant B in S02 and P03; the P05 NSAID must; the S03 and S06 entrapment musts; the S02 clause;
  the S06 discussion; the M04, M05 and S03 callosal clause.
- Every case that takes aspirin or an NSAID (meds or HPI) has a matching must, and no other case has
  one.
- Every positive ventricular obstruction (P05, RM01, RM03, S02, S03, S06) has management.
- Every sequence constraint names existing ids.
- Every stop rule lists exactly the required criteria. `max_additional_actions` is 0 in all 30.
- No literature criterion or stored literature output remains (class LIT).
- No new em dashes.

## Stragglers fixed by the auditor (logged in each case log)

- M01, M02 (C2):
  - The stored perimetry shows a right superior homonymous quadrantic defect, the exam records a
    subtle or subjective upper-quadrant defect, and the DTI puts Meyer loop in the temporal-stem
    oedema. Neither MRI study named the visual pathway.
  - Both MRI studies now name "the temporal stem (Meyer loop)" in the FLAIR finding and in the
    impression.
  - This goes beyond the lead's NO-ACTION for M01 (a "questionable" defect). The reason is that D2
    requires the MRI to agree with the perimetry and the DTI, and here both report the defect.
  - `mri_probe.py`: clean.
- RP04 (C6): the dominant mass's own `location` field extends into the splenium (tumour, not only
  oedema). The surgery must now adds "recognizing that the extension into the splenium of the corpus
  callosum limits the safe extent of resection". The resection report already says subtotal.
- P05, RM02, RS03 (leak): the `check_drug_interactions` follow-up is served to any interaction query,
  and its VTE warning said "high-grade glioma", which is an accepted label. The diagnosis clause is
  removed and the interaction stays.
- M04 (leak): past medical history said "No family history of brain tumors, IDH-mutant gliomas, ...",
  which names the entity class at turn 0. It now reads "No family history of brain tumors or
  hereditary cancer syndromes".

Cases changed since 06b74446 beyond the cross-condition classes:
- 16 cases: M01, M02, M04, M05, P03, P04, P05, RM01, RM02, RP04, RS03, S02, S03, S04, S05 and S06.
- Each has a log with `## Changes` and `## Verification`.
- The other 14 cases changed only through MRI-CONTRAST and the red-herring pointer follow-up, and
  their logs have `## Class changes` only.

## Blind leak pass (scripts and reading)

- Turn 0 (`format_patient_info`, which includes the medication indications) shows no accepted label
  and no case-sensitive acronym in any of the 30 cases.
  - P02's "likely GBM" is the referral error of a lymphoma case, so it is a red herring, not its own
    diagnosis.
  - RM02's childhood optic glioma is NF1 history.
  - The prior non-contrast CT results in the HPI are legitimate: no case scores `order_ct_scan`.
- Drug-interaction outputs (initial, follow-up and fallback):
  - After the fixes, none names the diagnosis or repeats any `expected_evidence` (checked in
    40-character windows).
  - Generic mentions remain: temozolomide, chemotherapy, "neuro-oncology". They are statements about
    interactions, and a mass is already known at turn 0 from the CT. Left as they are.
- Cross-modality synthesis:
  - No report cites another modality.
  - MRI impressions give imaging differentials, which the style guide allows.
  - Perfusion reports cite an "rCBV high-grade glioma threshold > 1.75" reference in 7 cases. That
    is the modality's own reference, so it is Kind 2 and kept.

## CENTRAL requests (consolidated)

1. `dataset-generation/criteria_packs/GLIO-HG.md` section 9:
   - add `[Frontera_2016]` (Neurocrit Care 2016;24:6-46);
   - extend the `[ESC_NCS_2022]` scope to "aspirin stopped at least 7 days before intracranial
     neurosurgery";
   - add the aspirin rule to section 6.

   The musts of S02, S04, S05, P03 and RM01 already cite Frontera 2016.
2. `costs.yaml` `interpret_labs`: add a `platelet_function` panel (PFA-100 or VerifyNow aspirin), with
   a library normal and the `tool_io.py` mirror. The aspirin musts say "platelet function testing
   where available", and that test cannot be ordered today.
3. web-review CaseDetail: label the differential likelihood "assessment-time likelihood (after the
   work-up)" and say that the labelled diagnosis is not listed (R2, S03).
4. Outside GLIO-HG:
   - VASC-DEM-S11 has a field defect that its MRI does not localise (C2 class).
   - 26 of 278 CBC or BMP sets in other conditions have MCHC or anion gap out of range
     (`work/scratch/glio-lead/labs_chk.py`).

## Check results (after the audit fixes)

- `perfect_agent.py`: 30/30 pass, one id per call.
  - RM02 and RM03 each print the warning "action-dna-methylation-profiling answered with the same
    stored report as action-10".
  - Both cases were unchanged when the warning appeared. The stored tissue report carries the
    methylation-class row, so the warning is benign.
- `test_case_guards.py -k GLIO-HG-`: 240 passed.
- `apply_diagnosis_synonyms.py --check --conditions brain_tumor_glioma`: would change 0 of 600.
- `test_panel_case_contract.py` and `test_red_herring_paths_resolve.py`: 4 passed.
- `case_io.py check` on the 7 cases the auditor touched: no failure names them. The 3 failures in
  the full suite belong to other conditions or to the central claims.
- `test_guidance_claims.py`: 1 failed. No GLIO-HG claim is stale: the stale claims are nmdar, mg,
  nph and sync, which are for the orchestrator.
