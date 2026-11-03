# BACT-MEN: decisions on the open questions (24 October 2026)

Andrea, 24 Oct 2026: resolve every open point "nel modo migliore per la qualità del dataset". Each
entry gives the question, the decision, the reason with its source, and what changed where. Every
source cited here was checked on 24 Oct 2026; the WHO 2025 meningitis guideline was read in full text
(IRIS PDF, ISBN 978-92-4-010804-2) and NICE NG240 from its recommendations page.

Verified facts used below:
- WHO 2025, section A.4 (cranial imaging, a recommendation section of chapter 3, **not an annex**):
  imaging before LP where readily accessible if GCS below 10, focal neurological signs, cranial nerve
  deficits, papilloedema, new-onset seizures (adults) or severe immunocompromised state (example given:
  organ transplantation). A.1.1: no LP with a known or suspected bleeding diathesis, skin or soft-tissue
  infection at the site, or haemodynamic or respiratory compromise that requires stabilisation.
- WHO 2025, B.2 remarks: Listeria risk factors are age over 60, pregnancy, immunosuppressive therapy,
  organ transplantation, malignancy, advanced HIV disease, **diabetes mellitus**, end-stage kidney
  disease, liver cirrhosis, alcohol use disease.
- WHO 2025, B.3: corticosteroid recommendations apply to people with HIV on ART with an undetectable
  viral load (below 50 copies/mL); no proven benefit in advanced HIV disease; continue up to 4 days for
  S. pneumoniae or Hib, can be discontinued for other pathogens.
- WHO 2025, C.4: formal audiological screening before discharge, or within four weeks of discharge, in
  children and adults with acute meningitis from any cause (strong recommendation).
- NICE NG240: 1.4.6 to 1.4.7 imaging; 1.4.11 treat and stabilise shock, respiratory compromise,
  uncontrolled seizures and bleeding risk before LP; 1.4.12 no LP with extensive or rapidly spreading
  purpura; 1.6.6 amoxicillin for Listeria risk factors; 1.8.3 to 1.8.5 dexamethasone; 1.12.7 audiology.

## Step 1: leak

