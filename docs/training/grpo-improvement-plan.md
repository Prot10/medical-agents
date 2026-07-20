# GRPO improvement plan — audit fixes + multi-turn

Status tracker for the "reach real results" effort. Three parallel audits (reward, trainer/data,
eval/orchestrator) + a TRL-0.29.1 architecture study drove this list. Decision on record:
**MockServer E2 is fixed and the whole benchmark is re-baselined** (user, 2026-07-17).

## Root cause of the flat single-turn GRPO result
`build_pseudo_trace` kept the model's `<think>` scratchpad in `final_response`; the safety /
critical-action / contraindication matchers read it raw, while eval strips `<think>`. So narrating
plan text in the scratchpad earned safety/critical/cost credit that scored nothing at eval →
reward rose in training, eval stayed flat. Verified by running `CompositeReward` on crafted
completions. The multi-turn rewrite removes this class entirely (it scores the real `AgentTrace`).

## Fix list

| id | sev | file | fix | state |
|----|-----|------|-----|-------|
| R1 | crit | online_reward.py, metrics.py | strip `<think>` / use assessment-only final_response; matchers ignore think | ✅ verified (0.500→0.000) |
| R4 | major | metrics.py | param-aware action credit for catchall tools (modality/test_type) | ✅ verified (garbage→0) |
| R5 | major | compliance_reward.py, composite_reward.py | no-pathway ⇒ reward-neutral (renormalise), not free 1.0 | ✅ |
| E1 | crit | run_sft_eval_cases.py | count crashed cases as wrong; equal denominators across arms | ✅ (subagent + tests) |
| E2 | crit | mock_server.py, generate_gold_trajectories.py | trigger/param-aware follow-up matching; follow-up overrides stale initial | ⏳ delegated |
| O1 | major | orchestrator.py | max-turns salvage reads last assistant content, not tool turn | ✅ (subagent, 57 tests) |
| O2 | minor | orchestrator.py | capture reason-and-act embedded assessment | ✅ (subagent) |
| T1 | major | train_grpo.py | val set carved from TRAIN, stratified by condition (no test leak) | ✅ |
| T2 | major | train_grpo.py | set GRPOConfig.temperature (not just generation_kwargs) | ✅ |
| T4 | minor | train_grpo.py | --hospital default → de_charite | ✅ |
| T6 | minor | train_grpo.py | promotion-failure logs at ERROR (visible on terminal) | ✅ |

Recipe knobs added to the trainer: `epsilon_high=0.28` (clip-higher), `mask_truncated_completions=True`.
T5 (--use-vllm no-op) left as-is: not on the multi-turn path (which generates via the live model).
All fixes verified; full suite **1521 passing**.

## Multi-turn GRPO (implemented)
TRL native `environment_factory`/`tools=` path ruled out empirically: Qwen3.5 tokenizer
`response_schema is None`, so TRL never parses qwen3_coder tool calls → its tool loop never fires.
**Custom `rollout_func`** (`training/rollout/`): drives the real ReAct rollout (our qwen3_coder
parser + `MockServer` + real `AgentTrace` scoring), returns `env_mask` (0 on tool-result tokens)
and the per-trajectory reward. Token concatenation is template-exact (validated with the real
tokenizer down to the `<|im_end|>\n<|im_start|>` seam).

Key constraint discovered, then **resolved**: Qwen3.5's *shipped* template strips `<think>` from
any assistant turn a `user` message follows, and reflection is a user message — which broke
append-only concatenation. This forced reflection OFF on TRL 0.29. On TRL 1.8 the
think-preserving *training* template fixes it (measured: append-only True, reasoning kept), so
**reflection is back ON** and matches serving. The re-baseline should therefore run with
reflection ON across all arms; serving must be given the same template (see Known config traps).

Files: `training/rollout/react_rollout.py` (token-exact masked rollout, CPU-testable via injected
policy), `training/rollout/trl_rollout.py` (TRL adapter + pass-through reward),
`train_grpo.py --multi-turn`, `run_grpo_training.sh MULTI_TURN=1` (G=4, max_completion=3072).
Recipe: clip-higher `epsilon_high=0.28`, KL=0, `mask_truncated_completions=True`, num_iterations=1
(fully on-policy), val carved from train, 4B G=6/QLoRA for single-turn / G=4 for multi-turn.

