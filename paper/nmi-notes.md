# Nature Machine Intelligence: what it wants and what reviewers ask (17 Nov 2026)

Collected on 17 Nov 2026 from four web searches: NMI's official pages and editorials, the published
reviewer reports of 8 Nature / Nature Communications articles and 5 NMI articles, and the figures of
about 25 papers close to ours. Every point has its source. "NMI" marks a rule of this journal;
"Nature" marks a rule shared by all Nature Portfolio journals. Decisions taken from here are recorded
in `decisions.md`.

## 1. What the editors look at

- To send a paper to review they weigh four things: how far it advances the field, whether the
  conclusions are sound, whether the evidence supports them, and whether it interests a wide
  readership (NMI,
  [editorial process](https://www.nature.com/natmachintell/submission-guidelines/editorial-process)).
- After review, rejection is almost always for "insufficient support for the conclusions" or because
  the reviewers lowered the perceived interest or advance (same page).
- Reviewers are asked: are the results of immediate interest to many people, also in other fields?
  Are they reproducible? Are error bars and statistical tests described correctly?
  ([peer review](https://www.nature.com/natmachintell/editorial-policies/peer-review)).
- High priority: papers must be accessible to non-specialists; after acceptance they are edited in
  that direction ([AIP and formatting](https://www.nature.com/natmachintell/submission-guidelines/aip-and-formatting)).
- Medicine and diagnosis are named explicitly in the journal's scope
  ([aims](https://www.nature.com/natmachintell/aims)).
- There is no "Benchmark" or "Resource" type: we are an **Article** ("a substantial novel research
  study, with a complex story often involving several techniques or approaches"). Benchmarks are
  published as Articles: MedPerf (2023), the laboratory-safety benchmark (January 2026)
  ([content types](https://www.nature.com/natmachintell/content-types),
  [lab safety](https://www.nature.com/articles/s42256-025-01152-1)).
- Timing: first decision in 10 days (median), acceptance in 231 days (median); the lab-safety
  benchmark took 6 months ([journal impact](https://www.nature.com/natmachintell/journal-impact)).
- NMI does not accept presubmission enquiries.

### NMI editorials that bear directly on this paper

| Editorial | What it says | For us |
|---|---|---|
| [What is in your LLM-based framework?](https://www.nature.com/articles/s42256-024-00896-6) (Aug 2024) | exact models and versions with access dates, prompts and example outputs, "ideally open-source LLMs" | our small open models count in our favour; publish prompts and versions |
| [Multi-agent AI systems need transparency](https://www.nature.com/articles/s42256-026-01183-2) (Jan 2026) | document workflows, versions, prompts; ablate the components; is the compute cost justified? compare with expert workflows | ablations (controls in ED), cost on one GPU (Fig. 6), physician vs agent (Fig. 4) |
| [Recognizing reproducibility and reusability](https://www.nature.com/articles/s42256-026-01219-7) (Mar 2026) | the editor assesses the repository: ReadMe, dependencies, checkpoints and models; Code Ocean encouraged; LLM outputs are not deterministic | a clean repository with the weights of models A and B (not those trained on MIMIC), seeds stated |
| [Stop 'tokenmaxxing'](https://www.nature.com/articles/s42256-026-01253-5) (May 2026) | verifying agent output will still need substantial human work | supports the blind physician ratings |
| [Towards understanding and monitorability of reasoning LLMs](https://www.nature.com/articles/s42256-026-01333-6) (Oct 2026) | written reasoning is not a faithful explanation, clinical decisions included | supports not persisting free-form reasoning and keeping thinking off |
| [Algorithmic recommendations, anyone?](https://www.nature.com/articles/s42256-023-00631-7) (Feb 2023) | against leaderboard chasing; several metrics, a fixed compute budget | the multi-component score and the cost term point the same way |

There is no NMI editorial dedicated to clinical LLM benchmarks.

## 2. Formal rules (Article)

- **Text:** at most 3,500 words (abstract, Methods, references and legends excluded); abstract at most
  150 words, no references; at most 6 figures and tables; about 50 references (guidance). Order:
  introduction without a heading, Results, Discussion without subheadings, Methods
  ([content types](https://www.nature.com/natmachintell/content-types)).
- **Methods:** no word limit stated by NMI; "as concisely as possible" but with everything needed to
  replicate.
- **Extended Data:** at most 10 items, one page each, not copy-edited. **Supplementary Information:** a
  single PDF, also read by the reviewers.
- **Figures:** at least 300 dpi, at most 180 mm wide, sans-serif text of 5–7 pt not flattened into the
  image. Legends must state the centre value, how error bars were computed, n, the test and the P
  values ([AIP and formatting](https://www.nature.com/natmachintell/submission-guidelines/aip-and-formatting)).
- **First submission:** any format (a PDF is fine); double-anonymized review is optional and the
  authors do the anonymizing.
- **Reporting Summary (Nature):** required for clinical research; the editor asks for it when the paper
  goes to review. On statistics it asks for exact n, repeated or independent measures, the test and
  whether one- or two-sided, correction for multiple comparisons, confidence intervals, effect sizes,
  **exact P values** ([form](https://www.nature.com/documents/nr-reporting-summary-flat.pdf)).
- **Code (Nature; NMI is strict about it):** shared with editors and reviewers; a "Code availability"
  section; on publication, deposited in an archive with a DOI (Zenodo or Code Ocean) under an
  open-source licence. The code is reviewed: README, installation guide with times, demo on example
  data with run times, licence
  ([reporting standards](https://www.nature.com/natmachintell/editorial-policies/reporting-standards),
  [code guidelines](https://www.nature.com/documents/GuidelinesCodePublication.pdf)).
- **Controlled-access data (MIMIC):** the "Data availability" section must say why access is
  controlled, how to obtain it, how long it takes and under which restrictions (the PhysioNet
  agreement). NMI says nothing specific about MIMIC: cite the PhysioNet agreement and the original
  ethics-committee waiver (our inference).
- **Use of AI by the authors:** green (language polishing), amber (analysis suggestions: disclose),
  red (undisclosed AI reasoning). Every use of an LLM must be described in the Methods
  ([AI policy](https://www.nature.com/natmachintell/editorial-policies/ai)).
- **Preprints:** encouraged; they do not count against novelty.
- **Transparent peer review:** at the end of review the authors choose whether the reviewer reports
  are published.
- **Cover letter:** why the work matters and why it suits NMI's readership; related manuscripts;
  reviewers to suggest or exclude. Reviewers do not see it.

## 3. Clinical reporting guidelines

| Guideline | Does it apply? |
|---|---|
| **MI-CLAIM-GEN** (Miao et al.) | Yes: the only one NMI names for clinical AI; attach the checklist ([clinical research](https://www.nature.com/natmachintell/editorial-policies/clinical-research)) |
| TRIPOD / TRIPOD-AI | NMI requires it for diagnostic prediction models; **TRIPOD-LLM** (Nat Med 2025) is the LLM extension: attach it as a precaution |
| STARD-AI (Nat Med 2025) | possible for the external MIMIC test (diagnostic accuracy) |
| CONSORT-AI, DECIDE-AI | No: they cover clinical trials and live clinical use |

## 4. What reviewers actually ask

From 8 reviewer reports read in full: Med-PaLM (Nature 2023), AMIE (Nature 2025, two papers),
DeepSeek-R1 (Nature 2025), MedR-Bench (Nat Commun 2025), a biomedical NLP benchmark (Nat Commun 2025),
MIRA (Nature 2026, an agent that orders tests on health records: the closest to us), AMIE-Mx (Nature
2026). Nature Medicine and Nature Cancer do not publish reviewer reports. The NMI ones are in
section 4b.

Recurring requests, most frequent first:

1. **Release code, cases, gold labels, prompts and case-level outputs** (7 of 8).
2. **Validate automatic judges against clinicians, and avoid judges or generators from the same model
   family as the system under test** (6). For us: the cases are generated by an LLM and the agent is
   an LLM; the translation of free-text requests uses GLM-5.3. State it and show agreement with
   physicians.
3. **Quality of the human raters** (6): how many, their experience, agreement between them, training;
   a human reference as a ceiling.
4. **Contamination** (6): can the cases or conditions be in the pre-training data? Fresh or held-out
   data.
5. **Ablations and current baselines that show where the gain comes from** (6): prompting only, SFT
   only, other base models, recent open and closed models. DeepSeek-R1 had to add non-RL baselines
   and PPO vs GRPO.
6. **Tone down the claims** (6): "outperforms physicians" and "expert level" were challenged
   everywhere.
7. **Proper statistics** (6): tests on the differences, paired non-parametric tests (Wilcoxon,
   McNemar), correction for multiple comparisons (FDR), error bars everywhere.
8. **Realism of the simulation** (5): patients who report everything perfectly, clean single-diagnosis
   cases, "N/A" answers to tests nobody planned, no healthy cases. For us: the library of normal
   reports must be explained and judged by physicians.
9. **Over-testing, efficiency, cost** (5): MIRA had to add precision and a penalty for unnecessary
   tests, and compare itself with MAI-DxO. That is exactly what our score measures: a strength to put
   forward.
10. **Error analysis by difficulty, case type and subgroup, and why the method works** (5).
11. **Positioning against prior work** (5): for agents, reviewers named HealthBench, AMIE, MAI-DxO.
12. **Validity of the ground truth** (5): several strategies can be acceptable; guidelines must hold
    where the physicians practise.
13. **Variability across runs, prompts and seeds** (4).
14. **Safety and robustness to perturbed patients** (4).
15. **Evaluate the process, not only the final answer** (3): an error in the work-up counts even when
    the diagnosis is right. For RL: describe the reward and show whether there is reward hacking.

### The objection that will certainly come: circularity

Model A is trained on the policy score and we also evaluate it with the policy score. How others
handled this:
- **independent human ground truth** (Uesato 2022: reasoning error from human labels; AMIE: the
  headline results come only from blinded specialists);
- **measures outside the reward** (DeepSeek-R1: many benchmarks the reward never sees);
- **held-out data** (Med-RLVR, SDBench).

For us: every model scored with **both** rewards and with measures that are in neither (diagnosis on
unseen conditions, cost, tests per case, unsafe actions), plus the **blind physician ratings**
(Fig. 4). Model B must not look like a weak opponent: it should win on its own reward, and its cost
weight must be justified.

## 4b. Nature Machine Intelligence specifically

NMI publishes reviewer reports only when the authors opt in at the end of review: no NMI paper on
LLMs up to November 2025 has them, many from 2026 do. Usually 2–3 reviewers.

### NMI papers close to ours

URL: `https://www.nature.com/articles/<id>`. F = figures, T = tables, ED = Extended Data, PRF =
published reviewer reports.

| Paper (id) | Year | Main | ED | PRF | Why it matters for us |
|---|---|---|---|---|---|
| **PsychFound**, an LLM for psychiatry (s42256-026-01224-w) | 2026 | 6F | 5F + 4T | yes | the closest: a 7B model trained (RL included) + its own benchmark + a clinician study. Fig. 3 score against parameter count for 22 LLMs; Fig. 4 comparison judged by 3 LLMs and 2 psychiatrists; Fig. 5 ablation of the training stages |
| **MatBrain**, two small Qwen3 models trained with RL (s42256-026-01298-6) | 2026 | 6F | — | no | compared with the same untrained base model, diagnoses entropy collapse: like our A vs base |
| **LabSafety Bench** (s42256-025-01152-1) | 2026 | 6F | 1 | no | a pure benchmark published as an Article; a panel with Llama3-8B trained on different data |
| **KaBLE**, belief vs knowledge (s42256-025-01113-8) | 2025 | 6F | — | no | benchmark + evaluation, Article |
| VLMs on neuropsychological tests (s42256-026-01179-y) | 2026 | 3F | — | yes | performance against human norms |
| LLMs as judges of empathy (s42256-025-01169-6) | 2026 | 3F + 2T | 6 | yes | inter-rater agreement (weighted kappa) between experts and LLMs |
| Agentic X-ray scientist (s42256-026-01261-5) | 2026 | 4F + 2T | 3 | yes | LLM agent with tools |
| Capable LMs outgrow multi-agent collaboration (s42256-026-01268-y) | 2026 | 3F + 3T | 2 | no | cost against performance in ED |
| Chemma, 7B with SFT + reward model + RLHF (s42256-025-01066-y) | 2025 | 5F | 10 | no | uses all 10 ED items |
| ChemCrow, LLM with chemistry tools (s42256-024-00832-8) | 2024 | 5F | — | no | the LLM judge disagreed with the experts |
| MedPerf, federated benchmarking of medical AI (s42256-023-00652-2) | 2023 | 4F + 3T | — | no | a medical benchmark as an Article |

NMI papers put these in Extended Data: full leaderboards, error analyses, robustness to
perturbations, cost against performance, reasoning traces, study-design diagrams.

### What NMI reviewers asked (5 reports read)

- **PsychFound** (the closest):
  - prove that the benchmark cases are not in the training or RL data (deduplication, a temporal
    split, a similarity check), because the authors had built the benchmark themselves;
  - confirm the LLM judge's verdicts with humans on a subset, and try another judge;
  - count unsafe or guideline-inconsistent recommendations (for example contraindicated
    interactions), with an error taxonomy;
  - in the clinician study: clustering by physician, blinding, a power calculation;
  - error bars in every panel; technical details consistent between text and Methods.
- **VLMs on neuropsychological tests:** make it a usable public benchmark (the authors added an
  automated pipeline on the non-proprietary tests); README and demo too sparse.
- **LLMs as judges of empathy:** vary the prompts and measure repeatability; construct validity; a
  summary of the robustness checks in the main text.
- **Agentic X-ray scientist:** is it more than prompt engineering? "Code released upon acceptance" is
  not enough; 5 trials are too few (repeats, temperature 0); compare with human experts on time and
  commands; **test open, small models (<20B) for local use**; requests, context, time and cost per
  run; drop the "first" claims and grand names.
- **Cardiac foundation model:** compare with more models of the same kind; demographics and bias;
  inference cost; distinguishable colours in the figures.

Common to all: contamination checks, human validation of every LLM judge, repeats and variance, fair
baselines (same base model, humans), open and small models, **code available already during review**,
claims proportionate to the evidence, null results stated in the abstract.

### More NMI editorials and comments

- [LLM-based agentic systems in medicine and healthcare](https://www.nature.com/articles/s42256-024-00944-1)
  (Comment, Dec 2024): opportunities for medical agents, rules needed for safe use. Cite in the
  introduction.
- [Clinical large language models with misplaced focus](https://www.nature.com/articles/s42256-024-00929-0)
  (Correspondence, 2024): Med-PaLM-style multiple-choice tests do not reflect real diagnosis, which is
  asking questions and integrating information; closed models change over time. **This is our
  motivation, written in NMI: cite it.**
- [Foundation models in healthcare require rethinking reliability](https://www.nature.com/articles/s42256-024-00924-5)
  (Comment, 2024).
- [The rewards of reusable machine learning code](https://www.nature.com/articles/s42256-024-00835-5)
  (Editorial, 2024): introduces Reusability Reports.
- [LLMs displaying less cognitive bias are not necessarily better decision makers](https://www.nature.com/articles/s42256-026-01208-w)
  (Comment, 2026).

### Article type

**Article**: the type of PsychFound, MatBrain and Chemma (benchmark + training) and of LabSafety and
KaBLE (pure benchmarks). "Analysis" is for new analyses without a new method: it does not fit, because
our central result is a training comparison. The publication bar: "an advance in understanding likely
to influence thinking in the field".

Not read: the reviewer reports of three other NMI papers (olympiad geometry s42256-025-01164-x,
implicit bias in reasoning models s42256-026-01300-1, medical image restoration s42256-026-01310-z).

## 5. Figures of close papers

| Paper | What the main figures show | In Extended Data |
|---|---|---|
| [SDBench / MAI-DxO](https://arxiv.org/abs/2506.22405) (Science 2026) | accuracy against cost per case with a Pareto frontier; gain per model with a paired test; validation against test | case × agent map |
| [Hager, Nat Med 2024](https://www.nature.com/articles/s41591-024-03097-1) (MIMIC-CDM) | accuracy against 4 physicians, ± s.d. over 20 seeds; per condition; treatment only on correctly diagnosed patients, with n under each bar | the process errors: physical exam, labs, imaging, instruction errors |
| [MIRA, Nature 2026](https://www.nature.com/articles/s41586-026-10675-5) | robustness of the simulator; accuracy for 8 conditions with Wilson CIs and McNemar; test recall per episode (Wilcoxon, corrected); guideline adherence; safety rated by a blinded physician | 10 figures, including a CONSORT diagram of the cases |
| [AMIE, Nature 2025](https://www.nature.com/articles/s41586-025-08866-7) | top-k accuracy with bootstrap CI bands and corrected P; Likert scales, Wilcoxon + FDR | by specialty (neurology n = 32), automatic evaluator against specialists |
| [DeepSeek-R1, Nature 2025](https://www.nature.com/articles/s41586-025-09422-z) | accuracy and response length per RL step | one behaviour ("wait") per RL step |
| [AgentClinic](https://arxiv.org/abs/2405.07960) | static against interactive accuracy: one does not predict the other | — |
| [DiagGym](https://arxiv.org/abs/2510.24654) (test-ordering agent, RL) | reward ablation (diagnosis only against diagnosis + tests) on three base models, 95% CIs | no training curves |
| [Uesato 2022](https://arxiv.org/abs/2211.14275) (process vs outcome) | same final error, very different reasoning error: the closest precedent for our Fig. 3 | — |
| [Baker 2025, OpenAI](https://arxiv.org/abs/2503.11926) | how often the model cheats during training, two conditions overlaid | — |
| [ChemCrow, NMI 2024](https://www.nature.com/articles/s42256-024-00832-8) | the LLM judge disagreed with the experts: an NMI precedent for not trusting automatic judges | — |

Notes: seeds are rare (Lightman uses 3, the medical RL papers none), so our 3 seeds are an asset. No
reward comparison places the models on the accuracy-cost plane: in Fig. 6 that would be new.

## 6. What this means for our figures (17 Nov)

**Fig. 2** (untrained models)
- Kept: one point per model, accuracy against policy score (as AgentClinic Fig. 3), the two rankings,
  100% bars, one worked case.
- Added: a "complete but with useless tests" class in the bars (MIRA: precision besides recall) and
  "n = xx" correct diagnoses next to each bar (Hager: nested denominators).
- Added: the neurologists as a human reference in panel a and as a row in panel c (Hager, MIRA and
  SDBench put clinicians beside the models). They come from the 20–30 cases the physicians solve.

**Fig. 3** (model A vs B vs base)
- a: correct diagnoses and tests per case over training (DeepSeek-R1, Baker).
- b: test results with 7 measures; the independent ones first, then **both** scores (outcome and
  policy), so each model is seen to win on its own and B is not a weak opponent.
- c: per test condition (all the main papers have it; only 4 conditions, so it is mandatory).
- d: the mechanism, with a measure that does not use the policy score: cases solvable from the story
  against cases that need tests.
- Out of the main text: the reward history (ED2) and the single worked case.

## 7. Action points, all in one place (17 Nov)

Each point comes from a request seen in the reports or in the rules above; the source is in
parentheses. When a point is done or decided, tick it here and record it in `decisions.md`.

**Figures**
- [x] Fig. 2: neurologists as a human reference in panel a and a row in the bars of c (Hager, MIRA,
  SDBench put clinicians beside the models). Needs the 20–30 cases solved by the physicians.
- [x] Fig. 2c: a "complete but with useless tests" class and n next to each bar (MIRA; Hager).
- [x] Fig. 3: both scores for every model, independent measures first, per condition, mechanism
  (circularity; Uesato; MIRA; PsychFound).
- [ ] Every panel with error bars, n, test and exact P values in the legend (NMI rules; Reporting
  Summary; PsychFound).
- [ ] Fig. 6 or ED: score against model size (PsychFound Fig. 3) and accuracy against cost with a
  frontier (SDBench; no reward comparison does it yet).
- [ ] ED: CONSORT diagram of the MIMIC cases (MIRA).
- [ ] ED: full leaderboard of all models; error analysis with a taxonomy (PsychFound, MIRA).

**Experiments and analyses**
- [ ] Non-RL baselines: prompting only and SFT on the same episodes (DeepSeek-R1; X-ray agent).
- [ ] Model B with a different cost weight or no cost: the collapse must not depend on that weight
  (MIRA; B must not look like a weak opponent).
- [ ] A second base model trained (ED4 already planned; DeepSeek-R1; PsychFound).
- [ ] Contamination: similarity between training and test cases, and the models' pre-training; the
  split by condition must be measured, not only stated (PsychFound, AMIE, Med-PaLM).
- [ ] The automatic judge that translates free-text requests (GLM-5.3) validated by physicians on a
  sample; state that the cases are generated by an LLM (MIRA, AMIE-Mx, PsychFound).
- [ ] Inter-physician agreement with kappa, number and experience of the reviewers, training (AMIE,
  Med-PaLM).
- [ ] Physicians rate the realism of the cases and of the library's normal reports (MIRA).
- [ ] Repeatability: 3 seeds for everything, and sensitivity to the prompt (NMI empathy paper; Nat
  Commun NLP benchmark).
- [ ] Unsafe actions counted and classified (PsychFound).
- [ ] Statistics: paired tests per case (Wilcoxon, McNemar), Wilson CIs for proportions, Holm or
  Benjamini–Hochberg correction when there are several measures (MIRA, AMIE).
- [ ] Time, number of requests, tokens and cost per episode (X-ray agent; multi-agent editorial).
- [ ] Analysis by case difficulty (AMIE, DeepSeek-R1).

**Text**
- [ ] Introduction: cite the NMI Correspondence "Clinical large language models with misplaced focus"
  and the NMI Comment on agents in medicine (Qiu et al. 2024).
- [ ] Position the work explicitly against SDBench/MAI-DxO, MIRA, AMIE, HealthBench, Hager, DiagGym.
- [ ] Measured claims: no "outperforms physicians", no "first"; null results in the abstract too.
- [ ] Clear limitations: synthetic cases, one diagnosis per case, library normal reports, guidelines
  from a single setting.
- [ ] Methods: exact models and versions with dates, prompts, sampling parameters (editorial "What is
  in your LLM-based framework?"); use of LLMs in writing disclosed (AI policy).

**Submission**
- [ ] Article; cover letter (why it interests NMI readers, reviewers to suggest).
- [ ] Code with README, installation, demo and timings, licence; DOI on Zenodo or Code Ocean;
  available to reviewers already (NMI rules; X-ray agent).
- [ ] Release of cases, policies, prompts, episodes; weights of A and B (not those trained on MIMIC).
- [ ] Data availability for MIMIC with the PhysioNet conditions.
- [ ] MI-CLAIM-GEN and TRIPOD-LLM checklists; Reporting Summary.
- [ ] Decide whether to publish the reviewer reports (transparent peer review, at the end of review).

## 8. Downloaded papers and bibliography keys (17 Nov)

PDFs in `docs/research/pdfs/` (ignored by git like the other references; the `file` field of the
`.bib` points there); keys in `paper/manuscript/references.bib`.

| Key | Paper | Why | PDF |
|---|---|---|---|
| `luo2024misplaced` | Clinical LLMs with misplaced focus, NMI 2024 | our motivation, written in NMI | **missing** (paywalled) |
| `wang2026psychfound` | PsychFound, NMI 2026 | the closest NMI paper | **missing** (paywalled); reviewer reports yes |
| `ferber2026mira` | MIRA, Nature 2026 | the closest Nature paper (test-ordering agent) | 23 + reviewer reports |
| `guo2025deepseekr1` | DeepSeek-R1, Nature 2025 | RL training figures; what reviewers ask about RL | 24 + reviewer reports |
| `mcduff2025ddx` | AMIE differential diagnosis, Nature 2025 | automatic evaluator against humans | 25 |
| `bran2024chemcrow` | ChemCrow, NMI 2024 | tool-using agent in NMI; LLM judge against experts | 26 |
| `zhou2026labsafety` | LabSafety Bench, NMI 2026 | a pure benchmark published as an Article | **missing** (paywalled) |
| `shi2026matbrain` | MatBrain, NMI 2026 | small models with RL against the same base model | **missing** (paywalled) |
| `gallifant2025tripodllm` | TRIPOD-LLM, Nat Med 2025 | checklist to attach | 29 |
| `miao2024miclaimgen` | MI-CLAIM-GEN | the checklist NMI names | 34 |
| `baker2025monitoring` | Baker et al., OpenAI 2025 | reward hacking over training | 30 |
| `qiu2025diaggym` | DiagGym 2025 | diagnostic agent with RL, reward ablation | 31 |
| `zhang2025medrlvr` | Med-RLVR 2025 | medical RL, reward hacking, in vs out of distribution | 32 |
| `xu2025medagentgym` | MedAgentGym 2025 | SFT, DPO, PPO, GRPO compared | 33 |
| `nmi2024llmframework`, `nmi2026multiagent`, `nmi2026monitorability` | NMI editorials | what the journal wants on LLMs, agents, reasoning | — |

Already in the `.bib`: Hager (`hager2024evaluation`), AMIE (`tu2025amie`), SDBench
(`nori2025sequential`), AgentClinic, Uesato (`uesato2022solving`), Lightman (`lightman2024verify`), the
NMI Comment on agents in medicine (`qiu2024agentic`), Med-PaLM.

Reviewer reports in `docs/research/pdfs/peer-review/`: MIRA, DeepSeek-R1, AMIE (Nature) and six NMI
2026 papers (PsychFound with OCR text, neuropsychological tests, empathy judges, X-ray agent, ICLR
feedback, cardiac model).

The four paywalled PDFs can be downloaded from a browser with CERN access.
