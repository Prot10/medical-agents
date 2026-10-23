# HEP-ENC: October 2026 review round, condition summary

Condition audit, 24 Oct 2026 (condition auditor, retry pass). Scope: the 30 HEP-ENC cases (M01-M10,
P01-P09, S01-S11), the plan `plans/HEP-ENC.md`, `PATTERNS.md`, `ROUND_POLICY.md`, the 30 logs and
`notes/HEP-ENC.json` (88 notes, all from Reviewer 2). Approved cases: P09, S01, S09.

## Checks (re-run after the auditor fixes)

- `perfect_agent.py` on all 30 ids: 30/30 pass.
- `case_io.py check` on all 30 ids: schema OK for all 30, synonym guard OK. The suite has 2 failing
  tests; case_io reports that no failure names a HEP-ENC case (other conditions are mid-edit).
- Scripted uniformity checks across the 30 cases. Everything below holds, or differs only by a
  deviation documented in the case log and accepted by its verifier:
  - criterion order and tiers per plan 3.1 (labs, blood cultures, paracentesis, urine, CT, MRI,
    EEG, case-specific steps, drug check); culture, paracentesis, CT, MRI, EEG and drug-check tiers
    as in plan sections 2-4;
  - stop rule equals the set of required ids in every case; no sequence constraints anywhere; no
    panel exemptions;
  - no literature criterion, no literature follow-up, `initial_tool_outputs.literature_search` and
    `drug_interactions` null; follow-up order paracentesis, urine, other diagnostics, drug check
    last (S01 keeps telemetry after the drug check, logged);
  - every core lab criterion has the two plan alternatives (`CMP` or `BMP` + `LFTs`) plus the case
    extras, and every lab term in every criterion is in the advertised `interpret_labs` enum
    (checked against `vocabulary.lab_panels()` after the auditor fix below);
  - MELD and MELD-Na recomputed from the printed creatinine, bilirubin, INR and sodium in all 30:
    every `accepted[0]` MELD-Na equals the computed value (M04 carries no score in the label, by
    plan); every other score in a case is dated as prior;
  - K-AMM pearl and a 2-3 soft-stool lactulose must present in all 30 (MUST-LACT verbatim, or the
    logged no-loading adaptation in M06, M08, P07, S02);
  - banned strings absent: "2-4"/"3-4" stools, "Exclusion studies", "umol", "No organism isolated
    to date", `before_antimicrobials` in criterion arguments, grade ranges in labels, "arginase",
    "the finding the lumbar puncture is gated on", "restricted diffusion" on CT, EEG drug
    challenges and treatment-response follow-ups;
  - fallback and initial ECG rates agree with the recorded heart rate (within 2 bpm) wherever a
    rate is stated.
- Note coverage: all 88 note ids appear in a log table row with a ruling. 85 ids appear in exactly
  one log. The three notes filed on S06 (170d2c1e, 988c74d2, 36bd67da) describe S05 and, by plan
  section 4 and CENTRAL 7, appear in both the S05 log (FIXED there) and the S06 log (ruled for S06);
  this is the only departure from "one log per note" and is by design.

## Error classes and how each was fixed (plan C1-C17, plus the auditor classes)

- **C1 Treatment, consults and response delivered through diagnostic tools (ruling 4).** Every
  `request_lactulose_rifaximin`, `request_thiamine_empiric`, `request_liver_transplant_evaluation`,
  EEG drug challenge (lorazepam, naloxone), post-treatment EEG, treatment filed as a drug check or
  specialised test (endoscopy, withdrawal monitoring, CPAP, Wilson and coeliac treatment, rifaximin
  insurance) and consult output was deleted in all 30. Their clinical content became musts.
- **C2 Ammonia.** One admission ammonia per case, range 11-51 µmol/L, flag recomputed; every serial
  value and every "falling ammonia confirms response" removed from HPI, pearls, red herrings and
  expected evidence; K-AMM pearl added in all 30.
