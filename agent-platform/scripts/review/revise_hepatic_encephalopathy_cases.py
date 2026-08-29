"""Apply the remaining Reviewer 2 abdominal-imaging correction for hepatic encephalopathy.

The post-TIPS case already contained a contemporaneous Doppler study, but it was attached to
``order_advanced_imaging`` even though this is abdominal/body imaging, not advanced brain
imaging.  This script moves that existing result to the reachable tool and makes the test an
optional, case-specific action.  It deliberately does not manufacture cross-sectional imaging
for the other hepatic-encephalopathy cases.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"


def revise(case: dict[str, Any]) -> None:
    if case["case_id"] != "HEP-ENC-M06":
        return
    gt = case["ground_truth"]
    for action in gt["optimal_actions"]:
        if action.get("action", "").startswith("TIPS Doppler ultrasound"):
            action.update({
                "action": (
                    "Obtain abdominal Doppler ultrasound to assess TIPS patency because this "
                    "post-TIPS patient has new overt encephalopathy; use it to identify shunt "
                    "stenosis or thrombosis, not as routine brain imaging."
                ),
                "tool_name": "order_body_imaging",
                "expected_finding": "TIPS patency and flow velocity, with any stenosis, thrombosis or recurrent ascites.",
                "category": "optional",
                "tool_parameters": {
                    "study": "pelvis_abdomen_ultrasound",
                    "contrast": False,
                },
                "citation": "[ACG_HE_2026]",
                "guideline_source": "ACG 2026 hepatic encephalopathy guideline",
            })

    for row in case["followup_outputs"]:
        if row.get("trigger_action") != "request_tips_shunt_assessment":
            continue
        row["tool_name"] = "order_body_imaging"
        row["tool_parameters"] = {"study": "pelvis_abdomen_ultrasound", "contrast": False}
        row["output"] = {
            "region": "abdomen",
            "modality": "Doppler ultrasound",
            "contrast": False,
            "findings": [
                {"type": "TIPS shunt", "location": "intrahepatic portosystemic shunt", "description": "Patent and functioning."},
                {"type": "Doppler flow", "location": "main shunt", "description": "Velocity 90 cm/s (reference 90–190 cm/s)."},
                {"type": "Shunt complication", "location": "TIPS", "description": "No stenosis or thrombosis."},
                {"type": "Ascites", "location": "peritoneal cavity", "description": "No recurrent ascites."},
                {"type": "Spleen", "location": "left upper quadrant", "description": "Splenomegaly, compatible with portal hypertension."},
            ],
            "measurements": {"main_shunt_velocity_cm_s": "90"},
            "impression": "Patent TIPS with normal main-shunt velocity. No stenosis, thrombosis or recurrent ascites.",
            "recommended_actions": [],
        }

    # A tool-less action had been treated as a critical action by the earlier audit script.
    gt["critical_actions"] = [x for x in gt.get("critical_actions", []) if not x.startswith("TIPS Doppler ultrasound")]
    case["metadata"]["last_revised"] = "2026-08-10"
    case["metadata"]["revision_reason"] = (
        "Reviewer 2 hepatic-encephalopathy audit: the existing post-TIPS Doppler result is now "
        "reachable through optional abdominal body imaging; no new imaging was authored for other cases."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("HEP-ENC-*.json")):
        case = json.loads(path.read_text())
        before = json.dumps(case, sort_keys=True)
        revise(case)
        if json.dumps(case, sort_keys=True) != before:
            changed += 1
            if not args.check:
                path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"hepatic-encephalopathy cases changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
