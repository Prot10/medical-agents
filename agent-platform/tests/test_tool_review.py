"""Tests for the tool-review backend: catalog builder + per-reviewer store."""

from __future__ import annotations

from pathlib import Path

import pytest

from neuroagent.review_api.config import (
    AVAILABLE_DATASETS,
    CONDITIONS_YAML_PATH,
    TOOL_COSTS_PATH,
)
from neuroagent.review_api.schemas.tool_review import ToolReview
from neuroagent.review_api.services.dataset_loader import load_dataset
from neuroagent.review_api.services.tool_catalog import build_catalog
from neuroagent.review_api.services.tool_review_store import ToolReviewStore


@pytest.fixture(scope="module")
def v5_catalog():
    _idx, objs = load_dataset(AVAILABLE_DATASETS["v5"]["path"])
    return build_catalog("v5", objs, CONDITIONS_YAML_PATH, TOOL_COSTS_PATH)


class TestToolCatalog:
    def test_thirteen_tools(self, v5_catalog):
        assert len(v5_catalog.tools) == 13

    def test_universal_tools(self, v5_catalog):
        assert set(v5_catalog.universal_tools) == {
            "search_medical_literature",
            "check_drug_interactions",
            "consult_medical_specialist",
        }

    def test_conditions_present(self, v5_catalog):
        # v5 has 20 distinct conditions, each appears once in the catalog.
        keys = [c.condition for c in v5_catalog.conditions]
        assert len(keys) == 20
        assert len(set(keys)) == 20

    def test_alias_resolution(self, v5_catalog):
        """Conditions whose enum value differs from the YAML key still map."""
        by_key = {c.condition: c for c in v5_catalog.conditions}
        for key in ("ftd", "nph", "als"):
            assert key in by_key, f"missing aliased condition {key}"
            mapping = by_key[key]
            # Each should have resolved a real label and at least one tool.
            assert mapping.label and mapping.label != key
            assert mapping.required_tools, f"{key} has no required tools"

    def test_no_tool_is_both_required_and_optional(self, v5_catalog):
        for c in v5_catalog.conditions:
            assert not (set(c.required_tools) & set(c.optional_tools))

    def test_unmapped_tools_are_real_catalog_tools(self, v5_catalog):
        names = {t.name for t in v5_catalog.tools}
        for name in v5_catalog.unmapped_tools:
            assert name in names

    def test_cost_summary_is_honest(self, v5_catalog):
        by_name = {t.name: t for t in v5_catalog.tools}
        assert by_name["search_medical_literature"].cost_summary == "free"
        # MRI is base $320 (the floor), never the $126 contrast modifier alone.
        assert by_name["analyze_brain_mri"].cost_summary == "from $320"


class TestToolReviewStore:
    def test_load_or_init_then_roundtrip(self, tmp_path: Path):
        store = ToolReviewStore(tmp_path)
        review = store.load_or_init("v5", "R-001")
        assert isinstance(review, ToolReview)
        assert review.first_opened_at is not None
        assert review.completed_at is None

        # Mutate + save, then reload.
        review.completed_at = review.last_updated_at
        store.save(review)
        reloaded = store.load("v5", "R-001")
        assert reloaded is not None
        assert reloaded.completed_at is not None

    def test_reviewer_isolation(self, tmp_path: Path):
        store = ToolReviewStore(tmp_path)
        store.load_or_init("v5", "R-001")
        store.load_or_init("v5", "R-002")
        assert set(store.list_all_reviewers("v5")) == {"R-001", "R-002"}
        assert store.load("v5", "R-999") is None

    def test_rejects_bad_path_segments(self, tmp_path: Path):
        store = ToolReviewStore(tmp_path)
        with pytest.raises(ValueError):
            store.load("v5", "../etc")
        with pytest.raises(ValueError):
            store.load("not-a-version", "R-001")
