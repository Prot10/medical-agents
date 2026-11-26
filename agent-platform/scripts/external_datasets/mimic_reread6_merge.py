"""Task 06, check C4: merge the readers' JSON files (tmp/reread6/out_*.json) into per-condition
counts: fields checked, findings by class and severity, error rate (errors per field checked, and
cases with at least one error). Writes $W/out/06_reread_all.json (case-level, workspace only) and
$W/out/06_reread_summary.json (aggregates, no ids). With --round2 DIR, merges the re-read of the
fixed cases and reports the residual. No record content in this file.

    python -I mimic_reread6_merge.py --out $W/out --dir $W/tmp/reread6 [--round2 $W/tmp/reread6b]
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
from pathlib import Path


def load(d: str) -> dict:
    allr = {}
    for f in sorted(glob.glob(f"{d}/out_*.json")):
        txt = Path(f).read_text()
        d, end = json.JSONDecoder().raw_decode(txt)  # a reader file with a stray trailing brace is read up to its first object
        if txt[end:].strip():
            print("note: trailing characters ignored in", Path(f).name)
        allr.update(d)
    return allr


def summarise(allr: dict) -> dict:
    per = collections.defaultdict(lambda: {"cases": 0, "fields_checked": 0, "errors": 0, "minor": 0, "cases_with_error": 0,
                                           "error_classes": collections.Counter(), "minor_classes": collections.Counter()})
    for cid, v in allr.items():
        cond = cid.split("-")[1]
        p = per[cond]
        p["cases"] += 1
        p["fields_checked"] += int(v.get("fields_checked") or 0)
        errs = [f for f in v.get("findings", []) if f.get("severity") == "error"]
        mins = [f for f in v.get("findings", []) if f.get("severity") != "error"]
        p["errors"] += len(errs)
        p["minor"] += len(mins)
        p["cases_with_error"] += bool(errs)
        p["error_classes"].update(f.get("class", "other") for f in errs)
        p["minor_classes"].update(f.get("class", "other") for f in mins)
    tot = {"cases": 0, "fields_checked": 0, "errors": 0, "minor": 0, "cases_with_error": 0,
           "error_classes": collections.Counter(), "minor_classes": collections.Counter()}
    for p in per.values():
        for k in ("cases", "fields_checked", "errors", "minor", "cases_with_error"):
            tot[k] += p[k]
        tot["error_classes"].update(p["error_classes"])
        tot["minor_classes"].update(p["minor_classes"])
    out = {c: {**p, "error_classes": dict(p["error_classes"]), "minor_classes": dict(p["minor_classes"]),
               "error_rate_per_field": round(p["errors"] / max(p["fields_checked"], 1), 4)} for c, p in sorted(per.items())}
    out["TOTAL"] = {**tot, "error_classes": dict(tot["error_classes"]), "minor_classes": dict(tot["minor_classes"]),
                    "error_rate_per_field": round(tot["errors"] / max(tot["fields_checked"], 1), 4)}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--round2", default="")
    ap.add_argument("--tag", default="06", help="output file prefix (task 07: 07_r3, 07_r4, ...)")
    a = ap.parse_args()
    out = Path(a.out)
    r1 = load(a.dir)
    (out / f"{a.tag}_reread_all.json").write_text(json.dumps(r1, indent=1))
    res = {"round1": summarise(r1)}
    if a.round2:
        r2 = load(a.round2)
        (out / f"{a.tag}_reread_round2_all.json").write_text(json.dumps(r2, indent=1))
        res["round2_fixed_cases"] = summarise(r2)
    (out / f"{a.tag}_reread_summary.json").write_text(json.dumps(res, indent=1))
    for k, s in res.items():
        print("==", k)
        for c, p in s.items():
            print(f"{c:6s} cases {p['cases']:3d} fields {p['fields_checked']:5d} errors {p['errors']:3d} (cases {p['cases_with_error']:2d}) "
                  f"minor {p['minor']:3d} rate {p['error_rate_per_field']:.4f} | {p['error_classes']}")


if __name__ == "__main__":
    main()
