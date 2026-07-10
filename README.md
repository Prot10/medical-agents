# NeuroAgent

Tool-augmented LLM agent for neurological clinical decision support. Reasons through patient cases using a ReAct loop with 12 diagnostic tools and follows hospital-specific protocols.

Targeting a **Nature Machine Intelligence** publication.

## Repository Layout

```
medical-agents/                     # uv workspace root
├── agent-platform/                 # Main Python package (neuroagent)
│   ├── src/neuroagent/
│   │   ├── agent/                  # Orchestrator (ReAct loop), reasoning, reflection
│   │   ├── api/                    # Main FastAPI app (port 8888) — agent runs, traces, models
│   │   ├── review_api/             # Separate FastAPI app (port 8889) — dataset review
│   │   ├── llm/                    # LLM client (OpenAI-compatible), prompts
│   │   ├── tools/                  # 12 diagnostic tools + MockServer + ToolRegistry
│   │   ├── rules/                  # Hospital rules engine (YAML pathways)
│   │   └── evaluation/             # Runner, metrics, noise injector, LLM judge
│   ├── config/
│   │   ├── system_prompts/         # orchestrator.txt, reflection.txt, llm_judge.txt
│   │   ├── hospital_rules/         # 5 hospital dirs
│   │   ├── runtime/                # Agent runtime defaults
│   │   ├── tools/                  # Tool cost registry
│   │   ├── training/               # Training reward config
│   │   └── review/                 # Reviewer-code registry (reviewer_codes.yaml)
│   ├── scripts/                    # CLI entry points + vLLM serve scripts
│   └── tests/                      # pytest suite
├── packages/neuroagent-schemas/    # Shared Pydantic models
├── dataset-generation/             # NeuroBench case generation pipeline
├── web/                            # Main React dashboard (port 5173)
├── web-review/                     # Dataset review UI (port 5174, shares tokens with web/)
└── data/
    ├── neurobench/cases/        # 600 cases across 20 conditions
    ├── review/annotations/         # Per-reviewer annotation files (runtime, gitignored)
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
uv run python agent-platform/scripts/runtime/run_single_case.py \
  data/neurobench/cases/<case>.json \
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

System prompt = base prompt + hospital protocols.

### 12 Diagnostic Tools

`analyze_brain_mri`, `analyze_eeg`, `analyze_ecg`, `interpret_labs`, `analyze_csf`, `order_ct_scan`, `order_echocardiogram`, `order_cardiac_monitoring`, `order_advanced_imaging`, `order_specialized_test`, `search_medical_literature`, `check_drug_interactions`

In evaluation mode, all backed by `MockServer` returning pre-generated outputs from the NeuroBench case files.

### Hospital Rules

5 hospitals with YAML pathway files: `us_mayo`, `uk_nhs`, `de_charite`, `jp_todai`, `br_hcfmusp`. Each pathway defines mandatory steps, timing, conditions, and contraindicated actions. Rules are injected into the system prompt and compliance is checked post-run.

Rules can be viewed, edited, and created from the web UI (sidebar → Rules tab).

### Web API

FastAPI on port 8888. Serves REST endpoints, SSE streaming for agent runs, and the built frontend as static files.

Key endpoints: `/api/v1/cases`, `/api/v1/hospitals`, `/api/v1/models`, `/api/v1/agent/run`, `/api/v1/agent/replay`, `/api/v1/traces`

### Web Dashboard

Vite + React 19 + TypeScript + Tailwind CSS v4. 3-panel layout:
- **Left (sidebar)**: Case browser, dataset analytics, trace replay, hospital rules editor, settings
- **Center**: Patient viewer / pathway editor / dataset dashboard
- **Right**: Agent execution timeline with real-time SSE streaming

State: Zustand + TanStack Query. Dark/light mode.

## NeuroBench Dataset

Each case contains: patient profile, initial tool outputs, conditional followup outputs, and comprehensive ground truth.

Difficulty levels: straightforward (S), moderate (M), diagnostic puzzle (P).

## Dataset Review App

A separate app for doctor-led review of the NeuroBench dataset. Built for a **blind triple-review** workflow: three reviewers work asynchronously and in isolation (each has a personal code; no one can see another reviewer's annotations or status decisions). An admin code unlocks aggregate views for the researcher.

- Backend: `agent-platform/src/neuroagent/review_api/` — FastAPI on **port 8889**, file-based persistence, gated by `X-Reviewer-Code` header
- Frontend: `web-review/` — separate Vite/React app on **port 5174**, shares design tokens with `web/` via the `@web/*` alias
- Reviewer codes: hand-edited in `agent-platform/config/review/reviewer_codes.yaml` (hot-reloads on mtime change)
- Annotations: `data/review/annotations/{version}/{reviewer_code}/{case_id}.json` (filesystem isolation per reviewer)

### Run

```bash
# Terminal 1 — backend
uv run uvicorn neuroagent.review_api.app:app --host 0.0.0.0 --port 8889

# Terminal 2 — frontend (Vite proxies /api → :8889)
cd web-review && npm install
npm run dev:remote    # binds 0.0.0.0:5174 for remote VM access
# or: npm run dev     # local only
```

Open `http://<vm-host>:5174` and enter a reviewer code from `reviewer_codes.yaml`.

### Reviewer experience

- **Code entry gate** on first visit; code stored in `localStorage` and sent on every request as `X-Reviewer-Code`
- **Overview tab**: progress strip (approved / needs-changes / in-progress / pending), recent cases, milestones, Random-Pending CTA
- **Cases tab**: 516-row hybrid list with status-colored left border, condition pill, severity dot cluster, multi-select condition filter, search, and a Random-Pending button
- **Case detail**: header + chief complaint pull-quote + patient/vitals + HPI (Source Serif Pro) + neuro exam + initial workup (collapsible) + diagnostic pathway timeline + ground truth showcase (differential cards, optimal actions, critical / contraindicated, red herrings, teaching pearls) + metadata
- **Field-level annotation gesture**: hover any field → primary-color "Comment" pill appears in the margin → popover with severity (note / issue / error) + free-text + `⌘↵` to save. Already-annotated fields get a persistent left border colored by highest severity + count badge
- **Annotation sidebar**: 4-state status switcher (pending / in-progress / needs-changes / approved), case-wide thread, severity-filterable field annotations, Approve case + Next-Pending CTAs
- **Methodology tab**: hero numbers, 4-stage pipeline diagram (PMC seeds → synthetic augmentation → tool outputs → ground truth) with framer-motion scroll reveal, 20-condition small-multiples grid, severity + encounter charts
- **Admin tab** (admin role only): inter-rater agreement table with consensus badges, per-reviewer progress dashboard, field hotspots (sortable), side-by-side diff per case (field-as-row layout)

### Deploy notes

The frontend can be served by anything that hosts static files (Nginx, Vercel, Netlify). The backend is a small Python container — no GPU required. The annotation store and reviewer YAML can live on a persistent volume; both are file-based and easy to back up.

## Evaluation

```bash
# Single case
uv run python agent-platform/scripts/runtime/run_single_case.py data/neurobench/cases/<case>.json

# Full benchmark (4 models × 2 modes × 3 hospitals × 3 reps)
uv run python agent-platform/scripts/benchmark/run_full_benchmark.py

# Resume after interruption (auto-checkpoints)
uv run python agent-platform/scripts/benchmark/run_full_benchmark.py  # same command, skips completed
```

> Results produced before the tool-contract migration are not comparable with
> results produced after it: optimal cost changed in 293 of 600 cases and a perfect
> agent was previously scored below 1.0 recall on 245. See
> [`docs/benchmark/tool-contract.md`](docs/benchmark/tool-contract.md).

## Tests

```bash
uv run pytest agent-platform/tests/ -v
```
