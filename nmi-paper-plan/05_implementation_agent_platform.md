# NeuroAgent Platform — Implementation Plan for Claude Code

## Overview

This file is the implementation guide for the **NeuroAgent agentic platform**. It consumes NeuroBench cases (produced by the dataset generation pipeline — see `04_implementation_dataset_generation.md`) and evaluates an LLM agent's ability to diagnose neurological conditions through sequential tool-calling, memory, and hospital-rule-aware reasoning.

### Critical Interface Contract

The agent platform imports tool output schemas from the shared `neuroagent-schemas` package. When the agent calls a tool, the mock tool server returns data in the exact Pydantic schemas defined there. The agent's tool-calling format must match the tool schemas.

---

## Project Structure

```
neuroagent/
├── packages/
│   └── neuroagent-schemas/              # SHARED (see dataset generation doc)
├── dataset-generation/                   # See 04_implementation_dataset_generation.md
└── agent-platform/
    ├── pyproject.toml
    ├── config/
    │   ├── agent_config.yaml             # LLM model, inference settings, prompts
    │   ├── hospital_rules/
    │   │   ├── first_seizure.yaml        # First seizure clinical pathway
    │   │   ├── stroke_code.yaml          # Acute stroke pathway
    │   │   ├── dementia_workup.yaml      # Dementia evaluation pathway
    │   │   ├── meningitis.yaml           # Meningitis/encephalitis pathway
    │   │   └── general.yaml              # General neurology rules
    │   └── system_prompts/
    │       ├── orchestrator.txt           # Main agent system prompt
    │       ├── reflection.txt             # Reflection step prompt
    │       └── report_generation.txt      # Clinical report generation prompt
    ├── src/neuroagent/
    │   ├── __init__.py
    │   ├── agent/
    │   │   ├── __init__.py
    │   │   ├── orchestrator.py            # Main agent: ReAct loop with tool dispatch
    │   │   ├── reasoning.py               # Chain-of-thought reasoning module
    │   │   ├── reflection.py              # Post-action reflection module
    │   │   ├── planner.py                 # Action planning (what tool to call next)
    │   │   └── report_generator.py        # Clinical report generation
    │   ├── tools/
    │   │   ├── __init__.py
    │   │   ├── base.py                    # BaseTool abstract class
    │   │   ├── tool_registry.py           # Registry of all available tools
    │   │   ├── mock_server.py             # Serves pre-generated outputs from NeuroBench cases
    │   │   ├── eeg_analyzer.py            # Tool definition: analyze_eeg
    │   │   ├── mri_analyzer.py            # Tool definition: analyze_brain_mri
    │   │   ├── ecg_analyzer.py            # Tool definition: analyze_ecg
    │   │   ├── lab_interpreter.py         # Tool definition: interpret_labs
    │   │   ├── csf_analyzer.py            # Tool definition: analyze_csf
    │   │   ├── literature_search.py       # Tool definition: search_medical_literature
    │   │   ├── drug_interaction.py        # Tool definition: check_drug_interactions
    │   │   └── hospital_rules_checker.py  # Tool definition: check_hospital_rules
    │   ├── memory/
    │   │   ├── __init__.py
    │   │   ├── patient_memory.py          # Per-patient longitudinal memory store
    │   │   ├── memory_retriever.py        # Retrieval strategy (what to include in context)
    │   │   └── memory_summarizer.py       # Compress old encounters into summaries
    │   ├── rules/
    │   │   ├── __init__.py
    │   │   ├── rules_engine.py            # Load and enforce hospital protocols
    │   │   └── pathway_checker.py         # Check if agent actions comply with pathways
    │   ├── evaluation/
    │   │   ├── __init__.py
    │   │   ├── runner.py                  # Run agent on NeuroBench cases, collect traces
    │   │   ├── metrics.py                 # Compute all evaluation metrics
    │   │   ├── noise_injector.py          # Inject noise into tool outputs for robustness eval
    │   │   ├── llm_judge.py              # LLM-as-judge for reasoning quality
    │   │   └── analyzer.py               # Analyze results, generate tables and figures
    │   └── llm/
    │       ├── __init__.py
    │       ├── client.py                  # Unified LLM client (vLLM, OpenAI, Anthropic)
    │       └── prompts.py                 # Prompt management and formatting
    ├── scripts/
    │   ├── run_evaluation.py              # Main: run agent on test set
    │   ├── run_single_case.py             # Debug: run agent on one case, print trace
    │   ├── run_robustness_eval.py         # Run noise injection experiments
    │   ├── run_longitudinal_eval.py       # Run multi-encounter evaluation
    │   ├── run_model_comparison.py        # Compare different orchestrator LLMs
    │   ├── analyze_results.py             # Generate tables, figures, statistics
    │   └── interactive_demo.py            # Interactive mode: doctor types, agent responds
    └── tests/
        ├── test_orchestrator.py
        ├── test_tools.py
        ├── test_mock_server.py
        ├── test_memory.py
        ├── test_rules.py
        ├── test_evaluation.py
        └── fixtures/
            └── sample_case.json           # One complete NeuroBenchCase for testing
```

