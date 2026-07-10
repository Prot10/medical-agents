# Literature Review — Tool-Augmented LLM Agents for Clinical Decision Support

**State of the art for the NeuroAgent project**
Compiled 2026-05-22 · 20 papers · companion file: [`references.bib`](./references.bib) · PDFs: [`pdfs/`](./pdfs/)

---

## 1. Scope and method

This review surveys the state of the art most relevant to **NeuroAgent** — a tool-augmented
LLM agent for neurological clinical decision support (ReAct loop, 12 diagnostic tools,
hospital-protocol grounding, patient memory, per-tool cost tracking, evaluated on the
NeuroBench benchmark, targeting *Nature Machine Intelligence*).

It covers five themes: (A) agentic and tool-augmented LLM systems in medicine,
(B) benchmarks and evaluation for clinical/agentic AI, (C) medical foundation models and
diagnostic-reasoning LLMs, (D) the agent method foundations NeuroAgent is built on, and
(E) neurology-specific evidence and tool grounding.

**Validation.** Every paper was checked against primary metadata sources — CrossRef, the
arXiv API, Semantic Scholar and Europe PMC. Each summary is grounded in the paper's own
**abstract or full text** (not third-party descriptions); all quantitative figures below are
taken verbatim from those sources. Where a downloaded PDF is a preprint rather than the
journal version of record, this is stated explicitly. One paper (Qiu et al.) is a *Nature
Machine Intelligence* Comment with no formal abstract; its summary is drawn from the
published Comment and is corroborated by how it is cited in the peer-reviewed review by
Zhao et al. \[6].

## 2. How to read this review

**Relevance score (0–10)** — how directly the paper informs NeuroAgent's *architecture,
evaluation methodology, baselines, or scientific positioning*:

| Band | Meaning |
|------|---------|
| 9–10 | Directly shapes NeuroAgent's design, the NeuroBench benchmark, or its central claims |
| 7–8.5 | Strong methodological precedent, baseline, or positioning reference |
| 5–6.5 | Important background / field context |
| <5 | Peripheral (none included) |

Each entry gives: relevance score · BibTeX key · venue · DOI link · local PDF path ·
a concise summary with the main *validated* findings · why it matters for NeuroAgent.

## 3. Summary table (sorted by relevance)

| # | Paper (key) | Venue | Year | Score | PDF |
|---|-------------|-------|------|:----:|:---:|
| 3 | Ferber et al. — autonomous oncology agent (`ferber2025autonomous`) | Nature Cancer | 2025 | **9.5** | ✓ |
| 7 | Schmidgall et al. — AgentClinic (`schmidgall2026agentclinic`) | npj Digital Medicine | 2026 | **9.5** | ✓ |
| 8 | Liu et al. — benchmarking agent systems (`liu2026benchmarking`) | npj Digital Medicine | 2026 | **9.5** | ✓ |
| 11 | Nori et al. — Sequential Diagnosis / MAI-DxO (`nori2025sequential`) | arXiv (Microsoft) | 2025 | **9.5** | ✓ |
| 2 | Gao et al. — TxAgent (`gao2025txagent`) | arXiv (Harvard) | 2025 | **9.0** | ✓ |
| 1 | Qiu et al. — agentic systems in medicine (`qiu2024agentic`) | Nature Machine Intelligence | 2024 | **8.5** | — |
| 9 | Bedi et al. — MedHELM (`bedi2026medhelm`) | Nature Medicine | 2026 | **8.5** | ✓ |
| 17 | Yao et al. — ReAct (`yao2023react`) | ICLR | 2023 | **8.5** | ✓ |
| 10 | Jiang et al. — MedAgentBench (`jiang2025medagentbench`) | NEJM AI | 2025 | **8.0** | ✓ |
| 12 | Tu et al. — AMIE (`tu2025amie`) | Nature | 2025 | **8.0** | ✓ |
| 19 | Barrit et al. — specialized neurology LLM (`barrit2025neurology`) | Brain Sciences | 2025 | **8.0** | ✓ |
| 20 | Goodell et al. — tools for clinical calculations (`goodell2025calculations`) | npj Digital Medicine | 2025 | **8.0** | ✓ |
| 4 | Kim et al. — MDAgents (`kim2024mdagents`) | NeurIPS | 2024 | **7.5** | ✓ |
| 16 | Sandmann et al. — DeepSeek clinical benchmark (`sandmann2025deepseek`) | Nature Medicine | 2025 | **7.5** | — |
| 5 | Tang et al. — MedAgents (`tang2024medagents`) | ACL Findings | 2024 | **7.0** | ✓ |
| 6 | Zhao et al. — AI agents in healthcare review (`zhao2026aiagent`) | npj Artificial Intelligence | 2026 | **7.0** | ✓ |
| 14 | Liu et al. — MedFound (`liu2025medfound`) | Nature Medicine | 2025 | **7.0** | — |
| 13 | Singhal et al. — Med-PaLM (`singhal2023medpalm`) | Nature | 2023 | **6.5** | ✓ |
| 18 | Schick et al. — Toolformer (`schick2023toolformer`) | NeurIPS | 2023 | **6.5** | ✓ |
| 15 | Moor et al. — generalist medical AI (`moor2023foundation`) | Nature | 2023 | **6.0** | ✓ |

