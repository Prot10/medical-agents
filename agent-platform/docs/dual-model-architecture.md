# Dual-Model Architecture: Qwen Orchestrator + MedGemma Specialist

## Motivation

Benchmark results (NeuroBench v3, 15 cases × 3 repeats) revealed complementary strengths:

| Capability | Qwen-27B (orchestrator) | MedGemma-4B (specialist) |
|:--|:--:|:--:|
| Tool calling / ReAct loop | 93% consistency | Cannot use tools |
| Evidence identification | 4.40/5 | N/A (no tools) |
| Red herring handling | 2.86/5 | **Resistant** (MS-RR-P01: 2/3 vs Qwen 0/3) |
| Dual pathology | **0/3** on FND-P03 | **3/3** on FND-P03 |
| Hallucinated findings | Never | In 4+ cases (critical risk) |
| Consistency | 93% | 53% |

**The insight**: Qwen is excellent at orchestrating investigations but weak at interpreting ambiguous findings. MedGemma has superior medical domain knowledge but cannot manage a multi-step workup. Combining them addresses both weaknesses.

## Architecture

```
Patient presentation
        │
        ▼
┌─────────────────────────────┐
│  Qwen-27B (Orchestrator)    │  Port 8000
│  - ReAct loop management    │
│  - Tool selection & ordering│
│  - Evidence collection      │
│  - Final report generation  │
└────────┬────────────────────┘
         │
         │  Calls 8 tools:
         │  ┌──────────────────────────────────────────────┐
         │  │ analyze_eeg, analyze_brain_mri, analyze_ecg, │
         │  │ interpret_labs, analyze_csf,                  │
         │  │ search_medical_literature,                    │
         │  │ check_drug_interactions,                      │
         │  │ ★ consult_medical_specialist  ← NEW          │
         │  └──────────────────────────────────────────────┘
         │
         │  When Qwen calls consult_medical_specialist:
         ▼
┌─────────────────────────────┐
│  MedGemma-4B (Specialist)   │  Port 8001
│  - Interprets raw findings  │
│  - Evaluates differential   │
│  - Flags red herrings        │
│  - Dual pathology check     │
│  - Returns structured opinion│
└─────────────────────────────┘
```

## When Qwen Should Consult MedGemma

Not every tool call needs MedGemma. The orchestrator should consult the specialist when:

1. **After collecting initial findings** — before committing to a primary diagnosis, ask MedGemma to review all gathered evidence and propose/critique the differential
2. **When findings are ambiguous** — borderline lab values, atypical presentations, conflicting modalities
3. **Before concluding** — as a "second opinion" check against premature closure

The system prompt instructs Qwen to use this tool at key decision points, NOT after every single test result.

## The `consult_medical_specialist` Tool

### Tool Definition (what Qwen sees)

```json
{
  "name": "consult_medical_specialist",
  "description": "Request a second opinion from a medical specialist trained on clinical neurology literature. Send a clinical summary with your current differential and gathered evidence. The specialist will evaluate your reasoning, flag potential red herrings or missed diagnoses, and provide their independent assessment. Use this tool: (1) after gathering initial evidence and before committing to a diagnosis, (2) when findings are ambiguous or conflicting, (3) when you suspect a rare or atypical presentation.",
  "parameters": {
    "clinical_summary": {
      "type": "string",
      "description": "Brief summary of the patient presentation and key findings gathered so far."
    },
    "current_differential": {
      "type": "string",
      "description": "Your current ranked differential diagnosis with supporting evidence for each."
    },
    "specific_question": {
      "type": "string",
      "description": "A specific clinical question you want the specialist to address (e.g., 'Could this be FND superimposed on MS rather than an MS relapse?')"
    }
  }
}
```

### MedGemma Prompt (what MedGemma receives)

```
You are a neurology specialist consultant. A colleague has gathered clinical data
and diagnostic test results for a patient and is asking for your expert opinion.

Review the evidence, evaluate the proposed differential diagnosis, and provide
your independent assessment. Be especially alert for:
- Red herrings: findings that may mislead toward the wrong diagnosis
- Dual pathology: could TWO conditions coexist?
- Atypical presentations of common diseases
- Negative test results that don't rule out a diagnosis (consider sensitivity)

## Clinical Summary
{clinical_summary}

## Colleague's Current Differential
{current_differential}

## Specific Question
{specific_question}

Provide your response as:
### Specialist Opinion
[Your independent assessment of the most likely diagnosis]

### Differential Critique
[Which diagnoses in the colleague's differential you agree/disagree with and why]

### Red Flags
[Any findings that may be misleading or any diagnoses that may have been missed]

### Recommendation
[What additional investigation or clinical consideration would you suggest?]
```

### Tool Implementation

```python
class MedicalSpecialistTool(BaseTool):
    """Consult MedGemma as a specialist second opinion."""

    name = "consult_medical_specialist"

    def __init__(self, specialist_client: LLMClient):
        self.specialist = specialist_client  # MedGemma on port 8001

    def execute(self, call: ToolCall) -> ToolResult:
        prompt = self._build_specialist_prompt(call.parameters)
        response = self.specialist.chat(
            messages=[
                {"role": "system", "content": SPECIALIST_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            tools=None,  # MedGemma gets NO tools — pure knowledge
        )
        return ToolResult(
            tool_name=self.name,
            success=True,
            output={"specialist_opinion": response.content},
        )
```

## Hardware Setup

### VRAM Budget (A100-40GB)

