"""GRPO training script for NeuroAgent tool-calling fine-tuning.

Two-stage training:
  Stage 1 (SFT warmup): Short supervised fine-tuning on top trajectories
  Stage 2 (GRPO RL): Reinforcement learning with composite reward

Supports both TRL (Hugging Face) and veRL (Volcano Engine) backends.
Default: TRL GRPOTrainer with LoRA (simpler, single-node friendly).

Usage:
    # Stage 1: SFT warmup
    python -m neuroagent.training.train_grpo \
        --stage sft \
        --model Qwen/Qwen3.5-9B \
        --data training_data/grpo_dataset/train.jsonl \
        --output checkpoints/sft_warmup

    # Stage 2: GRPO
    python -m neuroagent.training.train_grpo \
        --stage grpo \
        --model checkpoints/sft_warmup \
        --data training_data/grpo_dataset/train.jsonl \
        --output checkpoints/grpo_final

    # veRL multi-GPU (4x A100)
    python -m neuroagent.training.train_grpo \
        --stage grpo \
        --backend verl \
        --model Qwen/Qwen3.5-9B \
        --data training_data/grpo_dataset/train.parquet
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
from pathlib import Path
from typing import Any

# Qwen3.5's gated-delta-rule layers run through flash-linear-attention, which prefers a TileLang
# backend that shells out to the pip-installed CUDA 13 nvcc. On this box that nvcc rejects its
# own bundled headers ("CUDA compiler and CUDA toolkit headers are incompatible"), and only in
# the BACKWARD kernel — the forward compiles, so a run gets through generation and the first
# rollout before dying in loss.backward(). Pin fla to its Triton backend instead.
#
# Verified rather than assumed: with the default backend the gated_delta_rule backward raises
# that compile error; with FLA_TILELANG=0 forward and backward both produce finite gradients,
# the forward agrees with fla's independent recurrent implementation to 4.8e-3 relative, and the
# gradient agrees with a finite-difference directional derivative of its own forward to 3.5e-2
# (the bf16 floor). setdefault, so this can be flipped back once the packaging is fixed.
os.environ.setdefault("FLA_TILELANG", "0")

logger = logging.getLogger(__name__)


def _configure_split_logging(log_file: str | None) -> None:
    """Verbose logs + Python warnings to a FILE; keep the terminal for the progress UI.

    Training prints a lot — transformers/TRL INFO, deprecation warnings, per-step metric dicts.
    Routed to `log_file`, the terminal is left with the tqdm step bar and the concise reward
    line from _TerminalProgressCallback. Only ERROR records still surface on the terminal so a
    crash is never buried in a file. `captureWarnings` folds warnings.warn (e.g. the torch_dtype
    and generation_config notices) into the same file instead of the terminal.
    """
    import os
    import sys

    # 1. Env flags that must be set before the libraries configure themselves, to kill the
    #    progress bars / banners that write straight to the terminal, bypassing `logging`:
    #      HF_HUB_DISABLE_PROGRESS_BARS  -> the "Loading weights" / download bars
    #      BITSANDBYTES_NOWELCOME        -> the bnb ASCII welcome banner (QLoRA path)
    #      TOKENIZERS_PARALLELISM        -> the "The current process just got forked" warning
    #      TRANSFORMERS_NO_ADVISORY_WARNINGS -> transformers advisory notices
    os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
    os.environ.setdefault("BITSANDBYTES_NOWELCOME", "1")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
    # torch's C++ (glog) logging — the "I0716 … FakeTensor cache stats" dumps — bypasses Python
    # logging entirely. These must be set before torch is first imported; main() calls this
    # before run_grpo_trl does the (lazy) `import torch`, so they take effect.
    os.environ.setdefault("TORCH_CPP_LOG_LEVEL", "ERROR")
    os.environ.setdefault("GLOG_minloglevel", "2")

    logging.captureWarnings(True)  # warnings.warn (torch_dtype, generation_config) -> logging -> file
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    for h in list(root.handlers):
        root.removeHandler(h)
    if log_file:
        from pathlib import Path as _Path
        _Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s"))
        root.addHandler(fh)
    err = logging.StreamHandler(sys.stderr)
    err.setLevel(logging.ERROR)
    err.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    root.addHandler(err)

    # 2. transformers/peft/etc. install their OWN stderr handler and never propagate, so their
    #    INFO/WARNING (the fla "fast path" note, the tokenizer/PAD message, TRL logs) hit the
    #    terminal regardless of the root config. Point them at the root's file handler instead
    #    and turn off their progress bars.
    try:
        from transformers.utils import logging as hf_logging

        hf_logging.disable_default_handler()
        hf_logging.enable_propagation()
        hf_logging.disable_progress_bar()
    except Exception:  # transformers layout changed — fall back to level bumping below
        pass
    try:
        import datasets

        datasets.disable_progress_bars()  # the .map() tokenisation bars
        datasets.utils.logging.disable_default_handler()
        datasets.utils.logging.enable_propagation()
    except Exception:
        pass
    for name in ("transformers", "datasets", "peft", "trl", "accelerate", "bitsandbytes",
                 "huggingface_hub", "torch"):
        lg = logging.getLogger(name)
        lg.setLevel(logging.INFO)
        lg.propagate = True
        # drop any private stderr handler the library attached to its own logger
        for h in list(lg.handlers):
            lg.removeHandler(h)

    # 3. Uncaught exceptions (a CUDA OOM during generation, a dtype mismatch) print their
    #    traceback via the default sys.excepthook straight to stderr — which under this split
    #    setup means the terminal, NOT the log file. So a crash leaves the log ending mid-step
    #    with no error, undiagnosable after the terminal is gone (exactly how the 4B GRPO run
    #    died at step 232). Route the traceback through logging so it lands in the file too;
    #    keep Ctrl-C on the default path so an intentional interrupt is not logged as a crash.
    _prev_excepthook = sys.excepthook

    def _log_uncaught(exc_type, exc, tb):
        if issubclass(exc_type, KeyboardInterrupt):
            _prev_excepthook(exc_type, exc, tb)
            return
        logging.getLogger("__main__").critical(
            "Uncaught exception — training aborted", exc_info=(exc_type, exc, tb)
        )
        _prev_excepthook(exc_type, exc, tb)

    sys.excepthook = _log_uncaught


def _quiet_torch_loggers() -> None:
    """Raise torch's own Python loggers above INFO — call right AFTER `import torch`.

    torch installs its logging handlers at import time, so this cannot live in
    _configure_split_logging (which runs before torch is imported). Without it, torch dumps
    like the fake_tensor "cache stats" (an atexit hook) and dynamo/inductor INFO leak to the
    terminal past every other guard.
    """
    for name in ("torch._subclasses.fake_tensor", "torch._dynamo", "torch._inductor",
                 "torch._logging", "torch.distributed"):
        logging.getLogger(name).setLevel(logging.WARNING)


def _make_terminal_progress_callback(model_tag: str = "GRPO"):
    """A modern, always-visible Rich training bar with semantic colours.

    TRL's own tqdm bar is disabled (disable_tqdm=True) and its 50-key metric dict goes to the
    log file; this renders the signal worth watching, live, on the terminal:

        ⠹ GRPO Qwen3.5-4B ━━━━╸  40/250  reward 0.312 ↑0.021  eval 0.334  best 0.334  loss +0.001  ETA 2:41:03

    Colours carry meaning: reward green, its step-over-step delta green up / red down, held-out
    eval magenta, best-so-far bold-green, loss dim. The spinner animates on Rich's refresh thread
    even during the ~2-minute generation phase between steps, so "0/250" never looks frozen —
    it's the model rolling out completions, not a hang.
    """
    from rich.console import Console
    from rich.progress import (
        BarColumn,
        MofNCompleteColumn,
        Progress,
        SpinnerColumn,
        TextColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
    )
    from transformers import TrainerCallback

    console = Console()

    class _TerminalProgressCallback(TrainerCallback):
        def __init__(self) -> None:
            self.progress: Progress | None = None
            self.task = None
            self.prev_reward: float | None = None
            self.best: float | None = None

        def _fields(self) -> dict:
            return {"reward": "[dim]--", "delta": "", "eval": "[dim]--",
                    "best": "[dim]--", "loss": "[dim]--"}

        def on_train_begin(self, args, state, control, **kwargs):
            self.progress = Progress(
                SpinnerColumn(style="cyan"),
                TextColumn(f"[bold blue]{model_tag}"),
                BarColumn(bar_width=None, complete_style="green", finished_style="bold green"),
                MofNCompleteColumn(),
                TextColumn("[green]reward {task.fields[reward]}"),
                TextColumn("{task.fields[delta]}"),
                TextColumn("[magenta]eval {task.fields[eval]}"),
                TextColumn("[bold green]best {task.fields[best]}"),
                TextColumn("[dim]loss {task.fields[loss]}"),
                TextColumn("[dim]ETA"),
                TimeRemainingColumn(),
                TimeElapsedColumn(),
                console=console,
            )
            self.progress.start()
            self.task = self.progress.add_task(
                "train", total=state.max_steps or None, **self._fields()
            )

        def on_log(self, args, state, control, logs=None, **kwargs):
            if not self.progress or self.task is None or not logs:
                return
            # The full metric dict no longer prints to the terminal (PrinterCallback removed);
            # keep it in the log file so every step is analysable later.
            if "reward" in logs or "eval_reward" in logs:
                logger.info("step %d metrics: %s", int(state.global_step), logs)
            upd: dict = {}
            if "reward" in logs:
                r = float(logs["reward"])
                if self.prev_reward is not None:
                    diff = r - self.prev_reward
                    arrow, col = (("↑", "green") if diff > 0
                                  else ("↓", "red") if diff < 0 else ("→", "dim"))
                    upd["delta"] = f"[{col}]{arrow}{abs(diff):.3f}[/{col}]"
                self.prev_reward = r
                upd["reward"] = f"[green]{r:.3f}"
                if isinstance(logs.get("loss"), (int, float)):
                    upd["loss"] = f"{float(logs['loss']):+.4f}"
            if "eval_reward" in logs:
                e = float(logs["eval_reward"])
                upd["eval"] = f"[magenta]{e:.3f}"
                if self.best is None or e > self.best:
                    self.best = e
                    upd["best"] = f"[bold green]{e:.3f}"
            self.progress.update(self.task, completed=int(state.global_step), **upd)

        def on_train_end(self, args, state, control, **kwargs):
            if self.progress:
                self.progress.update(self.task, completed=state.max_steps or state.global_step)
                self.progress.stop()
            console.print(
                f"[bold green]✓ GRPO training complete[/bold green] — "
                f"{int(state.global_step)} steps, best held-out reward "
                f"[bold]{self.best if self.best is not None else float('nan'):.3f}[/bold]"
            )

    return _TerminalProgressCallback()


# ---------------------------------------------------------------------------
# LoRA configuration
# ---------------------------------------------------------------------------

# Qwen3.5 is a *hybrid* architecture: `config.layer_types` interleaves 3 `linear_attention`
# layers (Qwen3_5GatedDeltaNet) for every 1 `full_attention` layer (Qwen3_5Attention).
# On Qwen3.5-9B that is 24 linear-attention vs 8 full-attention layers.
#
# The classic ["q_proj","k_proj","v_proj","o_proj"] list only exists inside the 8 full
# attention layers, so targeting it alone leaves the token-mixing of 24/32 layers entirely
# frozen. The gated-delta-net layers project through different module names.
QWEN35_FULL_ATTENTION_MODULES = ["q_proj", "k_proj", "v_proj", "o_proj"]

# Gated-delta-net (linear attention) projections.
# `in_proj_a` / `in_proj_b` are deliberately excluded: they are (hidden_size, num_v_heads)
# = (4096, 32) per-head gating projections, so out_features < the usual LoRA rank. A rank-64
# adapter there holds more parameters than the weight it adapts and cannot be low-rank at all.
QWEN35_LINEAR_ATTENTION_MODULES = ["in_proj_qkv", "in_proj_z", "out_proj"]

QWEN35_MLP_MODULES = ["gate_proj", "up_proj", "down_proj"]

QWEN35_TARGET_MODULES = (
    QWEN35_FULL_ATTENTION_MODULES + QWEN35_LINEAR_ATTENTION_MODULES + QWEN35_MLP_MODULES
)


def get_lora_config(rank: int = 64, alpha: int = 128, target_modules: list[str] | None = None):
    """Build LoRA config covering BOTH attention families of the hybrid Qwen3.5 stack."""
    from peft import LoraConfig

    return LoraConfig(
        r=rank,
        lora_alpha=alpha,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=target_modules or QWEN35_TARGET_MODULES,
    )


def get_quantization_config():
    """Build BitsAndBytes config for QLoRA (NF4 quantization)."""
    import torch
    from transformers import BitsAndBytesConfig

    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_sft_data(data_path: str, top_fraction: float = 0.1) -> list[dict]:
    """Load top trajectories for SFT warmup.

    Selects the top `top_fraction` by reward as gold demonstrations.
    """
    path = Path(data_path)
    examples = []

    if path.suffix == ".jsonl":
        with open(path) as f:
            for line in f:
                examples.append(json.loads(line))
    elif path.suffix == ".json":
        examples = json.loads(path.read_text())
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")

    # For full-trajectory format, flatten completions with rewards
    flat = []
    for ex in examples:
        if "completions" in ex:
            for comp, rew in zip(ex["completions"], ex["rewards"]):
                flat.append({
                    "prompt": ex["prompt"],
                    "completion": comp,
                    "reward": rew,
                })
        else:
            flat.append(ex)

    # Sort by reward descending, take top fraction
    flat.sort(key=lambda x: x.get("reward", 0), reverse=True)
    n_top = max(1, int(len(flat) * top_fraction))
    top = flat[:n_top]

    logger.info("SFT data: %d total → top %d (%.0f%%)", len(flat), n_top, top_fraction * 100)
    return top


def _log_sequence_stats(dataset, tokenizer, max_seq_length: int, tools: list[dict]) -> None:
    """Log the token-length distribution and truncation count before training starts."""
    import statistics

    lengths = []
    for row in dataset:
        text = tokenizer.apply_chat_template(
            row["messages"], tools=row.get("tools") or tools, tokenize=False
        )
        lengths.append(len(tokenizer(text, add_special_tokens=False).input_ids))
    lengths.sort()
    n = len(lengths)
    p = lambda q: lengths[min(n - 1, int(n * q))]
    truncated = sum(1 for x in lengths if x > max_seq_length)

    logger.info(
        "Sequence lengths (tokens, with tools rendered): median=%d p95=%d max=%d  | max_seq_length=%d",
        int(statistics.median(lengths)), p(0.95), lengths[-1], max_seq_length,
    )
    if truncated:
        logger.warning(
            "%d/%d trajectories (%.1f%%) exceed max_seq_length=%d and WILL BE TRUNCATED at the "
            "tail — the final diagnosis is what gets cut. Raise --max-seq-length or shorten prompts.",
            truncated, n, 100 * truncated / n, max_seq_length,
        )
    else:
        logger.info("No truncation: every trajectory fits in %d tokens ✓", max_seq_length)


def _assert_loss_is_assistant_only(trainer, tokenizer) -> None:
    """Fail loudly if the loss covers tool observations.

    `assistant_only_loss=True` is a request, not a guarantee: it needs `{% generation %}`
    markers in the chat template, and TRL has shipped releases where enabling Liger threw
    the masks away (huggingface/trl#3781). Both failures are silent — training proceeds and
    the model learns to hallucinate tool outputs instead of reading them. Check one real
    batch before committing a GPU to three epochs.
    """
    batch = trainer.data_collator([trainer.train_dataset[0]])
    labels = batch["labels"][0]
    supervised = int((labels != -100).sum())
    total = int(labels.numel())

    if supervised == 0:
        raise RuntimeError(
            "assistant_only_loss is on but no token is supervised — the chat template has "
            "no {% generation %} markers, or TRL dropped the assistant mask."
        )
    if supervised == total:
        raise RuntimeError(
            "Every token is supervised: the assistant mask was dropped (see trl#3781). "
            "Loss would fall on tool observations. Set --no-liger or upgrade TRL."
        )
    logger.info(
        "Loss mask verified: %d/%d tokens supervised (%.1f%% — assistant turns only)",
        supervised, total, 100 * supervised / total,
    )


def _save_run_summary(
    output_dir: str,
    trainer,
    result,
    args,
    model_name: str,
    n_train: int,
    n_eval: int,
    precision: str = "unknown",
) -> None:
    """Persist the hyperparameters and the loss curve beside the adapter.

    A checkpoint whose recipe you cannot reconstruct is not a result.
    """
    summary = {
        "model": model_name,
        "precision": precision,  # "qlora" (4-bit NF4) or "bf16"
        "n_train_trajectories": n_train,
        "n_eval_trajectories": n_eval,
        "hyperparameters": {
            "learning_rate": args.learning_rate,
            "epochs": args.num_train_epochs,
            "per_device_train_batch_size": args.per_device_train_batch_size,
            "gradient_accumulation_steps": args.gradient_accumulation_steps,
            "effective_batch_size": args.per_device_train_batch_size * args.gradient_accumulation_steps,
            "max_length": args.max_length,
            "optim": str(args.optim),
            "lr_scheduler_type": str(args.lr_scheduler_type),
            "warmup_ratio": args.warmup_ratio,
            "weight_decay": args.weight_decay,
            "max_grad_norm": args.max_grad_norm,
            "neftune_noise_alpha": args.neftune_noise_alpha,
            "assistant_only_loss": getattr(args, "assistant_only_loss", None),
            "use_liger_kernel": args.use_liger_kernel,
            "seed": args.seed,
        },
        "train_runtime_s": result.metrics.get("train_runtime"),
        "final_train_loss": result.metrics.get("train_loss"),
        "log_history": trainer.state.log_history,
        "best_metric": trainer.state.best_metric,
        "best_checkpoint": trainer.state.best_model_checkpoint,
    }
    path = Path(output_dir) / "run_summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, default=str) + "\n")
    logger.info("Run summary written to %s", path)


def _agent_tool_definitions() -> list[dict]:
    """Exactly the tool schemas `AgentOrchestrator` sends to the model at inference.

    Derived from the same registry and the same `allowed_tools` / `excluded_tools` config,
    so the training prompt cannot drift from the serving prompt.
    """
    from ..agent.config import load_agent_config
    from ..agent.planner import restrict_tools
    from ..tools.tool_registry import ToolRegistry

    config = load_agent_config()
    return restrict_tools(
        ToolRegistry.create_default_registry().get_all_definitions(),
        allowed_tools=config.allowed_tools,
        excluded_tools=config.excluded_tools,
    )


def load_grpo_data(data_path: str) -> list[dict]:
    """Load GRPO training data (grouped by prompt)."""
    path = Path(data_path)
    examples = []

    if path.suffix == ".jsonl":
        with open(path) as f:
            for line in f:
                examples.append(json.loads(line))
    elif path.suffix == ".json":
        examples = json.loads(path.read_text())
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")

    logger.info("GRPO data: %d examples loaded", len(examples))
    return examples


# ---------------------------------------------------------------------------
# Stage 1: SFT Warmup
# ---------------------------------------------------------------------------

def _split_trajectories(
    examples: list[dict],
    splits_dir: str,
    val_fraction: float = 0.1,
    seed: int = 42,
) -> tuple[list[dict], list[dict]]:
    """Split trajectories into train/val, carving validation out of the TRAIN split.

    The held-out test set (`test_cases.txt`) is never touched here — no gold trajectory
    exists for it by construction. Validation is carved from train *by case_id*, so both
    styles of a case land on the same side and a case cannot be memorised in train and
    scored in val.
    """
    splits_path = Path(splits_dir)
    train_file = splits_path / "train_cases.txt"
    test_file = splits_path / "test_cases.txt"

    if not train_file.exists():
        logger.warning("No train_cases.txt at %s, using all data for training", splits_path)
        return examples, []

    train_cases = {c for c in train_file.read_text().split() if c}
    test_cases = {c for c in test_file.read_text().split() if c} if test_file.exists() else set()

    leaked = [ex for ex in examples if ex.get("case_id", "") in test_cases]
    if leaked:
        raise ValueError(
            f"{len(leaked)} trajectories belong to held-out test cases "
            f"(e.g. {leaked[0].get('case_id')}). Regenerate prompts from the train split."
        )

    unknown = [ex for ex in examples if ex.get("case_id", "") not in train_cases]
    if unknown:
        logger.warning("%d trajectories have case_ids outside the train split", len(unknown))

    val_case_ids: set[str] = set()
    if val_fraction > 0:
        ordered = sorted(train_cases)
        rng = random.Random(seed)
        rng.shuffle(ordered)
        n_val = int(len(ordered) * val_fraction)
        val_case_ids = set(ordered[:n_val])

    train = [ex for ex in examples if ex.get("case_id", "") not in val_case_ids]
    val = [ex for ex in examples if ex.get("case_id", "") in val_case_ids]

    logger.info(
        "Split: %d train / %d val trajectories (%d val cases, val_fraction=%.2f)",
        len(train), len(val), len(val_case_ids), val_fraction,
    )
    return train, val


def run_sft(
    model_name: str,
    data_path: str,
    output_dir: str,
    lora_rank: int = 64,
    lora_alpha: int = 128,
    epochs: int = 3,
    batch_size: int = 1,
    # LoRA adapters are randomly initialised, not pretrained, so they want ~10x the LR of a
    # full fine-tune. 2e-5 is a full-FT rate and underfits a rank-64 adapter.
    # Unsloth defaults to 2e-4; Thinking Machines' LoRA scaling work puts the optimum near
    # 10x full-FT. 1.5e-4 sits in the middle of the 1e-4..2e-4 consensus band.
    learning_rate: float = 1.5e-4,
    max_seq_length: int = 4096,
    bf16: bool = True,
    qlora: bool = False,
    top_fraction: float = 1.0,
    splits_dir: str | None = None,
    val_fraction: float = 0.1,
    use_liger: bool = True,
    grad_accum: int = 16,
    optim: str = "paged_adamw_8bit",
    # NEFTune's embedding noise was tuned for free-form conversational win-rate, not for
    # exact tool arguments. Off by default: noise on reasoning tokens is reported to make
    # the reasoning less load-bearing for the action that follows it.
    neftune_alpha: float | None = None,
    early_stopping_patience: int = 1,
    seed: int = 42,
    max_steps: int = -1,
) -> None:
    """Run SFT warmup on top trajectories.

    Supports two data formats:
    1. Gold trajectories (from generate_gold_trajectories.py): each example has
       a "messages" field with the full multi-turn conversation.
    2. Legacy format: each example has "prompt" and "completion" fields.

    Args:
        qlora: If True, load base model in 4-bit NF4 quantization (QLoRA).
        splits_dir: Path to the split directory (e.g., data/neurobench/splits/) holding
            train_cases.txt / test_cases.txt. Validation is carved out of the train split.
        val_fraction: Fraction of TRAIN cases held out for eval_loss / best-model selection.
    """
    import torch
    _quiet_torch_loggers()
    from datasets import Dataset
    from peft import get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import SFTConfig, SFTTrainer

    from .chat_template import apply_training_chat_template

    logger.info("Loading model: %s (qlora=%s)", model_name, qlora)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    load_kwargs: dict = {
        "device_map": "auto",
        "trust_remote_code": True,
    }
    if qlora:
        load_kwargs["quantization_config"] = get_quantization_config()
    else:
        load_kwargs["dtype"] = torch.bfloat16 if bf16 else torch.float16

    model = AutoModelForCausalLM.from_pretrained(model_name, **load_kwargs)

    # Prepare for k-bit training if QLoRA
    if qlora:
        model = prepare_model_for_kbit_training(model)

    # Apply LoRA
    lora_config = get_lora_config(rank=lora_rank, alpha=lora_alpha)
    model = get_peft_model(model, lora_config)
    _tr, _all = model.get_nb_trainable_parameters()
    logger.info("Trainable params: %d / %d (%.2f%%)", _tr, _all, 100 * _tr / _all)

    # Load data and optionally split into train/val
    top_examples = load_sft_data(data_path, top_fraction=top_fraction)

    train_examples, val_examples = top_examples, []
    if splits_dir:
        train_examples, val_examples = _split_trajectories(top_examples, splits_dir, val_fraction)
    else:
        logger.info("No splits_dir provided, using all %d examples for training (no validation)", len(top_examples))

    # Gold trajectories are conversational (`messages` with structured `tool_calls`).
    # We hand them to TRL as-is and let Qwen's own chat template render them, so the
    # training text is byte-identical to what the served model sees at inference.
    #
    # Loss masking: the shipped template has no `{% generation %}` markers, so we patch
    # them in (see training/chat_template.py) and set `assistant_only_loss=True`. Loss
    # then falls on thoughts + tool calls + final answer only — never on tool
    # observations, which the model must learn to *read*, not to *invent*.
    conversational = bool(train_examples) and "messages" in train_examples[0]

    if conversational:
        apply_training_chat_template(tokenizer)

        # The served agent passes `tools=` to vLLM, which renders a ~3k-token `# Tools`
        # JSON-schema block into the system message. Training without it would teach the
        # student to emit tool calls from a prompt that never declares the tools, then hand
        # it a schema block it has never seen at inference. TRL forwards this column
        # straight to `apply_chat_template(..., tools=...)`.
        tool_definitions = _agent_tool_definitions()
        logger.info("Rendering %d tool definitions into every prompt", len(tool_definitions))

        def _rows(examples: list[dict]) -> list[dict]:
            return [{"messages": ex["messages"], "tools": tool_definitions} for ex in examples]

        dataset = Dataset.from_list(_rows(train_examples))
        eval_dataset = Dataset.from_list(_rows(val_examples)) if val_examples else None
    else:
        def _to_prompt_completion(examples: list[dict]) -> list[dict]:
            """Legacy prompt/completion examples (pre-gold-trajectory format)."""
            formatted = []
            for ex in examples:
                prompt = ex.get("system_prompt", ex.get("prompt", ""))
                if ex.get("patient_info"):
                    prompt += "\n\n" + ex["patient_info"]
                formatted.append({"prompt": prompt, "completion": ex.get("completion", "")})
            return formatted

        dataset = Dataset.from_list(_to_prompt_completion(train_examples))
        eval_dataset = (
            Dataset.from_list(_to_prompt_completion(val_examples)) if val_examples else None
        )

    if eval_dataset is not None:
        logger.info("Eval dataset: %d examples", len(eval_dataset))

    # Pre-flight: report the token-length distribution and how much (if anything) truncates at
    # max_seq_length, so a silently-cut trajectory tail (the final diagnosis) is visible in the
    # log before a multi-hour run rather than discovered after.
    if conversational:
        _log_sequence_stats(dataset, tokenizer, max_seq_length, _agent_tool_definitions())

    # Training config — following SFT best practices:
    # - completion_only_loss=True: only compute loss on completion tokens (not prompt)
    # - cosine scheduler for smoother convergence
    # - weight_decay for regularization (important with 600 examples)
    # - neftune_noise_alpha for embedding noise regularization
    # - eval_strategy with validation set if available
    # Configure eval strategy based on whether we have a validation set
    eval_kwargs = {}
    if eval_dataset is not None:
        eval_kwargs = {
            "eval_strategy": "epoch",
            "per_device_eval_batch_size": 1,
            "eval_accumulation_steps": 8,
            "load_best_model_at_end": True,
            "metric_for_best_model": "eval_loss",
            "greater_is_better": False,
        }

    # Conversational data masks via assistant_only_loss; legacy prompt/completion data
    # masks via completion_only_loss. Setting both is contradictory.
    loss_mask_kwargs = (
        {"assistant_only_loss": True} if conversational else {"completion_only_loss": True}
    )

    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        max_steps=max_steps,  # -1 = ignore; >0 caps steps for a pipeline smoke test
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        learning_rate=learning_rate,
        max_length=max_seq_length,
        bf16=bf16,
        logging_steps=5,  # finer granularity for tmux monitoring (~11 logs/epoch)
        save_strategy="epoch",
        save_total_limit=2,
        save_only_model=True,
        gradient_checkpointing=True,
        warmup_ratio=0.05,
        lr_scheduler_type="cosine",
        weight_decay=0.01,
        max_grad_norm=1.0,
        optim=optim,
        seed=seed,
        neftune_noise_alpha=neftune_alpha,
        # Qwen3.5's vocabulary is 248k, so a full logits tensor at seq=8192 is ~4 GB in
        # bf16 and ~8 GB once cross-entropy upcasts to fp32 — the dominant memory term,
        # and what OOMs a 40 GB card. Liger's fused linear cross-entropy computes the loss
        # in chunks without ever materialising full logits.
        #
        # TRL once dropped `assistant_masks` whenever Liger was on (huggingface/trl#3781),
        # silently training on tool observations. Fixed in this pin, and asserted below —
        # never take it on trust.
        use_liger_kernel=use_liger,
        **loss_mask_kwargs,
        **eval_kwargs,
    )

    callbacks = []
    if eval_dataset is not None and early_stopping_patience > 0:
        from transformers import EarlyStoppingCallback

        callbacks.append(EarlyStoppingCallback(early_stopping_patience=early_stopping_patience))

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        callbacks=callbacks or None,
    )

    if conversational:
        _assert_loss_is_assistant_only(trainer, tokenizer)

    logger.info("Starting SFT training for %d epochs on %d examples", epochs, len(dataset))
    result = trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    _save_run_summary(output_dir, trainer, result, training_args, model_name, len(dataset),
                      len(eval_dataset) if eval_dataset else 0,
                      precision="qlora" if qlora else "bf16")
    logger.info("SFT model saved to %s", output_dir)


# ---------------------------------------------------------------------------
# Stage 2: GRPO with TRL
# ---------------------------------------------------------------------------

def _require_case_ids(raw_data: list[dict]) -> None:
    """Every training example must carry an explicit case_id (no prompt matching)."""
    missing = [i for i, ex in enumerate(raw_data) if not ex.get("case_id")]
    if missing:
        raise ValueError(
            f"{len(missing)} training example(s) have no 'case_id' (first at index "
            f"{missing[0]}). Rewards are looked up by explicit case_id — regenerate "
            "the dataset with format_for_grpo, which emits a case_id column."
        )


def load_training_chat_template() -> str | None:
    """TRL's think-preserving Qwen3.5 TRAINING chat template, or None if unavailable.

    Qwen3.5's shipped template is an INFERENCE template: it strips `<think>` from any assistant
    turn that a user message follows. In a multi-turn rollout that (a) silently deletes the
    policy's own reasoning from its context and (b) makes the render non-append-only, which
    breaks token concatenation. TRL's training variant keeps the reasoning and stays
    append-only through tool and reflection turns.
    """
    try:
        from trl.chat_template_utils import qwen3_5_think_training_chat_template

        return qwen3_5_think_training_chat_template
    except Exception as exc:  # older TRL without Qwen3.5 coverage
        logger.warning("No Qwen3.5 training chat template in this TRL (%s)", exc)
        return None


def export_training_chat_template(path: str | Path) -> Path | None:
    """Write the training chat template to disk for the eval server to load.

    Training and serving MUST render with the same template. If the policy is trained with
    reasoning preserved in history but evaluated with the shipped template that strips it, the
    agent sees a different context at eval than it ever saw while learning — the same class of
    train/serve mismatch that made the first GRPO runs look flat. vLLM takes this file via
    `--chat-template`.
    """
    template = load_training_chat_template()
    if template is None:
        return None
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(template)
    logger.info("Wrote training chat template for serving: %s", out)
    return out


def _stratified_holdout(
    raw_data: list[dict], per_condition: int, seed: int
) -> tuple[list[dict], list[dict]]:
    """Split a per-condition-stratified validation set out of the training data.

    Returns (train_remaining, validation). Deterministic given ``seed``: within each
    condition the cases are sorted by id then shuffled, and the first ``per_condition``
    become validation. Every condition is represented, so the held-out reward is a
    balanced generalisation signal rather than an alphabetical slice.
    """
    import random

    by_cond: dict[str, list[dict]] = {}
    for ex in raw_data:
        by_cond.setdefault(ex.get("condition", "_unknown"), []).append(ex)

    rng = random.Random(seed)
    val_ids: set[str] = set()
    val: list[dict] = []
    for cond in sorted(by_cond):
        items = sorted(by_cond[cond], key=lambda e: e["case_id"])
        rng.shuffle(items)
        for ex in items[:per_condition]:
            val.append(ex)
            val_ids.add(ex["case_id"])
    train = [ex for ex in raw_data if ex["case_id"] not in val_ids]
    return train, val


def _build_online_reward_fn(
    raw_data: list[dict],
    dataset_dir: Path,
    reward_config: str,
    tool_costs_config: str,
    rules_dir: str,
    hospital: str,
):
    """Online reward: score generated completions with the shared CompositeReward.

    Same scorer (CompositeReward → MetricsCalculator) and same weights file
    (config/training/reward_weights.yaml) that evaluation and gold-trajectory
    selection use. Case lookup is by the case_id dataset column, which TRL
    forwards to the reward function as a kwarg.
    """
    from .rewards.composite_reward import CompositeReward
    from .rewards.online_reward import OnlineRewardFunction, load_cases_by_id

    composite = CompositeReward.from_config(
        reward_config_path=reward_config,
        tool_costs_path=tool_costs_config,
        rules_dir=rules_dir,
        hospital=hospital,
    )
    cases = load_cases_by_id(
        dataset_dir, case_ids={ex["case_id"] for ex in raw_data}
    )
    return OnlineRewardFunction(cases=cases, composite=composite)


def _build_offline_reward_fn(raw_data: list[dict], allow_placeholder_rewards: bool):
    """Offline pre-computed rewards, keyed by (case_id, completion text) — never by prefix.

    This path exists only for replay-style debugging: pre-computed rewards cannot
    score the NEW completions an on-policy trainer generates. Worse, gold-mode
    datasets carry style-keyword PLACEHOLDER rewards (reward_source ==
    "style_placeholder") that encode no clinical signal at all. So this is a hard
    error unless --allow-placeholder-rewards is passed explicitly.
    """
    if not allow_placeholder_rewards:
        raise RuntimeError(
            "NeuroBench cases directory not found, so the online CompositeReward "
            "cannot run — and the dataset's pre-computed rewards may be style-keyword "
            "placeholders (format_for_grpo gold mode) that must never be optimised "
            "against. Point NEUROAGENT_DATASET at the dataset, or pass "
            "--allow-placeholder-rewards to proceed anyway (debugging only)."
        )

    sources = {ex.get("reward_source", "unknown") for ex in raw_data}
    if "style_placeholder" in sources:
        logger.warning(
            "Training on STYLE-PLACEHOLDER rewards (--allow-placeholder-rewards). "
            "These encode no clinical signal — do not report results from this run."
        )

    reward_data: dict[tuple[str, str], float] = {}
    for ex in raw_data:
        cid = ex["case_id"]
        if "completions" in ex and "rewards" in ex:
            for comp, rew in zip(ex["completions"], ex["rewards"]):
                if isinstance(comp, str):
                    reward_data[(cid, comp)] = rew
        elif "completion" in ex and "reward" in ex:
            reward_data[(cid, ex["completion"])] = ex["reward"]

    def offline_reward(prompts=None, completions=None, case_id=None, **kwargs) -> list[float]:
        if case_id is None:
            raise ValueError(
                "offline reward requires the 'case_id' dataset column (TRL forwards "
                "extra dataset columns to reward functions as kwargs)."
            )
        rewards = []
        for cid, comp in zip(case_id, completions):
            if not isinstance(comp, str):
                comp = "\n".join(
                    m.get("content", "") for m in comp if isinstance(m, dict)
                )
            key = (cid, comp)
            if key not in reward_data:
                raise KeyError(
                    f"No pre-computed reward for case {cid!r} and this completion — "
                    "offline rewards cannot score newly generated completions. Use "
                    "the online reward (NEUROAGENT_DATASET pointing at the cases dir)."
                )
            rewards.append(reward_data[key])
        return rewards

    offline_reward.__name__ = "offline_precomputed_reward"
    return offline_reward


def _build_multiturn_rollout(
    raw_data: list[dict],
    dataset_dir: Path,
    reward_config: str,
    tool_costs_config: str,
    rules_dir: str,
    hospital: str,
    tokenizer,
    max_completion_length: int,
    per_turn_max_tokens: int,
):
    """Assemble the multi-turn rollout_func and its pass-through reward function.

    Returns ``(rollout_func, reward_func)``. The rollout drives the real ReAct loop against a
    per-case ``MockServer`` and scores the resulting ``AgentTrace`` with the shared
    ``CompositeReward``; the reward is threaded to TRL through the ``trajectory_reward`` field.
    """
    from ..agent.config import load_agent_config
    from ..agent.orchestrator import AgentOrchestrator
    from ..evaluation.runner import format_patient_info
    from ..rules.rules_engine import RulesEngine
    from ..tools.cost_tracker import CostTracker
    from ..tools.mock_server import MockServer
    from ..tools.tool_registry import ToolRegistry
    from .rewards.composite_reward import CompositeReward
    from .rewards.online_reward import load_cases_by_id
    from .rollout.react_rollout import ReactRollout
    from .rollout.trl_rollout import MultiTurnRolloutFunc, precomputed_trajectory_reward

    # System prompt is composed exactly as at serving (base + reasoning style + hospital rules).
    rules = RulesEngine(rules_dir, hospital=hospital)
    orchestrator = AgentOrchestrator(
        config=load_agent_config(hospital=hospital),
        tool_registry=ToolRegistry.create_default_registry(),
        rules_engine=rules,
    )
    system_prompt = orchestrator._build_system_prompt()
    tools = _agent_tool_definitions()

    case_ids = {ex["case_id"] for ex in raw_data}
    cases = load_cases_by_id(dataset_dir, case_ids)
    patient_info = {cid: format_patient_info(case) for cid, case in cases.items()}
    prompt_to_case = {ex["prompt"]: ex["case_id"] for ex in raw_data}

    composite = CompositeReward.from_config(
        reward_config, tool_costs_config, rules_dir, hospital
    )

    # The think-preserving TRAINING chat template. Qwen3.5's shipped (inference) template drops
    # reasoning from any assistant turn a user message follows, which breaks append-only token
    # concatenation and previously forced reflection off; TRL's training template keeps it and
    # stays append-only through tool + reflection turns (both verified empirically). The eval
    # server MUST be given this same template — see export_training_chat_template().
    chat_template = load_training_chat_template()
    reflection_msg = None
    enable_reflection = False
    if chat_template is not None:
        from ..agent.reflection import get_reflection_prompt

        reflection_msg = get_reflection_prompt()
        enable_reflection = bool(load_agent_config(hospital=hospital).enable_reflection)
    else:
        logger.warning(
            "No think-preserving training chat template available — running multi-turn "
            "rollouts with reflection DISABLED, since the shipped template strips <think> "
            "after a user turn and would break token alignment."
        )

    rollout = ReactRollout(
        tokenizer=tokenizer,
        tools=tools,
        system_prompt=system_prompt,
        max_completion_tokens=max_completion_length,
        chat_template=chat_template,
        enable_reflection=enable_reflection,
        reflection_message=reflection_msg,
    )
    rollout_func = MultiTurnRolloutFunc(
        rollout=rollout,
        prompt_to_case=prompt_to_case,
        cases=cases,
        patient_info=patient_info,
        reward_fn=lambda trace, case: composite.compute(trace, case),
        mock_server_factory=lambda case: MockServer(case),
        cost_tracker_factory=CostTracker,
        per_turn_max_tokens=per_turn_max_tokens,
    )
    return rollout_func, precomputed_trajectory_reward()


def _save_rl_run_summary(
    output_dir: str,
    trainer,
    result,
    args,
    model_name: str,
    n_train: int,
    algorithm: str,
    data_path: str,
    seed: int,
    extra_hyperparameters: dict[str, Any] | None = None,
) -> None:
    """RL twin of `_save_run_summary`: persist the recipe beside the checkpoint.

    A checkpoint whose recipe you cannot reconstruct is not a result. Records the
    shared TrainingArguments plus the algorithm-specific knobs (beta/clip/etc.)
    and the full loss curve.
    """
    summary = {
        "algorithm": algorithm,
        "model": model_name,
        "dataset_path": str(data_path),
        "n_train_examples": n_train,
        "hyperparameters": {
            "learning_rate": args.learning_rate,
            "epochs": args.num_train_epochs,
            "per_device_train_batch_size": args.per_device_train_batch_size,
            "gradient_accumulation_steps": args.gradient_accumulation_steps,
            "effective_batch_size": (
                args.per_device_train_batch_size * args.gradient_accumulation_steps
            ),
            "seed": seed,
            "bf16": getattr(args, "bf16", None),
            "gradient_checkpointing": getattr(args, "gradient_checkpointing", None),
            **(extra_hyperparameters or {}),
        },
        "train_runtime_s": result.metrics.get("train_runtime") if result is not None else None,
        "final_train_loss": result.metrics.get("train_loss") if result is not None else None,
        "log_history": trainer.state.log_history,
    }
    path = Path(output_dir) / "run_summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, default=str) + "\n")
    logger.info("Run summary written to %s", path)


def _make_best_reward_callback():
    """Track the best held-out REWARD and which checkpoint produced it.

    HF's `load_best_model_at_end` cannot be used here: TRL *logs* `eval_reward` but does not
    return it in the metrics dict, so `metric_for_best_model="eval_reward"` raises KeyError,
    and the only metric on offer is `eval_loss` — which for GRPO is a policy-gradient
    surrogate, not a measure of quality (it drifts toward 0 as the policy stops changing).
    Selecting on it would be worse than selecting on nothing.

    So we watch the logs, remember the step with the highest held-out reward, and the caller
    promotes that checkpoint to the output root — the same "root adapter == best checkpoint"
    contract the SFT stage has.
    """
    from transformers import TrainerCallback

    class _BestRewardCallback(TrainerCallback):
        best_reward: float | None = None
        best_step: int | None = None

        def on_log(self, args, state, control, logs=None, **kwargs):
            if not logs or "eval_reward" not in logs:
                return
            reward = float(logs["eval_reward"])
            if self.best_reward is None or reward > self.best_reward:
                self.best_reward, self.best_step = reward, int(state.global_step)
                logger.info(
                    "New best held-out reward %.4f at step %d", reward, self.best_step
                )

    return _BestRewardCallback()


def _promote_best_checkpoint(output_dir: str, best_step: int | None) -> None:
    """Copy the best-reward checkpoint's adapter into the output root.

    Downstream (serving, eval) reads `<output>/adapter_model.safetensors`, so the root must
    hold the checkpoint we actually want — otherwise the run silently ships its LAST step,
    which for RL is often past the point where held-out reward peaked.
    """
    import shutil

    # These two failures ship a post-peak adapter while looking like success, so they must
    # surface on the terminal (ERROR), not only in the log file (the split-logging setup
    # routes WARNING to the file alone).
    if best_step is None:
        logger.error("No held-out eval ran — the root adapter is the LAST step, not the best.")
        return
    ckpt = Path(output_dir) / f"checkpoint-{best_step}"
    adapter = ckpt / "adapter_model.safetensors"
    if not adapter.exists():
        logger.error("Best step %d has no checkpoint at %s — keeping the last step.", best_step, ckpt)
        return
    for name in ("adapter_model.safetensors", "adapter_config.json"):
        src = ckpt / name
        if src.exists():
            shutil.copy2(src, Path(output_dir) / name)
    logger.info("Promoted checkpoint-%d (best held-out reward) to the output root", best_step)


def _make_generation_cache_callback(model):
    """Callback that keeps the KV cache enabled for GRPO's generation phase.

    HF's Trainer sets `model.config.use_cache = False` whenever gradient checkpointing is
    on. That is right for the training forward — but GRPO *generates* with the same model,
    and without a cache `generate()` cannot take the `logits_to_keep=1` shortcut: it
    materialises logits for EVERY prompt position. At a 6.2k-token prompt and Qwen3.5's
    248k vocab that is 4 x 6.2k x 248k = 12.2 GB (bf16) of logits per generation batch —
    for a tensor whose last row is the only one generate() reads.

    Flipping use_cache back on after Trainer's setup gives generation its cache; the
    checkpointed training forward still disables the cache locally (transformers does that
    per-forward, without mutating the config), so gradient checkpointing keeps working.

    Defined here rather than at module scope because transformers is imported lazily — the
    module must stay importable without torch installed.
    """
    from transformers import TrainerCallback

    class _GenerationCacheCallback(TrainerCallback):
        def _enable(self):
            cfg = getattr(model, "config", None)
            if cfg is not None:
                cfg.use_cache = True
            # PeftModel wraps the base; its inner config is the one generate() reads.
            inner = getattr(getattr(model, "base_model", None), "model", None)
            if inner is not None and getattr(inner, "config", None) is not None:
                inner.config.use_cache = True

        def on_train_begin(self, args, state, control, **kwargs):
            self._enable()

        def on_step_begin(self, args, state, control, **kwargs):
            self._enable()

    return _GenerationCacheCallback()


def run_grpo_trl(
    model_name: str,
    data_path: str,
    output_dir: str,
    base_model: str | None = None,
    lora_rank: int = 64,
    lora_alpha: int = 128,
    epochs: int = 15,
    batch_size: int = 4,
    learning_rate: float = 3e-6,
    num_generations: int = 8,
    max_completion_length: int = 4096,
    temperature: float = 1.0,
    kl_coeff: float = 0.001,
    bf16: bool = True,
    use_vllm: bool = False,
    vllm_gpu_memory_utilization: float = 0.30,
    vllm_max_model_length: int = 16384,
    qlora: bool = False,
    seed: int = 42,
    reward_config: str = "config/training/reward_weights.yaml",
    tool_costs_config: str = "config/tools/costs.yaml",
    rules_dir: str = "config/hospital_rules",
    hospital: str = "de_charite",
    allow_placeholder_rewards: bool = False,
    grad_accum: int = 4,
    generation_batch_size: int | None = None,
    max_steps: int = -1,
    logging_steps: int = 1,
    save_steps: int = 50,
    eval_data: str | None = None,
    eval_subset: int = 20,
    eval_steps: int = 40,
    num_generations_eval: int | None = None,
    importance_sampling_level: str = "sequence",
    scale_rewards: str = "none",
    loss_type: str = "dapo",
    epsilon_high: float = 0.28,
    mask_truncated_completions: bool = True,
    val_from_train: bool = True,
    val_per_condition: int = 1,
    multi_turn: bool = False,
    per_turn_max_tokens: int = 2048,
) -> None:
    """Run GRPO training using TRL GRPOTrainer.

    Note on prompt length: TRL 0.29 removed `max_prompt_length` from GRPOConfig
    (prompts are no longer truncated by the trainer), so this function no longer
    accepts one. With vLLM generation, size the context via `vllm_max_model_length`.

    Args:
        model_name: Model name or PEFT adapter checkpoint path.
        base_model: If model_name is an adapter, this is the base model name.
            Auto-detected from adapter_config.json if not specified.
        kl_coeff: KL coefficient, forwarded to GRPOConfig's `beta` field.
        seed: Random seed forwarded to GRPOConfig (mirrors the SFT stage).
    """
    import torch
    _quiet_torch_loggers()
    from datasets import Dataset
    from peft import PeftModel, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import GRPOConfig

    # Qwen3.5's 248,320-token vocabulary makes TRL's full logits tensor
    # (batch x seq x vocab) the largest allocation in the run — it is what OOM'd the
    # backward pass. This subclass swaps ONLY the logprob computation for Unsloth's chunked
    # kernel; everything else (generation, advantages, loss, our rollout_func) is stock TRL.
    # Validated on the real model: bit-exact vs an fp32 reference (TRL's own bf16 path is off
    # by 6e-2), at 2.5-4.4x less memory. See training/chunked_logps.py.
    from .chunked_grpo_trainer import ChunkedLogpsGRPOTrainer

    # Detect if model_name is a PEFT adapter checkpoint
    adapter_path = None
    model_path = Path(model_name)
    if model_path.exists() and (model_path / "adapter_config.json").exists():
        adapter_path = str(model_path)
        if base_model is None:
            import json
            adapter_cfg = json.loads((model_path / "adapter_config.json").read_text())
            base_model = adapter_cfg.get("base_model_name_or_path", "Qwen/Qwen3.5-9B")
        logger.info("Detected PEFT adapter at %s, base model: %s", adapter_path, base_model)
        model_name = base_model

    logger.info("Loading model: %s (qlora=%s)", model_name, qlora)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    load_kwargs: dict = {
        "device_map": "auto",
        "trust_remote_code": True,
    }
    if qlora:
        load_kwargs["quantization_config"] = get_quantization_config()
    else:
        load_kwargs["dtype"] = torch.bfloat16 if bf16 else torch.float16

    model = AutoModelForCausalLM.from_pretrained(model_name, **load_kwargs)

    if qlora:
        model = prepare_model_for_kbit_training(model)
        # prepare_model_for_kbit_training upcasts EVERY non-quantized parameter to fp32 for
        # numerical stability — a habit from fp16, where the narrow exponent range made fp32
        # norms necessary. On Qwen3.5 it is ruinous: the 248k-vocab embedding and lm_head are
        # ~1B params each, so the upcast costs ~3.8 GB of frozen weights and doubles every
        # logits tensor computed from that fp32 head. bf16 has fp32's exponent range, so the
        # stability argument does not apply here. Put everything back to bf16 — and it must be
        # everything, not just the head, or the fp32 norms feed a bf16 head and the forward
        # dies with "expected scalar type BFloat16 but found Float".
        compute_dtype = torch.bfloat16 if bf16 else torch.float16
        upcast = [n for n, p in model.named_parameters() if p.dtype == torch.float32]
        for _, p in model.named_parameters():
            if p.dtype == torch.float32:
                p.data = p.data.to(compute_dtype)
        logger.info(
            "Cast %d fp32 params (incl. the 248k-vocab embed/lm_head) back to %s",
            len(upcast), compute_dtype,
        )

    # Load existing adapter (SFT checkpoint) or create fresh LoRA
    if adapter_path:
        logger.info("Loading SFT adapter from %s", adapter_path)
        model = PeftModel.from_pretrained(model, adapter_path, is_trainable=True)
    else:
        lora_config = get_lora_config(rank=lora_rank, alpha=lora_alpha)
        model = get_peft_model(model, lora_config)
    # peft's print_trainable_parameters() writes to stdout and would litter the terminal; log
    # the same numbers to the file instead.
    _trainable, _all = model.get_nb_trainable_parameters()
    logger.info("Trainable params: %d / %d (%.2f%%)", _trainable, _all, 100 * _trainable / _all)
    # The bf16 cast above touches only FROZEN base weights. The trainable LoRA params must
    # stay fp32 (peft's autocast_adapter_dtype default) — optimising bf16 master weights at
    # a 3e-6 LR would lose most updates to rounding.
    trainable_dtypes = {p.dtype for p in model.parameters() if p.requires_grad}
    logger.info("Trainable param dtypes: %s", trainable_dtypes)
    if trainable_dtypes and trainable_dtypes != {torch.float32}:
        logger.warning(
            "Trainable params are %s, not fp32 — at lr=%g updates will round away.",
            trainable_dtypes, learning_rate,
        )

    # Load data — format as prompts for GRPO
    raw_data = load_grpo_data(data_path)
    _require_case_ids(raw_data)

    # Held-out validation is carved from the TRAIN split, stratified by condition. The old
    # path validated on the first `eval_subset` cases of the reported TEST split — that both
    # leaks the report set into model selection and (being an alphabetical head) covers only
    # ~9 of 20 conditions. Carving from train fixes both; the test split is touched only by
    # the final eval, never during training.
    held_out_val: list[dict] = []
    if val_from_train and val_per_condition > 0:
        raw_data, held_out_val = _stratified_holdout(raw_data, val_per_condition, seed)
        logger.info(
            "Held-out val carved from train: %d cases across %d conditions; %d cases remain for training",
            len(held_out_val),
            len({e.get("condition") for e in held_out_val}),
            len(raw_data),
        )

    # GRPO expects a "prompt" field; the trainer generates completions and scores
    # them with reward_funcs. `case_id` is kept as an extra dataset column —
    # GRPOConfig.remove_unused_columns defaults to False, so TRL forwards it to
    # the reward function as a kwarg for explicit, collision-free case lookup.
    #
    # build_grpo_dataset.py already renders the prompt to TEXT through the tokenizer's
    # chat template, with the system prompt and the serving tool schemas baked in. TRL
    # leaves a string prompt alone (a "standard" dataset), so it reaches the model exactly
    # as written. Wrapping it back into [{"role": "user", ...}] would make the dataset
    # conversational, TRL would apply the chat template a SECOND time, and the system
    # prompt + tools block would be lost — the policy would train without ever being told
    # which tools exist.
    formatted = []
    for ex in raw_data:
        prompt = ex.get("prompt", "")
        if not isinstance(prompt, str) or not prompt:
            raise ValueError(
                f"case {ex.get('case_id')!r}: 'prompt' must be the pre-rendered prompt "
                "string from build_grpo_dataset.py (got "
                f"{type(prompt).__name__}). Rebuild the dataset with "
                "`python -m neuroagent.training.data.build_grpo_dataset`."
            )
        formatted.append({"prompt": prompt, "case_id": ex["case_id"]})

    dataset = Dataset.from_list(formatted)

    # Held-out validation, mirroring the SFT stage. GRPO has no eval_loss to track — the
    # honest analogue is the mean reward on cases the policy never trains on, so a rising
    # train reward that does not generalise is visible instead of silently accepted.
    # Evaluation GENERATES (num_generations completions per prompt), so it is as expensive
    # per prompt as training: eval_subset caps how many of the held-out prompts are used.
    eval_dataset = None
    eval_raw: list[dict] = []
    if held_out_val:
        eval_raw = held_out_val
        eval_dataset = Dataset.from_list(
            [{"prompt": ex["prompt"], "case_id": ex["case_id"]} for ex in eval_raw]
        )
        logger.info(
            "Held-out validation: %d train-carved prompts, every %d steps",
            len(eval_dataset), eval_steps,
        )
    elif eval_data:
        # Legacy path: validate on an explicit file. Kept for compatibility, but it risks
        # test-set leakage into checkpoint selection — prefer val_from_train (the default).
        logger.warning(
            "Validating on explicit --eval-data (%s); this can leak the report set into "
            "model selection. Prefer --val-from-train.", eval_data,
        )
        eval_raw = load_grpo_data(eval_data)
        _require_case_ids(eval_raw)
        eval_raw = eval_raw[:eval_subset]
        eval_dataset = Dataset.from_list(
            [{"prompt": ex["prompt"], "case_id": ex["case_id"]} for ex in eval_raw]
        )

    # Build reward function — online CompositeReward scoring if the cases exist.
    dataset_path_env = os.environ.get("NEUROAGENT_DATASET", "data/neurobench")
    dataset_dir = Path(dataset_path_env)

    if use_vllm:
        # vLLM instantiates Qwen3.5 as the MULTIMODAL Qwen3_5ForConditionalGeneration, whose
        # parameters are language_model.model.* plus a visual.* tower, while we train the
        # text-only Qwen3_5ForCausalLM (model.*). Without this, TRL's weight sync raises
        # "no module or parameter named 'model'" the first time it pushes weights.
        from .vllm_qwen35_patch import patch_vllm_language_model_only

        patch_vllm_language_model_only()

    rollout_func = None
    if multi_turn:
        # Multi-turn ("grouped") GRPO: TRL calls our rollout_func, which drives the REAL
        # ReAct loop against the deterministic MockServer and scores the genuine AgentTrace.
        # The reward is computed inside the rollout and read back by a pass-through reward fn.
        if not (dataset_dir / "cases").exists():
            raise FileNotFoundError(
                f"Multi-turn GRPO needs the NeuroBench cases at {dataset_dir}/cases to serve "
                "tool outputs and score trajectories."
            )
        logger.info("Using MULTI-TURN rollout (real ReAct loop, trajectory reward from %s)",
                    reward_config)
        # The per-turn cap is the SINGLE assistant turn budget (measured ~300-400 tok for the
        # SFT policy), not the whole multi-turn completion budget — see
        # MultiTurnRolloutFunc._make_generate_batch_fn. Configurable because setting it too low
        # fails quietly: a turn cut mid-<think> carries no parseable tool call, so the rollout
        # reads it as the agent concluding, and the trajectory is scored as if it chose to stop
        # without ordering tests. The rollout counts such turns and warns.
        rollout_func, reward_func = _build_multiturn_rollout(
            raw_data + eval_raw, dataset_dir, reward_config, tool_costs_config, rules_dir,
            hospital, tokenizer, max_completion_length,
            per_turn_max_tokens=per_turn_max_tokens,
        )
    elif (dataset_dir / "cases").exists():
        logger.info("Using ONLINE reward (CompositeReward, weights from %s)", reward_config)
        # The reward function must be able to look up EVERY case it will be asked to score —
        # train and held-out alike, or validation raises KeyError on the first eval step.
        reward_func = _build_online_reward_fn(
            raw_data + eval_raw, dataset_dir, reward_config, tool_costs_config, rules_dir, hospital
        )
    else:
        reward_func = _build_offline_reward_fn(raw_data, allow_placeholder_rewards)
        logger.info("Using OFFLINE pre-computed rewards (dataset not found at %s)", dataset_dir)

    # GRPO config — TRL v0.29+ API.
    #
    # TRL requires generation_batch_size to be divisible by num_generations: a prompt's
    # G completions form one reward group, and the advantage is that group's mean-centred
    # reward, so a group may never be split across generation batches. We generate exactly
    # `grad_accum` prompts' worth of groups per optimiser step.
    if generation_batch_size is None:
        generation_batch_size = batch_size * grad_accum
    if generation_batch_size % num_generations != 0:
        raise ValueError(
            f"generation_batch_size ({generation_batch_size}) must be divisible by "
            f"num_generations ({num_generations}) — a reward group cannot be split "
            "across generation batches."
        )
    # Saving must land on the eval cadence, so every evaluated step has a checkpoint to
    # promote. Keep them all: with a rotation limit the best one can be deleted before the
    # run ends.
    save_total_limit = 3
    if eval_dataset is not None:
        save_steps = eval_steps
        save_total_limit = None

    training_args = GRPOConfig(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,
        learning_rate=learning_rate,
        num_generations=num_generations,
        # Held-out eval generates too, and TRL defaults this to num_generations — so an eval
        # costs (eval prompts x num_generations) full rollouts. Measured on the 4B: 18 prompts
        # x 4 = 72 rollouts, ~22 min, and that was with one-turn trajectories; a policy that
        # actually runs the ReAct loop multiplies it by the turn count. Over a full run that is
        # hours spent on a number used only to rank checkpoints.
        #
        # Left at TRL's default (None -> num_generations) because the eval reward IS the
        # checkpoint-selection metric and averaging G samples per prompt is what keeps it stable
        # enough to rank on. Lower it when eval time dominates, accepting a noisier ranking.
        num_generations_eval=num_generations_eval,
        generation_batch_size=generation_batch_size,
        max_completion_length=max_completion_length,
        beta=kl_coeff,  # TRL 0.29 name for the KL coefficient (0 = no KL, the recommended default)
        # GSPO: score the importance ratio at the SEQUENCE level, not per token. Our reward is
        # one scalar per rollout, so a sequence-level ratio is the matched, lower-variance
        # objective — Qwen3 itself was trained this way (arXiv 2507.18071).
        importance_sampling_level=importance_sampling_level,
        # Do NOT divide the advantage by the group's reward std. With a small group (G=8) that
        # std is a noisy per-case-difficulty estimate that injects bias (Dr. GRPO); centring on
        # the group mean without rescaling is more stable here.
        scale_rewards=scale_rewards,
        # "dapo": token-level loss normalised over active tokens in the batch — avoids the
        # length bias of the old "grpo" loss.
        loss_type=loss_type,
        seed=seed,
        bf16=bf16,
        logging_steps=logging_steps,
        save_steps=save_steps,
        save_total_limit=save_total_limit,
        max_steps=max_steps,
        # Track the held-out reward and keep the checkpoint that maximises it. GRPO can
        # over-optimise the reward on the training prompts (reward hacking) while the
        # held-out reward flattens or falls; without this the run would just save the last
        # step. greater_is_better=True because this is a reward, not a loss.
        **(
            {
                "eval_strategy": "steps",
                "eval_steps": eval_steps,
                "per_device_eval_batch_size": num_generations,
                # Best-checkpoint selection is done by _BestRewardCallback on eval_reward,
                # not by load_best_model_at_end on eval_loss — see the callback's docstring.
                "save_strategy": "steps",
            }
            if eval_dataset is not None
            else {}
        ),
        gradient_checkpointing=True,
        # (save_steps is set above; with eval on it is forced to eval_steps so that
        # load_best_model_at_end has a checkpoint at every evaluated step.)
        # use_reentrant=False is the supported checkpointing path: the reentrant one silently
        # drops grads for inputs that do not require grad, which is exactly the LoRA case.
        gradient_checkpointing_kwargs={"use_reentrant": False},
        # Generation is the memory peak: G completions are decoded with a KV cache before
        # any backward pass. See _GenerationCacheCallback — the config flag alone is not
        # enough, because Trainer turns it back off for gradient checkpointing.
        use_cache=True,
        # Only the LoRA params are trained, but AdamW still keeps fp32 moments for each:
        # 8-bit states cut that ~4x for free.
        optim="adamw_8bit",
        # Frees the generation KV cache before the training forward allocates its logits,
        # so the two peaks do not stack.
        torch_empty_cache_steps=1,
        # ONE temperature for both sampling and the importance-sampling logprobs. Setting only
        # generation_kwargs samples at `temperature` but scores the ratio at args.temperature
        # (default 1.0), a silent gradient bug for any temperature != 1.0. GRPOConfig.temperature
        # drives both, so leave generation_kwargs without a temperature override.
        temperature=temperature,
        # Clip-higher (DAPO): an asymmetric upper clip lets low-probability-but-good tokens gain
        # probability without the symmetric bound collapsing entropy. epsilon stays 0.2.
        epsilon_high=epsilon_high,
        # Single-turn: do not learn from completions truncated at max_completion_length (no
        # EOS) — their reward is computed on an unfinished trajectory, so the gradient is noise.
        # Multi-turn is the opposite case and must NOT mask: the trajectory is complete (every
        # tool ran, the trace is whole, the reward is valid) — only the token stream is clipped
        # at the budget. Masking those would throw away most of the batch, since long multi-turn
        # trajectories routinely exceed the budget. This is truncated-BPTT, not off-policy noise.
        mask_truncated_completions=(mask_truncated_completions and not multi_turn),
        # vLLM-accelerated rollouts. Colocate is the ONLY single-GPU mode — server mode refuses
        # to share a device — so the engine and the trainer split this card:
        # vllm_gpu_memory_utilization is the engine's share, the rest is left for training.
        # The win is prefix caching: HF generate re-prefills the shared ~6.2k prompt for every
        # generation of every turn (~20x per group); vLLM caches it.
        **(
            {
                "use_vllm": True,
                "vllm_mode": "colocate",
                "vllm_gpu_memory_utilization": vllm_gpu_memory_utilization,
                # Qwen3.5 advertises a 262144-token context, and vLLM sizes its KV cache for
                # the model's max length by default — 8.06 GiB, more than the engine's whole
                # share of the card, so the engine refuses to start. A multi-turn trajectory
                # needs prompt (~6.2k) + completion, nothing like 262k, so cap it there.
                "vllm_max_model_length": vllm_max_model_length,
            }
            if use_vllm
            else {}
        ),
        # Multi-turn rollouts are fully on-policy (the custom rollout_func generates with the
        # live model): one optimiser update per generation, so the importance ratio is 1 and
        # no stored sampling logprobs are needed.
        **({"num_iterations": 1} if multi_turn else {}),
        report_to=[],
        # Our Rich callback (_make_terminal_progress_callback) is the training UI; TRL's own
        # tqdm bar would fight it for the terminal.
        disable_tqdm=True,
    )

    trainer = ChunkedLogpsGRPOTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        reward_funcs=reward_func,
        # Multi-turn: our rollout drives the real ReAct loop and returns a masked, token-exact
        # trajectory + the trajectory reward. None → TRL's built-in single-shot generation.
        rollout_func=rollout_func,
    )
    # With disable_tqdm=True, transformers installs a PrinterCallback that print()s the full
    # 50-key metric dict straight to the terminal (bypassing logging). Remove it — our Rich
    # callback renders the concise line and logs the full dict to the file instead.
    try:
        from transformers.trainer_callback import PrinterCallback, ProgressCallback

        trainer.remove_callback(PrinterCallback)
        trainer.remove_callback(ProgressCallback)
    except Exception:  # class names/layout changed — the Rich bar still renders regardless
        pass
    trainer.add_callback(_make_generation_cache_callback(model))
    trainer.add_callback(_make_terminal_progress_callback(Path(output_dir).name or "GRPO"))
    best_reward_cb = _make_best_reward_callback()
    if eval_dataset is not None:
        trainer.add_callback(best_reward_cb)

    logger.info("Starting GRPO training for %d epochs (seed=%d, beta=%g)", epochs, seed, kl_coeff)
    torch.cuda.reset_peak_memory_stats()
    result = trainer.train()

    # Peak ALLOCATED bytes, not nvidia-smi / reserved: a paged optimizer inflates the
    # reserved figure well above what the run actually needs, which is what made the
    # earlier bf16-vs-QLoRA comparison come out backwards.
    peak_gb = torch.cuda.max_memory_allocated() / 1024**3
    total_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
    logger.info("PEAK GPU MEMORY: %.1f GB allocated of %.1f GB (%.0f%%)",
                peak_gb, total_gb, 100 * peak_gb / total_gb)

    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    # Ship the checkpoint with the best HELD-OUT reward, not the last step.
    if eval_dataset is not None:
        _promote_best_checkpoint(output_dir, best_reward_cb.best_step)
    _save_rl_run_summary(
        output_dir, trainer, result, training_args, model_name,
        n_train=len(dataset), algorithm="grpo", data_path=data_path, seed=seed,
        extra_hyperparameters={
            "beta_kl_coeff": kl_coeff,
            "num_generations": num_generations,
            "max_completion_length": max_completion_length,
            "generation_temperature": temperature,
            "lora_rank": lora_rank,
            "lora_alpha": lora_alpha,
            "qlora": qlora,
            "precision": "qlora" if qlora else ("bf16" if bf16 else "fp16"),
            "adapter_init": adapter_path,
            "peak_gpu_memory_gb": round(peak_gb, 2),
            "best_eval_reward": best_reward_cb.best_reward,
            "best_eval_step": best_reward_cb.best_step,
            "eval_data": eval_data,
        },
    )
    logger.info("GRPO model saved to %s", output_dir)


# ---------------------------------------------------------------------------
# veRL backend (multi-GPU)
# ---------------------------------------------------------------------------

def generate_verl_script(
    model_name: str,
    data_path: str,
    output_dir: str,
    n_gpus: int = 4,
    lora_rank: int = 64,
    lora_alpha: int = 32,
    epochs: int = 15,
    batch_size: int = 512,
    rollout_n: int = 8,
    learning_rate: float = 3e-6,
    kl_coeff: float = 0.001,
) -> str:
    """Generate a veRL training bash script.

    veRL is configured via CLI args, so we generate a runnable script
    rather than calling Python APIs directly.
    """
    script = f"""#!/bin/bash
# veRL GRPO + LoRA training script for NeuroAgent
# Generated by neuroagent.training.train_grpo
set -x

export PYTHONUNBUFFERED=1
export CUDA_DEVICE_ORDER="PCI_BUS_ID"

python3 -m verl.trainer.main_ppo \\
    \\
    # === ALGORITHM === \\
    algorithm.adv_estimator=grpo \\
    algorithm.use_kl_in_reward=False \\
    \\
    # === DATA === \\
    data.train_files={data_path} \\
    data.train_batch_size={batch_size} \\
    data.max_prompt_length=2048 \\
    data.max_response_length=4096 \\
    data.filter_overlong_prompts=True \\
    data.truncation=error \\
    \\
    # === MODEL === \\
    actor_rollout_ref.model.path={model_name} \\
    actor_rollout_ref.model.lora_rank={lora_rank} \\
    actor_rollout_ref.model.lora_alpha={lora_alpha} \\
    actor_rollout_ref.model.use_remove_padding=True \\
    actor_rollout_ref.model.enable_gradient_checkpointing=True \\
    \\
    # === ACTOR === \\
    actor_rollout_ref.actor.optim.lr={learning_rate} \\
    actor_rollout_ref.actor.ppo_mini_batch_size=256 \\
    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=20 \\
    actor_rollout_ref.actor.use_kl_loss=True \\
    actor_rollout_ref.actor.kl_loss_coef={kl_coeff} \\
    actor_rollout_ref.actor.kl_loss_type=low_var_kl \\
    actor_rollout_ref.actor.entropy_coeff=0 \\
    actor_rollout_ref.actor.fsdp_config.param_offload=False \\
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=False \\
    \\
    # === ROLLOUT (vLLM) === \\
    actor_rollout_ref.rollout.name=vllm \\
    actor_rollout_ref.rollout.tensor_model_parallel_size=1 \\
    actor_rollout_ref.rollout.n={rollout_n} \\
    actor_rollout_ref.rollout.gpu_memory_utilization=0.7 \\
    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=20 \\
    actor_rollout_ref.rollout.load_format=safetensors \\
    \\
    # === REFERENCE MODEL === \\
    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=20 \\
    actor_rollout_ref.ref.fsdp_config.param_offload=True \\
    \\
    # === TRAINER === \\
    trainer.critic_warmup=0 \\
    trainer.val_before_train=False \\
    trainer.n_gpus_per_node={n_gpus} \\
    trainer.nnodes=1 \\
    trainer.total_epochs={epochs} \\
    trainer.save_freq=50 \\
    trainer.save_total_limit=3 \\
    trainer.test_freq=5 \\
    \\
    # === LOGGING === \\
    trainer.logger='["console","wandb"]' \\
    trainer.project_name=neuroagent_grpo \\
    trainer.experiment_name=neuroagent_{model_name.split("/")[-1]}_grpo_lora \\
    \\
    "$@"
"""
    # Save script
    output_path = Path(output_dir) / "run_verl_grpo.sh"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(script)
    output_path.chmod(0o755)
    logger.info("Generated veRL script: %s", output_path)
    return str(output_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="NeuroAgent GRPO training")
    parser.add_argument("--stage", choices=["sft", "grpo"], required=True)
    parser.add_argument("--backend", choices=["trl", "verl"], default="trl")
    parser.add_argument("--model", required=True, help="Model name or PEFT adapter checkpoint path")
    parser.add_argument("--base-model", default=None, help="Base model name (auto-detected from adapter if not set)")
    parser.add_argument("--data", required=True, help="Training data path")
    parser.add_argument("--output", required=True, help="Output directory")

    # LoRA
    parser.add_argument("--lora-rank", type=int, default=64)
    parser.add_argument("--lora-alpha", type=int, default=128)

    # Training
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--num-generations", type=int, default=8)
    parser.add_argument("--max-completion-length", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--kl-coeff", type=float, default=0.001)
    parser.add_argument("--use-vllm", action="store_true")
    parser.add_argument("--top-fraction", type=float, default=1.0,
                        help="Fraction of top trajectories for SFT (1.0 = use all, 0.1 = top 10%%)")
    parser.add_argument("--qlora", action="store_true", help="Use QLoRA (4-bit NF4 quantization)")
    parser.add_argument("--splits-dir", default=None, help="Split dir with train_cases.txt / test_cases.txt (e.g., data/neurobench/splits/)")
    parser.add_argument("--grad-accum", type=int, default=16,
                        help="Gradient accumulation steps. effective batch = batch-size * this")
    parser.add_argument("--optim", default="paged_adamw_8bit",
                        help="paged_adamw_8bit (9B, pages optimizer state on VRAM spikes) "
                             "or adamw_8bit (4B, has headroom)")
    parser.add_argument("--neftune-alpha", type=float, default=None,
                        help="NEFTune embedding noise. Off by default: it degrades tool-argument "
                             "fidelity. The original paper's value is 5.0")
    parser.add_argument("--early-stopping-patience", type=int, default=1,
                        help="Stop after N evals without eval_loss improvement. 0 disables")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-steps", type=int, default=-1,
                        help="Cap training steps for an end-to-end smoke test. -1 runs full epochs")
    parser.add_argument("--val-fraction", type=float, default=0.1,
                        help="Fraction of train cases carved out for validation")
    parser.add_argument("--max-seq-length", type=int, default=8192,
                        help="Max sequence length; set from scripts/training/probe_max_seq_length.py")
    parser.add_argument("--no-liger", dest="use_liger", action="store_false", default=True,
                        help="Disable Liger fused cross-entropy (needed on 248k-vocab Qwen3.5)")
    parser.add_argument("--bf16", action="store_true", default=True)

    # Reward (for online GRPO)
    parser.add_argument("--reward-config", default="config/training/reward_weights.yaml")
    parser.add_argument("--tool-costs", default="config/tools/costs.yaml")
    parser.add_argument("--rules-dir", default="config/hospital_rules")
    parser.add_argument("--hospital", default="us_mayo")
    parser.add_argument(
        "--allow-placeholder-rewards", action="store_true",
        help="Permit offline pre-computed rewards when the cases dir is absent. "
             "Those rewards may be style-keyword placeholders with no clinical "
             "signal — debugging only, never for reportable runs.",
    )

    # GRPO batching / logging
    parser.add_argument("--generation-batch-size", type=int, default=None,
                        help="Completions generated per optimiser step. Must be divisible by "
                             "--num-generations. Defaults to batch-size * grad-accum")
    parser.add_argument("--logging-steps", type=int, default=1,
                        help="GRPO steps are slow and few — log every one by default")
    parser.add_argument("--save-steps", type=int, default=50)
    parser.add_argument("--eval-data", default=None,
                        help="Held-out prompts (test split) for validation reward + best-checkpoint "
                             "selection. GRPO has no eval_loss; the metric is mean held-out reward")
    parser.add_argument("--eval-subset", type=int, default=20,
                        help="How many held-out prompts to score per eval. Evaluation generates, so "
                             "it costs the same per prompt as training — 20 keeps it to a few minutes")
    parser.add_argument("--eval-steps", type=int, default=40,
                        help="Evaluate (and checkpoint) every N optimiser steps")
    parser.add_argument("--num-generations-eval", type=int, default=None,
                        help="Completions per prompt during held-out eval (default: same as "
                             "--num-generations). An eval costs eval_prompts x this many full "
                             "rollouts — measured 72 rollouts / ~22 min on the 4B at 4, before "
                             "multiplying by the ReAct turn count. Lower it when eval time "
                             "dominates, at the cost of a noisier checkpoint ranking.")
    parser.add_argument("--importance-sampling-level", choices=["token", "sequence"],
                        default="sequence",
                        help="GSPO: 'sequence' matches our one-reward-per-rollout objective")
    parser.add_argument("--scale-rewards", choices=["none", "group", "batch"], default="none",
                        help="'none' = do not divide the advantage by the group reward std (Dr. GRPO)")
    parser.add_argument("--loss-type", default="dapo",
                        help="GRPO loss normalisation (dapo = token-level, no length bias)")
    parser.add_argument("--vllm-gpu-memory-utilization", type=float, default=0.30,
                        help="Share of the GPU reserved for the colocated vLLM engine; the "
                             "remainder is left for training. Only used with --use-vllm.")
    parser.add_argument("--vllm-max-model-length", type=int, default=16384,
                        help="Context the colocated vLLM engine sizes its KV cache for. Qwen3.5 "
                             "advertises 262144, which alone exceeds the engine's memory share; "
                             "a trajectory needs ~6.2k prompt + the completion budget.")
    parser.add_argument("--multi-turn", action="store_true",
                        help="Multi-turn ('grouped') GRPO: drive the real ReAct loop against "
                             "the MockServer and score the genuine trajectory.")
    parser.add_argument("--per-turn-max-tokens", type=int, default=2048,
                        help="Token cap for ONE assistant turn during a multi-turn rollout. Was "
                             "512, chosen from a ~300-400 token AVERAGE, which produced ZERO "
                             "tool calls on every rollout: Qwen3.5 writes a long <think> before "
                             "its first call, and a turn cut mid-reasoning carries no parseable "
                             "tool call, so the rollout reads it as the agent concluding. "
                             "Measured at 4096: 3.0-6.2 turns and 1.0-3.8 tool calls on the same "
                             "model that produced 1.0/0.0 at 512.")

    parser.add_argument("--log-file", default=None,
                        help="Verbose logs + captured warnings go HERE; the terminal keeps the "
                             "progress bar and a concise per-step reward line")

    # veRL-specific
    parser.add_argument("--n-gpus", type=int, default=4)

    args = parser.parse_args()
    _configure_split_logging(args.log_file)

    if args.stage == "sft":
        epochs = args.epochs or 3
        lr = args.lr or 1.5e-4
        run_sft(
            model_name=args.model,
            data_path=args.data,
            output_dir=args.output,
            lora_rank=args.lora_rank,
            lora_alpha=args.lora_alpha,
            epochs=epochs,
            batch_size=args.batch_size,
            learning_rate=lr,
            bf16=args.bf16,
            qlora=args.qlora,
            top_fraction=args.top_fraction,
            splits_dir=args.splits_dir,
            val_fraction=args.val_fraction,
            max_seq_length=args.max_seq_length,
            use_liger=args.use_liger,
            grad_accum=args.grad_accum,
            optim=args.optim,
            neftune_alpha=args.neftune_alpha,
            early_stopping_patience=args.early_stopping_patience,
            seed=args.seed,
            max_steps=args.max_steps,
        )

    elif args.stage == "grpo":
        epochs = args.epochs or 15
        lr = args.lr or 3e-6

        if args.backend == "verl":
            generate_verl_script(
                model_name=args.model,
                data_path=args.data,
                output_dir=args.output,
                n_gpus=args.n_gpus,
                lora_rank=args.lora_rank,
                lora_alpha=args.lora_alpha,
                epochs=epochs,
                rollout_n=args.num_generations,
                learning_rate=lr,
                kl_coeff=args.kl_coeff,
            )
        else:
            run_grpo_trl(
                model_name=args.model,
                data_path=args.data,
                output_dir=args.output,
                base_model=args.base_model,
                lora_rank=args.lora_rank,
                lora_alpha=args.lora_alpha,
                epochs=epochs,
                batch_size=args.batch_size,
                learning_rate=lr,
                num_generations=args.num_generations,
                max_completion_length=args.max_completion_length,
                temperature=args.temperature,
                kl_coeff=args.kl_coeff,
                bf16=args.bf16,
                use_vllm=args.use_vllm,
                vllm_gpu_memory_utilization=args.vllm_gpu_memory_utilization,
                vllm_max_model_length=args.vllm_max_model_length,
                qlora=args.qlora,
                seed=args.seed,
                reward_config=args.reward_config,
                tool_costs_config=args.tool_costs,
                rules_dir=args.rules_dir,
                hospital=args.hospital,
                allow_placeholder_rewards=args.allow_placeholder_rewards,
                grad_accum=args.grad_accum,
                generation_batch_size=args.generation_batch_size,
                max_steps=args.max_steps,
                logging_steps=args.logging_steps,
                save_steps=args.save_steps,
                eval_data=args.eval_data,
                eval_subset=args.eval_subset,
                eval_steps=args.eval_steps,
                num_generations_eval=args.num_generations_eval,
                importance_sampling_level=args.importance_sampling_level,
                scale_rewards=args.scale_rewards,
                loss_type=args.loss_type,
                multi_turn=args.multi_turn,
                per_turn_max_tokens=args.per_turn_max_tokens,
            )


if __name__ == "__main__":
    main()
