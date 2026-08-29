"""Rebuild MS SFT traces around the reviewed conditional diagnostic pathway."""

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


def _actions(case: dict[str, Any], tool: str) -> list[dict[str, Any]]:
    return [x for x in case["ground_truth"]["optimal_actions"] if x.get("tool_name") == tool]


def _output(case: dict[str, Any], tool: str, test_type: str | None = None) -> dict[str, Any]:
    key = {
        "analyze_brain_mri": "mri", "analyze_csf": "csf", "interpret_labs": "labs",
        "order_specialized_test": "specialized_test", "order_body_imaging": "body_imaging",
        "search_medical_literature": "literature_search", "check_drug_interactions": "drug_interactions",
    }.get(tool)
    initial = case["initial_tool_outputs"].get(key) if key else None
    if initial is not None and (not test_type or initial.get("test_type") == test_type):
        return initial
    for row in case["followup_outputs"]:
        out = row.get("output") or {}
        if row.get("tool_name") != tool:
            continue
        if test_type and out.get("test_type") != test_type:
            continue
        return out
    raise ValueError(f"{case['case_id']}: missing output for {tool} {test_type or ''}")


def _clean_final(text: str, case: dict[str, Any], called: set[str], specialty: str | None) -> str:
    lines = []
    for line in text.splitlines():
        low = line.lower()
        if "eeg" in low or "ecg" in low:
            continue
        if ("lumbar puncture" in low or "csf" in low or "oligoclonal" in low) and "analyze_csf" not in called:
            continue
        if ("oct" in low or "optical coherence" in low) and specialty != "optical_coherence_tomography":
            continue
        if ("vep" in low or "visual evoked" in low) and specialty != "vep":
            continue
        lines.append(line.replace("McDonald 2017", "2024 revised McDonald"))
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    primary = case["ground_truth"]["primary_diagnosis"]
    out = re.sub(r"(### Primary Diagnosis\s*\n)[^\n]+", rf"\g<1>{primary}", out, count=1)
    return out or f"### Primary Diagnosis\n{primary}\n\nThe clinical and reviewed brain/cord MRI pathway supports this assessment."


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "multiple_sclerosis":
        return False
    before = json.dumps(row, sort_keys=True)
    original = row["messages"]
    differential = row.get("style") == "differential_reasoned"
    messages = [dict(x) for x in original if x.get("role") in {"system", "user"}][:2]
    final = next((x.get("content", "") for x in reversed(original)
                  if x.get("role") == "assistant" and not x.get("tool_calls")), "")
    calls: list[str] = []
    specialty: str | None = None

    mri = _actions(case, "analyze_brain_mri")[0]
    messages += _pair(
        "analyze_brain_mri", {"clinical_context": mri["action"], **mri["tool_parameters"]},
        _output(case, "analyze_brain_mri"),
        "MS is a clinical-radiological diagnosis. I need a dedicated brain MS protocol, using gadolinium when appropriate, to assess typical topographies and active versus inactive lesions.",
    )
    calls.append("analyze_brain_mri")

    spine = _actions(case, "order_body_imaging")[0]
    messages += _pair(
        "order_body_imaging", {"clinical_context": spine["action"], **spine["tool_parameters"]},
        _output(case, "order_body_imaging"),
        "The reviewers explicitly require brain and cord coverage. Cervical/thoracic MS-protocol MRI is a separately scored study and helps distinguish short peripheral lesions from longitudinally extensive mimics.",
    )
    calls.append("order_body_imaging")

    labs = _actions(case, "interpret_labs")[0]
    dem = case["patient"]["demographics"]
    messages += _pair(
        "interpret_labs", {"clinical_context": labs["action"], "panels": labs["tool_parameters"]["panels"],
                           "patient_age": dem["age"], "patient_sex": dem["sex"]},
        _output(case, "interpret_labs"),
        "Blood tests do not confirm MS. This required panel excludes common metabolic, inflammatory, endocrine, nutritional and infectious mimics; AQP4/MOG are included only when this phenotype is atypical.",
    )
    calls.append("interpret_labs")

    csf = _actions(case, "analyze_csf")[0]
    if differential and csf["category"] == "recommended":
        messages += _pair(
            "analyze_csf", {"clinical_context": csf["action"],
                            "special_tests": csf["tool_parameters"]["special_tests"]},
            _output(case, "analyze_csf"),
            "The clinical/MRI picture remains equivocal or atypical, so CSF now answers a real adjudication question. It is conditional—not a universal requirement—and imaging has been reviewed first for mass-effect safety.",
        )
        calls.append("analyze_csf")

    specialized = _actions(case, "order_specialized_test")
    if specialized:
        # The platform contract forbids repeating one tool in a trace.  Complementary
        # styles therefore demonstrate OCT versus VEP where both are justified.
        choices = {x["tool_parameters"]["test_type"]: x for x in specialized}
        specialty = ("vep" if differential and "vep" in choices else
                     "optical_coherence_tomography" if "optical_coherence_tomography" in choices else None)
        if specialty:
            action = choices[specialty]
            rationale = ("This presentation contains a specific optic-neuritis question, so OCT is a targeted optional measure of optic-nerve injury—not a blanket MS panel."
                         if specialty == "optical_coherence_tomography" else
                         "This optic or equivocal-dissemination presentation gives VEP a specific question: objective optic-pathway demyelination. It is optional, not routine in every MS case.")
            messages += _pair(
                "order_specialized_test", {"clinical_context": action["action"], "test_type": specialty},
                _output(case, "order_specialized_test", specialty), rationale,
            )
            calls.append("order_specialized_test")

    for tool in ("search_medical_literature", "check_drug_interactions"):
        actions = _actions(case, tool)
        if not actions:
            continue
        action = actions[0]
        if action.get("category") not in {"required", "recommended"}:
            continue
        if tool == "search_medical_literature":
            args = dict(action.get("tool_parameters", {})); args.setdefault("query", "2024 revised McDonald criteria multiple sclerosis"); args.setdefault("max_results", 3)
            thought = "I will verify the current diagnostic and disease-modifying-therapy framework rather than rely on the superseded 2017 criteria."
        else:
            args = {
                "drug": "proposed MS disease-modifying therapy",
                "current_medications": [str(x.get("drug", x)) if isinstance(x, dict) else str(x)
                                        for x in case["patient"]["clinical_history"].get("medications", [])],
            }
            thought = "Before recommending a disease-modifying therapy, I need the patient-specific contraindication and interaction check."
        messages += _pair(tool, args, _output(case, tool), thought)
        calls.append(tool)

    messages.append({"role": "assistant", "content": _clean_final(final, case, set(calls), specialty)})
    row["messages"] = messages
    row["tools_called"] = list(dict.fromkeys(calls))
    row["num_tool_calls"] = len(calls)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cases = {p.stem: json.loads(p.read_text()) for p in CASES.glob("MS-RR-*.json")}
    rows = [json.loads(x) for x in args.input.read_text().splitlines() if x.strip()]
    changed = sum(revise(row, cases[row["case_id"]]) for row in rows if row.get("condition") == "multiple_sclerosis")
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    print(f"Multiple-sclerosis trajectories changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)
    if not args.check:
        args.input.write_text(rendered)


if __name__ == "__main__":
    main()
