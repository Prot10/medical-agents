"""Rebuild Alzheimer SFT traces around the reviewed diagnostic sequence.

The old traces taught exactly the behaviour Reviewer 1 asked us to remove: no structured
clinical-assessment call, routine dual CSF/PET confirmation, and broad assay spellings.  This
migration keeps each trace's original system/user prompt and final assessment, but replaces the
tool sequence and observations with the reviewed case outputs in this order:

clinical/informant assessment -> neuropsychology -> labs -> MRI (or CT) -> optional subtype
imaging -> one biomarker route -> narrowly justified optional studies.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "training_data" / "gold_trajectories" / "trajectories.jsonl"
CASES = ROOT / "data" / "neurobench" / "cases"


def _pair(name: str, arguments: dict[str, Any], output: dict[str, Any], thought: str) -> list[dict[str, Any]]:
    return [
        {
            "role": "assistant",
            "content": f"<think>\n{thought}\n</think>",
            "tool_calls": [{"type": "function", "function": {"name": name, "arguments": arguments}}],
        },
        {"role": "tool", "content": json.dumps(output, indent=2, ensure_ascii=False)},
    ]


def _action(case: dict[str, Any], tool: str, *, key: str | None = None, value: str | None = None) -> dict[str, Any] | None:
    for row in case["ground_truth"]["optimal_actions"]:
        if row.get("tool_name") != tool:
            continue
        if key is not None and row.get("tool_parameters", {}).get(key) != value:
            continue
        return row
    return None


def _output(case: dict[str, Any], tool: str, *, key: str | None = None, value: str | None = None) -> dict[str, Any]:
    initial_key = {
        "perform_clinical_assessment": "clinical_assessment",
        "interpret_labs": "labs", "analyze_brain_mri": "mri", "order_ct_scan": "ct",
        "analyze_csf": "csf", "analyze_eeg": "eeg",
        "order_advanced_imaging": "advanced_imaging",
        "order_specialized_test": "specialized_test",
    }.get(tool)
    initial = case["initial_tool_outputs"].get(initial_key) if initial_key else None
    if initial is not None:
        if key is None or initial.get(key) == value:
            return initial
    for row in case.get("followup_outputs", []):
        if row.get("tool_name") != tool:
            continue
        output = row.get("output") or {}
        if key is not None and output.get(key) != value:
            continue
        return output
    raise ValueError(f"{case['case_id']}: no output for {tool} {key}={value}")


def _clean_final(
    text: str, case: dict[str, Any], *, called_csf: bool, called_modalities: set[str]
) -> str:
    kept = []
    for line in text.splitlines():
        lower = line.lower()
        if not called_csf and ("csf" in lower or "liquor" in lower):
            continue
        if "amyloid_PET" not in called_modalities and ("amyloid pet" in lower or "amyloid-pet" in lower):
            continue
        if "fdg" in lower and "FDG_PET" not in called_modalities:
            continue
        if "spect" in lower and "perfusion_SPECT" not in called_modalities and "datscan" not in lower:
            continue
        if "datscan" in lower and "DaTscan" not in called_modalities:
            continue
        if "eeg" in lower and _action(case, "analyze_eeg") is None:
            continue
        kept.append(line)
    text = "\n".join(kept)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text or (
        f"### Primary Diagnosis\n{case['ground_truth']['primary_diagnosis']}\n\n"
        "The reviewed clinical assessment, validated cognitive testing, laboratory panel and "
        "structural imaging support this diagnosis. Optional tests should not be duplicated."
    )


def revise(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "alzheimers_early":
        return False
    before = json.dumps(row, sort_keys=True)
    original = row["messages"]
    prefix = [m for m in original if m.get("role") in {"system", "user"}]
    # One system and one user prompt are expected; do not duplicate any later quoted user text.
    prefix = prefix[:2]
    if prefix and prefix[0].get("role") == "system":
        prefix[0] = dict(prefix[0])
        content = prefix[0]["content"].replace(
            "amyloid PET, FDG-PET, DaTscan, perfusion MRI",
            "amyloid PET, FDG-PET, brain perfusion SPECT, DaTscan, perfusion MRI",
        )
        if "**Clinical assessment**" not in content:
            content = content.replace(
                "  - **Specialized**: Neuropsych battery",
                "  - **Clinical assessment**: structured cognitive/behavioural assessment with informant and functional staging\n  - **Specialized**: Neuropsych battery",
            )
        prefix[0]["content"] = content
    final = next(
        (m.get("content", "") for m in reversed(original) if m.get("role") == "assistant" and not m.get("tool_calls")),
        "",
    )
    messages = list(prefix)
    diagnosis = case["ground_truth"]["primary_diagnosis"]

    clinical = _action(case, "perform_clinical_assessment")
    assert clinical is not None
    messages += _pair(
        "perform_clinical_assessment",
        {"clinical_context": "progressive cognitive or behavioural change with informant-reported functional impact", "assessment_type": "cognitive_screen"},
        _output(case, "perform_clinical_assessment"),
        "Before attributing the syndrome, I need a validated cognitive assessment, informant history and explicit functional staging.",
    )

    neuropsych = _action(case, "order_specialized_test", key="test_type", value="neuropsych_battery")
    assert neuropsych is not None
    messages += _pair(
        "order_specialized_test",
        {"clinical_context": "characterize affected cognitive domains and distinguish storage, retrieval, language, executive and visuospatial patterns", "test_type": "neuropsych_battery"},
        _output(case, "order_specialized_test", key="test_type", value="neuropsych_battery"),
        "The bedside screen establishes impairment; validated domain-level testing is required to define the phenotype and baseline.",
    )

    labs = _action(case, "interpret_labs")
    assert labs is not None
    messages += _pair(
        "interpret_labs",
        {"clinical_context": "identify reversible or contributing causes of cognitive decline", "panels": labs["tool_parameters"]["panels"], "patient_age": case["patient"]["demographics"]["age"], "patient_sex": case["patient"]["demographics"]["sex"]},
        _output(case, "interpret_labs"),
        "The clinical syndrome is documented. I will now check the reviewed metabolic, thyroid, vitamin and inflammatory panel before assigning a neurodegenerative cause.",
    )

    mri = _action(case, "analyze_brain_mri")
    if mri is not None:
        messages += _pair(
            "analyze_brain_mri",
            {"clinical_context": "structural dementia assessment after clinical and laboratory evaluation", **mri["tool_parameters"]},
            _output(case, "analyze_brain_mri"),
            "Reversible contributors have been assessed; structural MRI is the required next step to characterize atrophy and exclude vascular, mass and hydrocephalic mimics.",
        )
    else:
        ct = _action(case, "order_ct_scan")
        assert ct is not None
        messages += _pair(
            "order_ct_scan",
            {"clinical_context": "structural dementia assessment; MRI unavailable because of severe claustrophobia", "contrast": False},
            _output(case, "order_ct_scan"),
            "MRI is unavailable in this patient, so the reviewed alternative is non-contrast head CT with its sensitivity limitations stated explicitly.",
        )

    differential_style = row.get("style") == "differential_reasoned"
    called_modalities: set[str] = set()
    for modality in ("FDG_PET", "perfusion_SPECT"):
        action = _action(case, "order_advanced_imaging", key="modality", value=modality)
        if action is not None and differential_style:
            messages += _pair(
                "order_advanced_imaging",
                {"clinical_context": "dementia subtype remains uncertain after clinical assessment, labs and structural imaging", "modality": modality},
                _output(case, "order_advanced_imaging", key="modality", value=modality),
                "The core work-up leaves an atypical phenotype question. Optional functional imaging is justified now, not as a first-line test.",
            )
            called_modalities.add(modality)

    csf = _action(case, "analyze_csf")
    pet = _action(case, "order_advanced_imaging", key="modality", value="amyloid_PET")
    called_csf = csf is not None
    if csf is not None:
        messages += _pair(
            "analyze_csf",
            {"clinical_context": "single biological-confirmation route after the core dementia assessment", **csf["tool_parameters"]},
            _output(case, "analyze_csf"),
            "If biological confirmation will change management, this case uses CSF as the single route; amyloid PET should not be added after a conclusive result.",
        )
    elif pet is not None and not differential_style:
        messages += _pair(
            "order_advanced_imaging",
            {"clinical_context": "single biological-confirmation route after the core dementia assessment", "modality": "amyloid_PET"},
            _output(case, "order_advanced_imaging", key="modality", value="amyloid_PET"),
            "If biological confirmation will change management, this case uses amyloid PET as the single route; CSF Alzheimer biomarkers should not be duplicated.",
        )
        called_modalities.add("amyloid_PET")
    elif pet is None:
        raise AssertionError(f"{case['case_id']}: no biomarker route")

    dat = _action(case, "order_advanced_imaging", key="modality", value="DaTscan")
    if dat is not None and differential_style:
        messages += _pair(
            "order_advanced_imaging",
            {"clinical_context": "hallucinations, fluctuations and mild parkinsonian signs place DLB on the differential", "modality": "DaTscan"},
            _output(case, "order_advanced_imaging", key="modality", value="DaTscan"),
            "This is not routine Alzheimer imaging: soft DLB features create a separate presynaptic dopaminergic question.",
        )
        called_modalities.add("DaTscan")

    eeg = _action(case, "analyze_eeg")
    if eeg is not None:
        messages += _pair(
            "analyze_eeg",
            {"clinical_context": eeg["action"], **eeg["tool_parameters"]},
            _output(case, "analyze_eeg"),
            "EEG is removed from routine Alzheimer work-up; this case has a separate, explicit electrophysiological question that justifies the exception.",
        )

    messages.append({
        "role": "assistant",
        "content": _clean_final(
            final, case, called_csf=called_csf, called_modalities=called_modalities
        ),
    })
    row["messages"] = messages
    called = [m["tool_calls"][0]["function"]["name"] for m in messages if m.get("tool_calls")]
    row["tools_called"] = list(dict.fromkeys(called))
    row["num_tool_calls"] = len(called)
    return json.dumps(row, sort_keys=True) != before


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cases = {p.stem: json.loads(p.read_text()) for p in CASES.glob("ALZ-EARLY-*.json")}
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    changed = 0
    for row in rows:
        if row.get("condition") == "alzheimers_early":
            changed += revise(row, cases[row["case_id"]])
    rendered = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    print(f"Alzheimer trajectories changed: {changed}")
    if args.check and changed:
        raise SystemExit(1)
    if not args.check:
        args.input.write_text(rendered)


if __name__ == "__main__":
    main()
