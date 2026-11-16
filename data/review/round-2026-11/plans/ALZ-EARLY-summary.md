# ALZ-EARLY: condition summary, November 2026 round

Auditor's summary for the 30 ALZ-EARLY cases (16 Nov 2026). Plan: `ALZ-EARLY.md`. Decisions:
`ALZ-EARLY-decisions.md`. Base: commit 06b74446. Audit scripts:
`/home/aprotani/review-round-2026-11/work/scratch/alz-auditor/` (audit_alz.py, leak_alz.py, screen_cmp.py,
xmod.py, counts.py, fix_ms.py, fix_ct.py).

- Notes: 85, all R1, in 19 cases.
- Approved cases (work/approved.txt): none in ALZ-EARLY, so no approved case was changed.
- All 30 case files differ from 06b74446. Each has a log in `logs/<CASE>.md` with '## Changes' and
  '## Verification'.

## 1. Rulings

| status | count |
| --- | --- |
| FIXED | 34 |
| CENTRAL | 44 (43 neuropsych-flag display notes, plus RP05 835caa5b on the same display issue) |
| NO-ACTION | 7 (case comments, decision 15) |
| ALREADY-FIXED | 0 |
| DECLINED | 0 |
| NEEDS-ANDREA | 0 |

- Each of the 85 note ids appears in exactly one `work/rulings/<CASE>.json` (the case it belongs
  to), with a valid status and a non-empty `what`.
- The 11 cases without notes have an empty rulings file.

## 2. Classes: counts at 06b74446 and now (counts.py, by case unless stated)

| class | how fixed | before | after |
| --- | --- | --- | --- |
| LIT (class from commit 393c547e) | checked: no literature criterion or output remains | 0 | 0 |
| C1 NP-FLAG-DISPLAY | CENTRAL display; every row was checked against its own range | 43 notes | data correct |
| C2 S06 TMT-B flag | flag set to "yes", impression aligned | 1 | 0 |
| C3 stop rule: `max_additional_actions` not 0 | set to 0 | 30 | 2 (M01, M03, see below) |
| C3 FDG-PET criterion | deleted in P01, P02, RM04, RP01, RP02 and RP03; kept in P03 | 7 | 1 |
| C3 FDG-PET waste avoided action | added | 0 | 22 |
| C3 perfusion SPECT waste avoided action | added | 0 | 29 (all but P03, see below) |
| C3 RP04 amyloid PET waste | added | 0 | 1 |
| C3 follow-up order: credited, then second amyloid alternative, then on request | reordered | not ordered | 30/30 in order (script check through MockServer) |
| C4 abnormal lab rows with null significance (sodium, chloride, BUN and glucose excluded) | filled with plan texts | 45 rows | 0 |
| C5 "no medicine is approved for MCI" | canonical must; S06 educational point | 6 | 0 |
| C6 glycaemic target (RS05, M02) | ADA 2026 wording | 2 | 0 |
| C7 RS06 MRI pair | plain MRI required; gadolinium MRI optional, with a soft constraint | 1 | 0 (mri_probe clean) |
| C8 RS06 red herring; C9 S02 statin | fixed | 2 | 0 |

### Justified deviations from the plan

The verifiers made these and I re-checked each one. I kept them.

- **M01 and M03 keep `max_additional_actions` 1.** The CSF is borderline (M01 Abeta42/40 0.060)
  or intermediate (M03 0.053, tau high-normal).
  - October physician rulings 88980d7d (M01) and aec83190 (M03) say amyloid PET stays an option.
  - NICE NG97 1.2.15: if the first test is not diagnostic, consider the other.
  - Decision 7's reason (no second biomarker after a conclusive CSF) does not apply here. The plan
    already exempts these two cases from the FDG label for the same reason.
- **P03: perfusion SPECT is a second alternative of the FDG criterion, not waste.**
  - P03's imaging question is suspected FTD. NICE NG97 1.2.23 says "use either FDG-PET or perfusion
    SPECT".
  - The "SPECT only if FDG-PET is unavailable" wording is 1.2.15, the Alzheimer recommendation.
  - The criterion is claimed once, so a second scan is still uncredited.
  - Plan C3.4 and decision 6 should read "SPECT waste in the 29 cases whose imaging question is the
    Alzheimer subtype".
- **FDG waste rationale variants.** Each keeps the canonical meaning and `[NICE_NG97]`:
  - RS05: "supportive CT", because MRI is not possible (claustrophobia).
  - S06: "amnestic mild cognitive impairment"; S06 is an MCI case missing from the plan's MCI list.
  - RP04: names the required CSF as the confirmatory test, plus the CJD clause.
