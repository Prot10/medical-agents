"""Stage ``build`` of ``mimic_build_case.py``: source bundle + manual file -> NeuroBenchCase.

Inputs per case under OUT: ``02_source/<case>.json`` (rows, from ``extract``), ``02_draft/<case>.json``
(note sections, radiology FINDINGS), ``02_manual/<case>.json`` (hand-written: HPI cut as removal
ranges with reasons, admission exam fields and note-extracted study findings as verbatim phrases).
Outputs: ``cases/<case>.json``, ``02_hpi_audit/<case>.json``, ``review/<case>.md``,
``02_build_checks.json`` (validation, verbatim checks, timing, perfect-agent results).

Rules (conservative defaults, task 02):
- labs: first resulted value per item from ED arrival - 1 h to admission + 24 h, rows of another
  admission dropped; radiology: the earliest report of the study in the same window, FINDINGS only;
- note-extracted studies (EEG, ECG, echo, telemetry): findings only, the reader's verbatim phrases;
- every served answer records its origin in ``metadata.served`` (``table`` / ``note_extracted``);
- the policy is transferred from the NeuroBench cases of the condition (``draft``), required steps
  are the condition's core steps, recommended steps the template steps this case serves;
- the case file carries no MIMIC identifier: the case id <-> admission map is ``02_selection.csv``.

No record content in this file (PhysioNet DUA).
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for p in (ROOT / "agent-platform/src", ROOT / "packages/neuroagent-schemas/src", ROOT / "agent-platform/scripts/validation",
          ROOT / "data/review/round-2026-10/bin", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from mimic_case_assemble import anchor, hours, ts  # noqa: E402
from mimic_pilot_cohort import PANELS, step_key  # noqa: E402
from mimic_to_neurobench import ORDER_TOOLS  # noqa: E402

CONDITION_ENUM = {"SE": "status_epilepticus", "ISCH": "ischemic_stroke"}
SYNONYM_CATEGORY = {"SE": "G41", "ISCH": "I63"}
# Core steps (task 01: required in >= 15 of the 30 NeuroBench cases) and the template steps served
# as recommended when this case has a real result for them.
CORE = {"SE": ["eeg", "labs", "ct_head"], "ISCH": ["ct_head", "cta_head_neck", "labs", "ecg"]}
RECOMMENDED = {"SE": ["mri_brain"], "ISCH": ["echo", "cardiac_monitoring"]}
CORE_PANELS = {"SE": ["CBC", "CMP", "magnesium"], "ISCH": ["glucose", "CBC", "coagulation", "creatinine", "troponin"]}

_WS = lambda s: re.sub(r"\s+", " ", s or "").strip()
_NORM = lambda s: re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


# --------------------------------------------------------------------------------------------
# presentation
# --------------------------------------------------------------------------------------------
def cut_hpi(original: str, removals: list[dict]) -> tuple[str, list[dict], list[str]]:
    """Apply removal ranges (verbatim ``from`` .. ``to``, inclusive) to the whitespace-normalised HPI."""
    text = _WS(original)
    spans, errors, pos = [], [], 0
    for r in removals:
        a = text.find(_WS(r["from"]), pos)
        if a < 0:
            a = text.find(_WS(r["from"]))
        if a < 0:
            errors.append(f"HPI removal start not found: {r['from'][:40]!r}")
            continue
        to = _WS(r.get("to") or r["from"])
        b = text.find(to, a)
        if b < 0:
            errors.append(f"HPI removal end not found: {to[:40]!r}")
            continue
        b += len(to)
        spans.append((a, b, r))
        pos = b
    spans.sort()
    kept, removed, last = [], [], 0
    for a, b, r in spans:
        if a < last:
            errors.append(f"HPI removals overlap at {r['from'][:40]!r}")
            continue
        kept.append(text[last:a])
        removed.append({"text": text[a:b], "class": r["class"], "why": r["why"]})
        last = b
    kept.append(text[last:])
    # Repair punctuation at cut boundaries only: a fragment that ends without a full stop before a
    # capitalised continuation gets one (a trailing comma becomes a full stop). Counted, not hidden.
    pieces = [_WS(k) for k in kept if _WS(k)]
    for i in range(len(pieces) - 1):
        if pieces[i + 1][:1].isupper() and not re.search(r"[.!?:]$", pieces[i]):
            pieces[i] = re.sub(r"[,;]$", "", pieces[i]) + "."
            errors.append("note: punctuation repaired at one cut boundary")
    return _WS(" ".join(pieces)), removed, errors


def verbatim(value: str, source: str) -> bool:
    """Every fragment of the reader's value (split on ' | ') occurs in the source."""
    src = _NORM(source)
    return all(_NORM(part) in src for part in value.split(" | ") if _NORM(part))


