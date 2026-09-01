from __future__ import annotations

import json
from pathlib import Path

import pytest
from neuroagent_schemas import ClinicalEpisode, NeuroBenchCase, ToolAction
from pydantic import ValidationError


ROOT = Path(__file__).resolve().parents[3]


def test_every_case_uses_strict_v2_policy_schema():
    paths = sorted((ROOT / "data/neurobench/cases").glob("*.json"))
    assert len(paths) == 600
    for path in paths:
        case = NeuroBenchCase.model_validate_json(path.read_text())
        assert case.schema_version == "2.0"
        assert case.ground_truth.review_status.value in {
            "draft", "needs_revision", "approved"
        }


def test_pre_v2_case_shape_is_rejected():
    path = next((ROOT / "data/neurobench/cases").glob("*.json"))
    raw = json.loads(path.read_text())
    del raw["schema_version"]
    with pytest.raises(ValidationError):
        NeuroBenchCase.model_validate(raw)


def test_action_union_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        ToolAction(tool_name="analyze_eeg", arguments={}, thought="hidden")


def test_episode_is_append_only_event_shaped():
    episode = ClinicalEpisode()
    assert episode.events == []
