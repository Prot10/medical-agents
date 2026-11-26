"""MIMIC-IV neurology pilot, task 06: strict pools for all 20 conditions under decisions 1-41, and
the 100-case selection. Counts only on stdout; IDs only under OUT. No record content in this file.

Stages
  labs6    first blood values, first CSF sample and treatment times for the usable cohort of all 20
           conditions (as labs4), with anticoagulants classified by dose (decision 30).
           -> OUT/06_labfirst.parquet, 06_csffirst.parquet, 06_treatments.parquet, 06_treat_first.parquet, 06_anticoag.parquet
  strict6  strict pools for every condition: usable cohort, then a recorded result for every core step
           of the condition's NeuroBench policy, then the decisions; marginal counts and the main drop
           reason per condition. -> OUT/06_strict.csv, 06_strict_steps.csv
  select6  the 100-case selection (allocation below) -> OUT/06_selection.csv, 06_selection_counts.csv

Tables come from mimic_pilot_v3.stage_tables3 run on all 20 conditions into OUT/06_work/.

    nice -n 10 uv run -q --no-project --with duckdb --with pandas --with pyarrow python -I \
        mimic_pilot_v6.py --stage labs6|strict6|select6 --out $W/out --tmp $W/tmp
"""

from __future__ import annotations

import argparse
import random
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mimic_pilot_cohort import CONDITIONS, connect, csv, paths  # noqa: E402
from mimic_pilot_v3 import ALL_PANELS, DX_SECTION, SUPPORT, core_steps, served  # noqa: E402
from mimic_pilot_v4 import CSF_GROUPS, FEPI_SUPPORT, finish_labs4, lab_flags, query_labs4  # noqa: E402
from mimic_treat import anticoag_rows  # noqa: E402

# Record evidence for steps the task-03 detectors did not cover (new conditions).
ASSESS = {  # perform_clinical_assessment.assessment_type -> what the note must record
    "performance_status": r"\bKPS\b\s*(?:of|:|=|was|is)?\s*\d|Karnofsky[^.]{0,30}\d|\bECOG\b[^.]{0,25}\d",
    "functional_neuro_signs": r"Hoover|give[- ]?way weakness|entrainment|collapsing weakness|midline splitting|"
                              r"functional (?:weakness|signs?|exam|neurolog)|non-?physiolog|inconsistent (?:with|exam|effort)",
    "cognitive_screen": r"\bMoCA\b[^.]{0,20}\d|\bMMSE\b[^.]{0,20}\d|Montreal Cognitive[^.]{0,30}\d|Mini[- ]Mental[^.]{0,30}\d",
    "gait_and_balance_timed": r"timed up and go|\bTUG\b[^.]{0,20}\d|timed (?:walk|gait)|\d+\s*(?:m|meter|foot|feet) walk[^.]{0,30}\d+\s*s",
    "orthostatic_blood_pressure": r"orthostatic (?:vital signs?|vitals|blood pressures?|BPs?)[^.]{0,80}\d{2,3}/\d{2,3}",
    "structured_headache_history_ichd3": r"$^",  # an act on the history, never a recorded result
}
TISSUE = re.compile(r"(?is)(?:patholog|biopsy|resection|frozen section)[^.]{0,200}(?:glioblastoma|astrocytoma|oligodendroglioma|glioma|"
                    r"WHO grade|IDH|ependymoma|lymphoma|metasta)")
# Conditions whose required work-up an ED admission cannot supply (clinic diagnoses over months, or
# a required step with no record source); stated in the method document.
NOT_ED = {"ALZ": "neuropsychological battery and cognitive screen in clinic", "FTD": "neuropsychological battery in clinic",
          "VASC": "cognitive screen and longitudinal course in clinic", "PD": "clinical diagnosis over months; DaT imaging outpatient",
          "NPH": "elective lumbar drain / tap test admissions, not ED", "MIG": "the required step is a structured ICHD-3 history, an act with no recorded result",
          "ALS": "EMG and longitudinal course in clinic"}
PILOT6 = ["ISCH", "SAH", "SE", "GBS", "MS", "FEPI"]
PREFIX = lambda c: f"MIMIC-{c}"


