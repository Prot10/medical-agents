# PD round plan (November 2026)

Lead plan for PD-M01..M05, P01..P04, RM01..RM05, RP01..RP05, RS01..RS05 and S01..S06, written
16 Nov 2026.
- Decisions and reasons: `plans/PD-decisions.md`. D1..D32 below refer to its entries.
- Notes: 47, all from R1. No PD case is approved (`work/approved.txt`).

Cases read in full: M03, RP01, RM04 and RS02. Read in part (exam, MRI impression, musts,
differential): every other case, through the scripted dumps.

Scripts (`/home/aprotani/review-round-2026-11/work/scratch/pd-lead/`):

| file | content |
|---|---|
| `survey.txt` | every criterion, avoided action, constraint, stop rule, must and prohibition |
| `classes_pd.py` / `classes_out.txt` | class measures over the 30 |
| `mri_refs.py` | MRI mentions in evidence, differential and musts of the MRI-optional cases |
| `exams.txt` | the neurological exams |

The 600-case counts were run inline.

Workers:
- Edit through `case_io` only.
- After each case, run `perfect_agent.py CASE -v` and `case_io.py check CASE`. After any MRI
  edit, also run `mri_probe.py`.
- Keep every `criterion_id`. New ids are given below.
- English in the case's spelling. No em dashes in new text. No review-process text in `metadata`.
- After any `rejected` or `accepted[0]` edit, test the listed answers with
  `DiagnosisCriterion.matches`.
- Update `metadata.revision_reason` and `metadata.last_revised` ("2026-11-16") to describe the
  case as edited.

## 1. Governing guidelines and canonical facts

| Key | Source | Governs |
|---|---|---|
| `[Postuma_2015]` | MDS PD criteria, Mov Disord 2015;30:1591-1601 | Parkinsonism = bradykinesia (with decrement) + rest tremor and/or rigidity (velocity-independent; cogwheeling alone does not count). Established = ≥2 supportive, no red flag. Probable = red flags counterbalanced, one supportive per red flag, at most 2. The OH red flag excludes OH explained by medication. |
| `[NICE_NG71]` | NICE NG71 (2017) | 1.2.9 no structural MRI to diagnose PD; 1.2.10 MRI may be considered for other parkinsonian syndromes; 1.2.6 DaT-SPECT when ET cannot be clinically separated; 1.3.1 levodopa first line when motor symptoms affect quality of life; ICD and EDS warnings with agonists |
| `[Marshall_2009]` | Mov Disord 2009;24:500-508 | An abnormal DaTscan is a presynaptic deficit, not specific for PD |
| `[Schwarz_2014]` | PLoS One 2014;9:e93814 | Swallow-tail sign; not a diagnostic criterion |
| `[Wenning_2022]`, `[Hoglinger_2017]`, `[DLB_2017]` | MDS MSA, MDS PSP, DLB consortium | Mimic cases; no levodopa-resistance requirement for probable PSP-RS or for established MSA via the cerebellar route |
| `[ESC_2018]` | ESC syncope 2018 | 12-lead ECG in every syncope; orthostatic measurement |
| `[ESC_SVT_2019]` NEW | Brugada J et al. Eur Heart J 2020;41:655-720 | EPS risk stratification of pre-excitation; symptomatic pre-excitation (RP01) |
| `[EMA_Domperidone_2014]` NEW | EMA Art. 31 referral EMA/465179/2014; MHRA DSU May 2014 | Domperidone: nausea and vomiting only, ≤1 week, ≤10 mg three times daily; contraindicated with cardiac conduction disease, cardiac disease, QT drugs, potent CYP3A4 inhibitors, severe hepatic impairment |
| `[ACG_Gastroparesis_2022]` NEW | Camilleri M et al. Am J Gastroenterol 2022;117:1197-1220 | Gastroparesis management (diet, glycaemia, prokinetics by specialist) |
| `[EASL_ERN_Wilson_2025]` | J Hepatol 2025;82:690-728 | Wilson considered in otherwise unexplained neurological disease; first step ceruloplasmin + 24-h urinary copper |
| `[Tinazzi_2022]` NEW | Mov Disord Clin Pract 2022;9:594-603 | Pisa syndrome >10°; lateral trunk flexion 5-10° |
| `[Follett_2010]` NEW | N Engl J Med 2010;362:2077-2091 | GPi vs STN DBS |
| `[CAPSIT_PD_1999]`, `[Litvan_2012]` | as in the pack | DBS candidacy, PD-MCI |
| `[ATA_2014]` NEW | Jonklaas J et al. Thyroid 2014;24:1670-1751 | Levothyroxine absorption, timing, TSH recheck at 6-8 weeks |

