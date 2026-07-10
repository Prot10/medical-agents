# Proposal — Localization-First Neurological Diagnostic Reasoning

### A neurology-native reasoning architecture for NeuroAgent

*Research memo · 2026-05-22 · status: novelty validated against the literature · companions: `reasoning-frameworks-research.md`, `references.bib`*

> **What this is.** A proposed reasoning framework that is genuinely **specific to NeuroAgent's neurological use case** — not a rearrangement of general-purpose agent parts. It replaces the linear ReAct loop with the two-axis reasoning structure that *defines* the specialty of neurology. The novelty has been pressure-tested with targeted web searches (the validation log is §11); this memo states honestly what is and is not new.

---

## 1. The core idea in one paragraph

Neurological diagnosis does not work like internal-medicine diagnosis. Before asking *"what disease is this?"*, a neurologist answers two prior questions that internal medicine has no analogue for: **"where is the lesion?"** (anatomical **localization** along the neuraxis) and **"how did it evolve?"** (the **tempo** of onset and course). The intersection of those two axes — a (localization × tempo) cell — *generates and sharply prunes* the etiological differential, and it dictates **which investigations are even worth ordering**. NeuroAgent should be architected around that structure: a reasoning framework in which **localization and tempo are explicit, probabilistic, first-class stages** that (1) condition the etiological hypothesis space and (2) drive a **localization-aware, cost-aware test-selection policy**. Every general-purpose diagnostic agent in the literature — MAI-DxO, ACTMED, AMIE — is anatomy-agnostic and built for general medicine; none embeds this structure. That gap is the contribution.

---

## 2. Validation — what is and is not novel

The user's instruction was explicit: *validate online, do not hallucinate.* This section reports the result of ~14 targeted searches (full log in §11).

