"""Expand ICD-keyed diagnosis synonyms into every case's accepted labels and codes.

    uv run python agent-platform/scripts/validation/apply_diagnosis_synonyms.py [--check]

Idempotent: re-running after editing `config/policies/diagnosis_synonyms.yaml` adds only what
is missing. `--check` exits non-zero if any case would change (CI guard) and names the cases.

An entry may be restricted to conditions (`conditions: [...]`) or to named cases (`cases: [...]`),
e.g. a variant label that is right for one GBS case and wrong for the others. `--prune` also removes
synonyms an entry no longer grants: every label after `accepted[0]` that some entry of the table
lists, and every code after `icd_codes[0]`, is recomputed from the entries that apply now. Labels no
entry lists are case-specific and are kept, except those named under the table's `RETIRED` key
(labels the table once granted and no longer does). An entry's `rejected: [...]` labels are added to
`ground_truth.diagnosis.rejected` (answers naming them score no diagnosis credit) and are pruned the
same way. `except_cases: [...]` excludes named cases from
an otherwise applicable entry. `--cases` / `--conditions` limit the run (check, apply or prune) to
those cases, so a change can be applied to one condition while other conditions are being edited.
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


def entries_for(code: str, condition: str, table: dict, case_id: str = "") -> list[dict]:
    """Entries keyed by the exact code or its 3-character category, honouring `conditions`/`cases`."""
    keys = {code, code[:3]}
    chosen = []
    for key, entry in table.items():
        if key.split("+")[0] not in keys:
            continue
        if entry.get("conditions") and condition not in entry["conditions"]:
            continue
        if entry.get("cases") and case_id not in entry["cases"]:
            continue
        if case_id in entry.get("except_cases", []):
            continue
        chosen.append(entry)
    return chosen


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--prune", action="store_true", help="also remove synonyms no entry grants any more")
    parser.add_argument("--cases", nargs="+", default=[], help="limit the run to these case ids")
    parser.add_argument("--conditions", nargs="+", default=[], help="limit the run to these conditions")
    args = parser.parse_args()
    table = yaml.safe_load(SYNONYMS.read_text())
    granted = {label for entry in table.values() for label in entry.get("labels", [])}
    granted |= set(table.get("RETIRED", {}).get("retired_labels", []))
    granted_rejected = {label for entry in table.values() for label in entry.get("rejected", [])}
    changed = []
    reformatted = 0
    for path in sorted(CASES.glob("*.json")):
        raw = path.read_text()
        data = json.loads(raw)
        if args.cases and data["case_id"] not in args.cases:
            continue
        if args.conditions and data["condition"] not in args.conditions:
            continue
        reformatted += _dump(data) != raw  # canonical form: indent 2, sorted keys, ASCII
        diagnosis = data["ground_truth"]["diagnosis"]
        labels, codes = list(diagnosis["accepted"]), list(diagnosis["icd_codes"])
        rejected = list(diagnosis.get("rejected", []))
        if args.prune:
            labels = labels[:1] + [item for item in labels[1:] if item not in granted]
            codes = codes[:1]
            rejected = [item for item in rejected if item not in granted_rejected]
        # Entries are selected by the case's own primary code (always first); codes added by
        # earlier runs never cascade into further entries.
        for entry in entries_for(codes[0], data["condition"], table, data["case_id"]):
            labels += [item for item in entry.get("labels", []) if item not in labels]
            codes += [item for item in entry.get("codes", []) if item not in codes]
            rejected += [item for item in entry.get("rejected", []) if item not in rejected]
        if labels != diagnosis["accepted"] or codes != diagnosis["icd_codes"] or rejected != diagnosis.get("rejected", []):
            diagnosis["accepted"], diagnosis["icd_codes"] = labels, codes
            if rejected or "rejected" in diagnosis:
                diagnosis["rejected"] = rejected
            changed.append(path)
            if not args.check:
                path.write_text(_dump(data))
    verb = "would change" if args.check else "updated"
    print(f"{verb} {len(changed)} of {len(list(CASES.glob('*.json')))} cases ({reformatted} were not in canonical form)")
    if args.check and changed:
        print("\n".join(f"  {path.stem}" for path in changed))
        sys.exit(1)


if __name__ == "__main__":
    main()
