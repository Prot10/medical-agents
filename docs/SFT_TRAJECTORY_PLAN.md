# Golden Trajectory Generation → SFT — Progress Tracker

Persistent tracker for the multi-session agent-distillation effort.
Plan source: `~/.claude/plans/i-want-you-ot-ticklish-newell.md`

## Goal

Generate 1000 golden ReAct trajectories (2 per case × 500 NeuroBench train cases) with Sonnet
subagents (1 subagent = 1 trajectory), then QLoRA-SFT Qwen3.5-9B and Qwen3.5-4B on an A100-40GB.

This is **offline agent distillation via rejection sampling** (FireAct / Agent Distillation lineage).

## Key decisions

| Decision | Value |
| --- | --- |
| Trajectories per case | 2 (uniform) → 1000 |
| Styles | `efficient_linear`, `differential_reasoned` |
| Backtracking | Grounded in `ground_truth.red_herrings`; M/P cases only, `differential_reasoned` only |
| Hospital rules | ~40% none, ~60% one of 5 hospitals (rotated, deterministic by hash) |
| Max seq length | **12288** (probe: both models reach 16384 with Liger) |
| Teacher | Sonnet subagents via Workflow tool (subscription, not API) |

## Status

- [x] Phase 0a — Research SOTA (FireAct, Agent Distillation, partial masking, calibrated backtracking)
- [x] Phase 0c — Train/test split BEFORE generation (500 train / 100 test)
- [x] Phase 0b — Max-seq probe on A100-40GB (both models reach 16384 with Liger + fixed LoRA)
- [x] Phase 1 — Restructure gold pipeline (styles, rules mixing, template, validation)
- [x] Phase 4a — Fix loss masking (`{% generation %}` chat template + `assistant_only_loss`)
- [x] Phase 4c — Fix hybrid LoRA targets; enable Liger; add `--max-seq-length` CLI flag
- [x] Phase 4d — SFT smoke test on real trajectories (9B, QLoRA): passed, eval_loss 1.25
- [x] Phase 2 — Orchestrate generation (1000 trajectories, one Sonnet subagent each)
- [x] Phase 3 — Assemble + repair + audit → **1000/1000 valid, training-ready**
- [ ] Phase 4b — SFT both models on full data, evaluate vs base on the 100-case test set

## FINAL DATASET — `training_data/gold_trajectories_v6/trajectories.jsonl`

**1000 trajectories over 500 train cases** (2 per case, 100% of attempted).

| property | value |
| --- | --- |
| sequence length (chat-templated) | mean 5760, p90 7302, p99 8461, **max 9728** (< 12288 cap) |
| supervised (assistant) tokens | mean 1618, p90 1939, max 2650 |
| styles | efficient_linear 500 / differential_reasoned 500 |
| difficulty | moderate 376, puzzle 354, straightforward 270 |
| hospital mix | none 382, uk_nhs 130, de_charite 122, jp_todai 124, us_mayo 123, br_hcfmusp 119 |
| tool calls per trajectory | 2:24, 3:210, 4:369, 5:289, 6:89, 7:14, 8:2, 9:3 |
| tools exercised | all 12 |
| conditions | 18 (the 2 held-out conditions correctly absent) |
| **test-set cases present** | **0** |
| **answer-key leakage** | **0** |
| revision episodes | **365/365** required trajectories contain evidence-driven contradiction language |
| structurally invalid | **0** (every assistant turn has a non-empty `<think>`) |

Backtracking is calibrated, not uniform — explicit reappraisal ("I had favoured…", "revising…",
"no longer…") by cell:

| style | straightforward | moderate | puzzle |
| --- | --- | --- | --- |
| efficient_linear | 4% | 4% | 7% |
| differential_reasoned | 9% | **25%** | **30%** |

### Yield across rounds (rejection sampling + one repair round)

| round | valid |
| --- | --- |
| first pass (all 1000) | 694 (69%) |
| + repair of 265 rejects, backfill of 41 | 970 (97%) |
| + repair of last 27, backfill of 3 | 996 (99.6%) |
| + stricter `<think>`-per-turn rule, repair of 6 | **1000 (100%)** |

### Actual teacher cost

**61.7M tokens** (Sonnet subagents), vs the 46M approved. The overrun is the reject rate: 30% of
first-pass trajectories needed repair, not the assumed 10% (292 repairs + 44 backfills = 17.1M).

