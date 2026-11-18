# FEPI-TEMP: condition summary, November 2026 round

This is the auditor's summary for the 30 FEPI-TEMP (`focal_epilepsy_temporal`) cases, written
16 Nov 2026.

- Plan: `FEPI-TEMP.md`. Decisions: `FEPI-TEMP-decisions.md` (D1-D36). Base: commit 06b74446.
- Audit scripts are in `/home/aprotani/review-round-2026-11/work/scratch/fepi-auditor/`:
  - checks: `audit_classes.py`, `rulings_check.py`, `lat.py`, `leak.py`, `leak2.py`, `ddi.py`, `ddi2.py`, `xmod.py`, `labsig.py`, `counts.py`, `dxmatch.py`
  - fixes: `fix_ddi.py`, `fix_meta.py`, `fix_labs.py`, `logs_append.py`
- There are 213 notes, all from R1 (NB-KSC3-TWUA-QDTM), spread over all 30 cases.
- No FEPI-TEMP case is in `work/approved.txt`, so no approved case was changed.
- All 30 case files differ from 06b74446. Each one has a log in `logs/<CASE>.md` with '## Changes' and
  '## Verification'.

## 1. Rulings

| status | count |
| --- | --- |
| FIXED | 205 (three of them partly DECLINED, listed below) |
| ALREADY-FIXED | 6 |
| NO-ACTION | 2 |
| CENTRAL | 0 as a primary status. The display and documentation parts are carried as CENTRAL remarks inside FIXED, ALREADY-FIXED and NO-ACTION rulings |
| DECLINED | 0 in full |
| NEEDS-ANDREA | 0 |

- Each of the 213 note ids appears in exactly one `work/rulings/<CASE>.json`, the case it belongs
  to. Every ruling has a valid status and a non-empty `what`; `rulings_check.py` reports none
  missing, duplicated or extra.
- ALREADY-FIXED notes:
  - M05 0a5a3164, P01 1e26e813, P04 9df51056 (D9). The neuropsychology rows are already flagged
    abnormal; the remaining issue is display only (CENTRAL 3).
  - P01 8e90d267 and RP01 adaf74ab (D15). The stop rule already keys on `eeg_type` criteria
    (CENTRAL 3).
  - RP04 6571ab91 (D11). The case already says "possibly FCD IIIa" and the label already says
    "suspected".
- NO-ACTION notes: RM03 7d9daed6 and S01 e1e2f67a (D14). The stop rule is diagnostic only and the
  musts already say not to delay treatment (CENTRAL 4).
- Plan deviation, kept: the plan listed RP01 03911b8d as NO-ACTION. It is now FIXED, because a
  verifier changed the status-epilepticus must. That must had said only "treat ... under
  continuous EEG". It now says to treat promptly, without waiting for MRI, LP, PCR or the EEG.

### DECLINED in part (the reason for each)

- **M02 6a18310d** ("ancestry undocumented"). `patient.demographics.ethnicity` is "East Asian",
  and the agent sees demographics. The HLA part of the note is FIXED: the must became a
  prohibition (CPIC 2018).
- **S04 404a1855** ("ancestry inferred from surname"). Demographics state "Southeast Asian (Lao)".
  The HLA part is FIXED.
- **RM02 a7f7e00b** (do not mandate the switch from valproate).
  - What was applied: an individual risk-benefit discussion, and the pregnancy prevention
    programme while valproate continues.
  - What was declined: the switch to lamotrigine or levetiracetam stays. NICE NG217 (2025) and
    MHRA/EMA 2024 say valproate must not continue in a woman who can become pregnant unless no
    other treatment is suitable, and focal epilepsy has suitable alternatives.

### NEEDS-ANDREA

None. Every point was decided on clinical grounds (decisions file, section "NEEDS-ANDREA").

## 2. Classes: counts at 06b74446 and now (`counts.py`, cases unless stated)

