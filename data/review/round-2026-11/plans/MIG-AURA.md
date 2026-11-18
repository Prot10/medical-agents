# MIG-AURA round plan (November 2026)

Lead plan for MIG-AURA-M01..M08, P01..P09, RM11, RS11 and S01..S11, written 16 Nov 2026. There are
63 notes, all from R1 (NB-KSC3-TWUA-QDTM). The decisions and their reasons are in
`plans/MIG-AURA-decisions.md`; D1..D18 below refer to its entries. **No MIG-AURA case is approved**
(`work/approved.txt` lists none).

Cases read in full: P05, RS11, RM11, P02. Read in part: P08 (HPI, assessment, EEG, differential),
P03 (HPI, MRI), P04 and P06 (genetics, family history), P09, M01, M03, M04, M05, M06, M08, P01,
P07 and S10 (assessment and key texts). All 30 were surveyed structurally.

Scripts are in `/home/aprotani/review-round-2026-11/work/scratch/mig-lead/`:

| script | what it measures |
|---|---|
| `survey_mig.py` (output `survey.txt`) | criteria, tiers, avoided actions, sequence, stop rule, musts, prohibitions, outputs per case |
| `flat_mig.py CASE` | the whole case as path: value lines (full reads) |
| `classes_mig.py [prefix]` | topiramate with implant, TIA prohibition, antithrombotic-stop musts, DWI/TIA claims, "preventive therapy required/indicated", "all secondary causes excluded", literature, sinus-rhythm claims; prefix "" runs over all 600 cases |

Workers:
- Edit only through `case_io` (`/home/aprotani/projects/ma-round11/data/review/round-2026-11/bin/case_io.py`).
- After each case, run `perfect_agent.py CASE -v` and `case_io.py check CASE`. Run `mri_probe.py`
  after any MRI edit (P03).
- Keep every `criterion_id`. New ids are given below.
- English in the case's British spelling. No em dashes in new text. No review-process text in
  `metadata`.
- A label change (accepted[0]) is logged as a label change. Synonym labels after accepted[0] are
  not hand-edited.
- Do not add any literature criterion or stored output (class LIT).

## 1. Governing guidelines and canonical facts

The October table (pack section 8) still governs. Additions and changes for this round:

| key | source | governs |
|---|---|---|
| `[ICHD_3]` | Cephalalgia 2018;38:1-211 | 1.2.1, 1.2.2, 1.2.3 (1.2.3.2 sporadic), 1.4.3, 1.4.4, 1.5.2 |
| `[FSRH_DI_2022]` NEW | FSRH CEU Guidance, Drug Interactions with Hormonal Contraception, May 2022 | Topiramate is a potential enzyme inducer at any dose. With an enzyme-inducing teratogen use a Cu-IUD, LNG-IUS or DMPA; the POP and the implant are not recommended |
| `[MHRA_topiramate_2024]` | MHRA DSU June 2024 | Topiramate pregnancy prevention programme |
| `[MELAS_2026]` NEW | Mancuso M et al. Eur J Neurol 2026;33(4):e70588 | EEG early in a stroke-like episode; prompt antiseizure medicine if seizures are suspected; no specific contraindication to the standard acute headache drugs (triptans included) |
| InterERNs 2024 NEW (text) | Seizure management in primary mitochondrial disease, Eur J Neurol 2024 | Standard antiseizure medicines allowed; valproate excluded in POLG disease |
| NICE CG109 NEW (text) | TLoC in over 16s, 1.1.3 | 12-lead ECG and witness account for every blackout |
| NICE NG128 NEW (text) | Stroke and TIA in over 16s | Suspected TIA needs urgent specialist assessment; the diagnosis is clinical |
| Powers 2019 NEW (text) | AHA/ASA early management of acute ischaemic stroke, Stroke 2019;50:e344 | Brain imaging on arrival; noninvasive vessel imaging when endovascular therapy is considered |
| `[ESC_AF_2024]` | Eur Heart J 2024;45:3314 | CHA2DS2-VA: 0 means no anticoagulation; a TIA scores 2 |
| `[AHS_2021]` | Headache 2021;61:1021 | Prevention "offer" and "consider" thresholds; "consider" for brainstem, hemiplegic or prolonged aura |

