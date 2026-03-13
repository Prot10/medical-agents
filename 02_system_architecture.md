# NeuroAgent: System Architecture and Framework Design

## 1. System Overview

**NeuroAgent** is a tool-augmented, memory-enabled, multi-agent system for neurological clinical decision support. It is designed to assist neurologists throughout patient care by analyzing multimodal neurological data (EEG, MRI, fMRI, clinical reports), maintaining longitudinal patient memory, adhering to hospital-specific protocols, and providing diagnostic reasoning with actionable recommendations.

### 1.1 Design Principles

1. **Modularity** — Each analytical capability (EEG analysis, MRI interpretation, etc.) is encapsulated as a standalone tool, allowing independent development, testing, and improvement
2. **Transparency** — Every decision is accompanied by a chain-of-thought explanation, citing the evidence and tools used
3. **Safety-first** — The system suggests actions rather than taking them autonomously; high-risk decisions always require human confirmation
4. **Open-source** — Built entirely on open-source LLMs and frameworks to ensure reproducibility and academic scrutiny
5. **Extensibility** — New tools, data modalities, and hospital rules can be added without redesigning the core agent

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         NEUROAGENT SYSTEM                               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    ORCHESTRATOR AGENT                            │   │
│  │            (Central LLM: Qwen3-32B / MedGemma 27B)             │   │
│  │                                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────────┐  │   │
│  │  │ Reasoning │  │ Planning │  │ Reflection│  │ Tool Dispatch│  │   │
│  │  │  Engine   │  │  Module  │  │  Module   │  │    Router    │  │   │
│  │  └──────────┘  └──────────┘  └───────────┘  └──────────────┘  │   │
│  └──────────────────────────┬──────────────────────────────────────┘   │
│                             │                                           │
│  ┌──────────────────────────┼──────────────────────────────────────┐   │
│  │                    TOOL LAYER                                    │   │
│  │                                                                  │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐ │   │
│  │  │ EEG        │  │ Brain MRI  │  │ fMRI       │  │ Clinical │ │   │
│  │  │ Analyzer   │  │ Analyzer   │  │ Analyzer   │  │ Report   │ │   │
│  │  │            │  │            │  │            │  │ Parser   │ │   │
│  │  │ (EEG-FM)   │  │ (MedGemma  │  │ (fMRI-FM)  │  │ (NER +   │ │   │
│  │  │            │  │  + 3D ViT) │  │            │  │  LLM)    │ │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └──────────┘ │   │
│  │                                                                  │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐ │   │
│  │  │ ECG        │  │ Lab Results│  │ Medical    │  │ Drug     │ │   │
│  │  │ Analyzer   │  │ Interpreter│  │ Literature │  │ Interaction│ │   │
│  │  │            │  │            │  │ Search     │  │ Checker  │ │   │
│  │  │ (ECGChat)  │  │ (Rule-     │  │            │  │          │ │   │
│  │  │            │  │  based+LLM)│  │ (PubMed    │  │ (DrugBank│ │   │
│  │  │            │  │            │  │  + Scholar) │  │  API)    │ │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └──────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    MEMORY & KNOWLEDGE LAYER                      │   │
│  │                                                                  │   │
│  │  ┌──────────────────┐  ┌──────────────┐  ┌──────────────────┐  │   │
│  │  │ Patient Memory    │  │ Hospital     │  │ Medical          │  │   │
│  │  │ Store             │  │ Rules Engine │  │ Knowledge Graph  │  │   │
│  │  │                   │  │              │  │                  │  │   │
│  │  │ • Demographics    │  │ • Protocols  │  │ • Disease        │  │   │
│  │  │ • Visit history   │  │ • Guidelines │  │   ontologies     │  │   │
│  │  │ • Past results    │  │ • Formulary  │  │ • Symptom-disease│  │   │
│  │  │ • Medications     │  │ • Workflows  │  │   mappings       │  │   │
│  │  │ • Allergies       │  │ • Constraints│  │ • SNOMED-CT      │  │   │
│  │  │ • Family history  │  │              │  │ • ICD-10/11      │  │   │
│  │  └──────────────────┘  └──────────────┘  └──────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    INTERACTION LAYER                              │   │
│  │                                                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐    │   │
│  │  │ Doctor       │  │ Patient      │  │ Report             │    │   │
│  │  │ Interface    │  │ Interview    │  │ Generator          │    │   │
│  │  │              │  │ Module       │  │                    │    │   │
│  │  │ • Dashboard  │  │ • Question   │  │ • Diagnostic       │    │   │
│  │  │ • Alerts     │  │   generation │  │   summaries        │    │   │
│  │  │ • Overrides  │  │ • Symptom    │  │ • Discharge notes  │    │   │
│  │  │              │  │   elicitation│  │ • Referral letters  │    │   │
│  │  └──────────────┘  └──────────────┘  └────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Core Components — Detailed Design

