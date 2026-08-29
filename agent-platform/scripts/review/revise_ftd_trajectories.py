"""Rebuild FTD SFT traces around Reviewer 1's optional-imaging pathway."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "training_data" / "gold_trajectories" / "trajectories.jsonl"
CASES = ROOT / "data" / "neurobench" / "cases"


def _pair(name: str, args: dict[str, Any], output: dict[str, Any], thought: str) -> list[dict[str, Any]]:
    return [
        {"role": "assistant", "content": f"<think>\n{thought}\n</think>",
         "tool_calls": [{"type": "function", "function": {"name": name, "arguments": args}}]},
        {"role": "tool", "content": json.dumps(output, indent=2, ensure_ascii=False)},
    ]


def _action(case: dict[str, Any], tool: str, key: str | None = None, value: str | None = None) -> dict[str, Any] | None:
    for row in case["ground_truth"]["optimal_actions"]:
        if row.get("tool_name") != tool: continue
        if key is not None and row.get("tool_parameters", {}).get(key) != value: continue
        return row
    return None


def _output(case: dict[str, Any], tool: str, key: str | None = None, value: str | None = None) -> dict[str, Any]:
    initial_key = {"perform_clinical_assessment": "clinical_assessment", "interpret_labs": "labs",
                   "analyze_brain_mri": "mri", "order_ct_scan": "ct", "analyze_csf": "csf",
                   "order_advanced_imaging": "advanced_imaging", "order_specialized_test": "specialized_test"}.get(tool)
    initial = case["initial_tool_outputs"].get(initial_key) if initial_key else None
    if initial is not None and (key is None or initial.get(key) == value): return initial
    for row in case.get("followup_outputs", []):
        output = row.get("output") or {}
        if row.get("tool_name") == tool and (key is None or output.get(key) == value): return output
    raise ValueError(f"{case['case_id']}: no {tool} output for {key}={value}")


def _clean_final(
    text: str, case: dict[str, Any], *, modalities: set[str], csf: bool,
    specialized: set[str],
) -> str:
    keep_known_gene = case["case_id"] == "FTD-M06"
    lines = []
    for line in text.splitlines():
        lower = line.lower()
        if not csf and ("csf" in lower or "liquor" in lower): continue
        if "fdg" in lower and "FDG_PET" not in modalities: continue
        if "perfusion spect" in lower and "perfusion_SPECT" not in modalities: continue
        if "amyloid pet" in lower and "amyloid_PET" not in modalities: continue
        if "datscan" in lower and "DaTscan" not in modalities: continue
        if "emg" in lower and "emg_ncs" not in specialized: continue
        if "respiratory" in lower and "respiratory_function" not in specialized: continue
        if not keep_known_gene and any(token in lower for token in ("c9orf72", "grn mutation", "mapt p301", "pathogenic expansion")):
            continue
        lines.append(line)
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    primary = case["ground_truth"]["primary_diagnosis"]
    text = re.sub(r"(### Primary Diagnosis\s*\n)[^\n]+", rf"\g<1>{primary}", text, count=1)
    return text or f"### Primary Diagnosis\n{primary}\n\nThe reviewed core pathway supports this diagnosis."


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "ftd": return False
    before = json.dumps(row, sort_keys=True)
    original = row["messages"]
    prefix = [m for m in original if m.get("role") in {"system", "user"}][:2]
    if prefix and prefix[0]["role"] == "system":
        prefix[0] = dict(prefix[0]); content = prefix[0]["content"]
        content = content.replace("amyloid PET, FDG-PET, DaTscan, perfusion MRI",
                                  "amyloid PET, FDG-PET, brain perfusion SPECT, DaTscan, perfusion MRI")
        if "**Clinical assessment**" not in content:
            content = content.replace("  - **Specialized**: Neuropsych battery",
                                      "  - **Clinical assessment**: structured cognitive/behavioural assessment with informant and functional staging\n  - **Specialized**: Neuropsych battery")
        prefix[0]["content"] = content
    final = next((m.get("content", "") for m in reversed(original)
                  if m.get("role") == "assistant" and not m.get("tool_calls")), "")
    messages = list(prefix); case_id = case["case_id"]
    differential = row.get("style") == "differential_reasoned"
    modalities: set[str] = set(); specialized: set[str] = set()

    # The police/ED case needs acute haemorrhage exclusion before the longitudinal dementia work-up.
    if case_id == "FTD-M09":
        ct = _action(case, "order_ct_scan"); assert ct is not None
        messages += _pair("order_ct_scan",
                          {"clinical_context": "acute behavioural presentation in the emergency department; exclude haemorrhage, mass and hydrocephalus", **ct["tool_parameters"]},
                          _output(case, "order_ct_scan"),
                          "The immediate ED question is an acute structural emergency, so non-contrast CT precedes the longitudinal FTD pathway.")

    messages += _pair(
        "perform_clinical_assessment",
        {"clinical_context": "progressive behavioural, executive or language change with collateral history and functional impact", "assessment_type": "cognitive_screen"},
        _output(case, "perform_clinical_assessment"),
        "FTD is a clinical syndrome first: I need informant history, functional staging, behavioural features and a validated cognitive screen before attributing it.",
    )

    # The catch-all tool cannot be called repeatedly in one trace. The FTD-MND case therefore
    # uses its two trace styles to teach the cognitive and motor-neuron questions separately.
    special_type = "emg_ncs" if case_id == "FTD-P08" and differential else "neuropsych_battery"
    messages += _pair(
        "order_specialized_test",
        {"clinical_context": ("document active denervation for the motor-neuron-disease component" if special_type == "emg_ncs" else "define executive, language and social-cognition profile with validated testing"),
         "test_type": special_type},
        _output(case, "order_specialized_test", "test_type", special_type),
        ("This case has objective weakness and fasciculations, so EMG/NCS answers the separate MND question; it is not routine FTD testing."
         if special_type == "emg_ncs" else
         "Validated neuropsychological testing is required to define the affected domains and distinguish psychiatric, Alzheimer and FTD patterns."),
    )
    specialized.add(special_type)

    labs = _action(case, "interpret_labs"); assert labs is not None
    messages += _pair(
        "interpret_labs",
        {"clinical_context": "exclude reversible or contributing causes using the case-targeted FTD laboratory panel",
         "panels": labs["tool_parameters"]["panels"], "patient_age": case["patient"]["demographics"]["age"],
         "patient_sex": case["patient"]["demographics"]["sex"]},
        _output(case, "interpret_labs"),
        "With the clinical phenotype documented, I will now test the baseline metabolic, thyroid, vitamin and inflammatory contributors, adding only case-specific studies.",
    )

    mri = _action(case, "analyze_brain_mri")
    if mri is not None:
        messages += _pair(
            "analyze_brain_mri", {"clinical_context": "structural assessment of suspected frontotemporal degeneration", **mri["tool_parameters"]},
            _output(case, "analyze_brain_mri"),
            "Structural MRI follows the clinical and laboratory assessment to characterize regional atrophy and exclude vascular, mass and hydrocephalic mimics.",
        )
    elif case_id != "FTD-M09":
        ct = _action(case, "order_ct_scan"); assert ct is not None
        messages += _pair(
            "order_ct_scan", {"clinical_context": "structural dementia assessment; MRI unavailable because of severe claustrophobia", "contrast": False},
            _output(case, "order_ct_scan"),
            "MRI is unavailable, so the reviewed alternative is non-contrast CT with its sensitivity limitations stated explicitly.",
        )

    functional = "perfusion_SPECT" if _action(case, "order_advanced_imaging", "modality", "perfusion_SPECT") else "FDG_PET"
    if differential:
        messages += _pair(
            "order_advanced_imaging",
            {"clinical_context": "subtype remains uncertain after clinical assessment, labs and structural imaging", "modality": functional},
            _output(case, "order_advanced_imaging", "modality", functional),
            "The core assessment leaves a subtype question. Functional imaging is optional now; it would have been premature as a first-line test.",
        )
        modalities.add(functional)
    elif (amy := _action(case, "order_advanced_imaging", "modality", "amyloid_PET")) is not None:
        messages += _pair(
            "order_advanced_imaging",
            {"clinical_context": "active Alzheimer-pathology differential after the core FTD assessment", "modality": "amyloid_PET"},
            _output(case, "order_advanced_imaging", "modality", "amyloid_PET"),
            "This is one of the few cases with an explicit Alzheimer-pathology question; amyloid PET is optional and not routine FTD imaging.",
        )
        modalities.add("amyloid_PET")

    csf_action = _action(case, "analyze_csf")
    if csf_action is not None:
        messages += _pair(
            "analyze_csf", {"clinical_context": csf_action["action"], **csf_action["tool_parameters"]},
            _output(case, "analyze_csf"),
            "This HIV-positive patient has a separate CNS-infection question; targeted CSF is required for that reason, not as routine FTD biomarker testing.",
        )

    messages.append({"role": "assistant", "content": _clean_final(
        final, case, modalities=modalities, csf=csf_action is not None, specialized=specialized
    )})
    row["messages"] = messages
    called = [m["tool_calls"][0]["function"]["name"] for m in messages if m.get("tool_calls")]
    row["tools_called"] = list(dict.fromkeys(called)); row["num_tool_calls"] = len(called)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--input", type=Path, default=DEFAULT_INPUT); parser.add_argument("--check", action="store_true")
    args = parser.parse_args(); cases = {p.stem: json.loads(p.read_text()) for p in CASES.glob("FTD-*.json")}
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]; changed = 0
    for row in rows:
        if row.get("condition") == "ftd": changed += revise(row, cases[row["case_id"]])
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    print(f"FTD trajectories changed: {changed}")
    if args.check and changed: raise SystemExit(1)
    if not args.check: args.input.write_text(rendered)


if __name__ == "__main__": main()
