# NMDAR-ENC: decisions on the open questions (24 October 2026)

Andrea, 24 Oct 2026: resolve every open point "nel modo migliore per la qualità del dataset". No
physician reviewed this condition, so the condition summary's survey findings were the only safety
net; every fact below was checked on 24 Oct 2026 against the source (abstract or full text).

Verified facts used below:
- Titulaer MJ et al., Neurology 2013;81(12):1058-1063 (full text, PMC3795591): 31 of 661 patients aged
  45 or more; tumours 23% vs 51% in 18-44 (7 of 31: one ovarian teratoma, six carcinomas: breast 2,
  lung 2, thymic 1, ovarian 1); 45% men.
- Schmitt SE et al., Neurology 2012;79(11):1094-1100: extreme delta brush in 7 of 23 adults (30.4%).
- Armangue T et al., Lancet Neurol 2018;17(9):760-772: 14 of 51 (27%) developed autoimmune
  encephalitis after HSV encephalitis, 9 (64%) with NMDAR antibodies, 7 to 61 days after HSVE.
- Gresa-Arribas N et al., Lancet Neurol 2014;13(2):167-177: all 250 patients CSF-positive, 214 serum-
  positive (serum sensitivity 85.6%).
- EAU Guidelines on Testicular Cancer: the 2024 edition is a limited update of the 2023 text
  (Patrikidou A et al., Eur Urol 2023;84(3):289-301); a 2026 edition exists. Pre-orchiectomy markers
  and CT staging are unchanged across editions.

## Step 1: diagnosis synonyms and labels

**Scan of the 30 cases.** Every case accepted, through the G04.81 category entry, "autoimmune
encephalitis", "antibody mediated encephalitis", "autoimmune limbic encephalitis" and code G04.90.
Decision: not granted in the 30 anti-NMDAR cases. Reason: the scorer accepts an answer when every
token of an accepted label occurs in it, so "autoimmune encephalitis" credits "anti-LGI1 autoimmune
encephalitis" and "seronegative autoimmune encephalitis", the alternatives that the differential of
every case lists as excluded by its own panels. "Autoimmune limbic encephalitis" is a separate Graus
2016 syndrome, typically LGI1, GABA-B or onconeural. G04.90 is unspecified encephalitis. This follows
the SAH-P02 precedent (a generic label that credits the wrong answer the case tests). An answer naming
the antibody ("autoimmune encephalitis, anti-NMDAR") still scores, because it contains the NMDAR
labels' tokens. Added "glun1 encephalitis" and "nr1 encephalitis" (current and older names of the
antigen) and code G04.8 (parent of G04.81). Changed: `G04.81` gets `except_cases` with the 30
NMDAR-ENC ids and an explanatory comment, and `G04.81+nmdar` gets the two labels and the G04.8 code.
FEPI-TEMP-P02 (LGI1) keeps its generic labels. Ran `--prune --conditions autoimmune_encephalitis_nmdar`
(30 cases); `--check` is clean for the condition and for all 600 cases. Residual limit (CENTRAL, same
root as the GLIO-HG C71 item): a submitted G04.81 code still credits any autoimmune encephalitis
answer, because ICD-10-CM has no antibody-specific code.

**Summary CENTRAL 3, RP01 label.** Already applied in the round. The synonyms now fit: rerun done,
no change. See also Q1.

**Summary CENTRAL 7, M05 label em dash.** Decision: reword (ruling 3 allows a label correction once
decided; the diagnosis is unchanged). The new label is "Anti-NMDA receptor encephalitis,
tumour-negative (idiopathic), male patient". Changed: M05 `accepted[0]`.

## Step 2: criteria pack (`dataset-generation/criteria_packs/NMDAR-ENC.md`)

Rewritten from plan sections 1 to 3 and the July 2026 tool review (summary CENTRAL 6):
- The probable criteria now follow Graus 2016: four groups, or three with a teratoma, plus an
  abnormal EEG or CSF pleocytosis/OCB. MRI is not a criterion.
