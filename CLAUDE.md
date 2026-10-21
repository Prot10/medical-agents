# CLAUDE.md

## What is this project

NeuroAgent / NeuroBench: an executable clinical-policy benchmark for small open medical agents in
neurology. A typed action-observation harness (one tool call or one final assessment per turn),
16 diagnostic tools served from pre-generated case outputs, physician-reviewable per-case policies,
and a policy reward with safety caps. Targeting Nature Machine Intelligence.

See README.md for setup, `docs/README.md` for the documentation index,
`agent-platform/docs/clinical-policy-harness.md` for the harness contract and
`docs/A100_VALIDATION_HANDOFF.md` for the GPU validation procedure.

## PhD context

This is one project of Andrea's PhD. The PhD hub lives in `~/Documents/PhD`: read
`MEMORIA_PHD.md` there (and `DIREZIONE_PHD.md` for the research direction) when a task touches
the PhD narrative, supervisors, paper positioning or other projects; its `AGENTS.md` maps every
project repository. Read them on demand, not for routine code work here. The memory is a dated
snapshot: verify statuses before stating them as current. Facts that matter beyond NeuroAgent
belong in `MEMORIA_PHD.md` (with date and source); NeuroAgent-specific details stay here.

## CERN compute and inference

Besides the A100 VM, CERN offers GPUs on ml.cern.ch and an LLM gateway. The tested guide (21 Oct
2026) is `~/Documents/PhD/CERN/CERN_ML_ACCESS.md`, the single source: read it before using either,
and re-check anything time-sensitive (availability, model list). On Andrea's Mac the `cern`
command wraps both (`cern help`). In short, to choose:

- **ml.cern.ch (Kubeflow)**: H100 NVL 94 GB (46 CPU, 127 GB RAM), H100 47 GB MIG slice, A100 40 GB,
  RTX PRO 6000 96 GB, T4, V100S. One GPU unit per user at a time, a queued request included; at
  the test the full H100s were all taken (request pending) while the 47 GB slice started in
  seconds. Sessions (`cern up NAME h100`, then `ssh NAME@ml.cern.ch`) are for development and stop
  after 8 h idle per the docs; long SFT/GRPO runs go in a batch Job (`cern job`, no deadline
  imposed). Storage: `/scratch` node NVMe (lost at the end), `/shared` 10 GiB, EOS/AFS/CVMFS
  mounted, home on EOS. Internet and sudo work; install with uv into `/scratch` with
  `UV_NO_MODIFY_PATH=1`. Not yet checked from a session: write access to
  `/eos/project-d/diagbox` and a vLLM serve of the panel models.
- **AI gateway aigw.cern.ch** (OpenAI and Anthropic APIs, key in `~/.config/cern-ml/aigw.key`):
  CERN-hosted gpt-oss-20b, glm-5.3-flash-int4, gemma-4-12b-it-qat-w4a16-ct, hf-qwen3-32b-awq,
  qwen3.8-27b-fp16 and two embedding models; `GLM-5.3-FP8-VERTEX` and
  `MIMO-V2.6-FLASH-MOPD-VERTEX` run on Google Vertex AI (europe-west4), so prompts leave CERN.
  None of the panel models (Qwen3.5-9B, Granite 4.1 8B, Gemma 4 E4B) is served there, and CERN IT
  changes the list over time (6 months notice, 2 weeks for previews). Every model returns
  logprobs with top-5 alternatives; tool calling works on all seven.
- **Network**: on site or on eduVPN everything is direct from the Mac. Off site without VPN the
  gateway, ml.cern.ch SSH and kubectl are firewalled; `~/.ssh/config` and `cern` then go through
  lxtunnel (2FA once per 12 h).

## Key paths

- `agent-platform/src/neuroagent/harness/` — the harness: `context.py` (prompts and the single
  transcript codec shared by inference and SFT), `adapters.py` (native tool calling → one typed
  action), `loops.py` (policy / direct / ReAct), `environment.py`, `plugins.py`, `profile.py`
