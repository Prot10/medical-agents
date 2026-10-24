# FEPI-TEMP: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Sources:

- the plan, `plans/FEPI-TEMP.md` (classes A to V, per-case section 4, CENTRAL 1 to 10);
- the 30 case logs, `logs/FEPI-TEMP-*.md`. There is no reviewer notes file: R1 and R2 never
  reviewed this condition in a notes round. Every log has a worker table and an adversarial
  verifier section;
- scripted checks over the 30 case files: M01 to M05, P01 to P05, RM01 to RM04, RP01 to RP05,
  RS01 to RS05, S01 to S06.

All 30 cases are `draft`. The auditor did three reads in full:

- every literature and drug-interaction output of the condition;
- the cases the verifiers changed most: P02, RP01, RP02, RP04, RP05, RS04 and RS05;
- P02 and RS02, for the laboratory moves.

Each of the 30 logs now ends with a "## Condition audit" section listing the audit's edits and why.

## Final state

**Check results.**

- `perfect_agent.py` on all 30 ids: 30/30 pass, with no "same stored report" warning. The verbose
  `<- ?` markers come from the cosmetic `_source` comparison (CENTRAL 12).
- `case_io.py check` on all 30 ids: schema OK and synonym guard OK for every case. The suite has
  1 failure, `test_guidance_claims`, which is expected (CENTRAL 8); 3332 tests pass and no failure
  names a FEPI-TEMP case.
- `test_case_guards.py -k FEPI-TEMP`: 60 passed. Run directly on the 30 cases, the discriminator,
  leak, banned-string and hijacked-index helpers return nothing.

**Uniformity checks (scripted, clean after the audit fixes):**

- **Canonical facts (plan 1.2).**
  - Definitions: ILAE 2014 definition, 2017 classification, Glauser 2013 levels (lamotrigine
    Level A only in the elderly, everywhere it appears), ACNS 2021 frequency terms.
  - Treatment: valproate under 55 (MHRA 2024), topiramate pregnancy prevention, the contraceptive
    and inducer interactions.
  - HLA-B*15:02: the must is present in exactly M02, M04, M05, P04, RS05, S04 and S06.
  - Prolactin appears only in P05.
  - Driving and SUDEP musts follow plan 3.L. They are absent only where the case says otherwise:
    RM03 and RS04 do not drive; M05 has no convulsion and no drug resistance; P02, P03 and RP01
    are not epilepsy.
  - Gadolinium appears only in lesion cases and P02, never in an HS case.
- **Tiers, pathway order, constraints, stop rules.**
  - Tiers and pathway order match plan 3.2 and section 4. Literature is always optional and last.
  - Hard MRI -> CSF constraints in P02, RP01 and RP03; RM03 has CT -> MRI. A soft MRI -> drug check
    constraint appears only where the drug check is required or recommended.
  - Every stop rule equals the required set, with `max_additional_actions` 1 for S cases and 2
    otherwise. No expected_evidence is empty.
- **Plan and PATTERNS defects.** No defect from the plan or PATTERNS.md survives:
  - no source outside plan 1.1;
  - no new dash;
  - no engineering wording left in criteria, labels or red herrings;
  - every ECG interval set is unique.
- **Left as is (cosmetic):**
  - the MRI -> drug check citation varies between `[ILAE_MRI_2019]` and `[NICE_NG217_2025]`;
  - the echo and Holter avoided actions take `{}` arguments in RM04 and RP05;
  - `fallback_tool_kinds.ct` reads "case_specific" in RS01 and RS02;
  - an empty `summary` in four drug outputs (RM03, RM04, RP01, RP02).

## Error classes and how each was fixed

### Plan classes A to V (workers and verifiers)

All applied uniformly; the audit found the stragglers listed under W to AB.

- **A, O. Literature.** Literature is optional at most and last in the pathway. Every source is
  real, from plan 1.1, and cited as `Author et al., Journal Year;Vol:pages | Title`. Glauser 2013
  replaces the non-existent "Glauser 2017". Leak guard clean.
