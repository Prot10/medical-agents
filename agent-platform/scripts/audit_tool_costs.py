"""Sanity-check tool_costs.yaml against reference ranges.

Flags entries that look suspect (likely typos, missing decimals, outdated
rates) before the cost metrics are baked into evaluation results. NOT a
substitute for a CMS PFS refresh — this is a smoke test, not an audit.

Heuristic ranges per tool category (USD, 2024 Medicare reference; ranges
are deliberately broad to flag only obvious issues):

| Tool                        | Min  | Max   |
|---                          |---   |---    |
| analyze_brain_mri base      | 250  | 500   |
| analyze_eeg routine         | 150  | 400   |
| analyze_eeg ambulatory      | 400  | 1500  |
| analyze_eeg video           | 800  | 2000  |
| analyze_ecg                 | 5    | 80    |
| interpret_labs (basic)      | 5    | 60    |
| interpret_labs (specialty)  | 100  | 3500  |
| analyze_csf base            | 150  | 400   |
| order_ct_scan base          | 100  | 400   |
| order_echocardiogram TTE    | 200  | 500   |
| order_echocardiogram TEE    | 400  | 1000  |
| order_cardiac_monitoring    | 50   | 400   |
| order_advanced_imaging      | 200  | 6000  |
| order_specialized_test      | 100  | 3500  |

Usage:
    uv run python agent-platform/scripts/audit_tool_costs.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


COSTS_YAML = Path("agent-platform/config/tool_costs.yaml")


# (path-in-config, min, max, description)
RANGE_CHECKS: list[tuple[tuple[str, ...], float, float, str]] = [
    (("tools", "analyze_brain_mri", "base"), 250, 500, "MRI base"),
    (("tools", "analyze_brain_mri", "modifiers", "contrast"), 50, 250, "MRI contrast modifier"),
    (("tools", "analyze_eeg", "by_type", "routine"), 150, 400, "EEG routine"),
    (("tools", "analyze_eeg", "by_type", "ambulatory"), 400, 1500, "EEG ambulatory"),
    (("tools", "analyze_eeg", "by_type", "video"), 800, 2000, "EEG video"),
    (("tools", "analyze_eeg", "by_type", "continuous_icu"), 600, 1800, "EEG continuous ICU"),
    (("tools", "analyze_ecg", "base"), 5, 80, "ECG"),
    (("tools", "analyze_csf", "base"), 150, 400, "CSF (LP procedure + basic studies)"),
    (("tools", "order_ct_scan", "base"), 100, 400, "CT base"),
    (("tools", "order_ct_scan", "modifiers", "contrast"), 30, 200, "CT contrast"),
    (("tools", "order_ct_scan", "modifiers", "angiography"), 100, 350, "CT angiography"),
    (("tools", "order_echocardiogram", "by_type", "TTE"), 200, 500, "Echo TTE"),
    (("tools", "order_echocardiogram", "by_type", "TEE"), 400, 1000, "Echo TEE"),
    (("tools", "order_cardiac_monitoring", "by_type", "holter_24h"), 80, 300, "Holter 24h"),
    (("tools", "order_cardiac_monitoring", "by_type", "event_monitor_30d"), 150, 600, "Event monitor"),
    (("tools", "consult_medical_specialist", "base"), 50, 200, "Specialist consult"),
]

# Specialty lab panel range (broader, just flag absurd values)
LAB_PANEL_BROAD_RANGE = (5, 3500)
ADVANCED_IMAGING_BROAD_RANGE = (200, 6000)
SPECIALIZED_TEST_BROAD_RANGE = (0, 3500)  # 0 allowed for bedside ice_pack_test


def lookup(cfg: dict, path: tuple[str, ...]):
    cur = cfg
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def main() -> int:
    if not COSTS_YAML.is_file():
        print(f"ERROR: {COSTS_YAML} not found", file=sys.stderr)
        return 2

    cfg = yaml.safe_load(COSTS_YAML.read_text())

    issues: list[str] = []

    # Targeted range checks
    for path, lo, hi, desc in RANGE_CHECKS:
        val = lookup(cfg, path)
        if val is None:
            issues.append(f"MISSING  {' > '.join(path):60s}  ({desc})")
            continue
        try:
            v = float(val)
        except (TypeError, ValueError):
            issues.append(f"NON_NUMERIC {' > '.join(path)}: {val!r}")
            continue
        if not (lo <= v <= hi):
            issues.append(
                f"OUT_OF_RANGE  {' > '.join(path):50s}  ${v:>6.0f}   "
                f"expected ${lo:.0f}-${hi:.0f}  ({desc})"
            )

    # Broad-range scans
    labs = lookup(cfg, ("tools", "interpret_labs", "by_panel")) or {}
    for panel, v in labs.items():
        try:
            v = float(v)
        except (TypeError, ValueError):
            issues.append(f"NON_NUMERIC interpret_labs[{panel}]: {v!r}")
            continue
        if not (LAB_PANEL_BROAD_RANGE[0] <= v <= LAB_PANEL_BROAD_RANGE[1]):
            issues.append(
                f"OUT_OF_RANGE  interpret_labs[{panel}]: ${v:.0f}  "
                f"expected ${LAB_PANEL_BROAD_RANGE[0]:.0f}-${LAB_PANEL_BROAD_RANGE[1]:.0f}"
            )

    adv = lookup(cfg, ("tools", "order_advanced_imaging", "by_type")) or {}
    for modality, v in adv.items():
        try:
            v = float(v)
        except (TypeError, ValueError):
            issues.append(f"NON_NUMERIC advanced_imaging[{modality}]: {v!r}")
            continue
        if not (ADVANCED_IMAGING_BROAD_RANGE[0] <= v <= ADVANCED_IMAGING_BROAD_RANGE[1]):
            issues.append(
                f"OUT_OF_RANGE  advanced_imaging[{modality}]: ${v:.0f}"
            )

    spec = lookup(cfg, ("tools", "order_specialized_test", "by_type")) or {}
    for test, v in spec.items():
        try:
            v = float(v)
        except (TypeError, ValueError):
            issues.append(f"NON_NUMERIC specialized_test[{test}]: {v!r}")
            continue
        if not (SPECIALIZED_TEST_BROAD_RANGE[0] <= v <= SPECIALIZED_TEST_BROAD_RANGE[1]):
            issues.append(
                f"OUT_OF_RANGE  specialized_test[{test}]: ${v:.0f}"
            )

    # Genetic panels
    panels = lookup(cfg, ("tools", "order_specialized_test", "genetic_panels")) or {}
    for panel, v in panels.items():
        try:
            v = float(v)
        except (TypeError, ValueError):
            issues.append(f"NON_NUMERIC genetic_panels[{panel}]: {v!r}")
            continue
        if not (300 <= v <= 5000):
            issues.append(f"OUT_OF_RANGE  genetic_panels[{panel}]: ${v:.0f}")

    # Cross-check legacy flat costs against base values
    flat = cfg.get("tool_costs", {})
    base_map = {
        "analyze_brain_mri": lookup(cfg, ("tools", "analyze_brain_mri", "base")),
        "analyze_ecg": lookup(cfg, ("tools", "analyze_ecg", "base")),
        "analyze_csf": lookup(cfg, ("tools", "analyze_csf", "base")),
        "consult_medical_specialist": lookup(cfg, ("tools", "consult_medical_specialist", "base")),
    }
    for tool, base in base_map.items():
        if base is None:
            continue
        if tool not in flat:
            issues.append(f"LEGACY_MISSING  tool_costs[{tool}]")
            continue
        try:
            if abs(float(flat[tool]) - float(base)) > 1:
                issues.append(
                    f"LEGACY_MISMATCH  tool_costs[{tool}]: flat=${flat[tool]:.0f} "
                    f"vs structured base=${base:.0f}"
                )
        except (TypeError, ValueError):
            issues.append(f"NON_NUMERIC tool_costs[{tool}]: {flat.get(tool)!r}")

    if issues:
        print(f"Found {len(issues)} potential issue(s):\n")
        for i in issues:
            print(f"  {i}")
        return 1

    print("OK — no obvious issues in tool_costs.yaml.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
