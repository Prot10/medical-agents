# ALS: decisions on the open questions (24 Oct 2026)

Andrea ruled on 24 Oct 2026: "per i punti aperti, risolvili nel modo migliore per la qualità del
dataset", and any-query outputs (literature, drug interactions) must not repeat the
`expected_evidence` of any criterion, their own criterion included. Every item below is decided and,
where a change was needed, applied. Per-case detail is in each case log under "Open questions
resolved (24 Oct 2026)".

Sources checked on 24 Oct 2026: Van Damme P et al., EAN guideline on the management of ALS (with
ERN EURO-NMD), Eur J Neurol 2024;31(6):e16264, doi 10.1111/ene.16264; Roggenbuck J et al.,
Evidence-based consensus guidelines for ALS genetic testing and counseling, Ann Clin Transl Neurol
2023;10(11):2074-2091, doi 10.1002/acn3.51895; Miller RG et al., Practice Parameter update: the
care of the patient with ALS: drug, nutritional, and respiratory therapies, Neurology
2009;73(15):1218-1226 (PubMed 19822872). The remaining pack references (Gold Coast 2020, Awaji
2008, EFNS 2012, NICE NG42, Bourke 2006, Brown 2017, ENCALS 2018) already carry full and correct
bibliographic data.

## Step 1: leaks

| case | decision | change |
| --- | --- | --- |
| ALS-M03, ALS-RM11, ALS-S02 | The riluzole check output and the criterion's `expected_evidence` shared policy wording ("advise reducing the nightly alcohol because riluzole can raise...", "dysphagia with choking raises the risk of oesophageal injury"). Both texts reworded: the expected evidence in short policy voice, the output in report voice (what the interaction check says: alcohol as an additive hepatotoxicity risk, oral bisphosphonates and oesophagitis with dysphagia, the SmPC monitoring schedule). Clinical content unchanged. | `ground_truth.action_criteria[action-2-check-drug-interactions].expected_evidence`; `followup_outputs[check_drug_interactions].output.interactions[...]`, `.summary` |

All 30 ALS cases pass the leak, follow-up and banned-string guards.

## Step 2: open questions

### Condition-wide (summary Q1-Q10)

1. **Q1 / brief items: does ALS-P02 stay in the ALS condition?** Decision: keep it, as an ALS-mimic
   puzzle labelled with the mimic's own code (E05.90). Reason: this is how the dataset builds mimic
   cases in 15 of 20 conditions (e.g. migraine cases coded I63.9, status epilepticus F44.5 and
   T60.0X1A, myasthenia G73.1, focal epilepsy F44.5), and the criteria pack lists thyrotoxicosis as
   an ALS mimic. The case tests the condition's central skill (not calling ALS without Gold Coast).
   An answer naming thyrotoxicosis scores as correct even if it also mentions ALS (token matching
   cannot penalise that; the prohibitions record it for review). Codes: E05.90 primary, E05.9,
   E05.00 and T38.1X5A accepted. Data fix: levothyroxine 100 -> 150 mcg daily, because the verifier
   rightly noted that 100 mcg is not an over-replacement dose and the label must be derivable.
2. **Brief item: credit "Graves disease" in P02?** Decision: yes. TSI is still 180% after radioiodine,
   so residual Graves activity cannot be excluded from the case data (the must already asks
   endocrinology to distinguish them); what the case scores is recognising thyroid hormone excess
   as the reversible mimic. Added `hyperthyroidism`, `graves disease`, `graves hyperthyroidism`
   and E05.00 to the ALS-scoped E05.90 entry of `diagnosis_synonyms.yaml`; applied.
