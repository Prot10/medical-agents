"""Snapshot what every `interpret_labs` order is served in every case, and diff two snapshots.

The lab matcher decides which stored panel answers an order (`tools/lab_matching.py`,
`MockServer._lab_order_from`). A matcher change that fixes one case moves orders in others, and
neither the perfect-agent check nor the tests see a false positive that serves a stored panel to an
order it does not answer. On 4 Nov 2026 this audit found the AQP4/MOG panel served to clustered
AChR, parietal-cell, NMDAR and botulinum orders in MS cases, and the autoimmune-encephalitis panel
to antiphospholipid and immunoglobulin orders: 1518 of 104593 orders changed with the fix, read by
class (case -> library = a false positive removed, library -> case = a stored result now reached).

Orders: every advertised lab term alone, plus every `interpret_labs` alternative of the case's
policy with its own `panels`, each as the first call of a fresh session (state reset between
orders). One JSON line per (case, order): the tier that answered and the panels returned.

Usage:
    # before the change (e.g. on a checkout of the previous commit), then after it
    uv run python agent-platform/scripts/validation/lab_serving_audit.py snapshot before.jsonl
    uv run python agent-platform/scripts/validation/lab_serving_audit.py snapshot after.jsonl
    uv run python agent-platform/scripts/validation/lab_serving_audit.py diff before.jsonl after.jsonl --json diff.json
"""

from __future__ import annotations

import argparse
import collections
import json
from multiprocessing import Pool
from pathlib import Path

from neuroagent.datasets import REPO_ROOT

CASES = REPO_ROOT / "data" / "neurobench" / "cases"


def _serve(environment, panels: list[str]) -> dict:
    from neuroagent_schemas import ToolAction

    environment.mock_server.call_log.clear()
    environment.mock_server._served_triggers.clear()
    result = environment.execute(
        ToolAction(tool_name="interpret_labs", arguments={"clinical_context": "work-up", "panels": panels})
    )
    tier = "failed" if not result.success else "library" if result.library else "fallback" if result.from_fallback else "case"
    output = result.output or {}
    served = {name: [[row.get("test"), str(row.get("value"))] for row in rows] for name, rows in (output.get("panels") or {}).items()}
    return {"tier": tier, "panels": served, "interpretation": output.get("interpretation"),
            "summary": output.get("abnormal_values_summary"), "error": result.error_message}


def _audit(path: Path) -> list[str]:
    from neuroagent.harness import NeuroBenchEnvironment
    from neuroagent.tools.vocabulary import lab_panels
    from neuroagent_schemas import NeuroBenchCase

    case = NeuroBenchCase.model_validate_json(path.read_text())
    environment = NeuroBenchEnvironment(case)
    orders = [[term] for term in lab_panels()]
    for criterion in case.ground_truth.action_criteria:
        for alternative in criterion.alternatives:
            panels = alternative.required_arguments.get("panels") if alternative.tool_name == "interpret_labs" else None
            if panels:
                orders.append(panels if isinstance(panels, list) else [panels])
    rows, seen = [], set()
    for panels in orders:
        key = json.dumps(panels)
        if key not in seen:
            seen.add(key)
            rows.append(json.dumps({"case": case.case_id, "order": panels, **_serve(environment, panels)}))
    return rows


def snapshot(args: argparse.Namespace) -> None:
    with args.output.open("w") as out, Pool(args.workers) as pool:
        for rows in pool.imap(_audit, sorted(CASES.glob("*.json"))):
            out.write("\n".join(rows) + "\n")


def diff(args: argparse.Namespace) -> None:
    before = [json.loads(line) for line in args.before.open()]
    after = [json.loads(line) for line in args.after.open()]
    if [(row["case"], row["order"]) for row in before] != [(row["case"], row["order"]) for row in after]:
        raise SystemExit("the snapshots hold different orders (vocabulary or policies changed): diff by key instead")
    changed = [(old, new) for old, new in zip(before, after) if old != new]
    print(f"orders {len(after)}  changed {len(changed)}  cases {len({old['case'] for old, _ in changed})}")
    kinds = collections.Counter()
    for old, new in changed:
        added, removed = set(new["panels"]) - set(old["panels"]), set(old["panels"]) - set(new["panels"])
        if old["tier"] != new["tier"]:
            kinds[f"tier {old['tier']} -> {new['tier']}"] += 1
        elif added or removed:
            kinds[f"panels +{len(added)} -{len(removed)}"] += 1
        else:
            kinds["rows or prose only"] += 1
    for kind, count in kinds.most_common():
        print(f"  {count:6d}  {kind}")
    if args.json:
        args.json.write_text(json.dumps([[old, new] for old, new in changed], indent=1))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    snap = commands.add_parser("snapshot")
    snap.add_argument("output", type=Path)
    snap.add_argument("--workers", type=int, default=10)
    compare = commands.add_parser("diff")
    compare.add_argument("before", type=Path)
    compare.add_argument("after", type=Path)
    compare.add_argument("--json", type=Path)
    args = parser.parse_args(argv)
    {"snapshot": snapshot, "diff": diff}[args.command](args)


if __name__ == "__main__":
    main()
