"""Inter-rater agreement on the cases both physicians reviewed (ISCH-STR, Nov 2026).

    python3 -I data/review/feedback-2026-11/bin/agreement.py CLASSIFIED_JSON ANNOTATIONS_DIR

CLASSIFIED_JSON holds every note of both reviewers on the shared cases with its policy dimension
and a normalised issue label, plus the matched pairs (same clinical problem on the same case):
{"notes": [{id, case_id, reviewer, dimension, label}], "matches": [{case_id, r1_id, r2_id, ...}]}.
ANNOTATIONS_DIR is the review app's `annotations/neurobench` folder (case statuses).

Three levels:
1. Case verdict: needs changes vs approved. A case a reviewer did not submit counts as needs
   changes when it holds an `error` note, and is left out when it holds no note.
2. Case x dimension: does the reviewer flag that dimension of that case (any note on it)?
3. Issue: matched pairs over all notes, as Dice = 2 matches / (notes R1 + notes R2).
Cohen's kappa, Gwet's AC1 and PABAK are given for 1 and 2: with almost every case flagged by
both, kappa collapses (prevalence paradox) and AC1/PABAK are the usual companions.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

DIMS = ["scenario_plausibility", "diagnosis", "actions", "avoided_actions", "sequencing", "stopping", "assessment"]
CODES = {"R1": "NB-KSC3-TWUA-QDTM", "R2": "NB-87MF-FBTV-TPWE"}


def stats(pairs: list[tuple[int, int]]) -> dict:
    n = len(pairs)
    if not n:
        return {"n": 0}
    po = sum(a == b for a, b in pairs) / n
    p1 = sum(a for a, _ in pairs) / n
    p2 = sum(b for _, b in pairs) / n
    pe = p1 * p2 + (1 - p1) * (1 - p2)
    kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")
    pi = (p1 + p2) / 2
    pe_g = 2 * pi * (1 - pi)
    ac1 = (po - pe_g) / (1 - pe_g) if pe_g < 1 else float("nan")
    return {"n": n, "agreement": round(po, 3), "kappa": round(kappa, 3), "ac1": round(ac1, 3),
            "pabak": round(2 * po - 1, 3), "flag_rate_R1": round(p1, 3), "flag_rate_R2": round(p2, 3),
            "both": sum(a and b for a, b in pairs), "R1_only": sum(a and not b for a, b in pairs),
            "R2_only": sum(b and not a for a, b in pairs), "neither": sum(not a and not b for a, b in pairs)}


def verdict(path: Path) -> int | None:
    d = json.loads(path.read_text())
    notes = (d.get("field_annotations") or []) + (d.get("case_comments") or [])
    if d["status"] in ("approved", "needs_changes"):
        return int(d["status"] == "needs_changes")
    if any(n.get("severity") == "error" for n in notes):
        return 1
    return None


def main() -> None:
    data = json.loads(Path(sys.argv[1]).read_text())
    ann = Path(sys.argv[2])
    notes, matches = data["notes"], data["matches"]
    cases = sorted({n["case_id"] for n in notes if n["reviewer"] == "R1"})
    out: dict = {"cases": cases}

    rows = []
    for c in cases:
        v = {r: verdict(ann / code / f"{c}.json") for r, code in CODES.items()}
        if None not in v.values():
            rows.append((v["R1"], v["R2"]))
    out["case_verdict"] = stats(rows)

    flagged = defaultdict(set)
    for n in notes:
        flagged[(n["reviewer"], n["case_id"])].add(n["dimension"])
    per_dim, pooled = {}, []
    for dim in DIMS:
        pairs = [(int(dim in flagged[("R1", c)]), int(dim in flagged[("R2", c)])) for c in cases]
        per_dim[dim] = stats(pairs)
        pooled += pairs
    out["dimension_pooled"] = stats(pooled)
    out["dimension"] = per_dim

    n1 = sum(n["reviewer"] == "R1" and n["case_id"] in cases for n in notes)
    n2 = sum(n["reviewer"] == "R2" and n["case_id"] in cases for n in notes)
    m = len(matches)
    out["issue"] = {"notes_R1": n1, "notes_R2": n2, "matches": m, "dice": round(2 * m / (n1 + n2), 3),
                    "share_of_R1_raised_by_R2": round(m / n1, 3), "share_of_R2_raised_by_R1": round(m / n2, 3),
                    "matched_R2_ruled_fixed_in_october": sum(x.get("october_ruling") == "FIXED" for x in matches)}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
