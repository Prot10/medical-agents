# Component Architecture

The frontend is organized into feature-based directories under `src/components/`. Each component is a single `.tsx` file with co-located types.

## Layout

```
┌───────────┬──────────────────────────────────────────────┐
│           │  Header: Breadcrumb │ Metrics │ Evaluate │ Run │
│  Sidebar  ├───────────────────────┬──────────────────────┤
│  (nav +   │ Content panel         │ Agent Timeline       │
│  section  │ (Patient / Dataset /  │ ──────────────────── │
│  browser) │  Pathway Editor)      │ Oracle (optional)    │
└───────────┴───────────────────────┴──────────────────────┘
```

A collapsible, resizable sidebar (200–400px, or 64px collapsed) plus a main area split by `react-resizable-panels`. The sidebar's nav selects the active section (`cases` / `dataset` / `traces` / `rules` / `architecture` / `settings`); the content panel swaps accordingly, and the Architecture section takes over the full main area.

### Layout (`layout/`)

- **`AppShell`** — top-level layout: sidebar + header + resizable content/agent panels; optionally splits the agent panel vertically with the `OraclePanel`.
- **`Sidebar`** — nav items, per-section browser content, and a collapsible footer with agent-model / evaluator-model / hospital pickers, model load/stop controls (consumes the `/models/{key}/load` SSE stream), and the dark-mode toggle.
- **`Header`** — section breadcrumb + selected case ID, `TokenCounter` metrics, export-trace button, Evaluate button (triggers the Oracle), and Run/Stop controls.
- **`SidebarResizeHandle`** — drag handle that clamps sidebar width between 200 and 400px.

## Sidebar Section Panels

Rendered inside the sidebar based on the active nav section:

- **`CaseBrowser`** (`cases/`) — 600 cases grouped by condition, with text search (case ID / chief complaint), difficulty filter, and selection wired to `appStore.selectedCaseId`.
- **`DatasetOverview`** (`dataset/`) — compact dataset summary (total, avg age, difficulty and condition bars) whose rows toggle `appStore.datasetFilters`.
- **`TraceBrowser`** (`traces/`) — saved traces with search and difficulty filter; replay (streamed or instant), delete, and per-trace metadata (model, hospital, cost).
- **`HospitalRulesBrowser`** (`hospital/`) — hospital picker + searchable pathway list; selects a pathway for the editor or starts creation of a new one.
- **`SettingsPanel`** (`settings/`) — GitHub Copilot connection via OAuth device flow (pairing code, polling, logout).

## Content Panel

- **`PatientViewer`** (`patient/`) — full clinical data for the selected case in tabs: Overview (demographics, vitals, chief complaint, HPI), History, Neuro Exam, Diagnostics (pre-generated tool outputs), and Ground Truth.
- **`GroundTruthPanel`** (`ground-truth/`) — primary diagnosis + ICD code, differentials, and an action-compliance checklist cross-referencing `ground_truth.optimal_actions` against the agent's actual tool calls.
- **`DatasetDashboard`** (`dataset/`) — dataset analytics: stat cards (cases, avg age, sex split, conditions), dataset switcher (`/datasets/{v}/activate`), and four charts.
  - **`charts/ConditionChart`** — case counts per condition (bar).
  - **`charts/DifficultyDonut`** — difficulty breakdown (donut).
  - **`charts/AgeHistogram`** — age distribution in 10-year bins.
  - **`charts/CaseHeatmap`** — condition × difficulty matrix.
- **`PathwayEditorPanel`** (`hospital/`) — full CRUD editor for hospital pathways: name/description/triggers, step list (action, timing, mandatory, condition), contraindicated actions; saves via the hospitals rules POST/PUT/DELETE endpoints.
- **`ArchitectureExplorer`** (`architecture/`) — interactive system map of the whole project (nodes with paths, files, and links) filterable by layer (Runtime, Reasoning, Tools, Data, Evaluation, Frontend, Review, Research, Fine-tuning, Deployment). Replaces the whole main area.

## Agent Panel (`agent/`)

- **`AgentTimeline`** — vertical auto-scrolling timeline; pairs `tool_call` + `tool_result` events into render items, groups turns, and renders live streaming deltas via `StreamingContent`.
- **`StreamingContent`** — collapsible reasoning block that renders token deltas with Streamdown while streaming and react-markdown once complete.
- **`ThinkingBlock`** — card for a completed reasoning turn (markdown via react-markdown + remark-gfm).
- **`ToolCallCard`** — collapsible card per tool call: icon + args preview + status while collapsed, arguments JSON + specialized result renderer when expanded. Icon/color mappings for all 12 tools.
- **`ReflectionBlock`** — minimal divider marking an injected reflection prompt.
- **`AssessmentPanel`** — green-accented card for the final structured assessment, fully markdown-rendered.
- **`OraclePanel`** — evaluation view, opened by the header's Evaluate button (`appStore.oracleTrigger`). Streams `/agent/evaluate`: rule-based metrics grid (accuracy, precision/recall, safety, efficiency) then the LLM judge's streaming output and scores.
- **`TokenCounter`** — compact token count + elapsed time, monospace.

