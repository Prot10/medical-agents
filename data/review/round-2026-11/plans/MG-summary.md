# MG: condition audit summary (November 2026 round)

Auditor pass, 17 Nov 2026, after the workers and verifiers. Plan: `plans/MG.md`. Decisions:
`plans/MG-decisions.md` (D1..D30). Audit scripts and outputs are in
`/home/aprotani/review-round-2026-11/work/scratch/mg-auditor/`:
- `book.py`: notes against rulings and logs;
- `survey_mg.py` / `survey.txt`, `classes_mg.py`: the lead's survey and class counts, re-run on the current state;
- `plan_check.py`, `plan_check2.py`: every per-case decision of the plan (tiers, stop rules, canonical texts, Q1 reasons,
  follow-up order, IVIG grams against the Devine IBW, C14, C17 items);
- `orphans_mg.py`: serves each stored report's own order and matches it against criteria and avoided actions;
- `leak_t0_mg.py`, `leak_out_mg.py`, `ddi_hits.txt`, `xmod_mg.py`: the blind leak pass;
- `fix_stragglers.py`: the audit's edits (through `case_io`).

## Bookkeeping

- There are 40 notes, all from R2 (NB-87MF-FBTV-TPWE), in 29 cases (MG-RM12 has none). Each note id appears in exactly
  one `work/rulings/<CASE>.json` (its own case), with no extra ids and only valid statuses.
- Ruling counts: **FIXED 31, CENTRAL 4, NO-ACTION 4, ALREADY-FIXED 1**. DECLINED 0 and NEEDS-ANDREA 0 as whole
  rulings. The declined parts inside FIXED rulings are listed below.
- All 30 cases changed since 06b74446, and each has a log with `## Changes`.

## Classes: how they were fixed (before = the lead's count, after = this audit, scripted over the 30)

| class | before | after |
|---|---|---|
| C1 report display (D1) | 3 notes (M01-M03) | data verified correct in all 3. CENTRAL (display) |
| C2 RNS tier (D2) | RNS required in 27 | required in 9 (M02, RM12, RP12, RS16, P01, P04, RP14, P02, RM13), recommended in the other cases with an RNS criterion. No RNS criterion in M04, RM14, RM15 (crises with RNS labelled waste or not stored). Every stop rule equals the set of required criteria |
| C3 SFEMG reasons (D3) | "reserved for seronegative" in 21 | 0. Q1 wording in every SFEMG constraint. RM11's RNS reason adds "or borderline" (its RNS is borderline, logged). SFEMG follows the core results in the 12 listed cases |
| C4 steroids (D4, D5) | "above 20 mg/day" in 25; "10-20 mg" start in 15 | 1 / 1: RS11 only (approved, kept by plan). P1 or P2 per setting. M02 and RS17 use P2/S2 rather than the plan's P1, logged: inpatient with dysphagia and nasal regurgitation or a reduced gag |
| C5 thymectomy (D6, D24) | "18-65" in 6; MGTX basis in 9 | 0 / 0. T1 in 6, T2 in 4, T3 in 6. MGTX survives only as "no benefit at 50 or over in the post hoc MGTX analysis" (T2) and in approved RM14 |
| C6 pyridostigmine ceiling (D7) | "360-480" in 4 | 0. The M1 ceiling is in every non-approved non-LEMS case except M04 (crisis: "do not escalate") and RS14 (MuSK: "cautiously at low dose, if at all") |
| C7 respiratory thresholds (D8) | Lawn thresholds in 16 cases | only in approved RM14 and RM15 (kept by plan) |
| C8 beta-blocker absolutes (D9) | 3 | 0 |
| C9 unlabelled served reports (D10) | about 90 stored reports with no criterion and no label | 0 orphan follow-ups. Every stored follow-up order is matched by a criterion or an avoided action, and no call matches both. Remaining unlabelled: the initial ECG in approved RM14, RM15 and RS11 (a reasonable test in a patient on pyridostigmine, left as neutral) |
| C10 swallow (D11) | swallow wording in 12 musts | SLT swallowing must in 23 cases, now including M03 and RP13 (added by this audit, below). The orderable criterion waits for CENTRAL C1 |
| C11 respiratory tier (D18) | 16 to upgrade | done. P03 and RS15 stay recommended against the plan's provisional list: the HPI denies dysphagia, choking and breathlessness. Logged and accepted by the verifiers |
| C12 ECG (D12) | 0 baseline-ECG criteria | `action-baseline-ecg` recommended in 24 cases, each answered by a stored ECG |
| C13 screening, early azathioprine, IVIG, severity (D13-D15, D23) | 0 / 0 / no IBW / 1 | S5 in 25 (all non-approved non-LEMS except M04: on prednisone and azathioprine for 6 years, logged). S4 in 8. IBW in every IVIG must with a dose: all gram figures match the Devine IBW from the case's height, except RP12 (dosed at his lower actual weight of 66 kg, stated). G1 in 25 |
| C14 CBA / LRP4 (D16) | 3 | P01, RP14: CBA required and in the stop rule, LRP4 recommended. P04: LRP4 required, CBA recommended. Panels split |
| C15 mediastinal MRI (D17) | 9 thymic criteria lacked it | 0 (approved RM14, RM15 and the LEMS tumour-search CT in P02, RM13 excluded). Where the library answers (16 cases), the CT shows no thymic lesion, so the normal is consistent (probed) |
| C17 case-specific (RP13 label, RS14 scenario, S02/RM16 TRAb, S05 figures, P04 contrast, M04 first order) | 6 | done. S02 `[anti_AChR, TSH, TRAb]`; RM16 has a TRAb alternative; no "~80%" or "~50%" left in S05; the M04 first order returns the respiratory study; the cardiac-monitoring waste label is removed |
| LIT, MRI-CONTRAST | n/a | no literature criterion or stored literature output in any MG case |