def body_size(bundle: dict, t_admit) -> dict:
    om = pd.DataFrame(bundle["omr"])
    out = {"weight_kg": None, "height_cm": None, "bmi": None}
    if om.empty:
        return out
    om["d"] = pd.to_datetime(om.chartdate)
    om = om[(om.d <= t_admit.normalize()) & (om.d >= t_admit.normalize() - pd.Timedelta(days=365))]
    for name, key, f in (("Weight (Lbs)", "weight_kg", lambda v: round(v * 0.4536, 1)),
                         ("Height (Inches)", "height_cm", lambda v: round(v * 2.54, 1)),
                         ("BMI (kg/m2)", "bmi", lambda v: round(v, 1))):
        g = om[om.result_name == name].sort_values("d")
        if len(g):
            try:
                v = f(float(g.result_value.iloc[-1]))
            except ValueError:
                continue
            ok = {"weight_kg": 25 < v < 300, "height_cm": 120 < v < 230, "bmi": 10 < v < 80}[key]
            out[key] = v if ok else None
    return out


def vitals(bundle: dict) -> tuple[dict, str]:
    def conv(r):
        num = lambda v, lo, hi: int(v) if pd.notna(v) and lo <= float(v) <= hi else None
        t = r.get("temperature")
        temp = round((float(t) - 32) * 5 / 9, 1) if pd.notna(t) and 90 <= float(t) <= 110 else None
        return {"bp_systolic": num(r.get("sbp"), 50, 300), "bp_diastolic": num(r.get("dbp"), 20, 200),
                "hr": num(r.get("heartrate"), 20, 250), "temp": temp, "rr": num(r.get("resprate"), 4, 60),
                "spo2": num(r.get("o2sat"), 50, 100)}
    tri = bundle["triage"]
    if tri:
        v = conv(tri[0])
        if any(x is not None for x in v.values()):
            return v, "ed/triage"
    rows = sorted(bundle["ed_vitals"], key=lambda r: r["charttime"])
    if rows:
        return conv(rows[0]), "ed/vitalsign (first row; triage vitals blank)"
    return {k: None for k in ("bp_systolic", "bp_diastolic", "hr", "temp", "rr", "spo2")}, "none recorded"


# --------------------------------------------------------------------------------------------
# tool outputs from tables
# --------------------------------------------------------------------------------------------
def lab_rows(bundle: dict, t0, t_end) -> pd.DataFrame:
    labs = pd.DataFrame(bundle["labs"])
    if labs.empty:
        return labs
    labs["t"] = pd.to_datetime(labs.charttime)
    h = bundle["hadm_id"]
    other = labs.hadm_id.notna() & (labs.hadm_id != h)
    labs = labs[~other & (labs.t >= t0) & (labs.t <= t_end)]
    # task 07 round 6: an item whose first draw in the window has no recorded result (value and number both empty) is not served:
    # its next draw would be read as the first value
    first_ = labs.sort_values("t").drop_duplicates("itemid")
    empty_first = set(first_[first_.value.isna() & first_.valuenum.isna()].itemid)
    labs = labs[~labs.itemid.isin(empty_first) & (labs.value.notna() | labs.valuenum.notna())]
    # Not results: hemolysis / icterus / lipemia indices, tube holds, screen line codes, deleted rows.
    junk = labs.label.str.fullmatch(r"H|I|L|[SU]TX\d+|HPE\d+|Delete|Voided Specimen|.*\bHold\b.*|Specimen Type|Problem", case=False, na=False)
    junk |= labs.value.astype(str).str.contains(r"^HOLD|DISCARD", case=False, na=False)
    labs = labs[~junk]
    return labs.sort_values("t").drop_duplicates("itemid")


def lab_value(r) -> dict:
    lo, hi = r.get("ref_range_lower"), r.get("ref_range_upper")
    val = r["valuenum"] if pd.notna(r.get("valuenum")) else str(r["value"])
    return {"test": r["label"], "value": float(val) if not isinstance(val, str) else val,
            "unit": "" if pd.isna(r.get("valueuom")) else str(r["valueuom"]),
            "reference_range": f"{lo:g}-{hi:g}" if pd.notna(lo) and pd.notna(hi) else "",
            "is_abnormal": r.get("flag") == "abnormal"}


