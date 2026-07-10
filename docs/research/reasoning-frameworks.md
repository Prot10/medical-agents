# Structured Reasoning Frameworks for NeuroAgent
### State-of-the-art survey and three proposals to move beyond ReAct

*Research memo · 2026-05-22 · companion file: `references.bib` (80 verified citations)*

> **Purpose.** NeuroAgent currently reasons with a linear ReAct loop. This document surveys the state of the art in structured / graph-based reasoning — across LLM agents, medical diagnostic AI, classic Bayesian and model-based diagnosis, and the cognitive science of clinical reasoning — and proposes **three concrete reasoning frameworks** to replace ReAct, each with the evidence for *why it should work*, *how to build it inside the existing codebase*, and *how it couples with model fine-tuning*.

---

## Table of contents

1. [Executive summary](#1-executive-summary)
2. [Why move beyond ReAct — the problem](#2-why-move-beyond-react--the-problem)
3. [How to read the survey (scoring rubric)](#3-how-to-read-the-survey-scoring-rubric)
4. [Survey of approaches](#4-survey-of-approaches)
   - 4.1 [General LLM reasoning & agent frameworks](#41-general-llm-reasoning--agent-frameworks)
   - 4.2 [Medical & clinical diagnostic AI](#42-medical--clinical-diagnostic-ai)
   - 4.3 [Graph, Bayesian, decision-theoretic & "other-field" diagnosis](#43-graph-bayesian-decision-theoretic--other-field-diagnosis)
   - 4.4 [Cognitive science of clinical reasoning](#44-cognitive-science-of-clinical-reasoning)
5. [Synthesis — eight design principles](#5-synthesis--eight-design-principles)
6. [The three proposals](#6-the-three-proposals)
   - 6.1 [Proposal A — Diagnostic Hypothesis Graph (DHG)](#proposal-a--diagnostic-hypothesis-graph-dhg)
   - 6.2 [Proposal B — Deliberate Search over Diagnostic Trajectories](#proposal-b--deliberate-search-over-diagnostic-trajectories)
   - 6.3 [Proposal C — Multi-Agent Clinical Panel on a Shared Graph Blackboard](#proposal-c--multi-agent-clinical-panel-on-a-shared-graph-blackboard)
7. [How the three fit together + recommended roadmap](#7-how-the-three-fit-together--recommended-roadmap)
8. [Coupling the framework with fine-tuning](#8-coupling-the-framework-with-fine-tuning)
9. [Evaluation for the Nature MI paper](#9-evaluation-for-the-nature-mi-paper)
10. [Relevancy scoreboard](#10-relevancy-scoreboard)
11. [References](#11-references)

---

## 1. Executive summary

**The problem.** NeuroAgent's ReAct loop (`agent/orchestrator.py`, ≤15 turns) holds *no structured state*. Patient facts, the 12 tools' outputs, and the differential diagnosis all live as free text in a flat, ever-growing message list. There is no hypothesis object, no calibrated belief, no principled test-selection or stopping rule, and the final diagnosis is regex-extracted markdown. This is a poor fit for diagnosis, which is fundamentally **the management of a probability-weighted differential under sequential, costly evidence-gathering** — and it reproduces the two error modes that the medical-error literature blames for most misdiagnosis: *premature closure* and *anchoring* ([Graber et al., 2005](https://doi.org/10.1001/archinte.165.13.1493); [Croskerry, 2009](https://doi.org/10.1097/ACM.0b013e3181ace703)).

**The opportunity.** The field has converged, in 2024–2025, on exactly this direction. Microsoft's [MAI-DxO](https://arxiv.org/abs/2506.22405) runs a *Bayesian probability-ranked differential* with cost-aware, discrimination-maximising test selection and reaches 80% on NEJM cases vs. 20% for generalist physicians — but it uses persona free-text, **not an explicit graph**. [MedKGI](https://arxiv.org/abs/2512.24181), [LA-CDM](https://arxiv.org/abs/2506.13474) and [MindMap](https://aclanthology.org/2024.acl-long.558/) each add a piece (structured state, hypothesis+uncertainty, KG-grounded graph reasoning) but none unifies them into a persistent, typed, probabilistic graph that drives a multi-tool workup. **That white space is NeuroAgent's contribution.**

**The three proposals** (detailed in §6; they are *layered, not competing*):

| # | Proposal | One-line | Relevance |
|---|----------|----------|:---------:|
| **A** | **Diagnostic Hypothesis Graph (DHG)** | A persistent, typed, probabilistic graph — findings, hypotheses, tests, evidence — that *is* working memory, reasoning substrate, and explanation; test selection by cost-aware Value of Information. | **9.6 / 10** |
| **B** | **Deliberate Search over Diagnostic Trajectories** | Monte-Carlo Tree Search (LATS-style) over diagnostic paths with backtracking, value-guided lookahead, and self-reflection — and a *data engine* for fine-tuning. | **8.6 / 10** |
| **C** | **Multi-Agent Clinical Panel on a Shared Graph Blackboard** | A panel of specialist agents (Diagnostician, Workup Planner, Skeptic, Protocol Officer, Cost Steward, Moderator) reading/writing the DHG as a shared blackboard, with complexity-adaptive escalation. | **8.2 / 10** |

**Recommendation.** Build **A first** — it is the substrate everything else needs, the highest-relevance and most novel piece, and the cleanest fine-tuning target. Then add **C** (cheaply reuses the existing hospital-rules and `CostTracker` assets and adds the debiasing story). Use **B** mainly *offline* as the trajectory-generation engine that produces fine-tuning data, and online only for the hardest cases. A maximal system is **C's panel deliberating over A's graph, with B's lookahead on demand.**

---

## 2. Why move beyond ReAct — the problem

### 2.1 What NeuroAgent does today

From the codebase (`agent/orchestrator.py`, `tools/`, `evaluation/`, `packages/neuroagent-schemas/`):

- **Loop.** `AgentOrchestrator.run()` iterates ≤15 turns. Each turn calls the LLM with the *entire* message list; if the response has tool calls they are executed and appended, otherwise the loop breaks.
- **Memory.** `_build_initial_messages()` produces `[system, user]` and every turn *appends* assistant / tool / reflection messages. The conversation is a **flat, monotonically growing transcript**. There is no structured state object.
- **ReAct phases** are message roles only: THINK = assistant text, ACT = `tool_calls`, OBSERVE = `tool` messages (`json.dumps` of a `ToolResult`), REFLECT = a templated user message.
- **Differential.** *There is no differential data structure.* The working differential exists only as prose inside the LLM's thoughts; the final diagnosis is the `### Primary Diagnosis … ` markdown block extracted by a regex. The only "confidence" is a free-text string `(Confidence: 0.92)`.
- **Cost.** `CostTracker` computes a per-tool cost *after* execution and stores it on the `ToolResult` — it is recorded but **never feeds the agent's decision**.
- **Stopping.** The loop stops when the LLM emits no tool call — "enough evidence" is a vibe.

The good news for redesign: the **tool layer** (`BaseTool`, `ToolCall`, `ToolResult`, all 12 tools, `MockServer`), `CostTracker`, `RulesEngine`, `AgentTrace`, the `NeuroBenchCase`/`GroundTruth` schemas, and `MetricsCalculator` are all **fully decoupled from the loop**. Any new reasoning topology can reuse them unchanged.

### 2.2 Nine failure modes of linear ReAct for diagnosis

| # | Failure mode | Consequence |
|---|--------------|-------------|
| 1 | **Unstructured memory** — facts, tool outputs, differential all flat text. | Nothing can be queried; "what do I believe and how strongly?" is unanswerable. |
| 2 | **No explicit hypothesis tracking** — no differential object. | Diagnosis *is* differential management; ReAct simply doesn't represent the central object. |
| 3 | **No calibrated belief** — only a free-text confidence string. | Verbalised LLM confidence is consistently over-confident and poorly calibrated. |
| 4 | **Linear, no backtracking** — the transcript only grows. | A wrong early interpretation poisons every later turn; no clean revision. |
| 5 | **Greedy, un-principled test selection** — next tool from a free-text thought. | No notion of discriminating power or value of information; cost is ignored. |
| 6 | **No principled stopping rule** — stops when the LLM stops calling tools. | Simultaneously risks premature closure *and* over-testing. |
| 7 | **Context bloat** — verbose MRI/EEG/CSF JSON accumulates across 15 turns. | Salient findings get buried ("lost-in-the-middle"; cf. [MedRAG](https://arxiv.org/abs/2402.13178)). |
| 8 | **Anchoring & confirmation** — nothing structurally preserves alternatives. | The model follows its own earlier thoughts; the reflection prompt asks but cannot enforce. |
| 9 | **Opaque, unauditable output** — the "reasoning" *is* the transcript. | No artifact a clinician can inspect or a trainer can supervise step-by-step. |

### 2.3 Mapping to the diagnostic-error literature

This is not a generic software critique — it maps precisely onto the documented epidemiology of human diagnostic error. [Graber et al. (2005)](https://doi.org/10.1001/archinte.165.13.1493) found cognitive factors in 74% of diagnostic errors, with **premature closure** ("failure to continue generating alternatives") the single most common — that is failure modes 2, 6 and 8. [Croskerry's (2009)](https://doi.org/10.1097/ACM.0b013e3181ace703) dual-process model identifies the missing safeguard: a **metacognitive calibrator** that overrides fast pattern-matching when uncertainty is high — NeuroAgent has no such escalation logic. A reasoning framework that *structurally* keeps the differential alive, tracks calibrated belief, and stops on a decision-theoretic rule is therefore not just an engineering upgrade; it is a *de-biasing architecture*.

### 2.4 Design requirements for the replacement

Any successor must satisfy:

- **R1** — an explicit, persistent, inspectable diagnostic state (not a transcript);
- **R2** — first-class hypotheses as objects carrying calibrated belief;
- **R3** — principled, cost-aware test selection (Value of Information);
- **R4** — a principled stopping rule;
- **R5** — structural defences against premature closure and anchoring;
- **R6** — structured, auditable output and explanation;
- **R7** — decomposition into small, supervisable sub-decisions (to enable fine-tuning);
- **R8** — reuse of the existing tool layer, `CostTracker`, hospital rules, `MockServer`, and NeuroBench.

Each proposal in §6 is annotated with the requirements it satisfies.

---

## 3. How to read the survey (scoring rubric)

Every work in §4 carries a **relevance score (1–10)**: *how directly this work should shape NeuroAgent's next-generation reasoning framework.*

| Score | Meaning |
|:-----:|---------|
| **9–10** | **Core blueprint** — adopt or adapt directly into the design. |
| **7–8** | **Strong influence** — a major component, mechanism, or principle. |
| **5–6** | **Useful** — a reusable technique, substrate, or informative baseline. |
| **3–4** | **Background** — foundational context or a comparison point. |
| **1–2** | **Peripheral** — tangential. |

Pivotal works receive a **★ spotlight** with extended discussion.

---

## 4. Survey of approaches

### 4.1 General LLM reasoning & agent frameworks

The trajectory of this field is itself the argument: **chain → tree → graph → search**, plus **memory** and **verification**. Each step adds a structural capability ReAct lacks.

| Approach | Venue · Year | Core idea → relevance to NeuroAgent | Score |
|----------|-------------|--------------------------------------|:-----:|
| [ReAct](https://arxiv.org/abs/2210.03629) | ICLR 2023 | Interleaves Thought/Action/Observation in one linear loop. **NeuroAgent's current backbone** — the baseline being replaced; understand its limits (§2). | 6 |
| [Chain-of-Thought](https://arxiv.org/abs/2201.11903) | NeurIPS 2022 | Intermediate reasoning steps elicited in-context. Foundational; every successor is measured against it. | 4 |
| [Self-Consistency](https://arxiv.org/abs/2203.11171) | ICLR 2023 | Sample many reasoning paths, marginalise by majority vote. A cheap route to **calibrated belief** (sample-consistency is the best-discriminating uncertainty proxy in medicine). | 6 |
| [Tree of Thoughts](https://arxiv.org/abs/2305.10601) | NeurIPS 2023 | Search over a tree of thoughts with an LLM state-evaluator; BFS/DFS, lookahead, backtracking. Direct structural ancestor of **Proposal B**. | 8 |
| ★ [Graph of Thoughts](https://arxiv.org/abs/2308.09687) | AAAI 2024 | Reasoning as an *arbitrary graph*: thoughts are vertices, dependencies are edges; supports aggregation, refinement, feedback loops. Direct substrate inspiration for **Proposal A**. | 9 |
| ★ [LATS](https://arxiv.org/abs/2310.04406) | ICML 2024 | Monte-Carlo Tree Search unifying reasoning + acting + planning; LLM as policy, value, and self-reflector. The core of **Proposal B**. | 9 |
| [Reflexion](https://arxiv.org/abs/2303.11366) | NeurIPS 2023 | Verbal self-reflection stored in episodic memory drives retry. A debiasing primitive for **Proposal B** and a per-case learning loop. | 7 |
| [ReWOO](https://arxiv.org/abs/2305.18323) | preprint 2023 | Decouples planning from observation: plan all tool calls up front, execute, then solve. Cuts token cost ~5×; dependency-graph view of a workup. | 6 |
| [Cumulative Reasoning](https://arxiv.org/abs/2308.04371) | TMLR 2024 | Builds a **DAG of *verified* propositions** via Proposer/Verifier/Reporter roles. Close cousin of Proposal A's graph + a verifier step against hallucinated edges. | 7 |
| [CoALA](https://arxiv.org/abs/2309.02427) | TMLR 2024 | Cognitive-architecture taxonomy: working vs. episodic/semantic/procedural memory; internal vs. external actions. The vocabulary that *names* what NeuroAgent lacks. | 8 |
| [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) | ICLR 2024 | **Process reward models** (step-level supervision) beat outcome-only reward. The key to supervising graph operations for fine-tuning (R7). | 8 |
| [Self-Refine](https://arxiv.org/abs/2303.17651) | NeurIPS 2023 | One model generates → critiques → revises. The critique loop behind Proposal C's Skeptic and an internal-consistency check. | 6 |
| [Multi-agent debate](https://arxiv.org/abs/2305.14325) | ICML 2024 | Independent model instances debate to consensus; improves factuality & calibration. Evidence base for **Proposal C**. | 7 |
| [AlphaLLM](https://arxiv.org/abs/2404.12253) | NeurIPS 2024 | Self-improvement via imagination + MCTS (ηMCTS) + critics (value/PRM/ORM). Template for the search-to-train loop in Proposal B / §8. | 7 |
| [rStar-Math](https://arxiv.org/abs/2501.04519) | preprint 2025 | Small models reach o1-level maths via self-evolved MCTS + a process preference model. Proof a fine-tuned **small** model can rival frontier models — NeuroAgent's fine-tuning thesis. | 7 |
| [Buffer of Thoughts](https://arxiv.org/abs/2406.04271) | NeurIPS 2024 | A reusable "meta-buffer" of thought-templates. Maps to a **library of illness-script / workup templates** keyed by presentation. | 6 |
| [ADaPT](https://arxiv.org/abs/2311.05772) | NAACL-F 2024 | Recursively decompose a task *only when* the model fails it. Motivates the complexity-adaptive routing in Proposal C. | 6 |
| [MemGPT](https://arxiv.org/abs/2310.08560) | preprint 2023 | OS-style tiered memory with LLM-controlled paging. Architectural blueprint for NeuroAgent's longitudinal patient memory. | 6 |
| [Generative Agents](https://arxiv.org/abs/2304.03442) | UIST 2023 | Memory stream + recency/importance/relevance retrieval + periodic reflection. Belief-state maintenance ReAct lacks. | 6 |
| [Plan-and-Solve](https://arxiv.org/abs/2305.04091) | ACL 2023 | Explicit plan-then-execute; auditable. Background for a planned workup. | 5 |
| [rStar](https://arxiv.org/abs/2408.06195) | preprint 2024 | Generator–discriminator self-play via MCTS without a stronger teacher. Background for Proposal B. | 6 |
| [Algorithm of Thoughts](https://arxiv.org/abs/2308.10379) | ICML 2024 | Embeds search-algorithm exemplars in-context to get tree-like exploration in one query. Token-efficient alternative to explicit search. | 4 |
| [Least-to-Most](https://arxiv.org/abs/2205.10625) | ICLR 2023 | Decompose into easy→hard sub-problems. Background for staged workup. | 4 |
| [Toolformer](https://arxiv.org/abs/2302.04761) | NeurIPS 2023 | Self-supervised learning of when to call tools. Foundational tool-use context. | 4 |
| [Voyager](https://arxiv.org/abs/2305.16291) | preprint 2023 | Lifelong agent with a growing executable skill library. The "skill library" idea ≈ reusable workup templates. | 5 |
| [Survey: LLM autonomous agents](https://arxiv.org/abs/2308.11432) | Front. Comp. Sci. 2024 | Profile/Memory/Planning/Action taxonomy. Useful for positioning the NeuroAgent paper. | 4 |

> **★ Graph of Thoughts (Besta et al., AAAI 2024).** GoT is the formal generalisation of chain (CoT), set (Self-Consistency) and tree (ToT) reasoning into an *arbitrary directed graph* where vertices are "thoughts" and edges are dependencies, with operations to **generate, aggregate, refine and score**. It beats ToT by 62% on its benchmark task while cutting cost >31%. For NeuroAgent this is decisive: patient findings, tool results and diagnostic hypotheses map onto typed vertices; "aggregate" is exactly the clinical act of synthesising MRI + EEG + CSF into one judgment; feedback loops let a hypothesis be *revised* when a later result contradicts it. GoT proves that LLMs can both **construct and reason over** a graph — the technical premise of Proposal A.

> **★ LATS (Zhou et al., ICML 2024).** LATS casts agent decision-making as **Monte-Carlo Tree Search**: nodes are states (accumulated actions + observations + reflections), the LLM serves as policy, value function *and* self-reflector, and backpropagation spreads value estimates. It unifies ToT's search, ReAct's grounded acting, and Reflexion's self-critique, and reaches 92.7% pass@1 on HumanEval. Diagnosis is a sequential decision problem under uncertainty (formally a POMDP) — MCTS is its natural solver. LATS is the most complete *drop-in successor* to NeuroAgent's ReAct loop and the engine of Proposal B.

### 4.2 Medical & clinical diagnostic AI

#### 4.2a LLM-era diagnostic agents and reasoning (2023–2026)

| Approach | Venue · Year | Core idea → relevance to NeuroAgent | Score |
|----------|-------------|--------------------------------------|:-----:|
| ★ [MAI-DxO / Sequential Diagnosis](https://arxiv.org/abs/2506.22405) | Microsoft, 2025 | A 5-persona panel — *Dr. Hypothesis* (Bayesian ranked differential), *Dr. Test-Chooser* (discriminating tests), *Dr. Challenger* (devil's advocate), *Dr. Stewardship* (cost), *Dr. Checklist* (QC) — on stepwise NEJM cases. 80% vs. 20% physicians; −70% cost vs. bare o3. **The closest prior art and the bar to beat.** | **10** |
| ★ [MDAgents](https://arxiv.org/abs/2404.15155) | NeurIPS 2024 (oral) | *Complexity-adaptive* collaboration: solo agent for easy cases, multi-disciplinary team for hard ones. Directly shapes Proposal C's adaptive escalation. | 9 |
| ★ [MindMap](https://aclanthology.org/2024.acl-long.558/) | ACL 2024 | LLM + medical KG produce an explicit **graph-of-thoughts** reasoning trace; cuts hallucination. Closest existing graph-reasoning system for medicine — Proposal A prior art. | 9 |
| ★ [Chain-of-Diagnosis](https://arxiv.org/abs/2407.13301) | preprint 2024 | Formalises diagnosis as a 5-step chain ending in a **confidence distribution** over diseases; uses confidence *entropy* to decide whether to gather more. A ready stopping signal for Proposal A. | 9 |
| ★ [LA-CDM](https://arxiv.org/abs/2506.13474) | preprint 2025 | Hypothesis-driven agent: maintains hypotheses + per-hypothesis uncertainty, requests tests iteratively; trained with **SFT + RL** on three objectives (hypothesis accuracy, uncertainty, efficiency). Validates Proposal A's loop *and* the §8 fine-tuning plan. | 9 |
| ★ [MedKGI](https://arxiv.org/abs/2512.24181) | preprint 2025 | KG-grounded iterative DDx with **information-gain question selection** and an OSCE-format **structured state** across turns. The closest published analogue to a "diagnostic hypothesis graph". | 9 |
| [AMIE (diagnostic)](https://www.nature.com/articles/s41586-025-08866-7) | Nature 2025 | LLM optimised for diagnostic dialogue via self-play; inference-time chain-of-reasoning; beat PCPs on 30/32 axes in a blinded OSCE RCT. Gold-standard evaluation methodology. | 8 |
| [MedAgents](https://aclanthology.org/2024.findings-acl.33/) | ACL-F 2024 | Zero-shot multi-disciplinary specialist role-play with collaborative discussion to consensus. Evidence base for Proposal C's roles. | 8 |
| [HuatuoGPT-o1](https://arxiv.org/abs/2412.18925) | preprint 2024 | o1-style medical reasoning model trained with **verifiable rewards** (a medical verifier) — SFT then RL. The concrete recipe for §8. | 8 |
| [AgentClinic](https://arxiv.org/abs/2405.07960) | npj Digit. Med. 2026 | Simulated clinical environment; static-QA accuracy *collapses* (sometimes >90%) in sequential interactive mode. Validates building NeuroBench around sequential tool use; injects cognitive bias. | 7 |
| [DR.KNOWS](https://arxiv.org/abs/2308.14321) | 2023 / JMIR AI 2025 | UMLS-derived diagnostic graph with 108 physician-curated relations; multi-hop paths injected into the LLM. Methodology for building a neurology-focused KG. | 7 |
| [MedReason](https://arxiv.org/abs/2504.00993) | preprint 2025 | KG-grounded "thinking-path" dataset (32k chains) for fine-tuning factual medical reasoning. A data-generation recipe for §8. | 7 |
| [AMIE (multimodal)](https://arxiv.org/abs/2505.04653) | Nature Medicine 2025 | State-aware dialogue with **uncertainty-driven phase transitions** across history → DDx → follow-up; ingests images/ECG/PDF. Phase logic ≈ Proposal A's stage transitions. | 6 |
| [AMIE (management)](https://arxiv.org/abs/2503.06074) | preprint 2025 | Separates a Dialogue Agent from a Management-Reasoning Agent; longitudinal multi-visit reasoning. Argues for persistent patient state. | 6 |
| [Towards accurate DDx (DDx-LLM)](https://arxiv.org/abs/2312.00164) | preprint 2023 | LLM DDx assistant; top-10 accuracy 59% vs. 33% unassisted clinicians; **structured input formatting matters**. Co-pilot framing + input-format lesson. | 6 |
| [KARE](https://arxiv.org/abs/2410.04585) | ICLR 2025 | KG **community-level** retrieval for clinical prediction; +10–15% on MIMIC. Scalable knowledge-retrieval module. | 6 |
| [MedRAG (KG-elicited)](https://arxiv.org/abs/2502.04413) | WWW 2025 | Four-tier hierarchical diagnostic KG (category → disease → feature → differentiator) drives DDx + follow-up questions. A concrete KG schema. | 6 |
| [Med-R1](https://arxiv.org/abs/2503.13939) | preprint 2025 | GRPO reinforcement learning for medical vision-language reasoning; a 2B model beats 72B baselines. RL-efficiency evidence for §8. | 6 |
| [O1 Replication Journey, Part 3](https://arxiv.org/abs/2501.06458) | preprint 2025 | Inference-time scaling helps *most* on the hardest medical cases; **~500 supervised examples suffice**. Implies NeuroBench (600 cases; 500 in the train split) is enough for reasoning-model SFT. | 6 |
| [MedAgentBench](https://arxiv.org/abs/2501.14654) | NEJM AI 2025 | FHIR-compliant virtual-EHR benchmark; best model 69.7%. Tool-use planning is the bottleneck; benchmark-design template. | 6 |
| [MedRAG / MIRAGE](https://arxiv.org/abs/2402.13178) | preprint 2024 | RAG benchmark + toolkit for medicine; "lost-in-the-middle" effect. Informs the `search_medical_literature` tool. | 5 |
| [MedAgentsBench](https://arxiv.org/abs/2503.07459) | preprint 2025 | Hard multi-step medical-reasoning benchmark; search-based agents give the best cost/accuracy ratio. Eval-design reference. | 5 |
| [KG4Diagnosis](https://arxiv.org/abs/2412.16833) | preprint 2024 | Hierarchical GP→specialist multi-agent framework with automated KG construction (362 diseases). A Proposal C variant. | 6 |
| [GPT-4 on NEJM CPCs (Kanjee)](https://doi.org/10.1001/jama.2023.8288) | JAMA 2023 | GPT-4 names the diagnosis in 64% (top-1 39%) of the hardest cases — *no tools*. Upper-bound baseline. | 5 |
| [GPT-4 on complex cases (Eriksen)](https://ai.nejm.org/doi/full/10.1056/AIp2300031) | NEJM AI 2024 | GPT-4 outperformed 99.98% of journal readers. NeuroAgent's value must be tools + structure + auditability, not raw accuracy. | 5 |
| [Survey: LLM agents in medicine](https://arxiv.org/abs/2502.11211) | ACL-F 2025 | 60-study taxonomy; hallucination + non-standard evaluation are the top barriers. Positioning + gap analysis. | 4 |

#### 4.2b Classic medical diagnostic expert systems — the precedents

These 1976–1992 systems already did *structured, probabilistic, decision-theoretic* diagnosis. The LLM era is, in part, a rediscovery — and these establish that the approach **works** and **matches experts**.

| System | Venue · Year | Core idea → relevance to NeuroAgent | Score |
|--------|-------------|--------------------------------------|:-----:|
| ★ [Pathfinder](https://pubmed.ncbi.nlm.nih.gov/1635470/) | Methods Inf. Med. 1992 | Bayesian network for lymph-node pathology that computes posteriors **and the value of information** of each unobserved feature to guide the workup. Matched/beat expert pathologists. Direct blueprint for Proposal A's test selection. | 9 |
| [QMR-DT](https://pubmed.ncbi.nlm.nih.gov/1762578/) | Methods Inf. Med. 1991 | Reformulated INTERNIST-1/QMR as a two-level noisy-OR **Bayesian belief network** (~600 diseases × ~4,500 findings). The probabilistic ancestor of the hypothesis graph. | 8 |
| [INTERNIST-1 / QMR](https://www.nejm.org/doi/full/10.1056/NEJM198208193070803) | NEJM 1982 | Competitive hypothesis scoring with an **"explain-away"** mechanism; struggled with multi-disease cases — motivating probabilistic and graph successors. | 7 |
| [MYCIN](https://www.shortliffe.net/Shortliffe-1976/MYCIN%20thesis%20Book.htm) | book 1976 | Rule-based diagnosis with certainty factors and, crucially, **backward-chaining explanation**. Explanation-by-construction is a requirement (R6). | 6 |
| [DXplain](https://jamanetwork.com/journals/jama/article-abstract/367025) | JAMA 1987 | Scored DDx representing both **supporting and opposing** evidence per disease. Absence of a finding is as informative as presence — a signed-edge requirement for Proposal A. | 6 |

> **★ MAI-DxO (Nori et al., Microsoft, 2025) — the central reference.** MAI-DxO turns 304 NEJM clinicopathological cases into *stepwise* encounters where an agent must iteratively query a gatekeeper. Its orchestrator simulates five physician personas: **Dr. Hypothesis** maintains a probability-ranked top-3 differential updated *in a Bayesian manner* after each finding; **Dr. Test-Chooser** picks ≤3 tests per round that *maximally discriminate* the leading hypotheses; **Dr. Challenger** is a devil's advocate against anchoring; **Dr. Stewardship** enforces cost-conscious care; **Dr. Checklist** does silent QC. The panel deliberates and commits only when "certainty exceeds threshold." Result: **80%** vs. 20% for generalist physicians, at **lower cost**. Two things matter for NeuroAgent. (1) It is overwhelming validation of the proposed direction — Bayesian differential + discrimination-driven, cost-aware test selection + an explicit skeptic. (2) Its differential and deliberation live in **persona free-text, with no explicit graph** — so it inherits ReAct's unstructured-memory and auditability weaknesses. **Replacing the persona text with an explicit, typed, persistent graph (Proposal A) is a genuine, publishable advance over the current state of the art**, not a reimplementation of it.

> **★ Pathfinder (Heckerman, Horvitz & Nathwani, 1992) — the decision-theoretic core.** Pathfinder is a "normative" expert system: a Bayesian network over 60+ diseases and 100+ features that, after each observation, computes the **value of information** (value of clairvoyance) of every *un*observed feature and surfaces the highest-value ones. It is the historical proof that posterior tracking + VOI test selection = expert-level diagnosis. NeuroAgent's `CostTracker` already supplies the denominator; the missing numerator is expected information gain. Proposal A is, in essence, "Pathfinder, but the LLM constructs and updates the network dynamically for any neurological presentation."

### 4.3 Graph, Bayesian, decision-theoretic & "other-field" diagnosis

Diagnosis-as-structured-reasoning is also a mature field in statistics, classic AI, and engineering fault diagnosis — the "other fields" worth borrowing from.

| Approach | Venue · Year | Core idea → relevance to NeuroAgent | Score |
|----------|-------------|--------------------------------------|:-----:|
| ★ [Richens et al. — causal diagnosis](https://www.nature.com/articles/s41467-020-17419-7) | Nature Comms 2020 | Reframes diagnosis as **counterfactual** inference ("which disease, if removed, best explains recovery?"); the causal algorithm reached the top 25% of doctors vs. top 48% for the associative one. Justifies causal edges in Proposal A. | 8 |
| ★ [HEARSAY-II blackboard](https://doi.org/10.1145/356810.356816) | ACM Comp. Surv. 1980 | Many independent knowledge sources cooperate *only* via a shared, structured "blackboard." The architectural template for Proposal C. | 8 |
| [Pearl — Bayesian networks](https://dl.acm.org/doi/book/10.5555/534975) | book 1988 | Belief propagation, d-separation, and **"explaining away"** in probabilistic graphical models. The formal inference engine behind a hypothesis graph. | 7 |
| [Reiter — diagnosis from first principles](https://doi.org/10.1016/0004-3702(87)90062-2) | Artif. Intell. 1987 | Diagnosis as **logical consistency**: a diagnosis is a minimal set of abnormal components consistent with observations. Handles multi-fault (comorbidity) cleanly. | 7 |
| [de Kleer & Williams — multiple faults](https://doi.org/10.1016/0004-3702(87)90063-4) | Artif. Intell. 1987 | Conflict sets + **minimal hitting sets** enumerate multi-fault diagnoses without blow-up. The dangerous comorbidity case, formalised. | 7 |
| [Naghshvar & Javidi — active hypothesis testing](https://arxiv.org/abs/1203.4626) | Ann. Statist. 2013 | Information-theoretically optimal **sequential** test selection: pick the test maximising expected uncertainty reduction. The theory under Proposal A's VOI policy. | 7 |
| [Think-on-Graph](https://arxiv.org/abs/2307.07697) | ICLR 2024 | LLM agent does beam search over a knowledge graph, grounding each step in KG triples. How to navigate a medical KG as a reasoning act. | 7 |
| [Fansi Tchango et al. — trustworthy diagnosis](https://arxiv.org/abs/2210.07198) | NeurIPS 2022 | Deep-RL agent that maintains a **ranked differential**, is rewarded for exploring severe pathologies early, and is scored on interaction quality. The "can't-miss" utility asymmetry. | 7 |
| [PrimeKG](https://www.nature.com/articles/s41597-023-01960-3) | Sci. Data 2023 | Precision-medicine KG: 17k diseases, 4M relations across 10 scales. Candidate background-knowledge substrate. | 7 |
| [UMLS](https://doi.org/10.1093/nar/gkh061) | Nucleic Acids Res. 2004 | 2M+ biomedical concepts, 12M relations across 60+ vocabularies. Concept-normalisation layer for grounding tool outputs. | 7 |
| [REFUEL](https://proceedings.neurips.cc/paper/2018/hash/b5a1d925221b37e2e399f7b319038ba0-Abstract.html) | NeurIPS 2018 | RL for sequential symptom acquisition with **reward shaping by information gain**. A concrete recipe for training a test-selection policy (§8). | 6 |
| [GraphRAG](https://arxiv.org/abs/2404.16130) | preprint 2024 | KG extraction + hierarchical community summaries for global-sensemaking retrieval. Pattern for the literature/protocol knowledge layer. | 6 |
| [Reasoning on Graphs (RoG)](https://arxiv.org/abs/2310.01061) | ICLR 2024 | Plan KG-grounded relation paths, then retrieve and reason — faithful and interpretable. Plan-then-verify over a KG. | 6 |
| [Hetionet](https://elifesciences.org/articles/26726) | eLife 2017 | Open heterogeneous biomedical network; metapath reasoning. Lightweight KG option. | 5 |
| [SPOKE](https://academic.oup.com/bioinformatics/article/39/2/btad080/7033465) | Bioinformatics 2023 | 27M-node biomedical KG with an EHR-embedding pathway. KG option with patient-alignment. | 5 |

| Argumentation | Venue · Year | Core idea → relevance to NeuroAgent | Score |
|---------------|-------------|--------------------------------------|:-----:|
| [ArgMed-Agents](https://arxiv.org/abs/2403.06294) | preprint 2024 | LLM agents build a **conflict graph** of clinical arguments resolved by formal argumentation semantics; explainable. Closest argument-graph clinical system — a Proposal A/C hybrid prior art. | 8 |
| [Dung — abstract argumentation](https://doi.org/10.1016/0004-3702(94)00041-X) | Artif. Intell. 1995 | Arguments + attacks as a graph; "acceptable" extensions under conflict. Formalism for handling contradictory evidence and reinstatement. | 6 |
| [ASPIC+](https://doi.org/10.1080/19462166.2013.869766) | Argument & Comp. 2014 | Structured argumentation with strict + **defeasible** rules. A principled way to encode hospital protocols as defeasible rules. | 6 |
| [Sassoon et al. — argumentation schemes for CDS](https://doi.org/10.3233/AAC-200550) | Argument & Comp. 2021 | Clinical inference templates with "critical questions" evaluated under Dung semantics. Auditable, guideline-grained reasoning. | 6 |

> **★ HEARSAY-II & the blackboard model (Erman et al., 1980).** HEARSAY-II solved speech understanding with many specialist "knowledge sources" that never call each other — they only read and write a shared, layered **blackboard**, with a scheduler controlling focus. This is the cleanest known architecture for "multiple experts, one shared structured state," and it is exactly the shape of Proposal C: each diagnostic tool and each specialist agent is a knowledge source; the **Diagnostic Hypothesis Graph is the blackboard**; the Workup Planner is the scheduler. A 1980 architecture is, somewhat remarkably, the right one — provided the blackboard is a typed graph and the knowledge sources are LLM agents.

### 4.4 Cognitive science of clinical reasoning

The *why* layer. These four works describe how expert clinicians actually reason — and so define what a faithful framework should imitate.

| Work | Venue · Year | Core idea → relevance to NeuroAgent | Score |
|------|-------------|--------------------------------------|:-----:|
| ★ [Elstein et al. — hypothetico-deductive reasoning](#11-references) | book 1978 | Verbal-protocol studies show experts generate **4–5 hypotheses early** from cues, then run a test-and-revise cycle to discriminate them. The cognitive blueprint for Proposal A's loop and its *bounded* hypothesis set. | 9 |
| ★ [Schmidt, Norman & Boshuizen — illness scripts](#11-references) | Acad. Med. 1990 | Expertise = knowledge *organisation*: compact **illness scripts** (enabling conditions, fault/pathophysiology, consequences). Defines the *content* of a `HypothesisNode`. | 9 |
| [Croskerry — dual-process model](https://doi.org/10.1097/ACM.0b013e3181ace703) | Acad. Med. 2009 | System 1 (fast pattern-matching) + System 2 (slow analytic) + a **metacognitive calibrator** that overrides System 1. Specifies fast hypothesis-seeding, deliberate VOI/search, and an escalation rule. | 8 |
| [Graber et al. — diagnostic error](https://doi.org/10.1001/archinte.165.13.1493) | Arch. Intern. Med. 2005 | Cognitive factors in 74% of errors; **premature closure** is the most common. The failure-mode specification a framework must structurally prevent. | 8 |

> **★ Hypothetico-deduction & illness scripts — the cognitive contract.** Two findings from this literature should be hard constraints on the design. First (Elstein): expert reasoning is **hypothesis-first and bounded** — clinicians commit early to a *small* set of candidate diagnoses and then gather data specifically to discriminate them; they do not collect data exhaustively and diagnose at the end. Proposal A's loop (seed 4–7 hypotheses → VOI-driven discrimination → stop) is a direct mechanisation of this. Second (Schmidt): a diagnosis in an expert's mind is an **illness script** — enabling conditions (who gets it), the fault (pathophysiology), and consequences (expected findings and course). That is precisely the recommended schema for a `HypothesisNode`, and it makes each hypothesis node *generative*: it predicts which findings to expect, which is what makes Value-of-Information computable in the first place.

---

## 5. Synthesis — eight design principles

The 80 works converge on a consistent set of principles. A successor to ReAct should:

1. **Make the diagnostic state an explicit, typed, persistent object** — not a transcript. *(GoT, Cumulative Reasoning, CoALA, MedKGI, HEARSAY-II)*
2. **Represent hypotheses as first-class nodes carrying calibrated probability** — a live differential. *(MAI-DxO, Chain-of-Diagnosis, QMR-DT, Pathfinder, Elstein)*
3. **Structure each hypothesis as an illness script** — enabling conditions, fault, expected findings — so it is generative and testable. *(Schmidt et al., DR.KNOWS)*
4. **Select the next test by cost-aware Value of Information**, not greedily. *(Pathfinder, MAI-DxO, Naghshvar–Javidi, REFUEL, MedKGI)*
5. **Stop on a decision-theoretic rule** — posterior dominance, can't-miss coverage, or VOI below cost. *(Chain-of-Diagnosis entropy, Pathfinder, AMIE phase transitions)*
6. **Build in adversarial, anti-anchoring critique** — a structural skeptic and a metacognitive escalator. *(MAI-DxO's Dr. Challenger, Croskerry, Graber, multi-agent debate)*
7. **Make the reasoning artifact the explanation** — auditable by construction. *(MYCIN, MindMap, ArgMed-Agents, Reasoning-on-Graphs)*
8. **Decompose reasoning into small, verifiable sub-decisions** so the policy can be supervised and fine-tuned. *(Let's Verify / PRMs, HuatuoGPT-o1, rStar-Math, MedReason, LA-CDM)*

The three proposals are three ways to *operationalise these eight principles*. Proposal A is the **representation** (principles 1–5, 7–8). Proposal B is a **search control policy** over it (principles 4–6, 8). Proposal C is an **orchestration policy** over it (principles 2, 4, 6–7).

---

## 6. The three proposals

Each is specified as: concept → data/architecture → reasoning loop → why it works (with citations) → how to build it in NeuroAgent → fine-tuning coupling → evaluation → risks → scorecard.

---

### Proposal A — Diagnostic Hypothesis Graph (DHG)

> **Satisfies requirements R1–R8.** *The recommended foundation.*

#### Concept

Replace the flat message list with a **persistent, typed, directed graph** that is, simultaneously, the agent's **working memory**, its **reasoning substrate**, and its **explanation artifact**. The agent no longer "thinks in a transcript"; it performs a small set of *graph operations* — add a hypothesis, attach evidence, update belief, propose a test — and the graph at any moment *is* the complete diagnostic state. The control policy is decision-theoretic: at each step, order the test with the highest **Value of Information per dollar**, and stop on a principled rule. This is the LLM-era realisation of Pathfinder/QMR-DT — but where the LLM *dynamically constructs* the network for any presentation, instead of it being hand-built for one organ.

#### Data model

Five node types and a set of typed, signed, weighted edges (all Pydantic v2 models — consistent with the existing `neuroagent-schemas` package):

```text
FindingNode      id · text · kind{symptom|sign|history|demographic|exam|vital}
                 · status{present|absent|uncertain} · salience · source{presentation|tool}
HypothesisNode   id · name · icd_hint · prior · posterior(belief 0–1)
                 · status{active|confirmed|excluded|parked} · cant_miss:bool
                 · illness_script{enabling_conditions, fault, expected_findings}
TestNode         id · tool_name · parameters · status{proposed|ordered|resulted}
                 · cost_usd(from CostTracker) · expected_voi
EvidenceNode     id · from_test · salient_features[] · raw_output_ref
ConclusionNode   id · primary · posterior · differential[] · recommendations[] · red_flags[]

Edges (typed):
  explains       HypothesisNode → FindingNode      (this hypothesis accounts for this finding)
  supports/refutes  Evidence|Finding → Hypothesis   signed, weighted by a likelihood-ratio bucket
  discriminates  TestNode → {HypothesisNode}        (this test separates these hypotheses)
  requires       HypothesisNode|Rule → TestNode     (work-up mandated by hypothesis or protocol)
  excludes/co-occurs  Hypothesis ↔ Hypothesis
  caused-by      Finding|Hypothesis → Hypothesis    (causal edge; supports counterfactual queries)
  contraindicates  Finding|Hypothesis → Action      (safety)
```

Critically, **the LLM never does arithmetic.** It proposes *structured, discrete* things — a hypothesis set, a coarse likelihood-ratio bucket (`strong+ / weak+ / neutral / weak− / strong−`), the salient features of a tool report, the plausible results of a candidate test. All numeric belief updates and VOI computations happen in Python. This is what makes the framework reliable *and* supervisable.

#### Reasoning loop (replaces the 15-turn ReAct loop)

1. **Represent.** Parse the patient presentation into `FindingNode`s — structured, vs. today's opaque string.
2. **Generate hypotheses (System 1).** The LLM seeds 4–7 `HypothesisNode`s as illness scripts, *mandatorily including can't-miss diagnoses*, with coarse priors anchored to condition prevalence.
3. **Update belief (System 2).** For each finding/evidence node, the LLM assigns a likelihood-ratio bucket per connected hypothesis; Python updates posteriors in log-odds space (a noisy-OR-style combination, after QMR-DT).
4. **Select a test by VOI.** For each candidate `TestNode`, the LLM estimates the distribution over its possible results; Python computes expected information gain (expected entropy reduction of the posterior) and divides by `CostTracker` cost → **VOI-per-dollar**. Order the arg-max; force protocol-mandated and can't-miss work-up.
5. **Observe.** Execute the tool via the existing `ToolRegistry.execute`; create an `EvidenceNode`; the LLM extracts salient features only (defeating context bloat).
6. **Loop** 3→5 until the stopping rule fires.
7. **Stop** when: the top posterior exceeds a threshold *and* its margin over the second exceeds a threshold; **or** the best remaining VOI-per-dollar falls below a threshold; **or** all can't-miss hypotheses are excluded/addressed; **or** a turn/budget cap is hit.
8. **Conclude.** Emit a structured `ConclusionNode` / `DiagnosisOutput`. The graph *is* the explanation.

#### Why it should work

- **It mechanises how expert clinicians actually reason.** Steps 2→6 are the hypothetico-deductive cycle ([Elstein et al., 1978](#11-references)); `HypothesisNode`s are illness scripts ([Schmidt et al., 1990](#11-references)); the System-1 seed / System-2 update split is Croskerry's dual-process model with the stopping rule as the missing metacognitive calibrator.
- **It is decision-theoretically principled and proven.** Posterior tracking + VOI test selection is exactly [Pathfinder](https://pubmed.ncbi.nlm.nih.gov/1635470/) and [QMR-DT](https://pubmed.ncbi.nlm.nih.gov/1762578/), which matched experts; the VOI rule is information-theoretically optimal ([Naghshvar & Javidi, 2013](https://arxiv.org/abs/1203.4626)). It is also what [MAI-DxO](https://arxiv.org/abs/2506.22405)'s Dr. Hypothesis + Dr. Test-Chooser do — and they reached 80% vs. 20%.
- **It structurally prevents the two dominant error modes.** Because the differential is a *set of persistent nodes with live posteriors*, an alternative cannot be silently dropped — directly countering premature closure and anchoring ([Graber et al., 2005](https://doi.org/10.1001/archinte.165.13.1493)). The stopping rule is explicit, not a vibe.
- **It finally uses the cost data.** `CostTracker` exists but never informs decisions today; VOI-per-dollar makes cost a first-class driver — yielding the "diagnostic accuracy per dollar" story that is MAI-DxO's headline.
- **LLMs demonstrably can build and reason over such graphs.** [Graph of Thoughts](https://arxiv.org/abs/2308.09687), [MindMap](https://aclanthology.org/2024.acl-long.558/) and [Cumulative Reasoning](https://arxiv.org/abs/2308.04371) establish the mechanism; [MedKGI](https://arxiv.org/abs/2512.24181) and [LA-CDM](https://arxiv.org/abs/2506.13474) confirm it works for clinical diagnosis specifically.
- **It is novel against the SOTA.** No published system unifies a *persistent typed probabilistic graph* + *VOI-driven multi-tool workup* + *structured auditable output* — MAI-DxO uses persona text, MindMap is for QA, MedKGI is KG-constrained dialogue. This is the publishable delta.

#### How to build it in NeuroAgent

- New module `agent/graph/` — `DiagnosticGraph`, the node/edge Pydantic models, and the belief/VOI maths in pure Python.
- New `GraphOrchestrator` alongside `AgentOrchestrator`, reusing `ToolRegistry`, `CostTracker`, `RulesEngine`, `MockServer` and `AgentTrace` unchanged (all are loop-agnostic).
- The LLM is called for *discrete structured operations*, each with its **own tight system prompt** (this is where "proper system prompts" lives — a shared base diagnostic stance plus a per-operation instruction: `seed_hypotheses`, `score_evidence`, `estimate_test_outcomes`, `extract_salient_features`, `write_conclusion`).
- A structured `DiagnosisOutput(primary, confidence, differential[], evidence_by_hypothesis, recommendations, red_flags)` model replaces regex-extracted markdown — the codebase review explicitly flags this as needed.
- The graph serialises into `AgentTrace`, so `MetricsCalculator` and `LLMJudge` work as-is, and the existing `web/` dashboard / `web-review/` app can **render the graph** — a natural, compelling visualisation.

#### Coupling with fine-tuning

The DHG turns one hard, unsupervisable "diagnose this patient" task into *dozens of small, structured, verifiable sub-decisions* — exactly the credit-assignment win behind process reward models ([Let's Verify](https://arxiv.org/abs/2305.20050)). Fine-tune the model to (a) seed good hypothesis sets, (b) emit calibrated likelihood-ratio buckets, (c) select high-VOI tests. NeuroBench's `GroundTruth` (primary diagnosis, `optimal_actions`, `critical_actions`, `contraindicated_actions`) supplies a **verifiable reward** for RLVR/GRPO in the style of [HuatuoGPT-o1](https://arxiv.org/abs/2412.18925) and [Med-R1](https://arxiv.org/abs/2503.13939). Calibration can be a *direct training objective* (a proper scoring rule / Brier penalty on the posteriors). [LA-CDM](https://arxiv.org/abs/2506.13474) is an existence proof of exactly this SFT+RL recipe on a hypothesis-driven agent.

#### Evaluation

Keep all current metrics; the graph unlocks new, paper-grade axes: **calibration** (Brier score / ECE on hypothesis posteriors), **can't-miss recall**, **accuracy-per-dollar**, **robustness to red herrings** (NeuroBench `GroundTruth.red_herrings` already exists), and **auditability** (clinician ratings of the graph itself).

#### Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| LLM probability calibration is hard | Coarse LR buckets; numeric updates in Python; fine-tune for calibration; optional self-consistency sampling. |
| Wrong edges / graph-construction errors | A verifier step (Cumulative Reasoning); the Skeptic role from Proposal C audits edges. |
| Hypothesis set too narrow | Mandatory can't-miss seeding; a periodic "broaden the differential" operation. |
| Per-operation LLM-call overhead | Operations are small and cacheable; batch independent ones (ReWOO-style); often cheaper than a 15-turn full-context ReAct loop. |

#### Scorecard

| Relevance | Expected impact | Build effort | Novelty | Paper value | Risk |
|:---------:|:---------------:|:------------:|:-------:|:-----------:|:----:|
| **9.6 / 10** | High | Medium–High | High | High | Medium |

---

### Proposal B — Deliberate Search over Diagnostic Trajectories

> **Satisfies R3–R7; partially R1–R2.** *Best as an offline fine-tuning data engine + a hard-case mode.*

#### Concept

Keep a ReAct-like step as the primitive but wrap the whole diagnostic process in **Monte-Carlo Tree Search** ([LATS](https://arxiv.org/abs/2310.04406)). A search node is a diagnostic *state* (the DHG-so-far, or a lighter summary); actions are *order a test*, *reinterpret evidence*, or *conclude*. The LLM is the **policy** (proposes actions), the **value function** (scores states), and the **self-reflector** ([Reflexion](https://arxiv.org/abs/2303.11366)) on dead-end branches. The search expands, simulates, evaluates and back-propagates value — and, crucially, **backtracks**.

#### Why it should work

- **Diagnosis is a sequential decision problem under uncertainty — formally a POMDP** (hidden state = true disease; actions = tests; observations = results). MCTS is its canonical solver; [LATS](https://arxiv.org/abs/2310.04406) proved it beats ReAct, ToT and Reflexion on decision-making tasks.
- **Lookahead beats greedy.** Test-ordering is combinatorial; a greedy VOI step (Proposal A) is myopic. Search evaluates *sequences* of tests, finding cheaper or safer work-ups a greedy policy misses.
- **Backtracking + reflection directly counter anchoring and premature closure** — the agent can abandon and revisit a path, which a linear transcript cannot.
- **It is the fine-tuning data engine NeuroAgent needs.** Run the search *offline* over NeuroBench: because `MockServer` returns pre-generated outputs, the tree can branch and explore counterfactual test orders *freely*. Each case yields many scored trajectories → SFT on the best, preference/RL on the comparisons — the [rStar-Math](https://arxiv.org/abs/2501.04519) / [AlphaLLM](https://arxiv.org/abs/2404.12253) recipe — then **distil the search into a fast single-pass policy** for deployment. Proposal B *is* the §8 pipeline.
- **Cost in the reward yields cost-efficient work-ups** automatically, leveraging `CostTracker`.

#### How to build it in NeuroAgent

A LATS controller wrapping the `GraphOrchestrator`; `MockServer` powers rollouts; the search tree extends the existing `AgentTrace` (traces are already saved to `data/traces/`). The value function starts as an LLM-as-judge over `GroundTruth`-free heuristics (posterior margin, can't-miss coverage, cost, protocol adherence) and is later replaced by a fine-tuned **process reward model** ([Let's Verify](https://arxiv.org/abs/2305.20050)).

**Honest deployment caveat.** At a real bedside you cannot un-order a test. So *online*, search runs over *interpretation* trajectories and *planned* work-ups before committing — or you simply deploy the distilled single-pass policy. *In the NeuroBench benchmark*, full test-tree search is legitimate because outputs are pre-generated. This makes the benchmark an ideal testbed and training ground; deployment uses the distillate.

#### Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| Many LLM calls per case (compute) | Search **offline** for training; deploy the distilled policy; reserve online search for flagged hard cases. |
| Value-function quality | Bootstrap with LLM-judge; replace with a fine-tuned PRM trained on NeuroBench outcomes. |
| Search ≠ real clinical action | Explicit two-mode design (offline test-search vs. online interpretation-search / distilled policy). |

#### Scorecard

| Relevance | Expected impact | Build effort | Novelty | Paper value | Risk |
|:---------:|:---------------:|:------------:|:-------:|:-----------:|:----:|
| **8.6 / 10** | High (esp. for fine-tuning) | High | Medium–High | High | Medium–High |

---

### Proposal C — Multi-Agent Clinical Panel on a Shared Graph Blackboard

> **Satisfies R1–R8.** *Best second step — cheap reuse of existing assets + the de-biasing story.*

#### Concept

A panel of specialised LLM agents collaborates by reading and writing the **Diagnostic Hypothesis Graph as a shared blackboard** ([HEARSAY-II](https://doi.org/10.1145/356810.356816)). It mirrors a real clinical case conference / tumor board:

| Role | Responsibility | Reuses |
|------|----------------|--------|
| **Diagnostician** | Seeds and updates `HypothesisNode`s; maintains the differential. | — |
| **Workup Planner** | Selects tests by VOI (Proposal A's policy); may invoke Proposal B's lookahead. | `CostTracker` |
| **Skeptic / Devil's Advocate** | Argues *against* the leading hypothesis; raises can't-miss diagnoses; flags anchoring & premature closure. | — |
| **Protocol Officer** | Checks hospital clinical pathways; enforces mandatory / contraindicated steps. | `RulesEngine` + YAML rules |
| **Cost Steward** | Flags low-yield expensive testing; proposes cheaper equivalents. | `CostTracker` + `tool_costs.yaml` |
| **Moderator** | Drives consensus; applies the stopping rule; writes the `ConclusionNode`. | — |

Following [MDAgents](https://arxiv.org/abs/2404.15155), the panel is **complexity-adaptive**: a single agent handles straightforward cases; the full panel convenes only for moderate/`diagnostic_puzzle` cases (NeuroBench already labels `difficulty`).

#### Why it should work

- **It is the proven SOTA structure.** [MAI-DxO](https://arxiv.org/abs/2506.22405) (5 personas, 80% vs. 20%), [MDAgents](https://arxiv.org/abs/2404.15155) (adaptive collaboration, best on 7/10 benchmarks) and [MedAgents](https://aclanthology.org/2024.findings-acl.33/) all show role-decomposed panels beat single agents; [multi-agent debate](https://arxiv.org/abs/2305.14325) improves factuality and calibration.
- **The Skeptic directly attacks the #1 cause of diagnostic error.** A *mandatory, adversarial* role that must falsify the leading hypothesis is a structural de-biasing mechanism against premature closure and anchoring ([Graber](https://doi.org/10.1001/archinte.165.13.1493); [Croskerry](https://doi.org/10.1097/ACM.0b013e3181ace703)) — and is exactly MAI-DxO's Dr. Challenger.
- **It reuses NeuroAgent's existing assets better than any other proposal** — the Protocol Officer *is* the `RulesEngine`; the Cost Steward *is* `CostTracker`. Little new infrastructure.
- **It improves on MAI-DxO.** MAI-DxO's panel deliberates in persona free-text; here the shared substrate is an **explicit typed graph** — giving structured memory, auditability, and a fine-tuning target — and it is complexity-adaptive. The blackboard pattern ([HEARSAY-II](https://doi.org/10.1145/356810.356816)) is a proven way to coordinate many knowledge sources without brittle direct coupling.
- **It produces an auditable "case-conference transcript"** plus the graph — strong for clinical trust and for the paper.

#### How to build it in NeuroAgent

A `GraphOrchestrator` variant that runs role-conditioned LLM calls — *one base model, a distinct system prompt per role* (again, "proper system prompts"). Use a **structured turn-taking protocol**, not free chat, so agents cannot sycophantically converge — the Skeptic's adversarial turn is mandatory every round. Fine-tuning: distil the panel's consensus trajectories into a single model (panel-as-teacher), or train one model with role-conditioning.

#### Risks & mitigations

| Risk | Mitigation |
|------|-----------|
| More LLM calls (latency/cost) | Complexity-adaptive: solo path for easy cases; full panel only when needed. |
| Sycophantic agreement among agents | Structured adversarial protocol; the Skeptic is mandatory and scored on falsification attempts. |
| Orchestration complexity | The graph blackboard decouples roles (HEARSAY-II) — roles never call each other directly. |

#### Scorecard

| Relevance | Expected impact | Build effort | Novelty | Paper value | Risk |
|:---------:|:---------------:|:------------:|:-------:|:-----------:|:----:|
| **8.2 / 10** | High | Medium (reuses assets) | Medium | Medium–High | Low–Medium |

---

## 7. How the three fit together + recommended roadmap

The proposals are **layered, not alternatives**:

```
        ┌─────────────────────────────────────────────┐
        │   Proposal C — Multi-Agent Panel            │   orchestration policy
        │   (Diagnostician · Planner · Skeptic ·      │
        │    Protocol Officer · Cost Steward · Mod.)  │
        └───────────────────────┬─────────────────────┘
                                │ reads / writes
        ┌───────────────────────▼─────────────────────┐
        │   Proposal A — Diagnostic Hypothesis Graph   │   the representation /
        │   findings · hypotheses · tests · evidence   │   shared substrate
        │   belief tracking · cost-aware VOI policy    │
        └───────────────────────▲─────────────────────┘
                                │ expands / evaluates
        ┌───────────────────────┴─────────────────────┐
        │   Proposal B — Deliberate Search (LATS/MCTS) │   control policy +
        │   offline: fine-tuning data engine           │   offline data engine
        │   online: lookahead for hard cases           │
        └─────────────────────────────────────────────┘
```

**Proposal A is the substrate.** Proposal B is a *search control policy* over that substrate; Proposal C is an *orchestration policy* over it. The maximal system is **C's panel deliberating on A's graph, the Workup Planner using A's VOI rule and calling B's lookahead for hard cases — while B also runs offline as the engine that generates fine-tuning data.**

**Recommended roadmap:**

1. **Phase 1 — build Proposal A (the DHG).** Highest relevance, most novel, the substrate everything else needs, and the cleanest fine-tuning target. Ship it as a `GraphOrchestrator`, benchmark against the current ReAct NeuroAgent and a bare frontier model.
2. **Phase 2 — add Proposal C (the panel) on top of the DHG.** Cheap: the Protocol Officer and Cost Steward are wrappers over existing `RulesEngine` / `CostTracker`. Adds the Skeptic de-biasing story and complexity-adaptive routing.
3. **Phase 3 — run Proposal B offline as the fine-tuning data engine**; distil the search into the fine-tuned policy; enable online lookahead for the hardest `diagnostic_puzzle` cases.

This sequencing front-loads the novel contribution, reuses existing assets early, and treats fine-tuning as the capstone that the structured framework was designed to enable.

---

## 8. Coupling the framework with fine-tuning

The user's parallel goal — fine-tuning a model — is not separate from the reasoning framework; **the framework is what makes good fine-tuning possible.** Free-form ReAct gives one sparse outcome reward over a long, unstructured trajectory: terrible credit assignment. The structured framework changes this:

- **Verifiable, structured targets (R7).** Each graph operation — hypothesis seeding, LR-bucket scoring, test selection — is small and checkable. This is the [process-reward-model](https://arxiv.org/abs/2305.20050) setting, which strongly outperforms outcome-only supervision.
- **NeuroBench is already a verifiable reward source.** `GroundTruth` gives the correct diagnosis, `optimal_actions`, `critical_actions`, `contraindicated_actions` and `red_herrings`. A composite reward — correct primary dx + critical-action recall − contraindicated actions − cost overrun − miscalibration — enables **RLVR / GRPO** exactly as in [HuatuoGPT-o1](https://arxiv.org/abs/2412.18925) and [Med-R1](https://arxiv.org/abs/2503.13939).
- **Search as a data engine.** Proposal B generates many scored trajectories per case → SFT on the best, preference-optimise on the rest → distil into a fast policy ([rStar-Math](https://arxiv.org/abs/2501.04519), [AlphaLLM](https://arxiv.org/abs/2404.12253)).
- **Calibration as a first-class loss.** Because posteriors are explicit, a proper scoring rule (Brier) can be part of the objective — training the model to *know what it doesn't know*, which verbalised-confidence ReAct cannot.
- **Data sufficiency.** [O1 Journey Part 3](https://arxiv.org/abs/2501.06458) found ~500 well-supervised examples already move medical reasoning substantially — NeuroBench's 600 cases (500 train) are enough to start; the search engine multiplies them.

In short: **Proposal A makes the model *supervisable*, Proposal B *generates the training data*, Proposal C *provides a teacher to distil*.**

---

## 9. Evaluation for the Nature MI paper

Keep NeuroAgent's current metrics (diagnostic accuracy, action precision/recall, cost-efficiency, safety, the 8-dimension reasoning judge) and add the axes the structured framework uniquely unlocks — these *are* the paper's differentiation:

- **Calibration** — Brier score / Expected Calibration Error on hypothesis posteriors. A black-box model cannot report this honestly.
- **Accuracy-per-dollar** — the MAI-DxO headline metric; directly enabled by `CostTracker` + the VOI policy.
- **Can't-miss recall** — fraction of dangerous diagnoses kept in the differential until explicitly excluded.
- **Robustness to red herrings** — using `GroundTruth.red_herrings`; tests anti-anchoring structurally.
- **Auditability / interpretability** — clinician ratings of the graph as an explanation (vs. a ReAct transcript). For a Nature MI submission this is a primary contribution, not a footnote.

**Comparators:** (1) a bare frontier model, no tools (the [Kanjee](https://doi.org/10.1001/jama.2023.8288) / [Eriksen](https://ai.nejm.org/doi/full/10.1056/AIp2300031) baseline); (2) the current ReAct NeuroAgent; (3) ideally a re-implemented MAI-DxO-style persona panel — so the explicit-graph contribution is isolated and measured. The story to tell: *comparable-or-better accuracy, at lower cost, with calibrated uncertainty and an auditable reasoning artifact — and a fine-tunable small model that approaches frontier accuracy.*

---

## 10. Relevancy scoreboard

**The three proposals:**

| Proposal | Relevance | Impact | Effort | Novelty | Paper value | Risk | Recommended phase |
|----------|:---------:|:------:|:------:|:-------:|:-----------:|:----:|:-----------------:|
| **A — Diagnostic Hypothesis Graph** | **9.6** | High | Med–High | High | High | Medium | **Phase 1** |
| **B — Deliberate Search (LATS/MCTS)** | **8.6** | High | High | Med–High | High | Med–High | **Phase 3** |
| **C — Multi-Agent Panel on the Graph** | **8.2** | High | Medium | Medium | Med–High | Low–Med | **Phase 2** |

**Highest-relevance individual works** (full list scored in §4):

| Score | Works |
|:-----:|-------|
| **10** | MAI-DxO / Sequential Diagnosis |
| **9** | Graph of Thoughts · LATS · MDAgents · MindMap · Chain-of-Diagnosis · LA-CDM · MedKGI · Pathfinder · Elstein (hypothetico-deduction) · Schmidt (illness scripts) |
| **8** | Reflexion-adjacent search (AlphaLLM/rStar-Math) · CoALA · Process Reward Models · AMIE · MedAgents · HuatuoGPT-o1 · QMR-DT · Richens (causal diagnosis) · HEARSAY-II · ArgMed-Agents · Croskerry · Graber · Tree of Thoughts |

---

## 11. References

All entries are in the companion `references.bib`. Grouped below by theme; `[key]` matches the BibTeX key.

**General LLM reasoning & agents.** `[yao2023react]` ReAct · `[wei2022cot]` Chain-of-Thought · `[wang2023selfconsistency]` Self-Consistency · `[yao2023tot]` Tree of Thoughts · `[besta2024got]` Graph of Thoughts · `[zhou2024lats]` LATS · `[shinn2023reflexion]` Reflexion · `[xu2023rewoo]` ReWOO · `[zhang2024cumulative]` Cumulative Reasoning · `[sumers2024coala]` CoALA · `[lightman2024verify]` Let's Verify Step by Step · `[madaan2023selfrefine]` Self-Refine · `[du2024multiagentdebate]` Multi-agent debate · `[tian2024alphallm]` AlphaLLM · `[guan2025rstarmath]` rStar-Math · `[qi2024rstar]` rStar · `[yang2024bot]` Buffer of Thoughts · `[prasad2024adapt]` ADaPT · `[packer2023memgpt]` MemGPT · `[park2023generativeagents]` Generative Agents · `[wang2023planandsolve]` Plan-and-Solve · `[zhou2023leasttomost]` Least-to-Most · `[sel2024aot]` Algorithm of Thoughts · `[schick2023toolformer]` Toolformer · `[wang2023voyager]` Voyager · `[wang2024agentsurvey]` Survey of LLM agents.

**Medical & clinical diagnostic AI.** `[nori2025sequential]` MAI-DxO / Sequential Diagnosis · `[tu2025amie]` AMIE · `[palepu2025management]` AMIE-Management · `[saab2025multimodal]` AMIE-Multimodal · `[mcduff2023ddx]` Towards accurate DDx · `[tang2024medagents]` MedAgents · `[kim2024mdagents]` MDAgents · `[chen2024cod]` Chain-of-Diagnosis · `[schmidgall2024agentclinic]` AgentClinic · `[jiang2025medagentbench]` MedAgentBench · `[tang2025medagentsbench]` MedAgentsBench · `[wen2024mindmap]` MindMap · `[gao2023drknows]` DR.KNOWS · `[jiang2025kare]` KARE · `[xiong2024medrag]` MedRAG/MIRAGE · `[zhao2025medragkg]` MedRAG (KG-elicited) · `[wu2025medreason]` MedReason · `[chen2024huatuogpt]` HuatuoGPT-o1 · `[lai2025medr1]` Med-R1 · `[huang2025o1journey]` O1 Journey Part 3 · `[baniharouni2025lacdm]` LA-CDM · `[wang2025medkgi]` MedKGI · `[zuo2024kg4diagnosis]` KG4Diagnosis · `[kanjee2023gpt4]` Kanjee · `[eriksen2024gpt4]` Eriksen · `[wang2025medagentsurvey]` Survey of medical LLM agents.

**Classic diagnostic expert systems.** `[miller1982internist]` INTERNIST-1 · `[shwe1991qmrdt]` QMR-DT · `[heckerman1992pathfinder]` Pathfinder · `[shortliffe1976mycin]` MYCIN · `[barnett1987dxplain]` DXplain.

**Graph reasoning & knowledge graphs.** `[edge2024graphrag]` GraphRAG · `[sun2024tog]` Think-on-Graph · `[luo2024rog]` Reasoning on Graphs · `[chandak2023primekg]` PrimeKG · `[bodenreider2004umls]` UMLS · `[himmelstein2017hetionet]` Hetionet · `[morris2023spoke]` SPOKE.

**Bayesian, decision-theoretic & model-based diagnosis.** `[pearl1988probabilistic]` Pearl · `[reiter1987diagnosis]` Reiter · `[dekleer1987multiplefaults]` de Kleer & Williams · `[naghshvar2013active]` Active hypothesis testing · `[richens2020causal]` Causal diagnosis · `[peng2018refuel]` REFUEL · `[fansitchango2022trustworthy]` Trustworthy diagnosis · `[erman1980hearsay]` HEARSAY-II.

**Computational argumentation.** `[dung1995acceptability]` Dung · `[modgil2014aspic]` ASPIC+ · `[sassoon2021argumentation]` Argumentation schemes for CDS · `[hong2024argmedagents]` ArgMed-Agents.

**Cognitive science of clinical reasoning.** `[elstein1978medical]` Medical Problem Solving (hypothetico-deduction) · `[schmidt1990illnessscripts]` Illness scripts · `[croskerry2009universal]` Dual-process model · `[graber2005diagnostic]` Diagnostic error.

---

*Compiled 2026-05-22. 80 verified references in `references.bib`. Open question for the team: how richly to ground `HypothesisNode`s in an external medical KG (UMLS / PrimeKG) versus letting the LLM generate illness scripts on the fly — a build-vs-generate trade-off worth a small ablation early in Phase 1.*
