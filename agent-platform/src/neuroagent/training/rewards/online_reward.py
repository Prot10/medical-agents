"""Online reward function for GRPO/DAPO training.

Parses tool calls from model-generated completions, executes them against
MockServer to get realistic outputs, then scores with CompositeReward.

This bridges the gap between pre-computed offline rewards (which can't score
novel completions) and the full agent loop (which is too slow for RL training).

The key insight: during GRPO, the model generates NEW completions that don't
match any pre-computed trajectory. We need to score them on-the-fly by:
1. Extracting tool calls from the raw completion text
2. Looking up the case data for the prompt
3. Computing the composite reward (diagnosis accuracy + cost + safety)
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def extract_tool_calls(completion: str) -> list[dict[str, Any]]:
    """Extract tool calls from a model-generated completion.

    Handles both Qwen <tool_call> format and raw JSON tool calls.
    """
    tool_calls = []

    # Pattern 1: <tool_call>{"name": ..., "arguments": ...}</tool_call>
    for match in re.finditer(
        r"<tool_call>\s*(\{.*?\})\s*</tool_call>", completion, re.DOTALL
    ):
        try:
            tc = json.loads(match.group(1))
            tool_calls.append({
                "tool_name": tc.get("name", ""),
                "parameters": tc.get("arguments", {}),
            })
        except json.JSONDecodeError:
            continue

    # Pattern 2: OpenAI-style function calls in JSON
    if not tool_calls:
        for match in re.finditer(
            r'"name"\s*:\s*"([a-z_]+)".*?"arguments"\s*:\s*(\{[^}]*\})',
            completion, re.DOTALL,
        ):
            try:
                args = json.loads(match.group(2))
                tool_calls.append({
                    "tool_name": match.group(1),
                    "parameters": args,
                })
            except json.JSONDecodeError:
                tool_calls.append({
                    "tool_name": match.group(1),
                    "parameters": {},
                })

    return tool_calls


def extract_diagnosis(completion: str) -> str | None:
    """Extract the primary diagnosis from a completion's final assessment."""
    match = re.search(
        r"###?\s*Primary Diagnosis\s*\n+(.+?)(?:\n|$)", completion, re.IGNORECASE
    )
    if match:
        diag = match.group(1).strip()
        # Remove confidence annotation
        diag = re.sub(r"\(Confidence:?\s*[\d.]+\)", "", diag).strip()
        return diag
    return None


def extract_differential(completion: str) -> list[str]:
    """Extract differential diagnoses from a completion."""
    diffs = []
    match = re.search(
        r"###?\s*Differential\s*(?:Diagnos[ei]s)?\s*\n(.+?)(?=###|\Z)",
        completion, re.IGNORECASE | re.DOTALL,
    )
    if match:
        for line in match.group(1).strip().split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                # "1. Diagnosis - reason"
                diag = re.sub(r"^\d+\.\s*", "", line)
                diag = diag.split(" - ")[0].split(" — ")[0].strip()
                if diag:
                    diffs.append(diag)
    return diffs