def labs_output(first: pd.DataFrame, t_ed) -> tuple[dict | None, dict | None, dict]:
    """Blood (and urine) panels, CSF results, and the serving record."""
    if first.empty:
        return None, None, {}
    blood = first[first.fluid == "Blood"]
    panels: dict[str, list] = {}
    used = set()
    for pname, groups in PANELS.items():
        labels = {x for g in groups for x in g}
        rows = blood[blood.label.isin(labels)]
        if pname == "CBC":  # the whole blood count, as resulted
            rows = blood[(blood.category == "Hematology") & ~blood.label.isin({"PT", "PTT", "INR(PT)"})]
        if len(rows) and all(any(x in set(rows.label) for x in g) for g in groups if pname != "CBC") or (pname == "CBC" and len(rows)):
            rows = rows.sort_values("t").drop_duplicates("label")  # one value per test name, the first
            panels[pname] = [lab_value(r) for _, r in rows.iterrows()]
            used |= set(rows.itemid)
    rest = blood[~blood.itemid.isin(used)]
    # task 07: a test already served in a panel is not served again from another item code (a later draw of the same analyte)
    served_labels = {v["test"] for rows_ in panels.values() for v in rows_}
    rest = rest[~rest.label.isin(served_labels)]
    for cat, g in rest.groupby("category"):
        name = {"Blood Gas": "blood gas", "Chemistry": "other chemistry", "Hematology": "other hematology"}.get(cat, f"other {cat.lower()}")
        panels[name] = [lab_value(r) for _, r in g.iterrows()]
    urine = first[first.fluid == "Urine"]
    if len(urine):
        panels["urinalysis"] = [lab_value(r) for _, r in urine.iterrows()]
    abnormal = list(dict.fromkeys(f"{v['test']} {v['value']} {v['unit']}".strip() for rows in panels.values() for v in rows if v["is_abnormal"]))
    labs = {"panels": panels, "interpretation": "Values as resulted by the laboratory.",
            "abnormal_values_summary": abnormal} if panels else None
    csf = first[first.fluid == "Cerebrospinal Fluid"].copy()
    csf_out = None
    if len(csf):
        # A text value masked by de-identification ("___") with the number kept in valuenum is served
        # from valuenum, as the blood panels are (lab_value); a value with no number is not served.
        masked = csf.value.astype(str).str.fullmatch(r"\s*_{3}\s*", na=False)
        csf.loc[masked & csf.valuenum.notna(), "value"] = csf.loc[masked & csf.valuenum.notna(), "valuenum"].map(lambda v: f"{v:g}")
        csf = csf[~(masked & csf.valuenum.isna())]
        get = lambda rx: "; ".join(f"{r.label} {r.value} {'' if pd.isna(r.valueuom) else r.valueuom}".strip()
                                   for r in csf.itertuples() if re.search(rx, r.label, re.I))
        csf_out = {"appearance": "not recorded", "opening_pressure": "not recorded",
                   "cell_count": {r.label: f"{r.value} {'' if pd.isna(r.valueuom) else r.valueuom}".strip() for r in csf.itertuples()
                                  if re.search(r"WBC|RBC|Nucleated|Polys|Lymphs|Monos|Macroph|Eos|Bands|Basos|Atyp", r.label, re.I)},
                   "protein": get(r"Protein"), "glucose": get(r"Glucose"),
                   "interpretation": "Values as resulted by the laboratory."}
    serving = {"t_first_h": hours(first.t.min(), t_ed), "t_last_h": hours(first.t.max(), t_ed), "items": int(len(first))}
    return labs, csf_out, serving


RAD = {
    "ct_head": r"^(CT HEAD W/O|PORTABLE HEAD CT W/O|ED CODE STROKE ONLY CT|CT BRAIN W/O)",
    "cta_head_neck": r"^CTA (HEAD|NECK)|STROKE CTA|CTA HEAD AND",
    "mri_brain": r"^(MR HEAD|MRI BRAIN|MR BRAIN|STROKE PROTOCOL \(BRAIN)",
    "chest_xray": r"^CHEST \((PA|PORTABLE AP|SINGLE)",
}


def first_report(draft: dict, step: str, t_lo: float, t_hi: float, together_h: float = 0.0) -> list[dict]:
    """Earliest report(s) of a study in [t_lo, t_hi] hours with a FINDINGS section; CTA head and neck
    reports read within ``together_h`` of the first are one study."""
    rows = [r for r in draft["radiology"] if re.search(RAD[step], r["exam"].upper()) and r["findings"]
            and r["t_h"] is not None and t_lo <= r["t_h"] <= t_hi]
    rows.sort(key=lambda r: r["t_h"])
    if not rows:
        return []
    return [r for r in rows if r["t_h"] - rows[0]["t_h"] <= together_h and (together_h or r is rows[0])]


