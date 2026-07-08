# CLAUDE.md

## What is this project

NeuroAgent: tool-augmented LLM agent for neurological clinical decision support. ReAct loop + 12 diagnostic tools + hospital protocols + cost tracking. Targeting Nature Machine Intelligence.

See README.md for full project docs, setup, and architecture.

## Key paths

- `agent-platform/src/neuroagent/` — main Python package
- `agent-platform/src/neuroagent/api/` — main FastAPI app (port 8888)
- `agent-platform/src/neuroagent/review_api/` — review FastAPI app (port 8889, separate startup)
- `packages/neuroagent-schemas/` — shared Pydantic models
- `dataset-generation/` — NeuroBench case generation
- `web/src/` — main React dashboard (port 5173)
- `web-review/src/` — dataset review UI (port 5174, imports primitives via `@web/*` alias)
- `data/neurobench_v{1,2}/cases/` — 200 benchmark cases (JSON)
- `data/neurobench_v3/cases/` — 200 benchmark cases with realistic tool outputs (v1+v2 combined, stripped)
- `data/neurobench_v4/cases/` — 200 benchmark cases with 12-tool schema and cost tracking (v3 migrated)
- `data/neurobench_v5/cases/` — 600 benchmark cases across 20 conditions (current default)
- `data/review/annotations/{version}/{reviewer_code}/{case_id}.json` — per-reviewer annotation runtime data (gitignored)
- `agent-platform/config/hospital_rules/{hospital}/*.yaml` — clinical pathways
- `agent-platform/config/runtime/agent.yaml` — agent runtime defaults loaded by `load_agent_config()`
- `agent-platform/config/review/reviewer_codes.yaml` — review-app reviewer registry (hot-reloads on mtime)
- `agent-platform/config/tools/costs.yaml` — per-tool cost registry (Medicare reference rates)

## Common commands

```bash
uv sync --all-packages                    # install everything
cd web && npm run build                   # build main frontend
uv run uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888         # main API
uv run uvicorn neuroagent.review_api.app:app --host 0.0.0.0 --port 8889  # review API
cd web && npm run dev                     # main frontend dev (local)
cd web && npm run dev:remote              # main frontend dev (remote VM, binds 0.0.0.0)
cd web-review && npm install && npm run dev:remote   # review frontend dev (port 5174)
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
- Cost tracking: `CostTracker` in `tools/cost_tracker.py`, config in `config/tools/costs.yaml`, Medicare PFS reference rates
- Evaluation: `format_patient_info()` in `evaluation/runner.py` is the single source of truth for patient presentation formatting

## Models

4 vLLM models on A100-40GB. Qwen3.5 uses `--reasoning-parser qwen3` + `--tool-call-parser qwen3_coder`. MedGemma uses `--tool-call-parser hermes`. On Mac use Ollama.

LLM client (`llm/client.py`) strips `<think>` tags from Qwen and parses OpenAI-style tool calls. Default sampling: temperature=1.0, top_p=0.95, presence_penalty=1.5, max_tokens=8192.

## Architecture notes

- Agent orchestrator: ReAct loop up to 15 turns, system prompt = base + hospital rules
- Web API: FastAPI port 8888, serves REST + SSE streaming + static frontend from `web/dist/`
- SSE streaming uses `asyncio.Queue` bridge between sync generator and async response
- Model loading/unloading via `/api/v1/models/{key}/load` (SSE progress) and `/api/v1/models/unload`
- Hospital rules CRUD via `/api/v1/hospitals/{id}/rules` endpoints
- Traces auto-saved to `data/traces/` for replay without GPU
- `MockServer` in evaluation mode returns pre-generated outputs from NeuroBench case files

## Dataset review app

Separate FastAPI + Vite app for blind triple-review of the NeuroBench dataset. Independent from the main agent — its own startup command, port, and Vite project, but reuses the `NeuroBenchCase` Pydantic schema.

- Backend: `agent-platform/src/neuroagent/review_api/app.py` on port 8889. File-based persistence under `data/review/annotations/`. Gated by `X-Reviewer-Code` header; admin role unlocks aggregate endpoints under `/api/v1/admin/...`.
- Frontend: `web-review/` (Vite + React 19 + Tailwind v4 + framer-motion). Vite alias `@web/*` → `../web/src/*` so it can import primitives from the main app without a refactor. Vite proxies `/api` → `http://127.0.0.1:8889`. Light theme is the default.
- Reviewer registry: `agent-platform/config/review/reviewer_codes.yaml` — hand-edited; backend reloads on YAML mtime change inside the `current_reviewer` FastAPI dependency.
- Annotation storage: `data/review/annotations/{version}/{reviewer_code}/{case_id}.json` — one file per (reviewer, version, case) triple. Filesystem-level isolation: a reviewer endpoint cannot return another reviewer's data.
- Tabs: Overview (per-reviewer progress) / Cases (600 v5 cases) / Methodology (showcase) / Admin (4 aggregate views: inter-rater agreement, reviewer progress, field hotspots, side-by-side diff).
- Annotation gesture: hover an `AnnotatableField` → primary-color Comment pill in margin → Radix Popover with severity (note/issue/error) + textarea + `⌘↵` save. Annotated fields get a persistent left border colored by highest severity + count badge.
- Status flow per case per reviewer: `pending` → `in_progress` (auto on first annotation) → `needs_changes` / `approved`. Each reviewer's status is independent; admin agreement view aggregates them.
