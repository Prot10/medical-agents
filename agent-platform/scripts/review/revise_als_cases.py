"""Apply the July 2026 ALS review across actions, outputs and reasoning."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

CSF_TESTS = {
    "ALS-M04": ["cytology", "flow_cytometry"],             # prior breast cancer / neoplastic mimic
    "ALS-M08": ["oligoclonal_bands", "IgG_index", "JCV_PCR"],  # MS on natalizumab / PML activity
    "ALS-P03": [],                                         # MMN/CIDP adjudication: basic CSF
    "ALS-P05": ["HIV_RNA"],                               # HIV-associated motor syndrome
    "ALS-P06": ["cytology", "flow_cytometry"],             # IgM MGUS / malignant-paraneoplastic mimic
}

# The 2023 consensus guideline recommends offering testing to every person with
# ALS.  These are the cases where the SFT trace should actively take up that offer.
GENETICS_TRACE_CASES = {"ALS-P02", "ALS-P03", "ALS-P05", "ALS-P08", "ALS-P09", "ALS-S07", "ALS-S10"}

BASE_PANELS = ["CBC", "CMP", "calcium", "TSH", "vitamin_B12", "folate", "CK", "ESR", "CRP"]
TARGET_PANELS = {
    "ALS-M04": ["paraneoplastic"],
    "ALS-P03": ["anti_GM1_IgM"],
    "ALS-P04": ["androgen_receptor_CAG_repeat"],
    "ALS-P05": ["HIV"],
    "ALS-P06": ["SPEP", "IFE", "serum_free_light_chains"],
}


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _reports(case: dict[str, Any], tool: str, key: str) -> list[dict[str, Any]]:
    out = []
    if case["initial_tool_outputs"].get(key): out.append(case["initial_tool_outputs"][key])
    out.extend(x["output"] for x in case["followup_outputs"] if x.get("tool_name") == tool and x.get("output"))
    return out


def _find_report(case: dict[str, Any], tool: str, key: str, token: str) -> dict[str, Any]:
    rows = _reports(case, tool, key)
    report = next((x for x in rows if token.lower() in json.dumps(x).lower()), None)
    if report is None: raise ValueError(f"{case['case_id']}: missing {tool} report containing {token}")
    return _copy(report)


def _is_als_gene(name: str) -> bool:
    low = name.lower()
    return any(x in low for x in ("c9orf72", "sod1", "tardbp", "fus ", "fus_", "tbk1", "als genetic"))


def _genetic_report(case: dict[str, Any]) -> dict[str, Any]:
    existing = next((x for x in _reports(case, "order_specialized_test", "specialized_test")
                     if "genetic_panel" in str(x.get("test_type", "")).lower()), None)
    if existing:
        report = _copy(existing); report["test_type"] = "genetic_panel:ALS"
        for row in report.get("findings", []):
            if row.get("interpretation") is None: row["interpretation"] = ""
        return report
    findings = []
    for report in _reports(case, "interpret_labs", "labs"):
        for panel in report.get("panels", {}).values():
            for row in panel:
                if _is_als_gene(str(row.get("test", ""))):
                    findings.append({"test": row.get("test"), "result": row.get("value"),
                                     "interpretation": row.get("clinical_significance") or ""})
    if not findings:
        findings = [
            {"test": "C9orf72 repeat expansion", "result": "No pathogenic expansion detected", "interpretation": ""},
            {"test": "ALS gene panel (including SOD1, TARDBP, FUS, TBK1)", "result": "No pathogenic variant detected", "interpretation": ""},
        ]
    abnormal = any(any(x in str(row.get("result", "")).lower() for x in ("positive", "pathogenic", "600+", "800+", "a4v")) for row in findings)
    return {"test_type": "genetic_panel:ALS", "findings": findings,
            "quantitative_data": None,
            "impression": "Pathogenic ALS-associated variant identified; provide post-test counselling."
                          if abnormal else "No pathogenic variant identified on the offered ALS panel; a negative result does not exclude ALS.",
            "recommended_actions": ["Pre- and post-test genetic counselling; discuss implications for relatives and gene-targeted therapy/trials"]}


def _allowed_lab(name: str, cid: str) -> bool:
    low = name.lower().replace("-", "_").replace(" ", "_")
    if _is_als_gene(name): return False
    baseline = ("wbc", "hemoglobin", "hematocrit", "platelet", "rbc", "mcv", "sodium", "potassium", "chloride",
                "bicarbonate", "co2", "bun", "creatinine", "glucose", "ast", "alt", "bilirubin", "alkaline",
                "albumin", "calcium", "tsh", "thyroid", "free_t4", "vitamin_b12", "folate", "creatine_kinase", "ck", "esr", "crp")
    if any(token in low for token in baseline): return True
    target = {
        "ALS-M04": ("paraneoplastic", "anti_hu", "anti_yo", "anti_ri"),
        "ALS-P03": ("gm1",),
        "ALS-P04": ("androgen_receptor", "cag_repeat"),
        "ALS-P05": ("hiv",),
        "ALS-P06": ("spep", "immunofix", "free_light", "m_protein", "igm"),
    }.get(cid, ())
    return any(token in low for token in target)


def _baseline_rows() -> list[dict[str, Any]]:
    return [
        {"test": "ESR", "value": 8, "unit": "mm/h", "reference_range": "0-20", "is_abnormal": False, "clinical_significance": None},
        {"test": "CRP", "value": 2, "unit": "mg/L", "reference_range": "<5", "is_abnormal": False, "clinical_significance": None},
        {"test": "Vitamin B12", "value": 420, "unit": "pg/mL", "reference_range": "200-900", "is_abnormal": False, "clinical_significance": None},
        {"test": "Folate", "value": 10, "unit": "ng/mL", "reference_range": ">4", "is_abnormal": False, "clinical_significance": None},
    ]


def _clean_labs(case: dict[str, Any]) -> dict[str, Any]:
    cid = case["case_id"]; source = _copy(case["initial_tool_outputs"]["labs"])
    panels = {}
    seen = set()
    for name, rows in source.get("panels", {}).items():
        selected = []
        for row in rows:
            test = str(row.get("test", "")); key = test.lower()
            if _allowed_lab(test, cid) and key not in seen:
                selected.append(row); seen.add(key)
        if selected: panels[name] = selected
    supplements = [x for x in _baseline_rows() if str(x["test"]).lower() not in seen]
    if supplements: panels["Reviewer baseline rule-out additions"] = supplements
    source["panels"] = panels
    abnormal = []
    for rows in panels.values():
        for row in rows:
            if row.get("is_abnormal"): abnormal.append(f"{row.get('test')}: {row.get('value')}")
    source["abnormal_values_summary"] = abnormal
    source["interpretation"] = "Rule-out studies do not confirm ALS. " + ("Targeted abnormalities are listed above." if abnormal else "No treatable mimic identified in the selected panel.")
    return source


def _clean_csf(payload: dict[str, Any], requested: list[str]) -> dict[str, Any]:
    payload = _copy(payload); old = payload.get("special_tests", {})
    selected = {}
    aliases = {
        "oligoclonal_bands": ("oligoclonal",), "IgG_index": ("igg index",),
        "JCV_PCR": ("jc virus", "jcv"), "HIV_RNA": ("hiv",),
        "cytology": ("cytology",), "flow_cytometry": ("flow",),
    }
    defaults = {
        "JCV_PCR": "Not detected", "HIV_RNA": "Not detected",
        "cytology": "No malignant cells", "flow_cytometry": "No clonal lymphoid population",
        "oligoclonal_bands": "Absent", "IgG_index": "Within reference range",
    }
    for test in requested:
        value = next((v for k, v in old.items() if any(token in k.lower() for token in aliases[test])), defaults[test])
        selected[test] = value
    payload["special_tests"] = selected
    basics = f"WBC {payload.get('cell_count')}; protein {payload.get('protein')}; glucose {payload.get('glucose')}."
    payload["interpretation"] = basics + (f" Targeted mimic studies: {selected}." if selected else " Basic CSF only for the competing inflammatory neuropathy question.") + " CSF does not confirm ALS."
    return payload


def _rebuild_outputs(case: dict[str, Any]) -> None:
    cid = case["case_id"]; initial = case["initial_tool_outputs"]
    genetics = _genetic_report(case)
    emg = _find_report(case, "order_specialized_test", "specialized_test", "emg")
    emg["test_type"] = "emg_ncs"; initial["specialized_test"] = emg
    initial["labs"] = _clean_labs(case)
    initial["eeg"] = None; initial["ecg"] = None; initial["advanced_imaging"] = None
    csf_reports = _reports(case, "analyze_csf", "csf")
    initial["csf"] = _clean_csf(csf_reports[0], CSF_TESTS[cid]) if cid in CSF_TESTS and csf_reports else None

    respiratory = _find_report(case, "order_specialized_test", "specialized_test", "respiratory_function")
    respiratory["test_type"] = "respiratory_function"
    rows = [x for x in case["followup_outputs"] if x.get("tool_name") not in
            {"order_specialized_test", "analyze_csf", "analyze_eeg", "analyze_ecg", "order_advanced_imaging", "interpret_labs"}]
    rows.append({"trigger_action": "request_baseline_respiratory_function", "tool_name": "order_specialized_test",
                 "tool_parameters": {"test_type": "respiratory_function"}, "output": respiratory})
    rows.append({"trigger_action": "offer_als_genetic_panel_after_counselling", "tool_name": "order_specialized_test",
                 "tool_parameters": {"test_type": "genetic_panel:ALS"}, "output": genetics})
    case["followup_outputs"] = rows


def _action(tool: str, category: str, params: dict[str, Any], text: str, finding: str) -> dict[str, Any]:
    return {"action": text, "tool_name": tool, "expected_finding": finding, "category": category,
            "tool_parameters": params, "citation": "[EAN_ALS_2024]", "guideline_source": "Gold Coast; EAN 2024; NICE NG42"}


def _revise_actions(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    removed = {"analyze_brain_mri", "order_body_imaging", "interpret_labs", "analyze_csf", "order_specialized_test", "analyze_eeg", "analyze_ecg", "order_advanced_imaging"}
    kept = [x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") not in removed]
    kept += [
        _action("analyze_brain_mri", "required", {"protocol": "standard", "contrast": True},
                "Obtain brain MRI to exclude structural, brainstem, inflammatory, demyelinating or neoplastic ALS mimics",
                "No better structural explanation for progressive upper and lower motor-neuron findings"),
        _action("order_body_imaging", "required", {"study": "spine_MRI", "contrast": False},
                "Obtain cervical and thoracic spinal-cord MRI to exclude compressive myelopathy and other cord lesions",
                "No compressive, neoplastic, inflammatory or demyelinating cord mimic"),
        _action("interpret_labs", "required", {"panels": BASE_PANELS + TARGET_PANELS.get(cid, [])},
                "Order a baseline treatable-mimic panel, adding only phenotype-specific infectious, immune, paraprotein or metabolic tests",
                "Exclude common hematologic, renal/hepatic, electrolyte, calcium, thyroid, B12/folate, muscle and inflammatory alternatives; tests do not confirm ALS"),
        _action("order_specialized_test", "required", {"test_type": "emg_ncs"},
                "Perform EMG/NCS across bulbar, cervical, thoracic and lumbosacral regions using ALS electrodiagnostic criteria",
                "Active and chronic neurogenic change in multiple regions with preserved sensory studies and no conduction block"),
        _action("order_specialized_test", "recommended", {"test_type": "respiratory_function"},
                "Obtain baseline FVC/VC and SNIP or MIP after suspected ALS is established; this is a safety and management assessment, not a diagnostic confirmation",
                "Quantify respiratory involvement and need for surveillance or non-invasive ventilation"),
        _action("order_specialized_test", "optional", {"test_type": "genetic_panel:ALS"},
                "Offer an ALS gene panel including C9orf72 and SOD1 after pre-test counselling; do not embed genetics in a routine blood panel",
                "A pathogenic result can affect counselling, family risk and gene-targeted therapy/trial eligibility; a negative result does not exclude ALS"),
    ]
    if cid in CSF_TESTS:
        kept.append(_action("analyze_csf", "optional", {"special_tests": CSF_TESTS[cid]},
                            "Consider CSF only because this atypical case raises a specific inflammatory, infectious or neoplastic mimic",
                            "Answer the named mimic question; CSF and neurofilaments do not diagnose routine ALS"))
    for i, row in enumerate(kept, 1): row["step"] = i
    case["ground_truth"]["optimal_actions"] = kept


def _clean(case: dict[str, Any]) -> None:
    cid = case["case_id"]; gt = case["ground_truth"]
    for field in ("critical_actions", "key_reasoning_points", "contraindicated_actions"):
        gt[field] = [x for x in gt.get(field, []) if not any(token in str(x).lower() for token in
                     ("routine lumbar puncture", "csf neurofilament", "genetic testing is required"))]
    note = ("July 2026 review applied end to end: EMG/NCS is the required ALS-specific test; brain and cord MRI and targeted labs exclude mimics; "
            "respiratory function is a recommended safety baseline; genetics is separately offered after counselling; CSF is absent except in five atypical mimic work-ups.")
    if note not in gt.setdefault("key_reasoning_points", []): gt["key_reasoning_points"].append(note)
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = "independent ALS review: targeted CSF/labs, separate optional genetics, EMG diagnostic, respiratory safety baseline, brain+cord MRI"


def revise(case: dict[str, Any]) -> None:
    _rebuild_outputs(case); _revise_actions(case); _clean(case)


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--cases", type=Path, default=DEFAULT_CASES); parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("ALS-*.json")):
        case = json.loads(path.read_text()); before = json.dumps(case, sort_keys=True); revise(case)
        if json.dumps(case, sort_keys=True) != before:
            changed += 1
            if not args.check: path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"ALS cases changed: {changed}")
    if args.check and changed: raise SystemExit(1)


if __name__ == "__main__": main()
