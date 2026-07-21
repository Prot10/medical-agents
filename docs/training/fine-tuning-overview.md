# NeuroAgent fine-tuning — complete overview

Everything about how NeuroAgent is fine-tuned: the SFT → GRPO pipeline, the reward, the
validated recipe, the bugs found and fixed, and how to run each stage. This is the single
entry point; the deeper documents are linked where relevant.

- Recipe / hardware / evaluation methodology: `sft-recipe-hardware-and-evaluation.md`
- Trajectory generation (distillation): `distillation.md`
- The GRPO overhaul, with the fix table and status: `grpo-improvement-plan.md`

---

## 1. The pipeline at a glance

```
base model (Qwen3.5-4B / 9B)
      │
      ▼   SFT — supervised fine-tuning on gold trajectories (LoRA rank 64)
   sft_<model>  ──────────────────────────────────────────────► definitive eval (base vs SFT)
      │
      ▼   GRPO — multi-turn RL against the composite reward (continues the SAME adapter)
  grpo_<model>  ──────────────────────────────────────────────► GRPO vs SFT eval
```

- **One adapter, trained in two stages.** GRPO does not start a fresh LoRA; it loads the SFT
  adapter with `PeftModel.from_pretrained(..., is_trainable=True)` and keeps training it. SFT →
  GRPO is the standard order.
- **QLoRA (4-bit NF4) by default**, rank 64. `PRECISION=bf16` is available and buys back ~13 GB
  on the 9B but is not needed on the 4B.
- **One A100-40GB, one model at a time.** Base weights load from `/dev/shm` (staged from EOS);
  adapters and summaries are written to EOS, never local disk.
- **Everything is measured, not assumed.** Every number below came from a run on the actual
  hardware; where a claim was made from reasoning and later measured false, it was corrected.

Key paths:

| what | where |
|---|---|
| SFT / GRPO adapters | `/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/{sft,grpo}_Qwen3.5-{4B,9B}` |
| base weights (RAM) | `/dev/shm/hf/hub/models--Qwen--Qwen3.5-{4B,9B}` |
| training entry point | `agent-platform/src/neuroagent/training/train_grpo.py` |
| multi-turn rollout | `agent-platform/src/neuroagent/training/rollout/` |
| chunked logprob kernel | `agent-platform/src/neuroagent/training/chunked_logps.py`, `chunked_grpo_trainer.py` |
| reward | `agent-platform/src/neuroagent/training/rewards/`, `config/training/reward_weights_grpo_multiturn.yaml` |
| run scripts | `agent-platform/scripts/training/run_{sft_training,grpo_training,definitive_eval}.sh` |

---

## 2. Stage 1 — SFT

Supervised fine-tuning on gold trajectories (see `distillation.md` for how those are generated),
LoRA rank 64. This produces `sft_<model>` on EOS.

```bash
PRECISION=bf16 bash agent-platform/scripts/training/run_sft_training.sh Qwen/Qwen3.5-4B
```

The literature-aligned base-vs-SFT evaluation (greedy pass@1 + sampled reliability + LLM-judge
composite, paired bootstrap CI + McNemar) is in `sft-recipe-hardware-and-evaluation.md`. The
established finding from the weekend runs: **SFT roughly halves output variance** (a real,
reproducible effect); the top-1 accuracy delta is within noise.

---

## 3. Stage 2 — GRPO (multi-turn agentic RL)

### 3.1 Why multi-turn, and why a custom rollout

Single-turn GRPO optimises a one-shot "triage and order the workup" policy — the model writes
its reasoning and tool calls in a single pass and never sees a tool *response*. That is the
wrong objective: NeuroAgent is evaluated as a real ReAct loop that reacts to tool results.

Multi-turn GRPO drives the genuine ReAct loop. TRL's native `tools=`/`environment_factory`
path cannot be used — Qwen3.5's tokenizer has `response_schema=None`, so TRL never parses its
`qwen3_coder` tool calls — so the rollout is a custom TRL `rollout_func`
(`training/rollout/trl_rollout.py`) driving our own parser + the deterministic `MockServer` and
scoring the real `AgentTrace`. The completion it hands back is token-exact and loss-masked:
`env_mask` is 1 on the policy's own tokens and 0 on tool-result / reflection tokens, so only
model-generated tokens get gradient.

### 3.2 The validated recipe

Measured on the 40GB A100 (base model, then confirmed from the SFT adapter):

