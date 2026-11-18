# SYNC-CARD: November 2026 round, condition audit summary

Written 17 Nov 2026 by the condition auditor, after the workers and verifiers finished.
- 30 cases. 60 notes, all from R2 (NB-87MF-FBTV-TPWE).
- Decisions: `plans/SYNC-CARD-decisions.md` (D1-D27). Plan and canonical texts: `plans/SYNC-CARD.md` (C1-C11).
- Audit scripts: `/home/aprotani/review-round-2026-11/work/scratch/sync-audit/`:
  - `rulecheck.py`: note and ruling coverage;
  - `decoys.py`: stored studies against their avoided entries and criteria;
  - `leakscan.py` and `leakscan2.py`: turn-0 text and drug checks, scanned for labels and evidence;
  - `drugnums.py`: patient results that appear in drug checks;
  - `xmod.py`: cross-modality scan;
  - `serve_probe.py`: what the MockServer actually serves for a given order;
  - `fix_audit.py`, `fix_rr.py` and `logs_rulings.py`: the audit's own edits.

## 1. Classes: how each was fixed, with counts before and after

The "before" counts were measured by the lead at the start of the round, or by this audit where
marked. The "after" counts were measured by this audit on the final files.

| Class | Fix | Before | After |
|---|---|---|---|
| C1 EXERCISE-EXERTIONAL (D1) | In M01, M02 and RM03: the exercise waste label is deleted, `action-exercise-test` is added (recommended; exercise test or exercise echo) and a hard TTE-before constraint is added. The test is not in the stop rule. | 3 cases labelled waste | 0. Each of the 3 cases has the criterion and the hard constraint. |
| C2 EXERCISE-SEVERITY (D2, D9) | Harm where the arrhythmia is uncontrolled and symptomatic (Fletcher 2013). The exercise echo always carries the same severity as the exercise test. | Lead: RP05 and RS02. Workers added RS01 and S03 beyond the plan (RS01 had a pulseless arrest; S03 has hypotension and pauses). | See the audit straggler below: 0 left inconsistent. |
| C3 AVOIDED-DECOY (D3-D6) | Each served off-pathway report gets an avoided entry. Removing a report is declined. | Unlabelled: EPS 18, bubble 23, exercise echo 22 follow-ups and 7 fallbacks, coronary angiography 8, coronary CTA (fallback) 7, EMG/NCS 6 + 3, PSG 3 + 3, TEE (fallback) 21, body imaging in 6 cases | 0 outside the documented exceptions (listed after this table). |
| C4 AVB-TERMS (D7) | Kusumoto 2018 definitions applied, and the conduction arithmetic checked. | "Mobitz" strings: M01 29, M02 28, M03 14, RM02 16, RM03 33 | 0 misuses. "Mobitz II" now appears only in M02 and RM03, where 3:2 conduction is documented; in RM02's ECG (single dropped beats); and in the M01 general pearl. |
| C5 DRIVING-SOURCE (D8) | The canonical texts DR-PM, DR-ICD1, DR-ICD2, DR-OPEN and the P03 text. | 14 musts with a wrong or missing source: M01, M02, M03, RM02, RM03, RP04, RS02, P01, RS05, RP05, S03, RP01, RS01, P03 | 0. S01, S02, S04, S06 and RS03 keep "1 week (ESC 2018)" (NO-ACTION). |
| C6 TIER-HIGH-RISK (D13, D14) | M05 telemetry and P03 TTE become required and enter the stop rule. | 2 | 0 |
| C7 DX-CERTAINTY (D7, D12, D16, D17, D19, D23) | accepted[0] changed in 6 cases. "AVRT" removed from M05's rejected labels. | 6 + 1 | Done (see section 4) |
| C9 MUST-WRONG | Canonical musts in M04 (R2 and a new antidepressant must), M05 R4, RP03 R7 and R8, RP05 R2 and R3, RS01 R3, RS02 (new must) and RM03 R2. | 11 | 0 |
| C10 UNSATISFIABLE (D5, D18) | `action-coronary-assessment` added in RM03 and RS05 (approved). | 2 musts with no criterion | 0 |
| **Audit: EXERCISE-SEVERITY uniformity (new)** | S01, RS03, RS05 and RS06 (all approved) had waste labels on exercise test and exercise echo. They meet the same Fletcher 2013 absolute contraindication used to make RS01, RS02, RP05 and S03 harm. S01 and RS03: unpaced persistent complete AV block with symptomatic slowing or pauses of 4.2-5.2 s. RS05: sustained VT recurring on telemetry with near-syncope. RS06: flutter with 1:1 conduction and loss of consciousness on telemetry. The RS05 and RS06 rationales already stated a provocation risk. Both entries are now harm, citing [Fletcher_2013]. Exercise test ids are kept; the exercise echo id is now `avoid-harm-exercise-echo`. | 4 cases (8 entries) | 0. Every persistent unpaced complete AV block case is now harm (RS01, RS02, RP05, S01, S03, RS03, plus S02 and S04 on AS grounds). The paroxysmal-block cases stay waste or are criteria (D1). |
| **Audit: DRUG-LEAK (new, blind leak pass)** | Each case's `check_drug_interactions` outputs (initial, follow-up, fallback) are served to any drug query, including a first call. They named the diagnosis or quoted a result that a criterion orders. Fixed by wording only. | 9 cases: P02 "hypertrophic cardiomyopathy" (4 outputs); S05 "severe aortic stenosis" (4); S06 "sinus node dysfunction" (4); RS06 "atrial flutter" (2) and "4:1 conduction" (2); RS05 "VT substrate"; RS02 "complete heart block" and "LVEF 42%"; RS03 "complete heart block" and "LVEF 45%"; P01 "QTc 448 ms"; RP01 "magnesium 4.4 mg/dL" and "creatinine 0.7" | 0 |