PDF availability: **17 / 20** downloaded to [`pdfs/`](./pdfs/). Three could not be obtained
automatically (see §7).

---

## 4. The state of the art — synthesis

**(i) The paradigm has shifted from medical question-answering to medical *agents*.**
The 2023 foundational work established that LLMs encode clinical knowledge and excel at
exam-style QA — Med-PaLM reached 67.6% on USMLE-style MedQA \[13] — and sketched a vision of
flexible, multimodal "generalist medical AI" \[15]. But those same papers' human evaluations
exposed that exam scores do not equal clinical competence. By 2024–2026 the frontier moved to
systems that *plan, call tools, and act*: Qiu et al. \[1] gave this the canonical framing in
*Nature Machine Intelligence*, and ReAct \[17] and Toolformer \[18] are its method roots.

**(ii) Two architectural families now dominate.** *Multi-agent collaboration* — several
role-played LLMs debating to a consensus (MedAgents \[5], MDAgents \[4]) — and *tool-augmented
single agents* — one agent orchestrating external tools (TxAgent \[2], Ferber et al. \[3]).
**NeuroAgent belongs to the second family**, and the most decision-relevant comparisons in
this review are within it.

**(iii) Tools demonstrably fix specific LLM weaknesses — but generic "agentification" buys
little, and at high cost.** Goodell et al. \[20] prove that task-specific tools cut medical
calculation errors 5.5–13×. Ferber et al. \[3] report decision accuracy rising from 30.3% to
87.2% once oncology tools are added. Yet the most rigorous head-to-head benchmark — Liu et
al. \[8] — finds that *general* agentic systems gain only modestly over baseline LLMs while
consuming **>10× tokens and >2× latency**, and MDAgents' \[4] absolute gains over prior
methods are ≈4%. The honest synthesis: **tools help when they target a real weakness;
orchestration for its own sake does not — and cost is almost never reported.** This directly
validates NeuroAgent's decision to instrument per-tool cost.

**(iv) Evaluation is now the field's bottleneck.** Static multiple-choice QA massively
overstates clinical ability — AgentClinic \[7] shows diagnostic accuracy collapsing to below
one-tenth of static-QA accuracy once a case becomes a sequential, incomplete-information
encounter. The response is a wave of realistic interactive benchmarks: AgentClinic \[7]
(simulated clinic), MedAgentBench \[10] (virtual FHIR/EHR), Sequential Diagnosis \[11]
(iterative NEJM cases), and MedHELM \[9] (clinician-validated task taxonomy). **NeuroBench
sits squarely in this movement** and should be positioned against these four.

**(v) Cost-awareness is the newest and least-explored evaluation axis.** Only Sequential
Diagnosis \[11] treats the *monetary* cost of tests and visits as a first-class metric
alongside accuracy; MedHELM \[9] adds a cost–performance analysis, and Liu et al. \[8] account
for tokens and latency. NeuroAgent's per-tool Medicare-PFS cost registry places it at the
leading edge of this axis — and there is essentially **no prior cost-aware agentic benchmark
in neurology**.

**(vi) Open-weight models are now clinically credible.** Sandmann et al. \[16] show
open-source DeepSeek on par with GPT-4o and Gemini-2.0 in clinical decision-making; MedHELM
\[9] finds Claude-3.5-Sonnet matching top models at ~40% lower cost; MedFound \[14] is an open
176B diagnostic model. This peer-reviewed evidence legitimizes NeuroAgent's engineering
choice to run on locally-deployable open models (Qwen, MedGemma) for privacy and
reproducibility.

**(vii) Neurology specifically is under-served.** Despite the breadth above, only Barrit et
al. \[19] target neurology with a knowledge-grounded, memory-equipped LLM — and on just five
cases. There is **no tool-augmented, benchmark-scale neurological decision-support agent** in
the literature. That is the gap NeuroAgent fills.

---

## 5. Annotated papers

### Theme A — Agentic & tool-augmented LLM systems in medicine

