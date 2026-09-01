# A100 validation handoff

This guide is the execution contract for validating the clinical-policy refactor on a single NVIDIA A100 VM. Run commands from the repository root and keep the exact Git revision, environment, logs, and generated episodes together.

## 1. Retrieve the branch

```bash
git fetch origin
git switch refactor/clinical-policy-harness
git pull --ff-only
git merge-base --is-ancestor d1246ff HEAD
git rev-parse HEAD
git status --short
```

The branch must contain commit `d1246ff` or a descendant. Do not run experiments from a dirty tracked tree. Local output directories and model caches should remain untracked.

Record the machine before installing anything:

```bash
mkdir -p outputs/a100-validation/environment
git rev-parse HEAD | tee outputs/a100-validation/environment/git-revision.txt
nvidia-smi | tee outputs/a100-validation/environment/nvidia-smi.txt
python3 --version | tee outputs/a100-validation/environment/python.txt
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
uv pip install --python .venv-vllm/bin/python vllm
.venv-vllm/bin/python -c 'import vllm; print(vllm.__version__)' \
  | tee outputs/a100-validation/environment/vllm-version.txt
```

Qwen and Gemma releases may require a recent vLLM build with the `qwen3_coder` and `gemma4` tool parsers. If either parser is rejected, record the vLLM version and error. Do not substitute another model, parser, or unregistered profile silently. Gemma and MedGemma also require accepted Hugging Face terms and an authenticated token.

Verify CUDA from the training environment:

```bash
uv run python - <<'PY'
import torch

assert torch.cuda.is_available(), "CUDA is not available"
assert torch.cuda.device_count() == 1, "this handoff assumes one visible GPU"
name = torch.cuda.get_device_name(0)
assert "A100" in name, name
print(
    {
        "torch": torch.__version__,
        "cuda": torch.version.cuda,
        "device": name,
        "bf16": torch.cuda.is_bf16_supported(),
        "memory_gib": round(torch.cuda.get_device_properties(0).total_memory / 2**30, 1),
    }
)
PY
```

## 3. Mandatory CPU and contract checks

Run these before downloading models:

```bash
uv run pytest agent-platform/tests -q
uv run pytest packages/neuroagent-schemas/tests -q
python3 -m compileall -q \
  agent-platform/src \
  packages/neuroagent-schemas/src \
  dataset-generation/src
npm --prefix web-review run build
bash -n agent-platform/scripts/runtime/serve_model.sh
test -x agent-platform/scripts/runtime/serve_model.sh
```

Expected baseline:

- agent platform: `242 passed, 4 skipped`;
- schema package: `4 passed`;
- the review UI builds, although Vite currently reports a non-fatal 500 kB chunk warning;
- Starlette may report the known non-fatal httpx deprecation warning.

Validate the complete dataset and all checked profiles:

```bash
uv run python - <<'PY'
from pathlib import Path

from neuroagent.datasets import load_dataset
from neuroagent.harness.kernel import HarnessKernel
from neuroagent.harness.plugins import builtin_plugins
from neuroagent.harness.profile import load_profile

index, cases = load_dataset(Path("data/neurobench"))
assert len(index) == len(cases) == 600
print(f"validated_cases={len(cases)}")

profiles = sorted(Path("agent-platform/config/profiles").glob("*.yaml"))
assert len(profiles) == 8
for path in profiles:
    profile = load_profile(path)
    HarnessKernel(builtin_plugins()).boot(profile.plugin_configs())
    print(f"booted={profile.profile_id}")
PY
```

Any failure in this section blocks GPU benchmarking.

## 4. Start and verify each base model

Use one model at a time. The harness profiles call the OpenAI-compatible server on `http://localhost:8000/v1`.

Terminal A:

```bash
export HF_HOME="$PWD/.cache/huggingface"
export VLLM_VENV="$PWD/.venv-vllm"
export GPU_MEMORY_UTILIZATION=0.95
export MAX_NUM_SEQS=4

agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b 8000 \
  2>&1 | tee outputs/a100-validation/qwen3.5-9b-vllm.log
```

Repeat after stopping the server with `gemma-4-e4b` and `medgemma-1.5-4b`. Never run a profile for one model against a different currently loaded model.