Documented exceptions to C3 (unlabelled on purpose, re-verified):
- From D27 in the plan:
  - P02 exercise test;
  - RS06 PSG and TEE;
  - RP02 TEE, chest CTA and both PETs;
  - RS03 coronary angiography and CTA (R5 makes them conditional);
  - RM01 speech and cognitive screens;
  - M04 chest CT;
  - M05 and S06 exercise test and exercise echo;
  - gait, performance status, audiometry and orthostatic BP everywhere.
- From D4: RP01 exercise echo. The same rule covers P04 and RS04, whose fallback exercise echo answers the same question as the optional exercise test.
- RM02 TEE (the worker's justified departure, accepted). Fever, rheumatic valve disease and new AV block raise perivalvular extension of endocarditis (ESC 2023 endocarditis). The case now has an endocarditis entry in its differential.

Kept after review:
- **Product-label contraindications in drug checks.** These cases keep the generic product-label
  contraindication for beta-blockers or AV-nodal drugs in "second- or third-degree AV block
  without a pacemaker": S01, S02, S04, RP04, RS02 and RS03. It is what an interaction checker
  returns and does not assert the patient's state (kind 2). In RS02 and RS03 the narrower
  "third-degree" only wording was widened to the label wording.
- **M04's "drug-induced torsades de pointes" risk sentences.** These are CredibleMeds risk
  categories of the patient's own drugs, which is what the tool establishes.

## 2. Checks against the plan, by script, over all 30 cases

- **Canonical texts are verbatim:** driving (C5), the M04, M05, RP03, RP05, RS01, RS02 and RM03
  musts (C9), and the M05 and P03 tiers and stop rules (C6).
  - M05 R4 keeps an added clause on ambulatory event monitoring, because the event monitor is a
    required criterion there.
  - RS02's new must says "no oedema on CMR if it is obtained", because CMR is recommended, not
    required.
- **Stop rules:** every one lists exactly the required criteria.
- **Sequence constraints:** every one names existing criteria. The hard TTE-before constraint is
  present in M01, M02 and RM03.
- **AV block terminology (C4):** no "Mobitz" next to 2:1 or 3:1 conduction except "Mobitz II
  (3:2) and 2:1", which names the two separately.
- **RM01:** no ground-truth text calls the hypoxic events "syncope". The remaining hits are the
  ESC Class III remark and the reflex-syncope mimic.
- **Diagnosis matching (`DiagnosisCriterion.matches`):** these answers score:
  - "Mobitz II AV block" and "high-grade AV block with bifascicular block" (M02);
  - "paroxysmal SVT, likely AVNRT, AVRT not excluded" (M05);
  - "complete heart block from rheumatic carditis" (RM02);
  - "RVOT myxoma" (RP02);
  - "cardiac sarcoidosis with complete heart block" (RP05);
  - the anti-Hu answer (RM01).

  "WPW" is vetoed in M05. "AVRT" alone does not score in M05.

  Pending centrally: "Mobitz II AV block" still scores in M01 and M03 (C1a), and "acute rheumatic
  fever" does not yet score in RM02 (C1b).
- **Notes and rulings:** every one of the 60 note ids appears in exactly one
  `work/rulings/<CASE>.json`, in the right file, with a valid status.
  - P04 and RS04 had no ruling file. This audit added one for each: NO-ACTION, approval with
    LIT-only changes.
- **Logs:** every case changed since 06b74446 beyond the cross-condition classes has a log with
  `## Changes`. P04 and RS04 changed only by LIT, and their logs have `## Class changes` only.
- **Not a leak (RM04, worker's flag):** the stored D-dimer 8.4 is not served to the troponin,
  BNP, beta-hCG and creatinine order, nor to CBC, BMP or coagulation orders
  (`serve_probe.py`: zero hits). It reaches only a D-dimer order, which is labelled waste. No
  change.

## 3. Blind leak pass

- **Turn 0** (`format_patient_info`, rendered for all 30, with case-sensitive acronyms): no
  accepted label of the case's own diagnosis appears. The scan has three hits, all family
  history, which is a legitimate risk factor and kept:
  - RP04: father paced for complete heart block;
  - RS03: brother paced for complete heart block;
  - RP05: an aunt with pulmonary sarcoidosis. The matcher fires only on scattered tokens.

  No expected_evidence 5-gram appears in any patient block.
- **Drug checks:** fixed in 9 cases (section 1). After the fix, no drug output names an accepted
  label beyond the kind-2 product-label wording, and none repeats an expected_evidence 5-gram or
  quotes a criterion's result.
  - Normal creatinine values remain in the renal-dosing warnings of P04, RM01 and RP03. They are
    not in any criterion's evidence. Kept.
- **Cross-modality:** `xmod.py` scanned every impression, interpretation and summary. No report
  synthesises another modality. The hits are:
  - tilt reports naming the rhythm recorded during the tilt;
  - the S03 EEG's ECG-channel artefact;
  - "CMR recommended" lines in echo and X-ray reports;
  - RP02's CMR "most consistent with a myxoma; histological confirmation required" (kind 2).

## 4. Rulings

| Status | Count |
|---|---|
| FIXED | 40 |
| NO-ACTION | 16 (13 approvals, plus the comment-less verdicts of M04, RP03 and RS01) |
| ALREADY-FIXED | 3 (P03 1e6f0501, MRI-CONTRAST; RS01 4d6edbb9, tilt already waste; RS01 da138055, EEG already waste) |
| CENTRAL | 1 (RP03 d08aab43: review-app display order) |
| DECLINED (whole note) | 0 |
| NEEDS-ANDREA | 0 |

DECLINED parts of notes that are otherwise FIXED, with the reason for each:
- **M01 c5f02c42, pacing citation.** ESC 2021 pacing (Glikson) gives Class I pacing for Mobitz II,
  2:1 infranodal, high-grade and complete AV block without a reversible cause, so the citation is
  correct.
- **M01 verdict, "infra-Hisian on EPS" in the label.** The EPS is waste here (ESC 2018: EPS only
  when the non-invasive work-up is non-diagnostic), so the label must not depend on it.
- **M05 c0eda0e6, making the EP study required.** Management is the same either way (ESC 2019
  SVT), and the note itself offers the alternative that was applied (AVRT removed from rejected).
- **P01 verdict, labelling invasive angiography after CTA.** An avoided action matches every call,
  so the label would penalise angiography as the first and only coronary test, which the
  criterion accepts.
- **RM01 verdict, moving the case to another condition.** No paraneoplastic condition exists. The
  case stays as the condition's mimic (October Q1), relabelled.
- **RP02 verdict, tilt harm to waste.** The note allows harm when it is justified separately, and
  the preload rationale does that.
- **Removing stored reports (RP05 4c6bc3dc, RS01 eaa7610b, 4d6edbb9, da138055).** Per D3, deleting
  a report would let the library serve a normal report that contradicts the patient
  (`library_contradictions.yaml`). The reports are labelled instead.
- **RP05 2e4f14c5, stop rule.** The served reports are not an executed sequence. The extra tests
  are labelled.
- **RS02 verdict, contrast studies as harm.** The eGFR is about 42, and ACR-NKF 2020 puts the
  material risk below 30. They are labelled waste.

## 5. Approved cases changed, and why

All 13 are R2 approvals. Each now goes back to re-review.

| Case | Changes and reasons |
|---|---|
| P02 | C3: bubble study, PSG and TEE labelled waste; pathway reorder. Audit: the drug checks named HCM. |
| P04 | LIT class only. |
| RM04 | C3: bubble study and TEE waste, chest CT waste, exercise echo harm. |
| RP01 | C3: EPS, bubble study and TEE waste. C5: the driving source was wrong (ESC 2018 cited for 3 months after an ICD); now DR-ICD1. Audit: the drug checks quoted the labs criterion's magnesium and creatinine. |
| RS03 | C3: EPS, bubble study, exercise echo, chest CT and CTA, EMG and TEE. Audit: exercise test and exercise echo raised to harm; the drug checks named complete heart block and quoted the echo LVEF. |
| RS04 | LIT class only. |
| RS05 | C10: must R6 had no criterion, so `action-coronary-assessment` was added. C5: the source was wrong; now DR-ICD2. C3 labels. Audit: exercise raised to harm; "VT" removed from the amiodarone check. |
| RS06 | C3: EPS and bubble study. Audit: exercise raised to harm; the drug checks named atrial flutter and quoted the telemetry's 4:1 conduction. |
| S01 | C3 labels. Audit: exercise raised to harm. |
| S02 | C3 labels (exercise echo harm, AS). |
| S04 | C3 labels (exercise echo harm, AS). |
| S05 | C3 labels. Audit: the drug checks named severe aortic stenosis before the echo. |
| S06 | C3 labels. Audit: the drug checks named sinus node dysfunction. |

The open question from the plan still stands. If Andrea prefers to keep approved cases frozen,
the purely additive C3 labels could be reverted. The C10 and C5 source fixes, the audit's
drug-leak fixes and the exercise-harm uniformity correct real defects and should stay.

## 6. Label and code changes

accepted[0] changed in 6 cases, each on a reviewer ruling. No `icd_codes[0]` changed.

| Case | New accepted[0] |
|---|---|
| M01 | "Cardiac syncope due to paroxysmal 2:1 and high-grade AV block (infranodal) on a background of trifascicular conduction disease" |
| M02 | "Cardiac syncope due to Mobitz II and paroxysmal high-grade AV block with bifascicular conduction disease" |
| RM01 | "Hypoxic transient loss of consciousness from nocturnal central sleep apnoea with secondary sleep-related asystole, due to anti-Hu paraneoplastic brainstem encephalitis" |
| RM02 | "Cardiac syncope due to intermittent complete heart block from recurrent acute rheumatic fever with active carditis, on chronic rheumatic heart disease" |
| RP02 | "Cardiac syncope due to a right ventricular outflow tract mass most consistent with myxoma (histology pending), causing intermittent dynamic RVOT obstruction" |
| RP05 | "Cardiac syncope due to clinically diagnosed cardiac sarcoidosis (extracardiac histology with compatible cardiac imaging; no myocardial biopsy) with complete AV block and non-sustained VT" |

M05: "AVRT" was removed from `diagnosis.rejected`.

## 7. CENTRAL requests (consolidated)

1. **Synonyms** (`diagnosis_synonyms.yaml`, then `--prune --conditions syncope_cardiac` and
   `--check`):
   - a) Scope "mobitz ii", "mobitz type ii" and "mobitz 2" (I44.1) to M02 and RM03 only. Today a
     Mobitz II answer still scores in M01 and M03 (verified). Add a "2:1 AV block" or "2:1
     second-degree AV block" label for M01.
   - b) Add ARF labels to `I44.2+rheumatic` for RM02: "acute rheumatic fever", "recurrent acute
     rheumatic fever", "recurrent rheumatic fever", "acute rheumatic fever with carditis" and
     "acute rheumatic carditis". Check them against chloroquine, laminopathy and malaria. "acute
     rheumatic fever" does not score today.
   - c) Optional, for M05 (I47.1 entry scoped to the case): "orthodromic avrt" and
     "atrioventricular re-entrant tachycardia", so that an answer naming only AVRT is credited.
   - d) Record the six accepted[0] label changes listed in section 6.