#### 1. Qiu et al. (2024) — LLM-based agentic systems in medicine and healthcare
**Relevance 8.5/10** · `qiu2024agentic` · *Nature Machine Intelligence* 6(12):1418–1420
[DOI](https://doi.org/10.1038/s42256-024-00944-1) · PDF: *not available — paywalled Comment, no preprint (see §7)*

**Summary & main findings.** A Comment that gives the agentic-systems paradigm its canonical
framing for medicine. It characterizes LLM-based agents by a set of core capabilities —
processing input information, planning and deciding, recalling and reflecting, interacting and
collaborating, and leveraging tools to act — and maps the opportunity space from clinical
workflow automation to multi-agent-aided diagnosis, while flagging risks around data privacy
and over-reliance. (As a ~3-page Comment it has no formal abstract; this characterization is
corroborated by the peer-reviewed review \[6], which cites it as examining "applications in
diagnostic support and workflow optimization, while also highlighting challenges related to
data privacy and over-reliance.")

**Why it matters for NeuroAgent.** This is the reference definition of "agentic systems in
medicine" and it appears in NeuroAgent's target journal. NeuroAgent is a concrete
instantiation of exactly this paradigm — ReAct loop = plan/decide + reflect; 12 tools =
leverage tools to act; patient memory = recall. Cite it to define the paradigm and to
position NeuroAgent within *NMI*'s own editorial framing.

#### 2. Gao et al. (2025) — TxAgent: an AI agent for therapeutic reasoning across a universe of tools
**Relevance 9.0/10** · `gao2025txagent` · arXiv:2503.10970 (Harvard / Zitnik Lab)
[arXiv](https://arxiv.org/abs/2503.10970) · PDF: [`pdfs/02_gao2025txagent.pdf`](./pdfs/02_gao2025txagent.pdf) *(version of record — preprint-only)*

**Summary & main findings.** TxAgent performs multi-step reasoning with real-time biomedical
knowledge retrieval over a **toolbox of 211 tools** ("ToolUniverse," spanning all FDA-approved
drugs since 1939 and Open Targets evidence). It selects tools by task objective and executes
structured function calls to analyze drug–drug interactions, contraindications given
comorbidities/co-medications, and patient-specific treatment strategies, refining
recommendations through iterative reasoning. Across five new benchmarks (3,168 drug-reasoning
tasks + 456 treatment scenarios) it reaches **92.1% accuracy** on open-ended drug reasoning,
surpassing GPT-4o and outperforming DeepSeek-R1 (671B) on structured multi-step reasoning.

**Why it matters for NeuroAgent.** The largest-scale demonstration of the exact design
NeuroAgent uses — function-calling over a curated tool set with iterative reasoning and
guideline grounding. Its drug-interaction focus maps directly onto NeuroAgent's
`check_drug_interactions` and `search_medical_literature` tools, and its "tool universe"
framing helps justify why a fixed, well-chosen 12-tool set is a defensible design.

#### 3. Ferber et al. (2025) — Autonomous AI agent for clinical decision-making in oncology
**Relevance 9.5/10** · `ferber2025autonomous` · *Nature Cancer* 6(8):1337–1349
[DOI](https://doi.org/10.1038/s43018-025-00991-6) · PDF: [`pdfs/03_ferber2025autonomous.pdf`](./pdfs/03_ferber2025autonomous.pdf) *(published version)*

**Summary & main findings.** An autonomous clinical AI agent built on GPT-4 that orchestrates
multimodal precision-oncology tools — vision transformers for MSI and KRAS/BRAF mutation
detection from histopathology, MedSAM for radiology segmentation, and web search
(OncoKB, PubMed, Google). On 20 realistic multimodal patient cases the agent autonomously
selected appropriate tools with **87.5%** accuracy, reached correct clinical conclusions in
**91.0%** of cases, and cited relevant oncology guidelines correctly **75.5%** of the time.
Tool integration raised decision accuracy from **30.3% (GPT-4 alone) to 87.2%**.

**Why it matters for NeuroAgent.** The closest published architectural analog: a *single
tool-augmented agent for one specialty*, validated on a curated case set, reporting
tool-selection accuracy, conclusion accuracy and guideline-citation rate — almost exactly
NeuroAgent's evaluation surface. The 30→87% uplift is the headline "tools matter" result
NeuroAgent should replicate and contextualize for neurology, and its metric set is directly
reusable for NeuroBench.

#### 4. Kim et al. (2024) — MDAgents: an adaptive collaboration of LLMs for medical decision-making
**Relevance 7.5/10** · `kim2024mdagents` · NeurIPS 2024, pp. 79410–79452
[arXiv](https://arxiv.org/abs/2404.15155) · PDF: [`pdfs/04_kim2024mdagents.pdf`](./pdfs/04_kim2024mdagents.pdf) *(arXiv version ≈ camera-ready)*

**Summary & main findings.** A multi-agent framework that adaptively assigns a collaboration
structure — solo clinician, multi-disciplinary team, or integrated care team — based on an
automatically estimated medical-complexity level, emulating how real decision-making scales
with case difficulty. Across ten medical knowledge/diagnosis benchmarks it achieved the best
performance on **seven of ten**, with improvement of **up to 4.2% (p<0.05)** over prior best
methods; ablations show that combining moderator review with external medical knowledge yields
an **11.8%** average accuracy gain.

**Why it matters for NeuroAgent.** The leading example of the *alternative* paradigm —
multi-agent collaboration — against which NeuroAgent (a single tool-augmented agent) must be
positioned. Its complexity-routing idea is relevant to NeuroBench's case-difficulty design,
and its modest absolute gains feed the recurring debate over whether orchestration complexity
is worth its cost.

#### 5. Tang et al. (2024) — MedAgents: LLMs as collaborators for zero-shot medical reasoning
**Relevance 7.0/10** · `tang2024medagents` · Findings of ACL 2024, pp. 599–621
[ACL Anthology](https://aclanthology.org/2024.findings-acl.33) · PDF: [`pdfs/05_tang2024medagents.pdf`](./pdfs/05_tang2024medagents.pdf) *(published version)*

**Summary & main findings.** A **training-free** multi-disciplinary collaboration framework in
which LLM agents role-play domain experts and reach a decision through five steps: gather
experts, propose individual analyses, summarize into a report, iterate to consensus, and
decide. In the zero-shot setting it improves performance across nine datasets (MedQA,
MedMCQA, PubMedQA and six MMLU medical subtasks).

**Why it matters for NeuroAgent.** An early, heavily-cited multi-agent baseline showing that
structured role-play discussion can extract latent medical knowledge from a general LLM with
no fine-tuning. For NeuroAgent it is contrast: MedAgents improves reasoning *purely* through
prompting/collaboration with **no external tools** — sharpening the argument that NeuroAgent's
gains come from real diagnostic tool calls, not just agent dialogue.

#### 6. Zhao et al. (2026) — AI agent in healthcare: applications, evaluations, and future directions
**Relevance 7.0/10** · `zhao2026aiagent` · *npj Artificial Intelligence* 2(1):31
[DOI](https://doi.org/10.1038/s44387-026-00076-4) · PDF: [`pdfs/06_zhao2026aiagent.pdf`](./pdfs/06_zhao2026aiagent.pdf) *(published version, open access)*

**Summary & main findings.** A review tracing the evolution and core characteristics of
healthcare AI agents and systematically surveying applications across assisted diagnosis,
clinical decision support, medical report generation, patient-facing chatbots,
healthcare-system management and medical education. It analyzes existing evaluation
frameworks and their performance dimensions, then proposes **seven directions for future
work** — including integration with embodied systems, hybrid expert models, expanded
evaluation paradigms, safety and controllability, ethical governance and user trust, and
guidance for the evolving roles of healthcare staff.

**Why it matters for NeuroAgent.** The most current (March 2026) structured map of the field —
useful scaffolding for NeuroAgent's introduction and related-work, and an authoritative
source for an application taxonomy and the field's open evaluation problems. Its explicit
calls for "expanded evaluation paradigms" and "safety and controllability" directly support
the rationale for NeuroBench.

### Theme B — Benchmarks & evaluation for clinical / agentic AI

#### 7. Schmidgall et al. (2026) — AgentClinic: a multimodal benchmark for tool-using clinical AI agents
**Relevance 9.5/10** · `schmidgall2026agentclinic` · *npj Digital Medicine* (2026)
[DOI](https://doi.org/10.1038/s41746-026-02674-7) · PDF: [`pdfs/07_schmidgall2026agentclinic.pdf`](./pdfs/07_schmidgall2026agentclinic.pdf) *(arXiv preprint 2405.07960; journal version of record: npj Digital Medicine 2026)*

**Summary & main findings.** A multimodal benchmark evaluating LLMs *as agents* in simulated
clinical environments — patient dialogue, multimodal data collection under incomplete
information, and tool use — across **nine specialties and seven languages**, run by four
specialized agents (measurement, doctor, patient, moderator). Recasting MedQA into
AgentClinic's sequential decision-making format drops diagnostic accuracy **to below
one-tenth** of static-QA accuracy. Claude-3.5-based agents lead overall, but models differ
sharply in tool use; strikingly, **Llama-3 shows up to 92% relative improvement** when given a
persistent note-taking tool that carries information across cases.

**Why it matters for NeuroAgent.** The conceptual sibling of NeuroBench — a benchmark for
*tool-using clinical agents* in sequential, incomplete-information settings rather than static
QA. Its central finding (static accuracy collapses under sequential agency) validates
NeuroBench's entire premise. The persistent-notebook result is direct evidence for
NeuroAgent's **patient-memory** component, and the measurement/doctor/patient/moderator design
plus patient-centric metrics are reusable for NeuroBench.

#### 8. Liu et al. (2026) — Benchmarking LLM-based agent systems for clinical decision tasks
**Relevance 9.5/10** · `liu2026benchmarking` · *npj Digital Medicine* 9(1):259
[DOI](https://doi.org/10.1038/s41746-026-02443-6) · PDF: [`pdfs/08_liu2026benchmarking.pdf`](./pdfs/08_liu2026benchmarking.pdf) *(published version, open access)*

**Summary & main findings.** A systematic benchmark of two agent systems — open-source
OpenManus (Llama-4, medically customized) and proprietary Manus (planner-executor-verifier) —
across AgentClinic, MedAgentsBench and Humanity's Last Exam. Despite advanced tools (web
browsing, code execution, file editing), the agentic designs gave **only modest gains** over
baseline LLMs (60.3% / 28.0% on AgentClinic MedQA / MIMIC, 30.3% on MedAgentsBench, 8.6% on
HLE-text; multimodal stayed low at 15.5% / 29.2%) while resource demand rose sharply —
**>10× token usage and >2× latency**. In-agent safeguards filtered 89.9% of hallucinations,
but hallucinations remained prevalent.

**Why it matters for NeuroAgent.** The central cautionary result for NeuroAgent's thesis:
current agentic tooling buys *modest* accuracy at *large* compute/latency cost. It is the
strongest published argument for NeuroAgent's cost-tracking instrumentation — any claimed
benefit must be reported against token/latency/dollar cost. It also names AgentClinic and
MedAgentsBench as the field's reference benchmarks (useful NeuroBench positioning), and is
from the same lab as Ferber et al. \[3].

#### 9. Bedi et al. (2026) — Holistic evaluation of LLMs for medical tasks with MedHELM
**Relevance 8.5/10** · `bedi2026medhelm` · *Nature Medicine* 32(3):943–951
[DOI](https://doi.org/10.1038/s41591-025-04151-2) · PDF: [`pdfs/09_bedi2026medhelm.pdf`](./pdfs/09_bedi2026medhelm.pdf) *(arXiv preprint 2505.23802; journal version of record: Nature Medicine 2026)*

**Summary & main findings.** An evaluation framework with a **clinician-validated taxonomy**
(5 categories, 22 subcategories, 121 tasks, built with 29 clinicians) and a 35-benchmark suite
(17 existing + 18 new) covering it. Evaluating nine frontier LLMs, reasoning models led
(DeepSeek-R1 66% win-rate, o3-mini 64%), but Claude-3.5-Sonnet matched top models at **~40%
lower estimated compute cost**. On a 0–1 normalized accuracy scale, models scored well on
clinical note generation (0.73–0.85) and patient communication (0.78–0.83) but **lower on
clinical decision support (0.56–0.72)**. An "LLM-jury" evaluator agreed with clinicians
(ICC 0.47) better than clinician–clinician agreement (0.43).

**Why it matters for NeuroAgent.** The reference for benchmark *methodology*, published in
NeuroAgent's adjacent target venue. Its clinician-validated taxonomy directly models the
clinician-validation effort NeuroBench is preparing for; its cost–performance analysis and
LLM-jury method are templates for NeuroBench's evaluation. Crucially, it shows **clinical
decision support is the weakest task category** — exactly NeuroAgent's target.

#### 10. Jiang et al. (2025) — MedAgentBench: a virtual EHR environment to benchmark medical LLM agents
**Relevance 8.0/10** · `jiang2025medagentbench` · *NEJM AI* 2(9)
[DOI](https://doi.org/10.1056/AIdbp2500144) · PDF: [`pdfs/10_jiang2025medagentbench.pdf`](./pdfs/10_jiang2025medagentbench.pdf) *(arXiv preprint 2501.14654; journal version of record: NEJM AI 2025)*

**Summary & main findings.** An agent benchmark set in a realistic virtual EHR: **300**
physician-written, patient-specific tasks across 10 categories, 100 patient profiles with
**>700,000 data elements**, and a **FHIR-compliant interactive environment** using the
standard APIs of modern EHR systems. The best model (Claude-3.5-Sonnet v2) reached a
**69.67% success rate**, with large variation across task categories — an unsaturated
benchmark.

**Why it matters for NeuroAgent.** The closest existing "agent performs clinician tasks via
tool/API calls" benchmark and a methodological template for NeuroBench's tool-call evaluation
(it scores function-calling success against ground truth). Its FHIR-realistic environment and
per-category breakdown inform how NeuroBench should report results across NeuroAgent's 12
tools.

#### 11. Nori et al. (2025) — Sequential Diagnosis with Language Models (MAI-DxO)
**Relevance 9.5/10** · `nori2025sequential` · arXiv:2506.22405 (Microsoft AI)
[arXiv](https://arxiv.org/abs/2506.22405) · PDF: [`pdfs/11_nori2025sequential.pdf`](./pdfs/11_nori2025sequential.pdf) *(version of record — preprint-only)*

**Summary & main findings.** Introduces the **Sequential Diagnosis Benchmark** — 304 NEJM
clinicopathological-conference cases turned into stepwise encounters in which a physician or
AI iteratively queries a "gatekeeper" that reveals findings only on request — and scores both
diagnostic accuracy **and the monetary cost of visits and tests**. The MAI Diagnostic
Orchestrator (MAI-DxO), a model-agnostic "panel of physicians" that proposes differentials
and selects high-value, cost-effective tests, reaches **80% accuracy** with OpenAI o3 (vs 20%
for generalist physicians), cutting cost **20% vs physicians and 70% vs off-the-shelf o3**; a
maximum-accuracy configuration reaches 85.5%. Gains generalize across the OpenAI, Gemini,
Claude, Grok, DeepSeek and Llama families.

**Why it matters for NeuroAgent.** The single most important precedent for NeuroAgent's
**cost-tracking** design — essentially the only major benchmark that scores diagnostic agents
on monetary cost as well as accuracy. Its gatekeeper / iterative-querying setup mirrors
NeuroAgent's ReAct tool-ordering loop, and its accuracy-vs-cost framing is exactly what
NeuroBench's Medicare-PFS cost registry enables. Use it to ground NeuroAgent's cost
contribution and to argue that cost-aware evaluation is becoming the standard.

### Theme C — Medical foundation models & diagnostic-reasoning LLMs

#### 12. Tu et al. (2025) — Towards conversational diagnostic artificial intelligence (AMIE)
**Relevance 8.0/10** · `tu2025amie` · *Nature* 642(8067):442–450
[DOI](https://doi.org/10.1038/s41586-025-08866-7) · PDF: [`pdfs/12_tu2025amie.pdf`](./pdfs/12_tu2025amie.pdf) *(arXiv preprint 2401.05654; journal version of record: Nature 2025)*

**Summary & main findings.** AMIE (Articulate Medical Intelligence Explorer) is an LLM-based
system optimized for diagnostic dialogue, trained with a **self-play** simulated environment
and automated feedback to scale learning across conditions and specialties. In a
**randomized, double-blind crossover study** of 159 OSCE-style text consultations with
validated patient-actors, AMIE matched or exceeded 20 primary-care physicians, with greater
diagnostic accuracy and superior performance on **30/32 axes** (specialist raters) and
**25/26 axes** (patient-actors). The authors stress limitations — synchronous text chat is
not standard clinical practice.

**Why it matters for NeuroAgent.** The headline result for diagnostic AI and a gold standard
for **evaluation rigor**: its randomized, double-blind, multi-axis OSCE-style design is what
NeuroBench's clinician validation should emulate. It is also a clean contrast — AMIE optimizes
conversational *history-taking*, whereas NeuroAgent optimizes tool-augmented *work-up*;
together they cover the two halves of a real consultation, which makes a tidy positioning
argument.

#### 13. Singhal et al. (2023) — Large language models encode clinical knowledge (Med-PaLM)
**Relevance 6.5/10** · `singhal2023medpalm` · *Nature* 620(7972):172–180
[DOI](https://doi.org/10.1038/s41586-023-06291-2) · PDF: [`pdfs/13_singhal2023medpalm.pdf`](./pdfs/13_singhal2023medpalm.pdf) *(arXiv preprint 2212.13138; journal version of record: Nature 2023)*

**Summary & main findings.** Introduces **MultiMedQA** (six existing medical-QA datasets plus
the new HealthSearchQA) and a human-evaluation framework scoring answers on factuality,
comprehension, reasoning, possible harm and bias. Flan-PaLM (540B) reached state-of-the-art
on every MultiMedQA multiple-choice set, including **67.6% on MedQA** (USMLE-style),
>17 points above prior SOTA; instruction prompt tuning produced **Med-PaLM**, which improved
on human-judged axes but remained inferior to clinicians.

**Why it matters for NeuroAgent.** The foundational medical-LLM paper and the origin of the
"exam-score" evaluation paradigm. NeuroAgent's core motivation — that USMLE-style accuracy
does not equal clinical competence — is precisely the gap that Med-PaLM's own human evaluation
first exposed. Cite it as the historical baseline and as evidence that benchmarks beyond
multiple-choice (i.e., NeuroBench) are necessary.

#### 14. Liu et al. (2025) — A generalist medical language model for disease diagnosis assistance (MedFound)
**Relevance 7.0/10** · `liu2025medfound` · *Nature Medicine* 31(3):932–942
[DOI](https://doi.org/10.1038/s41591-024-03416-6) · PDF: *not available — paywalled, no preprint (see §7)*

**Summary & main findings.** MedFound is a **176-billion-parameter** medical LLM pre-trained
on diverse medical text and real clinical records, then fine-tuned to imitate physicians'
inferential diagnosis via a self-bootstrapping chain-of-thought strategy plus a unified
preference-alignment framework. It outperforms baseline and specialized models in
in-distribution (common), out-of-distribution (external validation) and long-tailed (rare
disease) settings across **eight specialties**; an AI-assistance reader study and an
eight-metric clinical evaluation framework show it can improve physicians' diagnostic
accuracy within the workflow.

**Why it matters for NeuroAgent.** MedFound represents the competing design philosophy — a
large, domain-fine-tuned diagnostic-reasoning model — versus NeuroAgent's tool-augmented
agent over open mid-size models. It is a strong baseline/contrast, and its rare-disease and
external-validation evaluations and AI-assistance reader study are methodological templates.
It frames a clear thesis for NeuroAgent: tooling + protocols vs. brute-force fine-tuning.

#### 15. Moor et al. (2023) — Foundation models for generalist medical artificial intelligence
**Relevance 6.0/10** · `moor2023foundation` · *Nature* 616(7956):259–265
[DOI](https://doi.org/10.1038/s41586-023-05881-4) · PDF: [`pdfs/15_moor2023foundation.pdf`](./pdfs/15_moor2023foundation.pdf) *(accepted manuscript via NSF Public Access Repository)*

**Summary & main findings.** A Perspective proposing **generalist medical AI (GMAI)**: models
built by self-supervision on large, diverse datasets that flexibly interpret combinations of
modalities (imaging, EHR, labs, genomics, graphs, text) and produce expressive outputs
(free-text explanations, annotations) with advanced medical reasoning. It identifies
high-impact applications and the technical capabilities/datasets needed, and warns that GMAI
will strain current strategies for **regulating and validating** medical-AI devices.

**Why it matters for NeuroAgent.** The agenda-setting vision paper for flexible, multi-task
medical AI — useful for framing NeuroAgent's ambition and for citing the regulatory/validation
foresight that motivates rigorous, clinician-validated benchmarking. It is context rather than
method: NeuroAgent realizes GMAI-style breadth through *tool orchestration* instead of a
single monolithic multimodal model.

#### 16. Sandmann et al. (2025) — Benchmark evaluation of DeepSeek LLMs in clinical decision-making
**Relevance 7.5/10** · `sandmann2025deepseek` · *Nature Medicine* 31(8):2546–2549
[DOI](https://doi.org/10.1038/s41591-025-03727-2) · PDF: *not auto-downloadable — open access via PMC (see §7)*

**Summary & main findings.** Benchmarks open-source **DeepSeek-V3 and DeepSeek-R1** against
proprietary GPT-4o and Gemini-2.0-Flash-Thinking on clinical decision-support tasks, using
**125 statistically-powered patient cases** spanning frequent and rare diseases. DeepSeek
models performed **on par with — and in some cases better than** — the proprietary models on
diagnosis and treatment-recommendation tasks. The authors emphasize that open-source models
can be deployed on-site, satisfying privacy regulations that block proprietary models.

**Why it matters for NeuroAgent.** Direct, peer-reviewed evidence — in NeuroAgent's adjacent
target journal — that open-weight LLMs are clinically competitive with proprietary ones. This
is the citation that justifies NeuroAgent's core engineering choice to run on
locally-deployable open models (Qwen, MedGemma) for privacy compliance, on-site deployment
and reproducibility.

### Theme D — Agent method foundations

#### 17. Yao et al. (2023) — ReAct: synergizing reasoning and acting in language models
**Relevance 8.5/10** · `yao2023react` · ICLR 2023
[arXiv](https://arxiv.org/abs/2210.03629) · PDF: [`pdfs/17_yao2023react.pdf`](./pdfs/17_yao2023react.pdf) *(arXiv 2210.03629)*

**Summary & main findings.** ReAct prompts an LLM to **interleave reasoning traces with task
actions**, so reasoning helps form/track/update action plans while actions gather information
from external sources (e.g., a Wikipedia API). It reduces hallucination and error propagation
versus pure chain-of-thought on HotpotQA and Fever, and beats imitation/RL methods on
ALFWorld and WebShop by **34% and 10% absolute** success with only one or two in-context
examples — while improving human interpretability.

**Why it matters for NeuroAgent.** ReAct is the literal algorithmic foundation of
NeuroAgent's orchestrator (the "ReAct loop, up to 15 turns" in `CLAUDE.md`). It must be cited
as the method NeuroAgent implements and extends to a clinical, multi-tool, cost-aware setting.
Its core claim — that actions/tools curb hallucination — is the mechanism by which
NeuroAgent's diagnostic tools are expected to improve safety.

#### 18. Schick et al. (2023) — Toolformer: language models can teach themselves to use tools
**Relevance 6.5/10** · `schick2023toolformer` · NeurIPS 2023
[arXiv](https://arxiv.org/abs/2302.04761) · PDF: [`pdfs/18_schick2023toolformer.pdf`](./pdfs/18_schick2023toolformer.pdf) *(arXiv 2302.04761)*

**Summary & main findings.** Toolformer shows an LLM can teach itself, in a self-supervised
way from a handful of demonstrations per API, to decide **which** external tools to call,
**when**, with **what arguments**, and how to fold results into generation. With a calculator,
a QA system, two search engines, a translation system and a calendar, it achieves
substantially better zero-shot performance — often competitive with much larger models —
**without degrading core language modeling**.

**Why it matters for NeuroAgent.** The seminal demonstration that tool use fixes LLMs'
*systematic* weaknesses (arithmetic, factual lookup) — the general principle behind
NeuroAgent's 12 diagnostic tools. It is method background that motivates why tool
augmentation, not raw scale, is the right lever for reliable clinical computation.

### Theme E — Neurology-specific evidence & tool grounding

#### 19. Barrit et al. (2025) — Specialized LLM outperforms neurologists at complex diagnosis
**Relevance 8.0/10** · `barrit2025neurology` · *Brain Sciences* 15(4):347
[DOI](https://doi.org/10.3390/brainsci15040347) · PDF: [`pdfs/19_barrit2025neurology.pdf`](./pdfs/19_barrit2025neurology.pdf) *(repository copy via UNIL Serval; open-access article)*

**Summary & main findings.** Deploys GPT-4 Turbo through "Neura," an infrastructure with a
**dual long-term / short-term memory database** over a curated neurological corpus, and tests
it blind against 13 neurologists on five complex neurological scenarios (differential then
final diagnosis). The AI scored **86.17% vs 55.11%** for neurologists (p<0.001) — 85% vs
46.15% for differentials, 88.24% vs 70.93% for final diagnoses — responded in **<30 s vs
~9 min**, and produced only relevant references with no detected hallucination. (Evaluation
scale is small: five scenarios, 20 AI evaluations.)

**Why it matters for NeuroAgent.** The single most domain-aligned paper — neurology-specific —
and it pairs a **curated knowledge base** with an explicit **dual-memory architecture**,
mirroring NeuroAgent's hospital-protocol grounding and patient-memory components. It is strong
motivating evidence that knowledge-grounded LLMs can reach specialist-level neurological
reasoning; and its tiny sample (n=5 cases) is precisely the limitation that NeuroBench's 516
cases across 20 conditions is designed to overcome.

#### 20. Goodell et al. (2025) — LLM agents can use tools to perform clinical calculations
**Relevance 8.0/10** · `goodell2025calculations` · *npj Digital Medicine* 8(1):163
[DOI](https://doi.org/10.1038/s41746-025-01475-8) · PDF: [`pdfs/20_goodell2025calculations.pdf`](./pdfs/20_goodell2025calculations.pdf) *(published version, open access)*

**Summary & main findings.** Evaluates ChatGPT on 48 medical-calculation tasks and finds
**incorrect responses in one-third of trials**, then tests three agentic augmentations across
10,000 trials: retrieval-augmented generation, a code-interpreter tool, and a set of
**task-specific calculation tools** (OpenMedCalc). Task-specific tools helped most: incorrect
responses fell **5.5-fold (88% → 16%)** for LLaMA-based models and **13-fold (64% → 4.8%)**
for GPT-based models, compared with the un-augmented models.

**Why it matters for NeuroAgent.** Clean, quantified proof that *machine-readable,
task-specific* tools — not RAG or generic code execution — are what overcome LLMs'
clinical-computation failures. This is direct empirical support for NeuroAgent's design choice
of specific diagnostic tools (e.g., `interpret_labs`, clinical scoring) over a general model,
and a template for ablations that isolate the contribution of each tool.

---

## 6. Gap analysis — where NeuroAgent fits

Each gap below is a position NeuroAgent can defensibly claim, grounded in the cited evidence:

1. **No neurology-specific, tool-augmented agent at benchmark scale.** The only
   neurology-specific agentic study, Barrit et al. \[19], used five cases; AgentClinic \[7],
   MedHELM \[9] and MedAgentBench \[10] are cross-specialty. NeuroBench (600 cases, 20
   conditions) plus NeuroAgent's 12 neurology tools fill a genuine void.

2. **Cost-aware agentic evaluation is nascent.** Only Sequential Diagnosis \[11] scores
   monetary cost as a first-class metric; MedHELM \[9] and Liu et al. \[8] account for
   compute cost. NeuroAgent's per-tool Medicare-PFS cost registry extends cost-aware
   evaluation to a multi-tool *neurology* setting — apparently a first.

3. **The value of tool augmentation is genuinely contested.** Ferber \[3] and Goodell \[20]
   show large gains; Liu et al. \[8] and MDAgents \[4] show modest ones. A controlled
   12-tool neurology study with cost accounting can clarify *when and why* tools help —
   a real scientific contribution, not just an engineering one.

4. **Hospital-protocol grounding as an explicit reasoning constraint is essentially absent.**
   The closest analogs are guideline *citation* in Ferber et al. \[3] and a curated knowledge
   base in Barrit et al. \[19]. No surveyed system treats institution-specific pathways as a
   first-class constraint on agent reasoning — NeuroAgent's hospital-rules layer does.

5. **Longitudinal patient memory is shown valuable but rarely built in.** AgentClinic \[7]
   found a persistent-notes tool drove up to 92% relative improvement; Barrit et al. \[19]
   used a dual-memory store. NeuroAgent makes cross-encounter patient memory a first-class
   component rather than an add-on.

6. **Reasoning evaluation is confounded by tool-model accuracy.** Prior agents wire in real
   models (Ferber \[3]) or live web tools (TxAgent \[2]), so a wrong answer can stem from the
   tool, not the reasoning. NeuroAgent's MockServer — clinically realistic, pre-generated,
   modality-faithful tool outputs — decouples *reasoning* evaluation from tool-model accuracy
   and enables controlled noise-injection robustness tests. This is a methodological
   contribution in its own right.

**One-line positioning.** *NeuroAgent is the first tool-augmented, cost-aware,
protocol-grounded ReAct agent for neurological decision support, evaluated on a
benchmark (NeuroBench) purpose-built for sequential, tool-using clinical reasoning — closing
gaps that the 2024–2026 literature leaves open in benchmark realism (\[7]\[8]\[10]),
cost-awareness (\[11]) and neurology coverage (\[19]).*

## 7. PDF inventory and access notes

**17 of 20 PDFs** are in [`pdfs/`](./pdfs/), named `NN_key.pdf` to match the numbering above.
Sources, in priority order: arXiv, publisher open-access (Springer Nature OA, ACL Anthology,
MDPI), institutional repositories (NSF PAR, UNIL Serval). Each PDF's exact version (published
vs. preprint vs. accepted manuscript) is annotated in §5.

**Three papers could not be downloaded automatically from this environment:**

| # | Paper | Reason | How to obtain |
|---|-------|--------|---------------|
| 1 | Qiu et al. — agentic systems in medicine | Paywalled *NMI* Comment; **no preprint exists** (Unpaywall: `is_oa = false`) | Institutional access via [doi.org/10.1038/s42256-024-00944-1](https://doi.org/10.1038/s42256-024-00944-1) |
| 14 | Liu et al. — MedFound | Paywalled *Nature Medicine*; **no preprint exists** (Unpaywall: `is_oa = false`) | Institutional access via [doi.org/10.1038/s41591-024-03416-6](https://doi.org/10.1038/s41591-024-03416-6) |
| 16 | Sandmann et al. — DeepSeek benchmark | **Open access (green)**, but the only OA copy is on PMC/Europe PMC, whose PDF endpoints blocked automated download from this environment | Free PDF: [PMC12353792](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12353792/) — opens directly in a browser |

For #16 the article *is* freely available; only the sandbox could not reach NCBI. Papers #1
and #14 are genuinely behind a paywall with no legal free version — institutional or library
access is required.

## 8. Validation notes

- Metadata (titles, authors, venues, volumes/pages, DOIs) cross-checked against **CrossRef**,
  the **arXiv API**, **Semantic Scholar** and **Europe PMC** on 2026-05-22.
- Every summary's quantitative claims are quoted from the paper's own **abstract or full
  text**; no figure is taken from a secondary description.
- Notable correction made during validation: the model **MedFound** is the paper *"A
  generalist medical language model for disease diagnosis assistance"* (`liu2025medfound`,
  Nature Medicine 31(3), DOI 10.1038/s41591-024-03416-6) — early web results had conflated it
  with a different Nature Medicine article. The citation here is the verified one.
- **MedHELM** appeared as an arXiv preprint (2505.23802, May 2025); the version of record is
  *Nature Medicine* 32(3):943–951 (2026) — cited accordingly.
- Relevance scores are this review's own assessment against the rubric in §2 and reflect
  fit to NeuroAgent specifically, not general paper quality or citation count.