| knob | value | why |
|---|---|---|
| `NUM_GENERATIONS` (G) | 4 | reward group size; full group, not weakened to a pair |
| `MAX_COMPLETION` | 8192 | whole-trajectory budget; 4096 cut 25-75% of workups short |
| `PER_TURN` | 3072 | one-turn cap; the uncensored per-turn max is 2106 |
| `LOGIT_CHUNKS` | 32 | training-memory lever; makes 8192 fit (8 OOMs) |
| `LR` | 1e-5 | rank-64 LoRA rate (Unsloth practice), not a full-FT 3e-6 |
| `KL` (β) | 0 | TRL default and DAPO both drop it; also skips the ref forward |
| `loss_type` | dapo | length-unbiased aggregation |
| `epsilon_high` | 0.28 | clip-higher (DAPO) |
| `num_iterations` | 1 | fully on-policy |
| precision | QLoRA | 4-bit NF4, rank 64 |

Measured behaviour at this recipe, on **both** the base model and the actual SFT policy (the
one that gets trained). They differ sharply, and the recipe was sized for the harder base case:

| | base (fresh LoRA) | **SFT adapter** |
|---|---:|---:|
| per-turn tokens (p50 / max) | 1161 / 2106 | **289 / 879** |
| turns | ~5-6 | **8.5** |
| tool calls | ~3.0 | **3.8** |
| clipped-turn / budget-capped | 0% / 0% | **0% / 0%** |
| peak memory | 39.5 GB (96%) | **31.4 GB (77%)** |
| step_time (per prompt-rollout) | 840 s | **465 s** |
| reward mean / std | 0.45 / 0.17 | **0.56 / —** |

The SFT policy writes **short, focused turns and more of them** — the opposite of base — so it is
memory-cheaper and faster, and the recipe has comfortable margin (77%, 0% truncation of any
kind). `PER_TURN=3072` gives ~3.5× headroom over the SFT max of 879, absorbing drift as the
policy changes during training; the rollout logs the per-turn tail every step so drift is
visible.

**Runtime: ~62 h/epoch on the 4B SFT policy** (482 train prompts × 465 s per prompt-rollout;
each prompt must be rolled out once per epoch, so this is invariant to how batch/grad-accum split
it). Generation dominates completely — the parked vLLM path (§9) would cut this by prefix-caching
the shared ~6 k prompt, but needs a 2nd GPU. *(An earlier "~37 h" figure in these notes was an
arithmetic error and is corrected here.)*

### 3.3 Reflection is ON

Qwen3.5's *shipped* (inference) chat template strips `<think>` from any assistant turn a
`user` message follows — and reflection is a user message, which broke append-only token
concatenation on TRL 0.29 and forced reflection off. TRL 1.8's think-preserving *training*
template fixes it (measured: append-only preserved, reasoning kept), so reflection is on and
train/serve stay aligned. **Serving must use the same template** or the policy is evaluated on
contexts it never trained on:

```bash
python -m neuroagent.training.export_chat_template   # writes the training template
CHAT_TEMPLATE=<path> bash agent-platform/scripts/runtime/serve_model.sh <model> <port>
```

---

## 4. The reward

Online `CompositeReward`, scored against each case's ground truth on the real trajectory.
Config: `config/training/reward_weights_grpo_multiturn.yaml`.

| component | weight | note |
|---|---:|---|
| correctness | 0.30 | stated diagnosis vs ground truth — the reported objective |
| actions | 0.25 | tool-selection precision + recall vs the optimal workup |
| safety | 0.25 | contraindicated-action gate (below) |
| cost | 0.10 | gated on workup completeness |
| compliance | 0.05 | hospital-pathway adherence |
| format | 0.05 | the assessment section must exist for a diagnosis to be extractable |

**Safety gate:** a contraindicated action caps the composite at **0.25** (not 0.0). The detector
has 89.1% recall and 97.2% per-action precision, but ~4.6 contraindicated actions per case make
the per-case false-fire rate ~9.5%, and it is biased against good agents — a diagnosis-only
answer trips it 0%, one stating the case's *required* critical actions trips 9.5%, because
contraindications read "Do not \<closely related action\>". At cap 0.0 that erased the whole
reward for ~1 in 10 good trajectories. At 0.25 the gate stays non-compensatory in practice
(safe trajectories measure 0.55-0.66) without annihilating the correctness signal.

**Two reward facts, measured:**