## Stragglers fixed in this audit (through case_io, logged under `## Verification`)

1. **Drug-interaction outputs named the undiagnosed condition** (blind leak pass). This affected 15 new-diagnosis
   cases: M01, M02, M03, P01, P03, P04, RM11, RM16, RP12, RP13, RP14, RS13, RS16, S03, S04 (30 strings). The text read
   "Myasthenia gravis: avoid fluoroquinolones...", "can worsen myasthenic weakness", "a drug of caution in myasthenia
   gravis", "exacerbate MG". These outputs are reachable by any query:
   - the initial drug output answers the first query for any drug;
   - a follow-up answers a query that names one of the patient's own drugs (propranolol, timolol, levodopa, aspirin).

   An agent could therefore read the diagnosis before ordering any test (TOOL_REPORT_STYLE_GUIDE: a drug check never
   announces the diagnosis). Each mention now names the mechanism instead: "disorders of neuromuscular transmission",
   "weakness from impaired neuromuscular transmission". The interaction content is unchanged. This was present since
   06b74446. The known-MG crises (M04, RM14, RM15) keep the disease name by design.
2. **M01 turn-0 result.** The HPI said a TSH 6 weeks ago was "mildly low, attributed to levothyroxine
   over-replacement". TSH is part of the required serology order, and a red herring rests on it. The sentence was
   deleted; nothing else referred to it. Present since 06b74446.
3. **C10 straggler** (M03, RP13). Both have oropharyngeal dysphagia: M03 has difficulty with solid boluses and weight
   loss, and starts steroids in hospital for bulbar weakness; RP13 has occasional choking on liquids. Neither had a
   swallowing must. Each now has the canonical "Arrange a speech and language therapy swallowing assessment because ...
   (Jacob 2025)". For RP13 this also answers the clinical point of the verdict (choking on liquids, ABN SLT
   assessment), and its ruling was updated.

All 15 edited cases were re-checked:
- `perfect_agent.py` passes;
- `case_io.py check`: schema OK, synonym guard OK, and no test failure names them;
- `test_case_guards -k MG-` passes.

## Blind leak pass

