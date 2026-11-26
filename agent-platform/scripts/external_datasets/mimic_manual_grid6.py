"""Task 06, re-read fix (decision 35): a strength or reflex grid of the admission exam that the reader
left out of the manual file is added to it verbatim (header line and its side rows), so the builder's
cell-level grid rule can serve the attributable cells. Only the admission exam (text before the first
discharge-exam heading) is searched; a grid already present in the manual field is left alone.
Manual files hold record content: written whole, only under the PhysioNet workspace. No record
content in this file.

    python -I mimic_manual_grid6.py --out $W/out [--cases ...]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

STRENGTH = re.compile(r"\b(?:Delt|D|Bic|Bi|Tri|T|WrE|WE|WrF|WF|FFl|FF|FE|IO|IP|Quad|Q|Ham|H|TA|Gastroc|Gas|EHL|ECR|Fext|Fflx|Grip)\b")
REFLEX = re.compile(r"\b(?:Bi|Tri|Br|Brach|BR|Pat|Ach|Pec|Toe|Plantar)\b")
REFLEX_HDR = re.compile(r"\b(?:Bi|Tri|Br|Brach|BR|Pat|Ach|Pec)\b")
SIDE = re.compile(r"^\s*(?:L|R|Left|Right|LUE|RUE|LLE|RLE|Lt|Rt)\b")
DISCH = re.compile(r"(?i)discharge\s+(?:physical\s+)?exam|DISCHARGE EXAM|Exam on discharge|At discharge")


def grids(note: str) -> list[tuple[str, str]]:
    adm = note[:DISCH.search(note).start()] if DISCH.search(note) else note
    lines = adm.splitlines()
    out = []
    for i, ln in enumerate(lines):
        toks = ln.split()
        if len(toks) < 4 or SIDE.match(ln):
            continue
        ns, nr = len(STRENGTH.findall(ln)), len(REFLEX.findall(ln))
        if ns < 3 and nr < 3:
            continue
        # task 07: the kind comes from the section label above the grid, never from the column names alone
        kind = None
        for up in reversed(lines[max(0, i - 12):i]):  # the nearest exam-section label above the grid
            m_ = re.search(r"(?i)\b(DTRs?|reflex\w*|motor|strength|power|sensory|sensation|coordination|gait|cranial)\b", up)
            if m_:
                lab = m_.group(1).lower()
                kind = "reflexes" if lab.startswith(("dtr", "reflex")) else ("motor" if lab in ("motor", "strength", "power") else None)
                break
        if not kind:
            continue
        rows = []
        for ln2 in lines[i + 1:i + 6]:
            if not rows and re.fullmatch(r"\s*(?:(?:[CTLS]\d(?:[-/][CTLS]?\d)?|___)\s*)+", ln2 or "") and ln2.strip():
                continue  # a line of root levels under the header (task 07)
            if SIDE.match(ln2):
                rows.append(" ".join(ln2.split()))
            elif rows and ln2.strip() and re.fullmatch(r"[\d+\-*\s_]+", ln2.strip()):
                rows[-1] += " " + " ".join(ln2.split())  # a wrapped tail of the row
            elif rows:
                break
        if rows:
            out.append((kind, " | ".join([" ".join(toks)] + rows)))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cases", nargs="*", default=[])
    a = ap.parse_args()
    out = Path(a.out)
    sel = pd.read_csv(out / "06_selection.csv")
    live = sel[sel.case_id.notna() & (sel.case_id != "") & (sel.exclusion.isna() | (sel.exclusion == ""))].case_id
    added = {"motor": 0, "reflexes": 0}
    for cid in (a.cases or live):
        f = out / "06_manual" / f"{cid}.json"
        if not f.exists():
            continue
        m = json.loads(f.read_text())
        if m.get("no_grid_insert"):
            continue
        note = json.loads((out / "02_source" / f"{cid}.json").read_text())["discharge"][0]["text"]
        ne = m["neurological_exam"]
        have = json.dumps(ne)
        done, changed = set(), False
        for kind, g in grids(note):
            rx = STRENGTH if kind == "motor" else REFLEX_HDR
            field_txt = str(ne.get(kind) or "")  # task 07: only the grid's own field counts (Plantar / Toe lines are not a grid)
            parts = g.split(" | ")
            flat = " ".join(have.split())
            if any(" ".join(p.split()) in flat for p in parts):
                continue  # this grid's header or a row is already in the manual file (in whatever form the reader kept it)
            done.add(kind)
            ne[kind] = (str(ne.get(kind) or "").rstrip(" |") + " | " + g).strip(" |")
            m.setdefault("other_edits", []).append(f"task-06 re-read: admission {kind} grid added from the note (decision 35)")
            added[kind] += 1
            changed = True
        if changed:
            f.write_text(json.dumps(m, indent=1) + "\n")
    print("grids added to manual files:", added)


if __name__ == "__main__":
    main()
