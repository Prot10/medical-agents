# NeuroAgent Web Dashboard

Dashboard for the clinical-policy harness. Pick a case and a checked experiment profile, watch the episode stream in live, replay saved episodes, and compare them with the case policy and the policy reward.

## Features

- **Case Browser**: the 600 NeuroBench cases across 20 conditions, with search and a difficulty filter.
- **Patient Viewer**: demographics, vitals with abnormal values highlighted, history, neurological exam, the stored diagnostic outputs and the case policy.
- **Live episode timeline**: every event of `POST /api/v1/runs/stream` as it happens: tool calls with their results and costs, rejected actions, ReAct rationales and the structured final assessment.
- **Profiles**: the nine checked profiles (3 models × policy / direct / ReAct loops), with the model's serving state and Load / Stop controls.
- **Case policy**: accepted diagnoses, action criteria, avoided actions, sequence, stop rule and assessment requirements, each criterion checked against the episode on screen.
- **Policy reward**: the reward components and any safety caps applied. On a draft policy it is shown as an engineering score that is not reportable.
- **Episode replay**: saved episodes from `data/episodes/`, replayed step by step or at once, with no GPU needed.
- **Hospital Rules**: browse and edit the hospital pathways. Harness runs do not read them.
- **Architecture**: an interactive map of the repository.
- **Export**: download the episode on screen as JSON.

## Quick Start

### Prerequisites

- Python 3.11+ with the workspace installed (`uv sync --all-packages` from the repo root)
- Node.js 20+

### 1. Build the frontend and start the API

```bash
cd web && npm ci && npm run build && cd ..
uv run uvicorn neuroagent.api.app:app --host 127.0.0.1 --port 8888
```

When `web/dist/` exists, the API serves the dashboard at `http://localhost:8888`.

### 2. (Optional) Serve a model and run a live episode

```bash
HF_HOME=/dev/shm/hf agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b
```

Choose a profile whose model is ready, select a case and click **Run Agent**. You can also start the profile's model from the sidebar, which uses `POST /models/{key}/load`.

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
| Frontend | Vite + React 19 + TypeScript |
| Styling | Tailwind CSS v4 |
| State | Zustand (UI and episode state) + TanStack Query (server data) |
| Charts | Recharts |
| Backend | FastAPI + uvicorn |
| Streaming | Server-Sent Events from a worker thread through an asyncio queue |

## Project Structure

```
web/src/
├── api/            # types.ts (mirrors the Pydantic episode/case models), client.ts (fetch + SSE)
├── stores/         # appStore (selection, sections, panels), agentStore (episode events, reward), modelLoadingStore
├── hooks/          # useCases (cases, profiles, models, rules), useAgentRun (live run), useReplay (episodes)
├── lib/            # conditions (labels, colours), policy (criterion matching, profile helpers), utils
└── components/
    ├── layout/       # AppShell, Sidebar (profile picker), Header (run, reward, export)
    ├── cases/        # CaseBrowser
    ├── patient/      # PatientViewer
    ├── ground-truth/ # GroundTruthPanel (case policy, checked against the episode)
    ├── agent/        # AgentTimeline, ToolCallCard, ThinkingBlock, AssessmentPanel, ScorePanel, TokenCounter
    ├── episodes/     # EpisodeBrowser
    ├── profiles/     # ProfilesPanel
    ├── results/      # per-tool result renderers + GenericResult
    ├── dataset/      # DatasetOverview, DatasetDashboard, charts
    ├── hospital/     # HospitalRulesBrowser, PathwayEditorPanel
    ├── architecture/ # ArchitectureExplorer
    ├── model/        # ModelLoadingToast
    └── ui/           # Badge, Card, DifficultyStars, SectionLabel, QueryError
```

See [docs/api.md](docs/api.md) for the endpoints the dashboard uses and [docs/components.md](docs/components.md) for the component architecture.
