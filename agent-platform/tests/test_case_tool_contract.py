"""The gate that keeps the benchmark and the tools from drifting apart again.

Three artifacts used to carry their own copy of the tool vocabulary — the tool schemas,
`costs.yaml`, and the 600 cases — and they diverged silently. Nothing failed; the agent was
simply unable to order studies the ground truth required, and `CostTracker` quietly priced
the wrong workup.

These tests make that impossible to reintroduce:

* every case satisfies the contract in `scripts/validation/validate_cases.py`
* a perfect agent scores perfectly on every case
* the tool enums are exactly the priced vocabulary
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = REPO_ROOT / "data" / "neurobench" / "cases"
sys.path.insert(0, str(REPO_ROOT / "agent-platform" / "scripts" / "validation"))

from check_perfect_agent import perfect_trace  # noqa: E402
from check_trajectories import _as_trace, check_trajectory  # noqa: E402,F401
from validate_cases import CATCHALL_PARAM, _tool_schemas, validate_case  # noqa: E402

from neuroagent.evaluation.metrics import MetricsCalculator  # noqa: E402
from neuroagent.tools.tool_registry import ToolRegistry  # noqa: E402
from neuroagent.tools.vocabulary import (  # noqa: E402
    advanced_imaging_modalities,
    by_type_values,
    specialized_test_types,
)
from neuroagent_schemas import NeuroBenchCase  # noqa: E402

CASE_FILES = sorted(CASES_DIR.glob("*.json"))


def _case_id(path: Path) -> str:
    return path.stem


@pytest.fixture(scope="module")
def schemas() -> dict:
    return _tool_schemas()


class TestCaseToolContract:
    """Every case names real tools and passes them arguments those tools accept."""

    def test_all_cases_present(self):
        assert len(CASE_FILES) == 600

    @pytest.mark.parametrize("path", CASE_FILES, ids=_case_id)
    def test_case_satisfies_contract(self, path: Path, schemas: dict):
        issues = validate_case(json.loads(path.read_text()), schemas)
        assert issues == [], "\n".join(f"{i['code']}: {i['detail']}" for i in issues)


class TestPerfectAgentIsPerfect:
    """An agent that does exactly what the ground truth says must score perfectly.

    When this fails, the case is unreachable: no model can attain its ceiling, and every
    reported score against it is measured against an impossible target.
    """

    @pytest.mark.parametrize("path", CASE_FILES, ids=_case_id)
    def test_ground_truth_is_attainable(self, path: Path, schemas: dict):
        case = NeuroBenchCase.model_validate(json.loads(path.read_text()))
        metrics = MetricsCalculator().compute_all(perfect_trace(case, schemas), case.ground_truth)

        if case.ground_truth.optimal_actions:
            assert metrics.action_recall == 1.0
        if metrics.required_total:
            assert metrics.required_coverage == 1.0
        assert metrics.useless_calls == 0
        assert metrics.harmful_calls == 0


class TestVocabularyHasOneSource:
    """The tool enums are generated from costs.yaml, so a term cannot exist without a price."""

    @pytest.fixture(scope="class")
    def registry(self) -> ToolRegistry:
        return ToolRegistry.create_default_registry()

    def _enum(self, registry: ToolRegistry, tool: str, param: str) -> list[str]:
        defn = registry.get_tool(tool).get_tool_definition()
        return defn["function"]["parameters"]["properties"][param]["enum"]

    def test_advanced_imaging_enum_matches_costs(self, registry):
        assert self._enum(registry, "order_advanced_imaging", "modality") == advanced_imaging_modalities()

    def test_specialized_test_enum_matches_costs(self, registry):
        assert self._enum(registry, "order_specialized_test", "test_type") == specialized_test_types()

    def test_cardiac_monitoring_enum_matches_costs(self, registry):
        assert self._enum(registry, "order_cardiac_monitoring", "monitor_type") == by_type_values(
            "order_cardiac_monitoring"
        )

    def test_every_case_value_is_priced(self, schemas):
        """No ground-truth value may fall back to a default cost rate.

        Covers all six discriminating parameters, not just the two original catchall tools.
        Checking only those two left the four post-review tools unguarded, and the validator
        had the mirror-image bug: it checked *their* values against the specialized-test
        vocabulary, so `study=chest_CTA` was reported as illegal while `study=emg_ncs` would
        have passed. Both blind spots were invisible while no case used the parameters.
        """
        unpriced: list[str] = []
        for path in CASE_FILES:
            gt = json.loads(path.read_text())["ground_truth"]
            entries = gt["optimal_actions"] + gt["useless_tools"] + gt["harmful_tools"]
            for entry in entries:
                params = entry.get("tool_parameters") or {}
                key_and_predicate = CATCHALL_PARAM.get(entry.get("tool_name"))
                if key_and_predicate is None:
                    continue
                key, is_valid = key_and_predicate
                if key in params and not is_valid(str(params[key])):
                    unpriced.append(f"{path.stem}: {key}={params[key]}")
        assert unpriced == [], unpriced

    @pytest.mark.parametrize("tool_name", sorted(CATCHALL_PARAM))
    def test_each_tool_is_validated_against_its_own_vocabulary(self, tool_name, registry):
        """The validator's predicate must accept exactly that tool's enum, and no other's."""
        key, is_valid = CATCHALL_PARAM[tool_name]
        own = self._enum(registry, tool_name, key)
        assert own, f"{tool_name}.{key} has no enum to validate against"
        assert all(is_valid(value) for value in own), (
            f"{tool_name}: the validator rejects legal values of its own vocabulary"
        )
        foreign = {
            value
            for other, (other_key, _) in CATCHALL_PARAM.items()
            if other != tool_name
            for value in self._enum(registry, other, other_key)
        } - set(own)
        leaked = sorted(value for value in foreign if is_valid(value))
        assert not leaked, f"{tool_name}: validator also accepts another tool's terms: {leaked}"


class TestGoldTrajectoriesSatisfyTheContract:
    """The trajectories are training data. If a tool changes shape under them, SFT trains on
    calls the agent can no longer make — and nothing else in the suite would notice."""

    @pytest.fixture(scope="class")
    def trajectories(self) -> list[dict]:
        path = REPO_ROOT / "training_data" / "gold_trajectories" / "trajectories.jsonl"
        if not path.exists():
            pytest.skip("gold trajectories not present")
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

    @pytest.fixture(scope="class")
    def cases_by_id(self) -> dict:
        from neuroagent_schemas import NeuroBenchCase as _Case
        return {
            c.case_id: c
            for c in (_Case.model_validate(json.loads(p.read_text())) for p in CASE_FILES)
        }

    def test_every_tool_call_satisfies_the_contract(self, trajectories, cases_by_id, schemas):
        from check_trajectories import check_trajectory

        failures = []
        for trajectory in trajectories:
            issues = check_trajectory(trajectory, cases_by_id[trajectory["case_id"]], schemas)
            if issues:
                failures.append((trajectory["case_id"], trajectory.get("style"), issues[:2]))
        assert failures == [], failures[:5]

    def test_no_trajectory_teaches_a_useless_or_harmful_call(self, trajectories, cases_by_id):
        from check_trajectories import _as_trace

        calculator = MetricsCalculator()
        offenders = []
        for trajectory in trajectories:
            gt = cases_by_id[trajectory["case_id"]].ground_truth
            m = calculator.compute_all(_as_trace(trajectory), gt)
            if m.useless_calls or m.harmful_calls or not m.diagnostic_accuracy_top1:
                offenders.append((trajectory["case_id"], trajectory.get("style")))
        assert offenders == [], offenders[:5]