- **B, C, D. Template tiers.**
  - Drug check: required only for a concrete interaction (P04, RM02, RP02, RS04, S04 and
    others, per section 4).
  - The shared MRI -> drug check constraint is kept only where the drug check is required or
    recommended. Stop rules are rebuilt.
- **E, F. Imaging.**
  - The MRI is ordered with `{protocol: epilepsy}`, except RP01 and RP03 `{contrast: true}`, P02
    `{}` and the RS02 harm avoidance on contrast.
  - Each case stores the dedicated study with the definite findings of fact 4.
  - Gadolinium lines are removed in HS cases.
- **G, H, L.** KCE, citations and rationales are rewritten per case. Musts and prohibitions
  follow the canonical texts: first-line ASM, valproate, contraception, HLA, driving, SUDEP,
  presurgical and lesional referral.
- **I, J, M.**
  - Avoided actions carry case rationales.
  - FDG-PET without a criterion is deleted and stays as waste (harm in RS02).
  - Prolactin is deleted everywhere except P05.
- **K, N, P.**
  - EEG limitations describe each recording and its own findings.
  - Lateralization claims follow fact 12.
  - Differentials are taken at assessment time, each naming its excluding finding.
- **Q, R, S, T, U, V.**
  - Discriminators: echo `TTE`; fallbacks are null where no single study fits.
  - Duplicate patients renamed.
  - Claims about absent outputs removed.
  - ECG optional, except P05 (required) and RP02 (recommended).
  - Volumetric arithmetic consistent: index (L - R)/(L + R), volumes unique.
  - Patient-block contradictions fixed.

### Classes found by this audit and fixed

