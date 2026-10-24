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

Six tools stand in for many studies each, selected by one discriminating parameter. Every
value is a priced row in `costs.yaml`, and `validate_cases.py` checks each parameter against
**its own** vocabulary — it previously checked four of the six against the specialized-test
list, which reported legal values as illegal:

| Tool | Parameter | Values |
| --- | --- | --- |
| `order_advanced_imaging` | `modality` | 21 (`amyloid_PET`, `tau_PET`, `FDG_PET`, `perfusion_SPECT`, `amino_acid_PET`, `cardiac_FDG_PET`, `DaTscan`, `MIBG_scan`, `perfusion_MRI`, `CT_perfusion`, `cardiac_MRI`, `coronary_CTA`, `coronary_angiography`, `cerebral_angiography`, `MR_spectroscopy`, `MR_angiography`, `MR_venography`, `carotid_duplex`, `transcranial_doppler`, `functional_MRI`, `DTI_tractography`) |
| `order_specialized_test` | `test_type` | 21, plus `genetic_panel:<panel>` for 17 panels |
| `order_body_imaging` | `study` | 16 (`<region>_<modality>` over pelvis/abdomen, testis, chest, chest-abdomen-pelvis, mediastinum, spine, peripheral nerve, leg veins, temporal arteries) |
| `order_microbiology` | `specimen` | 9 |
| `obtain_tissue_diagnosis` | `procedure` | 5 (`resection`, `stereotactic_biopsy`, `open_biopsy`, `lymph_node_biopsy`, `temporal_artery_biopsy`), plus 21 molecular assays |
| `perform_clinical_assessment` | `assessment_type` | 5 |

`order_ct_scan` images the **head and neck only** and has no region parameter, so its
discriminators (`contrast`, `angiography`) cannot distinguish a head-and-neck CTA from a
thoracic one. Thoracic, abdominal and spinal CT belongs to `order_body_imaging`.

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

### Fallback tiers

A legal order is answered from the first tier that has it: the case's pathway outputs (initial
and follow-up), the case's own off-pathway fallback (`fallback_tool_outputs`, authored per case),
and last the benchmark-level library `agent-platform/config/tools/fallback_library.yaml`: one
normal, non-contributory report per tool and parameter value, the same in every case, resolved
by the tool's discriminating parameter and assembled per requested analyte, CSF test or molecular
assay (`tools/fallback_library.py`). The library exists so that an off-pathway order never reveals
that it was off-pathway (the MockServer used to answer "no data available, consider whether this
test is appropriate" whenever a case lacked a fallback, in 104 of 105 tool × value combinations for
some cases). Library answers carry `from_fallback` and `library` on the observation. The library is
`status: draft` until physicians have reviewed it; `tests/test_fallback_library.py` proves every
legal order is answered in every case.

### Which stored report answers an order

The MockServer (`tools/mock_server.py`, with `tools/followup_matcher.py`) never answers one study
with another study's report. Where a stored report names its study with a vocabulary term (the
discriminator field: `specimen`, `modality`, `echo_type`, `test_type`, `procedure`,
`assessment_type`, `monitor_type`; region and modality for `order_body_imaging`), it answers only
an order for that study. This holds for initial outputs, follow-ups and, since the October 2026
review, the case's own `fallback_tool_outputs`: a case fallback written as an `amino_acid_PET`
report is not served for an `FDG_PET` order, which gets the library normal. A report that names
its study in prose, or not at all, is not adjudicated and answers any variant, so case authors
should write the term.

- Follow-ups that do not describe the study ordered are dropped *before* the trigger matcher
  chooses among siblings (SE-M05: the MRI follow-up won a tie against the ultrasound one and was
  then refused, leaving the ultrasound order to the library).
- The tool's own enum terms (`continuous_icu`, `lumbar_puncture`, `pelvis_abdomen_MRI`) route as
  study identities. A trigger token belonging to a term the call does not name never counts, so
  free text recalling another study of the same tool does not route to it; a term the call
  implies through the schema default counts only when the trigger names it whole; a term named
  explicitly counts unless the initial output already is that study. EEG reports carry no
  `eeg_type`, so for EEG a follow-up trigger must not repeat the index study's term
  (`request_continuous_eeg_monitoring` when the index recording is `continuous_icu`).
