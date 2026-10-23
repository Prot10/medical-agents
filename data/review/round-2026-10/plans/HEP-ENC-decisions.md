# HEP-ENC: open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026: decide every open point for the best clinical quality and benchmark
validity, and apply it. Sources were verified on 24 Oct 2026 (web search of the journal record or
DOI) before being cited. Every case change is also logged under "Open questions resolved (24 Oct
2026)" in that case's log.

## Leaks (any-query outputs)

**L1. Drug-check outputs repeating expected evidence (M03, M04, M05, P04, P06, S06, S07).**
Decision: reword `expected_evidence` of the drug-check criterion, not the report. Reason: each
stored report already carries the real, case-specific interaction content in checker voice (ruling
6); the criterion text had been written as a summary of it. The new evidence states the conclusion
a grader checks, with no 60-character overlap. Clinical content unchanged. Changed: the seven
`action-N-check-drug-interactions.expected_evidence`. Guard: 90/90 HEP-ENC pass.

## Plan questions (summary "Open questions for Andrea")

**Q1. M05 premise.** Decision: confirmed as applied (constipation precipitant; zinc excess with
copper deficiency incidental). Reason: zinc deficiency, not excess, is linked to HE; excess zinc
causes copper deficiency (EASL 2022). No change.

**Q2. Culture tier threshold (T 38.0 °C, WBC above 11, infective precipitant).** Decision: keep the
rule. Edge cases: P06 stays recommended (WBC 11.2 about an hour after a generalised seizure,
afebrile: post-ictal demargination), and the pack now names this as the one exception. S04 and S08
stay required (WBC above 11 with a bleed: infection is common and prophylaxis is due, Baveno VII).
M03 stays recommended (UTI already treated, afebrile, WBC 6.2). P07 stays optional (outpatient
covert HE). Changed: pack section 2 tier rule.

**Q3. Scores in `accepted[0]`.** Decision: keep classic MELD-Na (Kim 2008) and Child-Pugh. Reason:
both can be recomputed from the printed values; the reviewers used MELD-Na; MELD 3.0 adds sex and
albumin terms and would reopen 30 labels for no gain in validity. The label is not token-matched
(synonyms carry the scoring), so the numbers do not affect the scalar. No change.

**Q4. Core lab criterion.** Decision: confirmed (CBC, CMP or BMP + LFTs, coagulation, ammonia, plus
case extras; CRP, TSH, zinc, magnesium and lactate in the report, not required). Reason: ACG 2026
treats HE as a clinical diagnosis with a targeted precipitant search; requiring every analyte would
reward ordering by template. No change.

**Q5. P06 label.** Decision: keep NCSE with concurrent HE as the deliberate mimic case (G41 codes,
EEG required). Reason: the R-type mimic is part of the condition's design (pack section 6), and the
EEG establishes NCSE. No change.

**Q6. Small ascites (S07, S11, P09).** Decision: ultrasound-guided diagnostic paracentesis stays
required. Reason: EASL 2018 and AASLD 2021 recommend a diagnostic tap in every hospitalised
cirrhotic with ascites and encephalopathy; ultrasound guidance is standard for small volumes. No
change.

**Q7. Literature deleted in all 30 (approved cases included).** Decision: confirmed. Reason: ruling
5 makes literature at most optional; nothing in HE depends on it. No change.

## Tier and pathway deviations

**Drug check one tier above plan (M01, M03, S06 recommended).** Confirmed. Ruling 6 allows
recommended; each has a relevant interaction (diuretics with hypokalaemia, TMP-SMX with
spironolactone and methadone, sertraline in Child-Pugh C).
**CT recommended in M05, required in S06.** Confirmed: S06 is coma with possible head trauma, an ACG
2026 trigger.
**M06 ECG required** (K 2.6). Confirmed. **P03 MRI with contrast** (prostate cancer: metastasis
question). Confirmed. **P09 CT second, S01 telemetry after the drug check** (approved cases).
Confirmed, no change. **P08 shunt imaging recommended, no MUST-TX** (Child-Pugh A, MELD-Na 8; shunt
embolisation must present). Confirmed.

## Clinical content added this round (confirm or trim)

Checked: M04 thiamine 200 mg IV three times daily (EFNS 2010 treatment dose; fine), P02 L-carnitine
100 mg/kg (max 6 g) then 15 mg/kg every 4 hours (standard regimen), S03 piperacillin-tazobactam
option, S05 primary SBP prophylaxis with ciprofloxacin (ascitic protein 0.9 g/dL, bilirubin 9.8,
creatinine 1.8 meet EASL 2018 criteria; sulfonamide allergy excludes co-trimoxazole), M08 sorafenib
held and resumed with oncology, M10 no pre-emptive TIPS at Child-Pugh C 14 (Baveno VII: C 10-13 or B
8-9 with active bleeding), P08 stop aspirin without a vascular indication with thrombocytopenia,
transplant musts in P01 (overt HE is a decompensating event) and P02. All confirmed.
**Trimmed:** M03 `accepted[0]` carried a speculative mechanism "(gut microbiome disruption reducing
lactulose efficacy)"; removed, TMP-SMX now a possible contributor beside the constipation
precipitant (ICD unchanged).
Exam edits for grade (M01, P01, P02, S06, S07, S10, S11, M09): confirmed, they match the West Haven
definitions of the pack.

## Auditor flags