# Findings only, in the strict sense: an interpretive clause appended to an observation ("which may
# reflect subacute infarctions", "consistent with ...", "concerning for ...") is removed, the
# observation kept. Applied to every served radiology sentence; the count is recorded.
_INTERP = re.compile(
    r",?\s*(?:(?:which|that)\s+)?(?:(?:is|are|was|were)\s+)?(?:(?:most\s+)?(?:likely|probably|possibly|may|might|could)\s+)?(?:be\s+)?"
    r"(?:consistent with|compatible with|concerning for|suspicious for|worrisome for|suggestive of|suggesting|"
    r"in keeping with|indicative of|attributable to|secondary to(?!\s+(?:motion|patient motion|artifact|streak|technique|positioning|beam))|"
    r"represent(?:s|ing)?|reflect(?:s|ing)?|relates? to|related to|"
    r"(?:a\s+)?sequela(?:e)? of)\b[^.;]*", re.I)


def strip_interpretation(text: str) -> tuple[str, int]:
    out, n = [], 0
    for sent in re.split(r"(?<=[.;])\s+", text):
        new = _INTERP.sub("", sent)
        if new != sent:
            n += 1
            # Drop the words a cut clause leaves dangling at the end ("..., which are nonspecific, but",
            # "... and these"), one at a time.
            new = new.rstrip(" .;,")
            tail = re.compile(r"(?:[\s,]+)(?:and|but|though|while|these|this|they|it|which|that|is|are|was|were|non-?specific)$", re.I)
            while tail.search(new):
                new = tail.sub("", new).rstrip(" ,")
            new += "."
        out.append(new)
    return " ".join(out), n


def paragraphs(text: str) -> list[str]:
    return [_WS(p) for p in re.split(r"\n\s*\n", text) if _WS(p)]


def drop_sentences(text: str, drops: list[str]) -> tuple[str, int]:
    """Remove the reader's sentences (verbatim, whitespace-insensitive) from a served report."""
    n = 0
    for d in drops:
        pat = r"\s+".join(map(re.escape, d.split()))
        text, k = re.subn(pat, "", text)
        n += k
    return text, n


def ct_output(reports: list[dict], angiography: bool) -> dict:
    # Head and neck CTA are often one report filed under both exam names: serve it once, labelled
    # with every exam name it was filed under.
    seen: dict[str, dict] = {}
    for r in reports:
        k = _WS(r["findings"])
        if k in seen:
            seen[k] = {**seen[k], "exam": seen[k]["exam"] + " + " + r["exam"]}
        else:
            seen[k] = dict(r)
    reports = list(seen.values())
    findings = [{"type": "report findings", "location": r["exam"], "description": p}
                for r in reports for p in paragraphs(r["findings"])]
    out = {"findings": findings, "contrast_used": angiography, "additional_observations": [], "impression": "",
           "recommended_actions": []}
    if angiography:
        out["angiography_findings"] = {r["exam"]: _WS(r["findings"]) for r in reports}
    return out


def mri_output(report: dict) -> dict:
    contrast = bool(re.search(r"W ?& ?W/O|W/ CONTRAST|WITH CONTRAST", report["exam"].upper()))
    # A combined MR head + MRA report: the MRA paragraphs answer a different order, not this one.
    paras, mra = [], False
    for p in paragraphs(report["findings"]):
        if re.match(r"(?i)MRA\b", p):
            mra = True
        elif re.match(r"(?i)MR(I)? (head|brain)\b", p):
            mra = False
        if not mra:
            paras.append(p)
    return {"contrast_used": contrast, "findings": [], "additional_observations": paras,
            "impression": "", "recommended_actions": []}


# --------------------------------------------------------------------------------------------
# policy
# --------------------------------------------------------------------------------------------
STEP_PATTERN = {
    "eeg": [{"tool_name": "analyze_eeg", "required_arguments": {"eeg_type": "continuous_icu"}},
            {"tool_name": "analyze_eeg", "required_arguments": {"eeg_type": "video"}}],
    "ct_head": None, "cta_head_neck": None, "labs": None, "ecg": None, "mri_brain": None, "echo": None,
    "cardiac_monitoring": None,
}


