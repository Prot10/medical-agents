"""Online reward function for GRPO/DAPO training.

Parses tool calls and the final assessment out of a model-generated completion,
assembles a pseudo :class:`AgentTrace`, and scores it with the SAME
``CompositeReward`` → ``MetricsCalculator`` pipeline used by evaluation and
gold-trajectory selection. This module contains only the RL-specific plumbing
(completion text → pseudo-trace); every scoring decision — diagnosis matching,
tool precision/recall, safety, cost, compliance, format — is delegated to the
shared implementation, with weights loaded from
``config/training/reward_weights.yaml`` via ``CompositeReward.from_config``.

Case lookup is by explicit ``case_id``: each training example carries a
``case_id`` column (emitted by ``format_for_grpo``), which TRL's GRPOTrainer
forwards to reward functions as a kwarg. There is no prompt-prefix or fuzzy
matching — a missing case_id raises, it never silently scores 0.0.
"""

from __future__ import annotations

import ast
import json
import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from neuroagent_schemas import NeuroBenchCase

    from ...agent.reasoning import AgentTrace
    from .composite_reward import CompositeReward


_XML_FUNCTION = re.compile(
    r"<function=([a-zA-Z_][\w]*)>(.*?)</function>", re.DOTALL
)
_XML_PARAMETER = re.compile(
    r"<parameter=([a-zA-Z_][\w]*)>(.*?)</parameter>", re.DOTALL
)


def _coerce(value: str) -> Any:
    """Type an XML parameter body the way the tool schema expects it.

    qwen3_coder emits Python literals, not JSON — `True`, not `true` — so a plain
    json.loads leaves booleans as the strings "True"/"False". That matters: `contrast` is a
    boolean in the tool schema and it changes what an MRI costs, so a string would be priced
    wrong. Try JSON first (numbers, lists, objects), then Python literals, then give up and
    keep the raw string (which is right for free-text fields like clinical_context).
    """
    v = value.strip()
    try:
        return json.loads(v)
    except (json.JSONDecodeError, ValueError):
        pass
    try:
        return ast.literal_eval(v)
    except (ValueError, SyntaxError, MemoryError, RecursionError):
        return v


def extract_tool_calls(completion: str) -> list[dict[str, Any]]:
    """Extract tool calls from a model-generated completion.

    Qwen3.5 is served with `--tool-call-parser qwen3_coder`, and that is the syntax it
    actually generates — an XML function block, NOT a JSON object:

        <tool_call>
        <function=analyze_brain_mri>
        <parameter=clinical_context>progressive bulbar weakness</parameter>
        <parameter=contrast>True</parameter>
        </function>
        </tool_call>

    Parsing only the JSON form silently returns [] for every real Qwen3.5 completion, which
    hands the online reward an empty `tools_called` — so actions, cost, safety and
    compliance all score zero and GRPO optimises a reward that gives no credit for ordering
    the right test. The XML form is therefore tried first; the JSON forms are kept for other
    models and for hand-written fixtures.
    """
    tool_calls: list[dict[str, Any]] = []

    # Pattern 1: qwen3_coder XML — what Qwen3.5 emits.
    for fn in _XML_FUNCTION.finditer(completion):
        tool_calls.append({
            "tool_name": fn.group(1),
            "parameters": {
                p.group(1): _coerce(p.group(2))
                for p in _XML_PARAMETER.finditer(fn.group(2))
            },
        })
    if tool_calls:
        return tool_calls

    # Pattern 2: <tool_call>{"name": ..., "arguments": {...}}</tool_call>
    for match in re.finditer(
        r"<tool_call>\s*(\{.*?\})\s*</tool_call>", completion, re.DOTALL
    ):
        try:
            tc = json.loads(match.group(1))
            args = tc.get("arguments", {})
            tool_calls.append({
                "tool_name": tc.get("name", ""),
                "parameters": args if isinstance(args, dict) else {},
            })
        except json.JSONDecodeError:
            continue

    # Pattern 3: OpenAI-style function calls in raw JSON
    if not tool_calls:
        for match in re.finditer(
            r'"name"\s*:\s*"([a-z_]+)".*?"arguments"\s*:\s*(\{[^}]*\})',
            completion, re.DOTALL,
        ):
            try:
                args = json.loads(match.group(2))
                tool_calls.append({
                    "tool_name": match.group(1),
                    "parameters": args if isinstance(args, dict) else {},
                })
            except json.JSONDecodeError:
                tool_calls.append({
                    "tool_name": match.group(1),
                    "parameters": {},
                })

    return tool_calls