Facts every worker uses:
- **F1.** PD is a clinical diagnosis. In clinically typical PD, structural imaging is optional (D1).
- **F2.** One red flag needs one supportive criterion. Never write "counterbalanced by two" as if
  two were needed.
- **F3.** No routine domperidone substitute. Use the D4 canonical text.
- **F4.** Musts and evidence lines cite only patient data and the results of required or
  recommended criteria. An optional result is written "if obtained".
- **F5.** A condition that is true in the case (coexisting) is never in `diagnosis.rejected` (D30).

## 2. Classes

### C1 TIER-MRI and STOP-RULE: structural imaging in typical PD (D1)

**Notes.**
- 9d6d3209 RS04, 7d906e55 RS05, f4766ad1 S01, 9e04baa6 S02, 0dcbe488 S03, 5ee462a7 S04;
- e29754f8 S05, 69817fd8 RM05, 5dcbd891 S06 (CT).

**Measured.** MRI is required and in the stop rule in 29 of 30 cases; CT in S06.

**Fix: imaging becomes optional and leaves the stop rule** in the 15 typical cases:
- RS04, RS05, S01, S02, S03, S04, S05, RM05, S06 (noted);
- M04, M05, RM03, RM04, RS01, RS03 (class: asymmetric rest-tremor PD, no red flag, no atypical
  sign, no structural history).

**Stays required (reason):**

| case(s) | reason |
|---|---|
| M01, M02, M03 | bilateral, near-symmetric, gait-onset parkinsonism without rest tremor in older diabetics; vascular parkinsonism and NPH are in the differential |
| P01, RP03 | MSA MRI markers are MDS 2022 criteria |
| P03 | midbrain atrophy is supportive in MDS 2017 PSP |
| P02 | structural imaging in a dementia work-up |
| P04 | onset at 42 |
| RM01 | new episodic oculomotor and speech symptoms |
| RM02 | encephalitis 18 months ago |
| RP01, RP02 | early orthostatic hypotension raises the MSA question |
| RP04 | pre-DBS |
| RP05 | vascular question: prior TIA, Fazekas 2 |
| RS02 | VP shunt |

Canonical label and rationale: D1.

**Resulting stop rules.**
- Empty `required_before_assessment`, `max_additional_actions` 2: S01-S06, RS03, RS04, RS05, M04,
  M05, RM03, RM04, RS01 (14 cases with no required criterion).
- RM05: [`action-2-check-drug-interactions`].

**Evidence lines** in the 15 cases (`mri_refs.py` lists them):
- the MRI KCE line takes the D1 form;
- differential key_features lead with clinical features, with MRI as "and, if imaged, ...".

No must in the 15 cites the MRI (checked).

Across 600: the MRI-as-diagnosis question is PD-specific. No other condition was measured.

### C2 SEQUENCE (D2)

**Notes.** e29754f8 S05, 5dcbd891 S06.

**Measured.** The soft constraint "MRI before DaTscan" is in 13 cases, all PD:
M01, M02, M03, M04, P02, P04, RM02, RM03, RM05, RP05, RS01, S05, and S06 (CT).

**Fix.**
- Delete it in all except RP05.
- RP05 keeps it with the reason given in D2 and an empty citation list.
- RM05's constraint goes anyway with its DaTscan criterion (D17).

