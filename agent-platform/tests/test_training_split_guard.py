"""No test-split case reaches training: GRPO case lists, SFT episodes and the episode export (P0-03)."""

from __future__ import annotations

import pytest

from neuroagent.datasets import DATASETS, DEFAULT_DATASET_VERSION, refuse_test_cases, split_case_ids
from neuroagent.training.data.export_episodes import export
from neuroagent.training.train_sft import build_examples
from neuroagent_schemas import ClinicalEpisode, RunCompleted, RunStarted

SPLITS = DATASETS[DEFAULT_DATASET_VERSION].path
TEST = split_case_ids(SPLITS, "test")
TRAIN = split_case_ids(SPLITS, "train")


def completed_episode(case_id: str) -> ClinicalEpisode:
    return ClinicalEpisode(events=[RunStarted(turn=0, case_id=case_id, profile_id="p", model_id="m"), RunCompleted(turn=1)])


def test_the_splits_are_disjoint_and_cover_the_benchmark():
    assert not set(TEST) & set(TRAIN)
    assert len(TEST) == 100 and len(TRAIN) == 500


def test_a_training_list_with_one_test_case_is_refused():
    refuse_test_cases(TRAIN)
    with pytest.raises(ValueError, match=TEST[0]):
        refuse_test_cases([*TRAIN[:5], TEST[0]])


def test_the_export_refuses_a_run_that_holds_a_test_case(tmp_path):
    run = tmp_path / "run"
    (run / "episodes").mkdir(parents=True)
    for case_id in (TRAIN[0], TEST[0]):
        (run / "episodes" / f"{case_id}.json").write_text(completed_episode(case_id).model_dump_json())
    output = tmp_path / "records.jsonl"
    with pytest.raises(ValueError, match="test-split"):
        export([run], output)
    assert not output.exists()
    (run / "episodes" / f"{TEST[0]}.json").unlink()
    assert export([run], output) == 1


def test_sft_refuses_episodes_of_test_cases_before_tokenizing(tmp_path):
    # A record file written by hand, or by an export older than the guard, is caught by SFT itself.
    records = tmp_path / "records.jsonl"
    record = '{"candidate_id": "x", "case_id": "%s", "label": "candidate_not_gold", "provenance": {}, "episode": %s}'
    records.write_text(record % (TEST[0], completed_episode(TEST[0]).model_dump_json()) + "\n")
    with pytest.raises(ValueError, match="test-split"):
        build_examples("qwen3.5-9b", str(records), str(SPLITS / "cases"), tokenizer=None, allow_candidates=True)
