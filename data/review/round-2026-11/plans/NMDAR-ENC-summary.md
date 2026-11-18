# NMDAR-ENC: condition audit summary, November 2026 round (17 Nov 2026)

Scope: the 30 NMDAR-ENC cases, against `NMDAR-ENC.md` (plan, K1-K18) and
`NMDAR-ENC-decisions.md` (D1-D35). Base for "before" counts: commit 06b74446. Scripts:
`/home/aprotani/review-round-2026-11/work/scratch/nmdar-auditor/` (`classes_nm.py`,
`beforeafter.py`, `leak_t0_nm.py`, `leak_out_nm.py`, `xmod_nm.py`, `probe_body.py`,
`fix_ddi_dx.py`, `log_ddi.py`).

## 1. Classes found and how they were fixed (counts over 30 cases, before -> after)

| class | what | before | after | how |
| --- | --- | --- | --- | --- |
| K1 | MRI contrast header (notes S03, S04, S06, S09, S10 and the MRI sub-points of 9 verdicts) | class MRI-CONTRAST | 0 | ALREADY-FIXED by commit 71517e55. `mri_probe` is clean in all 30. |
| K2 | Must 1 has the unsourced 72-hour repeat-PCR rule | 28 | 0 | Graus 2016 wording. RS03 and RP02 use the early-LP form. |
| K2 | Must 1 has no empirical bacterial meningitis cover | 30 | 0 | Regimen chosen by allergy and age (D3). |
| K3 | "5 to 7 exchanges" anywhere in the case (musts and drug-interaction `alternatives`) | 30 | 0 | Now "5 to 10 sessions every other day" (Abboud 2021). |
| K3 | Musts say methylprednisolone "1 g daily for 5 days" | 29 | 0 | Now "3 to 7 days". RP02 keeps ASCO's "3 to 5 days", which lies inside Abboud's 3-7. |
| K3 | Combined versus sequential start, and the IVIG/PLEX trade-off | 30 | 0 | Matches the per-case table: 4 sequential (P01, P04, RM03, RP01); PLEX preferred in 8 (M01, M05, P01, P04, RP01, RP02, RS02, RS04). |
| K4 | No bridging must | 29 | 0 | Canonical must. RP02 already had an oral taper. |
| K5 | Escalation at "10 to 14 days" | 30 | 0 | Now 2 to 4 weeks. |
| K5 | No cyclophosphamide dose | 30 | 0 | Now 600 to 1000 mg/m² monthly. |
| K6 | Benzodiazepine-first must without a source | 28 | 0 | Now cites (Lejuste 2016). M01's script hit is a false positive: must 9 carries the citation. |
| K6 | Sodium correction limit without a source | 7 | 0 | Now cites (Spasovski 2014). |
| K7A | Required pelvic-ultrasound criterion without a pelvic MRI alternative | 21 | 1 | The remaining case is M03, excluded by design (D13: there pelvic MRI is the separate characterisation step). |
| K7B/C | Second-line tumour screen after a negative first study | 11 criteria missing | 0 | New criteria with stored reports in M02, P05, RM01, RS04, M05, RS03, RM03, RP01 and RS02; tumour musts reworded. |
| K8 | Resection as a criterion (M01) | - | - | DECLINED (D14). |
| K9 | Paired CSF/serum glucose does not match the labs | 6 | 0 | M01, P01, S01, S02, S03 and S04 now pair with the labs glucose; ratios recomputed and checked. |
| K10 | Measured versus calculated osmolality | 2 | 0 | RP01 286, RS01 274. |
| K11 | Lateralisation discordance (M03, M04) | 2 | 0 | Now stated in a key clinical evidence bullet. |
| K12 | Post-intervention screen contradicts the baseline screen | 3 | 0 | P01, P04, RP01: "unchanged from baseline". |
| K13 | Performance status contradicts gait | 3 | 0 | P06, P08, RM03. |
| K14 | Fever denied in the HPI but febrile on arrival | 2 | 0 | M01, RS04. |
| K15 | Diagnostic certainty before the antibody result | 3 | 0 | P01, P04, RP01. |
| K16-K18 | Case-specific fixes | - | done | RS03 ABG (pH 7.16, FiO2 0.36; the A-a gradient of about 120 mmHg recomputes), RP02 creatinine 1.5 (Cockcroft-Gault 45.7, stated as about 46) and right Babinski, P06 EEG, RP03 PET sentence, RP03 two `harm` avoided actions, RP01 MRA and CSF tissue-based assay, RM01 MOG/AQP4 and ANA, RS02 cultures, RS04 ACE and flow cytometry, P04 optional brain FDG-PET. |
| LIT | Literature criterion or output | 30 | 0 | Class LIT (commit 393c547e). |
| **NEW: DDI-DX** | A drug-interaction output names the case's accepted label ("anti-NMDA receptor encephalitis" or "anti-NMDAR encephalitis") in its D2-antagonist class warning | **18** | **0** | Fixed in this audit (section 4). |

