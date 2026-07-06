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

### Pipeline 3: Realistic Tool Outputs (v3)

v3 is NOT a new generation pipeline — it's a post-processing step that strips interpretive fields from v1 and v2 tool outputs to create realistic clinical reports. The v3 dataset combines all 200 cases (100 v1 + 100 v2) with stripped outputs.

```
v1/cases/ + v2/cases/ → create_v3_dataset.py → v3/cases/ (200 cases with realistic tool outputs)
```

**Why v3 exists**: An audit revealed that v1/v2 tool outputs contain interpretive fields that "give away the answer" — MRI impressions naming diseases, lab values explaining their diagnostic significance, EEG reports stating diagnoses. This inflates agent performance by testing reading comprehension instead of clinical reasoning. v3 strips these fields to match what real diagnostic reports provide.

**Stripping script**: `agent-platform/scripts/create_v3_dataset.py`

**Fields stripped or rewritten**:
- `LabValue.clinical_significance` → `null`
- `MRIReport.differential_by_imaging` → `[]`
- `MRI/EEG confidence` → `0.0`
- `MRI/EEG recommended_actions` → `["Clinical correlation recommended."]`
- `MRI/EEG impression` → descriptive findings only (disease names removed)
- `ECGReport.clinical_correlation` → `""`
- `CSFResults.interpretation` → terse numerical summary

## Directory Structure

```
data/
├── neurobench_v1/cases/        # 100 synthetic cases (enhanced tool outputs)
├── neurobench_v2/cases/        # 100 real-seeded cases (enhanced tool outputs)
└── neurobench_v3/cases/        # 200 combined cases (realistic tool outputs)

dataset-generation/
├── config/
│   ├── conditions.yaml              # 10 neurological conditions with clinical specs
│   ├── prompt_template.md           # Template for synthetic case generation (v1)
│   └── prompt_template_seeded.md    # Template for real-case-seeded generation (v2)
├── src/neurobench_gen/
│   ├── build_prompt.py              # Assembles v1 prompts from YAML + schema
│   ├── build_prompt_seeded.py       # Assembles v2 prompts from seed case + YAML + schema
│   ├── validate_case.py             # Pydantic validation + clinical plausibility checks
│   └── __init__.py
├── scripts/
│   ├── generate_batch.sh            # Batch generation via `claude -p` (outside Claude Code)
│   ├── generate_one.sh              # Single case debug script
│   └── dataset_statistics.py        # Dataset statistics (conditions, demographics, modalities)
└── docs/
    └── external_case_sources.md     # Research on 22+ external medical case datasets
```

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
uv run --project dataset-generation python -m neurobench_gen.validate_case data/neurobench_v1/cases/ISCH-STR-S01.json
```

### Run dataset statistics
```bash
uv run --project dataset-generation python dataset-generation/scripts/dataset_statistics.py
```

## Conditions

| Abbreviation | Condition | ICD Code |
|-------------|-----------|----------|
| `ISCH-STR` | Acute ischemic stroke | I63.9 |
| `FEPI-TEMP` | Focal epilepsy (temporal) | G40.209 |
| `MS-RR` | Multiple sclerosis (relapsing-remitting) | G35.A |
| `ALZ-EARLY` | Alzheimer's disease | G30.9 |
| `PD` | Parkinson's disease | G20 |
| `GLIO-HG` | High-grade glioma (glioblastoma) | C71.9 |
| `BACT-MEN` | Bacterial meningitis | G00.9 |
| `NMDAR-ENC` | Anti-NMDAR encephalitis | G04.81 |
| `FND` | Functional neurological disorder | F44.4 |
| `SYNC-CARD` | Cardiac syncope | R55 |

## Case ID Convention

- **v1**: `{ABBREV}-{S|M|P}{NUMBER}` — e.g., `ISCH-STR-S01`, `MS-RR-P03`
- **v2**: `{ABBREV}-R{S|M|P}{NUMBER}` — e.g., `ISCH-STR-RS01`, `MS-RR-RP03` (R = real-seeded)
- **v3**: Contains both v1 and v2 cases with their original IDs, stripped tool outputs
- Difficulty: S = straightforward, M = moderate, P = diagnostic puzzle
- Distribution per condition: 4S + 3M + 3P = 10 cases

## External Data Sources

See `docs/external_case_sources.md` for comprehensive research on 22+ medical case datasets evaluated for NeuroBench expansion, including licensing, access methods, and mapping potential.
