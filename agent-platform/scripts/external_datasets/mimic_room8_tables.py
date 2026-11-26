"""Task 08: the markdown tables of 08_room.md from REPORT/08_room.json (counts only). No record content here.

    python -I mimic_room8_tables.py --report $W/report
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def fmt(x):
    return "–" if x is None or (isinstance(x, float) and x != x) else (f"{x:g}" if isinstance(x, (int, float)) else str(x))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    a = ap.parse_args()
    J = json.loads((Path(a.report) / "08_room.json").read_text())
    print("| Condition | Strict | In the 100 | Read (any task) | Excluded on reading | Main exclusions | Strict, never read | of which patient in 100 | Distinct new patients | Yield 04–07 (kept/read) | Expected new cases |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in J["A"]:
        y = "–" if r["yield"] is None else f"{r['kept_0407']}/{r['read_0407']} = {r['yield']:.2f}" + (f" (95% CI {r['yield_ci'][0]:.2f}–{r['yield_ci'][1]:.2f})" if r["yield_ci"] else "")
        e = fmt(r["expected_new"]) + (f" ({fmt(r['expected_new_range'][0])}–{fmt(r['expected_new_range'][1])})" if r["expected_new_range"] else "")
        print(f"| {r['condition']} | {r['strict']} | {r['used_in_100']} | {r['read_any_task']} | {r['excluded_on_reading']} | {r['main_exclusions'] or '–'} | "
              f"{r['strict_never_read']} | {r['of_which_patient_in_100']} | {r['distinct_new_patients']} | {y} | {e} |")
    print("\n| Condition | Usable, not strict | Main blocking steps (admissions failing the step) |\n|---|---|---|")
    for r in J["A"]:
        print(f"| {r['condition']} | {r['usable_not_strict']} | {r['main_blocking_steps'] or '–'} |")
    print("\n| Condition | B1 readmission | B2 CC names a test | B3 symptom code first | B4 one step short | B5 age > 89 |\n|---|---|---|---|---|---|")
    keys = ["B1_readmission", "B2_cc_test_label", "B3_symptom_first", "B4_one_step_short", "B5_age_over_89"]
    tot = {k: [0, 0.0] for k in keys}
    for c, b in J["B"].items():
        cells = []
        for k in keys:
            d = b[k]
            cells.append(f"{d['added_strict']} / {fmt(d['expected'])}")
            tot[k][0] += d["added_strict"]
            tot[k][1] += d["expected"] or 0
        print(f"| {c} | " + " | ".join(cells) + " |")
    print("| **Total** | " + " | ".join(f"{v[0]} / {v[1]:.1f}" for v in tot.values()) + " |")
    print("\nB1, admissions whose HPI names an earlier episode with a study (proxy):", {c: b["B1_readmission"]["earlier_workup_in_hpi"] for c, b in J["B"].items() if b["B1_readmission"]["added_strict"]})
    print("B2 by triage label class:", {c: b["B2_cc_test_label"].get("by_label") for c, b in J["B"].items() if b["B2_cc_test_label"].get("by_label")})
    print("B4 missing step:", {c: b["B4_one_step_short"]["missing_step"] for c, b in J["B"].items() if b["B4_one_step_short"]["added_strict"]})
    print("pooled yield 04-07:", J["pooled_yield_0407"])


if __name__ == "__main__":
    main()