3. **Q2: ALS-P08 label and code.** Decision: recode `icd_codes[0]` G12.21 -> Z15.89 (genetic
   susceptibility), keep `accepted[0]` "Suspected early ALS in a SOD1 A4V pathogenic-variant
   carrier, Gold Coast criteria not yet met". Reason: the data do not meet Gold Coast (complex
   fasciculations without definite denervation or chronic change, no Hoffman or Babinski), and
   with the G12.21 synonyms a plain "ALS" answer, the overcall the case is built to catch, scored
   as fully correct. New entry Z15.89 scoped to ALS-P08 credits only cautious answers ("suspected
   ALS", "prodromal ALS", "possible ALS", "suspected motor neuron disease", "mild motor
   impairment"); G12.21 synonyms pruned. Changed `accepted`/`icd_codes` logged in ALS-P08.
4. **Q3: literature criterion removed in all 30.** Confirmed by scan (no criterion, follow-up or
   initial literature output in any ALS case), per ruling 5. No change.
5. **Q4: MIP/NIF -60 cmH2O for both sexes.** Keep, stated in the pack as a deliberate single
   cut-off: it is the AAN 2009 marker that prompts NIV discussion, not a sex-specific normal
   limit. S11 (man, NIF -52) is weaker than -60 under either reading, so no case changes.
6. **Q5: core work-up in `initial_tool_outputs`.** Keep. The harness serves initial outputs only
   when the agent orders the tool, so nothing is given upfront; the display order is CENTRAL 1.
7. **Q6: drug-interaction check required only in ALS-M06.** Agree (ruling 6): methotrexate adds
   hepatotoxicity and changes monitoring; alcohol (M03) and tamoxifen (M04, CYP3A4/2D6, no
   CYP1A2 interaction) do not change riluzole management, so recommended. No change.
8. **Q7: genetic panel in familial cases whose musts depend on the result.** Decision: required in
   ALS-P02, P08, P09 and S10 (each has a positive result that the label or the counselling musts
   rely on); in P02 and P08 it is also in `stop_rule.required_before_assessment`, because the label
   names the genotype. Sequence constraint EMG before genetics already exists. Other familial or
   sporadic cases unchanged (recommended / optional, Roggenbuck 2023: offered to all with ALS).
9. **Q8: `analyze_csf` as waste in the 25 non-CSF cases.** Decision: no. An unindicated LP is
   already penalised by the stop rule (`max_additional_actions` 0); a waste item for a tool that
   five cases of the same condition legitimately order would teach a blanket rule that EFNS 2012
   does not make (CSF in atypical presentations). Pack section 3 records it.
10. **Q9 / brief item: ALS-P01 riluzole deferred.** Decision: start now. The case meets Gold Coast
    (progressive weakness; UMN signs and clinical plus EMG LMN dysfunction in the cervical region),
    and EAN 2024 recommends riluzole for people with ALS without waiting for spread. Label now
    "Amyotrophic lateral sclerosis (ALS), early limb-onset, Gold Coast criteria met (possible ALS
    by Awaji criteria)" (G12.21 kept); riluzole must replaced by the canonical MUST-RILUZOLE; the
    diagnosis must now makes the diagnosis; the repeat EMG must became "review at 3 months, repeat
    EMG if needed to document spread" (a future study cannot be a criterion); DI check optional ->
    recommended; two key-evidence items reworded. Same repeat-EMG question in P08: the must stays,
    since there ALS is not established.
11. **Q10: LMN region rule in MUST-DX and K-GC.** Confirmed: it is the Gold Coast / Awaji rule
    already written in the pack section 1. No change.

### Case-level judgement calls

12. **M07 label.** Drop "progressing to definite": UMN plus LMN in cervical and lumbosacral regions,
    LMN only in bulbar, is Awaji "probable", and no study documents progression. New `accepted[0]`
    "Amyotrophic lateral sclerosis (ALS), limb-onset, probable ALS by Awaji criteria".
13. **Musts and prohibitions added beyond the plan** (M05 falls, S08 INR; P06 rituximab, P07 PPS
    anchoring, P09 FTD anchoring, S06 diabetic neuropathy): keep all; each is case-specific and
    correct.
14. **Musts possibly missing.** Added: statin review for CK 5.3x ULN on atorvastatin (pause and
    recheck CK in 2 to 6 weeks) in M02, S01 and S08 (one class); cognitive and behavioural screen
    (ECAS) and pseudobulbar affect in M01, M03 and RS11 (every ALS case that documents the affect;
    EAN 2024, NICE NG42); oncology liaison in M04; low alcohol in RM11 (as M03 already has); bulbar
    monitoring in S05 (EMG bulbar denervation without symptoms). Declined: M03 apixaban
    interruption around gastrostomy (gastrostomy is only discussed; peri-procedural anticoagulation
    is planned at placement); P04 liquid riluzole (no bulbar involvement).
