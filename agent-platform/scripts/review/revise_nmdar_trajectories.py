"""Rebuild anti-NMDAR traces with paired antibodies and tailored tumour screening."""

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
        {"role": "assistant", "content": f"<think>\n{thought}\n</think>",
         "tool_calls": [{"type": "function", "function": {"name": name, "arguments": args}}]},
        {"role": "tool", "content": json.dumps(output, indent=2, ensure_ascii=False)},
    ]


def _actions(case: dict[str, Any], tool: str) -> list[dict[str, Any]]:
    return [x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == tool]


def _output(case: dict[str, Any], tool: str, discriminator: str | None = None) -> dict[str, Any]:
    if tool == "analyze_eeg" and discriminator == "continuous_icu":
        return next(
            x["output"] for x in case["followup_outputs"]
            if x.get("tool_name") == tool and (x.get("tool_parameters") or {}).get("eeg_type") == discriminator
        )
    key = {
        "analyze_brain_mri": "mri", "analyze_csf": "csf", "analyze_eeg": "eeg",
        "interpret_labs": "labs", "order_body_imaging": "body_imaging",
        "search_medical_literature": "literature_search",
        "check_drug_interactions": "drug_interactions",
    }[tool]
    initial = case["initial_tool_outputs"].get(key)
    if initial:
        if tool in {"search_medical_literature", "check_drug_interactions"}:
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


def _call(messages: list[dict[str, Any]], calls: list[str], case: dict[str, Any],
          tool: str, args: dict[str, Any], thought: str, discriminator: str | None = None) -> None:
    messages.extend(_pair(tool, args, _output(case, tool, discriminator), thought))
    calls.append(tool)


def _final(case: dict[str, Any]) -> str:
    primary = case["ground_truth"]["primary_diagnosis"]
    study = _actions(case, "order_body_imaging")[0]["tool_parameters"]["study"]
    return (
        f"### Primary Diagnosis\n{primary}\n\n"
        "The subacute neuropsychiatric syndrome, seizures/movement disorder or autonomic features, EEG, "
        "and paired serum-CSF evaluation support the diagnosis. A normal or nonspecific brain MRI does not exclude it. "
        f"Tumour screening was tailored to this patient's age and sex ({study}) rather than applying blanket whole-body CT. "
        "Serum anti-GluN1 is never interpreted without the CSF result."
    )


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "autoimmune_encephalitis_nmdar":
        return False
    before = json.dumps(row, sort_keys=True)
    messages = [dict(x) for x in row["messages"] if x.get("role") in {"system", "user"}][:2]
    calls: list[str] = []
    differential = row.get("style") == "differential_reasoned"

    mri = _actions(case, "analyze_brain_mri")[0]
    _call(
        messages, calls, case, "analyze_brain_mri",
        {"clinical_context": mri["action"], "protocol": "standard", "contrast": True},
        "MRI is required mainly to exclude HSV, structural disease and overlapping demyelination. I will not treat a normal scan as evidence against anti-NMDAR encephalitis.",
    )
    csf = _actions(case, "analyze_csf")[0]
    _call(
        messages, calls, case, "analyze_csf",
        {"clinical_context": csf["action"],
         "special_tests": ["oligoclonal_bands", "IgG_index", "HSV_PCR", "NMDAR_antibodies"]},
        "CSF must include basic indices, HSV PCR, intrathecal inflammation and the cell-based IgG anti-GluN1 assay. The antibody result must be paired with serum, not replaced by it.",
    )

    eeg_actions = _actions(case, "analyze_eeg")
    use_continuous = differential and any(
        (x.get("tool_parameters") or {}).get("eeg_type") == "continuous_icu" for x in eeg_actions
    )
    eeg_type = "continuous_icu" if use_continuous else "routine"
    eeg = next(x for x in eeg_actions if (x.get("tool_parameters") or {}).get("eeg_type") == eeg_type)
    _call(
        messages, calls, case, "analyze_eeg",
        {"clinical_context": eeg["action"], "eeg_type": eeg_type},
        (
            "This case has severe encephalopathy or subclinical seizures, so continuous ICU EEG is a justified escalation; I will assess seizure burden and extreme delta brush."
            if use_continuous else
            "A routine EEG is the baseline study for encephalopathy, seizures and extreme delta brush; continuous monitoring is not automatic in every patient."
        ),
        eeg_type if use_continuous else None,
    )

    labs = _actions(case, "interpret_labs")[0]
    dem = case["patient"]["demographics"]
    _call(
        messages, calls, case, "interpret_labs",
        {"clinical_context": labs["action"], "panels": labs["tool_parameters"]["panels"],
         "patient_age": dem["age"], "patient_sex": dem["sex"]},
        "The serum work-up includes systemic, thyroid, inflammatory and alternative neuronal antibodies. Serum anti-GluN1 can mislead alone, so I will interpret it only against CSF.",
    )
    body = _actions(case, "order_body_imaging")[0]
    _call(
        messages, calls, case, "order_body_imaging",
        {"clinical_context": body["action"], **body["tool_parameters"]},
        "Occult-neoplasm screening is required once the syndrome is recognised, but its scope must follow age and sex: pelvic/abdominal imaging in women, selected testicular imaging in younger men, or broader imaging when the context supports it.",
    )

    if differential:
        literature = _actions(case, "search_medical_literature")
        if literature and _has_output(case, "search_medical_literature"):
            action = literature[0]
            _call(
                messages, calls, case, "search_medical_literature",
                {"query": (action.get("tool_parameters") or {}).get("query", "anti-NMDAR encephalitis treatment Graus 2016"), "max_results": 3},
                "A focused evidence check supports treatment sequencing but is not a diagnostic substitute.",
            )
        drug = _actions(case, "check_drug_interactions")
        if drug and _has_output(case, "check_drug_interactions"):
            meds = case["patient"]["clinical_history"].get("medications", [])
            current = [str(x.get("drug", x)) if isinstance(x, dict) else str(x) for x in meds]
            _call(
                messages, calls, case, "check_drug_interactions",
                {"drug": "methylprednisolone", "current_medications": current},
                "Immunotherapy and antipsychotic safety review is useful management support, not evidence for the diagnosis.",
            )

    messages.append({"role": "assistant", "content": _final(case)})
    row["messages"] = messages
    row["tools_called"] = calls
    row["num_tool_calls"] = len(calls)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cases = {path.stem: json.loads(path.read_text()) for path in CASES.glob("NMDAR-*.json")}
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    changed = sum(
        revise(row, cases[row["case_id"]])
        for row in rows if row.get("condition") == "autoimmune_encephalitis_nmdar"
    )
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    print(f"NMDAR trajectories changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)
    if not args.check:
        args.input.write_text(rendered)


if __name__ == "__main__":
    main()
