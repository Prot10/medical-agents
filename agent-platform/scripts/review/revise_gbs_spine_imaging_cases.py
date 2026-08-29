"""Make Reviewer 2's selective spine-imaging pathway reachable in GBS.

Fifteen GBS cases carried hidden spine-MRI reports under the brain-oriented advanced-imaging
tool, although no case could order them.  We retain only the five cases whose own presentation
has a concrete structural/myelopathic alternative, and expose those existing reports as optional
body imaging.  The remaining generic nerve-root MRIs are removed rather than promoted to a
routine GBS test.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"
SELECTED = {
    "GBS-RM14": "Recent spinal anaesthesia and progressive weakness require exclusion of epidural haematoma, abscess or cauda-equina injury.",
    "GBS-RP16": "Acute lymphoblastic leukaemia with abrupt quadriplegia warrants exclusion of cord or leptomeningeal infiltration alongside peripheral alternatives.",
    "GBS-RS12": "New severe pain and paralysis days after lumbar surgery require urgent exclusion of a postoperative compressive complication.",
    "GBS-RS13": "New ascending paralysis after major trauma requires exclusion of post-traumatic cord injury or compression.",
    "GBS-RS18": "A cervical sensory level, new urinary incontinence and cervical cord signal make a cord mimic a live alternative.",
}


def body_report(report: dict[str, Any]) -> dict[str, Any]:
    # The script is deliberately idempotent: after the first run the report already has the
    # BodyImagingReport shape, including its string-valued measurements.
    if report.get("region") == "spine" and report.get("modality") == "MRI":
        return report
    findings = []
    for item in report.get("findings") or []:
        text = item.get("finding") or item.get("description") or ""
        findings.append({
            "type": item.get("region") or item.get("type") or "spinal MRI finding",
            "location": item.get("region") or item.get("location") or "spine",
            "description": text,
        })
    return {
        "region": "spine",
        "modality": "MRI",
        "contrast": True,
        "findings": findings,
        "measurements": {k: str(v) for k, v in (report.get("quantitative_data") or {}).items()} or None,
        "impression": report.get("impression", ""),
        "recommended_actions": report.get("recommended_actions") or [],
    }


def action(reason: str) -> dict[str, Any]:
    return {
        "action": "Obtain contrast spine MRI only because " + reason,
        "tool_name": "order_body_imaging",
        "expected_finding": "Cord compression, traumatic/postoperative lesion, infection, myelitis or nerve-root enhancement relevant to the stated alternative.",
        "category": "optional",
        "tool_parameters": {"study": "spine_MRI", "contrast": True},
        "citation": "[EAN_PNS_GBS_2023]",
        "guideline_source": "EAN/PNS 2023 Guillain-Barré syndrome guideline",
    }


def revise(case: dict[str, Any]) -> None:
    cid, gt = case["case_id"], case["ground_truth"]
    spine_rows = [x for x in case["followup_outputs"] if x.get("trigger_action") == "request_spine_mri_contrast"]
    case["followup_outputs"] = [x for x in case["followup_outputs"] if x.get("trigger_action") != "request_spine_mri_contrast"]
    gt["optimal_actions"] = [a for a in gt["optimal_actions"] if a.get("tool_name") != "order_body_imaging"]
    if cid in SELECTED:
        if not spine_rows:
            raise ValueError(f"{cid}: selected case has no authored spine-MRI report")
        row = spine_rows[0]
        row["tool_name"] = "order_body_imaging"
        row["tool_parameters"] = {"study": "spine_MRI", "contrast": True}
        row["output"] = body_report(row["output"])
        case["followup_outputs"].append(row)
        gt["optimal_actions"].append(action(SELECTED[cid]))
    for i, item in enumerate(gt["optimal_actions"], 1):
        item["step"] = i
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = (
        "Reviewer 2 GBS audit: spine MRI is optional and limited to five cases with a concrete "
        "cord, traumatic, postoperative or infiltrative alternative; generic hidden MRI reports removed."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("GBS-*.json")):
        case = json.loads(path.read_text())
        before = json.dumps(case, sort_keys=True)
        revise(case)
        if json.dumps(case, sort_keys=True) != before:
            changed += 1
            if not args.check:
                path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"GBS spine-imaging cases changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
