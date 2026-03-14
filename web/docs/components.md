# Component Architecture

The frontend is organized into feature-based directories under `src/components/`. Each component is a single `.tsx` file with co-located types.

## Layout

```
┌──────────────────────────────────────────────────────────┐
│  Header: Logo │ ModelPicker │ HospitalPicker │ ThemeToggle│
├──────────┬───────────────────────┬───────────────────────┤
│ Case     │ Patient Viewer        │ Agent Timeline        │
│ Browser  │                       │                       │
│ (250px)  │ (flex)                │ (480px)               │
└──────────┴───────────────────────┴───────────────────────┘
```

### `AppShell`
3-panel layout with fixed-width sidebars and a flexible center. All panels scroll independently.

### `Header`
Contains the logo mark, model picker, hospital picker (separated by dividers), and a dark/light theme toggle.

## Left Panel — Case Browser

### `CaseBrowser`
Lists 100 cases grouped by neurological condition (10 groups). Features:
- **Search** — filters by case ID and chief complaint
- **Difficulty chips** — S (straightforward), M (moderate), P (diagnostic puzzle) with color coding
- **Sticky group headers** — condition name stays visible while scrolling
- **Selection state** — connected to `appStore.selectedCaseId`; selecting a case resets the agent timeline

## Center Panel — Patient Viewer

### `PatientViewer`
Full clinical data display for the selected case. Contains inline sub-components:

- **Demographics bar** — age, sex, handedness, ethnicity, BMI, encounter type, difficulty badges
- **VitalsRow** — 6 metric cards (BP, HR, Temp, RR, SpO2) with icons and abnormal-value highlighting (red border when outside reference range)
- **Chief Complaint** — prominent text
- **HPI** — full narrative
- **Tabbed sections**:
  - *History* — PMH list, medications table, allergy badges, family history, social history
  - *Neurological Exam* — collapsible sections for each of 8 exam domains
- **Ground Truth toggle** — expands `GroundTruthPanel` below

### `GroundTruthPanel`
Collapsible panel showing:
- Primary diagnosis + ICD code
- Differential diagnoses with likelihood
- **Action compliance checklist** — cross-references `ground_truth.optimal_actions` against the agent's actual tool calls (green check / gray X)
- Critical actions and key reasoning points

## Right Panel — Agent Timeline

The core feature. A vertical scrollable timeline that auto-scrolls during streaming.

### `AgentTimeline`
Container component managing:
- **Run controls** — Run Agent / Stop buttons, replay dropdown, export button
- **Event rendering** — converts raw `AgentEvent[]` from the store into render items by pairing `tool_call` + `tool_result` events
- **Live indicators** — pulsing dot with "Agent is thinking..." during runs

### `ThinkingBlock`
Indigo-accented card for agent reasoning. Left gradient accent bar. Content rendered with react-markdown + remark-gfm. Shows turn number.

### `ToolCallCard`
VSCode/Cursor-inspired collapsible card:
- **Collapsed** — chevron + tool icon (color-coded per tool) + tool name + args preview + status icon (spinning/check/X)
- **Expanded** — arguments JSON + specialized result renderer

7 tool-to-icon mappings:

| Tool | Icon | Color |
|------|------|-------|
| `analyze_brain_mri` | Brain | Violet |
| `analyze_eeg` | Activity | Blue |
| `analyze_ecg` | Heart | Rose |
| `interpret_labs` | FlaskConical | Emerald |
| `analyze_csf` | Droplets | Cyan |
| `search_medical_literature` | BookOpen | Amber |
| `check_drug_interactions` | Pill | Orange |

### `ReflectionBlock`
Minimal divider with gradient lines and a "Reflect" label in the reflection accent color.

### `AssessmentPanel`
Green-accented card for the final structured assessment. Gradient header with shield icon. Full markdown rendering of the agent's diagnosis, differentials, evidence, recommendations, and red flags.

### `TokenCounter`
Compact metrics display: token count (in thousands) and elapsed time. Monospace font.

## Tool Result Renderers (`results/`)

Each renderer is designed for a specific diagnostic tool output format:

| Component | Tool | Key Features |
|-----------|------|-------------|
| `LabResultsTable` | `interpret_labs` | Grouped by panel (CBC, BMP, etc.), auto-expands panels with abnormal values, red highlighting for out-of-range results |
| `MRIFindings` | `analyze_brain_mri` | Finding cards with signal characteristics grid (T1/T2/FLAIR/DWI), imaging differential badges |
| `ECGReport` | `analyze_ecg` | Top-line metric badges (rhythm, rate, axis), intervals grid, severity-colored findings |
| `EEGReport` | `analyze_eeg` | Classification header, background description, finding cards (type, location, frequency, morphology) |
| `CSFResults` | `analyze_csf` | Key-value grid (appearance, pressure, protein, glucose), cell count breakdown, special tests |
| `LiteratureResults` | `search_medical_literature` | Paper cards with title, source, summary; query echo; overall summary |
| `DrugInteractions` | `check_drug_interactions` | Severity-colored interaction cards (major/moderate/minor), contraindication list, green alternative badges |
| `GenericResult` | (fallback) | Auto-renders key metrics, findings list, impression text; raw JSON toggle |

### `ToolResultRenderer`
Router component that selects the appropriate specialized renderer based on `toolName`, falling back to `GenericResult`.

## State Management

### `appStore` (Zustand)
UI-level state persisted across component re-renders:
- `selectedCaseId` — which case is active
- `selectedHospital` — hospital rule set (`us_mayo` default)
- `selectedModel` — LLM backend (`qwen3.5-9b` default)
- `darkMode` — theme toggle (default: true)
- `showGroundTruth` — ground truth panel visibility

### `agentStore` (Zustand)
Agent execution state, updated at high frequency during SSE streaming:
- `status` — `idle` | `running` | `complete` | `error`
- `events` — append-only array of `AgentEvent` objects
- `totalTokens` / `elapsedTime` — accumulated metrics
- `errorMessage` — last error

### TanStack Query
Used for static data that doesn't change during a session:
- Cases list (`staleTime: Infinity`)
- Case detail (`staleTime: Infinity`, enabled only when a case is selected)
- Hospitals (`staleTime: Infinity`)
- Models (`staleTime: 10s` — re-fetches to detect vLLM status changes)
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
        → AgentTimeline re-renders with new events
        → buildRenderItems() pairs tool_call + tool_result
        → auto-scroll to bottom
    → on run_complete: status → "complete"
    → trace auto-saved to data/traces/ on backend
```