def template_criterion(cases_dir: Path, cond: str, step: str) -> tuple[dict, int]:
    """The most frequent criterion of a step among the condition's NeuroBench cases (by its first
    pattern), and how many cases carry it."""
    seen, example = collections.Counter(), {}
    prefix = f"{cond}-"
    for f in sorted(cases_dir.glob(f"{prefix}*.json")):
        for c in json.loads(f.read_text())["ground_truth"]["action_criteria"]:
            if step_key(c["alternatives"][0]) != step:
                continue
            key = json.dumps(c["alternatives"][0], sort_keys=True)
            seen[key] += 1
            example.setdefault(key, c)
    if not seen:
        raise KeyError(step)
    key, n = seen.most_common(1)[0]
    return example[key], n


def build_policy(cond: str, served_steps: set[str], cases_dir: Path, dx: dict, outputs: dict | None = None) -> tuple[dict, dict]:
    criteria, provenance = [], {}
    order = CORE[cond] + [s for s in RECOMMENDED[cond] if s in served_steps]
    for i, step in enumerate(order, start=1):
        tmpl, n = template_criterion(cases_dir, cond, step)
        alts = STEP_PATTERN.get(step) or [tmpl["alternatives"][0]]
        if step == "labs":
            alts = [{"tool_name": "interpret_labs", "required_arguments": {"panels": CORE_PANELS[cond]}}]
        if step == "cardiac_monitoring":
            alts = [{"tool_name": "order_cardiac_monitoring", "required_arguments": {"monitor_type": "telemetry"}}]
        if step == "mri_brain":
            # The study the case holds: a contrast report answers only a contrast order (MockServer).
            alts = [{"tool_name": "analyze_brain_mri", "required_arguments": {"contrast": bool((outputs or {}).get("mri", {}).get("contrast_used"))}}]
        if step == "echo":
            alts = [{"tool_name": "order_echocardiogram", "required_arguments": {"echo_type": "TTE"}}]
        cid = f"action-{i}-{alts[0]['tool_name'].replace('_', '-')}"
        importance = "required" if step in CORE[cond] else "recommended"
        criteria.append({"criterion_id": cid, "label": tmpl["label"], "importance": importance, "alternatives": alts,
                         "expected_evidence": "", "rationale": tmpl.get("rationale", ""), "citations": tmpl.get("citations", [])})
        provenance[cid] = {"step": step, "template_pattern_cases": n}
    ids = {provenance[c["criterion_id"]]["step"]: c["criterion_id"] for c in criteria}
    seq = []
    if cond == "ISCH":
        seq.append({"before_criterion_id": ids["ct_head"], "after_criterion_id": ids["cta_head_neck"],
                    "reason": "The non-contrast CT precedes the CT angiogram (transferred from the NeuroBench ISCH policy).",
                    "citations": [], "severity": "soft"})
    gt = {"review_status": "draft", "diagnosis": dx, "differential": [], "action_criteria": criteria,
          "avoided_actions": [], "sequence_constraints": seq,
          "stop_rule": {"required_before_assessment": [c["criterion_id"] for c in criteria if c["importance"] == "required"],
                        "max_additional_actions": 1},
          "assessment": {"required_recommendations": [], "prohibited_recommendations": []},
          "key_clinical_evidence": [], "red_herrings": []}
    return gt, provenance


def diagnosis(cond: str, bundle: dict) -> tuple[dict, dict]:
    from apply_diagnosis_synonyms import entries_for
    table = yaml.safe_load((ROOT / "agent-platform/config/policies/diagnosis_synonyms.yaml").read_text())
    table.pop("RETIRED", None)
    p = bundle["diagnoses"][0]
    code = str(p["icd_code"])
    v10 = int(p["icd_version"]) == 10
    dotted = f"{code[:3]}.{code[3:]}" if v10 and len(code) > 3 else code
    labels, codes = [], []
    for key in ([dotted] if v10 else []) + [SYNONYM_CATEGORY[cond]]:
        for e in entries_for(key, CONDITION_ENUM[cond], table):
            if e.get("cases"):
                continue
            labels += [x for x in e.get("labels", []) if x not in labels]
            codes += [x for x in e.get("codes", []) if x not in codes]
    if v10:
        codes = [dotted] + [c for c in codes if c != dotted]
    dx = {"accepted": labels, "icd_codes": codes, "rejected": [], "required_components": []}
    info = {"principal_icd": f"ICD-{p['icd_version']} {code}", "principal_title": p.get("long_title", ""),
            "synonym_keys": ([dotted] if v10 else []) + [SYNONYM_CATEGORY[cond]]}
    return dx, info


