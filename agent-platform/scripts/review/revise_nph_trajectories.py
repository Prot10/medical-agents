"""Align NPH SFT trajectories with the reviewed case-level tool pathway.

The original trajectories encoded the pre-review schema: many asked for timed gait testing
through arbitrary specialized-test values (including tilt table and EMG), and many requested
routine PET or broad CSF biomarker panels.  This migration removes those calls, inserts the
reviewed clinical assessment before the tap, and serves the exact reviewed case outputs.
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


def _tool_pair(name: str, arguments: dict[str, Any], output: dict[str, Any], thought: str) -> list[dict]:
    return [
        {
            "role": "assistant",
            "content": f"<think>\n{thought}\n</think>",
            "tool_calls": [{
                "type": "function",
                "function": {"name": name, "arguments": arguments},
            }],
        },
        {"role": "tool", "content": json.dumps(output, indent=2)},
    ]


def _clean_prose(text: str, case_id: str) -> str:
    text = text.replace("neuropsychological battery", "brief cognitive assessment")
    text = text.replace("Neuropsychological battery", "Brief cognitive assessment")
    text = text.replace("neuropsychological assessment", "cognitive assessment")
    text = text.replace("neuropsychological testing", "cognitive assessment")
    text = text.replace("neuropsychology", "cognitive assessment")
    text = text.replace("neuropsych profile", "cognitive profile")
    text = text.replace("neuropsych pattern", "cognitive profile")
    text = text.replace("order_specialized_test", "objective tap assessment")
    text = re.sub(
        r"(?:well )?(?:above|exceeds) the >?20% threshold associated with shunt "
        r"responsiveness",
        "shows a clear objective change associated with shunt responsiveness",
        text,
        flags=re.IGNORECASE,
    )
    text = text.replace(">20% threshold", "prespecified objective threshold")
    text = text.replace("20% threshold", "prespecified objective threshold")

    # The old traces repeatedly reasoned from assays and PET results that the cleaned base
    # CSF/PET pathway no longer returns.  Preserve the valid clinical inference while removing
    # unsupported observations.  P01's separately ordered targeted CSF markers remain valid.
    substitutions = {
        "CSF amyloid/tau biomarkers are normal":
            "the gait-predominant phenotype is not typical of primary AD",
        "normal CSF amyloid/tau biomarkers": "the gait-predominant phenotype",
        "Normal CSF amyloid/tau biomarkers": "The gait-predominant phenotype",
        "normal CSF amyloid/tau": "the gait-predominant phenotype",
        "Normal CSF amyloid/tau": "The gait-predominant phenotype",
        "CSF amyloid/tau are only borderline and nonspecific":
            "the mixed cognitive findings are nonspecific",
        "normal CSF beta-amyloid-42, total tau, and phospho-tau":
            "a gait-predominant, objectively tap-responsive syndrome",
        "normal CSF beta-amyloid-42 and tau":
            "a gait-predominant, objectively tap-responsive syndrome",
        "normal CSF beta-amyloid/tau":
            "a gait-predominant, objectively tap-responsive syndrome",
        "normal CSF amyloid-42/tau":
            "a gait-predominant, objectively tap-responsive syndrome",
        "CSF amyloid-42, tau, and phospho-tau all normal":
            "the gait-predominant, objectively tap-responsive pattern",
        "normal CSF cytology/amyloid-tau": "an unremarkable routine CSF profile",
        "cytology/AD biomarkers unremarkable": "the routine CSF profile unremarkable",
        "CSF AD biomarkers": "targeted Alzheimer biomarkers",
        "CSF biomarkers": "targeted biomarkers",
        "reversible mimics and AD copathology excluded":
            "no inflammatory CSF pattern identified",
        "argue against a coexisting Alzheimer process driving the cognitive change":
            "and the gait-predominant tap response weigh against Alzheimer disease as the sole driver",
    }
    for old, new in substitutions.items():
        text = text.replace(old, new)
    # Conclusions are line-oriented.  Remove any bullet/thought that still relies on a result
    # the revised trajectory never obtained; retaining it would train unsupported inference.
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        lower = line.lower()
        removed_result = (
            "amyloid pet" in lower
            or "amyloid-pet" in lower
            or "fdg-pet" in lower
            or ">20%" in lower
            or "20% threshold" in lower
            or (
                "csf" in lower
                and any(term in lower for term in ("amyloid", "tau", "biomarker", "cytology"))
            )
            or (
                "normal" in lower
                and any(term in lower for term in ("amyloid/tau", "amyloid-42", "beta-amyloid"))
            )
        )
        if removed_result and not (
            case_id == "NPH-P01" and "targeted alzheimer" in lower
        ):
            continue
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines)
    text = re.sub(r"\bneuropsychological\b", "cognitive", text, flags=re.IGNORECASE)
    text = re.sub(r"\bneuropsych\b", "cognitive", text, flags=re.IGNORECASE)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def revise_trajectory(row: dict[str, Any], case: dict[str, Any]) -> bool:
    if row.get("condition") != "nph":
        return False
    before = json.dumps(row, sort_keys=True)
    case_id = row["case_id"]
    messages = row["messages"]
    revised: list[dict[str, Any]] = []
    inserted_assessment = False
    inserted_targeted = False
    has_targeted_call = any(
        call["function"].get("name") == "analyze_csf"
        and bool(call["function"].get("arguments", {}).get("special_tests"))
        for item in messages
        for call in (item.get("tool_calls") or [])
        if call.get("function")
    )
    index = 0

    while index < len(messages):
        message = messages[index]
        calls = message.get("tool_calls") if message.get("role") == "assistant" else None
        if not calls:
            copy = dict(message)
            if copy.get("role") == "assistant" and isinstance(copy.get("content"), str):
                copy["content"] = _clean_prose(copy["content"], case_id)
            revised.append(copy)
            index += 1
            continue

        function = calls[0]["function"]
        name = function["name"]
        following_tool = index + 1 < len(messages) and messages[index + 1].get("role") == "tool"

        if name in {"order_specialized_test", "order_advanced_imaging"}:
            index += 2 if following_tool else 1
            continue

        if name == "perform_clinical_assessment":
            revised.extend(_tool_pair(
                "perform_clinical_assessment",
                {
                    "clinical_context": (
                        "prespecified objective gait and brief cognitive measures immediately "
                        "before and after the large-volume CSF tap"
                    ),
                    "assessment_type": "gait_and_balance_timed",
                },
                case["initial_tool_outputs"]["clinical_assessment"],
                (
                    "Before interpreting a tap response, I need a prespecified baseline and the "
                    "same timed gait and brief cognitive measures repeated after drainage."
                ),
            ))
            inserted_assessment = True
            index += 2 if following_tool else 1
            continue

        if name == "analyze_csf":
            requested_tests = function.get("arguments", {}).get("special_tests") or []
            if requested_tests:
                followup = next(
                    (
                        item for item in case["followup_outputs"]
                        if item.get("tool_name") == "analyze_csf"
                        and item.get("tool_parameters", {}).get("special_tests") == requested_tests
                    ),
                    None,
                )
                if followup is not None:
                    revised.extend(_tool_pair(
                        "analyze_csf",
                        {
                            "clinical_context": function.get("arguments", {}).get("clinical_context", ""),
                            "special_tests": requested_tests,
                        },
                        followup["output"],
                        message.get("content", "").replace("<think>\n", "").replace("\n</think>", ""),
                    ))
                    inserted_targeted = True
                    index += 2 if following_tool else 1
                    continue
            if not inserted_assessment:
                revised.extend(_tool_pair(
                    "perform_clinical_assessment",
                    {
                        "clinical_context": (
                            "prespecified objective gait and brief cognitive measures immediately "
                            "before and after the large-volume CSF tap"
                        ),
                        "assessment_type": "gait_and_balance_timed",
                    },
                    case["initial_tool_outputs"]["clinical_assessment"],
                    (
                        "Before interpreting a tap response, I need a prespecified baseline and the "
                        "same timed gait and brief cognitive measures repeated after drainage."
                    ),
                ))
                inserted_assessment = True

            context = function.get("arguments", {}).get("clinical_context") or (
                "large-volume lumbar puncture with opening pressure and tap-test assessment"
            )
            revised.extend(_tool_pair(
                "analyze_csf",
                {"clinical_context": context},
                case["initial_tool_outputs"]["csf"],
                (
                    "Structural imaging has excluded a mass or obstructive lesion, and the baseline "
                    "has been recorded. I can now perform the large-volume tap, measure opening "
                    "pressure, and interpret the prespecified post-drainage change."
                ),
            ))

            if (
                case_id in {"NPH-P01", "NPH-P06"}
                and not inserted_targeted
                and not has_targeted_call
            ):
                tests = (
                    ["Abeta42", "phospho_tau", "total_tau"]
                    if case_id == "NPH-P01" else ["cytology", "flow_cytometry"]
                )
                followup = next(
                    item for item in case["followup_outputs"]
                    if item.get("tool_name") == "analyze_csf"
                    and item.get("tool_parameters", {}).get("special_tests") == tests
                )
                question = (
                    "evaluate the case-specific suspicion of concurrent Alzheimer pathology"
                    if case_id == "NPH-P01"
                    else "exclude leptomeningeal carcinomatosis in the setting of active cancer"
                )
                revised.extend(_tool_pair(
                    "analyze_csf",
                    {"clinical_context": question, "special_tests": tests},
                    followup["output"],
                    f"This patient has a separate, case-specific CSF question: {question}.",
                ))
                inserted_targeted = True

            index += 2 if following_tool else 1
            continue

        copy = json.loads(json.dumps(message))
        copy["content"] = _clean_prose(copy.get("content") or "", case_id)
        revised.append(copy)
        if following_tool:
            revised.append(messages[index + 1])
        index += 2 if following_tool else 1

    if not inserted_assessment:
        # Defensive fallback for a trace that concluded without ordering the required tap.
        insert_at = max(1, len(revised) - 1)
        revised[insert_at:insert_at] = _tool_pair(
            "perform_clinical_assessment",
            {
                "clinical_context": "objective pre/post tap gait and brief cognitive assessment",
                "assessment_type": "gait_and_balance_timed",
            },
            case["initial_tool_outputs"]["clinical_assessment"],
            "I need objective pre/post gait and cognitive measures before concluding.",
        )

    row["messages"] = revised
    row["tools_called"] = [
        call["function"]["name"]
        for message in revised
        for call in (message.get("tool_calls") or [])
    ]
    row["num_tool_calls"] = len(row["tools_called"])
    return json.dumps(row, sort_keys=True) != before


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cases = {
        path.stem: json.loads(path.read_text())
        for path in CASES.glob("NPH-*.json")
    }
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    changed = sum(
        revise_trajectory(row, cases[row["case_id"]])
        for row in rows if row.get("condition") == "nph"
    )
    nph = sum(row.get("condition") == "nph" for row in rows)
    print(f"{'would change' if args.dry_run else 'changed'} {changed}/{nph} NPH trajectories")
    if not args.dry_run:
        args.input.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
