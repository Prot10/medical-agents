# Architecture

## Overview

NeuroAgent is a tool-augmented LLM agent for neurological clinical decision support. It follows a ReAct (Reasoning + Acting) loop to investigate patient cases through sequential tool use.

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  System      │     │   LLM        │     │  Tool        │
│  Prompt      │────▶│  (vLLM)      │────▶│  Registry    │
│  + Hospital  │     │              │◀────│  (7 tools)   │
│    Rules     │     │  ReAct Loop  │     └──────────────┘
│  + Memory    │     │              │
└─────────────┘     └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  AgentTrace  │
                    │  (reasoning  │
                    │   record)    │
                    └──────────────┘
```

## Components

### Agent Orchestrator (`agent/orchestrator.py`)

The main ReAct loop:
1. Build system prompt (base + hospital rules + patient memory)
2. Send patient info to LLM with tool definitions
3. Loop: LLM calls tools → observe results → reflect → repeat
4. LLM responds without tool calls → done

Key config: `AgentConfig` dataclass with model, hospital, max_turns, ablation controls.

### Tools (`tools/`)

7 diagnostic tools, all implementing `BaseTool`:

| Tool | Description |
|---|---|
| `analyze_eeg` | Electroencephalography analysis |
| `analyze_brain_mri` | Brain MRI interpretation |
| `analyze_ecg` | Electrocardiogram analysis |
| `interpret_labs` | Laboratory results interpretation |
| `analyze_csf` | Cerebrospinal fluid analysis |
| `search_medical_literature` | Literature search |
| `check_drug_interactions` | Drug interaction checking |

In evaluation mode, all tools are backed by a `MockServer` that returns pre-generated outputs from `NeuroBenchCase` data.

### Hospital Rules (`rules/`)

Clinical protocols loaded from YAML files, one directory per hospital. Injected into the system prompt — not a tool. See [hospital-rules.md](hospital-rules.md).

### Patient Memory (`memory/`)

ChromaDB-backed vector store for longitudinal patient encounters. Stores and retrieves past encounters for the same patient across cases.

### Evaluation (`evaluation/`)

- `EvaluationRunner`: Runs agent on NeuroBench cases
- `MetricsCalculator`: Computes diagnostic accuracy, action recall, safety scores
- `NoiseInjector`: Ablation tool — injects noise into tool outputs
- `LLMJudge`: Uses a judge LLM to rate reasoning quality
- `ResultsAnalyzer`: Generates comparison tables

### LLM Client (`llm/client.py`)

Wraps the OpenAI SDK. Key features:
- Strips `<think>...</think>` tags from Qwen3.x thinking mode output
- Parses tool calls from OpenAI-style responses
- Tracks token usage

### Web Dashboard (`api/`)

FastAPI server + React frontend for interactive agent visualization. See [web-api.md](web-api.md).

- Real-time SSE streaming of agent execution (thinking, tool calls, results, assessment)
- 7 specialized diagnostic result renderers (labs, MRI, ECG, EEG, CSF, literature, drugs)
- Case browser, patient viewer, hospital/model selection, ground truth comparison
- Trace save/replay for demos without a GPU

## Package structure

```
medical-agents/               # uv workspace root
├── packages/
│   └── neuroagent-schemas/   # Shared Pydantic models (patient, case, evaluation)
├── agent-platform/           # Main agent package
│   ├── src/neuroagent/
│   │   ├── agent/            # Orchestrator, reasoning, reflection, planner
│   │   ├── api/              # FastAPI web API + SSE streaming
│   │   ├── llm/              # LLM client, prompts
│   │   ├── tools/            # 7 diagnostic tools + mock server + registry
│   │   ├── memory/           # ChromaDB patient memory
│   │   ├── rules/            # Rules engine, pathway checker
│   │   └── evaluation/       # Runner, metrics, noise, judge, analyzer
│   ├── config/
│   │   ├── agent_config.yaml
│   │   ├── system_prompts/   # orchestrator.txt, reflection.txt, report_generation.txt
│   │   └── hospital_rules/   # Per-hospital YAML directories
│   ├── scripts/              # CLI entry points
│   └── tests/
├── web/                      # React frontend dashboard
│   ├── src/components/       # UI components (agent timeline, patient viewer, etc.)
│   ├── docs/                 # API reference, component architecture
│   └── dist/                 # Production build (served by FastAPI)
└── dataset-generation/       # NeuroBench case generation (separate package)
```