Canonical facts (use them verbatim in meaning):
- A normal MRI or DWI excludes infarction, not TIA. Imaging never "excludes" or "distinguishes"
  TIA, and sinus rhythm during an episode never excludes cardioembolism. The distinction is
  clinical.
- Topiramate: see the D3 canonical must. The implant and pills are not adequate at any dose. The
  methods are Cu-IUD, LNG-IUS, or DMPA with condoms.
- Prevention is "considered and discussed" when AHS lists the situation under "consider"
  (brainstem aura, prolonged aura, under 4 days a month). It is "offered" at or above the offer
  threshold.
- Probable migraine with aura, including the hemiplegic subtype with only one qualifying attack, is
  ICHD-3 1.5.2. Two qualifying attacks with no affected relative is 1.2.3.2, sporadic, with no
  "probable" and no genetics needed.
- AF found after a stroke supports a "probable" cardioembolic mechanism. It does not prove it.
- A stroke-like episode in MELAS is not an ischaemic stroke for the triptan label.

Scorer fact: recommended and optional criteria never count against `max_additional_actions`
(`policy_reward.py` 138-146).

## 2. Classes

| class | description | note ids | cases (measured) | decided fix |
|---|---|---|---|---|
| LIT | "no" on a literature step | 25 notes (D1) | 23 cases with notes; 0 literature strings left in all 30 | FIXED by class LIT (commit 393c547e): confirm, add nothing |
| PRAISE | approval of the chief complaint | 8 notes (D2) | S01-S05, S08, S09, S11 | NO-ACTION |
| TOPI-CONTRA | the implant is listed as adequate with topiramate; the dose threshold is given without the FSRH caution | 4ed3d3c1, 16e768ca, e903ea4c, f1d9b692, 801e6db7, 5b8ab438 | Musts: M04 REQ4, M06 REQ3, P03 REQ3, RM11 REQ2 and PRO1, S07 REQ3, S10 REQ2. Reports: P03 init warnings[2] and interactions[4]; M04 FU0 w[1] and FU2 i[1]; M06 FU0 w[1] and FU1 i[2]; P04 init i[1]; S10 FU0 w[0]; RM11 init i[0]. None outside MIG-AURA | D3 canonical must; reports add "FSRH: potential inducer at any dose"; S10 adds the vasectomy condition |
| TIA-CERT | categorical TIA exclusion or prohibition; unconditional antithrombotic stop | faa8bb3e, 30f0b036, b37e0b4d (+ D5, D6) | Prohibition in M01, M03, M05, P01, P09, RS11, S09. Stop musts in M03, P01, P02, P05. Imaging-excludes-TIA text in M05 REQ0, P01 REQ0 and accepted[0], P02 REQ0. Sinus-rhythm claims in P02 (3 fields) | D4: conditional must in first presentations (M01, M03, P01, RS11); reworded prohibition in M05, P09, S09; optional vessel imaging in M01 and M05; P01 MRA required |
| AF-ANTICOAG | anticoagulant stop made automatic; rhythm correlation used as proof | 316f77a5, 5ea76cbc, 794bf874, 93326a8a | P02, P05 | D5, D6 |
| STOP-RULE | the stop rule is said to penalise recommended studies | d33fb521, fee18a5b, 335b1fbd, 91145af1, f5f97597 | M03, M07, S10 (premise wrong: ALREADY-FIXED); RS11 ECG and P08 EEG were real gaps | D7, D10, D11 |
| DX-CERT | over-certain label or must | 1b2dc411, 034920f8, a219ebf2, befb9ef9, 0efba9dd, 19601077, 794bf874 | "preventive therapy required/indicated": M06, M04 (S10 kept). "All secondary causes excluded": RS11 (P03 kept, supported). Others are single cases: M08, P07, P09, RM11, P05; class extension to M03's code | D8, D9, D10, D12, D13, D15, D6 |
| MISSING-CRIT | safety action with no criterion | 93326a8a, 19601077, 91145af1, f5f97597, 1ea8561d | P05 labs, RS11 ECG, P08 EEG, RM11 arterial imaging | new criteria (section 3) |
| GENE-SCOPE | full NOTCH3 sequencing when the familial variant is known; testing imposed | 95362414, 7e1924c9 | P04, P06 (only cases with a named familial variant) | D16 |
| MELAS-DRUGS | categorical drug prohibitions in MELAS | 64c11ceb, 7dd02d6c | P08 | D11 (triptan prohibition removed; valproate kept on patient grounds; metformin as preference) |
| IMG-REVIEW | repeat MRI required where outside images exist | 19136208 | P03 | D14 |
| ED-PATHWAY | ED presentation without a stroke or seizure pathway; CT labelled waste | 1ea8561d | RM11 | D15 |