_TOOL_BLOCKS = re.compile(
    r"<tool_call>.*?</tool_call>|<tool_response[^>]*>.*?</tool_response>",
    re.DOTALL,
)
_THINK_BLOCKS = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def build_pseudo_trace(completion: str, case_id: str) -> AgentTrace:
    """Assemble an :class:`AgentTrace` from a raw single-shot RL completion.

    The trace carries exactly what ``MetricsCalculator`` / ``CompositeReward``
    read: ``tools_called``, per-turn structured ``tool_calls`` (so
    parameter-scoped useless/harmful classifications match), the CostTracker
    total, and a ``final_response`` built to MATCH the serving path — the
    committed assessment, with the reasoning scratchpad removed.

    The scratchpad removal is the load-bearing detail. The GRPO prompt pre-opens
    ``<think>``, so a completion begins mid-thought and the committed text is
    everything after the first ``</think>``; ``_extract_assessment`` then pulls
    the ``### Primary Diagnosis`` section, exactly as the orchestrator does at
    inference. Keeping ``<think>`` here (the old behaviour) let the safety and
    critical-action matchers read plan text out of the scratchpad and hand full
    credit to a completion that ordered nothing — reward that then scored zero at
    eval, which is why the training reward rose while the eval stayed flat.
    """
    from ...agent.orchestrator import _extract_assessment
    from ...agent.reasoning import AgentTrace, AgentTurn
    from ...tools.cost_tracker import CostTracker

    calls = extract_tool_calls(completion)
    tools_called = [c["tool_name"] for c in calls if c["tool_name"]]

    turns = []
    if calls:
        turns.append(
            AgentTurn(
                turn_number=1,
                role="assistant",
                content=None,
                tool_calls=[
                    {"function": {"name": c["tool_name"], "arguments": c["parameters"]}}
                    for c in calls
                ],
            )
        )

    # The committed answer: drop the leading (prompt-opened) think, then any closed
    # think blocks, then tool blocks, then extract the assessment section — the same
    # text the orchestrator stores as final_response at inference.
    body = completion.split("</think>", 1)[1] if "</think>" in completion else completion
    body = _THINK_BLOCKS.sub(" ", body)
    final_response = _extract_assessment(_TOOL_BLOCKS.sub("", body).strip())

    tracker = CostTracker()
    for c in calls:
        try:
            tracker.compute_cost(c["tool_name"], c.get("parameters", {}))
        except Exception:  # unknown tool name — costs nothing, format reward penalises it
            continue

    return AgentTrace(
        case_id=case_id,
        turns=turns,
        final_response=final_response,
        total_tool_calls=len(tools_called),
        tools_called=tools_called,
        total_cost_usd=tracker.total_cost_usd,
    )