- `agent-platform/src/neuroagent/evaluation/policy_reward.py` — the reward; `evaluation/benchmark.py`
  is the batch runner CLI
- `agent-platform/src/neuroagent/api/` — run API (port 8888): profiles, runs (+ SSE stream), episodes, models, cases
- `agent-platform/src/neuroagent/review_api/` — physician review API (port 8889, separate startup)
- `agent-platform/src/neuroagent/training/` — `train_sft.py` (LoRA SFT, one sequence per episode,
  sparse-logits loss), `train_grpo.py` (RLVR: benchmark loop as rollout on a colocated vLLM engine,
  DAPO loss, token-level IS correction, rollouts persisted; weights only on EOS via `--weights-dir`),
  `data/episodes.py` (episode records)
- `agent-platform/config/profiles/*.yaml` — the eight checked experiment profiles (model × loop);
  arbitrary model ids are rejected. Models live in `model_registry.py` with their per-request defaults
- `agent-platform/config/tools/costs.yaml` — per-tool cost registry (Medicare reference rates); the
  vocabulary in `tools/vocabulary.py` derives every enum from it
- `agent-platform/config/policies/diagnosis_synonyms.yaml` — accepted diagnosis labels/codes per
  ICD-10 code, expanded into each case by `scripts/validation/apply_diagnosis_synonyms.py`
  (idempotent; `--check` in CI). The scorer matches label tokens or the submitted `icd10_code`
- `agent-platform/config/hospital_rules/{hospital}/*.yaml` — clinical pathways (served by the API,
  not injected into the harness prompt)
- `agent-platform/config/tools/fallback_library.yaml` — benchmark-level normal results per tool × parameter
  value, the MockServer's last tier (draft until physician review); `tools/fallback_library.py` resolves it
- `agent-platform/config/review/reviewer_codes.yaml` — review-app reviewer registry (hot-reloads)
- `agent-platform/config/review/condition_tool_guidance.yaml` — per-condition tool guidance from the
  July 2026 clinical review, served by the review app only (`test_condition_tool_guidance.py` fails if
  anything agent-side reads it)
- `packages/neuroagent-schemas/` — shared Pydantic models: cases, actions, episodes, policies
- `data/neurobench/cases/` — 600 cases across 20 conditions; `data/neurobench/splits/` 500/100
- `data/review/annotations/{version}/{reviewer_code}/{case_id}.json` — annotation runtime data (gitignored)
- `web/` — dashboard (port 5173 in dev, or `web/dist` served by the run API at `/`): profile picker,
  live runs over `POST /runs/stream`, episode replay, case policy and reward panels
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
cd web && npm ci && npm run dev                                              # dashboard
cd web-review && npm ci && npm run dev:remote                                # review UI

# SFT (needs --extra training); --output must be on EOS (weights never go on the local disk);
# serve an adapter from a /dev/shm copy with LORA_ADAPTER=<dir> LORA_NAME=<alias>
uv run python -m neuroagent.training.train_sft --model qwen3.5-9b \
  --episodes training_data/approved_episodes.jsonl --output /eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/sft-qwen/qwen3.5-9b
# GRPO / RLVR on one GPU (colocated vLLM; nothing else may be on the GPU)
# Weights (checkpoints, adapters) go to EOS only: --weights-dir must be under /eos/
HF_HOME=/dev/shm/hf uv run python -m neuroagent.training.train_grpo --model qwen3.5-9b \
  --split train --output outputs/grpo/qwen \
  --weights-dir /eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/grpo-qwen/qwen3.5-9b --max-steps 50
```

## Conventions

- Python: Pydantic v2 models, dataclasses for config, `from __future__ import annotations`
- Frontend (web, web-review): `@/` alias, named exports only, Zustand for UI state, TanStack Query for data
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
