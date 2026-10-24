# MS-RR: close-out decisions (24 October 2026)

Close-out of MS-RR under `CLOSEOUT_BRIEF.md` (Andrea, 24 Oct 2026: decide every open point for the
quality of the dataset). Inputs: `plans/MS-RR.md`, `plans/MS-RR-summary.md` (open questions 1-15,
CENTRAL 1-8, auditor flags). There is no reviewer notes file for MS-RR. Every entry gives the
decision, the reason and what changed. Per-case details are in the "Close-out (24 Oct 2026)"
section of each `logs/MS-RR-*.md` (all 30, since the synonym change touches every case).

Sources checked on 24 Oct 2026:
- FY2026 ICD-10-CM G35 subcodes (effective 1 Oct 2025; ASHA and AAPC code-change summaries): G35.A
  relapsing-remitting MS (Excludes1 G37.9 demyelinating disease of the CNS, unspecified), G35.B0-B2
  primary progressive, G35.C0-C2 secondary progressive, G35.D MS unspecified; flat G35 retired.
- Montalban X et al. Diagnosis of MS: 2024 revisions of the McDonald criteria. Lancet Neurol
  2025;24(10):850-865, doi 10.1016/S1474-4422(25)00270-4 (citation confirmed; content read in
  summaries: optic nerve fifth region, kFLC as an alternative to OCB, CVS and PRL supportive;
  additional supporting evidence strongly recommended, not mandated, at 50 or over or with vascular
  risk factors). Migraine is not named in what could be read.
- Wattjes MP et al. Lancet Neurol 2021;20(8):653-670, doi 10.1016/S1474-4422(21)00095-8.
- NICE NG220 update page: June 2026 amendment refers the diagnosis recommendations to the 2024
  McDonald criteria and removes the "not on MRI alone" recommendation; management recommendations
  of 2022 unchanged.
- Hardy TA, Chataway J. Tumefactive demyelination: an approach to diagnosis and management. J Neurol
  Neurosurg Psychiatry 2013;84(9):1047-1053, doi 10.1136/jnnp-2012-304498, PMID 23334629 (Europe
  PMC record; abstract: diagnostic approach, the difficulty of when to biopsy, acute treatment, DMT
  only once MS is confirmed by DIS and DIT). The full text is paywalled: the key is cited for the
  diagnostic approach and the biopsy decision, not for a specific imaging threshold.

## CENTRAL items of the summary handled here

**C1. Criteria pack** (`dataset-generation/criteria_packs/MS-RR.md`, rewritten). Diagnostic text
moved from McDonald 2017 to the 2024 revision (five regions, 4-5 regions need no DIT, kFLC, CVS,
age and vascular-risk rule as a recommendation; migraine stated as clinical prudence, open question
6). Work-up hierarchy with the applied tiers and counts; literature and drug check out of the
required pathway (both optional; drug check recommended in RP03 and RP05); AQP4/MOG tier rule with
RS05 recommended (8 required, 17 recommended, 5 none); CSF 8 recommended, 20 optional, LP
contraindicated in RP02 and RP03; waste and contraindicated actions; soft constraints; tumefactive
section; musts; red herrings. Allow-list: every key the 30 cases cite (`McDonald_2024`,
`Wattjes_2021`, `NICE_NG220`, `Wingerchuk_2015`, `Banwell_2023_MOGAD`, `Petzold_2017`, and now
`Hardy_2013`) with a verified full reference; `Reich_2018` kept for general statements;
`McDonald_2017` and `MAGNIMS_2016` marked superseded; "MAGNIMS-CMSC-NAIMS 2024/2025" marked
non-existent. `Petzold_2017` was already in the allow-list.

**C1b. `[Hardy_2013]` on the tumefactive criteria.** Added to RM01 (`action-mrs`,
`action-biopsy`), RM02 (`action-mrs`), RP01 (`action-mrs`, `action-ct-cap`, which had no citation),
RP02 (`action-perfusion`, `action-mrs`, `action-biopsy`), RP03 (`action-mrs`, `action-biopsy`).

**C2. Synonyms** (`diagnosis_synonyms.yaml`, G35 entry; condition enum `multiple_sclerosis`).
- Codes G35.B and G35.C removed: progressive courses, wrong for 30 relapsing-remitting cases. G35
  (the pre-FY2026 code for any MS) and G35.D (MS, unspecified) kept: they are consistent with the
  accepted label "multiple sclerosis".
- Label "demyelinating disease" removed and added to `RETIRED` so `--prune` strips it: G37.9 is an
  Excludes1 of G35.A, and its tokens occur in "NMOSD, an inflammatory demyelinating disease", MOGAD
  and ADEM answers.
- Bare "MS" kept: it is the standard abbreviation, and its only false match ("MOGAD rather than MS")
  is the negation case that "multiple sclerosis" shares; no non-MS entity tokenises to `ms` (MSA is
  `msa`). Negation is a scorer item (CENTRAL below).