---

## Step-by-Step Implementation TODO

### Phase 0: Project Setup

```
TODO-A0.1: Initialize agent-platform package in the monorepo
  - Add to uv workspace
  - Dependencies:
    - neuroagent-schemas (local workspace dependency)
    - pydantic >= 2.0
    - openai >= 1.0        # For vLLM/OpenAI-compatible API
    - instructor >= 1.0    # Structured output from LLM
    - chromadb             # Vector store for patient memory
    - pyyaml               # Config loading
    - rich                 # Logging and trace display
    - typer                # CLI
    - polars               # Results analysis
    - matplotlib           # Figures for paper
    - seaborn              # Figures for paper
    - pytest
    - pytest-asyncio

TODO-A0.2: Copy sample_case.json from dataset-generation fixtures
  - This is the same fixture used in dataset tests
  - Ensures both systems agree on format
```

### Phase 1: Tool System

The tool system is the backbone. Every tool has the same interface but the mock server swaps in pre-generated outputs instead of calling real models.

```
TODO-A1.1: Implement base.py — BaseTool abstract class

  from abc import ABC, abstractmethod
  from pydantic import BaseModel

  class ToolCall(BaseModel):
      """What the agent produces when it wants to call a tool."""
      tool_name: str
      parameters: dict

  class ToolResult(BaseModel):
      """What the tool returns to the agent."""
      tool_name: str
      success: bool
      output: BaseModel  # One of: EEGReport, MRIReport, LabResults, ...
      error_message: str | None = None

  class BaseTool(ABC):
      name: str
      description: str
      parameter_schema: dict  # JSON schema for the tool's parameters

      @abstractmethod
      def execute(self, parameters: dict) -> ToolResult:
          """Execute the tool and return a result."""

      def get_tool_definition(self) -> dict:
          """Return OpenAI-style tool definition for the LLM."""
          return {
              "type": "function",
              "function": {
                  "name": self.name,
                  "description": self.description,
                  "parameters": self.parameter_schema
              }
          }

TODO-A1.2: Implement individual tool definitions
  Each tool file (eeg_analyzer.py, mri_analyzer.py, etc.) defines:
  - Tool name, description, parameter schema
  - In MOCK mode: delegates to MockServer
  - In REAL mode (future): delegates to actual model endpoint

  Example (eeg_analyzer.py):

  class EEGAnalyzerTool(BaseTool):
      name = "analyze_eeg"
      description = (
          "Analyze an EEG recording for neurological abnormalities. "
          "Returns classification (normal/abnormal), detected findings with "
          "locations and timestamps, activating procedure results, and "
          "clinical impression."
      )
      parameter_schema = {
          "type": "object",
          "properties": {
              "eeg_file_path": {"type": "string", "description": "Path to EEG file"},
              "patient_age": {"type": "integer"},
              "clinical_context": {"type": "string", "description": "Why the EEG was ordered"},
              "focus_areas": {
                  "type": "array",
                  "items": {"type": "string"},
                  "description": "Specific patterns to look for"
              }
          },
          "required": ["clinical_context"]
      }

      def __init__(self, mock_server: MockServer | None = None):
          self.mock_server = mock_server

      def execute(self, parameters: dict) -> ToolResult:
          if self.mock_server:
              return self.mock_server.get_output("analyze_eeg", parameters)
          else:
              raise NotImplementedError("Real EEG model not yet connected")

  Implement ALL 8 tools following this pattern:
  - analyze_eeg
  - analyze_brain_mri
  - analyze_ecg
  - interpret_labs
  - analyze_csf
  - search_medical_literature
  - check_drug_interactions
  - check_hospital_rules

TODO-A1.3: Implement tool_registry.py

  class ToolRegistry:
      def __init__(self):
          self.tools: dict[str, BaseTool] = {}

      def register(self, tool: BaseTool):
          self.tools[tool.name] = tool

      def get_tool(self, name: str) -> BaseTool:
          return self.tools[name]

      def get_all_definitions(self) -> list[dict]:
          """Return all tool definitions for the LLM system prompt."""
          return [t.get_tool_definition() for t in self.tools.values()]

      def execute(self, tool_call: ToolCall) -> ToolResult:
          tool = self.get_tool(tool_call.tool_name)
          return tool.execute(tool_call.parameters)

TODO-A1.4: Implement mock_server.py

  class MockServer:
      """
      Serves pre-generated tool outputs from a NeuroBenchCase.
      When the agent calls a tool, this returns the matching pre-generated output.
      """
      def __init__(self, case: NeuroBenchCase):
          self.case = case
          self.call_log: list[ToolCall] = []  # Track all tool calls for evaluation

      def get_output(self, tool_name: str, parameters: dict) -> ToolResult:
          self.call_log.append(ToolCall(tool_name=tool_name, parameters=parameters))

          # Check initial tool outputs
          output = self._match_initial_output(tool_name)
          if output:
              return ToolResult(tool_name=tool_name, success=True, output=output)

          # Check follow-up outputs
          output = self._match_followup_output(tool_name, parameters)
          if output:
              return ToolResult(tool_name=tool_name, success=True, output=output)

          # Tool not available for this case
          return ToolResult(
              tool_name=tool_name, success=False, output=None,
              error_message=f"No {tool_name} data available for this patient. "
                            f"Consider whether this test is appropriate."
          )

      def _match_initial_output(self, tool_name: str) -> BaseModel | None:
          """Match tool_name to the case's initial ToolOutputSet."""
          mapping = {
              "analyze_eeg": self.case.initial_tool_outputs.eeg,
              "analyze_brain_mri": self.case.initial_tool_outputs.mri,
              "analyze_ecg": self.case.initial_tool_outputs.ecg,
              "interpret_labs": self.case.initial_tool_outputs.labs,
              "analyze_csf": self.case.initial_tool_outputs.csf,
              # literature_search and drug_interactions use parameter-based lookup
          }
          return mapping.get(tool_name)

      def _match_followup_output(self, tool_name: str, parameters: dict) -> BaseModel | None:
          """Match against pre-generated follow-up outputs."""
          for followup in self.case.followup_outputs:
              if followup.tool_name == tool_name:
                  # Fuzzy match on trigger_action vs parameters
                  return followup.output
          return None

      def get_call_log(self) -> list[ToolCall]:
          return self.call_log
```

