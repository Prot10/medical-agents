"""Normalize malformed `followup_outputs[].output` blocks to their canonical model.

Background: `FollowUpToolOutput.output` is an unkeyed Pydantic union. Followup
outputs authored in legacy / wrong shapes (a `{"general": {...}}` wrapper, a
free-text `{"report": "..."}`, `{tool_name, study_type, report: {...}}`, a
`drug_pair` interaction form, `interactions` as list[dict], wrong value types,
etc.) silently resolve to the WRONG model (usually an empty `CardiacMonitoringReport`),
losing their content at runtime. This script rewrites every such output into the
canonical shape implied by its `tool_name`, **losslessly** — a safety net guarantees
every >=40-char source text fragment survives in the result.

It pairs with the `tool_name`-keyed validator on `FollowUpToolOutput` (which makes
resolution deterministic going forward). This migration cleans the stored data.

Usage:
    uv run python agent-platform/scripts/normalize_followup_outputs.py --dry-run
    uv run python agent-platform/scripts/normalize_followup_outputs.py --apply
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from neuroagent_schemas import NeuroBenchCase
from neuroagent_schemas.tool_outputs import (
    AdvancedImagingReport, CardiacMonitoringReport, CSFResults, CTReport, ECGReport,
    EchoReport, EEGReport, LabResults, LiteratureSearchResult, MRIReport,
    DrugInteractionResult, SpecializedTestReport,
)

CASES_DIR = Path("data/neurobench_v5/cases")

MODEL = {
    "analyze_eeg": EEGReport, "analyze_brain_mri": MRIReport, "interpret_labs": LabResults,
    "analyze_csf": CSFResults, "analyze_ecg": ECGReport, "order_ct_scan": CTReport,
    "order_echocardiogram": EchoReport, "order_cardiac_monitoring": CardiacMonitoringReport,
    "order_advanced_imaging": AdvancedImagingReport, "order_specialized_test": SpecializedTestReport,
    "search_medical_literature": LiteratureSearchResult, "check_drug_interactions": DrugInteractionResult,
}
PRIMARY = {
    "MRIReport": "impression", "CTReport": "impression", "AdvancedImagingReport": "impression",
    "SpecializedTestReport": "impression", "EchoReport": "impression",
    "CardiacMonitoringReport": "impression", "EEGReport": "impression",
    "LiteratureSearchResult": "summary", "DrugInteractionResult": "summary",
    "ECGReport": "interpretation", "LabResults": "interpretation", "CSFResults": "interpretation",
}
META_KEYS = {"tool_name", "timestamp", "study_type"}


def _s(v):
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, (int, float, bool)):
        return str(v)
    return json.dumps(v, ensure_ascii=False)


def _strlist(x):
    if x is None:
        return []
    if not isinstance(x, list):
        return [_s(x)]
    out = []
    for v in x:
        if isinstance(v, str):
            out.append(v)
        elif isinstance(v, dict):
            out.append(v.get("finding") or v.get("recommendation")
                       or "; ".join(f"{k}: {_s(w)}" for k, w in v.items()))
        else:
            out.append(_s(v))
    return out


def _dictstr(d):
    if not isinstance(d, dict):
        return {}
    return {str(k): _s(v) for k, v in d.items() if v is not None}


def _findings_strdict(x):
    if not isinstance(x, list):
        return []
    return [_dictstr(v) if isinstance(v, dict) else {"finding": _s(v)} for v in x]


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _all_texts(o, acc):
    if isinstance(o, str):
        if len(o.strip()) >= 40:
            acc.append(o)
    elif isinstance(o, dict):
        for v in o.values():
            _all_texts(v, acc)
    elif isinstance(o, list):
        for v in o:
            _all_texts(v, acc)


def _blob(o) -> str:
    """Whitespace-normalized concatenation of every string value in `o`.

    Compares like-with-like across the source dict and the normalized dict —
    avoids false mismatches from json escaping (real newlines vs the `\\n`
    two-char escape that json.dumps produces)."""
    parts: list[str] = []

    def walk(x):
        if isinstance(x, str):
            parts.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(o)
    return _ws(" ".join(parts))


def _core(tool, out):
    M = MODEL[tool]
    out = dict(out)
    if set(out.keys()) == {"general"} and isinstance(out["general"], dict):
        out = dict(out["general"])
    study = out.get("study_type")
    if isinstance(out.get("report"), dict):
        out = dict(out["report"])
    for k in META_KEYS:
        out.pop(k, None)

    if M is LiteratureSearchResult:
        rep = out.get("report")
        summ = (rep if isinstance(rep, str) else "") or out.get("summary") or out.get("interpretation") or ""
        return {"query": _s(out.get("query", "")),
                "results": [r for r in (out.get("results") or []) if isinstance(r, dict)],
                "summary": summ}
    if M is DrugInteractionResult:
        if "drug_pair" in out and "proposed" not in out:
            dp = out.get("drug_pair") or []
            pair = " x ".join(dp) if isinstance(dp, list) else _s(dp)
            it = out.get("interaction_type", "")
            s = f"{pair} ({out.get('severity','')}{', '+it if it else ''}): {out.get('mechanism','')} {out.get('recommendation','')}".strip()
            return {"proposed": (dp[0] if isinstance(dp, list) and dp else ""), "interactions": [s],
                    "contraindications": [], "warnings": [], "formulary_status": "",
                    "alternatives": [], "summary": _s(out.get("summary", ""))}
        if isinstance(out.get("report"), str):
            return {"proposed": "", "interactions": [], "contraindications": [], "warnings": [],
                    "formulary_status": "", "alternatives": [], "summary": out["report"]}
        prop = out.get("proposed", "")
        return {"proposed": "; ".join(prop) if isinstance(prop, list) else _s(prop),
                "interactions": _strlist(out.get("interactions")),
                "contraindications": _strlist(out.get("contraindications")),
                "warnings": _strlist(out.get("warnings")),
                "formulary_status": _s(out.get("formulary_status", "")),
                "alternatives": _strlist(out.get("alternatives")),
                "summary": _s(out.get("summary", ""))}
    if M is AdvancedImagingReport:
        impr = _s(out.get("impression", "")) or _s(out.get("summary", ""))
        if out.get("clinical_significance"):
            impr = (impr + " " + _s(out.get("clinical_significance"))).strip()
        if out.get("additional_observations"):
            impr = (impr + " " + " ".join(_strlist(out.get("additional_observations")))).strip()
        if out.get("differential_by_imaging"):
            impr = (impr + " Differential: " + "; ".join(_strlist(out.get("differential_by_imaging")))).strip()
        return {"modality": _s(out.get("modality") or study or ""),
                "tracer_or_protocol": out.get("tracer_or_protocol"),
                "findings": _findings_strdict(out.get("findings")),
                "quantitative_data": _dictstr(out["quantitative_data"]) if isinstance(out.get("quantitative_data"), dict) else None,
                "impression": impr, "recommended_actions": _strlist(out.get("recommended_actions"))}
    if M is SpecializedTestReport:
        return {"test_type": _s(out.get("test_type", "")),
                "findings": _findings_strdict(out.get("findings")),
                "quantitative_data": _dictstr(out["quantitative_data"]) if isinstance(out.get("quantitative_data"), dict) else None,
                "impression": _s(out.get("impression", "")),
                "recommended_actions": _strlist(out.get("recommended_actions"))}
    if M is MRIReport:
        extra = _strlist(out.get("additional_observations"))
        good = []
        for fi in (out.get("findings") or []):
            if isinstance(fi, dict) and fi.get("type") and fi.get("location"):
                good.append(fi)
            else:
                extra.append(fi if isinstance(fi, str) else json.dumps(fi, ensure_ascii=False))
        return {"findings": good, "volumetrics": out.get("volumetrics"), "additional_observations": extra,
                "impression": _s(out.get("impression", "")),
                "differential_by_imaging": [x for x in (out.get("differential_by_imaging") or []) if isinstance(x, dict)],
                "recommended_actions": _strlist(out.get("recommended_actions"))}
    if M is CTReport:
        extra = _strlist(out.get("additional_observations"))
        good = []
        for fi in (out.get("findings") or []):
            if isinstance(fi, dict) and fi.get("type") and fi.get("location"):
                good.append(fi)
            else:
                extra.append(fi if isinstance(fi, str) else json.dumps(fi, ensure_ascii=False))
        return {"findings": good, "contrast_used": bool(out.get("contrast_used", False)),
                "angiography_findings": out.get("angiography_findings"), "additional_observations": extra,
                "impression": _s(out.get("impression", "")),
                "recommended_actions": _strlist(out.get("recommended_actions"))}
    if M is ECGReport:
        try:
            rate = int(out.get("rate", 0))
        except (TypeError, ValueError):
            rate = 0
        return {"rhythm": _s(out.get("rhythm", "")), "rate": rate, "intervals": _dictstr(out.get("intervals", {})),
                "axis": _s(out.get("axis", "")), "findings": _strlist(out.get("findings")),
                "interpretation": _s(out.get("interpretation") or out.get("impression", "")),
                "clinical_correlation": " ".join(_strlist(out.get("recommended_actions"))) if out.get("recommended_actions") else _s(out.get("clinical_correlation", ""))}
    if M is EchoReport:
        ef = out.get("ejection_fraction")
        ef = ef if isinstance(ef, (int, float)) else (out.get("ef") if isinstance(out.get("ef"), (int, float)) else None)
        return {"chambers": _dictstr(out.get("chambers", {})),
                "valves": _dictstr(out["valves"]) if isinstance(out.get("valves"), dict) else ({"summary": _s(out.get("valves"))} if out.get("valves") else {}),
                "ejection_fraction": ef, "wall_motion": out.get("wall_motion"),
                "findings": _strlist(out.get("findings") or out.get("structural_findings") or out.get("additional_findings")),
                "impression": (_s(out.get("impression", "")) or _s(out.get("summary", ""))) + ((" " + _s(out.get("clinical_significance"))) if out.get("clinical_significance") else ""),
                "recommended_actions": _strlist(out.get("recommended_actions"))}
    if M is CardiacMonitoringReport:
        return {"duration_hours": int(out.get("duration_hours", 0) or 0), "monitor_type": _s(out.get("monitor_type", "")),
                "rhythm_summary": _s(out.get("rhythm_summary", "")),
                "heart_rate_range": {str(k): int(v) for k, v in (out.get("heart_rate_range", {}) or {}).items() if isinstance(v, (int, float))},
                "events": [_dictstr(e) for e in (out.get("events") or [])], "findings": _strlist(out.get("findings")),
                "impression": _s(out.get("impression", "")), "recommended_actions": _strlist(out.get("recommended_actions"))}
    if M is EEGReport:
        cls = out.get("classification", "")
        if cls not in ("normal", "abnormal"):
            cls = "abnormal" if out.get("findings") else "normal"
        return {"classification": cls, "background": _dictstr(out.get("background", {})),
                "findings": [f for f in (out.get("findings") or []) if isinstance(f, dict) and f.get("type") and f.get("location")],
                "artifacts": [a for a in (out.get("artifacts") or []) if isinstance(a, dict)],
                "activating_procedures": _dictstr(out.get("activating_procedures", {})),
                "impression": _s(out.get("impression", "")), "limitations": _s(out.get("limitations", "")),
                "recommended_actions": _strlist(out.get("recommended_actions"))}
    if M is LabResults:
        panels = out.get("panels", {}) or {}
        newp = {}
        for pname, pv in panels.items():
            if isinstance(pv, list):
                newp[pname] = pv
            elif isinstance(pv, dict):
                rows = []
                for analyte, val in pv.items():
                    sval = _s(val)
                    ab = any(t in sval for t in ("[H]", "[L]", "POSITIVE", "(H)", "(L)", "abnormal", "elevated", "reduced"))
                    rows.append({"test": analyte, "value": sval, "unit": "", "reference_range": "", "is_abnormal": ab})
                newp[pname] = rows
        return {"panels": newp, "interpretation": _s(out.get("interpretation", "")),
                "abnormal_values_summary": _strlist(out.get("abnormal_values_summary"))}
    if M is CSFResults:
        d = dict(out)
        d["cell_count"] = _dictstr(out.get("cell_count", {}))
        d["special_tests"] = _dictstr(out.get("special_tests", {}))
        for k in ("appearance", "opening_pressure", "protein", "glucose", "glucose_ratio", "interpretation"):
            d[k] = _s(out.get(k, ""))
        return d
    return dict(out)


def normalize_followup_output(tool, out):
    """Return a canonical model_dump() for `out` under `tool`, losslessly. Idempotent."""
    M = MODEL.get(tool)
    if M is None or not isinstance(out, dict):
        return out
    o = dict(out)
    if o.get("recommendations") and not o.get("recommended_actions"):
        o["recommended_actions"] = o["recommendations"]
    if o.get("test_name") and not o.get("test_type"):
        o["test_type"] = o["test_name"]
    d = _core(tool, o)
    dumped = M.model_validate(d).model_dump()
    # Safety net: every >=40-char source text fragment must survive in the
    # VALIDATED output (extra keys are already dropped at this point, so any
    # content that lived in a non-schema key is caught here and re-homed).
    prim = PRIMARY[M.__name__]
    src_texts = []
    _all_texts(out, src_texts)
    blob = _blob(dumped)
    missing = [t for t in src_texts if _ws(t)[:60] not in blob]
    if missing:
        dumped[prim] = (_s(dumped.get(prim, "")) + " " + " ".join(missing)).strip()
        dumped = M.model_validate(dumped).model_dump()
    return dumped


def needs_migration(tool, out) -> bool:
    """A followup needs migration iff it has keys outside its model (content that
    would be silently ignored) OR fails strict validation against its model."""
    M = MODEL.get(tool)
    if M is None or not isinstance(out, dict):
        return False
    if set(out.keys()) - set(M.model_fields.keys()):
        return True
    try:
        M.model_validate(out)
        return False
    except Exception:
        return True


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    p.add_argument("--cases-dir", type=Path, default=CASES_DIR)
    args = p.parse_args()

    files = sorted(args.cases_dir.glob("*.json"))
    n_out = 0
    n_files = 0
    lost = []
    for f in files:
        raw_text = f.read_text()
        raw = json.loads(raw_text)
        changed = False
        for fu in raw.get("followup_outputs", []) or []:
            tool = fu.get("tool_name")
            out = fu.get("output")
            if not needs_migration(tool, out):
                continue
            norm = normalize_followup_output(tool, out)
            # verify lossless
            src_texts = []
            _all_texts(out, src_texts)
            blob = _blob(norm)
            for t in src_texts:
                if _ws(t)[:60] not in blob:
                    lost.append((f.name, tool, _ws(t)[:70]))
            fu["output"] = norm
            n_out += 1
            changed = True
        if changed:
            n_files += 1
            if args.apply:
                use_literal = any(ord(c) > 127 for c in raw_text)
                f.write_text(json.dumps(raw, indent=2, ensure_ascii=not use_literal) + "\n")

    print(f"{'APPLIED' if args.apply else 'DRY-RUN'}: {n_out} followup outputs across {n_files} files")
    print(f"content fragments NOT preserved: {len(lost)}")
    for x in lost[:30]:
        print("   LOST:", x)
    return 1 if lost else 0


if __name__ == "__main__":
    raise SystemExit(main())