| run | tokens |
| --- | --- |
| pilots v1–v3 + pilot repair | 3.30M |
| full generation (977) | 40.95M |
| repairs (265 + 27) | 15.23M |
| backfills (41 + 3) | 1.86M |
| final repair (6) | 0.32M |
| **total** | **61.66M** |

## Phase 0 probe results (final: corrected hybrid LoRA + Liger, QLoRA NF4, bs=1)

| model | 8192 | 10240 | 12288 | 16384 | max |
| --- | --- | --- | --- | --- | --- |
| Qwen3.5-9B | 24.5 GB | 27.4 GB | 30.3 GB | 36.2 GB | **16384** |
| Qwen3.5-4B | 14.4 GB | 16.8 GB | 19.1 GB | 23.7 GB | **16384** |

`run_sft_training.sh` caps at `SEQ_CAP=12288` since the longest real trajectory is ~9.3k tokens.

Trainable params: 9B → 160,432,128 (1.76%); 4B → 121,896,960 (2.82%).

### Smoke test (verified on the 22 pilot trajectories, Qwen3.5-9B)
`trainable params: 160,432,128` · assistant-only loss · Liger on · no OOM · `eval_loss 1.25`,
`mean_token_accuracy 0.696` after 1 epoch. Saved adapter contains 200 adapted modules:
`in_proj_qkv`/`in_proj_z`/`out_proj` × 24 gated-delta-net layers **plus** `q/k/v/o_proj` × 8
full-attention layers → attention adapted in **32/32 layers**.

## The split (done — `data/neurobench/splits/`)

`make_train_test_split.py`. **500 train / 100 test.** Trajectories are generated for the
train split ONLY; `assemble`/`_split_trajectories` both hard-fail if a test case appears.

- Test = 2 fully held-out conditions (**myasthenia_gravis**, **hepatic_encephalopathy** = 60 cases)
  + 40 stratified across the other 18 conditions, matched to the pool's difficulty/encounter ratios.
- Held-out pair chosen because neither has a near-duplicate sibling condition among the remaining 18
  (unlike SAH/ischemic_stroke or alzheimers/ftd), and they exercise different tool families.
- Validation for early stopping is carved from TRAIN (`--val-fraction 0.1`, by case_id), never from test.

## Trajectory design (implemented)

- 500 cases × 2 styles = **1000 trajectories**.
- Styles: `efficient_linear`, `differential_reasoned`.
- Revision episodes: **365** — exactly the `differential_reasoned` traces on moderate/puzzle cases.
  Anchored to `ground_truth.red_herrings` (406/446 M/P cases have one); otherwise the
  highest-likelihood competing differential.
- Hospital mix (measured): none=382, uk_nhs=130, jp_todai=124, us_mayo=123, de_charite=122, br_hcfmusp=119.
- Tool-call counts and final-confidence ranges scale with difficulty.
- Validator rejects: wrong dx, missing sections, harmful/useless/no-output tool calls,
  missing revision where required, over-budget reasoning, and 11 answer-key leakage patterns.

## Findings / gotchas discovered during implementation

### Environment
- A100-PCIE-40GB.
- Local disk `/` is **95% full (24G free)** — do NOT download models locally.
- Both Qwen3.5-9B (19G) and Qwen3.5-4B (8.8G) are cached on EOS:
  `HF_HOME=/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface`
- `TRAINING_DATA_ROOT` defaults to EOS; override to `./training_data` for local iteration.
- `data/neurobench/splits/` is generated by `training/data/make_train_test_split.py`.

### FIXED: SFT loss masking was wrong (`train_grpo.py` `_to_prompt_completion`)
The old code flattened `messages` into plain concatenated strings:
- Tool observations were appended to **completion_parts** → **loss was computed on tool outputs**.
  SOTA (Agent Distillation 2505.17612, partial masking 2505.20023) requires observations be
  in-context but **masked from loss**; training on them teaches the model to invent lab values.
- Prompt/completion were raw strings, so TRL treated the dataset as non-conversational and **never
  applied the chat template** → training text had no `<|im_start|>` role tokens while inference is
  ChatML. A silent train/inference format mismatch.

**Fix (implemented):** `training/chat_template.py` derives a training template from the tokenizer's
own template by inserting `{% generation %}` / `{% endgeneration %}` around the assistant response
body. `run_sft` now feeds the conversational `messages` dataset directly with
`assistant_only_loss=True`. Verified: rendering is byte-identical to the shipped template, and loss
covers thoughts + tool-call XML + final answer only — observations/system/user are context-only.

Note: Qwen3.5's template contains the string `add_generation_prompt` but **no `{% generation %}`
tag** — grepping for "generation" gives a false positive. It must be patched.