def stage_labs6(a) -> None:
    p, con, out = paths(a.physionet), connect(a.tmp), Path(a.out)
    flags = pd.read_csv(out / "03_cohort_flags.csv", parse_dates=["admittime", "dischtime", "ed_intime"])
    coh = flags[flags.usable3 & flags.condition.isin(CONDITIONS)].copy()
    coh["t_ed"] = coh[["ed_intime", "admittime"]].min(axis=1)
    coh["t0"] = coh.t_ed - pd.Timedelta(hours=1)
    coh["t_end"] = coh.admittime + pd.Timedelta(hours=24)
    con.register("c4", coh[["subject_id", "hadm_id", "t0", "t_end", "dischtime"]])
    con.execute(f"create table items as select itemid, label, fluid, category from {csv(p['hosp'] / 'd_labitems.csv.gz')}")
    cache = Path(a.tmp) / "06_labs6_raw"
    cache.mkdir(exist_ok=True)
    if (cache / "tr.parquet").exists() and a.reuse:
        rows, csfr, tr = (pd.read_parquet(cache / f"{k}.parquet") for k in ("rows", "csf", "tr"))
    else:
        rows, csfr, tr = query_labs4(con, p, coh)
        for k, v in (("rows", rows), ("csf", csfr), ("tr", tr)):
            v.to_parquet(cache / f"{k}.parquet", index=False)
    if (cache / "ac.parquet").exists() and a.reuse:
        ac = pd.read_parquet(cache / "ac.parquet")
    else:
        ac = anticoag_rows(con, p, coh)
        for c in ("dose", "unit", "route", "name", "source"):
            ac[c] = ac[c].astype(str)
        ac.to_parquet(cache / "ac.parquet", index=False)
    # eMAR heparin rows carry the dose but no route: a dose <= 5,000 units counts as prophylactic when the
    # admission holds a subcutaneous prophylactic heparin prescription (the order the eMAR row executes).
    proph_rx = set(ac[(ac.source == "hosp_prescriptions") & (ac.level == "prophylactic") & ac.name.str.contains("(?i)heparin", na=False)].hadm_id)
    dnum = pd.to_numeric(ac.dose, errors="coerce")
    m = (ac.source == "hosp_emar") & (ac.level == "unknown") & ac.name.str.fullmatch(r"(?i)heparin", na=False) & (dnum <= 5000) \
        & ac.unit.str.upper().str.contains("UNIT", na=False) & ac.hadm_id.isin(proph_rx)
    ac.loc[m, "level"] = "prophylactic"
    print(f"eMAR heparin <= 5,000 units with a prophylactic SC prescription in the admission: {int(m.sum())} reclassified prophylactic")
    # decision 30: the anticoagulation class comes only from therapeutic (or unknown-dose) administrations
    tr = tr.copy()
    tr["classes"] = tr.classes.fillna("").str.replace(r"(?:^|;)anticoagulation", "", regex=True).str.strip(";")
    blk = ac[ac.level != "prophylactic"].assign(classes="anticoagulation")[["hadm_id", "t", "source", "name", "classes"]]
    tr = pd.concat([tr, blk], ignore_index=True)
    ac.to_parquet(out / "06_anticoag.parquet", index=False)
    finish_labs4(out, rows, csfr, tr, prefix="06")
    print("anticoagulant administrations by level:", ac.level.value_counts().to_dict(), "| by source x level:",
          ac.groupby(["source", "level"]).size().to_dict())
    lf4 = pd.read_parquet(out / "04_labfirst.parquet")
    lf6 = pd.read_parquet(out / "06_labfirst.parquet")
    m = lf4.merge(lf6, on=["hadm_id", "itemid"], suffixes=("_04", "_06"))
    back = m[(m.blocked_04 == "anticoagulation") & (m.blocked_06 == "")]
    print(f"decision 30: first coagulation values blocked under 23 that come back: {len(back)} of {int((m.blocked_04 == 'anticoagulation').sum())}")


