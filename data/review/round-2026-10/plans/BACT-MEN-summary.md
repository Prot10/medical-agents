# BACT-MEN: condition summary of the October 2026 review round

Condition auditor, 23 October 2026. Scope: the 30 cases BACT-MEN-M01..M05, P01..P05, RM01..RM04,
RP01..RP05, RS01..RS05, S01..S06, against `ROUND_POLICY.md`, `PATTERNS.md`, the condition plan
`plans/BACT-MEN.md`, the notes file `notes/BACT-MEN.json` (97 Reviewer 2 notes; Reviewer 1 has none)
and the 30 case logs.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass; every index CSF criterion (`action-3-analyze-csf`) is
  served the index lumbar puncture (`request_lumbar_puncture`, or `request_evd_csf_sample` in M05),
  never a post-treatment report.
- `case_io.py check` on all 30 ids: schema OK for all 30, synonym guard OK, no test failure names a
  BACT-MEN case.
- Every one of the 97 note ids appears in exactly one case log (the log of its own case), with a
  ruling. No log cites a note id of another case.
- Scripted checks over the 30 files (results after the audit fixes): only `labs` is given as an
  initial output in every case; no `search_medical_literature` criterion or output; no
  `request_repeat_lp` (P03 keeps a therapeutic drainage follow-up without the LP token),
  `request_pcr_panel`, `request_audiometry`, repeat-lab, ophthalmology or susceptibility follow-up;
  no `[IDSA_2004]`, ESCMID, "age >60"/"age >50" imaging or Listeria threshold, "normal >0.6",
  "likely traumatic" for 0 to 5 RBC, lactate "<2.1", LP-safety sentence in an imaging report,
  narrowing/interpretability boilerplate, undeclared "worst headache", "sinus thickening on MRI"
  without an MRI, or the "Do NOT discontinue dexamethasone solely because the Gram stain is
  negative" prohibition; the stop rule equals the required criteria in all 30; drug-check tiers
  match plan 4.0 in all 30; Listeria cover is a must exactly where plan 4.0 says (or is covered by
  meropenem or co-trimoxazole); the canonical dexamethasone must is present in every pyogenic case
  except the deliberate exceptions below; every index CSF uses the canonical ratio, RBC and lactate
  strings; every red-herring `field_path` resolves; every lab panel reports HIV and liver tests;
  citation keys in criteria, avoided actions and constraints are limited to `[WHO_Meningitis_2025]`,
  `[NICE_NG240]`, `[IDSA_2017_HCVM]`, `[WHO_Cryptococcal_2022]`, `[WHO_TB_Module4]`, `[Brouwer_2012]`.

## Error classes found in this condition and how each was fixed

The class codes are those of the plan (section 2). All 30 cases shared most of them, because the
August rewrite produced them from one template.