### 3.1 Orchestrator Agent

The central reasoning agent that coordinates all system activities.

**Base Model Options** (to be compared experimentally):
- **Primary**: Qwen3-32B fine-tuned with DoRA/rsLoRA on neurology cases + RL with clinical accuracy reward
- **Comparison 1**: MedGemma 27B (text variant) — pre-trained medical knowledge
- **Comparison 2**: OpenBioLLM-70B — strongest open-source medical baseline
- **Ablation**: Qwen3-8B — smaller model for efficiency analysis

**Agent Framework**: Built on a ReAct-style (Reasoning + Acting) loop:

```
OBSERVE → patient data, tool results, memory context
  ↓
THINK  → chain-of-thought reasoning about the clinical picture
  ↓
ACT    → call a tool, ask a question, generate a report, or request more data
  ↓
REFLECT → evaluate the tool result, update differential diagnosis
  ↓
REPEAT until → diagnosis confidence threshold met OR human decision requested
```

**Key Implementation Details**:
- **Function calling / tool use**: Structured output format where the LLM generates tool calls with typed parameters (JSON schema)
- **Context window management**: Sliding window over patient history + always-present summary; critical findings pinned in context
- **Confidence estimation**: The agent outputs confidence levels for diagnoses and explicitly flags uncertainty
- **Escalation logic**: If confidence is below threshold or the case involves high-risk decisions, the agent explicitly defers to the human doctor

### 3.2 Tool Layer

Each tool exposes a standardized interface to the orchestrator. In the current research prototype, tools are backed by a **MockServer** that returns pre-generated, clinically realistic outputs from NeuroBench cases. The architecture is designed so real specialized models can be plugged in later without changing the agent framework.

The system includes 8 tools:

| Tool | Purpose | Key Output Fields |
|------|---------|-------------------|
| `analyze_eeg` | Analyze EEG for epileptiform discharges, slowing, artifacts | Classification, findings (type, location, morphology), confidence, impression |
| `analyze_brain_mri` | Analyze structural MRI for lesions, atrophy, tumors | Findings (type, location, signal characteristics), volumetrics, differential |
| `analyze_ecg` | Analyze ECG for arrhythmias (syncope/stroke workup) | Rhythm, rate, intervals, findings, interpretation |
| `interpret_labs` | Interpret blood work, metabolic panels | Panel results with reference ranges, abnormal flags, interpretation |
| `analyze_csf` | Interpret cerebrospinal fluid analysis | Cell count, protein, glucose, special tests (HSV PCR, antibodies) |
| `search_medical_literature` | Query PubMed and clinical guidelines | Relevant papers with findings and evidence levels |
| `check_drug_interactions` | Check medication interactions and formulary | Interactions, contraindications, warnings, alternatives |
| `check_hospital_rules` | Verify compliance with institutional protocols | Protocol status, required next steps, documentation requirements |

All tool interfaces are defined as Pydantic models in the shared `neuroagent-schemas` package (see implementation docs for full schemas). This ensures the dataset generation pipeline and the agent platform always agree on data formats.

---

### 3.3 Memory and Knowledge Layer

#### 3.3.1 Patient Memory Store

A persistent, per-patient memory system that maintains longitudinal context across encounters.

**Storage Architecture**:
```
PatientMemory {
  patient_id: string
  demographics: { age, sex, relevant_history }

  encounters: [
    {
      date: datetime
      type: "outpatient" | "inpatient" | "emergency"
      chief_complaint: string
      findings: [structured findings from tools]
      diagnosis: string
      treatment_plan: string
      pending_tests: [string]
      follow_up: string
    }
  ]

  active_diagnoses: [{ icd_code, description, date_diagnosed, status }]
  medications: [{ drug, dose, frequency, start_date, prescriber }]
  allergies: [string]
  family_history: [string]

  longitudinal_trends: {
    eeg_trend: [summary of EEG changes over time]
    mri_trend: [summary of brain volume changes, lesion evolution]
    cognitive_trend: [MMSE/MoCA scores over time]
  }

  agent_notes: [
    { date, note: "differential narrowed after EEG showed..." }
  ]
}
```

**Implementation Options**:
- **Vector database** (e.g., ChromaDB, FAISS) for semantic retrieval of relevant past encounters
- **Structured database** (SQLite/PostgreSQL) for precise querying of medications, diagnoses, lab values
- **Hybrid approach**: Structured storage + vector index over clinical notes for flexible retrieval

**Memory Retrieval Strategy**:
When a new encounter begins, the system retrieves:
1. Always: demographics, active diagnoses, current medications, allergies
2. Semantic search: past encounters most relevant to the current chief complaint
3. Temporal: most recent 3 encounters regardless of relevance
4. Trend data: longitudinal summaries for relevant modalities