def tab6(out: Path) -> pd.DataFrame:
    w = out / "06_work"
    tab = pd.read_parquet(w / "03_tables.parquet")
    nt = pd.read_parquet(w / "03_notes.parquet").set_index("hadm_id").text
    # decision 10, automatic pass: the discharge-diagnosis section names the condition (FEPI: a focal
    # epilepsy; SYNC: a cardiac cause; patterns in mimic_pilot_v3.SUPPORT); reading decides the rest.
    sec = [(DX_SECTION.search(nt.get(h, "") or "") or [None, ""])[1] or "" for h in tab.hadm_id]
    tab["dx_support"] = [bool(re.search(FEPI_SUPPORT if c == "FEPI" else SUPPORT[c], x, re.I)) for c, x in zip(tab.condition, sec)]
    for k, rx in ASSESS.items():
        tab[f"assess_{k}"] = [bool(re.search(rx, nt.get(h, "") or "", re.I)) for h in tab.hadm_id]
    tab["note_tissue"] = [bool(TISSUE.search(nt.get(h, "") or "")) for h in tab.hadm_id]
    lf = lab_flags(out, tab, prefix="06")
    return tab.merge(lf, on="hadm_id", how="left")


def micro_flags(a, tab: pd.DataFrame) -> pd.DataFrame:
    """Ascitic fluid microbiology in the stay (HEP), from microbiologyevents."""
    out = Path(a.out)
    f = out / "06_work" / "micro_ascitic.parquet"
    if not f.exists():
        p, con = paths(a.physionet), connect(a.tmp)
        flags = pd.read_csv(out / "03_cohort_flags.csv", parse_dates=["admittime", "dischtime", "ed_intime"])
        coh = flags[flags.hadm_id.isin(tab.hadm_id)][["subject_id", "hadm_id", "admittime", "dischtime", "ed_intime"]].copy()
        coh["t0"] = coh[["ed_intime", "admittime"]].min(axis=1) - pd.Timedelta(hours=1)
        con.register("cm", coh)
        m = con.execute(f"""select distinct c.hadm_id from {csv(p['hosp'] / 'microbiologyevents.csv.gz')} m join cm c on m.subject_id = c.subject_id
                            and coalesce(m.charttime, cast(m.chartdate as timestamp)) between c.t0 and c.dischtime
                            where upper(m.spec_type_desc) like 'PERITONEAL FLUID%'""").df()
        m.to_parquet(f, index=False)
    s = set(pd.read_parquet(f).hadm_id)
    return tab.assign(micro_ascitic=tab.hadm_id.isin(s))


def served6(t: pd.DataFrame, step: str, panels: list[str], rules: dict, tmpl_args: dict) -> pd.Series:
    sfx = "_11"
    if step == "labs":
        use = [x for x in panels if x not in rules["dropped_panels"] and f"panel_{x}{sfx}" in t]
        return pd.concat([t[f"panel_{x}{sfx}"] for x in use], axis=1).all(axis=1) if use else pd.Series(True, index=t.index)
    if step == "csf":
        return t["csf_first_1"]
    if step == "echo":
        return t.note_echo
    if step == "perform_clinical_assessment":
        kinds = tmpl_args.get(step, [])
        ok = pd.Series(True, index=t.index)
        for k in kinds:
            ok &= t.get(f"assess_{k}", pd.Series(False, index=t.index))
        return ok
    if step == "obtain_tissue_diagnosis":
        return t.note_tissue
    if step == "micro:ascitic_fluid":
        return t.micro_ascitic
    return served(t, step, panels, rules)


def assess_kinds(cond: str) -> dict:
    """The assessment types the condition's templates require (>= half of its cases)."""
    import collections
    import json
    root = HERE.parents[2] / "data/neurobench/cases"
    files = sorted(root.glob(f"{cond}-*.json"))
    c = collections.Counter()
    for f in files:
        seen = set()
        for cr in json.loads(f.read_text())["ground_truth"]["action_criteria"]:
            if cr["importance"] != "required":
                continue
            for alt in cr["alternatives"]:
                if alt["tool_name"] == "perform_clinical_assessment":
                    seen.add(alt.get("required_arguments", {}).get("assessment_type"))
        c.update(seen)
    return {"perform_clinical_assessment": [k for k, v in c.items() if k and v >= len(files) / 2]}