**P04** `followup_outputs[4]` drug-check summary repeated the expected evidence of
`action-6-check-drug-interactions`. Decision: rewrite the summary in report voice ("Ceftriaxone and
dexamethasone: no contraindication found for this patient. One clinically significant interaction:
ibuprofen with dexamethasone ...; discontinuation of ibuprofen advised."). Same clinical content.
Changed: case P04. All 90 BACT-MEN guards pass.

## Plan and summary questions

**Q1. P02 (TB, A17.0) and P03 (cryptococcal, B45.1) in `bacterial_meningitis`.** Decision: keep both
as mimic cases with their own pathways and labels. Reason: the benchmark has no TB or fungal CNS
condition to move them to, the criteria pack lists TB and cryptococcal disease as the R-variant mimics
of this condition, and scoring uses each case's own label and ICD code, so nothing is misattributed.
No change.

**Q2. CT as `waste` in no-criterion cases.** Decision: keep (P01, P04, RP01, RS01, RS05, S05), because
WHO 2025 A.4 and NICE 1.4.6 both advise against routine imaging and `waste` is the mildest penalty;
two exceptions: RS03 (see Q5) and S06. **S06**: the case stores a temporal-bone CT, records a residual
middle-ear effusion after recent otitis, and pneumococcal meningitis with a recent otitis makes a
mastoid CT a defensible source study, so penalising it is wrong. Changed: S06 avoided action
`avoid-waste-6-order-ct-scan` removed (CT neither required nor penalised; ENT must kept).

**Q3. WHO-first where WHO and NICE diverge.** Decision: confirmed, WHO 2025 governs (global, 2025,
covers the immunocompromised hosts that NICE NG240 excludes). Related hearing must: it cited NICE
NG240 in patients outside NICE scope; WHO 2025 C.4 has its own strong recommendation covering everyone.
Changed: in 27 cases the canonical must now reads "Arrange formal audiological assessment before
discharge, or within 4 weeks of discharge if it cannot be done before (WHO 2025, strong
recommendation)" (case-specific suffixes kept); criteria pack updated.

**Q4. RM04 CT on the bilateral CN VIII deficit.** Decision: keep CT required with the HARD constraint.
Reason: WHO 2025 A.4 lists cranial nerve deficits without qualification (verified wording) and the
reviewer (7fdda22c) accepted either option provided it was stated; the cost of the guideline-literal
choice is a short CT after antibiotics, while the alternative would score a guideline-concordant CT as
non-required. No change.

**Q5. RS03 prednisolone 30 mg for about two weeks.** Decision: CT before LP is neutral. Reason: WHO
2025 gives no steroid threshold for "severe immunocompromised state" (its example is organ
transplantation), while 20 mg or more of prednisone daily for 14 days or more is high-level
immunosuppression in the IDSA 2013 vaccination guideline (Rubin LG et al., Clin Infect Dis
2014;58:e44-e100). A genuinely ambiguous threshold must not penalise either defensible course.
Changed: RS03 CT waste avoided action removed; the "proceed to LP without imaging" must and key
evidence replaced by a must accepting either course with cultures, antibiotics and dexamethasone first;
the CT prohibition removed (the generic "do not delay antimicrobials" prohibition remains). Pack: rule
added for high-level steroid immunosuppression; key `[IDSA_2013_Vaccination]`.

**Q6. S02 and S04 papilloedema removed.** Decision: confirmed. Papilloedema develops over days of
raised pressure and is implausible after 10 and 18 hours of illness. No change.

**Q7. Diabetes as a Listeria risk factor.** Decision: confirmed, and now on WHO's own authority: the
WHO 2025 B.2 remarks list diabetes mellitus explicitly (the earlier pack text attributed it to
Reviewer 2 only). The Listeria musts in S02, S04, RM04, RP05, RS01 stand. Checked the cases without
Listeria cover against the full WHO list (alcohol use disease, cirrhosis, malignancy, end-stage kidney
disease): none qualifies (M05 has a glioblastoma but is healthcare-associated, IDSA 2017). Changed:
criteria pack Listeria line.

**Q8. Recoding.** M04 and RS05 were already A32.11 (ICD-10-CM listerial meningitis; G00 excludes it).
**RM04** recoded G00.8 to **G00.2** (ICD-10-CM G00.2 Streptococcal meningitis, with B95.4 for other
streptococci; S. suis is a streptococcus, and G00.8 is for organisms without their own code).
Synonyms: the G00.2 category entry carried "group b streptococcus meningitis", which would have been
accepted for S. suis; it now carries only "streptococcal meningitis", with case-scoped entries
`G00.2+gbs` (RS01) and `G00.2+suis` (RM04, "streptococcus suis meningitis"). Script run with `--prune`
for bacterial_meningitis (RM04 loses "other bacterial meningitis"); `--check` clean. Changed: RM04,
RS01 (labels), `diagnosis_synonyms.yaml`.

**Q9. Literature criterion removed in all 30.** Decision: confirmed (ruling 5). No change.

**Q10. LP in shock, spreading purpura or coagulopathy.** Decision, per case on WHO 2025 A.1.1 and NICE
1.4.11 to 1.4.12:
- **S05** (rapidly spreading purpura, platelets 94, INR 1.4, compensated shock): NICE 1.4.12 forbids LP
  with rapidly spreading purpura and WHO forbids it with a bleeding diathesis, so a required LP rewarded
  a contraindicated act. `action-3-analyze-csf` is now `optional` (with the deferral in its label) and
  out of the stop rule; the "proceed to LP" must and key evidence became a deferral must (LP once the
  rash stops spreading, she is stable and coagulation is corrected; blood cultures and blood PCR carry
  the diagnosis; antibiotics not delayed); the CT prohibition became "do not perform the LP while the
  purpura is spreading or the coagulopathy is uncorrected, and do not delay antibiotics"; the
  septicaemia-without-meningitis differential now rests on meningism rather than on the CSF. Not made
  a harm-avoided action: an LP after stabilisation remains legitimate.
- **S04** (shock 85/53, petechiae without spreading purpura, platelets 95, INR 1.5): NICE 1.4.11 and WHO
  A.1.1 require stabilisation and correction first, not abstention, so the LP stays required; the must
  and key evidence add "stabilise the shock and correct the coagulopathy first (WHO 2025 A.1.1; NICE
  NG240 1.4.11)".
- **RM01** (92/58, platelets 142) and **S02** (90/54, platelets 147): must added, "Resuscitate the
  hypotension before the lumbar puncture"; WHO only in RM01 (asplenia, outside NICE scope).