#### 3.3.2 Hospital Rules Engine

A configurable rule system that constrains the agent's behavior according to institutional protocols.

**Rule Categories**:
- **Clinical pathways**: Standard diagnostic workup sequences (e.g., "first seizure pathway": EEG → MRI → bloodwork → neurology consult)
- **Formulary rules**: Which medications are available/preferred at this institution
- **Referral protocols**: When and how to escalate to specialists
- **Documentation requirements**: What must be included in reports
- **Safety constraints**: Absolute contraindications, never-events

**Implementation**: Rules encoded as structured YAML/JSON files that are loaded into the agent's system prompt and enforced via output validation.

```yaml
# Example: First Seizure Protocol
pathway:
  name: "First Unprovoked Seizure Workup"
  trigger: "new_onset_seizure"
  steps:
    - order: 1
      action: "obtain_eeg"
      timing: "within_24h"
      mandatory: true
    - order: 2
      action: "obtain_brain_mri"
      timing: "within_7d"
      mandatory: true
      sequences: ["T1", "T2", "FLAIR", "DWI"]
    - order: 3
      action: "lab_panel"
      tests: ["CBC", "BMP", "glucose", "prolactin_if_within_6h"]
      mandatory: true
    - order: 4
      action: "consider_lumbar_puncture"
      condition: "fever OR immunocompromised OR meningeal_signs"
    - order: 5
      action: "neurology_consult"
      timing: "within_48h"
      mandatory: true
  decision_points:
    - if: "eeg_shows_epileptiform AND mri_abnormal"
      then: "high_recurrence_risk → discuss_aed_initiation"
    - if: "eeg_normal AND mri_normal"
      then: "moderate_recurrence_risk → shared_decision_making"
```

#### 3.3.3 Report Generator

The agent produces clinical documents at the end of each encounter:
- Diagnostic summary with full reasoning chain
- Recommended next steps and treatment plan
- Flagged urgencies and safety concerns

Reports are generated by the orchestrator LLM as the final step of the reasoning loop, using all accumulated tool results and reasoning.

---

## 4. Agent Reasoning Loop — Detailed Workflow

### 4.1 Complete Clinical Encounter Flow

```
1. INTAKE
   ├── Doctor inputs: chief complaint, basic history
   ├── System retrieves: patient memory (if returning patient)
   └── Agent formulates: initial assessment + identifies information gaps

2. INFORMATION GATHERING
   ├── Agent reviews available data (uploaded reports, images, signals)
   ├── Agent identifies what tools to invoke
   ├── Agent determines what additional information is needed
   │   ├── Questions for the patient (via Patient Interview Module)
   │   └── Additional tests to request (via Doctor Interface)
   └── Agent prioritizes: which analyses to run first based on clinical urgency

3. ANALYSIS (iterative)
   ├── Invoke relevant tools (EEG analyzer, MRI analyzer, etc.)
   ├── Receive and interpret tool outputs
   ├── Update differential diagnosis based on new evidence
   ├── Check: does the differential narrow sufficiently?
   │   ├── YES → proceed to synthesis
   │   └── NO → request additional data/tests (return to step 2)
   └── Check hospital rules: are all required steps completed?

4. SYNTHESIS
   ├── Combine all evidence into a coherent clinical picture
   ├── Generate ranked differential diagnosis with confidence levels
   ├── Identify supporting and contradicting evidence for each diagnosis
   ├── Search medical literature for similar cases or updated guidelines
   └── Formulate treatment recommendations aligned with hospital formulary

5. OUTPUT
   ├── Present findings to doctor with full reasoning chain
   ├── Highlight critical/urgent findings
   ├── Suggest next steps (additional tests, specialist referral, treatment)
   ├── Generate clinical reports as requested
   └── Update patient memory store

6. FOLLOW-UP
   ├── Track pending test results
   ├── Alert doctor when new results arrive that change the clinical picture
   └── Update longitudinal trends
```

### 4.2 Example Scenarios

Detailed step-by-step scenario walkthroughs (including first seizure, longitudinal follow-up, autoimmune encephalitis, and cardiac syncope cases) are provided in `nmi-paper-plan/02_detailed_scenario_walkthrough.md`.

---

## 5. Technical Stack

### 5.1 Recommended Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Orchestrator LLM** | Qwen3-32B / MedGemma 27B | Best open-source medical reasoning; compared experimentally |
| **Agent Framework** | Custom ReAct implementation | Full control over reasoning loop, tracing, and prompts |
| **Schemas & Validation** | Pydantic + Instructor | Structured LLM outputs with automatic retry on validation failure |
| **Mock Tool Server** | Custom (Python) | Serves pre-generated NeuroBench tool outputs to agent |
| **Vector DB** | ChromaDB | Patient memory semantic search |
| **LLM Inference** | vLLM | Efficient local serving with OpenAI-compatible API + tool calling |
| **Dataset Generation** | Instructor + Anthropic/OpenAI API | Case generation with structured output enforcement |
| **Experiment Tracking** | Weights & Biases | Evaluation tracking across model/ablation experiments |
| **Compute** | 1-2x A100 80GB (or equivalent) | For serving 27-32B orchestrator LLM (no model training needed) |

