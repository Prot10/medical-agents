# API Reference

The NeuroAgent Web API is served by FastAPI at `http://localhost:8888`. All endpoints are prefixed with `/api/v1`.

## Datasets

### `GET /api/v1/datasets`

Lists available datasets with their case counts and which one is active.

**Response**:

```json
[
  {
    "version": "neurobench",
    "name": "NeuroBench",
    "description": "Tool-augmented neurology benchmark across 20 conditions.",
    "case_count": 600,
    "active": true
  }
]
```

### `POST /api/v1/datasets/{version}/activate`

Switches the active dataset (swaps the in-memory case index/objects). Legacy aliases are normalized (`v5` → `neurobench`).

**Response**: `{ "status": "ok", "version": "neurobench", "case_count": 600 }`

## Cases

### `GET /api/v1/cases`

Returns a lightweight index of all 600 NeuroBench cases (from the active dataset).

**Response**: `CaseIndexEntry[]`

```json
[
  {
    "case_id": "ISCH-STR-S01",
    "condition": "ischemic_stroke",
    "difficulty": "straightforward",
    "encounter_type": "emergency",
    "age": 72,
    "sex": "male",
    "chief_complaint": "Sudden onset right-sided weakness..."
  }
]
```

### `GET /api/v1/cases/{case_id}`

Returns the full case data including patient profile, tool outputs, and ground truth.

**Response**: Full `NeuroBenchCase` JSON (see `neuroagent_schemas.case.NeuroBenchCase`)

Key sections:
- `patient` — demographics, vitals, clinical history, neurological exam, HPI
- `initial_tool_outputs` — pre-generated results for EEG, MRI, ECG, labs, CSF
- `followup_outputs` — conditional outputs triggered by specific agent actions
- `ground_truth` — primary diagnosis, ICD code, differentials, optimal actions, critical/contraindicated actions

## Hospitals

### `GET /api/v1/hospitals`

Returns all 5 available hospital rule sets with pathway summaries.

**Response**: `Hospital[]`

```json
[
  {
    "id": "us_mayo",
    "name": "Mayo Clinic, USA (AAN guidelines)",
    "pathways": [
      { "name": "Acute Stroke Code", "description": "...", "triggers": ["stroke", "ischemic_stroke"] }
    ]
  }
]
```

Available hospitals: `us_mayo`, `uk_nhs`, `de_charite`, `jp_todai`, `br_hcfmusp`

### `GET /api/v1/hospitals/{hospital_id}/rules`

Returns full pathway details including steps (`action`, `timing`, `mandatory`, `condition`, `details`) and contraindicated actions.

### `POST /api/v1/hospitals/{hospital_id}/rules`

Creates a new pathway. The pathway name is slugified into a new YAML file in the hospital's rules directory. Returns `201` with the created pathway, or `409` if a file with that slug already exists.

**Request body** (`PathwayUpdate`, also used by PUT):

```json
{
  "name": "Acute Stroke Code",
  "description": "...",
  "triggers": ["stroke"],
  "steps": [{ "action": "order_ct_scan", "timing": "immediate", "mandatory": true, "condition": null, "details": {} }],
  "contraindicated": ["lumbar_puncture_before_imaging"]
}
```

### `PUT /api/v1/hospitals/{hospital_id}/rules/{pathway_index}`

Updates an existing pathway. `pathway_index` is the index into the hospital's YAML files sorted by filename (the order returned by `GET .../rules`). Returns `404` if out of range.

### `DELETE /api/v1/hospitals/{hospital_id}/rules/{pathway_index}`

Deletes the pathway's YAML file. Returns `{ "status": "ok" }`.

## Models

### `GET /api/v1/models`

Returns the 10 registered models (see `neuroagent/model_registry.py`) with their current status (probes the vLLM and Ollama servers). Ollama models not in the static registry are appended dynamically.

**Response**: `ModelInfo[]`

```json
[
  {
    "key": "qwen3.5-9b",
    "name": "Qwen3.5-9B",
    "hf_model_id": "Qwen/Qwen3.5-9B",
    "description": "Fast Qwen3.5 with thinking mode. Native tool calling.",
    "size_gb": 18.0,
    "expected_load_seconds": 90,
    "supports_tools": true,
    "status": "ready"
  }
]
```

Status values: `ready` (currently loaded), `loading` (load in progress), `offline` (not loaded)