class OnlineRewardFunction:
    """Score model-generated completions using case data + composite reward.

    Used as ``reward_funcs`` in TRL's GRPOTrainer. For each generated
    completion, it:
    1. Maps the prompt back to the NeuroBench case
    2. Extracts tool calls and diagnosis from the completion
    3. Computes a composite reward (correctness + cost + safety + format)

    This enables the model to learn from its OWN generated trajectories,
    not just pre-computed ones.
    """

    # Valid tool names for format checking
    VALID_TOOLS = frozenset({
        "analyze_eeg", "analyze_brain_mri", "analyze_ecg", "interpret_labs",
        "analyze_csf", "search_medical_literature", "check_drug_interactions",
        "order_ct_scan", "order_echocardiogram", "order_cardiac_monitoring",
        "order_advanced_imaging", "order_specialized_test",
    })

    # TRL GRPOTrainer expects reward_funcs to have __name__
    __name__ = "online_reward"

    def __init__(
        self,
        cases: dict[str, Any],
        cost_tracker: Any | None = None,
        weights: dict[str, float] | None = None,
    ):
        """
        Args:
            cases: Dict mapping prompt text (or prefix) → NeuroBenchCase data.
                   Built by ``build_prompt_to_case_mapping()``.
            cost_tracker: CostTracker instance for parameter-aware costs.
            weights: Reward component weights. Defaults balance accuracy and cost.
        """
        self.cases = cases
        self.cost_tracker = cost_tracker
        self._logged_first = False
        self.weights = weights or {
            "correctness": 0.35,
            "tool_precision": 0.15,
            "tool_recall": 0.15,
            "cost_efficiency": 0.15,
            "format": 0.10,
            "safety": 0.10,
        }

    def __call__(
        self,
        prompts: list[str] | None = None,
        completions: list[str] | None = None,
        **kwargs,
    ) -> list[float]:
        """Score a batch of completions. Compatible with TRL reward_funcs API."""
        if prompts is None or completions is None:
            logger.warning("Reward called with None prompts/completions")
            return []

        if not self._logged_first:
            self._logged_first = True
            p = prompts[0] if prompts else "NONE"
            c = completions[0] if completions else "NONE"
            logger.warning(
                "REWARD FIRST CALL: prompt_type=%s prompt[:150]=%s... completion[:150]=%s...",
                type(p).__name__,
                str(p)[:150].replace('\n', ' '),
                str(c)[:150].replace('\n', ' '),
            )

        rewards = []
        for prompt, completion in zip(prompts, completions):
            try:
                # TRL v0.29 passes prompts/completions as message lists or strings
                prompt_text = self._extract_text(prompt)
                completion_text = self._extract_text(completion)
                reward = self._score_one(prompt_text, completion_text)
            except Exception as e:
                logger.warning("Reward computation failed: %s", e)
                reward = 0.0
            rewards.append(reward)
        return rewards

    @staticmethod
    def _extract_text(item: str | list | dict) -> str:
        """Extract plain text from TRL's prompt/completion format.

        TRL v0.29 may pass:
        - str: plain text
        - list[dict]: [{"role": "user", "content": "..."}, ...]
        - dict: {"role": "assistant", "content": "..."}
        """
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return item.get("content", str(item))
        if isinstance(item, list):
            # Concatenate all message contents
            parts = []
            for msg in item:
                if isinstance(msg, dict):
                    parts.append(msg.get("content", ""))
                else:
                    parts.append(str(msg))
            return "\n".join(parts)
        return str(item)

    def _score_one(self, prompt: str, completion: str) -> float:
        """Score a single completion against its case ground truth."""
        # Find the case for this prompt
        case_data = self._lookup_case(prompt)
        if case_data is None:
            return 0.0

        gt = case_data["ground_truth"]

        # Extract model outputs
        tool_calls = extract_tool_calls(completion)
        stated_diagnosis = extract_diagnosis(completion)
        stated_differential = extract_differential(completion)
        tools_called = [tc["tool_name"] for tc in tool_calls]

        # Ground truth references
        gt_diagnosis = gt["primary_diagnosis"]
        optimal_tools = {
            a["tool_name"] for a in gt.get("optimal_actions", [])
            if a.get("tool_name")
        }
        required_tools = {
            a["tool_name"] for a in gt.get("optimal_actions", [])
            if a.get("tool_name") and a.get("category") in ("required", "ActionCategory.REQUIRED")
        }
        contraindicated = gt.get("contraindicated_actions", [])

        w = self.weights
        score = 0.0

        # 1. Correctness: Does the diagnosis match?
        if stated_diagnosis:
            gt_terms = {t.lower() for t in gt_diagnosis.split() if len(t) > 3}
            stated_terms = {t.lower() for t in stated_diagnosis.split() if len(t) > 3}
            overlap = gt_terms & stated_terms
            if len(gt_terms) > 0:
                match_ratio = len(overlap) / len(gt_terms)
                if match_ratio >= 0.6:
                    score += w["correctness"] * 1.0  # strong match
                elif match_ratio >= 0.3:
                    score += w["correctness"] * 0.5  # partial
            # Bonus for differential containing correct diagnosis
            for diff_diag in stated_differential[:3]:
                diff_terms = {t.lower() for t in diff_diag.split() if len(t) > 3}
                if len(gt_terms & diff_terms) / max(len(gt_terms), 1) >= 0.5:
                    score += w["correctness"] * 0.1
                    break

        # 2. Tool precision: Did the model avoid unnecessary tools?
        called_set = set(tools_called)
        if called_set:
            relevant = called_set & optimal_tools
            precision = len(relevant) / len(called_set)
            score += w["tool_precision"] * precision
        else:
            score += 0.0  # No tools called = 0 precision

        # 3. Tool recall: Did the model call required tools?
        if required_tools:
            hit = called_set & required_tools
            recall = len(hit) / len(required_tools)
            score += w["tool_recall"] * recall

        # 4. Cost efficiency
        if self.cost_tracker and optimal_tools:
            self.cost_tracker.reset()
            actual_cost = 0.0
            for tc in tool_calls:
                entry = self.cost_tracker.compute_cost(tc["tool_name"], tc.get("parameters", {}))
                actual_cost += entry.cost_usd

            self.cost_tracker.reset()
            optimal_cost = 0.0
            for a in gt.get("optimal_actions", []):
                if a.get("tool_name"):
                    entry = self.cost_tracker.compute_cost(
                        a["tool_name"], a.get("tool_parameters", {})
                    )
                    optimal_cost += entry.cost_usd

            if optimal_cost > 0:
                ratio = min(actual_cost / optimal_cost, 3.0)  # cap at 3x
                efficiency = max(0.0, 1.0 - (ratio - 1.0))  # 1.0 at optimal, 0 at 2x
                score += w["cost_efficiency"] * efficiency
            elif actual_cost == 0:
                score += w["cost_efficiency"]  # Both zero = perfect
        else:
            # Flat cost approximation
            score += w["cost_efficiency"] * 0.5

        # 5. Format: Proper structure?
        has_diagnosis = "Primary Diagnosis" in completion
        has_differential = "Differential" in completion
        has_tool_calls = len(tool_calls) > 0
        valid_tools = all(tc["tool_name"] in self.VALID_TOOLS for tc in tool_calls)

        format_score = (
            (0.3 if has_diagnosis else 0.0)
            + (0.2 if has_differential else 0.0)
            + (0.2 if has_tool_calls else 0.0)
            + (0.3 if valid_tools else 0.0)
        )
        score += w["format"] * format_score

        # 6. Safety: Check for contraindicated actions
        safety = 1.0
        completion_lower = completion.lower()
        for contra in contraindicated:
            # Check if the model recommended something contraindicated
            contra_terms = [t.lower() for t in contra.split() if len(t) > 4]
            # Only penalize if it appears in recommendations (not in "avoid" context)
            if any(t in completion_lower for t in contra_terms[:3]):
                # Check if it's in a warning/avoid context
                if not any(neg in completion_lower for neg in ["do not", "avoid", "contraindicated", "should not"]):
                    safety -= 0.3
        safety = max(0.0, safety)
        score += w["safety"] * safety

        # Clamp to [-1, 1]
        return max(-1.0, min(1.0, score))

    def _lookup_case(self, prompt: str) -> dict[str, Any] | None:
        """Find the NeuroBench case matching this prompt."""
        # Try exact prefix match
        prefix = prompt[:200]
        if prefix in self.cases:
            return self.cases[prefix]

        # Try fuzzy match on patient demographics
        for key, case_data in self.cases.items():
            if key[:100] in prompt[:200] or prompt[:100] in key[:200]:
                return case_data

        logger.warning("Could not find case for prompt: %s...", prompt[:80])
        return None


def build_prompt_to_case_mapping(
    dataset_path: str | Path,
    max_cases: int | None = None,
) -> dict[str, dict[str, Any]]:
    """Build a mapping from prompt text prefix → case data for reward lookup.

    This loads all NeuroBench cases and formats their patient info as prompts,
    then stores the full case data (including ground truth) for reward computation.
    """
    import json as _json
    from pathlib import Path as _Path

    dataset_path = _Path(dataset_path)
    cases_dir = dataset_path / "cases"
    mapping: dict[str, dict[str, Any]] = {}

    case_files = sorted(cases_dir.glob("*.json"))
    if max_cases:
        case_files = case_files[:max_cases]

    for cf in case_files:
        case_data = _json.loads(cf.read_text())

        # Build the prompt text that the model will see
        p = case_data["patient"]
        parts = [
            f"Patient: {p['demographics']['age']}-year-old {p['demographics']['sex']}",
            f"Chief complaint: {p['chief_complaint']}",
        ]
        prompt_text = "\n".join(parts)

        # Store by prefix for lookup
        mapping[prompt_text[:200]] = case_data

    return mapping
