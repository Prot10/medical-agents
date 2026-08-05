# The tool contract

Every NeuroBench case describes an ideal workup as a list of tool calls. The agent executes
tool calls. `CostTracker` prices them and `evaluation/metrics.py` scores them. Those four
things only agree if they share one definition of what a tool is and what arguments it takes.

They did not, for a long time. This page is that definition, and how it is enforced.

## The single source of truth

`agent-platform/config/tools/costs.yaml` is the source of truth for the **closed vocabulary**
of the two catchall tools. A term cannot exist without a price:

```
costs.yaml  ──►  tools/vocabulary.py  ──►  tool schemas (enum)
                                      └─►  scripts/validation/validate_cases.py
                                      └─►  dataset-generation/TOOL_PARAMETER_VOCABULARY.md
```

`agent-platform/tests/test_case_tool_contract.py` fails if these ever disagree again.

## The 16 tools

The registry is `agent-platform/src/neuroagent/tools/tool_registry.py`. There are exactly 12.
`consult_medical_specialist` was removed in `64d4091` — a specialist referral is a real
clinical step, but no tool performs it, so it appears in a case as an action with
`tool_name: null`.

The two catchall tools stand in for many studies, selected by one parameter:

| Tool | Parameter | Values |
| --- | --- | --- |
| `order_advanced_imaging` | `modality` | 12 (`amyloid_PET`, `tau_PET`, `FDG_PET`, `DaTscan`, `MIBG_scan`, `perfusion_MRI`, `cardiac_MRI`, `MR_spectroscopy`, `MR_angiography`, `MR_venography`, `carotid_duplex`, `transcranial_doppler`) |
| `order_specialized_test` | `test_type` | 21, plus `genetic_panel:<panel>` for 15 panels |

## What a case may write in `tool_parameters`

`ground_truth.optimal_actions[].tool_parameters` (and the same field on `useless_tools` /
`harmful_tools`) is an **annotation of intent, not a complete tool call**. 87% of steps carry
no `clinical_context`, and that is fine — the field records *which* study the clinician
intends, not a payload to replay.

What it may contain:

1. **Schema parameters** of that tool. Enum-typed ones must carry a legal value.
2. **Descriptive annotations** — clinical intent the tool does not accept as an argument
   (`sequences`, `region`, `indication`, …). The per-tool allowlist is `ANNOTATION_KEYS` in
   `scripts/validation/validate_cases.py`. One canonical spelling each. `CostTracker` ignores
   them.

Anything else is an error.

### `analyze_csf` is a trap worth knowing

`costs.yaml` prices the LP procedure together with cell count, protein and glucose inside
`analyze_csf.base`, and bills each entry of `special_tests` separately. Put the always-done
panel in the `basic` annotation and only billable assays in `special_tests`. Merging them
charges the basics a second time.

## Useless and harmful tools are parameter-scoped

A case may require `order_advanced_imaging{modality: FDG_PET}` and, in the same breath, mark
`{modality: MR_spectroscopy}` wasteful. One tool name, two different studies.

So `useless_tools` / `harmful_tools` match on `(tool_name, tool_parameters)`:

- an entry **with** parameters matches only calls that carry them
- an entry **without** parameters is a wildcard over the whole tool

Matching on the name alone charged a *perfect* agent with a useless call in 103 of 600 cases.

## The invariants, and how they are checked

```bash
# 1. every case satisfies the contract          -> 600/600 clean, 0 issues
uv run python agent-platform/scripts/validation/validate_cases.py

# 2. the ground truth is attainable             -> 0 cases where a perfect agent is imperfect
uv run python agent-platform/scripts/validation/check_perfect_agent.py

# 3. the gate that keeps it that way            -> 1205 tests
uv run pytest agent-platform/tests/test_case_tool_contract.py
```

`check_perfect_agent.py` is the one that matters. For each case it builds the trace of an
agent that does exactly what the ground truth says — every callable optimal action, with the
ground truth's own parameters, nothing else — and asserts it scores `action_recall == 1.0`,
`required_coverage == 1.0`, `useless_calls == 0`, `harmful_calls == 0`.

If that fails, the case is **unreachable**: no model can attain its ceiling, and every score
reported against it is measured against an impossible target. Before the migration this held
for only 355 of 600 cases.

## Repairing cases

`scripts/validation/migrate_cases.py` applies deterministic repairs (key renames, removed
tools, the CSF split) and reports exactly what it changed. Whatever survives needs clinical
judgment. `scripts/validation/check_sweep_guard.py` then verifies no case regressed and that
`primary_diagnosis` / `icd_code` / `condition` never changed.

## History

- `64d4091` removed `consult_medical_specialist` but not its 263 references in the cases.
- `c44993b` deleted the three validators that would have caught the drift.
- The tool schemas exposed 6 of 11 modalities and 9 of 19 test types, so ground-truth values
  that were legal in `costs.yaml` were unorderable by the agent.
- `CostTracker` read `imaging_type` while every case wrote `modality`, so it silently fell
  back to a default rate and mispriced the optimal workup in **293 of 600 cases** (mean
  |Δ| $2,046, max $5,750).

Any evaluation result produced before that migration is not comparable with one produced
after it.
