"""Collect every number the figures show into data/figures.json.

Run from the repository root with the project environment (the example rewards need the harness):
    uv run python paper/figures/data/prepare.py
Sources: case files and split manifest, git history of the cases, the leakage audit outputs
(`scripts/paper/leakage_audit.py`), and ClinicalPolicyReward on three constructed trajectories.
"""

from __future__ import annotations

import collections
import csv
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CASES = ROOT / "data/neurobench/cases"
SPLIT = json.loads((ROOT / "data/neurobench/splits/split_manifest.json").read_text())
LEAK = ROOT / "outputs/paper/leakage"
OUT = Path(__file__).resolve().parent / "figures.json"

GROUPS = {
    "Cerebrovascular": ["ischemic_stroke", "subarachnoid_hemorrhage"],
    "Infection and inflammation": ["bacterial_meningitis", "autoimmune_encephalitis_nmdar", "multiple_sclerosis"],
    "Neurodegeneration": ["alzheimers_early", "ftd", "vascular_dementia", "nph", "parkinsons", "als"],
    "Seizures": ["focal_epilepsy_temporal", "status_epilepticus"],
    "Neuromuscular": ["guillain_barre", "myasthenia_gravis"],
    "Oncology": ["brain_tumor_glioma"],
    "Headache": ["migraine_with_aura"],
    "Functional": ["functional_neurological_disorder"],
    "Systemic mimics": ["syncope_cardiac", "hepatic_encephalopathy"],
}
NAMES = {
    "als": "ALS", "alzheimers_early": "Early Alzheimer's disease", "autoimmune_encephalitis_nmdar": "Anti-NMDAR encephalitis",
    "bacterial_meningitis": "Bacterial meningitis", "brain_tumor_glioma": "High-grade glioma",
    "focal_epilepsy_temporal": "Temporal lobe epilepsy", "ftd": "Frontotemporal dementia",
    "functional_neurological_disorder": "Functional neurological disorder", "guillain_barre": "Guillain–Barré syndrome",
    "hepatic_encephalopathy": "Hepatic encephalopathy", "ischemic_stroke": "Ischaemic stroke",
    "migraine_with_aura": "Migraine with aura", "multiple_sclerosis": "Multiple sclerosis",
    "myasthenia_gravis": "Myasthenia gravis", "nph": "Normal-pressure hydrocephalus", "parkinsons": "Parkinson's disease",
    "status_epilepticus": "Status epilepticus", "subarachnoid_hemorrhage": "Subarachnoid haemorrhage",
    "syncope_cardiac": "Cardiac syncope", "vascular_dementia": "Vascular dementia",
}


def dataset():
    strat, held = set(SPLIT["test_stratified_case_ids"]), set(SPLIT["heldout_conditions"])
    by = collections.defaultdict(lambda: {"train": 0, "test_same": 0, "test_held": 0, "difficulty": collections.Counter()})
    diff, enc = collections.Counter(), collections.Counter()
    for f in sorted(CASES.glob("*.json")):
        c = json.loads(f.read_text())
        row = by[c["condition"]]
        key = "test_held" if c["condition"] in held else "test_same" if c["case_id"] in strat else "train"
        row[key] += 1
        row["difficulty"][c["difficulty"]] += 1
        diff[c["difficulty"]] += 1
        enc[c["encounter_type"]] += 1
    groups = [
        {"group": g, "conditions": [{"id": c, "name": NAMES[c], "held_out": c in held,
                                       **{k: v for k, v in by[c].items() if k != "difficulty"},
                                       "difficulty": dict(by[c]["difficulty"])} for c in cs]}
        for g, cs in GROUPS.items()
    ]
    assert sum(len(g["conditions"]) for g in groups) == 20
    return {"groups": groups, "difficulty": dict(diff), "encounter": dict(enc),
            "n_train": len(SPLIT["train_case_ids"]), "n_test_same": len(strat),
            "n_test_held": len(SPLIT["test_heldout_condition_case_ids"])}


def revisions():
    log = subprocess.run(["git", "log", "--name-only", "--format=@@%s", "--", "data/neurobench/cases"],
                         capture_output=True, text=True, cwd=ROOT, check=True).stdout
    commits = []
    for line in log.splitlines():
        if line.startswith("@@"):
            commits.append({"s": line[2:], "n": 0})
        elif line.endswith(".json"):
            commits[-1]["n"] += 1
    return {
        "commits": len(commits),
        "wide": sum(c["n"] >= 100 for c in commits),
        "rounds": sum(bool(re.search(r"close the \S+ review round", c["s"])) for c in commits),
    }


def policy_stats():
    keys = collections.defaultdict(int)
    n = 0
    for f in CASES.glob("*.json"):
        g = json.loads(f.read_text())["ground_truth"]
        c = json.loads(f.read_text())
        n += 1
        keys["required"] += sum(a["importance"] == "required" for a in g["action_criteria"])
        keys["recommended"] += sum(a["importance"] == "recommended" for a in g["action_criteria"])
        for a in g["avoided_actions"]:
            keys[a["severity"]] += 1
        keys["sequence"] += len(g["sequence_constraints"] or [])
        keys["hard"] += sum(s.get("severity") == "hard" for s in g["sequence_constraints"] or [])
        keys["accepted"] += len(g["diagnosis"]["accepted"])
        keys["rejected"] += len(g["diagnosis"].get("rejected") or [])
        keys["red_herrings"] += len(g.get("red_herrings") or [])
        keys["initial"] += sum(bool(v) for v in c["initial_tool_outputs"].values())
        keys["followup"] += len(c["followup_outputs"])
    return {"cases": n, "totals": dict(keys), "per_case": {k: round(v / n, 2) for k, v in keys.items()}}


