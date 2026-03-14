"""Print statistics for the NeuroBench dataset."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def compute_stats(cases_dir: str | Path) -> None:
    cases_dir = Path(cases_dir)
    if not cases_dir.exists():
        print(f"Directory not found: {cases_dir}")
        sys.exit(1)

    files = sorted(cases_dir.glob("*.json"))
    if not files:
        print("No cases found.")
        return

    conditions = Counter()
    difficulties = Counter()
    encounter_types = Counter()
    ages = []
    sexes = Counter()
    modalities_present = Counter()
    followup_counts = []
    errors = []

    for f in files:
        try:
            data = json.loads(f.read_text())
        except Exception as e:
            errors.append(f"{f.name}: {e}")
            continue

        conditions[data.get("condition", "unknown")] += 1
        difficulties[data.get("difficulty", "unknown")] += 1
        encounter_types[data.get("encounter_type", "unknown")] += 1

        patient = data.get("patient", {})
        demo = patient.get("demographics", {})
        if "age" in demo:
            ages.append(demo["age"])
        if "sex" in demo:
            sexes[demo["sex"]] += 1

        tos = data.get("initial_tool_outputs", {})
        for mod in ["eeg", "mri", "ecg", "labs", "csf", "literature_search", "drug_interactions"]:
            if tos.get(mod) is not None:
                modalities_present[mod] += 1

        followup_counts.append(len(data.get("followup_outputs", [])))

    total = len(files) - len(errors)
    print(f"{'=' * 60}")
    print(f"NeuroBench Dataset Statistics")
    print(f"{'=' * 60}")
    print(f"Total cases: {total}  (errors: {len(errors)})")
    print()

    print("By condition:")
    for cond, count in sorted(conditions.items()):
        print(f"  {cond:45s} {count:3d}")
    print()

    print("By difficulty:")
    for diff, count in sorted(difficulties.items()):
        print(f"  {diff:20s} {count:3d}")
    print()

    print("By encounter type:")
    for et, count in sorted(encounter_types.items()):
        print(f"  {et:20s} {count:3d}")
    print()

    if ages:
        print(f"Age: min={min(ages)}, max={max(ages)}, mean={sum(ages)/len(ages):.1f}")
    print(f"Sex: {dict(sexes)}")
    print()

    print("Modality coverage:")
    for mod, count in sorted(modalities_present.items(), key=lambda x: -x[1]):
        pct = 100 * count / total if total else 0
        print(f"  {mod:20s} {count:3d} ({pct:.0f}%)")
    print()

    if followup_counts:
        print(f"Follow-ups: min={min(followup_counts)}, max={max(followup_counts)}, "
              f"mean={sum(followup_counts)/len(followup_counts):.1f}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")


if __name__ == "__main__":
    cases_dir = sys.argv[1] if len(sys.argv) > 1 else "data/neurobench_v1/cases"
    compute_stats(cases_dir)
