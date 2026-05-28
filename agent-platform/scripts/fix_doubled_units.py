"""Collapse doubled measurement-unit artifacts in case JSON string values.

A generator artifact duplicated unit tokens in interpretation strings, e.g.
"FVC 2.2 L L (H)", "Increase of 8 bpm bpm", "transferrin 2.8% %". Only an
explicit allow-list of unit tokens (and the "<num>% %" form) is collapsed —
never generic word repetition — so legitimate prose is untouched.

Usage:
    uv run python agent-platform/scripts/fix_doubled_units.py            # dry-run
    uv run python agent-platform/scripts/fix_doubled_units.py --apply
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CASES_DIR = Path("data/neurobench_v5/cases")

# Exact unit tokens observed doubled. Order longest-first so multi-char units
# (cells/uL, cmH2O, g/dL) match before short ones.
UNITS = [
    "cells/uL", "cells/µL", "cmH2O", "mmHg", "g/dL", "mg/dL", "mg/L", "percentile",
    "seconds", "bpm", "ms", "L",
]
_UNIT_RE = re.compile(r"\b(" + "|".join(re.escape(u) for u in UNITS) + r")\s+\1\b")
_PCT_RE = re.compile(r"(\d\s*%)\s+%")


def _fix_str(s: str) -> str:
    prev = None
    while prev != s:  # collapse triples too (e.g. "L L L")
        prev = s
        s = _UNIT_RE.sub(r"\1", s)
        s = _PCT_RE.sub(r"\1", s)
    return s


def _walk(o):
    """Recursively fix strings; return (new_obj, n_fixes)."""
    if isinstance(o, str):
        new = _fix_str(o)
        return new, (1 if new != o else 0)
    if isinstance(o, dict):
        n = 0
        out = {}
        for k, v in o.items():
            nv, c = _walk(v)
            out[k] = nv
            n += c
        return out, n
    if isinstance(o, list):
        n = 0
        out = []
        for v in o:
            nv, c = _walk(v)
            out.append(nv)
            n += c
        return out, n
    return o, 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--cases-dir", type=Path, default=CASES_DIR)
    args = p.parse_args()

    total_fixes = 0
    files_changed = 0
    examples: list[str] = []
    for f in sorted(args.cases_dir.glob("*.json")):
        raw = f.read_text()
        data = json.loads(raw)
        fixed, n = _walk(data)
        if n:
            total_fixes += n
            files_changed += 1
            if len(examples) < 8:
                examples.append(f.name)
            if args.apply:
                use_literal = any(ord(c) > 127 for c in raw)
                f.write_text(json.dumps(fixed, indent=2, ensure_ascii=not use_literal) + "\n")

    print(f"{'APPLIED' if args.apply else 'DRY-RUN'}: {total_fixes} string values fixed "
          f"across {files_changed} files")
    if examples:
        print("  e.g.:", ", ".join(examples))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