class OnlineRewardFunction:
    """Score model-generated completions with the shared ``CompositeReward``.

    Used as ``reward_funcs`` in TRL's GRPOTrainer. For each generated
    completion, it:

    1. Reads the ``case_id`` kwarg TRL forwards from the dataset column.
    2. Parses tool calls + final assessment into a pseudo ``AgentTrace``.
    3. Delegates scoring to ``CompositeReward`` (→ ``MetricsCalculator``),
       the exact scorer used by evaluation and gold-trajectory selection,
       with weights from ``config/training/reward_weights.yaml``.

    A missing case_id (no column, or an id with no loaded case) raises —
    it is a data-plumbing bug, never a 0.0 reward.
    """

    # TRL GRPOTrainer expects reward_funcs to have __name__
    __name__ = "online_reward"

    def __init__(
        self,
        cases: dict[str, NeuroBenchCase],
        composite: CompositeReward,
    ):
        """
        Args:
            cases: Mapping case_id → ``NeuroBenchCase`` (see ``load_cases_by_id``).
            composite: The shared composite reward (build with
                ``CompositeReward.from_config`` so the weights come from
                ``config/training/reward_weights.yaml``).
        """
        self.cases = cases
        self.composite = composite

    def __call__(
        self,
        prompts: list | None = None,
        completions: list | None = None,
        case_id: list[str] | None = None,
        **kwargs,
    ) -> list[float]:
        """Score a batch of completions. Compatible with TRL reward_funcs API."""
        if completions is None:
            raise ValueError("online_reward called with completions=None")
        if case_id is None:
            raise ValueError(
                "online_reward requires a 'case_id' dataset column. Each training "
                "example must carry its NeuroBench case_id (format_for_grpo emits it; "
                "TRL forwards extra dataset columns to reward functions as kwargs). "
                "Refusing to score without it — prompt-prefix matching was removed."
            )
        if len(case_id) != len(completions):
            raise ValueError(
                f"case_id/completions length mismatch: {len(case_id)} vs {len(completions)}"
            )

        # Dynamic weight scheduling, if configured: derive the epoch from TRL's
        # trainer_state kwarg (1-based, matching reward_weights.yaml phases).
        epoch = None
        state = kwargs.get("trainer_state")
        if state is not None and getattr(state, "epoch", None) is not None:
            epoch = int(state.epoch) + 1

        rewards = []
        for cid, completion in zip(case_id, completions):
            case = self.cases.get(cid)
            if case is None:
                raise KeyError(
                    f"No NeuroBench case loaded for case_id={cid!r}. The training "
                    "dataset references a case the reward function cannot see — "
                    "check the dataset directory passed to load_cases_by_id()."
                )
            trace = build_pseudo_trace(self._extract_text(completion), cid)
            rewards.append(self.composite.compute(trace, case, epoch=epoch))
        return rewards

    @staticmethod
    def _extract_text(item: str | list | dict) -> str:
        """Extract plain text from TRL's prompt/completion format.

        TRL may pass:
        - str: plain text
        - list[dict]: [{"role": "assistant", "content": "..."}, ...]
        - dict: {"role": "assistant", "content": "..."}
        """
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return item.get("content", str(item))
        if isinstance(item, list):
            parts = []
            for msg in item:
                if isinstance(msg, dict):
                    parts.append(msg.get("content", ""))
                else:
                    parts.append(str(msg))
            return "\n".join(parts)
        return str(item)


def load_cases_by_id(
    dataset_path: str | Path,
    case_ids: set[str] | None = None,
) -> dict[str, NeuroBenchCase]:
    """Load NeuroBench cases keyed by case_id for explicit reward lookup.

    Args:
        dataset_path: Dataset root (containing ``cases/``).
        case_ids: If given, load only these cases and raise if any is missing —
            training must not start with silently unscorable examples.
    """
    from neuroagent_schemas import NeuroBenchCase

    cases_dir = Path(dataset_path) / "cases"
    if not cases_dir.exists():
        raise FileNotFoundError(f"Cases directory not found: {cases_dir}")

    mapping: dict[str, NeuroBenchCase] = {}
    if case_ids is not None:
        missing = []
        for cid in sorted(case_ids):
            cf = cases_dir / f"{cid}.json"
            if not cf.exists():
                missing.append(cid)
                continue
            mapping[cid] = NeuroBenchCase.model_validate(json.loads(cf.read_text()))
        if missing:
            raise FileNotFoundError(
                f"{len(missing)} case_id(s) in the training data have no case file "
                f"under {cases_dir} (e.g. {missing[:3]})"
            )
    else:
        for cf in sorted(cases_dir.glob("*.json")):
            case = NeuroBenchCase.model_validate(json.loads(cf.read_text()))
            mapping[case.case_id] = case

    logger.info("Loaded %d cases for online reward lookup", len(mapping))
    return mapping
