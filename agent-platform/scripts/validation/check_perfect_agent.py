"""Score a synthetic *perfect* agent against every case. The strongest end-to-end proof.

For each case we construct the trace of an agent that does exactly what the ground truth
says: it calls every callable optimal action, with the ground truth's own parameters, and
nothing else. Such an agent must score

    action_recall == 1.0, required_coverage == 1.0, useless_calls == 0, harmful_calls == 0

If it does not, the case and the metric layer disagree, and every model evaluated against
that case is being scored against an unreachable ceiling.

Before this migration that assertion failed for 332 of 600 cases:
  * 229 cases named `consult_medical_specialist` in optimal_actions — a tool the registry
    does not have, so recall could never reach 1.0
  * 103 cases marked a tool useless by name while also requiring it with different
    parameters, so a perfect agent was charged with a useless call

Usage:
    uv run python agent-platform/scripts/validation/check_perfect_agent.py
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_cases import CASES_DIR, _tool_schemas  # noqa: E402

from neuroagent.agent.reasoning import AgentTrace, AgentTurn  # noqa: E402
from neuroagent.evaluation.metrics import MetricsCalculator  # noqa: E402
from neuroagent_schemas import NeuroBenchCase  # noqa: E402


def perfect_trace(case: NeuroBenchCase, schemas: dict) -> AgentTrace:
    """The trace of an agent that performs exactly the callable optimal actions."""
    calls, names = [], []
    for step in case.ground_truth.optimal_actions:
        if not step.tool_name or step.tool_name not in schemas:
            continue  # a clinical action with no tool call
        names.append(step.tool_name)
        calls.append({
            "function": {"name": step.tool_name, "arguments": dict(step.tool_parameters or {})}
        })

    turns = [AgentTurn(turn_number=1, role="assistant", tool_calls=calls)] if calls else []
    trace = AgentTrace(case_id=case.case_id, turns=turns)
    trace.tools_called = names
    trace.total_tool_calls = len(names)
    trace.set_final_response(
        f"### Primary Diagnosis\n{case.ground_truth.primary_diagnosis} (Confidence: 0.95)"
    )
    return trace


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a perfect agent on every case")
    parser.add_argument("--cases-dir", default=str(CASES_DIR))
    parser.add_argument("--show", type=int, default=10, help="How many failures to print")
    args = parser.parse_args()

    schemas = _tool_schemas()
    calculator = MetricsCalculator()
    failures: list[tuple[str, str]] = []
    reasons: Counter[str] = Counter()
    n = 0

    for path in sorted(Path(args.cases_dir).glob("*.json")):
        case = NeuroBenchCase.model_validate(json.loads(path.read_text()))
        n += 1
        metrics = calculator.compute_all(perfect_trace(case, schemas), case.ground_truth)

        problems = []
        if case.ground_truth.optimal_actions and metrics.action_recall < 1.0:
            problems.append(f"action_recall={metrics.action_recall:.3f}")
        if metrics.required_total and metrics.required_coverage < 1.0:
            problems.append(f"required_coverage={metrics.required_coverage:.3f}")
        if metrics.useless_calls:
            problems.append(f"useless_calls={metrics.useless_calls}")
        if metrics.harmful_calls:
            problems.append(f"harmful_calls={metrics.harmful_calls}")

        if problems:
            failures.append((case.case_id, ", ".join(problems)))
            for p in problems:
                reasons[p.split("=")[0]] += 1

    print(f"perfect agent scored on {n} cases")
    print(f"  cases where it is NOT perfect: {len(failures)}")
    if reasons:
        print(f"  by metric: {dict(reasons)}")
    for case_id, why in failures[: args.show]:
        print(f"    {case_id}: {why}")
    if len(failures) > args.show:
        print(f"    ... and {len(failures) - args.show} more")

    if failures:
        return 1
    print("\nEvery case is reachable: a perfect agent scores 1.0 recall, 1.0 required "
          "coverage, 0 useless, 0 harmful.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
