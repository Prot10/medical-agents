# FEPI-TEMP: close-out decisions (24 October 2026)

Close-out of FEPI-TEMP (`focal_epilepsy_temporal`) under `CLOSEOUT_BRIEF.md` (Andrea, 24 Oct 2026:
decide every open point for the quality of the dataset). Inputs: `plans/FEPI-TEMP.md` (sections 1
to 5), `plans/FEPI-TEMP-summary.md` (CENTRAL 1 to 17, open questions, auditor flags). There is no
reviewer notes file for FEPI-TEMP. Every entry gives the decision, the reason and what changed.
Per-case details are in the "Close-out (24 Oct 2026)" section of each `logs/FEPI-TEMP-*.md` (all 30,
since the synonym change touches every case). Nothing is committed.

Sources checked on 24 Oct 2026:
- Beniczky S, Trinka E, Wirrell E, et al. Updated classification of epileptic seizures: position
  paper of the ILAE. Epilepsia 2025, doi 10.1111/epi.18338 (ILAE page and press summary: four
  classes kept, "awareness" becomes "consciousness", motor/non-motor replaced by observable and
  non-observable, 21 seizure types).
- NICE NG217: published April 2022; January 2025 safety update of the valproate (and topiramate)
  recommendations after the MHRA 2023-2024 measures (NICE methods document, January 2025).
- Schneider BJ et al. Management of immune-related adverse events in patients treated with immune
  checkpoint inhibitor therapy: ASCO guideline update. J Clin Oncol 2021;39(36):4073-4126, PMID
  34724392 (supersedes Brahmer 2018).
- ESC acute PE guideline: the 2019 edition is still the current ESC document; a 2026 AHA/ACC PE
  guideline exists (Feb 2026) and does not change RP02 (non-high-risk PE, DOAC).
- Glauser T et al. Epilepsia 2013;54:551-563 (the real ILAE monotherapy review; "Glauser 2017,
  Epilepsia 58:1235-1268" does not exist).

## CENTRAL items of the summary

**C1. Pack `[ILAE_drug_2017]` and hierarchy.** Done. `criteria_packs/FEPI-TEMP.md` rewritten from
the plan's facts and the applied tiers: codes (default G40.209, G40.219 only for Kwan 2010 drug
resistance, mimic codes, no G41 in ICD-10-CM), diagnostic criteria (ILAE 2014 definition, acute
symptomatic seizures, HS on MRI, dual pathology vs FCD IIIa, presumed tumor names, lateralization),
the work-up hierarchy with the counts of the 30 cases (MRI 29 required, staged EEG, labs and ECG
optional unless indicated, CSF 2 required and 1 recommended, PET and neuropsychology presurgical),
literature and drug check out of the required pathway, prolactin only with the 10-20 minute timing,
CT indicated in the emergencies of fact 3, the corrected "non-inducing ASM with a tumor" rule,
sequence constraints, musts. Since no case cites `[ILAE_drug_2017]`, the key is renamed in the pack
to `[ILAE_drug_2013]` (Glauser 2013) and the old key is listed as non-existent.

**C2. Allow-list.** Done. Every key the 30 cases cite (35) is in section 9 with a full reference;
a script check finds none missing. Added the plan keys the pack text uses (ILAE_ASS_2010,
AAN_prolactin_2005, ILAE_HS_2013, Irani_2011, Salzburg_2015, Wiebe_2001, ERSET_2012, AAN_2015,
ESC_syncope_2018, Garcia_2014, EXIST3_2016, Ray_2016), ILAE_2025 and ASCO_irAE_2021. Superseded:
ASCO_irAE_2018 (RP03 recited to the 2021 update); ILAE_2017 noted as updated by ILAE_2025 for seizure
types (cases keep the 2017 wording, see D6); ILAE_FCD_2011 noted as updated by Najm 2022 (types I to
III unchanged).