| Key | HF Model ID | Notes |
|-----|-------------|-------|
| `qwen3.5-4b` | `Qwen/Qwen3.5-4B` | Smallest Qwen3.5. |
| `qwen3.5-9b` | `Qwen/Qwen3.5-9B` | Default. Thinking mode. |
| `qwen3.5-27b-awq` | `QuantTrio/Qwen3.5-27B-AWQ` | Best Qwen quality. AWQ Marlin. |
| `medgemma-4b` | `google/medgemma-1.5-4b-it` | Medical specialist, fast. |
| `medgemma-27b` | `ig1/medgemma-27b-text-it-FP8-Dynamic` | Medical specialist, best quality. |
| `nemotron-nano-9b-v2` | `nvidia/NVIDIA-Nemotron-Nano-9B-v2` | NVIDIA Nemotron Nano. |
| `nemotron-3-nano-4b` | `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16` | Nemotron-3, smallest. |
| `gemma-4-e2b` | `google/gemma-4-E2B-it` | Gemma 4, 2B effective. |
| `gemma-4-e4b` | `google/gemma-4-E4B-it` | Gemma 4, 4B effective. |
| `gemma-4-12b` | `google/gemma-4-12B-it` | Gemma 4, 12B dense. |

### `POST /api/v1/models/{model_key}/load`

Loads a model into vLLM (via `scripts/runtime/serve_model.sh`), killing any currently loaded model first. Streams progress via SSE. Only one model fits on the GPU at a time.

**Response**: `text/event-stream` — each event has a `phase` plus progress fields:

```
data: {"phase": "unloading", "message": "Stopping qwen3.5-9b...", "progress": 0}

data: {"phase": "starting", "model": "medgemma-4b", "model_name": "MedGemma 1.5 4B", "size_gb": 8.0, "expected_seconds": 60, "message": "Starting vLLM...", "progress": 0}

data: {"phase": "weights", "message": "Loading model weights...", "elapsed": 24, "expected_seconds": 60, "progress": 36, "log": "..."}

data: {"phase": "ready", "model": "medgemma-4b", "message": "MedGemma 1.5 4B is ready", "elapsed": 57, "progress": 100}
```

Phases: `unloading` → `starting` → `loading` / `weights` / `cuda_graphs` → `ready`, or `error` (vLLM crash or 600s timeout, with `message` and optional `detail`).

### `POST /api/v1/models/unload`

Stops any running vLLM model server (kills the process group).

**Response**: `{ "status": "ok", "message": "Model server stopped" }`

## GitHub Copilot

Optional LLM provider via GitHub's OAuth device flow. When authenticated, Copilot models appear in the model pickers with `copilot:`-prefixed keys.

### `POST /api/v1/copilot/device-code`

Starts the OAuth device flow.

**Response**: `{ "device_code", "user_code", "verification_uri", "expires_in", "interval" }`

### `POST /api/v1/copilot/poll-token`

Polls GitHub for the OAuth token after the user enters the code.

**Request body**: `{ "device_code": "..." }`

**Response**: `{ "status": "pending" | "complete" | "expired" | "denied" | "error", "error"?, "interval"? }`

### `GET /api/v1/copilot/status`

**Response**: `{ "authenticated": boolean, "copilot_access": boolean }`

### `GET /api/v1/copilot/models`

Returns available Copilot models as `ModelInfo[]` (keys like `copilot:claude-sonnet-4.6`, `status: "ready"`, `provider: "copilot"`). Empty list when not authenticated.

### `POST /api/v1/copilot/logout`

Clears stored tokens. **Response**: `{ "status": "ok" }`

## Agent Execution

### `POST /api/v1/agent/run`

Runs the agent on a case and streams results via Server-Sent Events (SSE).

**Request body**:

```json
{
  "case_id": "ISCH-STR-S01",
  "hospital": "us_mayo",
  "model": "qwen3.5-9b",
  "base_url": null,
  "api_key": null
}
```

Model resolution: a registry key routes to vLLM; a `copilot:<id>` key routes to the Copilot API (requires authentication); `base_url` + `api_key` route to a custom OpenAI-compatible endpoint; anything else is assumed to be an Ollama model name (e.g. `qwen3.5:4b`).

**Response**: `text/event-stream`

Each event is a JSON object prefixed with `data: ` and terminated by `\n\n`:

