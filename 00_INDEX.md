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

**For references**: 03_bibliography.md