- **`correctness` does NOT supply the group variance** (a claim previously asserted from
  degenerate rollouts, since refuted). It is constant across a case's repeats in 78% of groups;
  what actually splits a group is safety (constant in only 10-15%), actions (15-17%) and cost
  (47%). `correctness` keeps 0.30 solely because it is the reported objective — train and eval
  must optimise the same thing.
- **The composite is directionally aligned with top-1 accuracy.** Scored on the definitive-eval
  runs, its base-vs-SFT delta has the same sign as the top-1 delta in all four model × sampling
  combinations. Pushing the reward up should not push the headline metric down.

Root cause of the original flat single-turn GRPO result (now removed by the multi-turn rewrite):
`build_pseudo_trace` kept the model's `<think>` scratchpad in `final_response`, so the
safety/critical-action matchers gave full credit to plan text narrated in reasoning — credit
that scored zero at eval, which strips `<think>`. Verified 0.500 → 0.000 on a crafted example.

---

## 5. Memory: the chunked logprob kernel

Qwen3.5 has a **248,320-token vocabulary**, so the full `batch × seq × vocab` logits tensor is
enormous. TRL's default path materialises it; we replace it with Unsloth's chunked kernel
(`chunked_grpo_trainer.py`), which computes `hidden @ lm_head.T` per chunk so the full tensor
never exists.

- **Run it EAGER, not compiled.** `@torch.compile` fails on torch 2.11 + triton 3.6, and where
  it compiled it recompiled against every new sequence length. Eager is **bit-exact** (0.000e+00
  vs fp32, forward and gradient), **2.53× less memory**, and **1.17× faster**.
- **`logit_chunks` is THE training-memory lever.** The peak allocation is one fp32 logit chunk:
  `(batch·completion / chunks) × 248320 × 4B`. At 8 chunks that is 2.65 GiB and `G=4 @ 8192`
  OOMs in `loss.backward()`; at 32 chunks it is 0.66 GiB and fits. Bit-exact regardless of chunk
  count, so it buys memory for a little speed with no numerical cost. This is what turned the
  "8192 doesn't fit" ceiling into a tunable constant.
- The kernel is loaded directly from `rl_replacements.py` on disk, bypassing
  `unsloth_zoo/__init__` (whose GPU-init pins trl≤0.24 and stubs out bitsandbytes). All six
  side-effects are re-verified on load.

---

## 6. Bugs found and fixed (this overhaul)

The recurring pattern: something that **silently changes what the reward measures** while every
visible signal — loss, gradient norm, reward, truncation rate — looks healthy. None of these
crash; each would have quietly produced a worthless or misleading run.

| # | bug | effect if shipped | fix |
|---|---|---|---|
| 1 | **`per_turn_max_tokens=512`** | **zero tool calls on every rollout** — Qwen3.5's long `<think>` runs past the cap, the cut turn has no parseable call, the trajectory ends after one turn. Trains on degenerate one-turn rollouts (reward_std ~0.02) → flat eval | raised to 3072 from the uncensored distribution (p50 1161, max 2106); rollout logs per-turn p50/p90/p99/max |
| 2 | TRL `_generate_single_turn` arity (0.29→3 values, 1.8→2) | first multi-turn step dies ~20 min in — multi-turn had **never run** since the upgrade | bind `completion_ids` positionally; contract test |
| 3 | fla TileLang backward vs pip CUDA-13 nvcc | run loads, generates, finishes a rollout, then dies in `loss.backward()` | `FLA_TILELANG=0` (Triton); verified within 4.8e-3 fwd / 3.5e-2 grad |
| 4 | `<think>` leak in `build_pseudo_trace` | plan text narrated in reasoning earns safety/critical credit that scores 0 at eval → reward rises, eval stays flat | assessment-only `final_response`; matchers strip think |
| 5 | budget reserve caps workup, logs "truncated 0%" | GRPO trains on shallower workups than eval, invisibly | `forced_conclusion` counted + warned ("budget-capped N/M") |
| 6 | clipped turn scored as deliberate conclusion | a too-tight cap looks like the agent choosing to stop | `clipped_turns` counted + warned |
| 7 | MockServer follow-up unreachability (55%) | ~half of follow-up tool calls returned nothing | trigger/param-aware matching → 100%, 0 false matches |
| 8 | eval dropped crashed cases | unequal denominators across arms (base /100, SFT /97) | count crashed cases as wrong |
| 9 | safety cap 0.0 biased against good agents | ~1 in 10 good trajectories lose their entire reward | cap → 0.25 (§4) |
| 10 | `num_generations_eval` = `num_generations`, invisible | an eval is `eval_prompts × G` rollouts (~22 min), unadjustable | exposed as `--num-generations-eval` |

