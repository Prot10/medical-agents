# MS-RR: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Sources: the plan (`plans/MS-RR.md`), the 30 case logs
(`logs/MS-RR-*.md`; there is no reviewer notes file for MS-RR) and scripted checks over the 30
case files (M01 to M04, P01 to P05, RM01 to RM04, RP01 to RP05, RS01 to RS06, S01 to S06). All 30
cases are `draft`. Every log has a worker table and a verifier section; the RS and S logs also
carry an adversarial verification. The auditor read in full the two thinnest logs' cases (M03,
M04) and every literature and drug output of the condition. Each of the 30 logs now ends with a
"## Condition audit" section listing the audit's edits and why.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass, with no warning. Before the audit 25 cases warned
  that the AQP4/MOG order was "answered with the same stored report" as the mimic labs (class S).
- `case_io.py check` on all 30 ids: schema OK and synonym guard OK for every case. The suite has
  1 failure (`test_guidance_claims`), expected until the MS-RR guidance claims are rewritten
  (CENTRAL 3). No test failure names an MS-RR case. 3332 tests pass.
- `test_case_guards.py -k MS-RR`: 60 passed. The discriminator, leak and hijacked-index helpers,
  run directly on the 30 cases, return nothing (MS-RR is not yet in `DISCRIMINATOR_CONDITIONS`;
  CENTRAL 4).
- Scripted uniformity checks, clean after the audit fixes:
  - canonical facts (plan 1.2): five 2024 DIS regions with the optic nerve by MRI, OCT or VEP;
    four or five regions need no DIT; two or three need DIT, positive CSF (OCB or kFLC) or the
    central vein sign; supporting evidence over 50 or with vascular risk. No "2017 criteria" text
    survives outside the literature outputs that say the 2024 revision supersedes them;
  - tiers match plan 3.2 and the per-case lines, or a logged deviation (M01, M02 OCT; RM04 VEP;
    RS05 AQP4/MOG recommended by the plan's own rule). AQP4/MOG: 8 required (M04, RM01, RM02,
    RP01, RP02, RP03, RP05, RS01), 17 recommended, none in P01, P02, P03, RM03, RS04;
  - pathway order brain MRI, spine MRI, labs, AQP4/MOG, CSF, VEP, OCT, others, drug check,
    literature last; the stop rule lists exactly the required criteria with max 2 additional
    actions (S, RS, M) or 3 (P, RP, RM01, RM02);
  - sequence constraints: brain MRI before CSF (soft) where CSF is a criterion; RP02 and RP03
    have no CSF criterion (LP contraindicated, avoided action, plan L);
  - no spinal-cord lesion text in any brain MRI report; no LP in a mass-effect case;
  - the literature criterion is optional, `{}`, last, with empty expected evidence (plan O); the
    drug check is `{}`, optional, recommended only in RP03 and RP05;
  - every literature and drug output was read: none names a finding the case lacks; every
    medicine or allergy a drug output names is in the patient record (RM01's levetiracetam is
    the proposed new drug, as its log decides);
  - no em dash in any new text; the remaining em dashes are in patient text and outputs written
    before the round, and in `metadata.condition_name` (9 cases);
  - none of these strings is left: "ruling", "ROUND_POLICY", "criteria pack", "earns no credit",
    "Optional:", "(optional)", "naive", "(background only)", "(background evidence only)",
    "agent not specified on this case's pathway", "Requested agent".

## Error classes and how each was fixed

The plan's classes A to R were applied by the workers and checked by the verifiers:

- **A. Template criteria (30).** Labels, rationales and expected evidence rewritten per case;
  labs `{panels: [CBC, vitamin_B12, TSH, HIV]}`; CSF alternatives OCB or kFLC; AQP4/MOG moved out
  of the labs criterion into `action-aqp4-mog-cba` with three alternatives (A8); VEP and OCT
  optional where the case relies on them.
- **B. AQP4/MOG targeting.** The template "exclude NMOSD and MOGAD" must deleted; the tier follows
  the red-flag rule (3.2).