| Component | VRAM |
|:--|:--:|
| Qwen3.5-27B AWQ (weights) | 14.0 GB |
| Qwen3.5-27B AWQ (KV cache) | 8.0 GB |
| MedGemma-4B bf16 (weights) | 8.6 GB |
| MedGemma-4B bf16 (KV cache) | 3.0 GB |
| **Total** | **33.6 GB** |
| **Headroom** | **6.4 GB** |

Both models fit simultaneously. No model swapping needed.

### Serving Configuration

Two separate vLLM instances on different ports:

```bash
# Terminal 1: Orchestrator (Qwen-27B AWQ)
bash agent-platform/scripts/serve_model.sh qwen3.5-27b-awq 8000

# Terminal 2: Specialist (MedGemma-4B)
# Needs modified GPU memory utilization since GPU is shared
VLLM_GPU_MEM=0.35 bash agent-platform/scripts/serve_model.sh medgemma-4b 8001
```

**Critical**: vLLM's `--gpu-memory-utilization` must be split:
- Qwen-27B: `--gpu-memory-utilization 0.58` (~23 GB for weights + KV cache)
- MedGemma-4B: `--gpu-memory-utilization 0.35` (~14 GB for weights + KV cache)
- Remaining ~3 GB for CUDA overhead

### Alternative: Qwen-9B + MedGemma (lighter)

If 27B+4B is too tight on VRAM:
- Qwen3.5-9B fp16: 18 GB + 4 GB KV = 22 GB
- MedGemma-4B bf16: 8.6 GB + 3 GB KV = 11.6 GB
- Total: 33.6 GB — same budget, but 9B gives more KV headroom

## Implementation Plan

### Phase 1: Infrastructure (1-2 days)

1. **Create `specialist_tool.py`** in `agent-platform/src/neuroagent/tools/`:
   - `MedicalSpecialistTool(BaseTool)` that makes an LLM call to MedGemma
   - Accepts clinical_summary, current_differential, specific_question
   - Returns structured specialist opinion
   - Timeout handling (MedGemma should respond in <10s)

2. **Create `serve_dual.sh`** — launches both vLLM instances:
   - Qwen on port 8000 with 58% GPU memory
   - MedGemma on port 8001 with 35% GPU memory
   - Health checks for both
   - Single Ctrl+C kills both

3. **Register the tool** in `ToolRegistry.create_default_registry()`:
   - Add `consult_medical_specialist` as the 8th tool
   - Only registered when `specialist_url` is configured

4. **Update `AgentConfig`** with `specialist_url: str | None = None`

### Phase 2: Prompt Engineering (1 day)

1. **MedGemma system prompt** — focused on:
   - Differential critique (not building the differential from scratch)
   - Red herring identification
   - Dual pathology alerting
   - Explicitly instructed: "Do NOT fabricate test results. You only have the information provided."

2. **Update orchestrator.txt** — add guidance for when to consult:
   ```
   ## When to Consult the Medical Specialist
   You have access to a medical specialist for second opinions. Use this tool:
   - After your initial investigation (2-3 tool calls), before committing to a diagnosis
   - When findings are ambiguous, conflicting, or suggest an atypical presentation
   - When you're considering a rare diagnosis or a diagnosis of exclusion
   Do NOT consult on every case — straightforward presentations don't need it.
   ```

3. **MedGemma anti-hallucination prompt**:
   ```
   CRITICAL: You do NOT have access to diagnostic tools. You have NOT seen any
   EEG, MRI, or lab results unless they are explicitly provided in the clinical
   summary below. Do NOT fabricate or imagine test results. Base your opinion
   ONLY on the information given.
   ```

### Phase 3: Evaluation (2-3 days)

1. **Run the same 15 cases × 3 repeats** with the dual-model setup
2. **Compare to single-model baselines** (already done)
3. **Key metrics to watch**:
   - Does FND-P03 improve from 0/3? (dual pathology test)
   - Does MS-RR-P01 improve from 0/3? (red herring test)
   - Does consistency stay >90%? (Qwen stability)
   - Does MedGemma consultation reduce hallucination vs solo MedGemma?
   - How many cases actually trigger the consultation? (cost efficiency)

### Phase 4: Ablation Studies (2 days)

1. **Always consult** vs **selective consult** vs **never consult**
2. **Consult at start** vs **consult before conclusion** vs **consult after each tool**
3. **9B+4B** vs **27B+4B** — does the orchestrator size matter when specialist is available?

## Expected Impact

| Metric | Qwen-27B Alone | Qwen-27B + MedGemma (expected) |
|:--|:--:|:--:|
| Top-1 accuracy | 64% | **70-75%** |
| Consistency | 93% | **90-93%** (maintained) |
| Red herring handling | 2.86/5 | **3.5+/5** |
| Dual pathology (FND-P03) | 0/3 | **2-3/3** |
| MS-RR-P01 | 0/3 react | **2-3/3** |
| Tools per case | 3.5 | **4.5** (+1 specialist call) |
| Time per case | 95s | **110-120s** (+15-25s for consultation) |
| Tokens per case | 36K | **42-48K** (+specialist I/O) |

## For the Paper

This is a strong architectural contribution:
- **Novel**: Orchestrator + specialist multi-model agent for clinical reasoning
- **Practical**: Fits on a single A100 — no multi-GPU needed
- **Evidence-based**: Motivated by measured complementary strengths from single-model benchmarks
- **Ablation-friendly**: Clean comparison of single vs dual model at each difficulty level
