"""Task 07: apply reader-level corrections to the manual files from an operations file kept in the
workspace ($W/out/07_manual_fixes.json; it holds record text, so it never leaves the workspace).
Each operation: {"case", "op", ...} with op one of
  set     {"path": "a.b", "value": ...}            set a field (dotted path into the manual file)
  append  {"path": "a.b", "text": "..."}           append a verbatim fragment to a " | "-joined text field
  list_replace {"path": "a", "old": "...", "new": [..]}  replace one list item by zero or more items
  list_drop    {"path": "a", "index": k}           drop one list item
Files are written whole (one write per file); the operation is recorded in other_edits. Idempotent:
an operation already recorded is skipped. No record content in this file.

    python -I mimic_manual_fix7.py --out $W/out
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _get(d: dict, path: str):
    for k in path.split(".")[:-1]:
        d = d.setdefault(k, {})
    return d, path.split(".")[-1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--ops", default="07_manual_fixes.json")
    a = ap.parse_args()
    out = Path(a.out)
    ops = json.loads((out / a.ops).read_text())
    by_case: dict[str, list] = {}
    for o in ops:
        by_case.setdefault(o["case"], []).append(o)
    n = 0
    for cid, lst in by_case.items():
        f = out / "06_manual" / f"{cid}.json"
        m = json.loads(f.read_text())
        done = set(m.get("task07_ops", []))
        changed = False
        for o in lst:
            tag = json.dumps(o, sort_keys=True)
            if tag in done:
                continue
            d, k = _get(m, o["path"])
            if o["op"] == "set":
                d[k] = o["value"]
            elif o["op"] == "append":
                d[k] = (str(d.get(k) or "").rstrip(" |") + " | " + o["text"]).strip(" |")
            elif o["op"] == "list_replace":
                lst_ = list(d.get(k) or [])
                i = lst_.index(o["old"])
                d[k] = lst_[:i] + list(o["new"]) + lst_[i + 1:]
            elif o["op"] == "list_drop":
                lst_ = list(d.get(k) or [])
                del lst_[o["index"]]
                d[k] = lst_
            elif o["op"] == "note":  # a withdrawn correction, recorded only
                pass
            else:
                raise SystemExit(f"unknown op {o['op']}")
            m.setdefault("task07_ops", []).append(tag)
            m.setdefault("other_edits", []).append(f"task-07 correction: {o['op']} {o['path']} ({o.get('why', '')})")
            changed, n = True, n + 1
        if changed:
            f.write_text(json.dumps(m, indent=1) + "\n")
    print("operations applied:", n, "in", len(by_case), "manual files")


if __name__ == "__main__":
    main()
