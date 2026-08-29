"""Rebuild Parkinson SFT traces around the independently reviewed case pathways."""

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
        if row.get("tool_name") != tool:
            continue
        if key is not None and row.get("tool_parameters", {}).get(key) != value:
            continue
        return row
    return None


def _output(case: dict[str, Any], tool: str, key: str | None = None, value: str | None = None) -> dict[str, Any]:
    initial_key = {
        "analyze_brain_mri": "mri", "order_ct_scan": "ct", "interpret_labs": "labs",
        "order_advanced_imaging": "advanced_imaging", "order_specialized_test": "specialized_test",
        "search_medical_literature": "literature_search", "check_drug_interactions": "drug_interactions",
        "order_cardiac_monitoring": "cardiac_monitoring",
    }.get(tool)
    initial = case["initial_tool_outputs"].get(initial_key) if initial_key else None
    if initial is not None and (key is None or initial.get(key) == value):
        return initial
    for row in case.get("followup_outputs", []):
        output = row.get("output") or {}
        if row.get("tool_name") == tool and (key is None or output.get(key) == value):
            return output
    raise ValueError(f"{case['case_id']}: no {tool} output for {key}={value}")


def _medications(case: dict[str, Any]) -> list[str]:
    meds = case["patient"].get("clinical_history", {}).get("medications", [])
    return [str(x.get("drug")) for x in meds if isinstance(x, dict) and x.get("drug")]


def _conditions(case: dict[str, Any]) -> list[str]:
    history = case["patient"].get("clinical_history", {}).get("past_medical_history", [])
    return [str(x) for x in history[:8]]