- **W. Knowledge outputs that name the diagnosis (18 literature, 3 drug; 19 cases).**
  - **Cause.** MockServer serves an initial literature or drug output for any query or drug.
    With no initial output, any first call gets the first stored follow-up. Literature
    follow-ups whose trigger shares a generic token (epilepsy, temporal, seizure) take any
    generic query.
  - **Effect.** A literature search before imaging returned the lesion or diagnosis:
    - lesion: DNET (S02, S03, S06), cavernoma (M05), FCD (M04, P01; and RP04's FCD IIIa),
      ganglioglioma (RM04), ECCL (RM03), encephalocele (RP05);
    - diagnosis: LGI1 encephalitis (P02, initial block), PNES (P03, initial block),
      neurocysticercosis (RS02), HSV encephalitis (RP01), the concurrent PE (RP02, two
      follow-ups), subtle HS with volumetry (M03), HS (RM01, S01).
    Any first drug check named the diagnosis-specific treatment:
    - methylprednisolone and IVIG in P02 (initial block);
    - acyclovir in RP01;
    - DOACs in RP02.
  - **Fix (the SYNC-CARD class P and Q pattern).**
    - Every case now has the same neutral `initial_tool_outputs.literature_search.general` block,
      with five sources from plan 1.1 and no case content: the definition, classification,
      HARNESS-MRI, NICE first-line ASM and Kwan 2010.
    - Lesion-specific follow-ups keep their content, with triggers renamed to the lesion's own
      words only, so they answer only a query that already names it. This was done in M03, M04,
      M05, RM03, RM04, RP01, RP02, RP05, RS02, S02, S03 and S06.
    - The initial blocks of P02 and P03 became the last follow-up.
    - Where the generic content itself named the case finding, the content was edited:
      - P01: FCD classification removed;
      - RM01: HS classification removed;
      - RP04: query "HS and temporopolar abnormality" and the FCD IIIa result removed;
      - S01: query "mesial temporal sclerosis" removed.
    - P02, RP01 and RP02 now have an initial drug block that reviews the current medicines. The
      steroid, acyclovir and anticoagulant follow-ups answer only a check naming those drugs.
    - Probed in MockServer:
      - generic queries and ASM checks get the neutral blocks;
      - "DNET", "LGI1", "encephalocele", "apixaban" and "methylprednisolone" get the case
        follow-ups;
      - required orders are unchanged.
- **X. Second-tier labs served with the first-line labs (P02, RS02).**
  - P02: the serum autoimmune encephalitis panel (LGI1 IgG positive 1:320) moved to an
    `interpret_labs` follow-up, `request_autoimmune_encephalitis_lgi1_caspr2_antibodies`, placed
    after the video-EEG. LGI1 was also removed from the initial interpretation and summary.
    - Probed: `[autoimmune_encephalitis, sodium]` and the BMP and CMP alternatives still receive
      both panels.
    - `[BMP, CBC]` no longer receives LGI1.
  - RS02: the infectious panel (cysticercosis IgG, HIV, RPR, HBsAg, HCV, QuantiFERON) moved to a
    follow-up, which comes first in the pathway. The red herring path is now
    `followup_outputs[0].output.panels.Infectious_Workup[0]`.
  - Kept, by design: RM04 iron studies (comorbidity red herring); RP03 and RM02 thyroid; RM03 CK,
    lactate and TSH; P05 prolactin.
- **Y. Copied numbers and text.**
  - M02, RM04 and S05 shared one ECG: 76/min, PR 154, QRS 86, QTc 416. Now:

    | case | rate | PR | QRS | QTc | triage HR |
    | --- | --- | --- | --- | --- | --- |
    | M02 | 72/min | 158 | 80 | 434 | 73 |
    | RM04 | 82/min | 146 | 94 | 410 | 88 |
    | S05 | 86/min | 140 | 90 | 414 | 88 |

    The ECG criteria are updated to match.
  - Remaining shared sentences are library-style normals (echo, Holter, CT), canonical technique
    lines and common lab values, which are acceptable.
- **Z. EEG terms.**
  - Spike-range durations given for sharp waves were corrected:
    - M04: 50-70 ms, now 80-120 ms;
    - M05: 40-70 ms, now 80-130 ms;
    - S05 (sharp component): 35-60 ms, now 80-120 ms.
  - "Frequent" or "rare" qualifiers that contradicted the stated rates now read "occasional" in
    the outputs, criteria and KCE. ACNS 2021: frequent is at least 1 per minute, occasional at
    least 1 per hour, rare under 1 per hour.

    | case | stated rate | old term |
    | --- | --- | --- |
    | M05 | 8-35/h | frequent |
    | P04 | 12/h | frequent |
    | P04 | 2/h | rare |
    | P05 | 8-22/h | frequent |
    | RM01 | 10/h | frequent |
    | P01 | 2-8/h | rare |
    | RP02 | 1-2/h | rare |

  - M02 and M03 ambiguous "sharp transients" and "sharply contoured" waves of 50-80 ms are kept:
    these are not called sharp waves.
- **AA. Differential ICD codes (9 in 8 cases).** The dataset uses ICD-10-CM.

  | case | entry | old code | new code | why |
  | --- | --- | --- | --- | --- |
  | M04 | | D43.2 | D43.0 | the lesion is supratentorial |
  | RM02 | SEGA | D33.0 | D43.0 | ICD-O 9384/1 |
  | RM03 | NCSE | G41.8 | G40.201 | G41 is WHO ICD-10, absent from CM |
  | RP02 | JME | G40.309 | G40.B09 | |
  | S01 | JME | G40.319 | G40.B09 | |
  | S04 | JME | G40.319 | G40.B09 | |
  | RS01 | LGS | G40.812 | G40.814 | drug-resistant |
  | RS02 | tuberculoma | A17.8 | A17.81 | |
  | RS02 | hyponatremia | G93.49 | E87.1 | |

- **AB. Engineering text.** 39 rationale and label edits in 22 cases:
  - rationales starting "Optional:", "Optional here:" or "Optional baseline";
  - "Optional background;", now "Background only;";
  - "so the test/check is optional";
  - labels starting "Optional" (RP05 x3, RS01 to RS05);
  - S06 "A naive agent".

  The P02 and P03 fallback literature and drug placeholders ("(agent not specified ...)", "No
  directly applicable evidence") were unreachable behind initial outputs and are deleted.
  The literature expected_evidence "...; not required for the diagnosis." is plan text and is
  kept.

## Counts

- **Own findings fixed:** 9 classes and 87 edits:

  | class | edits |
  | --- | --- |
  | W | 21 knowledge outputs |
  | X | 2 lab moves |
  | Y | 3 ECGs |
  | Z | 3 durations, 6 frequency cases |
  | AA | 9 codes |
  | AB | 39 text edits |
  | placeholders | 2 cases |
  | uniform general literature block | 30 cases |

- **Flagged, not fixed:**
  - 4 CENTRAL items new from the audit (9, 11, 15, 16);
  - 4 cosmetic non-uniformities (Final state).
- **Cases changed by the audit:**
  - 30, all through the uniform general literature block;
  - 29 with further changes, M01 being the exception.
- **Logs updated:** 30.

## CENTRAL requests (consolidated)

1. **Criteria pack `[ILAE_drug_2017]`.** It cites the non-existent "Glauser 2017 Epilepsia
   58:1235-1268". Correct it to Glauser T et al., Epilepsia 2013;54:551-563, and align the pack
   hierarchy with rulings 5 and 6 and facts 3 and 11 (plan CENTRAL 1).
2. **Pack allow-list.** Add the starred plan 1.1 keys used across the cases (`case_io check`
   accepts them today):
   - guideline keys: `NICE_NG217_2025`, `ILAE_MRI_2019`, `IFCN_ILAE_EEG_2023`, `SANAD2_2021`,
     `ILAE_def_2014`, `Lateralization_2005`, `ILAE_FCD_2011`, `ILAE_PNES_2013`, `AAN_SUDEP_2017`,
     `AAN_2015`, `CPIC_2018`, `Sabers_2003`, `EURAP_2018`, `MHRA_VPA_2024`;
   - topic keys: `Graus_2016`, `IDSA_enc_2008`, `ABN_enc_2012`, `ACNS_2021`, `ESC_PE_2019`,
     `EHRA_DOAC_2021`, `ASCO_irAE_2018`, `TSC_2021`, `Cavernoma_2017`, `Blumcke_2017`,
     `Encephalocele_2015`.
3. **Label RP01.** Acute symptomatic NCSE in HSV-1 encephalitis is not epilepsy (Beghi 2010).
   - accepted[0]: "Nonconvulsive focal status epilepticus of temporal origin due to HSV-1
     encephalitis in a post-radiotherapy patient (acute symptomatic, not epilepsy)".
   - Codes: `B00.4` first. The plan's `G41.8` is not an ICD-10-CM code; use `G40.901` as the
     ICD-10-CM status epilepticus code.
   - Synonyms: HSV encephalitis, herpes simplex encephalitis, nonconvulsive status epilepticus,
     acute symptomatic seizures. Remove the inherited epilepsy synonyms and G40.2x codes from
     this case.
4. **Label P01.** "drug-resistant" is wrong: no ASM was ever given.
   - accepted[0]: "Focal epilepsy of right temporal lobe origin with suspected focal cortical
     dysplasia on 3T epilepsy-protocol MRI, misdiagnosed as refractory panic disorder".
   - `icd_codes[0]`: `G40.209`.
   - Then delete the resolved AUDIT-FLAG in `metadata.case_body_concerns`.
5. **Label RP04.** accepted[0] becomes "left hippocampal sclerosis with associated left
   temporopolar cortical abnormality (suspected FCD type IIIa)". HS with an associated cortical
   lesion is FCD IIIa, a histological diagnosis, not dual pathology.
6. **Label RM04** (verifier). accepted[0] becomes "Focal epilepsy of left temporal lobe origin
   (lateral neocortical TLE with auditory aura) due to a left superior temporal gyrus low-grade
   epilepsy-associated tumor (presumed ganglioglioma, CNS WHO grade 1)". There is no tissue, and
   the old label uses the pre-2021 roman grade.
7. **Synonyms (`diagnosis_synonyms.yaml`).**
   - "mesial temporal lobe epilepsy" and "mesial temporal sclerosis epilepsy" are wrong in M04,
     M05, P01, P04, RM04, RP05, S02, S03 and S06 (no HS, or a lateral or neocortical focus).
     Make them per case or per sub-entity.
   - Drop the idiopathic `G40.009` and `G40.019` from the structural TLE list.
   - Use `G40.219` (intractable) only in P04, RP04, RS01 and RS04.
8. **`test_guidance_claims`.** The prolactin claim of the July reply is true after this round:
   only P05 keeps a timed level. Update the claim text and the test.
9. **MockServer knowledge tools** (new). Literature and drug outputs are any-query by design. A
   case is safe only if it adds a neutral initial block and gives lesion-specific triggers. The
   SYNC-CARD and FEPI-TEMP audits found this in 43 cases between them.
   - Proposal: route `search_medical_literature` and `check_drug_interactions` by query and drug
     tokens, answering an unmatched call with a library-level general block.
   - Add a guard that flags a knowledge follow-up with only generic trigger tokens whose text
     contains the diagnosis label.
10. **`analyze_eeg` routing by `eeg_type`** (verifiers P02, RP04, RS01).
    - Today a routine or sleep-deprived order receives the stored video-EEG (P02, RP04).
    - RS01 stores no routine EEG, so a routine order gets the library normal although he has
      frequent left temporal discharges.
    - Proposal: add `analyze_eeg: eeg_type` to the discriminators, with the library answering an
      unstored type. RS01 then needs a stored routine EEG; keep it a CENTRAL item until the
      router exists.
11. **Labs vocabulary** (new). `costs.yaml` has no cysticercosis serology and no
    interferon-gamma release assay. RS02's moved panel is reachable today through HIV, syphilis
    and hepatitis orders only. Add `cysticercosis_serology` and `IGRA` (QuantiFERON) with the
    `tool_io.py` mirror.
12. **Cosmetic tooling and text.**
    - `perfect_agent.py` `_source`: the `<- ?` marker comes from the `exclude_none` comparison.
    - Plan class Q text: `BodyImagingReport` has no `study` field; the router reads `region`
      plus `modality` (RP02 verifier).
    - `MRIReport` has no technique field; the technique is the first `additional_observations`
      line (M01).
13. **`DISCRIMINATOR_CONDITIONS`.** Add `FEPI-TEMP`: the discriminator helper returns nothing
    on all 30 cases.
14. **Banned strings for FEPI-TEMP.** None fire today:
    - `Epilepsia 2017;58:1235`;
    - `Category X`;
    - oxcarbazepine "Level A";
    - lamotrigine "Level A" unless "elderly";
    - prolactin outside P05, which needs a per-case exemption or a case-scoped row.
15. **Dataset-wide surnames** (verifiers RP05, RM03).
    - Shared names: Reyes (RP05, FND-RM03, SE-S02), Chen (7 cases), Tanaka (3), Delgado (3),
      Ramirez (3), Johnson (2).
    - Khatri was shared with SYNC-CARD-RM03 with the same occupation; RM03 was renamed.
    - Run one name pass across all conditions. Common surnames are not errors in themselves; the
      problem is identical name plus occupation templates.
16. **Label RM02** (new). accepted[0] contains an em dash ("hippocampal sclerosis — dual
    pathology"); replace it with a comma.
17. **Vocabulary HLA** (plan CENTRAL 10). There is no HLA genotype term, and none is needed; it
    stays a must. No action.

## Open questions

None for Andrea. Each judgment call was decided per the ruling "decide in the way best for
dataset quality":

- **One identical general literature block in 30 cases.** The alternative was rewriting 18
  lesion-specific outputs into generic ones. The block keeps each case's lesion literature for an
  agent that already suspects the lesion, and stops the free answer for one that does not. The
  shared text is a knowledge-tool answer, like the library normals, not patient data.
- **RS02 infectious panel.** It moved out of the first-line labs even though the cysticercosis
  term is not yet orderable (CENTRAL 11). Serving an unasked second-tier result is worse than a
  red herring that is reachable only through the HIV, syphilis and hepatitis orders until the
  vocabulary lands.
- **P02, RP01 and RP02 initial drug blocks.** These are medicine reviews, a change against the
  plan's "delete the initial blocks". The plan deleted empty blocks; these blocks carry real
  interactions of the current medicines and stop any first drug check from naming the
  immunotherapy, the antiviral or the anticoagulant. The required and recommended drug criteria
  still match any check.
- **ACNS qualifiers.** The term was changed and the counts kept, rather than raising counts to
  fit "frequent": the counts are the data, and each impression and criterion now uses the term
  the counts support.
