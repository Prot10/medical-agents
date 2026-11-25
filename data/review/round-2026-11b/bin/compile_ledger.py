"""Build data/review/round-2026-11b/ledger.jsonl from the per-case rulings.

    python3 -I data/review/round-2026-11b/bin/compile_ledger.py RULINGS_DIR NOTES_JSONL [--check]

RULINGS_DIR holds <CASE>.json (a list of {note_id, status, field_path_now, what, reason});
NOTES_JSONL is the round's new_notes.jsonl. Every note must have exactly one ruling with a valid
status. A fixed field note whose target no longer exists (e.g. a removed literature step) gets
field_path_now "(removed)". Each row records the cases changed (the note's case, when its file differs from the base
commit 332e52d9) and a sha256 of the ruled text, so new_notes_since.py can spot edited notes.
"""
from __future__ import annotations
import glob, json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "round-2026-11/bin"))
from new_notes_since import digest

ROOT = Path(__file__).resolve().parents[4]
STATUSES = {"FIXED", "DECLINED", "ALREADY-FIXED", "CENTRAL", "NEEDS-ANDREA", "NO-ACTION"}
REV = {"NB-87MF-FBTV-TPWE": "R2", "NB-KSC3-TWUA-QDTM": "R1"}

def main() -> None:
    rdir, notes_path = sys.argv[1], sys.argv[2]
    notes = [json.loads(l) for l in open(notes_path) if l.strip()]
    changed = set(subprocess.run(["git", "diff", "--name-only", "332e52d9", "--", "data/neurobench/cases"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split())
    rulings: dict[str, dict] = {}; errors = []
    for f in sorted(glob.glob(os.path.join(rdir, "*.json"))):
        for r in json.loads(Path(f).read_text()):
            if r["note_id"] in rulings: errors.append(f"duplicate ruling {r['note_id']}")
            r["_file"] = Path(f).stem; rulings[r["note_id"]] = r
    rows = []
    for n in notes:
        r = rulings.get(n["note_id"])
        if r is None: errors.append(f"no ruling: {n['case_id']} {n['note_id']}"); continue
        if r.get("status") not in STATUSES: errors.append(f"bad status {r.get('status')} {n['note_id']}")
        if r["_file"] != n["case_id"]: errors.append(f"ruling for {n['note_id']} filed under {r['_file']}, note is on {n['case_id']}")
        if r.get("status") in {"DECLINED", "CENTRAL", "NEEDS-ANDREA"} and not (r.get("reason") or "").strip(): errors.append(f"{r['status']} without reason {n['note_id']}")
        rows.append({"note_id": n["note_id"], "case_id": n["case_id"], "condition": n["condition"], "reviewer": REV.get(n["reviewer"], n["reviewer"]),
                     "kind": n["kind"], "status": r["status"],
                     "cases_changed": [n["case_id"]] if f"data/neurobench/cases/{n['case_id']}.json" in changed else [],
                     "field_path_seen": n.get("field_path") or "", "field_path_now": r.get("field_path_now") or ("(removed)" if n["kind"] == "field" and r["status"] in {"FIXED", "ALREADY-FIXED"} else ""),
                     "what": r.get("what") or "", "reason": r.get("reason") or "", "text_sha256": digest(n), "round": "2026-11b"})
    extra = set(rulings) - {n["note_id"] for n in notes}
    errors += [f"ruling for unknown note {x}" for x in sorted(extra)]
    for e in errors: print("ERROR", e)
    print(f"{len(rows)} rows, {len(errors)} errors")
    if "--check" not in sys.argv and not errors:
        (ROOT / "data/review/round-2026-11b/ledger.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
