# MS-RR: November 2026 round, condition audit summary

Condition auditor, 16 Nov 2026, after workers and verifiers. 30 cases (M01-M04, P01-P05, RM01-RM04,
RP01-RP05, RS01-RS06, S01-S06). Plan: `plans/MS-RR.md`; decisions D1-D20: `plans/MS-RR-decisions.md`.
Audit scripts: `/home/aprotani/review-round-2026-11/work/scratch/msrr-audit/` (`cover.py`, `classes.py`,
`musts.py`, `spec.py`, `leak0.py`, `leakout.py`, `xmod.py`, `labels.py`).

## Notes and rulings

- 118 notes, all R1 (NB-KSC3-TWUA-QDTM), none R2. Every note id appears in exactly one
  `work/rulings/<CASE>.json`, the one for its own case. All statuses are valid.
- Counts: **FIXED 117, DECLINED 1**. ALREADY-FIXED 0, CENTRAL 0, NEEDS-ANDREA 0, NO-ACTION 0.
- All 30 cases have changed since 06b74446, and every one has a log with `## Changes`.

### DECLINED

- **MS-RR-S03 d26941cf** (D18). The note says the patient is of East Asian descent. In S03,
  `patient.demographics.ethnicity` is "African American", unchanged since base 06b74446, and no field
  of S03 mentions East Asian descent (the East Asian patients are S02 and RS02). The NMOSD
  differential's remark that ancestry raises the prior probability of NMOSD is correct for an African
  American patient (Wingerchuk 2015 context). The note most likely describes another case.

### NEEDS-ANDREA

None.

## Classes: how each was fixed (before = lead's measurement on 16 Nov, after = this audit's scan)

| Class | Decision | Before | After |
|---|---|---|---|
| C1 LIT (literature step or output) | D1, commit 393c547e | 31 notes; 0 left after the class commit | 0 literature criteria, follow-ups or initial/fallback outputs |
| C2 MRI-CONTRAST (plain plus gadolinium pair) | D2, commit 71517e55 | 30 | 0 defects: 30/30 plain initial MRI, gadolinium follow-up, MRI criteria `contrast: true` |
| C3 four regions need no DIT only after a typical attack | D3 | 3 (P01, P02, P03) | 0: the three non-specific presentations say DIS is completed by DIT; the 27 typical ones keep the four-region rule |
| C4 uncertain earlier episodes counted as attacks | D4 | 9 cases (M01, M03, M04, P01, P02, RS04, RM01, RM02, plus a check of P05) | 0: every remaining "two attacks" or "prior attack" (RS02, RS03, S01, S03, S05, M02, RM04) rests on a residual sign on today's exam |
| C5 universal HBV/HCV/VZV pre-DMT screening | D5 | 30 musts plus 3 drug outputs | 0: 30/30 musts are drug-specific; HCV appears only in P05 (cladribine label line and stored serology) |
| C6 waiting for a urine culture before steroids | D6 | 13 | 0: all 13 use the canonical infection-assessment clause |
| C7 steroids beyond 14 days as an individual decision | D7 | 7 (M01, M02, P04, P05, RM04, RP04, RP05) | 0: all 7 say "Decide ... individually"; cases within 14 days keep "Offer/Treat" |
| C8 ISC after a single bladder scan | D8 | 12 | 0: the canonical "repeated if raised ... confirmed" text in all 12; RP05's own PVR must does not demand ISC |
| C9 S1P first-dose monitoring stated as universal | D9 | 2 (RS06, RP05) | **1 straggler found and fixed (RM04)**, now 0 |
| C10 tumefactive steroid gate | D10 | 5 (RM01, RM02, RP01, RP02, RP03) | 0: C10a text in RM01, RM02 and RP01; RP02 biopsy required and in the stop rule; RP03 urgent joint decision. RM02 and RP01 serve a demyelination histology fallback for a biopsy order |
| C11 pre-LP safety with a tumefactive lesion | D11 | 3 | 0: hard MRI-before-CSF constraint plus pre-LP must in RM01, RM02, RP01; the 25 non-tumefactive cases with a CSF criterion keep the soft constraint |
| C12 RP03 reversible postoperative causes | D12 | 1 | 0: new must; `action-abg` required, in the stop rule, served by the stored ABG |
| C13 RP03 OCB references without an LP | D13 | 1 | 0 OCB references in the RP03 ground truth |
| C14 AQP4/MOG CBA targeted | D14 | 10 recommended should be optional; "before DMT" wording in 8 rationales; 2 prohibitions | Tiers match the table exactly (8 required, 7 recommended, 10 optional, 5 none); 0 "before DMT" or "settles" wording; S05/S06 prohibitions deleted; S06 prohibition[0] no longer cites the AQP4 result |
| C15 P05 natalizumab and platform prohibitions | D15 | 1 | 0 |
| C16 RS01 vascular imaging | D16 | 1 | 0: required MRA criterion (CTA alternative), in the stop rule; the head-CT waste label matches only `angiography: false`, so no criterion/avoided overlap |
| C17 "CT" waste rationales without "head" | D17 | 18 of 27 | 0: 27/27 say head CT; RM04 has the optional chest CT criterion and the hypercalcaemia must |
| C18 S03 ancestry | D18 | 1 note | DECLINED (above) |

