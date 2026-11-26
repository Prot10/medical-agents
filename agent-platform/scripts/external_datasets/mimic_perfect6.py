"""Task 06: re-run the repository perfect-agent check on the final case files (after the label steps),
with the current MockServer. Counts only. No record content in this file.

    ~/projects/medical-agents/.venv/bin/python -I mimic_perfect6.py --out $W/out
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mimic_case_build3 as B  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
a = ap.parse_args()
out = Path(a.out)
sel = pd.read_csv(out / "06_selection.csv")
sel = sel[sel.case_id.notna() & sel.exclusion.isna()]
res = {}
for c in sel.case_id:
    if not (out / "06_cases" / f"{c}.json").exists():
        print(f"{c}: not built yet", file=sys.stderr)
        continue
    e, w, acc = B.perfect_agent3(out / "06_cases", c)
    res[c] = {"errors": e, "warnings": w, "knowledge_library_accepted": acc}
(out / "06_perfect_agent.json").write_text(json.dumps(res, indent=1))
print(f"cases {len(res)}; failures {sum(bool(v['errors']) for v in res.values())}; warnings {sum(len(v['warnings']) for v in res.values())}; "
      f"knowledge-library answers accepted {sum(len(v['knowledge_library_accepted']) for v in res.values())}")
for c, v in res.items():
    if v["errors"]:
        print(" ", c, v["errors"][:2])