Corrections I made to my own earlier claims, each after measuring: the zero-tool-call rollouts
were **not** "the base adapter being untrained" (it was bug #1); `160 s/step` was measured on
those degenerate rollouts and the real figure is **840 s**; `4096` was **not** the memory
ceiling (it was `logit_chunks=8`); and `correctness` does **not** carry the group variance (§4).

---

## 7. Verification / test coverage

Full suite **1557 passing, 4 skipped** (the skips are non-GPU environments). ~40 tests were
added on paths that previously had none:

- rollout budget reserve — a diagnosis at every budget, oversized tool report can't truncate
- clipped-turn detection — a cap below the first turn destroys the trajectory (bug #1 pinned)
- budget-capped reporting — a capped workup is distinguishable from a chosen one
- TRL generate-arity contract — survives 2- or 3-value returns
- chunked-logprob numerics — bit-exact vs fp32, forward and gradient, lower peak memory
- chunked-trainer contract — override tracks TRL's evolving signature and return arity
- checkpoint promotion — best step promoted (not last), degrades safely, callback keys on
  TRL's actual `eval_reward`
- importance-sampling level — sequence vs token gives identical gradients on-policy (so TRL's
  length-weighting warning does not apply; the tripwire fires if vLLM changes that)

---

## 8. How to run

All on EOS needs a live Kerberos ticket (`kinit`); an expired one shows up as `Permission
denied` on the adapter path, not as an auth error.

```bash
# 0. deps (training extra: torch/trl/peft/bitsandbytes/flash-linear-attention/liger)
uv sync --all-packages --extra training

# 1. SFT  (skip if sft_<model> already on EOS)
PRECISION=bf16 bash agent-platform/scripts/training/run_sft_training.sh Qwen/Qwen3.5-4B

# 2. RE-BASELINE base vs SFT on the corrected benchmark — the mandatory gate.
#    No GRPO number is comparable until this exists (the benchmark changed: MockServer
#    follow-ups fixed, crashed cases scored, think-leak removed).
bash agent-platform/scripts/training/run_definitive_eval.sh Qwen3.5-4B

# 3. GRPO — defaults ARE the validated recipe (G=4 / 8192 / per-turn 3072 / 32 chunks).
#    ~62 h/epoch on the 4B SFT policy (465 s/prompt-rollout x 482 prompts).
MULTI_TURN=1 PRECISION=qlora \
  bash agent-platform/scripts/training/run_grpo_training.sh Qwen3.5-4B

# 4. GRPO vs SFT on the same corrected benchmark
ADAPTER=/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/grpo_Qwen3.5-4B \
  bash agent-platform/scripts/training/run_definitive_eval.sh Qwen3.5-4B
```

Override any recipe knob via env: `MAX_COMPLETION`, `PER_TURN`, `LOGIT_CHUNKS`,
`NUM_GENERATIONS`, `EVAL_STEPS`, `PRECISION`. The rollout logs per-turn p50/p90/p99/max and the
clipped / budget-capped rates every step — resize from those, never from a mean.

**Recommended order: re-baseline (step 2) before the GRPO run (step 3).** The GRPO result is
only interpretable against a base/SFT baseline scored on the *same* corrected benchmark; without
it the GRPO number has nothing to compare to.

---

## 9. What is and is not established

**Established (measured):** the pipeline runs end to end and is correct — generation, masking,
tool execution, backward, optimiser step, held-out eval, best-step callback, checkpoint
promotion. The reward discriminates (`reward_std` 0.17). The recipe fits at 96% with no
truncation of any kind. Reflection is on and train/serve aligned.

**Not yet established:** whether GRPO improves the reported metric over SFT. That is the point of
steps 2-4. Everything validated so far used generation that produces real workups, but the
learning outcome — does the group advantage move the policy in the right direction over a full
run — can only be answered by running it and evaluating against the re-baseline.

**Parked:** vLLM-accelerated rollouts (code complete and working through generation + weight
sync, but colocate OOMs on one 40GB card — needs a 2nd GPU; would remove the generation
bottleneck and make deeper budgets trivial). Turn-level credit assignment (ARPO/TACO). 9B
multi-turn (same recipe, larger base — expect QLoRA and a smaller `MAX_COMPLETION` or higher
`LOGIT_CHUNKS`).
