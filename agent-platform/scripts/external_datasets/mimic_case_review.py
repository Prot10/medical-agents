"""One readable Markdown file per MIMIC pilot case, for the physician who reads every case.

Sections: presentation as the agent sees it (the harness's own renderer), the HPI kept next to
every removed passage with its reason, each tool output with its origin and source table, the
policy, the diagnosis and its sources, and the clinicians' reference trajectory. The file holds
record content and is written only under the PhysioNet workspace. No record content here.
"""

from __future__ import annotations

import json


def _fmt_output(name: str, out: dict) -> str:
    return f"```json\n{json.dumps(out, indent=1, ensure_ascii=False)}\n```"


def review_md(case: dict, audit: dict) -> str:
    from neuroagent.harness.context import format_patient_info
    from neuroagent_schemas import NeuroBenchCase
    md = [f"# {case['case_id']} ({case['condition']}, provenance: record, policy draft)", ""]
    try:
        md += ["## Presentation as the agent sees it", "", "```", format_patient_info(NeuroBenchCase.model_validate(case)), "```", ""]
    except Exception as exc:  # an invalid case still gets its review file
        md += [f"(presentation not rendered: {type(exc).__name__})", ""]
    src = case["metadata"]["presentation_sources"]
    md += ["Sources: " + "; ".join(f"{k}: {v}" for k, v in src.items()), ""]
    md += ["## HPI: kept and removed", "", "**Kept (served to the agent):**", "", audit["hpi_kept"], "",
           f"**Removed ({len(audit['removed'])} passages; by class {audit['removed_counts']}):**", ""]
    for i, r in enumerate(audit["removed"], 1):
        md += [f"{i}. *{r['class']}*: {r['why']}", f"   > {r['text']}", ""]
    if audit.get("chief_complaint_triage_original") is not None:
        md += [f"**Chief complaint:** triage wrote *{audit['chief_complaint_triage_original']}*; shown: *{audit.get('chief_complaint_shown', '')}*", ""]
    if audit.get("ambiguous_blank_dropped"):
        md += ["**Not served: de-identification blank that may hide a negation (decision 16):**", ""] + [f"- {x}" for x in audit["ambiguous_blank_dropped"]] + [""]
    if audit.get("exam_cuts"):
        md += ["**Exam items cut:**", ""] + [f"- {x.get('class', '')}: {x.get('text', '')}" for x in audit["exam_cuts"]] + [""]
    if audit.get("safety_pointers"):
        md += ["**Drafted safety items (decision 18, draft for physician review):**", ""] + [f"- {x}" for x in audit["safety_pointers"]] + [""]
    if audit.get("dx_support"):
        md += [f"**Record support for the code (decision 10):** {audit['dx_support']}", ""]
    f4 = audit.get("flags_04") or {}
    if f4.get("dx_support") == "clinical_only":
        md += ["**FOR THE PHYSICIANS: clinical diagnosis only (decision 26).** No study in this case confirms the diagnosis; "
               f"basis: {f4.get('dx_support_basis', '')}", ""]
    if f4.get("known_condition_in_history"):
        md += [f"**Known condition in the history (decision 25):** {f4.get('known_condition_detail', '')}", ""]
    if audit.get("exam_notes") or audit.get("other_edits"):
        md += ["**Exam and other edits:**", ""] + [f"- {x}" for x in audit.get("exam_notes", []) + audit.get("other_edits", [])] + [""]
    md += ["**Original HPI (for comparison):**", "", f"> {audit['hpi_original']}", ""]
    md += ["## Tool outputs", ""]
    served = case["metadata"]["served"]
    for name, out in case["initial_tool_outputs"].items():
        if out is None:
            continue
        s = served.get(name, {})
        md += [f"### {name}  (origin: **{s.get('origin', '?')}**; source: {s.get('source', '?')}"
               + (f"; exam: {s['exam']}" if "exam" in s else "")
               + (f"; t = {s.get('t_h', s.get('t_first_h'))} h from ED arrival" if s.get("t_h", s.get("t_first_h")) is not None else "") + ")",
               "", _fmt_output(name, out), ""]
    for f in case["followup_outputs"]:
        s = served.get(f"followup:{f['trigger_action']}") or (served.get("ct_angiography", {}) if f["tool_name"] == "order_ct_scan" else {})
        md += [f"### follow-up `{f['trigger_action']}` ({f['tool_name']}; origin: **{s.get('origin', '?')}**; "
               f"source: {s.get('source', '?')}; exam: {s.get('exam', '?')}; t = {s.get('t_h')} h)", "", _fmt_output(f["tool_name"], f["output"]), ""]
    md += ["Any other order is answered \"Not available\" (provenance: record); knowledge tools are answered from the library.", ""]
    gt = case["ground_truth"]
    md += ["## Policy (draft, transferred from the NeuroBench cases of the condition)", "",
           "| id | importance | call | label |", "|---|---|---|---|"]
    for c in gt["action_criteria"]:
        alts = " or ".join(f"`{a['tool_name']}({json.dumps(a['required_arguments'])})`" for a in c["alternatives"])
        md.append(f"| {c['criterion_id']} | {c['importance']} | {alts} | {c['label']} |")
    md += ["", f"Sequence: {[(s['before_criterion_id'], s['after_criterion_id'], s['severity']) for s in gt['sequence_constraints']]}; "
           f"stop rule: {gt['stop_rule']}. Avoided actions, assessment recommendations and differential: none transferred "
           "(they are case-specific in NeuroBench).", ""]
    d = case["metadata"]["diagnosis_source"]
    md += ["## Diagnosis", "", f"- Principal code: {d['principal_icd']} ({d['principal_title']})",
           f"- Discharge diagnosis (note): {d['discharge_diagnosis']}",
           f"- Accepted labels: {gt['diagnosis']['accepted']}", f"- ICD codes: {gt['diagnosis']['icd_codes']}", ""]
    md += ["## Reference trajectory (clinicians, first 72 h; hours from ED arrival)", "", "| t (h) | kind | tool | what |", "|---|---|---|---|"]
    for e in case["metadata"]["reference_trajectory"]:
        md.append(f"| {e['t_hours']} | {e['kind']} | {e['tool']} | {e['what']} |")
    md += ["", f"Timing (h from ED arrival): {case['metadata']['timing_hours_from_ed_arrival']}", ""]
    return "\n".join(md)
