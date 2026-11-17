# NPH: condition audit summary (November 2026 round)

Auditor pass, 17 Nov 2026, run after the workers and verifiers. Plan: `plans/NPH.md`. Decisions:
`plans/NPH-decisions.md` (D1..D18). Audit scripts and outputs are in
`/home/aprotani/review-round-2026-11/work/scratch/nph-auditor/`:
- `book.py`: notes against rulings and logs;
- `survey.py` / `survey.txt`: every criterion, avoided action, constraint, stop rule, must, prohibition
  and difficulty rationale;
- `classes.py`: plan classes C1-C4 and C12, stop rule, collisions, em dashes, last_revised;
- `beforeafter.py`: class counts at 06b74446 and now;
- `spec.py`, `dxmatch.py`, `presume.py`: C5-C10 specifics, `DiagnosisCriterion.matches` and
  wording that presumes surgery;
- `leak_t0.py` / `leak_t0.txt`, `leak_out.py`, `leak_lab.py`, `xmod.py` / `xmod.txt`: the blind
  leak pass;
- `fix_stragglers.py`, `log_stragglers.py`: the audit fixes;
- `perfect.txt`: the per-case perfect-agent runs.

## Bookkeeping

- 36 notes, all from R1 (NB-KSC3-TWUA-QDTM), none from R2.
- Each note id appears in exactly one `work/rulings/<CASE>.json` (its own case), with a valid
  status. No ruling file has an extra id.
- Ruling counts: **FIXED 20, NO-ACTION 15, ALREADY-FIXED 1** (b4648379, P06, class MRI-CONTRAST).
  DECLINED 0, CENTRAL 0 as a primary status, NEEDS-ANDREA 0.
  - The 15 NO-ACTION rulings are approvals of the chief complaint ("tutto ok", "bene", "ok" and
    so on).
  - Two FIXED rulings carry a CENTRAL part for the synonyms: 730a2ee7 (M08) and f6b2546c (P05).
- No chief complaint changed (compared with 06b74446 for all 30 cases).
- All 30 cases changed since 06b74446. Each has a log with `## Changes`.
- Approved cases: none. `work/approved.txt` lists no NPH case.

## Classes: how they were fixed (scripted over the 30 cases, 06b74446 -> now)

| class | before | after |
|---|---|---|
| C1 referral "for CSF shunting" -> "shunt eligibility assessment ... does not by itself decide surgery [Nakajima_2021]" (D1) | 30 / 0 | 0 / 30 |
| C2 one counselling must on benefit, its uncertainty and the complications (D2) | 0 | 30 (exactly one per case) |
| C2/D3 "expected to improve/reverse" in a must | 8 | 0 |
| C3 "awaiting surgery" | 28 | 0 (M07, P05 never had it) |
| C4 `avoid-waste-exercise-stress-test` entry (waste, `[AHA_ACC_perioperative_2024]`), placed right after the echo entry | 0 | 30 |
| C4 echo waste rationale names exercise stress echocardiography, with its citation | 0 | 30 |
| C5 P03 spine MRI required and in the stop rule; P08 drainage required | 0; 1 | 1; 0 (recommended, out of the stop rule, soft constraint kept) |
| C6/C7 pre-tap labs required with a hard labs-before-CSF constraint and in the stop rule (M03, M06, S10 on a DOAC; M08 in cirrhosis) | 0 | 4 |
| C7 "INR 1.5 or less" threshold (M08) | 1 | 0 |
| C8 iNPH / idiopathic NPH in `rejected` (M08, P05) | 2 | 0 |
| C8 "arachnoiditis" in M08 `accepted[0]` | 1 | 0 |
| C9 the "PSP needs a gaze palsy or midbrain atrophy" implication (P07) | 1 | 0 |
| C10 levothyroxine musts that demand a lab confirmation (S08, M04) | 2 | 0 |
| C12 `difficulty_rationale` tier counts wrong | 30 | 0 (recounted from `action_criteria`) |
| LIT: literature criteria and stored literature outputs | 0 | 0 |

Checked across all 30 cases:
- Every stop-rule id is a required criterion, and every required criterion is in the stop rule.
- Every sequence-constraint id exists.
- No call matches both a criterion and an avoided action.
- No must names a test that no criterion orders.
- `last_revised` is 2026-11-17 everywhere.
- The CHA2DS2-VASc scores in the DOAC musts match the patient blocks:
  - M03: age 72, hypertension and stroke give 4;
  - M06: age 74 and hypertension give 2;
  - S10: age 77, female sex and hypertension give 4.
- `DiagnosisCriterion.matches` was re-tested on 17 Nov:
  - M08 matches "Normal pressure hydrocephalus after pneumococcal meningitis";
  - P05 matches "Secondary NPH after SAH";
  - "Hepatic encephalopathy" (M08) does not match;
  - "Idiopathic normal pressure hydrocephalus" and "iNPH" do not match in M08 and P05. They are
    no longer vetoed, but they are not accepted until CENTRAL C-SYN lands.

