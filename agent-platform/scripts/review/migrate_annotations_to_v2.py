"""Move reviewer annotations from schema-v1 field paths to the schema-v2 fields that hold the same content.

The v2 migration renamed and restructured the ground truth (`optimal_actions` became
`action_criteria`, `contraindicated_actions` became `assessment.prohibited_recommendations`, ...)
but kept its content. An annotation stores the path of the field it was written on, so after a
v2 deploy every annotation on a renamed field would lose its anchor. This script finds, for each
annotation, the v2 field whose content is the one the reviewer annotated in the deployed v1 case,
and rewrites only `field_path`. Comments, severities, timestamps and resolved flags are untouched.

Standard library only, so it runs with the server's system Python while the review service is
stopped:

    python3 migrate_annotations_to_v2.py --annotations data/review/annotations \\
        --tool-reviews data/review/tool_reviews --old-cases /path/to/v1/cases \\
        --new-cases data/neurobench/cases --manifest out.json [--apply]

Without --apply it only reports. It is idempotent: a path that already names a v2 field and is
absent from v1 is left alone.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

MISSING = object()
_TOKENS = re.compile(r"[^.\[\]]+|\[\d+\]")
_REQUIRED = "ground_truth.assessment.required_recommendations"

# Read by hand: no rule finds these, and the step they comment on is plainly the named v2 field.
# ALZ-EARLY-P04 optimal_actions[2] is the tool-less genetic-counselling referral; v2 keeps the
# same referral, worded as the case's critical action, as required_recommendations[5]. The
# reviewer's error (do not imply predictive testing of the teenage children) applies to it as is.
OVERRIDES = {
    ("ALZ-EARLY-P04", "ground_truth.optimal_actions[2]"): f"{_REQUIRED}[5]",
}


def get(root: Any, path: str) -> Any:
    """The value at an annotation path such as `ground_truth.red_herrings[0]`, or MISSING."""
    node = root
    for token in _TOKENS.findall(path):
        if token.startswith("["):
            index = int(token[1:-1])
            if not isinstance(node, list) or index >= len(node):
                return MISSING
            node = node[index]
        else:
            if not isinstance(node, dict) or token not in node:
                return MISSING
            node = node[token]
    return node


def _unique(paths: list[str]) -> str | None:
    return paths[0] if len(paths) == 1 else None


def _criteria_with_label(new_gt: dict, label: str) -> list[str]:
    return [
        f"ground_truth.action_criteria[{i}]"
        for i, criterion in enumerate(new_gt["action_criteria"])
        if criterion["label"] == label
    ]


def _equal_items(new_gt: dict, key: str, prefix: str, value: Any) -> list[str]:
    return [f"{prefix}[{i}]" for i, item in enumerate(new_gt[key]) if item == value]


def _avoided(new_gt: dict, severity: str, tool: dict) -> list[str]:
    return [
        f"ground_truth.avoided_actions[{i}]"
        for i, item in enumerate(new_gt["avoided_actions"])
        if item["severity"] == severity
        and item.get("rationale") == tool.get("rationale")
        and [
            {"tool_name": tool["tool_name"], "required_arguments": tool.get("tool_parameters") or {}}
        ]
        == [{"tool_name": a["tool_name"], "required_arguments": a["required_arguments"]} for a in item["alternatives"]]
    ]


def _same_constraint(old: Any, new: Any) -> bool:
    # v2 names the endpoints by criterion id instead of tool name; the authored reason is kept.
    return isinstance(old, dict) and isinstance(new, dict) and old.get("reason") == new.get("reason")


def resolve(old_case: dict, new_case: dict, path: str) -> tuple[str | None, str]:
    """The v2 path for an annotation written on `path` of the v1 case, and the rule that found it.

    Returns (None, reason) when no v2 field holds the annotated content.
    """
    old = get(old_case, path)
    new = get(new_case, path)
    override = OVERRIDES.get((old_case.get("case_id"), path))
    if override is not None and old is not MISSING and get(new_case, override) is not MISSING:
        return override, "read by hand"
    if old is MISSING:
        if new is not MISSING:
            return path, "already-v2"
        return None, "not in the deployed case either"
    if new is not MISSING and (new == old or ("sequence_constraints[" in path and _same_constraint(old, new))):
        return path, "same"

    new_gt = new_case["ground_truth"]
    root = re.sub(r"\[\d+\]$", "", path)
    target: str | None = None
    if path == "ground_truth.primary_diagnosis":
        if new_gt["diagnosis"]["accepted"][:1] == [old]:
            target, rule = "ground_truth.diagnosis", "primary_diagnosis->diagnosis"
    elif root == "ground_truth.optimal_actions":
        target, rule = _unique(_criteria_with_label(new_gt, old["action"])), "optimal_actions->action_criteria"
        if target is None:
            # Steps without a tool call are not action criteria; a few survive as recommendations.
            target = _unique(_equal_items(new_gt["assessment"], "required_recommendations", _REQUIRED, old["action"]))
            rule = "optimal_actions->required_recommendations"
    elif root == "ground_truth.critical_actions":
        # The migration copied critical_actions verbatim into the assessment's required recommendations.
        target, rule = _unique(_equal_items(new_gt["assessment"], "required_recommendations", _REQUIRED, old)), (
            "critical_actions->required_recommendations"
        )
    elif root == "ground_truth.contraindicated_actions":
        target = _unique(
            _equal_items(
                new_gt["assessment"], "prohibited_recommendations", "ground_truth.assessment.prohibited_recommendations", old
            )
        )
        rule = "contraindicated_actions->prohibited_recommendations"
    elif root == "ground_truth.key_reasoning_points":
        target = _unique(_equal_items(new_gt, "key_clinical_evidence", "ground_truth.key_clinical_evidence", old))
        rule = "key_reasoning_points->key_clinical_evidence"
    elif root in ("ground_truth.useless_tools", "ground_truth.harmful_tools"):
        severity = "waste" if root.endswith("useless_tools") else "harm"
        target, rule = _unique(_avoided(new_gt, severity, old)), f"{root.split('.')[-1]}->avoided_actions"
    elif root == "ground_truth.sequence_constraints":
        matches = [
            f"ground_truth.sequence_constraints[{i}]"
            for i, item in enumerate(new_gt["sequence_constraints"])
            if _same_constraint(old, item)
        ]
        target, rule = _unique(matches), "sequence_constraints by reason"
    elif re.search(r"\[\d+\]$", path) and isinstance(get(new_case, root), list):
        matches = [f"{root}[{i}]" for i, item in enumerate(get(new_case, root)) if item == old]
        target, rule = _unique(matches), "same list, moved"
    else:
        rule = "no rule"
    if target is None:
        return None, f"no unique v2 field ({rule})"
    return target, rule


def _write_atomically(path: Path, text: str) -> None:
    with tempfile.NamedTemporaryFile("w", dir=path.parent, suffix=".tmp", delete=False, encoding="utf-8") as fh:
        fh.write(text)
        tmp = Path(fh.name)
    os.chmod(tmp, path.stat().st_mode & 0o777)
    tmp.replace(path)


# The v1 app read `neurobench` records and fell back to the legacy `v5` directory; the v2 app reads
# only `neurobench`. Copying each fallback record under the canonical name keeps what reviewers see.
LEGACY_ALIASES = {"v5": "neurobench"}


def promote_legacy_aliases(root: Path, pattern: str, apply: bool) -> list[dict]:
    """Copy alias records with no canonical counterpart into the canonical directory.

    `pattern` locates records under one version directory: `*/*.json` for case reviews
    (reviewer/case), `*.json` for tool reviews (reviewer). The alias files are left in place.
    """
    promoted = []
    for alias, canonical in LEGACY_ALIASES.items():
        for source in sorted((root / alias).glob(pattern)):
            target = root / canonical / source.relative_to(root / alias)
            if target.exists():
                continue
            text = source.read_text(encoding="utf-8")
            record = json.loads(text)
            if record.get("dataset_version") != alias:
                raise RuntimeError(f"{source}: dataset_version is {record.get('dataset_version')!r}")
            copied = text.replace(f'"dataset_version": "{alias}"', f'"dataset_version": "{canonical}"', 1)
            if json.loads(copied) != {**record, "dataset_version": canonical}:
                raise RuntimeError(f"{source}: promotion changed more than dataset_version")
            promoted.append({"from": str(source.relative_to(root)), "to": str(target.relative_to(root))})
            if apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(copied, encoding="utf-8")
                os.chmod(target, source.stat().st_mode & 0o777)
    return promoted


def migrate(annotations: Path, old_cases: Path, new_cases: Path, apply: bool) -> dict:
    changes: list[dict] = []
    unresolved: list[dict] = []
    outcome: Counter[str] = Counter()
    cache: dict[tuple[Path, str], dict] = {}

    def case(root: Path, case_id: str) -> dict | None:
        key = (root, case_id)
        if key not in cache:
            file = root / f"{case_id}.json"
            cache[key] = json.loads(file.read_text()) if file.exists() else None
        return cache[key]

    for file in sorted(annotations.glob("*/*/*.json")):
        text = file.read_text(encoding="utf-8")
        review = json.loads(text)
        old_case, new_case = case(old_cases, review["case_id"]), case(new_cases, review["case_id"])
        mapping: dict[str, str] = {}
        for annotation in review.get("field_annotations", []):
            path = annotation["field_path"]
            if old_case is None or new_case is None:
                target, rule = None, "case not in both datasets"
            else:
                target, rule = resolve(old_case, new_case, path)
            entry = {
                "file": str(file.relative_to(annotations)),
                "annotation_id": annotation["id"],
                "case_id": review["case_id"],
                "old_path": path,
            }
            if target is None:
                outcome["unresolved"] += 1
                unresolved.append({**entry, "reason": rule})
            elif target == path:
                outcome[rule] += 1
            else:
                outcome["moved"] += 1
                mapping[path] = target
                changes.append({**entry, "new_path": target, "rule": rule})

        if mapping and apply:
            migrated = text
            for old_path, new_path in mapping.items():
                migrated = migrated.replace(
                    f'"field_path": {json.dumps(old_path)}', f'"field_path": {json.dumps(new_path)}'
                )
            # Nothing but the remapped paths may differ.
            expected = json.loads(text)
            for annotation in expected.get("field_annotations", []):
                annotation["field_path"] = mapping.get(annotation["field_path"], annotation["field_path"])
            if json.loads(migrated) != expected:
                raise RuntimeError(f"{file}: rewrite changed more than field_path")
            _write_atomically(file, migrated)

    return {"applied": apply, "outcome": dict(outcome), "changes": changes, "unresolved": unresolved}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--old-cases", type=Path, required=True)
    parser.add_argument("--new-cases", type=Path, required=True)
    parser.add_argument("--tool-reviews", type=Path, help="tool-review root, for the legacy alias step")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    promoted = promote_legacy_aliases(args.annotations, "*/*.json", args.apply)
    if args.tool_reviews:
        promoted += promote_legacy_aliases(args.tool_reviews, "*.json", args.apply)
    report = migrate(args.annotations, args.old_cases, args.new_cases, args.apply)
    report["promoted"] = promoted
    args.manifest.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"applied": report["applied"], "outcome": report["outcome"], "promoted": len(promoted)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
