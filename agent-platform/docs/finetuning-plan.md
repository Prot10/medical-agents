# Fine-Tuning Qwen3.5-9B for NeuroAgent Tool Use

> **Partly superseded.** The numbers here (769 trajectories, 200 cases, 10 conditions)
> describe an earlier run. Current: 1000 trajectories over the 500 train cases, Qwen3.5-9B
> and -4B, QLoRA with hybrid LoRA targets (the gated-delta-net projections) and Liger fused
> cross-entropy. `test_max_seq_length.py` was replaced by `probe_max_seq_length.py`.
> See [`docs/training/distillation.md`](../../docs/training/distillation.md).

> **Status:** Phase 2 in progress — SFT training running on 769 trajectories
> **Last updated:** 2026-03-26
> **Hardware:** Single A100-40GB
> **Target:** Nature Machine Intelligence paper

---

## TODO Tracker

### Phase 1: Data Pipeline — COMPLETE
- [x] **1.1** Create Claude Code subagent definition (`scripts/training/generate_trajectories_subagent.md`)
- [x] **1.2** Build trajectory generation orchestrator (`training/data/generate_gold_trajectories.py`)
- [x] **1.3** Add QLoRA support to `training/train_grpo.py` (`--qlora` flag, BitsAndBytes NF4)
- [x] **1.4** Fix SFT formatting: prompt/completion split for proper loss masking (Qwen lacks `{% generation %}`)
- [x] **1.5** Increase lora_alpha from 32 to 128
- [x] **1.6** Build 5-fold stratified CV splitter (`training/data/split_dataset.py`)
- [x] **1.7** Generate 769 gold trajectories (200 cases × ~4 styles avg). Coverage: ALZ 100%, BACT-MEN 100%, FEPI-TEMP 100%, FND 100%, GLIO-HG 100%, ISCH-STR 100%, MS-RR 100%, NMDAR partial, PD partial, SYNC partial.
- [x] **1.8** Parse + validate all 769 trajectories → `training_data/gold_trajectories/trajectories.jsonl` (0 failures)
- [x] **1.9** Tool output compression (labs 76% smaller, MRI 19% smaller) to fit 6144 token budget
- [x] **1.10** Trimmed training system prompt (924→307 tokens, 67% savings)

### Phase 2: SFT Training — COMPLETE
- [x] **2.1** Full pipeline validation (every component verified end-to-end)
- [x] **2.2** Run SFT on 769 trajectories (QLoRA, 5 epochs) — `checkpoints/sft_769/checkpoint-272`
  - Val loss: 1.02 → 0.537 (best at epoch 4), val token accuracy: 82.8% → 85.2%
- [x] **2.3** Evaluate SFT model vs base model on fold0 val (60 cases × 3 repeats)
  - Base: 52.9% → SFT: 55.7% top-1 (+2.8%), driven by +9% on diagnostic puzzles
  - Full results: `results/sft_eval/finetuning_results_summary.md`

### Phase 3: Reinforcement Learning (GRPO + DAPO) — IN PROGRESS
- [x] **3.1** Parameter-aware cost reward (`training/rewards/cost_reward.py` + `CostTracker`)
- [x] **3.2** Online reward function (`training/rewards/online_reward.py`). Scores: gold=1.0, wrong-tools=0.81, partial=0.80, bad=0.48. Spread=0.52, sufficient for GRPO.
- [x] **3.3** Fixed PEFT adapter loading for RL from SFT checkpoint (auto-detect `adapter_config.json`)
- [x] **3.4** Build DAPO trainer (`training/train_dapo.py`) — uses TRL native `loss_type="dapo"` with asymmetric clipping
- [x] **3.5** Run GRPO from SFT checkpoint (5 epochs, 2 gens, max_completion=1024)
  - GRPO training was ineffective: loss≈0, reward flat at 0.39 across all epochs
  - Root cause: all completions truncated at 1024 tokens (traces need 4000+), reward_std=0.024 (no contrast)
  - Eval: 56.2% top-1 (+3.3% over base, +0.5% over SFT) — marginal, mostly within noise
