# Web Dashboard API

The `neuroagent.api` package provides a FastAPI web server for the NeuroAgent dashboard. It reuses the existing agent infrastructure (orchestrator, tools, rules, schemas) and adds HTTP endpoints + SSE streaming.

## Running

```bash
uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888
```

On startup, the server:
1. Loads all NeuroBench cases from `data/neurobench_v1/cases/` into memory
2. Builds a lightweight search index (case_id, condition, difficulty, patient summary)
3. Creates the `data/traces/` directory for saved agent runs
4. Mounts the frontend static files from `web/dist/` (if the build exists)

## Architecture

```
FastAPI app (app.py)
├── /api/v1/cases       → cases.py      (list + detail, from cached NeuroBenchCase objects)
├── /api/v1/hospitals   → hospitals.py   (list + rules, from RulesEngine)
├── /api/v1/models      → models.py      (list with live vLLM status probe via httpx)
├── /api/v1/agent/run   → agent.py       (SSE streaming via AgentOrchestrator.run_streaming())
├── /api/v1/agent/replay→ agent.py       (SSE replay of saved traces with delays)
├── /api/v1/traces      → traces.py      (list + download saved traces)
└── /                   → StaticFiles    (web/dist/ frontend, if it exists)
```

## SSE Streaming

The `/agent/run` endpoint is the critical path. It:

1. Creates a `MockServer`, `ToolRegistry`, `RulesEngine`, and `AgentOrchestrator` per request
2. Yields `run_started` immediately
3. Launches `orchestrator.run_streaming()` in a thread pool (`run_in_executor`)
4. Uses an `asyncio.Queue` to bridge between the synchronous generator and the async SSE response
5. Each event is yielded to the client as it's produced (real-time, not batched)
6. On completion, saves the full trace to `data/traces/` for replay

This design means:
- The LLM calls happen in a background thread (non-blocking for the event loop)
- Events appear in the browser as each LLM call / tool execution finishes
- Multiple concurrent runs are safe (each gets its own orchestrator instance)

## Dependencies

The API adds these dependencies beyond the base `neuroagent` package:
- `fastapi` — web framework
- `uvicorn` — ASGI server
- `httpx` — async HTTP client (for vLLM status probe)

Install them with:
```bash
uv pip install fastapi uvicorn httpx --python .venv/bin/python
```

## Module Structure

```
neuroagent/api/
├── __init__.py
├── app.py              # create_app() factory, case index, CORS, static files
└── routes/
    ├── __init__.py
    ├── cases.py        # GET /cases, GET /cases/{id}
    ├── hospitals.py    # GET /hospitals, GET /hospitals/{id}/rules
    ├── models.py       # GET /models (with vLLM probe)
    ├── agent.py        # POST /agent/run (SSE), POST /agent/replay (SSE)
    └── traces.py       # GET /traces, GET /traces/{id}
```

For the full API reference with request/response schemas, see [`web/docs/api.md`](../../web/docs/api.md).