### Phase 2: Agent Core — The Orchestrator

```
TODO-A2.1: Design the system prompt (config/system_prompts/orchestrator.txt)

  The system prompt is critical. It must:
  - Define the agent's role (neurology clinical decision support)
  - Explain the available tools (injected dynamically from ToolRegistry)
  - Define the reasoning format (structured chain-of-thought)
  - Explain the ReAct loop (THINK → ACT → OBSERVE → REFLECT)
  - Instruct on confidence reporting and differential diagnosis format
  - Instruct on when to ask follow-up questions
  - Instruct on safety (flag uncertainties, escalate high-risk decisions)
  - Include hospital rules context (loaded from rules engine)
  - Include patient memory context (loaded from memory retriever)

  The prompt should NOT be a giant wall of text. Structure it with clear sections.
  Test and iterate on this — the system prompt determines 80% of agent behavior.

TODO-A2.2: Implement orchestrator.py — the main agent loop

  class AgentOrchestrator:
      def __init__(self, config: AgentConfig, tool_registry: ToolRegistry,
                   memory: PatientMemory | None = None,
                   rules_engine: RulesEngine | None = None):
          self.llm = LLMClient(config)
          self.tools = tool_registry
          self.memory = memory
          self.rules = rules_engine
          self.max_turns = config.max_turns  # safety limit (e.g., 15)

      def run(self, patient_info: str, patient_id: str | None = None) -> AgentTrace:
          """
          Run the agent on a patient case.

          Args:
              patient_info: The initial clinical information (chief complaint + history)
              patient_id: If set, load patient memory

          Returns:
              AgentTrace: Complete record of all turns, thoughts, actions, and outputs
          """
          trace = AgentTrace()

          # Build initial context
          messages = self._build_initial_messages(patient_info, patient_id)

          for turn in range(self.max_turns):
              # Call LLM with tool definitions
              response = self.llm.chat(
                  messages=messages,
                  tools=self.tools.get_all_definitions(),
                  tool_choice="auto"  # LLM decides whether to call a tool or respond
              )

              # Record the turn
              trace.add_turn(response)

              # If LLM wants to call tool(s)
              if response.tool_calls:
                  for tool_call in response.tool_calls:
                      result = self.tools.execute(tool_call)
                      trace.add_tool_result(tool_call, result)
                      messages.append(format_tool_result(tool_call, result))

                  # Add reflection prompt after tool results
                  messages.append(self._reflection_prompt())

              # If LLM responds with text (no tool call) → it's done
              else:
                  trace.set_final_response(response.content)
                  break

          # Update patient memory with this encounter
          if self.memory and patient_id:
              self.memory.store_encounter(patient_id, trace)

          return trace

      def _build_initial_messages(self, patient_info, patient_id) -> list[dict]:
          system = self._build_system_prompt(patient_id)
          return [
              {"role": "system", "content": system},
              {"role": "user", "content": patient_info}
          ]

      def _build_system_prompt(self, patient_id) -> str:
          base = load_prompt("orchestrator.txt")

          # Inject hospital rules
          if self.rules:
              base += "\n\n## Hospital Protocols\n" + self.rules.get_context()

          # Inject patient memory
          if self.memory and patient_id:
              history = self.memory.retrieve(patient_id)
              if history:
                  base += "\n\n## Patient History\n" + history

          return base

      def _reflection_prompt(self) -> dict:
          return {
              "role": "user",
              "content": (
                  "Based on the tool results above, update your clinical reasoning. "
                  "What do these findings tell you? How does this change your differential? "
                  "What should you do next? If you have enough information for a diagnosis "
                  "and recommendations, provide your final assessment."
              )
          }

TODO-A2.3: Define AgentTrace — the complete record of an agent run

  class AgentTurn(BaseModel):
      turn_number: int
      role: str  # "assistant" or "tool"
      content: str | None  # reasoning text
      tool_calls: list[ToolCall] | None
      tool_results: list[ToolResult] | None

  class AgentTrace(BaseModel):
      case_id: str | None
      turns: list[AgentTurn] = []
      final_response: str | None = None
      total_tool_calls: int = 0
      tools_called: list[str] = []  # ordered list of tool names called
      total_tokens: int = 0
      elapsed_time_seconds: float = 0

      def add_turn(self, response): ...
      def add_tool_result(self, call, result): ...
      def set_final_response(self, content): ...
```

