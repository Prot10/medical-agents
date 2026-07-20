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

Key constraint discovered: **Qwen3.5 strips `<think>` from any assistant turn a `user` message
follows**, and reflection is a user message — so it breaks append-only concatenation and clean
credit assignment. Multi-turn GRPO therefore runs with **reflection OFF**; tool results are
`role="tool"`, after which the template preserves prior `<think>`. **The paired eval must also set
`agent.enable_reflection=false`** for train/serve parity — recommend disabling reflection across the
whole re-baseline (base/SFT/GRPO) for consistency.

Files: `training/rollout/react_rollout.py` (token-exact masked rollout, CPU-testable via injected
policy), `training/rollout/trl_rollout.py` (TRL adapter + pass-through reward),
`train_grpo.py --multi-turn`, `run_grpo_training.sh MULTI_TURN=1` (G=4, max_completion=3072).
Recipe: clip-higher `epsilon_high=0.28`, KL=0, `mask_truncated_completions=True`, num_iterations=1
(fully on-policy), val carved from train, 4B G=6/QLoRA for single-turn / G=4 for multi-turn.

## Status
1. ✅ All reward/eval/orchestrator/serving fixes + unit tests, full pytest **1521 passing**.
2. ✅ Multi-turn rollout_func + trainer, wired, unit-tested on CPU with the real tokenizer + a
   canned policy. Only the live-model generation (`_generate_single_turn`) is unvalidated on CPU.
3. ⏳ GPU (user launches): (a) 2-step multi-turn smoke to validate generation/logprobs/memory,
   (b) full run, (c) re-baseline eval on the corrected benchmark (reflection off).

## GPU smoke command (user launches)
```bash
# 2-step multi-turn smoke on the 4B (validates generation + masking + memory end-to-end)
tmux new -s grpo_smoke
MULTI_TURN=1 MAX_STEPS=2 EVAL_STEPS=2 NUM_GENERATIONS=4 PRECISION=qlora \
  bash agent-platform/scripts/training/run_grpo_training.sh Qwen3.5-4B
```
