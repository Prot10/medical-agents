"""Blinded files for the leakage review: per case, the presentation exactly as the harness renders
it and every tool output, under a shuffled letter code, with no case id, condition, diagnosis or
policy. The letter <-> case map is written next to the files. Output only under the PhysioNet
workspace (the files hold record content). No record content here.

    ~/projects/medical-agents/.venv/bin/python -I mimic_blind_files.py --cases $W/out/03_cases --to $W/tmp/blind3 --seed 7 --per-file 9
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for p in (ROOT / "agent-platform/src", ROOT / "packages/neuroagent-schemas/src"):
    sys.path.insert(0, str(p))


def main() -> None:
    from neuroagent.harness.context import format_patient_info
    from neuroagent_schemas import NeuroBenchCase
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--to", required=True)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--only", nargs="*", default=[])
    a = ap.parse_args()
    to = Path(a.to)
    if not str(to.resolve()).startswith(("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")):
        sys.exit("--to must be under the PhysioNet workspace")
    to.mkdir(parents=True, exist_ok=True)
    ids = sorted(p.stem for p in Path(a.cases).glob("*.json") if not a.only or p.stem in a.only)
    random.Random(a.seed).shuffle(ids)
    mapping = {}
    for i, cid in enumerate(ids):
        code = f"K{i:02d}"
        raw = json.loads((Path(a.cases) / f"{cid}.json").read_text())
        case = NeuroBenchCase.model_validate(raw)
        txt = [f"# Case {code}", "", "## Presentation (what the agent sees first)", "",
               format_patient_info(case).replace(cid, f"case-{code}"), "", "## Tool outputs (each returned only when ordered)", ""]
        for k, v in raw["initial_tool_outputs"].items():
            if v:
                txt += [f"### {k}", json.dumps(v, indent=1, ensure_ascii=False), ""]
        for f in raw["followup_outputs"]:
            txt += [f"### {f['tool_name']} ({f['trigger_action']})", json.dumps(f["output"], indent=1, ensure_ascii=False), ""]
        (to / f"case_{code}.md").write_text("\n".join(txt))
        mapping[code] = cid
    (to.parent / f"{to.name}_map.json").write_text(json.dumps(mapping, indent=1))
    print(f"{len(mapping)} blinded files written")


if __name__ == "__main__":
    main()