- [x] **3.5b** Fixed `generation_batch_size` bug in both `train_grpo.py` and `train_dapo.py`
- [x] **3.5c** Fixed val contamination: created `train_fold0.jsonl` (140 train-only cases, no val leakage)
- [ ] **3.6** Run DAPO from SFT checkpoint (5 epochs, 2 gens, max_completion=2048) — script: `scripts/training/run_dapo_training.sh`
- [ ] **3.7** Compare Base vs SFT vs GRPO vs DAPO on fold0 val

### Known limitation: Single A100-40GB RL bottleneck
- Full ReAct traces need 4000-5000 tokens for complete reasoning
- QLoRA generation + training fits max ~2048 token completions (OOM above)
- All RL completions truncated → uniform rewards → zero gradient signal
- Mitigation for future: vLLM-backed generation, multi-GPU, or offline RL with pre-collected traces

### Phase 4: Scale to 500 Cases & Remaining Trajectories
- [ ] **4.1** Generate remaining ~231 trajectories (NMDAR, PD, SYNC conditions still partial)
- [ ] **4.2** Generate trajectories for new cases when dataset reaches 500
- [ ] **4.3** Retrain best approach on full dataset

### Phase 5: Final Evaluation & Paper Figures
- [ ] **5.1** Full 5-fold CV evaluation of all model variants
- [ ] **5.2** Cost-accuracy Pareto front
- [ ] **5.3** Radar charts (8-dimension LLM judge scores)
- [ ] **5.4** Ablation tables
- [ ] **5.5** Write paper results section

---

## What Has Been Done

### 1. Gold Trajectory Generation Pipeline

**Built a fully automated pipeline** that generates ideal ReAct reasoning traces for training:

- **Subagent prompt** (`scripts/training/generate_trajectories_subagent.md`): Instructs Claude to generate complete multi-turn traces with `<think>`, `<tool_call>`, and `<tool_response>` blocks
- **Orchestrator** (`training/data/generate_gold_trajectories.py`): Prepares prompts for all cases, parses raw subagent output into structured JSONL, validates against ground truth
- **5 trajectory styles** per case for diversity: minimal_efficient, standard_clinical, thorough_workup, cost_conscious, differential_focused
- **Tool output compression**: Strips normal/unremarkable values from tool outputs to fit within the 6144-token training budget (labs 76% smaller, imaging 19% smaller)
- **769 trajectories generated** across 10 neurological conditions, 0 parse failures

**Token budget constraint discovered and solved:**
- Qwen3.5-9B has 248K vocab → logits at seq>6144 cause OOM on A100-40GB
- Trajectories redesigned to be token-efficient: 12,000-16,000 chars (~4,000-5,500 tokens)
- Verified: 6144 tokens uses 35.6 GB (4.4 GB headroom)

### 2. Training Infrastructure

**SFT (`training/train_grpo.py`):**
- QLoRA (NF4 quantization, double quant) reduces model from 18GB to 5GB
- LoRA r=64, alpha=128, targeting all attention + MLP layers
- `completion_only_loss=True` with prompt/completion format (Qwen's chat template lacks `{% generation %}` markers, so messages format doesn't support assistant-only masking)
- Cosine LR schedule, weight_decay=0.01, NEFTune noise alpha=5.0
- 5 epochs, batch=1, grad_accum=8 (effective batch 8)

**GRPO (`training/train_grpo.py`):**
- Online reward function replaces broken offline pre-computed rewards
- Auto-detects PEFT adapter checkpoints and loads base model + adapter separately
- Integrated 3-phase dynamic curriculum (format → accuracy → cost)
- TRL v0.29 API compatibility fixes (max_length, GRPOConfig, reward_func signature)

**DAPO (`training/train_dapo.py`):**
- Token-level policy gradient loss (better for long ReAct traces)
- Asymmetric clipping (clip_higher=0.28, clip_lower=0.18)
- Dynamic sampling (skips converged prompts)
- No KL penalty

**Online Reward (`training/rewards/online_reward.py`):**
- Parses tool calls from generated completions
- Scores against NeuroBench case ground truth
- 6 reward components: correctness (0.35), tool_precision (0.15), tool_recall (0.15), cost_efficiency (0.15), format (0.10), safety (0.10)
- Handles TRL v0.29's message-list format for prompts/completions

