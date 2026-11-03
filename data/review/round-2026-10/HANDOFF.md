# Handoff: October 2026 review round (25 Oct 2026)

Branch `fix/review-round-2026-10`, everything committed and pushed to origin (no PR); deployed
to the review VPS on 25 Oct 2026. The case-by-case round is finished: all 20 conditions (600 cases) are fixed,
verified, audited and closed out, and the cross-condition MockServer work is landed. Read, for
any follow-up: this file, `ROUND_POLICY.md`, `PATTERNS.md`, `CENTRAL_PENDING.md` (the open items),
`plans/<COND>-decisions.md` (per-condition decisions and the physicians' items). The skills
`claude-workflow-fanout` and `neurobench-case-serving` have the lessons learned.

## Standing rules from Andrea (24 Oct 2026)
- Open questions: decide them "nel modo migliore per la qualità del dataset", apply, record the
  reason. Ask Andrea only for information only Andrea has.
- Leaks on a criterion's own tool count too (any-query outputs never repeat any expected_evidence).
- Commit each finished, checked piece as you go (conventional commits); never stage files a
  running agent owns.
- Small steps, one agent at a time unless their files are disjoint; no workflows without asking.

## Where the round stands (25 Oct 2026)

| Batch | Conditions | State |
|---|---|---|
| 1 | ALS, BACT-MEN, ISCH-STR, HEP-ENC | done |
| 2 | GLIO-HG, GBS, ALZ-EARLY, SAH | done |
| 3 | SE, VASC-DEM, NMDAR-ENC, MIG-AURA | done |
| 4 | SYNC-CARD, NPH, FTD, MG | done |
| 5 | FND, MS-RR, FEPI-TEMP, PD | done |

Cross-condition work landed after the batches:
- MockServer (317e46db): EEG routed by `eeg_type`; `interpret_labs` serves only the ordered
  panels (`tools/lab_matching.py`), interpretation prose cut item by item (6938668c); MRI orders
  default to no contrast.
- Lab criteria order the panels their evidence cites (476dda4e, 6938668c, SE in 0f200830);
  decisions in `plans/LABS-EVIDENCE-decisions.md` and `plans/SE-routing-decisions.md`.
- SE stores a case-specific routine EEG; guard: every case storing a continuous EEG stores one.
- Batch-5 vocabulary (c02f3050) and wiring, matcher fixes, `test_no_review_process_text`
  (f6a33e45).
- Every condition is in `DISCRIMINATOR_CONDITIONS`.

Final checks at 6938668c: pytest 4723 passed, 0 failed (`--ignore=agent-platform/tests/test_grpo_rollout.py`,
which needs torch); `bin/perfect_agent.py --all` 600/600; `apply_diagnosis_synonyms.py --check` 0.

## Open items (details in CENTRAL_PENDING.md)
- Scorer v2 (677c7492, 7d9bbe3e): diagnosis on the asserted label only, denied clauses dropped,
  per-case `rejected` labels (6,614) and `required_components` (8 mixed cases), ICD code a weight-0
  component. Physician doubts in `plans/SCORER-V2-group{1..4}-decisions.md` (e.g. whether SE cases
  headed by the cause must name it, MG antibody subtype not policed by tokens).
- MockServer/library: library normals can contradict a case that does not store the variant
  (CT perfusion, amyloid PET, batch-4 terms); about 260 cases store a contrast MRI as their only
  study, so a non-contrast order gets post-gadolinium findings; a lab order returns the whole
  stored panel of an added assay.
- Weight and height (b5a46c7c and the consistency pass): every case records height, weight and
  BMI, consistent with its text (guard `test_height_weight_and_bmi_agree`); doubts in
  `plans/BODY-SIZE-{A,B}-decisions.md`. Deployed to the VPS on 25 Oct 2026.
- Prices of the new terms were recalled, some estimated: verify against the 2024 MPFS / CLFS.
- For the physicians: the scoring changes in `CENTRAL_PENDING.md` "For the physicians" and in
  each `plans/<COND>-decisions.md`; never physician-reviewed and changed by the round: VASC-DEM,
  NMDAR-ENC, MIG-AURA, SYNC-CARD, NPH, FTD, MG, FND, MS-RR, FEPI-TEMP, PD.
- Optional: patient-surname repetition across conditions (Reyes in 8 cases, Tanaka in 2); SE-P02
  off the global F44.5 synonym entry.
- The review VPS serves this branch (deployed 25 Oct 2026); redeploy with `deployment/hostinger/deploy.sh` only on Andrea's request.
