"""Structure of the downloaded PhysioNet tables, aggregates only.

For every .csv / .csv.gz under the given folders: row count, distinct subject_id / hadm_id /
stay_id, and per column its type, share of nulls and, for text columns, the median length in
characters. For a JSON file, its top-level keys and the size of each value. Never prints a value
of the data: PhysioNet's DUA forbids sending credentialed records to a service that retains them,
and this output is read by a Claude session.

    uv run --no-project --python 3.12 --with duckdb python -I mimic_profile.py \
        /eos/user/a/aprotani/physionet/mimic-iv-ext-cdm/1.1 ... [--skip labevents.csv.gz]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb

KEYS = ("subject_id", "hadm_id", "stay_id", "note_id")


def profile_csv(con: duckdb.DuckDBPyConnection, path: Path) -> None:
    src = f"read_csv_auto('{path}', sample_size=-1)"
    cols = con.execute(f"describe select * from {src}").fetchall()
    names = [c[0] for c in cols]
    aggs = ["count(*)"]
    aggs += [f'count(distinct "{k}")' for k in KEYS if k in names]
    for name, typ, *_ in cols:
        aggs.append(f'avg(("{name}" is null)::int)')
        if typ == "VARCHAR":
            aggs.append(f'median(length("{name}"))')
    row = con.execute(f"select {', '.join(aggs)} from {src}").fetchone()
    it = iter(row)
    n = next(it)
    keys = {k: next(it) for k in KEYS if k in names}
    print(f"\n## {path.parent.name}/{path.name}: {n:,} rows" + "".join(f", {v:,} {k}" for k, v in keys.items()))
    for name, typ, *_ in cols:
        null = next(it)
        med = f", median {next(it):.0f} chars" if typ == "VARCHAR" else ""
        print(f"  {name:<28} {typ:<10} null {null:6.1%}{med}")


def profile_json(path: Path) -> None:
    data = json.loads(path.read_text())
    print(f"\n## {path.parent.name}/{path.name}: JSON {type(data).__name__}")
    if isinstance(data, dict):
        for k, v in data.items():
            print(f"  {k:<28} {type(v).__name__} of {len(v) if hasattr(v, '__len__') else 1:,}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("folders", nargs="+", type=Path)
    ap.add_argument("--skip", nargs="*", default=[], help="file names still downloading")
    a = ap.parse_args()
    con = duckdb.connect()
    con.execute("set memory_limit = '16GB'; set threads = 4")
    for folder in a.folders:
        for path in sorted(folder.rglob("*")):
            if path.name in a.skip or not path.is_file():
                continue
            if path.name.endswith((".csv", ".csv.gz")):
                try:
                    profile_csv(con, path)
                except duckdb.Error as e:  # a file still downloading is a truncated gzip
                    print(f"\n## {path.parent.name}/{path.name}: unreadable ({type(e).__name__}), skipped")
            elif path.suffix == ".json":
                profile_json(path)


if __name__ == "__main__":
    main()