# --------------------------------------------------------------------------------------------
# reference trajectory
# --------------------------------------------------------------------------------------------
def trajectory(bundle: dict, t_ed, horizon_h: float = 72.0) -> list[dict]:
    ev = []
    for o in bundle["poe"]:
        tool = ORDER_TOOLS.get((o["order_type"], o["order_subtype"])) or ORDER_TOOLS.get((o["order_type"], None))
        if not tool:
            continue
        t = hours(o["ordertime"], t_ed)
        if t is None or t > horizon_h:
            continue
        ev.append({"t_hours": t, "kind": "order (poe)", "tool": tool, "what": f"{o['order_type']}/{o['order_subtype'] or ''}".rstrip("/")})
    for r in bundle["radiology"]:
        t = hours(r["charttime"], t_ed)
        if t is not None and t <= horizon_h and not str(r["exam_name"]).startswith(("-", "___")):
            ev.append({"t_hours": t, "kind": "study read (radiology)", "tool": "", "what": r["exam_name"]})
    for m in bundle["ed_pyxis"]:
        t = hours(m["charttime"], t_ed)
        if t is not None:
            ev.append({"t_hours": t, "kind": "ED medication (pyxis)", "tool": "", "what": m["name"]})
    ev.sort(key=lambda e: e["t_hours"])
    # Lab orders come in bursts: keep the first of each tool within the same hour.
    out, last = [], {}
    for e in ev:
        k = (e["kind"], e["tool"] or e["what"])
        if k in last and e["t_hours"] - last[k] < 1.0 and (e["tool"] == "interpret_labs" or e["kind"].startswith("ED medication")):
            continue
        last[k] = e["t_hours"]
        out.append(e)
    return out