## Status
1. ✅ All reward/eval/orchestrator/serving fixes + unit tests, full pytest **1548 passing**.
2. ✅ Multi-turn rollout_func + trainer, wired and unit-tested with the real tokenizer.
3. ✅ Live-model multi-turn validated on the A100: generation, masking, tool execution,
   backward, optimiser step, and held-out eval all run. ~160 s/step at G=4, QLoRA, 7.9 GB.
4. ⏳ Re-baseline base + SFT on the corrected benchmark — **the gate**. No GRPO number is
   comparable until it exists. Needs EOS (the SFT adapters live there).
5. ⏳ Full 4B multi-turn run, then GRPO-vs-SFT on the same corrected benchmark.

### Reward design decisions (measured)
- **`correctness` 0.30** — it is the reported objective, and it is the only component that
  reliably splits a reward group. Tool-selection/safety/cost are highly correlated within a
  group (`reward_std` ~0.02-0.06), so without correctness there is little advantage signal.
  With it zeroed, a right and a wrong diagnosis scored identically (0.3529 on ALS-M01).
- **Safety-gate cap 0.0 → 0.25.** The contraindication detector has 89.1% recall and 97.2%
  per-action precision, but ~4.6 contraindicated actions per case make the per-case false-fire
  rate ~9.5% — and it is biased against good agents: a diagnosis-only answer trips it 0% of the
  time, one stating the case's *required* critical actions trips it 9.5%, because
  contraindications read "Do not \<closely related action\>". At cap 0.0 that erased the whole
  reward, correctness included, for ~1 in 10 good trajectories. Safe trajectories measure
  0.55-0.66, so at 0.25 a genuine violation still ranks below every safe one.
- **Diagnosis matcher audited clean**: 0/600 false negatives, 0/600 false positives on
  cross-condition answers.

### Two failure modes that only appear mid-run
- **fla TileLang backward.** Qwen3.5's gated-delta-rule layers go through
  flash-linear-attention, whose TileLang backend shells out to the pip CUDA-13 nvcc and hits
  "CUDA compiler and CUDA toolkit headers are incompatible". Only the BACKWARD kernel fails, so
  a run loads, generates, completes a rollout, then dies in `loss.backward()`. Pinned to Triton
  via `FLA_TILELANG=0`. Verified: forward within 4.8e-3 of fla's independent recurrent
  implementation, gradient within 3.5e-2 of a finite-difference check of its own forward.
- **TRL `_generate_single_turn` arity.** 0.29 returned 3 values, 1.8 returns 2. Bind
  `completion_ids` positionally; contract tests pin this and the chunked-logprob override.

### Truncation, at two levels
- **Whole-completion budget** — `final_answer_reserve` (640 tok) is held back and checked
  *before* a tool result is appended, so the agent always reaches a diagnosis. A single report
  can exceed the entire reserve, which is why the check cannot come after. Measured 0%
  truncation across budgets 1000-16384, diagnosis every time; a tighter budget now costs tool
  calls, not the assessment.
- **Per-turn cap** — a turn cut by `per_turn_max_tokens` carries no parseable tool call, so the
  rollout reads it as the agent concluding and scores the trajectory as if it chose to stop
  without ordering tests. Now counted (`clipped_turns`), warned about, and configurable
  (`PER_TURN`). Set it from the measured per-turn distribution of the SFT policy, not by guess.

## Framework decision (branch `feat/agentic-rl-vllm-rollouts`)

Researched switching away from TRL for multi-turn agentic RL. **Conclusion: stay on TRL, but
upgrade off 0.29.** No surveyed alternative documents a working single-40GB-A100 configuration
for multi-turn agentic RL with LoRA:

| framework | blocker for us |
|---|---|
| slime, TorchForge | no LoRA at all — we need rank-64 from an existing PEFT adapter |
| SkyRL-Agent | not a trainer; delegates to verl/SkyRL-train/Tinker, so it adds a cluster backend |
| verl / verl-agent | no single-GPU LoRA example, no QLoRA; nearest row 1xH100-80GB, verl-agent floor 2xH100 for a 7B |
| VerlTool | 8xH100 + a Kubernetes cluster for tool execution |

Also refuted: observation-token masking is NOT built-in across the verl family — it would be
hand-rolled there too, exactly as here.