def strict_table(a) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    out = Path(a.out)
    tab = micro_flags(a, tab6(out))
    rows, steps_rows, pools = [], [], []
    for cond in CONDITIONS:
        t = tab[tab.condition == cond].reset_index(drop=True)
        steps, panels = core_steps(cond)
        steps = [s for s in steps if not s.startswith("knowledge")]
        dropped = [x for x in panels if (t[f"panel_{x}"].mean() if f"panel_{x}" in t else 0.0) < 0.5]
        rules = {"d1_ecg_table": True, "d2_cta_split": True, "d3_panel_rule": True, "d5_rhythm": True, "d10_support": True,
                 "d11_age": True, "timing": True, "se_strict_eeg": True, "dropped_panels": dropped, "steps": steps}
        targs = assess_kinds(cond)
        ok = ~t.age_over_89
        first_fail = pd.Series("", index=t.index)
        for s in steps:
            sv = served6(t, s, panels, rules, targs)
            steps_rows.append({"condition": cond, "step": s, "usable": len(t), "with_result": int(sv.sum())})
            first_fail[(first_fail == "") & ~sv & ok] = s
            ok &= sv
        sup = t.dx_support.astype(bool)
        first_fail[(first_fail == "") & ok & ~sup] = "record support (discharge diagnosis)"
        main = first_fail[first_fail != ""].value_counts()
        rows.append({"condition": cond, "usable": len(t), "core_steps": ";".join(steps), "panels_dropped": ";".join(dropped),
                     "assessment_required": ";".join(targs["perform_clinical_assessment"]),
                     "strict_before_support": int(ok.sum()), "strict": int((ok & sup).sum()),
                     "main_drop": f"{main.index[0]} ({int(main.iloc[0])})" if len(main) else "",
                     "ed_servable": cond not in NOT_ED, "not_ed_reason": NOT_ED.get(cond, "")})
        pools.append(t[ok].assign(strict_support=sup[ok]))
    return pd.DataFrame(rows), pd.DataFrame(steps_rows), pd.concat(pools)


def stage_strict6(a) -> None:
    out = Path(a.out)
    s, st, pool = strict_table(a)
    s.to_csv(out / "06_strict.csv", index=False)
    st.to_csv(out / "06_strict_steps.csv", index=False)
    pool[["hadm_id", "condition", "strict_support"]].to_csv(out / "06_strict_pool.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_colwidth", 70):
        print(s.drop(columns=["core_steps"]).to_string(index=False))


