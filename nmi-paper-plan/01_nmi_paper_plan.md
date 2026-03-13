# NeuroAgent — Nature Machine Intelligence Paper Plan

## 1. What Goes Into This One Paper

NMI expects a complete, self-contained story. We condense the framework, the benchmark, the mock evaluation methodology, the robustness analysis, AND the memory/rules evaluation into a single comprehensive paper. This works because NMI papers are typically longer than conference papers (methods + supplementary can be substantial), and they value depth over breadth.

The paper tells one story: **An LLM agent that reasons across multimodal neurological data through tool-calling outperforms existing approaches, degrades gracefully under tool imperfections, and benefits significantly from longitudinal memory and institutional protocol awareness.**

---

## 2. Paper Structure and Content

### Title (working)

"NeuroAgent: Tool-Augmented Multi-Modal Reasoning for Neurological Clinical Decision Support"

### Abstract (~250 words)

Frames the problem (neurological diagnosis requires integrating EEG, MRI, fMRI, labs, clinical history — currently no AI system does this), introduces the solution (a tool-augmented LLM agent with memory and hospital-rule compliance), announces the benchmark (NeuroBench — 500+ neurology cases with mock tool outputs), and highlights the key results (outperforms baselines on diagnostic accuracy, is robust to moderate tool noise, and benefits from memory/rules).

### Introduction (2-3 pages)

- The clinical need: neurological diagnosis is multi-modal, sequential, and error-prone
- The state of AI: current medical LLMs are text-only or single-modality; existing agent frameworks (MDAgents) don't integrate multimodal tool use
- Our contribution (stated explicitly — NMI reviewers want this upfront):
  1. NeuroAgent: the first tool-augmented agent framework for multi-modal neurological reasoning
  2. NeuroBench: a benchmark of 500+ neurology cases with pre-generated multi-modal tool outputs
  3. A mock-based evaluation methodology that enables controlled study of agentic clinical reasoning
  4. Systematic analysis of robustness to imperfect tool outputs
  5. First evaluation of longitudinal patient memory and hospital protocol compliance in clinical AI agents

### Related Work (1-2 pages)

- Medical AI agents (MDAgents, KG4Diagnosis, Zodiac, Healthcare Agent)
- Medical LLMs (MedGemma, Qwen3, OpenBioLLM)
- Multi-modal medical AI (RadFM, M3D-LaMed, ECGChat, EEG-LLM)
- Clinical evaluation benchmarks (AgentClinic, MedAgentBench)
- Synthetic clinical data generation

### Methods (5-7 pages — the core)

**3.1 NeuroAgent Architecture**
- Orchestrator agent design (ReAct loop with reflection)
- Tool interface specification (8 tools: EEG, MRI, fMRI, ECG, labs, CSF, literature search, drug interactions)
- Patient memory system (hybrid vector + structured storage)
- Hospital rules engine (YAML-encoded clinical pathways)
- Detailed tool schema examples (2-3 tools shown in full)

**3.2 NeuroBench: Benchmark Design**
- Case generation pipeline using strong oracle LLMs
- Condition coverage (30 neurological conditions, 3 tiers of rarity)
- Mock tool output format (detailed, clinically realistic, cross-modally consistent)
- Branching follow-up outputs for sequential decision-making
- Ground-truth action sequences (required, acceptable, contraindicated)
- Automated consistency validation
- Expert neurologist validation process
- Dataset statistics (demographics, difficulty distribution, modality coverage)

**3.3 Evaluation Methodology**
- Mock-based evaluation: rationale, design, validity argument
- Level 1: single-encounter diagnostic evaluation
- Level 2: robustness evaluation (noise injection framework — 5 noise types × 4 severity levels)
- Level 3: longitudinal memory evaluation (multi-encounter scenarios)
- Level 4: protocol adherence evaluation
- Metrics for each level
- Baselines: single LLM, MDAgents, chain-of-thought with all info upfront, human performance from literature

**3.4 Experimental Setup**
- Models compared as orchestrator (Qwen3-32B, MedGemma 27B, OpenBioLLM-70B)
- Inference infrastructure (vLLM, hardware specs)
- Prompt design (system prompts, tool-calling format)
- Evaluation details (LLM-as-judge setup, expert evaluation sample size)

### Results (4-5 pages)

**4.1 Main Results: Diagnostic Accuracy**
- Table: all models × all baselines on NeuroBench
- Analysis by condition category (Tier 1 vs Tier 2 vs Tier 3)
- Analysis by case difficulty (straightforward vs moderate vs puzzle)
- Tool-augmented agent vs. raw LLM gap quantified

**4.2 Ablation Studies**
- Remove each tool individually → measure impact
- Remove memory → measure impact on multi-encounter cases
- Remove rules → measure protocol adherence drop and safety impact
- Remove reflection step → measure reasoning quality drop

**4.3 Robustness to Imperfect Tools**
- Degradation curves: accuracy vs. tool noise level for each noise type
- Identification of critical failure thresholds
- Which error types are most dangerous (false negatives on critical findings)
- Agent's ability to detect and flag unreliable outputs
- Practical insight: what tool reliability is needed for clinical viability?

**4.4 Longitudinal Memory Evaluation**
- Memory-enabled vs. memoryless agent on multi-encounter cases
- Cases where memory helps (progressive diseases, medication tracking)
- Cases where memory hurts (anchoring bias, outdated information)

