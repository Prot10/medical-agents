# PD: close-out decisions (24 October 2026)

Close-out of PD (condition enum `parkinsons`) under `CLOSEOUT_BRIEF.md` (Andrea, 24 Oct 2026: "per i
punti aperti, risolvili nel modo migliore per la qualità del dataset"). Inputs: `plans/PD.md`
(classes C1 to C23, section 3, CENTRAL R1 to R10, Q1 to Q6) and `plans/PD-summary.md` (CENTRAL R1
to R11, open questions, auditor flags). There is no reviewer notes file for PD; the only physician
input is Reviewer 1's July 2026 tool guidance. Decisions the orchestrator took are applied, not
reopened. Every case log ends with a "Close-out (24 Oct 2026)" section (all 30 changed). Nothing is
committed.

Sources checked on 24 Oct 2026:
- ICD-10-CM FY2026 (CMS/NCHS tabular as reproduced by AAPC Codify and coding references): G90.3
  "Multi-system degeneration of the autonomic nervous system" (inclusion: neurogenic orthostatic
  hypotension [Shy-Drager]; index "Degeneration, multi-system" G90.3); G23.2 "Striatonigral
  degeneration"; no G23.3 in ICD-10-CM. G20.A1 to G20.B2 and G20.C "Parkinsonism, unspecified"
  are the FY2024 split of G20 (ASHA and ACDIS summaries of the FY2024 code set; ICD10monitor on the
  April 2026 index change that sends "Parkinson's disease" to G20.A1 rather than G20.C).
- WHO ICD-10 and ICD-10-GM (BfArM via gesund.bund.de; an NHS coding note that MSA "previously (all
  previous editions) trailed to G90.3"): G23.2 MSA, parkinsonian type [MSA-P]; G23.3 MSA,
  cerebellar type [MSA-C].
- Socha P et al. EASL-ERN Clinical Practice Guidelines on Wilson's disease. J Hepatol
  2025;82(4):690-728, doi 10.1016/j.jhep.2024.11.007 (supersedes EASL 2012; Leipzig score kept,
  relative exchangeable copper added; read from the abstract and summaries, not the full text).
- The other pack references (Postuma 2015, Berg 2015, Marshall 2009, Schwarz 2014, Tolosa 2021,
  NICE NG71, Wenning 2022, McKeith 2017, Höglinger 2017, Litvan 2012, Brignole 2018) carry their
  standard bibliographic data in the pack.

## Orchestrator decisions applied

**O1. Mimic cases stay in condition PD with their ids** (P01 MSA-P, P02 DLB, P03 PSP-RS, RP03 MSA
mixed; ROUND_POLICY ruling 3, precedent ALS-P02 and the MG LEMS cases). Summary question 1 is
closed. `metadata.case_body_concerns` (the "re-prefix or accept" note) cleared in the four cases;
the pack section 7 records them. For the paper: PD is 26 PD cases and 4 PD-mimic cases (R8).

**O2. A PD answer does not score in a mimic case, and a mimic answer does not score in a PD case.**
Checked with `DiagnosisCriterion.matches` over the 30 cases against 26 answers (PD, PD dementia,
MSA, MSA-P, MSA-C, DLB, Lewy body dementia, PSP, Richardson syndrome, drug-induced and vascular
parkinsonism, parkinsonism unspecified, ET, CBD, NPH, Parkinson-plus) and every differential entry
with its ICD code: no cross-credit in either direction, before or after the change. ("Parkinsonian"
is not the token "parkinson", so "multiple system atrophy parkinsonian type" never matches a PD
label.) The two code-level holes found are closed in S1.

**O3. RP02 MIBG note kept** as the auditor decided (R11); listed for the physicians below.

## Synonyms (`diagnosis_synonyms.yaml`; applied with `--prune --conditions parkinsons`)

**S1. G20 codes scoped to the case's motor complications.** The G20 entry granted G20, G20.A1,
G20.A2, G20.B1, G20.B2 and G20.C to every PD case. Decided:
- G20.C is "Parkinsonism, unspecified", not PD. Since the scorer accepts a code on its own, a
  "parkinsonism, likely drug-induced" or "atypical parkinsonism" answer coded G20.C scored as
  correct, which is the error M01 to M03, RP01 and RP02 test. Removed everywhere.
- The complication codes now follow the case, as FEPI-TEMP did for intractability: base entry
  G20 only; G20.A1 is the primary of the 24 cases without dyskinesia or fluctuations; RM05
  (wearing-off, denies dyskinesia; primary G20.A2) also accepts G20.A1 ("without mention of
  fluctuations", the PD NOS code); RP04 (fluctuations and peak-dose dyskinesia; primary G20.B2)
  also accepts G20.B1 ("with dyskinesia, without mention of fluctuations") and not G20.A1/A2
  ("without dyskinesia"). New entries `G20.A2` and `G20.B2` (keyed by the exact primary code).
- Labels unchanged (parkinson disease, parkinson's disease, parkinsons disease, idiopathic ...,
  PD).

**S2. MSA labels and codes (summary R6 and question 2).** Decision: `icd_codes[0]` stays **G90.3** in
P01 and RP03. Reason: the dataset codes in ICD-10-CM throughout (G20.A1, G35.A, G40.209), and
ICD-10-CM FY2026 still sends MSA to G90.3; G23.2 there is "Striatonigral degeneration" and G23.3
does not exist. The 20 MSA differential entries in the PD cases also use G90.3. The WHO/ICD-10-GM
codes are accepted as synonyms of the subtype each case has: G23.2 in P01 and RP03 (both
parkinsonian; also the ICD-10-CM code of striatonigral degeneration, the MSA-P pathology), G23.3
only in RP03 (mixed parkinsonian and cerebellar features). The entry is split: `G90.3` (multiple
system atrophy, MSA; global), `G90.3+p` (cases P01, RP03: MSA-P, multiple system atrophy
parkinsonian type, striatonigral degeneration; G23.2), `G90.3+c` (case RP03: MSA-C, multiple
system atrophy cerebellar type; G23.3). Nothing is retired (no label left the table).

**S3. Kept after the scan.**
- P02 "lewy body dementia": kept. It is an ICD-10-CM inclusion term of G31.83, PD dementia is coded
  G20 + F02.8x, and the PD-dementia answer ("Parkinson's disease dementia") does not contain its
  tokens.
- P03 PSP labels: "PSP" also credits a PSP-parkinsonism answer; same disease, kept.
- "PD": kept, as the abbreviation labels of other conditions (MS, ALS).
- Not fixable by labels (CENTRAL scorer item): a "Parkinson's disease dementia" answer scores in the
  PD-MCI cases (RP01, RP04) because every token of "parkinson's disease" is in it; an "MSA, not PD"
  answer scores in a PD case (negation).

`--check` clean over all 600 cases.

## CENTRAL items of the summary

**R1. Pack.** Done: `criteria_packs/PD.md` rewritten from plan facts F1 to F9 and section 3 with the
applied tiers and counts: MDS 2015 established versus probable and the four supportive criteria,
red flags and absolute exclusions, the D2-blocker rule, the work-up hierarchy (MRI 29 + CT 1
required; DaTscan required 4, recommended 1, optional 8, waste 17; labs 9 cases; drug check
required 5, recommended 7, optional 18; literature never), waste list, the single soft sequence
constraint, report rules (binary DaTscan and MIBG, PSG and battery impressions, MoCA item maxima,
CSF glucose, orthostatic figures), the mimic cases with MDS 2022, McKeith 2017 and MDS 2017
criteria and their codes. Allow-list: the 12 keys the cases cite plus `[EASL_ERN_Wilson_2025]`,
each with a full reference; a script finds none missing. Superseded: `[EASL_Wilson_2012]` (by
EASL-ERN 2025), `[Gilman_2008]` (by Wenning 2022), `[McKeith_2017_DLB]` (alias of `[DLB_2017]`, no
PD case uses it). `[Postuma_2019]` removed (no case cites it; its locator could not be verified).

**R1a. Wilson guideline (found while checking the keys).** EASL 2012 is superseded by EASL-ERN 2025.
PD-P04 recited to `[EASL_ERN_Wilson_2025]` (labs criterion, must, key evidence), and the rationale
no longer carries the 2012 "consider it from age 3 to 55" window (not verified in the 2025 text);
it names the first-line tests instead. No other case in the dataset cites the 2012 key.

**R1b. Metadata citation gaps.** `metadata.citation_gap` cleared in P01, P02, P03, P04, RM01, RM02,
RM03 and RP03: each asked for a key now in the pack.

**R2. Generator (`conditions.yaml`, parkinsons block).** Done for the block: the header comment
states the round's tiers and the probable-PD rule; the straightforward MRI line no longer says a
normal MRI "supports PD" (and loses its em dash); the moderate ventricle line now states the Evans
rule (above 0.30 abnormal); the puzzle MRI lines say atypical MRI markers belong only in an MSA or
PSP case (they produced the MSA-type MRIs in PD-labelled RP01 and RP02, C21); the puzzle
presentation no longer seeds "symmetric parkinsonism ... poor response to levodopa trial" (C7,
C21) and says the data must meet the label; DIP and MSA differential text corrected (normal
DaTscan; poor response only after a documented trial), DLB and vascular parkinsonism added;
follow-ups rewritten to plan section 3 (DaTscan stored abnormal everywhere with its tier rule,
MIBG, PSG, battery, genetics trigger renamed `request_counselled_pd_gene_panel` as in P04,
orthostatic BP). The generator code items are CENTRAL below.

**R3. Guard.** PD added to `DISCRIMINATOR_CONDITIONS` in `test_case_guards.py`;
`test_case_guards.py -k PD-` 90 passed (`test_routed_outputs_name_their_study` included).

**R6. ICD.** See S2.

**R9. Guidance answers.** `build_condition_tool_guidance.py` parkinsons responses rewritten and the
YAML regenerated with `--write` (only the four PD answers changed): labs (9 cases: required P04,
recommended RM02, RM05, RS01, optional 5), EEG (no criterion, waste in 28), ECG (now status
`confirm`: the RP01 ECG and Holter departure is shown to Reviewer 1 with the ESC 2018 reason and an
offer to remove it), specialised tests (EMG/RNS/biopsy/EP absent; autonomic and tilt never
criteria, waste in all 30, reports stored in P01 and RP03 only so an order is answered
consistently; neuropsychology 11 = 10 optional + RP04 required; PSG optional 14, recommended M05;
genetics P04 and RM05). `test_guidance_claims.py` PD rows replaced by 9 rows checking every number;
all pass.

**R4, R5, R7, R10, and the code part of R2.** Not mine (vocabulary and code): CENTRAL below.

**R8. Condition scoping.** Decided by the orchestrator (O1).

**R11. RP02 MIBG.** Kept (O3); for the physicians.

## Open questions and auditor flags

1. **Re-prefixing the PD-mimic cases (summary, for Andrea 1).** Closed by O1: keep ids and condition.
2. **Primary ICD code for MSA (summary, for Andrea 2).** G90.3, with G23.2/G23.3 accepted (S2).
3. **Q1 to Q6 (plan defaults).** Confirmed: mimic cases kept with their own criteria; RP01 and RP02
   data fixed to probable PD; RS03 and RS04 rewritten to typical PD; DaTscan waste where the
   diagnosis is clinical (NICE NG71 gives no indication; every case still stores an abnormal scan,
   so an agent that orders it is told the truth); RP01 keeps its ECG (shown to Reviewer 1, R9);
   literature deleted in all 30 (the outputs carried invented citations).
4. **P01 medication review recommended, RM02 labs recommended, RP02 optional PSG, RP03 six musts and
   mixed MSA-P/C label, RS03 and RS04 seed provenance.** Confirmed as the auditor decided; no change.
5. **RP04 genetics not added; B12 248 pg/mL.** Confirmed: genetics is limited to onset before 50 or
   a first-degree relative; the low-normal B12 is in an optional lab criterion, and a must may cite
   only required or recommended results (C8 rule 6), so no must. Listed for the physicians.
6. **Cosmetic items left by the auditor** (identical library-style normal fallbacks, pre-round em
   dashes in patient text, differential entries without ICD codes, `[Postuma_2015]` on some avoided
   actions, "24 /30" spacing, follow-ups of waste studies listed first in P03, S03, RP04): kept.
   None changes what an agent sees or how it is scored, and churn sends cases back to re-review.
   G21.19 for metoclopramide (not a neuroleptic) and G21.11 for prochlorperazine and antipsychotics
   are the correct ICD-10-CM choices; G24.9 and G24.1 are right. Differential codes are not scored.

## For the physicians at re-review

- PD has never been physician-reviewed in a notes round; all 30 cases changed in this round.
- RP02: delayed MIBG H/M 1.21 read as cardiac sympathetic denervation in a man on sertraline with
  paroxysmal AF and EF 65%; please confirm it is interpretable (R11).
- RP01: ECG and Holter recommended against Reviewer 1's removal (syncope with known WPW; ESC 2018).
- RP04: B12 248 pg/mL on long-term levodopa, left without a must (optional lab).
- Scoring changes: G20.C and the complication codes the case does not have no longer score; MSA
  cases accept G23.2 (and RP03 G23.3); PD-P04 cites EASL-ERN 2025.

## Still for Andrea

Nothing blocks.

## CENTRAL (not done here: vocabulary and code owners)

1. **Vocabulary.**
   - `perform_clinical_assessment` assessment_type `levodopa_challenge`: MDS-UPDRS III OFF and ON
     after a supra-threshold levodopa dose, percent improvement (at least 30% for DBS candidacy).
     Needed by PD-RP04 (its must asks for it), and by any DBS or MSA "poor response" case.
   - `order_specialized_test` test_type `olfactory_test` (UPSIT or Sniffin' Sticks, result against
     age and sex norms): a validated smell test is a supportive MDS criterion; today M04 and RP01
     state it in the exam and S04, S06, RS05 and M05 have only self-reported loss.
   - `laryngoscopy` (ENT, for stridor in MSA, PD-RP03): only if another condition needs it; RP03
     keeps it as a must.
2. **Library (R5).** Condition-aware defaults for DaTscan (the normal default is an MDS absolute
   exclusion in any parkinsonism case), MIBG, PSG, neuropsychological battery, orthostatic,
   autonomic and tilt reports, or a guard that fails a case when a library default would contradict
   it (exam MoCA below 28 without a stored battery; dream enactment without a stored PSG; a
   parkinsonism label without a stored DaTscan; measured orthostatic hypotension with a normal
   orthostatic default). The 30 PD cases store all of these where needed.
3. **Generator code (R2).** Stop emitting literature criteria and required drug checks for PD; the
   "Abnormal values" impression builder (inverted flags for lower-is-worse measures); the "July 2026"
   evidence lines; the amyloid PET fallback template; MRI `{"contrast": false, "protocol":
   "standard"}` arguments; tier words in trigger names and rationales; compute a CSF fallback glucose
   from the case's serum glucose; itemise MoCA losses within item maxima.
4. **perfect_agent.py and scorer (R7).** Call each tool with the minimal arguments a real agent uses
   (the baseline false pass came from exact `query` and `drug` strings); a guard forbidding free-text
   `required_arguments` on knowledge tools. Scorer: per-case rejected tokens (the open ALZ-EARLY
   item) would let PD-RP01 and PD-RP04 reject a "Parkinson's disease dementia" answer; negation
   matching (the open SAH item) would stop "MSA, not PD" scoring in a PD case.
5. **R10.** `perform_clinical_assessment` `orthostatic_blood_pressure` is used in M01, RM04 and RP04;
   the stored reports route (probe and perfect-agent check).
6. **CENTRAL_PENDING.md (orchestrator).** Remove "PD 30/30" from the discriminator line, the
   "`[McKeith_2017_DLB]` should become `[DLB_2017]`" item (no PD case uses the old key), and PD from
   the `test_guidance_claims` failure note (PD claims pass).

## Files changed

- Cases: all 30 PD cases (synonym prune: codes in 28, labels in P01 and RP03); P04 (Wilson key and
  rationale); metadata in P01, P02, P03, P04, RM01, RM02, RM03, RP03. Logs: all 30.
- `agent-platform/config/policies/diagnosis_synonyms.yaml` (G20, G20.A2, G20.B2, G90.3, G90.3+p,
  G90.3+c).
- `dataset-generation/criteria_packs/PD.md`; `dataset-generation/config/conditions.yaml`
  (parkinsons block).
- `agent-platform/scripts/review/build_condition_tool_guidance.py` (PD responses),
  `agent-platform/config/review/condition_tool_guidance.yaml` (regenerated),
  `agent-platform/tests/test_guidance_claims.py` (PD rows), `agent-platform/tests/test_case_guards.py`
  (PD in `DISCRIMINATOR_CONDITIONS`).

Checks: `perfect_agent.py` 30/30 pass with no "same stored report" warning; `case_io.py check` on
the 30: schema and synonym guard OK, full suite 3483 passed, no failure; `test_case_guards.py -k
PD-` 90 passed; `apply_diagnosis_synonyms.py --check` clean over all 600; guidance claims pass.
