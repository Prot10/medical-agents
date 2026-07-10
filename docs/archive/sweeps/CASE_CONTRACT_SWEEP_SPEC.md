# Case contract sweep — closing the last validator issues

You are a per-condition clinical expert. Your goal: drive

```
uv run python agent-platform/scripts/validation/validate_cases.py --case <FILE>
```

to **0 issues** for every case assigned to you, **without inventing pathology** and **without
changing any clinical content**.

Your work packet is `data/review/work_packets/{CONDITION}.json`, shaped
`{case_file: [{code, section, index, tool, detail, fix_class}, ...]}`. Cases live in
`data/neurobench/cases/{case_file}`.

## Absolute rules

1. **Only touch the case files listed in your packet.** Nothing else, ever.
2. **Never change clinical content.** `primary_diagnosis`, `icd_code`, `differential`,
   `patient`, every tool output, every `rationale` / `action` / `expected_finding` /
   `key_reasoning_points` stays exactly as written. You are fixing *how a step names the tool
   it intends and with which arguments*, not what the medicine says.
3. **Never invent a value to silence the validator.** If the honest fix needs a vocabulary
   term that does not exist, STOP and report it — do not map it onto a near-miss. A wrong
   `test_type` is worse than an open issue, because it becomes a silent scoring error.
4. Preserve file formatting: 2-space indent, unicode as-is, trailing newline. Read with
   `json.load`, write with `json.dumps(..., indent=2, ensure_ascii=False) + "\n"`.

## Background you need

`tool_parameters` in `optimal_actions` / `useless_tools` / `harmful_tools` is an **annotation
of intent**, not a complete tool call. A missing `clinical_context` is fine. What is not fine
is a key the tool does not have and that is not a documented annotation.

Two key groups exist:

* **Schema parameters** — the tool actually accepts them, and `CostTracker` prices some of
  them. Source of truth: `ToolRegistry`. Enum values must be legal.
* **Descriptive annotations** — allowed extras recording clinical intent the tool does not
  take as an argument. The allowlist is `ANNOTATION_KEYS` in
  `agent-platform/scripts/validation/validate_cases.py`. Read it.

The closed vocabularies for `order_specialized_test.test_type` and
`order_advanced_imaging.modality` come from `agent-platform/config/tools/costs.yaml`, and are
documented in `dataset-generation/TOOL_PARAMETER_VOCABULARY.md`.

## How to fix each issue code

### `PARAM_UNKNOWN_KEY` — `check_drug_interactions.drugs` (the big one)

The schema is `{drug: str (the drug being checked), current_medications: list[str] (what the
patient already takes), patient_conditions: list[str]}`.

`drugs` is a **list**. Read the case — the step's `action`, `rationale`, the sibling
`indication` / `context` keys, and the patient's `clinical_history.medications` — and decide
what it means:

* It names the drug(s) the clinician is **about to start** → the primary one becomes
  `drug` (a string). If there is genuinely more than one proposed drug, keep the principal
  one in `drug` and move the rest into the `screen_for` annotation.
* It names drugs the patient **already takes** → `current_medications` (keep the list).

Cross-check against `patient.clinical_history.medications`: if the drug is already on the
patient's list, it is a current medication, not a proposal. If it is the drug the step is
about to prescribe (e.g. riluzole in ALS, IVIg in GBS), it is `drug`.

### `PARAM_UNKNOWN_KEY` — the small ones

* `analyze_eeg.duration_hours` / `analyze_eeg.monitor_type` — the schema has
  `eeg_type ∈ {routine, ambulatory, video, continuous_icu}` plus the `duration` annotation.
  A 24-hour ICU recording is `eeg_type: "continuous_icu"`; put the hours into `duration`.
* `order_echocardiogram.contrast` — the schema has `echo_type ∈ {TTE, TEE, bubble_study}` and
  a `bubble_study` annotation. Agitated-saline / contrast study looking for a right-to-left
  shunt is `echo_type: "bubble_study"`. If contrast was for endocardial border definition on
  a plain transthoracic study, keep `echo_type: "TTE"` and drop the key.
* `order_ct_scan.protocol` / `order_ct_scan.scan_type` — the schema has `contrast: bool` and
  `angiography: bool`, plus `region` / `indication` annotations. A CT angiogram is
  `angiography: true`; a skull-base protocol is `region: "skull_base"`. If the value names a
  study this tool cannot perform (e.g. CT pulmonary angiography is a chest study, not a
  neuro CT), that is a **vocabulary gap** — report it, do not force it.

### `PARAM_BAD_ENUM` — `analyze_brain_mri.protocol`

Legal: `standard, epilepsy, stroke, tumor, ms, dementia`. The protocol selects the scanning
package; specific sequences belong in the `sequences` annotation.

* `standard_plus_SWI` → `protocol: "standard"`, add `"SWI"` to `sequences`.
* `stroke_posterior_fossa` → `protocol: "stroke"`, add `region: "posterior_fossa"`.
* `stroke + infection` → pick the protocol the case's imaging actually drove, put the other
  indication in `sequences` / the step's existing prose.
* `functional_DTI` → `protocol: "standard"`, add `"DTI"` (and `"fMRI"` if the case says so)
  to `sequences`.

Note `costs.yaml` prices every MRI protocol at 0 extra, so this never changes cost — but
picking the honest package still matters, because the protocol is what the agent must learn
to order.

### `PARAM_BAD_ENUM` — `order_cardiac_monitoring.monitor_type`

Legal now: `holter_24h, holter_48h, event_monitor_14d, event_monitor_30d,
implantable_loop_recorder, telemetry`. Use the sibling `duration_days` to choose:
14 → `event_monitor_14d`, 30 → `event_monitor_30d`, 180/365 → `implantable_loop_recorder`.
A bare `event_monitor` with no duration: read the case's rationale.

### `FOLLOWUP_TOOL_REMOVED`

A `followup_outputs` entry is keyed to `consult_medical_specialist`, a tool deleted from the
registry. No agent can ever trigger it, so the stored consultation report is unreachable.

Decide per case:
* If the consult's content is genuinely load-bearing (it carries the finding that clinches
  the diagnosis), **re-key** the entry onto a tool that can produce it and adjust the output
  object to that tool's report schema. Only do this if it is honest.
* Otherwise **delete the entry** from `followup_outputs`.

Deleting is the expected default: the corresponding `optimal_actions` step has already been
converted to a tool-less clinical action, and its `action` prose still tells the agent to
refer to the specialist.

## When you are done

For each of your case files run:

```
uv run python agent-platform/scripts/validation/validate_cases.py --case <FILE>
```

It must print `1/1 cases clean, 0 issues`. Then re-read your diff and confirm you changed
nothing clinical.

Report, in plain text:
* how many cases you fixed,
* every decision that was not mechanical (especially every `drugs` → `drug` vs
  `current_medications` call), one line each,
* every **vocabulary gap** you refused to force, with the case id and what term is missing.