The real problem was the TRL **version**. 1.8 ships what 0.29 lacks:
- `qwen3_5_schema` — 0.29 only knows the Qwen3 template and gates on exact string equality, so
  Qwen3.5 never matched and `response_schema` stayed None (which is why TRL's tool loop never
  fired). TRL 1.8's Qwen3.5 template is byte-identical to the shipped one, so the schema attaches.
- `qwen3_5_think_training_chat_template` — the shipped template strips `<think>` from any
  assistant turn a user turn follows. Measured: shipped -> append-only False, reasoning dropped;
  training template -> append-only True, reasoning kept. This is what allows reflection back on.
- `vllm_mode="colocate"` — the only single-GPU vLLM mode (server mode refuses to share a device).

Migration cost was near zero: every internal we override still exists in 1.8, and the suite
passes (1521 passed / 7 CUDA-skips) on trl 1.8.0 + transformers 5.14.1.

**Counter-argument on record:** TRL's GRPOTrainer is fully synchronous and its async path needs
separate GPUs, so on one card the ceiling is "vLLM-fast generation, still serialised" — not the
actor/rollout overlap verl's hybrid engine gives. With 2+ GPUs, verl would be the better answer.

### Unsloth kernel: run it EAGER
`@torch.compile(fullgraph=True, dynamic=True)` both fails on torch 2.11 + triton 3.6 and, where
it compiled, recompiled against the varying sequence lengths multi-turn inevitably produces —
the same smoke went 363-401 s/step -> 705-957 s/step. Eager is bit-exact (0.000e+00 forward AND
gradient vs fp32), 2.53x less memory, and 1.17x FASTER. The chunking is algorithmic; compile was
incidental.

The kernel is loaded directly from `rl_replacements.py` on disk, bypassing `unsloth_zoo/__init__`,
because importing the package is unsurvivable three ways: its GPU-init needs the `unsloth`
package (pins trl<=0.24) and clears `PYTORCH_CUDA_ALLOC_CONF`; `UNSLOTH_ZOO_DISABLE_GPU_INIT=1`
instead installs MLX aliases that **stub out bitsandbytes** and kill the 8-bit optimiser mid-run;
and `rl_replacements` drags in unsloth's model-patching machinery via one config import.
Verify ALL of: kernel numerics, `PYTORCH_CUDA_ALLOC_CONF`, bitsandbytes/`AdamW8bit`, and that
trl/transformers are untouched.

### Known config traps
- vLLM sizes its KV cache for the model's advertised max context — 262144 for Qwen3.5, needing
  8 GiB, more than the engine's whole share. Cap `--vllm-max-model-length` (16384 is ample:
  ~6.2k prompt + completion budget).
- Serving must use the SAME think-preserving template as training
  (`python -m neuroagent.training.export_chat_template`, then `CHAT_TEMPLATE=... serve_model.sh`),
  or the policy is evaluated on contexts it never trained on.

### Ignore TRL's importance-sampling warning
Every multi-turn run logs that `importance_sampling_level='sequence'` with `loss_type='dapo'`
length-weights sequences, advising `loss_type='grpo'`. Do not take it: TRL's own docs call
'grpo' "not recommended due to length bias", and multi-turn completion lengths vary several-fold.
The warning is also inapplicable — on-policy, TRL substitutes `per_token_logps.detach()` so
`log_ratio` is identically zero and both levels give **bitwise identical** gradients (measured on
ragged lengths spanning 8x). It becomes a real question only under vLLM rollouts, where TRL always
computes `old_per_token_logps`; `test_grpo_importance_sampling_level.py` is the tripwire.

## Commands

```bash
# Multi-turn smoke — generation + masking + backward + held-out eval + promotion (~160 s/step)
MULTI_TURN=1 MAX_STEPS=6 EVAL_STEPS=3 NUM_GENERATIONS=4 PRECISION=qlora \
  bash agent-platform/scripts/training/run_grpo_training.sh Qwen3.5-4B

# Re-baseline base vs SFT on the corrected benchmark — run this BEFORE any GRPO comparison
bash agent-platform/scripts/training/run_definitive_eval.sh Qwen3.5-4B

# Full multi-turn run
MULTI_TURN=1 PRECISION=qlora \
  bash agent-platform/scripts/training/run_grpo_training.sh Qwen3.5-4B
```

Everything on EOS needs a live Kerberos ticket (`kinit`); an expired one shows up as
`Permission denied` on the adapter path, not as an auth error.
