# CLAUDE.md

## What is this project

NeuroAgent / NeuroBench: an executable clinical-policy benchmark for small open medical agents in
neurology. A typed action-observation harness (one tool call or one final assessment per turn),
16 diagnostic tools served from pre-generated case outputs, physician-reviewable per-case policies,
and a policy reward with safety caps. Targeting Nature Machine Intelligence.

See README.md for setup, `docs/README.md` for the documentation index,
`agent-platform/docs/clinical-policy-harness.md` for the harness contract and
`docs/A100_VALIDATION_HANDOFF.md` for the GPU validation procedure.

## Key paths

- `agent-platform/src/neuroagent/harness/` — the harness: `context.py` (prompts and the single
  transcript codec shared by inference and SFT), `adapters.py` (native tool calling → one typed
  action), `loops.py` (policy / direct / ReAct), `environment.py`, `plugins.py`, `profile.py`
- `agent-platform/src/neuroagent/evaluation/policy_reward.py` — the reward; `evaluation/benchmark.py`
  is the batch runner CLI
- `agent-platform/src/neuroagent/api/` — run API (port 8888): profiles, runs, episodes, models, cases
- `agent-platform/src/neuroagent/review_api/` — physician review API (port 8889, separate startup)
- `agent-platform/src/neuroagent/training/` — `train_sft.py` (LoRA SFT, one sequence per episode,
  sparse-logits loss), `train_grpo.py` (RLVR: benchmark loop as rollout on a colocated vLLM engine,
  DAPO loss, token-level IS correction, rollouts persisted), `data/episodes.py` (episode records)
- `agent-platform/config/profiles/*.yaml` — the eight checked experiment profiles (model × loop);
  arbitrary model ids are rejected. Models live in `model_registry.py` with their per-request defaults
- `agent-platform/config/tools/costs.yaml` — per-tool cost registry (Medicare reference rates); the
  vocabulary in `tools/vocabulary.py` derives every enum from it
- `agent-platform/config/policies/diagnosis_synonyms.yaml` — accepted diagnosis labels/codes per
  ICD-10 code, expanded into each case by `scripts/validation/apply_diagnosis_synonyms.py`
  (idempotent; `--check` in CI). The scorer matches label tokens or the submitted `icd10_code`
- `agent-platform/config/hospital_rules/{hospital}/*.yaml` — clinical pathways (served by the API,
  not injected into the harness prompt)
- `agent-platform/config/review/reviewer_codes.yaml` — review-app reviewer registry (hot-reloads)
- `agent-platform/config/review/condition_tool_guidance.yaml` — per-condition tool guidance from the
  July 2026 clinical review, served by the review app only (`test_condition_tool_guidance.py` fails if
  anything agent-side reads it)
- `packages/neuroagent-schemas/` — shared Pydantic models: cases, actions, episodes, policies
- `data/neurobench/cases/` — 600 cases across 20 conditions; `data/neurobench/splits/` 500/100
- `data/review/annotations/{version}/{reviewer_code}/{case_id}.json` — annotation runtime data (gitignored)
- `web-review/` — review UI (port 5174); `outputs/`, `data/episodes/`, `training_data/` are gitignored

## Common commands

```bash
uv sync --all-packages --extra dev --extra training
uv run pytest agent-platform/tests packages/neuroagent-schemas/tests -q

# Serve one panel model (isolated vLLM venv; stage the HF cache in /dev/shm for fast loads)
HF_HOME=/dev/shm/hf agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b
# Run a profile over cases against the loaded server; draft policies need the explicit flag
uv run python -m neuroagent.evaluation.benchmark --profile policy-qwen3.5-9b \
  --cases FEPI-TEMP-M01 SAH-M01 --output outputs/smoke/policy-qwen --allow-draft-policies
uv run uvicorn neuroagent.api.app:app --host 127.0.0.1 --port 8888          # run API
uv run uvicorn neuroagent.review_api.app:app --host 0.0.0.0 --port 8889     # review API
cd web-review && npm ci && npm run dev:remote                                # review UI

# SFT (needs --extra training); an adapter is served with LORA_ADAPTER=<dir> LORA_NAME=<alias>
uv run python -m neuroagent.training.train_sft --model qwen3.5-9b \
  --episodes training_data/approved_episodes.jsonl --output outputs/qwen-sft
# GRPO / RLVR on one GPU (colocated vLLM; nothing else may be on the GPU)
HF_HOME=/dev/shm/hf uv run python -m neuroagent.training.train_grpo --model qwen3.5-9b \
  --split train --output outputs/grpo/qwen --max-steps 50
```