- **C3 Lactulose target.** MUST-LACT (2-3 soft stools, over-titration warning) in all 30;
  MUST-LACT-OVERUSE in M06 and S02; no-loading wording where the patient already has diarrhoea or
  covert HE (M06, M08, P07, S02); rifaximin kept only for recurrent episodes (removed in first
  overt episodes such as M07 and M10; conditional in M05).
- **C4 Literature (ruling 5).** Criterion, initial output and every literature follow-up deleted in
  all 30, including the approved cases (Q7).
- **C5 Drug checks (ruling 6).** Empty template blocks and expected-evidence echoes removed; one
  follow-up per case whose trigger names the drugs, placed last, listing only what changes
  management; tier required only for a concrete interaction (some cases logged one tier higher
  than the plan: M01, M03, S06 recommended); penicillin-rash wording for ceftriaxone.
- **C6 Paracentesis.** The duplicate `interpret_labs` tap criteria and outputs deleted; one required
  `order_microbiology` `ascitic_fluid` criterion in every case with ascites (21), none without.
- **C7 Cultures.** Tier by fever, WBC or infective precipitant; arguments reduced to the specimen;
  one specimen and one time point per block; contradictory "no growth"/positive blocks resolved
  (S03, S05, S09, M09); shared "No organism isolated to date" text replaced by each case's result;
  urine moved to its own follow-up.
- **C8 Imaging and EEG.** One MRI report per MRI case in `initial_tool_outputs.mri` (Wilson,
  Wernicke, contrast P03, P08 shunt work-up); "restricted diffusion" removed from every CT and
  pallidal hypodensity from S04-S07; M01 CSF criterion and CT-before-CSF constraint deleted; P07
  EEG rewritten with one normal range. Verifiers also corrected normal fallback EEGs in HE cases
  (M09, M10, P09, S11) and fallback MRIs reading "appropriate for age" against CT atrophy (M09,
  P01).
- **C9 Lab reports.** Template TSH, zinc, toxicology and "Exclusion studies" blocks replaced by one
  numeric entry per analyte with case-fitting values; each case's own values kept (M03 TSH, M05
  zinc, P02 and S08 ethanol, P05 B12); CRP added in all 30, creatinine in M04 and P05; the core
  criterion reduced to the two plan alternatives plus extras (CENTRAL 4 still pending).
- **C10 Scores.** MELD-Na and Child-Pugh recomputed from the printed labs in all 30 and written
  into `accepted[0]`, key evidence, reports and musts (ruling 3, CENTRAL 6); prior scores dated.
- **C11 Grade and type.** P01 overt grade II; P03 no longer "covert"; P08 type C throughout;
  grade ranges collapsed to one grade per plan 1.2, with the exam adjusted where needed (orientation
  to place made consistent with grade II in M01, P01, P02; GCS motor M5 corrected to M6 where the
  patient obeys commands; S10 GCS 11 to 13).
- **C12 Boilerplate prohibitions.** PROHIB-BZD, PROHIB-BZD-WD (M02, M04, S04, S06, S08) and
  PROHIB-BZD-SZ (P06) replace the benzodiazepine/haloperidol line; generic LP prohibition deleted;
  acetaminophen "up to 2 g per day"; M08 antidiarrhoeal contradiction resolved; S01 airway must.
- **C13 Timeline leaks.** Results of scored studies removed from HPI and exam; dated
  pre-encounter data kept. Verifiers also removed "prior HE grade 1" wording that contradicted
  secondary prophylaxis (S03, S04, S05, S07).
- **C14 Differentials and red herrings.** Excluded alternatives set to `low` with the excluding
  result; P09 SDH a concurrent contributor; S02 and M08 red herrings rewritten.
- **C15 Abnormal findings without work-up.** P06 EEG required; S05 renal ultrasound required; M06
  TIPS Doppler required; P08 shunt imaging recommended; M08 and S02 source search as musts until
  CENTRAL 5.
- **C16 Treatment musts (ruling 4).** Musts made specific and checkable (MUST-PRECIP, MUST-SBP,
  MUST-VB, MUST-SEPSIS, MUST-K, MUST-THIA, MUST-TX, MUST-THERAG, M04 Lille).
