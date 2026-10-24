# SE: decisions on the open questions (24 October 2026)

Andrea, 24 Oct 2026: resolve every open point "nel modo migliore per la qualità del dataset". Each
entry gives the question, the decision, the reason with its source, and what changed where. Sources
checked on 24 Oct 2026: the Salzburg criteria paper (Leitinger et al., Epilepsy Behav
2015;49:158-163; the pack had a wrong journal), the GEMNet TCA guideline (Body et al., Emerg Med J
2011;28:347-368), and the Neurocritical Care Society guideline list (no update of Brophy 2012; the
2026 NCS guideline covers neuroprognostication in SE only). Every changed case log has a
"## Close-out (24 Oct 2026)" section.

## Step 1: synonyms, labels and codes

**G41 type codes granted across types (scan of all 30).** Every G41 case accepted G41.0, G41.2 and
G41.8 through the category, so a convulsive case accepted the NCSE code and vice versa (the scorer
credits a code alone). Decision: the G41 category now grants only "status epilepticus", "SE",
G41.9, G40.901, G40.911; type labels come from the case's own code (G41.0 convulsive, G41.2 NCSE);
G41.8 labels are scoped per phenotype (G41.8+ncse for SE-M07 and HEP-ENC-P06, G41.8+myoclonic for
SE-P03, G41.8+fbds for SE-S12). `--prune --conditions status_epilepticus` applied. Known residue
(scorer): the generic "status epilepticus" label still credits an answer of the wrong type, as the
generic SAH label does (under-specified, kept by the SAH precedent).

**CENTRAL 3b, NCSE code and labels in convulsive or motor cases.** S02, S07, S09 (focal onset
evolving to bilateral convulsions, all three convulsive at presentation) -> G41.0: ILAE 2015 puts
focal-to-bilateral convulsive SE under convulsive SE [ILAE_2015_SE], and ICD-10-CM has no separate
code; S02 is coded the same as S07 and S09 because it is the same phenotype (the summary allowed
either). S12 (FBDS status) -> G41.8, a motor SE, with "faciobrachial dystonic seizures" as the only
specific label (anti-LGI1 encephalitis is in the history). M07 (generalized post-anoxic NCSE) ->
G41.8 with the NCSE labels kept. M01, M08, M09 and the other focal NCSE cases keep G41.2. P03
(myoclonic SE) loses the NCSE labels.

**CENTRAL 3c, labels with treatment, future or wrong-mechanism clauses.** Ruling 3 permits a label
correction once decided; condition and case ids unchanged.
- P05 -> "Organophosphate poisoning with cholinergic crisis and electrographic status epilepticus":
  the EEG records nine seizures in the first hour (real SE, not "apparent"), the seizures are not
  nicotinic, and the 48-hour intermediate syndrome is a future event.
- P07: "but resolving with ammonia correction" removed (treatment response).
- P08: "requiring IV pyridoxine as specific antidote" removed (treatment). S10: "requiring sodium
  bicarbonate" removed for the same reason (one note is a class).
- P03: "hypothermia confounding EEG interpretation" -> "on light propofol sedation during targeted
  temperature management at 36 C" (36 C is not a confounding hypothermia).
- M09: "from ibuprofen-warfarin interaction" -> "on warfarin with a supratherapeutic INR (4.8) and
  added bleeding risk from concurrent ibuprofen" (NSAIDs add bleeding risk through platelet and
  mucosal effects; the INR effect is variable, as the case's own drug check says).
- CENTRAL 3a (S03 Na 121, M04 Na 123): already in the cases; the synonym expansion is current.

**Wrong-cause synonyms.** Retired "cholinergic toxidrome" (P05: credits carbamate, nerve-agent,
muscarinic-mushroom or drug causes) and "pyridoxine deficiency seizures" (P08: dietary or inherited
deficiency, a different cause); both are in `RETIRED` so `--prune` strips them.

