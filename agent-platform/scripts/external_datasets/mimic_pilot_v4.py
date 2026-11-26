"""MIMIC-IV neurology pilot, task 04: decisions 20-29 (workspace CLAUDE.md) on top of task 03.
Counts only on stdout; IDs only under OUT. No record content in this file (PhysioNet DUA).

Stages
  labs4    per admission of the task-03 candidate cohort: the first value of every blood lab item in
           the lab window (ED arrival - 1 h to admission + 24 h), whether it is a de-identification
           blank (decision 27), whether a treatment that changes it came first (decision 23,
           ``mimic_treat``); the first CSF sample with its blank values; treatment times per class.
           -> OUT/04_labfirst.parquet, 04_csffirst.parquet, 04_treatments.parquet, 04_treat_first.parquet
  strict4  strict complete counts with decisions 23 and 27 (each switched off for its marginal), FEPI
           added (20), FEPI record support at the focal-epilepsy level.
           -> OUT/04_strict.csv, 04_strict_marginal.csv
  select4  pilot selection, six conditions (FEPI added last so the task-03 draws are unchanged);
           earlier case ids stay with their admission; exclusions after reading in 04_exclusions.csv.
           -> OUT/04_selection.csv, 04_selection_counts.csv

    nice -n 10 uv run -q --no-project --with duckdb --with pandas --with pyarrow python -I \
        mimic_pilot_v4.py --stage labs4|strict4|select4 --out $W/out --tmp $W/tmp
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
from mimic_pilot_cohort import connect, csv, paths  # noqa: E402
from mimic_pilot_v3 import ALL_PANELS, CANDIDATES, PREFIX3, core_steps, served, strict_pool  # noqa: E402
from mimic_treat import AED_LEVELS, AFFECTS, CLASSES, first_times, treatment_rows  # noqa: E402

PILOT4 = ["ISCH", "SAH", "SE", "GBS", "MS", "FEPI"]
PREFIX4 = {**PREFIX3, "FEPI": "MIMIC-FEPI"}
CSF_GROUPS = {"cells": r"WBC|Total Nucleated|White Blood|Polys|Lymphs|RBC", "protein": r"Protein", "glucose": r"Glucose"}
# Focal epilepsy named in the discharge diagnosis (decision 10 at the level of the condition code).
FEPI_SUPPORT = r"epilep|partial\s+seiz|focal\s+seiz|complex\s+partial|focal\s+(?:onset|aware|impaired)"
BLANK = r"^\s*_{3}\s*$"
JUNK = r"H|I|L|[SU]TX\d+|HPE\d+|Delete|Voided Specimen|.*\bHold\b.*|Specimen Type|Problem"


def is_blank(value, valuenum) -> bool:
    return pd.isna(valuenum) and bool(re.search(r"_{3}", str(value))) and not re.search(r"\d", str(value))


def stage_labs4(a) -> None:
    p, con, out = paths(a.physionet), connect(a.tmp), Path(a.out)
    flags = pd.read_csv(out / "03_cohort_flags.csv", parse_dates=["admittime", "dischtime", "ed_intime"])
    coh = flags[flags.usable3 & flags.condition.isin(CANDIDATES)].copy()
    coh["t_ed"] = coh[["ed_intime", "admittime"]].min(axis=1)
    coh["t0"] = coh.t_ed - pd.Timedelta(hours=1)
    coh["t_end"] = coh.admittime + pd.Timedelta(hours=24)
    con.register("c4", coh[["subject_id", "hadm_id", "t0", "t_end", "dischtime"]])
    labels = sorted({x for groups in ALL_PANELS.values() for g in groups for x in g} | set().union(*AFFECTS.values()) | set(AED_LEVELS))
    con.register("lab_labels", pd.DataFrame({"label": labels}))
    con.execute(f"create table items as select itemid, label, fluid, category from {csv(p['hosp'] / 'd_labitems.csv.gz')}")
    cache = Path(a.tmp) / "04_labs4_raw"
    cache.mkdir(exist_ok=True)
    if (cache / "tr.parquet").exists() and a.reuse:
        rows, csf, tr = (pd.read_parquet(cache / f"{k}.parquet") for k in ("rows", "csf", "tr"))
    else:
        rows, csf, tr = query_labs4(con, p, coh)
        for k, v in (("rows", rows), ("csf", csf), ("tr", tr)):
            v.to_parquet(cache / f"{k}.parquet", index=False)
    return finish_labs4(out, rows, csf, tr)


def query_labs4(con, p, coh):
    rows = con.execute(f"""
        select c.hadm_id, l.hadm_id lab_hadm, l.itemid, i.label, i.fluid, i.category, l.charttime t, l.value, l.valuenum
        from {csv(p['hosp'] / 'labevents.csv.gz')} l join items i using (itemid)
        join c4 c on l.subject_id = c.subject_id and l.charttime between c.t0 and c.t_end
        where i.fluid = 'Blood' and (l.value is not null or l.valuenum is not null)""").df()
    csf = con.execute(f"""
        select c.hadm_id, l.hadm_id lab_hadm, l.itemid, i.label, l.charttime t, l.value, l.valuenum
        from {csv(p['hosp'] / 'labevents.csv.gz')} l join items i using (itemid)
        join c4 c on l.subject_id = c.subject_id and l.charttime between c.t0 and c.dischtime
        where i.fluid = 'Cerebrospinal Fluid' and (l.value is not null or l.valuenum is not null)""").df()
    tr = treatment_rows(con, p, coh)
    return rows, csf, tr


def finish_labs4(out, rows, csf, tr, prefix="04"):
    rows = rows[~(rows.lab_hadm.notna() & (rows.lab_hadm != rows.hadm_id))]
    rows = rows[~rows.label.str.fullmatch(JUNK, case=False, na=False) & ~rows.value.astype(str).str.contains(r"^HOLD|DISCARD", case=False, na=False)]
    first = rows.sort_values("t").drop_duplicates(["hadm_id", "itemid"])
    first["blank"] = [is_blank(v, n) for v, n in zip(first.value, first.valuenum)]
    csf = csf[~(csf.lab_hadm.notna() & (csf.lab_hadm != csf.hadm_id))]
    t1 = csf.groupby("hadm_id").t.min().rename("t1")
    csf = csf.merge(t1, on="hadm_id")
    csf = csf[csf.t <= csf.t1 + pd.Timedelta(hours=1)].sort_values("t").drop_duplicates(["hadm_id", "itemid"])
    csf["blank"] = [is_blank(v, n) for v, n in zip(csf.value, csf.valuenum)]
    ft = first_times(tr)
    # decision 23 per first value
    ftd = ft.set_index("hadm_id")
    aed = tr[tr.classes.str.contains("antiseizure", na=False)].groupby("hadm_id")[["t", "name"]].apply(lambda g: list(zip(g["t"], g["name"]))).to_dict()
    from mimic_treat import blocked
    tt = {h: {k[2:]: v for k, v in r.items() if k.startswith("t_")} for h, r in ftd.to_dict("index").items()}
    first["blocked"] = [blocked(lb, t, tt.get(h, {}), aed.get(h, []))
                        for h, lb, t in zip(first.hadm_id, first.label, first.t)]
    first = first.merge(ft[["hadm_id", "t_first_ed_med"]], on="hadm_id", how="left")
    first["after_first_ed_med"] = first.t_first_ed_med.notna() & (first.t > first.t_first_ed_med)
    keep = ["hadm_id", "itemid", "label", "category", "t", "blank", "blocked", "after_first_ed_med"]
    first[keep].to_parquet(out / f"{prefix}_labfirst.parquet", index=False)
    csf[["hadm_id", "itemid", "label", "t", "blank"]].to_parquet(out / f"{prefix}_csffirst.parquet", index=False)
    tr[["hadm_id", "t", "source", "name", "classes"]].to_parquet(out / f"{prefix}_treatments.parquet", index=False)
    ft.to_parquet(out / f"{prefix}_treat_first.parquet", index=False)
    print(f"admissions {rows.hadm_id.nunique()}; first blood values {len(first)}; blank {int(first.blank.sum())}; "
          f"blocked by class {first[first.blocked != ''].blocked.value_counts().to_dict()}; CSF first-sample values {len(csf)}, blank {int(csf.blank.sum())}")
    print("treatment rows by source:", tr.source.value_counts().to_dict())
    print("admissions with a class timed in the window:", {k: int(ft[f't_{k}'].notna().sum()) for k in CLASSES})


def lab_flags(out: Path, tab: pd.DataFrame, prefix: str = "04") -> pd.DataFrame:
    """Panel and CSF flags per admission under decisions 23 / 27 (each on or off)."""
    lf = pd.read_parquet(out / f"{prefix}_labfirst.parquet")
    cf = pd.read_parquet(out / f"{prefix}_csffirst.parquet")
    res = pd.DataFrame({"hadm_id": tab.hadm_id})
    for d23 in (False, True):
        for d27 in (False, True):
            x = lf
            if d23:
                x = x[x.blocked == ""]
            if d27:
                x = x[~x.blank]
            have = x.groupby("hadm_id").label.apply(set).to_dict()
            sfx = f"_{int(d23)}{int(d27)}"
            for pn, groups in ALL_PANELS.items():
                res[f"panel_{pn}{sfx}"] = [all(any(lb in have.get(h, set()) for lb in g) for g in groups) for h in res.hadm_id]
    for d27 in (False, True):
        c = cf[~cf.blank] if d27 else cf
        lab = c.groupby("hadm_id").label.apply(lambda s: " ; ".join(sorted(s))).to_dict()
        res[f"csf_first_{int(d27)}"] = [bool(lab.get(h)) and all(re.search(rx, lab.get(h, "")) for rx in CSF_GROUPS.values()) for h in res.hadm_id]
    return res


def tab4(out: Path) -> pd.DataFrame:
    tab = pd.read_parquet(out / "03_tables.parquet")
    nt = pd.read_parquet(out / "03_notes.parquet").set_index("hadm_id").text
    from mimic_pilot_v3 import DX_SECTION
    f = tab.condition == "FEPI"
    sec = [(DX_SECTION.search(nt.get(h, "") or "") or [None, ""])[1] for h in tab.hadm_id[f]]
    tab.loc[f, "dx_support"] = [bool(re.search(FEPI_SUPPORT, s or "", re.I)) for s in sec]
    tab.loc[f, "dx_reason"] = ["" if ok else "discharge diagnosis does not name a focal epilepsy" for ok in tab.loc[f, "dx_support"]]
    return tab.merge(lab_flags(out, tab), on="hadm_id", how="left")


def served4(t: pd.DataFrame, step: str, panels: list[str], rules: dict) -> pd.Series:
    sfx = f"_{int(rules['d23'])}{int(rules['d27'])}"
    if step == "labs":
        use = [x for x in panels if x not in rules["dropped_panels"] and f"panel_{x}{sfx}" in t]
        return pd.concat([t[f"panel_{x}{sfx}"] for x in use], axis=1).all(axis=1) if use else pd.Series(True, index=t.index)
    if step == "csf":
        return t[f"csf_first_{int(rules['d27'])}"]
    return served(t, step, panels, rules)


def rules_for(t: pd.DataFrame, cond: str) -> tuple[list[str], list[str], dict]:
    steps, panels = core_steps(cond)
    steps = [s for s in steps if not s.startswith("knowledge")]
    dropped = [x for x in panels if (t[f"panel_{x}"].mean() if f"panel_{x}" in t else 0.0) < 0.5]
    rules = {"d1_ecg_table": True, "d2_cta_split": True, "d3_panel_rule": True, "d5_rhythm": True, "d10_support": True,
             "d11_age": True, "timing": True, "se_strict_eeg": True, "dropped_panels": dropped, "steps": steps,
             "d23": True, "d27": True}
    return steps, panels, rules


def ok_mask(t, steps, panels, rules) -> pd.Series:
    ok = pd.Series(True, index=t.index)
    for s in steps:
        ok &= served4(t, s, panels, rules)
    return ok & ~t.age_over_89


def stage_strict4(a) -> None:
    out = Path(a.out)
    tab = tab4(out)
    rows, marg = [], []
    for cond in CANDIDATES:
        t = tab[tab.condition == cond].reset_index(drop=True)
        steps, panels, rules = rules_for(t, cond)
        cnt = lambda r: int((ok_mask(t, steps, panels, r) & t.dx_support).sum())
        full = cnt(rules)
        rows.append({"condition": cond, "cohort": len(t), "core_steps": ";".join(steps), "panels_dropped": ";".join(rules["dropped_panels"]),
                     "strict_complete_04": full, "strict_before_support": int(ok_mask(t, steps, panels, rules).sum()),
                     "strict_03_rules": cnt({**rules, "d23": False, "d27": False})})
        for d in ("d23", "d27"):
            marg.append({"condition": cond, "decision": d, "with": full, "without": cnt({**rules, d: False})})
        # consistency: the task-03 panel flags against the recomputed ones with both rules off
        for pn in panels:
            if f"panel_{pn}" in t and f"panel_{pn}_00" in t:
                rows[-1][f"agree_{pn}"] = round(float((t[f"panel_{pn}"] == t[f"panel_{pn}_00"]).mean()), 3)
    s, m = pd.DataFrame(rows), pd.DataFrame(marg)
    s.to_csv(out / "04_strict.csv", index=False)
    m.to_csv(out / "04_strict_marginal.csv", index=False)
    with pd.option_context("display.width", 260, "display.max_colwidth", 60):
        print(s.to_string(index=False)); print()
        print(m.pivot(index="condition", columns="decision", values="without").to_string())


def stage_select4(a) -> None:
    """As task 03 (mimic_pilot_v3.stage_select3) with FEPI last and the decision-23/27 pool."""
    out = Path(a.out)
    tab = tab4(out)
    rev = pd.read_csv(out / "03_se_support_review.csv")
    if (out / "04_fepi_support_review.csv").exists():  # FEPI admissions without a focal-epilepsy discharge diagnosis, read
        rev = pd.concat([rev, pd.read_csv(out / "04_fepi_support_review.csv")], ignore_index=True)
    read_ok = set(rev[rev.supported].hadm_id)
    read_no = dict(zip(rev[~rev.supported].hadm_id, rev[~rev.supported].reason))
    exc_path = out / "04_exclusions.csv"
    ex_df = pd.read_csv(exc_path)
    excl = dict(ex_df[["hadm_id", "reason"]].itertuples(index=False))
    old = pd.read_csv(out / "02_selection.csv")
    old = old[old.case_id.notna() & (old.case_id != "")]
    old_ids = dict(zip(old.hadm_id, old.case_id))
    prev_ids = {}
    for f in ("03_selection.csv", "04_fepi_candidates.csv", "04_se_candidates.csv", "04_selection.csv"):
        if (out / f).exists():
            pr = pd.read_csv(out / f)
            pr = pr[pr.case_id.notna() & (pr.case_id != "")]
            prev_ids.update(dict(zip(pr.hadm_id, pr.case_id)))
    prev_ids.update({h: c for h, c in zip(ex_df.hadm_id, ex_df.case_id) if isinstance(c, str) and c})
    flags = pd.read_csv(out / "03_cohort_flags.csv")
    rows, counts = [], []
    rng = random.Random(a.seed)
    for cond in PILOT4:
        t = tab[tab.condition == cond].reset_index(drop=True)
        steps, panels, rules = rules_for(t, cond)
        # The draw order is the task-03 one: shuffle the task-03 pool (no 23/27), then apply 23/27.
        pool3 = strict_pool(tab, cond)
        ok4 = set(t[ok_mask(t, steps, panels, rules)].hadm_id)
        order = sorted(pool3.hadm_id)
        rng.shuffle(order)
        keep = []
        for rank, h in enumerate(order, start=1):
            r = pool3[pool3.hadm_id == h].iloc[0]
            if h in excl:
                reason = excl[h]
            elif h not in ok4:
                reason = "a required step loses its result under decision 23 / 27"
            elif r.dx_support or h in read_ok:
                reason = ""
            elif h in read_no:
                reason = "record does not support the code (read): " + read_no[h]
            else:
                reason = "record support not established (discharge diagnosis: " + str(r.dx_reason) + "; not read)"
            keep.append((rank, h, reason))
        counts.append({"condition": cond, "strict_pool_03": len(order), "eligible": sum(1 for _, _, x in keep if not x),
                       **pd.Series([x.split(" (")[0].split(":")[0] if x else "eligible" for _, _, x in keep]).value_counts().to_dict()})
        eligible = [h for _, h, x in keep if not x]
        first = [h for h in eligible if h in old_ids]
        rest = [h for h in eligible if h not in old_ids]
        rest = [h for h in rest if h in prev_ids] + [h for h in rest if h not in prev_ids]
        chosen = first + rest[: max(0, a.n - len(first))]
        known = {**{h: c for h, c in prev_ids.items() if c.startswith(PREFIX4[cond] + "-")}, **{h: old_ids[h] for h in first}}
        used = {int(c.rsplit("-", 1)[1]) for c in known.values()}
        nums = iter(i for i in range(1, 200) if i not in used)
        for rank, h, reason in keep:
            if h in known and (h in chosen or reason):
                cid, prev_note = (known[h] if h in chosen else ""), known[h]
            else:
                cid, prev_note = (f"{PREFIX4[cond]}-{next(nums):03d}" if h in chosen else ""), ""
            rows.append({"case_id": cid, "condition": cond, "hadm_id": int(h),
                         "subject_id": int(flags.loc[flags.hadm_id == h, "subject_id"].iloc[0]),
                         "draw_rank": rank, "exclusion": reason, "task02_case": h in old_ids,
                         "excluded_case_id": prev_note if (reason and prev_note) else ""})
    sel = pd.DataFrame(rows)
    sel.to_csv(out / "04_selection.csv", index=False)
    c = pd.DataFrame(counts).fillna(0)
    c.to_csv(out / "04_selection_counts.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_columns", 20):
        print(c.to_string(index=False))
        print("selected:", sel[sel.case_id != ""].groupby("condition").size().to_dict())
        s3 = pd.read_csv(out / "03_selection.csv")
        s3 = s3[s3.case_id.notna() & (s3.case_id != "")]
        lost = s3[~s3.case_id.isin(sel.case_id)]
        print("task-03 cases no longer selected:", len(lost), "| reasons:",
              sel[sel.excluded_case_id.isin(lost.case_id)].exclusion.str.split(" \\(").str[0].value_counts().to_dict())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["labs4", "strict4", "select4"])
    ap.add_argument("--seed", type=int, default=20261107)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--physionet", default="/eos/user/a/aprotani/physionet")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tmp", required=True)
    ap.add_argument("--reuse", action="store_true", help="labs4: reuse the raw query results under TMP")
    a = ap.parse_args()
    if not str(Path(a.out).resolve()).startswith(("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")):
        sys.exit("--out must be under the PhysioNet workspace (DUA)")
    {"labs4": stage_labs4, "strict4": stage_strict4, "select4": stage_select4}[a.stage](a)


if __name__ == "__main__":
    main()