Other conditions: the TIA prohibition, the topiramate-implant text and the 200 mg threshold were
counted over all 600 cases. Only MIG-AURA has them. The 12 "Stop aspirin/apixaban/warfarin" must
hits outside MIG-AURA (GLIO-HG-RP01/RP04/S05, ISCH-STR-RM02, SYNC-CARD-RM04, VASC-DEM-M03/P03/P04)
are a different context (perioperative or bleeding) and are not this class.

## 3. Per-case index (all 30)

Legend: notes with their ruling, then the class findings in the case. "Crit+" is a new criterion
(id, tier, alternatives). All cases are draft; none are approved.

### M01 (35 F, first sensory aura, Microgynon)
- 2a94bbb7: FIXED (class LIT, commit 393c547e; none left).
- faa8bb3e: FIXED (D4). Delete PRO1, the TIA prohibition. REQ1 becomes the D4 conditional must
  (features: positive sensory symptom spreading over 10-12 min, headache within 15 min, normal
  examination). Crit+ `action-vessel-imaging-optional` (optional; MR_angiography or carotid_duplex).
  metadata.difficulty_description "requires TIA exclusion" becomes "TIA must be considered".

### M02 (29 F, visual and sensory aura, Yasmin)
- 01f7876b: FIXED (class LIT).
- No class finding. No other change.

### M03 (42 M, first motor aura, aspirin from GP)
- 9664e97f: FIXED (class LIT).
- 30f0b036: FIXED (D4). REQ0 becomes the D4 aspirin-review must. Delete PRO1, the TIA prohibition.
- d33fb521: ALREADY-FIXED (D7). MRI and MRA are recommended criteria and never extra. Stop rule
  unchanged.
- Class DX-CERT (D13): in accepted[0] "(ICHD-3 1.2.3)" becomes "(ICHD-3 1.5.2)" (one qualifying
  motor attack). This is a label change.

### M04 (33 F, brainstem aura, Rigevidon)
- 9e6fc9af: FIXED (class LIT).
- 4ed3d3c1: FIXED (D3). REQ4 becomes the canonical topiramate must. FU0 warnings[1] and FU2
  interactions[1] get the FSRH any-dose caution.
- Class DX-CERT (D8): in accepted[0] "preventive therapy indicated" becomes "preventive therapy to
  be considered". REQ3 changes "Offer migraine prevention because the brainstem aura recurs" to
  "Discuss prevention (AHS 2021 'consider' for brainstem aura; three attacks in four months),
  weighing disability and preference", keeping the agents and doses.

### M05 (48 F, typical aura without headache)
- fca3be91, 8763368b: FIXED (class LIT).
- Class TIA-CERT (D4): PRO0 becomes the reworded prohibition (stereotyped auras identical to 20
  years of previous ones). REQ0 "MRI show no sign of TIA" becomes "MRI shows no infarct or structural
  disease; the TIA question is answered by the identical features of her lifelong aura". Crit+
  `action-vessel-imaging-optional` (optional; MR_angiography or carotid_duplex).

### M06 (31 F, prolonged aura, Gedarel, rizatriptan)
- b641b8e0: FIXED (class LIT).
- 16e768ca: FIXED (D3). REQ3 becomes the canonical must. FU0 warnings[1] and FU1 interactions[2]
  get the any-dose caution.
- 1b2dc411: FIXED (D8). accepted[0] "preventive therapy required" becomes "preventive therapy to be
  considered and discussed" (label change). REQ2 "Offer prevention" becomes "Discuss prevention,
  weighing disability, preference, comorbidity and drug risks", agents unchanged.

