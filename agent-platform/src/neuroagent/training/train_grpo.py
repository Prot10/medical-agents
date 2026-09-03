"""GRPO with verifiable clinical-policy rewards over multi-turn typed episodes, on one GPU.

Rollouts run the *same* harness loop the benchmark uses (`ClinicalPolicyLoop` + `NeuroBenchEnvironment`),
against a vLLM engine colocated in the training process. Episodes are scored by the deterministic policy
reward, so every reward is verifiable against the physician-authored case policy (RLVR).

Single-GPU memory plan (measured on an A100-40GB with 8–9B models): the policy stays on the CPU while
TRL starts the colocated engine so vLLM gets most of the GPU; around every rollout the policy is swapped
to the CPU and the engine woken, then the engine sleeps (level 2) and the policy returns. Training
computes the vocabulary projection only at the model's own action tokens (environment observations are
masked and never projected), so a 12k-token episode costs one forward pass and a few hundred logits.

Techniques (all measured, see docs): token-level DAPO loss with clip-higher, batch-level advantage
normalization, truncation masking, vLLM importance-sampling correction, no KL term, LoRA on all linear
layers in bf16, one optimizer step per group batch (on-policy).

    uv run python -m neuroagent.training.train_grpo --model qwen3.5-9b --split train \\
        --output outputs/grpo/qwen --max-steps 50 --allow-draft-policies
"""

from __future__ import annotations

import argparse
import json
import os
import threading
import logging
import time
from collections import defaultdict
from concurrent.futures import Future
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from neuroagent_schemas import ClinicalEpisode, NeuroBenchCase, RunCompleted, RunStarted

from ..datasets import DATASETS, DEFAULT_DATASET_VERSION, load_dataset
from ..evaluation.policy_reward import ClinicalPolicyReward
from ..harness.adapters import SUBMIT_TOOL, NativeToolModelAdapter
from ..harness.context import transcript
from ..harness.environment import NeuroBenchEnvironment
from ..harness.interfaces import RunContext
from ..harness.loops import ClinicalPolicyLoop
from ..llm.client import LLMResponse, LLMToolCall
from ..model_registry import KEY_TO_MODEL
from .prefix_packing import (
    ATTN_IMPLEMENTATION,
    group_preserving_shuffle,
    pack_group,
    packed_group_logps,
    packed_logits_to_keep,
    packing_config,
    row_logps,
)

# Tool-call syntax is sampled freely, as in serving (serve_model.sh pins the same value).
os.environ.setdefault("VLLM_ENFORCE_STRICT_TOOL_CALLING", "0")
# fla auto-selects its TileLang backend when tilelang is importable (it is, as a vLLM dependency);
# those kernels JIT-compile with nvcc, which the training host lacks. The Triton kernels are used.
os.environ.setdefault("FLA_TILELANG", "0")

# LoRA on the language model's decoder projections only (attention, gated delta net, MLP). Qwen3.5
# and Gemma 4 checkpoints carry vision/audio towers whose linears never see a gradient here and
# which vLLM refuses to load as LoRA targets; Gemma's per-layer-embedding gates sit outside these
# sub-modules and are excluded as well.
LORA_TARGETS = (
    r"^model(\.language_model)?\.layers\.\d+\.(self_attn|linear_attn|mlp)"
    r"\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|in_proj_qkv|in_proj_z|in_proj_a|in_proj_b|out_proj)$"
)

logger = logging.getLogger(__name__)

_SAMPLING_METRICS = (
    "sampling/sampling_logp_difference/mean", "sampling/sampling_logp_difference/max",
    "sampling/importance_sampling_ratio/min", "sampling/importance_sampling_ratio/mean", "sampling/importance_sampling_ratio/max",
)

TOOL_PARSERS = {"qwen3.5-9b": "qwen3_coder", "granite-4.1-8b": "granite4", "gemma-4-e4b": "gemma4"}
REWARD_COMPONENTS = ("diagnosis", "required_action_coverage", "tool_accuracy", "safety", "stopping")


# --------------------------------------------------------------------------------------------------
# Rollout: the benchmark harness driven by the colocated engine, one turn-synchronous batch at a time
# --------------------------------------------------------------------------------------------------


@dataclass
class TurnRecord:
    prompt_text: str
    prompt_ids: list[int]
    token_ids: list[int]
    logprobs: list[float]
    raw_text: str
    messages: list[dict[str, Any]]
    tools: list[dict[str, Any]]
    finish_reason: str


@dataclass
class _Pending:
    thread: int
    messages: list[dict[str, Any]]
    tools: list[dict[str, Any]]
    future: Future = field(default_factory=Future)