The checks also confirmed: every sequence constraint names existing criteria; every stop rule lists
exactly the required criteria; no avoided action matches a criterion's call (perfect-agent check).

## Fixes made by this audit

1. **Diagnosis named in drug-interaction outputs (blind leak pass, new finding, 4 cases).** The stored
   `check_drug_interactions` output returned to the agent named the diagnosis in its `proposed` field:
   - P03 initial: "Disease-modifying therapy classes for MS".
   - P04 follow-up: "MS disease-modifying therapy classes".
   - P05 follow-up: "high-efficacy MS disease-modifying therapies".
   - RS06 follow-up: "alternative first/high-efficacy DMT for RRMS".

   The acronym was removed in all four (RS06 now reads "or an alternative moderate- or high-efficacy
   disease-modifying therapy"). This is wording only and affects no ruling. It is logged under
   `## Verification`.
2. **C9 straggler, RM04.** The cardiac-monitoring waste rationale said rhythm monitoring "belongs to
   first-dose S1P modulator treatment". It now reads: "first-dose rhythm monitoring belongs to starting
   fingolimod (and another S1P modulator only where its label requires it)". Logged under
   `## Verification`.

## Blind leak pass (results)

- **Turn 0** (`format_patient_info`, rendered for all 30): no accepted label appears in the HPI,
  medications or indications, or exam, case-sensitive acronyms included.
  - "multiple sclerosis" appears only as a relative's diagnosis in the family history of P05, S03,
    S04 and S06. This is a recognised risk factor and does not name the patient's diagnosis. Kept.
  - Prior results:
    - P01, P02, P03: the outside MRIs, reported as "non-specific white matter changes", stay as
      referral history (October P01 decision). They do not give the lesion distribution or
      enhancement that the scored MS-protocol MRI returns.
    - RM02: the outside head CT is not a criterion.
    - RM04: the prior calcium 10.6 and non-elevated PTH, six months earlier, are history that R1's note
      0f34eee4 works from. The scored panel re-measures them (10.7, PTH 12) and is ordered for the
      mimic screen. Kept.
- **Stored outputs**: after fix 1, no output (initial, follow-up, fallback) names MS, "multiple
  sclerosis", RRMS, McDonald, DIS/DIT or "meets criteria". No drug-interaction output repeats another
  criterion's expected evidence (the only overlap is RP01's drug criterion with its own output).
- **Cross-modality synthesis**: no report cites another modality's results. The only hits were SSEP
  reports naming themselves "evoked potential" and CT reports recommending MRI, both legitimate.

## Approved cases changed

