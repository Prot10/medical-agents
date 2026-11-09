"""Which tests the clinicians actually ordered for the NeuroBench conditions in MIMIC-IV. Counts only.

For admissions whose principal diagnosis maps to one of the 20 NeuroBench conditions
(``mimic_neuro``), counts the admissions that have each orderable item, per condition:

- ``radiology``: ``exam_name`` of the radiology reports (MIMIC-IV-Note ``radiology_detail``);
- ``poe``: order type / subtype of the provider order entries (EEG, echo, consults, ...);
- ``lab``: lab items (label, fluid, category) in ``labevents``;
- ``micro``: specimen type and test name in ``microbiologyevents``.

Writes one row per (condition, source, item) with the number of admissions; items seen in fewer
than ``--min-admissions`` admissions overall are dropped. Names of tests and counts only, never a
result or a note (PhysioNet DUA: this output is read by a Claude session).

    uv run --no-project --python 3.12 --with duckdb --with pandas python -I mimic_order_catalogue.py \
        --hosp .../mimiciv/3.1/hosp --note .../mimic-iv-note/2.2/note --out orders.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mimic_neuro import neuro_condition


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hosp", required=True)
    ap.add_argument("--note", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-admissions", type=int, default=10)
    a = ap.parse_args()
    con = duckdb.connect()
    con.execute("set memory_limit = '24GB'; set threads = 8")
    csv = lambda d, name: f"read_csv_auto('{Path(d) / name}', sample_size=-1)"
    codes = con.execute(
        f"select distinct icd_code code, icd_version v from {csv(a.hosp, 'diagnoses_icd.csv.gz')} where seq_num = 1"
    ).df()
    codes["condition"] = [neuro_condition(c, v) for c, v in zip(codes.code, codes.v)]
    codes = codes[codes.condition.notna() & ~codes.condition.fillna("").str.startswith("other:")]
    con.register("icdmap", codes)
    con.execute(f"""
        create table cohort as select d.hadm_id, m.condition
        from {csv(a.hosp, 'diagnoses_icd.csv.gz')} d
        join icdmap m on d.icd_code = m.code and d.icd_version = m.v where d.seq_num = 1
    """)
    con.execute(f"""
        create table items as
        select distinct c.condition, c.hadm_id, 'radiology' as source, upper(trim(d.field_value)) as item
        from {csv(a.note, 'radiology.csv.gz')} r
        join {csv(a.note, 'radiology_detail.csv.gz')} d using (note_id)
        join cohort c on c.hadm_id = r.hadm_id
        where d.field_name = 'exam_name'
        union
        select distinct c.condition, c.hadm_id, 'poe', p.order_type || ' / ' || coalesce(p.order_subtype, '-')
        from {csv(a.hosp, 'poe.csv.gz')} p join cohort c using (hadm_id)
        union
        select distinct c.condition, c.hadm_id, 'lab', i.label || ' | ' || i.fluid || ' | ' || i.category
        from {csv(a.hosp, 'labevents.csv.gz')} l join {csv(a.hosp, 'd_labitems.csv.gz')} i using (itemid)
        join cohort c on c.hadm_id = l.hadm_id
        union
        select distinct c.condition, c.hadm_id, 'micro', m.spec_type_desc || ' | ' || m.test_name
        from {csv(a.hosp, 'microbiologyevents.csv.gz')} m join cohort c on c.hadm_id = m.hadm_id
    """)
    con.execute(f"""
        copy (
            with keep as (select source, item from items group by all
                          having count(distinct hadm_id) >= {a.min_admissions})
            select i.condition, i.source, i.item, count(distinct i.hadm_id) as admissions,
                   (select count(*) from cohort c where c.condition = i.condition) as condition_admissions
            from items i join keep using (source, item)
            group by all order by source, item, condition
        ) to '{a.out}' (header, delimiter ',')
    """)
    total = con.execute("select count(*) from cohort").fetchone()[0]
    n = con.execute(f"select source, count(distinct item) from read_csv_auto('{a.out}') group by 1 order by 1").fetchall()
    print(f"{total:,} cohort admissions; items kept (>= {a.min_admissions} admissions): {n}")


if __name__ == "__main__":
    main()
