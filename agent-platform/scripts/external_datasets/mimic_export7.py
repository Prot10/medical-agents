"""Task 07 export: the final 100 cases to $W/out/07_cases, the selection to $W/out/07_selection.csv (the 100 are the rows with a
case_id and no exclusion), and the per-round blind-review files merged to $W/tmp/blind7_rN_all.json (workspace only).
No record content in this file.

    python -I mimic_export7.py --out $W/out --tmp $W/tmp
"""
from __future__ import annotations

import argparse
import glob
import json
import shutil
from pathlib import Path

import pandas as pd


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--tmp", required=True)
    a = ap.parse_args()
    out, tmp = Path(a.out), Path(a.tmp)
    for p in (out, tmp):
        if not str(p.resolve()).startswith(("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")):
            raise SystemExit("paths must be under the PhysioNet workspace")
    sel = pd.read_csv(out / "06_selection.csv")
    live = sorted(sel[sel.case_id.notna() & sel.exclusion.isna()].case_id)
    dst = out / "07_cases"
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir()
    for c in live:
        shutil.copy(out / "06_cases" / f"{c}.json", dst / f"{c}.json")
    sel.to_csv(out / "07_selection.csv", index=False)
    for d in sorted(glob.glob(str(tmp / "blind7_r[0-9]"))):
        allr = {}
        for f in sorted(glob.glob(f"{d}/review_*.json")):
            r, _ = json.JSONDecoder().raw_decode(Path(f).read_text())
            allr.update(r)
        (tmp / f"{Path(d).name}_all.json").write_text(json.dumps(allr))
    print(len(live), "cases exported to", dst, "| selection rows", len(sel))


if __name__ == "__main__":
    main()
