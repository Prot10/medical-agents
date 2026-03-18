# CLAUDE.md

## What is this project

NeuroAgent: tool-augmented LLM agent for neurological clinical decision support. ReAct loop + 12 diagnostic tools + hospital protocols + patient memory + cost tracking. Targeting Nature Machine Intelligence.

See README.md for full project docs, setup, and architecture.

## Key paths

- `agent-platform/src/neuroagent/` — main Python package
- `packages/neuroagent-schemas/` — shared Pydantic models
- `dataset-generation/` — NeuroBench case generation
- `web/src/` — React frontend (Vite + TypeScript + Tailwind v4)
- `data/neurobench_v{1,2}/cases/` — 200 benchmark cases (JSON)
- `data/neurobench_v3/cases/` — 200 benchmark cases with realistic tool outputs (v1+v2 combined, stripped)
- `data/neurobench_v4/cases/` — 200 benchmark cases with 12-tool schema and cost tracking (v3 migrated)
- `agent-platform/config/hospital_rules/{hospital}/*.yaml` — clinical pathways
- `agent-platform/config/tool_costs.yaml` — per-tool cost registry (Medicare reference rates)

## Common commands

```bash
uv sync --all-packages                    # install everything
cd web && npm run build                   # build frontend
uv run uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888  # start server
cd web && npm run dev                     # frontend dev (local)
cd web && npm run dev:remote              # frontend dev (remote VM, binds 0.0.0.0)
uv run pytest agent-platform/tests/ -v   # tests
./agent-platform/scripts/run_v3_full.sh                       # full model comparison (v3, 7 tools)
./agent-platform/scripts/run_v4_full.sh                       # full model comparison (v4, 12 tools + cost)
uv run python agent-platform/scripts/create_v3_dataset.py     # regenerate v3 from v1+v2
uv run python agent-platform/scripts/migrate_v3_to_v4.py     # migrate v3→v4 (12-tool schema)
```

## Conventions

- Python: Pydantic v2 models, dataclasses for config, `from __future__ import annotations`
- All tool outputs are Pydantic BaseModel instances serialized with `.model_dump()`
- Case IDs: `{CONDITION}-{S|M|P}{NUMBER}` (v1) or `{CONDITION}-R{S|M|P}{NUMBER}` (v2)
- Hospital rules: YAML files, one per clinical pathway, inside per-hospital subdirectories
- Frontend: `@/` path alias for `src/`, named exports only, no default exports for components
- State: Zustand for UI/streaming state, TanStack Query for server data
- Commit style: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
- Dataset versions: v1 (synthetic, enhanced outputs), v2 (real-seeded, enhanced), v3 (v1+v2 combined, realistic/stripped outputs), v4 (12-tool schema + cost tracking, migrated from v3)
- Tool output modes: "enhanced" (v1/v2, interpretive fields present) vs "realistic" (v3/v4, stripped to match real clinical reports)
- 12 tools: analyze_brain_mri, analyze_eeg, analyze_ecg, interpret_labs, analyze_csf, order_ct_scan, order_echocardiogram, order_cardiac_monitoring, order_advanced_imaging, order_specialized_test, search_medical_literature, check_drug_interactions
- Cost tracking: `CostTracker` in `tools/cost_tracker.py`, config in `config/tool_costs.yaml`, Medicare PFS reference rates
- Evaluation: `format_patient_info()` in `evaluation/runner.py` is the single source of truth for patient presentation formatting

## Models

4 vLLM models on A100-40GB. Qwen3.5 uses `--reasoning-parser qwen3` + `--tool-call-parser qwen3_coder`. MedGemma uses `--tool-call-parser hermes`. On Mac use Ollama.

LLM client (`llm/client.py`) strips `<think>` tags from Qwen and parses OpenAI-style tool calls. Default sampling: temperature=1.0, top_p=0.95, presence_penalty=1.5, max_tokens=8192.

## Architecture notes

- Agent orchestrator: ReAct loop up to 15 turns, system prompt = base + hospital rules + patient memory
- Web API: FastAPI port 8888, serves REST + SSE streaming + static frontend from `web/dist/`
- SSE streaming uses `asyncio.Queue` bridge between sync generator and async response
- Model loading/unloading via `/api/v1/models/{key}/load` (SSE progress) and `/api/v1/models/unload`
- Hospital rules CRUD via `/api/v1/hospitals/{id}/rules` endpoints
- Traces auto-saved to `data/traces/` for replay without GPU
- `MockServer` in evaluation mode returns pre-generated outputs from NeuroBench case files
