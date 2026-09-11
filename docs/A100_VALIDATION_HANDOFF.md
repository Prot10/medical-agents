# A100 validation handoff

This guide is the execution contract for validating the clinical-policy harness on a single NVIDIA A100 VM. Run commands from the repository root and keep the exact Git revision, environment, logs, and generated episodes together. The result of the first execution is in `outputs/a100-validation/HANDOFF_RESULT.md` on the validation machine (the directory is gitignored).

## 1. Retrieve the branch

```bash
git fetch origin
git switch refactor/clinical-policy-harness
git pull --ff-only
git rev-parse HEAD
git status --short
```

Do not run experiments from a dirty tracked tree. Local output directories and model caches are gitignored (`outputs/`, `data/episodes/`, `training_data/`, `.cache/`).

Record the machine before installing anything:

```bash
mkdir -p outputs/a100-validation/environment
git rev-parse HEAD | tee outputs/a100-validation/environment/git-revision.txt
nvidia-smi | tee outputs/a100-validation/environment/nvidia-smi.txt
uv --version | tee outputs/a100-validation/environment/uv.txt
df -h | tee outputs/a100-validation/environment/disk.txt
```

## 2. Install the application and training environment

Python 3.11 or newer is required. Use the checked lockfile rather than upgrading packages ad hoc.

```bash
uv sync --all-packages --extra dev --extra training
npm --prefix web-review ci
```

The vLLM server is intentionally isolated from the application environment:

```bash
uv venv .venv-vllm --python 3.12
uv pip install --python .venv-vllm/bin/python vllm pandas datasets ninja   # pandas/datasets: `vllm bench serve`; ninja: JIT kernels (speculative decoding)
.venv-vllm/bin/python -c 'import vllm; print(vllm.__version__)' \
  | tee outputs/a100-validation/environment/vllm-version.txt
```

vLLM must provide the `qwen3_coder`, `granite4` and `gemma4` tool parsers (present from 0.23). Gemma requires accepted Hugging Face terms and an authenticated token; Granite 4.1 is Apache-2.0 and ungated. Model masters live on EOS; stage a copy in `/dev/shm/hf` (download there first, then `cp -a` to EOS, because FUSE writes stall on large files).

Verify CUDA from the training environment:

```bash
uv run python - <<'PY'
import torch
assert torch.cuda.is_available() and torch.cuda.device_count() == 1
name = torch.cuda.get_device_name(0)
assert "A100" in name, name
print({"torch": torch.__version__, "cuda": torch.version.cuda, "device": name,
       "bf16": torch.cuda.is_bf16_supported(),
       "memory_gib": round(torch.cuda.get_device_properties(0).total_memory / 2**30, 1)})
PY
```

## 3. Mandatory CPU and contract checks

```bash
uv run pytest agent-platform/tests packages/neuroagent-schemas/tests -q
python3 -m compileall -q agent-platform/src packages/neuroagent-schemas/src dataset-generation/src
npm --prefix web-review run build
bash -n agent-platform/scripts/runtime/serve_model.sh && test -x agent-platform/scripts/runtime/serve_model.sh
```

Expected: every test passes (251 at the time of writing, none skipped on a GPU host); Vite reports a non-fatal 500 kB chunk warning; Starlette reports the known non-fatal httpx deprecation warning.

Validate the complete dataset and all checked profiles:

```bash
uv run python - <<'PY'
from pathlib import Path
from neuroagent.datasets import load_dataset
from neuroagent.harness import boot_profile, load_profiles

index, cases = load_dataset(Path("data/neurobench"))
assert len(index) == len(cases) == 600
profiles = load_profiles("agent-platform/config/profiles")
assert len(profiles) == 9
for profile in profiles.values():
    boot_profile(profile)
    print(f"booted={profile.profile_id}")
PY
```

Diagnosis synonyms must be in sync with the cases:

```bash
uv run python agent-platform/scripts/validation/apply_diagnosis_synonyms.py --check
```

Policy self-consistency (no GPU): a perfect agent that follows each case's own policy must be served every required action by the MockServer and score every component at 1.0 except recommended coverage. The check lives in the validation record; any regression here is a policy or environment defect and blocks GPU benchmarking.

## 4. Start and verify each base model

Use one model at a time. The harness profiles call the OpenAI-compatible server on `http://localhost:8000/v1`. Stage the model in RAM first: a `cp -a` of the HF hub directory into `/dev/shm/hf/hub` turns a multi-minute FUSE load into seconds.

