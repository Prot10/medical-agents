# PD: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Sources:

- the plan, `plans/PD.md` (classes C1 to C23, pathway section 3, per-case section 4, CENTRAL R1 to
  R10, questions Q1 to Q6);
- the 30 case logs, `logs/PD-*.md`. There is no reviewer notes file: no physician has annotated
  PD in a notes round. The only physician input is Reviewer 1's July 2026 tool guidance
  (`condition_tool_guidance.yaml` key `parkinsons`). Every log has a worker table and an
  adversarial verifier section;
- scripted checks over the 30 case files: M01 to M05, P01 to P04, RM01 to RM05, RP01 to RP05,
  RS01 to RS05, S01 to S06.

All 30 cases are `draft`. The 17 logs of the cases this audit changed end with a
"## Condition audit" section listing the edits and why.

## Final state

**Check results.**

- `perfect_agent.py` on all 30 ids: 30/30 pass, no "same stored report" warning.
- A MockServer probe of every stored follow-up (91 across the 30 cases): each is served for its
  own discriminator, none falls through to a fallback.
- `case_io.py check` on all 30 ids: schema OK and synonym guard OK for every case. The suite has 1
  failure, `test_guidance_claims`, which is expected (R9 below); 3332 tests pass and no failure
  names a PD case.
- `test_case_guards.py -k PD-`: 60 passed. Run directly on the 30 cases, the discriminator, leak,
  banned-string and hijacked-index helpers return nothing, so PD can join
  `DISCRIMINATOR_CONDITIONS` (R3).

**Uniformity checks (scripted, clean after the audit fixes).**

- **Canonical facts (plan 1.2).** MDS 2015 wording: "clinically probable PD" in every first-visit
  PD must; "clinically established" only in M04, RM05 and RP04 (supportive criteria met) and in
  RP03's MSA must. MSA, DLB and PSP musts follow C7 (MDS 2022, McKeith 2017, MDS 2017). M01 to M03
  carry the canonical "PD unmasked by metoclopramide" must; the label fact "metoclopramide is also
  contraindicated in Parkinson's disease" in their drug outputs is kept (product information, not
  a leak). Serotonin syndrome appears only in the canonical SSRI with MAO-B inhibitor sentences.
- **DaTscan and MIBG.** Required in M01, M02, M03 and RM02 (the label rests on it), recommended in
  RP05, optional in M04, RM03, P02, P04, RM05, RS01, S05 and S06, waste in the other 17 cases with
  a stored abnormal report (Q4). Every report is in the canonical binary form; laterality (the
  putamen opposite the worse side) is correct in all 30. MIBG recommended in RP02, optional in
  P01, P02, RP01 and RP03.
- **Tiers, pathway order, constraints, stop rules.** Tiers match plan section 3 and section 4
  (drug review required in M01 to M03, RM05 and RP04; labs required only in P04; neuropsychology
  required only in RP04; ECG and Holter recommended only in RP01; PSG recommended in M05). The only
  sequence constraints are soft MRI (or CT) before DaTscan in the 13 cases with a DaTscan
  criterion. Every stop rule equals the required set with `max_additional_actions` 2.
- **Plan and PATTERNS defects.** No surviving case of: literature outputs (deleted everywhere, Q5);
  `[McKeith_2017_DLB]`; Gilman 2008; "Abnormal values" impressions; the "July 2026" evidence
  lines; "ruling", "ROUND_POLICY", "criteria pack", "earns no credit", "Tier per", "Optional:" or
  "(optional)"; empty `expected_evidence`; a rationale equal to its label; bare citation keys;
  second-tier assays in the first labs (every stored first panel answers the case's first-line
  question); an ECG-as-waste entry beside a domperidone/QTc must (verifiers fixed M01 to M03 and
  RM05). Citation keys in use: Postuma_2015, NICE_NG71, Marshall_2009, Berg_2015, Wenning_2022,
  DLB_2017, Schwarz_2014, ESC_2018, Hoglinger_2017, Litvan_2012, EASL_Wilson_2012, Tolosa_2021.
- **Numbers.** DaTscan, PSG, neuropsychological battery, orthostatic and MIBG figures are unique
  per case. Every exam MoCA now itemises its lost points within the item maxima and agrees with
  the stored battery and the ground truth. CSF fallback glucose ratios agree with the stored serum
  glucose where the case stores one.