- `order_cardiac_monitoring` routes by tier: hours to a week (telemetry, Holter), weeks (event
  monitors), months (loop recorder). A stored recording answers an order of its own tier or a
  longer one, never a shorter one: a Holter order is not answered by a 30-day monitor or a loop
  recorder, whose paroxysmal AF the short recording might miss. The tier is read from
  `duration_hours`, else from `monitor_type`. `device_interrogation` answers, and is answered by,
  only its own type.

A library normal answers a study the case does not store, and for an alternative study on the
case's own pathway it can contradict the case (a normal FDG-PET where the case stores an abnormal
amyloid PET). A criterion alternative should therefore be a study the case stores; the monitoring
tiers above are the one place where the MockServer bridges the gap itself.

### Recorded cases: "not available"

A case with `provenance: record` (a real admission, e.g. MIMIC-IV) holds the results of what
the clinicians ordered and nothing else. It may not carry `fallback_tool_outputs` (the schema
refuses it), and the library tier is skipped: an order with no recorded result fails with
`Not available: <tool> (<parameter>=<value>) was not performed during this recorded encounter`,
flagged `unavailable` on the observation. A normal library report would invent the patient's
data. The price is that the agent learns the study was not done, which a synthetic case hides on
purpose; that is a property of real records, and analyses of recorded cases should say so. The
order is still placed and billed. `search_medical_literature` and `check_drug_interactions` read
no patient data and are answered by the library as in any case.

### Vocabulary packs

`costs.yaml` has a `packs:` block below `tools:`. A pack adds rows to the vocabularies above and
may not re-price a term under any spelling (`vocabulary.merge_packs` raises). The case's
`domain` picks the packs its catalogue advertises (`vocabulary.DOMAIN_PACKS`): a `neurology`
case (every NeuroBench case) sees `tools:` alone, so its catalogue is unchanged by any pack; a
`general_medicine` case also sees the `general_medicine` pack (abdominal and limb X-ray,
endoscopy, pleural, synovial and bronchoalveolar microbiology, percutaneous and endoscopic biopsy,
lipase, ...). A tool declares which schema properties are vocabularies (`BaseTool.vocabulary`)
and what to tell the agent about each pack's terms (`BaseTool.pack_notes`). The cost registry
prices every pack. The review app's mirror covers the NeuroBench catalogue only. The pack's
rates are provisional (see the comment in `costs.yaml`): verify them before a cost result on
general-medicine cases is reported. `tests/test_general_medicine_harness.py` pins all of this.

### Execution-time validation

The catalogue the agent sees is the contract. `BaseTool.execute` validates every call against
the tool's advertised JSON schema before the MockServer or the cost registry sees it: a value
outside a closed enum, a missing required field or a wrong type is answered with a failed
observation naming the problem (`order_body_imaging: study='carotid_duplex' is not in the tool's
vocabulary`), flagged `rejected`, costs nothing (the order was never placed), and is never served a
substitute result. A legal order the case has no output for is a placed order: it fails with the
MockServer's message and is billed. Assay lists (lab panels,
CSF special tests, molecular assays) accept any spelling that normalises to an advertised member,
because the score and the bill already read them that way. Genetic panels are ordinary enum
members (`genetic_panel:<panel>`, one per priced panel). The cost registry therefore has no
fallback rates: an unpriced value that reaches it is a configuration error.

### `analyze_csf` is a trap worth knowing

`costs.yaml` prices the LP procedure together with cell count, protein and glucose inside
`analyze_csf.base`, and bills each entry of `special_tests` separately. Put the always-done
panel in the `basic` annotation and only billable assays in `special_tests`. Merging them
charges the basics a second time.

`source` says where the fluid was drawn: `lumbar_puncture` (the default), `shunt_tap` or
`external_ventricular_drain`. It is an enum from the `analyze_csf.sources` block, priced at 0
like the MRI protocols, so the bill is the same `base` for each. A criterion names it only when
the sample is not a lumbar puncture: a criterion that requires `source: lumbar_puncture` would
fail an agent that leaves the default implicit.

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