```bash
export HF_HOME=/dev/shm/hf HF_HUB_OFFLINE=1 VLLM_VENV="$PWD/.venv-vllm"
agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b 8000 2>&1 | tee outputs/a100-validation/qwen3.5-9b-vllm.log
```

Repeat after stopping the server with `granite-4.1-8b` and `gemma-4-e4b`. Never run a profile for one model against a different currently loaded model: the request carries the model id and the server rejects a mismatch, which the episode records as `model_error`.

```bash
curl --fail --silent http://127.0.0.1:8000/health
curl --fail --silent http://127.0.0.1:8000/v1/models | python3 -m json.tool
```

For every model record cold load time, model memory and KV-cache size from the server log (`Model loading took`, `GPU KV cache size`, `Maximum concurrency`), the exact model identifier from `/v1/models`, the vLLM version and flags, and any parser warnings.

Serving throughput on the real prompt shape (system + patient + tool catalogue, about 8k tokens):

```bash
uv run python - <<'PY'   # render 64 prompts through the model's chat template
...
PY
.venv-vllm/bin/vllm bench serve --backend openai --endpoint /v1/completions --model <hf id> \
  --dataset-name custom --dataset-path outputs/a100-validation/bench-prompts-<model>.jsonl \
  --custom-output-len 128 --ignore-eos --num-prompts 64 --max-concurrency 8 --save-result --result-dir outputs/a100-validation/bench/<model>
```

Report time-to-first-token, time-per-output-token and output tokens per second at concurrency 1, 4, 8 and 16.

## 5. Smoke matrix

Run the profiles that match the loaded server with the batch runner. Every episode is persisted whether it completed or failed; the summary reports completion rate, failure reasons, invalid-action counts, caps, cost, tokens and latency.

| Loaded server | Required smoke profiles |
|---|---|
| `qwen3.5-9b` | `direct-qwen3.5-9b`, `policy-qwen3.5-9b`, `react-qwen3.5-9b` |
| `granite-4.1-8b` | `direct-granite-4.1-8b`, `policy-granite-4.1-8b`, `react-granite-4.1-8b` |
| `gemma-4-e4b` | `direct-gemma-4-e4b`, `policy-gemma-4-e4b`, `react-gemma-4-e4b` |

```bash
for p in direct-qwen3.5-9b policy-qwen3.5-9b react-qwen3.5-9b; do
  uv run python -m neuroagent.evaluation.benchmark --profile $p \
    --cases FEPI-TEMP-M01 SAH-M01 FND-M01 ALS-M01 ALZ-EARLY-M01 \
    --output outputs/a100-validation/smoke/$p --concurrency 5 --seed 0 --allow-draft-policies
done
```

The five cases cover a tool-mediated work-up (`FEPI-TEMP-M01`), time-critical sequencing (`SAH-M01`), avoidance of low-value testing (`FND-M01`), a chronic pathway (`ALS-M01`) and a cognitive work-up (`ALZ-EARLY-M01`). Also exercise the API path once:

```bash
uv run uvicorn neuroagent.api.app:app --host 127.0.0.1 --port 8888 &
test "$(curl --fail --silent http://127.0.0.1:8888/api/v1/profiles | jq length)" -eq 9
test "$(curl --fail --silent http://127.0.0.1:8888/api/v1/cases | jq length)" -eq 600
curl --fail --silent -H 'content-type: application/json' \
  -d '{"case_id":"FEPI-TEMP-M01","profile_id":"policy-qwen3.5-9b"}' http://127.0.0.1:8888/api/v1/runs | jq '.events[-1]'
```

Every saved episode must start with exactly one `run.started`, contain only typed events, end with one `run.completed` or `run.failed`, carry the model identifier expected by the profile, pair each successful tool action with an observation, and hold exactly one submitted assessment when completed. Invalid-action, model-error and budget-exhausted rates are reported, never discarded. ReAct rationale is a namespaced plugin event, not gold reasoning.

## 6. Engineering reward check

All migrated policies are drafts until physician approval. The production scorer rejects draft policies; `--allow-draft-policies` disables the gate for engineering runs and the summary records `policy_review: draft (not reportable)`. Check in the persisted rewards that a correct diagnosis does not erase harm caps (0.35) or contraindication caps (0.10), that a hard sequence violation caps at 0.50, that cost and token rewards are zero when required evidence is missing, and that a re-ordered study counts as unjustified.

## 7. Staged experiment plan

