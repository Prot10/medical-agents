"""SFT examples are the inference transcript, gated by review provenance."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from neuroagent.harness import transcript
from neuroagent.training.data.episodes import EpisodeRecord, load_episode_records, sft_rows
from neuroagent_schemas import (
    ActionProposed,
    AssessmentSubmitted,
    ClinicalEpisode,
    NeuroBenchCase,
    ObservationReceived,
    PluginEvent,
    RunCompleted,
    RunFailed,
    RunStarted,
    SubmitAssessment,
    ToolAction,
)

ROOT = Path(__file__).resolve().parents[2]
CASE = NeuroBenchCase.model_validate_json((ROOT / "data/neurobench/cases/SE-M02.json").read_text())


def episode(*, completed: bool = True) -> ClinicalEpisode:
    assessment = SubmitAssessment(
        primary_diagnosis="status epilepticus", confidence=0.8, urgency="emergent"
    )
    events = [
        RunStarted(turn=0, case_id=CASE.case_id, profile_id="p", model_id="m"),
        ActionProposed(turn=1, action=ToolAction(tool_name="analyze_eeg", arguments={"eeg_type": "routine"})),
        PluginEvent(turn=1, namespace="react.rationale", payload={"value": "<think>secret</think>"}),
        ObservationReceived(turn=1, tool_name="analyze_eeg", success=True, output={"impression": "NCSE"}),
        ActionProposed(turn=2, action=assessment),
        AssessmentSubmitted(turn=2, assessment=assessment),
    ]
    events.append(RunCompleted(turn=2) if completed else RunFailed(turn=2, reason="model_error"))
    return ClinicalEpisode(events=events)


def record(label: str, **kwargs) -> str:
    return EpisodeRecord(
        candidate_id="c1", case_id=CASE.case_id, label=label, episode=episode(**kwargs)
    ).model_dump_json()


def test_candidates_are_not_training_eligible_by_default(tmp_path):
    path = tmp_path / "episodes.jsonl"
    path.write_text(record("candidate_not_gold") + "\n")
    with pytest.raises(ValueError, match="physician_approved"):
        load_episode_records(path)
    assert len(load_episode_records(path, allow_candidates=True)) == 1
    path.write_text(record("physician_approved") + "\n")
    assert load_episode_records(path)[0].label == "physician_approved"


def test_failed_episodes_are_rejected_as_training_examples():
    with pytest.raises(ValueError, match="completed"):
        EpisodeRecord(candidate_id="c", case_id=CASE.case_id, label="physician_approved", episode=episode(completed=False))


def test_sft_rows_replay_the_inference_transcript_without_rationale():
    item = EpisodeRecord.model_validate_json(record("physician_approved"))
    rows = sft_rows(item, CASE)
    assert len(rows) == 2  # one example per model turn
    expected = transcript(CASE, item.episode)
    for row in rows:
        assert row["prompt"] + row["completion"] == expected[: len(row["prompt"]) + 1]
        assert row["completion"][0]["role"] == "assistant"
        assert row["tools"][-1]["function"]["name"] == "submit_assessment"
    assert "secret" not in json.dumps(rows)