Accepted variants of the canonical texts (checked, kept):
- M06 spells "overdrainage", the spelling used throughout that case.
- M09 uses the physician's own wording from note c5685e22.
- P01 and P02 open with "gait and continence ..." or "the wide-based magnetic gait and urge
  incontinence ... are more likely to improve than ...". This has the same meaning as the
  canonical "gait is the symptom most likely to improve".
- The em dashes found by the scan are all in patient text that was already there at 06b74446
  (M01-M06, P03, P04, P06). There are none in new text.

## Stragglers fixed in this audit (through case_io, logged under `## Verification`)

1. **NPH-M07** (B, minor). The stored exercise stress test and exercise echo said the test stopped
   "for gait unsteadiness with freezing on the moving belt". Her exam and history describe a
   shuffling gait with no freezing and no start hesitation. Every other case that keeps this
   wording has freezing, start hesitation or a magnetic, "stuck to the floor" gait in the patient
   block. The four strings now read "for gait unsteadiness on the moving belt"
   (`followup_outputs[4]` and `[5]`, findings and impression).
2. **NPH-P03, P04, P07, S06, S09** (B, minor). In each case, the stored exercise test and exercise
   echo report that the exercise was not performed (the patient was unable to walk safely on a
   treadmill). The exercise waste rationale (`avoided_actions[3]`) still said the test "stops
   submaximal and non-diagnostic". It now reads "cannot be completed, so the test is
   non-diagnostic", the wording M05 already used.

After the fixes:
- `perfect_agent.py` passes for all 6 cases;
- `case_io.py check` passes the schema and the synonym guard;
- the only failures that name NPH are the `test_guidance_claims` rows.

No ruling changed, because these were own findings.

## Blind leak pass

**Turn 0.** The patient block was rendered with the real `format_patient_info`.
- No case names its own diagnosis. No accepted label appears, including the case-sensitive "NPH"
  and "iNPH" and the words "hydrocephalus" and "normal pressure".
- No patient block gives a result that a criterion orders: no TUG or timed-walk value, no Evans
  index, DESH or callosal angle of the current study, no opening pressure, no pre-tap lab value.
- The pre-encounter history is legitimate, by the October design:
  - "an outside MRI or CT was reported as showing enlarged ventricles; the images are not
    available" (the referral reason in every case; none of the decisive markers);
  - the comparison values P02 Evans 0.26 (2 years ago), P04 Evans 0.27 (at the bvFTD diagnosis)
    and M09 Evans 0.30 (3 months after the injury);
  - outpatient MMSE scores in S01 and S11 (the cognitive screen is optional, and it is a MoCA);
  - M08's "ammonia levels have been normal" (the hepatic encephalopathy red herring; the required
    lab criterion's evidence is platelets, INR and PT).
- Medication indications name no NPH diagnosis.

**Stored outputs.**
- No initial, follow-up or fallback output names an accepted label or NPH, iNPH or "normal
  pressure hydrocephalus".
- Only P06 stores a `check_drug_interactions` output (the initial output). No case stores a
  follow-up or fallback drug output, so every other drug check gets the library text.
- The P06 output names no diagnosis. Its venlafaxine sentence overlaps the CYP2D6 must in
  substance. That is the interaction content the check legitimately returns (ROUND_POLICY 6). It
  is unchanged since 06b74446, so it is kept.
- No literature output is left in any case.

**Cross-modality synthesis.** No MRI, CT, lab, ECG or echo report interprets another modality or
prescribes management. The hits were:
- the CT fallbacks giving their own Evans index;
- the MRI "CSF flow void";
- the ECG channel of the exercise tests;
- the bubble-study "no right-to-left shunt";
- the M09 EEG boilerplate "clinical correlation recommended".

One known exception was kept: the tap-test CSF report carries the post-tap TUG, 10-metre walk and
MoCA figures. This was an explicit October decision (October NPH plan, C6 item 2: the tap test is
CSF removal plus its measured response). The separate post-tap reassessment returns the same
figures. Verifiers flagged it in all batches, and it is listed below for the next physician review.

## DECLINED and NEEDS-ANDREA

None.

## Approved cases changed

None. No NPH case is approved.

## Label and code changes

- **NPH-M08** `accepted[0]`: "Secondary normal pressure hydrocephalus, post-meningitic
  arachnoiditis" became "Normal pressure hydrocephalus, possibly secondary to prior meningitis"
  (note 730a2ee7). `icd_codes[0]` G91.0 is unchanged. "idiopathic normal pressure hydrocephalus"
  and "iNPH" were removed from `rejected`.
- **NPH-P05**: `accepted[0]` is unchanged. "idiopathic normal pressure hydrocephalus" and "iNPH"
  were removed from `rejected` (note f6b2546c).
