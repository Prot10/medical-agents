# SYNC-CARD: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Sources: the plan (`plans/SYNC-CARD.md`), the 30 case logs
(`logs/SYNC-CARD-*.md`, each with a worker table and a verifier section, and for 25 cases a
"Condition audit (24 Oct 2026)" section), and scripted checks over the 30 case files (M01 to M05,
P01 to P04, RM01 to RM04, RP01 to RP05, RS01 to RS06, S01 to S06). SYNC-CARD has never been
annotated by a physician: there is no `notes/SYNC-CARD.md` or `.json`, so there are no note ids
to rule on. Every change comes from the lead survey, the workers, the verifiers or this audit.
All 30 cases are `draft` (`policy_spec_status` and `review_status`); none was approved before the
round.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass.
- `case_io.py check` on all 30 ids: schema OK and synonym guard OK for every case. The suite's 15
  failures are elsewhere and none names a SYNC-CARD case.
- `test_case_guards -k SYNC-CARD`: 60 passed (leak guard, hijacked index orders, banned strings).
- `discriminator_defects` and `hijacked_index_orders` run by hand on SYNC-CARD (not yet in
  `DISCRIMINATOR_CONDITIONS`): no defect in any of the 30 cases.
- Routing probe through `NeuroBenchEnvironment` on every case:
  - two generic literature queries ("syncope guidelines", "syncope evaluation") return the neutral
    initial literature block, never a disease-specific follow-up;
  - a query naming the condition (the follow-up's trigger words) returns that case's literature
    follow-up in all cases;
  - an unrelated drug (ibuprofen) returns the medication-list review;
  - tilt and exercise orders return this patient's report or "not performed", never the library
    normal where the library normal contradicts the case.
- Scripted uniformity checks, clean after the audit fixes:
  - stop rule lists every required criterion; `max_additional_actions` 2 for M and S, 3 for P and R;
  - sequence constraints: ECG before echo and ECG before monitoring (soft), TTE before any exercise
    criterion (hard), each with the plan's reason;
  - monitoring criteria accept telemetry, holter_24h and holter_48h; the case fallback equals the
    monitoring follow-up;
  - literature criterion optional and last in followup_outputs;
  - citation keys only `[ESC_2018]`, `[ACC_AHA_HRS_2017]`, `[EGSYS_2008]`, `[ROSE_2010]`,
    `[Strickberger_2006]`, `[Locati_2014]`; other guidelines are named in rationale text;
  - "CHA2DS2-VA" only, never "CHA2DS2-VASc"; no isoproterenol in a tilt report; no tool names or
    pipeline text in clinical text;
  - drug, lab, CMR, tilt, exercise, EEG, MRI, CSF and head-CT tiers match the plan or a logged and
    justified deviation;
  - differentials: non-low entries only where the results support them (RM02 ARF high and familial
    moderate; RM03 and RP04 familial moderate; RS01 LMNA high and sarcoid moderate; S02 and S04 AS
    moderate).
- Remaining hits of the banned-string scan are not defects: em dashes in text written before the
  round (the policy bans them in new text only), and "serotonergic" in the RP03 and RS01 drug
  reviews (escitalopram and a triptan; the plan's ban was on the P03 prohibition only). Red
  herrings that quote a structured lab or medication entry rather than prose are renderings of
  that entry and are acceptable.

## Error classes and how each was fixed

Plan classes, applied by the workers and checked by the verifiers:

- **A. Literature scored as work-up (all 30).** Literature criterion set optional and removed from
  the stop rule; invented references (RM01 Matsumoto, Saiz; P01 "2020 Revised Task Force"; the P03
  Antzelevitch title) removed; at most two literature follow-ups, placed last, with real guideline
  content and no conclusion about the patient; "Not retrieved" fallbacks deleted. The plan's step 2
  (delete every initial literature block) was not kept as written, see audit class P.
- **B. Drug interaction check (all 30).** Drug criterion optional or avoided per plan; the leaking
  "general" blocks deleted; per-drug follow-ups rewritten to labelled interactions only. Where the
  workers kept a medication-list review in `initial_tool_outputs.drug_interactions` (M01, M02, M03
  and others, logged), the reason is the tier-2 leak (class P).
- **C. Laboratory panels (all 30).** Panels pinned to the plan tier; reference ranges and
  abnormal flags made consistent (e.g. M01 Hct flagged low inside its range). Logged deviations:
  calcium alone rather than calcium plus ACE in the sarcoid case; troponin added where the history
  makes it targeted (RS02, RS03); beta-hCG pinned in RM04.
- **D. Sequence constraints and stop rule (all 30).** Rewritten to the canonical constraints and
  the full required list.
- **E. Monitoring modality mismatch (about 20).** Alternatives widened to telemetry, holter_24h
  and holter_48h; the fallback set equal to the stored monitoring report; "Continuous telemetry"
  removed as a monitor_type value.
- **F. Studies stored under the wrong tool.** Moved to the right tool (e.g. RM01 PSG under
  `order_specialized_test`, chest CT under `body_imaging`); genetic results stay under
  `interpret_labs` panel `genetic` until C2 lands.
- **G. Placeholder or wrong-voice reports.** Replaced with full reports in the tool's voice.
- **H. Engineering and pipeline text.** Removed ("cited via", "citation_gap", "on this pathway").
- **I. Boilerplate musts and prohibitions.** Replaced with case-specific ones, at most 5
  prohibitions.
- **J. Avoided actions.** Tilt, exercise, EEG, MRI, CSF set per plan. Logged deviation: tilt and
  exercise follow-ups kept and cleaned (no isoproterenol, the patient's own rates) instead of
  deleted, so a wasted order is not answered by a library normal at HR 68. Head CT is recommended
  instead of avoided in M03, RS02, RS03 and S01, where the fall caused a head injury that meets
  NICE NG232; the plan row that avoids head CT there contradicts NG232.
- **K. Differentials.** Likelihoods updated to the pathway results.
- **L. Red herrings.** Paths fixed and data_points quoted from the case (finished by this audit,
  class S).
- **M. Template carry-over.** Copied numbers replaced with values consistent within each case
  (e.g. RS03 against RS02).
- **N. Patient-block leaks.** Diagnosis-naming phrases removed from the patient block.
- **O. Kind 1 leakage inside reports.** Reports describe findings without naming the diagnosis or
  the decision; leak guard passes on all 30.

Classes found by this audit and fixed:

- **P. Tier-2 literature leak (24 cases).** With no initial literature output, MockServer tier 2
  answers ANY literature query with the first stored follow-up, which names the diagnosis. Fix:
  added the neutral `initial_tool_outputs.literature_search.general` block (syncope initial
  evaluation and risk stratification, ESC 2018 and ACC/AHA/HRS 2017, no diagnosis) already used in
  P02 to P04 and RM01 to RM03, to M01 to M05, P01, RM04, RP01 to RP05, RS01 to RS06 and S01 to S06.
- **Q. Generic literature triggers (13 cases).** Triggers whose only meaningful tokens were
  generic (management, guidelines, diagnosis, syncope) would still match a generic query in tier 1.
  Renamed to the condition's own words in M04, M05, P01, RM04, RP01 to RP05, RS01, RS04, RS06 and
  S05.
- **R. Drug and library contradictions in S01 to S06 (6 cases).**
  - drug texts asserted results the agent has not obtained ("while AV conduction disease is
    unpaced", "meets the labelled dose", device-implantation warnings, eGFR-specific metformin and
    cefazolin lines); rewritten as conditional labelled rules;
  - `initial_tool_outputs.drug_interactions` set to the medication-list review so an unrelated
    drug does not receive a per-drug follow-up;
  - "not performed" follow-ups added for tilt and exercise, because the library normal tilt (HR 68)
    and normal exercise test (10.4 METs) contradict high-grade AV block.
- **S. Red-herring quotes (6 cases).** data_points made verbatim in M01, M02, M03 (two), M04 and
  RM04; M05's red herring cited a PCP attribution absent from the PMH and now quotes the HPI.
- **T. Exercise testing in torsades (M04, P04).** M04: exercise testing added as an avoided action
  of severity harm (recurrent pause-dependent torsades, Fletcher 2013), with a "not performed"
  follow-up. P04: the exercise test moved from recommended to optional (QTc 510 ms and captured
  torsades already establish the diagnosis; testing waits for beta-blockade, ESC 2022), the hard
  TTE-before-exercise constraint kept.

## Counts

- Notes FIXED / ALREADY-FIXED / DECLINED / BLOCKED: 0 / 0 / 0 / 0 (no notes file for SYNC-CARD).
- Own findings, workers: 543 rows in the 30 logs, all FIXED; the verifiers' further fixes are in
  each log's Verification section.
- Own findings, this audit: 64 fixed across 25 cases (24 initial literature blocks, 13 trigger
  renames, 18 S01 to S06 drug and tilt or exercise items, 7 red-herring quotes, M04 exercise harm,
  P04 exercise tier); 3 flagged and not fixable in case data (library exercise report age, tier-2
  mechanism, the plan's head-CT row), listed under CENTRAL.
- Cases changed in the round: 30 of 30. Changed by this audit: 25 (all but P02, P03, RM01, RM02,
  RM03).
- Approved cases changed: 0 (none of the 30 was approved).

## DECLINED and BLOCKED notes

None: there are no reviewer notes for SYNC-CARD.

## CENTRAL requests (consolidated)

- **C1. Diagnosis synonyms** (`diagnosis_synonyms.yaml`):
  - remove the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia",
    "conduction disease syncope", "tachyarrhythmia" (29 of 30 cases accept "cardiac syncope", so
    diagnosis scoring is trivial), and RM01's "sleep related bradyarrhythmia" and "nocturnal
    asystole" unless a specific label is also required;
  - remove R55 from the I44 code list;
  - split I47 so SVT and AVNRT (I47.1) and VT (I47.2) are distinct: P01 (ARVC), RP03 (CPVT) and
    RS05 (VT) accept SVT or AVNRT, and M05 (AVNRT) accepts VT;
  - remove "mobitz ii" and "second degree av block" from complete-heart-block cases (including the
    RP04 loop-recorder case, which shows neither);
  - RP05: remove "complete heart block" so the sarcoid diagnosis must be named;
  - RM02: add a rheumatic carditis label ("rheumatic carditis with heart block") and I01.x;
  - M04: icd_codes[0] T46.2X5A is wrong for azithromycin, ondansetron and citalopram; use I45.81
    primary with T36.3X5A, T45.0X5A and T43.225A.
- **C2. Vocabulary** (costs.yaml with library reports and the tool_io.py mirror):
  `electrophysiology_study` and `sodium_channel_blocker_challenge` under order_specialized_test;
  genetic panels `inherited_arrhythmia` and `cardiomyopathy`; `orthostatic_blood_pressure` under
  perform_clinical_assessment; whole-body FDG-PET for tumour search (the existing `FDG_PET` is
  cerebral); coronary angiography. Until then these live in musts only.
- **C3. Library.**
  - Add a "no study stored for this order" answer: the normal tilt (HR 68), normal monitoring,
    normal exercise, normal TEE and normal mediastinum MRI reports contradict many cases, which this
    round covers with per-case "not performed" follow-ups.
  - The fixed exercise report ("peak 158 bpm, 93%" of predicted) is age-inconsistent for most
    patients (e.g. 93% at 71 years is about 139 bpm); make the percentage or the rate generic.
  - The tier-2 rule (the first unserved follow-up answers any call to a tool without an initial
    output) leaks disease-specific literature and drug reviews; this round neutralises it per case
    with initial blocks. A code-level fix, or a guard that fails a case whose literature or drug
    tool has follow-ups but no initial output, would stop it recurring.
- **C4. Citation keys.** ESC 2021 pacing, ACC/AHA/HRS 2018 bradycardia, ESC 2022 VA/SCD, ESC 2023
  cardiomyopathies, ESC 2019 SVT, ESC 2019 PE (Konstantinides 2020), ESC/EACTS 2021 VHD, ESC 2024
  AF, 2010 ARVC Task Force, HRS 2014 sarcoid (Birnie 2014), ATS 2020 sarcoidosis (Crouser 2020, new
  beyond the plan), O'Mahony 2014, Drew 2010, Gewitz 2015, Graus 2021, NICE NG232, Fletcher 2013.
  Criteria resting on these have empty `citations` and name the source in the rationale.
- **C5.** Verify the reference behind `[Locati_2014]` (the pack says Heart 2016; possibly the
  SYNARR-Flash study, Europace 2016;18:1265-1272) and correct the key or its entry.
- **C6. BANNED table for SYNC-CARD** in test_case_guards.py: "Do not call `", "cited via",
  "citation_gap", "Not retrieved on this pathway", "on this case's pathway", "on this pathway",
  "CHA2DS2-VASc", and "Continuous telemetry" as a monitor_type value.
- **C7. Guard.** Fail a tilt report containing "isoproterenol" in a case whose history lists
  ischaemic heart disease, AS or HCM.
- **C8. Review UI.** Show stop-rule criteria and sequence constraints next to the action criteria.
- **C9. Add SYNC-CARD to `DISCRIMINATOR_CONDITIONS`.** Its data is already clean under the guard.
- **Plan defects for the lead and future rounds:** plan A step 2 and plan B step 1 (delete every
  initial literature and drug output) trigger the tier-2 leak and must not be applied as written;
  the plan's head-CT avoid row contradicts NICE NG232 when the syncope caused a head injury.

## Open questions for Andrea

- **Q1. RM01 placement.** RM01 (anti-Hu brainstem encephalitis with central sleep apnoea and sleep
  asystole) is a neurological cause of syncope-like events, not cardiac syncope. It stays in
  SYNC-CARD with its data repaired. Should it move to a paraneoplastic or autoimmune condition?
  This is a dataset-structure choice.
- **Q2. RM01 source fidelity.** RM01 is seeded from PMC11623976 (MedCaseReasoning, CC-BY). The
  plan's repairs (no prolonged CPR, a dorsal medullary MRI lesion) may depart from the published
  case, which the worker could not open. Does fidelity to the source matter for this dataset?
- **Q3. M04 primary ICD code.** Confirm that CENTRAL owns the change of icd_codes[0] from T46.2X5A
  to I45.81 (it touches the scorer through the synonyms file); workers left it unchanged.
