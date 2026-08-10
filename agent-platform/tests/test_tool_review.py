"""Tests for the tool-review backend: catalog builder + per-reviewer store."""

from __future__ import annotations

from pathlib import Path

import pytest

from neuroagent.review_api.config import (
    AVAILABLE_DATASETS,
    CONDITION_TOOL_GUIDANCE_PATH,
    CONDITIONS_YAML_PATH,
    TOOL_COSTS_PATH,
)
from neuroagent.review_api.schemas.annotations import CaseReview
from neuroagent.review_api.schemas.tool_review import ToolReview
from neuroagent.review_api.services.dataset_loader import load_dataset
from neuroagent.review_api.services.annotation_store import AnnotationStore
from neuroagent.review_api.services.tool_catalog import build_catalog
from neuroagent.review_api.services.tool_review_store import ToolReviewStore


@pytest.fixture(scope="module")
def neurobench_catalog():
    _idx, objs = load_dataset(AVAILABLE_DATASETS["neurobench"].path)
    # The guidance path is passed exactly as app.py passes it, so the wiring is covered here
    # and not only in the file's own test.
    return build_catalog(
        "neurobench",
        objs,
        CONDITIONS_YAML_PATH,
        TOOL_COSTS_PATH,
        CONDITION_TOOL_GUIDANCE_PATH,
    )


class TestToolCatalog:
    def test_sixteen_tools(self, neurobench_catalog):
        assert len(neurobench_catalog.tools) == 16

    def test_universal_tools(self, neurobench_catalog):
        assert set(neurobench_catalog.universal_tools) == {
            "search_medical_literature",
            "check_drug_interactions",
        }

    def test_conditions_present(self, neurobench_catalog):
        keys = [c.condition for c in neurobench_catalog.conditions]
        assert len(keys) == 20
        assert len(set(keys)) == 20

    def test_alias_resolution(self, neurobench_catalog):
        """Conditions whose enum value differs from the YAML key still map."""
        by_key = {c.condition: c for c in neurobench_catalog.conditions}
        for key in ("ftd", "nph", "als"):
            assert key in by_key, f"missing aliased condition {key}"
            mapping = by_key[key]
            # Each should have resolved a real label and at least one tool.
            assert mapping.label and mapping.label != key
            assert mapping.required_tools, f"{key} has no required tools"

    def test_no_tool_is_both_required_and_optional(self, neurobench_catalog):
        for c in neurobench_catalog.conditions:
            assert not (set(c.required_tools) & set(c.optional_tools))

    def test_unmapped_tools_are_real_catalog_tools(self, neurobench_catalog):
        names = {t.name for t in neurobench_catalog.tools}
        for name in neurobench_catalog.unmapped_tools:
            assert name in names

    def test_cost_summary_is_honest(self, neurobench_catalog):
        by_name = {t.name: t for t in neurobench_catalog.tools}
        assert by_name["search_medical_literature"].cost_summary == "free"
        # MRI is base €294 (the floor), never the €116 contrast modifier alone.
        # Costs are EUR, converted from CMS PFS at 1 USD = 0.92 EUR — see
        # agent-platform/config/tools/costs.yaml.
        assert by_name["analyze_brain_mri"].cost_summary == "from €294"


class TestToolReviewStore:
    def test_load_or_init_then_roundtrip(self, tmp_path: Path):
        store = ToolReviewStore(tmp_path)
        review = store.load_or_init("neurobench", "R-001")
        assert isinstance(review, ToolReview)
        assert review.first_opened_at is not None
        assert review.completed_at is None

        # Mutate + save, then reload.
        review.completed_at = review.last_updated_at
        store.save(review)
        reloaded = store.load("neurobench", "R-001")
        assert reloaded is not None
        assert reloaded.completed_at is not None

    def test_reviewer_isolation(self, tmp_path: Path):
        store = ToolReviewStore(tmp_path)
        store.load_or_init("neurobench", "R-001")
        store.load_or_init("neurobench", "R-002")
        assert set(store.list_all_reviewers("neurobench")) == {"R-001", "R-002"}
        assert store.load("neurobench", "R-999") is None

    def test_legacy_v5_alias_reads_and_canonicalizes(self, tmp_path: Path):
        store = ToolReviewStore(tmp_path)
        review = store.load_or_init("v5", "R-001")
        assert review.dataset_version == "neurobench"
        assert (tmp_path / "neurobench" / "R-001.json").exists()
        assert store.load("v5", "R-001") is not None

    def test_rejects_bad_path_segments(self, tmp_path: Path):
        store = ToolReviewStore(tmp_path)
        with pytest.raises(ValueError):
            store.load("neurobench", "../etc")
        with pytest.raises(ValueError):
            store.load("../etc", "R-001")


class TestAnnotationStore:
    def test_legacy_v5_alias_reads_and_canonicalizes(self, tmp_path: Path):
        legacy_dir = tmp_path / "v5" / "R-001"
        legacy_dir.mkdir(parents=True)
        legacy_review = CaseReview(
            case_id="CASE-001",
            dataset_version="v5",
            reviewer_code="R-001",
        )
        (legacy_dir / "CASE-001.json").write_text(legacy_review.model_dump_json())

        store = AnnotationStore(tmp_path)
        loaded = store.load("neurobench", "R-001", "CASE-001")
        assert loaded is not None
        assert loaded.dataset_version == "neurobench"
        assert [summary.case_id for summary in store.list_for_reviewer("neurobench", "R-001")] == [
            "CASE-001"
        ]

        store.save(loaded)
        assert (tmp_path / "neurobench" / "R-001" / "CASE-001.json").exists()
        assert (tmp_path / "v5" / "R-001" / "CASE-001.json").exists()


class TestConditionToolGuidance:
    """The catalog must carry the reviewers' per-condition text, or the review app cannot
    show a reviewer what happened to the comment they wrote."""

    def test_the_catalog_serves_the_guidance(self, neurobench_catalog):
        served = {
            (m.condition, tool)
            for m in neurobench_catalog.conditions
            for tool in m.guidance
        }
        # 110 entries in the file, less the one for the retired condition, which no longer has
        # a row to hang on.
        assert len(served) == 109, len(served)
        assert ("myasthenia_gravis", "order_body_imaging") in served

    def test_a_tool_the_review_asked_to_remove_still_shows_our_answer(
        self, neurobench_catalog
    ):
        """A "REMOVE this from this condition" comment we acted on leaves no tier row behind.
        Without guidance on a tool outside both tier lists, the reviewer would see silence."""
        ms = next(
            m for m in neurobench_catalog.conditions if m.condition == "multiple_sclerosis"
        )
        assert "analyze_eeg" not in ms.required_tools + ms.optional_tools
        eeg = ms.guidance["analyze_eeg"]
        assert eeg.status == "applied"
        assert eeg.our_response

    def test_guidance_never_reports_a_tool_as_unmapped(self, neurobench_catalog):
        """A study the review asked for and no case orders yet must not be counted as an
        orphan tool: that would read as a coverage gap in the catalog rather than in the
        cases, which is the opposite of what the review established."""
        assert neurobench_catalog.unmapped_tools == []
