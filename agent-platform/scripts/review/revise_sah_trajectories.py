"""Rebuild aSAH traces around NCCT-first, separate CTA and conditional LP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "training_data" / "gold_trajectories" / "trajectories.jsonl"
CASES = ROOT / "data" / "neurobench" / "cases"


def _pair(name: str, args: dict[str, Any], output: dict[str, Any], thought: str) -> list[dict[str, Any]]:
    return [
        {
            "role": "assistant",
            "content": f"<think>\n{thought}\n</think>",
            "tool_calls": [{"type": "function", "function": {"name": name, "arguments": args}}],
        },
        {"role": "tool", "content": json.dumps(output, indent=2, ensure_ascii=False)},
    ]


def _action(case: dict[str, Any], tool: str, modality: str | None = None) -> dict[str, Any] | None:
    for row in case["ground_truth"]["optimal_actions"]:
        if row.get("tool_name") != tool:
            continue
        if modality is not None and (row.get("tool_parameters") or {}).get("modality") != modality:
            continue
        return row
    return None


def _output(case: dict[str, Any], tool: str, discriminator: str | None = None) -> dict[str, Any]:
    if tool == "order_ct_scan":
        if discriminator == "cta":
            row = next(x for x in case["followup_outputs"] if x.get("trigger_action") == "request_ct_angiography")
            return row["output"]
        return case["initial_tool_outputs"]["ct"]
    if tool == "order_advanced_imaging":
        trigger = {
            "transcranial_doppler": "request_transcranial_doppler",
            "cerebral_angiography": "request_digital_subtraction_angiography",
        }[str(discriminator)]
        return next(x["output"] for x in case["followup_outputs"] if x.get("trigger_action") == trigger)
    key = {
        "interpret_labs": "labs",
        "analyze_ecg": "ecg",
        "analyze_csf": "csf",
        "analyze_brain_mri": "mri",
        "order_echocardiogram": "echo",
        "order_cardiac_monitoring": "cardiac_monitoring",
        "search_medical_literature": "literature_search",
        "check_drug_interactions": "drug_interactions",
    }[tool]
    initial = case["initial_tool_outputs"].get(key)
    if initial:
        if isinstance(initial, dict) and tool in {"search_medical_literature", "check_drug_interactions"}:
            # These slots may be keyed collections rather than a single report.
            if "query" not in initial and "proposed" not in initial:
                return next(iter(initial.values()))
        return initial
    return next(x["output"] for x in case["followup_outputs"] if x.get("tool_name") == tool)


def _has_output(case: dict[str, Any], tool: str) -> bool:
    try:
        _output(case, tool)
    except (StopIteration, KeyError, TypeError):
        return False
    return True


def _call(
    messages: list[dict[str, Any]],
    calls: list[str],
    case: dict[str, Any],
    tool: str,
    args: dict[str, Any],
    thought: str,
    discriminator: str | None = None,
) -> None:
    messages.extend(_pair(tool, args, _output(case, tool, discriminator), thought))
    calls.append(tool)


def _final(case: dict[str, Any], lp: bool) -> str:
    conditional = (
        "The index NCCT is non-diagnostic, so the CSF tube comparison and spectrophotometric "
        "xanthochromia are decisive in this case."
        if lp else
        "The index NCCT is diagnostic, so lumbar puncture would add risk without diagnostic value."
    )
    return (
        f"### Primary Diagnosis\n{case['ground_truth']['primary_diagnosis']}\n\n"
        "The acute presentation and reviewed vascular work-up support subarachnoid hemorrhage. "
        "Noncontrast head CT is the first-line study; CTA is a separate subsequent aneurysm-localization study, not a substitute. "
        f"{conditional} Serial TCD is optional surveillance rather than a mandatory diagnostic test."
    )


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "subarachnoid_hemorrhage":
        return False
    before = json.dumps(row, sort_keys=True)
    original = row["messages"]
    messages = [dict(x) for x in original if x.get("role") in {"system", "user"}][:2]
    calls: list[str] = []
    differential = row.get("style") == "differential_reasoned"
    lp = _action(case, "analyze_csf") is not None

    ncct = _action(case, "order_ct_scan")
    assert ncct
    if not differential or lp:
        _call(
            messages, calls, case, "order_ct_scan",
            {"clinical_context": ncct["action"], "contrast": False, "angiography": False},
            "I will start with the mandatory noncontrast head CT. Contrast-enhanced CT or CTA cannot substitute for this hemorrhage-detection step.",
        )
    else:
        cta = next(
            x for x in case["ground_truth"]["optimal_actions"]
            if x.get("tool_name") == "order_ct_scan" and (x.get("tool_parameters") or {}).get("angiography")
        )
        _call(
            messages, calls, case, "order_ct_scan",
            {"clinical_context": cta["action"], "contrast": True, "angiography": True},
            "The first-line NCCT has already established SAH in this branch. I will now order the distinct subsequent CTA to localize the aneurysm and guide treatment; it is not the initial diagnostic scan.",
            "cta",
        )

    labs = _action(case, "interpret_labs")
    assert labs
    dem = case["patient"]["demographics"]
    _call(
        messages, calls, case, "interpret_labs",
        {
            "clinical_context": labs["action"],
            "panels": ["CBC", "BMP", "coagulation"],
            "patient_age": dem["age"],
            "patient_sex": dem["sex"],
        },
        "The reviewed baseline panel is limited to CBC, metabolic and coagulation studies; thyroid, inflammatory, autoimmune and paraneoplastic panels do not belong in routine aSAH diagnosis.",
    )

    ecg = _action(case, "analyze_ecg")
    if ecg:
        _call(
            messages, calls, case, "analyze_ecg", {"clinical_context": ecg["action"]},
            "An ECG is justified here for neurogenic myocardial injury and acute-management risk, not as a test that diagnoses SAH.",
        )

    if lp:
        csf = _action(case, "analyze_csf")
        assert csf
        _call(
            messages, calls, case, "analyze_csf",
            {"clinical_context": csf["action"], "special_tests": ["xanthochromia_spectrophotometry"]},
            "Because this case remains suspicious after a negative or inconclusive NCCT, LP is conditionally required. I need first-versus-last tube RBC counts, protein, glucose and spectrophotometric xanthochromia—not a neuroimmunology or infection panel.",
        )

    if differential:
        modality = "cerebral_angiography" if _action(case, "order_advanced_imaging", "cerebral_angiography") else "transcranial_doppler"
        adv = _action(case, "order_advanced_imaging", modality)
        assert adv
        thought = (
            "This selected case needs catheter DSA because CTA is occult/uncertain or definitive endovascular anatomy is required. This is not duplicate CTA/MRA billing."
            if modality == "cerebral_angiography" else
            "Optional TCD is the retained surveillance study for vasospasm and delayed cerebral ischemia; it is reasonable, not mandatory."
        )
        _call(
            messages, calls, case, "order_advanced_imaging",
            {"clinical_context": adv["action"], "modality": modality}, thought, modality,
        )

        mri = _action(case, "analyze_brain_mri")
        if mri and _has_output(case, "analyze_brain_mri"):
            _call(
                messages, calls, case, "analyze_brain_mri",
                {"clinical_context": mri["action"], "protocol": "standard", "contrast": False},
                "MRI is retained only for this case-specific competing lesion or subacute blood question, not as routine first-line aSAH imaging.",
            )
        echo = _action(case, "order_echocardiogram")
        if echo and _has_output(case, "order_echocardiogram"):
            _call(
                messages, calls, case, "order_echocardiogram",
                {"clinical_context": echo["action"], "echo_type": "TTE"},
                "The cardiac findings justify a targeted TTE for stress cardiomyopathy or ventricular dysfunction.",
            )
        monitor = _action(case, "order_cardiac_monitoring")
        if monitor and _has_output(case, "order_cardiac_monitoring"):
            _call(
                messages, calls, case, "order_cardiac_monitoring",
                {"clinical_context": monitor["action"], "monitor_type": "telemetry"},
                "Telemetry addresses acute arrhythmic complications of SAH and its treatment.",
            )
        literature = _action(case, "search_medical_literature")
        if literature and _has_output(case, "search_medical_literature"):
            _call(
                messages, calls, case, "search_medical_literature",
                {"query": (literature.get("tool_parameters") or {}).get("query", "2023 aneurysmal SAH management guideline"), "max_results": 3},
                "A concise guideline check can support management details, but it is not a required diagnostic investigation.",
            )
        drug = _action(case, "check_drug_interactions")
        if drug and _has_output(case, "check_drug_interactions"):
            meds = case["patient"]["clinical_history"].get("medications", [])
            current = [str(x.get("drug", x)) if isinstance(x, dict) else str(x) for x in meds]
            _call(
                messages, calls, case, "check_drug_interactions",
                {"drug": "nimodipine", "current_medications": current},
                "Nimodipine interaction review is a recommended management-safety step, not evidence for the diagnosis.",
            )

    messages.append({"role": "assistant", "content": _final(case, lp)})
    row["messages"] = messages
    row["tools_called"] = calls
    row["num_tool_calls"] = len(calls)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cases = {path.stem: json.loads(path.read_text()) for path in CASES.glob("SAH-*.json")}
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    changed = sum(
        revise(row, cases[row["case_id"]])
        for row in rows if row.get("condition") == "subarachnoid_hemorrhage"
    )
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    print(f"SAH trajectories changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)
    if not args.check:
        args.input.write_text(rendered)


if __name__ == "__main__":
    main()