- `apply_diagnosis_synonyms.py --check --conditions nph`: "would change 0 of 600 cases".

## CENTRAL requests (consolidated)

1. **C-SYN** (`diagnosis_synonyms.yaml`; not landed as of this audit). Add to the scoped entries
   `G91.0+meningitic` (NPH-M08) and `G91.0+sah` (NPH-P05):
   - the labels "normal pressure hydrocephalus", "NPH", "idiopathic normal pressure
     hydrocephalus" and "iNPH";
   - the code G91.2.

   Then:
   - re-apply with `--prune --conditions nph`, then `--check`;
   - update the comment above the G91 block: possible iNPH (Relkin 2005) allows a remote
     antecedent judged not causal; M08 and P05 accept both readings (November 2026 physician
     ruling);
   - record the M08 label change.

   Until this lands, an "iNPH" answer scores no diagnosis credit in M08 and P05, although it is no
   longer vetoed.
2. **C-PACK** (`dataset-generation/criteria_packs/NPH.md`):
   - add `[AASLD_2020]`, `[Hoglinger_2017]` and `[AHA_ACC_perioperative_2024]` to the allow-list;
   - tiers: post-tap reassessment required in 30; labs optional 23, recommended 3 (M04, M07, S08)
     and required 4 (M03, M06, S10, M08) as pre-tap safety checks with a hard labs-before-CSF
     constraint; P03 spine MRI required; P08 drainage recommended;
   - the referral must becomes "shunt eligibility assessment", with the counselling must;
   - add `exercise_stress_test` to the waste list;
   - replace "INR 1.5 or less" with the AASLD statement;
   - section 1: secondary NPH versus possible iNPH (M08, P05).
3. **C-GUIDE** (`condition_tool_guidance.yaml` / `build_condition_tool_guidance.py`).
   `test_guidance_claims.py` has these stale NPH claims:
   - `nph/labs optional 26 recommended 4, none required`: the cases say (23, 3, 4);
   - `nph/lumbar drain required in P08`: the cases say [] (it is recommended now).

   The `perform_clinical_assessment` answer also says the drainage is "required there", and this
   should become "recommended there".
4. **C-XCOND** (for the orchestrator). Five cases outside NPH store an exercise stress test with no
   avoided label: BACT-MEN-RS03, GBS-RS16, SYNC-CARD-P02, SYNC-CARD-RM01 and SYNC-CARD-S06.
5. **C-UI**: none for NPH. No NPH note is a row-shift or null-significance display note.
6. **PD lead's request** (PD-summary CENTRAL 6: pre-MRI verification of programmable valves).
   Considered: NO-ACTION for NPH. No NPH patient has a shunt or valve (scan of all 30 patient
   blocks). The cases mention a programmable valve only as the choice if a shunt is placed, so no
   MRI in these cases is done with a valve in place.

## For the next physician review (information, nothing blocking)

- **Certainty wording of the iNPH labels (D17).** Most cases meet "probable iNPH", but
  `accepted[0]` does not say so. Changing it needs a reviewer ruling.
- **M06 and M09.** The idiopathic reading stays rejected there, because the antecedent is recent
  and plainly causal (D8).
- **The tap-test CSF report carries the post-tap measures** (October design; see the leak pass).
- **Template text in the waste-labelled exercise tests.** 21 cases share "stopped at 2.3 METs at
  2 min 30 s" (heart rate and blood pressure are per case). The tests are waste, and each case
  agrees with its own patient. The numbers were not rewritten, so as not to invent per-case data
  for an unrewarded test.
- **Unlabelled low-yield stored follow-ups** (plan section 5). These are the levodopa challenge
  (all 30), EMG/NCS, SSEP, speech-language, olfactory testing and polysomnography. They were left
  for the physicians, because some are justified (levodopa in M05 and P02, SSEP in P03).
- **Mild symmetric hip-flexor weakness** (4+/5) is not discussed in two cases. It was flagged by a
  verifier and left as a judgment call.

## Check results (17 Nov 2026, after the audit fixes)

- `perfect_agent.py` for each of the 30 cases, one id per call: 30/30 pass. The 6 cases edited in
  the audit were re-run afterwards and pass.
- `pytest test_case_guards.py -k "NPH-"`: 240 passed.
- `apply_diagnosis_synonyms.py --check --conditions nph`: "would change 0 of 600 cases".
- `pytest test_panel_case_contract.py test_red_herring_paths_resolve.py`: 4 passed.
- `pytest test_guidance_claims.py`: fails. The NPH rows are the 2 stale claims in CENTRAL 3. The
  NMDAR and MG claims fail too, outside NPH.
- `case_io.py check` on the 6 audit-edited cases:
  - schema OK, synonym guard OK;
  - the full suite has 3 failures. The only ones that name NPH are the `test_guidance_claims`
    rows.
