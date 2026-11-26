"""Task 08: room left per condition, under the current rules (decisions 1-51) and under candidate rule
changes (B1 readmissions, B2 chief complaint naming a test, B3 symptom code first, B4 one required
step short, B5 age above 89). Counts only on stdout; IDs only under $W/out/08_*. No record content here.

Stages
  cohort8   candidate admissions outside the usable cohort (B1, B2 from the principal-diagnosis cohort;
            B3 from a new query: the condition's code at position 2 or 3, a symptom code first)
            -> OUT/08_work/03_cohort_flags.csv (+ 06_work/ copy), OUT/08_candidates.csv
  tables8   per-admission tables for the candidates (mimic_pilot_v3.stage_tables3 on all 20 conditions)
            -> OUT/08_work/06_work/03_tables.parquet, 03_notes.parquet
  labs8     first values, CSF and treatment times for the candidates (mimic_pilot_v6.stage_labs6)
            -> OUT/08_work/06_*.parquet
  room8     the counts of A and B -> OUT/08_room_admissions.csv (IDs), REPORT/08_room.json (counts)

    nice -n 10 uv run -q --no-project --with duckdb --with pandas --with pyarrow python -I \
        mimic_room8.py --stage cohort8|tables8|labs8|room8 --out $W/out --tmp $W/tmp/08 --report $W/report

DuckDB runs with at most 4 threads and memory_limit 16GB (shared VM).
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import re
import shutil
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mimic_pilot_cohort as PC  # noqa: E402


def connect4(tmp: str):
    import duckdb
    con = duckdb.connect()
    con.execute(f"set temp_directory = '{tmp}'; set memory_limit = '16GB'; set threads = 4; set preserve_insertion_order = false")
    return con


PC.connect = connect4  # every stage below runs with at most 4 threads
import mimic_pilot_v3 as V3  # noqa: E402
import mimic_pilot_v6 as V6  # noqa: E402

V3.connect = V6.connect = connect4
CONDITIONS = PC.CONDITIONS
WS = ("/eos/user/a/aprotani/physionet/", "/eos/home-a/aprotani/physionet/")


def _ws(p: Path) -> Path:
    if not str(p.resolve()).startswith(WS):
        sys.exit(f"{p} must be under the PhysioNet workspace")
    return p


# --------------------------------------------------------------------------------------------
def stage_cohort8(a) -> None:
    out = _ws(Path(a.out))
    p, con = PC.paths(a.physionet), connect4(a.tmp)
    f3 = pd.read_csv(out / "03_cohort_flags.csv")
    base = f3.f_not_transfer & f3.f_via_ed & f3.f_note & f3.f_hidden_transfer_ok
    b1 = f3[base & ~f3.f_new & f3.f_cc3].assign(variant="B1_readmission")
    b2 = f3[base & f3.f_new & (f3.cc_class3 == "test_label")].assign(variant="B2_cc_test_label")
    # B3: the condition's code at position 2 or 3, a symptom code (ICD-10 chapter R, ICD-9 780-799) first
    con.execute(f"create table dx as select subject_id, hadm_id, seq_num, cast(icd_code as varchar) icd_code, icd_version "
                f"from {PC.csv(p['hosp'] / 'diagnoses_icd.csv.gz')}")
    con.execute(f"create table adm as select * from {PC.csv(p['hosp'] / 'admissions.csv.gz')}")
    codes = con.execute("select distinct icd_code code, icd_version from dx").df()
    codes["condition"] = [PC.neuro_condition(c, v) for c, v in zip(codes.code, codes.icd_version)]
    con.register("icdmap", codes.dropna(subset=["condition"]))
    con.execute("""create table sym as select hadm_id from dx where seq_num = 1 and (
                     (icd_version = 10 and icd_code like 'R%') or
                     (icd_version = 9 and regexp_matches(icd_code, '^7[89][0-9]')))""")
    con.execute("""create table c3 as select distinct d.subject_id, d.hadm_id, m.condition, a.admittime, a.dischtime, a.admission_location
                   from dx d join icdmap m on d.icd_code = m.code and d.icd_version = m.icd_version join adm a using (hadm_id)
                   where d.seq_num in (2, 3) and d.hadm_id in (select hadm_id from sym)""")
    con.execute("""create table prior as select distinct c.hadm_id, c.condition from c3 c
                   join adm a2 on a2.subject_id = c.subject_id and a2.admittime < c.admittime
                   join dx d2 on d2.hadm_id = a2.hadm_id join icdmap m2 on d2.icd_code = m2.code and d2.icd_version = m2.icd_version
                   where m2.condition = c.condition""")
    con.execute(f"create table eds as select * from {PC.csv(p['ed'] / 'edstays.csv.gz')} where hadm_id is not null")
    con.execute(f"""create table edcc as select e.hadm_id, min(e.intime) ed_intime,
                    string_agg(coalesce(t.chiefcomplaint, ''), ' | ' order by e.intime) cc
                    from eds e left join {PC.csv(p['ed'] / 'triage.csv.gz')} t using (subject_id, stay_id) group by e.hadm_id""")
    con.execute(f"create table dsum as select distinct hadm_id from {PC.csv(p['note'] / 'discharge.csv.gz')}")
    con.execute(f"""create table hid as select distinct hadm_id from {PC.csv(p['hosp'] / 'diagnoses_icd.csv.gz')}
                    where (icd_version = 9 and icd_code = 'V4588') or (icd_version = 10 and icd_code = 'Z9282')""")
    b3 = con.execute("""select c.*, not exists (select 1 from prior p where p.hadm_id = c.hadm_id and p.condition = c.condition) f_new,
                         coalesce(c.admission_location, '') not like 'TRANSFER%' f_not_transfer, e.hadm_id is not null f_via_ed,
                         e.ed_intime, e.cc, c.hadm_id in (select hadm_id from dsum) f_note,
                         c.hadm_id not in (select hadm_id from hid) f_hidden_transfer_ok
                         from c3 c left join edcc e using (hadm_id)""").df()
    b3 = b3[b3.condition.isin(CONDITIONS)].copy()
    b3["cc_class3"] = [min((V3.cc_class3(x, c, False) for x in str(cc).split(" | ")),
                           key=["transfer", "test_label", "symptom_label", "ok", "missing"].index) if isinstance(cc, str) else "missing"
                       for cc, c in zip(b3.cc, b3.condition)]
    b3["f_cc3"] = b3.cc_class3.isin(["ok", "symptom_label", "missing"])
    b3 = b3[b3.f_new & b3.f_not_transfer & b3.f_via_ed & b3.f_note & b3.f_hidden_transfer_ok & b3.f_cc3].assign(variant="B3_symptom_first")
    # chief-complaint text classes of B2 (label class only; the text stays here)
    cc = con.execute(f"""select e.hadm_id, string_agg(coalesce(t.chiefcomplaint, ''), ' | ') cc from eds e
                         left join {PC.csv(p['ed'] / 'triage.csv.gz')} t using (subject_id, stay_id) group by 1""").df()
    ccd = dict(zip(cc.hadm_id, cc.cc))
    LBL = [("SAH", r"\bSAH\b|subarach"), ("ICH/IPH/IVH", r"\bICH\b|\bIPH\b|\bIVH\b"), ("bleed/hemorrhage", r"bleed|hemorrhag|haemorrhag"),
           ("aneurysm", r"aneurysm"), ("meningitis/encephalitis", r"mening|enceph|ventriculitis"), ("infarct/LVO/tPA", r"infarct|LVO|thrombectomy|tPA"),
           ("disease name", r"\bMS\b|multiple sclerosis|demyelin|optic neuritis|flare|GBS|guillain|epilep|myasthen|NMDA|NCSE|status")]
    b2 = b2.assign(cc_label=[next((n for n, rx in LBL if re.search(rx, str(ccd.get(h, "")), re.I)), "other test label") for h in b2.hadm_id])
    keep = ["subject_id", "hadm_id", "condition", "admittime", "dischtime", "admission_location", "ed_intime", "variant"]
    cand = pd.concat([b1[keep], b2[keep + ["cc_label"]], b3[keep]], ignore_index=True)
    # every candidate gets tables once per (admission, condition); B1/B2 rows are principal-cohort rows
    cand["admittime"], cand["dischtime"], cand["ed_intime"] = (pd.to_datetime(cand[c]) for c in ("admittime", "dischtime", "ed_intime"))
    w = out / "08_work"
    (w / "06_work").mkdir(parents=True, exist_ok=True)
    fl = cand.drop_duplicates(["hadm_id", "condition"]).assign(usable3=True)
    for d in (w, w / "06_work"):
        fl.to_csv(d / "03_cohort_flags.csv", index=False)
    cand.to_csv(out / "08_candidates.csv", index=False)
    print("candidates per variant x condition:")
    print(cand.groupby(["variant", "condition"]).size().unstack(0, fill_value=0).to_string())


def stage_tables8(a) -> None:
    out = _ws(Path(a.out))
    V3.CANDIDATES = list(CONDITIONS)
    a2 = argparse.Namespace(**{**vars(a), "out": str(out / "08_work" / "06_work")})
    V3.stage_tables3(a2)


def stage_labs8(a) -> None:
    out = _ws(Path(a.out))
    w = out / "08_work"
    shutil.copy(out / "04_labfirst.parquet", w / "04_labfirst.parquet")  # labs6 ends with a 04-vs-06 comparison print
    a2 = argparse.Namespace(**{**vars(a), "out": str(w), "reuse": False})
    V6.stage_labs6(a2)


# --------------------------------------------------------------------------------------------
def step_masks(a, outdir: Path) -> pd.DataFrame:
    """Per admission x condition: every core step servable (bool columns step:<name>), dx support, age."""
    a2 = argparse.Namespace(**{**vars(a), "out": str(outdir)})
    tab = V6.micro_flags(a2, V6.tab6(outdir))
    res = []
    for cond in CONDITIONS:
        t = tab[tab.condition == cond].reset_index(drop=True)
        if t.empty:
            continue
        steps, panels = V3.core_steps(cond)
        steps = [s for s in steps if not s.startswith("knowledge")]
        dropped = DROPPED.get(cond, [])
        rules = {"d1_ecg_table": True, "d2_cta_split": True, "d3_panel_rule": True, "d5_rhythm": True, "d10_support": True,
                 "d11_age": True, "timing": True, "se_strict_eeg": True, "dropped_panels": dropped, "steps": steps}
        targs = V6.assess_kinds(cond)
        r = pd.DataFrame({"hadm_id": t.hadm_id, "condition": cond, "age_over_89": t.age_over_89.astype(bool),
                          "dx_support": t.dx_support.astype(bool)})
        for s in steps:
            r[f"step:{s}"] = V6.served6(t, s, panels, rules, targs).astype(bool).values
        res.append(r)
    return pd.concat(res, ignore_index=True)


DROPPED: dict = {}  # the panels dropped by decision 3, fixed from the task-06 cohort (not recomputed on candidates)


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    z, ph = 1.96, k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (round(max(0, c - h), 3), round(min(1, c + h), 3))


def stage_room8(a) -> None:
    out, rep = _ws(Path(a.out)), Path(a.report)
    s6 = pd.read_csv(out / "06_strict.csv").set_index("condition")
    for c in CONDITIONS:
        x = s6.loc[c, "panels_dropped"] if c in s6.index else ""
        DROPPED[c] = [y for y in str(x).split(";") if y and y != "nan"]
    pat = pd.read_csv(out / "03_cohort_flags.csv")[["hadm_id", "subject_id", "condition", "admittime"]]
    # ---- reading history over every task
    sels = []
    for f in sorted(glob.glob(str(out / "0[2-7]_selection.csv"))):
        s = pd.read_csv(f)
        s["task"] = Path(f).name[:2]
        sels.append(s[["case_id", "condition", "hadm_id", "subject_id", "exclusion", "task"]])
    S = pd.concat(sels, ignore_index=True)
    final = pd.read_csv(out / "07_selection.csv")
    live = final[final.case_id.notna() & final.exclusion.isna()]
    used_h, used_p = set(live.hadm_id), set(live.subject_id)
    drawn = S[S.case_id.notna()]
    read_h = set(drawn.hadm_id)
    # status of every read admission: kept (in the final 100) or its last exclusion reason
    last = drawn.sort_values("task").drop_duplicates("hadm_id", keep="last").set_index("hadm_id")
    ex_files = [pd.read_csv(f) for f in sorted(glob.glob(str(out / "0[2-6]_exclusions.csv")))]
    EX = pd.concat([e[["hadm_id", "reason"]] for e in ex_files], ignore_index=True).drop_duplicates("hadm_id", keep="last").set_index("hadm_id").reason
    reads = pd.DataFrame({"hadm_id": sorted(read_h)})
    reads["condition"] = [last.loc[h, "condition"] for h in reads.hadm_id]
    reads["kept"] = reads.hadm_id.isin(used_h)
    reads["reason"] = [("" if k else str(EX.get(h, last.loc[h, "exclusion"]))) for h, k in zip(reads.hadm_id, reads.kept)]
    reads["cls"] = reads.reason.str.replace(r"\s*\(.*$", "", regex=True).str.replace(r":.*$", "", regex=True).str.strip().str[:60]
    tasks_of = drawn.groupby("hadm_id").task.apply(set)
    reads["task_0407"] = [bool(tasks_of[h] & {"04", "06", "07"}) for h in reads.hadm_id]
    # ---- per-admission step masks, current cohort and candidates
    M0 = step_masks(a, out)
    M1 = step_masks(a, out / "08_work")
    cand = pd.read_csv(out / "08_candidates.csv")
    sp = pd.read_csv(out / "06_strict_pool.csv")
    pool = sp[sp.strict_support.astype(bool)]
    stepcols = lambda m: [c for c in m.columns if c.startswith("step:")]

    def nfail(m: pd.DataFrame) -> pd.Series:
        return sum((~m[c].fillna(True).astype(bool)).astype(int) for c in stepcols(m) if c in m)

    A, B, J = [], [], {"conditions": {}}
    Bcounts = {}
    for cond in CONDITIONS:
        m0 = M0[M0.condition == cond]
        sc = [c for c in stepcols(m0) if m0[c].notna().any()]
        p_strict = pool[pool.condition == cond]
        rd = reads[reads.condition == cond]
        rd47 = rd[rd.task_0407]
        n_read, n_kept = len(rd47), int(rd47.kept.sum())
        y = n_kept / n_read if n_read else float("nan")
        lo, hi = wilson(n_kept, n_read)
        room = p_strict[~p_strict.hadm_id.isin(read_h)].merge(pat[pat.condition == cond][["hadm_id", "subject_id"]], on="hadm_id", how="left")
        in100 = room[room.subject_id.isin(used_p)]
        newp = room[~room.subject_id.isin(used_p)].subject_id.nunique()
        top_ex = rd[~rd.kept].cls.value_counts().head(3)
        # main blocking steps among usable, not strict
        ok0 = pd.concat([m0[c].astype(bool) for c in sc], axis=1).all(axis=1) if sc else pd.Series(True, index=m0.index)
        nonstrict = m0[~(ok0 & m0.dx_support & ~m0.age_over_89)]
        block = {c[5:]: int((~nonstrict[c].astype(bool)).sum()) for c in sc}
        nsup = int((ok0 & ~m0.dx_support & ~m0.age_over_89).sum())
        if nsup:
            block["record support (discharge diagnosis)"] = nsup
        top_block = sorted(block.items(), key=lambda kv: -kv[1])[:3]
        row = {"condition": cond, "strict": int(s6.loc[cond, "strict"]) if cond in s6.index else 0, "used_in_100": int((live.condition == cond).sum()),
               "read_any_task": len(rd), "excluded_on_reading": int((~rd.kept).sum()),
               "main_exclusions": "; ".join(f"{k} ({v})" for k, v in top_ex.items()),
               "strict_never_read": len(room), "of_which_patient_in_100": len(in100), "distinct_new_patients": int(newp),
               "read_0407": n_read, "kept_0407": n_kept, "yield": None if not n_read else round(y, 3), "yield_ci": [lo, hi] if n_read and n_read < 10 else None,
               "expected_new": None if not n_read else round(newp * y, 1),
               "expected_new_range": [round(newp * lo, 1), round(newp * hi, 1)] if n_read and n_read < 10 else None,
               "usable_not_strict": len(nonstrict), "main_blocking_steps": "; ".join(f"{k} ({v})" for k, v in top_block),
               "ed_servable": cond not in V6.NOT_ED}
        A.append(row)
        # ---- candidates
        seen_p = used_p | set(room.subject_id)  # patients already counted in A or in the 100
        bc = {}
        for var in ("B1_readmission", "B2_cc_test_label", "B3_symptom_first"):
            cv = cand[(cand.variant == var) & (cand.condition == cond)]
            m1 = M1[M1.condition == cond].merge(cv[["hadm_id", "subject_id", "admittime"] + (["cc_label"] if var.startswith("B2") else [])],
                                                on="hadm_id")
            sc1 = [c for c in stepcols(m1) if c in m1 and m1[c].notna().any()] if len(m1) else []
            if len(m1):
                ok1 = pd.concat([m1[c].astype(bool) for c in sc1], axis=1).all(axis=1) if sc1 else pd.Series(True, index=m1.index)
                st = m1[ok1 & m1.dx_support & ~m1.age_over_89 & ~m1.hadm_id.isin(read_h) & ~m1.subject_id.isin(seen_p)]
                st = st.sort_values("admittime").drop_duplicates("subject_id")
            else:
                st = m1
            add = len(st)
            d = {"candidates": len(cv), "added_strict": add, "expected": None if not n_read else round(add * y, 1)}
            if var.startswith("B2") and len(st):
                d["by_label"] = st.cc_label.value_counts().to_dict()
            if var.startswith("B1") and len(st):
                d["_ids"] = list(st.hadm_id)
            bc[var] = d
        # B4: usable (current cohort), every step but one, dx support, age ok, not read, new patient
        m0p = m0.merge(pat[pat.condition == cond][["hadm_id", "subject_id"]], on="hadm_id", how="left")
        nf = nfail(m0p[["hadm_id"] + sc]) if sc else pd.Series(0, index=m0p.index)
        one = m0p[(nf == 1) & m0p.dx_support & ~m0p.age_over_89 & ~m0p.hadm_id.isin(read_h) & ~m0p.subject_id.isin(seen_p)]
        miss = {}
        for c in sc:
            k = int((~one[c].astype(bool)).sum())
            if k:
                miss[c[5:]] = k
        bc["B4_one_step_short"] = {"added_strict": int(one.subject_id.nunique()), "missing_step": miss,
                                   "expected": None if not n_read else round(one.subject_id.nunique() * y, 1)}
        # B5: age above 89 only
        five = m0p[ok0.values & m0p.dx_support.values & m0p.age_over_89.values & ~m0p.hadm_id.isin(read_h).values & ~m0p.subject_id.isin(seen_p).values]
        bc["B5_age_over_89"] = {"added_strict": int(five.subject_id.nunique()), "expected": None if not n_read else round(five.subject_id.nunique() * y, 1)}
        Bcounts[cond] = bc
    # B1: earlier-episode work-up in the note (proxy: the HPI names an earlier admission or episode and a study)
    nt = pd.read_parquet(out / "08_work" / "06_work" / "03_notes.parquet").set_index("hadm_id").text
    prior_rx = re.compile(r"(?i)(?:prior|previous|last|recent)\s+(?:admission|hospitali[sz]ation|episode|stroke|seizure|flare|bleed|presentation)|"
                          r"was (?:recently )?admitted|admitted (?:to|at) ___ (?:in|on)|in ___ (?:she|he) (?:was|had)")
    study_rx = re.compile(r"(?i)\bMRI?\b|\bCTA?\b|\bEEG\b|\bLP\b|lumbar puncture|\bCSF\b|angiogra|EMG|echo")
    for cond, bc in Bcounts.items():
        ids = bc["B1_readmission"].pop("_ids", [])
        n = 0
        for h in ids:
            hpi = (re.search(V3.HPI_RX, nt.get(h, "") or "") or [None, ""])[1] or ""
            n += any(prior_rx.search(s) and study_rx.search(s) for s in re.split(r"(?<=[.!?])\s+", hpi))
        bc["B1_readmission"]["earlier_workup_in_hpi"] = n
    J["A"] = A
    J["B"] = Bcounts
    J["pooled_yield_0407"] = round(reads[reads.task_0407].kept.mean(), 3)
    J["read_total"] = len(reads)
    (rep / "08_room.json").write_text(json.dumps(J, indent=1, default=str))
    # admission-level list (IDs, workspace only)
    pd.DataFrame([{"condition": r["condition"], **{k: v for k, v in r.items() if k != "condition"}} for r in A]).to_csv(out / "08_room_by_condition.csv", index=False)
    with pd.option_context("display.width", 300, "display.max_columns", 40, "display.max_colwidth", 80):
        print(pd.DataFrame(A).drop(columns=["main_exclusions", "main_blocking_steps"]).to_string(index=False))
        for r in A:
            print(r["condition"], "| exclusions:", r["main_exclusions"], "| blocking:", r["main_blocking_steps"])
        for c, bc in Bcounts.items():
            print(c, json.dumps(bc))
    print("pooled yield 04-07:", J["pooled_yield_0407"], "| written", rep / "08_room.json")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["cohort8", "tables8", "labs8", "room8"])
    ap.add_argument("--physionet", default="/eos/user/a/aprotani/physionet")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tmp", required=True)
    ap.add_argument("--report", default="")
    ap.add_argument("--reuse", action="store_true")
    a = ap.parse_args()
    _ws(Path(a.tmp))
    Path(a.tmp).mkdir(parents=True, exist_ok=True)
    {"cohort8": stage_cohort8, "tables8": stage_tables8, "labs8": stage_labs8, "room8": stage_room8}[a.stage](a)


if __name__ == "__main__":
    main()