# --------------------------------------------------------------------------------------------
# build one case
# --------------------------------------------------------------------------------------------
def build_case(cid: str, cond: str, out: Path, cases_dir: Path) -> tuple[dict, dict, list[str]]:
    bundle = json.loads((out / "02_source" / f"{cid}.json").read_text())
    draft = json.loads((out / "02_draft" / f"{cid}.json").read_text())
    man = json.loads((out / "02_manual" / f"{cid}.json").read_text())
    errors: list[str] = []
    for d in man.get("radiology_drop_sentences", []):
        hits = 0
        for r in draft["radiology"]:
            if re.search(RAD[d["study"]], r["exam"].upper()):
                r["findings"], k = drop_sentences(r["findings"], [d["sentence"]])
                hits += k
        if not hits:
            errors.append(f"radiology drop not found: {d['sentence'][:40]!r}")
    interp_removed = 0
    for r in draft["radiology"]:
        if r["findings"]:
            paras = []
            for p in re.split(r"\n\s*\n", r["findings"]):
                q, k = strip_interpretation(_WS(p))
                interp_removed += k
                paras.append(q)
            r["findings"] = "\n\n".join(paras)
    note = bundle["discharge"][0]["text"]
    sec = draft["sections"]
    t_ed = anchor(bundle)
    adm = bundle["admission"][0]
    t_admit = ts(adm["admittime"])
    t0, t_lab_end = t_ed - pd.Timedelta(hours=1), t_admit + pd.Timedelta(hours=24)
    lab_end_h = hours(t_lab_end, t_ed)

    # --- presentation ---
    hpi, removed, err = cut_hpi(sec.get("History of Present Illness", ""), man["hpi_removals"])
    repairs = sum(e.startswith("note: punctuation") for e in err)
    errors += [e for e in err if not e.startswith("note:")]
    pat = bundle["patient"][0]
    age = int(pat["anchor_age"] + t_admit.year - pat["anchor_year"])
    size = body_size(bundle, t_admit)
    vit, vit_src = vitals(bundle)
    cc = (bundle["triage"][0].get("chiefcomplaint") if bundle["triage"] else None) or ""
    cc_src = "ed/triage"
    if man.get("chief_complaint_override"):
        cc, cc_src = man["chief_complaint_override"]["text"], man["chief_complaint_override"]["source"]
    exam_src = draft["admission_exam"]
    for field, value in {**man["neurological_exam"], **man.get("physical_exam", {})}.items():
        if value and not verbatim(value, exam_src):
            errors.append(f"exam field {field!r} is not verbatim from the admission exam")
    for item in man["past_medical_history"]:
        if not verbatim(item, sec.get("Past Medical History", "")):
            errors.append(f"PMH item not verbatim: {item[:40]!r}")
    meds = man.get("medications")
    meds_src = "note: Medications on Admission (parsed)"
    if meds is None:
        meds = draft["medications"]
    if not meds and bundle["ed_medrecon"]:
        meds = [{"drug": m["name"], "dose": "", "frequency": "", "indication": ""} for m in bundle["ed_medrecon"]]
        meds_src = "ed/medrecon (names only)"
    if not meds:
        meds_src = "none recorded"
    patient = {
        "patient_id": cid,
        "demographics": {"age": age, "sex": "female" if pat["gender"] == "F" else "male",
                         "handedness": man.get("handedness", ""), "ethnicity": str(adm.get("race") or "").title(), **size},
        "clinical_history": {"past_medical_history": man["past_medical_history"], "medications": meds,
                             "allergies": man["allergies"], "family_history": man["family_history"],
                             "social_history": man.get("social_history", {})},
        "neurological_exam": man["neurological_exam"], "physical_exam": man.get("physical_exam", {}),
        "vitals": vit, "chief_complaint": cc, "history_present_illness": hpi,
    }

    # --- tool outputs ---
    served: dict[str, dict] = {}
    first = lab_rows(bundle, t0, t_lab_end)
    labs, csf, lab_serving = labs_output(first, t_ed)
    outputs: dict = {}
    if labs:
        outputs["labs"] = labs
        served["labs"] = {"origin": "table", "source": "hosp/labevents (first value per item)", **lab_serving}
    # CSF over the whole stay (first sample).
    all_labs = pd.DataFrame(bundle["labs"])
    if len(all_labs):
        all_labs["t"] = pd.to_datetime(all_labs.charttime)
        c = all_labs[(all_labs.fluid == "Cerebrospinal Fluid") & ~(all_labs.hadm_id.notna() & (all_labs.hadm_id != bundle["hadm_id"]))]
        if len(c):
            c = c[c.t <= c.t.min() + pd.Timedelta(hours=1)].drop_duplicates("itemid")
            _, csf, _ = labs_output(c, t_ed)
            outputs["csf"] = csf
            served["csf"] = {"origin": "table", "source": "hosp/labevents fluid Cerebrospinal Fluid (first sample)",
                             "t_first_h": hours(c.t.min(), t_ed)}
    window = (-1.0, lab_end_h)
    ct = first_report(draft, "ct_head", *window)
    if ct:
        outputs["ct"] = ct_output(ct, angiography=False)
        served["ct"] = {"origin": "table", "source": "note/radiology FINDINGS", "exam": ct[0]["exam"], "t_h": ct[0]["t_h"]}
    followups = []
    if cond == "ISCH":
        cta = first_report(draft, "cta_head_neck", *window, together_h=3.0)
        if cta:
            followups.append({"trigger_action": "request_ct_angiography", "tool_name": "order_ct_scan",
                              "output": ct_output(cta, angiography=True)})
            served["ct_angiography"] = {"origin": "table", "source": "note/radiology FINDINGS",
                                        "exam": " + ".join(r["exam"] for r in cta), "t_h": cta[0]["t_h"]}
    mri = first_report(draft, "mri_brain", -1.0, draft["t_disch_h"])
    if mri:
        outputs["mri"] = mri_output(mri[0])
        served["mri"] = {"origin": "table", "source": "note/radiology FINDINGS", "exam": mri[0]["exam"], "t_h": mri[0]["t_h"]}
    for key, schema_key in (("eeg", "eeg"), ("ecg", "ecg"), ("echo", "echo"), ("telemetry", "cardiac_monitoring")):
        x = man.get(key)
        if not x:
            continue
        src = x.pop("_verbatim_source", None)
        for phrase in x.pop("_verbatim", []):
            if not verbatim(phrase, note):
                errors.append(f"{key}: phrase not verbatim in the note: {phrase[:40]!r}")
        outputs[schema_key] = x
        served[schema_key] = {"origin": "note_extracted", "source": src or "discharge note"}

    # --- policy and diagnosis ---
    served_steps = {"eeg": "eeg" in outputs, "labs": "labs" in outputs, "ct_head": "ct" in outputs,
                    "cta_head_neck": bool(followups), "ecg": "ecg" in outputs, "mri_brain": "mri" in outputs,
                    "echo": "echo" in outputs, "cardiac_monitoring": "cardiac_monitoring" in outputs}
    for step in CORE[cond]:
        if not served_steps[step]:
            errors.append(f"core step {step} has no served result")
    dx, dx_info = diagnosis(cond, bundle)
    gt, policy_prov = build_policy(cond, {k for k, v in served_steps.items() if v}, cases_dir, dx, outputs)

    case = {
        "schema_version": "2.0", "case_id": cid, "domain": "neurology", "provenance": "record",
        "condition": CONDITION_ENUM[cond], "difficulty": "moderate", "encounter_type": "emergency",
        "patient": patient, "initial_tool_outputs": outputs, "followup_outputs": followups,
        "ground_truth": gt,
        "metadata": {
            "source": "MIMIC-IV 3.1 + MIMIC-IV-ED 2.2 + MIMIC-IV-Note 2.2 (credentialed; id map in 02_selection.csv)",
            "builder": "mimic_build_case.py (task 02 pilot)",
            "served": served, "presentation_sources": {"chief_complaint": cc_src, "vitals": vit_src,
                                                       "medications": meds_src, "history_present_illness": "note HPI, cut by the reader (02_hpi_audit)",
                                                       "exam": "note admission exam, fields by the reader (verbatim)"},
            "policy": {"status": "draft", "transferred_from": f"NeuroBench {cond} cases", "criteria": policy_prov},
            "diagnosis_source": {**dx_info, "discharge_diagnosis": _WS(sec.get("Discharge Diagnosis", ""))},
            "reference_trajectory": trajectory(bundle, t_ed),
            "timing_hours_from_ed_arrival": {"admission": draft["t_admit_h"], "discharge": draft["t_disch_h"],
                                             "lab_window_end": lab_end_h},
            "difficulty_note": "not graded for recorded cases; 'moderate' is a placeholder",
            "radiology_interpretive_clauses_removed_all_reports": interp_removed,
        },
    }
    audit = {"case_id": cid, "hpi_original": _WS(sec.get("History of Present Illness", "")), "hpi_kept": hpi,
             "removed": removed, "removed_counts": dict(collections.Counter(r["class"] for r in removed)),
             "exam_notes": man.get("exam_notes", []),
             "other_edits": man.get("other_edits", []) + ([f"punctuation repaired at {repairs} cut boundaries"] if repairs else [])}
    return case, audit, errors


