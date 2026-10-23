"""The perfect-agent check: can an agent that does exactly what the policy asks reach its ceiling?

    uv run python data/review/round-2026-10/bin/perfect_agent.py GLIO-HG-RS01 [more ids | --all] [-v]

For each case, the perfect agent performs every required and recommended criterion (its first
alternative, with the criterion's own arguments) in an order that satisfies every sequence
constraint, then submits the accepted diagnosis. The check fails when:

  * the sequence constraints are cyclic, or name an unknown criterion;
  * a call is rejected by the tool schema (out-of-vocabulary value, missing argument);
  * a call is answered by a fallback (case fallback or benchmark library) instead of the case's
    own pathway data, so the evidence the criterion expects is not actually in the case;
  * an avoided action matches a call the policy requires or recommends;
  * the score is short of 1.0 on diagnosis, required/recommended coverage, tool accuracy,
    safety, waste, sequence or stopping.

It warns when two criteria are answered with the identical stored report (usually a mis-served
study), when a later alternative of a criterion is answered by a fallback, and when a stop-rule
id is not a required criterion. `-v` prints which stored output answers each call, so you can
confirm the evidence a criterion expects is the evidence it receives.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from neuroagent.evaluation.policy_reward import ClinicalPolicyReward
from neuroagent.harness.environment import NeuroBenchEnvironment
from neuroagent_schemas import (
    ActionProposed,
    AssessmentSubmitted,
    ClinicalEpisode,
    NeuroBenchCase,
    ObservationReceived,
    SubmitAssessment,
    ToolAction,
)

CASES = Path("/Users/andrea/Documents/medical-agents/data/neurobench/cases")


def _order(criteria, constraints) -> tuple[list, list[str]]:
    """Criteria in a sequence-respecting order (stable topological sort); errors if impossible."""
    ids = [c.criterion_id for c in criteria]
    errors = [
        f"sequence constraint names unknown criterion {name!r}"
        for sc in constraints for name in (sc.before_criterion_id, sc.after_criterion_id)
        if name not in {c.criterion_id for c in criteria} and name not in ids
    ]
    after = {i: set() for i in ids}
    for sc in constraints:
        if sc.before_criterion_id in after and sc.after_criterion_id in after:
            after[sc.after_criterion_id].add(sc.before_criterion_id)
    done, ordered = set(), []
    while len(ordered) < len(ids):
        ready = [i for i in ids if i not in done and after[i] <= done]
        if not ready:
            errors.append(f"sequence constraints are cyclic among {sorted(set(ids) - done)}")
            ordered += [i for i in ids if i not in done]
            break
        ordered.append(ready[0])
        done.add(ready[0])
    by_id = {c.criterion_id: c for c in criteria}
    return [by_id[i] for i in ordered], errors


def _source(case: NeuroBenchCase, tool: str, output) -> str:
    for followup in case.followup_outputs:
        if followup.tool_name == tool and followup.output.model_dump() == output:
            return f"followup[{case.followup_outputs.index(followup)}] {followup.trigger_action}"
    initial = case.initial_tool_outputs.model_dump(exclude_none=True)
    for field, value in initial.items():
        if value == output:
            return f"initial_tool_outputs.{field}"
        if isinstance(value, dict) and output in value.values():
            return f"initial_tool_outputs.{field}[...]"
    return "?"


def _arguments(case: NeuroBenchCase, criterion, pattern, environment) -> dict:
    """The criterion's own arguments, completed with what the tool schema requires.

    A criterion names only the arguments that identify the study; the call still needs the
    tool's required fields. `clinical_context` is the criterion's label; a drug or a literature
    query the criterion leaves open is the one the case stored a result for.
    """
    arguments = dict(pattern.required_arguments)
    schema = environment.registry.get_tool(pattern.tool_name).parameter_schema
    stored = case.initial_tool_outputs
    for name in schema.get("required", []):
        if name in arguments:
            continue
        if name == "clinical_context":
            arguments[name] = criterion.label
        elif name == "drug":
            arguments[name] = next(iter(stored.drug_interactions or {}), criterion.label)
        elif name == "query":
            arguments[name] = next(iter(stored.literature_search or {}), criterion.label)
    return arguments


def check(case_id: str, verbose: bool = False) -> tuple[list[str], list[str]]:
    case = NeuroBenchCase.model_validate_json((CASES / f"{case_id}.json").read_text())
    policy = case.ground_truth
    errors: list[str] = []
    warnings: list[str] = []
    wanted = [c for c in policy.action_criteria if c.importance.value in ("required", "recommended")]
    every_id = {c.criterion_id for c in policy.action_criteria}
    for sc in policy.sequence_constraints:
        for name in (sc.before_criterion_id, sc.after_criterion_id):
            if name not in every_id:
                errors.append(f"sequence constraint names unknown criterion {name!r}")
    # Only constraints between performed criteria shape the perfect order.
    ordered, order_errors = _order(wanted, [
        sc for sc in policy.sequence_constraints
        if sc.before_criterion_id in {c.criterion_id for c in wanted}
        and sc.after_criterion_id in {c.criterion_id for c in wanted}
    ])
    errors += [e for e in order_errors if "unknown" not in e]
    required_ids = {c.criterion_id for c in policy.action_criteria if c.importance.value == "required"}
    for name in policy.stop_rule.required_before_assessment:
        if name not in required_ids:
            warnings.append(f"stop rule names {name!r}, which is not a required criterion")

    environment = NeuroBenchEnvironment(case)
    episode = ClinicalEpisode()
    served: dict[str, str] = {}
    for turn, criterion in enumerate(ordered, start=1):
        pattern = criterion.alternatives[0]
        arguments = _arguments(case, criterion, pattern, environment)
        action = ToolAction(tool_name=pattern.tool_name, arguments=arguments)
        result = environment.execute(action)
        episode.events.append(ActionProposed(turn=turn, action=action))
        episode.events.append(ObservationReceived(
            turn=turn, tool_name=pattern.tool_name, success=result.success, output=result.output,
            error_message=result.error_message, cost_usd=result.cost_usd,
            from_fallback=result.from_fallback, library=result.library, rejected=result.rejected,
        ))
        label = f"{criterion.criterion_id} ({criterion.importance.value}) {pattern.tool_name} {pattern.required_arguments}"
        if result.rejected or not result.success:
            errors.append(f"{label}: call failed: {result.error_message}")
            continue
        if result.from_fallback:
            tier = "benchmark library" if result.library else "case fallback_tool_outputs"
            errors.append(f"{label}: answered by the {tier}, not by the case's pathway data")
            continue
        source = _source(case, pattern.tool_name, result.output)
        key = json.dumps(result.output, sort_keys=True)
        if key in served:
            warnings.append(f"{label}: answered with the same stored report as {served[key]} ({source})")
        served[key] = criterion.criterion_id
        if verbose:
            print(f"  {label}\n      <- {source}")
        for avoided in policy.avoided_actions:
            if avoided.matches(action):
                errors.append(f"{label}: also matched by avoided action {avoided.criterion_id} ({avoided.severity.value})")
    # Later alternatives: each should be answerable from the case too.
    for criterion in wanted:
        for index, pattern in enumerate(criterion.alternatives[1:], start=2):
            probe = NeuroBenchEnvironment(case)
            arguments = _arguments(case, criterion, pattern, probe)
            result = probe.execute(ToolAction(tool_name=pattern.tool_name, arguments=arguments))
            if result.rejected or not result.success:
                errors.append(f"{criterion.criterion_id} alternative {index} {pattern.tool_name} {pattern.required_arguments}: call failed: {result.error_message}")
            elif result.from_fallback:
                warnings.append(f"{criterion.criterion_id} alternative {index} {pattern.tool_name} {pattern.required_arguments}: answered by a fallback")
            for avoided in policy.avoided_actions:
                if avoided.matches(ToolAction(tool_name=pattern.tool_name, arguments=arguments)):
                    errors.append(f"{criterion.criterion_id} alternative {index}: matched by avoided action {avoided.criterion_id}")
    assessment = SubmitAssessment(
        primary_diagnosis=policy.diagnosis.accepted[0],
        icd10_code=policy.diagnosis.icd_codes[0] if policy.diagnosis.icd_codes else None,
        confidence=0.9, urgency="urgent",
        recommendations=list(policy.assessment.required_recommendations),
    )
    episode.events.append(AssessmentSubmitted(turn=len(ordered) + 1, assessment=assessment))
    score = ClinicalPolicyReward(require_approved=False).score(episode, case)
    for component in ("diagnosis", "required_action_coverage", "recommended_action_coverage", "tool_accuracy",
                      "safety", "waste_avoidance", "sequence", "stopping"):
        value = getattr(score, component)
        if value < 1.0:
            errors.append(f"perfect agent scores {component} = {value:.3f}")
    if score.caps_applied:
        errors.append(f"perfect agent hits caps {score.caps_applied}")
    return errors, warnings


def main(argv: list[str]) -> int:
    verbose = "-v" in argv
    ids = [a for a in argv if not a.startswith("-")]
    if "--all" in argv:
        ids = sorted(p.stem for p in CASES.glob("*.json"))
    if not ids:
        print(__doc__)
        return 2
    failed = 0
    for case_id in ids:
        if verbose:
            print(case_id)
        errors, warnings = check(case_id, verbose)
        failed += bool(errors)
        if errors or warnings or verbose:
            print(f"{case_id}: {'FAIL' if errors else 'ok'}")
            for line in errors:
                print(f"  ERROR   {line}")
            for line in warnings:
                print(f"  warning {line}")
    print(f"{len(ids) - failed}/{len(ids)} cases pass the perfect-agent check")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