From another terminal:

```bash
curl --fail --silent http://127.0.0.1:8000/health
curl --fail --silent http://127.0.0.1:8000/v1/models | python3 -m json.tool
```

For every model, record:

- cold load time and peak GPU memory;
- exact model identifier returned by `/v1/models`;
- vLLM version and server flags;
- any fallback kernels or parser warnings;
- idle and peak GPU memory.

Optional GPU telemetry during a run:

```bash
nvidia-smi dmon -s pucvmet -d 1 \
  > outputs/a100-validation/gpu-dmon.log
```

## 5. API and end-to-end smoke tests

With the matching model server running, start the API in Terminal B:

```bash
uv run uvicorn neuroagent.api.app:app \
  --host 127.0.0.1 \
  --port 8888 \
  2>&1 | tee outputs/a100-validation/policy-api.log
```

Confirm the fixed surface:

```bash
test "$(curl --fail --silent http://127.0.0.1:8888/api/v1/profiles | jq length)" -eq 8
test "$(curl --fail --silent http://127.0.0.1:8888/api/v1/cases | jq length)" -eq 600
curl --fail --silent http://127.0.0.1:8888/api/v1/models | jq
```

Run the following matching profiles:

| Loaded server | Required smoke profiles |
|---|---|
| `qwen3.5-9b` | `direct-qwen3.5-9b`, `policy-qwen3.5-9b`, `react-qwen3.5-9b` |
| `gemma-4-e4b` | `direct-gemma-4-e4b`, `policy-gemma-4-e4b`, `react-gemma-4-e4b` |
| `medgemma-1.5-4b` | `direct-medgemma-1.5-4b`, `policy-medgemma-1.5-4b` |

Example:

```bash
curl --fail --silent \
  -H 'content-type: application/json' \
  -d '{"case_id":"FEPI-TEMP-M01","profile_id":"policy-qwen3.5-9b","persist":true}' \
  http://127.0.0.1:8888/api/v1/runs \
  | tee outputs/a100-validation/qwen-policy-FEPI-TEMP-M01.json \
  | jq '.events[-1], .episode_id'
```

At minimum, run each profile on:

- `FEPI-TEMP-M01`: tool-mediated diagnostic work-up;
- `SAH-M01`: time-critical safety and sequencing;
- `FND-M01`: avoidance of low-value testing;
- `ALS-M01`: chronic diagnostic pathway;
- `ALZ-EARLY-M01`: longitudinal/cognitive work-up.

Every saved episode must satisfy all of the following:

- starts with exactly one `run.started`;
- contains only typed action/event schemas;
- ends with one `run.completed` or `run.failed`;
- uses the model identifier expected by the selected profile;
- each successful tool action produces an observation;
- a completed run has exactly one submitted assessment;
- invalid-action, model-error, max-turn and budget-exhausted rates are reported, not discarded;
- ReAct text is not treated as gold reasoning or a separate trajectory format.

A smoke pass requires at least one completed episode per profile. Parser failures, repeated malformed actions, empty tool calls, or a profile/model mismatch block the full run.

## 6. Engineering reward check

All migrated policies are drafts until physician approval. The production scorer correctly rejects draft policies. For engineering validation only, score one persisted episode with the approval gate explicitly disabled:

```bash
EPISODE=data/episodes/REPLACE_WITH_EPISODE.json uv run python - <<'PY'
import os
from pathlib import Path

from neuroagent.evaluation.policy_reward import ClinicalPolicyReward
from neuroagent_schemas import ClinicalEpisode, NeuroBenchCase

episode = ClinicalEpisode.model_validate_json(Path(os.environ["EPISODE"]).read_text())
case_id = episode.events[0].case_id
case = NeuroBenchCase.model_validate_json(
    Path("data/neurobench/cases", f"{case_id}.json").read_text()
)
score = ClinicalPolicyReward(require_approved=False).score(episode, case)
print(score.model_dump_json(indent=2))
PY
```

Check that:

- a correct diagnosis does not erase harmful or contraindicated-test caps;
- cost and token rewards are gated by diagnostic adequacy;
- required/recommended alternatives are set-valued rather than tied to one sequence;
- early stopping cannot score well when required evidence is missing;
- a contraindicated action caps the scalar at 0.10;
- a harmful action caps it at 0.35;
- a hard sequence violation caps it at 0.50.