**S01 no transplant must (approved).** Decision: add MUST-TX, and an alcohol-withdrawal must.
Reason: the round deleted S01's transplant panel under C1 without the replacement must that C16
requires, so this is a regression of this round, not a reviewer-approved choice; S04, S06, S08 carry
it. Ethanol 168 mg/dL with heavy daily drinking makes withdrawal likely within the admission.
Changed: S01 `required_recommendations` (+2).
**S01 PROHIB-BZD with ethanol 168.** Decision: keep PROHIB-BZD (it forbids benzodiazepines for
agitation or sleep, which is right); withdrawal is covered by the new must. No other change.
**M04 no MUST-TX.** Decision: keep. The Lille must at day 7 sets the next decision.
**S05 order (required renal ultrasound before optional CT).** Decision: keep. Obstructed
pyelonephritis needs source control before an optional head CT; list order is clinical order.
**S11 initial EEG with no criterion.** Decision: keep; it is served only if ordered and is
consistent with HE.
**S09 (approved) "uV", em dashes, fallback ECG 65 vs HR 88.** Decision: correct the ECG rate to 88
(real inconsistency); leave typography.
**M09, M10 lack the "HE is a clinical diagnosis" pearl.** Decision: add it (canonical text) at
`key_clinical_evidence[0]`.
**Pre-existing em dashes.** Leave: not errors, and changing them sends cases to re-review.
**Fallback MRI templates in P03, P04, P05.** Decision: set `fallback_tool_outputs.mri` to null.
`analyze_brain_mri` has no discriminator, so the initial MRI always answers; the normal template was
unreachable and contradicted the case MRI.

## Extra items

**E1. 'Reference to confirm' entries in the criteria pack.** All verified and completed:
- `[EXTRIP_lithium_2015]`: Decker BS et al., Clin J Am Soc Nephrol 2015;10:875-887.
- `[EASL_PBC_2017]`: EASL CPG PBC, J Hepatol 2017;67:145-172.
- `[AASLD_IDSA_HCV]` renamed `[AASLD_IDSA_HCV_2023]`: Bhattacharya D et al., Hepatitis C Guidance
  2023 Update, Clin Infect Dis 2023, doi:10.1093/cid/ciad319. S07 must text now says "2023 update".
- Found while checking: S05 cited the EASL 2017 HBV guideline, superseded by EASL CPG HBV 2025
  (J Hepatol 2025, doi:10.1016/j.jhep.2025.03.018); added `[EASL_HBV_2025]`, S05 must updated.
- Also completed: `[ACG_HE_2026]` DOI 10.14309/ajg.0000000000003899 (verified: Am J Gastroenterol
  2026;121(3):588-618); `[Brigo_2015]` title and DOI 10.1007/s00415-014-7369-9.
No case key cites these as bracketed keys (the musts cite in free text), so no key was removed.

**E2. S01 and S04 grade III coded K72.91 ("with coma").** Decision: K72.90 for both. Grade III is
somnolent but rousable (GCS 10 in both); only grade IV (S06) is coma and keeps K72.91. Checked all
30: no other grade-code mismatch. Synonyms re-derived (`--check --prune` clean).

**E3. conditions.yaml difficulty_variants.** Rewritten to the clinical picture only (no ammonia,
INR, EEG or CT results, no lab-derived hyponatraemia), with a comment stating the rule. Also in the
same block, the key_findings lines that contradicted the pack were corrected: ammonia thresholds that
implied grading (now "one admission value, neither grades nor confirms HE"), "Blood cultures:
positive" in every straightforward case (now an infective precipitant reported by microbiology when
present), and "NCSE cannot be excluded without benzodiazepine challenge" (now "excluded by the EEG
itself, never by a benzodiazepine challenge").

**E4. HE common_followups and the CT follow-up description.** The two follow-ups
(`request_diagnostic_paracentesis`, `request_urine_specimen` under `order_microbiology`) are
confirmed: they match the pack (tap only with ascites; one urine specimen and time point). The
paracentesis description now adds bedside inoculation into blood-culture bottles (EASL 2018; AASLD
2021). The "WHO 2025 Annex A.4" CT description is not in the HE block: it is the
`bacterial_meningitis` CT-before-LP follow-up, outside this agent's write scope, so it was not
edited here; it belongs to the BACT-MEN decisions.

**E5. P04 Wilson disease in the score (summary CENTRAL 5).** Decision: score it. P04 recoded
E83.01 (Wilson disease) with a case-scoped synonym entry requiring Wilson disease and HE together
(`wilson disease hepatic encephalopathy`, `wilson disease HE`, `wilsons disease hepatic
encephalopathy`, `hepatolenticular degeneration hepatic encephalopathy`); generic HE labels and
codes pruned from P04. Reason: the case exists to test recognition of the unrecognised Wilson
disease, and the generic labels or K72.90 gave full credit without it. `accepted[0]` unchanged.
**P07 overt synonym, P08 "hepatic coma"** (summary CENTRAL 5): already resolved in the table
(`K72+overt` excludes P07; `hepatic coma` scoped to S06). No change.

## Cases changed

M03, M04, M05, M09, M10, P03, P04, P05, P06, S01, S04, S05, S06, S07, S09 (S01, S09 approved).
Shared files: `diagnosis_synonyms.yaml` (new `E83.01` entry), `conditions.yaml` (HE block only),
criteria pack `HEP-ENC.md`.

## CENTRAL

1. The citation allow-list request (summary CENTRAL 1) gains `[EASL_HBV_2025]` and renames
   `[AASLD_IDSA_HCV]` to `[AASLD_IDSA_HCV_2023]`.
2. The scorer accepts a diagnosis on an ICD code alone. In mixed cases (P04) the secondary condition
   can be scored only by recoding; a per-case "all of" rule would be cleaner.
3. `fallback_tool_outputs` for a tool that also has an initial output and no discriminator is dead
   data; a schema or test check would stop templates that contradict the case.
4. BACT-MEN owner: confirm the `bacterial_meningitis` CT follow-up wording against the WHO 2025
   guideline annex (not checked here, outside scope).