**Cost Reward (`training/rewards/cost_reward.py`):**
- Parameter-aware costs via `CostTracker` (Medicare PFS rates)
- `interpret_labs(panels=["CBC"])` = $15 vs `interpret_labs(panels=["autoimmune_encephalitis"])` = $2,000

### 3. Critical Issues Found and Fixed

| Issue | Severity | Fix |
|-------|----------|-----|
| Offline GRPO reward always 0 | CRITICAL | Built online reward with tool call parsing |
| SFT top_fraction=0.1 default → trained on 1/769 examples | HIGH | Changed default to 1.0, added `--top-fraction` CLI arg |
| TRL v0.29 passes prompts as message lists, not strings | HIGH | Added `_extract_text()` to handle all TRL formats |
| Qwen chat template lacks `{% generation %}` for loss masking | HIGH | Converted to prompt/completion format with `completion_only_loss=True` |
| seq_length=16384 OOM (248K vocab × 16K seq = 16GB logits) | HIGH | Profiled max=6144, redesigned trajectories to fit |
| PEFT adapter can't load directly with QLoRA | MEDIUM | Auto-detect adapter, load base model + adapter separately |
| Tool responses in completion (model trained to generate them) | KNOWN | Standard for ReAct SFT (DeepSeek-R1, Search-R1 do this) |

### 4. Data Artifacts

| Artifact | Path | Description |
|----------|------|-------------|
| Raw trajectories | `training_data/gold_trajectories/raw_v2/` | 769 `.txt` files, 12-16K chars each |
| Training JSONL | `training_data/gold_trajectories/trajectories.jsonl` | 769 parsed trajectories with messages |
| Prompts | `training_data/gold_trajectories/prompts/` | 1000 prompt files (200 cases × 5 styles) |
| 5-fold splits | `data/neurobench/splits/` | fold0-4_train.txt, fold0-4_val.txt |
| Training system prompt | `config/system_prompts/orchestrator.txt` | Runtime prompt used unless a training script is passed a custom prompt |
| SFT training script | `scripts/training/run_sft_training.sh` | Ready to run in tmux |
| Comparison script | `scripts/training/run_finetuning_comparison.sh` | End-to-end pipeline |

---

## What Is Missing

### Immediate (before paper submission)

1. **SFT Training Run** — Script is ready (`scripts/training/run_sft_training.sh`), needs to complete successfully. Expected ~4-6 hours for 769 trajectories × 5 epochs on A100-40GB.

2. **GRPO Training Run** — From SFT checkpoint, 15 epochs with integrated curriculum. Needs GRPO-formatted data from `format_for_grpo.py --mode gold`.

3. **DAPO Training Run** — From same SFT checkpoint, 10 epochs. Parallel comparison with GRPO.

4. **Remaining Trajectories (~231)** — NMDAR-ENC, PD, SYNC-CARD conditions are partially covered. Need to generate the remaining thorough_workup and differential_focused styles for these conditions to reach 1000/1000.

5. **Evaluation Pipeline Enhancements** — `training/evaluate_finetuned.py` needs: 5-fold CV loop, bootstrap confidence intervals, McNemar's test, cost-accuracy Pareto visualization.

6. **GRPO Data Formatting** — `training/data/format_for_grpo.py` has a new `--mode gold` option but needs testing with the full 769-trajectory dataset.

### For Full Paper

7. **Scale to 500 Cases** — User plans to create 300 more NeuroBench cases. Once available, regenerate trajectories (5 per case = 2500 total) and retrain.

8. **Paper Figures** — Cost-accuracy Pareto front, radar charts (8-dimension LLM judge), curriculum learning curves, ablation tables.

9. **Statistical Analysis** — Bootstrap BCa CIs, McNemar's test for paired comparisons, leave-one-condition-out CV for generalization.

---

## Architecture Overview

