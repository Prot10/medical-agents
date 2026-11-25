"""Copy the physicians' notes from a review-app snapshot into readable files, one per group.

    python3 -I data/review/feedback-2026-11/bin/export_notes.py SNAPSHOT_ANNOTATIONS_DIR OUT_DIR

SNAPSHOT_ANNOTATIONS_DIR is the `annotations/` folder of a VPS backup tarball (one folder per
dataset or review set, then one per reviewer code, then one JSON file per case). Only cases
last updated on or after --since are exported. For each dataset folder the script writes
`<dataset>.json` (a flat list of notes, the October round's format plus `case_status` and
`dataset`) and `<dataset>.md` (the same notes grouped by case). Policy verdicts are exported
as a note of kind `policy_verdict` whose `verdict` holds the per-dimension verdicts.
The output holds reviewer text, so OUT_DIR must be a gitignored folder.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from pathlib import Path

REVIEWERS = {"NB-87MF-FBTV-TPWE": "R2", "NB-KSC3-TWUA-QDTM": "R1"}


def notes_of(d: dict, dataset: str) -> list[dict]:
    base = {"case_id": d["case_id"], "reviewer": REVIEWERS.get(d["reviewer_code"], d["reviewer_code"][:6]),
            "case_status": d.get("status"), "dataset": dataset}
    out = []
    for a in d.get("field_annotations") or []:
        out.append({"id": a["id"], **base, "kind": "field", "field_path": a.get("field_path"),
                    "snippet": a.get("field_snippet"), "severity": a.get("severity"),
                    "comment": a.get("comment"), "resolved": a.get("resolved", False)})
    for a in d.get("case_comments") or []:
        out.append({"id": a["id"], **base, "kind": "case", "field_path": None, "snippet": None,
                    "severity": a.get("severity"), "comment": a.get("comment"), "resolved": a.get("resolved", False)})
    pv = d.get("policy_verdict")
    if pv:
        out.append({"id": f"{d['reviewer_code'][:6]}:{d['case_id']}:policy_verdict", **base, "kind": "policy_verdict",
                    "verdict": {k: v for k, v in pv.items() if k not in ("comment", "submitted_at")},
                    "severity": None, "comment": pv.get("comment") or "", "submitted_at": pv.get("submitted_at")})
    if not out:
        out.append({"id": f"{d['reviewer_code'][:6]}:{d['case_id']}:empty", **base, "kind": "no_notes",
                    "severity": None, "comment": ""})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("annotations")
    ap.add_argument("out")
    ap.add_argument("--since", default="2026-11-18", help="ISO date; cases last updated before it are skipped")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for ds_dir in sorted(p for p in Path(a.annotations).iterdir() if p.is_dir()):
        notes = []
        for f in sorted(glob.glob(os.path.join(ds_dir, "*", "*.json"))):
            d = json.loads(Path(f).read_text())
            if (d.get("last_updated_at") or "") >= a.since:
                notes.extend(notes_of(d, ds_dir.name))
        if not notes:
            continue
        notes.sort(key=lambda n: (n["case_id"], n["reviewer"]))
        (out / f"{ds_dir.name}.json").write_text(json.dumps(notes, indent=2, ensure_ascii=False) + "\n")
        lines = [f"# Reviewer notes, {ds_dir.name} ({sum(n['kind'] in ('field', 'case') for n in notes)} notes)", "",
                 f"Copied from the review VPS snapshot; cases last updated on or after {a.since}. "
                 "R1 = Reviewer 1 (NB-KSC), R2 = Reviewer 2 (NB-87M).", ""]
        current = None
        for n in notes:
            key = (n["case_id"], n["reviewer"])
            if key != current:
                current = key
                lines += ["", f"## {n['case_id']}  ({n['reviewer']}: {n['case_status']})", ""]
            if n["kind"] == "policy_verdict":
                v = ", ".join(f"{k}={val}" for k, val in n["verdict"].items())
                lines.append(f"- **policy verdict**: {v}" + (f"\n  {n['comment']}" if n["comment"] else ""))
            elif n["kind"] == "no_notes":
                lines.append("- (no notes)")
            else:
                where = n["field_path"] or "case comment"
                lines.append(f"- **{n['id']}** [{n['reviewer']} · {n['severity']} · {where}]")
                if n.get("snippet"):
                    lines.append(f"  > {n['snippet'][:300]}")
                lines.append("  " + (n["comment"] or "").replace("\n", "\n  "))
                lines.append("")
        (out / f"{ds_dir.name}.md").write_text("\n".join(lines) + "\n")
        print(ds_dir.name, len(notes), "items")


if __name__ == "__main__":
    main()