### M07 (27 M, exercise-triggered single attack)
- a6bcf14f: FIXED (class LIT).
- fee18a5b: ALREADY-FIXED (D7). MRI and MRA are recommended and credited. No change.

### M08 (38 F, aura after sertraline)
- ce7ba35d: FIXED (class LIT).
- 034920f8: FIXED (D9). accepted[0] becomes the D9 label (label change). REQ3, KCE[1] and
  red_herrings[0].correct_interpretation are reworded: association, not causation; the earlier
  monocular flashes are poorly characterised.

### P01 (52 F, aphasic aura, aspirin and atorvastatin)
- af4ad7e1: FIXED (class LIT).
- b37e0b4d: FIXED (D4). REQ1 becomes the aspirin-review must. Delete PRO0, the TIA prohibition.
  REQ0 becomes "the gradual build-up and headache after every episode favour aura; imaging excludes
  infarction and arterial disease, not TIA". accepted[0] "after TIA exclusion" becomes "TIA judged
  unlikely on the clinical features" (label change). `action-mra` goes from recommended to
  required and joins the stop rule. Add a soft constraint action-4-analyze-brain-mri before
  action-mra.

### P02 (44 M, aphasic aura plus paroxysmal AF, apixaban)
- bf5d87c0: FIXED (class LIT).
- 316f77a5: FIXED (D5). Remove criterion action-5-order-cardiac-monitoring and its stop-rule entry
  and sequence constraint [1]. Add avoided waste `order_cardiac_monitoring`
  `{"monitor_type": "implantable_loop_recorder"}`. action-4-analyze-brain-mri goes from recommended
  to required and joins the stop rule. The ILR follow-up stays as stored data.
