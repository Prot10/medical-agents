# NeuroAgent

Tool-augmented LLM agent for neurological clinical decision support. Reasons through patient cases using a ReAct loop with 7 diagnostic tools, follows hospital-specific protocols, and maintains longitudinal patient memory.

Targeting a **Nature Machine Intelligence** publication.

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
│   │   └── hospital_rules/         # 5 hospital dirs
│   ├── scripts/                    # CLI entry points + vLLM serve scripts
│   └── tests/                      # pytest suite
├── packages/neuroagent-schemas/    # Shared Pydantic models
├── dataset-generation/             # NeuroBench case generation pipeline
├── web/                            # React frontend dashboard
└── data/
    ├── neurobench_v1/cases/        # 100 synthetic JSON cases
    ├── neurobench_v2/cases/        # 100 real-case-seeded JSON cases
    └── traces/                     # Saved agent execution traces
```

## Quick Start

### Prerequisites

- Python 3.11+ and [uv](https://github.com/astral-sh/uv)
- Node.js 20+ (for frontend)
- GPU with CUDA (for vLLM) or [Ollama](https://ollama.com) (for Mac)

### Install

```bash
uv sync --all-packages
cd web && npm install
```

### Run on GPU server (CERN VM / any Linux with CUDA)

```bash
# 1. Build the frontend
cd web && npm run build && cd ..

# 2. Start the web dashboard (serves API + frontend on port 8888)
uv run uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888
```

Open http://localhost:8888 — models can be loaded/unloaded directly from the UI.

If accessing from a remote machine, SSH tunnel the port:

```bash
# Inside CERN network
ssh -L 8888:localhost:8888 <user>@<vm>.cern.ch

# Outside CERN network (via lxplus jump host)
ssh -L 8888:localhost:8888 -J <user>@lxplus.cern.ch <user>@<vm>.cern.ch
```

Then open http://localhost:8888 in your local browser.

### Run on Mac (no GPU)

```bash
# Install Ollama: https://ollama.com
ollama pull qwen3.5:4b

# Run a single case via CLI
uv run python agent-platform/scripts/run_single_case.py \
  data/neurobench_v1/cases/ISCH-STR-S01.json \
  --model qwen3.5:4b \
  --base-url http://localhost:11434/v1
```

### Frontend development (hot reload)

```bash
# Terminal 1: API server
uv run uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888

# Terminal 2: Vite dev server (proxies /api to :8888)
cd web && npm run dev          # local
cd web && npm run dev:remote   # remote VM (binds 0.0.0.0)
```

## Models

4 models supported via vLLM on a single A100-40GB:

| Key | HF Model ID | VRAM | Load time |
|-----|-------------|------|-----------|
| `qwen3.5-9b` | `Qwen/Qwen3.5-9B` | ~18 GB | ~40s |
| `qwen3.5-27b-awq` | `QuantTrio/Qwen3.5-27B-AWQ` | ~16 GB | ~65s |
| `medgemma-4b` | `google/medgemma-1.5-4b-it` | ~9 GB | ~70s |
| `medgemma-27b` | `ig1/medgemma-27b-text-it-FP8-Dynamic` | ~27 GB | ~50s |

Models can be loaded/switched from the web UI (sidebar → model selector → Load button). Only one model runs at a time; switching unloads the previous one automatically.

For Mac: use Ollama with `qwen3.5:4b` or `qwen3.5:8b`.

## Architecture

### Agent

ReAct loop (up to 15 turns): THINK → ACT (tool call) → OBSERVE → REFLECT. Two modes: `run()` returns `AgentTrace`, `run_streaming()` yields SSE events.

System prompt = base prompt + hospital protocols + patient memory.

### 7 Diagnostic Tools

`analyze_eeg`, `analyze_brain_mri`, `analyze_ecg`, `interpret_labs`, `analyze_csf`, `search_medical_literature`, `check_drug_interactions`

In evaluation mode, all backed by `MockServer` returning pre-generated outputs from the NeuroBench case files.

### Hospital Rules

5 hospitals with YAML pathway files: `us_mayo`, `uk_nhs`, `de_charite`, `jp_todai`, `br_hcfmusp`. Each pathway defines mandatory steps, timing, conditions, and contraindicated actions. Rules are injected into the system prompt and compliance is checked post-run.

Rules can be viewed, edited, and created from the web UI (sidebar → Rules tab).

### Web API

FastAPI on port 8888. Serves REST endpoints, SSE streaming for agent runs, and the built frontend as static files.

Key endpoints: `/api/v1/cases`, `/api/v1/hospitals`, `/api/v1/models`, `/api/v1/agent/run`, `/api/v1/agent/replay`, `/api/v1/traces`

### Web Dashboard

Vite + React 18 + TypeScript + Tailwind CSS v4. 3-panel layout:
- **Left (sidebar)**: Case browser, dataset analytics, trace replay, hospital rules editor, settings
- **Center**: Patient viewer / pathway editor / dataset dashboard
- **Right**: Agent execution timeline with real-time SSE streaming

State: Zustand + TanStack Query. Dark/light mode.

## NeuroBench Dataset

200 cases across 10 neurological conditions: ischemic stroke, focal epilepsy, relapsing MS, early Alzheimer's, Parkinson's, glioblastoma, bacterial meningitis, NMDAR encephalitis, FND, cardiac syncope.

- **v1** (100 cases): Fully synthetic, generated by Claude
- **v2** (100 cases): Seeded from 94 peer-reviewed PMC case reports (CC-BY 4.0)

Each case contains: patient profile, initial tool outputs, conditional followup outputs, and comprehensive ground truth.

Difficulty levels: straightforward (S), moderate (M), diagnostic puzzle (P).

## Evaluation

```bash
# Single case
uv run python agent-platform/scripts/run_single_case.py data/neurobench_v1/cases/ISCH-STR-S01.json

# Full benchmark (4 models × 2 modes × 3 hospitals × 3 reps)
uv run python agent-platform/scripts/run_full_benchmark.py

# Resume after interruption (auto-checkpoints)
uv run python agent-platform/scripts/run_full_benchmark.py  # same command, skips completed
```

## Tests

```bash
uv run pytest agent-platform/tests/ -v
```