def timeline():
    """Commits touching case files, per ISO week, split by whether physicians' review drove them."""
    import datetime as dt
    log = subprocess.run(["git", "log", "--name-only", "--format=@@%ad|%s", "--date=short", "--", "data/neurobench/cases"],
                         capture_output=True, text=True, cwd=ROOT, check=True).stdout
    weeks = collections.defaultdict(lambda: {"review": 0, "other": 0, "files": 0})
    rounds = []
    for line in log.splitlines():
        if line.startswith("@@"):
            d, s = line[2:].split("|", 1)
            day = dt.date.fromisoformat(d)
            wk = (day - dt.timedelta(days=day.weekday())).isoformat()
            kind = "review" if re.search(r"review|physician|clinician|pathway", s, re.I) else "other"
            weeks[wk][kind] += 1
            if re.search(r"close the \S+ review round", s):
                rounds.append(d)
        elif line.endswith(".json"):
            weeks[wk]["files"] += 1
    start = dt.date(2026, 7, 6)
    out, w = [], start
    while w <= dt.date(2026, 10, 26):
        out.append({"week": w.isoformat(), **weeks.get(w.isoformat(), {"review": 0, "other": 0, "files": 0})})
        w += dt.timedelta(days=7)
    return {"weeks": out, "rounds": rounds}


def leakage():
    if not (LEAK / "nn_similarity.csv").exists():
        return None
    summary = json.loads((LEAK / "summary.json").read_text())["similarity"]
    rows = list(csv.DictReader((LEAK / "nn_similarity.csv").open()))
    keep = {"null_train_loo_same_condition": "null", "test_stratified_vs_train_same_condition": "same",
            "test_heldout_vs_all_train": "held"}
    out = {}
    for field in ("narrative", "tool_outputs", "policy"):
        out[field] = {
            "values": {short: [round(float(r["tfidf_cosine"]), 4) for r in rows if r["field"] == field and r["group"] == g]
                       for g, short in keep.items()},
            "median": {short: summary[field][g]["tfidf_cosine"]["median"] for g, short in keep.items()},
            "auc": summary[field]["test_vs_null_tfidf_cosine"]["auc_test_gt_null"],
            "p": summary[field]["test_vs_null_tfidf_cosine"]["p_one_sided"],
        }
    return out


def example():
    """Three constructed trajectories on BACT-MEN-RS02, scored by the benchmark reward."""
    from neuroagent.evaluation import ClinicalPolicyReward
    from neuroagent.harness.environment import NeuroBenchEnvironment
    from neuroagent_schemas import (ActionProposed, AssessmentSubmitted, ClinicalEpisode, NeuroBenchCase,
                                    ObservationReceived, RunCompleted, SubmitAssessment, ToolAction)

    case = NeuroBenchCase.model_validate_json((CASES / "BACT-MEN-RS02.json").read_text())
    crit = {c.criterion_id: c for c in case.ground_truth.action_criteria}
    short = {"action-2-order-microbiology": "Blood cultures", "action-1-interpret-labs": "Labs",
             "action-5-order-ct-scan": "CT head", "action-3-analyze-csf": "Lumbar puncture",
             "action-4-analyze-brain-mri": "MRI"}

    def run(cids):
        env, events, total, steps = NeuroBenchEnvironment(case), [], 0.0, []
        for t, cid in enumerate(cids, 1):
            p = crit[cid].alternatives[0]
            args = dict(p.required_arguments)
            for n in env.registry.get_tool(p.tool_name).parameter_schema.get("required", []):
                args.setdefault(n, "index order")
            a = ToolAction(tool_name=p.tool_name, arguments=args)
            r = env.execute(a)
            total += r.cost_usd or 0
            steps.append({"label": short[cid], "tool": p.tool_name, "cost": r.cost_usd})
            events += [ActionProposed(turn=t, action=a),
                       ObservationReceived(turn=t, tool_name=a.tool_name, success=r.success, output=r.output or {},
                                           cost_usd=r.cost_usd or 0)]
        s = SubmitAssessment(primary_diagnosis="Acute bacterial meningitis (pneumococcal)", confidence=0.9,
                             urgency="emergent", recommendations=case.ground_truth.assessment.required_recommendations)
        t = len(cids) + 1
        events += [ActionProposed(turn=t, action=s), AssessmentSubmitted(turn=t, assessment=s), RunCompleted(turn=t)]
        b = ClinicalPolicyReward(require_approved=False).score(ClinicalEpisode(events=events), case)
        return {"steps": steps, "cost": total, "reward": b.scalar, "diagnosis": b.diagnosis,
                "required": b.required_action_coverage, "sequence": b.sequence, "caps": b.caps_applied}

    return {
        "case_id": case.case_id,
        "A": run(["action-2-order-microbiology", "action-1-interpret-labs", "action-5-order-ct-scan",
                  "action-3-analyze-csf", "action-4-analyze-brain-mri"]),
        "B": run(["action-2-order-microbiology", "action-1-interpret-labs", "action-3-analyze-csf",
                  "action-5-order-ct-scan", "action-4-analyze-brain-mri"]),
        "C": run(["action-1-interpret-labs", "action-3-analyze-csf"]),
    }


if __name__ == "__main__":
    data = {"dataset": dataset(), "revisions": revisions(), "policy": policy_stats(), "timeline": timeline(),
            "leakage": leakage(), "example": example()}
    OUT.write_text(json.dumps(data, indent=1))
    print(OUT, {k: data["example"][k]["reward"] for k in "ABC"}, data["revisions"])