- Definite: CSF testing included.
- Serum sensitivity 85.6% (Gresa-Arribas 2014).
- MRI abnormal in about a third.
- Extreme delta brush in 30% (7/23), not "30-50%" or "specific".
- Tumour figures: 38% (Titulaer 2013); 23%, mostly carcinomas, at 45 or older.
- Post-HSV: 27%, 64% NMDAR, 7-61 days, replacing the wrong "5-10%".
- The work-up hierarchy carries the minimal arguments of plan 3.2: no `basic`, `query` or
  `protocol`. The tumour screen is tailored by age and sex.
- cEEG is a recommended escalation.
- DDI is required only with a concrete interaction. Literature is optional only.
- Specialist referral is a must, not a recommended step.
- Sequence: MRI before LP is soft, no longer hard (plan 3.4).
- New section 9 holds the canonical musts and prohibitions.
- Allow-list: the 13 new keys (summary CENTRAL 1) are added with full verified references. Every key
  cited in the 30 cases is now listed (18 keys; `[Solomon_2012]` is listed although no case cites
  it). No key is superseded.

## Step 3: generator block (`conditions.yaml`, `autoimmune_encephalitis_nmdar`)

- Removed the `request_nmdar_antibodies` serum follow-up. It seeded the C4 defect (a separate
  anti-NMDAR labs report carrying CSF values). The serum assay is part of the initial labs.
- Removed `request_repeat_lp`. No case uses it, and it invites a second CSF report that contradicts
  the first.
- Added `request_continuous_eeg`, consistent with the routine EEG (C7), and `request_pelvic_mri`
  for an equivocal adnexal lesion (M03 pattern).
- The CAP CT description is now age 45 or more, with contrast.
- Fixed `key_findings`:
  - CSF "antibodies pending" and "not yet resulted" generated the pending-versus-titre
    contradiction in 14 cases. They now give a final titre, with the low-titre, serum-negative
    pattern for puzzles.
  - "Could be mistaken for primary psychiatric disorder" is not a CSF finding. Replaced by the
    normal glucose ratio.
  - "50% normal MRI" became "about two thirds".
  - "Thyroid function normal (rules out Hashimoto encephalopathy)" is wrong: SREAT is usually
    euthyroid.
- Differential:
  - Hashimoto encephalopathy is now SREAT as a diagnosis of exclusion.
  - Added the other neuronal-surface antibody encephalitides.
- Header comment records the round's rules.
- The difficulty presentations contain no results. Unchanged.

## Step 4: review-app guidance

Three NMDAR claims were stale: cEEG recommended 13 (now 29), pelvic ultrasound in "all 23 women"
(now 21 women aged 12-44) and CAP CT in "3 older men" (now 5 patients aged 45 or older, 2 women and
3 men). The CSF answer also said "the seronegative case remains negative rather than being forced
positive", which RP01's recast made untrue. Updated the four responses in
`build_condition_tool_guidance.py`, regenerated with `--write`, and updated the claim table. I added
one claim, "continuous EEG never required" (no case requires cEEG beyond the routine baseline). All
NMDAR claims pass. The remaining failures are MIG-AURA claims, which belong to the MIG-AURA agent.

## Open questions

**Q1. RP01 label (lead decision flagged for veto).** Decision: keep the recast. RP01 is now
anti-NMDAR encephalitis after COVID-19, CSF anti-GluN1 1:4 and serum negative. Reasons:
- The condition is defined by the antibody. A seronegative autoimmune encephalitis inside it was
  scored with anti-NMDAR synonyms, so the key rewarded the wrong answer.
- CSF-positive, serum-negative disease is documented in about 14% of patients (Gresa-Arribas 2014),
  and the criteria pack lists it as a red herring.
- Graus 2016 makes the CSF assay sufficient for definite disease, with normal cells and absent OCB
  allowed.
- A seronegative mimic would belong to a seronegative-AE condition the benchmark does not have.
Nothing here needs information only Andrea has: the source case (PMC9799706) is a seed, not a
record the benchmark must reproduce. No change beyond the round.

## Auditor flags and judgment calls (summary)

