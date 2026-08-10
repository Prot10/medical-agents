"""Validate every NeuroBench case against the live tool contract and its own coherence.

Merges three validators that were deleted in `c44993b` (recover with
`git show c44993b^:agent-platform/scripts/<name>.py`) and fixes their two known smells:
the canonical tool set is now read from `ToolRegistry` instead of a hardcoded literal, and
the closed vocabulary is read from `costs.yaml` via `tools/vocabulary.py`. A term therefore
cannot exist in the benchmark without also having a price and a tool that can order it.

What "correct" means here:

* `tool_name` is a live tool, or `null` for a clinical step with no tool (e.g. a specialist
  referral — the consult tool was removed in `64d4091`).
* `tool_parameters` keys are either schema properties of that tool, or documented
  descriptive annotations (`ANNOTATION_KEYS`). Ground-truth parameters are annotations of
  intent, not complete calls, so a missing `clinical_context` is fine; an unknown key is not.
* Enum-typed parameters carry legal values; the two catchall tools carry closed-vocabulary
  values.
* `optimal_actions`, `useless_tools` and `harmful_tools` never contradict each other. The
  comparison is on `(tool_name, tool_parameters)`, not on the name: a case may legitimately
  require `order_advanced_imaging{modality: FDG_PET}` and condemn `{modality: MR_spectroscopy}`.
* A `required` action has a stored output, a `useless` tool has a fallback output, sequence
  constraints name real tools, red-herring paths resolve, differentials are sorted.

Each issue carries a `fix_class`: `deterministic` ones are repaired by
`migrate_cases.py`; `judgment` ones need a clinician subagent.

Usage:
    uv run python agent-platform/scripts/validation/validate_cases.py
    uv run python agent-platform/scripts/validation/validate_cases.py --json data/review/case_issue_manifest.json
    uv run python agent-platform/scripts/validation/validate_cases.py --case ALS-M01.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from neuroagent.evaluation.metrics import _action_key
from neuroagent.tools.tool_registry import ToolRegistry
from neuroagent.tools.vocabulary import (
    is_valid_assessment_type,
    is_valid_body_imaging_study,
    is_valid_modality,
    is_valid_specimen,
    is_valid_test_type,
    is_valid_tissue_procedure,
)

CASES_DIR = Path("data/neurobench/cases")

# Tools whose single parameter selects which study was ordered, with the predicate that knows
# that tool's closed vocabulary. Kept in step with
# evaluation/metrics.py::_SCALAR_DISCRIMINATORS — a value the validator lets through but the
# metric cannot match is a silent scoring loss.
#
# Each predicate used to be inferred from the tool name, with everything that was not
# `order_advanced_imaging` checked against the *specialized test* vocabulary. That was wrong
# for the four tools added after the July 2026 review and invisible, because no case used
# their discriminating parameter yet: the first two that did — a chest CT angiogram and a
# lymph-node biopsy — were both reported as out of vocabulary while being perfectly legal.
CATCHALL_PARAM: dict[str, tuple[str, Any]] = {
    "order_advanced_imaging": ("modality", is_valid_modality),
    "order_specialized_test": ("test_type", is_valid_test_type),
    "order_body_imaging": ("study", is_valid_body_imaging_study),
    "order_microbiology": ("specimen", is_valid_specimen),
    "obtain_tissue_diagnosis": ("procedure", is_valid_tissue_procedure),
    "perform_clinical_assessment": ("assessment_type", is_valid_assessment_type),
}

# Where each tool's pre-generated output lives inside the case.
TOOL_TO_OUTPUT_FIELD: dict[str, str] = {
    "analyze_brain_mri": "mri",
    "analyze_eeg": "eeg",
    "analyze_ecg": "ecg",
    "interpret_labs": "labs",
    "analyze_csf": "csf",
    "order_ct_scan": "ct",
    "order_echocardiogram": "echo",
    "order_cardiac_monitoring": "cardiac_monitoring",
    "order_advanced_imaging": "advanced_imaging",
    "order_specialized_test": "specialized_test",
    "order_body_imaging": "body_imaging",
    "order_microbiology": "microbiology",
    "obtain_tissue_diagnosis": "tissue_diagnosis",
    "perform_clinical_assessment": "clinical_assessment",
    "search_medical_literature": "literature_search",
    "check_drug_interactions": "drug_interactions",
}

# Descriptive keys a case may attach to a tool beyond its call schema. They record clinical
# intent (which MRI sequences, which body region) that the tool does not take as an argument;
# `CostTracker` ignores them. One canonical spelling each — that is the point of the list.
ANNOTATION_KEYS: dict[str, set[str]] = {
    "analyze_brain_mri": {"sequences", "region"},
    "analyze_eeg": {"duration", "indication", "video_eeg"},
    "analyze_csf": {"basic", "paired_serum", "opening_pressure", "xanthochromia",
                    "rbc_count", "spectrophotometry"},
    "check_drug_interactions": {"screen_for", "proposed_class", "context", "indication"},
    "order_ct_scan": {"region", "indication"},
    "order_echocardiogram": {"bubble_study"},
    "order_cardiac_monitoring": {"duration_days"},
    "interpret_labs": {"lab_type"},
}

# `region` stays allowed on the two head tools, because naming an intracranial sub-region is real
# clinical intent — but only intracranial values. That annotation is how a spine or body study hid
# inside a brain or head order: the schema has no region parameter, so it was silently dropped, the
# action kept the brain study's identity, and 63 actions were in that state — all 30 MS cases (the
# cord MRI the reviewers asked for by name), all 30 ALS cases (the cervical cord, whose compressive
# myelopathy is the mimic that must be excluded before a motor neuron diagnosis), and 3 others. All
# are `order_body_imaging` now, and `include_cervical_spine` is retired.
INTRACRANIAL_REGIONS = {
    "head", "head_neck", "brain", "brain_with_contrast", "skull_base", "posterior_fossa",
    "cerebrum", "temporal_lobes", "pituitary", "orbits", "neck", "cervical_arteries",
}

LIKELIHOOD_ORDER = {"very_high": 0, "high": 1, "moderate": 2, "low": 3, "very_low": 4}

# Issues migrate_cases.py can repair without judgment.
DETERMINISTIC_CODES = {"TOOL_REMOVED", "SEQ_TOOL_REMOVED", "PARAM_RENAMABLE", "ENUM_RENAMABLE"}

RENAMABLE_KEYS: dict[tuple[str, str], str] = {
    # All scalar drug names under three spellings of the same idea: the drug being checked.
    ("check_drug_interactions", "proposed_drug"): "drug",
    ("check_drug_interactions", "proposed_medication"): "drug",
    ("check_drug_interactions", "proposed"): "drug",
    # All lists of the patient's existing medications.
    ("check_drug_interactions", "medications"): "current_medications",
    ("check_drug_interactions", "current_drugs"): "current_medications",
    ("order_echocardiogram", "study_type"): "echo_type",
    ("analyze_brain_mri", "sequence"): "sequences",
    # `device` names the monitor; `monitor_type` is the schema's word for the same thing.
    ("order_cardiac_monitoring", "device"): "monitor_type",
}
RENAMABLE_VALUES: dict[tuple[str, str, str], str] = {
    ("analyze_brain_mri", "protocol", "MS_protocol"): "ms",
    # One device, two spellings; costs.yaml prices it as `event_monitor_30d`'s sibling.
    ("order_cardiac_monitoring", "monitor_type", "ambulatory_event_monitor"): "event_monitor_30d",
}
REMOVED_TOOLS = {"consult_medical_specialist"}


def _tool_schemas() -> dict[str, dict[str, Any]]:
    reg = ToolRegistry.create_default_registry()
    return {d["function"]["name"]: d["function"]["parameters"] for d in reg.get_all_definitions()}


def _signature(tool_name: str | None, params: dict | None) -> tuple[str, str]:
    """`(name, params)` identity. Two entries are the same tool only if both match."""
    if not params:
        return (tool_name or "", "")
    return (tool_name or "", json.dumps(params, sort_keys=True, default=str))


def _resolver(case: dict):
    """`(tool, params) -> None | "ok" | "fallback"`, or None if the case cannot be modelled."""
    try:
        from neuroagent.tools.mock_server import MockServer
        from neuroagent_schemas import NeuroBenchCase

        model = NeuroBenchCase.model_validate(case)
    except Exception:  # a case mid-migration; the other checks still apply
        return None

    def resolve(tool: str, params: dict) -> str | None:
        result = MockServer(model).get_output(tool, params)
        if not result.success:
            return None
        return "fallback" if result.from_fallback else "ok"

    return resolve


def _has_output(case: dict, tool_name: str) -> bool:
    field = TOOL_TO_OUTPUT_FIELD.get(tool_name)
    if not field:
        return False
    if (case.get("initial_tool_outputs") or {}).get(field):
        return True
    return any(
        fu.get("tool_name") == tool_name and fu.get("output")
        for fu in (case.get("followup_outputs") or [])
    )


def _has_fallback(case: dict, tool_name: str) -> bool:
    field = TOOL_TO_OUTPUT_FIELD.get(tool_name)
    if not field:
        return True
    return bool((case.get("fallback_tool_outputs") or {}).get(field))


def _resolve_field_path(case: dict, path: str) -> bool:
    cur: object = case
    for part in path.replace("]", "").replace("[", ".").split("."):
        if not part:
            continue
        if part.isdigit() and isinstance(cur, list):
            if int(part) >= len(cur):
                return False
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            if part not in cur:
                return False
            cur = cur[part]
        else:
            return False
    return True


def _check_parameters(
    section: str, index: int, tool: str, params: dict, schemas: dict
) -> list[dict]:
    """Keys must be schema properties or documented annotations; values must be legal."""
    issues: list[dict] = []
    props = schemas[tool].get("properties", {})
    allowed = set(props) | ANNOTATION_KEYS.get(tool, set())

    for key, value in params.items():
        if key not in allowed:
            renamed = RENAMABLE_KEYS.get((tool, key))
            issues.append({
                "code": "PARAM_RENAMABLE" if renamed else "PARAM_UNKNOWN_KEY",
                "section": section, "index": index, "tool": tool,
                "detail": (
                    f"`{key}` -> `{renamed}`" if renamed
                    else f"`{key}` is neither a {tool} parameter nor a documented annotation"
                ),
                "fix_class": "deterministic" if renamed else "judgment",
            })
            continue

        if key == "region" and tool in ("analyze_brain_mri", "order_ct_scan"):
            if str(value) not in INTRACRANIAL_REGIONS:
                issues.append({
                    "code": "REGION_NOT_INTRACRANIAL", "section": section, "index": index,
                    "tool": tool,
                    "detail": (
                        f"region=`{value}` is outside the head and neck, which this tool cannot "
                        "image; the study belongs to order_body_imaging"
                    ),
                    "fix_class": "judgment",
                })
            continue

        catchall_key, is_valid = CATCHALL_PARAM.get(tool, (None, None))
        if key == catchall_key:
            if not is_valid(str(value)):
                issues.append({
                    "code": "VOCAB_BAD_VALUE", "section": section, "index": index, "tool": tool,
                    "detail": f"{key}=`{value}` is not in the closed vocabulary",
                    "fix_class": "judgment",
                })
        elif key in props and (enum := props[key].get("enum")) and value not in enum:
            renamed = RENAMABLE_VALUES.get((tool, key, str(value)))
            issues.append({
                "code": "ENUM_RENAMABLE" if renamed else "PARAM_BAD_ENUM",
                "section": section, "index": index, "tool": tool,
                "detail": (
                    f"{key}=`{value}` -> `{renamed}`" if renamed
                    else f"{key}=`{value}` not in {enum}"
                ),
                "fix_class": "deterministic" if renamed else "judgment",
            })
    return issues


def validate_case(case: dict, schemas: dict[str, dict[str, Any]]) -> list[dict]:
    issues: list[dict] = []
    gt = case.get("ground_truth", {}) or {}
    server = _resolver(case)

    sections = {
        "optimal_actions": gt.get("optimal_actions") or [],
        "useless_tools": gt.get("useless_tools") or [],
        "harmful_tools": gt.get("harmful_tools") or [],
    }

    for section, entries in sections.items():
        for i, entry in enumerate(entries):
            tool = entry.get("tool_name")
            if not tool:
                continue  # a clinical step with no tool call is legitimate
            if tool in REMOVED_TOOLS:
                issues.append({
                    "code": "TOOL_REMOVED", "section": section, "index": i, "tool": tool,
                    "detail": f"`{tool}` was removed from the registry; set tool_name to null",
                    "fix_class": "deterministic",
                })
                continue
            if tool not in schemas:
                issues.append({
                    "code": "TOOL_UNKNOWN", "section": section, "index": i, "tool": tool,
                    "detail": f"`{tool}` is not a registered tool",
                    "fix_class": "judgment",
                })
                continue
            issues += _check_parameters(section, i, tool, entry.get("tool_parameters") or {}, schemas)

    # Contradictions, compared on (tool_name, parameters).
    sigs = {
        name: {_signature(e.get("tool_name"), e.get("tool_parameters")) for e in entries if e.get("tool_name")}
        for name, entries in sections.items()
    }
    for a, b in (("optimal_actions", "useless_tools"),
                 ("optimal_actions", "harmful_tools"),
                 ("useless_tools", "harmful_tools")):
        for tool, _ in sigs[a] & sigs[b]:
            issues.append({
                "code": "CONTRADICTION", "section": f"{a}+{b}", "index": -1, "tool": tool,
                "detail": f"`{tool}` with identical parameters appears in both {a} and {b}",
                "fix_class": "judgment",
            })

    # An action the mock server cannot answer is a trap for the agent — so resolve every one of them
    # through the server itself rather than asking the weaker question "does this tool have any
    # stored output at all?". That proxy passed while 15 required actions returned nothing and 96
    # more were answered by *another study's* report: the case stored an advanced-imaging report, so
    # the proxy was satisfied, but it was a carotid duplex and the action asked for a transcranial
    # Doppler. Being answered by the off-pathway fallback is also wrong for a step the gold workup
    # includes — that tier means "not on the pathway, did not contribute". The two zero-cost
    # universal tools are exempt from the fallback rule: a literature search and an interaction
    # check carry no diagnostic finding, so their generic answer is a fair simulation.
    for i, action in enumerate(sections["optimal_actions"]):
        tool = action.get("tool_name")
        if not tool or tool not in schemas or server is None:
            continue
        params = dict(action.get("tool_parameters") or {})
        params.setdefault("clinical_context", str(action.get("action", ""))[:80])
        if tool == "search_medical_literature":
            params.setdefault("query", str(action.get("action", ""))[:80])
        result = server(tool, params)
        if result is None:
            issues.append({
                "code": "ACTION_NO_RESULT", "section": "optimal_actions", "index": i, "tool": tool,
                "detail": (
                    f"{action.get('category')} `{tool}`"
                    + (f" ({params.get('modality') or params.get('test_type') or ''})"
                       if params.get("modality") or params.get("test_type") else "")
                    + " returns no result; the agent obeying the gold gets an error"
                ),
                "fix_class": "judgment",
            })
        elif result == "fallback" and tool not in ("search_medical_literature",
                                                  "check_drug_interactions"):
            issues.append({
                "code": "ACTION_ONLY_FALLBACK", "section": "optimal_actions", "index": i,
                "tool": tool,
                "detail": (
                    f"{action.get('category')} `{tool}` is answered only by the off-pathway "
                    "fallback, which says the study did not contribute — but this action carries "
                    "its own expected finding"
                ),
                "fix_class": "judgment",
            })

    for entry in sections["useless_tools"]:
        tool = entry.get("tool_name")
        if tool and tool in schemas and not _has_fallback(case, tool):
            issues.append({
                "code": "USELESS_NO_FALLBACK", "section": "useless_tools", "index": -1, "tool": tool,
                "detail": f"useless `{tool}` has no fallback output; calling it errors instead of returning a normal result",
                "fix_class": "judgment",
            })

    # Two optimal actions with the same action key are ONE action to the metric layer: identical
    # tool, identical discriminator. The case's author counted two required steps and the benchmark
    # counts one, so the second study is unscoreable and an agent that skips it loses nothing.
    #
    # All 30 multiple-sclerosis cases were in this state: a brain MRI and a cervico-thoracic cord
    # MRI, both `analyze_brain_mri{protocol: ms}`, the cord one carrying a `region` annotation the
    # brain tool drops. The reviewers had asked for brain *and* cord imaging by name, and imaging
    # only the brain scored full required coverage.
    #
    # `search_medical_literature` and `check_drug_interactions` are out of scope: they cost nothing,
    # have no discriminator, and "consulted the evidence" is fairly one act however many queries it
    # took. Everything that names a study is in scope.
    _NOT_A_STUDY = {"search_medical_literature", "check_drug_interactions"}
    by_key: dict[tuple, list[dict]] = {}
    for action in gt.get("optimal_actions") or []:
        tool = action.get("tool_name")
        if not tool or tool in _NOT_A_STUDY or tool not in schemas:
            continue
        by_key.setdefault(
            _action_key(tool, action.get("tool_parameters")), []
        ).append(action)
    for key, group in by_key.items():
        if len(group) < 2:
            continue
        issues.append({
            "code": "ACTION_KEY_COLLISION",
            "section": "optimal_actions", "index": gt["optimal_actions"].index(group[1]),
            "tool": key[0],
            "detail": (
                f"{len(group)} actions share one identity {key} — the metric counts them as one "
                f"study: {[a['action'][:60] for a in group]}"
            ),
            "fix_class": "judgment",
        })

    for i, constraint in enumerate(gt.get("sequence_constraints") or []):
        for key in ("before", "after"):
            tool = constraint.get(key)
            if not tool or tool in schemas:
                continue
            removed = tool in REMOVED_TOOLS
            issues.append({
                "code": "SEQ_TOOL_REMOVED" if removed else "SEQ_UNKNOWN_TOOL",
                "section": "sequence_constraints", "index": i, "tool": tool,
                "detail": (
                    f"{key}=`{tool}` was removed from the registry; the constraint is unenforceable"
                    if removed else f"{key}=`{tool}` is not a registered tool"
                ),
                # A constraint ordering a tool that no longer exists can never be violated
                # or satisfied; dropping it is mechanical.
                "fix_class": "deterministic" if removed else "judgment",
            })

        # A `hard` constraint is a safety gate: the metric counts a violation whenever the
        # dependent step is taken and the prerequisite was not. If the prerequisite is not itself
        # `required` in this case, the gold workup contradicts itself, and an agent that correctly
        # skips an optional study is penalised for it. Found in 8 cases — 5 gating a lumbar
        # puncture on imaging the case only recommended, and 3 gating drug selection on an ECG one
        # case never ordered at all. It is also how 28 cardiac-syncope cases would have penalised
        # an agent for skipping the untargeted laboratory panel the reviewers told us to demote.
        #
        # It is only a contradiction when the *dependent* step is one a good agent takes. If
        # `after` is itself optional or absent from the gold standard, no correct pathway reaches
        # the constraint, and the rule is a conditional safety gate rather than a self-inflicted
        # penalty: "the CT is not mandatory here, but if you choose to tap, image first." That is
        # the shape in hepatic encephalopathy after the July 2026 review demoted the head CT — the
        # gold standard performs a lumbar puncture in 1 of the 30 cases, and in that one the CT is
        # required. Checking `after` is what separates the two, and without it this rule would
        # have forced the CT back to mandatory in 22 cases against the reviewers' instruction.
        if constraint.get("severity") == "hard":
            prerequisite = constraint.get("before")
            tiers = {
                action.get("category")
                for action in gt.get("optimal_actions") or []
                if action.get("tool_name") == prerequisite
            }
            dependent_tiers = {
                action.get("category")
                for action in gt.get("optimal_actions") or []
                if action.get("tool_name") == constraint.get("after")
            }
            binds_a_correct_agent = bool(dependent_tiers & {"required", "recommended"})
            if prerequisite in schemas and "required" not in tiers and binds_a_correct_agent:
                issues.append({
                    "code": "SEQ_PREREQ_NOT_REQUIRED",
                    "section": "sequence_constraints", "index": i, "tool": prerequisite,
                    "detail": (
                        f"hard constraint gates `{constraint.get('after')}` on `{prerequisite}`, "
                        f"which this case marks {sorted(tiers) or ['absent']} — raise it to "
                        "required or soften the constraint"
                    ),
                    "fix_class": "judgment",
                })

    # A stored output keyed to a tool nobody can call is unreachable. Removing it can drop a
    # case below the followup-count floor, so a human decides: re-key it or drop it.
    for i, followup in enumerate(case.get("followup_outputs") or []):
        tool = followup.get("tool_name")
        if tool and tool not in schemas:
            issues.append({
                "code": "FOLLOWUP_TOOL_REMOVED" if tool in REMOVED_TOOLS else "FOLLOWUP_TOOL_UNKNOWN",
                "section": "followup_outputs", "index": i, "tool": tool,
                "detail": f"followup output keyed to `{tool}`, which no agent can call",
                "fix_class": "judgment",
            })

    for i, herring in enumerate(gt.get("red_herrings") or []):
        path = (herring.get("field_path") or "").strip()
        if path and not _resolve_field_path(case, path):
            issues.append({
                "code": "REDHERRING_BAD_PATH", "section": "red_herrings", "index": i, "tool": "",
                "detail": f"field_path `{path}` does not resolve",
                "fix_class": "judgment",
            })

    differential = gt.get("differential") or []
    prev = -1
    for i, dx in enumerate(differential):
        rank = LIKELIHOOD_ORDER.get(dx.get("likelihood"), 99)
        if rank < prev:
            issues.append({
                "code": "DIFFERENTIAL_UNSORTED", "section": "differential", "index": i, "tool": "",
                "detail": f"likelihood `{dx.get('likelihood')}` breaks descending order",
                "fix_class": "judgment",
            })
        prev = max(prev, rank)

    if not (gt.get("critical_actions") or []):
        issues.append({
            "code": "CRITICAL_EMPTY", "section": "critical_actions", "index": -1, "tool": "",
            "detail": "critical_actions is empty", "fix_class": "judgment",
        })

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate NeuroBench cases against the tool contract")
    parser.add_argument("--cases-dir", default=str(CASES_DIR))
    parser.add_argument("--case", default=None, help="Validate a single case file")
    parser.add_argument("--json", dest="manifest", default=None, help="Write a machine-readable manifest")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    schemas = _tool_schemas()
    cases_dir = Path(args.cases_dir)
    files = [cases_dir / args.case] if args.case else sorted(cases_dir.glob("*.json"))
    if not files:
        print(f"No cases under {cases_dir}", file=sys.stderr)
        return 2

    manifest: dict[str, list[dict]] = {}
    codes: Counter[str] = Counter()
    by_class: Counter[str] = Counter()

    for path in files:
        issues = validate_case(json.loads(path.read_text()), schemas)
        if issues:
            manifest[path.name] = issues
            for issue in issues:
                codes[issue["code"]] += 1
                by_class[issue["fix_class"]] += 1

    total = sum(codes.values())
    clean = len(files) - len(manifest)

    if args.manifest:
        out = Path(args.manifest)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(manifest, indent=2, sort_keys=True))

    if not args.quiet:
        print(f"{clean}/{len(files)} cases clean, {total} issues in {len(manifest)} cases")
        if codes:
            print("\nBy code:")
            for code, n in codes.most_common():
                print(f"  {code:22s} {n:5d}")
            print(f"\nBy fix class: {dict(by_class)}")
        if args.manifest:
            print(f"\nManifest -> {args.manifest}")

    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