- **C17 Criterion mechanics.** Every rationale rewritten as one case-specific sentence with its
  citation key; canonical core-lab, CT and EEG rationales.
- **Fallback ECG rate (verifier class).** Fallback ECG rates aligned with the vitals in S01-S06 and
  S10 (S09, approved, left; see flags).
- **Auditor class A1: unadvertised lab alias in a required criterion.** M02, S01, S06 and S08
  required `toxicology` in both core-lab alternatives. The tool advertises only `tox_screen`;
  `toxicology` is an accepted alias that `BaseTool` does not rewrite, and `_contains_required`
  folds only case and underscores, so an agent ordering the advertised `tox_screen` failed a
  required criterion (checked by direct call). Fixed in all four by `tox_screen` (the corpus
  spelling, 18 alternatives against 8). In S01 (approved) the term was itself added this round, so
  the fix corrects the round's change, not the approved policy.
- **Auditor class A2: template pearl surviving in S02-S05.** `key_clinical_evidence[0]` still held
  the July template "West Haven grading + evidence of liver dysfunction + exclusion of other causes
  of AMS ... (AASLD 2014)" with an em dash. Replaced in all four by the M01 canonical text "HE is a
  clinical diagnosis: West Haven grade, evidence of liver disease and exclusion of other causes of
  altered mental status (ACG 2026; EASL 2022)." The ammonia half is already carried by K-AMM.

Each auditor change is logged under "Auditor (24 Oct 2026)" in the case's log.

## Counts

- Notes (88, all R2):
  - FIXED: 85. Two of them carry a declined part: e9c07b1d (P01; treatment as a tool DECLINED by
    design) and d4cc8148 (P06; CK part partly DECLINED). The three S06-filed notes are FIXED in
    S05.
  - Split rulings: 2. 3559f393 (S02) DECLINED in part / FIXED in part; 1720c3d7 (S03) DECLINED in
    part / FIXED in part / ALREADY-FIXED in part.
  - DECLINED in full: 1 (43f8f665, P09).
  - ALREADY-FIXED in full: 0 (one partial, in 1720c3d7).
  - BLOCKED: 0.
- Own findings: 486 logged by the case leads (235 major, 251 minor), all FIXED. Auditor: 2 classes
  fixed (8 case edits: A1 in 4 cases, A2 in 4 cases); 9 flagged without change (below).
- Cases changed: 30 of 30.
- Approved cases changed: 3 of 3 (P09, S01, S09), each for real errors listed in their logs; the
  auditor touched S01 only to correct a term added this round.

## DECLINED and BLOCKED notes

- **43f8f665 (P09), DECLINED:** "no action delivers treatment" is by design (ruling 4, plan C16):
  treatment is scored through the musts, never a tool call. The musts were checked against plan 1.2
  and made specific.
- **3559f393 (S02), DECLINED in part:** same ruling 4 for the treatment-as-tool request. The
  treatment-response and rifaximin-insurance outputs it pointed at were deleted (FIXED part).
- **1720c3d7 (S03), DECLINED in part:** same ruling 4. MUST-SEPSIS, the antibiotic must and the
  haemodynamic/renal must were added (FIXED part); the referral criterion "with no tool" no longer
  existed (ALREADY-FIXED part).
- **e9c07b1d (P01), treatment part DECLINED:** ruling 4; the treatment-response follow-up was
  deleted and MUST-THERAG added.
- **d4cc8148 (P06), CK part partly DECLINED:** CK is now a measured normal value (186 U/L) because
  the admission sample was drawn about an hour after the convulsion and CK peaks 24-72 h later
  (Brigo 2015, stated in key evidence).
- **170d2c1e and 36bd67da, DECLINED for S06:** both describe S05 (positive E. coli urine culture,
  loin pain, creatinine 1.8), which S06 does not have. Applied and FIXED in S05.
- No note is BLOCKED.

## Auditor flags (not changed)

