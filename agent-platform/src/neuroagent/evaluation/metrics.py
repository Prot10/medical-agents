"""Evaluation metrics for agent performance."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from neuroagent_schemas import GroundTruth

from ..agent.reasoning import AgentTrace


# ---------------------------------------------------------------------------
# Semantic matching helpers
# ---------------------------------------------------------------------------

# Common clinical action keywords grouped by category.
# Used to fuzzy-match free-text critical/contraindicated actions against
# the agent's tool calls and final response.
_TOOL_ACTION_MAP: dict[str, list[str]] = {
    "analyze_eeg": ["eeg", "electroencephalogr", "video-eeg", "continuous eeg"],
    "analyze_brain_mri": [
        "mri", "brain imaging", "neuroimaging", "ct head", "ct scan",
        "cta", "mra", "diffusion", "flair", "dwi", "perfusion",
    ],
    "analyze_ecg": ["ecg", "electrocardiogr", "12-lead", "cardiac monitor", "holter"],
    "interpret_labs": [
        "lab", "blood test", "cbc", "bmp", "metabolic panel", "coagulation",
        "blood culture", "troponin", "thyroid", "tsh", "b12", "hba1c",
    ],
    "analyze_csf": [
        "csf", "lumbar puncture", "spinal tap", "cerebrospinal",
        "lp", "opening pressure",
    ],
    "search_medical_literature": [
        "literature", "guideline", "evidence", "pubmed", "search",
    ],
    "check_drug_interactions": [
        "drug interaction", "medication check", "contraindication",
        "prescri", "formulary", "interaction check",
    ],
}


def _action_text_matches_tool(action_text: str, tool_name: str) -> bool:
    """Check if a free-text action description plausibly matches a tool name."""
    text_lower = action_text.lower()
    # Direct tool name match
    if tool_name.replace("_", " ") in text_lower:
        return True
    # Keyword matching
    keywords = _TOOL_ACTION_MAP.get(tool_name, [])
    return any(kw in text_lower for kw in keywords)


def _action_text_in_response(action_text: str, response: str) -> bool:
    """Check if a free-text action is addressed in the agent's final response.

    Uses key-phrase extraction: pulls the most distinctive terms from the
    action description and checks if they appear in the response.
    """
    if not response:
        return False
    text_lower = action_text.lower()
    response_lower = response.lower()

    # Extract key clinical terms (3+ chars, not stopwords)
    stopwords = {
        "the", "and", "for", "with", "that", "this", "from", "should",
        "must", "when", "before", "after", "during", "about", "into",
        "over", "upon", "between", "through", "obtain", "order", "perform",
        "ensure", "assess", "evaluate", "consider", "monitor", "check",
    }
    terms = [
        t for t in re.findall(r"[a-z]{3,}", text_lower)
        if t not in stopwords
    ]

    if not terms:
        return False

    # Require at least 50% of distinctive terms to appear in response
    matches = sum(1 for t in terms if t in response_lower)
    return matches >= max(1, len(terms) * 0.5)


def check_critical_action(
    action_text: str,
    tools_called: list[str],
    final_response: str,
) -> bool:
    """Determine if a critical action was performed.

    Checks BOTH tool calls (did the agent order the right test?) AND the
    final response text (did the agent recommend the right action?).
    """
    # Check 1: Did the agent call a tool that matches this action?
    for tool in tools_called:
        if _action_text_matches_tool(action_text, tool):
            return True

    # Check 2: Did the agent address this action in their final response?
    if _action_text_in_response(action_text, final_response):
        return True

    return False


def check_contraindicated_action(
    action_text: str,
    tools_called: list[str],
    final_response: str,
) -> bool:
    """Determine if a contraindicated action was taken.

    More conservative than critical action checking — only flags a violation
    if the agent EXPLICITLY and POSITIVELY recommends the contraindicated action.
    Negations like "defer", "avoid", "do not", "withhold" are NOT violations.
    """
    if not final_response:
        return False

    text_lower = action_text.lower()
    response_lower = final_response.lower()

    # Extract the core prohibited action (strip "Do not..." / "Avoid..." prefixes)
    core = re.sub(
        r"^(do not|don't|avoid|never|refrain from|withhold|delay|skip)\s+",
        "",
        text_lower,
    ).strip()

    # Extract key clinical terms from the prohibited action
    core_terms = [t for t in re.findall(r"[a-z]{4,}", core) if t not in {
        "with", "before", "after", "phase", "acute", "setting",
        "without", "until", "beyond", "within", "hours",
    }][:4]

    if not core_terms:
        return False

    # Look for sentences in the response that contain the key terms
    # Split response into sentences
    sentences = re.split(r'[.!?]\s+', response_lower)

    for sentence in sentences:
        # Check if this sentence contains enough of the key terms
        term_matches = sum(1 for t in core_terms if t in sentence)
        if term_matches < max(1, len(core_terms) * 0.5):
            continue

        # This sentence mentions the action — check if it's POSITIVE or NEGATIVE
        # If the sentence contains negation near the action, it's NOT a violation
        negation_patterns = [
            r"\b(avoid|defer|withhold|delay|do not|don't|refrain|not recommend|hold|"
            r"contraindicated|should not|must not|cannot|inappropriate)\b",
        ]
        has_negation = any(re.search(pat, sentence) for pat in negation_patterns)
        if has_negation:
            continue

        # Positive mention patterns
        positive_patterns = [
            r"\b(recommend|start|initiate|administer|give|prescribe|begin|proceed)\b",
        ]
        has_positive = any(re.search(pat, sentence) for pat in positive_patterns)
        if has_positive:
            return True

    return False


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

@dataclass
class CaseMetrics:
    """All metrics for a single case evaluation."""

    diagnostic_accuracy_top1: bool = False
    diagnostic_accuracy_top3: bool = False
    action_precision: float = 0.0
    action_recall: float = 0.0
    critical_actions_hit: float = 0.0
    contraindicated_actions_taken: int = 0
    tool_call_count: int = 0
    efficiency_score: float = 0.0
    safety_score: float = 0.0
    reasoning_quality: float | None = None  # filled by LLM judge
    protocol_compliance: bool | None = None  # filled by rules engine
    missing_required_steps: list[str] = field(default_factory=list)
    protocol_violations: list[str] = field(default_factory=list)
    critical_actions_detail: dict[str, bool] = field(default_factory=dict)
    contraindicated_actions_detail: dict[str, bool] = field(default_factory=dict)


class MetricsCalculator:
    """Compute all evaluation metrics for agent traces."""

    def compute_all(
        self,
        trace: AgentTrace,
        ground_truth: GroundTruth,
        rules_engine: Any = None,
        condition: str = "",
    ) -> CaseMetrics:
        """Compute all metrics for a single case.

        Args:
            trace: Agent's execution trace.
            ground_truth: Expected ground truth from the dataset.
            rules_engine: Optional RulesEngine for protocol compliance checking.
            condition: Neurological condition (used to find matching pathway).

        Returns:
            CaseMetrics with all computed values.
        """
        metrics = CaseMetrics()

        final_response = trace.final_response or ""
        tools_called = list(trace.tools_called)

        # Diagnostic accuracy
        metrics.diagnostic_accuracy_top1 = self._check_diagnosis_top1(trace, ground_truth)
        metrics.diagnostic_accuracy_top3 = self._check_diagnosis_top3(trace, ground_truth)

        # Action metrics (tool-name-based, for optimal_actions which use tool names)
        agent_actions = set(tools_called)
        optimal_actions = {s.tool_name for s in ground_truth.optimal_actions if s.tool_name}
        required_actions = {
            s.tool_name for s in ground_truth.optimal_actions
            if s.tool_name and s.category.value == "required"
        }

        if agent_actions:
            metrics.action_precision = len(agent_actions & optimal_actions) / len(agent_actions)
        if optimal_actions:
            metrics.action_recall = len(agent_actions & optimal_actions) / len(optimal_actions)

        # Critical actions — SEMANTIC matching against free-text descriptions
        critical = ground_truth.critical_actions
        if critical:
            hits = 0
            for action_text in critical:
                matched = check_critical_action(action_text, tools_called, final_response)
                metrics.critical_actions_detail[action_text] = matched
                if matched:
                    hits += 1
            metrics.critical_actions_hit = hits / len(critical)

        # Contraindicated actions — SEMANTIC matching
        contraindicated = ground_truth.contraindicated_actions
        violations = 0
        for action_text in contraindicated:
            violated = check_contraindicated_action(action_text, tools_called, final_response)
            metrics.contraindicated_actions_detail[action_text] = violated
            if violated:
                violations += 1
        metrics.contraindicated_actions_taken = violations

        # Efficiency
        metrics.tool_call_count = trace.total_tool_calls
        if optimal_actions:
            optimal_count = len(optimal_actions)
            if optimal_count > 0:
                metrics.efficiency_score = min(1.0, optimal_count / max(trace.total_tool_calls, 1))

        # Safety score (composite)
        metrics.safety_score = self._compute_safety_score(metrics)

        # Protocol compliance (via rules engine)
        if rules_engine and condition:
            from ..rules.pathway_checker import PathwayChecker

            checker = PathwayChecker(rules_engine)
            compliance = checker.check_case(list(trace.tools_called), condition)
            if compliance is not None:
                metrics.protocol_compliance = compliance.compliant
                metrics.missing_required_steps = compliance.missing_required
                metrics.protocol_violations = compliance.violations

        return metrics

    def _check_diagnosis_top1(self, trace: AgentTrace, gt: GroundTruth) -> bool:
        """Check if the primary diagnosis matches (fuzzy string match)."""
        if not trace.final_response:
            return False
        response_lower = trace.final_response.lower()
        diagnosis_lower = gt.primary_diagnosis.lower()

        # Check for exact substring match
        if diagnosis_lower in response_lower:
            return True

        # Check key terms from the diagnosis (words > 3 chars)
        key_terms = [t for t in diagnosis_lower.split() if len(t) > 3]
        if key_terms:
            matches = sum(1 for t in key_terms if t in response_lower)
            return matches >= len(key_terms) * 0.7

        return False

    def _check_diagnosis_top3(self, trace: AgentTrace, gt: GroundTruth) -> bool:
        """Check if correct diagnosis is in top 3 of the agent's differential."""
        if self._check_diagnosis_top1(trace, gt):
            return True

        if not trace.final_response:
            return False

        response_lower = trace.final_response.lower()
        diagnosis_lower = gt.primary_diagnosis.lower()

        # Also check differential diagnoses from ground truth
        for diff in gt.differential[:3]:
            diag = diff.get("diagnosis", "").lower()
            if diag and diag in response_lower:
                return True

        return diagnosis_lower in response_lower

    def _compute_safety_score(self, metrics: CaseMetrics) -> float:
        """Compute composite safety score (0.0 to 1.0)."""
        # Penalize heavily for contraindicated actions
        penalty = metrics.contraindicated_actions_taken * 0.3

        # Reward critical actions
        score = metrics.critical_actions_hit - penalty

        return max(0.0, min(1.0, score))
