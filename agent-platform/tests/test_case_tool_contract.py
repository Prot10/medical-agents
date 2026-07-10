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
from validate_cases import _tool_schemas, validate_case  # noqa: E402

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
        """No ground-truth value may fall back to a default cost rate."""
        modalities, tests = set(advanced_imaging_modalities()), set(specialized_test_types())
        unpriced: list[str] = []
        for path in CASE_FILES:
            gt = json.loads(path.read_text())["ground_truth"]
            entries = gt["optimal_actions"] + gt["useless_tools"] + gt["harmful_tools"]
            for entry in entries:
                params = entry.get("tool_parameters") or {}
                tool = entry.get("tool_name")
                if tool == "order_advanced_imaging" and "modality" in params:
                    if params["modality"] not in modalities:
                        unpriced.append(f"{path.stem}: modality={params['modality']}")
                if tool == "order_specialized_test" and "test_type" in params:
                    value = params["test_type"]
                    if value not in tests and not value.startswith("genetic_panel:"):
                        unpriced.append(f"{path.stem}: test_type={value}")
        assert unpriced == [], unpriced