- **C. Differential** updated with case reasons and the results that lower each mimic.
- **D. Shared key clinical evidence** rewritten from the case data (attacks, DIS count, DIT or
  CSF, mimics argued against).
- **E. Lab rows with leaked significance** (19 cases, 22 rows): `clinical_significance` nulled.
- **F. Future-data and treatment-response follow-ups** (17 cases) deleted; their content became
  musts where it was a decision.
- **G. Wrong tool** (VEP and OCT on `order_specialized_test`, MRS on `order_advanced_imaging`,
  biopsy on `obtain_tissue_diagnosis`, spine on `order_body_imaging`).
- **H. Spinal-cord findings inside brain MRI reports** removed (M02, M03, RS02 and others).
- **I. Acute optic neuritis timing and OCT** (F7): no thinning in the first weeks.
- **J. CSF reports**: pattern interpretation, kFLC index added, contradictory flags fixed.
- **K. Musts and prohibitions template**: one formulation must, case-specific relapse, DMT and
  pre-DMT screening musts; T10 only in women of child-bearing potential, T9 and T8 only with a
  case reason, T13 only with myelopathic signs; wrong drug facts deleted.
- **L. LP with a mass lesion** (RP02, RP03): CSF criterion removed, LP an avoided action.
- **M. Fallbacks** consistent with the case (CT shows the lesion in RM01, RM02; EEG slowing after
  RM01's seizure). **N. Avoided actions** with case reasons. **O. Literature and drug outputs**
  without case findings. **P. Pathway order.** **Q. Diagnosis block.** **R. Patient realism.**

Classes the condition audit found after the workers and verifiers, all fixed through `case_io`:

- **S. AQP4/MOG results served to the mimic-panel order (25 cases).** Plan A8 kept the antibody
  rows in `initial_tool_outputs.labs`. The MockServer serves the whole initial labs payload to the
  first `interpret_labs` order, so the required mimic panel already returned "AQP4-IgG negative,
  MOG-IgG negative": an agent learned the result of `action-aqp4-mog-cba` without ordering it.
  The two rows now live in a `followup_outputs` entry (`interpret_labs`, trigger
  `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, interpretation "not detected by
  cell-based assay; a negative result does not entirely exclude NMOSD or MOGAD"), after the
  imaging follow-ups. Sentences about the antibodies were removed from the initial labs
  interpretation in P04, P05, RM01, RM02, RM04, RP01 to RP05, S05 and S06. A MockServer probe
  confirmed that all three alternatives and a combined order receive the rows in either order,
  and that the mimic panel no longer does. Deviation from plan A8, decided for dataset quality.
- **T. Differential ICD codes (17 cases, 25 fields).** Neurosarcoidosis was D86.85 (sarcoid
  myocarditis) in P04, P05, RM04, RP01, RP04, RP05, RS01 to RS06: now D86.89. ADEM was G04.81
  (other encephalitis) in P05, RM01, RM02, RM03, RP01, RP02, RP03, RS01 to RS06: now G04.00. The
  other MS-RR cases already used D86.89 and G04.00. Differential codes are not scored, so no
  synonym change follows.
- **U. Generic formulation must (12 cases).** M01 to M04, P01, P02 and S01 to S06 kept the
  plan's bare canonical text, which gives the grader no regions to check. Each now ends with
  "(here ...)", taken from the KCE DIS line and the stored outputs, as in the other 18 cases. M02,
  M03, P01 and P02 have three MRI regions completed by DIT, with the optic nerve a fourth region
  only if the optional VEP or OCT is done; M01 and S06 have four, with the optic nerve a fifth.
- **V. Empty drug-check expected evidence (12 cases).** M01 to M04, P01, P02, S01 to S06 now
  state the interaction result of the stored output in policy voice (no 60-character overlap
  with the output; the leak guard passes).
- **W. Prohibition texts T11 and T13 not canonical (18 and 11 cases).** Three variants of the
  chronic-steroid prohibition (two with em dashes, one truncated) are now the canonical "Do not
  use chronic oral corticosteroids as maintenance treatment for MS: they do not prevent relapses
  or disability and cause cumulative harm" in all 30. The spinal-cord prohibition is canonical in
  every case that has it, except P04's case-specific version. M04's teriflunomide prohibition and
  P03's vitamin D red herring lost an em dash (and a capitalised NOT).
- **X. Engineering text.** "(background only)" and "(background evidence only)" in 12 literature
  labels (RM04, RP01 to RP05, RS01 to RS06) became topic labels from the stored output; "a naive
  agent" in P04's red herring became "the agent"; the drug fallback `proposed` "Requested agent"
  (M03, P02) and "(agent not specified on this case's pathway)" (P03, P05) became "Not specified".
- **Y. Echo fallback without `echo_type` (S01 to S06).** Added "TTE"; the discriminator guard
  requires the vocabulary term, and the other 24 cases had it.
- **Z. HIV re-ordered in the pre-DMT screening must (13 cases).** M01 to M04, P01, P02, RM04 and
  S01 to S06 asked to check HIV although the required mimic panel reports it. The must now says
  "(HIV already non-reactive)" or "(HIV already negative)", as the RM, RP and RS cases do.
- **Single-case fixes.** RM04's brain MRI `recommended_actions` ("Spinal cord MRI recommended to
  complete demyelinating disease evaluation") pointed at a required order: emptied. RP04 gave
  Dobson 2013 an invented title ("a geographical meta-analysis"): now the published title, as in
  P02 and P03. RP02 and RP03 biopsy criteria had no citation: `[McDonald_2024]`, as on RM01.

## Counts

- Plan classes A to R: applied in all 30 cases by the workers; the worker and verifier findings
  are in the case logs.
- Condition audit: 145 field-level edits in 30 cases (classes S to Z and the single-case
  fixes), all fixed, none declined.
- Flagged and not changed: 4 items, all central (CENTRAL 5, 6, 7 and the `metadata.condition_name`
  wording, which is metadata only).
- Cases changed by the audit: 30 of 30.

## CENTRAL requests (consolidated)

1. **Criteria pack** `dataset-generation/criteria_packs/MS-RR.md` (plan 5.1, every log):
   - add the keys the cases cite: `[McDonald_2024]` (Montalban et al., Lancet Neurol
     2025;24:850-865), `[Wattjes_2021]` (Lancet Neurol 2021;20:653-670), `[NICE_NG220]`, and
     `[Petzold_2017]` (RP04, RP05; check that it is in the allow-list);
   - add `[Hardy_2013]` (Hardy TA, Chataway J. Tumefactive demyelination: an approach to
     diagnosis and management. JNNP 2013) and cite it on the tumefactive biopsy, MRS and CT CAP
     criteria (RM01, RM02, RP01 to RP03); RP01's CT CAP criterion has no citation until then;
   - move the diagnostic text from McDonald 2017 to the 2024 revision; drop literature and drug
     check from the required pathway.
2. **Synonyms** (`diagnosis_synonyms.yaml`, G35 entry, plan 5.2): remove the progressive-course
   codes G35.B and G35.C from a relapsing-remitting label (check the FY2026 G35 subcodes first);
   remove "demyelinating disease" (its tokens occur in "NMOSD, an inflammatory demyelinating
   disease"); review the bare "MS" ("MOGAD rather than MS" matches). Re-run
   `apply_diagnosis_synonyms.py`; never by hand.
3. **Guidance claims** (`condition_tool_guidance.yaml`, `test_guidance_claims.py`, plan 5.3): the
   AQP4/MOG criterion is now in 25 cases (8 required, 17 recommended) and its results are a
   follow-up, not initial labs rows; EEG and CT are no longer avoided in RM01 and RP03, CT not in
   RP02. Plan 3.5 and A8 should list RS05 as recommended. This is the one expected test failure.
4. **Discriminator guard**: add MS-RR to `DISCRIMINATOR_CONDITIONS`; all 30 cases pass it now.
5. **Code, MockServer labs** (class S):
   - the first `interpret_labs` order receives every panel of the initial labs, whatever it
     names. Second-tier assays stored there leak to the first-line order. Either filter the
     initial payload by the ordered panels, or make the perfect-agent "same stored report"
     warning a failure for labs so the data are fixed case by case. Other conditions with
     antibody or second-tier rows in their initial labs are likely affected;
   - an order naming only assays the case does not store is answered with the initial labs
     again: in P01, P02, P03, RM03 and RS04 an AQP4/MOG order returns the mimic panel and no
     antibody result. Serve the library normal for the ordered assay, or a "not stored" message.
6. **Checker** (`perfect_agent.py`): `<- ?` source labels for the brain MRI and labs in the S
   cases come from `_source` comparing an `exclude_none` dump with an output that keeps null
   fields. Cosmetic.
7. **Guards** (`test_case_guards.py`, plan 5.5): an `analyze_brain_mri` output must not contain
   "thoracic cord", a "T[1-9]-T" level or "conus"; add the banned strings "agent not specified on
   this case's pathway", "Requested agent" (drug fallback `proposed`), "naive agent",
   "(background only)" and "(background evidence only)".
8. **Vocabulary** (plan 5.4): closed. `kappa_free_light_chain_index`, `AQP4_IgG_cell_based`,
   `MOG_IgG_cell_based`, `NMO_MOG`, `MR_spectroscopy`, `chest_abdomen_pelvis_CT` and
   `stereotactic_biopsy` all resolve (the perfect agent orders them through the schema check).

## Open questions

None needs information only Andrea has. The workers' open questions, decided per "decide in the
way best for dataset quality":

1. **RM01 lesion sides**: left paramedian pons and left middle cerebellar peduncle (left
   abducens paresis, left limb ataxia: ipsilateral signs) and a right posterior column C2-C3
   lesion for the earlier right-hand episode. Kept: anatomically correct.
2. **RM02**: the CT fallback shows the lesion (it contradicted the outside CT in the HPI) and CT
   stays an avoided action because a CT was already done. The driving must (left homonymous
   hemianopia in a driver) is kept: a real safety item.
3. **RM03**: methylprednisolone must for constant binocular diplopia is kept (a relapse that
   affects function, NICE NG220). No AQP4/MOG criterion per plan 3.2; see CENTRAL 5 for what an
   order returns.
4. **RM04**: the added VEP follow-up and optional criterion (the library normal VEP contradicted
   the RAPD and pallor) and the PTH change to 12 pg/mL (suppressed, as granulomatous
   hypercalcaemia requires) are kept.
5. **M01, M02 OCT**: optional OCT criteria with stored thinning are kept: the library normal OCT
   contradicted the documented chronic optic neuropathy. M03 has none (the optic symptom is days
   old).
6. **P01, P02 migraine**: the cases call the cord lesion supporting evidence as clinical prudence,
   not as a criteria requirement, because only the over-50 and vascular-risk wording of plan F4
   was verified. Kept; correct under either reading of the 2024 text.
7. **P02**: "Lhermitte sign not tested" kept as realistic examiner behaviour.
8. **RP04**: "No relative afferent pupillary defect" with a 24 um inter-eye pRNFL difference kept
   (a recovered optic neuritis can leave the swinging-flashlight test negative); the left leg
   numbness 8 years ago stays an undocumented possible event, not a counted attack.
9. **RS02**: four MRI regions, optic neuritis as the prior attack; the optic nerve is not counted
   because no VEP or OCT is served. Kept: correct under the 2024 rule.
10. **RS05**: AQP4/MOG recommended (verifier decision, the plan's rule over its per-case line).
    Kept.
11. **RS06**: the symptomatic C3-C4 lesion does not enhance (kept: plausible); B12 228 pg/mL
    without methylmalonic acid is kept as a distractor, with no MMA must.
12. **S04**: the gastrointestinal work-up must for iron deficiency in an adult man is kept: a real
    management item of this patient.
13. **S05**: disc swelling kept (about a third of MS optic neuritis), settled by the negative
    live-cell MOG-IgG.
14. **S06**: four MRI regions, the optic nerve a fifth only with OCT or VEP; the formulation and
    KCE accept either count. Kept.
15. **Class S deviation from plan A8**: the antibody rows moved to a follow-up (above). The plan
    lead may prefer the central fix (CENTRAL 5); the case data are correct under either.
