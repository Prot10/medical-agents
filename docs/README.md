# NeuroAgent documentation

Start at the repo [`README.md`](../README.md) for setup and the one-minute tour.
[`CLAUDE.md`](../CLAUDE.md) is the instruction file for coding agents.

Every page below is **current**. Anything historical lives in [`archive/`](archive/) and is
labelled as such — do not follow its commands.

## Core

| Page | What it answers |
| --- | --- |
| [`architecture.md`](architecture.md) | How the whole repo fits together: ReAct loop, tools, mock server, evaluation, web apps |
| [`benchmark/tool-contract.md`](benchmark/tool-contract.md) | **What a tool is, what a case may say about it, and how that is enforced.** Read before touching a case or a tool |
| [`benchmark/diagnosis-scoring.md`](benchmark/diagnosis-scoring.md) | What `diagnostic_accuracy_top1`/`top3` actually measure, and why old figures do not compare |
| [`training/distillation.md`](training/distillation.md) | Gold trajectory generation and SFT of the small student models |
| [`training/sft-recipe-hardware-and-evaluation.md`](training/sft-recipe-hardware-and-evaluation.md) | The SFT recipe, bf16-vs-QLoRA + sequence-length/softmax memory, fla, EOS/RAM staging, and the literature-aligned eval — with measured numbers |

## Where the authoritative definition of each thing lives

Documentation drifts; code does not. When a doc and the code disagree, the code wins — and
these are the files that define reality:

| Thing | Defined in |
| --- | --- |
| The 12 tools and their parameters | `agent-platform/src/neuroagent/tools/tool_registry.py` |
| The closed vocabulary (modalities, test types, genetic panels) | `agent-platform/config/tools/costs.yaml` → `tools/vocabulary.py` |
| What a valid case looks like | `agent-platform/scripts/validation/validate_cases.py` |
| The case schema | `packages/neuroagent-schemas/` |
| Evaluation metrics | `agent-platform/src/neuroagent/evaluation/metrics.py` |
| Hospital protocols | `agent-platform/config/hospital_rules/{hospital}/*.yaml` |

## Authoring benchmark cases

These are living references. Read them before writing or reviewing a case.

- `dataset-generation/TOOL_PARAMETER_VOCABULARY.md` — the closed vocabulary
- `dataset-generation/TOOL_REPORT_STYLE_GUIDE.md` — how a realistic tool report reads
- `dataset-generation/GOLD_TRAJECTORY_AUTHORING_GUIDE.md` — how a gold trajectory reads
- `dataset-generation/criteria_packs/{CONDITION}.md` — per-condition diagnostic criteria,
  standard workup, useless/harmful tools, red herrings

## Platform reference

Colocated with the code they describe, under `agent-platform/docs/`:

[`architecture.md`](../agent-platform/docs/architecture.md) ·
[`quickstart.md`](../agent-platform/docs/quickstart.md) ·
[`tools.md`](../agent-platform/docs/tools.md) ·
[`models.md`](../agent-platform/docs/models.md) ·
[`hospital-rules.md`](../agent-platform/docs/hospital-rules.md) ·
[`web-api.md`](../agent-platform/docs/web-api.md) ·
[`patient-data.md`](../agent-platform/docs/patient-data.md)

## Research

[`research/literature-review.md`](research/literature-review.md) ·
[`research/literature-review-extended.md`](research/literature-review-extended.md) ·
[`research/bibliography.md`](research/bibliography.md) ·
[`research/references.bib`](research/references.bib) ·
[`research/reasoning-frameworks.md`](research/reasoning-frameworks.md) ·
[`research/reasoning-frameworks-references.bib`](research/reasoning-frameworks-references.bib) ·
[`research/proposal-localization-first-reasoning.md`](research/proposal-localization-first-reasoning.md)

## Archive

[`archive/`](archive/) — completed sweeps, per-condition audits, and superseded plans
(e.g. the original fine-tuning and improvement plans). Records of why cases changed.
Several reference scripts that were deleted; they are kept for provenance, not use.
