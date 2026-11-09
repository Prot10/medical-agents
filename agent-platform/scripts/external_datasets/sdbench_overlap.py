"""How many MIMIC-IV-Ext-SDBench cases fall in the NeuroBench conditions. Counts only.

Maps each SDBench case's ``mimic_note_id`` to its admission (MIMIC-IV-Note ``discharge``), then
the admission's principal diagnosis to a NeuroBench condition (``mimic_neuro``), and counts cases
per condition and split. Never prints a case text or diagnosis string (PhysioNet DUA).

    uv run --no-project --python 3.12 --with duckdb python -I sdbench_overlap.py \
        --sdbench .../mimic-iv-ext-sdbench/1.0.0/dataset.json --hosp .../hosp --note .../note
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mimic_neuro import icd_chapter, neuro_condition


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sdbench", required=True)
    ap.add_argument("--hosp", required=True)
    ap.add_argument("--note", required=True)
    a = ap.parse_args()
    con = duckdb.connect()
    con.execute(f"""
        create table sd as select case_id, mimic_note_id, unnest(case_sets) as split
        from read_json_auto('{a.sdbench}', maximum_object_size=100000000)
    """)
    con.execute(f"""
        create table pdx as
        select sd.case_id, sd.split, d.icd_code, d.icd_version
        from sd join read_csv_auto('{Path(a.note) / 'discharge.csv.gz'}', sample_size=-1) n
          on n.note_id = sd.mimic_note_id
        join read_csv_auto('{Path(a.hosp) / 'diagnoses_icd.csv.gz'}', sample_size=-1) d
          on d.hadm_id = n.hadm_id and d.seq_num = 1
    """)
    rows = con.execute("select case_id, split, icd_code, icd_version from pdx").fetchall()
    total = con.execute("select count(*) from sd").fetchone()[0]
    print(f"{total} SDBench cases, {len(rows)} linked to a principal diagnosis")
    by_cond: dict[tuple[str, str], int] = {}
    by_chap: dict[str, int] = {}
    for _, split, code, v in rows:
        cond = neuro_condition(str(code), int(v)) or "-"
        by_cond[(cond, split)] = by_cond.get((cond, split), 0) + 1
        by_chap[icd_chapter(str(code), int(v))] = by_chap.get(icd_chapter(str(code), int(v)), 0) + 1
    print("\nICD chapter of the principal diagnosis:", dict(sorted(by_chap.items(), key=lambda kv: -kv[1])))
    print("\nNeuro conditions (condition: train/validation/test):")
    conds = sorted({c for c, _ in by_cond if c != "-"})
    for c in conds:
        print(f"  {c:<45} " + " / ".join(str(by_cond.get((c, s), 0)) for s in ("train", "validation", "test")))


if __name__ == "__main__":
    main()
