# Hospital Rules

Hospital rules are clinical protocols per institution: mandatory investigation steps, timing constraints and contraindicated actions for each clinical scenario.

They are served by the run API (`api/routes/hospitals.py`: `GET /api/v1/hospitals`, `GET/POST/PUT/DELETE /api/v1/hospitals/{id}/rules`) for the dashboard. They are **not used by the harness**: they are not a tool, they are not injected into any harness prompt, and the policy reward does not read them. The policy each case is scored against lives in the case itself (`ground_truth.action_criteria`).

## Available hospital rule sets

| ID | Institution | Guidelines | Key characteristics |
|---|---|---|---|
| `us_mayo` | Mayo Clinic, USA | AAN/AHA/IDSA | Aggressive workup, liability-driven documentation, DMV reporting, tPA 0.9 mg/kg |
| `uk_nhs` | NHS England | NICE | Cost-effective, DVLA notification mandatory, specialist review before ASM, no A&E EEG |
| `de_charite` | Charité Berlin, Germany | DGN/DSG | 24h EEG emphasis, certified Stroke Unit mandatory, CSF biomarkers for dementia, 3T MRI preferred |
| `jp_todai` | University of Tokyo Hospital | JSN/JES/JSS | tPA 0.6 mg/kg (J-MARS), HLA-A*31:01 screening, 2-year driving ban, yokukansan before antipsychotics |
| `br_hcfmusp` | HC-FMUSP São Paulo, Brazil | ABN/SBAVC | SUS resource awareness, longer imaging wait times, VDRL/HIV mandatory, SINAN notification |

## Selecting a hospital

Through the run API:

```bash
curl http://127.0.0.1:8888/api/v1/hospitals
curl http://127.0.0.1:8888/api/v1/hospitals/uk_nhs/rules
```

### Programmatic

```python
from neuroagent.rules.rules_engine import RulesEngine, AVAILABLE_HOSPITALS

# List available hospitals
print(AVAILABLE_HOSPITALS)

# Load specific hospital rules
engine = RulesEngine("config/hospital_rules", hospital="de_charite")
print(engine.get_context())  # the rules rendered as Markdown
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

They do not. `RulesEngine.get_context()` can render a hospital's pathways as Markdown, and `rules/pathway_checker.py` (`PathwayChecker`) can check a list of tool calls against them, but neither is called by the harness, the benchmark runner or the reward.

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
