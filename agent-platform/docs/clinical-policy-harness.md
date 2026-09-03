# Clinical policy harness

NeuroBench v2 is an executable clinical-policy benchmark for agents acting in a 360-degree simulated patient environment. The benchmark does not require a single action sequence or expose a physician chain-of-thought.

## Core contract

A run emits typed actions:

- one tool call, or
- one explicit final assessment.

The environment executes the action and returns a typed observation. A tool call whose arguments violate the advertised schema (an enum value outside the catalogue, a missing required field) is a clinical turn that returns an error observation at no cost, never a substitute result. Invalid model output (no action, several calls, an unknown tool) is retried with a one-off correction, without consuming a clinical turn, inside the profile's `max_invalid_actions` budget; every rejection is recorded. The final turn must submit the assessment, so every episode that does not fail carries a diagnosis. No regular-expression parser, `<think>` extractor or hidden reasoning field is part of the scoring contract.

The immutable execution path is:

`HarnessProfile → ModelAdapter → AgentLoop → NeuroBenchEnvironment → ClinicalEpisode → ClinicalPolicyReward`.

Profiles compose checked plugins and reject arbitrary model identifiers. Episodes are append-only, replayable records of observable actions and observations.

## Transcript codec

`harness/context.py::transcript` is the single function that renders an episode into chat messages. It builds every inference request and every SFT example, so the trained format and the evaluated format cannot drift apart. Actions are OpenAI tool calls and observations are `tool` messages; the tool catalogue travels in the request or the chat template, not in the transcript. Tool-call arguments stay mappings in the transcript (what chat templates render) and the client serializes them for the wire.

Observations recorded at turn 0 (the direct baseline) are presented as results available at the start of the encounter. Rejected outputs are never replayed.

## Agent approaches

The primary condition is the standard policy loop. It gets the patient presentation and discovers evidence through typed tools.

Two preregistered ablations share the same environment and scorer:

- direct: receives every stored initial result and submits an assessment;
- ReAct prompt: uses the same typed execution loop and asks for a brief rationale in the assistant content, recorded as the `react.rationale` plugin event and replayed only within the ablation.

ReAct is an ablation, not a distinct data format.

Qwen3.5 and Gemma 4 run with thinking disabled on every request; Granite 4.1 has no thinking switch. Sampling is frozen per model at the model card's recommendation (`model_registry.request_defaults`: Qwen 0.7/0.8/top-k 20/presence 1.5, Gemma 1.0/0.95/top-k 64, Granite greedy) and runs are replicated over preregistered seeds; a uniform low temperature increased repetition loops on Qwen in the smoke matrix. Measured on vLLM 0.23: with thinking on, Qwen3.5-9B spent its entire 4096-token budget without emitting a tool call under `tool_choice=required`, and leaked the reasoning into content while emitting several calls under `auto`. Native adapters use `tool_choice=auto` because the required-mode grammar suppressed all assistant content (no ReAct rationale) while still allowing multiple calls at once; a text-only reply is an invalid action.

## Fixed model panel and profiles

| Model | Policy | Direct | ReAct |
|---|---:|---:|---:|
| Qwen/Qwen3.5-9B | yes | yes | yes |
| ibm-granite/granite-4.1-8b | yes | yes | yes |
| google/gemma-4-E4B-it | yes | yes | yes |

The nine checked YAML profiles live in `agent-platform/config/profiles`. Model serving and API loading accept only this panel. A LoRA adapter is evaluated by serving it under an alias (`LORA_ADAPTER`, `LORA_NAME`) and pointing a profile's model plugin at it with `served_model`; the alias is recorded as the episode's `model_id`.

## Policy reward

Components, each in [0, 1]:

