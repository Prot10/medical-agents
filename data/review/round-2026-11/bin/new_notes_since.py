"""Print the physician notes in an annotation folder that no round has ruled on yet.

    python3 -I data/review/round-2026-11/bin/new_notes_since.py ANNOTATIONS_DIR [--jsonl OUT]

ANNOTATIONS_DIR is a copy of the review app's `data/review/annotations/neurobench` (one folder
per reviewer code, one JSON file per case). A note is "handled" when its id is in this round's
`ledger.jsonl` or in the October round's notes (`data/review/round-2026-10/notes/*.json`, if
present). Item ids: field annotations and case comments use their own `id`; a policy verdict
uses `<reviewer_code[:6]>:<case_id>:policy_verdict`, as in new_notes.jsonl. A handled item whose
text or verdict changed since it was ruled on is printed too, flagged CHANGED (the ledger stores
a sha256 of the text it ruled on).
"""
from __future__ import annotations
import argparse, glob, hashlib, json, os
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
REVIEWERS = {"NB-87MF-FBTV-TPWE": "R2", "NB-KSC3-TWUA-QDTM": "R1"}

def digest(item: dict) -> str:
    body = json.dumps({"comment": item.get("comment") or "", "verdict": {k: v for k, v in (item.get("verdict") or {}).items() if k != "submitted_at"}}, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()

def flatten(folder: str):
    for f in sorted(glob.glob(os.path.join(folder, "*", "*.json"))):
        d = json.loads(Path(f).read_text())
        base = {"case_id": d["case_id"], "condition": d["case_id"].rsplit("-", 1)[0], "reviewer": d["reviewer_code"], "case_status": d.get("status")}
        for a in d.get("field_annotations") or []:
            yield {**base, "kind": "field", "note_id": a["id"], "field_path": a.get("field_path"), "field_snippet": a.get("snippet") or a.get("field_snippet"), "severity": a.get("severity"), "comment": a.get("comment"), "created_at": a.get("created_at")}
        for a in d.get("case_comments") or []:
            yield {**base, "kind": "case_comment", "note_id": a["id"], "severity": a.get("severity"), "comment": a.get("comment"), "created_at": a.get("created_at")}
        pv = d.get("policy_verdict")
        if pv:
            verdict = {k: v for k, v in pv.items() if k not in ("comment", "id")}
            yield {**base, "kind": "policy_verdict", "note_id": f"{d['reviewer_code'][:6]}:{d['case_id']}:policy_verdict", "verdict": verdict, "comment": pv.get("comment"), "created_at": pv.get("submitted_at")}

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("annotations"); ap.add_argument("--jsonl", help="also write the new items to this file")
    a = ap.parse_args()
    ruled: dict[str, str | None] = {}
    ledger = HERE / "ledger.jsonl"
    if ledger.exists():
        for line in ledger.read_text().splitlines():
            if line.strip():
                r = json.loads(line); ruled[r["note_id"]] = r.get("text_sha256")
    for f in glob.glob(str(HERE.parent / "round-2026-10/notes/*.json")):
        for n in json.loads(Path(f).read_text()):
            ruled.setdefault(n["id"], None)
    new = []
    for item in flatten(a.annotations):
        nid = item["note_id"]
        if item["kind"] == "policy_verdict" and not (item.get("comment") or "").strip() and nid not in ruled:
            item["empty_verdict"] = True
        if nid not in ruled:
            new.append(item)
        elif ruled[nid] and ruled[nid] != digest(item):
            item["changed_since_ruling"] = True; new.append(item)
    for item in new:
        flag = " CHANGED" if item.get("changed_since_ruling") else ""
        print(f"{item['case_id']}\t{REVIEWERS.get(item['reviewer'], item['reviewer'])}\t{item['kind']}\t{item['note_id']}{flag}\t{(item.get('comment') or '').strip()[:100]!r}")
    print(f"# {len(new)} items not in the ledger (or changed since ruled)")
    if a.jsonl:
        Path(a.jsonl).write_text("".join(json.dumps(i, ensure_ascii=False) + "\n" for i in new))

if __name__ == "__main__":
    main()