| class | what was wrong | how it was fixed (all 30 unless stated) |
| --- | --- | --- |
| C1 Index CSF upfront, repeat LP first | Index CSF in `initial_tool_outputs.csf` (29 cases); a post-treatment repeat LP was the first pathway step in 19 and was served to any "LP" call, so action-3 was answered by the wrong report and the HARD constraint was broken; repeat labs reported treatment effects. | Index CSF moved to a follow-up `request_lumbar_puncture` placed after the CT where one precedes the LP; initial `csf` null; repeat LPs and repeat labs deleted (P03 keeps a therapeutic drainage follow-up `request_therapeutic_csf_drainage`); culture final reports kept as separate later follow-ups in M04, P04, RM04, RP05; index culture "Pending" (P01, M05 report the index-specimen culture with its interval, as their notes asked). |
| C2 Imaging before LP on IDSA 2004 | 27 cases required CT with a HARD constraint on "altered mental status" and "age >60/>50". | Decided per case on WHO 2025 Annex A.4 (NICE NG240 1.4.7 where in scope). A (CT required, HARD CT before CSF, SOFT cultures before CT, canonical label, must, prohibition): M01, M02, M03, M04, P02, P03, P05, RM01, RM02, RM03, RM04, RP02, RP03, RP05, RS02, RS04, S02. B (CT kept for a source, no HARD constraint, SOFT cultures before CT): P04, RP04, S01, S03, S04. C (no CT; waste avoided action; canonical no-imaging must and prohibition): P01, RP01, RS01, RS03, RS05, S05, S06. M05: SOFT constraints only (IDSA 2017). Record fixes that the decision rests on: GCS components (M02, RM02, RP02, RP04, RS02, RS04, RS05, S04, S06 and others), progressive fall in consciousness (M01), papilloedema removed (S02, S04), fundoscopy documented (RS01). |
| C3 CT reports | "No contraindication to lumbar puncture" in 28 impressions; contrast findings on non-contrast CTs (P02, P03, RP03, RS02, RS04, S04); CT against MRI. | Findings-only impressions; enhancement removed from non-contrast studies; CT and MRI aligned (RM01, S04, RS02, RP03). |
| C4 Empirical regimen | Template "vancomycin 15-20 mg/kg + ceftriaxone" in about 20 cases; Listeria cover missing; ceftriaxone mandated despite allergy. | Canonical ceftriaxone/cefotaxime within 60 minutes with vancomycin conditional; ampicillin for Listeria risk factors (17 cases); meropenem plus vancomycin for cephalosporin hypersensitivity (S01, RP02) and HCA Gram-negative disease (RS04); vancomycin plus cefepime or meropenem in M05; ceftriaxone plus co-trimoxazole in S04 (non-severe penicillin rash); targeted narrowing musts; drug-check outputs rewritten to the same regimen. |
| C5 Dexamethasone | Pneumococcal stop rule applied to every organism; template Gram-stain prohibition. | Canonical must with the WHO stop rule plus the case line ("Continue for 4 days" for pneumococcus and Hib; "Stop ... on identification of" Listeria, Klebsiella, GBS, meningococcus); Listeria prohibition in M04, RS05; not indicated in RS04 (HCA Gram-negative), not required in RP02 (days of parenteral therapy), reassessment with a hearing trade-off in RM04 (S. suis, reviewer's wording); none in M05; TB and cryptococcal regimens in P02, P03. |
| C6 Microbiology reports | Pre-antimicrobial flag true after antibiotics; narrowing and interpretability sentences; no intervals; organism fields against findings; MIC 0.12 "intermediate". | Flag false with a collection line in 14 cases; intervals stated; canonical impressions; organism fields fixed (M05, RS01, RS05, RM01); CLSI meningitis breakpoints (penicillin 0.12 resistant). |
| C7 CSF reports | Ratio reference ">0.6", "traumatic" RBC, lactate references, interpretive conclusions, antigen as confirmation, panel limits explained in results. | Canonical strings with the paired blood glucose of the lab panel (ratios recomputed); values-and-pattern interpretations; antigen removed except P01 (deliberate negative antigen); "No panel target detected (targets: ...)" for non-targets. |
| C8 Wrong tool | CSF PCR under `interpret_labs` (18), audiometry as `baep` (18), susceptibility, shunt tap, AFB and fungal cultures, ophthalmology under `interpret_labs`. | Deleted or folded into the right report; RS02 shunt tap became an `analyze_csf` follow-up; hearing became the canonical must. |
| C9 Literature and drug checks | Literature criterion in all 30 expecting IDSA 2004, ESCMID, De Gans; outputs echoing the scoring key; drug blocks empty or about allergies the patient lacks. | Literature criteria and outputs deleted (ruling 5); drug checks rebuilt on each case's real regimen, medicines, allergies and eGFR (CKD-EPI 2021), placed last in the pathway. |
| C10 Differential | Viral and HSV left moderate after a bacterial CSF; missing entities. | Assessment-time likelihoods with the excluding result in `key_features`; missing entities added (meningococcal disease M02, S04; NPH RM03; Listeria, GCA RS03; spinal infections RS01; otogenic complications RP05; neurosyphilis RP03; and others). |
| C11 Red herrings | Undeclared SAH-type headache wording in 9 cases; sinus thickening "on MRI" without an MRI; undeclared distractors. | Headache rephrased; field paths point at the real report; missing blocks added (RS03, RS04, M02, RM02, RP03 and others). |
| C12 Record contradictions and labs | GCS components, anion gaps, eGFR stages, timelines, laterality (RS02 encephalomalacia, RP03 node, RP05 gaze), white-cell differentials not summing to 100%, male ranges in women, missing HIV and liver tests, HPI sentences naming the differential. | One version of each fact; HIV and liver tests added in all 30; differentials sum to 100%. |
| C13 Imaging in the initial work-up | MRI, CT, EEG, microbiology given upfront with diagnostic conclusions. | Moved to follow-ups, findings-only impressions. |
| C14 Missing actions | DIC and shock, catheter, ENT and skull-base imaging, spine MRI, cryptococcal antigenaemia, MenB. | Criteria where a tool exists (spine MRI RS01; contrast MRI and MR venography RP05, S03; urine culture RS04; immunoglobulins RP01, RP04; syphilis RP03), musts otherwise (DIC S04, S05; sepsis RM01, S02; catheter RS04; ENT S01, S02, S03, P04, RP04, RP05). |
| C15 Pyogenic boilerplate in TB and cryptococcal cases | Contradictory LP bullets, pyogenic prohibitions. | One LP position; TB (WHO Module 4) and cryptococcal (WHO 2022) musts. |
| C16 HCA cases written as community-acquired | M05, RS04, RS02 shunt, RP02 post-procedural. | IDSA 2017 governs the regimen; EVD label (M05); WHO line removed in M05. |
| C17 Key evidence template lines | IDSA, vancomycin, Gram stain 60-90%, ratio, De Gans, pauci-cellular lines. | Canonical replacements; the remaining "WHO 2025: obtain cultures promptly ... when the pathway requires treatment first" lines removed at the audit (below). |

## Audit findings fixed (stragglers)

1. **`before_antimicrobials` in the blood culture criterion was inconsistent across the condition**
   (flagged by the RM01, RM03, RP01, RP02, RP03 workers and verifiers). Five cases had dropped the
   argument, nine still required `true` although their own report says `collected_before_antimicrobials:
   false`. The matcher requires a required key to be present with the same value, so a truthful
   `false` order missed a required criterion. Rule now applied to all 30: the argument is required
   only where the report flag is true (16 cases), absent where it is false (14 cases). Changed: M01,
   M02, M03, M05, P02, P04, RP05, RS04, S03.
2. **Template key evidence line** "WHO 2025: obtain cultures promptly, but neither LP nor cranial
   imaging may delay empirical antimicrobials when the pathway requires treatment first." survived in
   RM03 and RP01 (deleted, duplicate of the timing line) and RM04 (replaced by the C17 timing line,
   which that case lacked).
3. **Stale metadata note** in P01 (`case_body_concerns` claiming no stored drug-check output): removed,
   as the P02 and P03 verifiers did for theirs.

Each change is appended to the case log under "Condition audit"; both checks re-run clean.

Checked and left as is (judged consistent or deliberate): P04 imaging B instead of the plan's C
(purulent sinusitis documented before the meningitis, as in S01); S02 imaging A instead of B (a
right-sided motor asymmetry recorded in the original exam is a focal sign); M05 has no hearing must
(post-neurosurgical MSSA ventriculitis, outside NICE NG240); the generic prohibitions "Do NOT delay
empiric antimicrobial therapy ...", "Do NOT rely on a negative Gram stain or a 'normal CT' ..." and
"Do NOT treat with oral antibiotics alone ..." remain in 17 to 21 cases: they are correct, so removing
them would be churn; generic social-history phrases shared by a few cases ("Never smoker", "Denies
illicit drug use") are not case-specific carry-over.

## Counts

- Reviewer notes: 97.
  - FIXED: 96.
  - FIXED in part, BLOCKED in part: 1 (RP04 8f75c86a: parts 2 to 4 fixed; part 1 BLOCKED).
  - ALREADY-FIXED: 0. DECLINED: 0.
- Worker own findings (log tables): 467 rows; 464 FIXED, 3 FLAGGED. Of the 3 flagged, 2 were then
  fixed by the verifiers (RP05 gaze direction; RS01 echocardiography removed from waste); 1 stays
  flagged with no change needed (RS02 "community acquired" synonym is correct for that patient).
- Verifier findings: further fixes in 27 of 30 cases (the M04, RP04 and RS03 verifiers found nothing to change).
- Audit findings fixed: 3 classes in 13 cases (listed above). Flagged for Andrea: see open questions.
- Cases changed: 30 of 30.
- Approved cases changed: 0 (no BACT-MEN case was approved before this round; all 30 were
  `needs_changes` from Reviewer 2).

## DECLINED and BLOCKED notes

- DECLINED: none.
- BLOCKED (part): **RP04, 8f75c86a-41e8-45e9-a036-98ce1b1e9cf3, part 1** (beta-2 transferrin as its own
  pathway step with a turnaround). There is no vocabulary term for a beta-2 transferrin assay on nasal
  secretion (`interpret_labs` has only `beta2_microglobulin`), and filing it under another assay is
  forbidden. The result was removed from the CSF report (so it is no longer handed over or misfiled),
  the differential no longer claims a positive result, and a must asks for the send-out assay with a
  realistic turnaround. Unblocks with CENTRAL item 4 below.

Notes applied with a chosen option or a reasoned departure (FIXED, logged): RM04 7fdda22c (CT required on
the bilateral CN VIII deficit, plan Q4; dexamethasone reassessment wording for S. suis); RS03 779f9ec1
(vancomycin conditional per WHO rather than the reviewer's wording); RP02 10d64799 (dexamethasone not
required after days of parenteral therapy); M05 00ce9e6f (SOFT "EVD CSF before CT" instead of the plan's
"CT before CSF"); RS01 00b8d7a0 (portal of entry also written into `accepted[0]`); S01 7e72aa2c (label
"(sinugenic source)"); M02 258fbb73 and S04 db9626f9 (meningococcal disease kept moderate and high as
ruled).

## Consolidated CENTRAL requests

1. **Citation keys** for the criteria pack allow-list: `[WHO_Meningitis_2025]`, `[NICE_NG240]`,
   `[IDSA_2017_HCVM]` (Tunkel AR et al., Clin Infect Dis 2017;64:e34-e65), `[CLSI_M100]`,
   `[WHO_Cryptococcal_2022]`, `[WHO_TB_Module4]` (edition to confirm); `[Brouwer_2012]` is now also used
   for complication imaging (RS01, RP05, S03, S04). Keys wanted for sources currently cited in prose
   only: Mai NTH et al., N Engl J Med 2007;357:2431-40 (RM04), Surviving Sepsis Campaign 2021 (S02), a
   syphilis-in-HIV screening guideline (RP03 `action-8-interpret-labs-syphilis` has no citation), a
   recurrent-meningitis work-up source (RP04 `action-8` has no citation).
2. **Criteria pack `BACT-MEN.md`**: replace the IDSA 2004 imaging list and "ampicillin if >50" with WHO
   2025 Annex A.4 / NICE 1.4.7, the over-60 Listeria threshold, the dexamethasone stop rule, scope
   rules and the WHO CSF reference values (plan 1.2).
3. **`conditions.yaml`** bacterial_meningitis `common_followups`: remove `request_repeat_lp`,
   `request_pcr_panel`, `request_audiometry` (the generators of C1 and C8).
4. **Vocabulary** (`costs.yaml`, `tool_io.py` mirror, fallback library): `interpret_labs`
   `beta2_transferrin` (unblocks RP04), `serum_cryptococcal_antigen` (RS04, P03), `CD4_count`,
   `HIV_viral_load`; `analyze_csf` `mycobacterial_panel` (AFB smear, Xpert MTB/RIF Ultra, culture),
   `fungal_culture`, `india_ink`, `ADA`, and a CSF source term that distinguishes a shunt tap or EVD
   sample from a lumbar puncture (RS02 shunt tap cannot be scored); `order_microbiology` `wound_swab`
   (RS01 ulcer) and `sputum` in the core pack (P02); `order_specialized_test` `audiometry`;
   `order_body_imaging` temporal artery ultrasound and `obtain_tissue_diagnosis` temporal artery biopsy
   (RS03, if GCA questions should be scoreable).
5. **Diagnosis synonyms**: `G00.8` appends "listeria meningitis", "listeria monocytogenes meningitis",
   "listeria meningoencephalitis" to RM04 (S. suis), RP05 (Klebsiella) and RS04 (Proteus), so a wrong
   organism scores as correct. Move the Listeria labels to an `A32.1` entry, recode M04 and RS05 to
   A32.1 (Listeria meningitis), consider G00.2 for RM04, give G00.8 neutral labels, and strip the
   appended Listeria labels from those three cases (the script only adds). `G00` appends "community
   acquired bacterial meningitis" to the healthcare-associated M05, RS04 and RP02.
6. **Matcher and schema defaults**: `_contains_required` requires every required key to be present in
   the call; tool-schema defaults are not applied before matching. `before_antimicrobials` defaults to
   `true`, so in the 16 BACT-MEN cases that still require it (and in HEP-ENC, SE and others) an agent
   that omits the argument misses a required criterion. Apply schema defaults before matching, or drop
   defaulted arguments from criteria benchmark-wide.
7. **Follow-up matcher test**: no repeat-study trigger may share a meaningful token with the index study
   of the same tool (the "LP" token made the repeat LP outrank the index LP in 19 BACT-MEN cases).
8. **Review UI**: show initial and follow-up outputs in criterion order (only `labs` stays initial here).
9. **Fallback library**: check the CSF, CT and literature fallbacks for "normal >0.6", "traumatic tap",
   "No contraindication to lumbar puncture" and IDSA 2004 criteria (S05 had it in its own fallback).
10. **Test**: no BACT-MEN case contains "age >60"/"age >50" as a criterion, "normal >0.6", "likely
    traumatic" for 5 RBC or fewer, the narrowing boilerplate, or `before_antimicrobials: true` in a case
    whose blood culture flag is false.
11. **Label change logged under ruling 3**: RS01 `accepted[0]` now names the venous stasis ulcer as the
    portal of entry; S01 `accepted[0]` now "(sinugenic source)". ICD codes unchanged, synonyms
    unaffected.

## Consolidated open questions for Andrea

Plan questions (Q1 to Q9), with what the cases now do:

1. **Q1** P02 (tuberculous meningitis, A17.0) and P03 (cryptococcal, B45.1) stay in
   `bacterial_meningitis` as mimics with their own pathways. Move them to another condition?
2. **Q2** CT as a `waste` avoided action in the no-criterion cases (P01, RP01, RS01, RS03, RS05, S05,
   S06); S06 has a recent otitis, so a post-LP mastoid CT is also counted as waste there.
3. **Q3** WHO 2025 governs where it diverges from NICE NG240 (asplenia and other immunocompromise as an
   imaging trigger: M01, M02, M03, RM01, RM02, RM03). Related: the canonical hearing must cites NICE
   NG240 for its 4-week timing in cases NICE does not cover (RM01, RM02, RM03 and others).
4. **Q4** RM04: CT required on the bilateral CN VIII deficit (applied), or the reviewer's alternative of
   no CT because cochlear injury is not a sign of mass effect?
5. **Q5** RS03: prednisolone 30 mg for about two weeks not counted as severe immunocompromise (no CT).
6. **Q6** S02 and S04 papilloedema removed (10 and 18 hours of illness). S02 stays A on a recorded
   right-sided motor asymmetry; S04 became B.
7. **Q7** Diabetes counted as a Listeria risk factor (Reviewer 2): Listeria cover is a must
   in 17 cases, and diabetes is the only risk factor in five of them: S02 (38), S04 (38), RM04 (56),
   RP05 (54) and RS01 (59).
8. **Q8** Recode M04 and RS05 to A32.1 and RM04 to G00.2 without a reviewer ruling (CENTRAL 5).
9. **Q9** Literature criterion removed in all 30.

Questions raised by workers and verifiers:

10. **Lumbar puncture in shock, spreading purpura or platelets below 100** (S04, S05; also relevant to
    hypotensive RM01 and S02): NICE meningitis guidance lists these among reasons to delay LP, yet the
    LP is a required criterion and the musts say to proceed. Should the LP be deferred until
    stabilisation, with the diagnosis carried by blood cultures and PCR, and how should scoring reflect
    it?
11. **"Overt DIC"** in S04 and S05 follows Reviewer 2 and the canonical must, but the stored values give an
    ISTH overt-DIC score of about 3 to 4 (cut-off 5). Keep, or write "sepsis-associated coagulopathy
    evolving to DIC"?
12. **Meningococcal disease likelihood** is `moderate` (M02) and `high` (S04) as Reviewer 2 ruled, while
    ruling 7 would set an excluded alternative to `low`. Which prevails?
13. **Dexamethasone departures**: RP02 (not required after days of parenteral therapy), RM04 (S. suis:
    continuing for hearing protection as a deliberate trade-off, Mai 2007), RP03 (given in HIV per WHO,
    although African HIV-prevalent trials showed no benefit). Confirm.
14. **M05**: SOFT "EVD CSF sample before CT" replaces the plan's "CT before CSF"; TMP-SMX susceptibility
    set to susceptible; the culture result sits in the index EVD CSF report rather than a separate
    final report.
15. **Additions beyond the notes** that a re-reviewer may want trimmed: sepsis musts (RM01, S02),
    immunosuppression plan (RM02), RS04 urine culture criterion and hyponatraemia, ART and fluconazole
    musts, RP02 and RP04 vaccination musts, RP03 syphilis criterion and levetiracetam must, P02 removal
    of the QuantiFERON result from the first panel.
16. **Plausibility margins**: RP03 CSF with 3 cells and protein 204.7 under co-trimoxazole partial
    treatment (raise to 20 to 40 cells?); RP03 unexplained left-sided chest pain in the chief complaint;
    RP01 post-vaccine pneumococcal titres returned with the immunoglobulins (turnaround); P04 CSF glucose
    lowered 38 to 34 mg/dL so the ratio is 0.37; P01 paired glucose 102 flagged high.
17. **Scored versus must-only imaging**: P05 (persistent right-sided deficit) and S02 (asymmetry) have a
    conditional contrast-MRI must but no MRI report; P02 chest imaging is a must only; P03 MRI is
    required although WHO 2022 does not need it once CSF CrAg is positive. Author reports and criteria,
    or keep them as musts?
18. **Echocardiography** stays `waste` in most cases (removed in RS01 for subacute GBS bacteraemia);
    confirm for the bacteraemic pneumococcal cases.
19. **S01**: the HPI describes a progressive fall in consciousness overnight (a NICE 1.4.7 trigger), but
    Reviewer 2 ruled no imaging criterion and WHO governs; S03 paraphasias likewise not counted as a
    focal sign. Confirm.
20. **RS04 meropenem dose**: 2 g every 8 hours "adjusted to creatinine clearance"; with BMI 17.2 the true
    clearance may be below 50 mL/min, and no weight is recorded.
