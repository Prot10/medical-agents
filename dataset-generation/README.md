# NeuroBench Dataset Generation Pipeline

Tools and scripts for generating, validating, and analyzing NeuroBench clinical cases.

## Overview

NeuroBench cases are generated via two pipelines:

### Pipeline 1: Fully Synthetic (v1)
Cases generated entirely from condition YAML specifications + prompt template.

```
conditions.yaml → build_prompt.py → prompt_template.md → Claude subagent → JSON case → validate_case.py
```

### Pipeline 2: Real-Case-Seeded (v2)
Cases grounded in real published case reports from the [MedCaseReasoning](https://github.com/kevinwu23/Stanford-MedCaseReasoning) dataset (CC-BY 4.0). The real case provides the clinical scenario; diagnostic test results are separated from the narrative and placed into structured tool outputs.

```
MedCaseReasoning seed → build_prompt_seeded.py → prompt_template_seeded.md → Claude subagent → JSON case → validate_case.py
```

Key difference: v2 cases separate diagnostic test results from the patient presentation, forcing the AI agent to call tools to discover evidence. Red herrings and disguising information are calibrated by difficulty level.

## Directory Structure

```
data/
└── neurobench/cases/        # final benchmark cases

dataset-generation/
├── config/
│   ├── conditions.yaml              # 20 neurological conditions with clinical specs
│   ├── prompt_template.md           # Template for synthetic case generation
│   └── prompt_template_seeded.md    # Template for real-case-seeded generation
├── criteria_packs/                  # Per-condition clinical criteria packs (one .md per condition)
├── seeds/                           # Real-case seeds (per-condition subdirs, tracked in git)
├── prompts/                         # Assembled prompts (NOT tracked in git — see note below)
├── src/neurobench_gen/
│   ├── build_prompt.py              # Assembles synthetic prompts from YAML + schema
│   ├── build_prompt_seeded.py       # Assembles seeded prompts from seed case + YAML + schema
│   ├── validate_case.py             # Pydantic validation + clinical plausibility checks
│   └── __init__.py
└── scripts/
    ├── generate_batch.sh            # Batch generation via `claude -p` (outside Claude Code)
    ├── generate_one.sh              # Single case debug script
    ├── filter_medcasereasoning.py   # Seed extraction from MedCaseReasoning
    └── dataset_statistics.py        # Dataset statistics (conditions, demographics, modalities)
```

> **Note on `prompts/`:** the assembled prompt files are no longer tracked in git.
> They are regenerated deterministically by `build_prompt.py` / `build_prompt_seeded.py`
> from `config/conditions.yaml` + `seeds/`, so there is nothing to version.

## Usage

### Generate a v1 (synthetic) prompt
```bash
uv run python -m neurobench_gen.build_prompt focal_epilepsy_temporal straightforward FEPI-TEMP-S01
```

### Generate a v2 (seeded) prompt
```bash
uv run python -m neurobench_gen.build_prompt_seeded /path/to/seed.json ischemic_stroke moderate ISCH-STR-RM01
```

### Validate a case
```bash
uv run --project dataset-generation python -m neurobench_gen.validate_case data/neurobench/cases/ISCH-STR-S01.json
```

### Run dataset statistics
```bash
uv run --project dataset-generation python dataset-generation/scripts/dataset_statistics.py
```

## Conditions

20 conditions, defined in `config/conditions.yaml` (one criteria pack per condition in `criteria_packs/`):

| Abbreviation | Condition | ICD Code |
|-------------|-----------|----------|
| `ISCH-STR` | Acute ischemic stroke | I63.9 |
| `FEPI-TEMP` | Focal epilepsy (temporal) | G40.209 |
| `MS-RR` | Multiple sclerosis (relapsing-remitting) | G35.A |
| `ALZ-EARLY` | Alzheimer's disease | G30.9 |
| `PD` | Parkinson's disease | G20.A1 |
| `GLIO-HG` | High-grade glioma (glioblastoma) | C71.9 |
| `BACT-MEN` | Bacterial meningitis | G00.9 |
| `NMDAR-ENC` | Anti-NMDAR encephalitis | G04.81 |
| `FND` | Functional neurological disorder | F44.4 |
| `SYNC-CARD` | Cardiac syncope | R55 |
| `GBS` | Guillain-Barré syndrome | G61.0 |
| `MG` | Myasthenia gravis | G70.0 |
| `SAH` | Subarachnoid hemorrhage | I60.9 |
| `MIG-AURA` | Migraine with aura | G43.1 |
| `FTD` | Frontotemporal dementia | G31.09 |
| `SE` | Status epilepticus | G41.9 |
| `VASC-DEM` | Vascular dementia (major vascular cognitive disorder) | F01.50 |
| `NPH` | Normal pressure hydrocephalus | G91.2 |
| `HEP-ENC` | Hepatic encephalopathy | K72.9 |
| `ALS` | Amyotrophic lateral sclerosis | G12.21 |

## Case ID Convention

- Synthetic cases: `{ABBREV}-{S|M|P}{NUMBER}` — e.g., `ISCH-STR-S01`, `MS-RR-P03`
- Real-seeded cases: `{ABBREV}-R{S|M|P}{NUMBER}` — e.g., `ISCH-STR-RS01`, `MS-RR-RP03` (R = real-seeded)
- Difficulty: S = straightforward, M = moderate, P = diagnostic puzzle

## Dataset Versions

- **v1** — fully synthetic (Pipeline 1), enhanced tool outputs. 10 conditions × 10 cases (4S + 3M + 3P).
- **v2** — real-case-seeded (Pipeline 2), enhanced tool outputs. Same 10 conditions and per-condition distribution.
- **v3** — v1 + v2 combined with their original IDs; tool outputs stripped to "realistic" mode (interpretive fields removed to match real clinical reports).
- **v4** — migrated from v3 to the 12-tool schema + cost tracking (`order_advanced_imaging`, `order_specialized_test`, etc.; see `docs/benchmark/tool-contract.md`).
- **v5** — **current default**: 600 cases across 20 conditions (30 per condition, mixed synthetic + real-seeded), in `data/neurobench/cases/`. Generated via per-condition criteria packs (`criteria_packs/`) + real-case seeds (`seeds/`). Split into 500 train / 100 test (`data/neurobench/splits/`; the test set includes 2 held-out conditions).
  - **Composition change, August 2026 (clinical tool review).** `peripheral_neuropathy` was
    retired — both reviewers judged it too broad a category to score — and **vascular dementia**
    (`VASC-DEM`, 30 synthetic cases) took its place, completing the four major dementias so the
    differential among them becomes scoreable. The split was rebuilt with
    `make_train_test_split --preserve <previous manifest>`, which keeps every surviving case on
    the side it was already on: only the 30 new cases were placed (28 train, 2 test), so
    published numbers stay comparable and existing gold trajectories stay valid. The 28 new
    train cases have no gold trajectory yet and are listed in
    `tests/test_sft_inference_parity.py::AWAITING_DISTILLATION` until the corpus is regenerated.

## External Data Sources

See `docs/archive/dataset-generation/external_case_sources.md` (historical) for the research on 22+ medical case datasets evaluated for NeuroBench expansion, including licensing, access methods, and mapping potential.