**Q11. "Overt DIC" with an ISTH score of 3 to 4.** Decision: keep Reviewer 2's ruling (DIC present)
and make the stored values support it, rather than weakening the ruling. ISTH overt DIC (score 5 or
more: platelets 50 to 100 = 1; D-dimer strongly raised = 3; PT prolonged 3 to 6 s = 1). Changed: **S04**
D-dimer 4.4 to 6.2 ug/mL FEU (more than 10 times the upper limit; score 5); **S05** PT 14.1 to 15.6 s
and INR 1.3 to 1.4 (score 5); key evidence names the score. Reviewer-cited numbers changed: logged.

**Q12. Meningococcal disease likelihood (M02 moderate, S04 high) against ruling 7.** Decision: `low` in
both. The differential is the assessment-time view for all 600 cases; at assessment N. meningitidis is
not detected and S. pneumoniae grows from blood (and CSF in S04). The reviewer's substantive ask, that
the entry exist with its bedside role and its exclusion route, is kept verbatim in `key_features`.

**Q13. Dexamethasone departures.**
- RP02: confirmed not required (WHO 2025 B.3: benefit falls with delay, given with or soon after the
  first antibiotic dose; she had days of parenteral meropenem; NICE 1.8.5 asks for specialist advice
  beyond 12 hours). No change.