2. **Citation keys** (pack allow-list, sec.10). Until they exist, the sources are named in the
   text.
   - `[ESC_2018_PI]` (Brignole 2018 Practical Instructions);
   - `[EHRA_2009_ICD_Driving]`;
   - `[ACR_NKF_2020]` (S03 harm labels);
   - `[AHA_2020_DrugArrhythmia]` (M04);
   - `[ESC_2022_CardioOnc]` (RS02);
   - `[BSG_2021_IDA]` (RP03).
3. **Pack text** (`criteria_packs/SYNC-CARD.md`):
   - exercise testing is recommended in exertional syncope with intermittent AV block (D1);
   - exercise testing is harm in any uncontrolled symptomatic arrhythmia, as now applied in 10
     cases (RS01, RS02, RP05, S01, S03, RS03, RS05, RS06, M04 and RM02, plus RM04, RP02 and the AS
     cases on their own grounds);
   - the TTE is required in Brugada with an induced type 1 pattern (D14);
   - the driving sources (D8);
   - the torsades potassium divergence (D10);
   - the decoy table (C3).
4. **Review UI** (`web-review/.../CaseDetail.tsx`): print a row's label key (`test`) before
   `interpretation`, `result` and `abnormal`, and print null as "not stated" (RP03 d08aab43).