| class | how fixed | before | after |
| --- | --- | --- | --- |
| LIT (commit 393c547e) | no literature criterion, follow-up, initial or fallback output left | 30 | 0 |
| MRI-CONTRAST (71517e55 + M04, D30) | plain initial `contrast_used: false` + gadolinium follow-up `true` | 0 pairs | 12 pairs (11 class cases + M04) |
| BIOPSY (D3) | avoided actions, stereotactic and open biopsy, severity `harm`, case-specific rationale; RP03 excepted | 0 | 29 |
| BIOPSY resection extension (D3) | resection `harm` [Kwan_2010] in the 18 cases with no surgical indication; none where surgery is the plan | 0 | 18 (exact list checked) |
| TUMOUR (D4) | canonical maximal-safe-resection must (S02, S03, S06, RM04, M04) | 0 | 5 |
| TEE (D5) | `avoid-waste-tee` severity `waste` (RM02, RP02, RS05) | 0 | 3; no case stores an unlabelled TEE |
| HLA (D6) | unconditional must replaced by the canonical prohibition (M02, M04, M05, P04, RS05, S04, S06) | 7 musts | 0 musts, 7 prohibitions; ancestry in each matches demographics |
| VPA (D7) | MHRA "under 55 / two specialists" wording replaced by the canonical sex-specific texts | 19 | 0 (19 canonical) |
| LABSIG (D8) | named rows filled; abnormal rows with null significance (script count, all 30 cases) | 76 rows | 43 rows (the remainder are borderline or explained, as the plan says, see 4) |
| LAT (D10) | automatism hand moved to the focus side in 13 cases; contralateral signs kept | 13 | 0 (`lat.py`: every remaining contralateral mention is dystonia, version or an auditory side) |
| DXCERT (D11) | 9 label changes (section 5) | - | 9 match the plan verbatim |
| DIFF / KCE (D12, D13) | canonical texts | - | present in every listed case |
| PREG (D16) | recommended `action-labs-hcg` {panels: [beta-hCG]} + stored `beta-hCG` panel, not in stop rule | 0 | 10 (exact list) |
| NEUROPSY (D17) | RS01 criterion; S02/S03 must clause | 0 | 3 |
| Stale generation line in `metadata.case_body_concerns` (worker class) | deleted | 18 | 0 (3 fixed by me) |
| Drug-interaction report quoting another modality's result (own, this audit) | rewritten | 1 (P05) + 1 introduced (RP04) | 0 |

Structural checks over the 30 cases come back clean:

- every stop-rule id is a required criterion;
- every sequence-constraint id exists;
- no avoided action matches a criterion's call;
- every criterion and avoided action carries a citation;
- every red-herring `field_path` resolves;
- no new em dash was added (M04 and S05 have fewer than at base).

Script hits that I accepted on purpose:

- **Pathology reports name "CNS WHO grade 1"** (S02, S03, S06, RM04). These are the stored resection
  reports, and histology legitimately grades the tumour (Kind 2). The ground truth and the label
  carry no grade.
- **RS01's must on paternal valproate risk** (MHRA/EMA 2024). The plan keeps it.
- **October `metadata.revision_reason` in M01-P01 mentions "literature optional".** It is a dated
  history line, not process text about this round.
- **Em dashes inherited from base text** (prose not churned).

## 3. Blind leak pass

- **Turn 0** (`format_patient_info`, `leak.py`, `leak2.py`).
  - No case names its own new diagnosis.
  - These cases say "focal epilepsy" at turn 0 only as their known history (drug-resistant or
    long-standing epilepsy, two failed ASMs, medication indications): P04, RP04, RS03, RS04, plus
    P03 (known right TLE), RP03 (known metastasis), RM02 (known TSC) and RS01 (known hypothalamic
    lesion). The lateralization, substrate and certainty the label asks for come from the
    work-up.
  - Several cases describe prior outside studies: M04, P02, P04, RP03, RP04 and RP05 (standard
    MRI, outside EEG). Each is either a red herring or a study the case does not score. P04 scores
    no MRI, and the encounter's own 3T MRI failed. Each scored study differs from the prior one.
- **Drug-interaction outputs** (`ddi.py`, `ddi2.py`; initial, follow-up and fallback in all 30
  cases). None names the diagnosis or another criterion's expected evidence.
  - Two reports quoted a result from another modality, and I fixed both (section 4).
  - P05's summary paraphrases its own criterion's evidence. That is the report's own content,
    which is legitimate.