None: no MS-RR case is in `work/approved.txt`.

## Label and code changes

None. `accepted[0]` and `icd_codes[0]` are identical to base 06b74446 in all 30, and no synonym label
changed. `apply_diagnosis_synonyms.py --check --conditions multiple_sclerosis`: would change 0 of 600.

## CENTRAL requests (consolidated)

1. **`agent-platform/tests/test_guidance_claims.py`, claim `ms/AQP4/MOG CBA in 25: required 8,
   recommended 17`** (lines 277-280). Under D14 the expected tuple becomes `(25, 8, 7)` and the label
   becomes "... required 8, recommended 7". This is the only MS-RR failure in that test (it now
   reports `(25, 8, 7)`). The other MS claims pass: MRI, CSF 20/8/0, LP contraindicated 2, spine MRI,
   OCT/VEP, AQP4 never in initial labs, EEG/ECG waste.
2. **`agent-platform/config/review/condition_tool_guidance.yaml`**, `multiple_sclerosis.interpret_labs`
   response (line 857). "required in 8 with a red flag ... and recommended in 17 with optic neuritis or
   myelitis" becomes "required in 8 with a red flag, recommended in 7 with a feature suggestive of
   NMOSD or MOGAD (simultaneous optic neuritis and myelitis, optic disc swelling, painful tonic
   spasms), optional in 10, and not ordered in 5". Regenerate with `build_condition_tool_guidance.py`.
3. **Criteria pack `dataset-generation/criteria_packs/MS-RR.md`**, as listed in plan section 4 item 1:
   - 1.3: the four-region rule applies only after a typical attack.
   - 1.9: the steroid gate becomes N6.
   - Section 2: the AQP4/MOG tiers per D14; RP02 biopsy required; RS01 MRA required; RP03 ABG
     required; RM04 chest CT optional; hard MRI-before-CSF in RM01, RM02 and RP01.
   - Section 3: "head CT".
   - Section 4: drop the anti-JCV index above 1.5 as a prohibition.
   - Section 8: musts per N3, N4, N5 and C7.
   - Section 9: add `[Fowler_2009]`, `[EHA_ESMO_PCNSL_2024]`, `[AHA_2021_SecPrev]` and `[Allen_2012]`
     to the allow-list.
4. **Review-app display** (from the RS01 log; addendum display facts). Abnormal lab rows whose
   `clinical_significance` is null are shown as "none" (RS01 lipid and vitamin D rows): print null as
   "not stated". No case change is needed (vitamin D is already a must and a red herring; lipids are
   in the differential and the key evidence).
5. No synonym, vocabulary, fallback-library, MockServer or schema change is needed for MS-RR.

## Check results (after the audit's edits)

- `perfect_agent.py <id>`: **30/30 pass**, one id per call, no "same stored report" warning.
- `pytest agent-platform/tests/test_case_guards.py -k "MS-RR-"`: **240 passed**.
- `apply_diagnosis_synonyms.py --check --conditions multiple_sclerosis`: **clean** (0 of 600 would
  change).
- `pytest test_guidance_claims.py test_panel_case_contract.py`: test_panel_case_contract passes.
  test_guidance_claims fails, and its only MS-RR line is the AQP4 tier claim (CENTRAL 1). The other
  failures are ALZ, FEPI and FTD claims, outside this condition.
- `case_io.py check` on the five edited cases (P03, P04, P05, RS06, RM04): schema OK, synonym guard
  OK; the full suite reports 2 failures, and the helper reports that neither names these cases or
  MS-RR (other conditions are mid-edit; central claim tests are handled later).

## For the physicians at re-review

- The AQP4/MOG assay tier change (10 cases from recommended to optional) applies R1's S05/S06 ruling
  across the condition.
- RS01 now requires vascular imaging, RP02 requires the biopsy, and RP03 requires an arterial blood
  gas.
- The drug-check outputs of P03, P04, P05 and RS06 no longer name the diagnosis.
