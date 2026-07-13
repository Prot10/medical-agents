# SFT recipe, hardware, and evaluation — learnings

Everything we established empirically about supervised fine-tuning the small Qwen3.5 students
(4B, 9B) on the gold ReAct trajectories, and about evaluating base-vs-SFT rigorously. This is
the "why" companion to [`distillation.md`](distillation.md) (which covers how the trajectories
are generated). Every number here was measured on the project's A100-PCIE-40GB unless noted.

Scripts referenced:
`agent-platform/scripts/training/` — `run_sft_training.sh`, `run_sft_eval.sh`,
`run_definitive_eval.sh`, `run_weekend_sft.sh`, `_stage.sh`, `_gpu.sh`,
`probe_max_seq_length.py`; `src/neuroagent/training/train_grpo.py` (the `--stage sft` path).

---

## 1. The training recipe

| Knob | Value | Why |
| --- | --- | --- |
| Method | QLoRA (default) or **bf16 LoRA** (`PRECISION=bf16`, opt-in) | bf16 avoids 4-bit quantization error on the base (Unsloth's Qwen3.5 guidance); costs ~2 GB more, fits fine (§3) |
| LoRA rank / alpha | 64 / 128 (α = 2r) | breadth (which modules) matters more than rank (QLoRA ablation) |
| Target modules | **all linear**: `q,k,v,o` + `gate,up,down` + gated-delta-net `in_proj_qkv,in_proj_z,out_proj` | Qwen3.5 is hybrid — 24/32 layers are gated-delta-net; attention-only would freeze most token-mixing |
| lora_dropout | 0.05 | mild regularisation on ~1000 examples |
| Learning rate | **1.5e-4** (9B) / **2e-4** (4B) | LoRA adapters are randomly initialised → ~10× a full-FT LR; 1e-4–2e-4 is the consensus band |
| Epochs | 3, **early stop on eval_loss** (patience 1) | both models overfit slightly at epoch 3 (eval loss ticks up) → load-best keeps epoch 2 |
| Effective batch | 16 (batch 1 × grad-accum 16) | LoRA tolerates large batches worse than full-FT; long sequences force batch 1 |
| Optimizer | `paged_adamw_8bit` (9B) / `adamw_8bit` (4B) | paging guards VRAM spikes on the tighter 9B |
| Scheduler / warmup | cosine, warmup 0.05, weight_decay 0.01, max_grad_norm 1.0 | standard |
| NEFTune | **off** | its embedding noise was tuned for conversational win-rate and degrades exact tool-argument fidelity |
| Loss masking | assistant-only (`assistant_only_loss=True`), tool observations masked out | the model must **read** observations, not learn to generate them |
| max_seq_length | **13312** | longest trajectory is 12,956 tokens *with tool schemas rendered*; truncation eats the final diagnosis |

Observed loss curves (both healthy, no divergence): 9B train 1.19→0.58, eval 0.83→0.79→0.80;
4B train 1.27→0.54, eval 0.86→0.83→0.85. `grad_norm` ~0.03–0.04 (small but stable — expected
for a rank-64 adapter on a frozen base).

### flash-linear-attention is required (2.2× speedup)
Qwen3.5's gated-delta-net (linear-attention) layers run a **pure-torch fallback** unless the
`fla` Triton kernels are present. Installing `flash-linear-attention` cut the 4B SFT step from
**~66s to ~30s** (measured, same recipe). It is pure Triton — no `nvcc`, installs on this
torch 2.11 / CUDA 13 / py3.13 stack. Its siblings `causal-conv1d` and `flash-attn` are **not**
installable here (no cu13/py313 wheels, need nvcc) and not worth it — torch SDPA already gives
FlashAttention-2-class kernels for the full-attention layers, and `fla` supplies the expensive
delta-rule core. The residual "fast path not available" warning is cosmetic (the gate needs
both libs, but each kernel has a correct torch fallback and `fla` captures the speedup). It is
a dependency of `agent-platform[training]`; the training script warns if it is missing.

---

## 2. What sequence length is, and the concepts around it

**`max_seq_length`** is the hard token cap on one training example — the whole rendered
conversation: system prompt + the ~3k-token tool-schema block + every turn. Anything longer is
**truncated at the tail**, and the tail is the final diagnosis. It drives three costs:

1. **Activation memory** (dominant). Every layer stores intermediate tensors for the backward
   pass. This grows ~linearly per token for the MLPs and **quadratically** for naive attention
   (an `L×L` score matrix). This is what OOMs a card at long context.
2. **Step time** — more tokens, more FLOPs.
3. **The output logits tensor** — separate from attention; the thing the softmax trick fixes (§4).

Sequence length does **not** change the parameter count or optimizer state.

### The interacting variables (the vocabulary)
| Concept | What it is | Trade |
| --- | --- | --- |
| **batch size** | examples per forward pass | memory ∝ batch × seq_len; we use 1 (long sequences) |
| **gradient accumulation** | sum grads over N micro-batches, then one step | effective batch = batch × accum; raises effective batch with **no** extra memory (time-for-memory) |
| **gradient checkpointing** | store a few checkpoints, **recompute** the rest in backward | big activation-memory cut for ~30% more compute (memory-for-time) — the main lever for long context |
| **padding vs packing** | packing concatenates short examples to fill `max_seq_length` | packing needs a padding-free/flattening collator or tokens attend across trajectory boundaries and corrupt multi-turn reasoning |
| **FlashAttention / SDPA** | attention that never materialises the `L×L` matrix (tiled, recomputed) | turns attention memory from quadratic to ~linear; torch SDPA provides it on the A100 |
| **precision / quantization** | bf16 vs 4-bit (QLoRA) for the frozen base | changes **resident weight** memory only, not activations (§3) |
| **KV cache** | *inference only* — stored keys/values for generated tokens | grows with generated length; dominates vLLM memory, **not** training |

---

## 3. bf16 LoRA vs QLoRA — measured (controlled)

QLoRA stores the frozen base in 4-bit; bf16 stores it in 16-bit. The LoRA adapter, its
gradients, and optimizer state are identical either way. **Controlled** head-to-head on the 9B
at seq 13312 — same optimizer (`paged_adamw_8bit`), same gradient checkpointing, same Liger,
`expandable_segments:True`, peak read via `torch.cuda.max_memory_allocated()`:

| @ seq 13312, identical settings | resident weights | **peak** | headroom (42 GB) |
| --- | --- | --- | --- |
| **QLoRA (4-bit)** | 12.4 GB | **25.2 GB** | 17.2 |
| **bf16 LoRA** | 18.5 GB | **27.2 GB** | 15.2 |

**QLoRA is lower (~2 GB), the expected ordering** — saving memory is the whole point of QLoRA.

> A caution, learned the hard way: an earlier *uncontrolled* comparison made it look like bf16
> used *less* than QLoRA (28.5 vs 30.9 GB). That was an artifact — the QLoRA figure came from a
> probe with a paged 8-bit optimizer measured via `nvidia-smi`, and **paged optimizers map
> unified memory that inflates the NVML/reserved figure far above the true allocated tensors**
> (bitsandbytes; PyTorch allocator fragmentation). Always compare with identical optimizer and
> `max_memory_allocated()`, not `nvidia-smi`. bf16 is not cheaper than QLoRA; QLoRA is designed
> to save ~the resident-weight delta.

Two real facts survive: (1) at long context the gap is **much smaller than the 6 GB
resident-weight difference** (down to ~2 GB) because the shared activation memory dominates —
so the weight saving matters less at 13k tokens than at short context; and (2) **both fit
comfortably** (25–27 GB, ~15 GB headroom). So the choice is not about memory.

**Why we still switch the retrain to bf16 LoRA:** quality, not memory. Unsloth recommends
against 4-bit for Qwen3.5 — quantizing the base adds error the LoRA has to work around. bf16
keeps the base exact and costs only ~2 GB more, which fits. It is an **opt-in flag**
(`PRECISION=bf16` in `run_sft_training.sh`); QLoRA remains the default.

---

## 4. The final-softmax trick (Liger fused linear cross-entropy)

The last layer maps each token's hidden vector to a score over the **entire vocabulary**;
softmax → probabilities; cross-entropy vs the true next token. Qwen3.5's vocabulary is
**~248,000 tokens**, so the logits tensor is `seq_len × 248k`. At 13,312 that is ~3.3 **billion**
numbers — **~6.6 GB in bf16, ~13 GB after cross-entropy upcasts to fp32** for numerical
stability. For one long sequence that single tensor is often the largest object on the GPU —
larger than the model activations — and it is what OOMs a 40 GB card at long context.

**Liger fused linear cross-entropy never materialises it.** It fuses the final linear
projection + softmax + cross-entropy into one kernel that walks the sequence in **chunks**: per
chunk it computes the logits, the loss, and the gradient, accumulates the loss, and discards the
chunk's logits before the next. Identical loss and gradients; peak memory for the output step
drops from ~13 GB to a small constant. This is what makes a 248k-vocab model trainable at 13k
context on 40 GB, in either precision. We keep Liger on.

> Caveat we verified: `assistant_only_loss` was once silently dropped when Liger was enabled
> (huggingface/trl#3781), training on tool observations. This TRL pin honours the mask
> (1532/9333 tokens supervised, measured), and `train_grpo._assert_loss_is_assistant_only`
> re-checks a real batch before step 1 — it fails the run if every token or no token is
> supervised.

---

## 5. Storage / infrastructure

Measured asymmetry on the EOS FUSE mount: **writes are fast (221 MB/s sequential — a 320 MB
adapter in 1.5 s); reads are pathologically slow (~1–2 h to load a full model, scattered small
reads).** So:

- **Base models** live on EOS but are **staged into `/dev/shm` (RAM tmpfs)** once per run and
  loaded from there (`_stage.sh`, idempotent + validated — it refuses to proceed until the
  snapshot's `config.json` and every safetensors shard resolve, so a half-finished copy can't
  masquerade as done). `/dev/shm` is RAM, **not** the (full) local disk.
- **Checkpoints / adapters / results** are written **straight to EOS** — small and fast to
  write there; never on local disk.
- **Eval serves base + LoRA from one vLLM process** (`--enable-lora`, adapter addressed as
  `sft`) — no 18 GB merge, no slow merged-model reload. Verified: vLLM supports LoRA on
  Qwen3.5's gated-delta-net (`PunicaWrapperGPU`), base loads from RAM in ~2 s.
- **GPU teardown** between phases is verified, not hoped: `_gpu.sh free_gpu` SIGKILLs the vLLM
  EngineCore (which does not reliably die with its launcher) and **blocks until nvidia-smi shows
  the memory released**, before training loads the model.

### Monitoring during a run
- Pre-flight **sequence-length report**: median/p95/max tokens with tools rendered, and a loud
  warning if anything would truncate (current data at 13312: median 10417, max 11551, **zero
  truncation**).
- Live **loss-mask verification** before step 1 (above).
- `logging_steps=5` for finer loss / grad_norm / LR in tmux; TRL's tqdm bar; rich progress bar
  in the eval.

---

## 6. Evaluation methodology (literature-aligned)

Base-vs-SFT on the held-out 100-case test split. The first runs (temp=1.0, single session per
condition) were **inconclusive by construction**: a single temp=1.0 run swings ±3.7%
run-to-run, and with only 100 cases the 95% bootstrap CI on the accuracy delta is ±8–10% — the
finite test set dominates, not temperature. The literature-aligned protocol (`run_definitive_eval.sh`):

- **Greedy (temp=0, 1 pass)** → primary pass@1, deterministic and comparable (HumanEval
  convention, Chen et al. 2021). At temp 0 we force `top_p=1`, `presence_penalty=0`.
- **Sampled (temp=0.7, 3×)** → reliability / variance across trials (τ-bench pass^k, Yao et al.
  2024; self-consistency, Wang et al.).
- **Full traces saved as judge bundles** → the 8-dimension LLM-judge composite (MT-Bench,
  Zheng et al.; Med-PaLM rubric, Singhal et al.).
- **Paired statistics** in `compare` (base and SFT see the same cases → paired is far more
  powerful than unpaired): **bootstrap CI over cases + McNemar** (Dietterich 1998; Efron), plus
  a **reliability metric** (per-case pass-rate SD across repeats).

### The LLM-judge composite
Run as the **`llm-judge` Claude subagent** (not local vLLM). Flow: `prepare_judge_batches.py` →
one llm-judge subagent per batch (reads bundles, writes per-dimension 0–5 scores) →
`aggregate_judge_scores.py` recomputes the weighted composite independently (diagnostic 0.22,
safety 0.18, integration 0.16, differential 0.16, evidence-ID 0.11, tool-efficiency 0.09,
uncertainty 0.08; ×red-herring variant) with a **non-compensatory safety gate** (any dimension
≤ threshold clamps the composite to 0). Verified end-to-end (composites ~0.73–0.89 on sample
bundles). It scores reasoning quality that binary top-1 misses.

### Verified references for the methods section
| Topic | Reference |
| --- | --- |
| pass@k / greedy pass@1 | Chen et al. (2021), *Evaluating LLMs Trained on Code*, arXiv:2107.03374 |
| self-consistency | Wang et al. (2023), ICLR, arXiv:2203.11171 |
| agent reliability / pass^k | Yao et al. (2024), *τ-bench*, arXiv:2406.12045 (verify the exact estimator vs the PDF) |
| LLM-as-judge | Zheng et al. (2023), *MT-Bench*, arXiv:2306.05685 |
| clinical rubric eval | Singhal et al. (2023), *Med-PaLM*, Nature 620 |
| paired significance | Dietterich (1998), *Neural Computation* (McNemar); Efron (1979/1993) (bootstrap) |
| underpowered benchmarks | Card et al. (2020), EMNLP, arXiv:2010.06595 |

---

## 7. Results, diagnosis, and what SOTA would do next

**Results (temp=1.0, existing adapters, paired):** neither model's accuracy delta is
significant. 9B: Δtop1 +1.7%, 95% CI [−2.7%, +6.3%], McNemar p=0.79. 4B: Δtop1 −1.1%, n.s. **The
one significant finding: SFT halves run-to-run variance** (9B per-case pass-rate SD 0.156 →
0.094) — the τ-bench reliability axis. The 9B improved consistency; the 4B mildly regressed on
accuracy but got more cost-efficient (fewer tools).

**Diagnosis — this is the textbook *Superficial Alignment* signature** (LIMA, Zhou 2023): vanilla
imitation SFT re-weights an output distribution the base already had, rather than adding
capability. "SFT Memorizes, RL Generalizes" (Chu et al., ICML 2025) frames SFT's real job as
**stabilising format as a warmup for RL**, not moving accuracy. The trajectory audit rules out a
data-quality cause: the data is good (35% hard cases, 85% unique reasoning openings, median
80-word `<think>` blocks, 385-word structured assessments, 40% unique tool sequences).

**What the literature says to do for the rerun (prioritised):**
1. **Diagnose first (cheap):** report pass@k and the teacher–student gap. If the base catches up
   at pass@k, accuracy needs RFT/RL, not more SFT (Yue et al., arXiv:2504.13837). The definitive
   eval is this diagnostic.
2. **Rejection-sampling fine-tuning (RFT/STaR)** — the best-evidenced single change: sample N
   trajectories from your *own* model, keep only the diagnostically-correct ones (gold labels =
   verifier), SFT on those. Beat vanilla SFT 35.9→49.3 on GSM8K (Yuan et al., 2023); helps most
   when the base is near-ceiling on imitation. What DeepSeek-R1 and Llama-3 do.
3. **Add ~5–10% error-recovery / abstention negatives** (Agent-FLAN) and a **general-data replay
   mix** (~1:1) to prevent forgetting.
4. **Recipe deltas (done / cheap):** bf16 LoRA over QLoRA (§3); all linear layers ✓; LR
   1.5e-4/2e-4 ✓; ≤3 epochs ✓; assistant-only loss ✓.
5. **Post-SFT stage:** SFT → RFT → DPO/GRPO with gold diagnoses as a binary verifier (RLVR,
   Tülu-3). Honest caveat: RLVR gains are often single-digit, and for small students Qwen3's own
   report finds strong-teacher distillation can beat RL — so scope it as an experiment gated on
   a real teacher–student gap.

**One-line strategic read:** "same accuracy, more consistent" is the *expected* outcome of
imitation SFT on a base that already has the format. The fix is not cleaner imitation data — it
is verified on-policy data (RFT) plus a verifier-based stage, with harder cases and
error-recovery negatives.
