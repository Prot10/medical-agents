# PD: condition audit summary (November 2026 round)

Auditor pass, 17 Nov 2026, after the workers and verifiers. Plan: `plans/PD.md`. Decisions:
`plans/PD-decisions.md` (D1..D32). Audit scripts and outputs are in
`/home/aprotani/review-round-2026-11/work/scratch/pd-auditor/`:
- `book.py`: notes against rulings and logs;
- `survey.py` / `survey.txt`: tiers, stop rules, constraints and avoided actions;
- `textcheck.py`, `f4check.py`, `collide.py`, `orphans.py`: class and consistency measures;
- `leak_t0.py`, `leak_out.py`, `xmod.py`: the blind leak pass.

## Bookkeeping

- There are 47 notes, all from R1. Each note id appears in exactly one `work/rulings/<CASE>.json`
  (its own case), with no extra ids.
- Ruling counts: **FIXED 46, NO-ACTION 1** (5b975043, P02 "tutto ok"). DECLINED 0, ALREADY-FIXED
  0, CENTRAL 0, NEEDS-ANDREA 0.
- All 30 cases changed since 06b74446, and each has a log with `## Changes`.
- Approved cases: none (`work/approved.txt` lists no PD case).

## Classes: how they were fixed (before -> after, scripted over the 30 cases)

| class | before | after |
|---|---|---|
| C1 TIER-MRI / stop rule (D1) | imaging required and in the stop rule in 30/30 (29 MRI, S06 CT) | required in 15 (each with a written reason), optional in 15 with the canonical label and rationale (14 MRI, 1 CT) and the D1 key-evidence form in all 15. Empty stop rule in 14 (S01-S06, RS01, RS03-RS05, M04, M05, RM03, RM04); RM05 [drug check] |
| C2 SEQUENCE, MRI before DaTscan (D2) | 13 soft constraints | 1 (RP05, case-specific reason, no citation) |
| C3 provisional diagnosis on metoclopramide (D3) | 3 | M01-M03: new `accepted[0]`, canonical REQ[0] and REQ[2], new prohibition |
| C4 domperidone "after an ECG" (D4) | 4 (M01-M03, RM05) | 0 |
| C5 MDS rigidity / bradykinesia (D5) | cogwheel-only rigidity without rest tremor in 4 (M01, M02, M03, P02); no decrement in RM04, plus P01 found in this audit | 0 / 0 |
| C6 near-duplicate triad (D6) | M01-M03 shared a chief complaint and an exam sentence | distinct chief complaints and teaching points |
| C7 family history / handedness (D7, D8) | M02 (+P04); M05 (+S06) | fixed |
| C8 swallow-tail (D9) | 5 evidence lines | all 5 in the non-specific D9 wording |
| C9 ECG (D10, D21) | P01 ECG listed as waste; P02 must demanding an unordered ECG; RP01 ECG recommended | P01 and P02 recommended with stored normal ECGs; RP01 required and in the stop rule; ECG waste 18 -> 17 |
| C10 levodopa trial / propranolol / first line (D11, D13, D15) | "1000 mg/day" mandatory in P03 and RP03; "levodopa does not treat" in 2; "are all options" in 1 | conditional; 0; 0 (P01 symptomatic trial kept) |
| C11 psychiatric, orthopaedic, cardiac, surgical and device musts (D14, D16, D21-D24, D26, D27) | 11 notes | canonical texts in place (bipolar musts in RM02 and RS01 consistent with no agonist warning that contradicts them) |
| C12 differential / certainty (D19, D20, D25, D31) | 4 notes | fixed |
| C13 Pisa (D28) | RS03, 6 fields | exam documents lateral flexion of 8 degrees, reversible; "Pisa" survives only as the >10-degree threshold reference |
| C14 rejected labels true in the case (D30) | 5 cases (RP01, RM04, RM02, RS01, M02) | 0. The remaining `essential tremor` rejections were checked: ET is in a relative only, never in the patient |
| LIT / MRI-CONTRAST (D32) | n/a | no literature criterion, initial, follow-up or fallback output left in any PD case |