class BatchedEngineClient:
    """Duck-types `LLMClient.chat` for the harness adapter with continuous batching over episodes.

    Each episode runs the unchanged `ClinicalPolicyLoop` in its own thread. A turn request blocks
    on a future; the coordinator submits it to the colocated engine the moment it arrives (rendered
    with the model's chat template, exactly as the server does) and keeps stepping the engine, so a
    fast episode never waits for a slow one and the batch stays full until episodes run out. Every
    call is recorded so the training sequence can be assembled from the tokens the model produced.
    """

    def __init__(self, llm, tokenizer, parser_name: str, request: dict[str, Any], *, max_tokens: int) -> None:
        from vllm import SamplingParams
        from vllm.entrypoints.openai.chat_completion.protocol import ChatCompletionRequest
        from vllm.tool_parsers import ToolParserManager

        self.engine = llm.llm_engine
        self.tokenizer = tokenizer
        self.parser_cls = ToolParserManager.get_tool_parser(parser_name)
        self.request_cls = ChatCompletionRequest
        self.template_kwargs = dict(request.get("chat_template_kwargs", {}))
        # Mirror the server's per-parser request adjustment (special-token handling, structural tags).
        probe = self.parser_cls(tokenizer).adjust_request(
            ChatCompletionRequest(model="policy", messages=[{"role": "user", "content": "x"}], tools=[SUBMIT_TOOL])
        )
        self.sampling = SamplingParams(
            temperature=float(request.get("temperature", 1.0)),
            top_p=float(request.get("top_p", 1.0)),
            top_k=int(request.get("top_k", 0)) or -1,
            presence_penalty=float(request.get("presence_penalty", 0.0)),
            max_tokens=max_tokens,
            logprobs=0,
            skip_special_tokens=probe.skip_special_tokens,
            structured_outputs=probe.structured_outputs,
        )
        self.model = "colocated"
        self.records: dict[int, list[TurnRecord]] = defaultdict(list)
        self.engine_steps = 0
        self.max_inflight = 0
        self._pending: dict[int, _Pending] = {}
        self._live: set[int] = set()
        self._cv = threading.Condition()

    # -- called from episode threads ------------------------------------------------------------
    def chat(self, messages, *, tools=None, tool_choice=None, response_format=None) -> LLMResponse:
        thread = threading.get_ident()
        item = _Pending(thread=thread, messages=messages, tools=list(tools or []))
        with self._cv:
            self._pending[thread] = item
            self._cv.notify_all()
        return item.future.result()

    def episode_started(self) -> None:
        with self._cv:
            self._live.add(threading.get_ident())
            self._cv.notify_all()

    def episode_finished(self) -> None:
        with self._cv:
            self._live.discard(threading.get_ident())
            self._cv.notify_all()

    # -- coordinator ----------------------------------------------------------------------------
    def serve_until_done(self, expected_threads: int) -> None:
        """Submit turn requests as they arrive and step the engine until no episode is live."""
        inflight: dict[str, tuple[_Pending, str, float]] = {}
        started = False
        submitted = 0
        while True:
            with self._cv:
                self._cv.wait_for(
                    lambda: (started or len(self._live) == expected_threads)
                    and (not self._live or self._pending or inflight)
                )
                started = True
                if not self._live and not inflight:
                    return
                ready = [self._pending.pop(thread) for thread in list(self._pending)]
            for item in ready:
                prompt = self.render(item)
                request_id = f"{item.thread}-{submitted}"
                submitted += 1
                self.engine.add_request(request_id, prompt, self.sampling)
                inflight[request_id] = (item, prompt, time.perf_counter())
            if not inflight:
                continue
            self.max_inflight = max(self.max_inflight, len(inflight))
            self.engine_steps += 1
            for output in self.engine.step():
                if output.finished:
                    item, prompt, started_at = inflight.pop(output.request_id)
                    self.finish(item, prompt, output, time.perf_counter() - started_at)

    def render(self, item: _Pending) -> str:
        return self.tokenizer.apply_chat_template(
            item.messages, tools=item.tools, tokenize=False, add_generation_prompt=True, **self.template_kwargs,
        )

    def finish(self, item: _Pending, prompt: str, output, latency: float) -> None:
        sample = output.outputs[0]
        raw = self.tokenizer.decode(sample.token_ids, skip_special_tokens=False)
        # The server builds the parser per request with the request's tools: the Qwen parser
        # casts XML parameter values (arrays, booleans, numbers) from the tool schemas.
        request = self.request_cls(model="policy", messages=[{"role": "user", "content": "x"}], tools=item.tools)
        parsed = self.parser_cls(self.tokenizer, tools=request.tools).extract_tool_calls(sample.text, request)
        calls = []
        for call in parsed.tool_calls:
            try:
                arguments = json.loads(call.function.arguments)
            except json.JSONDecodeError:
                arguments = None
            if isinstance(arguments, dict):
                calls.append(LLMToolCall(id=call.id, name=call.function.name, arguments=arguments))
        self.records[item.thread].append(
            TurnRecord(
                prompt_text=prompt,
                prompt_ids=list(output.prompt_token_ids),
                token_ids=list(sample.token_ids),
                logprobs=[lp[tok].logprob for tok, lp in zip(sample.token_ids, sample.logprobs)],
                raw_text=raw,
                messages=item.messages,
                tools=item.tools,
                finish_reason=str(sample.finish_reason),
            )
        )
        item.future.set_result(
            LLMResponse(
                content=parsed.content,
                tool_calls=calls,
                usage={"prompt_tokens": len(output.prompt_token_ids), "completion_tokens": len(sample.token_ids)},
                latency_seconds=latency,
            )
        )


def run_episodes(client: BatchedEngineClient, cases: list[NeuroBenchCase], *, max_turns: int, max_cost_usd: float):
    """Run one episode per case (cases may repeat) with the benchmark loop; returns (episode, records)."""
    results: dict[int, ClinicalEpisode] = {}
    threads: list[threading.Thread] = []
    order: list[int] = []

    def worker(case: NeuroBenchCase, slot: int) -> None:
        client.episode_started()
        try:
            context = RunContext(
                profile_id="grpo-rollout",
                model=NativeToolModelAdapter(client),
                loop=ClinicalPolicyLoop(),
                environment=NeuroBenchEnvironment(case),
                max_turns=max_turns,
                max_cost_usd=max_cost_usd,
            )
            results[slot] = context.loop.run(context)
        finally:
            client.episode_finished()

    for slot, case in enumerate(cases):
        thread = threading.Thread(target=worker, args=(case, slot), daemon=True)
        threads.append(thread)
    for thread in threads:
        thread.start()
    client.serve_until_done(len(threads))
    for thread in threads:
        thread.join()
    return [(results[slot], client.records.pop(thread.ident, [])) for slot, thread in enumerate(threads)]


