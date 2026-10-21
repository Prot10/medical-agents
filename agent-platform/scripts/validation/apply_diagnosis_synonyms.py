"""Expand ICD-keyed diagnosis synonyms into every case's accepted labels and codes.

    uv run python agent-platform/scripts/validation/apply_diagnosis_synonyms.py [--check]

Idempotent: re-running after editing `config/policies/diagnosis_synonyms.yaml` adds only what
is missing. `--check` exits non-zero if any case would change (CI guard).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
SYNONYMS = ROOT / "agent-platform/config/policies/diagnosis_synonyms.yaml"
CASES = ROOT / "data/neurobench/cases"


def _dump(data: dict) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def entries_for(code: str, condition: str, table: dict) -> list[dict]:
    """Entries keyed by the exact code or its 3-character category, honouring `conditions`."""
    keys = {code, code[:3]}
    chosen = []
    for key, entry in table.items():
        if key.split("+")[0] not in keys:
            continue
        if entry.get("conditions") and condition not in entry["conditions"]:
            continue
        chosen.append(entry)
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    table = yaml.safe_load(SYNONYMS.read_text())
    changed = []
    reformatted = 0
    for path in sorted(CASES.glob("*.json")):
        raw = path.read_text()
        data = json.loads(raw)
        reformatted += _dump(data) != raw  # canonical form: indent 2, sorted keys, ASCII
        diagnosis = data["ground_truth"]["diagnosis"]
        labels, codes = list(diagnosis["accepted"]), list(diagnosis["icd_codes"])
        # Entries are selected by the case's own primary code (always first); codes added by
        # earlier runs never cascade into further entries.
        for entry in entries_for(codes[0], data["condition"], table):
            labels += [item for item in entry.get("labels", []) if item not in labels]
            codes += [item for item in entry.get("codes", []) if item not in codes]
        if labels != diagnosis["accepted"] or codes != diagnosis["icd_codes"]:
            diagnosis["accepted"], diagnosis["icd_codes"] = labels, codes
            changed.append(path)
            if not args.check:
                path.write_text(_dump(data))
    verb = "would change" if args.check else "updated"
    print(f"{verb} {len(changed)} of {len(list(CASES.glob('*.json')))} cases ({reformatted} were not in canonical form)")
    if args.check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
