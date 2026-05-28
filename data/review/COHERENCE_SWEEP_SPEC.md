# Coherence Sweep Spec — v5 gold-trajectory case-body gaps

You are a per-condition clinical expert closing the **coherence gaps** left after
the gold-trajectory regen. Your goal: drive
`agent-platform/scripts/validate_ground_truth_coherence.py` to **0 issues** for
every case of your assigned condition, **without fabricating pathology** and
**without degrading clinical correctness**.

The gap manifest lives at `data/review/coherence_gap_manifest.json`
(`{case_file: {serious: [[tool, kind], ...], soft: [tool, ...]}}`). Read it and
filter to your condition's prefix.

## The three gap types and how to fix each

### 1. SERIOUS — `required` tool, no stored output (kind in manifest)

The gold marks a tool `required`, but no `initial_tool_outputs`/`followup_outputs`
entry exists, so the mock server returns a hard error when the agent obeys the
gold. Two valid fixes — **choose per case by clinical judgment**:

- **`search_medical_literature` / `check_drug_interactions`** (`kind = reclassify_or_author`):
  These are decision-support tools, rarely a true *must-call*. **Default: downgrade
  the `optimal_actions` entry's `category` from `required` to `recommended`.**
  Tell-tale signs of over-classification: empty `rationale`, `check_drug_interactions`
  with `medications: []` / no real drug, generic literature query. **Only keep it
  `required` if the case's diagnosis genuinely hinges on it** (e.g. FTD case ruling
  out lithium toxicity → the drug check is diagnostic). If you keep it required, you
  MUST author the matching output:
  - `initial_tool_outputs.literature_search` = `{ "<query>": LiteratureSearchResult }`
  - `initial_tool_outputs.drug_interactions` = `{ "<drug>": DrugInteractionResult }`
  and fix the action's `tool_parameters` to name the real query/drug.

- **Diagnostic tools** (`order_specialized_test`, `order_cardiac_monitoring`,
  `order_ct_scan`, `analyze_csf`, `analyze_brain_mri`, `order_advanced_imaging`, etc.;
  `kind = author_diagnostic`): if the tool is genuinely required for this diagnosis,
  **author the real, case-consistent output** in `initial_tool_outputs.<field>` (or a
  `followup_outputs` entry). The result must reflect this patient's actual pathology
  and be consistent with the diagnosis, exam, and other tool outputs. If, on review,
  the tool is NOT actually needed for the diagnosis, downgrade it to
  `recommended`/`optional` instead of inventing a finding.

### 2. SOFT — `useless` tool, no fallback

A tool listed in `ground_truth.useless_tools` has no entry in
`fallback_tool_outputs.<field>`, so calling it errors instead of returning a
realistic off-pathway result. **Fix: author a NORMAL / non-contributory result** in
`fallback_tool_outputs.<field>`. The fallback MUST be normal/unremarkable — its whole
purpose is to show the agent that this off-pathway test added nothing. One report per
field covers all useless variants of that tool (the mock server returns the single
field regardless of parameters). Use the existing `fallback_tool_outputs` in any
`ALS-M01.json` … `ALS-P*.json` as a shape reference.

## Field → output-model map (`fallback_tool_outputs` / `initial_tool_outputs`)

```
eeg                 -> EEGReport
mri                 -> MRIReport
ecg                 -> ECGReport
labs                -> LabResults
csf                 -> CSFResults
ct                  -> CTReport
echo                -> EchoReport
cardiac_monitoring  -> CardiacMonitoringReport
advanced_imaging    -> AdvancedImagingReport
specialized_test    -> SpecializedTestReport
literature_search   -> dict[str, LiteratureSearchResult]
drug_interactions   -> dict[str, DrugInteractionResult]
```

Model field shapes (from `packages/neuroagent-schemas/src/neuroagent_schemas/tool_outputs.py` — read it if unsure):

- **CTReport**: `findings:[CTFinding{type,location,size?,density?,description}]`, `contrast_used:bool`, `angiography_findings:dict|null`, `additional_observations:[str]`, `impression:str`, `recommended_actions:[str]`
- **MRIReport**: `findings:[MRIFinding{type,location,size?,signal_characteristics:dict,mass_effect?,borders?}]`, `volumetrics:dict|null`, `additional_observations:[str]`, `impression:str`, `differential_by_imaging:[dict]`, `recommended_actions:[str]`
- **AdvancedImagingReport**: `modality:str`, `tracer_or_protocol:str|null`, `findings:[dict]`, `quantitative_data:dict|null`, `impression:str`, `recommended_actions:[str]`
- **SpecializedTestReport**: `test_type:str`, `findings:[dict]`, `quantitative_data:dict|null`, `impression:str`, `recommended_actions:[str]`
- **CardiacMonitoringReport**: `duration_hours:int`, `monitor_type:str`, `rhythm_summary:str`, `heart_rate_range:dict[str,int]`, `events:[dict]`, `findings:[str]`, `impression:str`, `recommended_actions:[str]`
- **EchoReport**: `chambers:dict`, `valves:dict`, `ejection_fraction:float|null`, `wall_motion:str|null`, `findings:[str]`, `impression:str`, `recommended_actions:[str]`
- **EEGReport**: `classification:"normal"|"abnormal"`, `background:dict`, `findings:[EEGFinding]`, `artifacts:[dict]`, `activating_procedures:dict`, `impression:str`, `limitations:str`, `recommended_actions:[str]`
- **LiteratureSearchResult**: `query:str`, `results:[dict{title,year,key_finding,...}]`, `summary:str`
- **DrugInteractionResult**: `proposed:str`, `interactions:[str]`, `contraindications:[str]`, `warnings:[str]`, `formulary_status:str`, `alternatives:[str]`

## Editing the JSON safely (preserve each file's unicode convention)

Some v5 files store unicode escaped (`—`), others store literal (`—`). To avoid
spurious whole-file diffs, mutate and write back with this helper pattern:

```python
import json
from pathlib import Path
p = Path("data/neurobench_v5/cases/<CASE>.json")
raw = p.read_text()
use_literal = any(ord(c) > 127 for c in raw)   # detect original convention
case = json.loads(raw)
# ... mutate case dict (add fallback_tool_outputs / initial output / change category) ...
p.write_text(json.dumps(case, indent=2, ensure_ascii=not use_literal) + "\n")
```

## Hard constraints

- **Fallbacks are always NORMAL / non-contributory.** Never put pathology in a
  `fallback_tool_outputs` entry — that would leak a false positive into off-pathway space.
- **Do not alter the diagnosis, the patient body, exam, or existing on-pathway tool
  outputs** unless they are internally contradictory (flag in `metadata.case_body_concerns`
  rather than silently rewriting).
- **Author outputs must be clinically consistent** with this case's diagnosis and other findings.
- **Touch only your condition's files.**
- Keep `differential` sorted by likelihood descending (very_high → very_low).

## Self-validation (REQUIRED before you report done)

For every case you touched:

```bash
uv run python agent-platform/scripts/validate_ground_truth_coherence.py --case <CASE>.json   # must print 0 issue(s)
uv run python -c "from pathlib import Path; from neuroagent_schemas import NeuroBenchCase; NeuroBenchCase.model_validate_json(Path('data/neurobench_v5/cases/<CASE>.json').read_text())"
```

Then run the whole-condition sweep and confirm 0:

```bash
uv run python agent-platform/scripts/validate_ground_truth_coherence.py 2>&1 | grep -i "<PREFIX>"
```

Report back: cases touched, how many gaps were fixed by reclassification vs by
authoring an output, and any case you flagged instead of fixing (with reason).
