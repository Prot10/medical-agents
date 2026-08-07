"""A red herring must point at a field that exists.

`ground_truth.red_herrings[].field_path` tells a reader — a clinical reviewer, a judge, or whoever
regenerates the corpus — which stored value is the trap. Nothing in the codebase resolves it, so it had
never been checked, and 41 pointers across 29 anti-NMDAR-receptor cases used dot-indexing
(`initial_tool_outputs.labs.panels.BMP.0`) where the other 815 use bracket-indexing
(`...panels.BMP[0]`). Those 41 pointed nowhere.

An unvalidated field is how a benchmark ends up shipping documentation that no longer matches its data —
the same failure as the stale tool catalogue the clinical reviewers were shown. The rule is cheap to
state and cheap to keep: if the path is written down, it resolves.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES = REPO_ROOT / "data/neurobench/cases"

pytestmark = pytest.mark.skipif(not CASES.exists(), reason="cases not present")

SEGMENT = re.compile(r"[^.\[\]]+|\[\d+\]")


def _resolves(document: Any, path: str) -> bool:
    current = document
    for segment in SEGMENT.findall(path):
        if segment.startswith("["):
            index = int(segment[1:-1])
            if not isinstance(current, list) or index >= len(current):
                return False
            current = current[index]
        else:
            if not isinstance(current, dict) or segment not in current:
                return False
            current = current[segment]
    return True


def test_every_red_herring_field_path_resolves() -> None:
    broken: list[str] = []
    checked = 0
    for path in sorted(CASES.glob("*.json")):
        raw = json.loads(path.read_text())
        for herring in raw["ground_truth"].get("red_herrings") or []:
            pointer = herring.get("field_path")
            if not pointer:
                continue
            checked += 1
            if not _resolves(raw, pointer):
                broken.append(f"{raw['case_id']}: {pointer}")

    assert checked > 0, "no red herring carried a field_path — the check would be vacuous"
    assert not broken, (
        "these red-herring pointers do not resolve against their own case, so the trap they name "
        f"cannot be found:\n  " + "\n  ".join(broken[:15])
    )
