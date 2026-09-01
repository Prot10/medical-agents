"""The gate on the *fourth* copy of the tool vocabulary: the review app's mirror.

The schema contract tests lock the tool schemas, `costs.yaml` and the 600 cases
together. An earlier version missed `review_api/services/tool_io.py`, which carries its own mirror of the
agent-facing `parameter_schema` dicts because `tools/` is deliberately not shipped to the
review VPS. That mirror then drifted, and the drift was invisible: nothing failed, the
review app simply served an obsolete catalog.

The consequence was not theoretical. Between 2026-07-19 and 2026-07-27 two clinical
reviewers assessed the tool catalog through that app and saw 9 of 21 specialized tests,
6 of 12 imaging modalities and 4 of 6 cardiac monitors. Six studies they reported as
missing — single-fibre EMG, respiratory function, OCT, transcranial Doppler, MR venography,
cardiac MRI — were already orderable. Their review time was spent against a false picture of
the action space.

These tests make the mirror's correctness a CI property. The tool class is the truth.
"""

from __future__ import annotations

import pytest

from neuroagent.review_api.services.tool_io import (
    _COSTS_DERIVED_ENUMS,
    parameters_for,
)
from neuroagent.tools.tool_registry import ToolRegistry
from neuroagent.tools.vocabulary import (
    advanced_imaging_modalities,
    by_type_values,
    genetic_panels,
    mri_protocols,
    specialized_test_types,
)


@pytest.fixture(scope="module")
def real_schemas() -> dict[str, dict]:
    """The agent-facing parameter schemas, straight off the registered tool classes."""
    registry = ToolRegistry.create_default_registry()
    return {
        name: tool.get_tool_definition()["function"]["parameters"]
        for name, tool in registry.tools.items()
    }


def test_mirror_covers_every_registered_tool(real_schemas):
    missing = sorted(name for name in real_schemas if parameters_for(name) is None)
    assert not missing, (
        f"tool_io mirror has no entry for {missing} — reviewers would see an empty "
        "parameter form for a tool the agent can call"
    )


def test_tool_io_schemas_match(real_schemas):
    """The review mirror must equal every real schema, parameter for parameter."""
    for tool_name, schema in real_schemas.items():
        assert parameters_for(tool_name) == schema, (
            f"{tool_name}: review_api/services/tool_io.py has drifted from the tool class"
        )


class TestCostsDerivedVocabularies:
    """Vocabulary-bearing enums come from costs.yaml, never from a literal in the mirror."""

    @pytest.mark.parametrize(
        "tool_name,parameter,expected",
        [
            ("order_advanced_imaging", "modality", advanced_imaging_modalities),
            ("order_specialized_test", "test_type", specialized_test_types),
            (
                "order_cardiac_monitoring",
                "monitor_type",
                lambda: by_type_values("order_cardiac_monitoring"),
            ),
            # The three that were hardcoded in *both* copies until the cardiac-syncope pass,
            # so each could drift from costs.yaml on its own.
            (
                "order_echocardiogram",
                "echo_type",
                lambda: by_type_values("order_echocardiogram"),
            ),
            ("analyze_eeg", "eeg_type", lambda: by_type_values("analyze_eeg")),
            ("analyze_brain_mri", "protocol", mri_protocols),
        ],
    )
    def test_enum_matches_priced_vocabulary(self, tool_name, parameter, expected):
        schema = parameters_for(tool_name)
        assert schema["properties"][parameter]["enum"] == expected()

    @pytest.mark.parametrize("key", sorted(_COSTS_DERIVED_ENUMS))
    def test_no_hardcoded_enum_left_behind(self, key):
        """The literal must be absent from the source, or it can go stale again."""
        from neuroagent.review_api.services.tool_io import _TOOL_PARAMETERS

        tool_name, parameter = key
        spec = _TOOL_PARAMETERS[tool_name]["properties"][parameter]
        assert "enum" not in spec, (
            f"{tool_name}.{parameter} carries a literal enum in _TOOL_PARAMETERS; it is a "
            "costs-derived vocabulary and must be injected by parameters_for()"
        )

    def test_genetic_panels_are_interpolated(self):
        """`genetic_panel:<panel>` lives in prose, so the prose must be generated too."""
        description = parameters_for("order_specialized_test")["properties"]["test_type"][
            "description"
        ]
        assert "{genetic_panels}" not in description, "placeholder was not substituted"
        for panel in genetic_panels():
            assert panel in description, f"genetic panel {panel!r} missing from description"