## Tool Result Renderers (`results/`)

- **`ToolResultRenderer`** — router that picks the specialized renderer by `toolName`, falling back to `GenericResult`.

| Component | Tool | Key Features |
|-----------|------|-------------|
| `LabResultsTable` | `interpret_labs` | Grouped by panel, auto-expands abnormal panels, out-of-range highlighting |
| `MRIFindings` | `analyze_brain_mri` | Finding cards with signal characteristics grid (T1/T2/FLAIR/DWI) |
| `ECGReport` | `analyze_ecg` | Rhythm/rate/axis badges, intervals grid, severity-colored findings |
| `EEGReport` | `analyze_eeg` | Classification header, background description, finding cards |
| `CSFResults` | `analyze_csf` | Key-value grid, cell count breakdown, special tests |
| `LiteratureResults` | `search_medical_literature` | Paper cards, query echo, overall summary |
| `DrugInteractions` | `check_drug_interactions` | Severity-colored interaction cards, alternatives |
| `GenericResult` | (fallback) | Key metrics, findings, impression, raw JSON toggle — covers the `order_*` tools |

## Model (`model/`)

- **`ModelLoadingToast`** — floating toast for model loads: phase label, smoothly interpolated progress bar and elapsed clock, auto-dismiss on ready; driven by `modelLoadingStore`.

## UI Primitives (`ui/`)

- **`Badge`** — pill label with variants (default/outline/success/warning/destructive/info).
- **`Card`** — rounded bordered container with optional left accent and hover state.
- **`DifficultyStars`** — 1–3 colored stars for straightforward/moderate/diagnostic_puzzle.
- **`SectionLabel`** — small uppercase section heading with optional icon.

## State Management

### `appStore` (Zustand)
UI-level state: `selectedCaseId`, `selectedHospital`, `selectedModel`, `selectedEvaluatorModel`, `darkMode`, `showGroundTruth`, sidebar state (`sidebarCollapsed`, `sidebarWidth`, `activeSection`), `datasetFilters`, rules-editor state (`rulesHospitalId`, `selectedPathwayIndex`, `isCreatingPathway`), and Oracle state (`oracleOpen`, `oracleTrigger`).

### `agentStore` (Zustand)
Agent execution state, updated at high frequency during SSE streaming:
- `status` — `idle` | `running` | `complete` | `error`
- `events` — append-only array of `AgentEvent` objects
- `streamingContent` / `streamingThinkContent` / `streamingTurnNumber` — buffers accumulated from `content_delta` / `think_delta` events
- `totalTokens` / `elapsedTime` / `totalCost` — accumulated metrics
- `errorMessage` — last error

### `modelLoadingStore` (Zustand)
Model-load progress from the `/models/{key}/load` SSE stream: `phase`, `progress`, `elapsed`, `expectedSeconds`, `sizeGb`, `message`.

### TanStack Query (`hooks/`)
Server data via `useCases.ts` and `useReplay.ts`:
- Cases list / case detail (`staleTime: Infinity`)
- Hospitals (`staleTime: Infinity`), hospital rules (`staleTime: 30s`)
- Datasets (`staleTime: 30s`) + `useActivateDataset` mutation
- Models (`staleTime: 10s` — merges local models with Copilot models when authenticated)
- Copilot status (`staleTime: 5s`)
- Traces (`staleTime: 5s`)

## Data Flow

```
User clicks "Run Agent"
  → useAgentRun.run(caseId, hospital, model)
    → agentStore.startRun() — resets state
    → fetch POST /api/v1/agent/run (SSE stream)
      → Backend: orchestrator.run_streaming() yields events
      → async queue passes events to SSE response
    → consumeSSEStream() parses "data: {...}\n\n" lines
      → agentStore.appendEvent(event) for each
        → think_delta / content_delta accumulate into streaming buffers
        → AgentTimeline re-renders; buildRenderItems() pairs tool_call + tool_result
        → auto-scroll to bottom
    → on run_complete: status → "complete"
    → trace auto-saved to data/traces/ on backend
User clicks "Evaluate"
  → appStore.triggerOracle() opens OraclePanel
    → streamEvaluation() POSTs the run's events to /api/v1/agent/evaluate
    → metrics event renders the score grid; judge_delta streams the LLM judge
```