- **Left as is (cosmetic):**
  - identical library-style normal fallbacks (EEG in 17 cases, CSF in 19, CT in 20, echo groups);
    each is a normal study no criterion asks for;
  - em dashes in the pre-existing patient text of M01, M02, M04, M05, P02, P03, P04, RM01, RM04 and
    RM05 (no new text adds one);
  - differential entries without an ICD code in P02, P03, RM01, RM02, RP02, RP03, RP04 and S02 to
    S04;
  - `[Postuma_2015]` cited on some avoided-action rationales and on RP04's labs and ECG entries
    (verifier choice, not wrong);
  - "24 /30" spacing in the stored batteries of RM02, RM04, RM05, RP01 and RP02 (library format);
  - G21.11 versus G21.19 for metoclopramide-induced parkinsonism, G24.9 for dystonic tremor and
    G24.1 for dopa-responsive dystonia: all defensible;
  - follow-ups for waste studies listed before criterion-served ones (P03, S03, RP04): routing is by
    discriminator, the probe serves every one correctly, so the order was not changed.

## Error classes and how each was fixed

### Plan classes C1 to C23 (workers and verifiers)

All applied uniformly. The workers logged 548 FIXED rows and 1 FLAGGED row across the 30 logs;
the verifiers added cross-case fixes (the ECG waste entry in M01 to M03, the stop rules).

- **C1, C2. Literature and drug checks.** Literature deleted in all 30 cases (Q5: almost every
  output carried invented or misattributed citations). Drug checks re-tiered per section 3, with
  `{}` arguments matched by the any-query output and content rewritten to the case's own list.
  Leak guard clean (P02 and P03 failed at baseline).
- **C3, C4. Criterion text and evidence.** Labels, rationales and citations rewritten; engineering
  sentences deleted from `key_clinical_evidence`.
- **C5. MRI arguments.** `{"contrast": false, "protocol": "standard"}` replaced with the plain MRI
  criterion, so a real agent's MRI scores.
- **C6, C7. Label and musts.** "Clinically established PD" only where the supportive criteria are
  met; MSA, DLB and PSP cases scored against their own criteria.
- **C8, C9, C17. DaTscan, other library defaults, fallbacks.** A stored abnormal DaTscan in every
  case (the library default is normal, an absolute exclusion); stored PSG, battery, MIBG and
  orthostatic reports where the library would contradict the patient; untyped echo fallbacks
  typed or nulled, amyloid fallback nulled (the discriminator check failed 30/30 at baseline).
- **C10 to C12. Reports.** Inverted H/L flags in PSG and battery impressions rebuilt; reports that
  stated the diagnosis rewritten as findings; MRI reports aligned to the case.
- **C13 to C16. Differential, red herrings, evidence, musts.** Differentials moved to the
  assessment-time view; copied red herrings replaced; evidence asserting absent data removed;
  generic musts and prohibitions replaced with case management.
- **C18 to C20. Doses, metadata, stop rules.** Dose arithmetic and missing medicines fixed;
  metadata rewritten; stop rules equal the required set with 2 additional actions.
- **C21 to C23. Data against the label, templated patients, orthostatic figures.** RP01 and RP02
  data fixed to probable PD (Q2); RS03 and RS04 rewritten to typical PD (Q3); duplicated patients
  made distinct; every orthostatic complaint now has measured figures.

### Classes found by this audit and fixed (23 edits in 17 cases)

- **AA. MoCA losses that do not add up or exceed an item's maximum (5 cases).** The verbal
  fluency item is worth 1 point, abstraction 2, delayed recall 5, serial subtraction 3, clock 3,
  trail-making 1.
  - M01: "verbal fluency (2)" exceeded the item; now trail-making 1, letter fluency 1,
    abstraction 1, delayed recall 2 (25/30).
  - M05: "two points on letter fluency"; now one point each on fluency, abstraction and recall
    (27/30).
  - P01 (25/30), RP01 (24/30) and RP02 (23/30) named two or three items worth less than the stated
    loss; each is now itemised to the total and agrees with the MMSE losses and the stored battery.