- RM04: confirmed (Reviewer 2's reassessment wording, WHO permits stopping); the trade-off now also
  cites van Samkar A et al., PLoS Negl Trop Dis 2015;9(10):e0004191 (S. suis meta-analysis: hearing
  loss in 53%, dexamethasone associated with less hearing loss) next to Mai NTH et al., NEJM
  2007;357:2431-2440.
- **RP03: reversed.** WHO 2025 B.3 applies corticosteroids in HIV only on ART with an undetectable viral
  load; his viral load is 4850 copies/mL after 2 months of ART, and WHO reports no proven benefit in
  advanced HIV disease (a prior and a current meningitis episode are WHO stage 3 events). The must and
  key evidence now say not to give dexamethasone by default; the drug check, its criterion label, the
  imaging must and the soft constraint no longer include it.

**Q14. M05.** Decision: confirmed as is. The SOFT "EVD CSF before CT" is clinically right (bedside EVD
sampling carries no herniation risk and culture is the key test, IDSA 2017); co-trimoxazole-susceptible
MSSA on prophylactic dosing is plausible; the culture in the index EVD report follows the reviewer's
note. No change.

**Q15. Additions beyond the notes.** Decision: keep all; each is guideline-supported (sepsis care, SSC
2021; immunosuppression plan; RS04 urine culture with a catheter, IDSA 2017; ART and fluconazole, WHO
2022; pneumococcal vaccination after recurrent meningitis or a CSF leak; levetiracetam with efavirenz;
removing an IGRA from the TB first panel). RP03 syphilis criterion now cites `[CDC_STI_2021]`
(Workowski KA et al., MMWR Recomm Rep 2021;70(4)); see also the extra items.

**Q16. Plausibility margins.**
- RP03 CSF 3 cells with protein 205: kept; Reviewer 2 offered co-trimoxazole partial treatment as the
  rescue and it is stated; the case's teaching point ("do not exclude bacterial meningitis on a
  near-normal CSF white count when PCR or blood cultures identify a pathogen") depends on it.
- RP03 unexplained left-sided chest pain: removed from the chief complaint and HPI (nothing in the case
  explains it).
- RP01 post-vaccine pneumococcal titres returned with the immunoglobulins: the serotype-specific IgG is
  now "Pending (send-out assay; turnaround about 2 weeks)"; the immunology must no longer relies on it.
- P04 CSF glucose 34 (ratio 0.37): consistent; no change.
- P01 random glucose 102 flagged high: reference changed to 70-140 mg/dL (random, non-fasting), not
  abnormal.

**Q17. Scored versus must-only imaging.** P05 and S02 conditional MRI musts and P02 chest imaging must:
kept as musts (the fallback library answers an MRI order with a normal report; nothing is required that
the guideline does not require). **P03 MRI**: required to recommended and out of the stop rule (WHO 2022
needs CSF opening pressure and CrAg, not MRI; the required CT already screens for a mass).

**Q18. Echocardiography as waste.** Decision: confirmed. No BACT-MEN case records a murmur, embolic
stigmata or persistent bacteraemia; routine echocardiography is not part of the meningitis work-up.

**Q19. S01 and S03.** S01: confirmed; it is a B case with no constraint between CT and LP, so an agent
following NICE 1.4.7 (CT first for a progressive fall in consciousness) and one following WHO are both
scored correctly. **S03**: "occasional paraphasic errors" is a focal cortical sign under WHO A.4 and
contradicts Reviewer 2's ruling (f73b0114) that no criterion is present; MRI shows no cortical lesion,
so the record was corrected to "Speech is slow and confused, without dysphasia on bedside testing".

**Q20. RS04 meropenem dose.** Ward weight 44 kg (height 160 cm, BMI 17.2) recorded in the HPI;
Cockcroft-Gault clearance about 43 mL/min. The must now gives the first dose in full, then meropenem 2 g
every 12 hours (clearance 26 to 50 mL/min), reviewed daily because dolutegravir and trimethoprim raise
creatinine without lowering GFR.

**Auditor flags.** The summary has no separate auditor-flag section; its one flagged item (RS02
"community acquired" synonym) is correct (a VP shunt patient with community-onset pneumococcal disease)
and the healthcare-associated cases are already excluded by `G00+community`.

## Extra items in the brief

- **"Reference to confirm" entries** (criteria pack section 8): `[CLSI_M100]` completed as M100 36th
  edition, 2026 (CLSI shop: January 2026, replaces Ed35); `[WHO_TB_Module4]` completed as the 2025
  consolidated Module 4, ISBN 978-92-4-010724-3, 15 April 2025; `[SSC_2021]` completed as Evans L et al.,
  Crit Care Med 2021;49(11):e1063-e1143; `[Mai_2007]` completed with authors and pages. New keys:
  `[van_Samkar_2015]`, `[CDC_STI_2021]`, `[Tebruegge_2008]`, `[IDSA_2013_Vaccination]`.
  `[WHO_Meningitis_2025]` ISBN verified and its section map added.
- **"WHO 2025 Annex A.4"** (raised by the coordinator from the HEP-ENC agent): the guideline has no
  Annex A.4; the imaging recommendations are section A.4 of chapter 3 ("A.4 Cranial imaging"). Renamed
  "section A.4" in all 29 case files that used it, in the criteria pack and in the conditions.yaml CT
  description. The plan and summary files keep the old wording as history.
- **RP03 syphilis criterion**: cites `[CDC_STI_2021]`. **RP04 immune work-up criterion**: cites
  `[Tebruegge_2008]` (Clin Microbiol Rev 2008;21:519-537: 36% of recurrent bacterial meningitis is due
  to immunodeficiency, mostly complement and antibody defects).
- **Miller 2026 pregnancy reference**: not used by any BACT-MEN case, pack or plan (it belongs to
  ISCH-STR-RS04); nothing to do here.
- **RM04 G00.2**: done (Q8).
- **conditions.yaml** bacterial_meningitis block: the remaining follow-ups are defensible
  (`request_ct_head`, `request_blood_cultures`); the CT description now follows WHO A.4 verbatim
  (readily accessible, at presentation, after cultures and the first antibiotic dose, otherwise only for
  a source study after the LP); the blood culture description states the 7-day antimicrobial rule; a
  `request_lumbar_puncture` follow-up was added so a regenerated case gets the index LP as a pathway
  step (class C1) with the A.1.1 deferral rule; the comment "CT-then-LP-then-empirics" (antibiotics last,
  contrary to WHO and NICE) was corrected; "ratio <0.4" now "0.4 or less" (WHO A.2.2).

## Cases changed

29 case files (all except M05): the hearing and section A.4 renames, plus the specific changes above
in M02, P01, P03, P04, RM01, RM04, RP01, RP03, RP04, RS01, RS03, RS04, S02, S03, S04, S05, S06. Each
case log has a "## Open questions resolved (24 Oct 2026)" section. Checks: `perfect_agent.py` 30/30;
`case_io.py check` on all 30: schema OK, synonym guard OK, no failure names a BACT-MEN case; BACT-MEN
guards 90 passed; synonym `--check` clean.

## Still needing Andrea

Nothing that needs information only Andrea has.

## CENTRAL

1. Vocabulary (unchanged from the summary): `interpret_labs` `beta2_transferrin` (unblocks RP04 note
   8f75c86a part 1), `serum_cryptococcal_antigen`, `CD4_count`, `HIV_viral_load`; `analyze_csf`
   mycobacterial, fungal culture, India ink, ADA and a shunt or EVD source term; `order_microbiology`
   `wound_swab`, `sputum`; `order_specialized_test` `audiometry`.
2. S05: if `order_microbiology` gains (or has) a blood meningococcal PCR term, a recommended blood PCR
   criterion would let the deferred-LP pathway score the organism test NICE 1.4.4 names.
3. Other conditions citing "WHO 2025 Annex A.4" (HEP-ENC decisions file mentions it): the correct
   reference is "section A.4".
