# Web Dashboard API

The `neuroagent.api` package provides a FastAPI web server for the NeuroAgent dashboard. It reuses the existing agent infrastructure (orchestrator, tools, rules, schemas) and adds HTTP endpoints + SSE streaming.

## Running

```bash
uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888
```

On startup, the server:
1. Pre-loads every dataset registered in `neuroagent.datasets.DATASETS` into memory (currently the single `neurobench` dataset, 600 cases; `v5` is accepted as an alias)
2. Builds a lightweight search index per dataset (case_id, condition, difficulty, patient summary)
3. Creates the `data/traces/` directory for saved agent runs
4. Mounts the frontend static files from `web/dist/` (if the build exists)

## Architecture

```
FastAPI app (app.py)
├── /api/v1/datasets    → cases.py      (list dataset versions, activate one)
├── /api/v1/cases       → cases.py      (list + detail, from the active dataset's cached NeuroBenchCase objects)
├── /api/v1/hospitals   → hospitals.py  (list hospitals + full rules CRUD on the pathway YAML files)
├── /api/v1/models      → models.py     (list with live vLLM status probe, load with SSE progress, unload)
├── /api/v1/agent       → agent.py      (run, replay, and evaluate — all SSE streams)
├── /api/v1/traces      → traces.py     (list, download, delete saved traces)
├── /api/v1/copilot     → copilot.py    (GitHub Copilot device-flow auth + Copilot model list)
└── /                   → StaticFiles   (web/dist/ frontend, if it exists)
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

Two more SSE endpoints share the same event format: `/agent/replay` re-streams a saved trace with delays, and `/agent/evaluate` streams evaluation metrics + LLM-judge output for a completed run against the case's ground truth.

## Models

`GET /models` merges the static registry (`neuroagent/model_registry.py`, 10 models) with a live probe of the local vLLM server to mark which model is currently loaded. `POST /models/{model_key}/load` launches `serve_model.sh` for that model and streams load progress over SSE; `POST /models/unload` kills the vLLM process.

## GitHub Copilot integration

The `copilot` router lets the dashboard use GitHub Copilot chat models as an alternative backend:

- `POST /copilot/device-code` — start the GitHub OAuth device flow (returns `user_code` + `verification_uri`)
- `POST /copilot/poll-token` — poll for the OAuth token after the user enters the code (`pending`/`complete`/`expired`/`denied`)
- `GET /copilot/status` — whether a GitHub token is stored and Copilot access works
- `GET /copilot/models` — static list of Copilot chat models, keyed `copilot:<id>` (empty if not authenticated)
- `POST /copilot/logout` — clear stored tokens

The GitHub token persists to `data/.copilot_token.json` and is exchanged (with in-memory caching) for a short-lived Copilot API token. Agent endpoints accept `copilot:<id>` model keys and route those requests to `https://api.githubcopilot.com` instead of the local vLLM server.

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
├── app.py              # create_app() factory, dataset pre-loading, CORS, static files
└── routes/
    ├── __init__.py
    ├── cases.py        # GET /datasets, POST /datasets/{version}/activate, GET /cases, GET /cases/{id}
    ├── hospitals.py    # GET /hospitals, GET /hospitals/{id}/rules,
    │                   # POST/PUT/DELETE /hospitals/{id}/rules[/{pathway_index}]
    ├── models.py       # GET /models (vLLM probe), POST /models/{key}/load (SSE), POST /models/unload
    ├── agent.py        # POST /agent/run (SSE), POST /agent/replay (SSE), POST /agent/evaluate (SSE)
    ├── traces.py       # GET /traces, GET /traces/{id}, DELETE /traces/{id}
    └── copilot.py      # POST /copilot/device-code, POST /copilot/poll-token, GET /copilot/status,
                        # GET /copilot/models, POST /copilot/logout
```

For the full API reference with request/response schemas, see [`web/docs/api.md`](../../web/docs/api.md).
