"""TRL ``rollout_func`` adapter for multi-turn GRPO.

TRL 0.29's ``GRPOTrainer`` accepts a ``rollout_func(prompts, trainer)`` that returns
``{"prompt_ids", "completion_ids", "logprobs", ...}``; any extra key is forwarded to the
reward functions, and an ``env_mask`` key is consumed as the per-token loss mask (1 = model
token, 0 = external). We can't use TRL's native ``tools=``/``environment_factory`` path
because Qwen3.5's tokenizer has no ``response_schema``, so TRL never parses its tool calls.
Instead this adapter drives :class:`ReactRollout` — our own qwen3_coder parser + the
deterministic ``MockServer`` — and hands TRL a token-exact, masked multi-turn trajectory
plus the reward scored on the genuine :class:`AgentTrace`.

Generation for each assistant turn uses the trainer's own model (HF ``generate`` via
``_generate_single_turn``), so the rollout is always on-policy. The reward is computed here
(we hold the trace) and passed through as an extra field; ``precomputed_trajectory_reward``
below just reads it back, because TRL requires a reward function.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

from .react_rollout import ReactRollout

logger = logging.getLogger(__name__)


class MultiTurnRolloutFunc:
    """Callable passed as ``rollout_func`` to ``GRPOTrainer``.

    Args:
        rollout: the configured :class:`ReactRollout` (tokenizer, tools, system prompt).
        prompt_to_case: maps a dataset prompt string to its ``case_id`` (bijective — one
            rendered prompt per case).
        cases: ``case_id`` → ``NeuroBenchCase``.
        patient_info: ``case_id`` → the user-message patient text (``format_patient_info``).
        reward_fn: scores an ``AgentTrace`` against its case → float.
        mock_server_factory: ``case`` → a fresh ``MockServer`` for one trajectory.
        cost_tracker_factory: () → a fresh ``CostTracker`` for one trajectory.
        per_turn_max_tokens: token cap for a single assistant turn's generation.
    """

    def __init__(
        self,
        rollout: ReactRollout,
        prompt_to_case: dict[str, str],
        cases: dict[str, Any],
        patient_info: dict[str, str],
        reward_fn: Callable[[Any, Any], float],
        mock_server_factory: Callable[[Any], Any],
        cost_tracker_factory: Callable[[], Any],
        per_turn_max_tokens: int = 512,
    ) -> None:
        self.rollout = rollout
        self.prompt_to_case = prompt_to_case
        self.cases = cases
        self.patient_info = patient_info
        self.reward_fn = reward_fn
        self.mock_server_factory = mock_server_factory
        self.cost_tracker_factory = cost_tracker_factory
        self.per_turn_max_tokens = per_turn_max_tokens

    def _make_generate_batch_fn(
        self, trainer: Any
    ) -> Callable[[list[list[int]]], list[list[int]]]:
        """Batched one-turn generator bound to the trainer's model (on-policy HF generate).

        Takes every still-active trajectory's context and returns each one's next assistant
        turn, in ONE generate call — the per-turn ~6k-token prefill is then paid once for the
        whole group instead of once per trajectory.

        ``max_new_tokens`` is capped at ``per_turn_max_tokens`` for the duration of the call:
        the trainer's generation_config carries the whole-completion budget (thousands of
        tokens for multi-turn), and HF generate runs until EVERY sequence in the batch hits
        EOS, so leaving it uncapped lets one runaway sequence stall the entire group. A turn
        measures ~300-400 tokens.
        """
        use_vllm = bool(getattr(trainer, "use_vllm", False)) and getattr(
            trainer, "vllm_generation", None
        ) is not None

        def generate_batch_fn(batch_ids: list[list[int]]) -> list[list[int]]:
            if use_vllm:
                # vLLM path. This is the reason multi-turn is affordable at all: HF generate
                # re-prefills the shared ~6.2k-token prompt for every generation of every turn
                # (~20 times per group), whereas vLLM prefix-caches it and pages the KV cache.
                # TRL has already synced the policy weights into the engine before calling the
                # rollout (GRPOTrainer._generate, rollout_func branch), so this is on-policy.
                # num_generations=1: the group's G trajectories are already separate rows here,
                # each with its own diverging tool history, so vLLM must not fan them out again.
                _prompts, completion_ids, logprobs, *_ = trainer.vllm_generation.generate(
                    prompts=batch_ids,
                    images=None,
                    num_generations=1,
                )
                # Keep the sampling logprobs. TRL's vLLM importance-sampling correction needs
                # them: the engine's sampling distribution is not identical to the training
                # model's, and without them TRL computes `old_logps - None` and dies. vLLM
                # returns per-token top-k logprobs; take the top-1 (the sampled token), which
                # is what TRL itself does on its own vLLM path.
                out = []
                for c, lp in zip(completion_ids, logprobs or []):
                    flat = [x[0] if isinstance(x, (list, tuple)) else x for x in (lp or [])]
                    out.append((list(c), [float(v) for v in flat]))
                if not out:
                    out = [(list(c), None) for c in completion_ids]
                return out

            # HF generate fallback. Cap max_new_tokens to ONE assistant turn: the trainer's
            # generation_config carries the whole-completion budget (thousands of tokens for
            # multi-turn) and HF generate runs until EVERY sequence in the batch hits EOS, so
            # leaving it uncapped lets one runaway sequence stall the group. A turn is ~350 tok.
            gen_cfg = trainer.generation_config
            previous = getattr(gen_cfg, "max_new_tokens", None)
            try:
                gen_cfg.max_new_tokens = self.per_turn_max_tokens
                completion_ids, _logprobs, _extra = trainer._generate_single_turn(
                    batch_ids, None, {}
                )
            finally:
                gen_cfg.max_new_tokens = previous
            # HF generate supplies no logprobs; the rollout fills 0.0 and TRL skips the
            # importance-sampling correction (which is exact anyway when fully on-policy).
            return [list(c) for c in completion_ids]

        return generate_batch_fn

    def __call__(self, prompts: list, trainer: Any) -> dict[str, list]:
        generate_batch_fn = self._make_generate_batch_fn(trainer)

        # Resolve every prompt to its case, then roll the whole group out together.
        items = []
        case_ids_out: list[str] = []
        for prompt in prompts:
            text = prompt if isinstance(prompt, str) else _prompt_text(prompt)
            case_id = self.prompt_to_case.get(text)
            if case_id is None:
                raise KeyError(
                    "rollout_func received a prompt with no known case_id. The prompt→case "
                    "map is built from the training dataset; a mismatch means the dataset and "
                    "the map are out of sync."
                )
            case = self.cases[case_id]
            items.append((
                case,
                self.patient_info[case_id],
                self.mock_server_factory(case),
                self.cost_tracker_factory(),
            ))
            case_ids_out.append(case_id)

        results = self.rollout.rollout_batch(items, generate_batch_fn)

        prompt_ids_out = [r.prompt_ids for r in results]
        completion_ids_out = [r.completion_ids for r in results]
        env_mask_out = [r.env_mask for r in results]
        # None unless the backend actually produced logprobs (vLLM does, HF generate does not);
        # TRL treats None as "no importance-sampling correction", which is correct on-policy.
        any_logprobs = any(any(v != 0.0 for v in r.logprobs) for r in results)
        logprobs_out = [r.logprobs for r in results] if any_logprobs else None
        rewards_out = [
            float(self.reward_fn(r.trace, self.cases[r.case_id])) for r in results
        ]
        n = max(len(results), 1)
        n_trunc = sum(1 for r in results if r.truncated)
        logger.info(
            "rollout: %d trajectories, mean turns %.1f, mean tool calls %.1f, "
            "mean reward %.3f, truncated %d/%d (%.0f%%), mean completion tokens %.0f",
            len(results),
            sum(r.num_turns for r in results) / n,
            sum(r.num_tool_calls for r in results) / n,
            sum(rewards_out) / max(len(rewards_out), 1),
            n_trunc, len(results), 100.0 * n_trunc / n,
            sum(len(r.completion_ids) for r in results) / n,
        )
        if n_trunc:
            # A high truncation rate means the completion budget is clipping real agent
            # behaviour, not just tokens — the reward still scores the whole trace, but the
            # policy only gets gradient on the prefix. Surface it rather than let it hide.
            logger.warning(
                "%d/%d trajectories hit the %d-token completion budget — consider raising "
                "max_completion_length (memory permitting) or lowering num_generations.",
                n_trunc, len(results), self.rollout.max_completion_tokens,
            )

        return {
            "prompt_ids": prompt_ids_out,
            "completion_ids": completion_ids_out,
            # On-policy, single inner iteration: the sampling logprobs equal the policy's, so
            # the importance ratio is 1 and TRL recomputes what it needs from the model. None
            # (key present) selects that path; see GRPOTrainer._generate.
            "logprobs": logprobs_out,
            # Consumed by TRL as the loss mask: 1 on the policy's own tokens, 0 on tool tokens.
            "env_mask": env_mask_out,
            # Forwarded to the reward function below.
            "trajectory_reward": rewards_out,
            "case_id": case_ids_out,
        }


class precomputed_trajectory_reward:  # noqa: N801 — TRL matches reward funcs by __name__
    """Reward function that returns the reward already computed during rollout.

    The multi-turn reward must be scored on the full :class:`AgentTrace`, which only the
    rollout holds, so it is computed there and threaded through as the ``trajectory_reward``
    extra field. TRL still requires a ``reward_funcs`` entry; this reads it back.
    """

    __name__ = "trajectory_reward"

    def __call__(
        self,
        prompts: list | None = None,
        completions: list | None = None,
        trajectory_reward: list[float] | None = None,
        **kwargs: Any,
    ) -> list[float]:
        if trajectory_reward is None:
            raise ValueError(
                "trajectory_reward reward function requires the 'trajectory_reward' field "
                "from the rollout (MultiTurnRolloutFunc emits it). Got None — the rollout "
                "func and reward func are out of sync."
            )
        return [float(r) for r in trajectory_reward]


def _prompt_text(prompt: Any) -> str:
    """Extract plain text from a conversational prompt (list of message dicts)."""
    if isinstance(prompt, list):
        return "\n".join(
            m.get("content", "") for m in prompt if isinstance(m, dict)
        )
    return str(prompt)
