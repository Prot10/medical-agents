"""Task 06 builder: the task-04 case (mimic_case_build3.build_case3, decisions 1-29) plus decisions
30-41 and the completeness layer (serve every study the record holds up to the decision point).
No record content in this file (PhysioNet DUA).

Decision point (task 06): admission + 48 h for the extra studies (ECG, imaging, serial labs,
microbiology), the window already used for rhythm records; the policy-relevant first studies of the
stay (first MRI, spine MRI, CSF, EEG, EMG) keep the task-04 rule. Studies after admission + 24 h go
through the later-study treatment filter.

    ~/projects/medical-agents/.venv/bin/python -I mimic_case_build6.py --out $W/out --selection 06_selection.csv [--cases-only ...]
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mimic_case_build3 as B  # noqa: E402
from mimic_case_assemble import anchor, hours, ts  # noqa: E402
from mimic_case_build import labs_output  # noqa: E402
from mimic_pilot_v3 import CTA_EXAM, MRI_EXAM, NCCT_EXAM, SPINE_MRI_EXAM  # noqa: E402

B.OPTS.update({"treatments": "06_treatments.parquet", "eeg_strip_treatment": False, "grid_mode": "cells",
               "synonyms_overlay": "/eos/user/a/aprotani/physionet/work/mimic-neuro/out/07_synonyms_overlay.yaml"})
# new conditions (task 06): NeuroBench condition names and the synonym-file keys of their codes
B.CONDITION_ENUM.update({"SYNC": "syncope_cardiac", "FND": "functional_neurological_disorder", "HEP": "hepatic_encephalopathy",
                         "BACT": "bacterial_meningitis", "GLIO": "brain_tumor_glioma"})
B.SYNONYM_CATEGORY.update({"SYNC": "I44", "FND": "F44", "HEP": "K72", "BACT": "G00", "GLIO": "C71"})
B.ICD9_TO10.update({"SYNC": "R55", "FND": "F44.4", "HEP": "K72.90", "BACT": "G00.9", "GLIO": "C71.9"})
for c in ("SYNC", "FND", "HEP", "BACT", "GLIO"):
    B.RECOMMENDED.setdefault(c, [])
EXTRA_H = 48.0
C6 = collections.Counter()
ERRORS6: list[str] = []


# --- policy patterns of the new conditions' steps ------------------------------------------------
MAN_CURRENT: dict = {}
_orig_pattern_for = B.pattern_for


def pattern_for6(step, tmpl, outputs, followups, panels):
    if step == "perform_clinical_assessment":
        kind = (MAN_CURRENT.get("clinical_assessment") or {}).get("assessment_type") or \
            tmpl["alternatives"][0]["required_arguments"].get("assessment_type", "")
        return [{"tool_name": "perform_clinical_assessment", "required_arguments": {"assessment_type": kind}}]
    if step == "obtain_tissue_diagnosis":
        proc = (MAN_CURRENT.get("tissue_diagnosis") or {}).get("procedure") or "resection"
        # adapted: the record states the procedure; the molecular assays of the template are not required
        return [{"tool_name": "obtain_tissue_diagnosis", "required_arguments": {"procedure": proc}}]
    if step.startswith("micro:"):
        return [{"tool_name": "order_microbiology", "required_arguments": {"specimen": step.split(":", 1)[1]}}]
    return _orig_pattern_for(step, tmpl, outputs, followups, panels)


B.pattern_for = pattern_for6


# --- decision 35: exam grids, cell by cell ------------------------------------------------------
_GRADE = re.compile(r"^(?:\d(?:[+-]|\+/-)?\*{0,2}|\d-\d|___-?|NT|tr|0|\d\*|\*{1,2})$")  # task 07: a lone footnote mark is a cell


_HDR = re.compile(r"^(?:[\[(]?[A-Z][A-Za-z/]{0,8}\.?[\])]?|\[?___\]?|[A-Z]{1,3}\d?)$")
_SIDE = re.compile(r"^(?:L|R|Left|Right|LUE|RUE|LLE|RLE|Lt|Rt)$")


def grid_cells(value: str) -> tuple[str, int]:
    """Decision 35: an exam grid (a header run of muscle or reflex names followed by side rows of grades)
    is served row by row as 'Side: name grade, ...', leaving out only the blanked cells and a column whose
    name is blanked. When a row does not align with the header (de-identification removed tokens), only the
    cells before its first blank are attributable and are served (counted); a grid with no blank stays as written."""
    toks = re.sub(r"(?<=\d\+)(?=\d)|(?<=\*)(?=\d)", " ", value or "").split()  # task 07: grades glued by the source ("4+*4*")
    out, i, n = [], 0, 0
    while i < len(toks):
        j = i
        while j < len(toks) and (toks[j] == "|" or _HDR.match(toks[j]) or (j > i and re.fullmatch(r"[a-z]{2,10}", toks[j]) and _HDR.match(toks[j - 1])
                                                                             and toks[j] not in ("and", "or", "the", "with", "of", "in", "to", "is", "was"))) \
                and not _SIDE.match(toks[j]):
            j += 1  # task 07 round 6: two-word column names ("Pec jerk") belong to the header
        last_word = max([q for q in range(i, j) if toks[q] != "|"], default=i)
        bars = [q for q in range(i, last_word) if toks[q] == "|"]
        if bars and j < len(toks) and _SIDE.match(toks[j]):  # task 07 round 7: the header is the run after the last separator
            out += toks[i:bars[-1] + 1]
            i = bars[-1] + 1
        hdr = [t for t in toks[i:j] if t != "|"]
        rows, k = [], j
        while k < len(toks) and _SIDE.match(toks[k]):
            m = k + 1
            vals = []
            while m < len(toks) and (toks[m] == "|" or _GRADE.match(toks[m])):
                if toks[m] != "|":
                    vals.append(toks[m])
                m += 1
            if not vals:
                break
            rows.append((toks[k], vals))
            k = m
        hdr = [h.strip("[]()") or h for h in hdr]
        if len(hdr) >= 4 and rows and all(h == "___" for h in hdr):  # a fully blanked header: no cell is attributable (decision 45)
            C6["grid_dropped_blank_header"] += 1
            n += 1
            i = k
            continue
        if len(hdr) >= 4 and rows:
            blank = "___" in hdr or any(v.startswith("___") for _, vs in rows for v in vs)
            if hdr[-1] == "___" and all(len(vs) == len(hdr) - 1 and not any(v.startswith("___") for v in vs) for _, vs in rows):
                hdr = hdr[:-1]  # a trailing blanked header with no column under it
                C6["grid_trailing_blank_header_dropped"] += 1
            if not blank and not all(len(vs) == len(hdr) for _, vs in rows):
                out += toks[i:k] + ["|"]  # no blank: the grid stays as written
                i = k
                continue
            aligned = all(len(vs) == len(hdr) for _, vs in rows)  # task 07: position is trusted only in a grid whose rows all fit the header
            for side, vs in rows:
                if len(vs) == len(hdr) and (aligned or not any(v.startswith("___") for v in vs)):
                    cells = [f"{h} {v}" for h, v in zip(hdr, vs) if h != "___" and not v.startswith("___")]
                    C6["grid_cells_dropped"] += len(vs) - len(cells)
                    C6["grid_rows_served"] += 1
                    out += ["|", f"{side}: " + ", ".join(cells)]
                    continue
                # a row that de-identification shortened: the cells before the first blank are still attributable
                cells = []
                if not any(v.startswith("___") for v in vs):
                    vs_ = []  # task 07: shorter than the header with no blank of its own: the missing cell may be anywhere
                else:
                    vs_ = vs
                for h, v in zip(hdr, vs_):
                    if h == "___" or v.startswith("___"):
                        break
                    cells.append(f"{h} {v}")
                if cells:
                    C6["grid_rows_prefix_served"] += 1
                    C6["grid_cells_not_attributable"] += len(vs) - len(cells)
                    out += ["|", f"{side}: " + ", ".join(cells) + " (remaining cells not attributable)"]
                else:
                    C6["grid_rows_not_attributable"] += 1
                    n += 1
                    B.DROPPED.append("[grid row not attributable] " + side + " " + " ".join(vs)[:60])
            out.append("|")
            i = k
            continue
        out.append(toks[i])
        i += 1
    txt = re.sub(r"(?:\s*\|\s*)+", " | ", " ".join(out)).strip(" |")
    return txt, n


B.GRID_CELLS = grid_cells


# --- record studies ------------------------------------------------------------------------------
BODY = [  # (exam regex, tool, study / modality, region, trigger)
    (r"^CHEST \(|^CHEST PORT|^CHEST \(PORTABLE|^CHEST X|^PORTABLE CHEST", "order_body_imaging", "chest_xray", ("chest", "X-ray"), "request_chest_xray"),
    (r"^CTA CHEST", "order_body_imaging", "chest_CTA", ("chest", "CT"), "request_chest_cta"),
    (r"^CT CHEST", "order_body_imaging", "chest_CT", ("chest", "CT"), "request_chest_ct"),
    (r"^CT (?:ABD|ABDOMEN|PELVIS|A/P)", "order_body_imaging", "pelvis_abdomen_CT", ("pelvis_abdomen", "CT"), "request_abdomen_pelvis_ct"),
    (r"^(?:US|ULTRASOUND).*(?:ABD|PELVI|LIVER|RENAL|RUQ)|^LIVER OR GALLBLADDER US|^RENAL U\.?S", "order_body_imaging", "pelvis_abdomen_ultrasound",
     ("pelvis_abdomen", "ultrasound"), "request_abdominal_ultrasound"),
    (r"^CT (?:C|T|L)[- ]SPINE|^CT (?:CERVICAL|THORACIC|LUMBAR)", "order_body_imaging", "spine_CT", ("spine", "CT"), "request_spine_ct"),
    (r"^(?:UNILAT|BILAT).*(?:LOWER EXT|LOW EXT).*VEIN|LOWER EXTREMITY VEINS|VENOUS DUP", "order_body_imaging", "lower_extremity_venous_duplex",
     ("lower_extremity", "ultrasound"), "request_venous_duplex"),
    (r"^CAROTID", "order_advanced_imaging", "carotid_duplex", None, "request_carotid_duplex"),
    (r"PERFUSION|^CTP\b", "order_advanced_imaging", "CT_perfusion", None, "request_ct_perfusion"),
    (r"^MRA |MR ANGIO", "order_advanced_imaging", "MR_angiography", None, "request_mr_angiography"),
    (r"^MRV |MR VENO", "order_advanced_imaging", "MR_venography", None, "request_mr_venography"),
]


def clean(t: str, later: bool) -> str:
    t, _ = B.drop_ambiguous(t)
    return B.drop_value_blanks(t)


def rad_output(r: dict, tool: str, study: str, region, later: bool) -> dict:
    f, imp, _, _ = B.report_text(r, later=later)
    f, imp = clean(f, later), clean(imp, later)
    paras = [p for p in re.split(r"\n\s*\n", f) if p.strip()]
    if tool == "order_advanced_imaging":
        return {"modality": study, "tracer_or_protocol": None, "findings": [{"region": r["exam_name"], "finding": p} for p in paras],
                "impression": imp, "recommended_actions": []}
    if tool == "order_body_imaging":
        return {"region": region[0], "modality": region[1], "contrast": bool(re.search(r"W/ ?C|W/ |W&|W &|WITH CONTRAST|CTA", r["exam_name"].upper())),
                "findings": [{"finding": p, "location": r["exam_name"]} for p in paras], "impression": imp, "recommended_actions": []}
    if tool == "order_ct_scan":
        return B.ct_report(f, imp, r["exam_name"], bool(re.search(r"W/ CONTRAST|W&W|CTA", r["exam_name"].upper())))
    if tool == "analyze_brain_mri":
        return {"contrast_used": bool(re.search(r"W ?& ?W/O|W/ CONTRAST|WITH CONTRAST", r["exam_name"].upper())), "findings": [],
                "additional_observations": paras, "impression": imp, "recommended_actions": []}
    raise KeyError(tool)


def ecg_row(r: dict) -> dict | None:
    lines = [str(r[f"report_{i}"]).strip() for i in range(18) if r.get(f"report_{i}") not in (None, "") and str(r.get(f"report_{i}")) != "nan"]
    lines = [x for x in lines if not re.search(r"(?i)age not entered|assumed to be|for purpose of ecg interpretation|technically (?:limited|difficult)|"
                                               r"unconfirmed|analysis error|no further analysis attempted", x)] or lines
    ok = lambda v: v is not None and str(v) != "nan" and float(v) < 29999 and float(v) not in (999.0, -999.0)
    if not lines or not ok(r.get("rr_interval")) or float(r["rr_interval"]) <= 0:
        return None
    iv = {}
    for name, a, b in (("PR", "p_onset", "qrs_onset"), ("QRS", "qrs_onset", "qrs_end"), ("QT", "qrs_onset", "t_end")):
        if ok(r.get(a)) and ok(r.get(b)) and float(r[b]) > float(r[a]):
            d_ = float(r[b]) - float(r[a])
            if (name == "PR" and not 80 <= d_ <= 400) or (name == "QRS" and not 40 <= d_ <= 250) or (name == "QT" and not 200 <= d_ <= 700):
                continue  # task 07: an implausible machine interval is not served
            iv[name] = f"{d_:.0f} ms"
    if re.search(r"(?i)atrial (?:fibrillation|flutter)|\bafib\b", " ".join(lines)):
        iv.pop("PR", None)  # task 07: no PR interval (and no P axis) on a tracing read as atrial fibrillation or flutter
    axis = ", ".join(f"{k} {int(float(r[c]))}" for k, c in (("P", "p_axis"), ("QRS", "qrs_axis"), ("T", "t_axis")) if ok(r.get(c))
                     and not (k == "P" and re.search(r"(?i)atrial (?:fibrillation|flutter)|\bafib\b", " ".join(lines))))
    overall = [x for x in lines if re.search(r"(?i)\b(normal|abnormal|borderline|otherwise normal)\s+ecg\b", x)]
    return {"rhythm": lines[0], "rate": int(round(60000 / float(r["rr_interval"]))), "intervals": iv, "axis": axis,
            "findings": [x for x in lines[1:] if x not in overall], "interpretation": " ".join(overall)}


SPEC = {"BLOOD CULTURE": "blood_culture", "URINE": "urine", "SPUTUM": "sputum", "STOOL": "stool", "PERITONEAL FLUID": "ascitic_fluid",
        "SWAB": "wound_swab", "THROAT": "throat_swab", "BRONCHOALVEOLAR LAVAGE": "tracheal_aspirate", "TRACHEAL ASPIRATE": "tracheal_aspirate"}


def _test_result(g: pd.DataFrame) -> str:
    """The result of one test of a specimen: its organisms, else its own comment (growth or a stain), else no organism."""
    orgs = sorted({str(x) for x in g.org_name.dropna() if str(x) not in ("", "nan", "CANCELLED")})
    if orgs:
        return "; ".join(orgs)
    com = [B._WS(str(x)) for x in g.comments.dropna()] if "comments" in g else []
    com = list(dict.fromkeys(c for c in com if c and "___" not in c))
    if com:
        return com[0]
    return "Result text not available." if "comments" in g and g.comments.notna().any() else "no organism reported"


def _fluid_counts(bundle: dict, t, fluid: str, window_h: float = 6.0) -> dict | None:
    """Cell counts and chemistry of the same body fluid drawn within a few hours of the specimen (labevents)."""
    L = [l for l in bundle.get("labs", []) if l.get("fluid") == fluid and l.get("charttime")]
    out = {}
    for l in sorted(L, key=lambda l: l["charttime"]):
        dt = abs((pd.Timestamp(l["charttime"]) - t).total_seconds()) / 3600
        if dt > window_h or l["label"] in out:
            continue
        v = l.get("valuenum") if l.get("valuenum") not in (None, "") and not pd.isna(l.get("valuenum")) else l.get("value")
        if v in (None, "") or "___" in str(v) or str(v).strip().lower() == "nan":
            continue
        out[l["label"]] = f"{v} {l.get('valueuom') or ''}".strip()
    return out or None


def ascitic_first_tap(bundle: dict, mic: list, t0) -> tuple | None:
    """The admission paracentesis when its fluid labs precede the first ascitic culture by more than 6 h (task 07):
    the first ascitic result of the stay, served with the counts and no culture."""
    L = sorted(pd.Timestamp(l["charttime"]) for l in bundle.get("labs", []) if l.get("fluid") == "Ascites" and l.get("charttime")
               and pd.Timestamp(l["charttime"]) >= t0)
    if not L:
        return None
    first_cult = next((m[0] for m in mic if m[1] == "ascitic_fluid"), None)
    if first_cult is not None and (first_cult - L[0]).total_seconds() / 3600 <= 6:
        return None
    counts = _fluid_counts(bundle, L[0], "Ascites")
    if not counts:
        return None
    return (L[0], "ascitic_fluid", {"specimen": "ascitic_fluid", "tests": ["cell count and chemistry"], "collected_before_antimicrobials": None,
                                     "organism": None, "gram_stain": None, "susceptibility": None, "cell_counts": counts,
                                     "findings": [{"test": "cell count and chemistry", "result": "; ".join(f"{k} {v}" for k, v in counts.items())}],
                                     "impression": "Fluid cell count and chemistry; the culture and Gram stain of this sample are not in the structured record."})


def micro_outputs(bundle: dict, t0, t1) -> list[tuple[pd.Timestamp, str, dict]]:
    m = pd.DataFrame(bundle.get("micro", []))
    if m.empty:
        return []
    m["t"] = pd.to_datetime(m.charttime.fillna(m.chartdate))
    m = m[(m.t >= t0) & (m.t <= t1) & ~(m.hadm_id.notna() & (m.hadm_id != bundle["hadm_id"]))]
    res = []
    for (spec, t), g in m.groupby(["spec_type_desc", "t"]):
        key = next((v for k, v in SPEC.items() if str(spec).upper().startswith(k)), None)
        if key is None:
            C6["micro_specimen_not_mapped"] += 1
            continue
        orgs = sorted({str(x) for x in g.org_name.dropna() if str(x) not in ("", "nan", "CANCELLED")})
        tests = sorted({str(x) for x in g.test_name.dropna()})
        if key == "urine" and tests and all(re.search(r"(?i)antigen", tn) for tn in tests):
            C6["micro_urine_antigen_not_a_culture"] += 1  # task 07: a urinary antigen test does not answer a urine-culture order
            continue
        sus = {f"{r.org_name} / {r.ab_name}": str(r.interpretation) for r in g.itertuples()
               if isinstance(getattr(r, "ab_name", None), str) and isinstance(getattr(r, "interpretation", None), str)}
        comments = [B._WS(str(x)) for x in g.comments.dropna()] if "comments" in g else []
        blanked = any(c.strip(" _.") == "" for c in comments)
        comments = list(dict.fromkeys(c for c in comments if c and "___" not in c))[:3]
        # task 06 re-read: a culture without an organism row is not "no growth" when the comment reports growth
        growth_comment = [c for c in comments if re.search(r"(?i)mixed|colony types|contaminat|flora|organisms?\b|colonies|CFU|\d+,000", c)
                          and not re.search(r"(?i)^no growth", c)]
        if orgs:
            result, imp = "; ".join(orgs), "Growth: " + "; ".join(orgs)
        elif growth_comment:
            result = imp = growth_comment[0].rstrip(". ") + "."
            C6["micro_growth_from_comment"] += 1
        elif blanked and not comments:
            result = imp = "Result text not available."
            C6["micro_result_blanked"] += 1
        else:
            result, imp = (comments[0] if comments else "no organism reported"), (comments[0] if comments else "No growth reported.")
        gram = [tn for tn in tests if re.search(r"(?i)gram stain", tn)]
        gram_txt = _test_result(g[g.test_name == gram[0]]) if gram else None
        if gram_txt in ("no organism reported", "Result text not available."):
            gram_txt = None
        res.append((t, key, {"specimen": key, "tests": tests, "collected_before_antimicrobials": None,
                             "organism": "; ".join(orgs) or None, "gram_stain": gram_txt, "susceptibility": sus or None,
                             "cell_counts": _fluid_counts(bundle, t, "Ascites") if key == "ascitic_fluid" else None,
                             "findings": [{"test": tn, "result": _test_result(g[g.test_name == tn])} for tn in tests],
                             "impression": imp}))
    return sorted(res, key=lambda x: x[0])


ED_TX = re.compile(r"(?i)lorazepam|ativan|midazolam|diazepam|levetir|keppra|phenyto|fosphenyto|valpro|depak|lacosam|vimpat|phenobarb|"
                   r"propofol|ketamine|pentobarb")


GENERIC = {r"loraz|ativan": "lorazepam", r"midazol": "midazolam", r"diazep": "diazepam", r"levetir|keppra": "levetiracetam",
           r"fosphenyt": "fosphenytoin", r"(?<!fos)phenyt|dilantin": "phenytoin", r"valpro|depak": "valproate", r"lacosam|vimpat": "lacosamide",
           r"phenobarb": "phenobarbital", r"propofol": "propofol", r"ketamine": "ketamine", r"pentobarb": "pentobarbital",
           r"lamotrig|lamictal": "lamotrigine", r"topiram|topamax": "topiramate", r"(?<!ox)carbamaz|tegretol": "carbamazepine",
           r"oxcarbaz|trileptal": "oxcarbazepine", r"clonazep|klonopin": "clonazepam", r"clobazam": "clobazam", r"brivarac": "brivaracetam",
           r"zonisam": "zonisamide", r"fentanyl": "fentanyl", r"dexmedetom|precedex": "dexmedetomidine", r"hydromorph|dilaudid": "hydromorphone",
           r"morphine": "morphine", r"haloperid|haldol": "haloperidol"}
_ED_SENT = re.compile(r"(?i)\b(?:in the ED|in the emergency|ED course|at the ED|in ED\b|(?:up)?on arrival (?:here|to the ED|to the emergency))")


# --- task 06, leakage round A1 fixes (classes, no record content) ---------------------------------
# Sentences no study answer keeps: recommendations the earlier filter missed, references to another
# study of the stay, communication remnants, differential hedges and clinical attributions.
_REC2 = re.compile(r"(?i)would be (?:more |most )?(?:sensitive|helpful|useful|informative)|should (?:probably |also )?(?:be considered|undergo|be performed|be obtained)|may be further (?:evaluated|assessed|characteri[sz]ed)|"
                   r"can help|for further (?:assessment|evaluation|characteri[sz]ation)|repeat (?:examination|exam|study|imaging|CT|MRI)\b.{0,40}\b(?:in|within|days?|weeks?)\b|"
                   r"\balternatively\b|can be performed|suspicious findings include|\baddendum\b|please refer|for further details|for description of|"
                   r"\bfor which\b[^.;]{0,40}\bevaluation\b|white paper|incidental findings committee|\bACR\b|\bto reach\b|team members|\bsee below\b|see separate|"
                   r"separately (?:described|reported|dictated)|\bconcurrent(?:ly)?\b|attributable|can be attributed|could explain|"
                   r"as (?:found|seen|described) on the (?:recent|concurrent|same[- ]day)|\bechocardiogra\w*|(?<!spin )(?<!spin-)(?<!gradient )(?<!gradient-)(?<!fast spin )\becho\b(?!\s*(?:sequences?|planar|times?|trains?|images?|weighted))|"
                   r"^\s*[\w-]+(?:\s+[\w-]+)?\s+(?:is|are)\s+(?:much\s+)?less likely\.?\s*$|however,? given")
# A procedure of the stay: a follow-up report that shows one is not served; a first report loses the sentence.
_PROC = re.compile(r"(?i)\bEVD\b|ventriculostom|\bshunt|burr hole|craniotom|craniectom|post-?surgical|post-?operative|\bcoil(?:s|ed|ing)?\b|"
                   r"\bclip(?:s|ped|ping)?\b|emboliz|\bstent|\bdrain\b|drainage catheter|interval placement|status post|\bs/p\b|decompressed by")
# In a first report only a procedure of this stay goes (a prior craniotomy or old shunt is a finding of the study).
_PROC_STAY = re.compile(r"(?i)\bEVD\b|ventriculostom|\bdrain\b|drainage catheter|interval (?:placement|coil\w*|clip\w*|emboliz\w*|craniotom\w*|"
                        r"craniectom\w*|shunt|resection|evacuation)|decompressed by|newly placed|post-?procedur\w*|"
                        r"after (?:the )?(?:coil\w*|emboliz\w*|clip\w*|thrombectom\w*)|recent(?:ly)? (?:placed|performed|coil\w*|clip\w*)")
# Lines and tubes placed in hospital (decision 15 keeps the patient's devices in the presentation, not in reports).
_LINES = re.compile(r"(?i)extubat\w*|no evidence of complications|re-?expansion|central (?:venous )?(?:line|catheter)|\bIJ\b|\bPICC\b|\bcatheter\b|has been advanced|malposition\w*|newly placed|"
                    r"\bline\b(?=\s+(?:tip|terminat|project|courses|ends))|\btubes?\b|\blines\b(?=[^.]{0,40}\b(?:position|place|unchanged))")
_PERF = re.compile(r"(?i)perfusion|\bCBF\b|\bCBV\b|\bMTT\b|\bTmax\b|penumbra|\bcore\b|mismatch|blood flow|blood volume|transit time|\bCTP\b|hypoperfus")
_PERF_REF = re.compile(r"(?i)perfusion|\bCTP\b|\bCBF\b|\bCBV\b|\bMTT\b|\bTmax\b|blood flow|blood volume|transit time")
_VEN = re.compile(r"(?i)sinus|venous|vein|jugular|torcula|thromb")
_SPINE_SEC = re.compile(r"(?im)^\s*(?:MRI?|MR)\b[^\n:]{0,40}\bspine\b|^\s*(?:CERVICAL|THORACIC|LUMBAR)(?: SPINE)?\s*:")
_BRAIN_SEC = re.compile(r"(?im)^\s*(?:MRI?|MR)\s+(?:OF\s+THE\s+)?(?:HEAD|BRAIN)\b|^\s*(?:BRAIN|HEAD)\s*:")
_SPINE_S = re.compile(r"(?i)\bcord\b|spinal|\b(?:C[1-8]|T(?:[1-9]|1[0-2])|L[1-5])\s*-\s*(?:[CTLS])?\d{1,2}\b|\bat (?:C|T|L)\d{1,2}\b|\b(?:C|L)[1-8]\b|cervical|thoracic|lumbar|\bconus\b|\bdiscs?\b|foramin|vertebral bod|\bspine\b|marrow|atlantodental|uncovertebral|spondyl|\bfacet")
_BRAIN_S = re.compile(r"(?i)supratentorial|infratentorial|periventricular|subcortical|juxtacortical|pontine|\bpons\b|cerebr(?!ospinal)|corpus callosum|\bbrain\b|"
                      r"ventric|cerebell|MR head|basal ganglia|thalam|centrum semiovale|corona radiata|intracranial|infarct|\bsulci\b|cistern|flow voids?|paranasal|"
                      r"mastoid|\borbits?\b|extra-axial|dural venous|\bsinuses\b")
_CTA_SEC = re.compile(r"(?im)^\s*(?:CTA|CT ANGIO)[^\n:]{0,40}:")
_CTA_HDR = re.compile(r"(?i)\b(?:CTA|CT ANGIO\w*|CT PERFUSION|PERFUSION)(?:\s+(?:OF\s+THE\s+)?(?:HEAD|NECK|BRAIN))?\s*:")
_NC_SEG = re.compile(r"(?is)\b(?:NON-?\s?CONTRAST\s+CT\s+(?:OF\s+THE\s+)?HEAD|NON-?\s?CONTRAST(?:\s+(?:HEAD\s+)?CT)?|UNENHANCED(?:\s+(?:HEAD\s+)?CT)?|CT\s+HEAD\s+(?:WITHOUT|W/O)\s+(?:IV\s+)?CONTRAST|HEAD\s+CT\s+(?:WITHOUT|W/O)\s+(?:IV\s+)?CONTRAST|(?<!\w)HEAD\s+CT|CT\s+HEAD)\s*:.*?(?=\b(?:CTA|CT ANGIO\w*|CT PERFUSION|PERFUSION)(?:\s+(?:OF\s+THE\s+)?(?:HEAD|NECK|BRAIN))?\s*:|$)")
_NC_SENT = re.compile(r"(?i)\b(?:on|in)\s+the\s+(?:non-?\s?contrast|noncontrast|unenhanced|non-?enhanced|pre-?contrast)\s+(?:images?|portion|scan|head\s+CT|CT|study|sequence)|"
                      r"\bunenhanced (?:CT|images?)\b")
# In a plain-CT answer an aetiological inference about an aneurysm goes (the non-contrast image cannot show one; decision 13).
_ANEURYSM_INF = re.compile(r"(?i),?\s*(?:(?:a |an |in a )?(?:distribution|pattern|configuration|location)\s+(?:that is\s+)?)?(?:which is |most |in the absence of trauma,?\s*)?(?:likely|probably|possibly|presumably|concerning|suspicious|worrisome|"
                           r"suggestive|compatible|consistent|concern)\b[^.;]*\baneurysm\w*[^.;]*")
_PLACEMENT_EXAM = re.compile(r"(?i)LINE PLACEMENT|TUBE PLACEMENT|LINE/TUBE|\bPLACEMENT\b")
_LAB_SERIAL_DROP = re.compile(r"(?i)phenyto|valpro|levetir|carbamaz|phenobarb|lacosam|lamotrig|topiram|oxcarb|zonis|vancomycin|gentamicin|tobramycin|"
                              r"amikacin|digoxin|lithium|tacrolimus|cyclospor|sirolimus|theophyll|^INR\(PT\)$|^PT$|^PTT$")
_FLOOR = re.compile(r"(?i)^\s*(?:on|upon)\s+(?:arrival\s+(?:to|on)\s+|transfer\s+to\s+|admission\s+to\s+)?(?:the\s+)?(?:floor|ICU|unit|ward|neuro ?ICU)\b")
_EXAM_HDR = re.compile(r"(?i)physical exam|^\s*(?:_{3}\s+)?exam\s*:|^\s*neurologic(?:al)?(?: exam)?\s*:|^\s*VS\s*:|^\s*vitals?\s*:")


# A reference to another study inside a finding: the clause goes, the finding stays.
_REF_CLAUSE = re.compile(r"(?i)\bgiven the known [^,.;]*,\s*|,?\s*(?:which is |and )?(?:compatible|consistent|in keeping|corresponding)\s+with\s+[^.;]{0,120}?\b(?:as\s+)?(?:seen|found|described|demonstrated|shown)\s+on\s+the\s+"
                         r"(?:recent|concurrent|same[- ]day|current)[^.;]*|,?\s*as\s+(?:found|seen|described|demonstrated|shown)\s+on\s+the\s+(?:recent|concurrent|same[- ]day)[^.;]*")


def _cut_refs(t: str) -> str:
    out = []
    for x in B.split_sents(t or ""):
        y = _REF_CLAUSE.sub("", x)
        if y != x:
            y = y.rstrip(" ,;") + ("." if not y.rstrip().endswith((".", ";")) else "")
            if len(re.findall(r"[A-Za-z]{3,}", y)) >= 3:
                B.TXCOUNT["a1_reference_clause_cut"] += 1
                x = y
        out.append(x)
    return " ".join(out)


_CTA_ONLY = re.compile(r"(?i)paucity of (?:blood )?vessels|\bocclu\w*|\bstenos\w*|\bthromb\w*|cut-?\s?off|\bM[1-4]\b(?! territory)|non-?\s?opacif|aneurysm")


def _drop_nc_run(t: str) -> str:
    """In an angiography answer, a sentence on the unenhanced images goes with the sentences that continue it,
    up to the next sentence about the vessels or the angiographic acquisition."""
    out, in_nc = [], False
    for x in B.split_sents(t or ""):
        if _NC_SENT.search(x):
            in_nc = True
            B.TXCOUNT["a1_noncontrast_sentence_in_cta_dropped"] += 1
            continue
        if in_nc and not (B.VESSEL.search(x) or re.search(r"(?i)\bCTA\b|angiogra|neck|soft tissue|thyroid|lung", x)):
            B.TXCOUNT["a1_noncontrast_sentence_in_cta_dropped"] += 1
            continue
        in_nc = False
        out.append(x)
    return " ".join(out)


def _cut_clause(t: str, rx, counter: str) -> str:
    out = []
    for x in B.split_sents(t or ""):
        y = rx.sub("", x)
        if y != x:
            B.TXCOUNT[counter] += 1
            y = y.strip(" ,;")
            if len(re.findall(r"[A-Za-z]{3,}", y)) < 3:
                continue
            x = y if y.endswith((".", ";")) else y + "."
        out.append(x)
    return " ".join(out)


def _sfilter(t: str, pred, counter: str) -> str:
    if not t:
        return t
    return B.filter_sents(t, pred, counter)


def _norm(t: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def _sec_parts(src: str) -> tuple[str, str] | None:
    """Task 07: a combined brain + spine report: the normalised text of its brain section and of its spine section (findings only)."""
    m = re.search(r"(?m)^\s*IMPRESSIONS?\b", src or "")
    region = (src or "")[: m.start()] if m else (src or "")
    fm = re.search(r"(?m)^\s*FINDINGS?\s*:", region)
    region = region[fm.end():] if fm else region  # task 07: headers in TECHNIQUE are not sections
    b, sp = _BRAIN_SEC.search(region), _SPINE_SEC.search(region)
    if not b or not sp:
        return None
    if b.start() < sp.start():
        return _norm(region[b.start():sp.start()]), _norm(region[sp.start():])
    return _norm(region[b.start():]), _norm(region[sp.start():b.start()])


def _in_part(x: str, part: str, other: str) -> bool:
    n = _norm(re.sub(r"_{2,}", " ", x))[:60]
    return len(n) >= 12 and n in part and n not in other


_DANGLE_END = re.compile(r"(?i)(?:\b(?:may|might|could|can|would|a|an|the|is|are|was|were|be|of|with|without|and|or|in|on|to|for|by|which|that|"
                         r"highly|very|most|more|less)|\b(?:without|no|of) significant|\band (?:chronic|acute)|\ba distribution|\b(?:likely|probably|possibly) in combination)\s*[.;:]?$")
_DOUBLE = re.compile(r"(?i)\b(no|is|are|the|a)\s+(?:\w+\s+)?\1\b")


def _no_dangling(t: str) -> str:
    """Task 07 blind round 1: a sentence left ending on a dangling word or with a doubled word by a cut is dropped whole."""
    if not t:
        return t
    out = []
    for x in B.split_sents(t):
        if x.strip() and not [y for y in out if y.strip()] and re.match(r"(?i)^\s*(?:the\s+)?remainder\b", x):
            B.TXCOUNT["a1_dangling_sentence_dropped"] += 1  # "The remainder of ..." left first by a removal
            continue
        if x.strip() and (_DANGLE_END.search(x.strip()) or re.search(r"(?i)\bno otherwise no\b|^\s*is otherwise\b", x)
                          or re.match(r"^\s*(?:but|and|or|which|although|though)\b", x)):  # a lower-case clause left alone by a cut
            B.TXCOUNT["a1_dangling_sentence_dropped"] += 1
            continue
        out.append(x)
    return " ".join(y for y in out if y.strip())


def _walk_text(o: dict, f) -> dict:
    """Apply f to the report text fields of an imaging answer."""
    o = dict(o)
    f = (lambda t, g=f: _no_dangling(g(t)))
    if isinstance(o.get("impression"), str):
        o["impression"] = B.tidy_impression(f(o["impression"]))
        o["impression"] = re.sub(r"^\s*(?:\d+[.)]\s*)?Otherwise,?\s+(\w)", lambda m: m.group(1).upper(), o["impression"])
    if isinstance(o.get("findings"), list):
        fs = []
        for x in o["findings"]:
            x = dict(x)
            for k in ("description", "finding"):
                if isinstance(x.get(k), str):
                    x[k] = f(x[k])
            if any(isinstance(x.get(k), str) and x[k].strip() for k in ("description", "finding")):
                fs.append(x)
        o["findings"] = fs
    if isinstance(o.get("additional_observations"), list):
        o["additional_observations"] = [y for y in (f(x) if isinstance(x, str) else x for x in o["additional_observations"]) if y]
    if isinstance(o.get("angiography_findings"), dict):
        o["angiography_findings"] = {k: f(v) for k, v in o["angiography_findings"].items() if isinstance(v, str) and f(v).strip()}
    return o


def _empty(o: dict) -> bool:
    return not ((o.get("impression") or "").strip() or o.get("findings") or o.get("additional_observations") or o.get("angiography_findings"))


def _src_text(bundle: dict, exam: str) -> str:
    names = {x.strip() for x in str(exam or "").split(" + ")}
    return "\n".join(r["text"] for r in bundle["radiology"] if r["exam_name"] in names)


def post_filter(case: dict, bundle: dict, cnt: collections.Counter) -> None:
    """Round-A1 fixes on every imaging answer (first outputs and follow-ups)."""
    io, fu, served = case["initial_tool_outputs"], case["followup_outputs"], case["metadata"]["served"]
    tx0 = collections.Counter({k: v for k, v in B.TXCOUNT.items() if k.startswith("a1_")})
    _post_filter(case, bundle, cnt, io, fu, served)
    for k, v in B.TXCOUNT.items():
        if k.startswith("a1_") and v - tx0.get(k, 0):
            cnt[k] += v - tx0.get(k, 0)



_CONSIDER = re.compile(r"(?i),?\s*(?:although|though|but|and|however,?)\s+[^.;]{0,120}?\b(?:should|could|may|might|must)\s+(?:also\s+)?be\s+(?:considered|excluded|entertained)\b")


def _cut_consider(t: str) -> str:
    """Task 07: 'X, although Y should also be considered' keeps the finding X and drops the differential clause."""
    if not t:
        return t
    t2 = _CONSIDER.sub("", t)
    if t2 != t:
        B.TXCOUNT["a1_consider_clause_cut"] += 1
    return t2


_TREAT_EXAM = re.compile(r"(?i)EMBO|COIL|THROMBECT|INTERVENT|STENT|ANEURYSM (?:CLIP|REPAIR)|CRANIOT")


def _after_treatment(case, bundle, cnt, io, fu, served) -> None:
    """Task 07 round 7: brain imaging that is not a policy step and was acquired after a definitive procedure of the stay
    (coiling, embolization, thrombectomy, stenting, craniotomy) shows the treated state: not served (initial or follow-up)."""
    t_ed = anchor(bundle)
    tp = [hours(r["charttime"], t_ed) for r in bundle.get("radiology", []) if _TREAT_EXAM.search(str(r["exam_name"]))]
    tp = [h for h in tp if h is not None]
    if not tp:
        return
    t_tx = min(tp)
    pol = {c["alternatives"][0]["tool_name"] for c in case["ground_truth"]["action_criteria"] if c["importance"] in ("required", "recommended")}
    for key, tool in (("mri", "analyze_brain_mri"), ("advanced_imaging", "order_advanced_imaging")):
        th = served.get(key, {}).get("t_h")
        if io.get(key) and tool not in pol and th is not None and th > t_tx:
            io[key] = None
            served.pop(key, None)
            cnt[f"a1_{key}_after_treatment_not_served"] += 1
    keep = []
    for x in fu:
        k = KEYMAP.get(id(x), "")
        th = served.get(k, {}).get("t_h")
        if x["tool_name"] in ("order_ct_scan", "analyze_brain_mri", "order_advanced_imaging") and th is not None and th > t_tx \
                and x["trigger_action"] != "request_ct_angiography":
            served.pop(k, None)
            cnt["a1_followup_brain_imaging_after_treatment_not_served"] += 1
            continue
        keep.append(x)
    fu[:] = keep


def _post_filter(case, bundle, cnt, io, fu, served) -> None:
    _after_treatment(case, bundle, cnt, io, fu, served)
    base = lambda t: _sfilter(_sfilter(_cut_consider(_cut_refs(t)), _REC2.search, "a1_rec_or_reference_sentence_dropped"), _LINES.search, "a1_line_tube_sentence_dropped")
    first = lambda t: _sfilter(base(t), _PROC_STAY.search, "a1_procedure_sentence_dropped")
    for key, kind in (("ct", "ct"), ("mri", "mri"), ("body_imaging", "body"), ("advanced_imaging", "adv")):
        o = io.get(key)
        if not o:
            continue
        src = _src_text(bundle, served.get(key, {}).get("exam"))
        f = first
        if key == "ct":
            f = lambda t, g=f: _cut_clause(g(t), _ANEURYSM_INF, "a1_aneurysm_inference_in_plain_ct_cut")
        if key == "mri" and (_SPINE_SEC.search(src) or "SPINE" in str(served.get(key, {}).get("exam", "")).upper()):
            f = lambda t, g=f: _sfilter(g(t), _SPINE_S.search, "a1_spine_sentence_in_brain_mri_dropped")
        if False and key == "mri" and re.search(r"(?im)^\s*(?:MRI?|MR)\s+(?:OF\s+THE\s+)?ORBITS?\s*:", src):
            # withdrawn in round 6: analyze_brain_mri has an `orbits` protocol (costs.yaml), so the orbit section of a
            # brain + orbit report answers the brain MRI order
            # task 07: a brain + orbit report: the orbit section's results are another study (no orbit order exists)
            f = lambda t, g=f: _sfilter(g(t), lambda x: re.search(r"(?i)optic|orbit|retrobulbar|extraocular|chiasm|\bglobes?\b", x),
                                        "a1_orbit_sentence_in_brain_mri_dropped")
        parts = _sec_parts(src) if key in ("mri", "body_imaging") else None
        if parts and key == "mri":
            f = lambda t, g=f, P=parts: _sfilter(g(t), lambda x: _in_part(x, P[1], P[0]), "a1_spine_section_sentence_in_brain_mri_dropped")
        if parts and key == "body_imaging" and o.get("region") == "spine":
            f = lambda t, g=f, P=parts: _sfilter(g(t), lambda x: _in_part(x, P[0], P[1]), "a1_brain_section_sentence_in_spine_mri_dropped")
        if key == "body_imaging" and o.get("region") == "spine" and o.get("modality") == "MRI" and _BRAIN_SEC.search(src):
            f = lambda t, g=f: _sfilter(g(t), _BRAIN_S.search, "a1_brain_sentence_in_spine_mri_dropped")
        if key == "ct" and (_CTA_SEC.search(src) or "CTA" in str(served.get(key, {}).get("exam", "")).upper()):
            f = lambda t, g=f: _sfilter(_CTA_HDR.split(g(t))[0], lambda x: B.VESSEL_NC.search(x) or B._CONTRAST_ONLY.search(x),
                                        "a1_vessel_sentence_in_plain_ct_dropped")
        if key == "advanced_imaging" and o.get("modality") == "CT_perfusion":
            f = lambda t, g=f: _sfilter(g(t), lambda x: not _PERF.search(x) or _CTA_ONLY.search(x), "a1_non_perfusion_sentence_dropped")
        if key == "advanced_imaging" and o.get("modality") in ("MR_angiography", "MR_venography"):
            rx = B.VESSEL if o["modality"] == "MR_angiography" else _VEN
            f = lambda t, g=f, rx=rx: _sfilter(g(t), lambda x: not rx.search(x), "a1_non_vessel_sentence_dropped")
        n = _walk_text(o, f)
        if key == "body_imaging":
            for x in n.get("findings", []):
                if isinstance(x.get("location"), str):
                    x["location"] = re.sub(r"(?i)[.;,]?\s*(?:LINE PLACEMENT|TUBE PLACEMENT|LINE/TUBE[^;,]*)", "", x["location"]).strip()
        if _empty(n):  # nothing of this study is left to serve: not available (the perfect agent checks required steps)
            cnt[f"a1_initial_{key}_emptied_not_served"] += 1
            io[key] = None
            served.pop(key, None)
            continue
        io[key] = n
    keep = []
    for x in fu:
        if x["tool_name"] not in ("order_ct_scan", "analyze_brain_mri", "order_body_imaging", "order_advanced_imaging"):
            keep.append(x)
            continue
        o = x["output"]
        first_cta = x["trigger_action"] == "request_ct_angiography"
        raw = json.dumps(o)
        first_of_kind = not x["trigger_action"].startswith("request_repeat_")
        if not first_cta and _PROC.search(raw) and not first_of_kind:
            cnt["a1_followup_report_with_procedure_dropped"] += 1
            served.pop(KEYMAP.get(id(x), ""), None)
            continue
        proc_cut = first_of_kind and not first_cta and _PROC.search(raw)  # task 07 round 6: the first film of a kind keeps its other sentences
        if proc_cut:
            cnt["a1_first_followup_procedure_sentences_cut"] += 1
        if _PLACEMENT_EXAM.search(raw) and x["tool_name"] == "order_body_imaging":
            cnt["a1_followup_placement_exam_dropped"] += 1
            served.pop(KEYMAP.get(id(x), ""), None)
            continue
        f = first if first_cta else base
        if proc_cut:
            f = lambda t, g=f: _sfilter(g(t), _PROC.search, "a1_procedure_sentence_dropped")
        if x["tool_name"] == "order_ct_scan" and "angiography" not in x["trigger_action"]:  # a plain CT answer stops at the CTA section
            f = lambda t, g=f: _CTA_HDR.split(g(t))[0]
        if x["tool_name"] == "order_ct_scan" and "angiography" in x["trigger_action"]:  # the plain-CT section is not the angiography answer
            f = lambda t, g=f: _drop_nc_run(_NC_SEG.sub("", g(t)).strip())
        if x["tool_name"] == "order_ct_scan":  # nor a later MRI's result
            f = lambda t, g=f: _sfilter(g(t), lambda s_: re.search(r"\bMRI?\b|\bMR\b|diffusion", s_) and not re.search(
                r"(?i)\b(?:prior|previous|earlier|outside)\b|compar|from ___|dated", s_), "a1_mri_sentence_in_ct_dropped")
        if x["tool_name"] == "order_ct_scan":  # an angiography answer does not carry the perfusion study
            f = lambda t, g=f: _sfilter(g(t), lambda s_: _PERF_REF.search(s_) and not re.search(r"(?i)\b(?:prior|previous|earlier)\b", s_), "a1_perfusion_sentence_in_cta_dropped")
        if x["tool_name"] == "order_ct_scan" and "angiography" in x["trigger_action"]:  # task 07 round 10: perfusion-section sentences
            src_ = _src_text(bundle, served.get(KEYMAP.get(id(x)) or f"followup:{x['trigger_action']}", {}).get("exam"))
            m_ = re.search(r"(?im)^\s*(?:CT\s+)?PERFUSION[^:\n]{0,30}:", src_ or "")
            if m_:
                end_ = re.search(r"(?im)^\s*(?:CTA|CT ANGIO\w*|IMPRESSION)[^:\n]{0,40}:", src_[m_.end():])
                perf_part = _norm(src_[m_.end(): m_.end() + end_.start()] if end_ else src_[m_.end():])
                f = lambda t, g=f, P=perf_part: _sfilter(g(t), lambda s_: _in_part(s_, P, ""), "a1_perfusion_section_sentence_in_cta_dropped")
        if x["tool_name"] == "order_advanced_imaging" and o.get("modality") == "CT_perfusion":
            f = lambda t, g=f: _sfilter(g(t), lambda s_: not _PERF.search(s_), "a1_non_perfusion_sentence_dropped")
        n = _walk_text(o, f)
        if _empty(n):
            cnt["a1_followup_emptied_dropped"] += 1
            served.pop(KEYMAP.get(id(x), ""), None)
            if first_cta:
                ERRORS6.append("post-filter emptied the first CTA answer")
            continue
        keep.append({**x, "output": n})
        if id(x) in KEYMAP:
            KEYMAP[id(keep[-1])] = KEYMAP[id(x)]
    fu[:] = keep


def fix_presentation(case: dict, cnt: collections.Counter) -> None:
    p = case["patient"]
    meds = (p.get("clinical_history") or {}).get("medications")
    if isinstance(meds, list):  # task 07 round 6: a sentence fragment parsed as a drug (lower-case start, no dose, no frequency)
        keep_m = [m for m in meds if not (isinstance(m, dict) and not m.get("dose") and not m.get("frequency")
                                          and re.match(r"^[a-z]", str(m.get("drug", ""))) and len(str(m.get("drug", "")).split()) >= 2)]
        cnt["medication_fragment_dropped"] += len(meds) - len(keep_m)
        p["clinical_history"]["medications"] = keep_m
    al = (p.get("clinical_history") or {}).get("allergies")
    if isinstance(al, list) and all(str(x).strip(" _.") == "" for x in al) and al:
        p["clinical_history"]["allergies"] = []
        cnt["allergy_bare_blank_removed"] += 1
    elif isinstance(al, list):
        p["clinical_history"]["allergies"] = [x for x in al if str(x).strip(" _.") != ""]
    hpi = p.get("history_present_illness") or ""
    xs = [x for x in B.split_sents(hpi) if x.strip()]
    ys = [x for x in xs if not _FLOOR.match(x)]
    if len(ys) != len(xs):
        cnt["a1_hpi_floor_sentence_dropped"] += len(xs) - len(ys)
        p["history_present_illness"] = " ".join(ys)
    ch = p.get("clinical_history") or {}
    for k in ("family_history", "social_history", "past_medical_history", "allergies", "medications"):
        v = ch.get(k)
        if isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, str) and _EXAM_HDR.search(item):
                    ch[k] = v[:i]
                    cnt[f"a1_{k}_cut_at_exam_header"] += 1
                    break
        elif isinstance(v, str):
            m = _EXAM_HDR.search(v)
            if m:
                ch[k] = v[:m.start()].strip()
                cnt[f"a1_{k}_cut_at_exam_header"] += 1


# --- decision 47 (task 07): repeat values withheld only for the analytes a treatment changes ------
_LAB_LEVEL_DROP = re.compile(r"(?i)phenyto|valpro|levetir|carbamaz|phenobarb|lacosam|lamotrig|topiram|oxcarb|zonis|vancomycin|gentamicin|tobramycin|"
                             r"amikacin|digoxin|lithium|tacrolimus|cyclospor|sirolimus|theophyll")
_D47_AFFECTS = {"glucose": {"Glucose", "Potassium"}, "rbc": {"Hemoglobin", "Hematocrit", "Hematocrit, Calculated", "Red Blood Cells"},
                "platelet": {"Platelet Count"}, "plasma": {"INR(PT)", "PT", "PTT"}, "heparin": {"INR(PT)", "PT", "PTT"}}
_D47_NOTE = {"glucose": re.compile(r"(?i)\binsulin (?:drip|gtt|infusion|sliding scale|was given|given)|sliding[- ]scale|\bISS\b|\bD50\b|"
                                   r"dextrose (?:was )?(?:given|administered|infusion|bolus)|\bamp of D50|treated with insulin|started on insulin"),
             "rbc": re.compile(r"(?i)\btransfus\w*(?!\s+(?:of\s+)?platelets)|\bpRBCs?\b|\bPRBCs?\b|packed red (?:blood )?cells|units? of (?:packed )?(?:red|blood)"),
             "platelet": re.compile(r"(?i)platelet transfusion|transfus\w*[^.]{0,40}?platelets|units? of (?:\w+ )?platelets|\bplatelets? (?:were |was )?(?:given|transfused)"),
             "plasma": re.compile(r"(?i)\bFFP\b|fresh frozen plasma|vitamin K|phytonadione|kcentra|prothrombin complex"),
             # decision 30: therapeutic heparin (procedural bolus, drip) blocks coagulation repeats
             "heparin": re.compile(r"(?i)heparin (?:drip|gtt|infusion|bolus)|heparini[sz]ed|\bACT\b[^.]{0,40}therapeutic|systemic(?:ally)? heparin|argatroban|bivalirudin|"
                                   r"intra-?procedural heparin|heparin was (?:given|started|administered)|"
                                   # task 07: a therapeutic oral anticoagulant given in hospital (decision 30) also blocks coagulation repeats
                                   r"(?:continued|restarted|resumed|started|initiated|bridged)\s+(?:on\s+)?(?:(?:her|his|the)\s+)?(?:home\s+)?(?:warfarin|coumadin|apixaban|eliquis|rivaroxaban|xarelto|dabigatran|pradaxa|edoxaban)|"
                                   r"(?:warfarin|coumadin|apixaban|eliquis|rivaroxaban|xarelto|dabigatran|edoxaban)\s+(?:was|were)\s+(?:continued|restarted|resumed|started)")}
_MED_SECTIONS = re.compile(r"(?i)medications on admission|discharge medications|discharge instructions|followup instructions|"
                           r"discharge disposition|outpatient|home medications")


def _care_text(note: str) -> str:
    """The note without its medication lists and discharge instructions: where a treatment of this stay is stated."""
    from mimic_case_assemble import sections
    sec = sections(note)
    txt = note  # task 07: the whole note minus the medication sections (sections() does not hold every part of the note)
    for k, v in (sec or {}).items():
        if _MED_SECTIONS.search(k) and v and v.strip():
            txt = txt.replace(v, " ")
    return txt


def add_extras(case: dict, audit: dict, cid: str, cond: str, out: Path, man: dict) -> None:
    bundle = json.loads((out / "02_source" / f"{cid}.json").read_text())
    t_ed = anchor(bundle)
    t_adm = ts(bundle["admission"][0]["admittime"])
    t_dis = ts(bundle["admission"][0]["dischtime"])
    t1 = min(t_adm + pd.Timedelta(hours=EXTRA_H), t_dis)
    t24 = t_adm + pd.Timedelta(hours=24)
    io, fu, served = case["initial_tool_outputs"], case["followup_outputs"], case["metadata"]["served"]
    cnt = collections.Counter()
    used_exams = set()
    for v in served.values():
        for x in str(v.get("exam", "")).split(" + "):
            used_exams.add(x.strip())
    # task 06 re-read: a first study that is not a policy step of this case follows the extra-study window
    pol_tools = {c["alternatives"][0]["tool_name"] for c in case["ground_truth"]["action_criteria"] if c["importance"] in ("required", "recommended")}
    key_tool = {"mri": "analyze_brain_mri", "body_imaging": "order_body_imaging", "csf": "analyze_csf", "eeg": "analyze_eeg",
                "specialized_test": "order_specialized_test", "echo": "order_echocardiogram", "advanced_imaging": "order_advanced_imaging"}
    for key, tool in key_tool.items():
        th = served.get(key, {}).get("t_h")
        if io.get(key) and tool not in pol_tools and th is not None and th > hours(t1, t_ed):
            io[key] = None
            served.pop(key, None)
            cnt[f"late_nonpolicy_{key}_not_served"] += 1
        elif io.get(key) and tool in pol_tools and th is not None and th > hours(t1, t_ed):
            cnt[f"late_policy_{key}_served_task04_rule"] += 1
    # EEG storage (decision 41): first recording initial, later ones follow-ups in time order
    note = bundle["discharge"][0]["text"]
    for k, e in enumerate(man.get("eeg_followups", []) or [], start=1):
        e = dict(e)
        for ph in e.get("_verbatim", []) or []:
            if not B.verbatim(ph, note):
                ERRORS6.append(f"eeg_followups[{k}]: phrase not verbatim in the note: {ph[:40]!r}")
        for key in ("clinical_assessment", "tissue_diagnosis"):
            pass
        e.pop("_verbatim", None)
        e.pop("_verbatim_source", None)
        e = B.walk_strings(B.walk_strings(B.walk_strings(e, B.strip_disease_text), B.drop_value_blanks), B.strip_provenance)
        fu.append({"trigger_action": "request_repeat_eeg", "tool_name": "analyze_eeg", "output": e})
        served[f"followup:request_repeat_eeg:{k}"] = {"origin": "note_extracted", "source": "discharge note (later EEG, in time order)"}
        cnt["eeg_followups"] += 1
    if io.get("eeg"):
        case["metadata"]["eeg_source"] = man.get("eeg_source") or ("course_summary" if re.search(r"(?i)course|summary|narrative",
                                                                                             str(served.get("eeg", {}).get("source", ""))) else "formal_report")
        # decisions 36, 46: the recording's treatment context is stated. ED treatment always precedes an inpatient EEG, so the ED
        # medications are stated even when the EEG time is unknown; inpatient infusions only when timed before the recording.
        t_eeg = served.get("eeg", {}).get("t_h")
        ed = sorted({GENERIC[k] for m in bundle.get("ed_pyxis", []) for k in GENERIC if re.search(k, str(m.get("name")), re.I)
                     and (t_eeg is None or (hours(m.get("charttime"), t_ed) is not None and hours(m.get("charttime"), t_ed) < t_eeg))})
        hpi_src = " ".join(re.findall(r"(?is)(?:history of present illness|HPI)\s*:(.*?)(?:\n\s*(?:past medical history|PMH|review of systems|ROS)\b|$)", note)[:1])
        hpi_ed = {GENERIC[k] for sent in re.split(r"(?<=[.!?])\s+", hpi_src)
                  if _ED_SENT.search(sent) and not re.search(r"(?i)\bprior\b|previous|last (?:admission|visit|seizure)|history of|\bhome\b|"
                                                             r"\bon (?:\w+ )?(?:mg )?(?:bid|tid|daily)\b|was (?:on|taking)|takes|outpatient|in the past|years? ago|months? ago", sent)
                  for k in GENERIC if re.search(k, sent, re.I)}
        if hpi_ed - set(ed):
            cnt["eeg_ed_meds_note_only_not_stated"] += 1  # task 07 round 5: the note's HPI cannot be dated to this ED visit reliably
        inpt = []
        if t_eeg is not None:
            trx = B.treatments_for(out, bundle["hadm_id"])
            if len(trx):
                late = trx[(trx.t > t_ed) & trx.classes.str.contains("antiseizure", na=False)]
                late = late[[hours(t, t_ed) is not None and hours(t, t_ed) < t_eeg for t in late.t]]
                inpt = sorted({GENERIC[k] for n in late.name for k in GENERIC if re.search(k, str(n), re.I)} - set(ed))
        else:
            cnt["eeg_treatment_context_time_unknown"] += 1
        before_tx = re.search(r"(?i)before (?:any |the )?(?:ED )?(?:treatment|benzodiazepine|lorazepam|ativan|antiseizure|anti-?epileptic|loading)",
                              json.dumps(served.get("eeg", {})) + " " + str(man.get("eeg", {}).get("_verbatim_source", "")) + " " + json.dumps(man.get("eeg_notes", "")))
        if before_tx:
            cnt["eeg_recorded_before_treatment"] += 1
        elif ed or inpt:
            txt = ("Recorded after ED treatment (ED medication record) with: " + ", ".join(ed) if ed else "Recorded after treatment with: " + ", ".join(inpt))
            if ed and inpt:
                txt += "; then inpatient " + ", ".join(inpt)
            prev = str(io["eeg"].get("limitations") or "").strip()
            io["eeg"]["limitations"] = (prev.rstrip(". ") + ". " if prev and "Recorded after" not in prev else "") + txt + "."
            cnt["eeg_treatment_context"] += 1
    for key in ("clinical_assessment", "tissue_diagnosis"):
        x = man.get(key)
        for ph in (x or {}).get("_verbatim", []) or []:
            if not B.verbatim(ph, note):
                ERRORS6.append(f"{key}: phrase not verbatim in the note: {ph[:40]!r}")
        if x:
            x = {k: v for k, v in x.items() if not k.startswith("_")}
            io[key] = B.walk_strings(B.walk_strings(B.walk_strings(x, B.strip_disease_text), B.drop_value_blanks), B.strip_provenance) \
                if key == "clinical_assessment" else B.walk_strings(B.walk_strings(x, B.drop_value_blanks), B.strip_provenance)
            served[key] = {"origin": "note_extracted", "source": "discharge note"}
    # ECG: later machine reads in the window
    ecgs = sorted([r for r in bundle.get("ecg_machine", []) if hours(r["ecg_time"], t_ed) is not None
                   and -1.0 <= hours(r["ecg_time"], t_ed) <= hours(t1, t_ed)], key=lambda r: r["ecg_time"])
    first_t = served.get("ecg", {}).get("t_h")
    for r in ecgs:
        h = hours(r["ecg_time"], t_ed)
        if first_t is not None and h <= first_t + 1e-6:
            continue
        o = ecg_row(r)
        if o:
            fu.append({"trigger_action": "request_repeat_ecg", "tool_name": "analyze_ecg", "output": o})
            served[f"followup:request_repeat_ecg:{cnt['ecg_followups'] + 1}"] = {"origin": "table", "source": "MIMIC-IV-ECG machine_measurements", "t_h": h}
            cnt["ecg_followups"] += 1
            if cnt["ecg_followups"] >= 3:
                break
    # imaging: every report in the window not yet served
    rad = sorted([r for r in bundle["radiology"] if hours(r["charttime"], t_ed) is not None and -1.0 <= hours(r["charttime"], t_ed) <= hours(t1, t_ed)],
                 key=lambda r: r["charttime"])
    seen_text = set()
    for r in rad:
        name = str(r["exam_name"]).upper()
        if r["exam_name"] in used_exams or B._WS(r["text"]) in seen_text or not (re.search(B.FINDINGS, r["text"]) or B.IMPRESSION.search(r["text"])):
            continue
        seen_text.add(B._WS(r["text"]))
        later = ts(r["charttime"]) > t24
        h = hours(r["charttime"], t_ed)
        spec = None
        if re.search(NCCT_EXAM, name):
            spec = ("order_ct_scan", None, None, "request_repeat_ct")
        elif re.search(CTA_EXAM, name):
            spec = ("order_ct_scan", None, None, "request_repeat_ct_angiography")
        elif re.search(SPINE_MRI_EXAM, name):
            spec = ("order_body_imaging", "spine_MRI", ("spine", "MRI"), "request_repeat_spine_mri")
        elif re.search(MRI_EXAM, name) and not re.search(r"MRA|MRV", name):
            spec = ("analyze_brain_mri", None, None, "request_repeat_mri")
        else:
            for rx, tool, study, region, trig in BODY:
                if re.search(rx, name):
                    spec = (tool, study, region, trig)
                    break
        if spec is None:
            cnt["imaging_not_mapped"] += 1
            continue
        tool, study, region, trig = spec
        o = rad_output(r, tool, study, region, later)
        if tool == "order_ct_scan" and _CTA_SEC.search(r["text"]):  # a combined report (decision 2)
            f_, imp_, _, _ = B.report_text(r, later=later)
            ncf, nci, rest = B.split_cta(clean(f_, later), clean(imp_, later))
            if trig == "request_repeat_ct":
                if not ncf.strip():
                    cnt["a1_combined_report_no_separable_plain_ct"] += 1
                    continue
                o = B.ct_report(B.no_other_study(ncf, "ct"), B.no_other_study(nci, "ct"), "CT HEAD WITHOUT CONTRAST", False)
                if io.get("ct") and B._WS(json.dumps(o["findings"])) == B._WS(json.dumps(io["ct"].get("findings"))):
                    cnt["repeat_ct_same_as_first_skipped"] += 1  # the same combined report already answers the first CT
                    continue
                cnt["a1_repeat_ct_from_split"] += 1
            else:
                imp_k = B.tidy_impression(" ".join(x for x in B.split_sents(clean(imp_, later)) if x.strip() and (B.VESSEL.search(x) or B._NOT_HEAD.search(x))))
                o = B.ct_report(rest, imp_k, r["exam_name"], True)
                cnt["a1_repeat_cta_from_split"] += 1
        if not (o.get("impression") or o.get("findings") or o.get("additional_observations")):
            continue
        if tool == "order_advanced_imaging" and not io.get("advanced_imaging"):
            io["advanced_imaging"] = o
            served["advanced_imaging"] = {"origin": "table", "source": "note/radiology", "exam": r["exam_name"], "t_h": h}
        elif tool == "order_ct_scan" and trig == "request_repeat_ct_angiography":
            # the CTA follow-up already holds the first CTA; a later one is a repeat
            fu.append({"trigger_action": trig, "tool_name": tool, "output": {**o, "angiography_findings": {r["exam_name"]: " ".join(f["description"] for f in o["findings"])}}})
            KEYMAP[id(fu[-1])] = f"followup:{trig}:{h:.1f}"
            served[f"followup:{trig}:{h:.1f}"] = {"origin": "table", "source": "note/radiology", "exam": r["exam_name"], "t_h": h}
        else:
            if tool == "order_ct_scan" and not io.get("ct") and trig == "request_repeat_ct" and ts(r["charttime"]) <= t24:
                io["ct"] = o
                served["ct"] = {"origin": "table", "source": "note/radiology", "exam": r["exam_name"], "t_h": h}
            else:
                if any(x["trigger_action"] == trig for x in fu):
                    trig = trig.replace("request_", "request_repeat_", 1) if "repeat" not in trig else trig
                fu.append({"trigger_action": trig, "tool_name": tool, "output": o})
                KEYMAP[id(fu[-1])] = f"followup:{trig}:{h:.1f}"
                served[f"followup:{trig}:{h:.1f}"] = {"origin": "table", "source": "note/radiology", "exam": r["exam_name"], "t_h": h}
        cnt[f"imaging_{study or tool}"] += 1
    # serial labs: the next value of each item, up to the decision point, same rules as the first
    L = B.lab_rows_all(bundle) if hasattr(B, "lab_rows_all") else None
    labs = pd.DataFrame(bundle["labs"])
    if len(labs) and io.get("labs"):
        labs["t"] = pd.to_datetime(labs.charttime)
        labs = labs[~(labs.hadm_id.notna() & (labs.hadm_id != bundle["hadm_id"])) & (labs.t >= t_ed - pd.Timedelta(hours=1)) & (labs.t <= t1)
                    & (labs.fluid == "Blood")]
        f0 = labs.sort_values("t").drop_duplicates("itemid")  # task 07 round 7: an item whose first draw has no result is not served at all
        labs = labs[~labs.itemid.isin(set(f0[f0.value.isna() & f0.valuenum.isna()].itemid)) & (labs.value.notna() | labs.valuenum.notna())]
        labs = labs[~labs.label.str.fullmatch(r"H|I|L|[SU]TX\d+|HPE\d+|Delete|Voided Specimen|.*\bHold\b.*|Specimen Type|Problem", case=False, na=False)]
        labs = labs[~labs.label.str.contains(r"(?i)^intubated$|ventilat|\bPEEP\b|tidal volume|^O2 Flow$|required O2|^Rates$|^Vent|^Oxygen$", na=False)]
        labs = labs.sort_values("t")
        second = labs.groupby("itemid").nth(1)
        if isinstance(second, pd.DataFrame) and len(second):
            tr = B.treatments_for(out, bundle["hadm_id"])
            tt = {k: tr[tr.classes.str.contains(k, na=False)].t.min() for k in B.TREAT_CLASSES} if len(tr) else {}
            aed = list(zip(tr[tr.classes.str.contains("antiseizure", na=False)].t, tr[tr.classes.str.contains("antiseizure", na=False)].name)) if len(tr) else []
            n_ser = len(second)
            # decision 47: repeat blood gases and drug levels stay withheld; coagulation follows decision 30 (treat_blocked)
            second = second[~second.category.eq("Blood Gas") & ~second.label.str.contains(_LAB_LEVEL_DROP, na=False)]  # the whole gas sample, lactate included
            cnt["d47_serial_gas_or_level_withheld"] += n_ser - len(second)
            # decision 38 plausibility: a specimen whose Na - Cl - HCO3 is below 3 is not a valid serum set
            for spec, gs in second.groupby("specimen_id"):
                v = {r.label: r.valuenum for r in gs.itertuples() if pd.notna(r.valuenum)}
                if {"Sodium", "Chloride", "Bicarbonate"} <= set(v) and v["Sodium"] - v["Chloride"] - v["Bicarbonate"] < 3:
                    bad = gs.label.isin(["Sodium", "Chloride", "Bicarbonate", "Anion Gap"])
                    second = second.drop(gs[bad].index)
                    cnt["d38_serial_implausible_electrolytes_dropped"] += int(bad.sum())
            # decision 47: a treatment blocks only the analytes it changes; timed -> later draws; note-stated without a time -> all repeats
            timed = {"glucose": [], "rbc": [], "platelet": [], "plasma": [], "heparin": []}
            for r in tr.itertuples() if len(tr) else []:
                nm, cl = str(r.name).lower(), str(r.classes)
                if "glucose" in cl:
                    timed["glucose"].append(r.t)
                if "transfusion" in cl:
                    timed["platelet" if re.search(r"platelet", nm) else "rbc"].append(r.t)
                if re.search(r"plasma|\bffp\b|vitamin k|phytonadione|kcentra|prothrombin complex", nm):
                    timed["plasma"].append(r.t)
            care = _care_text(note)
            # a procedure report of the stay (catheter angiography, coiling) that states heparin is a timed anticoagulant exposure
            for r_ in bundle.get("radiology", []):
                if re.search(r"(?i)EMBO|COIL|CATH|ANGIO|INTERVENT|THROMBECT|\bDSA\b", str(r_["exam_name"])) \
                        and not re.search(r"(?i)^CTA|^MRA|^MR ANGIO|CT ANGIO|^CHEST", str(r_["exam_name"])) and re.search(r"(?i)heparin", r_["text"]):
                    timed["heparin"].append(pd.Timestamp(r_["charttime"]))
            stated = {k: bool(rx.search(care)) for k, rx in _D47_NOTE.items()}
            # decision 30: LMWH started in hospital at a therapeutic dose (the dose may be stated only in the discharge list)
            if re.search(r"(?i)(?:initiated|started|begun|began)\b[^.]{0,40}\b(?:lovenox|enoxaparin|dalteparin|fragmin)", care) and \
                    re.search(r"(?i)(?:enoxaparin|lovenox)[^\n]{0,30}?\b(?:[6-9]\d|1\d\d)\s*mg[^\n]{0,20}\b(?:BID|Q12H|twice)|mg/kg", note):
                stated["heparin"] = True
                cnt["d47_note_therapeutic_lmwh"] += 1
            def d47_blocked(row) -> str:
                for k, labs_k in _D47_AFFECTS.items():
                    if row.label not in labs_k:
                        continue
                    if timed[k] and min(timed[k]) < row.t:
                        return f"timed_{k}"
                    if stated[k]:  # stated in the note: its time is not known, so every repeat of the analyte is withheld
                        return f"note_{k}"
                return ""
            why = {i: d47_blocked(row) for i, row in second.iterrows()}
            for w in why.values():
                if w:
                    cnt[f"d47_serial_blocked_{w}"] += 1
            second = second.loc[[i for i, w in why.items() if not w]]
            tt_other = {k: v for k, v in tt.items() if k not in ("glucose", "transfusion")}
            keep = [i for i, row in second.iterrows() if not B.treat_blocked(row.label, row.t, tt_other, aed)
                    and not (pd.isna(row.valuenum) and re.fullmatch(r"\s*_{3}\s*", str(row.value)))]
            cnt["serial_lab_values_blocked"] += len(second) - len(keep)
            s2 = second.loc[keep]
            if len(s2):
                lo, _, _ = labs_output(s2, t_ed)
                if lo:
                    fu.append({"trigger_action": "request_repeat_labs", "tool_name": "interpret_labs", "output": lo})
                    served["followup:request_repeat_labs"] = {"origin": "table", "source": "hosp/labevents, second value per item up to admission + 48 h",
                                                              "t_first_h": hours(s2.t.min(), t_ed), "t_last_h": hours(s2.t.max(), t_ed), "items": int(len(s2))}
                    cnt["serial_lab_values"] += len(s2)
    post_filter(case, bundle, cnt)
    fix_presentation(case, cnt)
    # microbiology
    mic = micro_outputs(bundle, t_ed - pd.Timedelta(hours=1), t_dis)
    tap = ascitic_first_tap(bundle, mic, t_ed - pd.Timedelta(hours=1))
    if tap:
        mic = sorted(mic + [tap], key=lambda x: x[0])
        cnt["ascitic_first_tap_from_fluid_labs"] += 1
    want = [c["alternatives"][0]["required_arguments"].get("specimen") for c in case["ground_truth"]["action_criteria"]
            if c["alternatives"][0]["tool_name"] == "order_microbiology"]
    mic = [m for m in mic if m[1] in want] [:1] + [m for m in mic if not (m[1] in want and m is ([x for x in mic if x[1] in want] or [None])[0])]
    mic = [m for k_, m in enumerate(mic) if (k_ == 0 and m[1] in want) or m[0] <= t1]  # only the first policy specimen may follow the decision point
    abx = re.compile(r"(?i)cef|ceph|vanco|piperacillin|zosyn|tazobact|cipro|levoflox|moxiflox|metronid|flagyl|ampicillin|amoxicillin|unasyn|"
                     r"gentamicin|tobramycin|azithro|doxycycl|meropenem|ertapenem|imipenem|bactrim|sulfameth|nafcillin|oxacillin|clinda|"
                     r"linezolid|daptomycin|rifaximin|penicillin|aztreonam|acyclovir")
    trx = B.treatments_for(out, bundle["hadm_id"])
    abx_t = sorted([pd.Timestamp(r_.t) for r_ in trx.itertuples() if abx.search(str(r_.name))]) if len(trx) else []
    pat = case["patient"]
    med_txt = json.dumps(pat.get("clinical_history", {}).get("medications", ""))
    on_abx = abx.search(re.sub(r"(?i)\b(?:val)?acyclovir\b", " ", med_txt)) is not None  # antibacterial on the home list
    on_antiviral_only = not on_abx and re.search(r"(?i)\b(?:val)?acyclovir\b", med_txt) is not None
    hpi_abx = re.search(r"(?i)(?:antibiotic|" + abx.pattern.removeprefix("(?i)") + r")", str(pat.get("history_present_illness", ""))) is not None
    for k, (t, key, o) in enumerate(mic):
        o["collected_before_antimicrobials"] = (not abx_t or abx_t[0] > t)  # task 07: from the ED / ward medication times
        if on_abx:  # an antibiotic on the admission medication list: the sample follows an outpatient course
            o["collected_before_antimicrobials"] = False
            cnt["micro_after_outpatient_antibiotic"] += 1
        elif on_antiviral_only and o["collected_before_antimicrobials"]:  # home antiviral prophylaxis: not stated either way
            o["collected_before_antimicrobials"] = None
            cnt["micro_home_antiviral_timing_unknown"] += 1
        elif hpi_abx and o["collected_before_antimicrobials"]:  # the HPI names antibiotics: timing unknown (conservative)
            o["collected_before_antimicrobials"] = None
            cnt["micro_antibiotic_timing_unknown"] += 1
        src = "hosp/labevents (ascitic fluid cell count and chemistry)" if o.get("tests") == ["cell count and chemistry"] else "hosp/microbiologyevents"
        if not io.get("microbiology"):
            io["microbiology"] = o
            served["microbiology"] = {"origin": "table", "source": src, "t_h": hours(t, t_ed)}
        else:
            trig = f"request_{key}" + ("_culture" if key in ("urine", "sputum", "stool") else "")
            if any(x["trigger_action"] == trig for x in fu):
                trig = trig.replace("request_", "request_repeat_", 1)
            fu.append({"trigger_action": trig, "tool_name": "order_microbiology", "output": o})
            served[f"followup:{trig}:{hours(t, t_ed):.1f}"] = {"origin": "table", "source": "hosp/microbiologyevents", "t_h": hours(t, t_ed)}
        cnt["micro_specimens"] += 1
    # decision 38: CSF numbers in plausible ranges
    csf = io.get("csf")
    if csf:
        for k, v in list((csf.get("cell_count") or {}).items()):
            m = re.match(r"^\s*([<>]?\s*[\d.]+)", str(v))
            if not m:
                continue
            x = float(re.sub(r"[<>\s]", "", m.group(1)))
            lim = 100 if "%" in str(v) else 10_000_000
            if x < 0 or x > lim:
                del csf["cell_count"][k]
                cnt["csf_value_out_of_range_dropped"] += 1
    case["metadata"]["build_counts"].update({f"c6_{k}": v for k, v in cnt.items()})
    case["metadata"]["build_counts"].update({f"c6_{k}": v for k, v in C6.items()})
    case["metadata"]["decision_point"] = f"admission + {EXTRA_H:.0f} h for extra studies (first policy studies of the stay as in task 04)"


# --- task 07: decisions 42, 44 and the served-metadata cleanup ---------------------------------------
_SAH_STATUS: dict = {}
KEYMAP: dict = {}  # id(follow-up item) -> its served-metadata key (task 07: a dropped follow-up takes its own key with it)
_I60_8_FIRST = "non-aneurysmal subarachnoid hemorrhage"


def _drop_criteria(case: dict, tool: str, importance: str, why: str) -> int:
    crit = case["ground_truth"]["action_criteria"]
    keep = [c for c in crit if not (c["alternatives"][0]["tool_name"] == tool and c["importance"] == importance)]
    gone = [c.get("criterion_id") for c in crit if c not in keep]
    case["ground_truth"]["action_criteria"] = keep
    pol = case["metadata"].get("policy", {})
    for g in gone:
        pol.get("criteria", {}).pop(g, None)
    pol.setdefault("adapted", []).append(f"{importance} {tool} dropped: {why}")
    return len(crit) - len(keep)


_VIT_LINE = re.compile(r"(?i)\b(?:BP|HR|RR|R|O2\s*Sats?|SpO2|POX|T|Temp)\b\s*:?\s*(?:\d|___)")


def note_vitals(note: str) -> dict | None:
    """Vitals of the admission exam: the first line after an exam header that carries at least three vital-sign labels."""
    m = re.search(r"(?im)^\s*(?:admission (?:physical )?exam|physical exam(?:ination)?(?: on admission)?|exam on admission|on admission)\b.*$", note)
    if not m:
        return None
    for line in note[m.start():m.start() + 1500].splitlines()[:12]:
        if len(_VIT_LINE.findall(line)) < 3:
            continue
        g = lambda rx: (lambda mm: mm.group(1) if mm else None)(re.search(rx, line, re.I))
        bp = re.search(r"(?i)\bBP\s*:?\s*(\d{2,3})\s*/\s*(\d{2,3})", line)
        num = lambda v, lo, hi: int(float(v)) if v is not None and lo <= float(v) <= hi else None
        t = g(r"\b(?:T|Temp)\s*:?\s*(\d{2,3}(?:\.\d)?)(?![\d.])")
        temp = None
        if t is not None:
            t = float(t)
            temp = round((t - 32) * 5 / 9, 1) if 90 <= t <= 110 else (round(t, 1) if 32 <= t <= 43 else None)
        return {"bp_systolic": num(bp.group(1), 50, 300) if bp else None, "bp_diastolic": num(bp.group(2), 20, 200) if bp else None,
                "hr": num(g(r"\b(?:HR|P|Pulse)\s*:?\s*(\d{2,3})(?![\d.])"), 20, 250), "temp": temp,
                "rr": num(g(r"\b(?:RR|R|Resp)\s*:?\s*(\d{1,2})\b"), 4, 60),
                "spo2": num(g(r"(?:O2\s*Sats?|SpO2|POX|O2)\s*:?\s*(\d{2,3})\s*%"), 50, 100)}
    return None


_EXTRA7: dict = {}


def task07_post(case: dict, cid: str, cond: str, out: Path, man: dict, bundle: dict) -> list[str]:
    errs = []
    io, fu, served, meta = case["initial_tool_outputs"], case["followup_outputs"], case["metadata"]["served"], case["metadata"]
    note = bundle["discharge"][0]["text"]
    # task 07 round 5: note-extracted CSF results of the same LP and an intact social history (reader extraction, verbatim-checked)
    if not _EXTRA7 and (out / "07_extract_csf_social.json").exists():
        _EXTRA7.update(json.loads((out / "07_extract_csf_social.json").read_text()))
    wsn = lambda t: re.sub(r"\s+", " ", str(t or "")).strip().lower()
    nn = wsn(note)
    ex_ = _EXTRA7.get("csf", {}).get(cid)
    if ex_ and io.get("csf") and io["csf"].get("source", "lumbar_puncture") == "lumbar_puncture":
        added = []
        for fld in ("appearance", "opening_pressure"):
            v = ex_.get(fld)
            if v and wsn(v) in nn and str(io["csf"].get(fld, "")).strip().lower() in ("", "not recorded"):
                io["csf"][fld] = re.sub(r"\s+", " ", v).strip()
                added.append(fld)
        st = {k: re.sub(r"\s+", " ", v).strip() for k, v in (ex_.get("special_tests") or {}).items()
              if v and "___" not in v and all(wsn(part) in nn for part in v.split("; "))  # spans joined by "; " are each verbatim
              }
        # decision 24 applied to CSF test names: a disease name inside a test label or result is removed, the result is served
        _DZ = re.compile(r"(?i)\s*(?:multiple sclerosis|\bMS\b|neuromyelitis optica(?: spectrum disorder)?|\bNMO(?:SD)?\b)\s*(?:/\s*)?")
        dz = []
        st2 = {}
        for k, v in st.items():
            k2, v2 = _DZ.sub(" ", k).strip(" /-"), _DZ.sub(" ", v).strip(" /-")
            if (k2, v2) != (k, v):
                dz.append(k)
            if k2 and re.search(r"[A-Za-z]{3,}", v2):
                st2[re.sub(r"\s+", " ", k2)] = re.sub(r"\s+", " ", v2)
        st = st2
        if dz:
            case["metadata"]["build_counts"]["csf_test_disease_name_removed"] = len(dz)
        if st:
            io["csf"]["special_tests"] = {**(io["csf"].get("special_tests") or {}), **st}
            added.append("special_tests")
        dropped = [f for f in ("appearance", "opening_pressure") if ex_.get(f) and f not in added] + \
                  [k for k, v in (ex_.get("special_tests") or {}).items() if k not in st
                   and k not in dz and _DZ.sub(" ", k).strip(" /-") not in st]
        if added:
            served.setdefault("csf", {})["note_extracted_fields"] = added
            case["metadata"]["build_counts"]["csf_note_extracted_fields"] = len(added) - ("special_tests" in added) + len(st)
        if dropped:
            errs.append(f"csf note extraction not verbatim: {dropped}")
    if "meds" not in _EXTRA7 and (out / "07_extract_meds.json").exists():
        _EXTRA7["meds"] = json.loads((out / "07_extract_meds.json").read_text())
    mx = (_EXTRA7.get("meds") or {}).get(cid)
    if mx and mx.get("medications"):  # task 07 round 7: the parsed list was broken; reader extraction of the pre-admission list
        ml = [{k: re.sub(r"\s+", " ", str(m.get(k, ""))).strip() for k in ("drug", "dose", "frequency", "indication")} for m in mx["medications"]]
        bad = [m["drug"] for m in ml if not all(wsn(m[k]) in nn for k in ("drug", "dose", "frequency") if m[k]) or "___" in m["drug"]]
        if bad:
            errs.append(f"medication extraction not verbatim: {len(bad)} items")
        else:
            case["patient"]["clinical_history"]["medications"] = [{k: re.sub(r"\s*<br\s*/?>\s*", " ", v).strip() for k, v in m.items()} for m in ml]
            meta.setdefault("presentation_sources", {})["medications"] = "discharge note, pre-admission list (reader extraction, verbatim-checked)"
    sx = _EXTRA7.get("social", {}).get(cid)
    if sx:
        sh = {}
        for k, v in sx.get("social_history", {}).items():
            vs = v if isinstance(v, list) else [v]
            vs = [re.sub(r"\s+", " ", x).strip() for x in vs if x and "___" not in x]
            if vs and all(wsn(x) in nn for x in vs):
                sh[k] = "; ".join(vs)
            elif vs:
                errs.append(f"social history item not verbatim: {k}")
        if sh:
            case["patient"]["clinical_history"]["social_history"] = sh
            meta.setdefault("presentation_sources", {})["social_history"] = "discharge note, Social History section (reader extraction, blanked sentences left out)"
    # task 07: ED vitals blank in triage and vitalsign -> the admission exam's vitals line of the note (a blanked value stays empty)
    ps = meta.get("presentation_sources", {})
    have = sum(x is not None for x in (case["patient"].get("vitals") or {}).values())
    if ps.get("vitals") == "none recorded" or have < 3:  # task 07: ED vitals blank or nearly so (fewer than 3 values)
        v = note_vitals(note)
        if v and sum(x is not None for x in v.values()) >= max(3, have + 1):
            case["patient"]["vitals"] = v
            ps["vitals"] = "discharge note, admission exam vitals line (ED vitals blank)"
            case["metadata"]["build_counts"]["vitals_from_admission_exam"] = 1
    # decision 42: SAH aneurysm status from the record
    if cond == "SAH":
        if not _SAH_STATUS and (out / "07_sah_status.json").exists():
            _SAH_STATUS.update(json.loads((out / "07_sah_status.json").read_text()))
        st = _SAH_STATUS.get(cid, {})
        meta["sah_aneurysm_status"] = st.get("aneurysm_status", "not_read")
        if st.get("aneurysm_status") in ("angiography_negative", "non_aneurysmal_other_cause"):
            dx = case["ground_truth"]["diagnosis"]
            dx["icd_codes"] = ["I60.8"] + [c for c in dx["icd_codes"] if not c.startswith("I60")]
            dx["accepted"] = [_I60_8_FIRST]
            meta["diagnosis_code_note"] = "primary code set to I60.8 from the record's angiography (decision 42)"
        elif st.get("aneurysm_status") != "aneurysm_shown":
            errs.append("decision 42: SAH aneurysm status not established (exclude)")
    # decision 44: CSF source; a drain sample is never a lumbar puncture
    csf = io.get("csf")
    if csf:
        st = _SAH_STATUS.get(cid, {}) if cond == "SAH" else {}
        drain_note = bool(re.search(r"(?i)\bEVD\b|ventriculostom|external ventricular|lumbar drain", note))
        src = st.get("csf_source") if cond == "SAH" else ("" if drain_note else "lumbar_puncture")
        if src == "lumbar_puncture":
            csf["source"] = "lumbar_puncture"
        else:
            imp = [c["importance"] for c in case["ground_truth"]["action_criteria"] if c["alternatives"][0]["tool_name"] == "analyze_csf"]
            io["csf"] = None
            served.pop("csf", None)
            meta["csf_not_served"] = "first CSF of the stay is a drain sample or of unclear source; no lumbar-puncture CSF (decision 44)"
            if "required" in imp:
                errs.append("decision 44: required lumbar-puncture CSF has only drain or unclear-source samples (exclude)")
            elif imp:
                _drop_criteria(case, "analyze_csf", imp[0], "no lumbar-puncture CSF in the record (decision 44)")
    # decision 44: hours from ED arrival of every policy study
    key_of = {"interpret_labs": "labs", "analyze_eeg": "eeg", "analyze_brain_mri": "mri", "analyze_ecg": "ecg", "analyze_csf": "csf",
              "order_ct_scan": "ct", "order_echocardiogram": "echo", "order_cardiac_monitoring": "cardiac_monitoring",
              "order_advanced_imaging": "advanced_imaging", "order_specialized_test": "specialized_test", "order_body_imaging": "body_imaging",
              "order_microbiology": "microbiology", "obtain_tissue_diagnosis": "tissue_diagnosis", "perform_clinical_assessment": "clinical_assessment"}
    hrs = {}
    for c in case["ground_truth"]["action_criteria"]:
        if c["importance"] not in ("required", "recommended"):
            continue
        t = c["alternatives"][0]["tool_name"]
        k = key_of.get(t)
        if not k:
            continue
        args = c["alternatives"][0].get("required_arguments", {})
        angio = t == "order_ct_scan" and args.get("angiography")
        sv = (next((v for kk, v in served.items() if kk.startswith("followup:request_ct_angiography")), {}) if angio else served.get(k)) or {}
        if t == "order_specialized_test" and args.get("test_type") and (io.get("specialized_test") or {}).get("test_type") != args["test_type"]:
            trig = next((x["trigger_action"] for x in fu if x["tool_name"] == t and x["output"].get("test_type") == args["test_type"]), None)
            sv = next((v for kk, v in served.items() if trig and kk.startswith(f"followup:{trig}")), {}) if trig else {}
        th = (sv.get("t_h") if sv.get("t_h") is not None else sv.get("t_first_h")) if isinstance(sv, dict) else None
        hrs[c.get("criterion_id", t)] = {"tool": t, "importance": c["importance"], "t_h_from_ed_arrival": th,
                               "origin": sv.get("origin") if isinstance(sv, dict) else None}
    # telemetry: the first structured rhythm record of the window
    for v in hrs.values():
        if v["tool"] == "order_cardiac_monitoring" and v["t_h_from_ed_arrival"] is None and io.get("cardiac_monitoring"):
            t_ed_ = anchor(bundle)
            ts_ = [pd.Timestamp(x["charttime"]) for x in bundle.get("icu_chart", []) if x.get("itemid") == 220048 and x.get("charttime")]
            ts_ += [pd.Timestamp(x["charttime"]) for x in bundle.get("ed_vitals", []) if x.get("rhythm") not in (None, "") and str(x.get("rhythm")) != "nan" and x.get("charttime")]
            if ts_:
                v["t_h_from_ed_arrival"] = round(hours(min(ts_), t_ed_), 1)
    meta["policy_study_hours"] = hrs
    # contrast stated in the technique overrides the exam title (task 07 re-read)
    for key in ("mri", "body_imaging"):
        o = io.get(key)
        if not o or (key == "body_imaging" and o.get("modality") != "MRI"):
            continue
        src = _src_text(bundle, served.get(key, {}).get("exam"))
        tech = re.search(r"(?is)TECHNIQUE\s*:(.*?)(?:\n\s*[A-Z][A-Z ]{3,}:|\Z)", src)
        tech = tech.group(1) if tech else ""
        flag = "contrast_used" if key == "mri" else "contrast"
        ex = str(served.get(key, {}).get("exam", "")).upper().split(" + ")[0]
        if key == "mri" and re.search(r"W/O\b|WITHOUT", ex) and not re.search(r"W ?& ?W/O|W AND W/O|W/ CONTRAST|WITH CONTRAST|W/WO", ex) \
                and re.search(r"(?i)\bMRA\b|angiogra|\bneck\b", tech or ""):
            continue  # task 07: the exam title says non-contrast; contrast in the technique belongs to another part (e.g. a neck MRA)
        if re.search(r"(?i)gadolinium|gadavist|magnevist|multihance|dotarem|post-?contrast|after (?:the )?(?:intravenous |IV )?(?:administration of )?contrast", tech) \
                and not re.search(r"(?i)no (?:intravenous |IV )?contrast was|without (?:intravenous |IV )?contrast", tech) and o.get(flag) is False:
            o[flag] = True
            C6["contrast_flag_from_technique"] += 1
    for c in case["ground_truth"]["action_criteria"]:  # criteria name the contrast the served study has
        a0 = c["alternatives"][0]
        if a0["tool_name"] == "analyze_brain_mri" and "contrast" in a0.get("required_arguments", {}) and io.get("mri"):
            a0["required_arguments"]["contrast"] = bool(io["mri"].get("contrast_used"))
        if a0["tool_name"] == "order_body_imaging" and a0.get("required_arguments", {}).get("study") == "spine_MRI" \
                and "contrast" in a0["required_arguments"] and io.get("body_imaging"):
            a0["required_arguments"]["contrast"] = bool(io["body_imaging"].get("contrast"))
    # MRI contrast stated by the reader (combined reports where contrast was given for another part)
    if io.get("mri") and isinstance(man.get("mri_contrast_used"), bool):
        io["mri"]["contrast_used"] = man["mri_contrast_used"]
        for c in case["ground_truth"]["action_criteria"]:
            a0 = c["alternatives"][0]
            if a0["tool_name"] == "analyze_brain_mri" and "contrast" in a0.get("required_arguments", {}):
                a0["required_arguments"]["contrast"] = man["mri_contrast_used"]
    return errs


def build_all6(a) -> None:
    from neuroagent_schemas import NeuroBenchCase
    from mimic_case_review import review_md
    out = Path(a.out)
    B.TAG[0] = "06"
    if not (out / B.OPTS["treatments"]).exists():
        print("06_treatments.parquet missing: using 04_treatments.parquet (test builds only)", file=sys.stderr)
        B.OPTS["treatments"] = "04_treatments.parquet"
    sel = pd.read_csv(out / a.selection)
    sel = sel[sel.case_id.notna() & (sel.case_id != "")]
    if "exclusion" in sel and not a.cases_only:
        sel = sel[sel.exclusion.isna() | (sel.exclusion == "")]
    if a.cases_only:
        sel = sel[sel.case_id.isin(a.cases_only)]
    cdir = out / "06_cases"
    for d in ("06_cases", "06_hpi_audit", "06_review"):
        (out / d).mkdir(exist_ok=True)
    path = out / "06_build_checks.json"
    checks = json.loads(path.read_text()) if path.exists() else {}
    for r in sel.itertuples():
        if not (out / "06_manual" / f"{r.case_id}.json").exists():
            print(f"{r.case_id}: no manual file yet", file=sys.stderr)
            continue
        C6.clear()
        man = json.loads((out / "06_manual" / f"{r.case_id}.json").read_text())
        MAN_CURRENT.clear()
        MAN_CURRENT.update(man)
        case, audit, errors = B.build_case3(r.case_id, r.condition, out, Path(a.cases))
        ERRORS6.clear()
        add_extras(case, audit, r.case_id, r.condition, out, man)
        errors += list(ERRORS6)
        errors += task07_post(case, r.case_id, r.condition, out, man, json.loads((out / "02_source" / f"{r.case_id}.json").read_text()))
        cause = (man.get("dx_support") or {}).get("cause_icd10")
        if r.condition == "SYNC" and cause:
            dx = case["ground_truth"]["diagnosis"]
            dx["icd_codes"] = [cause] + [c for c in dx["icd_codes"] if c != cause]
            dx["accepted"] = [str((man.get("dx_support") or {}).get("cause_label") or (man.get("dx_support") or {}).get("reason", ""))[:120] or "cardiac syncope"]
        case["metadata"]["builder"] = "mimic_case_build6.py (task 06)"
        case["metadata"]["source"] = "MIMIC-IV 3.1 + ED 2.2 + Note 2.2 + ECG 1.0 (credentialed; id map in 06_selection.csv)"
        try:
            NeuroBenchCase.model_validate(case)
            valid = "ok"
        except Exception as exc:
            valid = f"INVALID: {exc}"
        (cdir / f"{r.case_id}.json").write_text(json.dumps(case, indent=1, default=str))
        (out / "06_hpi_audit" / f"{r.case_id}.json").write_text(json.dumps(audit, indent=1))
        pa_err, pa_warn, pa_acc = B.perfect_agent3(cdir, r.case_id) if valid == "ok" else (["not run: invalid"], [], [])
        checks[r.case_id] = {"condition": r.condition, "schema": valid, "build_errors": errors, "perfect_agent_errors": pa_err,
                             "perfect_agent_warnings": pa_warn, "perfect_agent_knowledge_library_accepted": pa_acc}
        (out / "06_review" / f"{r.case_id}.md").write_text(review_md(case, audit))
        print(f"{r.case_id}: schema {valid[:60]}; build errors {len(errors)}; perfect agent {'ok' if not pa_err else 'FAIL ' + str(len(pa_err))}",
              file=sys.stderr)
        for e in errors + pa_err:
            print(f"    {e}", file=sys.stderr)
    path.write_text(json.dumps(checks, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--selection", default="06_selection.csv")
    ap.add_argument("--cases", default=str(B.ROOT / "data/neurobench/cases"))
    ap.add_argument("--cases-only", nargs="*", default=[])
    build_all6(ap.parse_args())
