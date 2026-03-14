# CLAUDE.md

## Project Overview

NeuroAgent is a tool-augmented LLM agent for neurological clinical decision support. It reasons through patient cases using a ReAct loop with 7 diagnostic tools, follows hospital-specific protocols, and maintains longitudinal patient memory. The project targets a Nature Machine Intelligence publication.

## Repository Layout

```
medical-agents/                     # uv workspace root
├── agent-platform/                 # Main Python package (neuroagent)
│   ├── src/neuroagent/
│   │   ├── agent/                  # Orchestrator (ReAct loop), reasoning, reflection
│   │   ├── api/                    # FastAPI web server + SSE streaming
│   │   ├── llm/                    # LLM client (OpenAI-compatible), prompts
│   │   ├── tools/                  # 7 diagnostic tools + MockServer + ToolRegistry
│   │   ├── rules/                  # Hospital rules engine (YAML pathways)
│   │   ├── memory/                 # ChromaDB patient memory
│   │   └── evaluation/             # Runner, metrics, noise injector, LLM judge
│   ├── config/
│   │   ├── agent_config.yaml       # Default agent/LLM/rules config
│   │   ├── system_prompts/         # orchestrator.txt, reflection.txt
│   │   └── hospital_rules/         # 5 hospital dirs (us_mayo, uk_nhs, de_charite, jp_todai, br_hcfmusp)
│   ├── scripts/                    # CLI entry points
│   └── tests/                      # pytest suite
├── packages/neuroagent-schemas/    # Shared Pydantic models (NeuroBenchCase, patient, tool outputs)
├── dataset-generation/             # NeuroBench case generation pipeline
├── web/                            # React frontend dashboard
│   ├── src/                        # Vite + React + TypeScript + Tailwind v4
│   └── docs/                       # API reference, component architecture
└── data/
    ├── neurobench_v1/cases/        # 100 JSON case files (10 conditions × 10 cases)
    └── traces/                     # Saved agent execution traces (auto-generated)
```

## Setup & Common Commands

```bash
# Install all packages (from repo root)
uv sync --all-packages

# Start vLLM inference server (requires GPU)
cd agent-platform && ./scripts/serve_model.sh              # default: qwen3.5-9b
cd agent-platform && ./scripts/serve_model.sh medgemma-27b # other models

# Start web dashboard API (port 8888, serves frontend + API)
uv run uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888

# Run a single case from CLI
uv run python agent-platform/scripts/run_single_case.py data/neurobench_v1/cases/ISCH-STR-S01.json

# Run full evaluation
uv run python agent-platform/scripts/run_evaluation.py --split test --hospital us_mayo

# Run tests
uv run pytest agent-platform/tests/ -v

# Frontend dev (from web/)
cd web && npm install && npm run dev    # dev server on :5173, proxies /api to :8888
cd web && npm run build                 # production build → web/dist/
```

## Models

4 models supported via vLLM, configured in `scripts/serve_model.sh`:

| Key | HF Model ID | GPU Memory | Notes |
|-----|-------------|------------|-------|
| `qwen3.5-9b` | `Qwen/Qwen3.5-9B` | ~18 GB | **Default**. Thinking mode + native tool calling. |
| `qwen3.5-27b-awq` | `QuantTrio/Qwen3.5-27B-AWQ` | ~16 GB (AWQ) | Best quality. Marlin kernels for speed. |
| `medgemma-4b` | `google/medgemma-1.5-4b-it` | ~9 GB | Medical specialist. Hermes tool-call parser. |
| `medgemma-27b` | `ig1/medgemma-27b-text-it-FP8-Dynamic` | ~27 GB (FP8) | Medical specialist. Limited to 8K context. |

- Qwen3.5 models use `--reasoning-parser qwen3` (extracts `<think>` tags) and `--tool-call-parser qwen3_coder`
- MedGemma models use `--tool-call-parser hermes`
- All served on single A100-40GB with 95% GPU memory utilization
- LLM client (`llm/client.py`) strips `<think>` tags from Qwen output and parses OpenAI-style tool calls
- Default sampling: temperature=1.0, top_p=0.95, presence_penalty=1.5, max_tokens=8192