The plan's decisions were checked uniformly with scripts over all 30 cases:
- canonical texts of musts 1 and 2, bridging and escalation;
- the regimen against the allergy list and age;
- the preferred agent and the combined or sequential start against the K3 table;
- the Lejuste and Spasovski citations;
- the K7A pelvic MRI alternative and the K7B criteria.

Structural checks over the same 30 cases:
- every stop-rule id exists and every sequence-constraint id exists;
- no avoided action matches any criterion alternative (checked on `alternatives`);
- tumour follow-ups come before the drug-interaction step in the pathway;
- no new em dash. The only added `—` is a copied MRI string from the MRI-CONTRAST split in RM02.

Two required criteria are not in the stop rule: `check_drug_interactions` in P07 and RP02. This
was already so at 06b74446, by October design: the check is a management step, not needed before
the diagnosis. No change.

Every musts list was also read in full. No must demands a study that no criterion orders. P02's
staging CT and tumour markers have their own recommended criteria. The mammography clause is
held back until CENTRAL 1.

## 2. Note and ruling coverage

- `notes/NMDAR-ENC.json` has 35 notes, all from R2. Each appears in exactly one
  `work/rulings/<CASE>.json`, the case file of its note, with a valid status.
- Rulings per note: FIXED 21, NO-ACTION 11 (the plain approvals of P03, P07, P08, RM02, S01, S02,
  S03, S04, S06, S09, S10), ALREADY-FIXED 3 (S06, S09, S10 MRI contrast). DECLINED 0,
  CENTRAL 0 and NEEDS-ANDREA 0 at note level. The declined and central parts are sub-points of
  FIXED notes and are recorded in each ruling's `reason`.
- Every case changed since 06b74446 beyond the cross-condition classes (all 30) has a log with
  `## Changes`.

### DECLINED sub-points, with reasons
1. **M01, teratoma resection as a recommended `obtain_tissue_diagnosis` criterion.**
   ROUND_POLICY rule 4: treatment is never a tool call. Removal is management and stays in the
   must. The histology does not change the diagnosis, which the CSF anti-GluN1 result makes
   definite (Graus 2016). The stored resection report stays but earns no credit (D14).
2. **RP01, rewriting the phenotype to fit the antibody.** The physician's other option, a
   confirmatory tissue-based assay (Graus 2016), was taken instead. The October phenotype recast
   (October Q1, resting on Graus 2016 and Gresa-Arribas 2014) stands (D17).
3. **RP01, a sequence constraint "vascular imaging before immunotherapy".** Immunotherapy is not a
   criterion, so a constraint cannot reference it. The order is written into must 2 (D18).

### NEEDS-ANDREA
None. For awareness only, from the plan:
- D14 declines a physician request on contract rule 4. Scoring surgical tissue diagnosis would be a
  design change for all tumour conditions.
- Some Abboud 2021 numbers were applied as R2's reading of the paper because the search snippets
  did not reach them: steroids for 3-7 days, cyclophosphamide 600-1000 mg/m², box items 9 and 13.
  A full-text check at the next round would close this.

## 3. Approved cases changed, and why

The approved cases are P03, P07, P08, RM02, S01, S02, S03, S04, S06, S09 and S10. Each was changed
only for real class defects:
- **Template musts** the physician ruled wrong elsewhere (all 11):
  - K2: the 72-hour rule and no bacterial cover;
  - K3: the 5-day steroid course, 5-7 exchanges, and no combined-start reason or trade-off;
  - K4: no bridging must;
  - K5: escalation at 10-14 days with no cyclophosphamide dose;
  - K6: sources missing.