### C3 DX-CERTAINTY: metoclopramide triad (D3)

**Notes.** ee26c7b1 M01, e851351e M02, 811211a3 M03.

**Fix in all three.**
- New `accepted[0]` (CENTRAL 1).
- Canonical REQ[0] and REQ[2], plus the new prohibition.
- The DaTscan rationale and KCE say "supports degenerative parkinsonism, not specific for PD".
- The stop rule is unchanged (no tool for a later visit).

### C4 MUST-WRONG: domperidone (D4)

**Notes.** 004770c3 M01, 102d4199 M02, d0fa04ff M03.

**Measured.** "Domperidone ... ECG/QTc" appears in M01, M02, M03 and RM05 (REQ[1] and the
drug-interaction output; RM05 also in the criterion expected_evidence). Across 600, no other case.

**Fix.** The D4 canonical text in all four. RP02 PRO[1] stays.

### C5 SCENARIO: MDS rigidity and bradykinesia in the exam (D5)

**Notes.** 8cd68b0a M01, 92ca20f9 RM04.

**Measured.**
- No rest tremor on exam with cogwheel-only wording: M01, M02, M03, P02.
- Motor exam without decrement among the PD-labelled cases: RM04 only.

**Fix.** The D5 canonical sentences.

### C6 NEW:near-duplicate-case (D6)

**Notes.** 0d250e2e M02, 36b4026f M03.

**Measured.**
- Same label, tiers and stop rule.
- HPI Jaccard 0.30-0.34.
- One shared verbatim exam sentence between M01 and M03.

**Fix.** Distinct chief complaints for M02 and M03, no verbatim shared exam sentences, and a
distinct `metadata.primary_teaching_point` (the D6 axis).

### C7 REPORT-CONTRADICTION and SCENARIO: family history and handedness (D7, D8)

**Notes.** 82b35cac M02, b468a5e6 M05.

**Measured.**
- Family-history negation against an affected relative: M02. P04 is close and is extended.
- Handedness against writing hand: M05; S06 is extended.

### C8 DX-CERTAINTY: swallow-tail (D9)

**Note.** d579cd94 M04.

**Measured.** Evidence lines mentioning nigrosome or swallow-tail: M04, RM04, RM05, RP02, RP05.
Across 600: 9 cases mention the sign (NPH-M05 and NPH-P02 outside PD; they are not PD-diagnostic
lines, so the NPH lead may ignore them).

**Fix.** The D9 wording.

### C9 AVOIDED-MISSING and TIER: ECG (D10, D21)

**Note.** caaaca18 P01.

**Measured.**
- ECG waste in 18 cases. Of these, only P01 has near-syncope and recurrent falls.
- P02 demands an ECG in a must with no criterion and no stored ECG.
- RP01: ECG recommended, now required.

**Fix.** P01 recommended `ecg-baseline`; P02 recommended `ecg-before-chei`, each with a stored
ECG; RP01 per D21. The other 17 wastes stay, as checked in D10.

### C10 MUST-WRONG and UNSOURCED-RULE: levodopa trials, propranolol, levothyroxine, first-line choice (D11, D13, D15, D18)

**Notes.** 4d967b13 P03, 722c125f RP03, 3ed94a70 P04, 32a0532b RM03, 8de3e101 RM05.

**Measured.**
- "1000 mg/day" musts: P01, P03, RP03. P01 is symptomatic, so it is kept.
- "levodopa does not treat": M04, RM03.
- "are all options": P04 only (600-wide).

### C11 MUST-WRONG: psychiatric, orthopaedic, cardiac, surgical and device musts (D14, D16, D21-D24, D26, D27)

**Notes.**
- c2e6d577 RM02, 1d3af06d RS01 (bipolar; measured: only these two PD cases have bipolar
  disorder);
- 23ea4603 RM04; 8352e97d RP01; d6571979 and f4a8e329 RP02; 8069f8d7 RP03; 7ebc619e RP04;
- 582e1ee0 RS01; 0d17ed0e and 6029713d RS02.

