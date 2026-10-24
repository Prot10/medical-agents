# MIG-AURA: condition summary, October 2026 review round

Condition auditor, 24 October 2026. This covers all 30 cases (M01 to M08, P01 to P09, RM11, RS11,
S01 to S11). I read the plan (`plans/MIG-AURA.md`), all 30 case logs and every case file, then ran
scripted uniformity checks over the 30 cases.

## Reviewer notes

MIG-AURA has no reviewer notes: `notes/MIG-AURA.md` and `notes/MIG-AURA.json` do not exist. Every
log says so in its notes table. The physician input was the July 2026 tool guidance
(`condition_tool_guidance.yaml`, Reviewer 1), applied through the plan.

| ruling | count |
| --- | --- |
| FIXED | 0 |
| ALREADY-FIXED | 0 |
| DECLINED | 0 |
| BLOCKED | 0 |

There are no DECLINED or BLOCKED notes.

## Counts

- Cases changed: 30 of 30 (every case file differs from HEAD).
- Approved cases changed: 0. No MIG-AURA case was approved before this round.
- Own findings in the worker tables: 514 FIXED and 6 FLAGGED. The 6 FLAGGED are pre-existing em
  dashes in patient text the workers did not touch (S06 to S11), left alone to avoid churn.
- Verifier corrections recorded under "Verification": about 48, in 25 cases. M08, P02, P04, P06,
  P09 and S06 needed none.
- Auditor corrections: 14, in 13 cases. RM11 got a logged decision but no edit (see below).
- Final checks: `perfect_agent.py` passes 30/30. `case_io.py check` is clean for the condition
  (schema and synonym guard OK, and no test failure names a MIG-AURA case). `test_case_guards.py -k
  MIG-AURA` passes 60 of 60. At baseline the leak guard failed 13 cases.

## Error classes found and how each was fixed

The class letters are those of the plan. Each class was fixed in every case it applied to, and the
scripted checks confirm that.

- **A. Structured history output was a template (30 cases).** It copied HPI sentences, had a
  generic red-flag line and placeholder scores, and its counts contradicted themselves (for
  example "at least two attacks" set true for a first attack). Fix: each output was rewritten
  element by element from the patient's own data, with the SNNOOP10 flags named one by one. I
  recomputed the criterion C count from the six booleans in all 30 cases, and it matches the
  stated "N of 6" in every one.
- **B. Literature outputs (30 cases).** They echoed the scoring key, were empty, or used invented
  sources (REDUCE-AF, Giles 2010, Cammermans 2015, Olesen 2018, Broderick, the "EHF 2022" triptan
  guideline). Fix:
  - Every literature criterion is now optional, takes no arguments, comes last and is left out of
    the stop rule.
  - Empty and patient-specific follow-ups were deleted, as was every initial literature block.
  - At most one literature follow-up remains per case, with a natural query, real citations and
    no conclusions about the patient.
- **C. Drug checks no agent could reach (30 cases).** The criteria used `{"context": ...}`, and the
  outputs were empty, generic or wrong (a sumatriptan-propranolol "interaction" in S04, an
  invented LDL in M03, HRT "avoid" in M05). Fix:
  - Every criterion now has `{"drug": ...}` alternatives. The plan's drug names are present in
    every case (checked by script).
  - Every output has real interactions, contraindications and warnings.
  - Tiers follow plan 3.5: required only where a concrete interaction or contraindication
    changes management.
- **D. Engineering text (30 cases).** Lines such as "July 2026 review applied end to end" and
  "Tier per ..." were deleted everywhere. No such text remains.
- **E. Red herrings pointing at nothing (most cases).** They cited a PFO, WMH, LDL, ECG, Holter,
  CSF or EEG data that did not exist, or had empty paths. Fix: these were deleted or re-pointed.
  Every remaining `field_path` resolves to a real field.
- **F. Differential not updated (P01 to P06, P08, RM11, S11).** Fix: excluded mimics were
  re-graded low or very low, with the result that excludes each one. No differential entry is
  left at high or moderate.
- **G. "Normal DWI excludes TIA."** Fix: replaced everywhere. The class G prohibition was adapted
  to each patient's real aura features (the canonical parenthesis named features some patients
  do not have).
- **H. HRT wrongly prohibited (M05, P01, P05).** Fix: the prohibitions were deleted. The NICE NG23
  must was added where there are menopausal symptoms (M05) or a menopause history (P05).
- **I. Boilerplate prohibitions.**
  - The ergot line was deleted wherever no ergot is in play. S06 keeps a breastfeeding-specific
    ergot prohibition.
  - The canonical UKMEC 4 text is used in every woman of reproductive age with migraine with
    aura. P03 and P07 use an after-stroke variant that offers an IUD.
- **J. Musts that were really tests.** Fix: these became criteria (MRA, MRV, mtDNA, ECG, P05
  monitoring) or referral musts (hemiplegic migraine genetics).