| Component / claim | Status | Evidence |
|---|---|---|
| Localization-based neurological diagnosis as a clinical method | **Established (textbook)** — *not* claimed as novel; it is the clinical grounding | [Berkowitz, *Clinical Neurology and Neuroanatomy: A Localization-Based Approach*](#); standard StatPearls / curriculum materials |
| LLMs *evaluated on* lesion localization | **Done** | [Lee et al., 2024](https://www.neurology.org/doi/10.1212/CPJ.0000000000200293) — GPT-4 reaches F1 ≈ 0.85 for brain region; several similar eval papers |
| Multi-agent LLM system for neurology reasoning | **Done** — but generic | [Sorka et al., *PLOS Digital Health*, 2025](https://journals.plos.org/digitalhealth/article?id=10.1371/journal.pdig.0001106): 5 generic agents (complexity classifier → interpreter → retrieval → synthesis → validator), **multiple-choice answering**, *no* localization stage, *no* tempo stage, *no* sequential test selection |
| VOI / cost-aware sequential test selection | **Done** | [ACTMED](https://arxiv.org/abs/2510.18988) (van der Schaar, NeurIPS 2025); [MAI-DxO](https://arxiv.org/abs/2506.22405) |
| Longitudinal multi-encounter diagnosis | **Done / crowded (2026)** | TRACE (arXiv 2602.12833); CARE-AD (*npj Digital Medicine*, 2025) |
| Counterfactual diagnostic hypothesis testing | **Done** | [You et al., 2026](https://arxiv.org/abs/2603.27820) — counterfactual case *editing* |
| **An LLM diagnostic *agent* architected around localization × tempo as first-class stages that jointly generate the etiology space *and* condition a sequential, cost-aware test-selection policy** | **OPEN — not found** | No hit across ~14 searches; the closest work (Sorka et al.) explicitly does none of the three (localization stage, tempo stage, test selection) |

**Precise novelty claim.** *To our knowledge, no existing LLM diagnostic agent makes anatomical localization and temporal tempo explicit, probabilistic, first-class reasoning stages that jointly generate the etiological hypothesis space and condition a sequential, cost-aware diagnostic-test-selection policy.*

**Honest calibration of strength.** This is **architectural novelty grounded in domain-specific reasoning structure** — not a new universal reasoning primitive (the prior round of validation found those are essentially exhausted: predict-then-test, abduction, VOI, multi-agent, world models, active inference are all published). It is a legitimate *Nature Machine Intelligence*–grade contribution **when paired with** NeuroBench evaluation and clinician validation, because (a) it is the first agent to embed the specialty's actual reasoning structure, (b) it yields measurable wins a general agent cannot (localization-appropriate test selection, an interpretable localization artifact), and (c) the general-purpose incumbents (Microsoft, Google, van der Schaar) optimize for general medicine and have no incentive to build it. It also draws decades-old precedent honestly: pre-LLM expert systems for neuroanatomical localization existed — the novelty is the **modern LLM tool-using agent** architecture, not the clinical idea. A formal systematic related-work review is still required before paper submission.

---

## 3. The clinical foundation

### 3.1 Neurology's two reasoning axes

General-medicine diagnostic agents reason on a single axis: *symptoms → disease probabilities*. Neurology adds two structural axes that come **before** etiology:

**Axis 1 — Localization (the spatial axis).** Driven by the neurological exam. The neuraxis, distal → proximal:

```
muscle → neuromuscular junction → peripheral nerve → nerve root/plexus
   → spinal cord → brainstem → cerebellum → subcortical/deep → cortex
        (+ meninges/CSF spaces)        (+ laterality: L / R / midline / bilateral)
                                       (+ extent: focal / multifocal / diffuse)
```

**Axis 2 — Tempo (the temporal axis).** Driven by the history:

| Tempo class | Time scale | Etiologies it favours |
|---|---|---|
| Hyperacute | seconds–minutes | vascular (ischemia/hemorrhage), seizure |
| Acute | hours–days | vascular, early inflammatory/infectious |
| Subacute | days–weeks | inflammatory, infectious, neoplastic, toxic-metabolic |
| Chronic-progressive | months–years | neurodegenerative, neoplastic, genetic |
| Relapsing–remitting | discrete episodes, incomplete recovery | demyelinating (MS) |
| Paroxysmal | recurrent, stereotyped, full recovery | epilepsy, migraine, TIA, channelopathy |

**The grid.** The (localization × tempo) cell is the diagnostic engine. *Anterior horn + corticospinal, motor-pure, multifocal* × *chronic-progressive* → motor neuron disease. *Optic nerve / cord / brainstem, multifocal* × *relapsing* → multiple sclerosis (this **is** the McDonald criteria: dissemination in space and time — [Thompson et al., 2018](#)). *Cortex* × *hyperacute* → stroke or seizure. The cell does not just rank diseases — it **excludes** whole categories and **names the test that matters**.

### 3.2 Why general-purpose agents structurally cannot do this

[MAI-DxO](https://arxiv.org/abs/2506.22405), [ACTMED](https://arxiv.org/abs/2510.18988) and [AMIE](https://www.nature.com/articles/s41586-025-08866-7) reason directly from findings to a disease posterior. They have **no spatial state** — no representation of *where* the lesion is — so their test selection is generic information-gain over all tools. They cannot encode that a suspected cord lesion makes a brain MRI nearly worthless and a spine MRI essential, because they have nothing that says "cord." NeuroAgent's 12 tools are, in fact, **a neuraxis instrument set** — that asset is wasted by an anatomy-agnostic policy.

---

## 4. The architecture

This framework is the [Diagnostic Hypothesis Graph (Proposal A of `reasoning-frameworks-research.md`)](./reasoning-frameworks.md) **with a localization × tempo spine** — it builds on, and does not discard, that earlier design.

### 4.1 The reasoning state

A typed graph whose backbone is the two axes:

```text
LocalizationState   distribution over neuraxis levels · laterality · extent{focal|multifocal|diffuse}
TempoState          tempo class · onset · trajectory
EtiologyHypothesis  name · illness_script · belief · the (localization,tempo) cell it was generated from
FindingNode         exam/history/test finding · which localization(s) it implies · explained:bool
TestNode            tool + parameters · cost (CostTracker) · localization(s) it can resolve
```

### 4.2 The reasoning loop (replaces the ReAct loop)

1. **Localize.** From the exam (`PatientProfile`), the LLM emits a *probability distribution* over neuraxis localizations (+ laterality, + extent). Findings that conflict are surfaced, not averaged away.
2. **Characterize tempo.** From the history, classify the temporal profile.
3. **Generate etiologies — constrained.** The (localization × tempo) cell conditions the LLM to propose *only* etiologies consistent with that cell (illness scripts — [Schmidt et al., 1990](#)), including the cell's **can't-miss** entries.
4. **Select tests — localization-aware + cost-aware.** Candidate tools are first **filtered by the tool→localization map** (§4.3), then ranked by discrimination value ÷ `CostTracker` cost. This is the key mechanism: the spatial state *gates* the test policy.
5. **Reconcile.** Each result updates etiology beliefs **and** is checked for coverage: does the current (localization, etiology) explain *every* finding? An unexplained finding triggers **revise localization**, **revise tempo**, or **add a second localization** — which is multi-fault diagnosis (§4.4).
6. **Stop** when one (localization, tempo, etiology) explains all findings above a confidence threshold and the cell's can't-miss etiologies are excluded.

### 4.3 Localization-aware tool selection — the key mechanism

NeuroAgent's 12 tools map onto the neuraxis. This map is the test policy:

| Suspected localization | Localization-appropriate tools (of the 12) |
|---|---|
| Cortex | `analyze_brain_mri`, `analyze_eeg` |
| Subcortical / basal ganglia | `analyze_brain_mri`, `order_advanced_imaging` (DaTscan, FDG-PET) |
| Brainstem | `analyze_brain_mri`, `order_specialized_test` (BAEP) |
| Cerebellum | `analyze_brain_mri`, `order_advanced_imaging` |
| Spinal cord | spine `analyze_brain_mri`/`order_advanced_imaging`, `order_specialized_test` (SSEP) |
| Nerve root / plexus | `order_specialized_test` (EMG/NCS), MRI |
| Peripheral nerve | `order_specialized_test` (EMG/NCS), `analyze_csf` (e.g. GBS), `interpret_labs` |
| Neuromuscular junction | `order_specialized_test` (repetitive nerve stimulation), `interpret_labs` (AChR/MuSK antibodies) |
| Muscle | `order_specialized_test` (EMG), `interpret_labs` (CK) |
| Optic / visual pathway | `order_specialized_test` (VEP), MRI |
| Meninges / CSF | `analyze_csf` |
| Cardioembolic source (cortex × hyperacute → stroke) | `analyze_ecg`, `order_echocardiogram`, `order_cardiac_monitoring`, `order_advanced_imaging` (carotid duplex) |

A generic agent, anchored on "progressive weakness," may order a brain MRI first. A localization-first agent that has localized to the **anterior horn cell** orders **EMG/NCS** — the actually-confirmatory test. That difference is directly measurable on NeuroBench (`GroundTruth.optimal_actions`).

### 4.4 Multi-fault via multifocal localization

Most LLM diagnostic systems output one disease. Here, comorbidity is *structural*: if a finding cannot be explained by the current localization, the agent posits a **second localization**. Multiple localizations + a relapsing tempo = **dissemination in space and time** — literally the diagnostic criteria for MS ([Thompson et al., 2018](#)). The architecture's reconciliation step (§4.2, step 5) makes multi-fault the default behaviour, not a special case.

---

## 5. Worked example (an ALS-type NeuroBench case)

- **Presentation:** progressive limb weakness over 8 months; exam shows atrophy + fasciculations (lower motor neuron) **and** hyperreflexia + spasticity (upper motor neuron), in bulbar, cervical and lumbar regions; **no sensory loss**; cognition intact.
- **Stage 1 — Localize:** mixed UMN + LMN signs, **motor-pure**, across **multiple regions** → localization = *anterior horn cell + corticospinal tract, multifocal, motor-only*. The absence of sensory findings is itself a strong localizing fact.
- **Stage 2 — Tempo:** chronic-progressive.
- **Stage 3 — Etiologies (constrained by the cell):** motor neuron disease / ALS (dominant). The localization *excludes* major mimics: cervical spondylotic myelopathy (would give a sensory level — absent), multifocal motor neuropathy (LMN only, no UMN — contradicted), myasthenia gravis (NMJ, fatigable, no atrophy/UMN — contradicted).
- **Stage 4 — Localization-aware tests:** the anterior-horn localization → **EMG/NCS** (`order_specialized_test`) as the confirmatory test for widespread denervation; **MRI** is ordered *specifically to exclude* a compressive structural mimic, not as a first reflex.
- **Outcome:** the right diagnosis, the right confirmatory test, and an auditable trail — the localization is the explanation.

---

## 6. Why it should work

- **It is the specialty's actual method.** Localization-based diagnosis is how neurology is taught and practised ([Berkowitz textbook](#)); the architecture mirrors expert cognition (hypothetico-deduction — [Elstein et al., 1978](#); illness scripts — [Schmidt et al., 1990](#)) rather than imposing a generic loop.
- **Localization massively prunes the search.** Fixing *where* collapses a differential of dozens to a handful — faster, more accurate, and fewer wasted tool calls.
- **It fixes a real ReAct failure.** Anatomy-agnostic test selection orders localization-inappropriate tests; a localization-gated policy does not. This is directly measurable against `GroundTruth.optimal_actions`.
- **Multi-fault is free.** Multifocal localization yields comorbidity handling that single-label systems lack.
- **It is auditable by construction.** The localization distribution and the (localization × tempo) cell are a native, clinician-legible explanation — far better than a ReAct transcript.

---

## 7. How to build it in NeuroAgent

- Implement as a `GraphOrchestrator` (the Proposal-A `DiagnosticGraph` with `LocalizationState` + `TempoState` added), alongside the existing `AgentOrchestrator`.
- Reuse unchanged: the 12-tool layer, `ToolRegistry`, `CostTracker`, `RulesEngine`, `MockServer`, `AgentTrace`.
- The **tool→localization map** (§4.3) is a small static config (a YAML, like `tool_costs.yaml`).
- Localization and tempo are produced by dedicated LLM calls with their own tight system prompts; numeric belief updates and the VOI ÷ cost ranking are pure Python.
- Exam data already lives structured in `PatientProfile`; `format_patient_info()` stays the single source of truth for presentation.

---

## 8. Coupling with fine-tuning

The architecture creates **two verifiable intermediate supervision signals** that free-form ReAct cannot:

- **Localization accuracy** — the localization papers ([Lee et al., 2024](#)) prove this is annotatable and measurable; NeuroBench `GroundTruth` conditions imply a ground-truth localization per case.
- **Tempo classification** — derivable from each case's history.

This turns one sparse end-of-episode reward into **process-level supervision** (localize → tempo → etiology → test), the regime where process reward models beat outcome-only training ([Let's Verify Step by Step](#)). RLVR/GRPO ([HuatuoGPT-o1](#), [Med-R1](#)) can then use a composite verifiable reward: localization correctness + etiology correctness + localization-appropriate test recall − contraindicated actions − cost overrun.

---

## 9. Evaluation & the paper narrative

- **New intermediate metric:** localization accuracy (and tempo accuracy) — an interpretable, per-stage score no end-to-end system reports.
- **Localization-appropriate test rate:** fraction of ordered tests that match the localization (against `GroundTruth.optimal_actions`).
- Plus the standard axes: diagnostic accuracy, cost / accuracy-per-dollar, safety, calibration, robustness to `red_herrings`.
- **Comparators:** bare frontier model · current ReAct NeuroAgent · a re-implemented MAI-DxO-style panel · ablation = this framework **without** the localization spine (isolates the contribution).
- **The narrative:** *general-purpose diagnostic agents ignore the reasoning structure of the specialty; embedding neurology's localization × tempo structure into the agent improves accuracy, cost-efficiency, test appropriateness, and interpretability — validated on NeuroBench with clinician review.*

---

## 10. Honest risks & limitations

| Risk | Mitigation |
|---|---|
| A wrong localization propagates downstream | Keep localization a *distribution*, not a point; the reconciliation step (§4.2-5) can revise it; the Skeptic role from Proposal C can audit it. |
| Localization ground truth needs annotating for training/eval | Derivable from `GroundTruth` conditions; LLM-assisted pre-labelling + clinician review; localization is a well-defined, teachable label. |
| Some presentations are genuinely non-localizable (functional, diffuse, psychiatric) | Make "non-localizable / functional" an explicit localization class — itself diagnostically informative. |
| Novelty is architectural, not a universal new primitive | Stated honestly (§2); pair with strong evaluation + the NeuroBench benchmark contribution; do a formal systematic related-work review before submission. |

---

## 11. Validation log (transparency)

Searches run across this investigation and reported honestly:

- *predict-then-test / VOI test selection* → **taken** (ACTMED, NeurIPS 2025; CuriosiTree; Curious Language Model).
- *counterfactual diagnostic reasoning with LLMs* → **taken** ([You et al., 2026](https://arxiv.org/abs/2603.27820) — case editing).
- *abductive reasoning in LLMs* → now has a survey (arXiv 2604.08016) → **not open as a bare concept**.
- *multi-fault / comorbid diagnosis* → benchmarks exist (ANGST, MSDiagnosis) → **partly contested**.
- *world models for medical diagnosis* → world-model papers exist but explicitly for prognosis/planning, **not diagnosis** (arXiv 2511.16333).
- *longitudinal multi-encounter diagnosis* → **crowded** (TRACE arXiv 2602.12833; CARE-AD).
- *LLM lesion localization* → **evaluation papers only** ([Lee et al., 2024](https://www.neurology.org/doi/10.1212/CPJ.0000000000200293)); no agent architecture.
- *multi-agent neurology reasoning* → [Sorka et al., 2025](https://journals.plos.org/digitalhealth/article?id=10.1371/journal.pdig.0001106) — generic agents, MCQ task, **no localization/tempo stages, no test selection**.
- *localization × tempo agent architecture with localization-conditioned test selection* → **no result found** → the basis for this proposal.

Caveat: ~14 targeted searches is a strong signal but not a systematic review; the architecture-vs-evaluation gap was consistent across every neuro-localization search.

---

## 12. References

In `references.bib`. Key entries for this proposal: `[sorka2025multiagent]` · `[lee2024localization]` · `[estevez2025actmed]` (ACTMED) · `[nori2025sequential]` (MAI-DxO) · `[you2026counterfactual]` · `[berkowitz2022localization]` · `[thompson2018mcdonald]` (McDonald criteria) · `[elstein1978medical]` · `[schmidt1990illnessscripts]` · `[croskerry2009universal]` · `[besta2024got]` · `[chen2024cod]` · `[lightman2024verify]` · `[chen2024huatuogpt]`.

---

*Bottom line: a genuinely novel idea on a saturated landscape is best found by going **specific**, not general. Localization-first reasoning is novel precisely because it is neurological — it is NeuroAgent's structural advantage, and no general-purpose competitor will build it.*