Programmable valve: 32 cases across 600 (31 NPH, FEPI-TEMP-RM01), PD 1. See CENTRAL 6.

### C12 DX-CERTAINTY and DIFFERENTIAL (D19, D20, D25, D31)

**Notes.** d3fc1f93 and cfc0fa20 RM01, 07401754 RM02, 61f2065e RP05.

### C13 SCENARIO: trunk posture (D28)

**Note.** ec3fb0d3 RS03. "Pisa" appears only in RS03 (6 fields).

### C14 Rejected labels true in the case (D30; no note of its own, from D16, D21, D26 and D31)

**Measured** (rejected list against coexisting conditions):
- RP01 `wolff parkinson white` and `WPW`;
- RM04 `adhesive capsulitis` and `frozen shoulder`;
- RM02 `post encephalitic parkinsonism` and `postencephalitic`;
- RS01 `lithium induced tremor`;
- M02 `essential tremor`.

**Fix.** Remove these. Keep DIP rejected in M01-M03 (D3).

### C15 NO-ACTION

**Note.** 5b975043 P02.

## 3. Per-case index (all 30; none approved)

Rulings: FIXED, DECLINED, ALREADY-FIXED, CENTRAL, NEEDS-ANDREA, NO-ACTION. "Class" lines are
findings with no note in that case.

### PD-M01
Notes:
- 8cd68b0a-483a-4854-bbe8-0f0f333fdef8: FIXED (D5). Motor exam gets the canonical velocity-independent rigidity sentence
  (left > right).
- ee26c7b1-7dc8-432c-81b6-c995e7f1706d: FIXED (D3). New `accepted[0]` (CENTRAL 1); REQ[0] and REQ[2] canonical; new
  prohibition; DaTscan rationale and KCE "not specific for PD".
- 004770c3-3d36-49bd-a09c-1d02f49ee482: FIXED (D4). REQ[1] canonical; drug-output alternatives, interactions and warnings
  rewritten.

Class:
- MRI stays required.
- Delete the MRI->DaTscan constraint (D2).
- Stop rule [MRI, DaTscan, drug check] unchanged.

### PD-M02
Notes:
- e851351e-a160-401d-b66b-4dd35f9385e5: FIXED (D3), as M01, with "RBD and hyposmia are not drug effects".
- 102d4199-e441-47cf-88ff-b80592a5f40b: FIXED (D4). REQ[1] canonical, keeping "monitoring glucose on glipizide while the
  prokinetic changes".
- 0d250e2e-635e-4084-9473-f24f7688b9f4: FIXED (D6). New chief complaint (slowness and low mood); distinct teaching point.
- 82b35cac-4e68-49bd-aeb4-38684a440d15: FIXED (D7). `family_history[3]` becomes "No other family history of movement
  disorders".

Class:
- D5 rigidity sentence (no rest tremor; "subtle cogwheel ... with reinforcement" becomes
  velocity-independent rigidity, right > left).
- Delete the constraint (D2).
- Remove `essential tremor` from rejected (D30).

### PD-M03
Notes:
- 811211a3-6549-4b38-b840-788a6526589b: FIXED (D3), with the DaTscan as the only marker.
- d0fa04ff-a6ce-455e-877d-d15fb1499af7: FIXED (D4). REQ[1] canonical, keeping "watching his weight"; age 75 noted.
- 36b4026f-0ccc-4ce0-883d-ef49a9ca8bcf: FIXED (D6). New chief complaint (stiffness and smaller handwriting); rewrite the
  rigidity sentence it shares with M01; distinct teaching point.

Class: D5 rigidity; delete the constraint (D2).

### PD-M04
Notes:
- d579cd94-1eab-44e1-a747-55342f667e32: FIXED (D9). KCE[3] rewritten in the non-specific "if obtained" form.

