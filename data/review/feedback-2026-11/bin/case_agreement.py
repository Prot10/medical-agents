"""Case-level agreement between the two physicians, read from the annotations alone.

    python3 -I data/review/feedback-2026-11/bin/case_agreement.py ANNOTATIONS_ROOT

ANNOTATIONS_ROOT is the review app's `data/review/annotations/` (one folder per dataset or review
set, then one per reviewer code, then one JSON file per case).

Rule (Andrea, 25 Nov 2026): a case with annotations has not passed. Per reviewer and case:
  FAIL          at least one annotation (field note or case comment), whatever its severity
                and whatever status the reviewer chose (an `approved` case with notes fails);
  PASS          no annotation, and the reviewer decided the case (`approved` or
                `needs_changes`, i.e. pressed the button the app counts as "reviewed");
  NOT REVIEWED  no annotation and no decision (opened only: `pending`, `in_progress`). It is
                excluded, because it cannot be told apart from a case nobody looked at.
A case enters the agreement only when both reviewers have PASS or FAIL on it in the same dataset
folder. Caveat the script cannot check: the files do not record the case version, so a pair
whose reviews straddle a deploy that changed the case compares two different cases.

Reported on the 2x2 table: observed agreement, Cohen's kappa, Gwet's AC1, PABAK, and the
specific agreements on FAIL (2a / (2a + b + c)) and on PASS (2d / (2d + b + c)). With one
category near 100%, kappa collapses or is undefined; the specific agreements say which
category the reviewers agree on.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from collections import defaultdict

REVIEWERS = {"NB-KSC3-TWUA-QDTM": "R1", "NB-87MF-FBTV-TPWE": "R2"}


def verdict(d: dict) -> str:
    if (d.get("field_annotations") or []) or (d.get("case_comments") or []):
        return "FAIL"
    if d.get("status") in ("approved", "needs_changes"):
        return "PASS"
    return "NOT_REVIEWED"


def table(pairs: list[tuple[str, str]]) -> dict:
    a = sum(p == ("FAIL", "FAIL") for p in pairs)
    b = sum(p == ("FAIL", "PASS") for p in pairs)
    c = sum(p == ("PASS", "FAIL") for p in pairs)
    d = sum(p == ("PASS", "PASS") for p in pairs)
    n = a + b + c + d
    out: dict = {"n": n, "both_fail": a, "R1_fail_R2_pass": b, "R1_pass_R2_fail": c, "both_pass": d}
    if not n:
        return out
    po = (a + d) / n
    p1, p2 = (a + b) / n, (a + c) / n
    pe = p1 * p2 + (1 - p1) * (1 - p2)
    pi = (p1 + p2) / 2
    pe_g = 2 * pi * (1 - pi)
    out.update({
        "agreement": round(po, 3),
        "kappa": round((po - pe) / (1 - pe), 3) if pe < 1 else None,
        "ac1": round((po - pe_g) / (1 - pe_g), 3) if pe_g < 1 else None,
        "pabak": round(2 * po - 1, 3),
        "specific_fail": round(2 * a / (2 * a + b + c), 3) if a + b + c else None,
        "specific_pass": round(2 * d / (2 * d + b + c), 3) if d + b + c else None,
    })
    return out


def main() -> None:
    root = sys.argv[1]
    report = {}
    for ds in sorted(os.listdir(root)):
        cases: dict[str, dict] = defaultdict(dict)
        for f in glob.glob(os.path.join(root, ds, "*", "*.json")):
            d = json.load(open(f))
            if d["reviewer_code"] in REVIEWERS:
                cases[d["case_id"]][REVIEWERS[d["reviewer_code"]]] = d
        opened_by_both = sorted(c for c, v in cases.items() if len(v) == 2)
        rows, excluded = [], {}
        for c in opened_by_both:
            v1, v2 = verdict(cases[c]["R1"]), verdict(cases[c]["R2"])
            if "NOT_REVIEWED" in (v1, v2):
                excluded[c] = f"R1 {v1}, R2 {v2}"
            else:
                rows.append({"case_id": c, "R1": v1, "R2": v2,
                             "R1_dates": (cases[c]["R1"]["first_opened_at"][:10], cases[c]["R1"]["last_updated_at"][:10]),
                             "R2_dates": (cases[c]["R2"]["first_opened_at"][:10], cases[c]["R2"]["last_updated_at"][:10])})
        report[ds] = {"opened_by_both": len(opened_by_both), "excluded": excluded, "pairs": rows,
                      "stats": table([(r["R1"], r["R2"]) for r in rows])}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
