# NeuroAgent — Project Documentation Index

## Project Overview

**NeuroAgent** is a tool-augmented, memory-enabled LLM agent for neurological clinical decision support. The agent reasons across multimodal data (EEG, MRI, ECG, labs, clinical reports) through specialized tool-calling, maintains longitudinal patient memory, and follows hospital-specific protocols.

**Key design decision**: Tool outputs are mocked using pre-generated, clinically realistic results. This isolates the evaluation of agentic reasoning from the accuracy of individual modality models, and enables controlled robustness testing.

**Primary publication target**: Nature Machine Intelligence

---

## Folder Structure

```
medical-agents/
├── 00_INDEX.md                    ← You are here
│
├── 01_literature_review.md        ← State of the art in medical AI agents,
│                                     LLMs, multimodal AI, and neurology datasets
│
├── 02_system_architecture.md      ← NeuroAgent architecture: orchestrator,
│                                     tools, memory, rules, mock evaluation
│
├── 03_bibliography.md             ← 64 references organized thematically
│
├── agent-platform/docs/           ← Technical documentation
│   ├── architecture.md            ← Agent architecture + package structure
│   ├── hospital-rules.md          ← Hospital rule sets and pathways
│   ├── models.md                  ← Supported LLM models and configs
│   ├── quickstart.md              ← Setup and first run
│   └── web-api.md                 ← Web dashboard API and SSE streaming
│
├── web/                           ← Interactive web dashboard
│   ├── README.md                  ← Quick start, tech stack, project structure
│   └── docs/
│       ├── api.md                 ← Full REST + SSE API reference
│       └── components.md          ← Frontend component architecture
│
└── nmi-paper-plan/                ← NMI paper strategy and implementation
    ├── 01_nmi_paper_plan.md       ← What goes into the NMI paper, structure,
    │                                 timeline, claims, venue strategy
    │
    ├── 02_detailed_scenario_walkthrough.md
    │                              ← 4 complete clinical scenarios showing
    │                                 step-by-step agent behavior (show to
    │                                 supervisor and doctors)
    │
    ├── 03_supervisor_summary.md   ← Non-technical summary for supervisor
    │                                 and clinical collaborators
    │
    ├── 04_implementation_dataset_generation.md
    │                              ← Implementation TODO for the NeuroBench
    │                                 dataset generation pipeline (for Claude Code)
    │
    └── 05_implementation_agent_platform.md
                                   ← Implementation TODO for the NeuroAgent
                                      platform (for Claude Code)
```

---

## Reading Order

**For understanding the project**: 01 → 02 → nmi-paper-plan/01

**For presenting to supervisor**: nmi-paper-plan/03_supervisor_summary.md

**For presenting to doctors**: nmi-paper-plan/02_detailed_scenario_walkthrough.md

**For starting implementation**: nmi-paper-plan/04 and 05 (in parallel)

**For the web dashboard**: web/README.md → web/docs/api.md → web/docs/components.md

**For references**: 03_bibliography.md