- **K. Vessel findings inside brain MRI reports.** Fix: the vessel text was stripped from every
  brain MRI report, and no MRI report has MRA, MRV, venous flow-void or contrast text any more.
  Vessel imaging is now its own criterion where the plan calls for it: MRA in M03, M07, P01, P02,
  P03, P07, P09 and RS11, and MRV in RM11.
- **L. Placeholder labs (P01, P03, P07, P08, RM11).** Fix: real values with units and ranges, and
  real antiphospholipid panels.
- **M. Junk fallbacks.** Fix: set to null. No junk keys remain.
- **N. Citations.** Fix: one pack key per source. `[Holland_2012]` no longer appears beside an
  oral preventive, and `[Charles_2017]` is no longer cited for PFO. Sources without a pack key
  are named in the text.
- **O. Consults disguised as tests (P04, P06).** Fix: genetic counselling is now a must. In P04 it
  comes before testing.
- **P and Q. Preventive thresholds and teratogenic preventives.** Fix: musts follow the AHS 2021
  thresholds. The canonical topiramate text is used wherever topiramate is proposed for a woman
  who can become pregnant, and valproate is prohibited in those women.
- **Label and data changes.**
  - M01 and M07 were relabelled to probable migraine with aura (ICHD-3 1.5.2), because each HPI
    describes a single attack.
  - P03's HPI now has the 5-hour aura that migrainous infarction requires.
  - P08 gained a stroke-like episode with matching MRI and MRS findings, so the data now support
    MELAS.
  - P09 gained a second affected first-degree relative, so the "familial aneurysm" label holds.
  - S10's MIDAS was corrected to 24 (grade IV).
  - S11's headache and medication days were reconciled.
- **Found by the workers beyond the plan.**
  - Side-locked auras in S01, S02 and S05, an imaging red flag in a case designed to need no
    imaging. The HPIs now say the side alternates.
  - A thunderclap descriptor in M03.
  - Laterality flips in RS11.
  - A timeline impossibility in S06.
  - Answer hints in medication indications ("REQUIRES REVIEW") in 9 cases.

### Fixed by the auditor (each logged under "Condition audit" in the case log)

- **Candesartan without its pregnancy caution (M08, P07, S07, S10).** M06, P03 and S04 already
  said "only with reliable contraception". The caution was added in the four cases that lacked it.
- **Template prohibition (S01).** "Do not co-administer two different triptans within 24 hours"
  was deleted: she takes no triptan and is offered only one.
- **Stale metadata (M05, M07, P01, P02, P04).** The `case_body_concerns` note "check_drug_interactions (only
  fallback)" is no longer true and was removed, as P08, P09, RM11 and RS11 had already done.
- **Empty structured field (M04).** The triptan check's warnings were empty and are now filled.
- **ICD code consistency (S01, S03, S04).** The migraine-without-aura differential entry now uses
  ICD G43.009, as in S06 to S11.

### Checked and confirmed uniform (no change needed)

- `action-3` is required everywhere, comes first and uses
  `structured_headache_history_ichd3`.
- MRI and vessel tiers match the plan 3.5 table in all 30 cases. MRI criteria take no arguments.
  S cases have no imaging criterion.
- Drug-check tiers match plan 3.5. Two deliberate deviations are logged and justified:
  - M05 is recommended because HRT is in the plan.
  - P07 labs are recommended for the APS exclusion and the creatinine and blood count needed to
    dose a DOAC.
- Stop rules list exactly the required criteria. `max_additional_actions` is 0 in S cases and 1
  elsewhere.
- Every sequence constraint is soft, and none involves the literature or drug criteria.
  - History comes before MRI in every case with an MRI criterion.
  - MRI comes before the vessel study in P03, P07, P09 and RM11.
  - MRI comes before echo and monitoring in P03 and P07.
  - MRI comes before genetics in P04, P06 and P08.
- Follow-up order: diagnostic studies first, then the drug check, with literature last.
- No avoided action overlaps a criterion of the same case.
- No ICHD-3 "1.4.1" migrainous infarction, "category 3-4", "CHA2DS2-VASc", "heavy drinker" or
  "confusional aura" text survives.

## Decisions taken at audit (previously open)

- **RM11 label versus data.** `accepted[0]` says "single seizure during aura", but ten fields
  consistently record two aura-triggered seizures. I decided to keep the data:
  - two seizures are still ICHD-3 1.4.4;
  - the source story has two;
  - rewriting ten fields to fit a descriptive clause would be churn.

  The clause is a label wording error, so it goes to CENTRAL. Nothing about it needs Andrea.
- **Pre-existing em dashes.** Untouched patient and metadata text still has em dashes in all 30
  cases. ROUND_POLICY forbids them only in new text, and none of the new text has one, so they
  are left in place.

## CENTRAL requests (consolidated)