- Mimic and variant check: there is no NMOSD, MOGAD, ADEM, CIS or RIS case in MS-RR; all 30 have
  accepted[0] relapsing-remitting MS (5 tumefactive variant) and icd_codes[0] G35.A. Tested with
  `DiagnosisCriterion.matches`: NMOSD (including "an inflammatory demyelinating disease"), MOGAD,
  AQP4-positive NMOSD, ADEM, tumefactive demyelinating lesion, CIS, RIS, PCNSL, neurosarcoidosis,
  small-vessel disease, MSA and codes G35.B0, G35.C1, G37.9, G36.0 no longer match; RRMS,
  "tumefactive MS", G35.A, G35, G35.D match. No case of another condition has a G35 primary code,
  and the four other-condition labels that mention MS (ALS-M08, FND-M09, MG-P03, SAH-RP11) need
  their own disease tokens, so an MS answer does not score there.
- Applied with `apply_diagnosis_synonyms.py --prune --conditions multiple_sclerosis` (30 cases);
  `--check` clean over all 600.

**C3. Guidance claims.** `build_condition_tool_guidance.py` MS responses rewritten (CSF 20
optional, 8 recommended, LP contraindicated in 2; OCT 14 and VEP 18 optional; AQP4/MOG in 25, 8
required and 17 recommended, results only to an order naming the assay; EEG and ECG: no criterion,
EEG waste in 28 and not penalised in RM01 and RP03, ECG waste in 1; the old "no authored EEG/ECG
result remains" was false, every case has fallbacks). YAML regenerated with `--write` (only the
five MS lines changed). `test_guidance_claims.py`: MS claims rewritten to those numbers plus "AQP4
results never in the initial labs", with a small `avoided_with` helper; all MS claims pass (the
remaining failures are FEPI-TEMP and PD claims, their close-outs).

**C4. Discriminators.** MS-RR added to `DISCRIMINATOR_CONDITIONS`; `test_case_guards.py` passes
(1834), `-k MS-RR-` 90 passed. No output needed a change (the audit had added `echo_type` TTE to
S01-S06).

**C5b (data part). AQP4/MOG order in the five cases without a criterion.** Decided: store the same
negative CBA follow-up in P01, P02, P03, RM03 and RS04. These patients have MS, so a negative
result is the true one; before, an agent that ordered the assay got the first-line panel again,
which is incoherent. Scoring unchanged (no criterion). MockServer probe: every alternative, alone
or combined, in either order, gets the rows; the mimic panel alone does not. RS04's differential
said "AQP4-IgG was not tested": now "testing is not indicated without a red flag".

## Open questions of the summary (all decided; none needs Andrea)

1. **RM01 lesion sides.** Kept: left pontine and left MCP lesions explain ipsilateral abducens
   paresis and limb ataxia; the right C2-C3 posterior column lesion explains the earlier right-hand
   episode. Anatomically correct.
2. **RM02 CT and driving must.** Kept: the CT fallback now matches the lesion; CT stays a waste
   action because a CT was already done before the encounter; driving advice with a homonymous
   hemianopia is a real safety must.
3. **RM03 steroid must; no AQP4/MOG criterion.** Kept: constant binocular diplopia is a relapse that
   affects function (NICE NG220). The incoherent AQP4/MOG answer is fixed in the data (C5b).
4. **RM04 VEP follow-up and PTH 12 pg/mL.** Kept: the library normal VEP contradicted the RAPD and
   pallor; granulomatous hypercalcaemia suppresses PTH.
5. **M01, M02 OCT.** Kept optional with stored chronic thinning (documented earlier optic
   neuropathy); M03 has no OCT because the optic symptom is days old (no thinning expected).
6. **P01, P02 migraine and supporting evidence.** Kept. The 2024 rule verified is age 50 or over or
   vascular risk; the cases call the cord lesion supporting evidence as prudence, which is correct
   under either reading. The pack says so.
7. **P02 "Lhermitte sign not tested".** Kept: realistic examiner behaviour; nothing scored depends
   on it.
8. **RP04 no RAPD with a 24 um inter-eye pRNFL difference.** Kept: a recovered optic neuritis can
   leave the swinging-flashlight test negative, and the OCT asymmetry is what the case teaches. The
   8-year-old leg numbness stays an undocumented possible event. Listed for the physicians.
9. **RS02 regions.** Kept: four MRI regions with the earlier optic neuritis as the prior attack;
   the optic nerve is not counted as a region because no VEP or OCT is served (2024 rule).
10. **RS05 AQP4/MOG recommended.** Kept: the plan's rule (myelitis in the history) governs over its
    per-case line; pack and claims now say 17 recommended.