### Phase 3: Memory System

```
TODO-A3.1: Implement patient_memory.py

  class PatientMemory:
      """Per-patient longitudinal memory store."""

      def __init__(self, db_path: str = "./data/patient_memory"):
          self.vector_store = chromadb.PersistentClient(path=db_path)
          self.collection = self.vector_store.get_or_create_collection("patient_encounters")

      def store_encounter(self, patient_id: str, trace: AgentTrace):
          """Store a completed encounter in memory."""
          # Extract key information from the trace
          summary = self._summarize_encounter(trace)
          # Store as vector (for semantic retrieval) + metadata (for structured queries)
          self.collection.add(
              documents=[summary],
              metadatas=[{
                  "patient_id": patient_id,
                  "date": trace.timestamp,
                  "diagnoses": trace.extracted_diagnoses,
                  "medications": trace.extracted_medications,
              }],
              ids=[f"{patient_id}_{trace.timestamp}"]
          )

      def retrieve(self, patient_id: str, current_complaint: str | None = None,
                   max_encounters: int = 5) -> str:
          """Retrieve relevant patient history for the agent's context."""
          # Always retrieve: most recent encounters
          # If current_complaint provided: also retrieve semantically similar past encounters
          # Format as a structured patient history summary
          ...

TODO-A3.2: Implement memory_summarizer.py
  - Compress old encounters into concise summaries
  - Keep key facts: diagnoses, medications, test results, follow-up plans
  - Discard verbose reasoning chains from past encounters
  - This prevents context window overflow for patients with many encounters
```

### Phase 4: Hospital Rules Engine