**C3. Label RP01.** Applied with a different wording: "HSV-1 encephalitis with acute symptomatic
nonconvulsive focal status epilepticus of right temporal onset, after skull-base tumor resection and
radiochemotherapy", icd_codes[0] B00.4. Reasons: the label leads with the entity of the primary code;
"(acute symptomatic, not epilepsy)" is an exclusion clause, which the FND close-out removed from
positive labels; the onset is right temporal on the continuous EEG; the patient had resection and
radiochemotherapy, not radiotherapy alone. Second code: none. G41.8 is not ICD-10-CM, and G40.901 is
not added because the scorer accepts a diagnosis on any accepted code alone, so an epilepsy answer
coded G40.901 would score in the case built to test exactly that error. Synonyms: see S2.

**C4. Label P01.** Applied as requested; icd_codes[0] G40.219 -> G40.209; the AUDIT-FLAG removed from
`metadata.case_body_concerns`.

**C5. Label RP04.** Applied: "Drug-resistant focal epilepsy of left temporal lobe origin with left
hippocampal sclerosis and an associated left temporopolar cortical abnormality (suspected FCD type
IIIa)" (fact 13, Blumcke 2011). Code unchanged.

**C6. Label RM04.** Applied as requested ("...due to a left superior temporal gyrus low-grade
epilepsy-associated tumor (presumed ganglioglioma, CNS WHO grade 1)"); the red herring's "WHO grade
I" also became "CNS WHO grade 1".

**C7. Synonyms.** Applied, with three decisions beyond the request (S1 to S5 below).

**C8. Guidance claims.** Done. `build_condition_tool_guidance.py` FEPI responses rewritten for EEG,
MRI, labs (with the prolactin statement, now true: only P05), ECG (the old "required in 21" was the
opposite of Reviewer 1's request; now optional 19, required P05, recommended RP02), echo and rhythm
monitoring (no criterion; waste in 27 and 28; the old "authored reports removed" was false, normal
fallbacks exist). YAML regenerated with `--write` (only the six FEPI lines changed).
`test_guidance_claims.py` FEPI rows replaced by 12 rows that check every number of those responses;
all FEPI claims pass (the remaining failures are PD claims, its close-out).

**C9, C10, C11, C12.** Code or vocabulary: not mine, listed under CENTRAL below.

**C13. Discriminators.** FEPI-TEMP added to `DISCRIMINATOR_CONDITIONS`; the helper returned nothing
on all 30 cases, `test_routed_outputs_name_their_study` passes.

**C14. Banned strings.** Added five FEPI-TEMP rows to `BANNED` in `test_case_guards.py`: the
non-existent Glauser 2017 (author-year or the 2017;58:1235 locator), "Category X", oxcarbazepine
"Level A", lamotrigine "Level A" unless the sentence says elderly, and prolactin outside P05. The
last needed a small `except_cases` field on `Banned` (exempts a case where the phrase is right) and
an `unless` for the "prolactin removed" revision notes in metadata. `test_banned_table_rows_fire`
covers each row. None fires on the 30 cases.

**C15. Cross-condition surname pass.** Not mine: CENTRAL below.

**C16. Label RM02.** Em dash replaced by a comma. Pre-existing dashes elsewhere in old prose of 15
cases were left (correct prose, not new text).

**C17. HLA vocabulary.** No action, as the summary says: HLA-B*15:02 stays a must or prohibition.

## Synonym decisions (`diagnosis_synonyms.yaml`, condition enum `focal_epilepsy_temporal`)

Applied with `apply_diagnosis_synonyms.py --prune --conditions focal_epilepsy_temporal` (30 cases);
`--check` clean over all 600.

**S1. The G40 entry is split** (conditions-scoped to FEPI-TEMP, so a future G40 case elsewhere does
not inherit temporal labels):
- `G40` (27 epilepsy cases): focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe;
  codes G40.2, G40.1, G40.9.
- `G40+not-intractable` (23): G40.209, G40.109, G40.909. `G40+intractable` (P04, RP04, RS01, RS04):
  G40.219, G40.119, G40.919. A "not intractable" code no longer scores in a drug-resistant case and
  vice versa. G40.009 and G40.019 (idiopathic) dropped everywhere.
- `G40+mesial` (21): mesial temporal lobe epilepsy, MTLE (added: "right MTLE-HS" matched nothing
  before, because `mtle` is not the token `tle`).
- `G40+hs` (16 cases with HS on MRI): mesial temporal sclerosis epilepsy.

**S2. Where the mesial labels go (partly differs from the summary).** The summary called the mesial
labels wrong in M04, M05, P01, P04, RM04, RP05, S02, S03, S06. Decided per case from the stored MRI
and semiology:
- No mesial label: M04 (posterior superior temporal FCD), RM04 (superior temporal gyrus tumor,
  auditory aura), P01 (temporal pole FCD), RP05 (temporopolar encephalocele), S06 (inferior temporal
  gyrus DNET), P04 (MRI-negative, anterior temporal F8/T4 onset, mesial and lateral PET).
- "mesial temporal lobe epilepsy" kept, "mesial temporal sclerosis epilepsy" removed: M05 (cavernoma
  at the amygdala-hippocampal junction), S02 and S03 (DNET in the amygdala and anterior hippocampus;
  S03's own label says "right mesial temporal lobe origin"). MTLE denotes seizure onset in mesial
  structures, of any cause; the sclerosis label needs sclerosis.
- RP02 (MRI-negative, label "mesial TLE", epigastric and deja vu aura) and RP03 (metastasis "mesial
  and lateral" with edema into the hippocampal formation, mesial semiology): mesial label kept,
  sclerosis label removed (no HS). The summary did not list these two; the sclerosis label was wrong
  there too.

**S3. Seizure-type labels retired** ("focal seizures", "focal onset seizures", "focal impaired
awareness seizures", added to `RETIRED`). Reason: their tokens occur in "acute symptomatic focal
seizures due to hypoglycemia" (RS05's provoked-seizure question), in "functional seizures mimicking
focal impaired awareness seizures" (the F44.5 hazard, both directions), and they name a seizure type,
not the epilepsy the case scores (ILAE 2014; RP01 shows the distinction matters). A correct answer
names epilepsy, TLE or MTLE. No other case in the dataset held these labels.

**S4. RP01 synonyms.** New `B00.4` entry, scoped to RP01: HSV encephalitis, HSV-1 encephalitis,
herpes simplex encephalitis, herpes simplex virus encephalitis, HSE. Declined from the summary: plain
"nonconvulsive status epilepticus" and "acute symptomatic seizures" (each credits "temporal lobe
epilepsy with NCSE" or a metabolic seizure answer, i.e. the error the mimic tests; acyclovir depends
on naming the encephalitis, and the assessment carries no scalar weight). Not added: "herpes
encephalitis", "herpesviral encephalitis" (tokens of a VZV answer, a differential of the case).
"HSV encephalitis" is kept although an "HSV-2 encephalitis" answer contains its tokens: in adults
HSE is HSV-1 in about 90% and management is identical.

**S5. P02 synonyms (new, from the scan).** The generic G04.81 labels (autoimmune encephalitis,
antibody mediated encephalitis, autoimmune limbic encephalitis) and codes G04.8, G04.90 credited
"anti-NMDA receptor autoimmune encephalitis" and "GAD65 autoimmune limbic encephalitis", both in the
case's differential. P02 joins the entry's `except_cases` (the NMDAR-ENC close-out did the same in
reverse) and gets `G04.81+lgi1`: LGI1 encephalitis, anti-LGI1 encephalitis, LGI1 antibody
encephalitis, LGI1 limbic encephalitis, leucine rich glioma inactivated 1 encephalitis.

**F44.5 token hazard (FND close-out CENTRAL 7), both ways.** P03 left the global F44.5 entry for
`F44.5+fepi`: "non-epileptic seizures" removed (tokens of "focal non-motor epileptic seizures"; P03
had it before), "nonepileptic seizures" added, F44.4 and F44.7 removed. Probed with
`DiagnosisCriterion.matches`: 8 functional-seizure answers (including "functional seizures mimicking
focal impaired awareness seizures", "PNES mimicking focal onset seizures") score in no FEPI epilepsy
case; 10 epilepsy answers and the codes G40.209, G40.219, G40.909, G40.901, G41.2, R56.9 score in no
FND case nor P03. One hazard remains outside FEPI: SE-P02 still gets "non-epileptic seizures" from
the global entry (SE is closed; CENTRAL below). Wrong answers checked for RP01 (TLE with NCSE, NCSE,
autoimmune encephalitis, VZV, radiation necrosis, G40.901, G41.2) and P02 (NMDAR, GAD65, CASPR2,
anti-Hu, seronegative, HSV, TLE) do not score; the expected right answers do.

## Open questions of the summary

The summary lists none for Andrea; it recorded four judgment calls already decided. Confirmed:
1. **One identical general literature block in 30 cases.** Kept: it is a knowledge-tool answer like a
   library normal, not patient data, and it stops a first query from returning the lesion.
2. **RS02 infectious panel out of the first-line labs.** Kept, with the cysticercosis serology and
   IGRA terms requested under CENTRAL.
3. **P02, RP01, RP02 initial drug blocks** (medicine reviews). Kept: they carry real interactions of
   the current medicines and keep the immunotherapy, antiviral and anticoagulant follow-ups behind a
   check that names those drugs.
4. **ACNS frequency terms changed, counts kept.** Kept: the counts are the data.

## Auditor flags ("left as is (cosmetic)")

- **MRI -> drug check citation varies.** Changed: the six constraints citing `[ILAE_MRI_2019]` (RM02,
  RP02, RP03, RP04, RS03, RS04) now cite `[NICE_NG217_2025]` like the others; the constraint is about
  the ASM choice. P02 (`[Graus_2016]`) and RP01 (`[IDSA_enc_2008]`) keep their context keys.
- **Echo and Holter avoided actions with `{}` arguments in RM04 and RP05.** Kept: `{}` makes any echo
  or monitor order waste, which is clinically right; the typed form in the other cases names the study
  an agent would order by mistake. Neither changes the perfect trace.
- **`fallback_tool_kinds.ct` "case_specific" in RS01 and RS02.** Kept: free-text metadata no code
  reads ("case_specific" is used in 9 other cases), and the CT fallbacks are correctly case-specific
  (hamartoma, calcified granulomas).
- **Empty `summary` in four drug follow-ups** (RM03, RM04, RP01, RP02). Filled with one report-voice
  sentence each, distinct from the criteria's expected evidence; leak guard clean.

## Other decisions

- **D1. RP03 citation.** `[ASCO_irAE_2018]` -> `[ASCO_irAE_2021]` (4 places): the 2021 update
  supersedes it; RP03 cites it for neurologic irAE assessment, unchanged in the update's scope.
- **D2. DNET labels (S02, S03, S06) and M04 FCD kept** without "presumed": the MRI features are
  characteristic (multicystic, bright FLAIR rim, inner-table scalloping; transmantle sign) and the
  labels state no grade. RM04 differs: its MRI explicitly leaves ganglioglioma versus DNET and asks
  for tissue, and the label claimed a grade.
- **D3. Dual pathology wording kept in RM01, RM02, RM03, RS01, RS02:** each lesion (gliosis, tuber,
  ECCL, hamartoma, granulomas) is separate from the hippocampus, which is the definition (fact 13).
- **D4. Generator block** (`conditions.yaml`, FEPI-TEMP only): the interim comment replaced by the
  round's rules; the seeded repeat "3T MRI epilepsy protocol" follow-up removed (it produced class F
  and the 3T musts); neuropsychology moved to `order_specialized_test` and FDG-PET to
  `order_advanced_imaging`, both limited to presurgical or lesional cases; AED levels only with a
  named question; MRI moderate findings now definite subtle HS or FCD (the "equivocal, could be
  artifact" seed contradicted labels resting on definite HS); difficulty presentations no longer
  carry MRI or EEG results (scored studies); prolactin timing rule; acute symptomatic seizures and
  LGI1 encephalitis added to the differential seeds; CSF and advanced imaging added to the optional
  modalities.
- **D5. Codes in the differential** (G40.219 in RP04's HS and bitemporal entries) left: the
  differential is unscored, and those alternatives would be intractable too.
- **D6. 2017 seizure terminology kept** in the cases; the 2025 ILAE update renames awareness as
  consciousness but keeps the structure, and rewriting 30 cases for it would be churn. The pack says
  so.

Checks: `perfect_agent.py -v` 30/30 pass with no "same stored report" warning; `case_io.py check` on
the 30: schema and synonym guard OK, the one suite failure is `test_guidance_claims` on PD claims;
`test_case_guards.py -k FEPI-TEMP-` 120 passed (whole file 1894); `apply_diagnosis_synonyms.py
--check --conditions focal_epilepsy_temporal` and `--check` clean. (`test_grpo_rollout.py` does not
collect without torch; unrelated.)

## For the physicians at re-review

- FEPI-TEMP was never physician-reviewed, and this round changed every case.
- Scoring changes: answers must name epilepsy, TLE or MTLE ("focal seizures" alone no longer scores);
  mesial labels only where the onset zone is mesial; RP01 now scores only an HSV encephalitis answer
  (B00.4), P02 only an LGI1 answer, P03 only a functional-seizure answer; P01 and RP01 recoded.
- RS02 MRI: the criterion `{protocol: epilepsy}` and the harmful avoided action `{contrast: true}`
  both match a contrast epilepsy-protocol order; that is intended (credited for the MRI, penalized
  for gadolinium at 33 weeks).

## Still for Andrea

Nothing blocking.

## CENTRAL (vocabulary, code, shared files; not edited here)

1. **`analyze_eeg` routing by `eeg_type`** (summary C10; also FND CENTRAL 1). A routine or
   sleep-deprived order receives the stored video-EEG in P02 and RP04; RS01 stores no routine EEG, so
   a routine order gets the library normal although he has frequent left temporal discharges. Add
   `eeg_type` to the MockServer discriminators (and to `EEGReport`), library answer for an unstored
   type; then RS01 needs a stored routine EEG.
2. **Knowledge-tool routing by query and drug** (C9). Route `search_medical_literature` and
   `check_drug_interactions` by query and drug tokens, answering an unmatched call with a library
   general block; add a guard that flags a knowledge follow-up with only generic trigger tokens whose
   text contains the diagnosis label. FEPI-TEMP is safe today only through the neutral initial blocks
   and lesion-specific triggers (19 cases).
3. **Labs vocabulary** (C11): `interpret_labs` panels `cysticercosis_serology` (serum cysticercosis
   IgG, EITB/ELISA) and `IGRA` (QuantiFERON), with costs, a library normal and the `tool_io.py`
   mirror. Needed by FEPI-TEMP-RS02, whose moved infectious panel is reachable today only through
   the HIV, syphilis and hepatitis orders; then add a recommended criterion naming them.
4. **Cross-condition surname pass** (C15): identical surnames with the same occupation template
   across conditions (Reyes: FEPI-TEMP-RP05, FND-RM03, SE-S02; Chen in 7 cases, Tanaka 3, Delgado 3,
   Ramirez 3, Johnson 2). One pass over all 600.
5. **Tooling text** (C12): `perfect_agent.py` `_source` prints `<- ?` from the `exclude_none`
   comparison; plan class Q says body imaging has a `study` field, but `BodyImagingReport` routes on
   `region` plus `modality`; `MRIReport` has no technique field (the technique is the first
   `additional_observations` line).
6. **Global `F44.5` entry**: SE-P02 still accepts "non-epileptic seizures" (and F44.4, F44.7); "focal
   non-motor epileptic seizures" scores there. For the SE owner: move SE-P02 to a scoped entry as
   FEPI-TEMP-P03 and FND did, then drop the global labels.
7. **ICD-10-CM vs WHO G41**: the dataset says it uses ICD-10-CM, but SE and HEP-ENC use G41.x primary
   codes, which exist only in WHO ICD-10 (CM codes status epilepticus inside G40, e.g. G40.901,
   G40.211). Decide one system before reporting code-based scores.
8. **Scorer**: negation ("PNES rather than temporal lobe epilepsy" matches "temporal lobe epilepsy")
   and diagnosis-by-code-alone (already in `CENTRAL_PENDING.md`) affect FEPI-TEMP P02, P03 and RP01.
9. **`CENTRAL_PENDING.md`** (orchestrator): FEPI-TEMP is now in `DISCRIMINATOR_CONDITIONS`; its
   leak-guard item (P02, P03, RP05) is clean; the FEPI-TEMP guidance claims pass.