@dataclass
class Sequence:
    prompt_ids: list[int]
    completion_ids: list[int]
    env_mask: list[int]
    logprobs: list[float]
    turns: int
    dropped_retry_tokens: int
    conditioning_mismatches: int
    correction_turns: int = 0
    rerender_mismatches: int = 0
    rerender_example: tuple[str, str] | None = None


def _base_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The canonical transcript: a trailing user message after the patient text is a transient
    correction or final-turn instruction that later turns do not carry."""
    return messages[:-1] if len(messages) > 2 and messages[-1]["role"] == "user" else messages


def assemble_sequence(tokenizer, records: list[TurnRecord], template_kwargs: dict[str, Any] | None = None) -> Sequence:
    """One training sequence per episode.

    The model's own tokens stand for every accepted action; the environment text between actions
    is rendered from the canonical transcript (masked) and tokenized at the boundary where
    generation started. Rejected attempts (retried with a correction) are dropped from the
    sequence and counted. A turn whose conditioning differed from the sequence (a correction in
    its prompt, or a template re-rendering of the action that differs from the sampled text) is
    counted as a conditioning mismatch; the importance-sampling correction covers the rest.
    """
    template_kwargs = template_kwargs or {}

    def render(messages, tools, generation):
        return tokenizer.apply_chat_template(
            messages, tools=tools, tokenize=False, add_generation_prompt=generation, **template_kwargs
        )

    accepted: list[TurnRecord] = []
    dropped = 0
    for index, record in enumerate(records):
        if index + 1 < len(records):
            base = _base_messages(record.messages)
            following = records[index + 1].messages
            if not (len(following) > len(base) and following[len(base)]["role"] == "assistant"):
                dropped += len(record.token_ids)
                continue
        accepted.append(record)

    completion: list[int] = []
    mask: list[int] = []
    logprobs: list[float] = []
    mismatches = corrections = rerenders = 0
    example = None
    for index, record in enumerate(accepted):
        completion += record.token_ids
        mask += [1] * len(record.token_ids)
        logprobs += record.logprobs
        if index + 1 == len(accepted):
            break
        following = accepted[index + 1]
        # The canonical transcript is the one later turns see: the next record's messages, which
        # carry neither the correction appended for a retry nor a final-turn instruction.
        n = len(_base_messages(record.messages))
        generation_prompt = render(following.messages[:n], record.tools, True)
        full = render(following.messages[: n + 1], record.tools, False)
        if not following.prompt_text.startswith(full):
            at = next((i for i, (a, b) in enumerate(zip(full, following.prompt_text)) if a != b), min(len(full), len(following.prompt_text)))
            raise ValueError(
                "chat template does not chain turns as prefixes of one transcript; diverges at "
                f"{at}/{len(full)}: rendered {full[max(0, at - 80):at + 80]!r} vs next prompt "
                f"{following.prompt_text[max(0, at - 80):at + 80]!r}"
            )
        rendered_action = full[len(generation_prompt):]
        corrected = record.prompt_text != generation_prompt
        rerendered = not rendered_action.startswith(record.raw_text)
        corrections += corrected
        rerenders += rerendered
        if rerendered and example is None:
            example = (record.raw_text[-300:], rendered_action[-300:])
        if corrected or rerendered:
            mismatches += 1
            delta = following.prompt_text[len(full):]
        else:
            delta = rendered_action[len(record.raw_text):] + following.prompt_text[len(full):]
        ids = tokenizer(delta, add_special_tokens=False)["input_ids"]
        completion += ids
        mask += [0] * len(ids)
        logprobs += [0.0] * len(ids)
    return Sequence(
        # The canonical prompt is the first request's: a retry of the first turn carries the
        # correction, which is a conditioning mismatch like any other and must not become the
        # sequence's prefix (the group shares one prompt).
        prompt_ids=records[0].prompt_ids,
        completion_ids=completion,
        env_mask=mask,
        logprobs=logprobs,
        turns=len(accepted),
        dropped_retry_tokens=dropped,
        conditioning_mismatches=mismatches,
        correction_turns=corrections,
        rerender_mismatches=rerenders,
        rerender_example=example,
    )


# --------------------------------------------------------------------------------------------------
# Rewards: the verifiable policy reward and its components (components are logged, not optimized)
# --------------------------------------------------------------------------------------------------


def make_reward_funcs(cases: dict[str, NeuroBenchCase], scorer: ClinicalPolicyReward):
    def breakdown(episode_json: str):
        episode = ClinicalEpisode.model_validate_json(episode_json)
        started = next(event for event in episode.events if isinstance(event, RunStarted))
        return scorer.score(episode, cases[started.case_id])

    def scalar(completions, episode, **kwargs):
        return [breakdown(item).scalar for item in episode]

    scalar.__name__ = "policy_scalar"
    funcs = [scalar]
    for component in REWARD_COMPONENTS:
        def func(completions, episode, _component=component, **kwargs):
            return [getattr(breakdown(item), _component) for item in episode]

        func.__name__ = component
        funcs.append(func)

    def completed(completions, episode, **kwargs):
        return [float(isinstance(ClinicalEpisode.model_validate_json(item).events[-1], RunCompleted)) for item in episode]

    completed.__name__ = "completed"
    funcs.append(completed)
    return funcs


# --------------------------------------------------------------------------------------------------
# Trainer
# --------------------------------------------------------------------------------------------------


def build_trainer(
    *,
    model_key: str,
    cases: dict[str, NeuroBenchCase],
    train_cases: list[NeuroBenchCase],
    output_dir: str,
    scorer: ClinicalPolicyReward,
    max_steps: int,
    num_generations: int,
    cases_per_step: int,
    learning_rate: float,
    max_turns: int,
    max_cost_usd: float,
    max_completion_tokens: int,
    vllm_gpu_memory_utilization: float,
    seed: int,
    rollout_temperature: float | None = None,
    save_steps: int = 5,
    prefix_sharing: bool = True,
    verify_packing: bool = False,
):
    import torch
    from datasets import Dataset
    from peft import LoraConfig
    from transformers import AutoTokenizer, TrainerCallback
    from trl import GRPOConfig, GRPOTrainer
    from trl.generation.vllm_generation import VLLMGeneration
    from trl.trainer import grpo_trainer as grpo_module
    from trl.trainer.utils import selective_log_softmax, entropy_from_logits

    concurrent_episodes = num_generations * cases_per_step

    class Engine(VLLMGeneration):
        """TRL sizes the colocated engine for its own one-sequence-per-step generation; the rollout
        batches every live episode into one generate call, so the engine must admit all of them.
        The engine also gets the serving configuration that measured fastest (large prefill
        chunks; Qwen's lossless MTP draft), and its weight sync is timed."""

        def __init__(self, *args_, max_num_seqs=None, **kwargs):
            super().__init__(*args_, max_num_seqs=concurrent_episodes, **kwargs)

        def sync_weights(self):
            started = time.perf_counter()
            super().sync_weights()
            sync_seconds.append(time.perf_counter() - started)

    sync_seconds: list[float] = []
    grpo_module.VLLMGeneration = Engine
    import trl.generation.vllm_generation as vllm_generation_module
    from vllm import LLM as _LLM

    class EngineLLM(_LLM):
        def __init__(self, *args_, **kwargs):
            kwargs["max_num_batched_tokens"] = 16384
            if multimodal:
                kwargs["language_model_only"] = True  # rollouts are text; skip the vision/audio towers
            if engine_kwargs:
                kwargs.update(engine_kwargs)
            super().__init__(*args_, **kwargs)

    vllm_generation_module.LLM = EngineLLM

    entry = KEY_TO_MODEL[model_key]
    tokenizer = AutoTokenizer.from_pretrained(entry["hf_model_id"])
    engine_kwargs = dict(entry.get("engine_kwargs", {}))
    from transformers import AutoConfig

    model_config = AutoConfig.from_pretrained(entry["hf_model_id"])
    multimodal = getattr(model_config, "vision_config", None) is not None
    packing = packing_config(model_config) if prefix_sharing else None
    packable = packing is not None
    # GRPO needs stochastic rollouts: a greedy model-card default (Granite) yields identical
    # samples per group (no advantage) and a zero temperature breaks the trainer's logit scaling.
    request = {**entry["request_defaults"], "temperature": rollout_temperature or entry["request_defaults"].get("temperature") or 1.0}
    if request["temperature"] <= 0:
        request["temperature"] = 1.0
    case_by_prompt = {transcript(case, ClinicalEpisode())[1]["content"]: case for case in cases.values()}
    dataset = Dataset.from_list(
        [{"prompt": transcript(case, ClinicalEpisode()), "case_id": case.case_id} for case in train_cases]
    )
    device = torch.device("cuda")
    diagnostics: dict[str, list[float]] = defaultdict(list)
    self_packing_enabled = packable
    if packable:
        # Micro-batches must stay whole groups for the packed forward (TRL shuffles rows).
        def shuffle_groups(seq_dict):
            before = [int(m.sum()) for m in seq_dict["prompt_mask"]]
            shuffled = group_preserving_shuffle(seq_dict, group_size=num_generations)
            logger.info("prompt lengths before shuffle %s after %s", before, [int(m.sum()) for m in shuffled["prompt_mask"]])
            return shuffled

        grpo_module.shuffle_sequence_dict = shuffle_groups

    class PolicyGRPOTrainer(GRPOTrainer):
        """Policy on CPU while the colocated engine starts; sparse-logit log-probs; swap around rollouts."""

        def _move_model_to_device(self, model, device):  # noqa: D401 - Trainer hook
            return None

        def _log_metric(self, name: str, value: float) -> None:
            # TRL parks custom metrics in a pending buffer that is flushed at the next generation,
            # so anything logged after it (the training forward) would land one step late.
            self._metrics["train"][name].append(float(value))

        def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
            started = time.perf_counter()
            self._current_inputs = inputs  # the training forward fills in old log-probs and the vLLM ratio
            try:
                result = super().compute_loss(model, inputs, return_outputs=return_outputs, num_items_in_batch=num_items_in_batch)
            finally:
                self._current_inputs = None
            self._log_metric("train/compute_loss_seconds", time.perf_counter() - started)
            return result

        @staticmethod
        def _use_attention(model, implementation):
            if self_packing_enabled and model.config._attn_implementation != implementation:
                model.set_attn_implementation(implementation)

        def _row_logps(self, model, ids, att, logits_to_keep, compute_entropy, attention="sdpa"):
            """Per-row path: one forward, vocabulary projection only at supervised positions."""
            total = ids.size(0)
            completion = ids[total - logits_to_keep:]
            valid = int(att[total - logits_to_keep:].sum().item())
            env_mask = self._env_masks.get(tuple(completion[:valid].tolist()))
            if env_mask is None:
                raise RuntimeError("no environment mask recorded for a completion; rollout bookkeeping is broken")
            logps = torch.zeros(logits_to_keep, device=ids.device, dtype=torch.float32)
            entropies = torch.zeros_like(logps)
            supervised = [j for j, m in enumerate(env_mask) if m]
            if supervised:
                keep = torch.tensor([total - logits_to_keep + j - 1 for j in supervised], device=ids.device)
                self._use_attention(model, attention)  # sdpa by default: flash kernels, no per-length recompile
                forward_started = time.perf_counter()
                values, ent = row_logps(
                    model, ids, att, keep, completion[supervised], temperature=self.temperature,
                    kernel_options=self._packing["kernel_options"] if attention == ATTN_IMPLEMENTATION else None,
                )
                torch.cuda.synchronize()
                self._log_metric("train/forward_seconds_per_row", time.perf_counter() - forward_started)
                self._log_metric("train/row_tokens", float(att.sum().item()))
                logps[supervised] = values
                if compute_entropy:
                    entropies[supervised] = ent
            return logps, entropies

        def _group_logps(self, model, input_ids, attention_mask, logits_to_keep, compute_entropy):
            """Packed path: the group's shared prompt once, all completions block-causally masked."""
            total = input_ids.size(1)
            prompts, completions, supervised = [], [], []
            for row in range(input_ids.size(0)):
                ids, att = input_ids[row], attention_mask[row].bool()
                prompt_part, completion_part = ids[: total - logits_to_keep], ids[total - logits_to_keep:]
                prompts.append(prompt_part[att[: total - logits_to_keep]].tolist())
                completion = completion_part[att[total - logits_to_keep:]].tolist()
                env_mask = self._env_masks.get(tuple(completion))
                if env_mask is None:
                    raise RuntimeError("no environment mask recorded for a completion; rollout bookkeeping is broken")
                completions.append(completion)
                supervised.append([j for j, m in enumerate(env_mask) if m])
            if any(prompt != prompts[0] for prompt in prompts):
                current = self._current_inputs or {}
                described = {k: (tuple(v.shape) if torch.is_tensor(v) else (type(v).__name__, len(v) if hasattr(v, "__len__") else None)) for k, v in current.items()}
                divergence = [next((i for i, (a, b) in enumerate(zip(prompts[0], prompt)) if a != b), min(len(prompts[0]), len(prompt))) for prompt in prompts]
                raise RuntimeError(
                    "a micro-batch mixes prompts; the group-preserving shuffle is not in effect. "
                    f"prompt lengths {[len(p) for p in prompts]}, first divergence {divergence}, "
                    f"case ids {current.get('case_id')}, inputs {described}"
                )
            packed = pack_group(
                prompts[0], completions, device=input_ids.device,
                layer_types=self._packing["layer_types"], sliding_window=self._packing["sliding_window"],
            )
            keep, targets = packed_logits_to_keep(packed, supervised)
            logps = torch.zeros(input_ids.size(0), logits_to_keep, device=input_ids.device, dtype=torch.float32)
            entropies = torch.zeros_like(logps)
            if keep.numel():
                self._use_attention(model, ATTN_IMPLEMENTATION)
                forward_started = time.perf_counter()
                values, ent = packed_group_logps(
                    model, packed, keep, targets, temperature=self.temperature, kernel_options=self._packing["kernel_options"],
                )
                torch.cuda.synchronize()
                self._log_metric("train/forward_seconds_per_group", time.perf_counter() - forward_started)
                self._log_metric("train/packed_tokens", float(packed.input_ids.size(1)))
                offset = 0
                for row, positions in enumerate(supervised):
                    if positions:
                        index = torch.tensor(positions, device=input_ids.device)
                        logps[row, index] = values[offset : offset + len(positions)]
                        if compute_entropy:
                            entropies[row, index] = ent[offset : offset + len(positions)]
                    offset += len(positions)
            return logps, entropies

        def _get_per_token_logps_and_entropies(
            self, model, input_ids, attention_mask, logits_to_keep, batch_size=None, compute_entropy=False,
            compute_aux_loss=False, **kwargs,
        ):
            if batch_size is not None and not torch.is_grad_enabled() and self._on_policy:
                # TRL's old-log-prob pass over the generation batch (always run with vLLM importance
                # sampling). On-policy with aligned steps the weights do not change before the loss is
                # computed, so these equal the training forward's detached log-probs: the pass returns
                # a placeholder, and the training forward replaces it together with the vLLM
                # importance ratio TRL derives from it. One full forward per row less.
                self._placeholder_pending = True
                return torch.zeros(input_ids.size(0), logits_to_keep, device=input_ids.device), None, None
            started = time.perf_counter()
            chunk = batch_size or input_ids.size(0)
            parts = [
                self._chunk_logps(model, input_ids[i : i + chunk], attention_mask[i : i + chunk], logits_to_keep, compute_entropy)
                for i in range(0, input_ids.size(0), chunk)
            ]
            logps = torch.cat([p[0] for p in parts])
            entropies = torch.cat([p[1] for p in parts])
            if torch.is_grad_enabled() and not logps.requires_grad:
                # Every row was masked (overlong episodes): keep a grad path so backward sees a zero.
                logps.requires_grad_(True)
            if torch.is_grad_enabled() and self._on_policy and self._current_inputs is not None:
                self._fill_in_old_logps(self._current_inputs, logps.detach())
            self._log_metric("train/logps_seconds", time.perf_counter() - started)
            return logps, (entropies if compute_entropy else None), None

        def _fill_in_old_logps(self, inputs, old_logps):
            """On-policy: old log-probs are this forward's; recompute TRL's vLLM importance ratio from them."""
            sampled = inputs.get("sampling_per_token_logps")
            inputs["old_per_token_logps"] = old_logps
            if sampled is None:
                return
            mask = inputs["completion_mask"] * inputs.get("tool_mask", torch.ones_like(inputs["completion_mask"]))
            diff = (old_logps - sampled) * mask
            ratio = torch.exp(diff).clamp(min=self.vllm_importance_sampling_clip_min, max=self.vllm_importance_sampling_clip_max)
            inputs["importance_sampling_ratio"] = ratio
            metrics = self._metrics["train"]
            if self._placeholder_pending:  # drop the statistics TRL computed from the placeholder
                for key in _SAMPLING_METRICS:
                    if metrics.get(key):
                        metrics[key].pop()
                self._placeholder_pending = False
            valid = mask.bool()
            delta = (old_logps - sampled).abs()[valid]
            flat = ratio[valid]
            metrics["sampling/sampling_logp_difference/mean"].append(delta.mean().item() if delta.numel() else 0.0)
            metrics["sampling/sampling_logp_difference/max"].append(delta.max().item() if delta.numel() else 0.0)
            metrics["sampling/importance_sampling_ratio/min"].append(flat.min().item() if flat.numel() else 0.0)
            metrics["sampling/importance_sampling_ratio/mean"].append(flat.mean().item() if flat.numel() else 0.0)
            metrics["sampling/importance_sampling_ratio/max"].append(flat.max().item() if flat.numel() else 0.0)
            log_logp_disagreement(self, inputs)

        def _chunk_logps(self, model, input_ids, attention_mask, logits_to_keep, compute_entropy):
            """One micro-batch: a packed group when the model allows it, per-row forwards otherwise."""
            if self._packing is not None and input_ids.size(0) > 1:
                result = self._group_logps(model, input_ids, attention_mask, logits_to_keep, compute_entropy)
                if verify_packing and not self._packing_verified:
                    with torch.no_grad():  # reference forwards only; their graphs would not fit next to the packed one
                        per_row = torch.stack([self._row_logps(model, input_ids[r], attention_mask[r], logits_to_keep, False)[0] for r in range(input_ids.size(0))])
                        # Noise floor: the same rows under FlexAttention vs SDPA, both per-row (bf16 kernels differ).
                        rows_flex = torch.stack([self._row_logps(model, input_ids[r], attention_mask[r], logits_to_keep, False, attention=ATTN_IMPLEMENTATION)[0] for r in range(input_ids.size(0))])
                    # Checkpointed layers are recomputed in backward with the implementation current
                    # *then*; the packed graph holds a BlockMask, so FlexAttention must be back in place.
                    self._use_attention(model, ATTN_IMPLEMENTATION)
                    supervised_mask = per_row != 0
                    gap = (result[0].detach() - per_row.detach()).abs()[supervised_mask]
                    floor = (rows_flex - per_row).abs()[supervised_mask]
                    for name, values in (("packing", gap), ("kernel_floor", floor)):
                        self._log_metric(f"train/{name}_max_abs_logp_gap", values.max().item() if values.numel() else 0.0)
                        self._log_metric(f"train/{name}_mean_abs_logp_gap", values.mean().item() if values.numel() else 0.0)
                        self._log_metric(f"train/{name}_p99_abs_logp_gap", values.quantile(0.99).item() if values.numel() else 0.0)
                    self._packing_verified = True
                return result
            rows = [self._row_logps(model, input_ids[r], attention_mask[r], logits_to_keep, compute_entropy) for r in range(input_ids.size(0))]
            return torch.stack([r[0] for r in rows]), torch.stack([r[1] for r in rows])

    def log_logp_disagreement(trainer, inputs):
        """Where do the sampler (vLLM) and the trainer disagree most? Token, position, segment start."""
        old = inputs.get("old_per_token_logps")
        sampled = inputs.get("sampling_per_token_logps")
        if old is None or sampled is None:
            return
        completion_ids = inputs["completion_ids"]
        mask = (inputs["completion_mask"] * inputs.get("tool_mask", torch.ones_like(inputs["completion_mask"]))).bool()
        delta = (old - sampled).abs() * mask
        rows = []
        for b in range(delta.size(0)):
            values, positions = torch.topk(delta[b], k=min(3, delta.size(1)))
            for value, position in zip(values.tolist(), positions.tolist()):
                if value <= 0:
                    continue
                segment_start = position > 0 and not mask[b, position - 1].item()
                rows.append({
                    "step": trainer.state.global_step, "row": b, "position": position, "abs_logp_diff": round(value, 3),
                    "trainer_logp": round(old[b, position].item(), 3), "sampler_logp": round(sampled[b, position].item(), 3),
                    "token": tokenizer.decode([completion_ids[b, position].item()]),
                    "segment_start": bool(segment_start),
                })
        with open(Path(output_dir, "logp_disagreement.jsonl"), "a") as handle:
            handle.write("".join(json.dumps(row) + "\n" for row in rows))

    def rollout_func(prompts, trainer):
        engine = trainer.vllm_generation
        llm = engine.llm
        model = trainer.model
        phase = time.perf_counter()
        model.to("cpu")
        torch.cuda.empty_cache()
        if engine.enable_sleep_mode:
            llm.wake_up(tags=["kv_cache"])
        swap_out_seconds = time.perf_counter() - phase
        client = BatchedEngineClient(llm, tokenizer, TOOL_PARSERS[model_key], request, max_tokens=max_completion_tokens)
        batch_cases = [case_by_prompt[prompt[1]["content"]] for prompt in prompts]
        logger.info("cases in prompt order %s", [case.case_id for case in batch_cases])
        started = time.perf_counter()
        episodes = run_episodes(client, batch_cases, max_turns=max_turns, max_cost_usd=max_cost_usd)
        rollout_seconds = time.perf_counter() - started
        phase = time.perf_counter()
        if engine.enable_sleep_mode:
            llm.sleep(level=2)
        torch.cuda.empty_cache()
        model.to(device)
        swap_in_seconds = time.perf_counter() - phase

        output = {"prompt_ids": [], "completion_ids": [], "logprobs": [], "env_mask": [], "episode": []}
        trainer._env_masks = {}
        mismatches = turns = dropped = truncated_turns = corrections = rerenders = 0
        rerender_example = None
        rollout_dir = Path(output_dir, "rollouts")
        rollout_dir.mkdir(exist_ok=True)
        rows = []
        for episode, records in episodes:
            sequence = assemble_sequence(tokenizer, records, client.template_kwargs)
            truncated = sum(record.finish_reason == "length" for record in records)
            truncated_turns += truncated
            if truncated:
                # Overlong filtering (DAPO): an episode with a length-truncated action carries no
                # loss. Done here, model-agnostically, because TRL's EOS check does not know that
                # Gemma and Granite stop on several different tokens.
                sequence.env_mask = [0] * len(sequence.env_mask)
            terminal = episode.events[-1]
            rows.append(
                {
                    "case_id": episode.events[0].case_id,
                    "status": terminal.type,
                    "failure_reason": getattr(terminal, "reason", None),
                    "failure_message": getattr(terminal, "message", None),
                    "turns": sequence.turns,
                    "attempts": len(records),
                    "truncated_turns": sum(record.finish_reason == "length" for record in records),
                    "reward": scorer.score(episode, cases[episode.events[0].case_id]).model_dump(mode="json"),
                    "tools": [action.tool_name for action in episode.tool_actions],
                    "raw_turns": [
                        {"tokens": len(r.token_ids), "finish_reason": r.finish_reason, "raw_text": r.raw_text}
                        for r in records
                    ],
                    "episode": episode.model_dump(mode="json"),
                }
            )
            output["prompt_ids"].append(sequence.prompt_ids)
            output["completion_ids"].append(sequence.completion_ids)
            output["logprobs"].append(sequence.logprobs)
            output["env_mask"].append(sequence.env_mask)
            output["episode"].append(episode.model_dump_json())
            trainer._env_masks[tuple(sequence.completion_ids)] = sequence.env_mask
            mismatches += sequence.conditioning_mismatches
            corrections += sequence.correction_turns
            rerenders += sequence.rerender_mismatches
            rerender_example = rerender_example or sequence.rerender_example
            dropped += sequence.dropped_retry_tokens
            turns += sequence.turns
        with open(rollout_dir / f"step-{trainer.state.global_step:04d}.jsonl", "w") as handle:
            handle.write("".join(json.dumps(row) + "\n" for row in rows))
        generated = sum(sum(t["tokens"] for t in row["raw_turns"]) for row in rows)
        trainer._log_metric("rollout/generated_tokens_per_second", generated / max(rollout_seconds, 1e-6))
        trainer._log_metric("rollout/engine_steps", float(client.engine_steps))
        trainer._log_metric("rollout/max_inflight", float(client.max_inflight))
        trainer._log_metric("rollout/completed_rate", sum(row["status"] == "run.completed" for row in rows) / len(rows))
        trainer._log_metric("rollout/truncated_turns_per_episode", truncated_turns / len(episodes))
        trainer._log_metric("rollout/seconds", rollout_seconds)
        trainer._log_metric("rollout/turns_per_episode", turns / len(episodes))
        trainer._log_metric("rollout/conditioning_mismatch_rate", mismatches / max(1, turns))
        trainer._log_metric("rollout/correction_turn_rate", corrections / max(1, turns))
        trainer._log_metric("rollout/rerender_mismatch_rate", rerenders / max(1, turns))
        trainer._log_metric("rollout/swap_out_seconds", swap_out_seconds)
        if sync_seconds:
            trainer._log_metric("rollout/sync_weights_seconds", sync_seconds.pop())
        trainer._log_metric("rollout/swap_in_seconds", swap_in_seconds)
        if rerender_example is not None:
            with open(Path(output_dir, "rerender_examples.jsonl"), "a") as handle:
                handle.write(json.dumps({"step": trainer.state.global_step, "raw": rerender_example[0], "rendered": rerender_example[1]}) + "\n")
        trainer._log_metric("rollout/dropped_retry_tokens_per_episode", dropped / len(episodes))
        trainer._log_metric("rollout/action_tokens_per_episode", sum(sum(m) for m in output["env_mask"]) / len(episodes))
        trainer._log_metric("rollout/sequence_tokens_mean", sum(len(c) for c in output["completion_ids"]) / len(episodes))
        return output

    class JsonlLog(TrainerCallback):
        def on_log(self, args, state, control, logs=None, **kwargs):
            with open(Path(output_dir, "train_log.jsonl"), "a") as handle:
                handle.write(json.dumps({"step": state.global_step, **(logs or {})}) + "\n")

    config = GRPOConfig(
        output_dir=output_dir,
        # bf16 weights loaded on the CPU: the colocated engine is created during trainer init and
        # must see a free GPU; the policy is moved to the GPU right after (see below).
        # A packed group needs FlexAttention's block-sparse mask (see prefix_packing).
        model_init_kwargs={"dtype": "bfloat16", "device_map": "cpu", **({"attn_implementation": ATTN_IMPLEMENTATION} if packable else {})},
        max_steps=max_steps,
        learning_rate=learning_rate,
        lr_scheduler_type="constant_with_warmup",
        warmup_steps=min(5, max_steps),
        # A micro-batch is one group when the prompt prefix can be shared (Gemma, Granite); Qwen's
        # recurrent layers cannot fork a prefix state, so it trains one row at a time.
        per_device_train_batch_size=num_generations if packable else 1,
        gradient_accumulation_steps=cases_per_step if packable else num_generations * cases_per_step,
        generation_batch_size=num_generations * cases_per_step,
        num_generations=num_generations,
        gradient_checkpointing=True,
        bf16=True,
        seed=seed,
        # Sampling is done by the rollout with the model card's settings; these feed the trainer's
        # logit temperature and the engine's default params only.
        temperature=float(request.get("temperature", 1.0)),
        max_completion_length=max_completion_tokens,
        # Loss: token-level DAPO normalization, clip-higher, batch-level advantage scale, no KL,
        # truncated episodes masked, vLLM importance-sampling correction.
        loss_type="dapo",
        epsilon=0.2,
        epsilon_high=0.28,
        scale_rewards="batch",
        beta=0.0,
        num_iterations=1,
        mask_truncated_completions=False,  # handled per episode in the rollout (see env_mask)
        vllm_importance_sampling_correction=True,
        # Token-level truncated IS: a sequence-level ratio over ~1k action tokens underflows to 0
        # because vLLM reports top-k/top-p-processed log-probs (measured: ratio 1e-38, zero gradient).
        vllm_importance_sampling_mode="token_truncate",
        use_vllm=True,
        vllm_mode="colocate",
        vllm_enable_sleep_mode=True,
        vllm_gpu_memory_utilization=vllm_gpu_memory_utilization,
        vllm_max_model_length=32768,
        reward_weights=[1.0] + [0.0] * (len(REWARD_COMPONENTS) + 1),
        logging_steps=1,
        save_strategy="steps",
        save_steps=save_steps,
        save_total_limit=2,
        report_to="none",
        log_completions=False,
    )
    trainer = PolicyGRPOTrainer(
        model=entry["hf_model_id"],
        reward_funcs=make_reward_funcs(cases, scorer),
        args=config,
        train_dataset=dataset,
        processing_class=tokenizer,
        peft_config=LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules=LORA_TARGETS, task_type="CAUSAL_LM"),
        rollout_func=rollout_func,
        callbacks=[JsonlLog()],
    )
    trainer._env_masks = {}
    trainer._packing = packing
    trainer._packing_verified = False
    generate_every = config.steps_per_generation * trainer.num_iterations
    trainer._on_policy = trainer.num_iterations == 1 and config.gradient_accumulation_steps % generate_every == 0
    if trainer._on_policy and trainer.vllm_importance_sampling_mode != "token_truncate":
        raise ValueError("the on-policy importance ratio is implemented for token_truncate only")
    trainer._placeholder_pending = False
    trainer._current_inputs = None
    trainer.model.to(device)
    return trainer, diagnostics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, choices=sorted(KEY_TO_MODEL))
    parser.add_argument("--output", required=True)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--split", choices=["train", "test"])
    selection.add_argument("--cases", nargs="+")
    parser.add_argument("--max-steps", type=int, default=50)
    parser.add_argument("--num-generations", type=int, default=8)
    parser.add_argument("--cases-per-step", type=int, default=2)
    parser.add_argument("--learning-rate", type=float, default=1e-5)
    parser.add_argument("--max-turns", type=int, default=12)
    parser.add_argument("--max-cost-usd", type=float, default=15000.0)
    parser.add_argument("--max-completion-tokens", type=int, default=4096)
    parser.add_argument("--vllm-gpu-memory-utilization", type=float, default=0.8)
    parser.add_argument("--rollout-temperature", type=float, default=None, help="override the model card's sampling temperature for rollouts")
    parser.add_argument("--save-steps", type=int, default=5, help="adapter checkpoint interval (a VM stop must not lose the run)")
    parser.add_argument("--no-prefix-sharing", action="store_true", help="train one row at a time even when the group prompt could be shared")
    parser.add_argument("--verify-packing", action="store_true", help="also compute per-row log-probs on the first batch and log the gap")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--allow-draft-policies", action="store_true")
    args = parser.parse_args()

    dataset = DATASETS[DEFAULT_DATASET_VERSION]
    _, cases = load_dataset(dataset.path)
    if args.cases:
        train_cases = [cases[case_id] for case_id in args.cases]
    else:
        ids = (dataset.path / "splits" / f"{args.split}_cases.txt").read_text().split()
        train_cases = [cases[case_id] for case_id in ids]
    Path(args.output).mkdir(parents=True, exist_ok=True)
    Path(args.output, "run_config.json").write_text(json.dumps(vars(args), indent=2))
    trainer, _ = build_trainer(
        model_key=args.model,
        cases=cases,
        train_cases=train_cases,
        output_dir=args.output,
        scorer=ClinicalPolicyReward(require_approved=not args.allow_draft_policies),
        max_steps=args.max_steps,
        num_generations=args.num_generations,
        cases_per_step=args.cases_per_step,
        learning_rate=args.learning_rate,
        max_turns=args.max_turns,
        max_cost_usd=args.max_cost_usd,
        max_completion_tokens=args.max_completion_tokens,
        vllm_gpu_memory_utilization=args.vllm_gpu_memory_utilization,
        seed=args.seed,
        rollout_temperature=args.rollout_temperature,
        save_steps=args.save_steps,
        prefix_sharing=not args.no_prefix_sharing,
        verify_packing=args.verify_packing,
    )
    trainer.train()
    trainer.save_model(args.output)
    trainer.processing_class.save_pretrained(args.output)
    Path(args.output, "train_log.json").write_text(json.dumps(trainer.state.log_history, indent=2))


if __name__ == "__main__":
    main()