def stage_select6(a) -> None:
    """Allocation: the six task-04 conditions keep their cases (task-04 ids, decisions 32-34 applied by
    reading); new ED-servable conditions in order of strict pool size, 10 each (fewer if the pool is
    smaller, all taken); then ISCH, SAH, SE, MS raised towards 15 until 100. Draws: fixed seed, the
    strict pool's admissions shuffled once per condition; exclusions on reading in 06_exclusions.csv."""
    out = Path(a.out)
    s = pd.read_csv(out / "06_strict.csv").set_index("condition")
    pool = pd.read_csv(out / "06_strict_pool.csv")
    excl = pd.read_csv(out / "06_exclusions.csv") if (out / "06_exclusions.csv").exists() else pd.DataFrame(columns=["hadm_id", "case_id", "reason"])
    ex = dict(zip(excl.hadm_id, excl.reason))
    for f in ("03_se_support_review.csv", "04_fepi_support_review.csv"):  # read earlier and not supported
        if (out / f).exists():
            rv = pd.read_csv(out / f)
            for h, r in zip(rv[~rv.supported].hadm_id, rv[~rv.supported].get("reason", pd.Series(dtype=str))):
                ex.setdefault(h, "record does not support the code (read): " + str(r))
    s4 = pd.read_csv(out / "04_selection.csv")
    ids = {}
    for f in ("03_selection.csv", "04_selection.csv", "04_fepi_candidates.csv", "04_se_candidates.csv", "06_ids.csv"):
        if (out / f).exists():
            d = pd.read_csv(out / f)
            d = d[d.case_id.notna() & (d.case_id != "")]
            ids.update(dict(zip(d.hadm_id, d.case_id)))
    ids.update({h: c for h, c in zip(excl.hadm_id, excl.case_id) if isinstance(c, str) and c})
    flags = pd.read_csv(out / "03_cohort_flags.csv")
    rng = random.Random(a.seed)
    target = {}
    live4 = s4[s4.case_id.notna() & (s4.case_id != "")]
    new = [c for c in s.sort_values("strict", ascending=False).index if c not in PILOT6 and s.loc[c, "ed_servable"] and s.loc[c, "strict"] > 0]
    rows, counts = [], []
    for cond in PILOT6 + new:
        order = sorted(pool[pool.condition == cond].hadm_id)
        rng.shuffle(order)
        if cond in PILOT6:
            # task-04 cases first (their draw order), then the rest of the strict pool in the new order
            prev = [h for h in live4[live4.condition == cond].hadm_id if h in set(order) or True]
            order = prev + [h for h in order if h not in set(prev)]
        target[cond] = a.raise_to.get(cond, 10)
        chosen, n_ok = [], 0
        used = {int(c.rsplit("-", 1)[1]) for h, c in ids.items() if c.startswith(PREFIX(cond) + "-")}
        nums = iter(i for i in range(1, 400) if i not in used)
        for rank, h in enumerate(order, start=1):
            reason = ex.get(h, "")
            sup = bool(pool[(pool.hadm_id == h)].strict_support.iloc[0]) if (pool.hadm_id == h).any() else True
            if not reason and cond not in ("SE", "FEPI") and not sup and h not in ids:
                reason = "record support not established (discharge diagnosis; not read)"
            take = (not reason) and n_ok < target[cond]
            if take:
                n_ok += 1
            cid = ids.get(h) or (f"{PREFIX(cond)}-{next(nums):03d}" if (take or h in ex) else "")
            if take or cid:
                ids[h] = cid
            rows.append({"case_id": cid if (take or reason) else "", "condition": cond, "hadm_id": int(h),
                         "subject_id": int(flags.loc[flags.hadm_id == h, "subject_id"].iloc[0]),
                         "draw_rank": rank, "exclusion": reason if reason else ("" if take else "not drawn"),
                         "task04_case": h in set(live4.hadm_id)})
        counts.append({"condition": cond, "strict": int(s.loc[cond, "strict"]) if cond in s.index else 0, "target": target[cond],
                       "selected": n_ok, "excluded_on_reading": sum(1 for r in rows if r["condition"] == cond and r["exclusion"] not in ("", "not drawn"))})
    sel = pd.DataFrame(rows)
    sel.loc[sel.exclusion == "not drawn", "case_id"] = ""
    sel.to_csv(out / "06_selection.csv", index=False)
    pd.DataFrame([{"hadm_id": h, "case_id": c} for h, c in ids.items() if c]).to_csv(out / "06_ids.csv", index=False)
    c = pd.DataFrame(counts)
    c.to_csv(out / "06_selection_counts.csv", index=False)
    print(c.to_string(index=False))
    print("selected total:", int(c.selected.sum()))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["labs6", "strict6", "select6"])
    ap.add_argument("--seed", type=int, default=20261108)
    ap.add_argument("--raise", dest="raise_", nargs="*", default=[], help="COND=N targets for the six pilot conditions")
    ap.add_argument("--physionet", default="/eos/user/a/aprotani/physionet")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tmp", required=True)
    ap.add_argument("--reuse", action="store_true")
    a = ap.parse_args()
    a.raise_to = {k: int(v) for k, v in (x.split("=") for x in a.raise_)}
    if not str(Path(a.out).resolve()).startswith(("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")):
        sys.exit("--out must be under the PhysioNet workspace (DUA)")
    {"labs6": stage_labs6, "strict6": stage_strict6, "select6": stage_select6}[a.stage](a)


if __name__ == "__main__":
    main()
