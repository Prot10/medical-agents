# SAH: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Sources: the plan (`plans/SAH.md`), the 30 case logs
(`logs/SAH-*.md`, each with a worker table and a verifier section; ten now also have a "Condition
audit" section), the notes (`notes/SAH.json`, 44 notes, all from Reviewer 2, in 23 cases) and
scripted checks over the 30 case files.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass. `case_io.py check` on all 30 ids: schema OK and
  synonym guard OK for every case; no test failure names an SAH case. `test_case_guards -k SAH`:
  60 passed.
- Every one of the 44 note ids appears in exactly one log (its own case), in one table row, with a
  ruling.
- Scripted uniformity checks over the 30 files (all clean after the audit fixes below):
  - Canonical musts present as the plan assigns them: MUST-NIMO, MUST-SECURE (as early as
    feasible, preferably within 24 h, `[Hoh_2023]`), MUST-ICU, MUST-DCI in all 30 (P02 has its
    intended non-aneurysmal nimodipine must and no MUST-SECURE). One securing must per case (M07
    and S04 mention coiling a second time only inside MUST-REVERSE). MUST-BP-A or MUST-BP-B per
    plan; MUST-QT, MUST-LVEF and MUST-ALCOHOL in their cases; MUST-EVD-NOW in M02, M05, M07, P04
    and RS12 only; MUST-REVERSE in M07 and S04.
  - Canonical nimodipine and BP prohibitions and the four canonical pearls in all 30.
  - No "24-72" or "24-48" securing text, no triple-H, no "Exclusion" panels, no free-text
    citations, no management content in tool outputs.
  - Order: criteria and follow-ups NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD,
    literature (CT-negative P01, P03, P06 with CSF after labs). DSA criterion
    `dsa-aneurysm-anatomy` recommended in all 30. The canonical literature output is identical in
    all 30, last, optional; no initial literature or drug-check blocks.
  - Constraints: soft NCCT before CTA and CTA before DSA everywhere; hard reversal before DSA in
    M07 and S04; hard NCCT before CSF and soft labs before CSF in P01, P03, P06.
  - Stop rule: `required_before_assessment` equals the required criteria in all 30, and
    `max_additional_actions` is 1.
  - LP avoided action `contraindicated` in M02, M05, M07, P04, RS12, S04 (mass effect,
    hydrocephalus or anticoagulation) and `harm` elsewhere; none in P01, P03, P06. CSF exemptions
    correct.
  - Labs: magnesium and potassium in all 30, flags match ranges, no duplicate analytes,
    type-and-screen significance null. Abnormal-value summaries carry values and flags only.
  - TCD canonical (admission baseline at day 0; M08 day 3, P01 day 5, P03 day 1 by presentation).
    Telemetry 3 to 5 h, case-specific.
  - Differential all `low` or `very_low`, except PRES `high` in P05 (co-existing by design).
  - `metadata.case_body_concerns` empty everywhere.

## Error classes and how each was fixed

| class | defect | notes | fix |
| --- | --- | --- | --- |
| C1 securing window | "Within 24-72 hours" in musts and pearls (91 occurrences), "24-48 hours" in literature; no securing pathway. | 09f3f88b, 25ff44d7, 38447471, 4daa3aa1, 53d4e407, 66c7702e, 6dcebd64, 899fabe8, 9b8af8ad, a60d0697, c3c56bb2, cabb6393, f87e2dd7, f8f0befa, fddcb39d | One MUST-SECURE per case naming the aneurysm, "as early as feasible, preferably within 24 hours" `[Hoh_2023]`; canonical securing pearl. P01 (day 5) and other late presenters reworded so the instruction can be followed (verifier). |
| C2 pathway order and timeline | Drug checks, literature or echo before the CTA; TCD and lab follow-ups dated days 2 to 8 in patients hours from onset. | 61a944ea, bf848453 | Criteria and follow-ups in plan 3.1 order; TCD as admission baseline; follow-up timings fit the presentation. |
| C3 catheter DSA | DSA absent in 27 cases, mislabelled "CTA-occult" in M01 and M03, DSA outputs reporting treatment. | 09f3f88b, 25ff44d7, 66c7702e, 899fabe8, 9b8af8ad, a60d0697, c3c56bb2, cabb6393, fddcb39d | Recommended `dsa-aneurysm-anatomy` in all 30 with a diagnostic-only output consistent with the CTA (size, neck, dome-to-neck ratio, branches, no vasospasm); soft CTA before DSA. |
| C4 nimodipine | Must and IV prohibition misworded. | 5d5b5879, 60a5d171, 75c2bb0f, bf848453, db7c626e | MUST-NIMO with the 30 mg every 2 h adjustment and the canonical parenteral-injection prohibition; nimodipine notes ALREADY-FIXED for the must itself. |
| C5 BP before securing | No BP action, held home antihypertensives, invented targets. | 03f424a3, 2ab931d5, 2b67f747, 4f899419, 60a5d171, 633fd9a3, 6e139dfe, b12f861e, db7c626e, f6edc7fb, fb64b259 | MUST-BP-A or MUST-BP-B per the plan's assignment; case-specific MUST-HOME; canonical BP prohibition. P02 BP must ends at the DSA that excludes an aneurysm (verifier). |
| C6 hydrocephalus and EVD | Template EVD must in cases whose CT shows no hydrocephalus. | 9d172604, da99e9e0, f87e2dd7 | MUST-EVD-NOW only in M02, M05, M07, P04, RS12; removed from M06 and M08. |
| C7 literature as steps | Recommended literature criterion; patient-specific or wrong literature content; initial literature blocks. | 6a4a8415, 6b4234fb | One canonical general-evidence output, optional and last; initial blocks removed. |
| C8 drug-check template leaks | Empty `initial_tool_outputs.drug_interactions.general` blocks; treatment disguised as a check. | (survey) | Blocks removed; drug checks are follow-ups listing the patient's real medicines. |
| C9 QTc and electrolytes | No magnesium in any case, potassium missing in 14; QTc 500 ms or more without action. | 7f1b4f47, c621cf95, e38a8460 | Magnesium and potassium in all 30; MUST-QT where QTc is prolonged. |
| C10 drug-check content and tier | Triple-H, andexanet thresholds, PCC dosing errors; wrong tiers. | (survey) | Removed or corrected; tiers per the plan's C10 list. |
| C11 differential and red herrings | Five-entry generic differential in 25 cases; template red herrings. | 03a9ce4b, 9bd81d95 | Canonical case-specific key features; red herrings rewritten to the case data (see the audit row below). |
| C12 telemetry | Identical telemetry report in all 30, over 24 h. | (survey) | Case-specific 2 to 6 h stroke-unit telemetry. |
| C13 exam and grade | "Alert and oriented x4" beside GCS 14; grade labels inconsistent with the exam. | (survey) | Mental status matches the grade; HPIs aligned with the exam (M07 verifier). |
| C14 reports doing the agent's work | Cross-modality and clinical commentary in CT observations; LP recommended after a positive CT. | (survey) | Removed; CT recommends CTA. |
| C15 CSF in CT-negative cases | Contradictory xanthochromia and tube counts (P01, P03, P06). | (case-specific) | Coherent tube 1 versus tube 4 counts and spectrophotometry consistent with the time since onset. |
| C16 echo and other criteria | Echo labels, P01 orphan echo. | (survey) | As plan. |
| Case-specific | Late-presentation CT and LP reasoning, rebleed figures, M07 wording. | ee9a1623, 532566ea, 348b8e71, 7e2fa463, aa75afaa | As in plan section 4 (point estimates the evidence does not support were not written; see below). |
| Found by the audit (class) | Labs `abnormal_values_summary` named interpretations ("leukocytosis", "stress hyperglycemia", "neurogenic" troponin, which gives away the cardiac red herring). | none | Rewritten to values and flags in RS12, S01, S02, S03, S04 (workers had already done S05 to S10). |
| Found by the audit (class) | ECG "Sinus tachycardia" at a rate of 98 (S01); "(neurogenic pattern)" on the ECG T-wave finding (RS11). | none | "Sinus rhythm, rate 98" with matching criterion evidence; attribution removed. Same fixes as the verifiers made in M01, M04, S10, P08. |
| Found by the audit (class) | Red-herring template "echocardiogram showing apical ballooning confirms etiology" where the echo shows only mild apical hypokinesis (M04, S09, S10). | none | Interpretation now states the actual echo (LVEF 54% in M04; preserved EF in S09, S10), as the verifiers did in S01, S04, P05, P06. |
| Found by the audit | M04 MUST-HOME decided only metoprolol (also on metformin and atorvastatin, glucose 198). | none | Metformin held in critical care with insulin for hyperglycemia, atorvastatin continued; matches S02, RS12, S09. |
| Found by the audit | S07: MRA waste entry removed (reasonable with a contrast rash), but an MRA order returned the fallback "No abnormality identified" against the CTA and DSA. | none | New MRA follow-up (TOF, 5.3 x 4.7 mm right paraclinoid ICA aneurysm); simulation confirmed. |

## Counts

- Reviewer notes (44, R2 only, 23 cases):
  - FIXED: 37 notes.
  - ALREADY-FIXED: 1 note (M07 75c2bb0f).
  - Mixed: 5 notes ALREADY-FIXED for one part and FIXED for the rest: M07 da99e9e0, M08 5d5b5879,
    P03 7e2fa463, RS12 f87e2dd7, S04 60a5d171.
  - Mixed DECLINED/FIXED: 1 note (M06 c621cf95).
  - BLOCKED: 0.
- Own findings:
  - Workers: 456 logged; 454 FIXED, 1 FLAGGED (RS11: Hunt-Hess grade stated in the patient
    block, a condition-wide decision) and 1 no-change (P02 label kept per ruling 3).
  - Verifiers: further changes in at least 20 cases (M01, M02, M04, M06, M07, P01, P02, P04, P05,
    P06, P08, RP11, RS12, S01, S02, S04, S05, S06, S09, S10).
  - Auditor: 12 changes in 10 cases (RS12, S01, S02, S03, S04, RS11, M04, S09, S10, S07), each
    logged under "Condition audit" in that case's log. A further 6 findings were flagged and not
    changed (see CENTRAL 9 and 10, and open questions 10 and 11).
- Cases changed: 30 of 30.
- Approved cases changed: 14 of 14 confirmed approvals (M05, M06, P01, P02, P05, RM11, RP11, S01,
  S04, S06, S07, S08, S09, S10), each for logged real errors, plus all 7 probable approvals with no
  status in the notes file (P04, P06, P07, RS11, S02, S03, S05). The audit changed the approved
  S01, S04, S07, S09 and S10 and the probably-approved RS11, S02 and S03, for real errors only.

## DECLINED and BLOCKED notes

- M06 `c621cf95`: DECLINED for its facts, FIXED for its class. Reason: the note's text copies the
  facts of SAH-M05 (QTc 524, K 3.4, furosemide, U waves). In M06 QTc is 478 ms, K is 3.7, there is
  no furosemide and there are no U waves, so a QT must built on those facts would be false. The
  class (magnesium and potassium measured, QTc addressed) is applied.
- Parts of notes not applied as written (the notes themselves are FIXED):
  - M08 `ee9a1623`: the "20-50%" early rebleed figure was not written; published early rebleed is
    about 4 to 14% in the first 24 h.
  - P01 `348b8e71` and P03 `7e2fa463`: point estimates of CT sensitivity by day were not written;
    the canonical sensitivity fact is used.
  - M07 `4daa3aa1` and P03 `6dcebd64`: the note's own "24-72 h" was replaced by the Hoh 2023
    window.
- No note is BLOCKED.

## CENTRAL requests (consolidated)

1. **Criteria pack** `dataset-generation/criteria_packs/SAH.md`: correct the Perry_2011 title;
   add `[Perry_2013]`, `[Molyneux_2002]` and `[Drew_2010]` to the allow-list; replace "24-72h"
   with "as early as feasible, preferably within 24 h"; mark the literature and drug-check
   "required" tiers superseded by rulings 5 and 6; correct the xanthochromia timing to about 12 h;
   make TCD optional.
2. Allow-list the ESO/EANS/ESMINT 2026 SAH guideline key once Andrea supplies the reference.
3. **Synonyms** (`diagnosis_synonyms.yaml`): P02 (I60.8, non-aneurysmal perimesencephalic SAH)
   must not accept the aneurysmal labels or the I60.0 to I60.7 codes.
4. **Review UI:** show outputs, including the initial work-up, in criterion order.
5. Optional citation keys: SAHaRA (English 2024, NEJM; P06 transfusion must) and
   `[Thompson_2015]` (RM11 family screening).
6. RS12 `accepted[0]` corrected within the condition ("large" and "with severe DCI" removed);
   ICD I60.2 unchanged. Regenerate its synonyms if the central tool keys on the label.
7. **`perfect_agent.py`:** check that `required_arguments` keys exist in the tool schema (P06
   MRI `sequences` passed only because annotation keys are ignored).
8. **Review app:** flag note text duplicated across cases (M06 note copied from M05).
9. **Fallback (condition-wide):** `fallback_tool_outputs.cardiac_monitoring` is a 24 h Holter
   report in all 30 cases, which cannot exist at assessment time. Replace it with a short
   telemetry report.
10. **Fallback library and off-pathway imaging:** in CT-positive cases, off-pathway brain MRI,
    MRA and CT perfusion are answered by library or case fallbacks that report a normal study
    (for example "no susceptibility artefact on SWI", "No abnormality identified"), which
    contradicts the SAH. Needs a central decision: SAH-aware fallbacks per case, or a library text
    that does not assert absence of blood. S07 MRA now has its own follow-up.

## Open questions for Andrea (consolidated)

1. **EVD with GCS 15** in M02 and RS12 (plan question 1): MUST-EVD-NOW is kept because of early
   hydrocephalus with third-ventricle blood.
2. **DSA tier** (plan question 2): recommended in all 30. In P02 (perimesencephalic, CTA negative),
   should DSA be required?
3. **P02 nimodipine duration** after a negative DSA (plan question 3): the must leaves completion
   of 21 days to the neurovascular team.
4. **Citations** (plan question 4): ESO 2026 and AANN 2025 references to supply or confirm.
5. **Grade-range labels** (plan question 5): M03 "HH 2-3", S05 "HH 1-2" (the exam is now grade 2),
   M08 "Fisher 2-3". Pick one grade each or accept the ranges.
6. **Approval status** of the 7 cases with no notes and no status (P04, P06, P07, RS11, S02, S03,
   S05) (plan question 6). All were changed this round.
7. **RP11:** lymphocytes changed from 0.8 to 4.4 and the natalizumab timing wording rewritten;
   confirm.
8. **"Hunt-Hess Grade N" in the patient block** in all 30 cases (RS11 flag): the grade is a
   clinical judgment the agent should make; keep it in the exam or remove it everywhere.
9. **P08** field ECG kept in the HPI (the verifier agreed; informational).
10. **Echo wording:** many echo reports use "mild Takotsubo" or "apical ballooning" labels while
    the impression says "pattern"; left as Kind 2 echo wording. Confirm or ask for neutral wording.
11. **Left unchanged by the audit, confirm:** the "Late presentation (>24 h)" pearl in M08, P01 and
    P03; no home-drug must for sertraline (M03) or rosuvastatin (M07), since the drug checks cover
    them; the P04 exam note that clonazepam may lower the GCS (the intended distractor).
