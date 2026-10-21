# Component Architecture

The frontend is organized into feature-based directories under `src/components/`. Each component is a single `.tsx` file with co-located types.

## Layout

```
┌───────────┬──────────────────────────────────────────────┐
│           │  Header: Breadcrumb │ Metrics │ Reward │ Run  │
│  Sidebar  ├───────────────────────┬──────────────────────┤
│  (nav +   │ Content panel         │ Episode Timeline     │
│  section  │ (Patient / Dataset /  │ ──────────────────── │
│  browser) │  Pathway Editor)      │ Policy Reward (opt.) │
└───────────┴───────────────────────┴──────────────────────┘
```

A collapsible, resizable sidebar (200–400px, or 64px collapsed) plus a main area split by `react-resizable-panels`. The sidebar's nav selects the active section (`cases` / `dataset` / `episodes` / `rules` / `architecture` / `profiles`); the content panel swaps accordingly, and the Architecture section takes over the full main area.

### Layout (`layout/`)

- **`AppShell`**: top-level layout with the sidebar, the header and the resizable content and timeline panels. When `appStore.scoreOpen` is set, the timeline panel is split vertically with the `ScorePanel`.
- **`Sidebar`**: nav items, the content of each section, and a collapsible footer. The footer holds the profile picker, the profile's model with its serving state and Load / Stop controls (it consumes the `/models/{key}/load` SSE stream), the loop and turn budget, and the dark-mode toggle.
- **`Header`**: section breadcrumb and selected case ID, simulated cost, `TokenCounter`, export of the episode JSON, the Reward toggle and the Run/Stop controls.
- **`SidebarResizeHandle`**: drag handle that keeps the sidebar between 200 and 400px.

## Sidebar Section Panels

- **`CaseBrowser`** (`cases/`): cases grouped by condition, with text search (case ID / chief complaint) and a difficulty filter. Selection is wired to `appStore.selectedCaseId`.
- **`DatasetOverview`** (`dataset/`): compact dataset summary (total, average age, difficulty and condition bars). Its rows toggle `appStore.datasetFilters`.
- **`EpisodeBrowser`** (`episodes/`): saved episodes, newest first, filtered by profile. Each one can be replayed step by step or at once, or deleted.
- **`HospitalRulesBrowser`** (`hospital/`): hospital picker and searchable pathway list. Pathways are reference material and harness runs do not read them.
- **`ProfilesPanel`** (`profiles/`): the checked profiles with their model status, loop, turn, cost and retry budgets. Clicking one selects it for the next run.

## Content Panel

- **`PatientViewer`** (`patient/`): the selected case in tabs. Overview covers demographics, vitals (`hr` / `temp` / `rr` / BP / SpO2), the chief complaint and the HPI; the other tabs are History, Neuro Exam, Diagnostics (stored tool outputs) and Ground Truth.
- **`GroundTruthPanel`** (`ground-truth/`): the case policy, with its review status, accepted diagnoses and ICD codes, differential, action criteria, avoided actions, sequence constraints, stop rule, assessment requirements, key evidence and red herrings. When an episode is on screen, each criterion and avoided action is checked against its tool actions using the same pattern matching as the reward (`lib/policy.ts`).
- **`DatasetDashboard`** (`dataset/`): stat cards and four charts (`ConditionChart`, `DifficultyDonut`, `AgeHistogram`, `CaseHeatmap`).
- **`PathwayEditorPanel`** (`hospital/`): CRUD editor for hospital pathways.
- **`ArchitectureExplorer`** (`architecture/`): interactive system map of the repository, filterable by layer.

## Agent Panel (`agent/`)

- **`AgentTimeline`**: vertical timeline that scrolls itself, built from the episode events. It contains:
  - the run header (`run.started`);
  - ReAct rationales (`plugin.event`);
  - a tool card for each accepted `action.proposed`, paired with its `observation.received`;
  - rejected actions (`action.rejected`);
  - the assessment;
  - a failure card (`run.failed`).

  In the direct loop, observations given before any action appear as turn-0 cards.
- **`ToolCallCard`**: a collapsible card for each tool call, with its arguments and the result renderer. Badges mark results that were given upfront, rejected, or that came from the fallback library, and show the simulated cost and any error message.
- **`ThinkingBlock`**: a labelled markdown block, used for ReAct rationales.
- **`AssessmentPanel`**: the structured `submit_assessment`, with primary diagnosis, ICD-10 code, urgency, confidence, differential and recommendations.
- **`ScorePanel`**: the policy reward. It shows the scalar, each component, the caps applied and the invalid actions. On a draft policy it carries a warning that the score is not reportable.
- **`TokenCounter`**: compact token count and elapsed time. The time ticks live while a run is in flight.

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
UI-level state:
- selection: `selectedCaseId`, `selectedProfileId` (default `policy-qwen3.5-9b`);
- display: `darkMode`, `showGroundTruth`;
- sidebar: `sidebarCollapsed`, `sidebarWidth`, `activeSection`;
- `datasetFilters`;
- rules editor: `rulesHospitalId`, `selectedPathwayIndex`, `isCreatingPathway`;
- `scoreOpen`.

### `agentStore` (Zustand)
State of the episode on screen, whether live or replayed:
- `status`: `idle` | `running` | `complete` | `failed` | `cancelled` | `error`
- `events`: append-only `EpisodeEvent[]`, in the order the episode store recorded them
- `episodeId` and `reward`: set by the `stream.result` frame, or by a replay together with `/episodes/{id}/reward`
- `totalTokens`, `totalCost`, `startedAt`, `elapsedTime`: derived from the events
- `abortController`: the in-flight stream, which any component can cancel

### `modelLoadingStore` (Zustand)
Model-load progress from the `/models/{key}/load` SSE stream: `phase`, `progress`, `elapsed`, `expectedSeconds`, `sizeGb`, `message`.

### TanStack Query (`hooks/`)
- Cases, case detail, hospitals, profiles (`staleTime: Infinity`)
- Hospital rules (`staleTime: 30s`)
- Models (`staleTime: 10s`)
- Episodes (`staleTime: 5s`; invalidated when a run finishes)

## Data Flow

```
User clicks "Run Agent"
  → useAgentRun.run(caseId, profileId)
    → agentStore.startRun()
    → streamRun() POSTs /api/v1/runs/stream
      → backend: the harness loop runs in a worker thread; every episode_store.append
        is handed to the event loop and written as one SSE frame
    → consumeSSEStream() parses "data: {...}\n\n" frames
      → agentStore.appendFrame(frame): episode events are appended, and the timeline
        re-renders and scrolls
      → stream.result: episodeId and reward are set; the episode is already saved in data/episodes/
    → the episodes query is invalidated, so the new episode appears in the Episodes section
User clicks "Replay" in Episodes
  → GET /episodes/{id} and /episodes/{id}/reward
  → useReplay feeds the events into agentStore every 450 ms (or all at once with "Skip to End")
```