- **Turn 0** (rendered with the real `format_patient_info`):
  - Own diagnosis named only where it is by design:
    - known MG in crisis (M04, RM14, RM15);
    - the aunt with MG in M02 (family history, flagged in October);
    - the outside neurologist's "essentially excluding myasthenia gravis" in P04 (a designed wrong anchor, October
      DX-NAMED).
  - Results present at turn 0 are earlier history, outside the scored work-up:
    - prior negative AChR/MuSK serology in seronegative P01 and P04 (the CBA, LRP4 and SFEMG are what is scored);
    - RP13's absent ice-pack response decades ago;
    - RM16's known Graves serology;
    - RS14's prior brain MRI and muscle biopsy (real-case seed, before this admission);
    - surveillance CTs before the encounter (P02, RM13, RP12).

    After fix 2, none gives a result that a criterion orders now.
- **Stored outputs any query can reach:**
  - After fix 1, no drug-interaction output (initial, follow-up, fallback) of a new-diagnosis case names MG or LEMS.
  - The 7-gram shingle echo test finds no drug output repeating an expected_evidence. It does find:
    - approved RM13, whose amifampridine output repeats the dosing that its must states (legitimate label content);
    - RM15, whose atracurium output overlaps its own criterion's evidence.
  - Lab interpretations that name MG ("AChR antibodies are found in most patients with generalized myasthenia gravis";
    "a negative result does not exclude myasthenia gravis") are serology stating what it tests for (Kind 2), and are
    returned only to an antibody order.