```
TODO-A4.1: Implement rules_engine.py

  class RulesEngine:
      def __init__(self, rules_dir: str = "config/hospital_rules"):
          self.pathways = self._load_pathways(rules_dir)

      def get_context(self) -> str:
          """Return a summary of available protocols for the system prompt."""
          return "\n".join([
              f"- {p.name}: {p.description} (triggers: {p.triggers})"
              for p in self.pathways
          ])

      def get_pathway(self, trigger: str) -> ClinicalPathway | None:
          """Find the matching clinical pathway for a trigger condition."""
          ...

      def check_compliance(self, trace: AgentTrace, pathway: ClinicalPathway) -> ComplianceResult:
          """Check if the agent's actions comply with the specified pathway."""
          required_actions = pathway.get_required_actions()
          agent_actions = trace.tools_called
          missing = [a for a in required_actions if a not in agent_actions]
          violations = []  # contraindicated actions the agent took
          return ComplianceResult(compliant=len(missing)==0, missing=missing, violations=violations)

TODO-A4.2: Define YAML clinical pathway format
  Example (config/hospital_rules/first_seizure.yaml):

  name: "First Unprovoked Seizure Workup"
  description: "Standard workup for patients presenting with a first unprovoked seizure"
  triggers: ["first_seizure", "new_onset_seizure"]
  steps:
    - action: "interpret_labs"
      timing: "immediate"
      mandatory: true
      tests: ["CBC", "BMP", "glucose", "prolactin"]
    - action: "analyze_eeg"
      timing: "within_24h"
      mandatory: true
    - action: "analyze_brain_mri"
      timing: "within_7d"
      mandatory: true
      sequences: ["T1", "T2", "FLAIR", "DWI"]
    - action: "check_drug_interactions"
      timing: "before_discharge"
      mandatory: true
      condition: "if_aed_started"
  contraindicated:
    - "Starting phenytoin without checking HLA-B*15:02 in patients of Asian descent"
    - "Discharging without driving restriction counseling"

  Create pathways for: first_seizure, stroke_code, dementia_workup, meningitis, general
```

### Phase 5: Evaluation System