- **AB. Tier words in trigger names (4 cases).** P04 `request_optional_counselled_young_onset_pd_genetics`
  became `request_counselled_pd_gene_panel`; S03's PSG trigger became `request_sleep_study`; S05
  and S06 DaTscan triggers became `request_datscan` (the names the other PD cases use). Routing is
  by discriminator and unchanged; the probe confirms each.
- **AC. Tier words in clinical rationales (3 cases).** M04 and RM03 "so the scan is optional"
  became "so the scan is not needed to make the diagnosis"; RS03 "so the check is optional"
  became "so the check does not change the diagnosis". Tiers unchanged.
- **AD. Wrong or incomplete differential ICD codes (3 cases).** M04 "Enhanced physiologic tremor"
  G25.1 (drug-induced tremor) became G25.2; RM04 adhesive capsulitis M75.0 became M75.02 (left
  shoulder); RM03 cervical spondylosis M47.2 (category) became M47.12, the code RM04 uses for the
  same entry.
- **AE. CSF fallback glucose against the stored serum glucose (6 cases).** RS01, RS03 and RS04
  store a raised serum glucose (118, 142, 156 mg/dL) but the CSF fallback kept 62 mg/dL with
  "ratio 0.6" (true ratios 0.53, 0.44, 0.40, the last two reading as low). CSF glucose now 71, 85
  and 94 mg/dL, interpretation "in proportion to the raised serum glucose". The stated ratio was
  rounded wrongly in M04 (0.65, now 0.68), RM02 (0.6, now 0.66) and RP04 (0.69, now 0.70).
- **AF. Self-contradicting fluoxetine sentence (2 cases).** RS03 and RS04 said both "use the
  lowest dose and monitor" and "best avoided" for fluoxetine with rasagiline; now "serotonin
  syndrome is rare, but fluoxetine and fluvoxamine are best avoided with rasagiline; at least 5
  weeks should pass between stopping fluoxetine and starting rasagiline" (rasagiline product
  information). The canonical sertraline sentence (RM01, RM03, RS02, RP02) is unchanged.

## Counts

- Cases changed by the round: 30 of 30 (all re-tiered and rewritten to the plan).
- Worker and verifier rows: 548 FIXED, 1 FLAGGED.
- This audit: 23 own findings fixed in 17 cases (M01, M04, M05, P01, P04, RM02, RM03, RM04, RP01,
  RP02, RP04, RS01, RS03, RS04, S03, S05, S06); 7 cosmetic items left and listed above; 1
  verifier question decided (RP02 MIBG, below).

## CENTRAL requests (consolidated)

- **R1. Pack and keys** (`criteria_packs/PD.md`): literature and drug checks no longer `REQUIRED`;
  add `[NICE_NG71]`, `[Wenning_2022]`, `[DLB_2017]`, `[Hoglinger_2017]`, `[Litvan_2012]`,
  `[ESC_2018]` and `[EASL_Wilson_2012]` (all used in cases, none in the pack yet); mark Gilman 2008 superseded by Wenning
  2022; state the established-versus-probable rule (F1) and the four supportive criteria. The
  CENTRAL_PENDING item "`[McKeith_2017_DLB]` should become `[DLB_2017]`" is resolved: no PD case
  uses the old key.
- **R2. Generator.** Stop emitting literature criteria and required drug checks for PD; stop the
  "Abnormal values" impression builder for lower-is-worse measures, the "July 2026" evidence lines,
  the amyloid PET fallback, the MRI `{"contrast": false, "protocol": "standard"}` arguments and
  tier words in trigger names and rationales (AB, AC); compute the CSF fallback glucose from the
  case's serum glucose (AE); itemise MoCA losses within item maxima (AA). Update the `parkinsons`
  follow-ups in `conditions.yaml` to plan section 3.
- **R3. Guard.** Add PD to `DISCRIMINATOR_CONDITIONS`: all 30 cases pass the helper now. Remove PD
  from the CENTRAL_PENDING discriminator line ("PD 30/30" left).