- **P03 genetics split.** The FTD panel and the APP/PSEN1/PSEN2 panel are now two optional
  criteria. The label always asked for both, and with an allowance of 0 the second panel would have
  been penalised.
- **S02 statin intensity: high, not moderate (plan C9).**
  - ADA Standards of Care, section 10: high-intensity statin for diabetes at 40 to 75 years with
    ASCVD risk factors.
  - S02 has hypertension and is a former smoker.

## 3. Stragglers fixed by this audit (all through case_io; logged under '## Verification')

1. **EXAM-SCREEN (leakage, major, 30/30).** The bedside screen results were in
   `patient.neurological_exam.mental_status`, and in RM01 also in `additional`:
   - what was there: MMSE and MoCA totals with item losses, delayed recall with the cue response,
     clock drawing, pentagon and cube copy, fluency counts, digit span, serial sevens, Trail Making
     B (RM01);
   - why it is a leak: these are exactly what the required `perform_clinical_assessment`
     (cognitive_screen) criterion returns. Its expected evidence starts with those scores, and the
     August generation commit 63f9e934 had copied them out of the exam.
   - The October FTD audit fixed the same class in FTD and wrongly recorded ALZ-EARLY as already
     clean.

   Fix:
   - Those results were removed from the exam. Orientation, speech, naming, repetition,
     comprehension, behaviour, insight and frontal signs are kept verbatim.
   - A script confirmed that every removed number is in the stored clinical-assessment or
     neuropsychology report. The two exceptions are trivial: the M02 clock-hand position and RM03
     abstraction 2/2, which is normal.
   - RM01 `additional` is set to null.
   - M01 `red_herrings[2]` now points at the assessment report, and its interpretation no longer
     cites a "MoCA 22/30" that does not exist in M01.
   - Kept on purpose: three HPIs keep the screen the primary care physician did before the referral
     (M02 27/30; RP04 22 then 18 over two months; S06 28/30). These are pre-encounter history that
     frames the referral (the S06 reassurance premise, the RP04 rate of decline), not the
     assessment's own result.
   - Result: turn-0 screen overlap went from 30 cases to 0, apart from the S06 referral MMSE.
2. **CT-FALLBACK-GENERIC (consistency, minor, 24 cases).** The workers flagged this condition-wide.
   - Problem: `fallback_tool_outputs.ct` answered any head CT with empty findings and "No acute
     intracranial abnormality", or with partial text (M05, RM02). That omits what CT shows of the
     case's own MRI.
   - Fix: rewritten from the case's MRI, limited to what CT shows: medial temporal and cortical
     volume loss, white matter low attenuation, lacunes, ex vacuo ventricles. No Scheltens or Fazekas
     grades, no microbleeds, a technique and sensitivity note, and no diagnosis named.
   - Empty-findings CTs went from 29 to 2:
     - RS05: the real CT is the initial study.
     - RS06: the impression already lists the findings.
   - The 8 others had been fixed by the workers.
3. **SPECT-TEMPLATE (28 cases).** The on-request SPECT carried the identical ratio "0.78-0.84
   (normal above 0.90)". `quantitative_data` is now null; the visual read is unchanged. P03 keeps its
   case-specific values.
4. **TAU-TEMPLATE (23 cases).** The on-request tau PET SUVR was shared across cases (1.78 in 16 cases,
   1.71 in 4, 1.42 in 3). It is now null where shared. The impression still states positivity, and
   the 7 case-unique values stay.

## 4. Blind leak pass (results)

- **Turn 0 (`format_patient_info`), checked by script and by reading:**
  - No accepted label and no case-sensitive acronym (AD, MCI, PCA, lvPPA, EOAD, DLB, bvFTD) appears.
  - Medication indications are diagnosis-free.
  - "Dementia" and "Alzheimer" appear only in family history (relatives' diagnoses).
  - "CJD" appears only as RP04's referral question, which is the mimic.
  - The remaining numbers in past medical history are chronic-disease history, not the decisive
    result of any criterion: prior HbA1c, M05 eGFR 44 for known CKD G3b, M04's "B12 a little low",
    and M05's vague prior CT "white matter changes".
- **check_drug_interactions outputs (initial, follow-up, fallback):**
  - None names the diagnosis or "dementia".
  - The only overlap with expected evidence is the drug-check criterion's own evidence (RM03, RP01,
    RP02).
