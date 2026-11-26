"""Task 05: audit of the diagnosis scoring of the first model run on the MIMIC pilot.
No record content in this file. Reads EVAL (run folders) and OUT (cases, flags); writes tables
under OUT only (they hold model text about record cases).

    python -I mimic_dx_audit5.py --eval $W/out/eval_20261107 --out $W/out table
        -> OUT/05_dx_episodes.csv: one row per episode (arm, seed, case, condition, score, submitted
           primary diagnosis, failure reason, case flags)
    python -I mimic_dx_audit5.py --eval ... --out ... summary --classes OUT/05_dx_classes.csv
        -> counts per condition x arm x class, false-positive rate, sensitivity accuracy
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import pandas as pd

ARMS = ["narrative", "tools", "grpo-best"]
COND = {"focal_epilepsy_temporal": "FEPI", "guillain_barre": "GBS", "ischemic_stroke": "ISCH", "multiple_sclerosis": "MS",
        "status_epilepticus": "SE", "subarachnoid_hemorrhage": "SAH"}


def eeg_seen(ep: dict) -> dict:
    """Which EEG types the agent ordered, and whether it received the case's EEG (not 'Not available')."""
    types, got, unavailable, imp = [], False, 0, ""
    for e in ep.get("events", []):
        if e.get("type") == "action.proposed" and (e.get("action") or {}).get("tool_name") == "analyze_eeg":
            types.append(str((e["action"].get("arguments") or {}).get("eeg_type", "routine(default)")))
        if e.get("type") == "observation.received" and e.get("tool_name") == "analyze_eeg":
            if e.get("success") and not e.get("library"):
                got, imp = True, str((e.get("output") or {}).get("impression", ""))[:300]
            elif e.get("unavailable"):
                unavailable += 1
    seen = sorted({e.get("tool_name") for e in ep.get("events", []) if e.get("type") == "observation.received"
                   and e.get("success") and not e.get("library")})
    return {"eeg_types_ordered": ";".join(types), "eeg_seen": got, "eeg_unavailable": unavailable, "eeg_impression_seen": imp,
            "studies_seen": ";".join(x for x in seen if x)}


def table(a) -> None:
    ev, out = Path(a.eval), Path(a.out)
    flags = pd.read_csv(out / "04_case_flags.csv").set_index("case_id")
    rows = []
    for arm in ARMS:
        for seed in (1, 2, 3):
            d = ev / f"{arm}-s{seed}"
            for line in (d / "rewards.jsonl").read_text().splitlines():
                r = json.loads(line)
                ep = json.loads((d / "episodes" / f"{r['case_id']}.json").read_text()) if (d / "episodes" / f"{r['case_id']}.json").exists() else {}
                ass = next((e["assessment"] for e in ep.get("events", []) if e.get("type") == "assessment.submitted"), {}) or {}
                tools = [e["action"].get("type") or e["action"].get("tool_name") for e in ep.get("events", [])
                         if e.get("type") == "action.proposed" and e.get("action")]
                case = json.loads((ev / "dataset" / "cases" / f"{r['case_id']}.json").read_text())
                dx = case["ground_truth"]["diagnosis"]
                f = flags.loc[r["case_id"]] if r["case_id"] in flags.index else {}
                rows.append({"arm": arm, "seed": seed, "case_id": r["case_id"], "condition": COND.get(r["condition"], r["condition"]),
                             "status": r.get("status"), "failure_reason": r.get("failure_reason"),
                             "dx_score": (r.get("reward") or {}).get("diagnosis"),
                             "primary_diagnosis": r.get("primary_diagnosis") or ass.get("primary_diagnosis"),
                             "differential": json.dumps([x.get("diagnosis") for x in ass.get("differential", []) or []])[:400],
                             "tools": ";".join(r.get("tools_called") or []), "n_actions": len(tools),
                             **eeg_seen(ep),
                             "accepted": " | ".join(dx.get("accepted", [])), "rejected": " | ".join(dx.get("rejected", [])),
                             "required_components": json.dumps(dx.get("required_components", [])),
                             "dx_support": f.get("dx_support", "") if len(f) else "",
                             "known_condition": f.get("known_condition_in_history", "") if len(f) else ""})
    df = pd.DataFrame(rows)
    df.to_csv(out / "05_dx_episodes.csv", index=False)
    print(df.groupby(["condition", "arm"]).dx_score.agg(["size", "mean", lambda s: int((s == 0).sum())]).round(3).to_string())
    print("status:", df.groupby("arm").status.value_counts().to_dict())