- diagnosis: every token of an accepted label occurs in the submitted primary diagnosis, or the submitted `icd10_code` is an accepted code. Accepted labels and codes are seeded per ICD-10 code from `config/policies/diagnosis_synonyms.yaml` (`scripts/validation/apply_diagnosis_synonyms.py`, idempotent) and refined per case by physician review;
- required and recommended action coverage: fraction of criteria satisfied by any alternative pattern;
- tool accuracy: fraction of actions that were the first to satisfy some criterion (re-ordering a resulted study is unjustified);
- safety and waste avoidance: harmful / wasteful actions as a fraction of all actions;
- sequence: fraction of constraints respected among pairs of actions the agent actually took;
- stopping: unjustified actions taken after the required evidence was complete, beyond the policy's allowance;
- assessment: required and prohibited recommendations, reported for physician review but carrying no weight in the scalar (substring matching of prose sentences measures phrasing, not care);
- cost efficiency: the policy's own required work-up cost divided by the episode cost, capped at 1;
- token efficiency: completion tokens only, halving at 2048 per episode.

Cost and token efficiency are gated by diagnosis × required coverage so an agent cannot score well by stopping early. Contraindicated actions cap the scalar at 0.10, harmful actions at 0.35 and hard sequence violations at 0.50. A perfect agent that follows each case's own policy scores every component at 1.0 across all 600 cases except recommended coverage; this check is the policy self-consistency gate.

Approved policies are required by default for reportable evaluation. Draft policies remain usable for engineering checks when explicitly allowed (`--allow-draft-policies`), and the summary records that the numbers are not reportable.

## Running

```bash
HF_HOME=/dev/shm/hf agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b
uv run python -m neuroagent.evaluation.benchmark --profile policy-qwen3.5-9b \
  --split test --output outputs/policy-qwen --concurrency 8 --seed 0
```

The runner persists every episode, completed or failed, writes one reward row per case and a summary with completion and invalid-action rates, caps, means per component and per-condition breakdowns. `--resume` skips cases whose episode file exists.

## Data and review

Every v2 case has:

- accepted diagnosis labels and ICD codes;
- set-valued action criteria with alternative tool-call patterns;
- avoided actions graded as waste, harm or contraindicated;
- case-specific sequence constraints and stopping rules;
- required and prohibited assessment recommendations;
- observable clinical evidence and red herrings.

Synthetic generation always produces `draft` policies. Approval requires two independent physicians to approve all seven review dimensions. A third physician adjudicates disagreement, and unresolved errors block approval.

## Training

SFT consumes typed, completed episodes and trains one sequence per episode with loss on every model action (rollout-style): the transcript is rendered once by the chat template, turn boundaries are tokenized separately so they match generation, and the vocabulary projection is computed only at supervised positions. Prefix chaining of the template across turns is asserted per episode; it holds for all three panel models with thinking disabled. Candidate bootstrap episodes are labeled `candidate_not_gold` and are rejected by default unless the caller explicitly opts in. There are no golden reasoning trajectories.

GRPO (`training/train_grpo.py`) is reinforcement learning with verifiable rewards over the same environment: rollouts run the unchanged benchmark loop against a vLLM engine colocated in the training process, and every episode is scored by the deterministic policy reward, so nothing in the objective is model-judged. Design choices, each measured on the A100 (see `docs/A100_VALIDATION_HANDOFF.md`):