- **Cross-modality synthesis** (`xmod.py`, every stored report). No EEG report cites MRI, no MRI
  report cites EEG, and no lab report cites imaging. What remains is standard radiology wording
  ("MRI recommended for further characterization" in a CT, "CSF signal" in MRI sequences).

## 4. Stragglers fixed in this audit (case_io; logged under '## Verification')

- **P05** `followup[1].output.warnings`. "PR interval on the current ECG is 194 ms" gave the
  (optional) ECG result inside the drug-interaction report. It now reads "Lacosamide prolongs the
  PR interval: if it is chosen, check the PR interval on an ECG before starting and repeat the ECG
  after titration." This line was already present at base.
- **RP04** `followup[4].output.warnings[3]`. D22 had added "the sodium of 134 mEq/L", a result of
  the labs criterion, to the drug-interaction report. It now reads "... given its enzyme induction
  and its hyponatremia risk." The must that repeats the sodium value is ground truth and stays.
- **RM03, RP01, RP03** `metadata.case_body_concerns`. The false generation line ("useless_tools
  entry for `analyze_ecg` dropped: tool output is provided up-front ...") was still there after
  the other 27 cases had it deleted. Deleted.
- **RM03** TSH 5.8 (a red-herring row). Filled "Mildly raised TSH after an acute illness; repeat
  with free T4 as an outpatient."
- **RS02** fallback D-dimer 1.6 and beta-hCG 24500 were flagged abnormal against non-pregnant
  ranges at 33 weeks. Filled: D-dimer "rises physiologically in the third trimester ... cannot be
  read against the non-pregnant cut-off"; hCG "Consistent with the known third-trimester
  pregnancy."
- No ruling changed: these are my own findings, and no note covers them.

Left null on purpose, per the plan's LABSIG scope:

- RS04 and S02 iron-deficiency rows: known, treated, and not in the KCE (plan: "if anemia is in the
  KCE").
- Remaining RP03 inflammatory and CBC rows on ICI and dexamethasone.
- Borderline glucose, HbA1c, Mg and GGT rows.
- S05 bicarbonate 21, and the S03 MCV.

Considered and not changed: RM03 (South Asian, long-term phenytoin) and RS01 (East Asian, on
valproate) have no HLA prohibition. Neither case starts carbamazepine or oxcarbazepine, and the
HLA class (D6) converted existing musts; it did not add new prohibitions. RM03's drug-interaction
report already says to screen before oxcarbazepine.

## 5. Label / code changes (accepted[0]; no ICD code changed)

These are the DXCERT class (D11), each by physician note or class, and all are CENTRAL 2
(synonyms):

- **S02, S03, S06.** "secondary to dysembryoplastic neuroepithelial tumor" became "low-grade
  glioneuronal tumor (presumed DNET)". S02 and S06 also name the site.
- **RM04.** "(presumed ganglioglioma or DNET)", with no CNS WHO grade.
- **M04.** "(focal cortical dysplasia)" became "(suspected focal cortical dysplasia)".
- **P04.** "(MRI-negative)" became ", nonlesional on 1.5T epilepsy-protocol MRI (3T MRI not
  tolerated)".
- **RP03.** The checkpoint-inhibitor clause was dropped.
- **RS01.** Now "Drug-resistant focal epilepsy with left temporal lobe seizures and left mesial
  temporal sclerosis in a patient with a hypothalamic hamartoma and gelastic seizures (dual
  pathology)". The causal "secondary to" was dropped.
- **RS02.** "with right mesial temporal sclerosis and presumed remote calcified
  neurocysticercosis, presenting at 33 weeks gestation".

`apply_diagnosis_synonyms.py --check` is clean. A matcher probe (`dxmatch.py`) confirms:

- "DNET", "presumed DNET", "low-grade glioneuronal tumor/tumour", "ganglioglioma", "suspected
  FCD", "nonlesional"/"MRI-negative" and "dual pathology" answers score.
- "checkpoint inhibitor encephalitis" (RP03), "eclampsia" (RS02) and HS-only answers for tumour or
  nonlesional cases do not.
- One gap for CENTRAL 2: "left temporal epilepsy" (without "lobe") does not match.

## 6. CENTRAL requests (consolidated)

1. **Criteria pack and allow-list** (`criteria_packs/FEPI-TEMP.md`).
   - Add the new keys: HH_consensus_2026, SNO_EANO_prophylaxis_2021, AAN_AES_SMFM_2024,
     AHA_CVT_2024, ACEP_seizure_2004, Lacosamide_label, EAU_hyponatremia_2014, Friedman_IIH_2013,
     WHO_CNS5_2021, CDC_USMEC_2024. Verify the four marked "label" before adding them.
   - Update the work-up tiers, avoided actions, sequence and canonical musts as listed in plan
     section 4.1.
2. **Synonyms** (`diagnosis_synonyms.yaml`).
   - Review the 9 label changes above.
   - Consider "temporal epilepsy" as a variant of "temporal lobe epilepsy".
3. **Review app display** (web-review / review_api).
   - A null `clinical_significance` or `contrast_used` prints "none"; it should print "not
     stated".
   - Lab and neuropsychology rows print the flag above the test name; print `test` first.
   - The stop-rule panel shows tool names only; show each criterion's label and arguments.
   - This covers 15 LABSIG, 3 NEUROPSY-FLAG and 2 STOPSUB notes.
4. **Harness doc / review-app text.** State that the stop rule measures diagnostic completeness
   and never delays treatment, which is scored only in the musts. This covers 4 timing notes.
5. **Guidance claims** (`condition_tool_guidance.yaml` FEPI responses and `test_guidance_claims.py`).
   These are now false for FEPI-TEMP. Current values from the test:
   - routine EEG: 24 criteria, 22 required, optional in RP01;
   - video-EEG: 11, required in P01, P02, P03, P04, RP04, RS01, RS04 and recommended in M05, P05,
     RP03, RP05;
   - CT: optional in P04, RP01, RS02; required in RM03; recommended in RM01, RP05;
   - labs: 26 criteria, optional 15, required P02, RM03, RS02, recommended 17;
   - ECG: optional 20, required none, recommended RP02, absent in 9;
   - echo or cardiac-monitoring waste: 29 and 28.
6. **Cross-condition classes.**
   - Unlabelled stored biopsy follow-ups: NMDAR-ENC (18 cases), SE (6), GLIO-HG (3, where tissue
     is often required).
   - Unlabelled TEE: GBS (1), SE (3), VASC-DEM (4).
   - MHRA valproate wording: MIG-AURA (5).
   - Automatism side versus focus in any SE or FND case.
   - Drug-interaction reports that quote ECG or lab values from another modality: worth a scan in
     every condition (`ddi2.py` here).
7. **Guard suggestion** (`test_case_guards.py`). A stored `obtain_tissue_diagnosis` or TEE
   follow-up that no criterion orders should be matched by an avoided action or explicitly
   exempted.

## 7. Check results (after the fixes)

- **`perfect_agent.py <id>`**: all 30 cases pass, one id per call, with no warnings. `-v` on P05
  and RP04 confirms that each drug-interaction criterion receives its follow-up.
- **`pytest agent-platform/tests/test_case_guards.py -k "FEPI-TEMP-"`**: 270 passed.
- **`apply_diagnosis_synonyms.py --check --conditions focal_epilepsy_temporal`**: "Would change 0 of
  600 cases", exit code 0.
- **`pytest test_guidance_claims.py test_panel_case_contract.py`**: 4 passed, 1 failed.
  - The failure is `test_every_quantified_claim_in_the_guidance_is_true`. It names FEPI-TEMP
    claims (the expected tier changes of D16, D18, D19, D20, D21, D25, D5), plus ALZ, FTD and MS
    claims. This test is maintained centrally after the round (ROUND_POLICY; CENTRAL 5 above);
    the case data are right and the guidance text is stale.
  - `test_panel_case_contract` passes.
- **`case_io.py check`** on the six cases edited in this audit: schema OK and synonym guard OK. The
  only failures naming FEPI-TEMP are the guidance claims above.