- **S01 (approved) has no transplant must.** Its `request_liver_transplant_evaluation` panel was
  deleted under C1 without the MUST-TX that C16 says replaces such panels, while the other actively
  drinking Child-Pugh C cases (S04, S06, S08) have MUST-TX with alcohol treatment. The plan's S01
  list (real errors only) does not include it, so it was not added to an approved policy. Suggested
  text if wanted: "Refer for liver transplant assessment once the bleed and SBP are controlled:
  decompensated alcohol-related cirrhosis with overt HE, MELD-Na 38 (EASL 2018); offer treatment for
  alcohol use disorder."
- **S01 uses PROHIB-BZD although ethanol is 168 mg/dL** (S04, S06, S08 use PROHIB-BZD-WD). Withdrawal
  is not yet present; approved case, left.
- **M04 has no MUST-TX** (severe alcohol-related hepatitis on prednisolone, no score in the label by
  plan); plausible while the Lille response is pending.
- **S05 criterion order** puts the required renal ultrasound before the optional CT; harmless
  (no sequence constraints), noted for uniformity.
- **S11 has an initial `eeg` output but no EEG criterion**; it is served only if ordered.
- **S09 (approved)** keeps "uV", pre-existing em dashes and a fallback ECG rate of 65 against HR 88.
- **M09 and M10 lack the "HE is a clinical diagnosis" pearl** that the other 28 carry.
- **Pre-existing em dashes** remain in unchanged text of many cases (no new text adds one).
- **`fallback_tool_outputs.mri`** in P03, P04 and P05 still holds a normal template; it is never
  served because `initial_tool_outputs.mri` exists.

## CENTRAL requests (consolidated)

1. **Citation allow-list** (plan CENTRAL 1): add `[ACG_HE_2026]`, `[EASL_HE_2022]`,
   `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`, `[Baveno_VII]`, `[EASL_ALD_2018]`, `[Lille_2007]`,
   `[EFNS_Wernicke_2010]`, `[AES_2016]`, `[Brigo_2015]`, `[AASLD_Wilson_2022]` (Schilsky 2023
   executive summary verified, P04), `[Kim_MELDNa_2008]`; retire `[EASL_2010]` and `[Bajaj_2011]`.
   Keys asked for by musts that cite in free text: `[EXTRIP_lithium_2015]` (P02), EASL 2017 PBC
   (M05), AASLD-IDSA HCV guidance (S07). The M06 ECG criterion has no allow-listed source.
2. **Lab criterion matching** (plan CENTRAL 4): make `_contains_required` use `normalize_analyte`,
   so `CMP` matches `BMP` + `LFTs`, `coagulation` matches `INR`, and an alias such as `toxicology`
   matches the advertised `tox_screen`. Until then a criterion must use the advertised spelling
   (auditor class A1; 8 `toxicology` alternatives remain elsewhere in the corpus, in other
   conditions). A test that every criterion analyte is an advertised term would catch this class.
3. **Core vocabulary** (plan CENTRAL 5; M04, M08, S02, S06): `chest_xray` in `order_body_imaging`
   and a `stool` specimen (C. difficile toxin/PCR) in `order_microbiology` in the core block, with
   library report and `tool_io.py` mirror; until then they are musts. Optional: AFP in
   `interpret_labs` (M08).
4. **`accepted[0]` changes under ruling 3** (plan CENTRAL 6): severity numbers changed in all 30;
   M05 and P01 relabelled; grade ranges collapsed (M04, M06, M08, M10, S01, S04, S07, S09, S11). No
   ICD or synonym change.
5. **Synonyms:** P07 (covert HE) receives the synonym "overt hepatic encephalopathy" from
   `diagnosis_synonyms.yaml` by ICD code, so an "overt HE" answer scores in a covert case; consider
   a per-case exclusion. P08 (grade II): check whether "hepatic coma" belongs in its set (K76.82
   beside K72.90/K72.91). P04: decide whether Wilson disease should be scored in the label.