1. Run the smoke matrix above (five cases across eight profiles).
2. Run a 20-case stratified set with one case per condition.
3. Inspect failed runs, tool-parser behaviour, safety caps, latency, token use and cost.
4. Freeze the server versions, seeds, profiles, dataset revision, sampling policy and retry policy.
5. Only after physician policy approval, run `--split test` (and train if needed) for all eight profiles.
6. Use at least three preregistered seeds (`--seed`) for stochastic decoding.
7. Preserve every failed episode in the denominator (`--resume` never re-runs a persisted episode).

Report results by model, condition, difficulty, encounter type and profile with confidence intervals and paired comparisons on identical cases.

## 8. SFT handoff and hard gate

No physician-approved episode file is committed. Candidate episodes are exported from benchmark outputs and are training-eligible only with an explicit flag:

```bash
uv run python -m neuroagent.training.data.export_episodes \
  --runs outputs/a100-validation/smoke/policy-qwen3.5-9b outputs/a100-validation/smoke/react-qwen3.5-9b \
  --output training_data/candidate_episodes.jsonl
uv run python -m neuroagent.training.train_sft --model qwen3.5-9b \
  --episodes training_data/candidate_episodes.jsonl --output outputs/a100-validation/qwen-sft-smoke \
  --allow-candidates --max-steps 3
```

A valid output contains `adapter_config.json`, tokenizer files and a reloadable PEFT adapter. Monitor peak GPU memory, step time and loss for non-finite values. Then prove adapter selection end to end:

```bash
LORA_ADAPTER=outputs/a100-validation/qwen-sft-smoke LORA_NAME=sft-qwen3.5-9b \
  agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b
uv run python -m neuroagent.evaluation.benchmark --profile policy-qwen3.5-9b --served-model sft-qwen3.5-9b \
  --cases FEPI-TEMP-M01 --output outputs/a100-validation/adapter-check --allow-draft-policies
```

The episode's `run.started.model_id` and the summary's `model_id` must equal the adapter alias; that, plus the server log showing LoRA requests, is the evidence the adapter answered. Gemma 4 and MedGemma need their own smoke fits before any schedule.

## 9. GRPO

`python -m neuroagent.training.train_grpo` runs RLVR on one GPU: the benchmark loop is the rollout
against a vLLM engine colocated in the trainer process, the deterministic policy reward is the
objective, and every rollout is persisted with its reward breakdown. Nothing else may use the GPU.
Checkpoints and adapters are written only to `--weights-dir`, which must be on EOS
(`/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/<run>/<model>`); `--output` keeps logs and
rollouts on the local disk. A Kerberos ticket must be valid for the whole run (`klist`).

```bash
HF_HOME=/dev/shm/hf uv run python -m neuroagent.training.train_grpo --model granite-4.1-8b \
  --cases FEPI-TEMP-M01 SAH-M01 --output outputs/grpo/granite-smoke \
  --weights-dir /eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/grpo-smoke/granite-4.1-8b --max-steps 2 \
  --num-generations 4 --cases-per-step 2 --allow-draft-policies --verify-packing
```

Check in `train_log.jsonl`: every step completes episodes (`rollout/completed_rate`), rewards vary
within the batch (`reward_std` > 0, `frac_reward_zero_std` < 1), gradients are finite and bounded,
the engine/trainer log-prob ratio is near 1 (`sampling/importance_sampling_ratio/mean`), and with
`--verify-packing` the packed-versus-per-row gap (`train/packing_max_abs_logp_gap`) is at bf16
noise level. A learning claim requires the paired held-out evaluation of the saved adapter
(`outputs/grpo/scripts/paired_eval.py`), never per-step reward alone.

## 10. Required artifacts and handback

```text
outputs/a100-validation/
├── environment/            git-revision, nvidia-smi, uv, disk, vllm-version
├── *-vllm.log              server logs per model
├── bench/<model>/          serving benchmark results
├── smoke/<profile>/        episodes/, rewards.jsonl, summary.json
├── perfect-agent.txt       policy self-consistency check
├── qwen-sft-smoke/         adapter and train_log.json
└── HANDOFF_RESULT.md
```

`HANDOFF_RESULT.md` lists the exact commit and tree state, pass/fail per section, model download/load failures, per-profile completion and invalid-action counts, parser and schema failures with episode ids, peak GPU memory and throughput, whether any score used draft policies, whether an adapter was demonstrably active, and blockers with the smallest reproducible command. Do not push generated episodes, weights, caches, tokens or logs.
