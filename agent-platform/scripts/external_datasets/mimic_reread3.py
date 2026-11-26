"""Field-by-field re-read support for task-03 cases: independent recomputation of the table fields
against the source bundle (labs, ECG, demographics, vitals, radiology text), printed as counts; with
--show, the presentation and report impressions for the reader (record content: only to the reader's
terminal, never to a report).

    python -I mimic_reread3.py --out $W/out --pick 2 --seed 11 [--show CASE]
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mimic_case_assemble import anchor, hours, ts  # noqa: E402

TAG = ["03"]
_N = lambda s: re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def recheck(out: Path, cid: str) -> dict:
    c = json.loads((out / f"{TAG[0]}_cases" / f"{cid}.json").read_text())
    b = json.loads((out / "02_source" / f"{cid}.json").read_text())
    t_ed = anchor(b)
    adm = ts(b["admission"][0]["admittime"])
    r = {"case": cid}
    # labs: each served row equals the first source value of that test in the window
    L = pd.DataFrame(b["labs"])
    L["t"] = pd.to_datetime(L.charttime)
    W = L[(L.t >= t_ed - pd.Timedelta(hours=1)) & (L.t <= adm + pd.Timedelta(hours=24)) & (L.value.notna() | L.valuenum.notna())]
    n = ok = 0
    for pname, rows in (c["initial_tool_outputs"].get("labs") or {}).get("panels", {}).items():
        for row in rows:
            n += 1
            g = W[(W.label == row["test"]) & W.fluid.isin(["Urine"] if pname == "urinalysis" else ["Blood"])].sort_values("t")
            if g.empty:
                continue
            v = g.iloc[0].valuenum if pd.notna(g.iloc[0].valuenum) else str(g.iloc[0].value)
            ok += (abs(float(v) - float(row["value"])) < 1e-9) if not isinstance(v, str) and not isinstance(row["value"], str) else str(v) == str(row["value"])
    r["labs_rows"], r["labs_match"] = n, ok
    # ECG: first machine read in the window; rate from RR
    e = c["initial_tool_outputs"].get("ecg")
    if e and b.get("ecg_machine"):
        m = sorted([x for x in b["ecg_machine"] if -1 <= (hours(x["ecg_time"], t_ed) or 99) <= hours(adm + pd.Timedelta(hours=24), t_ed)],
                   key=lambda x: x["ecg_time"])
        if m:
            x = m[0]
            r["ecg_rate_match"] = int(round(60000 / float(x["rr_interval"]))) == e["rate"]
            r["ecg_rhythm_match"] = str(x["report_0"]).strip() == e["rhythm"]
    # demographics, vitals
    p = b["patient"][0]
    d = c["patient"]["demographics"]
    r["age_match"] = d["age"] == int(p["anchor_age"] + adm.year - p["anchor_year"])
    r["sex_match"] = d["sex"] == ("female" if p["gender"] == "F" else "male")
    tri = b["triage"][0] if b["triage"] else {}
    v = c["patient"]["vitals"]
    if tri and pd.notna(tri.get("heartrate")):
        r["vitals_hr_match"] = v["hr"] == int(tri["heartrate"])
    # radiology: every served findings paragraph is in the source report text
    srcs = " ".join(_N(x["text"]) for x in b["radiology"])
    paras = []
    io = c["initial_tool_outputs"]
    for k in ("ct", "mri", "body_imaging"):
        o = io.get(k) or {}
        paras += [f.get("description") or f.get("finding") or "" for f in o.get("findings", [])] + list(o.get("additional_observations", []))
    for f in c["followup_outputs"]:
        if f["tool_name"] == "order_ct_scan":
            paras += [x["description"] for x in f["output"]["findings"]]
    paras = [x for x in paras if x]
    r["radiology_paragraphs"], r["radiology_paragraphs_verbatim"] = len(paras), sum(_N(x) in srcs for x in paras)
    # omissions (task 04): source sentences of each served report (findings + impression) not served
    from mimic_case_assemble import FINDINGS
    served_txt = _N(json.dumps(io) + json.dumps(c["followup_outputs"]))
    n_src = n_kept = 0
    dropped = []
    for k, meta in c["metadata"]["served"].items():
        if meta.get("origin") != "table" or "radiology" not in str(meta.get("source", "")):
            continue
        names = [x.strip() for x in str(meta.get("exam", "")).split(" + ")]
        for rep in b["radiology"]:
            if rep["exam_name"] not in names:
                continue
            m = re.search(FINDINGS, rep["text"])
            body = (m.group(1) if m else "") + " " + (rep["text"].split("IMPRESSION:")[-1] if "IMPRESSION:" in rep["text"] else "")
            for sent in re.split(r"(?<=[.;])\s+", re.sub(r"\s+", " ", body)):
                t = _N(sent)
                if len(t.split()) < 3:
                    continue
                n_src += 1
                if t in served_txt:
                    n_kept += 1
                else:
                    dropped.append((k, sent.strip()))
            break
    r["rad_source_sentences"], r["rad_sentences_served_verbatim"] = n_src, n_kept
    DROPS[cid] = dropped
    return r


DROPS: dict = {}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--pick", type=int, default=2)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--cases", nargs="*", default=[])
    ap.add_argument("--csv", default="03_reread_auto.csv")
    ap.add_argument("--conditions", nargs="*", default=["ISCH", "SAH", "SE", "GBS", "MS"])
    ap.add_argument("--show")
    ap.add_argument("--show-dropped", action="store_true", help="print dropped source sentences (reader terminal only)")
    ap.add_argument("--tag", default="03")
    a = ap.parse_args()
    TAG[0] = a.tag
    out = Path(a.out)
    if a.show:
        c = json.loads((out / "03_review" / f"{a.show}.md").read_text()) if False else None
        print((out / f"{TAG[0]}_review" / f"{a.show}.md").read_text()[:20000])
        return
    built = sorted(p.stem for p in (out / f"{TAG[0]}_cases").glob("*.json"))
    sel = pd.read_csv(out / f"{TAG[0]}_selection.csv")
    live = set(sel[sel.case_id.notna() & (sel.case_id != "")].case_id)
    built = [x for x in built if x in live]
    pick = a.cases
    if not pick:
        rng = random.Random(a.seed)
        for cond in a.conditions:
            g = [x for x in built if x.split("-")[1] == cond]
            pick += sorted(rng.sample(g, min(a.pick, len(g))))
    rows = [recheck(out, x) for x in pick]
    df = pd.DataFrame(rows)
    df.to_csv(out / a.csv, index=False)
    if a.show_dropped:
        for cid, d in DROPS.items():
            print("#####", cid)
            for k, x in d:
                print(f"  [{k}] {x[:300]}")
    with pd.option_context("display.width", 250):
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
