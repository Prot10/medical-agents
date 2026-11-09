"""Run manifest: the cases, policies, scorer and environment a run was scored against (P0-04).

Two runs are comparable only if they saw the same cases, the same policies and the same scorer.
The git commit alone does not say so: runs on the VMs start from worktrees with uncommitted
diffs applied, and a case or policy edit lands without a code change. So every benchmark and
GRPO run writes ``manifest.json`` with content hashes:

* per case, the presented case (everything but ``ground_truth``) and the policy (``ground_truth``)
  separately, so a policy review shows up without a case change and the other way round;
* the scorer's id, its scalar configuration and the source of every module the score reads;
* the tool configuration that answers the agent's orders (costs, fallback library);
* the git commit and whether the tree had uncommitted changes.

Hashes are SHA-256 of canonical JSON (sorted keys) or of the file bytes.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import subprocess
from collections.abc import Iterable
from typing import Any

import neuroagent_schemas.evaluation

from neuroagent_schemas import NeuroBenchCase

from ..datasets import REPO_ROOT
from ..tools import cost_tracker, vocabulary
from . import outcome_reward, policy_reward

SCORER_MODULES = (policy_reward, outcome_reward, neuroagent_schemas.evaluation, cost_tracker, vocabulary)
ENVIRONMENT_FILES = ("agent-platform/config/tools/costs.yaml", "agent-platform/config/tools/fallback_library.yaml")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def case_hashes(case: NeuroBenchCase) -> dict[str, str]:
    return {
        "case": _sha256(_canonical(case.model_dump(mode="json", exclude={"ground_truth"}))),
        "policy": _sha256(_canonical(case.ground_truth.model_dump(mode="json"))),
    }


def _git_state() -> dict[str, Any]:
    def git(*args: str) -> str | None:
        try:
            return subprocess.run(
                ["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True, check=True, timeout=10
            ).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None

    status = git("status", "--porcelain", "--untracked-files=no")
    return {"commit": git("rev-parse", "HEAD"), "dirty": None if status is None else bool(status)}


def run_manifest(cases: Iterable[NeuroBenchCase], scorer: Any) -> dict[str, Any]:
    per_case = {case.case_id: case_hashes(case) for case in sorted(cases, key=lambda c: c.case_id)}
    return {
        "git": _git_state(),
        "cases": {
            "n": len(per_case),
            "cases_sha256": _sha256(_canonical({k: v["case"] for k, v in per_case.items()})),
            "policies_sha256": _sha256(_canonical({k: v["policy"] for k, v in per_case.items()})),
            "per_case": per_case,
        },
        "scorer": {
            "id": scorer.scorer_id,
            "config": {k: v for k, v in vars(scorer).items() if isinstance(v, (bool, int, float, str))},
            "source_sha256": {m.__name__: _sha256(inspect.getsource(m).encode()) for m in SCORER_MODULES},
        },
        "environment_sha256": {path: _sha256((REPO_ROOT / path).read_bytes()) for path in ENVIRONMENT_FILES},
    }