### Qwen3.5 tool-call format is XML, not JSON
The chat template renders `tool_calls` as `<tool_call><function=NAME><parameter=K>V</parameter>...`
(matching `--tool-call-parser qwen3_coder`), and renders `role: "tool"` turns as a **user** message
wrapping `<tool_response>`. So trajectories must store *structured* `tool_calls`, not JSON text
embedded in content. `parse_trajectory_from_response` now does this.

Every assistant turn must carry a `<think>` block — the template emits an empty `<think></think>`
otherwise.

### DEFECT: LoRA was frozen on 24 of 32 layers (hybrid architecture)
Qwen3.5 is a **hybrid** stack. `config.text_config.layer_types` on the 9B is
`Counter({'linear_attention': 24, 'full_attention': 8})` — 3 linear-attention layers per
full-attention layer (`full_attention_interval: 4`).

- `full_attention` layers → `Qwen3_5Attention` → `q_proj/k_proj/v_proj/o_proj` (8 layers)
- `linear_attention` layers → `Qwen3_5GatedDeltaNet` → `in_proj_qkv`, `in_proj_z`,
  `in_proj_b`, `in_proj_a`, `out_proj` (24 layers)

The old target list was `[q,k,v,o,gate,up,down]_proj`, so it adapted attention in **0 of 24**
linear-attention layers. Measured on a meta-device instantiation:

| target list | adapted modules | LoRA params (r=64) | layers w/ attention adapters |
| --- | --- | --- | --- |
| old | 128 | 116.4M | **8/32** (linear_attn 0/24) |
| new | 200 | 160.4M | **32/32** (linear_attn 24/24) |

`in_proj_a` / `in_proj_b` are excluded on purpose: shape `(4096, 32)`, so `out_features` (32)
is below the LoRA rank (64) — a rank-64 adapter there has more parameters than the weight it
adapts and cannot be low-rank. Constants live in `train_grpo.py::QWEN35_TARGET_MODULES`; the
probe imports them so probe and training can't drift.

### Liger fused cross-entropy is required, not optional
Qwen3.5's vocab is **248,320**. The logits tensor for one sequence is `seq × 248320`:
at seq=8192 that's 4.07 GB in bf16, ~8.1 GB once cross-entropy upcasts to fp32, plus its
gradient. That single tensor — not the weights — is what OOMs the 40 GB card.

`use_liger_kernel=True` swaps in a **fused linear cross-entropy** that computes loss in
chunks and never materialises the full logits. Measured on the 9B:

| | max seq | peak at 8192 |
| --- | --- | --- |
| without Liger | 6144 (OOM at 8192) | — (36.2 GB just for 6144) |
| with Liger | ≥12288 | **23.9 GB** |

### Sequence-length reality (measured with the Qwen3.5-9B tokenizer, 500 train cases)
- `orchestrator.txt` = 867 tokens; hospital rules = 827–1044 tokens; patient info mean 986 / max 1670.
- Full sequence (system + rules + patient + 6 largest tool outputs): mean 5119, **p90 6369, max 7451**;
  plus ~1200–1800 reasoning tokens → **p90 ≈ 8.2k, max ≈ 9.3k**.
- **The old `max_seq 4096` was silently truncating essentially every trajectory.**
- `max_seq_length` also had **no CLI flag**, so `run_sft_training.sh` could never change it from 4096.

### DEFECT: the dataset's `optimal_actions[].tool_parameters` don't match the tool schemas
Across 200 cases, ground-truth parameters use names the live tools reject:
`order_advanced_imaging.modality` (121), `analyze_csf.tests` (64), `analyze_brain_mri.sequences` (60),
`analyze_brain_mri.include_cervical_spine` (30), `check_drug_interactions.proposed_drug` (30) — plus a
tool `consult_medical_specialist` that isn't in the 12-tool registry.

The prompt rendered these verbatim, so the teacher copied them → 105 missing-required-argument errors
in the first pilot. Fix: `format_optimal_actions` no longer prints `tool_parameters`, drops
non-registry tool names, and the prompt carries the **live schemas** from `ToolRegistry`
(`format_tool_schemas`). We did NOT edit the 600 case files — the ground truth is benchmark data
used by the evaluation metrics.

### `useless_tools` / `harmful_tools` are parameter-scoped, not name-scoped
In **103/600 cases** a tool appears in both `optimal_actions` and `useless_tools` (e.g.
`order_advanced_imaging` is useless with `modality=MR_spectroscopy` but required with the right one).
A name-only ban produced false rejections, so `banned_tool_names()` subtracts the optimal tools.