def summary(a) -> None:
    out = Path(a.out)
    df = pd.read_csv(out / "05_dx_episodes.csv")
    cl = pd.read_csv(a.classes, dtype={"cls": str})
    z = df[df.dx_score == 0].merge(cl[cl.kind == "zero"][["arm", "seed", "case_id", "cls", "reason", "term"]], on=["arm", "seed", "case_id"], how="left")
    missing = z[z.cls.isna()]
    if len(missing):
        sys.exit(f"{len(missing)} zero episodes without a class")
    pd.set_option("display.width", 200)
    print("== zero-scored episodes per condition x arm x class")
    print(z.pivot_table(index=["condition", "arm"], columns="cls", values="case_id", aggfunc="size", fill_value=0).to_string())
    print("\n== class totals per condition")
    print(z.pivot_table(index="condition", columns="cls", values="case_id", aggfunc="size", fill_value=0).to_string())
    print("\n== class 1 failure reasons:", z[z.cls == "1"].reason.value_counts().to_dict())
    print("\n== class 3 terms (episodes changed):", z[z.cls == "3"].term.value_counts().to_dict())
    print("== class 4 reasons:", z[z.cls == "4"].reason.value_counts().to_dict())
    c4 = z[z.cls == "4"]
    print("== class 4 episodes on clinical_only cases:", int((c4.dx_support == "clinical_only").sum()), "of", len(c4),
          "| per condition", c4[c4.dx_support == "clinical_only"].condition.value_counts().to_dict())
    print("== class 5 reasons:", z[z.cls == "5"].reason.value_counts().to_dict())
    # false positives in the 20 % sample of score-1 episodes
    fp = cl[cl.kind == "one"]
    print(f"\n== score-1 sample: {len(fp)} episodes read; false positives {int((fp.cls == 'FP').sum())}"
          f" ({(fp.cls == 'FP').mean():.1%}); per condition", fp.groupby(fp.case_id.str.split('-').str[1]).cls.apply(lambda s: f"{(s == 'FP').sum()}/{len(s)}").to_dict())
    # sensitivity: class 3 counted as correct
    df = df.merge(z[["arm", "seed", "case_id", "cls"]], on=["arm", "seed", "case_id"], how="left")
    df["dx_sens"] = df.dx_score.where(df.cls != "3", 1.0)
    df["dx_sens4"] = df.dx_sens.where(df.cls != "4", 1.0)
    agg = lambda col: df.groupby(["condition", "arm", "case_id"])[col].mean().groupby(["condition", "arm"]).mean().unstack().round(2)
    scr = Path(a.out) / "05_dx_one_fp_screen.csv"
    if scr.exists():
        sf = pd.read_csv(scr)
        ones = df[df.dx_score == 1]
        sf = sf.merge(df[["arm", "seed", "case_id", "condition"]], on=["arm", "seed", "case_id"])
        print(f"== hedge screen of all {len(ones)} score-1 episodes: false positives {len(sf)} ({len(sf) / len(ones):.1%}); "
              "by reason", sf.reason.value_counts().to_dict())
        print("   per condition x arm:", sf.groupby(["condition", "arm"]).size().to_dict())
        key = set(zip(sf.arm, sf.seed, sf.case_id))
        df["dx_nofp"] = [0.0 if (r.arm, r.seed, r.case_id) in key else r.dx_score for r in df.itertuples()]
    print("\n== diagnosis accuracy (case mean over seeds, then over cases): scored"); print(agg("dx_score").to_string())
    if "dx_nofp" in df:
        print("\n== with the screened false positives counted wrong (sensitivity only)"); print(agg("dx_nofp").to_string())
        df["dx_both"] = df.dx_sens.where(~df.index.isin(df[df.dx_nofp != df.dx_score].index), 0.0)
        print("\n== class 3 counted correct and false positives counted wrong (sensitivity only)"); print(agg("dx_both").to_string())
    print("\n== with class 3 counted correct (sensitivity only)"); print(agg("dx_sens").to_string())
    print("\n== with classes 3 and 4 counted correct (upper bound, sensitivity only)"); print(agg("dx_sens4").to_string())


def sample(a) -> None:
    """The 20 % random sample of score-1 episodes to read (seed 5), per condition and arm."""
    out = Path(a.out)
    df = pd.read_csv(out / "05_dx_episodes.csv")
    ones = df[df.dx_score == 1]
    rng = random.Random(5)
    pick = []
    for _, g in ones.groupby(["condition", "arm"]):
        idx = list(g.index)
        pick += rng.sample(idx, max(1, round(0.2 * len(idx))))
    s = df.loc[sorted(pick)]
    s.to_csv(out / "05_dx_one_sample.csv", index=False)
    print(len(s), "of", len(ones), "score-1 episodes sampled")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("stage", choices=["table", "sample", "summary"])
    ap.add_argument("--classes")
    a = ap.parse_args()
    if not str(Path(a.out).resolve()).startswith(("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")):
        sys.exit("--out must be under the PhysioNet workspace")
    {"table": table, "sample": sample, "summary": summary}[a.stage](a)


if __name__ == "__main__":
    main()