```
NeuroBench v4 Cases (200, scaling to 500)
  │
  ▼
Gold Trajectory Generation (Claude Code Subagent)
  │  5 styles: minimal, standard, thorough, cost-conscious, differential
  │  Token-efficient: compressed tool outputs, concise reasoning
  │  Output: 769 trajectories (target 1000) in JSONL
  ▼
SFT Phase (QLoRA on Qwen3.5-9B)
  │  completion_only_loss, cosine schedule, NEFTune, weight_decay
  │  Max seq: 6144 tokens, batch=1, grad_accum=8, 5 epochs
  ▼
RL Phase (GRPO vs DAPO, compared)
  │  Online reward: correctness + tool precision/recall + cost + safety + format
  │  GRPO: 15 epochs, integrated 3-phase curriculum
  │  DAPO: 10 epochs, token-level loss, asymmetric clipping
  ▼
Evaluation (5-fold CV, LLM Judge, Cost Tracking)
  │  4 models: base, SFT, SFT+GRPO, SFT+DAPO
  │  Metrics: Top-1/3 accuracy, tool P/R, cost efficiency, safety
  ▼
Paper Figures & Tables
```

---

## Hardware Feasibility (Verified)

| Stage | GPU Memory | Max seq | Feasible? |
|-------|-----------|---------|-----------|
| SFT (QLoRA, batch=1, seq=6144) | 36.2 GB | 6144 | Yes (3.8 GB free) |
| SFT (QLoRA, batch=1, seq=4096) | 28.4 GB | 4096 | Yes (11.6 GB free) |
| GRPO (QLoRA, batch=1, G=2, seq=512) | ~25 GB | 512 | Yes (tested) |
| DAPO (QLoRA, batch=1, G=2, seq=512) | ~25 GB | 512 | Yes (tested) |
| OOM boundary | 39.2 GB | 7168 | Marginal |
| OOM | >40 GB | 8192+ | No |

---

## Key Literature

| Paper | arXiv / Venue | Relevance |
|-------|---------------|-----------|
| Qwen3 Technical Report | 2505.09388 | GRPO for agentic tool use |
| DeepSeek-R1 | 2501.12948 | GRPO methodology, distillation |
| Search-R1 | 2503.09516 | GRPO for tool-augmented agents |
| DAPO | 2503.14476 | Token-level PG, outperforms GRPO for long sequences |
| ToolACE | 2409.00920 | Tool-calling dataset generation |
| QLoRA | 2305.14314 | Memory-efficient fine-tuning |
| RAGEN/StarPO | 2504.20073 | RL for agentic reasoning, echo trap |
| AMIE | Nature 2025 | LLM agent outperforming clinicians |
| MedAgentBench | NEJM AI 2025 | Medical agent benchmark |
| NEFTune | 2310.05914 | Embedding noise improves SFT generalization |

---

## Files Summary

### Created
| File | Purpose |
|------|---------|
| `scripts/training/generate_trajectories_subagent.md` | Claude Code subagent prompt for trajectory distillation |
| `scripts/training/batch_generate_trajectories.py` | Anthropic API batch generation (alternative to subagents) |
| `scripts/training/run_sft_training.sh` | SFT training launcher for tmux |
| `scripts/training/run_finetuning_comparison.sh` | End-to-end experiment pipeline |
| `scripts/training/smoke_test_qlora.py` | GPU memory + training validation |
| `scripts/training/test_max_seq_length.py` | Seq length profiling |
| `training/data/generate_gold_trajectories.py` | Trajectory orchestrator + parser + validator |
| `training/data/split_dataset.py` | Stratified k-fold splitting |
| `training/train_dapo.py` | DAPO trainer (token-level PG, asymmetric clip) |
| `training/rewards/online_reward.py` | Online reward for GRPO/DAPO (parses tool calls, scores vs ground truth) |
| `config/system_prompts/orchestrator.txt` | Runtime system prompt; pass a custom prompt explicitly for training experiments |

### Modified
| File | Changes |
|------|---------|
| `training/train_grpo.py` | QLoRA, prompt/completion SFT formatting, completion_only_loss, lora_alpha=128, cosine schedule, NEFTune, weight_decay, online reward, PEFT adapter auto-detection, TRL v0.29 fixes |
| `training/rewards/cost_reward.py` | `compute_parameter_aware()` method via CostTracker |
| `training/data/format_for_grpo.py` | `--mode gold` for formatting from gold trajectories |
| `pyproject.toml` | Added `[project.optional-dependencies] training` group |
| `.claude/settings.json` | Write permissions for training_data/ (enables background subagents) |