## Backend Architecture

### Agent Orchestrator (`agent/orchestrator.py`)
- ReAct loop: up to 15 turns of THINK → ACT (tool call) → OBSERVE → REFLECT
- Two run modes: `run()` returns `AgentTrace`, `run_streaming()` yields SSE event dicts
- System prompt = base prompt + hospital protocols (from RulesEngine) + patient memory (from ChromaDB)
- Final assessment extracted via regex (`### Primary Diagnosis` heading)

### 7 Diagnostic Tools
`analyze_eeg`, `analyze_brain_mri`, `analyze_ecg`, `interpret_labs`, `analyze_csf`, `search_medical_literature`, `check_drug_interactions`

All backed by `MockServer` in evaluation mode — returns pre-generated outputs from `NeuroBenchCase.initial_tool_outputs` and `followup_outputs`.

### Hospital Rules (`rules/rules_engine.py`)
- 5 hospitals: `us_mayo`, `uk_nhs`, `de_charite`, `jp_todai`, `br_hcfmusp`
- Each has YAML pathway files (e.g., `stroke_code.yaml`) with steps, timing, mandatory flags, contraindications
- Injected into the system prompt, not exposed as a tool
- `check_compliance()` compares agent's tool calls against required/contraindicated actions

### Web API (`api/`)
- FastAPI on port 8888, serves REST endpoints + SSE streaming + static frontend
- SSE streaming uses `asyncio.Queue` bridge between sync generator and async response (real-time, not batched)
- Traces auto-saved to `data/traces/` for replay without GPU
- Endpoints: `/api/v1/cases`, `/api/v1/hospitals`, `/api/v1/models`, `/api/v1/agent/run`, `/api/v1/agent/replay`, `/api/v1/traces`

## Data

### NeuroBench Cases (`data/neurobench_v1/cases/`)
100 cases, 10 neurological conditions:
- `ISCH-STR` (ischemic stroke), `FEPI-TEMP` (focal epilepsy), `MS-RR` (relapsing MS), `ALZ-EARLY` (early Alzheimer's), `PD` (Parkinson's), `GLIO-HG` (glioblastoma), `BACT-MEN` (bacterial meningitis), `NMDAR-ENC` (NMDAR encephalitis), `FND` (functional neurological disorder), `SYNC-CARD` (cardiac syncope)

Each case contains: patient profile, initial tool outputs (EEG/MRI/ECG/labs/CSF), conditional followup outputs, and comprehensive ground truth (diagnosis, differentials, optimal actions, critical/contraindicated actions, key reasoning points).

Difficulty levels: straightforward (S), moderate (M), diagnostic puzzle (P).

### Schemas (`packages/neuroagent-schemas/`)
Pydantic models shared across packages: `NeuroBenchCase`, `PatientProfile`, `EEGReport`, `MRIReport`, `ECGReport`, `LabResults`, `CSFResults`, `LiteratureSearchResult`, `DrugInteractionResult`, `GroundTruth`.

## Frontend (web/)

Vite + React 18 + TypeScript + Tailwind CSS v4. 3-panel dashboard:
- Left: Case browser (grouped by condition, search + difficulty filters)
- Center: Patient viewer (vitals, history, neuro exam, ground truth)
- Right: Agent execution timeline (thinking blocks, tool call cards, assessment)

State: Zustand (agent streaming state) + TanStack Query (cached data). Dark/light mode. DM Sans + JetBrains Mono fonts.

## Key Conventions

- Python: Pydantic v2 models, dataclasses for config, `from __future__ import annotations`
- All tool outputs are Pydantic BaseModel instances serialized with `.model_dump()`
- Case IDs follow pattern: `{CONDITION}-{DIFFICULTY}{NUMBER}` (e.g., `ISCH-STR-S01`)
- Hospital rules are YAML files, one per clinical pathway
- Frontend uses `@/` path alias for `src/`, all components are named exports
- Commit style: `feat:`, `fix:`, `docs:` prefixes (conventional commits)