- **R4. Vocabulary.** `perform_clinical_assessment` `levodopa_challenge` (MDS-UPDRS III OFF and ON,
  RP04 and any DBS case); `order_specialized_test` `olfactory_test` (UPSIT, Sniffin' Sticks);
  `laryngoscopy` for MSA stridor (RP03) if other conditions need it.
- **R5. Library.** The DaTscan default is normal, which excludes every parkinsonism label. Make
  the DaTscan, MIBG, PSG, neuropsychological, orthostatic, autonomic and tilt defaults
  condition-aware, or add a guard that fails a case when a library default contradicts the
  patient block (exam MoCA below 28 with no stored battery; dream enactment with no stored PSG; a
  parkinsonism label with no stored DaTscan; measured orthostatic hypotension with a normal
  orthostatic default).
- **R6. ICD.** WHO ICD-10 2019 and ICD-10-GM code MSA-P G23.2 and MSA-C G23.3. Verify the
  ICD-10-CM tabular, then add both to the accepted codes of P01 and RP03 through the synonyms file;
  `icd_codes[0]` stays G90.3 until Andrea rules (question 2 below).
- **R7. Perfect agent and scorer.** `perfect_agent.py` should call each tool with the minimal
  arguments a real agent would use (the baseline false pass came from exact `query` and `drug`
  strings); a guard could forbid free-text `required_arguments` on knowledge tools.
- **R8. Condition scoping.** P01 (MSA-P), P02 (DLB), P03 (PSP-RS) and RP03 (MSA) sit under
  `parkinsons` with a PD prefix; the paper's per-condition counts must describe them (question 1).
- **R9. Guidance answers.** Regenerate the `parkinsons` `our_response` texts of
  `condition_tool_guidance.yaml` from the edited cases (this is the expected
  `test_guidance_claims` failure): ECG and Holter now recommended in RP01, labs required in P04
  and recommended in RM02, RM05 and RS01, the PSG count (RP02 gained an optional PSG), the
  neuropsychology and genetics counts. Show the RP01 ECG departure to Reviewer 1 with its reason
  (ESC 2018: 12-lead ECG in every syncope).
- **R10. Vocabulary in use.** `perform_clinical_assessment` `orthostatic_blood_pressure` is used
  in a case for the first time; the probe confirms the stored follow-ups route.
- **R11. UI note for the physician reviewer (RP02).** The verifier asked whether a delayed MIBG
  H/M of 1.21 can be read in a man on sertraline with paroxysmal AF. Decided: keep the report.
  The echo fallback shows EF 65% with no heart failure, he has no diabetes or coronary disease,
  sertraline is not a recognised major cause of a reduced H/M ratio, and AF with normal left
  ventricular function does not explain it. The review app should show the reviewer this note so
  they can confirm.

## Open questions

Decided here (Andrea's rule: decide in the way best for dataset quality), recorded, no action
needed:

- Q1 to Q6 keep the plan defaults: MSA, DLB and PSP stay as PD-mimic cases; RP01 and RP02 data
  fixed to probable PD; RS03 and RS04 rewritten to typical PD; DaTscan waste where the diagnosis is
  clinical; RP01 keeps its ECG; literature deleted.
- P01 medication review stays recommended: no D2 blocker is involved, and the nOH must already asks
  for the tamsulosin, lisinopril and sildenafil review.
- RM02 labs stay recommended: the valproate level and ammonia grade the drug's contribution but do
  not change the diagnosis once the DaTscan is abnormal; no repeat-ammonia must (58 umol/L, mild,
  asymptomatic).
- RP02 optional PSG (plan C9 rule) kept; counted in R9.
- RP03 keeps six musts (stridor, bladder and the levodopa trial each change management) and its
  mixed MSA-P/C label.
- RP04: genetics not added (plan limits it to P04 and RM05; the library's negative panel does not
  contradict the case); the B12 of 248 pg/mL is low-normal and flagged in the log, not a must,
  because labs are optional.
- RS03 and RS04 keep their seed `metadata.source_pmcid` as the provenance record, although the
  rewritten content no longer follows the seed.
- RP02 MIBG report kept (R11).

For Andrea (need his information or ruling):

1. **Re-prefixing the PD-mimic cases.** P01, P02, P03 and RP03 keep `PD-` ids with MSA, DLB and
   PSP labels. Moving them to their own conditions changes `case_id` and the splits; say whether
   to do it in a later round or to keep them as PD-mimic cases in the paper.
2. **Primary ICD code for MSA.** G90.3 (ICD-10-CM) or G23.2/G23.3 (WHO 2019, ICD-10-GM) as
   `icd_codes[0]` in P01 and RP03. Both are accepted once R6 lands; the primary choice depends on
   which ICD edition the paper reports.