```
data: {"type": "run_started", "case_id": "ISCH-STR-S01", "hospital": "us_mayo", "model": "Qwen/Qwen3.5-9B", "max_turns": 15}

data: {"type": "think_delta", "turn_number": 1, "delta": "Given the"}

data: {"type": "thinking", "turn_number": 1, "content": "Given the acute onset...", "think_content": "...", "token_usage": {"prompt_tokens": 2048, "completion_tokens": 256, "total_tokens": 2304}}

data: {"type": "tool_call", "turn_number": 1, "tool_name": "analyze_brain_mri", "arguments": {"clinical_context": "acute stroke"}}

data: {"type": "tool_result", "turn_number": 2, "tool_name": "analyze_brain_mri", "success": true, "output": {...}, "cost_usd": 412.35}

data: {"type": "reflection", "turn_number": 2}

data: {"type": "assessment", "turn_number": 5, "content": "### Primary Diagnosis\n...", "token_usage": {...}}

data: {"type": "run_complete", "total_tool_calls": 4, "tools_called": [...], "total_tokens": 12400, "elapsed_time_seconds": 34.2, "final_response": "### Primary Diagnosis\n...", "total_cost_usd": 1240.5}
```

### SSE Event Types

| Type | When | Key Fields |
|------|------|------------|
| `run_started` | Immediately | `case_id`, `hospital`, `model`, `max_turns` |
| `think_delta` | Streaming `<think>` reasoning tokens | `turn_number`, `delta` |
| `content_delta` | Streaming visible content tokens | `turn_number`, `delta` |
| `thinking` | Complete reasoning block (for replay/trace) | `turn_number`, `content`, `think_content`, `token_usage` |
| `tool_call` | Before each tool execution | `turn_number`, `tool_name`, `arguments` |
| `tool_result` | After each tool execution | `turn_number`, `tool_name`, `success`, `output`, `cost_usd` |
| `reflection` | Reflection prompt injected | `turn_number` |
| `assessment` | Final agent output (no tool calls) | `turn_number`, `content`, `token_usage` |
| `run_complete` | End of run | `total_tool_calls`, `tools_called`, `total_tokens`, `elapsed_time_seconds`, `final_response`, `total_cost_usd` |
| `error` | On exception | `message` |

Events are streamed in real-time via an async queue — each event appears as the corresponding LLM call or tool execution completes. On `run_complete` the trace is auto-saved to `data/traces/` for replay.

### `POST /api/v1/agent/evaluate`

Evaluates a finished run against ground truth: rule-based metrics plus a streaming LLM judge. The evaluator model is resolved the same way as in `/agent/run` (registry key → vLLM, `copilot:` → Copilot, else Ollama).

**Request body**:

```json
{
  "case_id": "ISCH-STR-S01",
  "model": "qwen3.5-9b",
  "events": [ ...AgentEvent[] from the run... ],
  "final_response": "### Primary Diagnosis\n...",
  "tools_called": ["analyze_brain_mri", "interpret_labs"]
}
```

**Response**: `text/event-stream`

| Type | Fields |
|------|--------|
| `metrics` | Rule-based scores (diagnostic accuracy, action precision/recall, safety, efficiency) |
| `judge_started` | LLM judge call begins |
| `judge_delta` | `delta` — streaming judge output tokens |
| `judge_complete` | Parsed judge scores |
| `eval_error` | `message` |

### `POST /api/v1/agent/replay`

Replays a saved trace as SSE events with small delays to simulate streaming (~80 tokens/sec for deltas).

**Request body**:

```json
{ "trace_id": "ISCH-STR-S01_1710446400000000000" }
```

**Response**: Same `text/event-stream` format as `/agent/run`.

## Traces

### `GET /api/v1/traces`

Lists saved trace files with metadata enriched from the case index.

**Response**: `TraceSummary[]`

```json
[
  {
    "trace_id": "ISCH-STR-S01_1710446400000000000",
    "case_id": "ISCH-STR-S01",
    "hospital": "us_mayo",
    "model": "Qwen/Qwen3.5-9B",
    "model_short": "qwen3.5-9b",
    "condition": "ischemic_stroke",
    "difficulty": "straightforward",
    "total_tool_calls": 4,
    "tools_called": ["analyze_brain_mri", "interpret_labs"],
    "total_tokens": 12400,
    "elapsed_time_seconds": 34.2,
    "total_cost_usd": 1240.5
  }
]
```

### `GET /api/v1/traces/{trace_id}`

Downloads the full trace JSON including all events.

### `DELETE /api/v1/traces/{trace_id}`

Deletes a saved trace file. Returns `204 No Content`.