- **Cross-modality scan over every stored report:** no synthesis. The hits are anatomy terms ("CSF
  spaces"), technique notes (RS05 CT, RS05 FDG attenuation correction), RM02 FDG "ventricles as on
  MRI", and Kind 2 statements (CSF "Alzheimer biomarker pattern", FDG "Alzheimer-type metabolic
  profile").

## 5. Label and code changes

None: `accepted[0]` and `icd_codes[0]` are unchanged in all 30 cases, and no synonym was edited.

## 6. CENTRAL requests (consolidated)

1. **Review app, on-request follow-ups** (`web-review/src/components/cases/CaseDetail.tsx`,
   `PathwaySection`): show follow-ups that match no criterion under "Served only if ordered", and
   label second alternatives "alternative to step N". This covers the ALZ notes in RM03, RM04 and
   RP01-RP05.
2. **Review app display** (CENTRAL.md items 1 and 2): render null as "not stated", and print label
   keys before value and flag. This covers 44 neuropsych-flag notes and 6 lab-significance notes.
3. **StopRule rationale** (`packages/neuroagent-schemas` `evaluation.py`): add an optional
   `rationale` string, shown in the app with "actions that match an optimal action never count
   against the allowance". It answers R1's 7 stop-rule notes.
4. **Criteria pack** `dataset-generation/criteria_packs/ALZ-EARLY.md`:
   - section 2: FDG optional only in P03 (with perfusion SPECT as its NICE 1.2.23 alternative);
     FDG waste in 22 cases; SPECT waste in the 29 Alzheimer-subtype cases;
   - section 5: stop rule 0, except 1 where the first amyloid test is borderline (M01, M03);
   - RS06 MRI: plain required, contrast optional;
   - section 7: the MCI wording per C5;
   - the turn-0 exam carries no screen totals or item scores (EXAM-SCREEN);
   - allow-list: `[EANO_meningioma_2021]`.
5. **Citation registry**: add `[EANO_meningioma_2021]` (Goldbrunner R et al., Neuro Oncol
   2021;23(11):1821-1834).
6. **Guidance claims** (`build_condition_tool_guidance.py` ALZ responses and
   `test_guidance_claims.py`, maintained centrally). The failing claim "alz/FDG optional in 7" must
   become 1, in P03, with a SPECT alternative. Add: SPECT waste in 29 cases; RS06 MRI plain-required
   with optional contrast.
7. **Optional guards**:
   - a neuropsych row whose value falls outside its own range must not carry the opposite flag;
   - the turn-0 exam must not contain a score that the case's cognitive-screen output reports
     (screen_cmp.py logic);
   - no quantitative value may repeat verbatim across more than N cases of a condition.
8. **Metadata** `fallback_tool_kinds.ct` still reads "normal" in the cases whose CT answer now
   reports atrophy. No code reads it (grep of `agent-platform/src`, `packages`, tests). Either drop
   the key dataset-wide or define its vocabulary.

## 7. Open questions

- None for Andrea.
- For the physicians at re-review:
  - max_additional_actions is 0 (1 in M01 and M03).
  - FDG-PET is uncredited outside P03.
  - The bedside screen now appears only in the cognitive assessment report.
  - A remark for the record, not acted on: the S and RS batteries use the 25th-75th band as the
    abnormality cutoff (D2).

## 8. Check results (after the last edit)

- `perfect_agent.py <id>`, one id per call: 30/30 pass, no warnings.
- `audit_alz.py`: no class defect. The only lines it prints are the deviations listed in section 2.
- `pytest test_case_guards.py -k "ALZ-EARLY-"`: 240 passed.
- `apply_diagnosis_synonyms.py --check --conditions alzheimers_early`: would change 0 of 600.
- `pytest test_guidance_claims.py test_panel_case_contract.py`: 4 passed, 1 failed.
  - The failure's only ALZ line is "alz/FDG optional in 7: the app says 7, the cases say 1". That is
    the intended effect of decision 5, and it is CENTRAL item 6.
  - The other lines in that failure belong to FEPI-TEMP, FTD and MS-RR.
  - `test_panel_case_contract` passes.
- `mri_probe.py`: RS06 pair correct; no unpaired gadolinium text in any ALZ case.
- `case_io.py check` (full suite, 6535 passed, 2 failed): schema OK, synonym guard OK. No failure
  names an ALZ-EARLY case; the 2 failures are the central guidance-claim tests.
- No em dash was added: 0 in the added lines of `git diff 06b74446` for the 30 cases.
