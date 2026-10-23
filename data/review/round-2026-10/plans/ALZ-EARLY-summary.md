# ALZ-EARLY: round 2026-10 summary

Condition auditor, 24 Oct 2026. Scope: 30 cases (M01-M05, P01-P04, RM01-RM04, RP01-RP05, RS01-RS06,
S01-S06), plan `plans/ALZ-EARLY.md`, notes `notes/ALZ-EARLY.json` (69 ids), logs `logs/ALZ-EARLY-*.md`.

Final state: `perfect_agent.py` 30/30, `case_io.py check` clean (schema and synonym guard OK; the
118 failures in the wider suite name no ALZ-EARLY case), `test_case_guards.py -k ALZ-EARLY` 60 passed.
Every case log ends with a "Condition audit (24 Oct 2026)" entry listing what this pass changed.

## 1. Error classes and how each was fixed

| class | defect | fix applied |
| --- | --- | --- |
| C1 | Cholinesterase-inhibitor drug check in MCI cases; wrong interaction content (amlodipine "slows the heart", CYP2C19 routing, tamsulosin called anticholinergic) | Drug check deleted in the six MCI cases (M01-M04, RM04, S06) with the canonical MCI prohibition, must and KCE; in dementia cases an optional check `{"drug": "donepezil"}` with rewritten content, required in P04, RP02, RP03; none in RP04 (per plan) |
| C2 | CSF and amyloid PET as duplicate or library-answered criteria | One optional biomarker criterion with two alternatives (CSF AD panel or `amyloid_PET`), canonical label, rationale and must; concordant counterpart authored in every case; `fallback advanced_imaging` null; RP04 keeps CSF required (CJD question) |
| C3 | Template clinical-assessment impressions with engineering sentences | Rewritten from each case's own findings (scores, cueing, informant, functional stage) |
| C4 | Staging: MCI versus mild dementia not decided by instrumental function | HPI, criteria_met and impression aligned to the functional rule; RM01, RM02, RM03, RS06 restaged to mild dementia |
| C5 | Contrast language in non-contrast MRI | Removed; RS06 keeps gadolinium text only in its contrast follow-up |
| C6 | CSF carrying 14-3-3, RT-QuIC, NfL, infectious and autoimmune panels | Routine AD panel only (keys `Abeta42`, `Abeta40`, `Abeta42_40_ratio`, `phospho_tau`, `total_tau`); RP04 keeps 14-3-3 and RT-QuIC |
| C7 | Lab `clinical_significance` prose; low-normal B12 without MMA | `clinical_significance` null; recommended MMA criterion with an authored follow-up in every case with B12 about 305 pg/mL or below (M01-M04, RP04, RP05, RS05, S01, S03, S05) |
| C8 | Literature search as a criterion or output | Removed everywhere; `literature_search` null |
| C9 | Consults and procedures that are not tools | Re-authored as tests (e.g. speech-language content inside the neuropsych battery for P02) |
| C10 | Over-long key clinical evidence | At most 4 items, case-specific |
| C11 | Differential not reflecting the assessment-time view | Likelihoods and key features cite only results the case returns; DLB and FTD low; VCI moderate only as a contributor |
| C12 | Generic musts and prohibitions | Written for each case (vascular risk with its values, safety, disclosure, deprescribing, thyroid and B12 musts where relevant) |
| C13 | Duplicated citation keys; rationale equal to label | One bracketed key each; patient-specific rationales and expected_evidence |
| C14 | QT-prolonging co-medication with no ECG step | ECG criterion where the plan required it (escitalopram cases); avoided ECG elsewhere with a consistent rationale |
| C15 | Narrative inconsistencies (vitals, ECG rate, HPI vs exam) | Fixed per case |
| C16 | Missing ordering rules; `max_additional_actions` 0 | Soft MRI before biomarker, clinical assessment before biomarker, battery before genetics; stop rule = required criteria, `max_additional_actions` 1 |

Stragglers fixed by this audit (cross-case consistency, all through case_io):

- Lab panel key `Reviewed_cognitive_panel_additions` (a review-round artefact visible to the agent)
  renamed by contents in all 30 cases (`Magnesium_homocysteine_ESR_CRP`, `Magnesium_homocysteine`,
  `Magnesium_homocysteine_CRP`, `Magnesium`; spaced or snake form where the case uses it).
- Label and metadata wording "the reviewed cognitive laboratory panel" changed to "the cognitive
  laboratory panel", the wording six cases already used (24 cases).
- Copied normal values (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8 in up to 13 cases) varied
  within each case's reference ranges (13 cases); M01's homocysteine kept because its differential cites it.
