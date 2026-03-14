# Hospital Rules

Hospital rules are clinical protocols injected into the agent's system prompt. They define mandatory investigation steps, timing constraints, and contraindicated actions for each clinical scenario.

Rules are **not a tool** — the agent cannot call them. Instead, they are part of the context the agent reasons over, similar to how a real clinician follows their institution's protocols.

## Available hospital rule sets

| ID | Institution | Guidelines | Key characteristics |
|---|---|---|---|
| `us_mayo` | Mayo Clinic, USA | AAN/AHA/IDSA | Aggressive workup, liability-driven documentation, DMV reporting, tPA 0.9 mg/kg |
| `uk_nhs` | NHS England | NICE | Cost-effective, DVLA notification mandatory, specialist review before ASM, no A&E EEG |
| `de_charite` | Charité Berlin, Germany | DGN/DSG | 24h EEG emphasis, certified Stroke Unit mandatory, CSF biomarkers for dementia, 3T MRI preferred |
| `jp_todai` | University of Tokyo Hospital | JSN/JES/JSS | tPA 0.6 mg/kg (J-MARS), HLA-A*31:01 screening, 2-year driving ban, yokukansan before antipsychotics |
| `br_hcfmusp` | HC-FMUSP São Paulo, Brazil | ABN/SBAVC | SUS resource awareness, longer imaging wait times, VDRL/HIV mandatory, SINAN notification |

## Selecting a hospital

### CLI flag

All scripts accept `--hospital`:

```bash
# Use UK NHS protocols
uv run python scripts/run_single_case.py tests/fixtures/sample_case.json \
    --hospital uk_nhs

# Use Japanese protocols
uv run python scripts/run_single_case.py tests/fixtures/sample_case.json \
    --hospital jp_todai

# Compare same case across hospitals
for h in us_mayo uk_nhs de_charite jp_todai br_hcfmusp; do
    echo "=== $h ==="
    uv run python scripts/run_single_case.py tests/fixtures/sample_case.json \
        --hospital "$h"
done
```

### Configuration file

In `config/agent_config.yaml`:

```yaml
rules:
  rules_dir: "config/hospital_rules"
  hospital: "uk_nhs"  # Change this
```

### Programmatic

```python
from neuroagent.rules.rules_engine import RulesEngine, AVAILABLE_HOSPITALS

# List available hospitals
print(AVAILABLE_HOSPITALS)

# Load specific hospital rules
engine = RulesEngine("config/hospital_rules", hospital="de_charite")
print(engine.get_context())  # Markdown for system prompt
```

## Condition pathways

Each hospital defines protocols for these neurological conditions:

| Pathway file | Condition |
|---|---|
| `first_seizure.yaml` | First unprovoked seizure workup |
| `stroke_code.yaml` | Acute ischemic/hemorrhagic stroke |
| `meningitis.yaml` | Meningitis and encephalitis |
| `dementia_workup.yaml` | Dementia evaluation |
| `general.yaml` | General neurology safety rules |

## How rules affect the agent

The rules are injected into the system prompt under a `## Hospital Protocols` section. The agent sees text like:

> You are operating under the clinical protocols of **NHS England (NICE guidelines)**.
> You MUST follow these protocols strictly. The following pathways apply:
> - **First Seizure Pathway (NICE CG137)**: ...
>   - interpret_labs (immediate, MANDATORY)
>   - analyze_eeg (after_specialist_review, MANDATORY)
>   ...
>   - CONTRAINDICATED: Starting ASM in A&E after a single seizure without epilepsy specialist review

Post-hoc, the `PathwayChecker` evaluates whether the agent's tool calls comply with the selected hospital's rules.

## Adding a new hospital

1. Create a directory under `config/hospital_rules/` with a short ID (e.g., `fr_salpetriere/`)
2. Add YAML files for each pathway (copy an existing hospital as template)
3. Register the hospital in `rules_engine.py`:

```python
AVAILABLE_HOSPITALS: dict[str, str] = {
    ...
    "fr_salpetriere": "Pitié-Salpêtrière, Paris, France (HAS guidelines)",
}
```

4. Add a test or run `pytest` to verify it loads correctly

## YAML pathway format

```yaml
name: "Human-readable pathway name"
description: "Brief description with guideline reference"
triggers: ["keyword1", "keyword2"]  # Used for pathway matching
steps:
  - action: "tool_name"        # Must match a registered tool name
    timing: "immediate"         # When to perform
    mandatory: true             # Required vs optional
    condition: "if_condition"   # When this step applies (optional)
    note: "Additional context"  # Free text for the agent (optional)
contraindicated:
  - "Free-text description of what must NOT be done"
```