Class:
- MRI optional and out of the stop rule, which becomes empty (D1).
- MRI wording in the KCE and in differential entries [3] and [4].
- Delete the constraint (D2).
- REQ[2] propranolol canonical (D15; HR 62; drop "which levodopa does not treat").

### PD-M05
Notes:
- b468a5e6-6b4b-4443-9059-26dda843bb31: FIXED (D8). `demographics.handedness` "left"; HPI "left-handed".

Class:
- MRI optional; stop rule empty (D1).
- MRI wording in KCE[3], KCE[4], differential [0], [2], [3] and red herring [0].
- PSG stays recommended.

### PD-P01
Notes:
- caaaca18-6421-457f-b7b3-b7ca2eee2316: FIXED (D10). Delete `avoid-waste-5-analyze-ecg`; add recommended `ecg-baseline` with
  a stored initial ECG.

Class:
- MRI required (MSA markers).
- REQ[1] levodopa trial kept (symptomatic, D11).

### PD-P02
Notes:
- 5b975043-c475-4614-afb7-a073d22fb33e: NO-ACTION (D29).

Class:
- D5 rigidity wording (no rest tremor; DLB parkinsonism).
- Add recommended `ecg-before-chei` with a stored ECG (D10).
- Delete the constraint (D2). MRI required.

### PD-P03
Notes:
- 4d967b13-bbc4-4ec6-bef0-d18402679ec8: FIXED (D11). REQ[3] conditional canonical; REQ[0] drops the missing-trial clause.

Class: MRI required.

### PD-P04
Notes:
- 56aee7f4-5ebd-4591-9c75-21801a942cc6: FIXED (D12). Labs optional and out of the stop rule (now [MRI]); REQ[1] canonical;
  copper evidence lines in "if obtained" form.
- 3ed94a70-4c7c-437f-ad9c-ca01654d7fd9: FIXED (D13). REQ[2] and KCE[5] canonical.

Class:
- `family_history` wording (D7).
- Delete the constraint (D2).
- MRI required (onset 42).

### PD-RM01
Notes:
- d3fc1f93-df7b-4a01-939e-b149828b4d72: FIXED (D19). New `accepted[0]` (CENTRAL 1); REQ[0] canonical.
- cfc0fa20-217c-4158-b4ae-25feba8a247e: FIXED (D20). Differential entry for posterior-circulation TIA, low; conditional must.

Class: MRI required.

### PD-RM02
Notes:
- 07401754-64db-4495-be50-0533ab76ab08: FIXED (D31). Differential key_features; MRI rationale; must to review the outside
  records; remove the two rejected labels (D30).
- c2e6d577-589e-4342-a044-87fd58fcf3ce: FIXED (D14). Canonical psychiatric must added to REQ[2] or as its own must.

Class:
- MRI and DaTscan required.
- Delete the constraint (D2).

### PD-RM03
Notes:
- 32a0532b-54c4-4fb1-b6ba-9286d71c43fd: FIXED (D15). REQ[2] canonical (HR 58); PRO[2] kept.

Class:
- MRI optional; stop rule empty (D1).
- MRI wording in KCE[5] and differential entries [3], [4] and [5].
- Delete the constraint (D2).

### PD-RM04
Notes:
- 23ea4603-bba3-476f-924e-c64cd9855125: FIXED (D16). REQ[1] canonical; delete PRO[0]; remove `adhesive capsulitis` and
  `frozen shoulder` from rejected; align the differential and red herring [0]; add passive range
  to the exam.
- 92ca20f9-f0d6-42d5-ba55-87a4e151622f: FIXED (D5). Decrement sentence in the motor exam.

Class:
- MRI optional; stop rule empty (D1).
- KCE[3] swallow-tail wording (D9).
- MRI wording in differential entries [4], [5] and [6].

### PD-RM05
Notes:
- 69817fd8-0b8e-470f-8db8-727b6e0cb4f7: FIXED (D1). MRI optional; stop rule [drug check]. KCE[4] and differential entry [5]
  in the D1/D9 form.
