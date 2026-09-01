# Clinical tools

The benchmark exposes 16 typed diagnostic actions through `ToolRegistry`. Every action has one
canonical tool name, a JSON parameter schema and a structured result.

## Registry

- `analyze_eeg`
- `analyze_brain_mri`
- `analyze_ecg`
- `interpret_labs`
- `analyze_csf`
- `search_medical_literature`
- `check_drug_interactions`
- `order_ct_scan`
- `order_echocardiogram`
- `order_cardiac_monitoring`
- `order_advanced_imaging`
- `order_specialized_test`
- `order_body_imaging`
- `order_microbiology`
- `obtain_tissue_diagnosis`
- `perform_clinical_assessment`

The registry is built by `ToolRegistry.create_default_registry()`. Unknown tools return a failed
`ToolResult`; they are never routed through aliases.

## Parameters and costs

`agent-platform/config/tools/costs.yaml` is the single source of truth for priced modalities,
panels, studies and assays. `tools/vocabulary.py`, the review schemas and the case validator derive
their closed vocabularies from that file. A vocabulary term without a price is a configuration
error, not a default-cost fallback.

Each policy criterion may provide multiple acceptable call patterns. Matching is parameter-aware,
so ordering the right tool with the wrong modality or assay does not satisfy a criterion.

## Executable patient environment

During benchmark evaluation, tools are backed by the case's observable initial, conditional and
fallback outputs. The environment resolves conditional outputs deterministically from the tool
name and arguments, records cost and returns a typed observation. A failed or low-value call remains
part of the episode and can affect safety, waste and efficiency scores.

The standard policy, direct ablation and ReAct ablation all use the same tool contracts and reward.
Direct profiles receive the complete observable evidence and therefore do not need to call tools.

## Adding or changing a tool

A tool change is incomplete until all of these agree:

1. implementation and parameter schema;
2. the cost/vocabulary registry;
3. shared case schemas;
4. case validator and authoring guide;
5. environment dispatch and episode serialization;
6. policy-reward matching;
7. physician review UI;
8. contract tests.

See `docs/benchmark/tool-contract.md` for the detailed invariants.