- **K7A pelvic MRI alternative:** P07, P08, RM02, S01, S02, S03, S04, S06, S09, S10. Not P03
  (male).
- **K9 glucose pairing:** S01, S02, S03, S04. The physician asked for this directly in the S03
  and S04 notes.
- **K13 performance status:** P08.
- **DDI-DX leak** (this audit): P03, P07, P08, RM02, S02, S03, S04, S06, S09, S10.

Each log says so.

## 4. Stragglers fixed in this audit

**DDI-DX (D leakage, major, 18 cases).** Cases: P02, P03, P04, P05, P06, P07, P08, RM01, RM02 (two
outputs), RM03, RP01, RP02, S02, S03, S04, S06, S09, S10.
- **The defect:** the D2-antagonist class warning in the drug-interaction output said the
  reactions occur "in anti-NMDA receptor encephalitis" or "in anti-NMDAR encephalitis". Both are
  accepted labels of the case. `check_drug_interactions` can be called on the first turn, so an
  agent could read the answer before ordering any test. The defect was present at 06b74446;
  workers and verifiers did not catch it.
- **The fix:** the phrase now reads "in autoimmune encephalitis". This is the wording the other
  12 cases already use; it is not an accepted label, and the content (Lejuste 2016) is kept.
- **Logged:** under `## Verification` and `## Changes` in each log. No ruling changed, because no
  note asked for this.
- **After the fix:** the leak scan finds no accepted label in any initial, follow-up or fallback
  drug-interaction output of the condition.

## 5. Blind leak pass

- **Turn 0** (`format_patient_info`, medication indications included): no accepted label and none
  of the strings NMDA, GluN1, "autoimmune encephalitis" or teratoma.
  - The result hits are pre-encounter history: P03's prior HSV-1 MRI and CSF PCR, RP01's outside
    low sodium, S03's outside CT and sodium 133, RP02's epidermoid cyst on serial MRI, and past
    PCOS or ovarian cysts. Each is from before the encounter and is not what the case's criteria
    order now.
  - Flagged, not changed: S10 (approved) has the husband asking whether this "could be related to
    an ovarian tumor he read about in the context of 'brain inflammation'". It names no label, but
    it is a strong cue. It was approved by the physician as a realistic detail.
