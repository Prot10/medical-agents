"""What does each brain-MRI order receive?  uv run python -I .../mri_probe.py CASE_ID [...]

For each case: the stored MRI slots (where, contrast_used, first 70 chars of the impression), then
the report served to a plain order, a contrast order, plain-then-contrast and contrast-then-plain,
and to the first alternative of every analyze_brain_mri criterion. "case"/"fallback"/"LIBRARY"
says which tier answered. A LIBRARY answer to an order in a case that stores an MRI is a defect.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from neuroagent.harness.environment import NeuroBenchEnvironment
from neuroagent_schemas import NeuroBenchCase
from neuroagent_schemas.actions import ToolAction
CASES = Path(__file__).resolve().parents[4] / "data/neurobench/cases"
GAD = re.compile(r"enhanc|gadolin|post-?contrast|T1\s*\+\s*C|T1[ _-]?post|\bGd\b|contrast[- ]enhanced", re.I)

def tag(r):
    o = r.output if r.output is not None else {}
    o = o if isinstance(o, dict) else o.model_dump()
    tier = "LIBRARY" if r.library else ("fallback" if r.from_fallback else "case")
    return f"{tier:8} contrast_used={o.get('contrast_used')!s:5} gad_text={'Y' if GAD.search(json.dumps({k: v for k, v in o.items() if k != 'recommended_actions'})) else 'n'} | {str(o.get('impression'))[:70]}"

def run(cid):
    raw = json.loads((CASES / f"{cid}.json").read_text())
    case = NeuroBenchCase.model_validate(raw)
    print(f"== {cid}")
    if raw["initial_tool_outputs"].get("mri"):
        m = raw["initial_tool_outputs"]["mri"]; print(f"  slot initial          contrast_used={m.get('contrast_used')} | {str(m.get('impression'))[:70]}")
    for i, f in enumerate(raw["followup_outputs"]):
        if f["tool_name"] == "analyze_brain_mri":
            print(f"  slot followup[{i}] {f['trigger_action']}: contrast_used={f['output'].get('contrast_used')} | {str(f['output'].get('impression'))[:70]}")
    fb = (raw.get("fallback_tool_outputs") or {}).get("mri")
    if fb: print(f"  slot fallback         contrast_used={fb.get('contrast_used')} | {str(fb.get('impression'))[:70]}")
    seqs = {"plain": [{}], "contrast": [{"contrast": True}], "plain>contrast": [{}, {"contrast": True}], "contrast>plain": [{"contrast": True}, {}]}
    for a in raw["ground_truth"]["action_criteria"]:
        al = a["alternatives"][0]
        if al["tool_name"] == "analyze_brain_mri":
            seqs[f"criterion {a['criterion_id']} ({a['importance']}) {al['required_arguments']}"] = [al["required_arguments"]]
    for name, seq in seqs.items():
        env = NeuroBenchEnvironment(case)
        outs = []
        for args in seq:
            r = env.execute(ToolAction(tool_name="analyze_brain_mri", arguments={"clinical_context": "neurological evaluation", **args}))
            outs.append(tag(r) if r.success else f"ERROR {r.error_message}")
        print(f"  {name}:")
        for o in outs: print(f"      {o}")

if __name__ == "__main__":
    for cid in sys.argv[1:]: run(cid)