- eac7edfb-b926-489a-bdae-e1bdce65c775: FIXED (D17). Delete `action-7-order-advanced-imaging` and its constraint; add
  `avoid-waste-datscan`; keep the stored DaTscan.
- 8de3e101-cf91-45eb-b37b-bc1bbbc66f68: FIXED (D18). REQ[4] canonical.

Class: REQ[1], the drug output and the action-2 expected_evidence on domperidone (D4).

### PD-RP01
Notes:
- 8352e97d-a39e-479d-8984-86f19f6c59fd: FIXED (D21).
  - ECG required and in the stop rule [MRI, ECG].
  - New recommended `eps-accessory-pathway` with a stored low-risk EPS follow-up.
  - REQ[1] and PRO[2] canonical; KCE[3] and differential [1] rewritten.
  - Remove `wolff parkinson white` and `WPW` from rejected.

Class: REQ[0] "two supportive" wording (F2).

### PD-RP02
Notes:
- d6571979-2a68-4ef2-ba3c-a38b80c0b71d: FIXED (D22). MIBG optional; REQ[0] canonical; MIBG evidence "if obtained".
- f4a8e329-6bfc-4f32-b39c-20cd00383c5a: FIXED (D22). KCE[1] canonical; new must for the cardiology medication review and
  repeat orthostatic measurement.

Class: KCE[3] swallow-tail (D9). MRI required.

### PD-RP03
Notes:
- 722c125f-0a79-41ae-92e7-53e7eedc5d1b: FIXED (D11). REQ[4] conditional canonical; REQ[0] notes the cerebellar route.
- 8069f8d7-f9ef-4d36-a91e-9923071e7b87: FIXED (D23). The amlodipine clause in REQ[2]. The note is anchored on REQ[3], but its
  target is REQ[2].

### PD-RP04
Notes:
- 7ebc619e-4a7f-47aa-bf25-ff5db7f6379b: FIXED (D24). REQ[2] canonical; REQ[3] "does not exclude DBS".

Class: the RP04 tremor history stays (D15).

### PD-RP05
Notes:
- 61f2065e-38b7-4007-b3a2-b84430cb651c: FIXED (D25). DaTscan optional; REQ[1] without the DaTscan; differential aligned; soft
  constraint kept.

Class: KCE[3] swallow-tail (D9). MRI required.

### PD-RS01
Notes:
- 582e1ee0-bba8-4bcf-b975-dc9c7cd2ea7f: FIXED (D26). REQ[1] canonical; remove `lithium induced tremor` from rejected;
  differential "possible contributor".
- 1d3af06d-d343-4919-9b88-4b2f0f80ae98: FIXED (D14). REQ[3] canonical.

Class:
- MRI optional; stop rule empty (D1).
- KCE[4] and differential entries [3] and [5].
- Delete the constraint (D2).

### PD-RS02
Notes:
- 0d17ed0e-8fa2-4edf-8aca-bdbefb964bba: FIXED (D27). PRO[1] canonical; red herring and differential aligned.
- 6029713d-ef69-49b2-8f82-cf3380c1a7b6: FIXED (D27). REQ[1] canonical (pre-MRI valve check).

Class: MRI required.

### PD-RS03
Notes:
- ec3fb0d3-edaa-4ec9-8a89-ef737d3a9f0d: FIXED (D28). Exam: lateral trunk flexion of about 8 degrees, reversible. "Pisa
  syndrome" replaced in REQ[4], differential [1], KCE[3] and metadata.

Class:
- MRI optional; stop rule empty (D1).
- KCE[2] and differential entries [0], [1] and [6].

### PD-RS04
Notes:
- 9d6d3209-37ba-49c1-b7cb-0e37160624e2: FIXED (D1). MRI optional; stop rule empty; KCE[3] and differential entries [2] and
  [3].

### PD-RS05
Notes:
- 7d906e55-4818-4eaa-b036-d819fc5c57ec: FIXED (D1). MRI optional; stop rule empty; KCE[4] and differential entries [3], [4]
  and [5].