- **Stored outputs:**
  - The only label-naming defect outside CSF and labs was the DDI-DX class above.
  - The CSF and serum antibody results naming anti-GluN1 are Kind 2 (the confirmatory test
    states what it establishes).
  - The MRI impressions "consistent with limbic encephalitis" name a radiological pattern, not an
    accepted label (Kind 2).
  - Drug-interaction outputs repeat no criterion `expected_evidence`. They share phrases with
    musts only where the must is built on the interaction they report (for example RM03's
    osmolality check, the plan's K3 "5 to 10 sessions").
- **Cross-modality synthesis:** no report synthesises across modalities.
  - PET-CT mentions the adnexal teratoma on its own CT component.
  - EEG artifact notes cite the dyskinesias observed by the technologist.
- **Served-answer probe** (`probe_body.py`, 25 cases): every pelvic MRI matches its ultrasound in
  side and size, and every CAP CT matches its pathway. One routing issue was found (CENTRAL C5).

## 6. Label and code changes

None: `accepted[0]`, `icd_codes[0]`, the synonym labels and the `rejected` lists are identical to
06b74446 in all 30 cases.

## 7. CENTRAL requests, consolidated

1. **Vocabulary: breast imaging** (RM03, RS02, Abboud 2021 box 1 item 6).
   - Add `order_body_imaging` study `breast_mammography` (CPT 77067), and possibly `breast_MRI`, to
     `costs.yaml`, with a library normal in `fallback_library.yaml`, the
     `review_api/services/tool_io.py` mirror and `TOOL_PARAMETER_VOCABULARY.md`.
   - Then add a recommended mammography criterion with a stored normal report and a must clause
     in RM03 and RS02.
2. **Vocabulary (optional): a CSF tissue-based assay.** Add an `analyze_csf` special test such as
   `neuronal_surface_tissue_assay`. In the interim, RP01 reports it inside `NMDAR_antibodies`.
3. **Criteria pack** `dataset-generation/criteria_packs/NMDAR-ENC.md` and the `conditions.yaml`
   template musts: rewrite to the plan.
   - Pelvic MRI alternative; demographic second-line tumour screen; FDG-PET optional; cultures when
     fever has a systemic source; canonical musts 1, 2, bridging and escalation; Lejuste and
     Spasovski.
   - Allow-list keys `[ESCMID_meningitis_2016]` and `[Gulati_2021]`. Gulati is the 2021
     AHA/ACC chest pain guideline, Circulation 2021;144:e368-e454, verified by the RP03 worker on
     PubMed 34709879, and is used in RP03's avoided actions.
4. **`condition_tool_guidance.yaml` / `test_guidance_claims`** (orchestrator): see section 8.
5. **MockServer routing** (`mock_server.py` or body-imaging matching; new in this audit).
   - A `chest_CT` order is answered by the case's stored chest-abdomen-pelvis CT follow-up. The
     region-stem overlap is already described in SKILL_NOTES.
   - In the 16 teratoma cases probed, a chest CT order therefore returns the ovarian teratoma
     finding: M01, M04, P01, P04, P06, P07, P08, RM02, RS01, S01, S02, S03, S04, S06, S09, S10.
     That is a result of a pelvic study the agent never ordered.
   - Proposal: answer a narrower-region order only with a report of that region, or else with the
     library normal of the ordered study. Case-side, this would otherwise need a chest-only
     follow-up in each of the 16 cases.
   - Not changed here: it is routing behaviour shared with every condition that stores a CAP CT,
     and it scores nothing.
6. **Library:** the `fallback_library.yaml` normals for `pelvis_abdomen_MRI` and
   `pelvis_abdomen_CT` say "no adnexal or pelvic mass" and are served to men on off-pathway orders
   (M05, RS03, RP01). Make them sex-neutral ("no pelvic mass").
7. **Authoring (informational):**
   - One identical `order_cognitive_screen_post_intervention` output was written into all 30
     cases. This round fixed the 3 that contradicted their baseline.
   - Other conditions' leads: the CSF paired serum glucose differs from the labs in 7 MS-RR cases
     and in ALZ-EARLY-P02, and "5 to 7 exchanges" appears in 1 MS-RR case.

## 8. Check results (17 Nov 2026, after the DDI-DX fix)

- `perfect_agent.py <id>`, one id per call: 30/30 pass.
  - One warning, RS04: `csf-flow-cytometry` is answered by the same stored CSF report as
    `action-2-analyze-csf`. This is accepted by design (D29): flow cytometry is an add-on on the
    same sample, and the case CSF answers every `analyze_csf` call, as for the TB PCR, cryptococcal
    antigen and VDRL already in that report.
- `pytest test_case_guards.py -k "NMDAR-ENC-"`: 240 passed.
- `apply_diagnosis_synonyms.py --check --conditions autoimmune_encephalitis_nmdar`: would change 0
  of 600 cases.
- `pytest test_panel_case_contract.py test_red_herring_paths_resolve.py`: 4 passed.
- `case_io.py check` over all 30: schema OK, synonym guard OK. "No test failure names these
  cases": the suite had 3 failures elsewhere, in other conditions or central claim tests.
- `pytest test_guidance_claims.py`: one NMDAR claim is stale. The guidance files were not edited;
  the orchestrator updates them.
  - Claim `nmdar/no FDG or blood cultures`: the app says (0, 0), the cases say (3, 1).
  - Advanced-imaging criteria are now in P04 (brain FDG-PET, optional), RM03 (whole-body FDG-PET)
    and RP01 (whole-body FDG-PET and MR angiography). Microbiology criteria (blood and urine
    cultures) are in RS02.
  - All other NMDAR claims still hold: MRI and routine EEG required in 30, continuous EEG
    recommended in 29, female pelvic ultrasound 21, testicular ultrasound 4, CAP CT at 45 or older
    5, CSF NMDAR antibodies required in 30.