15. **Changed stored values** (M02/M05 sural, P03 partial block history, S10 NCS and myopathy
    differential, S11 additions, S06/S07 MUP data): accepted; each made a report support its own
    impression.
16. **M08 respiratory** ("reduced" with FVC 78%, SNIP 60 at the women's limit): keep.
17. **RM11 and P09 EMG chronic change only in hand muscles:** keep; Gold Coast is met through UMN plus
    LMN in the cervical region, so no value is invented.
18. **P03 repeat anti-GM1 on IVIG:** keep. Passive transfer from IVIG can cause false positives, not
    false negatives, so a negative repeat is interpretable; the case does not rely on it.
19. **P05 HIV values in the HPI:** removed (prior viral load and CD4 numbers) because the current
    values are scored through the labs criterion; the HPI keeps adherence and clinic follow-up.
20. **P07 conus and ventral-root wording, earlier EMG confined to the left leg:** accept.
21. **Avoided actions.** S11: amyloid PET and DaTscan added as waste; FDG-PET left out (cancer
    history makes the request arguable). P09: ECG not added (quetiapine plus sertraline make a
    baseline QTc defensible).
22. **Thin HPIs S03, S04, S05:** no change; MRC grades and signs are in the examination, which is
    where the agent reads them.
23. **S09 "hypoglossal nuclei T2 signal":** deleted from the brain MRI findings and impression (not an
    established MRI sign of ALS).
24. **M01 UBQLN2 and VCP:** keep (extra negative genes are harmless and realistic for a broader panel).
25. **Repeated template values (ESR, CRP, B12, folate, CK):** keep; plausible and within range, not an
    error. Later variation is cosmetic.
26. **Spelling (British canonical text vs American reports):** keep; cosmetic.

### Auditor flags and brief extras

27. **Waste-action citation (CENTRAL 8).** `[AAN_2009]` -> `[EFNS_ALS_2012]` on every waste avoided
    action in all 30 cases: EFNS 2012 covers the diagnostic investigations, AAN 2009 Part 1 covers
    riluzole, nutrition and respiratory therapy. Pack section 3 updated.
28. **Pre-round em dashes in P01 and P04 EMG text:** replaced in the stored EMG reports (P01, P04);
    pre-round em dashes in patient blocks left (churn only).
29. **"Reference to confirm" entries in `criteria_packs/ALS.md`:** none present. The citations used
    in the cases were checked; `[AAN_2009]` now carries its full Part 1 title and `[EAN_ALS_2024]`
    the full title and issue.
30. **`conditions.yaml` ALS block (ruling 4).** Genetic panel moved from `interpret_labs` to
    `order_specialized_test` (`genetic_panel:ALS`); the MDT-clinic follow-up removed (management is a
    must); the 3-month repeat-EMG follow-up removed (a future result cannot be served); CSF NfL
    follow-up removed (not routine, EFNS 2012); respiratory follow-up described as staging; riluzole
    interaction follow-up added. Also corrected two generator lines that contradicted the pack: the
    Awaji fasciculation rule and the CK band.

## Files changed

- Cases: all 30 ALS cases (waste citations); substantive edits in M01, M02, M03, M04, M07, P01, P02,
  P04, P05, P08, P09, RM11, RS11, S01, S02, S05, S08, S09, S10, S11.
- `agent-platform/config/policies/diagnosis_synonyms.yaml`: E05.90 entry widened; new Z15.89 entry
  scoped to ALS-P08. Applied with `apply_diagnosis_synonyms.py --prune --conditions als`.
- `dataset-generation/criteria_packs/ALS.md`, `dataset-generation/config/conditions.yaml` (ALS block).

## Still for Andrea

Nothing blocks. Two decisions change scoring, so Andrea may want to check them: ALS-P08 now
rejects a plain "ALS" answer (Z15.89), and ALS-P02 accepts "Graves disease".

## CENTRAL

- None new. Earlier CENTRAL 1 (UI order), 4 (lab analyte matching, HIV viral load / CD4 vocabulary),
  6 (fallback literature text), 7 (banned-string test rows) and 9 (metadata revision text) stay open
  as listed in `ALS-summary.md`; 2, 3, 5 and 8 are done.