11. **RS06 non-enhancing symptomatic C3-C4 lesion; B12 228 pg/mL.** Kept: a symptomatic lesion need
    not enhance; B12 is within the reference range, the prohibition and the differential explain
    why it does not account for enhancing brain lesions and OCB. An MMA criterion is not possible
    (no `methylmalonic_acid` term; CENTRAL) and a must that orders a test is against the pack.
12. **S04 gastrointestinal work-up must** for iron deficiency in an adult man. Kept: a real
    management item for this patient.
13. **S05 disc swelling.** Kept: present in about a third of MS optic neuritis; the negative live-cell
    MOG-IgG addresses MOGAD.
14. **S06 four or five regions.** Kept: the formulation and KCE accept either count.
15. **Class S deviation from plan A8.** Kept: the antibody rows stay a follow-up; this is correct
    whether or not the MockServer later filters the initial labs (CENTRAL 1).

## Auditor flags

- `metadata.condition_name` with an em dash in 9 cases (M01, P02, RM04, RS01-RS06): declined.
  Metadata only, pre-existing, the same wording as the generator `name`; not an error, and the
  round's rule is "fix errors, do not churn".
- CENTRAL 5, 6, 7 of the summary: code and test items, listed below.

## Generator (`conditions.yaml`, multiple_sclerosis block)

- Comment rewritten to the applied design (2024 criteria, tiers, AQP4/MOG as a follow-up, no future
  data).
- `common_followups`: removed `request_repeat_mri_3months` (future scan, the class F defect in 17
  cases); VEP and OCT moved from `interpret_labs` to `order_specialized_test` (`vep`,
  `optical_coherence_tomography`); spine MRI from `analyze_brain_mri` to `order_body_imaging`
  `spine_MRI`; AQP4/MOG named as the cell-based-assay trigger used by the cases.
- `key_findings`: MRI "Meets the 2024 revised McDonald diagnostic framework" removed (a report does
  not state the criteria); cord findings out of the brain MRI (class H); puzzle MRI now carries a
  typical lesion (P01-P03 fix) instead of "no enhancement (monophasic presentation)"; tumefactive
  appearance added; body imaging lines are cord findings only (the migraine and subcortical lines
  were brain findings); labs: AQP4/MOG never in the initial labs, no significance text on normal
  rows (class E); CSF kFLC above or below the stated cutoff.
- `difficulty_variants`: results removed from the presentations ("Classic MRI and CSF", "MRI
  suggests prior subclinical lesions"); the moderate presentation's leg weakness is lateralised
  (class R); the puzzle keeps the outside "non-specific" MRI as history.

## For the physicians (at re-review)

- Scoring changes: "demyelinating disease" and the progressive codes no longer score in any MS-RR
  case.
- RP04: absent RAPD with a 24 um pRNFL asymmetry (question 8).
- The whole condition was never physician-reviewed and was rewritten by the round: schedule it.

## Still for Andrea

Nothing blocking.

## CENTRAL (code, tests, vocabulary; not edited here)

1. **MockServer labs** (`mock_server.py`, summary CENTRAL 5): the first `interpret_labs` order
   receives every panel of the initial labs whatever it names, so a second-tier assay stored there
   leaks to the first-line order; filter the initial payload by the ordered panels, or make the
   perfect-agent "same stored report" warning a failure for labs. An order naming only assays the
   case does not store is answered with the initial labs again: serve the library normal for the
   ordered assay or a "not stored" message (MS-RR now stores the assay in all 30; other
   conditions are likely affected).
2. **`perfect_agent.py` `_source`**: the `<- ?` labels for brain MRI and labs in the S cases come
   from comparing an `exclude_none` dump with an output that keeps null fields. Cosmetic.
3. **Guards** (`test_case_guards.py`): an `analyze_brain_mri` output must not contain "thoracic
   cord", a "T[1-9]-T" level or "conus"; banned strings "agent not specified on this case's
   pathway", "Requested agent" (drug fallback `proposed`), "naive agent", "(background only)",
   "(background evidence only)". All are absent from MS-RR now.
4. **Scorer, course and negation**: "secondary progressive multiple sclerosis" and "primary
   progressive MS" still score in a relapsing-remitting case through the label "multiple
   sclerosis", and "MOGAD rather than MS" scores through "MS". Same roots as the per-case rejected
   tokens (ALZ-EARLY) and negation (SAH) items already in `CENTRAL_PENDING.md`; MS-RR would reject
   the tokens `progressive`, and the negated forms.
5. **Vocabulary (optional)**: `interpret_labs` panel `methylmalonic_acid` (serum MMA, CPT 83921),
   to confirm a borderline B12; would allow RS06 to score the confirmation instead of leaving the
   low-normal B12 as a distractor only. Not needed for any current criterion.
6. **`CENTRAL_PENDING.md`** (orchestrator): MS-RR is in `DISCRIMINATOR_CONDITIONS`; its guidance
   claims pass; mark the MS-RR items done.
