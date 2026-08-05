# CLAUDE.md

## What is this project

NeuroAgent: tool-augmented LLM agent for neurological clinical decision support. ReAct loop + 16 diagnostic tools + hospital protocols + cost tracking. Targeting Nature Machine Intelligence.

See README.md for setup, and `docs/README.md` for the documentation index.

## Key paths

- `agent-platform/src/neuroagent/` — main Python package
- `agent-platform/src/neuroagent/api/` — main FastAPI app (port 8888)
- `agent-platform/src/neuroagent/review_api/` — review FastAPI app (port 8889, separate startup)
- `packages/neuroagent-schemas/` — shared Pydantic models
- `dataset-generation/` — NeuroBench case generation
- `web/src/` — main React dashboard (port 5173)
- `web-review/src/` — dataset review UI (port 5174, self-contained fork of the main app's primitives)
- `data/neurobench/cases/` — 600 benchmark cases across 20 conditions (current default)
- `data/review/annotations/{version}/{reviewer_code}/{case_id}.json` — per-reviewer annotation runtime data (gitignored)
- `agent-platform/config/hospital_rules/{hospital}/*.yaml` — clinical pathways
- `agent-platform/config/runtime/agent.yaml` — agent runtime defaults loaded by `load_agent_config()`
- `agent-platform/config/review/reviewer_codes.yaml` — review-app reviewer registry (hot-reloads on mtime)
- `agent-platform/config/tools/costs.yaml` — per-tool cost registry (Medicare reference rates)

## Common commands

```bash
uv sync --all-packages                    # app + eval (agent, dataset tools)
uv sync --all-packages --extra training   # + training deps (torch/trl/peft/bitsandbytes/flash-linear-attention/liger); required for SFT/RFT
cd web && npm run build                   # build main frontend
uv run uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888         # main API
uv run uvicorn neuroagent.review_api.app:app --host 0.0.0.0 --port 8889  # review API
cd web && npm run dev                     # main frontend dev (local)
cd web && npm run dev:remote              # main frontend dev (remote VM, binds 0.0.0.0)
cd web-review && npm install && npm run dev:remote   # review frontend dev (port 5174)
uv run pytest agent-platform/tests/ -v   # tests
uv run python agent-platform/scripts/runtime/run_single_case.py data/neurobench/cases/<case>.json
uv run python agent-platform/scripts/benchmark/run_baseline_eval.py

# Fine-tuning (needs --extra training). Base models load from EOS→/dev/shm; adapters write to EOS.
PRECISION=bf16 bash agent-platform/scripts/training/run_sft_training.sh Qwen/Qwen3.5-9B   # SFT (PRECISION=qlora default)
bash agent-platform/scripts/training/run_definitive_eval.sh Qwen3.5-9B                    # greedy+reliability eval + judge bundles
bash agent-platform/scripts/training/run_rft.sh Qwen3.5-9B                                # rejection-sampling FT: rollouts → filtered dataset
```

See `docs/training/sft-recipe-hardware-and-evaluation.md` for the recipe, bf16-vs-QLoRA, memory,
and the literature-aligned evaluation; `docs/training/distillation.md` for trajectory generation.

## Conventions

- Python: Pydantic v2 models, dataclasses for config, `from __future__ import annotations`
- All tool outputs are Pydantic BaseModel instances serialized with `.model_dump()`
- Case IDs: `{CONDITION}-{S|M|P}{NUMBER}` (v1) or `{CONDITION}-R{S|M|P}{NUMBER}` (v2)
- Hospital rules: YAML files, one per clinical pathway, inside per-hospital subdirectories
- Frontend: `@/` path alias for `src/`, named exports only, no default exports for components
- State: Zustand for UI/streaming state, TanStack Query for server data
- Commit style: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
- Dataset versions: v1 (synthetic, enhanced outputs), v2 (real-seeded, enhanced), v3 (v1+v2 combined, realistic/stripped outputs), v4 (12-tool schema + cost tracking, migrated from v3), v5 (current: 600 cases across 20 conditions, 500 train / 100 test)
- Tool output modes: "enhanced" (v1/v2, interpretive fields present) vs "realistic" (v3/v4, stripped to match real clinical reports)
- 16 tools: analyze_brain_mri, analyze_eeg, analyze_ecg, interpret_labs, analyze_csf, order_ct_scan, order_echocardiogram, order_cardiac_monitoring, order_advanced_imaging, order_specialized_test, search_medical_literature, check_drug_interactions,
  and (added after the July 2026 clinical tool review) order_body_imaging, order_microbiology, obtain_tissue_diagnosis, perform_clinical_assessment
- Cost tracking: `CostTracker` in `tools/cost_tracker.py`, config in `config/tools/costs.yaml`, Medicare PFS reference rates
- Tool vocabulary: `costs.yaml` is the single source; `tools/vocabulary.py` generates every enum from it,
  so a term cannot exist without a price. `order_advanced_imaging` takes `modality` (13 values);
  `order_specialized_test` takes `test_type` (19 + `genetic_panel:<panel>`); `order_body_imaging` takes
  `study` (9, `<region>_<modality>`); `order_microbiology` takes `specimen` (5); `obtain_tissue_diagnosis`
  takes `procedure` (2) + `molecular_assays` (11); `perform_clinical_assessment` takes `assessment_type` (4).
  `interpret_labs.panels` (153) and `analyze_csf.special_tests` (22) are advisory, not closed — an unlisted
  assay runs at the default rate.
  The review app mirrors these schemas in `review_api/services/tool_io.py` because `tools/` is not deployed
  to the review VPS; `tests/test_tool_io_schemas.py` fails CI if the mirror drifts. It did, silently, and the
  clinical reviewers assessed a stale catalog — see `docs/benchmark/tool-review-2026-07.md`.
- Scoring is per-study, not per-tool: `evaluation/metrics.py::_SCALAR_DISCRIMINATORS` /
  `_SET_DISCRIMINATORS` decide which parameter identifies the study, and every one of them is
  cost-bearing in `costs.yaml`. Adding a discriminating parameter to a tool means adding it there too
- Case contract: `agent-platform/scripts/validation/validate_cases.py` must report 0 issues on 600/600.
  Read `docs/benchmark/tool-contract.md` before editing a case or a tool schema
- `consult_medical_specialist` does not exist; a specialist referral is an action with `tool_name: null`
- Evaluation: `format_patient_info()` in `evaluation/runner.py` is the single source of truth for patient presentation formatting

## Models

10 models in `model_registry.py`, served one at a time on the A100-40GB (`scripts/runtime/serve_model.sh`). Qwen3.5 uses `--reasoning-parser qwen3` + `--tool-call-parser qwen3_coder`. MedGemma uses `--tool-call-parser hermes`. On Mac use Ollama.

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
- Frontend: `web-review/` (Vite + React 19 + Tailwind v4 + framer-motion). Carries its own copies of the UI primitives (forked from `web/src` and intentionally diverged — light theme, borders); it does not import from the main app. Vite proxies `/api` → `http://127.0.0.1:8889`. Light theme is the default.
- Reviewer registry: `agent-platform/config/review/reviewer_codes.yaml` — hand-edited; backend reloads on YAML mtime change inside the `current_reviewer` FastAPI dependency.
- Annotation storage: `data/review/annotations/{version}/{reviewer_code}/{case_id}.json` — one file per (reviewer, version, case) triple. Filesystem-level isolation: a reviewer endpoint cannot return another reviewer's data.
- Tabs: Overview (per-reviewer progress) / Cases (600 v5 cases) / Methodology (showcase) / Admin (4 aggregate views: inter-rater agreement, reviewer progress, field hotspots, side-by-side diff).
- Annotation gesture: hover an `AnnotatableField` → primary-color Comment pill in margin → Radix Popover with severity (note/issue/error) + textarea + `⌘↵` save. Annotated fields get a persistent left border colored by highest severity + count badge.
- Status flow per case per reviewer: `pending` → `in_progress` (auto on first annotation) → `needs_changes` / `approved`. Each reviewer's status is independent; admin agreement view aggregates them.
