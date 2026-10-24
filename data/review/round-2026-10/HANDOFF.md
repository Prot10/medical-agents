# Handoff: October 2026 review round (24 Oct 2026)

Branch `fix/review-round-2026-10`, everything committed (35 commits ahead of `master`, not
pushed, no PR). The session that wrote this stopped the batch-4 workflow on Andrea's request so
another account can continue. Read, in this order: this file, `ROUND_POLICY.md`, `PATTERNS.md`,
`CENTRAL_PENDING.md`, `CLOSEOUT_BRIEF.md`. The skill `claude-workflow-fanout` has the lessons on
running long fan-outs (limits, markers, token economy, scratchpad hygiene).

## Standing rules from Andrea (24 Oct 2026)
- Open questions: decide them "nel modo migliore per la qualità del dataset", apply, record the
  reason. Ask Andrea only for information only Andrea has.
- Leaks on a criterion's own tool count too (any-query outputs never repeat any expected_evidence).
- Commit each finished, checked piece as you go (conventional commits); never stage files a
  running agent owns.
- One workflow at a time, 4 conditions per batch; no `effort: 'high'`.

## Where the round stands

| Batch | Conditions | State |
|---|---|---|
| 1 | ALS, BACT-MEN, ISCH-STR, HEP-ENC | done: workflow, close-out, vocabulary wired |
| 2 | GLIO-HG, GBS, ALZ-EARLY, SAH | done |
| 3 | SE, VASC-DEM, NMDAR-ENC, MIG-AURA | done |
| 4 | SYNC-CARD, NPH, FTD, MG | workflow stopped mid-run (checkpoint commit) |
| 5 | FND, MS-RR, FEPI-TEMP, PD | not started |

The 12 done conditions pass every guard (leak, follow-up, banned strings, discriminators) and
600/600 cases pass the perfect-agent check. Discriminator fixes and the new guard
`test_routed_outputs_name_their_study` cover only the 12 done conditions so far
(`DISCRIMINATOR_CONDITIONS` in `agent-platform/tests/test_case_guards.py`).

### Batch 4 at the stop (from the on-disk markers)
- Plans: all four written (`plans/{SYNC-CARD,NPH,FTD,MG}.md`).
- Fixed (log has `## Changes`): SYNC-CARD 29/30 (missing RP05), NPH 27/30 (missing P02, P08,
  S05), FTD 30/30, MG 30/30. No case was left mid-edit.
- Verified (log has `## Verification`): SYNC-CARD 7, NPH 0, FTD 30, MG 18.
- Condition audits (`plans/<COND>-summary.md`): none yet.

## How to resume

1. Check the markers yourself first (a stopped run can differ from this file):
   ```bash
   uv run python data/review/round-2026-10/bin/perfect_agent.py --all
   uv run pytest agent-platform/tests/test_case_guards.py -q
   ```
2. Relaunch batch 4 with the Workflow tool, script `data/review/round-2026-10/bin/round-v2.js`,
   args one object per condition: `{"cond": "SYNC-CARD", "planDone": true, "cases": [...30 ids]}`
   (same for NPH, FTD, MG; all four plans exist, so `planDone: true`). Case ids:
   the files whose id minus its last `-` part equals the condition (so `MG-` does not pick up
   other prefixes). Workers skip cases with `## Changes`,
   verifiers skip cases with `## Verification`, so only the remaining work runs. Check
   `journal.jsonl` for `null` results before trusting a finished stage.
3. When batch 4 finishes: commit cases, logs, plans and summaries (one commit). Then the
   close-out, as for batches 1-3 (recipe in `CENTRAL_PENDING.md`):
   - one agent per condition with `CLOSEOUT_BRIEF.md` (COND replaced): synonyms, criteria pack,
     generator block, guidance claims (FTD and MG claims fail today until this step),
     discriminators plus adding COND to `DISCRIMINATOR_CONDITIONS`, open questions;
   - one vocabulary agent for the batch's CENTRAL terms (pattern: commits a07f7dfa, e19131d6,
     a27e03ad); then wire the new terms into the cases (one agent per condition or one for all).
   - Commit each condition's cases/logs/decisions/pack when its agent reports; commit the shared
     files (`conditions.yaml`, `diagnosis_synonyms.yaml`, guidance builder, YAML and claim test)
     once all four are done. Run the full suite and the perfect agent before each commit.
4. Batch 5 (FND, MS-RR, FEPI-TEMP, PD) the same way, without `planDone`. Batch 4 and batch 5 can
   overlap only as batch-4 close-out alongside the batch-5 workflow (disjoint files).
5. Final step: full suite
   (`uv run pytest agent-platform/tests packages/neuroagent-schemas/tests -q --ignore=agent-platform/tests/test_grpo_rollout.py`),
   `perfect_agent.py --all`, `apply_diagnosis_synonyms.py --check`, then the open items below.

## Open items (details in CENTRAL_PENDING.md)
- Scorer: a diagnosis is accepted on its ICD code alone (C71, G61.0, F01.50, G43.109 credit wrong
  answers); no negation matching ("non-aneurysmal SAH"); no per-case rejected tokens (dementia
  accepts MCI). These are the main remaining validity issues; they need code, not case edits.
- MockServer/library: normal library reports can contradict a case; a first lab order bundling a
  second-tier assay gets the first-line panel without it.
- Schema: no `weight_kg` / `height_cm`.
- Prices of the new terms were recalled, some estimated: verify against the fee schedule.
- For the physicians: the scoring changes listed per condition in `plans/<COND>-decisions.md`;
  VASC-DEM, NMDAR-ENC, MIG-AURA and the batch-4/5 conditions were never physician-reviewed and
  should be scheduled.
- Nothing is pushed and the review VPS still serves the old data: deploy only after the round.