### 5.2 Development Phases (Revised — Mock-Based Approach)

**Phase 1 — Foundation (Months 1-3)**: Literature review, architecture design, base LLM selection
**Phase 2 — Agent Framework (Months 4-5)**: Core agent loop, tool interface abstraction, mock tool infrastructure
**Phase 3 — Case Generation (Months 3-8)**: NeuroBench case generation pipeline using strong LLMs (Claude/GPT-4), automated validation
**Phase 4 — Memory & Rules (Months 4-5)**: Patient memory system, hospital rules engine
**Phase 5 — Evaluation & Papers (Months 6-16)**: Comprehensive evaluation, model comparison, ablation, paper writing

**Note**: Specialized model training (EEG, MRI analyzers) is NOT required for the core PhD. Tools are evaluated through mock outputs — clinically realistic, pre-generated results produced by a strong "oracle" LLM that knows the ground-truth diagnosis. This decouples the evaluation of agentic reasoning from the accuracy of individual modality models. Real models can be swapped in later without changing the agent framework.

---

## 6. Mock-Based Evaluation Architecture

### 6.1 Why Mock Tool Outputs

The core research question is: "Given reliable tool outputs, can an LLM agent reason across modalities, ask the right follow-up questions, and arrive at the correct diagnosis?" This is independent of whether the EEG model achieves 85% or 95% accuracy. Mocking allows us to:

1. **Isolate reasoning quality** from tool quality
2. **Control experimental conditions** precisely (inject specific noise levels, edge cases)
3. **Scale to hundreds of cases** without training specialized models
4. **Test robustness** by systematically degrading tool outputs

### 6.2 Mock Tool Infrastructure

```
CASE ORACLE (Claude/GPT-4, knows ground truth)
     │
     ├── Pre-generates tool outputs for each case:
     │   ├── analyze_eeg → detailed mock EEG report
     │   ├── analyze_brain_mri → detailed mock radiology report
     │   ├── interpret_labs → mock lab values
     │   ├── analyze_csf → mock CSF results
     │   └── ... (all tools)
     │
     ├── Pre-generates follow-up outputs (branching):
     │   ├── IF agent requests contrast MRI → mock enhanced MRI
     │   ├── IF agent requests video-EEG → mock prolonged EEG
     │   └── ... (15-20 anticipated follow-ups per case)
     │
     └── On-the-fly oracle (for unanticipated requests):
         └── Generates consistent result knowing the ground truth
```

The mock outputs are designed to be:
- **Clinically detailed** (realistic radiology/EEG report format, not just "abnormal")
- **Cross-modally consistent** (EEG focus matches MRI lesion location)
- **Appropriately noisy** (artifacts, borderline findings, limitations noted)

### 6.3 NeuroBench: The Evaluation Benchmark

500+ neurology cases across ~30 conditions with:
- Ground-truth diagnosis and ranked differential
- Pre-generated tool outputs for all tools
- Branching follow-up outputs
- Optimal action sequences (required, acceptable, contraindicated actions)
- Difficulty ratings (straightforward / moderate / diagnostic puzzle)
- Multi-encounter longitudinal cases (50 patients × 3-5 visits)

### 6.4 Evaluation Levels

**Level 1 — Single-Encounter Diagnostic Accuracy**:
- Top-1, Top-3, Top-5 diagnostic accuracy
- Action appropriateness (precision/recall over required/contraindicated actions)
- Reasoning quality (LLM-as-judge + expert sample validation)
- Efficiency (number of tool calls to reach diagnosis)

**Level 2 — Robustness to Imperfect Tools**:
- Noise injection across 5 dimensions × 4 severity levels
- Degradation curves and failure threshold identification
- Agent's ability to detect and flag unreliable outputs

**Level 3 — Longitudinal Memory Evaluation**:
- Multi-encounter scenarios: does the agent recall and integrate prior visits?
- Failure modes: anchoring bias, outdated information, irrelevant recall

**Level 4 — Protocol Adherence**:
- Does the agent follow hospital-specific clinical pathways?
- Safety metric: rate of protocol violations

### 6.5 Baselines

- **Single LLM without tools** (Qwen3-32B, MedGemma 27B) — same patient info, no tool calling
- **MDAgents-style multi-agent** — reimplemented with same base model, text-only reasoning
- **Chain-of-thought prompting** — single LLM with all tool outputs provided upfront (no sequential decision-making)
- **Human neurologist performance** — from published case series and AgentClinic benchmarks