```
TODO-A5.1: Implement runner.py — run agent on NeuroBench cases

  class EvaluationRunner:
      def __init__(self, agent: AgentOrchestrator, dataset_path: str):
          self.agent = agent
          self.cases = self._load_cases(dataset_path)

      def run_evaluation(self, split: str = "test",
                         max_cases: int | None = None) -> EvaluationResults:
          """Run agent on all cases in the specified split."""
          results = []
          for case in self.cases[split][:max_cases]:
              # Set up mock server for this case
              mock = MockServer(case)
              self.agent.tools = self._build_tool_registry(mock)

              # Prepare initial patient info (only chief complaint + history,
              # NOT the tool outputs — agent must request them)
              patient_info = self._format_initial_info(case)

              # Run agent
              trace = self.agent.run(patient_info)

              # Evaluate
              metrics = self._evaluate_trace(trace, case)
              results.append(CaseResult(case_id=case.case_id, trace=trace, metrics=metrics))

          return EvaluationResults(results=results)

      def _format_initial_info(self, case: NeuroBenchCase) -> str:
          """Format only what the doctor would tell the agent initially."""
          return (
              f"Patient: {case.patient.demographics.age}-year-old "
              f"{case.patient.demographics.sex}\n"
              f"Chief complaint: {case.patient.chief_complaint}\n"
              f"History of present illness: {case.patient.history_present_illness}\n"
              f"Past medical history: {case.patient.clinical_history.past_medical_history}\n"
              f"Medications: {case.patient.clinical_history.medications}\n"
              f"Allergies: {case.patient.clinical_history.allergies}\n"
              f"Examination: {case.patient.neurological_exam.model_dump_json()}\n"
              f"Vitals: {case.patient.vitals.model_dump_json()}"
          )

TODO-A5.2: Implement metrics.py — all evaluation metrics

  class MetricsCalculator:
      def compute_all(self, trace: AgentTrace, case: NeuroBenchCase) -> CaseMetrics:
          return CaseMetrics(
              diagnostic_accuracy=self._diagnostic_accuracy(trace, case),
              top3_accuracy=self._top3_accuracy(trace, case),
              action_precision=self._action_precision(trace, case),
              action_recall=self._action_recall(trace, case),
              critical_actions_hit=self._critical_actions(trace, case),
              contraindicated_actions_taken=self._contraindicated_actions(trace, case),
              tool_call_count=trace.total_tool_calls,
              efficiency_score=self._efficiency(trace, case),
              reasoning_quality=None,  # filled later by LLM judge
              protocol_compliance=None  # filled later by rules engine
          )

  Metrics computed:
  - diagnostic_accuracy_top1: bool — is the primary diagnosis correct?
  - diagnostic_accuracy_top3: bool — is the correct diagnosis in the top 3?
  - action_precision: float — fraction of agent's tool calls that were required/acceptable
  - action_recall: float — fraction of required actions the agent actually performed
  - critical_actions_hit: float — fraction of MUST-DO actions completed
  - contraindicated_taken: int — count of MUST-NOT-DO actions performed (should be 0)
  - efficiency: float — how close to optimal number of tool calls
  - safety_score: float — composite of critical_actions_hit and contraindicated_taken

TODO-A5.3: Implement llm_judge.py — reasoning quality assessment

  class LLMJudge:
      """Use a strong LLM to assess the quality of the agent's reasoning chain."""

      def judge(self, trace: AgentTrace, case: NeuroBenchCase) -> ReasoningScore:
          """
          Prompt a judge LLM to rate the reasoning on a rubric:
          1. Evidence identification (0-5): Does the agent identify key findings?
          2. Evidence integration (0-5): Does it correctly combine findings across modalities?
          3. Differential reasoning (0-5): Does it consider and rule out alternatives?
          4. Uncertainty handling (0-5): Does it acknowledge uncertainty appropriately?
          5. Clinical safety (0-5): Does it flag red flags and avoid dangerous actions?
          """

  Use a DIFFERENT model as judge than the one being evaluated.
  E.g., if evaluating Qwen3-32B, use Claude Sonnet as judge.

TODO-A5.4: Implement noise_injector.py — robustness evaluation

  class NoiseInjector:
      """Injects controlled noise into mock tool outputs."""

      def inject(self, tool_output: BaseModel, noise_type: NoiseType,
                 severity: float) -> BaseModel:
          """
          noise_type options:
          - ACCURACY: Replace correct findings with incorrect ones
          - COMPLETENESS: Remove some findings (partial report)
          - CONFIDENCE: Miscalibrate confidence scores
          - CONTRADICTION: Make findings contradict other modalities
          - SPECIFICITY: Replace detailed findings with vague ones

          severity: 0.0 (no noise) to 1.0 (maximum corruption)
          """

  Implementation approach:
  For each noise type, use an LLM to modify the tool output:
  - ACCURACY: "Take this EEG report and change the location of the epileptiform
    focus from right temporal to left frontal. Keep everything else the same."
  - COMPLETENESS: "Remove 2 out of 4 findings from this MRI report."
  - CONFIDENCE: Multiply/divide confidence by a random factor
  - CONTRADICTION: "Modify this MRI report so the lesion is on the LEFT side,
    contradicting the EEG which shows a RIGHT temporal focus."
  - SPECIFICITY: "Replace this detailed EEG report with a brief one that just
    says 'abnormal EEG showing epileptiform discharges.'"

  Critical: the modified output must still be a valid Pydantic model (pass schema
  validation). Use instructor to regenerate with constraints.

TODO-A5.5: Implement analyzer.py — results analysis and paper figures

  class ResultsAnalyzer:
      def generate_main_table(self, results: EvaluationResults) -> polars.DataFrame:
          """Table 1 of the paper: models × metrics."""

      def generate_ablation_table(self, results: dict[str, EvaluationResults]) -> polars.DataFrame:
          """Table 2: ablation (with/without tools, memory, rules)."""

      def generate_robustness_curves(self, robustness_results) -> matplotlib.Figure:
          """Figure: accuracy vs. noise level for each noise type."""

      def generate_condition_breakdown(self, results) -> matplotlib.Figure:
          """Figure: accuracy by condition category (Tier 1/2/3)."""

      def generate_difficulty_breakdown(self, results) -> matplotlib.Figure:
          """Figure: accuracy by difficulty level."""

      def export_case_examples(self, results, n=5) -> str:
          """Export detailed case walkthroughs for the paper's qualitative section."""
```

### Phase 6: Running Experiments

