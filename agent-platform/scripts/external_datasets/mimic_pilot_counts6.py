"""Counts for the task-06 report and the method document; writes the machine-readable flow.
Aggregates only (no ids). Reads OUT.

    python -I mimic_pilot_counts6.py --out $W/out --report $W/report [--blind r1.json r2.json ...] [--reread reread.json]
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

import pandas as pd

TOOL_OF = {"eeg": "analyze_eeg", "mri": "analyze_brain_mri", "ecg": "analyze_ecg", "labs": "interpret_labs", "csf": "analyze_csf",
           "ct": "order_ct_scan", "echo": "order_echocardiogram", "cardiac_monitoring": "order_cardiac_monitoring",
           "advanced_imaging": "order_advanced_imaging", "specialized_test": "order_specialized_test", "body_imaging": "order_body_imaging",
           "microbiology": "order_microbiology", "tissue_diagnosis": "obtain_tissue_diagnosis", "clinical_assessment": "perform_clinical_assessment"}
PATIENT_FIELDS = ["chief_complaint", "history_present_illness", "vitals", "neurological_exam", "physical_exam",
                  "clinical_history.past_medical_history", "clinical_history.medications", "clinical_history.allergies",
                  "clinical_history.family_history", "clinical_history.social_history", "demographics.handedness",
                  "demographics.height_cm", "demographics.weight_kg"]


def get(d, path):
    for k in path.split("."):
        d = (d or {}).get(k) if isinstance(d, dict) else None
    return d


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--blind", nargs="*", default=[])
    ap.add_argument("--reread", default="")
    ap.add_argument("--flow-name", default="06_flow.json")
    ap.add_argument("--rounds", nargs="*", default=[], help="task 07: re-read round summaries (07_rN_reread_summary.json), in order")
    a = ap.parse_args()
    out, rep = Path(a.out), Path(a.report)
    pd.set_option("display.width", 250)
    sel = pd.read_csv(out / "06_selection.csv")
    live = sel[sel.case_id.notna() & (sel.case_id != "") & (sel.exclusion.isna() | (sel.exclusion == ""))]
    flow = {"strict": pd.read_csv(out / "06_strict.csv").to_dict("records"),
            "waterfall": pd.read_csv(out / "03_waterfall.csv").to_dict("records")}
    ex = sel[sel.exclusion.notna() & (sel.exclusion != "") & (sel.exclusion != "not drawn") & sel.case_id.notna() & (sel.case_id != "")]
    ex = ex.assign(cls=ex.exclusion.str.replace(r"\s*\(.*$", "", regex=True).str.replace(r":.*$", "", regex=True).str.strip())
    print("== selection per condition:", live.groupby("condition").size().to_dict(), "| total", len(live))
    print("== exclusions after reading (drawn cases), by condition and class")
    print(ex.groupby(["condition", "cls"]).size().to_string())
    flow["selected"] = live.groupby("condition").size().to_dict()
    flow["excluded_on_reading"] = {f"{c}|{k}": int(v) for (c, k), v in ex.groupby(["condition", "cls"]).size().items()}
    # CONSORT-style flow per condition (decision 3/10 strict pool, reading, selection)
    wf = pd.read_csv(out / "03_waterfall.csv").set_index("condition")
    st = pd.read_csv(out / "06_strict.csv").set_index("condition")
    cons = []
    for cond in st.index:
        g = sel[sel.condition == cond]
        drawn = g[g.case_id.notna() & (g.case_id != "")]
        exc = drawn[drawn.exclusion.notna() & (drawn.exclusion != "") & (drawn.exclusion != "not drawn")]
        top = exc.exclusion.str.replace(r"\s*\(.*$", "", regex=True).str.replace(r":.*$", "", regex=True).value_counts()
        cons.append({"condition": cond, "principal_dx": int(wf.loc[cond, "principal"]), "new_ed_note_not_transfer": int(wf.loc[cond, "new_not_transfer_ed_note"]),
                     "hidden_transfer_dropped": int(wf.loc[cond, "hidden_transfer_dropped"]),
                     "cc_dropped": int(wf.loc[cond, "cc_dropped_transfer"] + wf.loc[cond, "cc_dropped_test_label"]),
                     "usable": int(st.loc[cond, "usable"]), "core_steps_servable": int(st.loc[cond, "strict_before_support"]),
                     "strict_record_support": int(st.loc[cond, "strict"]), "ed_servable": bool(st.loc[cond, "ed_servable"]),
                     "read": int(len(drawn)), "excluded_on_reading": int(len(exc)),
                     "main_reading_exclusion": (f"{top.index[0]} ({int(top.iloc[0])})" if len(top) else ""),
                     "selected": int(((drawn.exclusion.isna()) | (drawn.exclusion == "")).sum())})
    cons = pd.DataFrame(cons)
    print("== CONSORT flow per condition"); print(cons.to_string(index=False))
    flow["consort"] = cons.to_dict("records")
    rows, empty = [], collections.Counter()
    for r in live.itertuples():
        f = out / "06_cases" / f"{r.case_id}.json"
        if not f.exists():
            continue
        c = json.loads(f.read_text())
        io = c["initial_tool_outputs"]
        tools_init = {TOOL_OF[k] for k, v in io.items() if v and k in TOOL_OF}
        tools_fu = {x["tool_name"] for x in c["followup_outputs"]}
        tools = tools_init | tools_fu
        crit = c["ground_truth"]["action_criteria"]
        req = {x["alternatives"][0]["tool_name"] for x in crit if x["importance"] == "required" and not x["alternatives"][0]["tool_name"].startswith(("check_", "search_"))}
        rec = {x["alternatives"][0]["tool_name"] for x in crit if x["importance"] == "recommended" and not x["alternatives"][0]["tool_name"].startswith(("check_", "search_"))}
        bc = c["metadata"]["build_counts"]
        rows.append({"condition": r.condition, "tools_served": len(tools), "results_served": len([1 for v in io.values() if v]) + len(c["followup_outputs"]),
                     "followups": len(c["followup_outputs"]), "required_with_result": len(req & tools), "required": len(req),
                     "recommended_with_result": len(rec & tools), "recommended": len(rec), "other_tools_with_result": len(tools - req - rec),
                     "eeg_followups": bc.get("c6_eeg_followups", 0), "ecg_followups": bc.get("c6_ecg_followups", 0),
                     "imaging_extra": sum(v for k, v in bc.items() if k.startswith("c6_imaging_") and k != "c6_imaging_not_mapped"),
                     "serial_lab_values": bc.get("c6_serial_lab_values", 0), "micro_specimens": bc.get("c6_micro_specimens", 0),
                     "grid_rows_served": bc.get("c6_grid_rows_served", 0), "grid_cells_dropped": bc.get("c6_grid_cells_dropped", 0),
                     "grids_dropped_unaligned": bc.get("c6_grid_dropped_unaligned", 0) + bc.get("c6_grid_dropped_no_header", 0),
                     "eeg_source": c["metadata"].get("eeg_source", ""), "known": int(bool(c["metadata"].get("known_condition_in_history"))),
                     "clinical_only": int(c["metadata"].get("dx_support") == "clinical_only"),
                     "accepted": len(c["ground_truth"]["diagnosis"]["accepted"]), "rejected": len(c["ground_truth"]["diagnosis"].get("rejected", []))})
        for fld in PATIENT_FIELDS:
            v = get(c["patient"], fld)
            if v in (None, "", [], {}) or (isinstance(v, dict) and not any(v.values())):
                empty[(r.condition, fld)] += 1
    df = pd.DataFrame(rows)
    g = df.groupby("condition")
    comp = g.agg(cases=("tools_served", "size"), tools_mean=("tools_served", "mean"), tools_min=("tools_served", "min"), tools_max=("tools_served", "max"),
                 results_mean=("results_served", "mean"), followups=("followups", "sum"), required=("required", "sum"),
                 required_with_result=("required_with_result", "sum"), recommended=("recommended", "sum"),
                 recommended_with_result=("recommended_with_result", "sum"), other_tools=("other_tools_with_result", "sum"),
                 eeg_followups=("eeg_followups", "sum"), ecg_followups=("ecg_followups", "sum"), imaging_extra=("imaging_extra", "sum"),
                 serial_lab_values=("serial_lab_values", "sum"), micro=("micro_specimens", "sum"), grid_rows=("grid_rows_served", "sum"),
                 grid_cells_dropped=("grid_cells_dropped", "sum"), grids_dropped=("grids_dropped_unaligned", "sum"),
                 known=("known", "sum"), clinical_only=("clinical_only", "sum"), no_rejected=("rejected", lambda s: int((s == 0).sum()))).round(1)
    print("\n== completeness per condition"); print(comp.T.to_string())
    print("\n== eeg_source:", df[df.eeg_source != ""].groupby(["condition", "eeg_source"]).size().to_dict())
    e = pd.Series(empty).rename_axis(["condition", "field"]).reset_index(name="n")
    print("\n== patient fields left empty (cases)"); print(e.pivot_table(index="field", columns="condition", values="n", fill_value=0).to_string())
    flow["completeness"] = comp.reset_index().to_dict("records")
    flow["empty_fields"] = {f"{c}|{k}": int(v) for (c, k), v in empty.items()}
    # policies (transferred criteria per condition), knowledge-tool criteria, safety drafts, labels, build counters
    pol, bc_sum = {}, collections.Counter()
    for r in live.itertuples():
        c = json.loads((out / "06_cases" / f"{r.case_id}.json").read_text())
        p = pol.setdefault(r.condition, {"criteria": collections.Counter(), "template_pattern_cases": {}, "panels_dropped": collections.Counter(),
                                         "avoided_drafts": 0, "assessment_drafts": 0, "accepted": [], "rejected": [], "transferred_from": ""})
        meta = c["metadata"].get("policy", {})
        p["transferred_from"] = meta.get("transferred_from", "")
        for cr in c["ground_truth"]["action_criteria"]:
            a0 = cr["alternatives"][0]
            key = f"{cr['importance']}:{a0['tool_name']}:{json.dumps(a0.get('required_arguments', {}), sort_keys=True)}"
            p["criteria"][key] += 1
        for k, v in meta.get("criteria", {}).items():
            p["template_pattern_cases"][v.get("step", k)] = v.get("template_pattern_cases")
        for x in meta.get("lab_panels_dropped_rule_3", []) or []:
            p["panels_dropped"][x] += 1
        gt = c["ground_truth"]
        p["avoided_drafts"] += len(gt.get("avoided_actions", []) or [])
        p["assessment_drafts"] += len((gt.get("assessment") or {}).get("recommendations", []) or []) if isinstance(gt.get("assessment"), dict) else 0
        p["accepted"].append(len(gt["diagnosis"]["accepted"]))
        p["rejected"].append(len(gt["diagnosis"].get("rejected", [])))
        bc_sum.update({k: v for k, v in c["metadata"]["build_counts"].items() if isinstance(v, (int, float))})
    print("\n== policies per condition")
    for cond, p in pol.items():
        print(cond, "| from:", p["transferred_from"], "| criteria (cases):", dict(p["criteria"]), "| template pattern cases:", p["template_pattern_cases"],
              "| panels dropped (d3):", dict(p["panels_dropped"]), "| avoided-action drafts:", p["avoided_drafts"],
              "| accepted labels mean:", round(sum(p["accepted"]) / len(p["accepted"]), 1), "| rejected labels mean:", round(sum(p["rejected"]) / len(p["rejected"]), 1))
    flow["policies"] = {c: {**p, "criteria": dict(p["criteria"]), "panels_dropped": dict(p["panels_dropped"])} for c, p in pol.items()}
    flow["build_counts_sum"] = dict(bc_sum)
    print("\n== build counters (sum over the 100):", {k: v for k, v in sorted(bc_sum.items()) if v})
    ch = json.loads((out / "06_build_checks.json").read_text())
    ch = {k: v for k, v in ch.items() if k in set(live.case_id)}
    flow["checks"] = {"cases": len(ch), "schema_ok": sum(v["schema"] == "ok" for v in ch.values()),
                      "build_errors": sum(len(v["build_errors"]) for v in ch.values()),
                      "perfect_agent_failures": sum(bool(v["perfect_agent_errors"]) for v in ch.values()),
                      "perfect_agent_warnings": sum(len(v["perfect_agent_warnings"]) for v in ch.values()),
                      "knowledge_library_accepted": sum(len(v["perfect_agent_knowledge_library_accepted"]) for v in ch.values())}
    tf = out / "06_timing_checks.json"
    if tf.exists():
        t = {k: v for k, v in json.loads(tf.read_text()).items() if k in set(live.case_id)}
        flow["checks"]["timing_cases"], flow["checks"]["timing_errors"] = len(t), sum(len(v["errors"]) for v in t.values())
    print("\n== checks:", flow["checks"])
    rounds = []
    for b in a.blind:
        r = json.loads(Path(b).read_text())
        pres = collections.Counter(i.get("severity") for x in r.values() for i in x.get("presentation_leaks", []))
        tool = collections.Counter(i.get("severity") for x in r.values() for i in x.get("tool_output_issues", []))
        cls = collections.Counter(i.get("class") for x in r.values() for i in x.get("tool_output_issues", []) + x.get("presentation_leaks", [])
                                  if i.get("severity") == "leak")
        rounds.append({"file": Path(b).parent.name, "cases": len(r), "presentation_leaks": pres.get("leak", 0), "presentation_borderline": pres.get("borderline", 0),
                       "tool_leaks": tool.get("leak", 0), "tool_borderline": tool.get("borderline", 0), "leak_classes": dict(cls),
                       "cases_with_leak": sum(1 for x in r.values() if any(i.get("severity") == "leak" for i in x.get("presentation_leaks", []) + x.get("tool_output_issues", [])))})
    if rounds:
        print("\n== blind rounds"); print(pd.DataFrame(rounds).to_string(index=False))
        flow["leakage_rounds"] = rounds
    if a.reread and Path(a.reread).exists():
        flow["reread"] = json.loads(Path(a.reread).read_text())
        print("\n== re-read:", flow["reread"].get("summary"))
    if a.rounds:
        flow["reread_rounds"] = []
        for f in a.rounds:
            r = json.loads(Path(f).read_text())["round1"]
            flow["reread_rounds"].append({"round": Path(f).name.split("_")[1], **r["TOTAL"], "per_condition": {k: v for k, v in r.items() if k != "TOTAL"}})
            t = r["TOTAL"]
            print(f"== re-read {Path(f).name}: cases {t['cases']} fields {t['fields_checked']} errors {t['errors']} (cases {t['cases_with_error']}) minor {t['minor']}")
    # task 07 aggregates (decisions 42-48)
    t7 = {"sah_aneurysm_status": collections.Counter(), "csf_not_served": collections.Counter(), "rejected_labels_rule": collections.Counter(),
          "primary_code": collections.Counter(), "policy_study_hours": {}, "late_policy_studies_after_adm48": collections.Counter(),
          "vitals_source": collections.Counter()}
    for r in live.itertuples():
        c = json.loads((out / "06_cases" / f"{r.case_id}.json").read_text())
        m = c["metadata"]
        if r.condition == "SAH":
            t7["sah_aneurysm_status"][m.get("sah_aneurysm_status", "")] += 1
            t7["primary_code"][c["ground_truth"]["diagnosis"]["icd_codes"][0]] += 1
        if m.get("csf_not_served"):
            t7["csf_not_served"][f"{r.condition}|{(m['csf_not_served'] or {}).get('source', 'drain') if isinstance(m['csf_not_served'], dict) else 'yes'}"] += 1
        t7["rejected_labels_rule"][f"{r.condition}|{m.get('rejected_labels_rule', '')}"] += 1
        t7["vitals_source"][m.get("presentation_sources", {}).get("vitals", "")] += 1
        adm = (m.get("timing_hours_from_ed_arrival") or {}).get("admission")
        dp = adm + 48 if adm is not None else None
        for k, v in (m.get("policy_study_hours") or {}).items():
            h = v.get("t_h_from_ed_arrival")
            if h is None:
                continue
            t7["policy_study_hours"].setdefault(f"{r.condition}|{v.get('tool')}", []).append(h)
            t7.setdefault("_all", []).append(h)
            if dp is not None and h > dp:
                t7["late_policy_studies_after_adm48"][f"{r.condition}|{v.get('tool')}"] += 1
    q = lambda xs: {"n": len(xs), "median": round(float(pd.Series(xs).median()), 1), "p90": round(float(pd.Series(xs).quantile(0.9)), 1),
                    "max": round(max(xs), 1), "over_48h": sum(x > 48 for x in xs)}
    t7["policy_study_hours"] = {k: q(v) for k, v in sorted(t7["policy_study_hours"].items())}
    t7["policy_study_hours_all"] = q(t7.pop("_all", [0]))
    t7["policy_study_untimed"] = sum(1 for r in live.itertuples() for v in (json.loads((out / "06_cases" / f"{r.case_id}.json").read_text())["metadata"].get("policy_study_hours") or {}).values() if v.get("t_h_from_ed_arrival") is None)
    # decision 47: repeat values served, like for like with the task-06 build on the cases common to both selections
    if (out / "06_selection_task06.csv").exists() and (out / "06_cases_task06").exists():
        s6 = pd.read_csv(out / "06_selection_task06.csv")
        l6 = set(s6[s6.case_id.notna() & s6.exclusion.isna()].case_id)
        both = sorted(l6 & set(live.case_id))
        sv = lambda d, c: (json.loads((d / f"{c}.json").read_text())["metadata"]["build_counts"].get("c6_serial_lab_values", 0)
                           if (d / f"{c}.json").exists() else 0)
        t7["repeat_values_like_for_like"] = {"common_cases": len(both), "task06": sum(sv(out / "06_cases_task06", c) for c in both),
                                             "task07": sum(sv(out / "06_cases", c) for c in both)}
    flow["task07"] = {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in t7.items()}
    print("\n== task 07:", json.dumps(flow["task07"], default=str)[:3000])
    (rep / a.flow_name).write_text(json.dumps(flow, indent=1, default=str))
    print("\nflow written:", rep / a.flow_name)


if __name__ == "__main__":
    main()
