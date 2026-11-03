"""Load, edit and save NeuroBench cases safely during the October 2026 review round.

Library use (from any directory):

    import sys; sys.path.insert(0, "/Users/andrea/Documents/medical-agents/data/review/round-2026-10/bin")
    from case_io import load, save
    case = load("GLIO-HG-RS01")           # plain dict
    case["ground_truth"]["action_criteria"][3]["label"] = "..."
    save(case)                              # validates, then writes atomically in canonical form

Command line (run with `uv run python` from the repository root):

    uv run python data/review/round-2026-10/bin/case_io.py validate GLIO-HG-RS01 GLIO-HG-RS02
    uv run python data/review/round-2026-10/bin/case_io.py check GLIO-HG-RS01 GLIO-HG-RS02
    uv run python data/review/round-2026-10/bin/case_io.py diff GLIO-HG-RS01

`save` refuses a case that fails the `NeuroBenchCase` schema, and never changes `condition` or
`case_id`. `check` validates the schema, runs the synonym guard and the full test suite, and
prints only the failures that name the given cases (plus the condition-wide failures of their
condition). `diff` shows the change against the last commit.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/andrea/Documents/medical-agents")
CASES = ROOT / "data/neurobench/cases"
# Tests whose claims are maintained centrally after the round (do not chase these per case).
CENTRAL_TESTS = ("test_guidance_claims",)


def path_of(case_id: str) -> Path:
    path = CASES / f"{case_id}.json"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def load(case_id: str) -> dict:
    return json.loads(path_of(case_id).read_text())


def dumps(case: dict) -> str:
    return json.dumps(case, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def validate(case: dict) -> None:
    from neuroagent_schemas import NeuroBenchCase

    NeuroBenchCase.model_validate(case)


def save(case: dict) -> Path:
    """Validate, then atomically replace the case file in canonical form."""
    case_id = case["case_id"]
    path = path_of(case_id)
    before = json.loads(path.read_text())
    if before["condition"] != case["condition"]:
        raise ValueError(f"{case_id}: condition may not change ({before['condition']} -> {case['condition']})")
    validate(case)
    text = dumps(case)
    fd, tmp = tempfile.mkstemp(dir=CASES, prefix=f".{case_id}.", suffix=".tmp")
    with os.fdopen(fd, "w") as handle:
        handle.write(text)
    os.replace(tmp, path)
    return path


def _condition_prefix(case_id: str) -> str:
    return re.sub(r"-R?[MPS]\d+$", "", case_id)


def check(case_ids: list[str]) -> int:
    status = 0
    for case_id in case_ids:
        try:
            validate(load(case_id))
            print(f"schema OK      {case_id}")
        except Exception as exc:  # noqa: BLE001 - report every schema failure
            print(f"schema FAILED  {case_id}: {exc}")
            status = 1
    synonyms = subprocess.run(
        ["uv", "run", "python", "agent-platform/scripts/validation/apply_diagnosis_synonyms.py", "--check"],
        cwd=ROOT, capture_output=True, text=True,
    )
    named = [line for line in (synonyms.stdout + synonyms.stderr).splitlines() if any(c in line for c in case_ids)]
    print("synonym guard  " + ("OK" if not named else "WOULD CHANGE:\n  " + "\n  ".join(named)))
    status |= bool(named)
    tests = subprocess.run(
        ["uv", "run", "pytest", "agent-platform/tests", "packages/neuroagent-schemas/tests", "-q",
         "-p", "no:cacheprovider", "--ignore=agent-platform/tests/test_grpo_rollout.py", "-rf", "--tb=line"],
        cwd=ROOT, capture_output=True, text=True,
    )
    prefixes = {_condition_prefix(c) for c in case_ids}
    out = tests.stdout.splitlines()
    mine = [
        line for line in out
        if (any(c in line for c in case_ids) or any(re.search(rf"\b{re.escape(p)}-R?[MPS]?\d*\b", line) for p in prefixes))
        and not any(t in line for t in CENTRAL_TESTS)
    ]
    print(f"tests          {out[-1] if out else tests.stderr[-500:]}")
    if mine:
        print("failures naming these cases or their condition:")
        for line in dict.fromkeys(mine):
            print("  " + line[:600])
        status = 1
    else:
        print("no test failure names these cases (other conditions may be mid-edit; central claim tests are handled later)")
    return status


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    command, case_ids = argv[0], argv[1:]
    if command == "validate":
        for case_id in case_ids:
            validate(load(case_id))
            print(f"schema OK  {case_id}")
        return 0
    if command == "check":
        return check(case_ids)
    if command == "diff":
        return subprocess.call(["git", "diff", "--word-diff", "--", *[str(path_of(c)) for c in case_ids]], cwd=ROOT)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