def _clean_final(text: str, case: dict[str, Any], called: list[tuple[str, str | None]]) -> str:
    tools = {x[0] for x in called}
    modalities = {x[1] for x in called if x[0] == "order_advanced_imaging"}
    special = {x[1] for x in called if x[0] == "order_specialized_test"}
    lines = []
    for line in text.splitlines():
        low = line.lower()
        if any(term in low for term in ("formal autonomic testing", "autonomic testing showed", "tilt-table", "tilt table")):
            continue
        if "eeg" in low or re.search(r"\becg\b", low):
            continue
        if "lab" in low and "interpret_labs" not in tools:
            continue
        if "mri" in low and "analyze_brain_mri" not in tools:
            continue
        if "ct" in low and case["case_id"] == "PD-S06" and "order_ct_scan" not in tools:
            continue
        if "datscan" in low and "DaTscan" not in modalities:
            continue
        if "mibg" in low and "MIBG_scan" not in modalities:
            continue
        if ("fdg" in low or "hypometab" in low) and "FDG_PET" not in modalities:
            continue
        if ("tau pet" in low or "tau-pet" in low):
            continue
        if "polysom" in low and "polysomnography" not in special:
            continue
        if "neuropsych" in low and "neuropsych_battery" not in special:
            continue
        if any(gene in low for gene in ("prkn", "pink1", "lrrk2", "gba1", "snca")) and "genetic_panel:PD" not in special:
            continue
        lines.append(line)
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    primary = case["ground_truth"]["primary_diagnosis"]
    out = re.sub(r"(### Primary Diagnosis\s*\n)[^\n]+", rf"\g<1>{primary}", out, count=1)
    if case["case_id"] == "PD-S06":
        out = out.replace("brain MRI", "non-contrast head CT").replace("MRI", "CT")
    return out or f"### Primary Diagnosis\n{primary}\n\nThe reviewed clinical and structural pathway supports this diagnosis."


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "parkinsons":
        return False
    before = json.dumps(row, sort_keys=True)
    original = row["messages"]
    prefix = [dict(m) for m in original if m.get("role") in {"system", "user"}][:2]
    final = next((m.get("content", "") for m in reversed(original)
                  if m.get("role") == "assistant" and not m.get("tool_calls")), "")
    messages = list(prefix)
    called: list[tuple[str, str | None]] = []
    differential = row.get("style") == "differential_reasoned"

    mri = _action(case, "analyze_brain_mri")
    if mri:
        messages += _pair(
            "analyze_brain_mri",
            {"clinical_context": "exclude secondary or atypical structural causes of the parkinsonian syndrome", **mri["tool_parameters"]},
            _output(case, "analyze_brain_mri"),
            "Parkinson disease is diagnosed clinically. Structural MRI is being used to exclude another parkinsonian syndrome, not to prove idiopathic PD.",
        )
        called.append(("analyze_brain_mri", None))
    else:
        ct = _action(case, "order_ct_scan")
        assert ct is not None
        messages += _pair(
            "order_ct_scan",
            {"clinical_context": "structural assessment of parkinsonism; MRI unavailable because of severe claustrophobia", "contrast": False},
            _output(case, "order_ct_scan"),
            "MRI is unavailable in this patient, so the reviewed alternative is non-contrast CT and its lower sensitivity must remain explicit.",
        )
        called.append(("order_ct_scan", None))

    labs = _action(case, "interpret_labs")
    if labs:
        dem = case["patient"]["demographics"]
        messages += _pair(
            "interpret_labs",
            {"clinical_context": labs["action"], "panels": labs["tool_parameters"]["panels"],
             "patient_age": dem["age"], "patient_sex": dem["sex"]},
            _output(case, "interpret_labs"),
            "There is no routine PD panel; these tests answer the specific metabolic, toxic, young-onset or pretreatment issue in this case.",
        )
        called.append(("interpret_labs", None))

    interaction = _action(case, "check_drug_interactions")
    if interaction:
        args = dict(interaction.get("tool_parameters", {}))
        args.setdefault("current_medications", _medications(case))
        args.setdefault("patient_conditions", _conditions(case))
        messages += _pair(
            "check_drug_interactions", args, _output(case, "check_drug_interactions"),
            "Medication review is clinically relevant because dopamine blockers, absorption interactions and hypotensive drugs can alter this presentation or its treatment.",
        )
        called.append(("check_drug_interactions", None))

    literature = _action(case, "search_medical_literature")
    if literature:
        args = dict(literature.get("tool_parameters", {})); args.setdefault("max_results", 3)
        messages += _pair(
            "search_medical_literature", args, _output(case, "search_medical_literature"),
            "I will check the diagnostic criteria relevant to the active PD-versus-mimic question rather than treating an imaging biomarker as the diagnosis.",
        )
        called.append(("search_medical_literature", None))

    # The catch-all specialized tool cannot be repeated in a single trace.  Use the two styles
    # to expose different justified questions, prioritizing mandatory pre-DBS neuropsychology.
    special: str | None = None
    if _action(case, "order_specialized_test", "test_type", "neuropsych_battery") and (
        case["case_id"] == "PD-RP04" or not differential
    ):
        special = "neuropsych_battery"
    elif differential and _action(case, "order_specialized_test", "test_type", "genetic_panel:PD"):
        special = "genetic_panel:PD"
    elif _action(case, "order_specialized_test", "test_type", "polysomnography"):
        special = "polysomnography"
    elif _action(case, "order_specialized_test", "test_type", "neuropsych_battery"):
        special = "neuropsych_battery"
    if special:
        context = {
            "neuropsych_battery": "active cognitive impairment or formal DBS candidacy question",
            "polysomnography": "reported dream enactment with an unresolved REM sleep behaviour disorder question",
            "genetic_panel:PD": "young-onset disease after genetic counselling; result is not required for diagnosis",
        }[special]
        messages += _pair(
            "order_specialized_test", {"clinical_context": context, "test_type": special},
            _output(case, "order_specialized_test", "test_type", special),
            ("This is the required cognitive safety assessment before DBS." if case["case_id"] == "PD-RP04" else
             "This is a selected optional study tied to a live question in this case, not routine Parkinson testing."),
        )
        called.append(("order_specialized_test", special))

    modality: str | None = None
    if differential and _action(case, "order_advanced_imaging", "modality", "MIBG_scan"):
        modality = "MIBG_scan"
    elif _action(case, "order_advanced_imaging", "modality", "DaTscan"):
        modality = "DaTscan"
    elif _action(case, "order_advanced_imaging", "modality", "FDG_PET"):
        modality = "FDG_PET"
    elif _action(case, "order_advanced_imaging", "modality", "MIBG_scan"):
        modality = "MIBG_scan"
    if modality:
        messages += _pair(
            "order_advanced_imaging",
            {"clinical_context": "optional supportive study for the live degenerative or synucleinopathy differential after clinical and structural assessment", "modality": modality},
            _output(case, "order_advanced_imaging", "modality", modality),
            ("DaT imaging can support nigrostriatal degeneration here, but it cannot distinguish PD from MSA or PSP."
             if modality == "DaTscan" else
             "This supportive biomarker is optional and cannot replace the clinical syndrome and chronology."),
        )
        called.append(("order_advanced_imaging", modality))

    monitor = _action(case, "order_cardiac_monitoring")
    if monitor and differential:
        messages += _pair(
            "order_cardiac_monitoring",
            {"clinical_context": "recurrent syncope with a separate WPW/arrhythmia differential", **monitor["tool_parameters"]},
            _output(case, "order_cardiac_monitoring"),
            "This is a strong case-specific cardiac exception for recurrent syncope and WPW, not a Parkinson diagnostic test.",
        )
        called.append(("order_cardiac_monitoring", None))

    messages.append({"role": "assistant", "content": _clean_final(final, case, called)})
    row["messages"] = messages
    names = [name for name, _ in called]
    row["tools_called"] = list(dict.fromkeys(names))
    row["num_tool_calls"] = len(names)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cases = {p.stem: json.loads(p.read_text()) for p in CASES.glob("PD-*.json")}
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    changed = 0
    for row in rows:
        if row.get("condition") == "parkinsons":
            changed += revise(row, cases[row["case_id"]])
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    print(f"Parkinson trajectories changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)
    if not args.check:
        args.input.write_text(rendered)


if __name__ == "__main__":
    main()
