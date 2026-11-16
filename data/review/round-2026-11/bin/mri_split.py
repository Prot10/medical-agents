"""Structural half of the MRI-CONTRAST class (plans/MRI-CONTRAST-decisions.md).

    uv run python -I .../mri_split.py CASE_ID initial            # split initial_tool_outputs.mri
    uv run python -I .../mri_split.py CASE_ID followup INDEX     # split followup_outputs[INDEX]

The stored gadolinium study gets contrast_used=true and is stored as an analyze_brain_mri
follow-up (trigger `request_contrast_mri`, or `<old trigger>_with_contrast` for a follow-up);
a deep copy with contrast_used=false takes the original slot. The copy still contains the
gadolinium text: the script prints every field of it that mentions enhancement/gadolinium, and
YOU must then edit the plain copy (through case_io) so it reports only the non-contrast
sequences. Saves through case_io (schema-validated).
"""
from __future__ import annotations
import copy, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from case_io import load, save
GAD = re.compile(r"enhanc|gadolin|post-?contrast|T1\s*\+\s*C|T1[ _-]?post|\bGd\b|contrast[- ]enhanced", re.I)

def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if GAD.search(k): yield p + "." + k, v
            yield from walk(v, p + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, f"{p}[{i}]")
    elif isinstance(o, str) and GAD.search(o):
        yield p, o

def main():
    cid, where = sys.argv[1], sys.argv[2]
    case = load(cid)
    if where == "initial":
        study = case["initial_tool_outputs"]["mri"]
        assert study and study.get("contrast_used") is None, "already split or flagged: nothing to split"
        gad = copy.deepcopy(study); gad["contrast_used"] = True
        plain = copy.deepcopy(study); plain["contrast_used"] = False
        case["initial_tool_outputs"]["mri"] = plain
        # the contrast study goes before any other MRI follow-up, else first in the pathway; move it if the clinical order differs
        fus = case["followup_outputs"]; pos = next((i for i, f in enumerate(fus) if f["tool_name"] == "analyze_brain_mri"), 0)
        fus.insert(pos, {"tool_name": "analyze_brain_mri", "trigger_action": "request_contrast_mri", "output": gad})
        loc = "initial_tool_outputs.mri"
    else:
        i = int(sys.argv[3]); f = case["followup_outputs"][i]
        assert f["tool_name"] == "analyze_brain_mri" and f["output"].get("contrast_used") is None, "already split or flagged"
        gad = copy.deepcopy(f); gad["output"]["contrast_used"] = True; gad["trigger_action"] = f["trigger_action"] + "_with_contrast"
        f["output"]["contrast_used"] = False
        case["followup_outputs"].insert(i + 1, gad)
        loc = f"followup_outputs[{i}].output"
    save(case)
    print(f"{cid}: split done. Plain copy at {loc} still has gadolinium content to remove:")
    target = case["initial_tool_outputs"]["mri"] if where == "initial" else case["followup_outputs"][int(sys.argv[3])]["output"]
    for p, v in walk(target): print(f"  {p}: {json.dumps(v)[:300]}")

if __name__ == "__main__":
    main()