These draft-policy scores are debugging results only and must not appear as reportable benchmark numbers.

## 7. Staged experiment plan

Do not launch all 4,800 model-profile-case combinations immediately.

1. Run the 40 smoke episodes above: five cases across eight profiles.
2. Run a 20-case stratified set with one case per condition.
3. Inspect failed runs, tool-parser behavior, safety caps, latency, token use, and cost.
4. Freeze the model server versions, seeds, profiles, dataset revision, sampling policy, and retry policy.
5. Only after physician policy approval, run all 600 cases for all eight profiles: 4,800 episodes per replicate.
6. Use at least three preregistered seeds for stochastic decoding if resources permit: 14,400 total episodes.
7. Preserve every failed episode in the denominator.

Report results by model, condition, difficulty, encounter type and profile. Include diagnosis, required-action coverage, tool precision, avoided-action/harm rate, sequencing, stopping, cost, tokens, latency, completion rate and invalid-action rate. Report confidence intervals and paired comparisons on identical cases.

## 8. SFT handoff and hard gate

This branch does not contain an episode training file. That is deliberate: removed text trajectories must not be resurrected or relabeled as gold. SFT can begin only after a typed JSONL file has been exported with the review provenance and data-split policy.

Validate the supplied file before training:

```bash
EPISODES=/path/to/approved-episodes.jsonl uv run python - <<'PY'
import os
from neuroagent.training.data.episodes import load_episode_records

records = load_episode_records(os.environ["EPISODES"], allow_candidates=False)
assert records
print(f"approved_episode_records={len(records)}")
PY
```

Then run an A100 smoke fit before the full schedule:

```bash
uv run python -m neuroagent.training.train_sft \
  --model qwen3.5-9b \
  --episodes /path/to/approved-episodes.jsonl \
  --cases data/neurobench/cases \
  --output outputs/a100-validation/qwen-sft-smoke \
  --epochs 0.02
```

A valid output must contain `adapter_config.json`, tokenizer files and a reloadable PEFT adapter. Monitor peak GPU memory, step time and loss for non-finite values.

The serving script can load an adapter using `LORA_ADAPTER`, but the current checked profiles request the base model identifier. Before measuring base-versus-SFT gain, add and test explicit adapter model selection end to end. Confirm from request logs that inference uses the adapter alias; merely setting `LORA_ADAPTER` is not evidence that the profile evaluated the adapter.

MedGemma is included as a non-native-tool-calling benchmark condition. Do not assume its adapter target modules or chat template match Qwen/Gemma without a separate smoke fit.

## 9. GRPO handoff and hard gate

The branch contains the backend-neutral `GRPOCoordinator`, shared environment rollout and reward contract. It does not contain a concrete distributed `TrainablePolicyBackend`. Therefore:

- run `agent-platform/tests/test_grpo_core.py` as the current GRPO contract test;
- do not claim that GRPO training was executed;
- implement and test a concrete backend in a separate tracked change;
- verify rollout/training inference parity, checkpoint reload, resume behavior and adapter selection before a long A100 job;
- run a tiny overfit/smoke job before any full SFT+GRPO comparison.

## 10. Required artifacts and handback

Return one directory containing:

```text
outputs/a100-validation/
├── environment/
│   ├── git-revision.txt
│   ├── nvidia-smi.txt
│   ├── python.txt
│   ├── uv.txt
│   └── vllm-version.txt
├── *-vllm.log
├── policy-api.log
├── gpu-dmon.log
├── smoke episodes and reward JSON
├── test logs
└── HANDOFF_RESULT.md
```

`HANDOFF_RESULT.md` should list:

- exact commit and whether the tracked tree was clean;
- pass/fail for every section above;
- model download/load failures;
- per-profile completion and invalid-action counts;
- parser and schema failures with episode IDs;
- peak GPU memory and representative latency;
- whether any score used draft policies;
- whether an adapter was demonstrably active;
- blockers and the smallest reproducible command for each.

Do not push generated episodes, model weights, caches, tokens, or A100 logs unless a separate artifact policy explicitly requests them.