**4.5 Protocol Adherence**
- Rule-constrained vs. unconstrained agent
- Rate of protocol violations
- Safety analysis: how often does the unconstrained agent suggest dangerous actions?

**4.6 Qualitative Analysis**
- 3-4 detailed case walkthroughs showing the agent's full reasoning chain
- Example of a case where the agent succeeds by combining evidence across modalities
- Example of a case where the agent fails and why
- Expert neurologist commentary on agent reasoning quality

### Discussion (2-3 pages)

- What we learned about multi-modal agentic reasoning in medicine
- Why tool-augmented reasoning outperforms monolithic approaches
- The robustness problem: implications for deploying agent systems with imperfect components
- The memory advantage: why longitudinal context matters for clinical AI
- Limitations (mocked tools, synthetic cases, no real clinical deployment)
- Path forward: plugging in real models, real clinical data, prospective validation
- Ethical considerations: this is a decision-support tool, not an autonomous doctor

### Supplementary Material (substantial)

- Complete tool schemas for all 8 tools
- Full list of 30 neurological conditions with case counts
- NeuroBench dataset statistics and validation details
- All prompt templates
- Additional case walkthroughs
- Extended ablation results
- Inter-annotator agreement on expert validation

---

## 3. What This Paper Claims (and What It Doesn't)

### Claims:

1. Tool-augmented agentic reasoning significantly outperforms text-only LLM reasoning for multi-modal neurological diagnosis
2. Sequential decision-making (requesting tests in order) is better than receiving all information at once — the agent learns what to ask for
3. Open-source LLMs (Qwen3-32B, MedGemma 27B) are viable orchestrators for clinical agent systems
4. Agent performance degrades gracefully under moderate tool noise but collapses beyond specific thresholds
5. Longitudinal patient memory improves diagnostic accuracy on follow-up encounters
6. Hospital protocol constraints improve safety without sacrificing diagnostic accuracy

### Does NOT Claim:

- That the system is ready for clinical deployment (it's evaluated on mock/synthetic data)
- That individual tool models are state-of-the-art (tools are mocked; the contribution is the reasoning framework)
- That the system replaces neurologists (it's designed as a decision-support tool)

---

## 4. Timeline to Submission

| Month | Work | Output |
|-------|------|--------|
| **M1-2** | Literature review; study MDAgents/AgentClinic codebases; set up infrastructure | Literature review draft |
| **M3-4** | Implement core agent (ReAct loop + tool interfaces + mock infrastructure) | Working agent prototype |
| **M5-6** | Implement memory + rules; build case generation pipeline; generate 200 pilot cases | Memory/rules operational; pilot cases |
| **M7-8** | Scale to 500+ cases; implement all evaluation harnesses; run pilot experiments | Full benchmark; preliminary results |
| **M9-10** | Full experimental suite: model comparison, ablation, robustness, memory, rules | All results complete |
| **M11** | Expert validation (neurologist reviews 50+ cases and agent outputs) | Expert evaluation data |
| **M12-13** | Write paper; internal review with advisor and neurologist co-author | Full paper draft |
| **M14** | Revise; submit to NMI | **Submitted** |
| **M15-20** | Review period (~3-6 months); address reviews; revise and resubmit if needed | **Accepted (target)** |

**Realistic submission**: ~14 months after starting (~May-June 2027)

**Plan B if NMI rejects**: Revise framing and submit to ICLR 2028 (deadline ~October 2027) or NeurIPS 2027 (deadline ~May 2027 — only if you accelerate).

---

## 5. Remaining Papers (After NMI)

Once the NMI paper is submitted/published, the remaining publishable work:

**Paper 2 — Extended Robustness Study** → NeurIPS/ICML
The NMI paper will include robustness results, but as one section among many. A dedicated robustness paper can go deeper: more noise types, cross-domain experiments (apply the same framework to cardiology or emergency medicine), theoretical analysis of degradation patterns, practical guidelines for tool developers. This generalizes beyond neurology and targets the ML methods community.

**Paper 3 — NeuroBench Dataset Paper** → NeurIPS Datasets & Benchmarks
Release the full benchmark with documentation, baseline results, and a leaderboard. The NMI paper uses the benchmark but doesn't fully describe it as a community resource.

**Paper 4 — Clinical Pilot** → npj Digital Medicine / The Lancet Digital Health
If the hospital partnership materializes, run the agent on real de-identified cases. This is the clinical validation paper that transforms the work from "lab experiment" to "path to deployment."

---

## 6. What Makes This a NMI Paper (vs. a Conference Paper)

| Aspect | Conference Paper | NMI Paper (what we're doing) |
|--------|-----------------|-----|
| Story | One result ("our system beats baselines") | Complete narrative (system + benchmark + robustness + memory + rules + clinical analysis) |
| Depth | Results on one evaluation axis | Multi-level evaluation with qualitative clinical analysis |
| Clinical grounding | Benchmarks only | Expert neurologist evaluation + clinical case walkthroughs |
| Impact framing | "We advance the state of the art" | "We demonstrate a viable path toward AI-augmented neurological care" |
| Supplementary | Minimal | Extensive (full tool specs, all prompts, extended results) |
| Writing | Dense, technical | Narrative, accessible to both ML and clinical audiences |
| Reproducibility | Code release | Code + benchmark + prompts + evaluation framework |
