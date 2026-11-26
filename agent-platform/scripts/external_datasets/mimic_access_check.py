"""Check that every MIMIC file a NeuroBench conversion needs opens and decompresses. Counts only.

For each ``*.csv.gz`` under the given folders: compressed size, the header (field names), and,
with ``--full``, a full decompression (gzip CRC checked at the end of the stream) with the
number of decompressed bytes and newline characters. Notes hold multi-line quoted text, so the
newline count is an upper bound of rows there, not a row count. Never prints a data row.

    nice -n 10 python3 -I mimic_access_check.py [--full] DIR [DIR ...]
"""

from __future__ import annotations

import argparse
import gzip
import sys
import time
import zlib
from pathlib import Path

CHUNK = 1 << 24


def check(path: Path, full: bool) -> dict:
    row = {"file": str(path), "gz_mb": round(path.stat().st_size / 1e6, 1)}
    t0 = time.time()
    try:
        with gzip.open(path, "rt", newline="") as f:
            row["fields"] = f.readline().strip()
        if full:
            raw = nl = 0
            with gzip.open(path, "rb") as f:
                while chunk := f.read(CHUNK):
                    raw += len(chunk)
                    nl += chunk.count(b"\n")
            row["raw_mb"], row["newlines"] = round(raw / 1e6, 1), nl
        row["status"] = "ok"
    except (OSError, EOFError, zlib.error) as e:
        row["status"] = f"ERROR {type(e).__name__}: {e}"
    row["sec"] = round(time.time() - t0, 1)
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--full", action="store_true", help="decompress every file to the end")
    a = ap.parse_args()
    bad = 0
    for d in a.dirs:
        for p in sorted(Path(d).glob("*.csv.gz")):
            r = check(p, a.full)
            bad += r["status"] != "ok"
            extra = f" raw_mb={r['raw_mb']} newlines={r['newlines']}" if "raw_mb" in r else ""
            print(f"{r['status']:>3} {r['gz_mb']:>9} MB{extra} {r['sec']}s {r['file']}\n      fields: {r.get('fields', '')}", flush=True)
    print(f"files with errors: {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