### One tool call per tool
`get_tool_output_for_call` (and MockServer) key observations by **tool name**, so a second call to the
same tool returns the identical stored output. But `optimal_actions` repeats tools in 197 cases
(`order_specialized_test` ×197, `order_advanced_imaging` ×115, `interpret_labs` ×72). Printing the
same tool as two steps made the teacher call it twice and narrate two different results — a fiction.
`format_optimal_actions` now **merges** repeated tools into one step (`ALSO COVERS (same single call)`),
and the validator rejects duplicates.

## Pilot yield (24 stems, 14 conditions, all difficulties/styles/hospitals)

| round | valid | notes |
| --- | --- | --- |
| v1 (names only, no schemas) | **0/23** | 105 missing args, 14/23 duplicate tool calls |
| v2 (+ live schemas in prompt) | 10/23 | args improved; reference block still induced duplicates |
| v3 (+ merged steps, param-aware bans, tag checks) | **18/23 (78%)** | 4 duplicates + 1 malformed tag |
| v3 + one repair round | **22/23 (96%)** | repair feeds the exact validator issues back to the teacher |

Audit of the 22 (Qwen3.5-9B tokenizer): full sequence mean 5846 / p90 6881 / **max 7929** (< 12288, no
truncation). Supervised tokens mean 1627 / max 2051 — concise, as intended. All 12 tools exercised,
0 test-split leakage, 0 zero-signal examples.

## Measured cost (not estimated)

**42.9k tokens per trajectory** (77 pilot subagents, 3.30M tokens) — the prompt alone is ~8.4k tokens
(mean; p90 10.6k) because it embeds all of the case's tool outputs. Full 1000-trajectory run ≈ **46M
tokens** including a ~10% repair round. The earlier 15k/trajectory estimate was wrong by ~2.8×.

## Files

| Path | Role |
| --- | --- |
| `training/data/make_train_test_split.py` | 500/100 split, 2 held-out conditions (run first) |
| `training/data/generate_gold_trajectories.py` | `--prepare-prompts` / `--assemble` (parse + reject) |
| `scripts/training/generate_trajectories_subagent.md` | teacher prompt template |
| `scripts/training/generate_trajectories_workflow.js` | Workflow: 1 Sonnet subagent per trajectory |
| `scripts/training/probe_max_seq_length.py` | Phase 0 probe (both models, real QLoRA recipe) |
| `scripts/training/audit_trajectories.py` | pre-training audit (length, masking, leakage, diversity) |
| `training/chat_template.py` | `{% generation %}` patch → assistant-only loss |
| `scripts/training/run_sft_training.sh` | reads `max_seq` from the probe JSON |

## Pipeline

```bash
# 1. split (done)
uv run python -m neuroagent.training.data.make_train_test_split

# 2. prompts for the 500 train cases x 2 styles
uv run python -m neuroagent.training.data.generate_gold_trajectories \
    --dataset data/neurobench --output training_data/gold_trajectories_v6 \
    --splits-dir data/neurobench/splits --token-budget <BUDGET> --prepare-prompts

# 3. generate (Workflow tool, Sonnet subagents, chunked & resumable via skip-existing)

# 4. assemble + audit
uv run python -m neuroagent.training.data.generate_gold_trajectories \
    --dataset data/neurobench --output training_data/gold_trajectories_v6 --assemble
HF_HOME=... uv run python agent-platform/scripts/training/audit_trajectories.py \
    --data training_data/gold_trajectories_v6/trajectories.jsonl

# 5. SFT
bash agent-platform/scripts/training/run_sft_training.sh Qwen/Qwen3.5-9B
bash agent-platform/scripts/training/run_sft_training.sh Qwen/Qwen3.5-4B
```

## Phase 0 probe results

_(populated by `scripts/training/probe_max_seq_length.py`; results → `results/sft_probe/max_seq_probe.json`)_

| model | max stable seq_len (bs=1) | peak GB | chosen |
| --- | --- | --- | --- |
| Qwen/Qwen3.5-9B | TBD | | |
| Qwen/Qwen3.5-4B | TBD | | |

Requirement from measurement: **max_seq ≥ 8192** (p90 ≈ 8.2k, max ≈ 9.3k). If the 9B cannot
reach 8192 on this GPU, options are (a) shrink tool-output truncation from 2000 chars,
(b) cap tool calls at 4-5, or (c) train the 9B with a shorter budget than the 4B.