- The labs criterion orders a CMP but M01, M02, M03, P01, RM04, RP05 returned a BMP: normal liver
  tests added and the panel renamed CMP (this supersedes the M01 worker's FLAG).
- CBC index arithmetic (MCV = Hct x 10 / RBC) corrected in M01, M03, RS02, RS06.
- MMSE and MoCA item lists that did not sum to the stated totals: M05, P03, P04, RM04, S01-S04
  (totals unchanged; item breakdowns corrected or completed).
- M05 MRI: "Posterior fossa ... normal" contradicted the cerebellar lacune; now "Brainstem morphologically normal".
- "Lasting power of attorney" (UK instrument) changed to "durable power of attorney" in the 13 US-setting cases; RS05 keeps "lasting".
- Citation keys harmonised: RP04 and RP05 `[ADA_older_adults_2024]` to `[ADA_older_adults_2025]`
  (as M05); RM03 `[McKeith_2017_DLB]` to `[DLB_2017]` (as RP05 and the plan).

Checked and left as is: canonical texts without a final period in S01-S05 and the RM04 KCE (each case
omits final periods throughout, so it is that case's style); the S05 educational point that an A+T+
profile "establishes" AD (true under NIA-AA 2018); biomarker rationale variants in P02, P03, P04,
RM01, RM02, RM03, RS05 (case-specific, not drift); pre-existing em dashes in sentences nobody rewrote.

## 2. Counts

- Reviewer notes: 69 of 69 in exactly one case log with a ruling. FIXED 68, ALREADY-FIXED 1
  (fb473466-167b-46a9-83e3-5caf790c2932, M04, an agreement note), DECLINED 0, BLOCKED 0.
- Workers' own findings (log tables): 504 FIXED, 2 FLAGGED (M01 BMP without liver tests, now fixed
  by this audit; one case's 4+/5 hip flexors and hyporeflexia attributed to sarcopenia, covered by a
  nutrition must, no work-up added).
- Condition-audit findings: 11 straggler classes above, all fixed; none flagged.
- Cases changed: 30 of 30. Approved cases changed: 0 (all 30 are `draft`).

## 3. DECLINED and BLOCKED notes

None. No note was declined or blocked.

## 4. CENTRAL requests (consolidated)

1. **Synonyms** (`diagnosis_synonyms.yaml`, `apply_diagnosis_synonyms.py`): the expansion is per ICD
   code over every code in the case.
   - Stop granting "posterior cortical atrophy", "benson syndrome" and "early onset alzheimer" through
     G30.0 to cases whose `accepted[0]` is not PCA (every amnestic late-onset S, RS, RP04, RP05, P03, P04, RM04 case).
   - Do not cross MCI and dementia: the G31.84 entry grants dementia labels and G30.x codes to the MCI
     cases (M01-M04, RM04, S06).
   - Prune and re-run for the restaged cases RM01, RM02, RM03, RS06, which still accept the old MCI
     labels, and for the new labels of M01 and M03.
2. **Labels**: RM04 `accepted[0]` says "single-domain" while the data show amnestic multi-domain MCI;
   proposed "Mild cognitive impairment due to Alzheimer's disease (amnestic multi-domain, with naming
   involvement)", G31.84 unchanged. Needs a reviewer ruling.
3. **Citation keys** to add with references: `NIA_AA_MCI_2011`, `AA_2024`, `NICE_NG97`,
   `PCA_consensus_2017`, `PPA_2011`, `bvAD_2015`, `FTDC_2011`, `ACMG_NSGC_2011`, `CJD_2021`,
   `iNPH_2005`, `iNPH_Japan_2021`, `Boston_CAA_2022`, `STRIVE_2013`, `BSH_B12_2014`, `ETA_SCH_2013`,
   `TRUST_2017`, `Beers_2023`, `DLB_2017`, `ADA_older_adults_2025`, `AHA_secondary_stroke_2021`,
   `AHA_ACC_cholesterol_2018`, `ATA_hypothyroidism_2014`, `BSG_IDA_2021`, `CLARITY_AD_2023`,
   `Lecanemab_AUR_2023`. Alias: PD-P01, PD-P02, PD-P03, PD-RP03 cite the McKeith 2017 DLB consensus
   as `[McKeith_2017_DLB]`; pick one key dataset-wide.
4. **Vocabulary**: a speech and language assessment term for PPA cases (P02); the `not_completed`
   fallback kind used by RS05 if kinds are enumerated centrally.
5. **Library** (`fallback_library.yaml`): amyloid PET, CSF and FDG-PET defaults are normal, so an
   unanticipated order in an AD case returns a negative study (RP04, RP05 FDG); check the MR
   spectroscopy and DaTscan defaults are normal and non-contributory; the drug-check default says
   "no interaction" for any drug.
6. **Harness**: `check_drug_interactions` serves the single stored follow-up (donepezil) for any drug,
   e.g. memantine or rivastigmine; add a drug discriminator in the MockServer matcher.
7. **perfect_agent.py**: add a mode that exercises every alternative of each criterion and flags
   library answers.
8. **Dataset diversity**: near-duplicates S02/S03/S04, RS03/RS04 and RP01/RP02 (both 62-year-old
   women with PCA) need a central diversity check.

## 5. Open questions for Andrea (consolidated)

- Q1. Biological criteria: write impressions to NIA-AA 2018 or to AA 2024? The text is true under
  both; a choice would let M01 and M03 be labelled more precisely.
- Q2. RM03 and RS06 had no reviewer notes but were restaged to mild dementia by class (functional
  rule); this changed `accepted[0]` and `icd_codes[0]` without a reviewer ruling. Confirm or revert.
- Q3. CSF and amyloid PET counterparts were authored in all 30 cases, results no reviewer has seen:
  acceptable?
- Q4. FDG-PET is authored in S01-S06 and some R cases and left to the library's normal report
  elsewhere: author it everywhere, or accept the library answer for an optional study?
- Q5. RS06: the MRI criterion accepts both contrast false and true (contrast characterises the
  meningioma); keep both alternatives, or require non-contrast with contrast as a follow-up only?
- Q6. This audit added normal liver tests to six CMP reports and varied copied normal values: results
  no reviewer has seen, though nothing scored depends on them. Acceptable?
