# NeuroAgent Web Dashboard

Interactive web interface for visualizing the NeuroAgent clinical reasoning process. Select a patient case, choose a hospital protocol, and watch the agent reason through the diagnosis step by step.

## Features

- **Case Browser** — Browse 100 NeuroBench cases across 10 neurological conditions, filter by difficulty
- **Patient Viewer** — Full clinical data display: demographics, vitals (abnormal highlighting), HPI, medications, neurological exam
- **Agent Execution Timeline** — Real-time visualization of the ReAct loop:
  - Thinking/reasoning blocks with markdown rendering
  - Collapsible tool call cards (MRI, EEG, ECG, labs, CSF, literature, drug interactions)
  - 7 specialized result renderers with clinical formatting
  - Reflection steps and final structured assessment
- **Hospital Rules** — Select from 5 hospital protocol sets (Mayo/AAN, NHS/NICE, Charité/DGN, Todai/JSN, HC-FMUSP/ABN)
- **Model Selection** — Switch between 4 LLM backends with live status indicator
- **Ground Truth** — Compare agent output against gold-standard diagnosis and action compliance
- **Trace Replay** — Save and replay past agent runs without a GPU
- **Export** — Download agent traces as JSON

## Quick Start

### Prerequisites

- Python 3.11+ with the `neuroagent` package installed (`uv sync --all-packages` from repo root)
- Node.js 20+ (for frontend development)

### 1. Start the API server

```bash
cd agent-platform
uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888
```

The server loads all 100 cases into memory on startup and serves both the API and the frontend.

### 2. Open the dashboard

Navigate to `http://localhost:8888` in your browser. The production frontend is served as static files from `web/dist/`.

### 3. (Optional) Run a live agent

Start a vLLM inference server first:

```bash
./scripts/serve_model.sh qwen3.5-9b    # or qwen3.5-27b-awq, medgemma-4b, medgemma-27b
```

Then select a case, choose your hospital and model, and click **Run Agent**.

## Remote Access (CERN VM)

If running on a headless VM (e.g., a CERN VM), use SSH tunnels to access the dashboard from your laptop.

### On the VM

```bash
# Production mode (recommended for remote — single port, no hot reload)
cd web && npm run build
uv run uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888

# Dev mode (hot reload — requires tunneling two ports)
cd web && npm run dev:remote                                            # frontend on :5173
uv run uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888       # backend on :8888
```

### On your laptop

**Inside the CERN network:**

```bash
# Production (single tunnel)
ssh -L 8888:localhost:8888 <user>@<vm>.cern.ch

# Dev mode (two tunnels)
ssh -L 5173:localhost:5173 -L 8888:localhost:8888 <user>@<vm>.cern.ch
```

**Outside the CERN network** (uses lxplus as jump host):

```bash
# Production (single tunnel)
ssh -L 8888:localhost:8888 -J <user>@lxplus.cern.ch <user>@<vm>.cern.ch

# Dev mode (two tunnels)
ssh -L 5173:localhost:5173 -L 8888:localhost:8888 -J <user>@lxplus.cern.ch <user>@<vm>.cern.ch
```

Then open http://localhost:8888 (production) or http://localhost:5173 (dev).

> **Tip:** Add an SSH config block to simplify this:
>
> ```ssh-config
> # ~/.ssh/config
> Host lxplus
>     HostName lxplus.cern.ch
>     User <your-cern-username>
>
> Host neuroagent-vm
>     HostName <vm>.cern.ch
>     User <your-cern-username>
>     ProxyJump lxplus              # remove this line when inside CERN
>     LocalForward 8888 localhost:8888
>     LocalForward 5173 localhost:5173
> ```
>
> Then just: `ssh neuroagent-vm` and open http://localhost:8888.

## Development

### Frontend dev server (with hot reload)

```bash
cd web
npm install
npm run dev          # starts on http://localhost:5173 (local)
npm run dev:remote   # starts on http://0.0.0.0:5173 (remote, binds all interfaces)
```

The Vite dev server proxies `/api` requests to `localhost:8888`, so the FastAPI backend must be running.

### Build for production

```bash
cd web
npm run build        # outputs to web/dist/
```

The FastAPI app automatically serves `web/dist/` as static files when the directory exists.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vite + React 18 + TypeScript |
| Styling | Tailwind CSS v4 + shadcn/ui primitives |
| State | Zustand (streaming) + TanStack Query (data fetching) |
| Markdown | react-markdown + remark-gfm |
| Backend | FastAPI + uvicorn |
| Streaming | Server-Sent Events (SSE) via async queue |
| Fonts | DM Sans + JetBrains Mono |

## Project Structure

```
web/
├── index.html                      # Entry point (loads DM Sans + JetBrains Mono)
├── vite.config.ts                  # Vite config with Tailwind plugin + API proxy
├── src/
│   ├── main.tsx                    # React root
│   ├── App.tsx                     # QueryClientProvider + dark mode sync
│   ├── index.css                   # Tailwind imports + theme variables + prose styles
│   ├── api/
│   │   ├── types.ts                # TypeScript interfaces (mirrors Pydantic models)
│   │   └── client.ts              # fetch wrappers + SSE stream consumer
│   ├── stores/
│   │   ├── appStore.ts             # UI state: selected case/hospital/model, dark mode
│   │   └── agentStore.ts           # Agent run state: events[], status, metrics
│   ├── hooks/
│   │   ├── useCases.ts             # TanStack Query hooks for cases, hospitals, models
│   │   ├── useAgentRun.ts          # SSE streaming hook with abort support
│   │   └── useReplay.ts            # Trace replay hook
│   ├── components/
│   │   ├── layout/                 # AppShell (3-panel), Header
│   │   ├── cases/                  # CaseBrowser (grouped list, search, filters)
│   │   ├── patient/                # PatientViewer (demographics, vitals, history, neuro exam)
│   │   ├── hospital/               # HospitalPicker (select dropdown)
│   │   ├── model/                  # ModelPicker (select + status dot)
│   │   ├── agent/                  # AgentTimeline, ThinkingBlock, ToolCallCard,
│   │   │                           # ReflectionBlock, AssessmentPanel, TokenCounter
│   │   ├── results/                # 7 specialized renderers + GenericResult fallback
│   │   └── ground-truth/           # GroundTruthPanel (action compliance checklist)
│   └── lib/
│       └── utils.ts                # cn() helper (clsx + tailwind-merge)
```

See [docs/api.md](docs/api.md) for the full API reference and [docs/components.md](docs/components.md) for the component architecture.