6. **Criteria pack and `conditions.yaml`** (plan CENTRAL 2 and 3): update the HEP-ENC pack (2-3
   stools, covert definition, ammonia does not grade, ACG imaging triggers, no literature, drug check
   only for a concrete interaction, culture tiers, paracentesis with ascites, no CT/MRI-before-CSF
   constraint); remove the five seeded `common_followups` that caused C1.
7. **Review app** (plan CENTRAL 7): the three S06 notes describe S05; check the R2 note-to-case
   binding. Show initial and follow-up outputs together in criterion order.
8. **Tests** (plan CENTRAL 8): no stored literature or drug-check output contains a criterion's
   expected evidence; no HEP-ENC case contains "2-4 soft", "the finding the lumbar puncture is
   gated on" or a CT "restricted diffusion".
9. **`condition_tool_guidance.yaml`** (plan CENTRAL 9): it requires cultures in all 30 (C7 tiers
   them) and counts 13 cases with ascites (there are 21).

## Open questions for Andrea (consolidated)

Plan questions:
- **Q1 M05 premise:** applied as planned (constipation precipitant; zinc excess with copper
  deficiency incidental). Confirm.
- **Q2 culture tier threshold** (T 38.0, WBC above 11, infective precipitant). Edge cases: P06
  (post-ictal WBC 11.2), S04/S08, M03 (UTI on treatment, kept recommended), P07 (made optional).
- **Q3 scores in `accepted[0]`:** keep MELD-Na, move to MELD 3.0, or drop scores from the label.
- **Q4 core lab criterion** without TSH, zinc, magnesium, lactate (and CRP reported but not
  required). Logged extras beyond the plan: M06 magnesium, S01 toxicology.
- **Q5 P06 label:** NCSE with concurrent HE kept as a deliberate mimic; confirm.
- **Q6 small ascites** (S07, S11, P09): ultrasound-guided tap required; confirm.
- **Q7 literature** deleted in all 30, approved cases included; confirm.

Tier and pathway deviations to confirm:
- Drug check one tier above plan in M01, M03, S06; CT recommended in M05 and required in S06
  (head trauma possible); M06 ECG added as a required criterion; P03 MRI requires contrast; P09
  keeps CT second; S01 telemetry after the drug check; P08 shunt imaging recommended and no MUST-TX.

Clinical content added or changed (confirm or trim):
- Exam edits made to fit the plan grade: M01, P01, P02 orientation; S10 GCS 11 to 13; S06 grade IV
  kept at GCS 8 (E2V2M4), border of III-IV; S07, S11 grade III; M09 kept grade II.
- Transplant referral: P01 (drug-precipitated first episode, MELD-Na 13) and P02 (still drinking)
  have MUST-TX; M08 (HCC beyond Milan), P08 (MELD-Na 8) and M04 do not; S01 flagged above.
- New musts: M04 empirical antibiotics after cultures and thiamine 200 mg TID (vs 500 mg); P02
  L-carnitine dosing; P05 thiamine accepts both regimens; S03 piperacillin-tazobactam option; S04
  airway must (melena, not haematemesis); S05 ciprofloxacin primary prophylaxis and tenofovir
  options; S06 and S08 alcohol-related hepatitis musts; S08 PROHIB-BZD-WD with anticipated
  withdrawal; S10 drug check content; S11 three extra musts; M08 sorafenib "decide with oncology";
  M10 no pre-emptive TIPS at Child-Pugh C 14; P08 stop aspirin vs review.
- Case narrative edits: M03 precipitant mechanism in the label (TMP-SMX and microbiome) is
  speculative; M04 admission moved to 2 days ago; M05 rifaximin conditional; M06 lactulose-overuse
  history added; M07 rifaximin removed and odd repeated EMS glucose left; M10 ferritin
  re-accumulation; P01 clonazepam dose increase added; P02 HCTZ start date added; P05 label leads
  with Wernicke; P09 24-hour timeline without antibiotics; S05 renal ultrasound rests on notes filed
  on S06.
- S09 (approved): changed beyond the plan list in four places, each logged as a real error.
