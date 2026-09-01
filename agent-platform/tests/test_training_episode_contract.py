import json
from pathlib import Path

import pytest

from neuroagent.training.data.episodes import (
    episode_to_messages,
    load_case_map,
    load_episode_records,
)


ROOT = Path(__file__).resolve().parents[2]
EPISODES = ROOT / "training_data/bootstrap/candidate_episodes.jsonl"
CASES = ROOT / "data/neurobench/cases"


def test_candidates_are_not_training_eligible_by_default():
    with pytest.raises(ValueError, match="physician_approved"):
        load_episode_records(EPISODES)


def test_candidate_bootstrap_requires_explicit_flag():
    records = load_episode_records(EPISODES, allow_candidates=True)
    assert len(records) == 649
    assert all(record.label == "candidate_not_gold" for record in records)


def test_codecs_emit_no_hidden_reasoning():
    record = load_episode_records(EPISODES, allow_candidates=True)[0]
    case = load_case_map(CASES)[record.case_id]
    for codec in ("native-tools", "json-action"):
        messages = episode_to_messages(record, case, codec=codec)
        encoded = json.dumps(messages)
        assert "<think>" not in encoded
        assert "migration.provenance" not in encoded
        assert messages[0]["role"] == "system"