1. **Synonyms (`diagnosis_synonyms.yaml`).**
   - G43.109 group:
     - drop "migraine aura", whose tokens are a subset of "migraine without aura" (raised in
       nearly every log);
     - add "probable migraine with aura" (M01 and M07 are relabelled to 1.5.2);
     - add "typical aura without headache", "acephalgic migraine" and "migraine aura without
       headache" (M05);
     - consider "migraine with brainstem aura" and "basilar-type migraine" (M04);
     - "migraine with typical aura" is credited to M07's single attack.
   - New G43.609 group for P03: "migrainous infarction" and "persistent migraine aura with
     cerebral infarction", with codes G43.609, G43.6 and G43.619. Stop the I63 group crediting
     "cardioembolic stroke", "embolic stroke", "lacunar stroke", "lacunar infarct" and plain
     "stroke" in P03. G43.609 and G43.619 were appended to P03's codes by hand: they survive
     `--check` but not `--prune`.
   - P07: restrict to cardioembolic and ischaemic stroke labels, and drop "lacunar stroke",
     "lacunar infarct" and plain "stroke".
2. **Labels (ROUND_POLICY 3: not edited this round).**
   - M01 and M07 were changed to 1.5.2 (plan decision): confirm centrally.
   - M02: the "small PFO, no closure indicated" clause has no supporting data. Suggested
     replacement: "Migraine with combined visual and sensory aura (ICHD-3 1.2.1); combined OCP
     contraindicated (WHO Category 4)".
   - RM11: "single seizure during aura" should become "migraine aura-triggered seizures (ICHD-3
     1.4.4)".
   - P03: `icd_codes[0]` stays I63.9, with G43.609 added (plan default).
3. **Vocabulary.**
   - `order_specialized_test` needs `genetic_panel:hemiplegic_migraine` (CACNA1A, ATP1A2, SCN1A,
     PRRT2) for M03, RM11, RS11 and P09. Until then it is a referral must.
   - MockServer: `order_cardiac_monitoring` has no duration discriminator. P07 needed a separate
     short-recording follow-up so that a 24-hour Holter does not return the loop-recorder AF.
     Consider a duration-aware rule.
4. **Criteria pack `MIG-AURA.md`.**
   - Literature and drug checks are no longer required (ROUND_POLICY 5 and 6).
   - Add these keys to the allow-list, all cited only in the text until they exist:
     - guidelines and statements: `[AHS_2021]`, `[Silberstein_2012]`, `[AHS_neuroimaging_2020]`,
       `[NICE_CG150]`, `[UKMEC_2016]`, `[WHO_MEC_2015]`, `[NICE_NG23]`,
       `[MHRA_topiramate_2024]`, `[EHF_EAN_2021]`, `[ESC_AF_2024]`,
       `[AHA_ASA_2021_secondary]`, `[AHA_UIA_2015]`, `[EAN_CADASIL_2020]`, `[MMS_2017]`;
     - trials: `[PREMIUM_2017]`, `[PRIMA_2016]`, `[MIST_2008]`, `[Voskoboinik_2020]`;
     - further sources the workers used: CRYSTAL AF (Sanna 2014), PHASES (Greving 2014), Tran
       2013 (warfarin reversal), Ng 2019 (MELAS stroke-like episodes), the AHS 2010 triptan-SSRI
       position paper (Evans 2010), NICE TA682, Fisher 1980 and Vongvaivanich 2015.
   - Confirm whether the pack key is `[Sacco_2022]` or `[Sacco_2017]`. The cases use
     `[Sacco_2022]` for the 2022 EHF CGRP update.
5. **Guidance claims (`condition_tool_guidance.yaml`).** Refresh them to show:
   - MRA as a separate study in M03, M07, P01, P02, P03, P07, P09 and RS11;
   - MRV in RM11;
   - echo kept in P03, P07 and P08;
   - an ECG criterion added in P08;
   - RM11's ECG no longer an avoided action;
   - P01 MRI now required.

## Open questions for Andrea (consolidated)

Only these need Andrea. Every other judgment call was decided and logged in its case.

1. **Composition (open since July).** P06 (CADASIL), P07 (cardioembolic stroke) and P08 (MELAS)
   are mimic cases under MIG-AURA. They are kept with their own labels for now. Should they move
   to the stroke or genetic conditions in a later round?
2. **Data added to support a label.** These are invented history details. Please confirm they are
   acceptable as authored data:
   - P09: the sister's 3 mm aneurysm, which makes "familial" true;
   - P03: the 5-hour aura persistence;
   - P08: the prolonged stroke-like episode;
   - P05: the 5-minute build-up added to the structured history.
3. **Policy choices to confirm with the reviewers.** Each is applied in the case already. These
   are calls for the physician panel, not missing data:
   - **P02:** stop apixaban after review with cardiology (CHA2DS2-VA 0).
   - **RM11:**
     - EEG accepts routine as well as video;
     - CSF is left neutral, with no criterion and no avoided action;
     - the ECG avoided action was removed rather than an ECG criterion being added.
   - **P08:** triptan avoidance in MELAS is kept as a prohibition, stated as expert opinion. The
     stored lactate of 2.8 mmol/L was kept instead of the plan's example value of 4.1.
   - **P06:** the strength of the EAN 2020 advice against triptans in CADASIL. The worker could not
     open the guideline text.
   - **S cases:** no MRI waste avoided action (plan question 4).
