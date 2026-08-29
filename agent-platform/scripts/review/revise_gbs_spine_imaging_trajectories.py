"""Keep GBS trajectories executable after routing selective spine MRI to body imaging."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "training_data" / "gold_trajectories" / "trajectories.jsonl"
CASES = ROOT / "data" / "neurobench" / "cases"


def output(case: dict[str, Any]) -> dict[str, Any]:
    return next(x["output"] for x in case["followup_outputs"] if x.get("tool_name") == "order_body_imaging")


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "guillain_barre":
        return False
    before = json.dumps(row, sort_keys=True)
    selected = any(a.get("tool_name") == "order_body_imaging" for a in case["ground_truth"]["optimal_actions"])
    messages: list[dict[str, Any]] = []
    skip_next_tool = False
    calls: list[str] = []
    for message in row["messages"]:
        if skip_next_tool and message.get("role") == "tool":
            skip_next_tool = False
            continue
        calls_here = message.get("tool_calls") or []
        if any(c.get("function", {}).get("name") == "order_advanced_imaging" for c in calls_here):
            if not selected:
                skip_next_tool = True
                continue
            changed = json.loads(json.dumps(message))
            for call in changed["tool_calls"]:
                fn = call["function"]
                if fn["name"] == "order_advanced_imaging":
                    fn["name"] = "order_body_imaging"
                    fn["arguments"] = {
                        "clinical_context": "Targeted spine MRI is justified only by this case's live structural or myelopathic alternative.",
                        "study": "spine_MRI",
                        "contrast": True,
                    }
            messages.append(changed)
            messages.append({"role": "tool", "content": json.dumps(output(case), indent=2, ensure_ascii=False)})
            skip_next_tool = True
            calls.append("order_body_imaging")
            continue
        messages.append(message)
        calls.extend(c["function"]["name"] for c in calls_here)
    row["messages"] = messages
    row["tools_called"] = list(dict.fromkeys(calls))
    row["num_tool_calls"] = len(calls)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cases = {p.stem: json.loads(p.read_text()) for p in CASES.glob("GBS-*.json")}
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    changed = sum(revise(row, cases[row["case_id"]]) for row in rows if row.get("condition") == "guillain_barre")
    print(f"GBS spine-imaging trajectories changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)
    if not args.check:
        args.input.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


if __name__ == "__main__":
    main()