```
TODO-A6.1: Implement run_evaluation.py (main entry point)

  @app.command()
  def evaluate(
      model: str = "qwen3-32b",        # Orchestrator model
      dataset: str = "data/neurobench_v1",
      split: str = "test",
      output_dir: str = "results/",
      max_cases: int | None = None,
      enable_memory: bool = True,
      enable_rules: bool = True,
      judge_model: str = "claude-sonnet",  # For reasoning quality
  ):
      ...

TODO-A6.2: Implement run_model_comparison.py
  Run evaluation with different orchestrator models:
  - Qwen3-32B (via vLLM)
  - MedGemma 27B (via vLLM)
  - OpenBioLLM-70B (via vLLM)
  - Qwen3-8B (smaller ablation)
  - MedGemma 4B (smaller ablation)
  Save all results for comparative analysis.

TODO-A6.3: Implement run_robustness_eval.py
  For each noise type × severity level:
  - Inject noise into test set tool outputs
  - Run agent on noisy dataset
  - Compute metrics
  - Compare with clean baseline
  Grid: 5 noise types × 4 severity levels (0.1, 0.25, 0.5, 0.75) = 20 runs

TODO-A6.4: Implement run_longitudinal_eval.py
  - Load multi-encounter cases from data/neurobench_v1/longitudinal/
  - Run agent on encounter 1, store memory
  - Run agent on encounter 2 WITH memory from encounter 1
  - Compare: agent with memory vs. agent without memory
  - Evaluate: does it correctly recall and integrate prior information?

TODO-A6.5: Implement interactive_demo.py
  For demonstration and debugging:
  - Doctor types patient info
  - Agent responds in real-time
  - Tool calls shown interactively
  - Useful for paper demo and supervisor presentations
```

### Phase 7: Ablation Experiments

```
TODO-A7.1: Define ablation configurations
  Ablations to run (each is a full evaluation run):
  1. Full system (all tools + memory + rules) — the main result
  2. No tools — agent gets patient info only, must reason without any test results
  3. All info upfront — agent gets all tool outputs at once, no sequential reasoning
  4. No memory — agent has no access to prior encounters (longitudinal cases only)
  5. No rules — agent has no hospital protocols
  6. No reflection — remove the reflection step after each tool result
  7. Single tool only — only one tool available at a time (how much does each tool contribute?)
  8. Random tool ordering — force agent to use tools in random order (vs. its own chosen order)
```

---

## LLM Serving Configuration

```
TODO-A8.1: Set up vLLM for local model serving
  For Qwen3-32B:
    vllm serve Qwen/Qwen3-32B \
      --enable-auto-tool-choice \
      --tool-call-parser hermes \
      --max-model-len 32768 \
      --tensor-parallel-size 2 \
      --gpu-memory-utilization 0.90

  For MedGemma 27B:
    vllm serve google/medgemma-27b-it \
      --enable-auto-tool-choice \
      --tool-call-parser hermes \
      --max-model-len 32768 \
      --tensor-parallel-size 2

  Both expose an OpenAI-compatible API at http://localhost:8000
  The agent code doesn't need to change — just switch the base_url and model_name
  in agent_config.yaml.

TODO-A8.2: Set up judge model
  For LLM-as-judge, use a different provider (Anthropic Claude or OpenAI GPT-4)
  to avoid self-evaluation bias. Configure in agent_config.yaml:
    judge:
      provider: "anthropic"
      model: "claude-sonnet-4-20250514"
```

---

## Shared Interface Contract Summary

Both systems depend on `neuroagent-schemas`. Here's the contract:

| Schema | Produced by | Consumed by |
|--------|-------------|-------------|
| `PatientProfile` | Dataset generator | Agent (as initial input) |
| `EEGReport` | Dataset generator (mock) | Agent (as tool output) |
| `MRIReport` | Dataset generator (mock) | Agent (as tool output) |
| `LabResults` | Dataset generator (mock) | Agent (as tool output) |
| `CSFResults` | Dataset generator (mock) | Agent (as tool output) |
| `ECGReport` | Dataset generator (mock) | Agent (as tool output) |
| `LiteratureSearchResult` | Dataset generator (mock) | Agent (as tool output) |
| `DrugInteractionResult` | Dataset generator (mock) | Agent (as tool output) |
| `NeuroBenchCase` | Dataset generator | Evaluation runner (loads cases) |
| `GroundTruth` | Dataset generator | Evaluation metrics (compares against) |
| `AgentTrace` | Agent orchestrator | Evaluation metrics + LLM judge |

**Rule**: If you change a schema in `neuroagent-schemas`, BOTH systems must still work. Run tests in both packages after any schema change.