- **Cross-modality synthesis:** none. The scan hits are each report's own modality, CT indication lines, comparisons
  with earlier studies of the same modality, and one allowed further-diagnostic-step sentence (M02 RNS: "single-fiber EMG
  would increase sensitivity").

## DECLINED parts and NEEDS-ANDREA

NEEDS-ANDREA: none.

Points declined inside FIXED or CENTRAL rulings, with the reason recorded in each ruling:
- **P04: the OR equivalence** (clustered AChR accepted for the LRP4 action). Its premise was that the clustered AChR
  order returned the LRP4 result. After the panel split it does not, so that order cannot establish the LRP4 label (D16).
- **RP14: removing NUDT15** from the azathioprine pre-test. CPIC 2019 (Relling, Clin Pharmacol Ther 2019;105:1095-1105)
  recommends genotyping both TPMT and NUDT15; TPMT stays first (D14).
- **M04, P04, RS13, RS15, RS16: rewriting the speech-language battery into a swallow study.** `costs.yaml` defines
  `speech_language_evaluation` as motor speech and language, so the battery is labelled waste and a swallow term is
  requested (D11, CENTRAL C1).
- **RS14: TORCH in the pre-rituximab screen.** It is a pregnancy screen with no role in a 75-year-old man (D22).

## Approved cases changed

| case | change | reason |
|---|---|---|
| RS11 | neurophysiology (RNS or SFEMG) required -> recommended, out of the stop rule; `metadata.difficulty_rationale` count | D2, the reviewer's identical ruling in S05 |
| RM13 | 4 waste labels (chest X-ray after CT, gait battery, levodopa challenge, speech battery) | D10 |
| RM14 | 5 waste labels (ice pack, gait, levodopa, speech, orthostatic BP) | D10 |
| RM15 | 7 waste labels; the speech battery report no longer lists normal test scores under "not performed: intubated and sedated"; the PET waste label gains the `whole_body_FDG_PET` alternative | D10; internal contradiction; an unlabelled served order |

All four go back to re-review. The audit made no further change to them.

## Label and code changes

- **MG-RP13 accepted[0]** (D20). Was "AChR antibody-positive generalized myasthenia gravis, presenting as long-standing
  'ocular' disease previously misdiagnosed as chronic progressive external ophthalmoplegia". Now "New-onset AChR
  antibody-positive generalized myasthenia gravis (MGFA class IIb) superimposed on long-standing ptosis and
  ophthalmoparesis previously labelled CPEO; a coexisting mitochondrial myopathy is not excluded without muscle biopsy".
- **MG-RS14 `rejected`**: "progressive supranuclear palsy" and "PSP" were removed (D22: a possible coexisting condition).
- No `icd_codes[0]` change. G70.01 is still granted to the stable cases, pending CENTRAL C4.

## CENTRAL requests (consolidated)

1. **C1 vocabulary, swallow assessment** (`costs.yaml`, `fallback_library.yaml`, `review_api/services/tool_io.py`).
   Add `perform_clinical_assessment` `swallow_assessment` (bedside SLT swallow evaluation, CPT 92610), with a library
   normal and the mirror. Optionally add `videofluoroscopic_swallow_study`. Not landed this round. Afterwards add
   `action-swallow-assessment` (recommended; optional in S02) with a stored report in M01, M02, M04, P01, RP12, RP14,
   RS12, RS14, RS15, RS16, RS17, S01, S02, S03, S04, and consider M03 and RP13.
2. **C2 vocabulary, `clustered_MuSK_cell_based`** (interpret_labs; library normal; mirror). Not landed. Then the CBA
   alternative becomes `[clustered_AChR_cell_based, clustered_MuSK_cell_based]` in P01, RP14 and P04.
3. **C3 review-app display** (CENTRAL.md items 2 and 3):
   - print label keys first and null as "not stated" (M01-M03 rows);
   - show a criterion's discriminator next to the tool name in stop rules and constraints (M04, P01, P02, P04, RM11).
4. **C4 synonyms** (`diagnosis_synonyms.yaml`):
   - G70.00 entry: drop G70.01, keeping it only for M04, RM14 and RM15 (D21);
   - add "AChR antibody positive myasthenia gravis" and "seropositive myasthenia gravis" / "seropositive MG", scoped to
     the AChR-positive cases (not P01, P04, RP14, RS14);
   - record the RP13 relabel;
   - re-apply with `--prune --conditions myasthenia_gravis`.
5. **C5 criteria pack** `dataset-generation/criteria_packs/MG.md`: the tiers of D2/D12/D16/D18, the canonical texts
   (P1/P2, S1-S5, T1-T3, M1, R1, I1), the Q1 reasons, and the new keys `[Fionda_2026]`, `[Relling_2019]`,
   `[Virani_2023]`.
6. **C6 generator** `conditions.yaml` myasthenia_gravis block: the same tiers, so new cases do not bring back
   RNS-required, the 20 mg prohibition or "MGTX 18-65".
7. **C7 new, MockServer drug check** (`agent-platform/src/neuroagent/tools/mock_server.py`, the
   `check_drug_interactions` branch of the initial-output match). A query for any drug that is not stored receives the
   first stored drug output. In MG that output proposes pyridostigmine, so an agent that checks the patient's
   lisinopril reads a pyridostigmine interaction report. That is a strong pointer to the diagnosis, even after fix 1.
   Suggested: answer only an exact or token match of the drug, else the library or a "no stored interaction data"
   result. Then re-run the perfect-agent check over all 600 cases, since some drug criteria may rely on the
   first-output rule.
8. **Guidance claims** (`condition_tool_guidance.yaml` / `build_condition_tool_guidance.py`; orchestrator). Three MG
   claims are stale in `test_guidance_claims.py`:
   - "mg/brain MRI in 3 cases, required in 1": app (3, 1), cases (6, 1);
   - "mg/RNS required in 27": app 27, cases 9;
   - "mg/SFEMG ordered in 25: required 5 (2 as RNS alternative), recommended 3, optional 17": app (25, 5, 3, 17), cases
     (26, 3, 5, 18).

## Check results (17 Nov 2026, after the audit's edits)

- `perfect_agent.py`, one id per call: **30/30 pass**. The only warnings are the `mediastinum_MRI` alternative answered
  by the library normal in 16 cases, which is consistent with each case's normal thymic CT (probed).
- `pytest agent-platform/tests/test_case_guards.py -k "MG-"`: **240 passed**.
- `apply_diagnosis_synonyms.py --check --conditions myasthenia_gravis`: **would change 0 of 600**.
- `pytest test_panel_case_contract.py test_red_herring_paths_resolve.py`: **4 passed**.
- `pytest test_guidance_claims.py`: 1 failed. Its three MG claims are listed in CENTRAL 8; the other failing claims
  belong to other conditions.
- `case_io.py check` on the 15 edited cases: schema OK, synonym guard OK, and no failure names an MG case. The 3
  suite failures belong to other conditions or to the central claim test.
