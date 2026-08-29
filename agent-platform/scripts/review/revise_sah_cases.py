"""Apply Reviewer 2's aSAH pathway to every case, without generic carry-over panels."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CASES = ROOT / "data" / "neurobench" / "cases"

LP_CASES = {"SAH-P01", "SAH-P03", "SAH-P06"}
DSA_CASES = {"SAH-M01", "SAH-M03", "SAH-P02"}


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


def _action(
    tool: str,
    params: dict[str, Any],
    text: str,
    finding: str,
    category: str,
) -> dict[str, Any]:
    return {
        "action": text,
        "tool_name": tool,
        "expected_finding": finding,
        "category": category,
        "tool_parameters": params,
        "citation": "[Hoh_2023]",
        "guideline_source": "AHA/ASA aneurysmal subarachnoid hemorrhage guideline 2023",
    }


def _normalize_csf(report: dict[str, Any]) -> dict[str, Any]:
    out = _copy(report)
    old = out.get("special_tests") or {}
    spectro = next(
        (str(value) for key, value in old.items() if "spectro" in key.lower()),
        next((str(value) for key, value in old.items() if "xantho" in key.lower()), "Positive"),
    )
    out["special_tests"] = {"xanthochromia_spectrophotometry": spectro}
    cells = out.get("cell_count") or {}
    first = cells.get("Tube_1_RBC", "reported")
    last = cells.get("Tube_4_RBC", cells.get("last_tube_RBC", "reported"))
    out["interpretation"] = (
        f"First-versus-last tube RBC comparison: tube 1 {first}; tube 4 {last}. "
        f"Protein {out.get('protein', 'reported')}; glucose {out.get('glucose', 'reported')}. "
        f"Spectrophotometric xanthochromia: {spectro}"
    )
    return out


def _rebuild_outputs(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    initial = case["initial_tool_outputs"]
    if cid in LP_CASES:
        if not initial.get("csf"):
            raise ValueError(f"{cid}: conditional LP case has no CSF report")
        initial["csf"] = _normalize_csf(initial["csf"])
    else:
        initial["csf"] = None

    # The CT tool contains only the index NCCT and the subsequent CTA. Fifteen old
    # perfusion outputs had been routed into this bucket and contradicted the reviewed item.
    kept: list[dict[str, Any]] = []
    for row in case["followup_outputs"]:
        tool = row.get("tool_name")
        trigger = row.get("trigger_action", "")
        if tool == "order_ct_scan" and trigger != "request_ct_angiography":
            continue
        if tool == "order_advanced_imaging" and trigger not in {
            "request_transcranial_doppler",
            "request_digital_subtraction_angiography",
        }:
            continue
        if tool in {"analyze_csf", "analyze_eeg"}:
            continue
        kept.append(row)
    case["followup_outputs"] = kept


def _rebuild_actions(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    gt = case["ground_truth"]
    treatment = [row["action"] for row in gt["optimal_actions"] if row.get("tool_name") is None]
    for text in treatment:
        if text not in gt.setdefault("critical_actions", []):
            gt["critical_actions"].append(text)

    replaced = {None, "order_ct_scan", "analyze_csf", "order_advanced_imaging", "interpret_labs"}
    other = [_copy(row) for row in gt["optimal_actions"] if row.get("tool_name") not in replaced]
    for row in other:
        # These are useful management aids, but neither is a mandatory diagnostic test.
        if row.get("tool_name") in {"search_medical_literature", "check_drug_interactions"}:
            row["category"] = "recommended"

    actions = [
        _action(
            "order_ct_scan",
            {"contrast": False, "angiography": False},
            "Obtain an urgent noncontrast head CT as the mandatory first-line study for suspected aneurysmal subarachnoid hemorrhage",
            "Acute subarachnoid blood or, in a late/low-attenuation presentation, a negative or inconclusive index study that triggers the conditional LP pathway",
            "required",
        ),
        _action(
            "order_ct_scan",
            {"contrast": True, "angiography": True},
            "After the noncontrast CT, obtain a separate head-and-neck CT angiogram to localize the culprit aneurysm and plan treatment; CTA does not replace the index NCCT",
            "Culprit aneurysm location, size, neck and branch anatomy, or an angiographically occult pattern requiring selected catheter DSA",
            "required",
        ),
    ]
    if cid in LP_CASES:
        actions.append(_action(
            "analyze_csf",
            {
                "basic": ["cell_count_first_and_last_tube", "protein", "glucose"],
                "paired_serum": True,
                "special_tests": ["xanthochromia_spectrophotometry"],
            },
            "Because the noncontrast CT is negative or inconclusive despite persistent suspicion, perform LP with first-versus-last tube RBC counts, protein, glucose and spectrophotometric xanthochromia",
            "Non-clearing erythrocytes and/or spectrophotometric bilirubin/oxyhemoglobin support SAH while the tube comparison helps distinguish a traumatic tap",
            "required",
        ))
    actions.append(_action(
        "interpret_labs",
        {"panels": ["CBC", "BMP", "coagulation"]},
        "Obtain the condition-specific baseline blood work: CBC, metabolic panel and coagulation studies",
        "Anemia/platelets, sodium and renal function, and PT/INR/aPTT relevant to acute management and invasive procedures; no routine thyroid, inflammatory, autoimmune or paraneoplastic panel",
        "required",
    ))
    if cid in DSA_CASES:
        actions.append(_action(
            "order_advanced_imaging",
            {"modality": "cerebral_angiography"},
            "Use selected catheter digital-subtraction cerebral angiography because this case has CTA-occult/uncertain anatomy or requires definitive endovascular characterization",
            "Definitive six-vessel/aneurysm anatomy and, where applicable, endovascular treatment result; this is not a duplicate CTA or MRA order",
            "recommended",
        ))
    actions.append(_action(
        "order_advanced_imaging",
        {"modality": "transcranial_doppler"},
        "Consider serial transcranial Doppler during the vasospasm-risk window to monitor for vasospasm and delayed cerebral ischemia",
        "Velocity and Lindegaard-ratio trends that support or argue against clinically significant vasospasm; reasonable but not mandatory",
        "optional",
    ))

    # Put the reviewed diagnostic chain first, then retain case-specific complication work-up.
    actions.extend(other)
    for i, row in enumerate(actions, 1):
        row["step"] = i
    gt["optimal_actions"] = actions

    # Enforce the conditional nature of LP rather than merely omitting it silently.
    gt["harmful_tools"] = [row for row in gt.get("harmful_tools", []) if row.get("tool_name") != "analyze_csf"]
    if cid not in LP_CASES:
        gt["harmful_tools"].append({
            "tool_name": "analyze_csf",
            "tool_parameters": {},
            "rationale": "The noncontrast CT already establishes SAH; diagnostic LP adds procedural risk without diagnostic benefit.",
            "citation": "[Hoh_2023]",
        })
        gt["red_herrings"] = [
            row for row in gt.get("red_herrings", [])
            if not str(row.get("field_path", "")).startswith("initial_tool_outputs.csf")
        ]

    banned_modalities = {
        "amyloid_PET", "tau_PET", "FDG_PET", "DaTscan", "MIBG_scan",
        "perfusion_MRI", "MR_spectroscopy", "MR_angiography", "carotid_duplex",
    }
    gt["useless_tools"] = [
        row for row in gt.get("useless_tools", [])
        if not (
            row.get("tool_name") == "order_advanced_imaging"
            and (row.get("tool_parameters") or {}).get("modality") in banned_modalities
        )
    ]
    present = {
        (row.get("tool_parameters") or {}).get("modality")
        for row in gt["useless_tools"] if row.get("tool_name") == "order_advanced_imaging"
    }
    for modality in sorted(banned_modalities - present):
        gt["useless_tools"].append({
            "tool_name": "order_advanced_imaging",
            "tool_parameters": {"modality": modality},
            "rationale": "This modality does not answer the aneurysmal-SAH diagnostic or vasospasm-monitoring question reviewed for this dataset.",
            "citation": "[Hoh_2023]",
        })


def _metadata(case: dict[str, Any]) -> None:
    cid = case["case_id"]
    meta = case["metadata"]
    exemptions = meta.setdefault("panel_required_exemptions", {})
    if cid in LP_CASES:
        exemptions.pop("analyze_csf", None)
    else:
        exemptions["analyze_csf"] = (
            "CSF is conditionally required only after a negative/inconclusive NCCT with persistent suspicion. "
            "This case has diagnostic subarachnoid blood on NCCT, so LP is unnecessary and invasive."
        )
    meta["last_revised"] = "2026-08-10"
    meta["revision_reason"] = (
        "Reviewer 2 aSAH audit: separate first-line NCCT and subsequent CTA; conditional LP only in "
        "SAH-P01/P03/P06 with tube comparison and spectrophotometric xanthochromia; TCD optional; "
        "generic CSF/advanced-imaging panels and CT-perfusion carry-over removed"
    )


def revise(case: dict[str, Any]) -> None:
    _rebuild_outputs(case)
    _rebuild_actions(case)
    _metadata(case)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    changed = 0
    for path in sorted(args.cases.glob("SAH-*.json")):
        case = json.loads(path.read_text())
        before = json.dumps(case, sort_keys=True)
        revise(case)
        if json.dumps(case, sort_keys=True) != before:
            changed += 1
            if not args.check:
                path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"SAH cases changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
