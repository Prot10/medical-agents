# FTD: condition audit summary (November 2026 round)

Condition auditor, 16 Nov 2026. This covers the 30 cases FTD-M01..M10, P01..P08 and S01..S12,
and the 108 notes, all from R1 (NB-KSC3-TWUA-QDTM). No FTD case is approved
(`work/approved.txt` lists none). The base is 06b74446. The plan is `plans/FTD.md` and the
decisions are in `plans/FTD-decisions.md`. The audit scripts are in
`/home/aprotani/review-round-2026-11/work/scratch/ftd-audit/`:

- `notecov.py`: note and ruling coverage.
- `classes_audit.py` and `decisions_audit.py`: the plan applied uniformly.
- `leak_audit.py` and `report_scan.py`: the blind leak pass.
- `stragglers.py`: performance status, Rascovsky knock-ons and C23.
- `counts.py`: class counts before and after.

## Classes: how fixed, counts at base 06b74446 and now

| class (plan) | measure | before | after |
|---|---|---|---|
| C1 LIT (commit 393c547e) | cases with any literature criterion or output | 30 | 0 |
| C2 definite certainty | pathogenic-panel cases (12) whose must 0 lacks "definite" | 10 | 0 |
| C3 possible bvFTD, normal or borderline MRI | P05 and P07 must 0 with the three-level clause | 0 of 2 | 2 of 2 (P01 and P02 already had it) |
| C4 FDG/SPECT over-call | unhedged FDG or SPECT impressions in P01, P02, P05, P07 | 8 | 0 |
| C5 ALS panel without MND | stored ALS panel with no criterion or avoided action | 8 | 0 (7 waste avoided actions, report kept last; M02 ALS panel is an alternative of its optional genetics) |
| C6 templated performance status | cases with the template line | 26 | 0 (each rewritten from its HPI) |
| C7 Rascovsky over-scoring | E counted on a fixed meal routine (M01, M03, M04, P07) | 4 | 0; M09 F not established (5 of 6); M06 A and C not established (3 of 6); criteria_met, scores, impression and expected evidence agree in all 28 bvFTD cases (scripted) |
| C8 abnormal rows with null significance | rows | 34 (plan's measure 38) | 0 |
| C9 M05 lithium | must 1, must 2, rejected, differential | open | done |
| C11 ECG with a safety indication | ECG waste in P03 and M05 | 2 | 0 (P03 recommended QTc ECG plus must; M05 optional; ECG served from initial outputs) |
| C12 drug-check reports | M04 triptan, M05 bipolar switch, P03 escitalopram + HCQ | 3 wrong | 0 |
| C13 to C19 case-specific (M06, M07, M08, M09, M10, P01, P04) | text and tier checks in `decisions_audit.py` | open | all OK |
| C21 alcohol | rejected ARBD or alcohol dementia in S01, S05, S06, S09, S10 | 5 | 0; canonical AUDIT/SADQ/thiamine must in all 5; differential "contribution is not excluded" in all 5 |
| C22 head CT rationale | "CT lacks the resolution" | 27 | 0 (canonical text, NICE NG97 and SNLG/ISS 2024 citations) |
| C23 perfusion-MRI rationale | rationale naming amyloid PET as the lobar pattern study | 9 | 0 |
| C24 to C26 (S06, S11, S12) | text checks | open | all OK |
| P04 DaTscan | DaTscan criterion | 1 | 0 (waste avoided action, NICE NG71; report last) |

Structural checks over all 30 cases found nothing wrong:
- Sequence and stop-rule ids all exist.
- Every required criterion is in the stop rule, and nothing non-required is in it.
- No case has both an ECG criterion and an ECG avoided action, or neither.
- No literature remnant, no "sporadic" in M07, no "co-existing PD" left in P04.
- No new em dash in any FTD diff since 06b74446.
- No review-process text added to metadata.
- No FTD MRI report has gadolinium content (`mri_probe.py`: 0 gadolinium texts).

## Ruling counts (108 notes)

| status | n |
|---|---|
| FIXED | 102, of which 48 by class LIT |
| ALREADY-FIXED | 6: ccb82f4f (P01), 116ebe03 (P01), 7d0e7312 (P02), 8aa821c6 (P02), edc62f71 (P08), 0367115d (M05) |
| CENTRAL (as status) | 0. CENTRAL parts sit inside FIXED or ALREADY-FIXED rulings: d645ace0 (synonyms), 4473d085 (guidance), 0367115d (display), and the C8 display remark on 071a5363, 808af2e1, 94b68fbc, 68b33e69 |
| DECLINED | 0 |
| NEEDS-ANDREA | 0 |
| NO-ACTION | 0 |

Every note id of `notes/FTD.json` appears in exactly one `work/rulings/FTD-*.json`, with a valid
status. No ruling is missing, duplicated, or filed under another case. Every note appears in its
case log. All 30 cases changed since 06b74446, and each has a log with '## Changes'.

## DECLINED and NEEDS-ANDREA

None. Every point could be decided from the notes and the cited guidelines (see
FTD-decisions.md section 27 for the October decisions that were revised or kept).

## Approved cases changed

None. No FTD case is approved.

## Label and code changes (accepted[0]; every icd_codes[0] stays G31.09)

| case | before | after |
|---|---|---|
| M06 | ... definite (known pathogenic GRN variant), with early corticobasal syndrome features | ... definite (known pathogenic GRN variant), with possible early corticobasal-spectrum signs (mild right-hand apraxia and graphesthesia) |
| M07 | ... probable, sporadic, with concurrent alcohol use disorder and alcohol-related cerebellar degeneration (comorbid contributor) | ... probable (provisional until reassessment after abstinence and sleep apnoea treatment), with concurrent alcohol use disorder and alcohol-related cerebellar degeneration; family history suggestive but unconfirmed |
| M08 | ... probable, sporadic, in HIV-positive patient (well-controlled; HIV-associated neurocognitive disorder and opportunistic infections excluded) | ... probable, in a person with well-controlled HIV (CSF viral escape and opportunistic infection excluded; HIV-associated neurocognitive disorder unlikely) |
| M10 | Behavioral variant frontotemporal dementia (bvFTD) | Right temporal variant frontotemporal dementia (rtvFTD), meeting probable behavioral variant FTD (bvFTD) criteria |
| P04 | ... probable, with co-existing Parkinson's disease | ... probable, with levodopa-responsive parkinsonism (co-existing Parkinson's disease or FTD-associated parkinsonism) |