5. **MockServer** (S03 log): `order_body_imaging {study: chest_CT, contrast: false}` is answered
   with the stored contrast chest CT, because body imaging is not routed by contrast. The labels
   are correct (plain waste, contrast harm), but the served report is the contrast study.
6. **Guidance claims** (`condition_tool_guidance.yaml`, for the orchestrator):
   `test_guidance_claims` reports one stale SYNC-CARD claim. "sync/echo required 29 recommended 1"
   is now (30, 4):
   - P03's TTE is now required (D14);
   - the exercise echo is now an alternative of recommended exercise criteria (M01, M02, RM03 and
     P01; D1 and D4).

   The guidance files were not edited.

## 8. Open items (none needs information that only Andrea has)

- **RS01 label.** The event needed about 60 s of CPR before the pulse returned. ESC 2018 Table 2
  excludes cardiac arrest without spontaneous recovery from syncope, the same logic as RM01 (D16).
  The label is unchanged because no reviewer ruled it wrong and R2 did not object. Offered to the
  next round.
- **RM02 blood cultures.** With endocarditis now in the differential, blood cultures before
  benzathine penicillin would be good practice. The case stores no culture report and has no
  criterion for it, so this needs new data. Offered to the next round.
- **RS02 and RS03 tilt labels.** The rationales call tilt "unsafe" in hypotensive complete heart
  block, but the severity is waste. ESC 2018 does not list bradyarrhythmia among the tilt
  contraindications, so harm would have no clean citation. Kept as waste.
- **Orthostatic BP** (plan open question): 14 cases store an active-stand report with no
  criterion. These calls are unscored and unpenalised. Not changed.

## 9. Check results (final files)

- `perfect_agent.py <id>`, one call per case: 30 of 30 pass. One warning: in RM03 the coronary CTA
  alternative of `action-coronary-assessment` is answered by the case's own fallback CTA, which
  shows the LAD occlusion, as intended.
- `pytest test_case_guards.py -k "SYNC-CARD-"`: 240 passed.
- `apply_diagnosis_synonyms.py --check --conditions syncope_cardiac`: would change 0 of 600.
- `pytest test_panel_case_contract.py test_red_herring_paths_resolve.py`: 4 passed.
- `case_io.py check` on the 10 cases the audit edited: schema OK, synonym guard OK, and no failure
  names them. The 3 suite failures belong to other conditions or the central claims test.
- `pytest test_guidance_claims.py`: fails, with the SYNC-CARD part limited to the one stale claim
  in section 7, item 6. The other failures belong to NMDAR, MG and NPH.