- 5ea76cbc: FIXED (D5). REQ1 becomes the conditional apixaban review. REQ0 is reworded (no "not
  cardioembolic"). Delete PRO0. accepted[0] becomes "Migraine with aphasic aura (ICHD-3 1.2.1)
  co-existing with paroxysmal atrial fibrillation (alcohol-related)" (label change).
  required_components are kept. Reword differential[0], KCE[0] and [2], red_herrings[0] and
  metadata.condition_name / difficulty_description.

### P03 (38 F, migrainous infarction)
- 32b921e6: FIXED (class LIT).
- 19136208: FIXED (D14). action-4-analyze-brain-mri stays required. The label, rationale and
  expected_evidence become a review of the outside MRI (DWI/ADC). The MRI output becomes the
  neuroradiology review of the imported study at day 3: acute 4 mm right occipital cortical DWI
  lesion, low ADC. Run mri_probe.
- e903ea4c: FIXED (D3). REQ3's topiramate clause becomes the canonical text. Initial
  drug_interactions warnings[2] is corrected; interactions[4] gets the any-dose caution.
- Label: "all secondary causes excluded" kept (supported by four required studies; D14).

### P04 (34 F, typical aura, aunt with CADASIL)
- fb7dfc9b: FIXED (class LIT).
- 95362414: FIXED (D16). The NOTCH3 output becomes a targeted familial-variant test (exon 4
  c.457C>T, not detected), with no exon 2-24 sequencing or CNV. action-5-order-specialized-test
  goes from required to recommended and leaves the stop rule. action-4-analyze-brain-mri goes from
  recommended to required and joins the stop rule. REQ1 and REQ2 become conditional on her choice
  to test. action_criteria[2] expected_evidence and rationale say "targeted". Initial
  interactions[1] gets the topiramate any-dose caution (D3).

### P05 (46 F, aphasic aura labelled TIA, warfarin, INR 3.8, bleeding)
- 6f780f04: FIXED (class LIT).
- 93326a8a: FIXED (D6). Crit+ `action-labs-inr-fbc` (required; interpret_labs panels coagulation
  and CBC, either or both), in the stop rule, placed after the clinical assessment. New
  initial_tool_outputs.labs: INR 3.6, PT prolonged, aPTT and fibrinogen normal, Hb 124 g/L,
  platelets 238, WBC 6.4, MCV 88. fallback labs set to null.
- 794bf874: FIXED (D6). accepted[0] becomes the D6 label (label change). REQ1 splits into withhold
  now / decide on restarting after review of the original strip with the referring team. REQ0 and
  PRO0 are reworded. differential[0] and KCE[2] become conditional.

### P06 (58 M, CADASIL R182C)
- 26305ba4: FIXED (class LIT).
- 7e1924c9: FIXED (D16). The NOTCH3 output becomes targeted familial-variant testing (detected). The
  criterion label adds pre-test counselling and consent; tier stays required. New must: pre-test
  counselling and consent, including the implications for his three children.

### P07 (41 F, cardioembolic PCA infarct, AF on ILR)
- 895b9b5c: FIXED (class LIT).
- a219ebf2: FIXED (D12). accepted[0] becomes "probably cardioembolic ... not migrainous infarction
  (an alternative cause is present)" (label change). REQ0 is reworded. The DOAC must is unchanged.

### P08 (29 F, MELAS m.3243A>G)
- 6ee45bc0, 252c9961: FIXED (class LIT; no literature criterion or follow-up left).
- 64c11ceb: FIXED in part, DECLINED in part (D11). PRO0 becomes valproate only, on patient-specific
  grounds (POLG caution, alternatives, pregnancy potential). Metformin moves to REQ4 as a
  preference. DECLINED: removing the valproate restriction for her.
- 7dd02d6c: FIXED (D11). Delete PRO1 (triptan and ergot prohibition); this overturns Oct Q3 on the
  2026 consensus.
- f5f97597: FIXED (D11). Crit+ `action-eeg` (recommended; analyze_eeg eeg_type routine, ambulatory
  or video). Add a routine-EEG follow-up with the same findings as the stored ambulatory and video
  records. Not in the stop rule.

### P09 (36 M, hemiplegic migraine, 4 mm MCA aneurysm)
- 8d56a61f: FIXED (class LIT).
- befb9ef9: FIXED (D13). accepted[0] "Hemiplegic migraine (probable sporadic, ICHD-3 1.2.3)"
  becomes "Sporadic hemiplegic migraine (ICHD-3 1.2.3.2)"; the rest is kept (label change).
- Class TIA-CERT (D4): PRO1 becomes the reworded prohibition (five stereotyped attacks).

### RM11 (26 F, hemiplegic attack with seizures, ED at 3 h)
- 27cd7328: FIXED (class LIT).
- 1ea8561d: FIXED (D15). encounter_type becomes emergency. Crit+ `action-arterial-imaging`
  (required; MR_angiography, or order_ct_scan angiography true), in the stop rule. Add an MRA
  follow-up (normal). initial_tool_outputs.ct becomes a stroke-protocol CT with
  angiography_findings (fallback ct set to null). Delete avoided_actions[0] (CT waste). New musts:
  acute stroke pathway, and observation with seizure treatment.
- 0efba9dd: FIXED (D15). clinical_assessment findings[4] and the impression state only the
  documented history. accepted[0] becomes the D15 label (probable 1.5.2; suspected 1.4.4; label
  change). REQ0 has the same certainty plus confirmation on follow-up. Differential focal epilepsy
  key_features: "not excluded by focal slowing alone".
- f1d9b692: FIXED (D3). REQ2 is canonical. PRO1 becomes "...offer a copper IUD or a levonorgestrel
  IUS (or DMPA with condoms), since topiramate weakens pills and the implant". Initial
  interactions[0] gets the any-dose caution.

### RS11 (39 M, sporadic hemiplegic migraine, blackout in attack 2)
- 19601077: FIXED (D10). Crit+ `action-ecg` (required; analyze_ecg), in the stop rule, with a new
  initial ecg output (normal, no Brugada pattern, no pre-excitation). A witness account is added to
  the clinical assessment. accepted[0] drops "all secondary causes excluded" (label change). KCE[2]
  is reworded.
- 91145af1: FIXED (D7, D10). MRI and MRA are already credited. The ECG is now a criterion.
- Class TIA-CERT (D4): PRO1, the TIA prohibition, becomes the D4 conditional must.

### S01, S02, S03, S04, S05, S08, S09, S11 (typical aura)
- S01 a7893337, S02 9328b8dc, S03 eed597bc, S04 b33228a7, S05 f65505f9: NO-ACTION (approvals).
- S08 a36f4096: FIXED (class LIT). 69bca92e: NO-ACTION.
- S09 70750e29: FIXED (class LIT). 96e9ad91: NO-ACTION. Class TIA-CERT (D4): PRO0 becomes the
  reworded prohibition (episode 4 years ago with aura features, identical since).
- S11 4929a69f: FIXED (class LIT). f6ee93eb: NO-ACTION.
- S01-S05 have no class finding and no change. S08 and S11 have no other class finding.

### S06 (30 F, postpartum, breastfeeding)
- 72ca20f5: FIXED (class LIT). No class finding: REQ3 lists the implant for contraception while
  breastfeeding, without topiramate, which is correct (UKMEC 2).

### S07 (40 F, Yasmin, rizatriptan)
- b32b7c1a: FIXED (class LIT).
- 801e6db7: FIXED (D3). REQ3 is canonical. REQ0's switch list (implant included) concerns the aura
  and stays.

### S10 (34 F, MIDAS IV, partner vasectomy)
- 5b8ab438: FIXED (D3). REQ2 is canonical plus the vasectomy condition (sole partner, azoospermia
  confirmed). FU0 warnings[0] gets the any-dose caution.
- 335b1fbd: ALREADY-FIXED (D7). The drug check is recommended, so it is credited and never extra.
- Label "preventive therapy indicated" kept (AHS offer threshold; D8).

## 4. CENTRAL requests

1. Criteria pack `dataset-generation/criteria_packs/MIG-AURA.md` (the lead or orchestrator, after
   the workers finish):
   - Section 4, topiramate: replace "(IUD or implant ...)" with the D3 fact.
   - Section 4, antithrombotics: add the D4 conditional rule.
   - Section 4, CADASIL/MELAS: triptans not contraindicated in MELAS ([MELAS_2026]); valproate
     restricted in POLG and avoided when alternatives exist; metformin as a preference.
   - Section 2: P02 MRI required and ILR removed; P01 MRA required; P04 MRI required and NOTCH3
     recommended; RS11 ECG required; P08 EEG recommended; RM11 arterial imaging required; P05
     INR/CBC labs required.
   - Section 3: CT is not waste in an ED presentation within the stroke window (RM11).
   - Section 8: add `[FSRH_DI_2022]` and `[MELAS_2026]`, and NICE CG109 / NG128 / Powers 2019 as
     text sources.
2. `condition_tool_guidance.yaml` / `test_guidance_claims.py` (maintained centrally after the
   round). Counts change:
   - MRI required in 6 cases becomes 8 (P02, P04 added), recommended in 11 becomes 9.
   - MRA required in 3 becomes 5 (P01, RM11 via arterial imaging).
   - ECG: P08 recommended and RS11 required (claim "29 of 30 have no ECG" becomes 28).
   - EEG: RM11 required and P08 recommended (claim "29 of 30 have neither" becomes 28).
   - Labs: P05 coagulation and CBC required (claim "no case requires routine blood tests" needs
     wording: a safety INR in an over-anticoagulated patient).
3. Synonyms: none needed. Label changes (accepted[0] only) are recorded for the review app: M03,
   M04, M06, M08, P01, P02, P05, P07, P09, RM11, RS11. Each new label is a correct statement of the
   same entity and code. Check with `apply_diagnosis_synonyms.py --check --conditions
   migraine_with_aura` that the synonym lists are unchanged.
4. Scorer (existing item, re-raised): RM11 now says "probable" and "suspected". If the scorer's
   denial-clause handling treats "suspected" as hedging, check that "sporadic hemiplegic migraine
   with migralepsy" still scores. Run `DiagnosisCriterion.matches` on that answer after the edit.

## 5. Open questions

None for Andrea. Every point was decidable from the guidelines above. Residual items for the
physicians at re-review:
- P02 and P05: the antithrombotic musts are now conditional on the reassessment. A reviewer may
  prefer a firmer line once the work-up is complete.
- P08: the exact wording of the valproate statement in [MELAS_2026] was not visible in the
  searchable text. The patient-specific prohibition does not depend on it (POLG caution plus MHRA
  pregnancy rules).

<!-- PLAN COMPLETE -->