## Conventions

- Python: Pydantic v2 models, dataclasses for config, `from __future__ import annotations`
- Frontend (web-review): `@/` alias, named exports only, Zustand for UI state, TanStack Query for data
- Commit style: conventional commits (`feat:`, `fix:`, `docs:`, `chore:`)
- Case IDs: `{CONDITION}-{S|M|P}{NUMBER}` (v1) or `{CONDITION}-R{S|M|P}{NUMBER}` (v2)
- Every policy is `draft` until two independent physicians approve all dimensions; the reward
  refuses draft policies unless `require_approved=False` (engineering only, never reportable)
- The harness never persists free-form reasoning. ReAct is a prompt-only ablation whose rationale is
  a namespaced plugin event; SFT rows are rendered by `harness/context.py::transcript`, the same
  function that builds inference requests
- Panel: Qwen3.5-9B, IBM Granite 4.1 8B, Gemma 4 E4B, all native tool calling. Sampling and the
  thinking switch are frozen per model at the model card's recommendation in
  `model_registry.request_defaults`; profiles do not override them, replication is by `--seed`
- 16 tools: analyze_brain_mri, analyze_eeg, analyze_ecg, interpret_labs, analyze_csf, order_ct_scan,
  order_echocardiogram, order_cardiac_monitoring, order_advanced_imaging, order_specialized_test,
  search_medical_literature, check_drug_interactions, order_body_imaging, order_microbiology,
  obtain_tissue_diagnosis, perform_clinical_assessment. `consult_medical_specialist` does not exist
- Tool vocabulary: `costs.yaml` is the single source; `BaseTool.execute` validates every call
  against the advertised schema (an out-of-vocabulary value is an error observation, not a
  fallback result, and the cost registry has no fallback rates); the review app mirrors the
  schemas in `review_api/services/tool_io.py` and `tests/test_tool_io_schemas.py` fails if the
  mirror drifts
- Read `docs/benchmark/tool-contract.md` before editing a case or a tool schema; a change to the
  policies must keep the perfect-agent check clean (every required action served by the MockServer)

## Architecture notes

- Execution path: `HarnessProfile → ModelAdapter → AgentLoop → NeuroBenchEnvironment →
  ClinicalEpisode → ClinicalPolicyReward`
- The final turn of a policy run must submit the assessment; invalid model output is retried with a
  one-off correction inside the profile's `max_invalid_actions` budget and counted, never discarded
- Reward components: diagnosis, required/recommended coverage, tool accuracy (first match of a
  criterion only; re-ordering a resulted study is unjustified), safety, waste avoidance, sequence
  (orders two actions the agent actually took), stopping (unjustified actions after the required
  set), assessment, cost efficiency (relative to the policy's own required work-up) and completion
  token efficiency, both gated by diagnosis × required coverage. Contraindicated 0.10, harmful 0.35,
  hard-sequence 0.50 caps
- API `POST /api/v1/runs` executes one case synchronously through a checked profile and persists
  the episode under `data/episodes/`; the models route can spawn `serve_model.sh`
- vLLM serves one model at a time on the A100-40GB via `scripts/runtime/serve_model.sh`
  (Qwen: `qwen3_coder` tool parser; Gemma 4: `gemma4`; all with `--language-model-only`)

## Dataset review app

Separate FastAPI + Vite app for blind triple-review of the dataset. Gated by `X-Reviewer-Code`;
admin role unlocks aggregate endpoints under `/api/v1/admin/...`. Annotation storage is one file
per (reviewer, version, case). `review_api/services/policy_eligibility.py` implements the
approval rule (two independent all-dimension approvals, no unresolved errors, third reviewer on
disagreement). Tabs: Overview / Cases / Methodology / Admin.