Avoided actions and criteria: no call matches both a criterion and an avoided action, in any tier.
Every stop-rule id is a required criterion.

## Stragglers fixed in this audit (through case_io, logged under `## Verification`)

1. **F4, optional result without "if obtained"** (S04, S05, S06). `key_clinical_evidence[1]`
   gave the UPSIT score of the optional smell test as plain fact. ", if obtained" was added. The
   other cases already used the form.
2. **Blind leak** (M01, M02, M03). The drug-interaction report, which is required in these cases,
   ended "metoclopramide is also contraindicated in Parkinson's disease". That names the
   diagnosis the case asks for (PD versus pure drug-induced parkinsonism). The clause was deleted.
   The levodopa contraindication and the "causes and worsens parkinsonism" interaction line stay.
   The clause was already present at 06b74446.
3. **D5 class extension** (P01, MSA-P). Bradykinesia was stated without decrement. MDS 2022 MSA
   parkinsonism uses the MDS 2015 bradykinesia definition (note 92ca20f9's point). The sentence
   now documents progressive decrement.

All 7 cases were re-checked afterwards: perfect_agent and the case_io schema and synonym guard
pass.

## Blind leak pass

The turn-0 prompt was rendered with the real `format_patient_info`.
- No case names its own diagnosis, except where the encounter is a follow-up of known PD (RM01,
  RM05, RP04: established PD, in the HPI, history and medication indications by design).
- Relatives with PD (RM03, RM05, RS01, RS02, RS05, S01) are family history, not the patient's
  diagnosis.
- No ordered result appears in the patient block. The prior results present are pre-encounter
  history: RP01's WPW ECG at 42, RS05's TSH 14 months ago, RM04's cervical spine MRI, M04's UPSIT
  in the exam (no olfactory criterion there).

Stored outputs:
- After fix 2, no drug-interaction output names a diagnosis.
- The drug reports share only category-level management phrases with the musts ("lying and
  standing blood pressure at each step"). RM05's report carries the D4 text, as the plan
  specified.
- The remaining diagnosis names in reports follow the style guide's hedged pattern form:
  - P01 MRI: "a pattern that can be seen in MSA-P" (an MDS 2022 MRI marker);
  - P01 and RP03 FDG fallbacks: "pattern consistent with a ... MSA metabolic profile";
  - the gene-panel test name `genetic_panel:PD`.
- No report synthesises across modalities. The only hits were the PSG montage listing ECG
  channels, RS02 "stable compared to prior examinations", and S06's CT stating its own lower
  sensitivity.

## Deviations from the plan (checked, kept)

- **RM05: thyroid function moved from recommended to required, outside the stop rule** (worker).
  With the MRI optional, the only required criterion was the zero-cost medication review, which
  `test_no_case_has_a_free_required_set` rejects. The TSH is due and clinically indicated: she is
  on levothyroxine, the last TSH was 6 months ago, and she has new slowing (ATA 2014). Note
  8de3e101 asks to reassess thyroid function.
- **RP01 EPS report: right posteroseptal accessory pathway** (the plan text said left lateral).
  The stored ECG has positive delta waves in I and aVL. A left lateral pathway would make them
  negative, so posteroseptal is the consistent localisation. The risk values are as in D21.
- **Stored follow-ups with no criterion** (e.g. the olfactory test in S01-S03, timed gait and
  cognitive screens) are truthful answers to neutral orders, by dataset design. S01-S03 cite the
  UPSIT only in the "when tested / if obtained" form.

## Label and code changes (CENTRAL 1: synonyms)

- M01, M02, M03 `accepted[0]`: "Degenerative parkinsonism, probably Parkinson's disease, unmasked
  by metoclopramide (to be confirmed after withdrawal)".
- RM01 `accepted[0]`: "Parkinson's disease with motor worsening and episodic saccadic freezing on
  low-dose levodopa (possibly dopamine-responsive)".
- `icd_codes[0]` is unchanged in all four (G20.A1).
- Rejected labels removed (D30): RP01 `wolff parkinson white`, `WPW`; RM04 `adhesive capsulitis`,
  `frozen shoulder`; RM02 `post encephalitic parkinsonism`, `postencephalitic`; RS01
  `lithium induced tremor`; M02 `essential tremor`.
- `DiagnosisCriterion.matches`, re-tested 17 Nov:
  - "Parkinson's disease unmasked by metoclopramide" and "probable Parkinson's disease" match
    (M01-M03);
  - "drug-induced parkinsonism" does not match;
  - M02 "PD with coexisting essential tremor" matches;
  - RM01 "Parkinson's disease with saccadic freezing" matches and "progressive supranuclear
    palsy" does not.
- `apply_diagnosis_synonyms.py --check` passes. The orchestrator should still confirm the yaml
  entries carry the new `accepted[0]` texts.

## CENTRAL requests (consolidated)

1. **Synonyms**: confirm the four new `accepted[0]` labels above in `diagnosis_synonyms.yaml`.
   The check is already clean.
2. **Pack** `dataset-generation/criteria_packs/PD.md`:
   - section 2 tiers (MRI required 15 / optional 15; DaTscan RP05 optional, RM05 waste; MIBG RP02
     optional; Wilson labs P04 optional; thyroid RM05 required; ECG recommended P01 and P02,
     required RP01; EPS recommended RP01);
   - section 5: one soft constraint (RP05);
   - new keys `[ESC_SVT_2019]`, `[EMA_Domperidone_2014]`, `[ACG_Gastroparesis_2022]`,
     `[Tinazzi_2022]`, `[Follett_2010]`, `[ATA_2014]`;
   - facts F1-F5.
3. **Guidance answers** (`condition_tool_guidance.yaml` / `build_condition_tool_guidance.py`).
   Stale PD claims in `test_guidance_claims.py`:
   - `pd/MRI required in 29`: the cases say 15;
   - `pd/CT alternative required in 1`: the cases say 0;
   - `pd/labs required P04, recommended RM02 RM05 RS01, optional 5`: the cases say required
     [RM05], recommended [RM02, RS01], optional 6;
   - `pd/ECG only in RP01, recommended, waste in 18`: the cases say [P01, P02], 3, 17. RP01 is now
     required.
4. **Generator** `conditions.yaml` (parkinsons block): `required_modalities: [MRI]` becomes MRI
   conditional on atypical features or a structural question.
5. **Benchmark property** (no code change): 14 PD cases have no required criterion. A correct
   clinical diagnosis with no test scores 1.0. This belongs in the paper's description of the PD
   condition.
6. **NPH lead**: pre-MRI verification of programmable shunt valves (D27). 31 NPH cases and
   FEPI-TEMP-RM01 mention them.
7. **Review-app display**: null `clinical_significance` on abnormal rows is shown as "none" (e.g.
   RS04 glucose and HbA1c in known treated diabetes; no management gap). Show "not stated".

## For Andrea (information, nothing blocking)

- (a) The 14 zero-required PD cases (CENTRAL 5).
- (b) The D6 composition choice: M03 is kept as the DaTscan-only member of the graded
  metoclopramide triad. It could be replaced by a different dopamine-blocker scenario in a later
  round.

For the physicians at re-review:
- the RP01 EPS result (constructed, low risk);
- the P04 Wilson labs, optional rather than recommended (D12).

## Check results (17 Nov 2026, after the audit fixes)

- `perfect_agent.py` for each of the 30 cases, one id per call: 30/30 pass.
- `pytest test_case_guards.py -k "PD-"`: 240 passed.
- `apply_diagnosis_synonyms.py --check --conditions parkinsons`: "would change 0 of 600 cases".
- `pytest test_panel_case_contract.py test_red_herring_paths_resolve.py`: 4 passed.
- `pytest test_guidance_claims.py`: fails, with the 4 stale PD claims listed in CENTRAL 3 (the
  orchestrator updates them). The FND claims fail too, outside PD.
- `case_io.py check` on the 7 audit-edited cases:
  - schema and synonym guard OK;
  - the full suite has 2 failures. Among the failures that name PD, only the test_guidance_claims
    PD rows appear. The other failure does not name PD.