Per-case `rejected` labels removed so that qualified answers score. Each removal was checked with
`DiagnosisCriterion.matches`; the label alone still never scores.
- M05: lithium toxicity, lithium neurotoxicity.
- M07: wernicke, and korsakoff (verifier pass 1; this goes beyond the plan, which kept korsakoff,
  because "possible Wernicke-Korsakoff" is a correct qualifier when thiamine is given for
  suspected Wernicke).
- M08: HAND, HIV-associated neurocognitive disorder, and HIV-associated dementia (verifier pass 2;
  its tokens vetoed "bvFTD; HIV-associated neurocognitive disorder may contribute" when written
  out).
- M10: semantic dementia.
- P01: hyperammonaemic and hyperammonemic encephalopathy (verifier pass 2; beyond the plan,
  because must 2 keeps a valproate contribution open).
- S01, S05, S06, S09, S10: alcohol-related brain damage, alcohol-related dementia.

The scorer accepts the qualified answers in M05, M07, M08 and P04 and the alcohol qualifiers in
the five C21 cases. P08, S11 and S12 still correctly reject plain bvFTD answers.

## Leak pass (turn 0 and stored outputs)

- **Turn 0** (`format_patient_info`, rendered for all 30 cases): no case names its own diagnosis.
  The label hits are all family history:
  - ALS negatives in M01, M03, M09, P02, P03, S11 and S12; ALS in a relative in M02 and P08.
  - S05: the brother "recently diagnosed with FTD" (also in the chief complaint, unchanged since
    the reviewed base).
  - M06: the daughter has FTD-GRN and the mother is "likely FTD".

  Other pre-encounter results were kept:
  - M06's known GRN variant: no criterion orders genetics.
  - M08's long-term undetectable viral load: an October decision. The current viral load and CD4
    of 680 come from the criterion.
  - M05 eGFR 64 and S11 HbA1c 6.8%: known chronic background, not the decisive evidence of any
    criterion.

  Exam "atrophy" hits are tongue or calf findings. Medication indications name no diagnosis (P04
  levodopa for "Parkinson's disease" is history the label itself keeps open).
- **Drug checks** (initial, follow-up and fallback, all cases): none names the diagnosis or
  repeats an expected_evidence string. Each agrees with the patient's medication list and
  allergies: M02 ibuprofen bleeding, S02 naproxen, S06 aspirin and metoprolol, S09 thiazide
  hyponatraemia, P03 hydroxychloroquine QT, M05 bipolar switch, M08 Biktarvy.
- **Cross-modality**: no MRI, FDG or SPECT, neuropsychology or genetics report cites another
  modality. Bedside assessments name the clinical criteria they establish (Rascovsky,
  Gorno-Tempini) and genetic reports name the test panel; both are kind 2.

