"""Check the gold trajectories against the live tool contract and their own cases.

The trajectories were written by a teacher against the tool schemas as they were at
generation time. When a tool's parameters or enums change, the trajectories become training
data for a tool that no longer exists in that shape — and nothing would tell you: SFT would
happily train on it.

This is the gate. Every tool call in every trajectory must:

* name a tool in the registry
* carry only arguments that tool accepts, and every argument the tool requires
* use legal enum values, and closed-vocabulary values for the two catchall tools
* target a tool the trajectory's own case can actually answer (MockServer has an output)
* never call a tool the case marks useless or harmful

It also scores each trajectory with the real `MetricsCalculator`, because a trajectory that
passes the schema check can still teach the wrong lesson: a useless call, a harmful call, or
the wrong diagnosis.

Usage:
    uv run python agent-platform/scripts/validation/check_trajectories.py
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_cases import CASES_DIR, CATCHALL_PARAM, _tool_schemas  # noqa: E402

from neuroagent.agent.reasoning import AgentTrace, AgentTurn  # noqa: E402
from neuroagent.evaluation.metrics import MetricsCalculator  # noqa: E402
from neuroagent.tools.mock_server import MockServer  # noqa: E402
from neuroagent_schemas import NeuroBenchCase  # noqa: E402

DEFAULT_TRAJECTORIES = Path("training_data/gold_trajectories/trajectories.jsonl")

# Shared with validate_cases so each discriminating parameter is checked against ITS OWN
# closed vocabulary. This file had the same dispatch bug: everything that was not
# order_advanced_imaging was validated against the specialized-test list.
CATCHALL = {tool: key for tool, (key, _) in CATCHALL_PARAM.items()}


def _load_cases(cases_dir: Path) -> dict[str, NeuroBenchCase]:
    cases = {}
    for path in cases_dir.glob("*.json"):
        case = NeuroBenchCase.model_validate(json.loads(path.read_text()))
        cases[case.case_id] = case
    return cases


def _tool_calls(trajectory: dict) -> list[tuple[str, dict]]:
    return [
        (call["function"]["name"], call["function"].get("arguments") or {})
        for message in trajectory["messages"]
        for call in (message.get("tool_calls") or [])
    ]


def check_trajectory(
    trajectory: dict, case: NeuroBenchCase, schemas: dict
) -> list[str]:
    """Every way a trajectory can disagree with the tools or with its own case."""
    issues: list[str] = []
    banned = {t.tool_name for t in case.ground_truth.useless_tools}
    banned |= {t.tool_name for t in case.ground_truth.harmful_tools}
    optimal = {a.tool_name for a in case.ground_truth.optimal_actions if a.tool_name}
    banned -= optimal  # useless/harmful are parameter-scoped; a required tool is not banned

    mock = MockServer(case)

    for tool, arguments in _tool_calls(trajectory):
        if tool not in schemas:
            issues.append(f"unknown tool `{tool}`")
            continue

        params = schemas[tool].get("properties", {})
        for key in arguments:
            if key not in params:
                issues.append(f"{tool}: unknown argument `{key}`")
        for key in schemas[tool].get("required", []):
            if key not in arguments:
                issues.append(f"{tool}: missing required argument `{key}`")

        for key, value in arguments.items():
            if key not in params:
                continue
            if tool in CATCHALL and key == CATCHALL[tool]:
                if not CATCHALL_PARAM[tool][1](str(value)):
                    issues.append(f"{tool}.{key}=`{value}` is not in the closed vocabulary")
            elif (enum := params[key].get("enum")) and value not in enum:
                issues.append(f"{tool}.{key}=`{value}` not in {enum}")

        if tool in banned:
            issues.append(f"calls `{tool}`, which this case marks useless/harmful")

        if not mock.get_output(tool, arguments).success:
            issues.append(f"`{tool}` has no output in this case; the agent would get an error")

    calls = _tool_calls(trajectory)
    repeated = sorted({t for t, _ in calls if [n for n, _ in calls].count(t) > 1})
    if repeated:
        issues.append(f"tool called more than once: {repeated}")

    return issues


def _as_trace(trajectory: dict) -> AgentTrace:
    turns, names = [], []
    for i, message in enumerate(trajectory["messages"]):
        if message["role"] != "assistant":
            continue
        calls = message.get("tool_calls") or []
        names += [c["function"]["name"] for c in calls]
        turns.append(AgentTurn(turn_number=i, role="assistant", content=message["content"],
                               tool_calls=calls or None))
    trace = AgentTrace(case_id=trajectory["case_id"], turns=turns)
    trace.tools_called = names
    trace.total_tool_calls = len(names)
    trace.set_final_response(trajectory["messages"][-1]["content"])
    return trace


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the gold trajectories")
    parser.add_argument("--data", default=str(DEFAULT_TRAJECTORIES))
    parser.add_argument("--cases-dir", default=str(CASES_DIR))
    parser.add_argument("--show", type=int, default=10)
    args = parser.parse_args()

    schemas = _tool_schemas()
    cases = _load_cases(Path(args.cases_dir))
    calculator = MetricsCalculator()

    trajectories = [json.loads(l) for l in Path(args.data).read_text().splitlines() if l.strip()]
    failures: list[tuple[str, list[str]]] = []
    codes: Counter[str] = Counter()

    top1 = useless = harmful = 0
    recall: list[float] = []
    coverage: list[float] = []

    for trajectory in trajectories:
        case = cases[trajectory["case_id"]]
        stem = f"{trajectory['case_id']}_{trajectory.get('style', '?')}"

        issues = check_trajectory(trajectory, case, schemas)
        if issues:
            failures.append((stem, issues))
            for issue in issues:
                codes[issue.split(":")[0].split("`")[0].strip() or "issue"] += 1

        metrics = calculator.compute_all(_as_trace(trajectory), case.ground_truth)
        top1 += bool(metrics.diagnostic_accuracy_top1)
        useless += metrics.useless_calls
        harmful += metrics.harmful_calls
        recall.append(metrics.action_recall)
        coverage.append(metrics.required_coverage)

    n = len(trajectories)
    print(f"{n - len(failures)}/{n} trajectories satisfy the tool contract")
    print()
    print("Scored with the real metrics:")
    print(f"  diagnostic_accuracy_top1 : {top1}/{n}")
    print(f"  useless_calls            : {useless}")
    print(f"  harmful_calls            : {harmful}")
    print(f"  action_recall     mean   : {statistics.mean(recall):.3f}")
    print(f"  required_coverage mean   : {statistics.mean(coverage):.3f} "
          f"({sum(1 for c in coverage if c == 1.0)} at 1.0)")

    if failures:
        print(f"\nContract failures ({len(failures)}):")
        for stem, issues in failures[: args.show]:
            print(f"  {stem}: {issues[0]}")
        if len(failures) > args.show:
            print(f"  ... and {len(failures) - args.show} more")

    # A gold trajectory that demonstrates a useless or harmful call, or the wrong diagnosis,
    # is worse than no trajectory: SFT would teach it.
    fatal = bool(failures) or useless or harmful or top1 != n
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