### PD-S01
Notes:
- f4766ad1-4481-43c8-89fe-fb828b7b07e7: FIXED (D1). KCE[4] and differential entries [2], [3] and [4].

### PD-S02
Notes:
- 9e04baa6-725a-41b1-b868-dca3f91bd599: FIXED (D1). KCE[3] and differential entries [2], [3] and [4].

### PD-S03
Notes:
- 0dcbe488-5846-4a28-92ce-20760b496bda: FIXED (D1). KCE[4] and differential entries [2], [3] and [4].

### PD-S04
Notes:
- 5ee462a7-598c-4fbb-8638-ae9ea3fcc1ba: FIXED (D1). KCE[3] and differential entries [2] and [3].

### PD-S05
Notes:
- e29754f8-d2df-43bf-9977-6b7cee9652ed: FIXED (D1, D2). MRI optional; stop rule empty; delete the MRI->DaTscan constraint;
  KCE[4] and differential entries [2], [3] and [4].

### PD-S06
Notes:
- 5dcbd891-3b5f-4672-89f1-bafa55583171: FIXED (D1, D2).
  - CT optional and out of the stop rule (now empty).
  - Delete the CT->DaTscan constraint.
  - Keep `panel_required_exemptions.analyze_brain_mri`.
  - KCE[4] in the "if obtained" form.

Class: handedness made left (D8).

## 4. CENTRAL requests

1. **Synonyms and labels** (`diagnosis_synonyms.yaml`, `apply_diagnosis_synonyms.py --check`).
   New `accepted[0]` in M01, M02, M03 (D3) and RM01 (D19); codes unchanged. Confirm that the
   synonym guard keeps the G20.A1 labels after the new `accepted[0]`, and that "Parkinson's
   disease unmasked by metoclopramide" still matches.
2. **Pack** (`dataset-generation/criteria_packs/PD.md`).
   - Section 2 rewritten to the new tiers:
     - MRI required in 15 and optional in 15 (D1);
     - DaTscan recommended in none, RP05 optional, RM05 waste;
     - MIBG RP02 optional;
     - Wilson labs P04 optional;
     - ECG recommended in P01 and P02, required in RP01;
     - EPS recommended in RP01.
   - Section 5: one soft constraint, RP05 only.
   - Section 7 is unchanged.
   - Add the keys `[ESC_SVT_2019]`, `[EMA_Domperidone_2014]`, `[ACG_Gastroparesis_2022]`,
     `[Tinazzi_2022]`, `[Follett_2010]` and `[ATA_2014]` with the references from section 1.
   - State F1-F5.
3. **Guidance answers** (`build_condition_tool_guidance.py`, `condition_tool_guidance.yaml`,
   `test_guidance_claims.py` PD rows). The MRI answer ("Structural imaging remains required ...
   MRI in 29") and the ECG and labs counts become false. Regenerate from the edited cases.
4. **Generator** (`dataset-generation/config/conditions.yaml`, parkinsons block). Change
   `required_modalities: [MRI]` to MRI conditional on atypical features. The current tests pass
   with an optional MRI criterion.
5. **Benchmark property.** 14 PD cases have no required criterion (D1). The scorer gives 1.0 to
   a correct clinical diagnosis with no test. `test_no_case_has_a_free_required_set` skips such
   cases by design. Record this in the paper's description of the PD condition. No code change is
   requested.
6. **NPH lead.** Pre-MRI verification of programmable shunt valves (D27): 31 NPH cases mention
   programmable valves.

## 5. Open questions

- None blocks the work.
- For Andrea's information:
  - (a) the 14 zero-required PD cases (CENTRAL 5);
  - (b) the optional composition choice in D6: M03 could be replaced by a different
    dopamine-blocker scenario in a later round. It is kept as the graded triad's
    DaTscan-only member.
- For the physicians at re-review:
  - RP01 EPS result (invented, low-risk);
  - P04 Wilson labs optional rather than recommended (D12).

<!-- PLAN COMPLETE -->