- Rollout parity: the harness adapter, tool parsers and per-request settings are the ones used in serving (the parser is built with the request's tool schemas, exactly as vLLM's server does; tool-call syntax is sampled freely in both). Corrections and the final-turn instruction are delivered inside the latest observation, because Qwen's template re-renders earlier assistant turns once a user message follows them.
- One sequence per episode: the model's own tokens for every accepted action, the rendered environment text between them (masked), tokenized at the generation boundaries. Rejected attempts are dropped and counted; a turn whose conditioning differed from the sequence (correction in its prompt, or a template re-rendering of the action) is counted as a conditioning mismatch and left to the importance-sampling correction.
- Continuous batching: every episode runs the benchmark loop in its own thread; a turn request is submitted to the in-process engine the moment it is ready and the coordinator steps the engine until no episode is live, so the batch stays full and a fast episode never waits for a slow one (a per-turn barrier cost 3.2× the ideal on the persisted rollouts).
- Memory on one GPU: the policy loads on the CPU so the engine can take ~80% of the GPU; around each rollout the policy is swapped out, the engine woken, then slept (level 2) and the policy swapped back. The vocabulary projection is computed only at action tokens.
- Prefix sharing (`training/prefix_packing.py`): a group's episodes share the same ~8.5k-token prompt, so for Gemma and Granite the group is one forward over `prompt + completions` with a FlexAttention block mask (a completion attends to the prompt and to itself; per layer type for Gemma's sliding-window layers; a dense mask would push SDPA onto materialised scores and exhaust the A100 at ~18k tokens) and prompt-continuing positions. The head (vocabulary projection, the model's logit scaling or soft-capping, temperature, log-softmax) runs in checkpointed chunks so Gemma's 262k vocabulary never materialises for all supervised positions at once. Log-probabilities match per-row forwards (tested to 1e-4 on tiny models; `--verify-packing` logs the gap, its mean and 99th percentile, and the Flex-vs-SDPA kernel noise floor on the real model). TRL's row shuffle is replaced by a group-preserving one so a micro-batch is one group; a mixed micro-batch is an error. Qwen3.5's recurrent layers cannot fork a prefix state, so it trains one row at a time.
- On-policy log-probabilities: TRL recomputes "old" log-probs over the generation batch whenever vLLM importance sampling is on. With one iteration and aligned steps they equal the training forward's detached log-probs, so that pass returns a placeholder and the training forward fills in the old log-probs and the clamped token-level vLLM ratio (one full forward per row saved, ~25% of a Qwen step).
- Objective: token-level DAPO loss with clip-higher (0.2 / 0.28), batch-level advantage normalization, no KL term, truncated episodes masked, one optimizer step per group batch (on-policy), token-level truncated importance sampling against the engine's log-probs (a sequence-level ratio over ~1k action tokens underflows to zero because the engine reports top-k/top-p-processed log-probs).
- Adapter: LoRA r=16 on the language model's decoder projections only (attention, gated delta net, MLP). `all-linear` also swept the vision/audio towers of Qwen3.5 and Gemma 4, whose LoRA layers never receive a gradient and which vLLM refuses to load; the colocated engine loads those models text-only.
- Rewards: the policy scalar is optimized; diagnosis, required coverage, tool accuracy, safety, stopping and completion are logged with weight 0. Every rollout is persisted (`rollouts/step-*.jsonl`) with its reward breakdown, retries and truncation, so a run can be audited episode by episode.

Approved policies are required unless `--allow-draft-policies` is set, and adapters are evaluated with the standard benchmark runner through `--served-model`.

Context length. Measured on 90 real episodes (Qwen tokenizer): a full transcript is 10.9k tokens on average, 13.0k at the 95th percentile, 15.0k at most; the prompt is 8.5k of which the tool catalogue is 7.25k; one observation is 394 tokens on average and 2.6k at most (NMDAR lab panels). The worst theoretical 12-turn episode is ~36k, so the 32k serving/training context covers everything observed with a 2× margin; an overflow surfaces as a `model_error` episode, never as silent truncation. Should policies grow, raise `--max-model-len` (the panel models are native 128k–262k; KV cost ~40 KB/token on Qwen) before shortening observations, because the catalogue, not the observations, dominates. Every training row carries that catalogue, which is the main cost of a step; sharing the group's prompt prefix in one forward is the identified optimisation (exact for the attention-only models, needs a forked recurrent state for Qwen3.5).

## Experimental claims

The implementation supports the following tests; it does not itself establish their outcomes:

1. policy-loop performance for each model;
2. policy versus direct and ReAct ablations;
3. base versus LoRA SFT versus SFT+GRPO;
4. safety, diagnostic quality, tool selection, stopping, cost and token-efficiency effects;
5. robustness across difficulty and condition;
6. latency and resource measurements for local deployment.

A local hospital companion is therefore a deployment hypothesis until prospective usability, calibration and workflow-impact experiments are complete. It is not represented as a clinical efficacy claim.
