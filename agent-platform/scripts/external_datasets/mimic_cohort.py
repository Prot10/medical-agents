"""Per-condition yield of NeuroBench-style cases in MIMIC-IV (full database or demo).

Counts, per NeuroBench condition, the admissions whose principal diagnosis maps to it and how
many survive each filter a diagnostic case needs: arrival through the ED rather than as a
transfer, a diagnosis new to the patient, a discharge summary, and the studies that serve
tools (head imaging report, CSF, EEG order, ECG). Runs on the compressed CSVs with DuckDB,
so the full database needs no import. Prints counts only.

    uv run --no-project --with duckdb --with pandas python -I \
        agent-platform/scripts/external_datasets/mimic_cohort.py \
        --hosp data/external/mimic-iv-demo/hosp --ed data/external/mimic-iv-ed-demo/ed \
        [--note /path/to/mimic-iv-note/note] [--ecg /path/to/mimic-iv-ecg]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mimic_neuro import icd_chapter, neuro_condition


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hosp", required=True)
    ap.add_argument("--ed", required=True)
    ap.add_argument("--note")
    ap.add_argument("--ecg")
    ap.add_argument("--out")
    ap.add_argument("--all-domains", action="store_true", help="group every principal diagnosis by ICD chapter")
    a = ap.parse_args()
    con = duckdb.connect()
    csv = lambda d, name: f"read_csv_auto('{Path(d) / name}', all_varchar=false, sample_size=-1)"
    con.execute(f"create view dx as select * from {csv(a.hosp, 'diagnoses_icd.csv.gz')}")
    con.execute(f"create view adm as select * from {csv(a.hosp, 'admissions.csv.gz')}")

    codes = con.execute("select distinct cast(icd_code as varchar) code, icd_version from dx").df()
    label = icd_chapter if a.all_domains else neuro_condition
    codes["condition"] = [label(c, v) for c, v in zip(codes.code, codes.icd_version)]
    con.register("icdmap", codes.dropna(subset=["condition"]))
    con.execute("""
        create table cohort as
        select d.subject_id, d.hadm_id, m.condition, substr(cast(d.icd_code as varchar), 1, 3) as fam,
               a.admittime, a.admission_location
        from dx d join icdmap m on cast(d.icd_code as varchar) = m.code and d.icd_version = m.icd_version
        join adm a using (hadm_id)
        where d.seq_num = 1
    """)
    # New to the patient: no earlier admission carries a code of the same condition (neuro) or,
    # across all domains, of the same three-character ICD family.
    same = "substr(cast(d2.icd_code as varchar), 1, 3) = c.fam" if a.all_domains else "m2.condition = c.condition"
    con.execute(f"""
        create table prior as
        select distinct c.hadm_id from cohort c
        join adm a2 on a2.subject_id = c.subject_id and a2.admittime < c.admittime
        join dx d2 on d2.hadm_id = a2.hadm_id
        join icdmap m2 on cast(d2.icd_code as varchar) = m2.code and d2.icd_version = m2.icd_version
        where {same}
    """)
    con.execute(f"create table edh as select distinct hadm_id from {csv(a.ed, 'edstays.csv.gz')} where hadm_id is not null")
    con.execute(f"""
        create table csf as select distinct l.hadm_id from {csv(a.hosp, 'labevents.csv.gz')} l
        join {csv(a.hosp, 'd_labitems.csv.gz')} i using (itemid)
        where i.fluid = 'Cerebrospinal Fluid' and l.hadm_id is not null
    """)
    con.execute(f"""
        create table eeg as select distinct hadm_id from {csv(a.hosp, 'poe.csv.gz')}
        where order_type = 'Neurology' and order_subtype = 'EEG'
    """)
    extra = ""
    if a.note:
        con.execute(f"create table dsum as select distinct hadm_id from {csv(a.note, 'discharge.csv.gz')}")
        con.execute(f"""
            create table headimg as select distinct r.hadm_id from {csv(a.note, 'radiology.csv.gz')} r
            join {csv(a.note, 'radiology_detail.csv.gz')} d using (note_id)
            where d.field_name = 'exam_name'
              and regexp_matches(upper(d.field_value), '(CT|MR|MRA|CTA).*(HEAD|BRAIN|NECK|SPINE)')
        """)
        extra += ", count(*) filter (where hadm_id in (select hadm_id from dsum)) as discharge_note"
        extra += ", count(*) filter (where hadm_id in (select hadm_id from headimg)) as head_imaging_report"
    if a.ecg:
        con.execute(f"""
            create table ecg24 as select distinct c.hadm_id from cohort c
            join {csv(a.ecg, 'record_list.csv')} e on e.subject_id = c.subject_id
              and e.ecg_time between c.admittime - interval 12 hour and c.admittime + interval 24 hour
        """)
        extra += ", count(*) filter (where hadm_id in (select hadm_id from ecg24)) as ecg_24h"
    df = con.execute(f"""
        select condition,
               count(*) as principal,
               count(*) filter (where hadm_id not in (select hadm_id from prior)) as new_dx,
               count(*) filter (where hadm_id not in (select hadm_id from prior)
                                and admission_location not like 'TRANSFER%') as new_dx_not_transfer,
               count(*) filter (where hadm_id in (select hadm_id from edh)) as via_ed,
               count(*) filter (where hadm_id in (select hadm_id from csf)) as csf_labs,
               count(*) filter (where hadm_id in (select hadm_id from eeg)) as eeg_order
               {extra}
        from cohort group by condition order by principal desc
    """).df()
    with pd.option_context("display.width", 200):
        print(df.to_string(index=False))
    if a.out:
        df.to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