## Stragglers fixed by the audit

- **Rulings** (`work/rulings/` for M07, M08, M09, M10, P01, P02): 11 LIT rulings did not cite
  "class LIT, commit 393c547e", as the addendum requires. Their `what` now starts with that
  citation and the re-check; the status stays FIXED. The case logs already cited the class.
- **FTD-M08 log**: the 962d3cd1 row and the Changes paragraph still said "HIV-associated
  dementia" stays rejected, which contradicts the verifier pass 2 removal. Both are corrected and
  a '## Verification' entry is appended. No case data changed.
- **No case file needed a change.** The P04 ALS follow-up flag was a false positive: ALS is
  second-last and DaTscan last, after the unscored gait follow-up. The re-save was byte-identical,
  and every FTD file is in `case_io` canonical form.

## CENTRAL requests (consolidated)

1. **Synonyms** (`diagnosis_synonyms.yaml`): new entry `G31.09+rtv`, cases `[FTD-M10]`, with the
   labels rtvFTD, right temporal variant FTD, right temporal variant frontotemporal dementia,
   right semantic dementia and right temporal semantic dementia. Today "rtvFTD" and "right-sided
   semantic dementia" score n in M10 (checked). Check that S11 does not accept them.
2. **Label changes** (rule 3, scoring unchanged): M06, M07, M08, M10, P04 (table above).
   `apply_diagnosis_synonyms.py --check --conditions ftd` is clean.
3. **Guidance and test** (`condition_tool_guidance.yaml` via `build_condition_tool_guidance.py`;
   `tests/test_guidance_claims.py`):
   - The row `ftd/DaTscan optional only in P04` expects 1 but the cases now give 0 (P04 DaTscan is
     waste, note 4473d085). Remove the P04 DaTscan exception from the guidance and set the claim
     to 0, or to "DaTscan waste in P04".
   - Add M08 CSF recommended, M09 CT optional and toxicology recommended, and the P03
     (recommended) and M05 (optional) ECG exceptions.
   - The other FTD claims pass, including "CT used in 2" and "genetics optional in 27".
4. **Criteria pack** (`dataset-generation/criteria_packs/FTD.md`):
   - Section 2: M08 CSF recommended; M09 CT optional and toxicology recommended; P04 DaTscan
     waste; P03 and M05 ECG; the ALS-panel waste rule; the CT rationale (C22); the dietary-feature
     rule (C7).
   - Section 1: certainty wording (definite once a pathogenic variant is found).
   - Section 8: the new citations `[Armstrong_2013]`, `[Escitalopram_SmPC]`, `[AHS_Evans_2010]`,
     `[CANMAT_ISBD_2018]`, `[EFNS_Wernicke_2010]`, `[NICE_CG115]`, `[NICE_CG100]`, `[NICE_NG50]`,
     `[NICE_NG71]` and `[Betz_2018]`.
5. **Review app display** (CENTRAL.md item 1, null shown as "none"; notes 071a5363, 808af2e1,
   94b68fbc, 68b33e69). CENTRAL.md item 3: the stop rule shows only the tool name (note 0367115d).
6. **Vocabulary**: none needed. The M09 probe showed that `tox_screen` serves the stored blood
   alcohol. The follow-up's stray `BAL` (bronchoalveolar lavage) parameter was removed.
7. **Cross-condition flags for other leads**:
   - The "thiamine before any glucose" wording appears in 21 non-FTD cases (list in FTD.md
     section 4.7): add "never delaying glucose for hypoglycaemia".
   - ALZ-EARLY has templated performance status in 24 cases.
8. **Guard suggestion**: a test that per-case `rejected` labels do not veto a comorbid contributor
   that the case's own musts or differential keep open. The verifiers found three more instances
   after the plan (M07 korsakoff, M08 HIV-associated dementia, P01 hyperammonaemic
   encephalopathy), so a guard would catch the class.

## Check results (16 Nov 2026)

- `perfect_agent.py <id>`, one call per case: 30 of 30 pass.
- `pytest agent-platform/tests/test_case_guards.py -k "FTD-"`: 240 passed.
- `apply_diagnosis_synonyms.py --check --conditions ftd`: would change 0 of 600 cases.
- `pytest test_panel_case_contract.py`: passes.
- `pytest test_guidance_claims.py`: fails. The only FTD row is `ftd/DaTscan optional only in P04`
  (app says 1, cases 0), the intended result of note 4473d085 and CENTRAL item 3. The other
  failing rows belong to ALZ-EARLY, FEPI-TEMP and MS-RR.
- `mri_probe.py` over the 30 cases: no gadolinium text; plain studies only.