def build_all(a) -> None:
    from neuroagent_schemas import NeuroBenchCase
    out = Path(a.out)
    sel = pd.read_csv(out / "02_selection.csv")
    sel = sel[sel.case_id.notna() & (sel.case_id != "")]
    if a.cases_only:
        sel = sel[sel.case_id.isin(a.cases_only)]
    for d in ("cases", "02_hpi_audit", "review"):
        (out / d).mkdir(exist_ok=True)
    checks_path = out / "02_build_checks.json"
    checks = json.loads(checks_path.read_text()) if checks_path.exists() else {}
    for r in sel.itertuples():
        if not (out / "02_manual" / f"{r.case_id}.json").exists():
            print(f"{r.case_id}: no manual file yet", file=sys.stderr)
            continue
        case, audit, errors = build_case(r.case_id, r.condition, out, Path(a.cases))
        try:
            NeuroBenchCase.model_validate(case)
            valid = "ok"
        except Exception as exc:  # pydantic ValidationError
            valid = f"INVALID: {exc}"
        (out / "cases" / f"{r.case_id}.json").write_text(json.dumps(case, indent=1, default=str))
        (out / "02_hpi_audit" / f"{r.case_id}.json").write_text(json.dumps(audit, indent=1))
        pa_err, pa_warn = perfect_agent(out / "cases", r.case_id) if valid == "ok" else (["not run: invalid"], [])
        checks[r.case_id] = {"schema": valid, "build_errors": errors, "perfect_agent_errors": pa_err,
                             "perfect_agent_warnings": pa_warn}
        from mimic_case_review import review_md
        (out / "review" / f"{r.case_id}.md").write_text(review_md(case, audit))
        print(f"{r.case_id}: schema {valid[:60]}; build errors {len(errors)}; perfect agent "
              f"{'ok' if not pa_err else 'FAIL ' + str(len(pa_err))}", file=sys.stderr)
        for e in errors + pa_err:
            print(f"    {e}", file=sys.stderr)
    checks_path.write_text(json.dumps(checks, indent=1))


def perfect_agent(cases_dir: Path, cid: str) -> tuple[list[str], list[str]]:
    """The repository's perfect-agent check (data/review/round-2026-10/bin/perfect_agent.py) on a case dir."""
    import perfect_agent as pa
    pa.CASES = cases_dir
    return pa.check(cid)