- M01 serum 1:80 / CSF 1:128 and the mixed series in 10 cases: confirmed. Serum and CSF are titrated
  from different starting dilutions, and no value falls outside a series. No change.
- M03 and M04 MRI side differs from the EEG focus: confirmed. These are different phenomena in a
  diffuse disease, and M03's facial droop matches its MRI. No change.
- M04 "hemorrhage" in British prose: fixed ("haemorrhage").
- P01 serum glucose 92 at LP vs 100 in labs: kept. Different sampling times, and the ratio is normal
  either way.
- P01 clock drawing "numbers clustered on the right side": fixed. It implied left neglect with no
  other right-hemisphere sign. It now reads "unevenly spaced numbers and misplaced hands".
- RS02 without beta-hCG (postmenopausal since 48): confirmed. The pack's rule now excepts
  postmenopausal women.
- RP01 without amyloid-PET/DaTscan waste and without a seizure must: confirmed.
- RP02 open questions settled by the verifier: confirmed.
- Level of care per rule M6: confirmed.
- P08 in the plan's SIADH row with Na 130: confirmed that it has no SIADH criterion.
- Criterion ids (`ceeg-escalation` vs old ids; `siadh-workup` vs `siadh-osmolality-workup`): not
  unified. They are referenced only inside each case, and renaming adds churn without effect. The
  pack no longer prescribes the capitalised id that the schema rejects.
- **Summary CENTRAL 9, RP02 `case_body_concerns`.** Decision: the case stays in this condition.
  CSF anti-GluN1 is positive, so ICI-associated anti-NMDAR encephalitis is anti-NMDAR encephalitis;
  Graus 2021 classifies ICI-induced syndromes by their antibody. The policy encodes nivolumab
  withdrawal (ASCO 2021) and the interactions. The concern now describes a resolved item and was
  removed, as RP01's were.
- **Summary CENTRAL 10, difficulty field.** Dataset-wide and not NMDAR-specific. Left to central (below).

## Cases changed in the close-out

All 30 by the synonym prune (generic labels and G04.90 removed; two labels and G04.8 added). In
addition: M04 (spelling), M05 (label wording), P01 (clock drawing), RP02 (metadata concern). Each log
has a "## Close-out (24 Oct 2026)" section. Checks: `perfect_agent.py` 30/30; `case_io.py check` on
all 30: schema OK, synonym guard OK, no test failure names an NMDAR-ENC case;
`test_case_guards.py -k NMDAR-ENC-` 60 passed; `apply_diagnosis_synonyms.py --check --conditions
autoimmune_encephalitis_nmdar` clean; NMDAR guidance claims pass.

## Still needing Andrea

Nothing that needs information only Andrea has. For the physicians at first review: the whole
condition is unreviewed, and the scoring change in Step 1 means a plain "autoimmune encephalitis"
answer no longer scores.

## CENTRAL

Vocabulary: none. Every argument value in the 30 cases' criteria and avoided actions is in
`costs.yaml`, and no log requests a new term.

Code and tests (from summary CENTRAL 2, 4, 5, 8, 10; not made here):
1. Non-schema criterion keys: `analyze_csf.basic` (63 case files dataset-wide) and
   `check_drug_interactions.screen_for` make criteria unreachable while `perfect_agent.py` passes.
   Strip annotation keys before matching, or add a test that rejects non-schema criterion keys.
2. A case fallback for `order_advanced_imaging` / `order_specialized_test` is served for every
   modality or test type (already in CENTRAL_PENDING). NMDAR-ENC nulled its fallbacks.
3. A test that flags `query` in a literature criterion's `required_arguments` (string-equality
   match).
4. `perfect_agent.py` prints "<- ?" for initial outputs with null fields (cosmetic).
5. Scorer: a submitted G04.81 code credits any autoimmune encephalitis answer (no antibody-specific
   ICD-10 code). This has the same root as the GLIO-HG C71 and ICD-code-alone items.
6. Difficulty field (dataset-wide): every S and RS case is `moderate`, with expected confidence
   0.80-0.85.
