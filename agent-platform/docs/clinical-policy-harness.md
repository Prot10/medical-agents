# Clinical policy harness

NeuroBench v2 is an executable clinical-policy benchmark for agents acting in a 360-degree simulated patient environment. The benchmark does not require a single action sequence or expose a physician chain-of-thought.

## Core contract

A run emits typed actions:

- one tool call, or
- one explicit final assessment.

The environment executes the action and returns a typed observation. Invalid model output is retried without consuming a clinical turn. No regular-expression parser, `<think>` extractor or hidden reasoning field is part of the scoring contract.

The immutable execution path is:

`HarnessProfile → ModelAdapter → AgentLoop → NeuroBenchEnvironment → ClinicalEpisode → ClinicalPolicyReward`.

Profiles compose checked plugins and reject arbitrary model identifiers. Episodes are append-only, replayable records of observable actions and observations.

## Agent approaches

The primary condition is the standard policy loop. It gets the patient presentation and discovers evidence through typed tools.

Two preregistered ablations share the same environment and scorer:

- direct: receives full case evidence and submits an assessment;
- ReAct prompt: uses the same typed execution loop with explicit observe/plan instructions.

ReAct is an ablation, not a distinct data format. MedGemma is excluded from the ReAct condition because it lacks native tool calling; its standard policy condition uses the strict JSON-action adapter.

## Fixed model panel and profiles

| Model | Policy | Direct | ReAct |
|---|---:|---:|---:|
| Qwen/Qwen3.5-9B | yes | yes | yes |
| google/gemma-4-E4B-it | yes | yes | yes |
| google/medgemma-1.5-4b-it | yes | yes | no |

The eight checked YAML profiles live in `agent-platform/config/profiles`. Model serving and API loading accept only this panel.

## Policy reward

The scorer reports diagnosis, action coverage, tool accuracy, safety, waste avoidance, sequence, stopping, assessment, monetary cost, token efficiency and invalid-action components. Harm and contraindication events apply safety caps. Efficiency rewards are gated by clinical adequacy so an agent cannot score well by stopping early.

Approved policies are required by default for reportable evaluation. Draft policies remain usable for engineering checks when explicitly allowed.

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

SFT consumes typed, replay-valid episodes. Candidate bootstrap episodes are labeled `candidate_not_gold` and are rejected by default unless the caller explicitly opts in. There are no golden reasoning trajectories.

GRPO uses the same environment rollout and clinical-policy reward. `GRPOCoordinator` defines the backend-neutral boundary; a concrete distributed trainer must implement `TrainablePolicyBackend` and is intentionally outside the benchmark core.

## Experimental claims

The implementation supports the following tests; it does not itself establish their outcomes:

1. policy-loop performance for each model;
2. policy versus direct and ReAct ablations;
3. base versus LoRA SFT versus SFT+GRPO;
4. safety, diagnostic quality, tool selection, stopping, cost and token-efficiency effects;
5. robustness across difficulty, condition and hospital policy;
6. latency and resource measurements for local deployment.

A local hospital companion is therefore a deployment hypothesis until prospective usability, calibration and workflow-impact experiments are complete. It is not represented as a clinical efficacy claim.
