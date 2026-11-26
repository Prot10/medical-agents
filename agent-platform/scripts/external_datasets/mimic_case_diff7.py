"""Task 07: which live cases changed between two case folders, ignoring the build counters and the order of the
policy criteria (set order is not stable across runs). Writes the id list under $W/out. No record content in this file.

    python -I mimic_case_diff7.py --out $W/out --old $W/tmp/cases_r4_state --write 07_changed_since_r4.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd


def canon(d: dict) -> str:
    d = json.loads(json.dumps(d))
    d["metadata"].pop("build_counts", None)
    d["metadata"].pop("builder", None)
    gt = d["ground_truth"]
    ren = {}
    crit = sorted(gt.get("action_criteria", []), key=lambda c: json.dumps({k: v for k, v in c.items() if k != "criterion_id"}, sort_keys=True))
    for c in gt.get("action_criteria", []):
        m = re.match(r"^(Blood tests: )(.*)$", c.get("label", ""))
        if m:  # the panel list in the label follows the (unordered) panel set
            c["label"] = m.group(1) + ", ".join(sorted(m.group(2).split(", ")))
    crit = sorted(crit, key=lambda c: json.dumps({k: v for k, v in c.items() if k != "criterion_id"}, sort_keys=True))
    for i, c in enumerate(crit):
        ren[c["criterion_id"]] = re.sub(r"^action-\d+", f"action-S{i}", c["criterion_id"])  # position in the sorted order
        c["criterion_id"] = ren[c["criterion_id"]]
    gt["action_criteria"] = crit
    s = json.dumps(d, sort_keys=True)
    for old, new in ren.items():
        s = s.replace(f'"{old}"', f'"{new}"')
    # lists of panels / ids are order-free
    return json.dumps(_sortlists(json.loads(s)), sort_keys=True)


def _sortlists(x):
    if isinstance(x, dict):
        return {k: _sortlists(v) for k, v in x.items()}
    if isinstance(x, list):
        y = [_sortlists(v) for v in x]
        if all(isinstance(v, str) for v in y):
            return sorted(y)
        return y
    return x


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--old", required=True)
    ap.add_argument("--write", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    sel = pd.read_csv(out / "06_selection.csv")
    live = list(sel[sel.case_id.notna() & sel.exclusion.isna()].case_id)
    ch = []
    for c in live:
        new, old = out / "06_cases" / f"{c}.json", Path(a.old) / f"{c}.json"
        if not old.exists() or canon(json.loads(new.read_text())) != canon(json.loads(old.read_text())):
            ch.append(c)
    (out / a.write).write_text(json.dumps(ch))
    print(len(live), "live cases;", len(ch), "changed")


if __name__ == "__main__":
    main()