**History-given diagnosis (P06 verifier flag; P04 by the same class).** Decision: code the part the
case scores and accept only labels that name it (HEP-ENC-P04 precedent).
- P06: probable sCJD is in the past medical history; A81.09 and "CJD" scored without the NCSE. Now
  G41.2 with labels naming both ("CJD/sCJD/creutzfeldt jakob disease/prion disease" with "status
  epilepticus" or "NCSE"); G41 and G41.2 generic entries exclude the case. A81.09 now applies to no
  case and is kept for future CJD cases.
- P04: the left MCA stroke is in the chief complaint; the stroke labels and I63 codes scored a
  repeat of the history. Now R56.9 with labels naming the seizure component ("stroke LPDs", "stroke
  seizures", "acute symptomatic seizures" and variants). Residue: "NCSE with LPDs after stroke"
  still matches "stroke LPDs" (scorer negation/overcall item, CENTRAL).
- Not applied to P07: HE is the team's working hypothesis in the HPI, but the case tests resisting
  the NCSE answer, which a correct HE answer does.

**CENTRAL_PENDING SE items.** SE-P04: the pending prune is superseded by the recode (all stroke-only
labels and I63 codes gone; the I63.5/I63.51 addition no longer applies). SE-P07: "hepatic coma" and
K72.91 removed (GCS 13, West Haven II). "WHO 2025 Annex A.4": no SE case, log or the SE pack cites
it. `apply_diagnosis_synonyms.py --check --conditions status_epilepticus`: clean.

Side effect outside SE (not edited, for the orchestrator): HEP-ENC-P06 (G41.8) keeps its NCSE labels
through G41.8+ncse, but still lists G41.0 and G41.2 in `icd_codes` until `--prune --conditions
hepatic_encephalopathy` runs; that prune would remove only those two codes.

## Step 2: criteria pack (`dataset-generation/criteria_packs/SE.md`)

Rewritten from plan section 1 and the decisions here: ICD codes by type (and the P04/P06 coding
rule); ILAE 2015 and Salzburg definitions; ACNS 2021 wording; lateralization; work-up hierarchy
with the T-LABS extras, cEEG as the initial EEG with no post-treatment EEG, MRI and CSF by
indication, second-tier panels as their own criterion, blood cultures only with suspected
infection, ECG and SSEP indications; drug check per ruling 6 with T-DDI form and the corrected
phenytoin-amiodarone and dexamethasone facts; literature per ruling 5; treatment facts for musts
(Wernicke corrected to at least 200 mg tid per EFNS, 500 mg tid as common practice); waste and harm
lists (LP contraindications, phenytoin in TCA and isoniazid, PNES escalation, LPDs alone); sequence
constraints and stop rule as built; pitfalls including the template carry-over found in this round.
"Literature required" and "drug check required" are gone. Allow-list: every key cited in the 30
cases (29 keys, from [Brophy_2012] to [Magpie_2002], including [EANO_2021] and
[AHA_ASA_Stroke_2026]) with a full reference; [Salzburg_NCSE_2015] corrected; added and verified
[Body_2011_TCA] (S10) and [HIV_OI_guideline] (M08), not yet cited in a case; [AHA_Stroke_2019]
marked superseded. No isoniazid key: no authoritative guideline found; the pack states the facts
without one.

## Step 3: generator (`conditions.yaml`, status_epilepticus block)

- `common_followups`: removed `request_continuous_eeg_monitoring` (its "continuous" token hijacked
  the `continuous_icu` EEG criterion and seeded post-treatment EEGs, classes C4 and CENTRAL 4) and
  `request_aed_optimization` (post-loading levels, ruling 4); `request_lp_autoimmune` (orphan CSF in
  12 cases) replaced by `request_lumbar_puncture` with the indication and LP contraindications;
  autoimmune panel and MRI descriptions now carry their indications. A comment states the rule.
- `key_findings`: the benzodiazepine "therapeutic test" is a diagnostic trial only in equivocal NCSE;
  PLEDs -> LPDs (ACNS 2021); labs list values only, the indications for ASM levels, toxicology,
  ammonia, coagulation, troponin and beta-hCG, and blood cultures only with suspected infection; a
  comment bans the Exclusion-studies block; CSF post-ictal pleocytosis corrected (usually under 10
  cells, not "5-30 normal variant"), normal CSF no longer "excludes CNS infection".
- `difficulty_variants`: presentations no longer contain the valproate level, EEG results or the CT
  result. The Exclusion-studies and blood-culture templates are not in the generator code
  (`git grep` finds them nowhere), so nothing else to remove.

## Step 4: review-app guidance

`test_guidance_claims`: "se/MRI required in 17" failed (14 now). Response for `analyze_brain_mri`
rewritten (required 14, recommended 6, optional 7, absent in the 3 toxic cases); YAML regenerated
with `--write`; claims table checks required 14, (recommended, optional) (6, 7) and absent 3. All SE
claims pass (the remaining failures are NMDAR-ENC and MIG-AURA).

## Step 5: open questions and auditor flags

None needed information only Andrea has. Each judgment call in the summary, decided:
- **M07 SSEP deleted, prognostication as a prohibition on limiting care.** Confirmed: she woke and
  was discharged; ERC-ESICM prognostication is for patients who remain comatose [ERC_ESICM_2021].
- **P03 encounter at about 24 h, SSEP and MRI inside it, prognostication deferred to 72 h.**
  Confirmed [ERC_ESICM_2021]; label corrected (step 1).
- **P05 respiratory function criterion deleted.** Confirmed: FVC and NIF cannot be measured meaningfully at GCS 3,
  and the intermediate syndrome appears 1 to 4 days later [Eddleston_2008];
  monitoring is a must. Glucose 186: confirmed (hyperglycemia is typical of OP poisoning).
- **P08 intent unknown, T37.1X1A.** Confirmed: the ICD-10-CM guidelines (chapter 19, poisoning) code unknown intent
  as accidental; undetermined (X4) only when the record states intent cannot be determined.
- **P07 NCSE kept moderate, benzodiazepine trial a must.** Confirmed: the EEG does not separate
  metabolic from ictal origin; reactivity, evolution and a trial under EEG do [Salzburg_NCSE_2015].
- **S03 8 mmol/L in 24 h; S06 10 mmol/L.** Confirmed: hypokalemia is a demyelination risk factor
  [Verbalis_2013; Spasovski_2014].
- **M06 equivocal Babinski on the left.** Confirmed: a right temporal lesion gives left-sided signs,
  matching the left arm drift (plan 1.2). No revert.
- **S12 serum LGI1 required, CSF recommended.** Confirmed: serum is the more sensitive specimen and
  CSF LGI1 is often negative [Irani_2011; Graus_2016].
- **P06 serum autoimmune panel inside the core labs.** Decided: split into its own recommended
  criterion `action-autoimmune-panel` with its own follow-up (same values). Reason: inside the
  required core labs it forced the agent to bundle a second-tier test into the first order, unlike
  every other SE case (plan 3.1 item 7). perfect_agent: pass.
- **M05 perfect_agent warning on the ultrasound alternative.** Simulator artefact (the worker
  probed the order and the follow-up is served); left to CENTRAL.

## Checks

`perfect_agent.py` 30/30; `case_io.py check` on all 30: schema OK, synonym guard OK, no failure
names an SE case; `test_case_guards -k SE-`: 60 passed; `apply_diagnosis_synonyms.py --check
--conditions status_epilepticus`: clean; SE guidance claims pass.

## Cases changed in the close-out

29 of 30 (all but P02): code prune in all G41 cases; recodes S02, S07, S09 (G41.0), S12, M07 (G41.8),
P06 (G41.2), P04 (R56.9); labels P03, P05, P07, P08, M09, S10; synonym removals P05, P07, P08; P06
antibody-panel criterion.

## Still needing Andrea or the physicians

Nothing needs information only Andrea has. For Reviewer 2 at re-review: the label changes in P03,
P05, P07, P08, M09, S10 (M09 is unreviewed, the others approved or treated as approved); the
recodes of S02, S07, S09, S12, M07; P04 and P06 now need the seizure component for diagnosis credit;
the P06 antibody panel is a separate recommended step.

## CENTRAL

1. **Scorer**: negation and overcall matching. "NCSE with LPDs after stroke" contains the tokens of
   "stroke LPDs" (P04), and "non-convulsive status epilepticus" contains every token of "convulsive
   status epilepticus" (all G41.0 cases). Same root as the SAH "non-aneurysmal" item.
2. **Scorer**: a per-case "all of" rule would let P04 and P06 keep the disease code while requiring
   the seizure component (the recodes are the workaround, as in HEP-ENC-P04).
3. **Synonym prune outside SE**: HEP-ENC-P06 still lists G41.0 and G41.2; run `--prune --conditions
   hepatic_encephalopathy` when HEP-ENC is next touched.
4. **Vocabulary** (carried from the summary, not made here): `interpret_labs` panel `cholinesterase`
   (plasma and RBC; SE-P05, values now in the core labs); `analyze_csf` special tests
   `toxoplasma_PCR` and `EBV_PCR` and `interpret_labs` `toxoplasma_IgG` (SE-M08); `interpret_labs`
   `urine_sodium` (SE-M04); `NSE` only if SE-P03 is re-timed to 72 h. No `isoniazid_level`.
5. **Matcher**: a combined first lab order that includes a second-tier panel (`HIV`,
   `paraneoplastic_panel`) is answered by the initial labs (M08, P01).
6. **Library**: a tumour-aware tier so an off-pathway `MR_spectroscopy` in recurrent glioblastoma
   (M02) does not return a normal report.
7. **perfect_agent**: the M05 `pelvis_abdomen_ultrasound` alternative warning (simulator artefact).
8. Review UI: show initial outputs and follow-ups in criterion order (already requested).
