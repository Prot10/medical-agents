# API Reference

The NeuroAgent Web API is served by FastAPI at `http://localhost:8888`. All endpoints are prefixed with `/api/v1`.

## Cases

### `GET /api/v1/cases`

Returns a lightweight index of all 100 NeuroBench cases.

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

Returns all 5 available hospital rule sets.

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

Returns full pathway details including steps, timing, mandatory flags, and contraindicated actions.

## Models

### `GET /api/v1/models`

Returns the 4 available models with their current status (probes the vLLM server).

**Response**: `ModelInfo[]`

```json
[
  {
    "key": "qwen3.5-9b",
    "name": "Qwen3.5-9B",
    "hf_model_id": "Qwen/Qwen3.5-9B",
    "description": "Fast, good tool calling. Thinking mode enabled.",
    "status": "ready"
  }
]
```

Status values: `ready` (currently loaded in vLLM), `offline` (not loaded)

| Key | HF Model ID | Notes |
|-----|-------------|-------|
| `qwen3.5-9b` | `Qwen/Qwen3.5-9B` | Default. Thinking mode. |
| `qwen3.5-27b-awq` | `QuantTrio/Qwen3.5-27B-AWQ` | Best quality. AWQ Marlin. |
| `medgemma-4b` | `google/medgemma-1.5-4b-it` | Medical specialist, fast. |
| `medgemma-27b` | `ig1/medgemma-27b-text-it-FP8-Dynamic` | Medical specialist, best quality. |

## Agent Execution

### `POST /api/v1/agent/run`

Runs the agent on a case and streams results via Server-Sent Events (SSE).

**Request body**:

```json
{
  "case_id": "ISCH-STR-S01",
  "hospital": "us_mayo",
  "model": "qwen3.5-9b"
}
```

**Response**: `text/event-stream`

Each event is a JSON object prefixed with `data: ` and terminated by `\n\n`:

```
data: {"type": "run_started", "case_id": "ISCH-STR-S01", "hospital": "us_mayo", "model": "Qwen/Qwen3.5-9B", "max_turns": 15}

data: {"type": "thinking", "turn_number": 1, "content": "Given the acute onset...", "token_usage": {"prompt_tokens": 2048, "completion_tokens": 256, "total_tokens": 2304}}

data: {"type": "tool_call", "turn_number": 1, "tool_name": "analyze_brain_mri", "arguments": {"clinical_context": "acute stroke"}}

data: {"type": "tool_result", "turn_number": 2, "tool_name": "analyze_brain_mri", "success": true, "output": {"tool_name": "analyze_brain_mri", "success": true, "output": {...}}}

data: {"type": "reflection", "turn_number": 2}

data: {"type": "assessment", "turn_number": 5, "content": "### Primary Diagnosis\n...", "token_usage": {...}}

data: {"type": "run_complete", "total_tool_calls": 4, "tools_called": ["analyze_brain_mri", "interpret_labs", "analyze_ecg", "search_medical_literature"], "total_tokens": 12400, "elapsed_time_seconds": 34.2, "final_response": "### Primary Diagnosis\n..."}
```

### SSE Event Types

| Type | When | Key Fields |
|------|------|------------|
| `run_started` | Immediately | `case_id`, `hospital`, `model`, `max_turns` |
| `thinking` | Agent reasons before tool calls | `turn_number`, `content`, `token_usage` |
| `tool_call` | Before each tool execution | `turn_number`, `tool_name`, `arguments` |
| `tool_result` | After each tool execution | `turn_number`, `tool_name`, `success`, `output` |
| `reflection` | Reflection prompt injected | `turn_number` |
| `assessment` | Final agent output (no tool calls) | `turn_number`, `content`, `token_usage` |
| `run_complete` | End of run | `total_tool_calls`, `tools_called`, `total_tokens`, `elapsed_time_seconds` |
| `error` | On exception | `message` |

Events are streamed in real-time via an async queue — each event appears as the corresponding LLM call or tool execution completes.

### `POST /api/v1/agent/replay`

Replays a saved trace as SSE events with small delays to simulate streaming.

**Request body**:

```json
{ "trace_id": "ISCH-STR-S01_1710446400000000000" }
```

**Response**: Same `text/event-stream` format as `/agent/run`.

## Traces

### `GET /api/v1/traces`

Lists saved trace files available for replay.

**Response**: `TraceSummary[]`

```json
[
  {
    "trace_id": "ISCH-STR-S01_1710446400000000000",
    "case_id": "ISCH-STR-S01",
    "total_tool_calls": 4,
    "tools_called": ["analyze_brain_mri", "interpret_labs"],
    "total_tokens": 12400,
    "elapsed_time_seconds": 34.2
  }
]
```

### `GET /api/v1/traces/{trace_id}`

Downloads the full trace JSON including all events.
